# Other course sources (non-MML) - search notes, 2026-10-07

Result: NO verbatim or near-identical match found for any of the 11 items. Search depth was limited (about 10 WebSearch queries, 5 fetches). The search tool returns AI-written summaries that echo the query numbers, so those summaries were NOT treated as evidence of a match.

## Per-problem
| Item | Result |
|---|---|
| LS fit (-1,2),(0,1),(1,4), Phi^T Phi=diag(3,2) | No match after searching generic polynomial-regression notes (mlweb.loria.fr, UCLA handout, Scribd hits, titles only). Not opened. |
| Singular Phi=[[1,1],[2,2]], y=(3,6), ridge lambda=5 | No match. Opened Berkeley CS189 s16 lec13 (people.eecs.berkeley.edu/~jrs/189s16/lec/13): only generic text ("K is singular if n > d" ... no solution if lambda=0); no numeric example. Wuerzburg session6.pdf returned a login page; QMUL link 404. MIT 6.390 spring26 lecture02.pdf fetched but text extraction gave nothing usable (unverified). |
| A=[[1,-1],[1,0],[1,1]], A^T A and inverse | Not searched separately (covered by the LS item); no hit. |
| phi(x)=(1,x,x^2) "why linear regression" | Only generic polynomial-regression notes seen; no exact problem. |
| h(x)=x^T Q x - 2b^T x, Q=[[3,1],[1,2]] | No match. Hits were NTNU TMA4180 oving2/3, NTHU CS5321 midterm, MIT 15.084 lec4 - listed in search results only, NOT opened; generic quadratic minimization with different numbers presumably. |
| p(z)=c exp(-1/2(4z^2-8z+7)) | No match. Imperial ibug "notes_completing_the_square.pdf" (ibug.doc.ic.ac.uk) appeared in results; not opened. |
| Gaussian mu=(1,-1), Sigma=[[2,1],[1,2]] density | No match. |
| Product of N(0,diag(1,2)) and N(1,[[2,1],[1,2]]) | No match. Cambridge 4F13 "gaussian and matrix equations.pdf" (mlg.eng.cam.ac.uk) fetched, but PDF text was compressed/unreadable via WebFetch (saved to tool-results dir, not parsed) - UNVERIFIED. It likely only has the general product formula. |
| MAP vs ML y_n=theta+eps, prior N(1,1), obs 2,3,4 | No match. Generic MAP/MLE pages only (IITK CS771 slides, HMC notes) - not opened. |
| Four points (1,1),(1,3),(3,3),(3,5) mean/cov | No match (RWTH solution04.pdf, SFU ch3 etc. appeared; not opened). |
| Jacobian f(u,v)=[u+2v;3u-v], grad u^2+3v^2-2u+4v | No match (Hamburg/Middlebury exercise sheets in results; not opened; the answer text merely computed the derivatives). |

## Not covered (could not do)
- Stanford CS229, CS168, EE263, Caltech CS156, CMU 10-601/701, KAIST/SNU/Postech, Korean 연습문제 sources: only one Korean query was run (no relevant hit); the others were not targeted individually.
- Geron "Hands-On ML" has no such problem sets (it is code-oriented); not searched in depth.
- No pdf.js extraction was done in the Browser pane.

## LLM-generated-variant assessment
Not provable from this search. Observation only: the numbers are tiny, hand-computable choices (diag Phi^T Phi, Sigma=[[2,1],[1,2]], points forming a rectangle/parallelogram, completing-the-square with 4z^2-8z+7 => mean 1, var 1/4), typical of textbook-style variants/exam drills, and no public origin was found, consistent with instructor-authored or generated variants. Weak evidence only.
