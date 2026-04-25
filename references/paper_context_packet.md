# Paper Context Packet

Use this packet to reduce repeated token use across long manuscript sessions.
Instead of rereading the full paper every time, future agents can load these
compact `.paper/` files first.

## Recommended Files

```text
.paper/
  context.md
  figure_inventory.md
  claim_evidence_ledger.md
  journal_format.md
  style_overrides.md
  reviewer_comments.md
  submissions_log.md
```

## context.md

Purpose: one-page orientation for the manuscript.

Suggested structure:

```markdown
# Paper Context

## Working Title

## One-Sentence Contribution

## Research Questions

## Hypotheses Or Directional Expectations

## Method Summary

## Main Findings

## Key Terms And Definitions

## Current Manuscript State

## Known Risks Or Open Issues
```

Rules:

- Keep it concise enough to load in every future session.
- Prefer claims already backed by the claim-evidence ledger.
- Update it after major Results, Discussion, or reviewer-response changes.

## figure_inventory.md

Purpose: prevent figure-text mismatch.

Suggested table:

```markdown
| Figure | Panels | What It Shows | Key Numbers | Source Script/Data | Status |
|---|---|---|---|---|---|
| Figure 1 | a-c | Study area and exposure | n/a | scripts/map.py | draft |
```

Include units, scenario names, color meanings, and exact file paths when known.

## claim_evidence_ledger.md

Purpose: keep claims, evidence, and certainty aligned.

Suggested table:

```markdown
| Claim | Section | Evidence | Certainty Allowed | Missing Check | Revision |
|---|---|---|---|---|---|
| Adaptation reduces renter damage. | Results | Figure 5b, Table S2 | suggests | verify latest run | add mechanism |
```

Use `claim_evidence_audit.md` for the detailed rules.

## reviewer_comments.md

Purpose: preserve reviewer-response state across sessions.

Suggested table:

```markdown
| ID | Reviewer Comment | Anchor Text | Response Strategy | Manuscript Change | Status |
|---|---|---|---|---|---|
| R1.1 | ... | Section 2 paragraph 3 | accept | added sentence | done |
```

## submissions_log.md

Purpose: record what was submitted and when.

Suggested table:

```markdown
| Date | Journal | Version/Commit | Submission ID | Notes |
|---|---|---|---|---|
| YYYY-MM-DD | Journal Name | abc1234 | JID-0000 | initial submission |
```

## Maintenance Rules

- Update the packet after each major manuscript revision.
- Do not use the packet as evidence if it conflicts with the actual manuscript,
  figures, code output, or journal guidelines.
- When in doubt, refresh the relevant packet file from the source material.
