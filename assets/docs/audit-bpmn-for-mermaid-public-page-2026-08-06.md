# BPMN for Mermaid public project page audit

**Status:** Completed findings. No public-page changes were made by this audit.

**Review date:** 2026-08-06

**Disposition:** NEEDS CORRECTION before the project page is treated as an accurate public account of the current product.

## Scope and evidence

This review compared the live project page at <https://overkillhill.com/projects/bpmn-for-mermaid/>, its tracked source at `projects/bpmn-for-mermaid/index.html`, the public BPMN for Mermaid application, the public GitHub repository, and the supplied Replit URL.

The live public page and the tracked source matched during review. The embedded BPMN application loaded and rendered inside the project page without browser-console errors. This audit does not authenticate to Replit or assert the status of its private workspace beyond the public login redirect described below.

## Executive assessment

The page tells the correct high-level story: BPMN for Mermaid combines a text-first `bpmn-beta` diagramming prototype with a BP-SKILL distribution suite. It uses a polished OverKill Hill shell, exposes a working embedded preview, and supplies useful context for a portfolio visitor.

It is not current enough to serve as a reliable project highlight. Several visible claims describe early roadmap work as if it were still unfinished, while one installation command is demonstrably broken and one FAQ promises an SVG export that the playground does not provide. The page should be corrected as a factual-content refresh, not redesigned.

## What is accurate and should be preserved

- The page appropriately presents the project as two connected parts: a `bpmn-beta` authoring experience and BP-SKILL workflow resources.
- The hero calls to action, repository link, product explanation, project sidebar, and embedded preview form a coherent portfolio narrative.
- The embedded public application loaded successfully. The left-side application preview and right-side project context provide a credible live-product framing.
- The page is cautious in some important ways: it calls the work a prototype and does not claim a finished BPMN execution platform.
- The public source and public deployment appeared synchronized for this page, so there is no source-versus-site deployment drift to repair.

## Functional review

| Check | Result | Notes |
| --- | --- | --- |
| Live project page opens | Pass | Title, content, links, and embedded application rendered. |
| Embedded BPMN application loads | Pass | The iframe transitioned to the current public BPMN application. No console errors were observed. |
| GitHub source matches page story | Pass | The reviewed source carried the same substantive content as the live page. |
| Supplied Replit project link | Limited | The link redirected to Replit login. No authenticated inspection was performed. |
| BP-SKILL ZIP install URL | Fail | The displayed `bp-skill-suite-v0.3.zip` URL returned an HTML 404 response rather than a ZIP artifact. |
| FAQ promise of SVG export | Fail | The current playground does not expose an SVG export action. |

## Required factual corrections

| Priority | Public-page claim or surface | Current evidence | Required correction |
| --- | --- | --- | --- |
| P0 | The BP-SKILL quick-install command downloads `bp-skill-suite-v0.3.zip`. | The referenced URL returned HTTP 404 and HTML, not a ZIP file. | Remove the command until a valid versioned release artifact exists, or point it to a verified public download and test it at release time. |
| P0 | The page describes external diagram API packaging, parser validation, and `getStyles` integration as planned or not implemented. | The current BPMN repository contains the adapter, packaged workspace, integration test evidence, compatibility record, and a public Mermaid Host Demo. | Replace early-roadmap wording with an evidence-tiered current statement. Distinguish source and host proof from any unverified npm publication or broader production release. |
| P0 | The build-phase sidebar says "v0.1 Pools & Plugin API" is in progress. | The application now demonstrates pools and a tested host-adapter path. | Update the build state to the current phase and link the compatibility evidence. |
| P0 | The FAQ says users can use the Playground to render and export SVG. | The reviewed playground renders diagrams but has no visible SVG export control. | Remove "export SVG" until that capability exists, or implement it in the application before claiming it publicly. |
| P1 | The project is described as running via Replit. | The public runtime reviewed is GitHub Pages. The supplied Replit URL requires login. | Name GitHub Pages as the public runtime. Present Replit only as a development environment if that is still intended. |
| P1 | The page states there is a six-page React app and five canonical examples. | Current application routes and examples have moved beyond those counts. | Replace fixed counts with verified current counts or remove them when they do not help a visitor. |
| P1 | The hero sends the playground CTA to the embedded application's root. | The user reaches the BPMN application but may need another choice to begin diagramming. | Point the primary CTA and full-screen path directly to `/playground` where appropriate. |
| P1 | Theme palette and `getStyles` work are described as future work. | The product has progressed beyond the earlier roadmap framing. | Reconcile the narrative with the present integration status and separate remaining release gaps from completed work. |
| P1 | Broad claims such as "first," universal compatibility, no-repair-loop outcomes, and ecosystem-scale figures appear without nearby sourcing. | No dated supporting source is attached in the public page. | Add a source and retrieval date, narrow the claim, or remove it. |
| P1 | The page refers to a BPMN "Descriptive Conformance subset." | The product documentation is careful not to claim formal BPMN conformance. | Use "documented descriptive subset" to avoid a formal-conformance implication. |
| P2 | The social-preview image is a generic Sentinel asset. | It does not identify this specific project. | Create a project-specific open graph image when metadata work is otherwise scheduled. |

## Product-story guidance

The public page should make one precise claim:

> BPMN for Mermaid is a browser-first, text-first BPMN descriptive-subset prototype and workflow-resource distribution experience for Mermaid-oriented process work.

Then support that statement with three clearly labeled paths:

1. **Create a diagram**: open the live playground directly and explain what a visitor can produce today.
2. **Use with Mermaid**: link to the host demo and compatibility record, stating exactly what is tested and what has not yet been released as a public package.
3. **Start a process workflow**: link to the BP-SKILL catalog or starter material, without offering a download that has not been generated and verified.

The embedded application should be labeled as a **Live product preview**. That framing embraces the two-layer experience instead of making the OverKill Hill page look like a substitute application shell.

## Source locations for the future patch

The following locations in `projects/bpmn-for-mermaid/index.html` should be reviewed together:

| Approximate lines | Subject |
| --- | --- |
| 13, 22 | Project description and social metadata. |
| 253-259 | Hero calls to action. |
| 288-310 | Embedded application and loading behavior. |
| 392-395 | BP-SKILL scale and product claims. |
| 521-522 | Plugin-status statement. |
| 549-550 | Project-running claim. |
| 596-604 | Theme, page-count, and example-count language. |
| 665-670 | Build-phase sidebar status. |
| 731 | Scope and positioning statement. |
| 815-844 | Frequently asked questions, including SVG export. |
| 869-898 | Sidebar status and related calls to action. |

## Replit boundary

The supplied Replit link redirected to an authentication screen. Therefore, the audit cannot confirm whether the Replit workspace source, deployment configuration, or current session state matches the public GitHub repository. The public GitHub source and live OverKill Hill page were sufficient to identify the visible page issues above.

## Acceptance criteria for a public-page correction

- Every install or download control is verified against an actual successful artifact response before publication.
- The page accurately separates current implementation proof, current hosted demonstration, planned work, and unavailable release artifacts.
- The primary live-product CTA opens the user-facing playground in one action.
- The page does not promise export, packaging, or integration behavior absent from the public product.
- Fixed counts and ecosystem claims are either source-backed and dated or removed.
- The public runtime is identified accurately, and Replit is not presented as an accessible public runtime if it requires authentication.
- Page source, public deployment, and social metadata are reviewed together after the content patch.

## Recommended patch order

1. Remove or repair the broken ZIP installation path and remove the unsupported SVG-export claim.
2. Update plugin, pools, and build-phase language to the current evidence-backed state.
3. Correct runtime, CTA destination, and stale page/example counts.
4. Add a direct Mermaid host-demo path and qualify unsupported market claims.
5. Schedule a project-specific social-preview image as a separate metadata enhancement.

## Final judgment

The page has a sound structural story and a working live preview, but its factual layer has fallen behind the product. It should be treated as a high-priority content-maintenance patch: preserve the design, repair the broken and inaccurate claims, and make the current proof easier to reach.
