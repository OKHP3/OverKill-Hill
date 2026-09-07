/** Render real text and the complete accepted illustration; no image-model typography. */
import { chromium } from 'playwright';
import { createHash } from 'node:crypto';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = 'assets/img/library/murderbird-unified-master-candidate-03-2026-09-06.png';
const output = 'assets/img/og/murderbird-story-share-2026-09-06.png';
const review = '.local/murderbird-review/social/murderbird-story-share.html';
const expected = '538c51bcdbf5bfce95a0932fdbbb0f5868b446f4985346d15e6cacd32430e633';
const digest = data => createHash('sha256').update(data).digest('hex');
const bytes = await readFile(path.join(root, source));
if (digest(bytes) !== expected) throw new Error('Accepted artwork changed: renewed review required.');
const theme = await readFile(path.join(root, 'assets/css/theme.css'), 'utf8');
const fonts = 'https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap';
const html = `<!doctype html><html lang="en-US"><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>MurderBird story share composition - local review</title><link rel="stylesheet" href="${fonts}"><style>${theme}
html,body{width:1200px;height:630px;margin:0;overflow:hidden;background:var(--okh-espresso);color:var(--okh-paper)}
main{height:630px;display:grid;grid-template-columns:400px 680px;gap:24px;padding:44px 48px 72px;position:relative;box-sizing:border-box}
.copy{align-self:center;z-index:1}.eyebrow{font:14px var(--font-mono);letter-spacing:2px;color:var(--okh-amber);margin:0 0 22px}
h1{font:48px/1.15 var(--font-heading);color:var(--okh-paper);margin:0 0 20px;letter-spacing:-1px}
h2{font:26px/1.25 var(--font-body);color:var(--okh-paper);margin:0 0 24px}
.deck{font:19px/1.55 var(--font-body);margin:0;max-width:320px;color:var(--color-fg)}
img{width:680px;height:auto;align-self:center;display:block;border-radius:8px}
footer{position:absolute;left:48px;right:48px;bottom:28px;display:flex;justify-content:space-between;align-items:center;border-top:2px solid var(--okh-orange);padding-top:16px;font:14px var(--font-mono)}
.brand{white-space:nowrap;color:var(--okh-paper)}.url{color:var(--color-muted)}
</style><main><div class="copy"><p class="eyebrow">A MYTH IN THREE ERAS</p><h1>The MurderBird</h1><h2>What the Water Kept</h2><p class="deck">An ancient body.<br>An industrial resurrection.<br>A heart and mind of its own.</p></div><img src="data:image/png;base64,${bytes.toString('base64')}" alt="The floor-standing MurderBird beside a workbench and CRT computer."><footer><span class="brand">OverKill&nbsp;Hill&nbsp;P³™</span><span class="url">overkillhill.com/writings/murderbird/</span></footer></main></html>`;
await mkdir(path.dirname(path.join(root, review)), { recursive:true });
await writeFile(path.join(root, review), html);
const browser = await chromium.launch({ headless:true });
try {
  const page = await browser.newPage({ viewport:{width:1200,height:630}, deviceScaleFactor:1 });
  await page.setContent(html, {waitUntil:'networkidle'});
  await page.evaluate(async () => {
    await Promise.all(['48px "Alfa Slab One"','19px "DM Sans"','14px "JetBrains Mono"'].map(f => document.fonts.load(f)));
    await document.fonts.ready;
    for (const family of ['Alfa Slab One','DM Sans','JetBrains Mono']) {
      if (![...document.fonts].some(f => f.family.replaceAll('"','') === family && f.status === 'loaded')) throw new Error(`Font not loaded: ${family}`);
    }
    await document.images[0].decode();
    const img = document.images[0], box = img.getBoundingClientRect();
    if (Math.abs(box.width / box.height - img.naturalWidth / img.naturalHeight) > .001) throw new Error('Art aspect ratio changed.');
    if (document.documentElement.scrollWidth !== 1200 || document.documentElement.scrollHeight !== 630) throw new Error('Canvas overflow.');
    for (const el of document.querySelectorAll('h1,h2,footer,.deck')) if (el.scrollWidth > el.clientWidth) throw new Error('Text overflow.');
  });
  const raster = await page.screenshot({type:'png'});
  if (process.argv.includes('--check')) {
    if (digest(await readFile(path.join(root, output))) !== digest(raster)) throw new Error('Share raster is stale for this renderer/font environment.');
  } else {
    await mkdir(path.dirname(path.join(root, output)), {recursive:true});
    await writeFile(path.join(root, output), raster);
  }
  console.log(JSON.stringify({source,sourceSha256:expected,output,width:1200,height:630,sha256:digest(raster),bytes:raster.length,review,fonts:['Alfa Slab One','DM Sans','JetBrains Mono'],renderer:browser.version(),processing:'complete image scaled proportionally; separate real HTML typography; no crop',check:process.argv.includes('--check')},null,2));
} finally { await browser.close(); }
