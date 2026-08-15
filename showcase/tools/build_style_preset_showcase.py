#!/usr/bin/env python3
"""Build the README's reproducible four-preset comparison board."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[2]
RENDERER = Path(__file__).with_name("render_style_preset_previews.mjs")
TEMP = ROOT / "tmp" / "style-preset-renders"
OUTPUT = ROOT / "showcase" / "style-presets" / "style-presets.webp"
PRESETS = (
    "workshop-orange",
    "instrument-blue",
    "material-green",
    "gallery-red",
)

TILE = (720, 405)
MARGIN = 32
GAP = 20
SHADOW = 6
BACKGROUND = "#111312"
FRAME = "#404541"
SHADOW_COLOR = "#050605"
PANEL_BACKGROUND = "#202421"
PANEL_FRAME = "#5A625D"


def build_system_tile(preset: str) -> Image.Image:
    """Compose cover, evidence, and resolution renders into one comparison tile."""

    tile = Image.new("RGB", TILE, PANEL_BACKGROUND)
    placements = (
        ("ID01", (14, 75, 468, 330)),
        ("ID03", (482, 62, 706, 188)),
        ("ID14", (482, 217, 706, 343)),
    )
    draw = ImageDraw.Draw(tile)
    for layout, bounds in placements:
        source = TEMP / f"{preset}-{layout}.png"
        if not source.is_file():
            raise SystemExit(f"Missing rendered preset page: {source}")
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        with Image.open(source) as opened:
            panel = ImageOps.fit(
                ImageOps.exif_transpose(opened).convert("RGB"),
                (width, height),
                method=Image.Resampling.LANCZOS,
            )
        tile.paste(panel, (bounds[0], bounds[1]))
        draw.rectangle(bounds, outline=PANEL_FRAME, width=1)
    return tile


def main() -> int:
    if TEMP.exists():
        shutil.rmtree(TEMP)
    TEMP.mkdir(parents=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        ["node", str(RENDERER), str(TEMP)],
        cwd=ROOT,
        check=True,
    )
    rendered = tuple(json.loads((TEMP / "presets.json").read_text(encoding="utf-8")))
    if rendered != PRESETS:
        raise SystemExit(f"Renderer preset order does not match builder: {rendered!r}")

    width = MARGIN * 2 + TILE[0] * 2 + GAP
    height = MARGIN * 2 + TILE[1] * 2 + GAP
    board = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(board)

    for index, preset in enumerate(PRESETS):
        column = index % 2
        row = index // 2
        x = MARGIN + column * (TILE[0] + GAP)
        y = MARGIN + row * (TILE[1] + GAP)
        tile = build_system_tile(preset)
        draw.rectangle(
            (x + SHADOW, y + SHADOW, x + TILE[0] + SHADOW, y + TILE[1] + SHADOW),
            fill=SHADOW_COLOR,
        )
        board.paste(tile, (x, y))
        draw.rectangle(
            (x, y, x + TILE[0] - 1, y + TILE[1] - 1),
            outline=FRAME,
            width=2,
        )

    board.save(
        OUTPUT,
        format="WEBP",
        quality=86,
        method=6,
        optimize=True,
        exif=b"",
        icc_profile=None,
    )
    shutil.rmtree(TEMP)
    print(f"{OUTPUT}: {board.width}x{board.height} · {OUTPUT.stat().st_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
