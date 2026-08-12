# RAG Repository Evaluation Criteria

Read this before scoring a RAG project in Phase 2. It layers RAG-specific signals on
top of the general criteria — issue volume, recent activity, and the PR merge reality
gate below all still apply exactly as they do for any other repo.

## 1. PR merge reality (run this before triaging issues — but after the availability filter)

Cheap things first: a repo with zero currently-open, unassigned contribution-labelled issues cannot produce a contribution today whatever its gate numbers say, and checking that costs one REST call per label. Screen the batch on availability, then gate only the survivors. This bites hardest in RAG — `deepset-ai/haystack` and `run-llama/llama_index` both passed the gate cleanly and then turned out to have nothing available at all, because their labels are empty precisely by being worked promptly.

RAG repos are among the worst offenders for this pattern: enormous star counts, daily
commits from a funded core team, a `good first issue` label full of two-year-old
entries, and a PR queue where nothing from outside the company ever lands. Measure it
directly.

**Stale open-PR share** — how much of the open PR queue has been sitting 90+ days:

```bash
curl -s "https://api.github.com/search/issues?q=repo:{owner}/{repo}+type:pr+state:open"
curl -s "https://api.github.com/search/issues?q=repo:{owner}/{repo}+type:pr+state:open+created:<YYYY-MM-DD"  # 90 days ago
```

**Outsider merge share** — of PRs merged recently, how many came from someone other
than the handful of people who merge constantly:

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=100" \
  | jq -r '[.[] | select(.merged_at != null) | .user.login
            | select(test("\\[bot\\]|(?i)bot$") | not)]
           | group_by(.) | map({u: .[0], n: length}) | sort_by(-.n)
           | {merged: (map(.n)|add), top5: (.[0:5]|map(.n)|add), oneoff: (map(select(.n==1))|length)}'
```

Report the share of merged PRs **not** from the top-5 authors, plus the count of authors
with exactly one merged PR. Both are assumption-free — you never have to decide who is
an employee.

Do **not** classify core vs. external by name, and do not trust `author_association`.
Both fail, in opposite directions. On `deepset-ai/haystack`, `author_association`
reported only 11 core authors because staff keep org membership private — `sjrl`,
`davidsbatista`, and `bogdankostic` all came back as `CONTRIBUTOR` despite obviously
being maintainers.

Use `/pulls` rather than the search API here. The search API enforces a *secondary* rate
limit that trips even when authenticated, after only a handful of rapid queries — space
search calls 5-8 seconds apart, prefer plain REST endpoints, and back off a minute or two
on a 403 mentioning "secondary rate limit" rather than retrying.

| | Healthy | Warning |
|---|---|---|
| Open PRs 90+ days old | under ~30% | over ~50% |
| Merged PRs outside the top-5 authors | 25%+ | under ~10% |
| One-off authors in the window | several | ~none |

Both in the warning column means a first contribution here is unlikely to merge no
matter which issue gets picked. Show the user the actual numbers and let them decide
whether to continue — don't silently drop the repo, and don't proceed as though the
numbers were fine.

Measured 2026-08 for reference: `run-llama/llama_index` 8% stale / 50% outside top-5,
`langchain-ai/langchain` 44% stale / 23% outside top-5, `qdrant/qdrant` 41% stale / 29%
outside top-5.

## 2. Retrieval test coverage

A RAG project that can't test retrieval without live API calls is a project where your
PR's CI will fail for reasons unrelated to your change.

- Does the repo have a test suite that exercises the retrieval path at all?
- Are LLM and embedding calls **mocked** in CI, or does CI need real API keys? Check the
  workflow files for `OPENAI_API_KEY`-style secrets gating the test job.
- If tests require live keys, a first contribution is much riskier — say so up front.

## 3. Docs surface

- Is there a `docs/` folder, and is it built from the repo (mkdocs, Docusaurus, Sphinx)?
- Docs fixes are the most reliable first contribution in RAG projects, because they
  don't touch the retrieval pipeline and don't need API keys to verify.

## 4. Large-file hazards

RAG repos accumulate artifacts that must never enter a PR:

- Vector store directories (`.chroma/`, `.faiss`, `*.index`)
- Model checkpoints and downloaded embeddings
- Cached datasets under `data/` or `.cache/`

Check the repo's `.gitignore` covers these. If it doesn't, a contributor can trivially
commit hundreds of megabytes by accident — verify `git status` before every commit.

## 5. Framework churn

LangChain and LlamaIndex both restructured their package layout more than once
(`langchain` → `langchain-core` / `langchain-community`, etc.). Before scoping a fix:

- Check when the file you're touching last moved (`git log --follow <path>`).
- Check whether the issue predates the most recent restructure — an issue filed against
  the old layout may not apply to current code at all, even though it's still open.
