# Frozen independent derivations

The mathematical inputs used were only exam-1/questions.json, exam-2/questions.json and their README.md files. No course repository content, original source HTML, explanations, answer fragments, audits, harnesses, previous reviews, reference answers, memory files or parent task transcripts were consulted. All derivations and calculations in this artifact were independently authored from the supplied conditions. No comparison with reference answers has been performed.

No approval or reference-answer comparison is asserted.

## Round 1

Packet SHA-256: `47569e0f7214598ea817d0fdc85ce01b3f395c41dad215df16f5fe13f0ad2915`
Question-array SHA-256: `2b7713da873f5791aff569bd24b69baeb9257b6a0aff8c5d83fae335676fa236`

### p1

Input SHA-256: `23130a376c8d8c8eb2b0674e3474d4a6e9691b6ff77365ad2015c74c31890867`

- V is 3x3 and U is 3x2; coefficients are real.
- The column plane is {(a,b,a+b):a,b real}.

#### (a) [proof]

1. v1+v2=(1,1,2)^T=v3.
2. The coefficients (1,1,-1) are nonzero and give zero.

Conclusion: Linearly dependent; rank V=2 since v1,v2 have independent first two coordinates.

#### (b) [exact]

1. First two equations give alpha1+alpha3=2 and alpha2+alpha3=1.
2. With alpha3=t, alpha=(2-t,1-t,t)^T; the third equation is 3=3.
3. Every vector in col(V) satisfies its third coordinate = first + second. For c this would require 4=3.

Conclusion: For b all solutions are (2-t,1-t,t)^T, t real. For c there is no solution.

#### (c) [exact]

1. Inner products give U^T U=[[2,1],[1,2]] with determinant 3.
2. The 2x2 inverse formula gives (U^T U)^-1=(1/3)[[2,-1],[-1,2]].
3. V^T V=[[2,1,3],[1,2,3],[3,3,6]] annihilates (1,1,-1)^T.

Conclusion: U^T U is invertible; V^T V is singular.

### p2

Input SHA-256: `381a8b833a311f67f2550e5c81aaf5daf0d988da84b4812f757752e7c7449fb6`

- f maps R^2 to R^2; J is 2x2; gradient is 2x1 and Hessian 2x2.
- A is symmetric.

#### (a) [symbolic]

1. Differentiate each output with respect to x1,x2: J_f(x)=[[2x1,1],[x2,x1]].
2. Substitute x=(1,2)^T.

Conclusion: J_f(1,2)=[[2,1],[2,1]], dimension 2x2.

#### (b) [symbolic]

1. x^T A x=4x1^2+2x1x2+2x2^2.
2. q=2x1^2+x1x2+x2^2-x1.
3. Differentiate componentwise.

Conclusion: gradient q=(4x1+x2-1,x1+2x2)^T=A x-b; Hessian=A.

#### (c) [proof]

1. From x1+2x2=0 get x1=-2x2. Then -7x2=1.
2. Stationary point xhat=(2/7,-1/7)^T.
3. For nonzero h, h^T A h=4(h1+h2/4)^2+(7/4)h2^2>0.
4. q(xhat+h)=q(xhat)+(1/2)h^T A h since A xhat=b.

Conclusion: Unique global minimum at (2/7,-1/7)^T; value -1/7.

### p3

Input SHA-256: `e3e3fd0a1ea3e28c3f4cc53f88b4b5c0da212d6ec9a557f6bfb0ab89ad1a2153`

- Both second Gaussian arguments are variances.
- Univariate Lebesgue densities; q must integrate to one.

#### (a) [symbolic]

1. z^2+(z-2)^2/3=(4/3)z^2-(4/3)z+4/3.
2. Completing the square gives (4/3)(z-1/2)^2+1.

Conclusion: Completed square: (4/3)(z-1/2)^2+1.

#### (b) [exact]

1. The exponent of g is -1/2 times the expression in (a).
2. The z-dependent part is -(z-1/2)^2/[2(3/4)].
3. A Gaussian kernel of variance 3/4 integrates to sqrt(2 pi (3/4)).

Conclusion: q(z)=sqrt(2/(3 pi))*exp[-(2/3)(z-1/2)^2]; mean 1/2, variance 3/4.

#### (c) [exact]

1. Product leading coefficient is 1/(2 pi sqrt(3)).
2. g(z)=exp(-1/2)/(2 pi sqrt(3))*exp[-(2/3)(z-1/2)^2].
3. Integrate using sqrt(3 pi/2) for the kernel.

Conclusion: Z=exp(-1/2)/sqrt(8 pi). This is not 1, so g itself is not a probability density; g=Z q.

### p4

Input SHA-256: `04b56451a87f21c80e85494d7ba3596cf4e3ee1887bb65c5da8e380e9400d8f1`

- Phi is 3x2, y is 3x1, theta is 2x1; all coefficient priors have variance 1.
- Noise variance is 1; Gaussian ML minimizes squared residual norm.

#### (a) [exact]

1. Write feature rows (1,-1),(1,0),(1,1).
2. Sum row outer products and y-weighted rows.

Conclusion: Phi=[[1,-1],[1,0],[1,1]], Phi^T Phi=diag(3,2), Phi^T y=(5,4)^T.

#### (b) [exact]

1. Set Phi^T Phi theta=Phi^T y.
2. Solve 3 theta0=5 and 2 theta1=4.
3. At x*=2 use feature (1,2)^T.

Conclusion: theta_ML=(5/3,2)^T; mean prediction=17/3.

#### (c) [exact]

1. Negative log posterior up to constants is (1/2)||y-Phi theta||^2+(1/2)||theta||^2.
2. Gradient zero gives (Phi^T Phi+I)theta=Phi^T y=>(4 theta0,3 theta1)=(5,4).

Conclusion: theta_MAP=(5/4,4/3)^T; mean prediction=47/12. The prior penalizes both coefficients and shrinks them toward zero.

### p5

Input SHA-256: `3f9296b6814df43babb780698287314ee424fe9e0e3a4d8c1fdec2b1abbfd789`

- Population distribution has three equally weighted atoms, so use divisor 3.
- X,Y means are 2x1; all covariance matrices and C_XY are 2x2.

#### (a) [exact]

1. Mean is ((0+2+0)/3,(0+0+2)/3)^T.
2. E[XX^T]=diag(4/3,4/3).
3. Subtract mu_X mu_X^T=[[4/9,4/9],[4/9,4/9]].

Conclusion: mu_X=(2/3,2/3)^T; Sigma_X=[[8/9,-4/9],[-4/9,8/9]].

#### (b) [exact]

1. E[AX+b]=A mu_X+b.
2. Y-mu_Y=A(X-mu_X), hence Sigma_Y=A Sigma_X A^T and C_XY=Sigma_X A^T.
3. Multiply the matrices with the indicated order.

Conclusion: mu_Y=(7/3,-1)^T; Sigma_Y=diag(8/9,8/3); C_XY=[[4/9,4/3],[4/9,-4/3]].

#### (c) [proof]

1. The possible Y values are (1,-1),(3,1),(3,-3), each of probability 1/3.
2. Cov(Y1,Y2)=0 from (b), so the coordinates are uncorrelated.
3. P(Y1=1,Y2=-1)=1/3, whereas P(Y1=1)P(Y2=-1)=(1/3)(1/3)=1/9.

Conclusion: Uncorrelated but dependent, established directly from their actual discrete joint distribution.

### p6

Input SHA-256: `854b2212f71fef6cd9c55b8f25f784a290f123b3637dffa6c7435fe4ee17c333`

- N>=2 and Phi is N x 2 with full column rank; theta is 2x1, y is N x1.
- sigma^2 is a fixed positive scalar, so rescaling the objective by 1/(2 sigma^2) preserves minimizers.

#### (a) [proof]

1. For fixed x_n and theta, the deterministic mean is theta0+theta1 x_n; adding epsilon_n shifts its Gaussian.
2. Each y_n is a function only of epsilon_n and fixed quantities. Independence of the noises therefore gives conditional independence of the observations.

Conclusion: y_n | x_n,theta ~ N(theta0+theta1 x_n,sigma^2), conditionally independent.

#### (b) [symbolic]

1. Multiply the independent densities (2 pi sigma^2)^(-1/2) exp[-(y_n-phi_n^T theta)^2/(2 sigma^2)].
2. Take minus the logarithm of the product.

Conclusion: p(y|Phi,theta)=(2 pi sigma^2)^(-N/2)exp[-||y-Phi theta||^2/(2 sigma^2)]; L=N/2 log(2 pi sigma^2)+||y-Phi theta||^2/(2 sigma^2).

#### (c) [proof]

1. By definition Rhat=||y-Phi theta||^2/N.
2. L=N/2 log(2 pi sigma^2)+N/(2 sigma^2) Rhat.
3. The additive term is independent of theta and N/(2 sigma^2)>0.

Conclusion: L and squared-loss empirical risk have exactly the same minimizing theta.

#### (d) [symbolic]

1. SSE=(y-Phi theta)^T(y-Phi theta)=y^T y-2 theta^T Phi^T y+theta^T Phi^T Phi theta.
2. Phi^T Phi is symmetric, so the column gradient is -2 Phi^T y+2 Phi^T Phi theta.
3. Setting it to zero gives the normal equations.

Conclusion: Phi^T Phi theta=Phi^T y; gradient Rhat=(2/N)(Phi^T Phi theta-Phi^T y).

#### (e) [proof]

1. For nonzero h, h^T Phi^T Phi h=||Phi h||^2>0 by full column rank.
2. Thus the normal equations have theta_ML=(Phi^T Phi)^-1 Phi^T y, and the Hessian of L=Phi^T Phi/sigma^2 is positive definite.
3. At theta_ML+h, L-L_min=||Phi h||^2/(2 sigma^2)>0.
4. Changing features to (1,x,x^2) keeps the mean linear in the three coefficients, even though it is quadratic in x.

Conclusion: Unique ML minimum (Phi^T Phi)^-1 Phi^T y. Polynomial features still define linear regression in parameters; the new design must separately have full column rank to ensure uniqueness.

### p7

Input SHA-256: `8b466d4670ba071bc75f9cea911300247906079f5fcd0dcac575de851983514d`

- Phi is N x K with no rank assumption; sigma^2,tau^2 positive; theta,m0 are Kx1.
- lambda=sigma^2/tau^2>0 applies to every coefficient, including an intercept.

#### (a) [symbolic]

1. Bayes: p(theta|y,Phi)=p(y|Phi,theta)p(theta)/p(y|Phi).
2. The numerator uses N(Phi theta,sigma^2 I_N) times N(m0,tau^2 I_K).
3. Evidence integrates that numerator over theta and thus is constant with respect to theta.

Conclusion: Posterior is proportional to likelihood times prior; evidence is independent of theta.

#### (b) [symbolic]

1. The product leading coefficient is (2 pi sigma^2)^(-N/2)(2 pi tau^2)^(-K/2).
2. Its exponent is -||y-Phi theta||^2/(2 sigma^2)-||theta-m0||^2/(2 tau^2).
3. Minus log posterior adds C=N/2 log(2 pi sigma^2)+K/2 log(2 pi tau^2)+log p(y|Phi).

Conclusion: Negative log posterior = ||y-Phi theta||^2/(2 sigma^2)+||theta-m0||^2/(2 tau^2)+C.

#### (c) [symbolic]

1. Gradient of the first quadratic is Phi^T(Phi theta-y)/sigma^2.
2. Gradient of the second is (theta-m0)/tau^2.
3. Set their sum to zero and multiply by sigma^2.

Conclusion: (Phi^T Phi+lambda I_K)theta=Phi^T y+lambda m0.

#### (d) [symbolic]

1. The equation in (c) gives theta_MAP=(Phi^T Phi+lambda I_K)^-1(Phi^T y+lambda m0).
2. Multiplying the negative log posterior by 2 sigma^2 leaves SSE+lambda||theta-m0||^2 plus a constant.

Conclusion: MAP formula above with relative penalty lambda=sigma^2/tau^2.

#### (e) [proof]

1. For any h != 0, h^T(Phi^T Phi+lambda I)h=||Phi h||^2+lambda||h||^2.
2. The first term is nonnegative and the second strictly positive.

Conclusion: The coefficient matrix is positive definite, hence invertible, regardless of column dependence; MAP is unique.

#### (f) [exact]

1. Phi^T Phi=[[5,5],[5,5]], Phi^T y=(5,5)^T.
2. For lambda=1 solve [[6,5],[5,6]]theta=(5,5)^T: subtraction gives theta1=theta2 and then 11 theta1=5.
3. For lambda=0, predictions match y whenever theta1+theta2=1.
4. For general positive lambda the symmetric solution has both entries 5/(10+lambda).

Conclusion: lambda=1: theta=(5/11,5/11)^T. lambda=0: infinitely many solutions (a,1-a)^T. As lambda tends to infinity theta tends to (0,0)^T=m0.

### p8

Input SHA-256: `465239aead412b8102cce5c976e1c5c8cbaceb5492a795cda6116f53c6ebb40c`

- Scalar theta, x*=2, noise variances and prior variance are 2.
- Conditional posterior uncertainty and independent future observation noise are distinct variance contributions.

#### (a) [symbolic]

1. Likelihood is N(2|theta,2)N(0|theta,2); multiply by N(theta|1,2).
2. Leading factor is (4 pi)^(-3/2).
3. Exponent is -[(2-theta)^2+theta^2+(theta-1)^2]/4.

Conclusion: Product is (4 pi)^(-3/2) exp[-((2-theta)^2+theta^2+(theta-1)^2)/4].

#### (b) [symbolic]

1. Sum of squares =3 theta^2-6 theta+5.
2. Write -(3 theta^2-6 theta+5)/4=-1/2[(3/2)theta^2-3theta+5/2].

Conclusion: A=3/2, b=3/2, c=5/2.

#### (c) [exact]

1. A theta^2-2b theta+c=(3/2)(theta-1)^2+1.
2. The constant exp(-1/2) cancels in normalization.
3. The remaining Gaussian kernel has variance A^-1=2/3 and integral sqrt(4 pi/3).

Conclusion: theta|D ~ N(1,2/3), with density sqrt(3/(4 pi)) exp[-3(theta-1)^2/4].

#### (d) [proof]

1. For f*=2theta, conditional expectation is 2 E[theta|D]=2.
2. Conditional variance is 4 Var(theta|D)=8/3. Linear transforms of a Gaussian remain Gaussian.

Conclusion: f*|D ~ N(2,8/3).

#### (e) [proof]

1. Future noise is independent of theta and D and has mean 0, variance 2.
2. Means add, and independent variances add: 8/3+2=14/3.
3. A sum of independent Gaussians is Gaussian.

Conclusion: y*|D ~ N(2,14/3).

#### (f) [exact]

1. The posterior quadratic is minimized at theta=1, its mean and mode.
2. Fixing theta to MAP sets f*=2 deterministically, then adds only N(0,2) observation noise.

Conclusion: theta_MAP=1; plug-in y* ~ N(2,2). Full posterior prediction has additional variance 8/3 from uncertain theta propagated through x*=2.

### p9

Input SHA-256: `08ab9d83d215e9c57c702dea76d016f23aa53d6abf262dc8c1243e23b6d18fec`

- v_j>0; scalar observation evidence is a density value at y, not P(Y=y).
- Model choice in (e) uses the larger model posterior probability under the given model priors.

#### (a) [symbolic]

1. Marginalize the joint model p(y,theta|M_j)=p(y|theta,M_j)p(theta|M_j).
2. p(y|M_j)=integral N(y|theta,1)N(theta|0,v_j) dtheta.
3. The prior describes theta before the observed y; integrating against the posterior would count the observation again and is not this marginalization identity.

Conclusion: Evidence integral uses the prior, not posterior.

#### (b) [symbolic]

1. Let v=v_j. (y-theta)^2+theta^2/v=((v+1)/v)(theta-v y/(v+1))^2+y^2/(v+1).
2. The leading factor of the product is 1/(2 pi sqrt(v)).
3. Integral of the theta kernel is sqrt(2 pi v/(v+1)).

Conclusion: p(y|M_j)=[2 pi(v_j+1)]^(-1/2) exp[-y^2/(2(v_j+1))]; normalized N(0,v_j+1).

#### (c) [exact]

1. Set y=0 in (b).
2. For v1=1 use total variance 2; for v2=4 use variance 5.

Conclusion: p(0|M1)=1/sqrt(4 pi); p(0|M2)=1/sqrt(10 pi).

#### (d) [exact]

1. B12=p(0|M1)/p(0|M2)=sqrt(10 pi)/sqrt(4 pi)=sqrt(5/2)>1.

Conclusion: Data evidence favors M1.

#### (e) [proof]

1. Bayes gives P(Mj|y)=p(y|Mj)P(Mj)/p(y).
2. Dividing cancels common p(y), so posterior odds=B12 times prior odds.
3. Here prior odds=(1/3)/(2/3)=1/2. Posterior odds=sqrt(5/2)/2.
4. With only two models, P(M1|0)=B12/(B12+2). Since B12<2, that posterior is <1/2.

Conclusion: P(M1|0)=sqrt(5)/(sqrt(5)+2sqrt(2)); choose M2 by larger posterior despite B12>1.

### p10

Input SHA-256: `0c85ced5c682c249609ae174d21252d129ae6941f95b2f3a2d10dba101248bd8`

- Phi is N x K generally, here 3x2; full column rank, Euclidean inner product.
- P is N x N; r,y,yhat are N x1.

#### (a) [proof]

1. Let r=y-Phi thetahat. The path loss is ||r-t Phi h||^2=||r||^2-2t h^T Phi^T r+t^2||Phi h||^2.
2. Derivative at zero is -2 h^T Phi^T r=0 for every h.
3. Choosing h=Phi^T r implies ||Phi^T r||^2=0.

Conclusion: Phi^T r=0, so r is orthogonal to every vector in col(Phi).

#### (b) [symbolic]

1. Substitute r=y-Phi thetahat in Phi^T r=0.
2. Full column rank implies Phi^T Phi is positive definite and invertible.

Conclusion: Phi^T Phi thetahat=Phi^T y; thetahat=(Phi^T Phi)^-1 Phi^T y.

#### (c) [proof]

1. Substitution yields P=Phi(Phi^T Phi)^-1 Phi^T, dimension N x N.
2. The Gram matrix and its inverse are symmetric, so P^T=P.
3. P^2=Phi G^-1(Phi^T Phi)G^-1 Phi^T=Phi G^-1 Phi^T=P.

Conclusion: P is symmetric and idempotent, the orthogonal projector onto col(Phi).

#### (d) [exact]

1. G=diag(3,2), Phi^T y=(4,2)^T.
2. thetahat=(4/3,1)^T. Multiplication gives the matrix P and vectors below.
3. Phi^T r=(2/3-1/3-1/3,-1/3+1/3)^T=(0,0)^T.

Conclusion: P=[[1/3,1/3,1/3],[1/3,5/6,-1/6],[1/3,-1/6,5/6]]; yhat=(4/3,7/3,1/3)^T; r=(2/3,-1/3,-1/3)^T.

#### (e) [proof]

1. For any u in col(Phi), y-u=r+(yhat-u).
2. Both yhat and u lie in col(Phi), so r^T(yhat-u)=0.
3. Expand the squared norm and remove the zero cross term: ||y-u||^2=||r||^2+||yhat-u||^2.

Conclusion: Distance is at least ||r||^2, with equality only for u=yhat. Thus yhat is the unique closest point.

## Round 2

Packet SHA-256: `5b87c9053cd6313f909b20df691784f186b9f7343fafb3e5ccd7e8b0d6e28bd4`
Question-array SHA-256: `2d293177e81af15da7a572049d9971f0f5b91e9508bbe180ab83c0bd954e44b9`

### p1

Input SHA-256: `f0562b7dc4b3d269bab47725fdc61c5b3cf189dc451da4fc18df1bd1413b3586`

- t is real; V(t) is 3x3; coefficients are real.

#### (a) [symbolic]

1. V=[[1,0,1],[0,1,1],[1,1,t]].
2. Replace row3 by row3-row1-row2, obtaining upper triangular diagonal 1,1,t-2 without changing determinant.

Conclusion: det V(t)=t-2; the columns are a basis of R^3 exactly when t != 2.

#### (b) [exact]

1. At t=2 the third row is the sum of the first two.
2. For RHS (1,2,3)^T, alpha1+alpha3=1 and alpha2+alpha3=2; let alpha3=s.
3. Every vector in col(V(2)) has z=x+y, which excludes (1,2,4)^T.

Conclusion: All solutions for (1,2,3)^T are (1-s,2-s,s)^T, s real; none for (1,2,4)^T.

#### (c) [exact]

1. At t=3 write alpha1=1-alpha3, alpha2=2-alpha3.
2. Third equation becomes 3+alpha3=4, so alpha3=1.
3. det V(3)=1 so its column space is R^3, whereas col(V(2)) is only the plane z=x+y.

Conclusion: Unique solution alpha=(0,1,1)^T; changing t expands the column space from a plane to all R^3.

### p2

Input SHA-256: `51d1be4f7fb1dfdf0e0e24e526d984053ee7ba0cd8902474335d79b85e8a0c4c`

- f:R^2->R^2; J is 2x2; loss is scalar; gradients are 2x1.
- The specified directional derivative uses d itself, not d normalized to unit length.

#### (a) [symbolic]

1. Differentiate f1=x1+x2 and f2=x1x2 row by row.

Conclusion: J_f(x)=[[1,1],[x2,x1]], J_f(1,2)=[[1,1],[2,1]], dimension 2x2.

#### (b) [symbolic]

1. gradient_z ell=z-(1,2)^T. At x=(1,2), f(x)=(3,2)^T, so gradient ell=(2,0)^T.
2. Chain rule with column gradients gives gradient_x L=J_f^T gradient_z ell=(2,2)^T.
3. Directly L=(1/2)[(x1+x2-1)^2+(x1x2-2)^2].
4. Its derivatives are x1+x2-1+x2(x1x2-2) and x1+x2-1+x1(x1x2-2); both are 2 at the given point.

Conclusion: gradient_x L(1,2)=(2,2)^T by both derivations.

#### (c) [proof]

1. D_d L=gradient L^T d=(2,2)(1,-1)^T=0.
2. Along this path f=(3,2+h-h^2)^T, so L=2+(1/2)(h-h^2)^2, whose derivative at zero is 0.
3. A stationary point requires zero gradient, equivalently every directional derivative zero. Here gradient=(2,2)^T is not zero.

Conclusion: D_d L=0, but (1,2)^T is not stationary; derivative along (1,1)^T is 4.

### p3

Input SHA-256: `e2dc6d307aea0d93ed5cc9a61b9643e6f56ef10f32d91af3d8d0be34eedb34b2`

- X,Y are jointly Gaussian two-dimensional vectors; Sigma is positive definite (eigenvalues 3 and 1).
- A is invertible with determinant -2, so Y has an ordinary two-dimensional density.

#### (a) [exact]

1. E[Y]=A mu+b=(0,2)^T+(0,2)^T.
2. Cov(Y)=A Sigma A^T.
3. A Sigma=[[3,3],[1,-1]], hence covariance is diag(6,2).

Conclusion: E[Y]=(0,4)^T; Cov(Y)=diag(6,2).

#### (b) [exact]

1. Affine Gaussian transformation yields Y~N((0,4)^T,diag(6,2)).
2. det covariance=12, inverse=diag(1/6,1/2).
3. For dimension 2 the density coefficient is (2 pi)^-1 det(cov)^-1/2.

Conclusion: Y1~N(0,6), Y2~N(4,2); p_Y=1/(4 pi sqrt(3))*exp[-y1^2/12-(y2-4)^2/4].

#### (c) [proof]

1. The density in (b) factors into its two univariate Gaussian densities, proving independence.
2. Original Cov(X1,X2)=1 != 0. Independent finite-variance variables have zero covariance; this excludes independence for X1,X2.

Conclusion: Y1,Y2 are independent. X1,X2 are dependent. The Gaussian property makes zero cross covariance sufficient for Y independence.

### p4

Input SHA-256: `b90dfb4bedf1d6f0ae95f979d14c351ba9acc071ef60658c4d013afabe633f9f`

- All Gaussian second arguments are variances; theta is scalar.
- p(y=3) denotes the value of an evidence density, not the probability of a singleton.

#### (a) [symbolic]

1. Each density has leading coefficient (4 pi)^-1/2; product coefficient is 1/(4 pi).
2. The inner quadratic ((theta+1)^2+(3-theta)^2)/2=theta^2-2theta+5=(theta-1)^2+4.
3. The outer exponent factor remains -1/2.

Conclusion: g(theta)=1/(4 pi)*exp[-(theta-1)^2/2-2].

#### (b) [exact]

1. Divide the Gaussian kernel by its integral sqrt(2 pi).
2. The likelihood alone exp[-(3-theta)^2/4] is maximized at theta=3; the posterior kernel is maximized at theta=1.

Conclusion: theta|y=3~N(1,1); density (2 pi)^-1/2 exp[-(theta-1)^2/2]; ML=3, MAP=1.

#### (c) [exact]

1. Integrate (a): Z=exp(-2)/(4 pi)*sqrt(2 pi)=exp(-2)/sqrt(8 pi).
2. Equivalently prior predictive y has mean -1, variance 2+2=4 and evaluate its density at 3.
3. Z is constant in theta; posterior is g(theta)/Z and integrates to one over theta.

Conclusion: Z=exp(-2)/sqrt(8 pi), the evidence density value for y=3; it is not the posterior density function of theta.

### p5

Input SHA-256: `98d1a825f91f0a0654f639a6c98bcd6522f2e9cb505541e42c96ec6d69d1a0d4`

- Phi is 3x2, theta is 2x1, y is 3x1; model is linear in theta.
- Noise and both coefficient prior variances are 1; same feature at two inputs forces equal fitted means there.

#### (a) [exact]

1. Feature rows are (1,1),(1,0),(1,1).
2. Sum row outer products to get G=[[3,2],[2,2]]; sum y_n phi_n gives (6,6)^T.
3. det G=6-4=2>0, so duplicate rows do not destroy independent columns.

Conclusion: Phi=[[1,1],[1,0],[1,1]], G=[[3,2],[2,2]], Phi^T y=(6,6)^T; Gram is invertible.

#### (b) [exact]

1. Normal equations: 3 theta0+2 theta1=6 and 2 theta0+2 theta1=6, giving theta0=0 and theta1=3.
2. yhat=(3,0,3)^T, so r=y-yhat=(-1,0,1)^T.
3. r^T r=2; feature at 2 is (1,4)^T.

Conclusion: theta_ML=(0,3)^T; residual=(-1,0,1)^T; SSE=2; predicted mean at x*=2 is 12.

#### (c) [exact]

1. MAP solves (G+I)theta=(6,6)^T with G+I=[[4,2],[2,3]].
2. Inverse is (1/8)[[3,-2],[-2,4]], yielding (3/4,3/2)^T.
3. Prediction=(3/4)+4(3/2)=27/4.
4. The mean theta0+theta1 x^2 is a linear combination of fixed features with unknown coefficients.

Conclusion: theta_MAP=(3/4,3/2)^T; predicted mean 27/4. It is linear regression in coefficients despite nonlinear dependence on input x.

### p6

Input SHA-256: `7ca715fda202a2ff8e5bf8fcc7dfeea1096130069fb338c58d04a63229e4c093`

- x,y are N x1, theta is scalar; x^T x>0, sigma^2>0.
- No intercept is present; P is N x N and its range is span{x}.

#### (a) [symbolic]

1. Given x and theta, y_n~N(theta x_n,sigma^2).
2. Independence of noises makes observations conditionally independent.
3. Multiply their univariate densities.

Conclusion: p(y|x,theta)=(2 pi sigma^2)^(-N/2)exp[-sum_n(y_n-theta x_n)^2/(2 sigma^2)].

#### (b) [symbolic]

1. Taking minus log gives N/2 log(2 pi sigma^2)+SSE(theta)/(2 sigma^2).
2. The first term does not depend on theta; the second is a strictly positive multiple of SSE.

Conclusion: ML is equivalent to minimizing SSE(theta)=sum_n(y_n-theta x_n)^2.

#### (c) [symbolic]

1. SSE=sum y_n^2-2theta sum x_n y_n+theta^2 sum x_n^2.
2. Derivative=-2sum x_n y_n+2theta sum x_n^2.
3. Set derivative to zero and divide by sum x_n^2>0.

Conclusion: thetahat=(sum x_n y_n)/(sum x_n^2); positive denominator is guaranteed by the stated assumption.

#### (d) [proof]

1. Second derivative SSE=2sum x_n^2>0, so the quadratic has a unique global minimum.
2. The negative log likelihood second derivative is (sum x_n^2)/sigma^2>0.
3. Use vector inner products for the sums.

Conclusion: thetahat=(x^T y)/(x^T x), unique global ML minimum.

#### (e) [proof]

1. yhat=x(x^T y)/(x^T x)=P y with P=xx^T/(x^T x).
2. x^T(y-yhat)=x^T y-(x^T x)(x^T y)/(x^T x)=0.

Conclusion: P=xx^T/(x^T x); residual is orthogonal to x.

#### (f) [exact]

1. x^T x=1+4+1=6; x^T y=1+6+0=7.
2. thetahat=7/6; yhat=(7/6,7/3,-7/6)^T.
3. r=(-1/6,2/3,7/6)^T; SSE=(1+16+49)/36=11/6.

Conclusion: thetahat=7/6, yhat=(7/6,7/3,-7/6)^T, SSE=11/6; P=(1/6)[[1,2,-1],[2,4,-2],[-1,-2,1]].

### p7

Input SHA-256: `224d66c44a957b5d0367029caf3cefb3f00fdd7426e95d2b65be10f9a7ce9f8e`

- theta,m0 are 2x1; S0 is positive definite 2x2.
- s=sigma^2>0; prior precision S0^-1=diag(1/4,1), so unequal prior variances give unequal coefficient penalties.

#### (a) [symbolic]

1. Likelihood coefficient is (2 pi sigma^2)^-1 and exponent -||y-Phi theta||^2/(2 sigma^2).
2. Prior coefficient is (2 pi)^-1 det(S0)^-1/2 and exponent -(theta-m0)^T S0^-1(theta-m0)/2.
3. Posterior is their product divided by p(y|Phi); collect all leading coefficients and log evidence in C.

Conclusion: Negative log posterior=C+||y-Phi theta||^2/(2 sigma^2)+(theta-m0)^T S0^-1(theta-m0)/2; C=log(2 pi sigma^2)+log(2 pi)+(1/2)log det S0+log p(y|Phi).

#### (b) [symbolic]

1. For the likelihood term, gradient is Phi^T(Phi theta-y)/sigma^2.
2. For the prior term, symmetry of S0^-1 gives S0^-1(theta-m0).
3. The precision appears because Gaussian density measures squared displacement in units of covariance; here the penalties are (theta0-2)^2/4 and theta1^2 before the factor 1/2.

Conclusion: The two column gradients are Phi^T(Phi theta-y)/sigma^2 and S0^-1(theta-m0).

#### (c) [symbolic]

1. Set sum of gradients to zero: (Phi^T Phi/sigma^2+S0^-1)theta=Phi^T y/sigma^2+S0^-1 m0.
2. Multiply by sigma^2 and invert the positive definite coefficient matrix.

Conclusion: theta_MAP=(Phi^T Phi+sigma^2 S0^-1)^-1(Phi^T y+sigma^2 S0^-1 m0).

#### (d) [proof]

1. For h !=0, h^T(Phi^T Phi+sigma^2 S0^-1)h=||Phi h||^2+sigma^2 h^T S0^-1 h.
2. S0^-1 is positive definite and sigma^2>0, so the second term is strictly positive.

Conclusion: Coefficient matrix is positive definite and MAP is the unique global posterior mode.

#### (e) [exact]

1. Phi^T Phi=2I, Phi^T y=(4,4)^T and S0^-1 m0=(1/2,0)^T.
2. At sigma^2=1, coefficient matrix=diag(9/4,3) and RHS=(9/2,4)^T.
3. theta_MAP=(2,4/3)^T; mean prediction=2+2(4/3)=14/3.
4. ML solves 2I theta=(4,4)^T.

Conclusion: MAP=(2,4/3)^T, prediction 14/3; ML=(2,2)^T, prediction 6.

#### (f) [symbolic]

1. With s=sigma^2, theta0=(4+s/2)/(2+s/4)=2.
2. theta1=4/(2+s).
3. As s->0+, noise becomes negligible and theta->(2,2)^T, the exact fitting ML coefficients.
4. As s->infinity likelihood loses information and theta->(2,0)^T=m0.

Conclusion: theta_MAP(s)=(2,4/(2+s))^T; limits are ML at zero noise and prior mean at infinite noise.

### p8

Input SHA-256: `715bd874b8b09e430a4e8432723086ce2fddd9908c86b1e77dee3313dc62d54b`

- theta is 2x1; Phi is 2x2; B,S are 2x2, b,m are 2x1, c scalar.
- All future noises are independent of the training data and theta; posterior uncertainty in theta is shared by future predictions.

#### (a) [symbolic]

1. Product is (4 pi)^-1(2 pi)^-1 exp[-||y-Phi theta||^2/4-theta^T theta/2].
2. Inside -1/2, expand (1/2)(y-Phi theta)^T(y-Phi theta)+theta^T theta.
3. Collect the quadratic, linear, and constant terms.

Conclusion: B=I+(1/2)Phi^T Phi, b=(1/2)Phi^T y, c=(1/2)y^T y.

#### (b) [symbolic]

1. B is positive definite since h^T B h=||h||^2+(1/2)||Phi h||^2>0.
2. Set m=B^-1 b, S=B^-1.
3. theta^T B theta-2 b^T theta+c=(theta-m)^T B(theta-m)+c-b^T B^-1 b.
4. The final constant cancels in normalization; the Gaussian kernel integral is (2 pi)^(2/2)det(B)^-1/2.

Conclusion: Posterior N(m,S) has density [2 pi sqrt(det S)]^-1 exp[-(theta-m)^T S^-1(theta-m)/2].

#### (c) [exact]

1. Phi^T Phi=2I; Phi^T y=(2,2)^T; y^T y=4.
2. Hence B=2I, b=(1,1)^T, c=2.
3. m=B^-1 b=(1/2,1/2)^T and S=(1/2)I; c-b^T B^-1 b=1.

Conclusion: theta|y~N((1/2,1/2)^T,(1/2)I), density (1/pi)exp[-||theta-(1/2,1/2)^T||^2].

#### (d) [proof]

1. For any fixed phi_*, E[f_*|y]=phi_*^T m.
2. Var(f_*|y)=E[phi_*^T(theta-m)(theta-m)^T phi_*|y]=phi_*^T S phi_*.
3. A linear functional of a Gaussian is Gaussian (possibly degenerate if phi_*=0).
4. At x*=1, phi_*=(1,1)^T, giving mean 1 and variance 1.

Conclusion: f_*|y~N(phi_*^T m,phi_*^T S phi_*); at x*=1 this is N(1,1).

#### (e) [proof]

1. Independent future noise has conditional mean zero and variance 2.
2. Thus E[y_*|y]=phi_*^T m and Var(y_*|y)=phi_*^T S phi_*+2.
3. At x*=1 full posterior prediction is N(1,3).
4. Gaussian posterior mode equals m; fixing theta=m omits phi_*^T S phi_*=1.

Conclusion: y_*|y~N(phi_*^T m,2+phi_*^T S phi_*); at x*=1 N(1,3), versus MAP plug-in N(1,2).

#### (f) [proof]

1. Let a=phi(0)=(1,0)^T and d=phi(1)=(1,1)^T.
2. For two distinct future observations, Cov(a^T theta+eps0,d^T theta+eps1 | y)=a^T S d: cross terms vanish by noise independence and Cov(eps0,eps1)=0.
3. a^T S d=1/2. Their individual variances are 2+1/2=5/2 and 2+1=3.
4. Conditional on theta, independent future noises make these future observations independent. Integrating theta introduces its shared uncertainty.

Conclusion: Cross covariance is 1/2; joint posterior predictive covariance [[5/2,1/2],[1/2,3]]. The future observations are dependent after theta is integrated out, although independent given theta.

### p9

Input SHA-256: `ca1dba458a97e7e85025d6bf8aeaafbc9ba3f3ad1417017b357f1e5424f98ced`

- Observation y is 2x1; M1 parameter dimension 1, M2 dimension 2.
- All evidence values are two-dimensional densities; model space contains exactly M1,M2.

#### (a) [symbolic]

1. For M1 use B1=(1,1)^T, vartheta1=theta~N(0,1).
2. For M2 use B2=I2, vartheta2=(theta1,theta2)^T~N(0,I2).
3. For each i, p(y|Mi)=integral N_2(y|B_i vartheta_i,I2) N_{K_i}(vartheta_i|0,I_{K_i}) d vartheta_i, with K1=1,K2=2.

Conclusion: B1=[[1],[1]], B2=I2; evidence is the likelihood integrated over the respective independent Gaussian parameter priors.

#### (b) [proof]

1. E[y]=B_i E[vartheta_i]+E[eps]=0.
2. Expand E[(B_i vartheta_i+eps)(B_i vartheta_i+eps)^T].
3. The cross terms vanish because both vectors have zero means and are independent; remaining terms give C_i=B_i B_i^T+I2.
4. Independent Gaussian vectors combine to a joint Gaussian, and a linear map preserves Gaussianity.

Conclusion: M1: y~N(0,[[2,1],[1,2]]). M2: y~N(0,2I2).

#### (c) [exact]

1. In 2D, p(y|Mi)=1/(2 pi sqrt(det C_i))*exp[-y^T C_i^-1 y/2].
2. C1 determinant=3, inverse=(1/3)[[2,-1],[-1,2]]. At y=(1,-1)^T, C1^-1 y=y and y^T C1^-1 y=2.
3. C2 determinant=4, inverse=(1/2)I. Its quadratic form is 1.

Conclusion: p(y|M1)=exp(-1)/(2 pi sqrt(3)); p(y|M2)=exp(-1/2)/(4 pi).

#### (d) [exact]

1. B12=evidence1/evidence2=(2/sqrt(3))exp(-1/2).
2. B12<1 because B12^2=4/(3e)<1, using e>1+1=2>4/3.

Conclusion: B12=2 exp(-1/2)/sqrt(3); data evidence favors M2.

#### (e) [proof]

1. Divide Bayes model posteriors: P(M1|y)/P(M2|y)=[p(y|M1)/p(y|M2)] [P(M1)/P(M2)].
2. Prior odds=3, so posterior odds=2sqrt(3) exp(-1/2).
3. Convert odds O to probability O/(1+O).
4. O>1 because O^2=12/e>1 (e<3<12).

Conclusion: P(M1|y)=2sqrt(3)/(sqrt(e)+2sqrt(3)); choose M1 by larger posterior, since its prior odds outweigh the evidence preference for M2.

### p10

Input SHA-256: `8408fc448a8b87f1c91b1e0bcd89ce95a220d8b5346d1dcb8962f52a5b85f343`

- Phi is 3x2, y is 3x1; G and coefficient matrices are 2x2; P,H are 3x3.
- Both ridge coefficients have unit penalty; ordinary Euclidean orthogonality is used.

#### (a) [symbolic]

1. Q=(1/2)y^T y-theta^T Phi^T y+(1/2)theta^T G theta.
2. G=Phi^T Phi is symmetric, so column gradient=-Phi^T y+G theta.
3. Set gradient to zero.

Conclusion: Normal equations G thetahat=Phi^T y.

#### (b) [exact]

1. If columns of Phi are independent then G is positive definite, giving thetahat=G^-1 Phi^T y.
2. Here G=[[2,1],[1,2]], determinant 3>0; inverse=(1/3)[[2,-1],[-1,2]].
3. Phi^T y=(1,2)^T, giving thetahat=(0,1)^T.

Conclusion: Unique thetahat=(0,1)^T; yhat=(0,1,1)^T; r=(1,1,-1)^T.

#### (c) [proof]

1. P=Phi G^-1 Phi^T=(1/3)[[2,-1,1],[-1,2,1],[1,1,2]].
2. G^-1 symmetric implies P^T=P.
3. P^2=Phi G^-1 G G^-1 Phi^T=P; numerically the unscaled numerator matrix M obeys M^2=3M.

Conclusion: P is the stated symmetric idempotent orthogonal projector; Py=yhat.

#### (d) [exact]

1. Adding (1/2)||theta||^2 adds theta to gradient, so (G+I)theta_R=Phi^T y.
2. G+I=[[3,1],[1,3]] has inverse (1/8)[[3,-1],[-1,3]].
3. Multiply by (1,2)^T.

Conclusion: theta_R=(1/8,5/8)^T, versus ordinary least squares (0,1)^T.

#### (e) [exact]

1. H=Phi(G+I)^-1 Phi^T=(1/8)[[3,-1,2],[-1,3,2],[2,2,4]].
2. yhat_R=Hy=(1/8,5/8,3/4)^T; r_R=(7/8,11/8,-3/4)^T.
3. Ridge normal equation rearranges to Phi^T r_R=theta_R.
4. Numerically Phi^T r_R=(7/8-3/4,11/8-3/4)^T=(1/8,5/8)^T.

Conclusion: H is the stated matrix. Ridge residual is not orthogonal to col(Phi) here; Phi^T r_R=theta_R != 0, whereas ordinary least squares has Phi^T r=0.

#### (f) [proof]

1. v=Phi(1,1)^T=(1,1,2)^T.
2. Multiplication by H gives Hv=(3/4,3/4,3/2)^T=(3/4)v.
3. Applying H again gives H^2v=(9/16)v != Hv.
4. P fixes every vector in col(Phi), including Pv=P^2v=v. H is symmetric since its middle inverse matrix is symmetric, but is not idempotent.

Conclusion: H is not an orthogonal projection. Symmetry alone is insufficient: an orthogonal projector must also be idempotent.

## Independent computation checks

37 exact symbolic checks and 7 finite tolerance numerical checks completed. These supplement the derivations; finite samples are not used as a proof.

Coverage: {'round_1_questions': 10, 'round_1_subparts': 42, 'round_2_questions': 10, 'round_2_subparts': 44}

Unresolved items: none.
