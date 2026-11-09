"""패널 저장 닫힘 유지·문제 패널 붙이기/띄우기·이동·크기 제한·read 저장 키·인쇄 미디어 원문 보존 확인. python3 browser_panels.py <base_url>"""
import json, sys
from playwright.sync_api import sync_playwright
PAGE = sys.argv[1] + '/%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1104_PCA_Part2.html'
res = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(); ctx = br.new_context(viewport={'width': 1280, 'height': 900}); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(PAGE + '#p5'); pg.wait_for_timeout(700)
    res['buttons'] = pg.evaluate("()=>[...document.querySelectorAll('button')].filter(b=>b.offsetParent).map(b=>(b.getAttribute('aria-label')||b.innerText||'').trim()).filter(Boolean).slice(0,40)")
    vis = "(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden'}"
    # close TOC via its toggle, reload, check persists
    tog = pg.get_by_role('button', name='목차')
    res['tocBefore'] = pg.evaluate(vis, '#panel-left')
    if tog.count(): tog.first.click(); pg.wait_for_timeout(300)
    res['tocAfterClose'] = pg.evaluate(vis, '#panel-left')
    pg.reload(); pg.wait_for_timeout(700)
    res['tocAfterReload'] = pg.evaluate(vis, '#panel-left')
    res['storageKeys'] = pg.evaluate("()=>Object.keys(localStorage)")
    res['probPanelState'] = pg.evaluate("()=>localStorage.getItem('od-panels:explain:v2:prob')")
    # dock / float controls of problem panel
    for name in ['왼쪽', '오른쪽', '띄우기']:
        b = pg.locator('#panel-prob button', has_text=name)
        if not b.count(): b = pg.get_by_role('button', name=name)
        if b.count() and b.first.is_visible():
            b.first.click(); pg.wait_for_timeout(300)
            res['dock-' + name] = pg.evaluate("()=>{const p=document.querySelector('#panel-prob'); if(!p) return null; const r=p.getBoundingClientRect(); return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),cls:p.className,state:localStorage.getItem('od-panels:explain:v2:prob')}}")
    res['overflowX'] = pg.evaluate("()=>document.documentElement.scrollWidth-document.documentElement.clientWidth")
    pg.emulate_media(media='print'); pg.wait_for_timeout(300)
    res['print'] = pg.evaluate("()=>({sections:document.querySelectorAll('main section[id^=p]').length, origDetails:document.querySelectorAll('details').length, probText:(document.querySelector('#p5 [data-source-field], #p5 .problem, #p5')||{}).innerText?.includes('ignore the contribution of A3')})")
    res['errors'] = errs
    br.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
