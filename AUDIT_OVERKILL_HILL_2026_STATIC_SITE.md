# OverKill Hill P³™ — 2026 Static-Site Audit

**Date:** 2026-05-26  
**Scope:** All production HTML pages, `sitemap.xml`, `robots.txt`, `site.webmanifest`, `assets/scripts/validate_site.py`  
**Pages audited:** 28 production HTML files  
**Methodology:** Automated script analysis (`validate_site.py`) + manual phase-by-phase inspection  
**Auditor:** Sprint 4 remediation pass (Task #35)

---

## Executive Summary

The site is in strong structural health. All 28 pages pass title, description, canonical, H1, and internal-link checks. No broken links, no missing alt text, no target-blank safety gaps. The primary issues found were: a **script-breaking ROOT bug** in `validate_site.py` that caused 0 pages to be found, **17 pages with a missing ™ symbol** in the footer brand name, **6 noindex pages incorrectly listed in sitemap.xml**, and a **stale content block** on the homepage. All critical issues were remediated in-session.

---

## Phase 0 — Environment & Tooling

| Check | Result |
|-------|--------|
| Python server running | ✓ `python3 server.py` via "Start application" workflow |
| `validate_site.py` functional | **✖ FAIL** — ROOT bug caused 0 pages found |
| `build-search-index.py` | ✓ present, last index at 58 entries |
| `reorg-theme-css.py` | ✓ present |

### Finding 0-A — validate_site.py ROOT miscalculation (CRITICAL)

**Severity:** CRITICAL  
**File:** `assets/scripts/validate_site.py`, line 34  
**Detail:** `ROOT = Path(__file__).resolve().parent.parent` resolves to `assets/` (not the workspace root) because the script lives at `assets/scripts/validate_site.py`. Two `.parent` calls reach `assets/`; three are needed to reach the project root. The script reported "Validating 0 HTML pages — ✓ all clean" despite real issues existing.  
**Status:** ✅ Fixed — changed to `.parent.parent.parent`

### Finding 0-B — validate_site.py SKIP_DIRS missing `.agents`

**Severity:** HIGH  
**File:** `assets/scripts/validate_site.py`, line 38  
**Detail:** The `.agents/` directory contains internal Replit skill HTML files that are not production pages. They lack `<meta name="description">`, canonical, and sitemap entries by design. Without `.agents` in `SKIP_DIRS`, the validator emitted false-positive errors against these files.  
**Status:** ✅ Fixed — added `.agents` to `SKIP_DIRS`

---

## Phase 1 — Brand Consistency

### Finding 1-A — Footer ™ symbol missing on 17 pages (HIGH)

**Severity:** HIGH  
**Pages affected (17):**
- `about/index.html`
- `contact/index.html`
- `found-ry/index.html`
- `manifesto/index.html`
- `projects/abrahamic-reference-engine/index.html`
- `projects/bfs-framing-intelligent-futures/index.html`
- `projects/bpmn-for-mermaid/index.html`
- `projects/hometools/index.html`
- `projects/mac-studio-local-ai-workbench/index.html`
- `projects/mermaid-theme-builder/index.html`
- `projects/pathscrib-r/index.html`
- `projects/un-nocked-truth/index.html`
- `prompt-forge/index.html`
- `universe/index.html`
- `writings/biases-as-constants/index.html`
- `writings/index.html`
- `writings/magnus-saga/index.html`

**Detail:** Footer `<h3>` read `OverKill&nbsp;Hill&nbsp;P³` (missing `™`). Three pages (bpmn, mermaid-theme-builder, mac-studio) additionally had a "The " prefix: `<h3>The OverKill&nbsp;Hill&nbsp;P³™</h3>`. Canonical form is `OverKill&nbsp;Hill&nbsp;P³™`.  
**Status:** ✅ Fixed — bulk replacement across all 17 files; "The " prefix also removed from 3 files

### Finding 1-B — about/index.html og:title and twitter:title comma-separator (MEDIUM)

**Severity:** MEDIUM  
**File:** `about/index.html`, lines 24 and 40  
**Detail:** `og:title` and `twitter:title` read `"About OverKill Hill P³™ — Precision, Protocol &amp; Promptcraft"`. The tagline uses a comma `,` between terms where the brand standard is a middle dot `·`: `"Precision · Protocol · Promptcraft"`. The homepage og:title correctly uses middots.  
**Status:** ✅ Fixed — changed both attributes to `"About OverKill Hill P³™ — Precision · Protocol · Promptcraft"`

### Finding 1-C — og:title em-dash format on some pages (LOW)

**Severity:** LOW (informational)  
**Pages:** `contact/index.html`, `universe/index.html`, `404.html`, `under-construction.html`  
**Detail:** These pages use `Brand — Section` format with an em-dash, while most pages use `Section | Brand` with a pipe. Both are valid OG title patterns; the em-dash form is used intentionally on the homepage and core brand pages. No fix applied — this is an acceptable stylistic split.

---

## Phase 2 — Content Freshness

### Finding 2-A — Homepage "Fresh from the Forge" blurb is stale v0.4 copy (HIGH)

**Severity:** HIGH  
**File:** `index.html`, lines 246–252  
**Detail:** The article teaser card read "v0.4 is now live... The Council's own scoring and member interviews come in v0.5." v0.5 has been live since 2026-05-24. A visitor reading the homepage would think v0.5 was still upcoming.  
**Status:** ✅ Fixed — updated to v0.5-accurate copy reflecting the scoring results and meta-finding

---

## Phase 3 — SEO / Sitemap Integrity

### Finding 3-A — 6 noindex pages listed in sitemap.xml (HIGH)

**Severity:** HIGH  
**File:** `sitemap.xml`  
**Detail:** Eight pages marked `noindex, nofollow` were still present in `sitemap.xml`. Submitting noindex pages to a sitemap sends conflicting signals to search engines (the sitemap says "please crawl this" while the robots meta says "do not index"). The initial manual pass caught 6; the new automated check in `validate_site.py` caught 2 more (`biases-as-constants` and `magnus-saga`). Pages removed:

| URL | robots meta |
|-----|-------------|
| `/found-ry/` | noindex, nofollow |
| `/prompt-forge/` | noindex, nofollow |
| `/writings/biases-as-constants/` | noindex, nofollow |
| `/writings/magnus-saga/` | noindex, nofollow |
| `/projects/abrahamic-reference-engine/` | noindex, nofollow |
| `/projects/hometools/` | noindex, nofollow |
| `/projects/pathscrib-r/` | noindex, nofollow |
| `/projects/un-nocked-truth/` | noindex, nofollow |

**Status:** ✅ Fixed — all 8 removed from `sitemap.xml`

### Finding 3-B — Sitemap orphaned comment blocks (LOW)

**Severity:** LOW  
**File:** `sitemap.xml`  
**Detail:** After the noindex page removal, two comment blocks were orphaned: `<!-- FLAG: found-ry — brand/portfolio page; confirm indexability -->` (sitting above heat-guide URLs it did not belong to) and `<!-- FLAG: secondary project pages — confirm indexability for each -->` (referencing pages that were all removed). Additionally, `bfs-framing-intelligent-futures` (which has no noindex) was incorrectly grouped under the "secondary project pages" flag comment.  
**Status:** ✅ Fixed — sitemap reorganized into clean sections: CORE PAGES, v0.3 HEAT FIELD GUIDE SUB-PAGES, ADDITIONAL INDEXABLE PAGES, UTILITY

### Finding 3-C — sitemap.xml URL count

**Before audit:** 26 URLs (including 8 noindex pages)  
**After audit:** 18 URLs (all indexable)

---

## Phase 4 — Analytics

### Finding 4-A — GA4 script in `<body>` on all 28 pages (LOW/INFO)

**Severity:** LOW (informational)  
**Detail:** Google Analytics tag (G-VJ1BKXS27H) is loaded after `</body>` (actually inside `<body>` at the bottom) on all 28 pages, not in `<head>`. Google documents that the tag "should" be placed in `<head>` for reliable firing before page unload. However, Google's own Tag Manager and many CMS templates install it in the body. The current placement is widely used and functionally acceptable. Moving it to `<head>` carries regression risk without a clear measurement benefit on a static site.  
**Status:** Documented only — no fix applied. Revisit if bounce-rate measurement gaps appear.

---

## Phase 5 — Structured Data (JSON-LD)

### Summary table

| Page | WebSite | Organization | BreadcrumbList |
|------|---------|--------------|----------------|
| `index.html` | ✓ | ✓ | — |
| `about/index.html` | ✓ | — | ✓ |
| `contact/index.html` | ✓ | — | ✓ |
| `legal/index.html` | ✓ | — | ✓ |
| `manifesto/index.html` | ✓ | — | ✓ |
| `universe/index.html` | ✓ | — | ✓ |
| `found-ry/index.html` | ✓ | — | — |
| `search/index.html` | ✓ | — | — |
| `under-construction.html` | ✓ | — | — |
| `projects/index.html` | ✓ | — | ✓ |
| `projects/mermaid-theme-builder/` | — | ✓ | ✓ |
| `projects/bpmn-for-mermaid/` | — | ✓ | ✓ |
| `projects/mac-studio-local-ai-workbench/` | — | ✓ | ✓ |
| `projects/bfs-framing-intelligent-futures/` | ✓ | — | — |
| `projects/abrahamic-reference-engine/` | ✓ | — | — |
| `projects/hometools/` | ✓ | — | — |
| `projects/pathscrib-r/` | ✓ | — | — |
| `projects/un-nocked-truth/` | ✓ | — | — |
| `prompt-forge/index.html` | ✓ | ✓ | ✓ |
| `writings/index.html` | ✓ | — | ✓ |
| `writings/biases-as-constants/` | ✓ | ✓ | ✓ |
| `writings/magnus-saga/` | ✓ | ✓ | ✓ |
| `writings/first-diagram-is-a-liar/` | — | ✓ | ✓ |
| `v03/v1-heat-a/` | — | ✓ | — |
| `v03/v1-heat-b/` | — | ✓ | — |
| `v03/v2-heat-a/` | — | ✓ | — |
| `v03/v2-heat-b/` | — | ✓ | — |
| `404.html` | ✓ | — | — |

**Findings:**  
- `mermaid-theme-builder`, `bpmn-for-mermaid`, `mac-studio` lack WebSite JSON-LD (have Organization instead) — minor  
- `bfs-framing-intelligent-futures`, `abrahamic-reference-engine`, `hometools`, `pathscrib-r`, `un-nocked-truth`, `found-ry`, `search`, `under-construction`, 4 heat guide pages — all lack BreadcrumbList — LOW priority, noted for future sprint

---

## Phase 6 — Accessibility

| Check | Result |
|-------|--------|
| Skip link on all pages | ✅ Present on all 28 pages |
| Single H1 per page | ✅ All 28 pages have exactly 1 H1 |
| `alt` attribute on all `<img>` | ✅ No missing alt text found |
| `rel="noopener"` on all external `target="_blank"` | ✅ No violations found |
| `aria-current="page"` present on active nav item | ✅ All 28 pages except heat guides (which have no nav item to mark) and search (no nav item in nav for search) |
| `mac-studio-local-ai-workbench` has 2 `aria-current="page"` | ⚠ Low — duplicate aria-current in same page (nav + sub-nav) |

---

## Phase 7 — Performance Signals

| Check | Result |
|-------|--------|
| Speculative prefetch rules on all pages | ✅ All 28 pages |
| `loading="lazy"` on non-hero images | ✓ Confirmed on homepage hero illustration |
| `width` + `height` on images | ✓ Confirmed on audited pages |
| CSS cache-bust version | `?v=15` (current) |

---

## Phase 8 — robots.txt

**File:** `robots.txt`  
**Status:** Well-structured. 13 User-agent blocks covering all major AI crawlers plus SEO bots with rate-limiting. Disallows: `404.html`, `under-construction.html`, `assets/templates/`. All blocked paths are non-production.

**Finding:** `robots.txt` still disallows `prompt-forge/` and `found-ry/` indirectly via `noindex` (but robots.txt itself does not explicitly disallow them). These pages are crawlable but noindex — the `noindex` meta tag is the primary enforcement mechanism. This is correct behavior.

---

## Phase 9 — site.webmanifest

**Status:** Correct.
- `name`: "OverKill Hill P³™" ✓  
- `short_name`: "OKHP³" ✓  
- `theme_color`: "#2a2320" ✓  
- All favicon paths present ✓  

---

## Phase 10 — Internal Link Integrity

**Result:** Zero broken internal links across all 28 pages. All `href` attributes pointing to internal paths resolve to real files.

---

## Baseline Validator Results

### Before fixes

```
WARN: sitemap.xml not found or empty.
Validating 0 HTML pages…
✓ all clean.
```
(All issues masked by ROOT bug)

### After fixes

```
Validating 28 HTML pages…
✓ all clean.
```

---

## Full Findings Register

| ID | Severity | Status | Description |
|----|----------|--------|-------------|
| 0-A | CRITICAL | ✅ Fixed | `validate_site.py` ROOT resolves to `assets/` — 0 pages found |
| 0-B | HIGH | ✅ Fixed | `validate_site.py` SKIP_DIRS missing `.agents` — false positives |
| 1-A | HIGH | ✅ Fixed | Footer ™ missing on 17 pages |
| 1-B | MEDIUM | ✅ Fixed | `about/index.html` og:title uses comma separator |
| 1-C | LOW | INFO | Em-dash og:title on 4 pages — intentional style |
| 2-A | HIGH | ✅ Fixed | Homepage "Fresh from the Forge" blurb is stale v0.4 copy |
| 3-A | HIGH | ✅ Fixed | 6 noindex pages listed in `sitemap.xml` |
| 3-B | LOW | ✅ Fixed | Sitemap orphaned comment blocks after noindex removal |
| 4-A | LOW | INFO | GA4 in `<body>` (not `<head>`) on all 28 pages |
| 5-A | LOW | DEFERRED | BreadcrumbList JSON-LD absent from ~10 pages |
| 5-B | LOW | INFO | WebSite JSON-LD absent from 3 project pages |
| 6-A | LOW | INFO | `mac-studio` has 2 `aria-current="page"` in same page |
| 7-A | INFO | INFO | CSS cache-bust at `?v=15` — current |

---

*Generated by Sprint 4 audit pass — Task #35 — 2026-05-26*
