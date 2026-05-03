export default function WhySection() {
  return (
    <section data-testid="section-why" className="border border-border/50 rounded-lg bg-card p-6">
      <div className="okhp3-label mb-3">Why This Exists</div>
      <h2 className="text-xl font-bold text-foreground mb-4">
        What you get here that you don't get from prompting an LLM
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-3">
          <div className="flex gap-3 items-start">
            <div className="mt-0.5 w-5 h-5 rounded border border-destructive/40 bg-destructive/10 flex items-center justify-center flex-shrink-0">
              <span className="text-destructive text-xs font-bold">✗</span>
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground">Prompting an LLM</p>
              <p className="text-sm text-muted-foreground mt-0.5">
                Generates CSS variable blobs you paste and re-prompt until something looks right. No live preview, no iteration feedback, result varies by model.
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex gap-3 items-start">
            <div className="mt-0.5 w-5 h-5 rounded border border-primary/40 bg-primary/10 flex items-center justify-center flex-shrink-0">
              <span className="text-primary text-xs font-bold">✓</span>
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground">Mermaid Theme Builder</p>
              <p className="text-sm text-muted-foreground mt-0.5">
                Pick a color, see every diagram type update instantly. When it looks right, export. One round trip instead of five.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-5 pt-4 border-t border-border/40 text-sm text-muted-foreground">
        This is a <strong className="text-foreground">community contribution</strong> to the Mermaid.js ecosystem — not a commercial product, not a SaaS, not a competitor to Mermaid.ai. It runs entirely in your browser. No account. No data collected.
      </div>
    </section>
  );
}
