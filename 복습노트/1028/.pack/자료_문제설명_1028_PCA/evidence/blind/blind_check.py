from sympy import Matrix, Rational, sqrt, symbols, simplify, nsimplify

print("== P1 ==")
e1, e2 = Matrix([1,0]), Matrix([0,1])
x = Matrix([4,-7]); z = symbols('z')
assert 4*e1 + (-7)*e2 == x
print("a) x = 4 e1 - 7 e2")
assert 0*e1 + z*e2 == Matrix([0,z])
print("b) xt = 0 e1 + z e2; store only z")
print("c) U = span[e2], dim =", Matrix.hstack(e2).rank())

print("== P2 ==")
b1 = Rational(1,5)*Matrix([3,4]); b2 = Rational(1,5)*Matrix([4,-3])
print("b1.b1 =", b1.dot(b1), " b2.b2 =", b2.dot(b2), " b1.b2 =", b1.dot(b2))
print("det[b1 b2] =", Matrix.hstack(b1,b2).det(), "(nonzero -> lin. indep., 2 vectors in R^2 -> basis)")

print("== P3 ==")
V = Matrix([[0,-1,2,0,2],[1,-3,1,-1,2],[-3,4,1,2,1],[-1,-3,5,0,7]]).T
x = Matrix([-1,-9,-1,4,1])
print("rank of spanning set =", V.rank())
# pick independent columns via rref of V
piv = V.rref()[1]
B = V[:, list(piv)]
print("basis columns (indices):", piv)
# Method 1: normal equations
lam = (B.T*B).solve(B.T*x)
p1 = B*lam
print("lambda =", list(lam))
print("Method1 pi_U(x) =", list(p1))
# Method 2: Gram-Schmidt orthogonal basis, sum of 1-D projections
ortho = []
for i in range(B.shape[1]):
    v = B[:, i]
    for u in ortho:
        v = v - (u.dot(B[:, i]))/u.dot(u)*u
    ortho.append(v)
p2 = sum(((u.dot(x))/u.dot(u)*u for u in ortho), Matrix([0]*5))
print("Method2 pi_U(x) =", list(p2))
assert p1 == p2
r = x - p1
print("residual =", list(r), " V^T r =", list(V.T*r))
print("d(x,U) =", sqrt(r.dot(r)), "=", sqrt(r.dot(r)).evalf())

print("== P4 ==")
A = Matrix([[2,1,0],[1,2,-1],[0,-1,2]])
print("A sym:", A == A.T, " eigenvalues:", A.eigenvals(), " (all>0 -> pos. def.)")
ip = lambda a, b: (a.T*A*b)[0]
E = Matrix.eye(3); e2v = E[:,1]
B = Matrix.hstack(E[:,0], E[:,2])
# Method 1: generalized normal equations B^T A B lam = B^T A x
lam = (B.T*A*B).solve(B.T*A*e2v)
pA = B*lam
print("lambda =", list(lam), " Method1 pi_U(e2) =", list(pA))
# Method 2: <e1,e3>_A = 0 ? then sum of 1-D A-projections; else Gram-Schmidt
u1 = E[:,0]; u3 = E[:,2] - ip(u1,E[:,2])/ip(u1,u1)*u1
print("<e1,e3>_A =", ip(E[:,0],E[:,2]))
pB = ip(u1,e2v)/ip(u1,u1)*u1 + ip(u3,e2v)/ip(u3,u3)*u3
print("Method2 pi_U(e2) =", list(pB))
assert pA == pB
r = e2v - pA
print("residual =", list(r), " <r,e1>_A =", ip(r,E[:,0]), " <r,e3>_A =", ip(r,E[:,2]))
d = sqrt(ip(r,r))
print("d_A(e2,U) =", d, "=", d.evalf())
# contrast: Euclidean (wrong-metric) answer
print("(contrast, Euclidean dot) proj = [0,0,0], dist = 1")
