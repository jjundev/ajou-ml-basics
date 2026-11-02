"""Author-side independent check for 1102 PCA review problems p1-p5.

Computes characteristic polynomials, eigenvalues, eigenspaces (nullspaces),
multiplicities, Gram-Schmidt and the eigendecomposition with sympy (exact
rationals), and asserts the answers written in the explanation fragments.
"""
import sympy as sp

lam = sp.symbols("lambda")
out = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out.append(s)


def charpoly(A):
    n = A.shape[0]
    return sp.factor(sp.expand((A - lam * sp.eye(n)).det()))


def same_span(vs, ws):
    M1 = sp.Matrix.hstack(*vs)
    M2 = sp.Matrix.hstack(*ws)
    return M1.rank() == M2.rank() == sp.Matrix.hstack(M1, M2).rank()


# ---- p1 ----
log("== p1 (MML Ex 4.5 variant)")
A = sp.Matrix([[5, 4], [1, 2]])
p = charpoly(A)
log("p_A =", p, "| expanded:", sp.expand((A - lam * sp.eye(2)).det()))
assert sp.expand(p - (lam - 6) * (lam - 1)) == 0
for l, v in [(6, sp.Matrix([4, 1])), (1, sp.Matrix([1, -1]))]:
    N = (A - l * sp.eye(2)).nullspace()
    log(f"lambda={l}: nullspace={[list(n) for n in N]}, rank(A-lI)={(A-l*sp.eye(2)).rank()}, A v={list(A*v)}")
    assert len(N) == 1 and same_span(N, [v]) and A * v == l * v
# (a): A - lI singular exactly at roots
for l in [6, 1, 0, 2]:
    log(f"det(A-{l}I) =", (A - l * sp.eye(2)).det())
log("trace=", A.trace(), "sum eig=7; det=", A.det(), "prod eig=6")

# ---- p2 ----
log("== p2 (MML Ex 4.6 variant)")
A = sp.Matrix([[3, 1], [0, 3]])
p = charpoly(A)
log("p_A =", p)
assert sp.expand(p - (lam - 3) ** 2) == 0
log("eigenvals (alg mult):", A.eigenvals())
assert A.eigenvals() == {3: 2}
N = (A - 3 * sp.eye(2)).nullspace()
log("E_3 basis:", [list(n) for n in N], "geom mult =", len(N))
assert len(N) == 1 and same_span(N, [sp.Matrix([1, 0])])
log("diagonalizable?", A.is_diagonalizable())
assert not A.is_diagonalizable()

# ---- p3 ----
log("== p3 (MML Ex 4.8 variant)")
A = sp.Matrix([[4, 1, 1], [1, 4, 1], [1, 1, 4]])
assert A == A.T
p = charpoly(A)
log("p_A =", p)
assert sp.expand(p + (lam - 3) ** 2 * (lam - 6)) == 0
x1, x2, x3 = sp.Matrix([-1, 1, 0]), sp.Matrix([-1, 0, 1]), sp.Matrix([1, 1, 1])
N3 = (A - 3 * sp.eye(3)).nullspace()
N6 = (A - 6 * sp.eye(3)).nullspace()
log("E_3 basis(sympy):", [list(n) for n in N3], "E_6 basis:", [list(n) for n in N6])
assert len(N3) == 2 and same_span(N3, [x1, x2])
assert len(N6) == 1 and same_span(N6, [x3])
log("x3.x1 =", (x3.T * x1)[0], "x3.x2 =", (x3.T * x2)[0], "x1.x2 =", (x1.T * x2)[0])
assert (x3.T * x1)[0] == 0 and (x3.T * x2)[0] == 0 and (x1.T * x2)[0] == 1
a, b = sp.symbols("alpha beta")
comb = a * x1 + b * x2
assert sp.simplify(A * comb - 3 * comb) == sp.zeros(3, 1)
x2p = x2 - ((x1.T * x2)[0] / (x1.T * x1)[0]) * x1
log("x2' =", list(x2p))
assert x2p == sp.Matrix([sp.Rational(-1, 2), sp.Rational(-1, 2), 1])
assert (x1.T * x2p)[0] == 0 and (x3.T * x2p)[0] == 0 and A * x2p == 3 * x2p
GS = sp.GramSchmidt([x1, x2, x3], True)
P = sp.Matrix.hstack(*GS)
log("orthonormal P =", P.tolist())
assert sp.simplify(P.T * P) == sp.eye(3)
assert sp.simplify(P * sp.diag(3, 3, 6) * P.T - A) == sp.zeros(3, 3)
log("P D P^T == A : True")

# ---- p4 ----
log("== p4 (MML Ex 4.11 variant)")
A = sp.Rational(1, 2) * sp.Matrix([[7, -1], [-1, 7]])
p = charpoly(A)
log("p_A =", p, "| expanded:", sp.expand((A - lam * sp.eye(2)).det()))
assert sp.expand(p - (lam - 4) * (lam - 3)) == 0
p1 = sp.Matrix([1, -1]) / sp.sqrt(2)
p2 = sp.Matrix([1, 1]) / sp.sqrt(2)
assert sp.simplify(A * p1 - 4 * p1) == sp.zeros(2, 1)
assert sp.simplify(A * p2 - 3 * p2) == sp.zeros(2, 1)
assert sp.simplify(p1.norm() - 1) == 0 and sp.simplify(p2.norm() - 1) == 0
P = sp.Matrix.hstack(p1, p2)
D = sp.diag(4, 3)
log("P^T P =", sp.simplify(P.T * P).tolist(), "| det P =", sp.simplify(P.det()))
assert sp.simplify(P.T * P) == sp.eye(2)
assert sp.simplify(P.inv() - P.T) == sp.zeros(2, 2)
assert sp.simplify(P.inv() * A * P) == D
assert sp.simplify(P * D * P.T - A) == sp.zeros(2, 2)
log("P^-1 A P =", sp.simplify(P.inv() * A * P).tolist(), "; A == P D P^T : True")
log("trace=", A.trace(), "det=", A.det())

# ---- p5 ----
log("== p5 (MML Exercise 4.3)")
A = sp.Matrix([[1, 0], [1, 1]])
p = charpoly(A)
log("(a) p_A =", p, "eigenvals:", A.eigenvals())
N = (A - sp.eye(2)).nullspace()
log("(a) E_1 basis:", [list(n) for n in N], "geom mult =", len(N), "diagonalizable:", A.is_diagonalizable())
assert A.eigenvals() == {1: 2} and len(N) == 1 and same_span(N, [sp.Matrix([0, 1])])
B = sp.Matrix([[-2, 2], [2, 1]])
p = charpoly(B)
log("(b) p_B =", p, "| expanded:", sp.expand((B - lam * sp.eye(2)).det()))
assert sp.expand(p - (lam - 2) * (lam + 3)) == 0
for l, v in [(2, sp.Matrix([1, 2])), (-3, sp.Matrix([-2, 1]))]:
    N = (B - l * sp.eye(2)).nullspace()
    log(f"(b) lambda={l}: nullspace={[list(n) for n in N]}, B v={list(B*v)}")
    assert len(N) == 1 and same_span(N, [v]) and B * v == l * v
log("(b) v2.v(-3) =", (sp.Matrix([1, 2]).T * sp.Matrix([-2, 1]))[0], "(B symmetric:", B == B.T, ")")

log("ALL ASSERTIONS PASSED")
with open(__file__.replace(".py", ".txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
