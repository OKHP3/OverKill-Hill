import assert from 'node:assert/strict';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import {chromium} from 'playwright';

const root = path.resolve(import.meta.dirname, '..');
const server = http.createServer((request, response) => {
  const route = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
  let file = path.resolve(root, '.' + route);
  if (!file.startsWith(root + path.sep)) { response.writeHead(403).end(); return; }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  const type = file.endsWith('.mjs') || file.endsWith('.js') ? 'text/javascript' : file.endsWith('.css') ? 'text/css' : file.endsWith('.html') ? 'text/html' : 'application/octet-stream';
  try { response.setHeader('Content-Type', type); response.end(fs.readFileSync(file)); }
  catch { response.writeHead(404).end(); }
});
await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const browser = await chromium.launch({headless: true});
try {
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/universe/`);
  await page.locator('.universe-diagram svg').first().waitFor();
  await page.locator('.universe-generated details').evaluateAll((items) => items.forEach((item) => { item.open = true; }));
  const total = await page.locator('.universe-diagram').count();
  await page.waitForFunction((count) => document.querySelectorAll('.universe-diagram[data-rendered="true"]').length === count, total);
  assert.ok(await page.locator('.universe-diagram svg a[href="/projects/skillz/"]').count());
  assert.equal(await page.locator('.universe-generated li a[href="/projects/skillz/"]').count(), 1);
  for (const width of [390, 1440]) {
    await page.setViewportSize({width, height: 900});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1), false, `overflow at ${width}`);
    if (width === 390) {
      assert.ok(await page.locator('.universe-diagram').first().evaluate((element) => element.scrollWidth > element.clientWidth));
    }
  }
  await page.evaluate(() => document.documentElement.setAttribute('data-color-scheme', 'light'));
  await page.waitForFunction((count) => document.querySelectorAll('.universe-diagram[data-rendered="true"]').length === count, total);
  assert.deepEqual(errors, []);
  const offline = await browser.newContext({javaScriptEnabled: false});
  const plain = await offline.newPage();
  await plain.goto(`http://127.0.0.1:${server.address().port}/universe/`);
  assert.ok(await plain.locator('.universe-generated li a[href]').count() >= 31);
  assert.equal(await plain.locator(".universe-diagram:visible").count(), 0);
  await offline.close();
  console.log(`PASS: ${total} diagrams, SVG links, 31-page outline, two widths, theme switch, and no-JavaScript fallback`);
} finally {
  await browser.close();
  server.close();
}
