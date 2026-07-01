# Customizing style_overrides.md For Your Advisor, Group, Or Journal

The universal rules in this skill are field-agnostic. Every research group,
advisor, and target journal has its own house style on top of them. This file
shows how to capture that house style in a `.paper/style_overrides.md`, so the
skill audits your manuscript against your own standard instead of a generic
one. Copy the blocks you need into `<paper-repo>/.paper/style_overrides.md` and
fill in the values for your group. Rules there override the skill defaults.

Everything below is a template. The bracketed placeholders and the "Example"
blocks are illustrations; replace them with your own calibrated values.

## How To Calibrate From A Corpus

The strongest overrides are measured from the writing you want to emulate,
usually your advisor's or your group's own published papers. A quick recipe:

1. Collect 15 to 30 papers, and separate the ones where your advisor is first
   or corresponding author (the voice the group actually enforces) from papers
   where they are a middle author (co-author drafts drift from the house
   style). Weight the first group.
2. Extract the text and count, per 1000 words: em-dashes (U+2014), semicolons,
   and each candidate stock phrase. A few lines of Python (pdfplumber or
   PyMuPDF plus a regex counter) is enough.
3. Read a Methods, a Results, and a Discussion section from three of the
   first-author papers and note the recurring openings, transitions, and
   hedging verbs.
4. Write the measured budgets and the observed conventions into the blocks
   below. Re-measure when the group's style shifts.

## Allowed Terms Despite Defaults (field-native words)

Some words on the universal banned list are ordinary register in a given
field and appear in a large share of that field's published papers. List the
ones your target journal's reviewers use routinely, so the audit treats them
as a density check (flag only word-spamming) rather than a per-occurrence ban.

```text
Example (replace with your field's list):
- "robust" in its statistical or optimization sense.
- "comprehensive", "substantial", "facilitate" as ordinary register.
- "significant" when reporting a p-value or confidence interval.
- your-field-native-word-1
- your-field-native-word-2
```

## Banned Phrases (hard-flag; these are field-independent tells)

These multi-word stock phrases carry no domain meaning and are reliable
AI-or-throat-clearing tells regardless of field. Keep them flagged; extend the
list with any your group considers filler.

```text
- "in recent years"
- "this study aims to" / "seeks to"
- "in summary" / "to conclude"
- "it is important to note" / "it is worth noting"
- "shed light on" (unless your group treats it as an allowed idiom; say so)
- "moving forward"
```

## Em-Dash Budget

Set the budget from your own corpus, not a whole-field mean, and benchmark
against the author's first-author and corresponding-author papers (co-author
drafts run heavier and inflate the threshold).

```text
Example (replace with your measured values):
- Abstract: [0 to 2] em-dashes total. Prefer commas.
- Body: at or below [your measured density] per 1000 words. Do not flag a
  single em-dash if that is within the author's natural range.
```

## Section Conventions (your group's signatures)

Fill in the openings, transitions, and structure your group actually uses.
The prompts below are the questions to answer for each section; delete the
ones that do not apply.

```text
Abstract
- How does the opening move (importance-first, site-and-stakes, method-first)?
- Is a named case study or testbed required, and where is it placed?
- How are results introduced (a reporting frame, or a bare statement)?
- What closes the abstract (contribution only, or contribution plus a
  forward-looking or vision sentence)?

Introduction
- Is the literature review organized any particular way (thematic, by
  category, by sub-question)?
- Should each review paragraph map to a specific research sub-question?
- How is the gap stated, and how firmly relative to the contribution?
- Are numbered objectives and a roadmap paragraph expected?

Study Area (if the field carries one)
- Name-and-quantify opening, or a first-person testbed selection?
- Is an institutional or legal context layer expected?

Methods
- Component-then-formalize? A full "where X = ..." symbol gloss?
- Are deliberate signposts, long assumption-plus-justification sentences, or
  a statistical use of "robust" exempt from the universal repetition and
  length rules? List them so the audit does not misfire.

Results
- Figure-first or finding-first paragraph openings?
- Validate against history before projecting?

Discussion
- Is a dedicated, labeled Limitations and future work subsection required?
- Any intentional devices (scare-quotes on value terms) not to strip?

Conclusion
- Do the findings mirror the introduction's numbered objectives?
- Is a capability-phrased generalizability sentence expected?
```

## Author Voice

```text
Example (replace with your group's conventions):
- Use "we" for your own work; passive or third person for others'.
- Methods and specific results in past tense; definitions in present tense.
- Underclaim the contribution ("an attempt", "a first step") where the group
  prefers modesty.
- Do not restructure Methods without explicit approval.
```
