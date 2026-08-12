[한국어](./README.ko.md) | English

# first-contribution

A [Claude Skill](https://www.anthropic.com/news/skills) that helps you actually land your first (or next) open-source pull request — instead of spending an afternoon chasing a `good first issue` that turned out to be dead three months ago.

## The problem

`good first issue` labels lie more often than you'd think. On popular repos, a label opened in 2023 has usually already been claimed, fixed in a different PR, or quietly resolved — and the issue just never got closed. You find it, get excited, start reading the code, and then discover a linked PR sitting there from six months ago.

This skill exists because that happened to me, twice, in a row, on the same repo, in one afternoon.

## What it does

1. **Evaluates repos, not just vibes** — pulls real numbers from the GitHub API (open issue count, `good first issue` count, last-push recency, external-contributor ratio) so "is this repo good for beginners" is a comparison, not a guess.
2. **Filters out dead issues before recommending them** — checks the Development section for linked PRs, checks assignees, and actually reads the last few comments for "this looks resolved" before an issue makes it onto your shortlist.
3. **Finds community channels and drafts the outreach for you** — pulls the Discord/Slack link out of the README, drafts a short comment to claim the issue, and (if the labeled issues turn out to be dead) drafts a specific ask for the `#contributing` channel instead of a generic "how do I contribute?"
4. **Walks you through the actual contribution** — clones the repo, reads `CONTRIBUTING.md`, scopes down to the relevant files, drafts the fix, explains the diff, runs the real test suite, and drafts a PR description matching the project's existing style.

## Install

Two versions are included in this repo:

- **`first-contribution/`** — English, responds in English
- **`first-contribution-ko/`** — Korean, responds in Korean ([한국어 안내](./README.ko.md))

Drop the folder for your preferred language into your Claude Skills folder, or load the corresponding `.skill` file directly in Claude.ai / Claude Code / Cowork. They're independent skills — install one or both.

```
your-skills-dir/
└── first-contribution/          (or first-contribution-ko/)
    ├── SKILL.md
    └── references/
        ├── repo-evaluation-criteria.md
        ├── issue-triage-checklist.md
        └── message-templates.md
```

## Example

> "I want to contribute to a RAG or LLM-related open source project, help me find a good repo and issue"

Claude will pull live stats on candidate repos, recommend one with reasoning, then triage its `good first issue` list — surfacing only issues that are actually still open — before walking you through the fix.

## Status

This skill is being built and refined in public while I use it for my own contributions. If you hit a case where it recommends a stale issue, misjudges a repo, or misses a project convention, please open an issue — that's exactly the kind of feedback that improves the checklist.

## License

MIT
