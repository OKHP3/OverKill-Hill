# A19: Response-header hosting decision

Date: September 7, 2026. Status: decision brief complete; owner decision and provider staging pending. Source baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`, including A01/A02. No hosting, DNS, account, runtime, or deployment changes are part of this package.

## Decision and recommendation

Should OverKill Hill retain accepted GitHub Pages response-policy limitations, add a small edge policy, or move the validated static artifact to a host with full response control?

**PROPOSAL:** Retain direct GitHub Pages for the current visitor-improvement release. If the owner requires framing protection and basic response headers, evaluate option B first. If the requirement is full release-bound CSP, select option D for a separately authorized staging implementation. This is not an infrastructure acceptance or a security clearance. A19 supplies a concrete design and acceptance plan; it does not claim staging behavior that has not been exercised.

## Current evidence

Read `AGENTS.md`, `replit.md`, the advancement plan, delivery/security audit, `_headers`, `scripts/generate-csp.py`, `scripts/build-release.py`, `scripts/verify-live-edge.py`, and `.github/workflows/pages.yml` at the baseline. Prior audit references to uncommitted A01/A02 are historical.

The companion [machine observations](../audit/a19-header-observations-2026-09-07.json) retain UTC time, statuses, selected delivered headers, and body digests from six read-only HTTPS GETs at one network vantage. No report POST was sent.

| Claim | Tier | Evidence | Consequence if false | Next check |
| --- | --- | --- | --- | --- |
| Home, shared JS, French home, Found-Ry and the actual release manifest return 200 with `Server: GitHub.com` and `Cache-Control: max-age=600` | CONFIRMED | Observations, September 7, 07:09 UTC | Wrong host strategy baseline | Repeat from another network before selection |
| Those five responses omit CSP, HSTS, nosniff, X-Frame-Options, Permissions-Policy, COOP, CORP and Referrer-Policy headers | CONFIRMED | Same observations | Protection overstated | Repeat GETs after any host change |
| Live manifest identifies the source baseline | CONFIRMED | `/assets/audit/release-manifest.json` | Evidence could describe a different release | Full manifest/digest verification by A21; this sample is not all-file verification |
| The longest `_headers` line is 4,304 characters | CONFIRMED | UTF-8 source measurement | Raw adapter might be deployable | Recalculate on the frozen candidate |
| Cloudflare Pages cannot accept that line unchanged | INFERRED | Measurement plus S2 limit | Staging design unnecessarily complex | Provider parser test |
| GET `/__csp-report` returns 404 | CONFIRMED | Observations | Reporting assumptions wrong | No functioning POST collector is established; separately review before using reporting |
| New edge behavior and account prerequisites work | UNKNOWN | No provider staging or account inspection | Cutover could break navigation or TLS | Authorized staging and account inventory |

The response headers reproduce D06 against current source and live release. Meta CSP remains useful, but cannot deliver `frame-ancestors` or report-only policy (S3). Missing headers do not establish compromise.

## Options and operating costs

USD figures are published service terms retrieved September 7, 2026, not an account quote. Existing domain registration, GitHub plan/Actions charges, taxes, paid support, and staff time remain additional. Traffic, existing Cloudflare zone ownership, and shared account consumption are unknown.

| Option | Concrete implementation and protection | Incremental service cost | Operations and tradeoff |
| --- | --- | --- | --- |
| A. Direct GitHub Pages | Keep exact validated artifact deployment and meta CSP. Continue explicit missing-header classification. | No new service; existing account costs unchanged | Lowest added maintenance. No owner-controlled response framing/CSP/cache policy. GitHub documents 1 GB published-site and soft 100 GB/month bandwidth limits (S1). |
| B. Pages origin plus Cloudflare response transforms | Proxy only the approved site hostname; exact-host rules set a compact framing-only CSP, nosniff and referrer policy. Preserve generated meta CSP. Do not copy the hash union into dashboard rules. | Free plan includes 10 active Transform Rules, without regex (S4); account capacity must be checked | Keeps Pages publishing. Adds DNS/proxy/TLS ownership and two-provider incident diagnosis. This deliberately supplies partial header control, not full generated CSP. Cache policy needs separate cache configuration; response transforms alone do not prove edge storage behavior. |
| C. Cloudflare Pages static hosting | Upload the verified allowlisted artifact with a newly generated host-specific `_headers`; use compact framing-only response CSP plus existing meta CSP initially. Full per-route policies require length/rule validation. | Static requests free and unlimited; Functions billed as Workers if introduced (S5) | Replaces hosting/deploy integration. S2 permits 100 rules and 2,000 characters per line; overlapping values combine. Redirects and function responses need separate handling. Raw current file is unsuitable. |
| D. Cloudflare Worker with static assets | Publish verified assets and a generated route-to-policy map together; run Worker first for HTML, set one CSP response value, serve through the assets binding. No live Pages fetch dependency. | Free Worker: 100,000 requests/day and 10 ms CPU/invocation. Paid: $5/month minimum, 10M requests and 30M CPU-ms included; overages $0.30/M requests and $0.02/M CPU-ms. Direct static requests are free (S6). | Strongest release/policy coupling. Adds adapter code, platform version/testing and billing ownership. Worker-first requests count as Worker usage, including asset fetches through it (S7). More work than a response rule, but avoids origin/policy race. |

**PROPOSAL planning allowances, not measured estimates:** A adds about 15 minutes/month of policy review; B 1-2 engineering days for staging and 1-2 hours/month; C 2-4 days and 1-2 hours/month; D 3-5 days and 2-4 hours/month. DNS recovery or embed failures can extend these ranges. At internal rate R/hour, recurring labor is those hours multiplied by R; the owner has not supplied R.

For D, an illustrative 1M Worker requests/month at 5 ms CPU each fits the $5 paid inclusion. At 20M and 5 ms, estimated compute is $5 + $3 requests + $1.40 CPU = $9.40/month, excluding other account usage. These are scenarios, not measured site traffic. Budget alerts and CPU limits would be part of an approved implementation, not a guaranteed spending cap.

## Proposed adapter contract

For B, a hostname-scoped response rule would set `Content-Security-Policy: frame-ancestors 'self'`, `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`, and `Referrer-Policy: strict-origin-when-cross-origin`. This short CSP complements meta policies without adding a competing script allowlist. Confirm the owner does not need other sites to frame this site. Outbound embeds use `frame-src`, a distinct control.

For D, the build input is A21's verified allowlisted artifact, never repository root. Derive each HTML route's response policy from the same generated policy used in that exact HTML, add the approved response-only framing directive, and bind the map to artifact SHA/digests. Resolve directory indexes, explicit `.html` aliases and custom 404s to the correct policy. Unknown paths retain 404 status. Reject missing map entries, ambiguous routing, digest mismatch and policy overflow before upload. Assets and adapter must roll back as one version. A07's final artifact-name/attempt contract and A08's runtime contract must be verified before implementation.

Use `Headers.set`, not append, for a single final value per policy. Never split a hash union into multiple CSP headers to evade size limits: simultaneous CSP policies all apply and can block scripts allowed by only one (S3). Retain meta CSP through staging; do not add `unsafe-inline` for scripts to shrink headers. Measure final total response size against provider limits and test actual browser delivery.

Do not transport the existing `_headers` settings blindly:

- Start HTML, search, sitemap, manifest and stable-name images with short revalidating caches. Defer immutable caching until versioned URLs are proven to preserve old bytes; a changed query on a mutable file alone does not guarantee old-version content remains available. Test bare CSS/JS URLs too.
- Avoid overlapping CORP and cache rules that create comma-joined conflicting values on C (S2). Keep share images embeddable; scope resource restrictions intentionally.
- Stage Permissions-Policy against actual embedded tools and fullscreen behavior. Do not assume every currently listed directive is supported.
- Defer COOP/CORP changes until popup, opener and embedding tests pass. Do not claim cross-origin isolation from COOP/CORP alone.
- Introduce HSTS only after TLS and rollback endpoints work, initially `max-age=300` without `includeSubDomains` or `preload`. Longer duration and broader scope require explicit owner policy. Existing long-lived browser HSTS cannot be instantly reversed by DNS rollback.
- Omit the source `report-uri /__csp-report` from a new response adapter until a bounded collector is approved. Use browser violation/console capture during staging; do not claim server-side report collection.

## Staging, acceptance and rollback plan

All steps below are **PROPOSAL / NOT RUN**. No account, hostname or staging environment has been created by A19.

1. Owner selects A, B, C or D and names the operations owner. For an edge option, inventory DNS, TLS, account permissions, traffic and cost budget read-only. Record current DNS values/TTL, Pages custom domain and HTTPS settings without changing them. Preserve existing MX/TXT and unrelated hostnames.
2. Freeze the integrated candidate and preserve its verified artifact, complete manifest and last working production SHA. For D/C, add a separate reviewed adapter packaging stage; do not rebuild source at the host. For B, stage on an approved disposable hostname/origin pair with the same Pages behavior. Its origin and certificate must be explicitly proven; do not assume the production custom domain accepts another Host header.
3. Stage under a provider preview or approved test hostname, with `X-Robots-Tag: noindex` and unchanged canonical URLs. This header discourages indexing; it is not access control. Preserve existing draft/noindex locale boundaries. Add report-only CSP for the proposed full policy first, retain existing meta enforcement, then enforce on staging after review. Framing controls also need an enforced test because report-only does not block framing.
4. Test home, search, universe/Mermaid, one writing, one project with `okhp3.github.io` iframe, French, a regional draft, Found-Ry, 404, redirects, images/favicon, CSS/JS, search JSON and manifest. Cover GET/HEAD, cold/warm/conditional responses, slash aliases and query strings. Require one intended value per header, correct MIME/status, no source-file exposure, and byte hashes matching the approved artifact.
5. Browser acceptance: keyboard search/theme/navigation; fonts and analytics requests under the existing policy; allowed child iframe loads; same-origin parent framing works and an unrelated parent is blocked; popup/new-tab behavior; external image embedding; no new CSP violations. Include real Safari and available assistive technology through A20. The current live verifier's strict profile may demand policies deliberately deferred here; A21 must review that profile against the selected policy, retain all exceptions and report content, edge and external health separately. Do not use the direct-Pages exception for an edge-backed release.
6. Exercise rollback in staging before requesting cutover approval. For D/C restore the previous asset-and-policy deployment together; Workers rollback requires compatible bindings and does not automatically undo external resource changes (S8). For B disable only the test response rules and confirm origin delivery. Verify manifest, headers and key tasks again. Record observed recovery duration.
7. A21 presents the staging evidence, exact candidate, DNS/TLS delta, operator and rollback reference for owner cutover approval. Production deployment remains A21-only. After an authorized cutover, verify responses from more than one network and watch content, TLS, CSP, embeds and costs separately.

Rollback triggers: first-party content/digest mismatch, sustained TLS/5xx failure, blocked key tasks/embeds, or materially broken caching. First revert the edge policy or paired deployment while keeping hostname/TLS stable. If the provider path fails, restore the recorded direct-Pages DNS/proxy configuration only after confirming Pages still serves the intended custom domain with valid HTTPS. DNS propagation and browser caches delay recovery; no instant rollback promise. Retain Pages capability until that fallback is proven. Restore normal TTL only after stability. Long-lived HSTS/preload and immutable cached bytes are reasons to defer those policies during initial cutover.

## Source ledger

All external sources retrieved September 7, 2026. Authority rationale: official provider documentation for service behavior/prices, W3C specification for CSP semantics. The claim mapping appears beside each option and adapter requirement above.

| ID | Publisher and title | Supported claim |
| --- | --- | --- |
| S1 | GitHub, [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) | Published size and soft bandwidth limits |
| S2 | Cloudflare, [Pages headers](https://developers.cloudflare.com/pages/configuration/headers/) | Static response rules, line/rule limits, overlap and function/redirect exceptions |
| S3 | W3C, [CSP Level 3](https://www.w3.org/TR/CSP3/#meta-element) | Meta exclusions, report-only, simultaneous enforcement |
| S4 | Cloudflare, [Transform Rules](https://developers.cloudflare.com/rules/transform/) | Proxied DNS prerequisite and Free rule availability |
| S5 | Cloudflare, [Pages Functions pricing](https://developers.cloudflare.com/pages/functions/pricing/) | Static requests and Functions billing |
| S6 | Cloudflare, [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/) | Request/CPU prices and inclusions |
| S7 | Cloudflare, [Worker script routing](https://developers.cloudflare.com/workers/static-assets/routing/worker-script/) | Worker-first routing and billing implications |
| S8 | Cloudflare, [Workers rollbacks](https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/) | Version rollback and binding limitations |

## Handoff and unresolved evidence

This documentation-only package changes this brief and its machine observation file. Checks: six public GET observations, source line measurement, JSON parsing and scoped diff/whitespace review. No site regeneration or browser suite is needed for these non-published documentation records; no staging or live security acceptance is claimed.

Unresolved: owner choice; actual DNS/account authority and plan; traffic/billing baseline; provider parser/runtime acceptance; final A07/A08/A21 contracts; browser/iframe/cache/TLS behavior on staging; collector ownership; subdomain HSTS suitability; multi-network production verification. None blocks the independently useful visitor changes under accepted direct Pages limits.

**Next action:** owner selects whether to retain A or authorize the bounded staging scope for B or D. C remains a viable static-host alternative if its policy limits are acceptable. Do not promote this brief into permission to modify DNS, account policy, hosting, or deploy a proxy.
