// Shared scripts for OverKill Hill P³ + subsites

document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.querySelector(".theme-toggle");
  const savedTheme = localStorage.getItem("okh-theme");
  if (savedTheme) {
    document.documentElement.setAttribute("data-theme", savedTheme);
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const currentTheme = document.documentElement.getAttribute("data-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", newTheme);
      localStorage.setItem("okh-theme", newTheme);
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector(".site-header");
  const navToggle = document.querySelector(".nav-toggle");
  const yearSpans = document.querySelectorAll(
    "#current-year, #current-year-about, #current-year-manifesto, #current-year-projects, #current-year-glee"
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
});
