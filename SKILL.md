---
name: academic-writing-skills
description: End-to-end manuscript and submission workflow for academic papers. Trigger for full-paper writing, revising against reviewer comments, rebuttal letters, pre-submission audits, multi-section drafting, or figure-text consistency audits. Also for GPT-style / overclaim language detection across a manuscript. Defer to `abstract-writer` for abstract-only rewrites and `professor-yang-review` for critique-only passes. Enforces findings-first structure, mechanism-for-every-result, banned-word audit, figure-text consistency, and per-journal format compliance.
---

# Academic Writing Skills — Paper Writing & Submission Toolkit

A general, field-agnostic skill for rigorous academic paper writing. The skill itself
stays universal; journal-specific rules and paper-specific exceptions live inside each
paper's own repository under `<paper-repo>/.paper/`.

## When to Use

Activate on any of:
- Writing or editing paper sections
- Revising against reviewer/advisor comments
- Checking a draft against journal format
- Pre-submission audit
- Critiquing prose for academic rigor, overclaim, or GPT-style writing
- Adjusting figures or captions

## Mandatory Workflow

Before producing ANY paper prose, execute these steps in order:

### Step 1. Confirm Journal Format

Look for `<paper-repo>/.paper/journal_format.md` (the paper repo is the user's
working directory, or an explicitly specified path).

- **Present** → load it and apply all format rules (word limits, citation style,
  required sections, figure specs). Cite them back to the user so both sides agree
  on the contract before writing.
- **Missing, and task is format-sensitive** (word-count-bound writing, section
  structure, figure-count audit, submission prep) → stop. Ask the user which
  journal, then walk through `references/journal_format_template.md` to create it.
- **Missing, and task is small** (single-sentence polish, banned-word audit,
  transition fix, typo pass, one-paragraph critique) → **fast-path: skip format
  confirmation** and proceed directly to Steps 3–5. The user can fill the template
  later when a format-sensitive task comes up.

### Step 2. Load Paper-Specific Overrides

Look for `<paper-repo>/.paper/style_overrides.md`. If present, its rules
**take precedence** over any universal rule in this skill (e.g., a banned term
the paper allows, or an extra banned term specific to this paper).

### Step 3. Load Universal Rules

Always load:
- `references/writing_principles.md` — 7 core principles
- `references/banned_words.md` — GPT / overclaim / filler detection

### Step 4. Load Task-Specific References

| Task | Load |
|------|------|
| Drafting or editing any section | `references/section_checklists.md` (jump to the relevant section) |
| Working on a figure, caption, or figure-related prose | `references/figure_conventions.md` |
| Writing or rewriting an abstract | `references/section_checklists.md#abstract` (6-part structure) |
| Responding to reviewer comments | `references/section_checklists.md#reviewer-response` |
| Preparing for submission | `references/submission_checklist.md` |

### Step 5. Self-Audit Before Showing User

After producing any paragraph or block, run an internal audit:
1. Does every result have a mechanism explanation? (If not, add one.)
2. Do any sentences contain banned words from `banned_words.md`?
3. Does every figure/table citation match a real panel?
4. Do the numbers in the prose match the numbers in the referenced figure?
5. Does each sentence connect clearly to the previous one?

Only show the user after these pass.

## Paper-Repo Conventions

The skill expects each paper's repository to contain:

```
<paper-repo>/
└── .paper/
    ├── journal_format.md      # Built from journal_format_template.md on first use
    └── style_overrides.md     # Optional: paper-specific terminology, banned terms
```

When starting work on a new paper, offer to create the `.paper/` folder and walk
the user through filling the template.

## Reference Files

All reference files live under `references/`:

| File | Contains |
|------|----------|
| `writing_principles.md` | 7 core principles — structure, precision, mechanism, word choice, figures, redundancy, process |
| `banned_words.md` | Banned single words (by part of speech), banned phrases, banned sentence starters, banned patterns, detection heuristics |
| `figure_conventions.md` | Figure-text coupling, cross-figure label consistency, define-once rule, annotation style, field-specific conventions |
| `section_checklists.md` | Per-section checks: Abstract, Introduction, Methods, Results, Discussion, Conclusion, Reviewer Response |
| `submission_checklist.md` | Pre-submission audit: manuscript, cover letter, suggested reviewers, data availability, figure quality, references |
| `journal_format_template.md` | Template the user fills in once per target journal; saved to `<paper-repo>/.paper/journal_format.md` |
| `style_overrides_example.md` | Example of a filled `style_overrides.md` a user can copy into their paper repo |

## Operating Notes

- **Findings-first principle always**: state the result first, then the mechanism.
  Never open a results paragraph with "Figure X shows...".
- **Mechanism for every result**: if the reader can still ask "why?" after a finding,
  the paragraph is incomplete.
- **Match the user's voice**: the skill enforces rigor, not a specific prose style.
  Keep the user's sentence cadence and technical vocabulary unless it violates a rule.
- **Report violations concisely**: when flagging, quote the exact phrase + the rule
  violated + a specific replacement. Do not lecture.
- **Track-change mindset for revisions**: when revising existing prose, change only
  what the comment or audit requires. Do not rewrite clean paragraphs.
