# Study-Design Adapters

## Contents

1. Shared routing questions
2. Quantitative observational and survey
3. Experimental and quasi-experimental
4. Qualitative and mixed methods
5. Computational and simulation
6. AI and LLM studies
7. Evidence synthesis
8. Theoretical, framework, methods, and data papers

## Shared Routing Questions

For every design, ask what entity was observed or generated, what comparison or estimand is intended, what dependencies exist, what uncertainty is represented, and what inference the design permits. Report missing information as an issue; do not assume a conventional choice was used.

## Quantitative Observational and Survey

Check sampling frame, inclusion and exclusion, missingness, variable construction, measurement quality, estimator assumptions, dependence, multiplicity, effect sizes, uncertainty, subgroup size, and whether between-group differences were tested directly.

Do not infer that unequal sample sizes automatically require an independent-sample test. Determine whether observations are paired, nested, repeated, weighted, clustered, or independent and identify the estimand first.

For latent-variable or structural models, distinguish measurement fit, structural fit, standardized and unstandardized coefficients, model comparison, group invariance, and descriptive path comparison. Poor measurement does not forbid reporting, but it narrows construct-level claims.

After item selection, trace the administered instrument → retained items →
score meaning → claims using that score. Removing items can narrow a construct
without changing the original questionnaire. Shared item wording does not prove
measurement equivalence; different retained item sets do not prove that different
questionnaires were administered. Keep these questions separate from whether
structural coefficients can be reported or compared.

For repeated analyses, identify the observation unit, run selection/aggregation,
source of variability, tested contrast, and multiplicity family before reconciling
numbers. Different adjusted p-values can be valid when the same raw test belongs
to different declared comparison families. Distinguish within-model significance
from a direct between-group test, and nonsignificance from equivalence. For counts,
compare event definitions as well as values: affected runs, warning events, and
failed records are not interchangeable. Missing provenance is a verification
question, not proof that a number is wrong.

## Experimental and Quasi-Experimental

Check allocation, controls, treatment fidelity, preregistration when claimed, attrition, interference, power, outcome timing, estimator, missingness, multiple outcomes, robustness, and whether causal language matches identification.

Separate treatment effects from mechanisms and exploratory subgroup findings. Require direct evidence for manipulation checks and mediators.

## Qualitative and Mixed Methods

Check sampling logic, researcher role, consent, data generation, saturation or information power when claimed, coding process, reflexivity, negative cases, quotation support, audit trail, and transferability.

Do not translate theme frequency into population prevalence without a design that permits it. In mixed methods, identify the integration point and show what combining strands adds beyond parallel reports.

## Computational and Simulation

Trace source data → initialization → assumptions → algorithms → coupling or state updates → calibration → validation or verification → scenarios → outputs → claims. Check baselines, stochastic replications, sensitivity, uncertainty, parameter provenance, software versions, and reproducibility artifacts.

Distinguish code verification, empirical validation, predictive performance, scenario exploration, mechanism representation, and real-world inference.

## AI and LLM Studies

Check exact model identifiers and dates, system and user prompts, context construction, conversation state, sampling settings, runs, seeds when available, parser and validation logic, failures, selected-run rules, aggregation, workload, cost when reported, data retention, privacy, and release of reproducibility artifacts.

Map every input-conditioned attribute to the output claim. Test whether a reported pattern could follow directly from prompt conditioning, grouped questions, shared profiles, state leakage, or model architecture. Require ablations only when the claim depends on separating those explanations; otherwise state the limitation.

For repeated synthetic responses tied to the same source profiles, identify whether the estimand is marginal, paired, repeated, or hierarchical before selecting a test. Do not treat separate standardized coefficients as formal evidence of equality or difference without an appropriate comparison.

When input profiles change while a human or other reference remains fixed,
attribute the observed contrast to comparisons under those input conditions.
It does not show how the reference population would respond to changed inputs,
or reveal an internal model mechanism without evidence designed to test it.

## Evidence Synthesis

Check protocol, search sources and dates, eligibility, screening, extraction, risk of bias, synthesis method, heterogeneity, publication bias when relevant, certainty, and traceability from included studies to claims.

Organize findings around questions or synthesis logic, not arbitrary themes. Distinguish evidence volume, consistency, effect magnitude, study quality, and absence of evidence.

## Theoretical, Framework, Methods, and Data Papers

Map premises or requirements → derivation or design → demonstration or evaluation → boundary conditions → contribution. Do not require conventional empirical Results when the manuscript provides an appropriate proof, benchmark, case demonstration, usability assessment, or conceptual argument.

For framework and data papers, distinguish novelty of integration, implementation quality, validation evidence, reusability, and domain impact. Avoid claiming broad utility from a single illustrative case without qualification.
