/* ===========================================================
   OKH Search — client-side search engine
   - Loads /assets/search-index.json on first interaction.
   - Injects a search trigger button into the primary nav and a
     full-screen overlay search panel.
   - Powers the dedicated /search/ results page when present.
   - Keyboard: Ctrl/Cmd+K or "/" to open. Esc to close.
                ↑/↓ to navigate, Enter to follow.
   =========================================================== */
(function () {
  "use strict";

  const INDEX_URL = "/assets/search-index.json";
  const STYLE_URL = "/assets/css/search.css?v=1";

  // ----- styles -----
  // Pages should preload /assets/css/search.css statically in <head> to avoid a
  // FOUC where the injected nav button renders with an oversized SVG glyph
  // before the stylesheet arrives. This dynamic injection is a fallback for
  // any page that forgot the static link tag.
  function ensureStyles() {
    if (document.querySelector('link[href*="/assets/css/search.css"]')) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = STYLE_URL;
    link.setAttribute("data-okh-search-styles", "");
    document.head.appendChild(link);
  }

  // ----- index loader (cached promise) -----
  let _indexPromise = null;
  function loadIndex() {
    if (!_indexPromise) {
      _indexPromise = fetch(INDEX_URL, { credentials: "same-origin" })
        .then((r) => {
          if (!r.ok) throw new Error("Index fetch failed: " + r.status);
          return r.json();
        })
        .then((d) => Array.isArray(d.entries) ? d.entries : [])
        .catch((err) => {
          console.warn("[okh-search] index load failed:", err);
          return [];
        });
    }
    return _indexPromise;
  }

  // ----- scoring -----
  function tokenize(q) {
    return q.toLowerCase().split(/[^a-z0-9'-]+/i).filter((t) => t.length >= 2);
  }
  function scoreEntry(entry, tokens) {
    if (!tokens.length) return 0;
    const title = (entry.title || "").toLowerCase();
    const desc = (entry.description || "").toLowerCase();
    const headings = (entry.headings || []).join(" ").toLowerCase();
    const body = (entry.body || "").toLowerCase();
    const url = (entry.url || "").toLowerCase();

    let score = 0;
    let allHit = true;
    for (const t of tokens) {
      let tokenHit = 0;
      if (title.includes(t)) tokenHit += 8;
      if (headings.includes(t)) tokenHit += 5;
      if (desc.includes(t)) tokenHit += 4;
      if (body.includes(t)) tokenHit += 2;
      if (url.includes(t)) tokenHit += 1;
      if (tokenHit === 0) allHit = false;
      score += tokenHit;
    }
    // Bonus: full-phrase match
    const phrase = tokens.join(" ");
    if (phrase.length > 2) {
      if (title.includes(phrase)) score += 10;
      if (desc.includes(phrase)) score += 6;
      if (body.includes(phrase)) score += 4;
    }
    // Slight penalty for article-section duplicates so the parent ranks above
    if (entry.category === "Article Section") score -= 0.5;
    return allHit ? score : score * 0.4;
  }
  function search(entries, q, limit) {
    const tokens = tokenize(q);
    if (!tokens.length) return [];
    const scored = [];
    for (const e of entries) {
      const s = scoreEntry(e, tokens);
      if (s > 0) scored.push([s, e]);
    }
    scored.sort((a, b) => b[0] - a[0]);
    return scored.slice(0, limit || 30).map(([s, e]) => ({ score: s, entry: e }));
  }

  // ----- snippet + highlight -----
  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;"
    }[c]));
  }
  function snippetFor(entry, tokens, length) {
    const body = entry.body || entry.description || "";
    if (!body) return "";
    const lower = body.toLowerCase();
    let bestIdx = -1;
    for (const t of tokens) {
      const i = lower.indexOf(t);
      if (i !== -1 && (bestIdx === -1 || i < bestIdx)) bestIdx = i;
    }
    let start = 0;
    if (bestIdx > 80) start = Math.max(0, bestIdx - 60);
    let snip = body.slice(start, start + (length || 220));
    if (start > 0) snip = "…" + snip;
    if (start + (length || 220) < body.length) snip += "…";
    return snip;
  }
  function highlight(text, tokens) {
    let html = escapeHtml(text);
    for (const t of tokens) {
      if (!t) continue;
      const re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
      html = html.replace(re, "<mark>$1</mark>");
    }
    return html;
  }

  // ----- result rendering -----
  function renderResultHtml(result, tokens) {
    const e = result.entry;
    const snip = snippetFor(e, tokens, 220);
    return (
      '<div class="okh-search-result-meta">' +
        '<span class="okh-search-result-cat">' + escapeHtml(e.category || "Page") + "</span>" +
        '<span class="okh-search-result-url">' + escapeHtml(e.url) + "</span>" +
      "</div>" +
      '<h3 class="okh-search-result-title">' + highlight(e.title || e.url, tokens) + "</h3>" +
      (snip ? '<p class="okh-search-result-snippet">' + highlight(snip, tokens) + "</p>" : "")
    );
  }

  // ============================================================
  // Overlay (every page that loads search.js)
  // ============================================================
  function buildOverlay() {
    if (document.querySelector(".okh-search-overlay")) return null;
    const wrap = document.createElement("div");
    wrap.className = "okh-search-overlay";
    wrap.setAttribute("role", "dialog");
    wrap.setAttribute("aria-modal", "true");
    wrap.setAttribute("aria-label", "Search OverKill Hill");
    wrap.innerHTML = (
      '<div class="okh-search-panel" role="document">' +
        '<div class="okh-search-input-row">' +
          '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">' +
            '<circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" />' +
          "</svg>" +
          '<input type="search" class="okh-search-input" autocomplete="off" spellcheck="false" placeholder="Search the Forge — articles, projects, ideas…" aria-label="Search" />' +
          '<button type="button" class="okh-search-close" aria-label="Close search">Esc</button>' +
        "</div>" +
        '<div class="okh-search-results" role="list" aria-label="Search results"></div>' +
        '<div class="okh-search-footer">' +
          '<div class="okh-search-keys">' +
            "<span><kbd>↑</kbd><kbd>↓</kbd> navigate</span>" +
            "<span><kbd>↵</kbd> open</span>" +
            "<span><kbd>Esc</kbd> close</span>" +
          "</div>" +
          '<a href="/search/">Open full search →</a>' +
        "</div>" +
      "</div>"
    );
    document.body.appendChild(wrap);
    return wrap;
  }

  function emptyStateHtml() {
    return (
      '<div class="okh-search-empty">' +
        "<p>Search across writings, projects, manifesto, and the Council archives.</p>" +
        '<ul class="okh-search-hint-list">' +
          '<li><button type="button" data-q="mermaid">Mermaid</button></li>' +
          '<li><button type="button" data-q="ROY">ROY</button></li>' +
          '<li><button type="button" data-q="council">Council</button></li>' +
          '<li><button type="button" data-q="manifesto">Manifesto</button></li>' +
          '<li><button type="button" data-q="diagram">diagram</button></li>' +
          '<li><button type="button" data-q="visual edition">v0.3 Visual Edition</button></li>' +
        "</ul>" +
      "</div>"
    );
  }

  function initOverlay() {
    ensureStyles();
    const overlay = buildOverlay();
    if (!overlay) return;
    const input = overlay.querySelector(".okh-search-input");
    const list = overlay.querySelector(".okh-search-results");
    const closeBtn = overlay.querySelector(".okh-search-close");

    let entries = [];
    let activeIdx = 0;
    let currentResults = [];
    let lastTokens = [];
    let lastFocus = null;

    function focusableInPanel() {
      return Array.from(overlay.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), [tabindex]:not([tabindex="-1"])'
      )).filter((el) => el.offsetParent !== null || el === input);
    }

    function open() {
      if (overlay.dataset.open === "true") return;
      lastFocus = document.activeElement;
      overlay.dataset.open = "true";
      document.documentElement.style.overflow = "hidden";
      loadIndex().then((d) => { entries = d; renderEmpty(); });
      setTimeout(() => input.focus(), 30);
    }
    function close() {
      overlay.dataset.open = "false";
      document.documentElement.style.overflow = "";
      // Restore focus to the element that opened the modal
      if (lastFocus && typeof lastFocus.focus === "function") {
        try { lastFocus.focus(); } catch (e) { /* ignore */ }
      }
      lastFocus = null;
    }
    function renderEmpty() {
      list.innerHTML = emptyStateHtml();
      list.querySelectorAll("button[data-q]").forEach((btn) => {
        btn.addEventListener("click", () => {
          input.value = btn.getAttribute("data-q") || "";
          render();
          input.focus();
        });
      });
    }
    function setActive(i) {
      const links = list.querySelectorAll(".okh-search-result");
      activeIdx = Math.max(0, Math.min(i, links.length - 1));
      links.forEach((el, idx) => {
        if (idx === activeIdx) {
          el.setAttribute("data-active", "true");
          el.scrollIntoView({ block: "nearest" });
        } else {
          el.removeAttribute("data-active");
        }
      });
    }
    function render() {
      const q = input.value.trim();
      if (!q) { renderEmpty(); currentResults = []; lastTokens = []; return; }
      lastTokens = tokenize(q);
      currentResults = search(entries, q, 12);
      if (!currentResults.length) {
        list.innerHTML = '<div class="okh-search-noresults"><p>No matches for <strong>' + escapeHtml(q) + "</strong>.</p><p>Try <em>mermaid</em>, <em>ROY</em>, <em>council</em>, or <em>manifesto</em>.</p></div>";
        return;
      }
      list.innerHTML = currentResults.map((r) => (
        '<a class="okh-search-result" href="' + escapeHtml(r.entry.url) + '">' +
          renderResultHtml(r, lastTokens) +
        "</a>"
      )).join("");
      setActive(0);
    }
    input.addEventListener("input", render);
    input.addEventListener("keydown", (ev) => {
      if (ev.key === "ArrowDown") { ev.preventDefault(); setActive(activeIdx + 1); }
      else if (ev.key === "ArrowUp") { ev.preventDefault(); setActive(activeIdx - 1); }
      else if (ev.key === "Enter") {
        const links = list.querySelectorAll(".okh-search-result");
        if (links[activeIdx]) { ev.preventDefault(); window.location.href = links[activeIdx].getAttribute("href"); }
      }
    });
    closeBtn.addEventListener("click", close);
    overlay.addEventListener("click", (ev) => { if (ev.target === overlay) close(); });

    // Focus trap — keep Tab inside the panel while it's open
    overlay.addEventListener("keydown", (ev) => {
      if (ev.key !== "Tab" || overlay.dataset.open !== "true") return;
      const focusables = focusableInPanel();
      if (!focusables.length) { ev.preventDefault(); input.focus(); return; }
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      const active = document.activeElement;
      if (ev.shiftKey) {
        if (active === first || !overlay.contains(active)) { ev.preventDefault(); last.focus(); }
      } else {
        if (active === last) { ev.preventDefault(); first.focus(); }
      }
    });

    document.addEventListener("keydown", (ev) => {
      if (overlay.dataset.open === "true" && ev.key === "Escape") { ev.preventDefault(); close(); return; }
      const isMac = /Mac|iPod|iPhone|iPad/.test(navigator.platform);
      const trigger = (isMac && ev.metaKey && ev.key.toLowerCase() === "k") || (!isMac && ev.ctrlKey && ev.key.toLowerCase() === "k");
      if (trigger) { ev.preventDefault(); open(); return; }
      if (ev.key === "/" && !ev.metaKey && !ev.ctrlKey && !ev.altKey) {
        const tag = (document.activeElement && document.activeElement.tagName || "").toLowerCase();
        const isField = tag === "input" || tag === "textarea" || tag === "select" || (document.activeElement && document.activeElement.isContentEditable);
        if (!isField) { ev.preventDefault(); open(); }
      }
    });

    // Trigger button injection
    injectTrigger(open);
  }

  function injectTrigger(openFn) {
    if (document.querySelector(".okh-search-trigger")) return;
    const isMac = /Mac|iPod|iPhone|iPad/.test(navigator.platform);
    const shortcut = isMac ? "⌘K" : "Ctrl+K";
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "okh-search-trigger";
    btn.setAttribute("aria-label", "Open search (" + shortcut + ")");
    btn.innerHTML = (
      // width/height attrs are an intrinsic-size backstop in case search.css
      // is not yet parsed on first cold load (prevents a flash of an
      // oversized SVG glyph in the nav).
      '<svg class="okh-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">' +
        '<circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" />' +
      "</svg>" +
      '<span class="okh-search-label">Search</span>' +
      '<kbd>' + shortcut + '</kbd>'
    );
    btn.addEventListener("click", (e) => { e.preventDefault(); openFn(); });

    // Place inside primary nav if found, else next to nav-toggle, else into header
    const nav = document.querySelector(".primary-nav ul");
    if (nav) {
      const li = document.createElement("li");
      li.className = "nav-search-item";
      li.appendChild(btn);
      nav.appendChild(li);
      return;
    }
    const toggle = document.querySelector(".nav-toggle");
    if (toggle && toggle.parentNode) { toggle.parentNode.insertBefore(btn, toggle); return; }
    const header = document.querySelector(".site-header .container, .site-header");
    if (header) { header.appendChild(btn); return; }
    document.body.appendChild(btn);
  }

  // ============================================================
  // Dedicated /search/ page
  // ============================================================
  function initSearchPage() {
    const input = document.getElementById("search-page-input");
    const list = document.getElementById("search-results");
    const stats = document.getElementById("search-stats");
    const cats = document.getElementById("search-categories");
    if (!input || !list) return;

    let entries = [];
    let activeCategory = "all";

    function readQueryFromURL() {
      const url = new URL(window.location.href);
      return url.searchParams.get("q") || "";
    }
    function writeQueryToURL(q) {
      const url = new URL(window.location.href);
      if (q) url.searchParams.set("q", q); else url.searchParams.delete("q");
      window.history.replaceState({}, "", url.toString());
    }

    function render() {
      const q = input.value.trim();
      writeQueryToURL(q);
      if (!q) {
        list.innerHTML = "";
        if (stats) stats.textContent = entries.length ? "Type to search " + entries.length + " indexed entries." : "Loading index…";
        return;
      }
      const tokens = tokenize(q);
      let results = search(entries, q, 60);
      if (activeCategory !== "all") {
        results = results.filter((r) => (r.entry.category || "").toLowerCase() === activeCategory.toLowerCase());
      }
      if (!results.length) {
        list.innerHTML = '<div class="search-empty-state"><p>No matches for <strong>' + escapeHtml(q) + "</strong>" + (activeCategory !== "all" ? ' in <em>' + escapeHtml(activeCategory) + '</em>' : "") + ".</p></div>";
        if (stats) stats.textContent = "0 results";
        return;
      }
      if (stats) stats.textContent = results.length + " result" + (results.length === 1 ? "" : "s") + " for \u201c" + q + "\u201d";
      list.innerHTML = results.map((r) => (
        '<a class="okh-search-result" href="' + escapeHtml(r.entry.url) + '">' +
          renderResultHtml(r, tokens) +
        "</a>"
      )).join("");
    }

    function buildCategoryChips() {
      if (!cats) return;
      const counts = {};
      for (const e of entries) {
        const c = e.category || "Page";
        counts[c] = (counts[c] || 0) + 1;
      }
      const ordered = ["all"].concat(Object.keys(counts).sort());
      cats.innerHTML = ordered.map((c) => {
        const label = c === "all" ? "All (" + entries.length + ")" : c + " (" + counts[c] + ")";
        const pressed = c === activeCategory ? "true" : "false";
        return '<button type="button" data-cat="' + escapeHtml(c) + '" aria-pressed="' + pressed + '">' + escapeHtml(label) + "</button>";
      }).join("");
      cats.querySelectorAll("button").forEach((b) => {
        b.addEventListener("click", () => {
          activeCategory = b.getAttribute("data-cat") || "all";
          cats.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", x === b ? "true" : "false"));
          render();
        });
      });
    }

    loadIndex().then((d) => {
      entries = d;
      buildCategoryChips();
      const initialQ = readQueryFromURL();
      if (initialQ) { input.value = initialQ; }
      input.focus();
      render();
    });

    input.addEventListener("input", render);
  }

  // ============================================================
  // Bootstrap
  // ============================================================
  function start() {
    if (document.body.classList.contains("search-page")) {
      ensureStyles();
      initSearchPage();
      // Still inject the overlay so search button works on the search page too
      initOverlay();
    } else {
      initOverlay();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
