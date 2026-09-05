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

function makeSearchEntries() {
  const entries = [];
  for (let i = 1; i <= 60; i += 1) entries.push({ url: `/brand-${String(i).padStart(2, "0")}/`, title: `Brand ${i}`, category: "Brand", description: `omega brand ${i}`, headings: [], body: `omega brand ${i}` });
  entries.push({ url: "/project-61/", title: "Project 61", category: "Project", description: "omega project 61", headings: [], body: "omega project 61" });
  for (let i = 62; i <= 80; i += 1) entries.push({ url: `/project-${i}/`, title: `Project ${i}`, category: "Project", description: `omega project ${i}`, headings: [], body: `omega project ${i}` });
  return entries;
}

async function openSearchPage(page, indexResponder, path = "/search/?q=omega&cat=Project") {
  let requestCount = 0;
  await page.route("**/assets/data/search-index.json", async (route) => { requestCount += 1; await indexResponder(route, requestCount); });
  await page.goto(`${baseUrl}${path}`, { waitUntil: "networkidle" });
  return () => requestCount;
}

test("shows a retry when the search index fails, then recovers on retry", async () => {
  const browser = await chromium.launch({ headless: true }); const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  try {
    let firstRequest = true;
    const count = await openSearchPage(page, async (route) => { if (firstRequest) { firstRequest = false; await route.fulfill({ status: 503, contentType: "application/json", body: "{}" }); } else await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ count: 80, entries: makeSearchEntries() }) }); });
    await assert.match(await page.locator(".okh-search-noresults--error").innerText(), /Search could not load the index/i);
    await page.locator(".okh-search-retry").click(); await page.waitForTimeout(1000);
    assert.equal(count() >= 2, true); await assert.match(await page.locator("#search-results").innerText(), /Project 61/);
  } finally { await browser.close(); }
});

test("filters before the global cap and restores URL state", async () => {
  const browser = await chromium.launch({ headless: true }); const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  try {
    await openSearchPage(page, async (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ count: 80, entries: makeSearchEntries() }) }));
    await page.getByRole("button", { name: /^Project \(/ }).click(); assert.equal(page.url().includes("cat=Project"), true); await assert.match(await page.locator("#search-results").innerText(), /Project 61/);
    await page.getByRole("button", { name: /^Brand \(/ }).click(); await page.goBack(); assert.equal(page.url().includes("cat=Project"), true);
  } finally { await browser.close(); }
});

test("normalizes an unknown category and restores an empty query", async () => {
  const browser = await chromium.launch({ headless: true }); const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  try {
    await openSearchPage(page, async (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ entries: makeSearchEntries() }) }), "/search/?q=omega&cat=NotARealCategory");
    await assert.equal(await page.locator("#search-page-input").inputValue(), "omega"); await assert.equal(await page.locator('[data-cat="all"]').getAttribute("aria-pressed"), "true");
    await page.evaluate(() => window.history.pushState({}, "", "/search/")); await page.evaluate(() => window.dispatchEvent(new PopStateEvent("popstate"))); await assert.equal(await page.locator("#search-page-input").inputValue(), "");
  } finally { await browser.close(); }
});

test("contains overlay index failures without an unhandled rejection", async () => {
  const browser = await chromium.launch({ headless: true }); const page = await browser.newPage({ viewport: { width: 1280, height: 900 } }); const errors = []; let requests = 0; page.on("pageerror", (error) => errors.push(error.message));
  try {
    await page.route("**/assets/data/search-index.json", async (route) => { requests += 1; await route.fulfill(requests === 1 ? { status: 503, contentType: "application/json", body: "{}" } : { status: 200, contentType: "application/json", body: JSON.stringify({ entries: makeSearchEntries() }) }); });
    await page.goto(`${baseUrl}/`, { waitUntil: "networkidle" }); await page.getByRole("button", { name: "Search" }).click(); await page.locator(".okh-search-overlay .okh-search-noresults--error").waitFor(); await page.locator(".okh-search-overlay .okh-search-retry").click(); await page.waitForLoadState("networkidle"); assert.equal(requests >= 2, true); assert.deepEqual(errors, []);
  } finally { await browser.close(); }
});

test("preserves an overlay query entered while the index is loading", async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  try {
    await page.route("**/assets/data/search-index.json", async (route) => {
      await new Promise((resolveDelay) => setTimeout(resolveDelay, 500));
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          entries: [{
            url: "/resume-builder/",
            title: "Resume Builder",
            category: "Tool",
            description: "Build a clear resume",
            headings: [],
            body: "resume guidance",
          }],
        }),
      });
    });
    await page.goto(`${baseUrl}/`, { waitUntil: "domcontentloaded" });
    await page.getByRole("button", { name: "Search" }).click();
    await page.locator(".okh-search-input").fill("resume");
    await page.locator('.okh-search-result[href="/resume-builder/"]').waitFor();
    await assert.match(await page.locator(".okh-search-status").innerText(), /1 result found/i);
    await assert.equal(await page.locator(".okh-search-input").inputValue(), "resume");
    await assert.equal(await page.locator('.okh-search-results > [role="listitem"]').count(), 1);
    await assert.equal(await page.getByRole("link", { name: /Resume Builder/ }).getAttribute("href"), "/resume-builder/");
  } finally {
    await browser.close();
  }
});
