import assert from "node:assert/strict";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { after, before, test } from "node:test";
import { dirname, extname, resolve } from "node:path";
import { chromium } from "playwright";

const testsDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = resolve(testsDirectory, "..");
let server;
let baseUrl;

function contentTypeFor(pathname) {
  const ext = extname(pathname).toLowerCase();
  return { ".css": "text/css; charset=utf-8", ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp" }[ext] || "text/plain; charset=utf-8";
}

async function serveFile(request, response) {
  const url = new URL(request.url, "http://search-test");
  let pathname = url.pathname;
  if (pathname.endsWith("/")) pathname += "index.html";
  const filePath = resolve(repositoryRoot, "." + pathname);
  if (!filePath.startsWith(repositoryRoot)) { response.writeHead(403); response.end("forbidden"); return; }
  try { const body = await readFile(filePath); response.writeHead(200, { "content-type": contentTypeFor(filePath) }); response.end(body); }
  catch { response.writeHead(404, { "content-type": "text/plain; charset=utf-8" }); response.end("missing"); }
}

before(async () => {
  server = createServer((request, response) => serveFile(request, response).catch((error) => { response.writeHead(500); response.end(error.message); }));
  await new Promise((resolveListen) => server.listen(0, "127.0.0.1", resolveListen));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});
after(async () => { await new Promise((resolveClose, rejectClose) => server.close((error) => error ? rejectClose(error) : resolveClose())); });


const frenchEntries = [
  {url: "/fr/projects/", title: "Projets éprouvés", category: "Project", description: "protocoles", body: "protocoles"},
  {url: "/fr/about/", title: "À propos", category: "Brand", description: "protocoles", body: "protocoles"},
];

test("French overlay keeps localized counts, safe queries, focused links, and an explicit English fallback", async () => {
  const browser = await chromium.launch({headless: true});
  const page = await browser.newPage({viewport: {width: 390, height: 844}});
  try {
    await page.route("**/assets/data/search-index.fr.json", route => route.fulfill({contentType: "application/json", body: JSON.stringify({entries: frenchEntries})}));
    await page.goto(baseUrl + "/fr/", {waitUntil: "networkidle"});
    const trigger = page.locator(".okh-search-trigger");
    assert.match(await trigger.getAttribute("aria-label"), /Ouvrir la recherche/);
    assert.equal(await trigger.locator(".okh-search-label").textContent(), "Rechercher");
    await trigger.click();
    const overlay = page.getByRole("dialog", {name: "Rechercher sur OverKill Hill"});
    const input = overlay.getByRole("searchbox", {name: "Rechercher", exact: true});
    const status = overlay.locator(".okh-search-status");
    await page.waitForFunction(() => document.querySelector(".okh-search-status").textContent.startsWith("La recherche est prête"));
    await input.fill("protocoles");
    assert.equal(await status.textContent(), "2 résultats trouvés pour protocoles.");
    assert.deepEqual(await overlay.locator(".okh-search-result-cat").allTextContents(), ["Projet", "Marque"]);
    await input.press("ArrowDown");
    assert.equal(await overlay.locator(".okh-search-result").first().evaluate(el => el === document.activeElement), true);
    await page.keyboard.press("ArrowUp");
    assert.equal(await input.evaluate(el => el === document.activeElement), true);
    await input.fill("eprouves");
    assert.equal(await status.textContent(), "1 résultat trouvé pour eprouves.");
    await input.fill('<img src=x onerror=alert(1)>');
    assert.equal(await overlay.locator(".okh-search-results img").count(), 0);
    assert.match(await status.textContent(), /^Aucun résultat de recherche pour /);
    await input.fill("protocoles");
    const fallback = overlay.getByRole("link", {name: "Ouvrir la recherche complète (contenu en anglais) →"});
    assert.equal(await fallback.getAttribute("href"), "/search/?q=protocoles");
    const overflow = await overlay.evaluate(el => el.scrollWidth > el.clientWidth);
    assert.equal(overflow, false);
    await page.keyboard.press("Escape");
    assert.equal(await trigger.evaluate(el => el === document.activeElement), true);
    await trigger.click();
    await fallback.click();
    await page.waitForURL("**/search/?q=protocoles");
    assert.match(await page.locator("html").getAttribute("lang"), /^en/);
  } finally { await browser.close(); }
});

test("French loading, failure, retry, and empty-index states remain distinct", async () => {
  const browser = await chromium.launch({headless: true});
  const page = await browser.newPage();
  let release;
  const pending = new Promise(resolve => {release = resolve;});
  let count = 0;
  try {
    await page.route("**/assets/data/search-index.fr.json", async route => {
      count += 1;
      if (count === 1) { await pending; await route.fulfill({status: 503, body: "unavailable"}); }
      else await route.fulfill({contentType: "application/json", body: '{"entries":[]}'});
    });
    await page.goto(baseUrl + "/fr/", {waitUntil: "domcontentloaded"});
    await page.locator(".okh-search-trigger").click();
    const status = page.locator(".okh-search-status");
    assert.equal(await status.textContent(), "Chargement de l’index de recherche…");
    await page.locator(".okh-search-input").fill("projets");
    release();
    await page.getByRole("button", {name: "Réessayer de charger l’index"}).waitFor();
    assert.equal(await status.textContent(), "Impossible de charger l’index de recherche.");
    await page.getByRole("button", {name: "Réessayer de charger l’index"}).click();
    await page.waitForFunction(() => document.querySelector(".okh-search-status").textContent === "Aucune page indexée n’est disponible.");
    assert.equal(await page.locator(".okh-search-input").inputValue(), "projets");
    assert.equal(count, 2);
  } finally { release(); await browser.close(); }
});

test("all four French language controls and every theme action are localized", async () => {
  const browser = await chromium.launch({headless: true});
  const context = await browser.newContext();
  const page = await context.newPage();
  try {
    for (const route of ["/fr/", "/fr/about/", "/fr/projects/", "/fr/contact/"]) {
      await page.goto(baseUrl + route, {waitUntil: "networkidle"});
      assert.equal(await page.locator(".lang-switch-toggle").getAttribute("aria-label"), "Langue : Français (France)");
    }
    await page.evaluate(() => localStorage.removeItem("okh-theme"));
    await page.reload({waitUntil: "networkidle"});
    const theme = page.locator(".theme-toggle");
    for (const label of ["Passer au mode clair", "Passer au mode sombre", "Utiliser le thème du système", "Passer au mode clair"]) {
      assert.equal(await theme.getAttribute("aria-label"), label);
      await theme.click();
    }
    await page.goto(baseUrl + "/");
    assert.match(await page.locator(".theme-toggle").getAttribute("aria-label"), /^Switch to/);
  } finally { await browser.close(); }
});
