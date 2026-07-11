# Platform Compatibility

## Contents

1. Canonical source
2. Native skill locations
3. Adapter files
4. Capability fallbacks
5. Installation and discovery checks

## Canonical source

`SKILL.md` is the only normative source. Keep its YAML frontmatter limited to `name` and `description` for broad compatibility. Generate adapter instruction files with `scripts/sync_adapters.py`; never edit adapters independently.

The complete skill directory must remain intact because references, scripts, assets, and evaluation cases are resolved relative to `SKILL.md`.

## Native skill locations

Use the platform's native Skill directory when available:

| Runtime | User scope | Project scope | Notes |
|---|---|---|---|
| Codex | `$CODEX_HOME/skills/industrial-design-portfolio` or `~/.codex/skills/industrial-design-portfolio` | `.agents/skills/industrial-design-portfolio` | Keep `agents/openai.yaml` for Codex UI metadata |
| Claude Code | `~/.claude/skills/industrial-design-portfolio` | `.claude/skills/industrial-design-portfolio` | Reads Agent Skills packages |
| Cursor | `~/.cursor/skills/industrial-design-portfolio` | `.cursor/skills/industrial-design-portfolio` | Use the full directory |
| Gemini CLI | `~/.gemini/skills/industrial-design-portfolio` | `.gemini/skills/industrial-design-portfolio` | Refresh with `/skills reload` when needed |
| OpenCode | `~/.config/opencode/skills/industrial-design-portfolio` | `.opencode/skills/industrial-design-portfolio` | Also recognizes `.agents/skills` and `.claude/skills` |
| Generic Agent Skills | `~/.agents/skills/industrial-design-portfolio` | `.agents/skills/industrial-design-portfolio` | Preferred neutral fallback |

Run `python scripts/install_skill.py --help` for the current installer options. Prefer an explicit platform over automatic detection when several agents are installed.

## Adapter files

The package includes:

- `AGENTS.md` — generic persistent-instruction adapter for agents that read project guidance but do not discover skills.
- `CLAUDE.md` — Claude-compatible project instruction adapter.
- `GEMINI.md` — Gemini CLI hierarchical-context adapter.

These files contain the same core body as `SKILL.md` plus a short platform header. Native Skill installation is preferred because it loads on demand; copying an adapter to a project root makes the entire instruction persistent and consumes more context.

## Capability fallbacks

| Needed capability | Preferred | Fallback |
|---|---|---|
| Ask a material question | Native question tool | Plain chat question |
| Read/write files | Native filesystem tools | Return a file plan and copy-ready content |
| Run validator | Python 3 shell | Manual P0/P1 checklist |
| Preview HTML | Browser/computer tool | Structural validation + pending visual QA note |
| Generate imagery | Native image-generation tool | Supplied assets or labeled placeholders |
| Research current facts | Web/search connector | User-provided sources + unverified label |
| Create PDF | Browser print/export | Deliver reviewed HTML only |

Never substitute a different tool silently when it changes fidelity, cost, privacy, or evidence status.

## Installation and discovery checks

After installation:

1. Confirm `<target>/industrial-design-portfolio/SKILL.md` exists.
2. Confirm `references/`, `scripts/`, and `assets/` remain adjacent.
3. Confirm the folder name matches the `name` field exactly.
4. Restart or reload the runtime's Skill registry if it does not auto-refresh.
5. Ask for an industrial design portfolio task and confirm this Skill is discoverable.
6. Run `python scripts/sync_adapters.py --check` to detect adapter drift.
7. Run the platform-neutral smoke evaluation in `evals/evals.json` when changing workflow behavior.

Do not install by copying only `AGENTS.md` when the user expects the HTML template, references, and validator to work.

