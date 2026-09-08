# Repository Cleanup Closeout

Date: September 8, 2026

## Scope

This closeout records the safe cleanup pass for the OverKill Hill repository.
It preserves verified recovery points, identifies still-active work, and notes
the one detached checkpoint that could not be removed because Windows kept the
directory locked.

## What was preserved

- Archive ref created for the unique detached commit `37eb4c28`:
  `refs/archive/2026-09-08/a21-retry-evidence`
- The commit at `37eb4c28` is now protected before any worktree cleanup.
- The `ace6/.local/a21-evidence` material was ignored raw evidence, not tracked
  repository content. It was preserved without deletion at
  `C:/Users/jamie/OKH-Local/01_ChatGPT_Exports/2026-09-08/a21-release-evidence-preserved-1655`.
  The snapshot contains 2,779 files totaling 1,308,423,643 bytes; every source
  and copy SHA-256 matched. Its sibling manifest is
  `a21-release-evidence-preserved-1655-manifest.json`. The `ace6` source remains
  active and no deletion is authorized.

## What was cleaned up

- Detached worktree `C:/Users/jamie/.codex/worktrees/287a/overkill-hill`
  was removed after confirming it was clean and detached.

## What is still retained

- Active branch worktrees remain in place for the A08, A09, A11, A12, A13,
  A14, A15, A18, A20, and A21 lines of work.
- Local-only branches without confirmed prune authority were kept.
- Open PR 77, `codex/thread-closeout-status-doc-fix`, remains open.

## Blocked removal

- Detached worktree `C:/Users/jamie/.codex/worktrees/3d63/overkill-hill`
  could not be removed because Windows reported the path as in use by another
  process.
- The directory was verified as detached at `bd6ceacc`, but cleanup must wait
  until the handle is released.

## Current decision

- Keep: active named branches, open PR work, and preserved evidence.
- Archive: unique detached commit `37eb4c28`.
- Delete later: `3d63` detached worktree, once the Windows lock clears.
