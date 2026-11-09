"""Blind independent check for review-1028-PCA problems p1..p5 (exact arithmetic via sympy)."""
import sympy as sp
from sympy import Matrix, Rational, sqrt, symbols, expand, factor, simplify

def hdr(s): print("\n=== " + s + " ===")

# ---------------- P1 ----------------
hdr("P1")
e1, e2 = Matrix([1, 0]), Matrix([0, 1])
x = Matrix([4, -7])
# (a) x = x1 e1 + x2 e2 ; coefficients are the coordinates themselves
c = Matrix.hstack(e1, e2).solve(x)
assert c[0]*e1 + c[1]*e2 == x
print("p1(a): x = %s*e1 + (%s)*e2" % (c[0], c[1]))
z = symbols('z', real=True)
xt = Matrix([0, z])
ct = Matrix.hstack(e1, e2).solve(xt)
assert sp.simplify(ct[0]*e1 + ct[1]*e2 - xt) == sp.zeros(2, 1)
print("p1(b): x~ = %s*e1 + %s*e2 ; first coefficient always 0 -> only the single number z must be stored" % (ct[0], ct[1]))
# (c) U = {[0,z]^T : z in R} = {z e2} = span[e2]
# proof: every element is z*e2 (shown above); conversely any z*e2 = [0,z]^T is of that form.
print("p1(c): U = span[e2] = span[[0,1]^T]  (every [0,z]^T = z*e2 and every z*e2 has first component 0)")
# (d) e2 != 0 so {e2} is linearly independent -> basis of U -> dim 1
print("p1(d): dim U = rank([e2]) =", Matrix.hstack(e2).rank())

# ---------------- P2 ----------------
hdr("P2")
b1 = Rational(1, 5)*Matrix([3, 4]); b2 = Rational(1, 5)*Matrix([4, -3])
B = Matrix.hstack(b1, b2)
BtB = B.T*B
print("p2(a): B^T B =", BtB.tolist())
# (b) (B^T B)_{ij} = <b_i,b_j>. BtB = I means <b_i,b_i>=1 and <b1,b2>=0 -> orthonormal;
# two orthonormal (hence linearly independent) vectors in 2-dim R^2 form a basis.
print("p2(b): B^T B == I ?", BtB == sp.eye(2), "; rank B =", B.rank(), "-> orthonormal basis of R^2: YES")

# ---------------- P3 ----------------
hdr("P3")
x = Matrix([5, 1]); b1 = Matrix([1, -1]); b2 = Matrix([1, 1])
B = Matrix.hstack(b1, b2)
coords = B.solve(x)
assert coords[0]*b1 + coords[1]*b2 == x
print("p3(a): coordinates of x w.r.t. (b1,b2) =", coords.T.tolist()[0], " i.e. x = 2*b1 + 3*b2")
# note: b1 ⟂ b2 (dot 0) so also coords_i = <x,b_i>/<b_i,b_i>
print("       check via orthogonal formula: <x,b1>/|b1|^2 =", x.dot(b1)/b1.dot(b1), ", <x,b2>/|b2|^2 =", x.dot(b2)/b2.dot(b2), ", <b1,b2> =", b1.dot(b2))
print("p3(b): ||b1|| =", sqrt(b1.dot(b1)), ", ||b2|| =", sqrt(b2.dot(b2)), "-> NOT normalized (length sqrt(2) != 1); orthogonal but not orthonormal")

# ---------------- P4 ----------------
hdr("P4")
x1, x2 = symbols('x1 x2', real=True)
xv = Matrix([x1, x2])
A1 = Matrix([[4, 2], [2, 3]]); A2 = Matrix([[4, 2], [2, 0]])
q1 = expand((xv.T*A1*xv)[0])
cs1 = (2*x1 + x2)**2 + 2*x2**2
assert expand(cs1 - q1) == 0
print("p4(a): x^T A1 x =", q1, "=", cs1)
# argument: sum of squares >= 0; = 0 iff x2=0 and 2x1+x2=0 iff x1=x2=0. So >0 for x != 0 -> PD.
sol = sp.solve([2*x1 + x2, x2], [x1, x2])
print("       zero only when", sol, "-> A1 positive definite: YES")
print("       (cross-check: leading minors", A1[0, 0], A1.det(), "; eigenvalues", list(A1.eigenvals().keys()), ")")
q2 = expand((xv.T*A2*xv)[0])
cs2 = (2*x1 + x2)**2 - x2**2
assert expand(cs2 - q2) == 0
print("p4(b): x^T A2 x =", q2, "=", cs2, "=", factor(q2))
# argument: choose 2x1+x2=0 with x2 != 0 -> value = -x2^2 < 0. e.g. x2=2, x1=-1.
xn = Matrix([-1, 2])
print("       counterexample x = [-1, 2]^T: x^T A2 x =", (xn.T*A2*xn)[0], "< 0 -> A2 NOT positive definite (indefinite)")
xn2 = Matrix([1, -4])
print("       another: x = [1,-4]^T ->", (xn2.T*A2*xn2)[0], "; general family: x = t[-1,2]^T gives", expand(q2.subs({x1: -sp.Symbol('t'), x2: 2*sp.Symbol('t')})))
print("       (cross-check: det A2 =", A2.det(), "< 0 ; eigenvalues", list(A2.eigenvals().keys()), ")")

# ---------------- P5 ----------------
hdr("P5")
v = [Matrix([0, -1, 2, 0, 2]), Matrix([1, -3, 1, -1, 2]), Matrix([-3, 4, 1, 2, 1]), Matrix([-1, -3, 5, 0, 7])]
x = Matrix([-1, -9, -1, 4, 1])
M = Matrix.hstack(*v)
r = M.rank()
print("rank of spanning set =", r, "(dim U)")
rref, piv = M.rref()
print("pivot columns:", piv)
ns = M.nullspace()
print("linear dependence (nullspace of [v1..v4]):", [n.T.tolist()[0] for n in ns])
Bas = Matrix.hstack(*[v[i] for i in piv])
# projection: pi = B (B^T B)^{-1} B^T x, B full column rank
lam = (Bas.T*Bas).solve(Bas.T*x)
pi = Bas*lam
print("p5(a): pi_U(x) =", pi.T.tolist()[0], " (coeffs w.r.t. pivot basis:", lam.T.tolist()[0], ")")
# independent check via pseudo-inverse projection matrix with all 4 vectors
P = M*(M.T*M).pinv()*M.T
assert simplify(P*x - pi) == sp.zeros(5, 1)
assert simplify(P*P - P) == sp.zeros(5, 5) and P == P.T
res = x - pi
d = sqrt(res.dot(res))
print("p5(b): residual x - pi =", res.T.tolist()[0], "; ||res||^2 =", res.dot(res), "; d(x,U) =", d, "≈", sp.N(d))
dots = [res.dot(vi) for vi in v]
print("p5(c): <x-pi, v_i> for i=1..4 =", dots, "-> all orthogonal:", all(t == 0 for t in dots))
