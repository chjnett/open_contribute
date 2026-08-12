[한국어](./README.ko.md) | English

# first-contribution

A [Claude Skill](https://www.anthropic.com/news/skills) that gets you from "I want to contribute to open source" to an actual submitted pull request — without wasting an afternoon on a `good first issue` that turned out to be dead three months ago.

`good first issue` labels lie more often than you'd think. On popular repos, a label opened in 2023 is usually already claimed, fixed in a different PR, or quietly resolved — the issue just never got closed. You find it, get excited, start reading the code, then discover a linked PR sitting there from six months ago. This skill exists because that happened, twice in a row, on the same repo, in one afternoon.

## What's inside

- **`first-contribution/`** — the skill, responds in English
- **`first-contribution-ko/`** — the same skill, responds in Korean ([한국어 안내](./README.ko.md))

Each contains:
- **`SKILL.md`** — the workflow: repo evaluation, issue triage, outreach drafting, guided contribution
- **`references/repo-evaluation-criteria.md`** — scoring criteria for "is this repo actually beginner-friendly"
- **`references/issue-triage-checklist.md`** — the 6-step check that filters out stale/claimed issues before they're ever recommended
- **`references/message-templates.md`** — tone/structure guides for issue-claim comments, `#contributing` channel outreach, and PR descriptions

## How it works

1. **Narrows down what you're looking for** — domain, stack, experience level — before searching, so the recommendation is built on your actual preferences instead of guesses.
2. **Evaluates candidate repos with real data** — pulls live numbers from the GitHub API (open issue count, `good first issue` count, last-push recency, external-contributor ratio) instead of vibes.
3. **Filters out dead issues before recommending them** — checks linked PRs, assignees, and actually reads the last few comments for "this looks resolved."
4. **Finds community channels and drafts outreach** — pulls the Discord/Slack link from the README, drafts a claim comment for the issue, and — if the labeled issues are all dead — drafts a specific ask for the `#contributing` channel instead of a generic "how do I contribute?"
5. **Walks you through the actual fix** — clones the repo, reads `CONTRIBUTING.md`, scopes to the relevant files, drafts the change, explains the diff, runs the real test suite, and drafts a PR description matching the project's existing style.

## How it's packaged

This repo *is* an [Agent Skill](https://www.anthropic.com/news/skills) — each variant folder has a `SKILL.md` at its root with the required `name`/`description` frontmatter, plus a `references/` folder of load-on-demand detail. Agent Skills is an open standard read natively by Claude Code, Claude.ai, Cowork, and (via the same folder format) most other SKILL.md-aware coding agents.

## Install

### Easiest — paste this prompt to your coding agent

Copy the block below into Claude Code or any SKILL.md-aware agent. Swap the folder name for `first-contribution-ko` if you want the Korean-responding version instead.

```
Install the first-contribution agent skill for me, and nothing else.

1. Figure out my skills directory (Claude Code → ~/.claude/skills/,
   otherwise my tool's documented skills directory).
2. Clone https://github.com/chjnett/open_contribute into a temp folder.
3. Copy the first-contribution/ subfolder (or first-contribution-ko/ for
   the Korean-responding version) into <skills directory>/first-contribution/.
4. Confirm SKILL.md exists at the root of the copied folder.
5. Do not modify any other files, settings, or skills. Report the final
   install path and stop.
```

Restart the agent (or start a new session) so it picks up the skill.

### Or install it yourself

**Claude Code** — `~/.claude/skills/` (global) or `.claude/skills/` (per-project)

```bash
git clone https://github.com/chjnett/open_contribute /tmp/open_contribute
cp -r /tmp/open_contribute/first-contribution ~/.claude/skills/first-contribution
# or, for the Korean version:
cp -r /tmp/open_contribute/first-contribution-ko ~/.claude/skills/first-contribution-ko
```

**Claude.ai / Cowork** — upload the packaged `.skill` file (`first-contribution.skill` or `first-contribution-ko.skill`) from a release, or upload the `SKILL.md` + `references/` folder directly in Settings → Skills.

## Use it

Once installed, just describe what you want in plain language — the skill triggers on intent, no command needed:

> "I want to start contributing to open source, help me find a good repo and issue"
> "is this repo beginner-friendly? [github link]"
> "find me a good-first-issue in a Rust project"

## Publishing your own copy

Keep the repo public with `SKILL.md` at the root of each skill folder and a clear `description` — that's the line every agent reads to decide when to fire the skill. To go further: open a PR to [anthropics/skills](https://github.com/anthropics/skills), list it on a skills directory, or bundle it into a Claude Code plugin marketplace.

## Status

Built and refined in public while I use it for my own contributions. If it recommends a stale issue, misjudges a repo, or misses a project convention, open an issue — that's exactly the feedback that improves the checklist.

## License

[MIT](./LICENSE). Use it, fork it, build on it.
