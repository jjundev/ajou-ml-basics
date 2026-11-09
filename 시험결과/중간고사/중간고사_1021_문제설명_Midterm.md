# 머신러닝기초 중간고사 1021 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [Q1. 기울기와 야코비안](#p1)
  - [Q2. 행렬 연산과 직교 사영](#p2)
  - [Q3. 가우시안 확률밀도](#p3)
  - [Q4. 결합확률과 조건부확률](#p4)
  - [Q5. 베이즈 추론과 예측](#p5)
  - [Q6. 최대우도와 MAP 선형회귀](#p6)
  - [Q7. 공분산과 교차공분산 행렬](#p7)
  - [Q8. 가우시안 밀도의 곱](#p8)
  - [Q9. 베이즈 선형회귀: 파라미터 사후분포](#p9)
  - [Q10. 베이즈 선형회귀: 예측분포](#p10)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### Q1. 기울기와 야코비안

Midterm 1021 Q1 · [원 문제 보기](%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC_1021_Midterm.html#p1)

#### 주어진 조건

모든 벡터와 gradient는 열벡터이고, 야코비안은 $(\mathbf J_{\mathbf g})_{ij}=\partial g_i/\partial x_j$로 정의해요.

#### 구할 것

다음을 구해 보세요.

- (a) $f(u,v)=2u^2-2uv+4v^2+6u-2v$의 열 gradient $\nabla f(u,v)$를 구하고 $(u,v)=(-1,2)$에서 값을 구하세요.
- (b) $\mathbf g(u,v)=\begin{pmatrix}u^2+2v\\ uv-v^2\\ 3u-v\end{pmatrix}$의 야코비안 $\mathbf J_{\mathbf g}(u,v)$를 구하고 $(-1,2)$에서 값을 구하세요. 크기(차원)도 쓰세요.

<details><summary>원문 보기</summary>

"

(a) For $f(u,v)=2u^2-2uv+4v^2+6u-2v$, find the column gradient $\nabla f(u,v)$ and evaluate it at $(u,v)=(-1,2)$.

(b) For the vector-valued function $\mathbf g(u,v)=\begin{pmatrix}u^2+2v\\ uv-v^2\\ 3u-v\end{pmatrix}$, find the Jacobian $\mathbf J_{\mathbf g}(u,v)$ and evaluate it at $(-1,2)$. State its dimensions.

"

![Q1 시험지 스캔](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_exam1021_Midterm/fa26ef6c2ff73519-q1.webp)

</details>

#### 무엇을 구하는 문제인가요?

(a)는 스칼라 함수 $f(u,v)$를 두 변수로 각각 미분해 **열벡터**로 세우고, $(-1,2)$에서 값을 구해요. (b)는 출력이 3개인 벡터함수 $\mathbf g$의 편미분 6개를 표로 배치한 야코비안(Jacobian)과 그 크기를 구해요.

이 시험은 지시문에서 "All vectors and gradients are column vectors"라고 열 관례를 정했어요. 강의 정리노트는 스칼라 미분을 행벡터(편미분을 가로로 모은 것)로 쓰지만, 이 문항은 원문 조건대로 열벡터로 답해요. 두 표기는 전치 관계 $\nabla f=(\partial f/\partial(u,v))^\top$일 뿐 값은 같아요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

**(a)의 단서:** "column gradient"는 편미분 $\partial f/\partial u$, $\partial f/\partial v$를 세로로 쌓은 벡터예요.

$$
\nabla f(u,v)=\begin{bmatrix}\partial f/\partial u\\ \partial f/\partial v\end{bmatrix}\in\mathbb R^{2\times1}.
$$

편미분은 다른 변수를 상수로 보고 미분해요. 그래서 교차항 $-2uv$는 $u$로 미분하면 $-2v$, $v$로 미분하면 $-2u$가 돼요.

**(b)의 단서:** 지시문의 $(\mathbf J_{\mathbf g})_{ij}=\partial g_i/\partial x_j$는 "$i$행 = $i$번째 출력, $j$열 = $j$번째 입력"이라는 뜻이에요. 출력 $m$개, 입력 $d$개이면 야코비안은 **출력×입력** $m\times d$예요. 여기서는 $m=3$, $d=2$라서 $3\times2$이고, 각 행은 $g_i$ 하나의 편미분을 가로로 놓은 거예요.

"State its dimensions"처럼 문제에 적힌 요구는 계산과 별개로 답안에 따로 써야 해요.

#### 종이에 쓸 첫 줄

(a)는 $\partial f/\partial u=4u-2v+6$부터 써요. (b)는 빈 $3\times2$ 표를 그리고 1행에 $g_1=u^2+2v$의 $(\partial/\partial u,\ \partial/\partial v)=(2u,\ 2)$를 채우며 시작해요.

#### 한 단계씩 계산해요

#### (a)

항마다 미분해요. $2u^2\to4u$, $-2uv\to-2v$, $6u\to6$이라 $\partial f/\partial u=4u-2v+6$이에요. $4v^2\to8v$, $-2uv\to-2u$, $-2v\to-2$라 $\partial f/\partial v=-2u+8v-2$예요.

$$
\nabla f(u,v)=\begin{bmatrix}4u-2v+6\\-2u+8v-2\end{bmatrix},\qquad \nabla f(-1,2)=\begin{bmatrix}-4-4+6\\2+16-2\end{bmatrix}=\begin{bmatrix}-2\\16\end{bmatrix}.
$$

#### (b)

행마다 한 출력을 미분해요. $g_1=u^2+2v$는 $(2u,\ 2)$, $g_2=uv-v^2$는 $(v,\ u-2v)$, $g_3=3u-v$는 $(3,\ -1)$이에요.

$$
\mathbf J_{\mathbf g}(u,v)=\begin{bmatrix}2u&2\\ v&u-2v\\ 3&-1\end{bmatrix}.
$$

$(u,v)=(-1,2)$를 넣어요. $2u=-2$, $v=2$, $u-2v=-1-4=-5$이고 3행은 상수라 그대로예요.

$$
\mathbf J_{\mathbf g}(-1,2)=\begin{bmatrix}-2&2\\ 2&-5\\ 3&-1\end{bmatrix},\qquad 3\times2.
$$

**완성 답**<br>(a) $\nabla f(-1,2)=(-2,16)^\top$ (b) $\mathbf J_{\mathbf g}(-1,2)=\begin{bmatrix}-2&2\\2&-5\\3&-1\end{bmatrix}$, 크기 $3\times2$

#### 다른 길로 검산해요

#### (a) 검산

$f$를 이차형식으로 쓰면 $f=\tfrac12\mathbf x^\top\begin{bmatrix}4&-2\\-2&8\end{bmatrix}\mathbf x+(6,-2)\mathbf x$ ($\mathbf x=(u,v)^\top$)이에요. 열 gradient는 $\begin{bmatrix}4&-2\\-2&8\end{bmatrix}\mathbf x+(6,-2)^\top$이고, $(-1,2)$에서 $(-4-4+6,\ 2+16-2)^\top=(-2,16)^\top$으로 같아요.

#### (b) 검산

작은 이동으로 확인해요. $(u,v)=(-1,2)$에서 $v$만 $h$ 늘리면 $g_2=uv-v^2$는 $-2-4=-6$에서 대략 $-6+(-5)h$로 변해요(정확히 $-(2+h)-(2+h)^2=-6-5h-h^2$). 그래서 (2,2) 성분은 $-5$가 맞아요. $g_3=3u-v$는 $v$가 늘면 줄어드니 (3,2) 성분은 $-1$이에요. 표의 크기는 출력 3행 × 입력 2열이에요.

#### 이 부분을 조심해요

대입 단계의 부호 실수가 가장 흔해요. $u-2v$에 $u=-1,v=2$를 넣으면 $-1-4=-5$이고, 상수 성분 $-1$은 대입해도 그대로 $-1$이에요. 일반형을 맞게 써 놓고 숫자를 옮겨 적을 때 틀리기 쉬우니 성분마다 다시 확인해요.

"State its dimensions" 같은 짧은 요구를 빠뜨리지 않아요. 계산이 다 맞아도 요구 항목이 없으면 감점돼요. 야코비안을 입력×출력 $2\times3$으로 뒤집어 쓰지 않는 것도 확인해요.

#### 혼자 다시 풀어봐요

1. 지시문의 $(\mathbf J_{\mathbf g})_{ij}=\partial g_i/\partial x_j$를 보고 행·열이 무엇인지 말해요.
2. $\mathbf J_{\mathbf g}(u,v)$를 쓰고 $(-1,2)$를 성분마다 대입한 뒤 한 번 더 대입해 확인해요.
3. 답 끝에 크기 $3\times2$를 적었는지 문제 문장과 대조해요.

**페이지 요약**

#### 떠올릴 개념·공식

이 시험은 열 gradient $\nabla f=(\partial f/\partial u,\partial f/\partial v)^\top$를 써요(강의의 행 표기의 전치). 야코비안은 $(\mathbf J_{\mathbf g})_{ij}=\partial g_i/\partial x_j$, 출력×입력 $3\times2$예요.

#### 첫 줄

(a) $\partial f/\partial u=4u-2v+6$ (b) 1행 $(2u,\ 2)$부터 채워요.

#### 핵심 주의점

$u-2v$에 대입하면 $-5$, 상수 $-1$은 그대로예요. "State its dimensions"를 답에 써요.

#### 답

(a) $(-2,16)^\top$ (b) $\begin{bmatrix}-2&2\\2&-5\\3&-1\end{bmatrix}$, $3\times2$

#### 다시 볼 자료

[0928 그래디언트](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/0928/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_0928_Linear_Regression.html#s0-gradient), [0928 자코비안](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/0928/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_0928_Linear_Regression.html#s0-jacobian)

#### 용어

- **편미분(partial derivative)** — 다른 변수는 상수로 두고 한 변수로만 미분한 값이에요.
- **열 gradient(column gradient)** — 스칼라 함수의 편미분을 세로로 쌓은 $d\times1$ 벡터예요. 이 시험의 지정 관례예요.
- **야코비안(Jacobian)** — 벡터함수 $\mathbf g:\mathbb R^d\to\mathbb R^m$의 편미분 표 $(\mathbf J_{\mathbf g})_{ij}=\partial g_i/\partial x_j$, 크기 $m\times d$예요.

---

<a id="p2"></a>

### Q2. 행렬 연산과 직교 사영

Midterm 1021 Q2 · [원 문제 보기](%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC_1021_Midterm.html#p2)

#### 주어진 조건

$A=\begin{pmatrix}1&1\\1&0\\0&1\end{pmatrix}$, $\mathbf y=\begin{pmatrix}3\\0\\0\end{pmatrix}$이에요.

#### 구할 것

다음을 구해 보세요.

- (a) $A^\top A$와 그 행렬식, 역행렬을 구하세요.
- (b) $\mathbf y$를 $A$의 열공간에 직교 사영한 $\mathbf p=A(A^\top A)^{-1}A^\top\mathbf y$와 $\mathbf r=\mathbf y-\mathbf p$를 구하고, $\mathbf r$이 $A$의 두 열과 직교함을 확인하세요.

<details><summary>원문 보기</summary>

"Let $A=\begin{pmatrix}1&1\\1&0\\0&1\end{pmatrix}$, $\mathbf y=\begin{pmatrix}3\\0\\0\end{pmatrix}$.

(a) Compute $A^\top A$, its determinant, and its inverse.

(b) The orthogonal projection of $\mathbf y$ onto the column space of $A$ is $\mathbf p=A(A^\top A)^{-1}A^\top\mathbf y$. Compute $\mathbf p$ and $\mathbf r=\mathbf y-\mathbf p$. Verify that $\mathbf r$ is orthogonal to both columns of $A$.

"

![Q2 시험지 스캔](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_exam1021_Midterm/743661a4aaa0782b-q2.webp)

</details>

#### 무엇을 구하는 문제인가요?

$A$는 $3\times2$, $\mathbf y$는 3차원 벡터예요. (a)는 $2\times2$ 행렬 $A^\top A$와 그 행렬식·역행렬을 구해요. (b)는 $\mathbf y$를 $A$의 두 열이 만드는 평면(열공간)에 수직으로 떨어뜨린 점 $\mathbf p$와 남는 부분 $\mathbf r$을 구하고, $\mathbf r$이 그 평면에 수직인지 확인해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

**(a)의 단서:** $2\times2$ 행렬 $\begin{bmatrix}a&b\\c&d\end{bmatrix}$의 행렬식은 $ad-bc$, 역행렬은 $\frac{1}{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}$예요. 행렬식이 0이 아니어야 역행렬이 있어요. $A^\top A$의 $(i,j)$ 성분은 $A$의 $i$열과 $j$열의 내적이라 대칭이에요.

**(b)의 단서:** "orthogonal projection onto the column space"는 최소제곱(least squares)과 같은 그림이에요. 계수 $\hat{\boldsymbol\beta}=(A^\top A)^{-1}A^\top\mathbf y$를 먼저 구하면 $\mathbf p=A\hat{\boldsymbol\beta}$예요. 잔차 $\mathbf r=\mathbf y-\mathbf p$는 열공간과 직교해서 $A^\top\mathbf r=\mathbf 0$이 성립해요. "both columns와 직교"는 이 식의 두 성분이 모두 0이라는 뜻이에요.

#### 종이에 쓸 첫 줄

(a)는 $A^\top=\begin{bmatrix}1&1&0\\1&0&1\end{bmatrix}$을 쓰고 열끼리 내적해 $A^\top A$를 채워요. (b)는 $A^\top\mathbf y=(3,3)^\top$부터 계산해요.

#### 한 단계씩 계산해요

#### (a)

1열 $(1,1,0)$, 2열 $(1,0,1)$의 내적을 모아요. 1열·1열 $=2$, 1열·2열 $=1$, 2열·2열 $=2$예요.

$$
A^\top A=\begin{bmatrix}2&1\\1&2\end{bmatrix},\qquad \det(A^\top A)=4-1=3.
$$

$$
(A^\top A)^{-1}=\frac13\begin{bmatrix}2&-1\\-1&2\end{bmatrix}=\begin{bmatrix}2/3&-1/3\\-1/3&2/3\end{bmatrix}.
$$

#### (b)

$A^\top\mathbf y=(1\cdot3,\ 1\cdot3)^\top=(3,3)^\top$, 계수 $\hat{\boldsymbol\beta}=(A^\top A)^{-1}(3,3)^\top=(1,1)^\top$이에요.

$$
\mathbf p=A\hat{\boldsymbol\beta}=\begin{bmatrix}2\\1\\1\end{bmatrix},\qquad \mathbf r=\mathbf y-\mathbf p=\begin{bmatrix}1\\-1\\-1\end{bmatrix}.
$$

직교 확인: 1열과 내적 $1-1+0=0$, 2열과 내적 $1+0-1=0$이라 $A^\top\mathbf r=\mathbf 0$이에요.

**완성 답**<br>(a) $A^\top A=\begin{bmatrix}2&1\\1&2\end{bmatrix}$, $\det=3$, $(A^\top A)^{-1}=\frac13\begin{bmatrix}2&-1\\-1&2\end{bmatrix}$ (b) $\mathbf p=(2,1,1)^\top$, $\mathbf r=(1,-1,-1)^\top$, $A^\top\mathbf r=\mathbf 0$

#### 다른 길로 검산해요

#### (a) 검산

$\begin{bmatrix}2&1\\1&2\end{bmatrix}\cdot\frac13\begin{bmatrix}2&-1\\-1&2\end{bmatrix}=\frac13\begin{bmatrix}3&0\\0&3\end{bmatrix}=I$라 역행렬이 맞아요.

#### (b) 검산

피타고라스로 확인해요. $\|\mathbf y\|^2=9$, $\|\mathbf p\|^2=4+1+1=6$, $\|\mathbf r\|^2=1+1+1=3$이고 $6+3=9$예요. $\mathbf p$가 정말 열공간 안에 있는지도 봐요: $\mathbf p=1\cdot(1,1,0)^\top+1\cdot(1,0,1)^\top$이에요.

#### 이 부분을 조심해요

$A$는 정사각행렬이 아니라서 $A^{-1}$이 없어요. $\mathbf p=A(A^\top A)^{-1}A^\top\mathbf y$를 $A A^{-1}(A^\top)^{-1}A^\top\mathbf y=\mathbf y$처럼 줄이면 안 돼요. 직교 확인은 "$\mathbf r^\top A=[0\ 0]$"처럼 두 열 모두에 대해 보여야 해요.

#### 혼자 다시 풀어봐요

1. $A^\top A$의 각 성분이 어떤 두 열의 내적인지 말하며 채워요.
2. 계수 $\hat{\boldsymbol\beta}$를 먼저 구한 뒤 $\mathbf p=A\hat{\boldsymbol\beta}$로 가는 순서를 써요.
3. $A^\top\mathbf r=\mathbf 0$과 $\|\mathbf p\|^2+\|\mathbf r\|^2=\|\mathbf y\|^2$로 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

$2\times2$ 역행렬은 $\frac1{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}$예요. 사영 $\mathbf p=A\hat{\boldsymbol\beta}$, $\hat{\boldsymbol\beta}=(A^\top A)^{-1}A^\top\mathbf y$, 잔차는 $A^\top\mathbf r=\mathbf 0$이에요.

#### 첫 줄

$A^\top\mathbf y=(3,3)^\top$부터 계산해요.

#### 핵심 주의점

$A$는 $3\times2$라 $A^{-1}$이 없어요. 직교는 두 열 모두 확인해요.

#### 답

(a) $\det=3$, 역행렬 $\frac13\begin{bmatrix}2&-1\\-1&2\end{bmatrix}$ (b) $\mathbf p=(2,1,1)^\top$, $\mathbf r=(1,-1,-1)^\top$

#### 다시 볼 자료

[1019 평면과 열공간](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1019/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1019_Prediction_and_Projection.html#s2-plane), [1019 회귀계수와 예측벡터](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1019/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1019_Prediction_and_Projection.html#s2-regression)

#### 용어

- **열공간(column space)** — $A$의 열들의 모든 선형결합 $\{A\boldsymbol\beta\}$이에요. 여기서는 $\mathbb R^3$ 안의 평면이에요.
- **직교 사영(orthogonal projection)** — $\mathbf y$에서 열공간까지 수직으로 내린 가장 가까운 점 $\mathbf p$예요.
- **잔차(residual)** — $\mathbf r=\mathbf y-\mathbf p$이고 열공간과 직교해 $A^\top\mathbf r=\mathbf 0$이에요.
- **행렬식(determinant)** — $2\times2$에서 $ad-bc$이고 0이 아니면 역행렬이 있어요.

---

<a id="p3"></a>

### Q3. 가우시안 확률밀도

Midterm 1021 Q3 · [원 문제 보기](%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC_1021_Midterm.html#p3)

#### 주어진 조건

$\mathcal N(\mu,v)$의 $v$는 분산이고, 다변량 정규분포의 둘째 인자는 공분산행렬이에요.

#### 구할 것

다음을 구해 보세요.

- (a) $\mathbf x=(x_1,x_2)^\top\sim\mathcal N\!\left(\begin{pmatrix}2\\-2\end{pmatrix},\begin{pmatrix}3&1\\1&1\end{pmatrix}\right)$의 결합밀도를 정규화 상수까지 명시해 쓰고, 이차식을 $(x_1-2)$와 $(x_2+2)$로 전개하세요.
- (b) $p(z)=c\exp\!\left[-\tfrac12(9z^2+18z+13)\right]$, $z\in\mathbb R$가 정규화된 밀도가 되도록 $c>0$을 정하고, 완전제곱을 보이며 평균과 분산을 밝히세요.

<details><summary>원문 보기</summary>

"

(a) A random vector $\mathbf x=(x_1,x_2)^\top$ has distribution $\mathbf x\sim\mathcal N\!\left(\begin{pmatrix}2\\-2\end{pmatrix},\begin{pmatrix}3&1\\1&1\end{pmatrix}\right)$. Write its joint density explicitly, including the normalizing constant. Expand the quadratic expression in terms of $(x_1-2)$ and $(x_2+2)$.

(b) Suppose $p(z)=c\exp\!\left[-\tfrac12(9z^2+18z+13)\right]$, $z\in\mathbb R$. Determine $c>0$ so that $p$ is a normalized probability density. Identify its mean and variance, showing your completion of the square.

"

![Q3 시험지 스캔](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_exam1021_Midterm/c488cf1b49fd7ef6-q3.webp)

</details>

#### 무엇을 구하는 문제인가요?

(a)는 2차원 가우시안의 밀도 공식을 숫자로 완전히 채워 쓰는 문제예요. 앞의 상수(정규화 상수)와 지수 안의 이차식을 $(x_1-2)$, $(x_2+2)$의 제곱·곱으로 정리해야 해요. (b)는 지수 안이 $z$의 이차식인 함수를 가우시안 모양으로 바꿔 넓이가 1이 되는 $c$를 찾고, 그 가우시안의 평균과 분산까지 말하는 문제예요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

**(a)의 단서:** "$\mathbf x\sim\mathcal N(\boldsymbol\mu,\Sigma)$의 joint density"는 다변량 정규분포 공식이에요.

$$
\begin{aligned}p(\mathbf x)&=\frac{1}{(2\pi)^{D/2}|\Sigma|^{1/2}}\\&\quad\times\exp\!\left(-\tfrac12\mathbf d^\top\Sigma^{-1}\mathbf d\right),\\ \mathbf d&=\mathbf x-\boldsymbol\mu.\end{aligned}
$$

$D$는 차원(여기서 2), $|\Sigma|$는 공분산행렬의 행렬식이에요. $D=2$이면 상수는 $\frac{1}{2\pi\sqrt{|\Sigma|}}$예요. 1차원 상수 $\frac1{\sqrt{2\pi v}}$의 $v$ 자리에 $|\Sigma|$를 넣어 $D$번 곱한 $\left(\frac1{\sqrt{2\pi|\Sigma|}}\right)^D$는 틀려요. 대각 $\Sigma=\mathrm{diag}(v_1,v_2)$라면 각자의 $v_i$로 만든 1차원 상수의 곱 $\frac1{\sqrt{2\pi v_1}}\cdot\frac1{\sqrt{2\pi v_2}}=\frac1{2\pi\sqrt{|\Sigma|}}$가 정답과 같아요.

**(b)의 단서:** "completion of the square"와 "normalized"는 렘마 "지수가 $-\tfrac12\lambda(z-m)^2$ 꼴이면 $\mathcal N(m,1/\lambda)$"을 떠올리게 해요. $\int e^{-\lambda(z-m)^2/2}dz=\sqrt{2\pi/\lambda}$를 써서 $c$를 정해요. 평균 $m$과 분산 $1/\lambda$는 같은 완전제곱 식에서 바로 읽혀요.

#### 종이에 쓸 첫 줄

(a)는 $|\Sigma|=3\cdot1-1\cdot1=2$와 $\Sigma^{-1}=\tfrac12\begin{bmatrix}1&-1\\-1&3\end{bmatrix}$부터 써요. (b)는 $9z^2+18z+13=9(z+1)^2+4$를 먼저 써요.

#### 한 단계씩 계산해요

#### (a)

$a=x_1-2$, $b=x_2+2$로 두면 $\mathbf x-\boldsymbol\mu=(a,b)^\top$예요.

$$
(\mathbf x-\boldsymbol\mu)^\top\Sigma^{-1}(\mathbf x-\boldsymbol\mu)=\tfrac12\,(a,b)\begin{bmatrix}1&-1\\-1&3\end{bmatrix}\begin{pmatrix}a\\b\end{pmatrix}=\tfrac12(a^2-2ab+3b^2).
$$

상수는 $\frac{1}{(2\pi)^{2/2}\sqrt2}=\frac{1}{2\sqrt2\,\pi}$예요.

$$
\begin{aligned}p(\mathbf x)&=\frac{1}{2\sqrt2\,\pi}\exp\!\left(-\tfrac14Q\right),\\ Q&=(x_1-2)^2-2(x_1-2)(x_2+2)\\&\quad+3(x_2+2)^2.\end{aligned}
$$

#### (b)

$9z^2+18z+13=9(z^2+2z+1)+4=9(z+1)^2+4$라서

$$
p(z)=c\,e^{-2}\exp\!\left(-\frac{(z+1)^2}{2\cdot\frac19}\right).
$$

넓이는 $c\,e^{-2}\sqrt{2\pi\cdot\tfrac19}=c\,e^{-2}\frac{\sqrt{2\pi}}{3}$이고 이것이 1이어야 해요. 그래서 $c=\frac{3e^2}{\sqrt{2\pi}}$예요.

정규화하면 $p(z)=\mathcal N(z\mid-1,\tfrac19)$라 평균은 $-1$, 분산은 $\tfrac19$예요.

**완성 답**<br>(a) $p(\mathbf x)=\frac{1}{2\sqrt2\,\pi}\exp\!\left(-\tfrac14[(x_1-2)^2-2(x_1-2)(x_2+2)+3(x_2+2)^2]\right)$ (b) $c=\frac{3e^2}{\sqrt{2\pi}}$, 평균 $-1$, 분산 $\tfrac19$

#### 다른 길로 검산해요

#### (a) 검산

$\Sigma\Sigma^{-1}=\tfrac12\begin{bmatrix}3-1&-3+3\\1-1&-1+3\end{bmatrix}=I$예요. 상수는 sympy로 2차원 적분을 해서 1이 되는 것을 확인했어요(evidence/answer-checks.py의 p3:a). 상수를 $1/(4\pi)$로 쓰면 적분이 $2\sqrt2\pi/(4\pi)=1/\sqrt2\ne1$이 돼요.

#### (b) 검산

전개해서 되돌려요: $9(z+1)^2+4=9z^2+18z+9+4$예요. $z=-1$에서 지수가 가장 커서(꼭짓점) 평균이 $-1$이고, $-\tfrac12(\cdots)$ 괄호 안의 $z^2$ 계수 $9$가 정밀도라 그 역수가 분산 $\tfrac19$이에요.

#### 이 부분을 조심해요

2차원 정규화 상수를 $\left(\frac1{\sqrt{2\pi|\Sigma|}}\right)^2=\frac1{2\pi|\Sigma|}$로 쓰는 실수가 많아요. $|\Sigma|$는 제곱근이 한 번만 붙은 $|\Sigma|^{1/2}$로 들어가요.

(a)는 "Expand in terms of $(x_1-2)$ and $(x_2+2)$"라서 $x_1,x_2$로 섞어 둔 곱보다 $(x_1-2)^2$, $(x_1-2)(x_2+2)$, $(x_2+2)^2$ 세 항으로 정리해야 해요. (b)는 $c$만 구하고 끝내기 쉬워요. "Identify its mean and variance"를 따로 답해요.

#### 혼자 다시 풀어봐요

1. $D$차원 가우시안 상수 $(2\pi)^{-D/2}|\Sigma|^{-1/2}$를 보지 않고 써요.
2. $\Sigma^{-1}$을 구한 뒤 $(a,b)$ 이차형식을 세 항으로 펼쳐요.
3. (b)의 완전제곱에서 $c$, 평균, 분산 세 개를 모두 읽어 답에 적어요.

**페이지 요약**

#### 떠올릴 개념·공식

$p(\mathbf x)=(2\pi)^{-D/2}|\Sigma|^{-1/2}\exp(-\tfrac12\mathbf d^\top\Sigma^{-1}\mathbf d)$예요. 지수가 $-\tfrac12\lambda(z-m)^2$이면 $\mathcal N(m,1/\lambda)$예요.

#### 첫 줄

(a) $|\Sigma|=2$, $\Sigma^{-1}=\tfrac12\begin{bmatrix}1&-1\\-1&3\end{bmatrix}$ (b) $9(z+1)^2+4$

#### 핵심 주의점

2차원 상수는 $\frac1{2\pi\sqrt{|\Sigma|}}$이지 $\frac1{2\pi|\Sigma|}$가 아니에요. (b)는 평균·분산까지 답해요.

#### 답

(a) 상수 $\frac1{2\sqrt2\pi}$, 이차식 $\tfrac12[a^2-2ab+3b^2]$ (b) $c=3e^2/\sqrt{2\pi}$, 평균 $-1$, 분산 $\tfrac19$

#### 다시 볼 자료

[1007 가우시안 랜덤 벡터 PDF](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1007/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1007_Product_of_Gaussians.html#s2-pdf), [1012 det Σ와 정규화](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1012/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1012_Several_Mathematical_Proofs.html#s1-det), [1014 넓이를 1로](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1014/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1014_Bayesian_Posterior_Prediction.html#s0-normalize)

#### 용어

- **정규화 상수(normalizing constant)** — 밀도의 전체 적분을 1로 맞추는 앞 계수예요. $D$차원 가우시안은 $(2\pi)^{-D/2}|\Sigma|^{-1/2}$예요.
- **공분산행렬(covariance matrix)** — $\Sigma$, 대각은 분산, 비대각은 공분산이에요. 여기서는 $2\times2$ 대칭 양의 정부호예요.
- **완전제곱(completing the square)** — $\alpha z^2+\beta z+\gamma$를 $\alpha(z+\frac{\beta}{2\alpha})^2+$상수로 바꾸는 변형이에요.

---

<a id="p4"></a>

### Q4. 결합확률과 조건부확률

Midterm 1021 Q4 · [원 문제 보기](%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC_1021_Midterm.html#p4)

#### 주어진 조건

$U\in\{0,1\}$, $V\in\{0,1,2\}$의 결합 pmf는 $p(0,0)=\tfrac1{10},\ p(0,1)=\tfrac2{10},\ p(0,2)=\tfrac1{10},\ p(1,0)=\tfrac2{10},\ p(1,1)=\tfrac1{10},\ p(1,2)=\tfrac3{10}$이에요.

#### 구할 것

다음을 구해 보세요.

- (a) $U$와 $V$의 주변 pmf를 구하세요.
- (b) $P(U=1\mid V=2)$를 구하고, $U$와 $V$가 독립인지 수치로 판단하세요.

<details><summary>원문 보기</summary>

"The joint pmf of $U\in\{0,1\}$ and $V\in\{0,1,2\}$: $p(0,0)=1/10,\ p(0,1)=2/10,\ p(0,2)=1/10,\ p(1,0)=2/10,\ p(1,1)=1/10,\ p(1,2)=3/10$.

(a) Find the marginal probability mass functions of $U$ and $V$.

(b) Compute $P(U=1\mid V=2)$. Are $U$ and $V$ independent? Justify your conclusion using numerical probabilities.

"

![Q4 시험지 스캔](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_exam1021_Midterm/eec385e7f9b071fb-q4.webp)

</details>

#### 무엇을 구하는 문제인가요?

$2\times3$ 표에 $U,V$ 쌍의 확률이 적혀 있어요. (a)는 표의 행 합과 열 합으로 $U$ 혼자, $V$ 혼자의 확률을 구해요. (b)는 $V=2$라는 정보가 있을 때 $U=1$일 확률을 구하고, 그 정보가 $U$의 확률을 바꾸는지로 독립 여부를 판단해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

**(a)의 단서:** "marginal pmf"는 합 규칙(sum rule)이에요. $P(U=u)=\sum_vP(U=u,V=v)$, $P(V=v)=\sum_uP(U=u,V=v)$라서 표의 행 합·열 합이에요. 각 주변분포의 합이 1인지가 첫 확인이에요.

**(b)의 단서:** "$P(U=1\mid V=2)$"는 조건부확률 $\frac{P(U=1,V=2)}{P(V=2)}$이고 분모는 (a)의 주변확률이에요. "independent"는 모든 $(u,v)$에서 $P(u,v)=P(u)P(v)$인지, 같은 말로 모든 $(u,v)$에서 $P(U=u\mid V=v)=P(U=u)$인지예요. 한 칸에서 등식이 맞아도 독립이라는 결론은 나오지 않아요. 반대로 한 칸이라도 어긋나면 독립이 아니에요. 이 문제는 이 방향만 써요.

#### 종이에 쓸 첫 줄

표 오른쪽에 행 합 $\tfrac4{10},\tfrac6{10}$, 아래에 열 합 $\tfrac3{10},\tfrac3{10},\tfrac4{10}$을 적어요.

#### 한 단계씩 계산해요

#### (a)

$P(U=0)=\tfrac{1+2+1}{10}=\tfrac4{10}$, $P(U=1)=\tfrac{2+1+3}{10}=\tfrac6{10}$이에요.

$P(V=0)=\tfrac{1+2}{10}=\tfrac3{10}$, $P(V=1)=\tfrac{2+1}{10}=\tfrac3{10}$, $P(V=2)=\tfrac{1+3}{10}=\tfrac4{10}$이에요.

#### (b)

$$
P(U=1\mid V=2)=\frac{P(U=1,V=2)}{P(V=2)}=\frac{3/10}{4/10}=\frac34.
$$

$P(U=1)=\tfrac35$인데 $V=2$를 알면 $\tfrac34$로 바뀌어요. 또 $P(U=1,V=2)=\tfrac3{10}\ne P(U=1)P(V=2)=\tfrac35\cdot\tfrac25=\tfrac6{25}$예요. 그래서 독립이 아니에요.

**완성 답**<br>(a) $P_U=(\tfrac4{10},\tfrac6{10})$, $P_V=(\tfrac3{10},\tfrac3{10},\tfrac4{10})$ (b) $\tfrac34$, 독립 아님

#### 다른 길로 검산해요

#### (a) 검산

$\tfrac4{10}+\tfrac6{10}=1$, $\tfrac3{10}+\tfrac3{10}+\tfrac4{10}=1$이고 두 방향의 총합이 모두 표 전체 합 1과 같아요.

#### (b) 검산

$V=2$ 열만 떼어 다시 정규화하면 $(\tfrac1{10},\tfrac3{10})/\tfrac4{10}=(\tfrac14,\tfrac34)$예요. 합이 1이고 $U=1$ 쪽이 $\tfrac34$로 같아요.

#### 이 부분을 조심해요

조건부확률의 분모를 $P(U=1)$로 바꿔 쓰지 않아요. 조건으로 주어진 사건 $V=2$의 확률이 분모예요. 독립 판단은 "숫자로 정당화"하라고 했으니 비교한 두 값을 모두 적어요.

#### 혼자 다시 풀어봐요

1. 표에 행 합·열 합을 적고 각각 합이 1인지 봐요.
2. 조건으로 주어진 열을 떼어 다시 정규화해 조건부확률을 구해요.
3. $P(u,v)$와 $P(u)P(v)$를 한 칸에서 비교해 결론을 써요.

**페이지 요약**

#### 떠올릴 개념·공식

주변 = 행·열 합(sum rule), 조건부 = 결합/주변, 독립 ⇔ 모든 칸 $P(u,v)=P(u)P(v)$예요.

#### 첫 줄

행 합 $\tfrac4{10},\tfrac6{10}$과 열 합 $\tfrac3{10},\tfrac3{10},\tfrac4{10}$을 표에 적어요.

#### 핵심 주의점

분모는 조건 사건 $P(V=2)$예요. 비교한 두 수를 모두 써요.

#### 답

(a) $(\tfrac4{10},\tfrac6{10})$, $(\tfrac3{10},\tfrac3{10},\tfrac4{10})$ (b) $\tfrac34\ne\tfrac35$, 독립 아님

#### 다시 볼 자료

[0916 Joint · Marginal](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/0916/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_0916_MAP_and_Generative_Models.html#s2-joint), [0930 조건부확률](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/0930/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_0930_Bayesian_Linear_Regression.html#s0-cond-prob)

#### 용어

- **결합 pmf(joint pmf)** — $P(U=u,V=v)$, 두 이산 변수가 동시에 그 값을 가질 확률이에요.
- **주변 pmf(marginal pmf)** — 다른 변수에 대해 합한 $P(U=u)=\sum_vP(u,v)$예요.
- **독립(independence)** — 모든 $(u,v)$에서 $P(u,v)=P(u)P(v)$예요.

---

<a id="p5"></a>

### Q5. 베이즈 추론과 예측

Midterm 1021 Q5 · [원 문제 보기](%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC_1021_Midterm.html#p5)

#### 주어진 조건

패킷 성공확률 $\theta$의 사전분포는 $P(\theta=\tfrac13)=\tfrac23$, $P(\theta=\tfrac23)=\tfrac13$이에요. $\theta$가 주어지면 $X_1,X_2,\dots$는 독립 Bernoulli($\theta$)이고, 관측은 $\mathcal D=\{X_1=1,X_2=1\}$이에요.

#### 구할 것

다음을 구해 보세요.

- (a) 주변우도 $P(\mathcal D)$와 두 $\theta$ 값의 사후확률을 구하세요.
- (b) $\hat\theta_{\mathrm{MAP}}$과 완전 베이즈 예측 $P(X_3=1\mid\mathcal D)$를 구하고, MAP plug-in 예측과 비교해 왜 다른지 설명하세요.

<details><summary>원문 보기</summary>

"Unknown packet-success probability $\theta$ with prior $P(\theta=\tfrac13)=\tfrac23$, $P(\theta=\tfrac23)=\tfrac13$. Conditional on $\theta$, $X_1,X_2,\dots$ are independent Bernoulli($\theta$). Data $\mathcal D=\{X_1=1,X_2=1\}$.

(a) Compute the marginal likelihood $P(\mathcal D)$ and the posterior probabilities of the two possible values of $\theta$.

(b) Find $\hat\theta_{\mathrm{MAP}}$ and the fully Bayesian prediction $P(X_3=1\mid\mathcal D)$. Compare the latter with the MAP plug-in prediction, and briefly explain why they differ.

"

![Q5 시험지 스캔](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_exam1021_Midterm/41304f44744892bb-q5.webp)

</details>

#### 무엇을 구하는 문제인가요?

성공확률 $\theta$는 $\tfrac13$ 아니면 $\tfrac23$ 둘 중 하나예요. 처음엔 $\tfrac13$일 가능성을 더 크게 봤지만(사전 $\tfrac23$) 두 번 연속 성공을 봤어요. (a)는 이 관측으로 두 후보의 확률이 어떻게 바뀌는지(사후확률)를 구해요. (b)는 "다음 패킷도 성공할 확률"을 두 방식으로 구해 비교해요. 하나는 가장 그럴듯한 $\theta$ 하나만 넣는 MAP plug-in, 다른 하나는 두 후보를 사후확률로 평균하는 완전 베이즈(fully Bayesian) 예측이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

**(a)의 단서:** "marginal likelihood"와 "posterior"는 베이즈 룰이에요.

$$
P(\mathcal D)=\sum_\theta P(\mathcal D\mid\theta)P(\theta),\qquad P(\theta\mid\mathcal D)=\frac{P(\mathcal D\mid\theta)P(\theta)}{P(\mathcal D)}.
$$

조건부 독립이라 $P(\mathcal D\mid\theta)=\theta\cdot\theta=\theta^2$예요.

**(b)의 단서:** "fully Bayesian prediction"은 $\theta$를 주변화(marginalize)하는 거예요.

$$
P(X_3=1\mid\mathcal D)=\sum_\theta P(X_3=1\mid\theta)\,P(\theta\mid\mathcal D)=\sum_\theta\theta\,P(\theta\mid\mathcal D).
$$

$X_3$는 $\theta$가 주어지면 $\mathcal D$와 독립이라 $P(X_3=1\mid\theta,\mathcal D)=\theta$로 줄어요. 가중치는 데이터를 본 뒤의 사후확률이에요. 사전확률을 쓰면 데이터를 보기 전의 예측이 돼요. MAP은 사후확률이 가장 큰 $\theta$ 하나예요.

#### 종이에 쓸 첫 줄

$P(\mathcal D\mid\theta=\tfrac13)=\tfrac19$, $P(\mathcal D\mid\theta=\tfrac23)=\tfrac49$를 먼저 써요.

#### 한 단계씩 계산해요

#### (a)

$$
P(\mathcal D)=\tfrac19\cdot\tfrac23+\tfrac49\cdot\tfrac13=\tfrac2{27}+\tfrac4{27}=\tfrac6{27}=\tfrac29.
$$

$P(\theta=\tfrac13\mid\mathcal D)=\frac{2/27}{6/27}=\tfrac13$, $P(\theta=\tfrac23\mid\mathcal D)=\frac{4/27}{6/27}=\tfrac23$이에요. 두 번의 성공이 $\tfrac23$ 쪽으로 믿음을 옮겼어요.

#### (b)

사후확률이 큰 쪽이라 $\hat\theta_{\mathrm{MAP}}=\tfrac23$이고, MAP plug-in 예측은 $P(X_3=1\mid\hat\theta_{\mathrm{MAP}})=\tfrac23$이에요.

$$
P(X_3=1\mid\mathcal D)=\tfrac13\cdot\underbrace{\tfrac13}_{P(\theta=\frac13\mid\mathcal D)}+\tfrac23\cdot\underbrace{\tfrac23}_{P(\theta=\frac23\mid\mathcal D)}=\tfrac19+\tfrac49=\tfrac59.
$$

$\tfrac59<\tfrac23$이에요. 완전 베이즈 예측은 아직 사후확률 $\tfrac13$이 남아 있는 $\theta=\tfrac13$의 가능성도 평균에 넣지만, MAP plug-in은 그 불확실성을 버리고 $\tfrac23$ 하나만 쓰기 때문에 달라요.

**완성 답**<br>(a) $P(\mathcal D)=\tfrac29$, $P(\theta=\tfrac13\mid\mathcal D)=\tfrac13$, $P(\theta=\tfrac23\mid\mathcal D)=\tfrac23$ (b) $\hat\theta_{\mathrm{MAP}}=\tfrac23$, $P(X_3=1\mid\mathcal D)=\tfrac59$, plug-in $\tfrac23$

#### 다른 길로 검산해요

#### (a) 검산

사후확률 합 $\tfrac13+\tfrac23=1$이에요. 비율로도 봐요: 사후 비 = 우도 비 × 사전 비 $=4\times\tfrac12=2$라 $\tfrac23:\tfrac13$과 같아요.

#### (b) 검산

예측값은 두 후보 $\tfrac13,\tfrac23$ 사이여야 해요. $\tfrac59\approx0.556$이 그 사이에 있고, 사후확률이 큰 $\tfrac23$ 쪽에 더 가까워요. 사전확률로 가중하면 $\tfrac13\cdot\tfrac23+\tfrac23\cdot\tfrac13=\tfrac49$가 나오는데, 이는 데이터를 보기 전의 예측이라 이 문제의 답이 아니에요.

#### 이 부분을 조심해요

예측식 $\sum_\theta P(X_3=1\mid\theta)P(\theta\mid\mathcal D)$를 맞게 써 놓고 숫자를 넣을 때 사전확률 $P(\theta)$를 넣는 실수가 흔해요. 조건 기호 "$\mid\mathcal D$"가 붙은 확률은 (a)에서 구한 사후확률이에요. "왜 다른가"는 "사후 불확실성을 평균하느냐, 하나의 점추정으로 버리느냐"로 설명해요.

#### 혼자 다시 풀어봐요

1. 우도·사전·주변우도·사후를 표 한 장에 정리해요.
2. 예측식의 가중치 자리에 (a)의 사후확률을 넣어 $\tfrac59$를 다시 얻어요.
3. MAP plug-in과 비교하고 차이의 이유를 한 문장으로 써요.

**페이지 요약**

#### 떠올릴 개념·공식

사후 ∝ 우도 × 사전, $P(\mathcal D)=\sum P(\mathcal D\mid\theta)P(\theta)$예요. 완전 베이즈 예측은 $\sum_\theta\theta P(\theta\mid\mathcal D)$로 **사후** 가중이에요.

#### 첫 줄

$P(\mathcal D\mid\tfrac13)=\tfrac19$, $P(\mathcal D\mid\tfrac23)=\tfrac49$

#### 핵심 주의점

예측의 가중치에 사전확률을 넣으면 $\tfrac49$로 틀려요.

#### 답

(a) $\tfrac29$, 사후 $(\tfrac13,\tfrac23)$ (b) $\hat\theta_{\mathrm{MAP}}=\tfrac23$, $\tfrac59<\tfrac23$

#### 다시 볼 자료

[0921 주변화 → 곱셈 규칙 → 조건부 독립](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/0921/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_0921_Bayesian_Inference_Model_Selection.html#s1-derivation), [0916 MAP](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/0916/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_0916_MAP_and_Generative_Models.html#s1-map)

#### 용어

- **주변우도(marginal likelihood)** — $P(\mathcal D)=\sum_\theta P(\mathcal D\mid\theta)P(\theta)$, 사후확률의 분모예요.
- **사후확률(posterior)** — 데이터를 본 뒤의 $P(\theta\mid\mathcal D)$예요.
- **MAP 추정(maximum a posteriori)** — 사후확률이 가장 큰 $\theta$ 하나예요.
- **완전 베이즈 예측(fully Bayesian prediction)** — $\theta$를 사후확률로 평균해 없앤 $P(X_3=1\mid\mathcal D)$예요.

---

<a id="p6"></a>

### Q6. 최대우도와 MAP 선형회귀

Midterm 1021 Q6 · [원 문제 보기](%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC_1021_Midterm.html#p6)

#### 주어진 조건

$y_n=\theta_0+\theta_1x_n+\varepsilon_n$, $\varepsilon_n\overset{\text{iid}}{\sim}\mathcal N(0,1)$, $\boldsymbol\theta=(\theta_0,\theta_1)^\top$이고 관측은 $(-1,0),(0,1),(1,3)$이에요.

#### 구할 것

다음을 구해 보세요.

- (a) 우도를 정규화 상수까지 $\boldsymbol\theta$의 함수로 쓰고, 최대화 조건식을 유도해 $\hat{\boldsymbol\theta}_{\mathrm{ML}}$을 구하세요.
- (b) 사전분포 $\boldsymbol\theta\sim\mathcal N(\mathbf 0,I_2)$(관측 잡음과 독립, 절편·기울기 모두 적용)를 쓸 때 음의 로그사후를 상수 차이까지 쓰고, 미분해 $\hat{\boldsymbol\theta}_{\mathrm{MAP}}$을 구하세요.

<details><summary>원문 보기</summary>

"$y_n=\theta_0+\theta_1x_n+\varepsilon_n$, $\varepsilon_n\overset{\text{iid}}{\sim}\mathcal N(0,1)$, $\boldsymbol\theta=(\theta_0,\theta_1)^\top$. Observations $(-1,0),(0,1),(1,3)$.

(a) Write the likelihood as a function of $\boldsymbol\theta$, including its normalizing constant. Derive the equations for its maximizer and find $\hat{\boldsymbol\theta}_{\mathrm{ML}}$.

(b) Now use the prior $\boldsymbol\theta\sim\mathcal N(\mathbf 0,I_2)$, independent of the observation noise. This prior applies to both the intercept and the slope. Write the negative log-posterior up to an additive constant, and find $\hat{\boldsymbol\theta}_{\mathrm{MAP}}$ by differentiating it.

"

![Q6 시험지 스캔](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_exam1021_Midterm/73f52b0a114eab7a-q6.webp)

</details>

#### 무엇을 구하는 문제인가요?

점 세 개 $(-1,0),(0,1),(1,3)$에 직선 $\theta_0+\theta_1x$를 맞춰요. 잡음이 표준정규라 "이 직선이면 관측이 나올 확률"(우도)을 식으로 쓰고, 그것을 가장 크게 하는 $\boldsymbol\theta$(ML)를 구해요. (b)는 $\boldsymbol\theta$가 0 근처일 거라는 사전분포를 더해 사후를 가장 크게 하는 $\boldsymbol\theta$(MAP)를 구해요.

이 시험은 gradient를 열벡터로 쓰기로 했어요. 강의는 행벡터 미분을 0으로 놓고 양변을 전치해 정규방정식을 얻지만, 여기서는 열 gradient $\nabla_{\boldsymbol\theta}\tfrac12\|\mathbf y-\Phi\boldsymbol\theta\|^2=\Phi^\top(\Phi\boldsymbol\theta-\mathbf y)$를 바로 0으로 놓아요. 두 길은 전치 관계라 같은 정규방정식에 도착해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

**(a)의 단서:** "$\varepsilon_n\overset{\text{iid}}{\sim}\mathcal N(0,1)$"는 $y_n\mid\boldsymbol\theta\sim\mathcal N(\phi(x_n)^\top\boldsymbol\theta,1)$이라는 뜻이고, iid라 우도는 곱이에요. 특징벡터 $\phi(x)=(1,x)^\top$를 행으로 쌓은 설계행렬 $\Phi$($3\times2$)를 쓰면

$$
p(\mathbf y\mid\boldsymbol\theta)=\prod_n\frac{1}{\sqrt{2\pi}}e^{-(y_n-\phi_n^\top\boldsymbol\theta)^2/2}=(2\pi)^{-3/2}\exp\!\left(-\tfrac12\|\mathbf y-\Phi\boldsymbol\theta\|^2\right).
$$

최대화는 음의 로그우도 $\tfrac12\|\mathbf y-\Phi\boldsymbol\theta\|^2$의 최소화와 같아요. 열 gradient가 0인 조건이 정규방정식 $\Phi^\top\Phi\boldsymbol\theta=\Phi^\top\mathbf y$예요.

**(b)의 단서:** "prior $\mathcal N(\mathbf 0,I_2)$"는 음의 로그에 $\tfrac12\|\boldsymbol\theta\|^2$를 더해요(L2 정규화). 미분하면 $+\boldsymbol\theta$가 생겨 $(\Phi^\top\Phi+I)\boldsymbol\theta=\Phi^\top\mathbf y$가 돼요. 잡음 분산이 1, 사전 분산이 1이라 계수는 정확히 $I$예요.

#### 종이에 쓸 첫 줄

$\Phi=\begin{bmatrix}1&-1\\1&0\\1&1\end{bmatrix}$, $\mathbf y=(0,1,3)^\top$를 쓰고 바로 $\Phi^\top\Phi=\begin{bmatrix}3&0\\0&2\end{bmatrix}$, $\Phi^\top\mathbf y=(4,3)^\top$를 계산해 둬요.

#### 한 단계씩 계산해요

#### (a)

우도는 $p(\mathbf y\mid\boldsymbol\theta)=(2\pi)^{-3/2}\exp\!\left(-\tfrac12\|\mathbf y-\Phi\boldsymbol\theta\|^2\right)$이에요.

$L(\boldsymbol\theta)=-\log p=\tfrac12\|\mathbf y-\Phi\boldsymbol\theta\|^2+\tfrac32\log(2\pi)$예요. 노름을 펼치면 $\tfrac12(\mathbf y-\Phi\boldsymbol\theta)^\top(\mathbf y-\Phi\boldsymbol\theta)=\tfrac12\mathbf y^\top\mathbf y-\mathbf y^\top\Phi\boldsymbol\theta+\tfrac12\boldsymbol\theta^\top\Phi^\top\Phi\boldsymbol\theta$이고, 항마다 열 gradient를 구하면 $-\Phi^\top\mathbf y$와 $\Phi^\top\Phi\boldsymbol\theta$($\Phi^\top\Phi$가 대칭)예요. 그래서 열 gradient는 $\nabla_{\boldsymbol\theta}L=\Phi^\top(\Phi\boldsymbol\theta-\mathbf y)\in\mathbb R^{2\times1}$이에요. 0으로 놓으면

$$
\Phi^\top\Phi\,\boldsymbol\theta=\Phi^\top\mathbf y\ \Rightarrow\ \begin{bmatrix}3&0\\0&2\end{bmatrix}\boldsymbol\theta=\begin{bmatrix}4\\3\end{bmatrix}\ \Rightarrow\ \hat{\boldsymbol\theta}_{\mathrm{ML}}=\begin{bmatrix}4/3\\3/2\end{bmatrix}.
$$

#### (b)

$p(\boldsymbol\theta\mid\mathcal D)\propto p(\mathbf y\mid\boldsymbol\theta)p(\boldsymbol\theta)$라서

$$
-\log p(\boldsymbol\theta\mid\mathcal D)=\tfrac12\|\mathbf y-\Phi\boldsymbol\theta\|^2+\tfrac12\|\boldsymbol\theta\|^2+\text{const}.
$$

열 gradient $\Phi^\top(\Phi\boldsymbol\theta-\mathbf y)+\boldsymbol\theta=\mathbf 0$에서 $(\Phi^\top\Phi+I)\boldsymbol\theta=\Phi^\top\mathbf y$, 즉 $\begin{bmatrix}4&0\\0&3\end{bmatrix}\boldsymbol\theta=\begin{bmatrix}4\\3\end{bmatrix}$이라 $\hat{\boldsymbol\theta}_{\mathrm{MAP}}=(1,1)^\top$이에요.

**완성 답**<br>(a) $p(\mathbf y\mid\boldsymbol\theta)=(2\pi)^{-3/2}e^{-\frac12\|\mathbf y-\Phi\boldsymbol\theta\|^2}$, $\hat{\boldsymbol\theta}_{\mathrm{ML}}=(\tfrac43,\tfrac32)^\top$ (b) $\tfrac12\|\mathbf y-\Phi\boldsymbol\theta\|^2+\tfrac12\|\boldsymbol\theta\|^2$, $\hat{\boldsymbol\theta}_{\mathrm{MAP}}=(1,1)^\top$

#### 다른 길로 검산해요

#### (a) 검산

잔차 $\mathbf y-\Phi\hat{\boldsymbol\theta}_{\mathrm{ML}}=(0-(\tfrac43-\tfrac32),\ 1-\tfrac43,\ 3-(\tfrac43+\tfrac32))=(\tfrac16,-\tfrac13,\tfrac16)$이에요. $\Phi^\top$를 곱하면 $(\tfrac16-\tfrac13+\tfrac16,\ -\tfrac16+\tfrac16)=(0,0)$이라 정규방정식을 만족해요.

#### (b) 검산

$(\Phi^\top\Phi+I)(1,1)^\top=(4,3)^\top=\Phi^\top\mathbf y$예요. MAP은 ML보다 원점 쪽으로 줄었어요($\tfrac43\to1$, $\tfrac32\to1$). 사전분포가 0 근처를 선호한다는 의미와 맞아요.

#### 이 부분을 조심해요

우도의 정규화 상수는 1차원 상수를 관측 수 $N=3$번 곱한 $(2\pi)^{-3/2}$예요. 잡음 공분산 $I_3$의 행렬식은 1이라 추가 계수가 없어요. 행 gradient로 계산했다면 0으로 놓은 뒤 양변을 전치해 $\Phi^\top\Phi\boldsymbol\theta=\Phi^\top\mathbf y$로 바꾸는 단계를 적어요. 이 시험은 열 gradient를 지정했어요.

#### 혼자 다시 풀어봐요

1. $\Phi$의 각 행이 $\phi(x_n)^\top=(1,x_n)$인지 확인하며 써요.
2. 음의 로그우도/로그사후를 쓰고 열 gradient를 0으로 놓아 두 정규방정식을 얻어요.
3. 잔차가 $\Phi^\top\mathbf r=\mathbf 0$을 만족하는지로 ML 해를 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

가우시안 잡음 ML = 최소제곱, $\Phi^\top\Phi\boldsymbol\theta=\Phi^\top\mathbf y$예요. $\mathcal N(\mathbf 0,I)$ 사전을 더하면 $(\Phi^\top\Phi+I)\boldsymbol\theta=\Phi^\top\mathbf y$예요. 이 시험은 열 gradient를 써요(강의 행 표기의 전치).

#### 첫 줄

$\Phi^\top\Phi=\mathrm{diag}(3,2)$, $\Phi^\top\mathbf y=(4,3)^\top$

#### 핵심 주의점

상수 $(2\pi)^{-3/2}$, 행 표기로 풀었다면 양변 전치 단계를 써요.

#### 답

(a) $(\tfrac43,\tfrac32)^\top$ (b) $(1,1)^\top$

#### 다시 볼 자료

[0923 ML → 최소제곱](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/0923/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_0923_Linear_Regression.html#s2-nll), [0928 기울기를 0으로](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/0928/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_0928_Linear_Regression.html#s1-theta-ml), [0916 가우시안 prior = L2](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/0916/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_0916_MAP_and_Generative_Models.html#s1-map-reg)

#### 용어

- **우도(likelihood)** — $\boldsymbol\theta$를 고정했을 때 관측 $\mathbf y$의 밀도 $p(\mathbf y\mid\boldsymbol\theta)$를 $\boldsymbol\theta$의 함수로 본 거예요.
- **설계행렬(design matrix)** — $\Phi$, $n$행이 $\phi(x_n)^\top=(1,x_n)$인 $N\times2$ 행렬이에요.
- **정규방정식(normal equation)** — $\Phi^\top\Phi\boldsymbol\theta=\Phi^\top\mathbf y$, 제곱오차의 gradient를 0으로 놓은 식이에요.
- **음의 로그사후(negative log-posterior)** — $-\log p(\mathbf y\mid\boldsymbol\theta)-\log p(\boldsymbol\theta)$+상수, MAP은 이를 최소화해요.

---

<a id="p7"></a>

### Q7. 공분산과 교차공분산 행렬

Midterm 1021 Q7 · [원 문제 보기](%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC_1021_Midterm.html#p7)

#### 주어진 조건

$E[x_1]=2,\ E[x_2]=-1,\ \mathrm{Var}(x_1)=3,\ \mathrm{Var}(x_2)=2,\ E[x_1x_2]=-1$이에요. $\varepsilon$은 $\mathbf x$와 독립이고 평균 0, 분산 2예요. $\mathbf y=\begin{pmatrix}x_1+x_2+1+\varepsilon\\2x_1-x_2-2+2\varepsilon\end{pmatrix}$이고, 두 좌표에 같은 $\varepsilon$이 들어가요.

#### 구할 것

다음을 구해 보세요.

- (a) $\boldsymbol\mu_x=E[\mathbf x]$, $\Sigma_x=\mathrm{Cov}(\mathbf x)$, $\boldsymbol\mu_y=E[\mathbf y]$를 구하세요.
- (b) $\Sigma_y=\mathrm{Cov}(\mathbf y)$와 교차공분산 $C_{xy}=E[(\mathbf x-\boldsymbol\mu_x)(\mathbf y-\boldsymbol\mu_y)^\top]$를 구하고, 공유 잡음이 $\Sigma_y$에 어떻게 기여하는지 보이세요.

<details><summary>원문 보기</summary>

"$E[x_1]=2,\ E[x_2]=-1,\ \mathrm{Var}(x_1)=3,\ \mathrm{Var}(x_2)=2,\ E[x_1x_2]=-1$. $\varepsilon$ independent of $\mathbf x$, mean 0, variance 2. $\mathbf y=\begin{pmatrix}x_1+x_2+1+\varepsilon\\2x_1-x_2-2+2\varepsilon\end{pmatrix}$. The same scalar noise $\varepsilon$ appears in both coordinates.

(a) Find $\boldsymbol\mu_x=E[\mathbf x]$, $\Sigma_x=\mathrm{Cov}(\mathbf x)$, and $\boldsymbol\mu_y=E[\mathbf y]$.

(b) Find $\Sigma_y=\mathrm{Cov}(\mathbf y)$ and the cross-covariance matrix $C_{xy}=E[(\mathbf x-\boldsymbol\mu_x)(\mathbf y-\boldsymbol\mu_y)^\top]$. Show how the shared noise contributes to $\Sigma_y$.

"

![Q7 시험지 스캔](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_exam1021_Midterm/075f41a807e23487-q7.webp)

</details>

#### 무엇을 구하는 문제인가요?

$\mathbf x$의 평균·분산과 $E[x_1x_2]$가 주어져요. $\mathbf y$는 $\mathbf x$를 행렬로 섞고 상수를 더한 뒤, 같은 잡음 $\varepsilon$을 두 좌표에 1배·2배로 넣은 벡터예요. (a)는 $\mathbf x$의 평균·공분산과 $\mathbf y$의 평균을 구해요. (b)는 $\mathbf y$의 공분산, 그리고 $\mathbf x$와 $\mathbf y$가 함께 움직이는 정도인 교차공분산 $C_{xy}$를 구하고, 공유 잡음이 $\Sigma_y$에 어떻게 들어가는지 보여요. 요구가 세 가지($\Sigma_y$, $C_{xy}$, 잡음 기여)라는 점을 먼저 표시해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

**(a)의 단서:** $E[x_1x_2]$가 주어지면 공분산 공식 $\mathrm{Cov}(x_1,x_2)=E[x_1x_2]-E[x_1]E[x_2]$를 떠올려요. $\mathbf y$를 아핀(affine) 꼴 $\mathbf y=A\mathbf x+\mathbf b+\mathbf w\varepsilon$로 쓰면 $E[\mathbf y]=A\boldsymbol\mu_x+\mathbf b$예요($E[\varepsilon]=0$).

**(b)의 단서:** 아핀 변환의 공분산은 $\mathrm{Cov}(A\mathbf x)=A\Sigma_xA^\top$이고, 독립인 두 부분의 공분산은 더해져요. 스칼라 $\varepsilon$에 벡터 $\mathbf w=(1,2)^\top$가 곱해지면 기여는 $\mathrm{Var}(\varepsilon)\mathbf w\mathbf w^\top$예요. 교차공분산은 $C_{xy}=E[(\mathbf x-\boldsymbol\mu_x)(\mathbf y-\boldsymbol\mu_y)^\top]=\Sigma_xA^\top$이고, 독립인 $\varepsilon$은 기여하지 않아요. $A^\top$가 오른쪽에 **한 번만** 붙는다는 점이 $A\Sigma_xA^\top$와 달라요.

#### 종이에 쓸 첫 줄

$\mathbf y=\underbrace{\begin{bmatrix}1&1\\2&-1\end{bmatrix}}_{A}\mathbf x+\underbrace{\begin{bmatrix}1\\-2\end{bmatrix}}_{\mathbf b}+\underbrace{\begin{bmatrix}1\\2\end{bmatrix}}_{\mathbf w}\varepsilon$로 다시 써요.

#### 한 단계씩 계산해요

#### (a)

$\boldsymbol\mu_x=(2,-1)^\top$, $\mathrm{Cov}(x_1,x_2)=-1-(2)(-1)=1$이라 $\Sigma_x=\begin{bmatrix}3&1\\1&2\end{bmatrix}$이에요.

$\boldsymbol\mu_y=A\boldsymbol\mu_x+\mathbf b=\begin{bmatrix}2-1\\4+1\end{bmatrix}+\begin{bmatrix}1\\-2\end{bmatrix}=\begin{bmatrix}2\\3\end{bmatrix}$이에요.

#### (b)

$A\Sigma_x=\begin{bmatrix}4&3\\5&0\end{bmatrix}$, $A\Sigma_xA^\top=\begin{bmatrix}7&5\\5&10\end{bmatrix}$이에요.

공유 잡음 기여는 $\mathrm{Var}(\varepsilon)\mathbf w\mathbf w^\top=2\begin{bmatrix}1&2\\2&4\end{bmatrix}=\begin{bmatrix}2&4\\4&8\end{bmatrix}$이에요. 비대각 $4$는 같은 $\varepsilon$이 두 좌표를 함께 움직여서 생겨요(독립 잡음이었다면 0).

$$
\Sigma_y=\begin{bmatrix}7&5\\5&10\end{bmatrix}+\begin{bmatrix}2&4\\4&8\end{bmatrix}=\begin{bmatrix}9&9\\9&18\end{bmatrix}.
$$

$\mathbf y-\boldsymbol\mu_y=A(\mathbf x-\boldsymbol\mu_x)+\mathbf w\varepsilon$를 정의에 넣고 $(A\mathbf d)^\top=\mathbf d^\top A^\top$로 전치를 풀면, 기댓값의 선형성으로 $A^\top$와 $\mathbf w^\top$가 밖으로 나와요.

$$
C_{xy}=E[(\mathbf x-\boldsymbol\mu_x)(\mathbf x-\boldsymbol\mu_x)^\top]A^\top+E[(\mathbf x-\boldsymbol\mu_x)\varepsilon]\mathbf w^\top
$$

앞 기댓값은 $\Sigma_x$, 뒤 기댓값은 독립이라 $\mathbf 0$이에요.

$$
C_{xy}=\Sigma_xA^\top+\underbrace{E[(\mathbf x-\boldsymbol\mu_x)\varepsilon]}_{=\mathbf 0}\mathbf w^\top=\begin{bmatrix}3&1\\1&2\end{bmatrix}\begin{bmatrix}1&2\\1&-1\end{bmatrix}=\begin{bmatrix}4&5\\3&0\end{bmatrix}.
$$

**완성 답**<br>(a) $\boldsymbol\mu_x=(2,-1)^\top$, $\Sigma_x=\begin{bmatrix}3&1\\1&2\end{bmatrix}$, $\boldsymbol\mu_y=(2,3)^\top$ (b) $\Sigma_y=\begin{bmatrix}9&9\\9&18\end{bmatrix}$ (잡음 기여 $\begin{bmatrix}2&4\\4&8\end{bmatrix}$), $C_{xy}=\begin{bmatrix}4&5\\3&0\end{bmatrix}$

#### 다른 길로 검산해요

#### (a) 검산

성분으로 직접: $E[y_1]=2+(-1)+1+0=2$, $E[y_2]=4-(-1)-2+0=3$이에요.

#### (b) 검산

성분으로 확인해요. $\mathrm{Var}(y_1)=\mathrm{Var}(x_1)+\mathrm{Var}(x_2)+2\mathrm{Cov}+\mathrm{Var}(\varepsilon)=3+2+2+2=9$예요. $\mathrm{Cov}(x_1,y_2)=2\mathrm{Var}(x_1)-\mathrm{Cov}(x_1,x_2)=6-1=5$로 $C_{xy}$의 (1,2) 성분과 같아요. $\mathrm{Cov}(x_2,y_2)=2\cdot1-2=0$도 (2,2) 성분과 같아요.

#### 이 부분을 조심해요

(b)는 $\Sigma_y$, $C_{xy}$, 잡음 기여 설명 세 가지를 요구해요. $\Sigma_y$만 구하고 $C_{xy}$를 빠뜨리기 쉬워요. 문제 문장의 요구 명사를 동그라미 치고 마지막에 대조해요.

$C_{xy}$를 $A\Sigma_xA^\top$이나 $A\Sigma_x$로 쓰지 않아요. 정의 $E[(\mathbf x-\boldsymbol\mu_x)(\mathbf y-\boldsymbol\mu_y)^\top]$에서 $\mathbf y$ 쪽이 전치되므로 $\Sigma_xA^\top$예요. 공유 잡음의 비대각 $2\cdot1\cdot2=4$를 0으로 두는 실수도 조심해요.

#### 혼자 다시 풀어봐요

1. $\mathbf y=A\mathbf x+\mathbf b+\mathbf w\varepsilon$ 꼴로 다시 써요.
2. $\Sigma_y=A\Sigma_xA^\top+\mathrm{Var}(\varepsilon)\mathbf w\mathbf w^\top$, $C_{xy}=\Sigma_xA^\top$를 계산해요.
3. 답안 끝에서 요구 세 가지가 모두 있는지 체크해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mathrm{Cov}=E[x_1x_2]-E[x_1]E[x_2]$, $E[A\mathbf x+\mathbf b]=A\boldsymbol\mu+\mathbf b$, $\mathrm{Cov}(A\mathbf x)=A\Sigma A^\top$, 교차공분산 $\Sigma_xA^\top$, 공유 잡음 $\mathrm{Var}(\varepsilon)\mathbf w\mathbf w^\top$예요.

#### 첫 줄

$\mathbf y=A\mathbf x+\mathbf b+\mathbf w\varepsilon$, $A=\begin{bmatrix}1&1\\2&-1\end{bmatrix}$, $\mathbf w=(1,2)^\top$

#### 핵심 주의점

(b)의 $C_{xy}$를 빠뜨리지 않아요. $C_{xy}$는 $A^\top$를 한 번만 곱해요.

#### 답

(a) $(2,-1)^\top$, $\begin{bmatrix}3&1\\1&2\end{bmatrix}$, $(2,3)^\top$ (b) $\Sigma_y=\begin{bmatrix}9&9\\9&18\end{bmatrix}$, $C_{xy}=\begin{bmatrix}4&5\\3&0\end{bmatrix}$

#### 다시 볼 자료

[1012 분산은 A와 A의 전치](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1012/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1012_Several_Mathematical_Proofs.html#s0-variance), [1012 교차공분산](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1012/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1012_Several_Mathematical_Proofs.html#s0-cross)

#### 용어

- **공분산행렬(covariance matrix)** — $\Sigma_x=E[(\mathbf x-\boldsymbol\mu_x)(\mathbf x-\boldsymbol\mu_x)^\top]$, 대각은 분산이에요.
- **교차공분산(cross-covariance)** — $C_{xy}=E[(\mathbf x-\boldsymbol\mu_x)(\mathbf y-\boldsymbol\mu_y)^\top]$, $(i,j)$ 성분은 $\mathrm{Cov}(x_i,y_j)$예요. 일반적으로 대칭이 아니에요.
- **아핀 변환(affine transformation)** — $A\mathbf x+\mathbf b$ 꼴이에요. 평균은 그대로 따라가고 공분산은 $A\Sigma A^\top$가 돼요.

---

<a id="p8"></a>

### Q8. 가우시안 밀도의 곱

Midterm 1021 Q8 · [원 문제 보기](%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC_1021_Midterm.html#p8)

#### 주어진 조건

$g(z)=\mathcal N(z\mid0,1)\,\mathcal N(z\mid2,1)$, $Z=\int_{-\infty}^{\infty}g(z)\,dz$, $q(z)=g(z)/Z$예요.

#### 구할 것

다음을 구해 보세요.

- (a) $g(z)$의 지수에서 완전제곱을 하고, 정규화한 $q(z)$의 평균과 분산을 구하세요.
- (b) $Z$를 계산하세요. $g(z)$ 자체가 정규화된 확률밀도인지 근거와 함께 답하세요.

<details><summary>원문 보기</summary>

"$g(z)=\mathcal N(z\mid0,1)\,\mathcal N(z\mid2,1)$, $Z=\int_{-\infty}^{\infty}g(z)\,dz$, $q(z)=g(z)/Z$.

(a) Complete the square in the exponent of $g(z)$. Identify the mean and variance of the normalized Gaussian density $q(z)$.

(b) Calculate $Z$. Is $g(z)$ itself a normalized probability density? Justify your answer.

"

![Q8 시험지 스캔](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_exam1021_Midterm/5e3057cdb332b4b6-q8.webp)

</details>

#### 무엇을 구하는 문제인가요?

평균 0과 평균 2인 두 종 모양 곡선을 같은 $z$에서 곱한 함수 $g(z)$를 봐요. (a)는 곱의 지수를 하나의 완전제곱으로 정리해, 넓이를 1로 맞춘 $q(z)$가 어떤 가우시안인지(평균·분산) 알아내요. (b)는 $g$의 넓이 $Z$를 계산하고, $g$ 자체가 확률밀도인지(넓이 1인지) 판단해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

**(a)의 단서:** "complete the square"와 "normalized Gaussian"은 렘마 "지수가 $z$의 이차식이면 가우시안"이에요. 지수를 $-\frac{(z-m)^2}{2s^2}+\text{상수}$로 바꾸면 $q=\mathcal N(m,s^2)$이에요. 같은 변수의 두 가우시안 곱에서는 정밀도(precision)가 더해져요: $\frac1{s^2}=\frac11+\frac11=2$, 평균은 정밀도 가중평균 $m=\frac{0\cdot1+2\cdot1}{2}=1$이에요.

**(b)의 단서:** $Z$는 완전제곱에서 남는 상수 $e^{\text{상수}}$와 가우시안 적분 $\int e^{-(z-m)^2/(2s^2)}dz=\sqrt{2\pi s^2}$로 계산해요. 일반적으로 $Z=\mathcal N(0\mid2,\,1+1)$(두 평균 차이를 분산 합으로 본 밀도)이에요. "normalized"인지는 $Z=1$인지로 판정해요.

#### 종이에 쓸 첫 줄

$g(z)=\frac1{2\pi}\exp\!\left(-\tfrac12[z^2+(z-2)^2]\right)$로 두 지수를 합쳐 써요.

#### 한 단계씩 계산해요

#### (a)

$z^2+(z-2)^2=2z^2-4z+4=2(z-1)^2+2$예요. 그래서

$$
g(z)=\frac{1}{2\pi}e^{-1}\exp\!\left(-\frac{(z-1)^2}{2\cdot\frac12}\right).
$$

$z$에 의존하는 부분이 평균 1, 분산 $\tfrac12$인 가우시안 모양이라 $q(z)=\mathcal N(z\mid1,\tfrac12)$예요.

#### (b)

$$
Z=\frac{e^{-1}}{2\pi}\sqrt{2\pi\cdot\tfrac12}=\frac{e^{-1}}{2\pi}\sqrt\pi=\frac{e^{-1}}{2\sqrt\pi}=\frac{e^{-1}}{\sqrt{4\pi}}\approx0.104.
$$

$Z\ne1$이라 $g$는 정규화된 확률밀도가 아니에요. 넓이 1을 맞추려면 $Z$로 나눈 $q$를 써야 해요.

**완성 답**<br>(a) $z^2+(z-2)^2=2(z-1)^2+2$, $q=\mathcal N(1,\tfrac12)$ (b) $Z=\frac{e^{-1}}{\sqrt{4\pi}}\approx0.104$, $g$는 정규화되지 않음

#### 다른 길로 검산해요

#### (a) 검산

정밀도 공식으로: 분산 $(1+1)^{-1}=\tfrac12$, 평균 $\tfrac12(0+2)=1$로 같아요. 대칭으로 봐도 두 평균 0과 2의 가운데가 1이에요.

#### (b) 검산

공식 $Z=\mathcal N(0\mid2,2)=\frac1{\sqrt{4\pi}}e^{-4/4}=\frac{e^{-1}}{\sqrt{4\pi}}$로 같아요.

#### 이 부분을 조심해요

"두 가우시안의 곱은 가우시안"은 **모양**이 그렇다는 뜻이에요. 곱 자체는 넓이가 1이 아니에요. 독립인 두 확률변수의 합(분산이 더해짐)과 밀도의 곱(정밀도가 더해짐)을 혼동하지 않아요.

#### 혼자 다시 풀어봐요

1. 두 지수를 합쳐 $2(z-1)^2+2$를 다시 유도해요.
2. 정밀도 합·가중평균으로 같은 평균·분산이 나오는지 확인해요.
3. $Z$를 계산하고 1과 비교해 결론을 써요.

**페이지 요약**

#### 떠올릴 개념·공식

지수가 이차식이면 가우시안이에요. 곱의 정밀도는 합, 평균은 정밀도 가중평균이에요. $Z=\mathcal N(m_1\mid m_2,\sigma_1^2+\sigma_2^2)$예요.

#### 첫 줄

$g=\frac1{2\pi}\exp(-\tfrac12[z^2+(z-2)^2])$

#### 핵심 주의점

곱은 모양만 가우시안이고 넓이는 $Z\ne1$이에요.

#### 답

(a) $\mathcal N(1,\tfrac12)$ (b) $Z=e^{-1}/\sqrt{4\pi}$, 정규화 아님

#### 다시 볼 자료

[1007 두 가우시안의 곱](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1007/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1007_Product_of_Gaussians.html#s3-product-scalar), [1012 완전제곱 렘마](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1012/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1012_Several_Mathematical_Proofs.html#s2-lemma)

#### 용어

- **정밀도(precision)** — 분산의 역수 $1/\sigma^2$이에요. 같은 변수의 가우시안 밀도를 곱하면 더해져요.
- **정규화(normalization)** — 전체 적분이 1이 되도록 상수로 나누는 것이에요. 여기서는 $q=g/Z$예요.

---

<a id="p9"></a>

### Q9. 베이즈 선형회귀: 파라미터 사후분포

Midterm 1021 Q9 · [원 문제 보기](%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC_1021_Midterm.html#p9)

#### 주어진 조건

$\mathbf y=\Phi\boldsymbol\theta+\boldsymbol\varepsilon$, $\boldsymbol\theta\sim\mathcal N(\mathbf m_0,S_0)$, $\boldsymbol\varepsilon\sim\mathcal N(\mathbf 0,\sigma^2I_N)$이고 사후는 $\mathcal N(\mathbf m_N,S_N)$, $S_N=(S_0^{-1}+\sigma^{-2}\Phi^\top\Phi)^{-1}$, $\mathbf m_N=S_N(S_0^{-1}\mathbf m_0+\sigma^{-2}\Phi^\top\mathbf y)$예요(증명 없이 사용 가능). $\phi(x)=(1,x)^\top$, 관측 $(-1,1),(1,3)$, $\mathbf m_0=\mathbf 0$, $S_0=I_2$, $\sigma^2=1$이에요.

#### 구할 것

다음을 구해 보세요.

- (a) 설계행렬 $\Phi$와 관측벡터 $\mathbf y$를 만들고 $\Phi^\top\Phi$와 사후 공분산 $S_N$을 구하세요.
- (b) $\Phi^\top\mathbf y$와 사후 평균 $\mathbf m_N$을 구하고, 수치 평균·공분산으로 사후분포 $p(\boldsymbol\theta\mid\mathcal D)$를 쓰세요.

<details><summary>원문 보기</summary>

"$\mathbf y=\Phi\boldsymbol\theta+\boldsymbol\varepsilon$, $\boldsymbol\theta\sim\mathcal N(\mathbf m_0,S_0)$, $\boldsymbol\varepsilon\sim\mathcal N(\mathbf 0,\sigma^2I_N)$. Posterior $\mathcal N(\boldsymbol\theta\mid\mathbf m_N,S_N)$ with $S_N=(S_0^{-1}+\sigma^{-2}\Phi^\top\Phi)^{-1}$, $\mathbf m_N=S_N(S_0^{-1}\mathbf m_0+\sigma^{-2}\Phi^\top\mathbf y)$ (may be used without proof). $\phi(x)=(1,x)^\top$, observations $(-1,1),(1,3)$, $\mathbf m_0=\mathbf 0$, $S_0=I_2$, $\sigma^2=1$.

(a) Construct the design matrix $\Phi$ and the observation vector $\mathbf y$. Calculate $\Phi^\top\Phi$ and the posterior covariance matrix $S_N$.

(b) Calculate $\Phi^\top\mathbf y$ and the posterior mean $\mathbf m_N$. State the posterior distribution $p(\boldsymbol\theta\mid\mathcal D)$ with its numerical mean vector and covariance matrix.

"

![Q9 시험지 스캔](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_exam1021_Midterm/683dcb6724781e2a-q9.webp)

</details>

#### 무엇을 구하는 문제인가요?

점 두 개 $(-1,1),(1,3)$로 직선 계수 $\boldsymbol\theta$의 사후분포를 구해요. 공식은 주어졌으니 숫자를 정확히 넣는 문제예요. (a)는 설계행렬 $\Phi$, $\Phi^\top\Phi$, 사후 공분산 $S_N$을 구하고, (b)는 사후 평균 $\mathbf m_N$을 구해 사후분포를 수치로 완성해요. 10번이 이 결과를 그대로 이어 쓰므로 여기서의 실수는 다음 문항까지 번져요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

**(a)의 단서:** $S_N=(S_0^{-1}+\sigma^{-2}\Phi^\top\Phi)^{-1}$에서 괄호 안은 정밀도(precision), 즉 "확신의 양"이에요. 사전의 확신 $S_0^{-1}$에 데이터의 확신 $\sigma^{-2}\Phi^\top\Phi$를 더한 뒤 **역행렬**을 취해야 공분산이 돼요. 데이터가 늘면 정밀도가 커지고 공분산은 작아져요. 그래서 사후 공분산은 사전 공분산 $S_0=I$보다 작아야 해요.

**(b)의 단서:** $\mathbf m_N=S_N(S_0^{-1}\mathbf m_0+\sigma^{-2}\Phi^\top\mathbf y)$에서 $\mathbf m_0=\mathbf 0$이라 $\mathbf m_N=\sigma^{-2}S_N\Phi^\top\mathbf y$이고, $\sigma^2=1$이라 $\mathbf m_N=S_N\Phi^\top\mathbf y$예요. $S_0=I$, $\sigma^2=1$인 이 설정에서는 6번의 MAP 해 $(\Phi^\top\Phi+I)^{-1}\Phi^\top\mathbf y$와 같은 꼴이에요(가우시안 사후는 평균=최빈값).

#### 종이에 쓸 첫 줄

$\Phi=\begin{bmatrix}\phi(-1)^\top\\\phi(1)^\top\end{bmatrix}=\begin{bmatrix}1&-1\\1&1\end{bmatrix}$, $\mathbf y=(1,3)^\top$를 써요.

#### 한 단계씩 계산해요

#### (a)

$\Phi^\top\Phi=\begin{bmatrix}1&1\\-1&1\end{bmatrix}\begin{bmatrix}1&-1\\1&1\end{bmatrix}=\begin{bmatrix}2&0\\0&2\end{bmatrix}=2I$예요.

정밀도는 $S_0^{-1}+\sigma^{-2}\Phi^\top\Phi=I+2I=3I$이고, 공분산은 그 역행렬이에요.

$$
S_N=(3I)^{-1}=\tfrac13I=\begin{bmatrix}1/3&0\\0&1/3\end{bmatrix}.
$$

#### (b)

$\Phi^\top\mathbf y=(1\cdot1+1\cdot3,\ -1\cdot1+1\cdot3)^\top=(4,2)^\top$예요.

$$
\mathbf m_N=S_N\Phi^\top\mathbf y=\tfrac13\begin{bmatrix}4\\2\end{bmatrix}=\begin{bmatrix}4/3\\2/3\end{bmatrix},\qquad p(\boldsymbol\theta\mid\mathcal D)=\mathcal N\!\left(\boldsymbol\theta\,\middle|\,\begin{bmatrix}4/3\\2/3\end{bmatrix},\ \tfrac13I\right).
$$

밀도로 쓰면 $p(\boldsymbol\theta\mid\mathcal D)=\frac{1}{2\pi\cdot\frac13}\exp\!\left(-\tfrac32\|\boldsymbol\theta-\mathbf m_N\|^2\right)=\frac{3}{2\pi}\exp\!\left(-\tfrac32\|\boldsymbol\theta-\mathbf m_N\|^2\right)$이에요($|S_N|^{1/2}=\tfrac13$).

**완성 답**<br>(a) $\Phi=\begin{bmatrix}1&-1\\1&1\end{bmatrix}$, $\mathbf y=(1,3)^\top$, $\Phi^\top\Phi=2I$, $S_N=\tfrac13I$ (b) $\Phi^\top\mathbf y=(4,2)^\top$, $\mathbf m_N=(\tfrac43,\tfrac23)^\top$, $p(\boldsymbol\theta\mid\mathcal D)=\mathcal N(\mathbf m_N,\tfrac13I)$

#### 다른 길로 검산해요

#### (a) 검산

상식 검사: 사후 공분산은 사전 공분산 $I$보다 작아야 해요. $\tfrac13I$는 그렇고, $3I$였다면 데이터를 보고 불확실성이 커졌다는 모순이에요. $S_N\cdot3I=I$도 확인해요.

#### (b) 검산

$\mathbf m_N$은 정규화된 최소제곱 $(\Phi^\top\Phi+I)\boldsymbol\theta=\Phi^\top\mathbf y$의 해예요: $3I\cdot(\tfrac43,\tfrac23)^\top=(4,2)^\top$ ✓. 정규화 없는 ML 해는 두 점을 지나는 직선 $(2,1)^\top$인데, 사전 $\mathcal N(\mathbf 0,I)$가 원점 쪽으로 당겨 $(\tfrac43,\tfrac23)$가 된 것도 자연스러워요.

#### 이 부분을 조심해요

공식 바깥의 $^{-1}$을 빠뜨려 정밀도 $3I$를 공분산으로 쓰는 실수가 가장 치명적이에요. 그러면 $\mathbf m_N=(12,6)^\top$처럼 데이터 범위($y$는 1~3)를 크게 벗어난 값이 나와요. 숫자가 비현실적이면 공식을 다시 봐요. 2차원 밀도 상수는 $\frac{1}{2\pi|S_N|^{1/2}}$예요.

#### 혼자 다시 풀어봐요

1. "정밀도를 더하고, 역행렬로 공분산"을 말로 한 번 말해요.
2. $S_N$을 구한 뒤 "사전 $I$보다 작은가?"를 확인해요.
3. $\mathbf m_N$이 데이터와 사전 사이의 합리적 값인지 ML 해 $(2,1)$과 비교해요.

**페이지 요약**

#### 떠올릴 개념·공식

정밀도 $S_N^{-1}=S_0^{-1}+\sigma^{-2}\Phi^\top\Phi$, 공분산은 그 **역행렬**이에요. $\mathbf m_0=\mathbf 0$이면 $\mathbf m_N=\sigma^{-2}S_N\Phi^\top\mathbf y$예요.

#### 첫 줄

$\Phi=\begin{bmatrix}1&-1\\1&1\end{bmatrix}$, $\mathbf y=(1,3)^\top$

#### 핵심 주의점

$^{-1}$ 누락 → $S_N=3I$, $\mathbf m_N=(12,6)$의 비현실적 값이 돼요. 사후 공분산 &lt; 사전 공분산을 확인해요.

#### 답

(a) $2I$, $S_N=\tfrac13I$ (b) $(4,2)^\top$, $\mathbf m_N=(\tfrac43,\tfrac23)^\top$, $\mathcal N(\mathbf m_N,\tfrac13I)$

#### 다시 볼 자료

[1014 음의 로그를 이차식으로](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1014/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1014_Bayesian_Posterior_Prediction.html#s1-expand), [1014 계수 맞추기](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1014/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1014_Bayesian_Posterior_Prediction.html#s1-match)

#### 용어

- **사후 공분산(posterior covariance)** — $S_N=(S_0^{-1}+\sigma^{-2}\Phi^\top\Phi)^{-1}$, 데이터를 본 뒤 $\boldsymbol\theta$의 불확실성이에요.
- **정밀도 행렬(precision matrix)** — 공분산의 역행렬이에요. 독립 정보가 더해질 때 정밀도끼리 더해요.
- **사후 평균(posterior mean)** — $\mathbf m_N$, 가우시안 사후에서는 MAP 해와 같아요.

---

<a id="p10"></a>

### Q10. 베이즈 선형회귀: 예측분포

Midterm 1021 Q10 · [원 문제 보기](%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC_1021_Midterm.html#p10)

#### 주어진 조건

9(b)의 모델과 사후분포를 이어서 써요. 새 입력 $x_*=2$에서 $f_*=\phi(x_*)^\top\boldsymbol\theta=\theta_0+2\theta_1$, $y_*=f_*+\varepsilon_*$, $\varepsilon_*\sim\mathcal N(0,1)$이고, $\varepsilon_*$는 $\boldsymbol\theta$와 학습 잡음 모두와 독립이에요.

#### 구할 것

다음을 구해 보세요.

- (a) $p(f_*\mid x_*,\mathcal D)$를 평균·분산까지 구하고, 왜 가우시안인지 설명하며 밀도를 명시하세요.
- (b) $p(y_*\mid x_*,\mathcal D)$를 $\boldsymbol\theta$에 대한 적분으로 쓰고 결과 가우시안을 구하세요. 분산이 (a)와 왜 다른지 설명하세요.

<details><summary>원문 보기</summary>

"Continue with the numerical model and posterior from Question 9(b). At the new input $x_*=2$, $f_*=\phi(x_*)^\top\boldsymbol\theta=\theta_0+2\theta_1$, $y_*=f_*+\varepsilon_*$, $\varepsilon_*\sim\mathcal N(0,1)$. The fresh noise $\varepsilon_*$ is jointly independent of $\boldsymbol\theta$ and all training noise variables.

(a) Determine $p(f_*\mid x_*,\mathcal D)$, including its mean and variance. Explain why it is Gaussian and write its density explicitly.

(b) Express $p(y_*\mid x_*,\mathcal D)$ as an integral over $\boldsymbol\theta$, and determine the resulting Gaussian distribution. You may use the fact that a linear combination of jointly Gaussian variables is Gaussian. Explain why its variance differs from that in part (a).

"

![Q10 시험지 스캔](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_exam1021_Midterm/de9fc882b24f25b4-q10.webp)

</details>

#### 무엇을 구하는 문제인가요?

9번에서 구한 $\boldsymbol\theta$의 사후분포 $\mathcal N(\mathbf m_N,S_N)$를 새 입력 $x_*=2$로 옮겨요. (a)는 잡음 없는 함수값 $f_*=\theta_0+2\theta_1$의 분포를, (b)는 잡음까지 더한 관측 $y_*$의 분포를 구해요. 두 분포의 평균은 같고 분산만 다르며, 그 이유를 설명해야 해요. 9번의 수치를 이어 쓰고, 9번이 틀렸어도 일관되게 쓰면 방법 점수를 받아요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

**(a)의 단서:** $f_*=\phi(x_*)^\top\boldsymbol\theta$는 가우시안 벡터 $\boldsymbol\theta$의 **선형결합(스칼라 하나)**예요. 가우시안의 선형변환은 가우시안이라

$$
f_*\mid\mathcal D\sim\mathcal N\!\left(\phi_*^\top\mathbf m_N,\ \phi_*^\top S_N\phi_*\right),\qquad \phi_*=\phi(x_*)=(1,2)^\top.
$$

여기서 쓰는 것은 학습 설계행렬 $\Phi$가 아니라 **새 입력의 특징벡터** $\phi_*$예요. 결과는 $1\times1$ 스칼라 분포예요.

**(b)의 단서:** "integral over $\boldsymbol\theta$"는 주변화예요.

$$
p(y_*\mid x_*,\mathcal D)=\int\mathcal N(y_*\mid\phi_*^\top\boldsymbol\theta,\sigma^2)\,\mathcal N(\boldsymbol\theta\mid\mathbf m_N,S_N)\,d\boldsymbol\theta.
$$

$y_*=f_*+\varepsilon_*$이고 $\varepsilon_*$가 $\boldsymbol\theta$와 독립이라 분산이 더해져요: $\phi_*^\top S_N\phi_*+\sigma^2$. 앞 항은 파라미터 불확실성, 뒤 항은 새 관측 잡음이에요.

#### 종이에 쓸 첫 줄

$\phi_*=(1,2)^\top$, $\mathbf m_N=(\tfrac43,\tfrac23)^\top$, $S_N=\tfrac13I$를 한 줄에 다시 적어요.

#### 한 단계씩 계산해요

#### (a)

평균: $\phi_*^\top\mathbf m_N=1\cdot\tfrac43+2\cdot\tfrac23=\tfrac83$이에요. 분산: $\phi_*^\top S_N\phi_*=\tfrac13(1^2+2^2)=\tfrac53$이에요.

$f_*$는 가우시안 $\boldsymbol\theta$의 선형결합이라 가우시안이에요.

$$
p(f_*\mid x_*,\mathcal D)=\mathcal N\!\left(f_*\mid\tfrac83,\tfrac53\right)=\frac{1}{\sqrt{2\pi\cdot\frac53}}\exp\!\left(-\frac{(f_*-\frac83)^2}{2\cdot\frac53}\right).
$$

#### (b)

$$
p(y_*\mid x_*,\mathcal D)=\int p(y_*\mid\boldsymbol\theta,x_*)\,p(\boldsymbol\theta\mid\mathcal D)\,d\boldsymbol\theta=\int\mathcal N(y_*\mid\phi_*^\top\boldsymbol\theta,1)\,\mathcal N(\boldsymbol\theta\mid\mathbf m_N,S_N)\,d\boldsymbol\theta.
$$

이 적분은 $\boldsymbol\theta\sim\mathcal N(\mathbf m_N,S_N)$과 $\varepsilon_*\sim\mathcal N(0,1)$이 독립일 때 $y_*=\phi_*^\top\boldsymbol\theta+\varepsilon_*$의 분포와 같아요. 그래서 적분을 직접 하지 않고 합의 분포로 구해요. $y_*=f_*+\varepsilon_*$에서 $f_*$와 $\varepsilon_*$가 독립 가우시안이라 합도 가우시안이고, 평균은 $\tfrac83+0$, 분산은 $\tfrac53+1=\tfrac83$이에요.

$$
p(y_*\mid x_*,\mathcal D)=\mathcal N\!\left(y_*\mid\tfrac83,\tfrac83\right).
$$

(a)보다 분산이 1 큰 이유는 새 관측에 들어가는 잡음 $\varepsilon_*$의 분산 $\sigma^2=1$이 더해지기 때문이에요. (a)는 "직선 자체가 어디 있는지"의 불확실성만, (b)는 거기에 "관측할 때 흔들림"까지 포함해요.

**완성 답**<br>(a) $f_*\mid\mathcal D\sim\mathcal N(\tfrac83,\tfrac53)$ (b) $y_*\mid\mathcal D\sim\mathcal N(\tfrac83,\tfrac83)$, 차이 = 관측잡음 분산 1

#### 다른 길로 검산해요

#### (a) 검산

$f_*=\theta_0+2\theta_1$에서 $\theta_0,\theta_1$가 독립(공분산 $\tfrac13I$)이라 $\mathrm{Var}(f_*)=\tfrac13+4\cdot\tfrac13=\tfrac53$, $E[f_*]=\tfrac43+2\cdot\tfrac23=\tfrac83$으로 같아요. 9번을 $S_N=3I$, $\mathbf m_N=(12,6)$으로 잘못 구했다면, 일관된 방법 점수용 값은 $\mathcal N(24,15)$예요.

#### (b) 검산

독립 확률변수의 합의 분산은 분산의 합이에요: $\tfrac53+1=\tfrac83$. 사후 평균 직선 $\tfrac43+\tfrac23x$에 $x=2$를 넣은 값도 $\tfrac83$으로 평균과 같아요.

#### 이 부분을 조심해요

$f_*=\Phi\boldsymbol\theta$처럼 학습 설계행렬을 쓰면 새 점 하나가 아니라 학습 입력들의 함수값 벡터가 돼요. 새 입력 $x_*$의 특징벡터 $\phi(x_*)$를 써야 해요. 분산을 $\boldsymbol\theta$의 공분산 행렬 그대로 쓰지 말고 $\phi_*^\top S_N\phi_*$로 **전파**해 스칼라로 만들어요.

(b)의 "왜 분산이 다른가"는 "posterior의 영향"이 아니라 "독립인 관측 잡음 $\sigma^2$가 더해져서"라고 구체적으로 답해요. 적분식만 쓰고 결과 분포의 수치를 빠뜨리지 않아요.

#### 혼자 다시 풀어봐요

1. $\phi_*$를 쓰고, 평균 $\phi_*^\top\mathbf m_N$·분산 $\phi_*^\top S_N\phi_*$를 계산해요.
2. 적분식을 쓴 뒤 "독립 합 → 분산 합"으로 $y_*$의 분포를 완성해요.
3. (a)와 (b)의 분산 차이가 정확히 $\sigma^2$인지 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

$f_*\mid\mathcal D\sim\mathcal N(\phi_*^\top\mathbf m_N,\ \phi_*^\top S_N\phi_*)$, $y_*\mid\mathcal D\sim\mathcal N(\phi_*^\top\mathbf m_N,\ \phi_*^\top S_N\phi_*+\sigma^2)$예요.

#### 첫 줄

$\phi_*=(1,2)^\top$, $\mathbf m_N=(\tfrac43,\tfrac23)^\top$, $S_N=\tfrac13I$

#### 핵심 주의점

학습 $\Phi$가 아니라 새 $\phi(x_*)$를 써요. 분산 차이 = 관측잡음 $\sigma^2$예요.

#### 답

(a) $\mathcal N(\tfrac83,\tfrac53)$ (b) $\mathcal N(\tfrac83,\tfrac83)$

#### 다시 볼 자료

[1014 가중합의 분산](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1014/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1014_Bayesian_Posterior_Prediction.html#s2-weighted), [1014 남아 있는 잡음](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1014/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1014_Bayesian_Posterior_Prediction.html#s2-uncertainty), [1019 두 가지 불확실성](../../%EB%B3%B5%EC%8A%B5%EB%85%B8%ED%8A%B8/1019/%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1019_Prediction_and_Projection.html#s0-predictive)

#### 용어

- **사후 예측분포(posterior predictive distribution)** — $\boldsymbol\theta$를 사후분포로 적분해 없앤 $p(y_*\mid x_*,\mathcal D)$예요.
- **특징벡터(feature vector)** — $\phi(x_*)=(1,x_*)^\top$, 새 입력 하나를 모델에 넣는 $2\times1$ 벡터예요.
- **인식론적 불확실성(epistemic uncertainty)** — 파라미터를 모르는 데서 오는 분산 $\phi_*^\top S_N\phi_*$예요.
- **관측 잡음(aleatoric noise)** — 새 관측의 $\varepsilon_*$, 분산 $\sigma^2$예요.

---

원 문제·정리노트·PDF는 보존해요.
