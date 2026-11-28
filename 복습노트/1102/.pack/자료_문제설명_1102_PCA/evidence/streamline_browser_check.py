"""Playwright verification for streamlined 1102 PCA stage served from <BUCKET> on 127.0.0.1:0."""
import functools
import http.server
import json
import socketserver
import sys
import threading
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

bucket = Path(sys.argv[1]).resolve()
stage_info = json.loads((bucket / "stage.json").read_text(encoding="utf-8"))
stage_rel = stage_info["stage"]
html_name = stage_info["html"]
out_path = bucket / "evidence" / "browser_results.json"

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

handler = functools.partial(QuietHandler, directory=str(bucket))

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

IDS = [f"p{i}" for i in range(1, 11)]

PROBE = r"""
(id) => {
  const d = document, sec = d.getElementById(id);
  const ov = d.documentElement.scrollWidth - d.documentElement.clientWidth;
  const contentEl = d.querySelector('.content');
  const contentOv = contentEl ? (contentEl.scrollWidth - contentEl.clientWidth) : 0;
  const disp = [...sec.querySelectorAll('.katex-display')];
  const visScrollbar = disp.filter(e => e.offsetHeight - e.clientHeight > 1).length;
  const inlineScroll = [...sec.querySelectorAll('.katex')].filter(k => !k.closest('.katex-display')).filter(k => {
    const p = k.parentElement;
    const cs = getComputedStyle(p);
    return (cs.overflowX === 'auto' || cs.overflowX === 'scroll') && p.tagName !== 'P' && p.tagName !== 'DIV' && !p.classList.contains('math-row');
  }).length;
  const tableOverflows = [...sec.querySelectorAll('.table-wrap')].filter(tw => {
    const r = tw.getBoundingClientRect();
    const c = sec.getBoundingClientRect();
    return r.right > c.right + 2 || r.left < c.left - 2;
  }).length;
  const derivRows = [...sec.querySelectorAll('ol.deriv > li')];
  const derivBad = derivRows.filter(li => {
    const eqs = li.querySelectorAll(':scope > .deriv-eq');
    const whys = li.querySelectorAll(':scope > .deriv-why');
    const whyP = li.querySelector(':scope > .deriv-why > p');
    const wide = li.classList.contains('is-wide');
    const eqRect = eqs[0]?.getBoundingClientRect();
    const whyRect = whys[0]?.getBoundingClientRect();
    const overlap = eqRect && whyRect && !wide && (eqRect.right > whyRect.left + 2) && (eqRect.bottom > whyRect.top + 2 && whyRect.bottom > eqRect.top + 2);
    return eqs.length !== 1 || whys.length !== 1 || !whyP || !whyP.textContent.trim() || overlap;
  }).length;
  const layers = [...sec.querySelectorAll(':scope > [data-explanation]')].map(e => e.dataset.explanation);
  const solve = sec.querySelector(':scope > [data-explanation="solve"]');
  const solveLast = solve ? solve.lastElementChild : null;
  const finalOk = Boolean(solveLast && solveLast.matches('section.final-answer'));
  const retryCount = sec.querySelectorAll('[data-explanation="retry"]').length;
  const detailsInBody = sec.querySelectorAll(':scope > [data-explanation] details').length;
  const footer = d.querySelector('footer');
  const footerText = footer ? footer.textContent.trim() : '';

  const visibleSums = [...d.querySelectorAll('#sum-for .sum:not([hidden])')];
  const sum = visibleSums[0] || null;
  const sumTerms = sum ? sum.querySelectorAll('[data-summary-terms]') : [];
  const sumTermCount = sum ? sum.querySelectorAll('[data-summary-terms] dt').length : 0;
  const sumLastChildIsTerms = Boolean(sum && sum.lastElementChild && sum.lastElementChild.hasAttribute('data-summary-terms'));
  const sumFirstTerm = sum ? (sum.querySelector('[data-summary-terms] dt')?.textContent || '') : '';
  const probTermsTab = d.querySelector('#panel-prob [data-tab="terms"]');
  const probTermsHidden = probTermsTab ? (probTermsTab.hidden || getComputedStyle(probTermsTab).display === 'none') : true;
  const rightTitleDup = d.querySelectorAll('#sum-for h3').length;

  return {
    id,
    katexErr: d.querySelectorAll('.katex-error').length,
    rawDollar: (sec.innerText.match(/\$\S/g) || []).length,
    overflowX: ov,
    contentOv,
    dispCount: disp.length,
    visScrollbar,
    inlineScroll,
    tableOverflows,
    derivRows: derivRows.length,
    derivBad,
    layers,
    finalOk,
    retryCount,
    detailsInBody,
    footerText,
    visibleSums: visibleSums.length,
    sumTermsBlocks: sumTerms.length,
    sumTermCount,
    sumLastChildIsTerms,
    sumFirstTerm,
    probTermsHidden,
    rightTitleDup,
    h3: (sec.querySelector('h3') || {}).textContent
  };
}
"""

results = []
with ReusableTCPServer(("127.0.0.1", 0), handler) as httpd:
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"
    page_url = f"{base}/{stage_rel}/{quote(html_name)}"
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            try:
                for w, h in [(1280, 900), (1024, 900), (375, 812)]:
                    for scheme in ["light", "dark"]:
                        ctx = browser.new_context(viewport={"width": w, "height": h}, color_scheme=scheme)
                        pg = ctx.new_page()
                        cons, failed, external = [], [], []
                        pg.on("console", lambda m: cons.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
                        pg.on("pageerror", lambda e: cons.append(f"pageerror: {e}"))
                        pg.on("requestfailed", lambda r: failed.append(r.url))
                        pg.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
                        pg.on("request", lambda r: external.append(r.url) if not r.url.startswith(base) and not r.url.startswith("data:") else None)

                        pg.goto(page_url)
                        pg.wait_for_timeout(800)
                        cfg = {"viewport": f"{w}x{h}", "scheme": scheme, "problems": []}
                        for pid in IDS:
                            pg.goto(f"{page_url}#{pid}")
                            pg.wait_for_timeout(350)
                            cfg["problems"].append(pg.evaluate(PROBE, pid))
                        cfg["readStorage"] = pg.evaluate("() => localStorage.getItem('od-note-read:ml-problem-explain-review-1102-PCA')")
                        pg.goto(f"{page_url}#p1")
                        pg.wait_for_timeout(200)
                        pg.click("#pager-next")
                        pg.wait_for_timeout(200)
                        cfg["afterNextHash"] = pg.evaluate("() => location.hash")
                        pg.click("#pager-prev")
                        pg.wait_for_timeout(200)
                        cfg["afterPrevHash"] = pg.evaluate("() => location.hash")
                        cfg["console"] = cons
                        cfg["failed"] = failed
                        cfg["external"] = external
                        results.append(cfg)
                        ctx.close()
            finally:
                browser.close()
    finally:
        httpd.shutdown()

out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Summarize validation
issues = []
for cfg in results:
    tag = f"{cfg['viewport']}-{cfg['scheme']}"
    if cfg["console"] or cfg["failed"] or cfg["external"]:
        issues.append(f"{tag}: console={cfg['console']} failed={cfg['failed']} external={cfg['external']}")
    if cfg["afterNextHash"] != "#p2" or cfg["afterPrevHash"] != "#p1":
        issues.append(f"{tag}: pager failed: next={cfg['afterNextHash']} prev={cfg['afterPrevHash']}")
    if not cfg["readStorage"] or json.loads(cfg["readStorage"]) != IDS:
        issues.append(f"{tag}: readStorage mismatch: {cfg['readStorage']}")
    first_terms = [p["sumFirstTerm"] for p in cfg["problems"]]
    if len(set(first_terms)) < 2:
        issues.append(f"{tag}: terms did not switch across problems: {first_terms}")
    for p in cfg["problems"]:
        if p["katexErr"] or p["rawDollar"] or p["overflowX"] > 0 or p["contentOv"] > 0 or p["visScrollbar"] or p["inlineScroll"] or p["tableOverflows"] or p["derivBad"]:
            issues.append(f"{tag} {p['id']}: layout/math issue {p}")
        if p["layers"] != ["understand", "recall", "start", "solve", "verify", "pitfall"] or not p["finalOk"] or p["retryCount"] or p["detailsInBody"]:
            issues.append(f"{tag} {p['id']}: structure issue {p}")
        if p["visibleSums"] != 1 or p["sumTermsBlocks"] != 1 or p["sumTermCount"] == 0 or not p["sumLastChildIsTerms"] or not p["probTermsHidden"] or p["rightTitleDup"]:
            issues.append(f"{tag} {p['id']}: panel/terms issue {p}")

print(json.dumps({"configs": len(results), "issues": issues}, ensure_ascii=False, indent=2))
sys.exit(1 if issues else 0)
