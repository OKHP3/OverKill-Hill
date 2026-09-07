/** Bounded local-preview checks; not publication or native-language certification. */
import {chromium} from 'playwright';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const base=process.env.MURDERBIRD_PREVIEW_URL || 'http://127.0.0.1:5387';
const evidence=path.join(root,'.local/murderbird-review/homepage-qa');
const units=[{"route":"fr","alt":"Le MurderBird se tient sur deux pieds métalliques à côté d’un établi et d’un ordinateur à écran cathodique. Il possède un bec crochu, des ailes compactes repliées, une armure sombre patinée et un œil orange lumineux.","cta":"Découvrez le MurderBird : lisez son histoire (en anglais) →"},{"route":"de","alt":"Der MurderBird steht auf zwei Metallfüßen neben einer Werkbank und einem Computer mit Röhrenmonitor. Er hat einen gebogenen Schnabel, kompakte angelegte Flügel, eine dunkle patinierte Panzerung und ein orange leuchtendes Auge.","cta":"Lerne den MurderBird kennen: Lies seine Ursprungsgeschichte (auf Englisch) →"},{"route":"es","alt":"El MurderBird está de pie sobre dos patas metálicas junto a un banco de trabajo y un ordenador con monitor de tubo. Tiene un pico curvo, alas compactas plegadas, una armadura oscura con pátina y un ojo naranja luminoso.","cta":"Conoce al MurderBird: lee su historia de origen (en inglés) →"},{"route":"es-mx","alt":"El MurderBird está de pie sobre dos patas metálicas junto a un banco de trabajo y una computadora con monitor de tubo. Tiene un pico curvo, alas compactas plegadas, una armadura oscura con pátina y un ojo naranja brillante.","cta":"Conoce al MurderBird: lee la historia de su origen (en inglés) →"}];
units.push({route:'en-gb',alt:"The MurderBird stands on two metal feet beside a workbench and CRT computer, with a hooked beak, compact folded wings, dark patinated armour, and a glowing orange eye.",cta:'Meet the MurderBird: read the origin story (in English) →'});
const hash=data=>createHash('sha256').update(data).digest('hex');
const sourceAlt='The MurderBird stands on two metal feet beside a workbench and CRT computer, with a hooked beak, compact folded wings, dark patinated armor, and a glowing orange eye.';
const sourceCta='Meet the MurderBird: read the origin story →';
await mkdir(evidence,{recursive:true});
const browser=await chromium.launch({headless:true});
const results=[];
try {
 const page=await browser.newPage({reducedMotion:'reduce'});
 const errors=[];
 page.on('pageerror',error=>errors.push(error.message));
 for(const route of ['', 'fr','de','es','es-mx','en-gb']){
  for(const width of [1440,390,320]){
   await page.setViewportSize({width,height:900});
   await page.goto(base+'/'+(route?route+'/':''),{waitUntil:'networkidle'});
   await page.locator('#forge .hero-illustration').evaluate(img=>img.decode());
   for(const mode of ['dark','light']){
    for(let step=0;step<3 && await page.evaluate(()=>document.documentElement.dataset.theme)!==mode;step++) await page.getByRole('button',{name:/^Switch to .* mode$/}).click();
    await page.waitForTimeout(350);
    const result=await page.evaluate(()=>{
      const img=document.querySelector('#forge .hero-illustration'),box=img.getBoundingClientRect();
      const invitation=document.querySelector('#forge .hero-visual a[href="/writings/murderbird/"]');
      return {theme:document.documentElement.dataset.theme,viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,src:img.currentSrc,alt:img.alt,width:box.width,height:box.height,ratio:box.width/box.height,cta:invitation?.textContent,href:invitation?.getAttribute('href'),hreflang:invitation?.hreflang,headline:document.querySelector('#hero-title').textContent,actions:document.querySelectorAll('#forge .hero-actions a').length};
    });
    if(result.scrollWidth>width||result.theme!==mode||!result.src.includes('unified-master-03')||Math.abs(result.ratio-1.5)>.01||result.actions!==2||!result.cta) throw new Error(JSON.stringify(result));
    const unit=units.find(x=>x.route===route);
    if(result.alt!==(unit?.alt||sourceAlt)||result.cta!==(unit?.cta||sourceCta)||(route&&result.hreflang!=='en')) throw new Error('Locale unit mismatch: '+route);
    await page.locator('#forge').screenshot({path:path.join(evidence,`home-${route||'en'}-${width}-${mode}.png`)});
    results.push({route:route||'en',...result});
   }
  }
  await page.locator('#forge .hero-visual a').click();
  await page.waitForURL('**/writings/murderbird/');
 }
 await page.goto(base+'/writings/murderbird/',{waitUntil:'networkidle'});
 const meta=await page.evaluate(()=>({og:document.querySelector('meta[property="og:image"]').content,width:document.querySelector('meta[property="og:image:width"]').content,height:document.querySelector('meta[property="og:image:height"]').content,type:document.querySelector('meta[property="og:image:type"]').content,twitter:document.querySelector('meta[name="twitter:image"]').content,articles:[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>JSON.parse(s.textContent)).filter(x=>x['@type']==='Article').map(x=>x.image),paragraphs:document.querySelectorAll('#the-maker p,#the-mechanic p,#the-builder p,#the-water p,#the-sentinel p').length,figures:document.querySelectorAll('.murderbird-scene').length,videos:document.querySelectorAll('video').length}));
 if(meta.width!=='1200'||meta.height!=='630'||meta.type!=='image/png'||meta.og!==meta.twitter||meta.articles[0]!==meta.og||meta.figures!==5||meta.videos!==0) throw new Error(JSON.stringify(meta));
 const response=await page.request.get(base+new URL(meta.og).pathname);
 if(!response.ok()||!response.headers()['content-type'].includes('image/png')) throw new Error('Social raster not served.');
 for(const width of [1440,390,320]){
  await page.setViewportSize({width,height:900});
  for(const mode of ['dark','light']){
   for(let step=0;step<3 && await page.evaluate(()=>document.documentElement.dataset.theme)!==mode;step++) await page.getByRole('button',{name:/^Switch to .* mode$/}).click();
   await page.waitForTimeout(350);
   for(const scene of ['maker','water','mechanic','heart','sentinel']) {
   const figure=page.locator('#media-'+scene);
   await figure.scrollIntoViewIfNeeded();
   await figure.locator('img').evaluate(img=>img.decode());
   const state=await figure.evaluate(el=>{const img=el.querySelector('img'),box=img.getBoundingClientRect();return {parent:el.parentElement.id,alt:img.alt,loading:img.loading,ratio:box.width/box.height,overflow:document.documentElement.scrollWidth>innerWidth};});
   const parent=scene==='heart'?'the-builder':'the-'+scene;
   if(state.parent!==parent||state.loading!=='lazy'||state.overflow||Math.abs(state.ratio-(scene==='maker'?1.5:16/9))>.01) throw new Error(JSON.stringify(state));
   await figure.screenshot({path:path.join(evidence,`${scene}-${width}-${mode}.png`)});
   }
  }
 }
 if(errors.length) throw new Error(errors.join('\n'));
 const record={status:'model-translated, native review not performed',scope:'Local-preview homepage alt and invitation only; no story translation or publication',authority:'Bounded coordinating-task fallback instruction; full exact-pair fail-closed workflow did not pass',sourceRevision:execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),sourcePath:'site-src/pages/index.main.html',sourceHash:hash(await readFile(path.join(root,'site-src/pages/index.main.html'))),sourceLocale:'en-US',sourceRegister:'plainspoken',sourceUnits:{alt:sourceAlt,cta:sourceCta},protected:['MurderBird','/writings/murderbird/'],missingPrerequisites:['FR/DE/ES project pair records and owner-approved voice profiles','ES-MX profile remains provisional'],translations:await Promise.all(units.map(async unit=>({...unit,targetLocale:({'fr':'fr-FR','de':'de-DE','es':'es-ES','es-mx':'es-MX','en-gb':'en-GB'})[unit.route],targetPath:unit.route+'/index.html',targetHash:hash(await readFile(path.join(root,unit.route,'index.html'))),sourceDirection:'Directly from en-US; no target-to-target chaining',textVersion:1,review:'model-translated, native review not performed'}))),checks:{homeLayouts:results.length,sceneLayouts:30,consoleErrors:errors,metadata:meta},screenshots:'.local/murderbird-review/homepage-qa/'};
 await writeFile(path.join(root,'i18n/pilot/murderbird-homepage-preview-2026-09-06.json'),JSON.stringify(record,null,2)+'\n');
 await writeFile(path.join(evidence,'results.json'),JSON.stringify({results,record},null,2)+'\n');
 console.log(JSON.stringify(record.checks,null,2));
}finally{await browser.close();}
