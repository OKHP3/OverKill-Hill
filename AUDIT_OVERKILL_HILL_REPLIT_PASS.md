# OverKill Hill P³™ — Audit Pass Report

**Date:** 2026-05-03
**Branch:** `main`
**Last commit before pass:** `edb7112` (Replit checkpoint)
**Audit prompt:** 20-phase forensic audit/repair/polish/hardening
**Scope:** All 26 production HTML pages, infrastructure files, repo docs, validation tooling

---

## Final Summary

The site entered the audit in substantially better shape than the prompt assumed. Almost every page already had: unique canonical-format `<title>`, unique 120–160 char meta description, 11 OG tags + 7 Twitter tags, JSON-LD, single `<h1>`, semantic landmarks, working skip-link, SR-only "Toggle navigation" label, no `console.log` in JS, no inline `onclick`, no placeholder hrefs.

This pass closed every gap the validation harness can detect and produced the harness itself so future regressions are caught before commit. The site is now safe to commit, push, and deploy.

---

## Files Changed

### HTML — brand consistency, security, broken-link repair
| File | Change |
|---|---|
| `index.html` | `target="_blank" rel="noopener noreferrer"` on `askjamie.bot` link; `P3` → `P³` in keywords meta |
| `404.html` | `P3` → `P³` in keywords meta |
| `under-construction.html` | `P3` → `P³` in keywords meta |
| `search/index.html` | `OKHP3 / OverKill Hill P3` → `OKHP³ / OverKill Hill P³` in keywords meta |
| `legal/index.html` | Replaced two broken AskJamie image refs (files not in repo) with existing OverKill Hill assets; subtitle reframed to cover OverKill Hill + sub-brands; static `© 2025 AskJamie™` → dynamic `© <year> OverKill Hill P³™`; footer "The OverKill Hill P³™" duplicate-The fixed |
| `universe/index.html` | `target="_blank" rel="noopener noreferrer"` on two `askjamie.bot` links; broken internal link `/projects/homestead-r/` → `/projects/hometools/` |
| `projects/index.html` | `target="_blank" rel="noopener noreferrer"` on `askjamie.bot` link; footer copyright duplicate-The fixed |
| `projects/mermaid-theme-builder/index.html` | Footer copyright duplicate-The fixed (body content untouched) |
| `writings/first-diagram-is-a-liar/index.html` | `P3` → `P³` in keywords meta |

### Infrastructure
| File | Change |
|---|---|
| `sitemap.xml` | Expanded 16 → 24 URLs (added `/found-ry/`, `/prompt-forge/`, 5 missing project pages); `<lastmod>` added to every entry |
| `prompt-forge/index.html` | Added `WebPage` JSON-LD block (was the only production page missing structured data) |

### Repository documentation
| File | Change |
|---|---|
| `README.md` | Rewritten end-to-end; replaced old tagline `Precision. Power. Presence.` with current `Precision · Protocol · Promptcraft`; added stack table, real repo layout, route inventory, validation command, editing guidance, related projects, known limitations |
| `LICENSE.md` | **Removed** (byte-identical duplicate of `LICENSE`; Phase 9 specifically called out this duplication) |
| `scripts/validate_site.py` | **New.** Full Phase 16 validation harness (see below) |
| `AUDIT_OVERKILL_HILL_REPLIT_PASS.md` | This report |

---

## Validation Commands

```bash
python3 scripts/validate_site.py
```

The harness checks every HTML page (excluding `_replit/`, `.local/`, `attached_assets/`) for:

- `<title>` present and non-empty
- meta description present and non-empty
- canonical link present
- exactly one `<h1>`
- JSON-LD structured data present
- inclusion in `sitemap.xml` (skipping `noindex` and utility pages)
- broken internal links (`/`-rooted or relative hrefs that don't resolve)
- broken asset references (CSS, JS, images, favicons, manifest)
- external `target="_blank"` links missing `rel="noopener"`
- placeholder hrefs (`""`, `"#"`, `javascript:*`)
- `P3` (without superscript) inside `<title>` or `<meta>` — brand violation
- old tagline `Precision. Power. Presence.` anywhere — brand regression

Exits 0 with no errors; 1 with any errors. Warnings don't fail the build.

## Validation Results

```
Validating 26 HTML pages…
✓ all clean.
```

Zero errors. Zero warnings. All 26 production pages pass every check.

---

## Issues Fixed (by phase)

**Phase 1 – Inventory:** Full repo scan completed. 26 production HTML pages catalogued.

**Phase 2 – Routes:** No broken internal links remained after the universe/homestead-r fix. No placeholder hrefs anywhere. No orphaned routes; no nav references missing from sitemap.

**Phase 3 – IA:** Already strong. Sitemap now matches the full nav surface (was missing 8 of 24 pages). Every page now appears in `sitemap.xml` with a `<lastmod>` date.

**Phase 4 – Brand:** All `P3` (without ³) hits removed from titles/meta. Old tagline `Precision. Power. Presence.` purged from README (was the only remaining occurrence). Duplicate "The" removed from three footer copyrights. Sub-brand mixing on legal page (AskJamie hero on OverKill Hill site) corrected.

**Phase 6 – Accessibility:** Verified existing strengths — every page has skip-link, single H1, SR-only nav-toggle label, semantic `<header>`/`<main>`/`<footer>`, language attribute, focus-visible CSS in theme. No regressions introduced.

**Phase 7 – SEO:** Sitemap now complete with `<lastmod>` per URL. Every page now carries JSON-LD (prompt-forge was the lone exception). Robots.txt verified — has explicit AI-bot opt-ins for GPTBot, ChatGPT-User, OAI-SearchBot, Google-Extended, ClaudeBot, anthropic-ai, PerplexityBot, CCBot, Applebot-Extended, Bytespider, with crawl-delay polite-mode for AhrefsBot/SemrushBot.

**Phase 9 – Security:** All 5 external `askjamie.bot` anchor links now carry `rel="noopener noreferrer"`. `LICENSE.md` duplicate removed. No secrets, no API keys, no tokens committed (verified by full repo scan).

**Phase 13 – 404 / Under-construction:** Both verified — already brand-styled with recovery links, JSON-LD, OG/Twitter cards, robots `noindex`. Keywords cleaned (`P3` → `P³`).

**Phase 14 – README:** Rewritten from 36-line marketing blurb (still carrying the obsolete tagline) to 100+ line operator's manual: stack, layout, routes, validation, editing rules, related projects, known limitations.

**Phase 16 – Validation harness:** Built `scripts/validate_site.py`, ran it, fixed every error it found, re-ran clean.

**Phase 19 – Final polish:** Validation harness now serves as the editorial polish guard going forward.

---

## Deferred Items

The following sit outside what an agent should change unilaterally on a brand site, or require infrastructure access I don't have:

1. **Soften the homepage "⚠ Active build zone" eyebrow** (`index.html` line 174). Recommendation: `"⚙ Forge in motion — actively iterated, not under construction"`. Awaiting brand-voice approval.
2. **Standardize `sales@` vs `contact@`.** `sales@overkillhill.com` appears only on the homepage; `contact@` on every other page. Confirm whether the split is intentional inbound routing.
3. **Manifest theme color.** `site.webmanifest` uses `#111827` (dark slate). Likely should align to brand espresso/teal token. Cosmetic, low-impact.
4. **CSP header.** Not currently set. Recommended starting CSP (apply via Cloudflare Transform Rules in report-only mode first):
   ```
   default-src 'self';
   script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://cdn.jsdelivr.net;
   style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
   font-src 'self' https://fonts.gstatic.com;
   img-src 'self' data: https:;
   connect-src 'self' https://www.google-analytics.com;
   frame-src https://ko-fi.com;
   ```
5. **PNG → WebP bulk conversion.** Every photo/illustration is PNG. Heaviest assets (`OverKillHillP³-Background-Wide-4096.png`, the 1536-wide hero variants) would yield meaningful LCP wins. Bulk image work — best as a separate task with `cwebp -q 82`.
6. **Header/footer deduplication.** Currently every page hand-includes the same nav and footer. A build step (Eleventy, plain Python templater, or even GitHub Actions assembling from partials) would eliminate the duplication. Out of scope for a static-site rescue pass; would change deployment topology.
7. **Twitter/X handle verification.** Meta tags use `@OverKillHillP3` — confirm this is still the live handle.
8. **Mermaid lazy rendering.** The v0.3 article renders all diagrams on load; IntersectionObserver-driven lazy rendering would defer offscreen diagrams. Performance-only, no correctness impact.

---

## Recommended Next Pass

1. **Push current changes:**
   ```bash
   git add -A
   git commit -m "audit: 20-phase forensic pass — sitemap completeness, JSON-LD, brand consistency, validation harness, broken-link repair, README rewrite"
   git push origin main
   ```
2. **Run `python3 scripts/validate_site.py` before every commit** — wire it into a pre-commit hook or GitHub Action if desired.
3. **Hostile QA pass** (the prompt-author's own recommendation): review the diff with the question "what did the agent miss?" — focused on visual rendering on real devices (which the agent cannot do) and editorial nuance.
4. **Schedule the deferred items** based on priority: (a) brand-voice decisions on items 1–3 above, (b) CSP rollout, (c) WebP bulk conversion.

## Risks Remaining

- **No automated visual regression testing.** Visual breakage on real devices wouldn't be caught by `validate_site.py`.
- **No image optimization in CI.** New large PNGs could ship without warning.
- **Header/footer hand-duplication.** A nav update touches 26 files; easy to miss one. Validator catches broken links but not editorial drift.
- **Search index (`assets/search-index.json`) is committed but not regenerated automatically.** New pages won't be searchable until the index is rebuilt and committed.

## Safe to Deploy?

**Yes.** Validator is green, no broken links, no broken assets, no brand violations in titles/meta, no insecure external links, no placeholder hrefs, no committed secrets. The only gating item is the user pressing `git push`.
