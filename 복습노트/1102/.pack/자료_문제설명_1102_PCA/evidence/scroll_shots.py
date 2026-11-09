"""스크롤 컨테이너를 따라 문항별 전체 본문을 캡처해 시트로 묶는다. python3 scroll_shots.py <base_url> <outdir> <w> <h> <scheme> [pids]"""
import sys, io
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
BASE, OUT, W, H, SCHEME = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
PIDS = sys.argv[6].split(',') if len(sys.argv) > 6 else ['p%d' % i for i in range(1, 11)]
OUT.mkdir(parents=True, exist_ok=True)
PAGE = BASE + '/%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1102_PCA.html'
FIND = r"""(id)=>{const s=document.getElementById(id); let e=s; while(e&&e!==document.body){const cs=getComputedStyle(e); if((cs.overflowY==='auto'||cs.overflowY==='scroll')&&e.scrollHeight>e.clientHeight+2) break; e=e.parentElement;}
 if(!e||e===document.body) e=document.scrollingElement; window.__sc=e; const r=s.getBoundingClientRect(); const cr=(e===document.scrollingElement)?{top:0,left:0}:e.getBoundingClientRect();
 return {top:e.scrollTop + r.top - cr.top, h:s.offsetHeight, ch:e.clientHeight, x:Math.max(0,r.left-8), w:Math.min(r.width+16, innerWidth)}}"""
with sync_playwright() as pw:
    br = pw.chromium.launch(); ctx = br.new_context(viewport={'width': W, 'height': H}, color_scheme=SCHEME); pg = ctx.new_page()
    for pid in PIDS:
        pg.goto(PAGE + '#' + pid); pg.wait_for_timeout(700)
        info = pg.evaluate(FIND, pid); tiles = []; y = info['top']; end = info['top'] + info['h']
        while y < end and len(tiles) < 14:
            pg.evaluate('(y)=>{window.__sc.scrollTop=y}', y); pg.wait_for_timeout(250)
            png = pg.screenshot(clip={'x': info['x'], 'y': 0, 'width': info['w'], 'height': H})
            tiles.append(Image.open(io.BytesIO(png)).convert('RGB')); y += info['ch'] - 60
        tw, th = tiles[0].size; sheet = Image.new('RGB', (len(tiles) * (tw + 8), th), 'gray')
        for i, t in enumerate(tiles): sheet.paste(t, (i * (tw + 8), 0))
        sheet.save(OUT / f'{W}x{H}-{SCHEME}-{pid}.png'); print(pid, len(tiles), tw, sheet.size)
    br.close()
