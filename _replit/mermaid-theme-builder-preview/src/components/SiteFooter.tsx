export default function SiteFooter() {
  return (
    <footer className="border-t border-border/60 bg-card/50 mt-16" data-testid="site-footer">
      <div className="container mx-auto px-4 max-w-7xl py-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-5 h-5 rounded border border-primary/50 bg-primary/10 flex items-center justify-center">
                <span className="font-mono text-[10px] font-bold text-primary">OK</span>
              </div>
              <span className="font-mono text-sm font-semibold text-foreground/70">OverKill Hill P³</span>
            </div>
            <p className="text-xs text-muted-foreground">
              Community tools for the open-source ecosystem.{" "}
              <a
                href="https://overkillhill.com"
                rel="noopener noreferrer"
                className="text-primary/60 hover:text-primary transition-colors"
                data-testid="link-footer-home"
              >
                overkillhill.com
              </a>
            </p>
          </div>

          <div className="flex flex-wrap gap-4 text-xs font-mono text-muted-foreground">
            <a
              href="https://okhp3.github.io/mermaid-theme-builder/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-foreground transition-colors"
              data-testid="link-footer-live-tool"
            >
              Live Tool
            </a>
            <a
              href="https://github.com/OKHP3/mermaid-theme-builder"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-foreground transition-colors"
              data-testid="link-footer-github"
            >
              GitHub
            </a>
            <a
              href="https://github.com/OKHP3/mermaid-theme-builder/blob/main/LICENSE"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-foreground transition-colors"
              data-testid="link-footer-license"
            >
              MIT License
            </a>
            <a
              href="https://overkillhill.com/projects/"
              rel="noopener noreferrer"
              className="hover:text-foreground transition-colors"
              data-testid="link-footer-projects"
            >
              All Projects
            </a>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-border/30 text-xs text-muted-foreground/40 font-mono">
          <p>
            Canonical: <span className="text-muted-foreground/60">https://overkillhill.com/projects/mermaid-theme-builder/</span>
            {" · "}
            Not affiliated with Mermaid.ai
            {" · "}
            Free &amp; open source
          </p>
        </div>
      </div>
    </footer>
  );
}
