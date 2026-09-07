# Combined shared foundation, 2026-09-06

This reconciliation combines two independently reviewed releases without
replacing either behavior:

- OverKill Hill `3fad54ac0897684e261c5827d91c1ec03bae6648`: consistent centered
  sidebar follow, including the 14-route browser gate.
- Glee-fully Tools `def34adb3d20a1de19f769c5f1e4d6b194f0f2b9`: keyboard anchor
  focus, reduced-motion scrolling, search recovery/history/accent matching,
  Glee-scoped contrast/layout rules, and its versioned enhancement adapter.

The Glee shared-file delta from its previous main `9b4ade05` applies cleanly
to the OverKill Hill TOC release. The TOC section and CSS remain unchanged.
An explicit AskJamie search-copy branch corrects the previous fallback to
OverKill Hill branding. AskJamie's adapter remains an unversioned import-map
specifier, preserving its existing site-owned fingerprint mechanism.

The final three foundation files are propagated as one compatible superset
under ADR-0001. Each repository regenerates its own consuming HTML, CSP/import
maps, and cache references. No Glee site-specific enhancement implementation,
service-worker data, or generated page content is copied into OverKill Hill.
Locale evidence records cover only proved cache-query changes.

Verification includes the existing search/embed regressions plus a three-brand
search-label regression, all 14 TOC pages, accessibility, responsive layouts,
and each repository's hosted validation. Publication checks must verify each
actual merge commit and the live shared assets; a local copy alone does not
establish cross-site deployment parity.
