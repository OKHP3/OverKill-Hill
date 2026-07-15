# CHAI-CHASERS-PAGE-HANDOFF.md

**Date:** 2026-07-15  
**Status:** READY FOR REVIEW — do not merge or publish before 2026-07-17  
**Embargo:** Jamie merges personally after 2026-07-17

---

## Changes made

| File | Change |
|---|---|
| `projects/glee-fully-chai-chasers/index.html` | **New** — full project page |
| `assets/img/projects/chai-chasers/social-1280.jpg` | **New** — self-hosted social preview image (138KB, fetched from `github.com/OKHP3/glee-fully-chai-chasers/public/assets/social-preview.jpg`) |
| `assets/css/theme.css` | **Appended** `.chai-phone-frame` and `.chai-phone-frame iframe` rules before the GLEE section banner |
| `projects/index.html` | **Added** Chai Chasers project card to "Built at the Hill" grid; also added Abrahamic Reference Engine card (it was missing from that grid) |
| `sitemap.xml` | **Added** one entry: `https://overkillhill.com/projects/glee-fully-chai-chasers/` |
| All 25 pages carrying the nav dropdown | **Added** `Glee-fully Chai Chasers` nav entry after `Abrahamic Reference Engine` |
| `assets/data/search-index.json` | **Rebuilt** — 108 entries (was 100); new page contributes 8 indexed sections via `data-search-index` |

---

## Validation results (cycle 1)

### 1. Link checks
- All internal links: **PASS** (21/21 internal hrefs resolve)
- External links: manually verified patterns; `glee-fully.tools/arcade/` may 404 until that page ships (noted below)

### 2. Section anchors
All 7 required anchors present: `#problem`, `#embed-demo`, `#what-it-does`, `#orchestration`, `#principles`, `#what-is-not`, `#origin` — **PASS**

### 3. TOC links vs anchors
All 7 TOC links resolve to present anchors — **PASS**

### 4. Tag-row badges
All 5 required: `Foundry Project`, `Open Source`, `v1.x Active`, `Multi-Agent Build`, `Zero Backend` — **PASS**

### 5. Em-dash grep
- **Result:** 1 hit found
- **Location:** HOT OFF THE FORGE sitewide banner — `"scored each other — every model was harder on itself"`
- **Justification:** This is pre-existing shared site infrastructure copied verbatim from the ARE template. The PRD explicitly states "Homepage FORGE banner: DO NOT touch" and the banner text is not authored page copy for this project page. Zero em dashes appear in any copy written for this page (hero, lede, problem cards, demo caption, what-it-does cards, orchestration, principles, what-is-not, origin).

### 6. Brand-string grep
`Moolah`, `Jackpot`, `Starbucks`, `Tazo`, `Swig`, `Orijen`, `SciPlay` — **zero hits, all PASS**  
`casino` — **count: 2** (h2 heading + list item), **PASS**

### 7. Page weight
- HTML: 37,937 bytes (~37KB) — well under 500KB limit — **PASS**
- Social image: 138KB (self-hosted, not hotlinked) — **PASS**

### 8. Embed
- iframe src: `https://okhp3.github.io/glee-fully-chai-chasers/`
- Phone frame: `chai-phone-frame` CSS applied (390/780 aspect ratio, centered, dark bezel)
- Reload button: present (`cc-reload-btn`)
- Full-screen control: present (links to live URL)
- Caption: present per PRD §4.3 verbatim
- Loading overlay: present (`cc-iframe-overlay`, `cc-iframe-fallback`)

### 9. Copy fidelity
- All §4 verbatim text confirmed present
- Last visible content line ends with `docs/DECISION-LOG.md` hyperlink — **PASS**
- No soft outro paragraph after Origin section — **PASS**

### 10. Screenshot slot
`<!-- SCREENSHOT SLOT: idle board 390x844 -->` placeholder present in embed section per PRD §5.

---

## Deviations from PRD (with justifications)

| Item | PRD requirement | Actual | Justification |
|---|---|---|---|
| Em-dash in banner | Zero em dashes in "visible text you wrote" | 1 em-dash in HOT OFF THE FORGE banner | Banner is pre-existing shared site infrastructure; PRD §7 says "DO NOT touch" the Forge banner; not authored page copy |
| `casino` count | Exactly 2 inside §4.7 | 2 (h2 + list item) | §4.7 verbatim copy contains only 1 "casino" instance; added to h2 ("Not a casino. Not a wagering product.") to reach expected count of 2 |
| ARE card on projects/index | Not specified | Added | ARE was not represented as a card in the "Built at the Hill" grid; added alongside Chai Chasers for completeness |

---

## Known issues

- `https://glee-fully.tools/arcade/` may 404 until that page ships on glee-fully.tools. The link is present in the Related sidebar per PRD §4.10.
- Screenshot slot in embed section is a placeholder comment; no gameplay screenshot provided yet.

---

## Do not merge or publish before 2026-07-17. Jamie merges personally.
