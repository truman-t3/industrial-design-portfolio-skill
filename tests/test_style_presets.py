import json
import re
import tempfile
import unittest
from pathlib import Path

from scripts.validate_portfolio import validate as validate_portfolio


ROOT = Path(__file__).resolve().parents[1]
PRESETS = {
    "workshop-orange",
    "instrument-blue",
    "material-green",
    "gallery-red",
}


class StylePresetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = (ROOT / "assets" / "portfolio-template.html").read_text(encoding="utf-8")
        cls.reference = (ROOT / "references" / "style-presets.md").read_text(encoding="utf-8")
        cls.schema = json.loads(
            (ROOT / "schemas" / "portfolio-manifest.schema.json").read_text(encoding="utf-8")
        )

    def test_template_exposes_one_root_style_slot(self):
        self.assertIn('data-style="[STYLE_PRESET]"', self.template)
        self.assertEqual(1, self.template.count("[STYLE_PRESET]"))

    def test_every_registered_preset_has_css_and_guidance(self):
        for preset in PRESETS:
            with self.subTest(preset=preset):
                self.assertIn(f'html[data-style="{preset}"]', self.template)
                self.assertIn(f'`{preset}`', self.reference)

    def test_manifest_enum_matches_registered_presets(self):
        enum = set(
            self.schema["properties"]["portfolio"]["properties"]["style_preset"]["enum"]
        )
        self.assertEqual(PRESETS, enum)

    def test_presets_change_more_than_accent_color(self):
        for preset in PRESETS - {"workshop-orange"}:
            with self.subTest(preset=preset):
                selector = f'html[data-style="{preset}"]'
                declaration = self.template.split(selector, 1)[1].split("}", 1)[0]
                self.assertIn("--accent:", declaration)
                self.assertIn("--display:", declaration)
                self.assertIn("--grid-opacity:", declaration)

    def test_each_system_changes_composition_on_key_layouts(self):
        key_layouts = {"ID01", "ID03", "ID08", "ID10", "ID14", "ID16"}
        for preset in PRESETS:
            with self.subTest(preset=preset):
                selectors = set(
                    re.findall(
                        rf'html\[data-style="{re.escape(preset)}"\] \[data-layout="(ID\d\d)"\]',
                        self.template,
                    )
                )
                self.assertTrue(key_layouts.issubset(selectors))

    def test_signature_composition_recipes_are_copy_ready_and_distinct(self):
        required_layouts = {"ID01", "ID03", "ID08", "ID10", "ID13", "ID14", "ID16"}
        required_fields = {
            "ID01": {"[SYSTEM LABEL]", "[PORTFOLIO THESIS]", "[PROJECT NAME]", "[PORTFOLIO META]"},
            "ID03": {
                "[EVIDENCE QUESTION]", "[EVIDENCE TAKEAWAY]",
                *{f"[EVIDENCE IMAGE {index}]" for index in range(1, 4)},
                *{f"[EVIDENCE DESCRIPTION {index}]" for index in range(1, 4)},
                *{f"[EVIDENCE CAPTION {index}]" for index in range(1, 4)},
            },
            "ID14": {
                "[FINAL VALUE PROPOSITION]", "[FINAL PRODUCT IMAGE]",
                "[FINAL PRODUCT DESCRIPTION]", "[FINAL STATUS]", "[FINAL TAKEAWAY]",
            },
            "ID08": {
                "[CMF TITLE]", "[CMF IMAGE]", "[CMF IMAGE DESCRIPTION]", "[CMF STATUS]",
                "[CMF RATIONALE]", "[SWATCH 1]", "[SWATCH 2]", "[SWATCH 3]",
                "[MATERIAL 1]", "[MATERIAL 2]", "[MATERIAL 3]",
            },
            "ID10": {
                "[ARCHITECTURE TITLE]", "[ARCHITECTURE IMAGE]", "[ARCHITECTURE DESCRIPTION]",
                "[ARCHITECTURE STATUS]", "[ARCHITECTURE TAKEAWAY]",
                *{f"[COMPONENT {index}]" for index in range(1, 5)},
            },
            "ID13": {
                "[ITERATION TITLE]", "[ITERATION TAKEAWAY]",
                "[ITERATION IMAGE 1]", "[ITERATION IMAGE 2]",
                "[ITERATION DESCRIPTION 1]", "[ITERATION DESCRIPTION 2]",
                "[ITERATION CAPTION 1]", "[ITERATION CAPTION 2]",
            },
            "ID16": {"[PROJECT NUMBER]", "[PROJECT NAME]", "[PROJECT THESIS]", "[PROJECT META]"},
        }
        for preset in PRESETS:
            directory = ROOT / "assets" / "compositions" / preset
            self.assertTrue(directory.is_dir())
            self.assertEqual(required_layouts, {path.stem for path in directory.glob("ID*.html")})
            for layout in required_layouts:
                text = (directory / f"{layout}.html").read_text(encoding="utf-8")
                self.assertIn(f'data-layout="{layout}"', text)
                self.assertIn(f"composition-{preset.split('-', 1)[0]}", text)
                for field in required_fields[layout]:
                    self.assertIn(field, text)
        for layout in required_layouts:
            recipes = {
                (ROOT / "assets" / "compositions" / preset / f"{layout}.html").read_text(
                    encoding="utf-8"
                )
                for preset in PRESETS
            }
            self.assertEqual(4, len(recipes), f"{layout} recipes must not collapse to one skeleton")

    @staticmethod
    def _luminance(color):
        if len(color) == 4:
            color = "#" + "".join(channel * 2 for channel in color[1:])
        channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [
            value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
            for value in channels
        ]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    @classmethod
    def _contrast(cls, foreground, background):
        lighter, darker = sorted(
            (cls._luminance(foreground), cls._luminance(background)), reverse=True
        )
        return (lighter + 0.05) / (darker + 0.05)

    def test_semantic_accent_text_roles_meet_small_text_contrast(self):
        for preset in PRESETS:
            with self.subTest(preset=preset):
                selector = f'html[data-style="{preset}"]'
                declaration = self.template.split(selector, 1)[1].split("}", 1)[0]
                root_declaration = self.template.split(":root{", 1)[1].split("}", 1)[0]
                tokens = dict(re.findall(r"--([a-z-]+):(#[0-9a-fA-F]{3,6})", root_declaration))
                tokens.update(re.findall(r"--([a-z-]+):(#[0-9a-fA-F]{3,6})", declaration))
                pairs = (
                    ("accent-text", "paper"),
                    ("accent-on-dark", "dark-paper"),
                    ("on-accent", "accent"),
                )
                for foreground, background in pairs:
                    self.assertGreaterEqual(
                        self._contrast(tokens[foreground], tokens[background]),
                        4.5,
                        f"{preset} {foreground} on {background}",
                    )

    def test_accent_pages_use_semantic_foreground_tokens(self):
        self.assertIn("--accent-text:var(--on-accent)", self.template)
        self.assertIn("color:var(--accent-text)", self.template)
        self.assertNotIn(".eyebrow,.label{color:var(--accent)", self.template)

    def test_slide_recomputes_text_color_for_tonal_theme(self):
        slide_rule = self.template.split(".slide{", 1)[1].split("}", 1)[0]
        self.assertIn("color:var(--ink)", slide_rule)

    def test_readme_uses_real_rendered_preset_comparison(self):
        preview = ROOT / "showcase" / "style-presets" / "style-presets.webp"
        self.assertTrue(preview.is_file())
        self.assertGreater(preview.stat().st_size, 10_000)
        header = preview.read_bytes()[:12]
        self.assertEqual(b"RIFF", header[:4])
        self.assertEqual(b"WEBP", header[8:12])
        for filename in ("README.md", "README.zh-CN.md"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            self.assertIn("showcase/style-presets/style-presets.webp", text)

    def test_preview_renderer_uses_the_canonical_template_and_all_presets(self):
        renderer = (ROOT / "showcase" / "tools" / "render_style_preset_previews.mjs").read_text(
            encoding="utf-8"
        )
        self.assertIn('assets", "portfolio-template.html', renderer)
        self.assertIn('"assets", "compositions", preset', renderer)
        for preset in PRESETS:
            self.assertIn(preset, renderer)
        for layout in ("ID01", "ID03", "ID14"):
            self.assertIn(layout, renderer)

    def test_portfolio_validator_matches_html_preset_to_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            html = root / "index.html"
            html.write_text(
                '<!doctype html><html data-style="gallery-red"><head><title>Test</title>'
                '<style>@media print{} @media(prefers-reduced-motion:reduce){}</style></head>'
                '<body><section class="slide" data-layout="ID01"></section></body></html>',
                encoding="utf-8",
            )
            (root / "portfolio_manifest.json").write_text(
                json.dumps({"portfolio": {"style_preset": "instrument-blue"}}),
                encoding="utf-8",
            )
            messages = [message for _, message in validate_portfolio(html)]
            self.assertTrue(any("does not match manifest style_preset" in message for message in messages))

    def test_layout_rhythm_ignores_css_data_layout_selectors(self):
        with tempfile.TemporaryDirectory() as directory:
            html = Path(directory) / "index.html"
            css = "".join('[data-layout="ID01"]{}' for _ in range(4))
            slides = "".join(
                f'<section class="slide" data-layout="ID{index:02d}"></section>'
                for index in range(1, 5)
            )
            html.write_text(
                f'<!doctype html><html data-style="workshop-orange"><head><title>Test</title>'
                f'<style>{css}@media print{{}}@media(prefers-reduced-motion:reduce){{}}</style>'
                f'</head><body>{slides}</body></html>',
                encoding="utf-8",
            )
            messages = [message for _, message in validate_portfolio(html)]
            self.assertFalse(any("repeats three times" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
