# 복습문제 10선 — 0909~0916 수업 범위

수업 범위인 MML 8장에는 연습문제가 없어서, **8장 본문 예제(Example 8.1~8.6)를 문제로 바꾼 5문항**과 **수업 내용으로 풀 수 있는 6·7장 연습문제 5문항**을 골랐습니다. 먼저 스스로 풀고, 막히면 💡 힌트, 그다음 ✅ 풀이를 여세요.

> 이 문서는 `복습문제_0909-0916_When_Models_Meet_Data.html`의 마크다운 버전입니다. 📖 원문 · 💡 힌트 · ✅ 풀이는 접혀 있으니 먼저 스스로 풀어 본 뒤 펼치세요.

**목차**

- [A. 교과서 본문 예제 (MML 8장)](#partA)
  - [P1. bias를 내적 안으로 넣기](#p1)
  - [P2. ERM을 행렬 한 줄로](#p2)
  - [P3. λ를 0부터 무한대까지](#p3)
  - [P4. 가우시안 NLL을 펼치면 least squares](#p4)
  - [P5. prior가 곧 정규화](#p5)
- [B. 교과서 연습문제 (MML 6·7장)](#partB)
  - [P6. 결합분포 표에서 주변·조건부 구하기](#p6)
  - [P7. 망고는 어느 가방에서 왔을까 (Bayes)](#p7)
  - [P8. 베타-베르누이: 수업의 동전 완성하기](#p8)
  - [P9. 상수 + 가우시안 노이즈의 likelihood](#p9)
  - [P10. 미분해서 0: argmin 찾는 도구 연습](#p10)

<a id="partA"></a>

## A. 교과서 본문 예제 (MML 8장)

<a id="p1"></a>

### P1. bias를 내적 안으로 넣기

**MML Example 8.1 · ★ · 📅 0914**

D개의 특징을 가진 데이터에 대한 affine 예측기 $f(\mathbf{x}_n) = \theta_0 + \sum_{d=1}^{D} \theta_d x_n^{(d)}$를 생각하자.

- (a) 이 식을 내적 하나 $\boldsymbol{\theta}^\top \mathbf{x}_n$으로 쓰려면 $\mathbf{x}_n$과 $\boldsymbol{\theta}$를 어떻게 다시 정의해야 하는가?
- (b) 그때 두 벡터의 차원과 $f$의 정의역·공역은?
- (c) 이 함수를 linear가 아니라 affine이라고 부르는 이유는?

<details><summary>📖 교과서 원문</summary>

"We choose a more compact notation for an affine function by concatenating an additional unit feature $x^{(0)} = 1$ to $\mathbf{x}_n$ … (8.4) … (8.5)" — Example 8.1

</details>

<details><summary>💡 힌트</summary>

$\theta_0 = 1 \cdot \theta_0$이다. 숫자 1을 데이터 쪽에 붙여 보자.

</details>

<details><summary>✅ 풀이</summary>

1. $\mathbf{x}_n = [1, x_n^{(1)}, \dots, x_n^{(D)}]^\top$, $\boldsymbol{\theta} = [\theta_0, \theta_1, \dots, \theta_D]^\top$
2. $\boldsymbol{\theta}^\top \mathbf{x}_n = \theta_0 \cdot 1 + \sum_{d=1}^{D} \theta_d x_n^{(d)}$로 원래 식과 같다.
3. 두 벡터는 모두 $\mathbb{R}^{D+1}$에 속하고, $f: \mathbb{R}^{D+1} \to \mathbb{R}$이다(누운 벡터와 선 벡터의 내적은 스칼라).
4. $f(\mathbf{0}) = \theta_0$이라 일반적으로 원점을 지나지 않는다. 그래서 affine이다.

**✅ 정답:** 앞에 1과 $\theta_0$를 붙인다. 둘 다 $\mathbb{R}^{D+1}$이다. 원점을 지나지 않을 수 있어서 affine이다.

</details>

🔗 수업과 연결: [가장 중요한 수식: affine 모델과 augmentation](정리노트_0909-0916_When_Models_Meet_Data.md#s2-affine) — 이 카드는 그 augmentation 트릭을 직접 손으로 검산한다.

- [ ] 풀었음

---

<a id="p2"></a>

### P2. ERM을 행렬 한 줄로

**MML Example 8.2 · ★ · 📅 0914**

학습 데이터 $\{(\mathbf{x}_n, y_n)\}_{n=1}^{N}$($\mathbf{x}_n$은 P1처럼 1이 붙은 $\mathbb{R}^{D+1}$ 벡터), 선형 예측기 $\hat{y}_n = \boldsymbol{\theta}^\top \mathbf{x}_n$, squared loss가 주어졌다.

- (a) empirical risk를 합(Σ) 꼴로 쓰시오.
- (b) $\mathbf{X} := [\mathbf{x}_1, \dots, \mathbf{x}_N]^\top$, $\mathbf{y} := [y_1, \dots, y_N]^\top$로 두면 (a)가 $\frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$과 같음을 보이시오.
- (c) $\mathbf{X}$와 $\mathbf{X}\boldsymbol{\theta}$의 크기는?

<details><summary>📖 교과서 원문</summary>

Example 8.2, 식 (8.7)–(8.9) "…This equation can be equivalently expressed in matrix form…"

</details>

<details><summary>💡 힌트</summary>

벡터 $\mathbf{y} - \mathbf{X}\boldsymbol{\theta}$의 n번째 원소를 먼저 적어 보자. 유클리드 노름의 제곱은 원소 제곱의 합이다.

</details>

<details><summary>✅ 풀이</summary>

1. $R_{\text{emp}} = \frac{1}{N}\sum_{n=1}^{N}(y_n - \boldsymbol{\theta}^\top \mathbf{x}_n)^2$
2. $\mathbf{X}$의 n번째 행은 $\mathbf{x}_n^\top$이므로 $(\mathbf{X}\boldsymbol{\theta})_n = \mathbf{x}_n^\top \boldsymbol{\theta}$이다.
3. $(\mathbf{y} - \mathbf{X}\boldsymbol{\theta})_n = y_n - \mathbf{x}_n^\top \boldsymbol{\theta}$
4. $\|\mathbf{v}\|^2 = \sum_n v_n^2$이므로 (a)와 같다.
5. $\mathbf{X} \in \mathbb{R}^{N \times (D+1)}$, $\mathbf{X}\boldsymbol{\theta} = \hat{\mathbf{y}} \in \mathbb{R}^{N}$

**✅ 정답:** $\frac{1}{N}\sum_{n}(y_n - \boldsymbol{\theta}^\top \mathbf{x}_n)^2 = \frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$, $\mathbf{X} \in \mathbb{R}^{N \times (D+1)}$

</details>

🔗 수업과 연결: [데이터 행렬과 squared loss (김밥 말기)](정리노트_0909-0916_When_Models_Meet_Data.md#s2-matrix) — 그 "김밥 말기" 비유를 식으로 다시 확인한다.

- [ ] 풀었음

---

<a id="p3"></a>

### P3. λ를 0부터 무한대까지

**MML Example 8.3 · ★★ · 📅 0914**

$$
\min_{\boldsymbol{\theta}} \frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 + \lambda\|\boldsymbol{\theta}\|^2
$$

에 대해 답하시오.

- (a) $\lambda = 0$이면 어떤 문제가 되는가?
- (b) $\lambda \to \infty$이면 해는 어디로 가는가?
- (c) λ는 학습 파라미터인가, hyperparameter인가?
- (d) [도전] gradient를 0으로 두어 해를 구하시오.

<details><summary>📖 교과서 원문</summary>

Example 8.3, 식 (8.12) "The additional term $\|\boldsymbol{\theta}\|^2$ is called the regularizer…"

</details>

<details><summary>💡 힌트</summary>

(b) 두 번째 항이 첫 번째 항을 압도하면 어떻게 될까?<br> (d) $\nabla_{\boldsymbol{\theta}}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 = -2\mathbf{X}^\top(\mathbf{y} - \mathbf{X}\boldsymbol{\theta})$, $\nabla_{\boldsymbol{\theta}}\|\boldsymbol{\theta}\|^2 = 2\boldsymbol{\theta}$

</details>

<details><summary>✅ 풀이</summary>

- (a) $\lambda = 0$이면 보통의 least squares(ERM만)가 된다. 과적합 위험이 있다("딱 과적합되기 좋지").
- (b) $\lambda \to \infty$이면 벌점이 지배해서 $\boldsymbol{\theta} \to \mathbf{0}$(원점)이 된다. 너무 단순해져 과소적합이다(위젯: 차수 9, λ=10).
- (c) hyperparameter다. 학습 전에 사람이 정한다.
- (d) $-\frac{2}{N}\mathbf{X}^\top(\mathbf{y} - \mathbf{X}\boldsymbol{\theta}) + 2\lambda\boldsymbol{\theta} = \mathbf{0}$ ⇒ $(\mathbf{X}^\top \mathbf{X} + N\lambda \mathbf{I})\boldsymbol{\theta} = \mathbf{X}^\top \mathbf{y}$. 다음 주 Linear Regression에서 정식으로 다룬다.

**✅ 정답:** (a) 과적합 위험, (b) $\boldsymbol{\theta} \to \mathbf{0}$, (c) hyperparameter, (d) $\boldsymbol{\theta} = (\mathbf{X}^\top \mathbf{X} + N\lambda \mathbf{I})^{-1}\mathbf{X}^\top \mathbf{y}$

</details>

🔗 수업과 연결: [Overfitting과 Regularization](정리노트_0909-0916_When_Models_Meet_Data.md#s2-reg) — λ가 커질수록 원점으로 끌려가는 그 위젯과 같은 이야기다.

- [ ] 풀었음

---

<a id="p4"></a>

### P4. 가우시안 NLL을 펼치면 least squares

**MML Example 8.5 · ★★ · 📅 0914·0916**

각 라벨이 $p(y_n \mid \mathbf{x}_n, \boldsymbol{\theta}) = \mathcal{N}(y_n \mid \mathbf{x}_n^\top \boldsymbol{\theta}, \sigma^2)$를 따르고 데이터는 i.i.d.라고 하자(σ는 알려진 상수).

- (a) 전체 likelihood를 곱으로 쓰고, 왜 곱이 되는지 설명하시오.
- (b) negative log-likelihood를 전개하시오.
- (c) 그 최소화가 least squares와 같은 이유를 쓰시오.

<details><summary>📖 교과서 원문</summary>

Example 8.4 (8.15)와 Example 8.5 (8.18a–d) "…minimizing $\mathcal{L}(\boldsymbol{\theta})$ corresponds to solving the least-squares problem…"

</details>

<details><summary>💡 힌트</summary>

log는 곱을 합으로 바꾸고 exp를 없앤다. θ와 무관한 항은 argmin에 영향이 없다.

</details>

<details><summary>✅ 풀이</summary>

1. independent이면 곱, identical이면 θ가 하나다: $p(\mathcal{Y} \mid \mathcal{X}, \boldsymbol{\theta}) = \prod_{n=1}^{N} \mathcal{N}(y_n \mid \mathbf{x}_n^\top \boldsymbol{\theta}, \sigma^2)$
2. $\mathcal{L} = -\sum_{n} \log\Big[\frac{1}{\sqrt{2\pi\sigma^2}} \exp\big(-\frac{(y_n - \mathbf{x}_n^\top \boldsymbol{\theta})^2}{2\sigma^2}\big)\Big]$
3. $\mathcal{L}(\boldsymbol{\theta}) = \frac{N}{2}\log(2\pi\sigma^2) + \frac{1}{2\sigma^2}\sum_{n=1}^{N}(y_n - \mathbf{x}_n^\top \boldsymbol{\theta})^2$
4. 첫째 항은 상수이고, 둘째 항은 양수 × $\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$이다. 따라서 argmin이 least squares와 같다.

**✅ 정답:** 상수 + $\frac{1}{2\sigma^2}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$ → least squares와 같은 해

</details>

🔗 수업과 연결: [가우시안 노이즈면 MLE = Least Squares](정리노트_0909-0916_When_Models_Meet_Data.md#s3-mle-ls) — 그 전개를 처음부터 끝까지 손으로 다시 밟는다.

- [ ] 풀었음

---

<a id="p5"></a>

### P5. prior가 곧 정규화

**MML Example 8.6 · ★★★ 도전 · 📅 0916 · 📎 보충 · 수업 미유도**

P4에 prior $p(\boldsymbol{\theta}) = \mathcal{N}(\mathbf{0}, b^2\mathbf{I})$를 더한다. 교과서는 일반 공분산 $\boldsymbol{\Sigma}$를 쓰지만, 여기서는 $\boldsymbol{\Sigma} = b^2\mathbf{I}$로 단순화한 변형이다.

- (a) $-\log p(\boldsymbol{\theta})$를 구하시오.
- (b) MAP 목적함수를 쓰시오.
- (c) P3의 정규화 LS와 같은 해를 주는 λ를 구하시오.

<details><summary>📖 교과서 원문</summary>

Example 8.6 "…we assume that the parameter vector is distributed as a multivariate Gaussian with zero mean, i.e., $p(\boldsymbol{\theta}) = \mathcal{N}(\mathbf{0}, \boldsymbol{\Sigma})$…"

</details>

<details><summary>💡 힌트</summary>

$\mathcal{N}(\mathbf{0}, b^2\mathbf{I})$의 밀도는 $\exp\big(-\frac{1}{2b^2}\|\boldsymbol{\theta}\|^2\big)$에 비례한다. 목적함수에 양수를 곱해도 argmin은 그대로다.

</details>

<details><summary>✅ 풀이</summary>

1. $-\log p(\boldsymbol{\theta}) = \frac{1}{2b^2}\|\boldsymbol{\theta}\|^2 + \text{const}$
2. $\boldsymbol{\theta}_{\text{MAP}} = \arg\min_{\boldsymbol{\theta}} \Big[\frac{1}{2\sigma^2}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 + \frac{1}{2b^2}\|\boldsymbol{\theta}\|^2\Big]$
3. $\frac{2\sigma^2}{N}$를 곱하면 $\frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 + \frac{\sigma^2}{N b^2}\|\boldsymbol{\theta}\|^2$
4. 해석: b가 작을수록("θ는 작다"는 믿음이 강할수록) λ가 커진다.

**✅ 정답:** $\lambda = \frac{\sigma^2}{N b^2}$

</details>

🔗 수업과 연결: [📎 가우시안 prior = L2 정규화](정리노트_0909-0916_When_Models_Meet_Data.md#s3-map-l2) — 수업에서 미룬 이 유도를 직접 끝까지 전개한다.

- [ ] 풀었음

---

<a id="partB"></a>

## B. 교과서 연습문제 (MML 6·7장)

<a id="p6"></a>

### P6. 결합분포 표에서 주변·조건부 구하기

**MML Exercise 6.1 · ★ · 📅 0916**

두 이산 확률변수 X, Y의 결합분포 $p(x, y)$가 아래 표와 같다.

|   | x1 | x2 | x3 | x4 | x5 |
|---|---|---|---|---|---|
| y1 | 0.01 | 0.02 | 0.03 | 0.1 | 0.1 |
| y2 | 0.05 | 0.1 | 0.05 | 0.07 | 0.2 |
| y3 | 0.1 | 0.05 | 0.03 | 0.05 | 0.04 |

- (a) 주변분포 p(x), p(y)를 구하시오.
- (b) 조건부분포 $p(x \mid Y = y_1)$, $p(y \mid X = x_3)$를 구하시오.

<details><summary>📖 교과서 원문</summary>

"Consider the following bivariate distribution p(x, y) of two discrete random variables X and Y. … Compute: a. The marginal distributions p(x) and p(y). b. The conditional distributions p(x|Y = y1) and p(y|X = x3)." — Exercise 6.1

</details>

<details><summary>💡 힌트</summary>

주변화는 관심 없는 변수로 더하는 것이다. 연속이면 적분이며, 수업 식 $p(\mathbf{x}) = \int p(\mathbf{x}, \boldsymbol{\theta})\, d\boldsymbol{\theta}$와 같다. 조건부 = 결합 ÷ 주변.

</details>

<details><summary>✅ 풀이</summary>

1. p(x)는 열 합: (0.16, 0.17, 0.11, 0.22, 0.34). 합이 1인지 확인한다.
2. p(y)는 행 합: (0.26, 0.47, 0.27)
3. $p(x \mid y_1) = \frac{p(x, y_1)}{0.26} = \big(\frac{1}{26}, \frac{1}{13}, \frac{3}{26}, \frac{5}{13}, \frac{5}{13}\big)$
4. $p(y \mid x_3) = \frac{p(x_3, y)}{0.11} = \big(\frac{3}{11}, \frac{5}{11}, \frac{3}{11}\big)$

**✅ 정답:** p(x) = (0.16, 0.17, 0.11, 0.22, 0.34), p(y) = (0.26, 0.47, 0.27), $p(x \mid y_1) = \big(\frac{1}{26}, \frac{1}{13}, \frac{3}{26}, \frac{5}{13}, \frac{5}{13}\big)$, $p(y \mid x_3) = \big(\frac{3}{11}, \frac{5}{11}, \frac{3}{11}\big)$

</details>

🔗 수업과 연결: [Joint · Marginal · Latent](정리노트_0909-0916_When_Models_Meet_Data.md#s4-joint) — 수업에서 배운 marginal의 정의를 표 위에서 직접 계산해 본다.

- [ ] 풀었음

---

<a id="p7"></a>

### P7. 망고는 어느 가방에서 왔을까 (Bayes)

**MML Exercise 6.4 · ★ · 📅 0916**

가방 1에는 망고 4개와 사과 2개, 가방 2에는 망고 4개와 사과 4개가 있다. 앞면 확률이 0.6인 동전을 던져 앞면이면 가방 1, 뒷면이면 가방 2에서 과일을 하나 꺼낸다. 친구가(결과를 숨긴 채) 망고를 보여 줬다. 이 망고가 가방 2에서 나왔을 확률은?

<details><summary>📖 교과서 원문</summary>

"There are two bags. The first bag contains four mangos and two apples; … What is the probability that the mango was picked from bag 2? Hint: Use Bayes' theorem." — Exercise 6.4

</details>

<details><summary>💡 힌트</summary>

prior는 가방 선택 확률(0.6, 0.4), likelihood는 각 가방에서 망고가 나올 확률이다.

</details>

<details><summary>✅ 풀이</summary>

1. prior: P(bag1) = 0.6, P(bag2) = 0.4
2. likelihood: P(M | bag1) = 4/6 = 2/3, P(M | bag2) = 4/8 = 1/2
3. evidence(marginal likelihood): P(M) = 0.6·2/3 + 0.4·1/2 = 0.4 + 0.2 = 0.6
4. $$
   P(\text{bag2} \mid M) = \frac{0.4 \cdot \frac{1}{2}}{0.6} = \frac{1}{3}
   $$
5. 해석: prior 0.4가 posterior 1/3으로 줄었다. 망고는 가방 1에서 더 잘 나오기 때문이다. 참고로 ML(likelihood만)로도, MAP로도 가방 1을 고른다.

**✅ 정답:** $\frac{1}{3}$

</details>

🔗 수업과 연결: [MAP: 데이터 + 선입견(prior)](정리노트_0909-0916_When_Models_Meet_Data.md#s3-map) — prior와 likelihood를 곱해 posterior를 얻는 Bayes' theorem을 그대로 적용한다.

- [ ] 풀었음

---

<a id="p8"></a>

### P8. 베타-베르누이: 수업의 동전 완성하기

**MML Exercise 6.3 · ★★ · 📅 0916 · 📎 보충 · 수업 미유도**

(a) 원문 문제: Bernoulli likelihood $p(x \mid \mu) = \mu^x(1-\mu)^{1-x}$에 대한 켤레 사전분포를 고르고, 사후분포 $p(\mu \mid x_1, \dots, x_N)$를 구하시오.

[변형: 0916 수업의 동전] $x = 1$을 앞면이라 하고, 10번 던져 앞면이 2번 나왔다($\mu$는 수업의 θ와 같다).

- (b) $\mu_{\text{ML}}$을 미분으로 구하시오.
- (c) prior가 Beta(4, 4)일 때 $\mu_{\text{MAP}}$은?
- (d) prior가 Beta(1, 1)(uniform)이면?
- (e) Fully Bayesian으로 다음 던짐이 앞면일 확률은?

<details><summary>📖 교과서 원문</summary>

"You have written a computer program that sometimes compiles and sometimes not … Choose a conjugate prior for the Bernoulli likelihood and compute the posterior distribution $p(\mu \mid x_1, \dots, x_N)$." — Exercise 6.3

</details>

<details><summary>💡 힌트</summary>

Beta 밀도는 $\mu^{\alpha-1}(1-\mu)^{\beta-1}$에 비례한다. 곱해 보면 같은 모양이 나온다.<br> Beta(α, β)의 최빈값은 $\frac{\alpha - 1}{\alpha + \beta - 2}$, 평균은 $\frac{\alpha}{\alpha + \beta}$다(평균: 확률 추가강의 Lecture 10, 최빈값·MAP: Lecture 11).

</details>

<details><summary>✅ 풀이</summary>

1. likelihood: $\prod_n \mu^{x_n}(1-\mu)^{1-x_n} = \mu^{k}(1-\mu)^{N-k}$, 단 $k = \sum_n x_n$
2. prior Beta(α, β)와 곱하면 $\mu^{k+\alpha-1}(1-\mu)^{N-k+\beta-1}$ ⇒ 사후분포 $\mathrm{Beta}(\alpha + k, \beta + N - k)$. prior와 같은 가족이 되므로 켤레(conjugate)다.
3. (b) $\ell(\mu) = 2\log\mu + 8\log(1-\mu)$, $\frac{2}{\mu} - \frac{8}{1-\mu} = 0$ ⇒ $\mu_{\text{ML}} = 0.2$
4. (c) 사후분포 Beta(6, 12)의 최빈값: $\frac{5}{16} = 0.3125$. 교수님이 말한 "0.3 정도"와 맞는 값이다 (Beta(4,4)는 예시로 고른 prior).
5. (d) 사후분포 Beta(3, 9)의 최빈값: $\frac{2}{10} = 0.2$ = ML. uniform prior이면 MAP = ML이다.
6. (e) $P(x_{\text{new}} = 1 \mid \text{data}) = \int \mu\, p(\mu \mid \text{data})\, d\mu = \frac{6}{18} = \frac{1}{3}$. 이것이 posterior predictive이며 정리노트의 동전 위젯 기본값과 같다.

**✅ 정답:** (a) $\mathrm{Beta}(\alpha + k, \beta + N - k)$, (b) 0.2, (c) 0.3125, (d) 0.2, (e) $\frac{1}{3}$

</details>

🔗 수업과 연결: [동전으로 보는 세 가지 답](정리노트_0909-0916_When_Models_Meet_Data.md#s4-coin) — 수업 동전 예제(N=10, k=2)를 Beta prior로 일반화해서 ML·MAP·predictive를 모두 다시 구한다.

- [ ] 풀었음

---

<a id="p9"></a>

### P9. 상수 + 가우시안 노이즈의 likelihood

**MML Exercise 6.12 · ★ · 📅 0916**

$\mathbf{x} \sim \mathcal{N}(\boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$이고 $\mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{b} + \mathbf{w}$, $\mathbf{w} \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})$이며 x와 w는 독립이다.

- (a) likelihood $p(\mathbf{y} \mid \mathbf{x})$를 쓰시오.

원문의 (b)~(d)는 가우시안 주변화·조건화 규칙이 필요해서 이번 수업 범위 밖이다.

<details><summary>📖 교과서 원문</summary>

"Consider a Gaussian random variable $\mathbf{x} \sim \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$ … a. Write down the likelihood $p(\mathbf{y} \mid \mathbf{x})$." — Exercise 6.12

</details>

<details><summary>💡 힌트</summary>

x가 주어지면 $\mathbf{A}\mathbf{x} + \mathbf{b}$는 상수다. 수업의 $c_n = \mathbf{x}_n^\top \boldsymbol{\theta}$와 같은 역할이다.

</details>

<details><summary>✅ 풀이</summary>

1. 조건부에서 $\mathbf{A}\mathbf{x} + \mathbf{b}$는 상수다.
2. 상수 + 가우시안이면 평균만 이동하고 공분산은 그대로다.
3. $$
   p(\mathbf{y} \mid \mathbf{x}) = \mathcal{N}\big(\mathbf{y} \mid \mathbf{A}\mathbf{x} + \mathbf{b}, \mathbf{Q}\big)
   $$
4. 1차원 버전이 바로 수업의 $y_n \mid \mathbf{x}_n, \boldsymbol{\theta} \sim \mathcal{N}(\mathbf{x}_n^\top \boldsymbol{\theta}, \sigma^2)$이다.

**✅ 정답:** $p(\mathbf{y} \mid \mathbf{x}) = \mathcal{N}\big(\mathbf{y} \mid \mathbf{A}\mathbf{x} + \mathbf{b}, \mathbf{Q}\big)$

</details>

🔗 수업과 연결: [Generative process: 데이터는 이렇게 만들어졌을 거야](정리노트_0909-0916_When_Models_Meet_Data.md#s4-generative) — "상수 + 노이즈 = 평균만 이동한 가우시안"이라는 같은 아이디어를 벡터로 확장한다.

- [ ] 풀었음

---

<a id="p10"></a>

### P10. 미분해서 0: argmin 찾는 도구 연습

**MML Exercise 7.1 · ★ · 📅 0916**

$f(x) = x^3 + 6x^2 - 3x - 5$의 정상점(stationary point)을 구하고, 각각 최대·최소·안장점 중 무엇인지 판정하시오.

<details><summary>📖 교과서 원문</summary>

"Consider the univariate function $f(x) = x^3 + 6x^2 - 3x - 5$. Find its stationary points and indicate whether they are maximum, minimum, or saddle points." — Exercise 7.1

</details>

<details><summary>💡 힌트</summary>

$f'(x) = 0$으로 후보를 찾고, $f''$의 부호로 판정한다.

</details>

<details><summary>✅ 풀이</summary>

1. $f'(x) = 3x^2 + 12x - 3 = 0 \iff x^2 + 4x - 1 = 0$
2. 근의 공식으로 $x = -2 + \sqrt{5}$(≈ 0.236) 또는 $x = -2 - \sqrt{5}$(≈ −4.236)
3. $f''(x) = 6x + 12$
4. $x = -2 + \sqrt{5}$에서 $f'' = 6\sqrt{5} \gt 0$이므로 극소, $x = -2 - \sqrt{5}$에서 $f'' = -6\sqrt{5} \lt 0$이므로 극대. 안장점은 없다.
5. 수업과의 연결: MLE·ERM의 argmin도 "미분해서 0"으로 찾는다(0916 동전: "미분해 보면 나오거든요"). 2계 도함수는 그 점이 정말 최소인지 확인하는 도구다.

**✅ 정답:** 극소 $x = -2 + \sqrt{5}$, 극대 $x = -2 - \sqrt{5}$

</details>

🔗 수업과 연결: [동전으로 보는 세 가지 답](정리노트_0909-0916_When_Models_Meet_Data.md#s4-coin) — $\mu_{\text{ML}}$을 미분해서 0으로 두어 구하던 그 방법을 3차함수에 그대로 적용한다.

- [ ] 풀었음

---

출처: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* (Cambridge University Press, 2020). 풀이는 자체 작성이며 `scripts/review_answers.py`로 수치를 검증했습니다.
