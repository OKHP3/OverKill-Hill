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

---

## FOUNDATION — Shape & Spacing

| Field | Value | Notes |
|---|---|---|
| Border radius | `0.75` rem | Standard card/component radius (--radius-md). Buttons use 999px pills. |

---

## COMPONENTS — Actions

| Field | Value | Notes |
|---|---|---|
| Primary background | `#c46a2c` | OKH Orange (rust-orange) — CTA buttons gradient start |
| Primary text | `#0f172a` | Dark ink — high contrast on amber/orange CTA |
| Secondary background | `#111827` | Dark surface — secondary/ghost button bg |
| Secondary text | `#e5e7eb` | Light text on dark secondary buttons |
| Accent background | `#1c3a34` | OKH Teal — series badges, highlight panels |
| Accent text | `#e6a03c` | OKH Amber — amber on teal (the signature OKH contrast pair) |
| Destructive background | `#991b1b` | Dark crimson — harmonizes with earthy palette (no explicit destructive defined in CSS) |
| Destructive text | `#fef2f2` | Near-white — readable on dark crimson |

---

## COMPONENTS — Forms

| Field | Value | Notes |
|---|---|---|
| Input | `#181f26` | OKH Surface Soft — slightly lighter than card bg |
| Border | `#374151` | Mid-gray — visible on dark backgrounds |

---

## Full Colour Palette Reference

These are all named tokens from `theme.css`. Use them when building any new app in this workspace.

| Token name | Hex | Role |
|---|---|---|
| `--okh-espresso` | `#2a2320` | Darkest background — body / page canvas |
| `--okh-teal` | `#1c3a34` | Deep forest teal — badges, panels, accents |
| `--okh-olive` | `#676a2c` | Muted olive — secondary accents |
| `--okh-ochre` | `#a06e28` | Mid amber-brown — warm tones |
| `--okh-rust` | `#5b3a27` | Dark rust — warm dark panels |
| `--okh-orange` | `#c46a2c` | Rust-orange — primary CTA / link accent |
| `--okh-amber` | `#e6a03c` | Amber gold — highlight text, series badges |
| `--okh-paper` | `#f6f2ee` | Warm off-white — light mode surface |
| `--okh-gray` | `#6b7280` | Muted gray — secondary text |
| `--color-surface` | `#111827` | Card / panel background |
| `--color-surface-soft` | `#181f26` | Slightly lighter surface (inputs, nested panels) |
| `--color-fg` | `#e5e7eb` | Primary foreground text |
| **Primary CTA gradient** | `linear-gradient(135deg, #c46a2c, #e6a03c)` | Buttons — orange to amber diagonal |

---

## Heading Font

`Alfa Slab One` — loaded from Google Fonts. Display/slab serif used exclusively for H1/H2 headings.
The site uses a two-font system: **Alfa Slab One** (headings) + **DM Sans** (body).

Google Fonts URL:
```
https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=DM+Sans:wght@400;500;600&display=swap
```

---

*Generated from overkillhill.com theme — 2026-04-10*
