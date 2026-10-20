"""Independent derivation artifact. Inputs restricted to the two source-only packets."""
import json, hashlib, pathlib
import sympy as s
OUT=pathlib.Path(__file__).resolve().parent
BASE=pathlib.Path('/Users/hyunjun_macbook_pro/Documents/Univ/.course-summary-worktrees/2026-10-20/머신러닝기초/.task6b3-run-ml-01/blind-review-packets')
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
sha=lambda x:hashlib.sha256(canon(x)).hexdigest()
packets=[]
for rnd in (1,2):
 p=json.loads((BASE/f'exam-{rnd}'/'questions.json').read_text())
 assert sha({k:v for k,v in p.items() if k!='packet_payload_sha256'})==p['packet_payload_sha256']
 assert sha(p['questions'])==p['question_payload_sha256']
 for q in p['questions']: assert sha({k:v for k,v in q.items() if k!='input_sha256'})==q['input_sha256']
 packets.append(p)
results={1:[],2:[]}
def add(rnd,pid,checks,parts):
 q=next(q for q in packets[rnd-1]['questions'] if q['id']==pid)
 assert [v[0] for v in parts]==q['subpart_ids']
 results[rnd].append({'id':pid,'input_sha256':q['input_sha256'],'assumptions_dimension_normalization_checks':checks,'subparts':[{'id':i,'method':m,'derivation':d,'conclusion':c,'assumptions_dimension_normalization_checks':list(checks),'unresolved_issues':[]} for i,m,d,c in parts],'unresolved_issues':[]})
add(1,'p1',['V is 3x3 and U is 3x2; coefficients are real.','The column plane is {(a,b,a+b):a,b real}.'],[
 ('a','proof',['v1+v2=(1,1,2)^T=v3.','The coefficients (1,1,-1) are nonzero and give zero.'],'Linearly dependent; rank V=2 since v1,v2 have independent first two coordinates.'),
 ('b','exact',['First two equations give alpha1+alpha3=2 and alpha2+alpha3=1.','With alpha3=t, alpha=(2-t,1-t,t)^T; the third equation is 3=3.','Every vector in col(V) satisfies its third coordinate = first + second. For c this would require 4=3.'],'For b all solutions are (2-t,1-t,t)^T, t real. For c there is no solution.'),
 ('c','exact',['Inner products give U^T U=[[2,1],[1,2]] with determinant 3.','The 2x2 inverse formula gives (U^T U)^-1=(1/3)[[2,-1],[-1,2]].','V^T V=[[2,1,3],[1,2,3],[3,3,6]] annihilates (1,1,-1)^T.'],'U^T U is invertible; V^T V is singular.')])
add(1,'p2',['f maps R^2 to R^2; J is 2x2; gradient is 2x1 and Hessian 2x2.','A is symmetric.'],[
 ('a','symbolic',['Differentiate each output with respect to x1,x2: J_f(x)=[[2x1,1],[x2,x1]].','Substitute x=(1,2)^T.'],'J_f(1,2)=[[2,1],[2,1]], dimension 2x2.'),
 ('b','symbolic',['x^T A x=4x1^2+2x1x2+2x2^2.','q=2x1^2+x1x2+x2^2-x1.','Differentiate componentwise.'],'gradient q=(4x1+x2-1,x1+2x2)^T=A x-b; Hessian=A.'),
 ('c','proof',['From x1+2x2=0 get x1=-2x2. Then -7x2=1.','Stationary point xhat=(2/7,-1/7)^T.','For nonzero h, h^T A h=4(h1+h2/4)^2+(7/4)h2^2>0.','q(xhat+h)=q(xhat)+(1/2)h^T A h since A xhat=b.'],'Unique global minimum at (2/7,-1/7)^T; value -1/7.')])
add(1,'p3',['Both second Gaussian arguments are variances.','Univariate Lebesgue densities; q must integrate to one.'],[
 ('a','symbolic',['z^2+(z-2)^2/3=(4/3)z^2-(4/3)z+4/3.','Completing the square gives (4/3)(z-1/2)^2+1.'],'Completed square: (4/3)(z-1/2)^2+1.'),
 ('b','exact',['The exponent of g is -1/2 times the expression in (a).','The z-dependent part is -(z-1/2)^2/[2(3/4)].','A Gaussian kernel of variance 3/4 integrates to sqrt(2 pi (3/4)).'],'q(z)=sqrt(2/(3 pi))*exp[-(2/3)(z-1/2)^2]; mean 1/2, variance 3/4.'),
 ('c','exact',['Product leading coefficient is 1/(2 pi sqrt(3)).','g(z)=exp(-1/2)/(2 pi sqrt(3))*exp[-(2/3)(z-1/2)^2].','Integrate using sqrt(3 pi/2) for the kernel.'],'Z=exp(-1/2)/sqrt(8 pi). This is not 1, so g itself is not a probability density; g=Z q.')])
add(1,'p4',['Phi is 3x2, y is 3x1, theta is 2x1; all coefficient priors have variance 1.','Noise variance is 1; Gaussian ML minimizes squared residual norm.'],[
 ('a','exact',['Write feature rows (1,-1),(1,0),(1,1).','Sum row outer products and y-weighted rows.'],'Phi=[[1,-1],[1,0],[1,1]], Phi^T Phi=diag(3,2), Phi^T y=(5,4)^T.'),
 ('b','exact',['Set Phi^T Phi theta=Phi^T y.','Solve 3 theta0=5 and 2 theta1=4.','At x*=2 use feature (1,2)^T.'],'theta_ML=(5/3,2)^T; mean prediction=17/3.'),
 ('c','exact',['Negative log posterior up to constants is (1/2)||y-Phi theta||^2+(1/2)||theta||^2.','Gradient zero gives (Phi^T Phi+I)theta=Phi^T y=>(4 theta0,3 theta1)=(5,4).'],'theta_MAP=(5/4,4/3)^T; mean prediction=47/12. The prior penalizes both coefficients and shrinks them toward zero.')])
add(1,'p5',['Population distribution has three equally weighted atoms, so use divisor 3.','X,Y means are 2x1; all covariance matrices and C_XY are 2x2.'],[
 ('a','exact',['Mean is ((0+2+0)/3,(0+0+2)/3)^T.','E[XX^T]=diag(4/3,4/3).','Subtract mu_X mu_X^T=[[4/9,4/9],[4/9,4/9]].'],'mu_X=(2/3,2/3)^T; Sigma_X=[[8/9,-4/9],[-4/9,8/9]].'),
 ('b','exact',['E[AX+b]=A mu_X+b.','Y-mu_Y=A(X-mu_X), hence Sigma_Y=A Sigma_X A^T and C_XY=Sigma_X A^T.','Multiply the matrices with the indicated order.'],'mu_Y=(7/3,-1)^T; Sigma_Y=diag(8/9,8/3); C_XY=[[4/9,4/3],[4/9,-4/3]].'),
 ('c','proof',['The possible Y values are (1,-1),(3,1),(3,-3), each of probability 1/3.','Cov(Y1,Y2)=0 from (b), so the coordinates are uncorrelated.','P(Y1=1,Y2=-1)=1/3, whereas P(Y1=1)P(Y2=-1)=(1/3)(1/3)=1/9.'],'Uncorrelated but dependent, established directly from their actual discrete joint distribution.')])
add(1,'p6',['N>=2 and Phi is N x 2 with full column rank; theta is 2x1, y is N x1.','sigma^2 is a fixed positive scalar, so rescaling the objective by 1/(2 sigma^2) preserves minimizers.'],[
 ('a','proof',['For fixed x_n and theta, the deterministic mean is theta0+theta1 x_n; adding epsilon_n shifts its Gaussian.','Each y_n is a function only of epsilon_n and fixed quantities. Independence of the noises therefore gives conditional independence of the observations.'],'y_n | x_n,theta ~ N(theta0+theta1 x_n,sigma^2), conditionally independent.'),
 ('b','symbolic',['Multiply the independent densities (2 pi sigma^2)^(-1/2) exp[-(y_n-phi_n^T theta)^2/(2 sigma^2)].','Take minus the logarithm of the product.'],'p(y|Phi,theta)=(2 pi sigma^2)^(-N/2)exp[-||y-Phi theta||^2/(2 sigma^2)]; L=N/2 log(2 pi sigma^2)+||y-Phi theta||^2/(2 sigma^2).'),
 ('c','proof',['By definition Rhat=||y-Phi theta||^2/N.','L=N/2 log(2 pi sigma^2)+N/(2 sigma^2) Rhat.','The additive term is independent of theta and N/(2 sigma^2)>0.'],'L and squared-loss empirical risk have exactly the same minimizing theta.'),
 ('d','symbolic',['SSE=(y-Phi theta)^T(y-Phi theta)=y^T y-2 theta^T Phi^T y+theta^T Phi^T Phi theta.','Phi^T Phi is symmetric, so the column gradient is -2 Phi^T y+2 Phi^T Phi theta.','Setting it to zero gives the normal equations.'],'Phi^T Phi theta=Phi^T y; gradient Rhat=(2/N)(Phi^T Phi theta-Phi^T y).'),
 ('e','proof',['For nonzero h, h^T Phi^T Phi h=||Phi h||^2>0 by full column rank.','Thus the normal equations have theta_ML=(Phi^T Phi)^-1 Phi^T y, and the Hessian of L=Phi^T Phi/sigma^2 is positive definite.','At theta_ML+h, L-L_min=||Phi h||^2/(2 sigma^2)>0.','Changing features to (1,x,x^2) keeps the mean linear in the three coefficients, even though it is quadratic in x.'],'Unique ML minimum (Phi^T Phi)^-1 Phi^T y. Polynomial features still define linear regression in parameters; the new design must separately have full column rank to ensure uniqueness.')])
add(1,'p7',['Phi is N x K with no rank assumption; sigma^2,tau^2 positive; theta,m0 are Kx1.','lambda=sigma^2/tau^2>0 applies to every coefficient, including an intercept.'],[
 ('a','symbolic',['Bayes: p(theta|y,Phi)=p(y|Phi,theta)p(theta)/p(y|Phi).','The numerator uses N(Phi theta,sigma^2 I_N) times N(m0,tau^2 I_K).','Evidence integrates that numerator over theta and thus is constant with respect to theta.'],'Posterior is proportional to likelihood times prior; evidence is independent of theta.'),
 ('b','symbolic',['The product leading coefficient is (2 pi sigma^2)^(-N/2)(2 pi tau^2)^(-K/2).','Its exponent is -||y-Phi theta||^2/(2 sigma^2)-||theta-m0||^2/(2 tau^2).','Minus log posterior adds C=N/2 log(2 pi sigma^2)+K/2 log(2 pi tau^2)+log p(y|Phi).'],'Negative log posterior = ||y-Phi theta||^2/(2 sigma^2)+||theta-m0||^2/(2 tau^2)+C.'),
 ('c','symbolic',['Gradient of the first quadratic is Phi^T(Phi theta-y)/sigma^2.','Gradient of the second is (theta-m0)/tau^2.','Set their sum to zero and multiply by sigma^2.'],'(Phi^T Phi+lambda I_K)theta=Phi^T y+lambda m0.'),
 ('d','symbolic',['The equation in (c) gives theta_MAP=(Phi^T Phi+lambda I_K)^-1(Phi^T y+lambda m0).','Multiplying the negative log posterior by 2 sigma^2 leaves SSE+lambda||theta-m0||^2 plus a constant.'],'MAP formula above with relative penalty lambda=sigma^2/tau^2.'),
 ('e','proof',['For any h != 0, h^T(Phi^T Phi+lambda I)h=||Phi h||^2+lambda||h||^2.','The first term is nonnegative and the second strictly positive.'],'The coefficient matrix is positive definite, hence invertible, regardless of column dependence; MAP is unique.'),
 ('f','exact',['Phi^T Phi=[[5,5],[5,5]], Phi^T y=(5,5)^T.','For lambda=1 solve [[6,5],[5,6]]theta=(5,5)^T: subtraction gives theta1=theta2 and then 11 theta1=5.','For lambda=0, predictions match y whenever theta1+theta2=1.','For general positive lambda the symmetric solution has both entries 5/(10+lambda).'],'lambda=1: theta=(5/11,5/11)^T. lambda=0: infinitely many solutions (a,1-a)^T. As lambda tends to infinity theta tends to (0,0)^T=m0.')])
add(1,'p8',['Scalar theta, x*=2, noise variances and prior variance are 2.','Conditional posterior uncertainty and independent future observation noise are distinct variance contributions.'],[
 ('a','symbolic',['Likelihood is N(2|theta,2)N(0|theta,2); multiply by N(theta|1,2).','Leading factor is (4 pi)^(-3/2).','Exponent is -[(2-theta)^2+theta^2+(theta-1)^2]/4.'],'Product is (4 pi)^(-3/2) exp[-((2-theta)^2+theta^2+(theta-1)^2)/4].'),
 ('b','symbolic',['Sum of squares =3 theta^2-6 theta+5.','Write -(3 theta^2-6 theta+5)/4=-1/2[(3/2)theta^2-3theta+5/2].'],'A=3/2, b=3/2, c=5/2.'),
 ('c','exact',['A theta^2-2b theta+c=(3/2)(theta-1)^2+1.','The constant exp(-1/2) cancels in normalization.','The remaining Gaussian kernel has variance A^-1=2/3 and integral sqrt(4 pi/3).'],'theta|D ~ N(1,2/3), with density sqrt(3/(4 pi)) exp[-3(theta-1)^2/4].'),
 ('d','proof',['For f*=2theta, conditional expectation is 2 E[theta|D]=2.','Conditional variance is 4 Var(theta|D)=8/3. Linear transforms of a Gaussian remain Gaussian.'],'f*|D ~ N(2,8/3).'),
 ('e','proof',['Future noise is independent of theta and D and has mean 0, variance 2.','Means add, and independent variances add: 8/3+2=14/3.','A sum of independent Gaussians is Gaussian.'],'y*|D ~ N(2,14/3).'),
 ('f','exact',['The posterior quadratic is minimized at theta=1, its mean and mode.','Fixing theta to MAP sets f*=2 deterministically, then adds only N(0,2) observation noise.'],'theta_MAP=1; plug-in y* ~ N(2,2). Full posterior prediction has additional variance 8/3 from uncertain theta propagated through x*=2.')])
add(1,'p9',['v_j>0; scalar observation evidence is a density value at y, not P(Y=y).','Model choice in (e) uses the larger model posterior probability under the given model priors.'],[
 ('a','symbolic',['Marginalize the joint model p(y,theta|M_j)=p(y|theta,M_j)p(theta|M_j).','p(y|M_j)=integral N(y|theta,1)N(theta|0,v_j) dtheta.','The prior describes theta before the observed y; integrating against the posterior would count the observation again and is not this marginalization identity.'],'Evidence integral uses the prior, not posterior.'),
 ('b','symbolic',['Let v=v_j. (y-theta)^2+theta^2/v=((v+1)/v)(theta-v y/(v+1))^2+y^2/(v+1).','The leading factor of the product is 1/(2 pi sqrt(v)).','Integral of the theta kernel is sqrt(2 pi v/(v+1)).'],'p(y|M_j)=[2 pi(v_j+1)]^(-1/2) exp[-y^2/(2(v_j+1))]; normalized N(0,v_j+1).'),
 ('c','exact',['Set y=0 in (b).','For v1=1 use total variance 2; for v2=4 use variance 5.'],'p(0|M1)=1/sqrt(4 pi); p(0|M2)=1/sqrt(10 pi).'),
 ('d','exact',['B12=p(0|M1)/p(0|M2)=sqrt(10 pi)/sqrt(4 pi)=sqrt(5/2)>1.'],'Data evidence favors M1.'),
 ('e','proof',['Bayes gives P(Mj|y)=p(y|Mj)P(Mj)/p(y).','Dividing cancels common p(y), so posterior odds=B12 times prior odds.','Here prior odds=(1/3)/(2/3)=1/2. Posterior odds=sqrt(5/2)/2.','With only two models, P(M1|0)=B12/(B12+2). Since B12<2, that posterior is <1/2.'],'P(M1|0)=sqrt(5)/(sqrt(5)+2sqrt(2)); choose M2 by larger posterior despite B12>1.')])
add(1,'p10',['Phi is N x K generally, here 3x2; full column rank, Euclidean inner product.','P is N x N; r,y,yhat are N x1.'],[
 ('a','proof',['Let r=y-Phi thetahat. The path loss is ||r-t Phi h||^2=||r||^2-2t h^T Phi^T r+t^2||Phi h||^2.','Derivative at zero is -2 h^T Phi^T r=0 for every h.','Choosing h=Phi^T r implies ||Phi^T r||^2=0.'],'Phi^T r=0, so r is orthogonal to every vector in col(Phi).'),
 ('b','symbolic',['Substitute r=y-Phi thetahat in Phi^T r=0.','Full column rank implies Phi^T Phi is positive definite and invertible.'],'Phi^T Phi thetahat=Phi^T y; thetahat=(Phi^T Phi)^-1 Phi^T y.'),
 ('c','proof',['Substitution yields P=Phi(Phi^T Phi)^-1 Phi^T, dimension N x N.','The Gram matrix and its inverse are symmetric, so P^T=P.','P^2=Phi G^-1(Phi^T Phi)G^-1 Phi^T=Phi G^-1 Phi^T=P.'],'P is symmetric and idempotent, the orthogonal projector onto col(Phi).'),
 ('d','exact',['G=diag(3,2), Phi^T y=(4,2)^T.','thetahat=(4/3,1)^T. Multiplication gives the matrix P and vectors below.','Phi^T r=(2/3-1/3-1/3,-1/3+1/3)^T=(0,0)^T.'],'P=[[1/3,1/3,1/3],[1/3,5/6,-1/6],[1/3,-1/6,5/6]]; yhat=(4/3,7/3,1/3)^T; r=(2/3,-1/3,-1/3)^T.'),
 ('e','proof',['For any u in col(Phi), y-u=r+(yhat-u).','Both yhat and u lie in col(Phi), so r^T(yhat-u)=0.','Expand the squared norm and remove the zero cross term: ||y-u||^2=||r||^2+||yhat-u||^2.'],'Distance is at least ||r||^2, with equality only for u=yhat. Thus yhat is the unique closest point.')])
add(2,'p1',['t is real; V(t) is 3x3; coefficients are real.'],[
 ('a','symbolic',['V=[[1,0,1],[0,1,1],[1,1,t]].','Replace row3 by row3-row1-row2, obtaining upper triangular diagonal 1,1,t-2 without changing determinant.'],'det V(t)=t-2; the columns are a basis of R^3 exactly when t != 2.'),
 ('b','exact',['At t=2 the third row is the sum of the first two.','For RHS (1,2,3)^T, alpha1+alpha3=1 and alpha2+alpha3=2; let alpha3=s.','Every vector in col(V(2)) has z=x+y, which excludes (1,2,4)^T.'],'All solutions for (1,2,3)^T are (1-s,2-s,s)^T, s real; none for (1,2,4)^T.'),
 ('c','exact',['At t=3 write alpha1=1-alpha3, alpha2=2-alpha3.','Third equation becomes 3+alpha3=4, so alpha3=1.','det V(3)=1 so its column space is R^3, whereas col(V(2)) is only the plane z=x+y.'],'Unique solution alpha=(0,1,1)^T; changing t expands the column space from a plane to all R^3.')])
add(2,'p2',['f:R^2->R^2; J is 2x2; loss is scalar; gradients are 2x1.','The specified directional derivative uses d itself, not d normalized to unit length.'],[
 ('a','symbolic',['Differentiate f1=x1+x2 and f2=x1x2 row by row.'],'J_f(x)=[[1,1],[x2,x1]], J_f(1,2)=[[1,1],[2,1]], dimension 2x2.'),
 ('b','symbolic',['gradient_z ell=z-(1,2)^T. At x=(1,2), f(x)=(3,2)^T, so gradient ell=(2,0)^T.','Chain rule with column gradients gives gradient_x L=J_f^T gradient_z ell=(2,2)^T.','Directly L=(1/2)[(x1+x2-1)^2+(x1x2-2)^2].','Its derivatives are x1+x2-1+x2(x1x2-2) and x1+x2-1+x1(x1x2-2); both are 2 at the given point.'],'gradient_x L(1,2)=(2,2)^T by both derivations.'),
 ('c','proof',['D_d L=gradient L^T d=(2,2)(1,-1)^T=0.','Along this path f=(3,2+h-h^2)^T, so L=2+(1/2)(h-h^2)^2, whose derivative at zero is 0.','A stationary point requires zero gradient, equivalently every directional derivative zero. Here gradient=(2,2)^T is not zero.'],'D_d L=0, but (1,2)^T is not stationary; derivative along (1,1)^T is 4.')])
add(2,'p3',['X,Y are jointly Gaussian two-dimensional vectors; Sigma is positive definite (eigenvalues 3 and 1).','A is invertible with determinant -2, so Y has an ordinary two-dimensional density.'],[
 ('a','exact',['E[Y]=A mu+b=(0,2)^T+(0,2)^T.','Cov(Y)=A Sigma A^T.','A Sigma=[[3,3],[1,-1]], hence covariance is diag(6,2).'],'E[Y]=(0,4)^T; Cov(Y)=diag(6,2).'),
 ('b','exact',['Affine Gaussian transformation yields Y~N((0,4)^T,diag(6,2)).','det covariance=12, inverse=diag(1/6,1/2).','For dimension 2 the density coefficient is (2 pi)^-1 det(cov)^-1/2.'],'Y1~N(0,6), Y2~N(4,2); p_Y=1/(4 pi sqrt(3))*exp[-y1^2/12-(y2-4)^2/4].'),
 ('c','proof',['The density in (b) factors into its two univariate Gaussian densities, proving independence.','Original Cov(X1,X2)=1 != 0. Independent finite-variance variables have zero covariance; this excludes independence for X1,X2.'],'Y1,Y2 are independent. X1,X2 are dependent. The Gaussian property makes zero cross covariance sufficient for Y independence.')])
add(2,'p4',['All Gaussian second arguments are variances; theta is scalar.','p(y=3) denotes the value of an evidence density, not the probability of a singleton.'],[
 ('a','symbolic',['Each density has leading coefficient (4 pi)^-1/2; product coefficient is 1/(4 pi).','The inner quadratic ((theta+1)^2+(3-theta)^2)/2=theta^2-2theta+5=(theta-1)^2+4.','The outer exponent factor remains -1/2.'],'g(theta)=1/(4 pi)*exp[-(theta-1)^2/2-2].'),
 ('b','exact',['Divide the Gaussian kernel by its integral sqrt(2 pi).','The likelihood alone exp[-(3-theta)^2/4] is maximized at theta=3; the posterior kernel is maximized at theta=1.'],'theta|y=3~N(1,1); density (2 pi)^-1/2 exp[-(theta-1)^2/2]; ML=3, MAP=1.'),
 ('c','exact',['Integrate (a): Z=exp(-2)/(4 pi)*sqrt(2 pi)=exp(-2)/sqrt(8 pi).','Equivalently prior predictive y has mean -1, variance 2+2=4 and evaluate its density at 3.','Z is constant in theta; posterior is g(theta)/Z and integrates to one over theta.'],'Z=exp(-2)/sqrt(8 pi), the evidence density value for y=3; it is not the posterior density function of theta.')])
add(2,'p5',['Phi is 3x2, theta is 2x1, y is 3x1; model is linear in theta.','Noise and both coefficient prior variances are 1; same feature at two inputs forces equal fitted means there.'],[
 ('a','exact',['Feature rows are (1,1),(1,0),(1,1).','Sum row outer products to get G=[[3,2],[2,2]]; sum y_n phi_n gives (6,6)^T.','det G=6-4=2>0, so duplicate rows do not destroy independent columns.'],'Phi=[[1,1],[1,0],[1,1]], G=[[3,2],[2,2]], Phi^T y=(6,6)^T; Gram is invertible.'),
 ('b','exact',['Normal equations: 3 theta0+2 theta1=6 and 2 theta0+2 theta1=6, giving theta0=0 and theta1=3.','yhat=(3,0,3)^T, so r=y-yhat=(-1,0,1)^T.','r^T r=2; feature at 2 is (1,4)^T.'],'theta_ML=(0,3)^T; residual=(-1,0,1)^T; SSE=2; predicted mean at x*=2 is 12.'),
 ('c','exact',['MAP solves (G+I)theta=(6,6)^T with G+I=[[4,2],[2,3]].','Inverse is (1/8)[[3,-2],[-2,4]], yielding (3/4,3/2)^T.','Prediction=(3/4)+4(3/2)=27/4.','The mean theta0+theta1 x^2 is a linear combination of fixed features with unknown coefficients.'],'theta_MAP=(3/4,3/2)^T; predicted mean 27/4. It is linear regression in coefficients despite nonlinear dependence on input x.')])
add(2,'p6',['x,y are N x1, theta is scalar; x^T x>0, sigma^2>0.','No intercept is present; P is N x N and its range is span{x}.'],[
 ('a','symbolic',['Given x and theta, y_n~N(theta x_n,sigma^2).','Independence of noises makes observations conditionally independent.','Multiply their univariate densities.'],'p(y|x,theta)=(2 pi sigma^2)^(-N/2)exp[-sum_n(y_n-theta x_n)^2/(2 sigma^2)].'),
 ('b','symbolic',['Taking minus log gives N/2 log(2 pi sigma^2)+SSE(theta)/(2 sigma^2).','The first term does not depend on theta; the second is a strictly positive multiple of SSE.'],'ML is equivalent to minimizing SSE(theta)=sum_n(y_n-theta x_n)^2.'),
 ('c','symbolic',['SSE=sum y_n^2-2theta sum x_n y_n+theta^2 sum x_n^2.','Derivative=-2sum x_n y_n+2theta sum x_n^2.','Set derivative to zero and divide by sum x_n^2>0.'],'thetahat=(sum x_n y_n)/(sum x_n^2); positive denominator is guaranteed by the stated assumption.'),
 ('d','proof',['Second derivative SSE=2sum x_n^2>0, so the quadratic has a unique global minimum.','The negative log likelihood second derivative is (sum x_n^2)/sigma^2>0.','Use vector inner products for the sums.'],'thetahat=(x^T y)/(x^T x), unique global ML minimum.'),
 ('e','proof',['yhat=x(x^T y)/(x^T x)=P y with P=xx^T/(x^T x).','x^T(y-yhat)=x^T y-(x^T x)(x^T y)/(x^T x)=0.'],'P=xx^T/(x^T x); residual is orthogonal to x.'),
 ('f','exact',['x^T x=1+4+1=6; x^T y=1+6+0=7.','thetahat=7/6; yhat=(7/6,7/3,-7/6)^T.','r=(-1/6,2/3,7/6)^T; SSE=(1+16+49)/36=11/6.'],'thetahat=7/6, yhat=(7/6,7/3,-7/6)^T, SSE=11/6; P=(1/6)[[1,2,-1],[2,4,-2],[-1,-2,1]].')])
add(2,'p7',['theta,m0 are 2x1; S0 is positive definite 2x2.','s=sigma^2>0; prior precision S0^-1=diag(1/4,1), so unequal prior variances give unequal coefficient penalties.'],[
 ('a','symbolic',['Likelihood coefficient is (2 pi sigma^2)^-1 and exponent -||y-Phi theta||^2/(2 sigma^2).','Prior coefficient is (2 pi)^-1 det(S0)^-1/2 and exponent -(theta-m0)^T S0^-1(theta-m0)/2.','Posterior is their product divided by p(y|Phi); collect all leading coefficients and log evidence in C.'],'Negative log posterior=C+||y-Phi theta||^2/(2 sigma^2)+(theta-m0)^T S0^-1(theta-m0)/2; C=log(2 pi sigma^2)+log(2 pi)+(1/2)log det S0+log p(y|Phi).'),
 ('b','symbolic',['For the likelihood term, gradient is Phi^T(Phi theta-y)/sigma^2.','For the prior term, symmetry of S0^-1 gives S0^-1(theta-m0).','The precision appears because Gaussian density measures squared displacement in units of covariance; here the penalties are (theta0-2)^2/4 and theta1^2 before the factor 1/2.'],'The two column gradients are Phi^T(Phi theta-y)/sigma^2 and S0^-1(theta-m0).'),
 ('c','symbolic',['Set sum of gradients to zero: (Phi^T Phi/sigma^2+S0^-1)theta=Phi^T y/sigma^2+S0^-1 m0.','Multiply by sigma^2 and invert the positive definite coefficient matrix.'],'theta_MAP=(Phi^T Phi+sigma^2 S0^-1)^-1(Phi^T y+sigma^2 S0^-1 m0).'),
 ('d','proof',['For h !=0, h^T(Phi^T Phi+sigma^2 S0^-1)h=||Phi h||^2+sigma^2 h^T S0^-1 h.','S0^-1 is positive definite and sigma^2>0, so the second term is strictly positive.'],'Coefficient matrix is positive definite and MAP is the unique global posterior mode.'),
 ('e','exact',['Phi^T Phi=2I, Phi^T y=(4,4)^T and S0^-1 m0=(1/2,0)^T.','At sigma^2=1, coefficient matrix=diag(9/4,3) and RHS=(9/2,4)^T.','theta_MAP=(2,4/3)^T; mean prediction=2+2(4/3)=14/3.','ML solves 2I theta=(4,4)^T.'],'MAP=(2,4/3)^T, prediction 14/3; ML=(2,2)^T, prediction 6.'),
 ('f','symbolic',['With s=sigma^2, theta0=(4+s/2)/(2+s/4)=2.','theta1=4/(2+s).','As s->0+, noise becomes negligible and theta->(2,2)^T, the exact fitting ML coefficients.','As s->infinity likelihood loses information and theta->(2,0)^T=m0.'],'theta_MAP(s)=(2,4/(2+s))^T; limits are ML at zero noise and prior mean at infinite noise.')])
add(2,'p8',['theta is 2x1; Phi is 2x2; B,S are 2x2, b,m are 2x1, c scalar.','All future noises are independent of the training data and theta; posterior uncertainty in theta is shared by future predictions.'],[
 ('a','symbolic',['Product is (4 pi)^-1(2 pi)^-1 exp[-||y-Phi theta||^2/4-theta^T theta/2].','Inside -1/2, expand (1/2)(y-Phi theta)^T(y-Phi theta)+theta^T theta.','Collect the quadratic, linear, and constant terms.'],'B=I+(1/2)Phi^T Phi, b=(1/2)Phi^T y, c=(1/2)y^T y.'),
 ('b','symbolic',['B is positive definite since h^T B h=||h||^2+(1/2)||Phi h||^2>0.','Set m=B^-1 b, S=B^-1.','theta^T B theta-2 b^T theta+c=(theta-m)^T B(theta-m)+c-b^T B^-1 b.','The final constant cancels in normalization; the Gaussian kernel integral is (2 pi)^(2/2)det(B)^-1/2.'],'Posterior N(m,S) has density [2 pi sqrt(det S)]^-1 exp[-(theta-m)^T S^-1(theta-m)/2].'),
 ('c','exact',['Phi^T Phi=2I; Phi^T y=(2,2)^T; y^T y=4.','Hence B=2I, b=(1,1)^T, c=2.','m=B^-1 b=(1/2,1/2)^T and S=(1/2)I; c-b^T B^-1 b=1.'],'theta|y~N((1/2,1/2)^T,(1/2)I), density (1/pi)exp[-||theta-(1/2,1/2)^T||^2].'),
 ('d','proof',['For any fixed phi_*, E[f_*|y]=phi_*^T m.','Var(f_*|y)=E[phi_*^T(theta-m)(theta-m)^T phi_*|y]=phi_*^T S phi_*.','A linear functional of a Gaussian is Gaussian (possibly degenerate if phi_*=0).','At x*=1, phi_*=(1,1)^T, giving mean 1 and variance 1.'],'f_*|y~N(phi_*^T m,phi_*^T S phi_*); at x*=1 this is N(1,1).'),
 ('e','proof',['Independent future noise has conditional mean zero and variance 2.','Thus E[y_*|y]=phi_*^T m and Var(y_*|y)=phi_*^T S phi_*+2.','At x*=1 full posterior prediction is N(1,3).','Gaussian posterior mode equals m; fixing theta=m omits phi_*^T S phi_*=1.'],'y_*|y~N(phi_*^T m,2+phi_*^T S phi_*); at x*=1 N(1,3), versus MAP plug-in N(1,2).'),
 ('f','proof',['Let a=phi(0)=(1,0)^T and d=phi(1)=(1,1)^T.','For two distinct future observations, Cov(a^T theta+eps0,d^T theta+eps1 | y)=a^T S d: cross terms vanish by noise independence and Cov(eps0,eps1)=0.','a^T S d=1/2. Their individual variances are 2+1/2=5/2 and 2+1=3.','Conditional on theta, independent future noises make these future observations independent. Integrating theta introduces its shared uncertainty.'],'Cross covariance is 1/2; joint posterior predictive covariance [[5/2,1/2],[1/2,3]]. The future observations are dependent after theta is integrated out, although independent given theta.')])
add(2,'p9',['Observation y is 2x1; M1 parameter dimension 1, M2 dimension 2.','All evidence values are two-dimensional densities; model space contains exactly M1,M2.'],[
 ('a','symbolic',['For M1 use B1=(1,1)^T, vartheta1=theta~N(0,1).','For M2 use B2=I2, vartheta2=(theta1,theta2)^T~N(0,I2).','For each i, p(y|Mi)=integral N_2(y|B_i vartheta_i,I2) N_{K_i}(vartheta_i|0,I_{K_i}) d vartheta_i, with K1=1,K2=2.'],'B1=[[1],[1]], B2=I2; evidence is the likelihood integrated over the respective independent Gaussian parameter priors.'),
 ('b','proof',['E[y]=B_i E[vartheta_i]+E[eps]=0.','Expand E[(B_i vartheta_i+eps)(B_i vartheta_i+eps)^T].','The cross terms vanish because both vectors have zero means and are independent; remaining terms give C_i=B_i B_i^T+I2.','Independent Gaussian vectors combine to a joint Gaussian, and a linear map preserves Gaussianity.'],'M1: y~N(0,[[2,1],[1,2]]). M2: y~N(0,2I2).'),
 ('c','exact',['In 2D, p(y|Mi)=1/(2 pi sqrt(det C_i))*exp[-y^T C_i^-1 y/2].','C1 determinant=3, inverse=(1/3)[[2,-1],[-1,2]]. At y=(1,-1)^T, C1^-1 y=y and y^T C1^-1 y=2.','C2 determinant=4, inverse=(1/2)I. Its quadratic form is 1.'],'p(y|M1)=exp(-1)/(2 pi sqrt(3)); p(y|M2)=exp(-1/2)/(4 pi).'),
 ('d','exact',['B12=evidence1/evidence2=(2/sqrt(3))exp(-1/2).','B12<1 because B12^2=4/(3e)<1, using e>1+1=2>4/3.'],'B12=2 exp(-1/2)/sqrt(3); data evidence favors M2.'),
 ('e','proof',['Divide Bayes model posteriors: P(M1|y)/P(M2|y)=[p(y|M1)/p(y|M2)] [P(M1)/P(M2)].','Prior odds=3, so posterior odds=2sqrt(3) exp(-1/2).','Convert odds O to probability O/(1+O).','O>1 because O^2=12/e>1 (e<3<12).'],'P(M1|y)=2sqrt(3)/(sqrt(e)+2sqrt(3)); choose M1 by larger posterior, since its prior odds outweigh the evidence preference for M2.')])
add(2,'p10',['Phi is 3x2, y is 3x1; G and coefficient matrices are 2x2; P,H are 3x3.','Both ridge coefficients have unit penalty; ordinary Euclidean orthogonality is used.'],[
 ('a','symbolic',['Q=(1/2)y^T y-theta^T Phi^T y+(1/2)theta^T G theta.','G=Phi^T Phi is symmetric, so column gradient=-Phi^T y+G theta.','Set gradient to zero.'],'Normal equations G thetahat=Phi^T y.'),
 ('b','exact',['If columns of Phi are independent then G is positive definite, giving thetahat=G^-1 Phi^T y.','Here G=[[2,1],[1,2]], determinant 3>0; inverse=(1/3)[[2,-1],[-1,2]].','Phi^T y=(1,2)^T, giving thetahat=(0,1)^T.'],'Unique thetahat=(0,1)^T; yhat=(0,1,1)^T; r=(1,1,-1)^T.'),
 ('c','proof',['P=Phi G^-1 Phi^T=(1/3)[[2,-1,1],[-1,2,1],[1,1,2]].','G^-1 symmetric implies P^T=P.','P^2=Phi G^-1 G G^-1 Phi^T=P; numerically the unscaled numerator matrix M obeys M^2=3M.'],'P is the stated symmetric idempotent orthogonal projector; Py=yhat.'),
 ('d','exact',['Adding (1/2)||theta||^2 adds theta to gradient, so (G+I)theta_R=Phi^T y.','G+I=[[3,1],[1,3]] has inverse (1/8)[[3,-1],[-1,3]].','Multiply by (1,2)^T.'],'theta_R=(1/8,5/8)^T, versus ordinary least squares (0,1)^T.'),
 ('e','exact',['H=Phi(G+I)^-1 Phi^T=(1/8)[[3,-1,2],[-1,3,2],[2,2,4]].','yhat_R=Hy=(1/8,5/8,3/4)^T; r_R=(7/8,11/8,-3/4)^T.','Ridge normal equation rearranges to Phi^T r_R=theta_R.','Numerically Phi^T r_R=(7/8-3/4,11/8-3/4)^T=(1/8,5/8)^T.'],'H is the stated matrix. Ridge residual is not orthogonal to col(Phi) here; Phi^T r_R=theta_R != 0, whereas ordinary least squares has Phi^T r=0.'),
 ('f','proof',['v=Phi(1,1)^T=(1,1,2)^T.','Multiplication by H gives Hv=(3/4,3/4,3/2)^T=(3/4)v.','Applying H again gives H^2v=(9/16)v != Hv.','P fixes every vector in col(Phi), including Pv=P^2v=v. H is symmetric since its middle inverse matrix is symmetric, but is not idempotent.'],'H is not an orthogonal projection. Symmetry alone is insufficient: an orthogonal projector must also be idempotent.')])
# Independently written exact calculations; no reference solution is loaded.
checks=[]
def ck(name,expr):
 if isinstance(expr,s.MatrixBase): residual=expr.applyfunc(s.simplify); passed=residual==s.zeros(*expr.shape)
 else: residual=s.simplify(expr); passed=residual==0
 checks.append({'id':name,'method':'symbolic','residual':str(residual),'passed':bool(passed)})
 assert passed,(name,residual)
R=s.Rational
U=s.Matrix([[1,0],[0,1],[1,1]]); V=U.row_join(U[:,0]+U[:,1])
ck('r1p1_gram_inverse',(U.T*U)*s.Matrix([[2,-1],[-1,2]])/3-s.eye(2))
a=s.symbols('a',real=True)
ck('r1p1_all_solutions',V*s.Matrix([2-a,1-a,a])-s.Matrix([2,1,3]))
A=s.Matrix([[4,1],[1,2]]); xhat=s.Matrix([R(2,7),-R(1,7)])
ck('r1p2_stationary',A*xhat-s.Matrix([1,0]))
z=s.symbols('z',real=True)
ck('r1p3_square',z*z+(z-2)**2/3-(R(4,3)*(z-R(1,2))**2+1))
T=s.Matrix([[1,-1],[1,0],[1,1]]); yy=s.Matrix([0,1,4])
ck('r1p4_ML',T.T*T*s.Matrix([R(5,3),2])-T.T*yy)
ck('r1p4_MAP',(T.T*T+s.eye(2))*s.Matrix([R(5,4),R(4,3)])-T.T*yy)
C=s.Matrix([[R(8,9),-R(4,9)],[-R(4,9),R(8,9)]]); F=s.Matrix([[1,1],[1,-1]])
ck('r1p5_covariance',F*C*F.T-s.diag(R(8,9),R(8,3)))
ck('r1p5_cross_covariance',C*F.T-s.Matrix([[R(4,9),R(4,3)],[R(4,9),-R(4,3)]]))
G=s.Matrix([[5,5],[5,5]])
ck('r1p7_ridge',(G+s.eye(2))*s.Matrix([R(5,11),R(5,11)])-s.Matrix([5,5]))
th=s.symbols('theta',real=True)
ck('r1p8_completed_square',((2-th)**2+th**2+(th-1)**2)/2-(R(3,2)*(th-1)**2+1))
v=s.symbols('v',positive=True); y=s.symbols('y',real=True)
ck('r1p9_completed_square',(y-th)**2+th**2/v-((v+1)/v*(th-v*y/(v+1))**2+y*y/(v+1)))
T=s.Matrix([[1,0],[1,1],[1,-1]]); yy=s.Matrix([2,2,0]); P=T*(T.T*T).inv()*T.T
ck('r1p10_projection_matrix',P-s.Matrix([[R(1,3),R(1,3),R(1,3)],[R(1,3),R(5,6),-R(1,6)],[R(1,3),-R(1,6),R(5,6)]]))
ck('r1p10_residual',yy-P*yy-s.Matrix([R(2,3),-R(1,3),-R(1,3)]))
ck('r1p10_orthogonality',T.T*(yy-P*yy));ck('r1p10_idempotence',P*P-P)
t=s.symbols('t',real=True); T=s.Matrix([[1,0,1],[0,1,1],[1,1,t]])
ck('r2p1_det',T.det()-(t-2));ck('r2p1_solution',T.subs(t,3)*s.Matrix([0,1,1])-s.Matrix([1,2,4]))
x1,x2,h=s.symbols('x1 x2 h',real=True); loss=((x1+x2-1)**2+(x1*x2-2)**2)/2
ck('r2p2_gradient',s.Matrix([s.diff(loss,x1),s.diff(loss,x2)]).subs({x1:1,x2:2})-s.Matrix([2,2]))
ck('r2p2_direction',s.diff(loss.subs({x1:1+h,x2:2-h}),h).subs(h,0))
ck('r2p3_covariance',F*s.Matrix([[2,1],[1,2]])*F.T-s.diag(6,2))
ck('r2p4_completed_square',((th+1)**2+(3-th)**2)/2-((th-1)**2+4))
T=s.Matrix([[1,1],[1,0],[1,1]]); yy=s.Matrix([2,0,4]); G=T.T*T
ck('r2p5_ML',G*s.Matrix([0,3])-T.T*yy)
ck('r2p5_MAP',(G+s.eye(2))*s.Matrix([R(3,4),R(3,2)])-T.T*yy)
x=s.Matrix([1,2,-1]); yy=s.Matrix([1,3,0]); theta=(x.T*yy)[0]/(x.T*x)[0]; r=yy-x*theta
ck('r2p6_theta',theta-R(7,6));ck('r2p6_sse',(r.T*r)[0]-R(11,6))
T=s.Matrix([[1,-1],[1,1]]); yy=s.Matrix([0,4]); noise=s.symbols('noise_variance',positive=True); prior_precision=s.diag(R(1,4),1); m0=s.Matrix([2,0])
ck('r2p7_variance_function',(T.T*T+noise*prior_precision)*s.Matrix([2,4/(2+noise)])-(T.T*yy+noise*prior_precision*m0))
yy=s.Matrix([0,2]); B=s.eye(2)+T.T*T/2; b=T.T*yy/2
ck('r2p8_B',B-2*s.eye(2));ck('r2p8_mean',B.inv()*b-s.ones(2,1)/2)
C1=s.Matrix([[2,1],[1,2]]); C2=2*s.eye(2); yy=s.Matrix([1,-1]);
ck('r2p9_M1_quadratic',(yy.T*C1.inv()*yy)[0]-2);ck('r2p9_M2_quadratic',(yy.T*C2.inv()*yy)[0]-1)
T=s.Matrix([[1,0],[0,1],[1,1]]); yy=s.Matrix([1,2,0]); G=T.T*T; P=T*G.inv()*T.T; H=T*(G+s.eye(2)).inv()*T.T
ck('r2p10_ML',G.inv()*T.T*yy-s.Matrix([0,1]))
ck('r2p10_P',P-s.Matrix([[2,-1,1],[-1,2,1],[1,1,2]])/3)
ck('r2p10_H',H-s.Matrix([[3,-1,2],[-1,3,2],[2,2,4]])/8)
ck('r2p10_ridge_solution',(G+s.eye(2)).inv()*T.T*yy-s.Matrix([R(1,8),R(5,8)]))
ck('r2p10_ridge_residual',T.T*(yy-H*yy)-s.Matrix([R(1,8),R(5,8)]))
vect=T*s.ones(2,1);ck('r2p10_Hv',H*vect-R(3,4)*vect);ck('r2p10_H2v',H*H*vect-R(9,16)*vect)
# Finite tolerance numerical quadrature supplements the exact normalizations.
import mpmath as mp
mp.mp.dps=50
numeric=[]
def quadcheck(name,fn,expected):
 actual=mp.quad(fn,[-mp.inf,mp.inf]); residual=abs(actual-expected); tol=mp.mpf('1e-30')
 numeric.append({'id':name,'method':'numerical','value':mp.nstr(actual,45),'expected':mp.nstr(expected,45),'measured_residual':mp.nstr(residual,8),'finite_positive_tolerance':'1e-30','passed':bool(residual<tol)})
 assert residual<tol,(name,residual)
quadcheck('r1p3_q_normalization',lambda z:mp.sqrt(2/(3*mp.pi))*mp.exp(-mp.mpf(2)/3*(z-mp.mpf('0.5'))**2),mp.mpf(1))
quadcheck('r1p3_evidence_integral',lambda z:mp.exp(-z*z/2-(z-2)**2/6)/(2*mp.pi*mp.sqrt(3)),mp.exp(-mp.mpf('0.5'))/mp.sqrt(8*mp.pi))
quadcheck('r1p8_posterior_normalization',lambda th:mp.sqrt(3/(4*mp.pi))*mp.exp(-3*(th-1)**2/4),mp.mpf(1))
quadcheck('r2p4_evidence_integral',lambda th:mp.exp(-((th+1)**2+(3-th)**2)/4)/(4*mp.pi),mp.exp(-2)/mp.sqrt(8*mp.pi))
quadcheck('r2p3_y1_normalization',lambda t:mp.exp(-t*t/12)/mp.sqrt(12*mp.pi),mp.mpf(1))
quadcheck('r2p3_y2_normalization',lambda t:mp.exp(-(t-4)**2/4)/mp.sqrt(4*mp.pi),mp.mpf(1))
quadcheck('r2p8_posterior_first_factor',lambda th:mp.exp(-(th-mp.mpf('.5'))**2)/mp.sqrt(mp.pi),mp.mpf(1))
identity={'reviewer_identity':'independent mathematical reviewer /root/ml_blind_exams','context_isolation_statement':'The mathematical inputs used were only exam-1/questions.json, exam-2/questions.json and their README.md files. No course repository content, original source HTML, explanations, answer fragments, audits, harnesses, previous reviews, reference answers, memory files or parent task transcripts were consulted. All derivations and calculations in this artifact were independently authored from the supplied conditions. No comparison with reference answers has been performed.','input_resources':'Both packets list empty figure_resources arrays; no external figures or web resources were used.','approval_claim':False}
rounds=[]
for p in packets:
 rnd=p['round']; assert len(results[rnd])==len(p['questions'])
 rounds.append({'round':rnd,'packet_payload_sha256':p['packet_payload_sha256'],'question_payload_sha256':p['question_payload_sha256'],'reviewer':identity,'results':results[rnd],'unresolved_issues':[]})
doc={'schema_version':1,'artifact_status':'frozen_independent_derivations','reviewer':identity,'rounds':rounds,'verification':{'exact_symbolic_checks':checks,'numerical_checks':numeric},'coverage':{'round_1_questions':len(results[1]),'round_1_subparts':sum(len(q['subparts']) for q in results[1]),'round_2_questions':len(results[2]),'round_2_subparts':sum(len(q['subparts']) for q in results[2])},'unresolved_issues':[]}
(OUT/'results.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
lines=['# Frozen independent derivations','',identity['context_isolation_statement'],'','No approval or reference-answer comparison is asserted.','']
for rnd in rounds:
 lines.extend([f"## Round {rnd['round']}",'',f"Packet SHA-256: `{rnd['packet_payload_sha256']}`",f"Question-array SHA-256: `{rnd['question_payload_sha256']}`",''])
 for q in rnd['results']:
  lines.extend([f"### {q['id']}",'',f"Input SHA-256: `{q['input_sha256']}`",''])
  for c in q['assumptions_dimension_normalization_checks']: lines.append('- '+c)
  lines.append('')
  for part in q['subparts']:
   lines.extend([f"#### ({part['id']}) [{part['method']}]",''])
   lines.extend(f'{i}. {step}' for i,step in enumerate(part['derivation'],1))
   lines.extend(['','Conclusion: '+part['conclusion'],''])
lines.extend(['## Independent computation checks','',f'{len(checks)} exact symbolic checks and {len(numeric)} finite tolerance numerical checks completed. These supplement the derivations; finite samples are not used as a proof.','',f"Coverage: {doc['coverage']}",'','Unresolved items: none.'])
(OUT/'derivations.md').write_text('\n'.join(lines)+'\n')
(OUT/'calculation_output.json').write_text(json.dumps({'symbolic_checks':checks,'numerical_checks':numeric},ensure_ascii=False,indent=2)+'\n')
manifest={'results_sha256':hashlib.sha256((OUT/'results.json').read_bytes()).hexdigest(),'derivations_sha256':hashlib.sha256((OUT/'derivations.md').read_bytes()).hexdigest(),'derivation_script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'frozen_status':'independent_results_frozen_before_reference_comparison'}
(OUT/'freeze_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'coverage':doc['coverage'],'exact_checks':len(checks),'numeric_checks':len(numeric),'unresolved':0,'results':str(OUT/'results.json'),'freeze_manifest':manifest},indent=2))
