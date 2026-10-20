# 머신러닝기초 중간고사 모의평가 2회 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [1. 두 벡터로 표현하기](#p1)
  - [2. 행 미분과 Jacobian](#p2)
  - [3. 1차원 Gaussian의 곱](#p3)
  - [4. 작은 설계행렬의 ML과 MAP](#p4)
  - [5. 평균·공분산과 단순한 변환](#p5)
  - [6. 잡음모델에서 최소제곱까지](#p6)
  - [7. 평균모델의 prior와 MAP](#p7)
  - [8. 한 관측의 사후분포와 새 예측](#p8)
  - [9. 0을 관측했을 때의 모델 비교](#p9)
  - [10. 한 직선으로의 직교투영](#p10)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### 1. 두 벡터로 표현하기

EXAM Problem 1 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p1)

#### 주어진 조건

열벡터 $v_1=(1,0)^\top$, $v_2=(0,2)^\top$, $v_3=(1,2)^\top$를 생각하자.

#### 구할 것

1. $av_1+bv_2=0$을 이용하여 $v_1,v_2$가 선형독립인지 판정하라.
2. $c=(3,4)^\top$를 $v_1,v_2$의 선형결합으로 나타내라. 계수가 유일한 이유도 설명하라.
3. $v_1,v_2,v_3$는 선형독립인가? 0이 아닌 계수의 선형관계를 하나 제시하라.

<details><summary>원문 보기</summary>

#### Representing Vectors

Consider the column vectors $v_1=(1,0)^\top$, $v_2=(0,2)^\top$, and $v_3=(1,2)^\top$.

1. Use $av_1+bv_2=0$ to determine whether $v_1,v_2$ are linearly independent.
2. Express $c=(3,4)^\top$ as a linear combination of $v_1,v_2$. Explain why the coefficients are unique.
3. Are $v_1,v_2,v_3$ linearly independent? Give one relation whose coefficients are not all zero.

</details>

#### 문제를 내 말로 읽어요

먼저 두 벡터만 보고, 마지막에 세 번째 벡터를 추가해요. (a)는 영벡터를 만드는 방법, (b)는 목표벡터를 만드는 방법, (c)는 중복 방향이 생기는지를 물어요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“선형독립(linear independence)”은 영벡터를 만드는 계수가 모두 0이어야 한다는 뜻이에요. $av_1+bv_2=0$에서 $a,b$는 실수 계수예요. 각 성분을 비교하면 이 조건을 직접 검사할 수 있어요. 독립인 두 벡터로 같은 목표를 두 방법으로 나타냈다면 두 표현을 빼서 계수 차이가 모두 0임을 보일 수 있어요. 세 벡터의 종속은 계수가 모두 0은 아닌 관계 하나로 충분해요.

#### 종이에 쓰는 첫 줄

$$
av_1+bv_2=(a,2b)^\top.
$$

영벡터와 비교할 때와 목표 $(3,4)^\top$와 비교할 때를 나누어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$av_1+bv_2=0$은 $a=0$, $2b=0$이므로 $a=b=0$이에요. 따라서 $v_1,v_2$는 선형독립이에요.

#### (b)

$a=3$, $2b=4$에서 $b=2$예요. 따라서 $c=3v_1+2v_2$예요. 다른 계수 $a\prime,b\prime$도 같은 $c$를 만들면 $(a-a\prime)v_1+(b-b\prime)v_2=0$이에요. (a)의 독립성 때문에 두 계수 차이가 0이므로 유일해요.

#### (c)

$v_3=v_1+v_2$이므로 $v_1+v_2-v_3=0$이에요. 계수 $(1,1,-1)$는 모두 0이 아니므로 세 벡터는 선형종속이에요.

#### 완성 답과 검산

#### (a) 검산

$(a,2b)=(0,0)$의 두 성분을 따로 풀면 영해만 나와요. 두 벡터의 방향이 겹치지 않는다는 판정과 같아요.

#### (b) 검산

$3(1,0)^\top+2(0,2)^\top=(3,4)^\top$예요. 차이식에서 계수 차이가 0이라는 논증이 있으므로 단순히 한 표현을 찾은 데서 끝나지 않았어요.

#### (c) 검산

$(1,0)^\top+(0,2)^\top-(1,2)^\top=(0,0)^\top$예요. 0이 아닌 관계를 실제로 확인했어요.

#### 여기서 헷갈리기 쉬워요

두 벡터의 독립성을 확인한 결과를 세 벡터에 그대로 옮기지 않아요. 독립성은 어떤 벡터들의 집합을 검사하는지에 따라 달라져요.

#### 설명을 닫고 다시 풀어요

- 두 성분의 방정식으로 독립성을 판정해요.
- 목표를 만든 뒤 계수의 유일성을 차이식으로 설명해요.

**페이지 요약**

#### 떠올릴 개념·공식

두 벡터는 독립. $c=3v_1+2v_2$로 유일. 세 벡터는 $v_1+v_2-v_3=0$으로 종속.

#### 적용 조건

모든 벡터는 열벡터; 실수 계수

#### 출제 근거

HW1 P6-P7의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF 46, 47쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **선형결합 (linear combination)** — 벡터에 실수 계수를 곱해 더한 표현이에요. $av_1+bv_2$에서 계수는 스칼라이고 결과는 $2\times1$ 열벡터예요. 이 문제에서는 목표 $c$를 만드는 데 써요.
- **선형독립 (linear independence)** — 영벡터를 만드는 계수가 영계수뿐이라는 성질이에요. $av_1+bv_2=0$이 검사식이에요. 이 문제에서는 표현의 유일성을 보장해요.

---

<a id="p2"></a>

### 2. 행 미분과 Jacobian

EXAM Problem 2 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p2)

#### 주어진 조건

$x=(u,v)^\top\in\mathbb R^{2\times1}$, $f(x)=(u-1)^2+2(v+1)^2$, $g(x)=(u+v,u-2v)^\top$이다. 스칼라 함수의 미분은 행벡터, Jacobian은 출력×입력으로 쓴다.

#### 구할 것

1. $\nabla_x f$를 구하고 $(u,v)=(0,0)$에서 계산하라. 결과의 차원도 적어라.
2. $J_g$를 구하고 차원을 적어라.
3. $f$를 최소로 만드는 $x$와 최솟값을 구하라. 왜 전역 최소인지 제곱항으로 설명하라.

<details><summary>원문 보기</summary>

#### Row Derivatives and a Jacobian

Let $x=(u,v)^\top\in\mathbb R^{2\times1}$, $f(x)=(u-1)^2+2(v+1)^2$, and $g(x)=(u+v,u-2v)^\top$. Use row derivatives for scalar functions and output-by-input Jacobians.

1. Find $\nabla_x f$ and evaluate it at $(u,v)=(0,0)$. State its dimensions.
2. Find $J_g$ and state its dimensions.
3. Find the minimizer of $f$ and its minimum value. Use the squared terms to justify global minimality.

</details>

#### 문제를 내 말로 읽어요

입력 $x$는 열벡터지만 스칼라 출력 $f$의 미분은 행벡터예요. 벡터 출력 $g$의 미분은 출력마다 한 행을 갖는 행렬이에요. 최소점에서는 두 제곱항이 함께 0이 될 수 있는지 확인해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“행 미분(row derivative)”은 편미분을 가로로 모으라는 단서예요. $\nabla_xf=(\partial f/\partial u,\partial f/\partial v)$는 $1\times2$예요. Jacobian은 $J_{ij}=\partial g_i/\partial x_j$여서 출력 $g_1,g_2$가 행, 입력 $u,v$가 열이에요. 제곱항은 0 이상이므로 두 항을 동시에 0으로 만드는 점이 있으면 전역 최소를 바로 판단할 수 있어요.

#### 종이에 쓰는 첫 줄

$$
\frac{\partial f}{\partial u}=2(u-1),\qquad \frac{\partial f}{\partial v}=4(v+1).
$$

한 변수로 미분할 때 나머지는 상수예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$$
\nabla_xf=\begin{pmatrix}2(u-1)&4(v+1)\end{pmatrix}\in\mathbb R^{1\times2}.
$$

$(0,0)$에서는 $\begin{pmatrix}-2&4\end{pmatrix}$예요.

#### (b)

$g_1=u+v$의 두 미분을 첫 행에, $g_2=u-2v$의 두 미분을 둘째 행에 놓아요.

$$
J_g=\begin{pmatrix}1&1\\1&-2\end{pmatrix}\in\mathbb R^{2\times2}.
$$

선형함수라 입력값에 의존하지 않아요.

#### (c)

$f=(u-1)^2+2(v+1)^2\ge0$예요. $u=1$, $v=-1$일 때 두 항이 모두 0이므로 $x_*=(1,-1)^\top$, 최솟값은 0이에요. 0이 되려면 두 제곱이 각각 0이어야 하므로 이 전역 최소점은 유일해요.

#### 완성 답과 검산

#### (a) 검산

성분별 편미분이 $-2,4$이고 결과를 가로로 모았으므로 차원은 $1\times2$예요. 입력의 열 방향과 구별해요.

#### (b) 검산

$J_gx=(u+v,u-2v)^\top=g(x)$예요. $2\times2$ Jacobian과 $2\times1$ 입력의 곱이 원래 $2\times1$ 출력을 만들므로 출력 행·입력 열의 순서가 맞아요.

#### (c) 검산

$f(1,-1)=0$이고 모든 $x$에서 $f(x)\ge0$예요. 정지점 확인에만 머물지 않고 전역성·유일성까지 확인했어요.

#### 여기서 헷갈리기 쉬워요

gradient를 $(2(u-1),4(v+1))^\top$로 적으면 이 새 문제의 행 관례와 달라져요. Jacobian은 $2\times2$여도 성분의 행·열 위치를 바꾸면 다른 함수의 미분이 돼요.

#### 설명을 닫고 다시 풀어요

- 스칼라 미분과 Jacobian의 차원을 먼저 적어요.
- 제곱항으로 최소점의 전역성과 유일성을 설명해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\nabla_xf=(2(u-1),4(v+1))$, $J_g=\begin{pmatrix}1&1\\1&-2\end{pmatrix}$. 최소점 $(1,-1)^\top$, 최솟값 0.

#### 적용 조건

과제 원문의 열 관례를 그대로 인용하는 문제가 아니라 새 행 관례 변형; 출력×입력 Jacobian

#### 출제 근거

HW1 P10-P12의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF 153, 155, 156쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **행 미분 (row derivative)** — 스칼라 함수를 열 입력으로 미분한 $1\times2$ 행벡터예요. 이 문제에서는 $f$의 편미분 두 개를 가로로 모아요.
- **Jacobian** — 벡터 출력의 모든 1차 편미분이에요. $J_{ij}=\partial g_i/\partial x_j$로 정의해요. 이 문제에서는 두 출력과 두 입력이 있어 $2\times2$예요.

---

<a id="p3"></a>

### 3. 1차원 Gaussian의 곱

EXAM Problem 3 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p3)

#### 주어진 조건

$p_0(z)=\mathcal N(z\mid0,2)$, $p_1(z)=\mathcal N(z\mid2,2)$, $z\in\mathbb R$이다. 둘째 인수는 분산이다. $Z=\int_{\mathbb R}p_0(z)p_1(z)\,dz$, $q(z)=p_0(z)p_1(z)/Z$라 하자.

#### 구할 것

1. 곱의 지수에 나타나는 $z^2+(z-2)^2$를 완전제곱하라.
2. $q$의 평균·분산과 정규화된 밀도를 구하라.
3. $p_0p_1$의 상수 인자도 포함하여 $Z$를 구하라. $p_0p_1$ 자체가 밀도인지 판단하라.

<details><summary>원문 보기</summary>

#### A Product of Univariate Gaussians

Let $p_0(z)=\mathcal N(z\mid0,2)$ and $p_1(z)=\mathcal N(z\mid2,2)$ for $z\in\mathbb R$. The second argument is the variance. Define $Z=\int_{\mathbb R}p_0(z)p_1(z)\,dz$ and $q(z)=p_0(z)p_1(z)/Z$.

1. Complete the square in $z^2+(z-2)^2$, which appears in the exponent of the product.
2. Find the mean, variance, and normalized density of $q$.
3. Compute $Z$, including the constant factors in $p_0p_1$. Is $p_0p_1$ itself a probability density?

</details>

#### 문제를 내 말로 읽어요

두 밀도를 곱한 함수와 그것을 적분 1로 맞춘 밀도를 구별해요. (a)의 완전제곱으로 (b)의 평균·분산을 읽고, (c)에서는 처음 밀도의 앞 계수를 되살려 적분해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“Gaussian 곱”에서는 지수의 이차식을 완전제곱(completing the square)해요. $\mathcal N(z\mid m,v)=\exp[-(z-m)^2/(2v)]/\sqrt{2\pi v}$에서 $m$은 평균, $v>0$는 분산이에요. 지수의 제곱 중심이 평균이고 바깥 계수를 $1/(2v)$와 비교해 분산을 읽어요. 정규화(normalization)는 적분이 1이 되게 나누는 작업이므로 $Z$를 구할 때 상수항도 보존해야 해요.

#### 종이에 쓰는 첫 줄

$$
p_0(z)p_1(z)=\frac1{4\pi}\exp\left[-\frac{z^2+(z-2)^2}{4}\right].
$$

각 분산이 2라서 지수의 분모는 4예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$$
z^2+(z-2)^2=2z^2-4z+4=2(z-1)^2+2.
$$

따라서 곱의 지수는 $-(z-1)^2/2-1/2$예요.

#### (b)

$z$에 따른 모양은 $\exp[-(z-1)^2/2]$예요. $1/(2v)=1/2$에서 $v=1$, 중심은 1이에요.

$$
q(z)=\frac1{\sqrt{2\pi}}\exp\left[-\frac{(z-1)^2}{2}\right]=\mathcal N(z\mid1,1).
$$

#### (c)

$$
p_0p_1=\frac{e^{-1/2}}{4\pi}\exp\left[-\frac{(z-1)^2}{2}\right].
$$

뒤 지수함수의 적분은 $\sqrt{2\pi}$이므로

$$
Z=\frac{e^{-1/2}\sqrt{2\pi}}{4\pi}=\frac{e^{-1/2}}{\sqrt{8\pi}}.
$$

$Z\ne1$이므로 원래 곱은 정규화된 확률밀도가 아니에요.

#### 완성 답과 검산

#### (a) 검산

$z=0$에서 왼쪽은 4, 오른쪽도 $2+2=4$예요. 전개하면 두 다항식의 모든 계수가 같아요.

#### (b) 검산

$q$의 앞 계수와 Gaussian 적분을 곱하면 1이에요. 정밀도도 $1/2+1/2=1$이므로 사후 곱의 분산 1과 일치해요.

#### (c) 검산

$Zq(z)=e^{-1/2}\exp[-(z-1)^2/2]/(4\pi)$로 원래 곱과 같아요. $Z$는 약 $0.121$여서 1이 아니에요.

#### 여기서 헷갈리기 쉬워요

정규화된 $q$에서는 없어지는 $e^{-1/2}$가 $Z$에서는 필요해요. 분산 2를 표준편차 2로 바꾸어 지수 분모를 8로 쓰지 않아요.

#### 설명을 닫고 다시 풀어요

- 지수의 바깥 계수까지 포함해 평균·분산을 읽어요.
- 원래 곱의 상수와 적분값을 곱해 Z를 복원해요.

**페이지 요약**

#### 떠올릴 개념·공식

$z^2+(z-2)^2=2(z-1)^2+2$. $q=\mathcal N(1,1)$, $Z=e^{-1/2}/\sqrt{8\pi}\ne1$.

#### 적용 조건

두 Gaussian의 둘째 인수는 분산; 원래 곱과 정규화된 곱 구별

#### 출제 근거

HW1 P14,P25의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF 207, 208쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **정밀도 (precision)** — 분산의 역수 $1/v$예요. 같은 변수의 Gaussian을 곱할 때 정밀도가 더해져요. 이 문제에서는 $1/2+1/2=1$이에요.
- **정규화 상수 (normalizing constant)** — 함수의 전체 적분을 1로 만드는 데 필요한 상수예요. 이 문제의 $Z=\int p_0p_1$는 원래 곱을 나누는 값이에요.

---

<a id="p4"></a>

### 4. 작은 설계행렬의 ML과 MAP

EXAM Problem 4 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p4)

#### 주어진 조건

$\phi(x)=(1,x)^\top$, $f_\theta(x)=\phi(x)^\top\theta$, $\theta=(\theta_0,\theta_1)^\top$이다. 관측은 $(-1,1),(0,2),(1,3)$이고 잡음은 서로 독립인 $\mathcal N(0,1)$이다. MAP에서는 절편을 포함한 두 계수 모두에 $\theta\sim\mathcal N(0,I_2)$를 사용한다. ML/MAP의 표준 공식을 사용해도 된다.

#### 구할 것

1. 관측 순서대로 $\phi(x_n)^\top$를 쌓은 설계행렬 $\Phi$와 $y$를 구성하라.
2. $\Phi^\top\Phi$, $\Phi^\top y$, $\hat\theta_{\rm ML}$을 구하라.
3. $\hat\theta_{\rm MAP}$과 $x_*=0$에서의 평균 예측을 구하라. 절편도 줄어드는 이유를 설명하라.

<details><summary>원문 보기</summary>

#### ML and MAP with a Small Design Matrix

Let $\phi(x)=(1,x)^\top$, $f_\theta(x)=\phi(x)^\top\theta$, and $\theta=(\theta_0,\theta_1)^\top$. The observations are $(-1,1),(0,2),(1,3)$, with independent $\mathcal N(0,1)$ noise. For MAP use $\theta\sim\mathcal N(0,I_2)$ for both coefficients, including the intercept. You may use the standard ML and MAP formulas.

1. Construct the design matrix $\Phi$ by stacking $\phi(x_n)^\top$ in observation order, and construct $y$.
2. Compute $\Phi^\top\Phi$, $\Phi^\top y$, and $\hat\theta_{\rm ML}$.
3. Compute $\hat\theta_{\rm MAP}$ and the predicted mean at $x_*=0$. Explain why the intercept also shrinks.

</details>

#### 문제를 내 말로 읽어요

스칼라 입력 세 개를 특징 열벡터로 바꾼 다음 각각 전치해 행으로 쌓아요. ML은 데이터만, MAP는 두 계수 모두에 주어진 prior까지 반영해요. 이 문항은 공식 적용형이므로 공식을 대입해 계산해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“$\phi(x)=(1,x)^\top$”는 첫 특징이 절편, 둘째 특징이 입력임을 뜻해요. $\phi$는 함수, $\phi(x_n)$는 $2\times1$ 특징벡터, $\Phi$는 $3\times2$ 설계행렬(design matrix)이에요. $\Phi_{n1}=1$, $\Phi_{n2}=x_n$이며 $n$은 관측 행 번호예요. 독립·동일분산 Gaussian 잡음에서 열독립이면 ML은 $(\Phi^\top\Phi)^{-1}\Phi^\top y$예요. 잡음분산과 prior 분산이 모두 1이므로 MAP는 $(\Phi^\top\Phi+I_2)^{-1}\Phi^\top y$예요. 절편에도 prior가 적용된다는 조건 때문에 두 대각성분 모두에 1을 더해요.

#### 종이에 쓰는 첫 줄

$$
\phi(-1)=\begin{pmatrix}1\\-1\end{pmatrix},\quad \phi(0)=\begin{pmatrix}1\\0\end{pmatrix},\quad \phi(1)=\begin{pmatrix}1\\1\end{pmatrix}.
$$

이 전치들을 관측 순서대로 놓아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$$
\Phi=\begin{pmatrix}1&-1\\1&0\\1&1\end{pmatrix},\qquad y=\begin{pmatrix}1\\2\\3\end{pmatrix}.
$$

행은 관측, 열은 절편·입력 특징이에요.

#### (b)

열끼리 내적하면

$$
\Phi^\top\Phi=\begin{pmatrix}3&0\\0&2\end{pmatrix},\quad \Phi^\top y=\begin{pmatrix}6\\2\end{pmatrix}.
$$

따라서

$$
\hat\theta_{\rm ML}=\begin{pmatrix}1/3&0\\0&1/2\end{pmatrix}\begin{pmatrix}6\\2\end{pmatrix}=\begin{pmatrix}2\\1\end{pmatrix}.
$$

#### (c)

$$
\hat\theta_{\rm MAP}=(\Phi^\top\Phi+I_2)^{-1}\Phi^\top y=\begin{pmatrix}6/4\\2/3\end{pmatrix}=\begin{pmatrix}3/2\\2/3\end{pmatrix}.
$$

$x_*=0$에서는 $\phi(0)=(1,0)^\top$이므로 평균 예측은 $\phi(0)^\top\hat\theta_{\rm MAP}=3/2$예요. prior가 절편과 기울기 모두를 0 쪽으로 당기므로 절편도 줄어요.

#### 완성 답과 검산

#### (a) 검산

$\Phi\theta=(\theta_0-\theta_1,\theta_0,\theta_0+\theta_1)^\top$로 세 입력의 모델과 같아요.

#### (b) 검산

$\Phi(2,1)^\top=(1,2,3)^\top=y$이므로 오차 0이에요. Gram 행렬식은 $3\cdot2=6>0$이라 ML이 유일해요.

#### (c) 검산

$(\Phi^\top\Phi+I_2)(3/2,2/3)^\top=(6,2)^\top$예요. $x_*=0$의 특징은 기울기 항을 0으로 만들므로 예측값이 절편과 같아요.

#### 여기서 헷갈리기 쉬워요

$\phi(x)$를 행으로 정의해 놓고 다시 전치하면 차원이 바뀌어요. 이 문제의 prior는 절편을 제외하지 않으므로 첫 대각항도 $3+1=4$예요.

#### 설명을 닫고 다시 풀어요

- 특징벡터와 설계행렬의 차원을 말해요.
- ML 공식과 MAP 공식에 각각 수치를 대입해요.

**페이지 요약**

#### 떠올릴 개념·공식

$G=\operatorname{diag}(3,2)$, $\Phi^\top y=(6,2)^\top$. ML $(2,1)^\top$, MAP $(3/2,2/3)^\top$, $x_*=0$ 예측 $3/2$.

#### 적용 조건

입력 고정; 잡음분산 1; 모든 계수에 N(0,I2) prior

#### 출제 근거

HW1 P9,P17,P19의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF 300, 302, 307, 308쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **설계행렬 (design matrix)** — $\Phi_{n,:}=\phi(x_n)^\top$인 관측×특징 행렬이에요. 이 문제에서는 $3\times2$이고 두 열은 절편·입력이에요.
- **MAP (maximum a posteriori)** — posterior 밀도를 가장 크게 하는 모수예요. 이 문제에서는 prior가 두 계수에 제곱벌점을 주어 Gram에 $I_2$를 더해요.
- **ML (maximum likelihood)** — 주어진 모수에서 관측된 데이터의 밀도를 최대화해요. 이 문제의 동일 Gaussian 잡음에서는 최소제곱과 같아요.

---

<a id="p5"></a>

### 5. 평균·공분산과 단순한 변환

EXAM Problem 5 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p5)

#### 주어진 조건

$X$는 $(0,0)^\top,(2,0)^\top,(0,2)^\top,(2,2)^\top$ 중 하나를 각각 확률 $1/4$로 갖는다. $Y=AX+b$, $A=\operatorname{diag}(2,1)$, $b=(1,-1)^\top$라 하자. 공분산은 이 확률분포에 대한 것으로 분모는 $4$이다. Gaussian은 가정하지 않는다.

#### 구할 것

1. $\mu_X=E[X]$를 구하라.
2. $\Sigma_X=E[(X-\mu_X)(X-\mu_X)^\top]$를 구하라.
3. $E[Y]$, $\operatorname{Cov}(Y)$, $\operatorname{Cov}(X,Y)$를 구하라. 이동 $b$가 공분산에 영향을 주는지도 설명하라.

<details><summary>원문 보기</summary>

#### Mean, Covariance, and a Simple Transformation

$X$ takes each of $(0,0)^\top,(2,0)^\top,(0,2)^\top,(2,2)^\top$ with probability $1/4$. Let $Y=AX+b$, where $A=\operatorname{diag}(2,1)$ and $b=(1,-1)^\top$. Compute covariance under this distribution, using denominator $4$. Do not assume a Gaussian distribution.

1. Compute $\mu_X=E[X]$.
2. Compute $\Sigma_X=E[(X-\mu_X)(X-\mu_X)^\top]$.
3. Compute $E[Y]$, $\operatorname{Cov}(Y)$, and $\operatorname{Cov}(X,Y)$. Explain whether the shift $b$ affects covariance.

</details>

#### 문제를 내 말로 읽어요

네 점을 같은 확률로 고르는 이산분포예요. 평균에서 벗어난 네 벡터를 만든 뒤 외적을 평균내요. 변환에서는 배율과 이동의 역할을 구분해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“각각 확률 $1/4$”이므로 기대값(expectation)은 네 값의 평균이에요. 공분산(covariance)은 $\Sigma_X=E[(X-\mu_X)(X-\mu_X)^\top]$로 두 좌표의 함께 변하는 정도를 모은 $2\times2$ 행렬이에요. 아핀 변환 $Y=AX+b$에서는 $\mu_Y=A\mu_X+b$, $\Sigma_Y=A\Sigma_XA^\top$예요. 교차공분산은 첫 변수가 $X$일 때 $\operatorname{Cov}(X,Y)=\Sigma_XA^\top$예요. 중심화하면 상수 $b$가 사라져 이 공식들이 성립해요.

#### 종이에 쓰는 첫 줄

$$
\mu_X=\frac14\left[\begin{pmatrix}0\\0\end{pmatrix}+\begin{pmatrix}2\\0\end{pmatrix}+\begin{pmatrix}0\\2\end{pmatrix}+\begin{pmatrix}2\\2\end{pmatrix}\right].
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

각 좌표의 합이 4이므로 $\mu_X=(1,1)^\top$예요.

#### (b)

중심화 벡터는 $(-1,-1)^\top,(1,-1)^\top,(-1,1)^\top,(1,1)^\top$이에요. 각 좌표의 제곱은 모두 1이고 좌표곱의 합은 $1-1-1+1=0$이에요. 따라서

$$
\Sigma_X=\begin{pmatrix}1&0\\0&1\end{pmatrix}.
$$

#### (c)

공식에 대입하면

$$
E[Y]=A\mu_X+b=\begin{pmatrix}3\\0\end{pmatrix},
$$

$$
\operatorname{Cov}(Y)=AI_2A^\top=\begin{pmatrix}4&0\\0&1\end{pmatrix},
$$

$$
\operatorname{Cov}(X,Y)=I_2A^\top=\begin{pmatrix}2&0\\0&1\end{pmatrix}.
$$

$Y-E[Y]=A(X-\mu_X)$라 이동 $b$는 두 공분산에 들어가지 않아요.

#### 완성 답과 검산

#### (a) 검산

각 좌표는 0과 2를 같은 확률로 가지므로 두 평균은 각각 1이에요.

#### (b) 검산

외적 네 개를 합하면 $\operatorname{diag}(4,4)$이고 4로 나누면 $I_2$예요. 분모 3의 불편표본공분산을 계산한 것이 아니에요.

#### (c) 검산

$Y$의 실제 네 값은 $(1,-1),(5,-1),(1,1),(5,1)$이에요. 평균 $(3,0)$에서의 차는 $(\pm2,\pm1)$이므로 분산 4,1과 교차항 0이 직접 확인돼요. $X$와 $Y$의 첫 좌표 중심곱은 항상 2, 둘째는 항상 1이에요.

#### 여기서 헷갈리기 쉬워요

확률분포가 지정되어 있으므로 분모를 $N-1$로 바꾸지 않아요. $\operatorname{Cov}(X,Y)$와 $\operatorname{Cov}(Y,X)$는 일반적으로 전치 관계예요. 이 예에서 수치가 대각이라고 순서 규칙을 생략하지 않아요.

#### 설명을 닫고 다시 풀어요

- 중심화한 네 벡터로 공분산을 다시 계산해요.
- 평균에는 b가 남고 공분산에는 사라지는 이유를 말해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mu_X=(1,1)^\top$, $\Sigma_X=I_2$. $\mu_Y=(3,0)^\top$, $\Sigma_Y=\operatorname{diag}(4,1)$, $C_{XY}=\operatorname{diag}(2,1)$.

#### 적용 조건

명시한 이산분포; 분모4; Gaussian 가정 없음; Cov(X,Y)의 순서 고정

#### 출제 근거

HW1 P21-P22의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF 194, 196, 198, 200쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **아핀 변환 (affine transformation)** — 선형변환 $AX$에 상수이동 $b$를 더한 변환이에요. 이 문제에서는 첫 좌표를 두 배 하고 $(1,-1)^\top$만큼 이동해요.
- **교차공분산 (cross-covariance)** — $E[(X-\mu_X)(Y-\mu_Y)^\top]$예요. 행은 X좌표, 열은 Y좌표이고 이 문제에서는 $\Sigma_XA^\top$로 계산해요.

---

<a id="p6"></a>

### 6. 잡음모델에서 최소제곱까지

EXAM Problem 6 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p6)

#### 주어진 조건

$y_n=\phi(x_n)^\top\theta+\epsilon_n$, $\phi(x)=(1,x)^\top$, $\theta\in\mathbb R^{2\times1}$이다. 고정된 관측은 $(x_1,y_1)=(-1,1)$, $(x_2,y_2)=(1,3)$이고 $\epsilon_1,\epsilon_2$는 서로 독립인 $\mathcal N(0,1)$이다. $\Phi$의 $n$번째 행은 $\phi(x_n)^\top$이다. 미분은 행벡터로 쓴다.

#### 구할 것

1. 잡음분포에서 $p(y_n\mid x_n,\theta)$를 얻고, 독립성을 이용하여 두 관측의 likelihood $L(\theta)$를 상수까지 포함해 써라.
2. $-\log L(\theta)$를 구하라. 이를 최소화하는 것이 평균 제곱오차(ERM)를 최소화하는 것과 같은 이유를 설명하라.
3. $Q(\theta)=\|y-\Phi\theta\|^2$를 행 미분하고 0으로 놓아라. 양변을 전치하여 정규방정식을 도출하라.
4. 이 데이터의 $\Phi^\top\Phi$와 $\Phi^\top y$를 계산하여 $\hat\theta_{\rm ML}$과 훈련 예측 $\hat y$를 구하라. 해의 유일성도 확인하라.

<details><summary>원문 보기</summary>

#### From a Noise Model to Least Squares

Let $y_n=\phi(x_n)^\top\theta+\epsilon_n$, $\phi(x)=(1,x)^\top$, and $\theta\in\mathbb R^{2\times1}$. The fixed observations are $(x_1,y_1)=(-1,1)$ and $(x_2,y_2)=(1,3)$. The errors are independent $\mathcal N(0,1)$. Row $n$ of $\Phi$ is $\phi(x_n)^\top$. Use row derivatives.

1. Obtain $p(y_n\mid x_n,\theta)$ from the noise distribution. Use independence to write the likelihood $L(\theta)$ of both observations, including its constant factor.
2. Find $-\log L(\theta)$. Explain why minimizing it is equivalent to empirical risk minimization (ERM) with mean squared error.
3. Compute the row derivative of $Q(\theta)=\|y-\Phi\theta\|^2$ and set it to zero. Transpose both sides to derive the normal equations.
4. Compute $\Phi^\top\Phi$ and $\Phi^\top y$ for these data, then find $\hat\theta_{\rm ML}$ and the training predictions $\hat y$. Check uniqueness.

</details>

#### 문제를 내 말로 읽어요

먼저 입력과 계수를 고정해서 출력의 무작위성이 어디서 오는지 봐요. 그런 다음 독립인 밀도의 곱, 음의 로그, 제곱오차 미분, 실제 수치 해 순서로 이어가요. 결과 미분은 $1\times2$ 행벡터예요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“독립인 Gaussian 잡음”이 단서예요. $\theta$와 입력을 고정하면 $\phi(x_n)^\top\theta$는 상수라 출력의 평균만 이동해요. 조건부 독립(conditional independence)이 있으므로 likelihood를 두 밀도의 곱으로 써요. 로그는 곱을 합으로 바꾸고, 알려진 양의 분산에서는 음의 로그우도(NLL)의 최소점이 제곱오차와 같아요. $\Phi\in\mathbb R^{2\times2}$는 관측×특징, $y,\theta\in\mathbb R^{2\times1}$이에요. 정규방정식(normal equations)은 제곱오차의 행 미분을 0으로 둔 뒤 양변을 전치해서 얻어요.

#### 종이에 쓰는 첫 줄

$$
y_n\mid x_n,\theta=\phi(x_n)^\top\theta+\epsilon_n.
$$

조건을 고정한 뒤 남는 무작위 변수는 $\epsilon_n$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

잡음에 고정된 평균을 더하므로 $y_n\mid x_n,\theta\sim\mathcal N(\theta_0+\theta_1x_n,1)$이에요. 서로 다른 독립 잡음으로 만들어 조건부 출력들도 독립이에요.

$$
L(\theta)=\prod_{n=1}^2\frac1{\sqrt{2\pi}}e^{-(y_n-\phi(x_n)^\top\theta)^2/2}.
$$

따라서

$$
L(\theta)=\frac1{2\pi}\exp\left[-\frac{(1-\theta_0+\theta_1)^2+(3-\theta_0-\theta_1)^2}{2}\right].
$$

#### (b)

두 제곱의 합을 $Q$라 하면

$$
-\log L=\log(2\pi)+\frac12Q.
$$

경험위험은 관측 두 개의 평균 제곱손실 $\widehat R=Q/2$예요. 따라서 NLL $=\log(2\pi)+\widehat R$이고, 더한 항은 $\theta$와 무관하므로 최소점이 같아요. 로그가 증가함수라 likelihood 최대화도 같은 점을 골라요.

#### (c)

$G=\Phi^\top\Phi$로 놓고 제곱을 펼쳐요.

$$
Q=y^\top y-2y^\top\Phi\theta+\theta^\top G\theta.
$$

$G$는 대칭이므로 행 미분은

$$
\nabla_\theta Q=-2y^\top\Phi+2\theta^\top G\in\mathbb R^{1\times2}.
$$

이를 $0_{1\times2}$로 놓으면 $\theta^\top G=y^\top\Phi$예요. **양변을 전치**하고 $G^\top=G$를 쓰면

$$
G\theta=\Phi^\top y\in\mathbb R^{2\times1}.
$$

이것이 정규방정식이에요.

#### (d)

$$
\Phi=\begin{pmatrix}1&-1\\1&1\end{pmatrix},\quad y=\begin{pmatrix}1\\3\end{pmatrix}.
$$

따라서 $G=2I_2$, $\Phi^\top y=(4,2)^\top$예요.

$$
\hat\theta_{\rm ML}=G^{-1}\Phi^\top y=\begin{pmatrix}2\\1\end{pmatrix},\quad \hat y=\Phi\hat\theta_{\rm ML}=\begin{pmatrix}1\\3\end{pmatrix}.
$$

$G=2I_2$는 양의 정부호라 $Q$의 Hessian $2G=4I_2$도 양의 정부호이고 이 해가 유일한 전역 최소점이에요.

#### 완성 답과 검산

#### (a) 검산

두 조건부 평균은 $\theta_0-\theta_1$, $\theta_0+\theta_1$예요. 이를 각 $\mathcal N(y_n\mid\mu_n,1)$에 넣으면 전개식과 같고 상수는 $(\sqrt{2\pi})^{-2}=1/(2\pi)$예요.

#### (b) 검산

$Q$가 2만큼 증가하면 NLL은 1, $\widehat R$도 1만큼 증가해요. 고정된 상수를 더하는 연산만 남아 최소화 순서가 같아요.

#### (c) 검산

성분으로 직접 미분하면 $\nabla_\theta Q=(4\theta_0-8,4\theta_1-4)$예요. $G=2I_2$, $y^\top\Phi=(4,2)$를 행 식에 넣은 것과 같아요. 곱 $\theta^\top G$와 $y^\top\Phi$는 모두 $1\times2$예요.

#### (d) 검산

두 예측이 실제 y와 같아 $Q=0$이에요. $Q$는 항상 0 이상이고 $\det\Phi=2\ne0$이므로 같은 예측을 만드는 다른 계수도 없어요.

#### 여기서 헷갈리기 쉬워요

독립성은 입력과 $\theta$를 조건으로 둔 상태의 말이에요. 행 미분을 열 정규방정식으로 곧바로 바꾸지 말고 양변 전치를 적어요. 밀도값을 구하는 (a)에서는 상수 $1/(2\pi)$도 필요해요.

#### 설명을 닫고 다시 풀어요

- 잡음→조건부 밀도→곱 likelihood→NLL 순서로 써요.
- 행 미분을 0으로 놓고 양변을 전치해 수치 해를 얻어요.

**페이지 요약**

#### 떠올릴 개념·공식

$L=(2\pi)^{-1}e^{-Q/2}$, NLL $=\log(2\pi)+Q/2$. $\nabla Q=-2y^\top\Phi+2\theta^\top G$. 전치→$G\theta=\Phi^\top y$. ML $(2,1)^\top$.

#### 적용 조건

입력 고정; θ 조건부 독립; 알려진 분산1; 행 미분

#### 출제 근거

MML 9.2.1-9.2.2; HW1 P15-P17의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF 298, 299, 300, 302쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **우도 (likelihood)** — 고정한 관측에서 모수를 바꿔 평가하는 밀도예요. 이 문제에서는 $L(\theta)=p(y\mid\Phi,\theta)$이고 두 관측의 곱으로 시작해요.
- **경험위험 (empirical risk)** — 관측별 손실의 평균이에요. 이 문제의 관측 수는 2이므로 제곱손실 위험은 $Q/2$예요.
- **정규방정식 (normal equations)** — 최소제곱 정지점이 만족하는 $\Phi^\top\Phi\theta=\Phi^\top y$예요. 이 문제에서는 행 미분식의 양변 전치를 통해 얻어요.

---

<a id="p7"></a>

### 7. 평균모델의 prior와 MAP

EXAM Problem 7 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p7)

#### 주어진 조건

$y_n=\theta+\epsilon_n$이고 $\theta\in\mathbb R$, $\epsilon_n\stackrel{\rm iid}{\sim}\mathcal N(0,1)$이다. 관측은 $D=(y_1,y_2)=(1,3)$이다. prior는 $\theta\sim\mathcal N(0,1)$이며 잡음과 독립이다.

#### 구할 것

1. Bayes 법칙을 이용하여 $p(\theta\mid D)$를 likelihood와 prior의 곱에 비례하는 식으로 써라. 정규화 상수는 계산하지 않아도 된다.
2. 음의 log-posterior를 $\theta$와 무관한 상수를 제외하고 구하라. 데이터 오차 제곱합에 어떤 penalty가 더해지는가?
3. 앞 목적함수를 미분하여 $\hat\theta_{\rm MAP}$을 구하고, prior를 제외한 $\hat\theta_{\rm ML}$과 비교하라.
4. prior만 $\mathcal N(0,1/4)$로 바꾸어 MAP을 다시 구하라. prior 분산 감소가 추정값에 미친 영향을 설명하라.

<details><summary>원문 보기</summary>

#### A Prior and MAP in a Mean Model

Let $y_n=\theta+\epsilon_n$, where $\theta\in\mathbb R$ and $\epsilon_n\stackrel{\rm iid}{\sim}\mathcal N(0,1)$. The data are $D=(y_1,y_2)=(1,3)$. Use the prior $\theta\sim\mathcal N(0,1)$, independent of the noise.

1. Use Bayes rule to express $p(\theta\mid D)$ as proportional to likelihood times prior. You need not compute the normalizing constant.
2. Find the negative log-posterior up to terms independent of $\theta$. What penalty is added to the sum of squared data errors?
3. Differentiate that objective to find $\hat\theta_{\rm MAP}$. Compare it with $\hat\theta_{\rm ML}$ obtained without the prior.
4. Change only the prior to $\mathcal N(0,1/4)$ and recompute MAP. Explain the effect of decreasing the prior variance.

</details>

#### 문제를 내 말로 읽어요

같은 평균을 갖는 두 관측으로 스칼라 계수 하나를 추정해요. prior를 곱해 만든 목적함수에서 데이터 항과 prior 항을 구분하고, 분산만 바꿔 벌점 세기를 비교해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“prior와 MAP”가 나오면 Bayes 법칙 $p(\theta\mid D)=p(D\mid\theta)p(\theta)/p(D)$를 떠올려요. $p(D)$는 모수를 적분한 evidence라 현재 비교하는 $\theta$와 무관해요. Gaussian의 음의 로그는 중심에서의 제곱거리/분산을 남겨요. 따라서 prior 분산이 작을수록 평균 0에서 멀어지는 벌점이 커져요. 여기서는 $\theta\in\mathbb R^{1\times1}$인 스칼라라 미분도 $1\times1$이에요. ridge는 데이터 제곱오차에 양의 계수로 $\theta^2$를 더한 형태예요.

#### 종이에 쓰는 첫 줄

$$
p(D\mid\theta)=\mathcal N(1\mid\theta,1)\mathcal N(3\mid\theta,1).
$$

여기에 prior 밀도를 곱해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

Bayes 법칙에서 $p(D)=\int p(D\mid u)p(u)\,du$는 $\theta$와 무관해요. 그러므로

$$
p(\theta\mid D)\propto \mathcal N(1\mid\theta,1)\mathcal N(3\mid\theta,1)\mathcal N(\theta\mid0,1).
$$

즉 $p(\theta\mid D)\propto\exp[-\{(1-\theta)^2+(3-\theta)^2+\theta^2\}/2]$예요.

#### (b)

상수항을 제외하면

$$
J(\theta)=\frac12[(1-\theta)^2+(3-\theta)^2]+\frac12\theta^2.
$$

양수 2를 곱하면 데이터 제곱합 $Q$에 $\theta^2$가 더해져요. 따라서 $Q+\lambda\theta^2$로 쓴 ridge 계수는 $\lambda=1$이에요.

#### (c)

$$
J\prime(\theta)=(\theta-1)+(\theta-3)+\theta=3\theta-4.
$$

0으로 놓으면 $\hat\theta_{\rm MAP}=4/3$이에요. prior를 제외하면 $Q/2$의 미분은 $2\theta-4$여서 $\hat\theta_{\rm ML}=2$예요. $J\prime\prime=3>0$이고 데이터 항도 곡률 2가 양수라 두 최소점은 각각 유일해요. MAP가 prior 평균 0에 더 가까워요.

#### (d)

prior 분산이 $1/4$이면 prior 벌점은 $\theta^2/(2\cdot1/4)=2\theta^2$예요.

$$
J_{1/4}\prime=(\theta-1)+(\theta-3)+4\theta=6\theta-4.
$$

따라서 MAP는 $2/3$이에요. $Q$ 기준 벌점계수는 $\lambda=4$로 커지고, $2>4/3>2/3>0$이므로 더 강하게 0 쪽으로 줄었어요.

#### 완성 답과 검산

#### (a) 검산

세 Gaussian의 지수 분모가 모두 2이므로 세 제곱이 동일한 가중치로 더해져요. 분모 evidence를 생략했으므로 등식 대신 비례식이에요.

#### (b) 검산

$2J=Q+\theta^2$라 제곱오차 항과 벌점항의 상대계수가 1이에요. 양의 배수는 최소점을 바꾸지 않아요.

#### (c) 검산

$3(4/3)-4=0$, $2\cdot2-4=0$예요. 상수 곡률 3과 2는 양수라 정지점이 실제 최소점이에요.

#### (d) 검산

$6(2/3)-4=0$이고 곡률 6은 양수예요. 분산의 역수 4가 미분의 prior 항에 들어간 것도 확인해요.

#### 여기서 헷갈리기 쉬워요

prior 분산 $1/4$를 벌점계수 $1/4$로 쓰지 않아요. 여기서는 역수 4가 벌점 세기예요. likelihood를 모수의 정규화된 분포라고 부르지 않아요.

#### 설명을 닫고 다시 풀어요

- Bayes 식에서 evidence가 모수와 무관한 이유를 말해요.
- prior 분산을 바꿔 목적함수부터 다시 미분해요.

**페이지 요약**

#### 떠올릴 개념·공식

$J=Q/2+\theta^2/2$. ML $2$, MAP $4/3$. prior 분산 $1/4$→$J=Q/2+2\theta^2$→MAP $2/3$.

#### 적용 조건

모수1개; 독립 잡음분산1; prior 분산1 또는1/4

#### 출제 근거

MML 9.2.3-9.2.4; HW1 P18,P24의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF 307, 308, 309쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **사전분포 (prior)** — 데이터를 보기 전 계수의 분포예요. 이 문제의 평균 0은 벌점의 중심, 분산은 그 벌점의 역세기를 정해요.
- **사후분포 (posterior)** — likelihood와 prior를 곱해 데이터에 맞게 갱신한 계수 분포예요. 그 밀도의 최대점이 MAP예요.
- **ridge penalty** — 평균 0에서 벗어난 계수의 제곱에 벌점을 줘요. 이 문제에서 $Q+\lambda\theta^2$의 $\lambda$는 prior 분산 1이면 1, 1/4이면 4예요.

---

<a id="p8"></a>

### 8. 한 관측의 사후분포와 새 예측

EXAM Problem 8 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p8)

#### 주어진 조건

$\theta\sim\mathcal N(0,1)$, $y=\theta+\epsilon$, $\epsilon\sim\mathcal N(0,1)$이고 $\theta,\epsilon$은 독립이다. $y=2$를 관측했다. 새 입력에서 잡음 없는 값은 $f_*=2\theta$, 관측값은 $y_*=2\theta+\epsilon_*$이다. $\epsilon_*\sim\mathcal N(0,1)$는 $\theta,\epsilon$과 독립이다. Gaussian의 아핀 변환·독립합 공식을 사용해도 된다.

#### 구할 것

1. 잡음모델을 이용하여 관측 $y=2$의 likelihood $p(y=2\mid\theta)$를 써라. 여기서 likelihood는 관측점에서 평가한 밀도이다.
2. likelihood와 prior를 곱하고 완전제곱하여 정규화된 $p(\theta\mid y=2)$를 구하라.
3. 앞 사후분포를 이용하여 $f_*\mid y=2$의 평균·분산과 분포를 구하라.
4. $y_*\mid y=2$의 평균·분산과 분포를 구하라. (c)에 비해 분산이 늘어나는 이유를 설명하라.

<details><summary>원문 보기</summary>

#### One Observation, Posterior, and Prediction

Let $\theta\sim\mathcal N(0,1)$ and $y=\theta+\epsilon$, with $\epsilon\sim\mathcal N(0,1)$ independent of $\theta$. Observe $y=2$. At a new input the noise-free value is $f_*=2\theta$ and the observation is $y_*=2\theta+\epsilon_*$, where $\epsilon_*\sim\mathcal N(0,1)$ is independent of $\theta,\epsilon$. You may use the affine-transformation and independent-sum rules for Gaussians.

1. Use the noise model to write the likelihood $p(y=2\mid\theta)$. Here likelihood means the density evaluated at the observed value.
2. Multiply likelihood and prior, complete the square, and obtain the normalized posterior $p(\theta\mid y=2)$.
3. Use that posterior to find the mean, variance, and distribution of $f_*\mid y=2$.
4. Find the mean, variance, and distribution of $y_*\mid y=2$. Explain why its variance exceeds that in (c).

</details>

#### 문제를 내 말로 읽어요

관측 하나로 스칼라 $\theta$의 분포를 갱신한 뒤, 그 분포 전체를 이용해 새 값을 예측해요. $f_*$에는 새 잡음이 없고 $y_*$에는 새 잡음이 있어요. 둘째 인수는 항상 분산이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“잡음모델”에서 입력과 계수를 고정하면 출력 평균이 정해져 likelihood를 쓸 수 있어요. Gaussian prior와 likelihood의 곱은 완전제곱으로 Gaussian posterior가 돼요. “$f_*=2\theta$”에는 아핀 변환 공식 $E[aX]=aE[X]$, $\operatorname{Var}(aX)=a^2\operatorname{Var}(X)$를 적용해요. “독립인 새 잡음”이 더해지면 평균과 분산을 각각 더해요. 사용할 것은 prior 분산 1이 아니라 데이터를 반영한 posterior 분산이에요.

#### 종이에 쓰는 첫 줄

$$
y\mid\theta\sim\mathcal N(\theta,1),\qquad p(y=2\mid\theta)=\frac1{\sqrt{2\pi}}e^{-(2-\theta)^2/2}.
$$

출력에 고정된 $\theta$를 더해 평균이 이동해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$y=\theta+\epsilon$에서 $\theta$를 고정하면 $y$의 평균은 $\theta$, 분산은 1이에요. 관측값 2를 대입하면

$$
p(y=2\mid\theta)=\mathcal N(2\mid\theta,1)=\frac1{\sqrt{2\pi}}e^{-(2-\theta)^2/2}.
$$

이는 점확률 $P(y=2\mid\theta)$가 아닌 밀도값이에요.

#### (b)

prior까지 곱하면

$$
g(\theta)=\frac1{2\pi}e^{-\{(2-\theta)^2+\theta^2\}/2}.
$$

완전제곱은 $(2-\theta)^2+\theta^2=2(\theta-1)^2+2$예요. 따라서 모양은 $e^{-(\theta-1)^2}$이고 분산은 $1/2$예요. 적분 $\int e^{-(\theta-1)^2}d\theta=\sqrt\pi$로 정규화하면

$$
p(\theta\mid y=2)=\frac1{\sqrt\pi}e^{-(\theta-1)^2},\qquad \theta\mid y=2\sim\mathcal N(1,1/2).
$$

#### (c)

공식에 (b)의 값을 대입해요.

$$
E[f_*\mid y=2]=2\cdot1=2,
$$

$$
\operatorname{Var}(f_*\mid y=2)=2^2\cdot\frac12=2.
$$

Gaussian의 선형변환도 Gaussian이므로 $f_*\mid y=2\sim\mathcal N(2,2)$예요.

#### (d)

새 잡음은 관측과 모수로부터 독립이라 조건을 둔 뒤에도 더할 수 있어요.

$$
E[y_*\mid y=2]=2+0=2,
$$

$$
\operatorname{Var}(y_*\mid y=2)=2+1=3.
$$

따라서 $y_*\mid y=2\sim\mathcal N(2,3)$예요. 분산 차이 1은 새로운 관측잡음의 불확실성이에요.

#### 완성 답과 검산

#### (a) 검산

잔차 $2-\theta$를 평균 0·분산1 잡음 밀도에 넣으면 같은 식이에요. 계수 2가 아니라 관측값 2인 점도 확인해요.

#### (b) 검산

정규화 계수 $1/\sqrt\pi$와 적분 $\sqrt\pi$의 곱은 1이에요. precision도 prior 1+관측 1=2여서 분산 $1/2$와 맞아요.

#### (c) 검산

상수배는 분산에 제곱으로 들어가므로 $4\cdot1/2=2$예요. 분포의 평균 2와 분산 2는 서로 다른 역할이에요.

#### (d) 검산

새 잡음 평균이 0이라 예측 평균은 그대로이고 분산만 1 증가해요. MAP $\theta=1$에 고정했다면 분산 1만 남지만 여기서는 모수 불확실성에서 전파된 분산 2도 포함해요.

#### 여기서 헷갈리기 쉬워요

잠재값 $f_*$에 관측잡음 1을 미리 더하지 않아요. $\operatorname{Var}(2\theta)$를 $2\operatorname{Var}(\theta)$로 계산하지 말고 계수를 제곱해요. (c),(d)의 공식 적용을 위해 posterior를 다시 유도할 필요는 없어요.

#### 설명을 닫고 다시 풀어요

- likelihood의 관측값과 모수를 구분해 써요.
- posterior로 잠재분산을 계산하고 마지막에 새 잡음을 더해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\theta\mid y=2\sim\mathcal N(1,1/2)$. $f_*\mid y=2\sim\mathcal N(2,2)$, $y_*\mid y=2\sim\mathcal N(2,3)$. 분산 차이는 새 잡음1.

#### 적용 조건

분산표기; 새 잡음은 θ와 관측잡음에 독립; 모수와 잡음의 불확실성 구별

#### 출제 근거

MML 9.3.3-9.3.4; Lecture04 p14의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF 312, 314, 315쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **사후예측 (posterior predictive)** — 사후 모수 불확실성을 반영한 새 출력 분포예요. 이 문제에서는 $2\theta$의 분산과 새 잡음분산을 함께 포함해요.
- **잠재값 (latent function value)** — 새 관측잡음을 더하기 전 함수값이에요. 이 문제의 $f_*=2\theta$는 posterior로부터 분산 2를 가져요.

---

<a id="p9"></a>

### 9. 0을 관측했을 때의 모델 비교

EXAM Problem 9 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p9)

#### 주어진 조건

두 모델은 $M_0:y=\epsilon$, $M_1:y=\theta+\epsilon$이다. 두 모델의 잡음은 $\epsilon\sim\mathcal N(0,1)$이고, $M_1$에서는 독립인 prior $\theta\sim\mathcal N(0,3)$를 사용한다. 모델 사전확률은 각각 $1/2$이고 관측은 스칼라 $y=0$ 하나이다. Gaussian 독립합 성질을 사용해도 된다. Bayes factor의 방향은 $B_{01}=p(y=0\mid M_0)/p(y=0\mid M_1)$이다.

#### 구할 것

1. 각 모델의 주변분포 $p(y\mid M_i)$를 구하라. $M_1$에서는 prior를 평균낸다는 뜻을 적분식과 독립합의 분산으로 설명하라.
2. 각 주변밀도를 관측 $y=0$에서 평가하여 evidence를 구하라.
3. $B_{01}$을 계산하고 어느 모델에 유리한지 설명하라.
4. posterior odds와 $P(M_0\mid y=0)$를 구하라. 연속형 데이터의 evidence를 점확률 0으로 놓으면 안 되는 이유도 설명하라.

<details><summary>원문 보기</summary>

#### Model Comparison after Observing Zero

Consider $M_0:y=\epsilon$ and $M_1:y=\theta+\epsilon$. In both models $\epsilon\sim\mathcal N(0,1)$. Under $M_1$, use the independent prior $\theta\sim\mathcal N(0,3)$. Both models have prior probability $1/2$. The data consist of one scalar observation $y=0$. You may use the independent-sum property of Gaussians. Define $B_{01}=p(y=0\mid M_0)/p(y=0\mid M_1)$.

1. Find the marginal distribution $p(y\mid M_i)$ under each model. Under $M_1$, explain averaging over the prior using an integral and the variance of an independent sum.
2. Evaluate each marginal density at $y=0$ to obtain the evidences.
3. Compute $B_{01}$ and state which model it favors.
4. Find the posterior odds and $P(M_0\mid y=0)$. Explain why the evidence for continuous data must not be replaced by a zero point probability.

</details>

#### 문제를 내 말로 읽어요

이번에는 계수 하나의 최적값을 고르는 대신 두 모델을 비교해요. $M_0$에는 적분할 계수가 없고, $M_1$에는 prior 전체로 평균낼 계수가 있어요. 마지막에 모델 prior를 곱해 사후확률로 바꿔요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“모델 비교”는 evidence(주변우도)를 떠올리는 단서예요. $p(y\mid M_1)=\int p(y\mid\theta,M_1)p(\theta\mid M_1)d\theta$는 prior로 likelihood를 평균낸 밀도예요. 독립 Gaussian의 합은 평균끼리·분산끼리 더하므로 어려운 적분 대신 주변분포를 찾을 수 있어요. Bayes factor $B_{01}$는 두 evidence의 비, posterior odds는 $B_{01}$에 prior odds $P(M_0)/P(M_1)$를 곱한 값이에요. 여기서는 두 모델의 prior가 같아요.

#### 종이에 쓰는 첫 줄

$$
M_0:y=\epsilon,\qquad M_1:y=\theta+\epsilon.
$$

먼저 관측값 0을 대입하기 전 각각의 주변분포부터 적어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$M_0$에서는 $y\sim\mathcal N(0,1)$이에요. $M_1$에서는

$$
p(y\mid M_1)=\int\mathcal N(y\mid\theta,1)\mathcal N(\theta\mid0,3)d\theta.
$$

독립인 두 Gaussian의 합이라 평균은 $0+0=0$, 분산은 $3+1=4$예요. 따라서 $p(y\mid M_1)=\mathcal N(y\mid0,4)$예요. 이는 특정 $\theta$를 선택하는 대신 prior의 모든 값으로 평균낸 결과예요.

#### (b)

관측 $y=0$을 두 밀도에 대입해요.

$$
p(0\mid M_0)=\frac1{\sqrt{2\pi}},\qquad p(0\mid M_1)=\frac1{\sqrt{8\pi}}.
$$

평균에서 평가하므로 지수항은 둘 다 1이에요.

#### (c)

$$
B_{01}=\frac{1/\sqrt{2\pi}}{1/\sqrt{8\pi}}=2.
$$

데이터가 $M_0$에 부여하는 밀도가 두 배라 $M_0$에 유리해요. evidence만의 비교와 모델 사후확률은 구분해요.

#### (d)

Bayes 식의 공통 분모 $p(y)$를 약분하면

$$
\frac{P(M_0\mid y)}{P(M_1\mid y)}=\frac{P(M_0)}{P(M_1)}\frac{p(y\mid M_0)}{p(y\mid M_1)}.
$$

prior odds가 1이므로 posterior odds는 $2:1$이에요. 두 사후확률의 합이 1이라 $P(M_0\mid0)=2/3$, $P(M_1\mid0)=1/3$이에요. 연속형 y는 점확률이 0이지만 밀도는 0이 아니에요. 여기서 관측 자료의 likelihood/evidence로 쓰는 것은 밀도값이므로 점확률로 바꾸어 $0/0$을 만들지 않아요.

#### 완성 답과 검산

#### (a) 검산

$\operatorname{Var}(\theta+\epsilon)=3+1+2\operatorname{Cov}(\theta,\epsilon)=4$예요. 독립이라 공분산이 0인 조건을 사용했어요.

#### (b) 검산

표준편차는 각각 1과 2라 평균 위치에서의 높이가 $1:1/2$예요. 두 밀도는 각각 전체 적분 1을 유지해요.

#### (c) 검산

$p(0\mid M_0)=2p(0\mid M_1)$이므로 비의 방향 $01$과 값 2가 맞아요.

#### (d) 검산

정규화 전 가중치는 $(1/2)/\sqrt{2\pi}$와 $(1/2)/\sqrt{8\pi}$예요. 합으로 나누면 $2/3,1/3$이고 두 값의 합이 1이에요.

#### 여기서 헷갈리기 쉬워요

prior가 아닌 posterior로 evidence를 평균내면 관측을 반영하는 단계가 달라져요. $B_{01}=2$를 $P(M_0\mid y)=2$로 해석하지 않아요. odds를 확률로 바꾸는 정규화가 필요해요.

#### 설명을 닫고 다시 풀어요

- 두 주변분포를 먼저 정하고 관측점에서 밀도를 계산해요.
- Bayes factor의 방향과 모델 prior를 확인해 사후확률로 바꿔요.

**페이지 요약**

#### 떠올릴 개념·공식

$M_0:y\sim\mathcal N(0,1)$, $M_1:y\sim\mathcal N(0,4)$. $B_{01}=2$, 같은 모델prior→posterior odds $2:1$, $P(M_0\mid0)=2/3$.

#### 적용 조건

모델prior각1/2; M0 모수없음; M1 prior분산3; evidence는 밀도값

#### 출제 근거

Lecture04 p17; MML 9.3.3,9.3.4의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF 312, 319쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **Evidence (marginal likelihood)** — 모델이 관측 데이터에 부여하는 밀도예요. $M_1$에서는 prior로 모수를 적분하고, $M_0$에서는 모수가 없어 잡음밀도를 그대로 써요.
- **Bayes factor** — 모델 evidence의 비예요. 이 문제는 방향을 $01$로 정했으므로 값 2는 $M_0$에 유리해요.
- **Posterior odds** — 두 모델 사후확률의 비예요. prior odds에 Bayes factor를 곱하며 이 문제에서는 $2:1$이에요.

---

<a id="p10"></a>

### 10. 한 직선으로의 직교투영

EXAM Problem 10 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p10)

#### 주어진 조건

$b=(1,1,0)^\top$, $y=(2,0,1)^\top$이고 $\hat y=b\theta$로 근사한다. 내적은 Euclidean 내적이다. 확률 해석에서는 $y=b\theta+\epsilon$, $\epsilon\sim\mathcal N(0,I_3)$을 사용한다.

#### 구할 것

1. 오차벡터 $y-b\theta$가 $b$에 수직이라는 조건에서 $\hat\theta$를 구하라.
2. $\hat y=b\hat\theta$와 적합 잔차 $r=y-\hat y$를 구하고 $b^\top r=0$을 직접 확인하라.
3. $\hat y=Py$를 만족하는 직교투영행렬 $P$를 구하라. $P^\top=P$, $P^2=P$를 확인하라.
4. 임의의 $\theta$에 대해 $\|y-b\theta\|^2=\|r\|^2+(\theta-\hat\theta)^2\|b\|^2$임을 설명하라. 최소 제곱오차를 구하고 이 해가 ML인 이유를 설명하라.

<details><summary>원문 보기</summary>

#### Orthogonal Projection onto a Line

Let $b=(1,1,0)^\top$ and $y=(2,0,1)^\top$, and approximate $y$ by $\hat y=b\theta$. Use the Euclidean inner product. For the probabilistic interpretation, use $y=b\theta+\epsilon$ with $\epsilon\sim\mathcal N(0,I_3)$.

1. Find $\hat\theta$ by requiring the error vector $y-b\theta$ to be orthogonal to $b$.
2. Find $\hat y=b\hat\theta$ and the fitted residual $r=y-\hat y$, and directly verify $b^\top r=0$.
3. Find the orthogonal projection matrix $P$ satisfying $\hat y=Py$. Check $P^\top=P$ and $P^2=P$.
4. Explain why $\|y-b\theta\|^2=\|r\|^2+(\theta-\hat\theta)^2\|b\|^2$ for every $\theta$. Find the minimum squared error and explain why this solution is ML.

</details>

#### 문제를 내 말로 읽어요

3차원 벡터를 $b$ 방향의 직선 위로 내려놓아요. 계수 $\hat\theta$는 스칼라지만 투영 $\hat y$와 잔차 $r$은 원래와 같은 $3\times1$ 벡터예요. 직교조건을 세운 뒤 실제로 거리 최소까지 확인해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“잔차가 $b$에 수직”은 내적 $b^\top(y-b\theta)=0$을 쓰라는 단서예요. $b\ne0$이므로 $b^\top b>0$이고 계수는 $\hat\theta=(b^\top y)/(b^\top b)$예요. 이를 $b\hat\theta$에 대입하면 투영행렬(projection matrix) $P=bb^\top/(b^\top b)$가 나와요. 직교한 두 벡터의 제곱노름은 더해지므로 잔차와 직선방향의 차이를 나누면 전역 최소거리를 증명할 수 있어요. Gaussian 동일분산 잡음의 ML은 이 제곱거리를 최소화해요.

#### 종이에 쓰는 첫 줄

$$
b^\top(y-b\theta)=b^\top y-(b^\top b)\theta=0.
$$

먼저 두 내적을 계산해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$b^\top y=2$, $b^\top b=2$이므로 $2-2\theta=0$이에요. 따라서 $\hat\theta=1$이에요.

#### (b)

$$
\hat y=b\hat\theta=\begin{pmatrix}1\\1\\0\end{pmatrix},\qquad r=y-\hat y=\begin{pmatrix}1\\-1\\1\end{pmatrix}.
$$

$b^\top r=1-1+0=0$이라 직교해요.

#### (c)

$\hat y=b(b^\top y)/(b^\top b)$에서

$$
P=\frac{bb^\top}{b^\top b}=\frac12\begin{pmatrix}1&1&0\\1&1&0\\0&0&0\end{pmatrix}\in\mathbb R^{3\times3}.
$$

$bb^\top$가 대칭이므로 $P^\top=P$예요. 또한

$$
P^2=\frac{b(b^\top b)b^\top}{(b^\top b)^2}=\frac{bb^\top}{b^\top b}=P.
$$

#### (d)

임의의 $\theta$에 대해 $y-b\theta=r+b(\hat\theta-\theta)$예요. $r^\top b=0$이라 제곱노름을 펼친 교차항이 사라져요. 따라서

$$
\|y-b\theta\|^2=\|r\|^2+(\theta-\hat\theta)^2\|b\|^2=3+2(\theta-1)^2.
$$

최소 제곱오차는 3이고 $\theta=1$에서만 달성돼요. 알려진 Gaussian 잡음분산 1에서 NLL은 $\frac32\log(2\pi)+\frac12\|y-b\theta\|^2$이므로 같은 해가 ML이에요.

#### 완성 답과 검산

#### (a) 검산

$b^\top b=2>0$이므로 나눗셈이 가능하고 계수 해가 유일해요.

#### (b) 검산

$\hat y+r=(2,0,1)^\top=y$예요. 잔차를 직선 방향과 내적하면 정확히 0이에요.

#### (c) 검산

$Py=(1,1,0)^\top$로 (b)와 같아요. $Pb=b$이고 마지막 좌표를 0으로 보내 직선 위의 벡터를 보존해요. 대칭·멱등은 (c)의 행렬곱 계산으로 모든 입력에 대해 성립해요.

#### (d) 검산

직접 성분 전개한 $(2-\theta)^2+\theta^2+1=2\theta^2-4\theta+5$도 $3+2(\theta-1)^2$와 같아요. 모든 실수 $\theta$에서 추가항이 0 이상이라 일부 수치 예만으로 최소라고 판단하지 않았어요.

#### 여기서 헷갈리기 쉬워요

계수 $\hat\theta=1$을 투영벡터라고 부르지 않아요. $P$도 $3\times3$이에요. $P^\top=P^2=P$는 각 행렬이 같다는 뜻이고 모든 항등행렬이 된다는 뜻은 아니에요.

#### 설명을 닫고 다시 풀어요

- 잔차 직교조건 하나로 계수와 투영을 구해요.
- 교차항 0에서 거리분해와 ML의 연결까지 설명해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\hat\theta=1$, $\hat y=(1,1,0)^\top$, $r=(1,-1,1)^\top$. $P=bb^\top/2$. 오차 $3+2(\theta-1)^2$→유일 ML, 최소3.

#### 적용 조건

유클리드내적; b≠0; 알려진 동일 Gaussian 잡음분산1

#### 출제 근거

MML 3.8,9.4; Lecture04 p20,p24의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF 319, 320쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **직교투영 (orthogonal projection)** — 부분공간 위에서 원래 벡터에 가장 가까운 벡터예요. 이 문제에서는 $y$를 $\operatorname{span}(b)$ 위의 $b\hat\theta$로 보내요.
- **멱등 (idempotent)** — $P^2=P$라는 성질이에요. 한 번 투영한 결과를 다시 투영해도 같아요. 이 문제의 P는 대칭이기도 해서 직교투영행렬이에요.

---

원 문제·정리노트·PDF는 보존해요.
