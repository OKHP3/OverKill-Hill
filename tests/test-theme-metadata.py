#!/usr/bin/env python3
"""Regression tests for brand theme metadata in published page heads."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
validator_spec = importlib.util.spec_from_file_location(
    "validate_site", ROOT / "scripts" / "validate-site.py"
)
assert validator_spec and validator_spec.loader
validator = importlib.util.module_from_spec(validator_spec)
validator_spec.loader.exec_module(validator)


def parse_html(raw: str):
    parser = validator.TagCounter()
    parser.feed(raw)
    return parser


def brand_page(brand: str, light: str, dark: str, color_scheme: str = "dark light") -> str:
    return f"""<!doctype html>
<html><head>
  <meta name="theme-color" media="(prefers-color-scheme: light)" content="{light}">
  <meta name="theme-color" media="(prefers-color-scheme: dark)" content="{dark}">
  <meta name="color-scheme" content="{color_scheme}">
</head><body class="{brand}"></body></html>"""


class BrandThemeMetadataTests(unittest.TestCase):
    def test_valid_brand_metadata_passes(self) -> None:
        for brand, light, dark in (
            ("glee-main", "#d35b2d", "#1e1b19"),
            ("askjamie-main", "#f5efe1", "#2c5e6f"),
        ):
            with self.subTest(brand=brand):
                self.assertEqual(
                    validator.validate_brand_theme_metadata(
                        f"{brand}/index.html",
                        parse_html(brand_page(brand, light, dark)),
                    ),
                    [],
                )

    def test_missing_media_variant_names_page_and_media(self) -> None:
        raw = brand_page("glee-main", "#d35b2d", "#1e1b19").replace(
            'media="(prefers-color-scheme: dark)"', "", 1
        )
        findings = validator.validate_brand_theme_metadata(
            "projects/index.html", parse_html(raw)
        )
        self.assertTrue(
            any(
                "projects/index.html" in finding.page
                and "missing theme-color metadata" in finding.msg
                and "(prefers-color-scheme: dark)" in finding.msg
                for finding in findings
            )
        )

    def test_wrong_color_and_color_scheme_report_values(self) -> None:
        raw = brand_page("askjamie-main", "#wrong", "#2c5e6f", "light dark")
        findings = validator.validate_brand_theme_metadata(
            "index.html", parse_html(raw)
        )
        messages = "\n".join(finding.msg for finding in findings)
        self.assertIn("is '#wrong'; expected '#f5efe1'", messages)
        self.assertIn("is 'light dark'; expected exactly 'dark light'", messages)

    def test_missing_color_scheme_reports_expected_value(self) -> None:
        raw = brand_page("glee-main", "#d35b2d", "#1e1b19").replace(
            '<meta name="color-scheme" content="dark light">', "", 1
        )
        findings = validator.validate_brand_theme_metadata(
            "glee/index.html", parse_html(raw)
        )
        messages = "\n".join(finding.msg for finding in findings)
        self.assertIn("missing color-scheme metadata", messages)
        self.assertIn("expected 'dark light'", messages)

    def test_duplicate_or_unexpected_theme_color_is_rejected(self) -> None:
        raw = brand_page("glee-main", "#d35b2d", "#1e1b19").replace(
            "</head>",
            '<meta name="theme-color" content="#d35b2d"></head>',
            1,
        )
        findings = validator.validate_brand_theme_metadata(
            "glee/index.html", parse_html(raw)
        )
        messages = "\n".join(finding.msg for finding in findings)
        self.assertIn("unexpected theme-color metadata", messages)


if __name__ == "__main__":
    unittest.main()