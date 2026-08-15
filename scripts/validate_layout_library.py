#!/usr/bin/env python3
"""Validate the bundled ID01-ID18 HTML layout fragment library."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REGISTERED = {f"ID{i:02d}" for i in range(1, 19)}
COMPOSITION_IDS = {"ID01", "ID03", "ID08", "ID10", "ID13", "ID14", "ID16"}
COMPOSITION_PRESETS = {
    "workshop-orange",
    "instrument-blue",
    "material-green",
    "gallery-red",
}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    layout_dir = root / "assets" / "layouts"
    findings: list[str] = []
    files = {path.stem.upper(): path for path in layout_dir.glob("ID*.html")}

    missing = sorted(REGISTERED - set(files))
    extra = sorted(set(files) - REGISTERED)
    if missing:
        findings.append("Missing layout fragments: " + ", ".join(missing))
    if extra:
        findings.append("Unregistered layout fragments: " + ", ".join(extra))

    for layout_id in sorted(REGISTERED & set(files)):
        text = files[layout_id].read_text(encoding="utf-8")
        sections = re.findall(r"<section\b[^>]*>", text, re.I)
        if len(sections) != 1:
            findings.append(f"{layout_id}: expected exactly one section element")
            continue
        section = sections[0]
        if not re.search(r'class=["\'][^"\']*\bslide\b', section, re.I):
            findings.append(f"{layout_id}: section is missing slide class")
        match = re.search(r'data-layout=["\']([^"\']+)', section, re.I)
        if not match or match.group(1).upper() != layout_id:
            findings.append(f"{layout_id}: data-layout does not match file name")
        if not re.search(r'data-project=["\'][^"\']+', section, re.I):
            findings.append(f"{layout_id}: data-project is missing")
        for image_index, tag in enumerate(re.findall(r"<img\b[^>]*>", text, re.I), start=1):
            if not re.search(r'\balt=["\'][^"\']+["\']', tag, re.I):
                findings.append(f"{layout_id}: image {image_index} has missing or empty alt text")

    composition_root = root / "assets" / "compositions"
    composition_count = 0
    found_presets = {path.name for path in composition_root.iterdir() if path.is_dir()}
    missing_presets = sorted(COMPOSITION_PRESETS - found_presets)
    extra_presets = sorted(found_presets - COMPOSITION_PRESETS)
    if missing_presets:
        findings.append("Missing composition presets: " + ", ".join(missing_presets))
    if extra_presets:
        findings.append("Unregistered composition presets: " + ", ".join(extra_presets))

    for preset in sorted(COMPOSITION_PRESETS & found_presets):
        preset_dir = composition_root / preset
        variants = {path.stem.upper(): path for path in preset_dir.glob("ID*.html")}
        missing_variants = sorted(COMPOSITION_IDS - set(variants))
        extra_variants = sorted(set(variants) - COMPOSITION_IDS)
        if missing_variants:
            findings.append(f"{preset}: missing composition recipes: " + ", ".join(missing_variants))
        if extra_variants:
            findings.append(f"{preset}: unregistered composition recipes: " + ", ".join(extra_variants))
        for layout_id in sorted(COMPOSITION_IDS & set(variants)):
            composition_count += 1
            text = variants[layout_id].read_text(encoding="utf-8")
            sections = re.findall(r"<section\b[^>]*>", text, re.I)
            label = f"{preset}/{layout_id}"
            if len(sections) != 1:
                findings.append(f"{label}: expected exactly one section element")
                continue
            section = sections[0]
            if not re.search(r'class=["\'][^"\']*\bslide\b', section, re.I):
                findings.append(f"{label}: section is missing slide class")
            match = re.search(r'data-layout=["\']([^"\']+)', section, re.I)
            if not match or match.group(1).upper() != layout_id:
                findings.append(f"{label}: data-layout does not match file name")
            if not re.search(r'data-project=["\'][^"\']+', section, re.I):
                findings.append(f"{label}: data-project is missing")
            if f"composition-{preset.split('-', 1)[0]}" not in section:
                findings.append(f"{label}: system composition class is missing")
            for image_index, tag in enumerate(re.findall(r"<img\b[^>]*>", text, re.I), start=1):
                if not re.search(r'\balt=["\'][^"\']+["\']', tag, re.I):
                    findings.append(f"{label}: image {image_index} has missing or empty alt text")
                if not re.search(r'\bdata-src=["\'][^"\']+["\']', tag, re.I):
                    findings.append(f"{label}: image {image_index} must use data-src")

    for message in findings:
        print(f"P1: {message}")
    print(
        f"Checked {len(files)} shared layout fragment(s) and "
        f"{composition_count} composition recipe(s): {len(findings)} finding(s)."
    )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
