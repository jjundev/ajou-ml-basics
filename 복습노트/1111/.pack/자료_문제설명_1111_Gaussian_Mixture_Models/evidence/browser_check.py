"""Playwright browser check for streamlined 1111 problem explanations.

Serves the current stage HTML & assets alongside sibling repo files on 127.0.0.1:0
(OS-assigned port), and verifies 1280x900, 1024x900, 375x812 x light/dark across p1..p8.
Usage:
  uv run python browser_check.py <repo_root> <stage_dir> <out_json> <shot_dir>
"""
from functools import partial
import http.server
import json
from pathlib import Path
import socketserver
import sys
import threading
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

REPO = Path(sys.argv[1]).resolve()
STAGE = Path(sys.argv[2]).resolve()
OUT_JSON = Path(sys.argv[3]).resolve()
SHOTS = Path(sys.argv[4]).resolve()
SHOTS.mkdir(parents=True, exist_ok=True)

IDS = [f'p{i}' for i in range(1, 9)]
HTML_NAME = '문제설명_1111_Gaussian_Mixture_Models.html'
PREFIX = '/복습노트/1111/'


class StageHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean = unquote(path.split('?', 1)[0].split('#', 1)[0])
        if clean.startswith(PREFIX):
            rel = clean[len(PREFIX):]
            cand = (STAGE / rel).resolve()
            if cand.is_relative_to(STAGE) and cand.is_file():
                return str(cand)
            cand_repo = (REPO / '복습노트' / '1111' / rel).resolve()
            if cand_repo.is_relative_to(REPO) and cand_repo.is_file():
                return str(cand_repo)
        cand_root = (REPO / clean.lstrip('/')).resolve()
        if cand_root.is_relative_to(REPO):
            return str(cand_root)
        return str(REPO / '__nonexistent__')

    def log_message(self, format, *args):
        pass


PROBE = r"""
(id) => {
  const d = document, sec = d.getElementById(id);
  const ov = d.documentElement.scrollWidth - d.documentElement.clientWidth;
  const disp = [...sec.querySelectorAll('.katex-display')];
  const dispScroll = disp.filter(e => e.scrollWidth > e.clientWidth + 1).length;
  const visScrollbar = disp.filter(e => e.offsetHeight - e.clientHeight > 1).length;
  const inlineScroll = [...sec.querySelectorAll('.katex')].filter(k => !k.closest('.katex-display')).filter(k => {
    let p = k.parentElement; const cs = getComputedStyle(p);
    return (cs.overflowX === 'auto' || cs.overflowX === 'scroll') && p.tagName !== 'P' && p.tagName !== 'DIV';
  }).length;
  const tableOverflows = [...sec.querySelectorAll('.table-wrap')].filter(tw => {
    const r = tw.getBoundingClientRect();
    const sr = sec.getBoundingClientRect();
    return r.width > sr.width + 2;
  }).length;
  const derivRows = [...sec.querySelectorAll('ol.deriv > li')].map(li => {
    const eq = li.querySelector('.deriv-eq');
    const why = li.querySelector('.deriv-why');
    const rLi = li.getBoundingClientRect();
    const rWhy = why ? why.getBoundingClientRect() : null;
    return {
      hasEq: !!eq,
      hasWhy: !!(why && why.textContent.trim()),
      isWide: li.classList.contains('is-wide'),
      overflow: rLi.width > sec.getBoundingClientRect().width + 2,
      whyVisible: !!(rWhy && rWhy.height > 0)
    };
  });
  const solve = sec.querySelector('[data-explanation="solve"]');
  const verify = sec.querySelector('[data-explanation="verify"]');
  const finalAns = solve ? solve.querySelector('section.final-answer') : null;
  const finalAfterSolve = !!(solve && finalAns && solve.lastElementChild === finalAns);
  const finalBeforeVerify = !!(finalAns && verify && finalAns.getBoundingClientRect().bottom <= verify.getBoundingClientRect().top + 2);
  const hasRetry = !!sec.querySelector('[data-explanation="retry"]');
  const footerText = (d.querySelector('footer') || {}).textContent || '';
  const hasPreservationFooter = /보존 안내|다시 풀 때/.test(footerText);
  const sum = d.querySelectorAll('#sum-for .sum:not([hidden])');
  const sumTerms = sum[0] ? sum[0].querySelectorAll('[data-summary-terms]') : [];
  const termsLastInSum = !!(sum[0] && sumTerms.length === 1 && sum[0].lastElementChild === sumTerms[0]);
  const sumTermsText = sumTerms[0] ? [...sumTerms[0].querySelectorAll('dt')].map(x => x.textContent.trim()) : [];
  const tabTerms = d.getElementById('tab-terms');
  const tabTermsHidden = tabTerms ? tabTerms.hidden : null;
  const tabOrig = d.getElementById('tab-original');
  const tabOrigHidden = tabOrig ? tabOrig.hidden : null;
  const clipped = [...sec.querySelectorAll('.katex-display, .katex')].filter(k => {
    const r = k.getBoundingClientRect(); const c = sec.getBoundingClientRect();
    return r.width && (r.right > c.right + 2 || r.left < c.left - 2) && !k.closest('.math-pan') && !k.closest('.table-wrap');
  }).length;
  const imgs = [...d.querySelectorAll('#panel-prob img, .problem-pane img')].map(img => ({
    src: img.getAttribute('src'), complete: img.complete, naturalWidth: img.naturalWidth
  }));
  return {
    id,
    katexErr: d.querySelectorAll('.katex-error').length,
    rawDollarInSection: (sec.innerText.match(/\$\S/g) || []).length,
    overflowX: ov,
    dispCount: disp.length,
    dispScroll,
    visScrollbar,
    inlineScroll,
    tableOverflows,
    derivRows,
    finalAfterSolve,
    finalBeforeVerify,
    hasRetry,
    hasPreservationFooter,
    visibleSums: sum.length,
    termsLastInSum,
    sumTermsText,
    tabTermsHidden,
    tabOrigHidden,
    clipped,
    imgs,
    rightTitleDup: d.querySelectorAll('#sum-for h3').length,
    h3: (sec.querySelector('h3') || {}).textContent,
    pager: (d.getElementById('pager-count') || {}).textContent,
    theme: getComputedStyle(d.body).backgroundColor
  };
}
"""

out = []
httpd = socketserver.TCPServer(('127.0.0.1', 0), StageHandler)
port = httpd.server_address[1]
thread = threading.Thread(target=httpd.serve_forever, daemon=True)
thread.start()

base_url = f'http://127.0.0.1:{port}'
page_url = base_url + '/%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1111/%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1111_Gaussian_Mixture_Models.html'

try:
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
                    pg.on('request', lambda r: external.append(r.url) if not r.url.startswith(base_url) and not r.url.startswith('data:') else None)
                    pg.goto(page_url)
                    pg.wait_for_timeout(900)
                    cfg = {'viewport': f'{w}x{h}', 'scheme': scheme, 'port': port, 'problems': []}
                    cfg['tocOpen'] = pg.evaluate("() => { const l = document.getElementById('panel-left'); return l ? l.getBoundingClientRect().width > 0 && getComputedStyle(l).visibility !== 'hidden' : null }")
                    cfg['probOpen'] = pg.evaluate("() => { const p = document.getElementById('panel-prob'); return p ? p.getBoundingClientRect().width > 0 && getComputedStyle(p).visibility !== 'hidden' : null }")
                    # Open summary drawer so we can verify sum-for & terms rendering visually as well
                    if w >= 1024:
                        pg.click('#toggle-right')
                        pg.wait_for_timeout(300)
                    for pid in IDS:
                        pg.goto(page_url + '#' + pid)
                        pg.wait_for_timeout(450)
                        r = pg.evaluate(PROBE, pid)
                        cfg['problems'].append(r)
                        if w in (1280, 375) and pid in ('p1', 'p3', 'p5', 'p6', 'p7'):
                            pg.screenshot(path=str(SHOTS / f'{w}x{h}-{scheme}-{pid}.png'), full_page=False)
                    cfg['console'] = cons
                    cfg['failed'] = failed
                    cfg['external'] = external
                    out.append(cfg)
                    ctx.close()
        finally:
            br.close()
finally:
    httpd.shutdown()
    httpd.server_close()

OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Wrote', OUT_JSON)
