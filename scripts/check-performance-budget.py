#!/usr/bin/env python3
"""Check deterministic first-party asset budgets for representative pages.

This is intentionally a source-budget guard, not a browser timing or Core Web
Vitals check. It counts the published HTML document and selected local assets
reachable from it, including local CSS url() dependencies. External resources,
iframes, dynamically added requests, compression, and cache behavior are out
of scope.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT_ASSET_TAGS = {
    "script": {"src"},
    "img": {"src", "srcset"},
    "source": {"src", "srcset"},
    "audio": {"src"},
    "video": {"src", "poster"},
}
LINK_RELS = {"stylesheet", "icon", "apple-touch-icon", "manifest", "preload", "modulepreload"}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.lower(): value or "" for name, value in attrs}
        if tag == "link":
            rels = set(values.get("rel", "").lower().split())
            if rels & LINK_RELS:
                self.urls.append(values.get("href", ""))
            return
        for attribute in ROOT_ASSET_TAGS.get(tag, set()):
            value = values.get(attribute, "")
            if attribute == "srcset":
                self.urls.extend(candidate.strip().split()[0] for candidate in value.split(",") if candidate.strip())
            elif value:
                self.urls.append(value)


def local_path(value: str, *, root: Path, parent: Path) -> Path | None:
    """Return a safe local file path, ignoring external and data URLs."""
    value = html.unescape(value).strip()
    if not value or value.startswith(("#", "data:", "javascript:")):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    raw_path = unquote(parsed.path)
    if not raw_path:
        return None
    candidate = root / raw_path.lstrip("/") if raw_path.startswith("/") else parent / raw_path
    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve()
    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError as error:
        raise ValueError(f"local asset escapes root: {value}") from error
    return resolved_candidate


def collect_route(root: Path, document: str) -> tuple[list[Path], list[str]]:
    root = root.resolve()
    document_path = (root / document).resolve()
    try:
        document_path.relative_to(root)
    except ValueError as error:
        raise ValueError(f"route document escapes root: {document}") from error
    if not document_path.is_file():
        raise ValueError(f"missing route document: {document}")
    queue = [document_path]
    seen: set[Path] = set()
    missing: list[str] = []
    while queue:
        current = queue.pop()
        if current in seen:
            continue
        seen.add(current)
        text = current.read_text(encoding="utf-8")
        if current.suffix.lower() == ".css":
            urls = [match.group(2) for match in CSS_URL.finditer(text)]
        else:
            parser = AssetParser()
            parser.feed(text)
            urls = parser.urls
        for url in urls:
            asset = local_path(url, root=root, parent=current.parent)
            if asset is None:
                continue
            if not asset.is_file():
                missing.append(asset.relative_to(root).as_posix())
                continue
            if asset.suffix.lower() == ".css":
                queue.append(asset)
            else:
                seen.add(asset)
    return sorted(seen), sorted(set(missing))


def load_config(path: Path) -> dict:
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read budget config {path}: {error}") from error
    if config.get("schema_version") != 1 or not isinstance(config.get("routes"), list) or not config["routes"]:
        raise ValueError("budget config must contain schema_version 1 and at least one route")
    return config


def check(root: Path, config: dict) -> tuple[list[dict], bool]:
    results: list[dict] = []
    passed = True
    for item in config["routes"]:
        if not isinstance(item, dict) or not isinstance(item.get("route"), str) or not isinstance(item.get("document"), str) or not isinstance(item.get("max_bytes"), int):
            raise ValueError("each budget route needs route, document, and integer max_bytes")
        files, missing = collect_route(root, item["document"])
        total = sum(file.stat().st_size for file in files)
        route_pass = not missing and total <= item["max_bytes"]
        passed &= route_pass
        results.append({
            "route": item["route"], "document": item["document"], "bytes": total,
            "max_bytes": item["max_bytes"], "headroom_bytes": item["max_bytes"] - total,
            "files": [file.relative_to(root).as_posix() for file in files], "missing": missing,
            "pass": route_pass,
        })
    return results, passed


def main() -> int:
    parser = argparse.ArgumentParser(description="Check deterministic first-party asset budgets.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("assets/data/performance-budget.json"))
    parser.add_argument("--json", action="store_true", help="emit a machine-readable report")
    args = parser.parse_args()
    root = args.root.resolve()
    config_path = args.config if args.config.is_absolute() else root / args.config
    try:
        results, passed = check(root, load_config(config_path))
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    report = {"schema": "performance-budget-report/v1", "scope": load_config(config_path).get("scope", ""), "results": results, "pass": passed}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for result in results:
            state = "PASS" if result["pass"] else "FAIL"
            print(f"{state} {result['route']}: {result['bytes']} / {result['max_bytes']} bytes ({result['headroom_bytes']} headroom)")
            if result["missing"]:
                print(f"  missing: {', '.join(result['missing'])}")
        print("Performance asset budgets passed." if passed else "Performance asset budgets failed.")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
