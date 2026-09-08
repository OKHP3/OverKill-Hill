# A20 task closeout status

**NOT fully complete.** The scoped automated acceptance work and original evidence are preserved in GitHub. Full human/device acceptance remains open. No unconditional archive recommendation is made.

## Completed and preserved

[PR65](https://github.com/OKHP3/OverKill-Hill/pull/65) is merged at `f4a353c323fc1caa848e03f6f0aa1ea1e520210c`. The six original A20 branches were pushed normally and remote hashes verified: accessibility-acceptance `fb0aadda`, wave-one-acceptance `daa3ebd8`, wave-one-rebound `2d00450d`, wave-one-gated `ce1c3bcf`, content-acceptance `99d89786`, content-rebound `2471c014`, each prefixed `codex/a20-`. No force push, deletion, or unrelated worktree edits occurred.

The integrator's published evidence is preserved on `codex/a21-content-release-evidence` at `6c642fc164ca1b1e959533a65ef35b2f9015536d`. This records successful first-attempt hosted deployment and exact producer-artifact checks. A new independent A20 live check confirms manifest revision `f4a353` and 368 payload paths exactly matching raw Git blobs. Three direct requests return 404: `.nojekyll`, `.well-known/discord`, `.well-known/security.txt`. The deployment-only marker is distinct from the two intended public endpoints. See [live inventory evidence](../audit/a20-live-closeout-2026-09-08.json). One transient local Git-read error was retried successfully and retained in the initial-failure record.

A smallest-available-model subagent (gpt-5.6-luna, low effort) independently reconciled obligations and then completed [24 passing viewport/font samples](a20-closeout-visual-2026-09-08.md). These do not establish actual browser zoom or visual font quality.

## Remaining actions and needed evidence

| Action | Dependency or next step |
| --- | --- |
| Actual Safari/VoiceOver and Windows NVDA acceptance, including spoken/human task outcomes | A tester with these environments must record OS/browser/AT versions, exact release, the five prior visitor tasks, outcomes, and relevant recordings or logs. Automated browser results cannot substitute. |
| Physical phone/touch and native macOS acceptance | Test scoped routes, scrolling, tap targets, orientation, overflow, and link traversal on actual devices. Resolve the isolated Windows WebKit Tab limitation with native Safari evidence. |
| Actual 200%/400% zoom and human font/layout judgment | Run real browser zoom; the 24 new CSS viewport samples close only bounded automated reflow/font-loading coverage. |
| Fresh performance measurements | Record repeatable environment and trials. Previous optimization and integrator suites are not independent field-performance evidence. |
| Two missing public `.well-known` endpoints | Integration must triage packaging/hosting and restore them or explicitly document an accepted exclusion. The A20 acceptance task has not changed deployment code. Attempts to deliver this finding to A21 through the task messaging tool failed twice with `Cannot steer conversation ... without an active turn id`; this committed record is the durable handoff. |
| Deployment retry completion | Pages run `34224582972`, attempt 2, completed successfully during closeout; latest attempt 3 is now in progress. Separate Site Validation run `34231410815` passed. Completed attempts do not certify the pending retry. |
| Qualified French/native review if full locale acceptance is required | Supply qualified human review and explicit acceptance. French remains AI-reviewed; regional pages remain drafts/noindex/unaccepted. Those boundaries must remain until accepted. |

No credentials are needed for the completed work. The missing inputs are human/device access, recorded acceptance outcomes, and the integrator's hosted resolution. An explicit owner decision can narrow or transfer remaining scope; this record does not infer such a decision.

## Limits that are not new implementation blockers

The historical fallback-only English/French whole-text equality failure was explicitly adjudicated as superseded by authorized content changes; it is not relabeled PASS. Art, alt/title, decoded RGBA, and protected narrative checks remain preserved. Optional A14 presentation, A15 proposals, skipped future FoundRy parity/redirect diagnostics, Replit runtime certification, and general host/header/external-service limitations remain outside scoped A20 acceptance. They must not be silently represented as completed features or tests. No exhaustive rerun of every integrator suite is claimed.

Archive only after the remaining acceptance work is completed, or after an explicit owner decision to accept the limits and transfer the named open work to a durable owner/task.
