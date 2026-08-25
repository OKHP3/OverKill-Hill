---
name: Screen-reader verification without a real AT
description: How to verify screen-reader announcement in a headless sandbox with no NVDA/JAWS/VoiceOver/Orca installed, and a Chromium AX-tree gotcha to know about.
---

## The constraint

This is a headless Linux sandbox: no audio device, no desktop session, no
installed screen reader. NVDA/JAWS need Windows, VoiceOver needs macOS, and
Orca needs a graphical AT-SPI session — none exist here. A literal "run a
screen reader and listen" session is not possible.

## The substitute

Query Chromium's CDP `Accessibility.getFullAXTree` via Playwright (the
old `page.accessibility.snapshot()` helper is gone in Playwright ^1.62 —
`page.accessibility` is `undefined`; use `context.newCDPSession(page)` +
`Accessibility.enable` + `Accessibility.getFullAXTree` instead). This tree
is what Chromium hands to UIA/AT-SPI/AX platform APIs, so it verifies what
would be announced (roles, accessible names, landmarks, dialog exposure)
even though it can't verify a specific screen reader's phrasing/verbosity.

**Gotchas found doing this:**
- CDP reports the ARIA `img` role as the string `"image"`, not `"img"`.
- Chromium applies a **layout-table heuristic**: a `<table>` with no `<th>`,
  no `<caption>`, and no explicit `role` gets stripped of `table`/`row`/`cell`
  semantics in the AX tree (screen readers get flat text instead of a
  navigable table). Adding an explicit `role="table"` on the `<table>`
  element overrides the heuristic and restores semantics — a real,
  low-cost fix worth applying to any small layout-ish data table.
- Mermaid diagrams that defer rendering via `IntersectionObserver` (used
  when a page has >2 diagrams, see `assets/js/mermaid-init.js`) don't get
  their accessible name until scrolled near the viewport — scroll each
  `.mermaid` element into view before snapshotting the AX tree, mirroring
  how a real user would reach it.

**Where:** `scripts/screen-reader-tree-audit.mjs` (`npm run
test:screen-reader`) implements this pattern; `README.md` "Screen-reader
verification" documents the coverage/limitations record expected for a
manual-QA style task.
