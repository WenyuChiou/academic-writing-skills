# Pre-Submission Checklist

Run this checklist before submission or resubmission. Journal-specific rules in
`.paper/journal_format.md` override these defaults.

## 1. Manuscript

- [ ] File format matches journal requirements.
- [ ] Title page includes authors, affiliations, corresponding author, and ORCID.
- [ ] Abstract is within the word limit.
- [ ] Main text is within word or page limit.
- [ ] Required sections are present and in the required order.
- [ ] Section numbering matches journal style.
- [ ] Drafting scaffolds, paragraph-role labels, outline prompts, and internal
      author notes have been removed unless the journal explicitly requires
      them.
- [ ] Line numbers and spacing match journal instructions.
- [ ] Figures and tables are cited in order.

## 2. Figures And Tables

- [ ] Every figure is cited in the main text.
- [ ] Figure files use accepted format and resolution.
- [ ] Figure captions start with "Figure X."
- [ ] Panel labels match text citations.
- [ ] Figure numbers in text match file names.
- [ ] Table captions, numbering, and units are correct.
- [ ] Numbers in prose match figures and tables.
- [ ] Accessibility check passed.
- [ ] Every continued data table repeats its actual column headers; survey
      questions or data rows are not incorrectly repeated as headers.
- [ ] The first and last row on every rendered table page retain their labels,
      units, and comparison meaning.

## 3. Supplementary Material

- [ ] Each supplementary item has a specific label.
- [ ] Supplementary labels follow order of first mention.
- [ ] Supplementary captions are complete.
- [ ] No main-text claim depends only on uncited supplementary material.
- [ ] Every supplementary item is cited from the main text, and every
      supplementary citation resolves to an existing item.
- [ ] Main text and supplementary material use the same terminology,
      definitions, sample counts, group counts, model names, units, and
      analytical settings.
- [ ] Technical model or treatment identifiers are separated from display
      names, and any shortened table or figure names are defined once.
- [ ] Runtime, token, cost, call-count, and hardware rows trace to source
      records. Identical values across different systems have been verified
      rather than copied.

## 4. References

- [ ] Every in-text citation has a reference-list entry.
- [ ] Every reference-list entry is cited.
- [ ] Citation style matches the journal.
- [ ] DOI, volume, pages, year, and author names are accurate.
- [ ] Preprints and datasets follow journal rules.

## 5. Cover Letter

- [ ] Editor or journal addressed correctly.
- [ ] Central contribution stated in one or two sentences.
- [ ] Journal fit explained.
- [ ] Originality and no concurrent review confirmed.
- [ ] Related preprint or prior submission disclosed.
- [ ] Suggested or excluded reviewers included only if allowed.

## 6. Declarations

- [ ] Author contribution statement completed.
- [ ] Funding acknowledgment includes grant numbers.
- [ ] Competing interests statement completed.
- [ ] Data availability statement includes repository, DOI, or access condition.
- [ ] Code availability statement includes URL and commit or release.
- [ ] Ethics approval, consent, IRB, IACUC, or trial registration included when relevant.
- [ ] AI-usage disclosure follows journal policy.
- [ ] Preprint DOI and version disclosed when relevant.

## 7. Text Compliance

- [ ] Banned-word audit passed.
- [ ] Overclaim language corrected.
- [ ] Figure references are panel-specific where needed.
- [ ] Claim-evidence ledger covers Abstract, Discussion, and Conclusion.
- [ ] Paper-specific terminology applied consistently.
- [ ] Numbers were rechecked against the latest outputs.

## 8. Cross-Artifact Integrity

- [ ] Designate one authoritative source for each invariant, including sample
      totals, subgroup totals, model or treatment names, run counts, units,
      analysis versions, and figure states.
- [ ] Arithmetic and set relationships among invariants are valid, such as a
      total equaling the sum of mutually exclusive subgroups.
- [ ] Manuscript, title page, abstract file, cover letter, highlights,
      supplementary material, figure files, captions, and portal metadata all
      use those same invariants.
- [ ] Embedded figures match separately supplied figure files.
- [ ] After any component changes, rebuild the submission package from the
      authoritative files and verify the contents rather than patching only one
      copy.
- [ ] A forward review has been completed in the order document → heading
      hierarchy → section → paragraph → sentence → terminology → displays →
      evidence provenance.
- [ ] A reverse review has rechecked changed sentences in context, standalone
      summary files, rendered pages, and the rebuilt package. Completion
      evidence is recorded for each level.
- [ ] Technical paper-ready, author-action-required, and submission-ready
      states are reported separately.

## 9. Submission Portal

- [ ] Account created.
- [ ] Manuscript uploaded with correct file type tag.
- [ ] Figures uploaded separately if required.
- [ ] Supplementary files uploaded and tagged.
- [ ] Cover letter pasted or uploaded.
- [ ] Keywords and classifications selected.
- [ ] Reviewer information verified.

## 10. After Submission

- [ ] Submitted PDF and source files archived.
- [ ] Submission ID recorded in `.paper/submissions_log.md`.
- [ ] Submitted version tagged in version control.
- [ ] Any deviations from journal template recorded.
