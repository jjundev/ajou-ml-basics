from sympy import Matrix, diag, eye, simplify, sqrt, symbols, zeros

t = symbols('t')
A = Matrix([[1, 0, 1], [-2, 1, 0]])
assert A * A.T == Matrix([[2, -2], [-2, 5]])
assert simplify((A * A.T).charpoly(t).as_expr() - (t - 6) * (t - 1)) == 0
U = Matrix([[1, 2], [-2, 1]]) / sqrt(5)
V = Matrix.hstack(
    A.T * U[:, 0] / sqrt(6),
    A.T * U[:, 1],
    Matrix([-1, -2, 1]) / sqrt(6),
)
S = Matrix([[sqrt(6), 0, 0], [0, 1, 0]])
assert simplify(U.T * U) == eye(2)
assert simplify(V.T * V) == eye(3)
assert simplify(A - U * S * V.T) == zeros(2, 3)
print('P4 exact full SVD checked')

A = Matrix([[2, 2], [-1, 1]])
assert A * A.T == diag(8, 2)
U = eye(2)
S = diag(2 * sqrt(2), sqrt(2))
V = Matrix([[1, -1], [1, 1]]) / sqrt(2)
assert simplify(V.T * V) == eye(2)
assert simplify(A - U * S * V.T) == zeros(2, 2)
print('P6 exact SVD checked')

A = Matrix([[3, 2, 2], [2, 3, -2]])
assert A * A.T == Matrix([[17, 8], [8, 17]])
u1 = Matrix([1, 1]) / sqrt(2)
u2 = Matrix([1, -1]) / sqrt(2)
v1 = A.T * u1 / 5
v2 = A.T * u2 / 3
assert simplify(v1.T * v2) == zeros(1, 1)
assert simplify(v1.T * v1) == eye(1)
assert simplify(v2.T * v2) == eye(1)
B = simplify(5 * u1 * v1.T)
assert B == Matrix([[5, 5, 0], [5, 5, 0]]) / 2
assert B.rank() == 1
R = A - B
assert simplify(R - 3 * u2 * v2.T) == zeros(2, 3)
assert R.norm() == 3
assert (R * R.T).eigenvals() == {9: 1, 0: 1}
print('P7 exact rank-one approximation and residual checked')
