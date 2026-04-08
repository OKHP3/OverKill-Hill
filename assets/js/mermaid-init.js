// Mermaid diagram initialization with theme variables
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

const styles = getComputedStyle(document.body);

// Read brand-specific Mermaid theming variables
const mermaidPrimary =
  styles.getPropertyValue("--mermaid-primary-color").trim() || "#111827";
const mermaidPrimaryText =
  styles.getPropertyValue("--mermaid-primary-text-color").trim() || "#e5e7eb";
const mermaidBorder =
  styles.getPropertyValue("--mermaid-primary-border-color").trim() || "#c46a2c";
const mermaidLine =
  styles.getPropertyValue("--mermaid-line-color").trim() || "#c46a2c";
const mermaidSecondary =
  styles.getPropertyValue("--mermaid-secondary-color").trim() || "#181f26";
const mermaidTertiary =
  styles.getPropertyValue("--mermaid-tertiary-color").trim() || "#1c3a34";
const mermaidCluster =
  styles.getPropertyValue("--mermaid-cluster-bg").trim() || "#0d1117";
const mermaidEdgeLabel =
  styles.getPropertyValue("--mermaid-edge-label-bg").trim() || "#181f26";
const fontBody =
  styles.getPropertyValue("--font-body").trim() ||
  '"DM Sans", system-ui, -apple-system, "Segoe UI", sans-serif';

mermaid.initialize({
  startOnLoad: false,
  securityLevel: "loose",
  theme: "base",
  themeVariables: {
    primaryColor: mermaidPrimary,
    primaryTextColor: mermaidPrimaryText,
    primaryBorderColor: mermaidBorder,
    lineColor: mermaidLine,
    secondaryColor: mermaidSecondary,
    tertiaryColor: mermaidTertiary,
    textColor: mermaidPrimaryText,
    fontFamily: fontBody,
    noteBkgColor: mermaidSecondary,
    noteTextColor: mermaidPrimaryText,
    clusterBkg: mermaidCluster,
    edgeLabelBackground: mermaidEdgeLabel,
  },
  flowchart: {
    curve: "basis",
    nodeSpacing: 55,
    rankSpacing: 65,
    htmlLabels: true,
  },
});

// Explicitly render all .mermaid elements — more reliable than startOnLoad
// when loaded as an ES module at end-of-body
mermaid.run({
  querySelector: ".mermaid",
}).catch((err) => {
  console.warn("[mermaid-init] render error:", err);
});
