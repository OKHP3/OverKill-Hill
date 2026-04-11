# Cross-Site Sync — Full Prompt for Glee-fully Tools & AskJamie

**From:** overkillhill.com (the gold standard — `OKHP3/OverKill-Hill`)
**Applies to:**
- **Glee-fully Tools** — https://glee-fully.tools / `OKHP3/Glee-fullyTools`
- **AskJamie** — https://askjamie.bot / `OKHP3/AskJamie`

**Date of sync:** 2026-04-10

---

## YOUR MISSION

Bring this site's HTML, CSS, JavaScript, meta tags, and repository files up to the same level of quality as overkillhill.com. That site is the gold standard. Scan every page and every root-level file, find every gap, fix everything you can, flag what you cannot.

Work through each part in order. Do not skip parts. Deliver the report specified in Part 9 when done.

---

## PART 1 — SCAN: INVENTORY EVERY PAGE AND ROOT FILE

Before changing anything:
- List every `.html` file on this site
- List every file in the repository root
- Note which gold-standard files (listed in Part 8) are missing

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
- `og:image` must be an absolute URL to an image that actually exists — verify the file is present
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
- `theme-color` should match this site's primary background colour
- `color-scheme` should reflect whether the site supports dark mode, light mode, or both

### 2I. Favicons (required on every page)

```html
<link rel="icon" href="/assets/img/favicons/favicon-32x32.png" sizes="32x32" type="image/png" />
<link rel="icon" href="/assets/img/favicons/favicon-16x16.png" sizes="16x16" type="image/png" />
<link rel="apple-touch-icon" href="/assets/img/favicons/apple-touch-icon.png" sizes="180x180" type="image/png" />
<link rel="icon" href="/favicon.ico" sizes="any" />
```

Rules:
- Verify that each file actually exists at these paths before adding the link tag
- If favicon files are at a different path on this site, adjust accordingly
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
- Place this block just before `</body>`, not in `<head>`
- One block per page

### 2K. Required order of tags inside `<head>`

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
13. Mobile / PWA tags
14. Favicons
15. CSS `<link rel="stylesheet">` tags
16. Any remaining `<link>` or `<meta>` tags

---

## PART 3 — INLINE STYLES: EXTRACT TO CSS

Scan every page for `style=""` attributes and `<style>` blocks inside `<head>` or `<body>`.

For each found:
1. For repeated patterns, create a named class in the site's CSS file
2. Replace `style=""` with `class="your-new-class"` in the HTML
3. For genuinely one-off styles, leave inline but note them in the report
4. Run a final check confirming zero unexpected `style=""` attributes remain

Exception: do not touch styles inside `type="application/ld+json"` blocks.

---

## PART 4 — INLINE SCRIPTS: EXTRACT TO JS

**Keep inline:**
- Google Analytics / gtag `dataLayer` and `gtag()` blocks
- `<script type="application/ld+json">` blocks

**Move to external files:**
- All other `<script>` blocks containing functions, event listeners, or initialisation logic
- Mermaid initialisation — see Part 5

---

## PART 5 — MERMAID JS: UPDATE TO v11 ESM PATTERN

### 5A. Find every Mermaid reference

Search all HTML and JS files for: `mermaid`, `cdn.jsdelivr.net/npm/mermaid`, `unpkg.com/mermaid`

Remove outdated patterns:
- `<script src="https://cdn.jsdelivr.net/npm/mermaid@[below-11]/...">` — non-module CDN tag
- `<script src="https://unpkg.com/mermaid...">` — outdated CDN
- Any inline `<script type="module"> import mermaid from ... </script>` blocks in HTML
- Any `mermaid.initialize(...)` inside `<script>` tags in HTML files

### 5B. Create or replace `assets/js/mermaid-init.js`

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

mermaid.run({
  querySelector: ".mermaid",
}).catch((err) => {
  console.warn("[mermaid-init] render error:", err);
});
```

### 5C. Reference the file in every page that uses diagrams

```html
<script type="module" src="/assets/js/mermaid-init.js"></script>
```

Place just before `</body>`, after the main `app.js` reference.

### 5D. Do not set `themeVariables` in `initialize()`

Setting `themeVariables` overrides YAML front matter on individual diagrams. Let each diagram control its own theme:

```
---
config:
  theme: neutral
  look: neo
---
```

---

## PART 6 — CSS ADDITIONS: CROSS-SITE UTILITY CLASSES

Append to the end of this site's main CSS file. Do not remove existing rules. After appending, bump the CSS cache-bust version on every `<link rel="stylesheet">` tag (e.g. `?v=1` → `?v=2`; if no version exists, add `?v=2`).

```css
/* ===== CROSS-SITE SYNC — from overkillhill.com refactor 2026-04-10 ===== */

.mermaid foreignObject,
.mermaid foreignObject div,
.mermaid foreignObject p,
.mermaid foreignObject span {
  color: initial;
}

.text-amber { color: var(--okh-amber, #F59E0B); }

.link-amber {
  color: var(--okh-amber, #F59E0B);
  text-decoration: underline;
}

.diagram-static-img {
  display: block;
  max-width: 100%;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.diagram-live-render { margin-bottom: 0; }

.diagram-live-render > summary {
  font-size: 0.82rem;
  color: var(--color-muted, #6b7280);
  cursor: pointer;
  margin-bottom: 0.5rem;
  list-style: none;
}

.diagram-live-render > summary::-webkit-details-marker { display: none; }

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

.council-card--compact { margin: 2rem 0; }

.council-note {
  font-size: 0.9rem;
  color: var(--color-muted, #6b7280);
  margin-bottom: 0.6rem;
  line-height: 1.6;
}

.council-note:last-of-type { margin-bottom: 0; }

.prompt-note {
  font-size: 0.85rem;
  color: var(--color-muted, #6b7280);
  margin-top: 0.6rem;
  margin-bottom: 0;
}

.btn-block-top {
  display: inline-block;
  margin-top: 0.5rem;
}

.article-repo-cta {
  font-size: 0.9rem;
  color: var(--color-muted, #6b7280);
  margin-top: 1rem;
}

.article-repo-cta .link-amber {
  text-decoration: none;
  color: var(--okh-amber, #F59E0B);
}

.article-repo-cta .link-amber:hover { text-decoration: underline; }

.sidebar-footnote {
  font-size: 0.78rem;
  color: var(--color-muted, #6b7280);
  margin-top: 0.6rem;
  line-height: 1.5;
}

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

@media (min-width: 1024px) {
  #toc-widget { will-change: transform; }
}

/* ===== END CROSS-SITE SYNC ===== */
```

---

## PART 7 — STICKY TOC (conditional — skip if no #toc-widget)

Only apply if the site has `id="toc-widget"` anywhere. Otherwise skip entirely.

Append to the end of the site's main `app.js`:

```js
(function () {
  if (window.innerWidth < 1024) return;
  var toc    = document.getElementById('toc-widget');
  var footer = document.querySelector('.site-footer');
  if (!toc || !footer) return;
  var lerpedY = 0, targetY = 0, SPEED = 0.08, NAV_H = 112, PAD = 32;
  function lerp(a, b, t) { return a + (b - a) * t; }
  function getNaturalTop(el) { var top = 0; while (el) { top += el.offsetTop; el = el.offsetParent; } return top; }
  var tocNaturalTop = getNaturalTop(toc), tocH = toc.offsetHeight;
  function tick() {
    var scrollY = window.scrollY, footerTop = footer.offsetTop;
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
    if (window.innerWidth >= 1024) { tocNaturalTop = getNaturalTop(toc); tocH = toc.offsetHeight; }
  });
}());
```

---

## PART 8 — REPOSITORY FILES: GOLD STANDARD

Every repository must have the following files at its root. Check which exist, create any that are missing, and update any that are incomplete, generic, or placeholder. Templates and rules for each file are below.

**Required file checklist:**
- [ ] `AGENTS.md`
- [ ] `CHANGELOG.md`
- [ ] `CNAME`
- [ ] `CODE_OF_CONDUCT.md`
- [ ] `CONTRIBUTING.md`
- [ ] `favicon.ico`
- [ ] `LICENSE`
- [ ] `LICENSE.md`
- [ ] `README.md`
- [ ] `ROADMAP.md`
- [ ] `robots.txt`
- [ ] `SECURITY.md`
- [ ] `site.webmanifest`
- [ ] `sitemap.xml`
- [ ] `404.html`

---

### 8A. `CNAME`

Single line, the bare domain. No `https://`, no trailing slash.

```
[yourdomain.com]
```

Examples: `glee-fully.tools` or `askjamie.bot`

---

### 8B. `robots.txt`

```
User-agent: *
Allow: /

# Block utility/template pages that are not content
Disallow: /under-construction.html

Sitemap: https://[yourdomain.com]/sitemap.xml
```

Rules:
- Replace `[yourdomain.com]` with the real domain
- Add additional `Disallow:` lines for any other pages that should not be indexed (staging pages, placeholder pages, etc.)
- The Sitemap line is mandatory — it must point to the actual sitemap file

---

### 8C. `site.webmanifest`

```json
{
  "name": "[Full Brand Name]",
  "short_name": "[Short Name]",
  "icons": [
    {
      "src": "/assets/img/favicons/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/assets/img/favicons/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#[primary-brand-hex]",
  "background_color": "#[background-hex]",
  "display": "standalone"
}
```

Rules:
- `name` should be the full brand name (e.g. "Glee-fully Personalizable Tools™" or "AskJamie™")
- `short_name` should be 12 characters or fewer (e.g. "Glee-fully" or "AskJamie")
- `theme_color` and `background_color` must match the site's brand colours — not left as `#ffffff`
- Verify that the icon files actually exist at the specified paths; if they do not, flag this in the report
- The `site.webmanifest` must be referenced in every page's `<head>` with: `<link rel="manifest" href="/site.webmanifest" />`

---

### 8D. `sitemap.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

  <url>
    <loc>https://[yourdomain.com]/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>

  <!-- Add one <url> block per public HTML page on the site -->
  <!-- Use priority 0.8 for key pages, 0.6 for secondary, 0.4 for legal/utility -->
  <!-- Do not include: 404.html, under-construction.html, or any Disallowed pages -->

</urlset>
```

Rules:
- Every public page on the site must have an entry
- URLs must be absolute with https and trailing slashes
- `changefreq`: home page = `weekly`, key content pages = `monthly`, legal = `yearly`
- `priority`: home = `1.0`, key pages = `0.8`, secondary = `0.6`–`0.7`, utility/legal = `0.4`
- Do not include pages that are `Disallow`-ed in `robots.txt`

---

### 8E. `LICENSE`

Plain text file (no `.md` extension). CC BY 4.0 adapted for this brand:

```
Creative Commons Attribution 4.0 International License (CC BY 4.0)

Copyright (c) 2026 [Brand Name] / Jamie Hill

This work is licensed under the Creative Commons Attribution 4.0 International License.

You are free to:
  Share — copy and redistribute the material in any medium or format
  Adapt — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
  Attribution — You must give appropriate credit, provide a link to the license,
  and indicate if changes were made. You may do so in any reasonable manner, but
  not in any way that suggests the licensor endorses you or your use.

No additional restrictions — You may not apply legal terms or technological
measures that legally restrict others from doing anything the license permits.

Full license text: https://creativecommons.org/licenses/by/4.0/legalcode
```

---

### 8F. `LICENSE.md`

```markdown
# License

Unless otherwise noted, the contents of this repository are © [Brand Name] / Jamie Hill.

This repository includes website source and brand materials intended for public viewing and reference.

You may read, reference, and link to this material freely.

Do not republish, commercialize, or redistribute brand assets, written content, or design artifacts as your own without permission.

For licensing or reuse questions, contact **[contact@yourdomain.com]**.
```

---

### 8G. `CODE_OF_CONDUCT.md`

```markdown
# Code of Conduct

All participants in **[Brand Name]** public repositories are expected to:

* Be respectful and civil.
* Avoid harassment, abusive language, or attacks.
* Ensure feedback is constructive and practical.
* Keep discussions focused on the content, artifacts, and public materials.

## Reporting violations

Please contact the maintainer at [contact@yourdomain.com] with evidence of behavior that violates this code of conduct.

Maintainers will review and respond appropriately. Repeated or severe violations may result in restriction from contributions.
```

---

### 8H. `SECURITY.md`

```markdown
# Security Policy

This repository contains public website and brand source materials.

## Reporting Issues

If you discover:
- exposed credentials
- misconfigured artifacts
- broken links or misleading content

please contact **[contact@yourdomain.com]** immediately.

## Scope

No bounty program exists at this time. Reports will be reviewed and mitigated as practical.

## Notes

This repo is primarily for reference and public brand artifact access.
```

---

### 8I. `CONTRIBUTING.md`

```markdown
# Contributing

Thanks for your interest in **[Brand Name]**.

This repository primarily contains public website source, brand artifacts, and supporting materials.

## Helpful contributions
- flagging broken links
- identifying rendering issues
- suggesting documentation clarifications
- proposing cleaner artifact organization for public pages

## Please avoid
- large unsolicited brand rewrites
- structural changes that break live site continuity
- adding placeholder or experimental content to public-facing pages without alignment

## How to contribute
1. Be specific about the file, page, or artifact in question.
2. Describe the problem first, then the proposed improvement.
3. Keep suggestions practical, respectful, and public-artifact focused.

## Maintainer
Jamie Hill / [Brand Name]
[contact@yourdomain.com]
```

---

### 8J. `AGENTS.md`

```markdown
# Agent rules

- Work in small steps. Ask before large refactors.
- Prefer adding tests before changing logic if risk is medium/high.
- Keep changes localized. Avoid touching unrelated files.
- If you need config/secrets, stop and ask. Never invent credentials.
- Summarize what you changed and why at the end.
```

This file is identical across all three sites — no customisation needed.

---

### 8K. `README.md`

The README must be substantive, specific to this brand, and honest about what the site/product is. It must not be a placeholder or copy of another site's README.

Required sections:
1. **Brand name as H1 heading**
2. **One-paragraph brand description** — what this product is and who it is for
3. **What it does / what it builds** — key features or offerings, specific to this brand
4. **Why it matters** — the philosophy or mission behind it
5. **Explore** — website URL, contact email, and any relevant external links (Ko-fi, LinkedIn, etc.)
6. **Closing tagline** — one memorable line that captures the brand voice

Tone must match the brand voice of this specific site. Do not use OverKill Hill P³ language in the Glee-fully or AskJamie READMEs — each brand has its own voice.

---

### 8L. `CHANGELOG.md`

```markdown
# Changelog

All notable changes to the **[Brand Name]** public repository should be recorded here.

## [Unreleased]

### Planned
- [List near-term improvements specific to this site]

## [v0.1 — 2026-04-10]

### Established
- Core brand README
- Public website source for [yourdomain.com]
- Repository governance files (LICENSE, SECURITY, CODE_OF_CONDUCT, CONTRIBUTING, ROADMAP)
- Full meta tag pass across all pages
- Cross-site CSS and JS sync with overkillhill.com
- Mermaid JS updated to v11 ESM pattern
```

Rules:
- The `[v0.1 — 2026-04-10]` section should reflect what was actually set up on this date
- Add a bullet for every meaningful change made during this sync session
- Date format: `YYYY-MM-DD`

---

### 8M. `ROADMAP.md`

```markdown
# Roadmap

This roadmap outlines the near-term public direction for the **[Brand Name]** repository.

## Current
- [What is actively being worked on for this site right now]

## Next
- Improve repository-level documentation and governance
- Expand content and feature pages
- Align public page content with live LinkedIn and platform artifacts

## Later
- Continue evolving public case studies and documentation
- Improve cross-linking between OverKill Hill, Glee-fully, AskJamie, and supporting repositories
- Add more structured project indexes
```

Customise each section to reflect the actual roadmap priorities for this specific site. Do not copy the OverKill Hill roadmap verbatim.

---

### 8N. `404.html`

A custom 404 page must exist. It must:
- Match the site's design (header, footer, brand colours, fonts)
- Have a correct `<title>` tag: `[Site Name] — 404 Page Not Found`
- Contain a helpful heading and message explaining the page wasn't found
- Include a clear link or button back to the home page
- Include the full meta tag set from Part 2 (simplified — `og:type` = `website`, no `og:article` tags)
- Not be a default server/framework 404 page

If no `404.html` exists, create one. If one exists but is a default/generic page, rewrite it to match the site's design.

---

### 8O. `favicon.ico` (root level)

A `favicon.ico` file must exist at the repository root. This is separate from the favicon PNGs in `assets/img/favicons/`. If it is missing, flag it as a critical item — the user must provide the file.

---

## PART 9 — DELIVERY REPORT

When all work is complete, provide a structured report covering:

1. **Pages scanned** — every HTML file found and checked
2. **Repository files** — full checklist: which existed, which were created, which were updated
3. **Meta tag gaps fixed** — per page, which tags were missing or incorrect before your changes
4. **Meta tags still incomplete** — any tag you could not populate (state exactly what is needed and who must provide it)
5. **Inline styles** — count found, count extracted, count left inline with reason
6. **Inline scripts** — count found, count externalised, what was kept and why
7. **Mermaid** — version confirmed, pages updated, old pattern replaced
8. **CSS additions** — confirmed appended, cache-bust version before and after
9. **JSON-LD** — which pages had it, which had it added, any needing manual input
10. **sitemap.xml** — list of URLs included
11. **site.webmanifest** — confirmed values (name, short_name, theme_color, background_color)
12. **Orphaned or broken files** — any unreferenced files or dead links
13. **Items requiring your manual action** — anything the agent cannot resolve, described clearly with what is needed from you

---

*Gold standard source: overkillhill.com — refactor completed 2026-04-10*
*Apply this prompt in each site's own Replit project session.*
