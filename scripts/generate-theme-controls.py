#!/usr/bin/env python3
"""Generate the browser theme constants embedded in the shared app.js runtime."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from brand_theme import load_brand_theme_contract, render_brand_theme_block


ROOT = SCRIPT_DIR.parent
APP_SCRIPT_PATH = ROOT / "assets" / "js" / "app.js"
START_MARKER = "// BEGIN GENERATED BRAND THEME CONFIG."
END_MARKER = "// END GENERATED BRAND THEME CONFIG."


def replace_generated_block(source: str, generated: str) -> str:
    """Replace exactly one generated block without changing surrounding bytes."""
    start = source.find(START_MARKER)
    end = source.find(END_MARKER)
    if start < 0 or end < 0 or end < start:
        raise ValueError(
            f"{APP_SCRIPT_PATH}: generated brand theme markers are missing or out of order"
        )
    end += len(END_MARKER)
    if source.find(START_MARKER, start + len(START_MARKER)) >= 0:
        raise ValueError(f"{APP_SCRIPT_PATH}: duplicate generated brand theme blocks")
    if source.find(END_MARKER, end) >= 0:
        raise ValueError(f"{APP_SCRIPT_PATH}: duplicate generated brand theme blocks")

    block_start = source.rfind("\n", 0, start) + 1
    block_end = source.find("\n", end)
    if block_end < 0:
        block_end = len(source)
    else:
        block_end += 1
    return source[:block_start] + generated + source[block_end:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when app.js does not match the reviewed contract",
    )
    args = parser.parse_args(argv)

    try:
        generated = render_brand_theme_block(load_brand_theme_contract())
        current = APP_SCRIPT_PATH.read_text(encoding="utf-8")
        updated = replace_generated_block(current, generated)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if current != updated:
            print(
                "assets/js/app.js is stale with config/brand-theme-contract.json. "
                "Run: python3 scripts/generate-theme-controls.py"
            )
            return 1
        print("Browser theme constants are current.")
        return 0

    if current != updated:
        APP_SCRIPT_PATH.write_text(updated, encoding="utf-8")
    print(f"Generated browser theme constants in {APP_SCRIPT_PATH.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())