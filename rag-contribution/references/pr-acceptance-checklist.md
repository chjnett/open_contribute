# Pre-PR Quality Control Checklist (PR Acceptance Optimizer)

Before running `gh pr create`, the agent **must** enforce this checklist. A PR submitted by a first-time contributor that fails any of these checks is highly likely to be ignored, closed, or stalled.

## 0. Issue Assignment Verification (CRITICAL)
- **Do NOT open a PR unless the user is officially assigned to the linked issue.**
- Many large repositories (like LangChain) have automated bots that will instantly close PRs from unassigned users.
- Verify assignment by running `gh issue view <issue_number>`. If the user is not in the "Assignees" list, **STOP**. Tell the user they must wait for a maintainer to assign them based on their claim comment.
- Not every project works this way — Grafana, for instance, accepts external PRs without assignment. Check the repo's actual convention rather than assuming either way, and tell the user which one applies.

**Assignment is not the only pre-PR gate — some repos require the issue itself to be pre-approved.** mem0's PR Gate bot closes any PR whose linked issue lacks the `accepted` label ("We only review pull requests that fix an issue we have already agreed to take on"), automatically, on open. The fix landed correctly (Valkey `SCAN`+`DEL` replacing the unsupported `DD` flag) but the PR was closed twice — #7013 then #7023 — because the issue was never labelled. The label is a maintainer decision; the contributor can ask for it on the issue but cannot apply it, so the PR stays closed until then.

**Before opening a PR, check whether the repo gates on an issue label, not just assignment.** Read the PR-closing bot's workflow (e.g. `.github/workflows/pr-gate.yml`) or CONTRIBUTING.md for phrases like "accepted", "approved", "triaged", "prioritized" as a precondition. If a gate exists, confirm the issue carries the label *before* investing in the PR — opening early just gets it auto-closed. Also note the exact reopen procedure the bot prints: it usually only needs the label applied, then a reopen.

## 1. Local CI / Tests Verification (Non-Negotiable)
- Check `CONTRIBUTING.md` for the exact local testing command (e.g., `make test`, `npm run test`, `pytest`, `cargo test`).
- **Run it locally** via `bash_tool` before suggesting a PR.
- If it's a bug fix, ensure the fix is covered by a test. (Did we write a test? Does it fail without the fix and pass with the fix?)

**When you genuinely cannot run them**, say so instead of implying you did. Very large repos have real setup costs — a Grafana `yarn install` needs several GB, which is not always available. Check `df -h` before starting rather than discovering it halfway through, and never fill the user's disk to satisfy a checklist item.

**"Just run the one test file" is not a way around the install.** `yarn test path/to/one.test.ts` still needs `node_modules`, and a yarn/pnpm workspace has no partial install that covers a single file. It sounds like a lightweight escape hatch and isn't one — if the install won't fit, neither will the single test.

If you skip local tests, the PR description must say which files were not executed, why, and which specific parts the reviewer should scrutinise. Maintainers accept "I couldn't run the suite, here's what to check" far better than a silent gamble that CI catches it.

When adding a test to a multiprocessing/pool-based library (billiard, celery,
multiprocessing-based tools), pass *module-level* functions to the pool, not closures
defined inside the test. With the default start method (spawn on macOS/Windows), a local
function can't be pickled, so the worker never starts and the test *hangs* instead of
failing cleanly — it looks like your change broke the pool when it's just a test-harness
gotcha (this bit a real run on billiard #427).

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

## 1d. When a bug is reported against one implementation, check its sibling

Some projects ship two implementations of the same code path — a C extension plus a
pure-Python fallback, sync and async copies, or several dialects. A "bug" reported
against one is often really a *divergence*: the sibling already handles the case
correctly. psycopg's pure-Python `_parse_row_binary` silently truncated a field whose
declared length exceeded the buffer, while its C `parse_row_binary` already raised
`DataError("bad copy data: length exceeding data")` for the same input. That turns a
"is this even a bug?" debate into an unambiguous consistency fix — and the sibling's
behaviour and error message are your spec. Grep the sibling path and match it rather
than inventing a new policy.

## 1e. The issue's suggested fix is a hint, not a spec — verify it against the real API

A well-written bug report often includes a suggested fix. It is the reporter's best
guess, not the implementation contract. On mem0, issue #6995 suggested adding the `DD`
flag to `FT.DROPINDEX`; the maintainer's reviewer pointed out Valkey's
`FT.DROPINDEX` does not support `DD` at all (its signature is
`FT.DROPINDEX <index-name>` only), so the first PR was closed and the approach had to
be reworked to `SCAN` + `DEL`. The issue's own comment had suggested the correct
approach; the prose in the body pointed the wrong way.

Before committing to a fix that comes from an issue body, check the underlying API's
official documentation (the command reference, the SDK docs, the wire format) that the
suggested operation actually exists — and note that *two sources inside the same issue
can disagree*. When they do, the implementation should follow the API, and the PR
description should say why it diverged from the issue's suggestion.

## 1f. Verify your diff against the current source before submitting — not just run tests

A green suite doesn't prove the change is correct against the code that's actually on
`main`. Before pushing, grep the current default branch and confirm three things:

- every identifier you used really exists there (don't *assume* "config was already
  imported" — check it, since that's exactly the claim that's easy to get wrong);
- the field/type path you read is real and correctly typed (grafana's
  `config.bootData.user.orgId` is a `number`, so `${orgId}` yields a bare id);
- every *caller* of the function you changed still behaves correctly (grafana's
  `createShortLink` calls `buildShortUrl` internally, which is why the shared
  `beforeEach` default kept the existing k8s-path tests green).

If you can't run the suite, this static pass lets you say "I couldn't run it, but I
verified X, Y, Z" instead of a bare "couldn't run". A diff the author has already
checked against `main` is what turns a maintainer's first review into an approve — the
most common way a small PR dies is a first-review "did you check X?" or a CI failure a
grep would have caught.

## 1g. When making several PRs from one clone, verify each branch's diff is clean before pushing

A single clone used for multiple PRs will happily ship a branch that carries a
previous PR's commit. On vLLM, `fix/anthropic-tool-reference-conversion` was branched
off `fix/precompiled-wheel-variant-fallback`, so the second PR's diff included
`setup.py` from the first until the rebase `git rebase --onto origin/main <first-commit> <branch>`
dropped it. The DCO bot catches missing sign-offs; nothing catches a wrong base —
the PR just grows a file it shouldn't have, and the first review points it out.

Before pushing any branch, diff it against the *upstream* default branch, not your
fork's copy (they can drift), and confirm the file list is exactly what this PR
intends:

```bash
git diff --stat origin/{default_branch}...{branch}   # upstream, not your fork
```

Also re-check it *after* a force-push rebase — the rebase shown above silently
re-applies only the target commit, which is what you want, but only when the `--onto`
base is the upstream tip.

## 1h. Cut the diff to the smallest change that fixes the issue

A reviewer has to verify every line they didn't write, so merge probability tracks the
diff size, not the effort that went into it: `size/small` PRs get reviewed in minutes,
`size/large` ones sit for weeks. Before submitting, re-read the diff and delete anything
not strictly required by the fix — unrelated refactors, drive-by formatting, "while I'm
here" improvements. Move genuinely separate changes into their own PR. Every line you
can cut is a line the reviewer doesn't have to verify.

## 2. Linting and Formatting
- Many repos enforce formatting checks (e.g., `black`, `ruff`, `prettier`, `eslint`) in their CI pipelines.
- Find the formatting command in `CONTRIBUTING.md` or `package.json`/`Makefile` and run it (e.g., `make lint` or `npm run format`).
- Do not submit code with trivial whitespace or stylistic errors.
- Run the repo's *actual* lint config rather than guessing: `pre-commit run` if it
  exists, or the exact linter commands from its config. A custom isort profile can
  reorder even two function-local imports — psycopg uses `length_sort`, so
  `from psycopg.adapt import X` sorts before `from psycopg._copy_base import Y`. Run it
  locally before pushing instead of discovering it in CI.
- In repos whose type checker also checks `tests/` (psycopg's mypy config does), your
  *added tests* must satisfy it too — CI will catch a wrong argument type even when the
  test passes at runtime (psycopg's `set_loader_types([25], 0)` ran fine, but mypy
  rejected the bare int for a `pq.Format` parameter). Run the type checker on your new
  files locally before pushing, and use the named enum rather than the raw value.

## 2b. Check for auto-generated files before editing

Some repos keep a generated file next to a hand-written source — e.g. psycopg
generates `tests/test_copy.py` from `tests/test_copy_async.py` via
`tools/async_to_sync.py`, with a "DO NOT CHANGE — change the original instead"
header. Hand-editing the generated file gets silently overwritten or fails a
sync-check in CI. Read the file header and look for the generator script; edit the
source and regenerate. Keep the generated output byte-identical to what the repo's
generator version produces — a newer or older generator can reformat the whole file,
and committing that churn is a separate nuisance to avoid.

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

**A green `signed-commits` CI check does NOT mean the repo doesn't enforce signatures — the enforcement often lives in a separate branch *ruleset*, not the CI.** On grafana, the `signed-commits` workflow passed for an unsigned commit and the branch's classic protection had no `required_signatures` entry, but an active **ruleset** named `Signed Commits` (rule `required_signatures`, target `~ALL`) still blocks the merge. To find the real gate, query the rulesets, not just the status checks:

```bash
gh api "repos/{owner}/{repo}/rulesets?target=branch" --jq '.[] | select(.enforcement=="active") | {name, enforcement, rules: [.rules[]?.type]}'
```

**If the user already has an SSH key on GitHub, signing is a two-line local setup — no GPG needed.** SSH signature format is built into git:

```bash
git config gpg.format ssh
git config user.signingkey "$HOME/.ssh/id_ed25519.pub"   # the key registered on GitHub
git commit --amend -S -s --no-edit
git push --force fork {branch}
```

`~/.gitconfig` may be read-only in a sandbox, so scope both `git config` calls to the local repo (no `--global`). After the push, GitHub verifies the SSH signature against the key on the account:

```bash
gh api "repos/{owner}/{repo}/commits/{sha}" --jq '.commit.verification | "\(.verified) \(.reason)"'   # verified / valid
```

This satisfies an active `required_signatures` ruleset the same way a GPG-signed commit does.

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
- Some repos gate CI on a **label or a merge-count** for first-time contributors, not just approval. vLLM's `pre-run-check` fails with `PR must have the 'verified', 'ready', or 'ready-run-all-tests' label ... or the author must have at least 4 merged PRs (found 0)` — a first-PR author hits this every time, the maintainer has to add the label, and there is nothing for the contributor to fix. A red `pre-run-check` here is onboarding friction, not a defect: read the failure text before treating it as a problem.
- **DCO is checked by a separate bot and can fail independently of everything else.** vLLM's `DCO` check turns red when the commit lacks a `Signed-off-by:` trailer, even though the code is fine. Fix it with `git commit --amend -s` and a force-push; the check re-runs on the new commit. A `Signed-off-by` trailer is free and harmless on repos that don't require it, so defaulting every commit to `-s` (or amending it in) removes an entire failure class on the first push.
- Distinguish what the user must act on (an unsigned CLA) from what is simply waiting (reviewer assignment, `policy-bot 0/1 rules approved`).
- Re-read the actual check list with `gh pr checks <n>` before telling the user where things stand.
- **A bot workflow that "succeeded" may have done nothing.** Directus's `cla-comment.yml` finished green and posted no comment, because its artifact-download step is `continue-on-error` and silently no-opped. Telling the user "wait for the bot" would have left them waiting forever. When an expected comment doesn't appear, read the workflow file and find out what it actually requires — don't infer from the check's colour.
- A failing check is worth reading down to the step name. `Check / fail` on Directus meant one step called `Preserve CLA result` running `exit 1` — nothing to do with the code.
- And down to the *file* it names. A linter failure (isort, mypy, ruff, …) on a file
  you didn't touch is usually pre-existing — a dependency going stricter than the repo's
  floor pin (psycopg's `mypy>=2.1.0` started failing `psycopg_build_ext.py` when mypy
  2.3.1 shipped). Confirm it fails on the repo's own `master` runs too, then report it as
  pre-existing instead of "fixing" it in your PR.

**Verify any second-hand account of your PR before acting on it.** A confident summary — from the user, a teammate, or another tool — is a claim about state, not the state. Check it against the timeline and the check list yourself, especially when the suggested action is a nudge, because a nudge spent on a wrong diagnosis is the one nudge you had.

A worked example on `grafana/grafana#130614`. The account said a maintainer had moved the PR onto a squad board, that 28 workflows were awaiting approval, and that the right move was to comment asking maintainers to approve them. All three were wrong:

| Claim | What the API said |
| --- | --- |
| A maintainer moved it to a board | Every timeline actor was the author or `github-actions[bot]` |
| 28 workflows awaiting approval | Zero runs in `action_required`; all reported checks passing |
| Ask maintainers to approve the workflows | Nothing was awaiting approval to ask about |

```bash
gh api "repos/{owner}/{repo}/issues/{n}/timeline?per_page=100" \
  --jq '.[]|select(.event|test("added_to_project|moved_columns_in_project|review_requested"))|"\(.event) by \(.actor.login)"'
gh api "repos/{owner}/{repo}/actions/runs?event=pull_request" --jq '[.workflow_runs[]|select(.status=="action_required")]|length'
```

Had it been acted on, it would have `@`-mentioned two maintainers within a day of opening, to ask for something that wasn't blocked — three anti-patterns from §6 of the message templates at once.

Had it been acted on, it would have `@`-mentioned two maintainers within a day of opening, to ask for something that wasn't blocked — three anti-patterns from §6 of the message templates at once.

**A PR's head reference can desync from its branch when the branch is force-pushed externally, and it reads oddly — verify the *actual* refs before assuming the PR is wrong.** On grafana #130614, the `fix/shorturl-org-id` fork branch was force-pushed (by our own token) back to a huge one-commit state that added ~4.9M lines, and the PR went closed with a stale head SHA. The recovery — recreate the correct two-file commit from the intended diff, force-push the fork branch, confirm with `git ls-remote` that the branch really points at the good SHA — left the branch correct while `gh pr view` still reported the old head and CLOSED. Two API reads disagreed: `git ls-remote` said the branch was the good commit, while the PR's `head.sha` still named the broken one.

So when a PR's stated head/files look wrong:
- cross-check the *fork branch's* actual tip with `git ls-remote <fork-url> <branch>` or the commits endpoint — the PR's cached `head_sha` and a closed/reopened state can be stale;
- recover the branch first (recreate the intended commit from the reviewed diff, `git push --force`), *then* sort out the PR state;
- if the PR refuses to reopen or won't adopt the new head, tell the maintainer plainly on the PR — "the branch now points at <sha> (two-file change, same as you approved), but the PR still reads as the old head/closed" — and ask whether to reopen or open a fresh PR on the same branch. Do not silently abandon a PR whose branch you've already fixed, and don't burn the courtesy of explaining the desync.

**When a reviewer points at the "second half" of the same bug, fold it into this PR — don't defer it to a follow-up that will never be written.** On LLaMA-Factory #10759, the reviewer confirmed the `top_p` fix, then flagged that the *same* `or 1.0` silent-rewrite pattern still sat in the SGLang engine and in `repetition_penalty` at all three call sites (the HF engine never had it — the sibling was the spec). Those were one-char deletions each plus one more line in the `__post_init__` we'd already added, so folding them in was cheaper than a second PR, and it made four backends agree instead of a fork where they'd diverged. The reviewer ended with explicit praise for exactly that move. Practical rules this teaches:

- **Grep the whole repo for the same anti-pattern before submitting**, not just the single reported site. A bug reported against one implementation is usually a *class* — find its siblings (§1d) and cover them in the first pass.
- **When a reviewer finds the remaining copy, fold it in immediately** rather than "I'll open a follow-up." The reviewer is offering the scope; widening to the established sibling behaviour is what they're asking for.
- **Verify the *actual commit* each round, not just the summary.** The reviewer did this ("Verified `73d3f00` rather than the summary") — reviewers don't trust re-assertions, they trust the head they can read. When the PR grows, re-state the exact new head SHA so they know what to check.
- **Read the whole thread before treating a review as approval.** The reviewer's "ready" came only after every sibling site agreed; a single-site fix would have left the SGLang backend misbehaving and the reviewer's report open.
- **When a reviewer flags something as *deliberately* keeping (e.g. `top_k ... or -1` — a faithful `0`→`-1` translation, not a rewrite), leave it and say why.** Distinguishing what the reviewer told you *not* to touch is as important as folding in what they asked you to add — it shows you parsed their intent rather than matching a regex.

## 7. Audit against the project's own guide before calling it done
**`CONTRIBUTING.md` is often a stub.** Directus's is three lines pointing at `directus.com/docs/community/contribution/pull-requests`, and everything binding — the CLA mechanism, the mandatory changeset, the past-tense description rule — lives on that page, not in the repo. Follow the pointer; a repo-only reading misses the authoritative source.

When the PR is up, walk the guide's requirements against what you actually submitted, one line at a time, and report the result rather than asserting compliance. Name any deviation even when CI is green: this PR hand-wrote the changeset instead of running `pnpm changeset` as the guide prescribes, because the repo was never cloned. Same output, same passing check, different procedure — and worth one sentence rather than a silent pass.
