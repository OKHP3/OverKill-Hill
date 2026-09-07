#!/usr/bin/env node
// Local review QA. Missing Playwright is a failure, never a static fallback.
import { writeFile, mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE
  ? pathToFileURL(resolve(process.env.PLAYWRIGHT_MODULE)).href : 'playwright');
const base = process.env.A14_BASE || 'http://127.0.0.1:5144';
const out = resolve('.local/a14/evidence');
await mkdir(out, {recursive:true});
const browser = await chromium.launch({headless:true});
const results = [];
try {
  for (const width of [320,390,768,1280]) {
    for (const direction of ['a','b']) {
      for (const name of ['home','projects','detail','contact']) {
        const page = await browser.newPage({viewport:{width,height:width===1280?800:844}, reducedMotion:'reduce'});
        // External embeds/analytics are outside this local layout test. Fonts may load.
        await page.route('**/*', route => {
          const u = new URL(route.request().url());
          return u.origin === base || ['fonts.googleapis.com','fonts.gstatic.com'].includes(u.hostname)
            ? route.continue() : route.abort();
        });
        await page.goto(`${base}/.local/a14/${direction}/${name}.html`, {waitUntil:'domcontentloaded'});
        await page.evaluate(() => document.fonts.ready);
        const result = await page.evaluate(() => {
          const box = el => {const r=el.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,right:r.right};};
          const choices = document.querySelector('.task-choices');
          return {
            fonts: {heading:document.fonts.check('28px "Alfa Slab One"'),body:document.fonts.check('17px "DM Sans"')},
            overflow:document.documentElement.scrollWidth>innerWidth+1,
            h1:box(document.querySelector('h1')),
            selected:document.querySelector('.selected')?box(document.querySelector('.selected')):null,
            choices:choices?box(choices):null,
            primaryCounts:[...document.querySelectorAll('.selection')].map(el=>el.querySelectorAll('.primary-action').length),
            brokenImages:[...document.images].filter(im=>im.complete&&!im.naturalWidth).map(im=>im.src),
            duplicateIds:[...document.querySelectorAll('[id]')].map(el=>el.id).filter((id,i,a)=>a.indexOf(id)!==i),
            links:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))
          };
        });
        const failures=[];
        if(result.overflow) failures.push('horizontal overflow');
        if(result.h1.x<19||result.h1.right>width-19 || (width<=390 && Math.abs(result.h1.x-20)>1)) failures.push('heading gutter');
        if(result.primaryCounts.some(n=>n!==1)) failures.push('selected primary action count');
        if(result.brokenImages.length) failures.push('broken image');
        if(result.duplicateIds.length) failures.push('duplicate anchors');
        if(name==='home' && result.choices.y > 650) failures.push('choices too late');
        if(width===390||width===1280) {
          await page.screenshot({path:`${out}/${direction}-${name}-${width}.png`,fullPage:true});
          await page.screenshot({path:`${out}/${direction}-${name}-${width}-entry.png`});
        }
        results.push({direction,name,width,...result,failures});
        await page.close();
      }
    }
  }
  const tasks=[];
  for(const direction of ['a','b']) {
    const taskPage=await browser.newPage({viewport:{width:390,height:844},javaScriptEnabled:false});
    await taskPage.goto(`${base}/.local/a14/${direction}/home.html`);
    await taskPage.keyboard.press('Tab');
    await taskPage.keyboard.press('Enter');
    if(!taskPage.url().endsWith('#main')) throw new Error('Skip link failed');
    await taskPage.getByRole('link',{name:'Inspect projects',exact:true}).click();
    await taskPage.getByRole('link',{name:'Inspect project →',exact:true}).click();
    await taskPage.getByRole('link',{name:'Jump to release details ↓',exact:true}).click();
    if(!taskPage.url().endsWith('#release')) throw new Error('Release anchor failed');
    await taskPage.getByRole('link',{name:'Contact',exact:true}).click();
    if(await taskPage.getByRole('link',{name:'Email the Hill',exact:true}).getAttribute('href')!=='mailto:contact@overkillhill.com') throw new Error('Email destination mismatch');
    tasks.push({direction,result:'PASS',scope:'No-JS skip, home to shelf to detail release, Contact email href; no message sent'});
    await taskPage.close();
  }
  // Reproduce the baseline with normal scripts; record geometry separately.
  const page=await browser.newPage({viewport:{width:390,height:844}});
  await page.goto(base+'/',{waitUntil:'domcontentloaded'});
  await page.evaluate(()=>document.fonts.ready);
  const baseline=await page.evaluate(()=>Object.fromEntries(['h1','#start-here-heading','#selected-work-heading'].map(s=>{
    const r=document.querySelector(s).getBoundingClientRect();return [s,{x:r.x,y:r.y}];
  })));
  await page.screenshot({path:`${out}/baseline-home-390.png`,fullPage:true});
  await writeFile(`${out}/report.json`,JSON.stringify({browser:browser.version(),baseline,tasks,results},null,2)+'\n');
  await writeFile(resolve('assets/audit/a14-proposal-qa-2026-09-07.json'),JSON.stringify({
    browser:browser.version(),baseline,tasks,
    scope:'Local A14 proposals only. Reduced motion, dark palette, external embeds blocked in layout cases. Not integrated release acceptance.',
    results:results.map(({links,...rest})=>rest)
  },null,2)+'\n');
  const failed=results.filter(r=>r.failures.length);
  console.log(JSON.stringify({cases:results.length,failed:failed.map(({direction,name,width,failures})=>({direction,name,width,failures})),baseline},null,2));
  if(failed.length) process.exitCode=1;
} finally { await browser.close(); }
