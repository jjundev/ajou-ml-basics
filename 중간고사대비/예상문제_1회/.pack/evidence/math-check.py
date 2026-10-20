"""Exact arithmetic checks, separate from HTML and template rendering."""
import sympy as s
from pathlib import Path
import json
F=s.Rational;M=s.Matrix
results={}
def check(key,condition):
 assert condition,key
 results[key]='pass'
V=M([[1,0,1],[0,1,1],[1,1,2]]);U=V[:,:2];t=s.symbols('t',real=True)
check('p1:a',V*M([1,1,-1])==s.zeros(3,1))
check('p1:b',V*M([2-t,1-t,t])==M([2,1,3]) and V.row_join(M([2,1,4])).rank()>V.rank())
check('p1:c',(U.T*U).inv()==M([[2,-1],[-1,2]])/3 and (V.T*V).det()==0)
x1,x2=s.symbols('x1 x2');x=M([x1,x2]);A=M([[4,1],[1,2]]);b=M([1,0]);q=(x.T*A*x)[0]/2-(b.T*x)[0]
check('p2:a',M([x1*x1+x2,x1*x2]).jacobian(x).subs({x1:1,x2:2})==M([[2,1],[2,1]]))
check('p2:b',M([[s.diff(q,v) for v in x]])==x.T*A-b.T and s.hessian(q,x)==A)
check('p2:c',A.inv()*b==M([F(2,7),F(-1,7)]) and A.is_positive_definite)
z=s.symbols('z',real=True)
check('p3:a',s.expand(z*z+(z-2)**2/3-F(4,3)*(z-F(1,2))**2-1)==0)
check('p3:b',1/(1+F(1,3))==F(3,4) and F(3,4)*F(2,3)==F(1,2))
g=s.exp(-z*z/2-(z-2)**2/6)/(2*s.pi*s.sqrt(3))
check('p3:c',s.simplify(s.integrate(g,(z,-s.oo,s.oo))-s.exp(-F(1,2))/s.sqrt(8*s.pi))==0)
P=M([[1,-1],[1,0],[1,1]]);y=M([0,1,4]);G=P.T*P
check('p4:a',G==s.diag(3,2) and P.T*y==M([5,4]))
check('p4:b',G.inv()*P.T*y==M([F(5,3),2]) and (M([[1,2]])*G.inv()*P.T*y)[0]==F(17,3))
check('p4:c',(G+s.eye(2)).inv()*P.T*y==M([F(5,4),F(4,3)]) and (M([[1,2]])*(G+s.eye(2)).inv()*P.T*y)[0]==F(47,12))
xs=[M([0,0]),M([2,0]),M([0,2])];mu=sum(xs,s.zeros(2,1))/3;C=sum(((a-mu)*(a-mu).T for a in xs),s.zeros(2))/3;A=M([[1,1],[1,-1]]);b=M([1,-1]);ys=[A*a+b for a in xs]
check('p5:a',mu==M([F(2,3),F(2,3)]) and C==M([[8,-4],[-4,8]])/9)
check('p5:b',A*mu+b==M([F(7,3),-1]) and A*C*A.T==s.diag(F(8,9),F(8,3)) and C*A.T==M([[F(4,9),F(4,3)],[F(4,9),-F(4,3)]]))
check('p5:c',M([1,1]) not in ys and sum(a[0]==1 for a in ys)==1 and sum(a[1]==1 for a in ys)==1)

ck=check;checks=results

# New derivation checks. General sufficiency and independence proofs are separately reviewed.
a,b,z=s.symbols('a b z',real=True);v=s.symbols('v',positive=True)
Phi=M([[1,0],[1,1],[1,2]]);yy=M([1,2,2]);th=M([a,b]);G=Phi.T*Phi
Q=((yy-Phi*th).T*(yy-Phi*th))[0]
ck('derive:quadratic_gradient',M([s.diff(Q,t) for t in th])==2*Phi.T*(Phi*th-yy))
B=M([[3,1],[1,2]]);bb=M([a,b]);mm=B.inv()*bb;tt=M([z,v]);cc=s.symbols('c')
ck('derive:matrix_complete_square',s.expand((tt.T*B*tt)[0]-2*bb.dot(tt)+cc-((tt-mm).T*B*(tt-mm))[0]-cc+(bb.T*B.inv()*bb)[0])==0)

Phi=M([[1,1],[2,2]]);yy=M([1,2]);lam=s.symbols('lambda',positive=True)
theta=s.simplify((Phi.T*Phi+lam*s.eye(2)).inv()*Phi.T*yy)
ck('p7:regularized_solution',theta==M([5/(10+lam),5/(10+lam)]) and theta.subs(lam,1)==M([F(5,11),F(5,11)]))
ck('p8:scalar_square',s.expand(((z-1)**2+(2-z)**2+z*z)/2-F(3,2)*(z-1)**2-1)==0)
post=s.sqrt(3/(4*s.pi))*s.exp(-3*(z-1)**2/4)
ck('p8:normalization',s.integrate(post,(z,-s.oo,s.oo))==1)
ck('p8:predictive_variance',4*F(2,3)+2==F(14,3))
y=s.symbols('y',real=True);A=1+1/v
ck('p9:evidence_square',s.simplify((y-z)**2+z*z/v-A*(z-y/A)**2-y*y/(1+v))==0)
ck('p9:normalizer',s.simplify(s.sqrt(2*s.pi/A)/(2*s.pi*s.sqrt(v))-1/s.sqrt(2*s.pi*(1+v)))==0)
bf=s.sqrt(F(5,2));odds=bf/2
ck('p9:posterior_selection',bf>1 and odds<1 and abs(float(odds/(1+odds))-.44151844)<1e-7)
Phi=M([[1,0],[1,1],[1,-1]]);yy=M([2,2,0]);theta=(Phi.T*Phi).inv()*Phi.T*yy;P=Phi*(Phi.T*Phi).inv()*Phi.T;yh=Phi*theta;rr=yy-yh
ck('p10:solution',theta==M([F(4,3),1]) and rr==M([F(2,3),-F(1,3),-F(1,3)]) and Phi.T*rr==s.zeros(2,1))
ck('p10:projection',P==M([[2,2,2],[2,5,-1],[2,-1,5]])/6 and P*P==P and P.T==P)
u=Phi*M([a,b]);ck('p10:general_pythagoras',s.expand(((yy-u).T*(yy-u))[0]-(rr.T*rr)[0]-((yh-u).T*(yh-u))[0])==0)

Path(__file__).with_name('math-check-result.json').write_text(json.dumps({'status':'pass','revision':'row-convention-2026-10-20','checks':checks,'note':'First5 exact checks retained and rerun; new derivation identities checked. Row derivation checked separately; unchanged answers compared with previous independently solved results.'},indent=2)+'\n');print(len(checks),'exact/symbolic checks passed')
