#!/usr/bin/env python3
"""Check unreleased regional draft routes and their publication boundary."""
from __future__ import annotations

import json
import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ("/", "/about/", "/projects/", "/contact/")
FAILURES: list[str] = []
CSP_META_RE = re.compile(
    rb'<meta\b(?=[^>]*\bhttp-equiv=["\']Content-Security-Policy["\'])[^>]*>',
    re.I,
)


def fail(message: str) -> None:
    FAILURES.append(message)


def canonical_text_hash(path: Path) -> str:
    return hashlib.sha256(normalized_translation_source(path.read_bytes())).hexdigest()


def normalized_translation_source(content: bytes) -> bytes:
    return CSP_META_RE.sub(b"", content.replace(b"\r\n", b"\n"))


def release_source_hash(source_hashes: dict, route: str, source_rel: str) -> str:
    revision = source_hashes["source_revision"].removeprefix("git:")
    release_content = subprocess.run(
        ["git", "show", f"{revision}:{source_rel}"],
        check=True,
        capture_output=True,
    ).stdout
    recorded_raw_hash = hashlib.sha256(release_content.replace(b"\r\n", b"\n")).hexdigest()
    if recorded_raw_hash != source_hashes["routes"].get(route):
        raise ValueError(f"recorded release source does not match its hash for {route}")
    return hashlib.sha256(normalized_translation_source(release_content)).hexdigest()


def has_meta_content(text: str, property_name: str, content: str) -> bool:
    return bool(
        re.search(
            rf'<meta\b(?=[^>]*\bproperty=["\']{re.escape(property_name)}["\'])(?=[^>]*\bcontent=["\']{re.escape(content)}["\'])[^>]*>',
            text,
            re.I,
        )
    )


def has_canonical_url(text: str, url: str) -> bool:
    return bool(
        re.search(
            rf'<link\b(?=[^>]*\brel=["\'][^"\']*\bcanonical\b[^"\']*["\'])(?=[^>]*\bhref=["\']{re.escape(url)}["\'])[^>]*>',
            text,
            re.I,
        )
    )


def main() -> int:
    builder = (ROOT / "scripts/build-locale-drafts.py").read_text(encoding="utf-8")
    if "ROOT / 'es'" in builder or 'ROOT / "es"' in builder:
        fail("builder must not use the Spain Spanish tree as an input")
    if "source_path = ROOT / rel" not in builder:
        fail("builder must open canonical en-US paths for both pairs")
    source_hashes = json.loads((ROOT / "i18n/pilot/source-hashes-release-0ee.json").read_text(encoding="utf-8"))
    for name in ("index.html", "about-index.html", "projects-index.html", "contact-index.html"):
        if not (ROOT / "i18n/pilot/es-mx/reviewed" / name).exists():
            fail(f"missing reviewed es-MX source artifact: {name}")
    manifest = json.loads((ROOT / "i18n/pilot/regional-drafts-manifest.json").read_text(encoding="utf-8"))
    for locale, expected_lang, label in (("en-gb", "en-GB", "English (UK) · Draft"), ("es-mx", "es-MX", "Español (México) · Borrador")):
        entry = manifest["locales"][locale]
        if entry["status"] != "ai-reviewed-draft":
            fail(f"{locale}: status is not AI-reviewed draft")
        for route in ROUTES:
            source_rel = "index.html" if route == "/" else route.strip("/") + "/index.html"
            source_path = ROOT / source_rel
            if canonical_text_hash(source_path) != release_source_hash(source_hashes, route, source_rel):
                fail(f"{route}: canonical source is stale relative to the recorded release revision")
            path = ROOT / locale / ("index.html" if route == "/" else route.strip("/") + "/index.html")
            if not path.exists():
                fail(f"{locale}: missing {path.relative_to(ROOT)}")
                continue
            text = path.read_text(encoding="utf-8")
            if f'<html lang="{expected_lang}">' not in text:
                fail(f"{path.relative_to(ROOT)}: wrong html lang")
            robots = re.search(r'<meta[^>]+>', text, re.I)
            robot_tags = re.findall(r'<meta[^>]+>', text, re.I)
            if not any(re.search(r'name=["\']robots["\']', tag, re.I) and re.search(r'content=["\']noindex, follow', tag, re.I) for tag in robot_tags):
                fail(f"{path.relative_to(ROOT)}: missing noindex")
            if label not in text:
                fail(f"{path.relative_to(ROOT)}: missing visible draft label")
            if '<link' in text and 'rel="alternate"' in text[: text.find("</head>")]:
                fail(f"{path.relative_to(ROOT)}: draft head exposes public alternate links")
            if locale == "en-gb" and 'stroke="#CE1124"' not in text:
                fail(f"{path.relative_to(ROOT)}: missing St George flag")
            if locale == "en-gb" and 'stroke="#CE1124"' in text and 'stroke="#CE1124" stroke-width="4"' not in text:
                fail(f"{path.relative_to(ROOT)}: St George flag is not the upright cross contract")
            if locale == "en-gb":
                target_url = f"https://overkillhill.com/en-gb{route}"
                if not has_canonical_url(text, target_url):
                    fail(f"{path.relative_to(ROOT)}: incorrect canonical URL")
                if not has_meta_content(text, "og:url", target_url):
                    fail(f"{path.relative_to(ROOT)}: incorrect Open Graph URL")
                if not has_meta_content(text, "og:locale", "en_GB"):
                    fail(f"{path.relative_to(ROOT)}: incorrect regional Open Graph locale")
                if 'https://overkillhill.com/en-gb/en-gb/' in text or '/en-gb/assets/' in text:
                    fail(f"{path.relative_to(ROOT)}: has globally rewritten non-page URLs")
                if '"@type": "Organisation"' in text:
                    fail(f"{path.relative_to(ROOT)}: rewrites the Schema.org Organization type")
                for sibling_route in ROUTES:
                    expected_href = f'href="/en-gb{sibling_route}"'
                    if expected_href not in text:
                        fail(f"{path.relative_to(ROOT)}: missing localized navigation link {expected_href}")
            if locale == "es-mx" and 'fill="#006847"' not in text:
                fail(f"{path.relative_to(ROOT)}: missing Mexico flag")
            if locale == "es-mx" and 'Mexico coat of arms' not in text:
                fail(f"{path.relative_to(ROOT)}: Mexico flag lacks its coat of arms")
            if locale == "es-mx" and 'Español (México) · Borrador</span>' not in text:
                fail(f"{path.relative_to(ROOT)}: missing visible Mexico draft label")
            if locale == "es-mx" and 'href="https://fonts.googleapis.com' not in text:
                fail(f"{path.relative_to(ROOT)}: missing canonical heading-font resource")
            if locale == "es-mx" and 'class="site-specials site-specials--okh"' not in text:
                fail(f"{path.relative_to(ROOT)}: missing localized current forge notice")
            if locale == "es-mx" and 'data-banner-release="v0.5"' not in text:
                fail(f"{path.relative_to(ROOT)}: localized forge notice lacks its release marker")
            if locale == "es-mx" and not has_meta_content(text, "og:locale", "es_MX"):
                fail(f"{path.relative_to(ROOT)}: incorrect regional Open Graph locale")
            source_text = source_path.read_text(encoding="utf-8")
            for element in ("h1", "h2", "h3", "article", "figure", "img"):
                if len(re.findall(rf"<{element}\b", source_text, re.I)) != len(re.findall(rf"<{element}\b", text, re.I)):
                    fail(f"{path.relative_to(ROOT)}: {element} coverage differs from canonical source")
    for index in ("search-index.en-gb.json", "search-index.es-mx.json"):
        payload = json.loads((ROOT / "assets/data" / index).read_text(encoding="utf-8"))
        if payload.get("count") != 0 or payload.get("entries") != []:
            fail(f"{index}: draft routes must have zero public search entries")
    if FAILURES:
        print("Regional draft check failed:")
        print("\n".join(f"  - {item}" for item in FAILURES))
        return 1
    print("Regional draft check passed: en-gb and es-mx, four routes each, noindex, no public alternates, zero search entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
