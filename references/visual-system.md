# Visual System

## Contents

1. Design thesis
2. Presets and slide themes
3. Typography and grid
4. Image treatment
5. Motion and responsive behavior

## Design thesis

Use **evidence-led art direction**: preserve one evidence contract while changing how hierarchy, proportion, image role, and page rhythm express the project's strongest character. The four systems must remain recognizably different even when rendered in grayscale.

Avoid generic dashboard cards, glass effects, decorative gradients, fake blueprint clutter, excessive rounded corners, and repeated floating mockups.

Composition is the primary layer; typography and color are supporting layers. Workshop should feel assembled and iterative, Instrument aligned and testable, Material tactile and unhurried, and Gallery selective and exhibition-like. Do not reduce these differences to palette swaps.

## Presets and slide themes

Select one full-portfolio system from [style-presets.md](style-presets.md). Systems control layout-specific composition, typography, density, grid visibility, image framing, neutrals, and accent behavior.

| System ID | Ink | Paper | Accent | Best use |
|---|---|---|---|---|
| `workshop-orange` | `#171717` | `#F1EFE8` | `#F05A28` | General ID, tools, mobility |
| `instrument-blue` | `#10233E` | `#F4F6F8` | `#1C67D2` | Electronics, medical, technical |
| `material-green` | `#17251D` | `#F2EFE5` | `#4F8A5B` | Sustainability, home, wellbeing |
| `gallery-red` | `#201D1B` | `#FFFFFF` | `#B83A30` | Furniture, culture, premium goods |

Use `theme-light`, `theme-dark`, `theme-paper`, and `theme-accent` as page-level tonal roles inside the chosen preset. They are not independent style choices. Users may provide brand colors, but constrain them to one primary accent plus neutrals. Check contrast before use.

## Typography and grid

- Keep body copy in the neutral sans-serif stack. Use the preset display stack for titles: sans-serif in Workshop and Instrument, serif in Material and Gallery. Use monospace for measurements, evidence levels, and metadata.
- Follow the selected system's grid density, page proportions, and outer margin. Workshop uses deliberate offsets, Instrument aligns to a dense technical grid, Material uses asymmetric image-led balance, and Gallery removes the visible grid in favor of dominant visuals and editorial whitespace.
- Keep body copy between 17-24 px in a 16:9 deck.
- Limit a normal page to one title, one main visual structure, and one takeaway.
- Use hairlines and registration marks sparingly to organize evidence.
- Preserve a bottom safe area for navigation and captions.

## Semantic color tokens

Treat the preset colors as roles, not interchangeable hex values:

- `--accent`: larger fills, progress, and graphic anchors;
- `--accent-text`: small accent text on light or paper pages;
- `--accent-on-dark`: small accent text on dark pages;
- `--on-accent`: text on a full accent page.

Do not use `--accent` directly for small text. The template supplies contrast-safe text variants because the same color that works as a large fill may fail as a caption or label.

## Image treatment

- Give original artifacts priority over styled decoration.
- Show sketch texture and prototype imperfections when they are informative.
- Never crop away scale cues, hands, fixtures, labels, or test conditions.
- Align comparison images to the same scale whenever possible.
- Place captions immediately beneath images.
- Use one accent marker to point at a design decision; avoid annotation overload.
- Do not place final renders inside fake laptops or phones unless the product is software-dependent and the device context matters.

## Motion and responsive behavior

- Use motion only to reveal sequence or hierarchy.
- Keep transitions between 180-500 ms and respect reduced-motion preferences.
- Ensure every page is fully understandable when motion is disabled.
- Keep scrolling immediate by default; do not add smooth scrolling or backdrop filters to the navigation shell.
- Use `data-src` for local raster images so only the current page and its neighbors decode on desktop.
- Preserve `?page=N` for direct page entry and `?render=all` for screenshots and PDF export.
- Mount all pages before printing, then restore the adjacent-page window after printing.
- On narrow screens, stack grids and allow vertical scrolling within a slide rather than shrinking text below legibility.
- For PDF export, hide navigation and preserve a 16:9 page box.
