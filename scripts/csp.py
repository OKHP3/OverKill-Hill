#!/usr/bin/env python3
"""Canonical CSP policies and page classification for the static site."""
from __future__ import annotations

import base64
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_FILE = ROOT / "config" / "csp-policies.json"
META_RE = re.compile(
    r'<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content=(["\'])(.*?)\1\s*/?>',
    re.IGNORECASE,
)


def page_class(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel in {"404.html", "under-construction.html", "search/index.html", "vault/index.html"}:
        return "utility"
    # Pages that host another application need an explicit frame destination.
    source = path.read_text(encoding="utf-8", errors="replace")
    if 'id="tool-iframe"' in source or 'id="skillz-iframe"' in source or "<iframe" in source:
        return "embed"
    return "standard"


def sha256_source(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return "'sha256-" + base64.b64encode(digest).decode("ascii") + "'"


def inline_sources(path: Path) -> tuple[set[str], set[str]]:
    source = path.read_text(encoding="utf-8", errors="replace")
    script_hashes = {
        sha256_source(match.group(1))
        for match in re.finditer(r"<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", source, re.I)
        if match.group(1).strip()
    }
    style_attr_hashes = {
        sha256_source(html.unescape(match.group(1)))
        for match in re.finditer(r'\bstyle=["\']([^"\']*)["\']', source, re.I)
    }
    return script_hashes, style_attr_hashes


def all_pages() -> list[Path]:
    tracked = subprocess.run(
        ["git", "ls-files", "*.html"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return sorted(
        ROOT / name
        for name in tracked.stdout.splitlines()
        if not name.startswith("assets/templates/")
    )


def build_policies() -> dict[str, str]:
    hashes: dict[str, set[str]] = {"standard": set(), "embed": set(), "utility": set()}
    style_hashes: dict[str, set[str]] = {"standard": set(), "embed": set(), "utility": set()}
    for page in all_pages():
        scripts, styles = inline_sources(page)
        kind = page_class(page)
        hashes[kind].update(scripts)
        style_hashes[kind].update(styles)

    common = (
        "default-src 'self'; "
        "script-src 'self' https://www.googletagmanager.com https://cdn.jsdelivr.net "
        + " ".join(sorted(hashes["standard"]))
        + "; script-src-attr 'none'; "
        "style-src 'self' https://fonts.googleapis.com "
        + " ".join(sorted(style_hashes["standard"]))
        + "; style-src-attr 'unsafe-hashes' "
        + " ".join(sorted(style_hashes["standard"]))
        + "; font-src 'self' data: https://fonts.gstatic.com; "
        "img-src 'self' data: https://overkillhill.com https://*.github.io; "
        "connect-src 'self' https://www.google-analytics.com https://*.google-analytics.com https://www.googletagmanager.com https://cdn.jsdelivr.net; "
        "object-src 'none'; base-uri 'self'; form-action 'self'; "
        "manifest-src 'self'; upgrade-insecure-requests"
    )

    # Keep each class explicit even where it currently shares most directives.
    # This prevents an embed allowance from silently spreading to ordinary pages.
    policies = {"standard": common}
    for kind, frame in (("embed", "https://okhp3.github.io"), ("utility", "")):
        policy = (
            "default-src 'self'; "
            "script-src 'self' https://www.googletagmanager.com https://cdn.jsdelivr.net "
            + " ".join(sorted(hashes[kind]))
            + "; script-src-attr 'none'; "
            "style-src 'self' https://fonts.googleapis.com "
            + " " .join(sorted(style_hashes[kind]))
            + "; style-src-attr 'unsafe-hashes' "
            + " ".join(sorted(style_hashes[kind]))
            + "; font-src 'self' data: https://fonts.gstatic.com; "
            "img-src 'self' data: https://overkillhill.com https://*.github.io; "
            "connect-src 'self' https://www.google-analytics.com https://*.google-analytics.com https://www.googletagmanager.com https://cdn.jsdelivr.net; "
            + (f"frame-src 'self' {frame}; " if frame else "")
            + "object-src 'none'; base-uri 'self'; form-action 'self'; "
            "manifest-src 'self'; upgrade-insecure-requests"
        )
        policies[kind] = policy
    return policies


def build_edge_policy() -> str:
    """Build the enforcing header policy, broad enough for every page class.

    Page meta policies remain the tighter class-specific policies. Browsers
    intersect the header and meta policies, so this header must permit the
    union while never adding a destination absent from the page policies.
    """
    scripts: set[str] = set()
    styles: set[str] = set()
    for page in all_pages():
        page_scripts, page_styles = inline_sources(page)
        scripts.update(page_scripts)
        styles.update(page_styles)
    return (
        "default-src 'self'; script-src 'self' https://www.googletagmanager.com "
        "https://cdn.jsdelivr.net " + " ".join(sorted(scripts))
        + "; script-src-attr 'none'; style-src 'self' https://fonts.googleapis.com "
        + " ".join(sorted(styles))
        + "; style-src-attr 'unsafe-hashes' " + " ".join(sorted(styles))
        + "; font-src 'self' data: https://fonts.gstatic.com; "
        "img-src 'self' data: https://overkillhill.com https://*.github.io; "
        "connect-src 'self' https://www.google-analytics.com https://*.google-analytics.com "
        "https://www.googletagmanager.com https://cdn.jsdelivr.net; "
        "frame-src 'self' https://okhp3.github.io; frame-ancestors 'self'; "
        "object-src 'none'; base-uri 'self'; form-action 'self'; manifest-src 'self'; "
        "upgrade-insecure-requests; report-uri /__csp-report"
    )


def load_policies() -> dict[str, str]:
    return json.loads(POLICY_FILE.read_text(encoding="utf-8"))["policies"]


def meta_policy(path: Path) -> str | None:
    source = path.read_text(encoding="utf-8", errors="replace")
    match = META_RE.search(source)
    return match.group(2) if match else None


def render_meta(policy: str) -> str:
    return f'<meta http-equiv="Content-Security-Policy" content="{policy}" />'