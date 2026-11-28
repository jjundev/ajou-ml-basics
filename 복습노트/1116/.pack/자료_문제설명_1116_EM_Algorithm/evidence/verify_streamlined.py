"""Independent verification supplementing check_p1_p8.py against streamlined fragments p1..p8."""
import re
from pathlib import Path
from fractions import Fraction as F
import math
import sympy as sp

FRAG_DIR = Path(__file__).resolve().parents[1] / 'explanations'

def final_answer_text(pid):
    html = (FRAG_DIR / f'{pid}.html').read_text(encoding='utf-8')
    m = re.search(r'<section class="final-answer">(.*?)</section>', html, re.S)
    assert m, f'{pid}: missing final-answer'
    return m.group(1)

# P1: check exact values appear in streamlined final-answer
fa1 = final_answer_text('p1')
assert '0.294' in fa1 and '0.287' in fa1 and '0.419' in fa1
assert '1' in fa1 and '성분 $3$' in fa1

# P2
fa2 = final_answer_text('p2')
for s in [r'\frac{5}{2}', '2', '-2.6', '0.25', '4.4', r'-\frac{13}{5}', r'\frac{1}{4}', r'\frac{22}{5}']:
    assert s in fa2, f'p2 missing {s}'

# P3
fa3 = final_answer_text('p3')
for s in ['-2.70', '-0.40', '3.70', '1.30', '0.40', '4.30', '성분 $3$']:
    assert s in fa3, f'p3 missing {s}'

# P4
fa4 = final_answer_text('p4')
for s in ['0.15', '0.44', '1.53', '성분 $1$·$3$', '성분 $2$']:
    assert s in fa4, f'p4 missing {s}'

# P5
fa5 = final_answer_text('p5')
for s in ['1', '0.24', '0.50', '1.28', '성분 $3$', '4.36', '성분 $2$']:
    assert s in fa5, f'p5 missing {s}'

# P6: verify row gradient & normal equation consistency symbolically
Nn, Dd = 3, 2
Phi = sp.Matrix(Nn, Dd, lambda i, j: sp.Symbol(f'Phi_{i}{j}'))
theta = sp.Matrix(Dd, 1, lambda i, j: sp.Symbol(f'theta_{i}'))
y = sp.Matrix(Nn, 1, lambda i, j: sp.Symbol(f'y_{i}'))
e = y - Phi * theta
L = (e.T * e)[0, 0]
dL_dtheta = sp.Matrix(1, Dd, lambda i, j: sp.diff(L, theta[j]))
assert sp.simplify(dL_dtheta - (-2 * e.T * Phi)) == sp.zeros(1, Dd)
assert sp.simplify((-2 * e.T * Phi).T - (-2 * Phi.T * e)) == sp.zeros(Dd, 1)
fa6 = final_answer_text('p6')
assert r'-2\mathbf{e}^\top\boldsymbol{\Phi}' in fa6
assert r'\mathbb{R}^{1\times N}' in fa6 and r'\mathbb{R}^{N\times D}' in fa6 and r'\mathbb{R}^{1\times D}' in fa6

# P7
fa7 = final_answer_text('p7')
for s in [r'\frac{36}{25}', r'\frac{19}{16}', r'\frac{56}{25}', '성분 $1$·$3$', '성분 $2$']:
    assert s in fa7, f'p7 missing {s}'

# P8
fa8 = final_answer_text('p8')
assert r'\frac{2\cos\bigl(\log(\mathbf{t}^\top\mathbf{t})\bigr)}{\mathbf{t}^\top\mathbf{t}}\,\mathbf{t}^\top' in fa8
assert r'\mathbf{A}^\top\mathbf{B}^\top' in fa8
assert r'\mathbb{R}^{1\times D}' in fa8 and r'\mathbb{R}^{E\times F}' in fa8

print('STREAMLINED FINAL ANSWERS MATCH INDEPENDENT CHECKS: PASS')
