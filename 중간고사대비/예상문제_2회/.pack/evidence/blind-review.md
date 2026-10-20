# 2회 쉬운 버전: 독립 검산 기록

문제만 있는 questions-only.json과 행 미분 관례 전체만 읽고 독립적으로 10문항 35소문항을 풀었다. 정답·참고 풀이·explanations·author-explanations.py는 읽지 않았다. 원본 PDF는 참조하지 않았다. 수치검사 결과를 증명의 대용으로 사용하지 않았다.

판정: 수학적 결함 0, 한영 불일치 0. 모두 중하 이하 수준이다. p10의 잔차 기호는 편집상 명확히 할 여지가 있다. p7의 penalty는 목적함수 배율을 함께 적으면 명확하다.

## 문항별 검토

- p1: 난이도 하; 한영 pass. Explicit column vectors and real coefficients; sufficient. Direct coordinate matching and one dependence relation; appropriate introductory level.
- p2: 난이도 하; 한영 pass. Row scalar derivatives and output×input Jacobian explicitly fixed in both languages. Coordinate differentiation; no Hessian or hidden transpose requirement.
- p3: 난이도 중하; 한영 pass. Second Gaussian argument explicitly variance; Z and q are unambiguous. One completion of square plus normal constant; constant factors are the main trap.
- p4: 난이도 하~중하; 한영 pass. Noise variance and both prior coefficient variances are 1; intercept regularization explicit. Centered inputs diagonalize the 2×2 Gram matrix; formulas allowed.
- p5: 난이도 하~중하; 한영 pass. Distribution, divisor 4, affine map, and no-Gaussian instruction agree. Cross-covariance uses standard Cov(X,Y)=E[(X-EX)(Y-EY)^T]. Four equiprobable corners give identity covariance; affine covariance requires correct matrix order.
- p6: 난이도 중하; 한영 pass. Fixed inputs, independent unit Gaussian noise, and row derivative explicitly fixed. Four coherent steps connect density, likelihood, ERM, and a 2×2 solve. Transpose step is pedagogically substantive but simple.
- p7: 난이도 중하; 한영 pass. Scalar parameter and unit noise; prior variance changes alone. Penalty scaling should be displayed consistently: SSE+θ² versus half-SSE+θ²/2 are equivalent. This is an answer presentation consideration, not an ill-posed question.
- p8: 난이도 중하; 한영 pass. New error independence is explicit; density interpretation at exact observation is explicit. Completing the square and affine/sum rules are enough; predictive variance distinguishes latent and noisy responses.
- p9: 난이도 중하; 한영 pass. Model priors, parameter prior variance, observation, and Bayes-factor direction explicitly fixed. Independent Gaussian sum is allowed, avoiding a difficult integral. Density versus point probability requires a short conceptual explanation.
- p10: 난이도 중하; 한영 pass. Euclidean inner product and unit isotropic Gaussian noise are clear. Fitted residual r should be explicitly denoted r=y-bθhat after (a). Exact rank-one projection and orthogonal decomposition; 3D arithmetic is short. Residual notation is a minor editorial ambiguity, not a mathematical defect.

## 독립 풀이

### p1(a) — method=proof

v1,v2 are linearly independent.

a v1+b v2=(a,2b)^T=0 implies a=0 and b=0; thus only the trivial relation exists.

### p1(b) — method=exact

c=3 v1+2 v2; the coefficients are unique.

Matching coordinates gives a=3, 2b=4, hence b=2. If two representations existed, their difference would be a zero linear combination, and part (a) forces the coefficient differences to vanish.

### p1(c) — method=proof

They are linearly dependent; v1+v2-v3=0.

v1+v2=(1,2)^T=v3. The coefficient triple (1,1,-1) is not all zero.

### p2(a) — method=symbolic

∇_x f=[2(u-1),4(v+1)] (1×2); at (0,0), [-2,4].

Differentiate each scalar coordinate: ∂f/∂u=2(u-1), ∂f/∂v=4(v+1). Assemble these as a row according to the explicitly stated convention. x is 2×1; its scalar derivative is 1×2.

### p2(b) — method=symbolic

J_g=[[1,1],[1,-2]], dimensions 2×2.

Rows index outputs (u+v,u-2v); columns index inputs (u,v). Thus the first row is [1,1] and second row [1,-2].

### p2(c) — method=proof

x=(1,-1)^T, minimum f=0; the global minimizer is unique.

Both weighted squares are nonnegative, and both vanish at u=1,v=-1. Conversely f=0 requires both squares to be zero; hence the stated point is the sole minimizer.

### p3(a) — method=symbolic

z²+(z-2)²=2(z-1)²+2.

Expand: z²+z²-4z+4=2(z²-2z+1)+2.

### p3(b) — method=exact

q=N(1,1), q(z)=(2π)^(-1/2) exp(-(z-1)²/2).

Each original variance is 2, so p0p1=(4π)^(-1) exp(-[z²+(z-2)²]/4)=(4π)^(-1) exp(-1/2) exp(-(z-1)²/2). Its z-dependent exponent has mean 1 and variance 1; normalizing gives the displayed density.

### p3(c) — method=exact

Z=exp(-1/2)/sqrt(8π); p0p1 is not itself a probability density.

Integrating the expression from (b) gives Z=(4π)^(-1) exp(-1/2) sqrt(2π)=exp(-1/2)/(2sqrt(2π)). This is positive but not 1, so the nonnegative product lacks unit integral.

### p4(a) — method=exact

Φ=[[1,-1],[1,0],[1,1]], y=(1,2,3)^T.

The three row features are φ(-1)^T=(1,-1), φ(0)^T=(1,0), φ(1)^T=(1,1). Dimensions are Φ:3×2, y:3×1, θ:2×1.

### p4(b) — method=exact

Φ^TΦ=diag(3,2), Φ^Ty=(6,2)^T, θ_ML=(2,1)^T.

Σ1=3, Σx=0, Σx²=2; Σy=6 and Σxy=-1+3=2. Multiplication by diag(1/3,1/2) gives (2,1)^T. The diagonal entries 3 and 2 are positive, so the inverse exists and the solution is unique.

### p4(c) — method=exact

θ_MAP=(3/2,2/3)^T; mean prediction at x*=0 is 3/2.

The noise variance and prior coefficient variances are 1, including the intercept, so θ_MAP=(Φ^TΦ+I2)^(-1)Φ^Ty=diag(1/4,1/3)(6,2)^T. The prior contributes θ0² as well as θ1² to the equivalent penalized SSE; hence the intercept shrinks from 2 toward the prior mean 0. φ(0)^Tθ_MAP=[1,0]θ_MAP=3/2. Standard formulas are explicitly permitted; no derivative is required here.

### p5(a) — method=exact

E[X]=(1,1)^T.

Average the four vectors: ((0+2+0+2)/4,(0+0+2+2)/4)^T=(1,1)^T.

### p5(b) — method=exact

Σ_X=I2.

Centered vectors are (-1,-1)^T,(1,-1)^T,(-1,1)^T,(1,1)^T. Each diagonal centered square averages to 1; the off-diagonal products 1,-1,-1,1 average to 0. Hence Σ_X=[[1,0],[0,1]], using divisor 4.

### p5(c) — method=symbolic

E[Y]=(3,0)^T, Cov(Y)=diag(4,1), Cov(X,Y)=diag(2,1); b has no effect on any covariance.

E[Y]=A(1,1)^T+b=(2,1)^T+(1,-1)^T=(3,0)^T. Y-E[Y]=A(X-E[X]), so Cov(Y)=AΣ_XA^T=diag(4,1) and Cov(X,Y)=E[(X-μ_X)(Y-μ_Y)^T]=Σ_XA^T=diag(2,1). Translation cancels on centering. Dimensions and order: both X,Y are 2×1; both covariance products are 2×2. Gaussianity is unnecessary.

### p6(a) — method=symbolic

p(y_n|x_n,θ)=(2π)^(-1/2) exp(-(y_n-θ0-x_nθ1)²/2); L(θ)=(2π)^(-1) exp(-[(1-θ0+θ1)²+(3-θ0-θ1)²]/2).

Conditional on the fixed inputs and θ, y_n is the translation of an N(0,1) error by θ0+x_nθ1. Conditional independence makes the joint density the product of the two displayed univariate normal densities. This is a likelihood evaluated at fixed observed responses, not a density over θ.

### p6(b) — method=symbolic

-log L=log(2π)+Q(θ)/2, with Q=(1-θ0+θ1)²+(3-θ0-θ1)².

The Gaussian product has factor (2π)^(-1), so its negative log is log(2π)+Q/2. Empirical mean squared error for N=2 is R_emp=Q/2; here the NLL equals log(2π)+R_emp. Additive constants and positive scaling leave minimizers unchanged.

### p6(c) — method=symbolic

∇_θ Q=-2(y-Φθ)^TΦ=-2y^TΦ+2θ^TΦ^TΦ=0_(1×2). Then θ^TΦ^TΦ=y^TΦ; transpose both sides to get Φ^TΦθ=Φ^Ty.

Let r=y-Φθ be 2×1. Expanding Q=y^Ty-2y^TΦθ+θ^TΦ^TΦθ and differentiating produces the displayed row, because Φ^TΦ is symmetric. Dimensions: θ 2×1, Φ 2×2, Q scalar, gradient 1×2, r^TΦ is (1×2)(2×2). Before transposition both normal-equation sides are 1×2; after transposition they are 2×1. This explicit transposition respects the new problem’s row convention.

### p6(d) — method=exact

Φ^TΦ=2I2, Φ^Ty=(4,2)^T; θ_ML=(2,1)^T and yhat=(1,3)^T; unique.

Φ=[[1,-1],[1,1]] and y=(1,3)^T. Direct products give diag(2,2) and (1+3,-1+3)^T=(4,2)^T. Thus θ=(1/2)(4,2)^T, with predictions [2-1,2+1]^T. For nonzero h, h^TΦ^TΦh=2||h||²>0, proving positive definiteness and uniqueness, beyond merely observing a numeric fit.

### p7(a) — method=symbolic

p(θ|D) ∝ p(D|θ)p(θ) ∝ exp(-[(1-θ)²+(3-θ)²+θ²]/2).

Bayes rule gives p(θ|D)=p(D|θ)p(θ)/∫p(D|t)p(t)dt. Independence supplies p(D|θ)=(2π)^(-1)exp(-[(1-θ)²+(3-θ)²]/2); prior p(θ)=(2π)^(-1/2)exp(-θ²/2). Their product is (2π)^(-3/2) times the displayed exponential. The denominator is independent of θ.

### p7(b) — method=symbolic

J(θ)=1/2[(1-θ)²+(3-θ)²]+θ²/2 + C. Equivalently, minimize SSE+θ².

Take the negative log of the product in (a). In the NLL scaling the prior adds θ²/2 to half the data SSE; after multiplying the whole objective by 2 the penalty added to the unscaled data SSE is θ². State the scaling explicitly to avoid a factor-of-two ambiguity.

### p7(c) — method=exact

θ_MAP=4/3; θ_ML=2, so MAP is closer to the prior mean 0.

Differentiate J: J′=(θ-1)+(θ-3)+θ=3θ-4. It vanishes at 4/3; J″=3>0 guarantees a unique global minimum. Without the prior, J_ML′=(θ-1)+(θ-3)=2θ-4, giving 2 with curvature 2>0. The parameter is scalar, so there is no row/column mismatch.

### p7(d) — method=exact

For prior N(0,1/4), θ_MAP=2/3; smaller prior variance increases shrinkage toward 0.

Prior precision is 4, so J_new=1/2[(1-θ)²+(3-θ)²]+2θ²+C. J_new′=(θ-1)+(θ-3)+4θ=6θ-4, yielding 2/3 with J_new″=6>0. Data are unchanged; greater precision increases the prior penalty relative to the likelihood.

### p8(a) — method=symbolic

p(y=2|θ)=(2π)^(-1/2) exp(-(2-θ)²/2).

Given θ, y is N(θ,1). Evaluate that continuous density at 2. The notation p(y=2|θ) is explicitly stipulated to mean a density value, not the zero probability of a singleton.

### p8(b) — method=exact

θ|y=2 ∼ N(1,1/2), with density π^(-1/2)exp(-(θ-1)²).

Likelihood times prior=(2π)^(-1)exp(-[(2-θ)²+θ²]/2). Complete the square: (2-θ)²+θ²=2(θ-1)²+2. Thus the product is (2π)^(-1)e^(-1)exp(-(θ-1)²). Its integral is e^(-1)/(2sqrt(π)), because ∫exp(-(θ-1)²)dθ=sqrt(π). Division yields the stated normalized posterior. The normal exponent -(θ-1)²/(2s²) gives s²=1/2.

### p8(c) — method=exact

f*|y=2 ∼ N(2,2), mean 2 and variance 2.

An affine transform of the posterior Gaussian gives E[2θ|y]=2·1=2 and Var(2θ|y)=2²·(1/2)=2.

### p8(d) — method=proof

y*|y=2 ∼ N(2,3), mean 2 and variance 3.

ε* is independent of (θ,ε), and y is a function of (θ,ε). Thus p(ε*,θ|y)=p(ε*)p(θ|y): conditioning on y preserves independence of ε* from the posterior parameter and leaves ε*∼N(0,1). Sum the independent posterior Gaussian 2θ∼N(2,2) and ε*∼N(0,1), giving N(2,2+1). The added 1 is fresh observation noise uncertainty.

### p9(a) — method=symbolic

Under M0, y∼N(0,1). Under M1, y∼N(0,4).

p(y|M1)=∫p(y|θ,M1)p(θ|M1)dθ=∫N(y|θ,1)N(θ|0,3)dθ. This averages the conditional density over the prior parameter. Equivalently, independent Gaussian θ+ε has mean 0+0=0 and variance 3+1=4. Under M0 the response is just ε. The second normal parameter is variance in the stated model.

### p9(b) — method=exact

e0=p(0|M0)=1/sqrt(2π); e1=p(0|M1)=1/sqrt(8π).

Evaluate a normal density (2πs²)^(-1/2) exp(-y²/(2s²)) at zero. The exponential is 1; the standard deviations are 1 and 2 respectively.

### p9(c) — method=exact

B01=2; the observation favors M0.

B01=e0/e1=[1/sqrt(2π)]/[1/sqrt(8π)]=2. This ratio is in the explicitly declared M0-over-M1 direction.

### p9(d) — method=proof

Posterior odds M0:M1=2:1; P(M0|y=0)=2/3.

Posterior odds equal Bayes factor times prior odds: 2×[(1/2)/(1/2)]=2. Normalizing gives e0/(e0+e1)=2/3 and P(M1|0)=1/3. Although both point probabilities P(Y=0|Mi) are zero, the observation is represented by densities with respect to the same measure. For a small interval (-δ/2,δ/2), its probability is e_i δ+o(δ); their ratio tends to e0/e1. Replacing both evidences by zero would discard the information carried by the local densities and produce an undefined ratio.

### p10(a) — method=exact

θhat=(b^Ty)/(b^Tb)=1.

Orthogonality b^T(y-bθ)=0 gives b^Ty-θ b^Tb=0. Here b^Ty=2 and b^Tb=2>0, so θhat=1.

### p10(b) — method=exact

yhat=(1,1,0)^T; fitted residual r=(1,-1,1)^T; b^Tr=0.

Multiply b by θhat=1 and subtract from (2,0,1)^T. The dot product equals 1·1+1·(-1)+0·1=0.

### p10(c) — method=proof

P=bb^T/(b^Tb)=[[1/2,1/2,0],[1/2,1/2,0],[0,0,0]]. It satisfies P^T=P and P²=P.

For any vector z, projection onto span(b) is b(b^Tz)/(b^Tb), giving P. Transposition leaves bb^T unchanged, so P is symmetric. Algebraically P²=bb^Tbb^T/(b^Tb)²=b(b^Tb)b^T/(b^Tb)²=P. This exact identity proves idempotence without relying on numerical testing. Multiplication by y gives (1,1,0)^T. Dimensions: b 3×1, P 3×3, Py 3×1.

### p10(d) — method=proof

||y-bθ||²=||r||²+(θ-1)²||b||²=3+2(θ-1)². The minimum squared error is 3 at θ=1, which is also ML.

Here r is the fitted residual y-bθhat from (b). Decompose y-bθ=r+b(θhat-θ). Expansion gives ||r||²+2(θhat-θ)b^Tr+(θhat-θ)²||b||². The cross term vanishes by b^Tr=0. Since ||r||²=1+1+1=3 and ||b||²=2>0, the unique global minimum occurs at θ=1. For ε∼N(0,I3), L(θ)=(2π)^(-3/2)exp(-||y-bθ||²/2); maximizing this strictly decreasing function of the squared error yields the same θ.

검토 메모: Minor notation issue: (a) first uses r for y-bθ at a generic θ, while (d) necessarily means the fitted residual from (b). Sequential reading resolves it; prefer explicitly defining r=y-bθhat in (b)/(d).

## 벡터 미분 관례 감사

- variable_dimensions: p2 x:2×1; p4 θ:2×1, Φ:3×2; p6 θ:2×1, Φ:2×2; p10 b,y,r:3×1 and P:3×3.
- derivative_dimensions: p2 and p6 scalar derivatives:1×2. p2 J_g:2×2 with output rows/input columns. p7 scalar derivative:1×1.
- multiplication_order: p6 -2(y-Φθ)^TΦ and 2θ^TΦ^TΦ are rows. p5 Cov(X,Y)=Σ_XA^T. p10 P=bb^T/(b^Tb).
- transpose_step: p6 first establishes θ^TΦ^TΦ=y^TΦ, then transposes both sides to obtain Φ^TΦθ=Φ^Ty.
- authority_and_preservation: These are new questions explicitly using row derivatives; only the requested blind-review.json and blind-review.md are authored. Source PDFs and question input are preserved.
- synchronization_scope: This independent reviewer only records expected answers and derivations in blind-review.json and blind-review.md; generated answers/HTML/PDF were deliberately not read, so synchronization with them is not claimed.
