#!/usr/bin/env python3
"""
복습문제_0909-0916 정답 키.

교과서(MML)에는 공식 풀이가 없으므로, 복습문제 HTML의 모든 수치 정답을
여기서 Fraction으로 정확히 계산해 대조한다. 실행하면 정답표를 출력한다.
"""

from __future__ import annotations

from fractions import Fraction
import math

# MML Exercise 6.1: 행 = y1..y3, 열 = x1..x5
EX61_TABLE: tuple[tuple[Fraction, ...], ...] = (
    tuple(Fraction(v, 100) for v in (1, 2, 3, 10, 10)),
    tuple(Fraction(v, 100) for v in (5, 10, 5, 7, 20)),
    tuple(Fraction(v, 100) for v in (10, 5, 3, 5, 4)),
)


def ex61_marginals() -> tuple[list[Fraction], list[Fraction]]:
    """p(x)는 열 합, p(y)는 행 합."""
    px = [sum(row[j] for row in EX61_TABLE) for j in range(5)]
    py = [sum(row) for row in EX61_TABLE]
    return px, py


def ex61_conditionals() -> tuple[list[Fraction], list[Fraction]]:
    """p(x | Y=y1), p(y | X=x3)."""
    px, py = ex61_marginals()
    x_given_y1 = [v / py[0] for v in EX61_TABLE[0]]
    y_given_x3 = [row[2] / px[2] for row in EX61_TABLE]
    return x_given_y1, y_given_x3


def ex64_bag2_given_mango() -> Fraction:
    """MML Exercise 6.4: P(bag2 | mango)."""
    p_bag1, p_bag2 = Fraction(6, 10), Fraction(4, 10)
    p_mango_bag1, p_mango_bag2 = Fraction(4, 6), Fraction(4, 8)
    numerator = p_bag2 * p_mango_bag2
    return numerator / (p_bag1 * p_mango_bag1 + numerator)


def beta_bernoulli_posterior(alpha: int, beta: int, n: int, k: int) -> tuple[int, int]:
    """Beta(alpha, beta) prior + Bernoulli 관측 n번 중 k번 1 -> Beta(alpha+k, beta+n-k)."""
    return alpha + k, beta + n - k


def coin_estimates(n: int, k: int, alpha: int, beta: int) -> tuple[Fraction, Fraction, Fraction]:
    """(ML, MAP=사후 최빈값, 다음 관측이 1일 예측확률=사후 평균)."""
    ml = Fraction(k, n)
    map_ = Fraction(k + alpha - 1, n + alpha + beta - 2)
    pred = Fraction(k + alpha, n + alpha + beta)
    return ml, map_, pred


def ex71_stationary_points() -> list[tuple[float, str]]:
    """MML Exercise 7.1: f(x) = x^3 + 6x^2 - 3x - 5."""
    points = []
    for x in (-2 - math.sqrt(5), -2 + math.sqrt(5)):
        second = 6 * x + 12
        kind = "min" if second > 0 else "max" if second < 0 else "saddle"
        points.append((x, kind))
    return points


def map_l2_lambda(sigma2, b2, n) -> Fraction:
    """가우시안 likelihood(분산 sigma2) + N(0, b2 I) prior의 MAP = 정규화 LS의 lambda."""
    return Fraction(sigma2) / (n * Fraction(b2))


def main() -> None:
    px, py = ex61_marginals()
    x_y1, y_x3 = ex61_conditionals()
    print("Ex 6.1 p(x):", [str(v) for v in px], "p(y):", [str(v) for v in py])
    print("Ex 6.1 p(x|y1):", [str(v) for v in x_y1], "p(y|x3):", [str(v) for v in y_x3])
    print("Ex 6.4 P(bag2|mango):", ex64_bag2_given_mango())
    print("Ex 6.3 posterior Beta(4,4), N=10, k=2:", beta_bernoulli_posterior(4, 4, 10, 2))
    print("coin (ML, MAP, pred) a=4:", [str(v) for v in coin_estimates(10, 2, 4, 4)])
    print("Ex 7.1:", ex71_stationary_points())


if __name__ == "__main__":
    main()
