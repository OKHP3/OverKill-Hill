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