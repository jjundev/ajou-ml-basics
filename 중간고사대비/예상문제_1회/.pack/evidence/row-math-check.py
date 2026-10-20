"""Independent component differentiation, row shapes, and normal equations."""
from pathlib import Path
import json
import sympy as s

RUN=Path(__file__).resolve().parent
checks=[]
def eq(name,a,b):
    assert getattr(a,'shape',None)==getattr(b,'shape',None),(name,'shape')
    diff=a-b
    assert all(s.simplify(v)==0 for v in diff) if isinstance(diff,s.MatrixBase) else s.simplify(diff)==0,name
    checks.append({'name':name,'status':'pass','shape':getattr(a,'shape',None)})
M=s.Matrix
x=M(s.symbols('x1:4',real=True));A=M(3,3,s.symbols('a0:9',real=True));b=M(s.symbols('b1:4'))
row=lambda f,v:M([[s.diff(f,t) for t in v]])
eq('norm-square row derivative',row((x.T*x)[0],x),2*x.T)
eq('general nonsymmetric quadratic derivative',row((x.T*A*x)[0],x),x.T*(A+A.T))
x2=x[:2,0];A2=M([[4,1],[1,2]]);b2=M([1,0]);q=(x2.T*A2*x2)[0]/2-(b2.T*x2)[0]
eq('p2 row derivative',row(q,x2),x2.T*A2-b2.T)
eq('p2 Hessian',s.hessian(q,x2),A2)
eq('p2 minimum',A2.inv()*b2,M([s.Rational(2,7),-s.Rational(1,7)]))
P=M([[1,2,0],[1,-1,1],[1,0,2],[1,3,-1]]);y=M(s.symbols('y0:4'));theta=M(s.symbols('t0:3'));m=M(s.symbols('m0:3'))
res=P*theta-y;Q=(res.T*res)[0];sigma2,tau2=s.symbols('sigma2 tau2',positive=True)
eq('p6 LS component derivatives',row(Q,theta),2*res.T*P)
eq('p6 LS transpose normal equation',row(Q,theta).T/2,P.T*P*theta-P.T*y)
prior=(theta-m).T*(theta-m);J=Q/(2*sigma2)+prior[0]/(2*tau2)
eq('p7 MAP row derivative',row(J,theta),res.T*P/sigma2+(theta-m).T/tau2)
eq('p7 transposed normal equation',sigma2*row(J,theta).T,(P.T*P+sigma2/tau2*s.eye(3))*theta-P.T*y-sigma2/tau2*m)
S_inv=M([[2,1,0],[1,3,1],[0,1,2]])
J0=Q/(2*sigma2)+(theta.T*S_inv*theta)[0]/2
eq('p4 general covariance prior derivative',row(J0,theta),res.T*P/sigma2+theta.T*S_inv)
P2=M([[1,-1],[1,0],[1,1]]);y2=M([0,1,4]);G=P2.T*P2
eq('p4 ML unchanged',G.inv()*P2.T*y2,M([s.Rational(5,3),2]))
eq('p4 MAP unchanged',(G+s.eye(2)).inv()*P2.T*y2,M([s.Rational(5,4),s.Rational(4,3)]))
eq('p4 predictions unchanged',M([[1,2]])*M.hstack(G.inv()*P2.T*y2,(G+s.eye(2)).inv()*P2.T*y2),M([[s.Rational(17,3),s.Rational(47,12)]]))
result={'status':'pass','count':len(checks),'checks':checks,'note':'Rows computed directly from scalar components. Not inferred from lint.'}
(RUN/'row-math-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'pass','count':len(checks)}))
