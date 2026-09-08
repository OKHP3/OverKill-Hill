#!/usr/bin/env node
// Run against a loopback preview of the candidate homepage.
// Usage: node scripts/check-etch-parity.mjs --base=http://127.0.0.1:8166
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';

const base = process.argv.find(v => v.startsWith('--base='))?.slice(7) || 'http://127.0.0.1:8166';
assert(['127.0.0.1', 'localhost'].includes(new URL(base).hostname), 'Use a loopback preview');
const output = '.local/a16/parity';
mkdirSync(output, { recursive: true });
const browser = await chromium.launch();
const rows = [];
try {
  for (const [device, width, height, dpr] of [['desktop', 1280, 800, 1], ['phone', 390, 844, 3]]) {
    for (const theme of ['light', 'dark']) {
      const context = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: dpr, reducedMotion: 'reduce', colorScheme: theme });
      const page = await context.newPage();
      // Isolate image rendering; fonts and external content are outside this check.
      await page.route('https://**/*', route => route.abort());
      await page.goto(base);
      assert.equal(await page.locator('html').getAttribute('data-theme'), theme);
      const img = page.locator('.latest-image img');
      assert.equal(await page.locator('.latest-image picture source').count(), 1);
      await img.scrollIntoViewIfNeeded();
      await img.evaluate(i => i.decode());
      const candidate = await img.evaluate(i => new URL(i.currentSrc).pathname);
      assert(candidate.endsWith('-lossless.webp'));
      const after = await img.boundingBox();
      await img.screenshot({ path: `${output}/${device}-${theme}-after.png` });
      await page.locator('.latest-image picture').evaluate(p => { const i = p.querySelector('img'); p.replaceWith(i); });
      await img.evaluate(i => i.decode());
      const before = await img.boundingBox();
      assert.deepEqual(after, before, 'Image geometry changed');
      assert((await img.evaluate(i => i.currentSrc)).endsWith('.png'));
      await img.screenshot({ path: `${output}/${device}-${theme}-before.png` });
      rows.push({ device, theme, before, after, candidate });
      await context.close();
    }
  }
} finally { await browser.close(); }
const python = process.platform === 'win32' ? 'py' : 'python3';
const code = `from PIL import Image, ImageChops, ImageStat
from pathlib import Path
import json
rows=[]
for p in Path('${output}').glob('*-before.png'):
 a=Image.open(p).convert('RGB'); b=Image.open(str(p).replace('-before','-after')).convert('RGB')
 assert a.size == b.size
 d=ImageChops.difference(a,b)
 maximum=max(high for low,high in d.getextrema())
 assert maximum <= 1, f'{p}: rendered pixel difference {maximum} exceeds 1/255'
 rows.append(dict(file=p.name,max_channel_difference=maximum,mean_channel_difference=ImageStat.Stat(d).mean))
assert len(rows)==4
print(json.dumps(rows))`;
const pixels = JSON.parse(execFileSync(python, [...(process.platform === 'win32' ? ['-3'] : []), '-c', code], { encoding: 'utf8' }));
writeFileSync(`${output}/result.json`, JSON.stringify({ browser: browser.version(), geometry: rows, pixels, scope: 'Image crop only; external requests blocked. Source RGBA bytes are exact; browser scaling permits 1/255 channel rounding.' }, null, 2) + '\n');
console.log('PASS: four theme/device image comparisons, exact geometry, maximum channel difference <= 1/255.');
