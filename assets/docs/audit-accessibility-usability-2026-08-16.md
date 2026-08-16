# Site-Wide Accessibility, Usability & Functional QA Audit — overkillhill.com

## Executive Summary

- **P1 — Contrast failure on `--okh-amber` text (#e6a03c on paper backgrounds, 1.99:1).** Used as the `color` value for article H2/H3 headings, emphasis text, hover states on TOC/breadcrumb/diagram links, and scoring-lane headings across every article/writings page. Fails WCAG 1.4.3 for both normal and large text. Affects low-vision, color-blind, and older-adult personas. Fix once in `theme.css`, fixes every article page.
- **P1 — No visible keyboard focus indicator on both search inputs.** `.okh-search-input` (header overlay) and `#search-page-input` (dedicated `/search/` page) set `outline: none` with no paired `:focus`/`:focus-visible` replacement, unlike `.theme-toggle` and `.okh-search-trigger` which do this correctly. Keyboard-only and low-vision users tabbing into search get no visible indication of focus. WCAG 2.4.7.
- **P2 — 5 live pages missing from `sitemap.xml`.** `/projects/hometools/`, `/projects/pathscrib-r/`, `/projects/un-nocked-truth/`, `/writings/biases-as-constants/`, `/writings/magnus-saga/` are live but undiscoverable via sitemap. (`/found-ry/` is present, correcting an assumption in the source audit brief.) Mechanically detectable — good candidate for `validate-site.py`.
- **P3 — `--okh-gray` (#6b7280) muted text is borderline (4.34:1)**, passing only the large-text AA threshold. Needs a pass to confirm no small-text usage relies on it exclusively.
- **Confirmed passes worth recording** (so no persona is silently skipped): skip-to-main-content link present in 9 of 10 templates; mobile nav toggle uses `aria-expanded`/`aria-controls` correctly; search overlay closes on <kbd>Escape</kbd>; every template has exactly one `<h1>`; `<html lang="en">` set site-wide; primary nav has an `aria-label`.
- **Untested / not currently applicable:** `template--interior-form.html` has zero live page instances right now, so its form-label pattern could not be evaluated against a real page — marked untested, not assumed compliant.
- **Scope note:** this pass is source- and computation-verified (real hex values, real CSS/JS/HTML read from the repo) but does **not** include live screen-reader playback, 400%-zoom reflow measurement, or cross-browser keyboard-trap testing — those require interactive tooling beyond what this pass used. See Methodology and treat unflagged combinations as "not yet verified," not "passed."

## Methodology

- **Contrast**: extracted every color token from `assets/css/theme.css`, computed WCAG relative-luminance contrast ratios programmatically (not estimated) for foreground/background pairs actually used together in the stylesheet, and traced `color:` declarations back to their selectors to confirm real-world usage context (e.g., paper background vs. dark hero background).
- **Structure/ARIA**: grepped all 10 files in `assets/templates/` plus representative live pages for skip links, landmark elements (`header`/`nav`/`main`/`footer`/`aside`), `aria-*` attributes, heading counts, `lang` attribute, and image `alt` presence.
- **Interaction logic**: read `assets/js/app.js` for keyboard event handling (`keydown`, `Escape`) and `aria-expanded` state toggling on the mobile nav and search overlay.
- **Sitemap coverage**: diffed `sitemap.xml` against the actual page inventory on disk.
- **Visual spot check**: one live screenshot of the homepage at desktop width.
- **Not performed this pass** (flagged as follow-up, not assumed to pass): live NVDA/JAWS/VoiceOver playback, 200%/400% zoom reflow measurement, tap-target size measurement on real touch viewports, cross-browser rendering diffs, and interactive keyboard-trap testing via an automated browser driver.

## Findings

| ID | Scope | Issue | WCAG / Heuristic | Severity | Personas affected | Evidence | Recommended fix |
|----|-------|-------|-------------------|----------|--------------------|----------|------------------|
| A1 | Template-wide (article, article-study) | `--okh-amber` (#e6a03c) used as text `color` on paper backgrounds (#f6f2ee/#fffdfa) measures 1.99:1, computed via WCAG relative luminance | 1.4.3 Contrast (Minimum) | P1 | Low-vision, color-blind, older adult | `assets/css/theme.css`: `.article-hero h1 em`, `.article-body h2/h3`, `.article-body em`, `.diagram-links a:hover`, `.sidebar-links a:hover`, `.toc-list a:hover/.toc-active`, `.article-breadcrumb a:hover`, `.scoring-lane h4`, `.diagram-card a`, `.diagram-external-link`, `.council-pill.winner` all set `color: var(--okh-amber)` | Darken the amber token for on-paper text use (target ≥4.5:1, e.g. a value near #9a5f10) or introduce a separate `--okh-amber-on-light` token for these selectors while keeping the current value for dark-background uses |
| A2 | Template-wide (site header overlay + `/search/` page) | `.okh-search-input` and `#search-page-input` set `outline: none` with no `:focus`/`:focus-visible` replacement | 2.4.7 Focus Visible | P1 | Keyboard-only, low-vision, motor-impaired | `assets/css/theme.css` lines ~1696-1703 and ~1875-1881; compare to `.theme-toggle:focus-visible` and `.okh-search-trigger:focus-visible`, which correctly pair `outline: none` with a `border-color` change | Add a `:focus-visible` rule for both input selectors restoring a visible indicator (border-color or box-shadow change), matching the pattern already used elsewhere in the file |
| A3 | Site-wide | `sitemap.xml` is missing 5 live pages | Not a WCAG criterion — discoverability/SEO, but affects the "find a specific project" task for the general-public persona | P2 | Older adult / general public, mobile-on-slow-connection (relies on crawler-fed search) | `sitemap.xml` vs. file inventory: `/projects/hometools/`, `/projects/pathscrib-r/`, `/projects/un-nocked-truth/`, `/writings/biases-as-constants/`, `/writings/magnus-saga/` confirmed live, absent from sitemap | Add the 5 URLs to `sitemap.xml`; audit whatever script generates it so newly published pages are included automatically |
| A4 | Template-wide | `--okh-gray` (#6b7280) on paper background measures 4.34:1 — passes only the large-text AA threshold (3:1), fails the normal-text threshold (4.5:1) | 1.4.3 Contrast (Minimum) | P3 | Low-vision | Computed from theme tokens; usage sites not yet cross-checked against actual rendered font-size | Needs manual verification: confirm every selector using `--okh-gray` for body-size text; darken the token or restrict it to large text if any normal-size usage is found |
| A5 | `template--interior-form.html` | Template defined in the repo but has zero live page instances currently, so its label/form pattern is unverified | N/A — coverage gap, not a defect | Untested | — | `grep -rl "interior-form"` across live pages returns no matches outside the template file itself | No fix needed now; when this template is first used for a real page, run a full accessibility pass on that page before publishing |

## Confirmed Passes (recorded so personas aren't silently omitted)

- Skip-to-main-content link (`.okh-skip-link` → `#main`) present in `template--article`, `-article-study`, `-error`, `-holding`, `-homepage`, `-hub`, `-interior-form`, `-interior-single`, `-project-detail`, `-utility` — 9 of 10 in active use; benefits keyboard-only and screen-reader personas.
- Mobile nav toggle (`.nav-toggle`) correctly pairs `aria-controls="navigation"` with `aria-expanded` state toggling in `app.js` — benefits screen-reader and keyboard-only personas.
- Search overlay closes on <kbd>Escape</kbd> (`app.js` line ~587) — benefits keyboard-only and cognitive-load personas (predictable escape hatch).
- Every template in `assets/templates/` has exactly one `<h1>` — benefits screen-reader persona (heading-based navigation).
- `<html lang="en">` set — benefits screen-reader persona (correct pronunciation/voice selection).
- Primary nav landmark carries `aria-label="Primary"` — benefits screen-reader persona (landmark disambiguation).
- Dark "forge" hero and dark article-body color pairs (body text on `--color-surface`/`--color-surface-soft`) all measure above 13:1 — well clear of AA.

## Automatable

- A3 (sitemap completeness) is a good candidate to add to `scripts/validate-site.py` as a standing check: diff every `index.html` under a published route against `sitemap.xml` and fail if a live page is absent.
- A1 and A2 could seed a lightweight contrast-ratio and `outline: none`-without-`:focus-visible` linter, since both were caught by mechanical inspection of `theme.css`, not manual judgment.

## Appendix

- **Date:** 2026-08-16.
- **Method:** static source analysis (`assets/css/theme.css`, `assets/js/app.js`, `assets/templates/*.html`, live page HTML) plus one live homepage screenshot at 1280×720 via the dev server. Contrast ratios computed programmatically from actual hex values (WCAG relative-luminance formula), not estimated.
- **Not covered in this pass:** live screen-reader (NVDA/JAWS/VoiceOver) playback, 200%/400% zoom reflow, cross-browser rendering, real touch-viewport tap-target measurement, and full interactive keyboard-trap testing. Recommended as a distinct follow-up pass using a browser-automation tool before this audit is treated as WCAG-conformance-complete.
