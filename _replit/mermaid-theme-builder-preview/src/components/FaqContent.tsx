const faqs = [
  {
    q: "Is this affiliated with Mermaid.ai?",
    a: "No. This is an independent community contribution to the open-source Mermaid.js ecosystem. It has no relationship with Mermaid.ai or any commercial Mermaid product. Mermaid.js is the open-source library; this tool helps you theme it.",
  },
  {
    q: "Does it cost anything?",
    a: "Nothing. Free now, free always. No subscription, no freemium gate, no ads. MIT licensed.",
  },
  {
    q: "Does it collect any data?",
    a: "No. The tool is fully client-side. No analytics, no telemetry, no server communication. Your theme stays in your browser.",
  },
  {
    q: "Which Mermaid.js versions does it support?",
    a: "Tested against Mermaid.js v10 and v11. The themeVariables API has been stable across these versions. Earlier versions may have partial support.",
  },
  {
    q: "Can I use the exported theme with Docusaurus, VitePress, or GitHub?",
    a: "Yes. The exported themeVariables object is standard Mermaid config — it works anywhere Mermaid.js is used. Check the docs for your platform on how to pass themeVariables.",
  },
  {
    q: "Why doesn't it support dark/light mode toggle in the builder itself?",
    a: "It's V0.3 Public Alpha. Dark/light preview toggle is on the roadmap. For now, set your background color to match your target mode and the contrast preview is accurate.",
  },
  {
    q: "Can I save and share my theme?",
    a: "Not yet via a URL share feature, though it's planned. For now, export your themeVariables JSON and commit it to your project.",
  },
  {
    q: "How do I contribute or file a bug?",
    a: "Open an issue or PR on GitHub: github.com/OKHP3/mermaid-theme-builder. Community feedback is actively used to shape the roadmap.",
  },
];

export function FaqContent() {
  return (
    <div className="space-y-4 pt-2">
      {faqs.map((item, i) => (
        <div
          key={i}
          className="border-b border-border/30 pb-4 last:border-0 last:pb-0"
          data-testid={`faq-item-${i}`}
        >
          <p className="text-sm font-semibold text-foreground mb-1.5">{item.q}</p>
          <p className="text-sm text-muted-foreground leading-relaxed">{item.a}</p>
        </div>
      ))}
    </div>
  );
}
