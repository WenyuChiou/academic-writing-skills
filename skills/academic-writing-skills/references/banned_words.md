# Banned Words, Phrases, And Patterns

Items below should be deleted, replaced, quantified, or justified. Paper-specific
overrides in `.paper/style_overrides.md` take precedence.

This file covers field-agnostic GPT-style vocabulary. For field-foreign
jargon that signals "this author is not from our discipline" to reviewers
(terminology imported from a sub-field, method paper, software repository,
or neighbouring discipline that the target journal's reviewer pool does
not use natively), see `writing_principles.md` §4.6 and the "Domain
Vocabulary Swaps" section of `.paper/style_overrides.md`.

For noun-noun hyphenated compounds invented to label a concept the paper
introduces (rather than drawn from existing field vocabulary) and for the
limit on semicolons and colons in body prose, see `writing_principles.md`
§4.7 and §4.4 respectively.

## 1. Single Words

### Verbs

| Avoid | Prefer |
|---|---|
| delve | examine, investigate |
| utilize | use |
| leverage | use, apply, draw on |
| harness | use |
| navigate | address, handle |
| foster | encourage, produce |
| showcase | show, present |
| underscore | show, emphasize sparingly |
| bolster | support, strengthen |
| garner | receive, gather |
| embark | begin |
| unpack | explain, examine |
| endeavor | aim, work |
| elucidate | show, explain |
| substantiate | support |
| facilitate | enable, allow, or rewrite |
| exemplify | show, illustrate |
| conflates | confuses, treats as the same |
| entails | carries, involves |
| attained | reached, results from |
| reproduces (an effect or inequity) | repeats, extends |
| misreads (a figure or number) | mistakes ... for |
| collapses (X to Y) | reduces (X to Y) |

### Adjectives

Delete or quantify: crucial, pivotal, intricate, meticulous, vibrant, robust,
nuanced, multifaceted, comprehensive, paramount, imperative, indispensable,
noteworthy, novel, innovative, holistic, seamless, substantial, substantive,
major, dramatic. Several of these are field-native in some disciplines (see
Field-Native Exemptions below).

### Field-Native Exemptions

This exemption governs BOTH the verb table and the adjective list above. Some
of these words are ordinary register in a given discipline and appear in a
large share of that field's published papers, not as GPT tells. In water
resources and hydrology, for example, the verb "facilitate" and the adjectives
"robust" (a robust optimization algorithm, a statistically robust test),
"comprehensive", and "substantial" are used routinely and legitimately. In such
a field, treat these as a density check (flag only when one word appears many
times in a single section, i.e. word-spamming) rather than a per-occurrence
ban. Record the exempt list for a given paper or group in
`.paper/style_overrides.md` under "Allowed Terms Despite Defaults". The
multi-word stock PHRASES in §2 and §2a are the reliable tells and stay banned
regardless of field.

"novel" and "first" are permitted-but-hedged in BODY sections (Introduction,
Methods, Discussion, Conclusion) when they denote a genuine methodological or
model first, and only when fenced in the same or the next clause by a
knowledge-scope qualifier ("to the best of our knowledge, this is the first
study that ..."). An unfenced "novel"/"first" is still an overclaim. Results is
excluded from this list on purpose: a "novel"/"first" claim in a Results
paragraph is almost always a contribution claim rather than a finding, so move
it to the Introduction or Discussion. In the ABSTRACT the stricter rule holds:
keep "novel"/"first"/"unprecedented"/"pioneering" out entirely (see the
`abstract-writer` skill), because the abstract has no room to establish the
scope that justifies the claim.

The fence is necessary, not sufficient: "to the best of our knowledge" lowers
the tone but does not establish the fact. Route every fenced novelty or
priority claim to a literature and priority check (the `verify-references`
skill or the claim-evidence ledger); do not clear it on the qualifier string
alone. A prior work existing anywhere makes the claim false even when the
qualifier precedes it.

"Significant" is allowed for statistical significance. It is not allowed as a
generic intensifier.

Avoid journalistic register (news-article diction): harder-hit, hidden cost,
staggering, eye-watering, a stark reminder. State the quantity or the mechanism
plainly instead (for example, *harder-hit* becomes *bears the larger loss*).

### Adverbs

Usually delete: undeniably, remarkably, notably, crucially, importantly,
ultimately, meticulously, markedly, substantially, considerably.

Also delete when used as fillers (not when carrying technical content such as
*statistically significantly* or *spatially explicitly*): essentially,
fundamentally, inherently, particularly, specifically, effectively, largely,
broadly, generally, relatively (without a comparator), arguably.

### Redundant Qualifiers

Delete the qualifier — the noun already carries the meaning:

| Redundant | Use |
|---|---|
| completely unique | unique |
| absolutely essential | essential |
| totally novel | novel (and quantify why) |
| fully comprehensive | comprehensive (and quantify) |
| extremely critical | critical (and justify) |
| deeply concerning | concerning (and state the consequence) |
| highly significant | significant (with statistical evidence) |
| very important | (delete; if it matters, the sentence will show why) |

### Metaphorical Nouns

Avoid: tapestry, landscape as a metaphor, beacon, realm, interplay, synergy,
testament, paradigm, cornerstone.

## 2. Banned Phrases

- "It is important to note that..."
- "It is worth noting that..."
- "In recent years..."
- "In today's world..."
- "plays a crucial role"
- "provides a comprehensive framework"
- "as mentioned above"
- "as established earlier"
- "beyond this"
- "in this regard"
- "with respect to this"
- "sheds light on"
- "a testament to"
- "the interplay between"
- "ever-evolving"
- "at the forefront"
- "moving forward"

## 2a. AI-Conclusion And Throat-Clearing Phrasings

These are among the most reliable LLM-prose tells in 2025-2026. They add
no information and signal AI-generated wrap-up rhetoric. Delete or rewrite.

| Avoid | Prefer |
|---|---|
| in conclusion, / to conclude, | (delete — the sentence itself should be the conclusion) |
| in summary, / to summarise, | (delete or use a structured roadmap heading) |
| as discussed above / as we have seen / as established earlier | (delete; if needed, cite §X) |
| having explored / having considered | (delete or rewrite as a direct claim) |
| with that said / having said that / that being said | however, (or rewrite) |
| to that end / in light of this | (delete or name the specific reason) |
| the field of X has witnessed / has seen rapid growth | quantify: "publications grew from N to M, 20YY-20YY" |
| in the rapidly evolving landscape of X | (delete; usually meaningless) |
| paving the way for | "supports", "motivates", "suggests" |
| shedding light on | "shows", "indicates", "reveals" |
| this study aims to / sets out to / seeks to / endeavours to | "we test whether", "we estimate", "we show" |
| at the heart of / lies at the core of | "central to" (and only when justified) |

## 3. Weak Demonstratives

Flag subject-less openings such as:

- "This ensures..."
- "This enables..."
- "This allows..."

Replace "this" with the actual antecedent unless the previous sentence makes it
unmistakable.

## 4. Sentence Starters

Generally avoid:

- "Furthermore,"
- "Moreover,"
- "Additionally,"
- "Building on..."
- "Together,"
- repeated "By [verb]-ing, we..."

Style-dependent starters such as "Although", "Yet", "By contrast", "Therefore",
and "Thus" should follow journal and advisor preferences.

## 5. Structural Patterns

### Long Dash Overuse

Some journals allow long dashes and some advisors dislike them. The universal
rule is overuse: more than two long dashes in one paragraph usually signals
sloppy or AI-like prose. Follow `.paper/style_overrides.md`.

Corpus-calibrated baseline (optional, stronger than the universal rule). If a
`.paper/style_overrides.md` sets an em-dash budget from the target author's own
published corpus, benchmark against that baseline rather than a whole-field
mean. Prefer the author's own first-author and corresponding-author papers over
papers where they are a middle author, since co-author drafts run heavier on
dashes and would inflate the threshold. For a template that shows how to
measure and set this budget from your own corpus, see
`style_overrides_customization.md`.

### Adjective Stacks

Avoid noun piles such as "comprehensive robust multi-scale framework". Use one
adjective and a precise phrase.

### Colon Lists Inside Prose

Avoid "Three factors: (a)...". Integrate the list into the sentence or use a
proper list.

### Repetitive Openings

Three consecutive sentences beginning with "The" or "This" should be revised
unless the repetition is deliberate and clear.

### Participial Chains

Avoid paragraph openings such as "Building..., integrating..., and leveraging...".
Use direct claims.

## 6. Overclaim Language

For inferred findings, avoid:

| Avoid | Prefer |
|---|---|
| confirms | is consistent with |
| proves | suggests |
| demonstrates | indicates |
| determines | shapes |
| controls | influences |
| ensures | tends to |
| eliminates | reduces |
| drives | contributes to |
| explains | may explain, is consistent with |

Use "significant" only with statistical evidence.

Reporting-frame exemption. "the results show/showed that ...", "the [model]
results showed that ...", and "results suggest/indicate that ..." are allowed
as neutral frames for introducing model or experiment output. The frame is not
the overclaim; the hedge belongs on the interpretation that follows the number.
Do not remap this frame to "is consistent with". See `writing_principles.md`
§2.1.

## 7. Mechanistic Trigger Phrases

These phrases often invite reviewer pushback unless the method explicitly
supports them:

| Trigger phrase | Safer replacement |
|---|---|
| preferentially selected | more likely to |
| systematic bias | average difference of X |
| filter tightens | share changes from A to B |
| removed from the denominator | no longer included in the group |
| residual group | remaining group meeting criterion X |
| isolates the effect | focuses on, conditions on |
| hard-coded | specified in Methods |
| explains away | accounts for X of the gap |
| must, necessarily, invariably | tends to, on average, in N cases |

## 8. Detection Heuristic

For any suspicious sentence, ask:

1. Would a domain-expert PhD student write this?
2. Does removing the sentence lose information?
3. Are there too many adjectives before one noun?
4. Does the sentence use a metaphor where a technical term is needed?
5. Does every demonstrative have a clear antecedent?
