"""Blind independent solve of 1028 PCA review problems P1-P4 (exact, sympy)."""
import sympy as sp
from sympy import Matrix, Rational as R, sqrt, symbols

def hdr(s): print("\n" + "=" * 8, s, "=" * 8)

# ---------- P1 ----------
hdr("P1 (MML Ex 10.1 variant)")
e1, e2 = Matrix([1, 0]), Matrix([0, 1])
x = Matrix([4, -7]); z = symbols('z', real=True)
c = Matrix.hstack(e1, e2).solve(x)
print("(a) coords of x:", list(c), "-> x = 4 e1 + (-7) e2; check:", c[0]*e1 + c[1]*e2 == x)
xt = Matrix([0, z])
ct = Matrix.hstack(e1, e2).solve(xt)
print("(b) coords of x~:", list(ct), "-> x~ = 0 e1 + z e2; e1-coordinate always 0, store only z (code wrt e2)")
# U = {[0,z]}: closed under +, scalar mult; spanned by e2
z1, z2, a = symbols('z1 z2 a', real=True)
print("(c) closure: [0,z1]+[0,z2] =", list(Matrix([0, z1]) + Matrix([0, z2])), "; a*[0,z1] =", list(a*Matrix([0, z1])))
print("    U = span[e2], basis {e2} (nonzero, so independent) -> dim U =", Matrix.hstack(e2).rank())

# ---------- P2 ----------
hdr("P2 (MML Ex 3.8 variant)")
b1, b2 = R(1, 5)*Matrix([3, 4]), R(1, 5)*Matrix([4, -3])
print("b1.b2 =", b1.dot(b2), " (12-12)/25")
print("||b1||^2 =", b1.dot(b1), " (9+16)/25 ; ||b2||^2 =", b2.dot(b2), " (16+9)/25")
B = Matrix.hstack(b1, b2)
print("B^T B =", (B.T*B).tolist(), "= I ->", B.T*B == sp.eye(2))
print("orthonormal => linearly independent (c1 b1 + c2 b2 = 0, dot with bi gives ci=0); 2 indep. vectors in dim-2 R^2 => basis; det B =", B.det())

# ---------- P3 ----------
hdr("P3 (MML Exercise 3.5)")
vs = [Matrix([0, -1, 2, 0, 2]), Matrix([1, -3, 1, -1, 2]),
      Matrix([-3, 4, 1, 2, 1]), Matrix([-1, -3, 5, 0, 7])]
x = Matrix([-1, -9, -1, 4, 1])
A = Matrix.hstack(*vs)
print("rank of spanning set =", A.rank(), "(dim U)")
rref, piv = A.rref(); print("pivot columns:", piv)
# dependency check
ns = A.nullspace(); print("null space of [v1..v4]:", [list(n) for n in ns])
Bm = Matrix.hstack(*[vs[i] for i in piv])  # basis of U
lam = (Bm.T*Bm).solve(Bm.T*x)
p = Bm*lam
print("normal eq  B^T B lam = B^T x ; lam =", list(lam))
print("(a) pi_U(x) =", list(p))
r = x - p
print("residual x - pi_U(x) =", list(r))
print("check residual orthogonal to every spanning vector:", [r.dot(v) for v in vs])
d2 = r.dot(r)
print("(b) d(x,U)^2 =", d2, "; d(x,U) =", sp.sqrt(d2), "~", sp.N(sp.sqrt(d2), 10))
# cross-check with projection matrix built from all 4 vectors via pseudoinverse
P = A*A.pinv()
print("cross-check A A^+ x =", list(P*x), "match:", P*x == p, "; P idempotent:", sp.simplify(P*P - P) == sp.zeros(5))
# Pythagoras
print("Pythagoras ||x||^2 = ||p||^2 + ||r||^2 :", x.dot(x), "=", p.dot(p), "+", d2, "->", x.dot(x) == p.dot(p) + d2)

# ---------- P4 ----------
hdr("P4 (MML Exercise 3.6 a,b)")
M = Matrix([[2, 1, 0], [1, 2, -1], [0, -1, 2]])
print("A symmetric:", M == M.T, "; leading minors:", [M[:k, :k].det() for k in (1, 2, 3)], "-> SPD, valid inner product")
ip = lambda u, v: (u.T*M*v)[0]
E1, E2, E3 = sp.eye(3).col(0), sp.eye(3).col(1), sp.eye(3).col(2)
Bu = Matrix.hstack(E1, E3)
G = Bu.T*M*Bu
rhs = Bu.T*M*E2
lam = G.solve(rhs)
print("Gram G = B^T A B =", G.tolist(), "; B^T A e2 =", list(rhs), "; lam =", list(lam))
p = Bu*lam
print("(a) pi_U(e2) =", list(p), " = 1/2 e1 - 1/2 e3")
r = E2 - p
print("residual e2 - pi_U(e2) =", list(r))
print("check <r,e1> =", ip(r, E1), " <r,e3> =", ip(r, E3))
d2 = ip(r, r)
print("(b) d(e2,U)^2 = <r,r>_A =", d2, "; d =", sp.sqrt(d2))
# check minimality: ||e2 - (a e1 + c e3)||_A^2 minimized
a_, c_ = symbols('a c', real=True)
f = sp.expand(ip(E2 - a_*E1 - c_*E3, E2 - a_*E1 - c_*E3))
sol = sp.solve([sp.diff(f, a_), sp.diff(f, c_)], [a_, c_])
print("min over a,c of ||e2-a e1-c e3||_A^2:", f, "-> argmin", sol, ", min =", f.subs(sol))
print("contrast: Euclidean projection would give 0 (e2 ⟂ e1,e3 in dot product), distance 1 -> projection differs (distance happens to coincide = 1)")
