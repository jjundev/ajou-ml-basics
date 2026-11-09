"""Author-side exact check of every numeric claim written in explanations/p1..p10
(solve, verify, pitfall, sum). Independent of the card's reference answers."""
import json, sys
from sympy import Matrix, Rational as R, symbols, factor, expand, sqrt, eye, simplify, zeros, diag, MatrixSymbol
l = symbols('lambda')
out = {}
def rec(k, ok, note):
    out[k] = {"ok": bool(ok), "note": note}
    print(("PASS " if ok else "FAIL ") + k + " | " + note)

def cp(M): return factor((M - l*eye(M.shape[0])).det())

# p1
A = Matrix([[5,4],[1,2]])
rec("p1:a", A.det()==6 and (A-6*eye(2)).det()==0, "det A=6!=0 (lambda=0 not eigen), det(A-6I)=0")
rec("p1:b", expand(cp(A)-(l-6)*(l-1))==0 and 6*1==A.det(), "p=(l-6)(l-1); product 6 = det A")
rec("p1:c", A*Matrix([4,1])==6*Matrix([4,1]) and A*Matrix([1,-1])==Matrix([1,-1]) and (A-6*eye(2)).nullspace()[0].cross if False else (A*Matrix([4,1])==6*Matrix([4,1]) and A*Matrix([1,-1])==Matrix([1,-1]) and len((A-6*eye(2)).nullspace())==1 and len((A-eye(2)).nullspace())==1), "A[4,1]=6[4,1], A[1,-1]=[1,-1], each nullspace dim 1")
rec("p1:d", Matrix([4,1]).dot(Matrix([1,-1]))==3 and Matrix([8,2]).dot(Matrix([-1,1]))==-6 and A!=A.T, "dot=3, scaled -6, A not symmetric")
# p2
A = Matrix([[3,1],[0,3]])
rec("p2:a", expand(cp(A)-(l-3)**2)==0 and A.det()==9, "p=(l-3)^2, det=9 const term")
ns = (A-3*eye(2)).nullspace()
rec("p2:b", len(ns)==1 and ns[0]==Matrix([1,0]) and A*Matrix([0,1])==Matrix([1,3]), "E3=span[1,0]; A[0,1]=[1,3]")
rec("p2:c", len(ns)==1, "dim E3=1")
# p3
A = Matrix([[4,1,1],[1,4,1],[1,1,4]])
x1,x2,x3 = Matrix([-1,1,0]),Matrix([-1,0,1]),Matrix([1,1,1])
rec("p3:a", expand(cp(A)+(l-3)**2*(l-6))==0 and A*x1==3*x1 and A*x2==3*x2 and A*x3==6*x3 and len((A-3*eye(3)).nullspace())==2 and len((A-6*eye(3)).nullspace())==1, "p=-(l-3)^2(l-6); generators verified; dims 2,1")
rec("p3:b", x3.dot(x1)==0 and x3.dot(x2)==0 and x1.dot(x2)==1, "x3.x1=0, x3.x2=0, x1.x2=1")
c = x1.dot(x2)/x1.dot(x1); x2p = x2 - c*x1
wrong = x2 - x1.dot(x2)*x1
rec("p3:c", c==R(1,2) and x2p==Matrix([R(-1,2),R(-1,2),1]) and A*x2p==3*x2p and x1.dot(x2p)==0 and wrong==Matrix([0,-1,1]) and wrong.dot(x1)==-1, "c=1/2, x2'=[-1/2,-1/2,1], Ax2'=3x2', pitfall no-denominator gives [0,-1,1] with dot -1")
P = Matrix.hstack(x1/sqrt(2), x2p/sqrt(x2p.dot(x2p)), x3/sqrt(3))
rec("p3:d", x1.dot(x2p)==0 and x1.dot(x3)==0 and x2p.dot(x3)==0 and x2p.dot(x2p)==R(3,2) and simplify(P.T*P)==eye(3) and simplify(P*diag(3,3,6)*P.T-A)==zeros(3,3), "all dots 0; |x2'|^2=3/2; normalized P^TP=I, P diag(3,3,6) P^T=A")
# p4
A = R(1,2)*Matrix([[7,-1],[-1,7]])
p1v,p2v = Matrix([1,-1])/sqrt(2), Matrix([1,1])/sqrt(2)
P = Matrix.hstack(p1v,p2v); D = diag(4,3)
rec("p4:a", expand(cp(A)-(l-4)*(l-3))==0 and A.det()==12, "p=(l-4)(l-3); det=12=4*3")
rec("p4:b", A*Matrix([1,-1])==4*Matrix([1,-1]) and A*Matrix([1,1])==3*Matrix([1,1]) and p1v.dot(p1v)==1, "eigvecs and unit length")
rec("p4:c", simplify(P.T*P)==eye(2) and simplify(P*P.T)==eye(2), "P^TP=PP^T=I")
alt = simplify(P*diag(3,4)*P.T)
rec("p4:d", simplify(P*D*P.T-A)==zeros(2,2) and simplify(P*D)==Matrix([[4,3],[-4,3]])/sqrt(2) and alt==R(1,2)*Matrix([[7,1],[1,7]]) and set(Matrix([[7,-1],[-1,7]]).eigenvals())=={8,6}, "PDP^T=A; PD; pitfall diag(3,4)->1/2[[7,1],[1,7]]; missing 1/2 -> 8,6")
# p5
A = Matrix([[1,3,5],[2,4,6],[0,2,4]])
m = [Matrix([[4,6],[2,4]]).det(), Matrix([[2,6],[0,4]]).det(), Matrix([[2,4],[0,2]]).det()]
rec("p5:a", m==[4,8,4] and 1*4-3*8+5*4==0==A.det() and 4+24+20==48, "minors 4,8,4; det 0; sign pitfall 48")
c1,c2,c3 = A[:,0],A[:,1],A[:,2]
rec("p5:b", A*Matrix([1,-2,1])==zeros(3,1) and c1+c3==2*c2 and -c1+2*c2==c3 and all(Matrix.hstack(u,v).rank()==2 for u,v in [(c1,c2),(c1,c3),(c2,c3)]), "null [1,-2,1]; c3=-c1+2c2; no two columns proportional")
# p6
A = Matrix([[1,0],[1,1]]); B = Matrix([[-2,2],[2,1]])
nsA = (A-eye(2)).nullspace()
rec("p6:a", expand(cp(A)-(l-1)**2)==0 and len(nsA)==1 and nsA[0]==Matrix([0,1]) and A*Matrix([1,0])==Matrix([1,1]), "E1=span[0,1], A[1,0]=[1,1]")
rec("p6:b", expand(cp(B)-(l-2)*(l+3))==0 and expand((-2-l)*(1-l)-(l**2+l-2))==0 and B*Matrix([1,2])==2*Matrix([1,2]) and B*Matrix([-2,1])==-3*Matrix([-2,1]) and B.det()==-6, "p=(l-2)(l+3); eigvecs; det -6")
rec("p6:c", Matrix([1,2]).dot(Matrix([-2,1]))==0 and B==B.T and A!=A.T, "dot 0, B symmetric")
# p7
Ms = [Matrix([[1,0],[0,1]]),Matrix([[1,0],[0,0]]),Matrix([[1,1],[0,1]]),Matrix([[0,1],[0,0]])]
rec("p7:a", [M.is_diagonalizable() for M in Ms]==[True,True,False,False] and Ms[2]*Matrix([0,1])==Matrix([1,1]) and Ms[3]*Matrix([0,1])==Matrix([1,0]), "diag: T,T,F,F")
rec("p7:b", [M.det() for M in Ms]==[1,0,1,0] and Ms[2]*Matrix([[1,-1],[0,1]])==eye(2) and Ms[1]*Matrix([0,1])==zeros(2,1), "det 1,0,1,0; M3 inverse; M2 null vec")
# p8
A1 = Matrix([[2,3,0],[1,4,3],[0,0,1]])
A2 = Matrix([[1,1,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
rec("p8:a", expand(cp(A1)+(l-1)**2*(l-5))==0 and A1*Matrix([-3,1,0])==Matrix([-3,1,0]) and A1*Matrix([1,1,0])==5*Matrix([1,1,0]) and len((A1-eye(3)).nullspace())==1 and len((A1-5*eye(3)).nullspace())==1, "p=-(l-1)^2(l-5); E1,E5 dim1")
rec("p8:b", not A1.is_diagonalizable(), "not diagonalizable (sum 2<3)")
P = Matrix.hstack(Matrix([1,-1,0,0]),Matrix([0,0,1,0]),Matrix([0,0,0,1]),Matrix([1,0,0,0]))
minor2 = Matrix([[0,0,0],[0,-l,0],[0,0,-l]]).det()
rec("p8:c", expand(cp(A2)-l**3*(l-1))==0 and minor2==0 and len(A2.nullspace())==3 and len((A2-eye(4)).nullspace())==1 and A2*P[:,0]==zeros(4,1), "p=l^3(l-1); second minor 0; dims 3,1")
rec("p8:d", P.det()!=0 and A2*P==P*diag(0,0,0,1) and A2.is_diagonalizable(), "P invertible, A2 P = P diag(0,0,0,1)")
# p9
A1 = Matrix([[0,1],[-8,4]])
A2 = Matrix([[5,-6,-6],[-1,4,2],[3,-6,-4]])
rec("p9:a", expand(cp(A1)-(l**2-4*l+8))==0 and (-4)**2-4*8==-16 and expand(l**2-4*l+8-((l-2)**2+4))==0 and (-4)**2-4*(-8)==48 and all(not ev.is_real for ev in A1.eigenvals()), "p=l^2-4l+8, disc -16, (l-2)^2+4, pitfall disc 48, no real eigenvalue")
d1 = Matrix([[4-l,2],[-6,-4-l]]).det(); d2 = Matrix([[-1,2],[3,-4-l]]).det(); d3 = Matrix([[-1,4-l],[3,-6]]).det()
rec("p9:b", expand(d1-(l**2-4))==0 and expand(d2-(l-2))==0 and expand(d3-(3*l-6))==0 and expand(cp(A2)+(l-1)*(l-2)**2)==0 and A2*Matrix([3,-1,3])==Matrix([3,-1,3]) and A2*Matrix([2,1,0])==Matrix([4,2,0]) and A2*Matrix([2,0,1])==Matrix([4,0,2]) and len((A2-2*eye(3)).nullspace())==2, "minors l^2-4, l-2, 3l-6; p=-(l-1)(l-2)^2; eigvecs; dim E2=2")
P = Matrix([[3,2,2],[-1,1,0],[3,0,1]])
rec("p9:c", P.det()==-1 and P.inv()*A2*P==diag(1,2,2) and A2.det()==4, "det P=-1, P^-1 A2 P = diag(1,2,2), det A2=4")
# p10 (auxiliary numeric; proof is argument)
a = symbols('a0:6'); Ag = Matrix(2,3,a); xs = Matrix(symbols('y0:3')); us = Matrix(symbols('w0:2'))
Ae = Matrix([[1,1],[0,1],[1,0]])
rec("p10:a", expand(Ag*(Ag.T*Ag*xs) - (Ag*Ag.T)*(Ag*xs))==zeros(2,1) and Ae.T*Ae==Matrix([[2,1],[1,2]]) and Ae*Ae.T*(Ae*Matrix([1,1]))==3*(Ae*Matrix([1,1])), "associativity identity symbolic 2x3; example lambda=3")
rec("p10:b", expand(Ag.T*(Ag*Ag.T*us) - (Ag.T*Ag)*(Ag.T*us))==zeros(3,1) and Ae.T*Matrix([2,1,1])==Matrix([3,3]) and Ae.T*Ae*Matrix([3,3])==Matrix([9,9]), "symbolic identity; example")
Ac = Matrix([[1,0]])
rec("p10:c", Ac.T*Ac==Matrix([[1,0],[0,0]]) and Ac*Ac.T==Matrix([[1]]) and Ac*Matrix([0,1])==zeros(1,1) and (Ac.T*Ac)*Matrix([0,1])==zeros(2,1), "counterexample A=[1,0]; proof by contradiction is the argument")
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("ALL PASS" if all(v["ok"] for v in out.values()) else "SOME FAIL", len(out))
