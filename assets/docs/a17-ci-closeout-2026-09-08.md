# A17 CI concurrency closeout

Status: CLOSED AS DOCUMENTED, NOT FULLY ACCEPTED IN THIS CHECKOUT.
Date: September 8, 2026.

This closeout records the A17 concurrency and status-reporting work as it now
stands after A21's later release integration and wave-one release closeout.
It does not invent new hosted rerun evidence. The remaining acceptance items
for actual full/deploy-only retry behavior still require direct A21-owned
verification if the program wants them recorded as complete.

## What is now confirmed

- A17's source scope is the workflow concurrency and status-reporting patch
  recorded in [`a17-ci-status-2026-09-07.md`](a17-ci-status-2026-09-07.md).
- The integrated A21 ledger records A17 as integrated at `0714a2d4` and
  preserves the source-review outcome: nine reporter tests and seven
  expression tests passed, and one workflow conflict was resolved by keeping
  both A07 output and A17 job concurrency.
- The wave-one release closeout records the deployed revision
  `eeb3960778ddb56d99a80c3ae36c2e2db46c082b`, the live Pages run
  `34097031477`, and the live-edge report
  [`a21-wave-one-live-edge-2026-09-07.json`](../audit/a21-wave-one-live-edge-2026-09-07.json)
  with `428` checks, `0` failures, `39` blocked checks, and `315` warnings.
- The same closeout records the live browser evidence in
  [`a21-wave-one-live-browser-2026-09-07.json`](../audit/a21-wave-one-live-browser-2026-09-07.json)
  and confirms the producer artifact
  `validated-site-eeb3960778ddb56d99a80c3ae36c2e2db46c082b-34097031477-1`.
- A21 started two independent hosted validations against the verified
  live SHA `f4a353c323fc1caa848e03f6f0aa1ea1e520210c`: Pages rerun
  `34224582972` (attempt 2) and manual validation dispatch `34231410815`
  (attempt 1). Their validation jobs overlapped without cancellation. The
  manual dispatch completed successfully; its validation job was
  `102078207337`, with the edge and third-party monitors also successful and
  artifacts `10057934729` and `10057999763`. The Pages rerun also completed
  successfully: validation job `102078124098` and deployment job
  `102079922030` both passed, including exact artifact identity, provenance,
  deployment, and live-edge verification.

## What remains explicitly open

- Actual full-workflow and deploy-only rerun evidence remains unclaimed in the
  wave-one closeout.
- At this closeout revision, the overlapping validations and full Pages retry
  are successful. No deployment-only attempt has started yet, so producer-
  artifact reuse under an isolated deployment-only retry remains open.
- The A17 status report correctly describes that local tests pass, but GitHub
  scheduling acceptance is still bounded by hosted rerun evidence, not local
  fixtures.
- Any future claim that A17 is fully accepted should point to a concrete run
  ID, attempt number, artifact identity, and summary evidence from the A21
  release-integrator record.

## Closeout summary

A17 is now integrated and documented against the later wave-one release
evidence, but the final hosted retry acceptance is still a separate A21-owned
step. This file exists so the repository has a stable closeout record without
conflating local concurrency tests with hosted scheduler behavior.
