# 복습문제 5선 — 0909 수업 범위

교과서 본문 예제 변형 **1문항**(MML Example 9.1: 기울기 θ인 직선 모델)과 교과서 연습문제 **4문항**(MML Exercise 2.4: 행렬 곱의 크기 맞추기, 성분마다 내적)으로 구성했어요. 먼저 풀어 보고, 막히면 힌트를 열어 보세요.

> `복습문제_0909_Data_Models_Learning.html`를 마크다운으로 옮겼어요. 원문, 힌트, 풀이는 접혀 있어요. 먼저 풀어 보고 펼쳐 보세요.

**목차**

- [A. 교과서 예제 변형 (MML 9장)](#partA)
  - [P1. 기울기만 다른 세 직선](#p1)
- [B. 교과서 연습문제 (MML 2장)](#partB)
  - [P2. 곱할 수 있는 행렬인가요?](#p2)
  - [P3. 3×3 행렬 두 번 곱하기](#p3)
  - [P4. 넓은 행렬과 긴 행렬의 곱](#p4)
  - [P5. 긴 행렬과 넓은 행렬의 곱](#p5)

<a id="partA"></a>

## A. 교과서 예제 변형 (MML 9장)

<a id="p1"></a>

### P1. 기울기만 다른 세 직선

입력과 파라미터가 모두 실수($x, \theta \in \mathbb{R}$)인 직선 모델 $f(x) = \theta x$가 있어요. 여기서 $\theta$는 직선의 기울기예요.

- (a) $\theta = -1$, $\theta = \frac{1}{2}$, $\theta = 2$일 때 각각 $f(10)$을 구해 보세요.
- (b) 세 직선 중 가장 가파른 것은 어느 것인가요? $\theta$가 무엇을 뜻하는지와 이어서 말해 보세요.

<details><summary>교과서 원문 보기</summary>

"For x, θ ∈ ℝ the linear regression model … describes straight lines (linear functions), and the parameter θ is the slope of the line." — Example 9.1

</details>

<details><summary>힌트 보기</summary>

$\theta$ 값을 넣고 $x = 10$을 곱하면 돼요. (b)는 $x$가 1 늘 때 $f(x)$가 얼마나 느는지 보세요.

</details>

<details><summary>풀이 보기</summary>

1. $\theta = -1$: $f(10) = -1 \cdot 10 = -10$이에요.
2. $\theta = \frac{1}{2}$: $f(10) = \frac{1}{2} \cdot 10 = 5$예요.
3. $\theta = 2$: $f(10) = 2 \cdot 10 = 20$이에요.
4. $x$가 1 늘면 $f(x)$는 $\theta$만큼 변해요. $\theta$가 기울기라서, $\theta = 2$인 직선이 가장 가파르게 올라가요. $\theta = -1$인 직선은 오른쪽으로 갈수록 내려가요.
5. 수업에서는 $f(\mathbf{x}) = \boldsymbol{\theta}^\top \mathbf{x} + \theta_0$을 배웠어요. 이 문제는 $D = 1$, $\theta_0 = 0$인 경우라서 내적이 곱셈 $\theta x$ 하나로 줄어요.

**정답:** (a) $f(10) = -10,\ 5,\ 20$ (차례로 $\theta = -1, \frac{1}{2}, 2$), (b) $\theta = 2$인 직선. $\theta$가 기울기라서 클수록 가파른 직선이에요.

</details>

---

<a id="partB"></a>

## B. 교과서 연습문제 (MML 2장)

<a id="p2"></a>

### P2. 곱할 수 있는 행렬인가요?

다음 행렬 곱을 계산해 보세요. 계산할 수 없다면 그 이유를 말해 보세요.

$$
\left[\begin{matrix}1 \\ 4 \\ 7\end{matrix}\;\;\begin{matrix}2 \\ 5 \\ 8\end{matrix}\right]\left[\begin{matrix}1 \\ 0 \\ 1\end{matrix}\;\;\begin{matrix}1 \\ 1 \\ 0\end{matrix}\;\;\begin{matrix}0 \\ 1 \\ 1\end{matrix}\right]
$$

<details><summary>교과서 원문 보기</summary>

"Compute the following matrix products, if possible:" — Exercise 2.4 (a)

</details>

<details><summary>힌트 보기</summary>

행렬 곱의 각 칸은 앞 행렬의 행과 뒤 행렬의 열의 내적이에요. 두 벡터의 길이가 같은지 먼저 보세요.

</details>

<details><summary>풀이 보기</summary>

1. 앞 행렬은 행 3개, 열 2개라서 $3 \times 2$예요. 뒤 행렬은 $3 \times 3$이에요.
2. 곱의 한 칸을 만들려면 앞 행렬의 행(길이 2)과 뒤 행렬의 열(길이 3)을 내적해야 해요.
3. 길이가 $2 \neq 3$으로 달라서 내적을 할 수 없어요. 그래서 이 곱은 정의되지 않아요.
4. 수업의 차원 검증에서 $\boldsymbol{\theta}^\top \mathbf{x}$는 두 벡터의 길이가 같아야 내적할 수 있다고 했어요. 행렬 곱도 같은 규칙이에요.

**정답:** 계산할 수 없어요. $3 \times 2$ 행렬의 열 수 2와 $3 \times 3$ 행렬의 행 수 3이 달라서 곱이 정의되지 않아요.

</details>

---

<a id="p3"></a>

### P3. 3×3 행렬 두 번 곱하기

다음 두 행렬 곱을 각각 계산해 보세요.

- (b)

  $$
  \left[\begin{matrix}1 \\ 4 \\ 7\end{matrix}\;\;\begin{matrix}2 \\ 5 \\ 8\end{matrix}\;\;\begin{matrix}3 \\ 6 \\ 9\end{matrix}\right]\left[\begin{matrix}1 \\ 0 \\ 1\end{matrix}\;\;\begin{matrix}1 \\ 1 \\ 0\end{matrix}\;\;\begin{matrix}0 \\ 1 \\ 1\end{matrix}\right]
  $$
- (c)

  $$
  \left[\begin{matrix}1 \\ 0 \\ 1\end{matrix}\;\;\begin{matrix}1 \\ 1 \\ 0\end{matrix}\;\;\begin{matrix}0 \\ 1 \\ 1\end{matrix}\right]\left[\begin{matrix}1 \\ 4 \\ 7\end{matrix}\;\;\begin{matrix}2 \\ 5 \\ 8\end{matrix}\;\;\begin{matrix}3 \\ 6 \\ 9\end{matrix}\right]
  $$

<details><summary>교과서 원문 보기</summary>

"Compute the following matrix products, if possible:" — Exercise 2.4 (b), (c)

</details>

<details><summary>힌트 보기</summary>

$i$행 $j$열 칸 = 앞 행렬의 $i$번째 행과 뒤 행렬의 $j$번째 열의 내적이에요. 둘 다 $3 \times 3$끼리라 곱할 수 있어요.

</details>

<details><summary>풀이 보기</summary>

1. (b) 첫 행 $[1, 2, 3]$과 첫 열 $[1, 0, 1]^\top$의 내적은 $1 + 0 + 3 = 4$예요. 같은 방법으로 첫 행을 채우면 $[4, 3, 5]$예요.
2. (b) 나머지 행도 채우면 $[10, 9, 11]$, $[16, 15, 17]$이에요.
3. (c) 첫 행 $[1, 1, 0]$과 첫 열 $[1, 4, 7]^\top$의 내적은 $1 + 4 + 0 = 5$예요. 첫 행은 $[5, 7, 9]$예요.
4. (c) 나머지 행은 $[11, 13, 15]$, $[8, 10, 12]$예요.
5. 수업의 차원 검증에서 $\boldsymbol{\theta}^\top \mathbf{x}$는 길이가 같은 행벡터와 열벡터의 내적이라 스칼라 하나가 나온다고 했어요. 행렬 곱의 한 칸도 똑같이 길이 3인 행과 열의 내적이에요. 길이가 다르면($3 \neq 2$처럼) 그 칸은 만들 수 없어요.

**정답:** (b)

$$
\left[\begin{matrix}4 \\ 10 \\ 16\end{matrix}\;\;\begin{matrix}3 \\ 9 \\ 15\end{matrix}\;\;\begin{matrix}5 \\ 11 \\ 17\end{matrix}\right]
$$

(c)

$$
\left[\begin{matrix}5 \\ 11 \\ 8\end{matrix}\;\;\begin{matrix}7 \\ 13 \\ 10\end{matrix}\;\;\begin{matrix}9 \\ 15 \\ 12\end{matrix}\right]
$$

</details>

---

<a id="p4"></a>

### P4. 넓은 행렬과 긴 행렬의 곱

다음 행렬 곱을 계산해 보세요. 결과 행렬의 크기도 함께 말해 보세요.

$$
\left[\begin{matrix}1 \\ 4\end{matrix}\;\;\begin{matrix}2 \\ 1\end{matrix}\;\;\begin{matrix}1 \\ -1\end{matrix}\;\;\begin{matrix}2 \\ -4\end{matrix}\right]\left[\begin{matrix}0 \\ 1 \\ 2 \\ 5\end{matrix}\;\;\begin{matrix}3 \\ -1 \\ 1 \\ 2\end{matrix}\right]
$$

<details><summary>교과서 원문 보기</summary>

"Compute the following matrix products, if possible:" — Exercise 2.4 (d)

</details>

<details><summary>힌트 보기</summary>

앞 행렬의 열 수와 뒤 행렬의 행 수가 같으면 곱할 수 있어요. 결과 크기는 (앞의 행 수) $\times$ (뒤의 열 수)예요.

</details>

<details><summary>풀이 보기</summary>

1. 앞은 $2 \times 4$, 뒤는 $4 \times 2$예요. 가운데 4가 같아서 곱할 수 있고, 결과는 $2 \times 2$예요.
2. 1행 1열: $1 \cdot 0 + 2 \cdot 1 + 1 \cdot 2 + 2 \cdot 5 = 14$, 1행 2열: $3 - 2 + 1 + 4 = 6$이에요.
3. 2행 1열: $0 + 1 - 2 - 20 = -21$, 2행 2열: $12 - 1 - 1 - 8 = 2$예요.
4. 수업에서 $\mathbf{x}_n \in \mathbb{R}^D$와 $\boldsymbol{\theta}$의 길이가 같아야 내적이 된다고 했어요. 여기선 길이 4짜리 행과 열을 내적해서 칸 하나씩 스칼라를 얻어요.

**정답:**

$$
\left[\begin{matrix}14 \\ -21\end{matrix}\;\;\begin{matrix}6 \\ 2\end{matrix}\right]
$$

($2 \times 4$ 곱하기 $4 \times 2$ = $2 \times 2$)

</details>

---

<a id="p5"></a>

### P5. 긴 행렬과 넓은 행렬의 곱

다음 행렬 곱을 계산해 보세요. 결과 행렬의 크기도 함께 말해 보세요.

$$
\left[\begin{matrix}0 \\ 1 \\ 2 \\ 5\end{matrix}\;\;\begin{matrix}3 \\ -1 \\ 1 \\ 2\end{matrix}\right]\left[\begin{matrix}1 \\ 4\end{matrix}\;\;\begin{matrix}2 \\ 1\end{matrix}\;\;\begin{matrix}1 \\ -1\end{matrix}\;\;\begin{matrix}2 \\ -4\end{matrix}\right]
$$

<details><summary>교과서 원문 보기</summary>

"Compute the following matrix products, if possible:" — Exercise 2.4 (e)

</details>

<details><summary>힌트 보기</summary>

이번엔 행 하나의 길이가 2라서 칸마다 곱 두 개만 더하면 돼요. 대신 칸이 많아요.

</details>

<details><summary>풀이 보기</summary>

1. 앞은 $4 \times 2$, 뒤는 $2 \times 4$예요. 가운데 2가 같아서 곱할 수 있고, 결과는 $4 \times 4$예요.
2. 1행 $[0, 3]$: 뒤 행렬의 열 $[1,4]^\top, [2,1]^\top, [1,-1]^\top, [2,-4]^\top$과 내적하면 $12, 3, -3, -12$예요.
3. 2행 $[1, -1]$: $-3, 1, 2, 6$이에요. 3행 $[2, 1]$: $6, 5, 1, 0$이에요.
4. 4행 $[5, 2]$: $5 + 8 = 13$, $10 + 2 = 12$, $5 - 2 = 3$, $10 - 8 = 2$예요.
5. 결과가 $4 \times 4$로 커졌어요. 수업의 차원 검증처럼 곱하기 전에 크기부터 맞춰 보면 결과 모양이 먼저 보여요.

**정답:**

$$
\left[\begin{matrix}12 \\ -3 \\ 6 \\ 13\end{matrix}\;\;\begin{matrix}3 \\ 1 \\ 5 \\ 12\end{matrix}\;\;\begin{matrix}-3 \\ 2 \\ 1 \\ 3\end{matrix}\;\;\begin{matrix}-12 \\ 6 \\ 0 \\ 2\end{matrix}\right]
$$

($4 \times 2$ 곱하기 $2 \times 4$ = $4 \times 4$)

</details>

---

출처: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* (Cambridge University Press, 2020). 풀이는 자체 작성이며 수치는 Python으로 검증했습니다.
