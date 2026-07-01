# Changelog

All notable changes to `academic-writing-skills` (the Claude Code skill
at `WenyuChiou/academic-writing-skills`). Format:
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning:
[SemVer](https://semver.org/spec/v2.0.0.html).

This skill ships via the
[`WenyuChiou/ai-research-skills`](https://github.com/WenyuChiou/ai-research-skills)
marketplace; see that repo's CHANGELOG for the catalog-side history.

## [Unreleased]

## [0.3.0] - 2026-06-30

Calibrated the skill against a corpus of a water-resources advisor group's own
published papers (the corpus analysis is kept private to the maintainer). The
rules below were verified against that corpus and passed a multi-angle
adversarial gate (contradiction, corpus-faithfulness, dogfooding, anonymization,
cross-reference, apply-time usability) followed by a skeptic adjudication pass.
All additions are field-agnostic; group-specific values belong in
`.paper/style_overrides.md`.

### Added

- **Study Area section checklist** in `references/section_checklists.md` (the
  skill previously had none): a four-move funnel (name-and-quantify or a
  first-person testbed selection, stakes via a "However" pivot, an optional
  institutional or legal layer, and a mandatory testbed justification),
  two-layer hedging, a justify-every-choice lint, and an explicit carve-out
  that the abstract "no study area first" rule does not apply here.
- **§1.9 Paragraph-To-Question Alignment** in
  `references/writing_principles.md`: align Introduction review paragraphs,
  Results threads, and Conclusion findings to the research sub-questions
  (P2 to SQ1, P3 to SQ2), stated as a default to aim for rather than a rigid
  rule.
- **`references/style_overrides_customization.md`**: a generic template for
  calibrating a group's own overrides (a corpus-measurement recipe, a
  field-native word allow-list, the universal stock-phrase hard-flag list, an
  em-dash budget method, and per-section prompts). Registered in the integrity
  test manifest.
- Introduction, Abstract, Results, Discussion, and Conclusion checklist items
  for the patterns the corpus surfaced: reporting frames, who/where/time in the
  abstract WHERE, an optional forward-looking closer, figure-first Results
  openings, an opt-in certainty-grading ladder and validation-before-projection,
  a mandatory enumerated Limitations-and-future-work subsection, and a
  conclusion that mirrors the introduction's numbered objectives with a
  capability-phrased generalizability sentence.

### Changed

- **§1.1 Findings First** now scopes its figure-first ban to the abstract and
  finding-density prose, and permits a figure-first callout in Results when the
  finding's magnitude and its mechanism follow immediately in the same
  paragraph.
- **§2.1 No Overclaim** exempts the neutral reporting frame "the results
  show/showed that ..." (the hedge lives on the interpretation that follows,
  not on the frame). An unhedged causal or predictive verb after the frame
  still trips the overclaim and causal-claim audits.
- **`references/banned_words.md`**: a new Field-Native Exemptions subsection
  turns field-native words ("robust", "comprehensive", "facilitate") into a
  density check rather than a per-occurrence ban; "novel"/"first" are
  permitted-but-hedged in body sections when fenced by "to the best of our
  knowledge" and routed to a priority check, and stay banned in the abstract.
  The §6 overclaim table and the em-dash rule cross-reference the exemptions.
- Directional expectations in the Introduction are now optional rather than
  expected, and grand-narrative openers are discouraged.

### Notes

- Anonymization: a pre-existing advisor-group name in
  `references/writing_principles.md` §4.4 was generalized to "some advisor
  groups"; no advisor, paper, or basin is named anywhere in the skill.

## [0.2.4] - 2026-06-14

### Added

- **§4.10 "Each Paragraph Hands Off To The Next"** in
  `references/writing_principles.md`: a paragraph's final sentence must set up
  the next paragraph (a consequence, limitation, or open question it raises), so
  the reader feels the next question coming. Forbids both dead-stop endings and
  connective-only bridges (a "However," bolted on the start of the next
  paragraph in place of a real handoff). Complements §4.5 (transitions as a
  post-structure polish step) and §4.8 (plain, not ornate).

## [0.2.3] - 2026-06-11

### Added

- **§1.8 "Results Answers The Questions; Discussion Extends Beyond Them"** in
  `skills/academic-writing-skills/references/writing_principles.md`, plus a
  matching Discussion checklist line in `references/section_checklists.md`
  (plugin `0.2.2 -> 0.2.3`). Makes the Results/Discussion boundary explicit:
  Results answers the research questions (finding -> mechanism -> question);
  the Discussion extends beyond them (cross-result synthesis, boundary,
  positioning, implications, limitations) and is not a paragraph-by-paragraph
  re-answer (that 1:1 mapping is the Conclusion's job). The skill already
  encoded the anti-restate spirit; this adds the explicit "beyond the
  questions" framing.

## [0.2.2] - 2026-06-07

### Added

- **§1.7 "Emphasis In The Subject (End-Focus)"** in
  `skills/academic-writing-skills/references/writing_principles.md`
  (plugin `0.2.1 → 0.2.2`). Adds a sentence-level rule to §1 (Structure
  And Logic): put the main point in the grammatical subject and main
  clause, relegate secondary information (time, place, method genealogy,
  hedges) to subordinate clauses with the heaviest/newest material at the
  end (end-weight), and never split the subject from its verb with a
  time/place adverbial. Extends §1.1 (findings first) to the sentence
  level. The principle was already carried in downstream copies
  (`~/.claude/ACADEMIC_WRITING.md`, the 0.2.0 plugin cache); committing it
  to source so it survives plugin re-sync from `@main`.

## [0.2.1] - 2026-05-23

### Fixed

- **`claim_evidence_audit.md` is now schema-aware of `.paper/claims.yml`**
  (`skills/academic-writing-skills/references/claim_evidence_audit.md`,
  plugin `0.2.0 → 0.2.1`). Cross-plugin friction surfaced by Stage 7-8
  dogfood (`~/.claude/audits/dogfood_runs/2026-05-23-paper-memory-academic-writing-stage-7-8/VERIFICATION.md`
  F-cross1): SKILL.md prominently says *"When `.paper/claims.yml` and
  `.paper/figures.yml` exist (produced by `paper-memory-builder`),
  use them as ground truth instead of re-reading the manuscript"* —
  but `claim_evidence_audit.md`, the actual workflow doc, had **zero
  mentions** of any schema field (`evidence_artifacts`, `status`,
  `risk`, `sentence_in_manuscript`, `figures[].supports_claims`).
  An agent walking the audit doc had to either re-read the manuscript
  (defeating the contract) or guess how to map the YAML.
  - Adds a new `## When .paper/claims.yml is present (schema-aware
    audit, v0.2.1+)` section that maps each schema field to an
    audit-table column.
  - Documents the **status → certainty allowed** mapping:
    `supported` → direct verbs OK; `draft` → hedged verbs only;
    `gap` → NONE, must apply Disposition (1-5).
  - Documents **status transitions during audit** (e.g. `gap → draft`
    when Disposition 5 adds evidence; `draft → supported` when audit
    confirms wording matches evidence strength) so changes can be
    recorded in `.paper/revision_history.yml`.
  - Documents the **figures.yml cross-check** — every claim with
    `figure_or_table` entries should appear in the corresponding
    `figures[].supports_claims` list; mismatches flag for
    `paper-memory-builder` refresh.
  - Includes schema-aware audit pseudocode showing how to walk
    `claims.yml` while enforcing the anti-leakage rule.
  - Same shape of fix as the v0.3.13 (PR #97) F1 fix on the
    `research-context-compressor` Output spec (consumer-side
    workflow doc gains schema awareness so the producer-side
    contract is operational at workflow level).
  - Pure additive prose change to one reference file — no schema
    changes, no SKILL.md edits, no behaviour change for users
    auditing without a `.paper/claims.yml` present (they still
    follow the legacy generic-audit workflow above).

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

[Unreleased]: https://github.com/WenyuChiou/academic-writing-skills/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/WenyuChiou/academic-writing-skills/compare/v0.2.4...v0.3.0
[0.2.4]: https://github.com/WenyuChiou/academic-writing-skills/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/WenyuChiou/academic-writing-skills/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/WenyuChiou/academic-writing-skills/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/WenyuChiou/academic-writing-skills/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/WenyuChiou/academic-writing-skills/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/WenyuChiou/academic-writing-skills/releases/tag/v0.1.0
