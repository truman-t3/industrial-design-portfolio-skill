import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadmeConsistencyTests(unittest.TestCase):
    def test_version_is_consistent_across_package_and_readmes(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        package = (ROOT / "package.json").read_text(encoding="utf-8")
        package_lock = (ROOT / "package-lock.json").read_text(encoding="utf-8")
        for filename in ("README.md", "README.zh-CN.md"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            self.assertIn(f"version-v{version}-", text)
            self.assertIn(f"**v{version}**", text)
        self.assertRegex(package, rf'"version"\s*:\s*"{re.escape(version)}"')
        self.assertRegex(package_lock, rf'"version"\s*:\s*"{re.escape(version)}"')

    def test_embedded_chinese_readme_matches_standalone_version(self):
        combined = (ROOT / "README.md").read_text(encoding="utf-8").strip()
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8").strip()
        start = combined.rfind("# 工业设计作品集 Skill")
        self.assertNotEqual(-1, start)
        combined_body = combined[combined.index("</div>", start) + len("</div>") :].strip()
        standalone_body = chinese[chinese.index("</div>") + len("</div>") :].strip()
        self.assertEqual(standalone_body, combined_body)


if __name__ == "__main__":
    unittest.main()
