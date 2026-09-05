#!/usr/bin/env python3
"""Check unreleased regional draft routes and their publication boundary."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ("/", "/about/", "/projects/", "/contact/")
FAILURES: list[str] = []


def fail(message: str) -> None:
    FAILURES.append(message)


def main() -> int:
    builder = (ROOT / "scripts/build-locale-drafts.py").read_text(encoding="utf-8")
    if "ROOT / 'es'" in builder or 'ROOT / "es"' in builder:
        fail("builder must not use the Spain Spanish tree as an input")
    if "source_path = ROOT / rel" not in builder:
        fail("builder must open canonical en-US paths for both pairs")
    for name in ("index.html", "about-index.html", "projects-index.html", "contact-index.html"):
        if not (ROOT / "i18n/pilot/es-mx/reviewed" / name).exists():
            fail(f"missing reviewed es-MX source artifact: {name}")
    manifest = json.loads((ROOT / "i18n/pilot/regional-drafts-manifest.json").read_text(encoding="utf-8"))
    for locale, expected_lang, label in (("en-gb", "en-GB", "English (UK) · Draft"), ("es-mx", "es-MX", "Español (México) · Borrador")):
        entry = manifest["locales"][locale]
        if entry["status"] != "ai-reviewed-draft":
            fail(f"{locale}: status is not AI-reviewed draft")
        for route in ROUTES:
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
            if locale == "es-mx" and 'fill="#006847"' not in text:
                fail(f"{path.relative_to(ROOT)}: missing Mexico flag")
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
