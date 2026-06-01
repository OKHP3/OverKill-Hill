#!/usr/bin/env python3
"""
scripts/enhance-pages.py — v0.5 site-wide enhancement pass

Idempotent.  Re-running on already-enhanced files is a no-op.

For every HTML file in the project root it will:

  1. Replace the <div class="container footer-meta">…</div> block with the
     two-paragraph layout (Built-with-Replit badge + copyright).
  2. Add a <link rel="preconnect" href="https://www.googletagmanager.com">
     hint after the existing fonts.googleapis.com preconnect, if missing.
  3. Add `decoding="async"` to every <img> that doesn't already have it.
  4. Add `loading="lazy"` to every <img> EXCEPT the first 2 in document
     order (those are typically the LCP candidates: nav avatar + hero).
  5. Insert a BreadcrumbList JSON-LD block before </head> based on the
     page's URL path (homepage / 404 / under-construction excluded).
  6. Tighten over-length meta descriptions and titles to fit SERP limits
     (also mirrors the change to og:description / twitter:description and
     og:title / twitter:title where present).
  7. For every BrandGuard case study, insert an Article JSON-LD block
     before </head>.
  8. Fix the canonical URL typo on mathews-archery (capital `BrandGuard`
     in the path → lower-case).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
SITE_ORIGIN = "https://askjamie.bot"
TODAY = date.today().isoformat()

# --------------------------------------------------------------------------
# Per-page metadata overrides (description + optional title rewrites)
# --------------------------------------------------------------------------

# Each value: { "description": "...", "title": "..." (optional) }
META_OVERRIDES: dict[str, dict[str, str]] = {
    "lens-system/okhp3-brandguard/lego/index.html": {
        "description": "GPT‑BRG01: LEGO BrandGuard™ — a public, brand‑safe GPT proof‑of‑concept showing how LEGO's tone, ethics, and identity can be protected at GPT speed.",
    },
    "lens-system/okhp3-brandguard/discount-tire/index.html": {
        "description": "GPT‑BRG10: Discount Tire BrandGuard™ — a friendly OKHP³ sentinel demonstrating how trusted automotive brand voice and ethics can be safeguarded by GPT.",
    },
    "lens-system/okhp3-brandguard/hershey/index.html": {
        "description": "GPT‑BRG06: Hershey BrandGuard™ — a warm, public‑source‑only GPT showing how an iconic confection brand keeps its tone, ethics, and identity on track.",
    },
    "lens-system/okhp3-brandguard/mathews-archery/index.html": {
        "description": "GPT‑BRG12: Mathews Archery BrandGuard™ — an OKHP³ custom GPT helping archers and bowhunters navigate the brand with on‑voice, on‑ethics answers.",
    },
    "lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/index.html": {
        "description": "GPT‑BFS01: Builders FirstSource — Framing Intelligent Futures. A BrandGuard™ GPT that turns public BFS material into safe, on‑brand customer help.",
    },
    "lens-system/okhp3-brandguard/dollar-general/index.html": {
        "description": "GPT‑BRG08: Dollar General BrandGuard™ — a public OKHP³ proof‑of‑concept GPT helping people understand the brand without going off‑voice or off‑ethics.",
    },
    "lens-system/resume-representative/index.html": {
        "description": "GPT‑AJ01: AskJamie™ Résumé Representative turns your career into a living, conversational AI agent that writes tailored, on‑voice résumés on demand.",
    },
    "lens-system/professional-portfolio/index.html": {
        "description": "GPT‑AJ02: AskJamie™ Professional Portfolio turns your work, wins, and weirdly specific strengths into a living, conversational AI portfolio agent.",
    },
    "lens-system/okhp3-brandguard/starbucks/index.html": {
        "description": "GPT‑BRG02: Starbucks BrandGuard™ — an OKHP³ proof‑of‑concept showing how a global consumer brand can protect tone, ethics, and identity at GPT speed.",
    },
    "lens-system/index.html": {
        "description": "AskJamie™ Lens System — four disciplined ways of seeing and expressing your story through one consistent, architected AI persona.",
    },
    "lens-system/okhp3-brandguard/brooks-running/index.html": {
        "description": "GPT‑BRG03: Brooks Running BrandGuard™ — an OKHP³ custom GPT proof‑of‑concept that protects Brooks' brand voice, ethics, and identity at GPT speed.",
    },
    "lens-system/okhp3-brandguard/scheels/index.html": {
        "description": "GPT‑BRG11: Scheels BrandGuard™ — an OKHP³ custom GPT helping shoppers navigate outdoor and sporting goods brand questions with on‑voice answers.",
    },
    "lens-system/enterprise-sleuth/index.html": {
        "description": "GPT‑AJ03: Enterprise Sleuth™ — an AI detective for enterprise knowledge. A working demo and recipe pack for building investigative GPTs at work.",
        "title": "AskJamie™ — Enterprise Sleuth™ · AI Detective for Enterprise Knowledge",
    },
    "lens-system/okhp3-brandguard/costco/index.html": {
        "description": "GPT‑BRG05: Costco BrandGuard™ — a public, early proof‑of‑concept GPT showing how a member‑first brand voice can stay protected at GPT speed.",
    },
    "lens-system/okhp3-brandguard/coca-cola/index.html": {
        "description": "GPT‑BRG09: Coca‑Cola BrandGuard™ — a public OKHP³ demonstration that shows how an iconic global brand can protect its tone, ethics, and identity.",
    },
    "lens-system/okhp3-brandguard/ping/index.html": {
        "description": "GPT‑BRG04: Ping BrandGuard™ — an early public proof‑of‑concept GPT showing how a trusted brand can stay on‑voice and on‑ethics across customer chats.",
    },
    "lens-system/okhp3-brandguard/lvmh/index.html": {
        "description": "GPT‑BRG07: LVMH BrandGuard™ — an OKHP³ public proof‑of‑concept showing portfolio‑level brand stewardship: voice, ethics, and identity at GPT speed.",
    },
    "under-construction.html": {
        "description": "This part of the AskJamie™ helpdesk is under construction. Explore the main AskJamie™ site for what's already live across the OKHP³ ecosystem.",
    },
    "about/index.html": {
        "description": "Learn about AskJamie™ — the strategic intelligence layer that unifies your digital ecosystem and orchestrates reasoning, narrative, and structure.",
    },
    "lens-system/okhp3-brandguard/index.html": {
        "description": "GPT‑AJ04: AskJamie™ OKHP³ BrandGuard™ — AI‑powered tone, ethics, and identity guardrails for brands. Keep GPTs on‑voice, on‑ethics, on‑identity.",
        "title": "AskJamie™ — OKHP³ BrandGuard™ · Brand Safety & Ethics Guardrails",
    },
    "contact/index.html": {
        "description": "Contact AskJamie™ for project inquiries, collaboration, and professional engagements. Reach out about AI persona work, BrandGuard™, or the Lens System.",
    },
}

# --------------------------------------------------------------------------
# Breadcrumb URL → label chain
# --------------------------------------------------------------------------

CRUMB_LABELS: dict[str, str] = {
    "about/index.html":                              "About",
    "contact/index.html":                            "Contact",
    "legal/index.html":                              "Legal",
    "universe/index.html":                           "Universe",
    "lens-system/index.html":                        "Lens System",
    "lens-system/enterprise-sleuth/index.html":      "Enterprise Sleuth™",
    "lens-system/professional-portfolio/index.html": "Professional Portfolio",
    "lens-system/resume-representative/index.html":  "Résumé Representative",
    "lens-system/okhp3-brandguard/index.html":       "OKHP³ BrandGuard™",
    "lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/index.html":
        "BFS — Framing Intelligent Futures",
    "lens-system/okhp3-brandguard/brooks-running/index.html":  "Brooks Running",
    "lens-system/okhp3-brandguard/coca-cola/index.html":       "Coca-Cola",
    "lens-system/okhp3-brandguard/costco/index.html":          "Costco",
    "lens-system/okhp3-brandguard/discount-tire/index.html":   "Discount Tire",
    "lens-system/okhp3-brandguard/dollar-general/index.html":  "Dollar General",
    "lens-system/okhp3-brandguard/hershey/index.html":         "Hershey",
    "lens-system/okhp3-brandguard/lego/index.html":            "LEGO",
    "lens-system/okhp3-brandguard/lvmh/index.html":            "LVMH",
    "lens-system/okhp3-brandguard/mathews-archery/index.html": "Mathews Archery",
    "lens-system/okhp3-brandguard/ping/index.html":            "Ping",
    "lens-system/okhp3-brandguard/scheels/index.html":         "Scheels",
    "lens-system/okhp3-brandguard/starbucks/index.html":       "Starbucks",
}

# Pages that should NOT receive a BreadcrumbList
BREADCRUMB_SKIP = {"index.html", "404.html", "under-construction.html"}

# Pages that should receive an Article schema (BrandGuard case studies)
ARTICLE_PAGES = {
    "lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/index.html",
    "lens-system/okhp3-brandguard/brooks-running/index.html",
    "lens-system/okhp3-brandguard/coca-cola/index.html",
    "lens-system/okhp3-brandguard/costco/index.html",
    "lens-system/okhp3-brandguard/discount-tire/index.html",
    "lens-system/okhp3-brandguard/dollar-general/index.html",
    "lens-system/okhp3-brandguard/hershey/index.html",
    "lens-system/okhp3-brandguard/lego/index.html",
    "lens-system/okhp3-brandguard/lvmh/index.html",
    "lens-system/okhp3-brandguard/mathews-archery/index.html",
    "lens-system/okhp3-brandguard/ping/index.html",
    "lens-system/okhp3-brandguard/scheels/index.html",
    "lens-system/okhp3-brandguard/starbucks/index.html",
}

ARTICLE_DATE_PUBLISHED = "2026-04-10"
ARTICLE_DATE_MODIFIED = TODAY

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

NEW_FOOTER_META = (
    '<div class="container footer-meta">\n'
    '        <p class="footer-built-with">\n'
    '          Built with\n'
    '          <a class="footer-replit-link"\n'
    '             href="https://replit.com/refer/overkillhillp3/"\n'
    '             target="_blank"\n'
    '             rel="noopener noreferrer">Replit</a>\n'
    '        </p>\n'
    '        <p class="footer-copyright">©\n'
    '          <span id="current-year-askjamie"></span>\n'
    '          AskJamie™. All rights reserved.\n'
    '        </p>\n'
    '      </div>'
)

FOOTER_META_RE = re.compile(
    r'<div class="container footer-meta">.*?</div>',
    re.DOTALL,
)

PRECONNECT_GTM = (
    '<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin />'
)
PRECONNECT_FONTS_GS_RE = re.compile(
    r'(<link rel="preconnect" href="https://fonts\.gstatic\.com"[^/>]*/?>)'
)


def update_footer(html: str) -> tuple[str, bool]:
    if 'footer-replit-link' in html:
        return html, False
    new_html, n = FOOTER_META_RE.subn(NEW_FOOTER_META, html, count=1)
    return new_html, bool(n)


def add_gtm_preconnect(html: str) -> tuple[str, bool]:
    if 'googletagmanager.com' in re.findall(
        r'<link[^>]*rel="preconnect"[^>]*href="([^"]+)"', html
    ).__str__():
        return html, False
    new_html, n = PRECONNECT_FONTS_GS_RE.subn(
        r'\1\n    ' + PRECONNECT_GTM, html, count=1
    )
    return new_html, bool(n)


def upgrade_imgs(html: str) -> tuple[str, int, int]:
    """Add decoding=async to all <img>; loading=lazy to all but first 2."""
    img_re = re.compile(r'<img\b([^>]*?)\s*/?>', re.IGNORECASE)
    matches = list(img_re.finditer(html))
    decoding_added = 0
    loading_added = 0

    # Walk in REVERSE so offsets stay valid as we splice.
    parts = list(html)
    for idx, m in enumerate(reversed(matches)):
        # Position from the START
        forward_idx = len(matches) - 1 - idx
        attrs = m.group(1)
        new_attrs = attrs

        if 'decoding=' not in new_attrs:
            new_attrs = new_attrs + ' decoding="async"'
            decoding_added += 1

        # Skip the first 2 images on the page (likely LCP candidates)
        if forward_idx >= 2 and 'loading=' not in new_attrs:
            new_attrs = new_attrs + ' loading="lazy"'
            loading_added += 1

        if new_attrs != attrs:
            new_tag = f'<img{new_attrs}>'
            start, end = m.span()
            parts[start:end] = list(new_tag)

    return ''.join(parts), decoding_added, loading_added


def update_meta_description(html: str, new_desc: str) -> int:
    """Update meta name=description, og:description, twitter:description."""
    n_total = 0
    patterns = [
        (r'(<meta\s+name="description"\s+content=")([^"]+)("[^>]*>)', new_desc),
        (r'(<meta\s+property="og:description"\s+content=")([^"]+)("[^>]*>)', new_desc),
        (r'(<meta\s+name="twitter:description"\s+content=")([^"]+)("[^>]*>)', new_desc),
    ]
    new_html = html
    for pat, val in patterns:
        new_html, n = re.subn(pat, lambda m: m.group(1) + val + m.group(3),
                              new_html, count=1)
        n_total += n
    if n_total:
        # Apply mutation back to caller via outer scope -- handled below
        pass
    return n_total, new_html


def update_meta_title(html: str, new_title: str) -> tuple[str, int]:
    n_total = 0
    new_html, n = re.subn(r'(<title>)([^<]+)(</title>)',
                          lambda m: m.group(1) + new_title + m.group(3),
                          html, count=1)
    n_total += n
    new_html, n = re.subn(
        r'(<meta\s+property="og:title"\s+content=")([^"]+)("[^>]*>)',
        lambda m: m.group(1) + new_title + m.group(3),
        new_html, count=1,
    )
    n_total += n
    new_html, n = re.subn(
        r'(<meta\s+name="twitter:title"\s+content=")([^"]+)("[^>]*>)',
        lambda m: m.group(1) + new_title + m.group(3),
        new_html, count=1,
    )
    n_total += n
    return new_html, n_total


def build_breadcrumb_json(rel_path: str) -> dict | None:
    """Return BreadcrumbList JSON-LD for the given page (or None)."""
    parts = rel_path.split('/')
    items = [
        {"@type": "ListItem", "position": 1,
         "name": "AskJamie™", "item": SITE_ORIGIN + "/"}
    ]
    pos = 2
    if rel_path == "about/index.html":
        items.append({"@type": "ListItem", "position": pos,
                      "name": "About", "item": f"{SITE_ORIGIN}/about/"})
    elif rel_path == "contact/index.html":
        items.append({"@type": "ListItem", "position": pos,
                      "name": "Contact", "item": f"{SITE_ORIGIN}/contact/"})
    elif rel_path == "legal/index.html":
        items.append({"@type": "ListItem", "position": pos,
                      "name": "Legal", "item": f"{SITE_ORIGIN}/legal/"})
    elif rel_path == "universe/index.html":
        items.append({"@type": "ListItem", "position": pos,
                      "name": "Universe", "item": f"{SITE_ORIGIN}/universe/"})
    elif rel_path == "lens-system/index.html":
        items.append({"@type": "ListItem", "position": pos,
                      "name": "Lens System",
                      "item": f"{SITE_ORIGIN}/lens-system/"})
    elif rel_path.startswith("lens-system/okhp3-brandguard/") and rel_path != "lens-system/okhp3-brandguard/index.html":
        items.append({"@type": "ListItem", "position": pos,
                      "name": "Lens System",
                      "item": f"{SITE_ORIGIN}/lens-system/"})
        pos += 1
        items.append({"@type": "ListItem", "position": pos,
                      "name": "OKHP³ BrandGuard™",
                      "item": f"{SITE_ORIGIN}/lens-system/okhp3-brandguard/"})
        pos += 1
        leaf = CRUMB_LABELS.get(rel_path, "Case study")
        items.append({"@type": "ListItem", "position": pos,
                      "name": leaf,
                      "item": SITE_ORIGIN + '/' + rel_path.replace('index.html', '')})
    elif rel_path == "lens-system/okhp3-brandguard/index.html":
        items.append({"@type": "ListItem", "position": pos,
                      "name": "Lens System",
                      "item": f"{SITE_ORIGIN}/lens-system/"})
        pos += 1
        items.append({"@type": "ListItem", "position": pos,
                      "name": "OKHP³ BrandGuard™",
                      "item": f"{SITE_ORIGIN}/lens-system/okhp3-brandguard/"})
    elif rel_path.startswith("lens-system/") and rel_path != "lens-system/index.html":
        items.append({"@type": "ListItem", "position": pos,
                      "name": "Lens System",
                      "item": f"{SITE_ORIGIN}/lens-system/"})
        pos += 1
        leaf = CRUMB_LABELS.get(rel_path, "Lens")
        items.append({"@type": "ListItem", "position": pos,
                      "name": leaf,
                      "item": SITE_ORIGIN + '/' + rel_path.replace('index.html', '')})
    else:
        return None

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def build_article_json(rel_path: str, html: str) -> dict | None:
    if rel_path not in ARTICLE_PAGES:
        return None
    title_m = re.search(r'<title>([^<]+)</title>', html)
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    canon_m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
    img_m = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
    h1_m = re.search(r'<h1[^>]*>(.+?)</h1>', html, re.DOTALL)
    headline = re.sub(r'<[^>]+>', '', h1_m.group(1)).strip() if h1_m else (
        title_m.group(1) if title_m else rel_path)
    headline = re.sub(r'\s+', ' ', headline)

    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": desc_m.group(1) if desc_m else "",
        "image": img_m.group(1) if img_m else "",
        "datePublished": ARTICLE_DATE_PUBLISHED,
        "dateModified": ARTICLE_DATE_MODIFIED,
        "inLanguage": "en-US",
        "isPartOf": {
            "@type": "WebSite",
            "name": "AskJamie™",
            "url": SITE_ORIGIN,
        },
        "author": {
            "@type": "Organization",
            "name": "AskJamie™ by OverKill Hill P³",
            "url": SITE_ORIGIN,
        },
        "publisher": {
            "@type": "Organization",
            "name": "AskJamie™",
            "url": SITE_ORIGIN,
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_ORIGIN}/assets/img/askjamie-avatar-tall-left-square-1024.png",
            },
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canon_m.group(1) if canon_m else "",
        },
    }


def inject_jsonld_blocks(html: str, blocks: list[dict],
                         markers: list[str]) -> tuple[str, int]:
    """Insert each block before </head> if its marker isn't already present."""
    added = 0
    new_html = html
    for block, marker in zip(blocks, markers):
        if not block:
            continue
        if marker in new_html:
            continue  # already there
        block_json = json.dumps(block, indent=2, ensure_ascii=False)
        snippet = (
            f'    <!-- {marker} -->\n'
            f'    <script type="application/ld+json">\n{block_json}\n    </script>\n'
        )
        new_html = new_html.replace('</head>', snippet + '  </head>', 1)
        added += 1
    return new_html, added


def fix_canonical_typo(html: str) -> tuple[str, bool]:
    if 'okhp3-BrandGuard' in html:
        return html.replace('okhp3-BrandGuard', 'okhp3-brandguard'), True
    return html, False


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    files = sorted(p for p in ROOT.glob('**/*.html')
                   if not str(p.relative_to(ROOT)).startswith('.'))
    summary = {
        "files": 0,
        "footers": 0,
        "preconnects": 0,
        "decoding_attrs": 0,
        "loading_attrs": 0,
        "descriptions": 0,
        "titles": 0,
        "breadcrumbs": 0,
        "articles": 0,
        "canonical_fixes": 0,
        "files_changed": 0,
    }

    for f in files:
        rel = str(f.relative_to(ROOT))
        original = f.read_text(encoding='utf-8')
        html = original

        # 1. Footer badge
        html, did = update_footer(html)
        if did: summary["footers"] += 1

        # 2. GTM preconnect
        html, did = add_gtm_preconnect(html)
        if did: summary["preconnects"] += 1

        # 3. + 4. Image attribute polish
        html, dec_n, lazy_n = upgrade_imgs(html)
        summary["decoding_attrs"] += dec_n
        summary["loading_attrs"] += lazy_n

        # 5. Canonical typo (mathews-archery)
        html, did = fix_canonical_typo(html)
        if did: summary["canonical_fixes"] += 1

        # 6. Meta description / title overrides
        override = META_OVERRIDES.get(rel)
        if override:
            if "description" in override:
                n, html = update_meta_description(html, override["description"])
                if n: summary["descriptions"] += 1
            if "title" in override:
                html, n = update_meta_title(html, override["title"])
                if n: summary["titles"] += 1

        # 7. + 8. JSON-LD blocks (Breadcrumb + Article)
        breadcrumb = build_breadcrumb_json(rel) if rel not in BREADCRUMB_SKIP else None
        article    = build_article_json(rel, html)

        html, added = inject_jsonld_blocks(
            html,
            [breadcrumb, article],
            ["BreadcrumbList JSON-LD (v0.5)", "Article JSON-LD (v0.5)"],
        )
        if breadcrumb and 'BreadcrumbList JSON-LD (v0.5)' in html and added:
            summary["breadcrumbs"] += 1
        if article and 'Article JSON-LD (v0.5)' in html and added:
            summary["articles"] += 1

        summary["files"] += 1
        if html != original:
            f.write_text(html, encoding='utf-8')
            summary["files_changed"] += 1

    # Summary
    print(f"\nProcessed {summary['files']} HTML files; {summary['files_changed']} written.")
    print(f"  Footers updated      : {summary['footers']}")
    print(f"  GTM preconnects added: {summary['preconnects']}")
    print(f"  decoding=async added : {summary['decoding_attrs']}")
    print(f"  loading=lazy added   : {summary['loading_attrs']}")
    print(f"  Descriptions tightened: {summary['descriptions']}")
    print(f"  Titles tightened     : {summary['titles']}")
    print(f"  BreadcrumbList added : {summary['breadcrumbs']}")
    print(f"  Article schema added : {summary['articles']}")
    print(f"  Canonical typos fixed: {summary['canonical_fixes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
