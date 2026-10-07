# HW1 problem sources: books other than MML (PRML, Murphy PML1, GPML, ESL, ISL)

Method: downloaded PDF bytes into memory, extracted full text with PyMuPDF, then regex-searched. Page numbers are printed (book) pages.

## Books actually read (full text extracted and searched)
- Bishop, PRML (2006), Microsoft Research PDF, 758 pdf pages. Printed page = pdf page - 20.
- Murphy, Probabilistic Machine Learning: An Introduction (PML1), online version April 18 2025, 860 pdf pages. Printed page = pdf page - 30.
- Rasmussen & Williams, GPML, full RW.pdf, 266 pdf pages (App. A.2 on printed p.200).
- Hastie/Tibshirani/Friedman, ESL 2nd ed. (12th printing), 764 pdf pages.
- James et al., ISLP (Python ed.), 613 pdf pages.

## Books NOT read
- Murphy, MLAPP (2012): no legitimate free full-text PDF found; not opened. Its content (Ch.4 Gaussian, Ch.7 linear regression) is largely carried over into PML1, so PML1 is a good proxy.
- ISL (R edition) not separately read; ISLP used instead.

## Search for distinctive numbers
Regex search of all five texts found NO occurrence of: the exponent 4z^2-8z+7; data (-1,2),(0,1),(1,4); data 2,3,4; Phi^T Phi = diag(3,2) with Phi^T y=(7,2); mu=(1,-1) with Sigma=[[2,1],[1,2]]. So no near-identical numeric problems in these books. Matches below are STRUCTURAL (same derivation/theorem), not same numbers. Most likely the problems are instructor-made from lecture notes built on MML.

## Per problem

### P13 (MVN density with mu=(1,-1), Sigma=[[2,1],[1,2]], expand exponent)
- PML1 Eq. 3.11 (p.81): "The MVN density is defined by the following: N(y|mu,Sigma)". Eq. 3.18 (p.82) gives the expanded 2d form with rho. Same structure, no numeric match.
- PRML Eq. 2.43 (Sec 2.3, MVN density); GPML Eq. A.4 (p.200): density with (2pi)^{-D/2}|Sigma|^{-1/2}. Same structure, no numeric match.
- PML1 Exercise 3.6 (p.104) proves the normalizing constant (2pi)^{d/2}|Sigma|^{1/2}.

### P14 (p(z)=c exp[-1/2(4z^2-8z+7)], complete the square for c, mean, variance)
- PML1 Sec 3.3.2.1 "Completing the square" (p.88): "ax^2+bx+c = a(x-h)^2+k, h=-b/2a, k=c-b^2/4a". Best conceptual match. No numeric match.
- PRML Sec 2.3 (printed p.86, pdf 106) "sometimes called completing the square"; Exercise 2.38 (p.134) "Use the technique of completing the square".
- GPML Eq. 2.7 (p.9) completing the square for the weight posterior.
- No problem with these numbers.

### P15 (y_n = theta0 + theta1 x_n + eps, likelihood as single exponential of sum of squared errors)
- PRML Eq. 1.61-1.62 (p.29): likelihood p(t|x,w,beta)=prod N(t_n|y(x_n,w),beta^-1), and ln-likelihood "-beta/2 sum{y(x_n,w)-t_n}^2 + N/2 ln beta - N/2 ln 2pi". Also Eq. 3.10-3.12 (p.141).
- GPML Eq. 2.3 (p.9): "p(y|X,w) = 1/(2 pi sigma_n^2)^{n/2} exp(-1/(2 sigma_n^2)|y - X^T w|^2)". This is exactly the single-exponential form. Closest match for P15/P16.
- PML1 Eq. 11.4-11.5 (p.372): NLL(w,sigma^2) = 1/(2 sigma^2) sum (y_n - yhat_n)^2 + N/2 log(2 pi sigma^2).

### P16 (y|Phi,theta ~ N(Phi theta, sigma^2 I); full NLL incl constant; ML == min ||y-Phi theta||^2)
- PML1 Eq. 11.5-11.6 (p.372-373): NLL = 1/(2 sigma^2) sum ... + N/2 log(2 pi sigma^2); "NLL is equal (up to irrelevant constants) to the residual sum of squares".
- PRML Eq. 3.11-3.12 (p.141): "ln p(t|w,beta) = N/2 ln beta - N/2 ln(2pi) - beta E_D(w)"; text p.141 states that maximum likelihood under Gaussian noise equals minimizing sum-of-squares.
- GPML Eq. 2.3. No numeric match.

### P17 (normal equations from J=||y-Phi theta||^2; data (-1,2),(0,1),(1,4))
- PRML Eq. 3.15 (p.142): "w_ML = (Phi^T Phi)^-1 Phi^T t which are known as the normal equations".
- PML1 Eq. 11.7-11.9 (p.373): "Setting the gradient to zero ... X^T X w = X^T y. These are known as the normal equations".
- ESL Eq. 2.5 (p.12): "normal equations X^T(y - X beta) = 0".
- Numerical data (-1,2),(0,1),(1,4) not found in any book. PML1 Exercise 11.1 (p.411) is a numerical MLE (2d response, 6 data points) but different structure.

### P18 (prior theta~N(0,b^2 I): neg log posterior, MAP, lambda=sigma^2/b^2 ridge)
- PML1 Sec 11.3 (p.381), Eq. 11.52-11.53: "MAP estimation with a zero-mean Gaussian prior ... ridge regression", lambda = sigma^2/tau^2. Very close.
- ESL Exercise 3.6 and 3.7 (p.95): "Show that the ridge regression estimate is the mean (and mode) of the posterior" and "-log-posterior ... lambda = sigma^2/tau^2". Very close.
- PRML Sec 3.3.1 (p.153) ("minimization ... regularization term ... lambda = alpha/beta"); Sec 1.2.5 (p.30): "maximizing the posterior is equivalent to minimizing the regularized sum-of-squares ... lambda = alpha/beta".
- ISLP Sec 6.2 Fig 6.11 (p.251): "Ridge regression is the posterior mode for beta under a Gaussian prior".
- GPML Eq. 2.7 (p.9).
- PML1 Exercise 11.2 (p.411) ridge with centering.

### P19 (ML and MAP with Phi^T Phi=diag(3,2), Phi^T y=(7,2), b^2=1 and 1/4)
- Structure only (same as P17/P18 sources). Numbers not found in any of the five books.

### P22 (y=Ax+c: mean, covariance Sigma_y, cross-covariance C_xy; Gaussian given as exponent; shared noise in both coordinates)
- PML1 Eq. 3.5 (p.77) "Cov[Ax+b] = A Cov[x] A^T as shown in Exercise 3.4"; p.77 defines cross-covariance Cov[x,y]=E[(x-E x)(y-E y)^T]. Exercise 3.4 (p.103): "Let x be a random vector with mean m and covariance matrix Sigma. Let A and B be matrices. Derive the covariance matrix of Ax".
- PML1 Eq. 3.35-3.36 (p.86): joint of (z, y) with Sigma_z W^T cross-term, linear Gaussian system.
- PRML Eq. 2.108-2.110 (p.92): "E[y]=A mu + b; cov[y] = L^-1 + A Lambda^-1 A^T"; Eq. 2.105 joint covariance. Exercises 2.27 (p.132: covariance of sum of independent vectors), 2.31 (p.133: y=x+z), 2.28.
- GPML Eq. A.5-A.6. No numeric/"shared noise epsilon in both coordinates" problem found.

### P23 / P24 (scalar ML vs MAP: y_n=theta x_n+eps, prior N(0,1); y_n=theta+eps, prior N(1,1), data 2,3,4)
- PML1 Sec 3.3.3 "Inferring an unknown scalar" Eq. 3.50-3.57 (p.88-90): mu_N formula, posterior mean is convex combination of MLE and prior mean. Fig 3.8 uses prior N(0,1).
- PML1 Exercise 4.2 (p.164) "MAP estimation for 1D Gaussians": samples x_1..x_n, known sigma^2, prior mu~N(m,s^2); asks MAP estimate and its limits as n grows or prior variance changes. Closest textbook exercise to P24 (no numbers given).
- PML1 Exercise 4.3 (p.164).
- PRML Eq. 2.140-2.142 (p.98): posterior mean mu_N of Gaussian mean; Exercise 2.38-2.39 (p.134).
- Data 2,3,4 not found.

### P25 (normalized product of two Gaussians N(mu0,Sigma0) N(mu1,Sigma1))
- GPML Eq. A.7-A.8 (p.200): "N(x|a,A)N(x|b,B) = Z^-1 N(x|c,C), c = C(A^-1 a + B^-1 b), C = (A^-1 + B^-1)^-1", with Z^-1 = (2pi)^{-D/2}|A+B|^{-1/2} exp(-1/2 (a-b)^T (A+B)^-1 (a-b)). Best match, includes the normalizing constant.
- PML1 Sec 3.3.5 sensor fusion (p.92) and Eq. 3.58-3.60 (p.90), Eq. 3.66-3.68 (p.91): precision-weighted combination (posterior = prior x likelihood). Exercise 3.7 (p.105) sensor fusion.
- PRML Exercise 2.40 (p.134) (Gaussian posterior with prior N(mu|mu0,Sigma0)).

## Summary
No book contains the exact numeric instances. Closest structural sources by problem:
- P14: PML1 3.3.2.1 (p.88); P15/16: GPML Eq 2.3, PRML 1.62/3.11, PML1 11.5; P17: PRML 3.15, PML1 11.8; P18: ESL Ex 3.6/3.7 and PML1 11.52; P22: PML1 Ex 3.4 + PRML 2.108-2.110; P23/24: PML1 3.3.3 and Ex 4.2; P25: GPML A.7-A.8.
