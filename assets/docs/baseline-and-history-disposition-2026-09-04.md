# Baseline and history disposition, 2026-09-04

## R34 initial lab baseline

Measured at commit `e225176305a0d5cd8283cc0ad90d64f0d49d506f` using Chromium 153.0.8010.12, headless, viewport 1280x720, three fresh contexts per route, empty cache, local no-cache server, no throttling, and host-default CPU. `networkIdleNavigationMs` includes the network-idle wait. Transfer and encoded bytes are observed top-document resource-timing subtotals only. They exclude navigation payloads and opaque cross-origin or iframe bytes, so they are not total page payload.

| Route | Network-idle navigation median (range) | DOMContentLoaded median | Transfer subtotal median |
|---|---:|---:|---:|
| `/` | 971 ms (903–1076) | 255 ms | 5,517,877 bytes |
| `/writings/first-diagram-is-a-liar/` | 1382 ms (1215–1631) | 482 ms | 1,239,847 bytes |
| `/projects/mermaid-theme-builder/` | 1372 ms (1210–1890) | 242 ms | 359,313 bytes |

Evidence: [`baseline-measurement-2026-09-04.json`](../audit/baseline-measurement-2026-09-04.json). Failed request reports strip query strings. The Google Analytics request was aborted with unknown cause. Field data is unavailable; no INP or LCP distributions are claimed. This is an initial lab baseline only.

Proposed future repeatability budgets, not enforced: homepage network-idle navigation <= 5,000 ms, DOMContentLoaded <= 4,000 ms, observed resource timing subtotal <= 6 MiB. Re-measure on a declared device and network profile before any release rule.

## R35 history disposition

All six stashes are preserved by immutable commit ID: `d1d85689d1fe8499f94b3dbdad6040f4ef77920d` (abc9 parity draft), `ea250c89e7f6024ad7d9ebeea397a121be253798` (89eb edits), `f8829e694c86b773e576dbe5a674e28d6d66cfbc` (live-edge report after parser verification), `b157e48b970d6d6c9953ef92cb9a2251c5d99a8c` (live-edge verification), `6ec5f6eaccb62bd3597b90331ed594dc631f145f` (responsive QA), and `1399026e4dffe91cf36231b2c1a37b3a6c99c70f` (validation outputs).

Complete archive inventory was captured with `git for-each-ref refs/archive`, including every ref name, SHA, and subject. All dated pre-repair, pre-merge, merged-PR, and mirror-junitor refs remain preserved. `main` and `origin/main` point to `e225176305a0d5cd8283cc0ad90d64f0d49d506f`.

Detached worktrees `0822`, `6068`, `7433`, `8492`, and `d079` are historical evidence snapshots. Other-owned active worktrees include `45cd` (`codex/r05-r06-r07`), `6d60` (`codex/release-artifact-boundary`), `p3-copy-seo`, and `p3-dependencies`; none were modified. The retired `_replit` Mermaid Theme Builder preview remains a standalone prototype boundary and is excluded from production routes.

No stash was popped or deleted, and no branch or archive ref was pruned.
