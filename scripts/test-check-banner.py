#!/usr/bin/env python3
"""Focused regression checks for localized construction-banner validation."""

from __future__ import annotations

import importlib.util
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_banner", ROOT / "scripts" / "check-banner.py")
if SPEC is None or SPEC.loader is None:
    raise SystemExit("Unable to load scripts/check-banner.py")
check_banner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_banner)


def check_case(
    name: str,
    anchor: str,
    expected_status: str,
    *,
    expected_release: str = "v0.5",
    relative_path: str = "index.html",
    expected_message_parts: tuple[str, ...] = (),
) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        page = Path(temp_dir) / relative_path
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(f"<main>{anchor}</main>", encoding="utf-8")
        status, message = check_banner.check_file(str(page), expected_release=expected_release)
    if status != expected_status:
        raise AssertionError(f"{name}: expected {expected_status}, got {status}")
    for part in expected_message_parts:
        if message is None or part not in message:
            raise AssertionError(f"{name}: expected {part!r} in {message!r}")


def check_main_case(
    name: str,
    banner_path: str,
    anchor: str,
    expected_message_parts: tuple[str, ...],
) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        article = "<span>Article v0.6: Council-Assisted Scoring</span>"
        for relative_path in (
            check_banner.FEATURED_ARTICLE_SOURCE,
            check_banner.FEATURED_ARTICLE_GENERATED,
        ):
            article_path = root / relative_path
            article_path.parent.mkdir(parents=True, exist_ok=True)
            article_path.write_text(article, encoding="utf-8")

        banner = root / banner_path
        banner.parent.mkdir(parents=True, exist_ok=True)
        banner_content = article if banner_path == check_banner.FEATURED_ARTICLE_GENERATED else ""
        banner.write_text(banner_content + anchor, encoding="utf-8")

        output = StringIO()
        with (
            patch.object(check_banner, "__file__", str(root / "scripts/check-banner.py")),
            patch("sys.argv", ["check-banner.py"]),
            redirect_stdout(output),
        ):
            try:
                check_banner.main()
            except SystemExit as exc:
                if exc.code != 1:
                    raise AssertionError(f"{name}: expected exit 1, got {exc.code}")
            else:
                raise AssertionError(f"{name}: expected a mismatch")

    report = output.getvalue()
    for part in expected_message_parts:
        if part not in report:
            raise AssertionError(f"{name}: expected {part!r} in {report!r}")


def main() -> int:
    featured = "/writings/first-diagram-is-a-liar/#council-scoring"
    stale_release = "v0.6"
    release_failure = (
        f"banner release mismatch for {check_banner.FEATURED_ARTICLE_ROUTE}",
        f"expected {stale_release}",
        "found v0.5",
    )
    stale_source_failure = release_failure + (check_banner.SOURCE_BANNER,)
    check_main_case(
        "stale source partial reports featured route and expected release",
        check_banner.SOURCE_BANNER,
        f'<a class="site-specials-link" href="{featured}">{check_banner.CANONICAL_BANNER}</a>',
        stale_source_failure,
    )
    stale_generated_failure = release_failure + (check_banner.FEATURED_ARTICLE_GENERATED,)
    check_main_case(
        "stale generated banner reports featured route and expected release",
        check_banner.FEATURED_ARTICLE_GENERATED,
        f'<a class="site-specials-link" href="{featured}">{check_banner.CANONICAL_BANNER}</a>',
        stale_generated_failure,
    )
    check_case(
        "other article banner retains the allow-list behavior",
        '<a class="site-specials-link" href="/writings/another-article/">'
        "v0.4 is live: Another article"
        "</a>",
        "ok",
        expected_release=stale_release,
    )
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
