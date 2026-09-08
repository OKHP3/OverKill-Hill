# A19 response-header host decision and handoff

September 7, 2026. Status: **proposal prepared; owner choice and provider staging pending**.

## Decision

Should response-level controls justify another hosting surface for this static portfolio?

**Recommendation:** retain accepted direct GitHub Pages for the current visitor-repair release. If the owner wants response framing, MIME, permissions, transport and cache controls, evaluate the compact Cloudflare Pages adapter below on an isolated staging project. A programmable Worker is justified only if a complete response-delivered resource CSP, reporting receiver, or conditional policy becomes a requirement. No hosting, account, DNS, billing, workflow or publication change is part of A19.

This is a narrower alternative to reproducing every directive in the root `_headers`. The owner has not accepted that alternative as production policy. D06 stays open until a host/policy choice and actual provider acceptance are recorded.

## Baseline and reproduction

Worktree: `/Users/okh/.codex/worktrees/a8c6/OverKill-Hill`; initially clean and detached at `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. Local branch: `codex/a19-header-host-strategy`. The package commit is the commit containing this handoff; its full SHA is supplied to A21 separately to avoid a self-referential commit identifier.

Read `AGENTS.md`, `replit.md`, the September 7 advancement plan and delivery/security assessment; reviewed relevant sections of its other linked assessments and of `scripts/csp.py`, `scripts/check-csp.py`, `scripts/build-release.py`, `scripts/verify-live-edge.py`, the Pages workflow and root `_headers`. The current dispatch was read from the owner clone without modifying it.

- Confirmed locally: root `_headers` has a 4,304-character line. Cloudflare accepts at most 2,000 characters per line. Matching header values combine, so `/assets/img/favicons/*` inherits both the year-long immutable image cache value and its week-long favicon value. Later placement does not override the earlier value. [S1]
- Confirmed live: the retained [two-response observation](../audit/a19-host-observation-2026-09-07.json) records the retrieval timestamp, HTTP status, actual headers and manifest body hash. The manifest reports schema 3 and `98922aebf71d90b2b18ecc34c8b00a041fff51c7`; root responds with GitHub identity and `max-age=600`, without the proposed response CSP, HSTS, nosniff, framing, permissions or isolation headers. This supersedes the assessment's older SHA observation only. It is not a full live integrity check.
- Confirmed locally: generated meta CSP verifies on 56 HTML pages. `frame-ancestors` cannot be enforced through CSP meta. Multiple enforcing policies restrict cumulatively. [S2]

## Options and operating cost

| Option | Control and limitation | Cost and operating work | Disposition |
| --- | --- | --- | --- |
| Direct GitHub Pages | Existing trusted artifact and URLs; current response limitations remain accepted. Meta CSP governs resource loading after its delivery point; no response framing control. | No additional host or billing setup. GitHub documents a 1 GB published-site limit and soft 100 GB monthly bandwidth limit. Existing account costs were not inspected. [S3] | Recommended for the current release. Keep content and edge-policy status distinct. |
| Cloudflare Pages, static compact adapter | Adds response-only controls, retaining generated meta CSP. No function, report collector or oversized union policy. Redirect/error/cache behavior needs provider verification. | Free-plan limits include 20,000 files, 25 MiB per file and 500 builds/month. Local release has 371 files, largest 4,659,711 bytes; that fits these size limits. Account eligibility and other account usage are unknown. [S4] Budget one staging session plus a separate cutover/recovery session; this is an effort estimate, not a quote. | Concrete adapter supplied; staging only, pending owner choice. |
| Cloudflare Worker plus Static Assets | `run_worker_first: true` invokes code even for matching assets; a Worker can fetch through the ASSETS binding and set the complete generated CSP response header. [S5] Requires a host wrapper and updated verification contract; not implemented here. | Free Worker limit: 100,000 requests/day, 10 ms CPU/invocation. Paid starts at $5/month, includes 10 million requests and 30 million CPU ms; additional usage is metered. A Worker on every asset request consumes Worker quota. [S6] Adds runtime, deployment credentials, cost monitoring and failure ownership. | Conditional alternative if compact response policy is insufficient. Do not install or purchase it from this memo. |

A reverse proxy in front of GitHub would retain the origin but add two cache layers, origin/Host handling, redirect-loop and DNS recovery concerns. It is not the preferred first staging design. Serving the same verified static artifact directly on the alternate host gives a simpler comparison. There is no proposed framework or content migration.

## Concrete compact adapter

Authoritative proposal: [`config/hosting/cloudflare-staging/_headers`](../../config/hosting/cloudflare-staging/_headers). It is intentionally separate from generated root `_headers` and is excluded from the existing Pages release. It has one universal rule, eight headers, and a maximum line length of 71 characters. It needs no generator, dependency, backend, secret or public endpoint.

| Header choice | Intended behavior and remaining tradeoff |
| --- | --- |
| `Content-Security-Policy: frame-ancestors 'self'` plus `X-Frame-Options: SAMEORIGIN` | Restricts other origins framing this site. It does not restrict this site's outgoing MTB/Skillz iframes; those retain their meta `frame-src` rules. [S2] Third-party framing of OKH itself would become incompatible and needs an owner exception if required. |
| `X-Content-Type-Options: nosniff`; existing referrer policy | Require correct MIME types and retain current referrer intent. Provider MIME and browser behavior must be checked. |
| Camera, microphone and geolocation disabled | Small proposed permissions scope; embedded apps requiring these capabilities would need an explicit reviewed change. Does not claim parity with root's longer permissions list. |
| `Strict-Transport-Security: max-age=300` | Short initial HTTPS commitment. No subdomain or preload opt-in. HTTPS, certificate and browser persistence must be tested; local HTTP cannot prove HSTS. Any longer production duration requires a separate decision. |
| `Cache-Control: public, max-age=0, must-revalidate` | One consistent revalidation policy for HTML, search, manifest, stable images, favicons and query-versioned JS/CSS. Avoids overlapping immutable rules. Additional requests and provider cache behavior must be measured before optimization. |
| `X-Robots-Tag: noindex` | Entire staging deployment stays nonindexable. This is not access control. Never use this unchanged on the canonical production origin. |

No COOP, COEP, CORP or Origin-Agent-Cluster policy is introduced. Cross-origin isolation is not demonstrated as necessary for this portfolio; changing opener/resource behavior could affect embeds or shared images. This is a proposed exclusion, not proof those controls have no value. No CSP report destination is emitted because a static host does not supply the current `/__csp-report` receiver.

The compact response policy deliberately lacks `default-src`, script/style hashes and a full resource envelope. Generated meta CSP remains necessary and must pass its existing gate. If policy must apply before HTML parsing, or to documents without valid meta CSP, select the Worker alternative and implement that full contract. Do not split the root hash list across multiple CSP headers: independently enforced policies intersect rather than combine their hash allowlists. [S2]

## Local checks and reproducible commands

Run from this worktree:

```sh
python3 tests/test-cloudflare-header-proposal.py
python3 scripts/check-csp.py
python3 scripts/build-release.py --output /private/tmp/a19-release --commit 98922aebf71d90b2b18ecc34c8b00a041fff51c7
python3 scripts/build-release.py --verify --output /private/tmp/a19-release --commit 98922aebf71d90b2b18ecc34c8b00a041fff51c7
git diff --check
```

Actual results: five offline proposal contract tests pass, including rejection of long lines, extra rules and repeated headers; CSP verifies all 56 pages; local release build and exact-byte verification pass with 371 files. Neither `config/` nor root `_headers` appears in that release. The commit argument records the unchanged public-content baseline for this local exercise, not a newly validated CI revision. A21 must use the frozen candidate SHA for release validation.

The tests check the intentionally restricted file grammar and policy constraints. They do not run Cloudflare's parser, a local HTTP server, browser cache or frame enforcement. `require.resolve("playwright")` failed with `MODULE_NOT_FOUND` in this worktree (Node v26.0.0); no browser run is claimed and no dependency was installed. Cloudflare staging, TLS/HSTS, real embeds, rollback rehearsal, cold/warm network measurements and CI execution were not performed.

## Provider staging acceptance, not executed

1. After owner selection, use a dedicated Cloudflare Pages Direct Upload project with its own `pages.dev` staging origin. Direct Upload accepts prebuilt artifacts and cannot later switch that same project to Git integration. [S7] Do not point it at the repository root or enable automatic source builds. No production DNS change is needed for this first test.
2. A21 supplies a frozen, verified allowlisted release. Keep its payload and manifest unchanged. Create a separate host envelope containing only that payload plus the reviewed adapter renamed to root `_headers`. Record payload manifest digest, adapter digest, candidate SHA and exact upload inventory in a separate retained envelope record. The existing release verifier will correctly reject the extra `_headers` if pointed at the envelope; do not weaken it or hand-edit its manifest. A dedicated envelope validator is required before an authorized upload. Do not include the raw root `_headers`, source, docs, config directory or functions.
3. Capture actual response headers/statuses for `/`, `/about/`, explicit `index.html` aliases, an unknown route, root 404 document, JS/CSS both with and without `?v=`, search JSON, release manifest, a stable image and a favicon. Confirm one cache value, one supplemental CSP, all eight intended headers, no accidental indexable staging response, correct MIME and no source/dotfile exposure. Cloudflare redirects run before header rules, so redirect responses need separate evidence. [S1]
4. Repeat cold/warm requests and conditional ETag requests. Change a copied stable-name image in a separately recorded second staging candidate and prove a returning browser receives the new bytes; restore the first candidate and prove rollback. Query strings alone are not proof of immutable content identity. Retain bytes, ETags, 200/304 behavior and deployment IDs.
5. Browser checks on staging: English and French navigation/search/theme; live Mermaid; MTB and Skillz iframe startup plus actual editing/export/reload; outgoing tool links; same-origin framing allowed and a separate-origin framing fixture blocked. Check console violations, fonts and images, keyboard use, Downloads and new-window behavior. Distinguish outgoing embeds from external sites framing OKH. Use HTTPS browsers to verify HSTS; test permissions only through intended app tasks, without visitor submissions.
6. Leave canonical URLs, sitemap and locale noindex boundaries intact. A21 must define a host-specific verifier for the approved policy; the current strict live verifier expects longer HSTS, permissions, isolation and cache values and is not an acceptance oracle for this proposal. Do not downgrade the existing Pages checks to make staging green.

## Cutover and rollback, only after separate approval

Keep the current Pages configuration, certificate, known-good artifact and source SHA recoverable. For Cloudflare production, create a reviewed production adapter that removes blanket staging `noindex` while preserving page-specific noindex; select HSTS and framing exceptions explicitly. Record DNS before-state, certificates, custom-domain attachment and who can restore them. An apex Pages domain requires Cloudflare nameserver setup; a subdomain can use CNAME routing, subject to the provider's documented setup. [S8] Account and DNS choices are unknown here.

First rehearse content/header rollback on the alternate host. Cloudflare supports rollback to successful production deployments, not preview deployments; use a dedicated staging project's production deployment history for that rehearsal, without attaching the canonical domain. [S9] Retain both adapter and payload versions. A host rollback is not a DNS rollback.

On new first-party errors, failed embeds, unintended noindex or stale-byte delivery, stop promotion and restore the known-good alternate deployment. After a separately authorized DNS cutover, restore the recorded prior DNS/host configuration if the alternate host remains faulty, and verify canonical TLS, URLs, manifest and representative bytes. DNS caches can delay recovery. HSTS persists in browsers until expiry; removing a file does not clear it, and `max-age=0` requires a successful HTTPS response. [S10] No preload/subdomain expansion is included in the proposal.

## Claim and uncertainty register

| Claim | Tier | Evidence | Consequence if false | Next check |
| --- | --- | --- | --- | --- |
| Direct Pages still omits these response controls | Confirmed for sampled root | Retained response JSON | Wrong host decision | Repeat on frozen candidate and representative routes |
| Compact adapter fits documented parser limits | Confirmed locally and source-backed | Five tests; S1 | Rejected/partial edge policy | Provider response capture |
| Existing resource CSP and outgoing embeds remain compatible | Inferred design; browser result unknown | Exact supplemental directive; current meta gate; S2 | Broken tool tasks | HTTPS staging browser tasks |
| Free static hosting fits current file sizes | Confirmed size comparison; account cost unknown | Local build; S4 | Upload failure or unapproved cost | Confirm selected account plan and upload limits |
| Host switch is worth its operating burden | Proposal, owner choice pending | Options above | Extra maintenance without useful outcome | Owner selects retain Pages, compact staging or full Worker |
| Full response contract and rollback work at Cloudflare | Unknown | No deployment performed | Unsafe promotion | Complete staging evidence and recovery rehearsal |

## Source ledger

All external sources retrieved September 7, 2026. Publishers are the platform operators or standards authors, selected as primary authorities. IDs above map claims to these exact pages.

| ID | Title / publisher / URL | Supported claim |
| --- | --- | --- |
| S1 | [Headers, Cloudflare](https://developers.cloudflare.com/pages/configuration/headers/) | 100 rules, 2,000-character lines, combined overlaps, static-only application, redirects before headers |
| S2 | [Content Security Policy Level 3, W3C](https://www.w3.org/TR/CSP3/) | Meta limitations, ancestor control, cumulative policy enforcement |
| S3 | [GitHub Pages limits, GitHub](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) | Published size and soft bandwidth limits |
| S4 | [Limits, Cloudflare Pages](https://developers.cloudflare.com/pages/platform/limits/) | Free-plan file/build limits and individual file size |
| S5 | [Configuration and Bindings, Cloudflare Workers](https://developers.cloudflare.com/workers/static-assets/binding/) | Static Assets binding and unconditional Worker invocation |
| S6 | [Pricing, Cloudflare Workers](https://developers.cloudflare.com/workers/platform/pricing/) | Free/paid request and CPU allowances and billing |
| S7 | [Direct Upload, Cloudflare Pages](https://developers.cloudflare.com/pages/get-started/direct-upload/) | Prebuilt upload, preview branches and project integration limitation |
| S8 | [Custom domains, Cloudflare Pages](https://developers.cloudflare.com/pages/configuration/custom-domains/) | Apex and subdomain setup distinctions |
| S9 | [Rollbacks, Cloudflare Pages](https://developers.cloudflare.com/pages/configuration/rollbacks/) | Production-only rollback scope |
| S10 | [RFC 6797, IETF](https://www.rfc-editor.org/rfc/rfc6797) | HSTS max-age, expiry and HTTPS policy update behavior |

## A21 handoff

Changed paths: this memo, `config/hosting/cloudflare-staging/_headers`, `tests/test-cloudflare-header-proposal.py`, and the machine-generated `assets/audit/a19-host-observation-2026-09-07.json`. No page/source translation, generated CSP, root header, runtime, workflow or release-builder changes. No regeneration needed for this package; normal integrated generation/freshness gates still belong to A21. New files are outside the publication allowlist.

**Remaining acceptance:** owner policy/host selection; host-envelope validator and approved staging upload; actual response/cache/embed/TLS/rollback evidence; production adapter review if selected. Local proposal completion does not close D06. Next action: A21 presents these concrete options with the current release candidate, recommending continued direct Pages unless the owner selects staging.
