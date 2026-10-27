# Context-Rich Evidence and Repair Cases

Use only the matching case when a substantive review, an uncertain repair, or an
explicit regression exercise needs it. Existing section guides remain authoritative;
these examples operationalize their decisions, not a new universal checklist.
They are reconstructed teaching passages from an author-supplied failure report,
not quotations or verified findings from the private manuscript. Numbers below
belong to stated hypothetical contexts. Never copy them into another study.

For a regression case retain: original passage, necessary neighbors/source facts,
the expected obstruction or no-change outcome, an acceptable repair, protected
meaning, and a tempting but invalid repair. Check both false negatives and false
positives. Shape/link tests establish fixture integrity; exact-candidate dependency
tests establish provenance coverage; independent AI outputs are bounded behavior
evidence. None alone certifies scientific or editorial quality.

## 1. Continuity requires a relation, not a connector

**Context:** a paragraph explains which beliefs a survey measures; its last
sentence says only, “Participants were recruited online. CFA was performed.”
The surrounding section has not introduced CFA or its role.
**Problem:** recruitment and measurement assessment arrive without a reader route.
**Minimal repair:** place recruitment with sampling; introduce confirmatory factor
analysis as assessing whether the retained items represent the intended constructs,
where that assessment is needed. Keep the source's actual procedure.
**Reject:** adding “Furthermore” or a repeated “These results indicate” without
restoring the relation. A short SM pointer need not be removed when it supports,
rather than interrupts, the paragraph's closing function.
**Boundary:** inspect available sentence pairs and paragraph boundaries; missing
neighbors limit the check, not proof of a manuscript omission.

## 2. Name the comparison and its level

**Context:** the author compares a human sample, then generated responses against
that fixed human reference, then subgroup differences. The sentence says,
“The groups showed partial similarity in pathways.”
**Problem:** neither the compared entities, level, nor similar component is clear.
**Minimal repair:** name the source pair, population/subgroup, measured relation,
and supported direction from the available evidence. If these facts are missing,
ask for them rather than completing a plausible claim.
**Reject:** “The model reproduces human decisions” or ranking models as better
when the design supports only specified comparisons.
**Boundary:** that analytical order and the study's nonclaims are project choices,
not a mandatory human-first sequence for unrelated research.

## 3. Retained items constrain the construct's meaning

**Context:** both sources answered the same original questionnaire, but the human
coping-perception score retained only beliefs about a measure's effectiveness and
cost; self-efficacy items were removed.
**Problem:** “Higher scores show confidence in one's own ability to act” imports
meaning absent from the retained items.
**Minimal repair:** interpret the retained score through effectiveness/cost beliefs,
with the actual direction and scoring confirmed from the instrument.
**Reject:** declaring that the sources answered different questionnaires; treating
shared original wording as proof of equivalent retained measurement.
**Boundary:** item selection may narrow construct comparability without making
every structural-model result uninterpretable. See the study-design adapter.

## 4. Reconcile statistical provenance before alleging inconsistency

**Context:** one table reports a selected run, another a median across runs; bands
describe between-run variability, not variation among households. A path's
within-group significance is not a test of the difference between sources.
**Minimal repair:** label the unit, selection/summary, interval, and tested contrast
at the point needed. Preserve nonsignificance as lack of detected difference,
not equality.

**No-change control:** two correctly labeled tables use the same raw tests but
Holm families of 12 and 18 comparisons. Adjusted p-values differ while every
reported decision at the stated threshold agrees. That is not by itself a wrong
number or changed substantive finding.
**Count control:** 17 diagnostic events across 9 runs is compatible with 9 affected
runs. Trace what was counted before forcing the values to match.
**Boundary:** these explanations require actual provenance. Without it, report
unverified rather than inventing a correction or assuming the tables are valid.

## 5. An extension does not reveal an untested mechanism

**Context:** generated response patterns change when a profile changes; the human
reference and original human responses remain fixed.
**Minimal interpretation:** input conditions affect how those generated responses
compare with the fixed reference.
**Reject:** claiming the experiment measured how humans react to new information,
or that a model internally relies on a regional cue without testing that account.
Literature may motivate a possible explanation, not prove it in this experiment.
**Boundary:** separate observation, supported interpretation, possible mechanism,
and application. Do not ban literature-based Discussion or a result-led opening;
organize citations around the paragraph's argument.

## 6. State the inference boundary, not a confession or to-do list

**Context:** a one-region study has uncertain construct comparability after item
selection. Structural paths are reported with that measurement boundary.
**Minimal interpretation:** identify the scope/measurement constraint and the
particular transfer or construct comparison it limits.
**Reject:** “The study is flawed”; “CFA concerns invalidate all SEM comparisons”;
or a list of absent tests with no affected claim. Equally reject hiding a necessary
correction merely to avoid reviewer questions.
**Boundary:** remedies/future work belong only where requested. Existing limitations
guidance separates constraints from correctable defects; do not duplicate it.

## 7. Compression must retain the study's answers

**Context:** Results distinguish overall source comparisons and subgroup-specific
directions; neither equivalence nor causation was established.
**Problem:** “The sources were similar” discards which relation, direction, and
subgroup qualification mattered.
**Minimal repair:** preserve those answer-bearing relations in the Abstract and
Conclusion while giving each summary its own function.
**Reject:** a shorter fluent summary that changes association to causation,
nonsignificance to sameness, or comparative evidence to validated reproduction.
**Boundary:** explain a study-specific “decision-making pathway” enough for its
current use; do not replace it with unexplained “pathways” or ban all longer
technical names. No fixed sentence/paragraph count follows.

## 8. Supporting Material has reader and reproducibility functions

**Context:** two supplementary tables duplicate the same main comparison, while
one also carries the only analysis settings needed to reproduce it.
**Minimal repair:** explain each item's purpose; combine genuinely redundant
entries, move compact reading information to notes, and preserve indispensable
settings in an appropriate accessible location.
**Reject:** deleting needed settings to reduce table count, or adding a second
results narrative to every caption/note.
**Boundary:** after a split/merge, reconcile active body callouts, SM contents,
captions/notes and response locators by function, not blind number replacement.
Ascending first-call order is an author/venue convention when required, not a
universal test. Route Word operations and visual inspection to the document skill.

## 9. Completion requires the right evidence for each subquestion

**Context:** a comment asks for an explanation and a sensitivity test. A reply
exists, but the test is only planned. A DOI resolves, but claim-level support has
not been read. A rendered image exists, but its pages were not inspected.
**Minimal status:** retain the separate completed, pending, inapplicable-with-reason,
or unverified subquestions; do not report the whole comment resolved.
**Reject:** deleting the full thread because one issue is obsolete, certifying
support from DOI identity, or certifying layout because rendering succeeded.
**Boundary:** professor-review copies and anonymous submission copies are different
deliverables. Bind checks to the exact candidate and affected dependencies; a
later relevant change invalidates earlier acceptance. Required unavailable checks
stay incomplete. A grammar-only edit does not trigger this full package review.

## 10. Layered explanation without extra prose rituals

These invented examples illustrate the Results and functional-transition guides;
they are not quotations, validated findings, or vocabulary to copy into a paper.
The regression prompts are in `evals/layered_continuity_cases.json` at the
repository root. Preserve source facts and assess the actual reader relation,
not a keyword count.

**Result unit:** two neighborhood groups score 3.6 and 3.8 on a five-point
confidence scale with neutral midpoint 3; their interquartile ranges are 1.2 and
0.6. A list ending only with “These results are important” leaves the reader to
decode both level and spread. A minimal repair is: “Both groups report confidence
above the neutral midpoint (3.6 and 3.8 versus 3). Their responses differ more in
spread: the interquartile range is 1.2 in the first group and 0.6 in the second.”
This interprets the supplied scale and names the next comparison without adding
a causal explanation or a claim of practical importance. Keep a clear original
multi-number comparison; do not attach a separate so-what sentence to every value.

**Change of analytical level:** a relationship is statistically detectable in one
group but not another. That does not test whether the groups differ. State the
individual findings, then request the relevant group/model comparison if the
intended conclusion requires it. Do not manufacture that test or remove an
important nonsignificant result. Even a shared response scale does not rank
different constructs by influence or importance.

**Beyond Results:** “Prior studies examine adoption counts. We compare the reasons
people give for adoption” leaves the gap implicit. If the supplied literature
supports it, name the unexamined reasons, then explain how the present comparison
addresses that gap. Similarly, connect a regional data boundary to the inference
outside that region, not to an unsupported declaration that the whole study is
unreliable. A bridge names the relation; “therefore” alone supplies no evidence.

**No-change controls:** retain a coherent finding with several supporting values,
a timely and correctly bounded interpretation, and a later display introduced by
only its genuinely new comparison. Descriptive cross-construct values may remain
when the reader knows their scoring meanings and no unsupported ranking is made.
For a single-sentence repair, inspect available neighbors only; missing context
limits the flow verdict, not permission to invent or replan a whole section.

## 11. Comparison contribution is not a sequence label

**Context:** an invented study compares respondent and generated responses using
the same administered questionnaire. Its measurement section compares retained
question sets and model fit; later sections compare scores and relationships.
**Failure:** reporting retained counts and fit indices, then ending with "the
first level answers RQ2," leaves the contribution unexplained even if every
sentence pair sounds connected. Counts concern measurement inputs; fit concerns
how closely the measurement model describes response patterns. Neither alone
establishes common construct meaning or an internal decision mechanism.
**Minimal repair:** explain the particular measurement contrast supported by the
facts and why the later score/relationship comparison needs that context. Keep
the evidence and supported meaning adjacent, without an intervening technical
table inventory. A correct concise pointer may remain; it is not inherently a jump.
**Reject:** changing "different retained questions" into different questionnaires
administered; ranking quality by counts; or saying poorer fit forbids all later
structural comparisons. Do not invent formal invariance or missing item wording.
**No-change control:** a paragraph already explains that different retained sets
give scores different inputs and prepares the score comparison. Keep it without
adding "first level," an RQ label, or another conclusion sentence.
**Transfer boundary:** species coverage can likewise contextualize a later
ecological comparison, but does not require a CFA-first sequence or establish
accuracy without ground truth. The point is a recoverable contribution, not one
paper's analysis order. Synthetic prompts and counterexamples are in
`evals/comparison_layer_cases.json`; assess actual prose, not keyword presence.

## 12. Research identity before sentence compression

**Context:** a hypothetical cold-chain study asks when low-cost temperature
sensors can support delivery monitoring. Two sensor types are evaluated against
a calibrated reference. Overall work compares bias, variability and calibration
stability; warm/cold-condition comparisons cover bias and variability only.
The Conclusion's first paragraph identifies the study; the next reports findings.
**Failure:** “We sampled forty deliveries in one city. We compared differences
between warm and cold conditions between sensors” foregrounds data collection,
leaves the reference and dimensions unclear, and obscures the scientific goal.
Simply replacing it with “This study compared sensors at several levels” remains
too vague. Extending calibration-stability assessment to subgroups invents work.
**Minimal repair:** retain a clear purpose sentence; explain the observation/
reference comparison and distinguish overall from condition-specific dimensions
in connected prose. Keep the city as the data boundary, not a substitute purpose.
**Reject:** a plausible but invented safety benefit, causal or population claim,
or moving result interpretation into the study-identity paragraph contrary to
the author's plan. A polished list of steps is not a recoverable argument.

**No-change and scope controls:** keep an opening that already connects a tree-
cover question to observational temperature records and its stated comparisons.
Fixing only one agreement error does not require reconstructing the whole study.
A conceptual paper may develop two propositions without a field site; a
qualitative paper may organize its work without numbered SQs. Neither needs a
three-question empirical template. When the Introduction/aim is unavailable,
state that limit rather than promote a supplied method into an inferred goal.
**Transfer boundary:** distinguish the role of a recruited sample from a shared
scenario supplied to another source; correcting one must not erase the goal or
imply that all participants inhabit that scenario. These are role distinctions,
not one paper's locations, sample counts or mandatory paragraph structure.
Seven public hypothetical requests are in `evals/research_identity_cases.json`;
the private application and actual paired proposals remain task-local. Judge
their complete prose against source facts, preservation and reader progression;
fixture/link checks do not certify comprehension or first-handoff compliance.

## 13. A rewrite is not concern closure

**Context:** an invented qualitative study compares how rural and urban care
teams repair missing referral information. The advisor asks why those groups
are compared and how the sample sentence follows the literature gap.
**Failure:** changing “The teams differ” to “We compare rural and urban teams,
classified by clinic location” names the groups and basis but does not supply
the reason for the comparison. “We then interviewed twelve teams” adds order,
not the missing relation. A no-findings language scan and a preserved document
are different checks; neither answers the advisor's question.
**Minimal action:** in the existing ledger, locate the original selection and
full concern, then test the current passage against what the reader needs to
understand. If the rationale is not supplied, retain an open/partial assessment
and request the missing basis rather than inventing why rural teams differ.
Record an answered part separately from an unanswered part of the same comment.
**No-change controls:** a revised sentence may already name the response sources,
the procedure behind a quality claim, or the direction of an association. Keep
it when that answers the specific concern; do not demand a full Methods account
in a short summary. A reasoned non-change can close the concern without a rewrite.
**Different comparisons:** a null test of overall relationships between groups
does not establish a null difference in a single outcome, nor contradict a
comparison between two data sources. Identify the actual quantity, population,
level and test before deciding whether the prose links them adequately.
**Transfer boundary:** these decisions apply to conceptual arguments, field
studies and experiments as well as surveys. They do not require a fixed
“because” sentence, subgroup method, analysis order or author-template wording.
Missing source access limits the particular claim it prevents checking; it is
not automatic evidence that every visible correction is unverifiable. The
original range, current answer and closure reason belong in the same existing
comment record. Public hypothetical controls are in
`evals/comment_concern_cases.json`; real document text remains task-local.
