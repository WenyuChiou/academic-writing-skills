# Revise the requested comment scope

Use this procedure for edits driven by a Word comment, annotation, or selected
passage. It applies across research designs. A selection limits the default
**edit** scope, not how much context must be **read**. Existing minimal-change
rules still apply; a new note or clean scan cannot prove they were followed.

## Establish the current target before drafting

1. Confirm the latest author/advisor-approved file, its SHA256, effective revised
   wording and the actual comment selection. Read the full comment and reply
   thread with the surrounding prose. Do not substitute the containing paragraph
   for the selection, infer a target from comment text alone, or reuse an ID or
   locator from an older snapshot. Re-read the anchor after any source change.
2. Record a compact boundary: selected text/locator, requested action, unchanged
   surroundings, and any explicit broader instruction. A heading anchor with
   “revise this section” is section-level authorization, not a title-only task.
   A reply belongs to its existing thread; it is not automatically another
   independent request. Read any new clarification rather than discarding it.
3. Distinguish permission to propose wording, edit a file, write a reply and
   resolve a comment. “Discuss first,” “do not edit,” or “no reply/resolution”
   stays binding even when the comment itself suggests a revision. A local
   no-change answer is valid when the current text already meets the request.

The optional read-only `scripts/inspect_comment_targets.py DOCX` reports a
snapshot hash, comment text/thread links, selected XML text, paragraph context
and anchor diagnostics. Use `--expected-sha256 HASH` to reject a stale snapshot.
Read its actual output; knowing the command or finding no language-scan matches
is not anchor verification. This helper is not a registered adapter operation;
consumers need explicit support. It never edits, replies, resolves or authorizes.

Its offsets describe an XML text projection, not Word Range positions, line
numbers or a rendered view. `range` identifies a readable selection, not approval
to rewrite it. `point` needs context and the instruction's scope. Deleted-only
or deleted anchors, missing endpoints/definitions, multiple anchors and unresolved
threads remain uncertain. Do not silently select a nearby sentence. Coordinate
overlapping selections and retain every part of a cross-paragraph selection;
neither means the whole document is unlocked. Fields, drawings, nested paragraphs
and unsupported structures may need a dedicated document editor or inspection.

## Make the smallest sufficient revision

Preserve usable author/advisor wording and existing accepted edits outside the
target. Even within a selection, retain sentences that already perform their
function; its boundaries are not an instruction to rewrite every selected word.
Do not rewrite the introduction, figure orientation, scoring definitions,
method/SM pointers or adjacent sentences just for uniform style or a generic
template. Retain existing reader functions whether they are inside or outside
the selection. Necessary technical repetition is not permission to rename terms.

Expand only for an explicit larger request or a demonstrated fact, cross-reference,
grammar or logic dependency. Locate the affected neighbor, explain why the local
repair would otherwise be wrong or unreadable, and change only that dependency.
Do not use “improving flow” alone as evidence. Respect a specifically locked
neighbor: propose the needed change and mark the dependency unresolved instead
of overriding it. Re-read every affected sentence pair and paragraph boundary.

An advisor's older example supplies style or argument structure, not study facts.
Use current numbers, groups, measures and appropriate wording; do not copy old
values, causal strength or unperformed analyses into the current manuscript.
When a numerical result needs interpretation, connect the supported comparison
to its meaning and relevant question without adding an unrequested explanation.

## Verify the exact candidate and report the actual change

### Test concern closure separately from edit completion

In the existing comment ledger or inline finding, retain the original source
version and selected span, the full concern, the exact current wording and its
locator, and the reason that wording does or does not answer the concern. Keep
an original selection separate from its containing paragraph and from the new
selection: a later rewrite can move a range or change what its ID selects.
The range identifies the target; surrounding prose may supply the answer.

Before saying a comment is addressed, restate what an unfamiliar reader must
be able to understand, then locate that answer in the current reading unit.
For a logic comment, ask whether the original misunderstanding could still
reasonably arise, not only whether the sentence was rewritten. Naming groups
or a classification rule need not explain why their comparison matters; a
connector or a corrected place name need not supply a missing study rationale.
When findings appear to conflict, distinguish outcomes, groups, analytical
levels and tests before inferring a contradiction or a successful repair.

Use a reasoned assessment within that same record:

- **Addressed:** the available current wording answers every part of this
  concern; a justified no-change can qualify. Quote the answer, not just a reply.
- **Partly addressed:** identify both the part answered and the question still
  left to the reader. Do not report the whole thread as complete.
- **Open:** the required relation or correction is still absent or incorrect.
- **Unverifiable:** identify the missing source/selection/context and what
  cannot be judged. A visible grammar correction can still be checked from a
  quoted comment without claiming its original document anchor was verified.

These are concern assessments, not new manuscript-state statuses or Word
resolution actions. Keep ledger status `OPEN` for partial, open or required
unverifiable concerns; use `RESOLVED` only for a verified answer and `WAIVED`
only under the existing authority contract. Grouped replies must preserve each
subconcern's coverage. Distinguish this judgment from edit/format preservation,
word-count checks, language scans and independent-reader evidence. Preserve a
working repair rather than rewriting it to demonstrate activity. See
[evidence-context case 13](evidence-context-cases.md#13-a-rewrite-is-not-concern-closure).

Compare source and candidate at the selected-span level. Identify which sentences
changed and which surrounding wording remained exact. Include any necessary
expansion and its evidence; do not claim an unchanged paragraph if only its topic
was preserved. Reject an otherwise fluent candidate with unexplained out-of-scope
changes. An unchanged candidate must still answer the actual request.

Then check that the repaired unit retains its reader orientation, correct numbers
and meanings, internal/neighboring links and applicable answer to the question.
These are content checks, not a demand to add an SQ label or closing template.
Do not preserve a broken dependency merely to obtain a zero outside-span diff.

For a real DOCX edit, also check the saved revised view, existing revision authors,
comments/reply relationships and usable advisor changes using the document skill.
Never flatten the paragraph, accept all changes or resolve a thread as a shortcut.
Text equality alone does not establish metadata or visual preservation. Missing
checks remain unverified. If only a proposal was authorized, report the proposal
and its exact diff; do not imply the source file, reply or resolved state changed.

### Hypothetical local repair

Source: “Figure 4 compares the two groups. Scores use a 0–100 scale. **Group A
averaged 84.6 and group B 78.2. The difference is 6.4 points. This indicates higher
reported willingness in group A.** The instrument is described in Text S3.”

Assume only the bold text is selected, the author requests connecting result
and meaning, and the current source supports these facts. A sufficient proposal
is: “Group A reported greater willingness than group B, with mean scores of 84.6
and 78.2, respectively, a difference of 6.4 points.” Preserve the two opening
sentences and final SM pointer exactly. Do not add actual purchases, causation,
significance or an old example's numbers. This example is not a prescribed
sentence shape or evidence about any real questionnaire.
