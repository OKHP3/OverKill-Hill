# A21 hosted retry execution

September 8, 2026: the previously NOT RUN full and deployment-only retry cases are now observed PASS on current main/live revision `f4a353c323fc1caa848e03f6f0aa1ea1e520210c`. This execution record supplements the dated release closeout; A17 report review/integration remains separate.

User authorization was relayed by A17 to A21, the sole release integrator. Main and the live manifest matched before execution; main was rechecked before the deployment-only retry. No older revision, source change, concurrency setting change or duplicate deployment sequence was introduced.

## Actual executions

[Pages run 34224582972](https://github.com/OKHP3/OverKill-Hill/actions/runs/34224582972) full attempt 2 passed validation, deployment and live checks. It created validation artifact `validated-site-f4a353c323fc1caa848e03f6f0aa1ea1e520210c-34224582972-2`, artifact ID `10058127991`, and Pages artifact `github-pages-34224582972-2`.

A21 then reran only deployment job `102079922030`. Attempt 3 passed. Its actual required-output and download steps use the same attempt 2 validation artifact and ID; upload/deploy use the new `github-pages-34224582972-3`. The consumer did not infer a validation artifact from its own attempt 3. Both deployments logged successful SHA-bound verification of 56 HTML pages and 372 files. The public manifest still reports the same full release SHA after attempt 3.

Standalone [validation dispatch 34231410815](https://github.com/OKHP3/OverKill-Hill/actions/runs/34231410815) passed on the same revision while full attempt 2 validation was running. API job timestamps confirm overlapping intervals for jobs `102078124098` and `102078207337`; both succeeded without cancellation. This is observed push-triggered reusable validation overlapping manual standalone validation, not only an expression fixture.

## Summary and retained evidence

The actual attempt 3 summary separates content delivery PASS (74 checks), edge policy PARTIAL (354 checks), and external availability NOT RUN with a pointer to the separate runtime report. It displays the correct expected release SHA and matching release-manifest evidence. Both downloaded retry live-edge reports contain 428 checks, zero failures, 39 blocked checks and 315 warnings.

[Machine execution record](../audit/a21-hosted-retry-execution-2026-09-08.json) retains final job identities/times, independently checked overlap, selected actual log lines, raw-log hashes and both edge counts. Raw attempt logs, initial overlap API snapshots, final job API responses and complete attempt 2/3 live-edge reports remain in this integrator checkout under `.local/a21-evidence/a17-retries/`; preserve them before any checkout retirement. Hosted artifacts remain subject to GitHub retention.

No deploy-queue contention, FIFO ordering, newest-SHA enforcement, old-revision redeployment, or universal scheduler coverage is claimed. The existing deployment concurrency policy remains unchanged. PARTIAL is not security PASS. Human/native, Replit, physical-device and assistive-technology limitations are unaffected. A17 must review these observations and integrate its final acceptance report before being declared fully complete.

Supersession note: This retry execution report remains historical and bounded. PR76 (A14 implementation) and PR68 (retry closeout) now carry forward this context with subsequent deployment and retry scope.
