# Functional Prose and Citation Editing

## Contents

1. Functional transitions
2. Function-preserving concision
3. Natural scholarly prose
4. Claim–citation alignment
5. Observable stock or AI-like prose
6. Dash and hyphen style
7. Exact-candidate procedure

## Functional Transitions

Identify the relation that must carry the reader from one sentence or paragraph to the next: contrast, extension, qualification, cause, consequence, comparison, return to the study, or bridge to the next section. Express that relation through the subject and verb when possible. Use a transition word only when it makes the relation clearer.

Reject transitions that merely announce movement, such as an unexplained `Moreover`, `Taken together`, or `One line of work`. A transition is functional only when removing it would hide a real logical relation. Do not require every sentence to begin with a connector, and do not add a separate transition-only sentence when the relation can be carried by a content sentence.

At paragraph boundaries, read the prior closing sentence, the revised paragraph's opening and closing sentences, and the next opening sentence as one sequence. Confirm that the revised paragraph performs its own function and does not prematurely perform the next paragraph's work. When a paragraph bridges to numbered questions or objectives, identify exactly which question each closing phrase prepares; do not rely on a generic gap sentence.

When a literature paragraph contains several examples, choose an evidence order that advances the argument instead of preserving the order in which sources were found. A useful default is broad field context, then more specific applications, then the precedent most directly comparable to the present study, and finally the unresolved gap. Use chronological, methodological, causal, or contrastive order instead when it better serves the paragraph's function; do not force broad-to-specific progression onto evidence that has another clear relation.

Group sources that perform the same evidentiary function in one sentence or clause when their claims can be represented accurately. Use `For example` to introduce a representative set when it clarifies the move from a broad claim to concrete evidence, but do not repeat example markers before every citation. Place the closest precedent immediately before the gap when it establishes the comparison boundary. As a diagnostic, temporarily remove the citations: the remaining prose should still read as a cumulative argument rather than a list of study summaries.

## Function-Preserving Concision

Map each sentence to one or more required functions: claim, evidence, explanation, qualification, synthesis, or bridge. Remove or combine duplicated functions before deleting scientific content. Compress repeated examples, parallel literature inventories, and restated criteria while preserving the narrow claim, its evidence, inference limit, and bridge.

Use word counts, sentence counts, and comparison with neighboring paragraphs only as diagnostics. Do not impose a universal target. A shorter version is not better if it removes a required comparison level, citation, limitation, or transition.

Inspect sentence rhythm after compression. Merge a very short sentence when it exists only to say `Overall`, `However`, or `The results are mixed`; retain a short sentence when it carries necessary emphasis or a complete substantive finding. Avoid solving density by creating a sequence of clipped sentences.

## Natural Scholarly Prose

Prefer concrete scholarly subjects, direct verbs, and terms recognizable to the intended disciplinary audience. Preserve one term per concept and avoid synonym rotation. Turn literature inventories into cumulative argument by making each sentence state what a study group examined and how it advances the paragraph.

Read for cadence as well as grammar. Flag repeated sentence shapes, excessive parallel lists, long noun stacks, vague agents such as `researchers` or `studies` when the field or evidence source is clearer, and repeated demonstrative openings such as `This`, `These`, or `Such`. Revise only when the change improves meaning, flow, or evidence linkage.

## Claim–Citation Alignment

Split each sentence into its independently checkable claims. For every claim, identify the citation or manuscript evidence that supports it. A citation group at the end of a sentence must support every material clause it appears to cover; otherwise split the sentence, narrow the claim, or move the citations.

For grouped literature, verify that each cited source fits the named field, method, outcome, or limitation. Do not retain a citation merely because it appeared in an earlier draft. When a claim is compressed, recheck whether the surviving citation group still supports the new synthesis. When a citation is removed from a passage, confirm whether it remains cited elsewhere before changing the reference list.

Do not certify claim–citation support from titles or memory when the claim depends on details of the source. Read the primary source, abstract, or authoritative record at the level needed for the claim. Distinguish verified support from plausible topical relevance.

## Observable Stock or AI-Like Prose

Never infer AI authorship from writing style. Report observable features only: empty metadiscourse, stock transitions, generic synthesis, repeated deictic openings, excessive preview-and-summary language, symmetrical but content-light category lists, repeated cadence, vague subjects, or unsupported claims of consensus.

Assess combinations and local density rather than banning isolated phrases. A common phrase may be natural once but formulaic when several appear in sequence. Replace it only with wording that states the actual relation or evidence more precisely.

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
2. rerun all six audits above on that exact text;
3. read the previous and next paragraph with it;
4. inspect every deterministic diagnostic in context and record why any flagged form is retained;
5. reconcile retained and removed citations with the reference list; and
6. invalidate the audit if any word, citation, or punctuation mark changes afterward.

Do not call a passage final, polished, natural, concise, or citation-checked when only an earlier candidate passed.
