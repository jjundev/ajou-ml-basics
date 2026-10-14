# 복습문제 6선 — 0916 수업 범위

교과서 본문 예제(Example 8.6) **1문항**과 6장 연습문제 **5문항**(6.1을 네 장으로 나눔, 6.3)으로 구성했어요. 먼저 풀어 보고, 막히면 힌트를 열어 보세요.

> `복습문제_0916_MAP_and_Generative_Models.html`를 마크다운으로 옮겼어요. 원문, 힌트, 풀이는 접혀 있어요. 먼저 풀어 보고 펼쳐 보세요.

**목차**

- [A. 교과서 본문 예제 (MML 8장)](#partA)
  - [P1. 가우시안 prior를 더한 MAP 목적함수](#p1)
- [B. 교과서 연습문제 (MML 6장)](#partB)
  - [P2. Joint 표에서 p(x) 구하기](#p2)
  - [P3. Joint 표에서 p(y) 구하기](#p3)
  - [P4. 조건부 분포 p(x | Y = y1)](#p4)
  - [P5. 조건부 분포 p(y | X = x3)](#p5)
  - [P6. 컴파일 성공률의 posterior](#p6)

<a id="partA"></a>

## A. 교과서 본문 예제 (MML 8장)

<a id="p1"></a>

### P1. 가우시안 prior를 더한 MAP 목적함수

Example 8.5처럼 가우시안 likelihood $p(y\mid X,\theta)$로 회귀를 하고 있어요. 여기에 파라미터 벡터 $\theta\in\mathbb{R}^D$가 평균 0인 다변량 가우시안을 따른다고 더 가정해요: $p(\theta)=\mathcal{N}(0,\Sigma)=\frac{1}{(2\pi)^{D/2}|\Sigma|^{1/2}}\exp\!\left(-\frac{1}{2}\theta^\top\Sigma^{-1}\theta\right)$ ($\Sigma$는 공분산 행렬).

- (a) $-\log p(\theta)$를 $\theta$에 대한 항과 상수로 나눠 써 보세요.
- (b) $\theta_{\text{MAP}}$를 찾을 때 최소화하는 목적함수를 음의 로그우도와 (a)의 결과로 써 보세요.

<details><summary>교과서 원문 보기</summary>

"we assume that the parameter vector is distributed as a multivariate Gaussian with zero mean, i.e., p(θ) = N(0, Σ)" — Example 8.6

</details>

<details><summary>힌트 보기</summary>

$\log$는 곱을 합으로, $\exp$를 지수로 풀어 줘요. $\theta$가 안 들어간 앞쪽 계수는 최적화에 상관없는 상수예요.

</details>

<details><summary>풀이 보기</summary>

1. $-\log p(\theta) = \frac{D}{2}\log(2\pi)+\frac{1}{2}\log|\Sigma| + \frac{1}{2}\theta^\top\Sigma^{-1}\theta$예요. $\log(ab)=\log a+\log b$와 $-\log\exp(u)=-u$를 썼어요.
2. 앞의 두 항은 $\theta$와 무관하니 상수로 묶어요: $-\log p(\theta)=\frac{1}{2}\theta^\top\Sigma^{-1}\theta+\text{상수}$.
3. posterior는 $p(\theta\mid X,y)\propto p(y\mid X,\theta)\,p(\theta)$이고, $-\log$를 치면 곱이 합이 돼요.
4. 그래서 $\theta_{\text{MAP}}=\arg\min_\theta\big[-\log p(y\mid X,\theta)-\log p(\theta)\big]=\arg\min_\theta\big[-\log p(y\mid X,\theta)+\frac{1}{2}\theta^\top\Sigma^{-1}\theta\big]$예요.
5. 수업과의 연결: 0916 수업의 $\theta_{\text{MAP}}=\arg\min_\theta\big[-\log P(x\mid\theta)-\log P(\theta)\big]$, 즉 "MAP = MLE + log prior"에 가우시안 prior를 넣어 본 거예요.

**정답:** (a) $-\log p(\theta)=\frac{1}{2}\theta^\top\Sigma^{-1}\theta+\text{상수}$, (b) 음의 로그우도에 $-\log p(\theta)$를 더한 $-\log p(y\mid X,\theta)-\log p(\theta)$를 최소화해 $\theta_{\text{MAP}}$를 구해요

</details>

---

<a id="partB"></a>

## B. 교과서 연습문제 (MML 6장)

<a id="p2"></a>

### P2. Joint 표에서 p(x) 구하기

두 이산 확률변수 $X$($x_1,\dots,x_5$)와 $Y$($y_1,y_2,y_3$)의 joint distribution $p(x,y)$가 아래 표와 같아요. 표의 맨 위 행이 $y_1$이에요.

|   | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ |
|---|---|---|---|---|---|
| $y_1$ | 0.01 | 0.02 | 0.03 | 0.1 | 0.1 |
| $y_2$ | 0.05 | 0.1 | 0.05 | 0.07 | 0.2 |
| $y_3$ | 0.1 | 0.05 | 0.03 | 0.05 | 0.04 |

$X$의 marginal distribution $p(x)$를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"Compute: a. The marginal distributions p(x) and p(y). b. The conditional distributions p(x|Y = y1) and p(y|X = x3)." — Exercise 6.1

</details>

<details><summary>힌트 보기</summary>

관심 없는 변수 $Y$에 대해 더해요. 표에서는 열마다 세로로 더하면 돼요.

</details>

<details><summary>풀이 보기</summary>

1. marginal은 joint를 관심 없는 변수로 합(연속이면 적분)해서 얻어요: $p(x)=\sum_{y}p(x,y)$.
2. $p(x_1)=0.01+0.05+0.1=0.16$, $p(x_2)=0.02+0.1+0.05=0.17$
3. $p(x_3)=0.03+0.05+0.03=0.11$, $p(x_4)=0.1+0.07+0.05=0.22$, $p(x_5)=0.1+0.2+0.04=0.34$
4. 확인: $0.16+0.17+0.11+0.22+0.34=1$이에요.
5. 수업과의 연결: marginal likelihood $P(x)=\int P(x\mid\theta)P(\theta)\,d\theta$처럼 joint를 관심 없는 $\theta$로 적분한 것과 같은 동작을, 이산 표에서 합으로 한 거예요.

**정답:** $p(x) = (0.16,\ 0.17,\ 0.11,\ 0.22,\ 0.34)$

</details>

---

<a id="p3"></a>

### P3. Joint 표에서 p(y) 구하기

두 이산 확률변수 $X$($x_1,\dots,x_5$)와 $Y$($y_1,y_2,y_3$)의 joint distribution $p(x,y)$가 아래 표와 같아요. 표의 맨 위 행이 $y_1$이에요.

|   | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ |
|---|---|---|---|---|---|
| $y_1$ | 0.01 | 0.02 | 0.03 | 0.1 | 0.1 |
| $y_2$ | 0.05 | 0.1 | 0.05 | 0.07 | 0.2 |
| $y_3$ | 0.1 | 0.05 | 0.03 | 0.05 | 0.04 |

$Y$의 marginal distribution $p(y)$를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"Compute: a. The marginal distributions p(x) and p(y). b. The conditional distributions p(x|Y = y1) and p(y|X = x3)." — Exercise 6.1

</details>

<details><summary>힌트 보기</summary>

이번엔 $X$에 대해 더해요. 표에서는 행마다 가로로 더하면 돼요.

</details>

<details><summary>풀이 보기</summary>

1. $p(y)=\sum_{x}p(x,y)$라서 행 합을 구해요.
2. $p(y_1)=0.01+0.02+0.03+0.1+0.1=0.26$
3. $p(y_2)=0.05+0.1+0.05+0.07+0.2=0.47$
4. $p(y_3)=0.1+0.05+0.03+0.05+0.04=0.27$, 확인: $0.26+0.47+0.27=1$
5. 수업과의 연결: 교수님이 "joint 분포가 가장 많은 정보를 갖고 있다"고 했죠. joint만 있으면 $f_X(x)$, $f_Y(y)$ 같은 marginal은 더해서 언제든 꺼낼 수 있어요.

**정답:** $p(y) = (0.26,\ 0.47,\ 0.27)$ ($y_1, y_2, y_3$ 순)

</details>

---

<a id="p4"></a>

### P4. 조건부 분포 p(x | Y = y1)

두 이산 확률변수 $X$($x_1,\dots,x_5$)와 $Y$($y_1,y_2,y_3$)의 joint distribution $p(x,y)$가 아래 표와 같아요. 표의 맨 위 행이 $y_1$이에요.

|   | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ |
|---|---|---|---|---|---|
| $y_1$ | 0.01 | 0.02 | 0.03 | 0.1 | 0.1 |
| $y_2$ | 0.05 | 0.1 | 0.05 | 0.07 | 0.2 |
| $y_3$ | 0.1 | 0.05 | 0.03 | 0.05 | 0.04 |

조건부 분포 $p(x\mid Y=y_1)$를 분수로 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"Compute: a. The marginal distributions p(x) and p(y). b. The conditional distributions p(x|Y = y1) and p(y|X = x3)." — Exercise 6.1

</details>

<details><summary>힌트 보기</summary>

$P(A\mid B)=\dfrac{P(A,B)}{P(B)}$를 써요. $y_1$ 행만 떼어 내서 그 행의 합으로 나누면 돼요.

</details>

<details><summary>풀이 보기</summary>

1. 조건부확률 정의: $p(x\mid y_1)=\dfrac{p(x,y_1)}{p(y_1)}$
2. 분모 $p(y_1)=0.01+0.02+0.03+0.1+0.1=0.26$
3. $\frac{0.01}{0.26}=\frac{1}{26}$, $\frac{0.02}{0.26}=\frac{1}{13}$, $\frac{0.03}{0.26}=\frac{3}{26}$, $\frac{0.1}{0.26}=\frac{5}{13}$ (두 칸)
4. 확인: $\frac{1+2+3+10+10}{26}=1$
5. 수업과의 연결: posterior를 유도할 때 칠판에 쓴 첫 줄 $P(A\mid B)=\dfrac{P(A,B)}{P(B)}$를 표에 그대로 적용한 거예요.

**정답:** $p(x\mid Y=y_1) = \left(\frac{1}{26},\ \frac{1}{13},\ \frac{3}{26},\ \frac{5}{13},\ \frac{5}{13}\right)$

</details>

---

<a id="p5"></a>

### P5. 조건부 분포 p(y | X = x3)

두 이산 확률변수 $X$($x_1,\dots,x_5$)와 $Y$($y_1,y_2,y_3$)의 joint distribution $p(x,y)$가 아래 표와 같아요. 표의 맨 위 행이 $y_1$이에요.

|   | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ |
|---|---|---|---|---|---|
| $y_1$ | 0.01 | 0.02 | 0.03 | 0.1 | 0.1 |
| $y_2$ | 0.05 | 0.1 | 0.05 | 0.07 | 0.2 |
| $y_3$ | 0.1 | 0.05 | 0.03 | 0.05 | 0.04 |

조건부 분포 $p(y\mid X=x_3)$를 분수로 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"Compute: a. The marginal distributions p(x) and p(y). b. The conditional distributions p(x|Y = y1) and p(y|X = x3)." — Exercise 6.1

</details>

<details><summary>힌트 보기</summary>

$x_3$ 열만 떼어 내서 그 열의 합 $p(x_3)$로 나눠요.

</details>

<details><summary>풀이 보기</summary>

1. $p(y\mid x_3)=\dfrac{p(x_3,y)}{p(x_3)}$
2. 분모 $p(x_3)=0.03+0.05+0.03=0.11$
3. $\frac{0.03}{0.11}=\frac{3}{11}$, $\frac{0.05}{0.11}=\frac{5}{11}$, $\frac{0.03}{0.11}=\frac{3}{11}$
4. 확인: $\frac{3+5+3}{11}=1$
5. 수업과의 연결: "주어진 것을 조건으로 두고 알고 싶은 것을 앞에 둔다"는 틀 그대로예요. $X=x_3$을 손에 쥐고 $Y$를 추론하는 모양이에요.

**정답:** $p(y\mid X=x_3) = \left(\frac{3}{11},\ \frac{5}{11},\ \frac{3}{11}\right)$ ($y_1, y_2, y_3$ 순)

</details>

---

<a id="p6"></a>

### P6. 컴파일 성공률의 posterior

코드를 안 바꿨는데도 프로그램이 컴파일될 때도 있고 안 될 때도 있어요. 성공 여부 $x\in\{0,1\}$을 Bernoulli 분포 $p(x\mid\mu)=\mu^{x}(1-\mu)^{1-x}$로 모델링해요. $N$번 시도한 결과 $x_1,\dots,x_N$을 i.i.d.로 봐요. prior로 $\mathrm{Beta}(\alpha,\beta)\propto\mu^{\alpha-1}(1-\mu)^{\beta-1}$가 주어져요. posterior $p(\mu\mid x_1,\dots,x_N)$를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"model the apparent stochasticity (success vs. no success) x of the compiler using a Bernoulli distribution with parameter µ" — Exercise 6.3

</details>

<details><summary>힌트 보기</summary>

먼저 $N$개의 Bernoulli 확률을 곱해 $\mu$의 지수끼리 모아 보세요. 그다음 posterior $\propto$ likelihood $\times$ prior를 써요.

</details>

<details><summary>풀이 보기</summary>

1. i.i.d.라서 likelihood는 곱으로 나뉘어요: $\prod_{n=1}^{N}\mu^{x_n}(1-\mu)^{1-x_n}=\mu^{k}(1-\mu)^{N-k}$, 여기서 $k = \sum_{n=1}^{N} x_n$ (성공 횟수)예요.
2. prior를 상수까지 쓰면 $p(\mu)=\frac{1}{B(\alpha,\beta)}\mu^{\alpha-1}(1-\mu)^{\beta-1}$ ($B(\alpha,\beta)$는 넓이를 1로 맞추는 상수).
3. posterior $\propto$ likelihood $\times$ prior라서 $p(\mu\mid x_1,\dots,x_N)\propto\mu^{\alpha + k - 1}(1-\mu)^{\beta + N - k - 1}$이에요.
4. 이건 파라미터만 바뀐 Beta 꼴이에요. 그래서 posterior는 $\mathrm{Beta}(\alpha + k, \beta + N - k)$예요. prior와 같은 Beta 꼴이 유지되고 파라미터만 데이터만큼 늘어나요.
5. 숫자로 확인: $N=10$, $k=2$, $\alpha=\beta=4$면 posterior는 $\mathrm{Beta}(6,12)\propto\mu^{5}(1-\mu)^{11}$. $\log$를 미분해 0으로 두면 $\frac{5}{\mu}-\frac{11}{1-\mu}=0$, 봉우리는 $\mu=\frac{5}{16}=0.3125$예요. ML 값 $\frac{2}{10}=0.2$보다 반반 쪽으로 끌려가요.
6. 수업과의 연결: 동전 10번 중 앞면 2번이면 ML은 0.2, "모름지기 반반"이라는 prior를 섞은 MAP는 0.3 정도라고 한 이야기를, Beta prior로 계산하면 이렇게 나와요.

**정답:** $p(\mu\mid x_1,\dots,x_N)=\mathrm{Beta}(\alpha + k, \beta + N - k)$, $k = \sum_{n=1}^{N} x_n$

</details>

---

출처: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* (Cambridge University Press, 2020). 풀이는 자체 작성이며 수치는 Python으로 검증했습니다.
