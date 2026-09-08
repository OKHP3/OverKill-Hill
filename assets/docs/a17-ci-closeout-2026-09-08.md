# A17 CI concurrency closeout

Status: ACCEPTED WITH BOUNDED HOSTED EVIDENCE.
Date: September 8, 2026.

This closeout records the A17 concurrency and status-reporting work as it now
stands after A21's later release integration and wave-one release closeout.
The hosted evidence was executed by A21 and independently checked against its
retained job, overlap, deployment, and live-edge records. This closeout does
not claim queue contention, FIFO behavior, or an old-revision retry that was
not tested.

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
- The deployment-only retry was Pages run `34224582972`, attempt `3`, with
  deployment job `102080399785`. It downloaded the producer artifact
  `validated-site-f4a353c323fc1caa848e03f6f0aa1ea1e520210c-34224582972-2`
  (artifact `10058127991`), verified the SHA-bound release bytes, uploaded
  `github-pages-34224582972-3`, deployed successfully, and verified the live
  SHA remained `f4a353c323fc1caa848e03f6f0aa1ea1e520210c`.
- The retained summaries classify content delivery as `PASS` with `74`
  sampled checks, edge policy as `PARTIAL` with `354` checks, and external
  availability as `NOT RUN`. These are bounded evidence states, not a claim
  that every hosting policy is enforced at the GitHub Pages edge.

## Bounded Limitations

- No deploy-queue contention or FIFO/newest-SHA guarantee was claimed.
- No old-revision retry was executed.
- Edge policy remains `PARTIAL`, and third-party availability remains `NOT RUN`
  in the retained summaries.

## Closeout summary

A17 is integrated and accepted for the tested hosted behaviors: overlapping
validation, successful full Pages release, and deployment-only reuse of the
exact producer artifact. The explicit limitations above keep that acceptance
from being generalized into untested scheduler or hosting guarantees.
