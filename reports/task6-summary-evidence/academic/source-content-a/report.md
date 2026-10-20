# Current academic source/content review A

Reviewed 6 packs / 39 questions / 62 subparts; 27 actual local MML pages rendered and visually inspected.

This is a source/content review, not a code review or blind derivation. I read current source cards and explanations, then used the disclosed frozen controller-reference comparison as supplementary mathematical evidence. No product file, release approval, commit, or independent-review record was changed.

Verdicts: {'consistent': 48, 'qualified_consistent': 14}. Every qualified_consistent item below retains its assumptions; pass means consistent under those conditions, not unconditional approval.

## Exact binding

Detailed section HTML/text and source fields: `current-read-evidence.json`, SHA256 `29970ef14cd492f6314067e3058f3cf52b97b34b17944a2390ba12f9af41d63d`. `results.json` carries per-pack live HTML/source/manifest/MML hashes, per-question source_visual comparisons and page-image hashes, and all 62 per-subpart content records with seven section hashes. Figures are normalized only for scoped SVG IDs before geometry comparison.

## Limits

- No browser-layout, navigation, grading, or runtime release approval is given by this academic role. Graph-only captures are source figure evidence, not full page/browser validation.
- Dated explanation HTML has no inline data-original-problem/original tabs in either current or pre-change version. Original textbook excerpts remain in source cards accessible via the preserved 원 문제 보기 link; this role read those actual source excerpts.
- Source MML is the local Draft2024-01-15 PDF displayed in the page footer; textbook examples and current adapted numerical cards are deliberately distinguished.
- Qualified items remain conditional; mathematical consistency within stated assumptions is not an unconditional product approval.

0916/p1 current recall explicitly states fixed positive definite covariance and theta-only optimization. Supplementary comparison disclosure labels describing only solve/verify/pitfall are retained as historical comparison scope, not as a claim that the full seven-section body lacks this statement. Conditional covariance-domain approval remains in place.

## 0909 / review-0909-Data_Models_Learning

- Current source SHA256: `cd7d82ac470f2c9dde48a4c61a87c340336fa3fc96175ca4587c2c4163ca4ae5`
- Current explanation HTML SHA256: `3ebe3e26d61c21dd63066ad07bcb8e11cb11dae0582ad4ab53ee340fc7dba156`
- MML SHA256: `3f87b70c64a35d30ec4e565b4d5cfd18fe913002d3b3bed44691c7d0838911bc`
- source_visual: pass. content: pass with item qualifications. {'consistent': 6, 'qualified_consistent': 1}

### p1 source and figure comparison

Example9.1 is the real scalar theta x model. Current theta=-1,1/2,2 and x=10 are adapted practice values, not claims about book figure coordinates. Pages: 297. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `855efd5b27319f63cad6ac5c649068b17890d8e4c7c0664c6312d93d605400ec`.

- **p1:a: consistent** — At x=10 the three products are -10,5,20; division by the nonzero input restores the three slopes.
  Retained qualification: None
- **p1:b: qualified_consistent** — Absolute slopes are 1,1/2,2, so theta=2 is steepest. Retained signed-slope shorthand is valid only with the explicit absolute-value correction in solve/verify/pitfall/sum.
  Retained qualification: Signed-slope shorthand in retained answer is restricted by explicit absolute-value warning.
### p2 source and figure comparison

Exercise2.4(a) matrices visually match the card, including 3x2 then 3x3 dimensions. Pages: 70, 71. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `536509c909a6a20bc9e9029b9736ee42cbb79214f55794418a85fd7d97b88e15`.

- **p2:main: consistent** — A is 3x2 and B is 3x3: inner dimensions 2 and 3 do not match, so the product is undefined, not zero.
  Retained qualification: None
### p3 source and figure comparison

Exercise2.4(b,c) matrix entries and order visually match; card subparts deliberately retain book labels b,c. Pages: 70, 71. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `5b1cd71457626e46114be22693c83908350c409ffe2f145afff104cf70a7a374`.

- **p3:b: consistent** — For AB, columns are sums of the selected columns of A: rows [4,3,5],[10,9,11],[16,15,17]. Every column-major TeX entry matches these rows.
  Retained qualification: None
- **p3:c: consistent** — For BA, selected row sums give [5,7,9],[11,13,15],[8,10,12]. Same shape does not imply AB=BA.
  Retained qualification: None
### p4 source and figure comparison

Exercise2.4(d) 2x4 and 4x2 matrices including -1,-4 entries visually match. Pages: 70, 71. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `d571346cbc156275cbe5b94e893bd2543449d6555e55e3ac45c3d1ce421aac16`.

- **p4:main: consistent** — (2x4)(4x2) gives 2x2. Four row-column sums give [14,6],[-21,2]; last entry 12-1-1-8=2 checks the negative signs.
  Retained qualification: None
### p5 source and figure comparison

Exercise2.4(e) is the reversed rectangular product, visually matched entry by entry. Pages: 70, 71. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `d0be16947cab09bf2b8939157bc059eb0ec97e326c64043a053e9c0bcfbc1e6d`.

- **p5:main: consistent** — (4x2)(2x4) gives 4x4, with rows [12,3,-3,-12],[-3,1,2,6],[6,5,1,0],[13,12,3,2]. This is not a transpose of the previous 2x2 product.
  Retained qualification: None

## 0914 / review-0914-ERM_and_MLE

- Current source SHA256: `21eca2b247d7e4c3da3bde948bebe4425d598a63d223225bdb1815a1fd1bfc0e`
- Current explanation HTML SHA256: `821e45cfc93e3db98e4b799e4c024953cd847b50530afa64d2c066ae05b1a3ba`
- MML SHA256: `3f87b70c64a35d30ec4e565b4d5cfd18fe913002d3b3bed44691c7d0838911bc`
- source_visual: pass. content: pass with item qualifications. {'consistent': 13}

### p1 source and figure comparison

Example8.1 unit-feature convention and D+1 dimensional predictor match; supplied feature/coefficient numbers are current adaptations. Pages: 265. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `eb760b1651f21c58dd72b67359465e4490afa0cd410da46536f41f06620164ec`.

- **p1:a: consistent** — Appending the unit feature to (2,-1) gives [1,2,-1]^T, length D+1=3, matching the coefficient length.
  Retained qualification: None
- **p1:b: consistent** — The ordered inner product is 1/2+6-2=9/2; the affine form produces the same scalar.
  Retained qualification: None
### p2 source and figure comparison

Example8.2 and (8.9) use mean squared Euclidean error; current three points/two candidate vectors are adapted and authoritative. Pages: 266, 267. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `ffc042968dd1c6a89d4b937861df7c9ae4a5d57dec2219f4f116692cb0ead0d4`.

- **p2:a: consistent** — Each data point is one row: X=[[1,0],[1,1],[1,2]], y=[1,4,4]^T; X is 3x2.
  Retained qualification: None
- **p2:b: consistent** — A predicts [1,3,5] with squared residual sum 2; B predicts [3/2,3,9/2] with sum 3/2; division by N=3 gives 2/3 and 1/2.
  Retained qualification: None
- **p2:c: consistent** — B is the better of these candidates because 2/3-1/2=1/6>0. The text correctly avoids asserting that this candidate comparison alone proves a global optimum.
  Retained qualification: None
### p3 source and figure comparison

Example8.3 continues onto269 with N^-1 SSE+lambda||theta||^2. Current candidate values and inclusion of bias follow the displayed current objective. Pages: 268, 269. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `13bf206ad09a9d5e6e76d5e00e1788f18d2661bbb4250c9a64888ad2fc6f684e`.

- **p3:a: consistent** — At lambda=0, A has loss 0 and B 5/3, so A wins.
  Retained qualification: None
- **p3:b: consistent** — Including the bias in the specified penalty gives norms squared 5 and 2: at lambda=1 scores are 5 and 11/3, so B wins. The crossover is lambda=5/9.
  Retained qualification: None
### p4 source and figure comparison

Example8.4 specifies zero-mean independent Gaussian noise and conditional mean x^T theta; current numeric x,theta,sigma^2 are adapted. Pages: 272. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `0b18c81ec244d5ae3b7e4998890cd192a44d46b6b4d27015197ea5766c1b753b`.

- **p4:main: consistent** — Conditioning on fixed x and theta, x^T theta=5 shifts zero-mean noise and leaves its variance 1: the result is N(5,1).
  Retained qualification: None
### p5 source and figure comparison

Example8.5 displays the NLL expansion and fixed-sigma condition; current dataset/candidates remain authoritative. Pages: 273. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `fda80356f59d5353eed8573703108af6cecbef9b5af4a66defcf819ca30692d3`.

- **p5:a: consistent** — For independent common fixed variance Gaussian noise, -log likelihood=SSE/(2 sigma^2)+N log(2 pi sigma^2)/2; sigma^2=1,N=3 gives the constant 3 log(2pi)/2.
  Retained qualification: None
- **p5:b: consistent** — Using SSE 2 and 3/2 gives NLLs 3.7568156... and 3.5068156..., correctly rounded to 3.757 and 3.507.
  Retained qualification: None
- **p5:c: consistent** — A-B=1/4>0; identical positive scale and additive constant preserve SSE candidate ordering, so B wins.
  Retained qualification: None
### p6 source and figure comparison

Exercise3.3(a) vectors [1,2,3],[-1,-1,0] and standard inner product match exactly. Book subpart(b) weighted inner product is intentionally not asked. Pages: 102. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `1e84dfe2006e3b1f3e1c5ea01383440813b2111b560a5fac4dc8a76ef21f1578`.

- **p6:main: consistent** — x-y=[2,3,3]^T; its squared Euclidean norm is 4+9+9=22, so distance is sqrt(22), not 22. Reversing the difference leaves the result unchanged.
  Retained qualification: None
### p7 source and figure comparison

Exercise7.1 polynomial x^3+6x^2-3x-5 and stationary-point classification ask match exactly. Pages: 253. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `ad2c019d340c54e11ee5f8496b1eb804d21d8edb49ba964bbfaade4afe188f1f`.

- **p7:main: consistent** — Derivative 3x^2+12x-3 has roots -2±sqrt5; second derivative at those roots is ±6sqrt5. Thus the minus root is a local maximum, plus root a local minimum; values are 17±10sqrt5. The cubic is unbounded in both directions, so these are not global extrema.
  Retained qualification: None

## 0916 / review-0916-MAP_and_Generative_Models

- Current source SHA256: `85d147a0dc38d0aebc008ee4b67ea073bd82eff7d8bd0f0c7c7fcb4e025fe3a9`
- Current explanation HTML SHA256: `0379051cc5ae9ef41c0479a14a6f06b5c76b365a425710b3017d2c395e3d630c`
- MML SHA256: `3f87b70c64a35d30ec4e565b4d5cfd18fe913002d3b3bed44691c7d0838911bc`
- source_visual: pass. content: pass with item qualifications. {'qualified_consistent': 2, 'consistent': 5}

### p1 source and figure comparison

Example8.6 gives zero-mean multivariate Gaussian prior; actual density formula (6.63) on204 confirms determinant, inverse and half factor. Current density with ordinary inverse requires a nonsingular covariance. Pages: 204, 275. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `724ba10bf9d2e09d2ac1cd5bf74a14e29fd8bd105a75574f626646ac4c103425`.

- **p1:a: qualified_consistent** — Taking the negative log of the explicitly displayed Gaussian prior yields D log(2pi)/2+log|Sigma|/2+theta^T Sigma^-1 theta/2. This ordinary density needs a fixed positive definite covariance; singular covariance does not support this determinant/inverse formula.
  Retained qualification: An ordinary inverse/determinant Gaussian density requires Sigma positive definite. It is mathematically implicit in the displayed source PDF, but the non-summary body does not literally warn about singular covariance.
  Retained unresolved scope: Sigma is called a covariance matrix but positive definiteness is not explicit. For singular covariance the supplied inverse/determinant density is undefined; the displayed result applies to the nondegenerate case.
- **p1:b: qualified_consistent** — Bayes evidence does not depend on theta, so MAP minimizes NLL plus the prior quadratic term. Fixed nonsingular covariance and optimization over theta only are essential; Sigma-dependent constants cannot be dropped when Sigma is optimized.
  Retained qualification: MAP algebra inherits the nonsingular fixed prior covariance; fixing Sigma is disclosed non-summary, positive definiteness is explicit only in summary.
### p2 source and figure comparison

Exercise6.1 table visually checked: y1 top row, columns x1..x5, all15 decimals match; p(x) is the selected ask. Pages: 228. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `afb437609a2b2f926f295e84c168d119511b1ccaa74e234d94b6229db32b87a1`.

- **p2:main: consistent** — Column sums of the visually checked 3x5 joint table are [16,17,11,22,34]/100; the total is 1. Marginalization sums over Y, rather than normalizing each column.
  Retained qualification: None
### p3 source and figure comparison

Same actual table: all15 entries and axis orientation match; p(y) is the selected ask. Pages: 228. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `983aaa3677a886d27083ac94b6ff7fb08d8c6819970a939c45213ae71be8bdd8`.

- **p3:main: consistent** — Row sums are [26,47,27]/100; top row is y1, as specified in both the current card and MML table. The total is 1.
  Retained qualification: None
### p4 source and figure comparison

Same actual table: y1 row and conditional p(x|Y=y1) selection match. Pages: 228. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `97fef6412a76bd4c06a04df67ed0a92831541567c50fc8912ced3425b903aeee`.

- **p4:main: consistent** — The y1 row masses [1,2,3,10,10]/100 divided by its positive marginal 26/100 give [1,2,3,10,10]/26. The displayed reduced fractions sum to 1 and multiply back to the original row.
  Retained qualification: None
### p5 source and figure comparison

Same actual table: x3 column and conditional p(y|X=x3) selection match. Pages: 228. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `16d84698a80fa483c339e11daeaae3f02644a75ad2ce1a3903bb86d4dd4b1315`.

- **p5:main: consistent** — Column x3 masses [3,5,3]/100 divided by 11/100 give [3,5,3]/11, in y1,y2,y3 order. These sum to 1 and recover the source column on multiplication.
  Retained qualification: None
### p6 source and figure comparison

Exercise6.3 compiler Bernoulli model matches. Current card explicitly supplies Beta(alpha,beta) and i.i.d. observations; book asks to choose a conjugate prior. Pages: 228. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `b292979cc76e582af5f378412c7a3e587f2bc73bb65ebec8b29494c0dc55fdba`.

- **p6:main: consistent** — The i.i.d. Bernoulli likelihood has exponents k and N-k; multiplying a proper Beta(alpha,beta) prior adds alpha-1,beta-1, giving Beta(alpha+k,beta+N-k). For N=10,k=2,alpha=beta=4, mode=5/16 and mean=1/3 differ as disclosed.
  Retained qualification: None

## 0921 / review-0921-Bayesian_Inference_Model_Selection

- Current source SHA256: `5c18d13b5c14cea0a508c7dbe542a0257566f246b5bbf57ad0fbf601b2485863`
- Current explanation HTML SHA256: `f25504cee3113cf5a658fdbadcf82181c97c5a98398334355c1e2a7583e63dd4`
- MML SHA256: `3f87b70c64a35d30ec4e565b4d5cfd18fe913002d3b3bed44691c7d0838911bc`
- source_visual: pass. content: pass with item qualifications. {'qualified_consistent': 4, 'consistent': 7}

### p1 source and figure comparison

Example8.7 factors and Figure8.9(a) arrow structure match; book wording about direct dependence is interpreted as graphical parents. Pages: 285, 286. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `eedc837d6b55650d6318224f375320f6bcf54f88c95c66889bca5ccfd7fdf86e`.

- **p1:a: qualified_consistent** — The represented factor p(c|a,b) assigns c the graphical parents a,b. It does not prove every distribution has nonzero statistical dependence on each parent.
  Retained qualification: Read direct dependence as represented graphical parents, not proven nonzero statistical/causal dependence.
- **p1:b: qualified_consistent** — The represented p(b|a) assigns a as the graphical parent of b. This is a factorization reading, not a causal claim.
  Retained qualification: Read direct dependence as represented graphical parents.
- **p1:c: qualified_consistent** — The factor p(a) has no conditioning parents. It does not imply marginal independence of a from descendants b,c; the retained reference answer is explicitly restricted in verify and pitfall.
  Retained qualification: Parentless does not mean marginally independent of descendants; retained answer is expressly restricted.
### p2 source and figure comparison

Figure8.9(a) visually gives a→b,a→c,b→c, all three pairs linked. Pages: 285, 286. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `4f301552c547c0c980a086e98a4d42cee1e305511ada56dc66d5d9c411e9d218`.

- **p2:a: consistent** — The three parent-to-child arrows are a→b,a→c,b→c, matching the inspected Figure 8.9(a).
  Retained qualification: None
- **p2:b: consistent** — There is one edge for each of the three unordered pairs; topological order a,b,c excludes a directed cycle. Fully connected here describes the skeleton.
  Retained qualification: None
### p3 source and figure comparison

Figure8.9(b) and Example8.8 have five nodes, with arrows x5→x2,x1→x3,x2→x3,x2→x4. Current source SVG was separately rendered and inspected. Pages: 285, 286. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `6c63efd72bd4e01989d061ab605eeaffd5554584b1e5101d009854cfbe531e10`.

- **p3:a: consistent** — Five nodes require five node factors, including root marginal factors.
  Retained qualification: None
- **p3:b: consistent** — The source SVG arrowheads, visually re-rendered here, give Pa(x1)=Pa(x5)=empty, Pa(x2)={x5}, Pa(x3)={x1,x2}, Pa(x4)={x2}; these agree with MML Figure 8.9(b).
  Retained qualification: None
- **p3:c: consistent** — Only x2→x4 enters x4, hence its factor is p(x4|x2). x5 is an ancestor rather than an extra direct parent.
  Retained qualification: None
### p4 source and figure comparison

Current source SVG geometry is identical to p3 except ID and was separately captured; it matches Figure8.9(b) and (8.30) five-factor product. Pages: 285, 286. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `ace9470d1e767816d78a64b31f5d2df6537c0845ee4adc36b5202bd5601b7abf`.

- **p4:main: consistent** — The exact five-factor product is p(x1)p(x5)p(x2|x5)p(x3|x1,x2)p(x4|x2), matching MML (8.30). Every node is the target of exactly one factor; reverse topological integration/summation gives normalization 1.
  Retained qualification: None
### p5 source and figure comparison

Exercise6.4 bag1 4mango/2apple, bag2 4/4, biased coin0.6/0.4 and posterior bag2 ask match exactly. Pages: 228. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `aa97044b82fadaa267ccc645b0c18e98f263bbdcdc91aee9afc69d241ff122f7`.

- **p5:main: consistent** — Joint mango masses are (3/5)(2/3)=2/5 for bag1 and (2/5)(1/2)=1/5 for bag2. Evidence is 3/5, so P(bag2|mango)=1/3; posterior odds 2:1 give the same result.
  Retained qualification: None
### p6 source and figure comparison

Exercise6.11 total expectation identity and conditioning notation match. Current card specializes to continuous variables; integrability is supplied in the explanation, not presumed unconditional. Pages: 229. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `bffb887b061981a0ccf40568d31fd8f7f6efc7f9ed81a835735b622660d42b33`.

- **p6:main: qualified_consistent** — For E|X|<infinity, substitute p(x|y)p(y)=p(x,y), apply Fubini, and marginalize y to obtain integral x p(x) dx=E[X]. Conditional values on p(y)=0 sets do not change the outer expectation. The nonintegrable case is not unconditionally approved.
  Retained qualification: For signed X the Fubini step needs E|X|<infinity (or another justified existence condition); no unconditional nonintegrable claim.
  Retained unresolved scope: The packet does not explicitly assume E|X|<infinity or nonnegative X. For arbitrary signed nonintegrable X the displayed expectations may be undefined, so the universal claim needs an existence/integrability condition.

## 0923 / review-0923-Linear_Regression

- Current source SHA256: `ac7057573b610d2c3da240ef300e4b0b66fbe0afed3808c9ab3f268160b7b31f`
- Current explanation HTML SHA256: `2bd75889835c93b48424b098a65251f1d0404ebf308357d8221b7054486165fc`
- MML SHA256: `3f87b70c64a35d30ec4e565b4d5cfd18fe913002d3b3bed44691c7d0838911bc`
- source_visual: pass. content: pass with item qualifications. {'consistent': 10, 'qualified_consistent': 2}

### p1 source and figure comparison

Example9.2 provides fitting-through-origin theory; inspected (9.12) gives estimator/rank condition. Current points (1,2),(2,5),(4,7) are authoritative adaptations, not the plotted book sample. Pages: 300, 301. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `3452702f8d5ca6430cce650e682fb1af03513273ba8cc849297649c83bd54b18`.

- **p1:a: consistent** — The scalar Gram term is 1+4+16=21>0, so the scalar inverse exists.
  Retained qualification: None
- **p1:b: consistent** — The input-label product sum is 2+10+28=40.
  Retained qualification: None
- **p1:c: qualified_consistent** — SSE=21 theta^2-80 theta+78 has unique minimum theta=40/21 and value 38/21 because its second derivative is 42>0. ML attribution assumes independent common positive Gaussian noise; source gives the estimator and marginal Gaussian setting, not a fully specified joint likelihood.
  Retained qualification: The supplied estimator and unique SSE solution are exact; ML attribution uses the intended independent common positive Gaussian noise setting, not specified as a full joint likelihood.
### p2 source and figure comparison

Same normal-equation theory. Current repeated x=1 observations and y=(1,3,4) are authoritative; their likelihood assumptions are incompletely stated and retained as a qualification. Pages: 300, 301. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `392d547ba212f052ecc6979cef7ca46399fda6cdd75f9a65499e0ac5ac462fda`.

- **p2:a: consistent** — Counting repeated x=1 observations separately gives X^T X=6 and X^T y=12.
  Retained qualification: None
- **p2:b: qualified_consistent** — The scalar normal equation 6 theta=12 gives theta=2; residual [-1,1,0] is orthogonal to X and SSE=2. This is an exact least-squares solution. Calling it ML requires the intended independent common-variance Gaussian model, which this card does not specify separately.
  Retained qualification: Normal-equation solution is exact; the source supplies no separate joint likelihood with which to establish ML independently.
### p3 source and figure comparison

Example9.3 monomial feature convention K and degree K-1 match; current K4,theta=(1,-2,0,1),x2 are adaptations. Pages: 301, 302. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `3bc308b21f34878977cc3a5cff573e1bdf481d56c0a2a07040c633ccdf5f71be`.

- **p3:a: consistent** — K=4 means powers 0 through 3, so phi(2)=[1,2,4,8]^T.
  Retained qualification: None
- **p3:b: consistent** — The dot product is 1-4+0+8=5, matching direct substitution in 1-2x+x^3. Linear refers to coefficients.
  Retained qualification: None
### p4 source and figure comparison

Same feature convention; current K3,theta=(2,0,-1),x3 are adaptations. Pages: 301, 302. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `ba2e6c8cc1384a7d207f5c83b7e01f31213c5c35c0737ccc637bc35376222c43`.

- **p4:a: consistent** — K=3 gives phi(3)=[1,3,9]^T; the zero linear coefficient does not remove the middle feature.
  Retained qualification: None
- **p4:b: consistent** — The ordered dot product is 2+0-9=-7, matching 2-x^2 at x=3.
  Retained qualification: None
### p5 source and figure comparison

Exercise2.5(a) all16 matrix entries and b=(1,-2,4,6) visually match. Pages: 71. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `4626368a68f1465c49502327da1220f7cb17dd6336d65fcc2d8f87cb74187c2a`.

- **p5:main: consistent** — The stated row eliminations are arithmetically consistent and end at [0,0,0,0|1]; coefficient rank 3 versus augmented rank 4 proves S is empty. This does not deny the existence of a least-squares approximation.
  Retained qualification: None
### p6 source and figure comparison

Exercise2.8(a) 3x3 entries visually match, including diagonal2,4,6. Pages: 72. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `2db785e87bf824fc758d8a9a9fbcbb782a495880c9ea4afb7cf89518874b8ddf`.

- **p6:main: consistent** — R3=2R2-R1 shows row dependence; first two rows are independent, so rank=2. Determinant -2+6-4=0 and null vector [1,-2,1] give separate singularity criteria.
  Retained qualification: None
### p7 source and figure comparison

Exercise2.8(b) all16 binary matrix entries visually match. Pages: 72. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `4605128dc2f31a2eb43b9e325ce366018a94cde76695976afcc52b731109e7ae`.

- **p7:main: consistent** — Gauss–Jordan operations are applied to both halves of [A|I]. The proposed inverse rows [0,-1,0,1],[-1,0,0,1],[1,1,0,-1],[1,1,1,-2] give identity in both multiplication orders, as also established by the frozen controller comparison.
  Retained qualification: None

## 0928 / review-0928-Linear_Regression

- Current source SHA256: `73ec702cd6ce6531c2e4ba32bbb1502d80fe0c964fe48e7e4450e494c27aa334`
- Current explanation HTML SHA256: `220900e1e3186be806502a86cb65565e68c88eb4dd683eb3b6b31a40a8673a75`
- MML SHA256: `3f87b70c64a35d30ec4e565b4d5cfd18fe913002d3b3bed44691c7d0838911bc`
- source_visual: pass. content: pass with item qualifications. {'consistent': 7, 'qualified_consistent': 5}

### p1 source and figure comparison

Example9.4 design-matrix arrangement matches. Current inputs -1,1,2 are explicit numerical adaptations. Pages: 302. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `45e36c6b521b4a933430b40c6e986fa071bc89f462e55139d36ede29a120011a`.

- **p1:main: consistent** — Putting one transposed feature vector in each row gives [1,-1,1],[1,1,1],[1,2,4]. The design matrix is 3x3 and Phi theta is 3x1; squaring -1 gives +1.
  Retained qualification: None
### p2 source and figure comparison

Example9.5 original figure uses N10 and degree4; current question explicitly changes to N8 and degree3. The noise model/function matches, and current adapted values control all answers. Pages: 302, 303. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `e40f4cf63ca62aaaa8a489a2c355b575467c693f24eec1e7a7bf3e9e6e2fab2f`.

- **p2:a: qualified_consistent** — The current authoritative adaptation uses degree 3, hence four features [1,x,x^2,x^3]. MML Example 9.5 instead used degree 4; its historical quotation is not the current numerical question.
  Retained qualification: Current degree 3 adaptation is explicit in current conditions and solve; the historical original quote degree 4 is different.
  Retained unresolved scope: The optional historical quotation says degree 4 whereas the current ask explicitly says degree 3. The derivation follows the current ask; if the historical quotation were intended instead, K would be 5.
- **p2:b: qualified_consistent** — For the current N=8, degree3 adaptation, Phi is 8x4. The original book figure uses N=10, degree4 and must not overwrite the stated current values.
  Retained qualification: The 8x4 answer is for current degree 3, not historical degree 4.
- **p2:c: qualified_consistent** — For fixed positive Gaussian noise variance and full column rank 4, the normal equation yields (Phi^T Phi)^-1 Phi^T y. At least four distinct inputs suffice for these monomial columns; in rank-deficient cases the inverse formula and uniqueness fail, as disclosed.
  Retained qualification: Inverse formula needs rank 4; current pitfall already supplies generalized inverse/nonunique alternative.
  Retained unresolved scope: Full column rank is not stated. Marginal x_n~Uniform[-5,5] alone does not guarantee distinct inputs without a sampling-dependence assumption; the inverse formula is conditional on rank 4. The usual independent continuous draws have full rank with probability 1.
### p3 source and figure comparison

Actual (9.31), Example9.6, Figure9.7 degree6/8 plots inspected. Original prior is I; current prior I/4 changes lambda to0.16. Figure supports historical qualitative comparison, not a universal adapted-data ranking. Pages: 307, 308. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `0d16c3e6f718f5107ed2f8aaf128a876d241f681ff78e7b64f6f8ede1fcb676f`.

- **p3:a: consistent** — Noise variance is (0.2)^2=1/25 and prior variance is 1/4, so lambda=(1/25)/(1/4)=4/25=0.16. The adapted prior is I/4, whereas the inspected MML example uses I.
  Retained qualification: None
- **p3:b: qualified_consistent** — Figure9.7 illustrates greater regularization visibility for the historical degree8 fit than degree6. No realized design/labels or quantitative effect criterion is supplied for this adapted prior, so a universal ordering is underdetermined. y=0 gives zero estimates at both degrees. Current solve/verify/pitfall and summary disclose this; approve only the example-specific interpretation.
  Retained qualification: Degree 8 effect is a historical/example tendency, not implied for every adapted dataset; y=0 is a disclosed counterexample.
  Retained unresolved scope: No realized design, labels, or quantitative definition of regularization effect is supplied, so a definitive comparison between degree 6 and degree 8 is unresolved.
### p4 source and figure comparison

Exercise5.1 function log(x^4)sin(x^3) matches; real-domain x≠0 qualification is necessary. Pages: 176. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `c0123c3b00d766ceccb1c4a427ba9f5cf3a843ec676a5d3600b54efbc748da71`.

- **p4:main: consistent** — On real x≠0, product and chain rules give (4/x)sin(x^3)+3x^2 log(x^4)cos(x^3). The identity log(x^4)=4log|x| preserves negative x; replacing it by 4log x requires x>0.
  Retained qualification: None
### p5 source and figure comparison

Exercise5.3 exponent -(x-mu)^2/(2sigma^2) matches; book/card broad sigma∈R includes undefined0, explicitly qualified by explanation. Pages: 176. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `d0462d307ffc6134577c9357193af1b53a938a25ea17dcb3161da200adbc6248`.

- **p5:main: qualified_consistent** — With fixed mu and sigma≠0, the inner derivative is -(x-mu)/sigma^2, multiplying the original exponential. Its sign changes from positive to negative at mu because sigma^2>0; sigma=0 in the overly broad original R condition is excluded explicitly.
  Retained qualification: Original sigma∈R includes undefined sigma=0; result applies for sigma≠0, with sigma>0 in a standard-deviation interpretation.
  Retained unresolved scope: The condition sigma in R allows sigma=0, for which the original function is undefined. A nonzero-sigma condition is needed.
### p6 source and figure comparison

Exercise5.7(a,b) functions, dimensions ExD and componentwise sin agree exactly. Pages: 177. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `0a67a9feb9cb2810828be98970e435b7a027841c1458d6ea27f895551a282978`.

- **p6:a: consistent** — For z=x^T x, df/dz is 1x1 and dz/dx=2x^T is 1xD; multiplying gives 2x^T/(1+x^T x). The logarithm is defined for all real x vectors because z≥0.
  Retained qualification: None
- **p6:b: consistent** — For componentwise sine, df/dz=diag(cos z) is ExE and dz/dx=A is ExD; product is ExD. Component differentiation gives cos(z_i)A_ij, confirming orientation.
  Retained qualification: None
### p7 source and figure comparison

Exercise5.8(c) tanh composition input N, output M and A of size MxN and explicit permission not to multiply Jacobians agree; the selected current problem retains its full conditions. Pages: 177. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `9229e32ede529aacb05bca46894575e22f72b1c79aafbb72fafb74e0bbb6fdd8`.

- **p7:main: consistent** — For componentwise tanh, df/dz=diag(1-tanh^2 z) is MxM, dz/dx=A is MxN, and the product is MxN with entries (1-tanh^2 z_i)A_ij. Bias is fixed and has zero derivative.
  Retained qualification: None
### p8 source and figure comparison

Exercise5.2 logistic sigmoid matches. Rewriting the derivative using f(x) is an explicit current additional ask and is answered. Pages: 176. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `5d81ac10b936fce8317a28d3b9904737b1743274e19f35e12ff8d8f3f2329e86`.

- **p8:main: consistent** — Two chain-rule negatives cancel: fprime=e^-x/(1+e^-x)^2=f(1-f)>0. At x=0, f=1/2 and derivative=1/4; the domain is all real x.
  Retained qualification: None

## Figure evidence

The separately rendered current 0921/p3 and p4 SVGs show x1→x3, x2→x3, x5→x2, x2→x4. Both raster captures are byte-identical (same geometry, different source SVG IDs): SHA256 `6fd721f2914097036533cd8d8e7cf86b2c9c750e99ec9df82ccd5ada51f6b0e9`. These were compared visually to actual MML285 Figure8.9(b), then against MML286 (8.30).

Page continuation/theory locators were expanded beyond historical page pointers: MML267 for (8.9),269 for (8.12),300 for (9.12),307 for (9.31),204 for the actual multivariate Gaussian density. Historical reports supplied locators only and were not accepted as current approval.
