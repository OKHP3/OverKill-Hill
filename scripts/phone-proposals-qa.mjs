import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const fs=require('fs');
(async()=>{
const browser=await chromium.launch({headless:true});
const results=[];
for(const width of [390,1280,320]) for(const variant of ['baseline','a','b']) {
 const routes=variant==='baseline'?['']:['','projects/','projects/skillz/','contact/'];
 for(const route of routes){
 const page=await browser.newPage({viewport:{width,height:width===1280?800:844},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const url='http://127.0.0.1:5144/'+(variant==='baseline'?'':'.local/a14/'+variant+'/')+route;
 await page.goto(url,{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);
 await page.screenshot({path:'.local/a14/'+variant+'-'+(route.replaceAll('/','-').replace(/-$/,'')||'home')+'-'+width+'.png',fullPage:false});
 const metrics=await page.evaluate(()=>{
 const box=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height};};
 return {overflow:document.documentElement.scrollWidth>innerWidth,h1:box('h1'),choices:box('.proposal-choices'),start:box('#start-here-heading'),selected:box('#selected-work-heading'),images:[...document.querySelectorAll('.hero img')].map(i=>({complete:i.complete,width:i.naturalWidth,src:i.currentSrc})),proposal:document.body.dataset.proposal||null};});
 if(variant!=='baseline' && route===''){
  await page.locator('#selected-work-heading').scrollIntoViewIfNeeded();
  await page.screenshot({path:'.local/a14/'+variant+'-selected-'+width+'.png'});
 }
 results.push({variant,route,width,errors,...metrics});await page.close();
 }
}
fs.writeFileSync('.local/a14/geometry.json',JSON.stringify(results,null,2));
console.log(JSON.stringify(results.filter(x=>!x.route)));await browser.close();
if(results.some(x=>x.overflow||x.errors.length))process.exitCode=1;
})();
