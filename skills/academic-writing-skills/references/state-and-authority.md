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

The record supplies context, not review scope. For local work, consult only relevant source, lock, terminology, and decision entries; reuse current evidence whose inputs are unchanged. Do not initialize a new record, reopen every release gate, or restart a whole-paper audit simply because the task is another paragraph in an ongoing project.

Treat the style profile as project guidance, not proof that every registered phrase is wrong. Preserve technical terms and author-approved wording even when a deterministic prose audit reports frequent use.

Register established open compounds in `style_profile.preferred_open_compounds` when a project or venue requires them to remain open even before another noun. The prose audit then reports registered hyphenated variants for contextual review.

Use machine-auditable registry fields consistently:

- semantic lock: `id`, `kind` (`EXACT` or `SEMANTIC`), `canonical`, optional `required_roles`, and optional `forbidden_variants`
- terminology entry: `id` or `concept`, `preferred`, optional `prohibited` (the audit also accepts legacy `avoid`), and optional `scope_roles`
- fact entry: `id`, `value`, `source_id`, optional `expected_strings`, optional `forbidden_strings`, and optional `scope_roles`

Do not store a prose reminder such as `term/rule` inside `semantic_locks` and then claim the lock audit passed. Convert it to the schema above or record it as a decision that requires manual verification. A registry entry that cannot be audited must be reported as such rather than silently skipped.

### Persistent terminology procedure

Curate recurring constructs, consequential metrics, abbreviations, and easily
confused labels, not every ordinary word. Keep the one shared record beside the
paper. Its existing `project`, `artifacts`, `contract`, `facts`, `alignment`,
`decisions`, and `issues` supply authority and continuity; an outline or check
record can reference them instead of copying a second inventory.

Use the existing project record or equivalent glossary, not chat recall, as the
shared vocabulary for sustained writing. Bind it to the active manuscript's
identity and authoritative version. A copied record or a matching topic does not
establish authority for another paper. For a one-off edit, relevant author-supplied
terms can stay inline; do not require a new project file.

1. Before writing, read the relevant confirmed concepts, definitions, preferred
   terms, explicitly allowed variants/acronyms, and scope. Identify concepts that
   must remain distinct. Record definition/source and confirmation provenance
   where needed; do not invent a definition from an unfamiliar label.
2. During writing, preserve names of defined concepts rather than rotating
   synonyms. An author's explicit terminology decision or designated authoritative
   definition can confirm an entry; an assistant's draft usage cannot. Keep new
   suggestions and unresolved meanings separately, such as in
   `terminology_proposals`, with their source and reason. If an entry is explicitly
   marked `PROPOSED`, do not treat it as confirmed on resumption. Existing legacy
   entries without status retain their configured scan behavior, not invented
   approval provenance.
3. When a new phrase appears, determine whether it is an approved variant, a
   distinct concept, or a possible naming inconsistency. Propose the smallest
   repair or ask only when the unresolved meaning affects the requested claim.
   Do not ban every new phrase or merge willingness, observed behavior, welfare,
   and other distinct constructs. Protect quotations, reference titles, official
   instrument names, and valid inflections in their actual contexts; do not make
   a word globally exempt merely because one occurrence is protected.
4. At the requested section boundary, reconcile new confirmed choices and pending
   proposals. For an author-approved rename, identify affected prose, displays,
   and companion files before changing them. Conflicting confirmed decisions stay
   unresolved until authority resolves them; recency alone is not approval.
5. Check the exact deliverable against the current record. Retain candidate and
   state hashes, rule versions/hashes, and checked scope in audit evidence when
   supported. A changed registry, rule, scope, or candidate invalidates related
   prior evidence even if the paragraph itself is unchanged.

An empty registry needs a bounded proposal pass over available authoritative
material only when the task requires terminology coordination. It does not block
a grammar repair. Report confirmed applicable entries, unresolved concepts, and
literal scan findings separately. `PASS` means no configured scan findings, not
complete vocabulary coverage or semantic correctness. If artifact role is unknown,
disclose that limit; do not claim role-specific clearance. The local CLI can resolve
a role when `--label` exactly matches an active artifact ID in the supplied state.
Quoted matches remain contextual diagnostics; scripts do not establish whether
two previously unregistered expressions name the same concept.

For a confirmed entry, retain `definition`, `allowed_variants`, and
`confirmation_source` alongside the existing auditable fields when these are
needed to distinguish meanings. For example, an author's decision may confirm
`intention to enroll` as a reported likelihood while reserving `enrollment` for
observed registration. The two are not synonyms. A suggested replacement belongs
in `terminology_proposals`, with its question/source and `status: PROPOSED`,
until authority resolves it. These descriptive fields support human/agent
judgment; literal scans do not verify a definition or confirmation source.

On resumption, match the paper identity and active version, then read only the
relevant entries and open decisions. At a chapter boundary, reconcile new
confirmed decisions and still-pending proposals in this same record. A changed
definition can invalidate a comparison even when its sentence is unchanged;
identify affected Methods, displays, summaries, and checks before reusing old
evidence. Do not restart unrelated checks. Use the stage procedure in
[execution-and-acceptance.md](execution-and-acceptance.md) to record that boundary.

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
2. Reuse relevant project-state entries; initialize or update a record only when sustained coordination needs it.
3. Run `audit_manuscript_state.py` for state validation or integration/release work when relevant, not as a mandatory new full-state audit for every local edit.
4. Resolve source conflicts or retain them as explicit issues.
5. Perform the requested review or revision.
6. Update affected state entries and run impact checks.
7. Run the functional-completeness retrospective.
8. Certify readiness only if the release gate passes.

Report check coverage separately from issue/evidence status: checked, not applicable, outside requested scope, or source unavailable/unverified. An excluded artifact is neither passed nor automatically a blocker for completing a narrower task; it does limit any broader readiness claim.
