from pathlib import Path
import json,threading,functools,urllib.parse,hashlib
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright
folder=Path(__file__).parent.parent
meta=json.loads((folder/'stage.json').read_text(encoding='utf-8'))
stage=folder/meta['stage'];evidence=folder/'evidence'
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(stage)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'+urllib.parse.quote(meta['html'])
rows=[];failures=[]
inspect=r'''(root)=>{
 const problems=[]; const get=n=>getComputedStyle(n); const gap=n=>parseFloat(get(n).marginTop);
 const math=[...root.querySelectorAll('.katex')].filter(n=>n.getClientRects().length);
 const smallScroll=math.filter(n=>!n.closest('.math-row')&&get(n).overflowX!=='visible');
 if(smallScroll.length)problems.push('inline-scroll:'+smallScroll.length);
 const badRows=[...root.querySelectorAll('.math-row')].filter(n=>n.getClientRects().length).filter(n=>{
   if(n.scrollWidth>n.clientWidth+3&&!n.classList.contains('math-pan'))return true;
   if(n.classList.contains('math-pan')&&get(n).scrollbarWidth!=='none')return true;
   return n.scrollHeight>n.clientHeight+3;
 });
 if(badRows.length)problems.push('math-clipping-or-scrollbar:'+badRows.length);
 root.querySelectorAll(':scope > .layer').forEach(n=>{if(gap(n)<24)problems.push('section-gap:'+n.dataset.explanation)});
 root.querySelectorAll('.part + .part,[data-subpart] + [data-subpart]').forEach(n=>{if(gap(n)<16)problems.push('part-gap')});
 root.querySelectorAll('.layer h4,.sum h4').forEach(n=>{if(parseFloat(get(n).marginBottom)<12)problems.push('heading-gap')});
 root.querySelectorAll('.summary-group + .summary-group').forEach(n=>{if(gap(n)<24)problems.push('summary-gap')});
 const overflowingInline=math.filter(n=>!n.closest('.math-row')).filter(n=>{
  const r=n.getBoundingClientRect(),p=n.parentElement.getBoundingClientRect();return r.width>p.width+3;
 });
 if(overflowingInline.length)problems.push('unhandled-wide-inline:'+overflowingInline.length);
 return {problems,math:math.length,pan:[...root.querySelectorAll('.math-pan')].map(n=>({width:n.clientWidth,scroll:n.scrollWidth,tex:n.querySelector('annotation')?.textContent}))};
}'''
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width,height in [(1280,900),(375,812)]:
   for theme in ['light','dark']:
    context=browser.new_context(viewport={'width':width,'height':height},color_scheme=theme)
    page=context.new_page();errors=[];external=[];missing=[];reports=[]
    def route(r):
     if urllib.parse.urlsplit(r.request.url).hostname!='127.0.0.1':external.append(r.request.url);r.abort()
     else:r.continue_()
    page.route('**/*',route)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
    page.on('response',lambda r:missing.append(r.url) if r.status>=400 else None)
    page.goto(url,wait_until='networkidle');assert page.locator('article.topic').count()==25
    page.locator('#pager-next').click()
    for n in range(1,26):
     if n>1:page.locator('#pager-next').click()
     assert page.locator(f'#p{n}').is_visible()
     assert page.locator(f'#p{n} [data-explanation="recall"]').count()==1
     assert page.locator(f'#p{n} [data-explanation="recall"]').inner_text().startswith('이 문제를 봤을 때 떠올릴 개념과 공식')
     assert page.locator(f'#p{n}').evaluate('(e)=>Array.from(e.querySelectorAll("[data-explanation]")).map(n=>n.dataset.explanation).join(",")')=='understand,recall,start,solve,verify,pitfall,retry' 
     page.wait_for_timeout(70)
     main=page.locator(f'#p{n}').evaluate(inspect)
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
     assert page.locator('.content').evaluate('(e)=>e.scrollWidth<=e.clientWidth+3')
     # Summary is tested at its real visible width on every page, not just first.
     if page.locator('#toggle-right').get_attribute('aria-expanded')!='true':page.locator('#toggle-right').click()
     page.wait_for_timeout(260)
     summary=page.locator('#panel-right .sum:not([hidden])').evaluate(inspect)
     assert '떠올릴 개념·공식' in page.locator('#panel-right .sum:not([hidden])').inner_text()
     if width==375:page.locator('#panel-right [data-panel-close]').click();page.wait_for_timeout(170)
     else:page.locator('#toggle-right').click();page.wait_for_timeout(70)
     problems=main['problems']+summary['problems']
     if problems:failures.append({'width':width,'theme':theme,'id':n,'issues':problems})
     reports.append({'id':n,'main':main,'summary':summary})
     page.evaluate('document.querySelector(".content").scrollTop=1e7')
     assert page.locator(f'#p{n} [data-explanation="retry"]').is_visible()
     if n in [1,13,18,22,25]:
      if n==1:
       page.locator('#p1 [data-explanation="recall"]').scroll_into_view_if_needed()
      else:page.locator(f'#p{n} [data-explanation="recall"]').scroll_into_view_if_needed()
      page.screenshot(path=str(evidence/f'layout-p{n}-{width}-{theme}.png'))
    page.locator('#pager-prev').click();assert page.locator('#p24').is_visible()
    if width==375:page.locator('#toggle-left').click()
    page.locator('#panel-left a[href="#p1"]').click();page.wait_for_timeout(450)
    if width==375 and page.locator('#panel-left').evaluate('(e)=>e.classList.contains("is-open")'):
     page.locator('#panel-left [data-panel-close]').click();page.wait_for_timeout(170)
    page.locator('#toggle-right').click();page.wait_for_timeout(260)
    page.screenshot(path=str(evidence/f'layout-summary-{width}-{theme}.png'))
    assert page.locator('.katex-error').count()==0
    assert not errors and not missing and not external,(errors,missing,external)
    rows.append({'viewport':[width,height],'theme':theme,'reports':reports,'errors':errors,'missing':missing,'external':external})
    context.close()
  browser.close()
finally:server.shutdown();server.server_close()
(evidence/'recall-browser-results.json').write_text(json.dumps({'html_sha256':hashlib.sha256((stage/meta['html']).read_bytes()).hexdigest(),'runs':rows,'failures':failures},indent=2),encoding='utf-8')
print('Checked 100 main+summary views; failures:',json.dumps(failures,ensure_ascii=False))
assert not failures
