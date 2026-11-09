# Blind independent verification of p1..p10 (exact arithmetic, sympy).
import sys, site
# python3 -I drops the user site-packages where sympy is installed; add it explicitly.
sys.path.append(site.getuserbase() + '/lib/python/site-packages')
sys.path.append(site.getusersitepackages())
from sympy import (Matrix, Rational, symbols, factor, eye, sqrt, simplify,
                   zeros, discriminant, roots, Poly, sympify, nsimplify)
lam = symbols('lambda')

def out(pid, method, res):
    print(f"{pid} | {method} | {res}")

def cp(A):
    n = A.shape[0]
    return factor((A - lam*eye(n)).det())

def eig_info(A):
    n = A.shape[0]
    rs = roots(Poly((A - lam*eye(n)).det(), lam))
    info = []
    for ev in sorted(rs, key=lambda r: (sympify(r).as_real_imag()[0], sympify(r).as_real_imag()[1])):
        ns = (A - ev*eye(n)).nullspace()
        info.append((ev, rs[ev], [list(v) for v in ns]))
    return info

def fmt_info(info):
    return "; ".join(f"lam={ev} (alg {m}, geo {len(b)}) basis {b}" for ev, m, b in info)

def diag_check(info, n):
    s = sum(len(b) for _, _, b in info)
    return s, (s == n)

# ---------------- P1 ----------------
A = Matrix([[5,4],[1,2]])
out("p1:a", "proof", "Ax=lam x <=> (A-lam I)x=0; a nonzero solution exists iff A-lam I is singular (nontrivial nullspace, columns dependent) iff det(A-lam I)=0; if det!=0 the matrix is invertible and x=(A-lam I)^-1 0 = 0 only.")
out("p1:b", "exact", f"p(lam)={cp(A)}  -> eigenvalues 1, 6")
info = eig_info(A)
out("p1:c", "exact", fmt_info(info) + "  i.e. E1=span{[-1,1]}, E6=span{[4,1]}")
v1 = Matrix(info[0][2][0]); v6 = Matrix(info[1][2][0])
out("p1:d", "exact", f"[-1,1].[4,1] = {v1.dot(v6)} != 0 -> NOT orthogonal (A not symmetric)")

# ---------------- P2 ----------------
A = Matrix([[3,1],[0,3]])
out("p2:a", "exact", f"p(lam)={cp(A)} -> lam=3, algebraic multiplicity 2")
info = eig_info(A)
out("p2:b", "exact", fmt_info(info) + "  i.e. E3=span{[1,0]}")
out("p2:c", "exact", f"dim E3 = {len(info[0][2])} (geometric 1 < algebraic 2; A defective)")

# ---------------- P3 ----------------
A = Matrix([[4,1,1],[1,4,1],[1,1,4]])
out("p3:a", "exact", f"p(lam)={cp(A)} (given -(lam-3)^2(lam-6) matches: {simplify(cp(A) + (lam-3)**2*(lam-6))==0})")
# E3: x1 + x2 + x3 = 0, free x2,x3
x1 = Matrix([-1,1,0]); x2 = Matrix([-1,0,1])
ns6 = (A-6*eye(3)).nullspace()[0]; x3 = ns6/ns6[2]
assert (A*x1 - 3*x1) == zeros(3,1) and (A*x2 - 3*x2) == zeros(3,1) and (A*x3 - 6*x3) == zeros(3,1)
out("p3:a", "exact", f"E3: x1+x2+x3=0 -> x1={list(x1)}, x2={list(x2)} (free (x2,x3)=(1,0),(0,1)); E6=span{{x3={list(x3)}}}; sympy E3 basis {[list(v) for v in (A-3*eye(3)).nullspace()]}")
out("p3:b", "exact", f"x3.x1={x3.dot(x1)}, x3.x2={x3.dot(x2)}, x1.x2={x1.dot(x2)} -> (x3,x1),(x3,x2) orthogonal; (x1,x2) NOT")
x1p = x1
x2p = x2 - (x2.dot(x1p)/x1p.dot(x1p))*x1p
out("p3:c", "exact", f"x1'=x1={list(x1p)}, x2'=x2-(1/2)x1={list(x2p)} (scaled: {list(2*x2p)}); A x2' = 3 x2': {A*x2p==3*x2p}")
out("p3:d", "exact", f"x1'.x2'={x1p.dot(x2p)}, x1'.x3={x1p.dot(x3)}, x2'.x3={x2p.dot(x3)} -> mutually orthogonal")

# ---------------- P4 ----------------
A = Rational(1,2)*Matrix([[7,-1],[-1,7]])
out("p4:a", "exact", f"p(lam)={cp(A)} -> lam1=4, lam2=3")
p1 = (A-4*eye(2)).nullspace()[0]; p1 = p1/p1.norm()
p2 = (A-3*eye(2)).nullspace()[0]; p2 = p2/p2.norm()
out("p4:b", "exact", f"p1={list(p1)} (=[1,-1]/sqrt2, sign arbitrary), p2={list(p2)} (=[1,1]/sqrt2)")
P = p1.row_join(p2)
PtP = simplify(P.T*P)
out("p4:c", "exact", f"P^T P = {PtP.tolist()} = I -> P orthogonal, P^-1 = P^T")
D = Matrix([[4,0],[0,3]])
out("p4:d", "exact", f"D=diag(4,3); P D P^T == A : {simplify(P*D*P.T - A)==zeros(2,2)}; P={P.tolist()}")

# ---------------- P5 ----------------
A = Matrix([[1,3,5],[2,4,6],[0,2,4]])
c11 = A[1:,1:].det(); c12 = Matrix([[2,6],[0,4]]).det(); c13 = Matrix([[2,4],[0,2]]).det()
d = 1*c11 - 3*c12 + 5*c13
out("p5:a", "exact", f"det = 1*({c11}) - 3*({c12}) + 5*({c13}) = {c11} - {3*c12} + {5*c13} = {d}; sympy det={A.det()}")
nv = A.nullspace()[0]
out("p5:b", "exact", f"det=0 -> columns linearly DEPENDENT; null vector {list(nv)}: c1 - 2c2 + c3 = 0, A*v={list(A*nv)}")

# ---------------- P6 ----------------
A = Matrix([[1,0],[1,1]]); B = Matrix([[-2,2],[2,1]])
iA = eig_info(A); iB = eig_info(B)
out("p6:a", "exact", f"p(lam)={cp(A)}; " + fmt_info(iA) + "  i.e. E1=span{[0,1]} (dim1)")
out("p6:b", "exact", f"p(lam)={cp(B)}; " + fmt_info(iB) + "  i.e. E-3=span{[-2,1]}, E2=span{[1,2]}")
out("p6:c", "exact", f"[-2,1].[1,2] = {Matrix(iB[0][2][0]).dot(Matrix(iB[1][2][0]))} -> orthogonal (B symmetric)")

# ---------------- P7 ----------------
Ms = {"M1":Matrix([[1,0],[0,1]]),"M2":Matrix([[1,0],[0,0]]),"M3":Matrix([[1,1],[0,1]]),"M4":Matrix([[0,1],[0,0]])}
ra=[]; rb=[]
for k,M in Ms.items():
    info = eig_info(M); s, ok = diag_check(info, 2)
    ra.append(f"{k}: eig {[(e,m,len(b)) for e,m,b in info]} sum geo={s} -> {'diag' if ok else 'NOT diag'}")
    rb.append(f"{k}: det={M.det()} -> {'invertible' if M.det()!=0 else 'NOT invertible'}")
out("p7:a", "exact", "; ".join(ra))
out("p7:b", "exact", "; ".join(rb) + "  (M1 diag+inv, M2 diag+noninv, M3 nondiag+inv, M4 nondiag+noninv)")

# ---------------- P8 ----------------
A1 = Matrix([[2,3,0],[1,4,3],[0,0,1]])
A2 = Matrix([[1,1,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
i1 = eig_info(A1); s1, ok1 = diag_check(i1, 3)
out("p8:a", "exact", f"p(lam)={cp(A1)}; " + fmt_info(i1) + "  i.e. E1=span{[-3,1,0]}, E5=span{[1,1,0]}")
out("p8:b", "exact", f"dim sum = {s1} < 3 -> NOT diagonalizable (lam=1 alg 2, geo 1)")
i2 = eig_info(A2); s2, ok2 = diag_check(i2, 4)
out("p8:c", "exact", f"p(lam)={cp(A2)}; " + fmt_info(i2) + "  i.e. E0=span{[-1,1,0,0],[0,0,1,0],[0,0,0,1]}, E1=span{[1,0,0,0]}")
out("p8:d", "exact", f"dim sum = {s2} = 4 -> diagonalizable")

# ---------------- P9 ----------------
A1 = Matrix([[0,1],[-8,4]])
pA1 = (A1 - lam*eye(2)).det().expand()
out("p9:a", "exact", f"p(lam)={pA1}, discriminant={discriminant(pA1, lam)} < 0 -> eigenvalues {list(roots(Poly(pA1,lam)).keys())} complex; no real eigenvector -> NOT diagonalizable with real P (it IS diagonalizable over C, distinct complex eigenvalues)")
A2 = Matrix([[5,-6,-6],[-1,4,2],[3,-6,-4]])
i9 = eig_info(A2)
out("p9:b", "exact", f"p(lam)={cp(A2)}; " + fmt_info(i9))
s9, ok9 = diag_check(i9, 3)
mine = [Matrix(b) for _,_,bs in i9 for b in bs]
Pm = Matrix.hstack(*mine)
Dm = Matrix.diag(*[ev for ev,_,bs in i9 for _ in bs])
ref = [Matrix([3,-1,3]), Matrix([2,1,0]), Matrix([2,0,1])]
same = all((A2*ref[0]) == 1*ref[0] for _ in [0]) and (A2*ref[1]==2*ref[1]) and (A2*ref[2]==2*ref[2])
Pr = Matrix.hstack(*ref)
out("p9:c", "exact", f"dim sum={s9}=3 -> diagonalizable; my P={Pm.tolist()} det={Pm.det()}, D={Dm.tolist()}, P^-1 A P==D: {Pm.inv()*A2*Pm==Dm}; ordering [3,-1,3],[2,1,0],[2,0,1]: eigen-checks {same}, det={Pr.det()}, P^-1AP={ (Pr.inv()*A2*Pr).tolist() } -> D=diag(1,2,2)")

# ---------------- P10 ----------------
a = symbols('a11 a12 a13 a21 a22 a23')
A = Matrix(2,3,a)
# (a): A A^T (A x) = A (A^T A x); identity check of associativity with symbolic x
xs = Matrix(symbols('x1:4')); us = Matrix(symbols('u1:3'))
idA = simplify((A*A.T)*(A*xs) - A*((A.T*A)*xs)) == zeros(2,1)
idB = simplify((A.T*A)*(A.T*us) - A.T*((A*A.T)*us)) == zeros(3,1)
out("p10:a", "proof", f"AA^T(Ax) = A(A^T A x) = A(lam x) = lam(Ax). [aux symbolic 2x3 check AA^T(Ax)==A(A^TAx): {idA}] Ax!=0 when lam!=0 since A^TAx=lam x!=0 forces Ax!=0, so Ax is an eigenvector of AA^T for lam.")
out("p10:b", "proof", f"A^TA(A^Tu) = A^T(AA^T u) = A^T(lam u) = lam(A^T u). [aux symbolic check: {idB}] A^Tu!=0 when lam!=0 since AA^Tu=lam u!=0.")
# counterexample lam = 0
Ac = Matrix([[1,0]])  # 1x2: A^TA = [[1,0],[0,0]] has eigenvalue 0 with x=[0,1]; Ax = 0
xc = Matrix([0,1])
AtA = Ac.T*Ac; AAt = Ac*Ac.T
out("p10:c", "proof", f"Eigenvector must be nonzero. If lam=0 then A^TAx=0 can hold with Ax=0 (x in N(A), since x^TA^TAx=||Ax||^2=0), so Ax is not an eigenvector. Counterexample A=[[1,0]]: A^TA={AtA.tolist()} has lam=0 with x=[0,1], Ax={list(Ac*xc)}=0; AA^T={AAt.tolist()} has NO eigenvalue 0. For lam!=0: Ax=0 would give lam x=A^TAx=0 -> x=0, contradiction. Numeric/symbolic checks are auxiliary; the proof is the argument.")
