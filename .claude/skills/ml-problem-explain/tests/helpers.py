from pathlib import Path
from mpe_types import Problem, SourcePack

def problem():
    return Problem('p1', 1, '행렬', 'HW1 Problem 1', '<p>Find (a), (b).</p>',
                   '<p>$A=1$</p>', '<ol><li>(a) $A$</li><li>(b) $A^2$</li></ol>',
                   (), ('계산',), '1', ('a', 'b'))

def fragment(p=None):
    p = p or problem()
    parts = ''.join(f'<div data-subpart="{key}"><p>첫 식에서 계산하고 대입해 확인해요. $1=1$</p></div>' for key in p.subparts)
    return ('<div class="layer eli5" data-explanation="understand"><p>구할 것을 읽어요.</p></div>'
            '<div class="layer formal" data-explanation="recall">'
            '<h4>이 문제를 봤을 때 떠올릴 개념과 공식</h4>'
            '<p>제곱을 구하라는 단서에서 같은 수의 곱을 떠올려요. '
            '$A^2=A\\cdot A$이며 A는 주어진 스칼라예요.</p></div>'
            '<div class="layer formal" data-explanation="start"><p>$A=1$부터 써요.</p></div>'
            f'<div class="layer formal" data-explanation="solve">{parts}</div>'
            f'<div class="layer formal" data-explanation="verify">{parts}</div>'
            '<div class="layer warn" data-explanation="pitfall"><p>행과 열을 바꾸지 않아요.</p></div>'
            '<div class="layer formal" data-explanation="retry"><ul><li>다시 계산해요.</li></ul></div>'
            '<div class="sum" hidden><p>시작·판단·검산</p></div>')

def pack(path=Path('과제1_Homework1.html')):
    return SourcePack('homework', '1', 'Homework1', path, '0'*64, (problem(),))

def approved(pack, fragments, artifacts=None):
    from mpe_contract import payload_hash
    from mpe_render import artifact_hashes
    base = {'status': 'pass', 'reviewer': 'test fixture', 'evidence': 'fixture calculation at evidence.txt'}
    keys = [f'{p.id}:{s}' for p in pack.problems for s in p.subparts]
    from mpe_review_policy import POLICY_VERSION
    result = {'review_policy_version': POLICY_VERSION, 'input_hash': payload_hash(pack, fragments),
              'source_visual': dict(base), 'browser': dict(base),
              'content': {**base, 'items': {k: dict(base) for k in keys}},
              'independent': {**base, 'items': {k: {**base, 'method': 'exact', 'conclusion': '1=1'} for k in keys}},
              'references': []}
    if artifacts:
        result['artifact_hashes'] = artifact_hashes(artifacts)
    return result
