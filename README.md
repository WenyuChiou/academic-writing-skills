# Academic Writing Skills

[![tests](https://github.com/WenyuChiou/academic-writing-skills/actions/workflows/test.yml/badge.svg)](https://github.com/WenyuChiou/academic-writing-skills/actions/workflows/test.yml)
[![plugin version](https://img.shields.io/badge/plugin-v1.1.2-blue.svg)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

**Develop and review a manuscript as one connected evidence system—from
argument architecture and the extended outline to drafting, full-manuscript
review, revision, and final submission.**

Built on the open Agent Skills format. Designed for Claude Code, ChatGPT,
Codex, OpenCode, Hermes Agent, and other skills-compatible agents.
[繁體中文](./README.zh-TW.md)

## From research architecture to submission

A general-purpose AI can improve one paragraph while missing what changed
elsewhere in the paper. These skills manage the complete manuscript lifecycle:

`Research framing → Argument architecture → Extended outline → Evidence-led
drafting → Bidirectional alignment → Full-manuscript review → Revision →
Submission verification`

| Stage | What the workflow does |
|---|---|
| Research framing and architecture | Clarifies the problem, gap, questions, intended contribution, evidence boundaries, and nonclaims. |
| Extended outline | Assigns every planned paragraph a reader function, defensible claim, authorized evidence, inference limit, and bridge. |
| Evidence-led drafting | Develops Methods, Results, Discussion, Conclusion, Abstract, and other artifacts from approved sources and current results. |
| Bidirectional integrity | Checks top-down alignment from purpose to evidence and bottom-up alignment from evidence to contribution. |
| Full top-to-bottom review | Reads the complete manuscript in four distinct passes: argument and structure; evidence and scope; scholarly writing and flow; delivery integrity. |
| Revision and release | Propagates material changes across sections, figures, tables, supplements, metadata, and the exact submission package. |

Top-down review follows the gap or purpose through the questions, methods,
evidence, and conclusions. Bottom-up review starts from source evidence and
tests whether each result, interpretation, contribution, and summary claim is
actually supported.

## Two skills, one manuscript system

| Skill | Use it when... |
|---|---|
| [`academic-writing-skills`](./skills/academic-writing-skills/SKILL.md) | You want to frame, outline, draft, revise, synchronize, or prepare a manuscript and its companion files for submission. |
| [`paper-review`](./skills/paper-review/SKILL.md) | You want an evidence-safe reviewer critique, revision-round check, or submission audit without editing the manuscript. |

`paper-review` is review-only by default. After choosing which comments to
apply, use `academic-writing-skills` to make the revisions and propagate their
effects through the manuscript system.

## Install and use

The prompts below are platform-neutral: name the skill in ordinary language.
Compatible agents may also activate it automatically or offer their own skill
selector or shortcut.

| Client | Skill support |
|---|---|
| Claude Code | Install the plugin through the marketplace commands below. |
| ChatGPT and Codex | Use the installed skill or plugin through the available Skills interface; both support the open Agent Skills format. |
| OpenCode | Place the two skill folders in `.agents/skills/`, `.opencode/skills/`, or another supported skill directory. |
| Hermes Agent | Place them in `~/.hermes/skills/` or configure the repository's `skills/` folder as an external skill directory. |

For Claude Code:

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

One installation provides both skills. To update later:

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

For Codex, OpenCode, Hermes Agent, or another Agent Skills client, clone this
repository and copy or link both folders under `skills/` into a directory the
client scans. A shared `.agents/skills/` directory can serve Codex and
OpenCode; Hermes Agent can also scan that directory when configured as an
external source.

## Try it

Attach the exact active manuscript, section, or outline. Add figures, tables,
supplements, reviewer comments, prior versions, or venue guidance when they
control the task.

### Develop an extended outline

```text
Use the academic-writing-skills skill to develop an extended outline from the
attached materials. Establish the gap, research questions, planned evidence,
intended contribution, and nonclaims. Give every planned paragraph a function,
claim, authorized evidence, inference limit, and bridge. Do not draft the full
manuscript yet.
```

### Review the complete manuscript

```text
Use the paper-review skill to conduct a four-pass top-to-bottom review of the
attached manuscript and supplement: argument and structure; evidence and scope;
scholarly writing and flow; and delivery integrity. Rank issues by scientific
and reproducibility risk, anchor each comment to the files, and do not edit
them.
```

## What it protects

- Question-to-evidence alignment from research architecture through the final
  summaries.
- Scientific meaning, locked decisions, claim scope, and explicit nonclaims.
- Consistency across the manuscript, Abstract, figures, tables, supplements,
  reviewer responses, metadata, and submission files.
- Terminology, necessary versus avoidable repetition, paragraph flow, and
  stock phrasing without cosmetic synonym swapping.
- Relevant technical risks in equations and derived displays, surveys and
  psychometrics/SEM, simulations and AI/LLM studies, water and flood models,
  and revision rounds.

Missing results, citations, assumptions, and reviewer preferences are reported
as limitations; they are never invented.

## Learn more

- [Full usage guide](./docs/USER_GUIDE.md) — task inputs, more platform-neutral
  prompts, review stages, technical modules, and long-running project support.
- [Release history](./CHANGELOG.md)

Part of the
[agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh).

## License

[MIT](./LICENSE)
