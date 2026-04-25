# Example: style_overrides.md

Copy this file to `<paper-repo>/.paper/style_overrides.md` and edit it for the
specific manuscript. Rules here override the skill defaults.

## Banned Terms For This Paper

```text
- "GUL" because the manuscript uses "flood damage" throughout.
- "worst-case" because it is reserved for the named scenario only.
- "Monte Carlo" because the study uses stochastic runs, not a Monte Carlo estimator.
```

## Allowed Terms Despite Defaults

```text
- "significant" is allowed when reporting p-values or confidence intervals.
- "Although" is allowed as a sentence opener under the target journal style.
- Long dashes are allowed, but use at most two per paragraph.
```

## Terminology Preferences

```text
preferred                  avoid
-------------------------  -------------------------
flood damage               GUL, gross loss
adaptation scenario        worst-case scenario
two-way coupled            fully coupled
out-of-pocket loss         uncompensated loss
```

## Figure Conventions

```text
- red = damage
- blue = insured or recovered loss
- gray = severe-event shading
- endpoint labels report uncovered share
- severe flood years: 2011, 2021
```

## Author Voice

```text
- Use "we", not "the authors".
- Methods use past tense.
- General model definitions use present tense.
- Do not restructure Methods without explicit approval.
```

## Paper-Specific Notes

```text
- Table S2 is the authoritative parameter table.
- Sensitivity analysis belongs in Section 4.3, not the supplement.
- The accepted manuscript baseline is commit abc1234.
```
