from pathlib import Path
import sys

OUT = Path(__file__).resolve().parents[3]
REPO = next(p for p in OUT.parents if (p / '.git').exists())
sys.path.insert(0, str(REPO / '.claude/skills/ml-review-pack/scripts'))

def test_all_regeneration_inputs_use_course_derivative_convention():
    from check_vector_derivatives import check_text
    paths = list((OUT / '.pack/cards').glob('*.html')) + list((OUT / '.pack/explanations').glob('*.html'))
    assert len(paths) == 20
    errors = [(str(p.relative_to(OUT)), e) for p in paths for e in check_text(p.read_text(encoding='utf-8'))]
    assert errors == []

def test_derivative_to_normal_equation_explicitly_transposes():
    for n in (4, 6, 7):
        for folder in ('cards', 'explanations'):
            text = (OUT / f'.pack/{folder}/p{n}.html').read_text(encoding='utf-8')
            assert '전치' in text, (folder, n)
    assert 'Gradient는 행벡터' in (OUT / '.pack/cards/p2.html').read_text(encoding='utf-8')
