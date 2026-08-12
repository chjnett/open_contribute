---
name: rag-contribution
version: "1.0.0"
description: Guides a developer through contributing to a Retrieval‑Augmented Generation (RAG) open‑source project (e.g., LangChain, LlamaIndex). It evaluates candidate repos, narrows down a good‑first issue, and walks through a bug‑fix or documentation contribution.
---

# RAG Contribution

This skill follows the same four‑phase workflow as `first‑contribution` but adds RAG‑specific signals (model checkpoint size, test coverage for retrieval pipelines, etc.).

## Phase 1 – Understand
- Ask the user which programming language / framework they prefer (e.g., Python LangChain).
- Ask for experience level and any target repo they already have in mind.

## Phase 2 – Evaluate candidate RAG repos
- Pull GitHub metrics (stars, open issues, `good first issue` count, recent push).
- Additionally fetch:
  - Presence of a `docs/` folder.
  - Whether the repo runs CI for retrieval tests (`pytest` with `langchain` or `llama_index` in the workflow).
- Score using `references/rag-evaluation-criteria.md`.

## Phase 3 – Find a genuinely open issue
- Use the same issue‑triage checklist, but also verify that any referenced model files are not too large for a PR.

## Phase 4 – Guided contribution workflow
- Instruct the user to use `gh` (GitHub CLI) for an automated, token-free workflow.
- `gh auth status` to check login. If not logged in, `gh auth login --scopes workflow`. (If SSH fails later, use `gh config set git_protocol https`).
- `gh repo fork --clone` to instantly set up the repository locally.
- Set up a virtual environment, run the test suite, apply the bug fix, and run tests again.
- `gh pr create` to submit the PR directly from the terminal.

## References
- `references/rag-evaluation-criteria.md`
- `references/issue-triage-checklist.md`
- `references/message-templates.md`
