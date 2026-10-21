# Functional Prose and Citation Editing

## Contents

1. Functional transitions
2. Function-preserving concision
3. Natural scholarly prose
4. Gap statements and comparative framing
5. Claim–citation alignment
6. Observable stock or AI-like prose
7. Dash and hyphen style
8. Exact-candidate procedure

## Functional Transitions

Identify the relation that must carry the reader from one sentence or paragraph to the next: contrast, extension, qualification, cause, consequence, comparison, return to the study, or bridge to the next section. Express that relation through the subject and verb when possible. Use a transition word only when it makes the relation clearer.

Reject transitions that merely announce movement, such as an unexplained `Moreover`, `Taken together`, or `One line of work`. A transition is functional only when removing it would hide a real logical relation. Do not require every sentence to begin with a connector, and do not add a separate transition-only sentence when the relation can be carried by a content sentence.

Treat sentence-opening frames such as `Beyond X,` as cues for contextual review, not as default signals of progression. Retain them only when `X` names a boundary that the next clause genuinely extends. When the sentence merely adds another application or evidence type, name that content directly instead of announcing the move.

At paragraph boundaries, read the prior closing sentence, the revised paragraph's opening and closing sentences, and the next opening sentence as one sequence. Confirm that the revised paragraph performs its own function and does not prematurely perform the next paragraph's work. When a paragraph bridges to numbered questions or objectives, identify exactly which question each closing phrase prepares; do not rely on a generic gap sentence.

Apply the same relation test outside Results. A literature grouping must establish the specific comparison still missing; background must prepare the design choice that follows; a Discussion implication must remain tied to the reported finding; a limitation must name the inference affected by its constraint. These are examples of reader functions, not required section templates. If the relation is already explicit, preserve it. If the evidence is missing, expose the gap rather than inventing a bridge that sounds conclusive.

When a literature paragraph contains several examples, choose an evidence order that advances the argument instead of preserving the order in which sources were found. A useful default is broad field context, then more specific applications, then the precedent most directly comparable to the present study, and finally the unresolved gap. Use chronological, methodological, causal, or contrastive order instead when it better serves the paragraph's function; do not force broad-to-specific progression onto evidence that has another clear relation.

Group sources that perform the same evidentiary function in one sentence or clause when their claims can be represented accurately. Use `For example` to introduce a representative set when it clarifies the move from a broad claim to concrete evidence, but do not repeat example markers before every citation. Place the closest precedent immediately before the gap when it establishes the comparison boundary. As a diagnostic, temporarily remove the citations: the remaining prose should still read as a cumulative argument rather than a list of study summaries.

### Workflow handoff test

For passages explaining a process, inspect the complete requested unit and the available boundary sentences after repairing a local comment. Apply this test where order or dependencies matter; a conceptual comparison or literature synthesis need not be recast as a pipeline. Scale the reading to the change: a punctuation edit does not reopen an unrelated chapter, but a repaired paragraph opening can affect its neighboring handoff.

1. Identify each paragraph's reader function. Follow the information through the steps: what is available, what operation uses it, what is produced, and where that output is used next. A component inventory is insufficient when readers need a procedure.
2. Inspect every affected adjacent sentence pair. State what the second sentence adds and identify its link to the first in the prose itself. Resolve unclear actors, referents, prerequisites, or unexplained changes of subject. At each paragraph boundary, check whether the prior ending prepares the next opening; move a detail when its placement interrupts that link. Do not add a redundant bridge when the opening already supplies it.
3. Distinguish initial user configuration from actions repeated during execution. For example, selecting which variables a model receives is different from updating their values at each time step. Make the actor and frequency clear when confusing them would misdescribe the user workflow. If the source does not establish them, record that gap rather than inventing manual work, automation, or a schedule.
4. Preserve the actual branches. Distinguish a sequential step, an optional addition, a condition for proceeding, a diagnostic assessment, and an action that changes or stops execution. Do not turn a data dependency into simultaneous execution, a diagnostic into an automatic veto, or temporal order into causation. Establish these facts from the supplied method; an example cannot supply missing implementation evidence.
5. Select connectors by their supported relation. `Then` can mark a subsequent step; `once` or `after` can mark a prerequisite; `if` introduces a condition. Retain them when they help the reader. Avoid imposing a connector quota, mechanical synonym rotation, or a connector at every sentence opening.
6. Read the resulting passage at an ordinary researcher's pace and paraphrase the route using only the text. Check whether the intended disciplinary reader can identify the inputs, actions, outputs, and branch consequences without knowledge of the drafting discussion. Repair the smallest remaining obstruction and repeat the affected reading after the final wording change.

#### Worked example: daily forecasting

This is a hypothetical teaching example, not a claim about an actual package. Assume the source establishes that users select the input variables before a run; their values are updated daily; forecasting uses complete inputs; missing inputs stop that day's calculation; and an optional later comparison with observations records diagnostic results without changing the forecast.

**Before:** "At the start of each day, users define the inputs. The model calculates a forecast. An optional check compares it with observations. Missing inputs stop the calculation. Then the input values are updated."

**Findings:** The opening implies daily manual configuration. The daily values appear after the calculation that needs them. The missing-input condition arrives after the forecast, and the diagnostic's consequence is unstated. Adding `then` does not repair those errors.

**After:** "Users first select the input variables supplied to the forecasting model. Their values are updated each day. If required inputs are missing, that day's calculation stops; otherwise, the model uses the updated values to calculate a forecast. Once observations become available, an optional comparison records the difference between the forecast and observations without changing the forecast."

**Acceptance basis:** The revised route is configuration -> daily values -> forecast, with the missing-input condition before a completed calculation and the optional later diagnostic kept distinct from forecast generation. The change preserves the assumed source facts; it does not establish that a real implementation follows them. Preserve an already clear passage that expresses the same relations without these particular connectors.

## Function-Preserving Concision

Map each sentence to one or more required functions: claim, evidence, explanation, qualification, synthesis, or bridge. Remove or combine duplicated functions before deleting scientific content. Compress repeated examples, parallel literature inventories, and restated criteria while preserving the narrow claim, its evidence, inference limit, and bridge.

Use word counts, sentence counts, and comparison with neighboring paragraphs only as diagnostics. Do not impose a universal target. A shorter version is not better if it removes a required comparison level, citation, limitation, or transition.

For an accepted, submitted, or advisor-edited baseline, make the smallest repair that solves the actual issue and its dependencies. Preserve functioning original wording; do not rewrite neighboring sentences for stylistic uniformity alone. If a larger structural change is necessary, identify the displaced function and destination before editing. Comment labels identify changes made for a request, not every passage that shares its topic.

Inspect sentence rhythm after compression. Merge a very short sentence when it exists only to say `Overall`, `However`, or `The results are mixed`; retain a short sentence when it carries necessary emphasis or a complete substantive finding. Avoid solving density by creating a sequence of clipped sentences.

## Natural Scholarly Prose

Prefer concrete scholarly subjects, direct verbs, and terms recognizable to the intended disciplinary audience. Preserve one term per concept and avoid synonym rotation. Turn literature inventories into cumulative argument by making each sentence state what a study group examined and how it advances the paragraph.

Write for the intended journal's broad disciplinary readership, not only specialists in the narrow topic. Define or replace a nonessential umbrella label when readers must decode it before understanding the claim. For example, use a concrete description of disaster-related tasks instead of `disaster management cycle` when the stages of that cycle are not analytically important.

Maintain a clear sense of the reader. Write for the intended scholarly audience without assuming familiarity with the study's specific concepts, institutions, model logic, project labels, or data-processing choices. For interdisciplinary work, assume overlapping broad research knowledge rather than specialist knowledge of every component. Introduce necessary background and explain a term's role where the reader first needs it; spelling out an acronym alone does not supply that understanding. Plain language preserves scientific meaning and qualifications rather than making the prose casual.

Guide the reader by prerequisites, not only acronym definitions. Introduce relevant background or institutional rules before group differences, and introduce those differences before the model setting that uses them. Explain enough at each step for the next statement to be interpretable; avoid importing implementation details into background or implying that a real-world requirement is enforced by a model that lacks the needed attribute.

Check the reader's load as well as first definitions. Several correctly expanded acronyms can still obscure which entities or relationships a sentence compares. Keep essential registered terms; use their concrete role or a clear group name where repeated shorthand forces the reader to decode a list. Do not rename constructs, rotate synonyms, or expand every acronym again as a mechanical cure.

Prefer explicit actors, actions, and comparison references. Ask “higher than what?”, “which difference?”, “whose loss?”, and “what is the denominator?” when meaning is unclear. Replace a vague `this difference` or `these limits` with the specific result or constraint when needed, without repeating an entire definition. Plain scholarly language simplifies syntax and information order, not scientific distinctions.

Keep the main actor and action visible instead of burying them in a long noun stack or a sequence of qualifications. Introduce familiar information before new information when it helps the reader follow the relation. Reorder or divide an overloaded sentence when its meaning requires backtracking, but retain necessary technical terms, comparisons, and uncertainty. Do not impose a word-count ceiling or replace one dense sentence with disconnected fragments.

For example, `flood adaptation decision-making process` may be clearer as `flood adaptation decisions` when the sentence concerns choices, or `how households choose adaptation actions` when it concerns the process. Choose by meaning, not by a universal banned phrase list; do not erase a process-versus-outcome distinction merely to shorten the name.

### Plain Scholarly Language Across Fields

Aim for a scientifically literate reader from another field to understand the main claim without knowing the study's internal shorthand. This is an accessibility target, not a guarantee that every possible reader can follow specialized derivations without background knowledge. Preserve academic precision; simplify the route to the claim rather than replacing it with a vague or stronger assertion.

1. State the actor or unit, measured concept, and main relation through a visible subject and verb. Put the finding before dependent detail when it serves the paragraph's function, but not before a definition needed to understand it. Identify the comparator when reporting a difference; do not leave the reader to infer it from panel order or variable labels.
2. Supply the minimum prerequisite at the reading boundary where it is needed. Retain an essential technical term and briefly explain what it means or does in this study; an expanded acronym alone may not help. In a standalone passage, expand new acronyms and explain unfamiliar statistical labels when their meaning is needed to interpret the claim. For example, define species richness as the number of species observed when that is the measured quantity. Keep definitions in readable clauses rather than nested qualifications that hide the subject. Avoid replacing a defined construct with a looser everyday synonym or adding a textbook digression. State missing context instead of inventing a definition.
3. Keep the numerator, denominator, units, time, population, conditions, and uncertainty that determine the claim. A percentage-point difference is not a relative percent change; a normalized loss is not household welfare. Shorter wording fails if it removes those distinctions or changes the comparison.
4. Preserve the supported causal claim as well as its limits. Do not turn an observational association into an effect, a nonsignificant difference into equality, or a measured intermediate outcome into an unmeasured endpoint. Conversely, do not mechanically weaken an identified effect from a randomized design into mere association. Explain the result's meaning without adding evidence or an untested mechanism; name what cannot be concluded when that boundary is necessary to prevent a likely misreading.
5. After revision, perform a cold-read paraphrase without consulting hidden drafting history: who or what was studied, what was measured, what comparison or relationship was found, and what the passage permits or does not permit the reader to conclude. Locate the words that support each answer and check the repaired sentence's grammar. When the answer requires an unexplained term, referent, denominator, or logical jump, make the smallest repair and reread available adjacent sentences. Ask only for information needed to resolve the requested claim. Do not presume an intervention in a descriptive comparison or demand surrounding text solely to offer a local provisional edit; unavailable neighboring text limits a flow claim. Assess only the requested unit and affected dependencies.

Keep this check separate from sentence length or readability scores. An independent reader-style assessment can identify a remaining comprehension problem, but a model's fluent paraphrase is not proof of comprehension by actual readers across all fields. In tests, compare exact source facts and revisions as well as the takeaway; do not reward shorter wording that changes scientific meaning.

For an explicit independent review or repeated reader-access failures, use
[independent-reader-review.md](independent-reader-review.md) to distinguish what
is known at first use from a definition supplied later. Its cold-reader findings
complement these local prose checks; they do not impose extra agents on every edit.

### Unpack Noun Chains by Meaning

During drafting and scoped prose review, flag noun phrases that pack several modifiers around a central concept and make the reader guess their relationships. Four or five stacked nouns are a strong review cue, not a universal word-count limit; a shorter phrase can also be ambiguous. Apply the same check to affected headings, captions, and table labels without expanding a local edit into a whole-document audit.

1. Identify the central concept and the intended relations: whose, what responds to what, what is measured, what is covered, or what an action is for. Use the supplied context or definition; if the relation is unresolved, ask a focused question or offer explicitly conditional alternatives rather than silently choosing one.
2. Make those relations explicit with a possessive, an appropriate preposition, or a clause with a subject and verb. For example, use `responses to a policy`, `coverage for contents`, or `the wellness of households` when that is the intended meaning. Do not mechanically insert `of`, `for`, or `to`; `wellness to ...` is not a general repair pattern.
3. Preserve established technical terms, proper names, registered constructs, and clear conventional compounds. Do not interchange wellness, well-being, welfare, and willingness or change a willingness measure into observed behavior. Keep qualifications, comparison groups, units, time, and uncertainty. Adding hyphens or rotating synonyms does not clarify a hidden relation.
4. Re-read the complete sentence and its local context. Confirm that the reader can identify the concept and relationship without backtracking, and that the repair did not add causation, change the measure, or create another dense phrase.

Apply this meaning test to short comparison labels too. In running prose, `group mean differences` is incomplete when the reader cannot identify which groups or which quantity is compared. Name the people or data sources, the measured concept, and the comparator, then express the relation with a subject and verb. Preserve a clear statistical term or table heading when its groups and quantity are already explicit at that reading boundary; an author's rejection of a phrase in one paper is not a universal ban on comparisons of means.

Do not treat a possessive as a sufficient repair. `Human respondents' insurance willingness` can still hide what respondents are willing to do. Prefer `human respondents reported willingness to buy insurance` or `willingness to buy insurance among human respondents` when those relations are supported. If the finding is comparative, retain who is compared with whom; do not drop the comparator while simplifying the actor. Before accepting a repair, compare direction, magnitude, statistical significance, equivalence, and causal strength with the source. Keep a nonsignificant difference distinct from equal means, and stated willingness distinct from actual purchases.

Use these hypothetical repairs only when the stated meaning is confirmed:

- `renter flood insurance purchase willingness` → `renters' willingness to buy flood insurance`, when the construct is willingness rather than enrollment.
- `human insurance policy responses` → `people's responses to insurance policies`, when the policies are what people respond to, not who collects their responses.
- `insured household wellness scores` → `wellness scores for insured households`, when wellness is the study's defined construct and insured households are the scored population.

### Other Local Prose Checks

Use tense according to function: completed procedures and observations often use past tense, while figure descriptions and current interpretations can use present tense. Keep comparable clauses consistent where appropriate, but do not force Abstract, Results, and Conclusion into one tense. Repair grammar errors even in advisor-edited text with the smallest meaning-preserving change; preserving the baseline does not certify an error as correct.

Prefer a literal verb when an idiomatic academic verb adds no meaning. If `draw on data` only means `use data`, write `use data`; retain `draw on` only when it conveys a broader intellectual or evidentiary dependence that `use` would lose. Apply the same test to other polished-sounding phrases rather than rotating them mechanically.

Read for cadence as well as grammar. Flag repeated sentence shapes, excessive parallel lists, long noun stacks, vague agents such as `researchers` or `studies` when the field or evidence source is clearer, and repeated demonstrative openings such as `This`, `These`, or `Such`. Revise only when the change improves meaning, flow, or evidence linkage.

### Sentence-pattern variety without changing logic

Separate a stable argument order from repeated grammatical scaffolding. A passage may correctly move from finding to evidence to explanation while unnecessarily repeating the same sentence shape. Review sentence-opening families, not only identical strings: `We first ... / We then ... / We next ...`, `These results show ... / These findings indicate ...`, or repeated `By ... , we ...` clauses can sound repetitive even when their verbs differ.

For paragraph work, inspect the whole paragraph and its available neighbors. For subsection or section work, also read paragraph openings and endings in sequence for recurrent scaffolding. A one-sentence grammar correction does not authorize rewriting adjacent paragraphs for variety. The deterministic scan flags three adjacent procedural `We` frames within a paragraph as a review cue; it does not parse every sentence structure, establish a universal quota, or certify broader stylistic variety.

Preserve the actual sequence, dependencies, technical terms, actors, and comparison. Where useful, combine dependent steps, make the relevant data or result the subject, or remove a sequencing word that adds no information. Do not simply rotate `then` into `next`, change every sentence to passive voice, or replace a defined technical term to evade repetition. Retain deliberate parallelism for matched comparisons and procedural sequences when it helps the reader; record the reason rather than treating a diagnostic as an automatic error.

For example, this hypothetical wording can be repaired without changing the procedure:

- Before: `We first fit the income distributions. We then sample incomes from these distributions. We next calculate losses relative to income.`
- Minimal repair: `We fit the income distributions and sample incomes from them. The sampled incomes are then used to calculate losses relative to income.`

Use sentence-opening `Beyond X,` and `Taken together,` sparingly, not as default bridges or summaries. Prefer naming the added evidence, actual boundary, or combined finding directly. Retain `Beyond X,` when it identifies a genuine extension and `Taken together,` when the sentence actually synthesizes distinct evidence. Do not replace them mechanically with another stock connector. Literal wording such as `floodwater extended beyond the boundary` is not a stock transition. Both openings receive contextual diagnostics; project-specific stronger preferences remain in the prose profile.

After drafting, read the exact passage aloud or simulate how a researcher would naturally say it. The test is not whether the prose sounds conversational. It is whether the sentence can be spoken at an ordinary pace, whether its subject and action remain clear, and whether the listener can follow the information in the order presented. Rewrite passages that sound assembled, require backtracking, or contain wording a researcher would be unlikely to say.

## Gap Statements and Comparative Framing

Treat the main task verb as part of the scientific claim. Use verbs such as `compare`, `characterize`, `estimate`, `predict`, `validate`, `reproduce`, `replicate`, or `evaluate` only when they match the study's actual inferential aim and analysis. Do not turn a descriptive comparison into a capability, validation, equivalence, or pass/fail claim merely because a stronger verb sounds more consequential. When the study asks how two evidence sources differ or align, state the comparison directly instead of implying that one source is expected to recreate the other.

Write a gap as a specific missing piece of knowledge, evidence, comparison, mechanism, population, scale, or analytical level. Treat phrases such as `remains unclear`, `is not well understood`, or `little is known` as incomplete unless the sentence or adjacent context names exactly what has not been examined. Prefer a concrete literature-state statement when support allows it, such as `has not been examined`, `has rarely been compared`, or `remains largely unexamined`, while avoiding absolute novelty claims that the search basis cannot support.

Avoid packing the study object, outcome, comparison source, population, scale, and analytical level into one long noun stack. Put the main comparison or unknown in the subject–verb core, then add overall, subgroup, temporal, spatial, or methodological scope in a separate phrase or sentence when needed. A reader should be able to identify what is missing before reaching the end of the sentence.

State why the gap matters at the level justified by the paper: interpretation, theory, method choice, policy inference, program design, decision support, transferability, or another substantive consequence. The stake may appear in the same sentence or the next one; do not force it into every gap sentence. Avoid generic importance claims when the manuscript can name the concrete decision or inference that depends on the missing evidence.

When a close precedent overlaps strongly with the present study, use it to define the boundary rather than treating it as a threat to novelty. State what that study actually compared or established, then identify the different analytical level, outcome, structure, population, or inference that remains open. Do not claim that `no study` has performed a broad class of comparison when prior work has already covered a narrower version of it.

## Claim–Citation Alignment

Split each sentence into its independently checkable claims. For every claim, identify the citation or manuscript evidence that supports it. A citation group at the end of a sentence must support every material clause it appears to cover; otherwise split the sentence, narrow the claim, or move the citations.

For grouped literature, verify that each cited source fits the named field, method, outcome, or limitation. Do not retain a citation merely because it appeared in an earlier draft. When a claim is compressed, recheck whether the surviving citation group still supports the new synthesis. When a citation is removed from a passage, confirm whether it remains cited elsewhere before changing the reference list.

Do not certify claim–citation support from titles or memory when the claim depends on details of the source. Read the primary source, abstract, or authoritative record at the level needed for the claim. Distinguish verified support from plausible topical relevance.

When cited studies report a relationship in a direction that differs from the corresponding relationship calibrated or estimated for the present sample or study area, do not append the citations as an unexplained contradiction. State the scope difference before or with the citations: the relationship reported here reflects the current sample or location, whereas the relationship may differ in other populations, locations, or settings when the cited evidence supports that qualification. Keep this disclaimer brief and evidence-backed. Do not recast a calibrated relationship as a model assumption, imply that opposing evidence automatically invalidates the study result, or invent contextual variation that the sources do not support. If the difference cannot be reconciled from the available evidence, state the unresolved contrast and reserve its interpretation for the Discussion.

## Observable Stock or AI-Like Prose

Never infer AI authorship from writing style. Report observable features only: empty metadiscourse, stock transitions, generic synthesis, repeated deictic openings, excessive preview-and-summary language, symmetrical but content-light category lists, repeated cadence, vague subjects, or unsupported claims of consensus.

Assess combinations and local density rather than banning isolated phrases. A common phrase may be natural once but formulaic when several appear in sequence. Replace it only with wording that states the actual relation or evidence more precisely.

Treat diagnostics for forms such as sentence-opening `Beyond X,` and `draw on` as prompts for reader-accessibility review, not proof that the wording is wrong. Check whether a reader can state the sentence's concrete claim without first translating a transition template, field label, or indirect verb.

## Dash and Hyphen Style

Separate three cases before editing:

1. syntactic em or en dashes used as punctuation;
2. lexical hyphens in compound modifiers, technical terms, ranges, or names; and
3. suspended compounds such as `subgroup- and topic-specific`.

Do not impose a universal ban. Retain a compound when the hyphen prevents ambiguity, follows an established term or proper name, or is required by the venue's language convention. Prefer an open compound when the field normally treats it as a noun phrase and no ambiguity results. Rewrite suspended compounds and clusters of several nontechnical hyphenated modifiers when a natural phrase is clearer.

Do not add a hyphen solely because an established open compound precedes another noun. Determine the compound's grammatical role and verify its conventional form; for example, retain `disaster management` in `disaster management phases` rather than automatically writing `disaster-management phases`. When the project or venue establishes an open form, register it in `style_profile.preferred_open_compounds` so the exact-candidate audit can report a hyphenated variant.

Review dash density at the sentence and paragraph level. A technically correct dash can still be distracting when several occur close together. Check that a dash is not masking an overloaded sentence that should instead be reordered or divided.

## Exact-Candidate Procedure

After the last wording change:

1. freeze the exact candidate and record its hash when supported;
2. rerun the applicable audits above on that exact text, at the requested depth and change impact;
3. read the previous and next paragraph with it;
4. inspect every deterministic diagnostic in context and record why any flagged form is retained;
5. reconcile added, removed, and claim-affected citations with the reference list; check retained support for substantive review without re-certifying untouched sources in a grammar-only edit;
6. perform the intended-reader and read-aloud checks on the exact candidate; and
7. invalidate the audit if any word, citation, or punctuation mark changes afterward.

Do not call a passage final, polished, natural, concise, or citation-checked when only an earlier candidate passed.
