# Reviewer Red Team and Release

## Contents

1. Negative-space review
2. Issue classification
3. Release gate
4. Functional-completeness report

## Negative-Space Review

Search for what the manuscript fails to expose:

- a question with no substantive answer
- a method with no result or a result with no method
- one model, group, outcome, period, or scenario missing a field reported for its peers
- a conclusion that depends on evidence absent from the paper
- a fact inferred from formatting or an old artifact
- a required assumption that is never stated
- a pattern that could be induced by inputs, sampling, preprocessing, or measurement failure
- separate significance results presented as a significant difference
- missing privacy, ethics, conflict, data-retention, or reproducibility information
- a broad title or contribution whose actual outcome is narrower

Build a dimension-completeness matrix whenever three or more entities should be reported symmetrically.

For each main claim, ask:

1. What direct evidence supports it?
2. What plausible alternative explanation remains?
3. What unavailable evidence would change the conclusion?
4. What is the narrowest defensible wording?
5. Where else must this wording propagate?

## Issue Classification

Label every material issue with:

- scope: surface, semantic, section, manuscript, project, validity, or epistemic
- severity: S0–S4
- evidence: confirmed, probable, or unverified
- status: open, resolved, or waived
- authority or source needed
- affected artifacts and gates

Do not rank by how easy the prose is to edit. Rank by risk to the scientific task, inference, reproducibility, ethics, and submission integrity.

## Release Gate

Allow `SUBMISSION_READY` only when:

- S3 and S4 open blockers equal zero
- required sources and facts are verified or their limits are explicitly disclosed
- locked semantic content is current
- every central question or objective has a method, evidence, answer, and bounded interpretation
- dimension coverage is complete or justified
- summaries and companion artifacts match the active evidence
- exact filenames and active-release membership are unambiguous
- structural and visual checks passed on the final files
- required venue and ethical statements are present
- the final functional-completeness retrospective has no unresolved “no” answer

If a high-severity issue is waived, do not convert it to passed. Report the waiver, authority, reason, and remaining risk.

## Functional-Completeness Report

End every check with a compact record:

```text
FUNCTIONAL-COMPLETENESS RETROSPECTIVE
Scope covered: [artifacts and lifecycle stages]
Authority and locks: [passed / limits]
Alignment: [passed / affected links]
Adapters and overlays: [which ran / conflicts]
Change propagation: [artifacts rechecked]
Deterministic and visual checks: [performed / not applicable / limits]
Open issues and unknowns: [counts by severity]
Readiness: [not ready / conditionally ready / ready for named purpose]
```

Do not write `all functionality considered` without naming the dimensions reviewed and the remaining limits.
