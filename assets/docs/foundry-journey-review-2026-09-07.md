# FoundRy feature journey challenger review

Date: 2026-09-07  
Task: W06  
Scope: first-visitor choice of workbench versus Custom GPT studio, output expectations, recovery, and correct launch

This challenger review proposes copy and markup candidates only. It does not change shared source, CSS, generated HTML, runtime, or dependencies.

## Evidence boundary

### Confirmed from checked-in source

- The feature page describes a browser-only Custom GPT build workbench, nine stations, audit, platform comparison, and a specification export, with no backend, database, or login (`projects/found-ry/index.html:207-219`).
- The page has one prominent live-app destination, `https://okhp3.github.io/OverKill-Hill-FoundRy/`, repeated in the hero, embed, footer, and sidebar (`projects/found-ry/index.html:216-219`, `323-361`, `833-836`, `903-906`).
- The page calls the output a Markdown specification that can be copied, downloaded, committed, or handed to a reviewer, and distinguishes an instructions-only view (`projects/found-ry/index.html:503-506`, `737-771`).
- The page states that work is stored in browser local storage and warns that clearing site data clears the build. It says named project slots are on the roadmap (`projects/found-ry/index.html:589-597`, `790-792`).
- The page is explicit that FoundRy is not a place to run or host a Custom GPT and is not connected to a vendor account (`projects/found-ry/index.html:524-548`, `786-799`).
- The actual application source is `artifacts/mockup-sandbox/src/pages/capability-workbench.tsx` and `artifacts/mockup-sandbox/src/lib/capability-workbench.ts`; the separate GPT creator document head is `artifacts/custom-gpt-creator/index.html`.

### Live/browser boundary

- Read-only HTTP checks on 2026-09-07 returned `200` for the live app shell and canonical feature page. The app shell loads `assets/index-CrhN2SoF.js` and `assets/index-DG6BX3xx.css` and its title is “FoundRy Capability Workbench | OverKill Hill P3.”
- The live bundle includes a separate “Open Custom GPT studio →” control, browser-local capability workspace, JSON backup/import handling, export controls, a 2 MB backup limit, and storage-unavailable/tab-only recovery messages. These are live-edge observations, not checked-in website source claims.
- Native browser/keyboard/mobile inspection was not completed because the available Mac was locked and could not be automatically unlocked. No browser interaction or visual pass is claimed.
- The checked-in feature page uses an iframe with `sandbox="allow-scripts allow-same-origin allow-forms"`, explicit full-screen/new-tab links, and a slow-load fallback (`projects/found-ry/index.html:338-361`). Keyboard focus order, iframe load behavior, and mobile rendering remain unverified.

## Prioritized improvements

### 1. Make the first decision explicit: design here, configure the GPT elsewhere

**Finding:** A first visitor sees “Enter the Found‑Rᵧ” and a dense nine-station description. The page later says the workbench is not a hosting platform, but it does not present “workbench” and “Custom GPT studio” as two named destinations at the point of choice. The live app has the studio link, but a visitor may not discover it before entering.

**Exact markup candidate (place beside the hero CTAs at `projects/found-ry/index.html:216`; author in `site-src/pages/projects/found-ry/index.main.html`):**

```html
<p class="hero-choice-note">Choose the surface that matches the job.</p>
<div class="hero-journey-choices" role="group" aria-label="Choose your FoundRy surface">
  <a class="btn btn-primary" href="https://okhp3.github.io/OverKill-Hill-FoundRy/" target="_blank" rel="noopener noreferrer">Design a capability in FoundRy ↗</a>
  <a class="btn btn-quiet" href="https://chatgpt.com/gpts/editor" target="_blank" rel="noopener noreferrer">Configure a Custom GPT in ChatGPT ↗</a>
</div>
<p class="hero-choice-help">FoundRy produces the specification. The GPT studio is where you configure and run the resulting GPT.</p>
```

The ChatGPT destination requires owner verification before application. If no stable studio URL is approved, use an instructional link to the existing FAQ instead of inventing a launch route.

### 2. State the artifact in one concrete sentence above the embed

**Finding:** “Export the whole specification as one document” is accurate but abstract. The page later names Markdown and an instructions-only view, but the first live-workbench encounter does not say what the visitor will leave with.

**Exact copy candidate (insert immediately before `#embed-tool`, after `projects/found-ry/index.html:317`):**

> **What you leave with:** a portable Markdown specification for the capability, including its brief, boundaries, instructions, capabilities, tests, audit result, and an instructions-only version you can take to a builder.

Grounded in `projects/found-ry/index.html:503-506` and `737-771`; “audit result” remains a proposal pending live export confirmation.

### 3. Turn recovery from a warning into a short operating instruction

**Finding:** The FAQ says local storage is used and clearing site data clears the build, while the live bundle has backup/import and storage-unavailable handling. A first visitor is told to export when finished, but not when to export, where the backup is, or what to do after a storage failure.

**Exact copy candidate (replace the FAQ answer at `projects/found-ry/index.html:790-792`):**

> **Where is my work stored, and how do I recover it?** Your draft stays in this browser’s local storage. Download the workspace backup before clearing site data, changing browsers, or handing the work to someone else; use Import in the workbench to restore it. If the browser cannot write storage, keep the tab open and download a backup before refreshing. The Markdown specification is a separate human-readable export for review and handoff.

The storage-unavailable sentence is supported by the live bundle, not the checked-in feature-page source; keep it marked live-edge until the app source is used for parity.

### 4. Use a named launch label consistently, including the embedded-app fallback

**Finding:** “Enter the Found‑Rᵧ,” “Full Screen,” “Open the Found‑Rᵧ Full Screen,” and “Launch the Workbench” all point to the same live app. The page does not make clear that the full-screen/new-tab route is the reliable route for the dense interface.

**Exact markup candidate (adjust labels at `projects/found-ry/index.html:333-361`):**

```html
<a class="embed-btn embed-btn--primary" ...>Open the workbench in a new tab ↗</a>
<p class="embed-note">The embedded preview is for orientation. Use <strong>Open the workbench in a new tab</strong> for the full controls; your draft remains in this browser.</p>
```

The existing “wide by nature” note supports a roomier route (`359-362`); it does not prove keyboard behavior.

### 5. Add a small mobile/keyboard expectation beside the launch controls

**Finding:** The page acknowledges that the workbench is wide and shared CSS reduces iframe height at narrow widths (`assets/css/theme.css:3699-3701`), but a visitor is not told that the embedded frame may be awkward on a phone. The iframe title and reload label exist, yet focus order and control reachability were not verified.

**Exact copy candidate (under the embed disclosure at `projects/found-ry/index.html:343-347`):**

> **Best on desktop:** the workbench has several stations and side-by-side controls. On a phone or narrow embedded view, open it in a new tab and use the browser’s normal zoom and scrolling controls.

Before application, run responsive and keyboard checks at 320px and 390px and confirm the new-tab route exposes the same app state.

## Cheap validations before applying any candidate

1. Author changes in `site-src/pages/projects/found-ry/index.main.html`; regenerate and confirm every launch URL remains canonical.
2. Run `python3 scripts/validate-site.py` and `python3 scripts/build-search-index.py --check` from the website checkout.
3. Use a real browser at desktop, 390px, and 320px widths. Tab from the hero choice through the iframe fallback and confirm focus is visible and the new-tab link is reachable without entering a trapped iframe.
4. In the live app, create one disposable project, export its Markdown and workspace backup, reload, and import the backup. Record exact observed labels and limits before converting live-edge observations into checked-in claims.

## Review disposition

**NEEDS INPUT before integration:** the page needs an owner-approved destination for “configure the GPT” and a live browser pass for keyboard/mobile behavior. These candidates are evidence-bounded, but they are not applied changes and do not establish production readiness.
