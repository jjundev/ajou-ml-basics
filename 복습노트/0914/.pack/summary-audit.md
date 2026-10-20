# 본문–요약 수동 감사 0914

범위: 이 날짜의 정리노트·복습문제·문제설명 실제 본문과 실제 요약. 외부 원자료 전체의 독립 학술 검증은 아니다. 교수 일화·비유·반복은 원리/조건과 다른 새 핵심이 없으면 생략한다. 질문·풀이·정답 본문은 이번 작업에서 보존했다.

| 자료·토픽 | 구분 | 실제 본문 주장 | 대응하는 현재 요약 문장 / 생략 이유 | 보완 전 | 판정 |
|---|---|---|---|---|---|
| 문제설명_0914_ERM_and_MLE.html#p1 | 일반 | x에 1 추가→길이3, 계수와 맞춰 내적 9/2. | 첫 성분은 1이고 나머지는 주어진 입력이에요. 계수 벡터와 모두 길이 3이에요. | 기존 반영 | pass |
| 문제설명_0914_ERM_and_MLE.html#p2 | 일반 | X3×2와 y3×1, A MSE2/3, B1/2; 두 후보 비교일 뿐 전역최적해 증명 아님. | $2/3-1/2=1/6>0$이므로 B예요. 이는 두 후보끼리 비교한 결과이며 전역 최적해를 증명한 것은 아니에요. | 기존 반영 | pass |
| 문제설명_0914_ERM_and_MLE.html#p3 | 일반 | JA=5λ, JB=5/3+2λ; λ0은 A, λ1은 B; bias도 penalty 포함. | $J_A=0+5\lambda$, $J_B=5/3+2\lambda$를 적어요. | 기존 반영 | pass |
| 문제설명_0914_ERM_and_MLE.html#p3 | 주의 | JA=5λ, JB=5/3+2λ; λ0은 A, λ1은 B; bias도 penalty 포함. | 이 문제는 바이어스까지 벌점에 포함해요. 평균 손실의 $1/N$을 벌점에 추가로 곱하지 않고, 주어진 두 후보끼리 비교해요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0914_ERM_and_MLE.html#p4 | 일반 | 입력 계수 고정하고 잡음만 확률변수; 평균5 분산1, 표준편차와 구분. | $E[y]=5+E[\epsilon]=5$, $Var(y)=Var(\epsilon)=1$로 정의에서 확인돼요. | 기존 반영 | pass |
| 문제설명_0914_ERM_and_MLE.html#p4 | 주의 | 입력 계수 고정하고 잡음만 확률변수; 평균5 분산1, 표준편차와 구분. | 입력·계수를 고정한 조건부 분포이고, 가우시안의 두 번째 인자는 표준편차가 아닌 분산이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0914_ERM_and_MLE.html#p5 | 일반 | iid 고정 Gaussian 분산: NLL=상수+SSE/2, A3.757 B3.507; 상수는 값 계산시 필요. | 별도 계산에서 A=3.7568156…, B=3.5068156…이므로 반올림하면 3.757과 3.507예요. | 기존 반영 | pass |
| 문제설명_0914_ERM_and_MLE.html#p5 | 주의 | iid 고정 Gaussian 분산: NLL=상수+SSE/2, A3.757 B3.507; 상수는 값 계산시 필요. | 공통 분산을 고정했으므로 SSE에 같은 양의 배율과 상수를 더해도 후보 순서는 같아요. NLL의 실제 수치에는 로그 상수항을 남겨요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0914_ERM_and_MLE.html#p6 | 일반 | 표준 내적 차이[2,3,3], 제곱합22, 거리sqrt22. | 반대로 y−x=[−2,−3,−3]을 써도 제곱합은22, 거리는 $\sqrt{22}$예요. | 기존 반영 | pass |
| 문제설명_0914_ERM_and_MLE.html#p6 | 주의 | 표준 내적 차이[2,3,3], 제곱합22, 거리sqrt22. | $22$는 거리의 제곱이고 표준 내적에서 거리는 $\sqrt{22}$예요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0914_ERM_and_MLE.html#p7 | 일반 | f′의 두 근 -2±sqrt5, f″부호로 각각 국소극소/극대; 전역극값과 구분. | 삼차함수는 양끝이 반대 방향으로 무한히 가므로 전역 극값이라고 쓰지 않아요. | 기존 반영 | pass |
| 문제설명_0914_ERM_and_MLE.html#p7 | 주의 | f′의 두 근 -2±sqrt5, f″부호로 각각 국소극소/극대; 전역극값과 구분. | 정상점 $x=-2-\sqrt5$에서는 $f^{\prime\prime}<0$이라 국소 극대, $x=-2+\sqrt5$에서는 $f^{\prime\prime}>0$이라 국소 극소예요. 도함수 0만으로 판정하지 않으며, 이 삼차함수의 전역 최대·최소와 구별해요. | unresolved → 보완 후 다시 읽음 | pass |
| 복습문제_0914_ERM_and_MLE.html#p1 | 일반 | x에 1 추가→길이3, 계수와 맞춰 내적 9/2. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0914_ERM_and_MLE.html#p2 | 일반 | X3×2와 y3×1, A MSE2/3, B1/2; 두 후보 비교일 뿐 전역최적해 증명 아님. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0914_ERM_and_MLE.html#p3 | 일반 | JA=5λ, JB=5/3+2λ; λ0은 A, λ1은 B; bias도 penalty 포함. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0914_ERM_and_MLE.html#p4 | 일반 | 입력 계수 고정하고 잡음만 확률변수; 평균5 분산1, 표준편차와 구분. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0914_ERM_and_MLE.html#p5 | 일반 | iid 고정 Gaussian 분산: NLL=상수+SSE/2, A3.757 B3.507; 상수는 값 계산시 필요. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0914_ERM_and_MLE.html#p6 | 일반 | 표준 내적 차이[2,3,3], 제곱합22, 거리sqrt22. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0914_ERM_and_MLE.html#p7 | 일반 | f′의 두 근 -2±sqrt5, f″부호로 각각 국소극소/극대; 전역극값과 구분. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s0-learning-map | 일반 | ERM의 평균손실 최소화와 ML의 데이터 우도 최대화; 고정 분산 Gaussian에서만 동일한 계수 계산. | 가우시안 잡음의 분산이 고정된 선형회귀에서는 ML과 제곱 손실 최소화가 같은 파라미터를 골라요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s0-learning-map | 조건·구분 | ERM의 평균손실 최소화와 ML의 데이터 우도 최대화; 고정 분산 Gaussian에서만 동일한 계수 계산. | ERM은 평균 손실을 최소화하고 ML은 관측 우도를 최대화해요. 독립 가정으로 우도를 곱으로 나누고 로그로 합으로 바꾸며, ML의 파라미터는 고정된 미지의 값이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s0-suppose | 일반 | 원 규칙을 몰라 세운 suppose이며 모델은 유용성·선호로 평가한다. | 모델은 모르니까 세우는 가정(suppose)이고, 옳고 그름이 아니라 선호(preference)의 문제예요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s0-two-models | 일반 | 함수는 값 하나, PDF 모형은 불확실성 분포; 학습 데이터로 계수, 훈련 전 하이퍼파라미터를 정한다. | 모델은 결정론적 함수나 확률밀도함수(PDF)로 정하고, 트레이닝은 그 파라미터를 데이터로 고르는 일이에요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s1-erm-name | 일반 | 실제 관측의 위험을 목적함수로 정한 뒤 그 관점에서 계수를 최소화한다. | 실제 데이터로 잰 위험을 최소화하는 관점에서 파라미터를 최적화하는 게 ERM이에요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s1-data | 일반 | 각 x는 D열벡터; 열로 나란히 붙인 D×N을 전치해 N×D로 만든다. | 볼드 소문자는 벡터, 라벨은 스칼라이고, 열벡터를 옆으로 나란히 붙이면 D×N 행렬이 돼요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s1-data | 조건·구분 | 각 x는 D열벡터; 열로 나란히 붙인 D×N을 전치해 N×D로 만든다. | 각 열벡터를 옆으로 나란히 붙이면 $D\times N$이고, 이를 전치해 데이터 하나를 한 행에 두면 $N\times D$인 $\mathbf{X}$가 돼요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s1-goal | 일반 | y는 라벨, yhat은 추정; 공통 계수를 모든 n에서 두루 맞춰야 한다. | 모든 학습 데이터에서 추정치가 라벨에 가까워지는 파라미터 θ*를 찾는 게 목표예요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s1-affine | 일반 | 상수 1을 앞에 추가해 bias 흡수, x와 계수 길이 D+1; 뉴런은 어파인에 비선형을 합성. | 데이터 앞에 1을 붙이면 바이어스가 θ₀으로 흡수되어 어파인 모델이 내적 하나가 돼요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s1-affine | 조건·구분 | 상수 1을 앞에 추가해 bias 흡수, x와 계수 길이 D+1; 뉴런은 어파인에 비선형을 합성. | 입력과 계수 모두 길이 $D+1$로 맞춰요. 여기서 augmentation은 바이어스 흡수를 뜻하고, 뉴런은 어파인 출력에 비선형 활성화 함수를 적용해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s2-remp | 일반 | X는 예제를 행으로 쌓은 N×D, y는 따로 N×1; N개의 스칼라 손실 평균이 경험적 위험. | 입력을 가로로 눕혀 쌓은 행렬 X를 만들고, 데이터별 손실의 평균을 경험적 위험이라고 불러요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s2-remp | 조건·구분 | X는 예제를 행으로 쌓은 N×D, y는 따로 N×1; N개의 스칼라 손실 평균이 경험적 위험. | $\mathbf{X}$는 $N\times D$ 입력 행렬, $\mathbf{y}$는 $N\times1$ 라벨 벡터예요. 입력 앞에 1을 붙이면 행 길이는 $D+1$이고, 한 데이터의 손실은 음이 아닌 스칼라예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s2-squared | 일반 | 성분별 잔차 제곱합/N은 노름제곱/N; 데이터 고정, 계수만 최소화, 예측·잔차 벡터 N×1. | 제곱 손실의 평균은 X를 가로로 쌓아 둔 덕분에 노름 제곱 한 줄로 써져요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s2-squared | 조건·구분 | 성분별 잔차 제곱합/N은 노름제곱/N; 데이터 고정, 계수만 최소화, 예측·잔차 벡터 N×1. | $\mathbf{X},\mathbf{y}$는 고정하고 $\boldsymbol{\theta}$만 최소화해요. $\mathbf{X}\boldsymbol{\theta}$와 잔차는 $N\times1$이며 노름의 제곱은 잔차 성분 제곱의 합이에요. 보충의 $N=D=2$ 계산은 합과 행렬식이 같은지 확인한 것으로, 수업에서 유도하지 않았어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s2-squared | 보충 | N=D=2 산수 확인은 수업에서 유도하지 않은 보충. | 보충의 $N=D=2$ 계산은 합과 행렬식이 같은지 확인한 것으로, 수업에서 유도하지 않았어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s2-true-risk | 일반 | 유한 관측 평균 R_emp와 모든 데이터 기대 R_true를 구분; 분포가 크게 다르지 않아야 일반화 연결. | 학습 데이터에서의 평균 손실을 줄이는 건 수단이고, 진짜 목표는 처음 보는 데이터까지 포함한 기대 위험을 줄이는 거예요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s2-true-risk | 조건·구분 | 유한 관측 평균 R_emp와 모든 데이터 기대 R_true를 구분; 분포가 크게 다르지 않아야 일반화 연결. | 학습 데이터의 적합이 새 데이터 예측으로 이어지려면 앞으로의 데이터가 지금 데이터와 크게 다르지 않아야 해요. 유한한 데이터에서는 $R_{\text{emp}}$만 직접 계산하고, 남겨 둔 테스트 데이터로 예측 성능을 확인해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s3-reg | 일반 | 훈련 손실 작아도 테스트 손실 클 수 있음; λ는 데이터 적합과 계수 크기 균형을 목적함수에서 조절. | 학습 데이터에 너무 맞추면 과적합이 생겨서, 패널티 항을 더해 θ를 원점 쪽으로 붙잡아요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s3-reg | 조건·구분 | 훈련 손실 작아도 테스트 손실 클 수 있음; λ는 데이터 적합과 계수 크기 균형을 목적함수에서 조절. | $\lambda=0$이면 경험적 위험만 최소화하고, $\lambda>0$이면 적합 오차와 파라미터 크기를 함께 줄여요. 이 $\lambda$는 함수 꼴을 바꾸는 대신 최소화할 목적함수를 조절해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s3-norms | 일반 | L2는 제곱합의 제곱근, L1은 절댓값 합/희소성; 노름·λ 선택은 데이터마다 다름. | 정규화 항에 쓰는 노름은 여러 가지이고, 무엇을 얼마나 쓸지는 하이퍼파라미터 튜닝으로 정해요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s3-norms | 조건·구분 | L2는 제곱합의 제곱근, L1은 절댓값 합/희소성; 노름·λ 선택은 데이터마다 다름. | $\\|\theta\\|_2^2$은 성분 제곱합이고 $\\|\theta\\|_1$은 절댓값 합이에요. 보충(MML 3.1)의 노름 세 조건과 L1 영역의 꼭짓점에서 좌표가 0이 되는 직관은 수업에서 유도하지 않았어요. Bayesian optimization도 문제마다 성능이 달라요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s3-norms | 보충 | 노름 3공리와 L1 마름모 꼭짓점 직관의 출처/범위는 MML 3.1 보충. | 보충(MML 3.1)의 노름 세 조건과 L1 영역의 꼭짓점에서 좌표가 0이 되는 직관은 수업에서 유도하지 않았어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s3-norms | 주의 | Bayesian optimization은 만능이 아니라 될 때/안될 때가 있다는 교수 발언. | Bayesian optimization도 문제마다 성능이 달라요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s4-likelihood | 일반 | 데이터 고정, 계수의 함수인 likelihood를 최대화; -log 단조 감소로 최소화 형태. | 데이터를 가장 그럴듯하게 만들어 내는 파라미터를 고르는 게 MLE예요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s4-likelihood | 조건·구분 | 데이터 고정, 계수의 함수인 likelihood를 최대화; -log 단조 감소로 최소화 형태. | 데이터는 고정하고 파라미터를 바꾸므로 우도는 파라미터의 함수이며 데이터에 대한 PDF와 읽는 방향이 달라요. 단조증가인 로그에 음수를 붙이면 우도 최대화가 NLL 최소화로 바뀌어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s4-iid | 일반 | 독립이 곱 분해, 같은 분포/파라미터를 사용한 뒤 로그가 합을 만든다. | i.i.d.면 전체 우도가 곱으로 쪼개지고, 로그를 씌우면 합이 돼요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s4-iid | 조건·구분 | 독립이 곱 분해, 같은 분포/파라미터를 사용한 뒤 로그가 합을 만든다. | 독립 가정이 곱 분해를, 동일 분포 가정이 같은 분포·파라미터 사용을 맡아요. 분포 모양을 아직 정하지 않은 일반식이며 다음 계산에는 노이즈 가정이 필요해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s4-mle-ls | 일반 | Gaussian 평균 xᵀθ에 공통 고정 분산인 iid likelihood; NLL 상수와 양의 배율을 빼도 argmin 같음. | 노이즈를 가우시안으로 가정하면 음의 로그우도 최소화가 최소제곱과 같아져요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s4-mle-ls | 조건·구분 | Gaussian 평균 xᵀθ에 공통 고정 분산인 iid likelihood; NLL 상수와 양의 배율을 빼도 argmin 같음. | i.i.d.이며 공통 가우시안 분산 $\sigma^2$를 주어진 값으로 두고 $\boldsymbol{\theta}$를 최적화하는 경우예요. $\boldsymbol{\theta}$와 무관한 상수항과 양의 배율을 제거해도 최소점이 같아요. 보충(MML Example 8.5)의 상수항·argmin 확인은 수업 밖 유도이고, 최소제곱의 닫힌 해는 다음 주 범위예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s4-mle-ls | 보충 | MML Example8.5는 σ가 주어진 값일 때 상수항/argmin 동등성을 확인. | 보충(MML Example 8.5)의 상수항·argmin 확인은 수업 밖 유도이고, 최소제곱의 닫힌 해는 다음 주 범위예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s4-contains | 일반 | 상수는 한점 delta 확률모형; Gaussian MLE/LS 해 동일성은 별개의 특수 사례. | 결정론적 모델은 확률 모델의 특수한 경우라서, 확률 모델이 더 넓어요. | 기존 반영 | pass |
| 정리노트_0914_ERM_and_MLE.html#s4-contains | 조건·구분 | 상수는 한점 delta 확률모형; Gaussian MLE/LS 해 동일성은 별개의 특수 사례. | 상수는 $\delta(x-c)$처럼 한 점에 질량이 모여 불확실성이 없는 경우로 봐요. 가우시안 잡음에서 MLE와 최소제곱 해가 같다는 사실과 이 포함 관계는 구분해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s5-cheatsheet | 일반 | 앞 학습 토픽들을 연결하는 기존 치트시트 표. | N/A: 이 화면 자체가 요약·링크 표다. 별도 .sum을 새로 만들지 않았다. | 해당 없음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s5-next | 일반 | 아직 배우지 않은 다음 시간 범위를 명시한 예고. | N/A: 예고 화면이며 현재 학습 범위 요약으로 전환하지 않았다. | 해당 없음 | pass |
| 정리노트_0914_ERM_and_MLE.html#s5-links | 일반 | 기존 학습·문제·PDF 자료의 링크 모음. | N/A: 링크 화면으로 기존 구조를 유지했다. | 해당 없음 | pass |

## Current regeneration source classification correction (Task6b)

Active content inputs are the published `fragments/pN.html`, copied to RUN `explanations/pN.html` by `mpe_rerender.py` lines 188–206 and read by `mpe_cli.load_fragments`. The files under `evidence/`, including `author.py`, are historical authoring/review evidence; the current build copies them as artifacts and does not execute them. Their six Task6a summary edits were restored only after exact current bytes matched the controller Task6b baseline, retaining all current fragment summaries. No historical author/review script is a renewed approval. Current browser and approval binding remain pending.


## Task6c visible-summary equation line breaks

- `정리노트_0914_ERM_and_MLE.html#s1-goal`: actual summary display equations now `\begin{aligned}f(\mathbf{x}_n,\boldsymbol{\theta}^*)&=\hat y_n\approx y_n,\\&\text{for all }n=1,\dots,N\end{aligned}`. Same-body operators/values/order and conditions were directly reread; no learning-body change.
