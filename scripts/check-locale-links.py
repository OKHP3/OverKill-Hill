#!/usr/bin/env python3
"""Validate the published contract for a locale pilot.

The unpublished pilot is checked as a scaffold: its source routes must exist,
but no target pages or target sitemap/search-index entries may be present.
Once the manifest is no longer marked ``unpublished-scaffold``, every route is
checked for page metadata, reciprocal hreflang links, sitemap coverage, and
locale search-index coverage.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SITE_ORIGIN = "https://overkillhill.com"
DEFAULT_MANIFEST = ROOT / "i18n" / "pilot" / "manifest.json"
DEFAULT_SITEMAP = ROOT / "sitemap.xml"
SEARCH_INDEX_BUILDER = ROOT / "scripts" / "build-search-index.py"


class HeadMetadata(HTMLParser):
    """Collect only the head metadata needed by this release check."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.canonical = ""
        self.alternates: dict[str, set[str]] = {}
        self._in_html = False

    def handle_starttag(self, tag: str, attrs_list) -> None:
        attrs = {key.lower(): value or "" for key, value in attrs_list}
        tag = tag.lower()
        if tag == "html":
            self.lang = attrs.get("lang", "").strip()
            self._in_html = True
        elif tag == "link":
            rel = set(attrs.get("rel", "").lower().split())
            href = attrs.get("href", "").strip()
            if "canonical" in rel:
                self.canonical = href
            if "alternate" in rel and attrs.get("hreflang", "").strip() and href:
                self.alternates.setdefault(attrs["hreflang"].strip().lower(), set()).add(href)


def route_file(root: Path, route: str) -> Path:
    """Map a slash-terminated public route to its static HTML file."""
    path = root / route.lstrip("/")
    if route == "/":
        return root / "index.html"
    if route.endswith("/"):
        return path / "index.html"
    return path


def route_url(route: str) -> str:
    return f"{SITE_ORIGIN}{route}"


def read_metadata(path: Path) -> HeadMetadata:
    parser = HeadMetadata()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def fail(findings: list[str], message: str) -> None:
    findings.append(message)


def load_manifest(path: Path) -> dict:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read manifest {path}: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ValueError("manifest root must be a JSON object")
    return manifest


def sitemap_urls(path: Path) -> set[str]:
    try:
        root = ElementTree.fromstring(path.read_text(encoding="utf-8"))
    except (OSError, ElementTree.ParseError) as exc:
        raise ValueError(f"cannot read sitemap {path}: {exc}") from exc
    return {
        element.text.strip()
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] == "loc" and element.text and element.text.strip()
    }


def check_search_index(
    index_path: Path, target_routes: set[str], locale: str, findings: list[str]
) -> None:
    if not index_path.is_file():
        fail(findings, f"locale search index is missing: {index_path}")
        return
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(findings, f"locale search index is not valid JSON: {exc}")
        return
    if payload.get("locale") != locale:
        fail(findings, f"locale search index has locale {payload.get('locale')!r}, expected {locale!r}")
    entries = payload.get("entries")
    if not isinstance(entries, list):
        fail(findings, "locale search index entries must be a list")
        return
    urls = [entry.get("url") for entry in entries if isinstance(entry, dict)]
    missing = sorted(target_routes - set(urls))
    if missing:
        fail(findings, f"locale search index is missing routes: {', '.join(missing)}")
    if len(urls) != len(set(urls)):
        fail(findings, "locale search index contains duplicate URLs")
    if payload.get("count") != len(entries):
        fail(findings, f"locale search index count is {payload.get('count')!r}, expected {len(entries)}")


def run_index_freshness_check(index_path: Path, locale: str, findings: list[str]) -> None:
    expected = ROOT / "assets" / "data" / f"search-index.{locale}.json"
    if index_path.resolve() != expected.resolve():
        return
    result = subprocess.run(
        [sys.executable, str(SEARCH_INDEX_BUILDER), f"--locale={locale}", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip().splitlines()
        fail(findings, f"locale search index is stale: {detail[-1] if detail else 'build check failed'}")


def validate(
    manifest_path: Path = DEFAULT_MANIFEST,
    sitemap_path: Path = DEFAULT_SITEMAP,
    index_path: Path | None = None,
    root: Path = ROOT,
) -> list[str]:
    manifest = load_manifest(manifest_path)
    locale = manifest.get("target_locale")
    pages = manifest.get("pages")
    findings: list[str] = []
    if not isinstance(locale, str) or not locale:
        fail(findings, "manifest target_locale must be a non-empty string")
        return findings
    if not isinstance(pages, list) or not pages:
        fail(findings, "manifest pages must be a non-empty list")
        return findings
    index_path = index_path or root / "assets" / "data" / f"search-index.{locale}.json"
    try:
        urls = sitemap_urls(sitemap_path)
    except ValueError as exc:
        fail(findings, str(exc))
        urls = set()

    source_routes: set[str] = set()
    target_routes: set[str] = set()
    for page in pages:
        if not isinstance(page, dict):
            fail(findings, "manifest contains a non-object page entry")
            continue
        source_route = page.get("source_route")
        target_route = page.get("target_route")
        source_path = page.get("source_path")
        target_path = page.get("target_path")
        if not all(isinstance(value, str) and value for value in (source_route, target_route, source_path, target_path)):
            fail(findings, f"manifest page has incomplete route/path fields: {page!r}")
            continue
        source_routes.add(source_route)
        target_routes.add(target_route)
        source_file = root / source_path
        target_file = root / target_path
        if not source_file.is_file():
            fail(findings, f"English source page is missing: {source_path}")
        if not target_route.startswith(f"/{locale}/"):
            fail(findings, f"target route is outside /{locale}/: {target_route}")
        if manifest.get("status") == "unpublished-scaffold":
            if target_file.exists():
                fail(findings, f"unpublished scaffold contains target page: {target_path}")
            if route_url(target_route) in urls:
                fail(findings, f"unpublished target route is in sitemap.xml: {target_route}")
            continue
        if not target_file.is_file():
            fail(findings, f"locale page is missing: {target_path}")
            continue
        source_meta = read_metadata(source_file)
        target_meta = read_metadata(target_file)
        expected_source = route_url(source_route)
        expected_target = route_url(target_route)
        if source_meta.canonical != expected_source:
            fail(findings, f"{source_path} canonical is {source_meta.canonical!r}, expected {expected_source!r}")
        if target_meta.canonical != expected_target:
            fail(findings, f"{target_path} canonical is {target_meta.canonical!r}, expected {expected_target!r}")
        expected_source_links = {
            "en": expected_source,
            "x-default": expected_source,
            locale: expected_target,
        }
        expected_target_links = {
            locale: expected_target,
            "en": expected_source,
            "x-default": expected_source,
        }
        for label, meta, expected in (
            (source_path, source_meta, expected_source_links),
            (target_path, target_meta, expected_target_links),
        ):
            for hreflang, href in expected.items():
                if href not in meta.alternates.get(hreflang, set()):
                    fail(findings, f"{label} is missing hreflang={hreflang!r} href={href!r}")
        if target_meta.lang.lower() != locale.lower():
            fail(findings, f"{target_path} html lang is {target_meta.lang!r}, expected {locale!r}")
        if source_meta.lang.lower() not in ("", "en"):
            fail(findings, f"{source_path} html lang is {source_meta.lang!r}, expected 'en'")

    if manifest.get("status") == "unpublished-scaffold":
        check_search_index(index_path, set(), locale, findings)
    else:
        for route in sorted(source_routes | target_routes):
            if route_url(route) not in urls:
                fail(findings, f"route is missing from sitemap.xml: {route}")
        check_search_index(index_path, target_routes, locale, findings)
        run_index_freshness_check(index_path, locale, findings)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--sitemap", type=Path, default=DEFAULT_SITEMAP)
    parser.add_argument("--search-index", type=Path)
    args = parser.parse_args(argv)
    findings = validate(args.manifest, args.sitemap, args.search_index)
    if findings:
        print("Locale link check failed:", file=sys.stderr)
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        return 1
    print(f"Locale link check passed: {args.manifest} ({load_manifest(args.manifest).get('target_locale')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())