# 머신러닝기초 복습 1007 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [P1. 사전분포가 만드는 함수들](#p1)
  - [P2. 한 점에서 본 함수값의 평균과 분산](#p2)
  - [P3. 사후분포로 그린 함수 그림 읽기](#p3)
  - [P4. 2차원 가우시안에서 한 변수만 보기](#p4)
  - [P5. 독립인 가우시안의 가중합 구하기](#p5)
  - [P6. 가우시안 혼합의 차원별 주변분포](#p6)
  - [P7. 가우시안 혼합의 평균](#p7)
  - [P8. 두 가우시안 밀도의 곱: 완전제곱식으로 유도하기](#p8)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### P1. 사전분포가 만드는 함수들

MML Example 9.7 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1007_Product_of_Gaussians.html#p1)

#### 주어진 조건

5차 다항식으로 베이지안 선형회귀를 해요. 특징 함수는 $\boldsymbol{\phi}(x) = [1, x, x^2, x^3, x^4, x^5]^\top$이고, 함수는 $f(x) = \boldsymbol{\theta}^\top\boldsymbol{\phi}(x)$예요. 파라미터 사전분포는 $p(\boldsymbol{\theta}) = \mathcal{N}\left(\mathbf{0}, \frac{1}{4}\mathbf{I}\right)$로 골라요. 입력 $x_* \in [-5, 5]$에서 200개 점을 골라 특징 함수를 적용하고, 노이즈 없는 함수값 $f(x_*) = \boldsymbol{\phi}(x_*)^\top\boldsymbol{\theta}$의 분포를 그림으로 그려요. 그림에는 평균 함수(선), 음영 두 겹(진한 회색 67%, 옅은 회색 95% 신뢰 구간), 그리고 사전분포에서 뽑은 함수 표본 몇 개가 있어요.

#### 구할 것

- (a) 함수 표본 하나를 얻는 두 단계를 적어 보세요.
- (b) 파라미터 벡터 $\boldsymbol{\theta}$는 몇 차원인가요?
- (c) 그림의 음영(불확실성)은 어디에서 오나요?

#### 무엇을 구하는 문제인가요?

사전분포가 만드는 함수들를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

함수 사전분포(function prior)는 계수를 한 번 뽑아 전체 입력 구간에 같은 계수를 써 만든 곡선들의 분포예요. 5차는6계수이고 $f(x)=\phi(x)^\top\theta$에서 랜덤 재료는 θ예요.

#### 종이에 적을 첫 줄

$\theta_i\sim\mathcal N(0,I/4)$를 먼저 뽑아요.

#### 왜 이렇게 푸는지 함께 따라가요

함수 $f(x) = \boldsymbol{\theta}^\top\boldsymbol{\phi}(x)$에서 랜덤한 것은 $\boldsymbol{\theta}$뿐이에요. $\boldsymbol{\phi}(x)$는 $x$만 알면 정해지는 값이에요.

#### (a)

그래서 먼저 사전분포에서 파라미터 벡터 하나를 뽑아요.

$$
\boldsymbol{\theta}_i \sim p(\boldsymbol{\theta}) = \mathcal{N}\left(\mathbf{0}, \frac{1}{4}\mathbf{I}\right)
$$

다음으로 이 값을 넣어 함수 하나를 만들어요.

$$
f_i(\cdot) = \boldsymbol{\theta}_i^\top\boldsymbol{\phi}(\cdot)
$$

200개 입력 $x_*$마다 $\boldsymbol{\theta}_i^\top\boldsymbol{\phi}(x_*)$를 계산해 이으면 곡선 하나가 돼요.

#### (b)

$\boldsymbol{\phi}(x) = [1, x, x^2, x^3, x^4, x^5]^\top$의 성분은 상수항부터 $x^5$까지 6개예요. 내적 $\boldsymbol{\theta}^\top\boldsymbol{\phi}(x)$가 되려면 $\boldsymbol{\theta}$도 같은 크기여야 해요. 그래서 $\boldsymbol{\theta} \in \mathbb{R}^6$, 6차원이에요.

#### (c)

여기서 그린 것은 노이즈 없는 함수값 $f(x_*) = \boldsymbol{\phi}(x_*)^\top\boldsymbol{\theta}$예요. 노이즈 분산 $\sigma^2$이 들어가지 않아요.

남은 랜덤한 재료는 $\boldsymbol{\theta}$ 하나뿐이에요. 따라서 음영의 불확실성은 모두 파라미터 $\boldsymbol{\theta}$의 불확실성에서 와요.

#### 완성 답과 검산

#### (a) 검산

하나의 θ를200개 입력에 공유해 계산하면 매끄러운5차 곡선 하나예요.

#### (b) 검산

0차~5차 계수라6차원이에요.

#### (c) 검산

f에는 관측 잡음 ε가 없으므로 불확실성은 prior의 θ에서 와요.

정답: (a) $\boldsymbol{\theta}_i \sim p(\boldsymbol{\theta})$를 뽑고 $f_i(\cdot) = \boldsymbol{\theta}_i^\top\boldsymbol{\phi}(\cdot)$를 계산해요. (b) $\boldsymbol{\theta} \in \mathbb{R}^6$, 6차원이에요. (c) 노이즈 없는 함수값이라서 음영은 파라미터 불확실성에서만 와요.

#### 여기서 주의해요

x마다 새 θ를 뽑으면 같은 함수 한 개의 표본이 아니에요. 노이즈 없는 f의 음영에 σ²를 더하지 않아요.

#### 설명을 닫고 다시 해요

1. $\theta_i\sim\mathcal N(0,I/4)$를 먼저 뽑아요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. x마다 새 θ를 뽑으면 같은 함수 한 개의 표본이 아니에요. 노이즈 없는 f의 음영에 σ²를 더하지 않아요.

**페이지 요약**

#### 떠올릴 개념·공식

함수 사전분포(function prior)는 계수를 한 번 뽑아 전체 입력 구간에 같은 계수를 써 만든 곡선들의 분포예요. $f(x)=\phi(x)^\top\theta$

#### 첫 줄

$\theta_i\sim\mathcal N(0,I/4)$를 먼저 뽑아요.

#### 검산

하나의 θ를200개 입력에 공유해 계산하면 매끄러운5차 곡선 하나예요. 0차~5차 계수라6차원이에요. f에는 관측 잡음 ε가 없으므로 불확실성은 prior의 θ에서 와요.

---

<a id="p2"></a>

### P2. 한 점에서 본 함수값의 평균과 분산

MML Example 9.7 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1007_Product_of_Gaussians.html#p2)

#### 주어진 조건

5차 다항식으로 베이지안 선형회귀를 해요. 특징 함수는 $\boldsymbol{\phi}(x) = [1, x, x^2, x^3, x^4, x^5]^\top$이에요. 파라미터 사전분포는 $p(\boldsymbol{\theta}) = \mathcal{N}\left(\mathbf{0}, \frac{1}{2}\mathbf{I}\right)$로 골라요. 노이즈 없는 함수값은 $f(x_*) = \boldsymbol{\phi}(x_*)^\top\boldsymbol{\theta}$예요.

#### 구할 것

$f(x_*)$의 평균과 분산을 $x_* = 0$일 때와 $x_* = 1$일 때 각각 구해 보세요.

#### 무엇을 구하는 문제인가요?

한 점에서 본 함수값의 평균과 분산를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

한 점의 함수값은 랜덤 계수의 스칼라 가중합이에요. $E[f]=\phi^\top E[\theta]$, $Var(f)=\phi^\top S_0\phi$이고 S0=I/2예요. 각 계수의 분산에 특징의 제곱을 곱해 더해요.

#### 종이에 적을 첫 줄

$\phi(0)=[1,0,0,0,0,0]^\top$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

$x_*$를 고정하면 $\mathbf{A} = \boldsymbol{\phi}(x_*)^\top$ ($1 \times 6$ 행벡터), $\mathbf{b} = 0$으로 놓을 수 있어요. 그러면 $f(x_*) = \mathbf{A}\boldsymbol{\theta} + \mathbf{b}$예요.

평균은 $E[\mathbf{A}\mathbf{X} + \mathbf{b}] = \mathbf{A}E[\mathbf{X}] + \mathbf{b}$로 구해요.

$$
E[f(x_*)] = \boldsymbol{\phi}(x_*)^\top E[\boldsymbol{\theta}] = \boldsymbol{\phi}(x_*)^\top\mathbf{0} = 0
$$

어느 $x_*$에서든 평균은 0이에요.

분산은 $\mathbf{A}\Sigma_{\mathbf{X}}\mathbf{A}^\top$로 구해요. $\Sigma_{\boldsymbol{\theta}} = \frac{1}{2}\mathbf{I}$이니까

$$
\mathrm{var}[f(x_*)] = \boldsymbol{\phi}(x_*)^\top\left(\frac{1}{2}\mathbf{I}\right)\boldsymbol{\phi}(x_*) = \frac{1}{2}\boldsymbol{\phi}(x_*)^\top\boldsymbol{\phi}(x_*) = \frac{1}{2}\sum_{k=0}^{5} x_*^{2k}
$$

$x_* = 0$이면 $\boldsymbol{\phi}(0) = [1, 0, 0, 0, 0, 0]^\top$이라서 $\boldsymbol{\phi}(0)^\top\boldsymbol{\phi}(0) = 1$이에요.

$$
\mathrm{var}[f(0)] = \frac{1}{2} \cdot 1 = \frac{1}{2}
$$

$x_* = 1$이면 $\boldsymbol{\phi}(1) = [1, 1, 1, 1, 1, 1]^\top$이라서 $\boldsymbol{\phi}(1)^\top\boldsymbol{\phi}(1) = 6$이에요.

$$
\mathrm{var}[f(1)] = \frac{1}{2} \cdot 6 = 3
$$

가우시안의 아핀 변환은 가우시안이니까 $p(f(0)) = \mathcal{N}\left(0, \frac{1}{2}\right)$, $p(f(1)) = \mathcal{N}(0, 3)$이에요.

#### 완성 답과 검산

#### 검산

0에서는 상수계수만 남아분산1/2예요. 1에서는 독립계수6개의 합이라6×1/2=3이에요. 평균은 두 점 모두0이에요.

정답: 평균은 두 점 모두 $E[f(x_*)] = 0$이에요. 분산은 $\mathrm{var}[f(0)] = \frac{1}{2}$, $\mathrm{var}[f(1)] = 3$이에요.

#### 여기서 주의해요

분산1/2를 표준편차로 읽지 않아요. 특징 길이가6이라고 항상 분산3인 것도 아니에요.

#### 설명을 닫고 다시 해요

1. $\phi(0)=[1,0,0,0,0,0]^\top$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 분산1/2를 표준편차로 읽지 않아요. 특징 길이가6이라고 항상 분산3인 것도 아니에요.

**페이지 요약**

#### 떠올릴 개념·공식

한 점의 함수값은 랜덤 계수의 스칼라 가중합이에요. $E[f]=\phi^\top E[\theta]$, $Var(f)=\phi^\top S_0\phi$이고 S0=I/2예요.

#### 첫 줄

$\phi(0)=[1,0,0,0,0,0]^\top$예요.

#### 검산

0에서는 상수계수만 남아분산1/2예요. 1에서는 독립계수6개의 합이라6×1/2=3이에요. 평균은 두 점 모두0이에요.

---

<a id="p3"></a>

### P3. 사후분포로 그린 함수 그림 읽기

MML Example 9.8 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1007_Product_of_Gaussians.html#p3)

#### 주어진 조건

5차 다항식과 사전분포 $p(\boldsymbol{\theta}) = \mathcal{N}\left(\mathbf{0}, \frac{1}{4}\mathbf{I}\right)$로 베이지안 선형회귀(BLR)를 해요. 훈련 데이터 $\mathbf{X}, \mathbf{y}$를 보고 나면 파라미터 사후분포 $p(\boldsymbol{\theta} \mid \mathbf{X}, \mathbf{y})$를 얻어요. 이 사후분포는 가우시안 $\mathcal{N}(\boldsymbol{\theta} \mid \mathbf{m}_N, \mathbf{S}_N)$이에요. 결과 그림은 세 칸이에요. (a)는 훈련 데이터, (b)는 함수 위의 사후분포, (c)는 곡선 여러 개를 겹쳐 그린 그림이에요. (b)에는 최대가능도 추정으로 얻은 함수(MLE), MAP 추정으로 얻은 함수(MAP), BLR의 평균 함수가 선으로 있고, 그 둘레에 음영이 두 겹(진한 회색, 옅은 회색) 있어요.

#### 구할 것

- (a) MAP 추정으로 얻은 함수 $\boldsymbol{\theta}_{\mathrm{MAP}}^\top\boldsymbol{\phi}(\cdot)$는 BLR에서 무엇과 같나요?
- (b) 그림 (b)의 음영 두 겹은 무엇을 뜻하나요?
- (c) 그림 (c)의 곡선 여러 개는 무엇을 보여 주나요?

![훈련 데이터 점들 위로 BLR 평균 함수 선이 지나가고, 그 둘레에 안쪽 경계 점선과 바깥쪽 경계 점선이 있는 그림. 데이터가 있는 가운데에서는 경계가 좁고 양 끝으로 갈수록 넓어져요.](figures_문제설명_1007_Product_of_Gaussians/p3-fig-p3-posterior-functions.svg)

*그림 (b)를 간단히 그린 것이에요. 색칠된 점은 훈련 데이터, 실선은 BLR 평균 함수예요. 긴 점선은 진한 음영의 경계, 짧은 점선은 옅은 음영의 경계예요.*

#### 무엇을 구하는 문제인가요?

사후분포로 그린 함수 그림 읽기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

가우시안 posterior는 양의 정부호 공분산일 때 평균이 mode예요. 그래서 θMAP=mN이고 평균 함수도 φᵀmN예요. 음영은 각 입력점의 posterior 함수값 구간이며 표본곡선은 θ를 공유해요.

#### 종이에 적을 첫 줄

$\theta_{MAP}=m_N$을 적어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

MAP 추정값은 사후분포 $p(\boldsymbol{\theta} \mid \mathbf{X}, \mathbf{y})$를 가장 크게 하는 $\boldsymbol{\theta}$예요. 이 사후분포는 가우시안 $\mathcal{N}(\boldsymbol{\theta} \mid \mathbf{m}_N, \mathbf{S}_N)$이고, 가우시안은 평균에서 가장 높아요. 그래서 $\boldsymbol{\theta}_{\mathrm{MAP}} = \mathbf{m}_N$이에요.

BLR의 평균 함수는 각 $x_*$에서 $\boldsymbol{\phi}(x_*)^\top\boldsymbol{\theta}$의 평균이에요. 아핀 변환의 평균 공식으로

$$
E[\boldsymbol{\phi}(x_*)^\top\boldsymbol{\theta} \mid \mathbf{X}, \mathbf{y}] = \boldsymbol{\phi}(x_*)^\top\mathbf{m}_N = \boldsymbol{\theta}_{\mathrm{MAP}}^\top\boldsymbol{\phi}(x_*)
$$

그러니 MAP 함수는 BLR의 사후 평균 함수와 같아요. 사전분포를 쓰지 않는 MLE 함수 $\boldsymbol{\theta}_{\mathrm{ML}}^\top\boldsymbol{\phi}(\cdot)$는 이것과 다를 수 있어요.

#### (b)

음영은 함수값이 얼마나 불확실한지 보여 줘요. 교과서는 진한 회색을 67%, 옅은 회색을 95% 예측 신뢰 구간이라고 적어요. 평균에서 표준편차 1배(1σ), 2배(2σ)만큼 벌린 구간이에요. 데이터가 있는 가운데에서는 좁고 양 끝으로 갈수록 넓어져요.

#### (c)

BLR은 함수 하나가 아니라 함수 위의 분포를 줘요. 그림 (c)의 곡선들은 이 사후분포 아래에서 그럴듯한 함수 표본(realization)들이에요.

곡선 하나는 사후분포에서 파라미터 $\boldsymbol{\theta}_i \sim p(\boldsymbol{\theta} \mid \mathbf{X}, \mathbf{y})$를 뽑아 $\boldsymbol{\theta}_i^\top\boldsymbol{\phi}(\cdot)$로 만든 것이에요. 데이터가 있는 곳에서는 곡선들이 서로 가깝고, 양 끝에서는 많이 벌어져요.

#### 완성 답과 검산

#### (a) 검산

log posterior의 이차항은 θ=mN에서0으로 최소라 mode=mean이에요.

#### (b) 검산

교과서에서 진한 구간은약67%, 옅은 구간은95%예요. 함수 f의 구간과 잡음을 더한 관측 y의 예측구간을 구별해요.

#### (c) 검산

posterior에서 θ를 뽑아 각 곡선 전체에 공유하므로 데이터와 prior를 반영한 함수들의 표본이에요.

정답: (a) MAP 함수는 BLR의 사후 평균 함수 $\mathbf{m}_N^\top\boldsymbol{\phi}(\cdot)$와 같아요. (b) 진한 음영은 67%, 옅은 음영은 95% 예측 신뢰 구간이에요. (c) 함수 위의 사후분포에서 나온 그럴듯한 함수 표본들이에요.

#### 여기서 주의해요

점별 구간이 전체 함수가 동시에 그 띠 안에 있을 확률과 같지는 않아요. Bayesian 구간은 엄밀히 credible interval로 읽어요.

#### 설명을 닫고 다시 해요

1. $\theta_{MAP}=m_N$을 적어요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 점별 구간이 전체 함수가 동시에 그 띠 안에 있을 확률과 같지는 않아요. Bayesian 구간은 엄밀히 credible interval로 읽어요.

**페이지 요약**

#### 떠올릴 개념·공식

가우시안 posterior는 양의 정부호 공분산일 때 평균이 mode예요.

#### 첫 줄

$\theta_{MAP}=m_N$을 적어요.

#### 검산

log posterior의 이차항은 θ=mN에서0으로 최소라 mode=mean이에요. 교과서에서 진한 구간은약67%, 옅은 구간은95%예요. 함수 f의 구간과 잡음을 더한 관측 y의 예측구간을 구별해요. posterior에서 θ를 뽑아 각 곡선 전체에 공유하므로 데이터와 prior를 반영한 함수들의 표본이에요.

---

<a id="p4"></a>

### P4. 2차원 가우시안에서 한 변수만 보기

MML Example 6.6 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1007_Product_of_Gaussians.html#p4)

#### 주어진 조건

두 변수 $x_1, x_2$의 결합분포가 2차원 가우시안이에요.

$$
p(x_1, x_2) = \mathcal{N}\left(\left[\begin{matrix}1 \\ 2\end{matrix}\right], \left[\begin{matrix}0.5 \\ -1\end{matrix}\;\;\begin{matrix}-1 \\ 4\end{matrix}\right]\right)
$$

결합 가우시안에서 한 변수만 남긴 주변분포는 가우시안이고, 평균은 평균 벡터의 해당 성분, 분산은 공분산 행렬의 해당 대각 성분이라고 알려져 있어요. 그대로 써도 돼요.

#### 구할 것

$x_2$를 적분해서 없앤 주변분포 $p(x_1)$을 구해 보세요.

#### 무엇을 구하는 문제인가요?

2차원 가우시안에서 한 변수만 보기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

가우시안 주변화(Gaussian marginalization)는 관심 성분의 평균과 공분산 대각을 남겨요. 한 성분을 보는 데 다른 성분 값이 조건으로 주어진 것은 아니에요.

#### 종이에 적을 첫 줄

$\mu_1=1$, $\Sigma_{11}=0.5$를 원 행렬에서 읽어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

결합 가우시안을 주변화해도 가우시안이에요. 그래서 $p(x_1)$은 평균과 분산만 정하면 돼요.

평균 벡터 $E[\mathbf{x}] = [E[x_1], E[x_2]]^\top$의 첫 성분이 $x_1$의 평균이에요. $E[x_1] = 1$이에요.

공분산 행렬의 대각 성분은 각 변수의 분산이에요. $(1,1)$ 성분이 $\mathrm{cov}(x_1, x_1) = \mathrm{var}[x_1] = 0.5$예요.

비대각 성분 $-1$은 $x_1$과 $x_2$의 관계를 나타내요. $x_2$를 적분해 없애면 이 관계는 $x_1$만의 분포에 남지 않아요.

따라서

$$
p(x_1) = \mathcal{N}(1, 0.5)
$$

#### 완성 답과 검산

#### 검산

x1의 주변분포는 아래 원 조건의 첫 평균과 첫 대각 분산을 그대로 가진 가우시안이에요. 비대각 공분산은 둘 사이의 관계지만 한 변수의 주변분산을 바꾸지 않아요.

정답: $p(x_1) = \mathcal{N}(1, 0.5)$

#### 여기서 주의해요

조건부분산의 Schur complement를 주변분산에 쓰지 않아요.

#### 설명을 닫고 다시 해요

1. $\mu_1=1$, $\Sigma_{11}=0.5$를 원 행렬에서 읽어요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 조건부분산의 Schur complement를 주변분산에 쓰지 않아요.

**페이지 요약**

#### 떠올릴 개념·공식

가우시안 주변화(Gaussian marginalization)는 관심 성분의 평균과 공분산 대각을 남겨요.

#### 첫 줄

$\mu_1=1$, $\Sigma_{11}=0.5$를 원 행렬에서 읽어요.

#### 검산

x1의 주변분포는 아래 원 조건의 첫 평균과 첫 대각 분산을 그대로 가진 가우시안이에요. 비대각 공분산은 둘 사이의 관계지만 한 변수의 주변분산을 바꾸지 않아요.

---

<a id="p5"></a>

### P5. 독립인 가우시안의 가중합 구하기

MML Example 6.7 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1007_Product_of_Gaussians.html#p5)

#### 주어진 조건

서로 독립인 두 가우시안 확률변수가 있어요.

$$
x \sim \mathcal{N}(1, 2), \qquad y \sim \mathcal{N}(-1, 3)
$$

상수 $a = 2$, $b = -1$로 가중합 $ax + by = 2x - y$를 만들어요.

#### 구할 것

$2x - y$의 분포를 구해 보세요. 평균과 분산을 함께 적어 보세요.

#### 무엇을 구하는 문제인가요?

독립인 가우시안의 가중합 구하기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

독립 가우시안의 가중합은 가우시안이고 평균은 선형, 분산은 계수의 제곱으로 계산해요. $Var(2X-Y)=4Var(X)+Var(Y)$로 −1의 제곱이+1이에요.

#### 종이에 적을 첫 줄

$E[2X-Y]=2E[X]-E[Y]$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

$2x$와 $-y$는 각각 가우시안의 상수배라서 가우시안이고, 서로 독립이에요. 독립인 가우시안의 합도 가우시안이니까 $2x - y$는 가우시안이에요. 평균과 분산만 구하면 돼요.

기댓값은 선형이에요.

$$
E[2x - y] = 2E[x] - E[y] = 2 \cdot 1 - (-1) = 3
$$

상수배는 분산에서 제곱해서 나와요. $\mathrm{var}[2x] = 2^2 \cdot 2 = 8$, $\mathrm{var}[-y] = (-1)^2 \cdot 3 = 3$이에요.

$x$와 $y$가 독립이라 공분산이 0이에요. 그래서 합의 분산은 분산의 합이에요.

$$
\mathrm{var}[2x - y] = a^2\sigma_x^2 + b^2\sigma_y^2 = 8 + 3 = 11
$$

따라서

$$
2x - y \sim \mathcal{N}(3, 11)
$$

#### 완성 답과 검산

#### 검산

조건의 평균으로2μx−μy=3, 분산으로4×2+3=11이므로 N(3,11)이에요.

정답: $2x - y \sim \mathcal{N}(3, 11)$ (평균 $3$, 분산 $11$)

#### 여기서 주의해요

빼기라고 분산3을 빼지 않아요. 독립이라 교차항이0이에요.

#### 설명을 닫고 다시 해요

1. $E[2X-Y]=2E[X]-E[Y]$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 빼기라고 분산3을 빼지 않아요. 독립이라 교차항이0이에요.

**페이지 요약**

#### 떠올릴 개념·공식

독립 가우시안의 가중합은 가우시안이고 평균은 선형, 분산은 계수의 제곱으로 계산해요. $Var(2X-Y)=4Var(X)+Var(Y)$

#### 첫 줄

$E[2X-Y]=2E[X]-E[Y]$예요.

#### 검산

조건의 평균으로2μx−μy=3, 분산으로4×2+3=11이므로 N(3,11)이에요.

---

<a id="p6"></a>

### P6. 가우시안 혼합의 차원별 주변분포

MML Exercise 6.2 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1007_Product_of_Gaussians.html#p6)

#### 주어진 조건

두 가우시안을 섞은 2차원 분포 $\mathbf{x} = [x_1, x_2]^\top$가 있어요.

$$
p(\mathbf{x}) = 0.4\,\mathcal{N}\left(\left[\begin{matrix}10 \\ 2\end{matrix}\right], \left[\begin{matrix}1 \\ 0\end{matrix}\;\;\begin{matrix}0 \\ 1\end{matrix}\right]\right) + 0.6\,\mathcal{N}\left(\left[\begin{matrix}0 \\ 0\end{matrix}\right], \left[\begin{matrix}8.4 \\ 2.0\end{matrix}\;\;\begin{matrix}2.0 \\ 1.7\end{matrix}\right]\right)
$$

이 식은 성분 가우시안 둘을 $p_1(\mathbf{x})$, $p_2(\mathbf{x})$라 할 때 $p(\mathbf{x}) = 0.4\,p_1(\mathbf{x}) + 0.6\,p_2(\mathbf{x})$라는 뜻이에요. $\mathbf{x}$가 40% 확률로 첫째 성분에서, 60% 확률로 둘째 성분에서 나온다는 말이에요. 이런 가중합에 대한 적분과 기댓값은 각 성분에 대한 적분과 기댓값의 가중합으로 나뉘어요. 결합 가우시안에서 한 변수만 남긴 주변분포는 가우시안이고, 평균은 평균 벡터의 해당 성분, 분산은 공분산 행렬의 해당 대각 성분이라고 알려져 있어요. 그대로 써도 돼요.

#### 구할 것

각 차원의 주변분포 $p(x_1)$과 $p(x_2)$를 구해 보세요.

#### 무엇을 구하는 문제인가요?

가우시안 혼합의 차원별 주변분포를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

혼합분포(mixture)의 주변화는 적분의 선형성으로 각 성분을 주변화한 뒤 같은 가중치로 섞어요. 하나의 가우시안으로 합쳐 쓰는 문제가 아니에요.

#### 종이에 적을 첫 줄

$p(x_1)=0.4\int p_1(x)dx_2+0.6\int p_2(x)dx_2$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

$p(x_1)$은 $x_2$를 적분해서 얻어요. 적분은 선형이라서 가중치가 그대로 밖으로 나와요.

$$
p(x_1) = \int p(\mathbf{x})\,dx_2 = 0.4\int \mathcal{N}_1(\mathbf{x})\,dx_2 + 0.6\int \mathcal{N}_2(\mathbf{x})\,dx_2
$$

여기서 $\mathcal{N}_1$, $\mathcal{N}_2$는 첫째, 둘째 성분 가우시안이에요.

결합 가우시안을 주변화하면 가우시안이고, 평균 벡터의 해당 성분과 공분산 행렬의 해당 대각 성분을 그대로 가져와요.

첫째 성분에서 $x_1$의 평균은 $10$, 분산은 $1$이에요. 둘째 성분에서는 평균 $0$, 분산 $8.4$예요. 그래서

$$
p(x_1) = 0.4\,\mathcal{N}(10, 1) + 0.6\,\mathcal{N}(0, 8.4)
$$

$x_2$도 같은 방법으로 $x_1$을 적분해요. 첫째 성분에서 평균 $2$, 분산 $1$, 둘째 성분에서 평균 $0$, 분산 $1.7$이에요. 그래서

$$
p(x_2) = 0.4\,\mathcal{N}(2, 1) + 0.6\,\mathcal{N}(0, 1.7)
$$

비대각 성분 $2.0$은 $x_1$과 $x_2$의 관계라서 한 차원만 남긴 주변분포에는 들어가지 않아요. 두 결과 모두 가중치 합이 $0.4 + 0.6 = 1$이라 확률분포가 맞아요.

#### 완성 답과 검산

#### 검산

x1은0.4N(10,1)+0.6N(0,8.4), x2는0.4N(2,1)+0.6N(0,1.7)예요. 각각 적분은가중치합1이고 성분평균·대각분산이 보존돼요.

정답: $p(x_1) = 0.4\,\mathcal{N}(10, 1) + 0.6\,\mathcal{N}(0, 8.4)$, $p(x_2) = 0.4\,\mathcal{N}(2, 1) + 0.6\,\mathcal{N}(0, 1.7)$

#### 여기서 주의해요

혼합 가중치0.4,0.6을 분산으로 곱한 단일가우시안으로 바꾸지 않아요.

#### 설명을 닫고 다시 해요

1. $p(x_1)=0.4\int p_1(x)dx_2+0.6\int p_2(x)dx_2$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 혼합 가중치0.4,0.6을 분산으로 곱한 단일가우시안으로 바꾸지 않아요.

**페이지 요약**

#### 떠올릴 개념·공식

혼합분포(mixture)의 주변화는 적분의 선형성으로 각 성분을 주변화한 뒤 같은 가중치로 섞어요.

#### 첫 줄

$p(x_1)=0.4\int p_1(x)dx_2+0.6\int p_2(x)dx_2$예요.

#### 검산

x1은0.4N(10,1)+0.6N(0,8.4), x2는0.4N(2,1)+0.6N(0,1.7)예요. 각각 적분은가중치합1이고 성분평균·대각분산이 보존돼요.

---

<a id="p7"></a>

### P7. 가우시안 혼합의 평균

MML Exercise 6.2 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1007_Product_of_Gaussians.html#p7)

#### 주어진 조건

두 가우시안을 섞은 2차원 분포 $\mathbf{x} = [x_1, x_2]^\top$가 있어요.

$$
p(\mathbf{x}) = 0.4\,\mathcal{N}\left(\left[\begin{matrix}10 \\ 2\end{matrix}\right], \left[\begin{matrix}1 \\ 0\end{matrix}\;\;\begin{matrix}0 \\ 1\end{matrix}\right]\right) + 0.6\,\mathcal{N}\left(\left[\begin{matrix}0 \\ 0\end{matrix}\right], \left[\begin{matrix}8.4 \\ 2.0\end{matrix}\;\;\begin{matrix}2.0 \\ 1.7\end{matrix}\right]\right)
$$

이 식은 성분 가우시안 둘을 $p_1(\mathbf{x})$, $p_2(\mathbf{x})$라 할 때 $p(\mathbf{x}) = 0.4\,p_1(\mathbf{x}) + 0.6\,p_2(\mathbf{x})$라는 뜻이에요. $\mathbf{x}$가 40% 확률로 첫째 성분에서, 60% 확률로 둘째 성분에서 나온다는 말이에요. 이런 가중합에 대한 적분과 기댓값은 각 성분에 대한 적분과 기댓값의 가중합으로 나뉘어요.

#### 구할 것

- (a) 각 차원의 평균 $E[x_1]$, $E[x_2]$를 구해 보세요.
- (b) 2차원 분포의 평균 벡터 $E[\mathbf{x}]$를 적어 보세요.

#### 무엇을 구하는 문제인가요?

가우시안 혼합의 평균를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

혼합의 평균은 성분 선택변수에 대한 반복 기댓값이에요. $E[X]=\sum_k\pi_k\mu_k$에서 π는 선택확률, μ는 각 성분평균이에요. 공분산까지 이 공식을 그대로 쓰면 안 돼요.

#### 종이에 적을 첫 줄

$E[x]=0.4[10,2]^\top+0.6[0,0]^\top$예요.

#### 왜 이렇게 푸는지 함께 따라가요

평균의 정의에 혼합식을 넣고, 적분의 선형성으로 나눠요.

$$
E[\mathbf{x}] = \int \mathbf{x}\,p(\mathbf{x})\,d\mathbf{x} = 0.4\int \mathbf{x}\,\mathcal{N}_1(\mathbf{x})\,d\mathbf{x} + 0.6\int \mathbf{x}\,\mathcal{N}_2(\mathbf{x})\,d\mathbf{x}
$$

각 적분은 성분 가우시안의 평균 벡터예요. 그래서

$$
E[\mathbf{x}] = 0.4\left[\begin{matrix}10 \\ 2\end{matrix}\right] + 0.6\left[\begin{matrix}0 \\ 0\end{matrix}\right]
$$

#### (a)

랜덤 벡터의 평균은 성분마다 평균이에요. 성분별로 계산하면

$$
E[x_1] = 0.4 \cdot 10 + 0.6 \cdot 0 = 4
$$

$$
E[x_2] = 0.4 \cdot 2 + 0.6 \cdot 0 = 0.8
$$

#### (b)

두 값을 세로로 모으면 평균 벡터예요.

$$
E[\mathbf{x}] = [4, 0.8]^\top
$$

#### 완성 답과 검산

#### (a) 검산

각 차원은4와0.8이에요. 주변혼합에서 평균을 따로 계산해도 같아요.

#### (b) 검산

두 평균을 열벡터로 모으면[4,0.8]ᵀ예요. 공분산 행렬의 비대각은 평균 계산에 들어가지 않아요.

정답: (a) $E[x_1] = 4$, $E[x_2] = 0.8$ (b) $E[\mathbf{x}] = [4, 0.8]^\top$

#### 여기서 주의해요

성분 간 평균 차이가 분산에도 기여하지만 이 문제는 평균만 구해요.

#### 설명을 닫고 다시 해요

1. $E[x]=0.4[10,2]^\top+0.6[0,0]^\top$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 성분 간 평균 차이가 분산에도 기여하지만 이 문제는 평균만 구해요.

**페이지 요약**

#### 떠올릴 개념·공식

혼합의 평균은 성분 선택변수에 대한 반복 기댓값이에요. $E[X]=\sum_k\pi_k\mu_k$

#### 첫 줄

$E[x]=0.4[10,2]^\top+0.6[0,0]^\top$예요.

#### 검산

각 차원은4와0.8이에요. 주변혼합에서 평균을 따로 계산해도 같아요. 두 평균을 열벡터로 모으면[4,0.8]ᵀ예요. 공분산 행렬의 비대각은 평균 계산에 들어가지 않아요.

---

<a id="p8"></a>

### P8. 두 가우시안 밀도의 곱: 완전제곱식으로 유도하기

MML Exercise 6.10 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1007_Product_of_Gaussians.html#p8)

#### 주어진 조건

$\mathbf{x} \in \mathbb{R}^D$에 대한 두 가우시안 밀도 $\mathcal{N}(\mathbf{x} \mid \mathbf{a}, \mathbf{A})$와 $\mathcal{N}(\mathbf{x} \mid \mathbf{b}, \mathbf{B})$가 있어요. $\mathbf{A}$, $\mathbf{B}$는 공분산 행렬이라 대칭이고 역행렬이 있어요. $\mathbf{A}^{-1} + \mathbf{B}^{-1}$도 대칭이고 양의 정부호(그래서 역행렬이 있음)라는 사실은 그대로 써도 돼요. 두 밀도의 곱은 정규화되지 않은 가우시안이에요.

$$
\mathcal{N}(\mathbf{x} \mid \mathbf{a}, \mathbf{A})\,\mathcal{N}(\mathbf{x} \mid \mathbf{b}, \mathbf{B}) \propto \mathcal{N}(\mathbf{x} \mid \mathbf{c}, \mathbf{C})
$$

여기서 $\propto$는 "$\mathbf{x}$와 무관한 상수 배를 빼면 같다"는 뜻이에요.

#### 구할 것

완전제곱식을 만들어서 아래 두 식이 성립함을 보여 보세요.

$$
\mathbf{C} = (\mathbf{A}^{-1} + \mathbf{B}^{-1})^{-1}
$$

$$
\mathbf{c} = \mathbf{C}(\mathbf{A}^{-1}\mathbf{a} + \mathbf{B}^{-1}\mathbf{b})
$$

#### 무엇을 구하는 문제인가요?

두 가우시안 밀도의 곱: 완전제곱식으로 유도하기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

두 밀도의 곱(product of Gaussians)은 지수의 이차형식을 더해요. 정밀도(precision) Λ=A⁻¹+B⁻¹와 η=A⁻¹a+B⁻¹b를 정의하면 완전제곱식의 중심은 Λ⁻¹η예요. A,B는 양의 정부호이고 계수 순서를 지켜요.

#### 종이에 적을 첫 줄

$\Lambda=A^{-1}+B^{-1}$, $\eta=A^{-1}a+B^{-1}b$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

두 이차형식을 따로 이름 붙여요.

$$
Q_A=(\mathbf{x}-\mathbf{a})^\top\mathbf{A}^{-1}(\mathbf{x}-\mathbf{a})
$$

$$
Q_B=(\mathbf{x}-\mathbf{b})^\top\mathbf{B}^{-1}(\mathbf{x}-\mathbf{b})
$$

두 밀도의 곱을 $P(\mathbf{x})$라고 하면, 입력과 무관한 정규화 상수를 제외하고

$$
P(\mathbf{x})\propto\exp\left(-\frac12(Q_A+Q_B)\right)
$$

예요. 곱의 지수를 더한다는 뜻이에요.

첫째 이차형식을 펼쳐요. $\mathbf{A}^{-1}$이 대칭이라 $\mathbf{x}^\top\mathbf{A}^{-1}\mathbf{a} = \mathbf{a}^\top\mathbf{A}^{-1}\mathbf{x}$예요.

$$
(\mathbf{x} - \mathbf{a})^\top\mathbf{A}^{-1}(\mathbf{x} - \mathbf{a}) = \mathbf{x}^\top\mathbf{A}^{-1}\mathbf{x} - 2(\mathbf{A}^{-1}\mathbf{a})^\top\mathbf{x} + \mathbf{a}^\top\mathbf{A}^{-1}\mathbf{a}
$$

둘째도 같은 꼴이에요.

$$
(\mathbf{x} - \mathbf{b})^\top\mathbf{B}^{-1}(\mathbf{x} - \mathbf{b}) = \mathbf{x}^\top\mathbf{B}^{-1}\mathbf{x} - 2(\mathbf{B}^{-1}\mathbf{b})^\top\mathbf{x} + \mathbf{b}^\top\mathbf{B}^{-1}\mathbf{b}
$$

더해서 묶어요. $\boldsymbol{\Lambda} = \mathbf{A}^{-1} + \mathbf{B}^{-1}$, $\boldsymbol{\eta} = \mathbf{A}^{-1}\mathbf{a} + \mathbf{B}^{-1}\mathbf{b}$로 두면

$$
[\cdots] = \mathbf{x}^\top\boldsymbol{\Lambda}\mathbf{x} - 2\boldsymbol{\eta}^\top\mathbf{x} + \gamma
$$

이고, 상수항은

$$
\gamma = \mathbf{a}^\top\mathbf{A}^{-1}\mathbf{a} + \mathbf{b}^\top\mathbf{B}^{-1}\mathbf{b}
$$

스칼라 렘마의 $\alpha$ 자리에 $\boldsymbol{\Lambda}$, $\beta$ 자리에 $\boldsymbol{\eta}$가 왔어요.

완전제곱식을 만들어요. $\mathbf{m} = \boldsymbol{\Lambda}^{-1}\boldsymbol{\eta}$로 두고 펼쳐 봐요. $\boldsymbol{\Lambda}$가 대칭이라 $\mathbf{m}^\top\boldsymbol{\Lambda} = \boldsymbol{\eta}^\top$이에요.

$$
(\mathbf{x} - \mathbf{m})^\top\boldsymbol{\Lambda}(\mathbf{x} - \mathbf{m}) = \mathbf{x}^\top\boldsymbol{\Lambda}\mathbf{x} - 2\boldsymbol{\eta}^\top\mathbf{x} + \boldsymbol{\eta}^\top\boldsymbol{\Lambda}^{-1}\boldsymbol{\eta}
$$

그래서 같은 수를 더하고 빼면

$$
\mathbf{x}^\top\boldsymbol{\Lambda}\mathbf{x} - 2\boldsymbol{\eta}^\top\mathbf{x} + \gamma = (\mathbf{x} - \mathbf{m})^\top\boldsymbol{\Lambda}(\mathbf{x} - \mathbf{m}) + \left(\gamma - \boldsymbol{\eta}^\top\boldsymbol{\Lambda}^{-1}\boldsymbol{\eta}\right)
$$

괄호 안 상수는 $\mathbf{x}$와 무관하니 앞쪽 상수로 넘겨요.

$$
\mathcal{N}(\mathbf{x} \mid \mathbf{a}, \mathbf{A})\,\mathcal{N}(\mathbf{x} \mid \mathbf{b}, \mathbf{B}) \propto \exp\left(-\frac{1}{2}(\mathbf{x} - \mathbf{m})^\top\boldsymbol{\Lambda}(\mathbf{x} - \mathbf{m})\right)
$$

가우시안 PDF의 지수 $-\frac{1}{2}(\mathbf{x} - \boldsymbol{\mu})^\top\Sigma^{-1}(\mathbf{x} - \boldsymbol{\mu})$와 맞춰 보면 $\Sigma^{-1} = \boldsymbol{\Lambda}$, $\boldsymbol{\mu} = \mathbf{m}$이에요. 그러니

$$
\mathbf{C} = \boldsymbol{\Lambda}^{-1} = (\mathbf{A}^{-1} + \mathbf{B}^{-1})^{-1}
$$

$$
\mathbf{c} = \mathbf{m} = \boldsymbol{\Lambda}^{-1}\boldsymbol{\eta} = \mathbf{C}(\mathbf{A}^{-1}\mathbf{a} + \mathbf{B}^{-1}\mathbf{b})
$$

1차원으로 확인해요. $\mathbf{A} = \nu_0$, $\mathbf{B} = \nu_1$, $\mathbf{a} = \mu_0$, $\mathbf{b} = \mu_1$을 넣으면

$$
C = \left(\frac{1}{\nu_0} + \frac{1}{\nu_1}\right)^{-1} = \frac{\nu_0\nu_1}{\nu_0 + \nu_1}
$$

$$
c = \frac{\nu_0\nu_1}{\nu_0 + \nu_1}\left(\frac{\mu_0}{\nu_0} + \frac{\mu_1}{\nu_1}\right) = \frac{\nu_1\mu_0 + \nu_0\mu_1}{\nu_0 + \nu_1}
$$

스칼라 곱 공식과 같은 결과가 나와요.

#### 완성 답과 검산

#### 검산

m=Λ⁻¹η이면 Λm=η예요. (x−m)ᵀΛ(x−m)을 전개하면 xᵀΛx−2ηᵀx+ηᵀΛ⁻¹η예요. 원 식과 차이는 x와 무관한 상수라 C=Λ⁻¹,c=m이 정확히 나와요. 이는 일반 대칭 정부호 행렬에 대한 증명이에요.

정답: $\mathbf{C} = (\mathbf{A}^{-1} + \mathbf{B}^{-1})^{-1}$, $\mathbf{c} = \mathbf{C}(\mathbf{A}^{-1}\mathbf{a} + \mathbf{B}^{-1}\mathbf{b})$

#### 여기서 주의해요

밀도의 곱은 일반적으로 적분1이 아니에요. ∝를=로 바꾸거나 공분산을A+B로 쓰지 않아요.

#### 설명을 닫고 다시 해요

1. $\Lambda=A^{-1}+B^{-1}$, $\eta=A^{-1}a+B^{-1}b$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 밀도의 곱은 일반적으로 적분1이 아니에요. ∝를=로 바꾸거나 공분산을A+B로 쓰지 않아요.

**페이지 요약**

#### 떠올릴 개념·공식

두 밀도의 곱(product of Gaussians)은 지수의 이차형식을 더해요. 정밀도(precision) Λ=A⁻¹+B⁻¹와 η=A⁻¹a+B⁻¹b를 정의하면 완전제곱식의 중심은 Λ⁻¹η예요.

#### 첫 줄

$\Lambda=A^{-1}+B^{-1}$, $\eta=A^{-1}a+B^{-1}b$예요.

#### 검산

m=Λ⁻¹η이면 Λm=η예요. (x−m)ᵀΛ(x−m)을 전개하면 xᵀΛx−2ηᵀx+ηᵀΛ⁻¹η예요. 원 식과 차이는 x와 무관한 상수라 C=Λ⁻¹,c=m이 정확히 나와요. 이는 일반 대칭 정부호 행렬에 대한 증명이에요.

---

원 문제·정리노트·PDF는 보존해요.
