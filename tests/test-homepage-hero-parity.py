#!/usr/bin/env python3
"""Keep every localized homepage on the current responsive MurderBird hero."""
from __future__ import annotations

import importlib.util
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build-locale-drafts.py"
SPEC = importlib.util.spec_from_file_location("build_locale_drafts", BUILDER)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

HERO_RE = re.compile(r'<div class="hero-visual">\s*(.*?)\s*</div>', re.S)
LOCALES = ("fr", "de", "es", "es-mx")
EXPECTED_SRCSET = (
    "/assets/img/webp/murderbird-frontal-attack-2026-09-05-512.webp 512w, "
    "/assets/img/webp/murderbird-frontal-attack-2026-09-05-1024.webp 1024w"
)
EXPECTED_SIZES = "(max-width: 900px) 86vw, 42vw"
EXPECTED_SRC = "/assets/img/murderbird-frontal-attack-2026-09-05.png"


class HeroParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sources: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs_list) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if tag == "source":
            self.sources.append(attrs)
        elif tag == "img":
            self.images.append(attrs)


def hero_fragment(page: str) -> str:
    match = HERO_RE.search(page)
    if match is None:
        raise AssertionError("homepage hero visual is missing")
    return match.group(1)


class HomepageHeroParityTests(unittest.TestCase):
    def assert_current_hero(self, page: str, locale: str) -> None:
        fragment = hero_fragment(page)
        self.assertNotIn("sentinel", fragment.lower())
        parser = HeroParser()
        parser.feed(fragment)
        self.assertEqual(1, len(parser.sources))
        self.assertEqual(1, len(parser.images))
        source = parser.sources[0]
        image = parser.images[0]
        self.assertEqual("image/webp", source.get("type"))
        self.assertEqual(EXPECTED_SRCSET, source.get("srcset"))
        self.assertEqual(EXPECTED_SIZES, source.get("sizes"))
        self.assertIn("MurderBird", image.get("alt", ""))
        self.assertNotRegex(image.get("alt", ""), r"sentinel|chouette|búho", msg="alt text names the former identity")
        self.assertEqual(EXPECTED_SRC, image.get("src"))
        self.assertEqual("1254", image.get("width"))
        self.assertEqual("1254", image.get("height"))
        self.assertEqual("eager", image.get("loading"))
        self.assertEqual("high", image.get("fetchpriority"))
        self.assertEqual(EXPECTED_SIZES, image.get("sizes"))

    def test_localized_homepages_match_the_current_hero_asset_contract(self):
        for locale in LOCALES:
            with self.subTest(locale=locale):
                page = (ROOT / locale / "index.html").read_text(encoding="utf-8")
                self.assert_current_hero(page, locale)

    def test_es_mx_regeneration_keeps_the_current_hero(self):
        dictionary, _profile = MODULE.load_pair_contract("es-mx")
        reviewed = (ROOT / "i18n/pilot/es-mx/reviewed/index.html").read_text(encoding="utf-8")
        canonical = (ROOT / "index.html").read_text(encoding="utf-8")
        rendered = MODULE.build_es_mx(reviewed, canonical, "/", dictionary)
        self.assert_current_hero(rendered, "es-mx")

    def test_former_lazy_sentinel_hero_fails_the_contract(self):
        page = (ROOT / "es-mx/index.html").read_text(encoding="utf-8")
        former = hero_fragment(page).replace(
            "/assets/img/murderbird-frontal-attack-2026-09-05.png",
            "/assets/img/over-kill-hill-p3-sentinel-waiting-square-1024.png",
        ).replace('loading="eager"', 'loading="lazy"')
        with self.assertRaises(AssertionError):
            self.assert_current_hero(page.replace(hero_fragment(page), former), "es-mx")


if __name__ == "__main__":
    unittest.main()
