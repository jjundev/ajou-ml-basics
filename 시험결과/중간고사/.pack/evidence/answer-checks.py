"""Independent answer checks for the 2026-10-21 midterm, computed from the printed problem text only.

Run: uv run --no-project --with sympy python -I answer-checks.py  → writes answer-checks.json next to this file.
"""
import json
from pathlib import Path
import sympy as sp

R = sp.Rational
out = {}

def rec(key, conclusion, method='sympy exact'):
    out[key] = {'status': 'pass', 'method': method, 'conclusion': conclusion}

# Q1
u, v = sp.symbols('u v')
f = 2*u**2 - 2*u*v + 4*v**2 + 6*u - 2*v
grad = sp.Matrix([f.diff(u), f.diff(v)])
g1 = grad.subs({u: -1, v: 2})
assert g1 == sp.Matrix([-2, 16])
rec('p1:a', f'grad f = {list(grad)}, at (-1,2) = {list(g1)}')
g = sp.Matrix([u**2 + 2*v, u*v - v**2, 3*u - v])
J = g.jacobian([u, v])
J1 = J.subs({u: -1, v: 2})
assert J1 == sp.Matrix([[-2, 2], [2, -5], [3, -1]]) and J1.shape == (3, 2)
rec('p1:b', f'J = {J.tolist()}, J(-1,2) = {J1.tolist()}, shape 3x2')

# Q2
A = sp.Matrix([[1, 1], [1, 0], [0, 1]]); y = sp.Matrix([3, 0, 0])
AtA = A.T*A
assert AtA == sp.Matrix([[2, 1], [1, 2]]) and AtA.det() == 3
assert AtA.inv() == sp.Matrix([[R(2, 3), R(-1, 3)], [R(-1, 3), R(2, 3)]])
rec('p2:a', f'A^T A = {AtA.tolist()}, det 3, inverse {AtA.inv().tolist()}')
p = A*AtA.inv()*A.T*y; r = y - p
assert p == sp.Matrix([2, 1, 1]) and r == sp.Matrix([1, -1, -1]) and A.T*r == sp.zeros(2, 1)
rec('p2:b', 'p = (2,1,1), r = (1,-1,-1), A^T r = 0')

# Q3a
x1, x2 = sp.symbols('x1 x2', real=True)
mu = sp.Matrix([2, -2]); S = sp.Matrix([[3, 1], [1, 1]])
d = sp.Matrix([x1, x2]) - mu
quad = sp.expand((d.T*S.inv()*d)[0])
a, b = sp.symbols('a b')  # a = x1-2, b = x2+2
target = sp.expand(R(1, 2)*(a**2 - 2*a*b + 3*b**2)).subs({a: x1 - 2, b: x2 + 2})
assert sp.simplify(quad - sp.expand(target)) == 0
norm = 1/(2*sp.pi*sp.sqrt(S.det()))
assert sp.simplify(norm - 1/(2*sp.sqrt(2)*sp.pi)) == 0
dens = norm*sp.exp(-quad/2)
assert sp.simplify(sp.integrate(dens, (x1, -sp.oo, sp.oo), (x2, -sp.oo, sp.oo)) - 1) == 0
rec('p3:a', 'p(x) = 1/(2*sqrt(2)*pi) * exp(-1/4[(x1-2)^2 - 2(x1-2)(x2+2) + 3(x2+2)^2]); integrates to 1')
# Q3b
z = sp.symbols('z', real=True); c = sp.symbols('c', positive=True)
assert sp.expand(9*(z + 1)**2 + 4) == 9*z**2 + 18*z + 13
cval = sp.solve(sp.integrate(c*sp.exp(-R(1, 2)*(9*z**2 + 18*z + 13)), (z, -sp.oo, sp.oo)) - 1, c)[0]
assert sp.simplify(cval - 3*sp.exp(2)/sp.sqrt(2*sp.pi)) == 0
pz = cval*sp.exp(-R(1, 2)*(9*z**2 + 18*z + 13))
m = sp.simplify(sp.integrate(z*pz, (z, -sp.oo, sp.oo)))
var = sp.simplify(sp.integrate((z - m)**2*pz, (z, -sp.oo, sp.oo)))
assert m == -1 and var == R(1, 9)
rec('p3:b', 'c = 3e^2/sqrt(2pi), mean -1, variance 1/9')

# Q4
P = {(0, 0): R(1, 10), (0, 1): R(2, 10), (0, 2): R(1, 10), (1, 0): R(2, 10), (1, 1): R(1, 10), (1, 2): R(3, 10)}
pU = {i: sum(P[i, j] for j in range(3)) for i in range(2)}
pV = {j: sum(P[i, j] for i in range(2)) for j in range(3)}
assert pU == {0: R(2, 5), 1: R(3, 5)} and pV == {0: R(3, 10), 1: R(3, 10), 2: R(2, 5)}
rec('p4:a', 'P(U)=(4/10, 6/10), P(V)=(3/10, 3/10, 4/10)')
cond = P[1, 2]/pV[2]
assert cond == R(3, 4) and cond != pU[1] and P[1, 2] != pU[1]*pV[2]
rec('p4:b', 'P(U=1|V=2)=3/4 != P(U=1)=3/5 (also 3/10 != 6/25) -> not independent')

# Q5
prior = {R(1, 3): R(2, 3), R(2, 3): R(1, 3)}
lik = {t: t**2 for t in prior}
PD = sum(lik[t]*prior[t] for t in prior)
post = {t: lik[t]*prior[t]/PD for t in prior}
assert PD == R(2, 9) and post == {R(1, 3): R(1, 3), R(2, 3): R(2, 3)}
rec('p5:a', 'P(D)=2/9 (=6/27), posterior 1/3 and 2/3')
pred = sum(t*post[t] for t in prior)
assert max(post, key=post.get) == R(2, 3) and pred == R(5, 9)
assert sum(t*prior[t] for t in prior) == R(4, 9)  # the prior-weighted (wrong) value
rec('p5:b', 'theta_MAP=2/3, P(X3=1|D)=5/9 < plug-in 2/3 (posterior averaging keeps theta=1/3 mass); prior-weighted 4/9 is wrong')

# Q6
Phi = sp.Matrix([[1, -1], [1, 0], [1, 1]]); yy = sp.Matrix([0, 1, 3])
ml = (Phi.T*Phi).inv()*Phi.T*yy
assert ml == sp.Matrix([R(4, 3), R(3, 2)])
rec('p6:a', 'likelihood (2pi)^(-3/2) exp(-1/2||y-Phi theta||^2); Phi^T Phi theta = Phi^T y; theta_ML=(4/3, 3/2)')
mp = (Phi.T*Phi + sp.eye(2)).inv()*Phi.T*yy
assert mp == sp.Matrix([1, 1])
rec('p6:b', 'NLP = 1/2||y-Phi theta||^2 + 1/2||theta||^2 + const; (Phi^T Phi + I) theta = Phi^T y; theta_MAP=(1,1)')

# Q7
Ax = sp.Matrix([[1, 1], [2, -1]]); bvec = sp.Matrix([1, -2]); w = sp.Matrix([1, 2])
mux = sp.Matrix([2, -1]); Sx = sp.Matrix([[3, -1 - 2*(-1)], [-1 - 2*(-1), 2]])
assert Sx == sp.Matrix([[3, 1], [1, 2]])
muy = Ax*mux + bvec
assert muy == sp.Matrix([2, 3])
rec('p7:a', 'mu_x=(2,-1), Sigma_x=[[3,1],[1,2]], mu_y=(2,3)')
Sy = Ax*Sx*Ax.T + 2*w*w.T
Cxy = Sx*Ax.T
assert Sy == sp.Matrix([[9, 9], [9, 18]]) and Cxy == sp.Matrix([[4, 5], [3, 0]])
rec('p7:b', 'Sigma_y = A Sx A^T + Var(eps) w w^T = [[7,5],[5,10]] + [[2,4],[4,8]] = [[9,9],[9,18]]; C_xy = Sx A^T = [[4,5],[3,0]]')

# Q8
N = lambda zz, m_, s2: sp.exp(-(zz - m_)**2/(2*s2))/sp.sqrt(2*sp.pi*s2)
gz = N(z, 0, 1)*N(z, 2, 1)
assert sp.expand(z**2 + (z - 2)**2) == sp.expand(2*(z - 1)**2 + 2)
Z = sp.simplify(sp.integrate(gz, (z, -sp.oo, sp.oo)))
q = gz/Z
assert sp.simplify(sp.integrate(z*q, (z, -sp.oo, sp.oo))) == 1
assert sp.simplify(sp.integrate((z - 1)**2*q, (z, -sp.oo, sp.oo))) == R(1, 2)
rec('p8:a', 'z^2+(z-2)^2 = 2(z-1)^2+2, q = N(1, 1/2)')
assert sp.simplify(Z - sp.exp(-1)/sp.sqrt(4*sp.pi)) == 0 and Z != 1
rec('p8:b', f'Z = e^-1/sqrt(4pi) = {sp.N(Z, 6)} != 1 -> g is not normalized')

# Q9
Phi9 = sp.Matrix([[1, -1], [1, 1]]); y9 = sp.Matrix([1, 3])
SN = (sp.eye(2) + Phi9.T*Phi9).inv()
assert Phi9.T*Phi9 == 2*sp.eye(2) and SN == sp.eye(2)/3
rec('p9:a', 'Phi=[[1,-1],[1,1]], y=(1,3), Phi^T Phi = 2I, S_N = (I+2I)^-1 = I/3')
mN = SN*Phi9.T*y9
assert Phi9.T*y9 == sp.Matrix([4, 2]) and mN == sp.Matrix([R(4, 3), R(2, 3)])
rec('p9:b', 'Phi^T y=(4,2), m_N=(4/3, 2/3), p(theta|D)=N(m_N, I/3)')

# Q10
ph = sp.Matrix([1, 2])
mf = (ph.T*mN)[0]; vf = (ph.T*SN*ph)[0]
assert (mf, vf) == (R(8, 3), R(5, 3))
rec('p10:a', 'f* | D ~ N(8/3, 5/3) (linear map of Gaussian theta)')
assert vf + 1 == R(8, 3)
rec('p10:b', 'y* | D ~ N(8/3, 8/3): integral of N(y*|f*,1) N(theta|m_N,S_N); variance adds sigma^2=1 of fresh noise')
# method-credit values using the student's Q9 numbers (S_N=3I, m_N=(12,6))
alt = ((ph.T*sp.Matrix([12, 6]))[0], (ph.T*3*sp.eye(2)*ph)[0])
assert alt == (24, 15)
out['p10:method_credit'] = {'status': 'info', 'method': 'sympy exact', 'conclusion': 'with S_N=3I, m_N=(12,6): f* ~ N(24, 15), y* ~ N(24, 16)'}

Path(__file__).with_name('answer-checks.json').write_text(json.dumps({'items': out}, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'OK {sum(1 for k in out if k.count(":") == 1 and not k.endswith("credit"))} checks')
