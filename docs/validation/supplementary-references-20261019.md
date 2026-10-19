# Supplementary-reference guidance: bounded validation

## Scope and fixed criteria

This release integrates the previously retained `Purposeful supplementary
references` section into the existing display/SM guide. It does not change the
main skill router, manuscript-state schema, audit operations, or manuscript files.

The ten invented cases in `evals/supplementary_reference_cases.json` fix source
facts, requested scope, and criteria before the forward test. They cover first
use, clear later pointers, unavailable sources, wrong items and numbering,
single-run inference, grammar-only work, qualitative evidence, parenthetical
pointers, run-level variation, and results that need no SM reference.

An independent native agent received the candidate skill and blind inputs with
only facts, text, and the requested revise/review/proofread action. It did not
receive the evaluator criteria. Responses were read against those criteria;
fixture checks alone do not establish semantic correctness.

## Observed outputs and narrow correction

| Case | Initial substantive response | Parent assessment |
|---|---|---|
| SM01 | Five questions are listed in Table S2. | Correct item function; no invented contents. |
| SM02 | Remove the final Table S2 pointer because the opening already cites it. | Non-pass: unnecessary style-only removal during review. |
| SM03 | Text S4 is unavailable; its support remains unverified. | Preserves the evidence gap. |
| SM04 | Cite criteria in S3, then reconcile first-mention numbering and dependent references. | Corrects the evidence target without silently renumbering unseen items. |
| SM05 | Run 8 has p=.03; S9 summarizes scores across 12 runs without a cross-run significance analysis. | Does not generalize one run's inference. |
| SM06 | The selected items are reported in Table S2. | Only the agreement error is corrected. |
| SM07 | Text S1 defines categories; S2 supplies illustrative quotations. | Distinguishes qualitative source functions without invented prevalence. |
| SM08 | Retain. | Keeps a clear parenthetical diagnostic pointer. |
| SM09 | S3 shows mean-score distributions across 20 runs. | Keeps run-level variation distinct from respondent variation. |
| SM10 | Retain. | Does not invent an unnecessary SM pointer. |

The SM02 response motivated one narrow sentence: in review-only tasks, retain a
clear, correct pointer unless a concrete reader problem warrants a change. The
same agent re-read the changed guide and rechecked **only SM02**; its response
was `SM02. retain`. The original response remains a non-pass. The nine other
cases were not rerun after this clarification.

This is a small candidate forward test plus a feedback-informed targeted check,
not a blinded paired comparison, independent replication, measured improvement,
or evidence of performance across all models, disciplines, or manuscripts.

## Deterministic checks on the final candidate

- Targeted fixture/routing/package regressions: 13 passed. The public-file hash
  check first failed against the stale manifest, then passed after synchronization.
- Full source suite: 240 passed, 2 skipped on Python 3.14.0 / Windows.
- Existing bundled regression runner: 27 checks passed.
- Public adapter: all 50 files verified; bundle built and SHA-256 recorded.
- Skill frontmatter validation: passed with Python UTF-8 mode. The initial
  default-locale run failed on cp950 decoding; no validator source was changed.

These checks establish fixture coverage, routing, metadata/package coherence,
and the observed local responses only. They do not certify scientific validity,
actual layout, citation correctness in another paper, or future writing quality.
