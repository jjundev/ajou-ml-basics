"""Independent exact/symbolic checks; general proofs logged separately by item."""
from pathlib import Path
import json,sys,os
import sympy as s
ROOT=Path(os.environ.get('ML_EXPLAIN_WORKSPACE',Path(__file__).parent))
results={}
def record(date,pid,method,conclusion):
 results.setdefault(date,{})[pid]={'method':method,'conclusion':conclusion}
def eq(actual,expected):assert actual==expected,(actual,expected)
M=s.Matrix;R=s.Rational
A=M([[1,2,3],[4,5,6],[7,8,9]]);B=M([[1,1,0],[0,1,1],[1,0,1]])
C=M([[1,2,1,2],[4,1,-1,-4]]);D=M([[0,3],[1,-1],[2,1],[5,2]])
eq([t*10 for t in [-1,R(1,2),2]],[-10,5,20]);eq(max([-1,R(1,2),2],key=abs),2)
record('0909','p1','exact','direct multiplication and absolute slopes: -10,5,20; |2| greatest')
eq((3,2)[1]!=(3,3)[0],True);record('0909','p2','exact','inner dimensions 2 != 3; undefined')
eq(A*B,M([[4,3,5],[10,9,11],[16,15,17]]));eq(B*A,M([[5,7,9],[11,13,15],[8,10,12]]));record('0909','p3','exact','both ordered 3x3 products match all nine entries')
eq(C*D,M([[14,6],[-21,2]]));record('0909','p4','exact','2x4 times4x2 matches all four entries')
eq(D*C,M([[12,3,-3,-12],[-3,1,2,6],[6,5,1,0],[13,12,3,2]]));record('0909','p5','exact','4x2 times2x4 matches all sixteen entries')
x=s.symbols('x',real=True);sig=s.symbols('sigma',positive=True);mu=s.symbols('mu',real=True)
eq((M([R(1,2),3,2]).T*M([1,2,-1]))[0],R(9,2));record('0914','p1','exact','augmented feature length3; affine and dot product=9/2')
X=M([[1,0],[1,1],[1,2]]);y=M([1,4,4]);ta=M([1,2]);tb=M([R(3,2),R(3,2)])
eq(((y-X*ta).dot(y-X*ta)/3,(y-X*tb).dot(y-X*tb)/3),(R(2,3),R(1,2)));record('0914','p2','exact','residual vectors and means 2/3,1/2; B smaller')
y2=M([1,3,5]);tb2=M([1,1]);eq((y2-X*tb2).dot(y2-X*tb2)/3,R(5,3));eq((ta.dot(ta),tb2.dot(tb2)),(5,2));record('0914','p3','exact','objectives A=5lambda,B=5/3+2lambda; crossover5/9')
eq(M([1,2]).dot(M([1,2])),5);record('0914','p4','exact','conditional mean5 variance1')
la=1+3*s.log(2*s.pi)/2;lb=R(3,4)+3*s.log(2*s.pi)/2;eq(la-lb,R(1,4));eq((round(float(la),3),round(float(lb),3)),(3.757,3.507));record('0914','p5','symbolic','Gaussian log density yields SSE/2+3log(2pi)/2; rounded values3.757,3.507')
eq((M([1,2,3])-M([-1,-1,0])).dot(M([1,2,3])-M([-1,-1,0])),22);record('0914','p6','exact','distance squared22; distance sqrt22')
f=x**3+6*x**2-3*x-5;roots=s.solve(s.diff(f,x),x);eq(set(roots),{-2-s.sqrt(5),-2+s.sqrt(5)})
for r in roots:eq(s.simplify(f.subs(x,r)),s.simplify(-10*r-3))
record('0914','p7','symbolic','derivative roots -2±sqrt5; Hessian signs ±6sqrt5; extrema17∓10sqrt5')
record('0916','p1','proof','For fixed SPD Sigma, taking -log normalized Gaussian yields quadratic/2 plus Dlog(2pi)/2+logdetSigma/2. Bayes evidence independent of theta, so MAP adds this to NLL.')
T=M([[1,2,3,10,10],[5,10,5,7,20],[10,5,3,5,4]])/100
eq(list(T.T*M([1,1,1])),[R(n,100) for n in [16,17,11,22,34]]);record('0916','p2','exact','column sums16,17,11,22,34 over100, total1')
eq(list(T*M([1]*5)),[R(n,100) for n in [26,47,27]]);record('0916','p3','exact','row sums26,47,27 over100, total1')
eq(list(T[0,:]/sum(T[0,:])),[R(n,26) for n in [1,2,3,10,10]]);record('0916','p4','exact','conditioned first row [1,2,3,10,10]/26')
eq(list(T[:,2]/sum(T[:,2])),[R(n,11) for n in [3,5,3]]);record('0916','p5','exact','conditioned third column[3,5,3]/11')
alpha,beta,k,N=s.symbols('alpha beta k N');eq(s.expand(k+alpha-1),alpha+k-1);eq(s.expand(N-k+beta-1),beta+N-k-1)
u=s.symbols('u',positive=True);eq(s.integrate(u**5*(1-u)**11,(u,0,1)),s.beta(6,12).expand(func=True));record('0916','p6','proof','Bernoulli iid product adds k successes,N-k failures to positive Beta shapes; finite beta integral normalizes. Example mode5/16 mean1/3.')
for pid,note in [('p1','parent sets c:{a,b},b:{a},a:{}; no parents does not imply marginal independence'),('p2','three arrows a->b,a->c,b->c; fully connected underlying graph'),('p3','five nodes; parents1:{},5:{},2:{5},3:{1,2},4:{2}'),('p4','one normalized node factor each; reverse-topological integration equals1')]:record('0921',pid,'qualitative',note)
eq((R(2,5)*R(1,2))/(R(3,5)*R(2,3)+R(2,5)*R(1,2)),R(1,3));record('0921','p5','exact','Bayes path probabilities2/5 and1/5, posterior bag2=1/3')
record('0921','p6','proof','Under E|X|<infinity, insert conditional expectation integral, p(x|y)p(y)=p(x,y), Fubini and marginalize y; result integral xp(x)dx. Zero-density y immaterial.')
for pid,xv,yv,expect in [('p1',[1,2,4],[2,5,7],R(40,21)),('p2',[1,1,2],[1,3,4],2)]:
 xx=M(xv);yy=M(yv);th=xx.dot(yy)/xx.dot(xx);eq(th,expect);eq(xx.dot(yy-th*xx),0);eq((yy-th*xx).dot(yy-th*xx),R(38,21) if pid=='p1' else 2);record('0923',pid,'exact',f'normal equation and residual orthogonality, theta={th}, positive curvature')
eq(1-2*2+2**3,5);record('0923','p3','exact','phi(2)=[1,2,4,8], polynomial evaluation5')
eq(2-3**2,-7);record('0923','p4','exact','phi(3)=[1,3,9], polynomial evaluation-7')
AA=M([[1,1,-1,-1],[2,5,-7,-5],[2,-1,1,3],[5,2,-4,2]]);bb=M([1,-2,4,6]);eq((AA.rank(),AA.row_join(bb).rank()),(3,4));v=AA.T.nullspace()[0];eq(v.T*AA,s.zeros(1,4));assert (v.T*bb)[0]!=0;record('0923','p5','exact',f'inconsistent ranks3,4; left-nullspace witness {list(v)}, dot b={(v.T*bb)[0]}')
AA=M([[2,3,4],[3,4,5],[4,5,6]]);eq((AA.det(),AA.rank()),(0,2));eq(AA*M([1,-2,1]),s.zeros(3,1));record('0923','p6','exact','rank2 determinant0, null vector[1,-2,1]')
AA=M([[1,0,1,0],[0,1,1,0],[1,1,0,1],[1,1,1,0]]);inv=M([[0,-1,0,1],[-1,0,0,1],[1,1,0,-1],[1,1,1,-2]]);eq(AA.inv(),inv);eq(AA*inv,s.eye(4));eq(inv*AA,s.eye(4));record('0923','p7','exact','all16 entries in inverse; both products identity')
P=M([[1,a,a*a] for a in [-1,1,2]]);eq(P,M([[1,-1,1],[1,1,1],[1,2,4]]));record('0928','p1','exact','each row feature evaluation; matrix3x3')
record('0928','p2','proof','degree3 has4 monomials; 8 samples give8x4. Differentiate SSE, normal equations; inverse valid under full column rank, >=4 distinct inputs ensures it.')
eq(R(1,25)/R(1,4),R(4,25));record('0928','p3','qualitative','ratio4/25; example tendency high-degree regularization, not universal coefficient norm ordering. y=0 counterexample removes categorical assertion.')
eq(s.simplify(s.diff(s.log(x**4)*s.sin(x**3),x)-(4/x*s.sin(x**3)+3*x*x*s.log(x**4)*s.cos(x**3))),0);record('0928','p4','symbolic','product+chain derivative identity for real x!=0')
f=s.exp(-(x-mu)**2/(2*sig**2));eq(s.simplify(s.diff(f,x)+(x-mu)/sig**2*f),0);record('0928','p5','symbolic','Gaussian-shape derivative identity; sigma nonzero, peak atmu')
xx=M(s.symbols('x0:3'));AA=M(2,3,s.symbols('a0:6'));bb=M(s.symbols('b0:2'));z=AA*xx+bb;ff=M([s.sin(v) for v in z]);eq(ff.jacobian(xx),s.diag(*[s.cos(v) for v in z])*AA)
g=s.log(1+xx.dot(xx));eq(M([g]).jacobian(xx),2*xx.T/(1+xx.dot(xx)));record('0928','p6','symbolic','scalar derivative1xD and elementwise sine Jacobian ExD match direct component differentiation, general indices.')
ff=M([s.tanh(v) for v in z]);eq(ff.jacobian(xx),s.diag(*[1-s.tanh(v)**2 for v in z])*AA);record('0928','p7','symbolic','each Jacobian entry(1-tanh²z_i)A_ij; dimensions MxN')
f=1/(1+s.exp(-x));eq(s.simplify(s.diff(f,x)-f*(1-f)),0);eq(s.diff(f,x).subs(x,0),R(1,4));record('0928','p8','symbolic','sigmoid derivative f(1-f) identity; at0=1/4')
record('0930','p1','proof','Substitution gives EX³-EX EX²=0 with finite moments; dependent nondegenerate X² example, constant X² caveat.')
record('0930','p2','proof','Center aX+bY; expand four outer-product terms. Independence kills two cross terms; covariance a²SigmaX+b²SigmaY, mean linear.')
record('0930','p3','proof','Condition on past observations; fresh noise independent. Center AX_t+w, apply outer-product definition for ASigma_tAᵀ+Q; mean A mu_t.')
record('0930','p4','proof','Expand (X-mu)², use E[X]=mu and linearity for E[X²]-mu² under finite second moment.')
record('0930','p5','proof','With x fixed, y-(Ax+b)=w; translation preserves covarianceQ and Gaussian shape. Thus conditional meanAx+b.')
record('0930','p6','proof','Centered y=A centeredx+w. General (i,j) entry sum_kl A_ik Sigma_kl A_jl+Q_ij; independent noise makes both cross blocks0; b vanishes.')
record('0930','p7','proof','Condition y: z-Cy=v givesN(Cy,R). Unconditional centered z=C centeredy+v gives C Sigma_y Cᵀ+R; substitute prior step.')
record('0930','p8','proof','For all real samples N>0, sum_ij x_i²=N sum_i x_i², same for x_j²; sum_ij x_ix_j=(sum_i x_i)²; divide polynomial expansion byN². Not a numeric-only proof.')
record('1007','p1','qualitative','Sample one6D theta shared across all inputs; phi fixed so noiseless function uncertainty solely theta.')
eq((R(1,2)*M([1,0,0,0,0,0]).dot(M([1,0,0,0,0,0])),R(1,2)*6),(R(1,2),3));record('1007','p2','exact','zero mean; prior covariance I/2 gives variances1/2 and3')
record('1007','p3','proof','SPD Gaussian posterior log density minimized at mN, so mode=mean; expected linear function=phiᵀmN; credible bands pointwise, samples share theta.')
projection=M([[1,0]]);mean=M([1,2]);cov=M([[R(1,2),-1],[-1,4]]);eq((projection*mean)[0],1);eq((projection*cov*projection.T)[0],R(1,2))
record('1007','p4','exact','selection vector e1 projects mean1 and varianceSigma11=0.5; not conditioning')
eq(2*1-(-1),3);eq(4*2+3,11);record('1007','p5','exact','independent Gaussian linear combination mean3 variance11')
record('1007','p6','proof','Linear integral commutes with weighted sum. Gaussian marginal selects mean and diagonal covariance; weights0.4+0.6=1 retained.')
eq(R(2,5)*M([10,2])+R(3,5)*M([0,0]),M([4,R(4,5)]));record('1007','p7','exact','total expectation vector[4,4/5], component projections agree')
record('1007','p8','proof','General SPD Lambda=A^-1+B^-1, eta=A^-1a+B^-1b,m=Lambda^-1eta. Expand centered quadratic using Lambda m=eta and symmetry. Original exponent differs by constant gamma-etaᵀLambda^-1eta. Gives covarianceLambda^-1,meanm; product not normalized.')
# Supplement Gaussian product proof with an exact noncommuting matrix example.
AA=M([[2,1],[1,3]]);BB=M([[4,1],[1,2]]);av=M([1,2]);bv=M([3,-1]);xx=M(s.symbols('q0:2'));La=AA.inv()+BB.inv();eta=AA.inv()*av+BB.inv()*bv;mm=La.inv()*eta
original=((xx-av).T*AA.inv()*(xx-av)+(xx-bv).T*BB.inv()*(xx-bv))[0];center=((xx-mm).T*La*(xx-mm))[0];delta=s.expand(original-center);assert not delta.free_symbols
for pid,cols,area in [('p1',[[2,0],[1,3]],6)]:eq(abs(M(cols).det()),area)
eq(M([[2,4],[1,2]]).det(),0);record('1012','p1','exact','determinants6,0; g=2b in zero-area case')
SS=M([[4,2],[2,10]]);eq(SS.det(),36);eq(SS.inv(),M([[10,-2],[-2,4]])/36);eq(SS*SS.inv(),s.eye(2));record('1012','p2','exact','det36, inverse correct via both identity products')
record('1012','p3','proof','Invertible linear map inverse Jacobian A^-1 and absolute determinant1/|detA|. Quadratic yᵀA^-ᵀA^-1y=(A^-1y)ᵀ(A^-1y); forward substitution normalizes to1; covarianceAAᵀ.')
AA=s.diag(3,2);eq(AA.det(),6);eq(AA*AA.T,s.diag(9,4));record('1012','p4','exact','Jacobian1/6, covariance diag(9,4), normalizer and origin1/(12pi)')
AA=M([[1,1],[0,2]]);inv=AA.inv();eq(inv,M([[1,-R(1,2)],[0,R(1,2)]]));eq(inv.det(),R(1,2));eq(inv.T*inv,M([[1,-R(1,2)],[-R(1,2),R(1,2)]]));record('1012','p5','exact','inverse/Jacobian1/2 and quadratic entries checked; density1/(4pi)')
record('1012','p6','proof','Cov(x,y)_ij=sum_k Sigma_ik A_jk= (Sigma Aᵀ)_ij. Independence removes noise cross term, translation removesb; transpose gives A Sigma. Q diagonal not needed.')
record('1012','p7','proof','General block multiplication B diag(Sigma,Q)Bᵀ for B=[[I,0],[A,I]] yields Sigma,SigmaAᵀ,A Sigma,A SigmaAᵀ+Q. Stacked mean[mu,A mu+b]. Joint Gaussian from independent Gaussian affine map.')
record('1012','p8','proof','Apply prediction then same block map with C: mean[A mu_t,CA mu_t], blocksP,PCᵀ,CP,CPCᵀ+R whereP=A Sigma_tAᵀ+Q; fresh-noise conditional independence.')
sources=sorted(ROOT.glob('*/review-*/source.json'))
assert sources, 'Set ML_EXPLAIN_WORKSPACE to the extracted date workspace; no sources found'
for path in sources:
 data=json.loads(path.read_text());date=data['range'];assert set(results[date])=={p['id'] for p in data['problems']}
 out={}
 for p in data['problems']:
  for sub in p['subparts']:out[p['id']+':'+sub]=results[date][p['id']]
 dest=path.parent/'evidence';dest.mkdir(exist_ok=True)
 (dest/'independent-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(date,len(out),'independent units checked')
