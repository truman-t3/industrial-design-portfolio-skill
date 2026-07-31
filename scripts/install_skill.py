#!/usr/bin/env python3
"""Install this Skill into common Agent Skills locations."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


SKILL_NAME = "industrial-design-portfolio"
PLATFORMS = ("codex", "claude", "cursor", "gemini", "opencode", "agents")
RUNTIME_FILES = ("SKILL.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "VERSION", "LICENSE")
RUNTIME_DIRS = ("agents", "assets", "references", "schemas")
RUNTIME_SCRIPTS = ("validate_layout_library.py", "validate_manifest.py", "validate_portfolio.py")


def user_base(platform: str) -> Path:
    home = Path.home()
    if platform == "codex":
        return Path(os.environ.get("CODEX_HOME", home / ".codex")) / "skills"
    if platform == "claude":
        return Path(os.environ.get("CLAUDE_CONFIG_DIR", home / ".claude")) / "skills"
    if platform == "cursor":
        return home / ".cursor" / "skills"
    if platform == "gemini":
        return home / ".gemini" / "skills"
    if platform == "opencode":
        config = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
        return config / "opencode" / "skills"
    return home / ".agents" / "skills"


def project_base(platform: str, project: Path) -> Path:
    names = {
        "codex": ".agents",
        "claude": ".claude",
        "cursor": ".cursor",
        "gemini": ".gemini",
        "opencode": ".opencode",
        "agents": ".agents",
    }
    return project / names[platform] / "skills"


def detect_platform() -> str:
    if os.environ.get("CODEX_HOME"):
        return "codex"
    candidates = [
        ("claude", Path.home() / ".claude"),
        ("cursor", Path.home() / ".cursor"),
        ("gemini", Path.home() / ".gemini"),
        ("opencode", Path.home() / ".config" / "opencode"),
    ]
    for name, path in candidates:
        if path.exists():
            return name
    return "agents"


def ignored(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in {"__pycache__", ".git", ".DS_Store"} or name.endswith(".pyc")}


def copy_runtime(source: Path, target: Path) -> None:
    target.mkdir(parents=True)
    for name in RUNTIME_FILES:
        path = source / name
        if not path.is_file():
            raise FileNotFoundError(f"Required runtime file is missing: {name}")
        shutil.copy2(path, target / name)
    for name in RUNTIME_DIRS:
        path = source / name
        if not path.is_dir():
            raise FileNotFoundError(f"Required runtime directory is missing: {name}")
        shutil.copytree(path, target / name, ignore=ignored)
    scripts_target = target / "scripts"
    scripts_target.mkdir()
    for name in RUNTIME_SCRIPTS:
        path = source / "scripts" / name
        if not path.is_file():
            raise FileNotFoundError(f"Required runtime script is missing: scripts/{name}")
        shutil.copy2(path, scripts_target / name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=("auto",) + PLATFORMS, default="auto")
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project root for project scope")
    parser.add_argument("--dest", type=Path, help="Explicit parent skills directory")
    parser.add_argument("--force", action="store_true", help="Replace an existing installation")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    platform = detect_platform() if args.platform == "auto" else args.platform
    source = Path(__file__).resolve().parent.parent
    base = args.dest.expanduser().resolve() if args.dest else (
        user_base(platform).expanduser() if args.scope == "user" else project_base(platform, args.project.resolve())
    )
    target = base / SKILL_NAME
    print(f"platform={platform} scope={args.scope}")
    print(f"source={source}")
    print(f"target={target}")
    if args.dry_run:
        return 0

    if target.exists():
        if not args.force:
            print("Target already exists; pass --force to replace it.", file=sys.stderr)
            return 2
        shutil.rmtree(target)
    base.mkdir(parents=True, exist_ok=True)
    copy_runtime(source, target)
    if not (target / "SKILL.md").is_file():
        print("Installation verification failed: SKILL.md missing", file=sys.stderr)
        return 3
    print(f"installed {SKILL_NAME} to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
