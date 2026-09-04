#!/usr/bin/env python3
"""Prove the site validator rejects committed SEO regression mutations.

The fixtures intentionally mutate only metadata or navigation.  Editorial
fields, generated body content, and indexing boundaries are asserted to stay
unchanged so this suite cannot pass by changing the content contract itself.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "seo"
FIXTURES = FIXTURE_ROOT / "regressions.json"
GENERATED_FIXTURE = FIXTURE_ROOT / "generated"
HEAT_FIXTURE = GENERATED_FIXTURE / "heat-guides"

sys.path.insert(0, str(ROOT / "scripts"))
validator_spec = importlib.util.spec_from_file_location(
    "validate_site", ROOT / "scripts" / "validate-site.py"
)
if validator_spec is None or validator_spec.loader is None:
    raise RuntimeError("could not load scripts/validate-site.py")
validator = importlib.util.module_from_spec(validator_spec)
validator_spec.loader.exec_module(validator)


def findings_text(findings: list) -> str:
    return "\n".join(f"{finding.page}: {finding.msg}" for finding in findings)


def page_for_route(pages: list[dict], route: str) -> dict:
    return next(page for page in pages if page.get("route") == route)


def parse_html(raw: str):
    parser = validator.TagCounter()
    parser.feed(raw)
    return parser


def mutate_meta(raw: str, field: str, value: str | None) -> str:
    name_or_property, key = field.split(":", 1)
    attribute = "property" if key.startswith("og:") else "name"
    pattern = re.compile(
        rf'<meta\b(?=[^>]*\b{attribute}=["\']{re.escape(key)}["\'])[^>]*>',
        re.IGNORECASE,
    )
    if value is None:
        mutated, count = pattern.subn("", raw, count=1)
    else:
        replacement = (
            f'<meta {attribute}="{key}" content="{value}">'
        )
        mutated, count = pattern.subn(replacement, raw, count=1)
    if count != 1:
        raise AssertionError(f"fixture metadata tag not found: {field}")
    return mutated


def mutate_navigation(raw: str, key: str, value: str) -> str:
    pattern = re.compile(
        rf'<link\b(?=[^>]*\brel=["\'][^"\']*\b{key}\b[^"\']*["\'])[^>]*>',
        re.IGNORECASE,
    )
    replacement = f'<link href="{value}" rel="{key}">'
    mutated, count = pattern.subn(replacement, raw, count=1)
    if count:
        return mutated
    return raw.replace("</head>", f'  {replacement}\n</head>', 1)


class SEOFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture_data = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.source_pages, source_findings = validator.load_source_manifest()
        if source_findings:
            raise AssertionError(findings_text(source_findings))
        cls.pages_by_route = {
            page["route"]: page for page in cls.source_pages
        }

    def assert_rejected(self, findings: list, expected: str) -> None:
        self.assertTrue(findings, "mutation unexpectedly passed")
        self.assertIn(expected, findings_text(findings))

    def assert_source_seo_mutation(
        self,
        mutation: dict,
        expected: str,
    ) -> None:
        original = page_for_route(self.source_pages, mutation["route"])
        mutated = copy.deepcopy(original)
        if "value" in mutation:
            mutated[mutation["field"]] = mutation["value"]
        else:
            mutated.pop(mutation["field"], None)
        self.assertEqual(
            original.get("meta:robots"),
            mutated.get("meta:robots"),
            "SEO fixture changed the source indexing boundary",
        )
        self.assertEqual(
            {key: value for key, value in original.items() if not key.startswith("meta:")},
            {key: value for key, value in mutated.items() if not key.startswith("meta:")},
            "SEO fixture changed source editorial or routing fields",
        )
        findings = validator.validate_source_seo_contract(
            [
                mutated if page is original else page
                for page in self.source_pages
            ]
        )
        self.assert_rejected(findings, expected)

    def test_retired_social_image_rejected_in_source(self) -> None:
        mutation = self.fixture_data["retired_social_image"]
        self.assert_source_seo_mutation(
            mutation,
            "indexable source page uses retired social image",
        )

    def test_mismatched_image_dimensions_rejected_in_source(self) -> None:
        mutation = self.fixture_data["image_contract"][0]
        self.assert_source_seo_mutation(
            mutation,
            "social image dimensions",
        )

    def test_mismatched_image_type_rejected_in_source(self) -> None:
        mutation = self.fixture_data["image_contract"][1]
        self.assert_source_seo_mutation(
            mutation,
            "social image type",
        )

    def test_missing_article_metadata_rejected_in_source(self) -> None:
        mutation = self.fixture_data["missing_article_metadata"]
        self.assert_source_seo_mutation(
            mutation,
            "article source page is missing article:published_time",
        )

    def test_same_as_drift_rejected_in_shared_head_source(self) -> None:
        mutation = self.fixture_data["organization_same_as_drift"]
        original_raw = validator.HEAD_PARTIAL.read_text(encoding="utf-8")
        mutated_raw = original_raw.replace(mutation["from"], mutation["to"], 1)
        self.assertNotEqual(original_raw, mutated_raw)
        self.assertEqual(
            mutated_raw.replace(mutation["to"], mutation["from"], 1),
            original_raw,
            "head fixture mutation changed editorial content",
        )
        findings = validator.validate_organization_nodes(
            "tests/fixtures/seo/head.html.fixture",
            parse_html(mutated_raw),
        )
        self.assert_rejected(findings, "sameAs links do not match")

    def test_generated_metadata_baseline_is_valid(self) -> None:
        root_page = self.pages_by_route["/"]
        article_page = self.pages_by_route["/writings/first-diagram-is-a-liar/"]
        for fixture_name, manifest_page in (
            ("index.html.fixture", root_page),
            ("article.html.fixture", article_page),
        ):
            path = GENERATED_FIXTURE / fixture_name
            raw = path.read_text(encoding="utf-8")
            parser = parse_html(raw)
            self.assertFalse(
                validator.validate_generated_seo(path, parser, manifest_page),
                f"valid generated fixture failed: {fixture_name}",
            )
            self.assertIn("Fixture", raw)
            self.assertIn("index, follow", raw)

    def test_retired_social_image_rejected_in_generated_metadata(self) -> None:
        mutation = self.fixture_data["retired_social_image"]
        path = GENERATED_FIXTURE / "index.html.fixture"
        original_raw = path.read_text(encoding="utf-8")
        for field in ("meta:og:image", "meta:twitter:image"):
            with self.subTest(field=field):
                mutated_raw = mutate_meta(
                    original_raw,
                    field,
                    mutation["value"],
                )
                self.assertEqual(
                    original_raw.split("<body>", 1)[1],
                    mutated_raw.split("<body>", 1)[1],
                    "generated fixture mutation changed editorial content",
                )
                self.assertIn('name="robots" content="index, follow"', mutated_raw)
                findings = validator.validate_generated_seo(
                    path,
                    parse_html(mutated_raw),
                    self.pages_by_route["/"],
                )
                self.assert_rejected(findings, f"uses retired social image: {field}")

    def test_mismatched_image_metadata_rejected_in_generated_metadata(self) -> None:
        path = GENERATED_FIXTURE / "index.html.fixture"
        original_raw = path.read_text(encoding="utf-8")
        for mutation in self.fixture_data["image_contract"]:
            with self.subTest(mutation=mutation["id"]):
                mutated_raw = mutate_meta(
                    original_raw,
                    mutation["field"],
                    mutation["value"],
                )
                self.assertEqual(
                    original_raw.split("<body>", 1)[1],
                    mutated_raw.split("<body>", 1)[1],
                )
                findings = validator.validate_generated_seo(
                    path,
                    parse_html(mutated_raw),
                    self.pages_by_route["/"],
                )
                self.assert_rejected(findings, "social image")

    def test_missing_article_metadata_rejected_in_generated_metadata(self) -> None:
        mutation = self.fixture_data["missing_article_metadata"]
        path = GENERATED_FIXTURE / "article.html.fixture"
        original_raw = path.read_text(encoding="utf-8")
        mutated_raw = mutate_meta(original_raw, mutation["field"], None)
        self.assertEqual(
            original_raw.split("<body>", 1)[1],
            mutated_raw.split("<body>", 1)[1],
        )
        self.assertIn('name="robots" content="index, follow"', mutated_raw)
        findings = validator.validate_generated_seo(
            path,
            parse_html(mutated_raw),
            self.pages_by_route[mutation["route"]],
        )
        self.assert_rejected(findings, "article generated page is missing")

    def test_same_as_drift_rejected_in_generated_metadata(self) -> None:
        mutation = self.fixture_data["organization_same_as_drift"]
        path = GENERATED_FIXTURE / "index.html.fixture"
        original_raw = path.read_text(encoding="utf-8")
        mutated_raw = original_raw.replace(mutation["from"], mutation["to"], 1)
        findings = validator.validate_generated_seo(
            path,
            parse_html(mutated_raw),
            self.pages_by_route["/"],
        )
        self.assert_rejected(findings, "sameAs links do not match")
        self.assertEqual(
            original_raw.split("<body>", 1)[1],
            mutated_raw.split("<body>", 1)[1],
        )

    def test_each_heat_guide_edge_rejected_in_source(self) -> None:
        for mutation in self.fixture_data["heat_guide_edges"]:
            with self.subTest(route=mutation["route"], key=mutation["key"]):
                mutated_pages = copy.deepcopy(self.source_pages)
                page = page_for_route(mutated_pages, mutation["route"])
                page[mutation["key"]] = mutation["value"]
                original = page_for_route(self.source_pages, mutation["route"])
                self.assertEqual(
                    original.get("meta:robots"),
                    page.get("meta:robots"),
                )
                findings = validator.validate_heat_guide_chain(mutated_pages)
                self.assert_rejected(findings, f"heat-guide {mutation['key']} link is")

    def test_each_heat_guide_edge_rejected_in_generated_metadata(self) -> None:
        original_pages = []
        for route in validator.HEAT_GUIDE_ROUTES:
            page = copy.deepcopy(page_for_route(self.source_pages, route))
            page["path"] = page["path"].replace(
                "index.html", "index.html.fixture"
            )
            original_pages.append(page)
        with tempfile.TemporaryDirectory(prefix="seo-fixtures-") as temp:
            generated_root = Path(temp) / "heat-guides"
            shutil.copytree(HEAT_FIXTURE, generated_root)
            for mutation in self.fixture_data["heat_guide_edges"]:
                with self.subTest(route=mutation["route"], key=mutation["key"]):
                    mutated_root = Path(temp) / (
                        f"{validator.HEAT_GUIDE_ROUTES.index(mutation['route'])}-"
                        f"{mutation['key']}"
                    )
                    shutil.copytree(generated_root, mutated_root)
                    page = page_for_route(original_pages, mutation["route"])
                    fixture_path = mutated_root / page["path"]
                    original_raw = fixture_path.read_text(encoding="utf-8")
                    mutated_raw = mutate_navigation(
                        original_raw,
                        mutation["key"],
                        mutation["value"],
                    )
                    fixture_path.write_text(mutated_raw, encoding="utf-8")
                    self.assertEqual(
                        original_raw.split("<body>", 1)[1],
                        mutated_raw.split("<body>", 1)[1],
                    )
                    findings = validator.validate_heat_guide_chain(
                        original_pages,
                        generated_root=mutated_root,
                    )
                    self.assert_rejected(
                        findings,
                        f"generated heat-guide {mutation['key']} links",
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)