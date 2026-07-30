#!/usr/bin/env python3
"""Validate the bundled ID01-ID18 HTML layout fragment library."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REGISTERED = {f"ID{i:02d}" for i in range(1, 19)}


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

    for message in findings:
        print(f"P1: {message}")
    print(f"Checked {len(files)} layout fragment(s): {len(findings)} finding(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
