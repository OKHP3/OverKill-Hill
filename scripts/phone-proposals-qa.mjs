import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const fs=require('fs');
const assert=require('node:assert/strict');
const summaries=JSON.parse(fs.readFileSync('.local/a14/contract-summaries.json','utf8'));
const registry=JSON.parse(fs.readFileSync('.local/a14/contract-source/site-src/project-status.json','utf8'));
(async()=>{
const browser=await chromium.launch({headless:true});
const results=[];
for(const width of [390,1280,320]) for(const variant of ['baseline','a','b']) {
 const routes=variant==='baseline'?['']:['','projects/','projects/skillz/','contact/'];
 for(const route of routes){
 const page=await browser.newPage({viewport:{width,height:width===1280?800:844},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const url='http://127.0.0.1:5145/'+(variant==='baseline'?'':'proposals/'+variant+'/')+route;
 await page.goto(url,{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);
 await page.screenshot({path:'.local/a14/'+variant+'-'+(route.replaceAll('/','-').replace(/-$/,'')||'home')+'-'+width+'.png',fullPage:false});
 const metrics=await page.evaluate(()=>{
 const box=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height};};
 return {overflow:document.documentElement.scrollWidth>innerWidth,h1:box('h1'),choices:box('.proposal-choices'),start:box('#start-here-heading'),selected:box('#selected-work-heading'),images:[...document.querySelectorAll('.hero img')].map(i=>({complete:i.complete,width:i.naturalWidth,src:i.currentSrc})),proposal:document.body.dataset.proposal||null};});
 if(variant!=='baseline'){
  const contract=await page.evaluate(()=>({
   statuses:[...document.querySelectorAll('[data-project-status]')].map(p=>({id:p.dataset.projectStatus,text:p.querySelector('[data-project-status-text]').textContent,url:p.querySelector('a').href})),
   primaryCounts:[...document.querySelectorAll('.project-card')].map(c=>c.querySelectorAll('.btn-primary').length)
  }));
  for(const status of contract.statuses)assert.deepEqual({text:status.text,url:status.url},summaries[status.id]);
  for(const count of contract.primaryCounts)assert.equal(count,1);
  if(route==='projects/')assert.equal(contract.statuses.length,registry.projects.filter(r=>r.shelf).length);
  if(route==='projects/skillz/')assert.equal(contract.statuses.length,1);
  metrics.contract=contract;
 }
 if(variant!=='baseline' && route===''){
  await page.locator('#selected-work-heading').evaluate(e=>window.scrollTo(0,e.getBoundingClientRect().top+scrollY-180));
  await page.screenshot({path:'.local/a14/'+variant+'-selected-'+width+'.png'});
 }
 results.push({variant,route,width,errors,...metrics});await page.close();
 }
}
const supplemental=[];
for(const variant of ['a','b'])for(const route of ['','projects/','projects/skillz/','contact/'])for(const javaScriptEnabled of [true,false]){
 const page=await browser.newPage({viewport:{width:390,height:844},colorScheme:'dark',javaScriptEnabled,reducedMotion:'reduce'});
 await page.goto('http://127.0.0.1:5145/proposals/'+variant+'/'+route,{waitUntil:'networkidle'});
 const state=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,hidden:[...document.querySelectorAll('main .reveal-on-scroll')].some(e=>getComputedStyle(e).opacity==='0'),theme:document.documentElement.dataset.theme}));
 assert.equal(state.overflow,false);assert.equal(state.hidden,false);
 if(javaScriptEnabled)assert.equal(state.theme,'dark');
 supplemental.push({variant,route,javaScriptEnabled,...state});await page.close();
}
fs.writeFileSync('.local/a14/geometry.json',JSON.stringify(results,null,2));
fs.writeFileSync('.local/a14/supplemental.json',JSON.stringify(supplemental,null,2));
console.log(JSON.stringify(results.filter(x=>!x.route)));await browser.close();
if(results.some(x=>x.overflow||x.errors.length))process.exitCode=1;
})();
