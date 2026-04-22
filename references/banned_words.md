# Banned Words, Phrases, and Patterns

All items below should either be **deleted** or **replaced with concrete alternatives**.
Always audit a paragraph against this list before showing it to the user.

The paper's own `<paper-repo>/.paper/style_overrides.md` may add, remove, or override
entries here. Paper-specific rules take precedence.

---

## 1. Banned Single Words

### Verbs (delete or replace with plain equivalent)

| Banned | Use instead |
|---|---|
| delve | examine, investigate |
| utilize | use |
| leverage | use, apply, draw on |
| harness | use |
| navigate | handle, address |
| foster | encourage, produce |
| showcase | show, present |
| underscore | emphasize, highlight (sparingly) |
| bolster | support, strengthen |
| garner | gather, receive |
| embark | begin, start |
| unpack | explain, examine |
| endeavor | work, aim |
| elucidate | show, explain, clarify |
| substantiate | support, confirm |
| facilitate | enable, allow, or rewrite |
| exemplify | illustrate, show |

### Adjectives (delete or quantify)

| Banned | Rule |
|---|---|
| crucial | delete or justify with evidence |
| pivotal | delete |
| intricate | delete or describe specifically |
| meticulous | delete |
| vibrant | delete |
| robust | specify what (consistent across seeds? low variance?) |
| nuanced | delete or describe what is subtle |
| multifaceted | delete |
| comprehensive | delete or list the facets |
| paramount | delete |
| imperative | delete |
| indispensable | delete |
| noteworthy | delete |
| enduring | delete |
| novel | delete — let the reader judge |
| innovative | delete |
| holistic | delete or describe scope |
| seamless | delete |
| substantial | delete or quantify |
| substantive | delete or quantify |
| significant (non-statistical use) | delete or quantify — **keep** when reporting a statistical test with a p-value or confidence interval |
| major | delete or quantify |
| dramatic | delete or quantify |

### Adverbs (almost always delete)

| Banned | Rule |
|---|---|
| undeniably | delete |
| remarkably | delete |
| notably | delete |
| crucially | delete |
| importantly | delete |
| ultimately | delete |
| meticulously | delete |
| markedly | quantify |
| substantially | quantify |
| pronouncedly | quantify |
| considerably | quantify |

### Nouns (metaphor overload)

| Banned | Rule |
|---|---|
| tapestry | delete |
| landscape (metaphorical) | delete; OK for literal geographic landscape |
| beacon | delete |
| realm | delete — use domain, field |
| interplay | delete or specify interaction |
| synergy | delete |
| testament | delete |
| paradigm | use format, approach, framework |
| cornerstone | delete |

---

## 2. Banned Phrases

### Filler openings / meta-references
- "It is important to note (that)..."
- "It is worth noting (that)..."
- "In recent years..."
- "In today's [adj] world..."
- "plays a crucial/pivotal role..."
- "This approach provides a comprehensive framework..."
- "As mentioned above"
- "As established earlier"
- "Beyond this"
- "In the context of..."
- "In this regard..."
- "With respect to this..."
- "shed(s) light on..."
- "a testament to..."
- "the interplay between..."
- "ever-evolving"
- "at the forefront"
- "moving forward"

### Subject-less GPT tics
- "This ensures..."
- "This enables..."
- "This allows..."
  
  (Always name what "this" refers to.)

### Empty amplifiers
- "dynamic equilibrium"
- "increasingly layered [X] structure"
- "truly [adj]"

---

## 3. Banned Sentence Starters

### Universally banned (always rewrite)

- "Furthermore,"
- "Moreover,"
- "Additionally,"
- "Building on..." (GPT filler transition)
- "Together," (GPT filler)
- "Together building..." (participial GPT filler)
- "Together with X, Y..." (GPT filler)
- "By X-ing, we..." (overused when repeated across paragraphs)

### Style-dependent (default discouraged, overrideable in `style_overrides.md`)

These open sentences in many top-tier journals (Nature, Science, JAMA, AER).
Some style guides (e.g., Yang group) discourage them; other fields welcome them.

- "Although"
- "Yet"
- "By contrast" / "In contrast"
- "Because"
- "Therefore"
- "Thus"

Check the paper's `style_overrides.md` before flagging. Default action: flag but
do not rewrite without confirmation.

---

## 4. Banned Structural Patterns

### Em-dash abuse (paper-dependent, not universal)
Em-dashes (—) are permitted by most major style guides (Chicago, APA 7, Nature).
Some groups or journals discourage them — check `style_overrides.md`. Universal
rule here is *overuse*, not use: more than two em-dashes per paragraph signals
AI-generated text regardless of style. Default: flag on overuse or inconsistent
spacing; do not blanket-rewrite unless `style_overrides.md` says so.

### 3+ adjectives on one noun
"comprehensive robust multi-scale framework" → rewrite; use at most one adjective
plus a prepositional phrase.

### Colon-list when prose works better
"Three factors: (a)...(b)...(c)..." → integrate the list into sentence grammar
or split into separate sentences.

### Repetitive sentence starters
3+ consecutive "The..." or "This..." opens → rewrite one or two.

### Participial chain as paragraph openers
"Building a rigorous framework, integrating heterogeneous data, and leveraging
..." — this is pure GPT. Rewrite as direct statements.

### "In a [adjective] manner" construction
"in a timely manner", "in a seamless fashion" → delete the prepositional phrase
or replace with an adverb.

### Triplet rhetorical structure
"We analyze X, synthesize Y, and illuminate Z" — rule-of-three parallelism used
for cadence rather than content. Delete unless all three items carry distinct
information.

---

## 5. Causal-Connector Rule

Avoid "because" and "so" as causal connectors in academic prose (too oral).
Use instead:

- Subordinate clauses: *As X, Y...* / *Given that X, Y...*
- Participial phrases: *X, resulting in Y* / *X, which in turn Y*
- Semicolons with consequence: *X; this Y*
- Explicit connectors: *This difference arises from...* / *This pattern reflects...*

---

## 6. Overclaim Language (for Model / Simulation Outputs)

Reserve these verbs for established empirical facts or model-design statements,
not for model outputs:

| Red-flag verb | For outputs, use |
|---|---|
| confirms | is consistent with |
| proves | suggests |
| demonstrates | indicates |
| determines | shapes |
| controls | influences |
| ensures | tends to |
| eliminates | reduces |
| drives | contributes to |
| widens (a mechanism) | is associated with |

Reserve *clearly, dramatically, significantly* (without p-value) for literature-
established facts, never model outputs.

---

## 7. Self-Coined Compound Terms

Do not invent compound modifiers or noun-piles. Use plain, direct language.

| Avoid | Use instead |
|---|---|
| "X-mediated benefit" | "the benefit from X" |
| "X-plus-Y coverage" | "X and Y coverage" |
| "Tenure-dependent adaptation efficiency gap" | describe the pattern directly |
| "Event-driven adoption response" | "adoption response following events" |
| Any 3+ word compound modifier | split into a clause |

---

## 8. Detection Heuristic

For any suspicious sentence, ask:

1. **"Would a domain-expert PhD student actually write this?"**
   If it sounds like a press release → GPT.
2. **"Does removing this sentence lose any information?"**
   If no → filler, delete.
3. **"Are there 3+ adjectives before one noun?"** → rewrite.
4. **"Does the sentence contain a metaphorical noun (tapestry, landscape,
   beacon)?"** → rewrite.
5. **"Does every demonstrative (this/these/that) have a clear antecedent in
   the previous sentence?"** → if not, replace the demonstrative with the
   noun.

---

## 9. Reviewer-Triggering Mechanistic Language

When explaining *why* a result looks a certain way, certain phrasings activate
reviewer concerns about hidden assumptions, selection bias, circular
reasoning, or overclaim — even when the underlying claim is valid. Prefer
observational language grounded in numbers or features the reader can verify
in the paper, over algorithmic / statistical-toolkit / metaphorical framings.

This section applies broadly to empirical, experimental, computational, and
observational-study writing.

### 9.1 Trigger phrases → safer replacements

| Trigger phrase | Why it fires | Use instead |
|---|---|---|
| preferentially selected / absorbed / admitted | implies author-imposed bias or hand-picking | *more likely to [action]*; *tend to [action]*; cite the selection rule |
| selective composition / selected sample | triggers selection-bias critique | *composition of the [subset]*; *the subset meeting criterion X* |
| systematic(ally) higher / lower / biased | implies systematic bias in the underlying method | *on average higher / lower*; *higher by [number]*; *differs by [number]* |
| filter tightens / loosens / passes through | mechanical framing — sounds like a hidden knob | state the observable change (*the share of X rises from A% to B%*) |
| removed from the denominator / excluded from the analysis | statistician alarm — looks like denominator manipulation | *no longer included in the [figure/conditional group]*; *outside the scope of [figure]* |
| residual / residual group / residual pool | vaguely pejorative ("leftover"); bias connotation | *the remaining [subgroup]*; *participants not meeting criterion X* |
| low-X participants / high-X group (hyphenated latent-variable labels) | labels individuals by an unobservable property | *participants whose X is below the threshold*; *those with higher X* |
| decays / decays over time / accumulates (as a trend claim) | factual claim that must match the figure — if the line in the figure is flat, rising, or non-monotonic, the reviewer catches it in seconds | describe what the figure actually shows; use *declines / rises / stabilizes* only when the figure supports it |
| progressively accumulates / progressively filters / progressive decline | assumes monotonic temporal accumulation not always visible in data | *over the period*; *by year Y*; *during [window]* |
| isolates / isolates the effect of | overclaims identification | *focuses on*; *restricts to*; *conditions on* |
| absorbs (a signal, an effect) | algorithmic framing — implies unstated channeling | *is associated with*; *primarily reflects*; *covaries with* |
| embedded in / baked into the rule | implies hidden assumption | *defined by the [rule / specification]*; *as specified in Methods / Section X* |
| circular / self-reinforcing dynamics | triggers circular-reasoning concern | describe the specific forward/backward link without the meta-label |
| double-filtered / triply filtered | implies arbitrary stacking of selection steps | describe each selection step with a number from the figure |
| skimmed off / creamed off | strong mechanical metaphor, pejorative | *those with [property] are more likely to [action]* |
| hardwired / hard-coded | reads as uncalibrated author choice | *specified in the [rule / parameter / Methods]* |
| drives / governs / dictates (for model output) | overclaim for simulation / statistical output | *contributes to*; *is associated with*; *shapes* |
| explains away / explains the gap | suggests post-hoc rationalization | *accounts for [number] of the gap*; *corresponds to* |
| must / necessarily / invariably | overclaim of logical necessity | *tends to*; *on average*; *in [N/N] of [cases]* |

### 9.2 Rules of thumb

1. **Numbers from figures, not mechanisms from code.** When explaining why a
   panel or result looks a certain way, cite a number the reader can see in
   another panel or a table (*"67% of X hold Y by 2023 (Figure Z)"*), not a
   mechanism the reader cannot verify (*"the decision rule absorbs high-X
   agents"*).
2. **Say what the figure shows, not what the underlying method does.**
   Results should describe observed patterns and link them to prior
   observable quantities. Methods is where decision rules, estimators, and
   algorithmic behavior live.
3. **Never assert a trend the figure does not support.** If Figure X shows a
   flat or non-monotonic line, do not write "decays", "progressively declines",
   "accumulates". A reviewer will scroll back to Figure X and catch the
   contradiction in seconds. Replace with a neutral description of what the
   figure shows.
4. **Avoid hyphenated latent-variable labels for subgroups.** "Low-TP
   renters" / "high-mobility households" read like arbitrary
   author-defined bins. Use a threshold-based description, the continuous
   variable, or the observable criterion (*"participants in the highest
   quartile of X"*, *"renters with TP above 0.6"*).
5. **Do not name mechanisms the method does not explicitly implement.** If
   the model / estimator has no "filter", "selection stage", or "absorption
   step" as a named component, do not attribute the pattern to one. Describe
   the pattern and link it to a rule that *is* in Methods.
6. **Mechanism explanations in Results stay short.** One to two sentences
   maximum. Each must either (a) cite a number from another figure / table,
   or (b) point to the decision rule / estimator in Methods. Longer
   mechanistic reasoning belongs in Discussion.
7. **Neutral language for direction changes.** Use *crossover*, *convergence*,
   *rises above / falls below*, *differs by [number]*, rather than *reverses*,
   *flips*, *contradicts*, which signal surprise to reviewers and invite
   extra scrutiny.

### 9.3 Self-check before submitting a paragraph

- Can every causal claim be traced to (i) a number the reader can see in the
  paper, or (ii) a rule / specification in Methods? If not, rewrite or drop.
- Does any sentence describe the method doing something "preferentially",
  "selectively", "systematically", or "progressively" without a number
  attached? If yes, replace with the number.
- Does any claim about a trend ("decays", "rises", "accelerates") contradict
  what the reader would see in the corresponding figure? If yes, rewrite to
  match the figure.
- Is any subgroup named by a hyphenated latent-variable label? If yes,
  rephrase using the continuous variable, a threshold, or an observable
  criterion.
- Does any sentence use mechanical metaphors ("filter", "skim", "absorb",
  "funnel") for a process the method does not explicitly implement? If yes,
  replace with the observable change.
- Does any sentence describe a direction change using surprised language
  ("reverses", "flips")? If yes, replace with neutral wording (*crossover*,
  *rises above / falls below*).

Section 6 handles general overclaim verbs (confirms, proves, demonstrates).
This section focuses on the distinct trap of *mechanistic / algorithmic
framing in results prose*, which is common in GPT-assisted drafts and
invites disproportionate reviewer pushback.
