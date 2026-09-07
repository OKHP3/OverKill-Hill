import assert from 'node:assert/strict';
import { test } from 'node:test';
import { chromium } from 'playwright';

const base = process.env.REVEAL_BASE_URL || 'http://127.0.0.1:18303';
const scenarios = ['disabled', 'blocked', 'initialization-failure', 'missing-observer',
  'constructor-failure', 'observe-failure', 'callback-failure', 'silent-observer', 'normal', 'reduced'];

for (const { width, scenario } of [1280, 390].flatMap(width =>
  scenarios.map(scenario => ({ width, scenario })))) {
  test(`homepage content and links survive ${scenario} at ${width}px`, async () => {
    const browser = await chromium.launch();
    try {
      const page = await browser.newPage({ viewport: { width, height: 800 },
        javaScriptEnabled: scenario !== 'disabled',
        reducedMotion: scenario === 'reduced' ? 'reduce' : 'no-preference' });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      // Keep external services out of this local runtime regression.
      await page.route('**/*', route => new URL(route.request().url()).origin === base
        ? route.continue() : route.abort());
      if (scenario === 'blocked' || scenario === 'initialization-failure') {
        await page.route('**/assets/js/app.js*', route => scenario === 'blocked'
          ? route.abort() : route.fulfill({ contentType: 'text/javascript',
            body: 'throw new Error("Injected app initialization failure")' }));
      }
      await page.addInitScript(mode => {
        window.revealAnimations = [];
        document.addEventListener('animationstart', event => window.revealAnimations.push(event.animationName));
        if (mode === 'missing-observer') delete window.IntersectionObserver;
        if (mode === 'constructor-failure') window.IntersectionObserver = class {
          constructor() { throw new Error('Injected observer constructor failure'); }
        };
        if (['observe-failure', 'callback-failure', 'silent-observer'].includes(mode)) {
          window.IntersectionObserver = class {
            constructor(callback) { this.callback = callback; }
            observe(target) {
              if (mode === 'observe-failure') throw new Error('Injected observe failure');
              if (mode === 'callback-failure') setTimeout(() => this.callback([
                { target, isIntersecting: true }
              ]), 0);
            }
            unobserve() { throw new Error('Injected callback failure'); }
            disconnect() {}
          };
        }
      }, scenario);
      await page.goto(base, { waitUntil: 'load' });
      assert.match(await page.title(), /OverKill/);
      assert.ok(await page.locator('h1').innerText());
      const checkPaint = async () => {
        const hidden = await page.locator('.reveal-on-scroll').evaluateAll(nodes => nodes
          .filter(node => {
            const style = getComputedStyle(node);
            return Number(style.opacity) < 1 || style.visibility !== 'visible' || style.display === 'none';
          }).map(node => node.id || node.className));
        assert.deepEqual(hidden, [], 'Every reveal section must remain painted, including offscreen content');
      };
      await checkPaint();
      assert.ok(await page.locator('.hero-illustration').evaluate(img => img.complete && img.naturalWidth > 0));
      if (process.env.REVEAL_SCREENSHOT_DIR && scenario === 'disabled') {
        await page.screenshot({ path: `${process.env.REVEAL_SCREENSHOT_DIR}/a03-disabled-${width}.png` });
      }
      if (scenario === 'normal' && width === 1280) {
        await page.waitForFunction(() => window.revealAnimations.includes('scroll-reveal-slide'));
      }
      if (!['disabled', 'blocked', 'initialization-failure'].includes(scenario)) {
        await page.locator('.okh-skip-link').focus();
        await page.keyboard.press('Enter');
        assert.equal(new URL(page.url()).hash, '#main');
        assert.equal(await page.evaluate(() => document.activeElement.id), 'main');
      }
      await page.locator('#start-here-heading').scrollIntoViewIfNeeded();
      await checkPaint();
      if (scenario === 'reduced' || width === 390) {
        assert.equal(await page.locator('.reveal-on-scroll').first().evaluate(node =>
          getComputedStyle(node).animationName), 'none');
      }
      await page.locator('a[href="/contact/"]').filter({ hasText: 'contact page' }).click();
      assert.equal(new URL(page.url()).pathname, '/contact/');
      if (scenario === 'initialization-failure') assert.ok(errors.some(error => error.includes('Injected')));
      else assert.deepEqual(errors, []);
    } finally { await browser.close(); }
  });
}
