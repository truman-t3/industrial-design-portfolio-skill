import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}
TEXT_FILENAMES = {
    ".gitattributes",
    ".gitignore",
    "LICENSE",
    "VERSION",
}
EXCLUDED_DIRS = {
    ".git",
    ".test-deps",
    "__pycache__",
    "blob-report",
    "node_modules",
    "playwright-report",
    "test-results",
    "tmp",
}


def repository_text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not EXCLUDED_DIRS.intersection(path.relative_to(ROOT).parts)
        and (
            path.suffix.lower() in TEXT_SUFFIXES
            or path.name in TEXT_FILENAMES
        )
    ]


class TextEncodingTests(unittest.TestCase):
    def test_all_repository_text_files_are_valid_utf8(self):
        failures: list[str] = []
        for path in repository_text_files():
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                failures.append(f"{path.relative_to(ROOT)}: {exc}")
                continue
            if "\ufffd" in text:
                failures.append(f"{path.relative_to(ROOT)}: contains replacement characters")
        self.assertEqual([], failures, "\n".join(failures))

    def test_openai_interface_metadata_is_readable_and_actionable(self):
        text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Industrial Design Portfolio · 工业设计作品集"', text)
        self.assertIn("把工业设计项目证据整理成可信、可讲述、可评审的作品集", text)
        self.assertIn('brand_color: "#1C67D2"', text)
        self.assertIn("$industrial-design-portfolio", text)


if __name__ == "__main__":
    unittest.main()
