# Figure Conventions

Rules for figures, captions, panel references, and figure-text coupling.

## 1. Figure-Text Coupling

Any precise number in prose must be visible or traceable:

- visible annotation on the figure,
- readable axis value,
- table entry,
- code output,
- cited source.

If prose says "insurance covers 36%", the figure, table, or source must let the
reader verify 36%. If not, add the evidence or use qualitative wording.

## 2. Cross-Figure Consistency

Use the same label, color, and annotation style for the same concept across the
paper.

Examples:

- Do not switch between "flood damage", "gross loss", and "GUL" unless the
  paper defines a real distinction.
- If adaptation is red in Figure 5, keep it red in Figure 6.
- If a difference label uses "Delta = X" in one figure, use the same format
  elsewhere.

## 3. Define Once

Define a term on first use, then use the same term. Do not redefine concepts in
Results or Discussion that were already defined in Methods.

## 4. Annotation Style

Standardize:

| Annotation | Rule |
|---|---|
| Endpoint labels | same font size, color, and box style |
| Gap markers | same arrow style and same label format |
| Shaded event windows | same fill color and transparency |
| Panel labels | same position and font weight |
| Statistical markers | same threshold notation and caption explanation |

## 5. Caption Format

Recommended pattern:

```text
Figure X. One-sentence description of the figure as a whole. (a) Panel
description, (b) panel description, and (c) panel description.
```

Rules:

- Do not start a caption sentence with a parenthetical panel label.
- Describe each panel individually.
- Define abbreviations on first use unless already defined in the manuscript.
- Make captions self-contained enough for a reader scanning figures.

## 6. Panel-Level Citations

Cite specific panels:

- "Figure 5b, blue line"
- "Figure 6e, tail region"

Avoid bare figure citations when the claim depends on one panel.

## 7. Field Conventions

Prefer standard plots when the field has one:

| Field | Typical plot |
|---|---|
| Catastrophe or insurance | exceedance probability curve |
| Hydrology | hydrograph with calendar x-axis |
| Regression diagnostics | residual, Q-Q, and scale-location panels |
| Sensitivity analysis | tornado plot or Sobol index bar chart |
| Clinical or survival analysis | Kaplan-Meier curve when appropriate |
| Meta-analysis | forest plot |
| Probabilistic forecasts | reliability diagram and sharpness histogram |

Check assumptions behind the convention. For example, rank-based return periods
require independent events. If the same hazard sequence is reused with stochastic
agent decisions, use exceedance probability instead of return period language.

## 8. Accessibility

- Use colorblind-safe palettes.
- Do not rely on color alone.
- Use line styles, markers, direct labels, or annotations.
- Keep background shading distinct from data colors.

## 9. File Quality

- Prefer vector formats for line art: PDF, SVG, EPS.
- Use 600 DPI for raster line art when raster is required.
- Use 300 DPI or the journal's requirement for photos and halftones.
- Check exact journal requirements in `.paper/journal_format.md`.

## 10. Figure Audit

Before returning figure-related prose or captions, check:

- [ ] Every panel has a label.
- [ ] Axes include units.
- [ ] Plotted quantities are defined.
- [ ] Legend labels match prose terminology.
- [ ] Precise prose numbers are visible or traceable.
- [ ] Caption describes each panel.
- [ ] Chart type matches field convention.
- [ ] Colors and annotations are consistent with other figures.
