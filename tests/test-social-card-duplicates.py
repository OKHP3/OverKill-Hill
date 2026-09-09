import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-site.py"
SPEC = importlib.util.spec_from_file_location("validate_site", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SocialCardDuplicateTests(unittest.TestCase):
    def test_conflicting_duplicate_reports_metadata_key_and_page(self):
        findings = MODULE.validate_duplicate_social_card_metadata(
            "fr/projects/index.html",
            {
                "og:image": ["https://example.test/old.png", "https://example.test/new.png"],
                "twitter:image": ["https://example.test/card.png"],
            },
        )

        self.assertEqual(1, len(findings))
        self.assertEqual("fr/projects/index.html", findings[0].page)
        self.assertIn("meta:og:image", findings[0].msg)
        self.assertIn("old.png", findings[0].msg)
        self.assertIn("new.png", findings[0].msg)

    def test_identical_duplicate_is_not_conflicting(self):
        findings = MODULE.validate_duplicate_social_card_metadata(
            "fr/projects/index.html",
            {
                "og:image": ["https://example.test/card.png"] * 2,
                "twitter:image:alt": ["Card description"] * 2,
            },
        )

        self.assertEqual([], findings)

    def test_noindex_locale_page_does_not_enter_social_card_contract(self):
        parser = MODULE.TagCounter()
        parser.feed(
            '<meta property="og:image" content="https://example.test/old.png">'
            '<meta property="og:image" content="https://example.test/new.png">'
        )

        findings = MODULE.validate_generated_seo(
            ROOT / "de/projects/index.html",
            parser,
            None,
            {"indexable": False},
        )

        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()