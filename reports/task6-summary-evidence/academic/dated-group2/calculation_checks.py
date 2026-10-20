from pathlib import Path
import json,math
import sympy as s
import mpmath as mp
OUT=Path(__file__).parent
checks=[]
def exact(label,actual,expected):
 if isinstance(actual,s.MatrixBase):res=actual-s.Matrix(expected);zero=res==s.zeros(*res.shape)
 else:res=s.simplify(actual-expected);zero=res==0
 assert zero,(label,res)
 checks.append(dict(label=label,method='exact',actual=str(actual),expected=str(expected),residual=str(res)))
M=s.Matrix
A=M([[1,2,3],[4,5,6],[7,8,9]]);B=M([[1,1,0],[0,1,1],[1,0,1]])
exact('hw1/p3 AB',A*B,M([[4,3,5],[10,9,11],[16,15,17]]));exact('hw1/p3 BA',B*A,M([[5,7,9],[11,13,15],[8,10,12]]))
for label,A,I in [('hw1/p5a',M([[2,1],[1,1]]),M([[1,-1],[-1,2]])),('hw1/p5b',M([[1,-2],[3,1]]),M([[1,2],[-3,1]])/7),('hw1/p5c',M([[2,1,0],[1,2,0],[0,0,2]]),M([[s.Rational(2,3),-s.Rational(1,3),0],[-s.Rational(1,3),s.Rational(2,3),0],[0,0,s.Rational(1,2)]]))]:exact(label+' inverse product',A*I,s.eye(A.rows))
X=M([[1,1,2],[1,2,-1],[1,3,1]]); exact('hw1/p7 combination',X*M([-6,3,2]),M([1,-2,5]));exact('hw1/p7 determinant',X.det(),5)
Q=M([[3,1],[1,2]]);exact('hw1/p12 stationary equation',Q*M([s.Rational(3,5),-s.Rational(4,5)]),M([1,-1]))
u,v,w=s.symbols('u v w');fs=[u*u+3*v*v-2*u+4*v,u*u+2*u*v+3*v*v-4*u+2*v,(u+2*v-w-3)**2]
for i,(f,vars,point,answer) in enumerate([(fs[0],[u,v],{u:1,v:-1},[0,-2]),(fs[1],[u,v],{u:1,v:-1},[-4,-2]),(fs[2],[u,v,w],{u:1,v:0,w:-1},[-2,-4,2])],1):exact(f'hw1/p10/{i} derivative',M([s.diff(f,z) for z in vars]).subs(point),M(answer))
Phi=M([[1,-1],[1,0],[1,1]]); y=M([2,1,4]);th=M([s.Rational(7,3),1]);r=y-Phi*th
exact('hw1/p17 predictions',Phi*th,M([s.Rational(4,3),s.Rational(7,3),s.Rational(10,3)]));exact('hw1/p17 orthogonality',Phi.T*r,s.zeros(2,1));exact('hw1/p17 SSE',(r.T*r)[0],s.Rational(8,3))
for l,t in [(1,M([s.Rational(7,4),s.Rational(2,3)])),(4,M([1,s.Rational(1,3)]))]:exact('hw1/p19 ridge '+str(l),(Phi.T*Phi+l*s.eye(2))*t,Phi.T*y)
Phi=M([[1,1],[2,2]]);y=M([3,6]);t=M([1,1]);r=y-Phi*t
exact('hw1/p20 stationarity',(Phi.T*Phi+5*s.eye(2))*t,Phi.T*y);exact('hw1/p20 minimum',(r.T*r)[0]+5*(t.T*t)[0],15)
for name,S,A,mu,b,my,sy,cxy,noise in [
('22a',M([[4,1],[1,2]]),M([[1,2],[-1,1]]),M([1,2]),M([1,-2]),M([6,-1]),M([[16,-1],[-1,4]]),M([[6,-3],[5,1]]),s.zeros(2)),
('22b',M([[2,1],[1,1]]),M([[2,-1],[1,1]]),M([1,-1]),M([-1,2]),M([2,2]),M([[5,4],[4,5]]),M([[3,3],[1,2]]),s.zeros(2)),
('22c',M([[2,1],[1,3]]),M([[1,1],[1,-1]]),M([1,-1]),s.zeros(2,1),M([0,2]),M([[8,0],[0,4]]),M([[3,1],[4,-2]]),s.ones(2))]:
 exact('hw1/p'+name+' mean',A*mu+b,my);exact('hw1/p'+name+' covariance',A*S*A.T+noise,sy);exact('hw1/p'+name+' cross',S*A.T,cxy)
S0=s.diag(1,2);S1=M([[2,1],[1,2]]);H=S0.inv()+S1.inv();C=M([[7,2],[2,10]])/11;m=M([s.Rational(3,11),s.Rational(4,11)])
exact('hw1/p25 precision inverse',H*C,s.eye(2));exact('hw1/p25 mean equation',H*m,S1.inv()*M([1,1]));exact('hw1/p25 determinant',C.det(),s.Rational(6,11))
# The following integrals are numerical checks of concrete normalized densities,
# not substitutes for the analytic normalization arguments in the derivations.
mp.mp.dps=50
tol=mp.mpf('1e-25')
def numeric(label,value,expected=1):
 residual=abs(value-expected);assert mp.isfinite(value) and mp.isfinite(residual) and tol>0 and residual<tol
 checks.append(dict(label=label,method='numerical',value=str(value),expected=str(expected),absolute_residual=str(residual),absolute_tolerance=str(tol)))
def mpq(x):return mp.mpf(str(s.N(x,55)))
def normalize2(label,H,pref):
 a,b,d=mpq(H[0,0]),mpq(H[0,1]),mpq(H[1,1]);pref=mpq(pref)
 # Integrate the first coordinate analytically by completing the square;
 # evaluate the resulting one-dimensional integral numerically.
 integral=pref*mp.sqrt(2*mp.pi/a)*mp.quad(lambda z:mp.exp(-(d-b*b/a)*z*z/2),[-mp.inf,mp.inf])
 numeric(label,integral)
normalize2('1012/p4 mass',s.diag(s.Rational(1,9),s.Rational(1,4)),1/(12*s.pi))
normalize2('1012/p5 mass',M([[1,-s.Rational(1,2)],[-s.Rational(1,2),s.Rational(1,2)]]),1/(4*s.pi))
normalize2('hw1/p13 mass',M([[2,-1],[-1,2]])/3,1/(2*s.pi*s.sqrt(3)))
numeric('hw1/p14 mass',mp.exp(mp.mpf('1.5'))*mp.sqrt(2/mp.pi)*mp.quad(lambda z:mp.exp(-(4*z*z-8*z+7)/2),[-mp.inf,1,mp.inf]))
normalize2('hw1/p22b source density mass',M([[1,-1],[-1,2]]),1/(2*s.pi))
normalize2('hw1/p25 normalized product mass',H,s.sqrt(s.Rational(11,6))/(2*s.pi))
(OUT/'calculation-checks.json').write_text(json.dumps(dict(schema_version=1,description='Own exact calculations and supplementary concrete normalization integrals; no reference answers used.',checks=checks),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(exact_checks=sum(x['method']=='exact' for x in checks),numerical_checks=sum(x['method']=='numerical' for x in checks),finite_positive_absolute_tolerance=str(tol),largest_numeric_residual=str(max(mp.mpf(x['absolute_residual']) for x in checks if x['method']=='numerical'))),indent=2))
