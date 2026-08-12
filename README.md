<div align="center">
  <h1>First-Contribution AI Skill</h1>
  <p><strong>A fully automated Agent Skill that takes you from "I want to contribute" to a submitted Pull Request, instantly.</strong></p>

  <p>
    <a href="https://github.com/chjnett/open_contribute/actions"><img src="https://img.shields.io/badge/build-passing-brightgreen?style=flat-square" alt="Build Status"></a>
    <a href="https://github.com/chjnett/open_contribute/issues"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome"></a>
    <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License"></a>
    <img src="https://img.shields.io/badge/platform-Mac%20%7C%20Linux%20%7C%20Windows-lightgrey?style=flat-square" alt="Platform">
  </p>
</div>

---

[한국어](./README.ko.md) | English

## Overview

`good first issue` labels lie more often than you'd think. On popular repositories, an issue labeled as beginner-friendly is usually already claimed, fixed in a different PR, or quietly resolved. You find it, get excited, read the code, and then discover a linked PR sitting there from six months ago. 

This AI Skill was built because this exact scenario happens far too often. It acts as an autonomous guide within your AI coding editor (Claude Code, Cursor, Cowork) to intelligently filter out "dead" issues, handle all the Git/GitHub CLI overhead, and optimize your PR for immediate acceptance by maintainers.

## Key Features

- **Domain-Specific Targeting:** Specialized flows for standard open-source contributions (`first-contribution`) and AI/RAG specific projects (`rag-contribution`).
- **Pre-PR Quality Control:** Enforces a rigid `pr-acceptance-checklist.md` to ensure your code has tests, proper formatting, and DCO sign-offs (`git commit -s`) *before* opening a PR.
- **GitHub CLI Automation:** Zero manual tokens! Uses `gh` CLI to natively authenticate, fork, clone, and push without breaking a sweat.
- **Smart Issue Triage:** Automatically filters out "good first issues" that have hidden assignees or linked PRs.
- **Outreach Drafter:** Automatically drafts professional "claim comments" and community channel (Discord/Slack) outreach messages.

---

## Prerequisites

This skill fully automates the GitHub workflow (forking, cloning, and PR creation) without requiring you to manually generate Personal Access Tokens (PAT). To enable this, you must have the **GitHub CLI (`gh`)** installed and authenticated.

- **Mac:** `brew install gh`
- **Windows:** `winget install --id GitHub.cli`
- **Linux:** `sudo apt install gh`

After installing, run the following command to authenticate and ensure you have permissions to push workflow files:

```bash
gh auth login --scopes workflow
```

> **Note:** Follow the prompts to authenticate via your web browser. (If you get SSH host key errors later, try running `gh config set git_protocol https`).

---

## Quick Start / Installation

### Easiest — Paste this prompt to your coding agent

Copy the block below into Claude Code or any SKILL.md-aware agent. (Swap the folder name for `first-contribution-ko` if you want the Korean-responding version).

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

Restart your agent to pick up the newly installed skill.

---

## Usage

Once installed, just describe what you want in plain language — the skill triggers on intent, no commands needed:

> *"I want to start contributing to open source, help me find a good repo and issue"*

> *"Is this repo beginner-friendly? https://github.com/langchain-ai/langchain"*

> *"Find me a good-first-issue in a RAG/Python project."*

---

## Troubleshooting

If you encounter issues during the `gh` authentication or PR creation process, refer to the following common solutions:

| Error Message / Issue | Solution |
| :--- | :--- |
| **"refusing to allow an OAuth App to create or update workflow... without workflow scope"** | Your `gh` token lacks permission to push to repositories containing GitHub Actions. Fix it by running:<br>`gh auth refresh --scopes workflow` |
| **"The value of the GITHUB_TOKEN environment variable is being used for authentication."** | `gh` is refusing to refresh because an old manual token is stuck in your environment. Clear it first:<br>`unset GITHUB_TOKEN` (Mac/Linux) or `Remove-Item Env:\GITHUB_TOKEN` (Windows) |
| **"Host key verification failed" (during clone)** | Your system is trying to use SSH and failing because keys aren't set up. Tell `gh` to default to HTTPS instead:<br>`gh config set git_protocol https` |

---

## Contributing

We welcome contributions! 
Built and refined in public while used for real-world contributions. If it recommends a stale issue, misjudges a repo, or misses a project convention, open an issue — that's exactly the feedback that improves the checklist.

## License

This project is licensed under the [MIT License](./LICENSE). Feel free to use it, fork it, and build on it.
