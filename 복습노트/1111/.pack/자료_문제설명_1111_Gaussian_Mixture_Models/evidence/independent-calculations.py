"""1111 문제 전용 PDF에서 읽은 값으로 P1/P2/P4/P5/P6/P7/P8을 재계산한다."""

from decimal import Decimal
from fractions import Fraction
from math import comb, exp, fsum, isclose, pi, sqrt

coin_probabilities = tuple(
    comb(2, count) * Fraction(3, 10) ** count * Fraction(7, 10) ** (2 - count)
    for count in range(3)
)
print("P1:", coin_probabilities, sum(coin_probabilities))
assert coin_probabilities == (Fraction(49, 100), Fraction(42, 100), Fraction(9, 100))
assert sum(coin_probabilities) == 1

frequencies = ((1, 2, 3, 4, 5), (2, 4, 6, 8, 10), (3, 6, 9, 12, 15))
total = sum(map(sum, frequencies))
x3 = sum(row[2] for row in frequencies)
y2 = sum(frequencies[1])
intersection = frequencies[1][2]
marginals = (Fraction(x3, total), Fraction(y2, total))
conditionals = (Fraction(intersection, x3), Fraction(intersection, y2))
print("P2:", total, marginals, conditionals)
assert marginals == (Fraction(1, 5), Fraction(1, 3))
assert conditionals == (Fraction(1, 3), Fraction(1, 5))

mu = Fraction(7, 10)
bernoulli = tuple(mu ** x * (1 - mu) ** (1 - x) for x in (0, 1))
expectation = sum(x * probability for x, probability in enumerate(bernoulli))
print("P4:", bernoulli, expectation)
assert bernoulli == (Fraction(3, 10), Fraction(7, 10))
assert expectation == Fraction(7, 10)

cdf_half = Fraction(1, 2) ** 3
print("P5(b):", cdf_half)
assert cdf_half == Fraction(1, 8)

# The parameters are printed on page 6. Page 7 has no parameter values.
parameters = ((-4, 1), (0, 0.2), (8, 3))
expected_responsibilities = {
    -1: (0.057, 0.943, 0.000),
    2: (0.000, 0.066, 0.934),
}
inherited_responsibilities = {}
for x in (-3, -2.5, -1, 0, 2, 4, 5):
    weighted = tuple(exp(-(x - mean) ** 2 / (2 * var)) / (3 * sqrt(2 * pi * var))
                     for mean, var in parameters)
    density = fsum(weighted)
    responsibilities = tuple(value / density for value in weighted)
    inherited_responsibilities[x] = responsibilities
    print(f"P6 parameters, x = {x}: weighted = {weighted}, p(x) = {density:.15g}, "
          f"r(x) = {responsibilities}")
    assert isclose(fsum(responsibilities), 1, rel_tol=0, abs_tol=2e-15)
    if x == 0:
        assert format(density, ".4f") == "0.2974"
        assert weighted.index(max(weighted)) + 1 == 2
    if x in expected_responsibilities:
        assert tuple(round(value, 3) for value in responsibilities) == expected_responsibilities[x]
        assert responsibilities.index(max(responsibilities)) + 1 == {-1: 2, 2: 3}[x]

displayed_rows = (
    ("1.0", "0.0", "0.0"),
    ("1.0", "0.0", "0.0"),
    ("0.057", "0.943", "0.0"),
    ("0.001", "0.999", "0.0"),
    ("0.0", "0.066", "0.934"),
    ("0.0", "0.0", "1.0"),
    ("0.0", "0.0", "1.0"),
)
rows = tuple(tuple(map(Decimal, row)) for row in displayed_rows)
totals = tuple(map(sum, zip(*rows)))
print("P8:", totals, sum(totals))
assert totals == (Decimal("2.058"), Decimal("2.008"), Decimal("2.934"))
assert sum(totals) == 7
assert totals.index(max(totals)) + 1 == 3
for x, row in zip(inherited_responsibilities, rows):
    rounded = tuple(Decimal(format(value, ".3f")) for value in inherited_responsibilities[x])
    if rounded != row:
        print(f"P8 if identified with P6 in the same order, x = {x}: "
              f"P6 rounded to three digits = {rounded}, P8 displayed = {row}")
