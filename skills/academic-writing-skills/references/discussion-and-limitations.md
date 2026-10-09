# Discussion, Extension Analyses, and Limitations

## Contents

1. Choose the Discussion's function
2. Extension-analysis mode
3. Limitations paragraph planning
4. Hidden inference checks

## Choose the Discussion's Function

Plan Discussion from the actual manuscript and author preference. It may interpret findings against prior work, test alternative explanations, present additional analyses, clarify use boundaries, or combine these functions. Do not force every article into a literature-heavy implications essay or require a policy paragraph.

In an extension-analysis mode, prioritize analyses that add useful understanding beyond the direct answers already reported in Results, then state limitations. Conclusions generally synthesize the main Results and use Discussion to qualify them; an extension that changes a main answer must propagate to that answer and its summaries. Place an analysis with Results when it directly supplies the primary evidence for a study question, unless the genre intentionally combines the sections.

Keep direct findings, supported explanations, plausible interpretations, alternatives, and broader implications distinct. Use transitions that name the actual extension or qualification. Do not give the same result a new name merely to manufacture another contribution.

## Extension-Analysis Mode

For sensitivity analyses, scenario tests, or other extensions, develop **why the test matters → what was changed and held constant → findings relative to the baseline → consequence for the main answer**. Keep essential design and comparison logic in prose or an appropriate Methods passage. Put visual encodings in captions and compact entry-reading information in table notes; do not duplicate the full experiment narrative everywhere.

Do not require sensitivity analyses or extra experiments for every study. A writing check may identify missing evidence, but cannot invent completed work or authorize execution. An analysis can remain response-only when it answers a reviewer concern without being needed by general readers; state that destination honestly.

When writing “the conclusion is unchanged,” name whether this means direction, ranking, magnitude, or metric, state the conclusion itself, and retain the tested range and conditions. Changed numerical estimates can preserve a ranking without preserving every mechanism or claim. Robustness over alternatives does not validate a baseline parameter or supply a post hoc selection rationale. Varying several factors together does not isolate one factor's contribution.

For example, in a hypothetical scenario test, both groups' estimated losses change but their ordering does not. Report the stable ordering under the tested scenarios, not that all financial or welfare conclusions are invariant. The counterfactual contrast and the parameter-setting contrast are different analyses.

## Limitations Paragraph Planning

Begin with the specific constraint in the data, design, measurement, model, validation, or represented outcomes; follow with the inference or use it limits. The opening's job is to identify the study limitation, not merely warn about “interpreting results.” This is a function rule, not a blanket ban on that phrase wherever a concrete constraint and consequence are clear.

Frame a limitation as a boundary created by the study's data, measurement choices,
model representation, assumptions, validation design, or scope—not as a defect in
the manuscript. Name the choice or condition and explain what it makes uncertain
or what inference it cannot support. For example, uncertainty in a selected
geospatial dataset may bound the precision of exposure estimates; it does not
mean the paper itself is defective. Do not disguise a correctable analytical
error, unsupported claim, or omitted required analysis as a limitation: fix it or
state the unresolved issue accurately. This framing clarifies the source of the
boundary without minimizing its consequence.

Group related constraints into a paragraph and order them by dependency or consequence. A useful planning sequence is **constraint → affected component or inference → boundary → optional targeted remedy**. Combine these functions when concise; do not impose a fixed paragraph count, require ordinal starters, or tack a future-work sentence onto every limitation.

Check that consequential assumptions were already disclosed at their operational use in Methods. Limitations can explain their implications but should not reveal the model's actual design for the first time. Separate missing empirical validation from known failure. Lack of household-level evaluation, for example, may narrow claim accuracy without erasing the value of a verified aggregate diagnostic.

Do not invent the direction of bias when it is unknown, call an unexpected finding a methodological limitation, or soften a known omission to preserve a desired narrative. Missing recovery conditions or household resources can restrict a vulnerability interpretation even when modeled property-loss calculations are sound. Match the boundary to the actual construct, not a generic “more data are needed.”

Future work is optional. When included, connect it to the named constraint and state what additional inference it could permit. Do not offer a broad wishlist in place of the present limitation or imply that a proposed remedy has already been implemented.

### Allocate Limitation Claims to Their Actual Consequences

Before drafting a limitations paragraph, sort candidate material into a genuine
constraint on inference or use, a diagnostic or procedure, a substantive result,
or a scope boundary. A nonsignificant result, a repeated model run, a technical
adjustment, or a study's finite scope is not automatically a limitation; retain
it only when it identifies a specific conclusion or use that the design cannot
support. Do not relabel an unexpected or nonsignificant finding as a method
failure.

Keep related but distinct constraints separate. For example, unequal group
sample sizes may reduce precision or the ability to detect a difference, while
uncertain measurement comparability limits whether group-level construct
differences can be interpreted. The sample-size difference alone does not show
that it caused a nonsignificant finding, and identical item wording does not
establish measurement equivalence. When the evidence identifies multiple
material constraints, state each one and its distinct consequence rather than
letting one stand in for another or dropping it during compression. State only
the consequence supported by the design and diagnostics.

Allocate detail by reader function: the main text names the constraint and the
inference it limits; Methods or Supporting Material carries procedures and
extended numerical diagnostics when those details are needed for reproducibility.
Do not remove a real inference concern just because its diagnostic is technical.
When future work is useful, make each remedy answer a distinct constraint—for
example, a new sample can check whether selected questions work in other
households, while longitudinal follow-up can compare stated willingness with
later behavior. Neither remedy by itself establishes equivalence or causality.
These are conditional distinctions, not a universal checklist of statistical
tests or required data.

## Hidden Inference Checks

At chapter closure, revisit applicable blind spots even when the prose appears fluent:

- Did an extension change the main answer without updating Results or summaries?
- Does a stable direction or ordering stand in for invariance of magnitude, mechanism, or all metrics?
- Are apparent disagreements with prior work actually differences in populations, windows, outcomes, or normalization?
- Is a modeled asset-loss or coverage comparison being promoted to overall welfare, equity, vulnerability, or feasibility?
- Does a limitation name an affected inference, or only promise future research?
- Has the same information been repeated in Methods, Discussion, SM, and response without distinct reader functions?

Use the actual design's counterpart: negative cases and transferability for qualitative work, premises and counterexamples for theory, heterogeneity and evidence certainty for synthesis. Do not manufacture statistical or modeling requirements for another design. Apply [lifecycle-and-routing.md](lifecycle-and-routing.md) for scope and dependency boundaries.
