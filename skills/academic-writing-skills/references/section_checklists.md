# Section Checklists

Load only the subsection needed for the current task.

## Abstract

Recommended six-part order:

1. Challenge: why the problem matters scientifically.
2. What: the framework, dataset, experiment, or argument.
3. How: the method at a high level.
4. Where: study area or case, placed in the middle rather than the opening.
5. Results: the most important findings in logical order.
6. Contribution: the study-dependent advance.

Checklist:

- [ ] Opens with scientific challenge, not study area or method name.
- [ ] Avoids unexplained technique names.
- [ ] States only claims supported by the claim-evidence ledger.
- [ ] Keeps sentences under the target journal's word and length constraints.
- [ ] Does not include precise numbers that are absent from Results or figures.
- [ ] Ends with a contribution that could not be guessed without the study.

## Introduction

Recommended funnel:

1. Grand challenge.
2. Thematic literature review.
3. Gap and limitation.
4. Directional expectation or hypothesis.
5. Research objective and research questions.
6. Roadmap if the journal expects one.

Checklist:

- [ ] Opens at a broad scientific or societal scale.
- [ ] Literature is thematic, not a citation dump.
- [ ] Each cited work has a clear argumentative function.
- [ ] Gap language is specific and fair to prior work.
- [ ] Research questions are testable.
- [ ] Hypotheses or expectations state direction when possible.
- [ ] Roadmap uses the journal's preferred section numbering style.

## Methods

Recommended structure:

1. Overview of the study design or framework.
2. Data sources and preprocessing.
3. Model, experiment, or analytical approach.
4. Coupling or integration mechanism, if applicable.
5. Scenarios, variables, and metrics.
6. Calibration, validation, robustness, or sensitivity checks.
7. Reproducibility details.

Checklist:

- [ ] Overview states what the method does in one paragraph.
- [ ] Inputs, outputs, units, and time steps are explicit.
- [ ] Equations define every symbol.
- [ ] Assumptions include rationale and limitations.
- [ ] Data cleaning and exclusion rules are stated before analysis.
- [ ] Software versions, packages, seeds, and code availability are stated.
- [ ] Human-subject, animal, clinical, or ethics details are included when relevant.

Additional empirical checklist:

- [ ] Sample size or power justification.
- [ ] Randomization and blinding procedures, if applicable.
- [ ] Inclusion and exclusion criteria.
- [ ] Statistical assumptions checked.
- [ ] Effect sizes and confidence intervals, not only p-values.
- [ ] Outlier rules stated before analysis.

Additional qualitative or archival checklist:

- [ ] Primary source locations and dates accessed.
- [ ] Coding scheme or analytical framework.
- [ ] Inter-rater reliability, if multiple coders.
- [ ] Reflexivity or positionality statement if warranted.

## Results

Every paragraph should follow:

```text
finding -> mechanism -> link to research question
```

Checklist:

- [ ] Opens with the finding, not "Figure X shows".
- [ ] Includes a mechanism sentence grounded in data, method, or literature.
- [ ] Uses panel-specific figure citations when panels exist.
- [ ] Precise numbers in prose are visible or traceable.
- [ ] Counterintuitive findings passed the audit in `writing_principles.md`.
- [ ] Section-level synthesis appears after the individual findings.
- [ ] Does not overinterpret model output as causal proof.

## Discussion

Typical structure:

1. Main findings in brief.
2. Comparison with prior work.
3. Mechanism synthesis across results.
4. Implications for theory, policy, practice, or method.
5. Limitations and future work.

Checklist:

- [ ] Does not repeat Results paragraph by paragraph.
- [ ] Prior-work comparisons are specific and cited.
- [ ] Mechanism synthesis connects multiple findings.
- [ ] Implications are modest and evidence-bound.
- [ ] Limitations state constraint, impact, and next step.
- [ ] Does not undermine the central contribution.

## Conclusion

Checklist:

- [ ] Mirrors the order of the research questions.
- [ ] Summarizes what was done and what was found.
- [ ] Includes the strongest mechanism or implication.
- [ ] Introduces no new result.
- [ ] Uses numbers already verified in Results.
- [ ] Final sentence explains why the study matters beyond the case.

## Cover Letter

Checklist:

- [ ] Addresses the editor or journal correctly.
- [ ] States the central contribution in one or two sentences.
- [ ] Explains why the journal is a good venue.
- [ ] Confirms originality and no concurrent review.
- [ ] Notes related preprints or prior submissions.
- [ ] Suggests reviewers only if the journal allows.
- [ ] Avoids inflated claims not present in the manuscript.

## Reviewer Response

For reviewer response, use `reviewer_response_workflow.md`. This section is only
the quick gate:

- [ ] Every comment has a numbered response.
- [ ] Every response names the manuscript change.
- [ ] Every disagreement is evidence-backed.
- [ ] No response says "clarified" without a visible revision.
- [ ] Contradictory reviewer requests are reconciled explicitly.
