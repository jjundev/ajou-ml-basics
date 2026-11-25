#!/usr/bin/env python3
"""
과제1(Homework #1) 정답 키와 카드 대조기.

모든 수치 정답을 Fraction으로 정확히 계산하고, 과제1 카드 HTML의
`.answer`에 정답 TeX 토큰이 그대로 들어 있는지 검사한다.
토큰 규약: 정수는 그대로, 분수는 \\frac{p}{q}(음수는 앞에 -), 행렬·벡터는
\\begin{bmatrix}...\\end{bmatrix}(열벡터는 한 칸짜리 행). 비교 전 HTML 엔티티를
풀고 모든 공백을 지운다.
"""

from __future__ import annotations

from fractions import Fraction as F
import html
from pathlib import Path
import re
import sys

Matrix = list[list[F]]


def mat(rows) -> Matrix:
    return [[F(v) for v in row] for row in rows]


def col(*values) -> Matrix:
    return [[F(v)] for v in values]


def T(a: Matrix) -> Matrix:
    return [list(r) for r in zip(*a)]


def mul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(c, a: Matrix) -> Matrix:
    return [[F(c) * x for x in r] for r in a]


def eye(n: int) -> Matrix:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def det(a: Matrix) -> F:
    if len(a) == 1:
        return a[0][0]
    return sum((-1) ** j * a[0][j] * det([r[:j] + r[j + 1:] for r in a[1:]]) for j in range(len(a)))


def inv(a: Matrix) -> Matrix:
    n = len(a)
    m = [list(r) + e for r, e in zip(a, eye(n))]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        m[c] = [x / m[c][c] for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                m[r] = [x - m[r][c] * y for x, y in zip(m[r], m[c])]
    return [r[n:] for r in m]


def fr(x) -> str:
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    sign = '-' if x < 0 else ''
    return f'{sign}\\frac{{{abs(x.numerator)}}}{{{x.denominator}}}'


def bm(a: Matrix) -> str:
    return '\\begin{bmatrix}' + '\\\\'.join('&'.join(fr(v) for v in r) for r in a) + '\\end{bmatrix}'


# ---- 수치 정답 ----
P3_A, P3_B = mat([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), mat([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
P8_A = mat([[1, -1], [1, 0], [1, 1]])
P9_PHI = mat([[1, -1, 1], [1, 0, 0], [1, 1, 1]])
P17_PHI, P17_Y = mat([[1, -1], [1, 0], [1, 1]]), col(2, 1, 4)


def p17_ml() -> Matrix:
    return mul(inv(mul(T(P17_PHI), P17_PHI)), mul(T(P17_PHI), P17_Y))


def p19_map(b2) -> Matrix:
    g = add(mul(T(P17_PHI), P17_PHI), scale(1 / F(b2), eye(2)))  # sigma^2 = 1
    return mul(inv(g), mul(T(P17_PHI), P17_Y))


def p20() -> tuple[Matrix, F]:
    phi, y = mat([[1, 1], [2, 2]]), col(3, 6)
    th = mul(inv(add(mul(T(phi), phi), scale(5, eye(2)))), mul(T(phi), y))
    r = add(y, scale(-1, mul(phi, th)))
    return th, mul(T(r), r)[0][0] + 5 * mul(T(th), th)[0][0]


def p21() -> tuple[Matrix, Matrix]:
    xs = [col(1, 1), col(1, 3), col(3, 3), col(3, 5)]
    m = scale(F(1, 4), [[sum(x[i][0] for x in xs)] for i in range(2)])
    s = [[F(0)] * 2 for _ in range(2)]
    for x in xs:
        d = add(x, scale(-1, m))
        s = add(s, mul(d, T(d)))
    return m, scale(F(1, 4), s)


def linear_map(a: Matrix, c: Matrix, mu: Matrix, sx: Matrix, extra: Matrix | None = None):
    """y = A x + c (+ 독립 잡음 공분산 extra) -> (mu_y, Sigma_y, C_xy)."""
    sy = mul(mul(a, sx), T(a))
    return add(mul(a, mu), c), add(sy, extra) if extra else sy, mul(sx, T(a))


P22B_SX = inv(mat([[1, -1], [-1, 2]]))  # 지수 이차형식의 정밀도 행렬을 뒤집은 것
P22 = {
    'a': linear_map(mat([[1, 2], [-1, 1]]), col(1, -2), col(1, 2), mat([[4, 1], [1, 2]])),
    'b': linear_map(mat([[2, -1], [1, 1]]), col(-1, 2), col(1, -1), P22B_SX),
    # Cov(x1,x2) = E[x1x2] - E[x1]E[x2] = 0 - (1)(-1) = 1, 같은 eps가 두 좌표에 들어가 1로 채운 행렬이 더해짐
    'c': linear_map(mat([[1, 1], [1, -1]]), col(0, 0), col(1, -1), mat([[2, 1], [1, 3]]), mat([[1, 1], [1, 1]])),
}


def p23() -> tuple[F, F]:
    xs, ys = (1, 2), (2, 3)
    sxx, sxy = sum(F(x * x) for x in xs), sum(F(x * y) for x, y in zip(xs, ys))
    return sxy / sxx, sxy / (sxx + 1)  # prior N(0,1), noise var 1


def p24() -> tuple[F, F]:
    ys = (2, 3, 4)
    return F(sum(ys), len(ys)), F(sum(ys) + 1, len(ys) + 1)  # prior N(1,1), noise var 1


def p25() -> tuple[Matrix, Matrix]:
    s0, s1 = mat([[1, 0], [0, 2]]), mat([[2, 1], [1, 2]])
    sq = inv(add(inv(s0), inv(s1)))
    return mul(sq, add(mul(inv(s0), col(0, 0)), mul(inv(s1), col(1, 1)))), sq


def key() -> dict[str, list[str]]:
    th17, (th20, j20) = p17_ml(), p20()
    m21, s21 = p21()
    ml23, map23 = p23()
    ml24, map24 = p24()
    mu25, s25 = p25()
    g8 = mul(T(P8_A), P8_A)
    k = {
        'p1': [bm(T(mat([[1, -2, 3], [0, 4, 5]]))), bm(T(col(2, -1, 4))), bm(T(mat([[1, 2, 0], [-1, 3, 4], [5, 0, -2]])))],
        'p2': ['\\mathbf{x}^\\top\\mathbf{y}=0', '\\|\\mathbf{x}\\|_2=3', '\\|\\mathbf{y}\\|_2=\\sqrt{5}', '직교'],
        'p3': [bm(mul(P3_A, P3_B)), bm(mul(P3_B, P3_A)), '\\neq'],
        'p4': [f'\\det(\\mathbf{{{n}}})={fr(det(mat(m)))}' for n, m in
               [('A', [[3, 1], [2, 4]]), ('B', [[1, -2], [3, 0]]), ('C', [[2, 0, 0], [0, -1, 0], [0, 0, 3]]), ('D', [[1, 3, 5], [2, 4, 6], [0, 2, 4]])]],
        'p5': [f'\\mathbf{{{n}}}^{{-1}}=' + bm(inv(mat(m))) for n, m in
               [('A', [[2, 1], [1, 1]]), ('B', [[1, -2], [3, 1]]), ('C', [[2, 1, 0], [1, 2, 0], [0, 0, 2]])]],
        'p6': ['\\mathbf{x}_3=2\\mathbf{x}_1-\\mathbf{x}_2', '선형 종속'],
        'p7': ['\\mathbf{y}=-6\\mathbf{x}_1+3\\mathbf{x}_2+2\\mathbf{x}_3'],
        'p8': [bm(g8), '=' + fr(det(g8)), bm(inv(g8))],
        'p9': [bm(P9_PHI), bm(mul(P9_PHI, col(1, 1, 2)))],
        'p10': [bm(col(0, -2)), bm(col(-4, -2)), bm(col(-2, -4, 2))],
        'p11': [bm(mat([[1, 2], [3, -1]])), bm(mat([[2, 1], [2, 1], [0, 4]]))],
        'p12': ['3x_1^2+2x_1x_2+2x_2^2-2x_1+2x_2', 'x_1=' + fr(F(3, 5)), 'x_2=' + fr(F(-4, 5))],
        'p13': ['\\frac{1}{2\\pi\\sqrt{3}}', '-\\frac{1}{3}(x_1^2-x_1x_2+x_2^2-3x_1+3x_2+3)'],
        'p14': ['c=\\sqrt{\\frac{2}{\\pi}}e^{3/2}', '\\mu=1', 'v=\\frac{1}{4}'],
        'p15': ['(2\\pi\\sigma^2)^{-N/2}', '\\sum_{n=1}^{N}(y_n-\\theta_0-\\theta_1x_n)^2'],
        'p16': ['\\frac{N}{2}\\log(2\\pi\\sigma^2)', '\\frac{1}{2\\sigma^2}\\|\\mathbf{y}-\\boldsymbol{\\Phi}\\boldsymbol{\\theta}\\|_2^2'],
        'p17': ['(\\boldsymbol{\\Phi}^\\top\\boldsymbol{\\Phi})^{-1}\\boldsymbol{\\Phi}^\\top\\mathbf{y}', bm(th17), bm(mul(P17_PHI, th17)), 'S=\\frac{8}{3}'],
        'p18': ['\\frac{\\sigma^2}{b^2}\\mathbf{I}_K', '\\lambda=\\frac{\\sigma^2}{b^2}'],
        'p19': [bm(th17), bm(p19_map(1)), bm(p19_map(F(1, 4)))],
        'p20': [bm(mat([[5, 5], [5, 5]])), '\\det(\\boldsymbol{\\Phi}^\\top\\boldsymbol{\\Phi})=0', bm(col(3, 6)), bm(th20), '=' + fr(j20)],
        'p21': [bm(m21), bm(s21)],
        'p22': [bm(v) for part in 'abc' for v in P22[part]] + [bm(col(1, -1)), bm(P22B_SX)],
        'p23': ['\\frac{1}{2\\pi}', '\\theta_{\\mathrm{ML}}=' + fr(ml23), '\\theta_{\\mathrm{MAP}}=' + fr(map23),
                '\\hat{y}_{\\mathrm{ML}}=' + fr(3 * ml23), '\\hat{y}_{\\mathrm{MAP}}=' + fr(3 * map23)],
        'p24': ['(2\\pi)^{-3/2}', '\\theta_{\\mathrm{ML}}=' + fr(ml24), '\\theta_{\\mathrm{MAP}}=' + fr(map24), 'MAP'],
        'p25': [bm(mu25), bm(s25), bm(inv(s25)), '\\frac{1}{2\\pi}\\sqrt{\\frac{11}{6}}'],
    }
    return {p: [re.sub(r'\s+', '', t) for t in ts] for p, ts in k.items()}


def missing(answers: dict[str, str]) -> list[str]:
    """answers: 카드 id -> answer HTML. 카드가 없거나 토큰이 빠진 항목을 돌려준다."""
    out = []
    for pid, tokens in key().items():
        if pid not in answers:
            out.append(f'{pid}: no card')
            continue
        text = re.sub(r'\s+', '', html.unescape(answers[pid]))
        out += [f'{pid}: missing {t}' for t in tokens if t not in text]
    return out


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.claude/skills/ml-review-pack/scripts'))
    from review_pdf_cards import read_cards
    from review_pdf_types import HOMEWORK
    pack = read_cards(Path(argv[0]), HOMEWORK)
    only = set(argv[1].split(',')) if len(argv) > 1 else None
    problems = [m for m in missing({c.id: c.answer_html for c in pack.cards}) if only is None or m.split(':')[0] in only]
    print('\n'.join(problems) or 'OK')
    return 1 if problems else 0


if __name__ == '__main__':
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2:
        for pid, tokens in key().items():
            print(pid, *tokens, sep='\n  ')
        sys.exit(0)
    sys.exit(main(sys.argv[1:]))
