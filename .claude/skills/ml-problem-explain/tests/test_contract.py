from copy import deepcopy
import pytest
from helpers import problem, fragment, pack
from mpe_contract import validate_fragment, validate_reviews, payload_hash

def reviews():
    base = {'status': 'pass', 'reviewer': '검토자', 'evidence': '근거: MML p.1'}
    items = {f'p1:{s}': dict(base) for s in ('a', 'b')}
    return {'input_hash': payload_hash(pack(), {'p1': fragment()}),
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
