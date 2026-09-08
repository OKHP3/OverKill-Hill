# Complementary translation and analytics task dispatch

September 7, 2026. All seven task creations were accepted, and actual task IDs, isolated worktrees, and named branches were verified from local task records and Git. The native task listing had not yet indexed the new records at verification time.

These tasks supplement the nineteen A03-A21 tasks in [the main dispatch](website-remediation-dispatch-2026-09-07.md). They do not duplicate that queue. The shared baseline is `98922aebf71d90b2b18ecc34c8b00a041fff51c7`, which includes the September 7 assessment and A01/A02 repairs. Old audit assertions must be reproduced against current source before changing it.

Each implementation worker prepares a bounded local commit first. A21 assigns subsequent draft-PR publication and integration slots; workers must coordinate before pushing or opening a PR. No worker may merge, deploy, force-push, alter the shared checkout, or change sibling repositories. A21 is the sole integration manager: `01a07aaf-76a3-7d20-a26a-c29851127599`, in `/Users/okh/.codex/worktrees/6b42/OverKill-Hill`. It resolves overlapping files and reconciles generated outputs. Separate PRs are proposals for integration, not independent release paths.

T05 and W13 are documentation-only decision packages. They must not invent owner approval, alter locale publication states, introduce a consent UI, or change account/hosting settings. Creating any task does not establish that its finding is fixed or that a PR already exists.

| Item | Scope | Thread ID | Worktree | Branch |
| --- | --- | --- | --- | --- |
| T01 | Translation freshness in the Pages dependency | `01a07ab1-2cd9-7fe3-bcd8-f23eb9969bbb` | `/Users/okh/.codex/worktrees/ae66/OverKill-Hill` | `codex/t01-i18n-release-dependency` |
| T02 | Reviewed-target integrity and adoption | `01a07ab1-72fc-7602-b219-8811ce7ef253` | `/Users/okh/.codex/worktrees/0aac/OverKill-Hill` | `codex/t02-reviewed-target-integrity` |
| T03 | Translation skill test discovery | `01a07ab1-776b-7eb1-aa93-68d7fc00c4a8` | `/Users/okh/.codex/worktrees/a3a9/OverKill-Hill` | `codex/t03-translation-test-discovery` |
| T04 | Translation operating instructions | `01a07ab1-726e-7d52-9859-7eca97e51215` | `/Users/okh/.codex/worktrees/1378/OverKill-Hill` | `codex/t04-translation-operating-docs` |
| T05 | Unified locale policy proposal | `01a07ab1-7303-7330-b36a-a8742d522cfa` | `/Users/okh/.codex/worktrees/b21e/OverKill-Hill` | `codex/t05-locale-policy-proposal` |
| T06 | Regional generator cleanup | `01a07ab1-726e-7d52-9859-7ee1afdf7abd` | `/Users/okh/.codex/worktrees/354d/OverKill-Hill` | `codex/t06-protected-locale-generator` |
| W13 | Analytics policy and disclosure review | `01a07ab1-726e-7d52-9859-7f0a65c98dad` | `/Users/okh/.codex/worktrees/f49a/OverKill-Hill` | `codex/w13-analytics-decision` |

## Ownership and dependencies

- T01 owns the narrow live locale-check workflow addition. A07/A17 own artifact and concurrency changes; A08 owns runtime choices. A21 reconciles their workflow hunks.
- T02 owns executable reviewed-target integrity and adoption semantics with focused negative tests. Existing reviews and translation bytes must not be altered just to make a gate pass.
- T03 preserves all package tests, fixes Python discovery, and uses its own narrow skill-test workflow. Active hyphenated planner/validator names remain stable.
- T04 owns the locale operating guide, relevant script inventory rows, and page-sync command/help prose. It documents verified interfaces and coordinates changes pending from T02.
- T05 maps current policy into a versioned proposal; A13 owns French interaction review and T02 owns enforcement. It preserves the intentional differences between released French and draft alternate clusters.
- T06 owns regional generation and protected-content regressions. It preserves current MurderBird sources, PNG fallbacks, hash pointers, reviewed es-MX inputs, and historical evidence.
- W13 owns analytics data-flow/disclosure/owner-policy evidence. A16 owns measured performance economics. No silent reversal of a prior owner privacy/UI decision.

The workers must report exact changed files, source revision, branch/commit/PR, executed validation and test counts, remaining limits, and integration requirements. Full changes and owner-dependent decisions remain open until reviewed against those acceptance criteria.
