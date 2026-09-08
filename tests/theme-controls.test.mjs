import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { after, before, test } from "node:test";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import { dirname, join } from "node:path";

const testsDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = join(testsDirectory, "..");
const appScript = await readFile(join(repositoryRoot, "assets", "js", "app.js"), "utf8");

const BRAND_EXPECTATIONS = {
  glee: {
    bodyClass: "glee-main",
    storageKey: "glee-color-scheme",
    light: "#d35b2d",
    dark: "#1e1b19",
  },
  askjamie: {
    bodyClass: "askjamie-main",
    storageKey: "askjamie-color-scheme",
    light: "#f5efe1",
    dark: "#2c5e6f",
  },
};

let browser;

before(async () => {
  browser = await chromium.launch({ headless: true });
});

after(async () => {
  await browser?.close();
});

function fixtureMarkup(bodyClass = "") {
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="theme-color" media="(prefers-color-scheme: light)" content="fixture-light">
    <meta name="theme-color" media="(prefers-color-scheme: dark)" content="fixture-dark">
  </head>
  <body class="${bodyClass}">
    <header class="site-header">
      <div class="container"></div>
    </header>
    <main><h1>Theme control fixture</h1></main>
    <script>${appScript}</script>
  </body>
</html>`;
}

async function openFixture({ bodyClass = "", storage = {}, colorScheme = "light" } = {}) {
  const page = await browser.newPage();
  await page.emulateMedia({ colorScheme });
  await page.addInitScript(({ mode, values }) => {
    const saved = { ...values };
    Object.defineProperty(window, "localStorage", {
      configurable: true,
      get() {
        if (mode === "blocked") {
          throw new DOMException("Storage is disabled", "SecurityError");
        }
        return {
          getItem(key) {
            return Object.prototype.hasOwnProperty.call(saved, key) ? saved[key] : null;
          },
          setItem(key, value) {
            saved[key] = String(value);
          },
          removeItem(key) {
            delete saved[key];
          },
        };
      },
    });
  }, {
    mode: storage === "blocked" ? "blocked" : "available",
    values: storage === "blocked" ? {} : storage,
  });
  await page.setContent(fixtureMarkup(bodyClass), { waitUntil: "domcontentloaded" });
  return page;
}

async function readState(page, selector) {
  return page.locator(selector).evaluate((toggle) => ({
    state: toggle.dataset.state,
    theme: document.documentElement.getAttribute("data-theme"),
    colorScheme: document.documentElement.getAttribute("data-color-scheme"),
    labels: toggle.getAttribute("aria-label"),
    colors: [...document.querySelectorAll('meta[name="theme-color"]')].map((meta) => ({
      media: meta.getAttribute("media"),
      content: meta.getAttribute("content"),
    })),
  }));
}

async function clickAndRead(page, selector) {
  await page.locator(selector).click();
  return readState(page, selector);
}

test("OKH supports system, light, and dark transitions", async () => {
  const page = await openFixture();
  try {
    const selector = ".theme-toggle";
    assert.deepEqual(await readState(page, selector), {
      state: "system",
      theme: "light",
      colorScheme: null,
      labels: "Switch to light mode",
      colors: [
        { media: "(prefers-color-scheme: light)", content: "fixture-light" },
        { media: "(prefers-color-scheme: dark)", content: "fixture-dark" },
      ],
    });

    assert.equal((await clickAndRead(page, selector)).state, "light");
    assert.equal((await readState(page, selector)).theme, "light");

    assert.equal((await clickAndRead(page, selector)).state, "dark");
    assert.equal((await readState(page, selector)).theme, "dark");

    assert.equal((await clickAndRead(page, selector)).state, "system");
    assert.equal((await readState(page, selector)).theme, "light");

    await page.emulateMedia({ colorScheme: "dark" });
    await page.waitForFunction(() => document.documentElement.dataset.theme === "dark");
    assert.equal((await readState(page, selector)).theme, "dark");
  } finally {
    await page.close();
  }
});

test("Glee and AskJamie keep their light baseline and update theme-color metadata", async () => {
  for (const [brand, expected] of Object.entries(BRAND_EXPECTATIONS)) {
    const page = await openFixture({ bodyClass: expected.bodyClass });
    try {
      const selector = ".glee-color-toggle";
      assert.deepEqual(await readState(page, selector), {
        state: "auto",
        theme: "light",
        colorScheme: null,
        labels: "Color scheme: following your device — click to pin light",
        colors: [
          { media: "(prefers-color-scheme: light)", content: expected.light },
          { media: "(prefers-color-scheme: dark)", content: expected.dark },
        ],
      }, `${brand} auto baseline`);

      const light = await clickAndRead(page, selector);
      assert.equal(light.state, "light", `${brand} light state`);
      assert.equal(light.theme, "light", `${brand} light data-theme baseline`);
      assert.equal(light.colorScheme, "light", `${brand} light data-color-scheme`);
      assert(light.colors.every(({ content }) => content === expected.light), `${brand} light metadata`);

      const dark = await clickAndRead(page, selector);
      assert.equal(dark.state, "dark", `${brand} dark state`);
      assert.equal(dark.theme, "light", `${brand} dark data-theme baseline`);
      assert.equal(dark.colorScheme, "dark", `${brand} dark data-color-scheme`);
      assert(dark.colors.every(({ content }) => content === expected.dark), `${brand} dark metadata`);

      const auto = await clickAndRead(page, selector);
      assert.equal(auto.state, "auto", `${brand} auto state`);
      assert.equal(auto.theme, "light", `${brand} auto data-theme baseline`);
      assert.equal(auto.colorScheme, null, `${brand} auto removes data-color-scheme`);
      assert.deepEqual(auto.colors.map(({ media, content }) => ({ media, content })), [
        { media: "(prefers-color-scheme: light)", content: expected.light },
        { media: "(prefers-color-scheme: dark)", content: expected.dark },
      ], `${brand} auto metadata`);
    } finally {
      await page.close();
    }
  }
});

test("all three theme controls survive disabled storage", async () => {
  const fixtures = [
    { name: "OKH", bodyClass: "", selector: ".theme-toggle" },
    { name: "Glee", bodyClass: "glee-main", selector: ".glee-color-toggle" },
    { name: "AskJamie", bodyClass: "askjamie-main", selector: ".glee-color-toggle" },
  ];

  for (const fixture of fixtures) {
    const pageErrors = [];
    const page = await openFixture({ bodyClass: fixture.bodyClass, storage: "blocked" });
    page.on("pageerror", (error) => pageErrors.push(error));
    try {
      const initial = await readState(page, fixture.selector);
      assert.equal(initial.state, fixture.name === "OKH" ? "system" : "auto", `${fixture.name} fallback state`);
      assert.equal(initial.theme, "light", `${fixture.name} fallback theme`);

      await clickAndRead(page, fixture.selector);
      await clickAndRead(page, fixture.selector);
      await clickAndRead(page, fixture.selector);

      const final = await readState(page, fixture.selector);
      assert.equal(final.state, fixture.name === "OKH" ? "system" : "auto", `${fixture.name} cycles without storage`);
      assert.equal(pageErrors.length, 0, `${fixture.name} has no storage exception`);
    } finally {
      await page.close();
    }
  }
});