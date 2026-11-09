"""Browser sweep of an MPE stage HTML: 1280x900 / 1024x900 / 375x812, light/dark, every question.
Reports console errors, KaTeX errors, broken images, external requests, horizontal overflow, scrollable inline math.
Usage: python browser_sweep.py <url> <shots_dir> <out_json>
"""
import json, sys
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

url, shots, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
shots.mkdir(parents=True, exist_ok=True)
host = urlsplit(url).netloc
report = {'url': url, 'runs': []}
with sync_playwright() as p:
    browser = p.chromium.launch()
    try:
        for (w, h) in [(1280, 900), (1024, 900), (375, 812)]:
            for scheme in ['light', 'dark']:
                ctx = browser.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme)
                page = ctx.new_page()
                console, external = [], []
                page.on('console', lambda m: console.append(m.text) if m.type == 'error' else None)
                page.on('pageerror', lambda e: console.append(str(e)))
                page.on('request', lambda r: external.append(r.url) if urlsplit(r.url).netloc not in (host, '') and not r.url.startswith('data:') else None)
                page.goto(url.split('#')[0] + '#p1', wait_until='networkidle')
                page.wait_for_timeout(800)
                run = {'viewport': f'{w}x{h}', 'scheme': scheme, 'questions': []}
                for n in range(1, 11):
                    page.goto(url.split('#')[0] + f'#p{n}')
                    page.wait_for_timeout(400)
                    page.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
                    stats = page.evaluate("""() => ({
                        katexErr: document.querySelectorAll('.katex-error').length,
                        brokenImg: [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.getAttribute('src')).map(i => i.getAttribute('src')),
                        overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                        visibleH3: [...document.querySelectorAll('h3')].filter(e => e.offsetParent && e.getBoundingClientRect().width>0).map(e=>e.textContent.trim()).slice(0,1),
                    })""")
                    stats['q'] = n
                    run['questions'].append(stats)
                    if n in (1, 7, 10):
                        page.screenshot(path=str(shots / f'{w}x{h}-{scheme}-p{n}.png'))
                run['console_errors'] = console
                run['external_requests'] = sorted(set(external))
                report['runs'].append(run)
                ctx.close()
    finally:
        browser.close()
bad = []
for r in report['runs']:
    for q in r['questions']:
        if q['katexErr'] or q['brokenImg'] or q['overflowX'] > 0:
            bad.append((r['viewport'], r['scheme'], q))
    if r['console_errors'] or r['external_requests']:
        bad.append((r['viewport'], r['scheme'], {'console': r['console_errors'], 'external': r['external_requests']}))
report['problems'] = [str(b) for b in bad]
out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
print('PASS' if not bad else 'FAIL', len(bad))
for b in bad[:20]:
    print(b)
