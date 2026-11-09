"""패널·pager·탭·모바일 접힘·1023/1024 경계 상호작용 확인. python3 browser_interact.py <base_url>"""
import json, sys
from playwright.sync_api import sync_playwright
BASE = sys.argv[1]; PAGE = BASE + '/%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1028_PCA.html'
res = {}
with sync_playwright() as pw:
    br = pw.chromium.launch()
    try:
        for w in (1023, 1024, 1280):
            ctx = br.new_context(viewport={'width': w, 'height': 900}); pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(PAGE + '#p1'); pg.wait_for_timeout(700)
            vis = lambda sel: pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>0 && r.height>0 && getComputedStyle(e).visibility!=='hidden'}", sel)
            r = {'leftOpen': vis('#panel-left'), 'probOpen': vis('#panel-prob') if pg.query_selector('#panel-prob') else None}
            seq = []
            for _ in range(5):
                seq.append(pg.evaluate("()=>location.hash+' | '+(document.getElementById('pager-status')||{}).textContent"))
                btn = pg.get_by_role('button', name='다음')
                if btn.count() and btn.first.is_visible(): btn.first.click(); pg.wait_for_timeout(350)
                else: break
            r['pagerNext'] = seq
            prev = pg.get_by_role('button', name='이전')
            if prev.count() and prev.first.is_visible(): prev.first.click(); pg.wait_for_timeout(350)
            r['afterPrev'] = pg.evaluate("()=>location.hash")
            tabs = pg.locator('[role=tab]')
            names = [t.inner_text().strip() for t in tabs.all() if t.is_visible()]
            r['tabs'] = names
            shown = {}
            for t in tabs.all():
                if not t.is_visible(): continue
                n = t.inner_text().strip(); t.click(); pg.wait_for_timeout(200)
                shown[n] = pg.evaluate("()=>{const p=[...document.querySelectorAll('[role=tabpanel]')].find(x=>x.offsetParent && !x.hidden); return p? p.innerText.slice(0,70):null}")
            r['tabPanels'] = shown
            r['errors'] = errs
            res[str(w)] = r; ctx.close()
        ctx = br.new_context(viewport={'width': 375, 'height': 812}, is_mobile=True, has_touch=True); pg = ctx.new_page()
        pg.goto(PAGE + '#p3'); pg.wait_for_timeout(700)
        btn = pg.get_by_role('button', name='문제 보기')
        r = {'probToggle': btn.count()}
        r['overflowX'] = pg.evaluate("()=>document.documentElement.scrollWidth-document.documentElement.clientWidth")
        if btn.count() and btn.first.is_visible():
            btn.first.click(); pg.wait_for_timeout(300)
            r['afterOpen'] = pg.evaluate("()=>{const t=[...document.querySelectorAll('details[open], [aria-expanded=true]')].map(e=>e.tagName+':'+(e.innerText||'').slice(0,40)); return t}")
        res['375'] = r; ctx.close()
    finally:
        br.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
