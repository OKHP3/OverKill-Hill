# Cross-Site Sync — Full Prompt for Glee-fully Tools & AskJamie

**From:** overkillhill.com (the gold standard — `OKHP3/OverKill-Hill`)
**Applies to:**
- **Glee-fully Tools** — https://glee-fully.tools / `OKHP3/Glee-fullyTools`
- **AskJamie** — https://askjamie.bot / `OKHP3/AskJamie`

**Date of sync:** 2026-04-10

---

## YOUR MISSION

Bring this site's HTML, CSS, JavaScript, and meta tags up to the same level of quality as overkillhill.com. That site is the gold standard. Scan every page, find every gap, fix everything you can, flag what you cannot.

Work through each part in order. Do not skip parts. Deliver the report specified in Part 8 when done.

---

## PART 1 — SCAN: INVENTORY EVERY PAGE

Before changing anything, find and list every `.html` file on this site. Apply every check in Parts 2–7 to each one.

---

## PART 2 — META TAGS: GOLD STANDARD

Every page on this site must have the full meta tag set described below. This is the exact pattern used on overkillhill.com. Adapt the content (title, description, image, URL, etc.) to this site — do not copy overkillhill.com's content — but the structure and completeness of every tag must match.

### 2A. Core tags (required on every page)

```html
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="language" content="English" />
```

### 2B. Title

```html
<title>Page Name | Site Name — Tagline</title>
```

Rules:
- Must be unique per page — no two pages share an identical `<title>`
- Must be descriptive, not generic ("Home" or "Page" is not acceptable)
- Include the site name in every title using a consistent separator (`|` or `—`)
- Maximum ~60 characters recommended for SEO

### 2C. Core SEO meta tags

```html
<meta name="description" content="[Specific, substantive description of this page. 1–2 sentences. 120–155 characters. Written for humans, useful to search engines.]" />
<meta name="keywords" content="[comma, separated, relevant, terms, brand name, product name, topic]" />
<meta name="author" content="[Site/Brand Name]" />
<meta name="creator" content="[Site/Brand Name]" />
<meta name="publisher" content="[Site/Brand Name]" />
```

Rules:
- `description` must be unique per page — no two pages share an identical description
- `description` must not be empty, placeholder text, or "Coming soon"
- `keywords` should be specific to the page content, not just the site brand
- All three name/creator/publisher tags are required on every page

### 2D. Open Graph tags (required on every page)

```html
<meta property="og:title" content="[Same as <title> or close variant]" />
<meta property="og:description" content="[Same as or close variant of meta description]" />
<meta property="og:type" content="website" />
<!-- Use og:type="article" for individual article/post/tool pages -->
<meta property="og:url" content="https://[yourdomain.com]/[path/to/page]/" />
<meta property="og:image" content="https://[yourdomain.com]/assets/img/[your-og-image.png]" />
<meta property="og:image:alt" content="[Descriptive alt text for the OG image — what does it show?]" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:type" content="image/png" />
<meta property="og:site_name" content="[Site/Brand Name]" />
<meta property="og:locale" content="en_US" />
```

Rules:
- `og:url` must be the canonical absolute URL of the page (https, trailing slash, no query strings)
- `og:image` must be an absolute URL to an image that actually exists on the server — verify the file is present
- `og:image:alt` must not be empty and must describe the image in plain language
- Recommended OG image dimensions: 1200×630 px (landscape) — minimum 600×315 px
- If no suitable OG image exists for this site, flag it as a critical item in the report and use the best available image as a placeholder

### 2E. Twitter / X Card tags (required on every page)

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="[Same as og:title]" />
<meta name="twitter:description" content="[Same as og:description]" />
<meta name="twitter:image" content="[Same as og:image — absolute URL]" />
<meta name="twitter:image:alt" content="[Same as og:image:alt]" />
<meta name="twitter:site" content="@[TwitterHandle]" />
<meta name="twitter:creator" content="@[TwitterHandle]" />
```

Rules:
- `twitter:card` must be `summary_large_image` (not `summary`)
- `twitter:site` and `twitter:creator` must be the correct Twitter/X handle for this brand
- If this site does not have a dedicated Twitter handle, use `@OverKillHillP3` as the fallback

### 2F. Crawl and indexing tags (required on every page)

```html
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<meta name="googlebot" content="index, follow" />
<meta name="bingbot" content="index, follow" />
<meta name="revisit-after" content="7 days" />
```

### 2G. Canonical URL (required on every page)

```html
<link rel="canonical" href="https://[yourdomain.com]/[path/to/page]/" />
```

Rules:
- Must be the absolute URL of this specific page
- Must match the `og:url` value exactly
- Must be present on every page — not just the home page

### 2H. Mobile and PWA tags (required on every page)

```html
<meta name="theme-color" content="#[your-brand-color-hex]" />
<meta name="color-scheme" content="dark light" />
<meta name="mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
```

Rules:
- `theme-color` should match this site's primary background colour (dark sites: dark hex; light sites: brand accent hex)
- `color-scheme` should reflect whether the site supports dark mode, light mode, or both

### 2I. Favicons (required on every page)

```html
<link rel="icon" href="/assets/img/favicons/favicon-32x32.png" sizes="32x32" type="image/png" />
<link rel="icon" href="/assets/img/favicons/favicon-16x16.png" sizes="16x16" type="image/png" />
<link rel="apple-touch-icon" href="/assets/img/favicons/apple-touch-icon.png" sizes="180x180" type="image/png" />
<link rel="icon" href="/favicon.ico" sizes="any" />
```

Rules:
- Verify that each file actually exists at the specified path before adding the link tag
- If the favicon files live at a different path on this site, adjust the paths accordingly
- If favicon files are missing entirely, flag this as a critical item in the report

### 2J. JSON-LD Structured Data (required on every page)

Every page needs a `<script type="application/ld+json">` block placed just before `</body>`.

**For the home page and general/about pages** — use `WebSite` type:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "[Site/Brand Name]",
  "url": "https://[yourdomain.com]",
  "description": "[Same as meta description for this page]",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://[yourdomain.com]/?s={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
</script>
```

**For individual article, post, or tool pages** — use `Article` type:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Page title]",
  "description": "[Same as meta description for this page]",
  "author": {
    "@type": "Person",
    "name": "Jamie Hill",
    "url": "https://www.linkedin.com/in/jamiehill75"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[Site/Brand Name]",
    "url": "https://[yourdomain.com]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD — use 2026-04-10 if not known]",
  "image": "https://[yourdomain.com]/assets/img/[your-og-image.png]",
  "url": "https://[yourdomain.com]/[path/to/page]/"
}
</script>
```

Rules:
- The JSON must be valid — double-check before writing it
- `dateModified` must reflect the actual last modification date; use 2026-04-10 if unknown
- Place this block just before `</body>`, not in `<head>`
- One block per page

### 2K. Required order of tags inside `<head>`

Follow this order exactly:
1. `<meta charset>`
2. `<meta viewport>`
3. `<meta http-equiv>`
4. `<meta language>`
5. `<title>`
6. `<meta name="description">`
7. `<meta name="keywords">`
8. `<meta name="author">`, `creator`, `publisher`
9. Open Graph `<meta property="og:*">` tags (title, description, type, url, image, image:alt, image:width, image:height, image:type, site_name, locale)
10. Twitter `<meta name="twitter:*">` tags (card, title, description, image, image:alt, site, creator)
11. Robots / crawl tags (robots, googlebot, bingbot, revisit-after)
12. `<link rel="canonical">`
13. Mobile / PWA tags (theme-color, color-scheme, mobile-web-app-capable, apple tags)
14. Favicons
15. CSS `<link rel="stylesheet">` tags
16. Any remaining `<link>` or `<meta>` tags

---

## PART 3 — INLINE STYLES: EXTRACT TO CSS

Scan every page for:
- `style=""` attributes on HTML elements
- `<style>...</style>` blocks inside `<head>` or `<body>`

For each found:
1. For patterns that repeat across multiple elements or pages, create a named class in the site's CSS file
2. Replace the `style=""` attribute in HTML with `class="your-new-class"`
3. For genuinely one-off styles appearing only once with no likely reuse, leave inline but note them in the report
4. After all changes, run a final check to confirm zero unexpected `style=""` attributes remain

Exception: do not touch styles inside `type="application/ld+json"` blocks.

---

## PART 4 — INLINE SCRIPTS: EXTRACT TO JS

Scan every page for `<script>` blocks containing logic (not data).

**Keep inline — these must not be moved:**
- Google Analytics / gtag `dataLayer` initialisation and `gtag()` config blocks (industry standard requirement)
- `<script type="application/ld+json">` structured data blocks

**Move to external files:**
- Any other `<script>` block containing functions, event listeners, or initialisation logic
- Mermaid initialisation — see Part 5 for the correct external file pattern

---

## PART 5 — MERMAID JS: UPDATE TO v11 ESM PATTERN

### 5A. Find every Mermaid reference on the site

Search all HTML and JS files for: `mermaid`, `cdn.jsdelivr.net/npm/mermaid`, `unpkg.com/mermaid`

Outdated patterns to remove:
- `<script src="https://cdn.jsdelivr.net/npm/mermaid@[below-11]/...">` — non-module CDN tag
- `<script src="https://unpkg.com/mermaid...">` — unpkg CDN, outdated
- Any inline `<script type="module"> import mermaid from ... </script>` blocks in HTML files
- Any `mermaid.initialize(...)` calls inside `<script>` tags in HTML

### 5B. Create or replace `assets/js/mermaid-init.js`

If this file does not exist, create it. If it does, replace its entire content:

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

### 5C. Add the reference to every page that uses diagrams

Place this tag just before `</body>`, after your main `app.js` reference:

```html
<script type="module" src="/assets/js/mermaid-init.js"></script>
```

### 5D. Why `initialize()` must not set `themeVariables`

Setting `themeVariables` inside `initialize()` silently overrides any YAML front matter on individual diagrams. The correct pattern is to let each diagram control its own theme:

```
---
config:
  theme: neutral
  look: neo
---
```

Add this YAML at the top of each `<pre class="mermaid">` block only on diagrams that need explicit theme control. The `initialize()` call must not interfere.

---

## PART 6 — CSS ADDITIONS: CROSS-SITE UTILITY CLASSES

Open this site's main CSS file and append the following block at the very end, after all existing rules. Do not remove or overwrite anything — append only.

After appending, bump the cache-bust version on every `<link rel="stylesheet">` tag in every HTML file (e.g. `?v=1` → `?v=2`). If no version string exists, add `?v=2`.

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

/* Prompt meta note */
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

/* Sidebar footnote */
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

## PART 7 — STICKY TOC (conditional — skip if no #toc-widget)

Only apply this section if the site has a sidebar table of contents element with `id="toc-widget"`. If it does not exist anywhere on the site, skip this part entirely.

Append the following to the end of the site's main `app.js`:

```js
// ──────────────────────────────────────────────────────────────
// Sticky TOC: lerp scroll-follow (only on screens >= 1024px)
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

---

## PART 8 — DELIVERY REPORT

When all work is complete, provide a structured report covering:

1. **Pages scanned** — every HTML file found and checked
2. **Meta tag gaps fixed** — per page, list which tags were missing or incorrect before your changes
3. **Meta tags still incomplete** — any tag you could not populate because information was unavailable (e.g. OG image file missing, Twitter handle unknown) — state exactly what is needed and who must provide it
4. **Inline styles** — count found, count extracted to CSS, count left inline with reason for each
5. **Inline scripts** — count found, count externalised, what was kept inline and why
6. **Mermaid** — version confirmed, how many pages updated, old pattern that was replaced
7. **CSS additions** — confirmed appended, cache-bust version before and after on each page
8. **JSON-LD** — which pages had it before, which pages had it added, any that still need manual input
9. **Orphaned or broken files** — any files not referenced anywhere, or `<link>`/`<script>`/`<img>` tags pointing to missing files
10. **Items requiring your manual action** — anything the agent cannot resolve itself, described clearly with the specific information or file needed from you

---

*Gold standard source: overkillhill.com — refactor completed 2026-04-10*
*Apply this prompt in each site's own Replit project session.*
