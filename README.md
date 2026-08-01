# academic-writing-skills

A Claude/Codex plugin for lifecycle-aware academic manuscript work. Version
1.0 contains two composable skills:

- `academic-writing-skills`: the cross-disciplinary manuscript-integrity core
- `paper-review`: an evidence-safe Ethan-style overlay for water resources,
  coupled natural-human systems, ABM, flood and catastrophe modeling,
  hydrodynamics, uncertainty, and LLM studies

[Traditional Chinese README](./README.zh-TW.md)

> Part of the [agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh).

## What changed in 1.0

The plugin now treats a manuscript as an evolving evidence system rather than a
collection of isolated passages. It distinguishes:

- lightweight edits from managed, multi-artifact manuscript projects
- writing sequence from evidence dependency and review maturity
- universal integrity rules from study-design, domain, reviewer, venue, and
  project overlays
- supported findings from interpretations, mechanisms, and speculation
- a working draft from an exact, verified release candidate

Every review or revision ends with a functional-completeness retrospective.
High-severity validity, ethics, metadata, or release issues block
`SUBMISSION_READY`.

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

The plugin exposes both `$academic-writing-skills` and `$paper-review`.

## Use the core skill

Use `$academic-writing-skills` for planning, drafting, reviewing, revising,
proofreading, cross-file synchronization, or submission readiness. It supports
empirical, qualitative, computational, AI/LLM, review, theoretical, framework,
methods, and data papers without forcing every manuscript into IMRAD.

For a full manuscript or long-running project, initialize a project state:

```bash
python skills/academic-writing-skills/scripts/init_manuscript_state.py \
  manuscript_state.json
```

The state records active artifacts, authority sources, locked wording, facts,
question-to-evidence alignment, design dimensions, decisions, open issues, and
release checks. Keep it with the manuscript project, not inside the installed
skill.

Useful deterministic diagnostics include:

```bash
python skills/academic-writing-skills/scripts/audit_manuscript_state.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_text_consistency.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_docx_structure.py manuscript.docx
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

These scripts report evidence; they do not replace substantive scholarly
judgment.

## Use the review overlay

Use `$paper-review` only for a relevant Ethan-style internal review. It loads
the core skill first, then adds only the applicable water, CNHS, ABM,
flood/hydrodynamic, uncertainty, or AI module.

The overlay:

- labels comments as `MUST`, `SHOULD`, `QUERY`, or `PREFERENCE`
- uses an explicit R1-R4 label when supplied, otherwise maturity labels
- does not impersonate Prof. Ethan Yang
- does not infer AI authorship from prose
- does not invent a mechanism merely because a review asks “why”
- loads named project precedents only after the exact project is established

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

## Testing

```bash
python -m pytest tests/ -q
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

The tests check package structure, frontmatter, reference routing, project-state
schema, deterministic regressions, overlay isolation, and common encoding
corruption.

## Scope

The plugin does not invent scientific assumptions, analyses, results,
citations, mechanisms, or metadata. It also does not replace Zotero,
NotebookLM, document rendering, or format-specific tracked-change tooling.

## License

MIT
