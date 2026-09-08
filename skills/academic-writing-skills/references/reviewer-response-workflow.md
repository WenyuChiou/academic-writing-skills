# Reviewer Response Workflow

Use this reference for rebuttal letters and response-to-reviewers documents.

## Core Rule

A response is complete only when it directly answers the concern and either
points to a visible manuscript change or gives an evidence-backed reason for not
making the requested change. The response document may include analyses and
implementation details that help the reviewer but do not belong in the
manuscript or Supporting Material.

## Build a Comment Ledger First

Track every comment before drafting prose:

```markdown
| ID | Reviewer Comment | Anchor Text | Response Strategy | Manuscript Change | Status |
|---|---|---|---|---|---|
| R1.1 | ... | Section 3.1 | revise model; Figure R1 | revised method | RESOLVED |
```

Preserve reviewer comments verbatim. Split multi-part comments into their actual
questions so a polished paragraph does not hide an unanswered part. Record
subquestions and evidence within the response-strategy cell or add optional
columns when a complex revision needs them; do not create a second incompatible
ledger schema.

Use the manuscript-state status contract: `OPEN` for unresolved work,
`RESOLVED` for a completed and verified response, and `WAIVED` only when an
identified authority accepts the remaining issue and risk.

Classify the required work as one or more of:

- clarify an existing method or result;
- correct an error or ambiguous specification;
- add or rerun an analysis;
- add evidence or a citation;
- revise interpretation, scope, or limitation;
- decline or defer a request with a specific reason.

## Distinguish Navigation from the Full Answer

Reviewers sometimes provide high-level synthesis points before numbered major
comments.

- Keep a high-level response concise: acknowledge the issue, state the major
  action, and direct the reader to the detailed response below.
- Put the first complete explanation, design, evidence, and result under the
  earliest detailed comment that raises the issue.
- Treat every detailed reviewer comment as independently readable. A later
  related response must include enough local context, the key result, and its
  meaning to answer the distinct concern. It may refer backward for the full
  shared design, figure, or table instead of repeating that evidence.
- Do not make an earlier detailed response depend on a later reviewer response.
  Forward references are appropriate only in an introductory navigation block.

## Draft a Major Response in This Order

Use the smallest number of paragraphs needed while preserving this reasoning
order:

1. **Recognize the concern.** Explain briefly why the comment identified an
   important problem or opportunity.
2. **State what changed and why.** Name the method, model setting, analysis, or
   interpretation that changed. When correcting a specification, explain the
   inconsistency rather than implying that a parameter was tuned only to obtain
   a preferred result.
3. **Explain the implemented procedure.** Give enough detail for the reviewer to
   judge the work, including material details that are unnecessary in the paper.
4. **State the scope of the work.** If the change required a complete model
   rerun, regenerated figures, or repeated analyses, say so explicitly.
5. **Present verified evidence.** Put the statistical properties and comparison
   basis needed to interpret a number before the number. Give denominators,
   reference values, uncertainty summaries, or matched settings when relevant.
6. **Interpret the result.** Do not stop after reporting numbers or describing a
   figure. State what changed, what remained stable, and how the evidence
   addresses the concern.
7. **Identify manuscript changes.** Name the actual sections, figures, tables, or
   Supporting Material entries. Use final line numbers only after the clean
   manuscript is stable.
8. **State remaining boundaries when material.** Name what the study still does
   not represent and give the reason. Do not answer with a bare “no.”

For a short clarification or typographical correction, compress this sequence
to one or two sentences instead of manufacturing unnecessary detail.

When a multi-part comment requires both qualification and action, answer the
qualified point fully before shifting emphasis. Then use an explicit transition,
such as “However, we agree...” or “Following the reviewer’s suggestion...,” to
identify the part the authors accept and the concrete analysis or revision they
performed. This makes the responsive action visible after a careful defense, but
it must never distract from, replace, or leave incomplete the answer to the first
part of the comment.

## Match Response Length to the Scientific Weight

A comment that triggers a model redesign, new dataset, new analysis, or complete
rerun requires a response at least as complete as the reviewer comment and should
normally be comparable in length. Treat length as a warning that reasons,
implementation details, evidence, or implications may be missing, never as a
reason to repeat material or add filler. Make the additional work visible without
turning the response into a second Methods section. Minor editorial comments do
not require artificial expansion.

For a major model or analysis change, consider a response-only table or figure
when it lets the reviewer verify the effect quickly. Use one only when it directly
isolates the challenged factor and is based on the current model and evidence.
Do not include a comparison that mixes several simultaneous changes or relies on
obsolete outputs merely to make the response appear more substantial.

## Present Numbers Without Creating a New Vulnerability

- Give the denominator or comparison value for every absolute error or count
  when the reader needs it for interpretation.
- Explain data coverage, unit of analysis, geographic mismatch, or other
  statistical limits before presenting a potentially misleading metric.
- Use neutral descriptions of observed values. Avoid supplying verdicts such as
  “the model fails,” “weak agreement,” or “overall overestimation” unless that
  conclusion is supported and necessary.
- Point out the scientifically relevant signal, whether favorable or
  unfavorable, but do not advocate past the evidence.
- Do not explain standard metrics to a specialist unless the definition is
  study-specific. Explain what the values mean for this analysis instead.
- Separate an absolute-value diagnostic from a normalized temporal comparison
  and state which question each one answers.

## Explain Sensitivity and Robustness Results

A sensitivity response must identify:

- the challenged assumption;
- the current setting and alternatives in plain language;
- what was held constant;
- the outcomes used to judge sensitivity;
- the direction and magnitude of the result;
- whether the relevant interpretation changed; and
- where the result is reported.

Organize each sensitivity response as **why → what → comparison → result →
meaning**. If the reviewer explicitly requests a test, state how the selected
design answers that request. If the reviewer does not explicitly request a
test, first explain why the challenged assumption could affect the reported
outcomes and why an additional test is informative. Then name the exact
settings or groups compared and the outcomes used to judge the effect. Never
introduce an experiment without explaining its purpose.

Place the information needed to interpret a figure or table in the response
prose before the evidence is presented. This includes the comparison baseline,
the changed factor, the number of comparisons when material, the uncertainty
summary, and the meaning of positive or negative differences. Keep table notes
minimal and use them only for compact self-contained details; do not hide the
experimental design, comparison logic, or substantive interpretation in a
note.

Keep the adopted baseline model specification distinct from the sensitivity
procedure. Report the procedure in the Methods, Supporting Material, or response
letter as required by the venue and reproducibility needs; do not describe an
unchanged sensitivity setting as part of the adopted baseline formulation.
Report the resulting effects and interpretation in the Results or Discussion
when they matter to general readers, and place extended evidence in the
Supporting Material or response letter. State the chosen destination explicitly
and do not duplicate the same detail across all locations.

Do not use internal experiment IDs, unexplained labels such as “higher” or
“narrower,” or software terminology that the reviewer has not seen. Name the
actual parameter interval, rule, distribution, or event sequence.

When several comments concern the same experiment, give the full design and
evidence at the first substantive occurrence. Later responses must still state
the local purpose, key result, and comment-specific meaning, but may cite the
earlier figure or table for the shared design and full evidence.

## Separate Three Destinations

Every response should distinguish among:

1. **Response only:** diagnostic evidence, comparison tables, or implementation
   details needed to answer the reviewer but not needed by general readers.
2. **Main manuscript:** changes necessary for method transparency, result
   interpretation, or the main conclusion.
3. **Supporting Material:** reproducibility details, extended methods, full
   technical results, or instruments the authors have chosen to provide.

Do not promise a manuscript or Supporting Material addition merely to sound
accommodating. Do not claim that a change was made until it exists. During
planning, use future tense. In the final response letter, use past tense after
verifying the tracked and clean files.

## Tone and Vocabulary

- Use professional appreciation when the comment led to a meaningful change,
  but do not begin every paragraph with the same formula.
- Lead with the answer, followed by evidence and the manuscript change.
- Use terminology already present in the manuscript. Define an abbreviation on
  first use within a reviewer section when the reader may not have seen it.
- Define a study-specific term immediately and place it in quotation marks on
  first use when that helps distinguish it from established terminology.
- Avoid invented compound labels, vague references such as “the revised design,”
  and unexplained internal shorthand.
- Prefer plain sentences with explicit subjects and actions. Vary transitions so
  adjacent paragraphs do not read as disconnected bullets or repeated “We...”
  statements.
- Do not overstate completion, robustness, validation, or generalizability.

## Disagreement or an Unimplemented Request

Disagreement is acceptable when supported by evidence. Use this structure:

1. recognize the concern;
2. state the evidence, data boundary, or convention;
3. explain why the requested implementation is not defensible or feasible;
4. give the closest valid analysis or clarification when one exists; and
5. state the resulting limitation or future direction without using it as a
   substitute for the present answer.

Do not write “we respectfully disagree” or “this is outside scope” without an
argument. Do not add a partial mechanism that cannot be represented consistently
only to appear responsive.

## Contradictory Reviewer Requests

When reviewers request incompatible changes:

1. identify the conflict explicitly in the working ledger;
2. prioritize the editor's decision, journal scope, study evidence, and internal
   consistency rather than trying to satisfy both requests mechanically;
3. explain the selected approach in both reviewer responses so neither response
   appears to ignore the other concern; and
4. request editor guidance in the cover letter when the conflict cannot be
   resolved without changing the study's scientific scope.

## Formatted Response Documents

When the deliverable is a Word response document:

- preserve reviewer comments verbatim and in their existing color;
- preserve response color, tracked changes, margin comments, page setup, and the
  established lab template;
- format response-only figure and table labels consistently;
- keep references in the document's established location;
- verify cross-page comment-response blocks, table breaks, captions, equations,
  and figures after rendering; and
- do not fill line-number placeholders until the clean manuscript is stable.

Use the available `docx` or Word-document skill for tracked-change and OOXML
operations.

## Checks After a Model or Evidence Revision

These checks address recurring failures when a revised model changes both the
numbers and the explanation of the results:

- **Lock the current evidence first.** Identify the source version, configuration,
  and outputs behind each result. An old figure or completed experiment is not
  current evidence merely because its label still matches the comment.
- **Separate direction, magnitude, and mechanism.** A group can retain a larger
  proportional loss reduction while the process producing that reduction changes.
  Do not summarize this as “the conclusions are unchanged.” State precisely what
  remains and what must be reinterpreted. Distinguish absolute losses, percentage
  reductions, and losses relative to income or another denominator.
- **Do not attribute a combined revision to one factor.** Results after several
  model changes describe their combined effect. Claiming that one change caused a
  difference requires an appropriate controlled comparison or other supporting
  evidence. A mechanism suggested by the decision rule is not automatically a
  measured explanation of the observed effect size.
- **Keep assumptions, calibration, and validation distinct.** Literature may
  support a direction without supporting an exact interval or initial rate.
  Label modeler-selected values honestly. Call a value calibrated only when a
  calibration procedure and target exist, and do not treat the same target as
  independent validation. A threshold or assignment probability is not itself an
  observed or realized adoption rate.
- **Match the comparison population and definition.** Check geography, years,
  household group, denominators, and event or policy definitions. Do not compare
  a subgroup's modeled rate with an all-population reference without explaining
  the difference. A small signed error relative to absolute error can reflect
  cancellation and does not by itself establish accurate central tendency.
- **Keep model coverage claims narrow.** Adding an attribute does not mean the
  model captures every associated hazard, behavioral, institutional, or pricing
  relationship. Explain which calculations actually use the attribute and which
  correlations remain unrepresented.
- **Reconcile facts, not just wording.** Verify sample counts and analysis-specific
  exclusions against the source records. Do not force different effective sample
  sizes to match merely for consistency or describe an unverified correction as
  completed.
- **Read the effective revised text.** When inspecting Track Changes, distinguish
  retained and inserted text from deleted text. Do not concatenate both versions
  and diagnose the resulting duplication as current prose. Identify when an
  archived copy is used because the active file cannot be read.
- **Avoid unnecessary expansion.** Give summary points distinct functions, such
  as model changes, sensitivity evidence, documentation, and figure updates.
  Add no new experiment, figure, or manuscript paragraph solely to increase
  response length. A complete methodological correction may need no comparison
  figure, especially when the available comparison would confound other changes.

## Common Failure Modes

- Saying “clarified” without showing what changed.
- Reporting numbers without explaining their relevance to the concern.
- Giving limitations only after a surprising metric has already been framed as a
  failure.
- Restating the original text instead of revising it.
- Moving a challenged claim to the supplement without answering it.
- Tuning a parameter to a desired output without declaring the calibration target
  and independent evidence.
- Referring to a later response before the reader reaches it.
- Using an old analysis after the model baseline changed.
- Adding a figure that does not isolate the challenged factor.
- Adding a citation that does not support the claim.
- Saying the manuscript or Supporting Material changed when only the response
  changed.
- Rejecting a request without explaining why or offering a valid alternative.

## Final Checks

- [ ] Every reviewer comment and subquestion is recorded.
- [ ] Every response directly answers the current comment.
- [ ] Major changes state why they were made and whether the complete analysis
      was rerun.
- [ ] Major responses are at least as complete as the reviewer comments without
      padding or repetition.
- [ ] Every reported number has verified provenance and enough context to be
      interpreted.
- [ ] Every figure or table is current, cited in the response, and explained in
      the prose.
- [ ] Results are interpreted rather than merely listed.
- [ ] The response identifies what changed in the manuscript or explains why no
      change was made.
- [ ] Related comments cross-reference backward without omitting the current
      comment's distinct concern.
- [ ] Remaining limitations are specific and do not overclaim what the model now
      captures.
- [ ] Terminology, abbreviations, mathematical notation, tense, and response
      formatting are consistent.
- [ ] Final line numbers refer to the clean revised manuscript.
- [ ] New prose passes claim-evidence, claim-scope, terminology,
      forbidden-variant, repetition, stock-phrase, project-discouraged-phrase,
      and formatted-document checks.
