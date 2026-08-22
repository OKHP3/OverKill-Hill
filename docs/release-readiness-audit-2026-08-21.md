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
- `responsive-qa.mjs`: Playwright pass for 184 of 192 checks across 24
  sitemap routes and 8 viewports. No overflow, broken local asset, blocked
  embed-frame, or blocked Skillz live-data failures were found. The report is
  retained at
  `assets/docs/responsive-qa/results.json`.
- The remaining 8 browser failures are navigation timeouts on two
  Mermaid-heavy writing routes at selected viewport sizes. Those pages load
  Mermaid from the third-party jsDelivr CDN; the timeout is a nondeterministic
  third-party dependency limit, not a local CSP, layout, asset, or JavaScript
  failure. They remain visible in the report rather than being treated as
  passes.
- Existing structural audit findings were real release blockers; the CI gate
  now reports them instead of masking them.

## Browser QA findings and limitations

- The local development workflow now includes the Playwright Chromium runtime
  dependencies, so the full multi-width browser run is executable locally.
- The six intentional GitHub Pages project previews now pass the local
  enforcing CSP through a host-scoped `frame-src` allowance. Skillz's generated
  `project-summary.json` request now passes through a host-scoped
  `connect-src` allowance.
- The eight navigation timeouts occur on two Mermaid-heavy writing routes that
  depend on jsDelivr. They should be rerun when CDN availability is stable
  before claiming a completely clean browser run.
- External-link availability is not asserted in CI because third-party
  uptime and rate limits make that check nondeterministic. Local link and asset
  resolution remain deterministic.
- CSP remains report-only in `_headers` until deployed violation reports show
  that inline scripts and third-party resources are fully accounted for.

## Priorities

1. Rerun the two Mermaid-heavy writing routes when jsDelivr availability is
   stable, or add a deterministic local Mermaid asset if that dependency
   becomes a release requirement.
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

## Canonical-domain security proof — August 22, 2026

**Evidence:** `assets/audit/live-edge-report-2026-08-22.json`
**Expected deployed commit:** `344e046d7ba1e95be2f8d01907d18129240024e6`
**Result:** **FAILED — live content reachable, edge policy unproven**

The read-only verifier reached `https://overkillhill.com` without transport
blocking and checked 24 sitemap routes plus the noindex boundaries. The three
representative routes required for this proof behaved as follows:

| Route | Content/robots | Live `Cache-Control` | `_headers` security rules |
|---|---|---|---|
| `/` | HTTP 200; indexable | `max-age=600` | **FAIL** — all declared headers absent |
| `/projects/mermaid-theme-builder/` | HTTP 200; indexable | `max-age=600` | **FAIL** — all declared headers absent |
| `/found-ry/` | HTTP 200; `noindex, nofollow` | `max-age=600` | **FAIL** — all declared headers absent |

The absent declarations are `X-Content-Type-Options: nosniff`,
`X-Frame-Options: SAMEORIGIN`, `Referrer-Policy:
strict-origin-when-cross-origin`, the declared `Permissions-Policy`,
`Strict-Transport-Security`, `Cross-Origin-Opener-Policy: same-origin`,
`Cross-Origin-Resource-Policy: same-origin`, `Origin-Agent-Cluster: ?1`, and
`Content-Security-Policy-Report-Only`. The declared directory/HTML cache rule
(`public, max-age=300, must-revalidate`) therefore also **FAILS** on all three
routes. The report contains the full live response-header maps for each
checked route.

The release manifest request returned HTTP 404, so the expected SHA is not
confirmed as the identity of the served bytes. This is an explicit
commit-binding failure, not a pass based on the public `main` ref. No
Cloudflare zone or Transform Rules access was available, so DNS proxy state
and edge rule configuration remain **unverified**. The current evidence shows
GitHub Pages-style origin behavior; it does not establish whether Cloudflare
is configured but bypassed, or not configured for this hostname. Production
security and cache enforcement must remain an open release blocker until the
edge is inspected and the verifier passes.
