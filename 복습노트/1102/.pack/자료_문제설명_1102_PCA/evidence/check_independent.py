"""Exact matrix checks from the original 1102 problem PDF."""
from pathlib import Path
import re

from sympy import Matrix, diag, eye, sqrt, symbols, zeros

lam = symbols("lambda")


def check_space(matrix, value, *basis):
    shifted = matrix - value * eye(matrix.rows)
    vectors = Matrix.hstack(*(Matrix(vector) for vector in basis))
    assert shifted * vectors == zeros(matrix.rows, len(basis))
    assert vectors.rank() == len(basis) == matrix.rows - shifted.rank()


def check_polynomial(matrix, expected):
    actual = (matrix - lam * eye(matrix.rows)).det()
    assert (actual - expected).expand() == 0


m = Matrix([[5, 4], [1, 2]])
check_polynomial(m, (lam - 1) * (lam - 6))
check_space(m, 1, (-1, 1))
check_space(m, 6, (4, 1))
assert Matrix([-1, 1]).dot(Matrix([4, 1])) == -3

m = Matrix([[3, 1], [0, 3]])
check_polynomial(m, (3 - lam)**2)
check_space(m, 3, (1, 0))

m = Matrix([[4, 1, 1], [1, 4, 1], [1, 1, 4]])
v1, v2, v3 = (Matrix(v) for v in [(-1, 1, 0), (-1, 0, 1), (1, 1, 1)])
check_polynomial(m, -(lam - 3)**2 * (lam - 6))
check_space(m, 3, v1, v2)
check_space(m, 6, v3)
assert (v3.dot(v1), v3.dot(v2), v1.dot(v2)) == (0, 0, 1)
orthogonal_v2 = v2 - v1 * (v1.dot(v2) / v1.dot(v1))
check_space(m, 3, v1, orthogonal_v2)
assert (v1.dot(orthogonal_v2), v1.dot(v3), orthogonal_v2.dot(v3)) == (0, 0, 0)

m = Matrix([[7, -1], [-1, 7]]) / 2
check_polynomial(m, (4 - lam) * (3 - lam))
p = Matrix([[1, 1], [-1, 1]]) / sqrt(2)
d = diag(4, 3)
assert m * p == p * d
assert p.T * p == eye(2) and p * d * p.T == m

m = Matrix([[1, 3, 5], [2, 4, 6], [0, 2, 4]])
assert m.det() == 0 and m * Matrix([1, -2, 1]) == zeros(3, 1)

m = Matrix([[1, 0], [1, 1]])
check_polynomial(m, (1 - lam)**2)
check_space(m, 1, (0, 1))
m = Matrix([[-2, 2], [2, 1]])
check_polynomial(m, (lam - 2) * (lam + 3))
check_space(m, 2, (1, 2))
check_space(m, -3, (-2, 1))
assert Matrix([1, 2]).dot(Matrix([-2, 1])) == 0

m1, m2 = eye(2), diag(1, 0)
m3, m4 = Matrix([[1, 1], [0, 1]]), Matrix([[0, 1], [0, 0]])
assert m1.is_diagonal() and m2.is_diagonal()
check_polynomial(m3, (1 - lam)**2)
check_polynomial(m4, lam**2)
check_space(m3, 1, (1, 0))
check_space(m4, 0, (1, 0))
assert [m.det() for m in (m1, m2, m3, m4)] == [1, 0, 1, 0]

m = Matrix([[2, 3, 0], [1, 4, 3], [0, 0, 1]])
check_polynomial(m, (1 - lam)**2 * (5 - lam))
check_space(m, 1, (-3, 1, 0))
check_space(m, 5, (1, 1, 0))
m = Matrix([[1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
v1, v2, v3, v4 = (1, 0, 0, 0), (-1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)
check_polynomial(m, (1 - lam) * (-lam)**3)
check_space(m, 1, v1)
check_space(m, 0, v2, v3, v4)
p = Matrix.hstack(*(Matrix(v) for v in [v1, v2, v3, v4]))
assert p.det() == 1 and m * p == p * diag(1, 0, 0, 0)

m = Matrix([[0, 1], [-8, 4]])
check_polynomial(m, lam**2 - 4 * lam + 8)
assert (lam**2 - 4 * lam + 8).as_poly(lam).discriminant() == -16
m = Matrix([[5, -6, -6], [-1, 4, 2], [3, -6, -4]])
v1, v2, v3 = (-3, 1, -3), (2, 1, 0), (2, 0, 1)
check_polynomial(m, -(lam - 1) * (lam - 2)**2)
check_space(m, 1, v1)
check_space(m, 2, v2, v3)
p = Matrix.hstack(*(Matrix(v) for v in [v1, v2, v3]))
assert p.det() == 1 and m * p == p * diag(1, 2, 2)

m = Matrix([[1, 0]])
assert m.T * m == diag(1, 0) and m * m.T == Matrix([[1]])

notes = Path(__file__).with_name("independent.md").read_text(encoding="utf-8-sig")
keys = re.findall(r"^- \*\*(P\d+:[a-d])\*\*", notes, flags=re.M)
counts = [4, 3, 4, 4, 2, 3, 2, 4, 3, 3]
expected = [f"P{problem}:{letter}" for problem, count in enumerate(counts, 1)
            for letter in "abcd"[:count]]
assert keys == expected
print(f"{len(counts)} problems, {len(keys)} subparts. Exact SymPy checks passed.")
