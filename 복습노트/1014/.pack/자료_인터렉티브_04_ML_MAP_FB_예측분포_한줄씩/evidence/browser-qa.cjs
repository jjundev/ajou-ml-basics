const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),vm=require('vm');
const {chromium}=require('C:/Users/Hyunjun/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const run=fs.readFileSync(path.join(process.env.TEMP,'ml-full-flow-current.txt'),'utf8').trim();
(async()=>{const browser=await chromium.launch({headless:true,channel:'chrome'}),results=[];const target=process.argv[2]||path.join(run,'preview.html');
for(const width of [1440,375])for(const theme of ['light','dark']){
 const page=await browser.newPage({viewport:{width,height:width===375?812:900},colorScheme:theme,reducedMotion:'reduce'}),errors=[],external=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url())});
 await page.goto(pathToFileURL(target).href);await page.locator('.formula-row').first().waitFor();await page.evaluate(()=>document.fonts.ready);
 if(!await page.locator('[data-prev]').isDisabled())throw Error('first prev');
 const phases=[['ML',1],['MAP',9],['FB',19],['예측分布',28]];
 for(let i=0;i<36;i++){
   if(i)await page.locator('[data-next]').click();
   await page.waitForTimeout(20);
   const check=await page.evaluate(()=>{const head=document.querySelector('.stage-head').getBoundingClientRect(),tools=document.querySelector('.view-btns').getBoundingClientRect();return {rows:document.querySelectorAll('.formula-row').length,active:document.querySelectorAll('.formula-row.is-active').length,reasons:document.querySelectorAll('.formula-row .sub').length,errors:document.querySelectorAll('.katex-error').length,overflow:document.documentElement.scrollWidth>innerWidth,header:tools.top>=head.top&&tools.bottom<=head.bottom,scroll:getComputedStyle(document.querySelector('.formula-scroll')).scrollbarWidth,firstBorder:getComputedStyle(document.querySelector('.panel-left .panel-content .sec')).borderTopWidth};});
   if(check.rows!==i+1||check.active!==1||check.reasons!==1||check.errors||check.overflow||!check.header||check.scroll!=='thin'||check.firstBorder!=='0px')throw Error(JSON.stringify({width,theme,i,...check}));
   if([7,17,26,35].includes(i)){await page.screenshot({path:path.join(run,`topic/evidence/${width}-${theme}-step${i+1}.png`)});results.push({width,theme,step:i+1,...check});}
 }
 if(!await page.locator('[data-next]').isDisabled())throw Error('last next');
 await page.locator('.formula-scroll').focus();await page.keyboard.press('ArrowLeft');if(await page.locator('.formula-row').count()!==35)throw Error('left key');await page.keyboard.press('ArrowRight');
 const base=await page.locator('.formula-math').first().evaluate(e=>parseFloat(getComputedStyle(e).fontSize));await page.getByRole('button',{name:'확대',exact:true}).click();const big=await page.locator('.formula-math').first().evaluate(e=>parseFloat(getComputedStyle(e).fontSize));if(big<=base)throw Error('zoom');await page.getByRole('button',{name:'수식 크기 초기화',exact:true}).click();if(await page.locator('.formula-row').count()!==36)throw Error('size reset altered steps');
 if(width===375)await page.getByRole('button',{name:'조작 패널',exact:true}).click();
 for(const label of ['① ML','② MAP','③ FB','④ 예측분포']){await page.getByRole('button',{name:label,exact:true}).click();}
 const inputs=page.locator('.panel-left input[type=number]');
 for(const [i,min,max,off] of [[0,'-4','4','0.3'],[1,'0.25','4','0.3']]){
  await inputs.nth(i).fill(min);if(await inputs.nth(i).inputValue()!==min)throw Error('min');await inputs.nth(i).fill(max);if(await inputs.nth(i).inputValue()!==max)throw Error('max');
  for(const invalid of ['', '99',off]){await inputs.nth(i).fill(invalid);if(await inputs.nth(i).inputValue()!==max)throw Error('invalid '+invalid);}
 }
 await inputs.nth(0).fill('2');await inputs.nth(1).fill('1');await page.getByRole('button',{name:'처음부터',exact:true}).click();if(await inputs.nth(0).inputValue()!=='0'||await inputs.nth(1).inputValue()!=='1'||await page.locator('.formula-row').count()!==1)throw Error('restart');
 if(width===375){await page.keyboard.press('Escape');await page.getByRole('button',{name:'설명 패널',exact:true}).click();await page.locator('.panel-right details').first().locator('summary').click();await page.keyboard.press('Escape');}
 if(errors.length||external.length)throw Error(JSON.stringify({errors,external}));await page.close();
}
await browser.close();fs.writeFileSync(path.join(run,'topic/evidence/browser-qa.json'),JSON.stringify(results,null,2));console.log('144 line/theme/viewport checks + zoom, keyboard, jumps, inputs, reset, drawer passed');})().catch(e=>{console.error(e);process.exit(1)});
