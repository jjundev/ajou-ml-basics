# 1116 EM Algorithm 문제설명 내용 검토 (content)

- 검토 대상: `explanations/p1.html`~`p8.html`, stage `문제설명_1116_EM_Algorithm.html`, `.pack/문제설명_1116_EM_Algorithm.md`, `audit.md`.
- 구조·유형 형식: 8문항 모두 `understand(풀이 목표)` → `recall(풀이 단서)` → `start(첫 단계)` → `solve(핵심 풀이)`(내부 마지막 자식으로 `section.final-answer` 최종 답) → `verify(답 확인)` → `pitfall(주의할 점, data-omit-retry="")` 순서를 준수하고 `retry` 구역·`<details>`·인라인 `style`·`on*` 속성을 제거함.
- 용어·출제근거·요약: 문항별 `<div class="sum" hidden>`은 본문·최종 답과 동기화되었으며, `<section data-problem-panel="terms" data-summary-terms="">`에는 실제 풀이에 쓰는 용어만 남김. `provenance` 패널은 MML 원천·교안 페이지·실존 정리노트 앵커와 일치함.
- 미분 관례(`vector-derivative-convention.md`): `P6`과 `P8`은 원문이 명시한 수업 행벡터 미분 관례($\mathbb{R}^{1\times D}$), 출력×입력 야코비안($\mathbb{R}^{N\times D}$), 원소별 같은 자리 행렬 미분($\mathbb{R}^{E\times F}$)을 일관되게 유지함(`check_vector_derivatives.txt` pass).
- 감사 조치: `audit.md`의 Important 1건(`p8` $(\mathbf{A}\mathbf{X}\mathbf{B})_{ii}$의 $(\mathbf{A}\mathbf{X})_{il}$ 중간 전개 복원)과 Minor 2건(`p3` 양쪽 누락 설명 보완, `p7` 요약의 미정의 기호 제거)을 모두 수정 후 재빌드·재검토함.

| 문항·소문항 | 풀이 유형·형식 | 최종 답 위치·완결성 | 답 확인·요약·MD 일치 | 판정 |
|---|---|---|---|---|
| `p1:a`, `p1:b` | 수치 표(`table-wrap`) + 비율 합/비교 | `solve` 끝 `final-answer`에 $(0.294,0.287,0.419)$, 합 $1$, 성분 $3$ 완비 | $\times 7$ 역산·$\sum N_k=7$ 확인, `.sum`/MD 일치 | pass |
| `p2:a`, `p2:b` | 수치 표(`table-wrap`, 분수) | `final-answer`에 $N_k=(5/2,2,5/2)$, $\mu_k^{\text{new}}=(-2.6,0.25,4.4)=(-13/5,1/4,22/5)$ 완비 | 행 합 $1$·가중 편차 합 $0$ 확인, `.sum`/MD 일치 | pass |
| `p3:a`, `p3:b` | 수치 표(`table-wrap`, 반올림) | `final-answer`에 $(-2.70,-0.40,3.70)$, 이동 $(1.30,0.40,4.30)$, 성분 $3$ 완비 | $\sum N_k=7$·관측 구간 내 확인·반올림 전 순서 일치, `.sum`/MD 일치 | pass |
| `p4:a`, `p4:b` | 수치 표(`table-wrap`) + 교과서 차이 주석 | `final-answer`에 $(0.15,0.44,1.53)$, 성분 $1$·$3$ 감소/성분 $2$ 증가 완비 | 최대 편차 제곱 상한·반올림 전 증감 확인, 교과서 $0.14$ 차이 일관 설명, `.sum`/MD 일치 | pass |
| `p5:a`, `p5:b` | 수치 표 2종(`table-wrap`) | `final-answer`에 합 $1$, $\sigma_k\approx(0.24,0.50,1.28)$, 성분 $3$(이동 $4.36$), 성분 $2$ 증가 완비 | 제곱 역산·초기값 대비 부등식 확인, `.sum`/MD 일치 | pass |
| `p6:a`, `p6:b` | 유도형(`ol.deriv` 6줄) + 차원 분석 | `final-answer`에 $-2\mathbf{e}^\top\boldsymbol{\Phi}$ 및 $1\times N, N\times D, 1\times D$ 완비 | 변수 $\boldsymbol{\theta}\in\mathbb{R}^D$, 결과 $1\times D$, 곱 $(1\times N)(N\times D)$ 차원·$N=D=1$ 검산, `.sum`/MD 일치 | pass |
| `p7:a`, `p7:b` | 수치 표(`table-wrap`, 분수) | `final-answer`에 $(36/25,19/16,56/25)$, 성분 $1$·$3$ 감소/성분 $2$ 증가 완비 | $\mathbb{E}[x^2]-\mu^2$ 분수 검산·통분 비교 확인, `.sum`/MD 일치 | pass |
| `p8:a`, `p8:b`, `p8:c` | 유도형(`ol.deriv` 4줄+6줄) + 차원 읽기 | `final-answer`에 $\frac{2\cos(\log(\mathbf{t}^\top\mathbf{t}))}{\mathbf{t}^\top\mathbf{t}}\mathbf{t}^\top$, $\mathbf{A}^\top\mathbf{B}^\top$, $1\times D, E\times F$ 완비 | $(\mathbf{A}\mathbf{X})_{il}$ 전개 복원, 1차원 검산·전치 크기 일치, `.sum`/MD 일치 | pass |
