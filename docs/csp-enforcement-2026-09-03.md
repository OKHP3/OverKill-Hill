# CSP enforcement decision

**Decision date:** September 3, 2026  
**Canonical site:** OverKill Hill P³ (`overkillhill.com`)

## Decision

The canonical site now treats CSP as enforcing. The generated edge policy and
all generated page policies use `Content-Security-Policy`; no generated output
uses `Content-Security-Policy-Report-Only`.

The generator still owns the policy. `scripts/generate-csp.py` calculates the
inline script/style hashes from the deployed HTML, writes
`config/csp-policies.json`, updates `_headers`, and applies the matching
page-class policy to each production page. Its check mode now rejects a
Report-Only header or a missing/multiple enforcing header, as well as missing
or stale page metadata.

## Coverage review

No committed CSP violation log was available, and the local report sink did
not contain an accumulated report file. A fresh local observation was therefore
run against the sitemap inventory. The existing page classes continue to cover
standard, embedded, utility, and live-Mermaid pages. The only missing legitimate
request found was Skillz's fetch of
`https://okhp3.github.io/skillz/data/project-summary.json`; that origin is now
included in `connect-src`. No other directive or feature scope changed.

Mermaid pages retain the scoped `unsafe-inline` style allowance required for
runtime-generated diagram styles. Script execution remains hash-locked.

## Verification

- `python3 scripts/generate-csp.py --check` — pass; 47 production HTML pages.
- `python3 scripts/check-csp.py` — pass.
- `python3 scripts/validate-site.py` — pass with the repository's reviewed
  baseline warnings and no errors.
- `python3 scripts/check-links.py` — pass; 47 pages, 0 broken links, 0 sitemap
  mismatches.
- `python3 assets/scripts/check-contrast.py` — pass.
- `node scripts/phone-overflow-qa.mjs` — pass; all 30 sitemap routes at 320px.
- `node scripts/responsive-qa.mjs` — pass; 30 sitemap routes × 8 viewports
  (240 browser checks).
- `node scripts/accessibility-qa.mjs` — pass; 4 representative pages and all
  30 sitemap routes.
- A separate Playwright CSP observation loaded all 30 sitemap routes with
  policy messages unsuppressed: 0 CSP violations, 0 page errors, 0 failed
  local resources, and no Mermaid runtime errors. All lazy Mermaid diagrams
  rendered after each diagram was brought into view.

The repository's `_headers` file is now ready for a header-capable edge.
The September 3 live-edge report still shows GitHub Pages serving directly
without applying repository `_headers`; that is a hosting configuration
limitation, not a reason to keep the source policy in Report-Only mode.
Production response-header enforcement remains an edge follow-up.

## Sibling-site parity

OverKill Hill remains the canonical CSP source. The sibling repositories
`glee-fully.tools` and `askjamie.bot` were not modified by this task. When each
site is ready to adopt the policy, it should:

1. use the same enforcing header name and generator check;
2. regenerate its page metadata and edge policy from its own deployed HTML;
3. include the `okhp3.github.io` `connect-src` allowance only if that site's
   runtime makes the same Skillz request; and
4. verify its own hosting edge, because `_headers` is not applied by direct
   GitHub Pages hosting.

The shared runtime files were not changed as part of this CSP decision.