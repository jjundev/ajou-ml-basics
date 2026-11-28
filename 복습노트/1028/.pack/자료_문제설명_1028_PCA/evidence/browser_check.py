"""실제 렌더링 및 DOM 계약 검토(1028 PCA 문제설명 stage).
<BUCKET> 디렉터리를 127.0.0.1:0 (OS-assigned port 0) 로컬 HTTP 서버로 제공하고,
1280x900, 1024x900, 375x812 x light/dark에서 KaTeX/콘솔/네트워크 오류, 가로 넘침,
final-answer 배치, retry/footer 부재, 우측 요약 용어 이동 및 문항 전환, 문제 패널 용어 탭 숨김을 확인한다.
python3 browser_check.py <bucket_dir> <stage_rel_html> <shot_dir> <out_json>
"""
import functools
import http.server
import json
import os
import socketserver
import sys
import threading
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

BUCKET = Path(sys.argv[1]).resolve()
STAGE_REL_HTML = sys.argv[2]
SHOTS = Path(sys.argv[3]).resolve()
OUT_JSON = Path(sys.argv[4]).resolve()
SHOTS.mkdir(parents=True, exist_ok=True)
IDS = ['p1', 'p2', 'p3', 'p4', 'p5']


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


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
  const clipped = [...sec.querySelectorAll('.katex-display, .katex')].filter(k => {
    const r = k.getBoundingClientRect(); const c = sec.getBoundingClientRect();
    return r.width && (r.right > c.right + 2 || r.left < c.left - 2) && !k.closest('.katex-display[style*=overflow]');
  }).length;
  const layers = [...sec.querySelectorAll(':scope > [data-explanation]')].map(e => e.getAttribute('data-explanation'));
  const solve = sec.querySelector(':scope > [data-explanation="solve"]');
  const verify = sec.querySelector(':scope > [data-explanation="verify"]');
  const fa = solve ? solve.querySelector(':scope > section.final-answer') : null;
  const faIsLastInSolve = !!(solve && fa && solve.lastElementChild === fa);
  const faBeforeVerify = !!(fa && verify && (fa.compareDocumentPosition(verify) & Node.DOCUMENT_POSITION_FOLLOWING));
  const retryCount = sec.querySelectorAll('[data-explanation="retry"]').length;
  const footerCount = d.querySelectorAll('footer').length;

  const sum = d.querySelectorAll('#sum-for .sum:not([hidden])');
  const activeSum = sum.length === 1 ? sum[0] : null;
  const sumLastChild = activeSum ? activeSum.lastElementChild : null;
  const termsInSumBottom = !!(activeSum && sumLastChild && sumLastChild.matches('[data-summary-terms], [data-problem-panel="terms"]') || (activeSum && activeSum.querySelector(':scope > [data-problem-panel="terms"], :scope > [data-summary-terms]')));
  const sumTermCount = activeSum ? activeSum.querySelectorAll('dl.terms dt').length : 0;
  const sumFirstTerm = activeSum && activeSum.querySelector('dl.terms dt') ? activeSum.querySelector('dl.terms dt').textContent.trim() : null;

  const probTermsPanel = sec.querySelector('[data-problem-panel="terms"]');
  const probTermsHidden = !probTermsPanel || probTermsPanel.hidden || getComputedStyle(probTermsPanel).display === 'none' || !!probTermsPanel.closest('[hidden]');
  const probTabs = [...sec.querySelectorAll('[role="tab"]')].map(t => ({
    text: t.textContent.trim(),
    hidden: t.hidden || getComputedStyle(t).display === 'none'
  }));
  const termsTabHidden = probTabs.every(t => t.text !== '용어' || t.hidden);

  return {
    id,
    katexErr: d.querySelectorAll('.katex-error').length,
    rawDollarInSection: (sec.innerText.match(/\$\S/g) || []).length,
    overflowX: ov,
    dispCount: disp.length,
    dispScroll,
    visScrollbar,
    inlineScroll,
    clipped,
    layers,
    faIsLastInSolve,
    faBeforeVerify,
    retryCount,
    footerCount,
    visibleSums: sum.length,
    termsInSumBottom,
    sumTermCount,
    sumFirstTerm,
    probTermsHidden,
    termsTabHidden,
    h3: (sec.querySelector('h3') || {}).textContent,
    pager: (d.getElementById('pager-status') || {}).textContent
  };
}
"""


def main():
    handler = functools.partial(QuietHandler, directory=str(BUCKET))
    srv = ThreadingServer(('127.0.0.1', 0), handler)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    base = f'http://127.0.0.1:{port}'
    encoded_path = '/'.join(quote(part) for part in Path(STAGE_REL_HTML).parts)
    page_url = f'{base}/{encoded_path}'
    out = {'port': port, 'page_url': page_url, 'runs': []}
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
                        cfg = {'viewport': f'{w}x{h}', 'scheme': scheme, 'problems': []}
                        for pid in IDS:
                            pg.goto(page_url + '#' + pid)
                            pg.wait_for_timeout(450)
                            r = pg.evaluate(PROBE, pid)
                            cfg['problems'].append(r)
                            pg.screenshot(path=str(SHOTS / f'{w}x{h}-{scheme}-{pid}.png'), full_page=False)
                        cfg['console'] = cons
                        cfg['failed'] = failed
                        cfg['external'] = external
                        out['runs'].append(cfg)
                        ctx.close()
            finally:
                br.close()
    finally:
        srv.shutdown()
        srv.server_close()

    # Check hard pass criteria
    summary_errors = []
    for run in out['runs']:
        if run['console'] or run['failed'] or run['external']:
            summary_errors.append(f"{run['viewport']} {run['scheme']}: console/failed/external non-empty")
        term_heads = [p['sumFirstTerm'] for p in run['problems']]
        if len(set(term_heads)) < 2:
            summary_errors.append(f"{run['viewport']} {run['scheme']}: terms did not switch across problems ({term_heads})")
        for p in run['problems']:
            if p['katexErr'] != 0 or p['rawDollarInSection'] != 0 or p['overflowX'] != 0 or p['clipped'] != 0:
                summary_errors.append(f"{run['viewport']} {run['scheme']} {p['id']}: render/overflow error")
            if not p['faIsLastInSolve'] or not p['faBeforeVerify']:
                summary_errors.append(f"{run['viewport']} {run['scheme']} {p['id']}: final-answer placement error")
            if p['retryCount'] != 0 or p['footerCount'] != 0:
                summary_errors.append(f"{run['viewport']} {run['scheme']} {p['id']}: retry or footer found")
            if p['visibleSums'] != 1 or not p['termsInSumBottom'] or p['sumTermCount'] == 0 or not p['probTermsHidden'] or not p['termsTabHidden']:
                summary_errors.append(f"{run['viewport']} {run['scheme']} {p['id']}: terms relocation/tab hiding error")
    out['all_passed'] = len(summary_errors) == 0
    out['summary_errors'] = summary_errors
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'port': port, 'all_passed': out['all_passed'], 'errors': summary_errors}, ensure_ascii=False))
    if not out['all_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
