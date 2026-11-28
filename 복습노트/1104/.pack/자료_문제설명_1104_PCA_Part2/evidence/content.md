# 1104 PCA Part2 문제설명 경량화 내용·수식 검토 (p1~p10)

대상: `tmp/ml-problem-explain/streamline-1104/review-1104-PCA_Part2/explanations/p1.html` ~ `p10.html` (총 10문항, 30소문항) 및 조립된 stage HTML/MD.
대조 자료: `복습노트/1104/복습문제_1104_PCA_Part2-문제.pdf` (10쪽, SHA-256 `0994b94c2727b5a03c4634aa3fc3d072b855febe96d9a4ed0ff415ac1897ad43`), `복습노트/1104/정리노트_1104_PCA_Part2.html`, `evidence/independent.md`, `evidence/calculation.txt`, `evidence/author_results.txt`.

## 구조·형식 확인 (전 문항 공통)
- 직계 구역 순서: `understand(풀이 목표)` → `recall(풀이 단서)` → `start(첫 단계)` → `solve(핵심 풀이 + final-answer(최종 답))` → `verify(답 확인)` → `pitfall(주의할 점, data-omit-retry="")` → `sum[hidden]` → `provenance` → `terms[data-summary-terms=""]`.
- `data-explanation="retry"` 제거, `<details>`·인라인 `style`·`on*`·보존 푸터 없음.
- 모든 `data-subpart`(`a`,`b`,...)가 `solve`와 `verify` 양쪽에 1:1 보존됨.
- `check_vector_derivatives.py`: PASS (`errors: []`).

## 문항·소문항별 내용 검토
- **P1 (`p1:a`, `p1:b`)**: $V_M-V_{M-1}=\lambda_M$ 차분 및 그림 10.5 좌($\lambda_1\approx 46$, $\lambda_2\approx 32$, $m\approx 50$ 약 2~3, $m\approx 150\sim 200$ 1 미만)·우(50칸 증가량 $[0,50]$ 약 370 vs $[150,200]$ 약 20) 대조 일치. `final-answer` 및 `.sum` 동기화 완료.
- **P2 (`p2:a`, `p2:b`)**: 그림 10.10의 두 숫자 무리 분리 및 중심으로부터의 퍼짐 폭(집단 내 분산: 숫자 0 > 숫자 1) 판정, 8개 빨간 안내선 검산 일치. `p2:b` 불필요 표 제거 후 핵심 2문단으로 압축.
- **P3 (`p3:a`, `p3:b`, `p3:c`)**: 그림 10.12 $M=1,10,100,500$ 변화표, $M=784$에서 $\mathbf B\mathbf B^\top=\mathbf I_{784}$ 및 빈 합 $J_{784}^\star=0$, $M=500$ 단조성·가장자리 0분산 픽셀·테스트 4장 시각 비교 분리 서술 모두 일치.
- **P4 (`p4:a`, `p4:b`, `p4:c`, `p4:d`)**: $\mathbf A^\top\mathbf A$ 여인수 전개 → 고윳값 $3,1,0$ → 정규화 $\mathbf V(3\times 3)$, $\sigma_1=\sqrt3,\sigma_2=1$, $\mathbf\Sigma(2\times 3)$, $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$ → $\mathbf U(2\times 2)$. `calculate.py` 오차 $1.11\times 10^{-16}$, `check.py` 정확 확인.
- **P5 (`p5:a`, `p5:b`, `p5:c`)**: $\sigma_1 v_{1,3}\mathbf u_1=(1.1719,1.2570,0.1640,0.2646)^\top$, $\hat{\mathbf A}(2)$ Chandra 열 $(1.0246,-0.0250,4.9727,4.0280)^\top$, $\sigma_3^2/134\approx 0.37\%$ 판정 일치. 영화 행 첨자를 $k$로 통일하고 불필요한 에카르트-영 정리를 덜어냄.
- **P6 (`p6:a`, `p6:b`)**: $(I-\pi)^2(\mathbf x)=\mathbf x-2\pi(\mathbf x)+\pi(\pi(\mathbf x))=(I-\pi)(\mathbf x)$ 5줄 유도 및 $\rho=\mathrm{id}_V-\pi$에 (a) 적용해 $\mathrm{id}_V-\rho=\pi$ 증명. 중복 치환 표 제거.
- **P7 (`p7:a`, `p7:b`, `p7:c`, `p7:d`)**: $\mathbf A\mathbf A^\top=[[17,8],[8,17]]$ → $\sigma_1=5,\sigma_2=3$, $\mathbf u_1,\mathbf u_2$ → $\mathbf v_1,\mathbf v_2=\mathbf A^\top\mathbf u_i/\sigma_i$ → 직교 $\mathbf v_3=\frac13(2,-2,-1)^\top$ → $\mathbf A\mathbf v_3=\mathbf 0$ 및 $\mathbf\Sigma$ 0열 확인. `calculate.py` 오차 $4.44\times 10^{-16}$.
- **P8 (`p8:a`, `p8:b`, `p8:c`)**: $\mathbf A^\top\mathbf A=[[5,3],[3,5]]$ → $\mathbf V$, $\sigma_1=2\sqrt2,\sigma_2=\sqrt2$, $\mathbf U=\operatorname{diag}(1,-1)$, $\mathbf A\mathbf A^\top=\operatorname{diag}(8,2)$ 고유벡터·고윳값 $\sigma_i^2$ 판정 일치. `calculate.py` 오차 0.
- **P9 (`p9:a`, `p9:b`, `p9:c`)**: $\sigma_1=5, \mathbf u_1, \mathbf v_1$, $\mathbf A_1=\frac52[[1,1,0],[1,1,0]]$, $\|\mathbf A-\mathbf A_1\|_F^2=9=\sigma_2^2$ 일치. `calculate.py` 및 `check.py` 정확 확인.
- **P10 (`p10:a`, `p10:b`, `p10:c`, `p10:d`)**: 기저 전개 $\mathbf x=\sum c_i\mathbf v_i$ → $\|\mathbf A\mathbf x\|_2^2=\sum\sigma_i^2 c_i^2$ → $\sigma_i^2\le\sigma_1^2$ 상한 → $\mathbf x=\mathbf v_1$ 등호 → 최댓값 $\sigma_1$. 일반 증명 검증 원칙에 따라 `verify`를 조건·정규직교성·도달성 점검으로 정리.
