#!/usr/bin/env node
// Local transfer experiment, not a production server or field-performance gate.
// Usage: node scripts/measure-page-costs.mjs --label=before --trials=3
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFileSync, statSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve, extname, sep } from 'node:path';
import { gzipSync } from 'node:zlib';
import { execFileSync } from 'node:child_process';

const arg = (name, fallback) => process.argv.find(v => v.startsWith(`--${name}=`))?.split('=').slice(1).join('=') ?? fallback;
const root = resolve(arg('root', '.'));
const label = arg('label', 'measurement');
if (!/^[a-z0-9-]+$/.test(label)) throw new Error('Use a lowercase hyphenated label');
const trials = Number(arg('trials', '3'));
if (!Number.isInteger(trials) || trials < 1 || trials > 10) throw new Error('trials must be 1..10');
const routes = arg('routes', '/,/writings/first-diagram-is-a-liar/,/writings/murderbird/,/projects/mermaid-theme-builder/').split(',');
const output = resolve(root, '.local', 'a16', label);
mkdirSync(output, { recursive: true });
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp', '.ico': 'image/x-icon', '.woff2': 'font/woff2' };
const server = createServer((req, res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    let file = resolve(root, `.${pathname}`);
    if (!file.startsWith(root + sep) && file !== root) throw new Error('outside root');
    if (statSync(file).isDirectory()) file = resolve(file, 'index.html');
    const extension = extname(file);
    let body = readFileSync(file);
    const headers = { 'Content-Type': types[extension] || 'application/octet-stream', 'Cache-Control': 'public, max-age=3600' };
    if (['.html', '.css', '.js', '.json', '.svg'].includes(extension)) {
      body = gzipSync(body, { level: 6 });
      headers['Content-Encoding'] = 'gzip';
    }
    headers['Content-Length'] = body.length;
    res.writeHead(200, headers).end(body);
  } catch { res.writeHead(404).end('Not found'); }
});
await new Promise(done => server.listen(0, '127.0.0.1', done));
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch();
const report = {
  schema: 'page-cost-experiment/v1', label, sourceCommit: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim(),
  timestamp: new Date().toISOString(), browser: browser.version(), node: process.version,
  conditions: { network: '20 Mbps down, 5 Mbps up, 40 ms latency', localDelivery: 'gzip level 6 for text; public max-age=3600; loopback ephemeral port', initialWindow: 'load plus 2000 ms', scroll: '800 px steps, 100 ms each, then 2000 ms', cold: 'new browser context for every trial and route', warm: 'same context; navigate about:blank then revisit; cache enabled', motion: 'reduce', theme: 'light', external: 'live, unmodified; external variability retained; CDP page target only, out-of-process iframe traffic may be absent', byteMeaning: 'CDP loadingFinished encodedDataLength, including response overhead; cached requests recorded separately; incomplete requests have no claimed byte length' },
  runs: [],
};
const safeUrl = value => { const u = new URL(value); return (u.origin === origin ? '' : u.origin) + u.pathname; };
try {
  for (const [device, viewport, dpr, cpu, mobile] of [
    ['desktop', { width: 1280, height: 800 }, 1, 1, false],
    ['phone', { width: 390, height: 844 }, 3, 4, true],
  ]) for (const route of routes) for (let trial = 1; trial <= trials; trial++) {
    const context = await browser.newContext({ viewport, deviceScaleFactor: dpr, isMobile: mobile, hasTouch: mobile, reducedMotion: 'reduce', colorScheme: 'light', serviceWorkers: 'block' });
    const page = await context.newPage();
    const cdp = await context.newCDPSession(page);
    await cdp.send('Network.enable');
    await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 40, downloadThroughput: 20_000_000 / 8, uploadThroughput: 5_000_000 / 8 });
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: cpu });
    await page.addInitScript(() => {
      window.__costLongTasks = [];
      new PerformanceObserver(list => window.__costLongTasks.push(...list.getEntries().map(e => e.duration))).observe({ type: 'longtask', buffered: true });
    });
    let requests = new Map();
    cdp.on('Network.requestWillBeSent', e => {
      if (/^https?:/.test(e.request.url)) requests.set(e.requestId, { url: safeUrl(e.request.url), firstParty: e.request.url.startsWith(origin + '/'), type: e.type, finished: false });
    });
    cdp.on('Network.responseReceived', e => { const r = requests.get(e.requestId); if (r) Object.assign(r, { status: e.response.status, cached: Boolean(r.cached || e.response.fromDiskCache || e.response.fromPrefetchCache), mime: e.response.mimeType }); });
    cdp.on('Network.requestServedFromCache', e => { const r = requests.get(e.requestId); if (r) r.cached = true; });
    cdp.on('Network.loadingFinished', e => { const r = requests.get(e.requestId); if (r) Object.assign(r, { finished: true, encodedBytes: e.encodedDataLength }); });
    cdp.on('Network.loadingFailed', e => { const r = requests.get(e.requestId); if (r) r.failure = e.errorText; });
    for (const cache of ['cold', 'warm']) {
      requests = new Map();
      const errors = [];
      try { await page.goto(origin + route, { waitUntil: 'load', timeout: 45000 }); } catch (e) { errors.push(e.message.split('\n')[0]); }
      await page.waitForTimeout(2000);
      const initial = structuredClone([...requests.values()]);
      const height = await page.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < height; y += 800) { await page.evaluate(y => window.scrollTo(0, y), y); await page.waitForTimeout(100); }
      await page.waitForTimeout(2000);
      const runtime = await page.evaluate(() => ({
        longTasks: window.__costLongTasks, navigation: performance.getEntriesByType('navigation').map(e => ({ loadMs: e.loadEventEnd, domContentLoadedMs: e.domContentLoadedEventEnd })),
        fonts: document.fonts.status,
        images: [...document.images].map(img => ({ src: new URL(img.currentSrc || img.src).pathname, complete: img.complete, width: img.naturalWidth, displayedWidth: img.getBoundingClientRect().width })),
      }));
      const summarize = entries => ({ firstPartyBytes: entries.filter(r => r.firstParty).reduce((s, r) => s + (r.encodedBytes || 0), 0), externalBytes: entries.filter(r => !r.firstParty).reduce((s, r) => s + (r.encodedBytes || 0), 0), cached: entries.filter(r => r.cached).length, failed: entries.filter(r => r.failure).length, incomplete: entries.filter(r => !r.finished && !r.failure).length });
      report.runs.push({ device, viewport, dpr, cpu, route, trial, cache, initial: summarize(initial), scrolled: summarize([...requests.values()]), initialRequests: initial, requests: [...requests.values()], runtime, errors });
      writeFileSync(resolve(output, 'transfers.json'), JSON.stringify(report, null, 2) + '\n');
      console.log(JSON.stringify({ device, route, trial, cache, initial: summarize(initial), scrolled: summarize([...requests.values()]) }));
      await page.goto('about:blank');
    }
    await context.close();
  }
} finally { await browser.close(); await new Promise(done => server.close(done)); }
