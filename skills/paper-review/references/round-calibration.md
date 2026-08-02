# Review-Round Calibration

## Determine the Stage

Use an explicit R1–R4 label when the user supplies it. Otherwise use the base workflow's maturity labels. Comment count, file naming, apparent prose quality, and the presence of tracked changes do not establish the round.

## R1 or Developmental

Prioritize framing, contribution, manuscript architecture, missing reader functions, method feasibility, and the mapping from questions or objectives to planned evidence. Give structural guidance only when the manuscript needs it; do not impose one template on every genre.

## R2 or Substantive

When prior comments are available, begin with a compliance audit. Then emphasize equation and notation consistency, figure–text alignment, method completeness, terminology, evidence-backed interpretation, and Discussion structure.

Do not claim an R1 issue is unresolved without comparing the current artifact with the prior instruction.

## R3 or Integration

Prioritize unresolved blockers, regressions caused by revision, final interpretation, summary propagation, terminology, notation, figure captions, and the Conclusion. Keep the review targeted when the draft is stable, but report any newly discovered high-risk issue.

Do not infer near-readiness from a sharp drop in comments. Do not defer a scientifically material section merely because a historical example deferred it.

## R4 or Submission

Prioritize exact deliverables, evidence-scope integrity, Abstract and Conclusion synchronization, references, figures, supplementary ordering, authorship and funding metadata, declarations, journal requirements, tracked changes, comments, and rendering.

Do not use `FINAL` or `SUBMISSION_READY` when high-severity blockers, missing sources, stale companion files, or unverified metadata remain.

## Cross-Round Ledger

Classify prior issues as:

- `RESOLVED`: the requested change is present and did not introduce a new conflict
- `PARTIAL`: part of the request is addressed, but a material element remains
- `OPEN`: current evidence confirms it remains
- `REGRESSED`: it had been resolved but a later edit reintroduced it
- `WAIVED`: an authorized decision preserves it with a reason and risk statement
- `NOT_VERIFIABLE`: required prior artifact or source is unavailable

After material revisions, re-open upstream framing and downstream summaries rather than checking only the commented sentence.

## Audit Comment Threads Against the Current Artifact

When prior comments, author replies, tracked changes, or resolved comment threads are supplied, keep three evidence layers separate:

1. the reviewer instruction or requested decision
2. the author's response or claimed action
3. the change verified in the current manuscript and affected companion artifacts

A reply such as “revised,” “fixed,” or “addressed” does not establish resolution. Locate the claimed change in the active artifact, verify that it satisfies the instruction, and check that it did not create a contradiction or leave a stale Abstract, Conclusion, figure, table, equation, caption, supplement, or response letter.

Classify the issue as `PARTIAL` when the response is present but the verified change addresses only part of the request. Use `OPEN` when current evidence shows that the requested change is absent or substantively insufficient. Use `NOT_VERIFIABLE` when the prior instruction, cited source, earlier version, tracked-change basis, or active artifact needed for comparison is unavailable. Never upgrade a thread to `RESOLVED` from reply text or UI resolution state alone.
