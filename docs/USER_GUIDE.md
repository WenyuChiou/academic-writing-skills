# Usage Guide

This guide contains the optional detail removed from the main README. Most
users can start with the two prompts on the repository front page. Every
example below is platform-neutral: it names the skill in ordinary text instead
of relying on a client-specific invocation prefix.

[繁體中文](./USER_GUIDE.zh-TW.md)

## Choose a skill

Use the `academic-writing-skills` skill to plan, draft, revise, synchronize,
or prepare submission materials. Use the `paper-review` skill when you want a
review-only assessment. A review request does not authorize file editing.

## What to provide

| Task | Useful input |
|---|---|
| Outline | Purpose, gap, questions, methods, available evidence, target venue, and claims the paper must not make |
| Draft or revision | Approved outline, authorized sources or results, locked terminology, and adjacent text |
| Scientific review | Exact active manuscript, figures, tables, supplement, and intended review stage |
| Revision-round check | Current manuscript, prior comments, response letter, and prior version when available |
| Submission check | Exact submission files, current venue requirements, and metadata |

For work involving several files or versions, add this header to your prompt:

```text
TASK: [plan / draft / revise / review / submission check]
ACTIVE FILES: [exact versions to review or change]
AUTHORITY SOURCES: [results, data, code, approved outline, or decisions that control conflicts]
LOCKED DECISIONS: [wording, numbers, questions, or claims that must not change]
NONCLAIMS: [interpretations or conclusions the manuscript must not make]
TARGET / STAGE: [venue and developmental / substantive / integration / submission]
```

Use `developmental` for an outline or incomplete draft, `substantive` when the
core scientific content exists, `integration` for a complete draft and its
companion files, and `submission` only for the exact release package.

An editable source or DOCX is best for revision. A legible PDF is sufficient
for review-only work. Add standalone displays or supplements when they are not
fully readable in the manuscript. Provide source papers for exact citation
checks, code or data for reproducibility checks, and the current journal guide
for venue-specific formatting.

## More prompt examples

### Build an extended outline

```text
Use the academic-writing-skills skill to build an extended outline from the attached
materials. Establish the gap, research questions, methods, available evidence,
intended contribution, and nonclaims. For every planned paragraph, specify its
function, claim, authorized evidence, inference limit, and bridge. Do not draft
the full manuscript yet.
```

### Draft a section

```text
Use the academic-writing-skills skill to draft Section 2.3 from the approved outline
and supplied sources. Preserve all locked terms, numbers, and citations. Check
each paragraph's claim, evidence, development, and connection to adjacent text.
```

### Check terminology and flow

```text
Use the academic-writing-skills skill to revise this section for terminology
consistency, avoidable nontechnical repetition, stock phrasing, and paragraph
flow. Protect necessary technical repetition and do not change scientific
meaning, numbers, citations, or claim strength.
```

### Apply selected review comments

```text
Use the academic-writing-skills skill to implement review items 1, 3, and 5. Keep items
that require a missing source or author decision open, and propagate each
material change to every affected section, display, supplement, Abstract, and
Conclusion.
```

### Verify a revision round

```text
Use the paper-review skill to compare the current manuscript with the reviewer
comments, response letter, and prior version. Classify each issue as resolved,
partial, open, regressed, waived, new, or not verifiable. Do not treat the
response letter alone as proof that every affected file was updated.
```

### Check a submission package

```text
Use the paper-review skill at submission stage on the exact manuscript, supplement,
figures, tables, highlights, cover letter, declarations, and metadata. Identify
release blockers and mark the package SUBMISSION_READY only if the exact files
support that status.
```

## Review stages

| Stage | Purpose |
|---|---|
| Developmental | Structure, gap, questions, and planned evidence in an outline or incomplete draft |
| Substantive | Scientific validity, methods, evidence, interpretation, and reproducibility |
| Integration | Cross-section and cross-file consistency in a complete draft |
| Submission | Release readiness of the exact files to be submitted |

## Automatic review modules

`paper-review` selects the smallest sufficient set of technical references
from the paper itself. Users do not need to choose modules manually.

Available coverage includes:

- equations, notation, and derived-display provenance;
- surveys, psychometrics, CFA, SEM, mediation, and multi-group comparison;
- simulation, ABM, ML, GenAI, LLMs, and synthetic respondents;
- water resources, coupled human-natural systems, policy, and uncertainty;
- flood risk, hydrodynamics, catastrophe modeling, exposure, vulnerability,
  and loss; and
- prior-comment and revision-round regression checks.

A keyword or study-area mention alone does not activate a module. An
Ethan-style or project-precedent overlay is used only when that context is
explicitly requested or confirmed.

## Long-running projects

One-off edits need no setup. Repeated, multi-file projects can initialize a
manuscript state:

```bash
python skills/academic-writing-skills/scripts/init_manuscript_state.py manuscript_state.json
```

The state records active artifacts, authority sources, locked wording, facts,
terminology, decisions, open issues, and release checks. It is not a memory of
every wording choice.

Useful diagnostics:

```bash
python skills/academic-writing-skills/scripts/audit_manuscript_state.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_text_consistency.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_prose_patterns.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_docx_structure.py manuscript.docx
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

These scripts surface candidates for contextual review; they do not determine
that prose was AI-generated or that a technical term is overused.

## Boundaries

- The skills do not invent assumptions, analyses, results, citations,
  mechanisms, thresholds, reviewer preferences, or metadata.
- Technical terms are protected from cosmetic synonym rotation.
- AI-like prose patterns are editing diagnostics, not proof of authorship.
- A response letter is not proof that a revision appears in every affected
  file.
- The plugin complements source verification, statistical software, reference
  managers, rendering, and tracked-change tools rather than replacing them.

## Testing

```bash
python -m pytest tests/ -q
python skills/academic-writing-skills/scripts/run_regression_tests.py
```
