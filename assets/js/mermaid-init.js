// Mermaid initialization — shared module across overkillhill.com,
// glee-fully.tools, and askjamie.bot.
// Relies on YAML front-matter in each diagram for theme/look (theme: neutral, look: neo).
// initialize() intentionally omits themeVariables to avoid overriding the YAML config.
//
// Performance: on pages with many diagrams (e.g. the v0.3 article) we use
// IntersectionObserver to defer rendering until each diagram approaches the
// viewport. Falls back to immediate render where the API is unavailable.
import mermaid from "/assets/vendor/mermaid/mermaid.esm.min.mjs";

// Most diagrams are informational and do not need Mermaid's click handling.
// The two v2 heat pages opt in with data-mermaid-security="loose" because
// their diagrams contain curated outbound click directives.
const usesClickableLinks =
  document.body?.dataset.mermaidSecurity === "loose";

const ALLOWED_CLICK_TARGETS = [
  { origin: "https://mermaidchart.cello.so", pathname: "/UhVlNtC2MlS" },
  { origin: "https://replit.com", pathname: "/refer/overkillhillp3" },
  { origin: "https://overkillhill.com", pathname: "/writings/first-diagram-is-a-liar/" },
  { origin: "https://overkillhill.com", pathname: "/" },
  { origin: "https://www.linkedin.com", pathname: "/company/overkillhillp3" },
  { origin: "https://ko-fi.com", pathname: "/T6T71HCY6A" },
];

function isAllowedClickTarget(value) {
  try {
    const url = new URL(value);
    return (
      url.protocol === "https:" &&
      ALLOWED_CLICK_TARGETS.some(
        ({ origin, pathname }) =>
          url.origin === origin &&
          url.pathname === pathname
      )
    );
  } catch {
    return false;
  }
}

function sanitizeClickableLinks(source) {
  // Mermaid's click syntax is line-oriented: click NODE "URL" "tooltip".
  // Remove an entire directive when its URL is not an exact allowlist match.
  return source.replace(
    /^(\s*click\s+\S+\s+)"([^"]+)"(?:\s+"[^"]*")?\s*$/gm,
    (line, prefix, target) =>
      isAllowedClickTarget(target) ? line : "%% Removed disallowed click target"
  );
}

mermaid.initialize({
  startOnLoad: false,
  securityLevel: usesClickableLinks ? "loose" : "strict",
  flowchart: {
    curve: "basis",
    nodeSpacing: 55,
    rankSpacing: 65,
    htmlLabels: true,
  },
});

const diagrams = Array.from(document.querySelectorAll(".mermaid"));

function addAccessibleAlternative(node, index) {
  // Mermaid replaces the source element with an SVG. Preserve a concise,
  // screen-reader-readable alternative before that happens. Authors can
  // provide a better label with data-diagram-label; otherwise the node labels
  // and source type are useful text for users who cannot see the rendering.
  if (node.getAttribute("aria-label") || node.getAttribute("aria-describedby")) {
    return;
  }
  const source = node.textContent.replace(/\s+/g, " ").trim();
  const labels = [...source.matchAll(/["']([^"']{2,120})["']/g)]
    .map((match) => match[1].replace(/\\n/g, " "))
    .filter((label, position, all) => all.indexOf(label) === position)
    .slice(0, 24);
  const fallback = labels.length > 0
    ? labels.join("; ")
    : "Diagram source is available in the page markup.";
  const label = node.dataset.diagramLabel
    || `Diagram ${index + 1}: ${fallback}`;
  node.setAttribute("role", "img");
  node.setAttribute("aria-label", label);
}

function renderOne(node) {
  if (node.dataset.mermaidRendered === "1") return;
  node.dataset.mermaidRendered = "1";
  addAccessibleAlternative(node, diagrams.indexOf(node));
  if (usesClickableLinks) {
    node.textContent = sanitizeClickableLinks(node.textContent);
  }
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
