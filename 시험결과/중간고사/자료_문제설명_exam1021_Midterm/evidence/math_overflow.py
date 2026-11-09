import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h in [(1024,900),(375,812),(1280,900)]:
        pg=b.new_page(viewport={'width':w,'height':h}); pg.goto(url+'#p1',wait_until='networkidle'); pg.wait_for_timeout(600)
        for n in range(1,11):
            pg.goto(url+f'#p{n}'); pg.wait_for_timeout(300)
            res=pg.evaluate("""() => [...document.querySelectorAll('.katex-display')].filter(e=>e.offsetParent).map(e=>{
                const box=e.parentElement; return {over: e.scrollWidth - e.clientWidth, txt: (e.querySelector('annotation')||{}).textContent?.slice(0,60), inSum: !!e.closest('.sums,#sum-for'), inPanel: !!e.closest('[data-problem-panel],.problem-panel,aside')}
            }).filter(x=>x.over>2)""")
            for r in res: print(w, f'p{n}', r)
    b.close()
