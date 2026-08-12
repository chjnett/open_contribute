# Pre-PR Quality Control Checklist (PR Acceptance Optimizer)

Before running `gh pr create`, the agent **must** enforce this checklist. A PR submitted by a first-time contributor that fails any of these checks is highly likely to be ignored, closed, or stalled.

## 0. Issue Assignment Verification (CRITICAL)
- **Do NOT open a PR unless the user is officially assigned to the linked issue.**
- Many large repositories (like LangChain) have automated bots that will instantly close PRs from unassigned users.
- Verify assignment by running `gh issue view <issue_number>`. If the user is not in the "Assignees" list, **STOP**. Tell the user they must wait for a maintainer to assign them based on their claim comment.
- Not every project works this way — Grafana, for instance, accepts external PRs without assignment. Check the repo's actual convention rather than assuming either way, and tell the user which one applies.

## 1. Local CI / Tests Verification (Non-Negotiable)
- Check `CONTRIBUTING.md` for the exact local testing command (e.g., `make test`, `npm run test`, `pytest`, `cargo test`).
- **Run it locally** via `bash_tool` before suggesting a PR.
- If it's a bug fix, ensure the fix is covered by a test. (Did we write a test? Does it fail without the fix and pass with the fix?)

**When you genuinely cannot run them**, say so instead of implying you did. Very large repos have real setup costs — a Grafana `yarn install` needs several GB, which is not always available. Check `df -h` before starting rather than discovering it halfway through, and never fill the user's disk to satisfy a checklist item.

If you skip local tests, the PR description must say which files were not executed, why, and which specific parts the reviewer should scrutinise. Maintainers accept "I couldn't run the suite, here's what to check" far better than a silent gamble that CI catches it.

## 1b. Existing tests may encode the bug
A green test suite does not mean correct behaviour. When a bug shipped, ask why the tests allowed it — often they assert the broken output.

In `grafana/grafana#130567`, the short URL was built from the resource namespace instead of the org ID, and the tests locked that in:

```ts
metadata: { namespace: 'org-5' }
expect(result).toBe('...?orgId=org-5');   // the bug, as the expected value
```

Two consequences:

- **Update those assertions as part of the fix**, and say so in the PR — it explains how the bug escaped review.
- **Check what else calls the function you changed.** Two unrelated tests exercised the same code path through a different entry point and would have broken; they needed a default in the shared `beforeEach`. Grep for the function name across the test file before assuming your change is isolated.

## 2. Linting and Formatting
- Many repos enforce formatting checks (e.g., `black`, `ruff`, `prettier`, `eslint`) in their CI pipelines.
- Find the formatting command in `CONTRIBUTING.md` or `package.json`/`Makefile` and run it (e.g., `make lint` or `npm run format`).
- Do not submit code with trivial whitespace or stylistic errors.

## 3. Commit Message Style Matching
- Check the last 10 commits in the repository: `git log --oneline -n 10`, or `gh api "repos/{owner}/{repo}/pulls?state=closed&sort=updated&direction=desc" --jq '[.[]|select(.merged_at!=null)][].title'` when you have no clone.
- Does the repo use **Conventional Commits** (e.g., `feat:`, `fix:`, `docs:`), or an area prefix (`Alerting: Prevent race condition`)?
- Does the repo require referencing the issue number in the commit title? (e.g., `Fix memory leak (#123)`)
- **Action:** Rewrite the user's commit message to perfectly match the existing repository's conventions.

## 4. Sign-off, signatures, and CLAs are three different things
Confusing these wastes a round trip. Check which the repo requires — it may be more than one.

**DCO sign-off** — a `Signed-off-by:` trailer, added with `git commit -s`. Text only, no key involved. Safe default: always include it.

**Verified commit signatures** — a cryptographic GPG/SSH signature, shown as `Verified` on GitHub. A repo can enforce this with a branch rule, and an unsigned commit blocks the merge with "Commits must have verified signatures." `git commit -s` does **not** satisfy this. Check with:

```bash
gh api "repos/{owner}/{repo}/commits?sha={branch}" --jq '.[].commit.verification | "\(.verified) \(.reason)"'
```

If the user has no signing key configured, do not create one for them — say the repo requires signed commits and let them set it up, or use the API route in §4b, which GitHub signs for you.

**CLA** — a legal agreement, usually enforced by a bot such as cla-assistant. **Never sign or accept a CLA on the user's behalf.** Surface the link, say plainly that only they can sign it, and continue with everything else. Grafana's CLA blocks merge but nothing else, so the PR can be opened and reviewed while it is pending.

## 4b. Committing without a clone (and getting a verified commit)
For a small change in a very large repo, cloning may cost more disk and time than the change is worth. You can commit through the API instead — but the two API routes are not equivalent:

- **REST Contents API** (`PUT /repos/{owner}/{repo}/contents/{path}`) produces **unsigned** commits. On a repo that requires verified signatures, this silently sets up a blocked PR.
- **GraphQL `createCommitOnBranch`** produces commits **signed by GitHub**, which show as `Verified`. Prefer it whenever you commit via API.

```bash
gh api graphql --input payload.json   # {"query": "mutation($input: CreateCommitOnBranchInput!){...}", "variables": {...}}
```

The mutation takes `expectedHeadOid` and base64 file contents, and creates one commit with all the changes.

**Never reset a PR branch to its base as a separate step.** A PR whose branch has zero commits ahead of base is auto-closed by GitHub. Force-update the ref straight to the new commit, or create the new commit before moving the branch. If it does get closed, `gh pr reopen <n>` restores it once the branch has commits again.

## 5. PR Template Adherence
- Check if `.github/PULL_REQUEST_TEMPLATE.md` (or similar templates in `.github/PULL_REQUEST_TEMPLATE/`) exists.
- If it exists, the `gh pr create --body "..."` command **must** strictly fill out this template. Do not invent a new structure.
- Ensure all checkboxes (`[ ]`) relevant to the PR are marked as `[x]`.
- Include the exact phrase `Fixes #ISSUE_NUMBER` or `Closes #ISSUE_NUMBER` so GitHub auto-links the issue.
- Offer the reviewer an alternative where there is a real design choice. A line like "if you'd rather derive this from X than read it from Y, say so and I'll rework it" costs nothing and reads as collaborative rather than presumptuous.

## 6. After opening — read the checks before reporting success
- On external PRs, most CI is **held for maintainer approval** ("N workflows awaiting approval"). That is the normal flow, not a failure — say so rather than reporting it as a problem.
- Distinguish what the user must act on (an unsigned CLA) from what is simply waiting (reviewer assignment, `policy-bot 0/1 rules approved`).
- Re-read the actual check list with `gh pr checks <n>` before telling the user where things stand.
