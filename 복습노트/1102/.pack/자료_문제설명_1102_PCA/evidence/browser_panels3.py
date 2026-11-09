"""띄운 문제 패널의 머리 끌기·.float-resize 크기 조절·화면 내 제한·새로고침 유지. python3 browser_panels3.py <base_url>"""
import json, sys
from playwright.sync_api import sync_playwright
PAGE = sys.argv[1] + '/%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1102_PCA.html'
G = "()=>{const r=document.querySelector('.panel-prob').getBoundingClientRect(); return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),inView:r.left>=0&&r.top>=0&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1}}"
res = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 900}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(PAGE + '#p5'); pg.wait_for_timeout(700)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(x=>(x.getAttribute('aria-label')||x.innerText.trim())==='띄우기').click()"); pg.wait_for_timeout(300)
    res['float'] = pg.evaluate(G)
    head = pg.evaluate("()=>{const h=document.querySelector('.panel-prob .panel-head'); if(!h) return null; const r=h.getBoundingClientRect(); return {x:r.x+r.width*0.45,y:r.y+r.height/2,tag:h.tagName,cls:h.className}}")
    res['dragHandle'] = head
    if head:
        pg.mouse.move(head['x'], head['y']); pg.mouse.down(); pg.mouse.move(head['x'] - 500, head['y'] + 200, steps=10); pg.mouse.up(); pg.wait_for_timeout(300)
        res['afterDrag'] = pg.evaluate(G)
        rz = pg.evaluate("()=>{const e=document.querySelector('.float-resize'); if(!e) return null; const r=e.getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2,w:r.width}}")
        res['resizeHandle'] = rz
        if rz and rz['w']:
            before = pg.evaluate(G); pg.mouse.move(rz['x'], rz['y']); pg.mouse.down(); pg.mouse.move(rz['x'] + 120, rz['y'] + 100, steps=10); pg.mouse.up(); pg.wait_for_timeout(300)
            res['afterResize'] = pg.evaluate(G); res['resizeBefore'] = before
        pg.mouse.move(head['x'] - 500, head['y'] + 200); pg.mouse.down(); pg.mouse.move(3000, 3000, steps=10); pg.mouse.up(); pg.wait_for_timeout(300)
        res['afterDragOut'] = pg.evaluate(G)
    pg.reload(); pg.wait_for_timeout(700); res['afterReload'] = pg.evaluate(G)
    res['errors'] = errs; br.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
