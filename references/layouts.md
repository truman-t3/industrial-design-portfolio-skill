# Registered Portfolio Layouts

## Contents

1. Layout selection rules
2. Registered layouts
3. Image slots
4. Rhythm rules

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

## Suggested HTML skeletons

### ID02 Project Brief

```html
<section class="slide theme-light" data-layout="ID02" data-project="project-a">
  <div class="slide-inner">
    <p class="eyebrow">PROJECT 01 · BRIEF</p>
    <h1 class="title-xl">A precise statement of the design problem.</h1>
    <div class="grid-4 brief-grid">
      <div><span class="label">USER</span><p>...</p></div>
      <div><span class="label">ROLE</span><p>...</p></div>
      <div><span class="label">TIME</span><p>...</p></div>
      <div><span class="label">CONSTRAINT</span><p>...</p></div>
    </div>
  </div>
</section>
```

### ID03 Evidence Wall

```html
<section class="slide theme-paper" data-layout="ID03" data-project="project-a">
  <div class="slide-inner">
    <header class="slide-head"><p class="eyebrow">OBSERVATION</p><h1>Evidence before interpretation</h1></header>
    <div class="evidence-grid">
      <figure class="frame"><img src="images/03-observation.jpg" alt="..."><figcaption>E2 · Source · Finding</figcaption></figure>
      <figure class="frame"><img src="images/03-prototype.jpg" alt="..."><figcaption>E2 · Prototype purpose</figcaption></figure>
    </div>
  </div>
</section>
```

### ID13 Iteration Delta

```html
<section class="slide theme-dark" data-layout="ID13" data-project="project-a">
  <div class="slide-inner">
    <p class="eyebrow">ITERATION 02</p><h1>What changed and why</h1>
    <div class="compare-grid">
      <figure class="frame"><img src="images/13-before.jpg" alt="Before"><figcaption>Before · observed failure</figcaption></figure>
      <figure class="frame"><img src="images/13-after.jpg" alt="After"><figcaption>After · design response</figcaption></figure>
    </div>
    <p class="decision-note">Because [evidence], we changed [decision], improving/targeting [effect].</p>
  </div>
</section>
```

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

