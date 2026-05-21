# Changelog

All notable changes to `academic-writing-skills` (the Claude Code skill
at `WenyuChiou/academic-writing-skills`). Format:
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning:
[SemVer](https://semver.org/spec/v2.0.0.html).

This skill ships via the
[`WenyuChiou/ai-research-skills`](https://github.com/WenyuChiou/ai-research-skills)
marketplace; see that repo's CHANGELOG for the catalog-side history.

## [Unreleased]

### Added

- **CI `skill-version-guard` job** (`.github/workflows/test.yml`).
  Blocks a PR that changes `skills/` content without also bumping
  `.claude-plugin/plugin.json` `version`. The marketplace plugin
  cache is keyed on the version string, so an un-bumped skill change
  ships to `main` but never reaches user installs. The `0.2.0`
  release itself was a fix for exactly this — the `§8 step 10`
  change had merged without a version bump (dogfood finding V1b).
  This guard makes that a hard CI failure at PR time. Workflow-only
  change; no plugin version bump needed (the guard does not fire on
  `.github/` edits).

## [0.2.0] - 2026-05-21

### Added

- `.github/workflows/test.yml` — runs `python -m pytest tests/ -q` on
  push + PR to `main`.

### Changed

- **Plugin version `0.1.0` → `0.2.0`** (`.claude-plugin/plugin.json`).
  Required so the §8 step-10 change below actually reaches user
  installs: the marketplace plugin cache directory is keyed on this
  version string. A 2026-05-21 Phase 9 behavioral verification found
  step 10 was correct on `main` but absent from the cached `0.1.0`
  bundle — the change had shipped to the repo but not to installs.
  Bumping the version forces a fresh cache directory on
  `claude plugin update academic-writing-skills@ai-research-skills`.
- **§8 Self-Audit gains a mandatory claim-gap cross-reference (step 10).**
  The 2026-05-20 `ai-research-skills` dogfood found a real gap: a
  banned-word / overclaim audit could pass a sentence as
  linguistically clean while that sentence asserted a claim the
  `paper-memory-builder` memory layer recorded as `status: gap`
  (unevidenced). The skill consumed `.paper/claims.yml` as a context
  *source* (§4) but never cross-referenced audited prose against the
  `gap` status. Step 10 now makes it mandatory: every assertive
  sentence mapping to a `status: gap` claim must be flagged
  `[MATERIAL GAP]`, on overclaim / banned-word / claim-evidence
  audits alike — a clean-prose verdict never overrides a `gap`
  finding. Step 10 carries an inline `claims.yml` row-schema note
  (`id` / `text` / `status` one of `draft | supported | rejected |
  gap`) so a session that has not loaded `paper-memory-builder` can
  still execute it, plus an "assertive sentence" heuristic. Closes
  the dogfood C2 PARTIAL finding for audits orchestrated through
  `SKILL.md` §8 — a future caller that runs a banned-word pass as a
  standalone subagent without loading `SKILL.md` is out of this
  step's reach.
- **Frontmatter description surfaces the `paper-memory-builder`
  upstream-dep ordering hint.** Body text already explained the
  contract ("if `.paper/claims.yml` exists, prefer it; refresh via
  paper-memory-builder if changed", lines 96-100) and
  `WenyuChiou/ai-research-skills/CONTRIBUTING.md` §2 documents the
  cross-skill artifact contract — but the frontmatter `description`
  field never mentioned it. Auto-trigger by Claude Code routes via
  description-keyword matching, so the trigger-time hint to consider
  running `paper-memory-builder` first for multi-section /
  claim-evidence / reviewer-response work was missing. Closes the
  D6 / Phase 2 Item #6 gap surfaced by the `ai-research-skills`
  Task #27 dogfood walk.

### Fixed

- `tests/test_skill_integrity.py` — pre-existing bug: tests pointed at
  `ROOT / "SKILL.md"` and `ROOT / "references/..."`, but the
  2026-04-26 marketplace migration (commit
  [`fca3dc7`](https://github.com/WenyuChiou/academic-writing-skills/commit/fca3dc7))
  moved both under `skills/academic-writing-skills/`. Tests had never
  run in CI (none was configured) so the breakage was silent. Updated
  to use `SKILL_DIR = ROOT / "skills" / "academic-writing-skills"`.

## [0.1.0] - 2026-05-13

The initial published version. Captures the skill as it stood at
commit [`a04dee7`](https://github.com/WenyuChiou/academic-writing-skills/commit/a04dee7)
("Strengthen skill with 6 audit-driven additions"), the HEAD on
`main` when this CHANGELOG was first added.

### Included

- `SKILL.md` — Claude Code skill manifest with frontmatter + the
  full academic writing workflow (manuscript revision pipeline,
  banned-word + humanise pass, claim-evidence audit, journal-format
  check, reviewer response).
- `references/` — reference files for §4.x writing principles
  (no invented compound terms, colon/semicolon limits, domain-native
  vocabulary, …).
- `tests/test_skill_integrity.py` — pytest covering frontmatter
  validity, required-files presence, mojibake checks, eval shape,
  and bilingual README cross-reference.
- Bilingual `README.md` + `README.zh-TW.md`.
- `LICENSE` (MIT).
- `.claude-plugin/plugin.json` so the root SKILL.md is picked up by
  the `WenyuChiou/ai-research-skills` marketplace.

### Known limitations (as of 0.1.0)

- No GitHub Actions CI yet — pytest is run locally before each
  commit. (CI added in [0.2.0] above.)
- Tested by one graduate-student researcher; not corpus-scale
  validated.
- Domain lean: water-resources / agent-based modeling phrasing
  conventions surface in some references; the core workflow is
  domain-neutral.

[Unreleased]: https://github.com/WenyuChiou/academic-writing-skills/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/WenyuChiou/academic-writing-skills/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/WenyuChiou/academic-writing-skills/releases/tag/v0.1.0
