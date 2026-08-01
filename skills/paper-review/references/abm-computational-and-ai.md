# ABM, Computational, and AI Review Module

## Agent-Based and Coupled Models

Check:

- real-world entity represented by each agent
- agent state, observations, available actions, decision rules, timing, and heterogeneity
- initialization, calibration, validation, baselines, counterfactuals, and sensitivity analysis
- coupling direction, exchanged variables, update frequency, and feedback delays
- agreement between the architecture figure, equations, code description, and results
- stochastic replications, aggregation, uncertainty, and reproducibility artifacts

Do not equate bidirectional coupling with real-time exchange. Verify the paper's actual update schedule.

For learning agents, check state space, action space, reward, update rule, exploration, parameters, convergence criteria, and the added capability relative to simpler baselines.

## Computational Models and Simulations

Distinguish code verification, calibration, validation, benchmark performance, scenario behavior, sensitivity, uncertainty, mechanism representation, and real-world inference. A model may legitimately perform prediction; use `simulation` or `prediction` according to the actual task.

Require exact model and scenario counts across text, figures, tables, and supplements. Check symbol definitions and ensure sensitivity parameters match Methods notation.

## ML Surrogates and Sensors

Check training, validation, and test separation; spatial or temporal leakage; resolution; baselines; uncertainty; domain shift; sensor configurations; missingness; and whether deployment claims exceed the evaluation setting.

Determine the actual source and target tasks or distributions before accepting or rejecting `transfer learning` terminology.

## GenAI and LLM Studies

Check exact model identifiers and access dates, prompts, context and state sharing, sampling settings, runs, parser logic, failures, selected-run rules, aggregation, workload, cost when reported, privacy, data retention, and reproducibility artifacts.

Map conditioning variables to claims. Ask whether a finding could be induced by supplied profiles, prompt grouping, label leakage, shared history, sampling, or response parsing. Require validation proportional to the claim; a non-LLM baseline, human reference, ablation, or external benchmark may be appropriate depending on the task.

Do not treat LLM consistency as behavioral validity or use model-generated rationales as direct evidence of human mechanisms.
