# 본문–요약 수동 감사 0928

범위: 이 날짜의 정리노트·복습문제·문제설명 실제 본문과 실제 요약. 외부 원자료 전체의 독립 학술 검증은 아니다. 교수 일화·비유·반복은 원리/조건과 다른 새 핵심이 없으면 생략한다. 질문·풀이·정답 본문은 이번 작업에서 보존했다.

| 자료·토픽 | 구분 | 실제 본문 주장 | 대응하는 현재 요약 문장 / 생략 이유 | 보완 전 | 판정 |
|---|---|---|---|---|---|
| 문제설명_0928_Linear_Regression.html#p1 | 일반 | 2차K3, N3→3×3 행특징[1,−1,1],[1,1,1],[1,2,4], Φθ3×1. | 각 행에−1,1,2를 다시 대입하면 [1,−1,1],[1,1,1],[1,2,4]예요. | 기존 반영 | pass |
| 문제설명_0928_Linear_Regression.html#p1 | 주의 | 2차K3, N3→3×3 행특징[1,−1,1],[1,1,1],[1,2,4], Φθ3×1. | 2차식은 상수항까지 $K=3$이므로 $N=3$일 때 $\Phi$는 $3\times3$이에요. 데이터별 특징을 열로 쌓으면 전치된 다른 행렬이 돼요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0928_Linear_Regression.html#p2 | 일반 | 3차K4, Φ8×4, fullcolrank에서inverseML, 최소4distinct입력 Vandermonde독립. | 적어도4개의 서로 다른 입력이면 Vandermonde 열이 독립이에요. | 기존 반영 | pass |
| 문제설명_0928_Linear_Regression.html#p2 | 주의 | 3차K4, Φ8×4, fullcolrank에서inverseML, 최소4distinct입력 Vandermonde독립. | 표시한 역행렬 공식은 $\Phi$가 full column rank일 때 써요. 잡음 분산은 고정된 양수이고, rank가 부족하면 해가 유일하지 않을 수 있어요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0928_Linear_Regression.html#p3 | 일반 | σ²1/25/b²1/4=4/25, 8차효과는교과서경향이지보편정리 아님. | 하지만 입력·출력 실현값이 없으므로 이 문제의 모든 데이터에 대한 엄밀한 순위는 정할 수 없어요. | 기존 반영 | pass |
| 문제설명_0928_Linear_Regression.html#p4 | 일반 | 곱+chain미분:4/x sin(x³)+3x²log(x⁴)cos(x³), 정의역x≠0/절댓값log주의. | x≠0에서 u′=4/x, v′=3x²cos(x³)를 각각 곱해 더한 식이에요. | 기존 반영 | pass |
| 문제설명_0928_Linear_Regression.html#p4 | 주의 | 곱+chain미분:4/x sin(x³)+3x²log(x⁴)cos(x³), 정의역x≠0/절댓값log주의. | 실수 정의역은 $x\ne0$이고 전체 정의역에서 $\log(x^4)=4\log\|x\|$예요. $4\log x$로 바꾸는 것은 $x>0$에서만 가능해요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0928_Linear_Regression.html#p5 | 일반 | Gaussian모양exp합성미분=−(x−μ)/σ²×exp, σ≠0/분산해석σ>0. | σ²>0이면 μ 왼쪽에서 증가, 오른쪽에서 감소하므로 봉우리가 맞아요. | 기존 반영 | pass |
| 문제설명_0928_Linear_Regression.html#p5 | 주의 | Gaussian모양exp합성미분=−(x−μ)/σ²×exp, σ≠0/분산해석σ>0. | $\mu,\sigma$는 고정 상수이며 $\sigma=0$에서는 함수가 정의되지 않아요. 분산 모형에서는 $\sigma>0$으로 두어요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0928_Linear_Regression.html#p6 | 일반 | log(1+xᵀx)미분1×D, sin(Ax+b) Jacobian diagcos E×E·A E×D, 차원관례보존. | diag(cos z)A의 (i,j)칸과 같고 E×D예요. | 기존 반영 | pass |
| 문제설명_0928_Linear_Regression.html#p6 | 주의 | log(1+xᵀx)미분1×D, sin(Ax+b) Jacobian diagcos E×E·A E×D, 차원관례보존. | (a)의 연쇄 차원은 $(1\times1)(1\times D)$, (b)는 $(E\times E)(E\times D)$예요. 행 자코비안과 열 그래디언트 관례를 섞지 않아요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0928_Linear_Regression.html#p7 | 일반 | 성분tanh미분diag(1−tanh²z)M×M·AM×N, 비대각0/b상수. | (M×M)(M×N)=M×N이고 b의 미분은0이에요. | 기존 반영 | pass |
| 문제설명_0928_Linear_Regression.html#p7 | 주의 | 성분tanh미분diag(1−tanh²z)M×M·AM×N, 비대각0/b상수. | 성분별 도함수 벡터 $1-\tanh^2z$를 그대로 곱하지 않고 $M\times M$ 대각행렬로 만들어 $M\times N$인 $A$에 왼쪽에서 곱해요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0928_Linear_Regression.html#p8 | 일반 | sigmoid역수/exp 두음수상쇄, f′=f(1−f), x0에서1/4. | 별도 symbolic 미분에서 $e^{-x}/(1+e^{-x})^2=f(1-f)$를 확인해요. | 기존 반영 | pass |
| 문제설명_0928_Linear_Regression.html#p8 | 주의 | sigmoid역수/exp 두음수상쇄, f′=f(1−f), x0에서1/4. | 역수 미분과 안쪽 $e^{-x}$ 미분의 두 음수가 상쇄되어 $f^\prime(x)=f(x)(1-f(x))>0$이에요. 안쪽의 $-1$을 빠뜨리지 않아요. | unresolved → 보완 후 다시 읽음 | pass |
| 복습문제_0928_Linear_Regression.html#p1 | 일반 | 2차K3, N3→3×3 행특징[1,−1,1],[1,1,1],[1,2,4], Φθ3×1. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0928_Linear_Regression.html#p2 | 일반 | 3차K4, Φ8×4, fullcolrank에서inverseML, 최소4distinct입력 Vandermonde독립. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0928_Linear_Regression.html#p3 | 일반 | σ²1/25/b²1/4=4/25, 8차효과는교과서경향이지보편정리 아님. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0928_Linear_Regression.html#p4 | 일반 | 곱+chain미분:4/x sin(x³)+3x²log(x⁴)cos(x³), 정의역x≠0/절댓값log주의. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0928_Linear_Regression.html#p5 | 일반 | Gaussian모양exp합성미분=−(x−μ)/σ²×exp, σ≠0/분산해석σ>0. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0928_Linear_Regression.html#p6 | 일반 | log(1+xᵀx)미분1×D, sin(Ax+b) Jacobian diagcos E×E·A E×D, 차원관례보존. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0928_Linear_Regression.html#p7 | 일반 | 성분tanh미분diag(1−tanh²z)M×M·AM×N, 비대각0/b상수. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0928_Linear_Regression.html#p8 | 일반 | sigmoid역수/exp 두음수상쇄, f′=f(1−f), x0에서1/4. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 정리노트_0928_Linear_Regression.html#s0-learning-map | 일반 | ML/MAP 모두 점추정, 등방prior와 일반prior는 특수형/일반형이지 MAP/FB 구분 아님. | 특징행렬 Φ는 곡선의 재료를 모으고, 사전분포는 계수가 어디에 얼마나 모이길 기대하는지 나타내요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s0-learning-map | 조건·구분 | ML/MAP 모두 점추정, 등방prior와 일반prior는 특수형/일반형이지 MAP/FB 구분 아님. | ML은 우도를, MAP은 사후분포를 최대화하지만 둘 다 최종 계수는 한 점이에요. $\mathcal N(0,b^2I)$는 $\mathcal N(m_0,S_0)$의 특수형이고, 이 두 사전분포를 MAP과 FB의 차이로 나누지 않아요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s0-recap | 일반 | 고정입력·계수에서 iid Gaussian잡음, 자연log가 곱/exp를 제거해 SSE+상수, 스칼라손실 벡터미분 필요. | 가우시안 잡음에서 우도를 최대화하는 것은 음의 로그우도, 곧 최소제곱을 최소화하는 것과 같고, 이를 풀려면 스칼라를 벡터로 미분해야 해요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s0-recap | 조건·구분 | 고정입력·계수에서 iid Gaussian잡음, 자연log가 곱/exp를 제거해 SSE+상수, 스칼라손실 벡터미분 필요. | 입력·계수가 주어지면 잡음만 불확실해요. 공통 가우시안 분산을 계수와 무관하게 두면 i.i.d. 우도의 곱을 자연로그로 합으로 바꾸고, 계수와 무관한 상수를 제외해 최소제곱을 얻어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s0-gradient | 일반 | 편미분은 다른변수고정, n개를1×n 행벡터로 모으는 관례, 열벡터 관례도 가능. | 스칼라 함수를 벡터로 미분하면, 변수마다 편미분을 구해 행벡터로 모은 그래디언트가 나와요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s0-gradient | 조건·구분 | 편미분은 다른변수고정, n개를1×n 행벡터로 모으는 관례, 열벡터 관례도 가능. | 행벡터는 이 수업의 관례이며 열벡터로 정의하는 관례도 가능해요. 편미분은 다른 변수를 고정한 국소 변화이고, 딥러닝 가중치의 손실 변화와 경사하강법 연결은 슬라이드 밖 수업 설명이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s0-jacobian | 일반 | n입력m출력 Jacobian m×n; 고정Ax의 성분미분Aij를 모으면A. | 벡터값 함수를 벡터로 미분하면, 각 함수의 그래디언트 행벡터를 위아래로 쌓은 자코비안이 나오고, $\mathbf{A}\mathbf{x}$의 자코비안은 $\mathbf{A}$예요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s0-jacobian | 조건·구분 | n입력m출력 Jacobian m×n; 고정Ax의 성분미분Aij를 모으면A. | 입력 $n$, 출력 $m$인 자코비안은 $m\times n$이고 $m=1$이면 행 그래디언트예요. $A\in\mathbb R^{m\times n}$가 고정이면 $(Ax)_i=\sum_j A_{ij}x_j$의 편미분이 $A_{ij}$이므로 자코비안이 $A$예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s1-chain | 일반 | 잔차 e=y−Φθ, dL/de=2eᵀ1×N, de/dθ=−ΦN×D, 곱은1×D. | 스칼라 손실을 벡터 파라미터로 미분할 때는 오차로 한 번 치환해서 두 미분을 곱해요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s1-chain | 조건·구분 | 잔차 e=y−Φθ, dL/de=2eᵀ1×N, de/dθ=−ΦN×D, 곱은1×D. | $e=y-\Phi\theta$에서 $y$는 계수와 무관하고 $de/d\theta=-\Phi$예요. $(1\times N)(N\times D)=1\times D$ 순서로 곱하며, 특징 함수가 항등이면 $\Phi=X$예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s1-theta-ml | 일반 | 정규방정식과대칭역행렬 전치 제거; 역행렬조건rankD와증명은 보충. | 기울기를 0으로 두고 대칭행렬 성질로 전치를 지우면, 최대우도 해가 유사역행렬로 나와요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s1-theta-ml | 조건·구분 | 정규방정식과대칭역행렬 전치 제거; 역행렬조건rankD와증명은 보충. | 역행렬이 존재하는 대칭행렬의 역행렬도 대칭이어서 전치를 지워요. 보충의 전치·역행렬 증명과 $\operatorname{rk}(X)=D$이면 $X^\top X$가 양의 정부호라는 조건은 수업에서 유도하지 않았어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s1-theta-ml | 보충 | 수업에서 증명하지않은 대칭역행렬/전치및rank조건을 보충으로 구분. | 보충의 전치·역행렬 증명과 $\operatorname{rk}(X)=D$이면 $X^\top X$가 양의 정부호라는 조건은 수업에서 유도하지 않았어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s2-features | 일반 | φ:D→K와 θK내적은 scalar, linear in θ이면 입력비선형도 회귀. | 입력을 비선형 특징으로 바꿔도 θ에 대해 선형이면 선형회귀예요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s2-features | 조건·구분 | φ:D→K와 θK내적은 scalar, linear in θ이면 입력비선형도 회귀. | $\phi(x)$와 $\theta$는 모두 길이 $K$라 내적 평균은 스칼라예요. 특징 함수는 $\mathbb R^D\to\mathbb R^K$이고, 결과 곡선이 직선일 필요는 없어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s2-polynomial | 일반 | 상수포함 K=M+1, 계수는학습/차수는hyperparameter, 큰차수성능미정. | 스칼라 입력을 단항식으로 K차원까지 늘리면 곡선도 선형회귀로 맞출 수 있어요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s2-polynomial | 조건·구분 | 상수포함 K=M+1, 계수는학습/차수는hyperparameter, 큰차수성능미정. | 상수항을 포함하므로 최고 차수는 $K-1$이에요. $\theta$는 데이터로 배우는 파라미터이고 차수·$K$는 미리 고르는 하이퍼파라미터이며, 더 큰 차수가 더 좋은지는 데이터로 따져요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s2-feature-matrix | 일반 | ΦN×K의행데이터/열특징; iid잡음σ²IN조건부공분산과 K계수prior구분은 보충. | 특징 벡터를 행으로 쌓은 Φ를 X 자리에 넣으면 같은 최대우도 해가 나와요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s2-feature-matrix | 조건·구분 | ΦN×K의행데이터/열특징; iid잡음σ²IN조건부공분산과 K계수prior구분은 보충. | 한 행은 한 데이터, 한 열은 한 특징이라 $\Phi$는 $N\times K$예요. 보충에서는 독립·동일 분산 $\sigma^2$의 가우시안 잡음을 묶어 $\sigma^2I_N$인 $N\times N$ 조건부 공분산을 얻어요. 계수까지 고정한 이 공분산을 파라미터 불확실성까지 합친 예측 공분산이나 사전의 $b^2I_K$와 구별해요. 이 설명은 수업 밖 보충이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s2-feature-matrix | 보충 | 독립동분산관측 잡음의σ²IN조건부공분산, K차원계수prior/예측공분산과 구분. | 계수까지 고정한 이 공분산을 파라미터 불확실성까지 합친 예측 공분산이나 사전의 $b^2I_K$와 구별해요. 이 설명은 수업 밖 보충이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s3-polyfit | 일반 | 10점에M차 K=M+1; M9보간과출렁임, M≥10역행렬불가; .2std/.04variance. | 같은 점 10개에 차수 $M$을 바꿔 가며 최대우도 다항식을 맞춰 봐요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s3-polyfit | 조건·구분 | 10점에M차 K=M+1; M9보간과출렁임, M≥10역행렬불가; .2std/.04variance. | $K=M+1$이고 $\Phi$는 $10\times(M+1)$이에요. 이 예의 $M=9$는 열 개 점을 보간하지만 점 사이에서 출렁이고, $M\ge10$이면 $\Phi^\top\Phi$가 가역이 아니어서 표시한 역행렬 식을 쓸 수 없어요. 잡음의 0.2는 표준편차이고 분산은 0.04예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s3-overfitting | 일반 | 중첩모델로훈련오차비증가, 새비교점오차커짐; RMSE평균/제곱근 단위, 표본흔들림. | 차수를 올리면 훈련 오차는 계속 줄지만 테스트 오차는 어느 차수부터 커져요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s3-overfitting | 조건·구분 | 중첩모델로훈련오차비증가, 새비교점오차커짐; RMSE평균/제곱근 단위, 표본흔들림. | 상위 차수 모델이 새 계수를 0으로 두어 하위 모델을 포함하므로 최적 훈련 오차는 늘 수 없어요. RMSE는 제곱합을 데이터 수로 평균하고 제곱근을 취해 출력과 단위를 맞춰요. 여기 테스트 오차는 예제에서 새로 만든 비교점에서 잰 값이며 표본에 따른 국소 흔들림도 있어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s4-map-bayes | 일반 | prior가X조건에도 안바뀐다는가정 후 Bayes분모상수제외, NLL+negative logprior최소. | MAP은 우도에 사전분포를 곱한 사후분포를 가장 크게 만드는 $\boldsymbol{\theta}$를 찾아요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s4-map-bayes | 조건·구분 | prior가X조건에도 안바뀐다는가정 후 Bayes분모상수제외, NLL+negative logprior최소. | $p(\theta\mid\mathcal X)=p(\theta)$는 입력만으로 사전 믿음이 바뀌지 않는다는 가정이에요. 이 가정에서 계수와 무관한 분모를 제외하고 NLL과 음의 로그 prior의 합을 최소화해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s4-gaussian-prior | 일반 | b²I K×K인jointGaussian이라 무상관→독립; logprior=norm²/(2b²), 일반분포예외는보충. | 평균 0인 가우시안 사전분포를 두면 음의 로그사후확률에 $\boldsymbol{\theta}$ 크기 벌점 항이 하나 더 붙어요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s4-gaussian-prior | 조건·구분 | b²I K×K인jointGaussian이라 무상관→독립; logprior=norm²/(2b²), 일반분포예외는보충. | $b^2>0$인 사전 $\mathcal N(0,b^2I_K)$에서 $\theta$는 길이 $K$, 공분산은 $K\times K$이고 음의 로그 prior 벌점은 $\\|\theta\\|^2/(2b^2)$예요. 보충: 비대각 공분산 0에서 독립을 결론 내리는 데는 공동 가우시안 조건이 필요하며 일반 분포에는 성립하지 않아요. 대각/비대각의 분산·공분산 설명은 수업 밖 보충이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s4-gaussian-prior | 보충 | 무상관→독립의jointGaussian조건과 대각분산/비대각공분산의수업외범위. | 대각/비대각의 분산·공분산 설명은 수업 밖 보충이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s4-ml-vs-map | 일반 | σ²/b²I추가, b넓음ML/좁음0, positive term이면PD; MAP만능아님. | MAP 해는 ML 해의 역행렬 안에 $\frac{\sigma^2}{b^2} \mathbf{I}$ 한 항을 더한 것이고, $b \to \infty$이면 ML과 같아져요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s4-ml-vs-map | 조건·구분 | σ²/b²I추가, b넓음ML/좁음0, positive term이면PD; MAP만능아님. | 양의 $\sigma^2/b^2$ 항은 행렬을 양의 정부호로 만들어 역행렬을 보장하고, $b^2\to0$이면 계수를 0 쪽으로 눌러요. 이 양의 정부호 성질은 슬라이드에 있고 수업에서는 말하지 않았어요. 교과서도 MAP을 과적합의 일반 해결책으로 보지는 않아요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s5-general-prior | 일반 | m0 K평균, S0 K×K공분산, SPD역행렬조건; 등방특수형, 일반MAP가능, posterior다음시간. | 사전분포를 $\mathcal{N}(\mathbf{m}_0, \mathbf{S}_0)$로 일반화하면 선험적 의도 항이 바뀌고, $\mathcal{N}(\mathbf{0}, b^2\mathbf{I})$는 그 특수한 경우예요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s5-general-prior | 조건·구분 | m0 K평균, S0 K×K공분산, SPD역행렬조건; 등방특수형, 일반MAP가능, posterior다음시간. | 일반 사전분포도 MAP 한 점에 사용할 수 있어요. 보충에서 $m_0\in\mathbb R^K$, $S_0\in\mathbb R^{K\times K}$이고, 표시한 $S_0^{-1}$을 쓰려면 양의 정부호 공분산을 가정해요. 대각은 분산, 비대각은 공분산이며 이 성분 설명은 수업 밖 보충이고 사후분포 계산은 다음 시간 범위예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s5-general-prior | 보충 | 평균/공분산 차원및SPD조건은보충, posterior계산은미래범위. | 대각은 분산, 비대각은 공분산이며 이 성분 설명은 수업 밖 보충이고 사후분포 계산은 다음 시간 범위예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s5-rls | 일반 | SSE+λnorm²의λ=σ²/b²는 목적함수전체스케일 정합; λ>0PD역행렬/유일해증명은보충. | 정규화 최소제곱(RLS, 릿지)은 $\lambda = \frac{\sigma^2}{b^2}$일 때 가우시안 사전분포 MAP과 같은 문제예요. | 기존 반영 | pass |
| 정리노트_0928_Linear_Regression.html#s5-rls | 조건·구분 | SSE+λnorm²의λ=σ²/b²는 목적함수전체스케일 정합; λ>0PD역행렬/유일해증명은보충. | 여기의 데이터 항은 제곱합이므로 $\lambda=\sigma^2/b^2$이고, 슬라이드의 $1/(2b^2)$는 음의 로그 prior 항 자체의 계수예요. 목적함수 전체의 양의 배율을 맞춰 비교해야 해요. 보충의 직접 미분과 $\lambda>0$에서 $\\|\Phi v\\|^2+\lambda\\|v\\|^2>0$인 증명은 수업에서 유도하지 않았으며, 이 조건에서 역행렬과 유일해가 보장돼요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s5-rls | 보충 | 직접미분·λ양수에서PD증명은수업에서미룸. | 보충의 직접 미분과 $\lambda>0$에서 $\\|\Phi v\\|^2+\lambda\\|v\\|^2>0$인 증명은 수업에서 유도하지 않았으며, 이 조건에서 역행렬과 유일해가 보장돼요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0928_Linear_Regression.html#s6-cheatsheet | 일반 | 앞 학습 토픽들을 연결하는 기존 치트시트 표. | N/A: 이 화면 자체가 요약·링크 표다. 별도 .sum을 새로 만들지 않았다. | 해당 없음 | pass |
| 정리노트_0928_Linear_Regression.html#s6-next | 일반 | 아직 배우지 않은 다음 시간 범위를 명시한 예고. | N/A: 예고 화면이며 현재 학습 범위 요약으로 전환하지 않았다. | 해당 없음 | pass |
| 정리노트_0928_Linear_Regression.html#s6-links | 일반 | 기존 학습·문제·PDF 자료의 링크 모음. | N/A: 링크 화면으로 기존 구조를 유지했다. | 해당 없음 | pass |

## Current regeneration source classification correction (Task6b)

Active content inputs are the published `fragments/pN.html`, copied to RUN `explanations/pN.html` by `mpe_rerender.py` lines 188–206 and read by `mpe_cli.load_fragments`. The files under `evidence/`, including `author.py`, are historical authoring/review evidence; the current build copies them as artifacts and does not execute them. Their six Task6a summary edits were restored only after exact current bytes matched the controller Task6b baseline, retaining all current fragment summaries. No historical author/review script is a renewed approval. Current browser and approval binding remain pending.


## Task6c visible-summary equation line breaks

- `정리노트_0928_Linear_Regression.html#s3-polyfit`: actual summary display equations now `\begin{aligned}x_n&\sim\mathcal U[-5,5],\\y_n&=-\sin(x_n/5)\\&\quad+\cos(x_n)+\epsilon,\\\epsilon&\sim\mathcal N(0,0.2^2)\end{aligned}` / `\begin{aligned}f(x)&=\theta_0+\theta_1x\\&\quad+\theta_2x^2+\dots+\theta_Mx^M\\&=\boldsymbol\phi(x)^\top\boldsymbol\theta\end{aligned}`. Same-body operators/values/order and conditions were directly reread; no learning-body change.
