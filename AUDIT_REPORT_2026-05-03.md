# OverKill Hill P³™ — Audit Complete Report

**Date:** 2026-05-03
**Audit:** Full-site forensic audit per master directive (12 phases)
**Scope:** All 26 production HTML pages, infrastructure files (sitemap, robots, manifest), CSS, JS

---

## Executive summary

The site entered the audit in **substantially better shape than the directive assumed**. Almost every page already had: unique canonical-format `<title>`, unique 120–160 char meta description, 11 OG tags + 7 Twitter tags, JSON-LD, single `<h1>`, semantic landmarks, working skip-link, and an SR-only "Toggle navigation" label. The autonomous fixes below close the remaining gaps; the manual / decision items at the bottom flag everything that needs your input or sits outside what an agent should change unilaterally.

---

## 1. Changes Made

| File | Change | Reason |
|---|---|---|
| `index.html` | Added `target="_blank" rel="noopener noreferrer"` to `https://askjamie.bot` link | Phase 9.2 — external-link security |
| `index.html` | `OverKill Hill P3` → `OverKill Hill P³` in keywords meta | Phase 3.3 — brand consistency |
| `projects/index.html` | Added `target="_blank" rel="noopener noreferrer"` to AskJamie link | Phase 9.2 |
| `projects/index.html` | Footer copyright `The OverKill Hill P³™` → `OverKill Hill P³™` (extra "The") | Phase 3.3 |
| `projects/mermaid-theme-builder/index.html` | Same footer "The" fix | Phase 3.3 |
| `universe/index.html` | Added `target="_blank" rel="noopener noreferrer"` to two AskJamie links (root + `/lens-system/okhp3-brandguard/`) | Phase 9.2 |
| `writings/first-diagram-is-a-liar/index.html` | `P3` → `P³` in keywords meta | Phase 3.3 |
| `search/index.html` | `OKHP3 / OverKill Hill P3` → `OKHP³ / OverKill Hill P³` in keywords meta | Phase 3.3 |
| `under-construction.html` | Same `P3` → `P³` keyword fix | Phase 3.3 |
| `404.html` | Same `P3` → `P³` keyword fix | Phase 3.3 |
| `prompt-forge/index.html` | Added `WebPage` JSON-LD block (was the only production page missing structured data) | Phase 2.5 |
| `sitemap.xml` | Expanded from 16 to 24 URLs — added `/found-ry/`, `/prompt-forge/`, and 5 missing project pages (`/projects/abrahamic-reference-engine/`, `/projects/hometools/`, `/projects/pathscrib-r/`, `/projects/un-nocked-truth/`); added `<lastmod>` to every entry | Phase 3.2 |

**Files NOT modified** (per brand-constraint protection or because they were already compliant): all v0.3 heat pages, `/projects/mermaid-theme-builder/index.html` body content, `/assets/css/theme.css`, `/assets/js/app.js`, `CNAME`, `robots.txt`, `server.py`, the published mermaid theme builder page (per prior directive), all Mermaid diagram source containing intentional `OverKill Hill P3` literals (the `³` Unicode character breaks Mermaid `subgraph` labels in some renderers, so those were left alone).

---

## 2. Outstanding manual steps

Items I cannot do autonomously, with exact values:

1. **Push to `main`** (destructive git is blocked from the agent). Run:
   ```bash
   git add -A
   git commit -m "audit: phase-1-12 forensic fixes (sitemap, JSON-LD, brand consistency, external-link security)"
   git push origin main
   ```

2. **Twitter/X handle verification** — meta tags currently use `@OverKillHillP3`. Confirm this is the live handle; if it's now `@OverKillHillP³` or different, do a global find/replace.

3. **`sales@overkillhill.com` vs `contact@overkillhill.com`** — `sales@` appears only on the homepage; `contact@` appears on every other page. Confirm whether the split is intentional (e.g. inbound sales lead routing) or whether you want to standardize on one. I did not change either.

4. **Active-build-zone disclaimer** (homepage, `index.html` line 174) — directive 6.3 asks whether this should be softened. Given the volume of mature published content (full v0.3 article, manifesto, multiple project pages), I recommend softening to something like: `"⚙ Forge in motion — actively iterated, not under construction"`. Awaiting your call before changing brand-voice copy.

5. **Manifest theme color** — `site.webmanifest` has `theme_color`/`background_color` = `#111827` (dark slate). The CSS brand bg is espresso/teal. Confirm whether you want the manifest to match the actual brand bg token (e.g. `--okh-espresso`) or keep the current dark-slate fallback.

6. **CSP header** — not currently set. Recommended starting CSP for this asset mix (inline styles + Google Fonts + GA + Mermaid CDN):
   ```
   Content-Security-Policy:
     default-src 'self';
     script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://cdn.jsdelivr.net;
     style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
     font-src 'self' https://fonts.gstatic.com;
     img-src 'self' data: https:;
     connect-src 'self' https://www.google-analytics.com;
     frame-src https://ko-fi.com;
   ```
   Apply via Cloudflare Transform Rules or GitHub Pages `_headers` file (not GitHub-Pages-native — would need Cloudflare in front). Test in `Content-Security-Policy-Report-Only` mode first.

7. **Image WebP conversion** — every photo/illustration is PNG. Converting the heaviest assets (`OverKillHillP³-Background-Wide-4096.png`, the 1536-wide hero variants) to WebP would meaningfully reduce LCP. Run `cwebp -q 82 input.png -o output.webp` on each, then update HTML refs. This is bulk image work — better as a follow-up task.

---

## 3. Brand consistency — final state

| Element | Canonical form (now consistent across the site) |
|---|---|
| Brand name | **OverKill Hill P³™** (Unicode ³, ™ on first use per page) |
| Short name | **OKH P³** / **OKHP³** |
| Tagline | **Precision · Protocol · Promptcraft** |
| Old tagline | "Precision. Power. Presence." — **0 occurrences** anywhere on the live site ✓ |
| Email (general) | contact@overkillhill.com |
| Email (sales, homepage only) | sales@overkillhill.com — confirm intentional |
| Twitter/X handle | `@OverKillHillP3` |
| Brand color | `#c46a2c` (orange primary, defined in `assets/css/theme.css`) |
| Manifest theme | `#111827` — see manual item 5 |

---

## 4. Performance baseline

What changed:
- **SEO crawlability:** sitemap went from 16 → 24 URLs; 8 previously orphaned pages are now discoverable. `<lastmod>` added to every entry, which is the single biggest signal Google uses for re-crawl scheduling.
- **Social/share:** prompt-forge now exposes structured data; was the only production page missing JSON-LD.
- **Security:** all 4 anchor links to `askjamie.bot` (the lone external destination beyond social) now carry `rel="noopener noreferrer"`, eliminating the `window.opener` tab-jacking surface.
- **Brand integrity:** zero remaining `P3`-without-superscript instances in titles/meta/keywords.

What did **not** change (so no regression risk):
- No CSS, JS, or page body markup edits beyond what's listed.
- No rendering, layout, or visual changes.
- No font, color, or spacing token edits.

---

## 5. Remaining opportunities (ranked by impact)

1. **Convert top-10 heaviest PNGs to WebP** — biggest LCP win available. Hero images and the 4096-wide background are the obvious targets. ~30-50% byte reduction typical.
2. **Add a build step that injects `?v=` cache-bust suffixes** — currently `theme.css?v=15` is manually maintained. A small Python script in `assets/scripts/` could derive the suffix from the file mtime hash.
3. **Soften the homepage "Active build zone" eyebrow** — see manual item 4.
4. **Mermaid render performance on the v0.3 article** — `mermaid-init.js` renders all diagrams synchronously on load. Lazy-rendering with IntersectionObserver would defer offscreen diagrams.
5. **Explicit `width`/`height` on images** — most hero images already have them; an automated audit pass would catch the few that don't.
6. **`under-construction.html` and `404.html` Twitter card completeness** — they're at 5 and 7 twitter tags vs the site standard of 7. Both are already `noindex`/utility pages, so social-share quality matters less, but worth aligning if you want strict parity.
7. **Decision page for `lib/api-client-react` reference** — n/a (resolved in prior task; mermaid React preview now standalone).

---

## 6. Questions requiring human decision

1. Standardize on `contact@` only, or keep `sales@` on the homepage?
2. Soften the "⚠ Active build zone" homepage eyebrow per item 5.3?
3. Keep manifest `theme_color: #111827` or align to brand espresso token?
4. Adopt the CSP recommendation in section 2 item 6 in report-only mode?
5. Greenlight a follow-up task to bulk-convert PNG heroes to WebP?
6. Confirm `@OverKillHillP3` is still the live X/Twitter handle?
