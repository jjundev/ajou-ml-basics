# Source/content academic review B

Reviewer `/root/ml_source_content_b`. Read-only, answer-aware academic review of current original conditions, asks, original quotes/figures and all seven explanation sections for **54 questions / 151 subparts / 7 packs**. Mathematical corroboration uses the current controller comparisons after reading actual explanations; this is **not blind independent derivation**. Product files and approvals were not edited.

**Current-content limitation:** 1007 p3(b) remains disputed: retained solve equates 67%/95% exactly with ±1σ/±2σ. Gaussian central masses are about68.268949%/95.449974%; exact67%/95% widths are about0.9741139σ/1.9599640σ. Its summary correctly omits the false equivalence but cannot repair the protected body.

**Conditional conclusions:** 0930 p1 dependence needs the nonconstant-square exception;0930 p3 prediction requires fresh noise independent of state/history or equivalent conditional moments, not merely marginal state/noise independence;0930 p4 finite variance needs finite second moment, explicitly stated in recall/sum;1007 p2 uses current adapted I/2 despite original quote I/4;1012 p8 future joint prediction explicitly adopts fresh exogenous noises in solve. These are retained conditions/limitations, not unconditional confirmations.

**Source evidence:**53 authentic source pages freshly rendered and visually read:43 MML,7HW1,3Lecture04rev. SHA-bound PNG paths are in `results.json` and the two page-binding JSON files. Historical pointers were used solely to locate pages. Exercise6.12 measurement/cross-covariance/joint prompts continue on **MML PDF230**, newly inspected. No course-produced PDF was regenerated or freshly QA-rendered.

**Figure and packet limitation:** current1007p3 schematic retains mean/trainingpoints/inner/outer boundaries but no67%/95%labels and no actual panel(c). Fresh MML PDF316 Figure9.10/caption confirms those source facts. This resolves current authentic-source provenance, **not** the blind packet omissions for1007p3(b,c). The packet remains incomplete as originally issued.

## Per-pack current bindings and findings

### review-0930-Bayesian_Linear_Regression

- Current HTML SHA256: `959aa5c2584b4687cf5f855beb0702c993fe784620369a367245d86e4aa267e4`
- Current source SHA256: `c9c79fe4933a1199ebe1a003c8662bb84b5652664acc185238ad7164ca18e4cc`
- Manifest SHA256: `67a208ac86b4064cdb0cb18e48527c34f5abca19f6e5269e66cc801cd613e787`
- Source visual: pass (fresh authentic source PDF visual and current-card comparison). Content: pass under the recorded conditions only.

**p1** — Source: MML Example6.5, PDF200: zero first/third moments and y=x² are retained. The original itself overstates dependence; current verify/pitfall disclose constant-x² exception.
Content (all seven sections): Substituting XY=X³ connects both given moments to covariance. Recall states finite moments; start is the substitution; solve gives covariance0; verify supplies a genuinely dependent example and the constant-square exception; pitfall/sum retain that distinction.
- p1:main: **pass / qualified_consistent** — Cov(X,X^2)=E[X^3]-E[X]E[X^2]=0; third-moment finiteness ensures required lower moments. Source wording that deterministic X^2 is necessarily dependent has a constant-X^2 exception, already disclosed in current verify/pitfall.

**p2** — Source: MML Example6.7 PDF207 supplies same-dimensional independent Gaussian weighted sum. General a,b are original, no figure data are required.
Content (all seven sections): Linearity governs the mean while centered outer products square a,b and eliminate both cross terms by independence. Recall is more than a title; start only begins with the mean, and solve/verify complete covariance and Gaussian law. Sum preserves independence.
- p2:main: **pass / consistent** — For same-dimensional independent vectors, centering yields covariance a^2 Sigma_x+b^2 Sigma_y and mean a mu_x+b mu_y. Both cross terms vanish. The Gaussian notation can include a degenerate measure; no ordinary-density inverse is asserted in this body.

**p3** — Source: MML Exercise6.5 PDF228–229(b1) is narrowed to one-step state prediction, not update after observing y(t+1). Current source states state/noise independence but not full fresh-noise exogeneity.
Content (all seven sections): Recall calls for new independent noise; verify invokes conditional independence. N(Aμt,AΣtAᵀ+Q) is correct under independence from (state,history), or corresponding conditional moments. State-only marginal independence does not establish this after conditioning; the retained body does not explain this gap fully. Sum preserves conditioning on past observations and excludes C/R from the state variance.
- p3:main: **pass / qualified_consistent** — The standard prediction mean A mu_t and covariance A Sigma_t A^T+Q agree conditional on fresh noise independent of the state and observation history. State-only marginal independence in the source is insufficient; current verify mentions conditional independence but does not explicitly distinguish it from the weaker source condition.

**p4** — Source: MML Exercise6.6 PDF229 and raw variance formula PDF198 identify a proof of the second-moment identity, with no required given figure.
Content (all seven sections): Expanding (x−μ)², applying linearity and substituting E[X]=μ proves E[X²]−μ². Recall explicitly requires finite second moment; solve/verify give general algebra, not only a numerical example. Pitfall and sum distinguish E[X²] from (E[X])².
- p4:main: **pass / qualified_consistent** — Expanding E[(X−μ)²] gives E[X²]−μ² under finite second moment; current recall explicitly states 이차 모멘트 유한성이 필요해요, and summary repeats it. Protected solve/verify themselves do not spell out that condition.

**p5** — Source: MML Exercise6.12(a) PDF229, same affine/noise model and likelihood ask. The current card explicitly supplies independent x,w.
Content (all seven sections): With x fixed, Ax+b is deterministic and only w remains random, giving N(Ax+b,Q). Recall selects conditioning, start writes the law, solve derives mean/covariance and verify recenters. Sum correctly excludes AΣxAᵀ from this conditional covariance.
- p5:main: **pass / consistent** — Fixing x leaves only w random; both give N(Ax+b,Q), with no A Sigma_x A^T term. A maps D to E and Q is ExE.

**p6** — Source: MML Exercise6.12(b) PDF229, marginal mean/covariance and Gaussianity supplied, E×D mapping retained.
Content (all seven sections): Centering removes b, and x,w independence removes both mixed covariance terms. AΣxAᵀ+Q is E×E and Aμx+b is E×1. Solve and verify carry general component/outer-product arguments; sum retains order and independent-noise condition.
- p6:main: **pass / consistent** — Centering removes b and independent input/noise cross terms; both give A mu_x+b and A Sigma_x A^T+Q, with ExE covariance.

**p7** — Source: MML Exercise6.12(c) actually continues on PDF230, which was newly rendered and read; conditional z|y and marginal z asks both retained, with v added after C.
Content (all seven sections): Recall contrasts y fixed versus random. Start writes both centered expressions; solve/verify answer (a) N(Cy,R) and (b) Cμy,CΣyCᵀ+R. Pitfall and sum keep R outside the transformation C.
- p7:a: **pass / consistent** — Conditioning on y leaves N(Cy,R).
- p7:b: **pass / consistent** — Another affine transformation gives mean C(A mu_x+b), covariance C(A Sigma_x A^T+Q)C^T+R; measurement noise is added after C.

**p8** — Source: MML Exercise6.7 PDF229 refers to raw-score identity (6.45); current card supplies the complete ordered-pair equality and asks its proof.
Content (all seven sections): Expand all ordered-pair squared differences: each squared term repeats N times, cross term factors into (Σx)². Recall/start give this mechanism; solve/verify prove for arbitrary observations and N>0. Pitfall/sum prohibit replacing the specified N by N−1.
- p8:main: **pass / consistent** — The two squared terms each repeat N times, the cross term factors into (sum x_i)^2, yielding the exact ordered-pair identity with N^2 normalization, N≥1.

### review-1007-Product_of_Gaussians

- Current HTML SHA256: `f0a6a858e4d2795cc4d216399dbc8f122735cf577ab629aa64f7a7080258f300`
- Current source SHA256: `fd32f20f21c4492eef1130e37aa12a1649fd9915fc4dcc629211ce0172605e89`
- Manifest SHA256: `e8535c3bfc8baf3f16d063b97e8595209a041a272e09229ab4318453b826b8bc`
- Source visual: pass (fresh authentic source PDF visual and current-card comparison). Content: disputed.

**p1** — Source: MML Example9.7 PDF311: degree5, prior I/4,200inputs in[-5,5], noise-free f and67%/95% shading match. Original figure9.9 is qualitative; no extra numerical givens omitted.
Content (all seven sections): One theta draw must be shared across200inputs; six coefficients give R6; latent function uncertainty comes only from parameter prior. Recall explains function prior, start is one draw, solve/verify answer all(a–c), pitfall/sum exclude re-drawing at each x and adding observation noise.
- p1:a: **pass / consistent** — One six-vector prior draw shared across all 200 inputs defines one polynomial curve.
- p1:b: **pass / consistent** — Degree 5 requires coefficients 0..5, so theta∈R6.
- p1:c: **pass / consistent** — At fixed x, phi^T(I/4)phi is parameter-induced prior uncertainty of noise-free f; the supplied credible levels are pointwise, not simultaneous curve coverage.

**p2** — Source: Explicit numeric adaptation: current prior I/2 differs from original quoted Example9.7 I/4 on PDF311. The current conditions and solve both explicitly use I/2; do not apply quote as authoritative adapted numbers.
Content (all seven sections): Affine scalar variance φᵀS0φ gives means0 and variances1/2 at0,3 at1 for current I/2. Recall names S0=I/2 and coefficient-square mechanism; start evaluates φ(0); solve/verify evaluate both points, pitfall/sum distinguish variance from standard deviation.
- p2:main: **pass / qualified_consistent** — Current SourcePack explicitly uses I/2, giving means zero and variances 1/2 at 0 and 3 at 1. Current solve also explicitly uses I/2. Historical quote uses I/4 and would instead give 1/4 and 3/2. No unspoken precedence assumption is needed: both current conditions and reference disclose the adapted covariance.

**p3** — Source: MML Example9.8 PDF315–316 and actual Figure9.10(b,c): MAP=mean function, caption67%/95%, and posterior-sampled curves are authentic. Current schematic SVG depicts(b) only with inner/outer dashed bounds but lacks numeric mass labels and actual(c). Authentic source resolves provenance; blind packet remains incomplete for(b,c).
Content (all seven sections): Recall uses nondegenerate Gaussian mode=mean; solve(a) and(c) explain linear mean and shared posterior draws. Solve(b) falsely equates stated67%/95% to exact±1σ/±2σ. Verify/pitfall distinguish latent/observed and pointwise/simultaneous, sum omits false identity, but that does not repair protected solve. This item remains disputed.
- p3:a: **pass / consistent** — For an ordinary Gaussian posterior, mode=mean=mN and the linear image mean equals the MAP function; MLE need not agree.
- p3:b: **disputed / disagreement** — Posterior uncertainty bands and authentic MML Figure9.10 caption agree on 67%/95%. Packet alone omitted these labels. However current solve additionally equates them to exactly ±1σ/±2σ; central Gaussian coverages are 68.268949% and 95.449974%, so that exact equivalence disagrees with the frozen precise quantile check.
- p3:c: **pass / qualified_consistent** — The posterior draw construction in current solve agrees with frozen conditional interpretation. Authentic MML p316 Figure9.10(c) and its caption now verify the sampling provenance that was absent from the blind packet; this controller-only check does not retroactively make the packet complete.

**p4** — Source: Explicit numerical adaptation of MML Example6.6 PDF206: original μ=(0,2),Σ=[[.3,−1],[−1,5]], current μ=(1,2),Σ=[[.5,−1],[−1,4]]. Current asks only marginal x1, not conditional x1|x2=−1.
Content (all seven sections): Marginalization retains μ1=1,Σ11=.5, so N(1,.5); determinant1 and positive leading minor validate current covariance. Recall/start/solve/verify select marginal entries, pitfall/sum reject conditional Schur-complement substitution.
- p4:main: **pass / consistent** — Marginalization retains mean entry 1 and variance entry 1/2; determinant 1 and leading minor 1/2 confirm a valid joint Gaussian.

**p5** — Source: Numerical weighted-sum variant of Example6.7 PDF207: current x~N(1,2), y~N(−1,3),a=2,b=−1 are explicit authoritative numbers.
Content (all seven sections): Mean2·1−(−1)=3 and independent variance4·2+3=11. Recall/start select linear mean and squared coefficients; solve/verify compute both; pitfall/sum prevent subtracting variance.
- p5:main: **pass / consistent** — Independent Gaussian mean 2(1)-(-1)=3 and variance 4(2)+3=11 agree, including the squared negative coefficient.

**p6** — Source: Exercise6.2(a) PDF228 matches exact mixture weights .4/.6,means(10,2)/(0,0),covariancesI and[[8.4,2],[2,1.7]]. Only marginal distributions are selected; omitted mode/median demands are outside current card.
Content (all seven sections): Integral linearity preserves component weights and marginal μ/diagonal variance: x1=.4N(10,1)+.6N(0,8.4), x2=.4N(2,1)+.6N(0,1.7). Recall explains mixture versus single Gaussian; verify checks unit total mass; pitfall/sum keep two components.
- p6:main: **pass / consistent** — Integrating each mixture component retains weights .4,.6 and marginal parameters (10,1)/(0,8.4) and (2,1)/(0,1.7). Each mixture normalizes to one.

**p7** — Source: Exercise6.2(b,c) PDF228 narrowed to means, not all original mode/median asks. Current asks(a) coordinate means and(b) stack mean vector, same exact mixture numbers.
Content (all seven sections): Linearity of mixture expectation gives4 and.8, then[4,.8]ᵀ. Recall connects selection weights to means; start writes vector combination; solve/verify cover both parts. Pitfall/sum do not misapply weighted means to covariance.
- p7:a: **pass / consistent** — Mixture-weighted means are 4 and .8.
- p7:b: **pass / consistent** — Stacking these coordinate means gives [4,.8]^T, a 2x1 vector.

**p8** — Source: Exercise6.10(a) PDF229 narrowed to completing square and proportional Gaussian shape, not exponential-family alternative or calculation of multiplicative constant. A,B symmetric invertible covariances imply positive definiteness.
Content (all seven sections): With Λ=A⁻¹+B⁻¹ and η=A⁻¹a+B⁻¹b, center Λ⁻¹η yields C=Λ⁻¹,c=Cη and an x-independent residual constant. All sections retain matrix order, SPD condition and ∝; verify is general algebra, not numerical-only proof.
- p8:main: **pass / consistent** — General symmetric positive-definite precision sum and vector eta give C=(A^-1+B^-1)^-1 and c=C eta. Both complete-square derivations preserve matrix order and an x-independent constant, correctly retaining proportionality rather than equality.

### review-1012-Several_Mathematical_Proofs

- Current HTML SHA256: `eb59b5cb422c8c374bc875b485c2c43ea788d4a6d32a5271b4c354d2af3cc1c5`
- Current source SHA256: `f7fd19d05dbeb533a91e917c193e9f849640f7951386038236cfeb31d43d1a7c`
- Manifest SHA256: `292844adb1340effadf86921f790b1b4acc4cd71cc402f3475d3995e28afe79d`
- Source visual: pass (fresh authentic source PDF visual and current-card comparison). Content: pass under the recorded conditions only.

**p1** — Source: Example4.2 PDF107 gives determinant-area principle; current b=(2,1),g=(0,3)/(4,2) are numeric variants of its two-dimensional explanation, not its later3D numerical exercise.
Content (all seven sections): Area uses absolute determinant, yielding6 and0; g=2b explains zero area. Recall/start select column construction and signed-area distinction; solve/verify cover both, pitfall/sum preserve absolute value.
- p1:a: **pass / consistent** — Absolute determinant of columns [2,1]^T,[0,3]^T is 6.
- p1:b: **pass / consistent** — Columns [2,1]^T,[4,2]^T are dependent, so determinant and area are zero.

**p2** — Source: Example4.1 PDF106 gives 2×2 inverse/determinant rule; currentΣ=[[4,2],[2,10]] is a practice matrix, not a quoted source numeric matrix.
Content (all seven sections): det36≠0 allows inverse(1/36)[[10,−2],[−2,4]]. Recall/start apply determinant and adjugate; solve/verify show multiplication toI; pitfall/sum reject elementwise reciprocals.
- p2:a: **pass / consistent** — det Sigma=4(10)-2(2)=36≠0; first leading minor 4 also confirms positive definiteness.
- p2:b: **pass / consistent** — The adjugate divided by 36 gives [[10,-2],[-2,4]]/36; both multiplication orders return I2.

**p3** — Source: Example6.17 PDF225–226 general2D standard Gaussian and invertibleA formula retained; reverse-Jacobian determinant required, no extra source figure.
Content (all seven sections): Use x=A⁻¹y, inverse Jacobian|detA|⁻¹, precisionA⁻ᵀA⁻¹ and normalizer1/(2π|detA|). Recall/start explain inverse substitution and mass conservation; solve/verify prove normalization for arbitrary invertibleA. Sum keeps ad−bc≠0 and orientation absolute value.
- p3:main: **pass / consistent** — The inverse Jacobian has absolute determinant 1/|ad-bc|; substituting A^-1 y gives precision A^-T A^-1. The density integrates to one and agrees with N(0,AA^T), including orientation reversal.

**p4** — Source: Explicit numerical application of Example6.17 withA=diag(3,2), not an original numeric textbook problem.
Content (all seven sections): Inverse(y1/3,y2/2), area6 and covariance diag(9,4) give density1/(12π) exp[−(y1²/9+y2²/4)/2], same height at0. Recall/start set inverse axes, solve/verify complete density and origin; pitfall/sum distinguish axis scaling from variance.
- p4:main: **pass / consistent** — Inverse coordinates y1/3,y2/2 and area factor 1/6 give normalizer 1/(12pi), exponent -(y1^2/9+y2^2/4)/2, and the same height at zero.

**p5** — Source: Explicit numerical application of Example6.17 withA=[[1,1],[0,2]]; all current inverse/Jacobian/density asks are retained.
Content (all seven sections): Inverse[[1,−1/2],[0,1/2]], determinant1/2 and quadratic y1²−y1y2+y2²/2 give density1/(4π). Recall/start choose inverse components; solve/verify answer(a–c); pitfall/sum preserve negative mixed-term sign.
- p5:a: **pass / consistent** — Inverse [[1,-1/2],[0,1/2]] agrees and AA^-1=I2.
- p5:b: **pass / consistent** — The inverse Jacobian determinant is 1/2.
- p5:c: **pass / consistent** — The exponent quadratic y1^2-y1y2+y2^2/2 and normalizer 1/(4pi) agree; AA^T=[[2,2],[2,4]].

**p6** — Source: Exercise6.12(d) Hint is on PDF230, not solely historical229: it explicitly asks cross covariances as a prerequisite to posterior. Current card isolates that prerequisite and retains separate x/w independence and diagonalQ source wording.
Content (all seven sections): Centering yields Cov(x,y)=ΣxAᵀ D×E and reverseAΣx E×D. Recall identifies which variable owns rows/columns; solve/verify cancel independent-noise term; pitfall/sum correctly say diagonalQ alone does not imply vector independence.
- p6:main: **pass / consistent** — Centering gives Cov(x,y)=Sigma_x A^T (DxE), reverse covariance A Sigma_x (ExD). Current pitfall correctly distinguishes input/noise independence from diagonality of Q.

**p7** — Source: Exercise6.12(d) Hint PDF230 explicitly calls for jointGaussianp(x,y). Current card isolates joint construction, supplies crossblocks, and does not purport to solve later conditioned posterior.
Content (all seven sections): Stack means[μx,Aμx+b] and blocks[[Σx,ΣxAᵀ],[AΣx,AΣxAᵀ+Q]]. Recall/start select joint vector; solve/verify assemble via block linear transform; pitfall/sum keepQ in lower-right block and state diagonalQ is unnecessary.
- p7:main: **pass / consistent** — Stacking means and self/cross covariance blocks gives [[Sigma_x,Sigma_x A^T],[A Sigma_x,A Sigma_x A^T+Q]], symmetric of dimension (D+E)^2. Diagonal Q is not required.

**p8** — Source: Exercise6.5(b2) PDF229 asks future-state/future-measurement joint conditional on past; not(b3)measurement-updateposterior. Noise-onlyi.i.d wording is interpreted with fresh exogenous noises, disclosed explicitly in current solve.
Content (all seven sections): Given fresh noises independent of state/history, P=AΣtAᵀ+Q, mean[Aμt,CAμt], blocks[[P,PCᵀ],[CP,CPCᵀ+R]]. Recall/solve explicitly state exogeneity, verify reuses joint transform; pitfall/sum distinguish time indices and predict before new observation. Conclusion stays conditional on that assumption.
- p8:main: **pass / qualified_consistent** — With independent fresh noises, P=A Sigma_t A^T+Q and the future joint blocks are [[P,PC^T],[CP,CPC^T+R]], means [A mu_t;CA mu_t]. Current solve explicitly states exogeneity missing from a literal noise-only i.i.d. reading of the source; the formula is therefore conditional, not universally inferred from that phrase.

### review-1014-Bayesian_Posterior_Prediction

- Current HTML SHA256: `4348040da6e6b328dadce20ed0263fc185eab4d53a0745c5e7970f768be14e2b`
- Current source SHA256: `7d1a684d5150b21d139baeaf733330762846b78bc50c91ecc7d2f0540f6af94c`
- Manifest SHA256: `77ad49fdd763d48fb8169f5b3d7cd46a4161a0920e8528bf64a320d540f92a36`
- Source visual: pass (fresh authentic source PDF visual and current-card comparison). Content: pass.

**p1** — Source: Example6.3 grey box PDF188–189 has exactlystates−1.1,.3,1.5 and uniformsupport.9–1.6; Figure6.3 is explanatory, all needed values are explicit in current conditions.
Content (all seven sections): Equal mass gives1/3 each; width.7 gives height10/7 and integral1. Recall explicitly distinguishes PMFsum and PDFarea, start writes3q=1 and.7h=1, solve/verify cover both asks, pitfall/sum reject interpreting density as point probability.
- p1:a: **pass / consistent** — Three equal nonnegative masses give 1/3 each and sum one.
- p1:b: **pass / consistent** — Support width 7/10 requires density 10/7; integration equals one and the height is not point mass.

**p2** — Source: Example6.13 grey box PDF218 exactlysuppliesφ=(x,x²), θ=(μ/σ²,−1/(2σ²)); current task narrows to completing square and normalization rather than requiring exponential-family theory.
Content (all seven sections): Forσ²>0 exponent=−(x−μ)²/(2σ²)+μ²/(2σ²). Originalkernel normalization C=e^(−μ²/(2σ²))/√(2πσ²), so normalizedN(μ,σ²). Recall/start explain coefficients and integrability; solve/verify retain constant and general proof; pitfall/sum distinguish originalkernel from centeredkernel.
- p2:main: **pass / consistent** — Completing the square leaves -(x-mu)^2/(2sigma^2)+mu^2/(2sigma^2). Current and frozen normalization include exp(-mu^2/(2sigma^2))/sqrt(2pi sigma^2) for the original kernel; the normalized law is N(mu,sigma^2), valid for sigma^2>0.

### review-1019-Prediction_and_Projection

- Current HTML SHA256: `761ce4341f5aa94297be60f7ba7eda9d91f18d49341ead16c653b9990a91b213`
- Current source SHA256: `0c4b2cd33b500b1bae65840c73f8078cb8319fa4361fceb23beca0cbdee4dfd8`
- Manifest SHA256: `6faecd3df22908f800f12f53982617e498249df4af7eeac91fb828c7389b88dd`
- Source visual: pass (reuse of genuinely completed task6c current source_visual; its source-PDF, question-payload and all3PNGs were verified directly). Content: pass.

**p1** — Source: Current task6c visual evidence confirms Example3.10 R3 line projector/reprojection; p1/p5 original numeric inputs, otherquestions explicit practice numeric variants. No required given figures.
Content (all seven sections): Recall explains nearest-point residualorthogonality, nonzero direction andscalar innerproduct versus3×3outerproduct. Start computesnormsquare. Solve/verify answer(a)P,(b)Px,(c)reprojection, including fullmatrix square. Pitfall/sum distinguish orthogonalprojection from length-preserving orthogonalmatrix.
- p1:a: **pass / consistent** — For b=[1,2,2], b^T b=9 and bb^T/9 gives the same full 3x3 matrix.
- p1:b: **pass / consistent** — b^T x=5 gives lambda=5/9 and projection [5,10,10]^T/9; residual [4,-1,-1]^T/9 is orthogonal.
- p1:c: **pass / consistent** — The current full matrix square and frozen algebra both establish P^2=P, and reapplying P to this projection preserves it.

**p2** — Source: Current task6c visual evidence confirms Example3.10 R3 line projector/reprojection; p1/p5 original numeric inputs, otherquestions explicit practice numeric variants. No required given figures.
Content (all seven sections): Recall explains nearest-point residualorthogonality, nonzero direction andscalar innerproduct versus3×3outerproduct. Start computesnormsquare. Solve/verify answer(a)P,(b)Px,(c)reprojection, including fullmatrix square. Pitfall/sum distinguish orthogonalprojection from length-preserving orthogonalmatrix.
- p2:a: **pass / consistent** — Unit first-axis direction gives diag(1,0,0), a 3x3 orthogonal projector.
- p2:b: **pass / consistent** — The projection is [2,0,0]^T and the removed coordinates are [0,3,1]^T.
- p2:c: **pass / consistent** — Squaring the displayed diagonal matrix and reprojecting [2,0,0]^T leave each unchanged.

**p3** — Source: Current task6c visual evidence confirms Example3.10 R3 line projector/reprojection; p1/p5 original numeric inputs, otherquestions explicit practice numeric variants. No required given figures.
Content (all seven sections): Recall explains nearest-point residualorthogonality, nonzero direction andscalar innerproduct versus3×3outerproduct. Start computesnormsquare. Solve/verify answer(a)P,(b)Px,(c)reprojection, including fullmatrix square. Pitfall/sum distinguish orthogonalprojection from length-preserving orthogonalmatrix.
- p3:a: **pass / consistent** — Unit second-axis direction gives diag(0,1,0), not the first-axis projector.
- p3:b: **pass / consistent** — Projection is [0,2,0]^T, with second-coordinate placement matching both methods.
- p3:c: **pass / consistent** — The full matrix square and reprojected vector equal the original projector/vector.

**p4** — Source: Current task6c visual evidence confirms Example3.10 R3 line projector/reprojection; p1/p5 original numeric inputs, otherquestions explicit practice numeric variants. No required given figures.
Content (all seven sections): Recall explains nearest-point residualorthogonality, nonzero direction andscalar innerproduct versus3×3outerproduct. Start computesnormsquare. Solve/verify answer(a)P,(b)Px,(c)reprojection, including fullmatrix square. Pitfall/sum distinguish orthogonalprojection from length-preserving orthogonalmatrix.
- p4:a: **pass / consistent** — b=[1,1,1] has squared norm3, so P is the all-ones 3x3 matrix divided by3.
- p4:b: **pass / consistent** — x=3b already lies on the line, hence projection [3,3,3]^T and zero residual.
- p4:c: **pass / consistent** — The all-ones matrix squares to three times itself, so P^2=P; preserving this x alone would not establish P=I, as current pitfall notes.

**p5** — Source: Current task6c visual evidence confirms Example3.11 R3 two-basis coordinates/projection/norm/projector/orthogonality/idempotence; p1/p5 original numeric inputs, otherquestions explicit practice numeric variants. No required given figures.
Content (all seven sections): Recall explains full-column-rank3×2basis/Gram equations,2Dcoefficients versus3Dpoint,Euclideannorm and3×3projector. Start writesBᵀresidual0. Solve/verify answer(a–d) with allmatrixentries,orthogonalresidual andfull-matrixidempotence. Pitfall/sum retainrank,dimensions,normnotnormsquare, andsymmetry-onlyinsufficiency.
- p5:a: **pass / consistent** — G=[[3,3],[3,5]], det6 and right-hand side [6,0]^T give coordinates [5,-3]^T.
- p5:b: **pass / consistent** — Projection [5,2,-1]^T leaves residual [1,-2,1]^T, Euclidean error sqrt6 rather than squared error6.
- p5:c: **pass / consistent** — BG^-1 B^T equals [[5,2,-1],[2,2,2],[-1,2,5]]/6 in both results; coefficient map is 2x3 and projector3x3.
- p5:d: **pass / consistent** — Both basis-residual inner products vanish. General BG^-1 G G^-1 B^T=P and actual M^2=6M establish full-matrix idempotence.

**p6** — Source: Current task6c visual evidence confirms Example3.11 R3 two-basis coordinates/projection/norm/projector/orthogonality/idempotence; p1/p5 original numeric inputs, otherquestions explicit practice numeric variants. No required given figures.
Content (all seven sections): Recall explains full-column-rank3×2basis/Gram equations,2Dcoefficients versus3Dpoint,Euclideannorm and3×3projector. Start writesBᵀresidual0. Solve/verify answer(a–d) with allmatrixentries,orthogonalresidual andfull-matrixidempotence. Pitfall/sum retainrank,dimensions,normnotnormsquare, andsymmetry-onlyinsufficiency.
- p6:a: **pass / consistent** — The orthonormal two-column basis gives G=I2, coordinates [2,3]^T.
- p6:b: **pass / consistent** — Projection [2,3,0]^T leaves residual [0,0,4]^T and error4, not squared error16.
- p6:c: **pass / consistent** — Projector diag(1,1,0) agrees with BB^T and has size3x3.
- p6:d: **pass / consistent** — Both basis-residual inner products vanish and the full diagonal matrix square equals P.

**p7** — Source: Current task6c visual evidence confirms Example3.11 R3 two-basis coordinates/projection/norm/projector/orthogonality/idempotence; p1/p5 original numeric inputs, otherquestions explicit practice numeric variants. No required given figures.
Content (all seven sections): Recall explains full-column-rank3×2basis/Gram equations,2Dcoefficients versus3Dpoint,Euclideannorm and3×3projector. Start writesBᵀresidual0. Solve/verify answer(a–d) with allmatrixentries,orthogonalresidual andfull-matrixidempotence. Pitfall/sum retainrank,dimensions,normnotnormsquare, andsymmetry-onlyinsufficiency.
- p7:a: **pass / consistent** — Same G as p5 with right-hand side [6,6]^T gives coordinates [2,0]^T; a zero coefficient does not change basis independence.
- p7:b: **pass / consistent** — Projection [2,2,2]^T leaves [-2,4,-2]^T, squared norm24 and norm sqrt24=2sqrt6.
- p7:c: **pass / consistent** — The same plane projector as p5 agrees entrywise: [[5,2,-1],[2,2,2],[-1,2,5]]/6.
- p7:d: **pass / consistent** — Both actual inner products vanish; M^2=6M and the general Gram argument establish full P^2=P, not just invariance of one vector.

**p8** — Source: Current task6c visual evidence confirms Example3.11 R3 two-basis coordinates/projection/norm/projector/orthogonality/idempotence; p1/p5 original numeric inputs, otherquestions explicit practice numeric variants. No required given figures.
Content (all seven sections): Recall explains full-column-rank3×2basis/Gram equations,2Dcoefficients versus3Dpoint,Euclideannorm and3×3projector. Start writesBᵀresidual0. Solve/verify answer(a–d) with allmatrixentries,orthogonalresidual andfull-matrixidempotence. Pitfall/sum retainrank,dimensions,normnotnormsquare, andsymmetry-onlyinsufficiency.
- p8:a: **pass / consistent** — G=[[5,1],[1,2]], det9 and right-hand side [5,4]^T give coordinates [2/3,5/3]^T.
- p8:b: **pass / consistent** — Projection [7/3,4/3,5/3]^T leaves [-4/3,2/3,4/3]^T and norm2.
- p8:c: **pass / consistent** — Projector [[5,2,4],[2,8,-2],[4,-2,5]]/9 agrees entrywise, with symmetric cross terms and correct 3x3 shape.
- p8:d: **pass / consistent** — Both basis-residual inner products vanish; current explicit M^2=9M and frozen general Gram proof both imply P^2=P.

### exam-0909-1019-Midterm_Practice_01

- Current HTML SHA256: `253df05c4a96bd507394ad7ebd9813ef453f257ef4d9528119e96ce1ca0f5b37`
- Current source SHA256: `0854695247aa8ab335b125975070dd21077d219cd402184b828ad503547a2946`
- Manifest SHA256: `beaa443d4249c0bb7b2c0b63fe0720f7283e36c70636dbdb15d85eb2109f6ed6`
- Source visual: pass (fresh authentic source PDF visual and current-card comparison). Content: pass.

**p1** — Source: HW1P6–8 PDF3; changedvectors and RHS explicitly define currentvariant. No copiedoriginalexerciseclaim.
Content (all seven sections): Nontrivialrelation, all-solutionsfamily, column-space incompatibility and Gram invertibility each answered. Recall defines homogeneous independence and Gram quadratic form; start is relation, solve/verify cover a–c; pitfall/sum distinguish existence from uniqueness.
- p1:a: **pass / consistent** — Linearly dependent; rank V=2 since v1,v2 have independent first two coordinates. Current solve and verify read directly and agree; Dependency, affine solution family, incompatibility and explicit Gram/inverse/singularity agree.
- p1:b: **pass / consistent** — For b all solutions are (2-t,1-t,t)^T, t real. For c there is no solution. Current solve and verify read directly and agree; Dependency, affine solution family, incompatibility and explicit Gram/inverse/singularity agree.
- p1:c: **pass / consistent** — U^T U is invertible; V^T V is singular. Current solve and verify read directly and agree; Dependency, affine solution family, incompatibility and explicit Gram/inverse/singularity agree.

**p2** — Source: HW1P10–12 PDF3–4 with changedfunction,A,b; explicitcolumn-gradient/output×inputJacobian convention differs from MML rowgradient convention.
Content (all seven sections): Recall names each derivative object, start expands scalarq. Solve/verify provideJacobian,Ax−b,HessianA,stationary(2/7,−1/7) andSPD global-minimum proof. Pitfall/sum preservehalf-factor anddimensions.
- p2:a: **pass / consistent** — J_f(1,2)=[[2,1],[2,1]], dimension 2x2. Current solve and verify read directly and agree; General/point Jacobians, gradient/Hessian and unique SPD minimum agree; independent extra minimum value also correct.
- p2:b: **pass / consistent** — gradient q=(4x1+x2-1,x1+2x2)^T=A x-b; Hessian=A. Current solve and verify read directly and agree; General/point Jacobians, gradient/Hessian and unique SPD minimum agree; independent extra minimum value also correct.
- p2:c: **pass / consistent** — Unique global minimum at (2/7,-1/7)^T; value -1/7. Current solve and verify read directly and agree; General/point Jacobians, gradient/Hessian and unique SPD minimum agree; independent extra minimum value also correct.

**p3** — Source: HW1P14/P25 PDF5/9 inspire scalarGaussianproduct with changedmeans/variances; source is a new numeric variant.
Content (all seven sections): Recall identifiesprecision/normalization; start gathersquadratic. Solve/verify preserveconstant+1, q=N(.5,.75),Z=e^(−.5)/√(8π); pitfall/sum distinguish normalizeddensity fromunnormalizedproduct.
- p3:a: **pass / consistent** — Completed square: (4/3)(z-1/2)^2+1. Current solve and verify read directly and agree; Completed square, normalized Gaussian mean/variance/density and product integral agree exactly.
- p3:b: **pass / consistent** — q(z)=sqrt(2/(3 pi))*exp[-(2/3)(z-1/2)^2]; mean 1/2, variance 3/4. Current solve and verify read directly and agree; Completed square, normalized Gaussian mean/variance/density and product integral agree exactly.
- p3:c: **pass / consistent** — Z=exp(-1/2)/sqrt(8 pi). This is not 1, so g itself is not a probability density; g=Z q. Current solve and verify read directly and agree; Completed square, normalized Gaussian mean/variance/density and product integral agree exactly.

**p4** — Source: HW1P17–20 PDF6–7: changedy=(0,1,4),samefeature(1,x),noisevariance1,andprioronbothcoefficients.
Content (all seven sections): Recall/start set3×2design, fullcolumnrank andall-coefficientprior. Solve/verify computeG=diag(3,2),rhs(5,4),ML(5/3,2),MAP(5/4,4/3),predictions17/3,47/12. Pitfall/sum retaininterceptprior andobservationorder.
- p4:a: **pass / consistent** — Phi=[[1,-1],[1,0],[1,1]], Phi^T Phi=diag(3,2), Phi^T y=(5,4)^T. Current solve and verify read directly and agree; Feature Gram/RHS, ML/MAP coefficients, regularized objective and predictions agree exactly.
- p4:b: **pass / consistent** — theta_ML=(5/3,2)^T; mean prediction=17/3. Current solve and verify read directly and agree; Feature Gram/RHS, ML/MAP coefficients, regularized objective and predictions agree exactly.
- p4:c: **pass / consistent** — theta_MAP=(5/4,4/3)^T; mean prediction=47/12. The prior penalizes both coefficients and shrinks them toward zero. Current solve and verify read directly and agree; Feature Gram/RHS, ML/MAP coefficients, regularized objective and predictions agree exactly.

**p5** — Source: HW1P21–22 PDF7–8: changedthree-pointuniformX andA,b. CurrentnonGaussianfinite-supportmodel is explicit.
Content (all seven sections): Recall/start selectempiricalNdenominator,affinecrosscovariance andfinite-supportindependencecheck. Solve/verify computeallmoments andshowzerojointprobability versus1/9product; sum correctlykeepsuncorrelatedyetdependent.
- p5:a: **pass / consistent** — mu_X=(2/3,2/3)^T; Sigma_X=[[8/9,-4/9],[-4/9,8/9]]. Current solve and verify read directly and agree; Means/covariance/cross-covariance agree; independent discrete-event counterexample differs from reference event but proves the same dependence correctly.
- p5:b: **pass / consistent** — mu_Y=(7/3,-1)^T; Sigma_Y=diag(8/9,8/3); C_XY=[[4/9,4/3],[4/9,-4/3]]. Current solve and verify read directly and agree; Means/covariance/cross-covariance agree; independent discrete-event counterexample differs from reference event but proves the same dependence correctly.
- p5:c: **pass / consistent** — Uncorrelated but dependent, established directly from their actual discrete joint distribution. Current solve and verify read directly and agree; Means/covariance/cross-covariance agree; independent discrete-event counterexample differs from reference event but proves the same dependence correctly.

**p6** — Source: Theory-groundednewderivationusingMML9.2 PDF298–300/302,notverbatimtextbookexercise.
Content (all seven sections): Recall connectsindependentfixedpositiveGaussiannoise toproductlikelihood,known-varianceNLL andERM. Solve/verify retainconstants,Nscale,quadraticgradient,fullrankuniqueness andparameter-linearityofpolynomialfeatures; pitfall/sum keepconditionalindependence andvariancefixed.
- p6:a: **pass / consistent** — y_n | x_n,theta ~ N(theta0+theta1 x_n,sigma^2), conditionally independent. Current solve and verify read directly and agree; Conditional IID Gaussian model, likelihood/NLL/risk scaling, normal equations, rank uniqueness and parameter-linearity agree. Reference differentiates explicitly defined SSE Q; blind result additionally gives Rhat gradient scaled by1/N; actual(d)asks squared-error gradient and both yield same normal equations.
- p6:b: **pass / consistent** — p(y|Phi,theta)=(2 pi sigma^2)^(-N/2)exp[-||y-Phi theta||^2/(2 sigma^2)]; L=N/2 log(2 pi sigma^2)+||y-Phi theta||^2/(2 sigma^2). Current solve and verify read directly and agree; Conditional IID Gaussian model, likelihood/NLL/risk scaling, normal equations, rank uniqueness and parameter-linearity agree. Reference differentiates explicitly defined SSE Q; blind result additionally gives Rhat gradient scaled by1/N; actual(d)asks squared-error gradient and both yield same normal equations.
- p6:c: **pass / consistent** — L and squared-loss empirical risk have exactly the same minimizing theta. Current solve and verify read directly and agree; Conditional IID Gaussian model, likelihood/NLL/risk scaling, normal equations, rank uniqueness and parameter-linearity agree. Reference differentiates explicitly defined SSE Q; blind result additionally gives Rhat gradient scaled by1/N; actual(d)asks squared-error gradient and both yield same normal equations.
- p6:d: **pass / consistent** — Phi^T Phi theta=Phi^T y; gradient Rhat=(2/N)(Phi^T Phi theta-Phi^T y). Current solve and verify read directly and agree; Conditional IID Gaussian model, likelihood/NLL/risk scaling, normal equations, rank uniqueness and parameter-linearity agree. Reference differentiates explicitly defined SSE Q; blind result additionally gives Rhat gradient scaled by1/N; actual(d)asks squared-error gradient and both yield same normal equations.
- p6:e: **pass / consistent** — Unique ML minimum (Phi^T Phi)^-1 Phi^T y. Polynomial features still define linear regression in parameters; the new design must separately have full column rank to ensure uniqueness. Current solve and verify read directly and agree; Conditional IID Gaussian model, likelihood/NLL/risk scaling, normal equations, rank uniqueness and parameter-linearity agree. Reference differentiates explicitly defined SSE Q; blind result additionally gives Rhat gradient scaled by1/N; actual(d)asks squared-error gradient and both yield same normal equations.

**p7** — Source: Theory-groundednewderivationusingMML9.2.3–9.2.4 PDF307–309,withnonzeropriormeanextension madeexplicitinconditions.
Content (all seven sections): Recall/start selectposteriorquadratic andλ=σ²/τ². Solve/verify derivecentertermλm0,proveSPDwithoutcolumnrank andsolve(5/11,5/11); λ0nonuniqueness andinfinite-penaltylimit0areconditions-specific. Pitfall/sum retainthoseconditions andno-guaranteedgeneralization.
- p7:a: **pass / consistent** — Posterior is proportional to likelihood times prior; evidence is independent of theta. Current solve and verify read directly and agree; Bayes/evidence independence, NLL, nonzero prior-mean RHS, lambda scaling/SPD uniqueness and dependent-column numerical case agree exactly.
- p7:b: **pass / consistent** — Negative log posterior = ||y-Phi theta||^2/(2 sigma^2)+||theta-m0||^2/(2 tau^2)+C. Current solve and verify read directly and agree; Bayes/evidence independence, NLL, nonzero prior-mean RHS, lambda scaling/SPD uniqueness and dependent-column numerical case agree exactly.
- p7:c: **pass / consistent** — (Phi^T Phi+lambda I_K)theta=Phi^T y+lambda m0. Current solve and verify read directly and agree; Bayes/evidence independence, NLL, nonzero prior-mean RHS, lambda scaling/SPD uniqueness and dependent-column numerical case agree exactly.
- p7:d: **pass / consistent** — MAP formula above with relative penalty lambda=sigma^2/tau^2. Current solve and verify read directly and agree; Bayes/evidence independence, NLL, nonzero prior-mean RHS, lambda scaling/SPD uniqueness and dependent-column numerical case agree exactly.
- p7:e: **pass / consistent** — The coefficient matrix is positive definite, hence invertible, regardless of column dependence; MAP is unique. Current solve and verify read directly and agree; Bayes/evidence independence, NLL, nonzero prior-mean RHS, lambda scaling/SPD uniqueness and dependent-column numerical case agree exactly.
- p7:f: **pass / consistent** — lambda=1: theta=(5/11,5/11)^T. lambda=0: infinitely many solutions (a,1-a)^T. As lambda tends to infinity theta tends to (0,0)^T=m0. Current solve and verify read directly and agree; Bayes/evidence independence, NLL, nonzero prior-mean RHS, lambda scaling/SPD uniqueness and dependent-column numerical case agree exactly.

**p8** — Source: Theory-groundednewscalarposterior/predictiveproblemusingMMLPDF312,314–315; currentprior1,variance2,andtwoobservationsarecustom.
Content (all seven sections): Recall/start identifyprecisionaddition andlikelihood×prior. Solve/verifyderiveA=b=3/2,c=5/2,normalizedposteriorN(1,2/3),latentN(2,8/3),observedN(2,14/3),pluginN(2,2); pitfall/sum keepindependentfuture-noise andvariance-scalingbyx².
- p8:a: **pass / consistent** — Product is (4 pi)^(-3/2) exp[-((2-theta)^2+theta^2+(theta-1)^2)/4]. Current solve and verify read directly and agree; Product kernel/complete square, normalizedposterior, function/observation predictive variances and MAPplug-in missinguncertainty agree; independent also writes product leadingconstant explicitly.
- p8:b: **pass / consistent** — A=3/2, b=3/2, c=5/2. Current solve and verify read directly and agree; Product kernel/complete square, normalizedposterior, function/observation predictive variances and MAPplug-in missinguncertainty agree; independent also writes product leadingconstant explicitly.
- p8:c: **pass / consistent** — theta|D ~ N(1,2/3), with density sqrt(3/(4 pi)) exp[-3(theta-1)^2/4]. Current solve and verify read directly and agree; Product kernel/complete square, normalizedposterior, function/observation predictive variances and MAPplug-in missinguncertainty agree; independent also writes product leadingconstant explicitly.
- p8:d: **pass / consistent** — f*|D ~ N(2,8/3). Current solve and verify read directly and agree; Product kernel/complete square, normalizedposterior, function/observation predictive variances and MAPplug-in missinguncertainty agree; independent also writes product leadingconstant explicitly.
- p8:e: **pass / consistent** — y*|D ~ N(2,14/3). Current solve and verify read directly and agree; Product kernel/complete square, normalizedposterior, function/observation predictive variances and MAPplug-in missinguncertainty agree; independent also writes product leadingconstant explicitly.
- p8:f: **pass / consistent** — theta_MAP=1; plug-in y* ~ N(2,2). Full posterior prediction has additional variance 8/3 from uncertain theta propagated through x*=2. Current solve and verify read directly and agree; Product kernel/complete square, normalizedposterior, function/observation predictive variances and MAPplug-in missinguncertainty agree; independent also writes product leadingconstant explicitly.

**p9** — Source: Theory-groundednewevidence/model-choiceproblemusingMMLPDF312/318–319 andLecture4rev17; custommodelpriorodds1/2andobservation0.
Content (all seven sections): Recall/start distinguishprioraveraging/evidencefromposteriorprediction. Solve/verify integratewithconstants, getevidences1/√(4π),1/√(10π),BF√(5/2),posteriorprobability.44152; pitfall/sum distinguishdatafavorM1fromfinalM2choiceafterprior.
- p9:a: **pass / consistent** — Evidence integral uses the prior, not posterior. Current solve and verify read directly and agree; Prior-weighted evidence integral and normalization, model-density values/Bayesfactor and distinct prior-weightedposterior odds/probability agree; algebraicallyequivalent sqrt expressions both give0.441518... andchooseM2.
- p9:b: **pass / consistent** — p(y|M_j)=[2 pi(v_j+1)]^(-1/2) exp[-y^2/(2(v_j+1))]; normalized N(0,v_j+1). Current solve and verify read directly and agree; Prior-weighted evidence integral and normalization, model-density values/Bayesfactor and distinct prior-weightedposterior odds/probability agree; algebraicallyequivalent sqrt expressions both give0.441518... andchooseM2.
- p9:c: **pass / consistent** — p(0|M1)=1/sqrt(4 pi); p(0|M2)=1/sqrt(10 pi). Current solve and verify read directly and agree; Prior-weighted evidence integral and normalization, model-density values/Bayesfactor and distinct prior-weightedposterior odds/probability agree; algebraicallyequivalent sqrt expressions both give0.441518... andchooseM2.
- p9:d: **pass / consistent** — Data evidence favors M1. Current solve and verify read directly and agree; Prior-weighted evidence integral and normalization, model-density values/Bayesfactor and distinct prior-weightedposterior odds/probability agree; algebraicallyequivalent sqrt expressions both give0.441518... andchooseM2.
- p9:e: **pass / consistent** — P(M1|0)=sqrt(5)/(sqrt(5)+2sqrt(2)); choose M2 by larger posterior despite B12>1. Current solve and verify read directly and agree; Prior-weighted evidence integral and normalization, model-density values/Bayesfactor and distinct prior-weightedposterior odds/probability agree; algebraicallyequivalent sqrt expressions both give0.441518... andchooseM2.

**p10** — Source: Theory-groundednewprojection/least-squaresderivationusingMML3.8/9.4 PDF87–89,319–320 andLecture4rev23; numericPhi,ycustom.
Content (all seven sections): Recall/start choosevariationinallcoefficientdirections. Solve/verify deriveΦᵀr=0,rankcondition,Pdimensions/symmetry/idempotence,allnumericoutputsandPythagoreanminimum proof. Pitfall/sum distinguishNxNprojectorfromKxNestimatormap.
- p10:a: **pass / consistent** — Phi^T r=0, so r is orthogonal to every vector in col(Phi). Current solve and verify read directly and agree; Stationarityviaarbitrarydirection, normal equations/full-rankinverse, symmetricidempotentprojector, numericalP/prediction/residual andorthogonaldistance uniquenessproof agree exactly.
- p10:b: **pass / consistent** — Phi^T Phi thetahat=Phi^T y; thetahat=(Phi^T Phi)^-1 Phi^T y. Current solve and verify read directly and agree; Stationarityviaarbitrarydirection, normal equations/full-rankinverse, symmetricidempotentprojector, numericalP/prediction/residual andorthogonaldistance uniquenessproof agree exactly.
- p10:c: **pass / consistent** — P is symmetric and idempotent, the orthogonal projector onto col(Phi). Current solve and verify read directly and agree; Stationarityviaarbitrarydirection, normal equations/full-rankinverse, symmetricidempotentprojector, numericalP/prediction/residual andorthogonaldistance uniquenessproof agree exactly.
- p10:d: **pass / consistent** — P=[[1/3,1/3,1/3],[1/3,5/6,-1/6],[1/3,-1/6,5/6]]; yhat=(4/3,7/3,1/3)^T; r=(2/3,-1/3,-1/3)^T. Current solve and verify read directly and agree; Stationarityviaarbitrarydirection, normal equations/full-rankinverse, symmetricidempotentprojector, numericalP/prediction/residual andorthogonaldistance uniquenessproof agree exactly.
- p10:e: **pass / consistent** — Distance is at least ||r||^2, with equality only for u=yhat. Thus yhat is the unique closest point. Current solve and verify read directly and agree; Stationarityviaarbitrarydirection, normal equations/full-rankinverse, symmetricidempotentprojector, numericalP/prediction/residual andorthogonaldistance uniquenessproof agree exactly.

Course-produced PDFs: existing problem/answer bytes verified against current PDF-reuse equivalence record; no new render or regeneration claimed.

### exam-0909-1019-Midterm_Practice_02

- Current HTML SHA256: `4e9efd72adabc607ef210fdece5e7eaece7e9b5e3b741e10a5a08dd7d1f15eac`
- Current source SHA256: `a649d7234cc2bdb30596a7f3768a1353ec3783c3830e75a2480b595213c7963b`
- Manifest SHA256: `e078eaf9c6f6d8f55c34c074605148d6e155348173c6fe88d123927b77991f0d`
- Source visual: pass (fresh authentic source PDF visual and current-card comparison). Content: pass.

**p1** — Source: HW1P6–8 PDF3 inspires newparameter-dependentbasisproblem,notoriginalnumericexercise.
Content (all seven sections): Recall/start linkdeterminant,spanandcolumnspace. Solve/verify givest−2,t≠2basis,t2general family/no-solutionRHSandt3unique(0,1,1); pitfall/sum avoidall-RHS-inconsistencyinferencefromsingularity.
- p1:a: **pass / consistent** — det V(t)=t-2; the columns are a basis of R^3 exactly when t != 2. Current solve and verify read directly and agree; Determinant/basiscase, affinefamilies, inconsistentRHSanduniqueexpandedcolumnspace solutionagree; independentrowoperation and referencecolumnoperation bothvalid.
- p1:b: **pass / consistent** — All solutions for (1,2,3)^T are (1-s,2-s,s)^T, s real; none for (1,2,4)^T. Current solve and verify read directly and agree; Determinant/basiscase, affinefamilies, inconsistentRHSanduniqueexpandedcolumnspace solutionagree; independentrowoperation and referencecolumnoperation bothvalid.
- p1:c: **pass / consistent** — Unique solution alpha=(0,1,1)^T; changing t expands the column space from a plane to all R^3. Current solve and verify read directly and agree; Determinant/basiscase, affinefamilies, inconsistentRHSanduniqueexpandedcolumnspace solutionagree; independentrowoperation and referencecolumnoperation bothvalid.

**p2** — Source: HW1P10–12 PDF3–4 inspire newcomposition/directionalderivativeproblem; currentdefinitionkeepsdunnormalized.
Content (all seven sections): Recall/start chainruleusesJᵀforcolumngradient. Solve/verify comparedirectderivative(2,2)withchainruleandD_d=0,thenrejectstationarysincegradientnonzero; pitfall/sum preservedirectiondefinition andall-directionscriterion.
- p2:a: **pass / consistent** — J_f(x)=[[1,1],[x2,x1]], J_f(1,2)=[[1,1],[2,1]], dimension 2x2. Current solve and verify read directly and agree; General/pointJacobian, chain/directcolumn gradientsandzero-on-one-directionbutnonstationarity reasoningagree.
- p2:b: **pass / consistent** — gradient_x L(1,2)=(2,2)^T by both derivations. Current solve and verify read directly and agree; General/pointJacobian, chain/directcolumn gradientsandzero-on-one-directionbutnonstationarity reasoningagree.
- p2:c: **pass / consistent** — D_d L=0, but (1,2)^T is not stationary; derivative along (1,1)^T is 4. Current solve and verify read directly and agree; General/pointJacobian, chain/directcolumn gradientsandzero-on-one-directionbutnonstationarity reasoningagree.

**p3** — Source: HW1P13/P22 PDF4/8 inspire newA,bwithsamevalidjointGaussianinput; nogivensfromoriginalfiguresrequired.
Content (all seven sections): Recall/start selectaffinemoments/jointGaussianfactorization. Solve/verify yieldmean(0,4),covdiag(6,2),normalizedjointdensity1/(4π√3),independentYbutdependentX; pitfall/sum preservejointGaussiancondition.
- p3:a: **pass / consistent** — E[Y]=(0,4)^T; Cov(Y)=diag(6,2). Current solve and verify read directly and agree; AffineGaussian mean/covariance, determinantnormalizationandmarginals, YindependencevsoriginalXdependence agree.
- p3:b: **pass / consistent** — Y1~N(0,6), Y2~N(4,2); p_Y=1/(4 pi sqrt(3))*exp[-y1^2/12-(y2-4)^2/4]. Current solve and verify read directly and agree; AffineGaussian mean/covariance, determinantnormalizationandmarginals, YindependencevsoriginalXdependence agree.
- p3:c: **pass / consistent** — Y1,Y2 are independent. X1,X2 are dependent. The Gaussian property makes zero cross covariance sufficient for Y independence. Current solve and verify read directly and agree; AffineGaussian mean/covariance, determinantnormalizationandmarginals, YindependencevsoriginalXdependence agree.

**p4** — Source: HW1P14/P25 PDF5/9 inspire scalarpriorlikelihoodproductwithprior−1,variance2 andobserved3.
Content (all seven sections): Recall/start retainfrontfactor1/(4π)andcomplete-squareconstant4. Solve/verify giveposteriorN(1,1),ML3,MAP1,Z=e^(−2)/√(8π); pitfall/sum distinguishobserveddensityvaluefromposteriorfunction.
- p4:a: **pass / consistent** — g(theta)=1/(4 pi)*exp[-(theta-1)^2/2-2]. Current solve and verify read directly and agree; Productkernelconstant, normalizedposterior/ML/MAPdistinctionandevidence value agreeexactly; evidence isobserveddensitynotposteriorfunction.
- p4:b: **pass / consistent** — theta|y=3~N(1,1); density (2 pi)^-1/2 exp[-(theta-1)^2/2]; ML=3, MAP=1. Current solve and verify read directly and agree; Productkernelconstant, normalizedposterior/ML/MAPdistinctionandevidence value agreeexactly; evidence isobserveddensitynotposteriorfunction.
- p4:c: **pass / consistent** — Z=exp(-2)/sqrt(8 pi), the evidence density value for y=3; it is not the posterior density function of theta. Current solve and verify read directly and agree; Productkernelconstant, normalizedposterior/ML/MAPdistinctionandevidence value agreeexactly; evidence isobserveddensitynotposteriorfunction.

**p5** — Source: HW1P9/P17–19 PDF3/6 inspire customfeature(1,x²),y=(2,0,4),unitnoise/priorforallcoefficients.
Content (all seven sections): Recall/start distinguishduplicaterowsfromdependentcolumns. Solve/verify getG[[3,2],[2,2]],det2,ML(0,3),SSE2,prediction12,MAP(.75,1.5),prediction27/4; pitfall/sum keepφ(2)=(1,4)andparameterlinearity.
- p5:a: **pass / consistent** — Phi=[[1,1],[1,0],[1,1]], G=[[3,2],[2,2]], Phi^T y=(6,6)^T; Gram is invertible. Current solve and verify read directly and agree; Feature Gram [[3,2],[2,2]], determinant2; ML(0,3), SSE2, prediction12; MAP(3/4,3/2), prediction27/4. Actual equations, residual normal conditions and fixed-feature linearity agree.
- p5:b: **pass / consistent** — theta_ML=(0,3)^T; residual=(-1,0,1)^T; SSE=2; predicted mean at x*=2 is 12. Current solve and verify read directly and agree; Feature Gram [[3,2],[2,2]], determinant2; ML(0,3), SSE2, prediction12; MAP(3/4,3/2), prediction27/4. Actual equations, residual normal conditions and fixed-feature linearity agree.
- p5:c: **pass / consistent** — theta_MAP=(3/4,3/2)^T; predicted mean 27/4. It is linear regression in coefficients despite nonlinear dependence on input x. Current solve and verify read directly and agree; Feature Gram [[3,2],[2,2]], determinant2; ML(0,3), SSE2, prediction12; MAP(3/4,3/2), prediction27/4. Actual equations, residual normal conditions and fixed-feature linearity agree.

**p6** — Source: Theory-groundednewknown-variance scalarML/projectionderivationusingMML9.2/9.4 PDF298–300/319–320,customx,y.
Content (all seven sections): Recall/start buildindependentGaussianlikelihood. Solve/verifyderiveNLLconstants,positiveΣx²curvature,θ=(xᵀy)/(xᵀx),P=xxᵀ/(xᵀx),residualorthogonality,numeric7/6andSSE11/6. Pitfall/sum distinguishscalarcoefficientfromNdatavector andinnerfromouterproduct.
- p6:a: **pass / consistent** — p(y|x,theta)=(2 pi sigma^2)^(-N/2)exp[-sum_n(y_n-theta x_n)^2/(2 sigma^2)]. Current solve and verify read directly and agree; Known positive variance and nonzero input norm justify likelihood/SSE equivalence, unique scalar estimator and orthogonal projection. Concrete x norm6, xy7, estimator7/6, residual and SSE11/6 match.
- p6:b: **pass / consistent** — ML is equivalent to minimizing SSE(theta)=sum_n(y_n-theta x_n)^2. Current solve and verify read directly and agree; Known positive variance and nonzero input norm justify likelihood/SSE equivalence, unique scalar estimator and orthogonal projection. Concrete x norm6, xy7, estimator7/6, residual and SSE11/6 match.
- p6:c: **pass / consistent** — thetahat=(sum x_n y_n)/(sum x_n^2); positive denominator is guaranteed by the stated assumption. Current solve and verify read directly and agree; Known positive variance and nonzero input norm justify likelihood/SSE equivalence, unique scalar estimator and orthogonal projection. Concrete x norm6, xy7, estimator7/6, residual and SSE11/6 match.
- p6:d: **pass / consistent** — thetahat=(x^T y)/(x^T x), unique global ML minimum. Current solve and verify read directly and agree; Known positive variance and nonzero input norm justify likelihood/SSE equivalence, unique scalar estimator and orthogonal projection. Concrete x norm6, xy7, estimator7/6, residual and SSE11/6 match.
- p6:e: **pass / consistent** — P=xx^T/(x^T x); residual is orthogonal to x. Current solve and verify read directly and agree; Known positive variance and nonzero input norm justify likelihood/SSE equivalence, unique scalar estimator and orthogonal projection. Concrete x norm6, xy7, estimator7/6, residual and SSE11/6 match.
- p6:f: **pass / consistent** — thetahat=7/6, yhat=(7/6,7/3,-7/6)^T, SSE=11/6; P=(1/6)[[1,2,-1],[2,4,-2],[-1,-2,1]]. Current solve and verify read directly and agree; Known positive variance and nonzero input norm justify likelihood/SSE equivalence, unique scalar estimator and orthogonal projection. Concrete x norm6, xy7, estimator7/6, residual and SSE11/6 match.

**p7** — Source: Theory-groundednewgeneralGaussian-priorMAPderivationusingMMLPDF307–309/312; diagonalpriorS0andnonzerom0areexplicitcustomconditions.
Content (all seven sections): Recall/start selectprecisionS0⁻¹. Solve/verify retaincenterterm, deriveB=G/σ²+S0⁻¹,proveSPDUniqueness,getMAP(2,4/3),prediction14/3,andcomponentfunctions(2,4/(2+σ²))withlimits. Pitfall/sum keepinversevariance andproperprior.
- p7:a: **pass / consistent** — Negative log posterior=C+||y-Phi theta||^2/(2 sigma^2)+(theta-m0)^T S0^-1(theta-m0)/2; C=log(2 pi sigma^2)+log(2 pi)+(1/2)log det S0+log p(y|Phi). Current solve and verify read directly and agree; Nonzero-mean anisotropic prior precision is retained. Gradients and SPD Hessian give the same scaled/unscaled system; MAP(2,4/3), prediction14/3, ML(2,2), and noise-variance limits agree.
- p7:b: **pass / consistent** — The two column gradients are Phi^T(Phi theta-y)/sigma^2 and S0^-1(theta-m0). Current solve and verify read directly and agree; Nonzero-mean anisotropic prior precision is retained. Gradients and SPD Hessian give the same scaled/unscaled system; MAP(2,4/3), prediction14/3, ML(2,2), and noise-variance limits agree.
- p7:c: **pass / consistent** — theta_MAP=(Phi^T Phi+sigma^2 S0^-1)^-1(Phi^T y+sigma^2 S0^-1 m0). Current solve and verify read directly and agree; Nonzero-mean anisotropic prior precision is retained. Gradients and SPD Hessian give the same scaled/unscaled system; MAP(2,4/3), prediction14/3, ML(2,2), and noise-variance limits agree.
- p7:d: **pass / consistent** — Coefficient matrix is positive definite and MAP is the unique global posterior mode. Current solve and verify read directly and agree; Nonzero-mean anisotropic prior precision is retained. Gradients and SPD Hessian give the same scaled/unscaled system; MAP(2,4/3), prediction14/3, ML(2,2), and noise-variance limits agree.
- p7:e: **pass / consistent** — MAP=(2,4/3)^T, prediction 14/3; ML=(2,2)^T, prediction 6. Current solve and verify read directly and agree; Nonzero-mean anisotropic prior precision is retained. Gradients and SPD Hessian give the same scaled/unscaled system; MAP(2,4/3), prediction14/3, ML(2,2), and noise-variance limits agree.
- p7:f: **pass / consistent** — theta_MAP(s)=(2,4/(2+s))^T; limits are ML at zero noise and prior mean at infinite noise. Current solve and verify read directly and agree; Nonzero-mean anisotropic prior precision is retained. Gradients and SPD Hessian give the same scaled/unscaled system; MAP(2,4/3), prediction14/3, ML(2,2), and noise-variance limits agree.

**p8** — Source: Theory-groundednew2Dposteriorandshared-futureobservationsproblemusingMMLPDF198/312/314–315; future-noiseindependenceisexplicit.
Content (all seven sections): Recall/start chooseposteriorprecisionquadratic. Solve/verify giveB2I,b(1,1),c2,m(.5,.5),SI/2,normalizer1/π,latentN(1,1),observedN(1,3),pluginN(1,2),futurecrosscov.5. Pitfall/sum explicitlyrejectmarginalindependenceafterintegratingcommontheta.
- p8:a: **pass / consistent** — B=I+(1/2)Phi^T Phi, b=(1/2)Phi^T y, c=(1/2)y^T y. Current solve and verify read directly and agree; Completing-square coefficients B=2I,b=(1,1),c=2 and normalized posterior mean(.5,.5), covariance .5I agree. Latent variance1, observation variance3 vs plug-in2, shared-parameter crosscovariance.5 all match with independent fresh noise.
- p8:b: **pass / consistent** — Posterior N(m,S) has density [2 pi sqrt(det S)]^-1 exp[-(theta-m)^T S^-1(theta-m)/2]. Current solve and verify read directly and agree; Completing-square coefficients B=2I,b=(1,1),c=2 and normalized posterior mean(.5,.5), covariance .5I agree. Latent variance1, observation variance3 vs plug-in2, shared-parameter crosscovariance.5 all match with independent fresh noise.
- p8:c: **pass / consistent** — theta|y~N((1/2,1/2)^T,(1/2)I), density (1/pi)exp[-||theta-(1/2,1/2)^T||^2]. Current solve and verify read directly and agree; Completing-square coefficients B=2I,b=(1,1),c=2 and normalized posterior mean(.5,.5), covariance .5I agree. Latent variance1, observation variance3 vs plug-in2, shared-parameter crosscovariance.5 all match with independent fresh noise.
- p8:d: **pass / consistent** — f_*|y~N(phi_*^T m,phi_*^T S phi_*); at x*=1 this is N(1,1). Current solve and verify read directly and agree; Completing-square coefficients B=2I,b=(1,1),c=2 and normalized posterior mean(.5,.5), covariance .5I agree. Latent variance1, observation variance3 vs plug-in2, shared-parameter crosscovariance.5 all match with independent fresh noise.
- p8:e: **pass / consistent** — y_*|y~N(phi_*^T m,2+phi_*^T S phi_*); at x*=1 N(1,3), versus MAP plug-in N(1,2). Current solve and verify read directly and agree; Completing-square coefficients B=2I,b=(1,1),c=2 and normalized posterior mean(.5,.5), covariance .5I agree. Latent variance1, observation variance3 vs plug-in2, shared-parameter crosscovariance.5 all match with independent fresh noise.
- p8:f: **pass / consistent** — Cross covariance is 1/2; joint posterior predictive covariance [[5/2,1/2],[1/2,3]]. The future observations are dependent after theta is integrated out, although independent given theta. Current solve and verify read directly and agree; Completing-square coefficients B=2I,b=(1,1),c=2 and normalized posterior mean(.5,.5), covariance .5I agree. Latent variance1, observation variance3 vs plug-in2, shared-parameter crosscovariance.5 all match with independent fresh noise.

**p9** — Source: Theory-groundednewsharedversusseparatemodel-evidenceproblemusingMMLPDF205–206/312/317–319 andLecture4rev17; modelspaceandpriorodds3explicit.
Content (all seven sections): Recall/start constructB1columnones,B2I. Solve/verify showcov[[2,1],[1,2]]versus2I, normalizedevidencese^(−1)/(2π√3),e^(−.5)/(4π),BF.70036,posterior.67753; pitfall/sum keepmodelpriorodds andsharedparametercovariance.
- p9:a: **pass / consistent** — B1=[[1],[1]], B2=I2; evidence is the likelihood integrated over the respective independent Gaussian parameter priors. Current solve and verify read directly and agree; Integrated model covariances [[2,1],[1,2]] and2I, determinants3/4 and quadratic forms2/1 give matching normalized evidences. Bayes factor2exp(-.5)/sqrt3 and prior-adjusted posterior odds/probability agree; density and posterior model probability are distinguished.
- p9:b: **pass / consistent** — M1: y~N(0,[[2,1],[1,2]]). M2: y~N(0,2I2). Current solve and verify read directly and agree; Integrated model covariances [[2,1],[1,2]] and2I, determinants3/4 and quadratic forms2/1 give matching normalized evidences. Bayes factor2exp(-.5)/sqrt3 and prior-adjusted posterior odds/probability agree; density and posterior model probability are distinguished.
- p9:c: **pass / consistent** — p(y|M1)=exp(-1)/(2 pi sqrt(3)); p(y|M2)=exp(-1/2)/(4 pi). Current solve and verify read directly and agree; Integrated model covariances [[2,1],[1,2]] and2I, determinants3/4 and quadratic forms2/1 give matching normalized evidences. Bayes factor2exp(-.5)/sqrt3 and prior-adjusted posterior odds/probability agree; density and posterior model probability are distinguished.
- p9:d: **pass / consistent** — B12=2 exp(-1/2)/sqrt(3); data evidence favors M2. Current solve and verify read directly and agree; Integrated model covariances [[2,1],[1,2]] and2I, determinants3/4 and quadratic forms2/1 give matching normalized evidences. Bayes factor2exp(-.5)/sqrt3 and prior-adjusted posterior odds/probability agree; density and posterior model probability are distinguished.
- p9:e: **pass / consistent** — P(M1|y)=2sqrt(3)/(sqrt(e)+2sqrt(3)); choose M1 by larger posterior, since its prior odds outweigh the evidence preference for M2. Current solve and verify read directly and agree; Integrated model covariances [[2,1],[1,2]] and2I, determinants3/4 and quadratic forms2/1 give matching normalized evidences. Bayes factor2exp(-.5)/sqrt3 and prior-adjusted posterior odds/probability agree; density and posterior model probability are distinguished.

**p10** — Source: Theory-groundednewleast-squaresversusridgecomparisonusingMML3.8/9.4 PDF87–89/319–320 andridgePDF307–309;lambda1forallcoefficients.
Content (all seven sections): Recall/start derivefull-rankleast-squaresnormal equations. Solve/verify giveML(0,1),SSE3,P,symmetric/idempotentproof,ridge(1/8,5/8),H,residualΦᵀr_R=θ_R,andHv=.75vversusH²v=.5625v. Pitfall/sum preservesymmetry-insufficiency anddistinguishcolumnspacefromnearestpoint.
- p10:a: **pass / consistent** — Normal equations G thetahat=Phi^T y. Current solve and verify read directly and agree; Gram [[2,1],[1,2]] gives OLS(0,1), residual(1,1,-1), exact symmetric idempotent projector. Ridge(1/8,5/8), nonorthogonal residual and H eigenvalue3/4 versus squared9/16 match, proving symmetry alone insufficient.
- p10:b: **pass / consistent** — Unique thetahat=(0,1)^T; yhat=(0,1,1)^T; r=(1,1,-1)^T. Current solve and verify read directly and agree; Gram [[2,1],[1,2]] gives OLS(0,1), residual(1,1,-1), exact symmetric idempotent projector. Ridge(1/8,5/8), nonorthogonal residual and H eigenvalue3/4 versus squared9/16 match, proving symmetry alone insufficient.
- p10:c: **pass / consistent** — P is the stated symmetric idempotent orthogonal projector; Py=yhat. Current solve and verify read directly and agree; Gram [[2,1],[1,2]] gives OLS(0,1), residual(1,1,-1), exact symmetric idempotent projector. Ridge(1/8,5/8), nonorthogonal residual and H eigenvalue3/4 versus squared9/16 match, proving symmetry alone insufficient.
- p10:d: **pass / consistent** — theta_R=(1/8,5/8)^T, versus ordinary least squares (0,1)^T. Current solve and verify read directly and agree; Gram [[2,1],[1,2]] gives OLS(0,1), residual(1,1,-1), exact symmetric idempotent projector. Ridge(1/8,5/8), nonorthogonal residual and H eigenvalue3/4 versus squared9/16 match, proving symmetry alone insufficient.
- p10:e: **pass / consistent** — H is the stated matrix. Ridge residual is not orthogonal to col(Phi) here; Phi^T r_R=theta_R != 0, whereas ordinary least squares has Phi^T r=0. Current solve and verify read directly and agree; Gram [[2,1],[1,2]] gives OLS(0,1), residual(1,1,-1), exact symmetric idempotent projector. Ridge(1/8,5/8), nonorthogonal residual and H eigenvalue3/4 versus squared9/16 match, proving symmetry alone insufficient.
- p10:f: **pass / consistent** — H is not an orthogonal projection. Symmetry alone is insufficient: an orthogonal projector must also be idempotent. Current solve and verify read directly and agree; Gram [[2,1],[1,2]] gives OLS(0,1), residual(1,1,-1), exact symmetric idempotent projector. Ridge(1/8,5/8), nonorthogonal residual and H eigenvalue3/4 versus squared9/16 match, proving symmetry alone insufficient.

Course-produced PDFs: existing problem/answer bytes verified against current PDF-reuse equivalence record; no new render or regeneration claimed.

## Exact evidence files

- `results.json`:54questionsection-bindings and151subpartresults; currentHTML/source/manifest/fragmentSHA256 andallcurrentreferencehashes.
- `source-page-bindings.json` and `extra-source-page-bindings.json`:53freshauthenticpages,PDFandPNG SHA256. Contactsheet images were opened/read in this review; eachindividualPNG is preserved.
- `source-pages/current-1007-p3-figure.svg/png`: isolated current schematic geometry/text, with display stroke/color overrides and white background for inspection; not an original textbook image or product edit.
- Reused1019sourcevisual retains its originalreviewer and3PNGs, with exactmatchingcurrentquestionpayload.
- Existingdated/examcontrollercomparisons are cited as corroboration, with their currenthashes; none is represented as thisreviewersblindwork.

No product files, approvals, commits or course PDFs were written. Current content includes seven explanation sections plus a separate summary; retry is included in the section bindings.
