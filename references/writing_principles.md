# Writing Principles — 8 Core Rules

These are universal rules for rigorous academic writing. Every rule includes a
**why** so judgment calls at the edges stay consistent.

---

## 1. Structure & Logic

### 1.1 Findings-first

State the result before explaining the cause. Never open a result paragraph
with "Figure X shows..." or "Results indicate that...".

- **Correct**: *Adaptation reduces renter flood damage by 19%. Relocation to
  lower-exposure tracts accumulates over time, so damage avoidance contributes
  a growing share of the reduction.*
- **Wrong**: *Figure 5 shows that renters relocate to safer tracts, which
  leads to damage reductions of 19%.*

**Why**: readers scan for the finding; front-loading mechanism hides it.

### 1.2 Mechanism for every result

Every result sentence is followed by a mechanism sentence. If the reader can
ask "why?" after the finding, the paragraph is incomplete.

A result triple: **What (pattern) → Why (causal explanation grounded in the
study design) → Implication (for the RQ or broader context)**.

Missing any layer triggers an immediate rewrite.

### 1.3 Every sentence connects to the previous

Each sentence must be linked to the one before by:
- "While [prior], [new focus]" pivot, or
- A demonstrative + verb ("This gap reflects...", "These patterns suggest..."), or
- A pronoun with a clear, unambiguous antecedent.

If the reader cannot tell why sentence B follows sentence A, the transition
is broken and the whole paragraph fails.

### 1.4 Finish each section completely

Do not defer explanations to a later section. Each paragraph lands its own
mechanism and implication before moving on. Never force the reader to "wait"
for the next section to understand the current one.

**Why**: forward references make rebuttal reviews painful and signal that the
structure is not thought through.

### 1.5 Opening sentence per subsection

Every subsection begins with one sentence that states **(a) what this
subsection does, and (b) why it is needed now**. This is the
transition-plus-purpose pattern, not a topic sentence.

The reader should never wonder "why am I reading this section at this point?".

### 1.6 Hypothesis-driven research questions

Every RQ is preceded by a directional hypothesis — "We expect X because Y,
given Z" — and the Results section tests that specific hypothesis.

Vague RQs that ask "how does X change" with no directional expectation, paired
with descriptive results, trigger a complete rewrite.

---

## 2. Precision

### 2.1 No overclaim

Match certainty to evidence. Two tiers:

- **Direct language OK**: established empirical facts from the literature,
  mathematical identities, and design decisions the author controls
  (e.g., "we set X = 5", "the protocol was approved by the IRB", "the model
  threshold triggers an update").
- **Hedged language required**: any result, pattern, or mechanism *inferred
  from* your data, simulation, or statistical test. Use *is consistent with,
  suggests, appears to, may explain, is associated with*.

**Red-flag overclaim words for inferred findings**: *confirms, proves,
demonstrates, determines, controls, ensures, eliminates, clearly,
dramatically, significantly* (without a p-value or effect size).

### 2.2 No vague intensifiers

Words like *substantially, sharply, considerably, major, dramatic* require a
number or concrete comparison right next to them. Delete them if you cannot
quantify.

Note: "significant" is correct and expected when reporting a statistical
test with a p-value or confidence interval. It is a red flag only when used
as a vague intensifier outside a statistical context.

### 2.3 Precise targets

- "Distributions decline" → specify **what** declines (median? IQR? tail?).
- "Similar pattern" → state what is similar, or delete.
- "The gap" → specify "the gap between X and Y".
- "Various factors" → name them.
- Demonstratives ("this gap", "these asymmetries") must have a referent the
  reader can point to in the prior sentence.

### 2.4 Figure citations at panel level

Cite "(Figure 5b, blue line)" or "(Figure 6e, tail region)" rather than
"(Figure 5)". Panel-level precision lets the reader verify in one glance.

### 2.5 Numbers must match code / data output

Re-run the computation every time the paper is revised. Never copy numbers
from a prior draft. Values change between revisions and stale numbers are
the easiest reviewer catch. This applies equally to simulation output,
regression coefficients, bench-measurement readings, and literature quotes.

### 2.6 Numbers must match figures

Any precise percentage or value in the prose must be visible on the referenced
figure (as an annotation, endpoint label, or readable from a labeled axis). If
the figure does not display the number, either:
- Add the annotation to the figure, or
- Switch to a qualitative description in the prose.

Do not let precise percentages appear only in the text while the figure shows
nothing that supports them.

### 2.7 Symbols match figures and equations

Notation in the prose (e.g., `p_a^g`) must match exactly what the figure or
equation displays. Pick distinct symbols for distinct quantities — never reuse
`D` for both depth and deductible.

---

## 3. Mechanism & Argument

### 3.1 Every finding earns its mechanism

No result sentence stands alone. Results that only describe the figure
("Figure X shows A increases") without explaining **why** the study produced
that outcome are incomplete.

### 3.2 Counterintuitive Result Audit

Before writing a counterintuitive finding into the paper, run this 5-step
audit. This applies to any paper — simulation, empirical, lab, or archival:

1. **Denominator check**: if the result is a percentage, verify the denominator.
   Watch for units that leave the pool (e.g., dropouts in a cohort, failed
   batches in a lab, censored observations in survival data) that inflate the
   remaining category percentages mechanically.
2. **Direction plausibility**: trace the causal chain through the study's
   theory or design. If the direction seems wrong, investigate possible
   cascades (sequential-decision order, threshold interactions, non-monotonic
   dose response, confounders).
3. **Subgroup magnitude check**: compare to related subgroups. Outliers in one
   subgroup deserve a specific explanation, not a general one.
4. **Artifact check**: look for initialization bias, backfill rules, boundary
   effects, batch effects, instrument drift, questionnaire wording, or other
   structural causes that could produce the pattern without a real mechanism.
5. **Absolute-value sanity**: compare to real-world data or prior literature.
   Unusual magnitudes often signal a unit or scaling error.

Report the audit to the user **before** writing the finding into the paper.
If the audit reveals a real mechanism, the mechanism becomes the story. If it
reveals an artifact, fix the artifact first.

### 3.3 Counterintuitive findings need stories, not number dumps

When a result contradicts intuition, explain the mechanism as a narrative:
what happened, why the data produced it, and what the reader should take
away. Reporting a raw percentage without the story is a missed scientific
opportunity.

### 3.4 Logical-fallacy and argumentation audit

Before writing a causal claim, check against these common failures:

- **Correlation vs causation**: is the claim supported by more than a
  correlation? If you lack intervention, randomization, or instrumental
  variation, switch to associational language.
- **Reverse causality**: could the effect have caused the cause? Rule out
  before asserting direction.
- **Selection bias in framing**: does the sample under-represent a group
  whose inclusion would flip the finding? Name the selection rule.
- **Straw-manning prior work**: quote or paraphrase prior claims faithfully,
  then extend. Never caricature to make your contribution look bigger.
- **Base-rate neglect**: a 3x relative-risk increase from 0.1% to 0.3% is
  not "widespread" — report the absolute rate alongside the relative one.
- **Survivorship bias**: are you generalizing from cases that made it into
  the dataset while ignoring the silent failures that did not?

Apply these checks in Discussion paragraphs that make causal or policy claims.

### 3.5 Contribution test

Before claiming any result as a contribution, apply the test: **could a
reader guess this without running your study?**

- Yes → it is common sense and does not belong in the abstract, results,
  conclusion, or sensitivity analysis.
- No → it earns contribution status.

Only study-dependent insights are contributions.

---

## 4. Word Choice

### 4.1 No GPT / AI-style vocabulary

Load `banned_words.md` and audit every new paragraph against it.

### 4.2 Avoid awkward agency

Variables don't "receive" values; data don't "know" things. Use precise
descriptions:
- **Wrong**: *Subjects receive score increases after treatment.*
- **Right**: *Treatment raises subjects' scores.*

### 4.3 Causal connectors

Avoid "because" and "so" as causal connectors — too informal for academic
prose. Use instead:
- Subordinate clauses: *As X, Y...* / *Given that X, Y...*
- Participial phrases: *X, resulting in Y* / *X, which in turn Y*
- Semicolons with consequence: *X; this Y*
- Explicit connectors: *This difference arises from...* /
  *This pattern reflects...*

### 4.4 No colons as list starters inside prose

Do not write "Three factors: (a)...(b)...(c)...". Integrate the list into the
sentence grammar or break into separate sentences.

### 4.5 Academic polish pass

After structural rewrite, run a distinct **polish pass** for:
- Nominalized phrasings: *"knowledge gap reflects..."*,
  *"cumulative effect on..."*
- Parallel structure in lists and comparisons
- Redundant prepositional chains

---

## 5. Voice, Tense, and Rhythm

### 5.1 Active vs passive voice

- **Active** for claims, findings, contributions: *"We find X.", "This study
  shows Y."*
- **Passive** for methods that are conventional or when the actor is
  irrelevant: *"Samples were collected in triplicate."*
- **Neither** as a universal rule — mix to match the point being made.

Over-reliance on passive voice signals hedging or concealment. Over-reliance
on active "we" throughout methods reads as self-centered.

### 5.2 Tense conventions

- **Past tense** for methods, data collection, and specific results:
  *"We sampled 200 tracts. The adaptation scenario reduced damage by 19%."*
- **Present tense** for established background, definitions, equations, and
  general statements about how the model works:
  *"Equation 2 computes insurance payouts. Floods cause damage roughly
  proportional to inundation depth."*
- **Present perfect** ("has shown", "have demonstrated") for literature
  background when framing a gap.

Mixing tenses within a sentence is usually wrong; check each sentence.

### 5.3 Sentence rhythm

Vary sentence length. A paragraph of uniform 22-word sentences reads
monotonic even when the content is strong. Alternate:
- One long sentence that carries the main claim with its caveats.
- One short sentence that hits the consequence ("This reverses the pattern
  reported in prior work.").

Target hard max: ≤35 words per sentence. Average: 20–30.

### 5.4 Word repetition

- Same noun appearing 3+ times in one paragraph → replace two instances with
  synonyms or pronouns where the referent is clear.
- Same verb 2+ times in one paragraph → vary.
- Same adjective/adverb 2+ times in one paragraph → vary or delete.
- Exempt: proper nouns, defined acronyms, and unavoidable technical terms.

---

## 6. Figures

See `figure_conventions.md` for full rules. Core principles:

### 6.1 Define once, use thereafter

A term defined in the first figure's legend is used as-is in every later
figure. Do not redefine the same concept with a different label mid-paper.

### 6.2 Cross-figure consistency

Same concept → same label, same color, same annotation style across all
figures in the same paper.

### 6.3 Figure-text coupling

Numbers cited in the prose must appear on the figure. If the prose reports
"insurance covers 36%", the figure shows 36% (as a tail-gap annotation,
percentage label, or equivalent).

### 6.4 Caption format

*Figure X. [Description sentence]. (a) [panel description], (b) [panel
description], ...*

Never start a caption sentence with parentheses. Each panel is described
individually.

### 6.5 Field conventions

Use the standard chart type of the field (e.g., hydrograph in hydrology,
Kaplan–Meier in survival analysis, forest plot in meta-analysis,
exceedance-probability curve in catastrophe modeling).

Be careful with conventions that assume specific data properties. Example:
**rank-based return periods** require independent events — they are not valid
for ensembles generated by replicating the same hazard sequence with
stochastic agent decisions. Use plain exceedance probability when
independence fails.

---

## 7. Redundancy

### 7.1 Do not repeat across paragraphs

If a mechanism is explained in P1, a P5 summary does not re-explain it.
Summary paragraphs reference, they do not restate.

### 7.2 Do not repeat across sections

Anything established in Methods is not re-explained in Results. Results
references Methods by section or equation number if needed.

### 7.3 Define once per paper

A term defined on first use is never re-defined. Re-definitions are a common
reviewer annoyance and signal the sections were written by different people
without reconciliation.

### 7.4 Vary expression

Do not repeat the same phrasing back-to-back. Paraphrase while keeping the
technical term exactly the same.

---

## 8. Process

### 8.1 Base revisions on the accepted version

When revising against comments, apply track-changes first; then modify only
what the comments require. Do not rewrite from scratch.

### 8.2 Every comment → exact anchor text

Before responding, identify the exact sentence the comment is attached to.
Do not guess.

### 8.3 Build / compilation scripts are source of truth

When a compiled master document (e.g., `manuscript_V3.docx`) and the
individual build scripts or source files disagree, trust the build scripts.
Master docs can lag by weeks.

### 8.4 Iterative rewrite reality

Heavy rewrites (abstracts, rebuttal letters) typically need 3–6 passes, each
fixing a different class of issue:
1. Structure
2. Mechanism accuracy
3. Terminology
4. Academic polish
5. Transitions
6. Word count

Set this expectation with the user upfront.

### 8.5 Auto-review habit

After writing or significantly modifying any paragraph, run this skill's
audit before showing the paragraph to the user. Do not wait for the user
to ask.
