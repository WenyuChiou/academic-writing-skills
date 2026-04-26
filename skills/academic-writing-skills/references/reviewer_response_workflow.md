# Reviewer Response Workflow

Use this reference for rebuttal letters, response-to-reviewers documents, and
advisor-comment revisions.

## Core Rule

A reviewer response is only complete when the manuscript has a visible change or
the response gives an evidence-backed reason for not changing it.

## Response Table

Build a table with these columns:

```markdown
| ID | Reviewer Comment | Anchor Text | Response | Manuscript Change | Evidence |
|---|---|---|---|---|---|
| R1.1 | ... | Section 2, paragraph 3 | ... | Added sentence on page X line Y | Figure S2 |
```

## Step-By-Step Workflow

1. Number every comment by reviewer and order: R1.1, R1.2, R2.1.
2. Preserve the reviewer comment verbatim.
3. Identify the anchor text, figure, table, or section.
4. Classify the comment:
   - accept,
   - clarify,
   - add analysis,
   - add citation,
   - correct error,
   - disagree with evidence,
   - out of scope.
5. Make the manuscript change first when possible.
6. Write the response after the change exists.
7. Cite the exact location of the change.
8. Run the banned-word and overclaim audit on new text.

## Tone

Use concise, professional language. Avoid performative politeness and avoid
defensiveness.

Good:

```text
We added a robustness check using X. The result is reported in Figure S3 and
does not change the interpretation. The Methods now describe this check on
page 7, lines 142-150.
```

Weak:

```text
We thank the reviewer for this insightful comment and have clarified the text.
```

## Disagreement

Disagreement is acceptable when supported by evidence.

Use this structure:

1. Name the concern.
2. State the evidence or convention.
3. Explain why the original choice remains appropriate.
4. Make a clarifying manuscript change if possible.

Do not write "we respectfully disagree" without an argument.

## Contradictory Reviewer Requests

When reviewers ask for incompatible changes:

1. Name the tension explicitly.
2. Choose the path that best fits the editor's decision, journal scope, and
   evidence.
3. Inform both reviewers through their responses.
4. If needed, request editor guidance in the cover letter.

## Common Failure Modes

- Saying "clarified" with no manuscript change.
- Restating the original text instead of revising it.
- Moving a challenged claim to the supplement without addressing it.
- Adding a citation that does not support the claim.
- Overwriting clean text unrelated to the comment.
- Answering the reviewer but not updating the paper.

## Final Checks

- [ ] Every comment has an ID.
- [ ] Every response has anchor text.
- [ ] Every accepted comment has a manuscript change.
- [ ] Every disagreement has evidence.
- [ ] Contradictory comments are reconciled.
- [ ] New manuscript text passes overclaim and banned-word checks.
