"""Browser verification for 1116 EM Algorithm problem explanations on an ephemeral localhost port (127.0.0.1:0).

Usage:
  python3 browser_check.py <stage_dir> <repo_dir> <shot_dir> > browser_results.json
"""
import functools
import http.server
import json
import os
import socketserver
import sys
import threading
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

STAGE = Path(sys.argv[1]).resolve()
REPO = Path(sys.argv[2]).resolve()
SHOTS = Path(sys.argv[3]).resolve()
SHOTS.mkdir(parents=True, exist_ok=True)
DEST = (REPO / '복습노트' / '1116').resolve()

class StageHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean = unquote(path.split('?', 1)[0].split('#', 1)[0]).lstrip('/')
        if clean.startswith('복습노트/1116/'):
            rel = clean[len('복습노트/1116/'):]
            cand = (STAGE / rel).resolve()
            if cand.is_relative_to(STAGE) and cand.is_file():
                return str(cand)
            fallback = (DEST / rel).resolve()
            if fallback.is_relative_to(DEST):
                return str(fallback)
        cand = (REPO / clean).resolve()
        return str(cand)

    def log_message(self, format, *args):
        pass

class ThreadedTCPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

IDS = [f'p{i}' for i in range(1, 9)]

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
  const wraps = [...sec.querySelectorAll('.table-wrap')];
  const tableOverflow = wraps.filter(w => {
    const r = w.getBoundingClientRect();
    const sr = sec.getBoundingClientRect();
    return r.width > sr.width + 2;
  }).length;
  const blocks = [...sec.querySelectorAll(':scope > [data-explanation]')];
  const order = blocks.map(b => b.getAttribute('data-explanation'));
  const hasRetry = sec.querySelectorAll('[data-explanation="retry"]').length;
  const hasFooterNotice = /보존/.test((d.querySelector('footer') || {}).innerText || '');
  const solve = sec.querySelector('[data-explanation="solve"]');
  const verify = sec.querySelector('[data-explanation="verify"]');
  const fa = solve ? solve.querySelector(':scope > section.final-answer') : null;
  const faIsLastInSolve = Boolean(fa && solve.lastElementChild === fa);
  const faBeforeVerify = Boolean(fa && verify && (solve.compareDocumentPosition(verify) & Node.DOCUMENT_POSITION_FOLLOWING));
  const gaps = [];
  for (let i = 1; i < blocks.length; i++) {
    const a = blocks[i - 1].getBoundingClientRect(), b = blocks[i].getBoundingClientRect();
    if (a.height && b.height) gaps.push(Math.round(b.top - a.bottom));
  }
  const sumNodes = [...d.querySelectorAll('#sum-for .sum:not([hidden])')];
  const activeSum = sumNodes[0] || null;
  const sumTerms = activeSum ? [...activeSum.querySelectorAll('[data-problem-panel="terms"][data-summary-terms]')] : [];
  const sumTermsIsLast = Boolean(activeSum && sumTerms.length === 1 && activeSum.lastElementChild === sumTerms[0]);
  const sumTermNames = sumTerms[0] ? [...sumTerms[0].querySelectorAll('dt')].map(dt => dt.textContent.trim()) : [];
  const probTermsTab = d.querySelector('#problem-workspace [role="tab"][data-tab="terms"]');
  const probTermsTabHidden = probTermsTab ? probTermsTab.hidden : null;
  const clipped = [...sec.querySelectorAll('.katex-display, .katex')].filter(k => {
    const r = k.getBoundingClientRect(); const c = sec.getBoundingClientRect();
    return r.width && (r.right > c.right + 2 || r.left < c.left - 2) && !k.closest('.math-pan');
  }).length;
  const links = [...sec.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
  return {
    id, katexErr: d.querySelectorAll('.katex-error').length,
    rawDollarInSection: (sec.innerText.match(/\$\S/g) || []).length,
    overflowX: ov, dispCount: disp.length, dispScroll, visScrollbar, inlineScroll, tableOverflow, clipped,
    order, hasRetry, hasFooterNotice, faIsLastInSolve, faBeforeVerify,
    sectionGaps: [...new Set(gaps)],
    visibleSums: sumNodes.length, sumTermsCount: sumTerms.length, sumTermsIsLast, sumTermNames,
    probTermsTabHidden,
    rightTitleDup: d.querySelectorAll('#sum-for h3').length,
    h3: (sec.querySelector('h3') || {}).textContent,
    pager: (d.getElementById('pager-status') || {}).textContent,
    links
  };
}
"""

def main():
    srv = ThreadedTCPServer(('127.0.0.1', 0), StageHandler)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    base = f'http://127.0.0.1:{port}'
    page_url = base + '/%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1116/%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1116_EM_Algorithm.html'
    out = []
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
                        pg.on('request', lambda r: external.append(r.url) if not r.url.startswith(base) and not r.url.startswith('data:') else None)
                        pg.goto(page_url)
                        pg.wait_for_timeout(800)
                        cfg = {'viewport': f'{w}x{h}', 'scheme': scheme, 'port': port, 'problems': []}
                        cfg['tocOpen'] = pg.evaluate("() => { const l = document.getElementById('panel-left'); return l ? l.getBoundingClientRect().width > 0 && getComputedStyle(l).visibility !== 'hidden' : null }")
                        # Open summary panel on 1280px+ where all three panels fit comfortably
                        if w >= 1280:
                            pg.evaluate("() => { const b = document.getElementById('toggle-right'); if (b && b.getAttribute('aria-expanded') === 'false') b.click(); }")
                            pg.wait_for_timeout(250)
                        for pid in IDS:
                            pg.goto(page_url + '#' + pid)
                            pg.wait_for_timeout(450)
                            r = pg.evaluate(PROBE, pid)
                            cfg['problems'].append(r)
                            if pid in ('p1', 'p6', 'p8'):
                                pg.screenshot(path=str(SHOTS / f'{w}x{h}-{scheme}-{pid}.png'), full_page=False)
                        cfg['console'] = cons
                        cfg['failed'] = failed
                        cfg['external'] = external
                        out.append(cfg)
                        ctx.close()
            finally:
                br.close()
    finally:
        srv.shutdown()
        srv.server_close()
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
