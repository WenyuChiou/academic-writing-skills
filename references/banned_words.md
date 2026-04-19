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
