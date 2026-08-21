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
- Existing structural audit findings were real release blockers; the CI gate
  now reports them instead of masking them.

## Accepted limitations

- Full multi-width browser QA requires the Chromium binary installed by CI.
  The local environment currently has the Playwright package but not its
  browser binary, so only the 320px browser gate was executable locally.
- External-link availability is not asserted in CI because third-party
  uptime and rate limits make that check nondeterministic. Local link and asset
  resolution remain deterministic.
- CSP remains report-only in `_headers` until deployed violation reports show
  that inline scripts and third-party resources are fully accounted for.

## Priorities

1. Install/run Chromium locally and attach the full responsive report to the
   next release review.
2. Verify the published Pages headers and key routes after deployment.
3. Continue the existing CSP nonce/hash migration before enforcing CSP.