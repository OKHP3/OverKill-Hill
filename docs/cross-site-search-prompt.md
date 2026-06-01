# Cross-Site Search Implementation Prompt
## For: Glee-fully.tools · AskJamie.bot Replit agents
## Issued from: OverKill Hill P³™ (overkillhill.com) — source of truth

Paste this entire prompt into the target Replit agent. It is self-contained and requires no follow-up.

---

## 0 · What you are building

OverKill Hill P³™ (OKH), Glee-fully.tools, and AskJamie.bot are three sibling static sites that share `assets/js/app.js` and `assets/css/theme.css` as their common foundation.

OKH has a fully working search system. Your job is to bring this site to exact functional parity:

- A static JSON index of every indexable page (`assets/data/search-index.json`).
- A search overlay on every page (Ctrl/Cmd+K or `/` to open, Esc to close, ↑↓ navigate, ↵ follow) injected by the shared `app.js`.
- A dedicated `/search/` full-page search with category-pill filtering and shareable `?q=` URLs.
- A **secondary peer-results section** in both the overlay and the full search page: after showing this site's own results, fetch and show the top results from the other two sibling sites with distinct labelling and absolute links.

Do **not** touch the OKH repository. Work only inside this Replit project.

---

## 1 · Read these existing files first

Before doing any work, read:

1. `assets/js/app.js` — especially Section 5 (begins at the comment `// ── 5. OKH Search`). The entire search logic lives here.
2. `assets/css/theme.css` — the search CSS block begins at the comment `SECTION · OKH SEARCH` (around line 4544 if this is an OKH-derived theme). You need to know the exact line numbers so you can adapt the accent-color references.
3. Any existing `assets/data/search-index.json` — if it exists, note its structure. If it doesn't exist yet, you will create it.
4. `server.py` (or whatever file serves static files) — you need to add a CORS header for the index JSON.

---

## 2 · Index builder — create and run

Create `scripts/build-search-index.py` with the content below, then run it once with `python3 scripts/build-search-index.py` to generate the index.

**The only parts you must change from the template** are marked with `# ← CHANGE THIS` comments:

```python
#!/usr/bin/env python3
"""
Build assets/data/search-index.json from every indexable HTML page on the site.

Re-run any time content changes:
    python3 scripts/build-search-index.py
"""

from __future__ import annotations
import json, os, re, sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT  = ROOT / "assets" / "data" / "search-index.json"
SITE = "https://YOUR-DOMAIN.com"          # ← CHANGE THIS (e.g. "https://glee-fully.tools")

SKIP_FILES = {
    "404.html",
    "under-construction.html",
}
SKIP_DIR_PARTS = {".git", ".local", ".cache", ".vscode", ".github",
                  ".config", ".canvas", ".agents", "attached_assets",
                  "node_modules"}

# ← CHANGE THIS — map URL prefixes to category labels that match your site's structure.
# Order matters: first match wins. The final fallback is "Page".
CATEGORY_RULES = [
    ("/tools/",    "Tool"),          # example for Glee-fully
    ("/about/",    "Brand"),
    ("/contact/",  "Brand"),
    ("/legal/",    "Brand"),
]

def categorise(url_path: str) -> str:
    if url_path in ("/", ""):
        return "Home"
    for prefix, label in CATEGORY_RULES:
        if url_path.startswith(prefix):
            return label
    return "Page"


class TextExtractor(HTMLParser):
    SKIP_TAGS  = {"script", "style", "noscript", "svg", "template", "iframe"}
    DROP_BY_CLASS = {"site-header", "site-footer", "primary-nav", "sub-nav",
                     "skip-link", "sr-only", "okh-search-overlay",
                     "footer-bottom", "site-banner"}
    VOID_TAGS  = {"area","base","br","col","embed","hr","img","input",
                  "link","meta","param","source","track","wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._skip_stack, self._drop_stack = [], []
        self._text_parts, self._h2_parts, self._h3_parts = [], [], []
        self._current_heading, self._current_heading_id = None, ""
        self._current_heading_level = 0
        self.title, self._in_title = "", False

    @property
    def _skip_depth(self): return len(self._skip_stack)
    @property
    def _drop_depth(self): return len(self._drop_stack)

    def handle_starttag(self, tag, attrs):
        tag = tag.lower(); attrd = dict(attrs)
        if tag in self.VOID_TAGS: return
        if tag in self.SKIP_TAGS: self._skip_stack.append(tag); return
        if set(attrd.get("class","").split()) & self.DROP_BY_CLASS:
            self._drop_stack.append(tag); return
        if self._drop_depth or self._skip_depth: return
        if tag == "title": self._in_title = True
        elif tag in ("h2","h3"):
            self._current_heading = []
            self._current_heading_id = attrd.get("id","")
            self._current_heading_level = 2 if tag == "h2" else 3

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.VOID_TAGS: return
        if self._skip_stack and self._skip_stack[-1] == tag:
            self._skip_stack.pop(); return
        if self._drop_stack and self._drop_stack[-1] == tag:
            self._drop_stack.pop(); return
        if self._drop_depth or self._skip_depth: return
        if tag == "title": self._in_title = False
        elif tag in ("h2","h3") and self._current_heading is not None:
            text = re.sub(r"\s+", " ", "".join(self._current_heading)).strip()
            if text:
                if self._current_heading_level == 2:
                    self._h2_parts.append((self._current_heading_id, text))
                else:
                    self._h3_parts.append(text)
                self._text_parts.append(text)
            self._current_heading = None

    def handle_data(self, data):
        if self._skip_depth or self._drop_depth: return
        if self._in_title: self.title += data; return
        if self._current_heading is not None: self._current_heading.append(data)
        self._text_parts.append(data)

    def collected_text(self):
        return re.sub(r"\s+", " ", " ".join(self._text_parts)).strip()


META_TAG_RE = re.compile(r"<meta\b([^>]*)/?>",  re.I|re.S)
LINK_TAG_RE = re.compile(r"<link\b([^>]*)/?>",  re.I|re.S)
ATTR_RE     = re.compile(r"""([a-zA-Z][\w:-]*)\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))""")

def parse_attrs(s):
    out = {}
    for m in ATTR_RE.finditer(s):
        key = m.group(1).lower()
        val = m.group(3) if m.group(3) is not None else (m.group(4) if m.group(4) is not None else m.group(5))
        out[key] = (val or "").strip()
    return out

def read_meta(html, key):
    if key in ("description","robots","ogtype"):
        target = "og:type" if key == "ogtype" else key
        mk = "property" if key == "ogtype" else "name"
        for m in META_TAG_RE.finditer(html):
            a = parse_attrs(m.group(1))
            if a.get(mk,"").lower() == target.lower(): return a.get("content","").strip()
        return ""
    if key == "canonical":
        for m in LINK_TAG_RE.finditer(html):
            a = parse_attrs(m.group(1))
            if "canonical" in a.get("rel","").lower().split(): return a.get("href","").strip()
        return ""
    return ""

def is_noindex(html):
    targets = {"robots","googlebot","bingbot","slurp","duckduckbot","applebot","yandex"}
    for m in META_TAG_RE.finditer(html):
        a = parse_attrs(m.group(1))
        if a.get("name","").lower() in targets and "noindex" in a.get("content","").lower():
            return True
    return False

def url_for(path):
    rel = path.relative_to(ROOT).as_posix()
    if rel.endswith("/index.html"): rel = rel[:-len("index.html")]
    if not rel.startswith("/"): rel = "/" + rel
    if rel == "/index.html": rel = "/"
    return rel

def excerpt(text, limit=600):
    text = text.strip()
    if len(text) <= limit: return text
    cut = text[:limit]
    lp = cut.rfind(". ")
    if lp > limit * 0.6: return cut[:lp+1]
    ls = cut.rfind(" ")
    return (cut[:ls] + "…") if ls > 0 else (cut + "…")

def process_file(path):
    if path.name in SKIP_FILES: return []
    if set(path.relative_to(ROOT).parts) & SKIP_DIR_PARTS: return []
    html = path.read_text(encoding="utf-8", errors="replace")
    if is_noindex(html): return []
    parser = TextExtractor()
    try: parser.feed(html)
    except Exception as exc:
        print(f"[warn] parse failed for {path}: {exc}", file=sys.stderr); return []
    title     = re.sub(r"\s+", " ", parser.title).strip() or path.as_posix()
    desc      = read_meta(html, "description")
    canonical = read_meta(html, "canonical")
    url_path  = canonical.replace(SITE, "") if canonical.startswith(SITE) else url_for(path)
    body      = parser.collected_text()
    return [{
        "url":         url_path,
        "title":       title,
        "category":    categorise(url_path),
        "description": desc,
        "headings":    [t for _id, t in parser._h2_parts] + parser._h3_parts,
        "body":        excerpt(body, 700),
    }]

def main():
    entries = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(p in SKIP_DIR_PARTS for p in path.relative_to(ROOT).parts): continue
        entries.extend(process_file(path))
    cat_order = {"Home":0,"Brand":1,"Tool":2,"Page":3}
    entries.sort(key=lambda e: (cat_order.get(e["category"],99), e["url"]))
    payload = {"site": SITE, "generated": "static", "count": len(entries), "entries": entries}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(entries)} entries")
    by_cat = {}
    for e in entries: by_cat[e["category"]] = by_cat.get(e["category"],0) + 1
    for cat, n in sorted(by_cat.items()): print(f"  {cat}: {n}")

if __name__ == "__main__":
    main()
```

After running the builder, confirm the file exists at `assets/data/search-index.json` and the `count` field is reasonable (should match the number of indexable HTML pages).

---

## 3 · Serve the index with CORS headers

The cross-site peer fetch requires the index JSON to be readable by the other two domains. Open `server.py` and locate where static file responses are sent. Add this header **specifically for the search index route** (not globally — you don't need CORS everywhere):

```python
# If the request path is /assets/data/search-index.json, add:
response.headers["Access-Control-Allow-Origin"] = "*"
response.headers["Cache-Control"] = "public, max-age=3600"
```

How exactly to do this depends on your existing `server.py` structure. The key constraint: **only the search-index.json file needs `Access-Control-Allow-Origin: *`**. If it is simpler to add the header to all static JSON files, that is acceptable.

Restart the server after this change and verify by fetching `https://YOUR-DOMAIN.com/assets/data/search-index.json` in a browser — the response headers should include `Access-Control-Allow-Origin: *`.

---

## 4 · Check and tune `app.js` Section 5

The shared `app.js` already contains Section 5 (the search engine). Verify these six items are correct for this site:

### 4a · INDEX_URL path

```js
const INDEX_URL = "/assets/data/search-index.json";
```

This must be exactly `/assets/data/search-index.json`. If it says `/assets/search-index.json` (without the `data/` segment), correct it.

### 4b · Overlay aria-label and placeholder

In the `buildOverlay()` function, find:

```js
wrap.setAttribute("aria-label", "Search OverKill Hill");
```

Change `"Search OverKill Hill"` to `"Search [Site Name]"` matching this site's brand.

Also update the `placeholder` attribute on the search `<input>`:

```js
'placeholder="Search the Forge — articles, projects, ideas…"'
```

Change the placeholder text to something meaningful for this site's content. Keep it brief — one line, ≤ 60 characters.

### 4c · Overlay "Open full search" link

In `buildOverlay()`, find:

```js
'<a href="/search/">Open full search →</a>'
```

Keep this as-is — you will create `/search/` in step 5.

### 4d · Empty-state hint buttons

In `emptyStateHtml()`, find the `<ul class="okh-search-hint-list">` block. Replace the `data-q` values with 5–6 search terms that represent the most common things users will look for on this site:

```js
'<li><button type="button" data-q="YOUR TERM 1">Label 1</button></li>'
```

### 4e · No-results fallback suggestion text

In the `render()` function inside `initOverlay()`, find the no-results string:

```js
"<em>mermaid</em>, <em>ROY</em>, <em>council</em>, or <em>manifesto</em>"
```

Replace with 3–4 terms relevant to this site.

### 4f · Search page empty-state text

In the `render()` function inside `initSearchPage()`, find:

```js
'<p>Search across writings, projects, manifesto, and the Council archives.</p>'
```

Replace with a one-sentence description of what is searchable on this site.

### 4g · injectTrigger — search button placement

The shared `app.js` includes an `injectTrigger()` function that creates the `.okh-search-trigger` button and attaches it to the page header on every load. Verify the injection target hierarchy is present on this site:

**Primary target — `.header-controls` wrapper (required)**

The trigger is **prepended** into a `.header-controls` div that sits between the primary nav and the hamburger toggle. This wrapper must exist in your page `<header>` markup:

```html
<!-- Sits between <nav class="primary-nav"> and the hamburger <button class="nav-toggle"> -->
<div class="header-controls">
  <!-- theme toggle button goes here (if present) -->
  <!-- app.js prepends the search trigger before the first child -->
</div>
```

If `.header-controls` is absent, the trigger falls back in this order:
1. Inserted before `.nav-toggle` (the hamburger button)
2. Appended to `.site-header .container` or `.site-header`
3. Appended to `document.body` (last resort)

Add `.header-controls` to every page header (or to the shared template/partial). Without it the trigger will appear in a degraded position.

**Do not add `margin-left` to `.okh-search-trigger`**

Spacing between the trigger and adjacent controls (theme toggle, hamburger) is provided by the `gap: 0.5rem` on `.header-controls`. Adding `margin-left` to the trigger itself will double the gap.

---

## 5 · Add peer-results to `app.js` Section 5

This is the new cross-site feature. After all existing code in Section 5 but **before the closing `}());`**, insert the following block verbatim, then fill in the two constants at the top:

```js
// ── 5b. Cross-site peer results ──────────────────────────────────────────────
// Fetches the search indexes of the two sibling sites and shows their top
// results in a secondary section beneath this site's own results.
// Peer results appear ONLY when there is a query with at least one primary hit.
// Peer URLs are absolute so the user is taken to the correct domain.
(function () {
  "use strict";

  // ← FILL IN: The two peer site index URLs. Remove the site that is THIS site.
  var PEERS = [
    { label: "OverKill Hill P³™",        base: "https://overkillhill.com",  indexUrl: "https://overkillhill.com/assets/data/search-index.json"  },
    { label: "Glee-fully Tools™",         base: "https://glee-fully.tools",  indexUrl: "https://glee-fully.tools/assets/data/search-index.json"  },
    { label: "AskJamie™",                 base: "https://askjamie.bot",      indexUrl: "https://askjamie.bot/assets/data/search-index.json"      },
  ].filter(function (p) {
    // Remove the entry whose base matches the current origin
    return p.base.replace(/\/$/, "") !== window.location.origin.replace(/\/$/, "");
  });

  var _peerCache = {};     // keyed by indexUrl → Promise<entries[]>

  function loadPeer(url) {
    if (!_peerCache[url]) {
      _peerCache[url] = fetch(url, { credentials: "omit" })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function (d) { return Array.isArray(d.entries) ? d.entries : []; })
        .catch(function () { return []; });
    }
    return _peerCache[url];
  }

  function tokenizePeer(q) {
    return q.toLowerCase().split(/[^a-z0-9'-]+/i).filter(function (t) { return t.length >= 2; });
  }

  function scorePeer(entry, tokens) {
    if (!tokens.length) return 0;
    var title    = (entry.title       || "").toLowerCase();
    var desc     = (entry.description || "").toLowerCase();
    var headings = (entry.headings    || []).join(" ").toLowerCase();
    var body     = (entry.body        || "").toLowerCase();
    var score = 0; var allHit = true;
    tokens.forEach(function (t) {
      var hit = 0;
      if (title.includes(t))    hit += 8;
      if (headings.includes(t)) hit += 5;
      if (desc.includes(t))     hit += 4;
      if (body.includes(t))     hit += 2;
      if (!hit) allHit = false;
      score += hit;
    });
    return allHit ? score : score * 0.4;
  }

  function topPeerResults(entries, tokens, limit) {
    var scored = [];
    entries.forEach(function (e) {
      var s = scorePeer(e, tokens);
      if (s > 0) scored.push([s, e]);
    });
    scored.sort(function (a, b) { return b[0] - a[0]; });
    return scored.slice(0, limit || 3).map(function (x) { return x[1]; });
  }

  function escPeer(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
    });
  }

  function renderPeerSection(peer, results, tokens, base) {
    var html = '<div class="okh-peer-section">'
      + '<p class="okh-peer-label">Also on <a href="' + escPeer(base) + '" target="_blank" rel="noopener">'
      + escPeer(peer.label) + '</a></p>';
    results.forEach(function (e) {
      var absUrl = base + e.url;
      var snip   = (e.description || e.body || "").slice(0, 160);
      if (snip.length === 160) snip += "…";
      // Highlight tokens in title
      var titleHtml = escPeer(e.title || e.url);
      tokens.forEach(function (t) {
        var re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
        titleHtml = titleHtml.replace(re, "<mark>$1</mark>");
      });
      html += '<a class="okh-search-result okh-peer-result" href="' + escPeer(absUrl)
        + '" target="_blank" rel="noopener">'
        + '<div class="okh-search-result-meta">'
        + '<span class="okh-search-result-cat">' + escPeer(e.category || "Page") + "</span>"
        + '<span class="okh-search-result-url">' + escPeer(peer.label) + " · " + escPeer(e.url) + "</span>"
        + "</div>"
        + '<h3 class="okh-search-result-title">' + titleHtml + "</h3>"
        + (snip ? '<p class="okh-search-result-snippet">' + escPeer(snip) + "</p>" : "")
        + "</a>";
    });
    html += "</div>";
    return html;
  }

  // ── Hook into the overlay ──────────────────────────────────────────────────
  // We watch for the overlay input event and append peer results after a short
  // delay so the primary results (from the existing search function) land first.

  function attachPeerToOverlay() {
    var overlay = document.querySelector(".okh-search-overlay");
    if (!overlay) return;
    var input = overlay.querySelector(".okh-search-input");
    var list  = overlay.querySelector(".okh-search-results");
    if (!input || !list) return;

    var peerTimer = null;

    function renderPeerInOverlay() {
      var q = input.value.trim();
      // Remove any existing peer sections
      overlay.querySelectorAll(".okh-peer-section").forEach(function (el) { el.remove(); });
      if (!q || !list.querySelector(".okh-search-result")) return;

      var tokens = tokenizePeer(q);
      Promise.all(PEERS.map(function (p) {
        return loadPeer(p.indexUrl).then(function (entries) {
          return { peer: p, results: topPeerResults(entries, tokens, 3) };
        });
      })).then(function (groups) {
        // Remove again in case primary re-rendered while we were fetching
        overlay.querySelectorAll(".okh-peer-section").forEach(function (el) { el.remove(); });
        if (!list.querySelector(".okh-search-result")) return;  // primary now empty — bail
        groups.forEach(function (g) {
          if (g.results.length) {
            list.insertAdjacentHTML("beforeend", renderPeerSection(g.peer, g.results, tokens, g.peer.base));
          }
        });
      });
    }

    input.addEventListener("input", function () {
      clearTimeout(peerTimer);
      peerTimer = setTimeout(renderPeerInOverlay, 280);
    });
  }

  // ── Hook into the dedicated /search/ page ────────────────────────────────
  function attachPeerToSearchPage() {
    var input  = document.getElementById("search-page-input");
    var list   = document.getElementById("search-results");
    if (!input || !list) return;

    var peerTimer = null;

    function renderPeerOnPage() {
      var q = input.value.trim();
      list.querySelectorAll(".okh-peer-section").forEach(function (el) { el.remove(); });
      if (!q) return;
      var tokens = tokenizePeer(q);
      Promise.all(PEERS.map(function (p) {
        return loadPeer(p.indexUrl).then(function (entries) {
          return { peer: p, results: topPeerResults(entries, tokens, 6) };
        });
      })).then(function (groups) {
        list.querySelectorAll(".okh-peer-section").forEach(function (el) { el.remove(); });
        groups.forEach(function (g) {
          if (g.results.length) {
            list.insertAdjacentHTML("beforeend", renderPeerSection(g.peer, g.results, tokens, g.peer.base));
          }
        });
      });
    }

    input.addEventListener("input", function () {
      clearTimeout(peerTimer);
      peerTimer = setTimeout(renderPeerOnPage, 350);
    });
  }

  // Bootstrap — wait for the existing search to initialize first
  function bootPeer() {
    // Give the primary search overlay 200 ms to inject itself, then wire up
    setTimeout(function () {
      attachPeerToOverlay();
      if (document.body.classList.contains("search-page")) {
        attachPeerToSearchPage();
      }
    }, 200);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootPeer);
  } else {
    bootPeer();
  }
}());
```

**After inserting**, set the `PEERS` array correctly:

- If this is **Glee-fully.tools**, remove the Glee-fully entry from `PEERS` (it self-filters via `window.location.origin`, but removing it is cleaner).
- If this is **AskJamie.bot**, remove the AskJamie entry.
- The `base` values must exactly match the production domain including protocol, no trailing slash.

---

## 6 · CSS additions

### 6a · header-controls wrapper

The `.header-controls` div (introduced in section 4g) requires this rule. Add it inside `assets/css/theme.css` **within or near the header/nav block** — not inside the `SECTION · OKH SEARCH` block:

```css
/* Flex wrapper: search trigger + theme toggle, sits between nav and hamburger */
.header-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}
```

If you are using the foundation `theme.css` copied from OKH without modification, this rule is already present. Confirm it exists before adding a duplicate.

### 6b · Peer-results CSS

Add this block to the end of the `SECTION · OKH SEARCH` CSS block in `assets/css/theme.css`. It should appear **after** the last rule in that section:

```css
/* ── Peer (cross-site) results section ── */
.okh-peer-section {
  border-top: 2px solid var(--color-border-subtle, #2a2f37);
  margin-top: 0.25rem;
  padding-top: 0.25rem;
}
.okh-peer-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-muted, #9ca3af);
  padding: 0.5rem 1rem 0.25rem;
  margin: 0;
}
.okh-peer-label a {
  color: inherit;
  text-decoration: none;
  font-weight: 600;
}
.okh-peer-label a:hover { text-decoration: underline; }
.okh-peer-result {
  opacity: 0.82;
}
.okh-peer-result:hover,
.okh-peer-result[data-active="true"] {
  opacity: 1;
}
```

### Brand color override

The inherited search CSS references OKH's accent colors (`--okh-orange: #c46a2c` and `--okh-amber: #d99257`) as fallback hex values in selectors like `.okh-search-trigger:hover`, `.okh-search-result-cat`, `.okh-search-hint-list button`, and `mark` backgrounds.

These fallback values will be automatically overridden **if** your site's CSS already declares the correct CSS custom property names. If your accent colors use different variable names, add this small override block **inside** the SECTION · OKH SEARCH block:

```css
/* Brand accent override — replace values with this site's actual colors */
.okh-search-trigger:hover,
.okh-search-trigger:focus-visible    { border-color: var(--brand-accent); color: var(--brand-accent); }
.okh-search-close:hover              { color: var(--brand-accent); border-color: var(--brand-accent); }
.okh-search-result-cat               { background: rgba(VAR_R, VAR_G, VAR_B, 0.18); color: var(--brand-accent-light); }
.okh-search-hint-list button         { border-color: rgba(VAR_R, VAR_G, VAR_B, 0.35); color: var(--brand-accent-light); }
.okh-search-result:hover,
.okh-search-result[data-active="true"]{ background: rgba(VAR_R, VAR_G, VAR_B, 0.08); }
.okh-search-result mark              { background: rgba(VAR_R, VAR_G, VAR_B, 0.32); }
```

Replace `VAR_R, VAR_G, VAR_B` with the RGB components of this site's primary accent color (e.g. for Glee-fully's signature teal `#2a9d8f`, use `42, 157, 143`).

---

## 7 · Create the `/search/` page

Create `search/index.html`. Use this template and replace every `[PLACEHOLDER]` value:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Search [SITE NAME] | [SITE TAGLINE]</title>
    <meta name="description" content="Search [SITE NAME] — [one sentence description of what is searchable]." />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="[FULL CANONICAL URL — e.g. https://glee-fully.tools/search/]" />

    <!-- Copy all <link rel="icon">, <link rel="manifest">, and <meta property="og:…">
         tags from this site's existing index.html or another page.
         Update og:title, og:url, og:description for the search page. -->

    <link rel="stylesheet" href="/assets/css/theme.css" />
  </head>
  <body class="[BODY-CLASS] search-page">
    <!-- [BODY-CLASS] must be the class already used on all pages of this site,
         e.g. "glee-main" for Glee-fully.tools or "askjamie-main" for AskJamie.bot.
         Keep "search-page" — it activates the JS search-page initializer. -->

    <!-- Copy the exact <header> from another page of this site. Do not modify it. -->

    <main id="main">
      <div class="container">
        <section class="search-hero">
          <p class="eyebrow" style="text-transform:uppercase;letter-spacing:0.12em;color:var(--color-muted);font-size:0.8rem;margin:0;">[SITE NAME] Search</p>
          <h1>Search [SITE NAME]</h1>
          <p>[One sentence describing what users can find. E.g.: "Every tool, guide, and page — one box." Hit <kbd>Esc</kbd> any time to bail out, <kbd>↵</kbd> to follow.]</p>
        </section>

        <div class="search-input-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" />
          </svg>
          <input
            type="search"
            id="search-page-input"
            autocomplete="off"
            spellcheck="false"
            placeholder="[Site-specific placeholder text…]"
            aria-label="Search [SITE NAME]"
          />
        </div>

        <p class="search-stats" id="search-stats">Loading index…</p>
        <div class="search-categories" id="search-categories" role="group" aria-label="Filter by category"></div>
        <div class="search-results-list" id="search-results" role="list"></div>

        <noscript>
          <p style="text-align:center;color:var(--color-muted);margin-top:2rem;">
            Search requires JavaScript. Browse the <a href="/">home page</a> instead.
          </p>
        </noscript>
      </div>
    </main>

    <!-- Copy the exact <footer> from another page of this site. Do not modify it. -->

    <script src="/assets/js/app.js"></script>
  </body>
</html>
```

**Important:** The `id` attributes `search-page-input`, `search-stats`, `search-categories`, and `search-results` must be exactly as shown — the JS targets them by ID.

---

## 8 · Add the search page to the site's navigation

Open the header `<nav>` in one existing page and find the `<ul>` inside `.primary-nav`. Add a Search link. The exact placement is your call — typically after the last nav item or before a call-to-action:

```html
<li><a href="/search/">Search</a></li>
```

Then **copy this change to every page** of the site (or to the shared template/partial if one exists). The `app.js` search overlay already injects a search trigger button into `.header-controls` automatically (see section 4g), so this static link is just a fallback for the full-page `/search/` experience.

---

## 9 · Validate the implementation

Run through this checklist in order:

1. **Index exists and is valid JSON**
   ```
   python3 -c "import json; d=json.load(open('assets/data/search-index.json')); print(d['count'], 'entries')"
   ```
   Expected: a positive integer equal to the number of indexable HTML files.

2. **Index served with CORS header**
   Fetch `https://YOUR-DOMAIN.com/assets/data/search-index.json` in a browser dev-tools network tab. Confirm `access-control-allow-origin: *` appears in response headers.

3. **Overlay opens**
   Open any page. Press `/` or Ctrl+K. The search overlay should appear, the input should auto-focus, and the empty state with hint buttons should show.

4. **Primary search returns results**
   Type any word that appears in your content. Results should appear with category pills and snippets. Pressing ↑↓ should highlight results; Enter should navigate.

5. **Full search page works**
   Navigate to `/search/`. Type a query. Results should appear. Category filter buttons should appear. The URL should update with `?q=yourquery`.

6. **Peer results appear**
   In either the overlay or the `/search/` page, type a term likely to appear on the sibling sites (e.g. "GPT", "prompt", "Jamie", "tools"). After ~300ms a "Also on [Peer Site]" section should appear below the primary results with absolute links opening in a new tab.

7. **Brand colors applied**
   Search trigger button hover, result category badges, and highlighted `<mark>` text should use this site's accent color, not the OKH orange `#c46a2c`.

8. **Body class guard**
   Open browser console and type `document.body.classList`. Confirm both this site's brand class (`glee-main` or `askjamie-main`) AND `search-page` (only on `/search/`) are present. The theme toggle must NOT appear on brand-locked pages (the `app.js` `brandLocked` check handles this automatically).

---

## 10 · Do not change these things

- The scoring algorithm (`scoreEntry`, `tokenize`, `search`) in `app.js` Section 5 — do not touch it.
- The `SKIP_DIR_PARTS` set in the index builder — only add to it if this site has project-specific directories to exclude; never remove entries.
- The `okh-search-*` class names in CSS or JS — they are shared identifiers across all three sites.
- The `credentials: "same-origin"` on the primary index fetch (line in `loadIndex()`).
- The `credentials: "omit"` on the peer fetches (required for cross-origin requests).
- The focus-trap and keyboard-nav logic inside `initOverlay()`.

---

## Reference: OKH search index schema

Each entry in the index has this shape:

```json
{
  "url":         "/path/to/page/",
  "title":       "Page Title | Site Name",
  "category":    "Home | Brand | Tool | Page | …",
  "description": "Meta description text",
  "headings":    ["h2 text", "h2 text", "h3 text"],
  "body":        "Plain-text excerpt of visible page content (≤700 chars)"
}
```

Article-section deep-link entries also carry a `"parent"` field pointing at the section's parent page URL. This is an OKH-specific feature; sibling sites only need it if they have long-form articles with multiple named sections worth making independently searchable. Implementing it is optional.

---

*End of prompt. Questions from this document should be resolved by reading the referenced files in the OKH repository; all answers are in the code.*
