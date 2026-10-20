# 본문–요약 수동 감사 0930

이 날짜 실제 본문과 요약을 직접 대조했다. 문제 카드의 원문·힌트·풀이·정답은 보존한다. 같은 핵심의 반복·비유·일화는 생략하고 수업 외 보충의 범위를 명시한다. 외부 원전 전체의 독립 학술 검증은 아니다.

| 자료·토픽 | 구분 | 실제 본문 주장 | 현재 요약 문장 또는 생략 이유 | 보완 전 | 판정 |
|---|---|---|---|---|---|
| 문제설명_0930_Bayesian_Linear_Regression.html#p1 | 일반 | Y=X², E[X]=E[X³]=0을 공분산 정의에 넣어0이며 퇴화 상수 예외와 종속 반례를 구별한다. | 주어진 두 모멘트가0이므로 공분산은0이에요. | 기존 반영 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p1 | 주의·조건 | 공분산 계산의 유한 모멘트 조건과 함수가 상수인 퇴화 독립사례를 구별한다. | 관련 기댓값은 유한하다고 전제해요. 공분산 $0$에서 독립을 결론내리지 않으며, $X^2$가 상수인 퇴화 사례와 구별해요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p2 | 일반 | 독립 가우시안의 가중합: 평균 가중합과 계수제곱 공분산합, 주어진 가우시안성으로 분포 확정. | 독립으로 교차항이0이라 제시한 평균·공분산이 남아요. | 기존 반영 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p2 | 주의·조건 | 주어진 가우시안성을 이용하며 독립과 같은차원 가정으로 계수제곱 공분산이 성립한다. | 가중합이 가우시안이라는 사실은 문제에서 주어졌어요. 같은 차원의 독립 벡터이므로 교차항이 $0$이고, 평균은 $a\mu_x+b\mu_y$, 공분산은 $a^2\Sigma_x+b^2\Sigma_y$예요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p3 | 일반 | 현재 posterior를 A로 변환하고 독립 새 잡음Q를 더한 과거조건부 한걸음 예측. | 한 걸음 예측(predictive distribution)은 현재 posterior를 선형 변환하고 새 독립 잡음을 더해요. | 기존 반영 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p3 | 주의·조건 | 과거측정 조건부 상태예측이며 아직 관측하지 않은 측정행렬/잡음항을 더하지 않는다. | 모든 평균·공분산은 시각 $t$까지 관측한 측정값을 조건으로 해요. 아직 다음 관측을 보지 않았으므로 상태 예측분산에는 $Q$를 더하며 $R$이나 $C$를 더하지 않아요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p4 | 일반 | 편차제곱을 전개하고 μ=E[X] 상수로 취급해 E[X²]−μ²를 얻는다. | 선형성으로 E[X²]−2μE[X]+μ²=E[X²]−μ²예요. | 기존 반영 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p4 | 주의·조건 | 이차모멘트 유한 조건과 제곱의 평균/평균의 제곱 구별. | 이차 모멘트가 유한하다고 전제해요. $E[X^2]$와 $(E[X])^2$는 일반적으로 달라요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p5 | 일반 | 입력고정 조건부는 독립잡음만 랜덤하므로 N(Ax+b,Q). | x를 고정하면 y−(Ax+b)=w예요. | 기존 반영 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p5 | 주의·조건 | 입력고정이면 잡음만 남는 조건부 공분산과 입력불확실성을 포함하는 주변공분산 구별. | 잡음은 입력과 독립이므로 입력을 고정해도 공분산은 $Q$예요. $A\Sigma_xA^{\top}$는 입력까지 랜덤하게 평균낸 주변분포에서 생기는 항이라 조건부 가능도에 더하지 않아요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p6 | 일반 | 주변 평균은 Aμx+b, 공분산은 AΣxAᵀ+Q; 성분 계산과 E×E차원으로 확인. | 성분(i,j)은 ∑kl A_ik Cov(x_k,x_l)A_jl+Q_ij예요. | 기존 반영 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p6 | 주의·조건 | 독립잡음 교차항0을 이용해 Q를 더하며 행렬곱 순서를 유지한다. | 독립인 잡음으로 교차항이 사라져 $\mu_y=A\mu_x+b$, $\Sigma_y=A\Sigma_xA^{\top}+Q$예요. 행렬 곱 순서를 지키며 $A\Sigma_xA^{\top}$를 $AA^{\top}\Sigma_x$로 바꾸지 않아요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p7 | 일반 | z=Cy+v 조건부는 N(Cy,R), 주변은 Cμy,CΣyCᵀ+R이고 y의 결과를 대입한다. | y 고정 뒤 v만 변하므로 N(Cy,R)예요. | 기존 반영 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p7 | 주의·조건 | 측정잡음은 변환 뒤 들어오므로 R을 C로 변환하지 않는다. | 측정 잡음은 $C$로 변환한 뒤 더하므로 $R$을 다시 $C$로 감싸지 않아요. 조건부는 $\mathcal{N}(Cy,R)$, 주변 공분산은 $C\Sigma_yC^{\top}+R$예요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p8 | 일반 | 모든 순서쌍 제곱차를 세 항으로 전개하여 2N∑xi²−2(∑xi)²를 N²으로 나눈다. | 두 제곱항은 각각N번씩 반복되고 교차항은 합의 제곱으로 분리돼요. | 기존 반영 | pass |
| 문제설명_0930_Bayesian_Linear_Regression.html#p8 | 주의·조건 | 양의 N과 모든 순서쌍 가정; 분모N 경험분산과 N−1 불편분산은 다르다. | $N>0$이고 모든 순서쌍을 포함해요. 분모 $N$인 경험분산의 항등식이므로 불편분산의 $N-1$로 바꾸지 않아요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 복습문제_0930_Bayesian_Linear_Regression.html#p1 | 일반 | Y=X², E[X]=E[X³]=0을 공분산 정의에 넣어0이며 퇴화 상수 예외와 종속 반례를 구별한다. | N/A: 원래 요약 없는 문제 카드. 원문·힌트·풀이·정답의 기존 구조를 유지한다. | 해당 없음 | pass |
| 복습문제_0930_Bayesian_Linear_Regression.html#p2 | 일반 | 독립 가우시안의 가중합: 평균 가중합과 계수제곱 공분산합, 주어진 가우시안성으로 분포 확정. | N/A: 원래 요약 없는 문제 카드. 원문·힌트·풀이·정답의 기존 구조를 유지한다. | 해당 없음 | pass |
| 복습문제_0930_Bayesian_Linear_Regression.html#p3 | 일반 | 현재 posterior를 A로 변환하고 독립 새 잡음Q를 더한 과거조건부 한걸음 예측. | N/A: 원래 요약 없는 문제 카드. 원문·힌트·풀이·정답의 기존 구조를 유지한다. | 해당 없음 | pass |
| 복습문제_0930_Bayesian_Linear_Regression.html#p4 | 일반 | 편차제곱을 전개하고 μ=E[X] 상수로 취급해 E[X²]−μ²를 얻는다. | N/A: 원래 요약 없는 문제 카드. 원문·힌트·풀이·정답의 기존 구조를 유지한다. | 해당 없음 | pass |
| 복습문제_0930_Bayesian_Linear_Regression.html#p5 | 일반 | 입력고정 조건부는 독립잡음만 랜덤하므로 N(Ax+b,Q). | N/A: 원래 요약 없는 문제 카드. 원문·힌트·풀이·정답의 기존 구조를 유지한다. | 해당 없음 | pass |
| 복습문제_0930_Bayesian_Linear_Regression.html#p6 | 일반 | 주변 평균은 Aμx+b, 공분산은 AΣxAᵀ+Q; 성분 계산과 E×E차원으로 확인. | N/A: 원래 요약 없는 문제 카드. 원문·힌트·풀이·정답의 기존 구조를 유지한다. | 해당 없음 | pass |
| 복습문제_0930_Bayesian_Linear_Regression.html#p7 | 일반 | z=Cy+v 조건부는 N(Cy,R), 주변은 Cμy,CΣyCᵀ+R이고 y의 결과를 대입한다. | N/A: 원래 요약 없는 문제 카드. 원문·힌트·풀이·정답의 기존 구조를 유지한다. | 해당 없음 | pass |
| 복습문제_0930_Bayesian_Linear_Regression.html#p8 | 일반 | 모든 순서쌍 제곱차를 세 항으로 전개하여 2N∑xi²−2(∑xi)²를 N²으로 나눈다. | N/A: 원래 요약 없는 문제 카드. 원문·힌트·풀이·정답의 기존 구조를 유지한다. | 해당 없음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s0-learning-map | 일반 | 파라미터 분포와 새 출력 예측분포는 다른 대상이며 평균·공분산 도구를 준비한다. | 파라미터의 분포와 새 관측값의 분포는 대상이 달라요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s0-learning-map | 구분 | MAP은 posterior mode 하나, FB는 후보 예측밀도들을 가중평균하며 θ 평균대입과 다르다. | MAP은 사후분포의 최고점 하나를 고르고, FB는 파라미터 분포를 유지해 가능한 예측분포를 가중해 모아요. 파라미터 평균 하나만 대입한다는 뜻은 아니에요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s0-cond-prob | 일반 | 곱셈 법칙 확장은 결과 B를 조건으로 옮기고 P(B\|C)를 곱하며 원 조건 C는 모든 항에 남긴다. | 결과 자리의 사건을 조건으로 옮기고 그 사건의 확률을 곱하면 되고, 이미 있던 조건은 모든 항에 그대로 남아요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s0-cond-prob | 강조 | 교수는 정의 하나에서 곱셈 법칙을 유도할 수 있어야 한다고 강조했다. | 조건부확률의 정의 | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s0-why-bayes | 일반 | 확률로 불확실성을 PDF에 담으며 베이지안 선형회귀는 파라미터 분포 전체로 예측한다. | 베이지안은 확률을 도입해 "이럴 수도, 저럴 수도 있다"를 정확하게 말하는 방법이고, 그 내용은 확률밀도함수(PDF)에 모두 담겨요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s0-why-bayes | 구분 | 입력 피처가 아니라 θ에 대한 선형성을 뜻하며 분포전체 사용이 점추정과 다르다. | 이 회귀의 선형성은 $\boldsymbol{\theta}$에 대한 선형성이에요. ML·MAP은 파라미터 값 하나를 구했고, 베이지안 선형회귀는 분포 전체를 써서 예측해요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s0-fully-bayesian | 일반 | FB는 θ를 랜덤 벡터로 유지하며 ML/MAP은 한 값을 결정한다. | 풀리 베이지안은 파라미터를 값 하나로 정하지 않고 랜덤 벡터로 두어 결정을 유보해요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s0-fully-bayesian | 구분 | 분산0 극한의 델타 함수로 점 추정을 표현하며 본문에서 세 방법의 포함 관계로 설명한다. | 분산을 $0$으로 보낸 PDF, 곧 확실한 상수 | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s1-graphical | 일반 | m0/S0→θ, θ와 입력·잡음→y의 모델 구조로 읽고 θ의 평균/공분산을 구별한다. | 화살표를 따라 $\mathbf{m}_0$, $\mathbf{S}_0$에서 $\boldsymbol{\theta}$로, $\boldsymbol{\theta}$와 $\mathbf{x}$와 노이즈에서 $y$로 이야기를 읽어요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s1-graphical | 구분 | 관측 출력/숨은 파라미터/분포 하이퍼파라미터를 노드별로 구별한다. | $y$는 관측 출력, $\boldsymbol{\theta}$는 숨은 모델 파라미터예요. $\mathbf{m}_0$, $\mathbf{S}_0$, $\sigma$는 분포 모양을 밖에서 정하는 하이퍼파라미터 쪽이에요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s1-prior-likelihood | 일반 | 가우시안 파라미터 사전과 입력/θ 조건부 출력 가능도 두 분포가 모델이다. | 모델은 $\boldsymbol{\theta}$에 대한 사전분포와, $\mathbf{x}$와 $\boldsymbol{\theta}$가 주어졌을 때의 가능도 두 개로 적어요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s1-prior-likelihood | 조건 | θ와 입력고정 뒤의 출력평균은 φᵀθ이고 0평균은 잡음에 해당한다. | 입력과 $\boldsymbol{\theta}$를 고정하면 가능도의 평균은 $\boldsymbol{\phi}^{\top}(\mathbf{x})\boldsymbol{\theta}$, 분산은 $\sigma^2$예요. 평균 $0$인 것은 잡음이에요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s1-prior-likelihood | 구분 | 비선형 피처 허용과 θ 선형성 기준. | 피처 함수는 비선형이어도 $\boldsymbol{\theta}$에 대해 선형이면 선형회귀예요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s1-joint | 일반 | 체인룰의 p(θ\|x)를 p(θ)로 바꾸려면 θ와 x 독립이라는 모델 가정이 필요하다. | 조인트는 조건부확률의 정의로 풀고, 입력만으로는 $\boldsymbol{\theta}$가 바뀌지 않는다는 독립 가정을 넣어 가능도와 사전분포의 곱으로 써요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s1-joint | 주의 | 조건부 정의 자체와 입력독립이라는 모델가정은 구별된다. | 독립 가정 전의 정확한 둘째 항은 $p(\boldsymbol{\theta}\mid\mathbf{x})$예요. 이 항을 $p(\boldsymbol{\theta})$로 바꾸는 것은 모델에 따라 달라지는 가정이에요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s2-goal | 일반 | 모든 관측입출력과 새 입력은 조건에 두고 구할 새 출력 PDF는 결과에 둔다. | 가진 것은 모두 조건에, 궁금한 $y_*$는 결과에 쓰면 예측 목표가 식 하나로 정리돼요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s2-marginalize | 일반 | θ를 결과 위치에 도입한 joint를 적분하며 조건은 고정해 남긴다. | 없던 $\boldsymbol{\theta}$를 바의 왼쪽(주인공 자리)에 넣고 적분하면 원래 식과 같아요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s2-marginalize | 조건 | 주변화의 조건은 고정되고 결과 변수만 적분으로 제거된다. | 조건 $z$는 고정해 남겨 두고 결과 자리의 $y$를 적분해 없애요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s2-marginalize | 보충 | 수업에서 미룬 조건부 주변화 증명은 양의 p(z), 고정분모와 무조건 주변화로 정리한다. | 수업 외 보충 증명은 $p(z)\gt0$에서 조건부 정의를 풀고 $p(z)$를 적분 밖으로 꺼낸 뒤 $\int p(x,y,z)\,dy=p(x,z)$를 써요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s2-predictive | 일반 | 예측은 likelihood에 파라미터 posterior를 곱해 θ로 적분한다. | 조인트를 곱셈 법칙으로 쪼개고 두 가정을 넣으면, 사후 예측분포는 likelihood와 $\boldsymbol{\theta}$의 조건부 PDF를 곱해 $\boldsymbol{\theta}$로 적분한 식이 돼요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s2-predictive | 조건 | θ와 새 입력이 주어지면 학습자료 생략; 출력 없는 새 입력은 posterior를 바꾸지 않는 두 가정을 각각 쓴다. | 가정 ① | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s2-cond-expectation | 일반 | 예측밀도는 posterior 가중치로 likelihood 함수를 평균낸 조건부기댓값이다. | 사후 예측분포는 likelihood를 $\boldsymbol{\theta}$의 분포로 평균 낸 조건부 기댓값이고, ML · MAP은 그 분포가 델타 함수인 경우예요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s2-cond-expectation | 구분 | θ를 한 값에 둔 델타 가중치면 점추정 likelihood 하나가 된다. | 값 하나에만 서 있는 PDF. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s2-cond-expectation | 구분 | θ를 주변화해도 y*의 불확실성은 남으며 마지막 결정만 최빈값/평균으로 할 수 있다. | 적분으로 사라지는 것은 $\boldsymbol{\theta}$이고 새 출력 $y_*$의 불확실성은 PDF로 남아요. 값 하나가 필요하면 마지막에 이 PDF의 최대점이나 평균으로 결정해요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s2-cond-expectation | 예시 범위 | 세 후보 가우시안의 숫자는 실제 연속 θ를 설명하려고 노트가 설정한 값이다. | 세 후보의 평균 $-2,0,2$와 표준편차 $0.6$은 위젯을 위해 노트가 정한 예시예요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s3-gaussian-scalar | 일반 | 스칼라 가우시안은 평균과 분산 두 수로 정해지고 표준정규는 평균0 분산1이다. | 가우시안 PDF는 종 모양이라서 평균과 분산, 숫자 두 개로 전체를 전할 수 있어요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s3-gaussian-scalar | 구분 | 표준편차와 분산의 구별 및 σ감소의 폭/높이 효과. | 꼭대기는 $\mu$, 높이는 $1/\sqrt{2\pi\sigma^2}$예요. 표준편차 $\sigma$를 줄이면 좁고 높아져요. 본문 예의 $\sigma=0.1$과 분산 $\sigma^2$를 구별해요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s3-random-vector | 일반 | 확률변수를 열로 쌓은 joint PDF는 전 공간 적분1이고 평균벡터는 성분별 평균이다. | 확률변수 여러 개를 쌓으면 랜덤 벡터가 되고, 그 joint PDF가 모든 문제의 설계도예요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s3-random-vector | 구분 | 성분별 평균을 같은 순서로 쌓는 평균벡터. | 성분마다 평균을 구해 쌓은 벡터 | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s3-covariance | 일반 | 벡터 교차공분산의 (i,j)는 Cov(Xi,Yj), 결과는 n×m이다. | 공분산은 곱의 평균 빼기 평균의 곱이고, 벡터끼리는 성분 쌍마다 계산해 행렬에 넣어요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s3-covariance | 조건·차원 | Cov(x,y)=E[xyᵀ]−E[x]E[y]ᵀ이고 n×m; 외적과 성분별 기댓값으로 정의와 맞는다. | \mathbb{R}^{n \times m} | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s3-variance-matrix | 일반 | 자기 공분산은 n×n 대칭행렬이며 대각은 각 성분 분산이다. | 랜덤 벡터의 분산은 자기 자신과의 공분산 행렬이고, 항상 대칭인 정방행렬이에요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s3-variance-matrix | 구분 | 대각의 분산과 비대각 대칭성을 구별하며 대칭과 대각행렬/대각화는 다르다. | 대각 원소는 각 성분의 분산이에요. 대칭은 마주 보는 공분산이 같다는 뜻이며 대각행렬·대각화와는 달라요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s4-sum | 일반 | 같은 크기 벡터의 합 평균은 기댓값 선형성으로 더한다. | 합의 평균은 늘 더하면 되지만, 합의 분산은 독립이거나 공분산이 영행렬이면 더하면 돼요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s4-sum | 강조 | 교수는 합 분산 공식의 성립조건/증명을 중간고사 후보로 강조했다. | 합의 분산 (조건 필요) | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s4-sum | 보충 | 일반 합 공분산은 자기항 둘에 교차항 둘을 더하며 실제 필요한 것은 교차항의 합0이다. | 수업 외 보충의 일반형에는 $\operatorname{Cov}[\mathbf{x},\mathbf{y}]+\operatorname{Cov}[\mathbf{y},\mathbf{x}]$가 더 붙어요. 분산을 그냥 더하려면 이 두 교차항의 합이 영행렬이어야 해요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s4-sum | 주의 | 독립과 영교차공분산은 충분조건이고 영공분산에서 독립 역추론은 안 된다. | 교차공분산 자체가 영행렬이면 충분하고 독립도 충분하지만, 공분산이 영행렬이라고 독립인 것은 아니에요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s4-affine | 일반 | 상수행렬 A, 상수 b의 아핀변환은 평균 Aμ+b, 공분산 AΣAᵀ이다. | 아핀 변환을 하면 평균은 같은 변환을 그대로 따르고, 공분산 행렬은 양옆에 행렬이 곱해져요. | 기존 반영 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s4-affine | 조건·차원 | 상수 A:m×n,b:m에 n벡터를 변환하여 m벡터를 얻고 이동은 편차에서 지워진다. | $\mathbf{x}\in\mathbb{R}^n$, $\mathbf{A}\in\mathbb{R}^{m\times n}$, $\mathbf{b}\in\mathbb{R}^m$이고 $\mathbf{A},\mathbf{b}$는 상수예요. 평균에서 $\mathbf{b}$를 빼면 이동이 지워져 분산에 영향이 없어요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s4-affine | 주의 | 공분산 행렬은 AΣAᵀ 순서이고 AAᵀΣ로 모을 수 없다. | 행렬 곱 순서를 지켜 $\mathbf{A}\Sigma\mathbf{A}^{\top}$로 쓰며 일반적으로 $\mathbf{A}\mathbf{A}^{\top}\Sigma$로 바꾸지 않아요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s4-affine | 보충 | 행별 공분산을 모아 행렬식 증명 마무리 및 스칼라 a²분산은 수업 외 유도이다. | 수업 외 보충은 각 공분산 원소를 $\mathbf{a}_i^{\top}\mathbb{V}[\mathbf{x}]\mathbf{a}_j$로 모아 행렬식을 완성하고, 스칼라에서는 $a^2\mathbb{V}[X]$가 됨을 증명해요. | unresolved → 보완 후 실제 요약 다시 읽음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s5-cheatsheet | 일반 | 기존 학습 핵심 식을 모아 해당 토픽에 연결하는 치트시트. | N/A: 이 화면 자체가 요약 표이므로 별도 .sum을 만들지 않는다. | 해당 없음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s5-next | 일반 | 아직 배우지 않은 범위와 다음 수업/숙제를 구별해 적은 예고. | N/A: 학습 완료 요약이 아닌 기존 예고 화면을 유지한다. | 해당 없음 | pass |
| 정리노트_0930_Bayesian_Linear_Regression.html#s5-links | 일반 | 관련 학습자료와 문제·PDF 링크 모음. | N/A: 링크 화면의 기존 구조를 유지한다. | 해당 없음 | pass |

## 현행 원고 경로

현재 재생성의 내용 입력은 해당 자료 폴더의 `fragments/pN.html`이다. `mpe_rerender.py:188–206`이 이를 RUN의 `explanations/pN.html`로 복사하고 `mpe_cli.load_fragments`가 읽는다. `evidence/author.py` 및 검토 로그는 실행하지 않는 과거 증거이며 수정하지 않는다. 별도 날짜별 정리노트 section 원고는 이 폴더에 없고 정리노트 HTML이 현행 저작 내용이다. 브라우저·독립 승인·배포 바인딩은 후속 검증까지 pending이다.


## Task6c visible-summary equation line breaks

- `정리노트_0930_Bayesian_Linear_Regression.html#s2-predictive`: actual summary display equations now `\begin{aligned}&p(y_*\mid\boldsymbol\theta,\mathbf x_*,\mathcal X,\mathcal Y)\\&=p(y_*\mid\mathbf x_*,\boldsymbol\theta)\end{aligned}` / `\begin{aligned}&p(\boldsymbol\theta\mid\mathbf x_*,\mathcal X,\mathcal Y)\\&=p(\boldsymbol\theta\mid\mathcal X,\mathcal Y)\end{aligned}` / `\begin{aligned}&p(y_*\mid\mathbf x_*,\mathcal X,\mathcal Y)\\&=\int p(y_*\mid\mathbf x_*,\boldsymbol\theta)\\&\quad{}\cdot p(\boldsymbol\theta\mid\mathcal X,\mathcal Y)\,d\boldsymbol\theta\end{aligned}`. Same-body operators/values/order and conditions were directly reread; no learning-body change.
