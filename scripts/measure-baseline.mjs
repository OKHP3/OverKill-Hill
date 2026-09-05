import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';

const base = process.argv.find(a => a.startsWith('--base='))?.slice(7) ?? 'http://127.0.0.1:5051';
const viewport = { width: 1280, height: 720 };
const routes = [
  '/',
  '/writings/first-diagram-is-a-liar/',
  '/projects/mermaid-theme-builder/'
];
const git = args => execFileSync('git', args, { encoding: 'utf8' }).trim();
const sha256 = value => createHash('sha256').update(value).digest('hex');
const commit = git(['rev-parse', 'HEAD']);
const scriptPath = 'scripts/measure-baseline.mjs';
const routeFiles = new Map(routes.map(route => [route, route === '/' ? 'index.html' : `.${route}index.html`]));
const sourceFiles = Object.fromEntries([...routeFiles].map(([route, file]) => {
  const body = readFileSync(file);
  return [route, { file, gitBlobSha: git(['rev-parse', `HEAD:${file}`]), workingTreeSha256: sha256(body) }];
}));
const sourceState = {
  commit,
  workingTreeStatus: git(['status', '--short']),
  measurementScript: { path: scriptPath, workingTreeSha256: sha256(readFileSync(scriptPath)) }
};
let browser;
let version;
const results = [];
try {
  browser = await chromium.launch({ headless: true });
  version = browser.version();
  for (const route of routes) {
    const samples = [];
    for (let sample = 0; sample < 3; sample++) {
      const context = await browser.newContext({ viewport });
      try {
        const page = await context.newPage();
        const failed = [];
        page.on('requestfailed', request => failed.push({ url: request.url().split('?')[0], error: request.failure()?.errorText ?? 'unknown' }));
        const started = Date.now();
        const response = await page.goto(base + route, { waitUntil: 'networkidle', timeout: 30000 });
        if (!response?.ok()) throw new Error(`Top document request failed for ${route}: ${response?.status() ?? 'no response'}`);
        const observedDocumentSha256 = sha256(await response.body());
        const sourceMatch = observedDocumentSha256 === sourceFiles[route].workingTreeSha256;
        if (!sourceMatch) throw new Error(`Served document does not match ${sourceFiles[route].file} for ${route}`);
        const networkIdleNavigationMs = Date.now() - started;
        const metrics = await page.evaluate(() => {
          const entries = performance.getEntriesByType('resource');
          const transfer = entries.reduce((n, e) => n + (e.transferSize || 0), 0);
          const encoded = entries.reduce((n, e) => n + (e.encodedBodySize || 0), 0);
          return { resourceCount: entries.length, transferBytes: transfer, encodedBodyBytes: encoded,
            resourceDurationMs: Math.round(entries.reduce((n, e) => n + e.duration, 0)),
            domContentLoadedMs: Math.round(performance.getEntriesByType('navigation')[0]?.domContentLoadedEventEnd ?? 0) };
        });
        samples.push({ networkIdleNavigationMs, ...metrics, servedDocumentSha256: observedDocumentSha256, sourceMatch, failedRequests: failed });
      } finally {
        await context.close();
      }
    }
    const median = key => [...samples].map(s => s[key]).sort((a,b) => a-b)[1];
    results.push({ route, samples, median: { networkIdleNavigationMs: median('networkIdleNavigationMs'), domContentLoadedMs: median('domContentLoadedMs'), transferBytes: median('transferBytes') }, ranges: { networkIdleNavigationMs: [Math.min(...samples.map(s=>s.networkIdleNavigationMs)), Math.max(...samples.map(s=>s.networkIdleNavigationMs))], domContentLoadedMs: [Math.min(...samples.map(s=>s.domContentLoadedMs)), Math.max(...samples.map(s=>s.domContentLoadedMs))], transferBytes: [Math.min(...samples.map(s=>s.transferBytes)), Math.max(...samples.map(s=>s.transferBytes))] } });
  }
} finally {
  await browser?.close();
}
const output = JSON.stringify({ schema: 'baseline-measurement/v2', measuredAt: new Date().toISOString(), sourceState, sourceFiles,
  browser: { engine: 'chromium', version, headless: true, viewport }, cache: 'fresh context per sample; browser cache empty',
  network: 'local HTTP server; no throttling', cpu: 'host default; no emulation', fieldData: 'unavailable; no INP/LCP distributions claimed', base, results }, null, 2);
const outputPath = process.argv.find(a => a.startsWith('--output='))?.slice(9);
if (outputPath) writeFileSync(outputPath, `${output}\n`);
console.log(output);
