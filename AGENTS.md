# Code Review Rules

These rules guide review of repository changes; they do not authorize editing
manuscripts, running paid or live research evaluations, or publishing changes.

- Review the actual base-to-head diff and trace affected skill instructions,
  references, scripts, schemas, tests, and their consumers. Check that routing,
  declared inputs and outputs, cross-file references, and versioned packaging
  remain consistent. Scale checks to the changed contract and its impact.
- Check that changes preserve source identity, citation and provenance, author
  intent, and inference limits. Flag instructions that could invent citations,
  results, or unsupported claims, or present unavailable evidence as verified.
- Inspect representative regression evidence for the changed behavior and its
  failure cases. A fixture or static check proves only what it exercises; do not
  claim live research quality or manuscript acceptance from it.
- Each finding must identify the exact path and line or symbol, trigger,
  consequence, and supporting evidence. Separate confirmed defects from
  untested hypotheses and verification gaps; omit style-only preferences.
