# Wave one release closeout

Status: DEPLOYED; live-edge result PARTIAL with zero failures. This closes the
selected release wave, not the full advancement program or actual human/device
acceptance. Report date: September 7, 2026.

## Release identity

- PR62: https://github.com/OKHP3/OverKill-Hill/pull/62
- Reviewed candidate: `23e78e0dae0c441a0b42f11d01a0af6748c1de1c`.
- Merged and live revision: `eeb3960778ddb56d99a80c3ae36c2e2db46c082b`.
- Merge time: September 7, 2026, 07:45:15 UTC. Candidate and merged Git trees
  compare identically. No bypass, force push or source-branch deletion occurred.
- Independently confirmed rollback baseline:
  `98922aebf71d90b2b18ecc34c8b00a041fff51c7` (previous live schema 3 manifest).

Candidate Site Validation `34096530265` and locale run `34096530272` passed.
A20 independently accepted the exact candidate with limits in source evidence
commit `ce1c3bcf5c4cbf5bdcc46daac51708554b4bc0e4`. See the
[independent acceptance](a20-wave-one-gated-acceptance-2026-09-07.md) and its
linked prior browser evidence. PR60 was closed only after the exact mandatory
locale correction merged through PR62; its branch remains preserved.

## Hosted artifact and live delivery

[Pages run 34097031477](https://github.com/OKHP3/OverKill-Hill/actions/runs/34097031477)
passed validation, artifact handoff, deployment and live verification on the
merged revision. Main Site Validation `34097030873` and locale `34097031052`
also passed. A21 downloaded the actual producer artifact
`validated-site-eeb3960778ddb56d99a80c3ae36c2e2db46c082b-34097031477-1`
and independently ran the release verifier: 56 HTML pages and 371 files pass.
All 370 payload files compare byte-for-byte to the exact merged Git blobs.

Hosted manifest SHA-256:
`209b18f28632f501fd56c9f24777a67d14d4ac2507ea50bf86cc59a194e3eb69`.
This differs from the local Windows candidate manifest, as expected from the
merged revision and Linux payload representation; it is not claimed to be the
same artifact. The trusted manifest provides integrity, not a signature.
The public manifest independently reports the merged revision and schema 3.

The downloaded [live-edge report](../audit/a21-wave-one-live-edge-2026-09-07.json)
records 428 checks, zero failures, 39 blocked checks and 315 warnings. Its status
is PARTIAL. Existing direct GitHub Pages policy/header and external-service
limitations remain visible; deployment success does not establish those controls.

A21 independently ran live accessibility QA: four representative interaction
samples and all 56 public routes pass. Additional live Chromium checks confirm
real result-link focus, clean search snippets, Escape behavior, and painted
homepage headings with JavaScript disabled or the shared script blocked.
Private paths `/.git/config`, `/AGENTS.md`, `/site-src/pages.json`,
`/.local/a14/` and `/scripts/build-release.py` return 404. See the
[live browser record](../audit/a21-wave-one-live-browser-2026-09-07.json).

## Scope and remaining work

This wave includes A03/A04/A05/A07/A08/A09/A10/A17/A18, A19 decision evidence,
and the reviewed mandatory locale gate from PR60. It resolves the reproduced
visibility, search focus and parsed-snippet failures in tested environments.
No hosting strategy, analytics policy, accepted art, original manifesto,
regional noindex rule or human/native translation approval was changed.

Actual full-workflow and deploy-only retries remain NOT RUN. Successful attempt
one verifies the actual producer/consumer handoff, not retry behavior. Obsolete
PR validation cancellation was observed; all concurrency scenarios are not
therefore certified. Native macOS, actual Safari/VoiceOver, NVDA, physical phone,
human newcomer sessions and full accessibility conformance remain unverified.
A20's WebKit ordinary-link Tab qualification remains explicit. Replit runtime
and publication exposure are unresolved.

A06/A11/A12/A13-A16 content and presentation changes remain queued. A14's actual
A/B proposals were shown; owner selection remains pending. The architect's
requested concise status disclosure is a refinement for review, not an A/B
selection. Any revised English status wording needs its corresponding bounded
French review; regional source receipts must follow the final combined source.
No queued content or proposal was appended to the deployed candidate.

This evidence branch is based on the deployed revision and contains reports
plus the reviewed publishing-guide correction. It is intentionally separate
from the release and is ready for later documentation integration.
