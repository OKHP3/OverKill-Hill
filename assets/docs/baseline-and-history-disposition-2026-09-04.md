# Baseline and history disposition, 2026-09-04

## R34 initial lab baseline

Measured at `2026-09-05T05:03:35.065Z` from the `codex/p3-baseline-history` worktree at commit `5bc775a475b9d9950de0fa5c6ebdc2ddb4e648d2`. The measurement harness and server were uncommitted at measurement time; the evidence records their status and the harness SHA-256. The final server retains its prior `0.0.0.0` default, while the reproduce command explicitly binds `127.0.0.1`, matching the measured loopback behavior. This is therefore a reproducible working-tree measurement, not a claim that these changes were present in that commit.

The local source was served only from this worktree on `http://127.0.0.1:5051`. For every route and all three samples, Playwright hashed the received top document and matched it to the corresponding local HTML SHA-256. Node was `v24.11.1`; npm was `11.6.2`; Playwright was `1.63.0`; Chromium was `153.0.8010.12`, headless, viewport 1280x720. Each sample used a fresh browser context with an empty cache; network was local HTTP with no throttling and CPU was host-default with no emulation.

| Route | Network-idle navigation median (range) | DOMContentLoaded median | Transfer subtotal median |
|---|---:|---:|---:|
| `/` | 1482 ms (1120-1495) | 495 ms | 5,517,877 bytes |
| `/writings/first-diagram-is-a-liar/` | 1477 ms (1360-1980) | 638 ms | 1,239,847 bytes |
| `/projects/mermaid-theme-builder/` | 1810 ms (1663-1866) | 448 ms | 359,313 bytes |

Evidence: [`baseline-measurement-2026-09-05.json`](../audit/baseline-measurement-2026-09-05.json). Reproduce from this exact worktree:

```powershell
npm ci
npx playwright install chromium
$env:HOST = '127.0.0.1'; $env:PORT = '5051'; py -3 server.py
# In a second PowerShell at the same worktree root:
node scripts/measure-baseline.mjs --base=http://127.0.0.1:5051 --output=assets/audit/baseline-measurement-2026-09-05.json
```

`networkIdleNavigationMs` includes Playwright's `networkidle` wait and is not a Core Web Vital. Transfer and encoded-byte values are Resource Timing subtotals: they exclude navigation payloads and may omit opaque cross-origin or iframe bytes, so they are not total page payload. Failed request reports strip query strings. Field data is unavailable; no INP or LCP distributions are claimed. This is an initial lab baseline only.

## R34 deterministic asset-budget guard

The CI guard at `scripts/check-performance-budget.py` enforces first-party static release asset budgets for the same three representative routes. It counts each HTML document, selected local assets discovered from it, and local CSS `url()` dependencies. It deliberately excludes external resources, embedded iframe contents, dynamic requests, compression, cache behavior, and timing. It is an asset-weight guard, not a Core Web Vitals or full page-payload claim.

Measured source weights at commit `276e0164c4a8e24cfaf42bd8eeeaf4589bb4d325`, before setting budgets:

| Route | Measured local release bytes | Enforced budget | Headroom |
|---|---:|---:|---:|
| `/` | 4,859,909 | 5,767,168 (5.5 MiB) | 907,259 bytes (18.7%) |
| `/writings/first-diagram-is-a-liar/` | 3,536,399 | 4,194,304 (4 MiB) | 657,905 bytes (18.6%) |
| `/projects/mermaid-theme-builder/` | 526,278 | 655,360 (640 KiB) | 129,082 bytes (24.5%) |

The configured budgets are rounded binary units and retain at least 15% room above the measured first-party source footprint. Run `py -3 scripts/check-performance-budget.py --json` to reproduce the report. The regression test proves that a CSS-only dependency is counted, a missing selected asset fails, and an undersized budget fails.

The previous proposed local network-idle and DOMContentLoaded values remain non-enforced. They require a declared device and network profile before they can support a repeatable lab rule.

## R35 history disposition

The immutable archive inventory captured at `2026-09-05T05:03:35Z` is retained in [`archive-inventory-2026-09-05.md`](archive-inventory-2026-09-05.md). It records every `refs/archive` name and object SHA with a disposition; no archive ref was changed.

All six current stash objects were resolved and verified by immutable commit ID: `d1d85689d1fe8499f94b3dbdad6040f4ef77920d`, `ea250c89e7f6024ad7d9ebeea397a121be253798`, `f8829e694c86b773e576dbe5a674e28d6d66cfbc`, `b157e48b970d6d6c9953ef92cb9a2251c5d99a8c`, `6ec5f6eaccb62bd3597b90331ed594dc631f145f`, and `1399026e4dffe91cf36231b2c1a37b3a6c99c70f`.

Detached worktrees are not classified as historical solely because they are detached. Their owner and purpose are unknown unless separately evidenced; preserve them. Branch worktrees `45cd`, `6d60`, `p3-copy-seo`, and `p3-dependencies` are likewise owner-controlled/unknown and were not modified.

`_replit/` is absent from this current worktree. Historical documents describe a retired Mermaid Theme Builder preview there, but it is not an existing prototype or production route in this tree. No stash was popped or deleted, and no branch or archive ref was pruned.
