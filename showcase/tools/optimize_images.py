#!/usr/bin/env python3
"""Create deterministic, browser-ready WebP derivatives for the Showcase."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError as exc:  # pragma: no cover - exercised by the dependency check
    raise SystemExit(
        "Pillow is required. Install it with: "
        "python -m pip install -r showcase/requirements-dev.txt"
    ) from exc


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def optimize(source: Path, target: Path, max_edge: int, quality: int) -> tuple[int, int]:
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        width, height = image.size
        longest = max(width, height)
        if longest > max_edge:
            scale = max_edge / longest
            image = image.resize(
                (max(1, round(width * scale)), max(1, round(height * scale))),
                Image.Resampling.LANCZOS,
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(
            target,
            format="WEBP",
            quality=quality,
            method=6,
            optimize=True,
            exif=b"",
            icc_profile=None,
        )
        return image.size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "modular-desk-lamp" / "images" / "generated",
    )
    parser.add_argument("--quality", type=int, default=82)
    parser.add_argument("--max-edge", type=int, default=1680)
    parser.add_argument("--single-budget-kb", type=int, default=700)
    parser.add_argument("--total-budget-mb", type=float, default=4.0)
    args = parser.parse_args()

    sources = sorted(args.source_dir.glob("*.png"))
    if not sources:
        print(f"No PNG files found in {args.source_dir}", file=sys.stderr)
        return 2

    total = 0
    over_budget: list[str] = []
    for source in sources:
        target = source.with_suffix(".webp")
        width, height = optimize(source, target, args.max_edge, args.quality)
        size = target.stat().st_size
        total += size
        if size > args.single_budget_kb * 1024:
            over_budget.append(target.name)
        print(
            f"{target.name}: {width}x{height} · {size / 1024:.1f} KB · "
            f"sha256:{digest(target)}"
        )

    print(f"total: {total / 1024 / 1024:.2f} MB across {len(sources)} image(s)")
    if total > args.total_budget_mb * 1024 * 1024:
        over_budget.append("TOTAL")
    if over_budget:
        print(f"Budget exceeded: {', '.join(over_budget)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
