# Section Checklists

Load only the subsection needed for the current task.

## Abstract

Recommended six-part order:

1. Challenge: why the problem matters, then the gap that remains unresolved (importance first, then the open question).
2. What: the framework, dataset, experiment, or argument.
3. How: the method at a high level.
4. Where: study area or case as a testbed, placed in the middle rather than the opening; name who the method is applied to, the site, and the time period.
5. Results: the most important findings in logical order, introduced by a reporting frame or stated finding-first.
6. Contribution: the study-dependent advance, optionally followed by one forward-looking or vision sentence.

Skeleton (field-agnostic phrasing). The six parts group into three moves (importance and gap, then method, then results and contribution):

- Importance, then the unresolved gap (Challenge): "[Phenomenon] is increasingly important for [outcome], but [the open question] remains unresolved because existing [approaches] rarely [capability]."
- To address it, with method, for whom, and where (What + How + Where): "To address this gap, we develop/present [method] that [how it works], applied to [whom / study area] over [period]." Keep the study area in the middle, not the opening.
- Results, then contribution: "The results show that [headline finding], because [mechanism]. [Secondary finding]. These results show how [the advance]." For policy or equity venues, one implication sentence may follow the contribution.

For the full six-part method, banned-word list, and worked examples, use the `abstract-writer` skill.

Checklist:

- [ ] Opening signals why the problem matters (its importance or stakes), then pivots to the specific unresolved gap (not study area or method name).
- [ ] Avoids unexplained technique names.
- [ ] States only claims supported by the claim-evidence ledger.
- [ ] Keeps sentences under the target journal's word and length constraints.
- [ ] Does not include precise numbers that are absent from Results or figures.
- [ ] Where names who the method is applied to, the site, and the time period, and frames the site as a testbed rather than the primary subject.
- [ ] Results open either with a reporting frame (e.g., "The results show/suggest/indicate that...") or with a direct finding-first statement; both are acceptable in the abstract (see `writing_principles.md` §1.1). If a frame is used, the finding follows immediately.
- [ ] Ends with a contribution that could not be guessed without the study. The contribution sentence is required; one forward-looking or vision sentence may follow it, but is optional.
- [ ] Keywords (4-6) add discoverability terms not in the title (e.g., methods or concepts the title omits); no keyword repeats a title word.

## Introduction

Recommended funnel:

1. Grand challenge, or the importance of the study system.
2. Thematic literature review that hooks to this study's gap.
3. Gap or scientific question the paper addresses.
4. Directional expectation or hypothesis (optional).
5. Research objective and research questions.
6. Roadmap if the journal expects one.

Checklist:

- [ ] Opens at a broad scientific or societal scale, or on the importance of
      the study system.
- [ ] Avoids a grand-narrative opener ("We live in an interconnected world",
      "In modern society ..."); starts on a specific challenge, not a
      platitude.
- [ ] Literature is thematic, not a citation dump, and the review builds
      toward this study's own gap rather than surveying the field for its own
      sake.
- [ ] Each review paragraph builds toward one research sub-question where the
      paper has sub-questions (paragraph-to-question alignment; see
      `writing_principles.md` §1.9). If the review is organized by category
      ("falls into N categories"), that is one option, not a requirement.
- [ ] Each cited work has a clear argumentative function.
- [ ] The gap or scientific question is stated explicitly. Enumerate multiple
      gaps only if there genuinely are several; do not manufacture two.
- [ ] The gap is stated firmly; the study's own contribution is stated
      modestly (asymmetric hedging: "remains unexplored" for the gap, "a first
      step" / "at least partially" for the contribution).
- [ ] Research questions are testable.
- [ ] Directional expectations are optional; state direction when a hypothesis
      is warranted, not by default.
- [ ] Roadmap uses the journal's preferred section numbering style.

## Study Area

Many field sciences (hydrology, ecology, earth science, regional planning)
carry a dedicated Study Area or Case Description section, usually between the
Introduction and Methods or as the first Methods subsection. It has its own
conventions, distinct from the sections above.

Scope note: the Abstract rule "do not open with the study area" (a
study-area-first abstract reads like a consultant report) does NOT apply here.
In this section the site is the subject, and opening with it is correct.

Recommended four-move funnel:

1. Name and quantify. Open with the site named and immediately anchored by a
   hard number, ranking, or criticality claim (drainage area, mean annual
   flow, length, population served, "the Nth largest ..."), with a figure
   pointer. For a demonstration testbed, a first-person selection opener is
   also standard ("We use [site] as our study area", "The [basin] is selected
   as the study area"), always followed by a representativeness justification.
2. Establish the stakes. Economic importance, population dependence, or a
   scarcity or crisis fact, often pivoting on "However" to the problem the
   paper addresses.
3. Layer in institutional, legal, or governance context where relevant
   (interstate compacts, water-rights priority, agency flow targets, operating
   rules). Optional; relevant where the system carries a prominent
   institutional or legal layer.
4. Justify the site as a testbed. Close by earning the site's place in the
   paper: tie each descriptive choice to a modeling consequence and state why
   the site suits the method ("a suitable test bed for our methodology", "a
   suitable candidate for the demonstration").

Two-layer hedging:

- Descriptive layer (physical facts, flows, populations, institutional rules):
  state flatly, one citation per claim. Certainty is carried by sourced
  numbers, not by adjectives. Soften magnitudes only with "approximately" or
  "about".
- Interpretive or forward-looking layer: this is where hedging concentrates
  (implications, projected conditions).
- Modeling choices are not hedged as uncertainty; state them as deliberate
  decisions and justify each immediately. Data availability is a legitimate,
  openly stated selection criterion ("most critically, data availability").

Checklist:

- [ ] Opens by naming and quantifying the site (or a first-person testbed
      selection), with a figure pointer.
- [ ] States the stakes (economic, population, or scarcity), often via a
      "However" pivot to the problem.
- [ ] Includes institutional or legal context where the water or governance
      system requires it.
- [ ] Closes by justifying the site as a testbed for the method.
- [ ] Descriptive facts carry a citation; magnitudes use "approximately/about".
- [ ] Every exclusion, data window, and spatial unit is stated as a decision
      with an explicit rationale clause.
- [ ] Does not apply the abstract-level "no study area first" rule here.

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

Every paragraph should follow this arc. The finding may share the opening
sentence with a figure-first callout in fields where that is the norm (see the
first checklist item):

```text
[finding, or figure-first callout] -> number -> mechanism -> link to research question
```

Checklist:

- [ ] Opens with the finding OR with a figure/table callout that is followed
      immediately, in the same paragraph, by the number that quantifies the
      stated finding (its effect size or magnitude, not merely a count of
      panels, tracts, or samples) and its mechanism.
      A bare "Figure X shows ..." with no number and no mechanism is the
      failure; "Figure X shows [pattern], which is [number]. This is because
      [mechanism]" is acceptable and is the dominant form in some fields
      (see `writing_principles.md` §1.1 scope note).
- [ ] Where the paper has sub-questions, the results follow the same order as
      the questions, one result thread per sub-question (paragraph-to-question
      alignment; see `writing_principles.md` §1.9).
- [ ] Includes a mechanism sentence grounded in data, method, or literature,
      often via an explicit causal connector ("This is because ...", "The
      reason for this is that ...", "A possible reason is that ...").
- [ ] Uses panel-specific figure citations when panels exist.
- [ ] Precise numbers in prose are visible or traceable.
- [ ] Counterintuitive findings passed the audit in `writing_principles.md`.
- [ ] Section-level synthesis appears after the individual findings.
- [ ] Does not overinterpret model output as causal proof.

Optional field conventions (common in modeling / simulation Results; enable
per `.paper/style_overrides.md` when your group uses them):

- [ ] Expected-vs-surprising signposting: "as expected" for confirmatory
      results, "Interestingly," / "somewhat counterintuitive" for novel ones,
      each followed immediately by a mechanism. (Used here as a deliberate
      reader signal for confirmatory versus surprising findings, not as the
      formulaic signpost cluster that `writing_principles.md` §5.5 warns
      against.)
- [ ] Certainty-grading ladder: scale the verb to the evidence within the
      section ("It is certain that ..." for controlled facts, "It is likely
      that ..." / "This may indicate ..." for inference, "we can only
      qualitatively conjecture that ..." where data is thin), with an explicit
      anti-overclaim guardrail ("we do not extend these results to claim ...").
- [ ] Validation before projection: calibrate against history with a named
      metric (KGE, NSE, RMSE), report the number, explain discrepancies, then
      present scenario or projection results.

## Discussion

Typical structure:

1. Opener: restate the framework's capability or the single headline finding,
   then signpost what the section does ("The proposed X framework provides
   ...", "In this section, we ..."). A literature-first opener is one option,
   not the default.
2. Comparison with prior work.
3. Mechanism synthesis across results.
4. Implications for theory, policy, practice, or method.
5. Limitations and future work (see the dedicated-subsection requirement
   below).

Checklist:

- [ ] Does not repeat Results paragraph by paragraph.
- [ ] Extends beyond the research questions (synthesis / boundary / implication); not a paragraph-by-paragraph re-answer to them (that 1:1 mapping is the Conclusion's job).
- [ ] Prior-work comparisons are specific and cited.
- [ ] Mechanism synthesis connects multiple findings.
- [ ] Implications are modest and evidence-bound.
- [ ] Does not undermine the central contribution.

Limitations and future work (structural requirement, not a soft nicety):

- [ ] The Discussion (or Conclusion, if merged) carries a dedicated, labeled
      Limitations and future work subsection. This survives a merged
      "Results and Discussion" or "Discussion and Conclusions" layout: even
      when the rest is merged, the standalone Limitations subsection remains.
- [ ] Limitations are enumerated ordinally ("First, ... Second, ...
      Finally, ..."), each paired with a concrete future-work remedy and,
      where possible, a citation.
- [ ] Each limitation states constraint, impact, and next step.
- [ ] The model is framed as decision-support, a first step, or an attempt,
      not a predictor.

Optional field conventions (enable per `.paper/style_overrides.md` when your
group uses them):

- [ ] Validation by external comparison: name a prior study as a benchmark,
      map its results onto this study's agents or regions, concede local
      differences, argue the aggregate agreement holds, and close on a
      convergent number.
- [ ] Scare-quotes on normative value terms ("benefit", "cost", "soft"
      policy) are an intentional overclaim-avoidance device; do not strip
      them in a polish pass.

## Conclusion

Three-part structure (parallel to the 6-part abstract, at conclusion scale):

1. **Challenge recap** (2-3 sentences): re-establish the scientific problem, why existing approaches fall short, and what this approach offers. Not a "we did X" summary; restate why it matters.
2. **Findings, one per research question** (one paragraph): name the aims, then give one finding per research question in the SAME order, each with its mechanism (the "why", not only the "what"); mark the last with "Finally,".
3. **Scope, contribution, beyond the case** (one paragraph): bound the claim honestly (limitations, hedged), state the key contribution once, and end on why it matters beyond this case or system (a transferable direction), not a methods self-compliment.

Skeleton:

- P1: "Understanding [phenomenon] requires [capability]. Existing [approaches] [limitation]. [This approach] offers [opportunity]."
- P2: "We [built or applied X] to [aim 1], [aim 2], and [aim 3]. [Finding 1], because [mechanism 1]. [Finding 2], reflecting [mechanism 2]. Finally, [finding 3], which [mechanism 3]."
- P3: "This work is best viewed as [scope]. Limitations include [a, b, c], but the findings [contribution]. By [the advance], [approach] opens [a generalizable direction]."

Checklist:

- [ ] P1 recaps the challenge (why), not a bare "what we did" summary.
- [ ] Mirrors the order of the research questions, one finding paragraph per question (1:1).
- [ ] The enumerated findings mirror the introduction's numbered objectives or sub-questions, in the same order, closing the loop the introduction opened (see `writing_principles.md` §1.9).
- [ ] Each finding carries a mechanism, not only the result.
- [ ] Introduces no new result.
- [ ] Uses numbers already verified in Results.
- [ ] Key contribution stated exactly once.
- [ ] Limitations and future work are hedged.
- [ ] Includes a generalizability or transferability sentence phrased as capability, not guarantee ("can be applied to other [systems]", not "will work everywhere").
- [ ] Final sentence explains why the study matters beyond the case (generalization, not a methods self-compliment).

Final-sentence trap: do not end the conclusion on a methods self-compliment such as "these results show why coupled modeling is useful" or "the framework is a useful tool for X." That praises the method, not the science. End on what the findings imply beyond this case or system.

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
