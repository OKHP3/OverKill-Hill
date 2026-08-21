# OverKill Hill release-readiness audit

**Date:** August 21, 2026  
**Scope:** public sitemap routes, static source, local Pages workflow, and
browser checks. Companion sites were used only as mechanical comparisons.

## Fixed in this pass

- Responsive QA now derives its route inventory from `sitemap.xml`, checks
  every listed route, and fails instead of silently skipping missing pages.
- The comprehensive static audit now excludes development preview files,
  understands the committed search-index shape, ignores intentional noindex
  pages in sitemap reconciliation, and exits nonzero when it finds issues.
- CI now gates on the static audit, internal links and sitemap boundaries,
  cache-bust freshness, search-index freshness, phone overflow, and contrast.
- Contrast failures are no longer allowed to pass through the validation job.
- Pages deploy only after the validation job succeeds, from the validated
  commit, with scoped Pages/OIDC permissions and serialized deployment.
- Added a secure Replit publishing runbook. Credentials stay in workspace
  secrets and are never placed in remotes or repository files.

## Evidence

- `validate-site.py`: pass
- `build-search-index.py --check`: pass, 132 entries
- `check-links.py`: pass, 32 pages, 0 broken links, 0 sitemap mismatches
- `check-contrast.py`: pass
- `phone-overflow-qa.mjs`: pass, 24 sitemap routes at 320px
- `responsive-qa.mjs`: Playwright pass for 144 of 192 checks across 24
  sitemap routes and 8 viewports. No overflow or broken local asset failures
  were found. The report is retained at
  `assets/docs/responsive-qa/results.json`.
- The 48 browser failures are actionable external-content findings: 35
  blocked preview frames, 8 blocked Skillz live-data fetches, and 5 navigation
  timeouts on external-content pages. They are not treated as static-lint
  passes.
- Existing structural audit findings were real release blockers; the CI gate
  now reports them instead of masking them.

## Browser QA findings and limitations

- The local development workflow now includes the Playwright Chromium runtime
  dependencies, so the full multi-width browser run is executable locally.
- The embedded project previews and Skillz live-sync request are currently
  rejected by each page's enforcing CSP. The five navigation timeouts occur on
  pages with external embedded content and should be investigated before
  claiming a completely clean browser run.
- External-link availability is not asserted in CI because third-party
  uptime and rate limits make that check nondeterministic. Local link and asset
  resolution remain deterministic.
- CSP remains report-only in `_headers` until deployed violation reports show
  that inline scripts and third-party resources are fully accounted for.

## Priorities

1. Align CSP `frame-src`/`connect-src` with the intentionally embedded project
   previews and Skillz live-sync source, then rerun the full browser matrix.
2. Verify the published Pages headers and key routes after deployment.
3. Continue the existing CSP nonce/hash migration before enforcing CSP.

## Post-deploy verification

**Verified:** August 21, 2026 against the public GitHub Pages edge.

- The published GitHub `main` ref was `344e046d7ba1e95be2f8d01907d18129240024e6`.
- The published root, `sitemap.xml`, `robots.txt`, the First Diagram writing
  route, and the Mermaid Theme Builder project route all returned HTTP 200.
- The deployed bytes for those five routes matched the corresponding files from
  the current GitHub `main` branch. The deployed `theme.css` and `app.js` also
  matched the current branch, including their `?v=66e640fe` and `?v=e29596a8`
  fingerprints.
- The live root, sitemap, robots, writing, project, CSS, and JavaScript
  responses all reported `last-modified` at the current deployment and served
  successfully through the custom domain.
- GitHub Pages did **not** emit the security headers declared in `_headers`
  (`X-Content-Type-Options`, `X-Frame-Options`, HSTS, CSP, COOP, CORP, and
  related policies). It also served `Cache-Control: max-age=600` for HTML,
  CSS, and JavaScript rather than the long-lived immutable asset policy
  declared there.

The content release is confirmed against the published branch. The edge-header
and cache-policy declarations remain unconfirmed for GitHub Pages and require a
separate hosting/configuration decision; `_headers` is not applied by the
current Pages deployment.