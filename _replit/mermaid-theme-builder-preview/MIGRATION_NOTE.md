# Migration note (2026-05-03)

This folder was migrated from the now-retired Replit project
`Project-Page-Mermaid-Theme-Tool` via the GitHub branch
`migrate/mermaid-page-tooling` (folder `_replit/mermaid-theme-builder-preview/`).

## Status: standalone, buildable dev preview

The original `package.json` used pnpm catalog refs (`"catalog:"`) and a
workspace dep (`"@workspace/api-client-react": "workspace:*"`) that only
resolve inside a pnpm monorepo. This project is a plain static site, so
the deps were rewritten to concrete versions and the unused workspace
dep was dropped. `tsconfig.json` was made standalone (no `extends` / no
project references). Source code in `src/` was not modified.

## Run / build

Vite requires `PORT` and `BASE_PATH` env vars (a Replit convention baked
into `vite.config.ts`):

```
cd _replit/mermaid-theme-builder-preview
npm install
PORT=5173 BASE_PATH=/ npm run dev      # dev server
PORT=5173 BASE_PATH=/ npm run build    # production build → dist/public/
```

Verified: `npm install` + `npm run build` succeed (vite 6, 1683 modules
transformed, ~302 KB JS / ~104 KB CSS gzipped to ~95 KB / ~17 KB).

## Source of truth

The published page is `projects/mermaid-theme-builder/index.html` at the
repo root. Edit that file for any live-site changes. This React preview
is for visual editing only — its build output is not deployed.
