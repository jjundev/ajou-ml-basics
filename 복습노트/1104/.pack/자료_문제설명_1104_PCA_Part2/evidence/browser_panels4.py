"""띄운 문제 패널을 현재 머리 위치에서 화면 밖으로 끌 때 화면 안에 남는지, 문제 탭의 그림 확대(p1)를 확인. python3 browser_panels4.py <base_url>"""
import json, sys
from playwright.sync_api import sync_playwright
PAGE = sys.argv[1] + '/%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1104_PCA_Part2.html'
G = "()=>{const r=document.querySelector('.panel-prob').getBoundingClientRect(); return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),inView:r.left>=-1&&r.top>=-1&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1}}"
H = "()=>{const r=document.querySelector('.panel-prob .panel-head').getBoundingClientRect(); return {x:r.x+r.width*0.45,y:r.y+r.height/2}}"
res = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 900}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(PAGE + '#p1'); pg.wait_for_timeout(800)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(x=>(x.getAttribute('aria-label')||x.innerText.trim())==='띄우기').click()"); pg.wait_for_timeout(300)
    for tgt in [(3000, 3000), (-2000, -2000)]:
        h = pg.evaluate(H); pg.mouse.move(h['x'], h['y']); pg.mouse.down(); pg.mouse.move(*tgt, steps=10); pg.mouse.up(); pg.wait_for_timeout(300)
        res[f'dragTo{tgt}'] = pg.evaluate(G)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(x=>(x.getAttribute('aria-label')||x.innerText.trim())==='오른쪽에 붙이기').click()"); pg.wait_for_timeout(300)
    imgs = pg.evaluate("()=>[...document.querySelectorAll('.problem-workspace img, main img')].filter(i=>i.offsetParent).map(i=>({src:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0,w:Math.round(i.getBoundingClientRect().width)}))")
    res['imgs'] = imgs
    im = pg.locator('.problem-workspace img').first
    if im.count():
        im.click(); pg.wait_for_timeout(400)
        res['zoom'] = pg.evaluate("()=>{const d=document.querySelector('dialog[open], .lightbox, .zoom-overlay, [class*=zoom][class*=open], [aria-modal=true]'); if(!d) return null; const i=d.querySelector('img'); const r=(i||d).getBoundingClientRect(); return {tag:d.tagName,cls:d.className,w:Math.round(r.width),h:Math.round(r.height)}}")
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        res['zoomClosed'] = pg.evaluate("()=>!document.querySelector('dialog[open], [aria-modal=true]')")
    for pid in ['p2', 'p3', 'p5']:
        pg.goto(PAGE + '#' + pid); pg.wait_for_timeout(500)
        res['assets-' + pid] = pg.evaluate("(id)=>({imgs:[...document.querySelectorAll('.problem-workspace img')].filter(i=>i.offsetParent).map(i=>i.complete&&i.naturalWidth>0), tables:[...document.querySelectorAll('.problem-workspace table')].filter(t=>t.offsetParent).length})", pid)
    res['errors'] = errs; br.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
