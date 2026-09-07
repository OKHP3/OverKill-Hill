# Secure GitHub publishing

## Normal release path

Prepare the change on a review branch in this repository and run the relevant
checks from [Site Validation](../.github/workflows/validate.yml). Open a pull
request for review. Merge into protected `main` only within the owner's publication
authorization; passing local checks is not itself a publication instruction.
Use the existing authenticated Git/GitHub workflow. This runbook does not
require a new credential or changes to account permissions.

[Publish GitHub Pages](../.github/workflows/pages.yml) invokes the reusable
validation workflow for the exact release revision. Validation builds an
allowlisted `site-release` artifact named
`validated-site-<commit-sha>-<run-id>-<run-attempt>`. Committed HTML, search,
and universe freshness are checked before regeneration. The reusable workflow
returns the successful validation attempt's artifact name to the download step,
including when only deployment is retried. Pages upload and deployment both use
`github-pages-<run-id>-<run-attempt>` so retries do not select an earlier Pages
artifact. Keep the validated artifact available during its one-day retention;
after expiry, rerun validation and deployment together.
The deploy job downloads that artifact and verifies its commit identity and
recorded file hashes and byte lengths with `scripts/build-release.py --verify`
before uploading it to Pages. The local schema 3 implementation covers every
packaged file except the manifest itself; production remains schema 2 until
this change is released. The manifest is a trusted-workflow integrity record,
not an independent signature. The `pages` concurrency group queues deployments.
The deployment job uses read-only contents access, Pages write access, and
OIDC permission.

After deployment, confirm the workflow result and the uploaded live-edge
report. A release is not verified solely because a push or merge succeeded.
Read the deployed manifest and checks against the exact intended revision.

## Historical Replit API helper

The former `scripts/push-to-github.py` is archived at
[`scripts/archive/push-to-github.py`](../scripts/archive/push-to-github.py).
It is not an active release command. Its historical PAT-based governance
sync procedure is not a fallback for the normal PR and Pages workflow.
Do not run it for a current site release without a separate, scoped review of
its destinations and behavior.

## Failure diagnosis

- Validation failure: run the same commands from the `validate` job locally and
  fix the reported file or generated artifact before retrying.
- Pages failure: confirm the workflow has `pages: write` and `id-token: write`,
  then inspect the failed `upload-pages-artifact` or `deploy-pages` step.
- Authentication failure: inspect the existing Git/GitHub session and report
  the exact blocked operation. Resolve access through the approved account
  workflow; never paste credentials into chat, a file, or a Git remote.

## Read-only live-edge verification

The Pages workflow runs this verifier after deployment, using the deployment
URL and the validated commit SHA. It uploads the resulting JSON as the
`live-edge-report-<run-id>-<run-attempt>` release evidence artifact. The check reads the
committed sitemap and generated search index, requests every sitemap route plus
the noindex utility boundaries, checks security and cache headers, verifies
shared CSS/JS fingerprints, and confirms the deployed release manifest:

```bash
python3 scripts/verify-live-edge.py \
  --base https://overkillhill.com \
  --expected-commit "$(git rev-parse HEAD)" \
  --hosting github-pages \
  --accept-blocked \
  --report assets/audit/live-edge-report.json
```

The command is read-only with respect to the site and uses no credentials. It
has a per-request timeout and writes partial results before exiting. A missing
manifest, commit mismatch, artifact hash mismatch, route, generated artifact,
cache policy, or fingerprint is a nonzero failure in the applicable hosting
mode. In strict mode, missing security headers also fail. In
`--hosting github-pages` mode, a missing response header is an explicit `WARN`
accepted as a direct-Pages hosting limitation; it is not delivered protection.
External unavailability remains `BLOCKED`, and any blocked or warning checks
produce `PARTIAL` status rather than a policy pass. Use `--expected-commit` for
release verification. Do not omit `--base` or substitute a guessed deployment
URL.

### Policy layers and evidence

The repository's desired edge policy is [`_headers`](../_headers), generated
from the canonical policy data in
[`config/csp-policies.json`](../config/csp-policies.json). The page-level
`Content-Security-Policy` meta tags are generated from the same policy source
and are checked locally by `scripts/check-csp.py`; browser CSP QA then observes
runtime violations and page errors. These checks establish the intended policy
and page behavior, not response-header delivery by GitHub Pages.

The live-edge verifier requests the public response headers separately. A
present enforcing `Content-Security-Policy` is recorded as observed, while its
contents are explicitly not validated against the local policy artifact by
that verifier. A report-only CSP is recorded separately as `WARN` because it
does not enforce protection. When direct GitHub Pages omits a desired header,
the verifier records the absence as `WARN`; this documents the accepted
hosting limitation without describing the missing control as active.

### Historical canonical-domain result (September 3, 2026)

**Run date:** September 3, 2026
**Base:** `https://overkillhill.com`
**Expected deployed commit:** `860467f004ea88057e02764fd36a5ffc36cfa52b`
**Evidence:** `assets/audit/live-edge-report-2026-09-03.json`
**Result:** **PARTIAL — accepted direct GitHub Pages strategy; policy headers remain blocked**

The verifier reached the canonical domain with no blocked content-availability requests. The
live release manifest is reachable and identifies commit
`860467f004ea88057e02764fd36a5ffc36cfa52b`. Its SHA-256 values match both the
served `/sitemap.xml` and `/assets/data/search-index.json`, and those files
match the validated release checkout. The sitemap routes, noindex boundary, and
fingerprinted shared assets also passed.

DNS still resolves `overkillhill.com` directly to GitHub Pages
(`185.199.108.153` through `185.199.111.153`, plus GitHub's IPv6 addresses).
The live response identifies `server: GitHub.com`, includes GitHub/Fastly
markers, and returns `Cache-Control: max-age=600`. GitHub Pages does not read
the repository `_headers` file, so the declared security headers and cache
policies are reported as `BLOCKED`, not as policy passes. The current evidence
is therefore `PARTIAL`, not `PASS` and not a claim that the `_headers` contract
is enforced.

### Accepted direct GitHub Pages strategy

For the current release, direct GitHub Pages is the explicitly accepted
hosting strategy for this canonical static site. The acceptance is limited to
the evidence GitHub Pages can provide: route availability, robots boundaries,
generated-artifact integrity, release-manifest binding, and content-fingerprint
integrity. It does not waive the security or cache requirements in `_headers`.

The verifier's `--hosting github-pages` mode proves that the request path is
still direct GitHub Pages, records omitted security headers as `WARN` and
hosting-controlled cache checks as `BLOCKED`, and returns `PARTIAL` when no
deterministic checks fail. It returns
`FAILED` for a real route, artifact, manifest, fingerprint, or hosting-path
failure. Scheduled monitoring uses this mode with `--accept-blocked`, so a
known hosting limitation is visible as `PARTIAL` while real drift still fails
the workflow.

To enforce the full `_headers` contract later, proxy the custom domain through
an authorized edge that can emit response headers and override the origin cache
policy, then rerun the verifier in its default `strict` mode. Until that
happens, do not describe the production site as enforcing the `_headers`
security or cache policy.

### Historical DNS and edge-path follow-up (September 3, 2026)

**Checked:** September 3, 2026
**Evidence:** live DNS resolution and HTTPS response headers from the canonical domain

The follow-up check resolved `overkillhill.com` directly to GitHub Pages addresses
(`185.199.108.153` through `185.199.111.153`, plus GitHub's IPv6 addresses).
`www.overkillhill.com` resolved through the `okhp3.github.io` alias. HTTPS responses
identified `server: GitHub.com`, included GitHub/Fastly cache markers, and continued
to return `Cache-Control: max-age=600`. No Cloudflare edge marker or the headers
declared in `_headers` was present.

This confirmed that the canonical hostname was reaching GitHub Pages at that check
directly rather than a Cloudflare-proxied edge. No Cloudflare zone or Transform
Rules control is available through the approved workspace access path, so no
edge configuration was changed. The accepted direct-Pages strategy and its
limits are recorded above. Re-run the verifier in `strict` mode after any
future edge change before claiming production enforcement.

## Scheduled production drift monitor

The same workflow runs a read-only check against the canonical production
origin every six hours and on manual dispatch. It does not assume that the
latest GitHub commit is already published, so scheduled monitoring checks the
production edge's routes, generated artifacts, security headers, cache
policies, fingerprints, and the release manifest without `--expected-commit`.
In that mode the manifest's artifact hashes are compared with the live
artifact bytes, while the verifier does not compare those bytes with the
newest checkout.

Each run uploads `live-edge-monitor-<run-id>` as evidence for 30 days. A
`FAILED` report fails the monitor and identifies deterministic policy or
content drift. A `PARTIAL` report records blocked network checks, keeps the
report available, and emits a warning instead of calling an external outage a
policy regression. A missing or malformed report also fails the monitor.

## Production edge requirement

GitHub Pages does not read `_headers`. Under the accepted direct-Pages
strategy, GitHub Pages remains the origin and serves the repository contents
with its native cache behavior; the verifier records the unfulfilled header
and cache controls as `BLOCKED`. The full contract still requires a configured
edge proxy to emit the security headers and replace the origin's default
`Cache-Control: max-age=600`.

For the accepted direct-Pages strategy, confirm the hosting-path check, release
manifest, artifact hashes, routes, and fingerprints, then run the verifier
against `https://overkillhill.com` with `--hosting github-pages
--accept-blocked`. For full edge enforcement, confirm that the production DNS
record is proxied and run the verifier without `--hosting github-pages`.
