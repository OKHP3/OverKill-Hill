# Cross-Repo Sync — `overkillhill.com` ↔ `glee-fully.tools` ↔ `askjamie.bot`

**Generated:** 2026-05-02
**Source of truth:** [`OKHP3/OverKill-Hill`](https://github.com/OKHP3/OverKill-Hill)
**Targets:** [`OKHP3/Glee-fullyTools`](https://github.com/OKHP3/Glee-fullyTools), [`OKHP3/AskJamie`](https://github.com/OKHP3/AskJamie)

This drop contains the canonical foundational files for the three sibling sites. The intent (per the original design) is that **`assets/css/theme.css`, `assets/js/app.js`, and `assets/js/mermaid-init.js` are byte-identical across all three repositories**, with site-specific styling driven by class hooks already present in the shared CSS (`.glee-main`, `.askjamie-main`, `body:not(.glee-main):not(.askjamie-main)`).

---

## What's in this drop

```
dist/sync/
├── MIGRATION.md                    ← this file
├── glee/
│   └── assets/
│       ├── css/theme.css           ← drop into Glee-fullyTools/assets/css/
│       └── js/
│           ├── app.js              ← drop into Glee-fullyTools/assets/js/
│           └── mermaid-init.js     ← drop into Glee-fullyTools/assets/js/
└── askjamie/
    └── assets/
        ├── css/theme.css           ← drop into AskJamie/assets/css/
        └── js/
            ├── app.js              ← drop into AskJamie/assets/js/
            └── mermaid-init.js     ← drop into AskJamie/assets/js/
```

Both sibling subtrees contain **identical** files. They're staged separately so each can be committed/pushed to its own repo without confusion.

---

## What changed vs. the live `main` branches

### `mermaid-init.js` — Already aligned

Code was byte-identical across all three repos. Only line 1 (the brand comment) differed. Updated to a neutral cross-site header so the file can ship verbatim to all three:

```js
// Mermaid initialization — shared module across overkillhill.com,
// glee-fully.tools, and askjamie.bot.
```

**Glee impact:** comment-only change.
**AskJamie impact:** comment-only change (the existing comment incorrectly said "OverKill Hill P³" — it had been copied without updating the brand label).

### `app.js` — OKH was already the canonical source

| Repo | What's missing | Lines |
|---|---|---:|
| **Glee** | The entire **Sticky TOC scroll-follow** module (lerp-smoothed scroll position for `#toc-widget` on ≥1024px viewports) | +57 |
| **AskJamie** | Has the Sticky TOC module, but an older revision: missing inline-comment documentation and a buggier `resize` handler that always cleared the transform before re-checking width | +5 (refresh) |

**Behavior change for Glee:** the Sticky TOC will now smoothly track scroll position on article-style pages that include `#toc-widget`. If Glee doesn't currently have a TOC widget on any page, the module is a no-op (`return` on missing element).

**Behavior change for AskJamie:** the resize handler now branches cleanly — clears the transform when dropping below 1024px, recomputes natural top + height when staying above. Functionally tighter, no visible change in the common case.

### `theme.css` — Selective merge into OKH, then OKH ships everywhere

**Newly added to canonical (OKH absorbed from siblings):**

A `SHARED UTILITIES` section just before `HEADER & NAV` containing both the Glee margin convention (`.mt-1/2/3/4/075`) and the AskJamie convention (`.u-mt-sm/md/lg/xl`, `.u-flex-center`, `.u-opacity-90`, `.img-fluid`, `.img-constrained`). Both naming conventions are supported as aliases so existing markup in any of the three repos keeps working without churn.

> **Transitional, not permanent.** Shipping two naming systems is an explicit migration aid, not a long-term policy. Pick one canonical convention before any new pages get written:
>
> - **Recommended canonical:** `.u-mt-*` namespaced utilities (the AskJamie convention). Rationale: the `u-` prefix makes utilities visually distinct from semantic component classes (e.g., `.mt-3` reads like "milestone target 3"; `.u-mt-md` is unambiguously a utility). This matches the convention used by Tachyons / utility-first systems.
> - **Migration path:** in a future sync, run a codemod across all three repos to rewrite `.mt-1 → .u-mt-sm`, `.mt-2 → .u-mt-md`, `.mt-3 → .u-mt-lg`, `.mt-4 → .u-mt-xl`, `.mt-075 → .u-mt-sm` (or introduce `.u-mt-xs`). Then drop the short-form aliases from `theme.css` in the cycle after that.

**Deliberately NOT migrated from siblings (dead code):**

```css
body[data-theme="dark"] { … }
body[data-theme="light"] { … }
```

These rules existed in both Glee's and AskJamie's `theme.css` but **never matched anything**. The shared `app.js` sets `data-theme` on the `<html>` element (`document.documentElement.setAttribute(…)`), not on `<body>`. OKH already handles body backgrounds correctly via `html[data-theme="…"] body { … }` (lines 64–70 in canonical theme.css), so these dead rules are dropped on the way in.

**Net OKH additions (which both siblings will gain):**
- Full v0.3 article styling: `.article-hero`, `.article-meta`, `.article-changelog`, `.article-body-section`, `.bracket-heats`, `.council-table`, `.diagram-card`, `.diagram-grid`, `.heat-actions`, `.heat-competitors`, `.diagram-source-link`, `.download-options`, `.artifact-stack`, `.scorecard`, `.toc-list`, `.mermaid-referral-link`, etc.
- Most of these selectors are namespaced (`.article-*`) and inert on pages that don't use article markup.
- **⚠ However**, several class names are *not* namespaced and would apply to any element using them, regardless of site: `.diagram-card`, `.diagram-grid`, `.download-options`, `.scorecard`, `.toc-list`, `.heat-actions`, `.heat-competitors`. **Before propagating to a sibling repo, search that repo for these class names** to confirm there's no accidental collision. If you find one, either rename the colliding markup in the sibling, or wrap the OKH rule in a `.article-body` parent selector before re-syncing.

```bash
# Run inside each sibling clone before applying this drop:
for cls in diagram-card diagram-grid download-options scorecard toc-list heat-actions heat-competitors; do
  echo "=== .${cls} ==="
  grep -rn "\"${cls}\"\\|'${cls}'\\|class=\\\"[^\\\"]*\\b${cls}\\b" --include="*.html" . 2>/dev/null
done
```

If every block is silent, the drop is safe to apply as-is.

---

## How to apply this drop

For each sibling repo, in order:

### Glee-fullyTools
```bash
# from the root of the Glee-fullyTools clone
cp /path/to/dist/sync/glee/assets/css/theme.css       assets/css/theme.css
cp /path/to/dist/sync/glee/assets/js/app.js           assets/js/app.js
cp /path/to/dist/sync/glee/assets/js/mermaid-init.js  assets/js/mermaid-init.js

git add assets/css/theme.css assets/js/app.js assets/js/mermaid-init.js
git commit -m "chore(sync): align foundation files with overkillhill.com canonical (2026-05-02)"
git push
```

### AskJamie
```bash
# from the root of the AskJamie clone
cp /path/to/dist/sync/askjamie/assets/css/theme.css       assets/css/theme.css
cp /path/to/dist/sync/askjamie/assets/js/app.js           assets/js/app.js
cp /path/to/dist/sync/askjamie/assets/js/mermaid-init.js  assets/js/mermaid-init.js

git add assets/css/theme.css assets/js/app.js assets/js/mermaid-init.js
git commit -m "chore(sync): align foundation files with overkillhill.com canonical (2026-05-02)"
git push
```

---

## Verification after applying

After pushing both sibling repos, this single command will confirm homeostasis:

```bash
for repo in OverKill-Hill Glee-fullyTools AskJamie; do
  for f in assets/css/theme.css assets/js/app.js assets/js/mermaid-init.js; do
    sha=$(curl -sL "https://raw.githubusercontent.com/OKHP3/$repo/main/$f" | sha256sum | cut -c1-12)
    printf "%-20s %-30s %s\n" "$repo" "$f" "$sha"
  done
done
```

All three SHA columns for each filename should match. If they don't, something else committed to that repo between staging and applying.

---

## Going forward — preventing drift

Three options, in order of effort vs. robustness:

1. **Keep the manual copy-out workflow** (current). Make changes in OKH, run a small `sync.sh` that scp's the three files to the other two repos, commit with `chore(sync): align foundation files`. Cheap. Drifts again the moment you forget.

2. **Single-source via git submodule.** Move the three files into a tiny `OKHP3/web-foundations` repo. The three site repos add it as a submodule under `assets/_shared/`. Each site's HTML references `assets/_shared/css/theme.css`. Updating once propagates after a `git submodule update --remote` in each site. Mid-effort, eliminates drift.

3. **GitHub Actions cross-repo sync.** A workflow on the OKH repo that, on push to `main` touching any of these three paths, opens a PR in the other two repos with the updated files. Highest setup cost (needs a PAT or GitHub App), highest robustness, zero manual steps after configuration.

I'd recommend **option 2** if you have any other planned shared assets (images, fonts, JSON-LD partials) — the foundation will only grow. Option 3 is the "set it and forget it" answer if you want the sibling repos to feel autonomous.
