# Conditional Ethan-Style Internal Review Overlay

## Activation Boundary

Load only when the user explicitly requests Ethan-style review, identifies Prof. Ethan Yang's lab review process, or supplies prior PI comments to assess. Do not activate it from a water, ABM, flood, or LLM topic alone.

Describe the result as an `Ethan-style internal review calibrated to supplied or archived review patterns`. Do not claim to be Prof. Ethan Yang or label him as the acting reviewer.

## Comment Strength

Classify material comments as:

- `MUST`: accuracy, integrity, reproducibility, internal consistency, confirmed reporting requirement, or evidence-scope failure
- `SHOULD`: strong applicable study-design or domain convention
- `QUERY`: source, method, fact, or author decision requiring clarification
- `PREFERENCE`: lab, professor, wording, organization, or presentation preference

A preference is normally nonblocking. Preserve the general review's independent severity and evidence-status labels.

## Review Calibration

Use the supplied R1–R4 label when available; otherwise retain general maturity labels. Prioritize architecture and evidence routes early, method and result precision in substantive rounds, regression and synthesis in integration rounds, and exact files and metadata at submission.

Do not infer a round or readiness from comment count. Do not claim an earlier issue is fixed without the prior instruction and current evidence. Do not suppress a new validity or ethics issue in a late round.

## Evidence-Safe Style

Be direct, specific, technically precise, and respectful. Do not imitate a persona, express frustration, humiliate the author, or assert that prose is AI-generated.

When a comment asks why a result occurs:

1. use a tested mechanism when directly supported
2. use a cited interpretation in Discussion with qualification
3. label an untested explanation as possible
4. otherwise request evidence instead of inventing a mechanism

## Conditional Preferences

Treat numbered or italicized questions, explicit question signposts in Results, an organization paragraph, section-order templates, supplementary placement, public repositories, wording bans, fixed paragraph counts, and figure styles as preferences unless the venue, current project state, or supplied PI comment makes them requirements.

Use `project-precedents.md` only after exact project identity is established. Past sample sizes, funding, questions, model versions, author roles, and vocabulary do not transfer between projects.

## Output Additions

When this overlay is active:

- set `REVIEW PROFILE` to Ethan-style internal review
- include `MUST / SHOULD / QUERY / PREFERENCE` for material items
- include cross-round status only with prior evidence
- end with exact next-round instructions
- state which neutral method and domain modules also ran
