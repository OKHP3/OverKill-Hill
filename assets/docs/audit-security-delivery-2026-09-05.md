# Infrastructure, security, and delivery assessment

Assessment date: September 5, 2026, America/Chicago. Live captures occurred September 6 UTC. This is a bounded source, release-pipeline, and public-response review, not a penetration test or a security certification.

## Judgment

Keep the static architecture. It is appropriate for this portfolio and writing archive, and its lack of a first-party application server, authentication system, and visitor database removes substantial operational complexity. The strongest existing controls are the explicit Pages package, validation before deployment, pinned Actions, restrictive page CSP, production manifest, and recorded hosting limitations.

The next investment should make delivery claims match actual guarantees. Production still does not deliver the desired response headers. A successful deployment can legitimately carry hundreds of warnings under the accepted direct-Pages strategy. Package verification does not authenticate all packaged bytes. Replit's root-directory publishing configuration does not share the Pages publication boundary. The security and operations documentation also contains an obsolete credential-based publishing path. These deserve attention before adding infrastructure or broadening the application surface.

No critical remotely exploitable vulnerability was demonstrated. Priorities below express remediation urgency for this site's exposure and maintenance model; missing hardening headers are not evidence of compromise.

## Evidence boundaries and current state

| Surface | Observed state | Meaning |
| --- | --- | --- |
| Owner checkout | `897df5d33202bd65924f9f3a35c84e0068cbee02`, initially clean | Local findings are tied to this revision; no source edits were made. |
| Current remote audit snapshot | `40e18ee7916f4a54196cc407d60999ba1d786d11` | Parent audit created an isolated snapshot. Release builder, workflows, server, Replit configuration, and publishing guide were compared and are identical across these revisions. CSP artifacts differ. |
| Latest successful Pages execution | [Run 34007868479](https://github.com/OKHP3/OverKill-Hill/actions/runs/34007868479), manual dispatch | Validation, deployment, and live checks succeeded as jobs for remote revision `40e18ee7`. |
| Live release manifest | `/assets/audit/release-manifest.json` identifies `40e18ee7`; 343 inventory entries | Direct GET agrees with the successful deployment's revision. This is not proof that every listed file's bytes were checked. |
| CI post-deploy edge report | `PARTIAL`: 427 checks, 0 failures, 38 blocked, 315 warnings | Successful workflow means its accepted direct-Pages criteria passed, not that full desired security/cache policy was delivered. |
| Production hosting | API says workflow-built GitHub Pages, canonical `overkillhill.com`, HTTPS enforced, approved certificate | Certificate state and hosting settings were read without changing them. |
| Public response sample | Homepage, Mermaid Theme Builder, shared JS and release manifest return 200; `Cache-Control: max-age=600` | Responses identify GitHub/Fastly; sampled responses omit desired CSP response header, HSTS, nosniff, framing, permissions, and isolation headers. |
| Publication exclusion sample | `/AGENTS.md` and `/_headers` return 404 | Confirms these sampled repository files are not being exposed through the canonical Pages site. |

Machine evidence is under `assets/audit/comprehensive-2026-09-05/`: `live-security-headers.json`, `ci-live-edge/live-edge-report.json`, `pages-success-run.json`, `pages-settings.json`, `main-protection.json`, `github-security-settings.json`, `failed-run-artifacts.json`, `pages-retry-failure.log`, `release-route-inventory.json`, `security-checks.json`, `npm-audit.json`, `release-integrity-probe.json`, and `security-source-comparison.json`. The live report preserves all 427 check results, rather than only the summary.

## Findings and recommendations

### SD-01 - Full edge policy remains undelivered

**P1; medium security hardening gap; CONFIRMED.** `_headers:5-23` declares controls that sampled canonical responses do not contain. `docs/publishing.md` explicitly accepts direct GitHub Pages with these limitations. This is an outstanding architecture decision, not a new unexplained outage. Page CSP and the meta referrer policy still provide meaningful protection; the site is not without CSP. However, `frame-ancestors` is unavailable in a CSP meta element, so the desired framing restriction is not supplied by that fallback. [MDN frame-ancestors reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors).

**Proposal:** Retain direct Pages while preparing a reviewed edge adapter. Choose whether the value of response-header control justifies an edge proxy or a static host that supports it. If the owner retains direct Pages, keep a dated risk acceptance and a prominent operational summary of remaining controls. Do not claim full enforcement because Actions is green.

**Acceptance:** After an authorized edge change, run the canonical verifier in strict mode at the intended SHA, inspect actual CSP directives rather than header presence alone, and test first-party pages, external app embeds, social images, redirects and errors. Keep valid restrictive page policies; do not remove them merely to obtain a passing browser report. HSTS `includeSubDomains` and preload require an inventory of affected hostnames before adoption.

### SD-02 - The proposed `_headers` file needs a host-specific correction before deployment

**P1 before edge adoption; medium deployment risk; CONFIRMED source facts, INFERRED host impact.** The current remote CSP line at `_headers:23` is 4,358 characters; the older local version is 4,250. Cloudflare Pages limits each `_headers` line to 2,000 characters. Its matching rules also combine repeated header values with commas, whereas this file's comments assume later CORP and cache rules override broad earlier rules. `/assets/img/favicons/*` overlaps `/assets/img/*`, and the image CORP rule overlaps the global CORP rule. The file also assigns immutable year-long caching to image paths that are not uniformly content-addressed. [Cloudflare Pages header semantics and limits](https://developers.cloudflare.com/pages/configuration/headers/).

**Proposal:** Generate adapters for the selected host, with explicit header replacement behavior. Externalize repeated inline scripts to reduce hash inventories, or use the chosen edge mechanism's supported policy delivery. Avoid declaring the whole current file portable across hosts. Preserve short caching for assets whose bytes can change at stable URLs. Record a separate reason for COOP/CORP; do not describe them alone as full cross-origin isolation.

**Acceptance:** Automated adapter validation checks line limits and overlapping rules. Staging GETs show one intended effective CORP/cache value per resource class. Updating a stable image URL does not leave clients with a year of stale art. Root, directory index, explicit HTML, images, favicons, CSS, JS, search JSON, sitemap and 404 all have deliberate verified policy.

### SD-03 - Release verification does not check all release bytes

**P1; medium integrity gap; CONFIRMED by isolated fixture.** `scripts/build-release.py:167-179` hashes only the sitemap and English search index. Lines 222-230 verify those hashes and a filename inventory. HTML, CSS, JS, translated indexes, images, and vendored modules are not hashed by this verifier. A harmless comment appended to a copied `assets/js/app.js` after building a temporary package was accepted by `--verify` with the original manifest. No deployed or repository JS was changed. See `release-integrity-probe.json`.

GitHub's artifact transport and job isolation are useful controls. This finding does not establish an artifact substitution attack. It establishes that the step named “Verify downloaded release provenance and bytes” promises more than its custom verifier checks.

**Proposal:** Record SHA-256 and size for every released file, excluding the manifest's self-reference; verify those values and the exact inventory before upload. Keep the manifest bound to the validated source SHA. Add artifact attestation only if stronger externally verifiable provenance is needed; a complete digest manifest is the first useful increment.

**Acceptance:** A changed HTML, CSS, JS, locale JSON or vendor module fails verification; an added, removed or renamed file fails; untouched artifacts pass. A manifest with an unexpected SHA fails. Verify the deployed manifest and representative live bytes as a separate post-deploy check.

### SD-04 - Replit can publish a broader boundary than GitHub Pages

**P1 before Replit publication; medium operational exposure risk; CONFIRMED configuration, UNKNOWN live Replit exposure.** `.replit:67-69` uses `deploymentTarget = "static"` and `publicDir = "."`. No `.replitignore` exists. This differs from `scripts/build-release.py`, which deliberately excludes governance, tooling, templates, tests and authoring sources. The canonical site currently serves GitHub Pages, and this assessment did not verify any separate Replit deployment.

**Proposal:** Make every publication route consume the same generated allowlisted artifact, or explicitly retire the Replit production publishing route while retaining it for preview. Keep prototype work out of the published artifact based on route metadata, not assumptions about `noindex`; `noindex` controls indexing, not access.

**Acceptance:** A dry release inventory from each supported host is identical for the same commit. Negative checks cover governance, source templates, tests, reports, config and workspace files. Public noindex routes are explicitly approved for public access. Replit production configuration cannot silently revert to publishing the repository root.

### SD-05 - Pages reruns can fail on duplicate default artifact names

**P1; medium delivery reliability issue; CONFIRMED.** [Run 34007584411](https://github.com/OKHP3/OverKill-Hill/actions/runs/34007584411) is at attempt 2. Its failed deployment log reports two artifacts named `github-pages`. The API inventory confirms two IDs created at 02:56:14Z and 02:58:28Z. `.github/workflows/pages.yml:55-62` uses the default upload and deployment names. A new manual workflow run at the same SHA subsequently succeeded, so this is a retry defect rather than a current outage.

**Proposal:** Use an attempt-specific Pages artifact name for both uploader and deployer, and document retry versus new-run recovery. The official actions expose `name` and `artifact_name` inputs. Keep the validated source artifact dependency and the deployment queue. [Upload Pages artifact inputs](https://github.com/actions/upload-pages-artifact), [Deploy Pages inputs](https://github.com/actions/deploy-pages).

**Acceptance:** A controlled failed deployment can be rerun without manual artifact deletion or ambiguous artifact selection. The successful rerun deploys the intended validated SHA. Missing live-edge reports after a pre-deploy failure remain a secondary diagnostic, not the apparent root cause.

### SD-06 - Node 20 remains in the QA and Replit environment

**P1; medium maintenance risk; CONFIRMED.** `.github/workflows/validate.yml:49` and its external-runtime monitor use Node 20; `.replit:1` declares `nodejs-20`. Node's official release table now lists v20 as EOL and v24 as LTS. This is a CI/preview runtime exposure, not a Node production web server. [Node.js release status](https://nodejs.org/en/about/previous-releases).

**Proposal:** Move tooling to a supported LTS, preferably Node 24 after compatibility testing. Declare the supported version once in a version file or an equally clear contract, and make CI/local preview consume it. Move Playwright to `devDependencies` to express its QA role; that classification change itself adds little security.

**Acceptance:** Clean `npm ci` and the existing browser/regression gates run under the selected LTS. No active workflow or Replit module relies on Node 20. Keep the npm lockfile.

### SD-07 - Vulnerability response coverage is narrower than the dependency inventory

**P2; medium maintenance risk; CONFIRMED coverage, UNKNOWN unscanned advisories.** `npm audit` returned zero advisories for three installed dependency records. That only covers the root QA dependency tree; it does not assess the vendored Mermaid runtime. Mermaid 11.17.2 is pinned with a daily version watcher, which is valuable. GitHub API reports secret scanning and push protection enabled, but Dependabot security updates disabled. Monthly npm/pip/Actions version updates are configured.

**Proposal:** Enable security update PRs after checking repository eligibility and desired workflow. Create a concise vendor inventory with upstream package/version, tarball integrity, included dependencies, license notices and update procedure. Distinguish “new version available” from “security advisory affects this version.” Include pinned Python QA dependencies in a read-only advisory check. Preserve intentional review before re-vendoring.

**Acceptance:** A dependency inventory covers QA dependencies and shipped vendor code separately. Security advisory review has an owner and response target. Re-vendoring checks entry modules and all relative chunks, license distribution, CSP, clickable diagram destinations and every diagram page. The runtime LICENSE exists in source but is excluded by the current extension-based release asset rule; review notice distribution during this work.

### SD-08 - Root preview server is broader than necessary on a workstation

**P2; medium conditional local exposure; CONFIRMED source behavior, UNKNOWN network reachability.** `server.py:9` binds `0.0.0.0`; it serves the current working directory using `SimpleHTTPRequestHandler`, with no source-file exclusions. The CSP report receiver appends attacker-supplied report objects to a local file and has no rate/total-size retention bound. It caps positive Content-Length at 64 KiB but does not reject negative values before `read(length)`. Python documents that this handler follows symbolic links. No live report POST, network scan, or exposure test was performed. [Python server security notes](https://docs.python.org/3/library/http.server.html).

**Proposal:** Default workstation preview to loopback and require explicit binding for Replit. Offer preview of the release artifact for public sharing. Reject invalid/negative lengths, enforce a request timeout and maximum report-file size, and keep report collection optional. Deny source and dotfile serving when external preview is needed.

**Acceptance:** Default launch listens on loopback; explicit Replit binding still works. Controlled fixtures verify forbidden paths and symlinks are not served, invalid lengths fail promptly, and report storage is bounded. Existing browser QA continues to work.

### SD-09 - Analytics has disclosure but no first-party visitor choice

**P2; privacy/product decision; CONFIRMED source behavior, UNKNOWN account-side configuration.** `index.html:99-106` loads Google tagging and runs `gtag('config', ...)` without a default consent state. The generated page source contains no consent control. `site-src/pages/legal/index.main.html:43-61` discloses analytics and cookies, but delegates limiting them to browser controls. The site addresses multiple locales; the applicable legal analysis and Analytics account retention/ad settings were not inspected.

**Proposal:** Define what measurement is actually needed. Prefer a simple analytics-off choice with clear persistence and withdrawal. If Google Analytics remains, implement the selected basic/advanced consent behavior before configuration and align notices with observed network behavior. Do not describe advanced consent mode as “no requests before consent”; denied storage may still permit measurement pings. [Google consent implementation guide](https://developers.google.com/tag-platform/security/guides/consent).

**Acceptance:** Fresh-profile, accepted, rejected and withdrawn states have documented network/cookie expectations and tests. Rejecting analytics leaves all public content functional. Confirm account-side retention and advertising settings separately. This is a technical recommendation, not a finding of legal noncompliance.

### SD-10 - Publishing instructions reference an obsolete cross-repository write helper

**P1 documentation repair; medium process risk; CONFIRMED.** `docs/publishing.md:15-33` tells a Replit operator to configure a PAT and run `scripts/push-to-github.py`; that active path does not exist. The archived script hardcodes writes across OverKill-Hill, AskJamie and Glee-fullyTools using temporary source paths. Repairing the command by simply inserting `archive/` would reinstate a broad historical write operation. README also describes `_headers` as report-only even though its current declaration is enforcing.

**Proposal:** Replace the fallback section with the current protected Git/PR publishing procedure. Label the historical helper as retired and link its archive explanation only for history. Reconcile release and header wording with actual scripts. Do not revive the archived helper for a one-site audit or routine release.

**Acceptance:** Every active release command resolves to an active script with the documented behavior. No standard publishing instruction requires broad cross-repository contents-write credentials. Documentation correctly distinguishes page meta enforcement, desired enforcing response policy, and undelivered production headers.

### SD-11 - Branch controls protect checks, but do not require independent approval

**P2; owner governance decision; CONFIRMED.** Current `main` protection requires the strict `Validate site HTML, links, and structure` check, disallows force pushes and deletion, and requires PR processing. It requires zero approving reviews, does not enforce protection for admins, and does not require code-owner, last-push or conversation-resolution approval. The Pages environment permits the `main` branch and has no reviewer rule. These are reasonable choices for some single-owner repositories; they should be explicit as more agents write code.

**Proposal:** Keep routine content flow light. Require owner review for workflow, release packaging, security policy and shared runtime changes, using CODEOWNERS/rulesets where practical. Retain an explicit emergency path rather than pretending admin bypass is impossible. Independent human review requires another actual reviewer; do not configure an impossible approval requirement for a sole maintainer.

**Acceptance:** A test PR changing a protected delivery path cannot reach production without the selected owner review and required tests. Ordinary content PRs retain proportionate friction. Record who may approve and bypass, and review the policy when delegation expands.

### SD-12 - Monitoring and validation should report decision-level status

**P2; operational clarity; CONFIRMED design and observed warning volume.** The live report correctly separates `PARTIAL` from `PASS`, but 315 warnings and 38 blocked checks are buried in an artifact while the workflow succeeds. The external-runtime monitor deliberately does not fail for its reported route/dependency issues. Push also invokes standalone validation and reusable Pages validation with the same event/ref concurrency group; one standalone run was canceled for the observed release. This overlap is a source-level coordination risk, not the confirmed cause of the artifact retry failure.

**Proposal:** Publish a compact Actions summary with content delivery, policy enforcement, third-party availability and last-good SHA shown separately. Deduplicate expected repeated header limitations into a control-level rollup while retaining per-route evidence. Route new external outages through a distinct alert policy. Use an explicit trigger/input model for reusable validation so source and release execution do not inadvertently cancel one another.

**Acceptance:** An operator can tell “content passed; edge policy remains partial” without downloading JSON. A newly broken first-party route alerts; an accepted missing header does not flood the queue; a third-party outage has a visible owner and recovery state. Rapid consecutive pushes and manual dispatch have predictable validation/deploy behavior.

## Browser-code assessment

The reviewed shared JS escapes search text before HTML insertion, restricts search data loading to same-origin resources, and avoids `eval`, `document.write` and a generic cross-window message handler in the reviewed modules. Most Mermaid diagrams use strict security mode. Two curated heat pages opt into loose mode, with an explicit outbound target allowlist. These are useful controls.

Two defense-in-depth tasks are appropriate when touching these paths: validate search-index entry types and URL protocols before using an entry as a link; and test the Mermaid click-directive parser against unsupported syntax rather than describing its narrow regex as a universal sanitizer. Current search data and diagrams are repository-authored. No visitor-controlled path to executable content was demonstrated, so these are P2 hardening proposals, not confirmed XSS findings. Keep embedded applications on their own trust boundary and preserve their user-visible fallback routes.

## Validation performed

| Check | Context | Result | Limitation |
| --- | --- | --- | --- |
| `npm audit --json` | Owner checkout | PASS, zero returned advisories | QA tree only; not vendored/runtime-wide clearance. |
| `python3 tests/test-release-package.py` | Owner checkout | PASS, 3 tests | Existing tests do not detect changed JS bytes; separate probe demonstrates gap. |
| `python3 -m unittest tests/test_verify_live_edge.py` | Owner checkout | PASS, 9 tests | Tests verifier behavior, not production protections. |
| `python3 scripts/generate-csp.py --check` | Owner checkout | FAIL | Older local checkout is stale relative to canonical CSP calculation. |
| `python3 scripts/check-csp.py` | Owner checkout | FAIL | Multiple public and pilot HTML files differ from computed policy. No regeneration performed. |
| Current remote CSP/browser gates | GitHub `40e18ee7` | PASS in successful Pages run | Parent assessment owns independent local checks of the frozen remote snapshot. |
| Live edge verifier | Downloaded CI artifact at `40e18ee7` | PARTIAL, 427/0/38/315 | Check counts are checks/failures/blocked/warnings. |
| Seven bounded public GETs | Canonical domain | Four expected public resources 200; three tested nonpublic/unsupported paths 404 | GET `/__csp-report` does not test POST report ingestion. |
| Isolated package content-change probe | Temporary artifact, removed afterward | Changed copied JS still verified | Harmless fixture only; no production mutation. |
| GitHub configuration APIs and run logs | Read-only | Protection, security settings, Pages and failure reason captured | No repository or account settings changed. |

The older checkout failure must not be reported as a current production CSP regression: remote `40e18ee7` changed CSP discovery and regenerated outputs, and its CI passed. The audit preserves both facts instead of flattening them into a single status.

## Executable work packages

| Order | Package and suggested executor | Scope | Completion evidence |
| --- | --- | --- | --- |
| 1 | Release correctness - Codex or Copilot | SD-03 and SD-05; isolated branch, builder/workflow/tests only | Negative digest fixtures, retry scenario, validated artifact and release SHA. |
| 2 | Tooling lifecycle and runbook - Copilot with owner review | SD-06, SD-07 security PR setting proposal, SD-10 | LTS CI run, active-command check, vendor inventory and response procedure. |
| 3 | Publication boundary - Codex, Replit executor for verified Replit configuration | SD-04 and SD-08 | Identical dry artifact inventories, preview boundaries, no automatic publication. |
| 4 | Edge adapter proposal - Codex, owner controls deployment | SD-01 and SD-02 | Host choice, cost/operational tradeoff, staging policy evidence, rollback plan; owner authorizes infrastructure change. |
| 5 | Privacy behavior - Codex with owner measurement decision | SD-09 | Documented chosen behavior, network/cookie fixtures, matching public notice. |
| 6 | Governance and monitoring - Copilot, owner config review | SD-11 and SD-12 | Clear status summary, predictable triggers, owner approval policy and outage routing. |

Each package should have one reviewable PR and a named acceptance record. Shared JS/CSS changes also require the repository's existing cross-site compatibility review and synchronization process. Replit should implement preview/config work only after the target artifact and instructions are concrete; Copilot can take bounded test and workflow changes; the main agent should retain architectural decisions and final evidence reconciliation.

## Remaining unknowns

Live Replit deployment configuration and visibility, registrar/DNS account controls, edge-provider availability and pricing for this owner, Analytics account retention and advertising settings, vendored dependency advisory status, Python advisory status, alternate regional edge behavior, and independently audited external embedded applications remain unknown. The next checks are read-only inventories in those systems after choosing the relevant work package. Browser-wide UX, accessibility and content findings are covered by the companion assessment workstreams.

This report used `okhp3-site-release-validation` and `okhp3-evidence-standard`. Prior memory about missing production headers directed a fresh check; all current security/delivery conclusions above rely on source, API, CI, official documentation or live evidence collected during this assessment.
