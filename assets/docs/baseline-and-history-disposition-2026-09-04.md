# Baseline and history disposition — 2026-09-04

## Performance baseline (R34)

Measured from the isolated `codex/p3-baseline-history` worktree at commit
`e225176305a0d5cd8283cc0ad90d64f0d49d506f` on 2026-09-05 UTC (2026-09-04
America/Chicago). The local `server.py` served `http://127.0.0.1:5000` with
no-cache headers. The reusable command was:

```text
npm install --no-save --ignore-scripts playwright
npx playwright install chromium
node scripts/measure-baseline.mjs --base=http://127.0.0.1:5000
```

The temporary install was not added to the repository. The script uses one
fresh headless Chromium context per route, empty browser cache, local HTTP,
no network throttling, host-default CPU, and `networkidle`. It records browser
version, navigation duration, DOMContentLoaded, resource count, transfer bytes,
encoded bytes, resource duration, and failed requests. It does not claim field
data or INP/LCP distributions; those are unavailable.

| Representative route | Navigation ms | DOMContentLoaded ms | Transfer bytes | Resources |
|---|---:|---:|---:|---:|
| `/` | 4018 | 3547 | 5,517,877 | 27 |
| `/writings/first-diagram-is-a-liar/` | 1466 | 787 | 1,239,847 | 34 |
| `/projects/mermaid-theme-builder/` | 1798 | 375 | 359,313 | 7 |

The machine-readable evidence is [`baseline-measurement-2026-09-04.json`](../audit/baseline-measurement-2026-09-04.json).
Each route recorded one aborted Google Analytics collection request; this is
external availability behavior and is not treated as a page asset failure.

### Proposed budgets (proposal, not enforced)

For this unthrottled local reference run, use a future repeatability target of
navigation ≤5,000 ms, DOMContentLoaded ≤4,000 ms, and transfer ≤6 MiB for the
homepage. These are measurement guardrails derived from the observed values,
not CI gates and not claims about user field experience. Re-measure with a
declared device/network profile before turning any budget into a release rule.

## Historical-work disposition (R35)

Read-only inventory from the isolated worktree. No stash was applied or deleted,
and no branch or archive ref was pruned.

### Stashes

| Ref | Disposition |
|---|---|
| `stash@{0}` `archive detached worktree abc9 parity draft 2026-08-30` | preserved historical draft |
| `stash@{1}` `archive detached worktree 89eb edits 2026-08-30` | preserved historical edits |
| `stash@{2}` `codex live-edge report after parser verification 2026-08-23` | preserved report evidence |
| `stash@{3}` `codex live-edge verification report 2026-08-23` | preserved report evidence |
| `stash@{4}` `codex responsive QA results 2026-08-23` | preserved QA evidence |
| `stash@{5}` `codex validation outputs 2026-08-23` | preserved validation evidence |

### Archive refs and active worktrees

The archive namespace contains dated pre-repair, pre-merge, merged-PR, and
mirror-junitor refs. Examples verified by exact SHA include
`refs/archive/2026-08-22/pre-repair-344e046d` → `344e046d7ba1e95be2f8d01907d18129240024d`,
`refs/archive/2026-08-28/overkill-hill-recover-local-01ba2a0b` →
`01ba2a0b10240a7aa51dbf0c697feb9e9750de99`, and
`refs/archive/2026-08-31/pre-merge-932ffc2` →
`932ffc2032095e7633e424cd8d76bed3a7641ca0`. They remain preserved historical
anchors. `main` and `origin/main` both point to `e225176305a0d5cd8283cc0ad90d64f0d49d506f`.

Existing worktrees include the checked-out `main`, detached evidence worktrees
at `0822`, `45cd`, `6068`, `8492`, and `d079`, active branches
`codex/release-artifact-boundary` at `292d8f9`, `codex/p3-copy-seo`,
`codex/p3-dependencies`, and this worktree. These are owned or active surfaces;
they were not modified.

### Boundary

This change records evidence and disposition only. It does not pop or delete
stashes, rewrite history, prune refs, redesign runtime behavior, enforce budgets,
or address the separate Mermaid P1.
