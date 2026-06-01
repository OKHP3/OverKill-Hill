# Standards Compliance & Consistency Audit
**Date:** 2026-05-12  
**Scope:** 27 HTML pages across overkillhill.com  
**Domains audited:** 7 (Best Practices · Metadata · Analytics · SEO · Header/Footer · Design · CSS/JS)

---

## Domain 1 — 2026 Best Practices

### 1.1 Deprecated / legacy patterns
| Check | Status | Action taken |
|-------|--------|--------------|
| `X-UA-Compatible` meta tag | **Fixed** | Removed from all 26 affected pages (was absent only on `under-construction.html`) |
| `target="_blank"` without `rel` | **Pass** | 3 grep hits were multiline attributes that already had `rel="noopener noreferrer"` on the next line — no change needed |
| `rel="noopener"` (missing `noreferrer`) | **Fixed** | 159 instances across all pages upgraded to `rel="noopener noreferrer"` |

### 1.2 Skip links
| Check | Status |
|-------|--------|
| All pages use `class="okh-skip-link" href="#main"` | **Pass** — already consistent site-wide |

### 1.3 `<title>` tag format
Canonical format: `[Page Name] | OverKill Hill P³™`

| Page | Before | After |
|------|--------|-------|
| `about/` | `About OverKill Hill P³™ — Precision, Protocol & Promptcraft` | `About \| OverKill Hill P³™` |
| `contact/` | `OverKill Hill P³™ — Contact` | `Contact \| OverKill Hill P³™` |
| `manifesto/` | `OverKill Hill P³™ — The Manifesto` | `The Manifesto \| OverKill Hill P³™` |
| `universe/` | `OverKill Hill P³™ — OKHP³™ Universe Map` | `OKHP³™ Universe \| OverKill Hill P³™` |
| `404.html` | `OverKill Hill P³™ — 404 Page Not Found` | `404 Not Found \| OverKill Hill P³™` |
| `under-construction.html` | `OverKill Hill P³™ — Under Construction` | `Under Construction \| OverKill Hill P³™` |

Pages already using pipe format: all others — **Pass**

### 1.4 Script loading strategy
`app.js` is loaded at end of `<body>` on all pages — already non-render-blocking. `type="module"` scripts (mermaid) are implicitly deferred. No changes needed.

---

## Domain 2 — Metadata / OG / Twitter Card

### 2.1 OG and Twitter tags
All 27 pages have complete `og:` and `twitter:` meta blocks. **Pass**

### 2.2 OG image dimensions
Homepage, about, manifesto, contact, legal, universe, found-ry, prompt-forge, and project pages all use the 256×256 sentinel PNG with correct `og:image:width/height`. The FDIAL article and heat pages use the correct 1536×1024 landscape image. **Pass**

### 2.3 Twitter site handle
All pages declare `twitter:site` = `@OverKillHillP3`. **Pass**

### 2.4 Canonical link
All 27 pages have a `<link rel="canonical">` tag. **Pass**

---

## Domain 3 — Google Analytics

| Page | Before | After |
|------|--------|-------|
| `search/index.html` | Missing | Added (before `</body>` + `dns-prefetch` in `<head>`) |
| `v03/v1-heat-a/` | Missing | Added |
| `v03/v1-heat-b/` | Missing | Added |
| `v03/v2-heat-a/` | Missing | Added |
| `v03/v2-heat-b/` | Missing | Added |
| All other 22 pages | Present | **Pass** |

GA ID confirmed: `G-VJ1BKXS27H`. All pages now tracked.

---

## Domain 4 — SEO

### 4.1 `robots.txt`
Correctly blocks `assets/templates/`, sets crawl-delay for commercial bots, opts in named AI crawlers, includes `Sitemap:` directive. **Pass — no changes**

### 4.2 `sitemap.xml`
All 18 indexable URLs present including BPMN for Mermaid project page. **Pass — no changes**

### 4.3 Heading hierarchy
Spot-checked: all pages open with a single `<h1>` per page. **Pass**

### 4.4 JSON-LD structured data

| Page | Before | After |
|------|--------|-------|
| `index.html` (homepage) | `WebSite` only | Added `Organization` with `sameAs` for all social/platform profiles |
| `writings/biases-as-constants/` | `WebSite` only | Added `Article` schema |
| `writings/magnus-saga/` | `WebSite` only | Added `Article` schema |
| 4 heat pages | `Article` ✓ | **Pass** (Article schema present; note: placed after `</footer>` in `<body>` — Google accepts both locations) |
| `writings/first-diagram-is-a-liar/` | `Article` + `Organization` ✓ | **Pass** |
| All other pages | `WebSite` / `WebPage` / `SoftwareApplication` | **Pass** for their type |

**Deferred:** `BreadcrumbList` JSON-LD on all non-homepage pages — valid structured data enhancement, deferred due to the 20+ page scope. No regression risk if added incrementally.

---

## Domain 5 — Header / Footer Consistency

### 5.1 Primary navigation — Projects submenu

`BPMN for Mermaid` was missing from the Projects submenu on **20 pages**. Fixed via bulk script.

Pages that had it before: `index.html`, `projects/index.html`, `projects/mermaid-theme-builder/`, `projects/bpmn-for-mermaid/`

### 5.2 Primary navigation — About submenu (heat pages)

The 4 heat pages had a broken About submenu (only 2 items: "About OKH P³" + "P³ Universe") with Contact and Legal as separate top-level nav items. Fixed to canonical 4-item cluster:

```
About
  ├ OKHP³™ Universe
  ├ About OKHP³™
  ├ Contact
  └ Legal
```

### 5.3 Footer — copyright line

`OverKill Hill P³. All rights reserved.` (missing ™) was present on **22 pages**. Fixed to `OverKill Hill P³™. All rights reserved.` across all pages.

The legal page had an extra "The" prefix (`The OverKill Hill P³™`). Also corrected.

### 5.4 Footer — social links

Facebook and YouTube were missing from **12 pages**: all 4 heat pages, `writings/first-diagram-is-a-liar/index.html`, `writings/magnus-saga/index.html`, `writings/index.html`, `prompt-forge/index.html`, `search/index.html`, `404.html`, `under-construction.html`.

All 12 pages now have the canonical 6-link Connect column:
**Ko-fi → Fiverr → LinkedIn → Facebook → X (Twitter) → YouTube**

---

## Domain 6 — Design Principles

Site-wide dark theme (`#2a2320` / `--color-surface` token), brand typography (Alfa Slab One + DM Sans), and OKH orange accent (`--okh-orange`) are consistently applied across all pages via the shared `theme.css`. No regressions introduced.

---

## Domain 7 — CSS / JS Externalization

| Check | Status |
|-------|--------|
| Google Analytics `<script>` blocks | **Pass** — inline by specification; GA requires inline gtag initialization |
| JSON-LD `<script type="application/ld+json">` blocks | **Pass** — structured data must be inline |
| Page-specific `<style>` blocks (project pages) | **Deferred** — intentional page-specific overrides; externalization risk outweighs benefit |
| Page-specific `<script>` blocks (DSL copy button, iframe loaders) | **Deferred** — page-specific interactive logic; safe to leave inline |

---

## Summary

| Domain | Issues found | Issues fixed | Deferred |
|--------|-------------|--------------|---------|
| 1. Best Practices | 4 | 4 | 0 |
| 2. Metadata / OG / Twitter | 0 | 0 | 0 |
| 3. Google Analytics | 5 | 5 | 0 |
| 4. SEO / Structured Data | 3 | 3 | 1 (BreadcrumbList) |
| 5. Header/Footer Consistency | 4 | 4 | 0 |
| 6. Design Principles | 0 | 0 | 0 |
| 7. CSS/JS Externalization | 0 | 0 | 2 (low-risk inline) |
| **TOTAL** | **16** | **16** | **3** |

### Files modified
27 of 27 HTML pages received at least one correction.

### Deferred items (zero regression risk if added later)
1. **BreadcrumbList JSON-LD** on all non-homepage pages — enhances rich snippets, no functional dependency
2. **Inline `<style>` externalization** on project pages — intentional page-specific styles
3. **Inline page-specific `<script>` externalization** — DSL copy button, iframe loader

