# Agent Guidelines: OverKill Hill P³

This file is the operating constitution for any AI agent working in this repo.
Read it before touching any file. It applies equally to Replit Agent, Copilot,
Claude, and any other AI assistant.

Cross-reference `replit.md` for site-specific architecture, script inventory,
and current audit state.

- Work in small steps. Ask before large refactors.
- Prefer adding tests before changing logic if risk is medium/high.
- Keep changes localized. Avoid touching unrelated files.
- If you need config/secrets, stop and ask. Never invent credentials.
- Summarize what you changed and why at the end.

---

## Repository Hygiene Standard
**Brand:** OverKill Hill P³ (Forge / Rust-orange)
**Body scope class:** none -- this is the default brand; pages set no body class
**Canonical stylesheet:** https://raw.githubusercontent.com/OKHP3/OverKill-Hill/main/assets/css/theme.css
**Version:** 2.0

This section governs how files and folders are named, what structure all sibling
repos share, what counts as detritus, and the brand contract this repo serves.
It exists because AI agents, left alone, will name files inconsistently across
sessions, scatter working artifacts into the repo root, and leave paste-buffer
transcripts in `attached_assets/`. A reader two months later cannot tell what is
real, what is stale, and what was junk from the start. The rules below stop that.

---

### 0. Language Standard: en-US

This project is authored, owned, and maintained by a United States-based creator.
All user-facing content must use United States English (`en-US`).

**Scope:** UI copy, documentation, README content, release notes, comments intended
for human readers, prompts, tooltips, button text, error messages, validation
messages, QA/QC reports, marketing language, and any new code identifiers
authored in this repo.

**Examples of required US-EN spellings:** color, behavior, organization, optimize,
customize, center, analyze, modeling, artifact, visualization, standardization,
initialize, finalize, prioritize, summarize, license (noun), program, catalog,
fulfill, gray, toward, among, while.

**Protected exceptions (do NOT change spelling in):**
- Direct quotations from external sources
- Proper nouns, brand names, product names
- Dependency, package, or library names
- URLs, file names, route names
- API fields, schema keys, existing code identifiers
- Generated lockfiles or external standards

**Identifier rule:** en-US applies to identifiers authored in *new* code.
Renaming *existing* identifiers (variables, functions, types, exported symbols)
is a breaking change and falls under the same renaming policy as files in
Section 1: update every importer in the same commit, run the build and tests
after, and set up a redirect if anything external depends on the old name. Do
not run a blanket find-and-replace across existing identifiers without explicit
instruction.

**Status:** US English compliance is a required QA/QC gate, not a stylistic
preference. Any output failing this standard is a defect.

---

### 1. Naming conventions

#### 1.1 Default: lowercase with hyphens (kebab-case)

Every file and folder name defaults to lowercase letters and digits, with words
separated by single hyphens. Use this for documentation, configuration, assets,
data files, CSS, plain scripts, and folder names.

Examples that are correct:
- `site-tokens.css`
- `design-system.md`
- `brand-conformance-checklist.md`
- `sync-skills.sh`
- `assets/img/brand-sigil.svg`
- `assets/docs/release-plan.md`
- `scripts/build-search-index.py`

Examples that are wrong and must be renamed when discovered:
- `SiteTokens.css` (PascalCase used for a stylesheet)
- `designSystem.md` (camelCase)
- `BrandConformanceChecklist.md` (PascalCase used for a doc)
- `My Document.md` (spaces)

The convention does not change with file extension. A markdown doc and a YAML
workflow and an SVG asset all follow the same rule.

#### 1.2 The full convention by file role

The rule is "kebab-case by default" with three structural exceptions, all
dictated by ecosystem convention rather than preference. The table below is the
complete decision; deviations from it require an explicit reason.

| File role | Convention | Examples |
|---|---|---|
| Documentation (`.md`) | kebab-case | `design-system.md`, `release-plan.md` |
| Stylesheets (`.css`) | kebab-case | `theme.css`, `site-tokens.css` |
| YAML, JSON, TOML data and config | kebab-case | `sync-tokens.yml`, `palette-defaults.json` |
| Plain scripts (`.sh`, `.py`) | kebab-case | `sync-skills.sh`, `build-tokens.py` |
| Assets (SVG, PNG, WebP, etc.) | kebab-case | `brand-sigil.svg`, `og-cover.webp` |
| Folder names | kebab-case | `assets/img/`, `assets/docs/`, `scripts/` |
| Plain TypeScript modules (`.ts` not exporting a hook or component) | kebab-case | `theme-mode.ts`, `chat-store.ts` |
| React hooks (`.ts` exporting `useFoo`) | camelCase matching the hook | `useTheme.ts`, `useDebounce.ts` |
| React components (`.tsx`/`.jsx`) | PascalCase matching the component | `ChatPane.tsx`, `MessageList.tsx` |
| Root governance files | ALL CAPS (ecosystem convention) | `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `AGENTS.md`, `SKILL.md` |
| Tool-required filenames | Whatever the tool requires | `package.json`, `tsconfig.json`, `vite.config.ts`, `.gitignore`, `.replit`, `.npmrc`, `.prettierrc`, `Makefile`, `CNAME` |
| Web-standard files | Whatever the spec dictates | `humans.txt`, `robots.txt`, `llms.txt`, `404.html`, `_headers`, `favicon.ico`, `site.webmanifest` |

#### 1.3 The "why" behind the three structural exceptions

The three non-kebab cases (PascalCase components, camelCase hooks, ALL CAPS
governance) are not aesthetic choices. They are ecosystem signals.

- PascalCase `.tsx` matches the React component it exports, so the filename and
  the JSX tag read the same: `import Button from './Button'; <Button />`.
  Renaming it to kebab-case breaks tooling assumptions.
- camelCase `useTheme.ts` matches the hook function name. The convention is
  universal in the React ecosystem.
- ALL CAPS root files (LICENSE, README, etc.) trigger special rendering on
  GitHub and are recognized by virtually every tool that scans repos.
  Renaming them costs visibility.

Everything else is kebab-case because it is the most readable choice in URLs,
shell history, and `ls` output, and the broadly accepted default across modern
web ecosystems.

#### 1.4 Code identifiers are separate from filenames

These rules govern filenames and folder names only. Identifiers inside code
follow their language conventions: TypeScript uses `camelCase` for variables
and `PascalCase` for types; CSS custom properties use `--kebab-case`; Python
uses `snake_case`. Do not change identifiers when renaming files.

#### 1.5 Decision tree (when in doubt)

1. Is it a root governance file with a universally expected name (`README`,
   `LICENSE`, `CHANGELOG`, etc.)? Keep the ALL CAPS conventional name.
2. Is it a tool-required filename (`package.json`, `tsconfig.json`, dotfile,
   etc.)? Use whatever the tool requires.
3. Is it a `.tsx`/`.jsx` exporting a React component? Use PascalCase matching
   the component.
4. Is it a `.ts` exporting a React hook (`useFoo`)? Use camelCase matching the
   hook.
5. Otherwise: kebab-case.

#### 1.6 Renaming policy

Renaming a file changes import paths and deployed URLs. When fixing a casing
violation:
- Update every importer in the same change.
- If the file is referenced by a deployed URL, add a redirect or keep a stub
  at the old path until traffic clears.
- Never rename without running the build and tests after.

---

### 2. Sibling repo structural standard

Every OverKill Hill P3 static site repo shares this top-level structure.
Existing siblings converge toward it; deviations are permitted only when
site-specific content genuinely requires a different layout.

```
<repo-root>/
|-- .agents/               Replit Agent working memory (committed; canonical)
|   +-- skills/            agent skills consumed by this app
|-- .github/               GitHub Actions, issue templates
|-- .gitignore
|-- .replit
|-- .replitignore
|-- AGENTS.md              governance for AI agents working in this repo
|-- CHANGELOG.md
|-- CNAME                  GitHub Pages custom domain
|-- CODE_OF_CONDUCT.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- README.md
|-- ROADMAP.md
|-- SECURITY.md
|-- about/                 /about/ page directory
|-- assets/
|   |-- css/               stylesheets (theme.css is the canonical shared sheet)
|   |-- data/              JSON data files (search-index.json, etc.)
|   |-- docs/              generated documentation and audit artifacts
|   |-- img/               brand assets and images (kebab-case filenames)
|   |   +-- favicons/      full favicon set
|   |-- js/                JavaScript (app.js, mermaid-init.js, etc.)
|   +-- templates/         reusable HTML page-shell fragments
|-- contact/               /contact/ page directory
|-- favicon.ico
|-- humans.txt
|-- index.html             site homepage
|-- legal/                 /legal/ page directory
|-- llms.txt               LLM crawler guidance
|-- replit.md              Replit-specific project notes (not for GitHub display)
|-- robots.txt
|-- scripts/               Python build, audit, and maintenance scripts
|-- search/                /search/ page directory
|-- site.webmanifest
|-- sitemap.xml
|-- skills-lock.json
|-- under-construction.html
+-- universe/              /universe/ page directory
```
Each site also has its own unique content directories (e.g. `writings/`,
`projects/`, `found-ry/`, `manifesto/`, `prompt-forge/`, `vault/` for
OverKill Hill) that are not part of the shared standard. Do not remove content
directories that are unique to a site.

#### 2.1 Folders that must not exist at the repo root

These names are reserved for detritus (see Section 3) and must not be used
as legitimate folders: `_unused/`, `attached_assets/`, `attached-assets/`,
`_drafts/`, `_scratch/`, `_old/`, `tmp/`, `temp/`, `unused/`.

---

### 3. Detritus (what does not belong in version control)

Replit Agent generates working artifacts during a build. Some are useful in
the moment and become noise the next week. The categories below are detritus
by default and must be gitignored, moved to a proper home, or deleted.

#### 3.1 Replit working-buffer artifacts

- **`attached_assets/`**: paste-buffer transcripts and screenshots from Replit
  Agent prompts. Filenames look like `Pasted--<title>-<timestamp>.txt` or
  `image_<timestamp>.png`. Never useful after the session. Always gitignore.
  Delete from history if accidentally committed.
- **`_unused/`**: code Replit moved out of the way during a refactor. Read it
  once to confirm nothing important is stranded, then delete the folder.
- **`attached-assets/`** (hyphen variant) and **`unused/`**: same rules.

#### 3.2 Test and build output

- **`test-results/`**: Playwright run output. Always gitignored. Delete if
  committed.
- **`playwright-report/`**: same.
- **`coverage/`**: same.
- **`dist/`**, **`build/`**, **`.next/`**, **`.vite/`**: build output.
  Gitignore.
- **`node_modules/`**: already gitignored by default; verify.

#### 3.3 IDE and OS junk

- **`.DS_Store`**, **`Thumbs.db`**, **`.idea/`**, **`.vscode/`** (with
  team-specific settings): gitignore unless the project deliberately ships a
  workspace config.

#### 3.4 Stale planning artifacts

- **`_replit/`**: old Replit working notes that may contain genuinely useful
  audits or sprint plans. Triage before deleting: move anything worth keeping
  into `assets/docs/` or `assets/docs/archive/`, delete the rest.

#### 3.5 Duplicated content from sibling repos

When an agent copies a skill or asset from another repo, it sometimes lands in
the wrong repo. If the skill or folder is not actually owned by this app,
remove it.

#### 3.6 Pre-deploy preview directories

Pre-deploy previews of sibling apps copied into this repo are dead weight once
the live URL is deployed. Delete them.

---

### 4. Required `.gitignore` entries

Every OKHP3 repo must include at least the following. Add these where absent.

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

If a folder in this list is currently tracked, remove it from the index before
committing the `.gitignore` change so it disappears from tracking.

---

### 5. Decrapify command (reusable instruction)

When the repo accumulates working artifacts, paste this message to Replit Agent:

> **Decrapify this repo per the Repository Hygiene Standard in `AGENTS.md`
> Section 5.** Triage, do not just delete. Produce a plan first, then execute
> on confirmation. Cover: `attached_assets/` and any hyphen variant, `_unused/`,
> `test-results/`, `playwright-report/`, `coverage/`, `dist/`, `build/`,
> `_replit/` (triage into `assets/docs/` or `assets/docs/archive/` before
> deleting), any duplicated sibling-repo content, any file or folder violating
> Section 1, and any forbidden folder name from Section 3. Output a plan with
> four sections: A. DELETE / B. GITIGNORE-AND-UNTRACK / C. TRIAGE-THEN-DELETE /
> D. RENAME. Wait for "go" before executing.

---
### 6. Brand contract (OverKill Hill P³)

This repo serves the OverKill Hill P³ brand.
Canonical reference: https://raw.githubusercontent.com/OKHP3/OverKill-Hill/main/assets/css/theme.css

OverKill Hill P³ Forge motif declared values:

| Aspect | Value |
|---|---|
| Body scope class | none -- this is the default brand; pages set no body class |
| Display font | Alfa Slab One |
| Body font | DM Sans |
| Mono font | JetBrains Mono |
| Primary accent | rust-orange `#c46a2c` |
| Secondary accent | amber `#e6a03c` |
| Header surface | teal `#1c3a34` |
| Light page background | `#f0ebe5` (warm paper) |
| Light ink | `#0f172a` (deep navy) |
| Dark mode | espresso/slate-blue family |
| Mermaid line/border | `#c46a2c` |
| Tone | precise, editorial, forge-mode |

**Forbidden in this brand's design system:**
- Coral `#d94f63` (that is Glee-fully)
- Aqua/teal `#2d6f7e` as a primary accent (that is AskJamie)
- Fredoka or Baloo 2 headings (those are Glee-fully and AskJamie)
- Any font outside Alfa Slab One / DM Sans / JetBrains Mono

**Note on BFS content:** The site hosts a legitimate client project page at
`/projects/bfs-framing-intelligent-futures/`. BFS brand colors, images, and
copy on that page are intentional content, not violations. The prohibition above
applies to OverKill Hill's own design system, not to documented client work.

---

### 7. Universal guardrails

These apply in every session, regardless of task:

- No em dashes anywhere (code, comments, copy, commit messages). Use periods
  or restructure the sentence.
- No AI filler in copy or comments: not "seamlessly," "robust," "powerful,"
  "effortlessly," "elevate," "unleash."
- Tailwind v4 only if Tailwind is in use: no `tailwind.config.js` (tokens live
  in CSS via `@theme inline`).
- No new dependencies unless explicitly requested.
- All user-facing content must use US English per the Language Standard in
  Section 0. UK and Commonwealth spellings are defects, not stylistic variants.

---

### 8. US English audit command (reusable instruction)

When the repo accumulates UK or Commonwealth spellings, paste this message to
Replit Agent:

> **Run the US English audit per the Language Standard in `AGENTS.md` Section
> 0.** Produce a QA summary first; execute corrections only after I say "go."
> Cover: UI copy, docs, README, release notes, human-readable comments,
> prompts, tooltips, error and validation messages, and QA/QC reports. Apply
> protected exceptions in Section 0. For existing code identifiers with UK
> spellings, list them as renaming candidates but do not auto-rename without
> confirmation. Output: (1) files scanned, (2) files to change, (3) UK spellings
> found with location, (4) US-EN replacements proposed, (5) protected exceptions
> intentionally left unchanged with reason, (6) identifier renaming candidates
> flagged for separate handling, (7) final confirmation the report itself
> contains no UK spellings. Wait for "go." No em dashes.
