---
name: Layout-table CI gate
description: How the accessibility QA gate catches tables Chromium would strip of table semantics.
---

Chromium exposes a bare `<table>` with real `table`/`row`/`cell` accessibility
semantics only when it has at least one `<th>`, a `<caption>`, or an explicit
`role`. Without any of those three, Chromium applies a "layout table"
heuristic and silently drops the semantics, so a screen reader loses
row/column navigation even though the table renders visually fine.

`scripts/accessibility-qa.mjs` (`inspectAriaAndDiagrams`) now does a static
DOM check for this on every public route: it queries `document.querySelectorAll("table")`
and fails if a table has none of `th`, `caption`, or a non-empty `role`
attribute. This runs alongside the existing ARIA/Mermaid checks, not as a
separate script.

**Why:** the original detection only existed in
`scripts/screen-reader-tree-audit.mjs`, which inspects the CDP accessibility
tree on a handful of representative pages — good for spot-checking, but not a
required CI gate across every route. The static DOM check is cheaper and runs
everywhere the ARIA/Mermaid checks already run.

**How to apply:** if you add or edit table-detection logic, verify it against
both a table with no `th`/`caption`/`role` (should fail) and a table with only
`role="table"` (should pass) — a throwaway Playwright `page.setContent()`
script is enough to confirm without touching the real site pages.
