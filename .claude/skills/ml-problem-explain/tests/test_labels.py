from dataclasses import replace
from pathlib import Path
from helpers import fragment
from mpe_source import load_source
from mpe_render import build_explanation
from mpe_shared import parse

ROOT = Path(__file__).resolve().parents[4]


def test_build_removes_repeated_labels_and_preserves_references(tmp_path):
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    pack = replace(pack, problems=pack.problems[:1])
    p = pack.problems[0]
    body = ('<h4>(a)</h4><p>(a) 전개해요. $A^2=1$</p>'
            '<p><strong>(a) </strong>미분해요.</p>'
            '<p>(a)에서 구한 결과예요.</p><p>(b) 다른 소문항을 참조해요.</p>')
    text = fragment(p).replace('<div data-subpart="a"><p>',
                               '<div data-subpart="a">' + body + '<p>')
    for stage in ('first', 'regenerated'):
        result = build_explanation(pack, {p.id: text}, tmp_path / stage, ROOT)
        doc = parse(result.html.read_text(encoding='utf-8'))
        blocks = list(doc.find_all(lambda n: n.attrs.get('data-subpart') == 'a'))
        for block in blocks:
            paragraphs = [n.text() for n in block.find_all(lambda n: n.tag == 'p')]
            assert '전개해요. $A^2=1$' in paragraphs
            assert '미분해요.' in paragraphs
            assert '(a)에서 구한 결과예요.' in paragraphs
            assert '(b) 다른 소문항을 참조해요.' in paragraphs
        md = result.md.read_text(encoding='utf-8')
        assert '(a) 전개해요' not in md
        assert '(a)에서 구한 결과예요.' in md
        text = (result.manifest.parent / 'fragments/p1.html').read_text(encoding='utf-8')


def test_build_keeps_labels_without_a_subpart_heading(tmp_path):
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    pack = replace(pack, problems=pack.problems[:1])
    p = pack.problems[0]
    text = fragment(p).replace('첫 식에서 계산하고', '(a) 첫 식에서 계산하고')
    result = build_explanation(pack, {p.id: text}, tmp_path / 'stage', ROOT)
    assert '(a) 첫 식에서' in result.md.read_text(encoding='utf-8')
