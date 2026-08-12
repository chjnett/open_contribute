---
name: first-contribution
description: Guides a developer through making their first (or next) open-source contribution end to end — picking a beginner-friendly repository, finding a genuinely open "good first issue" (filtering out ones that are secretly already claimed via linked PRs, assignees, or resolving comments), and walking through the actual fix using an AI coding editor. Use this skill whenever the user wants to start contributing to open source, asks for a "good first issue," wants to know if a GitHub repo is beginner-friendly, wants to build up their GitHub contribution history/portfolio, or asks which project to contribute to — even if they only mention a language, framework, or interest area (e.g. "I want to contribute to something Rust-related") rather than saying "open source" explicitly.
---

# First Contribution

Helps a developer go from "I want to contribute to open source" to an actual merged (or at least submitted) pull request. The skill has four phases. Move through them in order, but don't force phases the user has already completed — e.g. if they already named a repo, skip straight to Phase 2.

## Why this skill exists

Good-first-issue labels lie. Repos leave them on issues for months or years after someone already opened a PR, fixed it in a different commit, or the issue simply stopped being relevant. Recommending an issue without checking is the single most common failure mode here — it wastes the user's time and makes them look out of the loop when they show up to a dead issue. **Never recommend a specific issue without verifying it's actually open** (see Phase 3).

---

## Phase 1 — Understand what the person is looking for

Don't skip straight to searching repos on a vague request like "help me find an open source project to contribute to." Get specific first — a recommendation built on guessed preferences wastes the later phases' precision.

If the person hasn't already specified these in conversation, ask directly (use a structured multiple-choice tool like `ask_user_input_v0` if available — it's faster for the person than typing, and forces you to actually narrow down instead of asking one giant open-ended question):

1. **Domain/interest area** — what kind of project (e.g. web frameworks, CLI tools, ML/AI & RAG, infra/DevOps, games, mobile, data tools, "no preference"). This is the single highest-leverage question — people sustain contributions to things they'd use anyway.
2. **Language/stack preference** — a specific language, or "no preference."
3. **Experience level** — first-ever PR / done a few, want something a bit bigger / experienced, want a meaningful issue.
4. **Already have a repo in mind?** — if yes, skip straight to Phase 2 with that repo as (at least) one candidate; don't re-ask questions 1-3 for that repo, though they still help if you're also suggesting alternatives.

Keep it to 2-3 quick questions max, single-select where possible — this is a narrowing step, not an interview. If the person already answered some of this earlier in the conversation (e.g. they were just discussing a specific stack), don't re-ask; carry that forward and only ask what's still missing.

## Phase 2 — Evaluate candidate repositories

Use `bash_tool` with `curl` against the GitHub REST API (`api.github.com` is allowlisted) to pull real numbers instead of guessing. Also use `web_search` to find candidate repos in the relevant domain if the user hasn't named any.

For each candidate repo, pull:

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}"
# -> stargazers_count, open_issues_count, pushed_at (recency), archived (must be false)

curl -s "https://api.github.com/search/issues?q=repo:{owner}/{repo}+label:%22good+first+issue%22+state:open"
# -> total_count of currently-open good-first-issues
```

Note: unauthenticated GitHub API calls are rate-limited to 60/hour. Space out calls (`sleep 3-5` between requests) and batch repos rather than hammering the API. If you hit a rate limit, fall back to `web_search` / `web_fetch` for that repo and tell the user briefly why the numbers might be less precise.

Score candidates against the criteria in `references/repo-evaluation-criteria.md` (read it before scoring — don't wing this from memory). At a glance, the key signals are:

| Signal | Good sign | Warning sign |
|---|---|---|
| Open issue count | Dozens to low-thousands | Near zero (nothing to do) or tens of thousands (drowning) |
| `good first issue` count | 5+ currently open | 0, or all several years old |
| Last push | Days | Months+ |
| Contributor base | Many outside orgs/individuals in recent PR authors | Nearly all commits from one company's employees |
| Feature status | Actively adding features | README says "in maintenance mode" / "feature frozen" |

Present 3-6 candidates as a comparison (a table works well) and give a clear recommendation, not just a data dump — the person came here for a decision, not a spreadsheet.

## Phase 3 — Find a genuinely open issue (the part everyone gets wrong)

Once a repo is chosen:

1. Pull good-first-issue-labeled issues, **sorted newest first**, unassigned:
   ```
   https://github.com/{owner}/{repo}/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22+sort%3Acreated-desc+no%3Aassignee
   ```
   (fetch this with `web_fetch`, or hit the search API with `+no:assignee` appended to the query)

2. For every candidate before recommending it, follow the full checklist in `references/issue-triage-checklist.md`. In short: check the **Development** section for linked PRs, check **Assignees**, and read the last 2-3 comments for signs it's already resolved or being worked on. Do this via `web_fetch` on the actual issue URL — don't infer staleness just from the `updated_at` timestamp; a recent update is often the sign it just got closed out, not that it's fresh (this bit the user before — an issue's most recent comment said "this looks resolved, closing candidate PR incoming").

3. Only recommend issues that pass all three checks. If most of the label's contents turn out to be stale (this happens more often than not on popular repos), say so plainly and pivot to:
   - The repo's Discord/Slack `#contributing` channel if one is linked in the README — ask a maintainer directly for a currently-open recommendation
   - Recently-*opened* bug reports that look self-contained, even without the label

4. Rank the surviving candidates by scope (smallest/clearest first) and explain *why* each one is a reasonable starting point, not just what it is.

## Phase 3.5 — Community outreach & draft messages

Don't stop at just naming an issue — draft the actual outreach the user needs to send, so they can copy/send it instead of staring at a blank textbox.

**Locate community channels.** Check `README.md` and `CONTRIBUTING.md` (fetch them directly, e.g. `raw.githubusercontent.com/{owner}/{repo}/main/README.md`) for Discord/Slack invite links, mailing lists, or a "how to get help" section. Surface whatever you find — most active projects link one.

**Draft a claim comment for the chosen issue.** Once an issue has passed the Phase 3 triage, write 1-2 short comment variants the user can post directly on the issue to signal intent before starting work (e.g. "casual" vs. "a bit more detail on planned approach"). Keep these genuinely short — a paragraph max. A comment that's too long or oversells intent reads as inexperienced; maintainers just want to know the issue is claimed and roughly how.

**Draft a maintainer/Discord outreach message when needed.** This applies in two cases: (a) the good-first-issue label turned out to be entirely stale (Phase 3, step 6), or (b) the user wants a bigger/more specific issue than what's labeled. Draft a short, specific message for the `#contributing` channel or as an issue comment — specific enough to get a useful reply (mention relevant experience/stack, ask for a currently-open recommendation) but not a wall of text. Avoid generic "hi I want to contribute, what should I do?" phrasing — maintainers see a lot of that and it doesn't stand out or get prioritized.

**Draft the PR description** at submission time too (already covered in Phase 4, step 5) — same principle: match the project's tone, keep it scoped to what actually changed.

See `references/message-templates.md` for the tone/structure guidelines behind each of these.

## Phase 4 — Guided contribution workflow

Once the user has picked an issue, walk them through it using their AI coding editor (Claude Code, Cursor, etc. — if they're doing this inside claude.ai chat rather than an editor, use `bash_tool` to actually clone and explore the repo yourself):

1. Clone the repo; read `CONTRIBUTING.md` and `README.md` first — every project has slightly different conventions (branch naming, commit message format, required tests, DCO/CLA sign-off).
2. Locate the exact files relevant to the issue — don't try to explain the whole codebase, scope down to what's needed.
3. Draft the fix, then **explain the diff back to the user line by line** rather than letting them submit something neither of you fully understands — reviewers can tell, and it erodes trust for future contributions too.
4. Run the project's actual test suite locally (per CONTRIBUTING.md — pytest, jest, cargo test, etc. all differ) before suggesting a PR.
5. Draft the PR title/description matching the *project's* existing PR style (look at 2-3 recently merged PRs for tone/format), and have the user do a final read-through before submitting — they're the author of record, not the AI.
6. After a maintainer responds with review feedback, help iterate quickly, but keep the user in the loop on *why* changes are being made, not just applying suggestions blindly.

## A note on iterating this skill

This skill is meant to be used repeatedly and refined based on what actually happens in real attempts (stale issues that slipped through, repos that turned out to be worse fits than the numbers suggested, PR conventions that weren't documented anywhere). When something in a real contribution attempt doesn't match what this skill predicted, that's a signal the checklist or scoring criteria should be updated — flag it back for a revision rather than treating it as a one-off surprise.
