---
name: academic-writing-skills
description: End-to-end academic manuscript workflow for drafting, revision, reviewer response, figure-text consistency, claim-evidence audits, and pre-submission checks. Use this skill whenever a user asks for manuscript sections, paper revision, rebuttal letters, journal compliance, overclaim detection, GPT-style prose cleanup, figure captions, or evidence-backed academic writing. It is especially useful for multi-section papers where context, claims, figures, and reviewer comments must stay consistent across revisions.
---

# Academic Writing Skills

Field-agnostic workflow for rigorous academic paper writing, revision, rebuttal,
and submission preparation.

The skill is intentionally general. Journal-specific rules, advisor preferences,
paper terminology, evidence maps, and figure inventories belong in each paper
repository under `.paper/`.

## When To Use

Use this skill for:

- Drafting or revising Abstract, Introduction, Methods, Results, Discussion,
  Conclusion, cover letter, or reviewer response.
- Auditing overclaim, GPT-style prose, vague mechanism language, or unsupported
  conclusions.
- Checking whether claims are backed by figures, tables, statistics, code output,
  or cited literature.
- Verifying figure captions, panel references, numerical consistency, and
  figure-text coupling.
- Preparing a paper for journal submission or resubmission.
- Compressing paper context so future LLM sessions do not reread the whole
  manuscript repeatedly.

Do not use this skill for generic literature workspace management, Zotero CRUD,
Obsidian vault setup, NotebookLM source curation, or coding tasks. Those belong
to separate research-workspace or coding-agent skills.

## Required Workflow

Before producing substantive manuscript prose, follow this sequence.

### 1. Classify The Task

Identify the requested artifact:

- New prose: section draft, paragraph rewrite, abstract, cover letter.
- Diagnostic audit: overclaim, banned words, claim-evidence, figure consistency.
- Revision: advisor comments, reviewer comments, response table.
- Submission: journal checklist, declarations, file inventory.
- Context compression: `.paper/` packet or paper memory update.

For small copyediting tasks, use the fast path in Step 3 and avoid asking for
unneeded setup.

### 2. Locate The Paper Repository

Use the current working directory unless the user gives another path. Look for:

```text
<paper-repo>/
  .paper/
    journal_format.md
    style_overrides.md
    context.md
    figure_inventory.md
    claim_evidence_ledger.md
    reviewer_comments.md
    submissions_log.md
```

If `.paper/` does not exist and the task is multi-section, submission-facing, or
reviewer-facing, offer to create a minimal paper context packet using
`references/paper_context_packet.md`.

### 3. Confirm Journal Format

Look for `<paper-repo>/.paper/journal_format.md`.

- If present, load it and apply its word limits, citation style, section order,
  figure specs, declarations, and submission rules.
- If missing and the task is format-sensitive, stop and ask for the target
  journal. Use `references/journal_format_template.md` to create the file.
- If missing and the task is small, proceed without journal setup and state that
  journal compliance was not checked.

Format-sensitive tasks include abstract word limits, cover letters, section
order, figure-count audits, declarations, reviewer suggestions, and submission
preparation.

### 4. Load Paper-Specific Overrides

If `<paper-repo>/.paper/style_overrides.md` exists, apply it after the universal
rules. It can override banned terms, allowed terms, terminology preferences,
figure conventions, and advisor-specific instructions.

If `<paper-repo>/.paper/context.md` exists, use it as the preferred compressed
source of paper context before reading the full manuscript.

If `<paper-repo>/.paper/claims.yml` or `<paper-repo>/.paper/figures.yml` exist
(produced by the `paper-memory-builder` skill), prefer them over re-reading the
manuscript when running claim-evidence audits, figure-text consistency checks,
or banned-word audits — the YAML is the authoritative shared memory layer
across writing sessions. Refresh the YAML via `paper-memory-builder` if the
manuscript has changed since the YAML was last written.

### 5. Load Universal Rules

Always load:

- `references/writing_principles.md`
- `references/banned_words.md`

These define findings-first structure, mechanism requirements, overclaim
language, GPT-style vocabulary, causal-claim checks, and revision discipline.

### 6. Load Task-Specific References

| Task | Load |
|---|---|
| Drafting or editing a manuscript section | `references/section_checklists.md` |
| Figure, caption, panel, or number consistency | `references/figure_conventions.md` |
| Claim support, overclaim, abstract/conclusion audit | `references/claim_evidence_audit.md` |
| Reviewer response or rebuttal letter | `references/reviewer_response_workflow.md` |
| Submission or resubmission prep | `references/submission_checklist.md` |
| Creating or refreshing `.paper/` memory | `references/paper_context_packet.md` |

Read only the relevant subsection when possible. The goal is to save context,
not load every reference by default.

### 7. Produce The Artifact

Use the output structure that fits the task:

- For prose: revised text first, then a short audit note if useful.
- For audits: findings table, severity, evidence, recommended fix.
- For reviewer response: point-by-point table with comment, response, manuscript
  change, and evidence.
- For submission: checklist with pass, fail, unknown, and required action.
- For context compression: concise `.paper/` files that future sessions can load
  instead of the full paper.

When revising existing text, change only what the task requires. Preserve the
author's voice unless the sentence violates a rigor rule.

### 8. Self-Audit Before Showing The User

Before returning prose or an audit result, check:

1. Does every result state the finding before the figure citation?
2. Does every finding have a mechanism grounded in data, method, or literature?
3. Are overclaim verbs and vague intensifiers removed or hedged?
4. Does every precise number in prose trace to a figure, table, code output, or
   citation?
5. Are figure references panel-specific when panels exist?
6. Do reviewer responses point to a real manuscript change?
7. Does journal format override any default rule?

If any item fails, fix it before showing the user.

## Paper Context Packet

Use `.paper/` files to reduce repeated token use across sessions. A mature paper
repository should contain:

```text
.paper/
  journal_format.md
  style_overrides.md
  context.md
  figure_inventory.md
  claim_evidence_ledger.md
  reviewer_comments.md
  submissions_log.md
```

`context.md`, `figure_inventory.md`, and `claim_evidence_ledger.md` are the most
important token-saving files. They let future agents understand the paper's
research question, claims, figures, and evidence without rereading the full
manuscript.

## Core Principles

- Findings first, then mechanism.
- Claims must be traceable to evidence.
- Figure text, captions, and prose must agree.
- Journal rules override generic preferences.
- Paper-specific overrides beat skill defaults.
- Reviewer response is a change-management task, not a politeness exercise.
- Preserve scientific uncertainty; do not invent assumptions or results.
- Prefer concise, evidence-backed prose over generic academic polish.
