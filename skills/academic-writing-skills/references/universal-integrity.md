# Universal Manuscript Integrity

## Contents

1. Argument and paragraph function
2. Evidence and claim scope
3. Abstract and Conclusion
4. Terminology, repetition, and flow
5. Numbers, citations, and visuals
6. Exact-candidate gate
7. Four-pass review

## Argument and Paragraph Function

Map purpose or gap → question or objective → method → evidence → result → interpretation → limitation → contribution. Flag missing, contradictory, or orphan links.

Make a paragraph's topic and purpose clear in its opening sentences, usually before detailed evidence. Read those openings in sequence; they should form a coherent section outline. Use one primary function per paragraph unless a concise transition genuinely requires two.

Keep the opening, development, and ending aligned with that function. The ending should complete the point established by the evidence or prepare a specific next step, not merely repeat the opening. It need not be a separate summary or transition sentence. Treat this as a reader-comprehension test, not a fixed sentence position or paragraph template.

Before drafting, define the paragraph's function, claim, evidence, development, and bridge. After drafting, verify that every sentence serves that contract. Read the preceding and following paragraphs before accepting a local rewrite.

In Results, state the finding before or with the figure or table callout. Report evidence needed to support it, then give the substantive answer at the paragraph or subsection boundary where it belongs. Do not append an empty synthesis after every result or close only with another inventory of statistics, themes, paths, or cases.

Test the “so what” by asking what the evidence establishes about the question: an effect, contrast, trade-off, boundary, or supported explanation. Removing an SQ/RQ label should not remove the answer. Do not make a descriptive plot carry a causal conclusion or force every visual to demonstrate the full feedback loop.

Keep reproducible procedures in Methods. Results may contain findings and explanations directly supported by the analysis; reserve extended, literature-based, or untested mechanism interpretations and implications for Discussion. Adapt these boundaries when the genre explicitly integrates the sections.

## Evidence and Claim Scope

Distinguish:

- presence from absence
- direction from magnitude
- uncertainty from statistical significance
- statistical significance from practical importance
- failure to reject from evidence of equivalence
- correlation or prediction from causation
- model fit from mechanism validity
- component-level similarity from overall reproduction
- simulated behavior from real-world behavior

Require a denominator, comparison set, population, time, place, and condition where they affect meaning. Use validation, equivalence, noninferiority, or agreement only when explicit criteria and analyses support them.

Place unsupported explanations in Discussion as possible interpretations or remove them. Never add a mechanism solely because a reviewer requests “why.”

For model-based explanation, separate four levels: a verified model rule, an observed output, an explanation tested or directly supported by the analysis, and a plausible but untested mechanism. A rule describes what the model allows; it does not by itself prove why an aggregate trend occurred. Qualify an untested explanation and identify the diagnostic needed instead of turning model logic into causal evidence. Likewise, introducing real-world policy as background does not establish that the model implements or enforces it.

In a Limitations section, name the specific data, design, measurement, model, or validation constraint first. Then, where needed, explain how that constraint limits inference or use of the results. Do not frame the section around a generic warning to interpret results cautiously or treat a finding itself as a methodological limitation.

Do not soften or conceal a limitation merely to preserve a preferred conclusion. Future work can follow the inference boundary, but cannot substitute for stating it.

## Abstract and Conclusion

Build the Abstract from the current evidence map:

1. importance or problem
2. unresolved gap
3. objective or question
4. minimum interpretable design
5. distinguishable findings in question or analytical order
6. contribution, implication, or use boundary

Give every main question a substantive answer. Preserve enough named relations, group contrasts, directions, and qualifications to make the answer intelligible without internal codes or figures. Treat the word limit as a ceiling, not a reason to erase essential meaning.

Identify the method and what it does, who or what is studied, and the time, place, dataset, or analytical scope necessary to interpret the answer. Apply a word limit only when it comes from the active venue or author contract. Use [conclusion-and-abstract.md](conclusion-and-abstract.md) for flexible information functions, direct Conclusion openings, and compression checks; do not convert that sequence into fixed sentence counts or unsupported testbed/optimization claims.

Build the Conclusion around:

1. what the study did
2. synthesized answers in analytical order
3. meaning, contribution, and use boundary

Do not add new evidence or copy the Abstract. Preserve the study's actual task verb and inference level.

## Terminology, Repetition, and Flow

Use the entity that produced or contains the evidence. Do not interchange participant, response, dataset, model, simulation, or estimate.

Use one stable term per concept. Allow contextual variants only when the terminology registry identifies them. Resolve vague referents locally.

For a material metric, retain its definition, numerator, denominator, units, comparison, and aggregation/interpretation boundary in the project record or existing Methods/notes. The same percent symbol does not make differently normalized metrics equivalent. Distinguish a difference between percentages (percentage points) from a relative percentage change. Do not call a separately ranked curve difference an event-matched payout without that evidence.

Define abbreviations at the relevant reading boundary, subject to venue and author conventions. An independently read abstract or SM may need its own first definition; a caption may need a self-contained explanation. Do not automatically redefine every abbreviation in every caption or assume definitions in the main text make all companion artifacts intelligible. Definition is not enough when the reader also needs institutional context or the metric's purpose.

Do not rotate technical terms merely for variety. Separate four cases:

1. required repetition of a defined construct, model, population, or outcome
2. useful repetition that preserves a section's subject or comparison
3. avoidable repetition of a nontechnical word, phrase, sentence opening, or paragraph function
4. exact or near-duplicate prose that adds no new evidence or reasoning

For prose that feels formulaic or AI-like, report only observable features: generic metadiscourse, empty intensifiers, stock transitions, vague subjects, repetitive cadence, excessive preview-and-summary sentences, symmetrical but content-light lists, or unsupported synthesis. Never infer or allege AI authorship from these features. Replace a flagged pattern only when the revision improves precision, evidence linkage, or information flow.

Test flow at three levels:

- **sentence:** place familiar information before new information when it helps comprehension; keep the grammatical subject aligned with the entity being discussed
- **paragraph:** develop one main function from claim through evidence and explanation; close by resolving the point or establishing a specific relation to what follows
- **section:** read topic sentences and closing sentences in sequence; verify cumulative movement rather than repeated restatement

Use transitions that name the actual relation—contrast, cause, condition, extension, qualification, or consequence. Do not insert a transition merely to make adjacent paragraphs sound connected.

## Numbers, Citations, and Visuals

Trace material numbers and metadata to sources. Check units, denominators, rounding, sample subsets, equations, figure labels, table notes, and supplement entries.

Require support for external facts, prior findings, established definitions, data sources, parameters, thresholds, and methodological rationales. Verify in-text citations against the reference list and the claim they support.

Explain each visual's main pattern, relevant evidence, uncertainty, and relation to the question. Explain mechanisms only when supported. Inspect captions, panels, legends, axes, units, callouts, resolution, readability, and cross-file numbering.

Inspect visuals at their actual final document size, not only a zoomed source. Use [figures-tables-and-supplements.md](figures-tables-and-supplements.md) for readable labels, balanced whitespace, caption/note functions, and cross-artifact checks. Project choices such as bold references or a plain range connector remain preferences, not universal venue standards.

## Exact-Candidate Gate

Audit the exact text that will be delivered after the final rewrite, not the source paragraph or an earlier candidate. A local edit must still pass these bounded checks:

1. paragraph function, claim, evidence, development, and bridge;
2. preservation of locked meaning and defensible claim scope;
3. stable terminology and abbreviations;
4. exact and semantic repetition, stock transitions, vague synthesis, excessive summary, and project-discouraged phrases;
5. support for every retained or added citation and reconciliation of every removed citation; and
6. flow with the preceding and following paragraph when they are available.

If the project has a style or terminology profile, apply it even in lightweight mode. Treat a deterministic finding as a prompt for contextual judgment, but do not ignore it silently. If any word changes after this gate, repeat the affected checks on the new exact candidate.

These checks follow requested action: a substantive paragraph review tests retained support; a grammar-only correction preserves unchanged verified support and does not claim a new citation audit. Apply whole-section functions to section work, not to every isolated sentence. State any unavailable context or source.

## Four-Pass Review

Use the full passes for whole-paper/package review. Apply them within a substantially revised subsection or chapter and its affected dependencies; use the bounded candidate gate for surface edits. Existing project state is context, not evidence that a full review was requested.

### Pass 1: Argument and structure

Test reader functions, gap, purpose, questions, organization, paragraph openings, and contribution.

### Pass 2: Evidence and consistency

Test methods against outputs, samples, units, equations, figures, tables, citations, claim scope, and propagation.

### Pass 3: Scholarly prose

First stabilize terminology and abbreviations. Then review exact duplication, repeated phrases and openings, nontechnical word overuse, stock phrasing, long noun stacks, vague intensifiers, unstable subjects, syntax, tense, voice, notation, and paragraph-to-paragraph flow. Preserve necessary technical repetition and do not use synonym rotation as a cosmetic fix. After revising, run this pass once more on the exact post-edit candidate; findings from the pre-edit text do not certify the revision.

### Pass 4: Delivery integrity

Re-read the exact deliverables. Verify summaries, references, numbering, required statements, tracked changes, comments, filenames, rendering, companion files, and release status.

When Pass 4 exposes a substantive problem, repeat the affected earlier passes after correction.
