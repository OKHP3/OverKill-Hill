# Secure GitHub publishing

## Normal release path

Push the reviewed commit to `main`. `.github/workflows/validate.yml` checks that
exact commit, then the Pages job runs only when validation succeeds. The deploy
job has read-only contents access plus the minimum Pages write and OIDC
permissions. Its `pages` concurrency group prevents overlapping deployments.
Before upload, the job writes `assets/audit/release-manifest.json` with the
validated commit SHA and SHA-256 hashes for `sitemap.xml` and
`assets/data/search-index.json`. That manifest is deployed with the site, so a
Pages artifact cannot be treated as current unless it identifies the commit
that passed validation and the generated files match its recorded hashes.

## Controlled API publishing from Replit

Use this only when the normal GitHub workflow is unavailable or when syncing
the explicitly listed governance files in `scripts/push-to-github.py`.

1. Create or use the workspace secret named `GITHUB_PAT`. Use a fine-grained
   credential limited to the required repositories and contents write access.
2. Run the helper without copying the credential into a file or remote:

   ```bash
   GITHUB_TOKEN="$GITHUB_PAT" python3 scripts/push-to-github.py
   ```

3. Review the API response and resulting commit in GitHub.

The script uses HTTPS and an Authorization header. It does not rewrite Git
remotes, persist the credential, or print it. Do not use the OAuth credential
used by ordinary Replit Git pushes for this path. Rotate or remove the
fine-grained credential when the controlled operation is complete.

## Failure diagnosis

- Validation failure: run the same commands from the `validate` job locally and
  fix the reported file or generated artifact before retrying.
- Pages failure: confirm the workflow has `pages: write` and `id-token: write`,
  then inspect the failed `upload-pages-artifact` or `deploy-pages` step.
- Authentication failure: repair the `GITHUB_PAT` workspace secret and its
  repository permissions. Never paste a token into chat or a Git remote.

## Read-only live-edge verification

The Pages workflow runs this verifier after deployment, using the deployment
URL and the validated commit SHA. It uploads the resulting JSON as the
`live-edge-report-<run-id>` release evidence artifact. The check reads the
committed sitemap and generated search index, requests every sitemap route plus
the noindex utility boundaries, checks security and cache headers, verifies
shared CSS/JS fingerprints, and confirms the deployed release manifest:

```bash
python3 scripts/verify-live-edge.py \
  --base https://overkillhill.com \
  --expected-commit "$(git rev-parse HEAD)" \
  --report assets/audit/live-edge-report.json
```

The command is read-only with respect to the site and uses no credentials. It
has a per-request timeout and writes partial results before exiting. A missing
manifest, commit mismatch, artifact hash mismatch, route, security header,
generated-artifact match, cache policy, or fingerprint is a nonzero failure;
external unavailability is reported with `PARTIAL` status rather than treated
as a policy pass. Use
`--expected-commit` for release verification. Do not omit `--base` or
substitute a guessed deployment URL.

### Latest canonical-domain result

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
still direct GitHub Pages, marks controls that GitHub Pages cannot apply as
`BLOCKED`, and returns `PARTIAL` when no deterministic checks fail. It returns
`FAILED` for a real route, artifact, manifest, fingerprint, or hosting-path
failure. Scheduled monitoring uses this mode with `--accept-blocked`, so a
known hosting limitation is visible as `PARTIAL` while real drift still fails
the workflow.

To enforce the full `_headers` contract later, proxy the custom domain through
an authorized edge that can emit response headers and override the origin cache
policy, then rerun the verifier in its default `strict` mode. Until that
happens, do not describe the production site as enforcing the `_headers`
security or cache policy.

### Confirmed DNS and edge-path follow-up

**Checked:** September 3, 2026
**Evidence:** live DNS resolution and HTTPS response headers from the canonical domain

The follow-up check resolved `overkillhill.com` directly to GitHub Pages addresses
(`185.199.108.153` through `185.199.111.153`, plus GitHub's IPv6 addresses).
`www.overkillhill.com` resolved through the `okhp3.github.io` alias. HTTPS responses
identified `server: GitHub.com`, included GitHub/Fastly cache markers, and continued
to return `Cache-Control: max-age=600`. No Cloudflare edge marker or the headers
declared in `_headers` was present.

This confirms that the canonical hostname is currently reaching GitHub Pages
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
