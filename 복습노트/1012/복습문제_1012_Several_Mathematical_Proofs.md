# 복습문제 8선 — 1012 수업 범위

교과서 본문 예제에서 가져온 문제 **5개**(그중 4개는 숫자를 바꾼 변형)와 연습문제 **3개**로 구성했어요. 먼저 풀어 보고, 막히면 힌트를 열어 보세요.

> `복습문제_1012_Several_Mathematical_Proofs.html`를 마크다운으로 옮겼어요. 원문, 힌트, 풀이는 접혀 있어요. 먼저 풀어 보고 펼쳐 보세요.

**목차**

- [A. 교과서 예제 변형](#partA)
  - [P1. 행렬식으로 평행사변형 넓이 재기](#p1)
  - [P2. 행렬식으로 역행렬 판정하기](#p2)
  - [P3. 선형 변환한 확률변수의 밀도 유도](#p3)
  - [P4. 축을 늘리는 변환과 밀도](#p4)
  - [P5. 기울이는 변환과 밀도](#p5)
- [B. 교과서 연습문제](#partB)
  - [P6. 잡음이 섞인 아핀 변환의 교차공분산](#p6)
  - [P7. 결합 가우시안 p(x, y) 세우기](#p7)
  - [P8. 시계열 모델의 다음 상태와 관측](#p8)

<a id="partA"></a>

## A. 교과서 예제 변형

<a id="p1"></a>

### P1. 행렬식으로 평행사변형 넓이 재기

두 벡터 $\mathbf{b}, \mathbf{g} \in \mathbb{R}^2$를 열로 세운 행렬을 ${\mathbf{A} = [\mathbf{b}, \mathbf{g}]}$라고 해요. 꼭짓점이 $\mathbf{0}$, $\mathbf{b}$, $\mathbf{g}$, $\mathbf{b} + \mathbf{g}$인 평행사변형의 넓이는 $|\det(\mathbf{A})|$예요. $2 \times 2$ 행렬의 행렬식은 ${\det\begin{bmatrix}a_{11} & a_{12} \\ a_{21} & a_{22}\end{bmatrix} = a_{11}a_{22} - a_{12}a_{21}}$예요.

- (a) ${\mathbf{b} = \begin{bmatrix}2 \\ 1\end{bmatrix}}$, ${\mathbf{g} = \begin{bmatrix}0 \\ 3\end{bmatrix}}$일 때 평행사변형의 넓이를 구해 보세요.
- (b) ${\mathbf{b} = \begin{bmatrix}2 \\ 1\end{bmatrix}}$, ${\mathbf{g} = \begin{bmatrix}4 \\ 2\end{bmatrix}}$일 때 넓이를 구하고, 왜 그런 값이 나오는지 설명해 보세요.

<details><summary>교과서 원문 보기</summary>

"the absolute value of the determinant of A is the area of the parallelogram with vertices 0, b, g, b + g" — Example 4.2

</details>

<details><summary>힌트 보기</summary>

$\mathbf{b}$를 첫째 열, $\mathbf{g}$를 둘째 열로 세워 행렬식을 계산해요. (b)에서는 두 벡터가 같은 방향인지 살펴보세요.

</details>

<details><summary>풀이 보기</summary>

1. (a) 두 벡터를 열로 세워요.

   $$
   \mathbf{A} = [\mathbf{b}, \mathbf{g}] = \begin{bmatrix}2 & 0 \\ 1 & 3\end{bmatrix}
   $$
2. 행렬식을 구하고 절댓값을 취해요.

   $$
   |\det(\mathbf{A})| = |2 \cdot 3 - 0 \cdot 1| = 6
   $$

   넓이는 6이에요.
3. (b) 같은 방법으로 세워요.

   $$
   \mathbf{A} = [\mathbf{b}, \mathbf{g}] = \begin{bmatrix}2 & 4 \\ 1 & 2\end{bmatrix}, \qquad |\det(\mathbf{A})| = |2 \cdot 2 - 4 \cdot 1| = 0
   $$
4. $\mathbf{g} = 2\mathbf{b}$라서 두 벡터는 선형종속(linearly dependent)이에요. 같은 직선 위에 있어 2차원 평행사변형을 만들지 못하고, 납작한 선분이 돼요. 그래서 넓이가 0이에요.

**정답:** (a) 넓이 6 (b) 넓이 0. $\mathbf{g} = 2\mathbf{b}$로 두 벡터가 선형종속이라 평행사변형이 납작해져요.

</details>

---

<a id="p2"></a>

### P2. 행렬식으로 역행렬 판정하기

$2 \times 2$ 행렬 ${\mathbf{A} = \begin{bmatrix}a_{11} & a_{12} \\ a_{21} & a_{22}\end{bmatrix}}$의 역행렬은 다음과 같아요.

$$
\mathbf{A}^{-1} = \frac{1}{a_{11}a_{22} - a_{12}a_{21}}\begin{bmatrix}a_{22} & -a_{12} \\ -a_{21} & a_{11}\end{bmatrix} \qquad (4.2)
$$

그래서 $\mathbf{A}$는 $a_{11}a_{22} - a_{12}a_{21} \ne 0$일 때만 역행렬을 가져요. 이 값이 행렬식 $\det(\mathbf{A})$예요. 이제 다음 행렬을 봐요.

$$
\boldsymbol{\Sigma} = \begin{bmatrix}4 & 2 \\ 2 & 10\end{bmatrix}
$$

- (a) $\det(\boldsymbol{\Sigma})$를 구하고, $\boldsymbol{\Sigma}$가 역행렬을 갖는지 판정해 보세요.
- (b) (4.2)로 $\boldsymbol{\Sigma}^{-1}$을 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"Let us begin with exploring if a square matrix A is invertible" — Example 4.1

</details>

<details><summary>힌트 보기</summary>

먼저 대각끼리 곱한 값에서 비대각끼리 곱한 값을 빼요. 0이 아니면 (4.2)에 넣으면 돼요.

</details>

<details><summary>풀이 보기</summary>

1. (a) 행렬식은 대각끼리 곱한 값에서 비대각끼리 곱한 값을 빼요.

   $$
   \det(\boldsymbol{\Sigma}) = 4 \cdot 10 - 2 \cdot 2 = 40 - 4 = 36
   $$
2. $36 \ne 0$이라 $\boldsymbol{\Sigma}$는 역행렬을 가져요.
3. (b) (4.2)에 넣어요. 대각 성분 4와 10은 자리를 맞바꾸고, 비대각 성분 2는 부호를 바꿔요.

   $$
   \boldsymbol{\Sigma}^{-1} = \frac{1}{36}\begin{bmatrix}10 & -2 \\ -2 & 4\end{bmatrix} = \begin{bmatrix}\frac{5}{18} & -\frac{1}{18} \\ -\frac{1}{18} & \frac{1}{9}\end{bmatrix}
   $$
4. 곱해서 확인해요.

   $$
   \begin{bmatrix}4 & 2 \\ 2 & 10\end{bmatrix}\begin{bmatrix}10 & -2 \\ -2 & 4\end{bmatrix} = \begin{bmatrix}36 & 0 \\ 0 & 36\end{bmatrix}
   $$

   이것을 36으로 나누면 $\mathbf{I}$가 되니 역행렬이 맞아요.

**정답:** (a) $\det(\boldsymbol{\Sigma}) = 36 \ne 0$이라 역행렬이 있어요. (b) ${\boldsymbol{\Sigma}^{-1} = \frac{1}{36}\begin{bmatrix}10 & -2 \\ -2 & 4\end{bmatrix}}$

</details>

---

<a id="p3"></a>

### P3. 선형 변환한 확률변수의 밀도 유도

상태가 ${\mathbf{x} = \begin{bmatrix}x_1 \\ x_2\end{bmatrix}}$인 2변수 확률변수 $X$의 밀도는 다음과 같아요.

$$
f(\mathbf{x}) = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{x}^\top\mathbf{x}\right) \qquad (6.145)
$$

행렬 ${\mathbf{A} = \begin{bmatrix}a & b \\ c & d\end{bmatrix}}$로 변환한 확률변수 $Y$의 상태는 $\mathbf{y} = \mathbf{A}\mathbf{x}$예요. $ad - bc \ne 0$이라 $\mathbf{A}$는 역행렬을 가져요. $\mathbf{A}^{-\top}$는 $(\mathbf{A}^{-1})^\top$을 뜻해요.

변수변환(change of variables)으로 $Y$의 밀도 $f(\mathbf{y})$를 유도해 보세요.

<details><summary>교과서 원문 보기</summary>

"We are interested in finding the probability density function of the transformed bivariate random variable Y with states y = Ax." — Example 6.17

</details>

<details><summary>힌트 보기</summary>

먼저 $\mathbf{x}$를 $\mathbf{y}$로 나타내 $f(\mathbf{x})$에 넣어요. 그다음 $\mathbf{A}$가 넓이를 몇 배로 바꾸는지 보고, 확률이 보존되도록 밀도를 그만큼 줄여요.

</details>

<details><summary>풀이 보기</summary>

1. 역변환을 구해요. 선형 변환이라 역행렬을 곱하면 돼요.

   $$
   \mathbf{x} = \mathbf{A}^{-1}\mathbf{y} = \frac{1}{ad - bc}\begin{bmatrix}d & -b \\ -c & a\end{bmatrix}\begin{bmatrix}y_1 \\ y_2\end{bmatrix}
   $$
2. $f(\mathbf{x})$에 대입해요. ${(\mathbf{A}^{-1}\mathbf{y})^\top = \mathbf{y}^\top\mathbf{A}^{-\top}}$이에요.

   $$
   f(\mathbf{A}^{-1}\mathbf{y}) = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{y}^\top\mathbf{A}^{-\top}\mathbf{A}^{-1}\mathbf{y}\right)
   $$
3. 넓이 배율을 봐요. $\mathbf{A}$는 $\mathbf{x}$ 쪽의 단위정사각형을 넓이 $|\det\mathbf{A}| = |ad - bc|$인 평행사변형으로 보내요. 확률은 그대로여야 하니 밀도는 $1/|ad - bc|$배가 돼요.
4. Jacobian으로도 같아요. ${\frac{\partial}{\partial \mathbf{y}}\mathbf{A}^{-1}\mathbf{y} = \mathbf{A}^{-1}}$이고, 행렬식은

   $$
   \det\left(\frac{\partial \mathbf{x}}{\partial \mathbf{y}}\right) = \det(\mathbf{A}^{-1}) = \frac{1}{ad - bc}
   $$
5. 2단계 식에 이 배율의 절댓값을 곱해요.

   $$
   f(\mathbf{y}) = f(\mathbf{A}^{-1}\mathbf{y})\left|\det\left(\frac{\partial \mathbf{x}}{\partial \mathbf{y}}\right)\right| = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{y}^\top\mathbf{A}^{-\top}\mathbf{A}^{-1}\mathbf{y}\right)|ad - bc|^{-1}
   $$

**정답:**

$$
f(\mathbf{y}) = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{y}^\top\mathbf{A}^{-\top}\mathbf{A}^{-1}\mathbf{y}\right)|ad - bc|^{-1}
$$

</details>

---

<a id="p4"></a>

### P4. 축을 늘리는 변환과 밀도

상태가 ${\mathbf{x} = \begin{bmatrix}x_1 \\ x_2\end{bmatrix}}$인 2변수 확률변수 $X$의 밀도는 다음과 같아요.

$$
f(\mathbf{x}) = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{x}^\top\mathbf{x}\right)
$$

행렬 ${\mathbf{A} = \begin{bmatrix}3 & 0 \\ 0 & 2\end{bmatrix}}$로 변환한 확률변수 $Y$의 상태는 $\mathbf{y} = \mathbf{A}\mathbf{x}$예요.

변수변환으로 $Y$의 밀도 $f(\mathbf{y})$를 구해 보세요. 원점에서의 값 $f(\mathbf{0})$도 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"We use the change-of-variable technique from Theorem 6.16 to derive the effect of a linear transformation" — Example 6.17

</details>

<details><summary>힌트 보기</summary>

$\mathbf{A}$는 $x_1$축을 3배, $x_2$축을 2배로 늘려요. 단위정사각형의 넓이가 몇 배가 되는지 보고, 밀도를 그만큼 줄여요.

</details>

<details><summary>풀이 보기</summary>

1. 역변환을 구해요. 대각 행렬이라 각 축을 따로 나누면 돼요.

   $$
   \mathbf{x} = \mathbf{A}^{-1}\mathbf{y} = \begin{bmatrix}\frac{1}{3} & 0 \\ 0 & \frac{1}{2}\end{bmatrix}\mathbf{y} = \begin{bmatrix}\frac{y_1}{3} \\ \frac{y_2}{2}\end{bmatrix}
   $$
2. $f(\mathbf{x})$에 대입해요. ${\mathbf{x}^\top\mathbf{x} = \mathbf{y}^\top\mathbf{A}^{-\top}\mathbf{A}^{-1}\mathbf{y}}$이고 ${\mathbf{A}^{-\top}\mathbf{A}^{-1} = \begin{bmatrix}\frac{1}{9} & 0 \\ 0 & \frac{1}{4}\end{bmatrix}}$이에요.

   $$
   \mathbf{x}^\top\mathbf{x} = \frac{y_1^2}{9} + \frac{y_2^2}{4}
   $$
3. 넓이 배율은 ${|\det\mathbf{A}| = |3 \cdot 2 - 0 \cdot 0| = 6}$이에요. 단위정사각형이 $3 \times 2$ 직사각형이 되니 넓이가 6배예요. 확률은 보존되니 밀도는 $\frac{1}{6}$배가 돼요. Jacobian 행렬식으로 쓰면 $\det(\mathbf{A}^{-1}) = \frac{1}{6}$이에요.
4. 둘을 곱해요. ${\frac{1}{2\pi} \cdot \frac{1}{6} = \frac{1}{12\pi}}$예요.

   $$
   f(\mathbf{y}) = \frac{1}{12\pi}\exp\left(-\frac{1}{2}\left(\frac{y_1^2}{9} + \frac{y_2^2}{4}\right)\right)
   $$
5. 원점에서는 지수부가 0이라 $\exp(0) = 1$이에요.

   $$
   f(\mathbf{0}) = \frac{1}{12\pi}
   $$

**정답:** $|\det\mathbf{A}| = 6$,

$$
f(\mathbf{y}) = \frac{1}{12\pi}\exp\left(-\frac{1}{2}\left(\frac{y_1^2}{9} + \frac{y_2^2}{4}\right)\right)
$$

$f(\mathbf{0}) = \frac{1}{12\pi}$

</details>

---

<a id="p5"></a>

### P5. 기울이는 변환과 밀도

상태가 ${\mathbf{x} = \begin{bmatrix}x_1 \\ x_2\end{bmatrix}}$인 2변수 확률변수 $X$의 밀도는 다음과 같아요.

$$
f(\mathbf{x}) = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{x}^\top\mathbf{x}\right)
$$

행렬 ${\mathbf{A} = \begin{bmatrix}1 & 1 \\ 0 & 2\end{bmatrix}}$로 변환한 확률변수 $Y$의 상태는 $\mathbf{y} = \mathbf{A}\mathbf{x}$예요.

- (a) 역변환 $\mathbf{x} = \mathbf{A}^{-1}\mathbf{y}$를 구해 보세요.
- (b) Jacobian $\frac{\partial \mathbf{x}}{\partial \mathbf{y}}$의 행렬식을 구해 보세요.
- (c) $Y$의 밀도 $f(\mathbf{y})$를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"Recall that for change of variables we require the inverse transformation of x as a function of y." — Example 6.17

</details>

<details><summary>힌트 보기</summary>

$\mathbf{x}^\top\mathbf{x}$에 역변환을 넣고 전개해요. 밀도는 $\mathbf{A}$의 넓이 배율 $|\det\mathbf{A}|$로 나눠요.

</details>

<details><summary>풀이 보기</summary>

1. (a) ${\det\mathbf{A} = 1 \cdot 2 - 1 \cdot 0 = 2}$예요. 2×2 역행렬 공식으로

   $$
   \mathbf{A}^{-1} = \frac{1}{2}\begin{bmatrix}2 & -1 \\ 0 & 1\end{bmatrix} = \begin{bmatrix}1 & -\frac{1}{2} \\ 0 & \frac{1}{2}\end{bmatrix}
   $$

   성분으로 쓰면 $x_1 = y_1 - \frac{1}{2}y_2$, $x_2 = \frac{1}{2}y_2$예요.
2. (b) ${\frac{\partial}{\partial \mathbf{y}}\mathbf{A}^{-1}\mathbf{y} = \mathbf{A}^{-1}}$이에요. 행렬식은

   $$
   \det\left(\frac{\partial \mathbf{x}}{\partial \mathbf{y}}\right) = 1 \cdot \frac{1}{2} - \left(-\frac{1}{2}\right) \cdot 0 = \frac{1}{2}
   $$

   $\mathbf{A}$가 넓이를 2배로 늘리니 밀도는 $\frac{1}{2}$배가 된다는 뜻이에요.
3. (c) 지수부를 정리해요. ${\mathbf{x}^\top\mathbf{x} = \mathbf{y}^\top\mathbf{A}^{-\top}\mathbf{A}^{-1}\mathbf{y}}$이고

   $$
   \mathbf{A}^{-\top}\mathbf{A}^{-1} = \begin{bmatrix}1 & 0 \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix}\begin{bmatrix}1 & -\frac{1}{2} \\ 0 & \frac{1}{2}\end{bmatrix} = \begin{bmatrix}1 & -\frac{1}{2} \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix}
   $$
4. 성분으로 전개해도 같아요.

   $$
   x_1^2 + x_2^2 = \left(y_1 - \frac{1}{2}y_2\right)^2 + \frac{1}{4}y_2^2 = y_1^2 - y_1 y_2 + \frac{1}{2}y_2^2
   $$
5. $f(\mathbf{A}^{-1}\mathbf{y})$에 Jacobian 행렬식의 절댓값 $\frac{1}{2}$를 곱해요. ${\frac{1}{2\pi} \cdot \frac{1}{2} = \frac{1}{4\pi}}$예요.

   $$
   f(\mathbf{y}) = \frac{1}{4\pi}\exp\left(-\frac{1}{2}\left(y_1^2 - y_1 y_2 + \frac{1}{2}y_2^2\right)\right)
   $$

**정답:** (a) ${\mathbf{A}^{-1} = \begin{bmatrix}1 & -\frac{1}{2} \\ 0 & \frac{1}{2}\end{bmatrix}}$ (b) $\frac{1}{2}$ (c)

$$
f(\mathbf{y}) = \frac{1}{4\pi}\exp\left(-\frac{1}{2}\left(y_1^2 - y_1 y_2 + \frac{1}{2}y_2^2\right)\right)
$$

</details>

---

<a id="partB"></a>

## B. 교과서 연습문제

<a id="p6"></a>

### P6. 잡음이 섞인 아핀 변환의 교차공분산

가우시안 확률변수 $\mathbf{x} \sim \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$가 있고 $\mathbf{x} \in \mathbb{R}^D$예요. 여기에

$$
\mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{b} + \mathbf{w}
$$

를 만들어요. $\mathbf{y} \in \mathbb{R}^E$, $\mathbf{A} \in \mathbb{R}^{E \times D}$, $\mathbf{b} \in \mathbb{R}^E$이고, $\mathbf{w} \sim \mathcal{N}(\mathbf{w} \mid \mathbf{0}, \mathbf{Q})$는 독립인 가우시안 잡음이에요. 독립이란 $\mathbf{x}$와 $\mathbf{w}$가 서로 독립이고 $\mathbf{Q}$가 대각 행렬이라는 뜻이에요.

교차공분산 $\mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}]$와 $\mathrm{Cov}_{y,x}[\mathbf{y}, \mathbf{x}]$를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

"This also requires us to compute the cross-covariances $\mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}]$ and $\mathrm{Cov}_{y,x}[\mathbf{y}, \mathbf{x}]$." — Exercise 6.12 (d) Hint

</details>

<details><summary>힌트 보기</summary>

$\mathbf{y}$에서 평균을 빼면 $\mathbf{b}$가 사라져요. 정의 $\mathbb{E}[(\mathbf{x} - \boldsymbol{\mu}_x)(\mathbf{y} - \boldsymbol{\mu}_y)^\top]$에 넣고, $\mathbf{w}$가 들어간 항은 독립이라 0이 돼요.

</details>

<details><summary>풀이 보기</summary>

1. $\mathbf{y}$의 평균부터 구해요. 기댓값은 linear operator이고 $\mathbb{E}[\mathbf{w}] = \mathbf{0}$이에요.

   $$
   \boldsymbol{\mu}_y = \mathbb{E}[\mathbf{y}] = \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}
   $$
2. 편차를 구해요. $\mathbf{b}$는 빠져요.

   $$
   \mathbf{y} - \boldsymbol{\mu}_y = \mathbf{A}(\mathbf{x} - \boldsymbol{\mu}_x) + \mathbf{w}
   $$
3. 교차공분산의 정의에 넣고 ${(\mathbf{A}\mathbf{B})^\top = \mathbf{B}^\top\mathbf{A}^\top}$를 써요.

   $$
   \mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}] = \mathbb{E}[(\mathbf{x} - \boldsymbol{\mu}_x)(\mathbf{x} - \boldsymbol{\mu}_x)^\top]\mathbf{A}^\top + \mathbb{E}[(\mathbf{x} - \boldsymbol{\mu}_x)\mathbf{w}^\top]
   $$

   $\mathbf{A}^\top$는 deterministic이라 기댓값 밖으로 나와요.
4. $\mathbf{x}$와 $\mathbf{w}$는 독립이라 교차공분산이 0이에요. ${\mathbb{E}[(\mathbf{x} - \boldsymbol{\mu}_x)\mathbf{w}^\top] = \mathbb{E}[\mathbf{x} - \boldsymbol{\mu}_x]\,\mathbb{E}[\mathbf{w}]^\top = \mathbf{0}}$이에요. 그래서

   $$
   \mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}] = \boldsymbol{\Sigma}_x\mathbf{A}^\top
   $$
5. 반대 순서는 전치예요. $\boldsymbol{\Sigma}_x$는 대칭이라 ${\boldsymbol{\Sigma}_x^\top = \boldsymbol{\Sigma}_x}$예요.

   $$
   \mathrm{Cov}_{y,x}[\mathbf{y}, \mathbf{x}] = \left(\boldsymbol{\Sigma}_x\mathbf{A}^\top\right)^\top = \mathbf{A}\boldsymbol{\Sigma}_x
   $$

**정답:** ${\mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}] = \boldsymbol{\Sigma}_x\mathbf{A}^\top}$, ${\mathrm{Cov}_{y,x}[\mathbf{y}, \mathbf{x}] = \mathbf{A}\boldsymbol{\Sigma}_x}$

</details>

---

<a id="p7"></a>

### P7. 결합 가우시안 p(x, y) 세우기

가우시안 확률변수 $\mathbf{x} \sim \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$가 있고 $\mathbf{x} \in \mathbb{R}^D$예요. 여기에

$$
\mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{b} + \mathbf{w}
$$

를 만들어요. $\mathbf{y} \in \mathbb{R}^E$, $\mathbf{A} \in \mathbb{R}^{E \times D}$, $\mathbf{b} \in \mathbb{R}^E$이고, $\mathbf{w} \sim \mathcal{N}(\mathbf{w} \mid \mathbf{0}, \mathbf{Q})$는 독립인 가우시안 잡음이에요. 독립이란 $\mathbf{x}$와 $\mathbf{w}$가 서로 독립이고 $\mathbf{Q}$가 대각 행렬이라는 뜻이에요. 결합분포 $p(\mathbf{x}, \mathbf{y})$는 가우시안이에요. 교차공분산은 다음과 같이 주어져요.

$$
\mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}] = \boldsymbol{\Sigma}_x\mathbf{A}^\top, \qquad \mathrm{Cov}_{y,x}[\mathbf{y}, \mathbf{x}] = \mathbf{A}\boldsymbol{\Sigma}_x
$$

$\mathbf{y}$의 평균과 공분산 $\mathrm{Var}[\mathbf{y}]$를 구해서, 결합분포 $p(\mathbf{x}, \mathbf{y})$의 평균 벡터와 공분산 행렬(블록 행렬)을 완성해 보세요.

<details><summary>교과서 원문 보기</summary>

"Start by explicitly computing the joint Gaussian p(x, y)." — Exercise 6.12 (d) Hint

</details>

<details><summary>힌트 보기</summary>

$\begin{bmatrix}\mathbf{x} \\ \mathbf{y}\end{bmatrix}$의 공분산은 $\mathrm{Var}[\mathbf{x}]$, $\mathrm{Var}[\mathbf{y}]$와 두 교차공분산으로 된 블록 행렬이에요. 교차공분산은 주어졌으니 $\mathrm{Var}[\mathbf{y}]$만 구하면 돼요. $\mathbf{y}$의 편차는 $\mathbf{A}(\mathbf{x} - \boldsymbol{\mu}_x) + \mathbf{w}$이고, $\mathbf{w}$와 $\mathbf{x}$가 만나는 항은 0이에요.

</details>

<details><summary>풀이 보기</summary>

1. 평균을 구해요. 기댓값은 linear operator이고 $\mathbb{E}[\mathbf{w}] = \mathbf{0}$이에요.

   $$
   \boldsymbol{\mu}_y = \mathbb{E}[\mathbf{y}] = \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}
   $$
2. 편차는 ${\mathbf{y} - \boldsymbol{\mu}_y = \mathbf{A}(\mathbf{x} - \boldsymbol{\mu}_x) + \mathbf{w}}$예요. $\mathbf{x}$와 $\mathbf{w}$는 독립이라 교차공분산이 0이에요. ${\mathbb{E}[(\mathbf{x} - \boldsymbol{\mu}_x)\mathbf{w}^\top] = \mathbf{0}}$이에요.
3. $\mathbf{y}$의 공분산을 정의대로 전개해요. $\mathbf{w}$와 $\mathbf{x}$가 만나는 두 항은 0이에요.

   $$
   \mathrm{Var}[\mathbf{y}] = \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbb{E}[\mathbf{w}\mathbf{w}^\top] = \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q}
   $$
4. 교차공분산은 주어진 대로 $\boldsymbol{\Sigma}_x\mathbf{A}^\top$와 $\mathbf{A}\boldsymbol{\Sigma}_x$예요. 왼쪽 위 블록은 ${\mathrm{Var}[\mathbf{x}] = \boldsymbol{\Sigma}_x}$예요.
5. 블록으로 모아요. 결합분포가 가우시안이니 이 평균과 공분산으로 정해져요.

   $$
   p(\mathbf{x}, \mathbf{y}) = \mathcal{N}\left(\begin{bmatrix}\boldsymbol{\mu}_x \\ \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}\end{bmatrix}, \begin{bmatrix}\boldsymbol{\Sigma}_x & \boldsymbol{\Sigma}_x\mathbf{A}^\top \\ \mathbf{A}\boldsymbol{\Sigma}_x & \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q}\end{bmatrix}\right)
   $$

**정답:** 평균 $\begin{bmatrix}\boldsymbol{\mu}_x \\ \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}\end{bmatrix}$, 공분산 $\begin{bmatrix}\boldsymbol{\Sigma}_x & \boldsymbol{\Sigma}_x\mathbf{A}^\top \\ \mathbf{A}\boldsymbol{\Sigma}_x & \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q}\end{bmatrix}$

</details>

---

<a id="p8"></a>

### P8. 시계열 모델의 다음 상태와 관측

다음 시계열 모델을 봐요.

$$
\mathbf{x}_{t+1} = \mathbf{A}\mathbf{x}_t + \mathbf{w}, \qquad \mathbf{w} \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})
$$

$$
\mathbf{y}_t = \mathbf{C}\mathbf{x}_t + \mathbf{v}, \qquad \mathbf{v} \sim \mathcal{N}(\mathbf{0}, \mathbf{R})
$$

$\mathbf{w}$와 $\mathbf{v}$는 i.i.d. 가우시안 잡음이에요. 또 ${p(\mathbf{x}_0) = \mathcal{N}(\boldsymbol{\mu}_0, \boldsymbol{\Sigma}_0)}$이에요. 지금까지의 관측으로 본 현재 상태가 다음과 같다고 해요.

$$
p(\mathbf{x}_t \mid \mathbf{y}_1, \dots, \mathbf{y}_t) = \mathcal{N}(\boldsymbol{\mu}_t, \boldsymbol{\Sigma}_t)
$$

$p(\mathbf{x}_{t+1}, \mathbf{y}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t)$는 가우시안이에요.

$p(\mathbf{x}_{t+1}, \mathbf{y}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t)$를 구해 보세요. 평균 벡터와 공분산 행렬(블록 행렬)을 구하면 돼요.

<details><summary>교과서 원문 보기</summary>

"Compute $p(\mathbf{x}_{t+1}, \mathbf{y}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t)$." — Exercise 6.5 (b) 2

</details>

<details><summary>힌트 보기</summary>

먼저 ${\mathbf{x}_{t+1} = \mathbf{A}\mathbf{x}_t + \mathbf{w}}$의 평균과 공분산 $\mathbf{P}$를 구해요. 그다음 ${\mathbf{y}_{t+1} = \mathbf{C}\mathbf{x}_{t+1} + \mathbf{v}}$로 나머지 블록을 채워요. 잡음은 다른 것과 독립이라 교차공분산이 0이에요.

</details>

<details><summary>풀이 보기</summary>

1. 모든 기댓값은 $\mathbf{y}_1, \dots, \mathbf{y}_t$가 주어진 조건 아래에서 계산해요. 이 조건 아래 $\mathbf{x}_t$의 평균은 $\boldsymbol{\mu}_t$, 공분산은 $\boldsymbol{\Sigma}_t$예요. 새 잡음 $\mathbf{w}$, $\mathbf{v}$는 $\mathbf{x}_t$와 지난 관측에 독립이고 평균이 $\mathbf{0}$이에요.
2. $\mathbf{x}_{t+1}$의 평균은 같은 꼴로 따라가요.

   $$
   \mathbb{E}[\mathbf{x}_{t+1}] = \mathbf{A}\boldsymbol{\mu}_t
   $$
3. 편차는 ${\mathbf{x}_{t+1} - \mathbf{A}\boldsymbol{\mu}_t = \mathbf{A}(\mathbf{x}_t - \boldsymbol{\mu}_t) + \mathbf{w}}$예요. $\mathbf{x}_t$와 $\mathbf{w}$는 독립이라 둘이 만나는 항은 0이에요.

   $$
   \mathbf{P} := \mathrm{Var}[\mathbf{x}_{t+1}] = \mathbf{A}\boldsymbol{\Sigma}_t\mathbf{A}^\top + \mathbf{Q}
   $$

   즉 ${p(\mathbf{x}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t) = \mathcal{N}(\mathbf{A}\boldsymbol{\mu}_t, \mathbf{P})}$예요.
4. ${\mathbf{y}_{t+1} = \mathbf{C}\mathbf{x}_{t+1} + \mathbf{v}}$의 평균은

   $$
   \mathbb{E}[\mathbf{y}_{t+1}] = \mathbf{C}\mathbf{A}\boldsymbol{\mu}_t
   $$
5. 편차는 ${\mathbf{y}_{t+1} - \mathbf{C}\mathbf{A}\boldsymbol{\mu}_t = \mathbf{C}(\mathbf{x}_{t+1} - \mathbf{A}\boldsymbol{\mu}_t) + \mathbf{v}}$예요. $\mathbf{v}$는 $\mathbf{x}_{t+1}$과 독립이라 교차항이 0이에요.

   $$
   \mathrm{Var}[\mathbf{y}_{t+1}] = \mathbf{C}\mathbf{P}\mathbf{C}^\top + \mathbf{R}
   $$
6. 교차공분산은 정의 $\mathbb{E}[(\mathbf{x}_{t+1} - \mathbf{A}\boldsymbol{\mu}_t)(\mathbf{y}_{t+1} - \mathbf{C}\mathbf{A}\boldsymbol{\mu}_t)^\top]$에 편차를 넣어요. $\mathbf{C}^\top$는 밖으로 나오고 $\mathbf{v}$ 항은 0이에요.

   $$
   \mathrm{Cov}[\mathbf{x}_{t+1}, \mathbf{y}_{t+1}] = \mathbf{P}\mathbf{C}^\top, \qquad \mathrm{Cov}[\mathbf{y}_{t+1}, \mathbf{x}_{t+1}] = \mathbf{C}\mathbf{P}
   $$

   $\mathbf{P}$는 대칭이라 ${(\mathbf{P}\mathbf{C}^\top)^\top = \mathbf{C}\mathbf{P}}$예요.
7. 블록으로 모아요. 결합분포가 가우시안이니 이 평균과 공분산으로 정해져요.

   $$
   p(\mathbf{x}_{t+1}, \mathbf{y}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t) = \mathcal{N}\left(\begin{bmatrix}\mathbf{A}\boldsymbol{\mu}_t \\ \mathbf{C}\mathbf{A}\boldsymbol{\mu}_t\end{bmatrix}, \begin{bmatrix}\mathbf{P} & \mathbf{P}\mathbf{C}^\top \\ \mathbf{C}\mathbf{P} & \mathbf{C}\mathbf{P}\mathbf{C}^\top + \mathbf{R}\end{bmatrix}\right)
   $$

**정답:** ${\mathbf{P} := \mathbf{A}\boldsymbol{\Sigma}_t\mathbf{A}^\top + \mathbf{Q}}$일 때 평균 $\begin{bmatrix}\mathbf{A}\boldsymbol{\mu}_t \\ \mathbf{C}\mathbf{A}\boldsymbol{\mu}_t\end{bmatrix}$, 공분산 $\begin{bmatrix}\mathbf{P} & \mathbf{P}\mathbf{C}^\top \\ \mathbf{C}\mathbf{P} & \mathbf{C}\mathbf{P}\mathbf{C}^\top + \mathbf{R}\end{bmatrix}$

</details>

---

출처: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* (Cambridge University Press, 2020). 풀이는 자체 작성이며 수치는 Python으로 검증했습니다.
