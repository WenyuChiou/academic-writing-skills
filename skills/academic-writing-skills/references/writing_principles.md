# Writing Principles

Universal rules for rigorous academic writing. Use paper-specific overrides in
`.paper/style_overrides.md` when a journal, advisor, or field convention differs.

## 1. Structure And Logic

### 1.1 Findings First

State the result before the figure citation or mechanism.

Correct:

> Adaptation reduces renter flood damage by 19%. Relocation to lower-exposure
> tracts accumulates over time, so damage avoidance contributes a growing share
> of the reduction.

Wrong:

> Figure 5 shows that renters relocate to safer tracts, which reduces damage by
> 19%.

Why: readers scan for the finding. Opening with "Figure X shows" hides the
scientific point.

### 1.2 Mechanism For Every Result

Every result needs a mechanism sentence. A complete result paragraph usually has:

```text
finding -> mechanism -> implication for the research question
```

If the reader can still ask "why?" after the finding, the paragraph is not done.

### 1.3 Sentence-To-Sentence Continuity

Each sentence must connect to the previous one through a clear pivot,
demonstrative, noun repeat, or causal link. If sentence B could be moved
elsewhere without changing meaning, the paragraph is probably a list, not an
argument.

### 1.4 Complete The Local Explanation

Do not defer an explanation to a later section when the current paragraph needs
it. A section may point forward, but it should not make the reader wait to
understand the current result.

### 1.5 Subsection Openings

Open each subsection with one sentence that states what the subsection does and
why it is needed at this point in the paper.

### 1.6 Hypothesis-Driven Research Questions

When possible, place a directional expectation before each research question:

```text
We expect X because Y, given Z.
```

Descriptive research questions without a directional expectation often produce
weak Results sections.

## 2. Precision

### 2.1 No Overclaim

Match certainty to evidence.

Direct language is appropriate for:

- established empirical facts,
- mathematical definitions,
- method settings controlled by the authors.

Hedged language is required for:

- patterns inferred from data,
- simulation output,
- statistical associations,
- mechanisms not directly observed.

Prefer "is consistent with", "suggests", "appears to", "is associated with",
"may explain", or "contributes to" when evidence is inferential.

### 2.2 No Vague Intensifiers

Words such as "substantial", "major", "dramatic", "strong", and "large" need a
number or comparison. Delete them if they cannot be quantified.

"Significant" is valid only when reporting a statistical test with a p-value,
confidence interval, or equivalent inferential result.

### 2.3 Precise Targets

Replace vague nouns with the actual quantity:

- "the distribution declines" -> "the median household loss declines"
- "the gap widens" -> "the homeowner-renter damage gap widens"
- "various factors" -> name the factors

Demonstratives such as "this", "these", and "that" need clear antecedents.

### 2.4 Panel-Level Figure Citations

Use panel-specific citations when panels exist:

- "Figure 5b, blue line"
- "Figure 6e, tail region"

Avoid bare "Figure 5" when the claim depends on one panel.

### 2.5 Numbers Must Match Source Output

Re-check numbers after every revision. Abstract numbers, Results numbers, code
output, tables, and figure annotations drift during editing.

### 2.6 Numbers Must Be Visible Or Traceable

Any precise number in prose must be visible on a figure, in a table, in code
output, or in a cited source. If the reader cannot verify it, either add the
evidence or soften the prose.

### 2.7 Symbols Must Match

Notation in prose, equations, legends, and figures must match exactly. Do not
reuse one symbol for distinct quantities.

## 3. Mechanism And Argument

### 3.1 Counterintuitive Result Audit

Before writing a surprising result, run this audit:

1. Denominator check: verify what the percentage is divided by.
2. Direction plausibility: trace the causal chain through the method or theory.
3. Subgroup magnitude check: compare the subgroup to related groups.
4. Artifact check: test initialization, censoring, measurement, model, or coding
   artifacts.
5. Absolute-value sanity check: compare against prior literature or real-world
   ranges.

Report the audit before treating the result as a contribution.

### 3.2 Mechanisms Need Evidence

Mechanism explanations in Results should point to either:

- a visible quantity in another figure or table,
- a method rule already described,
- a cited theory or empirical finding.

Longer interpretation belongs in Discussion.

### 3.3 Causal Claim Audit

Before writing a causal claim, check:

- correlation vs. causation,
- reverse causality,
- selection bias,
- base-rate neglect,
- survivorship bias,
- faithful treatment of prior work.

If the study design cannot support causality, use associational language.

### 3.4 Contribution Test

Before claiming a contribution, ask:

```text
Could a knowledgeable reader guess this without running the study?
```

If yes, it is background or common sense. If no, it may be a contribution.

## 4. Word Choice

### 4.1 Avoid GPT-Style Vocabulary

Audit new prose with `banned_words.md`.

### 4.2 Avoid Awkward Agency

Variables do not "receive" values, data do not "know" things, and models do not
"discover" unless that is technically accurate. Use plain verbs that name the
actor and action.

### 4.3 Causal Connectors

Avoid oral connectors such as "because" and "so" when formal alternatives are
available:

- "Given that X, Y..."
- "As X increases, Y..."
- "X increases, resulting in Y."
- "This pattern reflects..."
- "This difference arises from..."

### 4.4 Avoid Prose Colon Lists

Do not write "Three factors: (a)...". Integrate the list into grammar or split
the items into separate sentences.

### 4.5 Polish After Structure

Do not polish before the logic is fixed. The normal order is:

1. claim structure,
2. mechanism accuracy,
3. evidence consistency,
4. word choice,
5. transitions and rhythm.

## 5. Voice, Tense, And Rhythm

### 5.1 Active And Passive Voice

Use active voice for claims and contributions. Use passive voice when the actor
is conventional or irrelevant. Do not enforce either as a universal rule.

### 5.2 Tense

- Past tense: methods performed and specific results.
- Present tense: definitions, equations, stable facts, and paper structure.
- Present perfect: literature background when framing a gap.

### 5.3 Sentence Length

Avoid monotonous sentence rhythm. Target an average near 20-30 words and revise
sentences above 45 words unless the journal style or content justifies them.

### 5.4 Repetition

Repeated nouns, verbs, and adjectives can be useful for precision, but repeated
phrasing across consecutive sentences often reads machine-generated. Keep
defined technical terms stable while varying nontechnical wording.

## 6. Figures

Use `figure_conventions.md` for detailed checks. Core rules:

- Same concept -> same label, color, and annotation style.
- Precise numbers in prose must be visible or traceable.
- Captions should be self-contained.
- Panel citations should be specific.
- Field-standard plots are preferred over invented plot types.

## 7. Redundancy

Do not define the same term repeatedly across sections. Do not restate Methods
inside Results unless the interpretation requires a specific equation, rule, or
parameter.

## 8. Revision Process

### 8.1 Base Revisions On The Accepted Version

When revising against advisor or reviewer comments, start from the accepted
manuscript version and change only what the comments require.

### 8.2 Anchor Every Comment

Before answering a comment, identify the exact sentence, paragraph, figure, or
table it targets. Do not guess.

### 8.3 Build Scripts Are Source Of Truth

If a compiled manuscript and source scripts disagree, trust the build scripts or
source files, then regenerate the manuscript.

### 8.4 Iterative Rewrite Reality

Heavy rewrites usually need separate passes:

1. structure,
2. mechanism,
3. terminology,
4. evidence consistency,
5. academic polish,
6. word count.

Set this expectation before trying to fix everything in one pass.
