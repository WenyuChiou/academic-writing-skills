# Section-by-Section Checklists

Load only the checklist for the section currently being written or reviewed.

---

## Abstract

**6-Part structure (in order):**

1. **CHALLENGE (2–3 sentences)** — Why does this problem matter *scientifically*?
   Frame the knowledge gap as a scientific question, not a literature gap
   ("nobody has done this").
2. **WHAT (1–2 sentences)** — The tool / framework you built. High-level, no
   technique names yet.
3. **HOW (2–3 sentences)** — How the methodology works. Agent setup, actions,
   long-term objective. Avoid namedropping techniques without stating what they
   do.
4. **WHERE (1–2 sentences)** — Study area. Put it in the **middle**, never at
   the beginning. Study area is a testbed, not the employer.
5. **RESULTS (2–3 sentences)** — Most critical findings in internal logical
   order (temporal → spatial, or damage → financial).
6. **CONTRIBUTION (1 sentence)** — The one advance this study provides.

**Mindset rules**:
- The abstract is a sales pitch, not a mini-paper summary.
- Study area = testbed, not location of interest.
- Every sentence must carry load; delete any whose removal loses nothing.

**Checklist**:
- [ ] Opens with scientific challenge, not a study area or technique name
- [ ] WHERE appears in the middle, not the first sentence
- [ ] No "Monte Carlo" or technique names without explanation
- [ ] Sentences under 35 words
- [ ] No banned words (run `banned_words.md`)
- [ ] Relative terms preferred over raw numbers (unless journal format requires)
- [ ] Contribution is model/data-dependent, not common sense

---

## Introduction

**Funnel structure (4 stages)**:

1. **Grand Challenge (1–2 paragraphs)** — broad societal/scientific challenge
   at global/national scale. Cite authoritative source (policy acts, landmark
   stats) or historical arc of the field.
2. **Literature Review + Gap Identification (2–4 paragraphs)** — thematic,
   not chronological. Each cluster: review → critique → reveal limitation.
   "However," is the standard gap pivot.
3. **Research Objective (1 paragraph)** — direct statement: "To address these
   research gaps, the objective of this paper is to...". Multiple objectives
   as numbered list: "(1)... (2)... and (3)...".
4. **Roadmap (final paragraph)** — "The rest of the paper is structured as
   follows...".

**Before the RQ**: include a directional hypothesis — "We expect X because Y,
given Z". Vague RQs without direction trigger rewrite.

**Checklist**:
- [ ] Opens at broad scale (not study area)
- [ ] Gap pivot uses "However," or equivalent
- [ ] Every cited paper serves a specific argumentative function (no citation
      dumps)
- [ ] Directional hypothesis precedes the RQ
- [ ] RQs are testable (specific, measurable)
- [ ] Roadmap with explicit section numbers

---

## Methods

**Top-down modular structure**:

1. Overview paragraph (what the framework does, module list, SM references)
2. Physical / natural model
3. Human / decision model
4. Coupling mechanism (the key contribution — always explicit)
5. Scenarios and metrics
6. Calibration / validation

**Each module**:
- What it does (1–2 sentences defining the role)
- Data sources (with citations)
- Method / equations (text introduces → equation → "where" definitions)
- Dynamic updates (how other modules modify this one, if applicable)

**Equation presentation**:
- Introduce variables in text BEFORE the equation
- Centered equation with right-aligned numbering
- "where" paragraph defining every symbol
- Move derivations to SM

**Simplifying assumptions**:
- State the simplification
- Give the rationale briefly
- Forward pointer: "(implications discussed in Section X)"

**Checklist (simulation / modeling track)**:
- [ ] Overview states the framework's purpose in one paragraph
- [ ] Coupling or integration mechanism described explicitly (not just implied)
- [ ] Each equation has a "where" paragraph
- [ ] Every SM item referenced with a specific label (Text S1, Figure S2)
- [ ] Simplifying assumptions have forward pointers to Discussion
- [ ] No re-definition of terms defined in Introduction

### Empirical / lab-science track (use in addition or instead)

If the study involves human subjects, wet-lab experiments, clinical data, or
field measurements, also check:

- [ ] Sample size and power justification (a priori if possible)
- [ ] Randomization and blinding procedures (if applicable)
- [ ] Inclusion / exclusion criteria stated with numeric drop-offs
- [ ] Pre-registration reference (OSF, ClinicalTrials.gov, AEA registry, ...)
- [ ] Materials / reagents table with vendor, catalog number, RRID
- [ ] Biological vs. technical replicates clearly distinguished
- [ ] Statistical test assumptions checked (normality, independence,
      homogeneity of variance) and reported
- [ ] Effect sizes with confidence intervals, not just p-values
- [ ] Data cleaning and outlier rules stated before analysis
- [ ] Software version and analysis code availability

### Archival / theoretical / qualitative track

- [ ] Primary sources listed with archive locations and dates accessed
- [ ] Coding scheme or analytical framework described and cited
- [ ] Inter-rater reliability reported if multiple coders
- [ ] Reflexivity / positionality statement if warranted by method

---

## Results

**Dual-scale presentation**: system/basin level + agent/individual level.

**Every paragraph**: Finding → Mechanism → RQ link.

**Transition to the next paragraph**: the first sentence must link back to the
previous finding and introduce the new one (see `writing_principles.md` §1.3).

**RQ-echo opening**: the first sentence of a section should echo the RQ's key
terms without literally saying "RQ1 asks...". This signals what the section is
about to answer.

**Example RQ-echo opening**:
> *To examine how X and Y shape Z for groups A and B, we compare W between the
> X scenario and the Y baseline. [Directional preview of the finding.]*

**Checklist**:
- [ ] Opens with finding, not "Figure X shows..."
- [ ] Every result has a mechanism sentence
- [ ] Every counterintuitive finding has run the 5-step audit
- [ ] No single paragraph/figure bears the entire RQ conclusion —
      synthesis happens at the end of the section
- [ ] Precise numbers in prose are visible on the figure
- [ ] Figure citations specify panel (e.g., "Figure 6e, tail region")
- [ ] Medians / IQRs / CIs described once, not re-stated every paragraph

---

## Discussion

**Structure (flexible, journal-dependent, but typical order)**:

1. Restate the main findings in 1–2 sentences (no new detail)
2. Compare with prior work (where you confirm, where you extend, where you
   contradict — cite specifically)
3. Mechanism synthesis: what the model reveals about the system
4. Implications (policy / practice / theory)
5. Limitations + future directions

**Limitations section**:
- Thematic opening: *"Here we discuss N areas of limitation: [area 1] and
  [area 2]."* Do not open with validation metrics.
- Each limitation: identify constraint → explain practical impact → suggest
  solution / future direction.
- Cite literature within limitation paragraphs when relevant.
- Do NOT undermine core results. Reframe as: *"This limitation suggests future
  research should..."*
- Hedging language: *"are suggested for future research", "could improve",
  "We suggest..."*.

**Checklist**:
- [ ] Does not restate Results paragraph-by-paragraph
- [ ] Every comparison to prior work cites specifically
- [ ] Mechanism synthesis connects findings across RQs
- [ ] Implications are modest and grounded
- [ ] Limitations thematic opening, not metric-driven
- [ ] Future directions hedged

---

## Conclusion

**Structure (usually 2–3 short paragraphs)**:

1. What the study did and what it found (tied to RQs)
2. Key mechanism insight or policy implication
3. One-sentence statement of the broader significance

**Checklist**:
- [ ] Mirrors the RQ order from the Introduction
- [ ] Numbers match Results (re-run if necessary)
- [ ] Terminology consistent with Introduction and Methods
- [ ] No new results introduced
- [ ] Final sentence lands the broader "why this matters"
- [ ] No banned words (run `banned_words.md`)

---

## Reviewer Response (Rebuttal)

Most journals now require a **point-by-point response table** (reviewer
comment verbatim → response → change location). Build it as the primary
deliverable, not an afterthought.

**Structure for each comment**:

1. **Comment** (verbatim, numbered per reviewer, e.g., R1.3)
2. **Response** (student tone — "Fixed.", "Added explanation.",
   "Yes, confirmed via additional test...")
3. **Changes in the manuscript** (quote new text with page/line numbers,
   or cite the new figure/table). For LaTeX, reference the commit or diff.

**Rules**:
- Every comment → identify the exact anchor text in the manuscript before
  responding. Do not guess which sentence the comment refers to.
- Apply the editor-accepted changes first; then revise only what the comments
  require. Do not rewrite clean paragraphs.
- Iterative rewrites (abstract, intro) typically need 3–6 passes; set this
  expectation with the user upfront.

### Productive disagreement

Reviewers are not always right. When a comment rests on a misreading or a
methodological disagreement, disagree carefully:

- **Cite evidence, not politeness alone**: back up any counter-argument with
  literature (*"We follow the convention established by [Author, year], who
  showed that..."*) or with new data (*"To address this concern directly, we
  ran the suggested test; the result (Figure R1) supports the original
  interpretation."*).
- **Reframe before rejecting**: acknowledge the reviewer's underlying
  concern ("*The reviewer is right that X could be confounded...*"), then
  explain why your approach addresses it.
- **Never "we respectfully disagree" alone**: this reads as dismissal.
  Either provide the argument or accept the comment.
- **Run the reviewer's own suggested test** when feasible, even if you expect
  it to support your original finding. Showing the robustness check in the
  response is more persuasive than words.
- **Decline only with a reason**: if a requested experiment is out of scope,
  state why concretely (cost, timeframe, ethics, data access), propose a
  smaller surrogate where possible, and acknowledge the limit in Discussion.

### Handling contradictory reviewer requests

When R1 asks for X and R2 asks for not-X:
1. Name the tension explicitly in both responses.
2. Choose one path with justification, and inform the other reviewer through
   their response.
3. If neither can be dropped, request an editor ruling in the cover letter.

### Common rebuttal anti-patterns

- Restating the original text instead of revising it.
- Agreeing verbally but making no manuscript change.
- Moving a challenged claim to the SM without changing its substance.
- Adding a generic "we have clarified the text" without pointing to specific
  lines.

**Checklist**:
- [ ] Every reviewer comment has a numbered response
- [ ] Every response cites the specific change in the manuscript (page/line
      or figure/table reference)
- [ ] Changes use track-changes (Word) or diff-visible form (LaTeX)
- [ ] Student tone, not formal reviewer language
- [ ] Disagreements are supported by evidence or citation, not just politeness
- [ ] At least one reviewer suggestion was tested and reported, even when
      the original finding held
- [ ] Contradictory requests are explicitly reconciled
- [ ] No new banned words introduced in the revision
