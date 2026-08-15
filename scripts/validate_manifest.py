#!/usr/bin/env python3
"""Validate the evidence and authorship contract in a portfolio manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


LAYOUTS = {f"ID{i:02d}" for i in range(1, 19)}
LEVELS = {"E0", "E1", "E2", "E3"}
STATUSES = {"ready", "caveat", "to_validate", "omit"}
STYLE_PRESETS = {"workshop-orange", "instrument-blue", "material-green", "gallery-red"}


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def finding(level: str, message: str) -> tuple[str, str]:
    return level, message


def validate(data: object) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    if not isinstance(data, dict):
        return [finding("P0", "Manifest root must be a JSON object.")]

    for key in ("schema_version", "portfolio", "projects", "slides", "evidence", "assumptions", "generated_assets", "unresolved_gaps"):
        if key not in data:
            issues.append(finding("P0", f"Missing required field: {key}"))
    if data.get("schema_version") != "1.0":
        issues.append(finding("P1", "schema_version must be 1.0."))

    portfolio = data.get("portfolio")
    if not isinstance(portfolio, dict):
        issues.append(finding("P0", "portfolio must be an object."))
    else:
        for key in ("title", "audience", "presentation_context"):
            if not nonempty(portfolio.get(key)):
                issues.append(finding("P1", f"portfolio.{key} must be a non-empty string."))
        preset = portfolio.get("style_preset")
        if preset is None:
            issues.append(finding("P2", "portfolio.style_preset is not recorded; default to workshop-orange or choose a registered preset."))
        elif preset not in STYLE_PRESETS:
            issues.append(finding("P1", "portfolio.style_preset must be workshop-orange, instrument-blue, material-green, or gallery-red."))
        if preset is not None and not nonempty(portfolio.get("style_rationale")):
            issues.append(finding("P2", "portfolio.style_rationale should explain why the preset fits the evidence and audience."))

    projects = data.get("projects")
    project_ids: set[str] = set()
    if not isinstance(projects, list) or not projects:
        issues.append(finding("P0", "projects must contain at least one project."))
    else:
        for index, project in enumerate(projects, start=1):
            if not isinstance(project, dict):
                issues.append(finding("P0", f"projects[{index}] must be an object."))
                continue
            for key in ("id", "name", "thesis", "role"):
                if not nonempty(project.get(key)):
                    issues.append(finding("P1", f"projects[{index}].{key} must be a non-empty string."))
            project_id = project.get("id")
            if nonempty(project_id):
                if not re.fullmatch(r"[a-z0-9-]+", project_id):
                    issues.append(finding("P1", f"projects[{index}].id must use lowercase letters, numbers, or hyphens."))
                elif project_id in project_ids:
                    issues.append(finding("P0", f"Duplicate project id: {project_id}."))
                else:
                    project_ids.add(project_id)
            if not isinstance(project.get("contributions"), list) or not project["contributions"] or not all(nonempty(x) for x in project["contributions"]):
                issues.append(finding("P0", f"projects[{index}].contributions must list personal contributions."))

    evidence = data.get("evidence")
    evidence_ids: set[str] = set()
    if not isinstance(evidence, list):
        issues.append(finding("P0", "evidence must be an array."))
    else:
        for index, item in enumerate(evidence, start=1):
            if not isinstance(item, dict):
                issues.append(finding("P0", f"evidence[{index}] must be an object."))
                continue
            for key in ("id", "claim", "artifact", "source", "authorship"):
                if not nonempty(item.get(key)):
                    issues.append(finding("P0", f"evidence[{index}].{key} must be a non-empty string."))
            item_id = item.get("id")
            if nonempty(item_id):
                if item_id in evidence_ids:
                    issues.append(finding("P0", f"Duplicate evidence id: {item_id}."))
                evidence_ids.add(item_id)
            if item.get("level") not in LEVELS:
                issues.append(finding("P0", f"evidence[{index}].level must be E0, E1, E2, or E3."))
            if item.get("status") not in STATUSES:
                issues.append(finding("P1", f"evidence[{index}].status is invalid."))
            if item.get("level") == "E0" and item.get("status") == "ready":
                issues.append(finding("P0", f"evidence[{index}] is E0 and cannot be ready; mark it as an assumption, caveat, or omission."))

    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        issues.append(finding("P0", "slides must contain at least one slide."))
    else:
        pages: set[int] = set()
        for index, slide in enumerate(slides, start=1):
            if not isinstance(slide, dict):
                issues.append(finding("P0", f"slides[{index}] must be an object."))
                continue
            page = slide.get("page")
            if not isinstance(page, int) or page < 1:
                issues.append(finding("P1", f"slides[{index}].page must be a positive integer."))
            elif page in pages:
                issues.append(finding("P1", f"Duplicate slide page: {page}."))
            else:
                pages.add(page)
            if slide.get("project_id") not in project_ids:
                issues.append(finding("P0", f"slides[{index}] references an unknown project_id."))
            if slide.get("layout_id") not in LAYOUTS:
                issues.append(finding("P1", f"slides[{index}].layout_id must be a registered ID01-ID18 layout."))
            claim_ids = slide.get("claim_ids")
            if not isinstance(claim_ids, list):
                issues.append(finding("P1", f"slides[{index}].claim_ids must be an array."))
            else:
                for claim_id in claim_ids:
                    if claim_id not in evidence_ids:
                        issues.append(finding("P0", f"slides[{index}] references unknown evidence id: {claim_id}."))

    generated = data.get("generated_assets")
    if not isinstance(generated, list):
        issues.append(finding("P0", "generated_assets must be an array."))
    else:
        for index, asset in enumerate(generated, start=1):
            if not isinstance(asset, dict) or not nonempty(asset.get("file")) or not nonempty(asset.get("disclosure")):
                issues.append(finding("P0", f"generated_assets[{index}] must include file and visible disclosure."))

    for key in ("assumptions", "unresolved_gaps"):
        if not isinstance(data.get(key), list):
            issues.append(finding("P0", f"{key} must be an array."))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"P0: File not found: {args.manifest}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"P0: Invalid JSON: {exc}")
        return 2
    issues = validate(data)
    for level in ("P0", "P1", "P2", "P3"):
        for item_level, message in issues:
            if item_level == level:
                print(f"{level}: {message}")
    blockers = sum(level in {"P0", "P1"} for level, _ in issues)
    print(f"Checked {args.manifest}: {len(issues)} finding(s), {blockers} blocker(s).")
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
