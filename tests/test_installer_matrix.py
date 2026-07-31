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
