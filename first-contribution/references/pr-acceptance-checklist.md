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

## 1c. Let the existing fixtures decide how you write the fix
When a bug has several correct-looking fixes, the test fixtures often rule most of them out. Read them before you pick.

Fixing a Directus M2A bug, the obvious guard was "is this type condition a real collection?", i.e. `typeCondition in schema.collections`. The mock schemas in `parse-query.test.ts` are `{ relations: [...] }` and define no `collections` key at all — so that guard would have thrown on `undefined`, and defending it with `?? {}` would have made every existing M2A test take the wrong branch.

The same relation object already carried `meta.one_allowed_collections`, which the fixtures *do* populate (`['child']`, `['ComponentText']`). Keying off that fixed the bug and left every existing case passing.

So: before committing to an approach, trace it through each existing test case by hand and confirm the data it depends on is actually present in the fixtures. This costs a few minutes and is the difference between a green CI run and a reviewer watching your PR fail.

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

**CLA** — a legal agreement. **Never sign or accept a CLA on the user's behalf**, and treat a bare "yes" or "go ahead" as agreement to the *task*, not informed consent to a legal document. Point at the agreement text, say plainly that only they can accept it, and carry on with everything else — a pending CLA usually blocks merge and nothing else, so the PR can still be opened and reviewed.

CLAs come in at least two shapes, and the second one is easy to walk into:

- **External signing service** (cla-assistant and friends). Grafana uses this: a bot comments with a link, the user authorises an app and signs there. Obviously not something you can do for them.
- **A file edit inside the PR.** Directus asks contributors to add their GitHub username to `contributors.yml` in the pull request itself. Mechanically that is a one-line diff you are perfectly capable of making — and making it *is* the act of signing. Recognise it for what it is and hand it back to the user.

Read the CLA workflow rather than guessing which shape applies:

```bash
gh api "repos/{owner}/{repo}/contents/.github/workflows" --jq '.[].name' | grep -i cla
```

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

## 5b. Release tooling a PR of this type must carry
A correct code change can still fail CI for a missing sidecar file. Check for release tooling before you commit:

```bash
gh api "repos/{owner}/{repo}/contents/.changeset" --jq 'length'   # changesets in use?
```

If the repo uses [changesets](https://github.com/changesets/changesets), a bug fix needs a `.changeset/<name>.md` naming the affected package and describing the fix in the past tense:

```markdown
---
'@directus/api': patch
---

Fixed GraphQL fragments declared on an M2A union type resolving their fields as null
```

The reliable way to learn every convention at once is to read the **file list of a recently merged PR of the same kind** — it shows the changeset, the test placement, and any docs or spec updates that ship alongside:

```bash
gh api "repos/{owner}/{repo}/pulls/{n}/files" --jq '.[].filename'
```

## 6. After opening — read the checks before reporting success
- On external PRs, most CI is **held for maintainer approval** ("N workflows awaiting approval"). That is the normal flow, not a failure — say so rather than reporting it as a problem.
- Distinguish what the user must act on (an unsigned CLA) from what is simply waiting (reviewer assignment, `policy-bot 0/1 rules approved`).
- Re-read the actual check list with `gh pr checks <n>` before telling the user where things stand.
- **A bot workflow that "succeeded" may have done nothing.** Directus's `cla-comment.yml` finished green and posted no comment, because its artifact-download step is `continue-on-error` and silently no-opped. Telling the user "wait for the bot" would have left them waiting forever. When an expected comment doesn't appear, read the workflow file and find out what it actually requires — don't infer from the check's colour.
- A failing check is worth reading down to the step name. `Check / fail` on Directus meant one step called `Preserve CLA result` running `exit 1` — nothing to do with the code.
