#!/usr/bin/env python3
"""Emit and validate a static site's sitemap route inventory.

Read-only. Usage:
  python3 inventory-routes.py --root . --sitemap sitemap.xml [--origin https://example.com]
Exit 0 with JSON on stdout; exit 1 for invalid inventory or missing targets,
and exit 2 for invalid arguments.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

def target(root: Path, route: str) -> Path:
    if route == "/":
        return root / "index.html"
    path = root / route.lstrip("/")
    return path / "index.html" if route.endswith("/") else path

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--sitemap", type=Path, required=True)
    ap.add_argument("--origin")
    args = ap.parse_args()
    root = args.root.resolve()
    sitemap = args.sitemap if args.sitemap.is_absolute() else root / args.sitemap
    if not sitemap.is_file():
        print(f"ERROR: sitemap not found: {sitemap}", file=sys.stderr); return 1
    try:
        urls = [el.text.strip() for el in ET.parse(sitemap).iter() if el.tag.rsplit("}", 1)[-1] == "loc" and el.text and el.text.strip()]
    except (ET.ParseError, OSError) as exc:
        print(f"ERROR: cannot parse sitemap: {exc}", file=sys.stderr); return 1
    errors, routes, seen = [], [], set()
    expected_origin = args.origin.rstrip("/") if args.origin else None
    for url in urls:
        parsed = urlparse(url)
        route = parsed.path or "/"
        if not parsed.scheme or not parsed.netloc:
            errors.append(f"URL is not absolute: {url}")
        if expected_origin and f"{parsed.scheme}://{parsed.netloc}" != expected_origin:
            errors.append(f"non-production origin: {url}")
        if parsed.query or parsed.fragment:
            errors.append(f"query or fragment is not allowed: {url}")
        if route in seen:
            errors.append(f"duplicate route: {route}")
        seen.add(route); routes.append(route)
        if not target(root, route).is_file():
            errors.append(f"route has no local HTML target: {route}")
    if not urls:
        errors.append("sitemap contains no loc entries")
    if errors:
        for error in errors: print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"sitemap": str(sitemap), "count": len(routes), "routes": routes}, indent=2))
    return 0
if __name__ == "__main__":
    sys.exit(main())