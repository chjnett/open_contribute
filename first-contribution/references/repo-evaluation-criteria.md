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

## 3. General-contributor friendliness
- `by-<org>` style labels (like Chroma's `by-chroma`) usually mean the maintainers curate a subset of issues specifically as approachable for outsiders — a good sign when combined with recent activity on those labels.
- Check the CONTRIBUTING.md for a `#contributing` Discord/Slack channel, a written style guide, or a "first-timers-only" style program — these all correlate with lower-friction onboarding.
- A single company owning 90%+ of commits (check via `git shortlog -sn` after cloning, or by eyeballing recent commit authors on GitHub) isn't automatically bad, but sets expectations: contributions may be steered heavily toward what that company's roadmap wants.

## 4. Feature-freeze status
Read the README and recent CHANGELOG/release notes for phrases like "maintenance mode," "feature freeze," "we are no longer accepting new features," or a v0->v1 sunset notice. A project that's only accepting bugfixes has a much smaller surface area for a first contribution — not necessarily bad, but the person should know going in.

## 5. Personal interest fit
The single highest-leverage factor and the easiest to get wrong by over-optimizing on the metrics above. A repo that scores worse on paper but that the person actually wants to use/understand will produce better contributions, because they'll actually read the code instead of pattern-matching a diff. Don't let a spreadsheet override genuine interest — surface it as one input to a decision the person makes, not a verdict.
