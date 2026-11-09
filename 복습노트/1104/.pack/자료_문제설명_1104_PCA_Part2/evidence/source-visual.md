# source_visual — 1104 PCA Part2 문제설명 (재선정 10문항)

대조 자료: 교과서/Mathematics_for_Machine_Learning.pdf 해당 쪽을 pdftoppm(80dpi)으로 렌더링(evidence/pages/*.png)하고 PyMuPDF 텍스트 추출로 문장·수치를 대조했다. 그림은 카드가 쓰는 .pack/figures_1104/mml-figure-10-5·10-10·10-12.png를 직접 열람해 교과서 그림과 대조했다.

| 문항 | 원천(PDF쪽) | 대조 결과 |
|---|---|---|
| p1 | Example 10.2, 그림 10.5, PDF 330–331 | 그림 10.5(a) 고윳값 200개(첫 값 약 46, 둘째 약 32), (b) captured variance 0–525 곡선과 카드 PNG 일치. 원문 인용 “only a few of them … differs significantly from 0” 일치. V_M=Σλ_m은 식 (10.24)와 일치. 카드 소문항 a,b. |
| p2 | Example 10.3, 그림 10.10, PDF 338–339 | 0(파랑)·1(주황) 산점도와 빨간 안내선 8개, 인용 “relatively clear separation … variation within the set of “0” is significantly greater” 일치. 소문항 a,b. |
| p3 | Example 10.4, 그림 10.12, PDF 344–345 | 5,389장 학습, 테스트 4장, PCs 1/10/100/500 행과 카드 PNG 일치. 그림 10.13 설명(약 550개면 학습 데이터 완전 복원, 가장자리 픽셀 늘 검정)과 식 (10.62)를 카드 조건이 문장으로 옮김. “약 400개 넘으면 거의 0”은 그림 10.13 곡선 판독(카드 조건)이며 교과서 문장에는 없음 — 조건으로 주어진 사실로 사용. 소문항 a,b,c. |
| p4 | Example 4.13, PDF 131–132 | 교과서 행렬 [[1,0,1],[−2,1,0]](σ=√6,1). 카드는 [[1,1,0],[0,1,1]]로 수치 변형(“변형”으로 명시). Step 1–3(AᵀA 고유기저→Σ→u=Av/σ) 구조와 인용 일치. 소문항 a–d. |
| p5 | Example 4.15(+4.14, 그림 4.10), PDF 133, 138–139 | 평점표 [[5,4,1],[5,5,0],[0,0,5],[1,0,4]], σ=9.6438/6.3639/0.7056, U·V 소수 넷째 자리 값이 그림 4.10과 일치. (4.100b) A1 셋째 열 (0.1215,0.1303,0.0170,0.0274), (4.102) Â(2) 셋째 열 (1.0244,−0.0250,4.9724,4.0278), 인용 “ignore the contribution of A3” 일치. 교과서는 A_i=u_iv_iᵀ(σ 미포함)로 표기 — 설명 pitfall에 밝힘. 소문항 a–c. |
| p6 | Exercise 3.7, PDF 103 | 원문 (a) “π is a projection iff id_V−π is a projection”. 카드는 두 방향 (a),(b)로 분할. 원문 (b)(Im·ker 계산)는 카드에 없음 — 설명에도 상·핵을 쓰지 않음. |
| p7 | Exercise 4.8, PDF 144 | [[3,2,2],[2,3,−2]] “Find the SVD” 일치. 카드는 AAᵀ에서 시작하는 a–d로 구성. |
| p8 | Exercise 4.9, PDF 144 | [[2,2],[−1,1]] 일치. 카드 a,b와 AAᵀ 판정 c 추가. |
| p9 | Exercise 4.10, PDF 144 | [[3,2,2],[2,3,−2]] rank-1 approximation 일치. 카드 a,b와 Frobenius 판정 c 추가. |
| p10 | Exercise 4.12, PDF 144 | max‖Ax‖₂/‖x‖₂=σ1 (Theorem 4.24) 일치. 카드는 기저 전개 a–d로 분할, 조건에 AᵀAv_i=σ_i²v_i 제공. |

모든 문항의 원문 인용(original_html)과 그림·표(figures_html: p1–p3 그림, p5 표 3개)는 stage의 원문 탭·문제 패널에 그대로 표시되는지 browser 단계에서 확인한다.
