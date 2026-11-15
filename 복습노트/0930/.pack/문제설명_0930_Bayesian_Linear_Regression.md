# 머신러닝기초 복습 0930 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [P1. 종속인데 공분산이 0인 경우](#p1)
  - [P2. 독립인 가우시안의 가중합](#p2)
  - [P3. 시계열 모델에서 한 걸음 앞 예측하기](#p3)
  - [P4. 분산은 제곱의 평균 빼기 평균의 제곱](#p4)
  - [P5. 노이즈가 섞인 선형 변환의 가능도](#p5)
  - [P6. 노이즈가 섞인 선형 변환의 평균과 공분산](#p6)
  - [P7. 한 번 더 변환해서 측정하기](#p7)
  - [P8. 쌍끼리의 차이로 보는 분산](#p8)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### P1. 종속인데 공분산이 0인 경우

MML Example 6.5 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0930_Bayesian_Linear_Regression-%EB%AC%B8%EC%A0%9C.pdf#page=1)

#### 주어진 조건

확률변수 $X$는 평균이 0이고($\mathbb{E}[x] = 0$), 세제곱의 평균도 0이에요($\mathbb{E}[x^3] = 0$). 새 확률변수를 $y = x^2$으로 만들어요. $y$는 $x$로 정해지니까 $Y$는 $X$에 종속이에요.

#### 구할 것

이때 $X$와 $Y$의 공분산 $\operatorname{Cov}[x, y]$를 구해 보세요.

#### 무엇을 구하는 문제인가요?

종속인데 공분산이 0인 경우를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

공분산(covariance)은 $Cov(X,Y)=E[XY]-E[X]E[Y]$예요. Y=X²이면 XY=X³라 주어진1차·3차 모멘트를 바로 쓸 수 있어요. 관련 기댓값은 유한하다고 전제해요.

#### 종이에 적을 첫 줄

$Cov(X,X^2)=E[X^3]-E[X]E[X^2]$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

공분산 식을 적어요.

$$
\operatorname{Cov}[x, y] = \mathbb{E}[xy] - \mathbb{E}[x]\,\mathbb{E}[y]
$$

$y = x^2$을 넣으면 $xy = x \cdot x^2 = x^3$이에요. 그래서 첫 항은 $\mathbb{E}[xy] = \mathbb{E}[x^3]$이에요.

둘째 항은 $\mathbb{E}[x]\,\mathbb{E}[y] = \mathbb{E}[x]\,\mathbb{E}[x^2]$이에요. $\mathbb{E}[x] = 0$이라서 $\mathbb{E}[x^2]$이 얼마든 이 항은 0이에요.

문제에서 $\mathbb{E}[x^3] = 0$이라고 했어요. 두 항을 합치면

$$
\operatorname{Cov}[x, y] = \mathbb{E}[x^3] - \mathbb{E}[x]\,\mathbb{E}[x^2] = 0 - 0 = 0
$$

그런데 $X$와 $Y$는 독립이 아니에요. $x$를 알면 $y = x^2$이 바로 정해지기 때문이에요. 공분산이 0이어도 독립이라고 말할 수는 없어요.

수업과의 연결: 0930 수업의 $\operatorname{Cov}[X, Y] = \mathbb{E}[XY] - \mathbb{E}[X]\,\mathbb{E}[Y]$를 그대로 쓴 거예요. 합의 분산 식에 붙인 조건 "독립이거나, 적어도 공분산이 0"에서 두 조건이 서로 다른 말이라는 걸 보여 주는 예예요.

#### 완성 답과 검산

#### 검산

주어진 두 모멘트가0이므로 공분산은0이에요. 종속의 예로 X가−1,0,1을 각각1/3로 가지면 X²가 변하며 X에서 결정돼 독립이 아니에요. 반면 X=±1만 가지면 Y=1로 상수예요.

정답: $\operatorname{Cov}[x, y] = \mathbb{E}[x^3] - \mathbb{E}[x]\,\mathbb{E}[x^2] = 0$ ($Y$는 $X$에 종속이지만 공분산은 0이에요.)

#### 여기서 주의해요

공분산0에서 독립을 결론내리지 않아요. Y=X²여도 X²가 상수인 퇴화 사례는 독립일 수 있어요.

#### 설명을 닫고 다시 해요

1. $Cov(X,X^2)=E[X^3]-E[X]E[X^2]$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 공분산0에서 독립을 결론내리지 않아요. Y=X²여도 X²가 상수인 퇴화 사례는 독립일 수 있어요.

**페이지 요약**

#### 떠올릴 개념·공식

공분산(covariance)은 $Cov(X,Y)=E[XY]-E[X]E[Y]$예요.

#### 첫 줄

$Cov(X,X^2)=E[X^3]-E[X]E[X^2]$예요.

#### 검산

주어진 두 모멘트가0이므로 공분산은0이에요. 종속의 예로 X가−1,0,1을 각각1/3로 가지면 X²가 변하며 X에서 결정돼 독립이 아니에요. 반면 X=±1만 가지면 Y=1로 상수예요.

#### 조건·구분

관련 기댓값은 유한하다고 전제해요. 공분산 $0$에서 독립을 결론내리지 않으며, $X^2$가 상수인 퇴화 사례와 구별해요.

---

<a id="p2"></a>

### P2. 독립인 가우시안의 가중합

MML Example 6.7 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0930_Bayesian_Linear_Regression-%EB%AC%B8%EC%A0%9C.pdf#page=2)

#### 주어진 조건

서로 독립인 가우시안 확률변수 $\mathbf{x}$와 $\mathbf{y}$가 있어요. $\mathbf{x}$의 평균은 $\boldsymbol{\mu}_x$, 공분산 행렬은 $\boldsymbol{\Sigma}_x$이고, $\mathbf{y}$의 평균은 $\boldsymbol{\mu}_y$, 공분산 행렬은 $\boldsymbol{\Sigma}_y$예요. 상수 $a$, $b$로 가중합 $a\mathbf{x} + b\mathbf{y}$를 만들어요. 이 가중합도 가우시안이라는 사실은 주어진 것으로 써요.

#### 구할 것

가중합의 평균과 공분산 행렬을 구해서 $p(a\mathbf{x} + b\mathbf{y})$를 적어 보세요.

#### 무엇을 구하는 문제인가요?

독립인 가우시안의 가중합를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

기댓값은 계수를 그대로 통과하지만 분산은 두 편차를 곱하므로 계수가 제곱돼요. 같은 차원의 독립 벡터에 대해 $Var(aX+bY)=a^2\Sigma_x+b^2\Sigma_y$예요. 독립이 교차항을0으로 만들어요.

#### 종이에 적을 첫 줄

$E[aX+bY]=a\mu_x+b\mu_y$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

평균부터 구해요. 기댓값은 합과 상수배를 그대로 통과시켜요.

$$
\mathbb{E}[a\mathbf{x} + b\mathbf{y}] = a\,\mathbb{E}[\mathbf{x}] + b\,\mathbb{E}[\mathbf{y}] = a\boldsymbol{\mu}_x + b\boldsymbol{\mu}_y
$$

$a\mathbf{x}$는 $\mathbf{A} = a\mathbf{I}$, $\mathbf{b} = \mathbf{0}$인 아핀 변환이에요. 그래서

$$
\mathbb{V}[a\mathbf{x}] = (a\mathbf{I})\,\boldsymbol{\Sigma}_x\,(a\mathbf{I})^\top = a^2\boldsymbol{\Sigma}_x
$$

같은 방법으로 $\mathbb{V}[b\mathbf{y}] = b^2\boldsymbol{\Sigma}_y$예요.

$a\mathbf{x}$와 $b\mathbf{y}$ 사이의 공분산을 확인해요.

$$
\operatorname{Cov}[a\mathbf{x}, b\mathbf{y}] = \mathbb{E}[a\mathbf{x}\,b\mathbf{y}^\top] - \mathbb{E}[a\mathbf{x}]\,\mathbb{E}[b\mathbf{y}]^\top = ab\,\operatorname{Cov}[\mathbf{x}, \mathbf{y}]
$$

$\mathbf{x}$와 $\mathbf{y}$가 독립이라서 $\operatorname{Cov}[\mathbf{x}, \mathbf{y}] = \mathbf{0}$이고, 이 값도 $\mathbf{0}$이에요.

교차 공분산이 0이니까 합의 분산은 분산의 합이에요.

$$
\mathbb{V}[a\mathbf{x} + b\mathbf{y}] = \mathbb{V}[a\mathbf{x}] + \mathbb{V}[b\mathbf{y}] = a^2\boldsymbol{\Sigma}_x + b^2\boldsymbol{\Sigma}_y
$$

가중합이 가우시안이라는 사실은 주어졌어요. 가우시안은 평균과 공분산만 알면 정해지니까

$$
p(a\mathbf{x} + b\mathbf{y}) = \mathcal{N}\big(a\boldsymbol{\mu}_x + b\boldsymbol{\mu}_y,\; a^2\boldsymbol{\Sigma}_x + b^2\boldsymbol{\Sigma}_y\big)
$$

수업과의 연결: 0930 수업의 "상수는 분산에서 제곱해서 나온다"($\mathbb{V}[aX] = a^2\,\mathbb{V}[X]$)와, 독립이거나 적어도 공분산이 0일 때 쓸 수 있다고 한 $\mathbb{V}[\mathbf{x} + \mathbf{y}] = \mathbb{V}[\mathbf{x}] + \mathbb{V}[\mathbf{y}]$를 이어 쓴 거예요.

#### 완성 답과 검산

#### 검산

편차 a(X−μx)+b(Y−μy)의 외적을 펼치면 자기항2개와 교차항2개예요. 독립으로 교차항이0이라 제시한 평균·공분산이 남아요.

정답: $p(a\mathbf{x} + b\mathbf{y}) = \mathcal{N}\big(a\boldsymbol{\mu}_x + b\boldsymbol{\mu}_y,\; a^2\boldsymbol{\Sigma}_x + b^2\boldsymbol{\Sigma}_y\big)$

#### 여기서 주의해요

분산에 a,b를 그대로 곱하지 않아요. 같은 차원이라도 공분산 순서를 임의로 바꾸지 않아요.

#### 설명을 닫고 다시 해요

1. $E[aX+bY]=a\mu_x+b\mu_y$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 분산에 a,b를 그대로 곱하지 않아요. 같은 차원이라도 공분산 순서를 임의로 바꾸지 않아요.

**페이지 요약**

#### 떠올릴 개념·공식

기댓값은 계수를 그대로 통과하지만 분산은 두 편차를 곱하므로 계수가 제곱돼요. 같은 차원의 독립 벡터에 대해 $Var(aX+bY)=a^2\Sigma_x+b^2\Sigma_y$예요.

#### 첫 줄

$E[aX+bY]=a\mu_x+b\mu_y$예요.

#### 검산

편차 a(X−μx)+b(Y−μy)의 외적을 펼치면 자기항2개와 교차항2개예요. 독립으로 교차항이0이라 제시한 평균·공분산이 남아요.

#### 조건·구분

가중합이 가우시안이라는 사실은 문제에서 주어졌어요. 같은 차원의 독립 벡터이므로 교차항이 $0$이고, 평균은 $a\mu_x+b\mu_y$, 공분산은 $a^2\Sigma_x+b^2\Sigma_y$예요.

---

<a id="p3"></a>

### P3. 시계열 모델에서 한 걸음 앞 예측하기

MML Exercise 6.5 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0930_Bayesian_Linear_Regression-%EB%AC%B8%EC%A0%9C.pdf#page=3)

#### 주어진 조건

시간에 따라 변하는 상태 $\mathbf{x}_t$를 아래 시계열 모델로 나타내요.

$$
\mathbf{x}_{t+1} = \mathbf{A}\mathbf{x}_t + \mathbf{w}, \quad \mathbf{w} \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})
$$

$$
\mathbf{y}_t = \mathbf{C}\mathbf{x}_t + \mathbf{v}, \quad \mathbf{v} \sim \mathcal{N}(\mathbf{0}, \mathbf{R})
$$

$\mathbf{A}$, $\mathbf{C}$는 상수 행렬이고, $\mathbf{w}$, $\mathbf{v}$는 상태와 독립인 가우시안 노이즈예요. $\mathbf{y}_t$는 상태를 측정한 값이에요. 시각 $t$까지의 측정값을 본 뒤 $\mathbf{x}_t$의 분포가 $p(\mathbf{x}_t \mid \mathbf{y}_1, \dots, \mathbf{y}_t) = \mathcal{N}(\boldsymbol{\mu}_t, \boldsymbol{\Sigma}_t)$라고 해요.

#### 구할 것

같은 측정값만 가지고 다음 상태의 분포 $p(\mathbf{x}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t)$를 구해 보세요. 이 분포가 가우시안이라는 사실은 주어진 것으로 써요.

#### 무엇을 구하는 문제인가요?

시계열 모델에서 한 걸음 앞 예측하기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

한 걸음 예측(predictive distribution)은 현재 posterior를 선형 변환하고 새 독립 잡음을 더해요. $\mu_{t+1}=A\mu_t$, $P=A\Sigma_tA^\top+Q$예요. 모든 평균·공분산은 과거 관측을 조건으로 계산해요.

#### 종이에 적을 첫 줄

$x_{t+1}-A\mu_t=A(x_t-\mu_t)+w$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

아래의 평균과 분산은 모두 $\mathbf{y}_1, \dots, \mathbf{y}_t$를 본 상태에서 계산해요. 이때 $\mathbb{E}[\mathbf{x}_t] = \boldsymbol{\mu}_t$, $\mathbb{V}[\mathbf{x}_t] = \boldsymbol{\Sigma}_t$예요.

평균은 합을 그대로 통과해요. 아핀 변환 규칙과 $\mathbb{E}[\mathbf{w}] = \mathbf{0}$을 써요.

$$
\mathbb{E}[\mathbf{x}_{t+1}] = \mathbf{A}\,\mathbb{E}[\mathbf{x}_t] + \mathbb{E}[\mathbf{w}] = \mathbf{A}\boldsymbol{\mu}_t
$$

$\mathbf{A}\mathbf{x}_t$의 공분산 행렬은 아핀 변환 규칙으로 구해요.

$$
\mathbb{V}[\mathbf{A}\mathbf{x}_t] = \mathbf{A}\,\mathbb{V}[\mathbf{x}_t]\,\mathbf{A}^\top = \mathbf{A}\boldsymbol{\Sigma}_t\mathbf{A}^\top
$$

$\mathbf{A}\mathbf{x}_t$와 $\mathbf{w}$ 사이의 공분산을 확인해요. $\mathbb{E}[\mathbf{w}] = \mathbf{0}$이라서

$$
\operatorname{Cov}[\mathbf{A}\mathbf{x}_t, \mathbf{w}] = \mathbb{E}[\mathbf{A}\mathbf{x}_t\mathbf{w}^\top] - \mathbb{E}[\mathbf{A}\mathbf{x}_t]\,\mathbb{E}[\mathbf{w}]^\top = \mathbf{A}\,\mathbb{E}[\mathbf{x}_t\mathbf{w}^\top]
$$

$\mathbf{x}_t$와 $\mathbf{w}$가 독립이라 $\mathbb{E}[\mathbf{x}_t\mathbf{w}^\top] = \mathbb{E}[\mathbf{x}_t]\,\mathbb{E}[\mathbf{w}]^\top = \mathbf{0}$이에요. 그래서 $\operatorname{Cov}[\mathbf{A}\mathbf{x}_t, \mathbf{w}] = \mathbf{0}$이에요.

교차 공분산이 0이니까 합의 분산은 분산의 합이에요. $\mathbb{V}[\mathbf{w}] = \mathbf{Q}$를 넣어요.

$$
\mathbb{V}[\mathbf{x}_{t+1}] = \mathbb{V}[\mathbf{A}\mathbf{x}_t] + \mathbb{V}[\mathbf{w}] = \mathbf{A}\boldsymbol{\Sigma}_t\mathbf{A}^\top + \mathbf{Q}
$$

가우시안이라는 사실은 주어졌어요. 평균과 공분산만 알면 분포가 정해지니까

$$
p(\mathbf{x}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t) = \mathcal{N}\big(\mathbf{A}\boldsymbol{\mu}_t,\; \mathbf{A}\boldsymbol{\Sigma}_t\mathbf{A}^\top + \mathbf{Q}\big)
$$

한 걸음 나아가면 노이즈 $\mathbf{Q}$만큼 불확실성이 더해져요.

수업과의 연결: 0930 수업의 아핀 변환 규칙 $\mathbb{E}[\mathbf{y}] = \mathbf{A}\,\mathbb{E}[\mathbf{x}] + \mathbf{b}$, $\mathbb{V}[\mathbf{y}] = \mathbf{A}\,\mathbb{V}[\mathbf{x}]\,\mathbf{A}^\top$에서 $\mathbf{b} = \mathbf{0}$으로 둔 거예요. 여기에 독립이거나 적어도 공분산이 0일 때 쓸 수 있다고 한 $\mathbb{V}[\mathbf{x} + \mathbf{y}] = \mathbb{V}[\mathbf{x}] + \mathbb{V}[\mathbf{y}]$를 더했어요.

#### 완성 답과 검산

#### 검산

편차 외적의 교차항은 새 잡음과 과거 상태의 조건부 독립으로0이에요. A=I,Q=0이면 현재 평균·공분산이 그대로 복원돼요.

정답: $p(\mathbf{x}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t) = \mathcal{N}\big(\mathbf{A}\boldsymbol{\mu}_t,\; \mathbf{A}\boldsymbol{\Sigma}_t\mathbf{A}^\top + \mathbf{Q}\big)$

#### 여기서 주의해요

아직 다음 관측을 보지 않았으므로 R이나 C를 상태 예측분산에 더하지 않아요.

#### 설명을 닫고 다시 해요

1. $x_{t+1}-A\mu_t=A(x_t-\mu_t)+w$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 아직 다음 관측을 보지 않았으므로 R이나 C를 상태 예측분산에 더하지 않아요.

**페이지 요약**

#### 떠올릴 개념·공식

한 걸음 예측(predictive distribution)은 현재 posterior를 선형 변환하고 새 독립 잡음을 더해요. $\mu_{t+1}=A\mu_t$, $P=A\Sigma_tA^\top+Q$예요.

#### 첫 줄

$x_{t+1}-A\mu_t=A(x_t-\mu_t)+w$예요.

#### 검산

편차 외적의 교차항은 새 잡음과 과거 상태의 조건부 독립으로0이에요. A=I,Q=0이면 현재 평균·공분산이 그대로 복원돼요.

#### 조건·구분

모든 평균·공분산은 시각 $t$까지 관측한 측정값을 조건으로 해요. 아직 다음 관측을 보지 않았으므로 상태 예측분산에는 $Q$를 더하며 $R$이나 $C$를 더하지 않아요.

---

<a id="p4"></a>

### P4. 분산은 제곱의 평균 빼기 평균의 제곱

MML Exercise 6.6 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0930_Bayesian_Linear_Regression-%EB%AC%B8%EC%A0%9C.pdf#page=4)

#### 주어진 조건

확률변수 $X$의 평균을 $\mu = \mathbb{E}[x]$라고 해요. 분산의 정의는 평균에서 벗어난 정도를 제곱해 평균 낸 값이에요.

$$
\mathbb{V}[x] = \mathbb{E}[(x - \mu)^2]
$$

#### 구할 것

이 정의에서 출발해 아래 식을 증명해 보세요.

$$
\mathbb{V}[x] = \mathbb{E}[x^2] - (\mathbb{E}[x])^2
$$

#### 무엇을 구하는 문제인가요?

분산은 제곱의 평균 빼기 평균의 제곱를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

분산(variance)은 편차제곱의 평균이에요. μ=E[X]가 상수라서 $E[(X-\mu)^2]$를 전개하면 $E[X^2]-\mu^2$예요. 이차 모멘트 유한성이 필요해요.

#### 종이에 적을 첫 줄

$(x-\mu)^2=x^2-2\mu x+\mu^2$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

제곱을 펼쳐요.

$$
(x - \mu)^2 = x^2 - 2\mu x + \mu^2
$$

기댓값은 합과 상수배를 그대로 통과시켜요. $\mu$는 상수예요.

$$
\mathbb{E}[(x - \mu)^2] = \mathbb{E}[x^2] - 2\mu\,\mathbb{E}[x] + \mu^2
$$

$\mathbb{E}[x] = \mu$를 넣어요.

$$
\mathbb{E}[x^2] - 2\mu \cdot \mu + \mu^2 = \mathbb{E}[x^2] - \mu^2
$$

$\mu$를 다시 $\mathbb{E}[x]$로 적으면 증명이 끝나요.

$$
\mathbb{V}[x] = \mathbb{E}[x^2] - (\mathbb{E}[x])^2
$$

수업과의 연결: 0930 수업의 "곱의 평균 빼기 평균의 곱" $\operatorname{Cov}[X, Y] = \mathbb{E}[XY] - \mathbb{E}[X]\,\mathbb{E}[Y]$에서 $Y$ 자리에 $X$를 넣은 것과 같아요. 분산은 자기 자신과의 공분산이에요.

#### 완성 답과 검산

#### 검산

선형성으로 E[X²]−2μE[X]+μ²=E[X²]−μ²예요. 정의와 같으므로0이상이며 상수변수이면0이에요.

정답: $\mathbb{V}[x] = \mathbb{E}[(x - \mu)^2] = \mathbb{E}[x^2] - 2\mu\,\mathbb{E}[x] + \mu^2 = \mathbb{E}[x^2] - (\mathbb{E}[x])^2$

#### 여기서 주의해요

E[X²]와(E[X])²는 일반적으로 달라요. E[X²]를 먼저 평균의 제곱으로 바꾸면 안 돼요.

#### 설명을 닫고 다시 해요

1. $(x-\mu)^2=x^2-2\mu x+\mu^2$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. E[X²]와(E[X])²는 일반적으로 달라요. E[X²]를 먼저 평균의 제곱으로 바꾸면 안 돼요.

**페이지 요약**

#### 떠올릴 개념·공식

분산(variance)은 편차제곱의 평균이에요. μ=E[X]가 상수라서 $E[(X-\mu)^2]$를 전개하면 $E[X^2]-\mu^2$예요.

#### 첫 줄

$(x-\mu)^2=x^2-2\mu x+\mu^2$예요.

#### 검산

선형성으로 E[X²]−2μE[X]+μ²=E[X²]−μ²예요. 정의와 같으므로0이상이며 상수변수이면0이에요.

#### 조건·구분

이차 모멘트가 유한하다고 전제해요. $E[X^2]$와 $(E[X])^2$는 일반적으로 달라요.

---

<a id="p5"></a>

### P5. 노이즈가 섞인 선형 변환의 가능도

MML Exercise 6.12 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0930_Bayesian_Linear_Regression-%EB%AC%B8%EC%A0%9C.pdf#page=5)

#### 주어진 조건

가우시안 확률변수 $\mathbf{x} \sim \mathcal{N}(\boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$가 있어요($\mathbf{x} \in \mathbb{R}^D$). 여기에 상수 행렬 $\mathbf{A}$를 곱하고 상수 벡터 $\mathbf{b}$와 노이즈 $\mathbf{w}$를 더해요.

$$
\mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{b} + \mathbf{w}
$$

$\mathbf{y} \in \mathbb{R}^E$이고, $\mathbf{w} \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})$는 $\mathbf{x}$와 독립인 가우시안 노이즈예요.

#### 구할 것

$\mathbf{x}$ 값이 주어졌을 때 $\mathbf{y}$의 분포, 즉 가능도(likelihood) $p(\mathbf{y} \mid \mathbf{x})$를 적어 보세요.

#### 무엇을 구하는 문제인가요?

노이즈가 섞인 선형 변환의 가능도를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

조건부 likelihood는 x가 주어졌을 때 잡음 w만 변하는 분포예요. $y=Ax+b+w$에서 Ax+b는 조건부 평균, Q는 조건부 공분산이에요.

#### 종이에 적을 첫 줄

$p(y\mid x)=\mathcal N(y\mid Ax+b,Q)$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

$\mathbf{x}$가 주어졌다고 해요. 그러면 $\mathbf{A}\mathbf{x} + \mathbf{b}$는 더 이상 흔들리지 않는 상수 벡터예요.

$\mathbf{w}$는 $\mathbf{x}$와 독립이에요. $\mathbf{x}$를 알아도 $\mathbf{w}$의 분포는 그대로 $\mathcal{N}(\mathbf{0}, \mathbf{Q})$예요.

$\mathbf{y}$는 상수에 $\mathbf{w}$를 더한 것이에요. 평균은 상수만큼 옮겨져요.

$$
\mathbb{E}[\mathbf{y} \mid \mathbf{x}] = \mathbf{A}\mathbf{x} + \mathbf{b} + \mathbb{E}[\mathbf{w}] = \mathbf{A}\mathbf{x} + \mathbf{b}
$$

상수를 더해도 퍼진 정도는 바뀌지 않아요.

$$
\mathbb{V}[\mathbf{y} \mid \mathbf{x}] = \mathbb{V}[\mathbf{w}] = \mathbf{Q}
$$

가우시안 노이즈를 상수만큼 옮긴 것이라 종 모양은 그대로예요. 그래서

$$
p(\mathbf{y} \mid \mathbf{x}) = \mathcal{N}(\mathbf{y} \mid \mathbf{A}\mathbf{x} + \mathbf{b}, \mathbf{Q})
$$

수업과의 연결: 0930 수업의 가능도 $p(y \mid \mathbf{x}, \boldsymbol{\theta}) = \mathcal{N}\big(y \mid \boldsymbol{\phi}^\top(\mathbf{x})\boldsymbol{\theta},\, \sigma^2\big)$와 같은 논리예요. 조건으로 주어진 것은 상수가 되고, 불확실성은 노이즈에만 남아요.

#### 완성 답과 검산

#### 검산

x를 고정하면 y−(Ax+b)=w예요. 따라서 평균0, 공분산Q를 평행이동한 가우시안이 맞아요.

정답: $p(\mathbf{y} \mid \mathbf{x}) = \mathcal{N}(\mathbf{y} \mid \mathbf{A}\mathbf{x} + \mathbf{b}, \mathbf{Q})$

#### 여기서 주의해요

조건부에 AΣxAᵀ를 더하지 않아요. 그 항은 x까지 랜덤하게 평균낸 주변분포에서 나와요.

#### 설명을 닫고 다시 해요

1. $p(y\mid x)=\mathcal N(y\mid Ax+b,Q)$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 조건부에 AΣxAᵀ를 더하지 않아요. 그 항은 x까지 랜덤하게 평균낸 주변분포에서 나와요.

**페이지 요약**

#### 떠올릴 개념·공식

조건부 likelihood는 x가 주어졌을 때 잡음 w만 변하는 분포예요. $y=Ax+b+w$

#### 첫 줄

$p(y\mid x)=\mathcal N(y\mid Ax+b,Q)$예요.

#### 검산

x를 고정하면 y−(Ax+b)=w예요. 따라서 평균0, 공분산Q를 평행이동한 가우시안이 맞아요.

#### 조건·구분

잡음은 입력과 독립이므로 입력을 고정해도 공분산은 $Q$예요. $A\Sigma_xA^{\top}$는 입력까지 랜덤하게 평균낸 주변분포에서 생기는 항이라 조건부 가능도에 더하지 않아요.

---

<a id="p6"></a>

### P6. 노이즈가 섞인 선형 변환의 평균과 공분산

MML Exercise 6.12 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0930_Bayesian_Linear_Regression-%EB%AC%B8%EC%A0%9C.pdf#page=6)

#### 주어진 조건

가우시안 확률변수 $\mathbf{x} \sim \mathcal{N}(\boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$가 있어요($\mathbf{x} \in \mathbb{R}^D$). 여기에 상수 행렬 $\mathbf{A}$를 곱하고 상수 벡터 $\mathbf{b}$와 노이즈 $\mathbf{w}$를 더해요.

$$
\mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{b} + \mathbf{w}
$$

$\mathbf{y} \in \mathbb{R}^E$이고, $\mathbf{w} \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})$는 $\mathbf{x}$와 독립인 가우시안 노이즈예요.

#### 구할 것

$\mathbf{y}$의 분포 $p(\mathbf{y})$가 가우시안이라는 사실은 주어진 것으로 써요. 그 평균 $\boldsymbol{\mu}_y$와 공분산 행렬 $\boldsymbol{\Sigma}_y$를 단계별로 유도해 보세요.

#### 무엇을 구하는 문제인가요?

노이즈가 섞인 선형 변환의 평균과 공분산를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

아핀 변환(affine transformation)은 상수 이동 b가 평균에는 남고 편차에서는 사라져요. $Var(AX)=A\Sigma_xA^\top$은 스칼라 Var(aX)=a²Var(X)의 확장이에요. 두 번째 계수는 전치해 오른쪽에 둬요.

#### 종이에 적을 첫 줄

$y-E[y]=A(x-\mu_x)+w$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

$\mathbf{y}$를 두 조각으로 나눠요. $\mathbf{u} = \mathbf{A}\mathbf{x} + \mathbf{b}$라고 두면 $\mathbf{y} = \mathbf{u} + \mathbf{w}$예요.

평균은 합을 그대로 통과해요. 아핀 변환 규칙과 $\mathbb{E}[\mathbf{w}] = \mathbf{0}$을 써요.

$$
\boldsymbol{\mu}_y = \mathbb{E}[\mathbf{u}] + \mathbb{E}[\mathbf{w}] = \mathbf{A}\,\mathbb{E}[\mathbf{x}] + \mathbf{b} + \mathbf{0} = \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}
$$

$\mathbf{u}$의 공분산 행렬은 아핀 변환 규칙으로 구해요. 상수 $\mathbf{b}$는 퍼짐에 영향을 주지 않아요.

$$
\mathbb{V}[\mathbf{u}] = \mathbf{A}\,\mathbb{V}[\mathbf{x}]\,\mathbf{A}^\top = \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top
$$

$\mathbf{u}$와 $\mathbf{w}$ 사이의 공분산을 확인해요. $\mathbb{E}[\mathbf{w}] = \mathbf{0}$이라서

$$
\operatorname{Cov}[\mathbf{u}, \mathbf{w}] = \mathbb{E}[(\mathbf{A}\mathbf{x} + \mathbf{b})\mathbf{w}^\top] - \mathbb{E}[\mathbf{u}]\,\mathbb{E}[\mathbf{w}]^\top = \mathbf{A}\,\mathbb{E}[\mathbf{x}\mathbf{w}^\top]
$$

$\mathbf{x}$와 $\mathbf{w}$가 독립이라 $\mathbb{E}[\mathbf{x}\mathbf{w}^\top] = \mathbb{E}[\mathbf{x}]\,\mathbb{E}[\mathbf{w}]^\top = \mathbf{0}$이에요. 그래서 $\operatorname{Cov}[\mathbf{u}, \mathbf{w}] = \mathbf{0}$이에요.

교차 공분산이 0이니까 합의 분산은 분산의 합이에요. $\mathbb{V}[\mathbf{w}] = \mathbf{Q}$를 넣어요.

$$
\boldsymbol{\Sigma}_y = \mathbb{V}[\mathbf{u}] + \mathbb{V}[\mathbf{w}] = \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q}
$$

$p(\mathbf{y})$는 가우시안이라고 주어졌으니 $p(\mathbf{y}) = \mathcal{N}(\mathbf{y} \mid \boldsymbol{\mu}_y, \boldsymbol{\Sigma}_y)$로 정해져요.

수업과의 연결: 0930 수업의 아핀 변환 규칙 $\mathbb{V}[\mathbf{y}] = \mathbf{A}\,\mathbb{V}[\mathbf{x}]\,\mathbf{A}^\top$에, 독립이거나 적어도 공분산이 0일 때 쓸 수 있다고 한 $\mathbb{V}[\mathbf{x} + \mathbf{y}] = \mathbb{V}[\mathbf{x}] + \mathbb{V}[\mathbf{y}]$를 더한 거예요.

#### 완성 답과 검산

#### 검산

성분(i,j)은 ∑kl A_ik Cov(x_k,x_l)A_jl+Q_ij예요. 이것이 AΣxAᵀ+Q의 칸과 같아요. 차원은 E×E이고 b는 사라져요.

정답: $\boldsymbol{\mu}_y = \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}$, $\boldsymbol{\Sigma}_y = \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q}$

#### 여기서 주의해요

AΣxAᵀ를 AAᵀΣx로 바꾸지 않아요. 독립 잡음의 Q만 별도로 더해요.

#### 설명을 닫고 다시 해요

1. $y-E[y]=A(x-\mu_x)+w$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. AΣxAᵀ를 AAᵀΣx로 바꾸지 않아요. 독립 잡음의 Q만 별도로 더해요.

**페이지 요약**

#### 떠올릴 개념·공식

아핀 변환(affine transformation)은 상수 이동 b가 평균에는 남고 편차에서는 사라져요. $Var(AX)=A\Sigma_xA^\top$

#### 첫 줄

$y-E[y]=A(x-\mu_x)+w$예요.

#### 검산

성분(i,j)은 ∑kl A_ik Cov(x_k,x_l)A_jl+Q_ij예요. 이것이 AΣxAᵀ+Q의 칸과 같아요. 차원은 E×E이고 b는 사라져요.

#### 조건·구분

독립인 잡음으로 교차항이 사라져 $\mu_y=A\mu_x+b$, $\Sigma_y=A\Sigma_xA^{\top}+Q$예요. 행렬 곱 순서를 지키며 $A\Sigma_xA^{\top}$를 $AA^{\top}\Sigma_x$로 바꾸지 않아요.

---

<a id="p7"></a>

### P7. 한 번 더 변환해서 측정하기

MML Exercise 6.12 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0930_Bayesian_Linear_Regression-%EB%AC%B8%EC%A0%9C.pdf#page=7)

#### 주어진 조건

가우시안 확률변수 $\mathbf{x} \sim \mathcal{N}(\boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$로 $\mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{b} + \mathbf{w}$를 만들어요. $\mathbf{w} \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})$는 $\mathbf{x}$와 독립인 가우시안 노이즈예요. 이때 $\mathbf{y}$는 평균이 $\boldsymbol{\mu}_y = \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}$, 공분산 행렬이 $\boldsymbol{\Sigma}_y = \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q}$인 가우시안이에요. 이 결과는 주어진 것으로 써요. 이제 $\mathbf{y}$를 상수 행렬 $\mathbf{C}$로 한 번 더 변환해서 측정해요.

$$
\mathbf{z} = \mathbf{C}\mathbf{y} + \mathbf{v}
$$

$\mathbf{v} \sim \mathcal{N}(\mathbf{0}, \mathbf{R})$은 $\mathbf{y}$와 독립인 가우시안 측정 노이즈예요. $p(\mathbf{z})$가 가우시안이라는 사실도 주어진 것으로 써요.

#### 구할 것

- (a) $p(\mathbf{z} \mid \mathbf{y})$를 적어 보세요.
- (b) $p(\mathbf{z})$의 평균 $\boldsymbol{\mu}_z$와 공분산 행렬 $\boldsymbol{\Sigma}_z$를 단계별로 유도해 보세요.

#### 무엇을 구하는 문제인가요?

한 번 더 변환해서 측정하기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

같은 변환 규칙을 측정 단계에도 써요. y 고정이면 z의 공분산은 R, y까지 랜덤하면 CΣyCᵀ+R예요. conditioning과 marginalization을 구별하는 단서예요.

#### 종이에 적을 첫 줄

(a)는 z−Cy=v, (b)는 z−Cμy=C(y−μy)+v예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$\mathbf{y}$가 주어지면 $\mathbf{C}\mathbf{y}$는 상수 벡터예요. $\mathbf{v}$는 $\mathbf{y}$와 독립이라 분포가 그대로 $\mathcal{N}(\mathbf{0}, \mathbf{R})$이에요.

상수에 가우시안 노이즈를 더했으니 평균만 $\mathbf{C}\mathbf{y}$로 옮겨지고 퍼짐은 $\mathbf{R}$ 그대로예요.

$$
p(\mathbf{z} \mid \mathbf{y}) = \mathcal{N}(\mathbf{z} \mid \mathbf{C}\mathbf{y}, \mathbf{R})
$$

#### (b)

평균은 합을 그대로 통과해요. $\mathbb{E}[\mathbf{v}] = \mathbf{0}$이에요.

$$
\boldsymbol{\mu}_z = \mathbf{C}\,\mathbb{E}[\mathbf{y}] + \mathbb{E}[\mathbf{v}] = \mathbf{C}\boldsymbol{\mu}_y
$$

$\mathbf{C}\mathbf{y}$의 공분산 행렬은 아핀 변환 규칙으로 $\mathbf{C}\,\mathbb{V}[\mathbf{y}]\,\mathbf{C}^\top = \mathbf{C}\boldsymbol{\Sigma}_y\mathbf{C}^\top$이에요.

$\mathbf{y}$와 $\mathbf{v}$가 독립이라 $\mathbb{E}[\mathbf{y}\mathbf{v}^\top] = \mathbb{E}[\mathbf{y}]\,\mathbb{E}[\mathbf{v}]^\top = \mathbf{0}$이에요. 그래서 $\operatorname{Cov}[\mathbf{C}\mathbf{y}, \mathbf{v}] = \mathbf{C}\,\mathbb{E}[\mathbf{y}\mathbf{v}^\top] - \mathbf{C}\boldsymbol{\mu}_y\,\mathbb{E}[\mathbf{v}]^\top = \mathbf{0}$이에요.

교차 공분산이 0이니까 분산을 더해요.

$$
\boldsymbol{\Sigma}_z = \mathbb{V}[\mathbf{C}\mathbf{y}] + \mathbb{V}[\mathbf{v}] = \mathbf{C}\boldsymbol{\Sigma}_y\mathbf{C}^\top + \mathbf{R}
$$

주어진 $\boldsymbol{\mu}_y$, $\boldsymbol{\Sigma}_y$를 넣으면 처음 재료로도 적을 수 있어요.

$$
\boldsymbol{\mu}_z = \mathbf{C}(\mathbf{A}\boldsymbol{\mu}_x + \mathbf{b})
$$

$$
\boldsymbol{\Sigma}_z = \mathbf{C}(\mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q})\mathbf{C}^\top + \mathbf{R}
$$

수업과의 연결: 0930 수업의 아핀 변환 규칙 $\mathbb{E}[\mathbf{y}] = \mathbf{A}\,\mathbb{E}[\mathbf{x}] + \mathbf{b}$, $\mathbb{V}[\mathbf{y}] = \mathbf{A}\,\mathbb{V}[\mathbf{x}]\,\mathbf{A}^\top$를 한 번 더 쓴 거예요. 변환을 거칠 때마다 공분산 양옆에 행렬과 그 전치가 붙고, 독립인 노이즈의 공분산이 더해져요.

#### 완성 답과 검산

#### (a) 검산

y 고정 뒤 v만 변하므로 N(Cy,R)예요.

#### (b) 검산

평균은 Cμy이고 편차 외적은 CΣyCᵀ+R예요. 이를 y의 식에 넣으면 원 카드의 두 단계 변환 식과 일치해요.

정답: (a) $p(\mathbf{z} \mid \mathbf{y}) = \mathcal{N}(\mathbf{z} \mid \mathbf{C}\mathbf{y}, \mathbf{R})$ (b) $\boldsymbol{\mu}_z = \mathbf{C}\boldsymbol{\mu}_y = \mathbf{C}(\mathbf{A}\boldsymbol{\mu}_x + \mathbf{b})$, $\boldsymbol{\Sigma}_z = \mathbf{C}\boldsymbol{\Sigma}_y\mathbf{C}^\top + \mathbf{R} = \mathbf{C}(\mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q})\mathbf{C}^\top + \mathbf{R}$

#### 여기서 주의해요

측정 잡음 R을 C로 다시 감싸지 않아요. R은 C 뒤에서 더해져요.

#### 설명을 닫고 다시 해요

1. (a)는 z−Cy=v, (b)는 z−Cμy=C(y−μy)+v예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 측정 잡음 R을 C로 다시 감싸지 않아요. R은 C 뒤에서 더해져요.

**페이지 요약**

#### 떠올릴 개념·공식

같은 변환 규칙을 측정 단계에도 써요. y 고정이면 z의 공분산은 R, y까지 랜덤하면 CΣyCᵀ+R예요.

#### 첫 줄

(a)는 z−Cy=v, (b)는 z−Cμy=C(y−μy)+v예요.

#### 검산

y 고정 뒤 v만 변하므로 N(Cy,R)예요. 평균은 Cμy이고 편차 외적은 CΣyCᵀ+R예요. 이를 y의 식에 넣으면 원 카드의 두 단계 변환 식과 일치해요.

#### 조건·구분

측정 잡음은 $C$로 변환한 뒤 더하므로 $R$을 다시 $C$로 감싸지 않아요. 조건부는 $\mathcal{N}(Cy,R)$, 주변 공분산은 $C\Sigma_yC^{\top}+R$예요.

---

<a id="p8"></a>

### P8. 쌍끼리의 차이로 보는 분산

MML Exercise 6.7 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0930_Bayesian_Linear_Regression-%EB%AC%B8%EC%A0%9C.pdf#page=8)

#### 주어진 조건

확률변수 $X$에서 얻은 관측값 $x_1, \dots, x_N$이 있어요. 모든 쌍 $(x_i, x_j)$의 차이를 제곱해 평균 내면, "제곱의 평균 빼기 평균의 제곱"의 두 배가 돼요.

$$
\frac{1}{N^2}\sum_{i,j=1}^{N}(x_i - x_j)^2 = 2\left[\frac{1}{N}\sum_{i=1}^{N} x_i^2 - \left(\frac{1}{N}\sum_{i=1}^{N} x_i\right)^2\right]
$$

#### 구할 것

이 식을 증명해 보세요.

#### 무엇을 구하는 문제인가요?

쌍끼리의 차이로 보는 분산를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

쌍별 제곱차(pairwise squared difference)는 이중합을 전개해요. $\sum_{ij}x_i^2=N\sum_i x_i^2$, $\sum_{ij}x_ix_j=(\sum_i x_i)^2$예요. N&gt;0이고 모든 순서쌍을 포함해요.

#### 종이에 적을 첫 줄

$(x_i-x_j)^2=x_i^2-2x_ix_j+x_j^2$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

제곱을 펼쳐요.

$$
(x_i - x_j)^2 = x_i^2 - 2x_i x_j + x_j^2
$$

첫 항을 $i$, $j$ 모두에 대해 더해요. $x_i^2$은 $j$와 상관없으니 $j$에 대한 합은 같은 값을 $N$번 더하는 거예요.

$$
\sum_{i,j=1}^{N} x_i^2 = N\sum_{i=1}^{N} x_i^2
$$

셋째 항도 같아요. 이번에는 $i$에 대한 합이 $N$번 더하는 역할을 해요. 합의 첨자 이름은 바꿔도 값이 같아요.

$$
\sum_{i,j=1}^{N} x_j^2 = N\sum_{j=1}^{N} x_j^2 = N\sum_{i=1}^{N} x_i^2
$$

가운데 항은 두 합의 곱으로 나눠져요.

$$
\sum_{i,j=1}^{N} x_i x_j = \left(\sum_{i=1}^{N} x_i\right)\left(\sum_{j=1}^{N} x_j\right) = \left(\sum_{i=1}^{N} x_i\right)^2
$$

세 결과를 모으고 $\frac{1}{N^2}$을 곱해요.

$$
\frac{1}{N^2}\sum_{i,j=1}^{N}(x_i - x_j)^2 = \frac{1}{N^2}\left[2N\sum_{i=1}^{N} x_i^2 - 2\left(\sum_{i=1}^{N} x_i\right)^2\right]
$$

$\frac{1}{N^2}$을 괄호 안에 나눠 넣어요. 둘째 항에서는 $\frac{1}{N^2} = \left(\frac{1}{N}\right)^2$이라 제곱 안으로 들어가요.

$$
= 2\left[\frac{1}{N}\sum_{i=1}^{N} x_i^2 - \left(\frac{1}{N}\sum_{i=1}^{N} x_i\right)^2\right]
$$

수업과의 연결: 괄호 안은 관측값으로 계산한 "제곱의 평균 빼기 평균의 제곱"이에요. 0930 수업의 $\operatorname{Cov}[X, Y] = \mathbb{E}[XY] - \mathbb{E}[X]\,\mathbb{E}[Y]$에서 $Y$ 자리에 $X$를 넣고, 기댓값을 $N$개 관측값의 평균으로 바꾼 모양이에요.

#### 완성 답과 검산

#### 검산

두 제곱항은 각각N번씩 반복되고 교차항은 합의 제곱으로 분리돼요. 따라서2N∑x_i²−2(∑x_i)²를N²으로 나누면 정확한 우변이에요. 모든 실수 관측에 대한 대수 증명이며 숫자 예제만으로 끝낸 것이 아니에요.

정답: $\frac{1}{N^2}\sum_{i,j=1}^{N}(x_i - x_j)^2 = \frac{1}{N^2}\left[2N\sum_{i=1}^{N} x_i^2 - 2\left(\sum_{i=1}^{N} x_i\right)^2\right] = 2\left[\frac{1}{N}\sum_{i=1}^{N} x_i^2 - \left(\frac{1}{N}\sum_{i=1}^{N} x_i\right)^2\right]$

#### 여기서 주의해요

표본 불편분산의 N−1로 바꾸지 않아요. 이 식은 분모N인 경험분산의 항등식이에요.

#### 설명을 닫고 다시 해요

1. $(x_i-x_j)^2=x_i^2-2x_ix_j+x_j^2$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 표본 불편분산의 N−1로 바꾸지 않아요. 이 식은 분모N인 경험분산의 항등식이에요.

**페이지 요약**

#### 떠올릴 개념·공식

쌍별 제곱차(pairwise squared difference)는 이중합을 전개해요. $\sum_{ij}x_i^2=N\sum_i x_i^2$, $\sum_{ij}x_ix_j=(\sum_i x_i)^2$예요.

#### 첫 줄

$(x_i-x_j)^2=x_i^2-2x_ix_j+x_j^2$예요.

#### 검산

두 제곱항은 각각N번씩 반복되고 교차항은 합의 제곱으로 분리돼요. 따라서2N∑x_i²−2(∑x_i)²를N²으로 나누면 정확한 우변이에요. 모든 실수 관측에 대한 대수 증명이며 숫자 예제만으로 끝낸 것이 아니에요.

#### 조건·구분

$N>0$이고 모든 순서쌍을 포함해요. 분모 $N$인 경험분산의 항등식이므로 불편분산의 $N-1$로 바꾸지 않아요.

---

원 문제·정리노트·PDF는 보존해요.
