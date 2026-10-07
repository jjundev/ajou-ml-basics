# Source of Homework #1 Problems P15-P20, P23-P24 (linear regression likelihood, ML, MAP / ridge)

Method: web search for the textbook and syllabus returned nothing useful (the full MML PDF exceeded WebFetch's size limit). The course's own local copy of MML (`교과서/Mathematics_for_Machine_Learning.pdf`, draft 2024-01-15) was text-extracted with pdftotext and read directly. The Lecture03/04 slides and the homework PDF were extracted the same way. The syllabus PDF could not be extracted (CID font error, no text). Local file paths are given as sources because no web URL applies.

## Do P15-P20, P23-P24 match MML Section 9.2 and its notation?

### Takeaway
Yes on notation and derivation structure. The symbols (theta, Phi, sigma^2, prior N(0, b^2 I), the sigma^2/b^2 equivalence) match MML Ch. 9 almost one-to-one, and MML is the course textbook (Lecture03 and Lecture04 cite "Chapter 9.3.4"). The numeric examples and the exercises themselves are not in MML. They are most likely instructor-written, built on MML's formulas. Confidence that MML Ch. 9.2 is the notational and derivational source: high (about 90%). Confidence that any specific problem was copied from a textbook exercise: low, with no match found.

### Cited Findings
- MML 9.1 models y = f(x) + eps with eps ~ N(0, sigma^2) i.i.d. Gaussian noise and likelihood p(y|x) = N(y | f(x), sigma^2), eqs (9.1)-(9.2). Parameters are theta. The homework uses the same names. — `교과서/Mathematics_for_Machine_Learning.pdf`, p.291
- MML 9.2 gives the likelihood factorization p(Y|X,theta) = prod_n N(y_n | x_n^T theta, sigma^2), eq (9.5b). The homework's P15 and P23-P24 ask for exactly this "likelihood as a single exponential of a sum of squares". — same file, p.292
- MML 9.2.1 minimizes the negative log-likelihood. It gives L(theta) = (1/(2 sigma^2)) ||y - X theta||^2 in eq (9.10b), the gradient in (9.11), and theta_ML = (X^T X)^-1 X^T y in (9.12c). This matches P16 (negative log-likelihood equals least squares) and P17(a) (normal equations, theta_ML). — same file, pp.293-294
- MML "Maximum Likelihood Estimation with Features" (after Example 9.2) uses y = phi(x)^T theta + eps, the feature matrix Phi (K columns), the negative log-likelihood (9.18) and theta_ML = (Phi^T Phi)^-1 Phi^T y in (9.19). Example 9.4 gives Phi for second-order polynomials, with rows (1, x_n, x_n^2). Homework P9 uses phi(x) = (1, x, x^2)^T at x = -1, 0, 1. — same file, around pp.295-297
- MML 9.2.3 MAP uses the prior p(theta) = N(0, b^2 I) with the same symbol b^2. It writes the negative log-posterior as (1/(2 sigma^2)) (y - Phi theta)^T (y - Phi theta) + (1/(2 b^2)) theta^T theta + const, eq (9.28). The MAP estimate is theta_MAP = (Phi^T Phi + (sigma^2/b^2) I)^-1 Phi^T y, eq (9.31). This matches P18 and P19, including the "b^2" notation. — same file, pp.300-301
- MML 9.2.4 "MAP Estimation as Regularization" gives the regularized least-squares loss ||y - Phi theta||^2 + lambda ||theta||^2, eq (9.32), and theta_RLS = (Phi^T Phi + lambda I)^-1 Phi^T y, eq (9.34). It states this is identical to MAP for lambda = sigma^2/b^2, which is what P18 asks ("identify the value of lambda"). P20(c) uses the same loss with lambda = 5. — same file, pp.302-303
- MML says a prior p(theta) = N(0, 1) on a single parameter encodes values in [-2, 2] (9.2.3). That is the same flavor as the scalar prior N(0, 1) in P23. — same file, p.300
- MML Ch. 9 has no end-of-chapter exercises. The local exercise PDFs cover only Chapters 2-7 (`교과서/연습문제/Chapter_02..07_*.pdf`). The "Exercises" lines in the extracted text are for other chapters. So P15-P24 cannot come from MML's own exercise set. — `교과서/연습문제/` and the MML table of contents
- Lecture03 slides (MAPE with Gaussian prior N(0, b^2 I); "MAP vs. ML: theta_MAP = (Phi^T Phi + (sigma^2/b^2) I)^-1 Phi^T y, theta_ML = (Phi^T Phi)^-1 Phi^T y"; "Regularization: MAPE vs. Explicit Regularizer") and Lecture04 (footnote "Chapter 9.3.4", "mean coincides with the MAP estimate") follow MML's notation. — `강의노트/Lecture03_Linear_Regression_Part1_rev.pdf`, `강의노트/Lecture04_Linear_Regression_Part2.pdf`
- The homework statements for P15-P24 were read directly. Every one uses theta, Phi, sigma^2, b^2, theta_ML, theta_MAP and N(0, b^2 I_K). P18's own hint writes the prior density as (2 pi b^2)^(-K/2) exp(-||theta||^2/(2 b^2)). — `과제/과제1/26_10_Introduction_to_Machine_Learning_homework1_rev.pdf`

### Inferences
- Per-problem best match (all MML; the numbers are likely instructor-made):
  - P15 (theta_0 + theta_1 x_n + eps): MML (9.5b) with Gaussian likelihood (9.3)/(9.9), a straight line with intercept. MML's own line example (9.4) has no intercept, and the numbers are not from MML. Confidence in notation: medium-high; numbers: no source.
  - P16 (y | Phi, theta ~ N(Phi theta, sigma^2 I_N)): MML (9.13), (9.18), (9.10b). Confidence: high.
  - P17: normal equations and theta_ML from MML (9.11)-(9.12), (9.19). The numerical data (-1,2), (0,1), (1,4) was not found in MML. Confidence: high for the formula, none for the data.
  - P18: MML (9.24)-(9.31), (9.32)-(9.34) with lambda = sigma^2/b^2. Confidence: high (about 95%).
  - P19: MML (9.31) and (9.19), with instructor-chosen Phi^T Phi and Phi^T y. It is probably consistent with the P17 data: the Gram matrix [[3,0],[0,2]] and Phi^T y = (7,2) are what a design matrix with rows (1,-1), (1,0), (1,1) gives for the data of P17 (sum of y = 7, sum of x*y = 2). This was computed by hand, not found in a source.
  - P20: rank-deficient Phi, where MML only requires rk(Phi) = K for (9.19) and says that (Phi^T Phi + lambda I) is positive definite. The singular case is a pedagogical add-on. Confidence: medium (MML supports the point, the problem is not in MML).
  - P23, P24: scalar versions of (9.12c) and (9.31) with Phi a column of x_n (P23) or ones (P24). The prior N(1, 1) in P24 is a non-zero mean prior, which is outside MML's N(0, b^2 I). It matches the "Aside: MAPE for General Gaussian Prior N(m_0, S_0)" in Lecture03, so P24 may derive from the lecture slides.
- The notation fingerprint (theta, Phi, b^2, sigma^2/b^2) distinguishes MML from Bishop. Bishop (PRML Ch. 3) writes w, t, Phi, beta (noise precision) and alpha (prior precision), with the regularizer lambda = alpha/beta. This is from memory and was not checked against the text in this session. The homework therefore does not follow Bishop.
- Murphy, Hastie et al. were not checked. The use of b^2 and theta_MAP matches MML, and I did not see any need to look elsewhere.

### Gaps
- The Ajou syllabus (`강의계획서/...pdf`) text could not be extracted (font error), so the official textbook listing was not confirmed. MML being the textbook is inferred from the folder `교과서/Mathematics_for_Machine_Learning.pdf` and the slide citations.
- No online source was found for the specific numbers in P17, P19, P20, P23, P24 (e.g. data (-1,2),(0,1),(1,4)). They may come from a problem book or the instructor's own materials. MML's "Additional exercises with solutions" (Overleaf link on mml-book.github.io) could not be opened, so I cannot exclude that it contains similar problems.
- Bishop, Murphy and Hastie et al. were not opened. The claim that Bishop uses alpha, beta, w is from memory.
