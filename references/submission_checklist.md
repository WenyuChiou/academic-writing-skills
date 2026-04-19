# Pre-Submission Checklist

Run this full checklist **before** the user submits the manuscript. Cross-reference
with `<paper-repo>/.paper/journal_format.md` for journal-specific rules that
override or extend these universals.

---

## 1. Manuscript File

- [ ] Target journal's file format honored (Word / LaTeX / PDF)
- [ ] Title page with full author list, affiliations, corresponding author, ORCID
- [ ] Abstract within journal word limit
- [ ] Highlights / graphical abstract prepared if required
- [ ] Main text within journal word / page limit
- [ ] Section numbering matches journal convention (Arabic, Roman, or none)
- [ ] Figure count within limit
- [ ] Table count within limit
- [ ] Line numbers enabled (if required for review)
- [ ] Double spacing enabled (if required for review)

## 2. Figures and Tables

- [ ] Every figure referenced in the main text at least once
- [ ] Every figure has a caption that starts with "Figure X."
- [ ] Figure numbers in text match figure files
- [ ] DPI / resolution meets journal specification
- [ ] Color mode (RGB / CMYK) matches journal specification
- [ ] Font embedding confirmed if submitting PDF figures
- [ ] Figure cross-consistency audit passed (see `figure_conventions.md` §10)
- [ ] Same for tables (caption above, correct numbering, numbers match prose)

## 3. Supplementary Material

- [ ] Every SM item referenced in the main text has a specific label
      (Text S1, Figure S2, Table S3)
- [ ] SM numbering follows order of first appearance in main text
- [ ] SM caption/title page included
- [ ] No SM-only results claimed as main-text findings

## 4. References

- [ ] Every in-text citation has a matching entry in the reference list
- [ ] Every reference entry is cited at least once (no orphans)
- [ ] Citation style matches journal (author-year vs numbered)
- [ ] Author name spellings consistent between in-text and reference list
- [ ] Year, volume, pages, DOI accurate for every entry
- [ ] Preprints / data citations formatted per journal rules

## 5. Cover Letter

- [ ] Addresses editor by title (e.g., "Dear Dr. [Editor]")
- [ ] States the paper's central contribution in 1–2 sentences
- [ ] Explains why this journal is the right venue
- [ ] Confirms the work is original, unpublished, not under review elsewhere
- [ ] Discloses any prior interaction with the journal (resubmission, prior reviews)
- [ ] Suggests reviewers if the journal allows (with justification)
- [ ] Lists excluded reviewers if the journal allows (with reason)

## 6. Declarations and Statements

### Identity and authorship
- [ ] **ORCID for every author**, not just the corresponding author
- [ ] **Author contribution statement** using CRediT taxonomy (Conceptualization,
      Data Curation, Formal Analysis, Funding Acquisition, Investigation,
      Methodology, Project Administration, Resources, Software, Supervision,
      Validation, Visualization, Writing – Original Draft, Writing – Review &
      Editing) — most major journals now require this
- [ ] Corresponding author designated with email and affiliation
- [ ] Equal-contribution footnote if multiple first authors

### Data, code, and materials
- [ ] **Data availability statement** aligned with journal policy (include
      repository name, DOI, accession number; state any access restrictions)
- [ ] **Code availability statement** with repo URL and commit hash or release
      tag (Zenodo-archived if possible for persistence)
- [ ] **Materials availability** for lab studies (cell lines, plasmids, antibodies,
      with RRIDs or catalog numbers)

### Funding and conflicts
- [ ] **Funding acknowledgment** with grant numbers for every author's support
- [ ] **Competing interests (COI) statement** per ICMJE form — individual form
      per author for medical journals
- [ ] Prior publication / dual-submission declaration

### Preprint and prior posting
- [ ] **Preprint DOI** disclosed if posted (bioRxiv, medRxiv, arXiv, SSRN,
      OSF Preprints, Research Square) — including the exact version number
- [ ] Differences from the preprint version described, if substantive
- [ ] Conference-presentation history if applicable

### Ethics
- [ ] **IRB / ethics committee approval number** for human-subject research
- [ ] **IACUC / animal ethics protocol number** for animal research
- [ ] Informed consent statement (written / verbal / waived, and justification)
- [ ] **Clinical trial registration ID** for any prospective trial
      (ClinicalTrials.gov, ISRCTN, etc.) registered before enrollment
- [ ] Biosafety / biosecurity disclosures for BSL-3/4 work or dual-use research

### AI and emerging disclosures
- [ ] AI-usage disclosure following the journal's current policy (writing aid,
      figure generation, data analysis — often distinguished)
- [ ] Open-science badges claimed if the journal offers them (Open Data,
      Open Materials, Pre-registered)

## 7. Text Compliance

- [ ] Banned-word audit passed on Abstract, Introduction, Discussion, Conclusion
- [ ] No "As mentioned above" or meta-references
- [ ] No em-dashes
- [ ] Figure citations at panel level (where panels exist)
- [ ] All numbers re-verified against current code output
- [ ] All figure labels consistent across figures
- [ ] Paper-specific terminology (`style_overrides.md`) applied consistently

## 8. Final Read-Through Gates

- [ ] Read the Abstract cold: does it make the scientific case in 6 parts?
- [ ] Read the Introduction transitions: does each gap pivot logically?
- [ ] Read one Results paragraph at random: finding → mechanism → RQ link?
- [ ] Check the Conclusion: does the final sentence land the broader "why"?
- [ ] Verify Abstract numbers == Results numbers (they drift during revision)
- [ ] Verify Methods-described equations match Results interpretation

## 9. System / Submission-Portal Prep

- [ ] Account created on submission portal (Editorial Manager, ScholarOne, etc.)
- [ ] Manuscript file uploaded with correct file type tag
- [ ] Figures uploaded as separate files (if required) with correct naming
- [ ] Supplementary file uploaded and tagged
- [ ] Cover letter pasted into portal text box or uploaded
- [ ] Reviewer suggestions entered with email addresses verified
- [ ] Keywords entered per journal guidance
- [ ] Classification codes / research area selected

## 10. After Submission (housekeeping)

- [ ] Archive the exact submitted PDF + raw files in the paper repo under a
      tag like `submission-YYYY-MM-DD/`
- [ ] Record submission ID in `<paper-repo>/.paper/submissions_log.md`
- [ ] Note any deviation from the template used to build the manuscript
