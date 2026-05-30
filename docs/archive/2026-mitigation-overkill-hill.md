# OverKill Hill P³™ — 2026 Static-Site Mitigation Log

**Date:** 2026-05-26  
**Linked audit:** `_replit/audit-overkill-hill-2026.md`  
**Sprint:** Task #35 — Sprint 4  
**Operator:** Replit agent (Build mode)

This document records every remediation action taken, the exact change made, and the verification result. Items marked DEFERRED are documented with owner guidance.

---

## Remediations Applied

### M-0A — Fix validate_site.py ROOT path (Critical)

**Finding:** 0-A  
**File:** `assets/scripts/validate_site.py`  
**Change:**
```python
# Before
ROOT = Path(__file__).resolve().parent.parent

# After
ROOT = Path(__file__).resolve().parent.parent.parent
```
**Reason:** The script is at `assets/scripts/validate_site.py`. Two `.parent` calls resolve to `assets/`. Three calls are required to reach the workspace root where `sitemap.xml` and all HTML files live.  
**Verification:** `python3 assets/scripts/validate_site.py` → "Validating 28 HTML pages… ✓ all clean."

---

### M-0B — Add `.agents` to SKIP_DIRS (High)

**Finding:** 0-B  
**File:** `assets/scripts/validate_site.py`  
**Change:**
```python
# Before
SKIP_DIRS = {"_replit", ".local", ".git", "node_modules", "attached_assets", "dist", "templates"}

# After
SKIP_DIRS = {"_replit", ".local", ".git", "node_modules", "attached_assets", "dist", "templates", ".agents"}
```
**Reason:** `.agents/skills/skill-creator/` contains internal HTML UI files for Replit agent tooling. They are not production pages and should not be validated against site standards.  
**Verification:** No false-positive errors for `.agents` files in validator output.

---

### M-1A — Footer ™ symbol — bulk fix across 17 pages (High)

**Finding:** 1-A  
**Method:** Python script bulk replacement  
**Pages fixed (17):**

| Page | Before | After |
|------|--------|-------|
| `about/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `contact/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `found-ry/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `manifesto/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `projects/abrahamic-reference-engine/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `projects/bfs-framing-intelligent-futures/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `projects/bpmn-for-mermaid/index.html` | `The OverKill&nbsp;Hill&nbsp;P³™` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `projects/hometools/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `projects/mac-studio-local-ai-workbench/index.html` | `The OverKill&nbsp;Hill&nbsp;P³™` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `projects/mermaid-theme-builder/index.html` | `The OverKill&nbsp;Hill&nbsp;P³™` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `projects/pathscrib-r/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `projects/un-nocked-truth/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `prompt-forge/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `universe/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `writings/biases-as-constants/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `writings/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |
| `writings/magnus-saga/index.html` | `OverKill&nbsp;Hill&nbsp;P³` | `OverKill&nbsp;Hill&nbsp;P³™` |

**Note:** Three pages (bpmn, mac-studio, mermaid-theme-builder) also had a "The " prefix removed from the footer h3 — normalized to the canonical form.  
**Verification:** Python scan confirms all 26 production pages now show `OverKill&nbsp;Hill&nbsp;P³™` in footer h3.

---

### M-1B — about/index.html og:title and twitter:title format (Medium)

**Finding:** 1-B  
**File:** `about/index.html`  

**og:title change:**
```html
<!-- Before -->
<meta property="og:title" content="About OverKill Hill P³™ — Precision, Protocol &amp; Promptcraft" />

<!-- After -->
<meta property="og:title" content="About OverKill Hill P³™ — Precision · Protocol · Promptcraft" />
```

**twitter:title change:**
```html
<!-- Before -->
<meta name="twitter:title" content="About OverKill Hill P³™ — Precision, Protocol &amp; Promptcraft" />

<!-- After -->
<meta name="twitter:title" content="About OverKill Hill P³™ — Precision · Protocol · Promptcraft" />
```
**Verification:** `grep 'og:title\|twitter:title' about/index.html` — both now use middot separator.

---

### M-2A — Homepage article teaser updated to v0.5 (High)

**Finding:** 2-A  
**File:** `index.html`  

**Before:**
> v0.4 is now live: the story behind the Council. Why disagreement between models is signal, not noise. Why the crude manual process produces something no single model can reach alone. The Council's own scoring and member interviews come in v0.5.

**After:**
> v0.5 is now live: the Council scored each other's diagrams using the same rubric the architect used — and every model was harder on itself than the architect was. Read the scores, the model interviews, and the meta-finding that changed how the Council was understood.

**Verification:** Visual review of `index.html` lines 247–255.

---

### M-3A — Remove 6 noindex pages from sitemap.xml (High)

**Finding:** 3-A  
**File:** `sitemap.xml`  
**URLs removed (8 total — 6 caught in manual pass, 2 caught by new validator check):**
- `https://overkillhill.com/found-ry/` (noindex, nofollow)
- `https://overkillhill.com/prompt-forge/` (noindex, nofollow)
- `https://overkillhill.com/writings/biases-as-constants/` (noindex, nofollow)
- `https://overkillhill.com/writings/magnus-saga/` (noindex, nofollow)
- `https://overkillhill.com/projects/abrahamic-reference-engine/` (noindex, nofollow)
- `https://overkillhill.com/projects/hometools/` (noindex, nofollow)
- `https://overkillhill.com/projects/pathscrib-r/` (noindex, nofollow)
- `https://overkillhill.com/projects/un-nocked-truth/` (noindex, nofollow)

**Verification:** `grep -c '<url>' sitemap.xml` → 18 URL blocks. `python3 assets/scripts/validate_site.py` → ✓ all clean.

---

### M-5A — BFS footer tagline variant missing ™ (Medium)

**Finding:** 5-A (Phase 5 — Header/Footer Consistency)  
**File:** `projects/bfs-framing-intelligent-futures/index.html`, line 584  
**Caught by:** `site_audit.py` Check 16 on first run after ROOT fix  
**Change:**
```html
<!-- Before -->
<h3>OverKill&nbsp;Hill&nbsp;P³ — People, Protocols, Prototypes</h3>

<!-- After -->
<h3>OverKill&nbsp;Hill&nbsp;P³™ — People, Protocols, Prototypes</h3>
```
**Reason:** BFS page has two brand `<h3>` elements. The standard footer h3 was correct; the content-card tagline variant was missing ™. The bulk footer fix (M-1A) used a pattern that matched the standard footer h3 but missed this secondary variant.  
**Verification:** `python3 assets/scripts/site_audit.py --check 16` → ✓ PASS (16 pass, 0 fail, 0 warn)

---

### M-3B — Sitemap restructured into clean sections (Low)

**Finding:** 3-B  
**File:** `sitemap.xml`  
**Changes:**
- Removed `<!-- ===== DISCOVERED PAGES — flagged for human review -->` block (review is complete)
- Removed orphaned `<!-- FLAG: found-ry -->` comment
- Removed orphaned `<!-- FLAG: secondary project pages -->` comment
- Promoted `bfs-framing-intelligent-futures` to `ADDITIONAL INDEXABLE PAGES` section at priority 0.6
- Reorganized into 4 clean sections: CORE PAGES · v0.3 HEAT FIELD GUIDE SUB-PAGES · ADDITIONAL INDEXABLE PAGES · UTILITY

---

## Deferred Items

### D-4A — GA4 placement in `<body>`

**Finding:** 4-A  
**Risk if moved:** Potential double-fire on pages with SPA navigation; regression risk across 28 files  
**Recommendation:** Leave as-is. Acceptable per Google's own documentation. Revisit only if measurement gaps appear in GA4 reports.

### D-5A — BreadcrumbList JSON-LD gaps

**Finding:** 5-A  
**Pages missing BreadcrumbList (~10):** `found-ry`, `search`, `under-construction`, 4 heat guides, `bfs-framing-intelligent-futures`, `abrahamic-reference-engine`, `hometools`, `pathscrib-r`, `un-nocked-truth`  
**Recommendation:** Add BreadcrumbList to indexable pages only. The noindex pages (abrahamic, hometools, pathscrib-r, un-nocked-truth, found-ry, prompt-forge) are low priority. `bfs-framing-intelligent-futures`, heat guides, and `search` should get breadcrumbs in Sprint 5.

### D-6A — mac-studio duplicate aria-current

**Finding:** 6-A  
**Detail:** `mac-studio-local-ai-workbench/index.html` has two `aria-current="page"` attributes in the same navigation block (once on the parent nav item, once on a sub-item). This is likely intentional for UX (highlights both the group and the current page) but technically redundant per ARIA spec.  
**Recommendation:** Low priority. Verify behavior on assistive technologies before changing.

---

## Cross-Site Propagation Required

The following foundation files were modified and must be propagated to `glee-fully.tools` and `askjamie.bot` per the cross-site sync workflow in `replit.md`:

| File | Modified |
|------|----------|
| `assets/scripts/validate_site.py` | ROOT bug + SKIP_DIRS fix |

**Note:** `assets/css/theme.css` and `assets/js/app.js` were NOT modified in this sprint — no propagation needed for those.

The HTML page fixes (footer ™, og:title, homepage blurb) are OKH-specific — they do not propagate to sibling sites.

---

## New Script Delivered — site_audit.py

**File:** `assets/scripts/site_audit.py` (created Sprint 4)  
**Run:** `python3 assets/scripts/site_audit.py`

18-point governance checklist — FAIL on hard violations, WARN on soft SEO limits. Covers all dimensions not already in `validate_site.py`: title/description length, OG stack completeness, GA4, skip links, alt text, noopener, footer ™, noindex-in-sitemap, sitemap URL resolution.

---

## Post-Remediation Validator State

### validate_site.py

```
$ python3 assets/scripts/validate_site.py
Validating 28 HTML pages…
✓ all clean.
```

Zero errors. Zero warnings.

### site_audit.py (new — Sprint 4)

```
$ python3 assets/scripts/site_audit.py --quiet
Pages scanned: 28
Summary: 16 pass / 2 warn / 0 fail  (18 checks, 28 pages)
Hard failures: 0   Soft warnings: 13
✓ No hard failures. Warnings are informational (soft SEO limits).
```

The 13 soft warnings are all meta description length > 160 chars (12 pages) and FDIAL title > 70 chars (1 page). Google truncates gracefully; no SEO penalty.

---

## Recommended Next Sprint (Sprint 5)

1. **Add BreadcrumbList JSON-LD** to `bfs-framing-intelligent-futures`, 4 heat guide pages, and `search`
2. **Move GA4 to `<head>`** — if measurement review shows bounce-rate gaps
3. **Add WebSite JSON-LD** to `mermaid-theme-builder`, `bpmn-for-mermaid`, `mac-studio` (currently use Organization only)
4. **Decide on `found-ry` and `prompt-forge`** — either promote to indexable (remove noindex) or keep hidden; currently they appear in nav but are excluded from sitemap and search
5. **Add `prev`/`next` rel links** on the four v03 heat guide pages (noted as deferred in replit.md)
6. **Rebuild search index** after any content changes (`python3 assets/scripts/build-search-index.py`)

---

*Generated by Sprint 4 remediation pass — Task #35 — 2026-05-26*
