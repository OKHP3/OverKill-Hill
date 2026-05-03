export default function StoryPlaceholder() {
  return (
    <section
      className="border border-dashed border-border/40 rounded-lg p-6"
      data-testid="section-story-placeholder"
    >
      <div className="flex items-center gap-3 mb-3">
        <div className="okhp3-label">V0.3 Story</div>
        <span className="text-xs font-mono text-muted-foreground/60 border border-border/30 rounded px-2 py-0.5">
          Placeholder
        </span>
      </div>

      <p className="text-sm text-muted-foreground/60 italic leading-relaxed">
        The full write-up — what this is, how it came together, and what it means for the Mermaid.js community — is reserved for the V0.3 article. This page is the tool advertisement; the story is separate.
      </p>

      <p className="mt-3 text-xs font-mono text-muted-foreground/40">
        Article forthcoming. Check back or watch{" "}
        <a
          href="https://github.com/OKHP3"
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary/40 hover:text-primary/60 transition-colors"
          data-testid="link-placeholder-github"
        >
          github.com/OKHP3
        </a>{" "}
        for updates.
      </p>
    </section>
  );
}
