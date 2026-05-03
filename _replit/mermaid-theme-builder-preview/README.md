# Mermaid Theme Builder — Replit Dev Preview

  This folder contains the React + Vite dev preview app for the project page at:
  **https://overkillhill.com/projects/mermaid-theme-builder/**

  ## What this is

  This is **not** the Mermaid Theme Builder tool itself — that lives at:
  - Tool: https://okhp3.github.io/mermaid-theme-builder/
  - Tool repo: https://github.com/OKHP3/mermaid-theme-builder

  This is the **advertisement/project page** for that tool, intended to be embedded at
  `projects/mermaid-theme-builder/index.html` in this repo (OKHP3/OverKill-Hill).

  ## Stack

  - React 18 + Vite
  - Tailwind CSS v4
  - shadcn/ui components
  - OKH theme: Alfa Slab One (headings) + DM Sans (body) + JetBrains Mono (mono)
  - OKH colour palette: orange `#c46a2c`, espresso bg, teal radial gradient

  ## Setup in OverKill-Hill Replit project

  1. Copy this folder to `artifacts/mermaid-theme-builder-preview/`
  2. Add to `pnpm-workspace.yaml` packages list
  3. Install dependencies: `pnpm --filter @workspace/mermaid-theme-builder-preview install`
  4. Add workflow: `pnpm --filter @workspace/mermaid-theme-builder-preview run dev`
  5. The published page lives at `projects/mermaid-theme-builder/index.html` — edit that for the live site

  ## Migrated from

  Replit project: `Project-Page-Mermaid-Theme-Tool`  
  Migrated: 2026-05-02
  