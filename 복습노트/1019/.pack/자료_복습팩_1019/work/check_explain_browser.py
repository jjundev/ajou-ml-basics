from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import quote,urlparse,unquote
import json
r=Path('/tmp/ml-review-pack-20261019/1019');ep=r/'repo/tmp/ml-problem-explain/1019-20261019/review-1019-Prediction_and_Projection';cfg=json.loads((ep/'stage.json').read_text());stage=ep/cfg['stage'];out=r/'work/explain-browser';out.mkdir(exist_ok=True)
# Mount stage under running HTTP server; no unpublished artifacts go into public folder.
mount=r/'work/stage/explain'
if mount.is_symlink():mount.unlink()
mount.symlink_to(stage,target_is_directory=True)
url='http://localhost:49191/explain/'+quote(cfg['html']);errors=[];external=[];results=[];interactions=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='chrome',headless=True)
 for w,h in [(1280,900),(1024,900),(375,812)]:
  for theme in ['light','dark']:
   print('configuration',w,theme,flush=True);ctx=b.new_context(viewport={'width':w,'height':h},color_scheme=theme);p=ctx.new_page();p.set_default_timeout(6000)
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('requestfailed',lambda q:errors.append(q.url+':'+str(q.failure)))
   p.on('request',lambda q:external.append(q.url) if urlparse(q.url).hostname not in ('localhost','127.0.0.1',None) else None)
   p.on('response',lambda a:errors.append(str(a.status)+':'+a.url) if a.status>=400 else None)
   p.goto(url,wait_until='networkidle');p.wait_for_timeout(200);p.evaluate("location.hash='#p1'");p.wait_for_timeout(180)
   defaults=p.locator('.layout').evaluate('e=>({left:e.dataset.left,prob:e.dataset.prob,right:e.dataset.right})')
   if w>=1024:assert defaults['left']=='open' and defaults['prob']=='open',defaults
   stats=[]
   for i in range(1,9):
    sid=f'p{i}';p.evaluate('(id)=>location.hash="#"+id',sid);p.wait_for_timeout(90);p.evaluate('document.getAnimations().forEach(a=>a.finish())')
    st=p.evaluate('''(id)=>{const a=document.getElementById(id),c=document.querySelector('.content');return {id,katexErrors:document.querySelectorAll('.katex-error').length,katex:a.querySelectorAll('.katex').length,overflow:c.scrollWidth>c.clientWidth+1||document.documentElement.scrollWidth>innerWidth+1,sections:a.querySelectorAll('[data-explanation]').length,sum:document.querySelectorAll('#panel-right .sum').length,panels:document.querySelectorAll('.problem-pane').length,rawDollar:[...a.querySelectorAll('*')].filter(e=>!['SCRIPT','STYLE'].includes(e.tagName)&&!e.closest('[hidden]')).some(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.includes('$'))),inlineScroll:[...a.querySelectorAll('.katex:not(.katex-display .katex)')].filter(e=>e.parentElement.classList.contains('math-pan')).length};}''',sid)
    if (w==1280 and theme=='light') or (w==375 and theme=='dark'):
     p.screenshot(path=str(out/f'{w}-{theme}-{sid}-top.png'))
     for layer in ['recall','solve','verify','retry']:
      p.locator(f'#{sid} [data-explanation={layer}]').scroll_into_view_if_needed();p.screenshot(path=str(out/f'{w}-{theme}-{sid}-{layer}.png'))
    assert st['katexErrors']==0 and not st['overflow'] and not st['rawDollar'] and st['sections']==7,st
    stats.append(st)
   p.evaluate("location.hash='#p1'");p.wait_for_timeout(100)
   # TOC and previous/next actual clicks.
   p.locator('#toggle-left').click()
   if w<1024:p.locator('#panel-left [data-panel-close]').click()
   else:p.locator('#toggle-left').click()
   if w>=1024:
    p.locator('#tab-original').click();assert p.locator('#tab-original').get_attribute('aria-selected')=='true';p.locator('#tab-problem').click()
    for dock in ['right','float','left']:
     p.locator(f'[data-dock={dock}]').click();assert p.locator('.layout').get_attribute('data-prob-dock')==dock
     if dock=='float':
      move=p.locator('.float-move');move.focus();move.press('ArrowRight');resize=p.locator('.float-resize');resize.focus();resize.press('ArrowRight');bb=p.locator('#panel-prob').bounding_box();assert bb['x']>=0 and bb['x']+bb['width']<=w+1
    sep=p.locator('#panel-prob .panel-resize');sep.focus();sep.press('ArrowRight');sep.press('Home')
    p.locator('#toggle-prob').click();p.reload(wait_until='networkidle');assert p.locator('.layout').get_attribute('data-prob')=='closed';p.locator('#toggle-prob').click()
   else:
    btn=p.locator('#p1 .problem-toggle');assert btn.get_attribute('aria-expanded')=='false';btn.click();assert btn.get_attribute('aria-expanded')=='true';btn.click()
   before=p.locator('body').evaluate('e=>getComputedStyle(e).backgroundColor');p.locator('#theme-toggle').click();after=p.locator('body').evaluate('e=>getComputedStyle(e).backgroundColor');assert before!=after
   results.append({'width':w,'theme':theme,'defaults':defaults,'items':stats,'panel_controls':'pass'})
   ctx.close()
 # Boundary: initial opening vs saved closed survive 1023->1024
 ctx=b.new_context(viewport={'width':1023,'height':900});p=ctx.new_page();p.goto(url,wait_until='networkidle');p.set_viewport_size({'width':1024,'height':900});p.wait_for_timeout(150);assert p.locator('.layout').get_attribute('data-prob')=='open';p.locator('#toggle-prob').click();p.set_viewport_size({'width':1023,'height':900});p.set_viewport_size({'width':1024,'height':900});assert p.locator('.layout').get_attribute('data-prob')=='closed';ctx.close();b.close()
report={'results':results,'errors':errors,'external_requests':external,'boundary':'pass'};(r/'work/explain-browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({'configurations':len(results),'screens':48,'errors':errors,'external_requests':external,'boundary':'pass'}));assert not errors and not external
