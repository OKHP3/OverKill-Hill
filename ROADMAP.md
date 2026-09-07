# Roadmap

This roadmap separates verified repository capabilities from proposed future
work. Current assessment priorities and worker acceptance criteria are in the
[September 7 website advancement plan](assets/docs/website-advancement-plan-2026-09-07.md).
That plan records recommendations, not new delivery commitments.

## Current capabilities verified September 7, 2026

- Generated HTML, search index, universe navigation, cache fingerprints, locale
  boundaries and structural checks run through `.github/workflows/validate.yml`.
- Browser QA includes Chromium responsive, phone overflow, accessibility,
  sidebar following, search and CSP checks. Explicit `--static` responsive
  mode is structural lint and does not replace browser execution.
- Canonical CSP script policies use approved hashes and `script-src-attr 'none'`;
  the former proposal to remove script `unsafe-inline` is already implemented.
  Style-policy inline allowances remain and must not be conflated with scripts.
- Analytics and cookie disclosures are present in the legal-page source.
  Their existence alone does not establish legal compliance.
- Foundation sync covers `theme.css`, `app.js`, and `mermaid-init.js` through
  an explicit source repository and immutable revision. See [replit.md](replit.md).

## Proposed priorities

Use the linked advancement plan for current evidence, sequencing, dependencies,
and acceptance. Evaluate these remaining possibilities against that evidence:

- Measure social-card coverage and actual page performance before replacing
  images or changing font delivery.
- Confirm search-console submission state through owner-accessible records;
  repository files do not establish whether submission happened.
- Evaluate additional writings, a public prompt showcase, stronger companion-site
  navigation and install/offline behavior only against a defined visitor need.
- Reassess future response-header enforcement separately from the accepted
  direct GitHub Pages hosting limitations.

## Shipped
- **v1.0 (2026-05-29)** — Scripts superset sync: all general-purpose tooling
  distributed across all three OKHP3 repos. AGENTS.md unified v2.0.
- **v0.9 (2026-05-26)** — `app.js` and `theme.css` consolidated, analytics
  script unified, search index rebuilt, site auditor at 0 issues.
