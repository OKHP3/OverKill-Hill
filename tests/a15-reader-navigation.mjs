// Run after English HTML generation with a local preview already listening.
import { mkdirSync } from 'node:fs';
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = process.env.A15_BASE_URL || 'http://127.0.0.1:5155/';
const output = process.env.A15_OUTPUT || '.local/a15';
mkdirSync(output, { recursive: true });
import assert from 'node:assert/strict';
const browser = await chromium.launch({headless:true});
console.log('Chromium', browser.version());
try {
for (const width of [390,1280]) for (const variant of ['expanded','compact']) {
 const page=await browser.newPage({viewport:{width,height:844},reducedMotion:'reduce'});
 await page.route('**/*', r=>r.request().url().startsWith(base)?r.continue():r.abort());
 for (const route of ['contact/','writings/first-diagram-is-a-liar/']) {
  await page.goto(base+route);
  const contact=route==='contact/';
  if(variant==='compact') await page.evaluate(contact=>{
   const h=document.getElementById(contact?'inquiry-prompts':'reader-route'); const box=h.parentElement;
   const details=document.createElement('details'); details.className=box.className;
   const summary=document.createElement('summary'); summary.id=h.id; summary.textContent=h.textContent;
   details.append(summary); for(const n of [...box.childNodes]) if(n!==h) details.append(n);
   box.replaceWith(details);
  },contact);
  const id=contact?'inquiry-prompts':'reader-route';
  await page.locator('#'+id).scrollIntoViewIfNeeded();
  await page.screenshot({path:`${output}/${variant}-${contact?'contact':'article'}-${width}.png`});
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  if(variant==='compact') {await page.locator('#'+id).focus();await page.keyboard.press('Enter');assert(await page.locator('details:has(#'+id+')').getAttribute('open')!==null);}
  if(contact){assert.equal(await page.locator('main a[href="mailto:contact@overkillhill.com"]').count(),1);continue;}
  for(const hash of ['#roy','#council-scoring','#artifacts','#version-history']) assert.equal(await page.locator('.article-jump-nav a[href="'+hash+'"]').count(),1);
  const link=page.locator(variant==='expanded'?'aside:has(#reader-route) a':'details:has(#reader-route) a').first();
  await link.focus();await page.keyboard.press('Enter');
  assert.equal(await page.evaluate(()=>location.hash),'#prompts');
  assert.equal(await page.evaluate(()=>document.activeElement.id),'prompts');
  await page.keyboard.press('Tab');assert(await page.evaluate(()=>{const target=document.getElementById('prompts');return document.activeElement.closest('main') && Boolean(target.compareDocumentPosition(document.activeElement)&Node.DOCUMENT_POSITION_FOLLOWING);}));
  await page.goBack();assert.equal(await page.evaluate(()=>location.hash),'');
  await page.goForward();assert.equal(await page.evaluate(()=>location.hash),'#prompts');
 }
 await page.close();console.log('PASS',variant,width,'anchors, focus, Tab, Back/Forward, email, overflow');
}
} finally {await browser.close();}
