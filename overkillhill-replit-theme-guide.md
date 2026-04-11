# OverKill Hill P³™ — Replit App Theme

Reverse-engineered from `assets/css/theme.css`.
Enter these values into the **Manage app themes** panel field by field.

---

## FOUNDATION — Colors

| Field | Value | Notes |
|---|---|---|
| Background color | `#2a2320` | OKH Espresso — the page body dark background |
| Text color | `#e5e7eb` | Primary readable text (near-white warm gray) |
| Muted background color | `#111827` | Card and panel surface — slightly cooler dark |
| Muted text color | `#6b7280` | Subdued/secondary text (OKH Gray) |

---

## FOUNDATION — Typography

| Field | Value | Notes |
|---|---|---|
| Sans-serif font | `DM Sans` | Primary body font — loaded from Google Fonts |
| Serif font | `Georgia` | No serif used in this design; nearest universal fallback |
| Monospace font | `Menlo` | No monospace in this design; browser/system default |

> **Note on DM Sans:** This is a Google Font. If the Replit theme panel does not list it by name,
> it will fall back to the system sans-serif, which is fine for the theme config.
> The actual site loads it via:
> `https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&display=swap`
>
> **Heading font (not configurable in the theme panel):** `Alfa Slab One` — industrial slab serif used for H1/H2 only.

---

## FOUNDATION — Shape & Spacing

| Field | Value | Notes |
|---|---|---|
| Border radius | `0.75` rem | Standard card/component radius (--radius-md). Buttons use 999px pills. |

---

## COMPONENTS — Actions

| Field | Value | Notes |
|---|---|---|
| Primary background | `#c46a2c` | OKH Orange (rust-orange) — CTA gradient start |
| Primary text | `#0f172a` | Dark ink — high contrast on amber/orange CTA |
| Secondary background | `#111827` | Dark surface — secondary/ghost button bg |
| Secondary text | `#e5e7eb` | Light text on dark secondary buttons |
| Accent background | `#1c3a34` | OKH Forest Teal — series badges, highlight panels |
| Accent text | `#e6a03c` | OKH Amber — amber on teal (the signature OKH contrast pair) |
| Destructive background | `#991b1b` | Dark crimson — harmonizes with earthy palette |
| Destructive text | `#fef2f2` | Near-white — readable on dark crimson |

---

## COMPONENTS — Forms

| Field | Value | Notes |
|---|---|---|
| Input | `#181f26` | OKH Surface Soft — slightly lighter than card bg |
| Border | `#374151` | Mid-gray — visible on dark backgrounds |
| Focus border | `#d35b2d` | Glee Rust — warm orange-red focus ring; cross-brand signal |

---

## COMPONENTS — Containers

| Field | Value | Notes |
|---|---|---|
| Card background | `#fdfbf7` | OKH Paper Light — cards appear as light panels on the dark page, like documents on a dark desk |
| Card text | `#2e2b29` | Rich espresso — dark text on light card surface |
| Popover background | `#fdfbf7` | Same as card — consistent light surface for floating elements |
| Popover text | `#2e2b29` | Same as card text — espresso on paper |

> **Design note:** Using light paper cards on a dark espresso background is a deliberate OKH contrast — it makes cards read as physical objects (documents, artifacts, forge outputs) sitting on the dark worktop.

---

## COMPONENTS — Charts

| Field | Value | Source token | Notes |
|---|---|---|---|
| Chart 1 | `#d35b2d` | `glee-rust` | Warm rust-orange — strongest, most active data series |
| Chart 2 | `#1c3a34` | `okh-teal` | Deep forest teal — strong cool counterpoint |
| Chart 3 | `#f3b932` | `glee-gold` | Warm gold — bright mid-tone |
| Chart 4 | `#676a2c` | `okh-olive` | Muted olive — earthier secondary series |
| Chart 5 | `#a06e28` | `okh-ochre` | Warm brown-gold — deepest mid-tone |

> **Chart palette logic:** These five colours are the OKH industrial stripe family in descending vibrancy — rust, teal, gold, olive, ochre. The same five tones appear as the horizontal stripe band in the site's hero visual identity. Chart data and hero branding share one colour vocabulary.

---

## Full Colour Palette Reference

All named tokens from `theme.css` — use when building any new app in this workspace.

| Token name | Hex | Role |
|---|---|---|
| `--okh-espresso` | `#2a2320` | Darkest background — body / page canvas |
| `--okh-teal` | `#1c3a34` | Deep forest teal — badges, panels, Chart 2 |
| `--okh-olive` | `#676a2c` | Muted olive — secondary accents, Chart 4 |
| `--okh-ochre` | `#a06e28` | Mid amber-brown — warm tones, Chart 5 |
| `--okh-rust` | `#5b3a27` | Dark rust — warm dark panels |
| `--okh-orange` | `#c46a2c` | Rust-orange — primary CTA / link accent |
| `--okh-amber` | `#e6a03c` | Amber gold — highlight text, series badges |
| `--okh-paper` | `#f6f2ee` | Warm off-white — light mode surface |
| `okh-paper-light` | `#fdfbf7` | Lightest paper — cards, popovers |
| `--okh-gray` | `#6b7280` | Muted gray — secondary text |
| `glee-rust` | `#d35b2d` | Glee Rust — focus ring, Chart 1 (cross-brand signal) |
| `glee-gold` | `#f3b932` | Glee Gold — Chart 3 (cross-brand signal) |
| `--color-surface` | `#111827` | Card / panel background (dark context) |
| `--color-surface-soft` | `#181f26` | Slightly lighter surface — inputs, nested panels |
| `--color-fg` | `#e5e7eb` | Primary foreground text (on dark bg) |
| `color-fg-on-card` | `#2e2b29` | Text colour when used on light paper cards |
| **Primary CTA gradient** | `linear-gradient(135deg, #c46a2c, #e6a03c)` | Buttons — orange to amber diagonal |

---

## Hero Stripe Band — Colour Order

The five colours below appear as the horizontal stripe visual identity on the site's hero. They are also the chart palette in the same order:

```
#d35b2d  →  #1c3a34  →  #f3b932  →  #676a2c  →  #a06e28
Rust         Teal         Gold         Olive        Ochre
(Chart 1)   (Chart 2)   (Chart 3)   (Chart 4)   (Chart 5)
```

---

## Google Fonts URL

```
https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=DM+Sans:wght@400;500;600&display=swap
```

---

*Generated from overkillhill.com theme — last updated 2026-04-11*
