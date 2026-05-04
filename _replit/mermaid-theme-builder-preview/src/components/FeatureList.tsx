const features = [
  {
    title: "Live Diagram Preview",
    desc: "Every color change reflects instantly across multiple diagram types — flowchart, sequence, class, gantt, and more. What you see is exactly what you get.",
    icon: "M13 10V3L4 14h7v7l9-11h-7z",
  },
  {
    title: "Full CSS Variable Export",
    desc: "One-click export of the complete Mermaid themeVariables block. Paste directly into your mermaid.initialize() config.",
    icon: "M16 18l6-6-6-6M8 6l-6 6 6 6",
  },
  {
    title: "Browser-Only — No Server",
    desc: "Runs 100% client-side. No login, no account, no data leaves your machine. Close the tab and nothing is stored anywhere.",
    icon: "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z",
  },
  {
    title: "Multiple Diagram Types",
    desc: "Preview your theme across the full range of Mermaid diagram types simultaneously, not just a single example.",
    icon: "M3 3h18v18H3zM3 9h18M9 21V9",
  },
  {
    title: "Precise Color Picker",
    desc: "Not just a hex input — full HSL/RGB pickers let you dial in exact values with visual confirmation at every step.",
    icon: "M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0L12 2.69z",
  },
  {
    title: "Open Source, MIT License",
    desc: "Fork it, remix it, embed it. Full source on GitHub. Contributions welcome.",
    icon: "M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22",
  },
];

export default function FeatureList() {
  return (
    <section data-testid="section-features">
      <div className="okhp3-label mb-4">Features</div>
      <h2 className="text-xl font-bold text-foreground mb-5">What the builder does</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {features.map((f) => (
          <div
            key={f.title}
            className="flex gap-4 p-4 rounded-lg border border-border/50 bg-card hover:border-primary/30 transition-colors"
            data-testid={`card-feature-${f.title.toLowerCase().replace(/\s+/g, '-')}`}
          >
            <div className="flex-shrink-0 w-9 h-9 rounded border border-primary/30 bg-primary/8 flex items-center justify-center">
              <svg
                viewBox="0 0 24 24"
                className="w-4.5 h-4.5 text-primary fill-none stroke-current stroke-2"
                aria-hidden="true"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d={f.icon} />
              </svg>
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">{f.title}</p>
              <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
