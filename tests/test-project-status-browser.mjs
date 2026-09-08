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
    assert.equal(response.status(), 404, 'Private registry must not be served');
    for (const route of ['/', '/projects/', ...registry.projects.filter(r => r.kind === 'detail').map(r => r.route)]) {
      const publicResponse = await page.goto(base + route, {waitUntil: 'domcontentloaded'});
      assert.ok(publicResponse, route + ' navigation must return HTML');
      assert.equal(publicResponse.status(), 200, route + ' public HTML status');
      const candidate = readFileSync(new URL('..' + route + 'index.html', import.meta.url));
      assert.deepEqual(await publicResponse.body(), candidate, route + ' served HTML must match local candidate bytes');
      const blocks = page.locator('[data-project-status]');
      assert.ok(await blocks.count() > 0, route);
      const expected = route === '/projects/' ? registry.projects.filter(r => r.shelf) : registry.projects.filter(r => r.kind === 'detail' && r.route === route);
      if (expected.length) {
        assert.deepEqual((await blocks.evaluateAll(nodes => nodes.map(node => node.dataset.projectStatus))).sort(),
          expected.map(record => record.id).sort(), route + ' status record coverage');
      }
      for (const block of await blocks.all()) {
        const id = await block.getAttribute('data-project-status');
        const record = registry.projects.find(record => record.id === id);
        assert.ok(record, route + ' unknown status record ' + id);
        const expectedText = `Availability: ${record.availability}. Maturity: ${record.maturity}. Evidence: ${record.evidence.summary} Delivery: ${record.evidence.delivery}.`;
        assert.equal(await block.locator('[data-project-status-text]').textContent(), expectedText, route + ' canonical status text');
        assert.equal(await block.locator('a').getAttribute('href'), record.evidence.url, route + ' evidence source');
        assert.ok((await block.textContent()).includes(`(reviewed ${record.reviewed}).`), route + ' evidence review date');
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
console.log(`PASS ${checks} route/viewport checks, including noindex concepts; public HTML matched candidate bytes, rendered status matched local registry, private registry returned 404.`);

console.log(`Screenshots: ${output}`);
