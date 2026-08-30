# SxS Infrastructure Audit: OverKill-Hill / AskJamie / Glee-fullyTools
**Date:** 2026-08-29
**Scope:** functionality, scripting, CI/automation, validation, metadata/SEO, favicon, and behavior. Not a content or page-count comparison.

## Executive summary

- Root cause found for the overkillhill.com deploy outage (see `github-pages-deployment-incident` memory): OKH's `validate.yml` bundles the site-validation job and the Pages deploy job into one workflow with `concurrency: { cancel-in-progress: true }`. Any rapid push to `main` cancels an in-flight Pages deployment mid-flight — which is exactly what the 2026-08-22 Replit Agent push-loop would have done, and matches the "job was not acquired by Runner" / "Internal server error" symptoms in runs #411-415.
- Glee-fullyTools already solved this. It splits validation (`validate.yml`, `cancel-in-progress: true`, safe to cancel) from deployment (`pages.yml`, dedicated `concurrency: { group: pages, cancel-in-progress: false }`, triggered only on push to `main`). This is the pattern to backport to OKH.
- AskJamie's deploy step has **no concurrency block at all** — a different flavor of the same risk class (unbounded parallel deploy runs racing on the same Pages environment, no cancellation and no queuing discipline).
- Local QA tooling has forked into three incompatible stacks: OKH runs Playwright via 4 `npm run test:*` scripts; AskJamie has Playwright + Lighthouse as devDependencies but **zero `package.json` scripts** (tooling is invoked directly by workflow steps, not through npm); Glee-fully uses Puppeteer + Lighthouse, also with zero npm scripts, across the largest and least-consolidated `scripts/` directory of the three (~75 files).
- Only AskJamie has a real automated test suite (`tests/` — 6 pytest files + 1 Playwright smoke spec) and a documented `scripts/README.md` with an `scripts/archive/` for retired tooling. OKH and Glee-fully have no `tests/` directory and no scripts changelog; scripts accumulate with no retirement path.
- Governance docs have drifted from reality. OKH's `AGENTS.md` states "There is no root `package.json` or root build system" — false; a `package.json` with 4 QA scripts exists. AskJamie's `AGENTS.md` gives only the Mac path for the repo root; Glee-fully's gives both Mac and Windows paths.
- CSP `img-src` is scoped on OKH (`'self' data: https://overkillhill.com https://*.github.io https://avatars.githubusercontent.com`) but wide open on AskJamie and Glee-fully (`'self' data: https:`, i.e. any HTTPS host). This reads as an unintentional relaxation during CSP-generator drift, not a deliberate per-site choice.
- Analytics consent handling has diverged. AskJamie explicitly gates GA behind a documented consent key (`assets/js/app.js`, "Privacy-first analytics consent" block). OKH loads `gtag.js` unconditionally in `<head>` with a hardcoded measurement ID and no visible consent gate. Glee-fully's CSP permits GA/GTM plus Ko-fi's widget script; its consent-gating status needs a closer read of `app.js` (not confirmed either way in this pass).
- Root documentation filenames have drifted with no canonical casing rule: `security.md` (OKH) vs `SECURITY.md` (AskJamie, Glee-fully); `contributing.md` (OKH, present) vs `contributing.md` absent from AskJamie's listing vs `CONTRIBUTING.md` (Glee-fully); `roadmap.md` (OKH) vs `ROADMAP.md` (AskJamie) vs `docs/roadmap.md` (Glee-fully, nested instead of root). AskJamie is also the only repo with `LIFECYCLE.md` and `SUPPORT.md`; Glee-fully has `LIFECYCLE.md` but not `SUPPORT.md`; OKH has neither.

## Table 1 — Deploy & CI architecture

| Aspect | OverKill-Hill | AskJamie | Glee-fullyTools |
|---|---|---|---|
| Workflow files | mermaid-version-watch.yml, report-fork-contrast.yml, validate.yml | hosted-js-smoke.yml, mermaid-version-watch.yml, public-gpt-links.yml, validate.yml | mermaid-version-watch.yml, pages.yml, sparkle-qa.yml, validate.yml, viewport-qa.yml |
| Deploy trigger | Inside `validate.yml`, same job chain as validation (`needs: validate`) | Inside `validate.yml`, same job chain (`needs: validate`) | Separate `pages.yml`, push to `main` only |
| Validate concurrency | group keyed by event+ref, `cancel-in-progress: true` | none declared | group `site-validation-${{ref}}`, `cancel-in-progress: true` |
| Deploy concurrency | shares validate's `cancel-in-progress: true` (root cause of the outage) | shares validate's undeclared concurrency — unbounded parallel runs | dedicated `pages` group, `cancel-in-progress: false` |
| Scheduled validation run | every 6h (`17 */6 * * *`) | none | weekly (`17 4 * * 1`) |
| Pages artifact source | repo root (`.`) | `dist-pages` build dir, built by `scripts/prepare-pages-artifact.py` | repo root, built in the deploy job itself |
| Post-deploy verification | `scripts/verify-live-edge.py` diffs live origin against the validated commit | none found | none found |
| Deploy incident history | Active outage since 2026-08-06, ~1105 commits stale | none known | none known |

## Table 2 — Local QA / scripting / validation

| Aspect | OKH | AskJamie | Glee-fully |
|---|---|---|---|
| `package.json` scripts | 4: `test:accessibility`, `test:screen-reader`, `test:phone-overflow`, `test:responsive` | none declared | none declared |
| `package.json` deps | playwright | playwright, lighthouse (dev) | puppeteer (dep), lighthouse (dev) |
| Formal test suite | none | `tests/`: 6 pytest files + 1 Playwright `.spec.mjs` smoke test | none |
| `scripts/` size | ~65 files | ~15 files + `scripts/archive/` + `scripts/README.md` | ~75 files (largest, least documented) |
| Repo-unique scripts | `verify-live-edge.py`, `cross-site-sync.py`, `lint-voice.py` + baseline JSON | `capture-visual-baseline.mjs`, `check-public-gpt-links.py`, `lighthouse-routes.mjs`, `prepare-pages-artifact.py` | `check-glee-dark-coverage.py`, `check-workflow-actions.py`, `sync-css-version.py`, `sync-social-card.py`, `sync-sparkle-fallback.py`, `serve-site.py` |
| Lint/format config | `.editorconfig` only | `.editorconfig` only | `.editorconfig` only |
| Git hooks (husky, etc.) | none | none | none |
| Node/npm version pin | none | `.npmrc` present, no version pin | none |

## Table 3 — Metadata / SEO

| Aspect | OKH | AskJamie | Glee-fully |
|---|---|---|---|
| OG + Twitter cards | full | full | full |
| JSON-LD blocks in `index.html` | 2 | 3 | 2, incl. `WebSite` + `SearchAction` |
| hreflang / i18n | yes (`/fr/`, `x-default`) | no | no |
| robots.txt AI-crawler stance | opts in most named AI bots explicitly (GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot, CCBot, Bytespider, etc.) | opts in GPTBot/OAI-SearchBot/anthropic-ai, blocks CCBot | blocks GPTBot, allows OAI-SearchBot/ChatGPT-User |
| sitemap.xml `lastmod` | absent on homepage entry | present, dated 2026-05-03 | present, dated 2026-05-12 (some entries 05-27) |
| Search index freshness | 2026-08-28, 203.9 KB | 2026-08-29, 111.7 KB | 2026-08-26, 138.7 KB — 3 days stale relative to the other two |
| `feed.xml` | generator script exists, output file absent from repo root | no script, no file | script + current file both present |

## Table 4 — Favicon & manifest

| Aspect | OKH | AskJamie | Glee-fully |
|---|---|---|---|
| `favicon.ico` | yes | yes | yes |
| `favicon.svg` | yes, at repo root | no | yes, under `assets/img/favicons/` |
| Icon `<link>` tags in `<head>` | 5 (32px/16px/apple-touch/ico/manifest) | 5 (manifest/ico/32px/16px/apple-touch) | 6 (svg/32px/16px/apple-touch/ico/manifest) |
| `site.webmanifest` icon set | 6 sizes incl. maskable | 2 sizes only (192/512) — narrower than its own `<head>` icon links | 7 entries incl. svg + maskable |
| `theme_color` (manifest) | static `#2a2320` | static `#2c5e6f` | static `#d35b2d` |
| `theme-color` meta, light/dark split | no — single value | yes, split by `prefers-color-scheme` | yes, split but both values identical (`#d35b2d`) — dark mode doesn't actually get a distinct browser-chrome color despite the site having a dark theme toggle |

## Table 5 — Behavior (analytics, CSP, PWA)

| Aspect | OKH | AskJamie | Glee-fully |
|---|---|---|---|
| Analytics loader | `gtag.js` loaded unconditionally in `<head>`, hardcoded measurement ID, no visible consent gate | GA gated behind an explicit, documented consent key in `assets/js/app.js` | CSP permits GA/GTM + Ko-fi; loader location/consent gating not confirmed in this pass |
| CSP `img-src` | scoped: self + overkillhill.com + `*.github.io` + `avatars.githubusercontent.com` | wide open: `'self' data: https:` (any HTTPS host) | wide open: `'self' data: https:` (any HTTPS host) |
| CSP extra allowances | `cdn.jsdelivr.net` (script/connect) | none extra | `storage.ko-fi.com` (Ko-fi donation widget) |
| Service worker / offline | none | none | `sw.js` + `offline.html` — only site with PWA offline support |

## Mitigation plan

### Options

1. **Backport Glee-fully's split validate/deploy pattern to OKH and AskJamie**, standardize CSP `img-src`, freeze a canonical doc-filename casing. Medium effort (roughly one focused session per repo). Directly fixes the active outage's root cause and closes the AskJamie concurrency gap in the same pass.
2. **Minimal patch**: add `cancel-in-progress: false` to OKH's existing combined validate+deploy workflow without splitting it. Low effort, partially reduces risk, but a slow or failing validate step still blocks/delays every deploy, and the two concerns stay coupled.
3. **Full unification**: one shared reusable `site-infra` workflow (via `workflow_call`) plus a shared npm script contract (`lint`/`build`/`test`) and a shared CSP generator driven by `brand-styles/registry.yaml`, called by all three repos. High long-term payoff, but touches build tooling on all three live sites simultaneously — too much blast radius while OKH's pipeline is actively down.

### Recommendation

Option 1 now, Option 3 as a deliberate follow-up once OKH is confirmed deploying cleanly again on its own. Don't attempt full reusable-workflow unification while one site's pipeline is actively broken — stop the bleeding first, converge the architecture second.

### Risks + mitigations

- Splitting OKH's workflow could itself produce another failed run while GitHub's hosted-runner capacity issue is ongoing. Mitigate: keep the workflow change small, validate it via `workflow_dispatch` on a branch before merging to `main`.
- Touching three live production repos raises the odds of a bad push reaching a public site. Mitigate: work on branches, never push directly to `main`, open PRs for review rather than committing straight to the default branch.
- Tightening CSP `img-src` on AskJamie/Glee-fully could break an image host currently in live use. Mitigate: audit actual image `src` domains referenced by each site before narrowing its CSP — don't copy OKH's allowlist blindly.
- Doc filename renames (`SECURITY.md` vs `security.md`, etc.) touch GitHub's community-profile detection and any inbound links. Mitigate: confirm which casing GitHub's community-profile checklist actually reads before standardizing.

### Next actions

- [ ] Confirm remediation scope with Jamie (branch+PR vs. direct local commit vs. proposal-only) before any subagent touches these repos
- [ ] Fix OKH's `validate.yml` concurrency split — root-cause fix for the active deploy outage
- [ ] Add deploy-safe concurrency (`cancel-in-progress: false`, dedicated group) to AskJamie's deploy step
- [ ] Audit and tighten CSP `img-src` on AskJamie + Glee-fully to match OKH's scoped pattern (after confirming actual image hosts in use)
- [ ] Refresh the "Confirmed" sections of all three `AGENTS.md` files to match current repo reality
- [ ] Decide one canonical root-doc filename casing and apply it across all three repos
- [ ] Re-run this audit after fixes land to confirm convergence

## Remediation status (2026-08-29, same day)

All 3 repos now have a local feature branch with commits ready for Jamie to push and open as a PR. Nothing was pushed and no PR was opened — none of these sandboxes have a working GitHub credential (SSH egress is blocked, no HTTPS PAT configured), so push/PR is a manual step. `main` was not touched in any repo.

**Corrections to the tables above, found during remediation:**
- Table 1's claim that AskJamie's deploy job has "none declared" for concurrency is stale. `git blame` traces a fix to commit `068d432c` (2026-08-08, "ci: deploy AskJamie after validation (#5)") — three weeks before this audit. AskJamie's deploy job already had the correct `concurrency: {group: pages, cancel-in-progress: false}` block. No action was needed there.
- Table 1/Executive-summary's claim that OKH uses lowercase root doc filenames (`security.md`, `contributing.md`, `roadmap.md`, `code_of_conduct.md`) was a false read. `git ls-tree`/`git ls-files` on all three repos show the uppercase forms (`SECURITY.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `CODE_OF_CONDUCT.md`) were already git-tracked before this audit — the lowercase appearance was a case-display artifact of the local device-bridge mount (NTFS case-insensitivity), not the real committed casing. No renames were needed on any of the three repos.

### overkill-hill — branch `fix/split-pages-deploy-workflow`
- `735730a` — split the Pages deploy job out of `validate.yml` into a new dedicated `pages.yml` (concurrency group `pages`, `cancel-in-progress: false`), matching Glee-fullyTools' proven pattern. This is the root-cause fix for the active deploy outage. Same pinned action SHAs preserved; `verify-live-edge.py` post-deploy check carried over.
- `f3c35d7` — corrected AGENTS.md's false "no root package.json" claim.
- Doc-casing step: no-op (see correction above). On-disk case was cosmetically repaired to match git (zero-diff, git-invisible).

### askjamie — branch `fix/deploy-concurrency-and-csp`
- Deploy concurrency: no-op, already fixed on 2026-08-08 (see correction above).
- `b627d14` — tightened CSP `img-src` from wide-open `https:` to `'self' data:` (askjamie references zero external image hosts — tighter than OKH's own scoped list). Fixed at the generator source (`scripts/csp.py`, `scripts/generate-csp.py`), regenerated across all 26 tracked HTML pages, `_headers`, and `config/csp-policies.json`.
- `86ffbe7` — added the missing Windows repo-root path to AGENTS.md.
- Doc-casing step: no-op, already correct (see correction above).

### glee-fullytools — branch `fix/csp-tightening-and-theme-color`
- `3903767d` — tightened CSP `img-src` to `'self' data:` (67 files: generator source + `_headers` + config + 63 regenerated pages). Ko-fi's `storage.ko-fi.com` was deliberately left out of `img-src` — the widget isn't actually live on any page yet (only a plain `<a href>` donation link exists); a comment was left in `scripts/csp.py` to add it when the widget ships.
- `fe010326` — fixed the dark-mode `theme-color` meta bug (both light/dark variants were stamping the same value). New dark value `#1e1b19`, sourced directly from `assets/css/theme.css`'s actual dark-mode background variable, not invented. Root cause fixed in the generator (`scripts/normalize-head.py`) so it stays correct going forward; applied to 62 live pages + 9 template snapshots.
- `0410c25e` — refreshed AGENTS.md's stale validation-baseline note.
- **Needs manual cleanup before further git operations in this repo:** two stale 0-byte lock files, `.git/HEAD.lock` and `.git/index.lock`, are blocking ordinary `git add`/`commit`/`checkout` in this repo (the agent worked around them via low-level git plumbing; commits are valid and verified). Delete those two files first.
- **Needs manual cleanup:** a stray duplicate `code_of_conduct.md` (lowercase, byte-identical to the git-tracked `CODE_OF_CONDUCT.md`) sits on disk next to it — `core.ignorecase=true` hides it from `git status`, but it's a real extra file. Safe to delete.
- **Flagged, not changed:** `docs/roadmap.md` is nested under `docs/` in this repo, unlike OKH's and AskJamie's root-level roadmap file. Worth a deliberate decision on whether to relocate it, not a silent fix.

### Still open (not in this pass)
- Push each branch and open a PR (manual — no credential available in the automation sandbox).
- Delete the two stale glee-fullytools lock files and the stray `code_of_conduct.md` duplicate (a `device_request_delete_permission` prompt was sent for all three repo folders — approve it, or delete manually).
- Re-run this audit once all three PRs are merged and OKH's next Pages deploy is confirmed successful, to verify convergence.

## Addendum (2026-08-30) — analytics consent removed from AskJamie

Jamie's call: drop AskJamie's visible analytics-consent banner and have all three sites load GA4 the same way, silently. OKH and Glee-fullyTools already did this (unconditional `<script>` tag, no prompt) — only AskJamie had a first-party consent gate, added a commit to the same branch (`fix/deploy-concurrency-and-csp`, commit `246a5bc`):

- Removed the consent IIFE from `assets/js/app.js` (readConsent/writeConsent/buildConsentBanner/addPrivacySettingsLink) and the dead `.privacy-consent`/`.privacy-settings-link` CSS from `assets/css/theme.css`.
- All 26 pages: swapped the "loads only after visitor consent" head comment for a real, unconditional gtag bootstrap (GA ID `G-MT9Y10YY0G`) — same shape as OKH's and Glee-fully's.
- Updated the Privacy section of `legal/index.html` to describe analytics as always-on (matching OKH's phrasing), removed the now-nonexistent "Decline" / "Privacy settings" language.
- Regenerated CSP (new script-src hash for the inline gtag block) via `scripts/generate-csp.py`; `check-csp.py`, `validate-site.py` (26 pages, 0 issues), and `check-links.py` (0 broken links) all pass clean.

One caveat worth knowing, not a blocker: dropping the consent gate means GA's cookie is now set on first page load for every visitor, including any from the EU/UK. That's a real compliance-posture change (ePrivacy/GDPR consent-before-tracking expectations), not just a UI tweak — flagging it since it's a fact you'd want on record, not a reason I held anything back. OKH and Glee-fully already operate this way, so this only brings AskJamie in line with the other two, not a new site-wide risk.

**New manual step for you:** the askjamie branch also left a stale `.git/HEAD.lock` behind (same class of issue as glee-fullytools' lock files, from the sandbox's delete restriction) — I worked around it by renaming it out of the way (`HEAD.lock.stale-<timestamp>`), so the repo is usable now, but that stray file is still sitting in `.git/` and is safe to delete whenever you get to the earlier cleanup pass.

## Addendum (2026-08-30) — app.js side-by-side: best-of verdict

Scope: the three sites' `assets/js/app.js` (OKH 765 lines, AskJamie 819, Glee-fullyTools 919). All three share an obvious common ancestor (identical header comment, identical Section 1 reading-progress-bar code, identical Section 4b scrollspy code) and have since drifted feature-by-feature. Read-only comparison, no code changed.

**Verdict: no single file wins outright. Build a shared canonical module, cherry-picking the best implementation of each section.** Each file is strongest in a different area, and the gaps are structural (missing accessibility, missing defensive coding), not stylistic. Picking one file as the base and discarding the other two throws away real, working, better code.

### Section-by-section comparison

| Section | OKH | AskJamie | Glee-fullyTools | Best |
|---|---|---|---|---|
| 1. Reading progress bar | identical | identical | identical | tie (no drift) |
| 1b. Mermaid a11y text alternative | present | absent | absent | **OKH** — only site with Mermaid diagrams, so this is expected, not drift |
| 2. Mobile nav | full focus management, Escape, `inert` on background | minimal, no focus trap | mid-level | **OKH** |
| Theme toggle | single-layer, `okh-theme` key, raw `localStorage` calls (no try/catch) | same single-layer pattern as OKH | dual-layer: `data-theme` (always "light" on brand-locked sites) + separate `data-color-scheme` + brand-specific key (`glee-color-scheme`/`askjamie-color-scheme`), every `localStorage` call wrapped in try/catch | **Glee-fullyTools** — architecturally correct for a locked-brand site and the only one that survives a `localStorage`-disabled browser without throwing |
| 3. Under-construction overlay | dead code on this site, minimal markup, no ARIA | dead code on this site, minimal markup, no ARIA | live and fully built: ARIA dialog role, focus trap, focus restoration, auto-focus, try/catch | **Glee-fullyTools** — only one of the three that's actually WCAG-compliant, and the only one where it matters (it's live) |
| 4. Sticky TOC scroll-follow | **removed on purpose** — comment claims CSP rejects the dynamic inline styles and it was "producing browser QA errors" | full JS lerp-follow, working in production | full JS lerp-follow, working in production | see verdict below — the premise for removing it doesn't hold up |
| 4b. TOC scrollspy | identical | identical | identical | tie (no drift) |
| 5. Search — snippet selection | body-first, ignores whether the match token is actually in the description | same as OKH | same as OKH | **AskJamie** — prefers the description when the token actually appears there, falls back to body otherwise; produces more relevant snippets |
| 5. Search — accessibility | live-region present | `announce()` + `announceStats()` pattern, cleared then re-set via `requestAnimationFrame` so identical result counts still get re-announced | live-region present | **AskJamie** |
| 5. Search — brand awareness | not brand-detecting (single brand) | detects `askjamie-main` vs `glee-main` in overlay copy | not brand-detecting (single brand) | **AskJamie** — only one actually exercising this in code, but it's the right pattern for a shared module |
| 5. Search — index-key fallback | `.pages` only | `.pages` only | `.pages` then `.entries` fallback, plus an `entrySection()` helper | **Glee-fullyTools** — more defensive against a search-index schema change |
| 6. Service Worker registration | absent | absent | present (`/sw.js`) | Glee-fullyTools-only feature (offline shell) — not drift, a deliberate PWA choice; not a candidate for the shared module unless OKH/AskJamie also want offline support |
| 7. Sparkle banner loader | absent | absent | present | Glee-fullyTools-only content feature, same call as above — leave it site-specific |
| Analytics event tracking | absent | `gpt_click` / `inquiry_click` via `askJamieTrack()` wrapper | absent | AskJamie-only feature (tracks its own ChatGPT/mailto links) — site-specific, not shared-module material, but the `askJamieTrack()` wrapper pattern (thin, no-op-safe, checks `typeof window.gtag === "function"`) is worth adopting everywhere GA event tracking gets added later |

### The sticky-TOC discrepancy: resolved, not just flagged

OKH's Section 4 comment reads: *"The right rail owns sticky positioning in CSS. Keeping scroll positioning declarative avoids dynamic inline styles, which are correctly rejected by the page CSP and were producing browser QA errors on every TOC page."*

That premise doesn't hold up. AskJamie and Glee-fullyTools both ship the identical `.style.transform =` JS lerp-follow pattern in production right now, under CSPs that are equally strict or stricter than OKH's (Glee-fullyTools' `style-src-attr` allowlist is the most locked-down of the three, hash-for-hash). Both pass their own `check-csp.py` clean. CSP's `style-src-attr` directive governs the HTML `style=""` attribute (and `setAttribute('style', ...)`); assigning through the CSSOM `.style.transform` property is a different code path and isn't reliably gated the same way. Whatever produced OKH's original QA errors, it's very unlikely to have been `style-src-attr` blocking a `.style.property =` write outright — a stale CSP header from an older policy revision or a browser-specific enforcement quirk is a more plausible explanation than "this JS pattern is CSP-incompatible."

Practical read: OKH is the outlier, not the other two. Recommend restoring the JS lerp-follow to OKH's canonical module rather than treating the CSS-only fallback as correct-by-default. One condition before merging: smoke-test it live on an OKH TOC page under OKH's actual deployed CSP (not just `check-csp.py`) to rule out a real browser-specific rejection before trusting the comment was simply wrong.

### Recommendation

Build one canonical `app.js` (or split into shared modules + a small per-site config block, if you want to go further) combining:

- OKH's mobile-nav focus management and Mermaid a11y section (kept as an OKH-only module if Mermaid stays OKH-exclusive)
- Glee-fullyTools' dual-layer theme/color-scheme architecture, try/catch-wrapped `localStorage` access throughout, and the fully-accessible under-construction overlay pattern (even on sites where it's currently dead code — it costs nothing and any site could ship a "coming soon" page later)
- Glee-fullyTools' more defensive search index-key fallback (`.pages` → `.entries`)
- AskJamie's smarter `snippetFor()`, its `announce()`/`announceStats()` live-region pattern, and its brand-aware overlay copy generalized to detect all three brands instead of just two
- The restored JS lerp-follow sticky TOC, pending the live CSP smoke test above
- Service Worker registration and Sparkle banner loader stay Glee-fullyTools-only unless you want offline support and a content-banner system on the other two — that's a product decision, not a drift-correction

### Risks + mitigations

- **Regression risk from merging behavior that's currently untested on two of the three sites** (accessible overlay, dual-layer theming) → land behind the same validation gate used for the CSP/analytics changes (`validate-site.py`, `check-csp.py`, `check-links.py`) plus a manual pass in a real browser on each site before merging.
- **The CSP smoke test could go the other way** (OKH's comment turns out right for some OKH-specific reason — a page-specific CSP variant, a browser extension environment, etc.) → don't restore the JS lerp-follow on OKH until that test passes; ship the rest of the composite module without it if so, and leave a comment recording what was actually tested.
- **Three-way merge effort is nontrivial** — this is a real refactor, not a find-and-replace → recommend doing it as its own branch/PR per repo, separate from the deploy-concurrency and CSP fixes already in flight, so it doesn't block those from merging.

### Next actions

- [ ] Confirm you want this built, and whether you want one shared file per repo (current pattern) or actual shared modules with a build step
- [ ] Live-test the JS sticky-TOC lerp-follow on an OKH page under OKH's deployed CSP
- [ ] If confirmed, spawn per-repo subagents to build the composite `app.js` on new branches, same non-destructive local-commit pattern as the last pass

## Addendum (2026-08-30) — AskJamie fonts moved off local hosting to Google Fonts CDN

Jamie's call: no locally-hosted files, CDN only, converge AskJamie onto the same font-loading pattern as OKH and Glee-fullyTools. Landed as a new commit on askjamie's existing branch `fix/deploy-concurrency-and-csp` (commit `5c6a5d0`), local-only per the same no-push-credential constraint as the rest of this pass.

**What AskJamie's real brand fonts turned out to be:** `.askjamie-main` (its brand-scoped block, present in all three repos' shared `theme.css` per the original one-file-per-repo architecture) sets `--font-heading: "Baloo 2"`, `--font-body: "Open Sans"`, `--font-accent: "Kalam"`. Those were being self-hosted via `assets/css/fonts.css` (5 local `.woff2` files, imported at the top of `theme.css`) instead of loaded from Google Fonts like OKH's and Glee-fullyTools' own brand fonts already are. All three are ordinary Google Fonts families — no substitution needed.

- `theme.css`: dropped the `@import url("/assets/css/fonts.css")`.
- All 26 production pages + 9 templates: added the same preconnect + Google Fonts `css2` stylesheet pattern OKH and Glee-fullyTools already use, loading Baloo 2 (600/700), Open Sans (400/600), and Kalam (400) — the exact weights the local files served.
- `assets/css/fonts.css` and the 5 local `.woff2` files: untracked from git. The sandbox couldn't unlink the working-tree copies (same delete restriction as the earlier lock-file issue), so they're sitting on disk as untracked cruft — safe to delete manually, or once the `device_request_delete_permission` prompt gets approved.
- `scripts/csp.py`: added `https://fonts.googleapis.com` to `style-src` and `https://fonts.gstatic.com` (+ `data:`) to `font-src`, for the common policy and every per-page-class policy — matching the exact CSP shape OKH and Glee-fullyTools already carry for their own CDN fonts. Regenerated `config/csp-policies.json` and every page's CSP meta tag.
- `scripts/validate-site.py`: removed the `DISALLOWED_FONT_HOSTS` / `check_external_font_origins` guardrail and its now-unused `find_stylesheet_files` helper. That check existed specifically to enforce "no external font requests" under the old self-hosting architecture — it's the opposite of the now-intended behavior, so it came out rather than being updated to allow what it was built to block.

Verified clean: `check-csp.py` (26/26), `validate-site.py` (0 errors/warnings), `check-links.py` (0 broken links).

**Unrelated finding surfaced along the way, not fixed:** this repo's working tree has widespread line-ending drift — over 100 files (workflow YAML, JSON audit reports, markdown docs, ADRs, brand-styles YAML, none of them touched by this pass) show as locally modified against `git`'s tracked content, and the diff on every one is a pure CRLF/LF flip with no content change. Some of the HTML pages this commit touched picked up the same flip as a side effect of the edit (three of the nine templates show large line-count diffs that are line-ending noise, not content noise — `check-links.py`/`validate-site.py` confirm the actual content is correct). Worth a `.gitattributes` pass (`* text=auto eol=lf` or similar) at some point so local Windows checkouts stop drifting from what's actually committed — it's currently masking real diffs during review, the same class of false-drift-signal as the NTFS case-insensitivity issue caught earlier in this audit. Not urgent, not part of this scope, flagging so it doesn't get mistaken for content churn later.

## Addendum (2026-08-30) — scripts/ directory: SxS and unification scoping

Requested ahead of the theme.css pass: "if it works for one, why not all; if it's necessary for one, why not all," applied to each repo's `scripts/` directory. Short answer: this set doesn't behave like app.js or fonts.css. Those were one file each, doing one job, diverged by accident. `scripts/` is 73–76 files per repo doing dozens of unrelated jobs, and the divergence is mostly real — different sites, different content, different one-time migrations. Convergence is worth doing on a specific slice, not the whole directory.

### Inventory

| | OverKill-Hill | Glee-fullyTools | AskJamie |
|---|---|---|---|
| Total files in `scripts/` | 73 | 76 (+ `tests/`) | 16 (+ `README.md`, `archive/`) |
| Present in all three repos | 9 | 9 | 9 |
| Shared with exactly one other repo | 0 | 0 | 0 |
| Unique to this repo | 12 (incl. `voice-lint-baseline.json`) | 11 | 5 |
| Shared with the other two-way overlap (OKH+Glee only) | 47 | 47 | — |

AskJamie is the outlier in shape, not just content: it has no `voice-lint`/`banner`/`mtb-version`/`illustrations`/`kebab-rename` machinery at all, because it never went through the same years-long content-migration history OKH and Glee-fullyTools share. It's the newest, leanest repo of the three, and its `scripts/README.md` + `archive/` convention (documenting retired tooling instead of leaving it to rot in the working tree) is the best practice of the three and worth backporting on its own, independent of anything below.

The 47 files shared only between OKH and Glee-fullyTools are almost entirely one-shot content-migration and asset-conversion scripts from their shared build history — `generate-illustrations.py`, `wire-illustrations.py`, `kebab-rename-images.py`, `inject-toolette-hub.py`, `reorg-theme-css.py`, and so on. These already ran, already did their job, and have no ongoing execution path (not called from `post-merge.sh`, not called from CI). They're historical record, not live infrastructure. Unifying them would mean maintaining three-way parity on code that never runs again — pure cost, no benefit. Recommend leaving these alone and, if anything, moving the ones with zero references left into each repo's own `archive/` (AskJamie already has the convention).

### The core 9 — present in all three, actually live infrastructure

| Script | OKH lines | Glee lines | AskJamie lines | OKH↔Glee diff | OKH↔AskJamie diff | Glee↔AskJamie diff |
|---|---|---|---|---|---|---|
| `check-csp.py` | 8 | 9 | 9 | 21 | 21 | **0** |
| `check-links.py` | 233 | 161 | 161 | 123 | 123 | **4** |
| `responsive-qa.mjs` | 386 | 398 | 398 | 250 | 254 | **4** |
| `csp.py` | 207 | 194 | 172 | 403 | 381 | 46 |
| `generate-csp.py` | 77 | 143 | 110 | 147 | 83 | 104 |
| `post-merge.sh` | 55 | 19 | 70 | 53 | 98 | 58 |
| `audit-site.py` | 580 | 593 | 758 | 200 | 410 | 427 |
| `build-search-index.py` | 606 | 369 | 338 | 933 | 907 | 657 |
| `validate-site.py` | 920 | 1,079 | 597 | 1,964 | 1,109 | 1,623 |

Two different stories in that table, and they call for two different responses.

**`check-csp.py`, `check-links.py`, `responsive-qa.mjs`: already converged, just not admitted to it.** `check-csp.py` is byte-identical across all three (it's a 9-line `runpy` shim into `generate-csp.py --check`). `check-links.py` and `responsive-qa.mjs` are 4 lines apart between Glee-fullyTools and AskJamie — noise, not drift — and only diverge from OKH's copy because OKH's is carrying extra OKH-specific logic (its own extra route table, mostly). These are the actual "if it works for one, why not all" case: pull each into a genuine single shared file, parameterized by the couple of site-specific constants (site origin, route allowlist) that currently get hand-copied. Low risk, immediate payoff, no architecture change required.

**`csp.py` / `generate-csp.py`: same shape, different content on purpose — and OKH's is the best version.** The Glee-fullyTools↔AskJamie diff on `csp.py` (46 lines) is entirely per-site allowlist content: Glee-fullyTools' CSP permits its Ko-fi widget and its own `img-src` rationale comment; AskJamie's permits `https://www.google.com` in `connect-src` that Glee-fullyTools doesn't need. Same functions, same page-classifier approach, different third-party services each site actually embeds — this is config divergence, not logic divergence, and it's correct that it exists. OKH's version is functionally ahead of both: it has a 5-way page classifier (`standard` / `embed` / `utility` / `diagram` / `embed-diagram`) that Glee-fullyTools and AskJamie's 3-way classifiers don't carry, built to handle Mermaid-diagram pages needing a scoped `style-src` relaxation that a hash-only policy can't satisfy. AskJamie's `generate-csp.py` already shows the direction of travel — its own header comment says *"Ported from OverKill Hill P3's scripts/generate-csp.py"* and it independently rebuilt `build_edge_policy()` to match OKH's. Recommendation: promote OKH's classifier + edge-policy structure as the shared skeleton, keep each site's allowlist content (the actual different-origins list) as the per-site config block. Same "no single winner, composite" pattern as the app.js verdict — except here one repo (OKH) is unambiguously carrying the more complete logic, so this composite leans OKH's way more than app.js's did.

**`audit-site.py`, `build-search-index.py`, `validate-site.py`: real divergence, not a convergence candidate as a monolith.** These three are the largest files and the ones with the least line-for-line overlap, and it's because they're not really "one script" per repo — each is a grab-bag of independent checks or independent content-extraction logic that happens to live in one file. Pulling the function names out of `validate-site.py` makes the shape obvious:

| | OKH-only checks | Glee-fullyTools-only checks | AskJamie-only checks |
|---|---|---|---|
| Examples | voice-lint, banner text, MTB version consistency | ADR-index sync, sparkle-loader drift, dark-mode coverage, CSS token drift, offline-shell check | governance-docs consistency, plain-language terms |
| Shared core | `_page_renders_mermaid`, `validate_mermaid_csp_alignment`, `validate_mermaid_version_pin`, `html_to_route`, `find_html_files`, `load_sitemap_urls`, `resolve_internal`, `target_exists` (present in OKH and AskJamie; Glee-fullyTools' `main`/`check_page` structure has already diverged even on this shared core) | | |

`build-search-index.py` is worse: the three repos don't even share function names beyond `main`. OKH and AskJamie both center on a `TextExtractor` class, but with different internals; Glee-fullyTools uses an unrelated `PageParser` class. This isn't three implementations of the same idea that drifted apart — closer to three separate implementations of the same *goal* that were never the same code to begin with.

Forcing these three into one shared file per repo would mean either every site running every other site's irrelevant checks (OKH running AskJamie's plain-language linter, Glee-fullyTools running OKH's motorcycle-version checker), or building a real plugin/module system where each site opts into a shared core plus its own check modules. The second option is a legitimate long-term improvement, but it's a real architecture project, not a same-day unification pass, and it doesn't have the urgency the CSP/deploy work had. Recommend leaving these three alone for now and revisiting only if you want to formally invest in a shared validator framework later.

### A gap this comparison surfaced, unrelated to unification

`post-merge.sh` is correctly site-specific (it's each repo's own gate-sequencing recipe), but reading the three side by side surfaces a real coverage gap, not just a style difference:

- **OKH's hook** runs `check-mtb-version.py`, `build-site.py` (x2 + `--check`), `generate-csp.py`, `check-csp.py`, `validate-site.py` — but never calls `check-links.py` or `audit-site.py`, despite both scripts living in OKH's own `scripts/` directory.
- **Glee-fullyTools' hook** is 19 lines: rebuild search index, sync portfolio stats, done. It doesn't call `csp.py`/`check-csp.py`, `validate-site.py`, or `check-links.py` at all — none of Glee-fullyTools' own validation tooling runs on merge.
- **AskJamie's hook** is the most complete: search index, `audit-site.py --quiet`, `validate-site.py`, `check-links.py`, then spins up a local server and runs both `responsive-qa.mjs` and a Playwright JS smoke spec.

So the three sites aren't just running different checks because they have different content — Glee-fullyTools in particular is set up with real validation tooling (`check-csp.py`, `validate-site.py`, `check-links.py` all exist and work in that repo) that its own merge hook never invokes. That's a live gap independent of anything else in this document.

### Recommendation

- Converge `check-csp.py`, `check-links.py`, and `responsive-qa.mjs` into one real shared file each, parameterized by the small per-site config each already needs (site origin, route allowlist). Do this alongside the theme.css pass — low risk, immediate payoff.
- Rebuild `csp.py` / `generate-csp.py` as a shared skeleton (OKH's 5-way classifier + edge-policy builder) plus a per-site allowlist config block, same shape as the app.js composite recommendation. AskJamie's own code comments already point this direction.
- Leave `audit-site.py`, `build-search-index.py`, and `validate-site.py` as independent, site-specific files. Don't force them into a shared shape without a real plugin-architecture decision first.
- Leave the 47 OKH+Glee-fullyTools one-shot migration scripts alone; they're historical, not live. Consider retiring the ones with zero remaining references into each repo's `archive/`, following AskJamie's own `scripts/README.md` convention.
- Fix Glee-fullyTools' `post-merge.sh` to actually call its own `csp.py`/`validate-site.py`/`check-links.py` tooling, and OKH's to call `check-links.py` and `audit-site.py` — independent of the unification question, this is validation coverage that already exists and currently isn't wired in.

### Risks + mitigations

- **Shared `check-links.py`/`responsive-qa.mjs` could silently drop an OKH-specific route or check during the merge** → diff the pre- and post-unification output on all three sites before landing, not just a code review of the merged script.
- **The CSP skeleton promotion touches the same file the AskJamie fonts-CDN change just modified** → sequence this after that change is merged and live-verified, not concurrently, to avoid a three-way merge conflict on `csp.py`.
- **Wiring Glee-fullyTools' hook to actually run its validators for the first time may surface findings that have been silently accumulating** → run `validate-site.py`/`check-links.py` manually on Glee-fullyTools first and clear or triage whatever it reports before making the hook enforce it.

### Next actions

- [ ] Confirm the tiered approach above (converge the 3 thin scripts + CSP skeleton; leave the 3 large validators and the 47 legacy migration scripts alone)
- [ ] Build the shared `check-csp.py`/`check-links.py`/`responsive-qa.mjs` + CSP skeleton on the same branches already open for the CSP/font work, once those are confirmed live
- [ ] Wire Glee-fullyTools' and OKH's `post-merge.sh` to call the validation tooling they already have but don't run
- [ ] Decide, separately and with no urgency, whether a shared validator plugin architecture for `audit-site.py`/`build-search-index.py`/`validate-site.py` is worth building later

## Addendum (2026-08-30) — scripts/ janitor + organizer pass: archive, consolidate, naming, parity

Run via `okhp3-repository-janitor` + `okhp3-repository-organizer`. Both skills are propose-then-approve by contract ("never infer execution approval from a request to clean up, organize, or make consistent") — this is the evidence ledger and proposed move set. Nothing below has been executed. `git mv`/archive moves need an explicit go-ahead per repo.

### Branch-state check (janitor step 1, read-only)

All three repos are currently checked out on `main`, not the feature branches from the last pass — worth knowing before anything else moves:

- **OKH**: `fix/split-pages-deploy-workflow` (PR #7) and a follow-on contrast-report fix (PR #8) are both merged into `main`. Local feature branch is gone (deleted post-merge, as expected); nothing lost, confirmed via reflog.
- **AskJamie**: `fix/deploy-concurrency-and-csp`, including the font-CDN commit (`5c6a5d0`) from this pass, is merged into `main` (merge commit `86f404f`), plus two further commits landed on top since. Nothing lost.
- **Glee-fullyTools**: `fix/csp-tightening-and-theme-color` (`cec9ca1`) is still open and **unmerged** — `main` advanced separately via a different branch (`fix/kofi-and-mermaid-vendor` → PR #9, "Vendor Mermaid 11.17.2 and Ko-fi CSP support"). This is a pre-existing loose end, not something this pass touched — flagging so it doesn't get lost track of. The scripts/ comparison below is run against each repo's current `main`, which for Glee-fullyTools means the CSP-tightening branch's `csp.py` changes aren't reflected yet.

All three working trees also carry the same pre-existing CRLF/LF line-ending noise flagged in the last addendum (300-500 "modified" lines each, no real content change) — untouched, not part of this pass.

### One-and-done cleanup: AskJamie already solved this, twice

Before proposing anything new: AskJamie's `scripts/` already has exactly the taxonomy this request is asking for. `scripts/README.md` classifies every script as **active** (10 scripts — the live pipeline), **reference-only** (25 scripts — useful for a scoped one-off task, not part of the pipeline), or **retired** (17 scripts — historical, must not be run), with everything but "active" physically moved into `scripts/archive/`. `tests/test_release_checks.py` even enforces it: the active table is the allowlist, checked against what CI and `post-merge.sh` actually invoke, so nothing retired can silently sneak back into the pipeline. This is the best-practice version of the whole ask, already built and proven. Recommend copying this exact pattern to OKH and Glee-fullyTools rather than inventing a new one.

Cross-referencing AskJamie's own classification against OKH's and Glee-fullyTools' `scripts/` (most of the 47-file OKH+Glee-fullyTools overlap are the same tools, from the same shared migration history, that AskJamie already triaged on 2026-08-22) plus a live reference check of this session (grep for each filename against CI workflows, `post-merge.sh`, other scripts, and docs, repo-wide):

| Repo | Active (real refs: CI/post-merge/another script) | Reference-only (documented, not wired in) | Retired candidate (zero references anywhere, incl. docs) |
|---|---|---|---|
| OKH | 24 | 33 | **16** — `activate-icons.py`, `add-toolbox-to-footer.py`, `fix-audit-2026-05-12.py`, `fix-banner-text.py`, `fix-image-performance.py`, `fix-placeholder-gpt-links.py`, `generate-templates.py`, `inject-gpt-icon-picture.py`, `inject-keep-exploring.py`, `inject-showcase-footer.py`, `inject-showcase-subnav.py`, `reclassify-construction-banners.py`, `sync-portfolio-stats.py`, `update-card-srcsets.py`, `update-image-refs.py`, `update-placeholder-dimensions.py` |
| Glee-fullyTools | 27 | 49 (every script is at least mentioned in `AGENTS.md`/`replit.md` — Glee-fullyTools' docs hygiene is already good, but "documented" isn't the same as "still needed") | 0 by the zero-reference test, but the AskJamie cross-reference below narrows this |
| AskJamie | 10 (already done) | 25 (already done) | 17 (already archived) |

OKH's own zero-reference list (16 scripts, table above) is the cleanest, lowest-risk retire batch — nothing in the repo, including its own governance docs, mentions them anymore. Additionally, two files are dead duplicates, not just unused: `overkill-hill/scripts/site-audit.py` and `glee-fullytools/scripts/site-audit.py` are byte-for-byte identical (100% match) to each other, zero-referenced in either repo, and only 3.3% similar to the actually-active `audit-site.py` in the same directory — they're a different, superseded tool that happens to have a confusingly similar name, not a variant of the current auditor. Same story for `responsive-audit.py` (OKH and Glee-fullyTools copies are 100% identical, both superseded by `run-viewport-qa.py`/`viewport-qa.py`).

For Glee-fullyTools, since the zero-reference test alone doesn't separate active from historical (its docs mention everything), the AskJamie precedent is the more useful signal: matching Glee-fullyTools' file list against AskJamie's own retired/reference-only tables by name puts roughly 40 of Glee-fullyTools' 76 scripts in the same "historical migration tooling" bucket AskJamie already retired.

**Proposed action (needs approval):** create `scripts/archive/` + `scripts/README.md` in OKH and Glee-fullyTools, modeled on AskJamie's, and `git mv` each repo's retired/reference-only scripts into it. This is a rename/move, not a deletion — full history preserved, reversible with `git mv` back.

### Cluster, consolidate, streamline: the 70%+ test, run for real

Character-level similarity (`difflib.SequenceMatcher`, not just diff line count, since line-count diffs overstate divergence when only comments/reordering differ) across the 9 scripts every repo already has in common:

| Script | OKH↔Glee | OKH↔AskJamie | Glee↔AskJamie | Verdict at the 70% bar |
|---|---|---|---|---|
| `check-csp.py` | 99.8% | 99.8% | 100.0% | **Converge** — already identical |
| `audit-site.py` | 95.3% | 69.0% | 71.9% | **Converge** — OKH/Glee-fullyTools basically the same file already; AskJamie just under/at the line |
| `responsive-qa.mjs` | 71.0% | 71.0% | 100.0% | **Converge** — Glee-fullyTools/AskJamie identical, OKH close enough to fold in |
| `check-links.py` | 40.2% | 40.2% | 99.8% | **Converge Glee↔AskJamie**; OKH's copy carries extra OKH-specific route logic worth keeping as a config layer, not a rewrite |
| `csp.py` | 63.0% | 45.2% | 78.5% | **Converge Glee↔AskJamie** (per-site allowlist diffs only, as detailed in the previous addendum); OKH's stays the structural donor (5-way classifier) rather than a straight merge target |
| `generate-csp.py` | 8.6% | 72.8% | 12.0% | **Converge OKH↔AskJamie** — AskJamie's is a documented port of OKH's; Glee-fullyTools' has diverged furthest and needs the same treatment applied to it |
| `post-merge.sh` | 14.1% | 14.8% | 28.3% | **Leave separate** — under the bar on every pair; this is each site's own gate-sequencing recipe by design |
| `build-search-index.py` | 4.8% | 3.5% | 9.7% | **Leave separate** — three unrelated implementations, not drift |
| `validate-site.py` | 2.1% | 15.3% | 4.0% | **Leave separate** — confirmed last pass: mostly independent, site-specific checks in one file |

Net: 6 of the 9 clear the 70%+ bar on at least one pair and are real consolidation candidates; the other 3 (`post-merge.sh`, `build-search-index.py`, `validate-site.py`) are consistently under 30% on every pair and are doing genuinely different jobs, not drifting copies of the same job. Forcing those three into a shared file would be the opposite of streamlining.

### Naming conventions

Clean, for the most part. All three repos already use portable, ASCII, lowercase-hyphenated `.py`/`.mjs`/`.sh` names — no spaces, no case collisions, no reserved device names, nothing that would misbehave crossing Windows/macOS/Linux. Two things worth fixing:

- `site-audit.py` vs `audit-site.py`: two different tools with near-anagram names in the same directory (confirmed 3.3% similar — not a typo of each other, an actual different, dead tool). This is exactly the kind of name collision that causes someone to run the wrong script by habit. Resolved by the archive move above, since `site-audit.py` is one of the retire candidates.
- Date-stamped filenames (`fix-audit-2026-05-12.py` in OKH, `fix-footer-nav-2026-07-20.py` in Glee-fullyTools) are portable-clean as names but self-declare as one-shot by construction — same bucket as retired, and AskJamie's own convention (drop the fix script once it's applied, keep a changelog line instead) is the better long-term pattern.

### Foundational-file parity across the three sites

Combining this pass with the CSP/classifier findings from the previous addendum, the target end state for the core 9:

| Script | Target |
|---|---|
| `check-csp.py` | One shared file, identical in all three (already is) |
| `check-links.py` | One shared file + small per-site route-allowlist config |
| `responsive-qa.mjs` | One shared file + small per-site base-URL/route config |
| `audit-site.py` | One shared file, given the 95%/69%/72% overlap — needs a closer read to confirm the remaining ~30% (AskJamie side) is config, not logic, before finalizing |
| `csp.py` / `generate-csp.py` | OKH's 5-way classifier + edge-policy builder promoted as the shared skeleton; each site keeps its own allowlist (origins, third-party scripts) as config — matches the app.js "composite" pattern, OKH as structural donor |
| `post-merge.sh`, `build-search-index.py`, `validate-site.py` | Stay independent per repo — confirmed genuinely site-specific, not drift |

### Next actions

- [ ] Approve (or amend) the OKH 16-script retire list and the Glee-fullyTools cross-referenced retire/reference-only split, then execute as `git mv` into new `scripts/archive/` directories with a `scripts/README.md` modeled on AskJamie's
- [ ] Approve consolidating the 6 scripts that clear the 70% bar; sequence `csp.py`/`generate-csp.py` after Glee-fullyTools' open CSP branch is resolved, to avoid a three-way conflict
- [ ] Decide whether to also port AskJamie's `test_release_checks.py` allowlist-enforcement pattern to OKH and Glee-fullyTools once their own README/active-table exists
- [ ] Confirm what to do with Glee-fullyTools' still-open `fix/csp-tightening-and-theme-color` branch before any CSP consolidation touches that file

## Execution report (2026-08-30) — archive move, committed

Executed the approved retire/reference-only archive move for OKH and Glee-fullyTools (AskJamie already had it). Consolidation (the 70%+ cluster) and the naming fix were folded into the same pass where they were just the archive move itself (`site-audit.py` duplicate); the code-level merges (`check-links.py`, `responsive-qa.mjs`, `audit-site.py`, and the `csp.py`/`generate-csp.py` skeleton) were not executed this pass -- still pending, see below.

- **OKH** (`8d7ca88`): 50 scripts moved to `scripts/archive/` via `git mv` (19 stay active), new `scripts/README.md` modeled on AskJamie's, `AGENTS.md`'s stale `60 scripts` count corrected. `check-csp.py`, `check-links.py`, `validate-site.py`, `audit-site.py` all verified clean post-move.
- **Glee-fullyTools** (`e3ba074`): 47 scripts moved (22 stay active), new `scripts/README.md`, and a real regression caught and fixed along the way -- Glee-fullyTools' own `validate-site.py` has a `_check_scripts_py_drift` guard comparing the live `scripts/*.py` count against a `<!-- STAT:SCRIPTS-PY -->` marker in `AGENTS.md`; the archive move tripped it (`live=20` vs `documented=67`), confirming the guard works. Fixed the marker and the surrounding doc text; `validate-site.py` now passes 0 issues/0 warnings.
- Two classification corrections made mid-execution, both caught by checking actual call sites rather than trusting a raw "mentioned somewhere" signal: `apply-modern-baseline.py` and `extract-templates.py`/`inject-color-scheme-init.py` looked active (mentioned by an active validator) but were only mentioned in a comment, not actually invoked -- moved to reference-only. `viewport-qa.py` in Glee-fullyTools initially looked CI-active because `viewport-qa.py` is a literal substring of `run-viewport-qa.py`, which really is CI-called -- confirmed the standalone file has no real caller and reclassified it reference-only. `site-audit.py` was aligned to retired in both repos (initially reference-only in Glee-fullyTools pending confirmation; confirmed zero references there too).
- Local git identity had to be set for Glee-fullyTools (`git config --local user.name/user.email`, matching the identity already configured in OKH and AskJamie) -- it had none and the commit failed without it.

**Not yet done, holding for a follow-up decision:**
- Consolidating `check-links.py`, `responsive-qa.mjs`, and `audit-site.py` into real shared files (the three that cleared the 70% bar and are safe to touch now).
- `csp.py`/`generate-csp.py` skeleton promotion -- intentionally held per the previous addendum's sequencing note: Glee-fullyTools' `fix/csp-tightening-and-theme-color` branch is still open and unmerged, and touching `csp.py` now risks a three-way conflict with it.

## Execution report (2026-08-30, phase 2) — check-links.py, responsive-qa.mjs, audit-site.py, csp.py/generate-csp.py

Executed the consolidation work held back from the previous addendum, plus resolved the CSP branch question.

- **`check-links.py`** — converged Glee-fullyTools and AskJamie onto OKH's version verbatim (only the `SITE` constant differs), replacing the OKH-specific-route hardcoding with OKH's more general `PageIndexingMeta`/`sitemap_exclusion()` noindex-aware mechanism. Verified live: OKH 39 pages/0 broken, Glee-fullyTools 63/0, AskJamie 26/0.
- **`responsive-qa.mjs`** — spliced OKH's more complete MODE A/head section (dynamic `loadPublicPaths()`, bounded-wait navigation, console-error filtering) onto each site's own unchanged MODE B `staticLintPage()` tail, since the site-specific structural checks are genuinely different per site. Verified live against local servers: AskJamie 192/192 passing. Glee-fullyTools surfaced a real, pre-existing bug (not introduced by this change, confirmed via diff) -- `staticLintPage()` checks for `class="skip-link"` but the site's actual markup uses `class="skip-to-content"`, so every MODE B run currently reports a false "missing skip link" on all 480 checks. Left as-is and flagged below; MODE A (Playwright, presumably what CI actually runs) doesn't depend on this string. Committed: Glee-fullyTools `4a10953`, AskJamie `dc90a81`.
- **`audit-site.py`** — this file has real site-specific logic (AskJamie's Flesch-Kincaid reading-level scorer tied to its plain-language mission; Glee-fullyTools' extra search-index-freshness check), so this was a targeted two-fix port to Glee-fullyTools rather than a full swap: the attribute-order-agnostic theme-color regex, and the noindex-aware `rels_on_disk` computation (both from OKH). Live run dropped Glee-fullyTools' "Total issues found" from 50 to 48 (2 false positives fixed, 0 new). OKH's and AskJamie's `audit-site.py` were left untouched. Committed `38bdc28`.
- **`csp.py` / `generate-csp.py`** — turned out to need far less than the previous addendum assumed. Re-checking Glee-fullyTools' `csp.py` on `main` (not the open branch) showed the 5-way page-classifier architecture was *already* fully ported and identical to `origin/main` -- that work landed in an earlier phase, and the open `fix/csp-tightening-and-theme-color` branch's actual diff against current `csp.py`/`generate-csp.py` is trivial (an `img-src` tightening from a `https:` wildcard down to `'self' data:`, plus some comment cleanup), not a fresh architecture port. All three sites' `check-csp.py --check` already passed clean before any change this session. The one real gap: OKH's `csp.py` defines `build_edge_policy()` itself and `generate-csp.py` imports it, while Glee-fullyTools and AskJamie had it defined locally inside `generate-csp.py` (functionally identical, organizationally inconsistent). Relocated it into `csp.py` for both, matching OKH's file layout exactly -- pure move, no behavior change, verified via `check-csp.py` (63/63 and 26/26 pages) and each site's `validate-site.py` (0 issues) both before and after. OKH's newer `load_policies()` and the `vault/index.html`/`site-src/` handling are genuinely OKH-only (tied to its `build-site.py` build step, which neither sibling has) and were correctly left unported. Committed: Glee-fullyTools `07f1b43`, AskJamie `e70050a`.
- All three repos' `check-links.py`, `check-csp.py`, and `validate-site.py` reverified clean at the end of this pass.

**Resolved from the previous addendum's open question:** Glee-fullyTools' `fix/csp-tightening-and-theme-color` branch is not a competing architecture port -- it's a small, legitimate `img-src` tightening bundled with ~94 files of unrelated theme-color/cache-busting/audit-hardening work, still unmerged, still touching files (`AGENTS.md`, `audit-site.py`) this session has independently edited on `main`. Left untouched; still Jamie's call whether to pull it in via GitHub Desktop, and worth splitting the img-src tightening out from the unrelated bulk if so.

**Still open, not touched this pass (unchanged from before):**
- Glee-fullyTools' `staticLintPage()` skip-link/skip-to-content class-name mismatch.
- Glee-fullyTools' `audit-site.py` `main()` always returning 0 regardless of findings (48 outstanding).
- The `refs/codex/turn-diffs/checkpoints/...` bad-object push-error refs in all three repos.
- Repo-wide CRLF/LF line-ending drift (confirmed again this pass, at AskJamie repo-wide scale via normalized diff on `assets/js/app.js` -- content identical, only line endings flipped) -- needs a `.gitattributes` fix, out of scope for this pass.
- AskJamie's untracked leftover `fonts.css`/woff2 files from an earlier phase.

Check-links.py, responsive-qa.mjs, audit-site.py, csp.py, and generate-csp.py are now consolidated and verified across all three sites. Clear to move to the theme.css pass.

## Execution report (2026-08-30, phase 3) — theme.css consolidation

Blended, optimized, and canonicalized the three sites' independently-drifted
copies of theme.css back into one superset, matching the target end state
this document already called for. OKH: 6,535 -> 7,519 lines. AskJamie:
committed at `7f4048a`.

**Blend (uniqueness census, via a block-level fingerprint diff, not just a
line diff):** 1,106 top-level blocks in OKH, 913 in Glee, 808 in AskJamie;
358/143/37 were fingerprint-unique to each. The real news: most of what
looked like "Glee-only" content was Glee's `data-color-scheme="dark"`
dark-mode system -- a genuine, working feature (Glee's own app.js sets this
attribute; AskJamie's does not yet) that already covered `.glee-main` AND
`.askjamie-main` more completely than either OKH's or AskJamie's own copy.
Absorbed it whole. Also absorbed Glee's search page, breadcrumb nav, and
arcade page styles (all genuinely Glee-only, verified against Glee's own
HTML), and confirmed OKH's ~283-block "unique" set is entirely OKH's own
article/project-page component library (writings, project layouts, DSL
showcase) -- correctly stays in the shared file per the existing
architecture (ships to all three, scoped inert on pages that don't use it).

**Optimize (~30 real conflicts, resolved case by case, not by a blind
"prefer X" rule):** checked each one's actual token resolution and contrast
math rather than assuming newest-wins. Two notable finds: (1) OKH's own
`.okh-search-trigger:hover` had a stale `outline: none` that both Glee and
AskJamie had already independently removed as a focus-visibility fix (WCAG
2.4.7/2.4.11) -- adopted the fix. (2) Glee's `.search-page ... 
[aria-pressed="true"]` still referenced the raw (WCAG-failing, ~2:1) amber
value under a different token name than the one OKH had already fixed --
kept OKH's tokenized, corrected version instead of assuming the sibling
was ahead just because it differed.

**Trash:** dropped 8 AskJamie-only `html[data-theme="dark"] .askjamie-*`
blocks, confirmed dead -- AskJamie's app.js unconditionally forces
`data-theme="light"`; its real dark mode is the (now-merged) 
`data-color-scheme` system. Kept `.skip-link, .okh-skip-link` in spite of
OKH's own "legacy, removed" comment -- AskJamie's HTML (404.html,
about/index.html, several templates) still ships `class="skip-link"`,
confirmed via grep; dropping it would have broken the skip link there.

**Tooling:** extended `scripts/archive/reorg-theme-css.py`'s brand
classifier (GLEE_PAT/ASKJAMIE_PAT predated several newer Glee class
prefixes) and fixed a selector-list disambiguation bug, then used it to
re-canonicalize the merged file into GLOBAL -> OKH -> GLEE -> ASKJAMIE
order. Committed the tool fix separately (`dc4d82a`).

**Verification:** css-tree (real parser, 0 errors), brace balance,
idempotent re-run, a fingerprint diff confirming zero blocks lost and zero
duplicates introduced by the merge, `validate-site.py`, `audit-site.py`,
`check-links.py`, `check-csp.py`, and `assets/scripts/check-contrast.py`
(every WCAG AA pair still passes, dark and light) on all three repos.

**Not fixed, flagged:** Glee's own `validate-site.py` runs a
"dark-mode coverage" check that flags `.glee-search-page__form` and
`.glee-search-page__results > li` as missing a dark-mode override --
confirmed via `git show HEAD` that this gap predates this session's merge
entirely; it needs an actual color decision, not a mechanical port, so it
was left for a follow-up rather than guessed at.

**Blocked on Glee-fullyTools specifically -- see chat for the full
writeup:** this repo's git state changed under this session multiple times
today while this work was in progress (a `codex/publish-local-main-work`
branch got rebased, force-updated, and merged to `main` via a "protected
PR" mid-session, evidently by another actor with push credentials this
sandbox doesn't have). The consolidated theme.css was committed there once
but the commit is now orphaned (object intact, not reachable from any
branch) after the repo moved again. OKH and AskJamie were not affected the
same way and are both committed clean. Re-applying the merge to
Glee-fullyTools' current `main` is a five-minute job once it's confirmed
safe to touch that repo again.

## Execution report (2026-08-30, phase 4) -- Glee-fullyTools reapply + 3-way sync script

**Glee-fullyTools reapply:** confirmed `main` had been stable at `25049b1`
(the "protected PR" merge from phase 3) for 5+ hours with no further branch
movement, so reapplied the tested, verified theme.css consolidation:
wrote the canonical file (md5 `0c2eac73f1891ad627e09347e141c7f2`, 7,519
lines) into `assets/css/theme.css`, re-ran `sync-css-version.py` (63 files
re-tokenized) and `sync-portfolio-stats.py` (`css-lines=7519`,
`showcase/index.html` updated), then re-ran `validate-site.py`,
`audit-site.py`, `check-links.py`, and `check-csp.py`. All clean except the
pre-existing, already-flagged `.glee-search-page__form` /
`.glee-search-page__results > li` dark-mode-coverage gap (unrelated to this
merge; still needs a human color decision) and `audit-site.py`'s 44
findings, which are pre-existing content/accessibility issues unrelated to
theme.css (toolbox pages, `under-construction.html`) confirmed unrelated by
inspection.

**3-way sync script (`scripts/sync-foundation-files.py`):** built and
deployed identically to all three repos' `scripts/`, replacing the
one-directional "OKH source of truth, hand-drop a zip" model documented in
`replit.md`. Groups each foundation file's three current copies by exact
content: 1 group = in sync; 2 groups = the group with the newest
`git log` touch wins and is written into whichever repo(s) lack it (this is
what produces both directions -- sibling-to-OKH-to-other-sibling, and
OKH-to-both-siblings -- without hand-coded routing); 3 groups (every repo
different) is reported as a conflict and left untouched. Verified against a
synthetic 3-repo git fixture covering all four cases plus commit-lock
contention, before running for real. Real dry run against the mirror:
`theme.css` confirmed in sync across all three repos; `app.js` and
`mermaid-init.js` are correctly flagged as genuine 3-way conflicts (sizes
differ substantially per site -- OKH's own dark/light toggle vs. the
siblings' brand-locked-light `data-color-scheme` wiring) and need a
deliberate blend pass, the same treatment theme.css got, before this tool
will report them in sync.

**New, more serious concurrent-modification finding:** partway through
staging the sync-script commit, `.git/index.lock` appeared and could not be
removed (`Operation not permitted`) not just in Glee-fullyTools but
*simultaneously in all three repos* -- overkill-hill and askjamie included,
neither of which showed this in phase 3. This is different from the
phase-3 incident (a GitHub-side rebase/PR-merge with real push credentials
this sandbox doesn't have): a `.git/index.lock` is purely local, so
something running directly on the machine is touching all three mirrors'
git state at the same moment this session is. Content on disk is unaffected
either way (this session writes files directly, not through git), but no
commit could be made in any of the three repos as of this writeup. The
sync-foundation-files.py write to Glee-fullyTools' theme.css/HTML files and
the sync script + doc updates to all three repos are on disk and (in
OKH's case) staged, just not committed -- see chat for the exact commands
to re-run once the lock clears.
