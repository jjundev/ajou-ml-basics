# 머신러닝기초 과제 1 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [P1. 전치 구하기](#p1)
  - [P2. 내적과 노름](#p2)
  - [P3. 행렬 곱의 순서](#p3)
  - [P4. 행렬식 계산](#p4)
  - [P5. 역행렬 구하기](#p5)
  - [P6. 선형 독립 판정](#p6)
  - [P7. 선형결합으로 나타내기](#p7)
  - [P8. $\mathbf{A}^\top\mathbf{A}$와 역행렬](#p8)
  - [P9. 특징 행렬과 예측](#p9)
  - [P10. gradient 구하기](#p10)
  - [P11. 야코비 행렬](#p11)
  - [P12. 이차형식의 정류점](#p12)
  - [P13. 2차원 가우시안 밀도](#p13)
  - [P14. 완전제곱으로 정규화](#p14)
  - [P15. 단순회귀의 우도](#p15)
  - [P16. 음의 로그우도와 최소제곱](#p16)
  - [P17. 정규방정식과 수치 예](#p17)
  - [P18. MAP과 릿지 회귀](#p18)
  - [P19. ML과 MAP 수치 비교](#p19)
  - [P20. 특이한 $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}$와 규제](#p20)
  - [P21. 표본 평균과 공분산](#p21)
  - [P22. 아핀 변환의 평균과 공분산](#p22)
  - [P23. 절편 없는 회귀의 ML과 MAP](#p23)
  - [P24. 평균 추정의 ML과 MAP](#p24)
  - [P25. 두 가우시안의 곱](#p25)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### P1. 전치 구하기

HW1 Problem 1 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p1)

#### 주어진 조건

모든 벡터는 열벡터예요. 다음 행렬과 벡터가 주어져요.

$$
{\mathbf{A}=\begin{bmatrix}1 & -2 & 3\\0 & 4 & 5\end{bmatrix}},\quad{\mathbf{b}=\begin{bmatrix}2\\-1\\4\end{bmatrix}},\quad{\mathbf{C}=\begin{bmatrix}1 & 2 & 0\\-1 & 3 & 4\\5 & 0 & -2\end{bmatrix}}
$$

#### 구할 것

각각의 전치를 구해 보세요.

- (a) $\mathbf{A}^\top$
- (b) $\mathbf{b}^\top$
- (c) $\mathbf{C}^\top$

#### 과제 원문

"Find the transpose of each matrix or vector.

(a) ${\mathbf{A}=\begin{bmatrix}1 & -2 & 3\\0 & 4 & 5\end{bmatrix}}$.

(b) ${\mathbf{b}=\begin{bmatrix}2\\-1\\4\end{bmatrix}}$.

(c) ${\mathbf{C}=\begin{bmatrix}1 & 2 & 0\\-1 & 3 & 4\\5 & 0 & -2\end{bmatrix}}$."

#### 무엇을 구하는 문제인가요?

숫자를 바꾸는 문제가 아니라 자리의 방향을 바꾸는 문제예요. 행을 열로 옮기고, 결과의 크기도 함께 적어요.

#### 종이에 쓸 첫 줄

$(A^\top)_{ij}=A_{ji}$부터 써요. 전치(transpose)의 정의가 이 식이라, 원래 첫 행을 결과의 첫 열로 세우면 돼요. $2\times3\to3\times2$, $3\times1\to1\times3$을 먼저 표시해요.

#### 한 단계씩 계산해요

#### (a)

(a) $\mathbf{A}$는 $2\times 3$이라 $\mathbf{A}^\top$는 $3\times 2$예요. 첫 행 $(1,-2,3)$이 첫 열, 둘째 행 $(0,4,5)$가 둘째 열이 돼요.

$$
\mathbf{A}^\top=\begin{bmatrix}1 & 0\\-2 & 4\\3 & 5\end{bmatrix}
$$

#### (b)

(b) $\mathbf{b}$는 $3\times 1$ 열벡터라 $\mathbf{b}^\top$는 $1\times 3$ 행벡터예요.

$$
\mathbf{b}^\top=\begin{bmatrix}2 & -1 & 4\end{bmatrix}
$$

#### (c)

(c) $\mathbf{C}$의 각 행을 열로 세워요. 첫 행 $(1,2,0)$, 둘째 행 $(-1,3,4)$, 셋째 행 $(5,0,-2)$가 차례로 열이 돼요.

$$
\mathbf{C}^\top=\begin{bmatrix}1 & -1 & 5\\2 & 3 & 0\\0 & 4 & -2\end{bmatrix}
$$

**완성 답**<br>정답: ${\mathbf{A}^\top=\begin{bmatrix}1 & 0\\-2 & 4\\3 & 5\end{bmatrix}}$, ${\mathbf{b}^\top=\begin{bmatrix}2 & -1 & 4\end{bmatrix}}$, ${\mathbf{C}^\top=\begin{bmatrix}1 & -1 & 5\\2 & 3 & 0\\0 & 4 & -2\end{bmatrix}}$

#### 다른 길로 검산해요

#### (a) 검산

답의 첫 열 $(1,-2,3)^\top$을 다시 첫 행으로 옮기면 원래 A가 나와요. $(A^\top)^\top=A$이며 모든 여섯 원소가 복원돼요.

#### (b) 검산

$b^\top=(2,-1,4)$에 다시 전치를 하면 원래 $3\times1$ 벡터가 돼요. 원소 수는 3개 그대로예요.

#### (c) 검산

$(C^\top)_{12}=-1=C_{21}$, $(C^\top)_{31}=0=C_{13}$이에요. 전체를 다시 전치해 원래 C의 아홉 원소를 확인해요.

#### 이 부분을 조심해요

전치는 원소를 정렬하거나 부호를 바꾸는 연산이 아니에요. 열벡터의 전치는 행벡터예요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$(A^\top)_{ij}=A_{ji}$부터 써요. 전치(transpose)의 정의가 이 식이라, 원래 첫 행을 결과의 첫 열로 세우면 돼요. $2\times3\to3\times2$, $3\times1\to1\times3$을 먼저 표시해요.

#### 핵심 주의점

전치는 원소를 정렬하거나 부호를 바꾸는 연산이 아니에요. 열벡터의 전치는 행벡터예요.

#### 답

정답: ${\mathbf{A}^\top=\begin{bmatrix}1 & 0\\-2 & 4\\3 & 5\end{bmatrix}}$, ${\mathbf{b}^\top=\begin{bmatrix}2 & -1 & 4\end{bmatrix}}$, ${\mathbf{C}^\top=\begin{bmatrix}1 & -1 & 5\\2 & 3 & 0\\0 & 4 & -2\end{bmatrix}}$

---

<a id="p2"></a>

### P2. 내적과 노름

HW1 Problem 2 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p2)

#### 주어진 조건

모든 벡터는 열벡터예요. $\mathbf{x}=(1,-2,2)^\top$, $\mathbf{y}=(2,1,0)^\top$이에요.

#### 구할 것

다음을 구해 보세요.

- (a) $\mathbf{x}^\top\mathbf{y}$
- (b) $\|\mathbf{x}\|_2$
- (c) $\|\mathbf{y}\|_2$
- (d) $\mathbf{x}$와 $\mathbf{y}$는 직교하나요? (a)를 이용해 설명해요.

#### 과제 원문

"Let $\mathbf{x}=(1,-2,2)^\top$ and $\mathbf{y}=(2,1,0)^\top$.

(a) Compute $\mathbf{x}^\top\mathbf{y}$.

(b) Compute $\|\mathbf{x}\|_2$.

(c) Compute $\|\mathbf{y}\|_2$.

(d) Are $\mathbf{x}$ and $\mathbf{y}$ orthogonal? Explain using part (a)."

#### 무엇을 구하는 문제인가요?

내적은 두 벡터를 같은 자리끼리 곱해 더한 하나의 수이고, 노름은 벡터의 길이예요. 마지막에는 내적으로 직교 여부를 판단해요.

#### 종이에 쓸 첫 줄

$x^\top y=\sum_{i=1}^3x_i y_i$, $\|x\|_2=\sqrt{x^\top x}$부터 써요. 내적(dot product)은 $1\times3$과 $3\times1$의 곱이라 스칼라가 돼요.

#### 한 단계씩 계산해요

#### (a)

(a) 같은 자리끼리 곱해서 더해요.

$$
\mathbf{x}^\top\mathbf{y}=1\cdot 2+(-2)\cdot 1+2\cdot 0=2-2+0=0
$$

#### (b)

(b) $\|\mathbf{x}\|_2=\sqrt{1^2+(-2)^2+2^2}=\sqrt{9}=3$이에요.

#### (c)

(c) $\|\mathbf{y}\|_2=\sqrt{2^2+1^2+0^2}=\sqrt{5}$예요.

#### (d)

(d) 두 벡터는 내적이 $0$일 때 직교해요. (a)에서 $\mathbf{x}^\top\mathbf{y}=0$이고 두 벡터 모두 영벡터가 아니니, $\mathbf{x}$와 $\mathbf{y}$는 직교해요.

**완성 답**<br>정답: $\mathbf{x}^\top\mathbf{y}=0$, $\|\mathbf{x}\|_2=3$, $\|\mathbf{y}\|_2=\sqrt{5}$, 내적이 0이라 두 벡터는 직교해요.

#### 다른 길로 검산해요

#### (a) 검산

독립적으로 $x^\top y=2-2+0=0$이에요. 또 $\|x+y\|^2=\|(3,-1,2)\|^2=14=9+5$라 교차항이 0인 것도 확인돼요.

#### (b) 검산

$x^\top x=1+4+4=9$이고 양의 제곱근은 3이에요. $3^2=9$로 되돌려 확인해요.

#### (c) 검산

$y^\top y=4+1=5$이므로 길이는 $\sqrt5$예요. 노름은 음수가 될 수 없어요.

#### (d) 검산

두 벡터가 0이 아니므로 $\cos\alpha=(x^\top y)/(\|x\|\|y\|)=0$이에요. 따라서 각도는 $90^\circ$이고 직교해요.

#### 이 부분을 조심해요

$(-2)^2=4$예요. 길이의 제곱과 길이를 구별하고 마지막 제곱근을 잊지 않아요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$x^\top y=\sum_{i=1}^3x_i y_i$, $\|x\|_2=\sqrt{x^\top x}$부터 써요. 내적(dot product)은 $1\times3$과 $3\times1$의 곱이라 스칼라가 돼요.

#### 핵심 주의점

$(-2)^2=4$예요. 길이의 제곱과 길이를 구별하고 마지막 제곱근을 잊지 않아요.

#### 답

정답: $\mathbf{x}^\top\mathbf{y}=0$, $\|\mathbf{x}\|_2=3$, $\|\mathbf{y}\|_2=\sqrt{5}$, 내적이 0이라 두 벡터는 직교해요.

---

<a id="p3"></a>

### P3. 행렬 곱의 순서

HW1 Problem 3 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p3)

#### 주어진 조건

다음 두 행렬이 주어져요.

$$
{\mathbf{A}=\begin{bmatrix}1 & 2 & 3\\4 & 5 & 6\\7 & 8 & 9\end{bmatrix}},\quad{\mathbf{B}=\begin{bmatrix}1 & 1 & 0\\0 & 1 & 1\\1 & 0 & 1\end{bmatrix}}
$$

#### 구할 것

$\mathbf{A}\mathbf{B}$와 $\mathbf{B}\mathbf{A}$를 구하고, 두 곱이 같은지 비교해 보세요.

#### 과제 원문

"For the matrices ${\mathbf{A}=\begin{bmatrix}1 & 2 & 3\\4 & 5 & 6\\7 & 8 & 9\end{bmatrix}}$, ${\mathbf{B}=\begin{bmatrix}1 & 1 & 0\\0 & 1 & 1\\1 & 0 & 1\end{bmatrix}}$, compute $\mathbf{A}\mathbf{B}$ and $\mathbf{B}\mathbf{A}$. Are the two products equal?"

#### 무엇을 구하는 문제인가요?

두 곱을 각각 계산해야 해요. 왼쪽 행렬의 행과 오른쪽 행렬의 열을 짝지으면 순서를 왜 보존해야 하는지 보일 거예요.

#### 종이에 쓸 첫 줄

$(AB)_{ij}=\sum_{k=1}^3 A_{ik}B_{kj}$부터 써요. 예를 들어 $(AB)_{12}=1\cdot1+2\cdot1+3\cdot0=3$이에요. BA에서는 B의 행과 A의 열로 짝을 바꿔요.

#### 한 단계씩 계산해요

#### 풀이

$\mathbf{B}$의 열은 $(1,0,1)^\top$, $(1,1,0)^\top$, $(0,1,1)^\top$이에요. 그래서 $\mathbf{A}\mathbf{B}$의 각 행은 $\mathbf{A}$의 행에서 (1열+3열, 1열+2열, 2열+3열)을 더한 값이에요. 첫 행은 $(1+3,\,1+2,\,2+3)=(4,3,5)$예요.

같은 방식으로 둘째 행은 $(4+6,\,4+5,\,5+6)=(10,9,11)$, 셋째 행은 $(7+9,\,7+8,\,8+9)=(16,15,17)$이에요.

$$
\mathbf{A}\mathbf{B}=\begin{bmatrix}4 & 3 & 5\\10 & 9 & 11\\16 & 15 & 17\end{bmatrix}
$$

$\mathbf{B}\mathbf{A}$의 각 행은 $\mathbf{A}$의 행을 더한 거예요. 첫 행은 $\mathbf{A}$의 1행+2행 $=(5,7,9)$, 둘째 행은 2행+3행 $=(11,13,15)$, 셋째 행은 1행+3행 $=(8,10,12)$예요.

$$
\mathbf{B}\mathbf{A}=\begin{bmatrix}5 & 7 & 9\\11 & 13 & 15\\8 & 10 & 12\end{bmatrix}
$$

비교해 보면 $(1,1)$ 원소부터 $4\ne 5$로 달라요. 그래서 $\mathbf{A}\mathbf{B}\neq\mathbf{B}\mathbf{A}$이고, 행렬 곱은 순서를 바꾸면 결과가 달라질 수 있어요.

**완성 답**<br>정답: ${\mathbf{A}\mathbf{B}=\begin{bmatrix}4 & 3 & 5\\10 & 9 & 11\\16 & 15 & 17\end{bmatrix}}$, ${\mathbf{B}\mathbf{A}=\begin{bmatrix}5 & 7 & 9\\11 & 13 & 15\\8 & 10 & 12\end{bmatrix}}$, 따라서 $\mathbf{A}\mathbf{B}\neq\mathbf{B}\mathbf{A}$예요.

#### 다른 길로 검산해요

#### 답을 확인해요

곱을 일반적인 행·열 내적으로 다시 계산하면 $AB=\begin{bmatrix}4&3&5\\10&9&11\\16&15&17\end{bmatrix}$, $BA=\begin{bmatrix}5&7&9\\11&13&15\\8&10&12\end{bmatrix}$예요. $(1,1)$ 원소가 $4\ne5$이므로 두 곱은 달라요.

#### 이 부분을 조심해요

행렬 곱(matrix product)은 같은 자리의 원소끼리 곱하는 연산이 아니에요. 두 행렬 모두 $3\times3$이어도 교환법칙은 보장되지 않아요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$(AB)_{ij}=\sum_{k=1}^3 A_{ik}B_{kj}$부터 써요. 예를 들어 $(AB)_{12}=1\cdot1+2\cdot1+3\cdot0=3$이에요. BA에서는 B의 행과 A의 열로 짝을 바꿔요.

#### 핵심 주의점

행렬 곱(matrix product)은 같은 자리의 원소끼리 곱하는 연산이 아니에요. 두 행렬 모두 $3\times3$이어도 교환법칙은 보장되지 않아요.

#### 답

정답: ${\mathbf{A}\mathbf{B}=\begin{bmatrix}4 & 3 & 5\\10 & 9 & 11\\16 & 15 & 17\end{bmatrix}}$, ${\mathbf{B}\mathbf{A}=\begin{bmatrix}5 & 7 & 9\\11 & 13 & 15\\8 & 10 & 12\end{bmatrix}}$, 따라서 $\mathbf{A}\mathbf{B}\neq\mathbf{B}\mathbf{A}$예요.

---

<a id="p4"></a>

### P4. 행렬식 계산

HW1 Problem 4 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p4)

#### 주어진 조건

다음 네 행렬이 주어져요.

$$
{\mathbf{A}=\begin{bmatrix}3 & 1\\2 & 4\end{bmatrix}},\quad{\mathbf{B}=\begin{bmatrix}1 & -2\\3 & 0\end{bmatrix}}
$$

$$
{\mathbf{C}=\begin{bmatrix}2 & 0 & 0\\0 & -1 & 0\\0 & 0 & 3\end{bmatrix}},\quad{\mathbf{D}=\begin{bmatrix}1 & 3 & 5\\2 & 4 & 6\\0 & 2 & 4\end{bmatrix}}
$$

#### 구할 것

각 행렬의 행렬식을 구해 보세요. (d)는 첫 행 전개와 Sarrus 규칙 두 방법으로 모두 구해요.

- (a) $\det(\mathbf{A})$
- (b) $\det(\mathbf{B})$
- (c) $\det(\mathbf{C})$
- (d) $\det(\mathbf{D})$

#### 과제 원문

"Compute the determinant of each matrix. For part (d), use both expansion along the first row and the Sarrus rule.

(a) ${\mathbf{A}=\begin{bmatrix}3 & 1\\2 & 4\end{bmatrix}}$.

(b) ${\mathbf{B}=\begin{bmatrix}1 & -2\\3 & 0\end{bmatrix}}$.

(c) ${\mathbf{C}=\begin{bmatrix}2 & 0 & 0\\0 & -1 & 0\\0 & 0 & 3\end{bmatrix}}$.

(d) ${\mathbf{D}=\begin{bmatrix}1 & 3 & 5\\2 & 4 & 6\\0 & 2 & 4\end{bmatrix}}$."

#### 무엇을 구하는 문제인가요?

행렬식(determinant)은 행렬마다 하나의 수예요. 2×2, 대각행렬, 일반 3×3의 모양을 보고 계산법을 고르며 (d)는 두 방법 모두 써요.

#### 종이에 쓸 첫 줄

$\det\begin{bmatrix}a&b\\c&d\end{bmatrix}=ad-bc$부터 써요. (c)는 대각 원소를 곱해요. (d)의 첫 행 전개 부호는 $+,-,+$이고, 각 원소의 행·열을 지운 2×2 소행렬식을 곱해요.

#### 한 단계씩 계산해요

#### (a)

(a) $\det(\mathbf{A})=3\cdot 4-1\cdot 2=10$이에요.

#### (b)

(b) $\det(\mathbf{B})=1\cdot 0-(-2)\cdot 3=6$이에요.

#### (c)

(c) 대각행렬이라 $\det(\mathbf{C})=2\cdot(-1)\cdot 3=-6$이에요.

#### (d)

(d) 첫 행으로 전개해요.

$$
\det(\mathbf{D})=1(4\cdot 4-6\cdot 2)-3(2\cdot 4-6\cdot 0)+5(2\cdot 2-4\cdot 0)=4-24+20=0
$$

(d) Sarrus 규칙으로도 확인해요.

$$
(1\cdot 4\cdot 4+3\cdot 6\cdot 0+5\cdot 2\cdot 2)-(5\cdot 4\cdot 0+1\cdot 6\cdot 2+3\cdot 2\cdot 4)=36-36=0
$$

**완성 답**<br>정답: $\det(\mathbf{A})=10$, $\det(\mathbf{B})=6$, $\det(\mathbf{C})=-6$, $\det(\mathbf{D})=0$

#### 다른 길로 검산해요

#### (a) 검산

행을 소거하면 $R_2\leftarrow R_2-\frac23R_1$ 뒤 대각은 $3,10/3$이에요. 행 더하기는 행렬식을 보존하므로 곱은 10이에요.

#### (b) 검산

$R_2\leftarrow R_2-3R_1$ 뒤 대각은 $1,6$이에요. 곱 6은 공식 결과와 같아요.

#### (c) 검산

대각 원소 $2,-1,3$의 곱은 -6이에요. 음수 대각이 하나라 부호도 음수예요.

#### (d) 검산

열을 보면 $D_{:3}=2D_{:2}-D_{:1}$이에요. 열들이 종속이므로 행렬식은 0이에요. 첫 행 전개와 Sarrus의 $36-36=0$을 별도 성질로 확인했어요.

#### 이 부분을 조심해요

행렬식은 원소의 합이 아니에요. Sarrus 규칙은 3×3에만 그대로 적용하며, 첫 행 전개의 가운데 부호는 마이너스예요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$\det\begin{bmatrix}a&b\\c&d\end{bmatrix}=ad-bc$부터 써요. (c)는 대각 원소를 곱해요. (d)의 첫 행 전개 부호는 $+,-,+$이고, 각 원소의 행·열을 지운 2×2 소행렬식을 곱해요.

#### 핵심 주의점

행렬식은 원소의 합이 아니에요. Sarrus 규칙은 3×3에만 그대로 적용하며, 첫 행 전개의 가운데 부호는 마이너스예요.

#### 답

정답: $\det(\mathbf{A})=10$, $\det(\mathbf{B})=6$, $\det(\mathbf{C})=-6$, $\det(\mathbf{D})=0$

---

<a id="p5"></a>

### P5. 역행렬 구하기

HW1 Problem 5 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p5)

#### 주어진 조건

다음 세 행렬이 주어져요.

$$
{\mathbf{A}=\begin{bmatrix}2 & 1\\1 & 1\end{bmatrix}},\quad{\mathbf{B}=\begin{bmatrix}1 & -2\\3 & 1\end{bmatrix}},\quad{\mathbf{C}=\begin{bmatrix}2 & 1 & 0\\1 & 2 & 0\\0 & 0 & 2\end{bmatrix}}
$$

#### 구할 것

각 행렬의 역행렬을 구해 보세요. 주요 계산 과정을 함께 써요.

- (a) $\mathbf{A}^{-1}$
- (b) $\mathbf{B}^{-1}$
- (c) $\mathbf{C}^{-1}$

#### 과제 원문

"Find the inverse of each matrix. Show the main calculation steps.

(a) ${\mathbf{A}=\begin{bmatrix}2 & 1\\1 & 1\end{bmatrix}}$.

(b) ${\mathbf{B}=\begin{bmatrix}1 & -2\\3 & 1\end{bmatrix}}$.

(c) ${\mathbf{C}=\begin{bmatrix}2 & 1 & 0\\1 & 2 & 0\\0 & 0 & 2\end{bmatrix}}$."

#### 무엇을 구하는 문제인가요?

역행렬(inverse)은 곱했을 때 단위행렬이 되는 행렬이에요. 먼저 존재 여부를 보고, 후보를 만든 뒤 곱해서 확인해요.

#### 종이에 쓸 첫 줄

$M^{-1}=\frac1{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}$, $ad-bc\ne0$부터 써요. 2×2에서 주대각을 맞바꾸고 비대각의 부호를 바꾸는 공식이에요. (c)는 두 좌표와 마지막 좌표가 섞이지 않는 블록대각 구조를 이용해요.

#### 한 단계씩 계산해요

#### (a)

(a) $\det(\mathbf{A})=2\cdot 1-1\cdot 1=1$이에요. 공식에 넣으면

$$
\mathbf{A}^{-1}=\frac{1}{1}\begin{bmatrix}1 & -1\\-1 & 2\end{bmatrix}=\begin{bmatrix}1 & -1\\-1 & 2\end{bmatrix}
$$

(a) 확인: $\mathbf{A}\mathbf{A}^{-1}=\begin{bmatrix}2-1 & -2+2\\1-1 & -1+2\end{bmatrix}=\mathbf{I}$예요.

#### (b)

(b) $\det(\mathbf{B})=1\cdot 1-(-2)\cdot 3=7$이에요.

$$
\mathbf{B}^{-1}=\frac{1}{7}\begin{bmatrix}1 & 2\\-3 & 1\end{bmatrix}=\begin{bmatrix}\frac{1}{7} & \frac{2}{7}\\-\frac{3}{7} & \frac{1}{7}\end{bmatrix}
$$

(b) 확인: $\mathbf{B}\begin{bmatrix}1 & 2\\-3 & 1\end{bmatrix}=\begin{bmatrix}1+6 & 2-2\\3-3 & 6+1\end{bmatrix}=7\mathbf{I}$라서 $\frac{1}{7}$을 곱하면 $\mathbf{I}$예요.

#### (c)

(c) $\mathbf{C}$는 블록대각 행렬이에요. 왼쪽 위 블록 $\begin{bmatrix}2 & 1\\1 & 2\end{bmatrix}$의 행렬식은 $4-1=3$이라 역은 $\frac{1}{3}\begin{bmatrix}2 & -1\\-1 & 2\end{bmatrix}$이고, 오른쪽 아래 $2$의 역은 $\frac{1}{2}$이에요.

$$
\mathbf{C}^{-1}=\begin{bmatrix}\frac{2}{3} & -\frac{1}{3} & 0\\-\frac{1}{3} & \frac{2}{3} & 0\\0 & 0 & \frac{1}{2}\end{bmatrix}
$$

(c) 확인: 첫 행은 $(2\cdot\frac{2}{3}-\frac{1}{3},\;-\frac{2}{3}+\frac{2}{3},\;0)=(1,0,0)$, 둘째 행은 $(\frac{2}{3}-\frac{2}{3},\;-\frac{1}{3}+\frac{4}{3},\;0)=(0,1,0)$, 셋째 행은 $(0,0,2\cdot\frac{1}{2})=(0,0,1)$이라 $\mathbf{C}\mathbf{C}^{-1}=\mathbf{I}$예요.

**완성 답**<br>정답: ${\mathbf{A}^{-1}=\begin{bmatrix}1 & -1\\-1 & 2\end{bmatrix}}$, ${\mathbf{B}^{-1}=\begin{bmatrix}\frac{1}{7} & \frac{2}{7}\\-\frac{3}{7} & \frac{1}{7}\end{bmatrix}}$, ${\mathbf{C}^{-1}=\begin{bmatrix}\frac{2}{3} & -\frac{1}{3} & 0\\-\frac{1}{3} & \frac{2}{3} & 0\\0 & 0 & \frac{1}{2}\end{bmatrix}}$

#### 다른 길로 검산해요

#### (a) 검산

$\begin{bmatrix}1&-1\\-1&2\end{bmatrix}A=\begin{bmatrix}1&0\\0&1\end{bmatrix}$이에요. 풀이의 AX뿐 아니라 XA도 정확히 단위행렬이에요.

#### (b) 검산

$\begin{bmatrix}1&2\\-3&1\end{bmatrix}B=\begin{bmatrix}7&0\\0&7\end{bmatrix}$이에요. 따라서 $1/7$을 곱한 후보는 양쪽 곱 모두 단위행렬이에요.

#### (c) 검산

첫 블록은 $\frac13\begin{bmatrix}2&-1\\-1&2\end{bmatrix}\begin{bmatrix}2&1\\1&2\end{bmatrix}=I_2$이고 마지막 원소는 $(1/2)2=1$이에요. 블록 사이의 0도 그대로라 전체 양쪽 곱은 $I_3$예요.

#### 이 부분을 조심해요

모든 원소를 역수로 바꾸면 역행렬이 되지 않아요. 분모의 행렬식과 음수 부호를 빠뜨리지 않아요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$M^{-1}=\frac1{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}$, $ad-bc\ne0$부터 써요. 2×2에서 주대각을 맞바꾸고 비대각의 부호를 바꾸는 공식이에요. (c)는 두 좌표와 마지막 좌표가 섞이지 않는 블록대각 구조를 이용해요.

#### 핵심 주의점

모든 원소를 역수로 바꾸면 역행렬이 되지 않아요. 분모의 행렬식과 음수 부호를 빠뜨리지 않아요.

#### 답

정답: ${\mathbf{A}^{-1}=\begin{bmatrix}1 & -1\\-1 & 2\end{bmatrix}}$, ${\mathbf{B}^{-1}=\begin{bmatrix}\frac{1}{7} & \frac{2}{7}\\-\frac{3}{7} & \frac{1}{7}\end{bmatrix}}$, ${\mathbf{C}^{-1}=\begin{bmatrix}\frac{2}{3} & -\frac{1}{3} & 0\\-\frac{1}{3} & \frac{2}{3} & 0\\0 & 0 & \frac{1}{2}\end{bmatrix}}$

---

<a id="p6"></a>

### P6. 선형 독립 판정

HW1 Problem 6 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p6)

#### 주어진 조건

모든 벡터는 열벡터예요. 다음 세 벡터가 주어져요.

$$
{\mathbf{x}_1=\begin{bmatrix}2\\-1\\3\end{bmatrix}},\quad{\mathbf{x}_2=\begin{bmatrix}1\\1\\-2\end{bmatrix}},\quad{\mathbf{x}_3=\begin{bmatrix}3\\-3\\8\end{bmatrix}}
$$

#### 구할 것

세 벡터가 선형 독립인지 판정해 보세요. 비자명한 선형 관계를 찾거나, 그런 관계가 없음을 보여서 근거를 대요.

#### 과제 원문

"Determine whether the following vectors are linearly independent. Justify your answer by finding a nontrivial linear relation or showing that no such relation exists: ${\mathbf{x}_1=\begin{bmatrix}2\\-1\\3\end{bmatrix}}$, ${\mathbf{x}_2=\begin{bmatrix}1\\1\\-2\end{bmatrix}}$, ${\mathbf{x}_3=\begin{bmatrix}3\\-3\\8\end{bmatrix}}$."

#### 무엇을 구하는 문제인가요?

벡터 개수가 3이라는 이유만으로 독립이라고 할 수 없어요. 0을 만들 수 있는 계수 중 모두 0이 아닌 조합이 있는지 찾아요.

#### 종이에 쓸 첫 줄

$c_1x_1+c_2x_2+c_3x_3=0$부터 써요. 선형 독립(linear independence)의 정의를 그대로 방정식으로 바꾼 거예요. 각 좌표가 0이어야 하므로 세 식을 얻어요.

#### 한 단계씩 계산해요

#### 풀이

$c_1\mathbf{x}_1+c_2\mathbf{x}_2+c_3\mathbf{x}_3=\mathbf{0}$을 성분별로 쓰면 다음과 같아요.

$$
{2c_1+c_2+3c_3=0},\quad{-c_1+c_2-3c_3=0},\quad{3c_1-2c_2+8c_3=0}
$$

첫 식에서 둘째 식을 빼면 $3c_1+6c_3=0$, 즉 $c_1=-2c_3$예요. 둘째 식에 넣으면 $c_2=c_1+3c_3=c_3$예요.

셋째 식에 넣어 보면 $3(-2c_3)-2c_3+8c_3=0$으로 항상 성립해요. 그래서 $c_3$는 자유롭게 고를 수 있어요.

$c_3=1$로 두면 $(c_1,c_2,c_3)=(-2,1,1)$이라는 비자명한 해가 나와요. 즉 $-2\mathbf{x}_1+\mathbf{x}_2+\mathbf{x}_3=\mathbf{0}$이에요.

검산: $2\mathbf{x}_1-\mathbf{x}_2=(4-1,\,-2-1,\,6+2)^\top=(3,-3,8)^\top=\mathbf{x}_3$이 맞아요. 비자명한 선형 관계가 있으니 세 벡터는 선형 종속이에요.

**완성 답**<br>정답: $\mathbf{x}_3=2\mathbf{x}_1-\mathbf{x}_2$ (즉 ${-2\mathbf{x}_1+\mathbf{x}_2+\mathbf{x}_3=\mathbf{0}}$)라서 세 벡터는 선형 종속이에요.

#### 다른 길로 검산해요

#### 답을 확인해요

$-2(2,-1,3)+(1,1,-2)+(3,-3,8)=(0,0,0)$이에요. 계수 $(-2,1,1)$이 비자명하므로 종속이라는 결론이 정의에 직접 부합해요.

#### 이 부분을 조심해요

$(0,0,0)$ 계수는 어떤 벡터에도 가능해서 종속의 근거가 아니에요. 적어도 하나가 0이 아닌 계수를 보여야 해요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$c_1x_1+c_2x_2+c_3x_3=0$부터 써요. 선형 독립(linear independence)의 정의를 그대로 방정식으로 바꾼 거예요. 각 좌표가 0이어야 하므로 세 식을 얻어요.

#### 핵심 주의점

$(0,0,0)$ 계수는 어떤 벡터에도 가능해서 종속의 근거가 아니에요. 적어도 하나가 0이 아닌 계수를 보여야 해요.

#### 답

정답: $\mathbf{x}_3=2\mathbf{x}_1-\mathbf{x}_2$ (즉 ${-2\mathbf{x}_1+\mathbf{x}_2+\mathbf{x}_3=\mathbf{0}}$)라서 세 벡터는 선형 종속이에요.

---

<a id="p7"></a>

### P7. 선형결합으로 나타내기

HW1 Problem 7 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p7)

#### 주어진 조건

모든 벡터는 열벡터예요. 다음 벡터들이 주어져요.

$$
{\mathbf{y}=\begin{bmatrix}1\\-2\\5\end{bmatrix}},\quad{\mathbf{x}_1=\begin{bmatrix}1\\1\\1\end{bmatrix}},\quad{\mathbf{x}_2=\begin{bmatrix}1\\2\\3\end{bmatrix}},\quad{\mathbf{x}_3=\begin{bmatrix}2\\-1\\1\end{bmatrix}}
$$

#### 구할 것

$\mathbf{y}$를 $\mathbf{x}_1,\mathbf{x}_2,\mathbf{x}_3$의 선형결합으로 나타내 보세요.

#### 과제 원문

"Write $\mathbf{y}$ as a linear combination of $\mathbf{x}_1,\mathbf{x}_2,\mathbf{x}_3$: ${\mathbf{y}=\begin{bmatrix}1\\-2\\5\end{bmatrix}}$, ${\mathbf{x}_1=\begin{bmatrix}1\\1\\1\end{bmatrix}}$, ${\mathbf{x}_2=\begin{bmatrix}1\\2\\3\end{bmatrix}}$, ${\mathbf{x}_3=\begin{bmatrix}2\\-1\\1\end{bmatrix}}$."

#### 무엇을 구하는 문제인가요?

구할 것은 새로운 벡터가 아니라, 세 주어진 벡터를 얼마나씩 섞을지 정하는 세 계수예요.

#### 종이에 쓸 첫 줄

$y=ax_1+bx_2+cx_3$부터 써요. 선형결합(linear combination)의 미지수는 $a,b,c$예요. 같은 좌표끼리 맞추면 세 연립방정식이 돼요.

#### 한 단계씩 계산해요

#### 풀이

$\mathbf{y}=a\mathbf{x}_1+b\mathbf{x}_2+c\mathbf{x}_3$를 성분별로 쓰면 다음과 같아요.

$$
{a+b+2c=1},\quad{a+2b-c=-2},\quad{a+3b+c=5}
$$

둘째 식에서 첫 식을 빼면 $b-3c=-3$, 셋째 식에서 둘째 식을 빼면 $b+2c=7$이에요.

두 식을 빼면 $5c=10$이라 $c=2$, 그러면 $b=7-4=3$, $a=1-b-2c=1-3-4=-6$이에요.

검산: $-6(1,1,1)^\top+3(1,2,3)^\top+2(2,-1,1)^\top=(-6+3+4,\,-6+6-2,\,-6+9+2)^\top=(1,-2,5)^\top=\mathbf{y}$예요.

**완성 답**<br>정답: ${\mathbf{y}=-6\mathbf{x}_1+3\mathbf{x}_2+2\mathbf{x}_3}$

#### 다른 길로 검산해요

#### 답을 확인해요

답 $(-6,3,2)$를 대입하면 첫 좌표 $-6+3+4=1$, 둘째 $-6+6-2=-2$, 셋째 $-6+9+2=5$예요. 열로 세운 계수행렬의 행렬식은 5로 0이 아니어서 계수도 유일해요.

#### 이 부분을 조심해요

계수는 음수도 가능해요. 한 좌표만 맞추고 끝내지 말고 세 좌표를 모두 확인해요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$y=ax_1+bx_2+cx_3$부터 써요. 선형결합(linear combination)의 미지수는 $a,b,c$예요. 같은 좌표끼리 맞추면 세 연립방정식이 돼요.

#### 핵심 주의점

계수는 음수도 가능해요. 한 좌표만 맞추고 끝내지 말고 세 좌표를 모두 확인해요.

#### 답

정답: ${\mathbf{y}=-6\mathbf{x}_1+3\mathbf{x}_2+2\mathbf{x}_3}$

---

<a id="p8"></a>

### P8. $\mathbf{A}^\top\mathbf{A}$와 역행렬

HW1 Problem 8 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p8)

#### 주어진 조건

다음 행렬이 주어져요.

$$
\mathbf{A}=\begin{bmatrix}1 & -1\\1 & 0\\1 & 1\end{bmatrix}
$$

#### 구할 것

$\mathbf{A}^\top\mathbf{A}$와 그 행렬식을 구해 보세요. $(\mathbf{A}^\top\mathbf{A})^{-1}$이 존재하는지 판단하고, 존재하면 계산한 뒤 곱셈으로 검증해요.

#### 과제 원문

"Let ${\mathbf{A}=\begin{bmatrix}1 & -1\\1 & 0\\1 & 1\end{bmatrix}}$. Compute $\mathbf{A}^\top\mathbf{A}$ and its determinant. Determine whether $(\mathbf{A}^\top\mathbf{A})^{-1}$ exists and, if it does, calculate it. Verify your inverse by multiplication."

#### 무엇을 구하는 문제인가요?

직사각형 A 자체의 역을 묻는 것이 아니라, 두 열 사이의 내적을 모은 2×2 행렬의 역을 물어요.

#### 종이에 쓸 첫 줄

$A^\top A=\begin{bmatrix}a_1^\top a_1&a_1^\top a_2\\a_2^\top a_1&a_2^\top a_2\end{bmatrix}$부터 써요. $A:3\times2$, $A^\top:2\times3$이므로 결과는 $2\times2$예요.

#### 한 단계씩 계산해요

#### 풀이

$\mathbf{A}$의 열은 $\mathbf{a}_1=(1,1,1)^\top$, $\mathbf{a}_2=(-1,0,1)^\top$이에요. $\mathbf{a}_1^\top\mathbf{a}_1=3$, $\mathbf{a}_1^\top\mathbf{a}_2=-1+0+1=0$, $\mathbf{a}_2^\top\mathbf{a}_2=1+0+1=2$예요.

$$
\mathbf{A}^\top\mathbf{A}=\begin{bmatrix}3 & 0\\0 & 2\end{bmatrix}
$$

행렬식은 $\det(\mathbf{A}^\top\mathbf{A})=3\cdot 2-0\cdot 0=6$이에요. $6\ne 0$이라 역행렬이 존재해요.

대각행렬의 역은 대각 원소의 역수예요.

$$
(\mathbf{A}^\top\mathbf{A})^{-1}=\begin{bmatrix}\frac{1}{3} & 0\\0 & \frac{1}{2}\end{bmatrix}
$$

검증: $\begin{bmatrix}3 & 0\\0 & 2\end{bmatrix}\begin{bmatrix}\frac{1}{3} & 0\\0 & \frac{1}{2}\end{bmatrix}=\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}=\mathbf{I}_2$예요.

**완성 답**<br>정답: ${\mathbf{A}^\top\mathbf{A}=\begin{bmatrix}3 & 0\\0 & 2\end{bmatrix}}$, $\det(\mathbf{A}^\top\mathbf{A})=6$이라 역행렬이 존재하고, ${(\mathbf{A}^\top\mathbf{A})^{-1}=\begin{bmatrix}\frac{1}{3} & 0\\0 & \frac{1}{2}\end{bmatrix}}$

#### 다른 길로 검산해요

#### 답을 확인해요

$G=\operatorname{diag}(3,2)$, $\det G=6$, $G^{-1}=\operatorname{diag}(1/3,1/2)$예요. $GG^{-1}=G^{-1}G=I_2$이고, $v^\top Gv=3v_1^2+2v_2^2>0$은 영벡터 외에 성립해 역의 존재와도 맞아요.

#### 이 부분을 조심해요

$A^\top A$와 $AA^\top$는 크기부터 달라요. 대각의 역수 법칙은 비대각이 0인 대각행렬에 사용해요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$A^\top A=\begin{bmatrix}a_1^\top a_1&a_1^\top a_2\\a_2^\top a_1&a_2^\top a_2\end{bmatrix}$부터 써요. $A:3\times2$, $A^\top:2\times3$이므로 결과는 $2\times2$예요.

#### 핵심 주의점

$A^\top A$와 $AA^\top$는 크기부터 달라요. 대각의 역수 법칙은 비대각이 0인 대각행렬에 사용해요.

#### 답

정답: ${\mathbf{A}^\top\mathbf{A}=\begin{bmatrix}3 & 0\\0 & 2\end{bmatrix}}$, $\det(\mathbf{A}^\top\mathbf{A})=6$이라 역행렬이 존재하고, ${(\mathbf{A}^\top\mathbf{A})^{-1}=\begin{bmatrix}\frac{1}{3} & 0\\0 & \frac{1}{2}\end{bmatrix}}$

---

<a id="p9"></a>

### P9. 특징 행렬과 예측

HW1 Problem 9 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p9)

#### 주어진 조건

모든 벡터는 열벡터예요. 특징 사상은 $\phi(x)=(1,x,x^2)^\top$이고, 입력은 $x_1=-1$, $x_2=0$, $x_3=1$이에요. 파라미터는 $\boldsymbol{\theta}=(1,1,2)^\top$예요.

#### 구할 것

$n$번째 행이 $\phi(x_n)^\top$인 특징 행렬 $\boldsymbol{\Phi}$를 만들고 ${\hat{\mathbf{y}}=\boldsymbol{\Phi}\boldsymbol{\theta}}$를 구해 보세요. 또 $x^2$이 들어 있는데도 이것이 선형회귀 모델인 이유를 설명해요.

#### 과제 원문

"Consider the feature map $\phi(x)=(1,x,x^2)^\top$ and the three inputs $x_1=-1$, $x_2=0$, $x_3=1$. Construct the feature matrix $\boldsymbol{\Phi}$, with row $n$ equal to $\phi(x_n)^\top$, and calculate ${\hat{\mathbf{y}}=\boldsymbol{\Phi}\boldsymbol{\theta}}$ for $\boldsymbol{\theta}=(1,1,2)^\top$. Explain why this is a linear regression model even though it contains $x^2$."

#### 무엇을 구하는 문제인가요?

각 입력을 세 특징으로 바꾸고, 한 관측을 한 행에 담아요. 그 뒤 세 계수와 내적하면 예측값이 나와요.

#### 종이에 쓸 첫 줄

$\Phi_{n:}=\phi(x_n)^\top=(1,x_n,x_n^2)$부터 써요. 특징행렬(feature matrix)은 관측 수×특징 수이며, 열벡터 특징을 전치해서 행으로 넣어요.

#### 한 단계씩 계산해요

#### 풀이

각 입력의 특징 벡터는 $\phi(-1)=(1,-1,1)^\top$, $\phi(0)=(1,0,0)^\top$, $\phi(1)=(1,1,1)^\top$이에요. 이걸 행으로 쌓아요.

$$
\boldsymbol{\Phi}=\begin{bmatrix}1 & -1 & 1\\1 & 0 & 0\\1 & 1 & 1\end{bmatrix}
$$

행마다 $\boldsymbol{\theta}$와 내적해요. $1-1+2=2$, $1+0+0=1$, $1+1+2=4$예요.

$$
\hat{\mathbf{y}}=\boldsymbol{\Phi}\boldsymbol{\theta}=\begin{bmatrix}2\\1\\4\end{bmatrix}
$$

모델은 $f(x)=\theta_0+\theta_1x+\theta_2x^2=\phi(x)^\top\boldsymbol{\theta}$예요. $x$에 대해서는 이차식이지만, 파라미터 $\boldsymbol{\theta}$에 대해서는 일차 결합이에요. 선형회귀의 "선형"은 파라미터에 대한 선형성이라서, 특징 $\phi(x)$를 고정하면 이 모델은 선형회귀예요.

**완성 답**<br>정답: ${\boldsymbol{\Phi}=\begin{bmatrix}1 & -1 & 1\\1 & 0 & 0\\1 & 1 & 1\end{bmatrix}}$, ${\hat{\mathbf{y}}=\begin{bmatrix}2\\1\\4\end{bmatrix}}$. 모델이 $\boldsymbol{\theta}$에 대해 선형이라 선형회귀예요.

#### 다른 길로 검산해요

#### 답을 확인해요

직접 다항식 $f(x)=1+x+2x^2$에 $-1,0,1$을 넣으면 $(2,1,4)^\top$이에요. 행렬곱 예측과 같아요. 고정된 x에 대해 $f_{a\theta+b\eta}(x)=af_\theta(x)+bf_\eta(x)$이므로 파라미터에 선형이에요.

#### 이 부분을 조심해요

선형회귀의 선형성은 파라미터에 대한 것이에요. $x^2$가 있다는 이유만으로 선형회귀가 아니라고 판단하지 않아요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$\Phi_{n:}=\phi(x_n)^\top=(1,x_n,x_n^2)$부터 써요. 특징행렬(feature matrix)은 관측 수×특징 수이며, 열벡터 특징을 전치해서 행으로 넣어요.

#### 핵심 주의점

선형회귀의 선형성은 파라미터에 대한 것이에요. $x^2$가 있다는 이유만으로 선형회귀가 아니라고 판단하지 않아요.

#### 답

정답: ${\boldsymbol{\Phi}=\begin{bmatrix}1 & -1 & 1\\1 & 0 & 0\\1 & 1 & 1\end{bmatrix}}$, ${\hat{\mathbf{y}}=\begin{bmatrix}2\\1\\4\end{bmatrix}}$. 모델이 $\boldsymbol{\theta}$에 대해 선형이라 선형회귀예요.

---

<a id="p10"></a>

### P10. gradient 구하기

HW1 Problem 10 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p10)

#### 주어진 조건

gradient는 열벡터로 써요. 다음 세 함수가 주어져요.

$$
f(u,v)=u^2+3v^2-2u+4v
$$

$$
g(u,v)=u^2+2uv+3v^2-4u+2v
$$

$$
h(u,v,w)=(u+2v-w-3)^2
$$

#### 구할 것

각 함수의 gradient를 열벡터로 구하고, 주어진 점에서 값을 계산해 보세요.

- (a) $\nabla f$, $(u,v)=(1,-1)$
- (b) $\nabla g$, $(u,v)=(1,-1)$
- (c) $\nabla h$, $(u,v,w)=(1,0,-1)$

#### 과제 원문

"For each function, find its gradient as a column vector and evaluate it at the indicated point. Hint: For $f(u,v)$, ${\nabla f=(\partial f/\partial u,\partial f/\partial v)^\top}$. When differentiating with respect to one variable, treat the others as constants.

(a) $f(u,v)=u^2+3v^2-2u+4v$ at $(u,v)=(1,-1)$.

(b) $g(u,v)=u^2+2uv+3v^2-4u+2v$ at $(u,v)=(1,-1)$.

(c) $h(u,v,w)=(u+2v-w-3)^2$ at $(u,v,w)=(1,0,-1)$."

#### 무엇을 구하는 문제인가요?

먼저 함수 전체의 편미분을 구하고, 지정된 점은 마지막에 넣어요. 각 편미분에서는 다른 변수를 상수로 다뤄요.

#### 종이에 쓸 첫 줄

$\nabla f=(f_u,f_v)^\top$부터 써요. 예를 들어 $\partial_u(3v^2)=0$, $\partial_u(2uv)=2v$예요. (c)는 $s=u+2v-w-3$를 두고 $\nabla(s^2)=2s\nabla s$로 시작해요.

#### 한 단계씩 계산해요

#### (a)

(a) $\partial f/\partial u=2u-2$, $\partial f/\partial v=6v+4$예요. $(1,-1)$에서 $2-2=0$, $-6+4=-2$예요.

$$
\nabla f(1,-1)=\begin{bmatrix}0\\-2\end{bmatrix}
$$

#### (b)

(b) $\partial g/\partial u=2u+2v-4$, $\partial g/\partial v=2u+6v+2$예요. $(1,-1)$에서 $2-2-4=-4$, $2-6+2=-2$예요.

$$
\nabla g(1,-1)=\begin{bmatrix}-4\\-2\end{bmatrix}
$$

#### (c)

(c) $s=u+2v-w-3$로 두면 $h=s^2$이고, 연쇄법칙으로 $\nabla h=2s\,(\partial s/\partial u,\partial s/\partial v,\partial s/\partial w)^\top=2s\,(1,2,-1)^\top$예요.

(c) $(1,0,-1)$에서 $s=1+0+1-3=-1$이라

$$
\nabla h(1,0,-1)=2(-1)\begin{bmatrix}1\\2\\-1\end{bmatrix}=\begin{bmatrix}-2\\-4\\2\end{bmatrix}
$$

**완성 답**<br>정답: (a) ${\nabla f(1,-1)=\begin{bmatrix}0\\-2\end{bmatrix}}$, (b) ${\nabla g(1,-1)=\begin{bmatrix}-4\\-2\end{bmatrix}}$, (c) ${\nabla h(1,0,-1)=\begin{bmatrix}-2\\-4\\2\end{bmatrix}}$

#### 다른 길로 검산해요

#### (a) 검산

$f(1+t,-1)-f(1,-1)=t^2$이므로 u방향 일차계수는 0이에요. $f(1,-1+t)-f(1,-1)=-2t+3t^2$라 v방향은 -2예요.

#### (b) 검산

$g(1+t,-1)-g(1,-1)=-4t+t^2$, $g(1,-1+t)-g(1,-1)=-2t+3t^2$예요. 일차계수는 $(-4,-2)^\top$이에요.

#### (c) 검산

기준점에서 $s=-1$이에요. u,v,w만 각각 t만큼 옮겼을 때 h의 변화는 $-2t+t^2$, $-4t+4t^2$, $2t+t^2$예요. 일차계수는 $(-2,-4,2)^\top$이에요.

#### 이 부분을 조심해요

점의 값을 먼저 넣으면 상수 함수를 미분하게 돼요. (c)의 $w$ 미분은 $\partial_w s=-1$이고, 과제의 gradient는 열벡터예요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$\nabla f=(f_u,f_v)^\top$부터 써요. 예를 들어 $\partial_u(3v^2)=0$, $\partial_u(2uv)=2v$예요. (c)는 $s=u+2v-w-3$를 두고 $\nabla(s^2)=2s\nabla s$로 시작해요.

#### 핵심 주의점

점의 값을 먼저 넣으면 상수 함수를 미분하게 돼요. (c)의 $w$ 미분은 $\partial_w s=-1$이고, 과제의 gradient는 열벡터예요.

#### 답

정답: (a) ${\nabla f(1,-1)=\begin{bmatrix}0\\-2\end{bmatrix}}$, (b) ${\nabla g(1,-1)=\begin{bmatrix}-4\\-2\end{bmatrix}}$, (c) ${\nabla h(1,0,-1)=\begin{bmatrix}-2\\-4\\2\end{bmatrix}}$

---

<a id="p11"></a>

### P11. 야코비 행렬

HW1 Problem 11 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p11)

#### 주어진 조건

다음 두 벡터값 함수가 주어져요.

$$
{\mathbf{f}(u,v)=\begin{bmatrix}u+2v\\3u-v\end{bmatrix}},\quad{\mathbf{g}(u,v)=\begin{bmatrix}u^2+v\\uv\\v^2\end{bmatrix}}
$$

#### 구할 것

각 함수의 야코비 행렬을 구하고 주어진 점에서 값을 계산해 보세요.

- (a) $\mathbf{J}_\mathbf{f}$, $(u,v)=(1,2)$
- (b) $\mathbf{J}_\mathbf{g}$, $(u,v)=(1,2)$

#### 과제 원문

"Find the Jacobian matrix of each vector-valued function and evaluate it at the indicated point. Hint: For $\mathbf{f}:\mathbb{R}^n\to\mathbb{R}^m$, ${(\mathbf{J}_\mathbf{f})_{ij}=\partial f_i/\partial x_j}$. The Jacobian has $m$ rows (outputs) and $n$ columns (inputs).

(a) ${\mathbf{f}(u,v)=\begin{bmatrix}u+2v\\3u-v\end{bmatrix}}$ at $(u,v)=(1,2)$.

(b) ${\mathbf{g}(u,v)=\begin{bmatrix}u^2+v\\uv\\v^2\end{bmatrix}}$ at $(u,v)=(1,2)$."

#### 무엇을 구하는 문제인가요?

출력이 여러 개일 때 각 출력의 편미분을 행으로 쌓은 것이 야코비안(Jacobian)이에요. 입력 2개는 두 열에 대응해요.

#### 종이에 쓸 첫 줄

$J_{ij}=\partial f_i/\partial x_j$부터 써요. 첫 행은 첫 출력의 u,v 미분, 둘째 행은 둘째 출력의 미분이에요. (a)는 2×2, (b)는 3×2예요.

#### 한 단계씩 계산해요

#### (a)

(a) 출력 $f_1=u+2v$, $f_2=3u-v$를 $u$, $v$로 미분해 행으로 쌓아요. 모든 편미분이 상수라 점과 상관없이 같아요.

$$
\mathbf{J}_\mathbf{f}=\begin{bmatrix}\partial f_1/\partial u & \partial f_1/\partial v\\\partial f_2/\partial u & \partial f_2/\partial v\end{bmatrix}=\begin{bmatrix}1 & 2\\3 & -1\end{bmatrix}
$$

#### (b)

(b) 출력이 3개, 입력이 2개라 $3\times 2$ 행렬이에요.

$$
\mathbf{J}_\mathbf{g}=\begin{bmatrix}2u & 1\\v & u\\0 & 2v\end{bmatrix}
$$

(b) $(u,v)=(1,2)$를 넣어요.

$$
\mathbf{J}_\mathbf{g}(1,2)=\begin{bmatrix}2 & 1\\2 & 1\\0 & 4\end{bmatrix}
$$

**완성 답**<br>정답: (a) ${\mathbf{J}_\mathbf{f}(1,2)=\begin{bmatrix}1 & 2\\3 & -1\end{bmatrix}}$, (b) ${\mathbf{J}_\mathbf{g}(1,2)=\begin{bmatrix}2 & 1\\2 & 1\\0 & 4\end{bmatrix}}$

#### 다른 길로 검산해요

#### (a) 검산

입력을 $(\Delta u,\Delta v)=(a,b)$만큼 바꾸면 출력 변화는 정확히 $(a+2b,3a-b)^\top=J(a,b)^\top$이에요.

#### (b) 검산

$(1,2)$에서 입력 변화 $(a,b)$에 대한 출력 변화는 $(2a+b+a^2,2a+b+ab,4b+b^2)^\top$이에요. 일차항만 모으면 표시한 $3\times2$ 야코비안의 곱이에요.

#### 이 부분을 조심해요

출력과 입력의 축을 뒤집지 않아요. 마지막 출력 $v^2$는 u와 무관하므로 그 행 첫 원소는 0이에요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$J_{ij}=\partial f_i/\partial x_j$부터 써요. 첫 행은 첫 출력의 u,v 미분, 둘째 행은 둘째 출력의 미분이에요. (a)는 2×2, (b)는 3×2예요.

#### 핵심 주의점

출력과 입력의 축을 뒤집지 않아요. 마지막 출력 $v^2$는 u와 무관하므로 그 행 첫 원소는 0이에요.

#### 답

정답: (a) ${\mathbf{J}_\mathbf{f}(1,2)=\begin{bmatrix}1 & 2\\3 & -1\end{bmatrix}}$, (b) ${\mathbf{J}_\mathbf{g}(1,2)=\begin{bmatrix}2 & 1\\2 & 1\\0 & 4\end{bmatrix}}$

---

<a id="p12"></a>

### P12. 이차형식의 정류점

HW1 Problem 12 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p12)

#### 주어진 조건

모든 벡터는 열벡터이고, gradient도 열벡터로 써요. $\mathbf{x}=(x_1,x_2)^\top$이고

$$
{\mathbf{Q}=\begin{bmatrix}3 & 1\\1 & 2\end{bmatrix}},\quad{\mathbf{b}=\begin{bmatrix}1\\-1\end{bmatrix}},\quad{h(\mathbf{x})=\mathbf{x}^\top\mathbf{Q}\mathbf{x}-2\mathbf{b}^\top\mathbf{x}}
$$

#### 구할 것

다음을 구해 보세요.

- (a) $h$를 $x_1,x_2$로 전개하고 $\partial h/\partial x_1$, $\partial h/\partial x_2$를 계산해요.
- (b) 두 편미분을 $0$으로 두고 $x_1,x_2$를 구해요.

#### 과제 원문

"Let $\mathbf{x}=(x_1,x_2)^\top$ and ${\mathbf{Q}=\begin{bmatrix}3 & 1\\1 & 2\end{bmatrix}}$, ${\mathbf{b}=\begin{bmatrix}1\\-1\end{bmatrix}}$, ${h(\mathbf{x})=\mathbf{x}^\top\mathbf{Q}\mathbf{x}-2\mathbf{b}^\top\mathbf{x}}$.

(a) Expand $h$ in terms of $x_1,x_2$, and compute $\partial h/\partial x_1$ and $\partial h/\partial x_2$.

(b) Set both derivatives equal to zero and solve for $x_1,x_2$."

#### 무엇을 구하는 문제인가요?

행렬로 짧게 적힌 이차식을 두 변수 다항식으로 펼치고, 기울기가 0이 되는 점을 찾아요.

#### 종이에 쓸 첫 줄

$Qx=(3x_1+x_2,x_1+2x_2)^\top$부터 써요. 왼쪽에서 $(x_1,x_2)$를 곱하면 교차항이 두 번 생기는 이유가 보여요.

#### 한 단계씩 계산해요

#### (a)

(a) $\mathbf{x}^\top\mathbf{Q}\mathbf{x}=3x_1^2+x_1x_2+x_2x_1+2x_2^2=3x_1^2+2x_1x_2+2x_2^2$이고, $2\mathbf{b}^\top\mathbf{x}=2(x_1-x_2)$예요.

$$
h=3x_1^2+2x_1x_2+2x_2^2-2x_1+2x_2
$$

(a) 편미분하면 $\partial h/\partial x_1=6x_1+2x_2-2$, $\partial h/\partial x_2=2x_1+4x_2+2$예요.

#### (b)

(b) 두 식을 $0$으로 두면 $3x_1+x_2=1$, $x_1+2x_2=-1$이에요. 둘째 식에서 $x_1=-1-2x_2$를 첫 식에 넣으면 $-3-6x_2+x_2=1$, 즉 $x_2=-\frac{4}{5}$예요.

(b) 그러면 $x_1=-1+\frac{8}{5}=\frac{3}{5}$이에요. 검산: $6\cdot\frac{3}{5}+2(-\frac{4}{5})-2=\frac{18-8-10}{5}=0$, $2\cdot\frac{3}{5}+4(-\frac{4}{5})+2=\frac{6-16+10}{5}=0$이에요.

**완성 답**<br>정답: (a) $h=3x_1^2+2x_1x_2+2x_2^2-2x_1+2x_2$, $\partial h/\partial x_1=6x_1+2x_2-2$, $\partial h/\partial x_2=2x_1+4x_2+2$; (b) $x_1=\frac{3}{5}$, $x_2=-\frac{4}{5}$

#### 다른 길로 검산해요

#### (a) 검산

대칭행렬의 공식을 별도로 적용하면 $\nabla h=2Qx-2b=(6x_1+2x_2-2,2x_1+4x_2+2)^\top$예요. 직접 편미분과 같아요.

#### (b) 검산

$Q(3/5,-4/5)^\top=(1,-1)^\top=b$예요. 또 $Q$의 첫 주축소행렬식은 3, 행렬식은 5로 양수라 헤시안 $2Q$는 양의 정부호예요. 구한 점은 유일한 전역 최소점이에요.

#### 이 부분을 조심해요

교차항 $x_1x_2$가 두 번 있다는 것을 놓치지 않아요. $-2b^\top x=-2x_1+2x_2$의 둘째 부호도 확인해요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$Qx=(3x_1+x_2,x_1+2x_2)^\top$부터 써요. 왼쪽에서 $(x_1,x_2)$를 곱하면 교차항이 두 번 생기는 이유가 보여요.

#### 핵심 주의점

교차항 $x_1x_2$가 두 번 있다는 것을 놓치지 않아요. $-2b^\top x=-2x_1+2x_2$의 둘째 부호도 확인해요.

#### 답

정답: (a) $h=3x_1^2+2x_1x_2+2x_2^2-2x_1+2x_2$, $\partial h/\partial x_1=6x_1+2x_2-2$, $\partial h/\partial x_2=2x_1+4x_2+2$; (b) $x_1=\frac{3}{5}$, $x_2=-\frac{4}{5}$

---

<a id="p13"></a>

### P13. 2차원 가우시안 밀도

HW1 Problem 13 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p13)

#### 주어진 조건

모든 벡터는 열벡터예요. $\mathbf{X}\sim\mathcal{N}(\boldsymbol{\mu},\boldsymbol{\Sigma})$이고

$$
{\boldsymbol{\mu}=\begin{bmatrix}1\\-1\end{bmatrix}},\quad{\boldsymbol{\Sigma}=\begin{bmatrix}2 & 1\\1 & 2\end{bmatrix}}
$$

#### 구할 것

결합 밀도 $p_\mathbf{X}(x_1,x_2)$를 정규화 상수까지 포함해 명시적으로 써 보세요. 지수 안의 이차식은 전개해요.

#### 과제 원문

"Suppose $\mathbf{X}\sim\mathcal{N}(\boldsymbol{\mu},\boldsymbol{\Sigma})$, where ${\boldsymbol{\mu}=\begin{bmatrix}1\\-1\end{bmatrix}}$, ${\boldsymbol{\Sigma}=\begin{bmatrix}2 & 1\\1 & 2\end{bmatrix}}$. Write the joint density $p_\mathbf{X}(x_1,x_2)$ explicitly, including its normalizing constant. Expand the quadratic expression in the exponent. Hint: For a $d$-dimensional Gaussian with invertible covariance $\mathbf{S}$, ${\mathcal{N}(\mathbf{z}\mid\mathbf{m},\mathbf{S})=\dfrac{\exp[-\frac{1}{2}(\mathbf{z}-\mathbf{m})^\top\mathbf{S}^{-1}(\mathbf{z}-\mathbf{m})]}{(2\pi)^{d/2}\sqrt{\det\mathbf{S}}}}$."

#### 무엇을 구하는 문제인가요?

가우시안 밀도에는 지수와 정규화 상수가 모두 필요해요. 먼저 평균만큼 중심을 옮긴 좌표를 쓰면 부호 오류가 줄어요.

#### 종이에 쓸 첫 줄

$d=x-\mu=(x_1-1,x_2+1)^\top$부터 써요. 밀도는 $\exp(-d^\top\Sigma^{-1}d/2)/(2\pi\sqrt{\det\Sigma})$예요. 2차원이어서 분모의 $2\pi$는 제곱근이 아니에요.

#### 한 단계씩 계산해요

#### 풀이

$\det\boldsymbol{\Sigma}=2\cdot 2-1\cdot 1=3$이고, 역행렬은

$$
\boldsymbol{\Sigma}^{-1}=\frac{1}{3}\begin{bmatrix}2 & -1\\-1 & 2\end{bmatrix}
$$

$d=2$라 정규화 상수는 $\dfrac{1}{(2\pi)^{2/2}\sqrt{3}}=\dfrac{1}{2\pi\sqrt{3}}$이에요.

$d_1=x_1-1$, $d_2=x_2+1$로 두면 이차형식은

$$
(\mathbf{x}-\boldsymbol{\mu})^\top\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})=\frac{1}{3}(2d_1^2-2d_1d_2+2d_2^2)=\frac{2}{3}(d_1^2-d_1d_2+d_2^2)
$$

각 항을 전개해요. $d_1^2=x_1^2-2x_1+1$, $d_2^2=x_2^2+2x_2+1$, $d_1d_2=x_1x_2+x_1-x_2-1$이에요.

$$
d_1^2-d_1d_2+d_2^2=x_1^2-x_1x_2+x_2^2-3x_1+3x_2+3
$$

지수는 $-\frac{1}{2}\cdot\frac{2}{3}(\cdots)=-\frac{1}{3}(x_1^2-x_1x_2+x_2^2-3x_1+3x_2+3)$이에요. 모두 모으면

$$
p_\mathbf{X}(x_1,x_2)=\frac{1}{2\pi\sqrt{3}}\exp\left[-\frac{1}{3}(x_1^2-x_1x_2+x_2^2-3x_1+3x_2+3)\right]
$$

**완성 답**<br>정답: ${p_\mathbf{X}(x_1,x_2)=\frac{1}{2\pi\sqrt{3}}\exp[-\frac{1}{3}(x_1^2-x_1x_2+x_2^2-3x_1+3x_2+3)]}$

#### 다른 길로 검산해요

#### 답을 확인해요

중심 $(1,-1)$에서 전개된 괄호는 0이어서 최대밀도 $1/(2\pi\sqrt3)$이에요. 이동좌표에서 이차형식은 $\frac23(d_1^2-d_1d_2+d_2^2)$로 전개식과 항별 동일해요. 고윳값 3,1인 공분산이 양의 정부호이므로 가우시안 정규화 공식이 적용돼요.

#### 이 부분을 조심해요

지수에 들어가는 행렬은 공분산의 역인 정밀도(precision)예요. 평균의 둘째 성분이 -1이므로 중심좌표는 $x_2+1$이에요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$d=x-\mu=(x_1-1,x_2+1)^\top$부터 써요. 밀도는 $\exp(-d^\top\Sigma^{-1}d/2)/(2\pi\sqrt{\det\Sigma})$예요. 2차원이어서 분모의 $2\pi$는 제곱근이 아니에요.

#### 핵심 주의점

지수에 들어가는 행렬은 공분산의 역인 정밀도(precision)예요. 평균의 둘째 성분이 -1이므로 중심좌표는 $x_2+1$이에요.

#### 답

정답: ${p_\mathbf{X}(x_1,x_2)=\frac{1}{2\pi\sqrt{3}}\exp[-\frac{1}{3}(x_1^2-x_1x_2+x_2^2-3x_1+3x_2+3)]}$

---

<a id="p14"></a>

### P14. 완전제곱으로 정규화

HW1 Problem 14 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p14)

#### 주어진 조건

단변량 가우시안의 둘째 모수는 분산이에요. $z\in\mathbb{R}$에 대해

$$
p(z)=c\exp\left[-\frac{1}{2}(4z^2-8z+7)\right]
$$

#### 구할 것

$p$가 확률밀도가 되도록 하는 양의 상수 $c$를 구하고, 평균과 분산을 밝혀 보세요. 완전제곱을 이용해요.

#### 과제 원문

"For $z\in\mathbb{R}$, consider ${p(z)=c\exp\left[-\frac{1}{2}(4z^2-8z+7)\right]}$. Find the positive constant $c$ that makes $p$ a probability density, and identify its mean and variance. Use completion of the square. Hint: Compare your expression with ${\mathcal{N}(z\mid\mu,v)=\frac{1}{\sqrt{2\pi v}}\exp\left[-\frac{(z-\mu)^2}{2v}\right]}$."

#### 무엇을 구하는 문제인가요?

지수의 이차식을 완전제곱(completing the square)으로 바꾸면 중심과 폭을 읽을 수 있어요. 남는 상수는 밀도 앞에 반영해요.

#### 종이에 쓸 첫 줄

$4z^2-8z+7=4(z-1)^2+3$부터 써요. 원래 식에 다시 펼쳐 맞는지 확인하고 $e^{-3/2}$를 상수로 꺼내요.

#### 한 단계씩 계산해요

#### 풀이

완전제곱을 해요.

$$
4z^2-8z+7=4(z^2-2z+1)+3=4(z-1)^2+3
$$

대입하면 상수 부분이 지수 밖으로 나와요.

$$
p(z)=c\,e^{-3/2}\exp\left[-2(z-1)^2\right]=c\,e^{-3/2}\exp\left[-\frac{(z-1)^2}{2\cdot\frac{1}{4}}\right]
$$

$\mathcal{N}(z\mid\mu,v)$와 비교하면 $\mu=1$, $v=\frac{1}{4}$이에요.

밀도가 되려면 앞의 상수가 $\frac{1}{\sqrt{2\pi v}}=\frac{1}{\sqrt{\pi/2}}=\sqrt{\frac{2}{\pi}}$와 같아야 해요. 그래서 $c\,e^{-3/2}=\sqrt{\frac{2}{\pi}}$, 즉 $c=\sqrt{\frac{2}{\pi}}e^{3/2}$예요.

**완성 답**<br>정답: $c=\sqrt{\frac{2}{\pi}}e^{3/2}$, 평균 $\mu=1$, 분산 $v=\frac{1}{4}$

#### 다른 길로 검산해요

#### 답을 확인해요

$\int_{-\infty}^{\infty}e^{-2(z-1)^2}dz=\sqrt{\pi/2}$이므로 전체 적분은 $c e^{-3/2}\sqrt{\pi/2}=1$이에요. 따라서 $c=\sqrt{2/\pi}e^{3/2}$, 평균 1, 분산 $1/4$이며 표준편차는 $1/2$예요.

#### 이 부분을 조심해요

분산 v와 표준편차를 혼동하지 않아요. $e^{-3/2}$를 빠뜨리면 c가 틀려요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$4z^2-8z+7=4(z-1)^2+3$부터 써요. 원래 식에 다시 펼쳐 맞는지 확인하고 $e^{-3/2}$를 상수로 꺼내요.

#### 핵심 주의점

분산 v와 표준편차를 혼동하지 않아요. $e^{-3/2}$를 빠뜨리면 c가 틀려요.

#### 답

정답: $c=\sqrt{\frac{2}{\pi}}e^{3/2}$, 평균 $\mu=1$, 분산 $v=\frac{1}{4}$

---

<a id="p15"></a>

### P15. 단순회귀의 우도

HW1 Problem 15 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p15)

#### 주어진 조건

단변량 가우시안의 둘째 모수는 분산이에요. 관측 데이터 $(x_n,y_n)$, $n=1,\dots,N$은 고정되어 있고

$$
y_n=\theta_0+\theta_1x_n+\varepsilon_n
$$

이에요. 잡음 $\varepsilon_n$은 서로 독립인 $\mathcal{N}(0,\sigma^2)$이고 $\sigma^2\gt 0$은 알려져 있어요.

#### 구할 것

$N$개 관측 전체의 우도 $L(\theta_0,\theta_1)$을 상수 인자까지 포함해, 오차제곱합을 담은 하나의 지수 형태로 구해 보세요.

#### 과제 원문

"For fixed observed data $(x_n,y_n)$, $n=1,\dots,N$, consider $y_n=\theta_0+\theta_1x_n+\varepsilon_n$, where the noise terms are independent $\mathcal{N}(0,\sigma^2)$ variables and $\sigma^2\gt 0$ is known. Find the likelihood $L(\theta_0,\theta_1)$ of all $N$ observations, including its constant factor, as a single exponential involving a sum of squared errors."

#### 무엇을 구하는 문제인가요?

관측값은 고정하고, 파라미터를 바꿀 때 그 데이터가 얼마나 그럴듯한지 나타내는 우도(likelihood)를 구해요.

#### 종이에 쓸 첫 줄

$r_n=y_n-\theta_0-\theta_1x_n$부터 써요. 잔차가 잡음이고 $r_n\sim N(0,\sigma^2)$라 한 관측의 밀도를 먼저 쓸 수 있어요. 독립성 때문에 전체 밀도는 곱이에요.

#### 한 단계씩 계산해요

#### 풀이

$\varepsilon_n=y_n-\theta_0-\theta_1x_n\sim\mathcal{N}(0,\sigma^2)$이라 한 관측의 밀도는

$$
p(y_n\mid\theta_0,\theta_1)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\left[-\frac{(y_n-\theta_0-\theta_1x_n)^2}{2\sigma^2}\right]
$$

잡음이 독립이라 우도는 $N$개 밀도의 곱이에요. 상수 인자는 $(2\pi\sigma^2)^{-1/2}$가 $N$번 곱해져 $(2\pi\sigma^2)^{-N/2}$가 돼요.

지수끼리의 곱은 지수의 합이라 하나의 지수로 모여요.

$$
L(\theta_0,\theta_1)=(2\pi\sigma^2)^{-N/2}\exp\left[-\frac{1}{2\sigma^2}\sum_{n=1}^{N}(y_n-\theta_0-\theta_1x_n)^2\right]
$$

**완성 답**<br>정답: ${L(\theta_0,\theta_1)=(2\pi\sigma^2)^{-N/2}\exp[-\frac{1}{2\sigma^2}\sum_{n=1}^{N}(y_n-\theta_0-\theta_1x_n)^2]}$

#### 다른 길로 검산해요

#### 답을 확인해요

$N=1$이면 한 가우시안의 밀도로 돌아가요. 일반 N에서 $(2\pi\sigma^2)^{-1/2}$를 N번 곱한 계수와 지수의 합이 정확히 $(2\pi\sigma^2)^{-N/2}\exp[-\sum r_n^2/(2\sigma^2)]$가 돼요. 이는 모든 양의 $\sigma^2$에서 성립하는 대수적 확인이에요.

#### 이 부분을 조심해요

밀도의 합을 우도라고 쓰지 않아요. 독립 관측은 곱이고, 곱을 지수 하나로 모을 때만 제곱 잔차의 합이 돼요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$r_n=y_n-\theta_0-\theta_1x_n$부터 써요. 잔차가 잡음이고 $r_n\sim N(0,\sigma^2)$라 한 관측의 밀도를 먼저 쓸 수 있어요. 독립성 때문에 전체 밀도는 곱이에요.

#### 핵심 주의점

밀도의 합을 우도라고 쓰지 않아요. 독립 관측은 곱이고, 곱을 지수 하나로 모을 때만 제곱 잔차의 합이 돼요.

#### 답

정답: ${L(\theta_0,\theta_1)=(2\pi\sigma^2)^{-N/2}\exp[-\frac{1}{2\sigma^2}\sum_{n=1}^{N}(y_n-\theta_0-\theta_1x_n)^2]}$

---

<a id="p16"></a>

### P16. 음의 로그우도와 최소제곱

HW1 Problem 16 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p16)

#### 주어진 조건

모든 벡터는 열벡터예요. $\mathbf{y}\mid\boldsymbol{\Phi},\boldsymbol{\theta}\sim\mathcal{N}(\boldsymbol{\Phi}\boldsymbol{\theta},\sigma^2\mathbf{I}_N)$이고 $\sigma^2\gt 0$은 알려져 있어요.

#### 구할 것

상수항까지 포함한 음의 로그우도 전체를 유도해 보세요. 또 $\boldsymbol{\theta}$에 대해 우도를 최대화하는 것이 $\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2$를 최소화하는 것과 같은 이유를 보여요.

#### 과제 원문

"Let $\mathbf{y}\mid\boldsymbol{\Phi},\boldsymbol{\theta}\sim\mathcal{N}(\boldsymbol{\Phi}\boldsymbol{\theta},\sigma^2\mathbf{I}_N)$, where $\sigma^2\gt 0$ is known. Derive the full negative log-likelihood, including its constant term. Show why maximizing the likelihood over $\boldsymbol{\theta}$ is equivalent to minimizing $\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2$."

#### 무엇을 구하는 문제인가요?

우도의 로그를 취하면 곱이 합으로 바뀌어서 계산하기 쉬워요. 음수를 붙이면 최대화 문제가 최소화 문제로 바뀌어요.

#### 종이에 쓸 첫 줄

$r=y-\Phi\theta$, $\det(\sigma^2I_N)=(\sigma^2)^N$부터 써요. 전체 밀도의 정규화 상수를 알아야 음의 로그의 상수항도 빠짐없이 구할 수 있어요.

#### 한 단계씩 계산해요

#### 풀이

공분산이 $\sigma^2\mathbf{I}_N$이라 $\det(\sigma^2\mathbf{I}_N)=\sigma^{2N}$, $(\sigma^2\mathbf{I}_N)^{-1}=\frac{1}{\sigma^2}\mathbf{I}_N$이에요.

그래서 우도는

$$
p(\mathbf{y}\mid\boldsymbol{\Phi},\boldsymbol{\theta})=(2\pi)^{-N/2}(\sigma^{2N})^{-1/2}\exp\left[-\frac{1}{2\sigma^2}(\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta})^\top(\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta})\right]
$$

음의 로그를 취하면 $(2\pi)^{-N/2}\sigma^{-N}=(2\pi\sigma^2)^{-N/2}$이라

$$
-\log p(\mathbf{y}\mid\boldsymbol{\Phi},\boldsymbol{\theta})=\frac{N}{2}\log(2\pi\sigma^2)+\frac{1}{2\sigma^2}\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2
$$

$\log$는 단조증가라 우도 최대화는 음의 로그우도 최소화와 같아요. 첫 항은 $\boldsymbol{\theta}$와 무관한 상수이고, 둘째 항의 계수 $\frac{1}{2\sigma^2}\gt 0$은 최소점의 위치를 바꾸지 않아요. 그래서 우도를 최대화하는 $\boldsymbol{\theta}$는 $\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2$를 최소화하는 $\boldsymbol{\theta}$와 같아요.

**완성 답**<br>정답: ${-\log p(\mathbf{y}\mid\boldsymbol{\Phi},\boldsymbol{\theta})=\frac{N}{2}\log(2\pi\sigma^2)+\frac{1}{2\sigma^2}\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2}$. 상수항과 양의 계수는 최소점을 바꾸지 않으니 ML은 최소제곱과 같아요.

#### 다른 길로 검산해요

#### 답을 확인해요

$\exp[-\{\frac N2\log(2\pi\sigma^2)+\frac1{2\sigma^2}\|r\|^2\}]$를 되돌리면 원 밀도예요. 임의의 두 파라미터 사이 목적함수 차이는 잔차제곱합 차이의 양수 $1/(2\sigma^2)$배라 순서와 최소점이 보존돼요.

#### 이 부분을 조심해요

전체 음의 로그우도를 묻는 단계에서는 상수항을 지우지 않아요. 최적점만 비교할 때는 알려진 양의 분산이 파라미터와 무관하다는 조건을 사용해요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$r=y-\Phi\theta$, $\det(\sigma^2I_N)=(\sigma^2)^N$부터 써요. 전체 밀도의 정규화 상수를 알아야 음의 로그의 상수항도 빠짐없이 구할 수 있어요.

#### 핵심 주의점

전체 음의 로그우도를 묻는 단계에서는 상수항을 지우지 않아요. 최적점만 비교할 때는 알려진 양의 분산이 파라미터와 무관하다는 조건을 사용해요.

#### 답

정답: ${-\log p(\mathbf{y}\mid\boldsymbol{\Phi},\boldsymbol{\theta})=\frac{N}{2}\log(2\pi\sigma^2)+\frac{1}{2\sigma^2}\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2}$. 상수항과 양의 계수는 최소점을 바꾸지 않으니 ML은 최소제곱과 같아요.

---

<a id="p17"></a>

### P17. 정규방정식과 수치 예

HW1 Problem 17 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p17)

#### 주어진 조건

모든 벡터는 열벡터예요. ${\mathbf{y}=\boldsymbol{\Phi}\boldsymbol{\theta}+\boldsymbol{\varepsilon}}$, $\boldsymbol{\varepsilon}\sim\mathcal{N}(\mathbf{0},\sigma^2\mathbf{I}_N)$이고 $\sigma^2\gt 0$은 알려져 있어요. $\boldsymbol{\Phi}$의 $n$번째 행은 $\boldsymbol{\phi}_n^\top$이고

$$
J(\boldsymbol{\theta})=\sum_{n=1}^{N}(y_n-\boldsymbol{\phi}_n^\top\boldsymbol{\theta})^2=\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2
$$

#### 구할 것

- (a) $\boldsymbol{\Phi}$의 열이 선형 독립이라고 가정해요. $J(\boldsymbol{\theta})$를 전개하고 $\nabla_{\boldsymbol{\theta}}J$를 계산한 뒤 $\mathbf{0}$으로 두어 정규방정식과 $\boldsymbol{\theta}_{\mathrm{ML}}$을 유도해 보세요.
- (b) 모델 ${f_{\boldsymbol{\theta}}(x)=\theta_0+\theta_1x}$와 데이터 $(x_1,y_1)=(-1,2)$, $(x_2,y_2)=(0,1)$, $(x_3,y_3)=(1,4)$에 대해 $\boldsymbol{\theta}_{\mathrm{ML}}$, 예측 벡터 $\hat{\mathbf{y}}$, $S$의 값을 계산해 보세요. 여기서 ${\hat{y}_n=\theta_{0,\mathrm{ML}}+\theta_{1,\mathrm{ML}}x_n}$, ${\hat{\mathbf{y}}=(\hat{y}_1,\hat{y}_2,\hat{y}_3)^\top}$, ${S=\sum_{n=1}^{3}(y_n-\hat{y}_n)^2=\|\mathbf{y}-\hat{\mathbf{y}}\|_2^2}$예요.

#### 과제 원문

"Consider ${\mathbf{y}=\boldsymbol{\Phi}\boldsymbol{\theta}+\boldsymbol{\varepsilon}}$, where $\boldsymbol{\varepsilon}\sim\mathcal{N}(\mathbf{0},\sigma^2\mathbf{I}_N)$ and $\sigma^2\gt 0$ is known. Let row $n$ of $\boldsymbol{\Phi}$ be $\boldsymbol{\phi}_n^\top$, and define ${J(\boldsymbol{\theta})=\sum_{n=1}^{N}(y_n-\boldsymbol{\phi}_n^\top\boldsymbol{\theta})^2=\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2}$.

(a) Assume $\boldsymbol{\Phi}$ has linearly independent columns. Expand $J(\boldsymbol{\theta})$, compute $\nabla_{\boldsymbol{\theta}}J$, and set it equal to $\mathbf{0}$ to derive the normal equations and $\boldsymbol{\theta}_{\mathrm{ML}}$.

(b) For the model ${f_{\boldsymbol{\theta}}(x)=\theta_0+\theta_1x}$ and data $(x_1,y_1)=(-1,2)$, $(x_2,y_2)=(0,1)$, $(x_3,y_3)=(1,4)$, calculate the numerical values of $\boldsymbol{\theta}_{\mathrm{ML}}$, the prediction vector $\hat{\mathbf{y}}$, and $S$, defined by ${\hat{y}_n=\theta_{0,\mathrm{ML}}+\theta_{1,\mathrm{ML}}x_n}$, ${\hat{\mathbf{y}}=(\hat{y}_1,\hat{y}_2,\hat{y}_3)^\top}$, ${S=\sum_{n=1}^{3}(y_n-\hat{y}_n)^2=\|\mathbf{y}-\hat{\mathbf{y}}\|_2^2}$."

#### 무엇을 구하는 문제인가요?

제곱오차가 가장 작아지는 계수를 먼저 일반식으로 구하고, 실제 세 데이터에 넣어요. 예측과 실제값의 차이도 끝까지 계산해요.

#### 종이에 쓸 첫 줄

$J=(y-\Phi\theta)^\top(y-\Phi\theta)$부터 써요. 곱을 네 항으로 전개하면 미분할 때 무엇이 상수인지 보이고, 열벡터 gradient를 구할 수 있어요.

#### 한 단계씩 계산해요

#### (a)

(a) 전개해요. $\mathbf{y}^\top\boldsymbol{\Phi}\boldsymbol{\theta}$는 스칼라라 $\boldsymbol{\theta}^\top\boldsymbol{\Phi}^\top\mathbf{y}$와 같아요.

$$
J(\boldsymbol{\theta})=\mathbf{y}^\top\mathbf{y}-2\boldsymbol{\theta}^\top\boldsymbol{\Phi}^\top\mathbf{y}+\boldsymbol{\theta}^\top\boldsymbol{\Phi}^\top\boldsymbol{\Phi}\boldsymbol{\theta}
$$

(a) $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}$는 대칭이라

$$
\nabla_{\boldsymbol{\theta}}J=-2\boldsymbol{\Phi}^\top\mathbf{y}+2\boldsymbol{\Phi}^\top\boldsymbol{\Phi}\boldsymbol{\theta}
$$

(a) $\mathbf{0}$으로 두면 정규방정식 $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}\boldsymbol{\theta}=\boldsymbol{\Phi}^\top\mathbf{y}$를 얻어요.

(a) 열이 선형 독립이면 $\mathbf{v}\ne\mathbf{0}$일 때 $\boldsymbol{\Phi}\mathbf{v}\ne\mathbf{0}$이라 $\mathbf{v}^\top\boldsymbol{\Phi}^\top\boldsymbol{\Phi}\mathbf{v}=\|\boldsymbol{\Phi}\mathbf{v}\|_2^2\gt 0$이에요. 즉 $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}$는 양의 정부호라 가역이고, 헤시안 $2\boldsymbol{\Phi}^\top\boldsymbol{\Phi}$도 양의 정부호라 이 점이 최소예요.

(a) 음의 로그우도는 상수 $+\frac{1}{2\sigma^2}J(\boldsymbol{\theta})$라 $J$의 최소점이 ML 추정이에요.

$$
\boldsymbol{\theta}_{\mathrm{ML}}=(\boldsymbol{\Phi}^\top\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^\top\mathbf{y}
$$

#### (b)

(b) 행이 $(1,x_n)$이라

$$
{\boldsymbol{\Phi}=\begin{bmatrix}1 & -1\\1 & 0\\1 & 1\end{bmatrix}},\quad{\boldsymbol{\Phi}^\top\boldsymbol{\Phi}=\begin{bmatrix}3 & 0\\0 & 2\end{bmatrix}},\quad{\boldsymbol{\Phi}^\top\mathbf{y}=\begin{bmatrix}2+1+4\\-2+0+4\end{bmatrix}=\begin{bmatrix}7\\2\end{bmatrix}}
$$

(b) 대각행렬이라 바로 풀려요.

$$
\boldsymbol{\theta}_{\mathrm{ML}}=\begin{bmatrix}\frac{1}{3} & 0\\0 & \frac{1}{2}\end{bmatrix}\begin{bmatrix}7\\2\end{bmatrix}=\begin{bmatrix}\frac{7}{3}\\1\end{bmatrix}
$$

(b) 예측은 $\hat{y}_n=\frac{7}{3}+x_n$이라 $\hat{y}_1=\frac{4}{3}$, $\hat{y}_2=\frac{7}{3}$, $\hat{y}_3=\frac{10}{3}$이에요.

(b) 잔차는 $2-\frac{4}{3}=\frac{2}{3}$, $1-\frac{7}{3}=-\frac{4}{3}$, $4-\frac{10}{3}=\frac{2}{3}$이에요.

$$
S=\frac{4}{9}+\frac{16}{9}+\frac{4}{9}=\frac{24}{9}=\frac{8}{3}
$$

**완성 답**<br>정답: (a) 정규방정식 ${\boldsymbol{\Phi}^\top\boldsymbol{\Phi}\boldsymbol{\theta}=\boldsymbol{\Phi}^\top\mathbf{y}}$, ${\boldsymbol{\theta}_{\mathrm{ML}}=(\boldsymbol{\Phi}^\top\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^\top\mathbf{y}}$;<br>(b) ${\boldsymbol{\theta}_{\mathrm{ML}}=\begin{bmatrix}\frac{7}{3}\\1\end{bmatrix}}$, ${\hat{\mathbf{y}}=\begin{bmatrix}\frac{4}{3}\\\frac{7}{3}\\\frac{10}{3}\end{bmatrix}}$, $S=\frac{8}{3}$

#### 다른 길로 검산해요

#### (a) 검산

$v\ne0$에 대해 $v^\top\Phi^\top\Phi v=\|\Phi v\|^2>0$이에요. 따라서 헤시안은 양의 정부호예요. 정규방정식 해 $\theta_*$ 주위에서 $J(\theta_*+v)=J(\theta_*)+\|\Phi v\|^2$이므로 전역 최소성과 유일성도 확인돼요.

#### (b) 검산

$\theta_*=(7/3,1)^\top$, $\hat y=(4/3,7/3,10/3)^\top$, $r=(2/3,-4/3,2/3)^\top$이에요. $\Phi^\top r=(0,0)^\top$로 잔차가 두 특징 열과 직교하며 $r^\top r=8/3$이에요.

#### 이 부분을 조심해요

역행렬을 쓰기 전에 열의 선형 독립 조건을 확인해요. 잔차는 원 데이터와 예측의 차이이며, 최소제곱이어도 각 잔차가 0일 필요는 없어요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$J=(y-\Phi\theta)^\top(y-\Phi\theta)$부터 써요. 곱을 네 항으로 전개하면 미분할 때 무엇이 상수인지 보이고, 열벡터 gradient를 구할 수 있어요.

#### 핵심 주의점

역행렬을 쓰기 전에 열의 선형 독립 조건을 확인해요. 잔차는 원 데이터와 예측의 차이이며, 최소제곱이어도 각 잔차가 0일 필요는 없어요.

#### 답

정답: (a) 정규방정식 ${\boldsymbol{\Phi}^\top\boldsymbol{\Phi}\boldsymbol{\theta}=\boldsymbol{\Phi}^\top\mathbf{y}}$, ${\boldsymbol{\theta}_{\mathrm{ML}}=(\boldsymbol{\Phi}^\top\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^\top\mathbf{y}}$;<br>(b) ${\boldsymbol{\theta}_{\mathrm{ML}}=\begin{bmatrix}\frac{7}{3}\\1\end{bmatrix}}$, ${\hat{\mathbf{y}}=\begin{bmatrix}\frac{4}{3}\\\frac{7}{3}\\\frac{10}{3}\end{bmatrix}}$, $S=\frac{8}{3}$

---

<a id="p18"></a>

### P18. MAP과 릿지 회귀

HW1 Problem 18 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p18)

#### 주어진 조건

모든 벡터는 열벡터예요. 모델은 $\mathbf{y}\mid\boldsymbol{\Phi},\boldsymbol{\theta}\sim\mathcal{N}(\boldsymbol{\Phi}\boldsymbol{\theta},\sigma^2\mathbf{I}_N)$이고, 사전분포 $\boldsymbol{\theta}\sim\mathcal{N}(\mathbf{0},b^2\mathbf{I}_K)$는 고정된 입력과 독립이에요. $\sigma^2,b^2\gt 0$은 알려져 있고, 사전분포는 절편이 있다면 절편을 포함한 모든 계수에 적용돼요.

#### 구할 것

$\boldsymbol{\theta}$와 무관한 항을 제외한 음의 로그사후분포를 유도하고 MAP 추정을 구해 보세요. 또 이것이 $\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2+\lambda\|\boldsymbol{\theta}\|_2^2$의 최소화와 같아지는 $\lambda$ 값을 밝혀요.

#### 과제 원문

"In the model $\mathbf{y}\mid\boldsymbol{\Phi},\boldsymbol{\theta}\sim\mathcal{N}(\boldsymbol{\Phi}\boldsymbol{\theta},\sigma^2\mathbf{I}_N)$, place the prior $\boldsymbol{\theta}\sim\mathcal{N}(\mathbf{0},b^2\mathbf{I}_K)$, independent of the fixed inputs. Here $\sigma^2,b^2\gt 0$ are known, and the prior applies to every coefficient, including an intercept if present. Derive the negative log-posterior up to terms independent of $\boldsymbol{\theta}$ and obtain the MAP estimate. Identify the value of $\lambda$ for which this is equivalent to minimizing $\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2+\lambda\|\boldsymbol{\theta}\|_2^2$. Hint: Use Bayes' rule $p(\boldsymbol{\theta}\mid\boldsymbol{\Phi},\mathbf{y})\propto p(\mathbf{y}\mid\boldsymbol{\Phi},\boldsymbol{\theta})p(\boldsymbol{\theta})$. The prior density is ${p(\boldsymbol{\theta})=(2\pi b^2)^{-K/2}\exp[-\|\boldsymbol{\theta}\|_2^2/(2b^2)]}$."

#### 무엇을 구하는 문제인가요?

MAP은 데이터와 잘 맞는 정도에 사전분포의 선호를 더해 결정해요. 여기서는 절편을 포함한 모든 계수가 0에서 멀어질수록 벌점을 받아요.

#### 종이에 쓸 첫 줄

$-\log p(\theta\mid\Phi,y)=-\log p(y\mid\Phi,\theta)-\log p(\theta)+C$부터 써요. 베이즈 규칙의 분모는 theta에 무관해서 C에 들어가요.

#### 한 단계씩 계산해요

#### 풀이

베이즈 규칙에 로그를 취하면 $-\log p(\boldsymbol{\theta}\mid\boldsymbol{\Phi},\mathbf{y})=-\log p(\mathbf{y}\mid\boldsymbol{\Phi},\boldsymbol{\theta})-\log p(\boldsymbol{\theta})+\text{const}$예요. 상수는 $p(\mathbf{y}\mid\boldsymbol{\Phi})$처럼 $\boldsymbol{\theta}$와 무관한 항이에요.

우도와 사전분포의 정규화 상수도 $\boldsymbol{\theta}$와 무관하니 묶어요.

$$
-\log p(\boldsymbol{\theta}\mid\boldsymbol{\Phi},\mathbf{y})=\frac{1}{2\sigma^2}\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2+\frac{1}{2b^2}\|\boldsymbol{\theta}\|_2^2+\text{const}
$$

gradient를 $\mathbf{0}$으로 두면 $-\frac{1}{\sigma^2}\boldsymbol{\Phi}^\top(\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta})+\frac{1}{b^2}\boldsymbol{\theta}=\mathbf{0}$이고, $\sigma^2$를 곱해 정리하면 $(\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+\frac{\sigma^2}{b^2}\mathbf{I}_K)\boldsymbol{\theta}=\boldsymbol{\Phi}^\top\mathbf{y}$예요.

$\frac{\sigma^2}{b^2}\gt 0$이라 $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+\frac{\sigma^2}{b^2}\mathbf{I}_K$는 양의 정부호이고 항상 가역이에요.

$$
\boldsymbol{\theta}_{\mathrm{MAP}}=\left(\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+\frac{\sigma^2}{b^2}\mathbf{I}_K\right)^{-1}\boldsymbol{\Phi}^\top\mathbf{y}
$$

음의 로그사후분포에 양수 $2\sigma^2$를 곱해도 최소점은 그대로예요. 그러면 $\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2+\frac{\sigma^2}{b^2}\|\boldsymbol{\theta}\|_2^2$가 되니 $\lambda=\frac{\sigma^2}{b^2}$이에요.

**완성 답**<br>정답: ${-\log p(\boldsymbol{\theta}\mid\boldsymbol{\Phi},\mathbf{y})=\frac{1}{2\sigma^2}\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2+\frac{1}{2b^2}\|\boldsymbol{\theta}\|_2^2+\text{const}}$, ${\boldsymbol{\theta}_{\mathrm{MAP}}=(\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+\frac{\sigma^2}{b^2}\mathbf{I}_K)^{-1}\boldsymbol{\Phi}^\top\mathbf{y}}$, $\lambda=\frac{\sigma^2}{b^2}$

#### 다른 길로 검산해요

#### 답을 확인해요

$H=\Phi^\top\Phi+\lambda I$에 대해 $v^\top Hv=\|\Phi v\|^2+\lambda\|v\|^2>0$이에요. 열이 종속이어도 $\lambda>0$이면 역이 존재해요. $H\theta_*=\Phi^\top y$를 대입하면 gradient가 0이고 $J(\theta_*+v)-J(\theta_*)=v^\top Hv$라 유일 최소예요. $2\sigma^2$배 후 벌점계수가 $\sigma^2/b^2$인지도 확인해요.

#### 이 부분을 조심해요

$b^2$는 사전 분산이에요. 잔차항 계수를 1로 맞춘 목적함수에서 $\lambda=\sigma^2/b^2$예요. 사전항만의 계수 $1/(2b^2)$와 동일시하지 않아요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$-\log p(\theta\mid\Phi,y)=-\log p(y\mid\Phi,\theta)-\log p(\theta)+C$부터 써요. 베이즈 규칙의 분모는 theta에 무관해서 C에 들어가요.

#### 핵심 주의점

$b^2$는 사전 분산이에요. 잔차항 계수를 1로 맞춘 목적함수에서 $\lambda=\sigma^2/b^2$예요. 사전항만의 계수 $1/(2b^2)$와 동일시하지 않아요.

#### 답

정답: ${-\log p(\boldsymbol{\theta}\mid\boldsymbol{\Phi},\mathbf{y})=\frac{1}{2\sigma^2}\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2+\frac{1}{2b^2}\|\boldsymbol{\theta}\|_2^2+\text{const}}$, ${\boldsymbol{\theta}_{\mathrm{MAP}}=(\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+\frac{\sigma^2}{b^2}\mathbf{I}_K)^{-1}\boldsymbol{\Phi}^\top\mathbf{y}}$, $\lambda=\frac{\sigma^2}{b^2}$

---

<a id="p19"></a>

### P19. ML과 MAP 수치 비교

HW1 Problem 19 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p19)

#### 주어진 조건

모든 벡터는 열벡터예요. 모델은 ${f_{\boldsymbol{\theta}}(x)=\theta_0+\theta_1x}$, 관측은 $(-1,2)$, $(0,1)$, $(1,4)$이고 잡음 분산은 $\sigma^2=1$로 알려져 있어요. 사전분포 $\boldsymbol{\theta}\sim\mathcal{N}(\mathbf{0},b^2\mathbf{I}_2)$는 절편과 기울기 모두에 적용돼요. 다음 값을 써도 돼요.

$$
{\boldsymbol{\Phi}^\top\boldsymbol{\Phi}=\begin{bmatrix}3 & 0\\0 & 2\end{bmatrix}},\quad{\boldsymbol{\Phi}^\top\mathbf{y}=\begin{bmatrix}7\\2\end{bmatrix}}
$$

#### 구할 것

다음을 구해 보세요.

- (a) ML 추정과 $b^2=1$일 때의 MAP 추정을 계산해요.
- (b) $b^2=\frac{1}{4}$일 때의 MAP 추정을 계산해요. 두 MAP 추정을 ML 추정과 비교하고, $b^2$을 줄이는 효과를 설명해요.

#### 과제 원문

"For ${f_{\boldsymbol{\theta}}(x)=\theta_0+\theta_1x}$, use the observations $(-1,2)$, $(0,1)$, and $(1,4)$ with known noise variance $\sigma^2=1$. The prior is $\boldsymbol{\theta}\sim\mathcal{N}(\mathbf{0},b^2\mathbf{I}_2)$ and applies to both the intercept and the slope. You may use ${\boldsymbol{\Phi}^\top\boldsymbol{\Phi}=\begin{bmatrix}3 & 0\\0 & 2\end{bmatrix}}$, ${\boldsymbol{\Phi}^\top\mathbf{y}=\begin{bmatrix}7\\2\end{bmatrix}}$.

(a) Calculate the ML estimate and the MAP estimate when $b^2=1$.

(b) Calculate the MAP estimate when $b^2=1/4$. Compare the two MAP estimates with the ML estimate and explain the effect of decreasing $b^2$."

#### 무엇을 구하는 문제인가요?

같은 데이터에 사전분포를 다르게 적용해 계수가 얼마나 줄어드는지 비교해요. 이 과제에서는 절편도 규제해요.

#### 종이에 쓸 첫 줄

$\lambda=\sigma^2/b^2$, $(\Phi^\top\Phi+\lambda I)\theta=\Phi^\top y$부터 써요. 대각행렬이라 각 좌표의 식 $(3+\lambda)\theta_0=7$, $(2+\lambda)\theta_1=2$를 따로 풀면 돼요.

#### 한 단계씩 계산해요

#### (a)

(a) ML은 정규방정식의 해예요.

$$
\boldsymbol{\theta}_{\mathrm{ML}}=\begin{bmatrix}3 & 0\\0 & 2\end{bmatrix}^{-1}\begin{bmatrix}7\\2\end{bmatrix}=\begin{bmatrix}\frac{7}{3}\\1\end{bmatrix}
$$

(a) $b^2=1$이면 $\frac{\sigma^2}{b^2}=1$이라 $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+\mathbf{I}=\begin{bmatrix}4 & 0\\0 & 3\end{bmatrix}$이에요.

$$
\boldsymbol{\theta}_{\mathrm{MAP}}=\begin{bmatrix}\frac{7}{4}\\\frac{2}{3}\end{bmatrix}
$$

#### (b)

(b) $b^2=\frac{1}{4}$이면 $\frac{\sigma^2}{b^2}=4$라 $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+4\mathbf{I}=\begin{bmatrix}7 & 0\\0 & 6\end{bmatrix}$이에요.

$$
\boldsymbol{\theta}_{\mathrm{MAP}}=\begin{bmatrix}\frac{7}{7}\\\frac{2}{6}\end{bmatrix}=\begin{bmatrix}1\\\frac{1}{3}\end{bmatrix}
$$

(b) 비교하면 절편은 $\frac{7}{3}\to\frac{7}{4}\to 1$, 기울기는 $1\to\frac{2}{3}\to\frac{1}{3}$로 작아져요. $b^2$을 줄이면 사전분포가 $\mathbf{0}$ 주변에 더 좁게 몰려서 규제 강도 $\lambda=\frac{\sigma^2}{b^2}$가 커지고, MAP 추정이 $\mathbf{0}$ 쪽으로 더 강하게 수축돼요.

**완성 답**<br>정답: (a) ${\boldsymbol{\theta}_{\mathrm{ML}}=\begin{bmatrix}\frac{7}{3}\\1\end{bmatrix}}$, $b^2=1$일 때 ${\boldsymbol{\theta}_{\mathrm{MAP}}=\begin{bmatrix}\frac{7}{4}\\\frac{2}{3}\end{bmatrix}}$; (b) $b^2=\frac{1}{4}$일 때 ${\boldsymbol{\theta}_{\mathrm{MAP}}=\begin{bmatrix}1\\\frac{1}{3}\end{bmatrix}}$. $b^2$이 작을수록 추정이 $\mathbf{0}$ 쪽으로 더 수축돼요.

#### 다른 길로 검산해요

#### (a) 검산

ML은 $(3,2)$에 각각 $(7/3,1)$을 곱하면 $(7,2)$예요. MAP은 $(4,3)$에 $(7/4,2/3)$을 곱하면 똑같이 $(7,2)$가 돼요.

#### (b) 검산

$\lambda=4$일 때 $(7,6)$에 $(1,1/3)$을 곱하면 $(7,2)$예요. 두 좌표 모두 양수이고 분모가 증가하므로 0 쪽으로 수축해요.

#### 이 부분을 조심해요

$b^2=1/4$이면 lambda는 1/4가 아니라 4예요. 절편을 규제에서 빼는 다른 관행을 이 문제에 적용하지 않아요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$\lambda=\sigma^2/b^2$, $(\Phi^\top\Phi+\lambda I)\theta=\Phi^\top y$부터 써요. 대각행렬이라 각 좌표의 식 $(3+\lambda)\theta_0=7$, $(2+\lambda)\theta_1=2$를 따로 풀면 돼요.

#### 핵심 주의점

$b^2=1/4$이면 lambda는 1/4가 아니라 4예요. 절편을 규제에서 빼는 다른 관행을 이 문제에 적용하지 않아요.

#### 답

정답: (a) ${\boldsymbol{\theta}_{\mathrm{ML}}=\begin{bmatrix}\frac{7}{3}\\1\end{bmatrix}}$, $b^2=1$일 때 ${\boldsymbol{\theta}_{\mathrm{MAP}}=\begin{bmatrix}\frac{7}{4}\\\frac{2}{3}\end{bmatrix}}$; (b) $b^2=\frac{1}{4}$일 때 ${\boldsymbol{\theta}_{\mathrm{MAP}}=\begin{bmatrix}1\\\frac{1}{3}\end{bmatrix}}$. $b^2$이 작을수록 추정이 $\mathbf{0}$ 쪽으로 더 수축돼요.

---

<a id="p20"></a>

### P20. 특이한 $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}$와 규제

HW1 Problem 20 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p20)

#### 주어진 조건

모든 벡터는 열벡터예요. ${\boldsymbol{\theta}=(\theta_1,\theta_2)^\top}$이고

$$
{\boldsymbol{\Phi}=\begin{bmatrix}1 & 1\\2 & 2\end{bmatrix}},\quad{\mathbf{y}=\begin{bmatrix}3\\6\end{bmatrix}},\quad{J(\boldsymbol{\theta})=\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2+5\|\boldsymbol{\theta}\|_2^2}
$$

#### 구할 것

다음을 구해 보세요.

- (a) $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}$와 $\det(\boldsymbol{\Phi}^\top\boldsymbol{\Phi})$를 계산해요.
- (b) $\boldsymbol{\theta}_A=(3,0)^\top$, $\boldsymbol{\theta}_B=(1,2)^\top$ 각각에 대해 $\boldsymbol{\Phi}\boldsymbol{\theta}$와 $\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2$를 계산해요.
- (c) $J(\boldsymbol{\theta})$를 최소화하는 $\theta_1,\theta_2$의 값을 구하고 $J$의 최솟값을 계산해요.

#### 과제 원문

"Let ${\boldsymbol{\theta}=(\theta_1,\theta_2)^\top}$ and ${\boldsymbol{\Phi}=\begin{bmatrix}1 & 1\\2 & 2\end{bmatrix}}$, ${\mathbf{y}=\begin{bmatrix}3\\6\end{bmatrix}}$.

(a) Calculate $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}$ and $\det(\boldsymbol{\Phi}^\top\boldsymbol{\Phi})$.

(b) For each of $\boldsymbol{\theta}_A=(3,0)^\top$ and $\boldsymbol{\theta}_B=(1,2)^\top$, calculate $\boldsymbol{\Phi}\boldsymbol{\theta}$ and $\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2$.

(c) Find the numerical values of $\theta_1,\theta_2$ that minimize ${J(\boldsymbol{\theta})=\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2+5\|\boldsymbol{\theta}\|_2^2}$, and calculate the minimum value of $J$."

#### 무엇을 구하는 문제인가요?

두 특징 열이 같아서 데이터만으로는 계수를 구분할 수 없어요. 규제를 붙이면 계수의 합뿐 아니라 각각의 크기도 제한해요.

#### 종이에 쓸 첫 줄

$s=\theta_1+\theta_2$, $\Phi\theta=(s,2s)^\top$부터 써요. 이 데이터가 알려 주는 것은 합 s뿐이라는 사실이 바로 보여요. (c)의 벌점은 두 계수 각각에 적용돼요.

#### 한 단계씩 계산해요

#### (a)

(a) 두 열이 모두 $(1,2)^\top$이라 모든 원소가 $1+4=5$예요.

$$
{\boldsymbol{\Phi}^\top\boldsymbol{\Phi}=\begin{bmatrix}5 & 5\\5 & 5\end{bmatrix}},\quad{\det(\boldsymbol{\Phi}^\top\boldsymbol{\Phi})=25-25=0}
$$

#### (b)

(b) $\boldsymbol{\Phi}\boldsymbol{\theta}_A=(3+0,\,6+0)^\top$, $\boldsymbol{\Phi}\boldsymbol{\theta}_B=(1+2,\,2+4)^\top$로 둘 다 $\begin{bmatrix}3\\6\end{bmatrix}=\mathbf{y}$예요. 그래서 두 경우 모두 $\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2=0$이에요.

(b) $\det=0$이라 정규방정식의 해가 하나로 정해지지 않고, 오차를 $0$으로 만드는 $\boldsymbol{\theta}$가 $\theta_1+\theta_2=3$ 위에 무수히 많아요.

#### (c)

(c) $\nabla J=-2\boldsymbol{\Phi}^\top(\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta})+10\boldsymbol{\theta}=\mathbf{0}$에서 $(\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+5\mathbf{I})\boldsymbol{\theta}=\boldsymbol{\Phi}^\top\mathbf{y}$이고, $\boldsymbol{\Phi}^\top\mathbf{y}=(3+12,\,3+12)^\top=(15,15)^\top$이에요.

$$
\begin{bmatrix}10 & 5\\5 & 10\end{bmatrix}\boldsymbol{\theta}=\begin{bmatrix}15\\15\end{bmatrix}
$$

(c) 두 식을 빼면 $5\theta_1-5\theta_2=0$이라 $\theta_1=\theta_2$, 그러면 $15\theta_1=15$로 $\theta_1=\theta_2=1$이에요. 헤시안 $2(\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+5\mathbf{I})$가 양의 정부호라 이 점이 유일한 최소점이에요.

(c) $\boldsymbol{\Phi}\boldsymbol{\theta}=(2,4)^\top$이라 잔차는 $(1,2)^\top$, $\|\cdot\|_2^2=5$이고 $5\|\boldsymbol{\theta}\|_2^2=5\cdot 2=10$이에요. 그래서 $J_{\min}=5+10=15$예요.

**완성 답**<br>정답: (a) ${\boldsymbol{\Phi}^\top\boldsymbol{\Phi}=\begin{bmatrix}5 & 5\\5 & 5\end{bmatrix}}$, ${\det(\boldsymbol{\Phi}^\top\boldsymbol{\Phi})=0}$; (b) 둘 다 ${\boldsymbol{\Phi}\boldsymbol{\theta}=\begin{bmatrix}3\\6\end{bmatrix}}$, 오차 $0$; (c) ${\boldsymbol{\theta}=\begin{bmatrix}1\\1\end{bmatrix}}$, $J_{\min}=15$

#### 다른 길로 검산해요

#### (a) 검산

각 열 내적은 5여서 Gram은 모든 원소가 5인 행렬이에요. 벡터 $(1,-1)^\top$을 곱하면 0이므로 특이행렬이라는 결론과 행렬식 0이 일치해요.

#### (b) 검산

$(3,0)$과 $(1,2)$의 합은 둘 다 3이라 예측 $(3,6)^\top$과 제곱오차 0이 같아요. 실제로 $\theta_1+\theta_2=3$인 모든 계수가 같은 무규제 최소값을 내요.

#### (c) 검산

$d=\theta_1-\theta_2$를 쓰면 $J=5(3-s)^2+\frac52(s^2+d^2)=\frac{15}{2}(s-2)^2+\frac52d^2+15$예요. 독립적인 완전제곱 검산으로 $s=2,d=0$, 즉 $(1,1)^\top$에서 최소값 15예요.

#### 이 부분을 조심해요

행렬식 0인 Gram 행렬의 역을 억지로 계산하지 않아요. (c)의 J에는 잔차와 벌점이 모두 포함돼요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$s=\theta_1+\theta_2$, $\Phi\theta=(s,2s)^\top$부터 써요. 이 데이터가 알려 주는 것은 합 s뿐이라는 사실이 바로 보여요. (c)의 벌점은 두 계수 각각에 적용돼요.

#### 핵심 주의점

행렬식 0인 Gram 행렬의 역을 억지로 계산하지 않아요. (c)의 J에는 잔차와 벌점이 모두 포함돼요.

#### 답

정답: (a) ${\boldsymbol{\Phi}^\top\boldsymbol{\Phi}=\begin{bmatrix}5 & 5\\5 & 5\end{bmatrix}}$, ${\det(\boldsymbol{\Phi}^\top\boldsymbol{\Phi})=0}$; (b) 둘 다 ${\boldsymbol{\Phi}\boldsymbol{\theta}=\begin{bmatrix}3\\6\end{bmatrix}}$, 오차 $0$; (c) ${\boldsymbol{\theta}=\begin{bmatrix}1\\1\end{bmatrix}}$, $J_{\min}=15$

---

<a id="p21"></a>

### P21. 표본 평균과 공분산

HW1 Problem 21 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p21)

#### 주어진 조건

모든 벡터는 열벡터예요. 2차원 관측 4개가 주어져요.

$$
{\mathbf{x}_1=\begin{bmatrix}1\\1\end{bmatrix}},\quad{\mathbf{x}_2=\begin{bmatrix}1\\3\end{bmatrix}},\quad{\mathbf{x}_3=\begin{bmatrix}3\\3\end{bmatrix}},\quad{\mathbf{x}_4=\begin{bmatrix}3\\5\end{bmatrix}}
$$

#### 구할 것

다음을 구해 보세요.

- (a) 평균 벡터 ${\bar{\mathbf{x}}=\frac{1}{4}\sum_{n=1}^{4}\mathbf{x}_n}$
- (b) 분모를 4로 둔 공분산 행렬 ${\mathbf{S}=\frac{1}{4}\sum_{n=1}^{4}(\mathbf{x}_n-\bar{\mathbf{x}})(\mathbf{x}_n-\bar{\mathbf{x}})^\top}$

#### 과제 원문

"The following four two-dimensional observations are given: ${\mathbf{x}_1=\begin{bmatrix}1\\1\end{bmatrix}}$, ${\mathbf{x}_2=\begin{bmatrix}1\\3\end{bmatrix}}$, ${\mathbf{x}_3=\begin{bmatrix}3\\3\end{bmatrix}}$, ${\mathbf{x}_4=\begin{bmatrix}3\\5\end{bmatrix}}$.

(a) Calculate the mean vector ${\bar{\mathbf{x}}=\frac{1}{4}\sum_{n=1}^{4}\mathbf{x}_n}$.

(b) Calculate the covariance matrix defined here with denominator 4: ${\mathbf{S}=\frac{1}{4}\sum_{n=1}^{4}(\mathbf{x}_n-\bar{\mathbf{x}})(\mathbf{x}_n-\bar{\mathbf{x}})^\top}$."

#### 무엇을 구하는 문제인가요?

각 좌표의 평균을 구한 뒤 평균에서 얼마나 떨어졌는지로 공분산을 계산해요. 이 문제는 분모 4를 명시해요.

#### 종이에 쓸 첫 줄

$\bar x=\frac14\sum_n x_n$, $d_n=x_n-\bar x$부터 써요. 편차를 먼저 적으면 각 관측의 외적(outer product)을 한눈에 확인할 수 있어요.

#### 한 단계씩 계산해요

#### (a)

(a) 성분별로 더해 4로 나눠요. 첫 성분은 $\frac{1+1+3+3}{4}=2$, 둘째 성분은 $\frac{1+3+3+5}{4}=3$이에요.

$$
\bar{\mathbf{x}}=\begin{bmatrix}2\\3\end{bmatrix}
$$

#### (b)

(b) 편차는 $\mathbf{x}_1-\bar{\mathbf{x}}=(-1,-2)^\top$, $\mathbf{x}_2-\bar{\mathbf{x}}=(-1,0)^\top$, $\mathbf{x}_3-\bar{\mathbf{x}}=(1,0)^\top$, $\mathbf{x}_4-\bar{\mathbf{x}}=(1,2)^\top$예요.

(b) 외적은 차례로 $\begin{bmatrix}1 & 2\\2 & 4\end{bmatrix}$, $\begin{bmatrix}1 & 0\\0 & 0\end{bmatrix}$, $\begin{bmatrix}1 & 0\\0 & 0\end{bmatrix}$, $\begin{bmatrix}1 & 2\\2 & 4\end{bmatrix}$이고, 합은 $\begin{bmatrix}4 & 4\\4 & 8\end{bmatrix}$이에요.

(b) 4로 나눠요.

$$
\mathbf{S}=\frac{1}{4}\begin{bmatrix}4 & 4\\4 & 8\end{bmatrix}=\begin{bmatrix}1 & 1\\1 & 2\end{bmatrix}
$$

**완성 답**<br>정답: ${\bar{\mathbf{x}}=\begin{bmatrix}2\\3\end{bmatrix}}$, ${\mathbf{S}=\begin{bmatrix}1 & 1\\1 & 2\end{bmatrix}}$

#### 다른 길로 검산해요

#### (a) 검산

편차 네 개의 합은 $(0,0)^\top$이에요. 평균 $(2,3)^\top$가 모든 관측의 중심인 것을 확인했어요.

#### (b) 검산

별도로 $\frac14\sum x_nx_n^\top=\begin{bmatrix}5&7\\7&11\end{bmatrix}$이고 $\bar x\bar x^\top=\begin{bmatrix}4&6\\6&9\end{bmatrix}$예요. 차이는 $S=\begin{bmatrix}1&1\\1&2\end{bmatrix}$로 편차 외적 방식과 같아요.

#### 이 부분을 조심해요

$d_nd_n^\top$는 2×2 행렬이고 $d_n^\top d_n$는 수예요. 분모를 불편 추정에서 쓰는 3으로 바꾸지 않아요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$\bar x=\frac14\sum_n x_n$, $d_n=x_n-\bar x$부터 써요. 편차를 먼저 적으면 각 관측의 외적(outer product)을 한눈에 확인할 수 있어요.

#### 핵심 주의점

$d_nd_n^\top$는 2×2 행렬이고 $d_n^\top d_n$는 수예요. 분모를 불편 추정에서 쓰는 3으로 바꾸지 않아요.

#### 답

정답: ${\bar{\mathbf{x}}=\begin{bmatrix}2\\3\end{bmatrix}}$, ${\mathbf{S}=\begin{bmatrix}1 & 1\\1 & 2\end{bmatrix}}$

---

<a id="p22"></a>

### P22. 아핀 변환의 평균과 공분산

HW1 Problem 22 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p22)

#### 주어진 조건

모든 벡터는 열벡터이고 $\mathbf{x}=(x_1,x_2)^\top$은 확률벡터예요. $\boldsymbol{\mu}_y=E[\mathbf{y}]$, ${\boldsymbol{\Sigma}_y=\mathrm{Cov}(\mathbf{y})}$, ${\mathbf{C}_{xy}=E[(\mathbf{x}-E[\mathbf{x}])(\mathbf{y}-E[\mathbf{y}])^\top]}$로 써요.

#### 구할 것

- (a) $E[x_1]=1$, $E[x_2]=2$, $\mathrm{Var}(x_1)=4$, $\mathrm{Var}(x_2)=2$, $\mathrm{Cov}(x_1,x_2)=1$이고 ${\mathbf{y}=\begin{bmatrix}x_1+2x_2+1\\-x_1+x_2-2\end{bmatrix}}$일 때 $\boldsymbol{\mu}_y$, $\boldsymbol{\Sigma}_y$, $\mathbf{C}_{xy}$를 구해 보세요.
- (b) 대신 $\mathbf{x}$가 $(x_1,x_2)\in\mathbb{R}^2$에서 가우시안 결합 밀도

  $$
  p_\mathbf{x}(x_1,x_2)=\frac{1}{2\pi}\exp\left[-\frac{1}{2}\left\{(x_1-1)^2-2(x_1-1)(x_2+1)+2(x_2+1)^2\right\}\right]
  $$

  를 가지고 ${\mathbf{y}=\begin{bmatrix}2x_1-x_2-1\\x_1+x_2+2\end{bmatrix}}$예요. 먼저 밀도에서 $\boldsymbol{\mu}_x=E[\mathbf{x}]$와 ${\boldsymbol{\Sigma}_x=\mathrm{Cov}(\mathbf{x})}$를 찾은 뒤 $\boldsymbol{\mu}_y$, $\boldsymbol{\Sigma}_y$, $\mathbf{C}_{xy}$를 구해 보세요.
- (c) $E[x_1]=1$, $E[x_2]=-1$, $\mathrm{Var}(x_1)=2$, $\mathrm{Var}(x_2)=3$, $E[x_1x_2]=0$이에요. $\varepsilon$은 $\mathbf{x}$와 독립이고 $E[\varepsilon]=0$, $\mathrm{Var}(\varepsilon)=1$이며 ${\mathbf{y}=\begin{bmatrix}x_1+x_2+\varepsilon\\x_1-x_2+\varepsilon\end{bmatrix}}$예요. 두 좌표에 같은 $\varepsilon$이 들어가요. $\boldsymbol{\mu}_y$, $\boldsymbol{\Sigma}_y$, $\mathbf{C}_{xy}$를 구해 보세요.

#### 과제 원문

"Let $\mathbf{x}=(x_1,x_2)^\top$ be a random vector. In each part, calculate the mean vector $\boldsymbol{\mu}_y=E[\mathbf{y}]$, the covariance matrix ${\boldsymbol{\Sigma}_y=\mathrm{Cov}(\mathbf{y})}$, and the cross-covariance matrix ${\mathbf{C}_{xy}=\mathrm{Cov}(\mathbf{x},\mathbf{y})=E[(\mathbf{x}-E[\mathbf{x}])(\mathbf{y}-E[\mathbf{y}])^\top]}$.

(a) Suppose $E[x_1]=1$, $E[x_2]=2$, $\mathrm{Var}(x_1)=4$, $\mathrm{Var}(x_2)=2$, $\mathrm{Cov}(x_1,x_2)=1$, and define ${\mathbf{y}=\begin{bmatrix}x_1+2x_2+1\\-x_1+x_2-2\end{bmatrix}}$.

(b) Instead, suppose $\mathbf{x}$ has the Gaussian joint density ${p_\mathbf{x}(x_1,x_2)=\frac{1}{2\pi}\exp[-\frac{1}{2}\{(x_1-1)^2-2(x_1-1)(x_2+1)+2(x_2+1)^2\}]}$, for $(x_1,x_2)\in\mathbb{R}^2$, and define ${\mathbf{y}=\begin{bmatrix}2x_1-x_2-1\\x_1+x_2+2\end{bmatrix}}$. First identify $\boldsymbol{\mu}_x=E[\mathbf{x}]$ and ${\boldsymbol{\Sigma}_x=\mathrm{Cov}(\mathbf{x})}$ from the density. Then calculate $\boldsymbol{\mu}_y$, $\boldsymbol{\Sigma}_y$, and $\mathbf{C}_{xy}$.

(c) Suppose $E[x_1]=1$, $E[x_2]=-1$, $\mathrm{Var}(x_1)=2$, $\mathrm{Var}(x_2)=3$, $E[x_1x_2]=0$. Let $\varepsilon$ be independent of $\mathbf{x}$, with $E[\varepsilon]=0$ and $\mathrm{Var}(\varepsilon)=1$. Define ${\mathbf{y}=\begin{bmatrix}x_1+x_2+\varepsilon\\x_1-x_2+\varepsilon\end{bmatrix}}$. The same random variable $\varepsilon$ appears in both coordinates. Calculate $\boldsymbol{\mu}_y$, $\boldsymbol{\Sigma}_y$, and $\mathbf{C}_{xy}$."

#### 무엇을 구하는 문제인가요?

평균은 선형 변환하고, 공분산은 양쪽에서 행렬을 곱해요. (b)는 지수에서 역공분산을 읽어야 하고, (c)는 같은 잡음이 두 출력에 함께 들어가요.

#### 종이에 쓸 첫 줄

$y=Ax+c$, $y-E[y]=A(x-E[x])$부터 써요. 중심화하면 상수 c가 사라져 $\Sigma_y=A\Sigma_xA^\top$, $C_{xy}=\Sigma_xA^\top$를 정의에서 얻어요. (c)는 여기에 $\varepsilon(1,1)^\top$를 더해요.

#### 한 단계씩 계산해요

공통 공식: $\mathbf{y}=\mathbf{A}\mathbf{x}+\mathbf{c}$이면 $\mathbf{y}-\boldsymbol{\mu}_y=\mathbf{A}(\mathbf{x}-\boldsymbol{\mu}_x)$라서 $\boldsymbol{\mu}_y=\mathbf{A}\boldsymbol{\mu}_x+\mathbf{c}$, $\boldsymbol{\Sigma}_y=\mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top$, $\mathbf{C}_{xy}=E[(\mathbf{x}-\boldsymbol{\mu}_x)(\mathbf{x}-\boldsymbol{\mu}_x)^\top]\mathbf{A}^\top=\boldsymbol{\Sigma}_x\mathbf{A}^\top$예요.

#### (a)

(a) $\mathbf{A}=\begin{bmatrix}1 & 2\\-1 & 1\end{bmatrix}$, $\mathbf{c}=\begin{bmatrix}1\\-2\end{bmatrix}$, $\boldsymbol{\mu}_x=\begin{bmatrix}1\\2\end{bmatrix}$, $\boldsymbol{\Sigma}_x=\begin{bmatrix}4 & 1\\1 & 2\end{bmatrix}$이에요.

$$
\boldsymbol{\mu}_y=\begin{bmatrix}1+4+1\\-1+2-2\end{bmatrix}=\begin{bmatrix}6\\-1\end{bmatrix}
$$

(a) $\mathbf{C}_{xy}=\boldsymbol{\Sigma}_x\mathbf{A}^\top=\begin{bmatrix}4 & 1\\1 & 2\end{bmatrix}\begin{bmatrix}1 & -1\\2 & 1\end{bmatrix}$이에요.

$$
\mathbf{C}_{xy}=\begin{bmatrix}4+2 & -4+1\\1+4 & -1+2\end{bmatrix}=\begin{bmatrix}6 & -3\\5 & 1\end{bmatrix}
$$

(a) $\boldsymbol{\Sigma}_y=\mathbf{A}\mathbf{C}_{xy}$로 계산해요.

$$
\boldsymbol{\Sigma}_y=\begin{bmatrix}1 & 2\\-1 & 1\end{bmatrix}\begin{bmatrix}6 & -3\\5 & 1\end{bmatrix}=\begin{bmatrix}16 & -1\\-1 & 4\end{bmatrix}
$$

#### (b)

(b) 지수 안을 $(\mathbf{x}-\boldsymbol{\mu}_x)^\top\mathbf{P}(\mathbf{x}-\boldsymbol{\mu}_x)$와 비교하면 $\boldsymbol{\mu}_x=\begin{bmatrix}1\\-1\end{bmatrix}$, $\mathbf{P}=\boldsymbol{\Sigma}_x^{-1}=\begin{bmatrix}1 & -1\\-1 & 2\end{bmatrix}$이에요. $\det\mathbf{P}=1$이라 정규화 상수 $\frac{1}{2\pi\sqrt{\det\boldsymbol{\Sigma}_x}}=\frac{1}{2\pi}$와도 맞아요.

$$
\boldsymbol{\Sigma}_x=\mathbf{P}^{-1}=\begin{bmatrix}2 & 1\\1 & 1\end{bmatrix}
$$

(b) $\mathbf{A}=\begin{bmatrix}2 & -1\\1 & 1\end{bmatrix}$, $\mathbf{c}=\begin{bmatrix}-1\\2\end{bmatrix}$이에요.

$$
\boldsymbol{\mu}_y=\begin{bmatrix}2+1-1\\1-1+2\end{bmatrix}=\begin{bmatrix}2\\2\end{bmatrix}
$$

(b) $\mathbf{C}_{xy}=\boldsymbol{\Sigma}_x\mathbf{A}^\top=\begin{bmatrix}2 & 1\\1 & 1\end{bmatrix}\begin{bmatrix}2 & 1\\-1 & 1\end{bmatrix}$이에요.

$$
\mathbf{C}_{xy}=\begin{bmatrix}4-1 & 2+1\\2-1 & 1+1\end{bmatrix}=\begin{bmatrix}3 & 3\\1 & 2\end{bmatrix}
$$

(b) $\boldsymbol{\Sigma}_y=\mathbf{A}\mathbf{C}_{xy}$로 계산해요.

$$
\boldsymbol{\Sigma}_y=\begin{bmatrix}2 & -1\\1 & 1\end{bmatrix}\begin{bmatrix}3 & 3\\1 & 2\end{bmatrix}=\begin{bmatrix}5 & 4\\4 & 5\end{bmatrix}
$$

#### (c)

(c) $\mathrm{Cov}(x_1,x_2)=E[x_1x_2]-E[x_1]E[x_2]=0-(1)(-1)=1$이라 $\boldsymbol{\Sigma}_x=\begin{bmatrix}2 & 1\\1 & 3\end{bmatrix}$이에요. $\mathbf{y}=\mathbf{A}\mathbf{x}+\varepsilon\mathbf{1}$, $\mathbf{A}=\begin{bmatrix}1 & 1\\1 & -1\end{bmatrix}$, $\mathbf{1}=(1,1)^\top$이고 $E[\varepsilon]=0$이라

$$
\boldsymbol{\mu}_y=\mathbf{A}\boldsymbol{\mu}_x=\begin{bmatrix}1-1\\1+1\end{bmatrix}=\begin{bmatrix}0\\2\end{bmatrix}
$$

(c) $\varepsilon$이 $\mathbf{x}$와 독립이라 $\mathrm{Cov}(\mathbf{x},\varepsilon)=\mathbf{0}$이고 교차공분산엔 영향이 없어요.

$$
\mathbf{C}_{xy}=\boldsymbol{\Sigma}_x\mathbf{A}^\top=\begin{bmatrix}2 & 1\\1 & 3\end{bmatrix}\begin{bmatrix}1 & 1\\1 & -1\end{bmatrix}=\begin{bmatrix}3 & 1\\4 & -2\end{bmatrix}
$$

(c) 공분산에는 $\mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top=\mathbf{A}\mathbf{C}_{xy}=\begin{bmatrix}7 & -1\\-1 & 3\end{bmatrix}$에 같은 $\varepsilon$의 몫 $\mathrm{Var}(\varepsilon)\mathbf{1}\mathbf{1}^\top=\begin{bmatrix}1 & 1\\1 & 1\end{bmatrix}$이 더해져요. 같은 잡음이 두 좌표에 들어가 비대각에도 1이 더해져요.

$$
\boldsymbol{\Sigma}_y=\begin{bmatrix}8 & 0\\0 & 4\end{bmatrix}
$$

**완성 답**<br>정답: (a) ${\boldsymbol{\mu}_y=\begin{bmatrix}6\\-1\end{bmatrix}}$, ${\boldsymbol{\Sigma}_y=\begin{bmatrix}16 & -1\\-1 & 4\end{bmatrix}}$, ${\mathbf{C}_{xy}=\begin{bmatrix}6 & -3\\5 & 1\end{bmatrix}}$;<br>(b) ${\boldsymbol{\mu}_x=\begin{bmatrix}1\\-1\end{bmatrix}}$, ${\boldsymbol{\Sigma}_x=\begin{bmatrix}2 & 1\\1 & 1\end{bmatrix}}$, ${\boldsymbol{\mu}_y=\begin{bmatrix}2\\2\end{bmatrix}}$, ${\boldsymbol{\Sigma}_y=\begin{bmatrix}5 & 4\\4 & 5\end{bmatrix}}$, ${\mathbf{C}_{xy}=\begin{bmatrix}3 & 3\\1 & 2\end{bmatrix}}$;<br>(c) ${\boldsymbol{\mu}_y=\begin{bmatrix}0\\2\end{bmatrix}}$, ${\boldsymbol{\Sigma}_y=\begin{bmatrix}8 & 0\\0 & 4\end{bmatrix}}$, ${\mathbf{C}_{xy}=\begin{bmatrix}3 & 1\\4 & -2\end{bmatrix}}$

#### 다른 길로 검산해요

#### (a) 검산

성분별 검산: $\mathrm{Var}(x_1+2x_2)=4+4\cdot2+4\cdot1=16$, $\mathrm{Var}(-x_1+x_2)=4+2-2=4$, 교차항 $-4+(1-2)\cdot1+2\cdot2=-1$이에요. 평균 $(6,-1)^\top$과 $C_{xy}=\begin{bmatrix}6&-3\\5&1\end{bmatrix}$도 각 입력과 출력의 공분산으로 다시 계산돼요.

#### (b) 검산

정밀도 $P=\begin{bmatrix}1&-1\\-1&2\end{bmatrix}$와 $\Sigma_x=\begin{bmatrix}2&1\\1&1\end{bmatrix}$의 곱은 I예요. 성분별로 출력분산은 $4\cdot2+1-4=5$, $2+1+2=5$, 교차항은 $4+1-1=4$예요. 따라서 평균 $(2,2)^\top$, 공분산 $\begin{bmatrix}5&4\\4&5\end{bmatrix}$, 교차공분산 $\begin{bmatrix}3&3\\1&2\end{bmatrix}$예요.

#### (c) 검산

$\mathrm{Cov}(x_1,x_2)=0-(1)(-1)=1$이에요. 출력분산은 $2+3+2+1=8$, $2+3-2+1=4$이고 두 출력의 공분산은 $2-3+1=0$이에요. 평균 $(0,2)^\top$이며 입력-잡음 독립성 때문에 $C_{xy}=\begin{bmatrix}3&1\\4&-2\end{bmatrix}$에 잡음 항은 없어요.

#### 이 부분을 조심해요

(b)의 교차항 계수는 정밀도 비대각 원소의 두 배예요. (c)의 $E[x_1x_2]=0$은 공분산 0이 아니며, 공유 잡음 공분산은 I가 아니라 모든 원소가 1인 행렬이에요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$y=Ax+c$, $y-E[y]=A(x-E[x])$부터 써요. 중심화하면 상수 c가 사라져 $\Sigma_y=A\Sigma_xA^\top$, $C_{xy}=\Sigma_xA^\top$를 정의에서 얻어요. (c)는 여기에 $\varepsilon(1,1)^\top$를 더해요.

#### 핵심 주의점

(b)의 교차항 계수는 정밀도 비대각 원소의 두 배예요. (c)의 $E[x_1x_2]=0$은 공분산 0이 아니며, 공유 잡음 공분산은 I가 아니라 모든 원소가 1인 행렬이에요.

#### 답

정답: (a) ${\boldsymbol{\mu}_y=\begin{bmatrix}6\\-1\end{bmatrix}}$, ${\boldsymbol{\Sigma}_y=\begin{bmatrix}16 & -1\\-1 & 4\end{bmatrix}}$, ${\mathbf{C}_{xy}=\begin{bmatrix}6 & -3\\5 & 1\end{bmatrix}}$;<br>(b) ${\boldsymbol{\mu}_x=\begin{bmatrix}1\\-1\end{bmatrix}}$, ${\boldsymbol{\Sigma}_x=\begin{bmatrix}2 & 1\\1 & 1\end{bmatrix}}$, ${\boldsymbol{\mu}_y=\begin{bmatrix}2\\2\end{bmatrix}}$, ${\boldsymbol{\Sigma}_y=\begin{bmatrix}5 & 4\\4 & 5\end{bmatrix}}$, ${\mathbf{C}_{xy}=\begin{bmatrix}3 & 3\\1 & 2\end{bmatrix}}$;<br>(c) ${\boldsymbol{\mu}_y=\begin{bmatrix}0\\2\end{bmatrix}}$, ${\boldsymbol{\Sigma}_y=\begin{bmatrix}8 & 0\\0 & 4\end{bmatrix}}$, ${\mathbf{C}_{xy}=\begin{bmatrix}3 & 1\\4 & -2\end{bmatrix}}$

---

<a id="p23"></a>

### P23. 절편 없는 회귀의 ML과 MAP

HW1 Problem 23 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p23)

#### 주어진 조건

단변량 가우시안의 둘째 모수는 분산이에요. 절편 없는 선형회귀

$$
y_n=\theta x_n+\varepsilon_n
$$

에서 잡음은 서로 독립인 $\mathcal{N}(0,1)$이에요. 관측은 $(x_1,y_1)=(1,2)$, $(x_2,y_2)=(2,3)$이고, MAP 추정에는 사전분포 $\theta\sim\mathcal{N}(0,1)$을 써요.

#### 구할 것

다음을 구해 보세요.

- (a) 상수 인자를 포함한 우도 $L(\theta)$
- (b) 음의 로그우도를 미분해 $\theta_{\mathrm{ML}}$
- (c) 음의 로그사후분포를 미분해 $\theta_{\mathrm{MAP}}$. 그리고 $x=3$에서의 두 예측 ${\hat{y}_{\mathrm{ML}}=3\theta_{\mathrm{ML}}}$, ${\hat{y}_{\mathrm{MAP}}=3\theta_{\mathrm{MAP}}}$

#### 과제 원문

"Consider linear regression without an intercept, $y_n=\theta x_n+\varepsilon_n$, where the noise terms are independent $\mathcal{N}(0,1)$ variables. The observed data are $(x_1,y_1)=(1,2)$ and $(x_2,y_2)=(2,3)$. For MAP estimation, use the prior $\theta\sim\mathcal{N}(0,1)$.

(a) Write the likelihood $L(\theta)$, including its constant factor.

(b) Find $\theta_{\mathrm{ML}}$ by differentiating the negative log-likelihood.

(c) Find $\theta_{\mathrm{MAP}}$ by differentiating the negative log-posterior. Then calculate the two predictions ${\hat{y}_{\mathrm{ML}}=3\theta_{\mathrm{ML}}}$ and ${\hat{y}_{\mathrm{MAP}}=3\theta_{\mathrm{MAP}}}$ at $x=3$."

#### 무엇을 구하는 문제인가요?

절편이 없으므로 미지수는 기울기 하나예요. ML은 데이터만, MAP은 기울기가 0에 가깝다는 사전정보도 사용해요.

#### 종이에 쓸 첫 줄

$r_1=2-\theta$, $r_2=3-2\theta$부터 써요. 두 독립 표준 가우시안 밀도를 곱한 뒤 음의 로그를 미분해요.

#### 한 단계씩 계산해요

#### (a)

(a) 각 관측의 밀도는 $\frac{1}{\sqrt{2\pi}}\exp[-\frac{1}{2}(y_n-\theta x_n)^2]$이고 두 개를 곱해요.

$$
L(\theta)=\frac{1}{2\pi}\exp\left[-\frac{1}{2}\left((2-\theta)^2+(3-2\theta)^2\right)\right]
$$

#### (b)

(b) 음의 로그우도는 $\log(2\pi)+\frac{1}{2}[(2-\theta)^2+(3-2\theta)^2]$이에요. 미분하면 $-(2-\theta)-2(3-2\theta)=5\theta-8$이고, $0$으로 두면 $\theta_{\mathrm{ML}}=\frac{8}{5}$예요.

#### (c)

(c) 사전분포 $-\log p(\theta)=\frac{1}{2}\log(2\pi)+\frac{\theta^2}{2}$가 더해져요. 미분하면 $5\theta-8+\theta=6\theta-8$이고, $0$으로 두면 $\theta_{\mathrm{MAP}}=\frac{8}{6}=\frac{4}{3}$예요.

(c) $x=3$에서 $\hat{y}_{\mathrm{ML}}=3\cdot\frac{8}{5}=\frac{24}{5}$, $\hat{y}_{\mathrm{MAP}}=3\cdot\frac{4}{3}=4$예요. MAP은 사전분포 때문에 $0$ 쪽으로 조금 수축돼요.

**완성 답**<br>정답: (a) ${L(\theta)=\frac{1}{2\pi}\exp[-\frac{1}{2}((2-\theta)^2+(3-2\theta)^2)]}$; (b) $\theta_{\mathrm{ML}}=\frac{8}{5}$; (c) $\theta_{\mathrm{MAP}}=\frac{4}{3}$, $\hat{y}_{\mathrm{ML}}=\frac{24}{5}$, $\hat{y}_{\mathrm{MAP}}=4$

#### 다른 길로 검산해요

#### (a) 검산

곱의 상수는 $(2\pi)^{-1/2}(2\pi)^{-1/2}=1/(2\pi)$이고 지수는 $-[(2-\theta)^2+(3-2\theta)^2]/2$예요.

#### (b) 검산

잔차제곱합을 별도로 전개하면 $5\theta^2-16\theta+13=5(\theta-8/5)^2+1/5$예요. 따라서 ML은 $8/5$, 최소 제곱오차는 $1/5$예요.

#### (c) 검산

사전벌점까지 포함한 제곱식은 $6\theta^2-16\theta+13=6(\theta-4/3)^2+7/3$이에요. MAP은 $4/3$, 입력 3에서 예측은 ML $24/5$, MAP 4예요.

#### 이 부분을 조심해요

둘째 잔차를 미분하면 -2가 곱해져요. 예측은 학습에 쓰지 않은 입력 x=3에 구한 계수를 넣는 단계예요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$r_1=2-\theta$, $r_2=3-2\theta$부터 써요. 두 독립 표준 가우시안 밀도를 곱한 뒤 음의 로그를 미분해요.

#### 핵심 주의점

둘째 잔차를 미분하면 -2가 곱해져요. 예측은 학습에 쓰지 않은 입력 x=3에 구한 계수를 넣는 단계예요.

#### 답

정답: (a) ${L(\theta)=\frac{1}{2\pi}\exp[-\frac{1}{2}((2-\theta)^2+(3-2\theta)^2)]}$; (b) $\theta_{\mathrm{ML}}=\frac{8}{5}$; (c) $\theta_{\mathrm{MAP}}=\frac{4}{3}$, $\hat{y}_{\mathrm{ML}}=\frac{24}{5}$, $\hat{y}_{\mathrm{MAP}}=4$

---

<a id="p24"></a>

### P24. 평균 추정의 ML과 MAP

HW1 Problem 24 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p24)

#### 주어진 조건

단변량 가우시안의 둘째 모수는 분산이에요. 모델은 $y_n=\theta+\varepsilon_n$이고 $\varepsilon_n\sim\mathcal{N}(0,1)$은 서로 독립이에요. 관측은 $y_1=2$, $y_2=3$, $y_3=4$이고, MAP 추정에는 사전분포 $\theta\sim\mathcal{N}(1,1)$을 써요.

#### 구할 것

다음을 구해 보세요.

- (a) 상수 인자를 포함한 우도 $L(\theta)$
- (b) 음의 로그우도를 미분해 $0$으로 두고 $\theta_{\mathrm{ML}}$
- (c) 음의 로그사후분포를 미분해 $\theta_{\mathrm{MAP}}$. 사전 평균 $1$에 더 가까운 추정은 어느 쪽인가요?

#### 과제 원문

"Consider the model $y_n=\theta+\varepsilon_n$ with independent $\varepsilon_n\sim\mathcal{N}(0,1)$. The three observations are $y_1=2$, $y_2=3$, and $y_3=4$. For MAP estimation, use the prior $\theta\sim\mathcal{N}(1,1)$.

(a) Write the likelihood $L(\theta)$, including its constant factor.

(b) Find $\theta_{\mathrm{ML}}$ by differentiating the negative log-likelihood and setting the derivative equal to zero.

(c) Find $\theta_{\mathrm{MAP}}$ by differentiating the negative log-posterior. Which estimate is closer to the prior mean 1?"

#### 무엇을 구하는 문제인가요?

여기서는 x 없이 세 관측 모두 같은 평균 theta를 공유해요. 사전분포가 선호하는 중심은 0이 아니라 1이에요.

#### 종이에 쓸 첫 줄

$r_n=y_n-\theta$, $-\log p(\theta)=\frac12(\theta-1)^2+C$부터 써요. 사전 평균이 1이므로 제곱항의 중심도 1이어야 해요.

#### 한 단계씩 계산해요

#### (a)

(a) 세 관측의 밀도를 곱해요.

$$
L(\theta)=(2\pi)^{-3/2}\exp\left[-\frac{1}{2}\sum_{n=1}^{3}(y_n-\theta)^2\right]=(2\pi)^{-3/2}\exp\left[-\frac{1}{2}\left((2-\theta)^2+(3-\theta)^2+(4-\theta)^2\right)\right]
$$

#### (b)

(b) 음의 로그우도를 미분하면 $\sum_{n=1}^{3}(\theta-y_n)=3\theta-9$이고, $0$으로 두면 $\theta_{\mathrm{ML}}=3$이에요. 표본 평균과 같아요.

#### (c)

(c) 사전분포 몫 $\frac{(\theta-1)^2}{2}$의 미분 $\theta-1$이 더해져 $3\theta-9+\theta-1=4\theta-10$이에요. $0$으로 두면 $\theta_{\mathrm{MAP}}=\frac{5}{2}$예요.

(c) 사전 평균 $1$까지의 거리는 ML이 $2$, MAP이 $\frac{3}{2}$라서 MAP 추정이 더 가까워요. 사전분포가 추정을 $1$ 쪽으로 끌어당긴 결과예요.

**완성 답**<br>정답: (a) ${L(\theta)=(2\pi)^{-3/2}\exp[-\frac{1}{2}\sum_{n=1}^{3}(y_n-\theta)^2]}$; (b) $\theta_{\mathrm{ML}}=3$; (c) $\theta_{\mathrm{MAP}}=\frac{5}{2}$이고, 사전 평균 1에 더 가까운 쪽은 MAP이에요.

#### 다른 길로 검산해요

#### (a) 검산

독립 밀도 세 개의 곱은 $(2\pi)^{-3/2}\exp[-((2-\theta)^2+(3-\theta)^2+(4-\theta)^2)/2]$예요. 상수의 지수가 -3/2인지 확인해요.

#### (b) 검산

제곱오차는 $3\theta^2-18\theta+29=3(\theta-3)^2+2$예요. 완전제곱으로 최소점 3을 확인해요.

#### (c) 검산

사전 항을 더한 제곱식은 $4\theta^2-20\theta+30=4(\theta-5/2)^2+5$예요. 따라서 MAP은 $5/2=(3\cdot3+1\cdot1)/(3+1)$이고 사전 평균과의 거리 $3/2$가 ML의 거리 2보다 작아요.

#### 이 부분을 조심해요

P23의 $\theta^2$ 벌점을 그대로 복사하지 않아요. 세 데이터의 평균과 사전 평균의 정밀도 가중 평균을 비교해요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$r_n=y_n-\theta$, $-\log p(\theta)=\frac12(\theta-1)^2+C$부터 써요. 사전 평균이 1이므로 제곱항의 중심도 1이어야 해요.

#### 핵심 주의점

P23의 $\theta^2$ 벌점을 그대로 복사하지 않아요. 세 데이터의 평균과 사전 평균의 정밀도 가중 평균을 비교해요.

#### 답

정답: (a) ${L(\theta)=(2\pi)^{-3/2}\exp[-\frac{1}{2}\sum_{n=1}^{3}(y_n-\theta)^2]}$; (b) $\theta_{\mathrm{ML}}=3$; (c) $\theta_{\mathrm{MAP}}=\frac{5}{2}$이고, 사전 평균 1에 더 가까운 쪽은 MAP이에요.

---

<a id="p25"></a>

### P25. 두 가우시안의 곱

HW1 Problem 25 · [원 문제 보기](%EA%B3%BC%EC%A0%9C1_Homework1.html#p25)

#### 주어진 조건

모든 벡터는 열벡터예요. ${p_0(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_0,\boldsymbol{\Sigma}_0)}$, ${p_1(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_1,\boldsymbol{\Sigma}_1)}$이고

$$
{\boldsymbol{\mu}_0=\begin{bmatrix}0\\0\end{bmatrix}},\quad{\boldsymbol{\mu}_1=\begin{bmatrix}1\\1\end{bmatrix}},\quad{\boldsymbol{\Sigma}_0=\begin{bmatrix}1 & 0\\0 & 2\end{bmatrix}},\quad{\boldsymbol{\Sigma}_1=\begin{bmatrix}2 & 1\\1 & 2\end{bmatrix}}
$$

#### 구할 것

정규화된 곱 $q(\mathbf{x})\propto p_0(\mathbf{x})p_1(\mathbf{x})$의 평균과 공분산을 구하고, 정규화된 밀도를 명시적으로 써 보세요.

#### 과제 원문

"Let ${p_0(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_0,\boldsymbol{\Sigma}_0)}$ and ${p_1(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_1,\boldsymbol{\Sigma}_1)}$, where ${\boldsymbol{\mu}_0=\begin{bmatrix}0\\0\end{bmatrix}}$, ${\boldsymbol{\mu}_1=\begin{bmatrix}1\\1\end{bmatrix}}$, ${\boldsymbol{\Sigma}_0=\begin{bmatrix}1 & 0\\0 & 2\end{bmatrix}}$, ${\boldsymbol{\Sigma}_1=\begin{bmatrix}2 & 1\\1 & 2\end{bmatrix}}$. Determine the mean and covariance of the normalized product $q(\mathbf{x})\propto p_0(\mathbf{x})p_1(\mathbf{x})$, and write its explicit normalized density."

#### 무엇을 구하는 문제인가요?

두 밀도가 동시에 높게 보는 위치를 찾는 문제예요. 곱 자체는 적분이 1일 필요가 없으므로, 정규화된 새 가우시안을 구해요.

#### 종이에 쓸 첫 줄

$P_i=\Sigma_i^{-1}$, $\log(p_0p_1)=-\frac12\sum_{i=0}^1(x-\mu_i)^\top P_i(x-\mu_i)+C$부터 써요. 지수의 이차항과 일차항을 모아 완전제곱하면 평균과 공분산이 나와요.

#### 한 단계씩 계산해요

#### 풀이

로그를 취해 $\mathbf{x}$에 관한 항만 남기면

$$
\log p_0+\log p_1=-\frac{1}{2}\mathbf{x}^\top(\boldsymbol{\Sigma}_0^{-1}+\boldsymbol{\Sigma}_1^{-1})\mathbf{x}+\mathbf{x}^\top(\boldsymbol{\Sigma}_0^{-1}\boldsymbol{\mu}_0+\boldsymbol{\Sigma}_1^{-1}\boldsymbol{\mu}_1)+\text{const}
$$

가우시안 $\mathcal{N}(\boldsymbol{\mu}_q,\boldsymbol{\Sigma}_q)$의 로그는 $-\frac{1}{2}\mathbf{x}^\top\boldsymbol{\Sigma}_q^{-1}\mathbf{x}+\mathbf{x}^\top\boldsymbol{\Sigma}_q^{-1}\boldsymbol{\mu}_q+\text{const}$예요. 이차항과 일차항을 비교하면 $\boldsymbol{\Sigma}_q^{-1}=\boldsymbol{\Sigma}_0^{-1}+\boldsymbol{\Sigma}_1^{-1}$, $\boldsymbol{\mu}_q=\boldsymbol{\Sigma}_q(\boldsymbol{\Sigma}_0^{-1}\boldsymbol{\mu}_0+\boldsymbol{\Sigma}_1^{-1}\boldsymbol{\mu}_1)$이에요.

$\boldsymbol{\Sigma}_0^{-1}=\begin{bmatrix}1 & 0\\0 & \frac{1}{2}\end{bmatrix}$이고 $\det\boldsymbol{\Sigma}_1=3$이라 $\boldsymbol{\Sigma}_1^{-1}=\frac{1}{3}\begin{bmatrix}2 & -1\\-1 & 2\end{bmatrix}$이에요.

$$
\boldsymbol{\Sigma}_q^{-1}=\begin{bmatrix}1+\frac{2}{3} & -\frac{1}{3}\\-\frac{1}{3} & \frac{1}{2}+\frac{2}{3}\end{bmatrix}=\begin{bmatrix}\frac{5}{3} & -\frac{1}{3}\\-\frac{1}{3} & \frac{7}{6}\end{bmatrix}
$$

$\det\boldsymbol{\Sigma}_q^{-1}=\frac{5}{3}\cdot\frac{7}{6}-\frac{1}{9}=\frac{35}{18}-\frac{2}{18}=\frac{11}{6}$이라

$$
\boldsymbol{\Sigma}_q=\frac{6}{11}\begin{bmatrix}\frac{7}{6} & \frac{1}{3}\\\frac{1}{3} & \frac{5}{3}\end{bmatrix}=\begin{bmatrix}\frac{7}{11} & \frac{2}{11}\\\frac{2}{11} & \frac{10}{11}\end{bmatrix}
$$

$\boldsymbol{\mu}_0=\mathbf{0}$이라 $\boldsymbol{\Sigma}_0^{-1}\boldsymbol{\mu}_0=\mathbf{0}$이고, $\boldsymbol{\Sigma}_1^{-1}\boldsymbol{\mu}_1=\frac{1}{3}(2-1,\,-1+2)^\top=(\frac{1}{3},\frac{1}{3})^\top$이에요.

$$
\boldsymbol{\mu}_q=\boldsymbol{\Sigma}_q\begin{bmatrix}\frac{1}{3}\\\frac{1}{3}\end{bmatrix}=\frac{1}{3}\begin{bmatrix}\frac{9}{11}\\\frac{12}{11}\end{bmatrix}=\begin{bmatrix}\frac{3}{11}\\\frac{4}{11}\end{bmatrix}
$$

$\det\boldsymbol{\Sigma}_q=\frac{6}{11}$이라 정규화 상수는 $\frac{1}{2\pi\sqrt{6/11}}=\frac{1}{2\pi}\sqrt{\frac{11}{6}}$이에요.

$$
q(\mathbf{x})=\frac{1}{2\pi}\sqrt{\frac{11}{6}}\exp\left[-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu}_q)^\top\boldsymbol{\Sigma}_q^{-1}(\mathbf{x}-\boldsymbol{\mu}_q)\right]
$$

**완성 답**<br>정답: ${\boldsymbol{\mu}_q=\begin{bmatrix}\frac{3}{11}\\\frac{4}{11}\end{bmatrix}}$, ${\boldsymbol{\Sigma}_q=\begin{bmatrix}\frac{7}{11} & \frac{2}{11}\\\frac{2}{11} & \frac{10}{11}\end{bmatrix}}$, ${\boldsymbol{\Sigma}_q^{-1}=\begin{bmatrix}\frac{5}{3} & -\frac{1}{3}\\-\frac{1}{3} & \frac{7}{6}\end{bmatrix}}$,<br>${q(\mathbf{x})=\frac{1}{2\pi}\sqrt{\frac{11}{6}}\exp[-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu}_q)^\top\boldsymbol{\Sigma}_q^{-1}(\mathbf{x}-\boldsymbol{\mu}_q)]}$

#### 다른 길로 검산해요

#### 답을 확인해요

$P_q\Sigma_q=I_2$, $P_q\mu_q=(1/3,1/3)^\top$를 정확한 분수로 확인했어요. 직접 전개한 원 지수와 중심화 지수의 차이는 $\frac5{22}$이라는 x와 무관한 상수예요. 원 곱의 적분은 $Z=\frac{1}{2\pi\sqrt{11}}e^{-5/22}$이며 $(p_0p_1)/Z$의 앞 계수는 $\frac1{2\pi}\sqrt{11/6}$예요. $\det\Sigma_q=6/11>0$이고 정밀도도 양의 정부호여서 이 밀도의 적분은 1이에요.

#### 이 부분을 조심해요

공분산을 그냥 더하는 것은 독립 확률변수의 합에 쓰는 법칙이에요. 밀도의 곱에서는 정밀도를 더하고 마지막에 역을 취해요.

#### 혼자 다시 풀어봐요

1. 첫 줄의 식을 빈 종이에 쓰고 왜 이 식인지 말해요.
2. 각 소문항의 계산을 답을 보지 않고 끝까지 진행해요.
3. 검산 식으로 답과 조건이 맞는지 확인해요.

**페이지 요약**

#### 첫 줄

$P_i=\Sigma_i^{-1}$, $\log(p_0p_1)=-\frac12\sum_{i=0}^1(x-\mu_i)^\top P_i(x-\mu_i)+C$부터 써요. 지수의 이차항과 일차항을 모아 완전제곱하면 평균과 공분산이 나와요.

#### 핵심 주의점

공분산을 그냥 더하는 것은 독립 확률변수의 합에 쓰는 법칙이에요. 밀도의 곱에서는 정밀도를 더하고 마지막에 역을 취해요.

#### 답

정답: ${\boldsymbol{\mu}_q=\begin{bmatrix}\frac{3}{11}\\\frac{4}{11}\end{bmatrix}}$, ${\boldsymbol{\Sigma}_q=\begin{bmatrix}\frac{7}{11} & \frac{2}{11}\\\frac{2}{11} & \frac{10}{11}\end{bmatrix}}$, ${\boldsymbol{\Sigma}_q^{-1}=\begin{bmatrix}\frac{5}{3} & -\frac{1}{3}\\-\frac{1}{3} & \frac{7}{6}\end{bmatrix}}$,<br>${q(\mathbf{x})=\frac{1}{2\pi}\sqrt{\frac{11}{6}}\exp[-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu}_q)^\top\boldsymbol{\Sigma}_q^{-1}(\mathbf{x}-\boldsymbol{\mu}_q)]}$

---

원 문제·정리노트·PDF는 보존해요.
