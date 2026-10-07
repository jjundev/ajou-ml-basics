# Textbook origin of Homework #1 linear algebra problems P1-P9 (Ajou ML, Prof. Bang Chul Jung)

## Is there a specific textbook whose exercises match P1-P9 (MML, Strang, Lay, Bishop, Murphy, CS229 review)?

### Takeaway
I could not verify any exact source. After about 10 tool calls, no page text matching these problems or numbers was retrieved. P1-P8 look like generic drill problems, and P9 looks like standard polynomial-basis linear regression. The only defensible statement is "topical match, source unverified".

### Cited Findings
- The MML book site lists no per-chapter exercise list. It points to an instructor's manual from Cambridge University Press with exercise solutions, plus an Overleaf document of additional exercises with solutions. The Overleaf link was not opened. — [mml-book.github.io](https://mml-book.github.io/)
- A web search found MML Chapter 2 (Linear Algebra) includes a Linear Independence section. The search summary gave no problem-level details. — [MML PDF copy at NEU](https://course.ccs.neu.edu/ds4420/readings/mml-book.pdf)
- Generic web sources describe the polynomial design matrix Phi with columns [1, x, x^2, ...] and the model f(x)=w^T phi(x) as non-linear in x but linear in the parameters. This is the standard rationale for P9's "why is this linear regression" question, and it appears across many sources. — [Princeton COS324 basis functions](https://www.cs.princeton.edu/courses/archive/fall18/cos324/files/basis-functions.pdf); [Edinburgh MLPR w1b](https://www.inf.ed.ac.uk/teaching/courses/mlpr/2016/notes/w1b_linear_regression.html)
- Searches for the Ajou course syllabus (English and Korean) returned no relevant result. No public syllabus or textbook list was found for this course. — [search results with no hit; the closest unrelated KOCW listings are at kocw.net](https://www.kocw.net:444/home/common/contents/syllabus/1424075_2022011411317287.pdf)
- Search for the Sarrus example with MML-style matrices found no MML text. It returned only generic Sarrus-rule pages. — [Rule of Sarrus (GeoGebra)](https://mat.geogebra.org/m/ud2reec5)

### Inferences
These are my own reasoning, not verified facts. Confidence is low throughout.
- P1 (transpose): generic. Any intro linear algebra text. No specific source.
- P2 (inner product, norms, orthogonality): generic. It maps topically to MML Sec 3.1-3.2 (norms, inner products), but this was not verified.
- P3 (AB vs BA): generic. It maps topically to MML Sec 2.2.1 (matrix multiplication is not commutative), but the specific matrices were not matched.
- P4 (determinants, first-row expansion and Sarrus): topical match to MML Sec 4.1 (Laplace expansion and Sarrus' rule). Sarrus is named explicitly in MML, which makes it a plausible source, but the matrices were not matched. This is the strongest topical hint. Note that the 3x3 matrix [[1,3,5],[2,4,6],[0,2,4]] has dependent columns (column3 = 2*column2 - column1), so its determinant is 0. The instructor likely chose it deliberately.
- P5 (inverses): generic. It maps topically to MML Sec 2.2.2 (inverses) and Gaussian elimination (Sec 2.3).
- P6 (linear independence of three vectors): topical match to MML Sec 2.5 (linear independence). By my arithmetic x3 = 2*x1 - x2, so the set is dependent. The vectors were not matched to any book example.
- P7 (linear combination, solve a linear system): generic. It maps topically to MML Sec 2.4-2.5.
- P8 (A^T A, determinant, inverse): this is the normal-equation pattern from linear regression (A^T A)^{-1} A^T y. It is topical to MML Sec 9.2 (maximum likelihood estimation) and to Bishop PRML Sec 3.1.1. It is probably designed as a bridge to the regression part of the homework.
- P9 (feature map and feature matrix Phi): the notation phi(x) and Phi matches Bishop PRML Ch.3 (basis functions phi, design matrix Phi) and MML Ch.9 (Phi, "linear regression with nonlinear features"). Both use "Phi" for the feature or design matrix. This is notation fit only. No exact match was verified.
- Because homework values were possibly altered by the instructor, exact numeric matching was not expected anyway.

### Gaps
- Large PDF copies of MML could not be fetched. WebFetch failed with "maxContentLength size of 10485760 exceeded" on both mml-book.github.io/book/mml-book.pdf and the NEU copy. I did not download the files, because that needs user permission. Consequently MML's actual Ch.2 exercises (Sec 2.5) and Ch.4 Sarrus example were never read, and no claim of exact match can be made.
- Suggested next step for the user: download the MML PDF locally with permission and search for "Sarrus", "linearly independent" and "Phi". Also open the additional exercises on Overleaf (https://www.overleaf.com/read/jvnwngmkpckc).
- The Ajou course syllabus and reference textbooks were not publicly findable by web search. The Ajou Blackboard / university syllabus portal (login-restricted) is the likely place.
- Not checked: Strang, Lay, Murphy, and the CS229 linear algebra review by Kolter. No search targeted them specifically.
- The accuracy of any per-problem mapping above is unverified. Treat them as hypotheses for the instructor's likely sources.
