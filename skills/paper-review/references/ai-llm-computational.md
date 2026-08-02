# AI, LLM, Agent-Based, and Computational Review Module

## Trigger and Scope

Use for simulations, agent-based models, coupled computational systems, ML models or surrogates, GenAI, LLM-generated data or respondents, LLM agents, prompt studies, or agent evaluations. Load other domain modules when the computational study makes domain-specific physical, behavioral, or policy claims.

## Computational and Agent-Based Models

Trace source data → initialization → state and assumptions → algorithms or decision rules → coupling or updates → calibration → verification or validation → scenarios → outputs → claims.

Check the real-world entity represented by each agent; state, observations, actions, timing, heterogeneity, and decision logic; coupling direction, exchanged variables, update frequency, and feedback delays; baselines, counterfactuals, stochastic replications, sensitivity, uncertainty, software versions, and reproducibility artifacts.

Distinguish code verification, calibration, empirical validation, predictive evaluation, scenario exploration, mechanism representation, and real-world inference. Bidirectional coupling does not necessarily mean real-time exchange.

For learning agents, check state space, action space, reward, update rule, exploration, parameters, convergence or stopping criteria, and the capability added relative to simpler baselines.

## ML and Surrogate Models

Check training, validation, and test separation; spatial, temporal, subject, or profile leakage; preprocessing fit boundaries; baselines; tuning; uncertainty; calibration; domain shift; ablations when needed; and whether deployment claims exceed the evaluated setting.

Determine the actual source and target tasks or distributions before accepting transfer-learning terminology.

## GenAI and LLM Studies

Check exact model identifiers and access dates, provider or local build when relevant, system and user prompts, context construction, conversation state, sampling settings, runs, seeds when available, parser and validator logic, failures, retries, selected-run rules, aggregation, workload, cost when reported, privacy, data retention, and reproducibility artifacts.

Map every conditioned input attribute to the output claim. Test whether a pattern could follow from profiles, labels, prompt grouping, question order, shared history, sampling, filtering, or parsing. Require an ablation only when the claim depends on separating those explanations; otherwise state the limitation.

For repeated synthetic responses tied to source profiles, determine whether the estimand is marginal, paired, repeated, or hierarchical. Do not treat repeated generations as independent human participants.

Separate response reliability or consistency, measurement quality, distributional similarity, task performance, behavioral feasibility, behavioral validity, and real-world generalizability. LLM consistency is not behavioral validity, and generated rationales are not direct evidence of human mechanisms.

## Evaluation and Reporting

Check whether baselines, human references, gold labels, external benchmarks, judge models, or expert ratings match the claim. For LLM-as-judge designs, check judge independence, rubric, position and verbosity bias, calibration, agreement, and human adjudication where required.

Verify exact model, run, scenario, prompt, call, and sample counts across text, tables, figures, supplements, and code. Unknown runtime, tokens, cost, failures, or retention conditions must remain unknown rather than becoming zero.
