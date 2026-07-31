import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


class ManifestSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(
            (ROOT / "schemas" / "portfolio-manifest.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def test_example_and_showcase_manifests_conform(self):
        manifests = [
            ROOT / "assets" / "portfolio_manifest.example.json",
            ROOT / "showcase" / "modular-desk-lamp" / "portfolio_manifest.json",
        ]
        for path in manifests:
            with self.subTest(path=path):
                data = json.loads(path.read_text(encoding="utf-8"))
                errors = sorted(self.validator.iter_errors(data), key=lambda error: list(error.path))
                self.assertEqual([], errors, "\n".join(error.message for error in errors))


if __name__ == "__main__":
    unittest.main()
