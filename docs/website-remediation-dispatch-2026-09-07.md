# Website remediation dispatch

> Historical dispatch snapshot. IDs and original scopes remain useful; worktree,
> branch, and completion states must be checked against current GitHub and
> [the closeout ledger](../assets/docs/thread-closeout-status-2026-09-08.md).

September 7, 2026. Architect thread: `01a07a50-71fc-7543-9c4b-55a51d91b663`.

The owner requested one separate task/worktree per unresolved package. Nineteen task creations were accepted for A03 through A21, and nineteen new worktrees were observed at `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. This commit now includes the assessment and A01/A02 repairs, superseding the assessment's historical uncommitted status. Production state has not been reverified in this dispatch.

A21 is the integration PM; A03-A20 are individual workers or reviewers. All are instructed to preserve the owner checkout and siblings, implement bounded work, create local branch commits, and report tests and limitations. No package is marked fixed merely because its task was created. No branch publication, main merge or deployment is delegated by this dispatch. Broad presentation and hosting changes require concrete alternatives first.

Use the [advancement plan](../assets/docs/website-advancement-plan-2026-09-07.md) for package scope, dependencies and acceptance. A21 serializes shared runtime and workflow integration, regenerates combined outputs, and supplies a frozen candidate to A20. Workers must not duplicate each other's tasks. The PM keeps its ongoing status in its own worktree at `docs/website-remediation-status-2026-09-07.md`.

## Task inventory

All 19 task IDs and worktree paths below were verified from local task records after native task listing lagged setup. Branch names are a dispatch-time snapshot; a pending name does not mean the task lacks an isolated worktree.

| Package | Task | Thread ID | Worktree | Branch |
| --- | --- | --- | --- | --- |
| A03 | A03 Restore content when scripts fail | `01a07aaf-0dfd-7e83-911b-710fe5f1ef0c` | `/Users/okh/.codex/worktrees/3d31/OverKill-Hill` | `codex/a03-fail-open-reveal` |
| A04 | A04 Fix accessible search and excerpts | `01a07aaf-0e5b-7a32-9aa2-19994121f75f` | `/Users/okh/.codex/worktrees/21ea/OverKill-Hill` | Naming in progress |
| A05 | A05 Make Skillz installation reproducible | `01a07aaf-0dfd-7e83-911b-70ec8de457e1` | `/Users/okh/.codex/worktrees/a529/OverKill-Hill` | `codex/a05-skillz-install` |
| A06 | A06 Correct project claims and concept labels | `01a07aaf-0dfd-7e83-911b-70cbac70080a` | `/Users/okh/.codex/worktrees/862f/OverKill-Hill` | `codex/a06-content-truth` |
| A07 | A07 Fix release retries and freshness gates | `01a07aaf-0e55-7e51-9720-3a8e5ad36deb` | `/Users/okh/.codex/worktrees/a694/OverKill-Hill` | `codex/a07-release-retry-freshness` |
| A08 | A08 Update the supported QA runtime | `01a07aaf-5674-7bc3-b036-6968cb60db9b` | `/Users/okh/.codex/worktrees/4bf9/OverKill-Hill` | `codex/a08-supported-qa-runtime` |
| A09 | A09 Fix macOS review fixture portability | `01a07aaf-58b6-7fb1-b286-2876960fdba5` | `/Users/okh/.codex/worktrees/3bf5/OverKill-Hill` | `codex/a09-review-fixture-portability` |
| A10 | A10 Cover all released pages in browser QA | `01a07aaf-5ba9-7d53-940f-84bfb3b54667` | `/Users/okh/.codex/worktrees/9108/OverKill-Hill` | `codex/remediation-a10` |
| A11 | A11 Unify project maturity and evidence | `01a07aaf-5ba9-7d53-940f-8490678d2bcd` | `/Users/okh/.codex/worktrees/177d/OverKill-Hill` | `codex/remediation-a11-status-registry` |
| A12 | A12 Correct featured writing and metadata | `01a07aaf-5bfc-7a40-a63b-5214a7bbc8e7` | `/Users/okh/.codex/worktrees/e388/OverKill-Hill` | Naming in progress |
| A13 | A13 Complete French interaction labels | `01a07aaf-5d32-7d93-a007-600994bdcd21` | `/Users/okh/.codex/worktrees/a503/OverKill-Hill` | Naming in progress |
| A14 | A14 Improve phone hierarchy and spacing | `01a07aaf-5f84-7e00-8322-2de95f2e05fd` | `/Users/okh/.codex/worktrees/a1a8/OverKill-Hill` | `codex/a14-phone-proposals` |
| A15 | A15 Improve reading and contact journeys | `01a07aaf-662f-7321-a2df-5fc96ec56fae` | `/Users/okh/.codex/worktrees/6a75/OverKill-Hill` | `codex/a15-reader-orientation` |
| A16 | A16 Measure and improve transfer costs | `01a07aaf-6a21-74b1-a0dc-3b88375b1212` | `/Users/okh/.codex/worktrees/d191/OverKill-Hill` | `codex/a16-measured-economics` |
| A17 | A17 Repair CI concurrency and status reporting | `01a07aaf-6e61-7733-8687-d917fb7d81d5` | `/Users/okh/.codex/worktrees/46df/OverKill-Hill` | Naming in progress |
| A18 | A18 Harden preview serving and publication | `01a07aaf-7155-7460-a693-eb4f4cb66f87` | `/Users/okh/.codex/worktrees/b3e3/OverKill-Hill` | `codex/a18-preview-exposure` |
| A19 | A19 Evaluate response-header hosting options | `01a07aaf-73f5-7830-a79b-c84f52a17f9f` | `/Users/okh/.codex/worktrees/a8c6/OverKill-Hill` | `codex/a19-header-host-strategy` |
| A20 | A20 Independently verify visitor accessibility | `01a07aaf-7618-7fa1-8a56-226f7cc702a3` | `/Users/okh/.codex/worktrees/0a49/OverKill-Hill` | `codex/a20-independent-acceptance` |
| A21 | A21 Manage integration and release readiness | `01a07aaf-76a3-7d20-a26a-c29851127599` | `/Users/okh/.codex/worktrees/6b42/OverKill-Hill` | Naming in progress |

## Complementary queue

The concurrent Architect task `01a074b4-a15a-74e2-8b14-55bf53d0bc49` confirmed seven additional running tasks for T01-T06 translation findings and W13 analytics/privacy policy. Their verified IDs, worktrees and scopes are in the [translation and analytics dispatch](translation-analytics-task-dispatch-2026-09-07.md), and have been sent to A21. There are 26 distinct tasks across the two registries, including the integration PM. T01 coordinates workflow edits with A07/A08/A10/A17; T04 follows T02 interfaces; T05 aligns with A13/T02; W13 uses A16 measurement evidence. All prepare local branch commits first. A21 remains the sole integration authority.
