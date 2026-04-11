# AskJamie™ — Replit App Theme

Reverse-engineered from `assets/css/theme.css` (`.askjamie-main` block).
Enter these values into the **Manage app themes** panel field by field.

---

## FOUNDATION — Colors

| Field | Value | Notes |
|---|---|---|
| Background color | `#f6f2ee` | AskJamie Paper — warm cream page background |
| Text color | `#2e2b29` | Warm espresso near-black — primary readable text |
| Muted background color | `#fdfbf7` | Lighter paper — card and panel surfaces |
| Muted text color | `#6b6b6b` | Warm gray — captions, metadata, secondary labels |

---

## FOUNDATION — Typography

| Field | Value | Notes |
|---|---|---|
| Sans-serif font | `Open Sans` | Primary body font — loaded from Google Fonts |
| Serif font | `Georgia` | No serif used in this design; nearest universal fallback |
| Monospace font | `Menlo` | No monospace in this design; browser/system default |

> **Note on Open Sans:** This is a Google Font. If the Replit theme panel does not list it by name,
> it will fall back to the system sans-serif, which is fine for the theme config.
> The actual site loads it via:
> `https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600&display=swap`

---

## FOUNDATION — Shape & Spacing

| Field | Value | Notes |
|---|---|---|
| Border radius | `0.75` rem | Standard card/component radius (--radius-md). Buttons use 999px pills. |

---

## COMPONENTS — Actions

| Field | Value | Notes |
|---|---|---|
| Primary background | `#2d6f7e` | AskJamie Teal — primary CTA buttons gradient start |
| Primary text | `#f9fafb` | Off-white — high contrast on teal |
| Secondary background | `#2e2b29` | Espresso dark — secondary/ghost button bg |
| Secondary text | `#ffffff` | White text on dark secondary buttons |
| Accent background | `#007c84` | Deep teal — hero stripe, strong accent |
| Accent text | `#f6f2ee` | Cream — readable on deep teal (the AskJamie contrast pair) |
| Destructive background | `#c53030` | Dark red — harmonizes with warm palette (no explicit destructive defined in CSS) |
| Destructive text | `#ffffff` | White — readable on dark red |

---

## COMPONENTS — Forms

| Field | Value | Notes |
|---|---|---|
| Input | `#fdfbf7` | Paper surface — matches card background |
| Border | `#d7d7d7` | Light warm gray — visible on cream backgrounds |

---

## Full Colour Palette Reference

These are all named tokens from the `.askjamie-main` block in `theme.css`. Use them when building any new app in this workspace.

| Token name | Hex | Role |
|---|---|---|
| `--color-bg` | `#f6f2ee` | Paper base — body / page canvas |
| `--color-surface` | `#fdfbf7` | Card / panel background (lighter paper) |
| `--color-surface-soft` | `#f6f2ee` | Same as bg — soft inset panels |
| `--color-fg` | `#2e2b29` | Primary foreground text (warm espresso) |
| `--color-muted` | `#6b6b6b` | Muted gray — secondary text |
| `--color-accent` | `#2d6f7e` | AskJamie teal — links, active nav, primary actions |
| `--color-border-subtle` | `#d7d7d7` | Form borders, card dividers |
| `stripe-deep-teal` | `#007c84` | Hero stripe — deep teal |
| `stripe-aqua` | `#76b2ba` | Hero stripe — light aqua |
| `stripe-cream` | `#f5ead9` | Hero stripe — warm cream |
| `stripe-warm-beige` | `#d5ba9a` | Hero stripe — warm beige |
| `stripe-mocha` | `#69584c` | Hero stripe — dark mocha |
| `teal-hover` | `#3c8ea1` | Teal hover / CTA gradient end |
| `header-bg` | `#f6f2ee` | Nav header background |
| **Primary CTA gradient** | `linear-gradient(135deg, #2d6f7e, #3c8ea1)` | Buttons — teal to aqua diagonal |

---

## Heading Font

`Baloo 2` — loaded from Google Fonts. Rounded display font used exclusively for H1/H2 headings.
The site uses a three-font system: **Baloo 2** (headings) + **Open Sans** (body) + **Kalam** (handwritten accent).

Google Fonts URL:
```
https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Open+Sans:wght@400;500;600&family=Kalam:wght@400;700&display=swap
```

---

*Generated from askjamie.bot theme — 2026-04-10*
