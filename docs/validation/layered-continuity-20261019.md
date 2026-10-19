# Layered explanation and continuity: bounded behavior check

## Design and limits

The accepted v1.3.18 skill and the v1.3.19 candidate each produced one response
to the same 18 hypothetical tasks: 16 public cases in
[`evals/layered_continuity_cases.json`](../../evals/layered_continuity_cases.json)
and two transfer cases not present in the teaching guide. The four criteria per
case were fixed before execution and hidden from both writers. Separate native
agents used the inherited session settings, not an asserted cheaper or superior
model. No scientific experiment or manuscript was changed.

The parent read the actual revisions against the supplied facts and criteria;
this was not blind human grading. All 72 prespecified criteria were met in each
version in this one paired run. The sample does **not demonstrate improvement**
over v1.3.18. It supports retaining the narrow clarification and regression
controls without claiming a quantified quality or token-saving benefit.

An additional cold-read check found an unexplained `IQR` abbreviation in the
candidate's standalone LC01 paragraph. A disclosed, targeted correction spells
out and explains the statistic; the initial output remains preserved separately.
That feedback-assisted correction is not a new independent first-pass success.
The no-change controls LC11–LC13 were retained verbatim; LC14 changed only
`provide` to `provides`. These results concern the supplied reading contexts,
not a universal ban or requirement for a particular abbreviation.

## What was assessed

| Cases | Reader function and protected boundary |
| --- | --- |
| LC01, LC09 | Give score/measurement levels timely meaning, then explain spread; retain all comparison values and units. |
| LC02, LC10 | Separate component statistics from group/model claims, practical importance, and equivalence; leave missing tests missing. |
| LC03–LC06 | Bridge literature to gap, background to design, finding to Discussion implication, and limitation to affected inference. |
| LC07, LC08, LC15, LC16 | Name comparators and variable pairs, preserve construct meanings, avoid shared-scale importance rankings, and reduce acronym load without inventing behavior or causation. |
| LC11–LC14 | Preserve clear text, a coherent multi-value negative finding, an established display's reading context, and local grammar scope. |
| Transfer cases | Organize an unfamiliar environmental display and a qualitative theme/contrasting-account sequence without copying the teaching example's field or sentence pattern. |

## Actual transfer example: a seasonal display

Hypothetical facts: dissolved oxygen across monitoring sites, wet/dry medians
6.0/4.0 mg/L, interquartile ranges 1.0/2.0 mg/L, supplied threshold 5.0 mg/L.
No seasonal cause or site counts below threshold were available.

**Before:**

> Figure 4 presents the results. In the wet season the median is 6.0 and IQR is
> 1.0. In the dry season the median is 4.0 and IQR is 2.0. This answers the research
> question. The results demonstrate the importance of seasonal variation.

**Candidate output:**

> Figure 4 compares dissolved oxygen across monitoring sites in wet and dry
> seasons; violin width represents site density at each oxygen concentration,
> measured in mg/L. The wet-season median was above the management threshold of
> 5.0 mg/L (6.0 mg/L), whereas the dry-season median was below it (4.0 mg/L).
> Dissolved oxygen was also more consistent across sites in the wet season: the
> interquartile range was 1.0 mg/L, compared with 2.0 mg/L in the dry season.

The opening supplies the new display's population, quantity, and comparison.
The values immediately acquire meaning against the supplied threshold. The next
unit adds site-level consistency rather than another isolated number list. The
ending gives the substantive seasonal answer without a question label, causal
claim, or invented count. The actual plot and its layout were not inspected;
the orientation was checked only against the supplied display description.

## Actual inference-preserving example: changing analytical level

**Before:**

> Effectiveness is significant in A (.30, p=.02) and not in B (.20, p=.11).
> Therefore, the groups have different decision models.

**Candidate output:**

> Effectiveness was positively associated with willingness in group A
> (coefficient .30, p=.02). The estimate in group B was also positive (.20) but
> was not statistically significant (p=.11). These within-group results do not
> establish a between-group difference in the association or in the overall
> decision model.

The revision names the measured pair, retains both results, and exposes the
missing direct comparison. It neither manufactures a whole-model test nor
treats the nonsignificant result as equality. Missing evidence appropriately
prevents a completed group-level answer; polished continuity cannot replace it.

## Acceptance meaning

The exercise assesses the organization and reader guidance motivated by
author-supplied teaching: orientation when needed, timely evidence-to-meaning
links, layered analytical progression, functional transitions, and substantive
question closure. It does not copy private wording, metaphors, historical
numbers, or causal language, and is not an advisor's approval of these outputs.
The qualitative transfer case also retained the count of three contrasting
accounts, their schedule-specific mismatch, and the one-program boundary,
without turning coded accounts into prevalence or a causal success claim.

Repository tests check fixture/routing integrity, existing tools, and packaging;
they do not grade these passages. AI reader judgments do not establish that
human readers in all fields will understand the prose, prove scientific
correctness, or discover every hidden issue. Replication across models or human
readers was outside this bounded check.
