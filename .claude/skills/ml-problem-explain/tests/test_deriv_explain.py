from dataclasses import replace
from pathlib import Path
import pytest
from helpers import fragment, problem
from mpe_contract import validate_fragment
from mpe_render import build_explanation, vendor_relpath
from mpe_source import load_source

ROOT = Path(__file__).resolve().parents[4]

VALID_DERIV_SOLVE = (
    '<div class="layer formal" data-explanation="solve">'
    '<h4>왜 이렇게 푸는지 함께 따라가요</h4>'
    '<div data-subpart="a"><h4>(a)</h4>'
    '<p>결론: $A=1$이에요.</p>'
    '<div class="deriv-body"><ol class="deriv">'
    '<li><div class="deriv-eq">$$A = 1$$</div>'
    '<div class="deriv-why"><p>주어진 조건을 그대로 써요.</p></div></li>'
    '</ol></div></div>'
    '<div data-subpart="b"><h4>(b)</h4><p>답은 $2$예요.</p></div>'
    '</div>'
)


def _swap_solve(base: str, new_solve: str) -> str:
    from mpe_shared import outer, parse
    node = next(parse(base).find_all(lambda n: n.attrs.get('data-explanation') == 'solve'))
    return base.replace(outer(node), new_solve)


def test_valid_deriv_and_table_fragment_accepted():
    base = fragment()
    with_deriv = _swap_solve(base, VALID_DERIV_SOLVE)
    assert validate_fragment(problem(), with_deriv) == []
    with_table = _swap_solve(
        base,
        '<div class="layer formal" data-explanation="solve"><h4>풀이</h4>'
        '<div data-subpart="a"><h4>(a)</h4>'
        '<div class="table-wrap"><table><thead><tr><th>x</th><th>값</th></tr></thead>'
        '<tbody><tr><td>1</td><td>1</td></tr></tbody></table></div></div>'
        '<div data-subpart="b"><h4>(b)</h4><p>2</p></div></div>',
    )
    assert validate_fragment(problem(), with_table) == []


def test_deriv_row_requires_one_formula_visible_note_and_forbids_details():
    base = fragment()
    bad_eq = VALID_DERIV_SOLVE.replace('$$A = 1$$', '$$A = 1$$ $$B = 2$$')
    assert any('수식' in e for e in validate_fragment(problem(), _swap_solve(base, bad_eq)))
    bad_why = VALID_DERIV_SOLVE.replace('<p>주어진 조건을 그대로 써요.</p>', '<p>   </p>')
    assert any('주석' in e for e in validate_fragment(problem(), _swap_solve(base, bad_why)))
    bad_details = VALID_DERIV_SOLVE.replace(
        '</div></li>',
        '<details><summary>자세히</summary><p>숨김</p></details></div></li>',
    )
    assert any('details' in e for e in validate_fragment(problem(), _swap_solve(base, bad_details)))


def test_build_explanation_converts_deriv_to_markdown(tmp_path):
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    p = pack.problems[0]
    pack = replace(pack, problems=(p,))
    frag = _swap_solve(
        fragment(p),
        VALID_DERIV_SOLVE.replace('<div data-subpart="b"><h4>(b)</h4><p>답은 $2$예요.</p></div>',
                                  '<div data-subpart="b"><h4>(b)</h4><p>2</p></div>'
                                  '<div data-subpart="c"><h4>(c)</h4><p>3</p></div>'),
    )
    artifacts = build_explanation(pack, {p.id: frag}, tmp_path / 'stage', ROOT)
    md = artifacts.md.read_text(encoding='utf-8')
    assert 'A = 1' in md
    assert '↳ 주어진 조건을 그대로 써요.' in md


def test_deriv_fit_reflows_hidden_topic_without_horizontal_overflow(tmp_path):
    pw = pytest.importorskip('playwright.sync_api')
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    p1, p2 = pack.problems[0], pack.problems[1]
    pack = replace(pack, problems=(p1, p2))
    wide_eq = r'$$' + ' + '.join(f'x_{{{i}}}' for i in range(1, 20)) + r' = 0$$'
    frag2 = _swap_solve(
        fragment(p2),
        '<div class="layer formal" data-explanation="solve"><h4>풀이</h4>'
        '<div data-subpart="a"><h4>(a)</h4>'
        '<div class="deriv-body"><ol class="deriv">'
        f'<li><div class="deriv-eq">{wide_eq}</div>'
        '<div class="deriv-why"><p>넓은 식은 주석이 아래로 내려가요.</p></div></li>'
        '</ol></div></div>'
        + ''.join(f'<div data-subpart="{s}"><h4>({s})</h4><p>1</p></div>' for s in p2.subparts if s != 'a')
        + '</div>',
    )
    stage_dir = tmp_path / 'work' / 'stage'
    vendor_target = (stage_dir / vendor_relpath(pack, ROOT)).resolve()
    vendor_target.parent.mkdir(parents=True, exist_ok=True)
    try:
        vendor_target.symlink_to(ROOT / 'assets' / 'vendor', target_is_directory=True)
    except Exception:
        import shutil
        shutil.copytree(ROOT / 'assets' / 'vendor', vendor_target, dirs_exist_ok=True)

    artifacts = build_explanation(pack, {p1.id: fragment(p1), p2.id: frag2}, stage_dir, ROOT)
    with pw.sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        # 1) Mobile check (375x812)
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto(artifacts.html.as_uri(), wait_until='networkidle')
        page.evaluate('location.hash="p2"')
        page.wait_for_function('document.querySelector("#p2").hidden===false')
        page.wait_for_timeout(150)
        assert page.locator('#p2 .katex-display').count() >= 1
        assert page.locator('#p2 ol.deriv > li').first.evaluate('el => getComputedStyle(el).gridTemplateColumns.split(" ").length') == 1
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert page.locator('.katex-error').count() == 0
        page.close()

        # 2) Desktop check (1280x900) - wide formula in hidden topic #p2 reflows with is-wide
        page_desktop = browser.new_page(viewport={'width': 1280, 'height': 900})
        page_desktop.goto(artifacts.html.as_uri(), wait_until='networkidle')
        page_desktop.evaluate('location.hash="p2"')
        page_desktop.wait_for_function('document.querySelector("#p2").hidden===false')
        page_desktop.wait_for_timeout(150)
        assert page_desktop.locator('#p2 .katex-display').count() >= 1
        assert page_desktop.locator('#p2 ol.deriv > li').first.evaluate('el => el.classList.contains("is-wide")')
        assert page_desktop.locator('#p2 ol.deriv > li').first.evaluate('el => getComputedStyle(el).gridTemplateColumns.split(" ").length') == 1
        page_desktop.close()

        browser.close()
