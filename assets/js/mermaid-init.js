// Mermaid diagram initialization with theme variables
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";

const styles = getComputedStyle(document.body);
const surface =
  styles.getPropertyValue("--color-surface").trim() || "#111827";
const surfaceSoft =
  styles.getPropertyValue("--color-surface-soft").trim() || "#181f26";
const fg =
  styles.getPropertyValue("--color-fg").trim() || "#e5e7eb";
const accent =
  styles.getPropertyValue("--color-accent").trim() || "#c46a2c";
const muted =
  styles.getPropertyValue("--color-muted").trim() || "#6b7280";
const fontBody =
  styles.getPropertyValue("--font-body").trim() ||
  '"DM Sans", system-ui, -apple-system, "Segoe UI", sans-serif';

mermaid.initialize({
  startOnLoad: true,
  securityLevel: "loose",
  theme: "base",
  themeVariables: {
    primaryColor: surface,
    primaryTextColor: fg,
    primaryBorderColor: accent,
    lineColor: accent,
    secondaryColor: surfaceSoft,
    tertiaryColor: surfaceSoft,
    textColor: fg,
    fontFamily: fontBody,
    noteBkgColor: surface,
    noteTextColor: muted,
    clusterBkg: "#0d1117",
    edgeLabelBackground: surfaceSoft,
  },
  flowchart: {
    curve: "basis",
    nodeSpacing: 55,
    rankSpacing: 65,
  },
});
