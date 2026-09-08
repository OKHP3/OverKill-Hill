# Found‑Rᵧ metadata parity audit, 2026-09-07

Status: **proposed, not applied**. This audit does not edit the website, generated HTML, or either FoundRy application.

## Evidence boundary

Website ownership is split between `site-src/pages/projects/found-ry/index.main.html` (authoring source) and `projects/found-ry/index.html` (generated release). The website title is intentionally retained. The released capability workbench sources are `artifacts/mockup-sandbox/src/pages/capability-workbench.tsx` and `artifacts/mockup-sandbox/src/lib/capability-workbench.ts`; the separate Custom GPT studio head is `artifacts/custom-gpt-creator/index.html`. These are read-only comparison sources.

The workbench explicitly supports four capability kinds, `prompt`, `skill`, `workflow`, and `software` (`capability-workbench.tsx`, `KINDS`; `capability-workbench.ts`, `CapabilityKind`). Its masthead says “Make a clear, portable starter for a real system” and “Author and export without a model account or usage fees” (`capability-workbench.tsx`, `CapabilityWorkbench` masthead). The separate studio is a Custom GPT surface. The supplied app head names its own surface “FoundRy Capability Workbench”; confirm app identity before any release change.

## Current metadata and parity findings

| Surface | Current source | Finding |
| --- | --- | --- |
| Website title | `projects/found-ry/index.html:13`; authoring `site-src/pages/projects/found-ry/index.main.html:19` | `Found‑Rᵧ | OverKill Hill P³™`; retain as website brand title. |
| Website description | `projects/found-ry/index.html:14`; `site-src/pages.json:540` | Describes only a nine-station Custom GPT workbench and says “shippable.” It does not name prompt, skill, workflow, or software starters. |
| Website social description | `projects/found-ry/index.html:23,39`; `site-src/pages.json:546,558` | Same gap and “shippable artifact” framing. |
| Workbench head | `artifacts/custom-gpt-creator/index.html:5-13` | Names prompt, skill, workflow, software starters and Custom GPT specifications; social copy says reusable systems/tools with explicit contracts, evidence, portable source. |
| Workbench UI title/deck | `artifacts/mockup-sandbox/src/pages/capability-workbench.tsx`, `CapabilityWorkbench` masthead | Calls itself “Capability workbench”; says portable starter, browser-local project, author/export without model account or usage fees. |
| Workbench capability kinds | `artifacts/mockup-sandbox/src/pages/capability-workbench.tsx`, `KINDS`; `artifacts/mockup-sandbox/src/lib/capability-workbench.ts`, `CapabilityKind` | Four supported kinds: prompt, skill, workflow, software. |
| Website iframe title | `site-src/pages/projects/found-ry/index.main.html:169`; generated `projects/found-ry/index.html:357` | `The OverKill Hill Found-Ry: Custom GPT build workbench`; this identifies the embedded host surface, not proof of app behavior. |
| Website hero image alt/social image alt | `site-src/pages/projects/found-ry/index.main.html:36`; generated metadata `projects/found-ry/index.html:27,41` | Nine-station pipeline illustration; no workbench UI alt text is present. |

## Exact proposed copy

These candidates describe the released capability workbench without claiming that a generated starter is production-ready or behaviorally tested.

### Website meta description

Before:

```text
A browser-only build workbench for production-grade Custom GPTs. Nine stations from build brief to ship gate, plus audit scoring and a full spec export.
```

After candidate:

```text
A browser-local workbench for clear, portable prompt, skill, workflow, and software starters, with explicit contracts, evidence, export, and a separate Custom GPT studio.
```

Evidence: capability kinds and masthead in `artifacts/mockup-sandbox/src/pages/capability-workbench.tsx` (`KINDS`, `CapabilityWorkbench`); explicit contract/evidence/portable-source wording in `artifacts/custom-gpt-creator/index.html:5-13`. This avoids “shippable” proof inflation.

### Open Graph and X descriptions

Before (both `og:description` and `twitter:description`):

```text
Tools for making tools. A browser-only workbench that walks a Custom GPT from raw intent to a governed, shippable artifact. Nine stations. No backend.
```

After candidate (use identically for both):

```text
Build and package reusable prompt, skill, workflow, and software starters with explicit contracts, evidence, and portable source. Open the separate Custom GPT studio when that is the target.
```

Evidence: `artifacts/custom-gpt-creator/index.html:9-13` and the four-kind workbench source above. “Separate” is a surface distinction, not a claim about deployment or production readiness.

### Iframe title

Before:

```text
The OverKill Hill Found-Ry: Custom GPT build workbench
```

After candidate:

```text
Found‑Rᵧ capability workbench: prompt, skill, workflow, and software starters
```

Evidence: `site-src/pages/projects/found-ry/index.main.html:145-169` labels the embed as the Live Workbench; `capability-workbench.tsx` `KINDS` supplies the four supported types. This keeps the accessible name aligned with the actual workbench rather than the separate Custom GPT studio.

### Image alt text

Before:

```text
Six glyphs for ore, heat, anvil, quench, mark, and shelf arcing down onto a blueprint anvil -- the Found-Ry nine-station build pipeline
```

After candidate:

```text
Found‑Rᵧ nine-station build pipeline shown as six glyphs arcing onto a blueprint anvil
```

Evidence: authoring image at `site-src/pages/projects/found-ry/index.main.html:36`. This remains an illustration description; it does not claim the image depicts the capability workbench UI.

## Decision

The current website metadata is stale relative to the supplied released workbench's capability types and its separate Custom GPT studio. The candidates above are reviewable copy only. Applying them requires owner review, then edits to the authoring source followed by generated metadata regeneration and parity validation. No application, dependency, CSS, configuration, or publication change is authorized by this audit.
