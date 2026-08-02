# Academic Writing Skills

[![tests](https://github.com/WenyuChiou/academic-writing-skills/actions/workflows/test.yml/badge.svg)](https://github.com/WenyuChiou/academic-writing-skills/actions/workflows/test.yml)
[![plugin version](https://img.shields.io/badge/plugin-v1.1.1-blue.svg)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

**Keep a manuscript's questions, evidence, claims, and wording aligned from
the first outline to the final submission.**

For Claude Code, ChatGPT, and Codex. [繁體中文](./README.zh-TW.md)

## Why use these skills?

A general-purpose AI can improve one paragraph while missing what changed
elsewhere in the paper. That can leave you with:

- claims stronger than the results support;
- terminology, numbers, or conclusions that drift across sections and files;
- reviewer comments marked as resolved when the requested change is absent;
- polished prose hiding a broken link between the question, method, result,
  and conclusion.

These skills treat the manuscript as a connected evidence system. They
protect author decisions, flag missing evidence instead of guessing, and
progressively select only the method and domain checks relevant to the paper.

## Two skills, one workflow

`Plan → Draft → Review → Revise → Verify`

| Skill | Use it when... |
|---|---|
| [`$academic-writing-skills`](./skills/academic-writing-skills/SKILL.md) | You want to plan, outline, draft, revise, synchronize, or prepare a manuscript for submission. |
| [`$paper-review`](./skills/paper-review/SKILL.md) | You want a reviewer-style critique, revision-round check, or submission audit without editing the manuscript. |

`$paper-review` is review-only by default. After choosing which comments to
apply, use `$academic-writing-skills` to make and propagate the changes.

## Install

In Claude Code:

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

One installation provides both skills. To update later:

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

In ChatGPT or Codex, use `@academic-writing-skills` or `@paper-review` if the
skills are installed there.

## Try it

Attach the exact manuscript or section you want to use. Add figures, tables,
supplements, reviewer comments, or a prior version when they matter.

### Write or revise

```text
Use $academic-writing-skills to revise the attached section. Preserve the
scientific meaning, numbers, citations, and key terminology. Flag anything
that needs new evidence or an author decision instead of guessing.
```

### Review a manuscript

```text
Use $paper-review to review the attached manuscript and supplement. Rank the
issues by scientific and reproducibility risk, anchor each comment to the
paper, and do not edit the files.
```

## What it checks

- Claim-to-evidence alignment from research questions through conclusions.
- Consistency across the manuscript, Abstract, figures, tables, supplements,
  and submission materials.
- Terminology, repetition, paragraph flow, and stock phrasing without cosmetic
  synonym swapping.
- Relevant technical risks in equations and derived displays, surveys and
  psychometrics/SEM, simulations and AI/LLM studies, water and flood models,
  and revision rounds.

Missing results, citations, assumptions, and reviewer preferences are reported
as limitations; they are never invented.

## Learn more

- [Full usage guide](./docs/USER_GUIDE.md) — more prompts, input templates,
  review stages, and long-running project support.
- [Release history](./CHANGELOG.md)

Part of the
[agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh).

## License

[MIT](./LICENSE)
