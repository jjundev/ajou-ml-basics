const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Hyunjun/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const run=__dirname,evidence=path.join(run,'evidence');fs.mkdirSync(evidence,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'}),results=[];
 for(const width of [1440,375])for(const theme of ['light','dark']){
  const page=await browser.newPage({viewport:{width,height:width===375?812:900},colorScheme:theme});const errors=[],external=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url())});
  await page.goto(pathToFileURL(process.argv[2]||path.join(run,'preview.html')).href);await page.locator('.canvas').waitFor();await page.evaluate(()=>document.fonts.ready);
  if(await page.getByRole('button',{name:theme==='dark'?'다크 모드로':'라이트 모드로',exact:true}).count()){} // system theme comes from colorScheme
  for(const name of ['원래','이동']){
   await page.getByRole('button',{name,exact:true}).click();
   if(width<1024)await page.getByRole('button',{name:'조작 패널',exact:true}).click();
   const input=page.locator('#theta-number');
   for(const v of ['-0.5','2.5','1']){await input.fill(v);assert.equal(await input.inputValue(),v);}
   await input.fill('');assert.equal(await input.inputValue(),'1');
   await input.fill('9');assert.equal(await input.inputValue(),'1');
   await page.getByRole('button',{name:'최적 계수 θ̂ = 1',exact:true}).click();
   await page.getByRole('button',{name:'삼각형 정면',exact:true}).click();
   await input.fill('1.9');
   await page.getByRole('button',{name:'원점 벡터',exact:true}).click();await page.getByRole('button',{name:'원점 벡터',exact:true}).click();
   if(width<1024){await page.keyboard.press('Escape');assert.equal(await page.getByRole('button',{name:'조작 패널',exact:true}).getAttribute('aria-expanded'),'false');}
   await page.getByRole('button',{name:'확대',exact:true}).click();await page.getByRole('button',{name:'시점 처음으로',exact:true}).click();
   await page.waitForTimeout(150);await page.screenshot({path:path.join(evidence,`${width}-${theme}-${name==='원래'?'original':'shift'}.png`)});
   if(width<1024){await page.getByRole('button',{name:'설명 패널',exact:true}).click();await page.locator('.katex').first().waitFor();assert.equal(await page.locator('.katex-error').count(),0);await page.keyboard.press('Escape');}
  }
  await page.getByRole('button',{name:'수식',exact:true}).click();const next=page.getByRole('button',{name:'다음 줄 쓰기',exact:true}),prev=page.getByRole('button',{name:'이전 줄',exact:true});
  assert.equal(await prev.isDisabled(),true);for(let i=0;i<4;i++)await next.click();assert.equal(await next.isDisabled(),true);assert.equal(await page.locator('.formula-row').count(),5);
  await page.locator('.formula-scroll').focus();await page.keyboard.press('ArrowLeft');assert.equal(await page.locator('.formula-row').count(),4);await page.keyboard.press('ArrowRight');
  await page.getByRole('button',{name:'확대',exact:true}).click();await page.getByRole('button',{name:'수식 크기 초기화',exact:true}).click();
  const layout=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,katexErrors:document.querySelectorAll('.katex-error').length,firstLeft:getComputedStyle(document.querySelector('.panel-left .sec')).borderTopWidth,firstRight:getComputedStyle(document.querySelector('.panel-right .panel-content > details')).borderTopWidth}));
  assert.equal(layout.overflow,false);assert.equal(layout.katexErrors,0);assert.equal(layout.firstLeft,'0px');assert.equal(layout.firstRight,'0px');
  await page.screenshot({path:path.join(evidence,`${width}-${theme}-formula.png`)});
  if(width<1024)await page.getByRole('button',{name:'조작 패널',exact:true}).click();await page.getByRole('button',{name:'입력과 모드 처음으로',exact:true}).click();assert.equal(await inputValue(page),'1.9');
  assert.deepEqual(errors,[]);assert.deepEqual(external,[]);results.push({width,theme,...layout,modes:3,inputs:true,steps:true,reset:true,keyboard:true,external,errors});await page.close();
 }
 await browser.close();fs.writeFileSync(path.join(evidence,process.argv[2]?'final-browser.json':'browser.json'),JSON.stringify(results,null,2));console.log(JSON.stringify({passed:true,cases:results.length,evidence}));
})().catch(e=>{console.error(e);process.exit(1)});
async function inputValue(page){return page.locator('#theta-number').inputValue();}
