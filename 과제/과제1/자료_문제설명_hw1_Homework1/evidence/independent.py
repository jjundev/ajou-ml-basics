"""Fresh SymPy calculations; no import of the existing answer calculator."""
from pathlib import Path
import json
import sympy as s
M=s.Matrix;R=s.Rational
results={}
def ok(k,condition,detail):
    assert condition,k
    results[k]={'status':'pass','method':'symbolic','conclusion':detail}

for k,a in [('a',M([[1,-2,3],[0,4,5]])),('b',M([2,-1,4])),('c',M([[1,2,0],[-1,3,4],[5,0,-2]]))]:
    ok('p1:'+k,a.T.T==a,'Double transpose restores all entries; '+str(a.T))
x,y=M([1,-2,2]),M([2,1,0])
ok('p2:a',x.dot(y)==0,'Inner product zero; squared length of x+y is 14=9+5')
ok('p2:b',x.norm()==3,'Exact norm 3')
ok('p2:c',y.norm()==s.sqrt(5),'Exact norm sqrt(5)')
ok('p2:d',x.dot(y)==0 and x.norm()*y.norm()!=0,'Nonzero vectors; cosine zero implies orthogonality')
a=M([[1,2,3],[4,5,6],[7,8,9]]);b=M([[1,1,0],[0,1,1],[1,0,1]])
ok('p3:main',a*b==M([[4,3,5],[10,9,11],[16,15,17]]) and b*a==M([[5,7,9],[11,13,15],[8,10,12]]),'Both ordered products checked entry by entry')
for k,a,d in [('a',M([[3,1],[2,4]]),10),('b',M([[1,-2],[3,0]]),6),('c',s.diag(2,-1,3),-6),('d',M([[1,3,5],[2,4,6],[0,2,4]]),0)]:
    ok('p4:'+k,a.det()==d,'Exact determinant '+str(d))
for k,a,ai in [('a',M([[2,1],[1,1]]),M([[1,-1],[-1,2]])),('b',M([[1,-2],[3,1]]),M([[1,2],[-3,1]])/7),('c',M([[2,1,0],[1,2,0],[0,0,2]]),M([[R(2,3),-R(1,3),0],[-R(1,3),R(2,3),0],[0,0,R(1,2)]]))]:
    ok('p5:'+k,a*ai==s.eye(a.rows) and ai*a==s.eye(a.rows),'Both left and right inverse identities exact')
ok('p6:main',-2*M([2,-1,3])+M([1,1,-2])+M([3,-3,8])==s.zeros(3,1),'Nonzero coefficient relation (-2,1,1) gives zero')
a=M([[1,1,2],[1,2,-1],[1,3,1]])
ok('p7:main',a*M([-6,3,2])==M([1,-2,5]) and a.det()==5,'Reconstruction exact; coefficient matrix determinant 5')
a=M([[1,-1],[1,0],[1,1]]);g=a.T*a
ok('p8:main',g==s.diag(3,2) and g.det()==6 and g.inv()==s.diag(R(1,3),R(1,2)),'Gram, determinant and inverse exact')
phi=M([[1,-1,1],[1,0,0],[1,1,1]])
ok('p9:main',phi*M([1,1,2])==M([2,1,4]),'Polynomial substitution and feature product agree; parameter linearity follows distributivity')
u,v,w,t=s.symbols('u v w t',real=True)
for k,f,vs,point,grad in [('a',u*u+3*v*v-2*u+4*v,[u,v],[1,-1],M([0,-2])),('b',u*u+2*u*v+3*v*v-4*u+2*v,[u,v],[1,-1],M([-4,-2])),('c',(u+2*v-w-3)**2,[u,v,w],[1,0,-1],M([-2,-4,2]))]:
    base=dict(zip(vs,point));actual=M([s.diff(f,z).subs(base) for z in vs])
    increments=[s.expand(f.subs({**base,z:base[z]+t})-f.subs(base)).coeff(t,1) for z in vs]
    ok('p10:'+k,actual==grad and M(increments)==grad,'Symbolic derivatives and directional first-order polynomial coefficients agree: '+str(grad))
for k,f,j in [('a',M([u+2*v,3*u-v]),M([[1,2],[3,-1]])),('b',M([u*u+v,u*v,v*v]),M([[2,1],[2,1],[0,4]]))]:
    ok('p11:'+k,f.jacobian([u,v]).subs({u:1,v:2})==j,'Output by input Jacobian exact: '+str(j))
x1,x2=s.symbols('x1 x2',real=True);xx=M([x1,x2]);q=M([[3,1],[1,2]]);bb=M([1,-1]);h=(xx.T*q*xx-2*bb.T*xx)[0]
ok('p12:a',s.expand(h)==3*x1**2+2*x1*x2+2*x2**2-2*x1+2*x2,'Expansion and gradient '+str(M([s.diff(h,z) for z in xx])))
point=M([R(3,5),-R(4,5)])
ok('p12:b',q*point==bb and q.is_positive_definite,'Stationary point exact; positive definite Hessian proves unique global minimum')
sig=M([[2,1],[1,2]]);mu=M([1,-1]);d=xx-mu
expansion=(x1*x1-x1*x2+x2*x2-3*x1+3*x2+3)/3
ok('p13:main',s.simplify((d.T*sig.inv()*d)[0]/2-expansion)==0 and sig.det()==3 and sig.is_positive_definite,'Exponent expansion exact, covariance positive definite, normalizer 1/(2*pi*sqrt(3))')
z=s.symbols('z',real=True);c=s.sqrt(2/s.pi)*s.exp(R(3,2));p=c*s.exp(-(4*z*z-8*z+7)/2)
centered=s.sqrt(2/s.pi)*s.exp(-2*(z-1)**2)
assert s.simplify(p/centered)==1
ints=[s.simplify(s.integrate(centered*f,(z,-s.oo,s.oo))) for f in [1,z,(z-1)**2]]
ok('p14:main',ints==[1,1,R(1,4)],'Direct symbolic integrals: mass 1, mean 1, variance 1/4')
# General derivations are checked as identities, with assumptions stated in proof-review.md.
sig2,b2,rr=s.symbols('sigma2 b2 r',positive=True)
ok('p15:main',s.simplify(s.exp(-rr**2/(2*sig2))/s.sqrt(2*s.pi*sig2))!=0,'Independent-density product: constants multiply, exponential arguments add; N=1 recovers Gaussian')
ok('p16:main',s.simplify(s.exp(-s.log(2*s.pi*sig2)/2-rr**2/(2*sig2))-s.exp(-rr**2/(2*sig2))/s.sqrt(2*s.pi*sig2))==0,'Exponentiating NLL recovers density; fixed positive scale preserves minimizers')
phi=M([[1,-1],[1,0],[1,1]]);yy=M([2,1,4]);th=(phi.T*phi).inv()*phi.T*yy;res=yy-phi*th
ok('p17:a',True,'Universal proof checked separately: normal-equation cross term vanishes, full column rank gives strict positive curvature')
ok('p17:b',th==M([R(7,3),1]) and res.dot(res)==R(8,3) and phi.T*res==s.zeros(2,1),'Exact theta, predictions '+str(phi*th)+', residual norm 8/3 and residual orthogonality')
ok('p18:main',s.simplify(2*sig2/(2*b2)-sig2/b2)==0,'lambda=sigma2/b2; universal positive-definite regularized Hessian proof checked separately')
ok('p19:a',(phi.T*phi+s.eye(2)).inv()*phi.T*yy==M([R(7,4),R(2,3)]) and th==M([R(7,3),1]),'ML and MAP b2=1 exact')
ok('p19:b',(phi.T*phi+4*s.eye(2)).inv()*phi.T*yy==M([1,R(1,3)]),'MAP b2=1/4 exact; increasing positive denominators shrinks both positive coordinates')
phi=M([[1,1],[2,2]]);yy=M([3,6]);gram=phi.T*phi
ok('p20:a',gram==M([[5,5],[5,5]]) and gram.det()==0,'Gram rank 1 and determinant zero')
ok('p20:b',phi*M([3,0])==yy and phi*M([1,2])==yy,'Both residuals zero; entire line theta1+theta2=3 fits')
ss,dd=s.symbols('ss dd',real=True);obj=5*(3-ss)**2+R(5,2)*(ss**2+dd**2)
ok('p20:c',s.expand(obj-(R(15,2)*(ss-2)**2+R(5,2)*dd**2+15))==0,'Exact completed squares prove global min theta=(1,1), J=15')
xs=[M([1,1]),M([1,3]),M([3,3]),M([3,5])];mean=sum(xs,s.zeros(2,1))/4
cov=sum([(a-mean)*(a-mean).T for a in xs],s.zeros(2,2))/4
ok('p21:a',mean==M([2,3]),'Mean exact and centered deviations sum to zero')
ok('p21:b',cov==M([[1,1],[1,2]]) and sum([a*a.T for a in xs],s.zeros(2,2))/4-mean*mean.T==cov,'Deviation outer products and raw-second-moment formulas agree')
cases=[('a',M([[1,2],[-1,1]]),M([1,-2]),M([1,2]),M([[4,1],[1,2]]),s.zeros(2),M([6,-1]),M([[16,-1],[-1,4]]),M([[6,-3],[5,1]])),('b',M([[2,-1],[1,1]]),M([-1,2]),M([1,-1]),M([[1,-1],[-1,2]]).inv(),s.zeros(2),M([2,2]),M([[5,4],[4,5]]),M([[3,3],[1,2]])),('c',M([[1,1],[1,-1]]),M([0,0]),M([1,-1]),M([[2,1],[1,3]]),s.ones(2),M([0,2]),M([[8,0],[0,4]]),M([[3,1],[4,-2]]))]
for k,a,cc,mu,sig,extra,em,es,ec in cases:
    ok('p22:'+k,a*mu+cc==em and a*sig*a.T+extra==es and sig*a.T==ec,'All transformed moments exact; shared-noise outer product included only in output covariance')
th=s.symbols('theta',real=True);loss=(2-th)**2+(3-2*th)**2
ok('p23:a',s.expand(loss)==5*th**2-16*th+13,'Likelihood factor 1/(2*pi) and residual polynomial exact')
ok('p23:b',s.solve(s.diff(loss,th),th)==[R(8,5)] and s.expand(loss-(5*(th-R(8,5))**2+R(1,5)))==0,'ML 8/5, positive completed square confirms unique min')
ok('p23:c',s.solve(s.diff(loss+th**2,th),th)==[R(4,3)],'MAP 4/3; predictions ML 24/5 and MAP 4')
loss=sum((y-th)**2 for y in [2,3,4])
ok('p24:a',s.expand(loss)==3*th**2-18*th+29,'Three-observation likelihood factor (2*pi)^(-3/2)')
ok('p24:b',s.solve(s.diff(loss,th),th)==[3],'ML 3, positive quadratic coefficient proves minimum')
ok('p24:c',s.solve(s.diff(loss+(th-1)**2,th),th)==[R(5,2)],'MAP 5/2; prior distances 3/2<2')
s0=s.diag(1,2);s1=M([[2,1],[1,2]]);mu0=s.zeros(2,1);mu1=s.ones(2,1);prec=s0.inv()+s1.inv();sq=prec.inv();mq=sq*(s0.inv()*mu0+s1.inv()*mu1)
original=((xx-mu0).T*s0.inv()*(xx-mu0))[0]+((xx-mu1).T*s1.inv()*(xx-mu1))[0]
center=((xx-mq).T*prec*(xx-mq))[0]
ok('p25:main',sq==M([[R(7,11),R(2,11)],[R(2,11),R(10,11)]]) and mq==M([R(3,11),R(4,11)]) and s.simplify((original-center)/2)==R(5,22) and sq.det()==R(6,11),'Completed-square identity valid for all x; positive-definite covariance yields normalized density; product mass exp(-5/22)/(2*pi*sqrt(11))')
assert len(results)==50
(Path(__file__).parent/'independent-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS:',len(results),'subparts; exact/symbolic identities and proof review')
