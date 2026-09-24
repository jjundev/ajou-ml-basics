# 복습문제 7선 — 0914 수업 범위

MML 8장 본문 예제를 숫자만 바꾼 문제 **5문항**(어파인 모델, 최소제곱, 정규화, 가우시안 우도, 음의 로그우도)과 교과서 연습문제 **3문항**(MML 3·6·7장: 거리, 가우시안 우도, 정상점)으로 구성했어요. 먼저 풀어 보고, 막히면 힌트를 열어 보세요.

> `복습문제_0914_ERM_and_MLE.html`를 마크다운으로 옮겼어요. 원문, 힌트, 풀이는 접혀 있어요. 먼저 풀어 보고 펼쳐 보세요.

**목차**

- [A. 교과서 예제 변형 (MML 8장)](#partA)
  - [P1. 1을 붙여 어파인 예측기 계산하기](#p1)
  - [P2. 두 파라미터의 제곱 손실 평균 비교하기](#p2)
  - [P3. λ에 따라 달라지는 정규화 최소제곱의 선택](#p3)
  - [P4. 가우시안 우도의 평균과 분산 읽기](#p4)
  - [P5. 음의 로그우도와 최소제곱의 순서 비교하기](#p5)
- [B. 교과서 연습문제 (MML 3·6·7장)](#partB)
  - [P6. 두 벡터 사이의 유클리드 거리](#p6)
  - [P7. 삼차함수의 정상점과 종류](#p7)

<a id="partA"></a>

## A. 교과서 예제 변형 (MML 8장)

<a id="p1"></a>

### P1. 1을 붙여 어파인 예측기 계산하기

특징이 $D = 2$개인 예제 하나가 있어요. 특징 값은 $x_n^{(1)} = 2$, $x_n^{(2)} = -1$이에요. 교과서처럼 맨 앞에 단위 특징 $x^{(0)} = 1$을 붙여서 예측기를 $f(\mathbf{x}_n, \boldsymbol{\theta}) = \boldsymbol{\theta}^\top \mathbf{x}_n$으로 써요. 파라미터는 $\boldsymbol{\theta} = [\theta_0, \theta_1, \theta_2]^\top = [\tfrac{1}{2}, 3, 2]^\top$이에요.

- (a) 1을 붙인 벡터 $\mathbf{x}_n$을 써 보세요. 길이는 몇인가요?
- (b) 예측값 $f(\mathbf{x}_n, \boldsymbol{\theta})$를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"concatenating an additional unit feature $x^{(0)} = 1$ to $\mathbf{x}_n$ ... allowing us to write the predictor as a linear function" — Example 8.1

</details>

<details><summary>힌트 보기</summary>

$\theta_0$에는 항상 1이 곱해지도록 벡터 맨 앞에 1을 넣어요. 그다음 같은 자리끼리 곱해서 더해요.

</details>

<details><summary>풀이 보기</summary>

1. 맨 앞에 1을 붙이면 $\mathbf{x}_n = [1, x_n^{(1)}, x_n^{(2)}]^\top = [1, 2, -1]^\top$이에요.
2. 길이는 $D + 1 = 3$이에요. 그래서 예측기는 $f : \mathbb{R}^{D+1} \to \mathbb{R}$인 함수가 돼요.
3. 내적을 계산해요: $\boldsymbol{\theta}^\top \mathbf{x}_n = \tfrac{1}{2} \cdot 1 + 3 \cdot 2 + 2 \cdot (-1)$
4. $= \tfrac{1}{2} + 6 - 2 = \frac{9}{2}$
5. 어파인 꼴로 확인해요: $\theta_0 + \theta_1 x_n^{(1)} + \theta_2 x_n^{(2)} = \tfrac{1}{2} + 6 - 2$로 같아요.
6. 수업과의 연결: 교수님이 "가장 중요한 수식"이라고 한 바이어스 흡수예요. $b = \theta_0 \cdot 1$로 보고 1을 붙이면 어파인 함수가 내적 하나가 돼요 (0914 26:00).

**정답:** (a) $\mathbf{x}_n = [1, 2, -1]^\top$, 길이 $D + 1 = 3$ (b) $f(\mathbf{x}_n, \boldsymbol{\theta}) = \frac{9}{2}$

</details>

---

<a id="p2"></a>

### P2. 두 파라미터의 제곱 손실 평균 비교하기

학습 데이터가 세 개 있어요: $(x, y) = (0, 1), (1, 4), (2, 4)$. 각 입력 앞에 1을 붙여 $\mathbf{x}_n = [1, x_n]^\top$으로 쓰고, 예측기는 $f(\mathbf{x}_n, \boldsymbol{\theta}) = \boldsymbol{\theta}^\top \mathbf{x}_n$이에요. 제곱 손실의 평균은 행렬로 $\frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$이에요.

- (a) 데이터 행렬 $\mathbf{X}$와 라벨 벡터 $\mathbf{y}$를 써 보세요.
- (b) $\boldsymbol{\theta}_A = [1, 2]^\top$과 $\boldsymbol{\theta}_B = [\tfrac{3}{2}, \tfrac{3}{2}]^\top$ 각각에 대해 $\frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$를 구해 보세요.
- (c) 둘 중 어느 쪽의 평균 손실이 더 작나요?

<details><summary>교과서 원문 보기</summary>

"we specify that we measure the cost of making an error during training using the squared loss" — Example 8.2

</details>

<details><summary>힌트 보기</summary>

$\mathbf{X}\boldsymbol{\theta}$가 추정치 벡터 $\hat{\mathbf{y}}$예요. $\mathbf{y} - \hat{\mathbf{y}}$의 원소를 제곱해서 더하고 $N = 3$으로 나눠요.

</details>

<details><summary>풀이 보기</summary>

1. $\mathbf{X} = [\mathbf{x}_1, \mathbf{x}_2, \mathbf{x}_3]^\top \in \mathbb{R}^{3 \times 2}$이고, 행은 차례로 $[1, 0]$, $[1, 1]$, $[1, 2]$예요. $\mathbf{y} = [1, 4, 4]^\top$이에요.
2. $\boldsymbol{\theta}_A$: $\hat{\mathbf{y}} = \mathbf{X}\boldsymbol{\theta}_A = [1, 3, 5]^\top$
3. $\mathbf{y} - \hat{\mathbf{y}} = [0, 1, -1]^\top$, 제곱합은 $0 + 1 + 1 = 2$
4. $\frac{1}{3}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}_A\|^2 = \frac{2}{3}$
5. $\boldsymbol{\theta}_B$: $\hat{\mathbf{y}} = \mathbf{X}\boldsymbol{\theta}_B = [\tfrac{3}{2}, 3, \tfrac{9}{2}]^\top$
6. $\mathbf{y} - \hat{\mathbf{y}} = [-\tfrac{1}{2}, 1, -\tfrac{1}{2}]^\top$, 제곱합은 $\tfrac{1}{4} + 1 + \tfrac{1}{4} = \tfrac{3}{2}$
7. $\frac{1}{3}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}_B\|^2 = \frac{1}{2}$
8. $\frac{1}{2} \lt \frac{2}{3}$이니까 $\boldsymbol{\theta}_B$가 이 데이터에 더 잘 맞아요.
9. 수업과의 연결: 칠판에서 $\frac{1}{N}\sum_n (y_n - \boldsymbol{\theta}^\top \mathbf{x}_n)^2$을 $\frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$ 한 줄로 바꾼 "김밥 재료 손질"을 숫자로 해 본 거예요. 교수님이 "산수니까 해 보세요"라고 남긴 부분이에요 (0914 37:24).

**정답:** $\boldsymbol{\theta}_A$는 $\frac{2}{3}$, $\boldsymbol{\theta}_B$는 $\frac{1}{2}$이에요. $\boldsymbol{\theta}_B$가 더 작아요.

</details>

---

<a id="p3"></a>

### P3. λ에 따라 달라지는 정규화 최소제곱의 선택

학습 데이터가 $(x, y) = (0, 1), (1, 3), (2, 5)$예요. 입력 앞에 1을 붙여 $\mathbf{x}_n = [1, x_n]^\top$으로 쓰고, 예측기는 $\boldsymbol{\theta}^\top \mathbf{x}_n$이에요. 정규화된 문제의 목적함수는 다음과 같아요.

$$
J(\boldsymbol{\theta}) = \frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 + \lambda \|\boldsymbol{\theta}\|^2
$$

후보는 $\boldsymbol{\theta}_A = [1, 2]^\top$과 $\boldsymbol{\theta}_B = [1, 1]^\top$ 두 개예요.

- (a) $\lambda = 0$일 때 두 후보의 $J$를 구하고, 더 작은 쪽을 골라 보세요.
- (b) $\lambda = 1$일 때 두 후보의 $J$를 구하고, 더 작은 쪽을 골라 보세요.

<details><summary>교과서 원문 보기</summary>

"The regularization parameter trades off minimizing the loss on the training set and the magnitude of the parameters" — Example 8.3

</details>

<details><summary>힌트 보기</summary>

두 항을 따로 구해요. 앞은 제곱 손실의 평균, 뒤는 $\lambda$ 곱하기 원소 제곱합이에요.

</details>

<details><summary>풀이 보기</summary>

1. $\boldsymbol{\theta}_A$의 추정치는 $[1, 3, 5]^\top$이라 $\mathbf{y}$와 똑같아요. 그래서 $\frac{1}{3}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}_A\|^2 = 0$이에요.
2. $\boldsymbol{\theta}_B$의 추정치는 $[1, 2, 3]^\top$이고 잔차는 $[0, 1, 2]^\top$이에요. 그래서 $\frac{1}{3}(0 + 1 + 4) = \frac{5}{3}$이에요.
3. 파라미터 크기: $\|\boldsymbol{\theta}_A\|^2 = 1 + 4 = 5$, $\|\boldsymbol{\theta}_B\|^2 = 1 + 1 = 2$
4. (a) $\lambda = 0$: $J_A = 0$, $J_B = \frac{5}{3}$이라 $\boldsymbol{\theta}_A$를 골라요.
5. (b) $\lambda = 1$: $J_A = 0 + 5 = 5$, $J_B = \frac{5}{3} + 2 = \frac{11}{3}$이라 $\boldsymbol{\theta}_B$를 골라요.
6. 학습 데이터에 딱 맞는 $\boldsymbol{\theta}_A$도 크기가 크면 $\lambda \|\boldsymbol{\theta}\|^2$ 벌점을 받아 밀려나요.
7. 수업과의 연결: 교수님이 $\lambda = 0$이면 "딱 과적합되기 좋지"라고 하고, $\lambda = 1$처럼 양수를 주면 원점에서의 거리까지 따져 균형을 잡는다고 한 장면이에요 (0914 48:44–49:53).

**정답:** (a) $\lambda = 0$이면 $J_A = 0$, $J_B = \frac{5}{3}$ 이라 $\boldsymbol{\theta}_A$ (b) $\lambda = 1$이면 $J_A = 5$, $J_B = \frac{11}{3}$ 이라 $\boldsymbol{\theta}_B$

</details>

---

<a id="p4"></a>

### P4. 가우시안 우도의 평균과 분산 읽기

라벨에 평균 0인 가우시안 노이즈 $\varepsilon_n \sim \mathcal{N}(0, \sigma^2)$가 더해지고, 예측에는 선형 모델 $\mathbf{x}_n^\top \boldsymbol{\theta}$를 쓴다고 가정해요. 그러면 예제 하나의 우도는 $p(y_n \mid \mathbf{x}_n, \boldsymbol{\theta}) = \mathcal{N}(y_n \mid \mathbf{x}_n^\top \boldsymbol{\theta}, \sigma^2)$예요. 이제 $\mathbf{x}_n = [1, 2]^\top$, $\boldsymbol{\theta} = [1, 2]^\top$, $\sigma^2 = 1$이라고 해요. $y_n$의 조건부 분포의 평균과 분산을 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"we assume that we can explain our observation uncertainty by independent Gaussian noise ... with zero mean" — Example 8.4

</details>

<details><summary>힌트 보기</summary>

$\mathcal{N}(y_n \mid \mu, \sigma^2)$에서 첫 자리가 평균, 둘째 자리가 분산이에요. 평균 자리에는 $\mathbf{x}_n^\top \boldsymbol{\theta}$가 있어요.

</details>

<details><summary>풀이 보기</summary>

1. 평균: $\mathbf{x}_n^\top \boldsymbol{\theta} = 1 \cdot 1 + 2 \cdot 2 = 5$
2. 분산: 노이즈 분산이 그대로 남아서 $\sigma^2 = 1$이에요.
3. 그래서 $y_n \mid \mathbf{x}_n, \boldsymbol{\theta} \sim \mathcal{N}(5, 1)$이에요.
4. 수업과의 연결: 칠판에서 $y_n = \mathbf{x}_n^\top \boldsymbol{\theta} + w$로 suppose하고, 상수를 더하면 평균만 옮겨지고 분산은 그대로라서 $\mathcal{N}(\mathbf{x}_n^\top \boldsymbol{\theta}, \sigma^2)$가 된다고 한 부분이에요 (0914 65:40–69:39).

**정답:** 조건부 분포의 평균 $5$, 분산 $1$

</details>

---

<a id="p5"></a>

### P5. 음의 로그우도와 최소제곱의 순서 비교하기

데이터는 $(x, y) = (0, 1), (1, 4), (2, 4)$이고, 입력 앞에 1을 붙여 $\mathbf{x}_n = [1, x_n]^\top$으로 써요. 각 라벨은 $p(y_n \mid \mathbf{x}_n, \boldsymbol{\theta}) = \mathcal{N}(y_n \mid \mathbf{x}_n^\top \boldsymbol{\theta}, \sigma^2)$를 따르고 $\sigma^2 = 1$이에요. 예제들은 i.i.d.라고 가정해요.

- (a) 음의 로그우도 $\mathcal{L}(\boldsymbol{\theta}) = -\sum_{n=1}^{N} \log p(y_n \mid \mathbf{x}_n, \boldsymbol{\theta})$를 제곱합 항과 상수항으로 나눠 써 보세요.
- (b) $\boldsymbol{\theta}_A = [1, 2]^\top$과 $\boldsymbol{\theta}_B = [\tfrac{3}{2}, \tfrac{3}{2}]^\top$의 $\mathcal{L}$을 자연로그로 소수 셋째 자리까지 구해 보세요.
- (c) 어느 쪽의 $\mathcal{L}$이 더 작나요? 제곱 손실 합으로 비교한 순서와 같은가요?

<details><summary>교과서 원문 보기</summary>

"As $\sigma$ is given, the second term in (8.18d) is constant, and minimizing $\mathcal{L}(\boldsymbol{\theta})$ corresponds to solving the least-squares problem" — Example 8.5

</details>

<details><summary>힌트 보기</summary>

$\log$와 $\exp$가 서로 지워져요. $-\log\frac{1}{\sqrt{2\pi\sigma^2}} = \frac{1}{2}\log(2\pi\sigma^2)$이 $N$번 더해져요.

</details>

<details><summary>풀이 보기</summary>

1. $\mathcal{L}(\boldsymbol{\theta}) = -\sum_{n=1}^{N} \log \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(y_n - \mathbf{x}_n^\top \boldsymbol{\theta})^2}{2\sigma^2}\right)$
2. $= \frac{1}{2\sigma^2}\sum_{n=1}^{N} (y_n - \mathbf{x}_n^\top \boldsymbol{\theta})^2 + \frac{N}{2}\log(2\pi\sigma^2)$
3. 상수항: $N = 3$, $\sigma^2 = 1$이면 $\frac{3}{2}\log(2\pi) \approx 2.757$이에요. $\boldsymbol{\theta}$와 상관없어요.
4. $\boldsymbol{\theta}_A$: 추정치 $[1, 3, 5]^\top$, 잔차 $[0, 1, -1]^\top$, 제곱합 $2$라서 첫 항은 $\frac{2}{2} = 1$이에요.
5. $\mathcal{L}(\boldsymbol{\theta}_A) = 1 + \frac{3}{2}\log(2\pi) \approx 3.757$
6. $\boldsymbol{\theta}_B$: 추정치 $[\tfrac{3}{2}, 3, \tfrac{9}{2}]^\top$, 잔차 $[-\tfrac{1}{2}, 1, -\tfrac{1}{2}]^\top$, 제곱합 $\tfrac{3}{2}$라서 첫 항은 $\frac{3}{4}$이에요.
7. $\mathcal{L}(\boldsymbol{\theta}_B) = \frac{3}{4} + \frac{3}{2}\log(2\pi) \approx 3.507$
8. $\boldsymbol{\theta}_B$가 더 작아요. 상수항이 같으니 순서는 제곱합($2$ 대 $\tfrac{3}{2}$)이 정하고, 제곱 손실로 비교한 순서와 같아요.
9. 수업과의 연결: 칠판에서 $\frac{N}{2}\log(2\pi\sigma^2)$ 같은 상수항은 "무시하고" 넘어가고, 음의 로그우도 최소화가 최소제곱과 같은 해를 준다고 결론 낸 부분이에요 (0914 69:54–71:15).

**정답:** $\mathcal{L}(\boldsymbol{\theta}_A) = 1 + \frac{3}{2}\log(2\pi) \approx 3.757$, $\mathcal{L}(\boldsymbol{\theta}_B) = \frac{3}{4} + \frac{3}{2}\log(2\pi) \approx 3.507$이라 $\boldsymbol{\theta}_B$가 더 작고, 최소제곱으로 비교한 순서와 같아요.

</details>

---

<a id="partB"></a>

## B. 교과서 연습문제 (MML 3·6·7장)

<a id="p6"></a>

### P6. 두 벡터 사이의 유클리드 거리

두 벡터 $\mathbf{x} = [1, 2, 3]^\top$, $\mathbf{y} = [-1, -1, 0]^\top$이 있어요. 내적을 $\langle \mathbf{x}, \mathbf{y} \rangle := \mathbf{x}^\top \mathbf{y}$로 둘 때, 두 벡터 사이의 거리 $d(\mathbf{x}, \mathbf{y}) = \|\mathbf{x} - \mathbf{y}\|$를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"Compute the distance between $\mathbf{x}$ ... $\mathbf{y}$ ... using a. $\langle \mathbf{x}, \mathbf{y} \rangle := \mathbf{x}^\top \mathbf{y}$" — Exercise 3.3

</details>

<details><summary>힌트 보기</summary>

먼저 차이 벡터를 구해요. 그 벡터를 자기 자신과 내적한 뒤 제곱근을 씌워요.

</details>

<details><summary>풀이 보기</summary>

1. 차이 벡터: $\mathbf{x} - \mathbf{y} = [1 - (-1), 2 - (-1), 3 - 0]^\top = [2, 3, 3]^\top$
2. 자기 내적: $(\mathbf{x} - \mathbf{y})^\top(\mathbf{x} - \mathbf{y}) = 4 + 9 + 9 = 22$
3. $d(\mathbf{x}, \mathbf{y}) = \sqrt{22} \approx 4.690$
4. 수업과의 연결: 교수님이 2-노름 $\|\boldsymbol{\theta}\|_2$를 "원점에서의 거리"라고 설명했어요. 여기서는 원점 대신 $\mathbf{y}$에서 잰 거리예요 (0914 49:56).

**정답:** $d(\mathbf{x}, \mathbf{y}) = \sqrt{22} \approx 4.690$

</details>

---

<a id="p7"></a>

### P7. 삼차함수의 정상점과 종류

일변수 함수 $f(x) = x^3 + 6x^2 - 3x - 5$가 있어요. 정상점(stationary point)을 모두 찾고, 각각 극대인지 극소인지 안장점인지 판정해 보세요.

<details><summary>교과서 원문 보기</summary>

"Find its stationary points and indicate whether they are maximum, minimum, or saddle points." — Exercise 7.1

</details>

<details><summary>힌트 보기</summary>

$f'(x) = 0$인 점이 정상점이에요. 그 점에서 $f''(x)$의 부호를 보면 종류를 알 수 있어요.

</details>

<details><summary>풀이 보기</summary>

1. $f'(x) = 3x^2 + 12x - 3$
2. $f'(x) = 0 \Rightarrow x^2 + 4x - 1 = 0 \Rightarrow x = -2 \pm \sqrt{5}$
3. 정상점은 $x = -2 + \sqrt{5} \approx 0.236$과 $x = -2 - \sqrt{5} \approx -4.236$ 두 개예요.
4. $f''(x) = 6x + 12$
5. $x = -2 + \sqrt{5}$: $f'' = 6\sqrt{5} \gt 0$이라 극소예요.
6. $x = -2 - \sqrt{5}$: $f'' = -6\sqrt{5} \lt 0$이라 극대예요.
7. 함숫값: $x^2 = 1 - 4x$를 쓰면 $f(x) = -10x - 3$으로 줄어요.
8. 그래서 $f(-2 + \sqrt{5}) = 17 - 10\sqrt{5} \approx -5.36$, $f(-2 - \sqrt{5}) = 17 + 10\sqrt{5} \approx 39.36$이에요.
9. 수업과의 연결: 교수님은 $\boldsymbol{\theta}$를 하나씩 바꿔 보는 무식한 방법 대신 least squares 알고리즘과 pseudo-inverse 같은 체계적인 방법이 있다고 했어요. 그런 방법이 찾는 것도 이 문제처럼 목적함수가 가장 작아지는 점이에요 (0914 40:04–41:07).

**정답:** $x = -2 + \sqrt{5}$에서 극소($f = 17 - 10\sqrt{5} \approx -5.36$), $x = -2 - \sqrt{5}$에서 극대($f = 17 + 10\sqrt{5} \approx 39.36$)예요. 안장점은 없어요.

</details>

---

출처: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* (Cambridge University Press, 2020). 풀이는 자체 작성이며 수치는 Python으로 검증했습니다.
