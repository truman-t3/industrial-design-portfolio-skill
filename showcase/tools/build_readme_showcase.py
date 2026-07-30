#!/usr/bin/env python3
"""Build the deterministic six-page Showcase board used by the READMEs."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1] / "modular-desk-lamp"
PREVIEWS = ROOT / "previews"
SOURCES = (
    "01-cover.png",
    "04-evidence.png",
    "08-cmf.png",
    "09-architecture.png",
    "11-iteration.png",
    "12-final.png",
)
OUTPUT = PREVIEWS / "readme-showcase.webp"

TILE = (496, 279)
MARGIN = 36
GAP = 20
SHADOW = 6
BACKGROUND = "#0b1f37"
FRAME = "#2d6ed0"
SHADOW_COLOR = "#06111f"


def main() -> int:
    width = MARGIN * 2 + TILE[0] * 3 + GAP * 2
    height = MARGIN * 2 + TILE[1] * 2 + GAP
    board = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(board)

    for index, name in enumerate(SOURCES):
        source = PREVIEWS / name
        if not source.is_file():
            raise SystemExit(f"Missing preview: {source}")
        column = index % 3
        row = index // 3
        x = MARGIN + column * (TILE[0] + GAP)
        y = MARGIN + row * (TILE[1] + GAP)
        with Image.open(source) as opened:
            tile = ImageOps.fit(
                ImageOps.exif_transpose(opened).convert("RGB"),
                TILE,
                method=Image.Resampling.LANCZOS,
            )
        draw.rounded_rectangle(
            (x + SHADOW, y + SHADOW, x + TILE[0] + SHADOW, y + TILE[1] + SHADOW),
            radius=8,
            fill=SHADOW_COLOR,
        )
        board.paste(tile, (x, y))
        draw.rounded_rectangle(
            (x, y, x + TILE[0] - 1, y + TILE[1] - 1),
            radius=7,
            outline=FRAME,
            width=2,
        )

    board.save(
        OUTPUT,
        format="WEBP",
        quality=84,
        method=6,
        optimize=True,
        exif=b"",
        icc_profile=None,
    )
    print(f"{OUTPUT}: {board.width}x{board.height} · {OUTPUT.stat().st_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
