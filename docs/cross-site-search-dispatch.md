# Cross-Site Search Guide — Dispatch Record
**Staged:** 2026-05-28  
**Issued from:** OverKill Hill P³™ — source of truth  
**Destinations:** Glee-fully.tools Replit · AskJamie.bot Replit  
**Guide file:** `docs/cross-site-search-prompt.md` (784 lines)

---

## What changed since the previous version

This version of the guide adds two new sections not present in earlier drafts:

| Section | Content |
|---------|---------|
| **4g · injectTrigger — search button placement** | Requires a `.header-controls` div in every page `<header>`. The shared `app.js` prepends the search trigger button into this wrapper. Without it, the button falls back to a degraded position. |
| **6a · header-controls wrapper CSS** | `.header-controls { display: flex; align-items: center; gap: 0.5rem; flex-shrink: 0; }` — must exist in `assets/css/theme.css` near the header/nav block. If the site already has the OKH-derived `theme.css`, the rule is present; verify before adding a duplicate. |

Section 7 footer text was also updated to reference `.header-controls` explicitly.

---

## Cover note to paste before the guide (for each sibling agent)

> This is the updated cross-site search implementation guide from OverKill Hill P³™.
> Two sections are new since the last version — **please read them before implementing**:
>
> - **Section 4g** (injectTrigger placement): your page `<header>` must contain a
>   `<div class="header-controls">` wrapper between the primary nav and the hamburger
>   button. The shared `app.js` injects the search trigger into that element. Without
>   it the trigger appears in a degraded fallback position.
>
> - **Section 6a** (header-controls CSS): add the flex rule for `.header-controls`
>   inside `assets/css/theme.css` near your header/nav block (not inside the search
>   CSS block). If you already have the OKH-derived `theme.css`, confirm the rule is
>   present before adding a duplicate.
>
> The rest of the guide is unchanged from the prior version. Paste the full guide
> below and implement from scratch if you haven't started, or apply only sections
> 4g and 6a if you have already implemented everything else.

---

## Distribution status

| Site | Guide sent | Agent acknowledged `.header-controls` |
|------|-----------|---------------------------------------|
| Glee-fully.tools | — | — |
| AskJamie.bot | — | — |

**Action required (human step):** Open each sibling Replit project, paste the cover note above followed by the full contents of `docs/cross-site-search-prompt.md`, and update this table when each agent acknowledges.

---

## Verification checklist (after each agent responds)

- [ ] Agent confirmed it will add `<div class="header-controls">` to every page header (or shared template)
- [ ] Agent confirmed `.header-controls` CSS rule exists or will be added to `theme.css`
- [ ] Agent has not confused `.header-controls` with an OKH-specific class — it is part of the shared foundation
