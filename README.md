<div align="center">
  <h1>first-contribution</h1>
  <p><strong>An Agent Skill that gets you from "I want to contribute to open source" to a submitted pull request — and refuses to send you at issues that are already dead.</strong></p>

  <p>
    <a href="https://github.com/chjnett/open_contribute/actions/workflows/ci.yml"><img src="https://github.com/chjnett/open_contribute/actions/workflows/ci.yml/badge.svg" alt="Build Status"></a>
    <a href="https://github.com/chjnett/open_contribute/releases/latest"><img src="https://img.shields.io/github/v/release/chjnett/open_contribute?style=flat-square&color=1a7f37" alt="Latest release"></a>
    <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License"></a>
    <img src="https://img.shields.io/badge/platform-Mac%20%7C%20Linux%20%7C%20Windows-lightgrey?style=flat-square" alt="Platform">
  </p>
</div>

---

[한국어](./README.ko.md) | English

## The problem

`good first issue` labels lie. On a popular repo the labelled issue you find is usually already claimed, already fixed by a different PR, or quietly resolved with nobody closing the ticket. You read the code, get invested, and then find a linked PR from six months ago.

That is the visible half. The invisible half is worse: a repo can look thriving — daily commits, hundreds of merges a quarter — while merging almost nothing from anyone outside its core team. Stars and activity don't tell you whether *your* PR will land.

<div align="center">
  <img src="./assets/merge_gate.png" alt="Share of merged PRs from outside each repo's top-5 authors, 15 repositories measured" width="820">
</div>

Same day, same method: `grafana/grafana` merges 70% of its PRs from outside its five most frequent authors. `chroma-core/chroma` merges 8% — and every one of the 17 PRs opened against its good-first-issues had failed to merge. Both look healthy from the outside.

Then there's the race. Anything recent, well-scoped and labelled tends to be claimed within hours.

<div align="center">
  <img src="./assets/triage_attrition.png" alt="Share of candidate issues that already had a linked PR" width="820">
</div>

This skill measures all of that before it recommends anything.

## What's in the box

| Skill | Responds in | Use for |
| :--- | :--- | :--- |
| `first-contribution` | English | Any open-source project |
| `first-contribution-ko` | Korean | Any open-source project |
| `rag-contribution` | English | RAG projects (LangChain, LlamaIndex) |

Each is a self-contained Agent Skill: a `SKILL.md` plus a `references/` folder loaded on demand.

## How it works

1. **Narrows down what you want** — domain, sub-area, stack, experience level, contribution type — before searching, so the recommendation rests on your preferences rather than a guess.
2. **Filters on availability first.** A repo with no currently-open, unassigned contribution issues can't produce a contribution today, and that check is one cheap API call. Only the survivors get the expensive evaluation.
3. **Runs the PR merge reality gate** — the share of open PRs sitting 90+ days, and the share of merges from outside the top-5 authors. You see the numbers and decide; the skill never silently drops a repo.
4. **Triages every candidate issue** against an 8-step checklist: internal-only notices, linked PRs, assignees, resolving comments, claim pile-up, age — and finally whether the defect *still exists in current code*, because a fix can land without anyone closing the issue.
5. **Drafts the outreach** — claim comments, community-channel messages, PR descriptions — in the project's own register.
6. **Walks the contribution** — `gh`-based fork and clone, scoped edits, the project's real test suite, a pre-PR quality checklist covering DCO, signatures and CLAs, then submission and follow-up etiquette.

## Prerequisites

The skill drives forking, cloning and PR creation through the **GitHub CLI (`gh`)**, so no manual personal access tokens.

- **Mac:** `brew install gh`
- **Windows:** `winget install --id GitHub.cli`
- **Linux:** `sudo apt install gh`

```bash
gh auth login --scopes workflow
```

> If you hit SSH host key errors later, run `gh config set git_protocol https`.

## Install

### Easiest — paste this prompt to your coding agent

Swap the folder name for whichever variant you want.

```text
Install the first-contribution agent skill for me, and nothing else.

1. Figure out my skills directory (Claude Code → ~/.claude/skills/,
   otherwise my tool's documented skills directory).
2. Clone https://github.com/chjnett/open_contribute into a temp folder.
3. Copy the first-contribution/ subfolder into <skills directory>/first-contribution/.
4. Confirm SKILL.md exists at the root of the copied folder.
5. Do not modify any other files, settings, or skills. Report the final
   install path and stop.
```

Restart your agent to pick up the skill.

### Claude Code — copy the folder yourself

```bash
git clone https://github.com/chjnett/open_contribute /tmp/open_contribute
cp -r /tmp/open_contribute/first-contribution ~/.claude/skills/first-contribution
```

### Claude.ai / Cowork — upload a packaged `.skill`

Download the variant you want from the [latest release](https://github.com/chjnett/open_contribute/releases/latest) and upload it under Settings → Skills. To build the files yourself from a clone:

```bash
bash scripts/package_skill.sh
```

## Use it

The skill triggers on intent — no commands:

> *"I want to start contributing to open source, help me find a good repo and issue"*

> *"Is this repo beginner-friendly? https://github.com/langchain-ai/langchain"*

> *"Find me a good-first-issue in a RAG/Python project."*

## Field notes

Every rule in the checklist was added after it cost a real run something. A few of the findings:

- **`chroma-core/chroma`** — 29k stars, pushed daily, 11 open `good first issue`s. Also 275 of 452 open PRs sitting 90+ days, 8% of merges from outside the top-5 authors, and 17 of 17 PRs against those labelled issues failed to merge. The gate exists because of this repo.
- **`deepset-ai/haystack`** — passes the gate comfortably, and its contribution labels are *empty*: 199 such issues total, zero open. An empty label on a healthy repo means "come back later," which is the opposite diagnosis from a rotten one.
- **`argoproj/argo-cd#29051`** — 8 days old, unassigned, zero linked PRs, `severity:critical`. It passed every social check and had already been fixed by `v3.3.14`. That is why the checklist now verifies the defect against current code.
- **`grafana/grafana#130567`** — found by this skill, root-caused to a namespace being used as an org ID, and submitted as [#130614](https://github.com/grafana/grafana/pull/130614). Its existing tests had asserted the buggy output, which is how the bug shipped.

## Reproducing the charts

Both images come only from measurements taken on 2026-08-12, with the method printed on each chart:

```bash
python3 scripts/generate_charts.py
```

## Troubleshooting

| Error / symptom | Fix |
| :--- | :--- |
| **"refusing to allow an OAuth App to create or update workflow... without workflow scope"** | Your `gh` token can't push to repos with GitHub Actions:<br>`gh auth refresh --scopes workflow` |
| **"The value of the GITHUB_TOKEN environment variable is being used for authentication."** | An old token is stuck in your environment:<br>`unset GITHUB_TOKEN` (Mac/Linux) or `Remove-Item Env:\GITHUB_TOKEN` (Windows) |
| **"Host key verification failed"** during clone | SSH keys aren't set up; switch `gh` to HTTPS:<br>`gh config set git_protocol https` |
| **"Commits must have verified signatures"** | The repo requires signed commits. `git commit -s` is DCO sign-off and does **not** satisfy this — you need a signing key, or commit via GraphQL `createCommitOnBranch`. |
| **CLA check stays pending** | Only you can sign a CLA. Follow the bot's link from the PR itself; if the page renders blank, a content blocker is usually eating the agreement text. |

## Contributing

Built and refined in public while being used for real contributions. If it recommends a stale issue, misjudges a repo, or misses a project convention, open an issue — that feedback is what the checklist is made of.

## License

[MIT](./LICENSE). Use it, fork it, build on it.
