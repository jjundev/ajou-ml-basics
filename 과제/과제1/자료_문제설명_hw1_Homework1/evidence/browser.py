from pathlib import Path
import json,threading,functools,urllib.parse
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright
folder=Path(__file__).parent/'homework-1-Homework1'
meta=json.loads((folder/'stage.json').read_text(encoding='utf-8'))
stage=folder/meta['stage'];evidence=folder/'evidence'
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(stage)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'+urllib.parse.quote(meta['html'])
rows=[]
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        for width,height in [(1280,900),(375,812)]:
            for theme in ['light','dark']:
                context=browser.new_context(viewport={'width':width,'height':height},color_scheme=theme)
                page=context.new_page();errors=[];external=[];missing=[]
                def route(r):
                    if urllib.parse.urlsplit(r.request.url).hostname!='127.0.0.1':external.append(r.request.url);r.abort()
                    else:r.continue_()
                page.route('**/*',route)
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
                page.on('response',lambda r:missing.append(r.url) if r.status>=400 else None)
                page.goto(url,wait_until='networkidle')
                assert page.locator('article.topic').count()==25
                assert page.locator('.katex-error').count()==0
                assert page.locator('.katex').count()>200
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                page.locator('#pager-next').click()
                assert page.locator('#p1').is_visible()
                page.locator('#toggle-right').click()
                assert page.locator('#panel-right .sum:not([hidden])').count()==1
                if width==375: page.locator('#panel-right [data-panel-close]').click()
                else: page.locator('#toggle-right').click()
                # Traverse all pages, checking entire body and bottom rather than just hero.
                for n in range(1,26):
                    assert page.locator(f'#p{n}').is_visible()
                    assert page.locator(f'#p{n} [data-explanation="retry"]').count()==1
                    page.evaluate('document.querySelector(".content").scrollTop=1e7')
                    assert page.locator(f'#p{n} [data-explanation="retry"]').is_visible()
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                    if n<25: page.locator('#pager-next').click()
                page.locator('#pager-prev').click();assert page.locator('#p24').is_visible()
                if width==375:page.locator('#toggle-left').click()
                page.locator('#panel-left a[href="#p22"]').click();assert page.locator('#p22').is_visible()
                page.wait_for_timeout(450)
                if width==375 and page.locator('#panel-left').evaluate('(el)=>el.classList.contains("is-open")'):
                    page.locator('#panel-left [data-panel-close]').click()
                    page.wait_for_timeout(450)
                page.evaluate('document.querySelector(".content").scrollTop=0')
                page.screenshot(path=str(evidence/f'browser-{width}-{theme}.png'))
                page.locator('#p22 [data-explanation="start"]').scroll_into_view_if_needed()
                page.screenshot(path=str(evidence/f'explanation-{width}-{theme}.png'))
                scrolling=page.locator('#p22 .katex').evaluate_all('(els)=>els.filter(e=>e.scrollWidth>e.clientWidth+1 && getComputedStyle(e).overflowX==="auto").length')
                assert scrolling>0
                assert not errors and not external and not missing,(errors,external,missing)
                assert page.locator('.katex-error').count()==0
                rows.append({'viewport':[width,height],'theme':theme,'pages':25,'console_errors':errors,'external_requests':external,'missing_resources':missing,'katex_errors':0,'document_overflow':False,'navigation_summary_toc':'pass'})
                context.close()
        browser.close()
finally:server.shutdown();server.server_close()
(evidence/'browser-results.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print('PASS four viewports/themes; 100 page visits; navigation, summary, TOC, math, offline resources')
