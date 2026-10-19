const {chromium}=require('C:/Users/Hyunjun/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),assert=require('assert');const run='C:/Users/Hyunjun/AppData/Local/Temp/ml-map-derivation-9b5e365a43b94cd6a982c674397155ac';
(async()=>{const browser=await chromium.launch({headless:true,channel:'chrome'});const report={cases:[],errors:[],external:[]};
for(const [width,height] of [[1440,900],[375,812]]){
 const context=await browser.newContext({viewport:{width,height},reducedMotion:'reduce'});const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text())});page.on('request',r=>{if(!r.url().startsWith('http://127.0.0.1:8765/')&&!r.url().startsWith('data:'))report.external.push(r.url())});
 await page.goto('http://127.0.0.1:8765/preview.html');await page.waitForSelector('.nb-row');await page.evaluate(()=>document.fonts.ready);
 for(const theme of ['light','dark']){
  const toggle=page.getByRole('button',{name:theme==='dark'?'다크 모드로 전환':'라이트 모드로 전환',exact:true});if(await toggle.count())await toggle.click();
  for(const [mode,total] of [['사전',6],['평균',6],['예측',5]]){
   await page.getByRole('button',{name:mode,exact:true}).click();
   for(let i=1;i<total;i++){await page.getByRole('button',{name:'다음 줄 쓰기',exact:true}).click();assert.equal(await page.locator('.nb-row').count(),i+1);}
   assert(await page.getByRole('button',{name:'다음 줄 쓰기',exact:true}).isDisabled());assert.equal(await page.locator('.katex-error').count(),0);
   const layout=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,board:(()=>{const b=document.querySelector('.notebook').getBoundingClientRect();return {x:b.x,y:b.y,right:b.right,bottom:b.bottom}})(),katex:document.querySelectorAll('.notebook .katex').length}));assert(!layout.overflow);assert(layout.board.right<=width&&layout.board.bottom<=height);
   report.cases.push({width,height,theme,mode,total,...layout});
   if(mode==='평균'||mode==='사전')await page.screenshot({path:run+'/topic/evidence/'+width+'-'+theme+'-'+(mode==='평균'?'mean':'prior')+'.png'});
   await page.getByRole('button',{name:'이전 줄',exact:true}).click();assert.equal(await page.locator('.nb-row').count(),total-1);await page.locator('[data-action="next"]').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('.nb-row').count(),total);
  }
 }
 if(width<1024){await page.getByRole('button',{name:'조작 패널',exact:true}).click();assert.equal(await page.getByRole('button',{name:'조작 패널',exact:true}).getAttribute('aria-expanded'),'true');await page.keyboard.press('Escape');assert.equal(await page.getByRole('button',{name:'조작 패널',exact:true}).getAttribute('aria-expanded'),'false');await page.getByRole('button',{name:'조작 패널',exact:true}).click();}
 await page.locator('#prior-mean').fill('4');await page.locator('#prior-var').fill('4');await page.waitForFunction(()=>document.querySelector('.nb-live').textContent.includes('예측평균 8'));
 assert((await page.locator('.tile b').allTextContents()).every(s=>s==='4'));
 await page.locator('#prior-mean').fill('-4');await page.locator('#prior-var').fill('0.25');assert((await page.locator('.tile b').allTextContents()).every(s=>s==='-2.4'));
 for(const [id,value,expected] of [['prior-mean','', '-4'],['prior-mean','9','-4'],['prior-mean','0.1','-4'],['prior-var','0','0.25'],['prior-var','','0.25'],['prior-var','4.1','0.25']]){await page.locator('#'+id).fill(value);assert.equal(await page.locator('#'+id).inputValue(),expected);}
 await page.getByRole('button',{name:'식과 입력 처음부터',exact:true}).click();assert.equal(await page.locator('#prior-mean').inputValue(),'0');assert.equal(await page.locator('#prior-var').inputValue(),'1');assert.equal(await page.locator('.nb-row').count(),1);
 if(width<1024)await page.keyboard.press('Escape');await page.keyboard.press('Tab');assert(await page.evaluate(()=>document.activeElement!==document.body));
 await context.close();
}
assert.deepEqual(report.errors,[]);assert.deepEqual(report.external,[]);fs.writeFileSync(run+'/topic/evidence/browser-qa.json',JSON.stringify(report,null,2));console.log(JSON.stringify({cases:report.cases.length,errors:report.errors,external:report.external,inputBounds:'passed',keyboard:'passed',drawerEscape:'passed',reset:'passed'}));await browser.close();})().catch(e=>{console.error(e);process.exit(1)});
