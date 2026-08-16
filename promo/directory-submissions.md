# Directory submissions — copy + checklist

Ready-to-paste copy for every directory. Do these in order; the first three are the
highest-leverage for search/browse traffic.

---

## 1. skills.sh

- Site: https://skills.sh (skill directory for Claude/agent skills)
- How to submit: follow [skill-factory's publishing handbook](https://github.com/rooftop-Owl/skill-factory/blob/main/handbook/publishing-skills.md)
  (section "Publishing Skills to skills.sh"). It's a GitHub-repo-driven listing, so
  your public repo is the source of truth.

**Listing copy**

- **Name:** `first-contribution`
- **Category:** Developer Tools / Open Source
- **Tagline (one line):** Find a repo that actually merges outside PRs, then go from
  "I want to contribute" to a submitted pull request.
- **Description:**

  `first-contribution` measures whether a repo actually merges PRs from outside its
  core team *before* recommending an issue. It filters repos on availability, gates
  them on the PR merge reality (share of open PRs 90+ days old, share of merges from
  outside the top-5 authors), and triages every candidate `good first issue` against an
  8-step checklist ending with "does this defect still exist in current code?". Ships
  an English variant, a Korean variant, and a RAG-specific flow (LangChain/LlamaIndex).
  Two real PRs — grafana/grafana#130614 and directus/directus#28092 — were found and
  root-caused by the skill from a cold start.

- **Tags:** `claude-code`, `agent-skill`, `open-source`, `good-first-issue`,
  `contributing`, `github`, `developer-tools`
- **Repo:** https://github.com/chjnett/open_contribute
- **Install:** `/plugin marketplace add chjnett/open_contribute` →
  `/plugin install first-contribution@open-contribute`

---

## 2. Awesome lists (open a PR to each)

Candidate lists — verify the contributor guide, then PR the repo into the right
section (usually "Skills" or "Plugins"):

- [subinium/awesome-claude-code](https://github.com/subinium/awesome-claude-code)
- [onmyway133/awesome-claude-code](https://github.com/onmyway133/awesome-claude-code)
- [frankxai/awesome-claude-code](https://github.com/frankxai/awesome-claude-code)
- [helloianneo/awesome-claude-code-skills](https://github.com/helloianneo/awesome-claude-code-skills)
- [rdmgator12/awesome-claude-plugins](https://github.com/rdmgator12/awesome-claude-plugins)

**One-line entry block (paste in the list's format):**

```
- [first-contribution](https://github.com/chjnett/open_contribute) — Agent skill that
  finds open-source issues you can actually get merged: gates repos on whether external
  PRs land, triages `good first issue`s against an 8-step checklist, and walks you to a
  submitted PR. EN + KO + RAG variants.
```

**PR title / body template**

```
## Add first-contribution

- **What:** Agent Skill for open-source contribution — filters repos on availability,
  gates them on external-PR merge rate, triages `good first issue`s, and walks the
  contribution to a submitted PR.
- **Repo:** https://github.com/chjnett/open_contribute
- **Install:** `/plugin marketplace add chjnett/open_contribute` →
  `/plugin install first-contribution@open-contribute`
- **License:** MIT
```

---

## 3. GitHub topics / discoverability (already done, just verify)

The repo already has strong topics set. Keep these; consider adding:

- `agent-skills` ✅  · `claude-code` ✅  · `claude-skills` ✅  · `good-first-issue` ✅
- add: `pull-requests`, `rag`, `developer-experience`, `open-source-tools`

Check at: https://github.com/chjnett/open_contribute → ⚙️ (gear) → **Topics**.

---

## 4. Anthropic / official & community catalogs

- **Anthropic official plugin marketplace** — the repo is already installable via
  `/plugin marketplace add`. Watch Anthropic's developer docs/announcements for how
  community plugins get into the *built-in* catalog; there is no self-serve PR path
  today, so the marketplace.json you ship is the correct public surface.
- [vsxd/agent-skills](https://github.com/vsxd/agent-skills) — portable agent skills
  directory; PR if it accepts community submissions.

---

## Order of operations (recommended)

1. Post the Show HN (highest spike potential) — see `show-hn-post.md`.
2. Same day, publish the blog on dev.to (see `blog-post.md`), link the repo at top/bottom.
3. Within the week, submit to skills.sh + open the awesome-list PRs above.
4. Post the community threads (see `community-posts.md`) linking the blog, not the repo,
   to avoid link-spam flags.
