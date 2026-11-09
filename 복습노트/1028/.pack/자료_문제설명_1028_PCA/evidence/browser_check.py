"""실제 렌더링 검토(1028 PCA 문제설명 stage). 로컬 http 서버(stage+정리노트·복습문제 사본)를 대상으로
1280x900·1024x900·375x812 × light/dark에서 문항마다 KaTeX 오류, 콘솔 오류, 실패·외부 요청, 문서 가로 넘침,
수식 스크롤, 요약 전환, 간격을 측정하고 스크린샷을 남긴다.
python3 browser_check.py <base_url> <shot_dir> > browser_results.json"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE, SHOTS = sys.argv[1], Path(sys.argv[2])
SHOTS.mkdir(parents=True, exist_ok=True)
PAGE = BASE + '/%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1028_PCA.html'
IDS = ['p1', 'p2', 'p3', 'p4', 'p5']
PROBE = r"""
(id) => {
  const d = document, sec = d.getElementById(id);
  const ov = d.documentElement.scrollWidth - d.documentElement.clientWidth;
  const disp = [...sec.querySelectorAll('.katex-display')];
  const dispScroll = disp.filter(e => e.scrollWidth > e.clientWidth + 1).length;
  const visScrollbar = disp.filter(e => e.offsetHeight - e.clientHeight > 1).length;
  const inlineScroll = [...sec.querySelectorAll('.katex')].filter(k => !k.closest('.katex-display')).filter(k => {
    let p = k.parentElement; const cs = getComputedStyle(p); return (cs.overflowX === 'auto' || cs.overflowX === 'scroll') && p.tagName !== 'P' && p.tagName !== 'DIV';
  }).length;
  const blocks = [...sec.querySelectorAll(':scope [data-explanation]')];
  const gaps = []; for (let i = 1; i < blocks.length; i++) { const a = blocks[i-1].getBoundingClientRect(), b = blocks[i].getBoundingClientRect(); if (a.height && b.height) gaps.push(Math.round(b.top - a.bottom)); }
  const h4gaps = blocks.map(b => { const h = b.querySelector(':scope > h4'); const n = h && h.nextElementSibling; if (!h || !n || !n.getBoundingClientRect().height) return null; return Math.round(n.getBoundingClientRect().top - h.getBoundingClientRect().bottom); }).filter(x => x !== null);
  const subs = [...sec.querySelectorAll('[data-subpart] + [data-subpart]')].map(s => Math.round(s.getBoundingClientRect().top - s.previousElementSibling.getBoundingClientRect().bottom));
  const sum = d.querySelectorAll('#sum-for .sum:not([hidden])');
  const clipped = [...sec.querySelectorAll('.katex-display, .katex')].filter(k => { const r = k.getBoundingClientRect(); const c = sec.getBoundingClientRect(); return r.width && (r.right > c.right + 2 || r.left < c.left - 2) && !k.closest('.katex-display[style*=overflow]'); }).length;
  const links = [...sec.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
  return { id, katexErr: d.querySelectorAll('.katex-error').length, rawDollarInSection: (sec.innerText.match(/\$\S/g) || []).length,
    overflowX: ov, dispCount: disp.length, dispScroll, visScrollbar, inlineScroll, clipped, sectionGaps: [...new Set(gaps)], h4gaps: [...new Set(h4gaps)], subpartGaps: [...new Set(subs)],
    visibleSums: sum.length, sumHead: sum[0] ? sum[0].innerText.slice(0, 30) : null, rightTitleDup: d.querySelectorAll('#sum-for h3').length,
    h3: (sec.querySelector('h3') || {}).textContent, pager: (d.getElementById('pager-status') || {}).textContent, theme: getComputedStyle(d.body).backgroundColor, links };
}
"""
out = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    try:
        for (w, h) in [(1280, 900), (1024, 900), (375, 812)]:
            for scheme in ['light', 'dark']:
                ctx = br.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme)
                pg = ctx.new_page()
                cons, failed, external = [], [], []
                pg.on('console', lambda m: cons.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
                pg.on('pageerror', lambda e: cons.append('pageerror: ' + str(e)))
                pg.on('requestfailed', lambda r: failed.append(r.url))
                pg.on('response', lambda r: failed.append(f'{r.status} {r.url}') if r.status >= 400 else None)
                pg.on('request', lambda r: external.append(r.url) if not r.url.startswith(BASE) and not r.url.startswith('data:') else None)
                pg.goto(PAGE); pg.wait_for_timeout(900)
                cfg = {'viewport': f'{w}x{h}', 'scheme': scheme, 'problems': []}
                cfg['tocOpen'] = pg.evaluate("() => { const l = document.getElementById('panel-left'); return l ? l.getBoundingClientRect().width > 0 && getComputedStyle(l).visibility !== 'hidden' : null }")
                for pid in IDS:
                    pg.goto(PAGE + '#' + pid); pg.wait_for_timeout(500)
                    r = pg.evaluate(PROBE, pid)
                    cfg['problems'].append(r)
                    pg.screenshot(path=str(SHOTS / f'{w}x{h}-{scheme}-{pid}.png'), full_page=False)
                    if w == 375:
                        pg.screenshot(path=str(SHOTS / f'{w}x{h}-{scheme}-{pid}-full.png'), full_page=True)
                    else:
                        sec = pg.locator('#' + pid)
                        sec.screenshot(path=str(SHOTS / f'{w}x{h}-{scheme}-{pid}-section.png'))
                # pager next/prev from p1
                pg.goto(PAGE + '#p1'); pg.wait_for_timeout(400)
                nxt = pg.locator('#pager-bar button, #pager-bar a').all()
                cfg['pagerControls'] = [n.inner_text().strip() for n in nxt]
                cfg['console'] = cons; cfg['failed'] = failed; cfg['external'] = external
                out.append(cfg)
                ctx.close()
    finally:
        br.close()
print(json.dumps(out, ensure_ascii=False, indent=1))
