# Claim-Evidence Audit

Use this reference before writing or revising Abstract, Results, Discussion,
Conclusion, cover letter, and reviewer response. These sections often compress
claims and are therefore prone to overclaim.

## Goal

Every claim should map to evidence and an allowed certainty level.

```text
claim -> evidence -> certainty -> revision
```

## Evidence Types

| Evidence type | Examples | Typical allowed language |
|---|---|---|
| Direct measurement | observed data, lab measurement, survey response | shows, estimates, reports |
| Statistical inference | regression, test, confidence interval | is associated with, suggests |
| Simulation output | ABM, scenario run, model ensemble | suggests, is consistent with |
| Mechanistic rule | method specification, equation, algorithm | follows from, is specified by |
| Literature | cited peer-reviewed result | prior work reports, prior work suggests |
| Expert judgment | advisor note, domain convention | treat as assumption unless cited |

## Audit Table

Use this table when auditing:

```markdown
| Claim | Location | Evidence Source | Certainty Allowed | Problem | Revision |
|---|---|---|---|---|---|
| ... | Abstract sentence 4 | Figure 5b | suggests | "proves" overclaims | replace with "suggests" |
```

## When `.paper/claims.yml` is present (schema-aware audit, v0.2.1+)

If `<paper-repo>/.paper/claims.yml` and `<paper-repo>/.paper/figures.yml`
exist (produced by `paper-memory-builder`), use the structured schema
fields as ground truth instead of re-extracting from the manuscript.
This is how the SKILL.md "ground truth" promise becomes operational at
the workflow level.

**Schema fields → audit-table columns:**

| `claims.yml` field | Audit-table column | Notes |
|---|---|---|
| `claims[].sentence_in_manuscript` | **Claim** | Verbatim claim text — copy as-is. |
| Manuscript section (inferred from sentence; not in schema) | **Location** | E.g. "Abstract sentence 4", "Result §4.2". |
| `claims[].evidence_artifacts` + `claims[].figure_or_table` | **Evidence Source** | A bulleted list of all artifacts. Empty list ⟺ `status: gap` (anti-leakage). |
| `claims[].status` → certainty | **Certainty Allowed** | See status→certainty mapping below. |
| `claims[].risk` | **Problem** | Pre-identified reviewer-pushback risk; use verbatim or refine. |
| Auditor's revision proposal | **Revision** | Per "Certainty Rules" section above. |
| Disposition (1-5) | **Disposition** | Per "Disposition When A Claim Cannot Be Verified". |

**Status → Certainty allowed mapping:**

| `claims[].status` | Allowed language | Action if audit finds the wording stronger |
|---|---|---|
| `supported` | "shows", "demonstrates", "estimates" (direct verbs OK) | None — wording matches evidence strength. |
| `draft` | "suggests", "is consistent with", "appears to", "is associated with" | Soften wording to hedged verbs. |
| `gap` | NONE — claim must be revised or moved | Apply Disposition (1-5). If keeping the claim, populate `evidence_artifacts` and lift to `draft` first. |
| `rejected` | Claim dropped from manuscript | No audit row needed — it's audit-trail only. |

**Status transitions during audit:**

The audit can drive these `claims[].status` transitions (record changes
in `.paper/revision_history.yml`):

- `draft` → `supported`: audit confirmed evidence is solid AND wording is appropriately hedged.
- `draft` → `gap`: audit found the `evidence_artifacts` pointer is stale/missing/insufficient → strip `evidence_artifacts`, add `gap_reason`, hand back to `paper-memory-builder` for refresh.
- `gap` → `draft`: Disposition 5 applied — added evidence, populated `evidence_artifacts`, moved `gap_reason` to `risk`.
- any → `rejected`: Disposition 1 applied — claim dropped, kept for audit trail.

**Cross-checking with `figures.yml`:**

For each claim with `figure_or_table` entries, verify the
corresponding `figures[]` entry in `.paper/figures.yml` lists the
claim id in its `supports_claims:` field. A figure that supports a
claim but doesn't list it (or vice versa) is a cross-reference drift —
flag for `paper-memory-builder` refresh.

```python
# Schema-aware audit pseudocode (wrap in open() for real usage)
import yaml
with open('.paper/claims.yml') as fh:
    data = yaml.safe_load(fh)

for claim in data['claims']:
    if not claim.get('evidence_artifacts') and claim['status'] != 'gap':
        raise SchemaViolation("anti-leakage rule")
    if claim['status'] == 'gap' and not claim.get('gap_reason'):
        raise SchemaViolation("gap claim missing gap_reason")

    # Audit row from schema fields
    row = {
        'claim': claim.get('sentence_in_manuscript', claim['text']),
        'evidence': claim.get('evidence_artifacts') or [],
        'certainty_allowed': STATUS_TO_CERTAINTY[claim['status']],
        'problem': claim.get('risk', ''),
        # ...
    }
```

**Why this matters:** without the schema mapping, the auditor must
re-read the manuscript and re-derive each row, defeating the
"`.paper/` as ground truth" promise. With the mapping, the audit
is a structured pass over the YAML — faster, more consistent, and
machine-checkable for anti-leakage / certainty drift.

## Required Checks

- [ ] The claim has a visible or cited evidence source.
- [ ] The certainty matches the evidence type.
- [ ] The number in the claim matches the source.
- [ ] The source is current, not an old draft or stale run.
- [ ] The mechanism is either observed, specified in Methods, or framed as an
      interpretation.
- [ ] The same claim is worded consistently across Abstract, Results,
      Discussion, Conclusion, and cover letter.

## Disposition When A Claim Cannot Be Verified

If the audit cannot find a source for a claim, do NOT leave it as-is. Choose
one of five dispositions:

| Option | When to use | Example |
|---|---|---|
| 1. Drop | The claim is not load-bearing for the contribution. | A throwaway adjective in Discussion; a parenthetical aside. |
| 2. Hedge | The claim is plausible but evidence is inferential. | "X reduces Y by Z%" → "X may reduce Y" or "X is associated with a reduction in Y". |
| 3. Move to Discussion | The claim is interpretation, not result. | A mechanism narrative misplaced in Results. |
| 4. Add a Limitations caveat | The claim is needed but evidence is partial or indirect. | "We cannot directly observe Z; this finding assumes…". |
| 5. Add the evidence | The evidence exists but is missing from the figure/table/text. | Re-run the analysis or add an SI panel; cite the existing source. |

**Never leave a precise number unverified.** If none of (1)-(5) is possible,
remove the number and rewrite the sentence qualitatively. A vague number is
worse than no number; a reviewer will check the number.

**Record dispositions in the audit table.** Add a "Disposition" column (1-5)
so future audits can verify each previously unverifiable claim was actually
handled and not silently retained.

## Certainty Rules

Use direct verbs only when the study design supports them:

- "we set", "we define", "the model computes" for design choices,
- "the table reports" for displayed values,
- "the regression estimates" for model output.

Use hedged verbs for inferred findings:

- "suggests",
- "is consistent with",
- "appears to",
- "is associated with",
- "may explain",
- "contributes to".

Avoid:

- proves,
- confirms,
- demonstrates, unless the design truly demonstrates,
- ensures,
- eliminates,
- conclusively shows.

## Abstract And Conclusion Gate

Before finalizing Abstract or Conclusion:

1. Extract each claim sentence.
2. Map each claim to a source.
3. Remove claims without evidence.
4. Reduce certainty where evidence is inferential.
5. Verify all numbers against current Results or figures.

## Reviewer Response Gate

When a reviewer challenges a claim:

1. Identify the exact sentence.
2. Locate the evidence source.
3. Decide whether the claim should be defended, hedged, moved, or deleted.
4. Record the manuscript change in the response table.
