from pathlib import Path
from playwright.sync_api import sync_playwright
import json
from urllib.parse import quote
r=Path('/tmp/ml-review-pack-20261019/1019'); out=r/'work/browser';out.mkdir(exist_ok=True)
errors=[];results=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='chrome',headless=True)
 for typ in ['정리노트','복습문제']:
  for width,height,theme in [(1280,900,'light'),(375,812,'dark')]:
   ctx=b.new_context(viewport={'width':width,'height':height},color_scheme=theme);page=ctx.new_page()
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('requestfailed',lambda req:errors.append(req.url+':'+str(req.failure)))
   page.on('response',lambda res:errors.append(str(res.status)+':'+res.url) if res.status>=400 else None)
   url='http://localhost:49191/'+quote('복습노트/1019/'+typ+'_1019_Prediction_and_Projection.html')
   page.goto(url,wait_until='networkidle');page.wait_for_timeout(500)
   stats=page.evaluate('''async()=>{
    const wait=ms=>new Promise(r=>setTimeout(r,ms));const scroller=document.querySelector('.content')||document.documentElement;let over=[];
    document.querySelectorAll('details').forEach(d=>d.open=true);
    for(const s of document.querySelectorAll('main .screen')){location.hash='#'+s.id;await wait(80);document.getAnimations().forEach(a=>a.finish());if(scroller.scrollWidth>scroller.clientWidth+1||document.documentElement.scrollWidth>innerWidth+1)over.push(s.id);}
    const nodes=[...document.querySelectorAll('main *,#panel-right *')].filter(e=>!['SCRIPT','STYLE'].includes(e.tagName)&&!e.closest('[hidden]'));
    return {katex:document.querySelectorAll('.katex').length,katexErrors:document.querySelectorAll('.katex-error').length,rawDollar:nodes.some(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.includes('$'))),over,sums:document.querySelectorAll('#panel-right .sum').length,left:document.querySelectorAll('main .sum').length,cards:document.querySelectorAll('article.card').length,aids:document.querySelectorAll('#panel-right .aid').length,screens:[...document.querySelectorAll('main .screen')].map(s=>s.id)};
   }''')
   # Capture actual every-topic rendering; representative screenshots below are also visually inspected.
   for sid in stats['screens']:
    page.evaluate('(sid)=>location.hash="#"+sid',sid);page.wait_for_timeout(120);page.evaluate('document.getAnimations().forEach(a=>a.finish())')
    page.screenshot(path=str(out/f'{typ}-{width}-{sid}.png'))
   if typ=='정리노트':
    widgets=page.locator('.widget').count();stats['widgets']=widgets
    if widgets:
     page.evaluate("location.hash='#s2-line'");page.wait_for_timeout(150)
     slider=page.locator('.widget input[type=range]').first
     slider.fill('4');slider.dispatch_event('input');stats['widget4']=page.locator('.widget .readout').inner_text()
     slider.fill('2');slider.dispatch_event('input');stats['widget2']=page.locator('.widget .readout').inner_text()
    toggle=page.locator('#theme-toggle');before=page.locator('body').evaluate('e=>getComputedStyle(e).backgroundColor');toggle.click();after=page.locator('body').evaluate('e=>getComputedStyle(e).backgroundColor');stats['toggleChanges']=before!=after
   results.append(dict(type=typ,width=width,theme=theme,**stats));ctx.close()
 b.close()
(r/'work/browser-report.json').write_text(json.dumps({'results':results,'errors':errors},ensure_ascii=False,indent=2));print(json.dumps({'results':results,'errors':errors},ensure_ascii=False,indent=2))
assert not errors
for s in results:assert s['katex']>0 and not s['katexErrors'] and not s['rawDollar'] and not s['over']
