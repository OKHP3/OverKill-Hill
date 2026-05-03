export default function SiteHeader() {
  return (
    <header className="border-b border-border/60 bg-background/95 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 max-w-7xl h-14 flex items-center justify-between">
        <a
          href="https://overkillhill.com"
          rel="noopener noreferrer"
          className="flex items-center gap-2 group"
          data-testid="link-site-home"
        >
          <div className="w-7 h-7 rounded border border-primary/50 bg-primary/10 flex items-center justify-center">
            <span className="font-mono text-xs font-bold text-primary">OK</span>
          </div>
          <span className="font-mono text-sm font-semibold text-foreground/80 group-hover:text-foreground transition-colors">
            OverKill Hill P³
          </span>
        </a>

        <nav className="flex items-center gap-4 text-sm" data-testid="nav-main">
          <a
            href="https://overkillhill.com/projects/"
            rel="noopener noreferrer"
            className="text-muted-foreground hover:text-foreground transition-colors font-mono text-xs tracking-wide"
            data-testid="link-nav-projects"
          >
            Projects
          </a>
          <a
            href="https://github.com/OKHP3/mermaid-theme-builder"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 text-muted-foreground hover:text-foreground transition-colors font-mono text-xs tracking-wide"
            data-testid="link-nav-github"
          >
            <svg viewBox="0 0 24 24" className="w-3.5 h-3.5 fill-current" aria-hidden="true">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
            </svg>
            GitHub
          </a>
          <a
            href="https://okhp3.github.io/mermaid-theme-builder/"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1 rounded border border-primary/60 bg-primary/10 text-primary hover:bg-primary/20 transition-colors font-mono text-xs font-semibold tracking-wide"
            data-testid="link-nav-live-tool"
          >
            Open Tool
          </a>
        </nav>
      </div>
    </header>
  );
}
