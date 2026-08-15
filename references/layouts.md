# Registered Portfolio Layouts

## Contents

1. Layout selection rules
2. Registered layouts
3. System-specific composition recipes
4. Image slots
5. Rhythm rules

## Layout selection rules

- Add `data-layout="IDxx"` to every slide.
- Choose a layout because it matches the evidence shape.
- Keep titles on the top-left content axis except for ID01, ID14, and ID16.
- Use captions for every research, prototype, test, competitor, and generated image.
- Do not place technical labels inside decorative SVG; use readable HTML.

## Registered layouts

| ID | Name | Best use | Required content |
|---|---|---|---|
| ID01 | Portfolio Cover | Identity and thesis | Name, discipline, year |
| ID02 | Project Brief | Problem, role, constraints | User, role, timeline, scope |
| ID03 | Evidence Wall | Research/prototype evidence | 2-6 sourced artifacts |
| ID04 | Insight Statement | One decisive insight | Claim + supporting evidence |
| ID05 | Landscape | Competitor or precedent comparison | Named axes and sources |
| ID06 | Concept Divergence | Sketch families or alternatives | 3+ meaningfully different routes |
| ID07 | Decision Matrix | Selection and trade-offs | Criteria, ratings, decision note |
| ID08 | Form and CMF | Form language, material, finish | Hero view + annotations/swatches |
| ID09 | Ergonomic Relationship | Grip, reach, posture, scale | Human relationship + method |
| ID10 | Product Architecture | Exploded, section, system | Components + interfaces + caveat |
| ID11 | Manufacturing Sheet | Process, assembly, BOM, risks | Assumptions + review status |
| ID12 | Prototype and Test | Test method and observations | Prototype, variable, result |
| ID13 | Iteration Delta | Before/after design change | Change + cause + consequence |
| ID14 | Final Resolution | Final product and experience | Strong image + concise value |
| ID15 | Reflection | Outcome, limits, learning | What worked, next validation |
| ID16 | Project Divider | Multi-project transition | Number, title, one-line thesis |
| ID17 | Index | Selected work overview | Projects, roles, capabilities |
| ID18 | Contact | Closing identity | Contact and relevant links |

## Copy-ready HTML fragments

Every registered layout has a complete fragment under `assets/layouts/IDxx.html`. Copy the fragment that matches the page plan instead of inventing a new section structure. Replace every square-bracket placeholder; the portfolio validator treats unresolved placeholders as P1 blockers.

The fragments deliberately contain only one `<section class="slide">`. Insert that section inside `<!-- PORTFOLIO_SLIDES -->` in `assets/portfolio-template.html`. Keep the `data-layout` value unchanged and replace `data-project` with the manifest project ID.

Run `python scripts/validate_layout_library.py` after changing any fragment. The check requires all ID01-ID18 files, matching layout IDs, project identifiers, and non-empty image alt text.

## System-specific composition recipes

ID01, ID03, ID08, ID10, ID13, ID14, and ID16 also have registered recipes under:

```text
assets/compositions/<style-preset>/ID01.html
assets/compositions/<style-preset>/ID03.html
assets/compositions/<style-preset>/ID08.html
assets/compositions/<style-preset>/ID10.html
assets/compositions/<style-preset>/ID13.html
assets/compositions/<style-preset>/ID14.html
assets/compositions/<style-preset>/ID16.html
```

Use these recipes when a visual system is selected. They keep the same layout ID and semantic evidence fields while changing the page skeleton:

- Workshop uses process boards, decision tickets, offsets, and visible making marks.
- Instrument uses registers, aligned evidence cells, status bands, and technical sidebars.
- Material uses a dominant contextual image, detail stacks, soft geometry, and slower reading rhythm.
- Gallery uses extreme type scale, a single dominant plate, exhibition captions, and editorial whitespace.

Use the shared `assets/layouts/IDxx.html` fragment as the fallback. Never mix recipes from different systems inside one portfolio.

## Image slots

| Slot | Ratio | Use |
|---|---|---|
| `hero-wide` | 16:9 or 21:9 | Final product, environment |
| `evidence-landscape` | 3:2 | Research, sketches, prototypes |
| `technical` | 4:3 or source ratio | CAD, section, exploded, test rig |
| `comparison` | matched pair | Before/after, alternatives |
| `material-strip` | 4:5 or square | CMF samples |

Use `object-fit: contain` for drawings, screenshots, diagrams, and text-bearing evidence. Use `cover` only for photographs whose crop does not remove evidence.

## Rhythm rules

- Start each project with ID16 or a project-specific ID14-style visual.
- Within every 4-5 pages, include one quiet synthesis page such as ID04 or ID13.
- Do not repeat the same layout more than twice consecutively.
- A 12-page case should use at least seven distinct layout IDs.
- End with resolution plus reflection; do not end on an unexplained render.
