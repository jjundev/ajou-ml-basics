# 본문–요약 수동 감사 0923

범위: 이 날짜의 정리노트·복습문제·문제설명 실제 본문과 실제 요약. 외부 원자료 전체의 독립 학술 검증은 아니다. 교수 일화·비유·반복은 원리/조건과 다른 새 핵심이 없으면 생략한다. 질문·풀이·정답 본문은 이번 작업에서 보존했다.

| 자료·토픽 | 구분 | 실제 본문 주장 | 대응하는 현재 요약 문장 / 생략 이유 | 보완 전 | 판정 |
|---|---|---|---|---|---|
| 문제설명_0923_Linear_Regression.html#p1 | 일반 | 원점직선, XTX21,XTy40,θ40/21, SSE38/21; 고정분산과 분모양수 조건. | 내적은21로 양수라 역수가 존재해요. | 기존 반영 | pass |
| 문제설명_0923_Linear_Regression.html#p1 | 주의 | 원점직선, XTX21,XTy40,θ40/21, SSE38/21; 고정분산과 분모양수 조건. | 고정된 양의 가우시안 잡음 분산에서 ML과 SSE 최소화가 같고, 분모 $\sum x_n^2=21>0$라 해가 유일해요. 이 모델은 상수항이 없으므로 입력 앞에 1을 새로 붙이지 않아요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0923_Linear_Regression.html#p2 | 일반 | 중복입력도 각관측포함, XTX6,XTy12,θ2, 잔차직교/SSE2. | θ=2의 잔차는[-1,1,0]이에요. | 기존 반영 | pass |
| 문제설명_0923_Linear_Regression.html#p2 | 주의 | 중복입력도 각관측포함, XTX6,XTy12,θ2, 잔차직교/SSE2. | 입력이 같은 두 $x=1$ 예제도 출력이 다르므로 각각의 관측으로 합에 포함해요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0923_Linear_Regression.html#p3 | 일반 | 3차 상수포함4성분φ2=[1,2,4,8], θ선형 내적답5. | 0제곱부터3제곱까지라4성분이에요. | 기존 반영 | pass |
| 문제설명_0923_Linear_Regression.html#p3 | 주의 | 3차 상수포함4성분φ2=[1,2,4,8], θ선형 내적답5. | 3차식은 상수항까지 특징·계수 4개예요. $x$에 대해서는 비선형이지만 계수에 대해서 선형이므로 선형회귀예요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0923_Linear_Regression.html#p4 | 일반 | 2차3성분φ3=[1,3,9], f=2−x²→−7; 0계수 특징도 보존. | 상수항부터2차항까지3성분이에요. | 기존 반영 | pass |
| 문제설명_0923_Linear_Regression.html#p4 | 주의 | 2차3성분φ3=[1,3,9], f=2−x²→−7; 0계수 특징도 보존. | 선형항 계수가 0이어도 그 특징을 벡터에서 지우지 않고 주어진 계수 순서를 보존해요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0923_Linear_Regression.html#p5 | 일반 | 행소거0=1, rankA3/augmented4, 정확해공집합; LS근사와 다름. | 독립 행소거와 rank 계산에서 rank(A)=3, 확대행렬rank=4예요. | 기존 반영 | pass |
| 문제설명_0923_Linear_Regression.html#p5 | 주의 | 행소거0=1, rankA3/augmented4, 정확해공집합; LS근사와 다름. | 모순 행 $0=1$이므로 정확한 해 집합은 $S=\emptyset$이에요. 최소제곱 근사해를 구하는 질문과 구별해요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0923_Linear_Regression.html#p6 | 일반 | 3×3 rank2, det0, 영공간 비영벡터 있으므로 역행렬 없음. | 독립 계산으로 det=0, rank=2이고 비영 영공간 벡터 [1,−2,1]이 있어요. | 기존 반영 | pass |
| 문제설명_0923_Linear_Regression.html#p7 | 일반 | GaussJordan은 [A\|I]동일행연산; inverse양곱I4와 전체네행 결과. | 결과의 행은 [0,−1,0,1], [−1,0,0,1], [1,1,0,−1], [1,1,1,−2]예요. | 기존 반영 | pass |
| 문제설명_0923_Linear_Regression.html#p7 | 주의 | GaussJordan은 [A\|I]동일행연산; inverse양곱I4와 전체네행 결과. | 같은 행연산을 $[A\mid I]$ 양쪽에 함께 적용해야 해요. 왼쪽만 바꾸거나 오른쪽 행 순서를 따로 바꾸면 역행렬이 아니에요. | unresolved → 보완 후 다시 읽음 | pass |
| 복습문제_0923_Linear_Regression.html#p1 | 일반 | 원점직선, XTX21,XTy40,θ40/21, SSE38/21; 고정분산과 분모양수 조건. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0923_Linear_Regression.html#p2 | 일반 | 중복입력도 각관측포함, XTX6,XTy12,θ2, 잔차직교/SSE2. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0923_Linear_Regression.html#p3 | 일반 | 3차 상수포함4성분φ2=[1,2,4,8], θ선형 내적답5. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0923_Linear_Regression.html#p4 | 일반 | 2차3성분φ3=[1,3,9], f=2−x²→−7; 0계수 특징도 보존. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0923_Linear_Regression.html#p5 | 일반 | 행소거0=1, rankA3/augmented4, 정확해공집합; LS근사와 다름. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0923_Linear_Regression.html#p6 | 일반 | 3×3 rank2, det0, 영공간 비영벡터 있으므로 역행렬 없음. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0923_Linear_Regression.html#p7 | 일반 | GaussJordan은 [A\|I]동일행연산; inverse양곱I4와 전체네행 결과. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 정리노트_0923_Linear_Regression.html#s0-learning-map | 일반 | 입력/고정미지계수/랜덤잡음을 구분; Gaussian NLL→정규방정식, 역행렬 조건 필요. | ML의 결과는 파라미터 벡터 하나예요. 특징에 대해 선형이면, 원래 입력에 대해 곡선이어도 선형회귀로 다룰 수 있어요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s0-learning-map | 조건·구분 | 입력/고정미지계수/랜덤잡음을 구분; Gaussian NLL→정규방정식, 역행렬 조건 필요. | 입력·특징은 모형의 재료이고, ML의 파라미터는 고정된 미지의 계수, 잡음은 계수가 정해져도 남는 확률변수예요. 가우시안 NLL의 제곱오차를 미분하면 정규방정식이 나오며 역행렬 해에는 가역성 조건이 필요해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s0-regression | 일반 | 회귀는 실수, 분류는 유한클래스 선택; 목적은 새입력 일반화. | 실수 값 하나를 맞히면 회귀, 정해진 클래스 중 하나를 고르면 분류예요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s0-formulation | 일반 | 모델·잡음 가정을 세운 formulation에서 Gaussian ML→LS 연결, 일정상 ML절반까지. | 문제를 잘 세우는 포뮬레이션이 가장 중요하고, 오늘은 가우시안 노이즈에서 ML이 최소제곱이 되는 것까지 가요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s1-det-prob | 일반 | 곡선+출력PDF인 확률모델에서 delta가 결정론적 특수경우. | 결정론적 모델은 곡선만, 확률적 모델은 곡선 위의 PDF까지 찾아요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s1-gaussian | 일반 | 잡음은 평균0분산σ² 가정, bell shape이되 항상Gaussian은 아님. | 노이즈는 평균 근처에 몰린 종 모양 가우시안이라고 가정해요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s1-gaussian | 조건·구분 | 잡음은 평균0분산σ² 가정, bell shape이되 항상Gaussian은 아님. | 이 회귀 모형에서는 잡음 평균을 0, 분산을 $\sigma^2$로 두어요. 노이즈가 항상 가우시안인 것은 아니며 샷 노이즈나 라플라스 모형 등 도메인별 예외도 있어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s1-assume | 일반 | 선형가정은 생성사실 증명 아님, linear in θ의 의미. | 선형회귀는 "선형 함수 더하기 노이즈일 거야"라는 가정이지, 사실 확인이 아니에요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s1-assume | 조건·구분 | 선형가정은 생성사실 증명 아님, linear in θ의 의미. | 선형이라는 말은 계수 $\boldsymbol\theta$에 대한 선형성이에요. 데이터에 잘 맞는다는 사실을 실제 생성 과정이 선형이었다는 증명으로 바꾸지 않아요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s1-likelihood | 일반 | 같은 D벡터 내적은 스칼라평균, 고정조건에서 잡음만 랜덤; 분산으로 불확실성 표현. | 선형회귀의 우도는 평균이 내적값, 분산이 노이즈 분산인 가우시안이에요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s1-likelihood | 조건·구분 | 같은 D벡터 내적은 스칼라평균, 고정조건에서 잡음만 랜덤; 분산으로 불확실성 표현. | 길이 $D$의 두 벡터 내적은 스칼라 평균이고, 입력과 계수·함수를 정하면 불확실성은 잡음에서만 와요. 평균만 내는 결정론적 예측과 분산까지 주는 확률적 예측을 구분해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s1-features | 일반 | 다항식 입력확장 φ(x)도 θ에 선형이므로 회귀; 0.3³=.027 수정 포함. | $\boldsymbol{\theta}$에 대해 선형이면 $x$에 대해 비선형이어도 선형회귀예요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s2-dataset | 일반 | 열입력을 행으로 전치해 XN×D, θD×1, 출력/잡음N×1; plate는 N반복. | 짝지은 데이터 $N$개를 행렬로 쌓으면 모델 전체를 식 한 줄로 쓸 수 있어요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s2-dataset | 조건·구분 | 열입력을 행으로 전치해 XN×D, θD×1, 출력/잡음N×1; plate는 N반복. | $\mathbf X$는 각 행이 입력 전치인 $N\times D$, $\theta$는 $D\times1$, 출력과 잡음은 $N\times1$이에요. $D\times N$으로 열을 나란히 세운 행렬은 한 번 전치해야 이 모델식에 맞아요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s2-iid | 일반 | iid는 잡음, y평균은 각입력마다 달라 동일분포아님; 조건부독립이 우도곱 근거. | 노이즈가 i.i.d.라서 $y_n$이 입력이 주어졌을 때 조건부 독립이에요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s2-iid | 조건·구분 | iid는 잡음, y평균은 각입력마다 달라 동일분포아님; 조건부독립이 우도곱 근거. | 동일 분포인 것은 잡음 $\epsilon_n$이에요. $y_n$은 입력마다 평균 $\mathbf x_n^\top\theta$가 달라 일반적으로 동일 분포가 아니며, 주어진 입력 아래 조건부 독립이어서 우도를 곱해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s2-nll | 일반 | 우도max→-log min, 공통분산을 계수와 무관하게 고정하여 상수와 양배율 제거. | 가우시안 노이즈에서 우도를 최대화하는 것은 예측치와 실측값의 제곱 거리를 최소화하는 최소제곱과 같아요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s2-nll | 조건·구분 | 우도max→-log min, 공통분산을 계수와 무관하게 고정하여 상수와 양배율 제거. | 공통 가우시안 분산 $\sigma^2$를 $\theta$와 무관하게 두고 $\theta$만 바꿔요. NLL에서 계수와 무관한 상수 및 양의 배율을 제외해도 최소점은 같아요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s2-ml-erm | 일반 | Gaussian ML의 NLL과 squared ERM은 양상수배이므로 동일최소점; 치우친잡음 예는 제한된스케치. | 평균이 0인 가우시안 노이즈에서는 데이터를 그대로 믿는 게 최선이라, ML 해와 제곱 손실 ERM 해가 같아요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s2-ml-erm | 조건·구분 | Gaussian ML의 NLL과 squared ERM은 양상수배이므로 동일최소점; 치우친잡음 예는 제한된스케치. | 계산상의 이유는 $L$과 제곱손실 $R_{\mathrm{emp}}$가 양의 상수 배만 달라 같은 최소점을 갖는다는 것이에요. 치우친 잡음에서 관측을 옮겨 본다는 이야기는 교수님이 정확한 설명이 아닌 직관용 스케치로 한정했어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s2-ml-erm | 주의 | 비평균0 잡음의 y−λ 비유는 정확한설명이 아니라고 한정한 직관. | 치우친 잡음에서 관측을 옮겨 본다는 이야기는 교수님이 정확한 설명이 아닌 직관용 스케치로 한정했어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s3-normal-eq | 일반 | 스칼라손실의 행미분을0으로 정규방정식; full column rank일때 PD Hessian과 유일전역최소. | 손실을 θ로 미분해 0이 되는 곳을 찾으면 정규방정식이 나와요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s3-normal-eq | 조건·구분 | 스칼라손실의 행미분을0으로 정규방정식; full column rank일때 PD Hessian과 유일전역최소. | $L:\mathbb R^D\to\mathbb R$의 이 표기에서 미분은 $1\times D$ 행벡터예요. $\mathrm{rk}(\mathbf X)=D$이면 $\mathbf X^\top\mathbf X$와 Hessian이 양의 정부호라 가역이고, 정상점이 유일한 전역 최소점이에요. rank 조건은 슬라이드에 있고 수업에서는 말로 풀지 않았어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s3-pinv | 일반 | 역행렬이 존재하는 XTX를 써 X+ D×N, θ=X+y D×1; 실제계산은 연립계 가능. | 선형회귀(최소제곱)의 해는 데이터 행렬의 유사역행렬을 y에 곱한 거예요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s3-pinv | 조건·구분 | 역행렬이 존재하는 XTX를 써 X+ D×N, θ=X+y D×1; 실제계산은 연립계 가능. | 표시한 $\mathbf X^+=(\mathbf X^\top\mathbf X)^{-1}\mathbf X^\top$ 식은 해당 역행렬이 있을 때 써요. $\mathbf X^+$는 $D\times N$, $\theta_{\mathrm{ML}}$은 $D\times1$이며, 계산은 역행렬을 직접 만들기보다 정규방정식 연립계를 풀 수 있어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s3-vector-diff | 일반 | MML9.11 보충; 상수미분0/선형항/대칭이차항 규칙으로 1×D 행미분. | 손실을 전개한 뒤 두 가지 미분 규칙을 쓰면 슬라이드의 dL/dθ가 나와요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s3-vector-diff | 조건·구분 | MML9.11 보충; 상수미분0/선형항/대칭이차항 규칙으로 1×D 행미분. | 보충(MML 식 9.11)이며 수업에서 이 유도를 하지 않았어요. 선형항의 미분은 $\mathbf a^\top$, 이차항은 $\theta^\top(A+A^\top)$이고 $A=X^\top X$가 대칭이라 두 배가 돼요. 상수 $y^\top y$의 미분은 0이며 결과는 $1\times D$ 행벡터예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s3-vector-diff | 보충 | 행벡터 미분 convention과 상세유도는 수업에서 하지않은 MML9.11 보충. | 보충(MML 식 9.11)이며 수업에서 이 유도를 하지 않았어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s3-bias | 일반 | 상수1과계수추가로 D+1, 확장XN×(D+1), inverse해 rankD+1 필요. | 상수항은 입력에 1을 붙여 D+1 차원으로 늘리면 같은 방법으로 풀려요. | 기존 반영 | pass |
| 정리노트_0923_Linear_Regression.html#s3-bias | 조건·구분 | 상수1과계수추가로 D+1, 확장XN×(D+1), inverse해 rankD+1 필요. | 계수도 $D+1$로 늘리고 데이터 행렬은 첫 열이 모두 1인 $N\times(D+1)$이 돼요. 이 확장행렬의 역행렬 해에는 $\mathrm{rk}(\tilde{\mathbf X})=D+1$ 조건이 필요해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0923_Linear_Regression.html#s4-cheatsheet | 일반 | 앞 학습 토픽들을 연결하는 기존 치트시트 표. | N/A: 이 화면 자체가 요약·링크 표다. 별도 .sum을 새로 만들지 않았다. | 해당 없음 | pass |
| 정리노트_0923_Linear_Regression.html#s4-next | 일반 | 아직 배우지 않은 다음 시간 범위를 명시한 예고. | N/A: 예고 화면이며 현재 학습 범위 요약으로 전환하지 않았다. | 해당 없음 | pass |
| 정리노트_0923_Linear_Regression.html#s4-links | 일반 | 기존 학습·문제·PDF 자료의 링크 모음. | N/A: 링크 화면으로 기존 구조를 유지했다. | 해당 없음 | pass |

## Current regeneration source classification correction (Task6b)

Active content inputs are the published `fragments/pN.html`, copied to RUN `explanations/pN.html` by `mpe_rerender.py` lines 188–206 and read by `mpe_cli.load_fragments`. The files under `evidence/`, including `author.py`, are historical authoring/review evidence; the current build copies them as artifacts and does not execute them. Their six Task6a summary edits were restored only after exact current bytes matched the controller Task6b baseline, retaining all current fragment summaries. No historical author/review script is a renewed approval. Current browser and approval binding remain pending.


## Task6c visible-summary equation line breaks

- `정리노트_0923_Linear_Regression.html#s3-vector-diff`: actual summary display equations now `\begin{aligned}L=\frac1{2\sigma^2}\bigl(&\mathbf y^\top\mathbf y\\&-2\mathbf y^\top\mathbf X\boldsymbol\theta\\&+\boldsymbol\theta^\top\mathbf X^\top\mathbf X\boldsymbol\theta\bigr)\end{aligned}` / `\begin{aligned}\frac{dL}{d\boldsymbol\theta}&=\frac1{2\sigma^2}\bigl(-2\mathbf y^\top\mathbf X\\&\quad+2\boldsymbol\theta^\top\mathbf X^\top\mathbf X\bigr)\\&=\frac1{\sigma^2}\bigl(-\mathbf y^\top\mathbf X\\&\quad+\boldsymbol\theta^\top\mathbf X^\top\mathbf X\bigr)\\&\in\mathbb R^{1\times D}\end{aligned}`. Same-body operators/values/order and conditions were directly reread; no learning-body change.
