/** Render registry summaries at phone/desktop sizes, including noindex details. */
import { chromium } from 'playwright';
import { readFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import assert from 'node:assert/strict';
const base = process.argv.find(arg => arg.startsWith('--base-url='))?.slice(11) || 'http://127.0.0.1:5000';
const registry = JSON.parse(readFileSync(new URL('../site-src/project-status.json', import.meta.url), 'utf8'));
const browser = await chromium.launch({headless: true});
const output = mkdtempSync(join(tmpdir(), 'okh-a11-status-'));
let checks = 0;
try {
  for (const width of [320, 1280]) {
    const page = await browser.newPage({viewport: {width, height: 800}});
    await page.route('**/*', route => route.request().url().startsWith(base + '/') ? route.continue() : route.abort());
    const response = await page.request.get(base + '/site-src/project-status.json');
    assert.deepEqual(await response.json(), registry, 'Preview must serve the current registry');
    for (const route of ['/', '/projects/', ...registry.projects.filter(r => r.kind === 'detail').map(r => r.route)]) {
      await page.goto(base + route, {waitUntil: 'domcontentloaded'});
      const blocks = page.locator('[data-project-status]');
      assert.ok(await blocks.count() > 0, route);
      for (const block of await blocks.all()) {
        await block.scrollIntoViewIfNeeded();
        assert.ok(await block.isVisible(), route);
        const box = await block.boundingBox();
        assert.ok(box.x >= -1 && box.x + box.width <= width + 1, route + ' summary overflow');
      }
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1), false, route + ' document overflow');
      if (route === '/projects/') {
        await blocks.first().scrollIntoViewIfNeeded();
        await page.screenshot({path: join(output, `a11-project-status-${width}.png`)});
      }
      checks++;
    }
    await page.close();
  }
} finally {
  await browser.close();
}
console.log(`PASS ${checks} route/viewport checks, including noindex concepts; served registry matched candidate.`);

console.log(`Screenshots: ${output}`);
