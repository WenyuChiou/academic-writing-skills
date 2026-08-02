# Display, Notation, and Provenance Review

## Load This Module Selectively

Load this module when the manuscript uses equations, formal symbols, indexed variables, normalized or aggregated series, composite metrics, shaded ranges, divergence measures, scenario summaries, or other derived quantities in figures or tables.

Do not load it merely because a manuscript contains a simple descriptive table or an untransformed plot whose variables, units, and source are already explicit. A display filename, one symbol, or a generic mention of uncertainty is not sufficient by itself.

## Build an Equation and Notation Ledger

For each material symbol, record its definition, unit or scale, domain, indices, first defining location, and every artifact where it appears. Then verify:

- one symbol does not silently represent different variables
- one variable is not assigned competing symbols without an explicit reason
- spatial, temporal, group, scenario, model, and agent indices remain distinct
- vectors, matrices, parameters, estimates, random variables, and observed values use consistent notation
- equations, prose, figures, tables, captions, appendices, and supplements agree
- sensitivity-analysis and implementation notation matches the Methods definition
- transformed, normalized, or dimensionless quantities remain distinguishable from their source variables

Do not invent a definition for an undefined symbol. Classify it as missing, ambiguous, conflicting, or not verifiable and identify the authority needed to resolve it.

## Trace Derived Display Quantities

For every material quantity that is not a direct reported variable, trace:

```text
source data or model output -> transformation or equation -> aggregation or normalization -> displayed value -> textual claim
```

Require a traceable basis in the Methods, an equation, a reproducible code rule, a table note, or a caption definition. Check:

- numerator, denominator, baseline, reference group, and normalization range
- aggregation level and weighting across time, space, people, runs, models, or scenarios
- uncertainty definition, including whether bands show spread, confidence, credible intervals, quantiles, ensembles, or sensitivity ranges
- treatment of missing values, censored values, zero denominators, and excluded runs or groups
- whether omitted models, events, groups, scenarios, or panels have a stated and defensible reason
- whether the caption defines non-obvious transformations and uncertainty instead of only identifying colors and panels
- whether the prose interprets the displayed quantity at the same scale and with the same comparison basis

Do not infer provenance from visual appearance. If the transformation or exclusion rule is unavailable, mark the claim as not verifiable and bound any requested revision to clarification rather than reconstructed analysis.

## Report Material Failures

Distinguish:

- **notation conflict:** the same symbol or label has incompatible meanings
- **definition gap:** a symbol, transformation, or uncertainty display lacks a definition
- **provenance gap:** the displayed value cannot be traced to an authorized source or rule
- **display–claim mismatch:** the text asserts a comparison, scale, or uncertainty meaning that the display does not support
- **cross-artifact regression:** a later edit updates one artifact but leaves equations, captions, supplement, or summaries stale

Apply the base severity and evidence-status system. Do not make a cosmetic notation preference blocking unless ambiguity, reproducibility, or claim interpretation is materially affected.
