from pathlib import Path
import json,sys
import sympy as s
R=Path.cwd();OUT=R/'중간고사대비/예상문제_2회';E=OUT/'.pack/evidence';E.mkdir(parents=True,exist_ok=True)
results={}
def check(key,expr):
 ok=bool(expr)
 results[key]={'pass':ok,'calculation':str(expr)}
 assert ok,key
u,v,z,t=s.symbols('u v z t',real=True)
M=s.Matrix
check('p1-coordinate-solve',s.solve(M([[1,0],[0,2]])*M([u,v])-M([3,4]),[u,v])=={u:3,v:2})
f=(u-1)**2+2*(v+1)**2
check('p2-gradient',M([[s.diff(f,u),s.diff(f,v)]])==M([[2*(u-1),4*(v+1)]]))
check('p2-jacobian',M([u+v,u-2*v]).jacobian([u,v])==M([[1,1],[1,-2]]))
check('p3-square',s.expand(z*z+(z-2)**2-2*(z-1)**2-2)==0)
g=s.exp(-(z*z+(z-2)**2)/4)/(4*s.pi)
check('p3-integral',s.simplify((s.integrate(g,(z,-s.oo,s.oo))-s.exp(-s.Rational(1,2))/s.sqrt(8*s.pi)).rewrite(s.erf))==0)
F=M([[1,-1],[1,0],[1,1]]);Y=M([1,2,3]);G=F.T*F;h=F.T*Y
check('p4-ML',G.inv()*h==M([2,1]))
check('p4-MAP',(G+s.eye(2)).inv()*h==M([s.Rational(3,2),s.Rational(2,3)]))
X=[M([0,0]),M([2,0]),M([0,2]),M([2,2])];mu=sum(X,s.zeros(2,1))/4
S=sum([(x-mu)*(x-mu).T for x in X],s.zeros(2))/4;A=s.diag(2,1)
check('p5-covariance',S==s.eye(2) and A*S*A.T==s.diag(4,1) and S*A.T==s.diag(2,1))
F=M([[1,-1],[1,1]]);Y=M([1,3]);th=M([u,v]);Q=((Y-F*th).T*(Y-F*th))[0]
check('p6-gradient',M([[s.diff(Q,u),s.diff(Q,v)]])==-2*Y.T*F+2*th.T*F.T*F)
check('p6-ML',(F.T*F).inv()*F.T*Y==M([2,1]))
Q=(1-t)**2+(3-t)**2
check('p7-ML',s.solve(s.diff(Q/2,t),t)==[2])
check('p7-MAP',s.solve(s.diff(Q/2+t*t/2,t),t)==[s.Rational(4,3)])
check('p7-strong-MAP',s.solve(s.diff(Q/2+2*t*t,t),t)==[s.Rational(2,3)])
g=s.exp(-((2-t)**2+t*t)/2)/(2*s.pi);normalizer=s.integrate(g,(t,-s.oo,s.oo));posterior=s.simplify(g/normalizer)
check('p8-normalization',s.simplify(posterior-s.exp(-(t-1)**2)/s.sqrt(s.pi))==0)
check('p8-mean',s.simplify(s.integrate(t*posterior,(t,-s.oo,s.oo))-1)==0)
check('p8-variance',s.simplify(s.integrate((t-1)**2*posterior,(t,-s.oo,s.oo))-s.Rational(1,2))==0)
check('p8-prediction',4*s.Rational(1,2)==2 and 4*s.Rational(1,2)+1==3)
check('p9-marginal-evidence',s.simplify(s.integrate(s.exp(-t*t/2)/s.sqrt(2*s.pi)*s.exp(-t*t/6)/s.sqrt(6*s.pi),(t,-s.oo,s.oo))-1/s.sqrt(8*s.pi))==0)
check('p9-posterior',s.simplify((1/s.sqrt(2*s.pi))/(1/s.sqrt(2*s.pi)+1/s.sqrt(8*s.pi)))==s.Rational(2,3))
b=M([1,1,0]);Y=M([2,0,1]);P=b*b.T/(b.dot(b));r=Y-P*Y
check('p10-projection',P*Y==M([1,1,0]) and r==M([1,-1,1]) and b.dot(r)==0)
check('p10-symmetric-idempotent',P.T==P and P*P==P)
check('p10-global-distance-identity',s.expand(((Y-b*t).T*(Y-b*t))[0]-3-2*(t-1)**2)==0)
(E/'symbolic-checks.json').write_text(json.dumps({'status':'pass','checks':results,'note':'Symbolic checks supplement the blind proof/qualitative review; they do not replace it.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(results),'symbolic/exact checks passed')
