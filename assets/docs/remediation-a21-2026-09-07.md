# A21 Mac integration handoff

Updated September 8, 2026. Status: superseded candidate, preservation and coordinated closeout. Full program completion is not established.

Initial baseline was `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. The local integration reached clean `a210ff2fde1e884f1c1c13321f7b9413ec8804ff`. In parallel, alternate reviewed implementations reached GitHub main through PR62 and PR65. Main was independently verified at `f4a353c323fc1caa848e03f6f0aa1ea1e520210c`. Do not merge this old branch wholesale or overwrite the newer generated site.

The [reconciled PM ledger](../../docs/website-remediation-status-2026-09-07.md) distinguishes current main work, unique local proposals, active closeout delegates, open PR66-68 and manual/owner dependencies. The initial release/edge tests passed nine each; after A07/A09 integration, twelve release tests, three review-boundary cases and 36-page HTML freshness passed. Later combined source changes were not regenerated or fully validated before the integration was superseded. No release artifact was frozen or deployed by this Mac task.

Preserve this task on a labeled remote branch. Current-main ports belong to the existing closeout coordinator and delegates named in the ledger. No independent duplicate PR, main merge, worktree cleanup, sibling edit or deployment should follow from this historical branch. Source changes already on current main may differ legitimately from these earlier implementations.
