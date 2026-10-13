# 복습문제 8선 — 0928 수업 범위

MML 9장 본문 예제 변형 **3개**와 5장 연습문제 **5개**로 구성했어요. 먼저 풀어 보고, 막히면 힌트를 열어 보세요.

> `복습문제_0928_Linear_Regression.html`를 마크다운으로 옮겼어요. 원문, 힌트, 풀이는 접혀 있어요. 먼저 풀어 보고 펼쳐 보세요.

**목차**

- [A. 교과서 본문 예제 변형 (MML 9장)](#partA)
  - [P1. 2차 다항식의 특징행렬 쓰기](#p1)
  - [P2. 3차 다항식 최대우도 적합 준비하기](#p2)
  - [P3. 사전분포를 바꾼 다항회귀 MAP](#p3)
- [B. 교과서 연습문제 (MML 5장)](#partB)
  - [P4. 곱의 미분과 치환 미분](#p4)
  - [P5. 가우시안 모양 함수 미분하기](#p5)
  - [P6. 연쇄법칙과 편미분의 차원](#p6)
  - [P7. tanh 층의 자코비안 차원](#p7)
  - [P8. 로지스틱 시그모이드 미분하기](#p8)

<a id="partA"></a>

## A. 교과서 본문 예제 변형 (MML 9장)

<a id="p1"></a>

### P1. 2차 다항식의 특징행렬 쓰기

입력이 스칼라인 훈련 데이터 $N = 3$개가 있어요: $x_1 = -1$, $x_2 = 1$, $x_3 = 2$. 2차 다항식 특징 $\boldsymbol{\phi}(x) = [1, x, x^2]^\top$을 쓸 때, 특징행렬 $\boldsymbol{\Phi}$를 숫자로 적어 보세요.

<details><summary>교과서 원문 보기</summary>

"For a second-order polynomial and $N$ training points $x_n \in \mathbb{R}$, $n = 1, \dots, N$, the feature matrix is" — Example 9.4

</details>

<details><summary>힌트 보기</summary>

$n$번째 행은 $\boldsymbol{\phi}^\top(x_n) = [1, x_n, x_n^2]$이에요. 데이터 하나가 한 행이 돼요.

</details>

<details><summary>풀이 보기</summary>

1. 특징이 $1, x, x^2$ 세 개라서 $K = 3$이고, 행은 데이터 수만큼 $N = 3$개예요. 그래서 $\boldsymbol{\Phi} \in \mathbb{R}^{3 \times 3}$이에요.
2. $\Phi_{ij} = \phi_j(x_i)$이므로 $i$번째 행에 $[1, x_i, x_i^2]$를 적어요.
3. $x_1 = -1$이면 $[1, -1, 1]$, $x_2 = 1$이면 $[1, 1, 1]$, $x_3 = 2$이면 $[1, 2, 4]$예요.
4. 세 행을 위에서부터 쌓아요.

   $$
   \boldsymbol{\Phi} = \begin{bmatrix} 1 & -1 & 1 \\ 1 & 1 & 1 \\ 1 & 2 & 4 \end{bmatrix}
   $$
5. 수업과의 연결: 0928 수업에서 "첫 행은 $\mathbf{x}_1$로, 마지막 행은 $\mathbf{x}_N$으로 만든다"고 한 특징행렬 $\Phi_{ij} = \phi_j(\mathbf{x}_i)$를 숫자로 채워 본 거예요.

**정답:** $\boldsymbol{\Phi} = \begin{bmatrix} 1 & -1 & 1 \\ 1 & 1 & 1 \\ 1 & 2 & 4 \end{bmatrix}$

</details>

---

<a id="p2"></a>

### P2. 3차 다항식 최대우도 적합 준비하기

데이터셋이 $N = 8$개의 쌍 $(x_n, y_n)$으로 이뤄져 있어요. $x_n \sim \mathcal{U}[-5, 5]$이고 $y_n = -\sin(x_n/5) + \cos(x_n) + \epsilon$, $\epsilon \sim \mathcal{N}(0, 0.2^2)$이에요. 이 데이터에 3차 다항식을 최대우도 추정으로 맞추려고 해요.

- (a) 특징 벡터 $\boldsymbol{\phi}(x)$의 길이 $K$는 얼마인가요?
- (b) 특징행렬 $\boldsymbol{\Phi}$의 크기는 얼마인가요?
- (c) 최대우도 해 $\boldsymbol{\theta}_{\text{ML}}$을 $\boldsymbol{\Phi}$와 $\mathbf{y}$로 적어 보세요.

<details><summary>교과서 원문 보기</summary>

"We fit a polynomial of degree 4 using maximum likelihood estimation" — Example 9.5

</details>

<details><summary>힌트 보기</summary>

3차 다항식은 $x^0$부터 $x^3$까지 항을 가져요. $\boldsymbol{\Phi}$는 데이터 하나가 한 행이에요.

</details>

<details><summary>풀이 보기</summary>

1. (a) 3차 다항식의 특징은 $\boldsymbol{\phi}(x) = [1, x, x^2, x^3]^\top$이에요. 항이 네 개라서 $K = 4$예요.
2. (b) 행은 데이터 수 $N = 8$개, 열은 특징 수 $K = 4$개예요. 그래서 $\boldsymbol{\Phi} \in \mathbb{R}^{8 \times 4}$이고, $n$번째 행은 $[1, x_n, x_n^2, x_n^3]$이에요.
3. (c) 음의 로그우도는 $\frac{1}{2\sigma^2}\|\mathbf{y} - \boldsymbol{\Phi}\boldsymbol{\theta}\|^2 + \text{const}$예요. 이걸 $\boldsymbol{\theta}$로 미분해 0으로 두면

   $$
   \boldsymbol{\theta}_{\text{ML}} = (\boldsymbol{\Phi}^\top \boldsymbol{\Phi})^{-1} \boldsymbol{\Phi}^\top \mathbf{y}
   $$
4. 이때 $\boldsymbol{\Phi}^\top \boldsymbol{\Phi}$는 $4 \times 4$라서 역행렬 계산이 작아요.
5. 수업과의 연결: 0928 수업에서 "3차면 $K = 4$"라고 한 말과, $\mathbf{X}$ 자리에 $\boldsymbol{\Phi}$를 넣은 유사역행렬 해를 그대로 쓴 거예요.

**정답:** (a) $K = 4$ (b) $\boldsymbol{\Phi} \in \mathbb{R}^{8 \times 4}$ (c) $\boldsymbol{\theta}_{\text{ML}} = (\boldsymbol{\Phi}^\top \boldsymbol{\Phi})^{-1} \boldsymbol{\Phi}^\top \mathbf{y}$

</details>

---

<a id="p3"></a>

### P3. 사전분포를 바꾼 다항회귀 MAP

잡음이 $\epsilon \sim \mathcal{N}(0, 0.2^2)$인 다항회귀 데이터에서 파라미터에 가우시안 사전분포 $p(\boldsymbol{\theta}) = \mathcal{N}(\mathbf{0}, \frac{1}{4}\mathbf{I})$를 두고 MAP 추정을 해요. MAP 해는 아래와 같아요.

$$
\boldsymbol{\theta}_{\text{MAP}} = \left(\boldsymbol{\Phi}^\top \boldsymbol{\Phi} + \frac{\sigma^2}{b^2} \mathbf{I}\right)^{-1} \boldsymbol{\Phi}^\top \mathbf{y}
$$

- (a) 이 식에 들어가는 $\frac{\sigma^2}{b^2}$ 값을 구해 보세요.
- (b) 6차 다항식과 8차 다항식 중 어느 쪽에서 사전분포(정규화)의 효과가 크게 드러날까요? 이유도 말해 보세요.

<details><summary>교과서 원문 보기</summary>

"The prior (regularizer) does not play a significant role for the low-degree polynomial" — Example 9.6

</details>

<details><summary>힌트 보기</summary>

$\mathcal{N}(\mathbf{0}, b^2 \mathbf{I})$와 비교해 $b^2$를 읽어요. 차수가 높을수록 최대우도 해가 점을 억지로 다 지나려고 해요.

</details>

<details><summary>풀이 보기</summary>

1. (a) 잡음 표준편차가 $0.2$라서 $\sigma^2 = 0.04 = \frac{1}{25}$이에요.
2. 사전분포 $\mathcal{N}(\mathbf{0}, \frac{1}{4}\mathbf{I})$를 $\mathcal{N}(\mathbf{0}, b^2 \mathbf{I})$와 맞춰 보면 $b^2 = \frac{1}{4}$이에요.
3. 나누면 $\frac{\sigma^2}{b^2} = \frac{1/25}{1/4} = \frac{4}{25} = 0.16$이에요.
4. (b) 차수가 높을수록 최대우도 해는 점을 다 지나려고 계수를 크게 키워요(과적합). 그래서 8차의 최대우도 계수가 6차보다 커요.
5. $\frac{1}{2b^2} \boldsymbol{\theta}^\top \boldsymbol{\theta}$ 항은 $\boldsymbol{\theta}$가 클수록 크게 벌줘요. 계수가 큰 8차에서 이 항이 더 많이 끌어내려, 사전분포(정규화) 효과가 더 크게 드러나요.
6. 수업과의 연결: 0928 수업에서 ML과 MAP는 $\frac{\sigma^2}{b^2}\mathbf{I}$ 한 항만 다르고 이 항이 정규화(regularizer) 역할을 한다고 했어요. $b^2$를 $\frac{1}{4}$로 작게 잡을수록 이 항이 커져 선호를 더 강하게 반영해요.

**정답:** (a) $\frac{\sigma^2}{b^2} = \frac{4}{25} = 0.16$ (b) 8차 다항식. 차수가 높을수록 최대우도 계수가 커지므로 사전분포(정규화) 효과가 더 크게 드러나요.

</details>

---

<a id="partB"></a>

## B. 교과서 연습문제 (MML 5장)

<a id="p4"></a>

### P4. 곱의 미분과 치환 미분

아래 함수의 도함수 $f'(x)$를 구해 보세요. $\log$는 자연로그예요.

$$
f(x) = \log(x^4) \sin(x^3)
$$

<details><summary>교과서 원문 보기</summary>

"Compute the derivative $f'(x)$ for $f(x) = \log(x^4) \sin(x^3)$." — Exercise 5.1

</details>

<details><summary>힌트 보기</summary>

두 함수의 곱이라 곱의 미분을 써요. 각 조각은 안쪽 $x^4$, $x^3$을 치환해서 미분해요.

</details>

<details><summary>풀이 보기</summary>

1. 곱의 미분: $f'(x) = [\log(x^4)]' \sin(x^3) + \log(x^4) [\sin(x^3)]'$이에요.
2. $u = x^4$로 두면 $[\log u]' = \frac{1}{u} \cdot 4x^3 = \frac{4x^3}{x^4} = \frac{4}{x}$예요.
3. $v = x^3$으로 두면 $[\sin v]' = \cos v \cdot 3x^2 = 3x^2 \cos(x^3)$이에요.
4. 합치면

   $$
   f'(x) = \frac{4}{x} \sin(x^3) + 3x^2 \log(x^4) \cos(x^3)
   $$
5. 수업과의 연결: 0928 수업에서 $(x + 2y^3)^2$을 $y$로 미분할 때 쓴 치환 미분이 여기서도 두 번 쓰였어요. 교수님 말대로 $\log$는 자연로그(ln)예요.

**정답:** $f'(x) = \frac{4}{x} \sin(x^3) + 3x^2 \log(x^4) \cos(x^3)$

</details>

---

<a id="p5"></a>

### P5. 가우시안 모양 함수 미분하기

$\mu, \sigma \in \mathbb{R}$은 상수예요. 아래 함수의 도함수 $f'(x)$를 구해 보세요.

$$
f(x) = \exp\left(-\frac{1}{2\sigma^2}(x - \mu)^2\right)
$$

<details><summary>교과서 원문 보기</summary>

"Compute the derivative $f'(x)$ of the function … where $\mu, \sigma \in \mathbb{R}$ are constants." — Exercise 5.3

</details>

<details><summary>힌트 보기</summary>

지수 안쪽을 $u$로 치환해요. $[\exp u]' = \exp(u) \cdot u'$예요.

</details>

<details><summary>풀이 보기</summary>

1. $u = -\frac{1}{2\sigma^2}(x - \mu)^2$로 두면 $f = \exp(u)$예요.
2. $\frac{du}{dx} = -\frac{1}{2\sigma^2} \cdot 2(x - \mu) = -\frac{x - \mu}{\sigma^2}$예요.
3. 연쇄법칙으로 곱하면

   $$
   f'(x) = -\frac{x - \mu}{\sigma^2} \exp\left(-\frac{1}{2\sigma^2}(x - \mu)^2\right)
   $$
4. $x = \mu$에서 도함수가 0이라 여기가 봉우리예요.
5. 수업과의 연결: 0928 수업에서 가우시안 PDF의 지수 부분 $-\frac{(y - \mathbf{x}^\top\boldsymbol{\theta})^2}{2\sigma^2}$을 다뤘어요. 같은 꼴을 치환 미분으로 직접 미분해 본 거예요.

**정답:** $f'(x) = -\frac{x - \mu}{\sigma^2} \exp\left(-\frac{1}{2\sigma^2}(x - \mu)^2\right)$

</details>

---

<a id="p6"></a>

### P6. 연쇄법칙과 편미분의 차원

연쇄법칙으로 $\frac{df}{d\mathbf{x}}$를 구해 보세요. 각 편미분의 차원도 함께 적어요.

- (a) $f(z) = \log(1 + z)$, $z = \mathbf{x}^\top \mathbf{x}$, $\mathbf{x} \in \mathbb{R}^D$
- (b) $\mathbf{f}(\mathbf{z}) = \sin(\mathbf{z})$, $\mathbf{z} = \mathbf{A}\mathbf{x} + \mathbf{b}$, $\mathbf{A} \in \mathbb{R}^{E \times D}$, $\mathbf{x} \in \mathbb{R}^D$, $\mathbf{b} \in \mathbb{R}^E$. 여기서 $\sin$은 $\mathbf{z}$의 성분마다 따로 적용해요.

<details><summary>교과서 원문 보기</summary>

"Compute the derivatives df/dx of the following functions by using the chain rule. Provide the dimensions of every single partial derivative." — Exercise 5.7

</details>

<details><summary>힌트 보기</summary>

$\frac{df}{d\mathbf{x}} = \frac{df}{dz}\frac{dz}{d\mathbf{x}}$로 나눠요. (b)에서 $\sin(z_i)$는 $z_i$ 하나에만 기대요.

</details>

<details><summary>풀이 보기</summary>

1. (a) $\frac{df}{dz} = \frac{1}{1 + z}$이고, 스칼라라서 차원은 $1 \times 1$이에요.
2. $z = \mathbf{x}^\top \mathbf{x} = x_1^2 + \dots + x_D^2$이므로 $\frac{dz}{d\mathbf{x}} = 2\mathbf{x}^\top \in \mathbb{R}^{1 \times D}$예요.
3. 곱하면 $\frac{df}{d\mathbf{x}} = \frac{2\mathbf{x}^\top}{1 + \mathbf{x}^\top \mathbf{x}} \in \mathbb{R}^{1 \times D}$예요.
4. (b) $\frac{\partial f_i}{\partial z_j}$는 $i = j$일 때 $\cos z_i$, 아니면 0이에요. 그래서 $\frac{d\mathbf{f}}{d\mathbf{z}} = \operatorname{diag}(\cos \mathbf{z}) \in \mathbb{R}^{E \times E}$예요.
5. $\frac{d\mathbf{z}}{d\mathbf{x}} = \mathbf{A} \in \mathbb{R}^{E \times D}$예요. $\mathbf{b}$는 $\mathbf{x}$와 상관없어서 미분하면 0이에요.
6. 곱하면 $\frac{d\mathbf{f}}{d\mathbf{x}} = \operatorname{diag}(\cos \mathbf{z})\,\mathbf{A} \in \mathbb{R}^{E \times D}$예요. $(E \times E)(E \times D)$라 차원이 맞아요.
7. 수업과의 연결: 0928 수업의 $\frac{\partial L}{\partial \mathbf{e}} = 2\mathbf{e}^\top$, $\frac{d(\mathbf{A}\mathbf{x})}{d\mathbf{x}} = \mathbf{A}$를 연쇄법칙으로 이어 붙이고, "디멘션만 맞추면 된다"는 말대로 차원을 확인한 거예요.

**정답:** (a) $\frac{df}{d\mathbf{x}} = \frac{2\mathbf{x}^\top}{1 + \mathbf{x}^\top \mathbf{x}} \in \mathbb{R}^{1 \times D}$ (b) $\frac{d\mathbf{f}}{d\mathbf{x}} = \operatorname{diag}(\cos \mathbf{z})\,\mathbf{A} \in \mathbb{R}^{E \times D}$

</details>

---

<a id="p7"></a>

### P7. tanh 층의 자코비안 차원

아래 함수에서 연쇄법칙으로 $\frac{d\mathbf{f}}{d\mathbf{x}}$를 구해 보세요. 각 편미분의 차원도 적어요. 두 편미분의 곱을 끝까지 계산하지 않아도 돼요.

$$
\mathbf{f} = \tanh(\mathbf{z}) \in \mathbb{R}^M, \quad \mathbf{z} = \mathbf{A}\mathbf{x} + \mathbf{b}, \quad \mathbf{x} \in \mathbb{R}^N,\ \mathbf{A} \in \mathbb{R}^{M \times N},\ \mathbf{b} \in \mathbb{R}^M
$$

여기서 $\tanh$는 $\mathbf{z}$의 성분마다 따로 적용해요.

<details><summary>교과서 원문 보기</summary>

"You do not need to compute the product of the partial derivatives explicitly." — Exercise 5.8

</details>

<details><summary>힌트 보기</summary>

스칼라 함수의 도함수는 $\frac{d}{dz}\tanh z = 1 - \tanh^2 z$예요. $f_i$는 $z_i$ 하나에만 기대요.

</details>

<details><summary>풀이 보기</summary>

1. $\frac{d\mathbf{f}}{d\mathbf{x}} = \frac{d\mathbf{f}}{d\mathbf{z}}\frac{d\mathbf{z}}{d\mathbf{x}}$로 나눠요.
2. $\frac{\partial f_i}{\partial z_j}$는 $i = j$일 때 $1 - \tanh^2 z_i$, 아니면 0이에요. 그래서 $\frac{d\mathbf{f}}{d\mathbf{z}} = \operatorname{diag}(1 - \tanh^2 \mathbf{z}) \in \mathbb{R}^{M \times M}$예요.
3. $\frac{d\mathbf{z}}{d\mathbf{x}} = \mathbf{A} \in \mathbb{R}^{M \times N}$예요. $\mathbf{b}$는 상수라 사라져요.
4. 곱은 $(M \times M)(M \times N)$이므로 $\frac{d\mathbf{f}}{d\mathbf{x}} = \operatorname{diag}(1 - \tanh^2 \mathbf{z})\,\mathbf{A} \in \mathbb{R}^{M \times N}$예요.
5. 수업과의 연결: 0928 수업에서 $\mathbb{R}^n \to \mathbb{R}^m$ 함수의 자코비안은 $m \times n$이라고 했어요. 여기서도 $\mathbb{R}^N \to \mathbb{R}^M$이라 결과가 $M \times N$이에요. 수업에서 말한 DNN 가중치 학습도 이런 층의 연쇄법칙이에요.

**정답:** $\frac{d\mathbf{f}}{d\mathbf{z}} = \operatorname{diag}(1 - \tanh^2 \mathbf{z}) \in \mathbb{R}^{M \times M}$, $\frac{d\mathbf{z}}{d\mathbf{x}} = \mathbf{A} \in \mathbb{R}^{M \times N}$, $\frac{d\mathbf{f}}{d\mathbf{x}} \in \mathbb{R}^{M \times N}$

</details>

---

<a id="p8"></a>

### P8. 로지스틱 시그모이드 미분하기

로지스틱 시그모이드 함수의 도함수 $f'(x)$를 구해 보세요. 구한 결과를 $f(x)$로도 나타내 보세요.

$$
f(x) = \frac{1}{1 + \exp(-x)}
$$

<details><summary>교과서 원문 보기</summary>

"Compute the derivative $f'(x)$ of the logistic sigmoid" — Exercise 5.2

</details>

<details><summary>힌트 보기</summary>

$u = 1 + \exp(-x)$로 치환하면 $f = u^{-1}$이에요. $\exp(-x)$를 미분하면 $-\exp(-x)$예요.

</details>

<details><summary>풀이 보기</summary>

1. $u = 1 + \exp(-x)$로 두면 $f = u^{-1}$이고, $\frac{df}{du} = -u^{-2}$예요.
2. $\frac{du}{dx} = -\exp(-x)$예요.
3. 곱하면 부호 두 개가 상쇄돼요.

   $$
   f'(x) = -\frac{1}{(1 + \exp(-x))^2} \cdot (-\exp(-x)) = \frac{\exp(-x)}{(1 + \exp(-x))^2}
   $$
4. 분자를 $\exp(-x) = (1 + \exp(-x)) - 1$로 쪼개요. 그러면 $\frac{\exp(-x)}{1 + \exp(-x)} = 1 - f(x)$예요.
5. 그래서 $f'(x) = \frac{1}{1 + \exp(-x)} \cdot \frac{\exp(-x)}{1 + \exp(-x)} = f(x)(1 - f(x))$예요. 함숫값만 알면 도함수가 바로 나와요.
6. 수업과의 연결: 0928 수업에서 $(x + 2y^3)^2$에 쓴 치환 미분 그대로예요. 교수님이 DNN 가중치를 학습할 때 연쇄법칙을 많이 쓴다고 했는데, 시그모이드의 이 도함수가 그 연쇄에 자주 들어가요.

**정답:** $f'(x) = \frac{\exp(-x)}{(1 + \exp(-x))^2} = f(x)(1 - f(x))$

</details>

---

출처: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* (Cambridge University Press, 2020). 풀이는 자체 작성이며 수치는 Python으로 검증했습니다.
