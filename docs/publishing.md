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

## Scheduled production drift monitor

The same workflow runs a read-only check against the canonical production
origin every six hours and on manual dispatch. It does not assume that the
latest GitHub commit is already published, so scheduled monitoring checks the
production edge's routes, generated artifacts, security headers, cache
policies, and fingerprints without `--expected-commit`.

Each run uploads `live-edge-monitor-<run-id>` as evidence for 30 days. A
`FAILED` report fails the monitor and identifies deterministic policy or
content drift. A `PARTIAL` report records blocked network checks, keeps the
report available, and emits a warning instead of calling an external outage a
policy regression. A missing or malformed report also fails the monitor.

## Production edge requirement

GitHub Pages does not read `_headers`. The custom domain must therefore be
proxied through the configured Cloudflare zone, with the response-header and
cache rules from `_headers` applied at that edge. The GitHub Pages deployment
remains the origin and continues to publish the repository contents; Cloudflare
is the layer that emits the security headers and replaces the origin's default
`Cache-Control: max-age=600`.

Before treating a release as complete, confirm that the production DNS record is
orange-cloud proxied and run the verifier against `https://overkillhill.com`.
If the response still identifies `GitHub.com` without the required headers,
Cloudflare is not in the request path and the release is not edge-complete.