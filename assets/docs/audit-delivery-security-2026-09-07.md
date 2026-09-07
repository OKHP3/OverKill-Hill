# Delivery and security assessment, September 7, 2026

## Assessment boundary

Baseline: `ca38d5b9fc46746ea8b41e2ba32e39685c53f511`, local `main`, initially clean. Observation time: September 7 UTC, September 6 local evening. This is a passive source, GitHub configuration, release, and public-response assessment. No penetration testing, visitor submissions, settings changes, sibling changes, or publication occurred. The assessment used the repository's `okhp3-site-release-validation` skill. A separately authorized local repair is recorded at the end without changing the baseline findings.

Keep the static architecture. Its SHA-bound allowlisted publication boundary, pinned Actions, minimum deployment permissions, source CSP, and substantial browser CI are valuable. The remaining priority is to make verification cover what its name promises and make operator documentation match actual supported paths. Missing response headers are an accepted hosting limitation, not evidence that the site is compromised.

## Current release evidence

Machine evidence: `assets/audit/assessment-2026-09-07/delivery/`.

| Check | Current evidence | Conclusion |
| --- | --- | --- |
| GitHub branch inventory | GitHub connector branch search and REST branch listing; only `main`; local `git branch -avv` agrees | No active remote feature-branch backlog observed. |
| Pull requests and local worktrees | `gh pr list --state open`: empty; `git worktree list`: owner checkout only; `git stash list`: empty | Historical Sep6 detached-worktree and six-stash descriptions are not current inventory on this host. Four archive refs remain; no cleanup performed. |
| Pages settings | `github-state.json`: workflow build, canonical `overkillhill.com`, HTTPS enforced, certificate approved through November 20 | Hosting configuration is healthy at observation time. |
| Current deployment | [Pages run 34084298158](https://github.com/OKHP3/OverKill-Hill/actions/runs/34084298158) succeeds at baseline SHA | Reusable validation and deployment jobs both succeed. |
| Standalone validation | [Run 34084297864](https://github.com/OKHP3/OverKill-Hill/actions/runs/34084297864) canceled at same SHA | Coordination noise remains; not evidence the deployed revision skipped validation. |
| Live manifest | `live-manifest.json`: baseline SHA, 371 inventory files, schema 2, two artifact hashes | Current manifest agrees with successful deployment; does not authenticate every listed byte. |
| Live verifier | `live-edge.json`: PARTIAL, 428 checks, zero failures, 39 blocked, 315 warnings; exit 0 in accepted Pages mode | Current first-party checks pass within declared limits. Header/cache policy is not fully delivered. |
| Bounded publication exclusions | `/AGENTS.md`, `/_headers`, `/server.py`, `/site-src/pages/index.main.html`, `/assets/docs/audit-security-delivery-2026-09-05.md` all return 404 | Sampled canonical-site publication boundary works. |
| Public response sample | Root, shared JS, release manifest return 200; root identifies GitHub/Fastly and `Cache-Control: max-age=600` | Source `_headers` is not the effective edge policy. |

These observations supersede the September 5 report's release SHA and older checkout CSP failure. They do not erase its still-reproducible findings. The September 6 closeout describes many delivered visitor and tooling repairs, but does not establish completion of every proposed September 5 package.

## Reconciled findings and delegated work

Prior IDs below refer to [September 5 security assessment](audit-security-delivery-2026-09-05.md) and [advancement plan](website-advancement-plan-2026-09-05.md). Priority reflects this site's operating risk, not a generic security score.

| ID / priority | Verified current finding | Concrete worker scope and acceptance |
| --- | --- | --- |
| D01, P1; SD-03/W03 | `scripts/build-release.py` schema 2 hashes only sitemap and English search JSON. A freshly built isolated 56-page/371-file package still passed verification after appending a harmless comment to copied `assets/js/app.js`. `digest-probe.json` records this. This is an integrity-check gap, not demonstrated artifact substitution. | Add SHA-256 and byte length for every release file except the manifest itself. Retain exact inventory and expected commit checks. Negative fixtures must reject altered HTML, CSS, JS, locale JSON, vendor JS, image bytes, added/removed/renamed files, missing integrity entries, and wrong commit. Preserve live verifier compatibility. Authorized local repair below. |
| D02, P1 reliability; SD-05/W03 | Pages upload/deploy still use default artifact names. September 5 duplicate-artifact rerun incident remains historical evidence; no rerun failure was induced today. | Use the same attempt-specific artifact name in upload and deployment inputs. Validate a controlled rerun at an authorized release; no artifact deletion required. Keep validated artifact download and serialized deployment. [Official deployment action inputs](https://github.com/actions/deploy-pages) support `artifact_name`. |
| D03, P1 maintenance; SD-06/W10 | Both active `validate.yml` Node setup steps use Node 20, and `.replit` declares `nodejs-20`. Official release table currently lists Node 20 EOL and Node 24 LTS. This affects QA/preview, not a production Node server. | Select supported LTS, preferably Node 24, centralize version contract, and pass clean install and current browser/regression gates. Do not add dependencies merely for this migration. [Node release table](https://nodejs.org/en/about/previous-releases), retrieved September 7. |
| D04, P1 runbook; SD-10/W09 | `docs/publishing.md` still instructs a PAT-based call to nonexistent active `scripts/push-to-github.py`. The historical writer is archived and broad in scope. Its dated “latest” edge result is September 3. | Replace retired helper instructions with current one-repository PR/Pages flow and failure recovery. Verify every active command resolves. Do not revive archived cross-repository writes or solicit credentials. Preserve historical evidence as dated history. |
| D05, conditional P1; SD-04/08/W11 | `.replit` still publishes `publicDir = "."`; no `.replitignore`. `server.py` defaults `HOST` to `0.0.0.0`, serves current directory, and its CSP report receiver has no retention cap and accepts a negative parsed Content-Length before reading. Canonical Pages exclusion checks pass; separate Replit exposure/network reachability is unknown. | Before any external preview/Replit production use, adopt the allowlisted artifact or retire that publication route. Default workstation preview to loopback; explicit Replit bind remains possible. Test negative lengths, request bounds, storage bounds, source/dotfile/symlink exclusions. Python documents that SimpleHTTPRequestHandler follows symlinks. [Python server documentation](https://docs.python.org/3/library/http.server.html). |
| D06, accepted P2 architecture decision; SD-01/02/W12 | Effective responses omit CSP response header, HSTS, nosniff, framing, permissions and isolation headers. Meta CSP remains relevant. `_headers` longest line is 4,304 characters; it is not a ready Cloudflare Pages adapter. | Retain direct Pages acceptance until owner selects an edge strategy. Produce a host-specific adapter and staging evidence before deployment. Cloudflare Pages limits each header line to 2,000 characters and combines overlapping header values; test overlaps and stable-image cache behavior. Framing policy needs response delivery because CSP meta cannot supply `frame-ancestors`. [Cloudflare header rules](https://developers.cloudflare.com/pages/configuration/headers/), [W3C CSP policy delivery](https://www.w3.org/TR/CSP3/#meta-element). |
| D07, P2 coordination; SD-12/W18 | Standalone and reusable validation share `site-validation-${{ github.event_name }}-${{ github.ref }}` with cancellation enabled. The current standalone required-name validation was canceled while reusable release validation passed. Pages `needs: validate` remains intact. | Separate caller/trigger concurrency identities or remove duplicate push validation deliberately while preserving required PR checks and exact-release validation. Acceptance covers PR checks, rapid pushes, manual dispatch and reruns. Do not interpret current cancellation as unsafe deployment or assert its cause solely from status. |
| D08, P2 visibility; SD-12/W18 | Pages succeeds while live policy is PARTIAL with hundreds of expected warnings. Current external-runtime and edge classification primarily print logs and upload JSON. | Emit a compact Actions summary for content delivery, edge policy, external availability and exact release SHA. Retain route evidence; roll up repeated expected limitations. Alert on new first-party failures distinctly from accepted missing headers. |
| D09, P2 owner governance; SD-11/W18 | Current main protection requires strict validation and PR processing, disallows force push/deletion, but requires zero approvals and permits admin bypass. Pages environment has branch policy, no reviewer requirement in fetched rules. | Document actual single-owner review rules for sensitive workflows, release builders and runtime/security policy. If desired and feasible, enforce owner review through CODEOWNERS/rulesets. Avoid requiring a nonexistent independent reviewer. Settings changes require the owner's selected policy. |

D06 is not a blocker for independently useful visitor repairs under the already accepted direct-Pages strategy. D05 is a prerequisite for using its affected exposure paths, not proof the canonical site currently publishes source files. D01 and D02 remain separate acceptance criteria even though the earlier plan grouped them in W03.

## Coverage limits and lower-priority follow-up

The September 5 report's privacy/analytics recommendation is an owner product decision. This pass did not inspect Analytics account settings or overturn the existing accepted policy. Do not create a consent UI by treating an old recommendation as a new authorization.

The current root dependency file contains only Playwright as a dependency; npm-tree status alone cannot clear vendored Mermaid or pinned Python packages. A vendor/advisory inventory remains useful. This pass did not repeat an advisory scan, so the older “zero advisories” result is not a current assurance. The GitHub repository API response omitted `security_and_analysis`; secret scanning and Dependabot security-update status are UNKNOWN in this fresh response, not confirmed disabled or enabled. Avoid repeating September 5 settings as live facts.

No active exploit, report POST, load test, DNS change, Replit publication, GitHub modification, or external account review was performed. Regional CDN differences, registrar controls, Replit live configuration, Analytics retention/advertising settings, and the internals of externally embedded applications remain outside this evidence.

## Verification and dispatch order

1. Release worker: D01 digest repair, then independent D02 artifact retry correction. Existing release and live-edge tests plus new tamper tests are required.
2. Maintenance worker: D03 LTS and D04 runbook correction. Keep active script inventory consistent.
3. Preview worker: D05 before authorizing an externally reachable preview or Replit release.
4. Operations worker: D07 concurrency and D08 status summaries; owner decides D09 policy.
5. Architect: D06 host decision only if full response control warrants additional infrastructure.

The authorizing architect retains integration and publication authority. A worker's local pass is not a deployed repair. Preserve source CSP, release allowlists, current artwork exclusions and localized draft boundaries through every package.

## Local remediation record

D01 repair is authorized as a bounded local change in `scripts/build-release.py` and `tests/test-release-package.py`. Baseline evidence above remains immutable. Implementation and validation results follow below. D02 and all external deployment/settings actions remain outside that repair.


### D01 local correction completed

The local candidate now emits schema 3 with a separate `integrity` map covering SHA-256 and byte length for every packaged file except the manifest. The existing `files` inventory still includes the manifest. The two-entry `artifacts` map is preserved for `verify-live-edge.py`; this repair does not broaden its network requests or claim every deployed file was freshly fetched. Its reader does not reject schema 3.

Verification rejects missing or extra integrity entries, altered file lengths or bytes, inventory changes, and an unexpected commit. It iterates the verified disk inventory instead of opening arbitrary manifest-only paths. Older schema 2 packages fail closed in the updated local verifier; an authorized release rebuilds a schema 3 package before upload. Existing historical releases remain readable by the unchanged live-edge monitor.

Tests were added first and failed against the baseline. After the repair, all nine release-package tests and all nine live-edge/hook regressions pass. New tests include unchanged bytes, same-length replacements and appended bytes in HTML/CSS/JS/locale JSON/vendor modules/images; removed, renamed and extra files; missing/extra integrity entries; wrong lengths/hashes; wrong commit; and old schema rejection. The real source overlay test passes, preserving all 25 accepted still paths and historical artwork exclusions.

A fresh full candidate package contains 371 files, with 370 digest/length entries. Untouched verification passes; appending the same harmless copied-JS comment now fails with a byte-size mismatch. Evidence: `digest-tests-before.log`, `digest-tests-after.log`, `live-edge-tests.log`, and `digest-probe-after.json` in the machine-evidence directory. `git diff --check` passes.

This is a local, uncommitted correction. No new release SHA exists, and production remains the audited schema 2 release. The manifest is an integrity record inside a trusted CI artifact, not a cryptographic signature against simultaneous replacement of payload and manifest. D02 retry naming, D03-D09, and broader live-byte verification remain open.
