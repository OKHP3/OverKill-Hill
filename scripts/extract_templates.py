#!/usr/bin/env python3
"""
extract_templates.py — derives stripped layout templates from live pages.

For every (donor, template_name, covered_pages) tuple in TEMPLATES, copies
the donor HTML, applies tag-targeted strip transforms (BeautifulSoup), then
writes the result to assets/templates/<template_name>.

Idempotent: re-running on already-stripped templates is a no-op (placeholders
match themselves).

Usage:
    python3 scripts/extract_templates.py            # build all templates
    python3 scripts/extract_templates.py --check    # dry-run, summarise diffs
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

ROOT = Path(__file__).resolve().parent.parent
TPL_DIR = ROOT / "assets" / "templates"

TEMPLATES = [
    # (donor_path, template_filename, [covered_pages], layout_label)
    ("index.html", "home-template.html", ["/"], "Homepage"),
    ("writings/index.html", "writings-hub-template.html",
     ["/writings/"], "Content hub / index"),
    ("writings/biases-as-constants/index.html", "writings-article-template.html",
     ["/writings/biases-as-constants/", "/writings/magnus-saga/",
      "/writings/first-diagram-is-a-liar/"], "Long-form article"),
    ("writings/first-diagram-is-a-liar/v03/v1-heat-a/index.html",
     "writings-article-study-template.html",
     ["/writings/first-diagram-is-a-liar/v03/v1-heat-a/",
      "/writings/first-diagram-is-a-liar/v03/v1-heat-b/",
      "/writings/first-diagram-is-a-liar/v03/v2-heat-a/",
      "/writings/first-diagram-is-a-liar/v03/v2-heat-b/"],
     "Article variant / heat-test study"),
    ("projects/index.html", "projects-hub-template.html",
     ["/projects/"], "Content hub / index"),
    ("projects/hometools/index.html", "projects-project-template.html",
     ["/projects/abrahamic-reference-engine/",
      "/projects/bfs-framing-intelligent-futures/",
      "/projects/hometools/",
      "/projects/mermaid-theme-builder/",
      "/projects/pathscrib-r/",
      "/projects/un-nocked-truth/"],
     "Individual project page"),
    ("universe/index.html", "universe-template.html",
     ["/universe/"], "Brand universe"),
    ("about/index.html", "about-template.html",
     ["/about/"], "About / brand page"),
    ("contact/index.html", "contact-template.html",
     ["/contact/"], "Contact / form page"),
    ("legal/index.html", "legal-template.html",
     ["/legal/"], "Legal / policy page"),
    ("manifesto/index.html", "manifesto-template.html",
     ["/manifesto/"], "Manifesto / editorial"),
    ("prompt-forge/index.html", "prompt-forge-template.html",
     ["/prompt-forge/"], "Tool / resource page"),
    ("found-ry/index.html", "found-ry-template.html",
     ["/found-ry/"], "Foundry / studio brand page"),
    ("search/index.html", "search-template.html",
     ["/search/"], "Search results / utility page"),
    ("404.html", "404-template.html",
     ["/404.html"], "Error page"),
    ("under-construction.html", "under-construction-template.html",
     ["/under-construction.html"], "Placeholder / stub"),
]

# ---------------------------------------------------------------------------
# Meta tag swaps (head). Each entry: (selector_dict, content_placeholder).
META_SWAPS = [
    ({"name": "description"}, "[PAGE META DESCRIPTION — 120-160 chars]"),
    ({"property": "og:title"}, "[OG TITLE]"),
    ({"property": "og:description"}, "[OG DESCRIPTION]"),
    ({"property": "og:url"}, "[CANONICAL URL]"),
    ({"property": "og:image"}, "[OG IMAGE PATH]"),
    ({"property": "og:image:alt"}, "[OG IMAGE ALT]"),
    ({"property": "article:published_time"}, "[PUBLICATION DATE]"),
    ({"property": "article:modified_time"}, "[MODIFICATION DATE]"),
    ({"property": "article:author"}, "[AUTHOR NAME]"),
    ({"name": "twitter:title"}, "[TWITTER TITLE]"),
    ({"name": "twitter:description"}, "[TWITTER DESCRIPTION]"),
    ({"name": "twitter:image"}, "[OG IMAGE PATH]"),
    ({"name": "twitter:image:alt"}, "[OG IMAGE ALT]"),
    ({"name": "author"}, "[AUTHOR NAME]"),
]

# Class hints that mark "chrome" regions whose visible text should NOT be stripped.
# These are the explicit site-frame containers — <header class="section-header">,
# <header class="article-hero">, etc. are CONTENT and must be stripped.
CHROME_CONTAINER_CLASSES = {
    "site-header", "site-nav", "site-footer", "primary-nav",
    "skip-link", "site-specials", "site-banner", "main-nav",
    "footer", "global-nav", "global-header", "global-footer",
}
# Tags that are *always* chrome regardless of class. <header> is intentionally
# NOT in this set: pages frequently use <header> as a content section header,
# so we require an explicit chrome class to qualify.
CHROME_TAGS = {"nav", "footer"}


def in_chrome(tag: Tag) -> bool:
    """True if tag is inside the site frame (header/nav/footer chrome)."""
    for parent in tag.parents:
        if not isinstance(parent, Tag):
            continue
        if parent.name in CHROME_TAGS:
            return True
        classes = set(parent.get("class") or [])
        if classes & CHROME_CONTAINER_CLASSES:
            return True
        # <header> only counts as chrome when it carries an explicit
        # site-chrome class (handled by the CHROME_CONTAINER_CLASSES check
        # above). Bare <header> or <header class="section-header"> is content.
    return False


# ---------------------------------------------------------------------------
# Asset path normalisation. Templates live at /assets/templates/<name>.html and
# must use root-relative paths so they resolve correctly from any depth.

LOCAL_ASSET_RE = re.compile(
    r"""^(?!https?:|//|/|#|mailto:|tel:|data:|javascript:)"""
    r"""(assets/|favicon\.ico|site\.webmanifest|sitemap\.xml|robots\.txt)""",
    re.IGNORECASE,
)


def normalise_asset_path(value: str) -> str:
    """Prefix '/' to bare local asset references so they're root-relative."""
    if not value:
        return value
    if LOCAL_ASSET_RE.match(value):
        return "/" + value
    return value


def normalise_srcset(value: str) -> str:
    """Apply normalise_asset_path to every URL in a srcset attribute."""
    parts = []
    for entry in value.split(","):
        entry = entry.strip()
        if not entry:
            continue
        bits = entry.split(None, 1)
        bits[0] = normalise_asset_path(bits[0])
        parts.append(" ".join(bits))
    return ", ".join(parts)


def normalise_all_assets(soup: BeautifulSoup) -> None:
    """Walk the whole document and convert local asset refs to root-relative."""
    for el in soup.find_all(href=True):
        el["href"] = normalise_asset_path(el["href"])
    for el in soup.find_all(src=True):
        el["src"] = normalise_asset_path(el["src"])
    for el in soup.find_all(srcset=True):
        el["srcset"] = normalise_srcset(el["srcset"])
    # CSS url() inside inline <style>
    for style in soup.find_all("style"):
        if style.string:
            style.string = re.sub(
                r"""url\((['"]?)(?!https?:|//|/|data:)(assets/[^'")\s]+)\1\)""",
                lambda m: f"url({m.group(1)}/{m.group(2)}{m.group(1)})",
                style.string,
            )


def replace_text(tag: Tag, placeholder: str) -> None:
    """Empty a tag's children and insert a single placeholder text node."""
    tag.clear()
    tag.append(NavigableString(placeholder))


def strip_inline_links_to_placeholder(tag: Tag) -> None:
    """In-content <a href=...> → href becomes [LINK URL] (text preserved)."""
    for a in tag.find_all("a", href=True):
        if in_chrome(a):
            continue
        href = a["href"]
        # Preserve in-page anchors (they're structural to the page outline)
        if href.startswith("#"):
            continue
        a["href"] = "[LINK URL]"


def scrub_jsonld(script_tag: Tag) -> None:
    """Replace string values in JSON-LD blocks with key-name placeholders."""
    raw = script_tag.string or ""
    raw = raw.strip()
    if not raw:
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return

    PRESERVE_KEYS = {"@context", "@type", "@id"}

    def scrub(node, key_hint=None):
        if isinstance(node, dict):
            return {k: scrub(v, k) for k, v in node.items()}
        if isinstance(node, list):
            return [scrub(v, key_hint) for v in node]
        if isinstance(node, str):
            if key_hint in PRESERVE_KEYS:
                return node
            if key_hint:
                return f"[{key_hint.upper()}]"
            return "[VALUE]"
        return node

    scrubbed = scrub(data)
    script_tag.string = "\n" + json.dumps(scrubbed, indent=2) + "\n"


def strip_template(donor_path: Path, template_name: str,
                   covered_pages: list[str]) -> str:
    html = donor_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    # ---- HEAD ------------------------------------------------------------
    if soup.title:
        replace_text(soup.title, "[PAGE TITLE]")

    for selector, placeholder in META_SWAPS:
        for meta in soup.find_all("meta", attrs=selector):
            meta["content"] = placeholder

    canonical = soup.find("link", attrs={"rel": "canonical"})
    if canonical:
        canonical["href"] = "[CANONICAL URL]"

    # JSON-LD scrub
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        scrub_jsonld(script)

    # ---- BODY: headings --------------------------------------------------
    for h1 in soup.find_all("h1"):
        if not in_chrome(h1):
            replace_text(h1, "[PAGE HEADLINE]")
    for h2 in soup.find_all("h2"):
        if not in_chrome(h2):
            replace_text(h2, "[SECTION HEADING]")
    for h3 in soup.find_all("h3"):
        if not in_chrome(h3):
            replace_text(h3, "[SUBSECTION HEADING]")
    for h4 in soup.find_all("h4"):
        if not in_chrome(h4):
            replace_text(h4, "[H4 HEADING]")

    # ---- BODY: paragraphs (preserve <p> tag, empty body w/ comment) ------
    for p in soup.find_all("p"):
        if in_chrome(p):
            continue
        p.clear()
        p.append(Comment(" [BODY CONTENT] "))

    # ---- BODY: images ----------------------------------------------------
    for img in soup.find_all("img"):
        if in_chrome(img):
            continue
        src = img.get("src", "")
        if "/favicons/" in src or "/og/" in src:
            continue
        ext = Path(src).suffix or ".png"
        img["src"] = f"/assets/img/[IMAGE-FILENAME{ext}]"
        if img.has_attr("srcset"):
            del img["srcset"]
        img["alt"] = "[Descriptive alt text for image]"

    # <picture><source srcset=...><img></picture> — neutralise srcset too
    for source in soup.find_all("source"):
        if in_chrome(source):
            continue
        if source.has_attr("srcset"):
            ext = ".webp" if "webp" in source.get("type", "") else ".png"
            source["srcset"] = f"/assets/img/[IMAGE-FILENAME{ext}]"

    # ---- BODY: in-content links → [LINK URL] -----------------------------
    body = soup.body or soup
    strip_inline_links_to_placeholder(body)

    # ---- BODY: time/byline elements --------------------------------------
    for tm in soup.find_all("time"):
        if in_chrome(tm):
            continue
        if tm.has_attr("datetime"):
            tm["datetime"] = "[ISO DATE]"
        replace_text(tm, "[PUBLICATION DATE]")

    # version badges (heuristic: small text starting with "v" + digit)
    for tag in soup.find_all(class_=re.compile(r"(?i)(version|badge|edition)")):
        if in_chrome(tag):
            continue
        txt = tag.get_text(strip=True)
        if re.match(r"^v\d", txt):
            replace_text(tag, "[VERSION BADGE]")

    # ---- Asset paths: enforce root-relative ------------------------------
    normalise_all_assets(soup)

    # ---- Serialise -------------------------------------------------------
    rendered = str(soup)

    # Insert template comment block right after <!DOCTYPE html>
    today = date.today().strftime("%B %Y")
    consolidated = "Y" if len(covered_pages) > 1 else "N"
    covers_block = "\n                  ".join(covered_pages)
    header_comment = f"""<!--
  =====================================================
  OverKill Hill P³™ — Page Template
  =====================================================
  Template:       {template_name}
  Covers pages:   {covers_block}
  Derived from:   /{donor_path.relative_to(ROOT).as_posix()}
  Created:        {today}
  Last updated:   {today}

  PURPOSE:
  Stripped structural clone of the above page(s). All page-specific
  content replaced with labeled placeholders. Navigation, footer,
  CSS, and JS are live and functional. Use this file as the starting
  point when creating a new page of this layout type.

  USAGE:
  1. Copy this file to the appropriate directory path
  2. Rename to index.html
  3. Replace all [PLACEHOLDER] tokens with real content
  4. Update <head> meta, canonical URL, and OG tags
  5. Commit and deploy

  Consolidated from: {consolidated}{(" — covers " + ", ".join(covered_pages)) if consolidated == "Y" else ""}
  =====================================================
-->
"""
    rendered = re.sub(
        r"^(<!DOCTYPE[^>]+>)\s*",
        lambda m: m.group(1) + "\n" + header_comment,
        rendered, count=1, flags=re.IGNORECASE,
    )
    return rendered


def write_readme(built: list[tuple[str, list[str], str]]) -> None:
    today = date.today().strftime("%B %Y")
    lines = [
        "# OverKill Hill P³™ — Template Library",
        f"**Location:** `/assets/templates/`  ",
        f"**Last updated:** {today}",
        "",
        "## Purpose",
        "Structural clones of every page layout on overkillhill.com, stripped of",
        "page-specific content and ready to use as starting points for new pages.",
        "All templates are complete, valid HTML files. Navigation and footer are",
        "live. CSS and JS are functional. All asset paths are root-relative",
        "(starting with `/`) so they resolve correctly from this subdirectory.",
        "",
        "## Template Inventory",
        "",
        "| Template File | Covers These Pages | Layout Type |",
        "|---|---|---|",
    ]
    for name, pages, label in built:
        pages_str = ", ".join(f"`{p}`" for p in pages)
        lines.append(f"| `{name}` | {pages_str} | {label} |")

    lines += [
        "",
        "## Usage Protocol",
        "1. Identify which template matches the layout type of the page you're building",
        "2. Copy the template file to the correct directory path",
        "3. Rename to `index.html`",
        "4. Replace every `[PLACEHOLDER]` token with real content",
        "5. Populate all `<head>` meta, OG tags, and canonical URL",
        "6. Validate HTML before committing (`python3 scripts/validate_site.py`)",
        "7. Update this README with any new templates added",
        "",
        "## Placeholder Token Reference",
        "| Token | Where Used |",
        "|---|---|",
        "| `[PAGE TITLE]` | `<title>` tag |",
        "| `[PAGE META DESCRIPTION — 120-160 chars]` | `<meta name=\"description\">` |",
        "| `[OG TITLE]` / `[OG DESCRIPTION]` / `[OG IMAGE PATH]` | Open Graph meta |",
        "| `[TWITTER TITLE]` / `[TWITTER DESCRIPTION]` | Twitter card meta |",
        "| `[CANONICAL URL]` | `<link rel=\"canonical\">` and `og:url` |",
        "| `[PAGE HEADLINE]` | First `<h1>` on page |",
        "| `[SECTION HEADING]` | `<h2>` section headers |",
        "| `[SUBSECTION HEADING]` | `<h3>` subheaders |",
        "| `[BODY CONTENT]` | Body `<p>` elements (HTML comment placeholder inside `<p>`) |",
        "| `[IMAGE-FILENAME.ext]` | `<img src>` and `<picture><source srcset>` |",
        "| `[Descriptive alt text for image]` | `<img alt>` attributes |",
        "| `[LINK URL]` | In-content `<a href>` (nav/footer hrefs are preserved) |",
        "| `[PUBLICATION DATE]` / `[ISO DATE]` | Visible dates and `<time datetime>` |",
        "| `[VERSION BADGE]` | Article version indicators (e.g. v0.3) |",
        "| `[AUTHOR NAME]` | Author bylines + `meta name=\"author\"` |",
        "",
        "## What's preserved (chrome)",
        "- Site `<header>`, `<nav>`, and `<footer>` blocks (live links and labels)",
        "- Skip-to-content link",
        "- Hot-forge / announcement banner (`.site-specials`)",
        "- All `<head>` `<link>`/`<script>` references and CSS/JS",
        "- Every layout `<div>`, `<section>`, `<article>`, `<aside>` wrapper and class",
        "- In-page anchor `href=\"#…\"` links (they belong to the page outline)",
        "",
        "## What's stripped (content)",
        "- All `<title>`, meta description, OG, Twitter, canonical values",
        "- Visible `<h1>` / `<h2>` / `<h3>` / `<h4>` text",
        "- All `<p>` body text (tag preserved, content replaced with HTML comment)",
        "- Image `src`, `srcset`, and `alt` (favicons/OG images preserved)",
        "- In-content `<a>` `href` values (text preserved as written)",
        "- `<time>` datetime + visible date text",
        "- JSON-LD string values (replaced with `[KEY_NAME]` placeholders; `@context` / `@type` preserved)",
    ]
    (TPL_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def assert_conformance(name: str, html: str) -> list[str]:
    """Conformance asserts: every template must satisfy the directive's rules.

    Returns a list of violation strings (empty list = pass).
    """
    violations: list[str] = []
    soup = BeautifulSoup(html, "lxml")

    # 1) Every non-chrome heading must be a placeholder.
    expected = {
        "h1": "[PAGE HEADLINE]",
        "h2": "[SECTION HEADING]",
        "h3": "[SUBSECTION HEADING]",
        "h4": "[H4 HEADING]",
    }
    for tag_name, placeholder in expected.items():
        for tag in soup.find_all(tag_name):
            if in_chrome(tag):
                continue
            text = tag.get_text(strip=True)
            if text and text != placeholder:
                violations.append(
                    f"unstripped <{tag_name}>: {text[:60]!r}"
                )

    # 2) Every local asset reference must be root-relative.
    for el in soup.find_all(href=True):
        if LOCAL_ASSET_RE.match(el["href"]):
            violations.append(f"non-root href: {el['href']}")
    for el in soup.find_all(src=True):
        if LOCAL_ASSET_RE.match(el["src"]):
            violations.append(f"non-root src: {el['src']}")
    for el in soup.find_all(srcset=True):
        for entry in el["srcset"].split(","):
            url = entry.strip().split(None, 1)[0]
            if LOCAL_ASSET_RE.match(url):
                violations.append(f"non-root srcset: {url}")

    # 3) Header comment block + DOCTYPE present.
    if not html.lstrip().lower().startswith("<!doctype html>"):
        violations.append("missing <!DOCTYPE html>")
    if "OverKill Hill P³™ — Page Template" not in html:
        violations.append("missing template header comment block")

    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="dry-run; report which templates would change + run conformance asserts")
    args = parser.parse_args()

    TPL_DIR.mkdir(parents=True, exist_ok=True)
    built = []
    changed = 0
    skipped = 0
    total_violations = 0

    for donor_rel, name, pages, label in TEMPLATES:
        donor = ROOT / donor_rel
        if not donor.exists():
            print(f"  ✗ donor missing: {donor_rel}", file=sys.stderr)
            continue
        out = TPL_DIR / name
        rendered = strip_template(donor, name, pages)

        if not args.check:
            if not (out.exists() and out.read_text(encoding="utf-8") == rendered):
                out.write_text(rendered, encoding="utf-8")
                changed += 1
                print(f"  ✓ {name}")
            else:
                skipped += 1
                print(f"  · {name} (unchanged)")
            built.append((name, pages, label))
        else:
            # In --check mode, validate the existing on-disk template (or the
            # freshly-rendered one if file is missing).
            check_html = out.read_text(encoding="utf-8") if out.exists() else rendered
            violations = assert_conformance(name, check_html)
            would_change = not (out.exists() and out.read_text(encoding="utf-8") == rendered)
            status = "~" if would_change else "·"
            print(f"  {status} {name}" + (" (would change)" if would_change else ""))
            for v in violations:
                print(f"      ✗ {v}")
            total_violations += len(violations)
            if would_change: changed += 1
            built.append((name, pages, label))

    if not args.check:
        write_readme(built)
        print(f"  ✓ README.md (index for {len(built)} templates)")
        print(f"\nDone. {changed} written, {skipped} unchanged, {len(built)} total.")
        return 0
    else:
        print(f"\n--check: {total_violations} conformance violation(s), {changed} drifted template(s) across {len(built)} templates.")
        return 1 if (total_violations or changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
