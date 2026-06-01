# Roadmap

This roadmap outlines the near-term public direction for the **OverKill Hill P³™** repository.

## Current
- Quality gates: `scripts/audit-site.py` — run on every meaningful HTML change
- Responsive QA: `node scripts/responsive-qa.mjs --static` — run after major edit rounds
- Sister-site sync: `theme.css` and `app.js` kept in lock-step across all three repos

## Next
- **OG images** — commission 1200×630 landscape social-card images to replace
  current square assets. See `assets/docs/og-image-requirements.md` if present.
- **Submit sitemap** to Google Search Console and Bing Webmaster Tools.
- **CSP hardening** — refactor `onload="this.media='all'"` lazy-CSS inline
  handlers into `assets/js/lazy-css.js` so `script-src 'unsafe-inline'` can
  be dropped from the CSP meta tag.
- **Self-hosted fonts** — move Google Fonts to `assets/fonts/` to eliminate
  the third-party privacy boundary and reduce DNS lookups.
- **Organization JSON-LD `sameAs`** — add social profile URLs (LinkedIn, X, etc.).

## Later
- Expand Writings section with additional long-form technical content
- Add progressive web app install flow (PWA manifest + service worker)
- Evaluate adding a public prompt library or showcase section
- GA disclosure in `legal/index.html` (GDPR/CCPA best practice)
- Cross-link more explicitly between OverKill Hill, AskJamie™, and Glee-fully Tools

## Shipped
- **v1.0 (2026-05-29)** — Scripts superset sync: all general-purpose tooling
  distributed across all three OKHP3 repos. AGENTS.md unified v2.0.
- **v0.9 (2026-05-26)** — `app.js` and `theme.css` consolidated, analytics
  script unified, search index rebuilt, site auditor at 0 issues.
