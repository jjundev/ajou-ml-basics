"""Generated panels keep content, navigation and exact progress payloads."""
import functools
import http.server
import json
import re
import shutil
import threading
import pytest
from playwright.sync_api import sync_playwright, expect
from _util import MINI_RUN, REPO
import assemble


@pytest.mark.parametrize('width,height', [(1280, 900), (375, 812)])
@pytest.mark.parametrize('theme', ['light', 'dark'])
def test_note_and_review_panel_copy(tmp_path, width, height, theme):
    run = tmp_path / 'run'
    shutil.copytree(MINI_RUN, run)
    section = run / 'sections/s1.html'
    summaries = iter(['첫 토픽 요약', '둘째 토픽 요약'])
    section.write_text(re.sub(r'<div class="sum" hidden>.*?</article>',
        lambda m: '<div class="sum" hidden><p>' + next(summaries) + '</p></div></article>',
        section.read_text(encoding='utf-8'), flags=re.S), encoding='utf-8')
    # A second distinct card is temporary; real fixture learning data stays intact.
    manifest = json.loads((run / 'manifest.json').read_text(encoding='utf-8'))
    manifest['problems'].append({**manifest['problems'][0], 'id': 'p2'})
    (run / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')
    card = (run / 'cards/p1.html').read_text(encoding='utf-8')
    (run / 'cards/p2.html').write_text(card.replace('id="p1"', 'id="p2"').replace('P1. 두 수의 평균', 'P2. 다른 평균'), encoding='utf-8')
    note, review = assemble.assemble(run, tmp_path)
    # Local bundled math resources avoid relying on CDN availability.
    vendor = REPO / 'assets/vendor'
    shutil.copytree(vendor, tmp_path / 'vendor')
    for path in (note, review):
        text = path.read_text(encoding='utf-8')
        for prefix, local in [('https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/', 'vendor/pretendard/'),
                              ('https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/', 'vendor/katex/')]:
            text = text.replace(prefix, local)
        path.write_text(text, encoding='utf-8')
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(tmp_path)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            try:
                context = browser.new_context(viewport={'width': width, 'height': height}, color_scheme=theme)
                context.add_init_script(f"localStorage.setItem('od-theme', {json.dumps(theme)})")
                page = context.new_page(); page_errors = []
                page.on('pageerror', lambda e: page_errors.append(str(e)))
                for path in (note, review):
                    page.goto(f'http://127.0.0.1:{server.server_port}/{path.name}', wait_until='networkidle')
                    if not page.locator('#panel-right').is_visible(): page.locator('#toggle-right').click()
                    expect(page.locator('#panel-right')).to_be_in_viewport(ratio=0.95)
                    expect(page.locator('#panel-right')).to_be_visible()
                    expect(page.locator('#panel-right .panel-empty:visible')).to_have_count(1)
                    ids = ['s1-mean', 's1-var'] if path == note else ['p1', 'p2']
                    for index, topic in enumerate(ids):
                        page.evaluate('(id)=>{location.hash=id}', topic)
                        expect(page.locator(f'main #{topic}')).to_be_visible()
                        current_title = page.locator(f'main #{topic} h3').inner_text()
                        assert page.locator('main h3', has_text=current_title).is_visible()
                        assert page.locator('#panel-right').get_by_text(current_title, exact=True).count() == 0
                        if path == note:
                            assert page.locator('#sum-for.sums').count() == 1
                            assert page.locator('[id="sum-for"]').count() == 1
                            assert page.locator('#panel-right .sum:not([hidden])').count() == 1
                            assert page.locator('#panel-right .sum:not([hidden])').inner_text() == ['첫 토픽 요약', '둘째 토픽 요약'][index]
                            assert page.evaluate("JSON.parse(localStorage.getItem('od-note-read:0101-0102'))") == ids[:index+1]
                        else:
                            aid = page.locator('#panel-right .aid:not([hidden])')
                            expect(aid).to_have_count(1)
                            aid.locator('details.hint summary').click()
                            expect(aid.locator('details.hint')).to_contain_text('더해서 개수로 나눈다.')
                            aid.locator('details.solution summary').click()
                            expect(aid.locator('.answer')).to_be_visible()
                            page.locator('#solved-btn').click()
                            expect(page.locator('#solved-btn')).to_have_attribute('aria-pressed', 'true')
                            assert page.evaluate("JSON.parse(localStorage.getItem('od-review-solved:0101-0102'))") == ids[:index+1]
                    page.reload(wait_until='networkidle')
                    assert page.evaluate("JSON.parse(localStorage.getItem('od-note-read:0101-0102'))") == ['s1-mean', 's1-var']
                    if path == review:
                        expect(page.locator('#solved-btn')).to_have_attribute('aria-pressed', 'true')
                        assert page.evaluate("JSON.parse(localStorage.getItem('od-review-solved:0101-0102'))") == ['p1', 'p2']
                    assert page_errors == []
                context.close()
            finally: browser.close()
    finally:
        server.shutdown(); thread.join(); server.server_close()
