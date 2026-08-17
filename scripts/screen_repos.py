#!/usr/bin/env python3
"""Screen GitHub repos for outside-contributor PR merge likelihood."""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

REPOS = sys.argv[1:] if len(sys.argv) > 1 else [
    "vllm-project/vllm",
    "py-pdf/pypdf",
    "huggingface/transformers",
    "unstructured-io/unstructured",
]

STALE_CUTOFF = datetime(2026, 5, 19, tzinfo=timezone.utc)  # 90d before 2026-08-17
BOT_RE = re.compile(r"\[bot\]|bot$", re.IGNORECASE)

last_call = 0.0


def gh_api(path, paginate=False, max_pages=1):
    """Call gh api with rate-limit pacing. Returns parsed JSON (list merge)."""
    global last_call
    delay = 1.5 - (time.time() - last_call)
    if delay > 0:
        time.sleep(delay)
    cmd = ["gh", "api", path]
    if paginate:
        cmd.append("--paginate")
    r = subprocess.run(cmd, capture_output=True, text=True)
    last_call = time.time()
    if r.returncode != 0:
        err = r.stderr.strip()
        if "403" in err or "rate limit" in err.lower():
            print(f"  !! 403 rate limit on {path} — sleeping 65s", flush=True)
            time.sleep(65)
            r = subprocess.run(cmd, capture_output=True, text=True)
            last_call = time.time()
        if r.returncode != 0:
            raise RuntimeError(f"gh api {path} failed: {r.stderr[:500]}")
    if not r.stdout.strip():
        return []
    return json.loads(r.stdout)


def fetch_pages(path, n):
    """Fetch n pages of per_page=100, concatenated."""
    out = []
    for page in range(1, n + 1):
        sep = "&" if "?" in path else "?"
        data = gh_api(f"{path}{sep}per_page=100&page={page}")
        out.extend(data)
        if len(data) < 100:
            break
    return out


def screen(repo):
    print(f"\n===== {repo} =====", flush=True)
    row = {"repo": repo}

    # ---- STEP 1: open unassigned issues (paginate to be accurate) ----
    issues = fetch_pages(f"repos/{repo}/issues?state=open", n=5)
    unassigned = [i for i in issues if i.get("pull_request") is None and i.get("assignee") is None]
    bug_labelled = [i for i in unassigned if any(
        (l.get("name", "")).lower() in ("bug", "bugfix", "type:bug", "kind/bug")
        for l in i.get("labels", [])
    )]
    row["open_unassigned_issues"] = len(unassigned)
    row["bug_labelled"] = len(bug_labelled)
    row["issue_pages_seen"] = min(5, (len(issues) + 99) // 100)
    print(f"  open unassigned issues (first {row['issue_pages_seen']*100} scanned): {len(unassigned)} | bug-labeled: {len(bug_labelled)}", flush=True)
    # candidate issues: bug-labeled, unassigned, sorted newest
    cand = sorted(bug_labelled, key=lambda i: i["created_at"], reverse=True)
    row["candidates"] = [(i["number"], i["title"][:90], i["created_at"][:10]) for i in cand[:8]]

    # ---- STEP 2: stale open PR share (first 200 open PRs) ----
    prs = fetch_pages(f"repos/{repo}/pulls?state=open", n=2)
    if prs:
        created = [datetime.fromisoformat(p["created_at"].replace("Z", "+00:00")) for p in prs]
        stale = sum(1 for c in created if c < STALE_CUTOFF)
        row["open_prs_sampled"] = len(prs)
        row["stale_pct"] = round(100.0 * stale / len(prs), 1)
        print(f"  open PRs sampled: {len(prs)} | stale (>90d): {stale} = {row['stale_pct']}%", flush=True)
    else:
        row["stale_pct"] = None
        print("  no open PRs", flush=True)

    # ---- STEP 3: outsider merge share (first 200 recently-updated closed PRs) ----
    closed = fetch_pages(f"repos/{repo}/pulls?state=closed&sort=updated&direction=desc", n=2)
    merged = [p for p in closed if p.get("merged_at")]
    nonbot = [p for p in merged if not BOT_RE.search(p["user"]["login"])]
    row["closed_prs_sampled"] = len(closed)
    row["merged_sampled"] = len(merged)
    row["nonbot_merged"] = len(nonbot)
    if nonbot:
        from collections import Counter
        cnt = Counter(p["user"]["login"] for p in nonbot)
        top5 = {a for a, _ in cnt.most_common(5)}
        outside = [p for p in nonbot if p["user"]["login"] not in top5]
        one_offs = [a for a, c in cnt.items() if c == 1]
        row["outside_pct"] = round(100.0 * len(outside) / len(nonbot), 1)
        row["top5"] = sorted(top5)
        row["one_off_count"] = len(one_offs)
        row["one_offs"] = one_offs[:10]
        print(f"  merged sampled: {len(merged)} (nonbot {len(nonbot)}) | outside top-5: {len(outside)} = {row['outside_pct']}% | one-off authors: {len(one_offs)}", flush=True)
        print(f"    top5: {row['top5']}", flush=True)
    else:
        row["outside_pct"] = None
        row["one_off_count"] = 0
        print("  no non-bot merged PRs in sample", flush=True)

    # ---- STEP 4: repo meta ----
    meta = gh_api(f"repos/{repo}")
    row["stars"] = meta.get("stargazers_count")
    row["pushed_at"] = meta.get("pushed_at")
    row["open_issues_count"] = meta.get("open_issues_count")
    print(f"  stars: {row['stars']} | pushed: {row['pushed_at']} | open issues: {row['open_issues_count']}", flush=True)
    return row


def main():
    rows = []
    for repo in REPOS:
        try:
            rows.append(screen(repo))
        except Exception as e:
            print(f"  !! ERROR on {repo}: {e}", flush=True)
            rows.append({"repo": repo, "error": str(e)})
    with open("/Users/cheonhyeonjun/open_contribute/screen_results.json", "w") as f:
        json.dump(rows, f, indent=2, default=str)
    print("\n\nDONE — results written to screen_results.json", flush=True)


if __name__ == "__main__":
    main()
