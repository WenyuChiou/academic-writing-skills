# Example: `style_overrides.md`

Copy this file to `<paper-repo>/.paper/style_overrides.md` and edit to fit
your paper. Anything here overrides the skill's defaults in
`writing_principles.md` and `banned_words.md`.

Only include the sections you need — leave everything else to inherit the
skill defaults.

---

## Banned terms for THIS paper

Terms that are globally allowed but banned in this manuscript specifically:

```
- "housing tenure"      # reason: this paper uses "homeowners and renters" only
- "Monte Carlo"         # reason: reviewers flagged as not applicable to our stochastic setup; use "stochastic runs"
- "GUL"                 # reason: legacy term; this paper uses "flood damage" throughout
```

## Terms that are ALLOWED here despite global default

Overrides of the skill's banned list (use sparingly — justify each one):

```
- "significant"         # allowed because this paper reports p-values throughout
- "Although" at start   # allowed: journal style (Nature Climate Change) welcomes it
- em-dashes             # allowed: journal style permits; target ≤ 2 per paragraph
```

## Terminology preferences (prescriptive)

Pairs of preferred → avoid for this paper:

```
preferred            avoid
-------------------  ----------------------
"flood damage"       "GUL", "gross loss"
"adaptation scenario" "worst-case scenario" (reserve "worst-case" for a specific scenario)
"two-way coupled"    "fully coupled", "dynamically coupled"
"out-of-pocket"      "uncompensated loss"
```

## Figure convention overrides

```
- Colors: red = damage, blue = loss, gray = severe-year shading
- Percent endpoint labels on EP curves: report UNCOVERED share (actual_loss / damage)
- Severe flood years highlighted: 2011, 2021
```

## Section-numbering / reference-format overrides

Used when this paper's target journal deviates from what the skill assumes:

```
- Equation refs: use "(Eq. 3)" not just "Equation 3"
- Section refs: Roman numerals in Discussion only; Arabic elsewhere
- SI refs: "Fig. S3" with period and space (per AGU house style)
```

## Author voice

```
- First-person: "we" (not "the authors" or "the writers")
- Tense: methods past, results past, general claims present
- Never use "this paper shows..." — use "we show..." or "[result]
  indicates..."
```

## Paper-specific quirks

Free-form notes the skill should respect:

```
- The Methods section was structured by the advisor with track-changes
  accepted on 2026-04-10 — do not restructure without discussion.
- Sensitivity analysis lives in Section 4.3, NOT the SM.
- Table S2 is the authoritative parameter table; the one inside Methods
  is a trimmed view.
```

---

## How the skill reads this file

1. Loaded after `writing_principles.md` and `banned_words.md`
2. Any banned term added here is added to the active banned list
3. Any allowed override removes that term from the active banned list
4. Terminology preferences become flag-on-use rules with the preferred
   replacement suggested automatically
5. Figure / section conventions override `figure_conventions.md` defaults
