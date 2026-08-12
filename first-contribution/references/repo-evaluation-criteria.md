# Repository Evaluation Criteria

Use these to score and compare candidate repos in Phase 2. None of these alone is disqualifying — weigh them together.

## 1. Issue volume
More open issues generally means more opportunity, but read the shape of the backlog, not just the count.
- A repo with 50-2000 open issues and a reasonable close rate is healthy.
- A repo with 10,000+ open issues and barely any recent closes is a graveyard — contributions may sit unreviewed for a long time.
- A repo with <10 open issues either has an extremely tight-knit maintainer team (hard to break into) or is quietly dying.

Check close rate roughly by comparing `open_issues_count` against how recently issues in the tracker are getting closed (spot check a few `state:closed` results sorted by `closed:desc`).

## 2. Recent commit/PR activity
`pushed_at` from the repo API tells you the last push. Also worth checking:
- Are PRs from external contributors (not just the core team) getting merged recently? Look at the last 10-20 merged PRs and their authors.
- A project that only merges its own employees' PRs is technically "active" but not actually welcoming outside contributors.

## 3. PR merge reality (run this before triaging issues)

Everything above can look healthy on a repo where outside PRs never actually land. A project can push daily, merge hundreds of PRs a quarter, and still merge almost nothing from anyone outside the core team. Activity and openness are different questions — measure the second one directly instead of inferring it from the first.

**Stale open-PR share** — how much of the open PR queue has been sitting for 90+ days:

```bash
curl -s "https://api.github.com/search/issues?q=repo:{owner}/{repo}+type:pr+state:open"
curl -s "https://api.github.com/search/issues?q=repo:{owner}/{repo}+type:pr+state:open+created:<YYYY-MM-DD"  # 90 days ago
```

**Outsider merge share** — of the PRs merged recently, how many came from someone other than the handful of people who merge constantly:

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=100" \
  | jq -r '[.[] | select(.merged_at != null) | .user.login
            | select(test("\\[bot\\]|(?i)bot$") | not)]
           | group_by(.) | map({u: .[0], n: length}) | sort_by(-.n)
           | {merged: (map(.n)|add), top5: (.[0:5]|map(.n)|add), oneoff: (map(select(.n==1))|length)}'
```

Report two numbers from this: the share of merged PRs **not** from the top-5 authors, and the count of authors with exactly one merged PR in the window. Both are assumption-free — you never have to decide who is an employee.

Do **not** try to classify core vs. external by name, and do not trust the `author_association` field. Both fail in opposite directions. On `deepset-ai/haystack`, `author_association` reported only 11 core authors because deepset staff keep org membership private — `sjrl`, `davidsbatista`, and `bogdankostic` all came back as `CONTRIBUTOR` despite obviously being maintainers. Guessing from names fails the other way as soon as a repo has regular outside contributors you don't recognize.

Use the `/pulls` REST endpoint rather than the search API for this. Search is where the strict secondary rate limit lives (see below), and `/pulls` gives you the same authorship data.

| | Healthy | Warning |
|---|---|---|
| Open PRs 90+ days old | under ~30% | over ~50% |
| Merged PRs outside the top-5 authors | 25%+ | under ~10% |
| One-off authors in the window | several | ~none |

Both columns landing in "warning" means a first contribution here is unlikely to merge regardless of which issue gets picked. **Show the user the actual numbers and let them decide whether to continue** — some people have a good reason to contribute to a specific project anyway (they use it at work, they want to learn that codebase, visibility). Don't silently drop the repo, and don't quietly proceed as though the numbers were fine.

**Rate limits.** The GitHub search API enforces a *secondary* rate limit that trips even when authenticated, after only a handful of rapid queries — it is separate from the 60/hour unauthenticated primary limit and from the 5000/hour authenticated one. Space search calls at least 5-8 seconds apart, and prefer plain REST endpoints (`/pulls`, `/issues`, `/issues/{n}/timeline`) wherever they can answer the same question, since they are far more forgiving. A 403 mentioning "secondary rate limit" needs a minute or two of backoff, not a retry.

Worked example — `chroma-core/chroma`, checked 2026-08. Every headline signal was good: 29k stars, pushed the previous day, 238 PRs merged in 90 days, 11 open `good first issue`s. The gate numbers were not: 275 of 452 open PRs (61%) were 90+ days old, external authors accounted for roughly 9% of merged PRs, and all 17 PRs opened against its good-first-issues had failed to merge — 11 still open after up to 8 months, 6 closed unmerged. One contributor's parting comment on issue #2054: "It is taking too long to get a PR merged so I am removing myself from the issue." The activity was real; it just wasn't reaching outsiders.

## 4. General-contributor friendliness
- `by-<org>` style labels (like Chroma's `by-chroma`) usually mean the maintainers curate a subset of issues specifically as approachable for outsiders — a good sign when combined with recent activity on those labels.
- Check the CONTRIBUTING.md for a `#contributing` Discord/Slack channel, a written style guide, or a "first-timers-only" style program — these all correlate with lower-friction onboarding.
- A single company owning 90%+ of commits (check via `git shortlog -sn` after cloning, or by eyeballing recent commit authors on GitHub) isn't automatically bad, but sets expectations: contributions may be steered heavily toward what that company's roadmap wants.

## 5. Feature-freeze status
Read the README and recent CHANGELOG/release notes for phrases like "maintenance mode," "feature freeze," "we are no longer accepting new features," or a v0->v1 sunset notice. A project that's only accepting bugfixes has a much smaller surface area for a first contribution — not necessarily bad, but the person should know going in.

## 6. Personal interest fit
The single highest-leverage factor and the easiest to get wrong by over-optimizing on the metrics above. A repo that scores worse on paper but that the person actually wants to use/understand will produce better contributions, because they'll actually read the code instead of pattern-matching a diff. Don't let a spreadsheet override genuine interest — surface it as one input to a decision the person makes, not a verdict.
