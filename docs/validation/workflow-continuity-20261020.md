# Workflow continuity: bounded candidate validation

## Change and test boundary

Version 1.3.20 already required sentence/paragraph continuity, source fidelity,
and located reader findings. This candidate integrates a process-specific
input/action/output test and a hypothetical example into those existing routes.
It does not add a new checklist, manuscript-state field, audit operation, model,
or automatic semantic gate. A conceptual comparison need not become a pipeline;
grammar-only work stays local and functioning prose can remain unchanged.

Twelve invented cases in `evals/workflow_continuity_cases.json` fixed the source
facts, requested action, and parent criteria before execution. An independent
native agent received the candidate skill and a packet containing only facts,
text, audience, and requests, not the criteria, expected outcomes, or private
manuscripts. It performed one candidate-only batch. The parent then read every
response against the fixed facts and criteria; the table reports that comparison,
not a deterministic score or a human-reader experiment.

## Observed findings and parent assessment

| Case | Actual response or preserved boundary | Parent assessment |
| --- | --- | --- |
| RC01 | Move production of the corrected series before its forecast use; the supplied scan does not settle the dependency. | Criteria met; the paragraph handoff is repaired with the supplied operation, not a connector alone. |
| RC02 | Diagnose unsupported `Then`; do not substitute simultaneous execution. | Criteria met; actual execution order remains unknown. |
| RC03 | Users select variables once per run; a service updates values daily. | Criteria met; actor, frequency, and variables/values stay distinct. |
| RC04 | Calculate forecast, then record error without stopping or modifying it. | Criteria met; no invented diagnostic veto. |
| RC05 | Core questionnaire analysis does not require the optional contextual module. | Criteria met; no new schedule or statistical-independence claim. |
| RC06 | Request actor, frequency, and check consequence; no replacement asserted. | Criteria met by preserving unavailable facts, not by resolving them. |
| RC07 | Diagnose screening-order contradiction and retain locked wording. | Criteria met; the mismatch stays open pending editing authorization. |
| RC08 | Retain the clear configuration, update, forecast, and missing-value branch. | Criteria met; no redundant bridge or branch relocation. |
| RC09 | Raw measurements enter quality control; corrected measurements drive the forecast. | Criteria met; repair extends to the affected neighboring referent. |
| RC10 | Change only `was` to `were`; preserve 4°C and the assay sentence. | Criteria met; no broader rewrite or scientific-validation claim. |
| RC11 | Retain the explicit conceptual contrast. | Criteria met; no imposed workflow or experimental structure. |
| RC12 | Retain complete-file prerequisite, missing-file stop, and optional report-only diagnostic. | Criteria met; supported conditional connectors remain. |

The full response artifact has SHA256
`7beb72c2e474ae304af65c8dfb60394122e46d65d8b6816e182b0f2262576174`.
The candidate guidance was frozen for this batch. Its inherited CRLF endings
were normalized to the repository's required LF without changing the prose;
the agent verified the final three guidance hashes. No feedback correction or
case rerun was needed after the batch. No real terminology scan of these proposed
passages was run: RC01's scan result is a supplied scenario premise, not a claim
that the test agent executed that audit.

## Deterministic checks and limits

- New fixture/routing/package suite: 14 passed and one stale-manifest failure
  before synchronization; the full final suite passed after hash synchronization.
- Full source suite: 255 passed, 2 skipped, Python 3.14.0 on Windows in UTF-8 mode.
- Existing bundled regression runner: all 27 checks passed.
- Public adapter: 50 files verified; version 1.3.21 ZIP built and hashed.
- Skill frontmatter validation passed. Schema, operation signatures, and public
  file closure are unchanged.

Fixture checks establish case registration and package coherence. The behavior
assessment establishes only what was observed in one candidate batch with parent
review. It is not a baseline/candidate comparison, independent replication,
measured improvement, general human comprehension, or scientific/implementation
validation. A fluent paraphrase or a structured `checked` entry still cannot
prove honest reading. Open source facts and author locks must remain visible
when the skill is used on a real manuscript.
