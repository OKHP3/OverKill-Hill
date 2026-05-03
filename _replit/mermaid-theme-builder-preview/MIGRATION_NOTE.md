# Migration note (2026-05-03)

This folder was migrated from the now-retired Replit project
`Project-Page-Mermaid-Theme-Tool` via the GitHub branch
`migrate/mermaid-page-tooling` (folder `_replit/mermaid-theme-builder-preview/`).

## Status: preserved snapshot, NOT wired to a workflow

The OverKill-Hill repo is a plain static site served by `python3 server.py`
— it is **not** a pnpm monorepo. This app's `package.json` uses pnpm
catalog references (`"catalog:"`) and a workspace dep
(`"@workspace/api-client-react": "workspace:*"`), so `pnpm install` /
`npm install` will fail here without first:

1. Replacing every `"catalog:"` dep with a concrete version.
2. Removing or stubbing `@workspace/api-client-react`.
3. Setting `PORT` and `BASE_PATH` env vars (required by `vite.config.ts`).

If you want to revive the dev preview, do that surgery first, then add a
workflow such as `cd _replit/mermaid-theme-builder-preview && PORT=5173
BASE_PATH=/ pnpm dev`.

## Source of truth

The published page is `projects/mermaid-theme-builder/index.html` at the
repo root. Edit that file for any live-site changes.
