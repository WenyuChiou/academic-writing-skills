# Academic Writing Skills

Evidence-safe academic writing and scientific review for Claude Code,
ChatGPT, and Codex.

[繁體中文](./README.zh-TW.md)

This plugin includes two complementary skills:

| What you want to do | Use |
|---|---|
| Plan, draft, revise, or polish a manuscript | [`$academic-writing-skills`](./skills/academic-writing-skills/SKILL.md) |
| Critique a paper without editing it | [`$paper-review`](./skills/paper-review/SKILL.md) |

`$paper-review` finds and prioritizes problems. Use
`$academic-writing-skills` when you want those changes applied.

## Install

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

One installation provides both skills. To update later:

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

## Quick start

1. Attach the current manuscript or section.
2. Add any relevant figures, tables, supplement, reviewer comments, or prior
   version.
3. State what you want and copy one of the prompts below.

The examples use Claude Code's `$skill-name` form. In ChatGPT or Codex, use
`@skill-name` if the skills are installed there.

### Write or revise

```text
Use $academic-writing-skills to revise the attached section. Preserve the
scientific meaning, numbers, citations, and key terminology. Flag anything
that requires new evidence or an author decision instead of guessing.
```

### Review a manuscript

```text
Use $paper-review to review the attached manuscript and supplement. Rank the
issues by scientific and reproducibility risk, anchor each comment to the
paper, and do not edit the files.
```

## What the skills check

- Whether claims are supported by the available evidence.
- Whether Methods, Results, Discussion, Abstract, figures, tables, and
  supplement remain consistent.
- Whether terminology, repetition, and paragraph flow are controlled without
  changing scientific meaning.
- Whether method- and domain-specific risks need attention. Relevant review
  modules are selected automatically.

The skills do not invent missing results, citations, assumptions, or reviewer
preferences. Missing evidence is reported as a limitation.

## More help

- [Full usage guide](./docs/USER_GUIDE.md)
- [Release history](./CHANGELOG.md)

Part of the
[agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh).

## License

MIT
