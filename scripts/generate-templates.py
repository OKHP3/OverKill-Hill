#!/usr/bin/env python3
"""
generate-templates.py
Glee-fully Tools — Template Library Generator
=============================================
Reads every site HTML page, strips page-specific content, and writes
structural templates to ``assets/templates/`` mirroring the site
hierarchy.

Run from the repo root. Idempotent — skips pages that already have a
template (use ``--force`` to overwrite).

Per the spec (GLEE-FULLY-TOOLS-FINAL-SESSION-TASK):
  • PRESERVE: <head>, <nav>, <footer>, <script>, all classes/data/aria,
    skip-to-content, <main id="main"> wrapper, layout containers.
  • REPLACE: page-specific text/URLs/images with {{TOKEN}} placeholders.
  • Nav logo image (Glee-fullyTools ButterflyWaiting…) is structural —
    do NOT tokenize it.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = REPO_ROOT / "assets" / "templates"

# Path prefixes (relative to REPO_ROOT) that are NEVER scanned.
EXCLUDE_PREFIXES = (
    "assets/",          # includes assets/templates/ — prevents recursion
    "attached_assets/",
    "scripts/",
    "audit/",
    ".agents/",
    ".github/",
    ".vscode/",
    ".local/",
    ".git/",
    "node_modules/",
)

# Image src substrings that are STRUCTURAL (nav/footer logos) — keep verbatim.
NAV_LOGO_PATTERNS = (
    "ButterflyWaiting",
    "ButterflyLoopLeft",
    "favicon",
)


# ── Placeholder substitution rules ───────────────────────────────────────────
def strip_to_template(html: str, source_path: str) -> str:
    """Apply all placeholder substitutions to produce a template."""
    # 1. Insert template header comment right after <html …>
    header_comment = (
        "\n<!--\n"
        "  GLEE-FULLY TOOLS™ — PAGE TEMPLATE\n"
        f"  Source page: {source_path}\n"
        "  Template created: 2026-05-03\n"
        f"  Template location: assets/templates/{source_path}\n"
        "\n"
        "  USAGE:\n"
        "  1. Copy this file to the target page location.\n"
        "  2. Replace all {{PLACEHOLDER}} tokens with actual content.\n"
        "  3. Update <link rel=\"canonical\"> + og:url + og:image values.\n"
        "  4. Replace {{CONTENT_IMAGE_PATH}} with paths under /assets/img/.\n"
        "  5. Test in a browser before committing.\n"
        "\n"
        "  PLACEHOLDER INDEX:\n"
        "  {{PAGE_TITLE}}         — Short page name (e.g., \"Menu Conductor\")\n"
        "  {{PAGE_HEADING}}       — H1 text displayed on page\n"
        "  {{PAGE_SUBHEADING}}    — Subtitle / deck below H1\n"
        "  {{META_DESCRIPTION}}   — 140–160 char SEO description\n"
        "  {{OG_TITLE}}           — Open Graph title\n"
        "  {{OG_DESCRIPTION}}     — Open Graph description\n"
        "  {{OG_IMAGE_URL}}       — Absolute URL to 1200x630 image\n"
        "  {{CANONICAL_URL}}      — Full absolute URL\n"
        "  {{CONTENT_IMAGE_PATH}} — Path to hero/content image\n"
        "  {{CONTENT_IMAGE_ALT}}  — Descriptive alt text\n"
        "  {{TOOL_NAME}}          — Tool / Tool-ette / GPT name\n"
        "  {{CTA_LABEL}}          — Button label text\n"
        "  {{CTA_URL}}            — Button destination URL\n"
        "  {{SECTION_HEADING}}    — H2/H3/H4 text\n"
        "  {{SECTION_BODY}}       — Section paragraph text\n"
        "  {{BODY_COPY}}          — Body paragraph content\n"
        "  {{BREADCRUMB_LABEL}}   — Breadcrumb segment name\n"
        "  {{BREADCRUMB_URL}}     — Breadcrumb segment URL\n"
        "  {{SPARKLE_TEXT}}       — \"Today's Sparkle\" text (if present)\n"
        "  {{SPARKLE_URL}}        — \"Today's Sparkle\" link (if present)\n"
        "-->\n"
    )
    html = re.sub(r"(<html\b[^>]*>)", r"\1" + header_comment, html, count=1)

    # 2. <title>
    html = re.sub(
        r"(<title>)([^<]+)(</title>)",
        r"\1{{PAGE_TITLE}} — Glee-fully Personalizable Tools™\3",
        html,
    )

    # 3. Meta tags (description / og:* / twitter:*)
    meta_subs = [
        (r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']+)(["\'])',
         r"\1{{META_DESCRIPTION}}\3"),
        (r'(<meta\s+property=["\']og:title["\']\s+content=["\'])([^"\']+)(["\'])',
         r"\1{{OG_TITLE}}\3"),
        (r'(<meta\s+property=["\']og:description["\']\s+content=["\'])([^"\']+)(["\'])',
         r"\1{{OG_DESCRIPTION}}\3"),
        (r'(<meta\s+property=["\']og:url["\']\s+content=["\'])([^"\']+)(["\'])',
         r"\1{{CANONICAL_URL}}\3"),
        (r'(<meta\s+property=["\']og:image["\']\s+content=["\'])([^"\']+)(["\'])',
         r"\1{{OG_IMAGE_URL}}\3"),
        (r'(<meta\s+(?:name|property)=["\']twitter:title["\']\s+content=["\'])([^"\']+)(["\'])',
         r"\1{{PAGE_TITLE}}\3"),
        (r'(<meta\s+(?:name|property)=["\']twitter:description["\']\s+content=["\'])([^"\']+)(["\'])',
         r"\1{{META_DESCRIPTION}}\3"),
        (r'(<meta\s+(?:name|property)=["\']twitter:image["\']\s+content=["\'])([^"\']+)(["\'])',
         r"\1{{OG_IMAGE_URL}}\3"),
    ]
    for pattern, repl in meta_subs:
        html = re.sub(pattern, repl, html)

    # 4. <link rel="canonical">
    html = re.sub(
        r'(<link\s+rel=["\']canonical["\']\s+href=["\'])([^"\']+)(["\'])',
        r"\1{{CANONICAL_URL}}\3",
        html,
    )

    # 5. JSON-LD — page-specific name/description/url/image values
    def strip_jsonld(m: re.Match) -> str:
        block = m.group(0)
        # name → only when value is NOT immediately followed by "@type" (avoid clobbering Org names)
        block = re.sub(
            r'("name"\s*:\s*")[^"]+(")',
            r'\1{{PAGE_TITLE}}\2',
            block,
        )
        block = re.sub(
            r'("description"\s*:\s*")[^"]+(")',
            r'\1{{META_DESCRIPTION}}\2',
            block,
        )
        block = re.sub(
            r'("url"\s*:\s*")https://glee-fully\.tools[^"]*(")',
            r'\1{{CANONICAL_URL}}\2',
            block,
        )
        block = re.sub(
            r'("image"\s*:\s*")https://glee-fully\.tools[^"]*(")',
            r'\1{{OG_IMAGE_URL}}\2',
            block,
        )
        return block

    html = re.sub(
        r'<script\s+type=["\']application/ld\+json["\']>.*?</script>',
        strip_jsonld,
        html,
        flags=re.DOTALL,
    )

    # 6. Hero <h1> inside <main> — replace inner text (first occurrence only)
    html = re.sub(
        r'(<main\b[^>]*>.*?<h1\b[^>]*>)([^<]+)(</h1>)',
        r"\1{{PAGE_HEADING}}\3",
        html,
        count=1,
        flags=re.DOTALL,
    )

    # 7. Content image src — replace if NOT a structural nav/footer logo
    def img_src_repl(m: re.Match) -> str:
        src = m.group(1)
        if any(p in src for p in NAV_LOGO_PATTERNS):
            return m.group(0)
        return f'src="{{{{CONTENT_IMAGE_PATH}}}}"'

    html = re.sub(
        r'src=["\']([^"\']*assets/img[^"\']+)["\']',
        img_src_repl,
        html,
    )

    # 8. Content image alt (≥5 chars; preserve empty/decorative)
    def alt_repl(m: re.Match) -> str:
        # Skip alts on structural images that we already left alone.
        return f'{m.group(1)}{{{{CONTENT_IMAGE_ALT}}}}{m.group(3)}'

    # Only swap alt where preceding src already became {{CONTENT_IMAGE_PATH}}.
    # Pattern catches the alt within the same <img …> tag.
    html = re.sub(
        r'(<img\b[^>]*src=["\']\{\{CONTENT_IMAGE_PATH\}\}["\'][^>]*?\balt=["\'])([^"\']+)(["\'])',
        alt_repl,
        html,
    )
    html = re.sub(
        r'(<img\b[^>]*?\balt=["\'])([^"\']+)(["\'][^>]*src=["\']\{\{CONTENT_IMAGE_PATH\}\}["\'])',
        alt_repl,
        html,
    )

    return html


# ── Discovery ────────────────────────────────────────────────────────────────
def find_all_pages() -> list[Path]:
    pages: list[Path] = []
    for path in REPO_ROOT.rglob("*.html"):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if any(rel.startswith(ex) for ex in EXCLUDE_PREFIXES):
            continue
        pages.append(path)
    return sorted(pages)


# ── Manifest ─────────────────────────────────────────────────────────────────
def classify(rel: str) -> str:
    parts = rel.split("/")
    if rel == "index.html":
        return "Homepage"
    if rel == "404.html":
        return "Error page"
    if rel == "under-construction.html":
        return "Under construction"
    if parts[0] == "toolbox":
        if len(parts) == 2:        # toolbox/index.html
            return "Toolbox hub (CollectionPage)"
        if len(parts) == 3:        # toolbox/<branch>/index.html
            return "Tool Branch (CollectionPage)"
        return "Tool-ette (SoftwareApplication)"
    if parts[0] == "search":
        return "Search page (SearchResultsPage)"
    if parts[0] in {"about", "contact", "legal", "persona",
                    "ecosystem", "universe"}:
        return "Supporting page (WebPage)"
    return "Supporting page (WebPage)"


def write_manifest(processed: list[str]) -> Path:
    manifest = TEMPLATE_ROOT / "TEMPLATE_INDEX.md"
    lines = [
        "# Glee-fully Tools — Template Library Index",
        "",
        f"Generated: 2026-05-03  |  Total templates: {len(processed)}",
        "",
        "## Usage",
        "",
        "Copy any template from this folder to its target location in the site",
        "hierarchy.  Replace every `{{PLACEHOLDER}}` token with real content",
        "before committing.  See the comment block at the top of each template",
        "for the full placeholder index.",
        "",
        "These templates are **development artifacts**, not crawlable pages —",
        "they are excluded from `sitemap.xml` and from every site-validator in",
        "`scripts/` (the validators skip the whole `assets/` tree).",
        "",
        "## Template Inventory",
        "",
        "| Template Path | Page Type |",
        "|---|---|",
    ]
    for rel in sorted(processed):
        lines.append(f"| `assets/templates/{rel}` | {classify(rel)} |")
    lines.append("")
    manifest.write_text("\n".join(lines), encoding="utf-8")
    return manifest


# ── Main ────────────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing template files.")
    args = parser.parse_args()

    TEMPLATE_ROOT.mkdir(parents=True, exist_ok=True)

    pages = find_all_pages()
    print(f"Found {len(pages)} HTML source pages\n")

    created: list[str] = []
    overwritten: list[str] = []
    skipped: list[str] = []

    for page in pages:
        rel = page.relative_to(REPO_ROOT).as_posix()
        template_path = TEMPLATE_ROOT / rel

        if template_path.exists() and not args.force:
            skipped.append(rel)
            continue

        try:
            source_html = page.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:                     # pragma: no cover
            print(f"  ERROR reading {rel}: {exc}", file=sys.stderr)
            continue

        template_html = strip_to_template(source_html, rel)
        template_path.parent.mkdir(parents=True, exist_ok=True)
        existed = template_path.exists()
        template_path.write_text(template_html, encoding="utf-8")
        if existed:
            overwritten.append(rel)
            print(f"  OVERWRITTEN: assets/templates/{rel}")
        else:
            created.append(rel)
            print(f"  CREATED:     assets/templates/{rel}")

    all_processed = created + overwritten + skipped
    manifest = write_manifest(all_processed)

    print("\n" + "=" * 60)
    print(f"Templates created:     {len(created)}")
    print(f"Templates overwritten: {len(overwritten)}  (--force)")
    print(f"Templates skipped:     {len(skipped)}  (already existed)")
    print(f"Total in library:      {len(all_processed)}")
    print(f"Manifest:              {manifest.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
