---
name: Site-wide sticky lerp TOC pattern
description: How the sticky lerp-tracking TOC is wired across all content/project pages via app.js sections 4 + 4b.
---

## The rule

Any page with an element `id="toc-widget"` containing `.toc-list a[href^="#"]` links gets:
- **Lerp sticky scroll** — app.js Section 4 (IIFE) animates `transform: translateY()` to track scroll position while staying clear of the nav+banner (NAV_H = 112px).
- **Scrollspy** — app.js Section 4b (IIFE) adds/removes `.toc-active` class on the matching anchor link as sections scroll into the 20% viewport trigger.

No per-page JS needed. The container element needs `id="toc-widget"` and the list needs class `toc-list`.

**Why:** Centralising both behaviours in app.js removes duplicated inline scrollspy scripts from FDIAL and manifesto, and makes it trivially easy to add TOC sidebars to any new page.

**How to apply:**
- **TOC widget must be the LAST element in any sidebar-rail.** The lerp moves it down via `transform: translateY()` — if static widgets follow it in the DOM, the lerp will slide the TOC over them. All static widgets (CTA, PROJECT INFO, RELATED, etc.) must come before `id="toc-widget"` in the sidebar.
- Project pages with existing `sidebar-rail`: add `id="toc-widget"` to a `<div class="sidebar-related">` wrapper containing the `.toc-list`.
- Single-column pages needing a sidebar (Mac Studio, Prompt Forge): add a two-column grid layout wrapping content sections + `<aside id="toc-widget">`. Use the `.two-col` (1fr 340px) or a page-specific grid class. Hide sidebar at <=1023px.
- NAV_H = 112px covers sticky nav (~64px) + HOT OFF THE FORGE banner (~48px).
- CSS `#toc-widget { will-change: transform; }` is already in theme.css at media min-width 1024px.
- `.toc-list a.toc-active` styles already in theme.css.

## Pages with toc-widget (as of 2026-06-10)

| Page | Widget location |
|---|---|
| FDIAL article | `.toc-card` in sidebar-rail |
| MTB project | `.sidebar-related` in sidebar-rail |
| Manifesto | `.sidebar-toc-box` in manifesto-sidebar |
| BPMN project | `.sidebar-related` first in sidebar-rail |
| Mac Studio | `<aside class="mac-toc-sidebar">` in `.mac-body-with-sidebar` two-col grid |
| Prompt Forge | `<aside class="pf-toc-sidebar">` in `.pf-body-with-sidebar` two-col grid |

## Templates updated

- `template--article.html`: `id="toc-widget"` on `.toc-card`.
- `template--project-detail.html`: full two-col `project-layout` with sidebar-rail containing `id="toc-widget"` placeholder.
- `template--interior-single.html`: comment note explaining when/how to add a TOC sidebar.

## Cross-site notes

- Scrollspy added in app.js Section 4b (backward-compatible - activates only when `#toc-widget` exists).
- `app.js` change propagated to `dist/sync/glee/` and `dist/sync/askjamie/` drops (zip: `dist/okh-cross-repo-sync-2026-06-10.zip`).
- All site files use Windows CRLF. Always `data.replace(b'\r\n', b'\n')` before Python edits. app.js was normalised to LF during Section 4b addition.
