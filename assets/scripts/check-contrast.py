#!/usr/bin/env python3
"""
check-contrast.py — WCAG AA contrast audit for theme.css tokens.

Usage:
    python3 assets/scripts/check-contrast.py [path/to/theme.css]

Exit codes:
    0  — all checks pass
    1  — one or more contrast failures detected

Checks (WCAG 1.4.3, AA level):
  Normal text (≥ 4.5 : 1):
    • --color-fg          on --color-bg, --color-surface, --color-surface-soft
    • --color-muted       on --color-bg, --color-surface, --color-surface-soft
    • --color-amber-text  on --color-bg, --color-surface, --color-surface-soft
    • --color-link-hover  on --color-bg, --color-surface, --color-surface-soft
    • --color-btn-primary-fg on --okh-orange (primary button text on its
      gradient background)

  Large / UI text and non-text UI components (≥ 3.0 : 1, WCAG 1.4.11):
    • --color-accent    on --color-bg, --color-surface, --color-surface-soft
      (also covers the branded a:focus-visible outline ring, which uses
      --color-accent against the same surfaces)

Both dark (default :root) and light (:root[data-theme="light"]) themes are
checked independently.
"""

import re
import sys
import math
import pathlib
from typing import Optional


# ── WCAG helpers ────────────────────────────────────────────────────────────

def _linearise(c: float) -> float:
    """Convert an sRGB channel (0–1) to linear light."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    """Return WCAG relative luminance of a #rrggbb hex colour."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    r, g, b = (int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return 0.2126 * _linearise(r) + 0.7152 * _linearise(g) + 0.0722 * _linearise(b)


def contrast_ratio(fg: str, bg: str) -> float:
    """Return WCAG contrast ratio between two #rrggbb hex colours."""
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ── CSS token extraction ─────────────────────────────────────────────────────

# Matches a CSS custom property declaration:  --name: value;
_PROP_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;]+?)\s*;")

# Matches a var() reference — supports nested fallbacks naively
_VAR_RE  = re.compile(r"var\(\s*(--[\w-]+)(?:\s*,[^)]+)?\s*\)")

# Matches a solid #rgb / #rrggbb hex colour
_HEX_RE  = re.compile(r"#[0-9a-fA-F]{3,6}\b")

# Matches rgba?(r, g, b, a?) — used to skip non-solid colours
_RGBA_RE = re.compile(r"rgba?\s*\(", re.IGNORECASE)


def _extract_block(css: str, selector: str) -> str:
    """
    Return the raw content inside the *first* matching rule block.

    selector is matched as a plain-text prefix of the selector text, so
    passing ':root' matches both ':root {' and ':root[data-theme="light"] {'.
    We use a precise match approach: scan for the selector, then collect
    balanced braces.
    """
    # Find all positions where `selector` could be followed by optional
    # whitespace / attributes and then an opening brace.
    pattern = re.compile(
        re.escape(selector) + r'(?:[^\{]*?)\{',
        re.DOTALL
    )
    for m in pattern.finditer(css):
        # Make sure the found selector is *exactly* selector (not a substring
        # of a longer one).  We check that the character immediately before
        # the selector is a newline / start-of-string or is not alphanumeric.
        start = m.start()
        if start > 0 and css[start - 1] not in ('\n', '\r', ' ', '\t', '}', '{'):
            continue
        # Walk forward collecting balanced braces.
        depth = 1
        pos = m.end()  # position just after the opening '{'
        while pos < len(css) and depth:
            if css[pos] == '{':
                depth += 1
            elif css[pos] == '}':
                depth -= 1
            pos += 1
        return css[m.end() - 1: pos - 1]  # content between the outer braces
    return ""


def _parse_tokens(block: str) -> dict:
    """Extract {name: raw_value} pairs from a CSS block."""
    return {m.group(1): m.group(2).strip() for m in _PROP_RE.finditer(block)}


def _resolve(name: str, tokens: dict, stack: Optional[set] = None) -> Optional[str]:
    """
    Recursively resolve a CSS custom property name to its hex value.
    Returns None if the value cannot be resolved to a hex colour.
    """
    if stack is None:
        stack = set()
    if name in stack:
        return None  # circular reference guard
    stack.add(name)

    raw = tokens.get(name)
    if raw is None:
        return None

    # If it contains a var() reference, resolve that first
    var_match = _VAR_RE.search(raw)
    if var_match:
        resolved = _resolve(var_match.group(1), tokens, stack)
        return resolved

    # If it's a direct hex colour, return it
    hex_match = _HEX_RE.match(raw.strip())
    if hex_match:
        return hex_match.group(0)

    return None


def _build_theme(css: str, selector_exact: str, inherit_from: Optional[dict] = None) -> dict:
    """
    Build a resolved token map for one theme.

    css              — full CSS text
    selector_exact   — exact selector string, e.g. ':root'
    inherit_from     — base token map to inherit (for override themes)
    """
    block = _extract_block(css, selector_exact)
    raw_tokens = _parse_tokens(block)

    # Merge: override theme inherits base, then applies its own declarations
    merged_raw = dict(inherit_from or {})
    merged_raw.update(raw_tokens)

    # Resolve all tokens to hex
    resolved = {}
    for name in merged_raw:
        hex_val = _resolve(name, merged_raw)
        if hex_val:
            resolved[name] = hex_val.lower()

    return resolved


# ── Contrast check logic ─────────────────────────────────────────────────────

NORMAL_TEXT_MIN = 4.5   # WCAG AA normal text
LARGE_UI_MIN    = 3.0   # WCAG AA large / UI elements


CHECK_PAIRS = [
    # (fg_token, bg_token, min_ratio, label)
    # Normal text
    ("--color-fg",          "--color-bg",           NORMAL_TEXT_MIN, "normal text"),
    ("--color-fg",          "--color-surface",       NORMAL_TEXT_MIN, "normal text"),
    ("--color-fg",          "--color-surface-soft",  NORMAL_TEXT_MIN, "normal text"),
    ("--color-muted",       "--color-bg",            NORMAL_TEXT_MIN, "normal text"),
    ("--color-muted",       "--color-surface",       NORMAL_TEXT_MIN, "normal text"),
    ("--color-muted",       "--color-surface-soft",  NORMAL_TEXT_MIN, "normal text"),
    ("--color-amber-text",  "--color-bg",            NORMAL_TEXT_MIN, "normal text"),
    ("--color-amber-text",  "--color-surface",       NORMAL_TEXT_MIN, "normal text"),
    ("--color-amber-text",  "--color-surface-soft",  NORMAL_TEXT_MIN, "normal text"),
    ("--color-link-hover",  "--color-bg",            NORMAL_TEXT_MIN, "normal text (link hover)"),
    ("--color-link-hover",  "--color-surface",       NORMAL_TEXT_MIN, "normal text (link hover)"),
    ("--color-link-hover",  "--color-surface-soft",  NORMAL_TEXT_MIN, "normal text (link hover)"),
    ("--color-btn-primary-fg", "--okh-orange",        NORMAL_TEXT_MIN, "normal text (primary button)"),
    # Large / UI elements (also covers the branded focus-visible outline ring)
    ("--color-accent",      "--color-bg",            LARGE_UI_MIN,    "large/UI, focus ring"),
    ("--color-accent",      "--color-surface",       LARGE_UI_MIN,    "large/UI, focus ring"),
    ("--color-accent",      "--color-surface-soft",  LARGE_UI_MIN,    "large/UI, focus ring"),
]


def _check_theme(theme_name: str, tokens: dict) -> list:
    """Run all CHECK_PAIRS for one theme. Returns list of failure strings."""
    failures = []
    for fg_tok, bg_tok, min_ratio, label in CHECK_PAIRS:
        fg = tokens.get(fg_tok)
        bg = tokens.get(bg_tok)
        if fg is None or bg is None:
            missing = []
            if fg is None:
                missing.append(fg_tok)
            if bg is None:
                missing.append(bg_tok)
            failures.append(
                f"  SKIP  [{theme_name}] {fg_tok} / {bg_tok} "
                f"— could not resolve: {', '.join(missing)}"
            )
            continue

        ratio = contrast_ratio(fg, bg)
        status = "PASS" if ratio >= min_ratio else "FAIL"
        msg = (
            f"  {status}  [{theme_name}] {fg_tok} ({fg}) on {bg_tok} ({bg})"
            f"  →  {ratio:.2f}:1  (min {min_ratio:.1f}:1, {label})"
        )
        if status == "FAIL":
            failures.append(msg)
        else:
            print(msg)

    return failures


# ── Entry point ──────────────────────────────────────────────────────────────

def main(css_path: str = "assets/css/theme.css") -> int:
    path = pathlib.Path(css_path)
    if not path.exists():
        print(f"ERROR: {css_path} not found.", file=sys.stderr)
        return 1

    css = path.read_text(encoding="utf-8")

    print(f"\n{'='*70}")
    print(f"  WCAG AA contrast audit — {css_path}")
    print(f"{'='*70}\n")

    # Build dark-mode token map (the :root defaults)
    # Use a two-pass approach: first parse raw, then resolve with the raw map
    root_block = _extract_block(css, ":root")
    root_raw   = _parse_tokens(root_block)

    # Exclude light-mode block from contaminating the root parse by checking
    # that :root is parsed without the [data-theme] suffix tokens
    dark_tokens = _build_theme(css, ":root")

    # Build light-mode token map (inherits dark, then overrides)
    light_tokens = _build_theme(css, ':root[data-theme="light"]', inherit_from=root_raw)

    print("── Dark mode (default :root) ──────────────────────────────────────────\n")
    dark_failures = _check_theme("dark", dark_tokens)

    print("\n── Light mode (:root[data-theme=\"light\"]) ────────────────────────────\n")
    light_failures = _check_theme("light", light_tokens)

    all_failures = dark_failures + light_failures

    print(f"\n{'='*70}")
    if all_failures:
        print(f"  ✗  {len(all_failures)} FAILURE(S) detected:\n")
        for f in all_failures:
            print(f)
        print(f"\n{'='*70}\n")
        return 1
    else:
        print(f"  ✓  All contrast checks PASSED.\n{'='*70}\n")
        return 0


if __name__ == "__main__":
    css_file = sys.argv[1] if len(sys.argv) > 1 else "assets/css/theme.css"
    sys.exit(main(css_file))
