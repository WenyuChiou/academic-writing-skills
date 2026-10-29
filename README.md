# Academic Writing Skills

[![plugin version](https://img.shields.io/badge/plugin-v1.4.0-blue.svg)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

Part of [ai-research-skills](https://github.com/WenyuChiou/ai-research-skills).

Develop a research argument, write connected paragraphs, and check what the current evidence supports—from an outline to a revision package.

Use with **Codex**, **Claude Code**, **OpenCode**, **Hermes Agent**, and other AI agents that support the Agent Skills format. Available tools and integrations depend on the host.

[繁體中文](./README.zh-TW.md) | [简体中文](./README.zh-CN.md)

![Academic writing workflow: Ground, Develop, Draft, Review, and Revise, with evidence linked to the manuscript and a revision loop back to development and drafting.](./docs/images/workflow-cover.png)

*Cover illustration created with ChatGPT’s built-in image generation (raster PNG).*

## What you can do

One plugin provides two capabilities, with English, Traditional Chinese and Simplified Chinese entries:

- [academic-writing-skills](./skills/academic-writing-skills/SKILL.md): plan, draft, revise, and coordinate manuscript changes.
- [paper-review](./skills/paper-review/SKILL.md): assess the manuscript and report located findings; review-only by default.

| Capability | English | 繁體中文 | 简体中文 |
|---|---|---|---|
| Plan, draft and revise | [academic-writing-skills](./skills/academic-writing-skills/SKILL.md) | [academic-writing-skills-zh-tw](./skills/academic-writing-skills-zh-tw/SKILL.md) | [academic-writing-skills-zh-cn](./skills/academic-writing-skills-zh-cn/SKILL.md) |
| Review without editing by default | [paper-review](./skills/paper-review/SKILL.md) | [paper-review-zh-tw](./skills/paper-review-zh-tw/SKILL.md) | [paper-review-zh-cn](./skills/paper-review-zh-cn/SKILL.md) |

Choose one language entry per capability; do not load all three for the same task.
For manual installs, a review entry also needs the writing entry in the same language.
The Chinese entries translate the guidance, not the manuscript automatically.
Keep the author's requested output language, confirmed terminology and scope.
Executable helpers, schemas and English editing examples retain their original form.
English word-pattern audits remain English-language checks, not a Chinese grammar checker.

| Scope | Provide | Receive |
|---|---|---|
| One passage | Current text, relevant neighbors/sources and wording to preserve | A bounded proposal or edit, located checks and unresolved evidence needs |
| One section | Current purpose/outline, evidence and paragraph roles | A function plan, connected prose or a scoped review—not a whole-paper rewrite |
| Whole paper or revision package | Exact active manuscript and relevant companion files | Four-pass findings, affected cross-file checks and explicit unverified items |

### Coverage and guide selection

The writing skill selects the relevant guide from the request and manuscript;
you do not need to load every section or choose technical modules manually.

| Work | Relevant guidance |
|---|---|
| Framing, outline, Introduction and study context | [Lifecycle](./skills/academic-writing-skills/references/lifecycle-and-routing.md) and [Introduction/context](./skills/academic-writing-skills/references/introduction-and-study-context.md) |
| Methods, data and assumptions | [Methods and assumptions](./skills/academic-writing-skills/references/methods-and-assumptions.md) |
| Results, Discussion and Limitations | [Results](./skills/academic-writing-skills/references/results-and-explanation.md) and [Discussion/limitations](./skills/academic-writing-skills/references/discussion-and-limitations.md) |
| Conclusion and Abstract | [Study identity, synthesis and compression](./skills/academic-writing-skills/references/conclusion-and-abstract.md) |
| Figures, tables, SM and references | [Displays/SM](./skills/academic-writing-skills/references/figures-tables-and-supplements.md) and [prose/citations](./skills/academic-writing-skills/references/prose-and-citation-editing.md) |
| Reviewer response and revision alignment | [Response workflow](./skills/academic-writing-skills/references/reviewer-response-workflow.md) |

## From research architecture to submission

The workflow is **Frame & outline → Plan & write → Check & revise**. Develop the argument architecture from the paper's purpose and evidence, then check the actual prose—not only a plan or language scan. Distinguish the goal from the methods used to pursue it. Section reviews check the argument across paragraphs; comment-driven reviews distinguish a completed edit from an answered concern.

Full-paper review reads top-to-bottom in four passes: **argument and structure; evidence and scope; scholarly writing; delivery integrity**. Check alignment top-down, from questions to evidence, and bottom-up, from evidence to conclusions. Revisit affected sections when a material issue is found.

**One shared terminology record runs throughout.** For sustained work, reuse the paper's definitions, preferred terms, and allowed variants. Read confirmed entries before writing and record agreed updates. Proposed names remain separate until the author confirms them.

Checks scale to the task. A local grammar edit does not trigger every stage or require a new management file. Cross-file changes also reopen affected summaries, references, and supplements.

## Install and use

**Install version:** the four Chinese entries are included in this source tree.
The marketplace tracks `main`; check the installed plugin version after updating.
GitHub releases, catalog metadata and local caches are updated separately.
For a manual install, copy the selected skill folder into the host's supported
skill directory; keep its references, scripts and assets together.

For Claude Code, install through the ai-research-skills marketplace:

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

Update with `claude plugin update academic-writing-skills@ai-research-skills`.

For Codex or ChatGPT, use the available skill/plugin interface. For other Agent Skills clients, copy the selected capability/language folders under `skills/` into a supported directory: `.agents/skills/` or `.opencode/skills/` for OpenCode, or `~/.hermes/skills/` for Hermes Agent.

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

### Revise one paragraph

```text
Use the academic-writing-skills skill to revise only this paragraph.
Use the supplied Introduction/outline when needed to preserve the research goal,
comparisons and scope. Keep clear author wording and established technical terms.
Check the exact revision for meaning and flow; identify missing evidence.
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
