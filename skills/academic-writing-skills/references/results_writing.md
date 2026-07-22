# Results Writing

Use this reference when drafting or revising Results. Its purpose is to turn
figures and tables into a selective scientific account rather than a narrated
inventory of every displayed value.

## Contents

1. Establish the evidence baseline
2. Build the subsection around patterns
3. Keep Methods, Results, and Discussion distinct
4. Control evidence attribution
5. Handle group comparisons precisely
6. Use natural transitions
7. Apply the final Results gate

## 1. Establish The Evidence Baseline

Before drafting, identify the current authoritative version of every source
used in the subsection:

| Source | Version or date | What it supports | Conflicts to resolve |
|---|---|---|---|
| Figure or table | ... | pattern, mean, coefficient | ... |
| Analysis output | ... | test statistic, uncertainty | ... |
| Methods definition | ... | variable type, reference group | ... |

Do not combine numbers from different figure generations or analysis runs.
When a figure, table, caption, and prose disagree, pause drafting and resolve
the conflict against the analysis output or another designated source of
truth. Do not silently choose the value that best fits the sentence.

## 2. Build The Subsection Around Patterns

Use this default arc:

```text
main pattern -> selective evidence -> result-level synthesis
```

Add a mechanism only when it is directly supported by a measured quantity, a
specified method rule, or a cited source. Descriptive means, subgroup models,
and statistical associations do not by themselves establish why the pattern
occurred.

Select numbers that establish one of the following:

- magnitude or direction of the main pattern,
- the clearest comparison,
- an important exception,
- uncertainty or statistical support.

Do not report every node, coefficient, or panel value merely because it is
available. Refer readers to the figure or table for secondary values.

## 3. Keep Methods, Results, And Discussion Distinct

- Methods defines variables, models, tests, and planned comparisons.
- Results reports the patterns produced by those analyses.
- Discussion explains broader mechanisms, compares prior work, and develops
  implications or limitations.

Do not repeat the model architecture in Results when Methods has already
defined it. Include only the minimum reminder needed to interpret an unusual
display, such as noting that one variable is binary while the others are
latent scores.

## 4. Control Evidence Attribution

Each precise number and assertive result must point to the source that actually
supports it. A number known from the dataset is not automatically supported by
the figure cited in the paragraph.

If the number is not displayed in the cited figure or table:

1. cite the correct table, supplement, or analysis output made available to
   readers;
2. add the number to an appropriate display; or
3. remove the number and write the supported qualitative pattern.

Never imply that a figure shows a value that it does not contain.

## 5. Handle Group Comparisons Precisely

Distinguish three claims that are often conflated:

| Evidence available | Claim allowed |
|---|---|
| Different group means or coefficients | descriptive difference |
| A path is significant in one group but not another | separate within-group results |
| A valid between-group test rejects equality | statistically supported group difference |

Do not infer a significant between-group difference from significance in one
group and nonsignificance in another. Name the formal comparison test when
claiming that groups differ statistically.

When one group dominates the pooled sample, the full-sample pattern may
resemble that group. State sample composition as interpretive context, not as
proof that the dominant group caused the pooled result. Preserve the
group-specific pattern when it answers the research question.

## 6. Use Natural Transitions

Make transitions name the analytical move rather than announce generic
progress. For example, use "When examined separately by group" when shifting
from pooled to subgroup results. Avoid repeatedly opening paragraphs with
formulaic phrases such as "Moving from" or "Building on these results" when
the sentence can state the actual comparison.

## 7. Final Results Gate

- [ ] The paragraph leads with the main pattern, not an inventory of values.
- [ ] Only decision-relevant numbers are reported in prose.
- [ ] Every number comes from the current authoritative source.
- [ ] The cited source visibly supports the claim or is correctly identified.
- [ ] Methods content is repeated only when needed for interpretation.
- [ ] Descriptive, within-group, and between-group claims are distinguished.
- [ ] Any mechanism is directly supported and stays brief.
- [ ] The ending synthesizes the result without expanding into Discussion.
