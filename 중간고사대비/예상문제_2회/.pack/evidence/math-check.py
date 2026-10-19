import sympy as s,json
from pathlib import Path
M=s.Matrix;F=s.Rational;checks={}
def ck(k,v):
 assert v,k
 checks[k]='pass'
t,z,x1,x2,h=s.symbols('t z x1 x2 h',real=True);x=M([x1,x2])
V=M([[1,0,1],[0,1,1],[1,1,t]])
ck('p1:a',V.det()==t-2);ck('p1:b',V.subs(t,2)*M([1-z,2-z,z])==M([1,2,3]) and V.subs(t,2).row_join(M([1,2,4])).rank()==3);ck('p1:c',V.subs(t,3)*M([0,1,1])==M([1,2,4]))
f=M([x1+x2,x1*x2]);J=f.jacobian(x);L=((f-M([1,2])).T*(f-M([1,2])))[0]/2;grad=M([s.diff(L,v) for v in x]);subs={x1:1,x2:2}
ck('p2:a',J.subs(subs)==M([[1,1],[2,1]]));ck('p2:b',grad.subs(subs)==M([2,2]) and s.simplify(grad-J.T*(f-M([1,2])))==s.zeros(2,1));ck('p2:c',s.diff(L.subs({x1:1+h,x2:2-h}),h).subs(h,0)==0)
A=M([[1,1],[1,-1]]);C=M([[2,1],[1,2]]);mu=M([1,-1]);CY=A*C*A.T
ck('p3:a',CY==s.diag(6,2) and A*mu+M([0,2])==M([0,4]));ck('p3:b',1/(2*s.pi*s.sqrt(CY.det()))==1/(4*s.pi*s.sqrt(3)))
ck('p4:a',s.expand((z+1)**2/2+(3-z)**2/2-(z-1)**2-4)==0)
g=s.exp(-((z+1)**2+(3-z)**2)/4)/(4*s.pi);Z=s.exp(-2)/s.sqrt(8*s.pi)
ck('p4:bc',s.simplify(s.integrate(g,(z,-s.oo,s.oo))-Z)==0 and s.simplify(g/Z-s.exp(-(z-1)**2/2)/s.sqrt(2*s.pi))==0)
Phi=M([[1,1],[1,0],[1,1]]);y=M([2,0,4]);G=Phi.T*Phi;cross=Phi.T*y;ml=G.inv()*cross;mp=(G+s.eye(2)).inv()*cross;r=y-Phi*ml
ck('p5:a',G==M([[3,2],[2,2]]) and cross==M([6,6]));ck('p5:b',ml==M([0,3]) and Phi.T*r==s.zeros(2,1) and r.dot(r)==2 and (M([[1,4]])*ml)[0]==12);ck('p5:c',mp==M([F(3,4),F(3,2)]) and (M([[1,4]])*mp)[0]==F(27,4))
N,S,v=s.symbols('N S v',positive=True);nll=N*s.log(2*s.pi*v)/2+S/(2*v)
ck('p6:a',s.simplify(s.diff(nll,v)-(N*v-S)/(2*v*v))==0 and s.simplify(s.diff(nll,v).subs(v,S/N))==0)
rr=M([1,2,6])-3*s.ones(3,1);ck('p6:b',rr.dot(rr)==14 and F(14,3)<7);ck('p6:c',s.limit((2*s.pi*v)**(-N/2),v,0,dir='+')==s.oo)
Phi=M([[1,-1],[1,1]]);y=M([0,4]);G=Phi.T*Phi;C0=s.diag(4,1);m0=M([2,0]);theta=s.simplify((G+v*C0.inv()).inv()*(Phi.T*y+v*C0.inv()*m0))
ck('p7:a',theta==M([2,4/(2+v)]));ck('p7:b',theta.subs(v,1)==M([2,F(4,3)]));ck('p7:c',theta.limit(v,0)==M([2,2]) and theta.limit(v,s.oo)==m0)
y=M([0,2]);SN=(s.eye(2)+G/2).inv();mn=SN*Phi.T*y/2;phi=M([1,1]);phi0=M([1,0])
ck('p8:a',SN==s.eye(2)/2 and mn==M([F(1,2),F(1,2)]));ck('p8:b',(phi.T*mn)[0]==1 and (phi.T*SN*phi)[0]+2==3);ck('p8:c',(phi0.T*SN*phi)[0]==F(1,2))
C1=M([[2,1],[1,2]]);C2=2*s.eye(2);y=M([1,-1]);ev=lambda C:s.exp(-(y.T*C.inv()*y)[0]/2)/(2*s.pi*s.sqrt(C.det()));bf=s.simplify(ev(C1)/ev(C2));odds=3*bf
ck('p9:ab',bf==2*s.exp(-F(1,2))/s.sqrt(3) and float(bf)<1);ck('p9:c',float(odds)>1 and abs(float(odds/(1+odds))-.6775320977)<1e-9)
Phi=M([[1,0],[0,1],[1,1]]);y=M([1,2,0]);G=Phi.T*Phi;P=Phi*G.inv()*Phi.T;H=Phi*(G+s.eye(2)).inv()*Phi.T;ml=G.inv()*Phi.T*y;mr=(G+s.eye(2)).inv()*Phi.T*y
ck('p10:a',ml==M([0,1]) and Phi.T*(y-Phi*ml)==s.zeros(2,1));ck('p10:b',P==M([[2,-1,1],[-1,2,1],[1,1,2]])/3 and P.T==P and P*P==P);ck('p10:c',mr==M([F(1,8),F(5,8)]) and Phi.T*(y-Phi*mr)==mr)
w=Phi*M([1,1]);ck('p10:d',H.T==H and H*w==F(3,4)*w and H*H*w==F(9,16)*w and H*H!=H)
Path(__file__).with_name('math-check-result.json').write_text(json.dumps({'status':'pass','checks':checks,'note':'General proof claims separately reviewed in blind-solutions.md and content review.'},indent=2)+'\n');print(len(checks),'exact/symbolic checks passed')
