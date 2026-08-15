import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "showcase" / "modular-desk-lamp"
INPUT = CASE / "input"


class ShowcaseEvidenceChainTests(unittest.TestCase):
    def test_public_input_chain_is_complete(self):
        required = (
            INPUT / "brief.md",
            INPUT / "asset-inventory.json",
            INPUT / "reproduction-prompt.md",
            INPUT / "gating-questions.md",
            CASE / "input-to-output-trace.md",
        )
        for path in required:
            self.assertTrue(path.is_file(), str(path.relative_to(ROOT)))

    def test_created_assets_exist_and_remain_e0(self):
        inventory = json.loads((INPUT / "asset-inventory.json").read_text(encoding="utf-8"))
        self.assertEqual("fictional_demonstration", inventory["case_type"])
        self.assertEqual(1, len(inventory["intake_assets"]))
        self.assertGreaterEqual(len(inventory["missing_evidence"]), 6)
        for asset in inventory["assets_created_after_story_lock"]:
            self.assertEqual("E0", asset["evidence_level"])
            self.assertTrue((INPUT / asset["file"]).resolve().is_file(), asset["file"])

    def test_disclosures_do_not_claim_a_real_run_or_project(self):
        brief = (INPUT / "brief.md").read_text(encoding="utf-8")
        prompt = (INPUT / "reproduction-prompt.md").read_text(encoding="utf-8")
        questions = (INPUT / "gating-questions.md").read_text(encoding="utf-8")
        trace = (CASE / "input-to-output-trace.md").read_text(encoding="utf-8")
        self.assertIn("FICTIONAL DEMONSTRATION INPUT", brief)
        self.assertIn("not a verbatim transcript", prompt)
        self.assertIn("not presented as a verbatim Agent conversation", questions)
        self.assertIn("sanitized real-project forward test is still required", trace)


if __name__ == "__main__":
    unittest.main()
