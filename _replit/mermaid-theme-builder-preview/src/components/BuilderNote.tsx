export default function BuilderNote() {
  return (
    <section
      className="border border-border/50 rounded-lg bg-card p-6"
      data-testid="section-builder-note"
    >
      <div className="okhp3-label mb-3">Builder's Note</div>

      <div className="border-l-2 border-primary/40 pl-4 space-y-3 text-sm text-muted-foreground leading-relaxed">
        <p>
          This tool started as a personal itch. I kept running into the same friction: needing a custom Mermaid theme, describing what I wanted in a prompt, getting CSS, pasting it, noticing something was off, re-prompting. The feedback loop was slow and imprecise.
        </p>
        <p>
          So I built the direct-manipulation version. Pick a color. See the change. Move on.
        </p>
        <p>
          It's useful to me and probably useful to someone else in the Mermaid.js community. That's why it's here.
        </p>
        <p className="text-foreground/70 italic">
          Not a startup. Not a SaaS pivot in progress. A tool I built, made free, and put on GitHub.
        </p>
      </div>

      <div className="mt-4 text-xs text-muted-foreground font-mono">
        — OverKill Hill P³
      </div>
    </section>
  );
}
