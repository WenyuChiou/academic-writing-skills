# academic-writing-skills

Two composable skills for evidence-safe academic writing and scientific paper
review. They treat a manuscript as an evolving evidence system: every claim
must remain aligned with its question, method, evidence, interpretation, and
summary across the active manuscript and companion files.

[Traditional Chinese README](./README.zh-TW.md)

> Part of the [agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh).

## Skills at a glance

| Skill | Best starting point for |
|---|---|
| [`$academic-writing-skills`](./skills/academic-writing-skills/SKILL.md) | Extended outlines, section or paragraph drafting, revision, terminology control, repetition and flow checks, cross-file synchronization, and submission-package preparation |
| [`$paper-review`](./skills/paper-review/SKILL.md) | Review-only critique, top-to-bottom scientific review, revision-round assessment, prior-comment regression checks, and method- or domain-specific review |

`$paper-review` uses `$academic-writing-skills` as its manuscript-integrity
base, then progressively loads only the technical references supported by the
paper. A request to review does not authorize manuscript editing.

## Quick start

### 1. Install or update

Install through the
[`ai-research-skills` Claude Code marketplace](https://github.com/WenyuChiou/ai-research-skills):

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

This single plugin installation enables both `$academic-writing-skills` and
`$paper-review`.

Update an existing installation:

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

### 2. Invoke the skill you need

In Claude Code, invoke `$academic-writing-skills` or `$paper-review`. The
installation commands above are specifically for Claude Code. If the skills
are already installed separately in ChatGPT or Codex, request them by name,
for example `Use @paper-review ...`.

The copyable prompts below use Claude Code's `$skill-name` form. In ChatGPT or
Codex, replace it with `@skill-name`.

You do not need to select technical modules manually. State the task, attach
the active files, and identify any prior version, reviewer comments, journal,
or locked decisions that matter.

### 3. Provide the right evidence

| Task | Minimum useful input |
|---|---|
| Outline planning | Research purpose, gap, questions or objectives, methods, available evidence, intended venue, and explicit nonclaims |
| Section drafting | Approved outline, authorized sources or results, locked terminology, and adjacent paragraphs |
| Scientific review | Exact active manuscript plus relevant figures, tables, supplement, and intended review stage |
| Revision-round check | Current manuscript, prior comments, author responses, and the prior version when available |
| Submission check | Exact files to be submitted plus current venue requirements and metadata |

If a required source is unavailable, the skills report the limit instead of
guessing.

For work involving several files or versions, this compact header prevents
most authority conflicts:

```text
TASK: [plan / draft / revise / review / submission check]
ACTIVE FILES: [the exact versions to review or change]
AUTHORITY SOURCES: [results, data, code, approved outline, or decisions that control conflicts]
LOCKED DECISIONS: [wording, numbers, questions, or claims that must not change]
NONCLAIMS: [interpretations or conclusions the manuscript must not make]
TARGET / STAGE: [venue and developmental / substantive / integration / submission]
```

Use `developmental` for an outline or incomplete draft, `substantive` when the
core scientific content exists, `integration` for a complete draft and its
companion files, and `submission` only for the exact release package. If a
journal or reviewer supplied an R1–R4 label, provide it explicitly; the skill
does not infer a round from writing quality or comment count.

For editable revision, provide the DOCX or source file; a PDF is sufficient
for review-only work when its text and displays are legible. Attach standalone
figures, tables, and supplements when they are not fully readable in the main
file. Add source papers for exact citation checks, code or data for
reproducibility and derived-display checks, and the current journal guide for
venue-specific formatting.

## Copy-and-paste prompts

### Build an extended outline

```text
Use $academic-writing-skills to build an extended outline from the attached
materials. First establish the gap, task, research questions, methods,
available evidence, intended contribution, and nonclaims. For every planned
paragraph, specify its function, claim, authorized evidence, inference limit,
and bridge to the next paragraph. Do not draft the full manuscript yet.
```

### Draft a section

```text
Use $academic-writing-skills to draft Section 2.3 from the approved outline
and supplied sources. Preserve all locked terms, numbers, and citations. Check
each paragraph's function, claim, evidence, development, and bridge, then
verify its connection to the preceding and following paragraphs.
```

### Revise an existing section

```text
Use $academic-writing-skills to revise the attached current version of Section
2.3 for the stated purpose. Treat the supplied results and approved outline as
authority sources. Preserve the locked terms, numbers, citations, research
questions, and claim scope. Show any requested change that would require new
evidence or an author decision instead of silently making it.
```

### Check terminology, repetition, and flow

```text
Use $academic-writing-skills to revise this section for terminology
consistency, avoidable nontechnical repetition, stock phrasing, and
paragraph-to-paragraph flow. Protect necessary technical repetition and do not
change scientific meaning, numbers, citations, or claim strength.
```

### Run a substantive scientific review

```text
Use $paper-review for a substantive, review-only assessment of the attached
manuscript and supplement. Infer and state the smallest applicable module set,
rank issues by scientific and reproducibility risk, anchor comments to the
manuscript, and do not edit the files.
```

### Verify a revision round

```text
Use $paper-review to compare the current manuscript with the supplied prior
comments, response letter, and earlier version. Classify each issue as
resolved, partial, open, regressed, waived, new, or not verifiable. Do not
treat an author reply or resolved comment thread as proof that the requested
change appears in every affected file.
```

### Apply selected review comments

```text
Use $academic-writing-skills to implement review items 1, 3, and 5. Preserve
the accepted scientific meaning. Keep items that require a missing source or
author decision open, and propagate each material change to every affected
section, figure, table, supplement, Abstract, and Conclusion.
```

### Check the final submission package

```text
Use $paper-review at submission stage on the exact attached manuscript,
supplement, figures, tables, highlights, cover letter, declarations, and
metadata. Run top-to-bottom and bottom-up checks, identify release blockers,
and mark the package SUBMISSION_READY only if the exact deliverables support
that status.
```

## Recommended manuscript workflow

| Stage | Skill | Outcome |
|---|---|---|
| 1. Establish authority | `$academic-writing-skills` | Active files, authoritative sources, locked decisions, questions, contribution, and nonclaims |
| 2. Plan | `$academic-writing-skills` | Evidence-linked extended outline |
| 3. Draft and integrate | `$academic-writing-skills` | Sections with coherent paragraph functions and cross-section consistency |
| 4. Review | `$paper-review` | Priority-ranked scientific and presentation issues without edits |
| 5. Revise | `$academic-writing-skills` | Authorized fixes propagated across affected artifacts |
| 6. Verify | `$paper-review` | Cross-round regression or exact-package release assessment |

The workflow is iterative. A material change to a question, method, result, or
claim reopens every affected downstream summary and companion file.

## How progressive paper review works

`$paper-review` infers the smallest sufficient module set from the conversation,
Abstract, questions, Methods, equations, figures, tables, and supplement. A
hybrid paper may load more than one module.

| Manuscript evidence | Reference loaded when applicable |
|---|---|
| Equations, formal notation, normalization, aggregation, composite metrics, or derived uncertainty displays | `display-notation-provenance.md` |
| Surveys, scales, psychometrics, CFA, SEM, mediation, or multi-group comparison | `quantitative-psychometrics-sem.md` |
| Simulation, ABM, ML, GenAI, LLMs, synthetic respondents, or agent evaluation | `ai-llm-computational.md` |
| Water resources, CNHS, policy, frameworks, uncertainty, or equifinality | `water-cnhs-uncertainty.md` |
| Flood risk, inundation, drainage, hydrodynamics, catastrophe models, exposure, vulnerability, or loss | `flood-hydrodynamics-catastrophe.md` |
| Prior comments, earlier drafts, or an explicit revision round | `round-calibration.md` |
| An explicit Ethan-style request or confirmed relevant lab-review context | `ethan-style-overlay.md`; exact project context may also load `project-precedents.md` |

A keyword or study-area mention alone does not activate a module. The reviewer
asks one targeted question only when an unresolved ambiguity would materially
change the review standard, such as whether a factor analysis is exploratory
or confirmatory.

## Long-running projects and deterministic diagnostics

A one-off passage edit can use lightweight mode without extra setup. For a
full manuscript, repeated revision, or a multi-file submission package,
initialize a project state and keep it with the manuscript project:

```bash
python skills/academic-writing-skills/scripts/init_manuscript_state.py \
  manuscript_state.json
```

The state records active artifacts, authority sources, locked wording, facts,
terminology, question-to-evidence alignment, decisions, open issues, and
release checks. It is a project record, not a memory of every wording choice.

Useful diagnostics:

```bash
python skills/academic-writing-skills/scripts/audit_manuscript_state.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_text_consistency.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_prose_patterns.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_docx_structure.py manuscript.docx
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

These scripts surface candidates for contextual review. They do not decide
that a technical term is overused, a transition is wrong, or prose was
AI-generated.

## Evidence and review boundaries

- The skills do not invent assumptions, analyses, results, citations,
  mechanisms, thresholds, reviewer preferences, or metadata.
- Technical terminology is protected from cosmetic synonym rotation; prose
  repetition is assessed in context.
- Observable stock or AI-like writing patterns are editing diagnostics, not
  evidence of AI authorship.
- A response letter is evidence of an author claim, not proof that a revision
  is present in the current manuscript and all companion files.
- Every review, revision, audit, or release check ends with a
  functional-completeness retrospective that states what was checked, what
  remains unresolved, and what limits readiness.
- The plugin complements rather than replaces Zotero, NotebookLM, statistical
  software, source verification, document rendering, or tracked-change tools.

## Repository layout

```text
skills/
  academic-writing-skills/
    SKILL.md
    references/
    scripts/
    assets/
    agents/
  paper-review/
    SKILL.md
    references/
    assets/
    agents/
evals/
tests/
```

New reusable review knowledge belongs in a direct `paper-review` reference
with explicit trigger and exclusion cues, technical and evidence checks,
claim-scope boundaries, and at least one routing or boundary eval. Journal,
reviewer, laboratory, and project rules remain separate conditional overlays.

## Testing

```bash
python -m pytest tests/ -q
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

The tests cover skill boundaries, progressive routing, project-state schema,
prose and integrity regressions, eval coverage, and common encoding corruption.

See [CHANGELOG.md](./CHANGELOG.md) for release history.

## License

MIT
