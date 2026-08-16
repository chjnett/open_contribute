# Good first issue labels lie. I measured it, then built an agent that checks first.

*~1,100 words · target: dev.to / personal blog / GeekNews-en*

---

Everyone gives beginners the same advice: go to GitHub, filter by `good first issue`,
and pick something. I followed that advice. Twice. Both times it cost me real work
before I realized the label had nothing to do with whether my PR would ever land.

The worst part: the failures were invisible. A repo can look thriving — daily commits,
hundreds of merges a quarter, thousands of stars — while merging almost nothing from
anyone outside its core team.

So I started measuring, and then I built an agent skill around the measurement.

## The measurement

I took 15 popular repositories, same day, same method, and counted two things:

1. **The merge reality gate** — what share of open PRs have been sitting 90+ days,
   and what share of merged PRs came from authors outside the repo's top-5 committers.
2. **Triage attrition** — for candidate "good first issue" candidates, how many
   already had a linked PR.

The results were uncomfortable.

`grafana/grafana` merges about **70%** of its PRs from people outside its five most
frequent authors. `chroma-core/chroma` — 29,000 stars, commits pushed every day —
merges **8%**. And of the 17 PRs opened against its `good first issue`s, **17 out of
17 failed to merge**. Both repos look identical from the outside: active, popular,
welcoming.

The charts are in the repo, method printed on each:

![Share of merged PRs from outside each repo's top-5 authors](https://github.com/chjnett/open_contribute/raw/main/assets/merge_gate.png)

![Share of candidate issues that already had a linked PR](https://github.com/chjnett/open_contribute/raw/main/assets/triage_attrition.png)

## The race you don't see

Even on healthy repos, the label has a shelf life. Anything recent, well-scoped and
labelled tends to get claimed within hours. By the time you finish reading the code,
there's a linked PR from six months ago — or a fix already merged with the issue never
closed.

The worst case I hit: an issue that was 8 days old, unassigned, `severity:critical`,
zero linked PRs. It passed every "is this claimable?" check I had. It had already been
fixed in `v3.3.14`. The bot simply never closed the ticket.

That's the moment the checklist was born.

## What the skill actually does

`first-contribution` is a Claude Code plugin (an "Agent Skill") that runs this funnel
before it recommends anything:

1. **Filter on availability first.** A repo with no currently-open, unassigned
   contribution issues can't produce a contribution today. That's one cheap API call,
   and it eliminates most repos before the expensive evaluation.
2. **Run the merge reality gate.** You see the numbers — 90-day stale-PR share and
   outside-author merge share — and decide. The skill never silently drops a repo.
3. **Triage every candidate issue** against an 8-step checklist: internal-only notices,
   linked PRs, assignees, resolving comments, claim pile-up, age — and finally whether
   the defect *still exists in current code*.
4. **Walk the contribution.** `gh`-based fork and clone, scoped edits, the project's
   real test suite, and a pre-PR checklist covering DCO, signatures and CLAs — then
   submission and follow-up etiquette.

It responds in English, Korean, and there's a RAG-specific variant for the
LangChain/LlamaIndex crowd.

## Does it work?

Two pull requests, each found and root-caused by the skill from a cold start:

| PR | Bug | State |
| :--- | :--- | :--- |
| [grafana/grafana#130614](https://github.com/grafana/grafana/pull/130614) | Copied short URLs carried `orgId=org-5` because the resource namespace was used as the org ID | All checks green, in review |
| [directus/directus#28092](https://github.com/directus/directus/pull/28092) | GraphQL fragments on an M2A union resolved every field to `null` | All checks green, 100% patch coverage, in review |

The second run is the better illustration of the funnel: **30** backend repos screened
for availability → **13** with open contribution issues → **11** through the merge gate
→ **229** candidate issues checked for linked PRs → **26** still claimable → **one**
with a defect verified live in `main`.

## What it cost to learn

Every rule in the checklist was added after it cost a real run something:

- `chroma-core/chroma` is why the merge gate exists.
- `deepset-ai/haystack` taught me an empty label on a *healthy* repo means "come back
  later" — the opposite diagnosis from a rotten one.
- `argoproj/argo-cd#29051` is why the checklist now verifies the defect against
  current code instead of trusting the ticket.
- Grafana and Directus have *different* CLA mechanisms — one is an external signing
  service, the other asks you to add your username to `contributors.yml` inside the PR.
  The skill will never sign a CLA for you.
- A confident second-hand summary of my own PR claimed 28 workflows were awaiting
  approval. The API showed zero. I'd have burned my one follow-up nudge on a
  non-problem.

## Try it

```
/plugin marketplace add chjnett/open_contribute
/plugin install first-contribution@open-contribute
```

Then just say *"I want to start contributing to open source"* or
*"is this repo beginner-friendly?"*.

MIT licensed. If it recommends a stale issue or misjudges a repo, open an issue — that
feedback is literally what the checklist is made of.
