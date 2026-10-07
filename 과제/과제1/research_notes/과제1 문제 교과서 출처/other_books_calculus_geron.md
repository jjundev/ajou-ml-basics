# Other textbooks vs. HW1 problems (MML excluded)

Method: downloaded files, extracted text (PyMuPDF / ipynb JSON), grep + read around hits. Date 2026-10-07.

## What was actually read

| Source | Status |
|---|---|
| Matrix Cookbook (Petersen & Pedersen, 2012-11-15), `math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf` | READ in full text (72 p., grep + sections 2.4, 6.1-6.2) |
| Boyd & Vandenberghe, Convex Optimization, `web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf` | READ text (714 p.); inspected Appendix A.4 (derivative/gradient/Jacobian) and notation, grep for worked numbers |
| Geron handson-ml3 notebooks (GitHub raw): `04_training_linear_models.ipynb`, `math_linear_algebra.ipynb`, `math_differential_calculus.ipynb` | READ (code + markdown cells + Ch.4 exercise SOLUTIONS 1-12). NOTE: notebooks do NOT contain the book's Ch.4 prose/equations, nor the exercise question texts (only answers). Book prose could not be opened (not free). |
| Calafiore & El Ghaoui, Optimization Models | BOOK NOT FREE. Read only the free Exercise Manual (`ExManual.pdf`, 77 p.) and ToC. Chapter text not read. |
| Blitzstein & Hwang | COULD NOT OPEN (Harvard PDF returned Access Denied; mirror returned HTML stub). Not read. |
| Bertsekas & Tsitsiklis | NOT OPENED (no free direct PDF found). |
| Ross, Gubner, Stewart/Thomas Calculus | NOT OPENED (no free legal text found). |

## Per-problem results

### P10 gradients (f=u^2+3v^2-2u+4v; g=u^2+2uv+3v^2-4u+2v; h=(u+2v-w-3)^2)
- Geron: not found. `math_differential_calculus.ipynb` defines gradient in general ("Gradient Descent, revisited", "Jacobians" sections) with different examples (e.g. sin(xy)); no matching function.
- Matrix Cookbook: not found as numerical exercise; only general formulas, eq (69) d(x^T a)/dx = a, eq (96)-(97) gradient of x^T A x + b^T x = (A+A^T)x + b.
- Boyd-Vandenberghe A.4.1: general definition only; "gradient ... is a (column) vector" (matches the HW convention). Example f=(1/2)x^T P x+q^T x+r, grad = Px+q. No numeric match.
- Calafiore ExManual: not found (Ex 3.1 composite derivatives, general only).

### P11 Jacobian (f=[u+2v;3u-v], g=[u^2+v;uv;v^2], m rows outputs, n cols inputs)
- Geron `math_differential_calculus.ipynb`, "Jacobians": "one column per input dimension and one row per output dimension" - SAME CONVENTION/wording as the HW hint, but generic matrix, no matching functions. Best Geron wording match found.
- Boyd-Vandenberghe A.4.1: "Df(x)_ij = df_i/dx_j, i=1..m, j=1..n" with Df in R^{m x n} - identical convention to HW hint ((J_f)_ij = df_i/dx_j). No numeric examples.
- Calafiore ExManual Ex 3.1: "Jacobian matrix of h at x, i.e., the matrix whose (i, j) element is dh_i/dx_j" - same convention, proof exercise only.
- Matrix Cookbook: no Jacobian section (word absent).

### P12 h(x)=x^T Q x - 2 b^T x, Q=[[3,1],[1,2]], b=(1,-1)
- Not found with these numbers anywhere read.
- Closest structure: Calafiore ExManual Ex 4.4 "Minimizing a quadratic function": min 1/2 x^T Q x - c^T x (general Q, no numbers; answer x=Q^-1 c). Boyd A.4.1 quadratic example (grad = Px+q). Matrix Cookbook (96)-(97). All general, none numeric.
- Geron: not found.

### P21 sample mean & covariance (denominator N) of (1,1),(1,3),(3,3),(3,5)
- Not found with these numbers in any source read.
- Definition match only: Calafiore ExManual Ex 4.5: sample covariance "Sigma = 1/m sum (x_i - xhat)(x_i - xhat)^T" with xhat = 1/m sum x_i - same denominator-m definition as HW; no numbers.
- Geron: not found (Ch.4 notebooks contain no sample covariance computation).

### P22 y=Ax+c: mean, covariance, cross-covariance (incl. shared noise)
- Matrix Cookbook sec 6.2.1, eqs (312)-(317): E[Ax+b]=Am+b, Var[Ax]=A Var[x] A^T, Cov[Ax,By]=A Cov[x,y] B^T (so C_xy = Sigma_x A^T). Formula source only; no numeric problem. Quote: "Var[Ax] = AVar[x]A^T".
- Calafiore ExManual Ex 3.9: u zero mean, cov I_n, "covariance matrix of the output, y = Au?" - structural cousin (A u), no shift c, no cross-covariance, no numbers.
- Geron: not found. Boyd: not found.
- Shared-noise case (epsilon in both coordinates): not found anywhere read.

### P8, P9, P16-P20 vs Geron Ch.4 (as far as notebook shows)
- Normal equation: notebook `theta_best = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y` (Geron uses theta, X_b with x0=1 bias column; HW uses Phi, beta-like notation instead of X). Same formula as P17(a); no matching numbers. Geron generates random data y=4+3x+noise; HW P17(b)/P19 data (-1,2),(0,1),(1,4) not present.
- P8 (A^T A, det, inverse): only appears in Geron's math_linear_algebra notebook generically (matrix products/inverse); no match for the 3x2 matrix [[1,-1],[1,0],[1,1]].
- P9 feature map phi(x)=(1,x,x^2): Geron Ch.4 "Polynomial Regression" uses `PolynomialFeatures(degree=2, include_bias=False)` and says (notebook text) it is still a linear model in the parameters; HW's explicit design matrix with x=-1,0,1 not present. Concept match, not problem match.
- P18/P19/P20 ridge/MAP: notebook "Ridge Regression" has closed form code `np.linalg.inv(X_b.T @ X_b + alpha * A) @ X_b.T @ y` with A = identity except 0 for bias (so Geron does NOT penalise the intercept; HW P18 says prior applies to every coefficient incl. intercept - a notation/convention difference). Geron never derives ridge as MAP with Gaussian prior (no "likelihood"/"posterior" strings in the Ch.4 notebook). Its objective is MSE + alpha*(1/2)||w||^2 style (prose from memory, NOT verified - book text not opened), vs HW ||y-Phi b||^2 + lambda||b||^2.
- P16/P17 MLE under Gaussian noise: Not in Geron Ch.4 notebook (no likelihood derivation).
- Geron Ch.4 exercises (solutions section, `## 1. to 11.` and `## 12.`): 12 exercises, all conceptual (millions of features, feature scales, convexity, early stopping, overfit/underfit, Ridge vs Lasso vs Elastic Net, logistic/softmax). Exercise 12 = Batch GD with early stopping for Softmax on iris. NONE match P8-P22. (Exercise question text itself not read - only solutions.)

## Bottom line
- No exact or near-identical problem (same numbers) found in any readable source. The HW problems appear to be original numerical instances of standard formulas.
- Best formula/convention sources: Boyd-Vandenberghe A.4.1 (gradient column vector, Jacobian m x n, grad of quadratic), Geron math_differential_calculus (Jacobian rows=outputs, cols=inputs), Matrix Cookbook 6.2.1 (mean/cov/cross-cov of linear maps), Calafiore ExManual Ex 4.4 (quadratic minimisation), Ex 4.5 (sample covariance with 1/m), Ex 3.9 (covariance of Au).
- Not checked: Blitzstein-Hwang, Bertsekas-Tsitsiklis, Ross, Gubner, Stewart/Thomas, Calafiore book chapters, Geron book prose.
