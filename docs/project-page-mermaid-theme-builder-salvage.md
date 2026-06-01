# Salvage Doc — Mermaid Theme Builder Project Page

**Created:** May 2026  
**Task:** #78 — Sync MTB project page to v0.5.0 + SKILL.md Hardening state  
**Purpose:** Authority order, donor inspection notes, and pre-edit audit record

---

## Donor Availability

| Source | Status | Notes |
|---|---|---|
| Legacy Donor Replit (`Project-Page-Mermaid-Theme-Tool`) | **Inaccessible** — external Repl URL, not available from this repo | Could not be read; treated as unavailable |
| Current production page (`projects/mermaid-theme-builder/index.html`) | **Available** | Primary working surface |
| Theme Builder GitHub Pages app (`okhp3.github.io/mermaid-theme-builder/`) | **Available** (public) | Used to verify live tool state |
| Theme Builder GitHub repo README | **Available** (public) | Used for feature/version reference |
| Task #78 brief (`/.local/tasks/task-78.md`) | **Available** | Used as specification proxy |

**Authority order used:**
1. `assets/css/theme.css` — canonical design tokens and component classes
2. Task #78 brief — specification proxy for content, structure, and copy
3. Current production page — structural anchor (preserve what's correct)
4. Theme Builder GitHub Pages app + README — ground truth for feature/version claims

---

## Pre-Edit State Audit

### Forbidden strings found in production page before edit

| String | Line | Disposition |
|---|---|---|
| `v0.5.x Alpha Active` (hero badge) | 967 | Changed to `v0.5.0 Shipped` |
| `v0.5.x Alpha Active` (sidebar status) | 1741 | Changed to `v0.5.0 Shipped` |

### Strings confirmed absent (pre-edit)

- `Trust Sprint` — not present
- `V0.3 to V0.5 Active` — not present
- `v10, v11+` — not present (sidebar says `v11.15.0`)
- `v10 and v11` — not present
- `picard.replit.dev` — not present
- `BFS` — not present
- `seamlessly` / `robust` / `powerful` / `effortlessly` / `elevate` / `unleash` — not present

### Section inventory — pre-edit

| Section | ID | Present pre-edit | Status |
|---|---|---|---|
| Embed tool iframe | `#embed-tool` | ✓ | src missing `?embed=1` |
| Current Release card | `#release` | ✓ | Correct |
| What It Is | `#what-it-is` | ✓ | Correct |
| Why This Exists | `#why-this-exists` | ✓ | Correct |
| What Changed since v0.3 | `#since-v03` | ✓ | Correct |
| Features grid | `#features` | ✓ | 16 cards — removed 1 |
| Relationships | *(no id)* | ✓ | Correct |
| Diagram Family Taxonomy | *(no id)* | ✓ | Correct (support taxonomy) |
| Renderer Awareness | *(no id)* | ✓ | Updated to bullet structure |
| SKILL.md agent skill | *(no id)* | ✓ | Added install examples |
| Mobile companion | *(no id)* | ✓ | Correct |
| Roadmap / Build History | `#roadmap` | ✓ | 6 entries — expanded to 10 |
| FAQ | *(collapsible)* | ✓ | 8 Q&As — expanded to 11 |
| Builder's note | *(no id)* | ✓ | Correct |
| Development update | *(no id)* | ✓ | Updated text |
| Sidebar — Start Now | *(sidebar)* | ✓ | Correct |
| Sidebar — Project Info | *(sidebar)* | ✓ | Status updated; Compat row added |
| Sidebar — Related Resources | *(sidebar)* | ✓ | SKILL.md + Apply tab added |

### check-mtb-version.py state — pre-edit

All 11 version-string checks passed before edit. The script expected `{sp} Alpha Active`
for the hero tag and sidebar status. These patterns were updated in the script to match
the new `{v} Shipped` convention, keeping all 11 checks passing post-edit.

---

## Changes Applied

### HTML page (`projects/mermaid-theme-builder/index.html`)

1. **Hero badges**: `v0.5.x Alpha Active` → `v0.5.0 Shipped` + added `SKILL.md Sprint Active`
2. **Hero CTA**: "Sibling: BPMN for Mermaid" → "BPMN for Mermaid"
3. **Iframe src**: added `?embed=1` parameter
4. **Feature grid**: removed `Forge UI System` card (implementation-detail card, 16→15)
5. **Build history**: added V0.1–V0.4 as Shipped entries (6→10 total phases)
6. **FAQ**: added SKILL.md Q&A, BPMN sibling Q&A, Mermaid Chart disaffiliation Q&A (8→11)
7. **SKILL.md section**: added Claude Code / Cursor / Copilot / VS Code install code blocks
8. **Renderer awareness**: converted prose-only to prose + bulleted key points
9. **Development update**: updated to v0.5.0 baseline + SKILL.md hardening context (May 2026)
10. **Sidebar Status**: `v0.5.x Alpha Active` → `v0.5.0 Shipped`
11. **Sidebar**: added `Compatibility` meta row (`Renderer-dependent v10/v11 portability`); added SKILL.md source and Apply tab links to Related Resources

### Script (`scripts/check-mtb-version.py`)

- `EXPECTED["hero tag"]`: updated from `f"{sp} Alpha Active"` to `f"{v} Shipped"`
- `EXPECTED["sidebar · Status meta-val"]`: updated from `f"{sp} Alpha Active"` to `f"{v} Shipped"`
- `REPLACEMENTS["hero tag"]`: updated regex from `Alpha Active` to `Shipped`, capture groups adjusted
- `REPLACEMENTS["sidebar · Status meta-val"]`: updated regex from `Alpha Active` to `Shipped`
