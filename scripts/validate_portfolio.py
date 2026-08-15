#!/usr/bin/env python3
"""Validate structural and credibility markers in an HTML portfolio deck."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REGISTERED = {f"ID{i:02d}" for i in range(1, 19)}
PLACEHOLDERS = (
    "[PORTFOLIO_TITLE]",
    "[DESIGNER_NAME]",
    "[PORTFOLIO_META]",
    "PORTFOLIO_SLIDES",
    "TODO",
    "TBD",
    "Lorem ipsum",
)
GENERIC_PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9_ -]{2,}\]")


def issue(level: str, message: str) -> tuple[str, str]:
    return level, message


def validate(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    findings: list[tuple[str, str]] = []

    for token in PLACEHOLDERS:
        if token.lower() in text.lower():
            findings.append(issue("P1", f"Unresolved placeholder: {token}"))
    for token in sorted(set(GENERIC_PLACEHOLDER.findall(text)) - set(PLACEHOLDERS)):
        findings.append(issue("P1", f"Unresolved placeholder: {token}"))

    preset_match = re.search(r"<html\b[^>]*\bdata-style=[\"']([^\"']+)[\"']", text, re.I)
    html_preset = preset_match.group(1) if preset_match else None
    if html_preset is None:
        findings.append(issue("P1", "The root html element has no data-style preset."))

    slides = re.findall(r"<section\b[^>]*class=[\"'][^\"']*\bslide\b[^\"']*[\"'][^>]*>", text, re.I)
    if not slides:
        findings.append(issue("P1", "No slide sections found."))

    layout_counts: dict[str, int] = {}
    for index, tag in enumerate(slides, start=1):
        match = re.search(r"data-layout=[\"']([^\"']+)[\"']", tag, re.I)
        if not match:
            findings.append(issue("P1", f"Slide {index} has no data-layout."))
            continue
        layout = match.group(1)
        layout_counts[layout] = layout_counts.get(layout, 0) + 1
        if layout not in REGISTERED:
            findings.append(issue("P1", f"Slide {index} uses unregistered layout {layout}."))

    image_tags = re.findall(r"<img\b[^>]*>", text, re.I)
    for index, tag in enumerate(image_tags, start=1):
        if not re.search(r"\balt=[\"'][^\"']+[\"']", tag, re.I):
            findings.append(issue("P1", f"Image {index} has missing or empty alt text."))
        direct_src = re.search(r"(?<!data-)\bsrc=[\"']([^\"']+)[\"']", tag, re.I)
        if direct_src and not direct_src.group(1).lower().startswith("data:") and not re.search(
            r"(?:generated|ai-)", direct_src.group(1), re.I
        ):
            findings.append(issue("P2", f"Image {index} loads eagerly; prefer data-src for the lightweight page window."))

    generated_refs = re.findall(r"(?:(?:src|data-src)=[\"'][^\"']*(?:generated|ai-)[^\"']*[\"']|AI-assisted|AI generated)", text, re.I)
    disclosures = re.findall(r"AI-assisted concept visualization|Not engineering evidence", text, re.I)
    if generated_refs and not disclosures:
        findings.append(issue("P0", "Generated imagery appears without an AI disclosure."))

    generated_paths = re.findall(r"data-src=[\"']([^\"']*images/generated/[^\"']+)[\"']", text, re.I)
    direct_generated = re.findall(r"(?<!data-)src=[\"']([^\"']*images/generated/[^\"']+)[\"']", text, re.I)
    for ref in direct_generated:
        findings.append(issue("P1", f"Generated image bypasses deferred loading: {ref}"))
    for ref in sorted(set(generated_paths)):
        if Path(ref).suffix.lower() != ".webp":
            findings.append(issue("P1", f"Browser-facing generated image is not WebP: {ref}"))
        if not (path.parent / ref).is_file():
            findings.append(issue("P1", f"Deferred image file is missing: {ref}"))

    slide_blocks = re.findall(r"<section\b[^>]*class=[\"'][^\"']*\bslide\b[^\"']*[\"'][^>]*>.*?</section>", text, re.I | re.S)
    for index, block in enumerate(slide_blocks, start=1):
        if re.search(r"data-src=[\"'][^\"']*images/generated/", block, re.I) and not re.search(
            r"AI-assisted|Not engineering evidence|Not research evidence|Not test evidence", block, re.I
        ):
            findings.append(issue("P0", f"Slide {index} has generated imagery without a nearby disclosure."))

    manifest_path = path.parent / "portfolio_manifest.json"
    manifest: dict | None = None
    if manifest_path.is_file():
        try:
            loaded_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if isinstance(loaded_manifest, dict):
                manifest = loaded_manifest
            else:
                findings.append(issue("P1", "Could not verify HTML against manifest: root must be an object."))
        except (json.JSONDecodeError, OSError) as exc:
            findings.append(issue("P1", f"Could not verify HTML against manifest: {exc}"))

    if manifest is not None:
        manifest_preset = manifest.get("portfolio", {}).get("style_preset")
        if html_preset and manifest_preset and html_preset != manifest_preset:
            findings.append(
                issue(
                    "P1",
                    f"HTML data-style {html_preset!r} does not match manifest style_preset {manifest_preset!r}.",
                )
            )
        if generated_paths:
            manifest_paths = {
                item.get("file") for item in manifest.get("generated_assets", []) if isinstance(item, dict)
            }
            missing = sorted(set(generated_paths) - manifest_paths)
            stale = sorted(manifest_paths - set(generated_paths))
            for ref in missing:
                findings.append(issue("P1", f"Generated image is missing from manifest: {ref}"))
            for ref in stale:
                findings.append(issue("P1", f"Manifest generated asset is not used by HTML: {ref}"))

    if len(slides) >= 12 and len(layout_counts) < 7:
        findings.append(issue("P2", "A 12+ page case uses fewer than seven distinct layouts."))

    sequences = []
    for tag in slides:
        match = re.search(r"data-layout=[\"'](ID\d{2})[\"']", tag, re.I)
        if match:
            sequences.append(match.group(1))
    for i in range(len(sequences) - 2):
        if sequences[i] == sequences[i + 1] == sequences[i + 2]:
            findings.append(issue("P2", f"Layout {sequences[i]} repeats three times consecutively."))
            break

    if "prefers-reduced-motion" not in text:
        findings.append(issue("P1", "No reduced-motion CSS handling found."))
    if "@media print" not in text:
        findings.append(issue("P3", "No print/PDF CSS found."))
    if not re.search(r"<title>[^<]+</title>", text, re.I):
        findings.append(issue("P1", "Document title is missing."))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Path to portfolio index.html")
    args = parser.parse_args()
    if not args.html.is_file():
        print(f"P0: File not found: {args.html}")
        return 2

    findings = validate(args.html)
    for level in ("P0", "P1", "P2", "P3"):
        for item_level, message in findings:
            if item_level == level:
                print(f"{level}: {message}")

    blockers = sum(1 for level, _ in findings if level in {"P0", "P1"})
    print(f"Checked {args.html}: {len(findings)} finding(s), {blockers} blocker(s).")
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
