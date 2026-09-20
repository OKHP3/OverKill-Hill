import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { chromium } from 'playwright';

const base = process.argv.find(arg => arg.startsWith('--base-url='))?.slice(11)
  || 'http://127.0.0.1:5000';
const manifest = JSON.parse(readFileSync(new URL('../assets/fonts/provenance.json', import.meta.url)));
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage();
  const externalFonts = [];
  const localFonts = new Map();
  page.on('request', request => {
    if (['fonts.googleapis.com', 'fonts.gstatic.com'].includes(new URL(request.url()).hostname)) {
      externalFonts.push(request.url());
    }
  });
  page.on('response', response => {
    const path = new URL(response.url()).pathname;
    if (path.startsWith('/assets/fonts/')) {
      localFonts.set(path, { status: response.status(), type: response.headers()['content-type'] });
    }
  });
  // External services must not be needed to load the site's typography.
  await page.route('**/*', route => new URL(route.request().url()).origin === new URL(base).origin
    ? route.continue() : route.abort());
  await page.goto(base, { waitUntil: 'networkidle' });
  const loaded = await page.evaluate(async () => {
    const requests = ['400 18px "Alfa Slab One"', '400 18px "DM Sans"',
      '500 18px "DM Sans"', '600 18px "DM Sans"',
      '400 18px "JetBrains Mono"', '700 18px "JetBrains Mono"'];
    const results = [];
    for (const font of requests) {
      const faces = await document.fonts.load(font, 'Brand ABC Ā Ă Ж Ѡ Ω Ắ');
      results.push({ font, count: faces.length, loaded: faces.every(face => face.status === 'loaded') });
    }
    return results;
  });
  for (const result of loaded) {
    assert.ok(result.count > 0 && result.loaded, `Font failed: ${JSON.stringify(result)}`);
  }
  assert.deepEqual(externalFonts, [], 'A page still requested Google Fonts');
  for (const item of manifest.files) {
    const response = localFonts.get(`/assets/fonts/${item.file}`);
    assert.ok(response, `Font subset was not requested: ${item.file}`);
    assert.equal(response.status, 200, item.file);
    assert.match(response.type, /^font\/woff2(?:;|$)/, item.file);
  }
  console.log(JSON.stringify({ weights: loaded, localSubsets: localFonts.size, externalFontRequests: externalFonts.length }, null, 2));
} finally {
  await browser.close();
}
