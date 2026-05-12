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

## Domain Vocabulary Swaps

Use this section when the manuscript originated as a software-method or
AI-method draft and was later refocused for a field audience. Source the
field-native side from a sample of recent papers in the target journal —
two or three Methods and Discussion sections is usually enough to identify
the vocabulary the reviewer pool uses.

Example for a water-resources manuscript whose method layer is an LLM-based
agent-based model:

```text
field-foreign (CS / engineering / generic)        water-resources native
------------------------------------------------  ---------------------------------------------------------
validator stack                                   institutional rule checks
intercepts proposals before execution             screens each proposed decision before the agent acts
numerical state in, numerical action out          takes observed conditions and returns a numerical action
compressed into coefficients                      absorbed into the equation's calibrated parameters
computational interior                            the model's parameter values
cross-theory portability                          same architecture hosts different behavioural theories
decomposed across self-reported cognitive coords  broken down by the agent's own reported appraisal
factor these (verb)                               separate the two
theoretical mobility                              switching the underlying behavioural assumption
```

Novel terms that name the paper's contribution (for the example above:
"action layer" vs "cognitive layer" in human-water ABM) are allowed but
must be defined inline with a field-native concrete example at first use.

The same kind of table applies in any field — ecology papers should not
adopt RL terminology wholesale, materials-science papers should not import
LLM-paper phrasing, and epidemiology papers should keep clinical-research
vocabulary even when the underlying model is computational.

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
