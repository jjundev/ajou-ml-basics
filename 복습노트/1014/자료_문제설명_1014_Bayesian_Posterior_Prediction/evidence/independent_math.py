from fractions import Fraction as F
import sympy as s
# An independently constructed posterior and direct quadratic expansion.
t1,t2=s.symbols('t1 t2',real=True);t=s.Matrix([t1,t2])
P=s.Matrix([[1,0],[1,1],[1,2]]); y=s.Matrix([0,1,3]);S0=s.Matrix([[2,1],[1,3]]);m0=s.Matrix([1,-1]);v=s.Rational(2)
A=S0.inv()+P.T*P/v;b=S0.inv()*m0+P.T*y/v;S=A.inv();m=S*b
E=((y-P*t).T*(y-P*t))[0]/(2*v)+((t-m0).T*S0.inv()*(t-m0))[0]/2
Ec=((t-m).T*S.inv()*(t-m))[0]/2
assert all(s.diff(s.expand(E-Ec),z)==0 for z in t)
a=s.Matrix([1,3]);nu=(a.T*S*a)[0];mu=(a.T*m)[0]
assert nu>0 and (a.T*S*a)[0]==S[0,0]+6*S[0,1]+9*S[1,1]
z,u,mu0=s.symbols('z u mu',real=True);n,q=s.symbols('nu q',positive=True)
bar=(n*u+q*mu0)/(n+q);C=q*n/(q+n)
assert s.simplify((u-z)**2/q+(z-mu0)**2/n-(z-bar)**2/C-(u-mu0)**2/(q+n))==0
assert s.simplify(s.sqrt(C)/(s.sqrt(q)*s.sqrt(n))-1/s.sqrt(q+n))==0
print('posterior S=',S,'m=',m,'predictive mean=',mu,'latent variance=',nu,'obs variance=',nu+v)
print('exact posterior completion and covariance cross terms: PASS')
print('symbolic convolution completion + normalization: PASS for sigma2>0 and nu>0')
# p1 independent integral and p2 independent derivatives.
x,mu1,v1=s.symbols('x mu1 v1',real=True,nonzero=True)
assert F(1,3)*3==1
assert s.integrate(s.Rational(10,7),(x,s.Rational(9,10),s.Rational(16,10)))==1
f=mu1*x/v1-x*x/(2*v1)
assert s.diff(f,x).subs(x,mu1)==0 and s.diff(f,x,2)==-1/v1
assert s.simplify(f+(x-mu1)**2/(2*v1)-mu1**2/(2*v1))==0
print('p1 a: exact sum 1; p1 b: exact integral 1; p2: symbolic derivatives and square identity PASS')
