interface ProjectSidebarProps {
  onOpenTool: () => void;
}

export default function ProjectSidebar({ onOpenTool }: ProjectSidebarProps) {
  return (
    <div className="space-y-4" data-testid="sidebar-project">
      {/* Primary CTA */}
      <div className="rounded-lg border border-primary/40 bg-primary/5 okhp3-glow p-5">
        <p className="okhp3-label mb-2">Start Now</p>
        <button
          onClick={onOpenTool}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded border border-primary bg-primary text-primary-foreground font-semibold text-sm hover:bg-primary/90 transition-all mb-3"
          data-testid="button-sidebar-open-tool"
        >
          <svg viewBox="0 0 24 24" className="w-4 h-4 fill-none stroke-current stroke-2" aria-hidden="true" strokeLinecap="round" strokeLinejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
            <polyline points="15 3 21 3 21 9" />
            <line x1="10" y1="14" x2="21" y2="3" />
          </svg>
          Open Full Screen
        </button>
        <p className="text-xs text-muted-foreground text-center">No login. No install. Works immediately.</p>
      </div>

      {/* Project Meta */}
      <div className="rounded-lg border border-border/50 bg-card p-5 space-y-4">
        <p className="okhp3-label">Project Info</p>

        <div className="space-y-3 text-sm">
          <div>
            <p className="text-xs text-muted-foreground font-mono mb-0.5">Status</p>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-yellow-500/80" />
              <span className="text-foreground">V0.3 Public Alpha</span>
            </div>
          </div>

          <div>
            <p className="text-xs text-muted-foreground font-mono mb-0.5">License</p>
            <span className="text-foreground">MIT</span>
          </div>

          <div>
            <p className="text-xs text-muted-foreground font-mono mb-0.5">Type</p>
            <span className="text-foreground">Community Contribution</span>
          </div>

          <div>
            <p className="text-xs text-muted-foreground font-mono mb-0.5">Cost</p>
            <span className="text-foreground">Free / Open Source</span>
          </div>

          <div>
            <p className="text-xs text-muted-foreground font-mono mb-0.5">Maintained by</p>
            <a
              href="https://overkillhill.com"
              rel="noopener noreferrer"
              className="text-primary/80 hover:text-primary transition-colors font-mono"
              data-testid="link-sidebar-maintainer"
            >
              OverKill Hill P³
            </a>
          </div>

          <div>
            <p className="text-xs text-muted-foreground font-mono mb-0.5">Mermaid.js compat</p>
            <span className="text-foreground">v10, v11+</span>
          </div>
        </div>

        <div className="border-t border-border/30 pt-3 space-y-2">
          <a
            href="https://github.com/OKHP3/mermaid-theme-builder"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
            data-testid="link-sidebar-github"
          >
            <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current flex-shrink-0" aria-hidden="true">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
            </svg>
            View on GitHub
          </a>
          <a
            href="https://github.com/OKHP3/mermaid-theme-builder/issues"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
            data-testid="link-sidebar-issues"
          >
            <svg viewBox="0 0 24 24" className="w-4 h-4 fill-none stroke-current stroke-2 flex-shrink-0" aria-hidden="true" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            Report an Issue
          </a>
          <a
            href="https://github.com/OKHP3/mermaid-theme-builder/blob/main/CONTRIBUTING.md"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
            data-testid="link-sidebar-contributing"
          >
            <svg viewBox="0 0 24 24" className="w-4 h-4 fill-none stroke-current stroke-2 flex-shrink-0" aria-hidden="true" strokeLinecap="round" strokeLinejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
              <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
            Contribute
          </a>
        </div>
      </div>

      {/* Related */}
      <div className="rounded-lg border border-border/50 bg-card p-5">
        <p className="okhp3-label mb-3">Related Resources</p>
        <div className="space-y-2 text-sm">
          <a
            href="https://mermaid.js.org/config/theming.html"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
            data-testid="link-sidebar-mermaid-theming-docs"
          >
            <svg viewBox="0 0 24 24" className="w-3.5 h-3.5 fill-none stroke-current stroke-2 flex-shrink-0" aria-hidden="true" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
            Mermaid.js Theming Docs
          </a>
          <a
            href="https://mermaid.js.org/config/theming.html#theme-variables"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
            data-testid="link-sidebar-theme-variables"
          >
            <svg viewBox="0 0 24 24" className="w-3.5 h-3.5 fill-none stroke-current stroke-2 flex-shrink-0" aria-hidden="true" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
            themeVariables Reference
          </a>
          <a
            href="https://overkillhill.com/projects/"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
            data-testid="link-sidebar-all-projects"
          >
            <svg viewBox="0 0 24 24" className="w-3.5 h-3.5 fill-none stroke-current stroke-2 flex-shrink-0" aria-hidden="true" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="3" width="7" height="7" />
              <rect x="14" y="3" width="7" height="7" />
              <rect x="14" y="14" width="7" height="7" />
              <rect x="3" y="14" width="7" height="7" />
            </svg>
            All OverKill Hill Projects
          </a>
        </div>
      </div>
    </div>
  );
}
