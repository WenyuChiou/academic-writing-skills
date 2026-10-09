# First-Draft Execution and Handoff Acceptance

Use this procedure before the **first** delivery of a substantive passage or
formatted artifact, not only after the author finds a problem. It operationalizes
the existing integrity gates; it does not add a fixed article structure or a new
scientific standard. A language scan alone is never section acceptance.

## Before writing: agree on the reader's route

Reuse the active contract and sources. Name the reader's likely knowledge, the
unit being compared, the paragraph functions, and the minimum prerequisites.
For section work, write a short function sequence before drafting: what is
established, what is added next, and what question the sequence answers. For a
bounded paragraph, inspect only its available neighbors. Do not silently invent
missing context or impose a whole-paper rewrite on a local edit.

Keep the primary comparison visible before its dependent detail. If the author
asks for human-versus-LLM comparison, introduce that comparison before differences
between individual LLMs. In another study the primary contrast may be treatments,
regions, theories, or time periods. **Human-first is a project choice, not a
universal rule.** Definitions and technical terms must arrive before the reader
needs them; explain their role, not just their expanded acronym.

For displays, allocate information before composing the caption:

- Caption: what is shown and the essentials needed to decode it independently.
- Main text: the supported finding, comparison, interpretation, and next step.
- Methods/SM: extended procedures, selection rules, settings, or diagnostics.

Remove repeated procedures from captions, but retain an essential sample/run
convention, uncertainty definition, denominator, or exclusion if omitting it would
mislead the reader. Do not enforce a universal caption word count.

## Before handoff: perform, then record

After the last edit, inspect the **exact** candidate and its affected dependencies.
Record a located finding for each applicable check; a tick or a stock assurance
is not evidence that the check ran. Existing project notes can hold these records.
For a local chat edit, a concise inline record is enough; do not create a project
state or JSON file merely to revise a sentence.

| Check | Required action and acceptance evidence |
| --- | --- |
| Meaning and evidence | Compare the candidate with locked meaning and source evidence; locate any changed claims or citations. For grammar-only work, preserve unchanged verified support and do not claim a fresh literature audit. |
| Language scan | Run the applicable terminology/stock-phrase checks on these bytes and resolve or explicitly retain each contextual finding. A scan's `PASS` covers that scan only. |
| Reader walkthrough | Before the first handoff and after any later substantive prose edit, read or simulate a cold pass by an informed cross-disciplinary reader who knows the broad field but not the study's internal shorthand. For substantive paragraph or section work, inspect **every adjacent sentence pair**: state what the next sentence adds and why it follows from the previous one, then identify the evidence, comparison, referent, or prerequisite in the text that lets the reader make that link. Check unclear actors, technical terms, comparisons, and referents. If the relation cannot be paraphrased from the passage without hidden project history, repair the order, content, reference, or qualification; removing a redundant sentence may be the minimal repair. Adding a transition word alone is not a repair. Do not force an explicit connector between every sentence, or rewrite necessary technical repetition just to vary the wording. Then paraphrase what the passage lets the reader conclude. An actual independent cold reader is useful for a complex section or a repeated comprehension failure when available; do not fabricate one. |
| Progression and framing | For substantive work or a section/package, read openings and endings in sequence. Record what each paragraph adds and the actual relation at each boundary. Repair repeated functions, jumps, and drift from the author-locked comparison; adding connectors alone does not repair logic. |
| Limitations framing | When limitations are in scope, distinguish a choice, uncertainty, or design boundary in the data, indicator, measurement, model, or study scope from correctable errors or missing required work. For a genuine research boundary, name the documented source or condition, what it makes uncertain, and the specific result or inference it limits. Verify the uncertainty before describing it; do not infer a bias direction or call the paper defective. Correct a fixable error, or report unresolved required work accurately, rather than relabeling it as a limitation. |
| Caption allocation | When displays/captions are affected, compare each caption with its figure, main text, and Methods/SM. Locate essentials kept and redundancies removed; recheck panel mapping, statistics, and callouts. |
| Final layout | When editing a formatted file, inspect its saved rendering at the intended size: caption position, spacing, page breaks, figure placement, legibility, and overlap. Verify direct formatting plus inherited styles; preserve a working baseline unless a verified rule or author request warrants change. XML, DPI, and source-image inspection do not certify the embedded layout. |
| Editor identity | For formatted edits or metadata changes, verify the explicit expected identity against **new** revision/comment/reply authors and applicable file properties. Preserve historical authors and comments; do not rewrite everyone as the current author or infer identity from the assistant/model name. |
| Venue basis | When venue-directed formatting is applied, identify the dated official requirement, author/project preference, or observed example. Do not present a local spacing or caption choice as a journal mandate. Unavailable official guidance stays unverified; provisional formatting may proceed without compliance certification. |

Use `checked` only with a concrete locator, finding, and resolved/open outcome.
An open finding remains incomplete even if the check ran. Distinguish `not_run`,
`unavailable` (with reason), and `not_applicable` (because the check is outside the
declared scope/effects). Never turn unavailable sources, an author waiver, or a
clean banned-word scan into a pass. Missing neighboring text limits continuity
verification, but does not prevent a clearly labeled provisional local draft.

## Optional deterministic coverage checker

For repeated or multi-file handoffs, use `scripts/audit_handoff.py RECORD --json`
to validate a **coverage record**, not the quality or truth of its findings. It
requires no managed manuscript state. Reuse existing records when equivalent;
do not manufacture a second bookkeeping system to satisfy this format.

The JSON contract is:

- `schema_version`: integer `1`; `scope`: `sentence`, `paragraph`, `section`, or
  `package`; `change`: `surface` or `substantive`.
- `features`: four explicit booleans: `displays`, `formatted_file`,
  `venue_formatting`, `metadata_changes`. Declare effects honestly; the checker
  cannot infer them from document contents. Formatted edits require identity
  verification even if metadata was not deliberately changed.
- `artifacts`: nonempty list of `{id, path, role, sha256}` records. Paths are
  absolute or relative to the coverage file; hashes cover exact file bytes.
  At least one role is `candidate`; other roles are `context`, `evidence`, or
  `render`. Include the current adjacent prose/contract and affected sources or
  render evidence used in the checks so changed dependencies invalidate coverage.
- `checks`: names from the table, in snake case. Each `checked` entry has
  `outcome` (`resolved` or `open`), nonempty `artifact_ids`, `locator`, and
  `finding`. Pending entries have a status and `reason`.
- Checked `final_layout` references an artifact with role `render`, bound in
  the review finding to the exact saved candidate and rendering procedure.
  Checked `editor_identity` also records `expected_author` and
  `new_edit_authors`; these concern this edit, not all historical authors.
  An empty list requires `absence_reason` documenting inspected absence of new
  revision/comment/reply authors and applicable identity-bearing file properties;
  never fill it with a fictional author just to satisfy a gate.
- Checked `venue_basis` also records `basis` (`verified_requirement`,
  `project_preference`, or `example`) and `source` (dated official source or
  explicit instruction/example locator). Source strings are not independently
  verified by this tool.

For a meaning-preserving sentence edit with no file/display/venue effects, only
`meaning_and_evidence`, `language_scan`, and `reader_walkthrough` are required.
For substantive work, `progression_and_framing` is also required. Extra applicable
checks follow the effects above; a required check cannot be marked not applicable.

The CLI is read-only and uses the standard library. It returns `0` for
`COVERAGE_COMPLETE`, `1` for `INCOMPLETE`, and `2` for invalid records or read errors.
Every result explicitly states that editorial quality is **not certified**.
It cannot detect fabricated notes, dishonest applicability declarations, semantic
errors, or a render made from the wrong document merely by validating hashes.

## Close the handoff honestly

Report the candidate checked, the applicable coverage completed, and the specific
remaining limits. A provisional draft can be useful while source or layout checks
are pending; do not label it final, fully checked, or journal-compliant. A complete
record still requires editorial and scientific judgment under the existing gates.
Any relevant wording, citation, metadata, formatting, or dependency change
invalidates earlier acceptance: update the exact candidate and recheck affected
gates before delivery. Do not defer these checks because this is “only a first
draft,” and do not force unrelated full-package checks onto bounded work.
