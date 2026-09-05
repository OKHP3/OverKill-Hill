#!/usr/bin/env python3
"""Build the static site from shared chrome and page sources.

This is deliberately a commit-time generator.  The published output remains
ordinary HTML files, which keeps GitHub Pages simple and makes the generated
files inspectable.  Run ``--bootstrap`` once to extract the current pages into
``site-src/``; normal development uses the default build or ``--check``.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site-src"
PARTIALS = ROOT / "assets" / "partials"
MANIFEST = SRC / "pages.json"
EXCLUDED = ("assets/", ".agents/", ".local/", "node_modules/", "site-src/")
APP_RE = re.compile(r"/assets/js/app\.js(?:\?[^\"']*)?")
# The French pilot only covers these four routes. The shared header must not
# grow a language switcher on any other English page.
# Pilot languages beyond English, in display order, for the four evergreen
# routes below. Each entry is route -> {lang_code: target_route}.
PILOT_LANGUAGES = ["fr", "de", "es"]
PILOT_LANG_SWITCH = {
    "/": {"fr": "/fr/", "de": "/de/", "es": "/es/"},
    "/about/": {"fr": "/fr/about/", "de": "/de/about/", "es": "/es/about/"},
    "/projects/": {"fr": "/fr/projects/", "de": "/de/projects/", "es": "/es/projects/"},
    "/contact/": {"fr": "/fr/contact/", "de": "/de/contact/", "es": "/es/contact/"},
}

# Small inline flag icons for the language switcher (USA, not UK -- this is
# an en-US site). Kept as compact SVG rather than emoji so rendering is
# identical across every OS/browser instead of depending on platform
# emoji-flag support.
USA_FLAG_SVG = (
    '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21">'
    '<rect fill="#B22234" height="20" width="30"/>'
    '<rect fill="#FFFFFF" height="1.54" width="30" y="1.54"/>'
    '<rect fill="#FFFFFF" height="1.54" width="30" y="4.62"/>'
    '<rect fill="#FFFFFF" height="1.54" width="30" y="7.69"/>'
    '<rect fill="#FFFFFF" height="1.54" width="30" y="10.77"/>'
    '<rect fill="#FFFFFF" height="1.54" width="30" y="13.85"/>'
    '<rect fill="#FFFFFF" height="1.54" width="30" y="16.92"/>'
    '<rect fill="#3C3B6E" height="10.77" width="12"/>'
    "</svg>"
)
FRANCE_FLAG_SVG = (
    '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21">'
    '<rect fill="#0055A4" height="20" width="10"/>'
    '<rect fill="#FFFFFF" height="20" width="10" x="10"/>'
    '<rect fill="#EF4135" height="20" width="10" x="20"/>'
    "</svg>"
)
GERMANY_FLAG_SVG = (
    '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21">'
    '<rect fill="#000000" height="6.67" width="30"/>'
    '<rect fill="#DD0000" height="6.67" width="30" y="6.67"/>'
    '<rect fill="#FFCE00" height="6.66" width="30" y="13.34"/>'
    "</svg>"
)
SPAIN_FLAG_SVG = (
    '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21">'
    '<rect fill="#AA151B" height="5" width="30"/>'
    '<rect fill="#F1BF00" height="10" width="30" y="5"/>'
    '<rect fill="#AA151B" height="5" width="30" y="15"/>'
    "</svg>"
)

LANG_FLAG_SVG = {"en": USA_FLAG_SVG, "fr": FRANCE_FLAG_SVG, "de": GERMANY_FLAG_SVG, "es": SPAIN_FLAG_SVG}
LANG_LABEL = {"en": "English (US)", "fr": "Fran\u00e7ais", "de": "Deutsch", "es": "Espa\u00f1ol"}

# Keep one identity node for the whole site. Page-specific JSON-LD should
# reference this node with @id instead of defining divergent organizations.
ORGANIZATION_JSONLD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://overkillhill.com/#organization",
    "name": "OverKill Hill P³™",
    "url": "https://overkillhill.com/",
    "logo": {
        "@type": "ImageObject",
        "url": "https://overkillhill.com/assets/img/over-kill-hill-p3-sentinel-warning-square-256.png",
        "width": 256,
        "height": 256,
    },
    "sameAs": [
        "https://www.linkedin.com/company/overkillhillp3",
        "https://facebook.com/OverKillHillP3/",
        "https://x.com/OverKillHillP3",
        "https://www.youtube.com/@OverKillHillP3",
        "https://ko-fi.com/overkillhillp3",
        "https://pro.fiverr.com/s/VYKPpoB",
    ],
}


def tracked_pages() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.html"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    return sorted(
        ROOT / name for name in result.stdout.splitlines()
        if not name.startswith(EXCLUDED)
    )


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel


def canonical_meta(soup: BeautifulSoup) -> dict[str, str]:
    metadata: dict[str, str] = {"title": soup.title.get_text() if soup.title else ""}
    for tag in soup.head.find_all("meta"):
        key = tag.get("name") or tag.get("property")
        if key and tag.get("content") is not None:
            metadata[f"meta:{key}"] = tag["content"]
    canonical = soup.head.find("link", rel=lambda value: value and "canonical" in value)
    alternate = soup.head.find("link", rel=lambda value: value and "alternate" in value)
    metadata["canonical"] = canonical.get("href", "") if canonical else ""
    metadata["alternate"] = alternate.get("href", "") if alternate else ""
    return metadata


def active_route(route: str) -> str:
    if route == "/":
        return "home"
    for section in ("/projects/", "/writings/", "/about/"):
        if route.startswith(section):
            return route if route in {
                "/projects/", "/projects/skillz/", "/projects/found-ry/",
                "/projects/mermaid-theme-builder/", "/projects/bpmn-for-mermaid/",
                "/projects/mac-studio-local-ai-workbench/",
                "/projects/abrahamic-reference-engine/",
                "/projects/glee-fully-chai-chasers/", "/projects/kierans-lifetrkr/",
                "/projects/first-diagram-is-a-liar/",
                "/projects/telling-forward/",
                "/writings/",
                "/writings/first-diagram-is-a-liar/", "/manifesto/",
                "/prompt-forge/", "/universe/", "/about/", "/contact/", "/legal/",
            } else section
    return route


def write_source(path: Path, soup: BeautifulSoup) -> dict[str, str]:
    rel = path.relative_to(ROOT).as_posix()
    stem = SRC / "pages" / rel
    stem.parent.mkdir(parents=True, exist_ok=True)
    body = soup.body
    main = body.find("main") if body else None
    if main is None:
        raise ValueError(f"{rel}: expected <main>")
    # decode_contents() keeps HTML comments intact. Converting individual
    # BeautifulSoup Comment nodes with str() would emit their text without
    # the comment delimiters, leaking section labels into the page.
    main_source = main.decode_contents()
    # The shared footer owns the live year. A legacy legal-page body copy also
    # carried that id; keep its visible text without creating duplicate ids.
    main_source = re.sub(
        r'(<span\b[^>]*?)\s+id=(["\'])current-year\2',
        r"\1",
        main_source,
        flags=re.IGNORECASE,
    )
    (stem.with_suffix(".main.html")).write_text(main_source, encoding="utf-8")

    extras: list[str] = []
    for child in body.contents:
        if not getattr(child, "name", None) or child.name in {"header", "main", "footer"}:
            continue
        if child.name == "a" and any("skip-link" in cls for cls in (child.get("class") or [])):
            continue
        if child.name == "script" and APP_RE.search(child.get("src", "")):
            continue
        extras.append(str(child))
    for script in soup.head.find_all("script", {"type": "application/ld+json"}):
        extras.append(str(script))
    (stem.with_suffix(".extras.html")).write_text("\n".join(extras), encoding="utf-8")

    metadata = canonical_meta(soup)
    metadata.update({
        "path": rel,
        "route": route_for(path),
        "active": active_route(route_for(path)),
        "lang": soup.html.get("lang", "en") if soup.html else "en",
        "body_class": " ".join(body.get("class") or []) if body else "",
    })
    return metadata


def make_head_partial(index: BeautifulSoup) -> str:
    head = index.head
    # A failed earlier bootstrap could leave the placeholder as escaped text
    # inside the donor head. Remove that artifact before inserting the real
    # canonical element.
    for node in list(head.contents):
        if isinstance(node, NavigableString) and "Content-Security-Policy" in str(node) and "<meta" in str(node):
            node.extract()
    for tag in list(head.find_all("script", {"type": "application/ld+json"})):
        tag.decompose()
    csp = head.find("meta", attrs={"http-equiv": re.compile("^Content-Security-Policy$", re.I)})
    csp_tag = BeautifulSoup(
        '<meta http-equiv="Content-Security-Policy" content="{{CSP}}" />',
        "html.parser",
    ).meta
    if csp:
        csp.replace_with(csp_tag)
    else:
        referrer = head.find("meta", attrs={"name": "referrer"})
        (referrer or head.find("meta")).insert_after(csp_tag)
    dynamic_names = {
        "description", "keywords", "author", "creator", "publisher",
        "twitter:title", "twitter:description", "twitter:image", "twitter:image:alt",
    }
    dynamic_properties = {
        "og:title", "og:description", "og:type", "og:url", "og:image", "og:image:alt",
        "og:image:width", "og:image:height", "og:image:type", "article:published_time",
    }
    for tag in head.find_all("meta"):
        name = tag.get("name")
        prop = tag.get("property")
        if name in dynamic_names:
            tag["content"] = "{{META:" + name + "}}"
        elif prop in dynamic_properties:
            tag["content"] = "{{META:" + prop + "}}"
    for tag in list(head.find_all("link", rel=lambda value: value and any(
        rel in value for rel in ("prev", "next")
    ))):
        tag.decompose()
    head.append(BeautifulSoup(
        '<link href="{{PREV}}" rel="prev"/><link href="{{NEXT}}" rel="next"/>',
        "html.parser",
    ))
    organization = BeautifulSoup(
        '<script type="application/ld+json"></script>',
        "html.parser",
    ).script
    organization.string = json.dumps(ORGANIZATION_JSONLD, ensure_ascii=False, indent=2)
    head.append(organization)
    if head.title:
        head.title.string = "{{TITLE}}"
    for tag in head.find_all("link"):
        rel = tag.get("rel") or []
        if "canonical" in rel:
            tag["href"] = "{{CANONICAL}}"
        elif "alternate" in rel and tag.get("hreflang") == "en":
            tag["href"] = "{{ALTERNATE}}"
    rendered = str(head)
    rendered = re.sub(
        r'<meta\b(?=[^>]*\bhttp-equiv="Content-Security-Policy")'
        r'(?=[^>]*\bcontent="[^"]*")[^>]*/?>',
        '<meta http-equiv="Content-Security-Policy" content="{{CSP}}" />',
        rendered,
        count=1,
        flags=re.IGNORECASE,
    )
    return rendered


def make_chrome_partials(index: BeautifulSoup) -> None:
    header = index.body.find("header", class_="site-header")
    footer = index.body.find("footer", class_="site-footer")
    if not header or not footer:
        raise ValueError("index.html must contain site header and footer")
    for tag in header.select("[aria-current]"):
        del tag["aria-current"]
    (PARTIALS / "head.html").write_text(make_head_partial(index), encoding="utf-8")
    for name, fragment in (("header.html", str(header)), ("footer.html", str(footer))):
        # Partial files are reusable from any route, so local assets must be
        # root-relative rather than relative to the partial's own directory.
        fragment = re.sub(r'((?:href|src)=")(?!/)(assets/)', r'\1/\2', fragment)
        (PARTIALS / name).write_text(fragment, encoding="utf-8")


def bootstrap() -> None:
    PARTIALS.mkdir(parents=True, exist_ok=True)
    (SRC / "pages").mkdir(parents=True, exist_ok=True)
    pages = []
    index = BeautifulSoup((ROOT / "index.html").read_text(encoding="utf-8"), "html.parser")
    make_chrome_partials(index)
    for path in tracked_pages():
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        pages.append(write_source(path, soup))
    MANIFEST.write_text(json.dumps({"schema": 1, "pages": pages}, indent=2) + "\n", encoding="utf-8")
    print(f"Bootstrapped {len(pages)} pages into {SRC}")


def policies() -> dict[str, str]:
    sys.path.insert(0, str(ROOT / "scripts"))
    from csp import load_policies, page_class
    # The CSP consolidation task owns policy generation.  This renderer only
    # consumes that checked-in canonical output; it must not silently derive a
    # second policy while rendering pages.
    return load_policies(), page_class


def render_page(page: dict[str, str], csp_policies: dict[str, str], classify) -> str:
    rel = page["path"]
    stem = SRC / "pages" / rel
    main = stem.with_suffix(".main.html").read_text(encoding="utf-8")
    extras = stem.with_suffix(".extras.html").read_text(encoding="utf-8")
    head = (PARTIALS / "head.html").read_text(encoding="utf-8")
    header = (PARTIALS / "header.html").read_text(encoding="utf-8")
    footer = (PARTIALS / "footer.html").read_text(encoding="utf-8")
    values = {
        "TITLE": page["title"],
        "CANONICAL": page.get("canonical", ""),
        "ALTERNATE": page.get("alternate", ""),
        "ALTERNATE_FR": page.get("alternate_fr", ""),
        "ALTERNATE_DE": page.get("alternate_de", ""),
        "ALTERNATE_ES": page.get("alternate_es", ""),
        "ALTERNATE_X_DEFAULT": page.get("alternate_x_default", ""),
        "PREV": page.get("prev", ""),
        "NEXT": page.get("next", ""),
    }
    for key, value in page.items():
        if key.startswith("meta:"):
            values["META:" + key[5:]] = value
    kind = classify(ROOT / rel)
    values["CSP"] = csp_policies[kind]
    for key, value in values.items():
        # CSP is already a serialized policy and must retain its quotes.
        replacement = value if key == "CSP" else html.escape(value, quote=True)
        head = head.replace("{{" + key + "}}", replacement)
    # Metadata is optional for utility routes. Remove dynamic tags whose
    # manifest values are intentionally absent instead of shipping literal
    # template placeholders into the generated document.
    rendered_head = BeautifulSoup(head, "html.parser")
    for tag in list(rendered_head.find_all("meta")):
        if str(tag.get("content", "")).startswith("{{META:"):
            tag.decompose()
    # Utility/error routes deliberately have no social metadata in the
    # manifest. Remove the remaining fixed OG/Twitter scaffolding from the
    # shared donor head as well, rather than leaving partial card tags behind.
    if "meta:og:title" not in page:
        for tag in list(rendered_head.find_all("meta")):
            if tag.get("property", "").startswith("og:") or tag.get("name", "").startswith("twitter:"):
                tag.decompose()
    head = str(rendered_head)
    # BeautifulSoup serializes attributes in a different order from the CSP
    # generator. Normalize the generated tag here so build-site --check and
    # scripts/generate-csp.py share one byte-stable representation.
    head = re.sub(
        r'<meta\b(?=[^>]*\bhttp-equiv=["\']Content-Security-Policy["\'])'
        r'(?=[^>]*\bcontent="([^"]*)")[^>]*/?>',
        lambda match: (
            '<meta http-equiv="Content-Security-Policy" '
            f'content="{match.group(1)}" />'
        ),
        head,
        count=1,
        flags=re.IGNORECASE,
    )
    if not page.get("canonical"):
        head = re.sub(
            r'\s*<link href="" rel="canonical"/>\n?',
            "",
            head,
            count=1,
        )
    if not page.get("alternate"):
        head = re.sub(
            r'\s*<link href="" hreflang="en" rel="alternate"/>\n?',
            "",
            head,
            count=1,
        )
    for key, hreflang in (("alternate_fr", "fr"), ("alternate_de", "de"), ("alternate_es", "es"), ("alternate_x_default", "x-default")):
        if not page.get(key):
            head = re.sub(
                rf'\s*<link href="" hreflang="{hreflang}" rel="alternate"/>\n?',
                "",
                head,
                count=1,
            )
    for key, rel in (("prev", "prev"), ("next", "next")):
        if not page.get(key):
            head = re.sub(
                rf'\s*<link href="" rel="{rel}"/>\n?',
                "",
                head,
                count=1,
            )
    header_soup = BeautifulSoup(header, "html.parser")
    for tag in header_soup.select("[aria-current]"):
        del tag["aria-current"]
    target = "/" if page["active"] == "home" else page["active"]
    candidates = header_soup.select("nav a")
    exact = [a for a in candidates if a.get("href", "").split("#")[0] == target]
    chosen = exact[0] if exact else next(
        (a for a in candidates if a.get("href", "").split("#")[0] == target.rstrip("/") + "/"),
        None,
    )
    if chosen is None and target in {"/projects/", "/writings/", "/about/"}:
        chosen = next((a for a in candidates if a.get("href", "").split("#")[0] == target), None)
    if chosen is not None:
        chosen["aria-current"] = "page"
    lang_targets = PILOT_LANG_SWITCH.get(page["route"])
    if lang_targets:
        nav_toggle_el = header_soup.select_one(".nav-toggle")
        if nav_toggle_el is None:
            raise ValueError(f"{rel}: expected mobile nav toggle for language switcher placement")
        # Dropdown language switcher: a toggle button showing the current
        # page's language flag (English/USA by default on every EN page),
        # plus a hidden menu of the other pilot languages revealed on
        # click -- same interaction shape as the light/dark/system theme
        # toggle, adapted for real navigation since each option is a link
        # to a different page rather than a client-side state change.
        #
        # Lives as its own top-level section of the header row (a sibling
        # of nav.primary-nav and .header-controls), not inside the nav
        # link list and not folded into the search/theme-toggle cluster:
        #   1. It must stay visually and structurally separate from
        #      .header-controls (search + display-mode switcher) -- its
        #      own section of the header, not a third icon bolted onto
        #      that group.
        #   2. It must NOT live inside nav.primary-nav > ul, because that
        #      list collapses into the off-canvas mobile menu; a switcher
        #      inside it would only be reachable after opening the
        #      hamburger, at the bottom of the link list, while the
        #      display-mode switch stays visible at the top of the page.
        #      Placing it here keeps it visible in the header on every
        #      viewport, matching the theme toggle's behavior.
        options = [
            f'<li><a aria-current="true" aria-label="{LANG_LABEL["en"]}" class="lang-switch-option is-current" '
            f'href="{html.escape(page["route"], quote=True)}" hreflang="en" lang="en">{LANG_FLAG_SVG["en"]}'
            f'<span class="lang-switch-option-label">{LANG_LABEL["en"]}</span></a></li>'
        ]
        for lang in PILOT_LANGUAGES:
            target = lang_targets.get(lang)
            if not target:
                continue
            options.append(
                f'<li><a aria-label="{LANG_LABEL[lang]}" class="lang-switch-option" '
                f'href="{html.escape(target, quote=True)}" hreflang="{lang}" lang="{lang}">{LANG_FLAG_SVG[lang]}'
                f'<span class="lang-switch-option-label">{LANG_LABEL[lang]}</span></a></li>'
            )
        toggle = (
            f'<button aria-expanded="false" aria-haspopup="true" aria-label="Language: {LANG_LABEL["en"]}" '
            f'class="lang-switch-toggle" type="button"><span class="lang-flag-current">{LANG_FLAG_SVG["en"]}</span></button>'
        )
        menu = '<ul class="lang-switch-menu" hidden>' + "".join(options) + "</ul>"
        switch_section = BeautifulSoup(
            '<div class="lang-switch">' + toggle + menu + "</div>",
            "html.parser",
        ).div
        nav_toggle_el.insert_before(switch_section)
    body_class = f' class="{html.escape(page["body_class"], quote=True)}"' if page["body_class"] else ""
    app = next((x for x in BeautifulSoup((ROOT / "index.html").read_text(encoding="utf-8"), "html.parser").body.find_all("script")
                if APP_RE.search(x.get("src", ""))), None)
    app_html = str(app) if app else '<script src="/assets/js/app.js"></script>'
    return (
        "<!DOCTYPE html>\n<html lang=\"" + html.escape(page["lang"], quote=True) + "\">\n"
        + head + "\n<body" + body_class + ">\n"
        + '  <a class="okh-skip-link" href="#main">Skip to main content</a>\n'
        + str(header_soup) + '\n  <main id="main">\n' + main + "\n  </main>\n"
        + str(BeautifulSoup(footer, "html.parser")) + "\n    " + app_html + "\n"
        + extras + "\n</body>\n</html>\n"
    )


def build(check: bool) -> int:
    if not MANIFEST.exists():
        print("Missing site-src/pages.json. Run: python3 scripts/build-site.py --bootstrap", file=sys.stderr)
        return 1
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    csp_policies, classify = policies()
    failures = []
    for page in data["pages"]:
        output = ROOT / page["path"]
        rendered = render_page(page, csp_policies, classify)
        if check:
            if not output.exists() or output.read_text(encoding="utf-8") != rendered:
                failures.append(page["path"])
        else:
            output.write_text(rendered, encoding="utf-8")
    if failures:
        print("Generated HTML is stale:")
        print("\n".join(f"  {path}" for path in failures))
        print("Run: python3 scripts/build-site.py")
        return 1
    print(f"Generated HTML verified for {len(data['pages'])} pages." if check
          else f"Generated {len(data['pages'])} static HTML pages.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", action="store_true", help="extract current pages into site-src")
    parser.add_argument("--check", action="store_true", help="fail when committed HTML differs")
    args = parser.parse_args()
    if args.bootstrap:
        bootstrap()
        return build(False)
    return build(args.check)


if __name__ == "__main__":
    raise SystemExit(main())
