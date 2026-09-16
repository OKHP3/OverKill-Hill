/** Compose the v2 CRT artwork with real, unbroken brand typography. */
import {chromium} from 'playwright';
import {readFile, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const art=await readFile(path.join(root,'assets/murderbird/production/images/murderbird-v2-crt-sharing-background-wide-1536-2026-09-08.png'));
const browser=await chromium.launch({headless:true});
try {
  const page=await browser.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});
  await page.setContent(`<!doctype html><html lang="en-US"><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=DM+Sans:wght@500&display=swap"><style>
  *{box-sizing:border-box}html,body{margin:0;width:1200px;height:630px;overflow:hidden;background:#141715;color:#fff4e4}
  img{position:absolute;width:1200px;height:630px;object-fit:cover;object-position:center}
  .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,16,14,.78),transparent 68%)}
  main{position:absolute;left:48px;top:215px;width:535px}h1{font:37px/1.3 'Alfa Slab One';white-space:nowrap;margin:0 0 20px;color:#fff4e4}
  p{font:21px/1.6 'DM Sans';margin:0}.url{font-size:17px;margin-top:28px;color:#e4b477}
  </style><img alt="" src="data:image/png;base64,${art.toString('base64')}"><div class="shade"></div><main><h1>OverKill&nbsp;Hill&nbsp;P³™</h1><p>Precision · Protocol · Promptcraft</p><p class="url">overkillhill.com</p></main></html>`,{waitUntil:'networkidle'});
  await page.evaluate(async()=>{await document.fonts.ready;await document.images[0].decode();for(const family of ['Alfa Slab One','DM Sans'])if(![...document.fonts].some(f=>f.family.replaceAll('"','')===family&&f.status==='loaded'))throw Error('Missing font: '+family);const h=document.querySelector('h1');if(h.scrollWidth>h.clientWidth)throw Error('Brand name overflow');});
  await page.screenshot({path:path.join(root,'assets/img/og/murderbird-v2-brand-share-1200x630.png')});
} finally {await browser.close();}
