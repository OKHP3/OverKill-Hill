#!/usr/bin/env python3
"""Focused regression checks for localized construction-banner validation."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_banner", ROOT / "scripts" / "check-banner.py")
if SPEC is None or SPEC.loader is None:
    raise SystemExit("Unable to load scripts/check-banner.py")
check_banner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_banner)


def check_case(name: str, anchor: str, expected_status: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        page = Path(temp_dir) / "index.html"
        page.write_text(f"<main>{anchor}</main>", encoding="utf-8")
        status, _ = check_banner.check_file(
            str(page), expected_release="v0.5"
        )
    if status != expected_status:
        raise AssertionError(f"{name}: expected {expected_status}, got {status}")


def main() -> int:
    featured = "/writings/first-diagram-is-a-liar/#council-scoring"
    check_case(
        "localized marker matches release",
        f'<a class="site-specials-link" data-banner-localized="true" data-banner-release="v0.5" href="{featured}">La versión 0.5 ya está en línea</a>',
        "ok",
    )
    check_case(
        "localized marker accepts valid quoting, spacing, and casing",
        f'<a class="site-specials-link" DATA-BANNER-LOCALIZED = \'TRUE\' data-banner-release="v0.5" href="{featured}">La versión 0.5 ya está en línea</a>',
        "ok",
    )
    check_case(
        "localized marker without release fails",
        f'<a class="site-specials-link" data-banner-localized="true" href="{featured}">La versión 0.5 ya está en línea</a>',
        "mismatch",
    )
    check_case(
        "localized marker with wrong release fails",
        f'<a class="site-specials-link" data-banner-localized="true" data-banner-release="v0.4" href="{featured}">La versión 0.4 ya está en línea</a>',
        "mismatch",
    )
    check_case(
        "ordinary English mismatch still fails",
        f'<a class="site-specials-link" href="{featured}">v0.5 is live: unrelated copy</a>',
        "mismatch",
    )
    print("check-banner localized regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
