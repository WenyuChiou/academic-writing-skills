# Academic Writing Skills

[![plugin version](https://img.shields.io/badge/plugin-v1.3.18-blue.svg)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

Part of [ai-research-skills](https://github.com/WenyuChiou/ai-research-skills).

Plan a paper's research focus and argument architecture, write connected paragraphs, and review the full manuscript.

Use with **Codex**, **Claude Code**, **OpenCode**, **Hermes Agent**, and other AI agents that support the Agent Skills format. Available tools and integrations depend on the host.

[繁體中文](./README.zh-TW.md)

![Workflow: Frame and Outline, Plan and Write, Check and Revise, Section Review, and Full-Paper Review; one shared terminology record supports every stage.](./docs/images/workflow-cover.png)

## What you can do

One plugin provides two skills:

- [academic-writing-skills](./skills/academic-writing-skills/SKILL.md): plan, draft, revise, and coordinate manuscript changes.
- [paper-review](./skills/paper-review/SKILL.md): assess the manuscript and report located findings; review-only by default.

| Task | What it helps you produce |
|---|---|
| Frame & outline | A research focus, gap, questions, evidence boundaries, and an extended outline. |
| Plan & write | Paragraph plans and drafts with clear links between ideas. |
| Check & revise | Checks of meaning, terminology, evidence, flow, citations, and affected figures or tables. |
| Review | Section reviews and four-pass critiques of the whole manuscript. |
| Coordinate revisions | Aligned manuscript, supplement, figures, tables, reviewer responses, and submission files. |

## From research architecture to submission

Plan each paragraph's point, evidence, and links before writing; recheck the revised text afterward. At section closure, review the argument across paragraphs.

Full-paper review reads top-to-bottom in four passes: **argument and structure; evidence and scope; scholarly writing; delivery integrity**. Check alignment top-down, from questions to evidence, and bottom-up, from evidence to conclusions. Revisit affected sections when a material issue is found.

**One shared terminology record runs throughout.** For sustained work, reuse the paper's definitions, preferred terms, and allowed variants. Read confirmed entries before writing and record agreed updates. Proposed names remain separate until the author confirms them.

Checks scale to the task. A local grammar edit does not trigger every stage or require a new management file. Cross-file changes also reopen affected summaries, references, and supplements.

## Install and use

For Claude Code, install through the ai-research-skills marketplace:

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

Update with `claude plugin update academic-writing-skills@ai-research-skills`.

For Codex or ChatGPT, use the available skill/plugin interface. For other Agent Skills clients, copy both folders under `skills/` into a supported directory: `.agents/skills/` or `.opencode/skills/` for OpenCode, or `~/.hermes/skills/` for Hermes Agent.

## Try it

Attach the active text and sources. Add figures, tables, the supplement, review comments, or venue guidance only when relevant. Use the skill names in ordinary language.

### Frame a paper and build an outline

```text
Use the academic-writing-skills skill to frame this paper and build an extended outline.
Identify the gap, questions, evidence, and each paragraph's purpose.
Do not draft the manuscript yet.
```

### Plan and draft a section

```text
Use the academic-writing-skills skill to plan this section, then draft it paragraph by paragraph.
Before each paragraph, state its point, evidence, inference limits, and connection to adjacent text.
After writing, recheck meaning, terminology, and flow.
```

### Check a paragraph

```text
Use the academic-writing-skills skill to check this paragraph's definitions, terminology, flow, and repetition.
Preserve established technical terms and scientific meaning.
Report missing evidence instead of inventing it.
```

### Review the whole paper

```text
Use the paper-review skill to review this manuscript and supplement in four passes:
argument and structure; evidence and scope; scholarly writing; delivery integrity.
Locate each finding and explain its evidence and consequence. Do not edit the files.
```

### Align a reviewer response

```text
Use the academic-writing-skills skill to align this response with the latest manuscript and supplement.
Preserve accurate author wording. Flag unmet promises and unverified cross-references.
Do not claim a change is complete unless the relevant files support it.
```

## Boundaries and further reading

Review modules adapt to the study, including equations, psychometrics/SEM, AI/LLM, water, and flood models. These skills support source verification and author judgment; they do not replace them. Missing results or sources remain unverified, not invented.

- [Full usage guide](./docs/USER_GUIDE.md): inputs, more prompts, review stages, and project records.
- [Display examples](./skills/academic-writing-skills/references/figures-tables-and-supplements.md): figures, captions, tables, and supplements.
- [Venue and citation guidance](./skills/academic-writing-skills/references/overlay-contract.md).
- [Release history](./CHANGELOG.md).

## License

[MIT](./LICENSE)
