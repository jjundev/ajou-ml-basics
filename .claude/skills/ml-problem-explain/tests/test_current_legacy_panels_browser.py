"""Execute actual older explanation pages whose title-copy implementation differs.

Keep this page list explicit: filtering on the broken JS would silently remove
coverage once the obsolete clone block is fixed.
"""
import functools
import http.server
import threading
from pathlib import Path
from urllib.parse import quote

import pytest
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[4]
AUTHORED_SUMMARY_TEXT = '(el)=>{const copy=el.cloneNode(true);copy.querySelectorAll(".math-pan-hint").forEach(hint=>hint.remove());return copy.textContent}'

LEGACY_PAGES = ['과제/과제1/과제1_문제설명_Homework1.html', '복습노트/0909/문제설명_0909_Data_Models_Learning.html', '복습노트/0914/문제설명_0914_ERM_and_MLE.html', '복습노트/0916/문제설명_0916_MAP_and_Generative_Models.html', '복습노트/0921/문제설명_0921_Bayesian_Inference_Model_Selection.html', '복습노트/0923/문제설명_0923_Linear_Regression.html', '복습노트/0928/문제설명_0928_Linear_Regression.html', '복습노트/0930/문제설명_0930_Bayesian_Linear_Regression.html', '복습노트/1007/문제설명_1007_Product_of_Gaussians.html', '복습노트/1012/문제설명_1012_Several_Mathematical_Proofs.html', '복습노트/1014/문제설명_1014_Bayesian_Posterior_Prediction.html']


@pytest.fixture(scope='module')
def current_server():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown(); thread.join(); server.server_close()


@pytest.fixture(scope='module')
def current_browser():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            yield browser
        finally:
            browser.close()


@pytest.mark.parametrize('relative_path', LEGACY_PAGES)
@pytest.mark.parametrize('width,height', [(1280, 900), (375, 812)])
@pytest.mark.parametrize('theme', ['light', 'dark'])
def test_actual_legacy_explanation_progress(current_server, current_browser, relative_path, width, height, theme):
    context = current_browser.new_context(viewport={'width': width, 'height': height}, color_scheme=theme)
    context.add_init_script(f"localStorage.setItem('od-theme', '{theme}')")
    try:
        page = context.new_page(); page.set_default_timeout(5000)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(current_server + '/' + quote(relative_path), wait_until='networkidle')
        key = page.evaluate("'od-note-read:' + document.body.dataset.range")
        ids = page.locator('main article.topic').evaluate_all('(els)=>els.map(el=>el.id)')
        assert len(ids) >= 2
        assert page.evaluate('(key)=>localStorage.getItem(key)', key) is None
        # Load plus a real next click reproduces the two broken od:screen calls.
        page.locator('#pager-next').click()
        expect(page.locator('main #' + ids[0])).to_be_visible()
        payload = page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))', key)
        assert errors == [], f'pageerrors={errors}; key={key}; payload={payload}'
        assert payload == ids[:1]
        if not page.locator('#panel-right').is_visible(): page.locator('#toggle-right').click()
        expect(page.locator('#panel-right')).to_be_in_viewport(ratio=0.95)
        assert page.locator('#sum-for.sums').count() == 1
        assert page.locator('[id="sum-for"]').count() == 1
        # Layout inserts a transient math-pan hint only when a summary is visible.
        # Compare all authored text, excluding that generated reading instruction.
        summaries = [node.evaluate(AUTHORED_SUMMARY_TEXT) for node in page.locator('#sum-for > .sum').all()]
        assert len(summaries) == len(ids)
        for index, topic in enumerate(ids):
            if index: page.evaluate('(id)=>{location.hash=id}', topic)
            expect(page.locator('main #' + topic)).to_be_visible()
            title = page.locator('main #' + topic + ' h3').text_content().strip()
            assert page.locator('#panel-right').get_by_text(title, exact=True).count() == 0
            current = page.locator('#sum-for > .sum:not([hidden])')
            expect(current).to_have_count(1)
            assert current.evaluate(AUTHORED_SUMMARY_TEXT) == summaries[index]
            assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))', key) == ids[:index+1]
        page.reload(wait_until='networkidle')
        assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))', key) == ids
        assert errors == []
        assert page.locator('.katex-error').count() == 0
    finally:
        context.close()
