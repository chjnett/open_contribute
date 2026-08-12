# Changelog

All notable changes to this project will be documented in this file.

## [1.2.1] - 2026-08-12
### Fixed
- **Packaging was broken.** A top-level `version:` key in `SKILL.md` frontmatter is not
  part of the Agent Skills spec, and the official packager refused to build any skill
  carrying it. Version now lives under `metadata.version`, which the spec allows.
- `scripts/validate_skill.py` required the very key that broke packaging. It now enforces
  the spec's allowed-key set instead, so CI fails on a skill that cannot be packaged.
- `scripts/validate_skill.py` matched skill folders by substring, so `first-contribution`
  also matched `first-contribution-ko` and demanded references it did not carry. Now
  matched by exact folder name, with a per-skill required-reference list.
- `rag-contribution` referenced four `references/` files while shipping no `references/`
  folder at all. The folder now exists, including a new `rag-evaluation-criteria.md`.
- Removed a duplicated `curl` block in `first-contribution/SKILL.md` Phase 2.
- The build badge was a hardcoded "passing" image unconnected to CI. It now reports the
  real workflow status.

### Changed
- CI validates and packages **every** skill folder. It previously skipped
  `first-contribution-ko` entirely, and `package_skill.sh` only built `first-contribution`
  — a CI-produced release would have silently dropped the Korean variant.
- `first-contribution` Phase 1 and its two new reference files were written in Korean
  inside the English-responding skill. Translated to English.
- `first-contribution-ko` brought back in sync with the English variant: Phase 1 rewritten
  to the same five-question structure, Phase 4 migrated to the `gh` workflow, and the
  missing Phase 4.5 (pre-PR quality control) and Phase 5 (PR submission) added.
- `README.ko.md` rebuilt to match the redesigned `README.md`.
- Restored the install paths dropped in the README redesign: manual folder copy, and the
  packaged `.skill` upload for Claude.ai / Cowork.

### Added
- `.gitignore` — the repo had none, so build artifacts (`*.skill`) and `.venv/` were only
  one `git add` away from being committed.

## [1.2.0] - 2026-08-12
### Added
- Version field added to `SKILL.md`.
- CI workflow for linting and packaging.
- Validation script for `SKILL.md` frontmatter.
- Repository identifier validation before GitHub API calls.
- Packaging script for `.skill` artifact.
- Refactored Phase 1 in `first-contribution/SKILL.md` to use detailed dynamic multi-select questions (Domain -> Subcategory -> Stack -> Contribution type).
- Added `domain-categories.md` and `subcategory-map.md` to support dynamic questions.
- Added new skill `rag-contribution` tailored for Retrieval-Augmented Generation projects (e.g. LangChain).

### Fixed
- Security improvement: input validation for `owner/repo`.
