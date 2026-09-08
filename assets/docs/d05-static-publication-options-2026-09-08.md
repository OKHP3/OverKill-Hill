# D05 Replit static publication closeout

## Outcome: source exposure fixed

On September 8, 2026, the owner authorized repairing the old public Replit
publication while preserving repository sources. PR #85 merged at
`1af9218fe22562800a6383c0271d67357c3f3318`; A21 confirmed its Git tree matched the
independently reviewed candidate `3003da99fe1f5a8f5d855e7e01fa205046a4f678`.
Required Site Validation run `34258607857` and i18n run `34258607792` passed.

The actual Replit project was synchronized to that accepted commit. Its
Publishing settings showed `.local/site-release` as the effective public
directory. The deployment-specific `REPLIT_RELEASE_SHA` was submitted with the
same full SHA through Settings > Publish. The successful publication completed
its build and bundling stages; Production reported a new publication.

Public URL: <https://over-kill-hill.replit.app/>
Source change: <https://github.com/OKHP3/OverKill-Hill/pull/85>

## Verification

The root executor verified the live manifest contains the accepted SHA and 372
files. Public homepage, project hub, JavaScript, and stylesheet returned 200.
The following internal paths returned 404:

- `/server.py`
- `/site-src/pages.json`
- `/AGENTS.md`
- `/replit.md`
- `/.git/config`
- `/scripts/build-release.py`
- `/tests/test-preview-server.py`
- `/.local/`

A18 independently verified at `2026-09-08T17:55:31Z` that the live manifest
matched the accepted SHA. Homepage, `/projects/found-ry/`, JavaScript,
stylesheet, and search-index responses returned 200 and their SHA-256 values
matched the live manifest. Nine private/listing paths returned 404, including
`/.replit`, `/scripts/build-replit-release.py`,
`/.local/site-release/index.html`, and `/assets/js/`. A18 accepted D05 source
exposure remediation as PASS.

A21 independently verified the same manifest and public/private boundary at
`2026-09-08T17:55:36Z`, including `/contact/` 200 and `/.local/a08/` 404.
Only statuses and public manifest/hash markers were retained; source response
bodies were not retained.

## Build and recovery contract

`.replit` invokes `python3 scripts/build-replit-release.py`. The wrapper
requires an explicitly accepted full `REPLIT_RELEASE_SHA`, matching HEAD, and a
clean checkout. This does not independently attest GitHub CI; the publication
operator supplies the SHA whose required checks and review passed.

Before building, prior output moves into unique private recovery storage under
`.local/replit-release-*/previous`. Failed preflight, build, or verification
leaves the public output directory absent. The wrapper builds and verifies the
allowlisted package, rechecks source identity, then promotes the package to
`.local/site-release`. It preserves recovery and failed staging bytes privately
and performs no recursive deletion.

Eight focused tests ran: seven passed and the Windows symlink-privilege test
skipped. Tests cover fresh and repeated builds, preflight/build/verification
failure, preservation, SHA identity, clean source, and path guards. The suite is
wired into CI. Two real local builds each verified 56 HTML pages and 372 files.
After staging, generated-source checks remained 36 pages, search remained 160
entries, structural validation remained 56 pages, and the checkout stayed
clean. The actual Replit workspace also built and verified the package before
publication. Existing `.local/` exclusions prevent staging from polluting
source scans or recursive packaging.

The first publish attempt failed closed because leaving the settings draft
with Back discarded the new variable. The corrected attempt submitted the
variable using Settings > Publish and completed successfully. No safeguard was
relaxed and no repository authoring file was removed.

Official configuration references:
[Replit deployment types](https://docs.replit.com/features/publishing/deployment-types)
and [Replit configuration](https://docs.replit.com/features/project-setup/configuration).

## Separate host compatibility limit

`/.well-known/security.txt` appears in the release manifest but returned 404
from Replit in A18's independent check. The exact host cause is unverified;
this is a documented public-route compatibility limit, not a source-exposure
failure. This repair does not claim full Replit route parity or header-policy
acceptance. No hosting migration or retirement was performed.

## Related runtime closeout

PR #83 merged the Replit Node 24 module at
`6071bc2b0c748fde88b1d5ef1302e039e256444b`. Actual Replit main was clean and
synchronized at that SHA, and a fresh shell reported Node 24.13.0 and npm
11.6.2. The publication fix retains that runtime setting. Runtime tests and
preview-boundary evidence remain in `qa-runtime-a08-2026-09-07.md`.

## Post-publication reconciliation

On September 8, Replit created an empty-tree `Published your App` checkpoint
`065e75c0263a2e7a28799485c7a7fe08332e9274`. Its file tree matched the published
source commit `1af9218fe22562800a6383c0271d67357c3f3318`; both diff statistics and
changed-path inventory were empty. The checkpoint was preserved locally and
pushed to `codex/replit-publication-checkpoint-20260908`. No reset, deletion,
or authoring-source removal was used.

Replit's local main was then recreated from the current remote main and
verified clean, ahead/behind 0/0, at
`bdd6bed1c737cf4d44e7cea5dae37afb33e18970`. This later source HEAD is distinct
from the accepted Replit live release SHA, which remains
`1af9218fe22562800a6383c0271d67357c3f3318`. Subsequent repository integration
must not be represented as a Replit publication without a new verified publish.
