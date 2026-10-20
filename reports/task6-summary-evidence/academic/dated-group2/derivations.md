# Frozen independent mathematical derivations

Frozen at 2026-10-20T06:16:29.406634+00:00. Source-only, before any reference comparison.

Only group-2/{0930,1007,1012,1014,1019,hw1}/README.md and questions.json were read as academic inputs. No course source, solutions, reference answers, other reviewers, memory, web, or existing harnesses were consulted. Python/SymPy calculations below are reviewer-authored.

Optional original_question_html was read as supplied source prompt. The derivations use the explicit conditions and self-contained mathematical arguments, without consulting authored hints or references. The I/2 versus I/4 difference in 1007/p2 is resolved by the actual question conditions, and noted in that result.

Coverage: 6 packs, 59 questions, 115 subparts.

## Pack 0930

Packet payload SHA-256: `9c3f86c4cdc0fe2bae5ff375853c31ebd8771008c77d52b4bfde46572f04e9d5`
Question payload SHA-256: `94b1877c889fdb79e7bb6cdcc62d195e5568efd2de93544485b8d4cb27a87e52`
Raw packet SHA-256: `652e6f06895a72a09a0a3cebd797e93ae206de4d3b7e55b4796bfbc628cbf540`

### p1

Input SHA-256: `1a15b68f123e7d1e8b69b6b01a0c974aea7cffa51e22296d5546690f400fc583`

#### Subpart main (exact)

Cov(X,Y)=E[XY]-E[X]E[Y]. Substituting Y=X² gives E[X³]-E[X]E[X²]=0-0 E[X²].

Conclusion: Cov(X,Y)=0.

Checks: Scalar covariance; finite third moment in the usual expectation sense implies finite second moment. The asserted dependence need not hold for degenerate X or constant X², but that does not alter covariance.

### p2

Input SHA-256: `54440fff35d62369dbdf647b16360353596892fd20d1727a7ea3cd1b7a4ba081`

#### Subpart main (symbolic)

Let z=ax+by. E[z]=aμx+bμy. Center z: a(x-μx)+b(y-μy). Its outer product has a²Σx+b²Σy and two ab cross terms; independence makes both cross terms zero. Gaussianity is supplied.

Conclusion: z~N(aμx+bμy, a²Σx+b²Σy).

Checks: x,y must have the same dimension d; means d×1 and covariance d×d. If covariance is positive definite, density is (2π)^(-d/2)|Σz|^(-1/2) exp[-(z-μz)ᵀΣz⁻¹(z-μz)/2]; otherwise use a degenerate Gaussian measure.

### p3

Input SHA-256: `a8cb7622c3062310b09b3bce431811fe4dccc931802e036ec0a11e7f144ec4a7`

#### Subpart main (symbolic)

Write H=(y1,…,yt). In full generality let mw=E[w|H], QH=Cov(w|H), K=Cov(xt,w|H). Conditional linearity gives E[xt+1|H]=Aμt+mw and Cov(xt+1|H)=AΣtAᵀ+QH+AK+KᵀAᵀ. For fresh process noise independent of (xt,H), mw=0,QH=Q,K=0.

Conclusion: Under fresh-noise independence: N(Aμt,AΣtAᵀ+Q).

Checks: A maps state to next-state dimension; the displayed covariance is square in next-state dimension and symmetric. Gaussianity is given.

Assumptions: The usual prediction formula assumes w independent of (xt,H).

Unresolved: Independence of w from the state alone does not logically establish independence after conditioning on H; a fresh-noise or equivalent conditional independence condition is needed to uniquely deduce the usual formula.

### p4

Input SHA-256: `244a3f59fe61eb5d74660079a892cec6e142d751721b84a8922a48f48be6f634`

#### Subpart main (proof)

E[(x-μ)²]=E[x²-2μx+μ²]=E[x²]-2μE[x]+μ²E[1]=E[x²]-2μ²+μ².

Conclusion: Var(x)=E[x²]-(E[x])².

Checks: Requires a finite second moment for an ordinary finite variance; constants leave expectation unchanged.

### p5

Input SHA-256: `f9a1e4c5b7d28832bfc6abe4cdffb2a58b7990094c02ea4f03df842eecee3a7e`

#### Subpart main (symbolic)

Condition on x. Then Ax+b is constant and w retains N(0,Q) because w is independent of x. Translation changes only the mean.

Conclusion: p(y|x)=N(y|Ax+b,Q).

Checks: A:E×D, x:D×1, b:E×1, Q:E×E. For Q≻0 use (2π)^(-E/2)|Q|^(-1/2) exp[-(y-Ax-b)ᵀQ⁻¹(y-Ax-b)/2]; the prior covariance of x does not enter this conditional.

### p6

Input SHA-256: `65badfa78dec27026ea4f516cef55f5a5a4c4d1abef9825982a8a9f709e807a1`

#### Subpart main (symbolic)

E[y]=A E[x]+b+E[w]=Aμx+b. Then y-E[y]=A(x-μx)+w. Expanding its outer product gives AΣxAᵀ+AE[(x-μx)wᵀ]+E[w(x-μx)ᵀ]Aᵀ+E[wwᵀ]. Independence and centering remove the middle terms.

Conclusion: μy=Aμx+b; Σy=AΣxAᵀ+Q; y~N(μy,Σy).

Checks: A:E×D, Σx:D×D, Σy,Q:E×E; b affects only the mean. Covariance is positive semidefinite since uᵀΣyu=(Aᵀu)ᵀΣx(Aᵀu)+uᵀQu≥0.

### p7

Input SHA-256: `5bf530dbb975bbaab9be0d84982d6e611449bda89bb08ac47151a32efa640fc0`

#### Subpart a (symbolic)

Fix y; Cy is constant and v is independent of y.

Conclusion: p(z|y)=N(z|Cy,R).

Checks: If C:F×E then z:F×1 and R:F×F; ordinary density requires R≻0.

#### Subpart b (symbolic)

E[z]=CE[y]=C(Aμx+b). Centering gives z-μz=C(y-μy)+v; covariance expands to CΣyCᵀ+R because independence kills cross terms.

Conclusion: μz=C(Aμx+b); Σz=C(AΣxAᵀ+Q)Cᵀ+R; z~N(μz,Σz).

Checks: CΣyCᵀ and R are both F×F. Given Gaussianity; zero noise recovers covariance of deterministic linear transformation.

### p8

Input SHA-256: `9e25638b4185b304bf22f1c1efd8e1f113821f85c21ed5a6efa0e37a51ed181f`

#### Subpart main (proof)

For N≥1, Σij(xi-xj)²=Σij xi²+Σij xj²-2Σij xixj=2NΣi xi²-2(Σi xi)². Divide by N² and factor 2.

Conclusion: N⁻²Σij(xi-xj)²=2[N⁻¹Σi xi²-(N⁻¹Σi xi)²].

Checks: The double sum is over ordered pairs including i=j, which contribute zero. For N=1 both sides vanish.

## Pack 1007

Packet payload SHA-256: `1a3d9b34011fe13ff45c5e8070f5516cf191d7bdaa45fe731f3c3e20f9105b8a`
Question payload SHA-256: `fead155338118864ec4409fb65bc0009508173bc250fb9598290e68d4773ccaf`
Raw packet SHA-256: `c89add3013f65fe5bfba475ca769ad4057a4fb339c80d51d69bee3bf50990d72`

### p1

Input SHA-256: `458ee0102fe56a64deafed52823a5097a2c88df3cd326b95e366f14c4b4d624d`

#### Subpart a (qualitative)

Draw one 6-vector θi~N(0,I6/4). Hold that single vector fixed and evaluate fi(xj)=φ(xj)ᵀθi at all 200 input locations.

Conclusion: A parameter draw followed by evaluation across the grid produces one function sample.

Checks: The same θi must be used at every xj; independent draws at each x would not produce one polynomial.

#### Subpart b (exact)

The monomials x⁰ through x⁵ require six coefficients.

Conclusion: θ∈R⁶.

Checks: φ(x) is 6×1, hence θᵀφ(x) is scalar.

#### Subpart c (symbolic)

At fixed x, f=φ(x)ᵀθ has mean 0 and variance φᵀ(I6/4)φ=(1/4)Σk=0⁵ x^(2k). The shading comes from this prior parameter uncertainty propagated through the polynomial.

Conclusion: Pointwise prior credible intervals for noiseless function values, with supplied inner 67% and outer 95% levels.

Checks: No observation noise is included. Different x values are correlated through Cov(f(x),f(x′))=(1/4)Σk=0⁵(xx′)^k. Exact central Gaussian half-width for mass p is Φ⁻¹((1+p)/2) times the standard deviation; 67% is not exactly ±1σ.

### p2

Input SHA-256: `412f26924ef1500fb90d1c857798217f02c2df11c11f5b49a798509194a68675`

#### Subpart main (exact)

E[f]=φᵀ0=0. Var(f)=φᵀ(I6/2)φ=(1/2)Σk=0⁵x^(2k). At x=0, φ=(1,0,0,0,0,0)ᵀ; at x=1, φ=(1,1,1,1,1,1)ᵀ.

Conclusion: x*=0: mean 0, variance 1/2. x*=1: mean 0, variance 3.

Checks: Uses the question conditions covariance I/2, despite the optional original quotation mentioning I/4; these are different parameter choices, not algebraically interchangeable.

### p3

Input SHA-256: `d3fba7efa6b6fd495e3d2936b165e08add8656d5a3fa6d02f49608ca3098eeec`

#### Subpart a (proof)

A nondegenerate Gaussian posterior is maximized at θ=mN because its negative log density differs from (θ-mN)ᵀSN⁻¹(θ-mN)/2 by a constant. Linearity of expectation gives E[f(x)|data]=φ(x)ᵀmN.

Conclusion: The MAP function equals the BLR posterior mean function.

Checks: φ,mN:6×1; if the posterior is degenerate, its Gaussian mean still determines the mean function, with mode interpreted on its support.

#### Subpart b (qualitative)

A Gaussian linear image has f(x)|data~N(φᵀmN,φᵀSNφ). Narrow and wide bands therefore express smaller and larger posterior credible ranges for the latent function at each x. The supplied SVG shows narrower bounds near training points and wider bounds toward the ends.

Conclusion: Inner and outer pointwise uncertainty bands about the posterior mean function.

Checks: The figure depicts function uncertainty; adding observation noise would increase the variance by its noise variance.

Unresolved: The packet does not assign numerical posterior coverage levels to the two bands. 67% and 95% cannot be confirmed for this specific plot from the provided conditions or SVG.

#### Subpart c (qualitative)

The posterior distribution on θ induces a distribution on entire functions. A representative sample curve is generated with θi~N(mN,SN), then fi(x)=φ(x)ᵀθi at all x. Overlaying these illustrates plausible functions and their variation after observing data.

Conclusion: The natural posterior-function interpretation is several posterior parameter draws evaluated as complete curves.

Checks: Each complete curve uses one shared θi. The supplied SVG only renders panel (b).

Unresolved: Panel (c) itself and an explicit statement of its sampling construction are not supplied; the posterior-sample reading is the standard interpretation, not visually verified provenance.

### p4

Input SHA-256: `ac5d319edff021554a95e86c45b4751bea74f2852f80ffaf833dfe62b2098d31`

#### Subpart main (exact)

Marginalizing a Gaussian retains mean entry μ1=1 and covariance entry Σ11=1/2.

Conclusion: p(x1)=N(x1|1,1/2)=π^(-1/2)exp[-(x1-1)²].

Checks: Σ=[[1/2,-1],[-1,4]] has determinant 1>0 and positive first leading minor. The marginal integrates to 1 by the Gaussian integral.

### p5

Input SHA-256: `8cb33e916d882b42417be4df2a319adc34984c8e26dfd237ddc3e7594b9b27b2`

#### Subpart main (exact)

E[2x-y]=2·1-(-1)=3. Independence gives Var(2x-y)=4·2+(-1)²·3=11. Independent Gaussian sums are Gaussian.

Conclusion: 2x-y~N(3,11).

Checks: The second Gaussian parameter is interpreted as variance; the squared negative coefficient contributes positive variance.

### p6

Input SHA-256: `0e1ade754d230f9684dd03b4aca3b2759a2bf79aec66b2d63b4064d2865ff975`

#### Subpart main (symbolic)

Integrate each mixture component over the discarded coordinate using linearity of integration and Gaussian marginalization. The mixture weights are unaffected because each integrated component remains normalized.

Conclusion: p(x1)=0.4N(x1|10,1)+0.6N(x1|0,8.4); p(x2)=0.4N(x2|2,1)+0.6N(x2|0,1.7).

Checks: Weights 0.4+0.6=1. Both component variances are positive. Second covariance determinant=8.4·1.7-4=10.28>0.

### p7

Input SHA-256: `e890ecfbac15145d20b129b2239a3fe2f725b20cdd63c88886b0b0e506f580d6`

#### Subpart a (exact)

Linearity over the mixture gives E[x1]=0.4·10+0.6·0 and E[x2]=0.4·2+0.6·0.

Conclusion: E[x1]=4, E[x2]=0.8.

Checks: The weights sum to one; covariance entries do not change these first moments.

#### Subpart b (exact)

Expectation of a vector is the vector of coordinate expectations.

Conclusion: E[x]=(4,0.8)ᵀ.

Checks: 2×1 column vector.

### p8

Input SHA-256: `81ee2920b26221f6245981786286990bef48678cb596bb667aa667a391774c7f`

#### Subpart main (proof)

Let H=A⁻¹+B⁻¹, h=A⁻¹a+B⁻¹b and k=aᵀA⁻¹a+bᵀB⁻¹b. Expanding both exponents gives xᵀHx-2hᵀx+k. Set C=H⁻¹ and c=Ch, so Hc=h. Then xᵀHx-2hᵀx+k=(x-c)ᵀH(x-c)+k-cᵀHc. The final two terms are independent of x, so normalizing the product leaves Gaussian N(c,C).

Conclusion: C=(A⁻¹+B⁻¹)⁻¹; c=C(A⁻¹a+B⁻¹b).

Checks: C is D×D and positive definite, c:D×1. Normalized density is (2π)^(-D/2)|C|^(-1/2) exp[-(x-c)ᵀC⁻¹(x-c)/2]. No commutativity of A and B was used.

## Pack 1012

Packet payload SHA-256: `94d40a7075cfe48243b6c0060e7615d1c96505a18fa5f5cc5a6c14b892cccf27`
Question payload SHA-256: `aa9890c0adf6ea49b3374048907332e51505112ad56acc6648316677bd3e2697`
Raw packet SHA-256: `47c44bc42bec2b40b5f48d68dfdc96baed479124ff6627a2381c6b88355a3a43`

### p1

Input SHA-256: `f00e97da7af6883cf23be9154b9b028e750093638b5716d63f4442b99d6a3e1b`

#### Subpart a (exact)

A=[[2,0],[1,3]], det A=2·3-0·1=6.

Conclusion: Area=6.

Checks: Absolute determinant gives nonnegative area.

#### Subpart b (exact)

A=[[2,4],[1,2]], det A=4-4=0. Moreover g=2b, so all vertices lie on one line.

Conclusion: Area=0.

Checks: The zero area agrees with linearly dependent columns.

### p2

Input SHA-256: `1c43dfce1125c7c76722ab25136da79463f23312540245abd3cbe0411c2640f3`

#### Subpart a (exact)

det Σ=4·10-2·2=36≠0.

Conclusion: det Σ=36; inverse exists.

Checks: Positive first minor and determinant also show Σ≻0.

#### Subpart b (exact)

Swap diagonal entries, negate off-diagonal entries, and divide by determinant.

Conclusion: Σ⁻¹=(1/36)[[10,-2],[-2,4]].

Checks: Σ[[10,-2],[-2,4]]=[[36,0],[0,36]], giving identity after division.

### p3

Input SHA-256: `70203ffbad6cc9f32af9930353d7998314b647943b67a9da99237a96162d6b5b`

#### Subpart main (proof)

The inverse transformation is x=A⁻¹y. The derivative ∂x/∂y=A⁻¹ has absolute determinant 1/|ad-bc|. Substitute x into the original exponent: xᵀx=yᵀA⁻ᵀA⁻¹y. Probability conservation fY(y)dy=fX(A⁻¹y)dx supplies the determinant factor.

Conclusion: fY(y)=[2π|ad-bc|]⁻¹ exp[-yᵀA⁻ᵀA⁻¹y/2], y∈R². Equivalently N(0,AAᵀ).

Checks: |AAᵀ|=(det A)² and (AAᵀ)⁻¹=A⁻ᵀA⁻¹. Substitution y=Ax makes its integral equal the original normalized integral 1, including orientation reversing det A<0.

### p4

Input SHA-256: `38542bfe1d1dbef51499511d42c9fcfa45c3e1b0b53b9ed5703e2e7e8943028e`

#### Subpart main (exact)

x1=y1/3,x2=y2/2 and |det ∂x/∂y|=1/6. The squared norm becomes y1²/9+y2²/4.

Conclusion: fY(y)=1/(12π) exp[-(y1²/9+y2²/4)/2]; fY(0)=1/(12π).

Checks: Covariance diag(9,4) has determinant 36; normalizer is 1/(2π√36). Two one-dimensional Gaussian integrals yield total mass 1.

### p5

Input SHA-256: `516ab758e56c447297ec9d17426bb9881df13622787eee740df56e9dc8a76a5b`

#### Subpart a (exact)

From y2=2x2 get x2=y2/2. From y1=x1+x2 get x1=y1-y2/2.

Conclusion: x=A⁻¹y=[[1,-1/2],[0,1/2]]y.

Checks: AA⁻¹=I2.

#### Subpart b (exact)

∂x/∂y=[[1,-1/2],[0,1/2]], so determinant is 1·(1/2)-0=1/2.

Conclusion: det Jacobian=1/2; absolute determinant=1/2.

Checks: This equals 1/det A, with det A=2.

#### Subpart c (exact)

Substitute the inverse coordinates into x1²+x2²=(y1-y2/2)²+(y2/2)²=y1²-y1y2+y2²/2 and multiply density by 1/2.

Conclusion: fY(y)=1/(4π) exp[-(y1²-y1y2+y2²/2)/2].

Checks: Σ=AAᵀ=[[2,2],[2,4]], det Σ=4, Σ⁻¹=[[1,-1/2],[-1/2,1/2]]. Its normalizer matches; invertible change of variables proves total integral 1.

### p6

Input SHA-256: `dfac192fabb0a3100bdb9dfb87cbde6acd5b19e5b212974c3a9f3eb484bfb608`

#### Subpart main (proof)

Let δx=x-μx. Since μy=Aμx+b, δy=Aδx+w. Then Cov(x,y)=E[δx(Aδx+w)ᵀ]=ΣxAᵀ+E[δxwᵀ]. Independence and zero means make the last term zero. Transposing yields Cov(y,x)=AΣx.

Conclusion: Covxy=ΣxAᵀ; Covyx=AΣx.

Checks: Shapes D×E and E×D, respectively; they are transposes, not generally equal. Diagonality of Q is unnecessary for this result.

### p7

Input SHA-256: `3d6bf988e84db329730743916c2858a3694717ce175f97232e98dfab2794ee3a`

#### Subpart main (symbolic)

Mean y is Aμx+b. Center y to Aδx+w; expansion and independent zero-mean noise give Cov(y)=AΣxAᵀ+Q. Stack x and y, placing the supplied cross-covariances into opposite off-diagonal blocks.

Conclusion: (x;y)~N((μx;Aμx+b), [[Σx,ΣxAᵀ],[AΣx,AΣxAᵀ+Q]]).

Checks: Mean length D+E, covariance (D+E)×(D+E), symmetric. It equals T diag(Σx,Q)Tᵀ with T=[[I,0],[A,I]], so it is positive semidefinite.

### p8

Input SHA-256: `047c2367d4edfdff09fcbd28de3c412b32c13b7e80075c323846bec85b63f38a`

#### Subpart main (symbolic)

Let H=(y1,…,yt). Under independent fresh noises, m=Aμt and V=AΣtAᵀ+Q. Next y=Cxt+1+vt+1 has mean Cm, variance CVCᵀ+R and cross covariance Cov(xt+1,yt+1|H)=VCᵀ. Stack these blocks; Gaussianity is supplied.

Conclusion: Under the stated fresh-noise interpretation: N((m;Cm), [[V,VCᵀ],[CV,CVCᵀ+R]]), m=Aμt, V=AΣtAᵀ+Q.

Checks: If state dimension d and observation dimension e, A:d×d,C:e×d,Q,V:d×d,R:e×e. The joint block is positive semidefinite by the same triangular transformation construction. μ0,Σ0 are not needed once μt,Σt are supplied.

Assumptions: wt and vt+1 are independent of the current state and observation history, and of each other.

Unresolved: The phrase i.i.d. Gaussian noises does not explicitly state independence from x0/the state/history. If it means only independence among noise draws, the usual prediction blocks additionally require exogeneity. Also w and v cannot literally be identically distributed across different dimensions or unequal Q,R; the conventional reading is each process independent over time and mutually independent.

## Pack 1014

Packet payload SHA-256: `acde3dd70747f1d336afdca9073509f887e7eea29d9ab4e80e4c36a6ee890288`
Question payload SHA-256: `11de830dcd9e343b2d25d1b0115b09460e0afa983d32059979ba3d99967605e4`
Raw packet SHA-256: `c172c1125b0881adebb606e4c6f4207367660dbb96cc85f5d22ee866d0db2aea`

### p1

Input SHA-256: `19c57219b9d27eccf5469ed071a5dd20e9e1cad11b8e549ff7c8c4a401ce5009`

#### Subpart a (exact)

The three states have equal probability p; normalization 3p=1 gives p=1/3.

Conclusion: P(Z=-1.1)=P(Z=0.3)=P(Z=1.5)=1/3, and 0 elsewhere.

Checks: Three nonnegative masses sum to 1.

#### Subpart b (exact)

Let the height be h. The support length is 1.6-0.9=0.7=7/10. Normalization h·7/10=1 gives h=10/7.

Conclusion: pX(x)=10/7 for 0.9≤x≤1.6, and 0 otherwise.

Checks: Integral=(10/7)(7/10)=1. A density may exceed 1; endpoint values do not affect the integral.

### p2

Input SHA-256: `d4ffd965bb0b484c2cf4e05a111730c71b4d319b5fbcbf2920458651919397b7`

#### Subpart main (proof)

θ1x+θ2x²=(μx-x²/2)/σ²=-(x-μ)²/(2σ²)+μ²/(2σ²). The final term is independent of x. The unnormalized integral is exp[μ²/(2σ²)]√(2πσ²), so its reciprocal cancels this factor.

Conclusion: p(x|θ)=(2πσ²)^(-1/2)exp[-(x-μ)²/(2σ²)]=N(μ,σ²).

Checks: σ²>0 makes the exponent concave in x and the Gaussian integral finite; normalized integral is 1.

## Pack 1019

Packet payload SHA-256: `183e5099c2ca57443c0cd3d6b274187d1133d1f74d87e2065bae05edcc4da3ec`
Question payload SHA-256: `c16e284bebd31566309205d3dcc6e91b22e730883046fbd09d580d286e27288a`
Raw packet SHA-256: `1a21e3dc148ee0671236b323f218082e1c07eea684ec006e6c8149e267dcb194`

### p1

Input SHA-256: `d5fa76227f3443a49b10b62752abedffd1fc22c8cf73ad2f0f974fefb31f653c`

#### Subpart a (exact)

For p=λb, minimize ||x-λb||². Derivative -2bᵀx+2λbᵀb=0 gives λ=bᵀx/(bᵀb). Thus P=bbᵀ/(bᵀb). Here bᵀb=9.

Conclusion: P=[[1/9, 2/9, 2/9], [2/9, 4/9, 4/9], [2/9, 4/9, 4/9]].

Checks: P is 3×3 and symmetric. b≠0 ensures denominator 9>0.

#### Subpart b (exact)

bᵀx=5, so λ=5/9=5/9; multiply λ by b.

Conclusion: πU(x)=[5/9, 10/9, 10/9]ᵀ.

Checks: Exact residual bᵀ(x-p)=0; hence residual is orthogonal to the line.

#### Subpart c (proof)

P²=(bbᵀbbᵀ)/(bᵀb)²=b(bᵀb)bᵀ/(bᵀb)²=P. Therefore P(Px)=Px for this x and every x.

Conclusion: PπU(x)=πU(x)=[5/9, 10/9, 10/9]ᵀ.

Checks: Exact computed P²-P=[[0, 0, 0], [0, 0, 0], [0, 0, 0]], Pp-p=[0, 0, 0].

### p2

Input SHA-256: `263b0c9f39439364fedc2002608ed85ea655dfb13f8c91dcabdb408f83faae3f`

#### Subpart a (exact)

For p=λb, minimize ||x-λb||². Derivative -2bᵀx+2λbᵀb=0 gives λ=bᵀx/(bᵀb). Thus P=bbᵀ/(bᵀb). Here bᵀb=1.

Conclusion: P=[[1, 0, 0], [0, 0, 0], [0, 0, 0]].

Checks: P is 3×3 and symmetric. b≠0 ensures denominator 1>0.

#### Subpart b (exact)

bᵀx=2, so λ=2/1=2; multiply λ by b.

Conclusion: πU(x)=[2, 0, 0]ᵀ.

Checks: Exact residual bᵀ(x-p)=0; hence residual is orthogonal to the line.

#### Subpart c (proof)

P²=(bbᵀbbᵀ)/(bᵀb)²=b(bᵀb)bᵀ/(bᵀb)²=P. Therefore P(Px)=Px for this x and every x.

Conclusion: PπU(x)=πU(x)=[2, 0, 0]ᵀ.

Checks: Exact computed P²-P=[[0, 0, 0], [0, 0, 0], [0, 0, 0]], Pp-p=[0, 0, 0].

### p3

Input SHA-256: `ddae2bd36e46fd81cabeaa71626ce6d692c04215fb7db2771d7f104b956380f7`

#### Subpart a (exact)

For p=λb, minimize ||x-λb||². Derivative -2bᵀx+2λbᵀb=0 gives λ=bᵀx/(bᵀb). Thus P=bbᵀ/(bᵀb). Here bᵀb=1.

Conclusion: P=[[0, 0, 0], [0, 1, 0], [0, 0, 0]].

Checks: P is 3×3 and symmetric. b≠0 ensures denominator 1>0.

#### Subpart b (exact)

bᵀx=2, so λ=2/1=2; multiply λ by b.

Conclusion: πU(x)=[0, 2, 0]ᵀ.

Checks: Exact residual bᵀ(x-p)=0; hence residual is orthogonal to the line.

#### Subpart c (proof)

P²=(bbᵀbbᵀ)/(bᵀb)²=b(bᵀb)bᵀ/(bᵀb)²=P. Therefore P(Px)=Px for this x and every x.

Conclusion: PπU(x)=πU(x)=[0, 2, 0]ᵀ.

Checks: Exact computed P²-P=[[0, 0, 0], [0, 0, 0], [0, 0, 0]], Pp-p=[0, 0, 0].

### p4

Input SHA-256: `f0fad2ab39aedf5fd7523581060ff4daebefad284ca387b7b9bab905a740578a`

#### Subpart a (exact)

For p=λb, minimize ||x-λb||². Derivative -2bᵀx+2λbᵀb=0 gives λ=bᵀx/(bᵀb). Thus P=bbᵀ/(bᵀb). Here bᵀb=3.

Conclusion: P=[[1/3, 1/3, 1/3], [1/3, 1/3, 1/3], [1/3, 1/3, 1/3]].

Checks: P is 3×3 and symmetric. b≠0 ensures denominator 3>0.

#### Subpart b (exact)

bᵀx=9, so λ=9/3=3; multiply λ by b.

Conclusion: πU(x)=[3, 3, 3]ᵀ.

Checks: Exact residual bᵀ(x-p)=0; hence residual is orthogonal to the line.

#### Subpart c (proof)

P²=(bbᵀbbᵀ)/(bᵀb)²=b(bᵀb)bᵀ/(bᵀb)²=P. Therefore P(Px)=Px for this x and every x.

Conclusion: PπU(x)=πU(x)=[3, 3, 3]ᵀ.

Checks: Exact computed P²-P=[[0, 0, 0], [0, 0, 0], [0, 0, 0]], Pp-p=[0, 0, 0].

### p5

Input SHA-256: `c9ca91c49007653fc91c6c30bb17e89e1766fce1e1a7b1ed5ca252fb3ae1a48c`

#### Subpart a (exact)

Minimize ||x-Bλ||²: ∇λ=2BᵀBλ-2Bᵀx, so Gλ=Bᵀx. Here G=[[3, 3], [3, 5]], det G=6, Bᵀx=[6, 0]. Invert G.

Conclusion: λ=[5, -3]ᵀ.

Checks: λ has dimension 2×1 and Bλ dimension 3×1. Exact normal equation residual=[0, 0].

#### Subpart b (exact)

Multiply Bλ to get p=[5, 2, -1]. Difference r=x-p=[1, -2, 1]; squared error rᵀr=6.

Conclusion: πU(x)=[5, 2, -1]ᵀ; ||x-πU(x)||=sqrt(6).

Checks: This is the Euclidean norm, not the squared norm. For any other Bη, ||x-Bη||²=||r||²+||B(λ-η)||² because Bᵀr=0; hence p is the closest point.

#### Subpart c (exact)

The coefficient map is λ=G⁻¹Bᵀx; composing with B gives P=BG⁻¹Bᵀ, G⁻¹=[[5/6, -1/2], [-1/2, 1/2]].

Conclusion: P=[[5/6, 1/3, -1/6], [1/3, 1/3, 1/3], [-1/6, 1/3, 5/6]].

Checks: P is a 3×3 symmetric matrix; rank 2 since columns of B are independent.

#### Subpart d (proof)

Bᵀr=Bᵀx-Gλ=0. Also P²=BG⁻¹(BᵀB)G⁻¹Bᵀ=BG⁻¹GG⁻¹Bᵀ=P. This algebra proves orthogonality and idempotence.

Conclusion: Both b1ᵀr and b2ᵀr vanish; P²=P.

Checks: Exact Bᵀr=[0, 0] and P²-P=[[0, 0, 0], [0, 0, 0], [0, 0, 0]].

### p6

Input SHA-256: `87c543c43c7f3b883ae1d3fc77bebc8857eca00648f28808787c21af6b447770`

#### Subpart a (exact)

Minimize ||x-Bλ||²: ∇λ=2BᵀBλ-2Bᵀx, so Gλ=Bᵀx. Here G=[[1, 0], [0, 1]], det G=1, Bᵀx=[2, 3]. Invert G.

Conclusion: λ=[2, 3]ᵀ.

Checks: λ has dimension 2×1 and Bλ dimension 3×1. Exact normal equation residual=[0, 0].

#### Subpart b (exact)

Multiply Bλ to get p=[2, 3, 0]. Difference r=x-p=[0, 0, 4]; squared error rᵀr=16.

Conclusion: πU(x)=[2, 3, 0]ᵀ; ||x-πU(x)||=4.

Checks: This is the Euclidean norm, not the squared norm. For any other Bη, ||x-Bη||²=||r||²+||B(λ-η)||² because Bᵀr=0; hence p is the closest point.

#### Subpart c (exact)

The coefficient map is λ=G⁻¹Bᵀx; composing with B gives P=BG⁻¹Bᵀ, G⁻¹=[[1, 0], [0, 1]].

Conclusion: P=[[1, 0, 0], [0, 1, 0], [0, 0, 0]].

Checks: P is a 3×3 symmetric matrix; rank 2 since columns of B are independent.

#### Subpart d (proof)

Bᵀr=Bᵀx-Gλ=0. Also P²=BG⁻¹(BᵀB)G⁻¹Bᵀ=BG⁻¹GG⁻¹Bᵀ=P. This algebra proves orthogonality and idempotence.

Conclusion: Both b1ᵀr and b2ᵀr vanish; P²=P.

Checks: Exact Bᵀr=[0, 0] and P²-P=[[0, 0, 0], [0, 0, 0], [0, 0, 0]].

### p7

Input SHA-256: `98086be333ea2dc2f626d4029c3b48865d22a75058d2cea0c21097a93e29bf26`

#### Subpart a (exact)

Minimize ||x-Bλ||²: ∇λ=2BᵀBλ-2Bᵀx, so Gλ=Bᵀx. Here G=[[3, 3], [3, 5]], det G=6, Bᵀx=[6, 6]. Invert G.

Conclusion: λ=[2, 0]ᵀ.

Checks: λ has dimension 2×1 and Bλ dimension 3×1. Exact normal equation residual=[0, 0].

#### Subpart b (exact)

Multiply Bλ to get p=[2, 2, 2]. Difference r=x-p=[-2, 4, -2]; squared error rᵀr=24.

Conclusion: πU(x)=[2, 2, 2]ᵀ; ||x-πU(x)||=2*sqrt(6).

Checks: This is the Euclidean norm, not the squared norm. For any other Bη, ||x-Bη||²=||r||²+||B(λ-η)||² because Bᵀr=0; hence p is the closest point.

#### Subpart c (exact)

The coefficient map is λ=G⁻¹Bᵀx; composing with B gives P=BG⁻¹Bᵀ, G⁻¹=[[5/6, -1/2], [-1/2, 1/2]].

Conclusion: P=[[5/6, 1/3, -1/6], [1/3, 1/3, 1/3], [-1/6, 1/3, 5/6]].

Checks: P is a 3×3 symmetric matrix; rank 2 since columns of B are independent.

#### Subpart d (proof)

Bᵀr=Bᵀx-Gλ=0. Also P²=BG⁻¹(BᵀB)G⁻¹Bᵀ=BG⁻¹GG⁻¹Bᵀ=P. This algebra proves orthogonality and idempotence.

Conclusion: Both b1ᵀr and b2ᵀr vanish; P²=P.

Checks: Exact Bᵀr=[0, 0] and P²-P=[[0, 0, 0], [0, 0, 0], [0, 0, 0]].

### p8

Input SHA-256: `fb2cc471cf2c4d961f7babc7642ec9180ec1302bfe7a65bb9a54acb43a7b434c`

#### Subpart a (exact)

Minimize ||x-Bλ||²: ∇λ=2BᵀBλ-2Bᵀx, so Gλ=Bᵀx. Here G=[[5, 1], [1, 2]], det G=9, Bᵀx=[5, 4]. Invert G.

Conclusion: λ=[2/3, 5/3]ᵀ.

Checks: λ has dimension 2×1 and Bλ dimension 3×1. Exact normal equation residual=[0, 0].

#### Subpart b (exact)

Multiply Bλ to get p=[7/3, 4/3, 5/3]. Difference r=x-p=[-4/3, 2/3, 4/3]; squared error rᵀr=4.

Conclusion: πU(x)=[7/3, 4/3, 5/3]ᵀ; ||x-πU(x)||=2.

Checks: This is the Euclidean norm, not the squared norm. For any other Bη, ||x-Bη||²=||r||²+||B(λ-η)||² because Bᵀr=0; hence p is the closest point.

#### Subpart c (exact)

The coefficient map is λ=G⁻¹Bᵀx; composing with B gives P=BG⁻¹Bᵀ, G⁻¹=[[2/9, -1/9], [-1/9, 5/9]].

Conclusion: P=[[5/9, 2/9, 4/9], [2/9, 8/9, -2/9], [4/9, -2/9, 5/9]].

Checks: P is a 3×3 symmetric matrix; rank 2 since columns of B are independent.

#### Subpart d (proof)

Bᵀr=Bᵀx-Gλ=0. Also P²=BG⁻¹(BᵀB)G⁻¹Bᵀ=BG⁻¹GG⁻¹Bᵀ=P. This algebra proves orthogonality and idempotence.

Conclusion: Both b1ᵀr and b2ᵀr vanish; P²=P.

Checks: Exact Bᵀr=[0, 0] and P²-P=[[0, 0, 0], [0, 0, 0], [0, 0, 0]].

## Pack hw1

Packet payload SHA-256: `8c02f22c5a5a39c0e13d72ab27d43e01d4f4d12f648b749209345aa0936e943b`
Question payload SHA-256: `e7b453fa0b51049544e26b2388e6d33e51edc3319dd4556baeba4146b17722ba`
Raw packet SHA-256: `59e8e3880e845b1048ceef2aaeb8adf7896637c080e53ef8ae0fa021b336f720`

### p1

Input SHA-256: `8163fc43377bd690562cc3b6952c0dfa2428999f9f38cd6dad201b2b7072ff2a`

#### Subpart a (exact)

By (Aᵀ)ij=Aji, the three columns of A become three rows.

Conclusion: Aᵀ=[[1,0],[-2,4],[3,5]].

Checks: A is 2×3 and Aᵀ is 3×2; transposing twice returns A.

#### Subpart b (exact)

Exchange the 3×1 vector row and column positions.

Conclusion: bᵀ=[2,-1,4].

Checks: A 1×3 row; the entries retain their order.

#### Subpart c (exact)

Rows of Cᵀ are columns of C.

Conclusion: Cᵀ=[[1,-1,5],[2,3,0],[0,4,-2]].

Checks: Both matrices are 3×3; for example (Cᵀ)13=C31=5.

### p2

Input SHA-256: `42ffd86fcdb8802919b33c8f7123102ddfecfe03b8a3654d246c4caa6e03abba`

#### Subpart a (exact)

xᵀy=1·2+(-2)·1+2·0.

Conclusion: xᵀy=0.

Checks: 1×3 times 3×1 yields a scalar.

#### Subpart b (exact)

||x||₂=√(1²+(-2)²+2²)=√9.

Conclusion: ||x||₂=3.

Checks: Norm is nonnegative.

#### Subpart c (exact)

||y||₂=√(2²+1²+0²).

Conclusion: ||y||₂=√5.

Checks: Squared norm is 5.

#### Subpart d (proof)

The Euclidean definition of orthogonality is zero inner product. Part (a) gives xᵀy=0 with both vectors nonzero.

Conclusion: Yes, x and y are orthogonal.

Checks: The claim concerns the ordinary inner product specified by the formulas.

### p3

Input SHA-256: `4d35b11503f64ff19b997cc5d34e3b1869527a51210b0c288187c8308c85eb6f`

#### Subpart main (exact)

Use (AB)ij=ΣkAikBkj. Columns of AB are Acol1+Acol3, Acol1+Acol2, Acol2+Acol3. Rows of BA are Arow1+Arow2, Arow2+Arow3, Arow1+Arow3.

Conclusion: AB=[[4,3,5],[10,9,11],[16,15,17]]; BA=[[5,7,9],[11,13,15],[8,10,12]]; AB≠BA.

Checks: Both products are 3×3. The (1,1) entries 4 and 5 already distinguish the products.

### p4

Input SHA-256: `d0a737b5e1e081b5565e137c30e4adabbc6540256956e9621daa8dd570e8c714`

#### Subpart a (exact)

For a 2×2 matrix take the product of diagonal entries minus the product of off-diagonal entries: 3·4-1·2.

Conclusion: det A=10.

Checks: Nonzero determinant agrees with invertibility.

#### Subpart b (exact)

det B=1·0-(-2)·3.

Conclusion: det B=6.

Checks: The minus sign on B12 changes the subtracted product into +6.

#### Subpart c (exact)

A diagonal determinant is the product of its diagonal entries, 2·(-1)·3.

Conclusion: det C=-6.

Checks: Determinants can be negative; this is not an area magnitude.

#### Subpart d (exact)

First-row cofactor expansion: 1(4·4-6·2)-3(2·4-6·0)+5(2·2-4·0)=4-24+20=0. Sarrus: positive cyclic products 1·4·4+3·6·0+5·2·2=36; negative cyclic products 5·4·0+3·2·4+1·6·2=36; difference 0.

Conclusion: det D=0 by both first-row expansion and Sarrus.

Checks: The two independent expansions yield the same scalar; Drow3=2Drow1-Drow2 also proves row dependence.

### p5

Input SHA-256: `9b03ed8f6e7c8e2cbeabdf1440883d0a6e67bfc644c30b65dbf9080ec122329a`

#### Subpart a (exact)

det A=2·1-1·1=1. The adjugate swaps the diagonal and negates off-diagonal entries.

Conclusion: A⁻¹=[[1,-1],[-1,2]].

Checks: A A⁻¹=[[2-1,-2+2],[1-1,-1+2]]=I2.

#### Subpart b (exact)

det B=1·1-(-2)·3=7. Divide its adjugate by 7.

Conclusion: B⁻¹=(1/7)[[1,2],[-3,1]].

Checks: B[[1,2],[-3,1]]=[[7,0],[0,7]], so multiplying by 1/7 gives I2.

#### Subpart c (exact)

C is block diagonal with 2×2 block T=[[2,1],[1,2]] and scalar 2. det T=3, T⁻¹=(1/3)[[2,-1],[-1,2]] and inverse scalar=1/2.

Conclusion: C⁻¹=[[2/3,-1/3,0],[-1/3,2/3,0],[0,0,1/2]].

Checks: The first block product is I2 and last product is 1, so CC⁻¹=I3; det C=6≠0.

### p6

Input SHA-256: `452b8c4a31423a200551a26ea71b4dd7dd5a20ec1a5195d02f19e3fc8200e1c4`

#### Subpart main (proof)

Compute 2x1-x2=(4,-2,6)ᵀ-(1,1,-2)ᵀ=(3,-3,8)ᵀ=x3.

Conclusion: Linearly dependent: 2x1-x2-x3=0.

Checks: The coefficient vector (2,-1,-1) is nonzero; all three coordinate residuals are exactly 0.

### p7

Input SHA-256: `fbab2c0f01bc7f01d8169cc15a6f9c6ebdd583cef9b5c13d7fa111f860462d93`

#### Subpart main (exact)

Set y=a x1+b x2+c x3. Coordinate equations are a+b+2c=1, a+2b-c=-2, a+3b+c=5. Subtracting first from second and third gives b-3c=-3 and 2b-c=4. Thus c=2,b=3,a=-6.

Conclusion: y=-6x1+3x2+2x3.

Checks: Reconstruction=(-6,-6,-6)+(3,6,9)+(4,-2,2)=(1,-2,5). The coefficient matrix determinant=5≠0, so representation is unique.

### p8

Input SHA-256: `9b71f01ac8322e7b45412174190c7bd8ddcbd210cdc419ab5d7955076ca3ccd2`

#### Subpart main (exact)

The columns are (1,1,1)ᵀ and (-1,0,1)ᵀ. Their squared norms are 3 and 2 and their dot product is 0, giving AᵀA=diag(3,2).

Conclusion: AᵀA=[[3,0],[0,2]]; determinant=6; inverse=[[1/3,0],[0,1/2]].

Checks: diag(3,2)diag(1/3,1/2)=I2, so the requested multiplication verification holds.

### p9

Input SHA-256: `40d7483f910a2f0ac8e5c6ef7bc9c7de1d25ebebaed4273bedb17a289a878511`

#### Subpart main (exact)

Evaluate φ at -1,0,1 and put each transpose into a row. Multiplying θ gives 1+x+2x² at each input.

Conclusion: Φ=[[1,-1,1],[1,0,0],[1,1,1]]; ŷ=(2,1,4)ᵀ. It is linear regression because fθ(x)=θ0+θ1x+θ2x² is linear in the unknown coefficients.

Checks: Φ is 3×3 and θ is 3×1. Nonlinearity in the input x does not introduce products or nonlinear functions of parameters.

### p10

Input SHA-256: `894d284bfff1f37a71b0601cdd675e186aee5f43262884869b9a079a3bede0bf`

#### Subpart a (symbolic)

Differentiate u² and -2u with respect to u and 3v² and 4v with respect to v.

Conclusion: ∇f=(2u-2,6v+4)ᵀ; ∇f(1,-1)=(0,-2)ᵀ.

Checks: Gradient is 2×1; mixed derivatives are both zero.

#### Subpart b (symbolic)

The mixed term 2uv contributes 2v to ∂/∂u and 2u to ∂/∂v.

Conclusion: ∇g=(2u+2v-4,2u+6v+2)ᵀ; ∇g(1,-1)=(-4,-2)ᵀ.

Checks: Gradient is 2×1; both mixed second derivatives are 2.

#### Subpart c (symbolic)

Let r=u+2v-w-3. Chain rule gives ∇h=2r∇r=2r(1,2,-1)ᵀ. At (1,0,-1), r=-1.

Conclusion: ∇h=(2r,4r,-2r)ᵀ; evaluated gradient=(-2,-4,2)ᵀ.

Checks: Gradient is 3×1; the negative w coefficient reverses the third component sign.

### p11

Input SHA-256: `fe3e947c89414cec11a78f5831f7c3d800ae2d3a40d0dcb911830816c46cdf50`

#### Subpart a (symbolic)

Use rows indexed by output coordinates and columns by input coordinates (u,v). The derivatives of u+2v are (1,2); those of 3u-v are (3,-1).

Conclusion: Jf=[[1,2],[3,-1]], also at (1,2).

Checks: Two outputs and two inputs require a 2×2 Jacobian; this linear map has constant derivative.

#### Subpart b (symbolic)

Differentiate each output: u²+v→(2u,1), uv→(v,u), v²→(0,2v).

Conclusion: Jg=[[2u,1],[v,u],[0,2v]]; Jg(1,2)=[[2,1],[2,1],[0,4]].

Checks: Three outputs and two inputs require a 3×2 Jacobian.

### p12

Input SHA-256: `a360c180da64468f9a7a96838472279d171bc7818b01e850d5f74b3666555f04`

#### Subpart a (symbolic)

Expand xᵀQx=3x1²+x1x2+x2x1+2x2² and -2bᵀx=-2x1+2x2.

Conclusion: h=3x1²+2x1x2+2x2²-2x1+2x2; ∂h/∂x1=6x1+2x2-2; ∂h/∂x2=2x1+4x2+2.

Checks: The two cross terms combine because scalar multiplication commutes; ∇h=2Qx-2b since Q is symmetric.

#### Subpart b (exact)

Set derivatives to zero: 3x1+x2=1, x1+2x2=-1. From x2=1-3x1, substitution gives -5x1=-3.

Conclusion: x1=3/5, x2=-4/5.

Checks: Qx=b exactly. Q has positive leading minors 3 and det Q=5, so Hessian 2Q is positive definite and this is also the unique minimum.

### p13

Input SHA-256: `d3b636a0aff3e8d68d4631d565bb01f730553b73d15e448e9f1210fface7797b`

#### Subpart main (exact)

det Σ=4-1=3 and Σ⁻¹=(1/3)[[2,-1],[-1,2]]. With a=x1-1,b=x2+1, the exponent is -(a²-ab+b²)/3. Expanding gives a²-ab+b²=x1²-x1x2+x2²-3x1+3x2+3.

Conclusion: pX(x1,x2)=1/(2π√3) exp[-(x1²-x1x2+x2²-3x1+3x2+3)/3], on R².

Checks: Σ≻0 since its first leading minor is 2 and determinant is 3. Normalizer follows (2π)^(-2/2)|Σ|^(-1/2), so integral=1; quadratic at μ=(1,-1) is 0.

### p14

Input SHA-256: `e64e219ca924a8432b5c11a9497651504981992d9e02defe77e26065e9546286`

#### Subpart main (exact)

4z²-8z+7=4(z-1)²+3. Thus integral p=c e^(-3/2)∫exp[-2(z-1)²]dz=c e^(-3/2)√(π/2). Setting it to 1 yields c=e^(3/2)√(2/π). The exponent -2(z-1)² is -(z-1)²/(2·1/4).

Conclusion: c=e^(3/2)√(2/π)>0; mean=1, variance=1/4.

Checks: Normalized density becomes √(2/π) exp[-2(z-1)²], whose integral is 1. c alone is not the Gaussian prefactor until the e^(-3/2) term is combined.

### p15

Input SHA-256: `641f6779f08ba7a99eb748bc6b527c0fbba3a5cb424760e92ed60404c6e6a18d`

#### Subpart main (symbolic)

Each independent residual εn=yn-θ0-θ1xn has density (2πσ²)^(-1/2)exp[-εn²/(2σ²)]. Multiply N densities: prefactors multiply to (2πσ²)^(-N/2), and exponent terms sum.

Conclusion: L(θ0,θ1)=(2πσ²)^(-N/2) exp[-Σn=1ᴺ(yn-θ0-θ1xn)²/(2σ²)].

Checks: Inputs are fixed, so this is the joint conditional data density as a function of parameters. σ²>0 ensures a positive finite normalizer.

### p16

Input SHA-256: `9834b6c0449369f81a6a974d50918c3e5f930886607bcf3b4807d9e7aacfa5f4`

#### Subpart main (symbolic)

The N-dimensional covariance determinant is (σ²)^N and inverse is I/σ². Taking minus the log of the Gaussian likelihood gives N log(2π)/2+N log(σ²)/2+||y-Φθ||²/(2σ²). The first terms are independent of θ and the SSE coefficient is positive.

Conclusion: -log L(θ)=N/2 log(2πσ²)+(1/(2σ²))||y-Φθ||₂². Therefore argmax L=argmin ||y-Φθ||₂².

Checks: Φ:N×K, θ:K×1, y:N×1; the norm is scalar. Since log is strictly increasing and negation reverses order, the optimization equivalence holds even if the minimizer is not unique.

### p17

Input SHA-256: `a300c14033a5515664cce85693463a015460163010d3d3e0f4a99e0c947a4680`

#### Subpart a (proof)

J=(y-Φθ)ᵀ(y-Φθ)=yᵀy-2θᵀΦᵀy+θᵀΦᵀΦθ. Because ΦᵀΦ is symmetric, ∇J=-2Φᵀy+2ΦᵀΦθ. Set to zero: ΦᵀΦθ=Φᵀy. For any nonzero v, vᵀΦᵀΦv=||Φv||²>0 under full column rank, so the matrix is invertible and Hessian 2ΦᵀΦ is positive definite.

Conclusion: θML=(ΦᵀΦ)⁻¹Φᵀy; normal equations ΦᵀΦθML=Φᵀy.

Checks: Gradient K×1 and Hessian K×K. Positive definiteness proves the unique global minimum, not merely stationarity.

#### Subpart b (exact)

Φ=[[1,-1],[1,0],[1,1]], ΦᵀΦ=diag(3,2), Φᵀy=(7,2)ᵀ. Solve to obtain (7/3,1)ᵀ. Predicted values are (7/3-1,7/3,7/3+1); residuals are (2/3,-4/3,2/3).

Conclusion: θML=(7/3,1)ᵀ; ŷ=(4/3,7/3,10/3)ᵀ; S=4/9+16/9+4/9=8/3.

Checks: Φᵀ(y-ŷ)=(0,0)ᵀ exactly, verifying the normal equations.

### p18

Input SHA-256: `7df9d65654045b0cef421f2205c243cafd3583bd4fcdc8aee710ea68c3bfeb9d`

#### Subpart main (proof)

Bayes gives -log posterior=||y-Φθ||²/(2σ²)+||θ||²/(2b²)+constant independent of θ. Its gradient is (ΦᵀΦθ-Φᵀy)/σ²+θ/b². Multiplication by σ² and setting zero yields (ΦᵀΦ+(σ²/b²)I)θ=Φᵀy. Multiplying the objective by the positive 2σ² gives SSE+(σ²/b²)||θ||².

Conclusion: λ=σ²/b²; θMAP=(ΦᵀΦ+λI_K)⁻¹Φᵀy.

Checks: λ>0. For v≠0, vᵀ(ΦᵀΦ+λI)v=||Φv||²+λ||v||²>0, so the inverse exists even without full rank. All coefficients, including the intercept, receive the penalty.

### p19

Input SHA-256: `120f11a24bf428e02386f675de83ccbb04af1588b707082d0b6a775f7a20dfd0`

#### Subpart a (exact)

ML solves diag(3,2)θ=(7,2)ᵀ. With σ²=b²=1, λ=1 and MAP solves diag(4,3)θ=(7,2)ᵀ.

Conclusion: θML=(7/3,1)ᵀ; θMAP at b²=1 is (7/4,2/3)ᵀ.

Checks: Both systems have nonzero diagonal entries, and substitution verifies both right-hand sides.

#### Subpart b (exact)

For b²=1/4, λ=1/(1/4)=4. MAP solves diag(7,6)θ=(7,2)ᵀ. Both coordinates shrink as denominators increase.

Conclusion: θMAP at b²=1/4 is (1,1/3)ᵀ. Coordinatewise 1<7/4<7/3 and 1/3<2/3<1; smaller b² strengthens the zero-centered prior and shrinks both intercept and slope toward zero.

Checks: This comparison uses the supplied diagonal Gram matrix; in a general correlated basis shrinkage is most directly characterized along eigenvectors of ΦᵀΦ.

### p20

Input SHA-256: `c08962ba8cb072f8ebd13afda502bda415e48708dbc3ebfeeaa2f771549e41f8`

#### Subpart a (exact)

Both columns equal (1,2)ᵀ; each column inner product is 1²+2²=5.

Conclusion: ΦᵀΦ=[[5,5],[5,5]], determinant=25-25=0.

Checks: Rank is 1, so the unregularized Gram matrix is singular.

#### Subpart b (exact)

Predictions depend only on θ1+θ2: Φθ=(θ1+θ2)(1,2)ᵀ. For A and B the sum is 3.

Conclusion: ΦθA=ΦθB=(3,6)ᵀ=y; both SSE values are 0.

Checks: Different parameters can yield identical fits because the columns are dependent.

#### Subpart c (exact)

J=5(3-θ1-θ2)²+5(θ1²+θ2²). The gradient equations after dividing by 10 are 2θ1+θ2=3 and θ1+2θ2=3. Subtract to get θ1=θ2, hence both are 1. At this point SSE=5 and penalty=5(1+1)=10.

Conclusion: Unique minimizer (θ1,θ2)=(1,1); minimum J=15.

Checks: Hessian=2(ΦᵀΦ+5I)=[[20,10],[10,20]] has eigenvalues 10 and 30>0, proving global uniqueness; the exact gradient at (1,1) is zero.

### p21

Input SHA-256: `27331836be2cd9cd445da45cadf09df6b43cddaec3770edad23a3c4901225ad0`

#### Subpart a (exact)

Sum coordinates: Σx=(1+1+3+3,1+3+3+5)ᵀ=(8,12)ᵀ; divide by 4.

Conclusion: x̄=(2,3)ᵀ.

Checks: Centered vectors sum to zero.

#### Subpart b (exact)

Centered vectors are (-1,-2),(-1,0),(1,0),(1,2). Their outer products sum to [[4,4],[4,8]]; divide by the specified 4.

Conclusion: S=[[1,1],[1,2]].

Checks: Symmetric 2×2 matrix with det=1>0. Denominator is 4 as requested, not the unbiased-estimator denominator 3.

### p22

Input SHA-256: `aec66e299c476d9dff94109f8ec8b719cc9f6eb9342fff309424d6e31ef518b6`

#### Subpart a (exact)

Set μx=(1,2)ᵀ, Σx=[[4,1],[1,2]], A=[[1,2],[-1,1]], b=(1,-2)ᵀ. Since y-μy=A(x-μx), μy=Aμx+b, Σy=AΣxAᵀ and Cxy=ΣxAᵀ. Matrix multiplication gives the following.

Conclusion: μy=(6,-1)ᵀ; Σy=[[16,-1],[-1,4]]; Cxy=[[6,-3],[5,1]].

Checks: μy:2×1 and both covariance matrices:2×2. Σy is symmetric while Cxy need not be. det Σx=7 and det A=3 imply det Σy=63, agreeing with 16·4-1.

#### Subpart b (exact)

Let u=x1-1,v=x2+1. Exponent is -(u²-2uv+2v²)/2, with precision H=[[1,-1],[-1,2]]. Thus μx=(1,-1)ᵀ and Σx=H⁻¹=[[2,1],[1,1]]. det H=1 and H11=1>0 verify a normalized Gaussian prefactor 1/(2π). For A=[[2,-1],[1,1]], b=(-1,2)ᵀ, use μy=Aμx+b, Σy=AΣxAᵀ, Cxy=ΣxAᵀ.

Conclusion: μx=(1,-1)ᵀ, Σx=[[2,1],[1,1]]; μy=(2,2)ᵀ; Σy=[[5,4],[4,5]]; Cxy=[[3,3],[1,2]].

Checks: HΣx=I2. det Σy=9=(det A)²det Σx=3²·1. The supplied density prefactor is correct because det Σx=1.

#### Subpart c (exact)

Cov(x1,x2)=E[x1x2]-E[x1]E[x2]=0-(1)(-1)=1, so Σx=[[2,1],[1,3]]. Set A=[[1,1],[1,-1]], e=(1,1)ᵀ, y=Ax+eε. Independence gives μy=A(1,-1)ᵀ, Σy=AΣxAᵀ+eeᵀVar ε, and Cxy=ΣxAᵀ. Before noise, AΣxAᵀ=[[7,-1],[-1,3]]; common noise adds [[1,1],[1,1]].

Conclusion: μy=(0,2)ᵀ; Σy=[[8,0],[0,4]]; Cxy=[[3,1],[4,-2]].

Checks: The same ε in both coordinates creates off-diagonal noise covariance 1, canceling the pre-noise covariance -1. Zero final covariance alone does not imply independence because Gaussianity is not given here.

### p23

Input SHA-256: `e3ed5a9a607688ceacf90e1f1d574f08ec0fde97b40ade295084ec084e4d1e7e`

#### Subpart a (exact)

Multiply the two N(θxn,1) data densities.

Conclusion: L(θ)=(2π)⁻¹ exp[-{(2-θ)²+(3-2θ)²}/2].

Checks: Two independent unit-variance observations give prefactor (2π)^(-2/2).

#### Subpart b (exact)

-log L=log(2π)+(1/2)[5θ²-16θ+13]. Its derivative is 5θ-8, zero at 8/5.

Conclusion: θML=8/5.

Checks: Second derivative 5>0 proves the unique minimum of negative log likelihood.

#### Subpart c (exact)

Adding prior N(0,1) adds θ²/2 plus a constant to the negative log posterior. Derivative becomes 6θ-8, so θMAP=8/6=4/3. Multiply both estimates by x=3.

Conclusion: θMAP=4/3; ŷML=24/5; ŷMAP=4.

Checks: Second derivative 6>0. MAP is closer to prior mean 0: 4/3<8/5.

### p24

Input SHA-256: `02ee0fd1452040e90b89a3477b86b5a519e2aed89fea92f3194722250e369a3b`

#### Subpart a (exact)

Multiply three independent N(θ,1) densities.

Conclusion: L(θ)=(2π)^(-3/2) exp[-{(2-θ)²+(3-θ)²+(4-θ)²}/2].

Checks: Three unit-variance observations determine the prefactor.

#### Subpart b (exact)

-log L=(3/2)log(2π)+(1/2)(3θ²-18θ+29). Differentiation gives 3θ-9.

Conclusion: θML=3.

Checks: Second derivative 3>0 ensures a unique optimum.

#### Subpart c (exact)

The N(1,1) prior adds (θ-1)²/2 to the negative log posterior, so derivative is (3θ-9)+(θ-1)=4θ-10.

Conclusion: θMAP=5/2; MAP is closer to prior mean 1 because |5/2-1|=3/2<|3-1|=2.

Checks: Second derivative 4>0. The estimate (9+1)/(3+1)=5/2 also follows from combining three data precision units and one prior precision unit.

### p25

Input SHA-256: `05797d24ffd68ab951beeadb0fcb9cb17dbab1ec44b932b09526ea0572f450f5`

#### Subpart main (exact)

Σ0⁻¹=diag(1,1/2), Σ1⁻¹=(1/3)[[2,-1],[-1,2]]. Their sum H=[[5/3,-1/3],[-1/3,7/6]] has determinant 11/6. The linear term h=Σ0⁻¹μ0+Σ1⁻¹μ1=(1/3,1/3)ᵀ. Completing the square gives covariance C=H⁻¹=(1/11)[[7,2],[2,10]] and mean m=Ch=(3/11,4/11)ᵀ. With u=x1-3/11,v=x2-4/11, (x-m)ᵀH(x-m)=(5/3)u²-(2/3)uv+(7/6)v².

Conclusion: m=(3/11,4/11)ᵀ; C=(1/11)[[7,2],[2,10]]. q(x)=√(11/6)/(2π) exp[-(10u²-4uv+7v²)/12], u=x1-3/11, v=x2-4/11.

Checks: HC=I2 and Hm=h exactly. det C=6/11, so normalizer=(2π)^(-1)(det C)^(-1/2)=√(11/6)/(2π). H11=5/3>0 and det H=11/6>0 prove integrability and positive covariance; the normalized Gaussian integral is 1.

## Own calculation log

30 exact matrix/derivative/stationarity calculations and 6 concrete density normalization integrals were evaluated by calculation_checks.py. The numeric integrals use a finite, positive absolute tolerance 1e-25; the largest observed absolute residual was approximately 1.3364e-51. These support the detailed algebra and do not replace proofs.

No reference answers have been compared and no academic approval is asserted.
