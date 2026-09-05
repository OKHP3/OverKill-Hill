# Three-site infrastructure implementation status

Evidence date: September 5, 2026. Scope: the August 29 infrastructure
comparison, its applicable repairs, publication, and safe Git cleanup.
This record supersedes the historical audit's current-state claims.

## Shared foundation verified on GitHub and live

All three remote main branches contain identical shared files, implementing
`docs/adr/0001-shared-runtime-compatibility.md`. Brand behavior uses existing
DOM hooks and separate site extensions. All nine live requests returned 200.

| File | Git blob in all three repositories | Live SHA-256 in all three sites |
| --- | --- | --- |
| `assets/css/theme.css` | `dcab6c7e2e35c028949a22dbc2c70104d802fd1c` | `b60e5d8337d73b196f394bb861f3b4e509d29d7abd81d6f42bd69056ed42f11d` |
| `assets/js/app.js` | `5ddad63558afe6c5299313238204d09712aaf294` | `33c354b0b21eea42bfb5b855869d3808f54fe2272e4c0b4a3d0fbe46f73c9023` |
| `assets/js/mermaid-init.js` | `420effa94deb78302090e3369e45c1bc8d315dea` | `d0b6657726e69353ddb98fc19d4ae65763fd1fdd6b9887f7858729de85663dad` |

Baseline revisions: OverKill Hill `0ee6bc875a183ca2e065448d01fe97da62fc1ff7`,
Glee `f5689fe4852b72e5d584db9d8f87cac9121b87c4`, AskJamie
`e800d4aebf0dc2543c5ced295ec78d10ba192473`.

## Earlier findings reconciled with current source

| Finding | Disposition |
| --- | --- |
| Divergent shared CSS and JavaScript | Implemented and live, verified above. |
| Mermaid security divergence | Shared strict-default initializer with explicit curated loose opt-ins. |
| Theme branch mismatch | Shared runtime now handles both branded sites; palettes remain scoped. |
| Search payload dialects | Runtime accepts supported entries/pages payloads; generators retain site indexing rules. |
| Missing navigation aria-label | Absence alone was a false positive: AskJamie supplies screen-reader text. |
| OverKill deployment cancellation | Separate Pages workflow deploys a validated SHA-bound artifact with serialized deployment. |
| AskJamie deploy concurrency | Already serialized before the original audit. |
| Missing OverKill Replit contrast command | Current assets/scripts/check-contrast.py exists and the configured command resolves. |
| Portfolio script assumes showcase route | Script is archived and reference-only. No new public route is needed. |
| Script accumulation | Active/reference/retired inventories and archive boundaries now exist. |
| AskJamie audit portability | Already implemented on current main with UTF-8, external report paths, and nonzero findings. |
| OverKill and Glee audit portability | Implemented, regression-tested, and merged in OverKill #15 and Glee #20. |
| Hook line endings | OverKill enforces LF; Glee and AskJamie durable attributes included in closeout repairs. |
| AskJamie manifest root scope | Explicit root start_url/scope included in closeout repair. |
| AskJamie defer and asset fingerprints | Implemented in #11: 27 canonical pages and nine templates, normalized-content hashes, ordered deferred app loading, fingerprinted brand import, and read-only CI freshness gate. Shared runtime bytes unchanged. |
| AskJamie analytics CSP | Post-merge browser checks exposed intermittently emitted Google Tag Manager image beacons. #12 adds only the already-configured Google host to img-src, regenerates policies, and adds a regression. No broad HTTPS wildcard or suppressed browser errors. |
| Missing post-merge validation gates | OverKill #15 adds links and audit; Glee #21 adds CSP, structure, and links. Both have failure-propagation regression tests. |
| Glee search dark-mode coverage | Current checker passes all 16 light-surface rules, including both required dark-mode forms. |
| Glee skip-link lint mismatch | Current responsive checker accepts both skip-link and skip-to-content. |
| Glee advisory audit exit code | Explicit current release policy: 38 findings remain advisory, separate from blocking structural/link/browser gates. Not falsely reported as a zero-finding audit. |
| Historical invalid checkpoint refs and stray fonts | Current inspected checkpoint refs resolve to valid Git tree objects; no push errors reproduced. Ask main has no untracked font leftovers. No deletion needed. |
| HTTPS enforcement | Enabled for AskJamie September 5; API confirms true and HTTP redirects 301 to HTTPS. All three now enforce HTTPS. |
| Root filenames and favicon differences | Tracked Git casing and resolved asset paths govern; no blanket renaming or icon-count parity required. |
| Analytics, crawler and offline differences | Preserve current accepted site policies; do not restore superseded August assumptions. |

## External and hosting limits

Source CSP and `_headers` are not proof of delivered response headers.
Sampled GitHub Pages responses lack the full source header set. Arbitrary edge
header delivery requires an additional hosting capability, not a repository-only
patch. Browser CSP meta evidence remains distinct from response-header evidence.

AskJamie [GPT availability run 33961264162](https://github.com/OKHP3/AskJamie/actions/runs/33961264162)
reported HTTP 404 for BRG02 Starbucks, BRG05 Costco, BRG07 LVMH, and BRG09
Coca-Cola. Destination publication needs investigation. Monitoring must retain
these failures. The independent shell quoting bug in its Markdown summary is
repaired in #11 without replacing destinations or changing availability results.

Large optional redesigns (a reusable cross-repository workflow or validator
plugin framework) are not required for the accepted shared-runtime contract.
Site-specific validators, search inclusion rules, analytics IDs, crawler policy,
and Glee's offline/Sparkle features remain intentional differences.

## Publication and cleanup evidence

OverKill PR #12 was squash-merged as `e94da4a1da314b474351e1562a87d10eff732448`.
Its local main was fast-forwarded and verified at divergence 0/0. Incorporated
remote branches were removed and eligible local history was preserved under
`refs/archive/2026-09-05` before cleanup. Active worktrees and unique or dirty
work remain owned by their respective tasks. MurderBird context material is
preserved separately from this infrastructure release.

| Repair | Squash result | Verification |
| --- | --- | --- |
| [OverKill #15](https://github.com/OKHP3/OverKill-Hill/pull/15) | `276e0164c4a8e24cfaf42bd8eeeaf4589bb4d325` | Three portability regressions and nine live-edge/hook tests pass; PR validation passes. Pages run 33974291158 succeeds, including exact-release live-edge verification. |
| [Glee #20](https://github.com/OKHP3/Glee-fullyTools/pull/20) | `390cbae6b3675eb6a684ec69bb5260def5fc9a48` | 23 script tests; structural, link, responsive, Sparkle and three-engine resilience checks pass. Pages run 33973828127 succeeds and public release-provenance.json identifies the same commit. |
| [AskJamie #11](https://github.com/OKHP3/AskJamie/pull/11) | `101428680781fd1c46623cbec30135b71f7f3b06` | PR validation includes 200 responsive checks with zero failures and browser smoke proving Mermaid, search, dark mode, defer and single-event analytics behavior. Parent independently passes 14 non-shell regression tests and the 36-input cache freshness check. |
| [AskJamie #12](https://github.com/OKHP3/AskJamie/pull/12) | `04cc3e7b8965f568253b6e2c18aa532f6e2a3d57` | PR and post-merge validation/deployment run 33974863335 pass. Public-site browser smoke 33975015777 passes. Repairs the CSP failure from #11's first post-merge run 33974292677 rather than suppressing it. Public manifest scope/start URL and deferred fingerprinted references verified. |
| [Glee #21](https://github.com/OKHP3/Glee-fullyTools/pull/21) | `5da805785d47f9bc29058b07d2a5467da32a1573` | Five regressions cover sequencing, all six gate failures, missing files, LF preservation, and report-free validation retaining real failures. Both review comments addressed; all PR validation/browser checks pass. Maintenance-only follow-on: no public runtime assets changed. [Release run 33974974192](https://github.com/OKHP3/Glee-fullyTools/actions/runs/33974974192) records its deployment status. |

Windows verification note: the existing AskJamie post-merge test fixtures use
POSIX PATH construction and selected the Windows WSL bash launcher in the
parent's environment. Those three fixtures were excluded from the successful
targeted Windows rerun; the full Linux CI gate is separate evidence. UTF-8
must be inherited by subprocesses (`PYTHONUTF8=1`), not just passed to the
parent interpreter.

Completed Glee portability and Glee/Ask R04 ancestor worktrees were removed
after clean-state and incorporation checks, with archive refs retained.
OverKill's R04 branch has unique commits and is preserved, as are unrelated
active and dirty worktrees. Cleanup does not mean deleting every branch.

The applicable infrastructure repairs are incorporated into remote main.
The successful runtime deployment proofs above remain distinct from merge
evidence and from the external/hosting limits. Optional architecture redesigns
and unrelated active work are not silently merged or deleted to manufacture
an empty backlog.
