# Pre-PR Quality Control Checklist (PR Acceptance Optimizer)

Before running `gh pr create`, the agent **must** enforce this checklist. A PR submitted by a first-time contributor that fails any of these checks is highly likely to be ignored, closed, or stalled. 

## 0. Issue Assignment Verification (CRITICAL)
- **Do NOT open a PR unless the user is officially assigned to the linked issue.**
- Many large repositories (like LangChain) have automated bots that will instantly close PRs from unassigned users.
- Verify assignment by running `gh issue view <issue_number>`. If the user is not in the "Assignees" list, **STOP**. Tell the user they must wait for a maintainer to assign them based on their claim comment.

## 1. Local CI / Tests Verification (Non-Negotiable)
- Check `CONTRIBUTING.md` for the exact local testing command (e.g., `make test`, `npm run test`, `pytest`, `cargo test`).
- **Run it locally** via `bash_tool` before suggesting a PR.
- If it's a bug fix, ensure the fix is covered by a test. (Did we write a test? Does it fail without the fix and pass with the fix?)

## 2. Linting and Formatting
- Many repos enforce formatting checks (e.g., `black`, `ruff`, `prettier`, `eslint`) in their CI pipelines.
- Find the formatting command in `CONTRIBUTING.md` or `package.json`/`Makefile` and run it (e.g., `make lint` or `npm run format`). 
- Do not submit code with trivial whitespace or stylistic errors.

## 3. Commit Message Style Matching
- Check the last 10 commits in the repository: `git log --oneline -n 10`.
- Does the repo use **Conventional Commits** (e.g., `feat:`, `fix:`, `docs:`)? 
- Does the repo require referencing the issue number in the commit title? (e.g., `Fix memory leak (#123)`)
- **Action:** Rewrite the user's commit message to perfectly match the existing repository's conventions.

## 4. DCO / Sign-off Requirement
- Does the repository require a Developer Certificate of Origin (DCO)? Check for a `DCO` file or mentions in `CONTRIBUTING.md`.
- **Safe Default:** Instruct the agent to always use `git commit -s -m "..."` to append the `Signed-off-by` line automatically. It rarely hurts, and saves PRs from failing DCO checks.

## 5. PR Template Adherence
- Check if `.github/PULL_REQUEST_TEMPLATE.md` (or similar templates in `.github/PULL_REQUEST_TEMPLATE/`) exists.
- If it exists, the `gh pr create --body "..."` command **must** strictly fill out this template. Do not invent a new structure.
- Ensure all checkboxes (`[ ]`) relevant to the PR are marked as `[x]`. 
- Include the exact phrase `Fixes #ISSUE_NUMBER` or `Closes #ISSUE_NUMBER` so GitHub auto-links the issue.
