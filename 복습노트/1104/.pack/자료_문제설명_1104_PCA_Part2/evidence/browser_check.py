"""Playwright verification for 1104 PCA Part2 streamlined problem-explain stage."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import threading
from urllib.parse import quote
from playwright.sync_api import sync_playwright

BUCKET = Path(sys.argv[1]).resolve()
STAGE_INFO = json.loads((BUCKET / "stage.json").read_text(encoding="utf-8"))
STAGE_REL = STAGE_INFO["stage"] + "/" + quote(STAGE_INFO["html"])
SHOTS = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
if SHOTS:
    SHOTS.mkdir(parents=True, exist_ok=True)

IDS = [f"p{i}" for i in range(1, 11)]

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
  const blocks = [...sec.querySelectorAll(':scope > [data-explanation]')];
  const blockOrder = blocks.map(b => b.getAttribute('data-explanation'));
  const gaps = [];
  for (let i = 1; i < blocks.length; i++) {
    const a = blocks[i - 1].getBoundingClientRect(), b = blocks[i].getBoundingClientRect();
    if (a.height && b.height) gaps.push(Math.round(b.top - a.bottom));
  }
  const h4gaps = blocks.map(b => {
    const h = b.querySelector(':scope > h4'); const n = h && h.nextElementSibling;
    if (!h || !n || !n.getBoundingClientRect().height) return null;
    return Math.round(n.getBoundingClientRect().top - h.getBoundingClientRect().bottom);
  }).filter(x => x !== null);
  const subs = [...sec.querySelectorAll('[data-subpart] + [data-subpart]')].map(s =>
    Math.round(s.getBoundingClientRect().top - s.previousElementSibling.getBoundingClientRect().bottom));

  const solve = sec.querySelector(':scope > [data-explanation="solve"]');
  const solveChildren = solve ? [...solve.children] : [];
  const finalAns = solve ? solve.querySelector(':scope > section.final-answer') : null;
  const finalIsLastInSolve = Boolean(finalAns && solveChildren[solveChildren.length - 1] === finalAns);
  const verify = sec.querySelector(':scope > [data-explanation="verify"]');
  const finalBeforeVerify = Boolean(solve && verify && solve.nextElementSibling === verify);

  const retryCount = sec.querySelectorAll('[data-explanation="retry"]').length;
  const footerText = (d.querySelector('footer') || {}).innerText || '';
  const hasPreservationFooter = /보존/.test(footerText);

  const visibleSums = [...d.querySelectorAll('#sum-for .sum:not([hidden])')];
  const sumEl = visibleSums[0] || null;
  const sumTerms = sumEl ? sumEl.querySelector(':scope > [data-problem-panel="terms"][data-summary-terms]') : null;
  const sumTermsIsLast = Boolean(sumEl && sumTerms && sumEl.lastElementChild === sumTerms);
  const sumTermTitles = sumTerms ? [...sumTerms.querySelectorAll('dt')].map(dt => dt.textContent.trim()) : [];

  const termsTab = d.querySelector('.problem-workspace [role="tab"][data-tab="terms"]');
  const termsTabHidden = termsTab ? termsTab.hidden : null;
  const provTab = d.querySelector('.problem-workspace [role="tab"][data-tab="provenance"]');
  const provTabHidden = provTab ? provTab.hidden : null;
  const origTab = d.querySelector('.problem-workspace [role="tab"][data-tab="original"]');
  const origTabHidden = origTab ? origTab.hidden : null;

  const secRect = sec.getBoundingClientRect();
  const tableWrapBad = [...sec.querySelectorAll('.table-wrap')].filter(tw => {
    const r = tw.getBoundingClientRect();
    return r.right > secRect.right + 2 || r.left < secRect.left - 2;
  }).length;
  const derivRows = [...sec.querySelectorAll('ol.deriv > li')];
  const derivBad = derivRows.filter(li => {
    const r = li.getBoundingClientRect();
    const isGen = li.classList.contains('deriv-gen');
    const pad = isGen ? 20 : 2;
    return li.scrollWidth > li.clientWidth + 1 || r.right > secRect.right + pad || r.left < secRect.left - pad;
  }).length;
  const derivWrappedCount = derivRows.filter(li => li.classList.contains('is-wrapped') || li.dataset.wrapped === '1' ||
    (() => {
      const eq = li.querySelector('.deriv-eq'), why = li.querySelector('.deriv-why');
      return eq && why && why.getBoundingClientRect().top >= eq.getBoundingClientRect().bottom - 2;
    })()).length;

  const clipped = [...sec.querySelectorAll('.katex-display, .katex')].filter(k => {
    if (k.closest('.table-wrap')) return false;
    const r = k.getBoundingClientRect();
    return r.width && (r.right > secRect.right + 2 || r.left < secRect.left - 2) && !k.closest('.katex-display[style*=overflow]');
  }).length;

  return {
    id,
    blockOrder,
    katexErr: d.querySelectorAll('.katex-error').length,
    rawDollarInSection: (sec.innerText.match(/\$\S/g) || []).length,
    overflowX: ov,
    dispCount: disp.length,
    dispScroll,
    visScrollbar,
    inlineScroll,
    clipped,
    tableWrapBad,
    derivRows: derivRows.length,
    derivBad,
    derivWrappedCount,
    sectionGaps: [...new Set(gaps)],
    h4gaps: [...new Set(h4gaps)],
    subpartGaps: [...new Set(subs)],
    finalIsLastInSolve,
    finalBeforeVerify,
    retryCount,
    hasPreservationFooter,
    visibleSums: visibleSums.length,
    sumTermsPresent: Boolean(sumTerms),
    sumTermsIsLast,
    sumTermTitles,
    termsTabHidden,
    provTabHidden,
    origTabHidden,
    rightTitleDup: d.querySelectorAll('#sum-for h3').length,
    h3: (sec.querySelector('h3') || {}).textContent,
    pager: (d.getElementById('pager-status') || {}).textContent,
    theme: getComputedStyle(d.body).backgroundColor,
  };
}
"""


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


handler = partial(QuietHandler, directory=str(BUCKET))
server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
BASE = f"http://127.0.0.1:{port}"
PAGE = f"{BASE}/{STAGE_REL}"

out = {"base": BASE, "page": PAGE, "configs": []}
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        try:
            for (w, h) in [(1280, 900), (1024, 900), (375, 812)]:
                for scheme in ["light", "dark"]:
                    ctx = br.new_context(viewport={"width": w, "height": h}, color_scheme=scheme)
                    pg = ctx.new_page()
                    cons, failed, external = [], [], []
                    pg.on("console", lambda m: cons.append(m.type + ": " + m.text) if m.type in ("error", "warning") else None)
                    pg.on("pageerror", lambda e: cons.append("pageerror: " + str(e)))
                    pg.on("requestfailed", lambda r: failed.append(r.url))
                    pg.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
                    pg.on("request", lambda r: external.append(r.url) if not r.url.startswith(BASE) and not r.url.startswith("data:") else None)
                    pg.goto(PAGE)
                    pg.wait_for_timeout(800)
                    cfg = {"viewport": f"{w}x{h}", "scheme": scheme, "problems": []}
                    cfg["tocOpen"] = pg.evaluate(
                        "() => { const l = document.getElementById('panel-left'); return l ? l.getBoundingClientRect().width > 0 && getComputedStyle(l).visibility !== 'hidden' : null }"
                    )
                    for pid in IDS:
                        pg.goto(PAGE + "#" + pid)
                        pg.wait_for_timeout(350)
                        r = pg.evaluate(PROBE, pid)
                        cfg["problems"].append(r)
                        if SHOTS and scheme == "light" and pid in ("p1", "p4", "p5", "p10") and w in (1280, 375):
                            pg.screenshot(path=str(SHOTS / f"{w}x{h}-{scheme}-{pid}.png"), full_page=False)
                    # Check persistence of solved button on p1 across reload (once per 1280x900 light)
                    if w == 1280 and scheme == "light":
                        pg.goto(PAGE + "#p1")
                        pg.wait_for_timeout(300)
                        solved_btn = pg.locator("#p1 .solved-btn, .solved-btn").first
                        if solved_btn.count():
                            solved_btn.click()
                            pg.wait_for_timeout(200)
                        storage_before = pg.evaluate("() => ({...localStorage})")
                        pg.reload()
                        pg.wait_for_timeout(500)
                        storage_after = pg.evaluate("() => ({...localStorage})")
                        cfg["storagePersisted"] = (storage_before == storage_after and len(storage_after) > 0)
                        # Test dock buttons on problem panel
                        dock_states = []
                        for mode in ("left", "right", "float"):
                            btn = pg.locator(f'.prob-dock button[data-dock="{mode}"]').first
                            if btn.count():
                                btn.click()
                                pg.wait_for_timeout(150)
                                dock_states.append(pg.evaluate("() => document.querySelector('.layout')?.dataset?.probDock || ''"))
                        cfg["dockStates"] = dock_states
                    cfg["console"] = cons
                    cfg["failed"] = failed
                    cfg["external"] = external
                    out["configs"].append(cfg)
                    ctx.close()
        finally:
            br.close()
finally:
    server.shutdown()
    server.server_close()

print(json.dumps(out, ensure_ascii=False, indent=1))
