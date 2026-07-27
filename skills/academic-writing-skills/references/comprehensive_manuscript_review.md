# Comprehensive Manuscript Review

Use this workflow when the user asks for a full-manuscript review, a
top-to-bottom check, a paper-ready decision, or a final submission gate. It is
not a sampled copyedit. Every level must be checked in order, and the edited
manuscript must then be checked again in reverse order.

## 1. Establish Authority Before Editing

Record the authoritative source for:

- journal limits and section order;
- manuscript, supplementary material, and standalone submission files;
- sample and subgroup counts;
- model, treatment, scenario, and dataset names;
- analysis versions, run counts, units, and statistical thresholds;
- figures, captions, tables, and computational workload records.

Create or refresh the relevant `.paper/` files. Do not reconcile a conflict by
choosing the most convenient value. Resolve it against the source record.

## 2. Forward Pass: Document To Sentence

Review the manuscript in this order. Do not skip to sentence polishing while a
higher level is unresolved.

| Level | Required questions | Completion evidence |
|---|---|---|
| Document | Are all required artifacts present, current, and correctly ordered? | File inventory and authoritative-version record |
| Heading hierarchy | Does each parent heading lead directly to its intended subsection or deliberate overview? | Heading tree and orphan-text check |
| Section | Does each section perform its expected function without material belonging elsewhere? | One-line function for every section and subsection |
| Paragraph | Does each paragraph have one defensible role and hand its key noun, contrast, or question to the next paragraph? | Paragraph-role and handoff notes |
| Sentence | Does every sentence add a claim, method, evidence, interpretation, transition, scope condition, or necessary definition? | Sentence-level disposition for anything redundant, vague, or displaced |
| Terms and abbreviations | Is every term stable, every abbreviation defined in each independent artifact, and every model name shown at the right level of detail? | Terminology, abbreviation, and model-identity ledgers |
| Displays and pagination | Do figures and tables remain interpretable after page breaks, scaling, and separate export? | Rendered-page inspection and cross-artifact hash or content comparison |
| Evidence provenance | Can every number, workload value, and strong claim be traced to a source record visible to the reader or retained in the evidence ledger? | Claim-evidence and workload-provenance records |

### Heading And Orphan-Text Gate

- Body text must not sit between a numbered parent heading and its first
  subsection merely because it was written earlier.
- A section overview is allowed only when it has a distinct function that is
  not duplicated in the first subsection.
- Record the expected paragraph count when the author specifies one. Confirm it
  after edits and after rendering.

### Paragraph And Transition Gate

A transition is conceptual, not decorative. A connector such as "however",
"therefore", or "moreover" does not repair a missing relationship.

For each adjacent pair of sentences and paragraphs, identify at least one
handoff:

- repeated scientific subject;
- explicit cause or consequence;
- contrast on the same comparison axis;
- narrowing from background to gap;
- gap to study response;
- result to interpretation;
- limitation to remedy.

If the reader must infer what a generic word means, replace it with the actual
object. Words such as "variation", "difference", "performance", "agreement",
"this", and "these results" require an explicit referent when more than one
interpretation is possible.

### Sentence-Necessity Gate

Retain a sentence only if it performs at least one necessary function:

1. scientific claim or context;
2. method or reproducibility detail;
3. evidence;
4. interpretation;
5. transition that names the relationship;
6. scope, limitation, or qualification;
7. definition needed for subsequent reading.

Move a sentence when its function belongs in another section. Delete it when
it merely restates the previous sentence without adding precision.

## 3. Identity Ledgers

### Abbreviation Ledger

For every abbreviation, record:

| Long form | Abbreviation | First use in main text | First use in each standalone artifact | Reuse justified? |
|---|---|---|---|---|

Abstracts, highlights, cover letters, graphical abstracts, and supplementary
files may be read independently. A definition in the manuscript does not
automatically define the term in those artifacts. Avoid an abbreviation when
it appears only once or when the long form fits the artifact limit.

### Model Or Treatment Identity Ledger

Separate:

- display name for prose;
- shortened display name for narrow tables or figures;
- technical identifier for reproducibility;
- access path or provider;
- version or date when relevant.

Use the display name in prose. Put technical identifiers in Methods or a
reproducibility table, not in redundant parentheses after the display name.
When a shortened table label is necessary, define that shortening once.

## 4. Display And Page-Break Semantics

Visual presence is not enough; the display must retain meaning.

- Repeat genuine column headers on every continued page of a data table.
- Do not repeat a survey question or data row as though it were a header.
- Keep captions with the display they label and ensure the full label remains
  inside the page boundary.
- Prevent a data row from splitting when the split destroys its meaning.
- Inspect the rendered first and last row on every page of a continued table.
- Check that embedded and standalone figures show the same state, labels, and
  numbering.
- Treat a thumbnail ambiguity as a prompt for higher-resolution inspection,
  not immediate evidence of an error.

## 5. Workload And Reproducibility Provenance

Runtime, tokens, costs, calls, and hardware are evidence-bearing results even
when reported only for reproducibility.

- Require a source record for every reported row.
- Do not copy one system's workload into another system's row.
- Treat identical values across different models, providers, or hardware paths
  as a duplication warning that requires verification.
- Distinguish local hardware from provider-managed infrastructure.
- If a record is unavailable, state that it was unavailable rather than
  estimating or silently omitting the limitation.
- Do not use incomparable tokenizers, access paths, or wall-clock measures to
  claim relative efficiency without a valid design.

## 6. Reverse Pass: Sentence To Submission Package

After editing, check in the reverse direction:

1. Re-read every changed sentence in its paragraph.
2. Re-read every changed paragraph with its predecessor and successor.
3. Confirm the section still performs its intended function and retains any
   required paragraph count.
4. Confirm Abstract, Conclusion, Highlights, cover letter, and supplementary
   text use the final terms and claims.
5. Re-render every changed document and inspect affected pages plus adjacent
   pages.
6. Re-run number, abbreviation, citation, figure, table, and review-markup
   checks.
7. Rebuild the submission package from the authoritative files.
8. Verify archive integrity, manifest entries, and checksums after the rebuild.

## 7. Paper-Ready Stop Rule

Do not label a manuscript paper-ready while any level is failed, unknown, or
unchecked. Report three states separately:

- **technical paper-ready**: manuscript content, structure, displays, and files
  pass the review;
- **author action required**: declarations, ethics, authorship, or approvals
  remain;
- **submission-ready**: both the technical gate and all author actions are
  complete.

The final review note must list:

- checks performed;
- substantive corrections made;
- unresolved items and their owner;
- rendered page counts;
- package or manifest verification;
- any judgment that could not be automated.
