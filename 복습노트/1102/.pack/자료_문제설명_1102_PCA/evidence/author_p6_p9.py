"""Independent check for 1102 review problems p6-p9 (MML Ex 4.5, 4.6, 4.4, 4.11).
Uses sympy exact arithmetic; p9 adds a symbolic argument check plus random numeric support."""
import random
import sympy as sp

lam = sp.symbols('lambda')
out = []
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)

def report(name, M):
    n = M.shape[0]
    cp = sp.factor((M - lam*sp.eye(n)).det())
    say(f'[{name}] det(M - lambda I) = {cp}')
    say(f'[{name}] det M = {M.det()}  -> invertible: {M.det() != 0}')
    total = 0
    for ev, am, vecs in M.eigenvects():
        gm = len(vecs)
        total += gm
        # check basis vectors by substitution
        for v in vecs:
            assert M*v == ev*v
        say(f'[{name}] lambda={ev}: alg={am}, geo={gm}, basis={[list(v) for v in vecs]}')
    say(f'[{name}] sum of eigenspace dims = {total} / n={n} -> diagonalizable: {M.is_diagonalizable()} (consistent: {(total==n)==M.is_diagonalizable()})')
    return cp

say('== p6 (Ex 4.5) ==')
Ms = {'M1': sp.Matrix([[1,0],[0,1]]), 'M2': sp.Matrix([[1,0],[0,0]]),
      'M3': sp.Matrix([[1,1],[0,1]]), 'M4': sp.Matrix([[0,1],[0,0]])}
for k, M in Ms.items():
    report(k, M)
# alternative check: 2x2 with single eigenvalue c is diagonalizable iff M == cI
for k in ('M3', 'M4'):
    c = list(Ms[k].eigenvals())[0]
    say(f'[{k}] single eigenvalue {c}; M == {c}I ? {Ms[k] == c*sp.eye(2)} -> not diagonalizable')

say('== p7 (Ex 4.6) ==')
Aa = sp.Matrix([[2,3,0],[1,4,3],[0,0,1]])
cp = report('7a', Aa)
say('[7a] expanded char poly:', sp.expand((Aa - lam*sp.eye(3)).det()))
for v, ev in (([-3,1,0],1), ([1,1,0],5)):
    say(f'[7a] A*{v} = {list(Aa*sp.Matrix(v))} = {ev}*v ? {Aa*sp.Matrix(v)==ev*sp.Matrix(v)}')
say('[7a] rank(A-I)=', (Aa-sp.eye(3)).rank(), ' rank(A-5I)=', (Aa-5*sp.eye(3)).rank())
Ab = sp.Matrix([[1,1,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
report('7b', Ab)
say('[7b] rank(A)=', Ab.rank(), ' rank(A-I)=', (Ab-sp.eye(4)).rank())
P = sp.Matrix([[1,0,0,1],[-1,0,0,0],[0,1,0,0],[0,0,1,0]])  # columns: E0 basis, E1 basis
say('[7b] det P =', P.det(), ' P^{-1} A P =', (P.inv()*Ab*P).tolist())

say('== p8 (Ex 4.4) ==')
A8 = sp.Matrix([[0,-1,1,1],[-1,1,-2,3],[2,-1,0,0],[1,-1,1,0]])
B = A8 - lam*sp.eye(4)
C = lambda i, j: sp.factor((-1)**(i+j) * B.minor_submatrix(i, j).det())
C31, C32, C33, C34 = C(2,0), C(2,1), C(2,2), C(2,3)
say('[p8] cofactors row3: C31=', C31, ' C32=', C32, ' C33=', C33, ' C34=', C34)
lap = sp.expand(2*C31 + (-1)*C32 + (-lam)*C33 + 0*C34)
say('[p8] 2C31 - C32 - lambda C33 =', lap, ' = ', sp.factor(lap))
say('[p8] matches det directly:', sp.expand(B.det() - lap) == 0)
report('p8', A8)
for ev in (-1, 1, 2):
    say(f'[p8] rank(A - ({ev})I) =', (A8 - ev*sp.eye(4)).rank())
for v, ev in (([0,1,1,0],-1), ([1,1,1,1],1), ([1,0,1,1],2)):
    say(f'[p8] A*{v} = {list(A8*sp.Matrix(v))}  ({ev}*v ? {A8*sp.Matrix(v)==ev*sp.Matrix(v)})')
say('[p8] det A =', A8.det(), ' product of eigenvalues with alg. mult. (-1)^2*1*2 =', (-1)**2*1*2)
say('[p8] trace A =', A8.trace(), ' sum of eigenvalues -1-1+1+2 =', -1-1+1+2)
# row reductions in the explanation
say('[p8] rref(A+I)=', (A8+sp.eye(4)).rref()[0].tolist())
say('[p8] rref(A-I)=', (A8-sp.eye(4)).rref()[0].tolist())
say('[p8] rref(A-2I)=', (A8-2*sp.eye(4)).rref()[0].tolist())

# minors used in the explanation (rows 1,2,4 kept)
M31 = sp.Matrix([[-1,1,1],[1-lam,-2,3],[-1,1,-lam]])
M32 = sp.Matrix([[-lam,1,1],[-1,-2,3],[1,1,-lam]])
M33 = sp.Matrix([[-lam,-1,1],[-1,1-lam,3],[1,-1,-lam]])
say('[p8] minors: det M31 =', sp.factor(M31.det()), ' det M32 =', sp.factor(M32.det()), ' det M33 =', sp.factor(M33.det()))
say('[p8] minors equal submatrices:', M31 == B.minor_submatrix(2,0), M32 == B.minor_submatrix(2,1), M33 == B.minor_submatrix(2,2))
br = sp.expand(-2*(lam+1) - 2*(lam-2) + lam*(lam**2-2*lam+3))
say('[p8] bracket after factoring (lambda+1):', br, '=', sp.factor(br))
say('[p8] det = (lambda+1)*bracket ?', sp.expand((lam+1)*br - B.det()) == 0)
# row-reduction intermediates shown in the explanation: same row space as the start matrix
def same_rows(X, Y):
    return X.rref()[0] == Y.rref()[0]
I4 = sp.eye(4)
steps = {
 'A+I step1': sp.Matrix([[1,-1,1,1],[0,1,-1,4],[0,1,-1,-2],[0,0,0,0]]),
 'A+I step2': sp.Matrix([[1,-1,1,1],[0,1,-1,4],[0,0,0,-6],[0,0,0,0]]),
}
for k, X in steps.items(): say(f'[p8] {k} row-equivalent to A+I:', same_rows(X, A8+I4))
steps = {
 'A-I step1': sp.Matrix([[-1,-1,1,1],[0,1,-3,2],[0,-3,1,2],[0,-2,2,0]]),
 'A-I step2': sp.Matrix([[-1,-1,1,1],[0,1,-3,2],[0,0,-8,8],[0,0,-4,4]]),
 'A-I step3': sp.Matrix([[-1,-1,1,1],[0,1,-3,2],[0,0,-8,8],[0,0,0,0]]),
}
for k, X in steps.items(): say(f'[p8] {k} row-equivalent to A-I:', same_rows(X, A8-I4))
steps = {
 'A-2I step1': sp.Matrix([[1,-1,1,-2],[0,1,-1,1],[0,-2,-1,1],[0,1,-4,4]]),
 'A-2I step2': sp.Matrix([[1,-1,1,-2],[0,1,-1,1],[0,0,-3,3],[0,0,-3,3]]),
 'A-2I step3': sp.Matrix([[1,-1,1,-2],[0,1,-1,1],[0,0,-3,3],[0,0,0,0]]),
}
for k, X in steps.items(): say(f'[p8] {k} row-equivalent to A-2I:', same_rows(X, A8-2*I4))
# geometric multiplicities equal for nonzero eigenvalues (supplement): check on random cases below via ranks
# pitfall claim: dropping the (-1)^(3+2) sign on C32 gives constant term -6 != det A = 2
wrong = sp.expand(2*C31 + C32 - lam*C33)
say('[p8] sign-dropped expansion at lambda=0:', wrong.subs(lam, 0), ' (correct value det A =', A8.det(), ')')
# p7(b) P with the eigenvector sign used in the explanation
Pb = sp.Matrix([[-1,0,0,1],[1,0,0,0],[0,1,0,0],[0,0,1,0]])
say('[7b] explanation P: det =', Pb.det(), ' P^{-1}AP =', (Pb.inv()*Ab*Pb).tolist())
say('== p9 (Ex 4.11) ==')
# symbolic: the key identity (A A^T)(A x) = A (A^T A x) holds for generic symbolic A, x
m, n = 2, 3
Asym = sp.Matrix(m, n, sp.symbols(f'a0:{m*n}'))
x = sp.Matrix(n, 1, sp.symbols(f'x0:{n}'))
say('[p9] (A A^T)(A x) - A (A^T A x) == 0 symbolically:', sp.simplify((Asym*Asym.T)*(Asym*x) - Asym*((Asym.T*Asym)*x)) == sp.zeros(m,1))
u = sp.Matrix(m, 1, sp.symbols(f'u0:{m}'))
say('[p9] (A^T A)(A^T u) - A^T (A A^T u) == 0 symbolically:', sp.simplify((Asym.T*Asym)*(Asym.T*u) - Asym.T*((Asym*Asym.T)*u)) == sp.zeros(n,1))
# exact rational support: random integer matrices of several shapes
random.seed(1102)
def nonzero_spec(M):
    # numeric nonzero eigenvalues (real, since M is symmetric), rounded, as a sorted list with multiplicity
    # strip exact factors of lambda (zero eigenvalues) first, then find the remaining roots numerically
    q = sp.Poly(M.charpoly(lam).as_expr(), lam)
    while q.degree() > 0 and q.eval(0) == 0:
        q = sp.Poly(sp.quo(q.as_expr(), lam), lam)
    roots = q.nroots(n=15, maxsteps=200) if q.degree() > 0 else []
    return sorted(round(float(sp.re(r)), 8) for r in roots)
ok = True
for (mm, nn) in [(2,3),(3,2),(3,3),(1,4),(4,2),(2,4)]:
    for _ in range(3):
        A = sp.Matrix(mm, nn, lambda i, j: random.randint(-3, 3))
        s1 = nonzero_spec(A.T*A); s2 = nonzero_spec(A*A.T)
        # compare via char polys after removing lambda factors
        p1 = sp.Poly((A.T*A).charpoly(lam).as_expr(), lam); p2 = sp.Poly((A*A.T).charpoly(lam).as_expr(), lam)
        rel = sp.expand(lam**mm * p1.as_expr() - lam**nn * p2.as_expr())
        same = (rel == 0)
        ok &= same
        ok &= (s1 == s2)
        for ev in [r for r in sp.roots(sp.Poly((A.T*A).charpoly(lam).as_expr(), lam), filter='Q') if r != 0]:  # rational nonzero eigenvalues only (fast exact rank)
            g1 = nn - (A.T*A - ev*sp.eye(nn)).rank(); g2 = mm - (A*A.T - ev*sp.eye(mm)).rank()
            ok &= (g1 == g2)
        say(f'[p9] A {mm}x{nn} rank={A.rank()}: lambda^m p_AtA = lambda^n p_AAt ? {same}; nonzero eig equal ? {s1 == s2} {s1}')
say('[p9] all random checks pass:', ok)
# zero eigenvalue need not be shared: A = [1 1]
A = sp.Matrix([[1, 1]])
say('[p9] A=[1,1]: eig(A^T A)=', (A.T*A).eigenvals(), ' eig(A A^T)=', (A*A.T).eigenvals())
