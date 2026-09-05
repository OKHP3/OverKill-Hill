#!/usr/bin/env python3
"""Build the deliberately allowlisted GitHub Pages release directory.

The site is authored in this repository, but Pages must receive only rendered
routes and runtime files.  This builder makes that boundary explicit and puts
release provenance alongside the packaged files rather than changing the
working tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = (
    ".nojekyll",
    "CNAME",
    "favicon.ico",
    "favicon.svg",
    "humans.txt",
    "llms.txt",
    "robots.txt",
    "site.webmanifest",
    "sitemap.xml",
)
STATIC_EXTENSIONS = {".avif", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
RUNTIME_ASSET_RULES = (
    ("assets/css", {".css"}),
    ("assets/data", {".json"}),
    ("assets/downloads", None),
    ("assets/img", STATIC_EXTENSIONS),
    ("assets/js", {".js"}),
    ("assets/vendor", {".css", ".js", ".json", ".mjs", ".wasm"}),
    (".well-known", None),
)
REQUIRED_EXCLUSIONS = (
    "AGENTS.md",
    "package-lock.json",
    "scripts/build-site.py",
    "site-src/pages/index.main.html",
    "tests/csp-qa.test.mjs",
    "assets/templates/template--homepage.html",
)
PUBLIC_HTML_DIRECTORIES = (
    "about", "contact", "de", "es", "found-ry", "fr", "legal", "manifesto",
    "projects", "prompt-forge", "search", "universe", "vault", "writings",
)


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def checked_relative_path(value: object, label: str) -> Path:
    if not isinstance(value, str) or not value:
        fail(f"{label} must be a non-empty string")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.suffix.lower() != ".html":
        fail(f"unsafe published page path: {value!r}")
    return Path(*path.parts)


def load_public_pages(source: Path) -> list[Path]:
    manifest_path = source / "site-src/pages.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read source page manifest: {exc}")
    pages = manifest.get("pages") if isinstance(manifest, dict) else None
    if not isinstance(pages, list) or not pages:
        fail("source page manifest has no pages list")
    paths = [checked_relative_path(page.get("path") if isinstance(page, dict) else None, "page path") for page in pages]
    if len(paths) != len(set(paths)):
        fail("source page manifest has duplicate paths")
    sitemap_path = source / "sitemap.xml"
    try:
        sitemap = ElementTree.parse(sitemap_path)
    except (OSError, ElementTree.ParseError) as exc:
        fail(f"cannot parse source sitemap: {exc}")
    sitemap_pages = [route_file(location) for node in sitemap.findall(".//{*}loc") if (location := node.text)]
    if not sitemap_pages:
        fail("source sitemap has no routes")
    # Some public noindex routes (including localized pilots) are independently
    # authored and therefore absent from both the renderer manifest and sitemap.
    # Their explicitly allowlisted route directories keep them public without
    # treating every repository HTML file as a release candidate.
    directory_pages: list[Path] = []
    for directory in PUBLIC_HTML_DIRECTORIES:
        root = source / directory
        if root.is_dir():
            directory_pages.extend(path.relative_to(source) for path in root.rglob("*.html"))
    return sorted(set(paths) | set(sitemap_pages) | set(directory_pages))


def copy_file(source: Path, output: Path, relative: Path) -> None:
    original = source / relative
    if not original.is_file():
        fail(f"allowlisted file is missing: {relative.as_posix()}")
    target = output / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(original, target)


def copy_runtime_assets(source: Path, output: Path) -> None:
    for directory, extensions in RUNTIME_ASSET_RULES:
        original_directory = source / directory
        if not original_directory.exists():
            continue
        if not original_directory.is_dir():
            fail(f"allowlisted runtime location is not a directory: {directory}")
        for original in sorted(path for path in original_directory.rglob("*") if path.is_file()):
            if extensions is not None and original.suffix.lower() not in extensions:
                continue
            relative = original.relative_to(source)
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, target)


def route_file(path: str) -> Path:
    parsed = urlparse(path)
    if parsed.query or parsed.fragment:
        fail(f"sitemap route is not a plain path: {path!r}")
    route = parsed.path
    if route == "/":
        return Path("index.html")
    if route.endswith("/"):
        return Path(route.lstrip("/")) / "index.html"
    return Path(route.lstrip("/"))


def verify_package(output: Path, pages: list[Path]) -> None:
    for page in pages:
        if not (output / page).is_file():
            fail(f"published page is missing from package: {page.as_posix()}")
    for relative in ROOT_FILES:
        if not (output / relative).is_file():
            fail(f"required root release file is missing: {relative}")
    for forbidden in REQUIRED_EXCLUSIONS:
        if (output / forbidden).exists():
            fail(f"forbidden source file entered release package: {forbidden}")

    try:
        sitemap = ElementTree.parse(output / "sitemap.xml")
    except (OSError, ElementTree.ParseError) as exc:
        fail(f"cannot parse packaged sitemap: {exc}")
    locations = [node.text for node in sitemap.findall(".//{*}loc") if node.text]
    if not locations:
        fail("packaged sitemap has no routes")
    missing = [location for location in locations if not (output / route_file(location)).is_file()]
    if missing:
        fail("packaged sitemap routes are missing: " + ", ".join(missing))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest(output: Path, commit: str) -> None:
    artifacts = {}
    for public_path in ("sitemap.xml", "assets/data/search-index.json"):
        path = output / public_path
        if not path.is_file():
            fail(f"generated artifact is missing from release package: {public_path}")
        artifacts[f"/{public_path}"] = {"sha256": sha256(path)}
    manifest_relative = "assets/audit/release-manifest.json"
    files = sorted(
        [path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()]
        + [manifest_relative]
    )
    manifest = {"schema": 2, "commit": commit, "artifacts": artifacts, "files": files}
    target = output / manifest_relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build(source: Path, output: Path, commit: str) -> None:
    if output.exists():
        fail(f"release output already exists; provide a new empty path: {output}")
    if not source.is_dir():
        fail(f"source directory does not exist: {source}")
    if len(commit) != 40 or any(char not in "0123456789abcdef" for char in commit.lower()):
        fail("commit must be a full 40-character Git SHA")
    pages = load_public_pages(source)
    output.mkdir(parents=True)
    for page in pages:
        copy_file(source, output, page)
    for root_file in ROOT_FILES:
        copy_file(source, output, Path(root_file))
    copy_runtime_assets(source, output)
    verify_package(output, pages)
    write_manifest(output, commit)
    print(f"Built allowlisted release: {len(pages)} HTML pages, {sum(1 for path in output.rglob('*') if path.is_file())} files")


def verify(source: Path, output: Path, commit: str) -> None:
    """Verify an already-built release without copying or regenerating it."""
    if not output.is_dir():
        fail(f"release output does not exist: {output}")
    pages = load_public_pages(source)
    verify_package(output, pages)
    manifest_path = output / "assets/audit/release-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read release manifest: {exc}")
    if not isinstance(manifest, dict) or manifest.get("schema") != 2:
        fail("release manifest has an unsupported schema")
    if manifest.get("commit") != commit:
        fail(f"release manifest commit does not match expected SHA: {manifest.get('commit')!r}")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        fail("release manifest artifacts map is missing")
    for public_path in ("sitemap.xml", "assets/data/search-index.json"):
        entry = artifacts.get(f"/{public_path}")
        expected_hash = entry.get("sha256") if isinstance(entry, dict) else None
        actual_hash = sha256(output / public_path)
        if expected_hash != actual_hash:
            fail(f"release manifest hash mismatch for {public_path}")
    actual_files = sorted(path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file())
    if manifest.get("files") != actual_files:
        fail("release manifest file inventory does not match packaged bytes")
    print(f"Verified SHA-bound release: {len(pages)} HTML pages, {len(actual_files)} files")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="release directory")
    parser.add_argument("--commit", required=True, help="full validated Git SHA")
    parser.add_argument("--source", type=Path, default=ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--verify", action="store_true", help="verify an existing release without rebuilding it")
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    if args.verify:
        verify(source, output, args.commit)
    else:
        build(source, output, args.commit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
