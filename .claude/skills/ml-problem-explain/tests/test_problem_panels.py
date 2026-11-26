"""Catch stale per-question metadata and loss during mobile/print reparenting."""
from dataclasses import replace
from pathlib import Path
import pytest
from helpers import TERMS, course_stage, fragment, local_server
from mpe_contract import validate_fragment
from mpe_render import build_explanation, check_artifacts
from mpe_source import load_source

ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture
def panel_stage(tmp_path):
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    p1, p2 = pack.problems[:2]
    p1 = replace(p1, title=r'행렬 $A^\top A$')
    p2 = replace(p2, original_html='')
    pack = replace(pack, profile='review', problems=(p1, p2))
    bodies = {
        p1.id: fragment(p1).replace('시작·판단·검산', '첫 문제 판단 요약').replace(TERMS, '') + '<section data-problem-panel="provenance"><h4>출제 근거</h4><p>첫 문항의 근거</p></section>'
               '<section data-problem-panel="terms"><h4>용어</h4><dl class="terms"><dt>선형독립</dt><dd>$V\\alpha=0$의 해가 $\\alpha=0$뿐인 성질. $$p(y\\mid\\theta,X)=\\prod_{n=1}^{N}\\frac{1}{\\sqrt{2\\pi\\sigma^2}}\\exp\\left(-\\frac{(y_n-\\phi(x_n)^\\top\\theta)^2}{2\\sigma^2}\\right)$$</dd></dl></section>',
        p2.id: fragment(p2).replace('시작·판단·검산', '둘째 문제 판단 요약'),
    }
    art = build_explanation(pack, bodies, course_stage(tmp_path), ROOT)
    assert check_artifacts(pack, art) == []
    assert '선형독립' in art.md.read_text(encoding='utf-8')
    return art


@pytest.mark.parametrize('width', [375, 1024, 1280])
def test_current_question_tabs_survive_mobile_navigation_and_print(panel_stage, width):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': 900})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(panel_stage.html.as_uri(), wait_until='networkidle')
        page.evaluate('location.hash="p1"')
        page.wait_for_function('!document.querySelector("#p1").hidden')
        if width < 1024:
            page.locator('#p1 .problem-toggle').click()
        assert page.locator('#tab-provenance').count() == 1
        page.locator('#tab-provenance').click()
        assert page.locator('#tabpanel-provenance').inner_text().strip().endswith('첫 문항의 근거')
        assert page.locator('#tabpanel-provenance').is_visible()
        assert page.locator('#tabpanel-problem').is_hidden()
        page.locator('#tab-provenance').press('ArrowRight')
        assert page.locator('#tab-terms').get_attribute('aria-selected') == 'true'
        assert page.locator('#tabpanel-terms .katex').count() > 0
        page.locator('#pager-next').click()
        if width < 1024:
            page.locator('#p2 .problem-toggle').click()
        assert page.locator('#tab-original').is_hidden()
        assert page.locator('#tab-terms').get_attribute('aria-selected') == 'true'
        assert '선형독립' not in page.locator('#tabpanel-terms').inner_text()
        # 출제 근거가 없는 문항은 탭을 숨기고, 그 탭을 고른 상태면 문제 탭을 보인다(선호는 유지)
        assert page.locator('#tab-provenance').is_hidden()
        page.locator('#pager-prev').click()
        page.locator('#tab-provenance').click()
        assert '첫 문항의 근거' in page.locator('#tabpanel-provenance').inner_text()
        page.locator('#pager-next').click()
        assert page.locator('#tab-provenance').is_hidden()
        assert page.locator('#tab-problem').get_attribute('aria-selected') == 'true'
        page.locator('#pager-prev').click()
        assert page.locator('#tab-provenance').get_attribute('aria-selected') == 'true'
        page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
        assert page.locator('#p1 > [data-problem-for="p1"]').count() == 1
        assert page.locator('#p2 > [data-problem-for="p2"]').count() == 1
        assert page.locator('#p1 [data-original-problem="p1"]').is_visible()
        assert page.locator('#p1 > [data-problem-panel="terms"]').is_visible()
        page.evaluate('window.dispatchEvent(new Event("afterprint"))')
        assert page.locator('#tabpanel-provenance').is_visible()
        page.locator('#tab-problem').click()
        assert page.locator('[data-problem-for="p1"]').is_visible()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert page.locator('.katex-error').count() == 0
        assert errors == []
        browser.close()


def test_duplicate_or_unknown_panel_metadata_is_rejected():
    from helpers import problem
    body = fragment()
    duplicate = '<section data-problem-panel="terms"><p>용어</p></section>' * 2
    assert validate_fragment(problem(), body + duplicate)
    assert validate_fragment(problem(), body + '<section data-problem-panel="typo"><p>잘못된 패널</p></section>')


def test_long_panel_formula_receives_accessible_math_layout(tmp_path):
    from playwright.sync_api import sync_playwright
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    p = pack.problems[0]
    pack = replace(pack, problems=(p,))
    body = fragment(p).replace(TERMS, '') + r'<section data-problem-panel="terms"><p>$$p(y\mid\theta,X)=\prod_{n=1}^{N}\frac{1}{\sqrt{2\pi\sigma^2}}\exp\left(-\frac{(y_n-\phi(x_n)^\top\theta)^2}{2\sigma^2}\right)$$</p></section>'
    art = build_explanation(pack, {p.id: body}, course_stage(tmp_path), ROOT)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1024, 'height': 900})
        page.goto(art.html.as_uri()+'#p1', wait_until='networkidle')
        page.locator('#tab-terms').click()
        page.wait_for_timeout(100)
        assert page.locator('#tabpanel-terms .math-row').count() > 0
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        browser.close()


def test_focused_mobile_tab_survives_moving_to_desktop_panel(panel_stage):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto(panel_stage.html.as_uri()+'#p1', wait_until='networkidle')
        page.locator('#p1 .problem-toggle').click()
        page.locator('#tab-terms').click()
        assert page.locator('#tab-terms').evaluate('(e)=>document.activeElement===e')
        page.set_viewport_size({'width': 1024, 'height': 900})
        page.wait_for_function('document.querySelector("#panel-prob #problem-workspace")!==null')
        assert page.locator('#tab-terms').evaluate('(e)=>document.activeElement===e')
        page.locator('#tab-terms').press('ArrowLeft')
        assert page.locator('#tab-provenance').get_attribute('aria-selected') == 'true'
        browser.close()


@pytest.mark.parametrize('width,height', [(1280, 900), (375, 812)])
@pytest.mark.parametrize('theme', ['light', 'dark'])
def test_summary_title_removal_keeps_question_tabs(panel_stage, width, height, theme):
    import functools, http.server, threading
    from playwright.sync_api import sync_playwright, expect
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    server = local_server(functools.partial(Quiet, directory=str(panel_stage.html.parents[2])))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            try:
                context = browser.new_context(viewport={'width': width, 'height': height}, color_scheme=theme)
                context.add_init_script(f"localStorage.setItem('od-theme', '{theme}')")
                page = context.new_page(); page.set_default_timeout(5000); page_errors = []
                page.on('pageerror', lambda e: page_errors.append(str(e)))
                page.goto(f'http://127.0.0.1:{server.server_port}/{panel_stage.html.relative_to(panel_stage.html.parents[2]).as_posix()}', wait_until='networkidle')
                if not page.locator('#panel-right').is_visible(): page.locator('#toggle-right').click()
                expect(page.locator('#panel-right')).to_be_in_viewport(ratio=0.95)
                expect(page.locator('#sum-empty')).to_be_visible()
                if width < 1024:
                    page.locator('#panel-right [data-panel-close]').click()
                    expect(page.locator('#panel-right')).to_be_hidden()
                expected_summaries = ['첫 문제 판단 요약', '둘째 문제 판단 요약']
                key = page.evaluate("'od-note-read:' + document.body.dataset.range")
                for index, pid in enumerate(['p1', 'p2']):
                    page.locator('#pager-next').click()
                    expect(page.locator(f'main #{pid}')).to_be_visible()
                    if not page.locator('#panel-right').is_visible(): page.locator('#toggle-right').click()
                    expect(page.locator('#panel-right')).to_be_in_viewport(ratio=0.95)
                    current_title = page.locator(f'main #{pid} h3').text_content().strip()
                    assert page.locator('main h3', has_text=current_title).is_visible()
                    assert page.locator('#panel-right').get_by_text(current_title, exact=True).count() == 0
                    assert page.locator('#sum-for.sums').count() == 1
                    assert page.locator('[id="sum-for"]').count() == 1
                    assert page.locator('#panel-right .sum:not([hidden])').count() == 1
                    assert page.locator('#panel-right .sum:not([hidden])').inner_text() == expected_summaries[index]
                    assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))', key) == ['p1', 'p2'][:index+1]
                    if width < 1024:
                        page.locator('#panel-right [data-panel-close]').click()
                        expect(page.locator('#panel-right')).to_be_hidden()
                        page.locator(f'#{pid} .problem-toggle').click()
                    page.locator('#tab-problem').click()
                    expect(page.locator(f'[data-problem-for="{pid}"]')).to_be_visible()
                    if pid == 'p1':
                        page.locator('#tab-original').click()
                        expect(page.locator('#tabpanel-original')).to_be_visible()
                        expect(page.locator('#tabpanel-original')).not_to_be_empty()
                    else: expect(page.locator('#tab-original')).to_be_hidden()
                page.locator('#pager-prev').click()
                expect(page.locator('#p1')).to_be_visible()
                if not page.locator('#panel-right').is_visible(): page.locator('#toggle-right').click()
                expect(page.locator('#panel-right')).to_be_in_viewport(ratio=0.95)
                assert page.locator('#panel-right .sum:not([hidden])').inner_text() == expected_summaries[0]
                assert page.locator('main h3 .katex').count() > 0
                if width < 1024:
                    page.locator('#panel-right [data-panel-close]').click()
                    expect(page.locator('#panel-right')).to_be_hidden()
                page.locator('#tab-terms').click()
                expect(page.locator('#tabpanel-terms .math-row')).not_to_have_count(0)
                assert page.locator('.katex-error').count() == 0
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                page.reload(wait_until='networkidle')
                assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))', key) == ['p1', 'p2']
                assert page_errors == []
                context.close()
            finally: browser.close()
    finally:
        server.shutdown(); thread.join(); server.server_close()
