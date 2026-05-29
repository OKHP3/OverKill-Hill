#!/usr/bin/env python3
"""
check-accent-contrast.py
Advisory scanner: flags uses of accent colors on body-text elements.

Background
----------
The glee-fully.tools accent colors (#d94f63, #d35b2d) sit at 3.37-3.55:1
contrast against the paper background (#f6f2ee). They pass WCAG 2.1 AA for
large/bold text (>=18.67 px normal, >=14 px bold) but fail for normal-weight
body text at default size.

Task #26 introduced a dark-mode palette (--bg #1a1210, --color-accent #f07585)
where the lightened coral reaches 4.9:1 against the dark surface (#241c1a),
passing WCAG AA for all text sizes. This script checks BOTH modes and reports
contrast ratios for each so regressions in either direction are caught.

Editorial rule (from assets/docs/gleefully-replit-theme-guide.md):
  var(--color-accent) must not be used as the sole color signal for
  normal-weight body text smaller than 18.67 px.

Scanning passes
---------------
Pass 1 — HTML files: inline style= attributes and known utility class names.
Pass 2 — CSS files:  class rules in theme.css (and any other project CSS)
          that set `color` to an accent token/hex on a risky element selector.

Usage
-----
  python3 scripts/check-accent-contrast.py [--strict]

  --strict  Exit 1 if any advisory findings are found (for manual gate use).

Output
------
  Prints a structured advisory report.
  Writes machine-readable JSON to assets/audit/accent-contrast-report.json.
"""

import re
import sys
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# WCAG contrast-ratio math
# ---------------------------------------------------------------------------

def _srgb_linearize(c: int) -> float:
    s = c / 255.0
    return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4


def _hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def relative_luminance(hex_color: str) -> float:
    r, g, b = _hex_to_rgb(hex_color)
    return (
        0.2126 * _srgb_linearize(r)
        + 0.7152 * _srgb_linearize(g)
        + 0.0722 * _srgb_linearize(b)
    )


def contrast_ratio(fg: str, bg: str) -> float:
    """Return WCAG contrast ratio (>=1.0) between two hex colors."""
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_aa_normal(ratio: float) -> bool:
    return ratio >= 4.5


def wcag_aa_large(ratio: float) -> bool:
    return ratio >= 3.0


# ---------------------------------------------------------------------------
# Mode palettes
# ---------------------------------------------------------------------------

# Light-mode palette (Glee-fully paper theme)
LIGHT_MODE = {
    "bg":           "#f6f2ee",
    "surface":      "#f6f2ee",
    "accent_hex":   ["#d94f63", "#d35b2d"],   # coral, rust
}

# Dark-mode defaults (Task #26; overridden by parse_dark_mode_tokens if found)
_DARK_MODE_DEFAULTS = {
    "bg":           "#1a1210",
    "surface":      "#241c1a",
    "accent_hex":   ["#f07585"],              # lightened coral
}


def parse_dark_mode_tokens(theme_css_path: Path) -> dict:
    """
    Read the first `@media (prefers-color-scheme: dark) { .glee-main { … } }`
    block in theme.css and extract --color-bg, --color-surface, --color-accent.

    Falls back to _DARK_MODE_DEFAULTS for any token not found.
    """
    result = dict(_DARK_MODE_DEFAULTS)
    if not theme_css_path.exists():
        return result

    text = theme_css_path.read_text(encoding="utf-8", errors="ignore")

    # Find the token-layer block: @media dark { .glee-main { --color-bg: … } }
    # We look for the first @media block that contains `--color-accent` override.
    dark_block_re = re.compile(
        r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)"
        r"\s*\{(.*?)\}",
        re.DOTALL | re.IGNORECASE,
    )

    for m in dark_block_re.finditer(text):
        block = m.group(1)
        # Only care about blocks that touch Glee token overrides
        if "--color-accent" not in block:
            continue
        # Extract token values
        bg_m      = re.search(r"--color-bg\s*:\s*(#[0-9a-fA-F]{3,6})", block)
        surf_m    = re.search(r"--color-surface\s*:\s*(#[0-9a-fA-F]{3,6})", block)
        accent_m  = re.search(r"--color-accent\s*:\s*(#[0-9a-fA-F]{3,6})", block)

        if bg_m:
            result["bg"] = bg_m.group(1)
        if surf_m:
            result["surface"] = surf_m.group(1)
        if accent_m:
            result["accent_hex"] = [accent_m.group(1)]
        break  # first matching block is the canonical token layer

    return result


# Pre-populate dark mode at module init (re-parsed in main if needed)
DARK_MODE = dict(_DARK_MODE_DEFAULTS)


def _worst_light_contrast(fg_hex: str) -> float:
    """Lowest contrast the fg hex achieves against any light-mode surface."""
    return min(
        contrast_ratio(fg_hex, LIGHT_MODE["bg"]),
        contrast_ratio(fg_hex, LIGHT_MODE["surface"]),
    )


def _worst_dark_contrast(fg_hex: str) -> float:
    """Lowest contrast the fg hex achieves against any dark-mode surface."""
    return min(
        contrast_ratio(fg_hex, DARK_MODE["bg"]),
        contrast_ratio(fg_hex, DARK_MODE["surface"]),
    )


def _worst_accent_light() -> tuple:
    """(worst_ratio, which_hex) across all light-mode accent hexes."""
    pairs = [(_worst_light_contrast(h), h) for h in LIGHT_MODE["accent_hex"]]
    return min(pairs, key=lambda x: x[0])


def _worst_accent_dark() -> tuple:
    """(worst_ratio, which_hex) across all dark-mode accent hexes."""
    pairs = [(_worst_dark_contrast(h), h) for h in DARK_MODE["accent_hex"]]
    return min(pairs, key=lambda x: x[0])


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ACCENT_HEX_PATTERN = re.compile(
    r"#(?:d94f63|d35b2d)", re.IGNORECASE
)

ACCENT_VAR_PATTERN = re.compile(
    r"var\(\s*--color-(?:accent|rust)\s*[,)]", re.IGNORECASE
)

# Matches a text `color:` declaration (not background-color / border-color)
# pointing to an accent hex or accent CSS variable.
ACCENT_TEXT_COLOR_RE = re.compile(
    r"(?<![a-z-])color\s*:\s*"
    r"(var\(\s*--color-(?:accent|rust)\b[^;]*|#(?:d94f63|d35b2d)\b)",
    re.IGNORECASE,
)

# Matches background-color or border-color (used to exclude those properties)
BG_BORDER_RE = re.compile(r"(background|border)-color", re.IGNORECASE)

# CSS variable definition line (--foo: ...) — not a text-color usage
CSS_VAR_DEF_RE = re.compile(r"^\s*--")

# Bold font-weight in the same rule block (prerequisite for INFO downgrade)
BOLD_WEIGHT_RE = re.compile(r"font-weight\s*:\s*(bold|bolder|[6-9]\d\d)", re.IGNORECASE)

# Explicit font-size in the same rule block — extracts the numeric value in rem/px/pt
# Used alongside BOLD_WEIGHT_RE to confirm the qualifying threshold is provably met.
# Rule: bold text >= 14 px passes WCAG AA at these accent contrast ratios.
FONT_SIZE_RE = re.compile(
    r"font-size\s*:\s*([\d.]+)(rem|em|px|pt)\b", re.IGNORECASE
)

# CSS utility classes known to apply accent color to text
ACCENT_TEXT_CLASSES = {"text-accent", "link-accent"}

# Tags where accent color on text is safe (large/interactive controls)
SAFE_TAGS = {
    "button", "a",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "span",
}

# Tags where accent color on text is risky (normal body text containers)
RISKY_TAGS = {
    "p", "li", "td", "th", "dd", "dt", "figcaption", "blockquote",
    "label", "caption", "small", "em", "strong",
}

# Directories to skip when walking the project tree
SKIP_DIRS = {
    ".pythonlibs", ".cache", ".local", "node_modules",
    ".git", "attached_assets", ".agents",
}

# CSS files to scan (relative to repo root)
CSS_FILES = [Path("assets/css/theme.css")]


# ---------------------------------------------------------------------------
# Contrast helpers for findings
# ---------------------------------------------------------------------------

def _contrast_summary(is_var: bool) -> dict:
    """
    Return a dict with contrast ratios for the finding detail.

    is_var=True  → caller used var(--color-accent/rust); dark mode resolves
                   to the dark-mode accent token (#f07585 by default).
    is_var=False → caller hardcoded a light-mode hex; dark mode does NOT
                   override it, so contrast against dark surfaces improves
                   (dark bg is darker, making the warm accent stand out more).
    """
    light_ratio, light_hex = _worst_accent_light()

    if is_var:
        dark_ratio, dark_hex = _worst_accent_dark()
    else:
        # Hardcoded hex doesn't change in dark mode — pick the light accent
        # hex that has the worst light ratio (same hex stays in dark mode).
        light_ratio, light_hex = _worst_accent_light()
        dark_ratio = _worst_dark_contrast(light_hex)
        dark_hex = light_hex

    light_pass_normal = wcag_aa_normal(light_ratio)
    light_pass_large  = wcag_aa_large(light_ratio)
    dark_pass_normal  = wcag_aa_normal(dark_ratio)
    dark_pass_large   = wcag_aa_large(dark_ratio)

    return {
        "light_contrast":       round(light_ratio, 2),
        "light_accent_hex":     light_hex,
        "light_bg_hex":         LIGHT_MODE["bg"],
        "light_pass_aa_normal": light_pass_normal,
        "light_pass_aa_large":  light_pass_large,
        "dark_contrast":        round(dark_ratio, 2),
        "dark_accent_hex":      dark_hex if is_var else light_hex,
        "dark_bg_hex":          DARK_MODE["surface"],
        "dark_pass_aa_normal":  dark_pass_normal,
        "dark_pass_aa_large":   dark_pass_large,
    }


def _contrast_detail_suffix(cs: dict, is_bold_exempt: bool) -> str:
    """
    Build the human-readable contrast suffix included in every finding detail.

    Shows both light-mode and dark-mode contrast ratios and WCAG AA status.
    """
    lc = cs["light_contrast"]
    dc = cs["dark_contrast"]

    l_status = "✓ AA" if cs["light_pass_aa_normal"] else (
        "✓ AA large" if cs["light_pass_aa_large"] else "✗ below AA"
    )
    d_status = "✓ AA" if cs["dark_pass_aa_normal"] else (
        "✓ AA large" if cs["dark_pass_aa_large"] else "✗ below AA"
    )

    suffix = (
        f" Contrast — light: {lc:.2f}:1 ({l_status}), "
        f"dark: {dc:.2f}:1 ({d_status})."
    )
    return suffix


def _severity_from_contrast(cs: dict, is_bold_exempt: bool) -> str:
    """
    Compute severity given contrast summary and bold-exempt flag.

    ADVISORY — fails WCAG AA on normal text in *either* mode (and not exempt).
    INFO      — passes large/bold AA in both modes (or explicitly bold-exempt).
    """
    light_ok = cs["light_pass_aa_normal"] or (
        is_bold_exempt and cs["light_pass_aa_large"]
    )
    dark_ok  = cs["dark_pass_aa_normal"] or (
        is_bold_exempt and cs["dark_pass_aa_large"]
    )

    if light_ok and dark_ok:
        return "INFO"
    return "ADVISORY"


# ---------------------------------------------------------------------------
# CSS utilities
# ---------------------------------------------------------------------------

def _approx_px(value: float, unit: str) -> float:
    """Approximate pixel size from a CSS length at standard 16 px root."""
    unit = unit.lower()
    if unit in ("rem", "em"):
        return value * 16.0
    if unit == "px":
        return value
    if unit == "pt":
        return value * (4.0 / 3.0)
    return value * 16.0  # conservative fallback


def _block_qualifies_for_bold_exemption(declarations: str) -> bool:
    """
    Return True if this CSS rule block explicitly declares:
      - font-weight >= 600 / bold, AND
      - font-size that computes to >= 14 px (bold WCAG AA threshold)
    Both must be present in the same block — inherited values are not provable.
    """
    if not BOLD_WEIGHT_RE.search(declarations):
        return False
    fs_m = FONT_SIZE_RE.search(declarations)
    if not fs_m:
        return False  # no explicit size — cannot prove threshold is met
    approx = _approx_px(float(fs_m.group(1)), fs_m.group(2))
    return approx >= 14.0


def extract_final_element(selector: str) -> str | None:
    """
    Return the final element type from a CSS selector, or None if the
    selector is class/id/attribute-only (no element type to match on).

    Examples:
      '.glee-main p'            -> 'p'
      '.keep-exploring__name'   -> None
      'body:not(.glee) p.bold'  -> 'p'
      '.foo a > em:first-child' -> 'em'
    """
    s = selector
    # Strip pseudo-elements (::before, ::after, …)
    s = re.sub(r"::[a-zA-Z-]+", "", s)
    # Strip pseudo-classes with parens (:not(…), :nth-child(…), …)
    s = re.sub(r":[a-zA-Z-]+\([^)]*\)", "", s)
    # Strip remaining simple pseudo-classes (:hover, :focus, …)
    s = re.sub(r":[a-zA-Z-]+", "", s)
    # Strip attribute selectors ([attr=val])
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = s.strip()

    # Split on combinators and inspect last token
    for seg in reversed(re.split(r"[\s>~+]+", s)):
        seg = seg.strip()
        m = re.match(r"^([a-zA-Z][a-zA-Z0-9]*)", seg)
        if m:
            return m.group(1).lower()

    return None


def extract_css_rules(css_text: str):
    """
    Yield (selector_str, declarations_str, start_lineno) for every CSS rule
    block in *css_text*, recursing into @media and other at-rules.

    Block comments are stripped (with line-count preserved) before parsing.
    """
    # Strip block comments but keep newlines so line numbers stay accurate
    clean = re.sub(
        r"/\*.*?\*/",
        lambda m: "\n" * m.group(0).count("\n"),
        css_text,
        flags=re.DOTALL,
    )

    def _process(text: str, base_line: int = 1):
        n = len(text)
        j = 0
        while j < n:
            # Skip leading whitespace
            while j < n and text[j] in " \t\n\r":
                j += 1
            if j >= n:
                break

            brace = text.find("{", j)
            if brace == -1:
                break

            selector = text[j:brace].strip()
            # Line number = base + newlines before this opening brace
            lineno = base_line + text[:brace].count("\n")

            # Find the matching closing brace
            depth, k = 1, brace + 1
            while k < n and depth > 0:
                if text[k] == "{":
                    depth += 1
                elif text[k] == "}":
                    depth -= 1
                k += 1

            content = text[brace + 1 : k - 1]

            if selector.lstrip().startswith("@"):
                # At-rule: recurse so inner rules are checked
                yield from _process(content, lineno)
            elif selector:
                yield selector, content, lineno

            j = k

    yield from _process(clean)


# ---------------------------------------------------------------------------
# Pass 1 — HTML scanning
# ---------------------------------------------------------------------------

def scan_html_file(path: Path) -> list[dict]:
    """Return advisory findings for one HTML file (inline styles + utility classes)."""
    findings = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return findings

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("<!--"):
            continue

        # 1a. Inline style= with accent hex as text color
        if "style=" in line and ACCENT_HEX_PATTERN.search(line):
            if re.search(r"(?<!\w)color\s*:\s*(?:#d94f63|#d35b2d)", line, re.IGNORECASE):
                tag_m = re.search(r"<(\w+)\b", line)
                tag = tag_m.group(1).lower() if tag_m else "unknown"
                cs = _contrast_summary(is_var=False)
                severity = "ADVISORY" if tag in RISKY_TAGS else "INFO"
                findings.append({
                    "file": str(path),
                    "line": lineno,
                    "severity": severity,
                    "tag": tag,
                    "rule": "inline-style-accent-color",
                    "detail": (
                        f"<{tag}> has inline accent color -- "
                        f"verify it is large/bold text (>=18.67 px normal "
                        f"or >=14 px bold)."
                        + _contrast_detail_suffix(cs, False)
                    ),
                    "snippet": stripped[:120],
                    **cs,
                })

        # 1b. Inline style= with accent var as text color
        if "style=" in line and ACCENT_VAR_PATTERN.search(line):
            if re.search(
                r"(?<!\w)color\s*:\s*var\(--color-(?:accent|rust)", line, re.IGNORECASE
            ):
                tag_m = re.search(r"<(\w+)\b", line)
                tag = tag_m.group(1).lower() if tag_m else "unknown"
                if tag in RISKY_TAGS:
                    cs = _contrast_summary(is_var=True)
                    findings.append({
                        "file": str(path),
                        "line": lineno,
                        "severity": "ADVISORY",
                        "tag": tag,
                        "rule": "inline-style-accent-var",
                        "detail": (
                            f"<{tag}> uses var(--color-accent/rust) as text color -- "
                            f"accent tokens are below 4.5:1 for normal body text."
                            + _contrast_detail_suffix(cs, False)
                        ),
                        "snippet": stripped[:120],
                        **cs,
                    })

        # 1c. Utility classes that apply accent color to text
        for cls in ACCENT_TEXT_CLASSES:
            if 'class="' in line and cls in line:
                tag_m = re.search(r"<(\w+)\b", line)
                tag = tag_m.group(1).lower() if tag_m else "unknown"
                if tag in RISKY_TAGS:
                    cs = _contrast_summary(is_var=True)
                    findings.append({
                        "file": str(path),
                        "line": lineno,
                        "severity": "ADVISORY",
                        "tag": tag,
                        "rule": f"utility-class-{cls}",
                        "detail": (
                            f"<{tag}> uses .{cls} -- verify it meets "
                            f"large/bold text threshold."
                            + _contrast_detail_suffix(cs, False)
                        ),
                        "snippet": stripped[:120],
                        **cs,
                    })

    return findings


# ---------------------------------------------------------------------------
# Pass 2 — CSS rule scanning
# ---------------------------------------------------------------------------

def scan_css_file(path: Path) -> list[dict]:
    """
    Return advisory findings for CSS rule blocks in *path* that set `color`
    to an accent token/hex on a selector targeting a risky element type.

    Exemptions (downgraded to INFO):
    - `border-color` and `background-color` declarations are ignored.
    - CSS custom-property definitions (--foo: ...) are ignored.
    - If the same rule block also declares a bold font-weight (600+/bold),
      the finding is INFO not ADVISORY, because bold text at >=14 px passes
      WCAG AA for these accent colors.

    Dark-mode awareness (Task #69):
    - Each finding now carries light_contrast and dark_contrast ratios.
    - Severity is ADVISORY when the rule fails WCAG AA on *either* mode.
    - Rules using var(--color-accent) resolve to the dark-mode token in
      dark mode; hardcoded hex values do not change across modes.
    """
    try:
        css_text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    findings = []

    for selector_raw, declarations, lineno in extract_css_rules(css_text):
        # Check every declaration line for a text-color accent usage
        decl_lines = [dl.strip() for dl in declarations.splitlines() if dl.strip()]
        has_accent_text_color = any(
            ACCENT_TEXT_COLOR_RE.search(dl)
            and not BG_BORDER_RE.search(dl)
            and not CSS_VAR_DEF_RE.match(dl)
            for dl in decl_lines
        )
        if not has_accent_text_color:
            continue

        # Determine if usage is via CSS variable or hardcoded hex
        is_var = any(
            ACCENT_VAR_PATTERN.search(dl)
            for dl in decl_lines
            if not BG_BORDER_RE.search(dl) and not CSS_VAR_DEF_RE.match(dl)
        )

        # INFO exemption: same block must prove bold weight + explicit size >= 14 px
        qualifies_for_exemption = _block_qualifies_for_bold_exemption(declarations)

        # Font-size hint for developer guidance
        fs_m = FONT_SIZE_RE.search(declarations)
        if fs_m:
            fs_val = float(fs_m.group(1))
            fs_unit = fs_m.group(2)
            fs_approx = _approx_px(fs_val, fs_unit)
            font_size_hint = f"{fs_m.group(1)}{fs_unit} (~{fs_approx:.0f}px)"
        else:
            font_size_hint = "inherited — check parent rules"

        cs = _contrast_summary(is_var=is_var)

        # Inspect each comma-separated selector part
        for sel_part in selector_raw.split(","):
            sel_part = sel_part.strip()
            if not sel_part:
                continue

            element = extract_final_element(sel_part)
            if element is None:
                continue  # class/id/attribute-only selector — skip

            if element in RISKY_TAGS:
                severity = _severity_from_contrast(cs, qualifies_for_exemption)

                findings.append({
                    "file": str(path),
                    "line": lineno,
                    "severity": severity,
                    "selector": sel_part,
                    "tag": element,
                    "rule": "css-rule-accent-color",
                    "font_size_hint": font_size_hint,
                    "detail": (
                        f"CSS rule '{sel_part}' targets <{element}> with accent color"
                        + (
                            " (bold + explicit font-size >=14px in same block — INFO only)."
                            if qualifies_for_exemption
                            else " -- verify this element is always large/bold text "
                                 "(>=18.67 px normal or >=14 px bold)."
                        )
                        + f" Font size: {font_size_hint}."
                        + _contrast_detail_suffix(cs, qualifies_for_exemption)
                    ),
                    "snippet": f"{sel_part[:70]} {{ color: <accent>; }}",
                    **cs,
                })

    return findings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    strict = "--strict" in sys.argv

    # Parse live dark-mode tokens from theme.css before scanning
    global DARK_MODE
    theme_css = Path("assets/css/theme.css")
    DARK_MODE = parse_dark_mode_tokens(theme_css)

    root = Path(".")
    all_findings: list[dict] = []

    # Pass 1: HTML files
    html_scanned = 0
    for path in sorted(root.rglob("*.html")):
        if any(s in path.parts for s in SKIP_DIRS):
            continue
        all_findings.extend(scan_html_file(path))
        html_scanned += 1

    # Pass 2: CSS files
    css_scanned = 0
    for css_path in CSS_FILES:
        if not css_path.exists():
            continue
        all_findings.extend(scan_css_file(css_path))
        css_scanned += 1

    # Additionally scan any other .css files in the project (excluding skip dirs)
    css_paths_seen = {p.resolve() for p in CSS_FILES}
    for path in sorted(root.rglob("*.css")):
        if any(s in path.parts for s in SKIP_DIRS):
            continue
        if path.resolve() in css_paths_seen:
            continue
        all_findings.extend(scan_css_file(path))
        css_scanned += 1
        css_paths_seen.add(path.resolve())

    # Separate by severity
    advisories = [f for f in all_findings if f["severity"] == "ADVISORY"]
    infos      = [f for f in all_findings if f["severity"] == "INFO"]

    # Write machine-readable output
    out_dir = Path("assets/audit")
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "generated": "2026-05-28",
        "html_files_scanned": html_scanned,
        "css_files_scanned": css_scanned,
        "advisory_count": len(advisories),
        "info_count": len(infos),
        "findings": all_findings,
        "light_mode": {
            "bg": LIGHT_MODE["bg"],
            "surface": LIGHT_MODE["surface"],
            "accent_colors": LIGHT_MODE["accent_hex"],
            "worst_contrast": round(_worst_accent_light()[0], 2),
        },
        "dark_mode": {
            "bg": DARK_MODE["bg"],
            "surface": DARK_MODE["surface"],
            "accent_colors": DARK_MODE["accent_hex"],
            "worst_contrast": round(_worst_accent_dark()[0], 2),
            "source": str(theme_css) if theme_css.exists() else "defaults",
        },
        "rule": (
            "var(--color-accent) must not be used as the sole color signal for "
            "normal-weight body text smaller than 18.67 px. "
            "Light-mode contrast: #d94f63 = 3.37:1, #d35b2d = 3.55:1 (bg #f6f2ee). "
            "Dark-mode contrast: #f07585 = 4.9:1 (surface #241c1a). "
            "Passes WCAG 2.1 AA for large/bold text (>=18.67px normal or >=14px bold) "
            "but light-mode fails for normal body text. "
            "Any rule that fails on either mode is flagged ADVISORY."
        ),
        "passes": [
            "Pass 1 — HTML inline style= attributes and utility class names",
            "Pass 2 — CSS rule blocks in project stylesheet(s)",
        ],
    }
    out_path = out_dir / "accent-contrast-report.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Human-readable output
    print("Accent contrast advisory scan (light + dark mode)")
    print(f"  HTML files scanned : {html_scanned}")
    print(f"  CSS files scanned  : {css_scanned}")
    print(f"  Advisories         : {len(advisories)}")
    print(f"  Info notes         : {len(infos)}")
    print(f"  Report             : {out_path}")

    # Print mode palette summary
    lw, lh = _worst_accent_light()
    dw, dh = _worst_accent_dark()
    print(f"\n  Light-mode palette : accent {lh} / bg {LIGHT_MODE['bg']} → {lw:.2f}:1")
    print(f"  Dark-mode palette  : accent {dh} / surface {DARK_MODE['surface']} → {dw:.2f}:1")

    if advisories:
        print("\nAdvisories (accent color on body-text elements):")
        for f in advisories:
            loc = f.get("selector") or f.get("tag", "unknown")
            print(f"  [ADVISORY] {f['file']}:{f['line']} — {loc}")
            print(f"    Rule     : {f['rule']}")
            print(f"    Detail   : {f['detail']}")
            print(f"    Snippet  : {f['snippet']}")
            lc = f.get("light_contrast", "?")
            dc = f.get("dark_contrast", "?")
            print(f"    Ratios   : light {lc}:1 / dark {dc}:1")
            fsh = f.get("font_size_hint")
            if fsh:
                print(f"    Font size: {fsh}")
            print()
    else:
        print("\n  No body-text accent color violations found.")

    if infos:
        print("Info notes (context-dependent -- review manually):")
        for f in infos:
            loc = f.get("selector") or f.get("tag", "unknown")
            lc = f.get("light_contrast", "?")
            dc = f.get("dark_contrast", "?")
            print(f"  [INFO] {f['file']}:{f['line']} {loc} -- {f['rule']} "
                  f"(light {lc}:1 / dark {dc}:1)")

    print()
    print("This script is advisory only. Exit 0 regardless of findings.")
    print("Use --strict to exit 1 on any advisory (for manual gate use).")

    if strict and advisories:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
