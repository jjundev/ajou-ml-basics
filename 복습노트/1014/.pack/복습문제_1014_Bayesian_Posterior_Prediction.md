# 복습문제 2선 — 1014 수업 범위

교과서 본문 예제 변형 2개로 정규화와 가우시안의 계수 비교를 복습해요. 먼저 풀어 보고, 막히면 힌트를 열어 보세요.

> `복습문제_1014_Bayesian_Posterior_Prediction.html`를 마크다운으로 옮겼어요. 원문, 힌트, 풀이는 접혀 있어요. 먼저 풀어 보고 펼쳐 보세요.

**목차**

- [A. 교과서 예제 변형](#partA)
  - [P1. 확률의 합과 밀도의 넓이](#p1)
  - [P2. 이차식에서 가우시안을 알아봐요](#p2)

<a id="partA"></a>

## A. 교과서 예제 변형

<a id="p1"></a>

### P1. 확률의 합과 밀도의 넓이

이산 확률변수 $Z$는 $-1.1,0.3,1.5$의 세 상태에서 같은 확률을 가져요. 연속 확률변수 $X$는 $0.9\le X\le1.6$에서 균일하며, 구간 밖 밀도는 0이에요.

- (a) $Z$의 세 상태별 확률을 표로 나타내 보세요.
- (b) $X$의 일정한 밀도 높이를 구하고, 전체 적분이 1인지 확인해 보세요.

<details><summary>교과서 원문 보기</summary>

“This example illustrates some differences between discrete and continuous probability distributions.” — Example 6.3 (책 182–183쪽)

</details>

<details><summary>힌트 보기</summary>

세 상태의 확률 합은 1이에요. 일정한 밀도를 적분하면 직사각형의 넓이가 돼요.

</details>

<details><summary>풀이 보기</summary>

1. (a) 세 상태의 확률을 $q$라고 두면 $3q=1$이므로 $q=\frac{1}{3}$이에요.

   | 상태 | 확률 |
   |---|---|
   | $-1.1$ | $\frac{1}{3}$ |
   | $0.3$ | $\frac{1}{3}$ |
   | $1.5$ | $\frac{1}{3}$ |
2. (b) 밀도 높이를 $h$라 두면 $h(1.6-0.9)=1$이에요. 따라서 $h=\frac{10}{7}$이에요.
3. 구간 전체를 적분하면 $\int_{0.9}^{1.6}\frac{10}{7}\,dx=\frac{10}{7}\cdot\frac{7}{10}=1$이에요. 밀도 높이는 1을 넘을 수 있어도 전체 넓이는 1이에요.

**정답:** (a) 각 상태 $\frac{1}{3}$, (b) 구간 안 밀도 $\frac{10}{7}$, 전체 적분 1이에요.

</details>

---

<a id="p2"></a>

### P2. 이차식에서 가우시안을 알아봐요

$\sigma^2\gt0$이고, $\phi(x)=\begin{bmatrix}x\\x^2\end{bmatrix}$예요. 두 계수를 모은 벡터를 다음처럼 정해요.

$$
\theta=\begin{bmatrix}\frac{\mu}{\sigma^2}\\-\frac{1}{2\sigma^2}\end{bmatrix}
$$

함수 $p(x\mid\theta)$는 $\exp(\theta_1x+\theta_2x^2)$에 비례해요.

계수를 대입하고 완전제곱하여, 정규화한 분포가 $\mathcal N(\mu,\sigma^2)$임을 확인해 보세요.

<details><summary>교과서 원문 보기</summary>

“Setting” the parameter vector “and substituting into (6.109), we obtain” the Gaussian form. — Example 6.13 (책 212쪽)

</details>

<details><summary>힌트 보기</summary>

$x^2-2\mu x=(x-\mu)^2-\mu^2$를 써요. $x$와 무관한 항은 정규화 상수에 흡수해요.

</details>

<details><summary>풀이 보기</summary>

1. 계수 $\theta_1=\frac{\mu}{\sigma^2}$, $\theta_2=-\frac{1}{2\sigma^2}$를 넣어요.

   $$
   p(x\mid\theta)\propto\exp\left(\frac{\mu x}{\sigma^2}-\frac{x^2}{2\sigma^2}\right)
   $$
2. 지수부를 완전제곱해요.

   $$
   \frac{\mu x}{\sigma^2}-\frac{x^2}{2\sigma^2}=-\frac{(x-\mu)^2}{2\sigma^2}+\frac{\mu^2}{2\sigma^2}
   $$
3. 마지막 항은 $x$와 무관해요. 따라서 원래 함수는 $\exp[-(x-\mu)^2/(2\sigma^2)]$에 비례해요. 이 종 모양의 적분은 $\sqrt{2\pi\sigma^2}$이므로 그 값으로 나눠요.
4. 정규화된 밀도는 다음과 같아요.

   $$
   p(x\mid\theta)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
   $$

**정답:** 정규화하면 평균 $\mu$, 분산 $\sigma^2$인 가우시안 분포가 돼요.

</details>

---

출처: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* (2020). 풀이는 자체 작성이며 수치는 Python으로 검증했습니다. 기존 팩과 출처 중복 및 수업 밖 문제를 제외하여 2문항을 실었어요. BLR 종합 예제는 이전 팩 링크로 이어져요.
