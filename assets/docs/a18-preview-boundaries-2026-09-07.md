# A18 preview exposure boundaries, September 7, 2026

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.
Scope: local preview and release source-copy guards. No hosting configuration,
remote Replit checkout, sibling repository, content, or generated page changes.

## Reproduced

A temporary loopback instance of baseline `server.py` returned HTTP 200 and
2,031 bytes for `/server.py`. Source inspection confirmed an all-interface
bind default, negative Content-Length acceptance before reading, an unbounded
append file, and unrestricted SimpleHTTPRequestHandler serving. The release
builder's copy paths also followed linked source files.

## Changes

- Loopback is the default; explicit HOST/PORT overrides remain available.
- Preview inventory uses existing release builder APIs and archive policy.
  Public GET/HEAD and directory redirects work; listings, private paths,
  traversal, Windows alternate-stream paths, symlinks, and junctions are denied.
- Reports require one positive length of at most 64 KiB. Transfer encoding,
  invalid JSON, non-object reports, truncated input and excessive encoded data
  are rejected. Socket inactivity timeout is five seconds.
- A private temporary report file replaces CSP_REPORT_FILE and shared append
  storage. Locked writes enforce a 1 MiB per-process cap; full storage returns
  507. The file is removed when closed. No permanent collection is provided.
- Release copies reject hidden files, linked paths and root escapes. Existing
  allowlist APIs and schema 3 remain unchanged. A07 confirmed it does not edit
  the builder before this scoped change was made.

## Validation

- PASS: preview HTTP regressions, default/explicit bind, allowlist, malformed
  input, concurrent storage cap and actual Windows directory junction rejection.
- NOT RUN: file symlink HTTP regression; this Windows host denied symlink
  creation. The test remains available for a Linux runner.
- PASS: existing release package suite, nine tests.
- PASS: structural site validator, with accepted baseline voice warnings.
- PASS: generated HTML freshness, 36 pages; search index freshness.
- PASS: diff whitespace check.

Run `python3 tests/test-preview-server.py` and
`python3 tests/test-release-package.py` on the integrated candidate. A21 should
include the preview regression in the combined CI test contract. No CI run,
merge, deployment, or live Replit acceptance is claimed here.

## Remaining boundary

The checked-in `.replit` still declares `publicDir = "."`. No actual connected
Replit checkout or external reachability was established, so it was not changed.
That publication route requires an allowlisted artifact or retirement before
external use. This local server is a preview utility, not a hardened public
service. Filesystem checks assume a trusted checkout; they do not defend against
a concurrent malicious local process replacing files between check and open.
