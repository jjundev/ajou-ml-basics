from decimal import Decimal, localcontext
from fractions import Fraction


def gaussian_density(x, mean, variance, pi):
    normalizer = (2 * pi * variance).sqrt()
    exponent = -(x - mean) ** 2 / (2 * variance)
    return exponent.exp() / normalizer


success = Fraction(3, 10)
failure = 1 - success
pmf = [failure ** 2, 2 * success * failure, success ** 2]
print("P1(a)", pmf, "(b)", sum(pmf))

counts = [[row * col for col in range(1, 6)] for row in range(1, 4)]
total = sum(map(sum, counts))
col_3 = sum(row[2] for row in counts)
row_2 = sum(counts[1])
cell = counts[1][2]
print("P2 counts", total, col_3, row_2, cell)
print("P2(a)", Fraction(col_3, total), Fraction(row_2, total))
print("P2(b)", Fraction(cell, col_3), Fraction(cell, row_2))

p_one = Fraction(7, 10)
p_zero = 1 - p_one
print("P4(a)", p_zero, p_one, "(b)", 0 * p_zero + 1 * p_one)
print("P5(b)", Fraction(1, 2) ** 3)

with localcontext() as ctx:
    ctx.prec = 72
    pi = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")
    params = [(Decimal("-4"), Decimal("1")),
              (Decimal("0"), Decimal("0.2")),
              (Decimal("8"), Decimal("3"))]
    for x in map(Decimal, ["0", "-1", "2"]):
        contributions = [gaussian_density(x, mean, variance, pi) / 3
                         for mean, variance in params]
        mixture = sum(contributions)
        posteriors = [c / mixture for c in contributions]
        winner = contributions.index(max(contributions)) + 1
        print(f"x={x} weighted components", [f"{c:.16g}" for c in contributions])
        print(f"x={x} p(x)={mixture:.18g}, to 4 d.p. {mixture:.4f}, winner={winner}")
        if x:
            print(f"x={x} responsibilities", [f"{p:.16g}" for p in posteriors])
            print(f"x={x} 3 d.p.", [f"{p:.3f}" for p in posteriors])
            assert abs(sum(posteriors) - 1) < Decimal("1e-70")

responsibility_rows = [(1000, 0, 0), (1000, 0, 0), (57, 943, 0),
                       (1, 999, 0), (0, 66, 934), (0, 0, 1000),
                       (0, 0, 1000)]
assert all(sum(row) == 1000 for row in responsibility_rows)
column_totals = [Fraction(sum(column), 1000) for column in zip(*responsibility_rows)]
print("P8(a)", column_totals, "sum", sum(column_totals))
print("P8(b)", column_totals.index(max(column_totals)) + 1)
