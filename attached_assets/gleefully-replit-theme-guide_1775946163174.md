# Glee-fully Personalizable Tools™ — Replit App Theme

Reverse-engineered from `assets/css/theme.css` (`.glee-main` overrides).
Enter these values into the **Manage app themes** panel field by field.

---

## FOUNDATION — Colors

| Field | Value | Notes |
|---|---|---|
| Background color | `#f6f2ee` | OKH Paper — the warm cream page canvas |
| Text color | `#2e2b29` | Rich espresso — primary readable text |
| Muted background color | `#fdfbf7` | Lightest paper surface — cards and panels |
| Muted text color | `#6b6b6b` | Warm gray — subdued/secondary text |

---

## FOUNDATION — Typography

| Field | Value | Notes |
|---|---|---|
| Sans-serif font | `DM Sans` | Primary body font — loaded from Google Fonts |
| Serif font | `Georgia` | No serif used in this design; nearest universal fallback |
| Monospace font | `Menlo` | No monospace in this design; browser/system default |

> **Note on fonts:** The site uses a two-font display system:
> - **Fredoka** — playful rounded display font for H1/H2 headings on branch/twig pages
> - **DM Sans** — clean, modern body text throughout
>
> Both are Google Fonts. Load them via:
> ```
> https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=DM+Sans:wght@400;500;600&display=swap
> ```
> If the Replit theme panel does not list Fredoka or DM Sans by name, select **Poppins** (headings) and **Open Sans** (body) as the closest available substitutes.

---

## FOUNDATION — Shape & Spacing

| Field | Value | Notes |
|---|---|---|
| Border radius | `0.75` rem | Standard card/component radius (`--radius-md`). Buttons use 999px pills. |

---

## COMPONENTS — Actions

| Field | Value | Notes |
|---|---|---|
| Primary background | `#d35b2d` | Glee Rust — primary CTA, active nav underline start |
| Primary text | `#0f172a` | Dark ink — high contrast on rust/orange |
| Secondary background | `#2a2320` | OKH Espresso — dark complement surface |
| Secondary text | `#f6f2ee` | Paper — readable on espresso |
| Accent background | `#f3b932` | Glee Gold — nav underline end, highlight colour |
| Accent text | `#2e2b29` | Espresso — dark text on gold |
| Destructive background | `#d94f63` | Coral-red — used in the site CSS for error states |
| Destructive text | `#ffffff` | White — readable on coral |

> **Primary CTA gradient** (used on `.btn-primary`):
> `linear-gradient(90deg, #d35b2d, #f3b932)` — Glee Rust → Glee Gold

---

## COMPONENTS — Forms

| Field | Value | Notes |
|---|---|---|
| Input | `#fdfbf7` | Lightest paper surface — inputs blend into page |
| Border | `#d7d7d7` | Soft warm gray — visible on cream backgrounds |

---

## Full Colour Palette Reference

These are all named tokens from `theme.css`. Use them when building any new app in this workspace.

| Token name | Hex | Role |
|---|---|---|
| `--okh-paper` | `#f6f2ee` | Warm cream — page canvas / background |
| `--color-surface` | `#fdfbf7` | Lightest paper — card and panel surface |
| `--color-surface-soft` | `#f6f2ee` | Standard paper — nested panels, inputs |
| `--color-fg` | `#2e2b29` | Rich espresso — primary body text |
| `--color-muted` | `#6b6b6b` | Warm gray — captions, secondary text |
| `glee-rust` | `#d35b2d` | Glee Rust — primary CTA / link accent |
| `glee-gold` | `#f3b932` | Glee Gold — gradient end / highlight |
| `--okh-orange` | `#c46a2c` | OKH Rust-orange — shared CTA base |
| `--okh-amber` | `#e6a03c` | Amber gold — shared secondary accent |
| `--okh-teal` | `#1c3a34` | Deep forest teal — retro stripe 1 |
| `--okh-olive` | `#676a2c` | Muted olive — retro stripe 2 |
| `--okh-ochre` | `#a06e28` | Warm brown-gold — retro stripe 3 |
| `--okh-rust` | `#5b3a27` | Dark rust — retro stripe 4 |
| `--okh-espresso` | `#2a2320` | Darkest tone — dark mode bg / secondary btn |
| `--color-border` | `#d7d7d7` | Soft border — form fields, card edges |
| **Nav gradient** | `linear-gradient(90deg, #d35b2d, #f3b932)` | Active nav underline, Glee signature stripe |
| **Retro stripe band** | Teal → Olive → Ochre → Rust → Espresso | The 5-stripe hero visual identity |

---

*Generated from glee-fully.tools theme — 2026-04-11*
