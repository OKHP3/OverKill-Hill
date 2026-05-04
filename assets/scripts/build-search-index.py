#!/usr/bin/env python3
"""
Build /assets/data/search-index.json from every indexable HTML page on the site.

- Walks the project root for *.html files.
- Skips files whose <meta name="robots"> contains "noindex".
- Skips known utility pages (404, under-construction).
- Extracts title, description, canonical URL, headings, and a plaintext body excerpt.
- For the article /writings/first-diagram-is-a-liar/ it also creates one entry
  per <section id="..."> and per <h2 id="..."> so deep links inside the article
  become independently searchable.

Re-run any time content changes:
    python3 assets/scripts/build-search-index.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "data" / "search-index.json"
SITE = "https://overkillhill.com"

SKIP_FILES = {
    "404.html",
    "under-construction.html",
}
SKIP_DIR_PARTS = {".git", ".local", ".cache", ".vscode", ".github",
                  ".config", ".canvas", ".agents", "attached_assets",
                  "node_modules"}

CATEGORY_RULES = [
    ("/writings/first-diagram-is-a-liar/v03/", "Field Guide"),
    ("/writings/first-diagram-is-a-liar/", "Article"),
    ("/writings/", "Writing"),
    ("/projects/", "Project"),
    ("/manifesto/", "Brand"),
    ("/universe/", "Brand"),
    ("/about/", "Brand"),
    ("/contact/", "Brand"),
    ("/legal/", "Brand"),
    ("/found-ry/", "Brand"),
    ("/prompt-forge/", "Brand"),
]


def categorise(url_path: str) -> str:
    if url_path in ("/", ""):
        return "Home"
    for prefix, label in CATEGORY_RULES:
        if url_path.startswith(prefix):
            return label
    return "Page"


class TextExtractor(HTMLParser):
    """Strip script/style/nav/footer/header and collect main-body text + headings."""

    SKIP_TAGS = {"script", "style", "noscript", "svg", "template", "iframe"}
    DROP_BY_CLASS = {"site-header", "site-footer", "primary-nav", "sub-nav",
                     "skip-link", "sr-only", "okh-search-overlay",
                     "footer-bottom", "site-banner"}

    # Self-closing / void HTML elements — never push to drop stack
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                 "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_stack: list[str] = []   # stack of skipped (script/style/etc) tag names
        self._drop_stack: list[str] = []   # stack of dropped (header/nav/etc) tag names
        self._text_parts: list[str] = []
        self._h2_parts: list[tuple[str, str]] = []  # (id, text)
        self._h3_parts: list[str] = []
        self._current_heading: list[str] | None = None
        self._current_heading_id: str = ""
        self._current_heading_level: int = 0
        self.title: str = ""
        self._in_title = False

    @property
    def _skip_depth(self) -> int:
        return len(self._skip_stack)

    @property
    def _drop_depth(self) -> int:
        return len(self._drop_stack)

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrd = dict(attrs)
        cls = attrd.get("class", "")
        cls_set = set(cls.split())

        if tag in self.VOID_TAGS:
            return

        if tag in self.SKIP_TAGS:
            self._skip_stack.append(tag)
            return
        if cls_set & self.DROP_BY_CLASS:
            self._drop_stack.append(tag)
            return
        if self._drop_depth or self._skip_depth:
            return

        if tag == "title":
            self._in_title = True
        elif tag in ("h2", "h3"):
            self._current_heading = []
            self._current_heading_id = attrd.get("id", "")
            self._current_heading_level = 2 if tag == "h2" else 3

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.VOID_TAGS:
            return
        # Pop matching skip frame (handle close of script/style/etc)
        if self._skip_stack and self._skip_stack[-1] == tag:
            self._skip_stack.pop()
            return
        # Pop matching drop frame — only when the closing tag matches the
        # tag that opened the dropped region. Anything in between is collateral.
        if self._drop_stack and self._drop_stack[-1] == tag:
            self._drop_stack.pop()
            return
        if self._drop_depth or self._skip_depth:
            return
        if tag == "title":
            self._in_title = False
        elif tag in ("h2", "h3") and self._current_heading is not None:
            text = re.sub(r"\s+", " ", "".join(self._current_heading)).strip()
            if text:
                if self._current_heading_level == 2:
                    self._h2_parts.append((self._current_heading_id, text))
                else:
                    self._h3_parts.append(text)
                self._text_parts.append(text)
            self._current_heading = None

    def handle_data(self, data):
        if self._skip_depth or self._drop_depth:
            return
        if self._in_title:
            self.title += data
            return
        if self._current_heading is not None:
            self._current_heading.append(data)
        self._text_parts.append(data)

    def collected_text(self) -> str:
        text = " ".join(self._text_parts)
        return re.sub(r"\s+", " ", text).strip()


META_TAG_RE = re.compile(r"<meta\b([^>]*)/?>", re.I | re.S)
LINK_TAG_RE = re.compile(r"<link\b([^>]*)/?>", re.I | re.S)
ATTR_RE = re.compile(r"""([a-zA-Z][\w:-]*)\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))""")


def parse_attrs(attr_str: str) -> dict:
    out = {}
    for m in ATTR_RE.finditer(attr_str):
        key = m.group(1).lower()
        val = m.group(3) if m.group(3) is not None else (
            m.group(4) if m.group(4) is not None else m.group(5))
        out[key] = (val or "").strip()
    return out


def read_meta(html: str, key: str) -> str:
    """Attribute-order-agnostic meta/link reader.

    `key` is one of: "description", "robots", "canonical", "ogtype".
    """
    if key in ("description", "robots", "ogtype"):
        target_attr = "og:type" if key == "ogtype" else key
        match_key = "property" if key == "ogtype" else "name"
        for m in META_TAG_RE.finditer(html):
            attrs = parse_attrs(m.group(1))
            if attrs.get(match_key, "").lower() == target_attr.lower():
                return attrs.get("content", "").strip()
        return ""
    if key == "canonical":
        for m in LINK_TAG_RE.finditer(html):
            attrs = parse_attrs(m.group(1))
            rel = attrs.get("rel", "").lower().split()
            if "canonical" in rel:
                return attrs.get("href", "").strip()
        return ""
    return ""


def is_noindex(html: str) -> bool:
    """Return True if any robots-style meta tag declares noindex."""
    targets = {"robots", "googlebot", "bingbot", "slurp", "duckduckbot",
               "applebot", "yandex"}
    for m in META_TAG_RE.finditer(html):
        attrs = parse_attrs(m.group(1))
        name = attrs.get("name", "").lower()
        if name in targets and "noindex" in attrs.get("content", "").lower():
            return True
    return False


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    if not rel.startswith("/"):
        rel = "/" + rel
    if rel == "/index.html":
        rel = "/"
    return rel


def excerpt(text: str, limit: int = 600) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    # Try to end on a sentence boundary
    last_period = cut.rfind(". ")
    if last_period > limit * 0.6:
        return cut[: last_period + 1]
    last_space = cut.rfind(" ")
    if last_space > 0:
        return cut[:last_space] + "…"
    return cut + "…"


def extract_article_sections(html: str, base_url: str, base_title: str) -> list[dict]:
    """For the long-form article, emit one entry per <section id="..."> with an h2 inside,
    plus per top-level <h2 id="...">."""
    out: list[dict] = []
    # Match sections with id
    for m in re.finditer(
        r'<section[^>]*\sid=["\']([^"\']+)["\'][^>]*>(.*?)</section>',
        html, re.S | re.I,
    ):
        sec_id = m.group(1)
        body = m.group(2)
        # Pull a title — first h2/h3 inside
        title_match = re.search(r"<h[23][^>]*>(.*?)</h[23]>", body, re.S | re.I)
        if title_match:
            sec_title = re.sub(r"<[^>]+>", "", title_match.group(1))
            sec_title = re.sub(r"\s+", " ", sec_title).strip()
        else:
            sec_title = sec_id.replace("-", " ").title()
        # Strip tags
        plain = re.sub(r"<script.*?</script>", " ", body, flags=re.S | re.I)
        plain = re.sub(r"<style.*?</style>", " ", plain, flags=re.S | re.I)
        plain = re.sub(r"<[^>]+>", " ", plain)
        plain = re.sub(r"\s+", " ", plain).strip()
        if len(plain) < 60:
            continue
        out.append({
            "url": f"{base_url}#{sec_id}",
            "title": f"{sec_title} — {base_title}",
            "category": "Article Section",
            "description": excerpt(plain, 220),
            "headings": [],
            "body": excerpt(plain, 800),
            "parent": base_url,
        })
    # Also catch standalone <h2 id="..."> not inside a <section id="...">
    for m in re.finditer(
        r'<h2[^>]*\sid=["\']([^"\']+)["\'][^>]*>(.*?)</h2>',
        html, re.S | re.I,
    ):
        h_id = m.group(1)
        # If we already produced this anchor as a section, skip
        if any(e["url"].endswith(f"#{h_id}") for e in out):
            continue
        h_title = re.sub(r"<[^>]+>", "", m.group(2))
        h_title = re.sub(r"\s+", " ", h_title).strip()
        if not h_title:
            continue
        # Grab the text immediately following the heading until the next h2
        rest = html[m.end():]
        next_h2 = re.search(r"<h2", rest, re.I)
        chunk = rest[: next_h2.start()] if next_h2 else rest[:4000]
        plain = re.sub(r"<script.*?</script>", " ", chunk, flags=re.S | re.I)
        plain = re.sub(r"<style.*?</style>", " ", plain, flags=re.S | re.I)
        plain = re.sub(r"<[^>]+>", " ", plain)
        plain = re.sub(r"\s+", " ", plain).strip()
        if len(plain) < 80:
            continue
        out.append({
            "url": f"{base_url}#{h_id}",
            "title": f"{h_title} — {base_title}",
            "category": "Article Section",
            "description": excerpt(plain, 220),
            "headings": [],
            "body": excerpt(plain, 800),
            "parent": base_url,
        })
    return out


def process_file(path: Path) -> list[dict]:
    rel = path.relative_to(ROOT).as_posix()
    if path.name in SKIP_FILES:
        return []
    parts = set(path.relative_to(ROOT).parts)
    if parts & SKIP_DIR_PARTS:
        return []

    html = path.read_text(encoding="utf-8", errors="replace")
    if is_noindex(html):
        return []

    parser = TextExtractor()
    try:
        parser.feed(html)
    except Exception as exc:  # pragma: no cover - defensive
        print(f"[warn] parse failed for {rel}: {exc}", file=sys.stderr)
        return []

    title = re.sub(r"\s+", " ", parser.title).strip() or rel
    description = read_meta(html, "description")
    canonical = read_meta(html, "canonical")
    url_path = canonical.replace(SITE, "") if canonical.startswith(SITE) else url_for(path)
    body = parser.collected_text()

    entry = {
        "url": url_path,
        "title": title,
        "category": categorise(url_path),
        "description": description,
        "headings": [t for _id, t in parser._h2_parts] + parser._h3_parts,
        "body": excerpt(body, 700),
    }
    out = [entry]

    # Article deep-link entries
    if url_path == "/writings/first-diagram-is-a-liar/":
        out.extend(extract_article_sections(html, url_path, title))

    return out


def main() -> None:
    entries: list[dict] = []
    for path in sorted(ROOT.rglob("*.html")):
        # Filter directories
        rel_parts = path.relative_to(ROOT).parts
        if any(p in SKIP_DIR_PARTS for p in rel_parts):
            continue
        entries.extend(process_file(path))

    # Stable sort: Home → Brand → Writing/Article → Article Section → Project → Page
    cat_order = {"Home": 0, "Brand": 1, "Writing": 2, "Article": 3,
                 "Article Section": 4, "Field Guide": 5, "Project": 6, "Page": 7}
    entries.sort(key=lambda e: (cat_order.get(e["category"], 99), e["url"]))

    payload = {
        "site": SITE,
        "generated": "static",
        "count": len(entries),
        "entries": entries,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(entries)} entries")
    by_cat: dict[str, int] = {}
    for e in entries:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + 1
    for cat, n in sorted(by_cat.items()):
        print(f"  {cat}: {n}")


if __name__ == "__main__":
    main()
