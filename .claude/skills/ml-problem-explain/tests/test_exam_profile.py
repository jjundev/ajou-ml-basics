"""Actual-exam card profile: explicit HTML path only, outputs beside the HTML."""
from pathlib import Path
from mpe_source import load_source, resolve_sources
from mpe_types import SourcePack
from mpe_render import names, md_name

CARD = '''<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><title>머신러닝기초 중간고사 1021</title></head><body><main>
<h1>머신러닝기초 중간고사 1021</h1><section id="exam">
{cards}
</section></main></body></html>'''

def card(n):
    return (f'<article class="card" id="p{n}" data-source="Midterm 1021 Q{n}"><h3>Q{n}. 문항</h3>'
            '<div class="problem"><div class="conditions">$a=1$이에요.</div>'
            '<div class="ask">구해 보세요.<ol><li>(a) $a$</li><li>(b) $2a$</li></ol></div></div>'
            '<details class="original"><summary>시험 원문 보기</summary>"(a) Find a. (b) Find 2a."</details>'
            '<details class="hint" data-label="대입"><summary>힌트 보기</summary>대입해요.</details>'
            '<details class="solution"><summary>풀이 보기</summary><ol class="steps"><li>(a) $a=1$</li><li>(b) $2a=2$</li></ol>'
            '<p class="answer">정답: (a) $1$, (b) $2$</p></details></article>')

def make(tmp_path):
    path = tmp_path / '시험결과/중간고사/중간고사_1021_Midterm.html'
    path.parent.mkdir(parents=True)
    path.write_text(CARD.format(cards=card(1) + card(2)), encoding='utf-8')
    return path

def test_resolve_exam_html_path(tmp_path):
    path = make(tmp_path)
    assert resolve_sources(tmp_path, str(path)) == (path.resolve(),)

def test_load_source_exam_profile(tmp_path):
    pack = load_source(make(tmp_path), tmp_path)
    assert (pack.profile, pack.range, pack.slug) == ('midterm', '1021', 'Midterm')
    assert [p.id for p in pack.problems] == ['p1', 'p2']
    assert pack.problems[0].subparts == ('a', 'b')

def test_exam_output_names():
    pack = SourcePack('midterm', '1021', 'Midterm', Path('중간고사_1021_Midterm.html'), '0' * 64, ())
    assert names(pack) == ('중간고사_1021_문제설명_Midterm', 'figures_문제설명_exam1021_Midterm', '자료_문제설명_exam1021_Midterm')
    assert md_name(pack) == '중간고사_1021_문제설명_Midterm.md'

def test_all_excludes_exam(tmp_path):
    make(tmp_path)
    review = tmp_path / '복습노트/1007/복습문제_1007_A.html'
    review.parent.mkdir(parents=True)
    review.touch()
    assert resolve_sources(tmp_path, 'all') == (review,)

def test_mock_exam_pack_keeps_review_style_outputs():
    """ml-midterm's 예상문제 adapter builds SourcePack('exam', ...); its paths and title must not change."""
    from mpe_render import names, md_name
    pack = SourcePack('exam', '0909-1019', 'Midterm_Practice_01', Path('cards.html'), '0' * 64, ())
    assert names(pack) == ('문제설명_0909-1019_Midterm_Practice_01',
                           '.pack/figures_문제설명_0909-1019_Midterm_Practice_01',
                           '.pack/자료_문제설명_0909-1019_Midterm_Practice_01')
    assert md_name(pack) == '.pack/문제설명_0909-1019_Midterm_Practice_01.md'
