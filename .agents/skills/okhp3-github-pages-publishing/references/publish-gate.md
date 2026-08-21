# GitHub Pages publishing gate

Before a write, prove all of the following:

- the validation report names the exact full SHA being deployed;
- `HEAD` and the clean worktree match that SHA;
- the workflow deploy job depends on validation and checks out that SHA;
- write permissions are limited to the deploy job, with `contents: read`,
  `pages: write`, and `id-token: write`;
- untrusted pull-request code is never executed with those write permissions;
- the credential is scoped, supplied by a secret manager, and absent from
  remotes, files, logs, URLs, and reports.

After the write, confirm the workflow result, Pages deployment SHA (where the
host exposes it), HTTP status/headers for key routes, sitemap/index freshness,
and a cache-busted CSS or JS URL. If any item is missing, report `PARTIAL`.