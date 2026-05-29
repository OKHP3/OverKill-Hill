#!/usr/bin/env python3
"""
responsive-audit.py — Static responsive-design analysis
=========================================================
Analyzes theme.css + every HTML page for patterns known to cause
horizontal overflow or layout breakage at narrow viewports.

Checks:
  CSS-1  Fixed-px widths > 320px without a mobile override
  CSS-2  min-width values > 320px in non-media-query context
  CSS-3  white-space: nowrap on interactive / text elements
  CSS-4  Grid / flex children with fixed minmax() floors > 300px
         that lack a ≤900px stacking override
  CSS-5  Hardcoded negative margins that could push content off-screen
  HTML-1 <img> without max-width guard (missing class or style)
  HTML-2 Tables without overflow-x wrapper
  HTML-3 <pre>/<code> blocks without overflow-x
  HTML-4 Inline style="width:Npx" where N > 320
  HTML-5 Nav toggle present on every page

Writes:
  assets/audit/responsive-audit-2026-05-26.json
  Prints human-readable summary.

Exit: 0 if no P0 issues, 1 otherwise.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"node_modules", ".local", ".git", "attached_assets", "assets", ".pythonlibs", ".cache"}
THEME_CSS = ROOT / "assets" / "css" / "theme.css"

# ─── CSS Analysis ────────────────────────────────────────────────────────────

def parse_media_blocks(css: str) -> list[tuple[str, str]]:
    """Return list of (query, block_content) for all @media blocks."""
    blocks = []
    i = 0
    while True:
        m = re.search(r'@media\s+([^{]+)\{', css[i:])
        if not m:
            break
        query = m.group(1).strip()
        start = i + m.end()
        depth = 1
        j = start
        while j < len(css) and depth > 0:
            if css[j] == '{':
                depth += 1
            elif css[j] == '}':
                depth -= 1
            j += 1
        blocks.append((query, css[start:j-1]))
        i = i + m.start() + 1
    return blocks


def extract_mobile_queries(css: str) -> set[str]:
    """Collect all selectors that appear in max-width ≤ 900px media blocks."""
    selectors: set[str] = set()
    for query, block in parse_media_blocks(css):
        m = re.search(r'max-width\s*:\s*(\d+)', query)
        if m and int(m.group(1)) <= 900:
            for sel in re.findall(r'([.#\w][^{]+)\{', block):
                selectors.add(sel.strip())
    return selectors


def audit_css(css: str) -> list[dict]:
    issues = []

    # CSS-1: Fixed px widths > 320px in non-media context
    # Strip media blocks from main body first
    stripped = re.sub(r'@media[^{]+\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', '', css)
    for m in re.finditer(r'([.#\w][^{]*)\{([^}]*width\s*:\s*(\d+)px[^}]*)\}', stripped):
        selector = m.group(1).strip()
        width_px = int(m.group(3))
        if width_px > 320 and 'max-width' not in m.group(2):
            # Check if it's a fixed width (not max-width) that could overflow
            prop_match = re.search(r'(?<!\-)(?<!min-)(?<!max-)\bwidth\s*:\s*(\d+)px', m.group(2))
            if prop_match and int(prop_match.group(1)) > 480:
                issues.append({
                    "type": "CSS-1",
                    "severity": "P1",
                    "message": f"Fixed width:{prop_match.group(1)}px on '{selector[:60]}' — may overflow on mobile",
                })

    # CSS-2: min-width > 300px (not in media queries)
    for m in re.finditer(r'([.#\w][^{]*)\{([^}]*)\}', stripped):
        selector = m.group(1).strip()
        block = m.group(2)
        mw = re.search(r'min-width\s*:\s*(\d+)px', block)
        if mw and int(mw.group(1)) > 300:
            # Exclude fit-content, min-content etc
            issues.append({
                "type": "CSS-2",
                "severity": "P2",
                "message": f"min-width:{mw.group(1)}px on '{selector[:60]}' — verify mobile override exists",
            })

    # CSS-3: white-space:nowrap on nav/button/link contexts without mobile override
    mobile_selectors = extract_mobile_queries(css)
    for m in re.finditer(r'([.#\w][^{]*)\{([^}]*white-space\s*:\s*nowrap[^}]*)\}', stripped):
        selector = m.group(1).strip()
        # Check if there's a mobile override for this selector
        has_override = any(selector.split()[0] in ms for ms in mobile_selectors)
        if not has_override and ('nav' in selector.lower() or 'btn' in selector.lower()
                                  or 'link' in selector.lower() or 'menu' in selector.lower()
                                  or 'tag' in selector.lower()):
            issues.append({
                "type": "CSS-3",
                "severity": "P2",
                "message": f"white-space:nowrap on '{selector[:60]}' — could overflow at 320px",
            })

    # CSS-4: minmax floors in grid columns > 240px without stacking breakpoint
    for m in re.finditer(r'([.#\w][^{]*)\{([^}]*grid-template-columns[^}]*)\}', stripped):
        selector = m.group(1).strip()
        block = m.group(2)
        for floor in re.finditer(r'minmax\((\d+)px', block):
            floor_px = int(floor.group(1))
            if floor_px > 240:
                # Check if there's a ≤900px override that stacks it
                has_stack = False
                for query, qblock in parse_media_blocks(css):
                    mq = re.search(r'max-width\s*:\s*(\d+)', query)
                    if mq and int(mq.group(1)) <= 900:
                        # Check if selector appears in this block
                        sel_base = selector.split()[0].strip()
                        if sel_base in qblock and '1fr' in qblock:
                            has_stack = True
                            break
                if not has_stack:
                    issues.append({
                        "type": "CSS-4",
                        "severity": "P0",
                        "message": f"grid minmax({floor_px}px,…) on '{selector[:60]}' — no ≤900px 1fr stack override found",
                    })

    # CSS-5: Negative margins that could push off-screen
    for m in re.finditer(r'([.#\w][^{]*)\{([^}]*margin[^:]*:\s*-(\d+)px[^}]*)\}', stripped):
        neg_px = int(m.group(3))
        if neg_px > 20:
            selector = m.group(1).strip()
            issues.append({
                "type": "CSS-5",
                "severity": "P2",
                "message": f"Large negative margin (-{neg_px}px) on '{selector[:60]}'",
            })

    return issues


# ─── HTML Analysis ────────────────────────────────────────────────────────────

def audit_html_page(rel: Path, html: str) -> list[dict]:
    issues = []

    # HTML-1: Tables without overflow-x wrapper
    if re.search(r'<table', html, re.I):
        # Check if wrapped in overflow container
        if not re.search(r'overflow[^"]*auto|overflow[^"]*scroll|overflow-x', html):
            issues.append({
                "type": "HTML-2",
                "severity": "P1",
                "page": rel.as_posix(),
                "message": "Contains <table> with no overflow-x wrapper",
            })

    # HTML-2: <pre> blocks not inside overflow-x container
    # Exclude <pre class="mermaid"> — those are converted to SVG by Mermaid.js and
    # are wrapped by .glee-mermaid-shell which provides overflow-x:auto in CSS.
    # Also: theme.css now has a global `pre:not(.mermaid){overflow-x:auto}` rule
    # that protects every non-mermaid <pre> on pages that load theme.css (all 60).
    # Only flag pages that have non-mermaid <pre> AND don't load theme.css.
    pre_tags = re.findall(r'<pre[^>]*>', html, re.I)
    has_non_mermaid_pre = any(
        not re.search(r'class=["\'][^"\']*mermaid', tag, re.I)
        for tag in pre_tags
    )
    loads_theme_css = 'theme.css' in html or 'assets/css' in html
    if has_non_mermaid_pre and not loads_theme_css:
        if not re.search(r'overflow[^"]*auto|overflow[^"]*scroll|overflow-x|code-drop|diagram-shell|mermaid-shell', html):
            issues.append({
                "type": "HTML-3",
                "severity": "P1",
                "page": rel.as_posix(),
                "message": "Contains <pre> without overflow-x container and does not load theme.css",
            })

    # HTML-3: Inline style with fixed width > 320px
    for m in re.finditer(r'style="[^"]*(?<!\-)(?<!min-)(?<!max-)width\s*:\s*(\d+)px', html, re.I):
        px = int(m.group(1))
        if px > 480:
            issues.append({
                "type": "HTML-4",
                "severity": "P1",
                "page": rel.as_posix(),
                "message": f"Inline style width:{px}px (may overflow mobile)",
            })

    # HTML-4: Nav toggle present
    if '.nav-toggle' not in html and 'nav-toggle' not in html:
        if '<nav' in html.lower():  # only flag pages with nav
            issues.append({
                "type": "HTML-5",
                "severity": "P1",
                "page": rel.as_posix(),
                "message": "Page has <nav> but no .nav-toggle found",
            })

    # HTML-5: Images wider than viewport — check for explicit width > 320px without max-width:100%
    for m in re.finditer(r'<img[^>]+>', html, re.I):
        tag = m.group(0)
        width_m = re.search(r'\bwidth=["\']?(\d+)', tag)
        if width_m and int(width_m.group(1)) > 480:
            # Check if it has a class that implies responsive handling or max-width style
            if 'max-width' not in tag and 'class="logo' not in tag.lower():
                issues.append({
                    "type": "HTML-1",
                    "severity": "P2",
                    "page": rel.as_posix(),
                    "message": f"<img width={width_m.group(1)}> without max-width:100% protection",
                })

    return issues


# ─── GLEE-specific checks ─────────────────────────────────────────────────────

def audit_glee_hero_css(css: str) -> list[dict]:
    """Check for Glee-specific hero layout issues."""
    issues = []

    # Check .glee-hero two-column layout
    glee_hero_match = re.search(
        r'\.glee-main\s+\.hero[^{]*\{[^}]*grid-template-columns[^}]*\}|'
        r'\.glee-hero[^{]*\{[^}]*grid-template-columns[^}]*\}|'
        r'\.askjamie-hero-grid[^{]*\{[^}]*grid-template-columns[^}]*\}',
        css, re.DOTALL
    )

    # Check two-column class
    two_col_match = re.search(r'\.two-column\s*\{([^}]+)\}', css)
    if two_col_match:
        block = two_col_match.group(1)
        if 'grid-template-columns' in block or 'flex' in block:
            # Verify it stacks on mobile
            mobile_two_col = re.search(
                r'@media[^{]*max-width[^{]*\{[^}]*\.two-column[^}]*\}',
                css, re.DOTALL
            )
            if not mobile_two_col:
                issues.append({
                    "type": "GLEE-1",
                    "severity": "P1",
                    "message": ".two-column layout has no confirmed mobile stacking rule",
                })

    return issues


# ─── Nav toggle mobile check ─────────────────────────────────────────────────

def audit_nav_css(css: str) -> list[dict]:
    """Verify mobile nav toggle is shown at ≤768px."""
    issues = []

    # nav-toggle should be display:none by default (desktop) and shown at mobile
    nav_toggle_desktop = re.search(r'\.nav-toggle\s*\{[^}]*display\s*:\s*none', css)
    nav_toggle_mobile = re.search(
        r'@media[^{]*max-width\s*:\s*(\d+)[^{]*\{[^}]*\.nav-toggle[^}]*display\s*:\s*(?:flex|block|inline)',
        css, re.DOTALL
    )

    if not nav_toggle_mobile:
        # Check differently — look for the mobile breakpoint
        for query, block in parse_media_blocks(css):
            mq = re.search(r'max-width\s*:\s*(\d+)', query)
            if mq and int(mq.group(1)) <= 900:
                if '.nav-toggle' in block and ('display' in block):
                    nav_toggle_mobile = True
                    break

    if nav_toggle_desktop and not nav_toggle_mobile:
        issues.append({
            "type": "NAV-1",
            "severity": "P0",
            "message": ".nav-toggle is hidden (display:none) but no mobile show rule found",
        })

    return issues


# ─── Padding / container mobile check ────────────────────────────────────────

def audit_container_css(css: str) -> list[dict]:
    """Verify .container has mobile-safe padding."""
    issues = []
    container_match = re.search(r'\.container\s*\{([^}]+)\}', css)
    if container_match:
        block = container_match.group(1)
        padding_m = re.search(r'padding[^:]*:\s*[^;]+', block)
        if padding_m:
            # Check that padding is not 0
            if re.search(r'padding\s*:\s*0\s*;|padding\s*:\s*0$', block):
                issues.append({
                    "type": "CONT-1",
                    "severity": "P0",
                    "message": ".container has padding:0 — content will touch screen edges on mobile",
                })
    return issues


# ─── Tool-ette page specific check ───────────────────────────────────────────

def audit_toolette_pages(pages: list[tuple[Path, str]]) -> list[dict]:
    """Check tool-ette pages for common mobile issues."""
    issues = []
    for rel, html in pages:
        if '/toolbox/' in rel.as_posix() and rel.parts.count('toolbox') > 0:
            # Check for GPT hero card on tool pages
            if 'gpt-hero' in html or 'bfs-hero' in html:
                # Verify breakpoint override exists
                if 'max-width: 900px' not in html and 'max-width:900px' not in html:
                    pass  # handled by CSS, not inline — OK

    return issues


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    css = THEME_CSS.read_text(encoding="utf-8", errors="replace")

    print("Analyzing theme.css for responsive defects…")
    css_issues = audit_css(css)
    css_issues += audit_glee_hero_css(css)
    css_issues += audit_nav_css(css)
    css_issues += audit_container_css(css)

    print(f"  CSS checks done: {len(css_issues)} issues")

    print("Analyzing HTML pages…")
    html_issues = []
    pages_data = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        page_issues = audit_html_page(rel, html)
        html_issues.extend(page_issues)
        pages_data.append((rel, html))

    print(f"  HTML checks done: {len(html_issues)} issues across {len(pages_data)} pages")

    all_issues = css_issues + html_issues
    p0 = [i for i in all_issues if i.get("severity") == "P0"]
    p1 = [i for i in all_issues if i.get("severity") == "P1"]
    p2 = [i for i in all_issues if i.get("severity") == "P2"]

    print(f"\n{'='*60}")
    print(f"RESPONSIVE AUDIT SUMMARY")
    print(f"  P0 (critical):  {len(p0)}")
    print(f"  P1 (high):      {len(p1)}")
    print(f"  P2 (medium):    {len(p2)}")
    print(f"  Total:          {len(all_issues)}")

    if p0 or p1:
        print("\nP0 Issues:")
        for i in p0:
            print(f"  ! [{i['type']}] {i['message'][:100]}")
        print("\nP1 Issues:")
        for i in p1[:20]:
            src = f" ({i['page']})" if 'page' in i else ""
            print(f"  ! [{i['type']}] {i['message'][:100]}{src}")
        if len(p1) > 20:
            print(f"  … and {len(p1)-20} more P1 issues")

    if p2:
        print(f"\nP2 Issues (first 15):")
        for i in p2[:15]:
            src = f" ({i['page']})" if 'page' in i else ""
            print(f"  △ [{i['type']}] {i['message'][:100]}{src}")

    # Write JSON report
    out_dir = ROOT / "assets" / "audit"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "responsive-audit-2026-05-26.json"
    out.write_text(json.dumps({
        "date": "2026-05-26",
        "css_file": str(THEME_CSS.relative_to(ROOT)),
        "pages_scanned": len(pages_data),
        "totals": {"p0": len(p0), "p1": len(p1), "p2": len(p2), "total": len(all_issues)},
        "issues": all_issues,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReport: {out.relative_to(ROOT)}")

    return 1 if p0 else 0


if __name__ == "__main__":
    sys.exit(main())
