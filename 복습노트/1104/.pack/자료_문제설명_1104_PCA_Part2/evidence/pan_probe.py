"""375/1024/1280에서 '가로로 밀어 전체 수식 읽기' 안내가 붙은(국소 이동) 수식과 그 TeX를 문항별로 나열. python3 pan_probe.py <base_url>"""
import json, sys
from playwright.sync_api import sync_playwright
PAGE = sys.argv[1] + '/%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1104_PCA_Part2.html'
out = {}
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for w, h in [(375, 812), (1024, 900), (1280, 900)]:
        pg = br.new_page(viewport={'width': w, 'height': h})
        for i in range(1, 11):
            pid = f'p{i}'
            pg.goto(PAGE + '#' + pid); pg.wait_for_timeout(600)
            r = pg.evaluate("""(id)=>{const sec=document.getElementById(id); const rows=[...document.querySelectorAll('.math-row')].filter(r=>{const n=r.nextElementSibling; return n && /가로로 밀어/.test(n.textContent) && (sec.contains(r) || r.closest('.sums,.problem-workspace'))}); return rows.map(r=>{const a=r.querySelector('annotation'); return {where: sec.contains(r)?(r.closest('[data-explanation]')||{}).dataset?.explanation:'panel', tex:(a?a.textContent:'').slice(0,90), over: r.scrollWidth - r.clientWidth}})}""", pid)
            if r: out[f'{w}-{pid}'] = r
        pg.close()
    br.close()
print(json.dumps(out, ensure_ascii=False, indent=1))
