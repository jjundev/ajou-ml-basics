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

@pytest.mark.parametrize('width', [375, 1280])
def test_math_row_and_table_spacing(tmp_path, width):
    pw = pytest.importorskip('playwright.sync_api')
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    p = pack.problems[0]
    pack = replace(pack, problems=(p,))
    body = (
        '<div class="layer eli5" data-explanation="understand"><h4>풀이 목표</h4><p>평문 목표입니다.</p></div>'
        '<div class="layer formal" data-explanation="recall"><h4>풀이 단서</h4><p>공식을 떠올려요.</p></div>'
        '<div class="layer formal" data-explanation="start"><h4>첫 단계</h4><p>값을 대입해요.</p></div>'
        '<div class="layer formal" data-explanation="solve"><h4>핵심 풀이</h4>'
        '<div data-subpart="main"><h4>(a) 계산</h4>'
        '<p class="plain-row">평문으로 쓴 문단입니다.</p>'
        '<p class="math-text-row">수식이 들어간 행 $\\frac{\\sigma_1^2}{N_k}=0.15$입니다.</p>'
        '<div class="table-wrap"><table>'
        '<thead><tr><th>성분</th><th>$\\sigma_k^2$</th></tr></thead>'
        '<tbody><tr><td>1</td><td>$0.15$</td></tr><tr><td>2</td><td>0.44</td></tr></tbody>'
        '</table></div>'
        '<p>표 다음 문단입니다.</p>'
        '</div>'
        '<div data-subpart="next"><h4>(b) 비교</h4><p>다음 소문항입니다.</p></div>'
        '<section class="final-answer"><h4>최종 답</h4><p>$0.15$</p></section>'
        '</div>'
        '<div class="layer formal" data-explanation="verify"><h4>답 확인</h4><div data-subpart="main"><p>확인됨.</p></div><div data-subpart="next"><p>확인됨.</p></div></div>'
        '<div class="layer warn" data-explanation="pitfall" data-omit-retry=""><h4>주의할 점</h4><p>주의.</p></div>'
        '<div class="sum" hidden><div class="summary-group"><h4>요약</h4><p>핵심 요약</p></div></div>'
        '<section data-problem-panel="terms" data-summary-terms=""><h4>용어</h4><dl class="terms"><dt>분산</dt><dd>퍼진 정도</dd></dl></section>'
    )
    # Use a 2-subpart problem or main subpart matching pack.problems[0]
    p = replace(p, subparts=('main', 'next'))
    pack = replace(pack, problems=(p,))
    artifact = build_explanation(pack, {p.id: body}, course_stage(tmp_path), ROOT)
    with pw.sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': width, 'height': 900})
        page.goto(artifact.html.as_uri(), wait_until='networkidle')
        page.locator('#pager-next').click()
        page.wait_for_timeout(150)
        metrics = page.evaluate('''() => {
            const plain = document.querySelector('#p1 .plain-row');
            const mathP = document.querySelector('#p1 .math-text-row');
            const wrap = document.querySelector('#p1 .table-wrap');
            const th = document.querySelector('#p1 .table-wrap thead th');
            const tdMath = document.querySelector('#p1 .table-wrap tbody tr:first-child td');
            const tdPlain = document.querySelector('#p1 .table-wrap tbody tr:last-child td');
            const sub2 = document.querySelector('#p1 [data-explanation="solve"] [data-subpart="next"]');
            const outerH4 = document.querySelector('#p1 [data-explanation="solve"] > h4');
            const subH4 = document.querySelector('#p1 [data-explanation="solve"] [data-subpart="main"] > h4');
            return {
                plainLH: parseFloat(getComputedStyle(plain).lineHeight),
                mathLH: parseFloat(getComputedStyle(mathP).lineHeight),
                wrapMT: parseFloat(getComputedStyle(wrap).marginTop),
                wrapMB: parseFloat(getComputedStyle(wrap).marginBottom),
                thPT: parseFloat(getComputedStyle(th).paddingTop),
                thPB: parseFloat(getComputedStyle(th).paddingBottom),
                tdMathPT: parseFloat(getComputedStyle(tdMath).paddingTop),
                tdPlainPT: parseFloat(getComputedStyle(tdPlain).paddingTop),
                sub2MT: parseFloat(getComputedStyle(sub2).marginTop),
                outerH4FS: parseFloat(getComputedStyle(outerH4).fontSize),
                subH4FS: parseFloat(getComputedStyle(subH4).fontSize),
                overflowX: document.documentElement.scrollWidth > window.innerWidth,
                katexErrors: document.querySelectorAll('.katex-error').length,
            };
        }''')
        assert metrics['mathLH'] > metrics['plainLH']
        assert metrics['wrapMT'] >= 24 and metrics['wrapMB'] >= 24
        assert metrics['thPT'] >= 11 and metrics['thPB'] >= 11
        assert metrics['tdMathPT'] >= 12 and metrics['tdPlainPT'] >= 11
        assert metrics['sub2MT'] >= 28
        assert metrics['subH4FS'] < metrics['outerH4FS']
        assert not metrics['overflowX']
        assert metrics['katexErrors'] == 0
        browser.close()


@pytest.mark.parametrize('width', [1280, 375])
def test_toc_checkmarks_align_in_single_column_and_track_current(tmp_path, width):
    pw = pytest.importorskip('playwright.sync_api')
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    titles = [
        'P1. 짧은 제목',
        'P2. 중간 길이의 문제 제목 확인',
        'P3. 좌측 목차 폭을 넘어서 두 줄 이상으로 줄바꿈되는 아주 긴 문제 제목 테스트',
    ]
    problems = tuple(replace(p, title=t) for p, t in zip(pack.problems[:3], titles))
    pack = replace(pack, problems=problems)
    artifact = build_explanation(
        pack,
        {p.id: fragment(p) for p in pack.problems},
        course_stage(tmp_path),
        ROOT,
    )
    with pw.sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': width, 'height': 900})
        page.goto(artifact.html.as_uri(), wait_until='networkidle')
        page.locator('#pager-next').click()
        page.locator('#p1').wait_for(state='visible')
        page.locator('#pager-next').click()
        page.locator('#p2').wait_for(state='visible')
        if width == 375:
            page.locator('#toggle-left').click()
            page.locator('#panel-left.is-open').wait_for(state='visible')
        page.wait_for_timeout(150)
        info = page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('#panel-left .toc-list a'));
            const rects = links.map((a) => {
                const mark = a.querySelector('.toc-mark');
                const r = mark ? mark.getBoundingClientRect() : null;
                return {
                    href: a.getAttribute('href'),
                    hasTitle: Boolean(a.querySelector('.toc-title')),
                    hasMark: Boolean(mark),
                    ariaCurrent: a.getAttribute('aria-current'),
                    left: r ? r.left : null,
                    right: r ? r.right : null,
                };
            });
            return {
                rects,
                katexErrors: document.querySelectorAll('.katex-error').length,
                overflowX: document.documentElement.scrollWidth > window.innerWidth + 1,
            };
        }''')
        assert len(info['rects']) == 3
        assert all(r['hasTitle'] and r['hasMark'] for r in info['rects'])
        lefts = [r['left'] for r in info['rects']]
        rights = [r['right'] for r in info['rects']]
        assert max(lefts) - min(lefts) <= 1.0
        assert max(rights) - min(rights) <= 1.0
        by_href = {r['href']: r for r in info['rects']}
        assert by_href['#p2']['ariaCurrent'] == 'true'
        assert by_href['#p1']['ariaCurrent'] == 'false'
        assert info['katexErrors'] == 0
        assert not info['overflowX']
        browser.close()
