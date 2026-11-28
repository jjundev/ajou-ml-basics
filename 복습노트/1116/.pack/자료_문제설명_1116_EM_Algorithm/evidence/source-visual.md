# 1116 EM Algorithm 원천 대조 (source_visual)

- 검토 대상: `복습노트/1116/복습문제_1116_EM_Algorithm-문제.pdf` (8쪽, `evidence/source-pages/page-1.png`~`page-8.png`) ↔ `source.json` (`복습노트/1116/.pack/복습문제_1116_EM_Algorithm.cards.json`) 및 MML 원천.
- 대조 결과: **8문항 전체 일치 (pass)**

| 문항 | PDF 페이지 | 제목·출처 | 조건·표·식·소문항 대조 | 비고 |
|---|---|---|---|---|
| P1 | 1쪽 (`page-1.png`) | MML Example 11.5 (교과서 360쪽 / PDF 366쪽) | $N=7$, $\pi_k=1/3$, $N_1=2.058, N_2=2.008, N_3=2.934$, $\pi_k^{\text{new}}=N_k/N$, 소문항 `(a)`, `(b)` 일치 | 그림·표 없음 |
| P2 | 2쪽 (`page-2.png`) | MML Example 11.3 변형 (교과서 355쪽 / PDF 361쪽) | $x_n\in\{-4,-2,-1,0,2,4,6\}$, $7\times3$ 분수 책임도 표, $\mu_k^{\text{new}}=\frac{1}{N_k}\sum_{n=1}^7 r_{nk}x_n$, 소문항 `(a)`, `(b)` 일치 | 표 7행 4열 일치 |
| P3 | 3쪽 (`page-3.png`) | MML Example 11.3 (교과서 353·355쪽 / PDF 359·361쪽) | $x_n\in\{-3,-2.5,-1,0,2,4,5\}$, $\mu=(-4,0,8)$, 반올림 책임도 표, 소문항 `(a)`, `(b)` 일치 | 표 7행 4열 일치 |
| P4 | 4쪽 (`page-4.png`) | MML Example 11.4 (교과서 357–358쪽 / PDF 363–364쪽) | $(N_1,N_2,N_3)=(2.058,2.008,2.934)$, $\mu^{\text{new}}=(-2.7,-0.4,3.7)$, $\sigma^2=(1,0.2,3)$, 반올림 표, 소문항 `(a)`, `(b)` 일치 | 표 7행 4열 일치 |
| P5 | 5쪽 (`page-5.png`) | MML Example 11.6 (교과서 361–362쪽 / PDF 367–368쪽, 식 11.57) | 수렴 GMM $0.29\mathcal{N}(-2.75,0.06)+0.28\mathcal{N}(-0.50,0.25)+0.43\mathcal{N}(3.64,1.63)$, 초기값 $\mu=(-4,0,8),\sigma^2=(1,0.2,3),\pi_k=1/3$, 소문항 `(a)`, `(b)` 일치 | 그림·표 없음 |
| P6 | 6쪽 (`page-6.png`) | MML Example 5.11 (교과서 154쪽 / PDF 160쪽, 식 5.75–5.83) | $\boldsymbol{\theta}\in\mathbb{R}^D,\mathbf{y}\in\mathbb{R}^N,\boldsymbol{\Phi}\in\mathbb{R}^{N\times D}$, $L(\mathbf{e})=\|\mathbf{e}\|^2$, $\mathbf{e}=\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}$, 행벡터 미분 관례 및 야코비안 정의 명시, 소문항 `(a)`, `(b)` 일치 | 그림·표 없음 |
| P7 | 7쪽 (`page-7.png`) | MML Example 11.4 변형 (교과서 357–358쪽 / PDF 363–364쪽) | $x_n\in\{-4,-2,-1,0,2,4,6\}$, 분수 표, $N=(5/2,2,5/2)$, $\mu^{\text{new}}=(-13/5,1/4,22/5)$, $\sigma^2=(2,1/2,3)$, 소문항 `(a)`, `(b)` 일치 | 표 7행 4열 일치 |
| P8 | 8쪽 (`page-8.png`) | MML Exercise 5.6 (교과서 171쪽 / PDF 177쪽) | $f(\mathbf{t})=\sin(\log(\mathbf{t}^\top\mathbf{t}))$, $g(\mathbf{X})=\operatorname{tr}(\mathbf{A}\mathbf{X}\mathbf{B})$, 크기 $\mathbf{t}\in\mathbb{R}^D,\mathbf{A}\in\mathbb{R}^{D\times E},\mathbf{X}\in\mathbb{R}^{E\times F},\mathbf{B}\in\mathbb{R}^{F\times D}$, 행벡터·행렬 미분 관례 명시, 소문항 `(a)`, `(b)`, `(c)` 일치 | 그림·표 없음 |
