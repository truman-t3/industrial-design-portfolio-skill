# Image and Generation Policy

## Contents

1. Source priority
2. Allowed transformations
3. Generated imagery
4. Technical image rules
5. Naming and captions

## Source priority

Use visuals in this order:

1. User research and field evidence
2. Sketches and process artifacts
3. CAD and engineering screenshots
4. Physical prototypes and test records
5. Final photography or verified production imagery
6. AI-assisted concept visualization
7. Neutral placeholders

## Allowed transformations

For evidence images, default to crop, exposure, color balance, redaction, background extension, and layout framing. Do not alter the product, participant behavior, test setup, measurement, or result unless the change is disclosed and the original remains available.

Never regenerate a screenshot, sketch, prototype photo, or test image when fidelity matters.

## Generated imagery

Generate only when it clarifies:

- an early form direction;
- a controlled usage atmosphere;
- a non-evidentiary cover visual;
- a clearly hypothetical future scenario.

Do not generate:

- fake user research;
- fake prototype or workshop photos;
- patent, safety, medical, or compliance evidence;
- technical drawings presented as dimensionally accurate;
- fake production or launch imagery;
- precise material samples presented as real CMF approval.

Save generated assets under `images/generated/` and pair each with:

```html
<figcaption>AI-assisted concept visualization · Not engineering evidence</figcaption>
```

## Technical image rules

- CAD, orthographic, section, and exploded views must come from consistent geometry to be called technical drawings.
- If a generated visual explains architecture, title it `conceptual architecture illustration`.
- Keep dimension text, tolerances, units, and part numbers outside generated raster imagery.
- Use HTML overlays or verified vector/CAD exports for annotations.
- Use `contain` for drawings and diagrams; never crop critical geometry.

## Naming and captions

Use `{project}-{page}-{type}-{sequence}.{ext}`:

```text
kettle-03-research-01.jpg
kettle-08-cmf-02.png
kettle-12-prototype-03.jpg
kettle-14-final-01.webp
```

A strong caption answers: what is shown, why it matters, source/authorship, and evidence level.

