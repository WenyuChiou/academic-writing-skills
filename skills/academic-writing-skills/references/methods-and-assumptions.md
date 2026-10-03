# Methods and Assumption Provenance

## Contents

1. Scope and reader functions
2. Separate origin, application, and evaluation
3. Explain consequential choices
4. Hypothetical examples
5. Design-dependent hidden failure checks
6. Scope-aware revision checks

## Scope and Reader Functions

Methods explains how the study produces the evidence needed to answer its questions, with enough detail to understand and reproduce the consequential procedures. Use the functions below to plan the requested unit, not as five mandatory subsections. Adapt them to the actual design using [study-design-adapters.md](study-design-adapters.md).

| Reader function | Information to supply when relevant |
|---|---|
| Understand the overall approach | The units studied, the intended comparison, and how the main steps connect to the research purpose. |
| Understand the inputs | Data sources, selection, measurement, and material transformations or assignments. |
| Follow the procedure | Inputs, operations, outputs, and relevant sequence or dependencies; define symbols before using them. |
| Understand consequential choices | What comes from evidence, what the researchers choose, why the choice is appropriate, and what remains assumed. |
| Understand the evaluation and design | The actual comparison baseline, diagnostics, calibration, validation, uncertainty, or sensitivity procedures relevant to the design and claims. |

Begin a procedural paragraph by making its role clear, then explain how it works and any consequential rationale. Introduce prerequisites before dependent operations rather than making readers reconstruct the sequence from later text. Do not add an extended defense of every routine step. Main text must retain the essential logic; a supplement can hold detailed settings or derivations but cannot replace the explanation needed to follow the method.

## Separate Origin, Application, and Evaluation

A sourced parameter is not an assumption-free parameter. Check three independent questions:

1. **Origin:** Where did the value, distribution, relationship, or rule come from?
2. **Application:** How is it used here, and what additional choices make that use possible?
3. **Evaluation:** What evidence assesses that use, and what does the assessment actually establish?

These categories can coexist within one setting. For example, a value can be fitted to data, transferred to another population under an assumption, and examined in a sensitivity experiment without being externally validated.

| Origin | Report accurately | Do not imply |
|---|---|---|
| Observed or measured | The source, relevant unit, and any measurement or preprocessing needed for its use. | That synthetic assignments are observed household or site records. |
| Empirically estimated or fitted | The data and estimation procedure supplying the value or relationship. | That cross-sectional fit identifies temporal dynamics or a causal mechanism. |
| Calibrated | The parameters adjusted, calibration target or objective, data, and procedure. | That fitting a target validates every model component or an independent prediction. |
| Adopted from a study, manual, or default | The exact setting supplied by that source and its relevance to the present use. | That a qualitative rationale supplies a numerical value, or that a default was estimated locally. |
| Author-assumed or simplified | The chosen rule or value and a concise, study-specific rationale. | That it is empirically identified merely because a related concept has a citation. |
| Scenario or sensitivity setting | The experimental change, comparison baseline, and purpose. | That a tested range is an estimated confidence interval or that robustness proves a rule correct. |

Application assumptions may concern scale, population or time transfer, assigning a common value, holding a variable fixed, independence, an operational threshold, or the form of an update rule. Identify the actual assumption rather than calling every setting either “data-based” or “assumed.” An unknown origin remains unverified until checked; do not silently classify it as an author assumption.

Verify what each citation supports: a number, an equation, a qualitative rationale, institutional background, or an evaluation claim. A citation supporting one role does not automatically support the others. Keep code verification, calibration, empirical validation, and sensitivity analysis distinct. A represented mechanism is not evidence that the mechanism caused the observed real-world outcome.

## Explain Consequential Choices

For a setting material to interpretation, retain the relevant parts of this compact record: **what is specified** (including value and units where applicable), **its origin**, **how it is applied**, **the remaining assumption and rationale**, and **what assessment supports it**. Use concise prose or a table when several settings need comparison; do not require a ledger for every routine parameter.

Explain a consequential assumption at its first relevant operational use. State the actual research purpose, evidence limitation, or modeling simplification that motivates it. “This is an assumption” identifies status but does not answer why it was chosen. Do not invent a rationale or describe missing data as the reason unless that is established. Relevant limitations bound interpretation; they do not excuse leaving the operational rule unclear in Methods.

When auditing existing text, first compare its claims with the available source and implementation. Repair overstatement or missing distinctions without silently changing settings. If essential evidence is unavailable, flag the precise unknown and limit the claim. An editing request does not authorize new calibration, sensitivity runs, or replacement parameter values.

## Hypothetical Examples

The following are hypothetical teaching examples, not verified descriptions of any manuscript. They contain no reusable numerical settings or source citations. Copy the distinction, not the scientific claim; use the sample wording only when the corresponding procedure is confirmed.

### A. A fitted starting distribution and an assumed time rule

Suppose survey data supply the initial distribution of a behavioral trait, but the model holds that trait fixed over time.

- **Evidence-derived part:** the fitted initial distribution and its parameters.
- **Assumed part:** temporal constancy. Independent assignment to agents, if used, is a separate choice rather than a consequence of fitting the distribution.
- **Possible wording:** “The initial trait distribution is fitted to survey responses. We hold the trait fixed during the simulation because the survey does not observe within-person changes over time.” The reason is usable only if the survey and modeling rationale actually support it.

Do not compress this into “the behavioral dynamics are calibrated using survey data.” The survey may support initialization without identifying dynamics. Similarly, a manual can supply an initial value, while applying that value to every modeled household remains a simplification.

### B. Institutional background does not estimate an adoption threshold

Suppose a real-world insurance rule motivates different adoption thresholds for two groups, but the researchers choose the numerical intervals.

- **Source-supported part:** the relevant institutional distinction, including the conditions under which the rule applies.
- **Assumed part:** the chosen numerical intervals and their use as a proxy, rather than explicit enforcement of the institution's rule.
- **Possible wording:** “The institutional distinction motivates separate adoption thresholds for the two groups. The intervals are model assumptions; the cited policy does not estimate their values.” State the actual reason for selecting the intervals when it is known.

A citation to the policy alone does not support “thresholds estimated from the policy.” Report any sensitivity assessment separately; unchanged outcomes over tested intervals do not validate the original intervals.

### C. A published community-level formulation applied to individuals

Suppose the model adapts a published community-level memory formulation to update individual perception using local aggregate losses.

- **Source-supported part:** the original formulation at its stated analytical level.
- **Assumed part:** the individual-level application and use of aggregate losses as the signal, reflecting possible influence from community flood experiences as well as personal damage.
- **Possible wording:** “We adapt the community-level formulation to individual perception and use local aggregate losses as the update signal. This assumes that perception can respond to community flood experiences, not only personal damage.” Cite support for that rationale separately from the source of the formulation, where available.

Do not describe this transfer as an empirically validated individual update unless the evidence establishes that claim. Sharing an aggregate signal also does not mean household interaction, information diffusion, or social-network learning is explicitly modeled.

### D. Qualitative sampling and an unsupported coverage claim

Suppose interviews use purposive recruitment and reflexive thematic analysis. The recruitment procedure and coding approach can be documented without establishing population prevalence or saturation. State the actual selection rationale and analytic process; do not add “representative” or “saturation achieved” solely because those words often appear in Methods. Identify researcher position and negative-case handling when relevant and verified.

### E. A theoretical premise and a proved conclusion

Suppose a theorem is derived for a graph with nonnegative capacities. Distinguish the stated premise from the conclusion established by the proof. Do not describe the premise as empirically calibrated, require an experimental dataset, or extend the conclusion to negative capacities without a supporting argument. Reproducibility here means an inspectable derivation and definitions, not necessarily stochastic runs.

## Design-Dependent Hidden Failure Checks

After the procedure and provenance are understandable, inspect the relevant comparisons and dependencies below. These are diagnostic questions, not a requirement to add every analysis, assumption table, or limitation to every design.

| Potentially hidden issue | What to establish before accepting the interpretation |
|---|---|
| A group comparison changes several starting conditions | Which attributes or conditions differ, and what does the design actually isolate? A descriptive group comparison need not isolate a pathway, but should not be presented as its causal effect. |
| A summary conceals the operation order | Are ratios computed before or after aggregation, which weights are used, and is the denominator initial or current? An average of unit ratios and a ratio of totals need not answer the same question. |
| A changing group mean looks like individual change | Do observations follow the same units, or can moving, exiting, or reclassification alter membership? Distinguish within-unit changes from composition changes to the extent the available evidence permits. |
| Repeated runs look like additional empirical observations | Are replications stochastic realizations of the same inputs, new observations, or independent experimental units? Name what the reported variability represents and which uncertainties it does not address. |
| Evaluation shares inputs or fitting targets | Which data and transformations are reused for calibration and evaluation? Disclose that dependence and match the evaluation claim to the actual evidence; independent external validation is not mandatory for every study. |
| An explanation merely repeats a programmed rule | What output or diagnostic supports the explanation beyond the rule itself? Keep represented mechanisms, observed patterns, tested explanations, and untested interpretations distinct, as in [universal-integrity.md](universal-integrity.md). |

Missing evidence for a stronger interpretation is not automatically evidence that the method is wrong. Narrow the claim, identify the unresolved distinction, or propose the targeted diagnostic when appropriate. Do not claim that the diagnostic was run, or run it without the necessary authorization, merely to complete a writing check.

## Scope-Aware Revision Checks

For one sentence or paragraph, check the consequential settings it actually mentions and the prerequisites available in adjacent text. For a Methods subsection, trace its inputs, procedure, outputs, and provenance. For a chapter or manuscript review, additionally reconcile relevant parameter tables, equations, implementation evidence, supplements, and claims of calibration or validation. Do not apply all possible checks to every local edit.

Preserve the accepted or advisor-edited baseline when it already performs these functions. Correct only missing distinctions, unsupported attribution, consequential omissions, or affected transitions. Use [lifecycle-and-routing.md](lifecycle-and-routing.md) for the impact scan; checking a dependency does not expand write authority. If no settings change, do not imply that the model was rerun or newly validated.

For cross-section planning or review, use the handoff checks in [introduction-and-study-context.md](introduction-and-study-context.md). A local procedural or grammar edit does not require that full cross-section review.
