# HW1 problem sources: other applied-LA books (not MML)

Method: text extracted with pdf.js in the Browser pane (or raw HTML fetch), then regex-searched for distinctive numbers and phrases. Number matching is weak because pdf.js flattens matrices, so numeric non-hits are "not found by text search", not proof of absence.

## Actually read (full text searched)
1. VMLS (Boyd & Vandenberghe), web.stanford.edu/~boyd/vmls/vmls.pdf, 473 PDF pages, ~1.04M chars.
2. CS229 Linear Algebra Review and Reference (Kolter/Do), cs229.stanford.edu/section/cs229-linalg.pdf, 26 pages.
3. Goodfellow et al., Deep Learning, Ch.2 (deeplearningbook.org/contents/linear_algebra.html), full chapter HTML (~980k chars with markup).
4. MIT 18.06SC Session 2.3 problem set (Strang 4.3 #17-22), one PDF only.
5. Berkeley CS189 lec 13 (ridge) via WebFetch summary only (not full text).

## Not read
- Strang textbook itself and "Linear Algebra and Learning from Data" (not free; only the OCW problem set above).
- Calafiore & El Ghaoui, Axler, Lay: not opened.
- WebSearch hits for the HW numbers (e.g. (-1,2),(0,1),(1,4); Phi=[[1,1],[2,2]]) returned generic least-squares pages only; I did not open them.

## Per problem
- P1 (transposes): VMLS p.~? transpose defined in Ch.6; no match for these matrices. Not found in VMLS, CS229, DL.
- P2 (x=(1,-2,2), y=(2,1,0), inner product, norms, orthogonal): VMLS p.68 defines orthogonal ("the vectors are said to be orthogonal"). Specific vectors not found in VMLS, CS229, DL.
- P5 (inverses): VMLS p.212 ("A square matrix that is not invertible is called singular"); CS229 sec 3.7 "The Inverse". Numeric matrices not found anywhere.
- P8 (A=[[1,-1],[1,0],[1,1]], A^T A, (A^T A)^-1): VMLS Gram matrix p.191 and left inverse (A^T A)^-1 A^T (Ch.11). The specific A not found by text search in VMLS. Same A is the design matrix of P17 data, a standard textbook line-fit setup.
- P9 (feature map phi(x)=(1,x,x^2), "linear in theta"): VMLS Ch.13 basis functions, e.g. polynomial fit; p.285 "basis function ... x^3". Concept matches (linear in parameters, nonlinear basis); numeric example not found. VMLS calls them basis functions, not feature map.
- P12 (h=x^T Q x - 2 b^T x, gradient): CS229 sec 4.3 "Gradients and Hessians of Quadratic and Linear Functions" (p.~22-23) and sec 3.11 quadratic forms; VMLS p.46 gradient, p.238 "gradient ... = 0". Numbers (Q=[[3,1],[1,2]]) not found.
- P17 (line fit through (-1,2),(0,1),(1,4)): VMLS Sec 13.1 p.259-260 "Straight-line fit", with "parameters in the optimal straight-line fit ... (A^T A)^-1 A^T y". MIT 18.06SC Ses2.3 (Strang 4.3 #17-22): same structure, different data, e.g. "b = 7 at t = -1, b = 7 at t = 1, and b = 21 at t = 2" (quote shortened). The exact HW data not found.
- P20 (Phi^T Phi singular, ridge lambda=5): VMLS Sec 15.? p.327-328 Tikhonov regularized inversion; "is therefore always invertible (provided lambda > 0)" and x = (A^T A + lambda I)^-1 A^T y. Phi=[[1,1],[2,2]] not found. CS229 note and DL ch.2: no ridge/regularization text (searched).
- P21 (mean vector, covariance of four 2-D points, denominator 4): VMLS Exercise 10.16 p.203 "Covariance matrix" (defines k x k covariance of vectors; different object). No mean-vector/ covariance-with-denominator-N example with these points. Not found in CS229, DL.

## Derivations
- ML = least squares under Gaussian noise: not found in VMLS (searched "likelihood", "posteriori", "prior distribution": zero hits), CS229 linalg review (only says its objective equals the least-squares one, p.13), DL ch.2 (no hits). Not a linear-algebra-book topic; look in Bishop PRML, Murphy, or CS229 main notes.
- Ridge = MAP with Gaussian prior (lambda = sigma^2/b^2): not in VMLS (no Bayesian text; ridge appears only as Tikhonov "minimize ||Ax-y||^2 + lambda||x||^2"). Berkeley CS189 lec 13 (summary only): "Assign a prior probability on w': a Gaussian centered at 0", but it gives no explicit lambda = sigma^2/b^2 formula.

## Conclusion
None of VMLS, CS229 LA review, Deep Learning Ch.2 or the MIT 18.06 line-fit set contains the HW numbers verbatim. Closest conceptual matches: P17/P8 to VMLS Ch.13 and Strang 4.3; P20 to VMLS Sec 15.? Tikhonov; P12 to CS229 sec 4.3. The numbers look instructor-made.
