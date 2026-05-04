// Mermaid initialization — shared module across overkillhill.com,
// glee-fully.tools, and askjamie.bot.
// Relies on YAML front-matter in each diagram for theme/look (theme: neutral, look: neo).
// initialize() intentionally omits themeVariables to avoid overriding the YAML config.
//
// Performance: on pages with many diagrams (e.g. the v0.3 article) we use
// IntersectionObserver to defer rendering until each diagram approaches the
// viewport. Falls back to immediate render where the API is unavailable.
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

mermaid.initialize({
  startOnLoad: false,
  securityLevel: "loose",
  flowchart: {
    curve: "basis",
    nodeSpacing: 55,
    rankSpacing: 65,
    htmlLabels: true,
  },
});

const diagrams = Array.from(document.querySelectorAll(".mermaid"));

function renderOne(node) {
  if (node.dataset.mermaidRendered === "1") return;
  node.dataset.mermaidRendered = "1";
  mermaid.run({ nodes: [node] }).catch((err) => {
    console.warn("[mermaid-init] render error:", err);
  });
}

// If only a few diagrams, or no IntersectionObserver, render immediately.
if (diagrams.length <= 2 || typeof IntersectionObserver === "undefined") {
  diagrams.forEach(renderOne);
} else {
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          renderOne(entry.target);
          io.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "400px 0px", threshold: 0.01 }
  );
  diagrams.forEach((node) => io.observe(node));
}
