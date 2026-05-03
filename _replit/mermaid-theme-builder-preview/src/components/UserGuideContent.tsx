const steps = [
  {
    num: "01",
    title: "Open the builder",
    desc: "Use the embedded tool above or open it in a full tab for maximum workspace. No login required.",
  },
  {
    num: "02",
    title: "Select a diagram type to preview",
    desc: "The panel shows multiple Mermaid diagram types. Pick the one most relevant to your use case as your primary reference.",
  },
  {
    num: "03",
    title: "Adjust base colors",
    desc: "Start with your primary background and node fill colors. Everything else cascades from these. Use the color pickers — HSL sliders give you the most control.",
  },
  {
    num: "04",
    title: "Refine edges, text, and accents",
    desc: "Dial in edge colors, label text colors, and cluster/subgraph backgrounds. Watch the preview update in real time.",
  },
  {
    num: "05",
    title: "Export your theme",
    desc: "Hit Export. You get a complete mermaid themeVariables object ready to drop into your mermaid.initialize() call or mdx frontmatter.",
  },
  {
    num: "06",
    title: "Paste and verify",
    desc: "Drop the exported variables into your project. If anything needs a tweak, return to the builder — your context is preserved in the URL.",
  },
];

export function UserGuideContent() {
  return (
    <div className="space-y-4 pt-2">
      <p className="text-sm text-muted-foreground">
        Get from zero to a custom Mermaid theme in under five minutes.
      </p>
      <div className="space-y-3">
        {steps.map((step) => (
          <div
            key={step.num}
            className="flex gap-4"
            data-testid={`guide-step-${step.num}`}
          >
            <div className="flex-shrink-0 font-mono text-xs font-bold text-primary/60 pt-0.5 w-5">
              {step.num}
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground mb-0.5">{step.title}</p>
              <p className="text-sm text-muted-foreground">{step.desc}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 p-3 rounded border border-primary/20 bg-primary/5 text-xs text-muted-foreground font-mono">
        <span className="text-primary font-semibold">Tier 1 users:</span> Go straight to the tool. It's self-evident.<br />
        <span className="text-primary font-semibold">Tier 2 users:</span> Follow steps 1–5. Total time: ~3 minutes.
      </div>
    </div>
  );
}
