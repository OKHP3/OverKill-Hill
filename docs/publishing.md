# Secure GitHub publishing

## Normal release path

Push the reviewed commit to `main`. `.github/workflows/validate.yml` checks that
exact commit, then the Pages job runs only when validation succeeds. The deploy
job has read-only contents access plus the minimum Pages write and OIDC
permissions. Its `pages` concurrency group prevents overlapping deployments.

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

After a Pages deployment, run the verifier with the deployed origin explicitly
provided. It reads the committed sitemap and generated search index, requests
every sitemap route plus the noindex utility boundaries, checks security and
cache headers, and verifies that shared CSS/JS fingerprints match the checked
out files:

```bash
python3 scripts/verify-live-edge.py \
  --base https://overkillhill.com \
  --report assets/audit/live-edge-report.json
```

The command is read-only with respect to the site and uses no credentials. It
has a per-request timeout and writes partial results before exiting. A missing
route, security header, generated-artifact match, cache policy, or fingerprint
is a nonzero failure; external unavailability is reported rather than treated
as a pass. Do not omit `--base` or substitute a guessed deployment URL.

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