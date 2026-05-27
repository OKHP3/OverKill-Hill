# Agent Guidelines — OverKill Hill P³

- Work in small steps. Ask before large refactors.
- Prefer adding tests before changing logic if risk is medium/high.
- Keep changes localized. Avoid touching unrelated files.
- If you need config/secrets, stop and ask. Never invent credentials.
- Summarize what you changed and why at the end.

### Language Standard: en-US

This project is authored, owned, and maintained by a United States-based creator.
All user-facing content must use United States English (`en-US`).

Scope: UI copy, documentation, README content, release notes, comments intended for
human readers, prompts, tooltips, button text, error messages, validation messages,
QA/QC reports, and marketing language.

Examples of required US-EN spellings:
color, behavior, organization, optimize, customize, center, analyze, modeling,
artifact, visualization, standardization, initialize, finalize, prioritize, summarize,
license (noun), program, catalog, fulfill, gray, toward, among, while.

Do NOT change the following where spelling is externally defined or technically significant:
- Direct quotations from external sources
- Proper nouns, brand names, product names
- Dependency, package, or library names
- URLs, file names, route names
- API fields, schema keys, code identifiers
- Generated lockfiles or external standards

**Identifier rule:** en-US applies to identifiers authored in *new* code. Renaming *existing* identifiers (variables, functions, types, exported symbols) is a breaking change and falls under the same renaming policy as files in Section 1: update every importer in the same commit, run the build and tests after, and set up a redirect if anything external depends on the old name. Do not run a blanket find-and-replace across existing identifiers without explicit instruction.

US English compliance is a required QA/QC gate. It is not a stylistic preference.
Any output that fails this standard is a defect.

---

## Repository Hygiene Standard

**Scope:** Every OverKill Hill P³ Replit-created repo (parent site, companion apps, future siblings).
**Status:** Canonical. Paste this section into every `AGENTS.md` under a heading of `## Repository Hygiene Standard`. Do not edit downstream copies. Edit here and re-sync.
**Version:** 1.0

This section governs how files and folders are named, what structure all sibling repos share, and what counts as detritus that must not accumulate. It exists because Replit Agent, left alone, will name files inconsistently across sessions, scatter working artifacts into the repo root, and leave paste-buffer transcripts in `attached_assets/`. A reader two months later cannot tell what's real, what's stale, and what was junk from the start. The rules below stop that.

---

## 1. Naming conventions

### 1.1 Default: lowercase with hyphens (kebab-case)

Every file and folder name defaults to lowercase letters and digits, with words separated by single hyphens. Use this for documentation, configuration, assets, data files, CSS, plain scripts, and folder names.

Examples that are correct:
- `forge-tokens.css`
- `design-system.md`
- `brand-conformance-checklist.md`
- `sync-forge-tokens.yml`
- `assets/img/forge-anvil-sigil.svg`
- `docs/release-plan.md`
- `scripts/sync-skills.sh`

Examples that are wrong and must be renamed when discovered:
- `Forge_Tokens.css` (mixed case, underscore)
- `designSystem.md` (camelCase)
- `BrandConformanceChecklist.md` (PascalCase used for a doc)
- `OverKillHillBrandTokens.css` (PascalCase used for a stylesheet)
- `My Document.md` (spaces)

The convention does not change with file extension. A markdown doc and a YAML workflow and an SVG asset all follow the same rule.

### 1.2 The full convention by file role

The rule is "kebab-case by default" with three structural exceptions, all dictated by ecosystem convention rather than preference. The table below is the complete decision; deviations from it require an explicit reason.

| File role | Convention | Examples |
|---|---|---|
| Documentation (`.md`) | kebab-case | `design-system.md`, `release-plan.md` |
| Stylesheets (`.css`) | kebab-case | `forge-tokens.css`, `index.css` |
| YAML, JSON, TOML data and config | kebab-case | `sync-forge-tokens.yml`, `palette-defaults.json` |
| Plain scripts (`.sh`, `.py`) | kebab-case | `sync-skills.sh`, `build-tokens.py` |
| Assets (SVG, PNG, etc.) | kebab-case | `forge-anvil-sigil.svg` |
| Folder names | kebab-case | `src/styles/`, `docs/roadmap/`, `skills/agent-skills/` |
| Plain TypeScript modules (`.ts` that don't export a hook or component) | kebab-case | `bpmn-styles.ts`, `theme-mode.ts`, `palettes.ts` |
| React hooks (`.ts` exporting `useFoo`) | camelCase matching the hook | `useTheme.ts`, `useDebounce.ts` |
| React components (`.tsx`/`.jsx`) | PascalCase matching the component | `ApplyTab.tsx`, `DiffView.tsx`, `BuilderNote.tsx` |
| Root governance files | ALL CAPS (ecosystem convention) | `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `AGENTS.md`, `SKILL.md` |
| Tool-required filenames | Whatever the tool requires | `package.json`, `pnpm-lock.yaml`, `tsconfig.json`, `vite.config.ts`, `playwright.config.ts`, `.gitignore`, `.replit`, `.npmrc`, `.prettierrc`, `Dockerfile`, `Makefile`, `CNAME` |
| Web-standard files | Whatever the spec dictates | `humans.txt`, `robots.txt`, `llms.txt`, `404.html`, `_headers`, `favicon.ico`, `manifest.webmanifest` |

### 1.3 The "why" behind the three structural exceptions

The three non-kebab cases (PascalCase components, camelCase hooks, ALL CAPS governance) are not aesthetic choices. They are ecosystem signals.

- PascalCase `.tsx` matches the React component it exports, which means the filename and the JSX tag read the same: `import Button from './Button'; <Button />`. Renaming it to kebab-case breaks tooling assumptions and reads wrong to every React developer.
- camelCase `useTheme.ts` matches the hook function name. The convention is universal in the React ecosystem.
- ALL CAPS root files (LICENSE, README, etc.) trigger special rendering on GitHub and are recognized by virtually every tool that scans repos. Renaming them costs visibility.

Everything else is kebab-case because kebab-case is the most readable choice in URLs, shell history, and ls output, and the broadly accepted default across modern web ecosystems.

### 1.4 Code identifiers are separate from filenames

These rules govern filenames and folder names only. Identifiers inside code follow their language conventions: TypeScript uses `camelCase` for variables and functions and `PascalCase` for types and components; SQL uses `snake_case`; CSS custom properties use `--kebab-case`. Do not change identifiers when renaming files.

### 1.5 Decision tree (when in doubt)

1. Is it a root governance file with a universally expected name (`README`, `LICENSE`, `CHANGELOG`, etc.)? Keep the ALL CAPS conventional name.
2. Is it a tool-required filename (`package.json`, `tsconfig.json`, dotfile, etc.)? Use whatever the tool requires.
3. Is it a `.tsx`/`.jsx` exporting a React component? Use PascalCase matching the component.
4. Is it a `.ts` exporting a React hook (`useFoo`)? Use camelCase matching the hook.
5. Otherwise: kebab-case.

### 1.6 Renaming policy

Renaming a file changes import paths and breaks builds. When fixing a casing violation:
- Update every importer in the same change.
- If the file is referenced by URL on a deployed site, add a redirect or keep a stub at the old path until traffic clears.
- Never rename without running the build and the test suite after.

---

## 2. Sibling repo structural standard

Every OverKill Hill P³ companion app (TypeScript/Vite/React/Tailwind v4) shares this top-level structure. Future siblings start from this; existing siblings converge toward it.

```
<repo-root>/
├── .agents/                  Replit Agent working memory (committed; canonical)
│   └── skills/               agent skills consumed by this app
├── .github/                  GitHub Actions, issue templates
├── .gitignore
├── .npmrc
├── .prettierrc
├── .replit
├── .replitignore
├── AGENTS.md                 governance for AI agents working in this repo
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── docs/                     human-readable design and process docs
│   ├── design-system.md      canonical brand spec (synced from upstream)
│   ├── conformance-audit.md  brand audit evidence
│   ├── release-plan.md       active release plan
│   └── roadmap/              ahead-of-current planning
├── public/                   static assets served as-is
├── scripts/                  build, sync, and maintenance scripts
├── skills/                   SKILL.md packages this app owns or ships
│   └── <skill-name>/         one folder per skill
├── src/                      application source (the app lives here)
│   ├── components/           PascalCase React components
│   ├── data/                 static data (lowercase-hyphen filenames)
│   ├── hooks/                React hooks
│   ├── lib/                  pure logic, palette tables, theme engines
│   ├── pages/                top-level route components
│   ├── styles/               CSS, including forge-tokens.css
│   └── __tests__/            unit tests (Vitest)
├── e2e/                      end-to-end tests (Playwright)
├── examples/                 reference diagrams or demo inputs
├── standards/                process standards this app applies
├── index.html                Vite entrypoint
├── package.json
├── playwright.config.ts
├── pnpm-lock.yaml
├── pnpm-workspace.yaml       if and only if monorepo
├── tsconfig.base.json
├── tsconfig.json
└── vite.config.ts
```

### 2.1 Flat layout vs `artifacts/` monorepo

Two valid layouts exist in the current siblings: a flat layout (`src/` at repo root) and a monorepo layout (`artifacts/<app-name>/src/`). The flat layout is the default for single-app repos. Use `artifacts/` only when the repo legitimately ships more than one app or sandbox (BPMN ships the main app plus `mockup-sandbox` and an `api-server`). Do not put a single app under `artifacts/` for no reason; it just adds depth.

### 2.2 Folders that must not exist at the repo root

These names are reserved for detritus (see Section 3) and must not be used as legitimate folders: `_unused/`, `attached_assets/`, `attached-assets/`, `_drafts/`, `_scratch/`, `_old/`, `tmp/`, `temp/`, `unused/`.

---

## 3. Detritus (what does not belong in version control)

Replit Agent generates working artifacts during a build. Some are useful in the moment and become noise the next week. The categories below are detritus by default and must be either gitignored, moved to a proper home, or deleted.

### 3.1 Replit working-buffer artifacts

- **`attached_assets/`** — paste-buffer transcripts and screenshots from Replit Agent prompts. Filenames look like `Pasted--<title>-<timestamp>.txt` or `image_<timestamp>.png`. Never useful after the session. Always gitignore. Delete from history if accidentally committed.
- **`_unused/`** — code Replit moved out of the way during a refactor. Read it once to make sure nothing important is stranded, then delete the folder. Don't gitignore the name; if it appears, deal with it and remove it.
- **`attached-assets/`** (hyphen variant) and **`unused/`** — same rules.

### 3.2 Test and build output

- **`test-results/`** — Playwright run output. Always gitignored. Delete if committed.
- **`playwright-report/`** — same.
- **`coverage/`** — same.
- **`dist/`**, **`build/`**, **`.next/`**, **`.vite/`** — build output. Gitignore.
- **`node_modules/`** — already gitignored by default; verify.

### 3.3 IDE and OS junk

- **`.DS_Store`**, **`Thumbs.db`**, **`.idea/`**, **`.vscode/`** (with team-specific settings) — gitignore unless the project deliberately ships a workspace config.

### 3.4 Stale planning artifacts

- **`_replit/`** — old Replit working notes that may contain genuinely useful audits or sprint plans. Triage before deleting: move anything worth keeping into `docs/`, archive the rest into a clearly labeled `docs/archive/<date>-<topic>.md`, delete the rest.

### 3.5 Duplicated content from sibling repos

When Replit Agent copies a skill or asset from another repo, it sometimes lands in the wrong repo. Example: a `skills/okhp3-mermaid-theme-builder/` folder appearing inside the BPMN repo. If the skill is not actually owned or shipped by this app, remove it.

### 3.6 Pre-deploy preview directories

- **`_replit/<app-name>-preview/`** — pre-deploy previews of sibling apps copied into the parent repo. Once the live URL is deployed and linked, the preview is dead weight. Delete.

---

## 4. Required `.gitignore` entries

Every OKHP3 repo must include at least the following in `.gitignore`. Add these where absent.

```
# Replit working-buffer artifacts
attached_assets/
attached-assets/
_unused/
unused/

# Test and build output
test-results/
playwright-report/
coverage/
dist/
build/
.next/
.vite/

# IDE / OS
.DS_Store
Thumbs.db
.idea/

# Node
node_modules/
*.log
```

If a folder in this list is currently tracked, untrack it (`git rm -r --cached <folder>`) before committing the `.gitignore` change so it actually disappears from the index.

---

## 5. Decrapify command (the reusable instruction)

When the repo accumulates the artifacts above, run the following short command as a chat message to Replit Agent. It is intentionally terse; it points at this section as the canonical rules.

> **Decrapify this repo per the Repository Hygiene Standard in `AGENTS.md` Section 5.** Triage, do not just delete. Produce a plan first, then execute on confirmation. Cover: `attached_assets/` and any hyphen variant, `_unused/`, `test-results/`, `playwright-report/`, `coverage/`, `dist/`, `build/`, `_replit/` (triage contents into `docs/` or `docs/archive/` before deleting), any duplicated sibling-repo content, any file or folder violating the naming rules in Section 1, and any files or folders that don't fit the project's actual structure.

---

## 6. Brand contract — OverKill Hill P³ Forge

This repo serves the OverKill Hill P³ Forge motif. Canonical reference:
`https://raw.githubusercontent.com/OKHP3/OverKill-Hill/main/assets/css/theme.css`

| Aspect | Value |
|---|---|
| Body scope class | NONE — this is the default brand; pages set no body class |
| Display font | Alfa Slab One |
| Body font | DM Sans |
| Mono font | JetBrains Mono |
| Primary accent | rust-orange `#c46a2c` |
| Secondary accent | amber `#e6a03c` |
| Header surface | teal `#1c3a34` |
| Light page bg | `#f0ebe5` (warm paper) |
| Light ink | `#0f172a` (deep navy) |
| Dark mode | espresso/slate-blue family (hue ~224) |
| Base radius | `0.75rem` |
| Mermaid accent | `#c46a2c` lines and borders |

**Forbidden in this brand's design system:**
- Coral `#d94f63` — that is the glee-fully brand
- Aqua `#2d6f7e` — that is the AskJamie brand
- Olive hue family in dark mode
- Fraunces, Inter, or any font not in Alfa Slab One / DM Sans / JetBrains Mono

**Note on BFS content:** The site hosts a legitimate client project page at
`/projects/bfs-framing-intelligent-futures/`. BFS brand colors, images, and copy
on that page are intentional content, not violations. The prohibition above applies
to OverKill Hill's own design system and brand expression, not to documented client work.

---

## 7. Universal guardrails

These apply in every session, regardless of task:

- No em dashes anywhere — in code, comments, copy, or commit messages. Use periods or restructure the sentence.
- No AI filler in copy or comments: not "seamlessly," "robust," "powerful," "effortlessly," "elevate," "unleash."
- Tailwind v4 only in companion apps: no `tailwind.config.js` (tokens live in CSS via `@theme inline`).
- No new dependencies unless explicitly requested.
- All user-facing content must use US English per the Language Standard in Section 0. UK and Commonwealth spellings are defects, not stylistic variants.

---

## 8. US English audit command (reusable instruction)

When the repo accumulates UK or Commonwealth spellings, send this message to Replit Agent:

> **Run the US English audit per the Language Standard in `AGENTS.md` Section 0.** Produce a QA summary first; execute corrections only after I say "go." Cover: UI copy, docs, README, release notes, human-readable comments, prompts, tooltips, error and validation messages, and QA/QC reports. Apply protected exceptions in Section 0. For existing code identifiers with UK spellings, list them as renaming candidates but do not auto-rename without confirmation. Output: (1) files scanned, (2) files changed, (3) UK spellings found with location, (4) US-EN replacements proposed, (5) protected exceptions intentionally left unchanged with reason, (6) identifier renaming candidates flagged for separate handling, (7) final confirmation that the report itself contains no UK spellings. Wait for "go." No em dashes.
