// OverKill Hill P³ site scripts

document.addEventListener("DOMContentLoaded", () => {
  const navToggle = document.querySelector(".nav-toggle");
  const header = document.querySelector(".site-header");
  const nav = document.querySelector(".primary-nav");
  const yearSpans = document.querySelectorAll(
    "#current-year, #current-year-about, #current-year-manifesto, #current-year-projects"
  );
  const themeToggle = document.createElement("button");

  // Mobile nav
  if (navToggle) {
    navToggle.addEventListener("click", () => {
      header.classList.toggle("nav-open");
      const expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", !expanded);
    });
  }

  // Header shadow on scroll
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  });

  // Set current year
  const now = new Date();
  yearSpans.forEach((span) => {
    if (span) {
      span.textContent = now.getFullYear();
    }
  });

  // Theme toggle
  themeToggle.classList.add("theme-toggle");
  themeToggle.setAttribute("aria-label", "Toggle theme");
  themeToggle.innerHTML = "🌓";
  header.querySelector(".container").appendChild(themeToggle);

  // Load theme from localStorage
  const savedTheme = localStorage.getItem("okh-theme");
  if (savedTheme === "light" || savedTheme === "dark") {
    document.documentElement.setAttribute("data-theme", savedTheme);
  }

  themeToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("okh-theme", next);
  });
});
