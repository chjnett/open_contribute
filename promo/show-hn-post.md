# Show HN submission

## Title

Show HN: I measured which "good first issue" labels lie, and turned it into an agent skill

## URL

https://github.com/chjnett/open_contribute

## Top comment (paste immediately after posting)

Most "start contributing to open source" advice tells you to filter GitHub by the
`good first issue` label and pick something. I did that. Twice. The label lies.

What I found, measuring 15 popular repos the same day with the same method:

- **A repo can look healthy and merge almost nothing from outsiders.**
  `grafana/grafana` merges ~70% of its PRs from people outside its top-5 authors.
  `chroma-core/chroma` — 29k stars, commits daily — merges **8%**, and **17 of 17
  PRs** opened against its `good first issue`s failed to merge.
- **Issues labelled "good first issue" are frequently already claimed, already
  fixed, or quietly dead.** In one funnel I checked 229 candidate issues for linked
  PRs; 26 were still claimable, and exactly one had a defect I could verify was
  still live in `main`. One "severity:critical, 8 days old, unassigned" issue had
  already been fixed in v3.3.14 — nobody closed the ticket.

So I built `first-contribution`: an [Agent Skill](https://github.com/chjnett/open_contribute)
(Claude Code plugin) that does that measurement *before* recommending anything:

1. filters repos on availability (are there even open, unassigned issues?),
2. gates them on the **PR merge reality** — share of open PRs sitting 90+ days,
   and share of merges from outside the top-5 authors,
3. triages every candidate issue against an 8-step checklist ending with
   "does this defect still exist in current code?",
4. then walks you through claim → fork → fix → project test suite → PR → follow-up.

It's not hypothetical. Two real PRs were found and root-caused by the skill from a
cold start, both currently in review with all checks green:

- [grafana/grafana#130614](https://github.com/grafana/grafana/pull/130614) — copied
  short URLs carried the wrong org ID because the resource namespace was used as org ID
- [directus/directus#28092](https://github.com/directus/directus/pull/28092) — GraphQL
  fragments on an M2A union resolved every field to `null` (100% patch coverage)

The full method + the two charts are in the README. I'd love feedback on the merge
gate itself — the "share of merges from outside the top-5 authors" metric — since
that's the part I'm least sure generalizes.

Install: `/plugin marketplace add chjnett/open_contribute` then
`/plugin install first-contribution@open-contribute`. MIT licensed.
