# Reproduction Prompt

> This is a reusable forward-test prompt, not a verbatim transcript of the original development session.

Give an Agent this `input/` folder and invoke the Skill with:

```text
Use $industrial-design-portfolio to turn this fictional brief into a
14-page industrial design case study for people evaluating the Skill.

Before planning pages:
1. inventory the supplied material;
2. list the questions that cannot be answered from the files;
3. separate evidence, assumptions, concept intent, and future validation;
4. refuse to invent users, quotes, prototypes, CAD, tests, measurements,
   engineering decisions, manufacturing conclusions, costs, or outcomes.

Use the registered industrial-design layouts. Create a portfolio manifest
and source notes. If concept images are generated, disclose them next to
every use. The architecture page must say "conceptual architecture
illustration", and the validation page must describe a future plan rather
than completed results.
```

Expected repository output:

```text
showcase/modular-desk-lamp/
├── index.html
├── portfolio_manifest.json
├── source_notes.md
├── storyboard.md
├── images/generated/*.webp
└── previews/*
```

The current Showcase is a reviewed reference output. A fresh Agent run may make different editorial or layout choices; it should preserve the same evidence boundaries.
