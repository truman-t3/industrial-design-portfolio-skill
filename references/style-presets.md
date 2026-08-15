# Style Systems

## Contents

1. Selection rule
2. System catalog
3. Low-friction conversation pattern
4. Applying a system
5. Customization boundaries

## Selection rule

Choose one visual system for the entire portfolio after the evidence and audience are understood. A system changes composition, hierarchy, typography, density, grid behavior, image role, neutral colors, and accent behavior. It preserves the registered `ID01-ID18` identities and the evidence standard. Seven high-signal layouts—ID01, ID03, ID08, ID10, ID13, ID14, and ID16—have system-specific composition recipes; the other layouts use the shared fragment library plus system styling.

Frame the decision as **what the reviewer should believe first**, not as a favorite color. Use the human-facing names Workshop, Instrument, Material, and Gallery in conversation; keep the code IDs secondary. If the user has no preference, infer the best fit from the flagship evidence and target audience, state the choice in one sentence, and continue. Do not mix systems between projects in the same portfolio.

## System catalog

| Name and ID | Reviewer should believe first | Composition signature | Image logic | Avoid when |
|---|---|---|---|---|
| **Workshop / 工坊** `workshop-orange` | The designer explored, made, and iterated broadly | Offset process panels, staggered evidence, bold markers, visible making rhythm | Show process artifacts at useful scale; allow honest texture and work-in-progress edges | The work needs quiet luxury or a highly clinical tone |
| **Instrument / 仪器** `instrument-blue` | The system is precise, reasoned, and testable | Rigid technical grid, aligned comparison cells, compact metadata, measured hierarchy | Contain CAD, architecture, measurement, and test evidence; align comparisons rigorously | The project depends mainly on craft, emotion, or organic materiality |
| **Material / 材质** `material-green` | The designer understands touch, CMF, context, and human experience | Asymmetric image-led pages, soft frames, slower serif hierarchy, generous breathing room | Give material studies, domestic context, hands, and surface details room to breathe | Dense technical diagrams are the dominant proof |
| **Gallery / 展陈** `gallery-red` | Form, craft, final resolution, and cultural intent are exceptional | One dominant visual, extreme scale contrast, editorial whitespace, secondary evidence as satellites | Use fewer and larger images; privilege final photography and craft details | The audience needs rapid comparison of many engineering details |

Default to `workshop-orange` for mixed portfolios. Prefer `instrument-blue` when architecture, CAD, testing, or hardware/software evidence dominates. Prefer `material-green` when material, domestic context, lifecycle, or sensory experience dominates. Prefer `gallery-red` when form, cultural rationale, craft, or final photography dominates.

## Low-friction conversation pattern

Do not ask a designer to inspect CSS or choose among raw IDs. Use this pattern:

1. Summarize the strongest evidence signal in one phrase.
2. Recommend one human-facing system and explain why in one sentence.
3. Offer the other three only if the user asks to compare or the choice materially affects the outcome.
4. Record the selected code ID and rationale in the manifest.

Example: “Your strongest proof is the enclosure-to-PCB relationship and measured prototype iteration, so I recommend **Instrument** (`instrument-blue`) for a precise technical read.”

## Applying a system

Replace `[STYLE_PRESET]` on the root `<html>` element in `assets/portfolio-template.html` with one system ID:

```html
<html lang="en" data-style="instrument-blue">
```

Record the same ID in `portfolio.style_preset` in `portfolio_manifest.json`. Keep slide-level classes such as `theme-light`, `theme-dark`, `theme-paper`, and `theme-accent`; they are tonal roles inside the selected system, not separate portfolio styles.

## Customization boundaries

- Preserve the system's layout-specific composition, spacing, type hierarchy, and image-treatment logic unless the supplied brand system requires a change.
- A user-provided brand color may replace the accent after checking the semantic text roles in `references/visual-system.md`; do not add multiple decorative accent colors.
- Use system font fallbacks already present in the template. Do not add network-hosted fonts to a portable or offline deck.
- Do not choose a system based only on a favorite color. Choose the system that makes the strongest evidence easiest to review.
- Use the 28 registered system recipes under `assets/compositions/` for ID01, ID03, ID08, ID10, ID13, ID14, and ID16. Do not create further per-system duplicates unless a shared fragment cannot express a materially different evidence hierarchy.
- Preserve the shared placeholder meanings across recipes. A visual-system change may alter composition, but it must not alter evidence level, source, authorship, or claim status.
- Treat colors as a lower layer than composition. A custom accent must not silently turn Workshop, Instrument, Material, and Gallery into palette-only variants.
