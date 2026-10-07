# Textbook origin of Homework 1 problems P10-P14, P21-P22 (gradients, Jacobians, quadratic forms, Gaussian density, sample stats, affine transforms)

Method: I downloaded the MML PDF (draft 2024-01-15, mml-book.github.io/book/mml-book.pdf), ran pdftotext, and read the exercise lists and relevant sections directly. I did not obtain the Bishop, Murphy or Matrix Cookbook texts, so statements about them come from background knowledge and are labelled unverified. No Ajou course page or lecture slides were found.

## Do the problems match specific worked examples or exercises in MML, Bishop or other texts?

### Takeaway
No problem matches an MML or other textbook exercise verbatim, and none of the numbers match. P22 follows MML Sec 6.4.4 and Exercise 6.12 in topic and structure. P21 follows MML Definition 6.9 (denominator N). P10-P14 look like generic instructor-written drill problems. Their gradient convention (column vector) differs from MML (row vector).

### Cited Findings
- MML Ch.5 exercises 5.1-5.9 are single-variable derivatives, Taylor polynomials, Jacobians of f1(x)=sin(x1)cos(x2), f2(x,y)=x^T y, f3(x)=x x^T (Ex 5.5), tr(AXB) (5.6), and chain-rule problems (5.7-5.9). None has the numeric polynomials of P10-P12 (e.g. u^2+3v^2-2u+4v). — [MML PDF](https://mml-book.github.io/book/mml-book.pdf), Ch.5 "Exercises" (read via local pdftotext)
- MML defines the gradient of f: R^n -> R as a ROW vector (1 x n). It states explicitly that "it is not uncommon in the literature to define the gradient vector as a column vector", and it uses the numerator layout, so the Jacobian of f: R^n -> R^m is m x n. P10's "gradient as column vector" therefore contradicts MML. P11's "m rows outputs, n columns inputs" matches MML (Sec 5.3, numerator layout). — [MML PDF](https://mml-book.github.io/book/mml-book.pdf), Remark "Gradient as a Row Vector", Sec 5.2, 5.3
- MML Example 5.7 (gradient of x1^2 x2 + x1 x2^3) and Example 5.9 (Jacobian of f(x)=Ax gives A in R^{MxN}) are the closest worked examples to P10/P11 in topic. — [MML PDF](https://mml-book.github.io/book/mml-book.pdf)
- MML Ch.6 exercises: 6.10 asks for the product of two Gaussians "by completing the square". 6.12 "Manipulation of Gaussian Random Variables" uses y = Ax + b + w with independent noise w ~ N(0,Q) and asks for the mean and covariance of y. — [MML PDF](https://mml-book.github.io/book/mml-book.pdf), Ch.6 Exercises
- MML Sec 6.4.4 states the affine transformation results: E[y]=Aμ+b (6.50), V[y]=AΣA^T (6.51), and Cov[x,y]=ΣA^T (6.52d) with y=Ax+b. Sec 6.5 uses Σ_xy = Cov[x,y] for the cross-covariance matrix (6.64). — [MML PDF](https://mml-book.github.io/book/mml-book.pdf)
- MML Definition 6.9 (Sec 6.4.2): the empirical mean is x̄ = (1/N) Σ x_n and the empirical covariance is Σ = (1/N) Σ (x_n - x̄)(x_n - x̄)^T. MML uses the biased 1/N version and says the 1/(N-1) version is the unbiased one. This matches P21's "denominator N=4". — [MML PDF](https://mml-book.github.io/book/mml-book.pdf)
- Searches did not find the Ajou course page or homework (Prof. Jung's public profile pages point to Chungnam National University, not Ajou). — [Search result list](https://www.aminer.org/profile/bang-chul-jung/53f46b71dabfaeb2ac10a52c)
- General web results confirm only the standard fact Y=AX+b implies Y ~ N(Aμ+b, AΣA^T). — [Columbia lecture notes](https://www.cs.columbia.edu/~djhsu/coms4771-f20/lectures/06-multivariate_gaussians_and_pca.pdf) (found in search results, not opened in full)

### Inferences
Per-problem best source (confidence: exact / same topic and notation / generic):
- P10 (column-vector gradients at a point): generic. Topic is MML Sec 5.2 and Ex 5.7, but the column convention is not MML's. The convention fits Bishop and Murphy (unverified) and the Matrix Cookbook.
- P11 (Jacobian, m x n): same topic and layout as MML Sec 5.3 and Ex 5.5, 5.9. The numbers do not match (confidence: moderate on topic, low on exactness).
- P12 (quadratic form x^T Q x - 2b^T x, set gradient to zero): generic. The minimizer is x = Q^{-1}b. Related in spirit to the MML Ch.9 least-squares derivations (Example 5.11 gradient of a least-squares loss, Sec 9.2). This is not a specific match.
- P13 (explicit 2-D Gaussian density, expand the exponent): generic. Topic is MML Sec 6.5 or Bishop 2.3; no specific match.
- P14 (p(z)=c·exp[-½(4z²-8z+7)], find c, mean, variance): same technique as MML Ex 6.10 (completing the square) and Bishop Sec 2.3.1 (unverified). The numbers are instructor-made (confidence: generic/same topic).
- P21 (sample mean and covariance of four 2-D points, denominator N): same topic and notation as MML Def 6.9. The 1/N choice is explicitly MML's convention (confidence: high on convention, no exact exercise).
- P22 (mean, covariance and cross-covariance of y=Ax+c): same topic and notation as MML Sec 6.4.4 (6.50-6.52) and Ex 6.12. The shared-noise-epsilon variant is like the MML Ex 6.12 setup (confidence: high on topic, not exact).

Overall, MML is the most plausible reference text for P11, P21 and P22. The column-gradient convention in P10 hints the instructor may use a different text or their own notes (e.g. Bishop/Murphy style); this is speculation.

### Gaps
- Bishop PRML, Murphy and Matrix Cookbook were not opened, so chapter and section claims for them are unverified.
- The Ajou course syllabus, slides and textbook were not found, so the course's actual reference text is unknown.
- I did not search exhaustively for the exact numbers on other university problem sets. Instructor-modified numbers would be hard to find that way.
- Only MML draft 2024-01-15 was checked; later printings may renumber exercises.
