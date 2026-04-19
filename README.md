# academic-writing-skills

A Claude Code skill for rigorous academic paper writing, revision, and submission.
Field-agnostic. Journal-specific rules and paper-specific exceptions live inside
each paper's own repository, so the skill itself stays general.

[繁體中文 README](./README.zh-TW.md)

## What it does

- Enforces **findings-first + mechanism** structure in every result paragraph
- Runs a **banned-word audit** catching GPT / overclaim / filler language
- Checks **figure-text consistency** (numbers in prose must appear on figures)
- Guides **per-section writing** (Abstract, Introduction, Methods, Results,
  Discussion, Conclusion)
- Requires **journal format confirmation** before writing any prose
- Provides a **pre-submission checklist** covering manuscript, cover letter,
  reviewer suggestions, data availability, figure specs, and post-submission
  housekeeping

## Install

Clone into the Claude Code skills directory. Replace `<your-fork>` with your
GitHub username or the upstream owner:

```bash
# User-level (all projects)
git clone https://github.com/<your-fork>/academic-writing-skills ~/.claude/skills/academic-writing-skills

# Project-level (this project only)
git clone https://github.com/<your-fork>/academic-writing-skills <project>/.claude/skills/academic-writing-skills
```

Claude Code auto-discovers skills from these paths; no further setup needed.

## Per-paper setup (one-time)

For each paper, create a `.paper/` folder in the paper's git repository:

```
<paper-repo>/
└── .paper/
    ├── journal_format.md      # Built from journal_format_template.md
    └── style_overrides.md     # Optional: paper-specific terminology, banned terms
```

On first use in a paper repo, the skill will:
1. Check for `.paper/journal_format.md`
2. If missing, walk you through filling
   `references/journal_format_template.md`
3. Save the completed file to `<paper-repo>/.paper/journal_format.md`

## Skill layout

```
academic-writing-skills/
├── SKILL.md                            # Entry point + workflow
├── references/
│   ├── writing_principles.md           # 7 core principles
│   ├── banned_words.md                 # GPT / overclaim / filler detection
│   ├── figure_conventions.md           # Figure-text coupling + cross-figure rules
│   ├── section_checklists.md           # Per-section writing checks
│   ├── submission_checklist.md         # Pre-submission audit
│   └── journal_format_template.md      # Template for .paper/journal_format.md
└── README.md
```

## Workflow

On any paper-writing request, the skill runs this workflow:

1. **Confirm journal format** — load `<paper-repo>/.paper/journal_format.md`
   or ask the user to fill the template.
2. **Load paper-specific overrides** — apply any rules in
   `<paper-repo>/.paper/style_overrides.md` (takes precedence over skill defaults).
3. **Load universal rules** — `writing_principles.md` and `banned_words.md`.
4. **Load task-specific references** — section checklists, figure conventions,
   or submission checklist as appropriate.
5. **Self-audit before output** — verify mechanism, check banned words, confirm
   numbers match figures, check sentence-level transitions.

## What's NOT in the skill

- **Specific journal libraries** — each user maintains their own in their paper
  repos, because journal choice varies by field and user.
- **Field-specific terminology preferences** — paper-specific
  `style_overrides.md` handles these.
- **Personal voice or tone rules** — these belong in user-level CLAUDE.md.

## Philosophy

- **Rigor without style enforcement**: the skill flags violations of universal
  rigor (overclaim, no mechanism, figure-text mismatch) but does not impose a
  specific prose style.
- **Journal-first, prose-second**: format compliance is confirmed before any
  writing starts.
- **Paper sovereignty**: each paper's `.paper/` folder owns its overrides. The
  skill never silently applies its own preferences when a paper has stated
  otherwise.

## License

MIT
