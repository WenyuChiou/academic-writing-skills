# academic-writing-skills

A shareable Claude/Codex skill for rigorous academic paper writing, revision,
reviewer response, figure-text consistency, and pre-submission audits.

[Traditional Chinese README](./README.zh-TW.md)

## Purpose

This skill helps researchers turn manuscript work into a repeatable workflow:

- Draft sections with findings-first structure.
- Rewrite results and discussion paragraphs with explicit mechanisms.
- Detect GPT-style prose, vague intensifiers, and overclaim language.
- Check whether claims are backed by figures, tables, statistics, code output,
  or literature.
- Keep numbers, figure panels, captions, and prose consistent.
- Build point-by-point reviewer response tables.
- Prepare journal submission checklists and declaration items.
- Create `.paper/` context files so future AI sessions use fewer tokens.

The skill is field-agnostic. Journal-specific rules and paper-specific
terminology live inside each paper repository.

## Install

Clone the repo into your Claude Code skills directory:

```bash
git clone https://github.com/WenyuChiou/academic-writing-skills ~/.claude/skills/academic-writing-skills
```

For a single project only:

```bash
git clone https://github.com/WenyuChiou/academic-writing-skills <project>/.claude/skills/academic-writing-skills
```

Claude Code discovers skills from these paths automatically.

## Per-Paper Setup

For each manuscript, create a `.paper/` folder in the paper repository:

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

Minimum setup:

1. Copy `references/journal_format_template.md` to
   `<paper-repo>/.paper/journal_format.md`.
2. Fill in target journal rules from current author guidelines.
3. Optionally copy `references/style_overrides_example.md` to
   `<paper-repo>/.paper/style_overrides.md`.
4. For long projects, create the context packet described in
   `references/paper_context_packet.md`.

## Skill Layout

```text
academic-writing-skills/
  SKILL.md
  references/
    banned_words.md
    claim_evidence_audit.md
    figure_conventions.md
    journal_format_template.md
    paper_context_packet.md
    reviewer_response_workflow.md
    section_checklists.md
    style_overrides_example.md
    submission_checklist.md
    writing_principles.md
  evals/
    evals.json
  tests/
    test_skill_integrity.py
```

## Typical Workflows

### Draft or revise a section

The skill loads journal format, paper overrides, writing principles, banned
words, and the relevant section checklist. It then rewrites with:

- finding before figure citation,
- mechanism after each result,
- precise terminology,
- no unsupported overclaim,
- panel-specific figure references when needed.

### Audit claims and evidence

The skill builds a claim-evidence ledger:

```text
claim -> evidence source -> allowed certainty -> missing check -> revision
```

This is useful before editing Abstract, Discussion, Conclusion, cover letter, or
reviewer response.

### Respond to reviewers

The skill converts comments into a response table:

```text
comment -> anchor text -> response -> manuscript change -> evidence
```

It avoids the common failure mode of saying "clarified" without a visible
manuscript change.

### Save tokens across AI sessions

For long manuscripts, the skill can maintain `.paper/context.md`,
`.paper/figure_inventory.md`, and `.paper/claim_evidence_ledger.md`. Future
sessions can read those concise files before opening the full manuscript.

## What This Skill Is Not

- It is not a Zotero manager.
- It is not an Obsidian or NotebookLM workspace skill.
- It is not a coding-agent delegation skill.
- It is not a generic grammar checker.
- It does not invent scientific assumptions, results, or citations.

## Testing

Run integrity tests with:

```bash
python -m pytest -q
```

The tests validate frontmatter, bundled references, eval prompts, and common
mojibake/encoding corruption markers.

## License

MIT
