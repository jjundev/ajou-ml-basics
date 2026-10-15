from mpe_review_policy import POLICY_VERSION
from copy import deepcopy
import pytest
from helpers import problem, fragment, pack
from mpe_contract import validate_fragment, validate_reviews, payload_hash

RECALL = ('<div class="layer formal" data-explanation="recall">'
          '<h4>이 문제를 봤을 때 떠올릴 개념과 공식</h4>'
          '<p>제곱을 구하라는 단서에서 같은 수의 곱을 떠올려요. '
          '$A^2=A\\cdot A$이며 A는 주어진 스칼라예요.</p></div>')

def with_recall():
    text = fragment()
    if 'data-explanation="recall"' not in text:
        text = text.replace('<div class="layer formal" data-explanation="start">',
                            RECALL + '<div class="layer formal" data-explanation="start">')
    return text

def test_recall_required_and_legacy_fragment_refused():
    from mpe_shared import parse, outer
    text = with_recall()
    assert validate_fragment(problem(), text) == []
    node = next(parse(text).find_all(lambda n: n.attrs.get('data-explanation') == 'recall'))
    assert validate_fragment(problem(), text.replace(outer(node), ''))

def test_recall_duplicate_empty_and_wrong_order_refused():
    from mpe_shared import parse, outer
    text = with_recall()
    node = next(parse(text).find_all(lambda n: n.attrs.get('data-explanation') == 'recall'))
    block = outer(node)
    assert validate_fragment(problem(), text + block)
    empty = '<div class="layer formal" data-explanation="recall"><h4>개념</h4></div>'
    assert any('recall' in e for e in validate_fragment(problem(), text.replace(block, empty)))
    wrong = text.replace(block, '').replace('<div class="layer formal" data-explanation="solve">',
                                           block + '<div class="layer formal" data-explanation="solve">')
    assert any('순서' in e for e in validate_fragment(problem(), wrong))

def test_recall_edit_invalidates_approval():
    before = fragment()
    changed = before.replace('제곱을 구하라는 단서', '곱셈을 요구하는 단서')
    assert changed != before
    assert validate_reviews(pack(), {'p1': changed}, reviews())

def test_nested_heading_only_recall_refused():
    from mpe_shared import parse, outer
    text = with_recall()
    block = outer(next(parse(text).find_all(lambda n: n.attrs.get('data-explanation') == 'recall')))
    nested = ('<div class="layer formal" data-explanation="recall">'
              '<div><h4>제목뿐인 개념 구역</h4></div></div>')
    assert any('recall' in e for e in validate_fragment(problem(), text.replace(block, nested)))

def reviews():
    base = {'status': 'pass', 'reviewer': '검토자', 'evidence': '근거: MML p.1'}
    items = {f'p1:{s}': dict(base) for s in ('a', 'b')}
    return {'review_policy_version': POLICY_VERSION, 'input_hash': payload_hash(pack(), {'p1': fragment()}),
            'source_visual': base, 'browser': base, 'content': {**base, 'items': items},
            'independent': {**base, 'items': {k: {**v, 'method': 'exact', 'conclusion': '1=1'} for k,v in items.items()}}}

def test_all_subparts_must_be_solved_and_verified():
    assert validate_fragment(problem(), fragment()) == []
    broken = fragment().replace('data-subpart="b"', 'data-subpart="a"', 1)
    assert any('소문항' in e for e in validate_fragment(problem(), broken))

@pytest.mark.parametrize('markup', ['<details>답</details>', '<p hidden>답</p>', '<script>alert(1)</script>',
                                    '<img src="x" onerror="x">', '<a href="javascript:alert(1)">x</a>',
                                    '<p style="display:none">답</p>', '<iframe src="x"></iframe>'])
def test_hidden_or_active_explanation_refused(markup):
    assert validate_fragment(problem(), fragment() + markup)

def test_retry_and_missing_sections_refused():
    assert validate_fragment(problem(), fragment().replace('data-explanation="start"', 'data-explanation="solve"'))
    assert validate_fragment(problem(), fragment().replace('<li>다시 계산해요.</li>', ''))

def test_unreviewed_or_stale_or_incomplete_reports_refused():
    assert validate_reviews(pack(), {'p1': fragment()}, {})
    good = reviews()
    assert validate_reviews(pack(), {'p1': fragment()}, good) == []
    assert validate_reviews(pack(), {'p1': fragment() + '변경'}, good)
    for kind in ('source_visual', 'browser', 'content', 'independent'):
        bad = deepcopy(good)
        bad[kind]['status'] = 'not_run'
        assert validate_reviews(pack(), {'p1': fragment()}, bad)
    bad = deepcopy(good)
    del bad['independent']['items']['p1:b']
    assert validate_reviews(pack(), {'p1': fragment()}, bad)

def test_numerical_residual_requires_real_bounds():
    good = reviews()
    item = good['independent']['items']['p1:a']
    item.update(method='numerical', tolerance=1e-8, residual=1e-9)
    assert validate_reviews(pack(), {'p1': fragment()}, good) == []
    item['residual'] = 1
    assert validate_reviews(pack(), {'p1': fragment()}, good)
    item['residual'] = float('nan')
    assert validate_reviews(pack(), {'p1': fragment()}, good)
