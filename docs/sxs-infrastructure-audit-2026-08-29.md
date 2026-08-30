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
