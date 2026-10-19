"""Catch stale per-question metadata and loss during mobile/print reparenting."""
from dataclasses import replace
from pathlib import Path
import pytest
from helpers import fragment
from mpe_contract import validate_fragment
from mpe_render import build_explanation, check_artifacts
from mpe_source import load_source

ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture
def panel_stage(tmp_path):
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    p1, p2 = pack.problems[:2]
    p2 = replace(p2, original_html='')
    pack = replace(pack, profile='review', problems=(p1, p2))
    bodies = {
        p1.id: fragment(p1) + '<section data-problem-panel="provenance"><h4>출제 근거</h4><p>첫 문항의 근거</p></section>'
               '<section data-problem-panel="terms"><h4>용어</h4><dl class="terms"><dt>선형독립</dt><dd>$V\\alpha=0$의 해가 $\\alpha=0$뿐인 성질.</dd></dl></section>',
        p2.id: fragment(p2) + '<section data-problem-panel="provenance"><h4>출제 근거</h4><p>둘째 문항의 근거</p></section>',
    }
    art = build_explanation(pack, bodies, tmp_path / 'stage', ROOT)
    assert check_artifacts(pack, art) == []
    assert '선형독립' in art.md.read_text()
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
        assert '등록된 용어가 없어요' in page.locator('#tabpanel-terms').inner_text()
        assert '선형독립' not in page.locator('#tabpanel-terms').inner_text()
        page.locator('#tab-provenance').click()
        assert '둘째 문항의 근거' in page.locator('#tabpanel-provenance').inner_text()
        page.locator('#pager-prev').click()
        assert '첫 문항의 근거' in page.locator('#tabpanel-provenance').inner_text()
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
    body = fragment(p) + r'<section data-problem-panel="terms"><p>$$p(y\mid\theta,X)=\prod_{n=1}^{N}\frac{1}{\sqrt{2\pi\sigma^2}}\exp\left(-\frac{(y_n-\phi(x_n)^\top\theta)^2}{2\sigma^2}\right)$$</p></section>'
    art = build_explanation(pack, {p.id: body}, tmp_path/'stage', ROOT)
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
