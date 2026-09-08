# FoundRy recovery and export FAQ candidate

**Status:** ready-to-apply content candidate. This file records proposed copy and its evidence map; it does not edit the published FoundRy page.

**Scope:** W04 owns the recovery/export FAQ copy for the FoundRy feature page. The destination is the existing `Frequently asked questions` `<details>` block in the canonical authoring source `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/site-src/pages/projects/found-ry/index.main.html`. The generator-owned published output is `projects/found-ry/index.html`; the page's origin story at `id="origin"` remains intact.

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
| Named projects | `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/artifacts/mockup-sandbox/src/lib/capability-workbench.ts` (`CapabilityWorkspace`, `projects`, `MAX_CAPABILITY_PROJECTS`); `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/artifacts/mockup-sandbox/src/pages/capability-workbench.tsx` (Project selector, Duplicate, Delete project, and create controls). | The FAQ describes only the project controls visible in the current workbench. It does not claim archival or version history. |
| Origin-specific storage | `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/artifacts/mockup-sandbox/src/lib/capability-workbench.ts` (`CAPABILITY_WORKSPACE_KEY`, `loadCapabilityWorkspace`, `saveCapabilityWorkspace`, temporary-workspace warning); `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/artifacts/mockup-sandbox/src/lib/creatorStorage.ts` (`WORKSPACE_KEY`, `loadWorkspace`, `persistWorkspace`, storage-health fallback). | Browser-local behavior is stated per store. No server sync, account recovery, or cross-browser continuity is implied. |
| Backup/import | `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/artifacts/mockup-sandbox/src/lib/capability-workbench.ts` (`createCapabilityBackup`, `parseCapabilityBackup`, `MAX_CAPABILITY_BACKUP_BYTES`); `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/artifacts/mockup-sandbox/src/pages/capability-workbench.tsx` (Download backup, Import backup, validation error, and Replace workspace confirmation); `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/artifacts/mockup-sandbox/src/lib/creatorStorage.ts` (`exportWorkspace`, `importWorkspace`). | “Restore” means validated replacement in the selected browser workspace. It does not claim merge, cloud backup, or rollback. |
| Source ZIP versus GPT exports | `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/artifacts/mockup-sandbox/src/pages/capability-workbench.tsx` (`-starter.zip` download and workspace backup); `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/artifacts/mockup-sandbox/src/pages/ExportPackage.tsx` (`Full Spec (Markdown)`, `Evidence (JSON)`, `Instructions Only`, and download controls). | ZIP, Markdown, Instructions Only, and Evidence JSON are described as distinct outputs. No claim that a ZIP is a deployable runtime or a GPT import package. |
| Release boundary | `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/artifacts/mockup-sandbox/src/lib/capability-workbench.ts` (`assessCapability`, structural draft states, `reviewed`, and evidence fields); `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/site-src/pages/projects/found-ry/index.main.html` (export/browser-only framing, `id="origin"`, and FoundRy/Skillz relationship). | The FAQ preserves the page's “tools for making tools” origin and does not convert a generated starter, `reviewed` flag, or export into behavioral testing or publication approval. |

## Apply location

Replace the existing FAQ entries inside the canonical authoring source `/Volumes/OKH-Local/04_GitHub_Mirrors/OverKill-Hill-FoundRy/site-src/pages/projects/found-ry/index.main.html`'s `Frequently asked questions` block. Then let the normal generator update the published output `projects/found-ry/index.html`. Preserve the surrounding `<details>`, existing FAQ classes, parent CSS, the origin-story section, and the page's generated/static distinction. This candidate intentionally leaves both page files untouched.

## Validation performed

- Read the assigned handoff and local `AGENTS.md`/`replit.md` before editing.
- Read the current FAQ and origin-story blocks in the canonical source `site-src/pages/projects/found-ry/index.main.html`; treated `projects/found-ry/index.html` as generator-owned output.
- Read the capability workbench storage, backup/import, project-control, ZIP-export, and Custom GPT studio export sources from the owner checkout without modifying them.
- Checked the candidate for unsupported backend, account recovery, blanket licensing, runtime, behavioral-test, or publication claims.
- Confirmed the worktree diff is limited to this candidate and its required handoff record.

This is a proposed content change only. It has not been applied to the webpage, generated HTML, CSS, app source, configuration, or deployment.
