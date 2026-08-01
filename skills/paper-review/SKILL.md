---
name: paper-review
description: Review journal-paper drafts for Prof. Ethan Yang's students and collaborators using an evidence-safe Ethan-style internal-review overlay for coupled natural–human systems, water resources, agent-based modeling, catastrophe and flood modeling, hydrodynamics, model uncertainty, and GenAI or LLM studies. Use when the user requests this lab-specific review style, uploads a relevant draft for review or critique, asks to assess a revision round, or wants prior PI comments checked. Supports partial drafts and R1–R4 reviews. Do not use for grants, cover letters, response-to-reviewer documents, unrelated fields, or generic academic editing when the lab overlay is not requested.
---

# Paper Review Overlay

## Base Workflow

Use `academic-writing-skills` as the manuscript-integrity base. Apply this skill only as a conditional reviewer, study-design, domain, and project-history overlay. The base skill determines what makes the manuscript defensible; this overlay determines which specialized questions to ask, how to calibrate the internal-review round, and how to organize an Ethan-style review memo.

Do not claim to be Prof. Ethan Yang or write `REVIEWER: Ethan Yang`. Describe the output as an `Ethan-style internal review calibrated to supplied or archived review patterns`.

Do not edit the manuscript unless the user authorizes revision. A request to review, critique, or comment is non-mutating.

## Establish the Review Basis

Before reviewing, identify:

- the manuscript and companion artifacts in scope
- review-only versus editing mode
- manuscript archetype and actual study design
- applicable water, CNHS, ABM, flood, modeling, or AI domain
- explicit review round, if supplied
- prior draft, prior comments, tracked responses, and issue status, if available
- target venue or reporting standard, if supplied
- exact project identity, if any

Prefer an explicit R1–R4 label. If the round is not supplied, use `developmental`, `substantive`, `integration`, or `submission` rather than inferring a round from prose quality or comment count. Cross-round claims such as `fixed` or `not fixed` require prior-round evidence.

Read [overlay-contract.md](references/overlay-contract.md) for precedence, comment strength, evidence safety, and output behavior. Read [round-calibration.md](references/round-calibration.md) only when review maturity or cross-round progress is in scope.

## Select Only Applicable Modules

Load [abm-computational-and-ai.md](references/abm-computational-and-ai.md) for ABM, coupled models, simulations, ML surrogates, or GenAI/LLM studies.

Load [cnhs-water-and-uncertainty.md](references/cnhs-water-and-uncertainty.md) for CNHS, water policy, framework, equifinality, or water-resources review papers.

Load [flood-and-hydrodynamics.md](references/flood-and-hydrodynamics.md) for flood, catastrophe, hydrodynamic, drainage, sensor, or inundation-model papers.

Load more than one module only when the paper genuinely spans them. Treat named citations as literature candidates requiring verification, never mandatory insertions.

Load [project-precedents.md](references/project-precedents.md) only when the user or manuscript establishes the exact named project and the rule remains current. Project precedents are advisory history, not authoritative facts.

## Classify Every Overlay Comment

Label each material comment by strength:

- **MUST:** research integrity, reproducibility, internal consistency, applicable reporting requirement, or evidence-scope failure
- **SHOULD:** strong study-design or domain convention whose applicability is established
- **QUERY:** missing source, unclear method, factual uncertainty, or author decision requiring confirmation
- **PREFERENCE:** lab, professor, organization, wording, or presentation preference

Also inherit the base skill's scope, severity, evidence status, and issue status. A preference is not blocking merely because prior lab drafts used it.

## Protect Evidence and Interpretation

For every request to explain why a pattern occurs:

1. explain a mechanism in Results only when analysis or directly relevant evidence supports it
2. place a literature-supported interpretation in Discussion with appropriate qualification
3. label a plausible but untested explanation as a hypothesis or possible interpretation
4. when support is absent, flag the missing evidence instead of supplying a mechanism

Do not replace one unverified literature, policy, historical, or terminology claim with another. Ask for or verify the relevant source.

Do not infer AI authorship from writing style. Describe observable problems such as vague claims, stock transitions, unstable subjects, repetitive synthesis, or unsupported mechanisms.

## Run the Ethan-Style Review

Apply the base skill's lifecycle and four-pass integrity review, then add applicable overlay checks:

1. **Framing and contribution:** verify that the stated gap is supported, the study task matches the methods, and the paper explains what its approach adds without overstating novelty.
2. **Study-design reporting:** verify agents, coupling, model logic, calibration, validation, uncertainty, prompts, model calls, or synthesis procedures as applicable.
3. **Domain precision:** verify definitions, units, mechanisms, model capabilities, policy context, and field-specific distinctions against available evidence.
4. **Figure and equation audit:** verify symbols, subscripts, panels, captions, axes, data exchange, scenario counts, and text–visual agreement.
5. **Round regression:** when prior material exists, verify resolved, unresolved, regressed, and newly introduced issues.
6. **Reader synthesis:** ensure each stated question or objective has a substantive answer and that summaries reflect the final evidence.

Numbered italicized questions, explicit question signposts in Results, section-order templates, public repositories, supplementary placement, wording bans, and paragraph-count rules are preferences or conditional requirements unless a venue, reporting standard, or current project decision makes them mandatory.

## Output Format

Adapt the memo to the available artifact. Do not create comments for absent sections or invent findings to meet a quota.

### Header

```text
REVIEW PROFILE: Ethan-style internal review
PAPER: [title]
MODE: [review only / authorized revision]
STAGE OR ROUND: [developmental / substantive / integration / submission, or explicit R1–R4]
SOURCE BASIS: [current draft, prior comments, companion files, unavailable sources]
READINESS: [primary bottleneck and named next-stage readiness]
```

### A. Cross-Round Status

Include only when prior-round material is available. List resolved, unresolved, regressed, and newly introduced material issues.

### B. Priority-Ranked Action Items

For each item, give:

```text
[number]. [section or artifact] — [label]
Strength: [MUST / SHOULD / QUERY / PREFERENCE]
Severity and evidence: [S0–S4; confirmed / probable / unverified]
Problem: [specific evidence-backed issue]
Required action or decision: [bounded next step]
Blocking?: [yes/no, and for which next stage]
```

Stop when all material issues are covered. Do not target a fixed number.

### C. Section-Linked Comments

Follow the manuscript's actual structure. Begin each section with a brief structural verdict, then anchor comments to short quoted fragments. Distinguish an accuracy or validity issue from a lab preference.

### D. Writing and Presentation Flags

Include only representative, material cases. Give a rewrite direction unless the user authorized rewriting.

### E. Next-Round Instruction

State exactly which artifacts and issues should be addressed before the next review.

### F. Functional-Completeness Retrospective

Use the base skill's retrospective. Explicitly name the lifecycle stage, modules and precedents loaded, prior-round evidence available, artifacts covered, unresolved sources, impact propagation, and readiness limits.

## Safety and Restraint

Be direct, technically precise, and respectful. Do not perform persona imitation, express frustration, or use humiliation as a teaching device. Never suppress a newly found validity, ethics, evidence, or metadata issue because the draft is in a late round.

Use the appropriate document or PDF skill for extraction, comments, tracked changes, and rendering. Do not certify a visual or prior-comment check that was not performed.
