// Generated maps use strict Mermaid rendering and links from the visible outline.
import mermaid from "/assets/vendor/mermaid/mermaid.esm.min.mjs";

const diagrams = [...document.querySelectorAll(".universe-diagram")];
const sources = new Map(diagrams.map((element) => [element, element.textContent]));
let sequence = 0;
let pending = Promise.resolve();

async function nodeId(url) {
  const bytes = new TextEncoder().encode(url);
  const hash = await crypto.subtle.digest("SHA-256", bytes);
  return "n" + [...new Uint8Array(hash)].map((value) => value.toString(16).padStart(2, "0")).join("").slice(0, 16);
}

function configure() {
  const styles = getComputedStyle(document.documentElement);
  const token = (key, fallback) => styles.getPropertyValue(key).trim() || fallback;
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: "base",
    themeVariables: {
      primaryColor: token("--mermaid-primary-color", "#111827"),
      primaryTextColor: token("--mermaid-primary-text-color", "#e5e7eb"),
      primaryBorderColor: token("--mermaid-primary-border-color", "#c46a2c"),
      lineColor: token("--mermaid-line-color", "#c46a2c"),
    },
    flowchart: {useMaxWidth: true, htmlLabels: false, wrappingWidth: 180},
  });
}

async function renderVisible() {
  configure();
  for (const element of diagrams) {
    if (!element.closest("details")?.open || element.dataset.rendered) continue;
    try {
      const {svg} = await mermaid.render("universe-render-" + sequence++, sources.get(element));
      element.innerHTML = svg;
      const view = element.querySelector("svg");
      view.setAttribute("aria-label", element.closest("details").querySelector("summary").textContent);
      // Preserve readable labels on phones; the diagram scrolls inside its panel.
      element.style.overflowX = "auto";
      element.style.maxWidth = "100%";
      view.style.width = Math.max(720, view.viewBox.baseVal.width) + "px";
      view.style.maxWidth = "none";
      view.style.height = "auto";
      for (const link of element.closest("details").querySelectorAll("li a[href]")) {
        const target = new URL(link.getAttribute("href"), "https://overkillhill.com/");
        if (target.origin !== "https://overkillhill.com" || target.username || target.password) continue;
        const id = await nodeId(target.href);
        const node = [...view.querySelectorAll("g.node")].find((item) => item.id.includes("flowchart-" + id + "-"));
        if (!node) continue;
        const anchor = document.createElementNS("http://www.w3.org/2000/svg", "a");
        anchor.setAttribute("href", target.pathname + target.hash);
        anchor.setAttribute("aria-label", link.textContent);
        anchor.setAttribute("tabindex", "0");
        while (node.firstChild) anchor.append(node.firstChild);
        node.append(anchor);
      }
      element.dataset.rendered = "true";
      element.hidden = false;
    } catch (error) {
      element.textContent = "The diagram is unavailable. Use the page links below.";
      element.hidden = false;
      console.error("Universe diagram rendering failed", error);
    }
  }
}

function enqueue() {
  pending = pending.then(renderVisible).catch((error) => {
    console.error("Universe diagram queue failed", error);
  });
}
document.querySelectorAll(".universe-generated details").forEach((details) => details.addEventListener("toggle", enqueue));
new MutationObserver(() => {
  diagrams.forEach((element) => { element.removeAttribute("data-rendered"); });
  enqueue();
}).observe(document.documentElement, {attributes: true, attributeFilter: ["data-theme", "data-color-scheme"]});
enqueue();
