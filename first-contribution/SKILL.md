---
name: first-contribution
metadata:
  version: "1.4.0"
description: Guides a developer through making their first (or next) open-source contribution end to end — picking a beginner-friendly repository, finding a genuinely open "good first issue" (filtering out ones that are secretly already claimed via linked PRs, assignees, or resolving comments), and walking through the actual fix using an AI coding editor. Use this skill whenever the user wants to start contributing to open source, asks for a "good first issue," wants to know if a GitHub repo is beginner-friendly, wants to build up their GitHub contribution history/portfolio, or asks which project to contribute to — even if they only mention a language, framework, or interest area (e.g. "I want to contribute to something Rust-related") rather than saying "open source" explicitly.
---

# First Contribution

Helps a developer go from "I want to contribute to open source" to an actual merged (or at least submitted) pull request. The skill has four phases. Move through them in order, but don't force phases the user has already completed — e.g. if they already named a repo, skip straight to Phase 2.

## Why this skill exists

Good-first-issue labels lie. Repos leave them on issues for months or years after someone already opened a PR, fixed it in a different commit, or the issue simply stopped being relevant. Recommending an issue without checking is the single most common failure mode here — it wastes the user's time and makes them look out of the loop when they show up to a dead issue. **Never recommend a specific issue without verifying it's actually open** (see Phase 3).

---

## Phase 1 — Understand what the person is looking for

Don't skip straight to searching repos on a vague request like "help me find an open source project to contribute to." Get specific first — a recommendation built on guessed preferences wastes the later phases' precision.

If the person hasn't already specified these in conversation, use a structured multiple-choice tool (`ask_user_input_v0`) to narrow down their preferences interactively. Carry forward anything they've already answered instead of re-asking it.

1. **Domain** (single select) — options from `references/domain-categories.md`. This is the highest-leverage question; people sustain contributions to things they'd use anyway.
2. **Sub-area** (single select, dynamic) — load the matching list from `references/subcategory-map.md` based on the domain picked.
3. **Language / stack** (single or multi select) — present the common stacks for that sub-area, plus "no preference."
4. **Experience level** (single select) — first-ever PR / a few PRs, want something bigger / experienced, want a meaningful issue.
5. **Contribution type** (multi select) — docs & README, type hints & code cleanup, bug fix, small feature.

Don't run all five as a rigid interview. Skip any the person has already answered, and if they arrive with a repo already in mind, go straight to Phase 2 with that repo as a candidate.

**Most structured-question tools cap out at four options per question**, and `domain-categories.md` lists eight. Don't silently drop four domains to fit — group them into four coherent buckets for question 1 (e.g. "AI / RAG · vector DBs", "Backend · databases", "Infra / DevOps · security", "Frontend · mobile · games"), then let question 2 do the narrowing inside the bucket. Say that you're grouping, so the person knows the missing options weren't a judgment about them.

## Phase 2 — Evaluate candidate repositories

Use `bash_tool` with `curl` against the GitHub REST API (`api.github.com` is allowlisted) to pull real numbers instead of guessing. Also use `web_search` to find candidate repos in the relevant domain if the user hasn't named any.

For each candidate repo, pull:
```bash
# Validate repository identifier (owner/repo)
repo_regex='^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$'
if [[ ! "${owner}/${repo}" =~ $repo_regex ]]; then
  echo "Invalid repository identifier: ${owner}/${repo}"
  exit 1
fi
curl -s "https://api.github.com/repos/{owner}/{repo}"
# -> stargazers_count, open_issues_count, pushed_at (recency), archived (must be false)

curl -s "https://api.github.com/search/issues?q=repo:{owner}/{repo}+label:%22good+first+issue%22+state:open"
# -> total_count of currently-open good-first-issues
```

Note on rate limits: unauthenticated GitHub API calls are capped at 60/hour. Authenticating (via `gh`, which Prerequisites already requires) raises that to 5000/hour — but the **search API** additionally enforces a *secondary* limit that trips after only a handful of rapid queries no matter how you authenticate. Space search calls 5-8 seconds apart, and prefer plain REST endpoints (`/pulls`, `/issues`, `/issues/{n}/timeline`) whenever they answer the same question. A 403 mentioning "secondary rate limit" needs a minute or two of backoff, not an immediate retry. If you're still stuck, fall back to `web_search` / `web_fetch` and tell the user briefly why the numbers might be less precise.

Score candidates against the criteria in `references/repo-evaluation-criteria.md` (read it before scoring — don't wing this from memory). At a glance, the key signals are:

| Signal | Good sign | Warning sign |
|---|---|---|
| Open issue count | Dozens to low-thousands | Near zero (nothing to do) or tens of thousands (drowning) |
| `good first issue` count | 5+ currently open | 0, or all several years old |
| Last push | Days | Months+ |
| Contributor base | Many outside orgs/individuals in recent PR authors | Nearly all commits from one company's employees |
| Feature status | Actively adding features | README says "in maintenance mode" / "feature frozen" |

**Before moving on to Phase 3, run the PR merge reality check** (`references/repo-evaluation-criteria.md` §3): the share of open PRs sitting 90+ days, and the external share of recently merged PRs. Everything in the table above measures whether a project is *active*; these two measure whether an outsider's PR actually lands, which is a different question — and it's the one that decides whether Phase 3 is worth doing at all. A repo can push daily and merge hundreds of PRs a quarter while merging nearly nothing from outside the core team.

If both numbers land in the warning column, **show the user the actual figures and ask whether to continue with this repo or look at alternatives**. It's their call — don't auto-reject the repo, and don't proceed as if the numbers were fine. Skipping this check is how a repo passes Phase 2 on healthy-looking headline stats and only reveals itself after a full Phase 3 pass has already been spent on it.

Present 3-6 candidates as a comparison (a table works well) and give a clear recommendation, not just a data dump — the person came here for a decision, not a spreadsheet.

## Phase 3 — Find a genuinely open issue (the part everyone gets wrong)

Once a repo is chosen:

1. Pull good-first-issue-labeled issues, **sorted newest first**, unassigned:
   ```
   https://github.com/{owner}/{repo}/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22+sort%3Acreated-desc+no%3Aassignee
   ```
   (fetch this with `web_fetch`, or hit the search API with `+no:assignee` appended to the query)

2. For every candidate before recommending it, follow the full checklist in `references/issue-triage-checklist.md`. In short: read the **whole body** for an internal-only notice, check the **Development** section for linked PRs, check **Assignees**, and read the last 2-3 comments for signs it's already resolved or being worked on. Do this via `web_fetch` on the actual issue URL — don't infer staleness just from the `updated_at` timestamp; a recent update is often the sign it just got closed out, not that it's fresh (this bit the user before — an issue's most recent comment said "this looks resolved, closing candidate PR incoming").

   The body check is not optional. Some projects auto-append "this issue will be handled internally and isn't open for external contributions" to every non-curated issue, and it is invisible in search results — on `deepset-ai/haystack`, three issues passed every other check and all three carried that footer.

   Then, on whatever survives, **verify the defect still exists in current code** (checklist Step 7). Every other check is a social signal and none of them prove the bug is still there — `argoproj/argo-cd#29051` was 8 days old, unassigned, zero linked PRs and labelled `severity:critical`, and had already been fixed by a release nobody closed the issue for. Read the file at the current default branch, and use a real parser rather than grep when the artifact is structured.

3. Only recommend issues that pass every check. When nothing survives, **diagnose why before pivoting** — count the contribution label in both `state=open` and `state=all`:
   - **Rotten label** (many open, all old, nothing closing) plus a failing merge gate → say so plainly and recommend a different repo. Choosing more carefully inside a backlog that never merges is wasted effort.
   - **Empty label** (few or zero open, many closed) → the repo is healthy and issues get finished fast; nothing is free *right now*. Say the wait is worth it and offer to watch the label.
   - Either way, the README's Discord/Slack `#contributing` channel is worth asking in, and recently-opened self-contained bug reports are worth checking — but re-run the internal-only check on those, since unlabeled issues are exactly where those notices live.

4. Rank the surviving candidates by scope (smallest/clearest first) and explain *why* each one is a reasonable starting point, not just what it is.

## Phase 3.5 — Community outreach & draft messages

Don't stop at just naming an issue — draft the actual outreach the user needs to send, so they can copy/send it instead of staring at a blank textbox.

**Locate community channels.** Check `README.md` and `CONTRIBUTING.md` (fetch them directly, e.g. `raw.githubusercontent.com/{owner}/{repo}/main/README.md`) for Discord/Slack invite links, mailing lists, or a "how to get help" section. Surface whatever you find — most active projects link one.

**Draft a claim comment for the chosen issue.** Once an issue has passed the Phase 3 triage, write 1-2 short comment variants the user can post directly on the issue to signal intent before starting work (e.g. "casual" vs. "a bit more detail on planned approach"). Keep these genuinely short — a paragraph max. A comment that's too long or oversells intent reads as inexperienced; maintainers just want to know the issue is claimed and roughly how.

**Draft a maintainer/Discord outreach message when needed.** This applies in two cases: (a) nothing survived triage (Phase 3, step 3) — whether the label was rotten or simply empty, or (b) the user wants a bigger/more specific issue than what's labeled. Draft a short, specific message for the `#contributing` channel or as an issue comment — specific enough to get a useful reply (mention relevant experience/stack, ask for a currently-open recommendation) but not a wall of text. Avoid generic "hi I want to contribute, what should I do?" phrasing — maintainers see a lot of that and it doesn't stand out or get prioritized.

**Draft the PR description** at submission time too (already covered in Phase 4, step 5) — same principle: match the project's tone, keep it scoped to what actually changed.

See `references/message-templates.md` for the tone/structure guidelines behind each of these.

## Phase 4 — Guided contribution workflow

Once the user has picked an issue, guide them through the GitHub CLI (`gh`) automated workflow. Using `gh` removes the need for manual Personal Access Tokens and cumbersome `git remote` setups.

1. **Authentication Check:** Ask the user to run `gh auth status`. If not logged in or missing scopes, instruct them to run `gh auth login --scopes workflow` and follow the interactive prompts (use the web browser option for easiest setup). If they encounter SSH host key errors during cloning, tell them to run `gh config set git_protocol https`.
2. **Automated Fork & Clone:** Instead of manual cloning, instruct the user to run `gh repo fork {owner}/{repo} --clone`. This single command creates the fork on their account, clones it locally, and sets up `origin` and `upstream` remotes perfectly.
3. Locate the exact files relevant to the issue — don't try to explain the whole codebase, scope down to what's needed.
4. Draft the fix, then **explain the diff back to the user line by line** rather than letting them submit something neither of you fully understands.
5. Run the project's actual test suite locally (per `CONTRIBUTING.md` — pytest, jest, cargo test, etc.) before suggesting a PR.
6. Commit the changes and push to the fork's branch.

## Phase 4.5 — Pre-PR Quality Control
Before running `gh pr create`, you **MUST** read and enforce `references/pr-acceptance-checklist.md`.
1. **Assignment Check (CRITICAL):** Run `gh issue view <issue>` to verify the user is officially assigned. Do NOT create a PR if they are not assigned. Bots will auto-close it.
2. **Tests & Linting:** Ensure all local tests and linters (`CONTRIBUTING.md`) have been run and pass.
3. **Commit Conventions:** Rewrite the commit message if it doesn't match the repo's history (e.g., Conventional Commits) and ensure it's signed (`git commit -s`) if a DCO is required.
4. **PR Template:** If `.github/PULL_REQUEST_TEMPLATE.md` exists, strictly use it for the PR body.

## Phase 5 — PR Submission and Iteration
1. **Automated PR Creation:** Instruct the user to run `gh pr create --title "..." --body "..."` using the drafted title and description matching the project's style.
2. After a maintainer responds with review feedback, help iterate quickly, but keep the user in the loop on *why* changes are being made, not just applying suggestions blindly.

## A note on iterating this skill

This skill is meant to be used repeatedly and refined based on what actually happens in real attempts (stale issues that slipped through, repos that turned out to be worse fits than the numbers suggested, PR conventions that weren't documented anywhere). When something in a real contribution attempt doesn't match what this skill predicted, that's a signal the checklist or scoring criteria should be updated — flag it back for a revision rather than treating it as a one-off surprise.
