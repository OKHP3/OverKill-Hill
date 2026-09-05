import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';

const base = process.argv.find(a => a.startsWith('--base='))?.slice(7) ?? 'http://127.0.0.1:5000';
const routes = [
  '/',
  '/writings/first-diagram-is-a-liar/',
  '/projects/mermaid-theme-builder/'
];
const commit = execFileSync('git', ['rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
const browser = await chromium.launch({ headless: true });
const version = browser.version();
const results = [];
for (const route of routes) {
  const context = await browser.newContext();
  const page = await context.newPage();
  const failed = [];
  page.on('requestfailed', request => failed.push({ url: request.url(), error: request.failure()?.errorText ?? 'unknown' }));
  const started = Date.now();
  await page.goto(base + route, { waitUntil: 'networkidle', timeout: 30000 });
  const navigationMs = Date.now() - started;
  const metrics = await page.evaluate(() => {
    const entries = performance.getEntriesByType('resource');
    const transfer = entries.reduce((n, e) => n + (e.transferSize || 0), 0);
    const encoded = entries.reduce((n, e) => n + (e.encodedBodySize || 0), 0);
    return { resourceCount: entries.length, transferBytes: transfer, encodedBodyBytes: encoded,
      resourceDurationMs: Math.round(entries.reduce((n, e) => n + e.duration, 0)),
      domContentLoadedMs: Math.round(performance.getEntriesByType('navigation')[0]?.domContentLoadedEventEnd ?? 0) };
  });
  results.push({ route, navigationMs, ...metrics, failedRequests: failed });
  await context.close();
}
await browser.close();
console.log(JSON.stringify({ schema: 'baseline-measurement/v1', measuredAt: new Date().toISOString(), commit,
  browser: { engine: 'chromium', version, headless: true }, cache: 'fresh context per route; browser cache empty',
  network: 'local HTTP server; no throttling', cpu: 'host default; no emulation', fieldData: 'unavailable; no INP/LCP distributions claimed', base, results }, null, 2));
