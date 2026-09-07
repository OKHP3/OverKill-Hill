async (page) => {
  const ids=['01-maker','02-water','03-recovery','04-mechanic','05-heart','06-choice','07-sentinel','08-hero'];
  // Serve the repository root; HTML is excluded local review output, not public assets.
  const base='http://127.0.0.1:5379/.local/murderbird-review';
  const root='C:/Users/jamie/OKH-Local/04_GitHub_Mirrors/overkill-hill/assets/murderbird/v2/';
  const evidence=[];
  await page.setViewportSize({width:1200,height:630});
  for(const id of ids){
    await page.goto(`${base}/social/${id}.html`);
    await page.locator('img').evaluate(img=>img.decode());
    const layout=await page.evaluate(()=>({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,imageLoaded:document.images[0].naturalWidth>0,fit:getComputedStyle(document.images[0]).objectFit,footerOverflow:document.querySelector('footer').scrollWidth>document.querySelector('footer').clientWidth}));
    if(layout.width!==1200||layout.height!==630||!layout.imageLoaded||layout.fit!=='contain'||layout.footerOverflow)throw new Error(JSON.stringify({id,layout}));
    await page.screenshot({path:root+`social/${id}.png`});
    evidence.push({id,...layout});
  }
  await page.setViewportSize({width:1440,height:1000});
  await page.goto(`${base}/index.html`);
  await page.locator('img').evaluateAll(images=>Promise.all(images.map(img=>{img.loading='eager';return img.decode();})));
  await page.screenshot({path:'output/playwright/murderbird-library-desktop.png',fullPage:true});
  await page.setViewportSize({width:390,height:844});
  await page.screenshot({path:'output/playwright/murderbird-library-mobile.png',fullPage:true});
  const mobile=await page.evaluate(()=>({viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0,alt:!!i.alt,uncropped:getComputedStyle(i).height==='auto'||Math.abs(i.getBoundingClientRect().width/i.getBoundingClientRect().height-i.naturalWidth/i.naturalHeight)<.01}))}));
  if(mobile.scrollWidth>mobile.viewport||mobile.images.some(i=>!i.loaded||!i.alt||!i.uncropped))throw new Error(JSON.stringify(mobile));
  return {social:evidence,mobile};
}
