# Project State and Authority

## Contents

1. Authority hierarchy
2. Managed-project records
3. Lock and change rules
4. Issue and version states
5. Minimum operating procedure

## Authority Hierarchy

Create a project-specific hierarchy instead of assuming that one universal source order fits every study. A useful default is:

1. verified primary evidence: raw or processed data, analysis outputs, equations, tables, figures, transcripts, source corpus, or formally approved metadata
2. current Methods and Results tied to that evidence
3. current Discussion and limitations
4. current summaries: Abstract, highlights, Conclusion, conference abstract, cover letter
5. historical drafts or related manuscripts used only as references

Override this order when the author identifies a different authoritative source. Record the exception.

Do not infer a fact from typography, filename, author order, an asterisk, a previous paper, or a stale summary. Mark it unknown until a source resolves it.

## Managed-Project Records

Maintain one `manuscript_state.json` or an equivalent project record containing:

- project identity, manuscript archetype, lifecycle stage, and review maturity
- active artifacts and historical references
- authority sources and their scopes
- manuscript contract: gap, task, questions or objectives, outcomes, contribution, and nonclaims
- semantic locks and terminology rules
- language variant, protected technical terms, allowed repetition, and project-discouraged phrases
- facts and metadata with sources
- gap–question–method–evidence–claim alignment entries
- design dimensions and reporting-field coverage
- decisions and open issues
- release candidate and required checks

Use `assets/manuscript_state_template.json` as a starting point. Keep the state beside the manuscript project, not inside this skill.

Treat the style profile as project guidance, not proof that every registered phrase is wrong. Preserve technical terms and author-approved wording even when a deterministic prose audit reports frequent use.

## Lock and Change Rules

Use an exact lock only for content the user has explicitly finalized or that must remain verbatim, such as a formal research question. Use a semantic lock when wording may vary but the scientific task and scope must remain stable.

Before changing a lock:

1. explain the proposed semantic change
2. identify affected sections and artifacts
3. obtain authority from the user or designated source
4. record that the new decision supersedes the old one
5. run the applicable impact gate

Do not change locked meaning merely for parallel sentence structure, stylistic variety, or word-count reduction.

## Issue and Version States

Record issue status as `OPEN`, `RESOLVED`, or `WAIVED`. A waiver must include the authority, reason, affected claim, and remaining risk.

Use severity independently from scope:

- `S0`: formatting only
- `S1`: local readability
- `S2`: plausible misunderstanding or local inconsistency
- `S3`: main argument, reproducibility, cross-file, or submission-integrity risk
- `S4`: research question, evidence validity, major conclusion, ethics, or formal metadata risk

Record evidence status as `CONFIRMED`, `PROBABLE`, or `UNVERIFIED`.

Maintain one active release candidate. Mark every other draft as historical, superseded, or reference-only. Do not use filenames such as `FINAL` as evidence of readiness.

## Minimum Operating Procedure

1. Locate the active files and relevant sources.
2. Populate or update the project state.
3. Run `audit_manuscript_state.py` before substantive work.
4. Resolve source conflicts or retain them as explicit issues.
5. Perform the requested review or revision.
6. Update affected state entries and run impact checks.
7. Run the functional-completeness retrospective.
8. Certify readiness only if the release gate passes.
