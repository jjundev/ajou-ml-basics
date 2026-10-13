"""Real Chromium checks for every problem, four viewport/theme combinations."""
from pathlib import Path
import json,sys,threading,functools,urllib.parse,hashlib
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
REPO=ROOT.parents[2];sys.path.insert(0,str(REPO/'.claude/skills/ml-problem-explain/scripts'))
from mpe_cli import load_run,load_artifacts
INSPECT=r'''(root)=>{
 const problems=[],get=n=>getComputedStyle(n);
 const math=[...root.querySelectorAll('.katex')].filter(n=>n.getClientRects().length);
 if(math.filter(n=>!n.closest('.math-row')&&get(n).overflowX!=='visible').length)problems.push('inline-scroll');
 for(const n of [...root.querySelectorAll('.math-row')].filter(n=>n.getClientRects().length)){
  if(n.scrollWidth>n.clientWidth+3&&!n.classList.contains('math-pan'))problems.push('wide-math');
  if(n.classList.contains('math-pan')&&get(n).scrollbarWidth!=='none')problems.push('visible-scrollbar');
  if(n.scrollHeight>n.clientHeight+3)problems.push('vertical-math-clipping');
 }
 for(const n of root.querySelectorAll(':scope > .layer'))if(parseFloat(get(n).marginTop)<24)problems.push('section-gap');
 for(const n of root.querySelectorAll('[data-subpart] + [data-subpart]'))if(parseFloat(get(n).marginTop)<16)problems.push('subpart-gap');
 for(const n of root.querySelectorAll('.layer h4,.sum h4'))if(parseFloat(get(n).marginBottom)<12)problems.push('heading-gap');
 const wide=math.filter(n=>!n.closest('.math-row')).filter(n=>n.getBoundingClientRect().width>n.parentElement.getBoundingClientRect().width+3);
 if(wide.length)problems.push('wide-inline:'+wide.length);
 return {problems,math:math.length,pan:[...root.querySelectorAll('.math-pan')].map(n=>({width:n.clientWidth,scroll:n.scrollWidth,tex:n.querySelector('annotation')?.textContent}))};
}'''
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass

def examine(date,published=False):
 item=load_run(ROOT/date)[0];pack=item['pack'];art=load_artifacts(item)
 base=pack.path.parent if published else art.html.parent
 target=base/art.html.name
 evidence=item['folder']/'evidence';evidence.mkdir(exist_ok=True)
 server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(REPO if published else base)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 rel=target.relative_to(REPO) if published else Path(target.name)
 url=f'http://127.0.0.1:{server.server_port}/'+urllib.parse.quote(str(rel))
 rows=[];failures=[]
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
     page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
     page.on('response',lambda r:missing.append(r.url) if r.status>=400 else None)
     page.goto(url,wait_until='networkidle')
     assert page.locator('article.topic').count()==len(pack.problems)
     page.locator('#pager-next').click()
     for i,p in enumerate(pack.problems):
      if i:page.locator('#pager-next').click()
      topic=page.locator('#'+p.id);assert topic.is_visible()
      assert topic.evaluate('(e)=>Array.from(e.querySelectorAll("[data-explanation]")).map(n=>n.dataset.explanation).join(",")')=='understand,recall,start,solve,verify,pitfall,retry'
      page.wait_for_timeout(60)
      main=topic.evaluate(INSPECT)
      if not page.evaluate('document.documentElement.scrollWidth<=innerWidth'):failures.append((width,theme,p.id,'document-overflow'))
      if not page.locator('.content').evaluate('(e)=>e.scrollWidth<=e.clientWidth+3'):failures.append((width,theme,p.id,'content-overflow'))
      if page.locator('#toggle-right').get_attribute('aria-expanded')!='true':page.locator('#toggle-right').click()
      page.wait_for_timeout(240)
      summary=page.locator('#panel-right .sum:not([hidden])').evaluate(INSPECT)
      assert '떠올릴 개념·공식' in page.locator('#panel-right .sum:not([hidden])').inner_text()
      if i in [0,len(pack.problems)-1]:page.screenshot(path=str(evidence/f'{"public" if published else "stage"}-summary-{p.id}-{width}-{theme}.png'))
      if width==375:page.locator('#panel-right [data-panel-close]').click()
      else:page.locator('#toggle-right').click()
      page.wait_for_timeout(170)
      for key in ['understand','recall','start','solve','verify','pitfall','retry']:
       topic.locator(f'[data-explanation="{key}"]').scroll_into_view_if_needed()
       assert topic.locator(f'[data-explanation="{key}"]').is_visible()
      topic.locator('[data-explanation="recall"]').scroll_into_view_if_needed()
      page.screenshot(path=str(evidence/f'{"public" if published else "stage"}-{p.id}-{width}-{theme}.png'))
      problems=main['problems']+summary['problems']
      if problems:failures.append((width,theme,p.id,problems))
      reports.append({'id':p.id,'main':main,'summary':summary})
     page.locator('#pager-prev').click();assert page.locator('#'+pack.problems[-2].id).is_visible()
     if width==375:page.locator('#toggle-left').click()
     page.locator('#panel-left a[href="#p1"]').click();page.wait_for_timeout(300)
     assert page.locator('#p1').is_visible()
     if page.locator('.katex-error').count():failures.append((width,theme,'katex-error'))
     if errors or external or missing:failures.append((width,theme,errors,external,missing))
     rows.append({'viewport':[width,height],'theme':theme,'reports':reports,'errors':errors,'external':external,'missing':missing})
     context.close()
   browser.close()
 finally:server.shutdown();server.server_close()
 report={'html_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'path':str(target),'rows':rows,'failures':failures}
 reportpath=evidence/('browser-public.json' if published else 'browser-stage.json');reportpath.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(date,'public' if published else 'stage',len(rows)*len(pack.problems),'views',failures,flush=True)
 return not failures
if __name__=='__main__':
 published='--published' in sys.argv;dates=[a for a in sys.argv[1:] if a!='--published'];ok=True
 for d in dates:ok=examine(d,published) and ok
 sys.exit(0 if ok else 1)
