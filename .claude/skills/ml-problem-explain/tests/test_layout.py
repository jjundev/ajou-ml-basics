"""Behavioral browser regression using the real offline template, not CSS token assertions."""
from dataclasses import replace
from pathlib import Path
import pytest
from mpe_source import load_source
from mpe_render import build_explanation
from helpers import course_stage, fragment

ROOT=Path(__file__).resolve().parents[4]

@pytest.mark.parametrize('width', [375, 1440])
def test_summary_preserves_math_when_navigating_after_render(tmp_path, width):
    pw=pytest.importorskip('playwright.sync_api')
    pack=load_source(ROOT/'과제/과제1/과제1_Homework1.html',ROOT)
    # Plain and formula titles catch stale content when navigating in both directions.
    pack=replace(pack,problems=(pack.problems[0],pack.problems[19]))
    sums={'p1':'평문 요약','p20':r'규제 $\lambda I$ 요약'}
    artifact=build_explanation(pack,{p.id:fragment(p).replace('시작·판단·검산',sums[p.id]) for p in pack.problems},course_stage(tmp_path),ROOT)
    with pw.sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':width,'height':900},color_scheme='dark')
        page.goto(artifact.html.as_uri(),wait_until='networkidle')
        for problem_id in ['p20','p1','p20']:
            page.evaluate('(id)=>{location.hash=id}',problem_id)
            page.wait_for_function('(id)=>document.querySelector("#"+id).hidden===false',arg=problem_id)
            # The panel shows only the current summary; titles stay in the main column.
            shown=page.locator('#sum-for .sum:not([hidden])')
            assert shown.count()==1
            assert shown.locator('.katex').count()==(1 if problem_id=='p20' else 0)
            assert '요약' in shown.text_content() and '$' not in shown.text_content()
            assert page.locator(f'#{problem_id} h3 .katex').count()==(1 if problem_id=='p20' else 0)
        assert page.locator('.katex-error').count()==0
        page.evaluate('location.hash="intro"')
        page.wait_for_function('!document.querySelector("#sum-for .sum:not([hidden])")')
        browser.close()

def test_short_math_and_layer_spacing_remain_readable(tmp_path):
    pw=pytest.importorskip('playwright.sync_api')
    pack=load_source(ROOT/'과제/과제1/과제1_Homework1.html',ROOT)
    pack=replace(pack,problems=pack.problems[:1])
    p=pack.problems[0]
    body=fragment(p).replace('$A=1$', '$(A^\\top)_{ij}=A_{ji}$')
    artifact=build_explanation(pack,{'p1':body},course_stage(tmp_path),ROOT)
    with pw.sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':375,'height':812})
        page.goto(artifact.html.as_uri(),wait_until='networkidle')
        page.locator('#pager-next').click()
        page.wait_for_timeout(100)
        inline=page.locator('#p1 [data-explanation="start"] .katex').first
        assert inline.evaluate('(e)=>getComputedStyle(e).overflowX')=='visible'
        assert not inline.evaluate('(e)=>e.classList.contains("math-block")')
        for kind in ['understand','retry']:
            assert page.locator(f'#p1 [data-explanation="{kind}"]').evaluate('(e)=>parseFloat(getComputedStyle(e).marginTop)')>=24
        # The source matrix renders as a full readable block, not its own scrollbar.
        page.locator('#p1 .problem-toggle').click()
        page.wait_for_timeout(100)
        matrix=page.locator('#p1 [data-source-field="conditions"] .math-row').first
        assert matrix.count()==1
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert page.locator('.katex-error').count()==0
        browser.close()

def test_long_likelihood_overflow_is_accessible_after_layout(tmp_path):
    pw=pytest.importorskip('playwright.sync_api')
    pack=load_source(ROOT/'과제/과제1/과제1_Homework1.html',ROOT)
    p=pack.problems[14];pack=replace(pack,problems=(p,))
    body=fragment(p).replace('$A=1$',p.reference_answer)
    artifact=build_explanation(pack,{'p15':body},course_stage(tmp_path),ROOT)
    with pw.sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':375,'height':812})
        page.goto(artifact.html.as_uri(),wait_until='networkidle')
        page.locator('#pager-next').click();page.wait_for_timeout(150)
        rows=page.locator('#p15 .math-row')
        assert rows.count()>0
        for row in rows.all():
            if row.evaluate('(e)=>e.scrollWidth>e.clientWidth+3'):
                assert row.evaluate('(e)=>e.classList.contains("math-pan")&&getComputedStyle(e).scrollbarWidth==="none"')
                row.focus();row.press('ArrowRight')
                assert page.locator('#p15').is_visible()
        browser.close()
