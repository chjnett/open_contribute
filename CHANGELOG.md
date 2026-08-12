# Changelog

All notable changes to this project will be documented in this file.

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
