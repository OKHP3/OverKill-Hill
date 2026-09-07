# A18 preview and Replit exposure handoff

September 7, 2026. Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.
Branch: `codex/a18-preview-exposure`. The package commit is the commit containing
this handoff; its immutable SHA is supplied directly to A21 after commit.

## Disposition

Local correction implemented and tested. External Replit publication remains
closed pending account inspection and an explicitly verified artifact route.
No current production SHA, Replit reachability, or platform configuration is
claimed. No hosting, account, DNS, sibling, main, or publication changes occurred.

## Reproduction and correction

The baseline `server.py` sets HOST to `0.0.0.0`, delegates GET to the unrestricted
current-directory SimpleHTTPRequestHandler, reads `min(Content-Length, 65536)`
without rejecting negative values, and appends reports without a storage cap.
Baseline `.replit` declares `publicDir = "."`. These reproduce the source
conditions recorded as D05 in the September 7 delivery/security assessment.
The initial test attempt also demonstrated that importing the baseline starts
its listener immediately; the sandbox denied that bind. That initial run is
not counted as a successful behavioral test.

- `server.py`: defaults to loopback, anchors serving to the repository containing
  the script, and reuses the reviewed release builder's public route, asset,
  and artwork-exclusion inventory. Existing file edits remain immediately
  visible; new public files require restart. No release builder edits are made.
- Every HTTP file open traverses directory descriptors with `O_NOFOLLOW` and
  checks for a regular file. Source paths, dotfiles, traversal, directory
  listings, and symlink files or parents are denied. `.well-known` is the sole
  allowed dot-directory. `.nojekyll` is intentionally not served by preview.
- CSP collection is opt-in. Requests require one positive decimal length up
  to 64 KiB, a supported JSON media type, and an object body. Transfer encoding,
  incomplete bodies, invalid JSON and ambiguous lengths are rejected.
  Private temporary session storage is capped at 1 MiB under a lock. Full
  storage returns 507. Shutdown discards storage; `CSP_REPORT_FILE` is retired.
- Requests have five-second socket inactivity timeouts and a 32-worker cap.
  This bounds resources; it does not provide production denial-of-service
  protection or an absolute wall-clock deadline for a trickling client.
- `.replit`: makes its preview bind explicit and removes repository-root static
  deployment metadata. This retires the unsafe checked-in publication route;
  it cannot disable an already configured platform deployment.
- `replit.md`: records operation, collection limits, POSIX requirement, and
  publication boundary. `tests/test-preview-server.py` owns the HTTP regressions.

## Actual validation

Python 3.14.5 on macOS. HTTP tests used ephemeral loopback ports after the
sandbox initially denied binding; no external endpoint was probed.

- `python3 tests/test-preview-server.py`: 10 tests PASS, 5.205 seconds. Coverage
  includes GET/HEAD/redirect behavior, all 369 selected repository files
  (56 HTML pages), source/dotfile/listing/traversal rejection, file and parent
  symlinks including replacement after inventory creation, invalid/negative/
  oversized/duplicate lengths, transfer encoding, short bodies, read timeout,
  media type and object validation, disabled collection, sequential and
  concurrent storage limits, and parsed Replit configuration.
- `python3 tests/test-release-package.py`: 9 tests PASS, 2.592 seconds.
- `python3 -m py_compile server.py tests/test-preview-server.py`: PASS.
- `git diff --check`: PASS.

No generated HTML, CSP, search, universe, asset fingerprint or locale changes
are required. Preview shares the release selection functions but is not a
SHA-bound release and does not regenerate or authenticate working-tree bytes.
No new dependencies. Artwork, public URLs and locale indexing are unchanged.

## Integration and remaining acceptance

A21 must preserve A08's runtime work when integrating `.replit`; A18 changes
only the preview command and deployment block. No shared runtime files or
workflow YAML are changed. A08 was notified directly.

Independent integrated browser/CI checks and Python 3.11/Linux execution were
not run here. The secure opener requires POSIX directory-relative no-follow
operations; Windows preview support is not established. Durable CSP report
export is not part of this package.

Before externally publishing through Replit, inspect actual platform settings,
confirm any old repository-root deployment is retired, then test a reviewed
allowlisted artifact route on that platform. This requires the separately
selected publication action. Canonical Pages remains unchanged. Source tests
alone do not establish that an existing external Replit path is safe or off.
