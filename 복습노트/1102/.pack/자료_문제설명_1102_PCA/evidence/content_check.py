"""content review check for 문제설명_1102_PCA: recompute every answer and intermediate numeric claim in p1..p9 explanations."""
import sympy as sp, random
from sympy import Matrix, Rational as Q, symbols, factor, expand, sqrt, eye, zeros
lam=symbols('lambda'); ok=[]
def chk(name,cond):
    ok.append((name,bool(cond))); print(("PASS " if cond else "FAIL ")+name)
def cp(A): return factor((A-lam*eye(A.shape[0])).det())
def ns(A,l): return (A-l*eye(A.shape[0])).nullspace()
def same_span(vs,ws):
    return Matrix.hstack(*vs).rank()==Matrix.hstack(*ws).rank()==Matrix.hstack(*vs,*ws).rank()
# p1
A=Matrix([[5,4],[1,2]])
chk("p1 b charpoly (l-6)(l-1)", expand(cp(A)-(lam-6)*(lam-1))==0)
chk("p1 c E6=span[4,1]", same_span(ns(A,6),[Matrix([4,1])]))
chk("p1 c E1=span[1,-1]", same_span(ns(A,1),[Matrix([1,-1])]))
chk("p1 verify A[4,1]=[24,6]", A*Matrix([4,1])==Matrix([24,6]))
chk("p1 verify det A=6, det(A-6I)=0", A.det()==6 and (A-6*eye(2)).det()==0)
# p2
A=Matrix([[3,1],[0,3]])
chk("p2 a (l-3)^2", expand(cp(A)-(lam-3)**2)==0)
chk("p2 b E3=span[1,0], dim1", len(ns(A,3))==1 and same_span(ns(A,3),[Matrix([1,0])]))
chk("p2 rank(A-3I)=1, not diag", (A-3*eye(2)).rank()==1 and not A.is_diagonalizable())
chk("p2 A[0,1]=[1,3]", A*Matrix([0,1])==Matrix([1,3]))
# p3
A=Matrix([[4,1,1],[1,4,1],[1,1,4]])
chk("p3 charpoly -(l-3)^2(l-6)", expand(cp(A)+(lam-3)**2*(lam-6))==0)
x1,x2,x3=Matrix([-1,1,0]),Matrix([-1,0,1]),Matrix([1,1,1])
chk("p3 a E3", same_span(ns(A,3),[x1,x2]) and len(ns(A,3))==2)
chk("p3 a E6", same_span(ns(A,6),[x3]))
chk("p3 b dots", x3.dot(x1)==0 and x3.dot(x2)==0 and x1.dot(x2)==1)
x2p=x2-Q(1,2)*x1
chk("p3 c x2'=[-1/2,-1/2,1]", x2p==Matrix([Q(-1,2),Q(-1,2),1]))
chk("p3 c orth & eig", x1.dot(x2p)==0 and x3.dot(x2p)==0 and A*x2p==3*x2p)
chk("p3 verify Ax1=[-3,3,0], Ax2'=[-3/2,-3/2,3]", A*x1==Matrix([-3,3,0]) and A*x2p==Matrix([Q(-3,2),Q(-3,2),3]))
P=Matrix.hstack(x1/x1.norm(),x2p/x2p.norm(),x3/x3.norm())
chk("p3 P^TP=I, PDP^T=A, 2/sqrt6 normalizer", sp.simplify(P.T*P-eye(3))==zeros(3) and sp.simplify(P*sp.diag(3,3,6)*P.T-A)==zeros(3) and sp.simplify(x2p.norm()-sqrt(6)/2)==0)
chk("p3 cos angle x1,x2 = 1/2", x1.dot(x2)/(x1.norm()*x2.norm())==Q(1,2))
# p4
A=Q(1,2)*Matrix([[7,-1],[-1,7]])
chk("p4 a (l-4)(l-3)", expand(cp(A)-(lam-4)*(lam-3))==0)
p1v=Matrix([1,-1])/sqrt(2); p2v=Matrix([1,1])/sqrt(2)
chk("p4 a Ap1=4p1, Ap2=3p2", sp.simplify(A*p1v-4*p1v)==zeros(2,1) and sp.simplify(A*p2v-3*p2v)==zeros(2,1))
P=Matrix.hstack(p1v,p2v)
chk("p4 b det P = 1", sp.simplify(P.det())==1)
chk("p4 c P^-1 A P = diag(4,3), P^-1=P^T", sp.simplify(P.inv()*A*P-sp.diag(4,3))==zeros(2) and sp.simplify(P.inv()-P.T)==zeros(2))
chk("p4 c PD = 1/sqrt2[[4,3],[-4,3]]", sp.simplify(P*sp.diag(4,3)-Matrix([[4,3],[-4,3]])/sqrt(2))==zeros(2))
chk("p4 pitfall unnormalized P^TP=2I", Matrix([[1,1],[-1,1]]).T*Matrix([[1,1],[-1,1]])==2*eye(2))
chk("p4 pitfall eig of [[7,-1],[-1,7]] = 8,6", set(Matrix([[7,-1],[-1,7]]).eigenvals())=={8,6})
# p5
A=Matrix([[1,0],[1,1]]); B=Matrix([[-2,2],[2,1]])
chk("p5 a (1-l)^2, E1=span[0,1]", expand(cp(A)-(1-lam)**2)==0 and len(ns(A,1))==1 and same_span(ns(A,1),[Matrix([0,1])]))
chk("p5 b (l-2)(l+3)", expand(cp(B)-(lam-2)*(lam+3))==0)
chk("p5 b E2, E-3", same_span(ns(B,2),[Matrix([1,2])]) and same_span(ns(B,-3),[Matrix([-2,1])]))
chk("p5 b B[-2,1]=[6,-3]", B*Matrix([-2,1])==Matrix([6,-3]))
# p6
Ms=[Matrix([[1,0],[0,1]]),Matrix([[1,0],[0,0]]),Matrix([[1,1],[0,1]]),Matrix([[0,1],[0,0]])]
res=[(M.is_diagonalizable(), M.det()!=0) for M in Ms]
chk("p6 (diag,inv) = (T,T),(T,F),(F,T),(F,F)", res==[(True,True),(True,False),(False,True),(False,False)])
chk("p6 M3,M4 eigenspace span[1,0]", same_span(ns(Ms[2],1),[Matrix([1,0])]) and same_span(ns(Ms[3],0),[Matrix([1,0])]))
# p7
A=Matrix([[2,3,0],[1,4,3],[0,0,1]])
chk("p7 a charpoly -(l-1)^2(l-5)", expand(cp(A)+(lam-1)**2*(lam-5))==0)
chk("p7 a E1=span[-3,1,0], E5=span[1,1,0]", len(ns(A,1))==1 and same_span(ns(A,1),[Matrix([-3,1,0])]) and same_span(ns(A,5),[Matrix([1,1,0])]))
chk("p7 a rank(A-I)=2, det A=5, tr=7, not diag", (A-eye(3)).rank()==2 and A.det()==5 and A.trace()==7 and not A.is_diagonalizable())
A=Matrix([[1,1,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
chk("p7 b charpoly (l-1)l^3", expand(cp(A)-(lam-1)*lam**3)==0)
chk("p7 b E0 3-dim, E1 span e1", same_span(ns(A,0),[Matrix([-1,1,0,0]),Matrix([0,0,1,0]),Matrix([0,0,0,1])]) and same_span(ns(A,1),[Matrix([1,0,0,0])]))
P=Matrix([[-1,0,0,1],[1,0,0,0],[0,1,0,0],[0,0,1,0]])
chk("p7 b det P=-1, P^-1AP=diag(0,0,0,1)", P.det()==-1 and P.inv()*A*P==sp.diag(0,0,0,1) and A.is_diagonalizable())
chk("p7 b rank(A-I)=3", (A-eye(4)).rank()==3)
# p8
A=Matrix([[0,-1,1,1],[-1,1,-2,3],[2,-1,0,0],[1,-1,1,0]])
M=A-lam*eye(4)
def C(i,j): return factor((-1)**(i+j)*M.minor_submatrix(i-1,j-1).det())
chk("p8 C31=-(l+1)^2", expand(C(3,1)+(lam+1)**2)==0)
chk("p8 C32=2(l-2)(l+1)", expand(C(3,2)-2*(lam-2)*(lam+1))==0)
chk("p8 C33=-(l+1)(l^2-2l+3)", expand(C(3,3)+(lam+1)*(lam**2-2*lam+3))==0)
chk("p8 minor for C32 = -2(l-2)(l+1)", expand(M.minor_submatrix(2,1).det()+2*(lam-2)*(lam+1))==0)
chk("p8 charpoly expansion & factor", expand(M.det()-(lam**4-lam**3-3*lam**2+lam+2))==0 and expand(M.det()-(lam+1)**2*(lam-1)*(lam-2))==0)
chk("p8 2C31-C32-lC33 = det", expand(2*C(3,1)-C(3,2)-lam*C(3,3)-M.det())==0)
chk("p8 pitfall: sign error on C32 gives const -6", expand(2*C(3,1)+C(3,2)-lam*C(3,3)).subs(lam,0)==-6)
for l,v in [(-1,[0,1,1,0]),(1,[1,1,1,1]),(2,[1,0,1,1])]:
    chk(f"p8 E{l}=span{v}, rank 3", (A-l*eye(4)).rank()==3 and same_span(ns(A,l),[Matrix(v)]))
# row-reduction intermediates (row-equivalent check)
def roweq(X,Y): return X.rref()[0]==Y.rref()[0]
chk("p8 l=-1 echelon", roweq(A+eye(4),Matrix([[1,-1,1,1],[0,1,-1,4],[0,0,0,-6],[0,0,0,0]])))
chk("p8 l=-1 middle", roweq(A+eye(4),Matrix([[1,-1,1,1],[0,1,-1,4],[0,1,-1,-2],[0,0,0,0]])))
X=A-eye(4); Y=Matrix([X.row(0), X.row(1)-X.row(0), X.row(2)+2*X.row(0), X.row(3)+X.row(0)])
chk("p8 l=1 step1 rows", Y==Matrix([[-1,-1,1,1],[0,1,-3,2],[0,-3,1,2],[0,-2,2,0]]))
Z=Matrix([Y.row(0),Y.row(1),Y.row(2)+3*Y.row(1),Y.row(3)+2*Y.row(1)])
chk("p8 l=1 step2 rows", Z==Matrix([[-1,-1,1,1],[0,1,-3,2],[0,0,-8,8],[0,0,-4,4]]))
X=A-2*eye(4); r4=X.row(3)
Y=Matrix([r4,(X.row(0)+2*r4)/(-3),X.row(1)+r4,X.row(2)-2*r4])
chk("p8 l=2 step1 rows (as described)", Y==Matrix([[1,-1,1,-2],[0,1,-1,1],[0,-2,-1,1],[0,1,-4,4]]))
Z=Matrix([Y.row(0),Y.row(1),Y.row(2)+2*Y.row(1),Y.row(3)-Y.row(1)])
chk("p8 l=2 step2 rows", Z==Matrix([[1,-1,1,-2],[0,1,-1,1],[0,0,-3,3],[0,0,-3,3]]))
chk("p8 det=2 tr=1, not diag", A.det()==2 and A.trace()==1 and not A.is_diagonalizable())
# p9
a=Matrix(2,3,symbols('a0:6')); x=Matrix(3,1,symbols('x0:3'))
chk("p9 (AA^T)(Ax)=A(A^TAx) symbolic", expand((a*a.T)*(a*x)-a*(a.T*a*x))==zeros(2,1))
A1=Matrix([[1,1]])
chk("p9 counterexample [1,1]: eig A^TA {2,0}, AA^T {2}", set((A1.T*A1).eigenvals())=={0,2} and set((A1*A1.T).eigenvals())=={2})
random.seed(1102); cnt=0
for m,n in [(2,3),(3,2),(3,3),(2,4),(4,2),(1,3)]*3:
    R_=Matrix(m,n,lambda i,j:random.randint(-3,3))
    e1={k:v for k,v in (R_.T*R_).eigenvals().items() if k!=0}; e2={k:v for k,v in (R_*R_.T).eigenvals().items() if k!=0}
    cnt+= (e1==e2)
chk(f"p9 random 18 matrices nonzero eig (with alg mult) equal: {cnt}/18", cnt==18)
print("TOTAL", sum(o for _,o in ok), "/", len(ok))
