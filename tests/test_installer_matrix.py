import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install_skill.py"
SKILL_NAME = "industrial-design-portfolio"
PLATFORMS = ("codex", "claude", "cursor", "gemini", "opencode", "agents")
REQUIRED = {
    "SKILL.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "VERSION",
    "LICENSE",
    "agents",
    "assets",
    "references",
    "schemas",
    "scripts",
}
FORBIDDEN = {
    ".github",
    "showcase",
    "evals",
    "tests",
    "README.md",
    "README.zh-CN.md",
    "requirements-test.txt",
    "package.json",
    "package-lock.json",
    "playwright.config.mjs",
    "node_modules",
}
RUNTIME_SCRIPTS = {
    "validate_layout_library.py",
    "validate_manifest.py",
    "validate_portfolio.py",
}


def install(dest: Path, platform: str, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(INSTALLER),
            "--platform",
            platform,
            "--dest",
            str(dest),
            *extra,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class InstallerMatrixTests(unittest.TestCase):
    def test_all_platforms_install_only_the_runtime_whitelist(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for platform in PLATFORMS:
                with self.subTest(platform=platform):
                    dest = base / platform
                    result = install(dest, platform)
                    self.assertEqual(0, result.returncode, result.stderr)
                    target = dest / SKILL_NAME
                    self.assertEqual(REQUIRED, {path.name for path in target.iterdir()})
                    self.assertFalse(FORBIDDEN & {path.name for path in target.iterdir()})
                    self.assertEqual(
                        RUNTIME_SCRIPTS,
                        {path.name for path in (target / "scripts").iterdir()},
                    )
                    recipes = list((target / "assets" / "compositions").glob("*/ID*.html"))
                    self.assertEqual(28, len(recipes))
                    metadata = (target / "agents" / "openai.yaml").read_text(encoding="utf-8")
                    self.assertIn('display_name: "Industrial Design Portfolio · 工业设计作品集"', metadata)
                    self.assertIn("$industrial-design-portfolio", metadata)

    def test_installed_validators_execute_without_repository_only_files(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory)
            result = install(dest, "agents")
            self.assertEqual(0, result.returncode, result.stderr)
            target = dest / SKILL_NAME

            layout = subprocess.run(
                [sys.executable, str(target / "scripts" / "validate_layout_library.py")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, layout.returncode, layout.stderr)

            manifest = subprocess.run(
                [
                    sys.executable,
                    str(target / "scripts" / "validate_manifest.py"),
                    str(target / "assets" / "portfolio_manifest.example.json"),
                ],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, manifest.returncode, manifest.stderr)

            portfolio = Path(directory) / "portfolio.html"
            portfolio.write_text(
                """<!doctype html><html data-style="workshop-orange"><head><title>Audit</title>
                <style>@media print{} @media(prefers-reduced-motion:reduce){}</style>
                </head><body><section class="slide" data-layout="ID01">Ready</section></body></html>""",
                encoding="utf-8",
            )
            html = subprocess.run(
                [
                    sys.executable,
                    str(target / "scripts" / "validate_portfolio.py"),
                    str(portfolio),
                ],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, html.returncode, html.stderr)

    def test_force_is_required_and_replaces_an_existing_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory)
            self.assertEqual(0, install(dest, "agents").returncode)
            sentinel = dest / SKILL_NAME / "stale.txt"
            sentinel.write_text("stale", encoding="utf-8")

            refused = install(dest, "agents")
            self.assertEqual(2, refused.returncode)
            self.assertTrue(sentinel.exists())

            replaced = install(dest, "agents", "--force")
            self.assertEqual(0, replaced.returncode, replaced.stderr)
            self.assertFalse(sentinel.exists())


if __name__ == "__main__":
    unittest.main()
