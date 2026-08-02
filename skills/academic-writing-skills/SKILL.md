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
- artifact scope: passage, section, full manuscript, supplement, or submission package
- manuscript archetype and study design
- lifecycle stage and review maturity
- authoritative sources, active files, and historical references
- user-locked wording, facts, terminology, and decisions
- whether editing is authorized or the task is diagnosis only

Use **lightweight mode** for a passage, isolated section, or bounded language edit. Use **managed-project mode** for a full manuscript, repeated revision, multiple companion files, material scientific changes, or any submission-ready request.

In managed-project mode, read [state-and-authority.md](references/state-and-authority.md) and use the project-state template. Initialize it with `scripts/init_manuscript_state.py` when no equivalent project record exists. Do not create project state for a simple one-off edit.

## Follow the Manuscript Lifecycle

Map the work to this lifecycle without forcing the final article order to equal the writing order:

1. establish project authority, manuscript archetype, and intended venue
2. develop the extended outline, Introduction, gap, questions, and planned contribution
3. develop study context, data, theory, and Methods
4. build Results from verified analyses, figures, tables, or source evidence
5. develop Discussion, alternatives, implications, limitations, and future work
6. synthesize the Conclusion from the stabilized evidence map
7. rebuild the title, Abstract, highlights, and summaries from the current manuscript
8. reconcile references, supplements, metadata, and submission files
9. pass release checks on the exact deliverables

At every stage, run both directions of alignment:

- **top-down:** purpose or gap → question or objective → method → expected evidence
- **bottom-up:** source evidence → result → interpretation → contribution and summary claim

Read [lifecycle-and-routing.md](references/lifecycle-and-routing.md) for stage gates, review maturity, non-IMRAD routing, and change-impact classes.

## Draft from Explicit Writing Contracts

Before drafting an outline, section, or paragraph, identify its reader function, central claim or question, authorized evidence, inference limit, and link to adjacent material. For a paragraph, use this compact contract:

1. function: what the paragraph must accomplish
2. claim: the narrowest defensible main point
3. evidence: the source, result, citation, or reasoning that supports it
4. development: how the evidence is explained without adding a mechanism
5. bridge: what relation leads into the next paragraph

Draft only after the contract is coherent. After drafting, compare the paragraph against the contract and re-read its previous and next paragraphs. Do not polish a paragraph into fluency if its function, evidence, or placement is wrong.

## Apply Universal Integrity Gates

Always verify:

1. **Authority:** derive facts from identified sources; do not infer authorship roles, funding, sample sizes, or methods from formatting or old drafts.
2. **Contract:** preserve locked gap, task, questions, outcomes, contribution, and explicit nonclaims unless the user authorizes a semantic change.
3. **Alignment:** connect every central question or objective to a method, evidence source, substantive answer, interpretation, limitation, and contribution.
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
- `scripts/audit_docx_structure.py`: inspect Word OOXML using exact tag names for tracked changes, comments, fields, and placeholders
- `scripts/run_regression_tests.py`: verify the audit tools against bundled failure cases

Treat script findings as diagnostics. Inspect each match in context before editing. A clean script report never replaces substantive reading.

## Conduct Four Distinct Passes

For full reviews or substantial revisions, complete four top-to-bottom passes:

1. **Argument and structure:** reader functions, purpose, questions, organization, paragraph openings, and contribution.
2. **Evidence and scope:** methods, data, results, figures, tables, citations, uncertainty, claim strength, and cross-file propagation.
3. **Scholarly writing:** clarity, natural subjects, terminology, necessary versus avoidable repetition, sentence-opening variety, observable stock phrasing, paragraph flow, syntax, tense, voice, and notation. Never label prose AI-generated from style alone.
4. **Delivery integrity:** summaries, references, numbering, metadata, exact filenames, tracked changes, visual rendering, and release blockers.

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

If any answer is no or unknown, continue the work or report the limit. Never collapse this retrospective into a generic “all checks passed.”

Read [reviewer-red-team-and-release.md](references/reviewer-red-team-and-release.md) for negative-space tests, issue severity, readiness criteria, and the final report format.

## Work with Formatted Files

Use the dedicated document, spreadsheet, presentation, or PDF skill for file-format operations and visual verification. This skill governs scholarly integrity; it does not replace format-specific rendering, tracked-change, or OOXML workflows.

## Report the Outcome

Lead with readiness and remaining blockers. Report only checks actually performed. State:

- what changed and what was preserved
- whether scientific meaning, evidence, numbers, citations, or metadata changed
- which artifacts and lifecycle gates were checked
- unresolved issues, unavailable sources, or explicit waivers
- the functional-completeness retrospective outcome

Do not call a manuscript final when the evidence supports only a partial or conditional review.
