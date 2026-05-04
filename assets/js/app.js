// ════════════════════════════════════════════════════════════════════════════
//  app.js — Shared client-side script (OverKill Hill P³)
//
//  Sections (in load order):
//   1. GLOBAL   · Reading-progress bar (article pages)
//   2. GLOBAL   · DOMContentLoaded: nav, year stamps, theme toggle (OKH only),
//                 scroll reveal, smooth anchors
//   3. GLEE     · Under-construction overlay gate (toolbox WIP pages)
//   4. GLOBAL   · Sticky TOC scroll-follow (article pages, ≥1024px)
//   5. OKH      · Site search — overlay + dedicated /search/ page
//                 (search.js consolidated here 2026-05-03)
// ════════════════════════════════════════════════════════════════════════════

// ── 1. Reading progress bar ─────────────────────────────────────────────────
(function () {
  const bar = document.getElementById("reading-progress");
  if (!bar) return;

  window.addEventListener(
    "scroll",
    function () {
      const scrollTop =
        window.scrollY || document.documentElement.scrollTop;
      const docHeight =
        document.documentElement.scrollHeight -
        document.documentElement.clientHeight;
      const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      bar.style.width = Math.min(pct, 100) + "%";
    },
    { passive: true }
  );
})();

// ── 2. Page interactions: nav, year, theme toggle, scroll reveal ───────────
document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector(".site-header");
  const navToggle = document.querySelector(".nav-toggle");
  const yearSpans = document.querySelectorAll(
    "#current-year, #current-year-about, #current-year-manifesto, #current-year-projects, #current-year-glee, #current-year-askjamie"
  );
  const body = document.body;

  // Mobile nav
  if (navToggle && header) {
    navToggle.addEventListener("click", () => {
      header.classList.toggle("nav-open");
      const expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!expanded));
    });
  }

  // Header shadow
  if (header) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 50) {
        header.classList.add("scrolled");
      } else {
        header.classList.remove("scrolled");
      }
    });
  }

  // Year stamps
  const year = new Date().getFullYear();
  yearSpans.forEach((el) => {
    if (el) el.textContent = year;
  });

  // Theme toggle – only for core OverKill Hill pages
  const brandLocked =
    body.classList.contains("glee-main") ||
    body.classList.contains("askjamie-main");

  if (!brandLocked) {
    const themeToggle = document.createElement("button");
    themeToggle.classList.add("theme-toggle");
    themeToggle.setAttribute("aria-label", "Toggle theme");
    themeToggle.textContent = "🌓";

    if (header && header.querySelector(".container")) {
      header.querySelector(".container").appendChild(themeToggle);
    }

    const savedTheme = localStorage.getItem("okh-theme");
    if (savedTheme === "light" || savedTheme === "dark") {
      document.documentElement.setAttribute("data-theme", savedTheme);
    }

    themeToggle.addEventListener("click", () => {
      const current =
        document.documentElement.getAttribute("data-theme") || "dark";
      const next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("okh-theme", next);
    });
  } else {
    // Subsites stay on their brand "light" look
    document.documentElement.setAttribute("data-theme", "light");
  }

  // Scroll reveal
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  if (!prefersReducedMotion && "IntersectionObserver" in window) {
    const revealEls = document.querySelectorAll(".reveal-on-scroll");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    revealEls.forEach((el) => observer.observe(el));
  } else {
    document
      .querySelectorAll(".reveal-on-scroll")
      .forEach((el) => el.classList.add("is-visible"));
  }

  // Smooth scroll for internal anchors
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href");
      if (!href || href === "#") return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  // ── 3. GLEE · Under-construction overlay gate ────────────────────────────
  // Used on glee-fully.tools toolbox pages that are live-but-not-finished.
  // No-op on pages without `.construction-overlay`.
  const constructionOverlay = document.querySelector(".construction-overlay");

  if (constructionOverlay) {
    const body = document.body;
    const wipKey =
      constructionOverlay.getAttribute("data-wip-key") ||
      window.location.pathname;

    const storageKey = `glee-wip-dismissed:${wipKey}`;

    // If user already dismissed this specific WIP page, hide overlay
    if (localStorage.getItem(storageKey) === "true") {
      body.classList.add("construction-dismissed");
      constructionOverlay.setAttribute("hidden", "true");
    } else {
      // Wire up dismiss buttons
      const dismissButtons = constructionOverlay.querySelectorAll(
        "[data-wip-dismiss]"
      );

      dismissButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
          body.classList.add("construction-dismissed");
          constructionOverlay.setAttribute("aria-hidden", "true");
          localStorage.setItem(storageKey, "true");
        });
      });

      // Optional: clicking the dark scrim (outside the card) also dismisses
      constructionOverlay.addEventListener("click", (event) => {
        if (event.target === constructionOverlay) {
          const primaryDismiss = constructionOverlay.querySelector(
            "[data-wip-dismiss]"
          );
          if (primaryDismiss) primaryDismiss.click();
        }
      });
    }
  }

});

// ── 4. Sticky TOC: smooth-lerp scroll-follow for #toc-widget ───────────────
// Only activates on wide viewports (≥1024 px) when widget exists.
// No-op on every other page (return on missing element).
(function () {
  if (window.innerWidth < 1024) return;

  var toc    = document.getElementById('toc-widget');
  var footer = document.querySelector('.site-footer');
  if (!toc || !footer) return;

  var lerpedY = 0;
  var targetY = 0;
  var SPEED   = 0.08;   /* 0 = no movement, 1 = instant */
  var NAV_H   = 112;    /* minimum px from viewport top — clears sticky nav */
  var PAD     = 32;     /* px breathing room above the footer */

  function lerp(a, b, t) { return a + (b - a) * t; }

  /* Natural document position of the TOC widget before any transforms */
  function getNaturalTop(el) {
    var top = 0;
    while (el) { top += el.offsetTop; el = el.offsetParent; }
    return top;
  }

  var tocNaturalTop = getNaturalTop(toc);
  var tocH          = toc.offsetHeight;

  function tick() {
    var scrollY   = window.scrollY;
    var footerTop = footer.offsetTop;

    var centeredOffset = Math.max(NAV_H, (window.innerHeight - tocH) / 2);
    var raw = Math.max(0, scrollY + centeredOffset - tocNaturalTop);
    var max = Math.max(0, footerTop - PAD - tocNaturalTop - tocH);
    targetY = Math.min(raw, max);

    lerpedY = lerp(lerpedY, targetY, SPEED);
    toc.style.transform = 'translateY(' + lerpedY.toFixed(2) + 'px)';

    requestAnimationFrame(tick);
  }

  requestAnimationFrame(tick);

  window.addEventListener('resize', function () {
    if (window.innerWidth < 1024) {
      toc.style.transform = '';
    } else {
      toc.style.transform = '';
      tocNaturalTop = getNaturalTop(toc);
      tocH = toc.offsetHeight;
    }
  });
}());

// ── 5. OKH Search — overlay + dedicated /search/ page ──────────────────────
// Consolidated from search.js (2026-05-03). All 26 production pages load this.
// Index: /assets/search-index.json  Styles: inlined into theme.css (2026-05-04)
// Keyboard: Ctrl/Cmd+K or "/" to open · Esc to close · ↑/↓ navigate · ↵ follow
(function () {
  "use strict";

  const INDEX_URL = "/assets/search-index.json";

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
    const title    = (entry.title       || "").toLowerCase();
    const desc     = (entry.description || "").toLowerCase();
    const headings = (entry.headings    || []).join(" ").toLowerCase();
    const body     = (entry.body        || "").toLowerCase();
    const url      = (entry.url         || "").toLowerCase();

    let score = 0;
    let allHit = true;
    for (const t of tokens) {
      let tokenHit = 0;
      if (title.includes(t))    tokenHit += 8;
      if (headings.includes(t)) tokenHit += 5;
      if (desc.includes(t))     tokenHit += 4;
      if (body.includes(t))     tokenHit += 2;
      if (url.includes(t))      tokenHit += 1;
      if (tokenHit === 0) allHit = false;
      score += tokenHit;
    }
    // Bonus: full-phrase match
    const phrase = tokens.join(" ");
    if (phrase.length > 2) {
      if (title.includes(phrase)) score += 10;
      if (desc.includes(phrase))  score += 6;
      if (body.includes(phrase))  score += 4;
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
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
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
        '<span class="okh-search-result-cat">'  + escapeHtml(e.category || "Page") + "</span>" +
        '<span class="okh-search-result-url">'  + escapeHtml(e.url) + "</span>" +
      "</div>" +
      '<h3 class="okh-search-result-title">' + highlight(e.title || e.url, tokens) + "</h3>" +
      (snip ? '<p class="okh-search-result-snippet">' + highlight(snip, tokens) + "</p>" : "")
    );
  }

  // ── Overlay (every page) ────────────────────────────────────────────────
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
          '<input type="search" class="okh-search-input" autocomplete="off" spellcheck="false" ' +
            'placeholder="Search the Forge — articles, projects, ideas…" aria-label="Search" />' +
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
    const overlay = buildOverlay();
    if (!overlay) return;
    const input    = overlay.querySelector(".okh-search-input");
    const list     = overlay.querySelector(".okh-search-results");
    const closeBtn = overlay.querySelector(".okh-search-close");

    let entries        = [];
    let activeIdx      = 0;
    let currentResults = [];
    let lastTokens     = [];
    let lastFocus      = null;

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
      lastTokens     = tokenize(q);
      currentResults = search(entries, q, 12);
      if (!currentResults.length) {
        list.innerHTML =
          '<div class="okh-search-noresults"><p>No matches for <strong>' +
          escapeHtml(q) + "</strong>.</p><p>Try <em>mermaid</em>, <em>ROY</em>, " +
          "<em>council</em>, or <em>manifesto</em>.</p></div>";
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
      if (ev.key === "ArrowDown")  { ev.preventDefault(); setActive(activeIdx + 1); }
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
      const first  = focusables[0];
      const last   = focusables[focusables.length - 1];
      const active = document.activeElement;
      if (ev.shiftKey) {
        if (active === first || !overlay.contains(active)) { ev.preventDefault(); last.focus(); }
      } else {
        if (active === last) { ev.preventDefault(); first.focus(); }
      }
    });

    document.addEventListener("keydown", (ev) => {
      if (overlay.dataset.open === "true" && ev.key === "Escape") { ev.preventDefault(); close(); return; }
      const isMac    = /Mac|iPod|iPhone|iPad/.test(navigator.platform);
      const trigger  = (isMac && ev.metaKey && ev.key.toLowerCase() === "k") ||
                       (!isMac && ev.ctrlKey && ev.key.toLowerCase() === "k");
      if (trigger) { ev.preventDefault(); open(); return; }
      if (ev.key === "/" && !ev.metaKey && !ev.ctrlKey && !ev.altKey) {
        const tag     = (document.activeElement && document.activeElement.tagName || "").toLowerCase();
        const isField = tag === "input" || tag === "textarea" || tag === "select" ||
                        (document.activeElement && document.activeElement.isContentEditable);
        if (!isField) { ev.preventDefault(); open(); }
      }
    });

    injectTrigger(open);
  }

  function injectTrigger(openFn) {
    if (document.querySelector(".okh-search-trigger")) return;
    const isMac   = /Mac|iPod|iPhone|iPad/.test(navigator.platform);
    const shortcut = isMac ? "⌘K" : "Ctrl+K";
    const btn      = document.createElement("button");
    btn.type      = "button";
    btn.className = "okh-search-trigger";
    btn.setAttribute("aria-label", "Open search (" + shortcut + ")");
    btn.innerHTML = (
      '<svg class="okh-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" ' +
        'stroke="currentColor" stroke-width="2" aria-hidden="true">' +
        '<circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" />' +
      "</svg>" +
      '<span class="okh-search-label">Search</span>' +
      '<kbd>' + shortcut + '</kbd>'
    );
    btn.addEventListener("click", (e) => { e.preventDefault(); openFn(); });

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
    const hdr = document.querySelector(".site-header .container, .site-header");
    if (hdr) { hdr.appendChild(btn); return; }
    document.body.appendChild(btn);
  }

  // ── Dedicated /search/ page ─────────────────────────────────────────────
  function initSearchPage() {
    const input = document.getElementById("search-page-input");
    const list  = document.getElementById("search-results");
    const stats = document.getElementById("search-stats");
    const cats  = document.getElementById("search-categories");
    if (!input || !list) return;

    let entries        = [];
    let activeCategory = "all";

    function readQueryFromURL() {
      return new URL(window.location.href).searchParams.get("q") || "";
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
        if (stats) stats.textContent = entries.length
          ? "Type to search " + entries.length + " indexed entries."
          : "Loading index…";
        return;
      }
      const tokens = tokenize(q);
      let results  = search(entries, q, 60);
      if (activeCategory !== "all") {
        results = results.filter((r) =>
          (r.entry.category || "").toLowerCase() === activeCategory.toLowerCase()
        );
      }
      if (!results.length) {
        list.innerHTML =
          '<div class="search-empty-state"><p>No matches for <strong>' +
          escapeHtml(q) + "</strong>" +
          (activeCategory !== "all" ? ' in <em>' + escapeHtml(activeCategory) + "</em>" : "") +
          ".</p></div>";
        if (stats) stats.textContent = "0 results";
        return;
      }
      if (stats) stats.textContent =
        results.length + " result" + (results.length === 1 ? "" : "s") +
        " for \u201c" + q + "\u201d";
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
        const label   = c === "all" ? "All (" + entries.length + ")" : c + " (" + counts[c] + ")";
        const pressed = c === activeCategory ? "true" : "false";
        return '<button type="button" data-cat="' + escapeHtml(c) +
               '" aria-pressed="' + pressed + '">' + escapeHtml(label) + "</button>";
      }).join("");
      cats.querySelectorAll("button").forEach((b) => {
        b.addEventListener("click", () => {
          activeCategory = b.getAttribute("data-cat") || "all";
          cats.querySelectorAll("button").forEach((x) =>
            x.setAttribute("aria-pressed", x === b ? "true" : "false")
          );
          render();
        });
      });
    }

    loadIndex().then((d) => {
      entries = d;
      buildCategoryChips();
      const initialQ = readQueryFromURL();
      if (initialQ) input.value = initialQ;
      input.focus();
      render();
    });

    input.addEventListener("input", render);
  }

  // ── Bootstrap ────────────────────────────────────────────────────────────
  function start() {
    if (document.body.classList.contains("search-page")) {
      initSearchPage();
      initOverlay(); // search button still works on the search page itself
    } else {
      initOverlay();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
}());
