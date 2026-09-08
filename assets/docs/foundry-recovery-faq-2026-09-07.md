# FoundRy recovery and export FAQ candidate

**Status:** ready-to-apply content candidate. This file records proposed copy and its evidence map; it does not edit the published FoundRy page.

**Scope:** W04 owns the recovery/export FAQ copy for the FoundRy feature page. The destination is the existing `Frequently asked questions` `<details>` block in `projects/found-ry/index.html` (current block begins at line 778). The page's origin story at `#origin` (current lines 610–636) remains intact.

## Replacement FAQ copy

### Can I keep more than one project?

Yes. The FoundRy workbench has named project records in its browser workspace. You can create projects, choose the active project, duplicate one, or delete one. The current workspace allows up to 20 projects. Download a backup before deleting anything you may need later.

### Where is my work stored?

FoundRy stores work in this browser's local storage. The capability workbench uses its own `okh-capability-workspace` store; the Custom GPT studio uses the separate `cgpt-workspace` store. That separation lets the two tools keep their own project data. If browser storage is unavailable or cannot be read, the workbench can keep a temporary in-memory workspace for the current tab, but that state is not a durable save. Clearing site data, changing browser profiles, or using a different browser can remove or hide the saved work. Download a backup before those changes.

### How do I back up or restore a FoundRy project?

In the capability workbench, choose **Download backup** to save the JSON workspace backup, then choose **Import backup** and review the replacement prompt before applying it. A capability backup is an OverKill Hill FoundRy export with a versioned schema and lineage marker. The current limit is 2 MB. Import validates the schema and workspace before replacing the current capability workspace; an invalid or oversized file is rejected. Keep the downloaded file somewhere you control, because browser storage is not an off-device backup.

### Is the source ZIP the same thing as a GPT export?

No. A capability **source ZIP** is a generated starter package for a capability project. It can contain the generated project files and is intended to be inspected, adapted, committed, or handed to another reviewer. The Custom GPT studio's **Full Spec** export is a Markdown specification, and its **Instructions Only** view is text prepared for a builder's Instructions field. Its **Evidence (JSON)** export preserves the studio's readiness, provenance, boundaries, failure behavior, and phase records for review. These are different outputs for different destinations; neither one silently creates or publishes a GPT, Skill, or production system.

### Can I move a capability project into the Custom GPT studio?

The workbench can open the separate Custom GPT studio, but its capability backup and the studio's GPT workspace backup are different formats and stores. Treat them as separate project records. Copy or adapt the authored specification deliberately, then export the artifact you need from the destination tool. Do not rename a file or change an extension and assume that makes it importable.

### Does an export mean the capability is released?

No. An export is a portable artifact or review record. The capability workbench labels generated starters and structural readiness as drafts for owner review; its evidence field is not behavioral proof. A public release requires its own review, source and license checks, privacy and employer/conflict review where applicable, documentation, and an approved publication surface. FoundRy hosting or a downloadable file does not grant publication permission for private source material or create a separate ReFolDec release.

## Evidence map and destination map

| Proposed block | Current source evidence (read-only) | Claim boundary |
| --- | --- | --- |
| Named projects | `artifacts/mockup-sandbox/src/lib/capability-workbench.ts:1-3, 40-42` (`CapabilityWorkspace`, project list, `MAX_CAPABILITY_PROJECTS = 20`); `artifacts/mockup-sandbox/src/pages/capability-workbench.tsx:160-208` (create, duplicate, delete, active project controls). | The FAQ describes only the project controls visible in the current workbench. It does not claim archival or version history. | 
| Origin-specific storage | `artifacts/mockup-sandbox/src/lib/capability-workbench.ts:45-47, 221-290` (`okh-capability-workspace`, memory fallback, storage warning); `artifacts/mockup-sandbox/src/lib/creatorStorage.ts:9-12, 322-365` (`cgpt-workspace`, local-storage persistence and fallback). | Browser-local behavior is stated per store. No server sync, account recovery, or cross-browser continuity is implied. |
| Backup/import | `artifacts/mockup-sandbox/src/lib/capability-workbench.ts:297-362` (versioned FoundRy backup, 2 MB byte limit, parser, replacement validation); `artifacts/mockup-sandbox/src/pages/capability-workbench.tsx:225-270, 386-438` (file picker, import error, explicit replacement prompt); `artifacts/mockup-sandbox/src/lib/creatorStorage.ts:388-410` (separate GPT workspace export/import format). | “Restore” means validated replacement in the selected browser workspace. It does not claim merge, cloud backup, or rollback. |
| Source ZIP versus GPT exports | `artifacts/mockup-sandbox/src/pages/capability-workbench.tsx:755-777` (workspace backup and generated `-starter.zip`); `artifacts/mockup-sandbox/src/pages/ExportPackage.tsx:632-641, 674-676, 770-816` (Markdown, JSON, Instructions Only views and download). | ZIP, Markdown, Instructions Only, and Evidence JSON are described as distinct outputs. No claim that a ZIP is a deployable runtime or a GPT import package. |
| Release boundary | `artifacts/mockup-sandbox/src/lib/capability-workbench.ts:400-430` (structural assessment states and evidence fields); `projects/found-ry/index.html:589-597` (export and browser-only framing), `projects/found-ry/index.html:610-636` (origin story and FoundRy/Skillz relationship). | The FAQ preserves the page's “tools for making tools” origin and does not convert a generated starter, `reviewed` flag, or export into behavioral testing or publication approval. |

## Apply location

Replace the existing FAQ entries inside `projects/found-ry/index.html`'s `Frequently asked questions` block (`<details>` beginning at line 778). Preserve the surrounding `<details>`, existing FAQ classes, parent CSS, the origin-story section, and the page's generated/static distinction. This candidate intentionally leaves the page and generated source untouched.

## Validation performed

- Read the assigned handoff and local `AGENTS.md`/`replit.md` before editing.
- Read the current FAQ and origin-story blocks in `projects/found-ry/index.html`.
- Read the capability workbench storage, backup/import, project-control, ZIP-export, and Custom GPT studio export sources from the owner checkout without modifying them.
- Checked the candidate for unsupported backend, account recovery, blanket licensing, runtime, behavioral-test, or publication claims.
- Confirmed the worktree diff is limited to this candidate and its required handoff record.

This is a proposed content change only. It has not been applied to the webpage, generated HTML, CSS, app source, configuration, or deployment.
