# academic-writing-skills

A Claude/Codex plugin for lifecycle-aware manuscript development and
reviewer-style scientific assessment. Version 1.1 has two main skills:

| Skill | Use it for |
|---|---|
| `$academic-writing-skills` | Extended outlines, section and paragraph drafting, evidence alignment, terminology, repetition, flow, revision, cross-file synchronization, and release checks |
| `$paper-review` | Review-only critique, top-to-bottom scientific review, revision-round assessment, prior-comment regression, and progressively loaded method, domain, or reviewer modules |

`$paper-review` uses `$academic-writing-skills` as its integrity base. Its
specialized knowledge is stored in direct references and loaded only when the
conversation or manuscript establishes that it applies.

[Traditional Chinese README](./README.zh-TW.md)

> Part of the [agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh).

## What changed in 1.1

- Made `$paper-review` a general reviewer rather than an Ethan- or water-only
  entry point.
- Added progressive modules for psychometrics and SEM; AI, LLM, ABM, and
  computational studies; water, CNHS, policy, and uncertainty; and flood,
  hydrodynamics, and catastrophe modeling.
- Kept Ethan-style review and named project precedents as explicit-only
  references that never activate from a water or modeling topic alone.
- Added an end-to-end workflow from extended outline through paragraph
  drafting, section integration, top-to-bottom review, revision regression,
  summary rebuilding, and exact submission-package release.
- Added a style profile and deterministic prose diagnostics for exact
  duplication, repeated sentence openings and phrases, stock phrasing, and
  candidate nontechnical word overuse.
- Clarified that formulaic or AI-like prose features are writing diagnostics,
  not proof of AI authorship, and that technical terms must not be rotated for
  cosmetic variety.

## Install

Install through the
[`ai-research-skills` Claude Code marketplace](https://github.com/WenyuChiou/ai-research-skills):

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

For an existing installation:

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

## Which skill should I use?

| Request | Invoke |
|---|---|
| Build or revise an outline, section, paragraph, Abstract, or Conclusion | `$academic-writing-skills` |
| Check terminology, repeated wording, stock phrasing, or flow while revising | `$academic-writing-skills` |
| Critique an outline, section, manuscript, supplement, or submission package | `$paper-review` |
| Run a psychometrics, SEM, LLM, water, flood, ABM, or hybrid technical review | `$paper-review`; it selects the relevant references |
| Run an Ethan-style R1–R4 review or check supplied PI comments | `$paper-review` with the Ethan-style request stated explicitly |
| Apply accepted review comments | `$academic-writing-skills` plus the selected comments |
| Verify that prior comments were resolved without regressions | `$paper-review` plus the prior comments and relevant versions |

## How progressive review routing works

`$paper-review` first uses the conversation, title, Abstract, questions,
Methods, equations, figures, tables, and supplement to infer the smallest
sufficient module set:

| Evidence in the paper | Reference loaded |
|---|---|
| Surveys, scales, CFA, psychometrics, SEM, mediation, multi-group analysis | `quantitative-psychometrics-sem.md` |
| Simulation, ABM, ML, GenAI, LLMs, synthetic respondents, agent evaluation | `ai-llm-computational.md` |
| Water resources, CNHS, policy, frameworks, reviews, uncertainty, equifinality | `water-cnhs-uncertainty.md` |
| Flood risk, hydrodynamics, drainage, inundation, catastrophe and loss models | `flood-hydrodynamics-catastrophe.md` |
| Explicit revision round or prior-review comparison | `round-calibration.md` |
| Explicit Ethan-style or confirmed lab-review context | `ethan-style-overlay.md`; exact project context may also load `project-precedents.md` |

A hybrid paper may load several modules. The reviewer asks one targeted
question only when unresolved ambiguity would materially change the required
evidence or review standard—for example, whether a factor analysis is
exploratory or confirmatory. It does not ask the user to select a domain when
the manuscript already makes the choice clear.

Additional users can contribute a new direct reference. Each module should
define trigger and exclusion cues, technical and evidence checks, claim-scope
boundaries, display or reproducibility checks, and at least one routing or
boundary eval. Reviewer, journal, laboratory, and project rules remain separate
conditional overlays.

## End-to-end manuscript workflow

### 1. Establish project authority

For a full manuscript, repeated revision, or multi-file package, initialize a
project state:

```bash
python skills/academic-writing-skills/scripts/init_manuscript_state.py \
  manuscript_state.json
```

Record active artifacts, authoritative analyses and sources, locked questions
and decisions, terminology, facts, question-to-evidence alignment, open issues,
and release checks. Keep the state with the manuscript project, not inside the
installed plugin.

> Use `$academic-writing-skills` to establish the manuscript contract and
> authority hierarchy for these files. Do not draft yet. Identify the gap,
> task, questions, outcomes, contribution, nonclaims, and unresolved sources.

### 2. Build the extended outline

Use `$academic-writing-skills` to build an evidence plan rather than a list of
headings. For each section and planned paragraph, define the reader function,
central claim or question, authorized evidence, inference boundary, and bridge
to the next unit. Test the plan top-down from gap to contribution and bottom-up
from available evidence to supported claims.

> Use `$academic-writing-skills` to build the extended outline. Map every
> planned paragraph to its function, claim, evidence, inference limit, and
> next-paragraph bridge. Flag missing analyses or sources; do not fabricate
> expected results.

For a technically complex study, then ask `$paper-review` to critique the
outline. It will load the applicable psychometric, computational, LLM, water,
or flood modules without turning the review into prose drafting.

### 3. Draft one paragraph or section at a time

Use a five-part paragraph contract:

1. function
2. narrowest defensible claim
3. authorized evidence
4. evidence-based development
5. bridge to the next paragraph

Provide the active outline, sources, locked wording, and adjacent paragraphs.
A bounded request stays bounded.

> Use `$academic-writing-skills` to draft Section 2.3 from the approved outline
> and supplied sources. Preserve locked terms and numbers. For every paragraph,
> verify function, claim, evidence, development, and bridge, then check its
> handoff to the preceding and following paragraphs.

When a completed passage needs an independent technical critique, use
`$paper-review` in review-only mode and let it select the relevant references.

### 4. Integrate each section

After drafting a section, read its topic sentences and closing sentences in
sequence. Verify that paragraphs form one cumulative argument, do not duplicate
the same function, and do not introduce orphan evidence or unsupported
transitions. Reconcile terminology, abbreviations, citations, figures, and
tables before moving on.

### 5. Run milestone reviews

General or domain-specific review:

> Use `$paper-review` for a substantive, review-only assessment of the current
> manuscript and supplement. Infer and state the modules used, rank issues by
> scientific and reproducibility risk, and do not edit.

Explicit Ethan-style review:

> Use `$paper-review` for an Ethan-style R2 review. Compare the current files
> with the supplied prior comments, separate MUST/SHOULD/QUERY/PREFERENCE from
> severity, and report resolved, partial, open, regressed, and new issues.

### 6. Revise through the writing core

Return accepted review items to `$academic-writing-skills`. Separate authorized
edits from items needing an author decision or missing source. Propagate every
semantic or evidence change to affected Methods, Results, Discussion,
limitations, Abstract, Conclusion, supplement, displays, and submission
materials.

### 7. Run the full top-to-bottom review

When all major sections exist, ask `$paper-review` to run four distinct passes
on the exact active files:

1. argument and structure
2. evidence, methods, claims, figures, tables, equations, and citations
3. scholarly prose, terminology, repetition, observable stock phrasing, and
   paragraph-to-paragraph flow
4. summaries, references, numbering, metadata, rendering, and release
   integrity

Then run the bottom-up check from source evidence through result,
interpretation, contribution, Abstract, and Conclusion. If a prose edit changes
scientific meaning, repeat the affected evidence checks.

### 8. Rebuild summaries from the stabilized manuscript

Use `$academic-writing-skills` to rebuild the title, Abstract, highlights,
Conclusion, conference abstract, and cover materials from the current evidence
map. Never treat an older Abstract as the authority source.

### 9. Verify the exact submission package

Use `$paper-review` at submission stage on the final manuscript, supplement,
figures, tables, highlights, cover letter, metadata, declarations, and required
repository statements. High-severity blockers, unknown required facts, stale
companion files, tracked changes, or failed rendering prevent
`SUBMISSION_READY`.

## Terminology, repeated wording, stock phrasing, and flow

The writing core distinguishes necessary technical repetition from avoidable
prose repetition. Register one preferred term per concept and protect
constructs, model names, populations, and outcomes from cosmetic synonym
rotation.

The scholarly-prose pass checks:

- exact or near-duplicate sentences and paragraph functions
- repeated nontechnical words, phrases, and sentence openings
- generic metadiscourse, empty intensifiers, stock transitions, vague subjects,
  repetitive cadence, and content-light summaries
- subject continuity and familiar-to-new information order
- paragraph claim–evidence–development logic
- topic-sentence and closing-sentence flow across each section

These are writing diagnostics, not AI detection. The skills must never claim
that prose was generated by GPT or another model solely from style.

Useful deterministic diagnostics:

```bash
python skills/academic-writing-skills/scripts/audit_manuscript_state.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_text_consistency.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_prose_patterns.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_docx_structure.py manuscript.docx
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

The scripts report candidates for contextual review; they do not decide that a
technical term is overused, a transition is wrong, or prose is AI-generated.

## Repository layout

```text
skills/
  academic-writing-skills/
  paper-review/
    references/
evals/
tests/
```

## Testing

```bash
python -m pytest tests/ -q
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

The tests check both skill boundaries, progressive reference routing,
project-state schema, prose and integrity regressions, eval coverage, and
common encoding corruption.

Every review, revision, audit, or release check ends with a named
functional-completeness retrospective rather than a generic all-clear.

## Scope

The plugin does not invent assumptions, analyses, results, citations,
mechanisms, or metadata. It also does not replace Zotero, NotebookLM, document
rendering, or format-specific tracked-change tooling.

## License

MIT
