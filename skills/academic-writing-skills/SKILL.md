---
name: academic-writing-skills
description: Plan, outline, draft, review, revise, or proofread academic manuscripts, journal articles, theses, conference papers, abstracts, supplementary materials, and submission packages across disciplines and study designs. Use for extended-outline development, section or paragraph drafting, developmental editing, top-to-bottom and bottom-up integrity checks, reviewer-style revision, method and evidence alignment, terminology control, repetition and flow review, observable stock or AI-like prose patterns, citation consistency, natural scholarly prose, claim-scope control, cross-file synchronization, change-impact review, or final submission readiness.
---

# Academic Writing Skills

## Governing Principle

Preserve the authors' evidence, intended meaning, and locked decisions while making the scholarly argument clear, reproducible, internally consistent, and no stronger than the evidence permits. Never invent results, mechanisms, citations, metadata, analyses, or field requirements.

Treat a manuscript as an evolving evidence system, not as isolated prose. Follow the author's writing sequence, but re-open earlier sections whenever later evidence changes them.

## Route the Task

First identify:

- requested action: plan, draft, review, revise, proofread, or certify readiness
- artifact scope: sentence, paragraph, subsection, chapter, full manuscript, supplement, or submission package
- change impact and available verification sources, separately from artifact scope
- manuscript archetype and study design
- lifecycle stage and review maturity
- authoritative sources, active files, and historical references
- user-locked wording, facts, terminology, and decisions
- whether editing is authorized or the task is diagnosis only

Use **lightweight mode** for bounded text work. Use **managed-project mode** for full-manuscript integration, companion-file coordination, or release certification; reuse an existing managed context for local work in that project. Managed context does not turn a paragraph edit into a whole-paper audit. Route checks by requested action, textual scope, change impact, and source availability using [lifecycle-and-routing.md](references/lifecycle-and-routing.md).

In managed-project mode, read [state-and-authority.md](references/state-and-authority.md) and reuse equivalent project records. Initialize the project-state template with `scripts/init_manuscript_state.py` only when sustained coordination actually needs a record and none exists. Do not create project machinery for a one-off edit or reinitialize state merely because a new turn begins.

## Confirm Venue Direction, Format, and Style

For venue-directed planning, substantive restructuring, display/reference formatting, or submission checks, first confirm the target journal, article type, audience, and publication stage. Use the **Venue Profile** in [overlay-contract.md](references/overlay-contract.md) to separate scientific direction, verified requirements, stylistic examples, and project preferences. Reuse a current profile; verify changed or uncertain official requirements before applying them. A grammar-only edit does not trigger journal reselection or a whole-package audit. If no venue is selected, keep advice provisional and do not invent compliance.

Use the ABM examples in the display guide and overlay contract as source-grounded reasoning aids, not journal-wide templates or certification of the original paper.

For a worked example of an outline, abstract, reviewer response, or display check, load [professor-teaching-cases.md](references/professor-teaching-cases.md) when requested or when a matching task needs a concrete demonstration. Select the relevant case; do not load all examples or expand a grammar-only edit into a section review.

## Follow the Manuscript Lifecycle

Map the work to this lifecycle without forcing the final article order to equal the writing order:

1. establish project authority, manuscript archetype, and intended venue
2. develop the extended outline, Introduction, gap, questions, and planned contribution
3. develop study context, data, theory, and Methods
4. build Results from verified analyses, figures, tables, or source evidence
5. develop Discussion, alternatives, implications, limitations, and future work
6. synthesize the Conclusion from the stabilized evidence map
7. rebuild the title, Abstract, highlights, and summaries from the current manuscript
8. reconcile references, parallel-developed supplements, metadata, and submission files
9. pass release checks on the exact deliverables

At every stage, test the relevant part of both directions of alignment:

- **top-down:** purpose or gap → question or objective → method → expected evidence
- **bottom-up:** source evidence → result → interpretation → contribution and summary claim

Read [lifecycle-and-routing.md](references/lifecycle-and-routing.md) for stage gates, review maturity, non-IMRAD routing, and change-impact classes.

For planning, drafting, or reorganizing an Introduction or study-context section, read [introduction-and-study-context.md](references/introduction-and-study-context.md). It guides section functions and content placement, not fixed paragraph counts or a mandatory article structure. A bounded language edit uses the local prose checks instead.

For planning or developing Methods, or substantively clarifying a setting's source, rationale, or assumption status, read [methods-and-assumptions.md](references/methods-and-assumptions.md). Distinguish the provenance of a value or rule from assumptions about its application and from evidence of validation. Use the hypothetical examples as reasoning aids, not as verified study facts.

Load the remaining guides only for the requested reader function or an affected dependency:

- [results-and-explanation.md](references/results-and-explanation.md): evidence-led findings, so-what/SQ closure, visual functions, and supported versus merely programmed mechanisms.
- [discussion-and-limitations.md](references/discussion-and-limitations.md): interpretation or extension-analysis mode, sensitivity boundaries, and specific-constraint-first limitations.
- [conclusion-and-abstract.md](references/conclusion-and-abstract.md): study identity, supported summaries, and flexible abstract information functions rather than universal sentence templates.
- [figures-tables-and-supplements.md](references/figures-tables-and-supplements.md): final-size legibility, captions/notes, parallel SM, numbering, and project formatting.

At each chapter completion or substantial chapter revision, run the chapter-closure blind-spot check in [lifecycle-and-routing.md](references/lifecycle-and-routing.md). The checkpoint is required; select diagnostic questions by design, content, and evidence. Do not run a full chapter audit for a grammar-only edit or claim exhaustive discovery of unknown unknowns.

## Draft from Explicit Writing Contracts

Before drafting an outline, section, or paragraph, identify its reader function, central claim or question, authorized evidence, inference limit, and link to adjacent material. For a paragraph, use this compact contract:

1. function: what the paragraph must accomplish
2. claim: the narrowest defensible main point
3. evidence: the source, result, citation, or reasoning that supports it
4. development: how the evidence is explained without adding a mechanism
5. bridge: what relation leads into the next paragraph

Before drafting or substantively rewriting, run the pre-draft logic check in [universal-integrity.md](references/universal-integrity.md): check both the progression within a paragraph and the relation between adjacent paragraphs. Match the depth to the requested scope; a local edit does not require replanning the whole section.

Draft only after the contract and information order are coherent. After drafting, compare the paragraph against the contract and re-read its previous and next paragraphs. Do not polish a paragraph into fluency if its function, evidence, or placement is wrong.

Also identify the intended reader's likely knowledge. For interdisciplinary papers and reviewer responses, assume a reader who understands the broader research area but does not know the study's internal terminology, model sequence, data transformations, or earlier drafting history. Supply the minimum context that reader needs at the point of use; do not make the reader reconstruct it from later text.

## Apply Universal Integrity Gates

Always consider these gates within the requested scope and directly affected dependencies. Determine applicability; do not rerun every whole-paper check for every local edit:

1. **Authority:** derive facts from identified sources; do not infer authorship roles, funding, sample sizes, or methods from formatting or old drafts.
2. **Contract:** preserve locked gap, task, questions, outcomes, contribution, and explicit nonclaims unless the user authorizes a semantic change.
3. **Alignment:** connect the affected question or objective to its method, evidence, substantive answer, and inference boundary; check the complete map during whole-paper review.
4. **Method–evidence integrity:** require enough detail to understand how evidence was produced and which assumptions bound the inference.
5. **Claim scope:** distinguish direction, magnitude, uncertainty, significance, equivalence, causation, mechanism, prediction, and generalizability.
6. **Cross-artifact synchronization:** propagate material changes to every affected section and companion artifact.
7. **Version integrity:** identify one active release and distinguish it from historical references.
8. **Release integrity:** never use `FINAL`, `VERIFIED`, or `SUBMISSION_READY` while a high-severity blocker or unresolved required source remains.
9. **Prose integrity:** preserve one term per concept, distinguish necessary technical repetition from avoidable verbal repetition, and verify paragraph-to-paragraph flow without using synonym rotation to hide repetition.

Read [universal-integrity.md](references/universal-integrity.md) for paragraph, abstract, conclusion, evidence, terminology, citation, and four-pass review rules.

## Select Study-Design Adapters

Select adapters by research design, not by discipline label. Load only the relevant sections of [study-design-adapters.md](references/study-design-adapters.md):

- quantitative observational or survey research
- experiments or quasi-experiments
- qualitative research
- mixed methods
- computational models or simulations
- AI/LLM-based studies
- evidence syntheses, reviews, or meta-analyses
- theoretical, conceptual, framework, methods, or data papers

Combine adapters when the design is genuinely hybrid. Treat adapter checks as questions requiring manuscript evidence, not assumptions that a method was used incorrectly.

## Compose External Overlays Safely

Apply a supplied domain skill, reviewer rubric, professor checklist, reporting standard, or journal guide as an overlay. Read [overlay-contract.md](references/overlay-contract.md) before applying one.

Keep overlay rules classified as:

- study-design requirement
- domain convention or technical check
- reviewer preference or tone
- venue requirement
- project-specific fact or decision

Never promote an overlay rule into a universal rule. When an overlay conflicts with evidence, author instructions, ethics, or defensible inference, preserve the evidence and report the conflict. A request to explain “why” does not authorize an unsupported mechanism.

## Apply Registered Project Workflows

When the project, folder, manuscript, or user request identifies **Survey paper**, **PiDS**, or a **WC_vX** manuscript, use the installed `survey-paper-wcvx` skill as the project-state and reviewer-round overlay together with these universal integrity gates. Keep that project's filenames, author identity, priority scheme, and version rules within the project overlay.

## Handle Reviewer Responses

For rebuttal letters, response-to-reviewers documents, or revisions of an
advisor-edited response draft, read
[reviewer-response-workflow.md](references/reviewer-response-workflow.md).
Use its comment ledger, response-order, evidence, cross-reference, and formatted
document checks together with the active manuscript state and any supplied lab
examples. Keep reviewer-facing prose, manuscript or supplement changes, and
internal replies to an advisor distinct. A high-level synthesis response may
navigate to later detail, but the first substantive response to an issue must
explain the change, evidence, interpretation, manuscript effect, and remaining
boundary needed to answer that comment.

## Control Material Changes

Classify each proposed change before editing:

- **Class A — semantic contract:** gap, task, question, outcome, contribution, causal or validation framing
- **Class B — evidence or method:** data, sample, model, analysis, number, figure, table, limitation
- **Class C — metadata:** authors, affiliations, funding, roles, declarations, repository links
- **Class D — surface:** grammar, punctuation, formatting, local clarity with no scientific change

Run the corresponding impact scan before declaring the edit complete. Class A normally reopens the whole evidence chain and all summaries. Class B reopens affected methods, results, interpretations, visuals, supplements, and summaries. Class C reopens every submission artifact and metadata field. Class D requires a local semantic diff and formatted-file check.

Do not make a global replacement across equations, field codes, citations, XML, or metadata without protected-context checks and a post-change diff.

## Use Deterministic Audits as Evidence, Not Judgment

For managed projects, use the bundled scripts when relevant:

- `scripts/audit_manuscript_state.py`: validate state completeness, source links, question alignment, dimension coverage, and release blockers
- `scripts/audit_text_consistency.py`: extract text from supported files and scan registered locked strings, prohibited variants, and fact conflicts
- `scripts/audit_prose_patterns.py`: report exact duplication, repeated openings and phrases, stock phrasing, and candidate nontechnical word overuse without claiming AI authorship
- `scripts/audit_candidate_text.py`: scan the exact proposed passage against the active project terminology, forbidden variants, and prose profile and record its hash
- `scripts/audit_docx_structure.py`: inspect Word OOXML using exact tag names for tracked changes, revision authors, comments, parent-linked replies, reply authors, fields, and placeholders
- `scripts/run_regression_tests.py`: verify the audit tools against bundled failure cases

Treat script findings as diagnostics. Inspect each match in context before editing. A clean script report never replaces substantive reading.

## Gate the Exact Candidate Before Delivery

After the last wording change, freeze the exact passage or artifact that will be delivered. Reuse the relevant active-state entries and applicable overlay rules, including for local work in a managed project. Do not load unrelated project history or audit companion files merely because they exist. Then, at the depth required by the requested action and change impact:

1. compare the exact candidate with its writing contract, locked meaning, evidence, and adjacent paragraphs;
2. check added, removed, or semantically affected citations against their claims and the reference list; substantive passage review also checks retained claim–citation support, while grammar-only work preserves unchanged verified support and states any verification limit;
3. run terminology, forbidden-variant, repetition, stock-phrase, and project-discouraged-phrase checks on the exact candidate itself;
4. inspect and resolve each deterministic finding in context, or record an explicit author-approved reason to retain it; and
5. record which candidate was checked, using its hash when a deterministic candidate audit is available.

For prose revision, select the applicable functional checks in [prose-and-citation-editing.md](references/prose-and-citation-editing.md): transitions, function-preserving concision, natural scholarly prose, claim–citation alignment, observable stock or AI-like features, and dash/hyphen style. A punctuation edit needs meaning preservation, not a new literature audit. Treat diagnostics as prompts for judgment, not universal bans or authorship detection.

For a substantial manuscript section, abstract, rebuttal, or explicit banned-word audit, also inspect the exact candidate against [banned_words.md](references/banned_words.md). Treat every match as a contextual diagnostic rather than an automatic deletion or evidence of AI authorship, and apply any project-specific writing contract or terminology override first.

Any edit after this gate invalidates its result. Re-run every affected candidate check before calling the wording checked, final, polished, or ready to paste. Never report that `academic-writing-skills` passed when only an earlier draft, the surrounding manuscript, or an unchanged source artifact was audited.

## Conduct Four Distinct Passes

For whole-paper or submission-package review, complete four top-to-bottom passes. For a substantial subsection or chapter revision, apply the passes to that unit and its affected dependencies; a bounded language edit uses the local candidate gate:

1. **Argument and structure:** reader functions, purpose, questions, organization, paragraph openings, and contribution.
2. **Evidence and scope:** methods, data, results, figures, tables, citations, uncertainty, claim strength, and cross-file propagation.
3. **Scholarly writing:** clarity, natural subjects, terminology, necessary versus avoidable repetition, sentence-opening variety, observable stock phrasing, paragraph flow, syntax, tense, voice, and notation. Never label prose AI-generated from style alone.
4. **Delivery integrity:** summaries, references, numbering, metadata, exact filenames, tracked changes, visual rendering, and release blockers. Read the revised prose aloud or simulate an ordinary spoken reading. If a sentence would sound unnatural when said by a researcher, or its meaning becomes clear only after rereading, revise its syntax, referents, or information order without making the scholarly language casual.

If a later pass finds a material issue, fix it and repeat every affected upstream and downstream check. Do not certify the earlier pass as current.

## End Every Check with a Functional-Completeness Retrospective

After every review, revision round, audit, or release check, explicitly revisit the task's functional coverage before reporting completion. Ask:

1. Did the work cover the requested lifecycle stage and every artifact in scope?
2. Did it preserve locked meaning and consult the correct authority sources?
3. Did every affected question, method, result, interpretation, limitation, and summary remain aligned?
4. Did all relevant study-design adapters and overlays run without becoming universal assumptions?
5. Did the change-impact scan cover upstream, downstream, and companion-file dependencies?
6. Are any unknowns, unavailable sources, open issues, waivers, or high-severity blockers still present?
7. Were deterministic, structural, and visual checks used where applicable, and were their limits stated?
8. Is the exact deliverable—not an intermediate copy—the one inspected?
9. Did the exact post-edit candidate pass the applicable project profile, and were all findings resolved or explicitly retained with a reason?

Apply these questions to the agreed scope, not every possible artifact. If a required answer is no or unknown, continue safe in-scope work or report the limit. Distinguish **checked**, **not applicable**, **outside requested scope**, and **source unavailable/unverified**; an excluded check is not a pass. Never collapse this retrospective into a generic “all checks passed.”

Read [reviewer-red-team-and-release.md](references/reviewer-red-team-and-release.md) for negative-space tests, issue severity, readiness criteria, and the final report format.

## Work with Formatted Files

Use the dedicated document, spreadsheet, presentation, or PDF skill for file-format operations and visual verification. This skill governs scholarly integrity; it does not replace format-specific rendering, tracked-change, or OOXML workflows.

## Report the Outcome

Lead with readiness and remaining blockers. Report only checks actually performed. State:

- what changed and what was preserved
- whether scientific meaning, evidence, numbers, citations, or metadata changed
- which artifacts and lifecycle gates were checked, not applicable, outside scope, or unverified
- unresolved issues, unavailable sources, or explicit waivers
- the functional-completeness retrospective outcome

Do not call a manuscript final when the evidence supports only a partial or conditional review.
