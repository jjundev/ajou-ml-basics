"""문제 패널 붙이기/띄우기·이동·크기 조절과 인쇄 미디어 표시 확인. python3 browser_panels2.py <base_url>"""
import json, sys
from playwright.sync_api import sync_playwright
PAGE = sys.argv[1] + '/%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1102_PCA.html'
GEO = "(n)=>{const b=[...document.querySelectorAll('button')].find(x=>x.innerText.trim()===n||x.getAttribute('aria-label')===n); let p=b; while(p&&p.parentElement&&!(p.getBoundingClientRect().height>300)) p=p.parentElement; const r=p.getBoundingClientRect(); return {id:p.id,cls:p.className,x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),inView:r.left>=0&&r.top>=0&&r.right<=innerWidth&&r.bottom<=innerHeight,state:localStorage.getItem('od-panels:explain:v2')}}"
res = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 900}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(PAGE + '#p5'); pg.wait_for_timeout(700)
    for name in ['왼쪽에 붙이기', '오른쪽에 붙이기', '띄우기']:
        res[name+'-attrs']=pg.evaluate("(n)=>{const b=[...document.querySelectorAll('button')].find(x=>(x.getAttribute('aria-label')||x.innerText.trim())===n); if(!b) return null; const a={disabled:b.disabled, pressed:b.getAttribute('aria-pressed')}; b.click(); return a}", name); pg.wait_for_timeout(350)
        res[name] = pg.evaluate(GEO, '원문')
    # drag floating panel by its header and resize via bottom-right corner, then check it stays within viewport
    g = res['띄우기']
    pg.mouse.move(g['x'] + 40, g['y'] + 12); pg.mouse.down(); pg.mouse.move(g['x'] + 2000, g['y'] + 2000, steps=8); pg.mouse.up(); pg.wait_for_timeout(300)
    res['afterDragFar'] = pg.evaluate(GEO, '원문')
    g = res['afterDragFar']
    pg.mouse.move(g['x'] + g['w'] - 3, g['y'] + g['h'] - 3); pg.mouse.down(); pg.mouse.move(g['x'] + g['w'] + 400, g['y'] + g['h'] + 400, steps=8); pg.mouse.up(); pg.wait_for_timeout(300)
    res['afterResize'] = pg.evaluate(GEO, '원문')
    pg.reload(); pg.wait_for_timeout(700); res['afterReload'] = pg.evaluate(GEO, '원문')
    pg.emulate_media(media='print'); pg.wait_for_timeout(300)
    res['printVisibleExplain'] = pg.evaluate("()=>[...document.querySelectorAll('[data-explanation]')].filter(e=>e.getBoundingClientRect().height>0).length")
    res['printOriginalText'] = pg.evaluate("()=>document.body.innerText.includes('Compute the determinant using the Laplace expansion')")
    res['errors'] = errs; br.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
