# Content wave release closeout

Status: DEPLOYED on September 8, 2026. Live-edge result is PARTIAL with zero failures. This closes the selected content release, not the full advancement program or human/device acceptance.

## Release identity and independent acceptance

- [PR65](https://github.com/OKHP3/OverKill-Hill/pull/65) merged normally at 12:10:12 UTC.
- Reviewed candidate: `f0b2eb5bb0e99ec5ea6bb4cdf8f97dc115ca24f7`.
- Merged and live revision: `f4a353c323fc1caa848e03f6f0aa1ea1e520210c`.
- Both Git trees equal `2194c089d1e4c1ac44bb9a288a7fb6d91a3c497e`.
- Independently observed previous live rollback baseline: `6f6079d9a5ac771412f3e153be80e5abb6f4f5a9`.

Exact-candidate Site Validation `34223924264` and locale `34223924267` passed before merge. A20 independently accepted with limits in evidence commits `99d897864d1de17672b1a1bf44c17faff4071328` and `2471c014212f97ed946fe9bcff69d739d11879d8`. The latter verified all 371 payloads were unchanged after reconciling PR64's 12 nonserved documentation/test files. See [full acceptance](a20-content-acceptance-2026-09-08.md) and [exact-candidate rebind](a20-content-rebound-acceptance-2026-09-08.md). These evidence commits were preserved separately from the frozen release candidate.

## Actual hosted artifact and live checks

[Pages run 34224582972](https://github.com/OKHP3/OverKill-Hill/actions/runs/34224582972) passed merged-revision validation, artifact handoff, deployment and live verification. Main validation `34224582624` and locale `34224582566` also passed.

A21 downloaded the actual producer artifact `validated-site-f4a353c323fc1caa848e03f6f0aa1ea1e520210c-34224582972-1`. Release verification passes: 56 HTML pages and 372 files. An independent binary comparison confirms all 371 served payload files exactly equal the merged Git blobs. [Integrity evidence](../audit/a21-content-hosted-integrity-2026-09-08.json) records hosted manifest SHA-256 `9eb086a79bfe637927d82b89d7fc48746eeb7e3044bedcc2e6753c8eba302210`. It is an integrity record, not a signature. The local Windows candidate manifest is distinct and is not represented as the hosted artifact.

The public manifest reports the merged revision. The downloaded [live-edge report](../audit/a21-content-live-edge-2026-09-08.json) records 428 checks, zero failures, 39 blocked checks and 315 warnings: PARTIAL, not security PASS. Existing GitHub Pages header/policy and external-service limits remain unresolved.

Independent live accessibility QA passed four representative interaction samples and all 56 public routes. [Live Chromium checks](../audit/a21-content-live-browser-2026-09-08.json) passed search result focus, clean snippets, Escape, five private-path 404 checks, and painted homepage headings with JavaScript disabled or the shared script blocked. [Ten live content/locale pages](../audit/a21-content-live-parity-2026-09-08.json) exactly match the verified hosted bytes, covering English homepage/projects/writings/vault and French/en-GB/es-MX home/projects pages. These are automated checks, not spoken assistive-technology or native-language approval.

## Scope and preserved limits

A06/A11/A12/A13/A16 content packages qualify unsupported claims, align registry/page/search status, label selected writing Featured, update reviewed French interaction/status copy, and add a lossless smaller WebP of the existing homepage illustration. Existing production presentation stays in use. Neither A14 layout choice nor optional status disclosures are activated.

English source freeze and exact-pair French review provenance are recorded in the integration checkpoint. French remains AI-reviewed with human/native approval false and condensed-page omissions retained. Regional en-GB/es-MX pages remain drafts, noindex, human/native false and release-acceptance false. Eight existing de/es stale records remain advisory. Source-described status is not evidence of operational delivery.

Historical fallback-only English/French whole-page text equality remains FAIL because authorized content edits supersede its no-text-change premise. The test was preserved unchanged. A20 independently adjudicated this scope; continuing image alt/title, original PNG, decoded RGBA and 11 protected narrative/unrelated main-text comparisons passed. Original narratives and manifesto remain protected.

Actual Safari/VoiceOver/NVDA, physical-phone/touch, native macOS, human/native translation, Replit runtime/public-directory behavior, fresh field performance, and actual full-workflow/deploy-only retries remain unperformed or unresolved. WebKit ordinary-link Tab traversal retains the independently isolated environment limitation. Successful attempt one does not certify retry behavior. A14 owner choice and A15 proposals remain outside this release. No full-program completion is claimed.

No force push, branch deletion, primary/sibling checkout mutation or cleanup occurred in this release closeout. Prior parent cleanup lost ignored A05/A10 raw outputs; this record does not imply those outputs were recovered. Retained source branches, committed evidence and this separate release-evidence branch remain available.
