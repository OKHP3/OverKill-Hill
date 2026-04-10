# Cross-Site Sync: CSS, JS, and Mermaid — Prompt for Glee-fully Tools & AskJamie

---

## CONTEXT FOR THE AGENT

This document is the canonical sync brief for two satellite sites:
- **Glee-fully Tools** — https://glee-fully.tools / https://github.com/OKHP3/Glee-fullyTools
- **AskJamie** — https://askjamie.bot / https://github.com/OKHP3/AskJamie

Both sites share a codebase pattern with the primary site **overkillhill.com** (`OKHP3/OverKill-Hill`).
The primary site has just had a comprehensive refactor. Your job is to bring this site into parity with those changes and fix any issues found during your scan.

---

## PART 1 — SITE SCAN & QA

Before making any changes, audit every HTML page on this site and report what you find. Check for:

### 1A. Inline styles to extract
- Any `style=""` attributes on HTML elements that belong in CSS classes
- Any `<style>...</style>` blocks inside `<head>` or inside `<body>` — these should move to the external CSS file
- Exception: `type="application/ld+json"` schema blocks are fine as-is

### 1B. Inline scripts to extract
- Any `<script>` blocks that contain logic (not just `type="application/ld+json"` and not Google Analytics `gtag`/`dataLayer` blocks, which must stay inline)
- Mermaid initialization code that is inline — see Part 3 for the correct external file pattern

### 1C. Mermaid JS references
- Scan every page for any `<script src=...mermaid...>` or `import mermaid from ...` patterns
- Check whether they use an outdated CDN URL or version (anything older than mermaid@11 is outdated)
- The correct reference is:
  ```
  https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs
  ```
  imported as a JS module (`type="module"`), never as a plain `<script src>` tag

### 1D. General page health
- `<title>` tags — are they descriptive and not placeholder text?
- `<meta name="description">` — present and non-empty on every page?
- `og:title`, `og:description`, `og:image` — present on every page?
- `og:image:alt` — present and non-empty?
- Canonical `<link rel="canonical">` — correct URL on each page?
- `<html lang="en">` — present on every page?
- Footer copyright year — is it current (2026) or hardcoded to a past year?
- Any 404-prone links to files that no longer exist?
- Any orphaned files (HTML, JS, CSS) not referenced anywhere?

---

## PART 2 — CSS ADDITIONS

Open the site's main CSS file (likely `assets/css/theme.css` or similar) and append the following block **at the very end**, after all existing rules. Do not remove or overwrite anything — append only.

After adding it, bump the CSS cache-bust query string on every HTML page from whatever it currently is to the next version number (e.g. `?v=2` → `?v=3`). If no cache-bust string exists, add `?v=2`.

```css
/* ===== CROSS-SITE SYNC — from overkillhill.com refactor 2026-04-10 ===== */

/* Mermaid: isolate diagram labels from page colour inheritance.
   Prevents --color-fg (near-white) leaking into HTML foreignObject
   labels on light-themed diagrams. */
.mermaid foreignObject,
.mermaid foreignObject div,
.mermaid foreignObject p,
.mermaid foreignObject span {
  color: initial;
}

/* Amber text utility */
.text-amber {
  color: var(--okh-amber, #F59E0B);
}

/* Amber inline link */
.link-amber {
  color: var(--okh-amber, #F59E0B);
  text-decoration: underline;
}

/* Diagram static PNG fallback */
.diagram-static-img {
  display: block;
  max-width: 100%;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

/* Live-render <details> toggle inside .diagram-shell */
.diagram-live-render {
  margin-bottom: 0;
}

.diagram-live-render > summary {
  font-size: 0.82rem;
  color: var(--color-muted, #6b7280);
  cursor: pointer;
  margin-bottom: 0.5rem;
  list-style: none;
}

.diagram-live-render > summary::-webkit-details-marker {
  display: none;
}

/* Section subtitle beneath h2 */
.section-subtitle {
  font-family: var(--font-body, sans-serif);
  font-weight: 600;
  font-size: 1rem;
  text-transform: none;
  letter-spacing: 0;
  color: var(--color-muted, #6b7280);
  margin-top: -0.5rem;
  margin-bottom: 1.5rem;
}

/* Compact council-card variant */
.council-card--compact {
  margin: 2rem 0;
}

/* Council fairness-note paragraphs */
.council-note {
  font-size: 0.9rem;
  color: var(--color-muted, #6b7280);
  margin-bottom: 0.6rem;
  line-height: 1.6;
}

.council-note:last-of-type {
  margin-bottom: 0;
}

/* Prompt meta note — small italic text below each prompt card */
.prompt-note {
  font-size: 0.85rem;
  color: var(--color-muted, #6b7280);
  margin-top: 0.6rem;
  margin-bottom: 0;
}

/* Inline CTA link button block */
.btn-block-top {
  display: inline-block;
  margin-top: 0.5rem;
}

/* Repo CTA paragraph */
.article-repo-cta {
  font-size: 0.9rem;
  color: var(--color-muted, #6b7280);
  margin-top: 1rem;
}

.article-repo-cta .link-amber {
  text-decoration: none;
  color: var(--okh-amber, #F59E0B);
}

.article-repo-cta .link-amber:hover {
  text-decoration: underline;
}

/* Sidebar footnote (disclosure / attribution) */
.sidebar-footnote {
  font-size: 0.78rem;
  color: var(--color-muted, #6b7280);
  margin-top: 0.6rem;
  line-height: 1.5;
}

/* Footer built-with bar */
.footer-built-with {
  font-size: 0.8rem;
  color: var(--color-muted, #6b7280);
  white-space: nowrap;
  padding-left: 1rem;
}

.footer-built-with a {
  color: #FF3C00;
  text-decoration: none;
  font-weight: 600;
}

.footer-copyright {
  margin: 0;
  text-align: center;
}

/* TOC widget: GPU-layer hint for smooth animation */
@media (min-width: 1024px) {
  #toc-widget {
    will-change: transform;
  }
}

/* ===== END CROSS-SITE SYNC ===== */
```

---

## PART 3 — MERMAID JS UPDATE

If the site uses Mermaid diagrams, the initialization pattern must be updated to match the primary site.

### 3A. Create or replace `assets/js/mermaid-init.js`

If this file does not exist, create it. If it does, replace its content entirely:

```js
// Mermaid diagram initialization
// Relies on YAML front-matter in each diagram for theme/look (theme: neutral, look: neo).
// initialize() intentionally omits themeVariables to avoid overriding the YAML config.
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

mermaid.initialize({
  startOnLoad: false,
  securityLevel: "loose",
  flowchart: {
    curve: "basis",
    nodeSpacing: 55,
    rankSpacing: 65,
    htmlLabels: true,
  },
});

// Explicit run — more reliable than startOnLoad with ES module loading order
mermaid.run({
  querySelector: ".mermaid",
}).catch((err) => {
  console.warn("[mermaid-init] render error:", err);
});
```

### 3B. Reference the file in HTML

On every page that contains Mermaid diagrams, replace any existing inline mermaid `<script>` or `import` block with this one tag, placed just before `</body>`:

```html
<script type="module" src="/assets/js/mermaid-init.js"></script>
```

Remove any old:
- `<script src="https://cdn.jsdelivr.net/npm/mermaid@...">` (non-module CDN tag)
- `<script src="https://unpkg.com/mermaid...">` (unpkg CDN — outdated)
- Inline `<script type="module"> import mermaid from ... </script>` blocks
- Any `mermaid.initialize(...)` calls inside `<script>` tags in HTML

### 3C. Mermaid YAML front matter (if your diagrams use it)

Each `<pre class="mermaid">` block may optionally start with YAML front matter to control the theme without needing JS `themeVariables`. This is the pattern used on the primary site:

```
---
config:
  theme: neutral
  look: neo
---
```

This is optional — only add it if you want diagram-level theme control.

---

## PART 4 — STICKY TOC (conditional — only if the site has a sidebar TOC)

If the site has a sidebar table of contents widget with id `toc-widget`, append this function to the site's main `app.js` (just before the closing of the file):

```js
// ──────────────────────────────────────────────────────────────
// Sticky TOC: lerp scroll-follow (only on screens ≥1024px)
// ──────────────────────────────────────────────────────────────
(function () {
  if (window.innerWidth < 1024) return;

  var toc    = document.getElementById('toc-widget');
  var footer = document.querySelector('.site-footer');
  if (!toc || !footer) return;

  var lerpedY = 0;
  var targetY = 0;
  var SPEED   = 0.08;
  var NAV_H   = 112;
  var PAD     = 32;

  function lerp(a, b, t) { return a + (b - a) * t; }

  function getNaturalTop(el) {
    var top = 0;
    while (el) { top += el.offsetTop; el = el.offsetParent; }
    return top;
  }

  var tocNaturalTop = getNaturalTop(toc);
  var tocH          = toc.offsetHeight;

  function tick() {
    var scrollY   = window.scrollY;
    var footerTop = footer.offsetTop;

    var centeredOffset = Math.max(NAV_H, (window.innerHeight - tocH) / 2);
    var raw = Math.max(0, scrollY + centeredOffset - tocNaturalTop);
    var max = Math.max(0, footerTop - PAD - tocNaturalTop - tocH);
    targetY = Math.min(raw, max);

    lerpedY = lerp(lerpedY, targetY, SPEED);
    toc.style.transform = 'translateY(' + lerpedY.toFixed(2) + 'px)';

    requestAnimationFrame(tick);
  }

  requestAnimationFrame(tick);

  window.addEventListener('resize', function () {
    toc.style.transform = '';
    if (window.innerWidth >= 1024) {
      tocNaturalTop = getNaturalTop(toc);
      tocH = toc.offsetHeight;
    }
  });
}());
```

If the site does **not** have a `#toc-widget` element, skip this section entirely.

---

## PART 5 — INLINE STYLE EXTRACTION

After completing the scan from Part 1, extract any `style=""` attributes you found:

1. For each repeated pattern, create a named class in the site's CSS file (before the cross-site sync block added in Part 2)
2. Replace the `style=""` attribute in the HTML with `class="your-new-class"`
3. If a pattern appears only once and is truly one-off, it may stay inline — but flag it in your report
4. After all extractions, do a final grep to confirm zero unexpected `style="` attributes remain

---

## PART 6 — DELIVERY REPORT

When you are done, provide a summary that includes:

1. **Pages scanned** — list every HTML file checked
2. **Issues found** — itemised list with severity (critical / warning / info)
3. **Changes made** — what was added, extracted, or replaced
4. **Inline styles remaining** — count and reason for any kept
5. **Mermaid status** — version confirmed, number of pages updated
6. **CSS version** — what the cache-bust string was bumped to
7. **Any items requiring manual action** — e.g. GitHub repo commits, image files not present, etc.

---

*Brief generated from overkillhill.com refactor — 2026-04-10*
