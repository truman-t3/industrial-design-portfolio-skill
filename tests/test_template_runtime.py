import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TemplateRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = (ROOT / "assets" / "portfolio-template.html").read_text(encoding="utf-8")

    def test_lightweight_runtime_contract_is_present(self):
        required = (
            "data-src",
            "slideMarkup",
            "mountSlide",
            "unmountSlide",
            "IntersectionObserver",
            "params.get('page')",
            "params.get('render')==='all'",
            "beforeprint",
            "afterprint",
            "content-visibility:auto",
            "contain-intrinsic-size:100vw 100svh",
        )
        for signature in required:
            with self.subTest(signature=signature):
                self.assertIn(signature, self.template)

    def test_expensive_default_effects_are_absent(self):
        self.assertNotIn("backdrop-filter", self.template)
        self.assertNotIn("scroll-behavior:smooth", self.template)
        self.assertNotIn("behavior:'smooth'", self.template)


if __name__ == "__main__":
    unittest.main()
