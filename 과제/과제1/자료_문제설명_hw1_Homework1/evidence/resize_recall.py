from pathlib import Path
import json,threading,functools,urllib.parse,hashlib
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright
folder=Path(__file__).parent.parent
meta=json.loads((folder/'stage.json').read_text(encoding='utf-8'))
stage=folder/meta['stage']; evidence=folder/'evidence'
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(stage)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'+urllib.parse.quote(meta['html'])
rows=[]
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        for theme in ['light','dark']:
            ctx=browser.new_context(viewport={'width':1280,'height':900},color_scheme=theme)
            page=ctx.new_page();errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(url,wait_until='networkidle');page.locator('#pager-next').click()
            if page.locator('#toggle-right').get_attribute('aria-expanded')!='true':
                page.locator('#toggle-right').click()
            page.wait_for_timeout(350)
            panel=page.locator('#panel-right');handle=panel.locator('.panel-resize')
            before=panel.bounding_box()['width']
            handle.focus();handle.press('Shift+ArrowLeft');page.wait_for_timeout(350)
            wider=panel.bounding_box()['width'];assert wider>before,(before,wider)
            handle.press('Home');page.wait_for_timeout(350)
            reset=panel.bounding_box()['width'];assert abs(reset-before)<2
            box=handle.bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+40)
            page.mouse.down();page.mouse.move(box['x']-60,box['y']+40,steps=8);page.mouse.up()
            page.wait_for_timeout(350)
            dragged=panel.bounding_box()['width'];assert dragged>reset
            handle.focus();handle.press('Home')
            for n in [1,13,18,22,25]:
                page.locator(f'#panel-left a[href="#p{n}"]').click();page.wait_for_timeout(250)
                assert '떠올릴 개념·공식' in panel.locator('.sum:not([hidden])').inner_text()
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                assert page.locator('.katex-error').count()==0
            page.screenshot(path=str(evidence/f'resize-summary-{theme}.png'))
            assert not errors,errors
            rows.append({'theme':theme,'before':before,'keyboard':wider,'reset':reset,'dragged':dragged,'errors':errors})
            ctx.close()
        browser.close()
finally:server.shutdown();server.server_close()
report={'html_sha256':hashlib.sha256((stage/meta['html']).read_bytes()).hexdigest(),'runs':rows}
(evidence/'resize-recall-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PASS: keyboard/drag/Home resizing and summaries for P1/P13/P18/P22/P25 in both themes')
