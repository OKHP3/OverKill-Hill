export default function Hero() {
  return (
    <section className="relative border-b border-border/60 okhp3-grid-bg" data-testid="section-hero">
      <div className="container mx-auto px-4 max-w-7xl py-14 md:py-20">
        {/* Breadcrumb */}
        <nav className="mb-6 flex items-center gap-2 font-mono text-xs text-muted-foreground" aria-label="Breadcrumb">
          <a href="https://overkillhill.com" rel="noopener noreferrer" className="hover:text-foreground transition-colors">
            overkillhill.com
          </a>
          <span>/</span>
          <a href="https://overkillhill.com/projects/" rel="noopener noreferrer" className="hover:text-foreground transition-colors">
            projects
          </a>
          <span>/</span>
          <span className="text-foreground/70">mermaid-theme-builder</span>
        </nav>

        <div className="flex flex-wrap items-center gap-3 mb-5">
          <span className="okhp3-label px-2 py-0.5 rounded border border-border/60 bg-card">
            Community Tool
          </span>
          <span className="okhp3-label px-2 py-0.5 rounded border border-border/60 bg-card">
            Open Source
          </span>
          <span className="okhp3-label px-2 py-0.5 rounded border border-primary/30 bg-primary/5 text-primary/80">
            V0.3 Public Alpha
          </span>
        </div>

        <h1 className="text-3xl md:text-5xl font-bold tracking-tight text-foreground leading-tight mb-4">
          Mermaid Theme Builder
          <span className="block text-primary okhp3-glow-text mt-1">
            Visual. Instant. Yours.
          </span>
        </h1>

        <p className="text-lg md:text-xl text-muted-foreground max-w-2xl leading-relaxed mb-8">
          A free, open-source visual editor for Mermaid.js themes. Pick your colors, watch diagrams update live, and export production-ready CSS — no prompting, no guessing, no iteration cycles.
        </p>

        <div className="flex flex-wrap gap-3">
          <a
            href="#embed-tool"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded border border-primary bg-primary text-primary-foreground font-semibold text-sm hover:bg-primary/90 transition-all okhp3-glow"
            data-testid="button-hero-use-tool"
          >
            <svg viewBox="0 0 24 24" className="w-4 h-4 fill-none stroke-current stroke-2" aria-hidden="true">
              <polygon points="5 3 19 12 5 21 5 3" />
            </svg>
            Use the Tool Now
          </a>
          <a
            href="https://github.com/OKHP3/mermaid-theme-builder"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded border border-border bg-card text-foreground font-semibold text-sm hover:border-primary/40 hover:bg-card/80 transition-all"
            data-testid="button-hero-github"
          >
            <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current" aria-hidden="true">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
            </svg>
            View Source
          </a>
        </div>
      </div>
    </section>
  );
}
