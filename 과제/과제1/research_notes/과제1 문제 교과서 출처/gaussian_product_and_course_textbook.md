# P25 (product of Gaussians) source and Ajou "Introduction to Machine Learning" (Prof. Bang Chul Jung) textbook

## Q1. Which textbooks present the product-of-two-Gaussians result, and which fits P25's style best?

### Takeaway
The result (precision-additive covariance, precision-weighted mean) is stated verbatim in Rasmussen & Williams GPML Eq. A.7 and Matrix Cookbook Sec. 8.1.8; I verified both from the actual PDF text. Rasmussen & Williams A.7 is the best stylistic fit (explicit "normalized up to Z" phrasing). I could not verify Bishop, Murphy or MML section/equation numbers (PDFs too large or snippets not retrieved), so they are NOT claimed. No source found that is the specific origin of P25's numbers; it is almost certainly an instructor-made numeric instance.

### Cited Findings
- Rasmussen & Williams, GPML (MIT Press 2006), App. A.2, Eq. (A.7): "The product of two Gaussians gives another (un-normalized) Gaussian: N(x|a,A) N(x|b,B) = Z^-1 N(x|c,C), where c = C(A^-1 a + B^-1 b) and C = (A^-1 + B^-1)^-1." Text adds that the precision is the sum of precisions and the mean is the precision-weighted convex sum of the means. — [GPML Appendix A PDF](https://gaussianprocess.org/gpml/chapters/RWA.pdf) (text extracted and read)
- GPML Eq. (A.8) gives the constant: Z^-1 = (2π)^(-D/2) |A+B|^(-1/2) exp(-1/2 (a-b)^T (A+B)^-1 (a-b)); the hint to expand C = A - A(A+B)^-1 A = B - B(A+B)^-1 B (matrix inversion lemma). — same source
- Matrix Cookbook Sec. 8.1.8 "Product of gaussian densities": N_x(m1,Σ1) N_x(m2,Σ2) = c_c N_x(m_c,Σ_c), with c_c = N_{m1}(m2, Σ1+Σ2), m_c = (Σ1^-1+Σ2^-1)^-1 (Σ1^-1 m1 + Σ2^-1 m2), Σ_c = (Σ1^-1+Σ2^-1)^-1; "the product is not normalized as a density of x". — [Matrix Cookbook (Petersen & Pedersen)](https://www2.imm.dtu.dk/pubdb/edoc/imm3274.pdf) (text extracted and read; section 8.1.8 as in the 2012 version)
- Julius O. Smith, Spectral Audio Signal Processing, "Product of Two Gaussian PDFs" gives the scalar version (parallel-combination variance, precision-weighted mean). — [DSPRelated](https://www.dsprelated.com/freebooks/sasp/Product_Two_Gaussian_PDFs.html)
- Search snippet (secondary, not primary text) confirms the general statement for arbitrary precision-parameterised Gaussians in several arXiv papers; not a textbook locator. — [Gaussian Belief Propagation (arXiv 0811.2518)](https://arxiv.org/pdf/0811.2518)

### Worked answer for P25 (my own computation, checked by hand; not from a source)
- Σ0^-1 = diag(1, 1/2); Σ1^-1 = (1/3)[[2,-1],[-1,2]]
- Σ_q^-1 = [[5/3, -1/3],[-1/3, 7/6]], det = 11/6
- Σ_q = [[7/11, 2/11],[2/11, 10/11]], det Σ_q = 6/11
- μ_q = Σ_q (Σ0^-1 μ0 + Σ1^-1 μ1) = Σ_q (1/3, 1/3)^T = (3/11, 4/11)^T
- q(x) = 1/(2π sqrt(6/11)) exp(-1/2 (x-μ_q)^T [[5/3,-1/3],[-1/3,7/6]] (x-μ_q))
- Unnormalized constant (Matrix Cookbook c_c / GPML Z^-1) = N(μ0 | μ1, Σ0+Σ1) with Σ0+Σ1 = [[3,1],[1,4]], det 11, exponent -1/2 (1,1)[[4,-1],[-1,3]]/11 (1,1)^T = -3/22.

### Inferences
- P25's wording ("normalized product q(x) ∝ p0 p1", "explicit normalized density") matches GPML A.7's framing (un-normalized product, Z^-1 N(c,C)) and Matrix Cookbook 8.1.8; the "normalize it yourself" step is the extra work the homework asks for. Best citation pair: GPML Eq. A.7 and Matrix Cookbook 8.1.8.
- The homework's sequence (Gaussian density expansion, completing the square, MAP/ridge, cross-covariance) is the standard route to derive the product by completing the square, so Bishop PRML Sec. 2.3.3 (Bayes' theorem for Gaussian variables) and MML Sec. 6.5 are plausible pedagogical neighbours, but this is unverified.

### Gaps
- Bishop PRML Sec. 2.3.3 / Eqs. 2.113-2.117, Murphy (PML Sec. 2.2.3 / MLAPP Sec. 4.4), MML Sec. 6.5 and its exercises: could not retrieve text (PDF too large for fetch; searches returned no snippet). Do not cite these as verified.
- No source found that contains P25's specific μ0, μ1, Σ0, Σ1; origin appears to be instructor-authored.

## Q2. Which textbooks are listed for the Ajou course (Prof. Bang Chul Jung)?

### Takeaway
I found NO publicly accessible syllabus, lecture notes or slides naming a textbook for Ajou's "머신러닝기초 / Introduction to Machine Learning" under Prof. Jung, and no ML textbook authored by him. The course textbook is unknown from public sources; Blackboard or the Ajou sugang syllabus (login-gated) would be the place to check.

### Cited Findings
- Prof. Bang Chul Jung (정방철) is a wireless-communications researcher (Wireless Communications and Network Research Lab); research areas: interference management/anti-jamming, MIMO and compressed sensing, 5G/6G access and backhaul. B.S. Ajou (2002), M.S./Ph.D. KAIST. — [KOTECH Market profile](https://www.kotechmarket.com/en/researcher/701); [AMiner snippet via search](https://www.aminer.org/profile/bang-chul-jung/53f46b71dabfaeb2ac10a52c)
- Affiliation conflict: the KOTECH page lists "Chungnam National University" but gives contact bcjung@ajou.ac.kr and an 031-219 (Suwon/Ajou) number, and a search summary says he is in Ajou's Dept. of Electronics Engineering; AMiner/older sources say Chungnam National University (older affiliation, then Gyeongsang National Univ 2010-2015). Likely moved to Ajou and the profile pages are stale; the Ajou ECE page I fetched did not mention him (it only showed other faculty news). — [Ajou ECE](https://ajou.ac.kr/ece), [KOTECH](https://www.kotechmarket.com/en/researcher/701)
- Search-engine summary (secondary, unverified by me) claims he received the IEEE ComSoc Certificate of Merit in 2026 as an Ajou ECE professor. — [search result: Ajou ECE](https://www.ajou.ac.kr/ece/index.do)
- Multiple Korean and English queries (정방철 머신러닝 교재, 아주대 머신러닝기초 강의계획서, Bang Chul Jung Ajou machine learning textbook, Mathematics for Machine Learning pairing) returned only unrelated books (Zhou's Machine Learning, Forsyth, MML generic pages) and other universities' syllabi; none connect to Prof. Jung.

### Inferences
- Because his field is wireless/information theory, he is unlikely to have authored a general ML textbook; the course probably uses a standard text or his own slides. Which one is unknown.
- The homework's content (linear algebra, Gaussians, ridge/MAP) is consistent with MML (Deisenroth et al.) or Bishop PRML, but this is a guess based on topic fit, not evidence about the course.

### Gaps
- Official syllabus (Ajou sugang / Blackboard) not publicly accessible or not indexed; the aurora.ajou.ac.kr researcher profile (id=463) loaded only "Loading..." (JS-rendered), so unread.
- No lecture slides, YouTube descriptions, GitHub repos or personal homepage found citing a textbook.
- Recommendation: check the course's Blackboard syllabus or lecture-slide reference list directly (the ajou-bb skill can download slides), and grep them for "Bishop", "Deisenroth", "Murphy".
