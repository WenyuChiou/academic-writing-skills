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

## Work with Ethan-Edited Drafts

Use the latest Ethan-edited draft as the baseline and preserve wording that is
already accurate and clear. Make the smallest revision that resolves each
comment, then check whether the change alters related manuscript, Supporting
Material, figure, table, or response claims.

Keep the reviewer response, the manuscript or Supporting Material revision, and
the reply to Ethan separate. Write replies to Ethan in concise first person,
using forms such as `I revised`, `I clarified`, or `I added`. If a comment gives
a writing strategy, thank him briefly and say where the strategy was applied. If
he says that wording is unclear, explain the intended meaning in plain language
and then provide the revised wording. If he asks why a requested feature is not
represented, place the reason immediately after the limitation or refusal.
Formatting checks, confirmations, and closing acknowledgments should receive a
short reply rather than a repeated scientific explanation.

When Ethan asks `so what?` about a sensitivity or robustness test, require the
response to state, in order: what numerical result changed, which named pattern
or conclusion remained or changed, when specification choice is at issue which
setting is used in the formal model and its independent basis, and how the
manuscript or Supporting Material presents the test. Do not answer with vague
phrases such as `this finding`, `the ordering`, or `the conclusion` without
restating the substantive comparison.

When Ethan questions `current`, `revised`, `updated`, or `original` setting,
first determine whether the phrase names a locally defined whole-model version
or hides a one-factor comparison. Preserve an advisor-defined whole-model label
when both versions are explicitly introduced. For a one-factor test, replace the
label with the actual value, interval, distribution, rule, or event sequence.
Do not perform a global terminology replacement across unrelated comments.

When a final-decision sentence is needed, place it after the sensitivity result
and its meaning. Vary the transition and sentence structure across nearby
responses. Treat a stable pattern or conclusion as evidence of robustness, not
as proof that the baseline setting is preferable. State the independent basis
for the adopted setting when one has already been established; otherwise say
that the sensitivity analysis does not determine the setting choice. Do not add
a new rationale merely to make the decision sound stronger. Update the reply to
Ethan after the revision so that it reports the actual decision or unresolved
selection basis rather than only saying that the response was clarified.

## Output Additions

When this overlay is active:

- set `REVIEW PROFILE` to Ethan-style internal review
- include `MUST / SHOULD / QUERY / PREFERENCE` for material items
- include cross-round status only with prior evidence
- end with exact next-round instructions
- state which neutral method and domain modules also ran
