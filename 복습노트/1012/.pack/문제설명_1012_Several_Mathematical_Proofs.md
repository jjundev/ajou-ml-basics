# 머신러닝기초 복습 1012 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [P1. 행렬식으로 평행사변형 넓이 재기](#p1)
  - [P2. 행렬식으로 역행렬 판정하기](#p2)
  - [P3. 선형 변환한 확률변수의 밀도 유도](#p3)
  - [P4. 축을 늘리는 변환과 밀도](#p4)
  - [P5. 기울이는 변환과 밀도](#p5)
  - [P6. 잡음이 섞인 아핀 변환의 교차공분산](#p6)
  - [P7. 결합 가우시안 p(x, y) 세우기](#p7)
  - [P8. 시계열 모델의 다음 상태와 관측](#p8)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### P1. 행렬식으로 평행사변형 넓이 재기

MML Example 4.2 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1012_Several_Mathematical_Proofs-%EB%AC%B8%EC%A0%9C.pdf#page=1)

#### 주어진 조건

두 벡터 $\mathbf{b}, \mathbf{g} \in \mathbb{R}^2$를 열로 세운 행렬을 ${\mathbf{A} = [\mathbf{b}, \mathbf{g}]}$라고 해요. 꼭짓점이 $\mathbf{0}$, $\mathbf{b}$, $\mathbf{g}$, $\mathbf{b} + \mathbf{g}$인 평행사변형의 넓이는 $|\det(\mathbf{A})|$예요. $2 \times 2$ 행렬의 행렬식은 ${\det\begin{bmatrix}a_{11} & a_{12} \\ a_{21} & a_{22}\end{bmatrix} = a_{11}a_{22} - a_{12}a_{21}}$예요.

#### 구할 것

- (a) ${\mathbf{b} = \begin{bmatrix}2 \\ 1\end{bmatrix}}$, ${\mathbf{g} = \begin{bmatrix}0 \\ 3\end{bmatrix}}$일 때 평행사변형의 넓이를 구해 보세요.
- (b) ${\mathbf{b} = \begin{bmatrix}2 \\ 1\end{bmatrix}}$, ${\mathbf{g} = \begin{bmatrix}4 \\ 2\end{bmatrix}}$일 때 넓이를 구하고, 왜 그런 값이 나오는지 설명해 보세요.

#### 무엇을 구하는 문제인가요?

행렬식으로 평행사변형 넓이 재기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

행렬식(determinant)은 열벡터가 만드는 부호 있는 넓이예요. 평행사변형의 넓이는 $|b_1g_2-b_2g_1|$이고 선형종속이면0이에요.

#### 종이에 적을 첫 줄

$A=[b,g]$로 두 벡터를 열에 세워요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

두 벡터를 열로 세워요.

$$
\mathbf{A} = [\mathbf{b}, \mathbf{g}] = \begin{bmatrix}2 & 0 \\ 1 & 3\end{bmatrix}
$$

행렬식을 구하고 절댓값을 취해요.

$$
|\det(\mathbf{A})| = |2 \cdot 3 - 0 \cdot 1| = 6
$$

넓이는 6이에요.

#### (b)

같은 방법으로 세워요.

$$
\mathbf{A} = [\mathbf{b}, \mathbf{g}] = \begin{bmatrix}2 & 4 \\ 1 & 2\end{bmatrix}, \qquad |\det(\mathbf{A})| = |2 \cdot 2 - 4 \cdot 1| = 0
$$

$\mathbf{g} = 2\mathbf{b}$라서 두 벡터는 선형종속(linearly dependent)이에요. 같은 직선 위에 있어 2차원 평행사변형을 만들지 못하고, 납작한 선분이 돼요. 그래서 넓이가 0이에요.

#### 완성 답과 검산

#### (a) 검산

2×3−0×1=6이고 넓이6이에요.

#### (b) 검산

2×2−4×1=0이며 g=2b라 모든 점이 한 직선에 있어요.

정답: (a) 넓이 6 (b) 넓이 0. $\mathbf{g} = 2\mathbf{b}$로 두 벡터가 선형종속이라 평행사변형이 납작해져요.

#### 여기서 주의해요

음의 행렬식은 방향을 뜻해요. 실제 넓이는 절댓값이에요.

#### 설명을 닫고 다시 해요

1. $A=[b,g]$로 두 벡터를 열에 세워요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 음의 행렬식은 방향을 뜻해요. 실제 넓이는 절댓값이에요.

**페이지 요약**

#### 떠올릴 개념·공식

행렬식(determinant)은 열벡터가 만드는 부호 있는 넓이예요. $|b_1g_2-b_2g_1|$

#### 첫 줄

$A=[b,g]$로 두 벡터를 열에 세워요.

#### 검산

2×3−0×1=6이고 넓이6이에요. 2×2−4×1=0이며 g=2b라 모든 점이 한 직선에 있어요.

#### 조건·구분

행렬식의 음수 부호는 방향을 뜻하며 실제 넓이는 절댓값이에요. $\mathbf g=2\mathbf b$처럼 선형종속이면 넓이가 $0$이에요.

---

<a id="p2"></a>

### P2. 행렬식으로 역행렬 판정하기

MML Example 4.1 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1012_Several_Mathematical_Proofs-%EB%AC%B8%EC%A0%9C.pdf#page=2)

#### 주어진 조건

$2 \times 2$ 행렬 ${\mathbf{A} = \begin{bmatrix}a_{11} & a_{12} \\ a_{21} & a_{22}\end{bmatrix}}$의 역행렬은 다음과 같아요.

$$
\mathbf{A}^{-1} = \frac{1}{a_{11}a_{22} - a_{12}a_{21}}\begin{bmatrix}a_{22} & -a_{12} \\ -a_{21} & a_{11}\end{bmatrix} \qquad (4.2)
$$

그래서 $\mathbf{A}$는 $a_{11}a_{22} - a_{12}a_{21} \ne 0$일 때만 역행렬을 가져요. 이 값이 행렬식 $\det(\mathbf{A})$예요. 이제 다음 행렬을 봐요.

$$
\boldsymbol{\Sigma} = \begin{bmatrix}4 & 2 \\ 2 & 10\end{bmatrix}
$$

#### 구할 것

- (a) $\det(\boldsymbol{\Sigma})$를 구하고, $\boldsymbol{\Sigma}$가 역행렬을 갖는지 판정해 보세요.
- (b) (4.2)로 $\boldsymbol{\Sigma}^{-1}$을 구해 보세요.

#### 무엇을 구하는 문제인가요?

행렬식으로 역행렬 판정하기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

2×2 역행렬은 det≠0일 때 대각을 교환하고 비대각 부호를 바꾼 행렬을 det로 나눠요. 공분산 Σ의 역행렬은 정밀도 행렬이에요.

#### 종이에 적을 첫 줄

$\det\Sigma=4\cdot10-2\cdot2$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

행렬식은 대각끼리 곱한 값에서 비대각끼리 곱한 값을 빼요.

$$
\det(\boldsymbol{\Sigma}) = 4 \cdot 10 - 2 \cdot 2 = 40 - 4 = 36
$$

$36 \ne 0$이라 $\boldsymbol{\Sigma}$는 역행렬을 가져요.

#### (b)

(4.2)에 넣어요. 대각 성분 4와 10은 자리를 맞바꾸고, 비대각 성분 2는 부호를 바꿔요.

$$
\boldsymbol{\Sigma}^{-1} = \frac{1}{36}\begin{bmatrix}10 & -2 \\ -2 & 4\end{bmatrix} = \begin{bmatrix}\frac{5}{18} & -\frac{1}{18} \\ -\frac{1}{18} & \frac{1}{9}\end{bmatrix}
$$

곱해서 확인해요.

$$
\begin{bmatrix}4 & 2 \\ 2 & 10\end{bmatrix}\begin{bmatrix}10 & -2 \\ -2 & 4\end{bmatrix} = \begin{bmatrix}36 & 0 \\ 0 & 36\end{bmatrix}
$$

이것을 36으로 나누면 $\mathbf{I}$가 되니 역행렬이 맞아요.

#### 완성 답과 검산

#### (a) 검산

det=36&gt;0이고 첫 대각도4&gt;0이므로 이 대칭행렬은 양의 정부호예요.

#### (b) 검산

독립 계산에서 Σ⁻¹=(1/36)[[10,−2],[−2,4]]예요. 양쪽 곱 모두I2로 확인해요.

정답: (a) $\det(\boldsymbol{\Sigma}) = 36 \ne 0$이라 역행렬이 있어요. (b) ${\boldsymbol{\Sigma}^{-1} = \frac{1}{36}\begin{bmatrix}10 & -2 \\ -2 & 4\end{bmatrix}}$

#### 여기서 주의해요

각 원소의 역수를 취하는 것이 역행렬은 아니에요.

#### 설명을 닫고 다시 해요

1. $\det\Sigma=4\cdot10-2\cdot2$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 각 원소의 역수를 취하는 것이 역행렬은 아니에요.

**페이지 요약**

#### 떠올릴 개념·공식

2×2 역행렬은 det≠0일 때 대각을 교환하고 비대각 부호를 바꾼 행렬을 det로 나눠요.

#### 첫 줄

$\det\Sigma=4\cdot10-2\cdot2$예요.

#### 검산

det=36&gt;0이고 첫 대각도4&gt;0이므로 이 대칭행렬은 양의 정부호예요. 독립 계산에서 Σ⁻¹=(1/36)[[10,−2],[−2,4]]예요. 양쪽 곱 모두I2로 확인해요.

#### 조건·구분

공분산 $\boldsymbol\Sigma$의 역행렬은 정밀도 행렬이에요. 각 원소의 역수를 취하는 계산과는 달라요.

---

<a id="p3"></a>

### P3. 선형 변환한 확률변수의 밀도 유도

MML Example 6.17 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1012_Several_Mathematical_Proofs-%EB%AC%B8%EC%A0%9C.pdf#page=3)

#### 주어진 조건

상태가 ${\mathbf{x} = \begin{bmatrix}x_1 \\ x_2\end{bmatrix}}$인 2변수 확률변수 $X$의 밀도는 다음과 같아요.

$$
f(\mathbf{x}) = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{x}^\top\mathbf{x}\right) \qquad (6.145)
$$

행렬 ${\mathbf{A} = \begin{bmatrix}a & b \\ c & d\end{bmatrix}}$로 변환한 확률변수 $Y$의 상태는 $\mathbf{y} = \mathbf{A}\mathbf{x}$예요. $ad - bc \ne 0$이라 $\mathbf{A}$는 역행렬을 가져요. $\mathbf{A}^{-\top}$는 $(\mathbf{A}^{-1})^\top$을 뜻해요.

#### 구할 것

변수변환(change of variables)으로 $Y$의 밀도 $f(\mathbf{y})$를 유도해 보세요.

#### 무엇을 구하는 문제인가요?

선형 변환한 확률변수의 밀도 유도를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

변수변환(change of variables)은 역변환의 밀도에 역 Jacobian 행렬식의 절댓값을 곱해요. $p_Y(y)=p_X(A^{-1}y)/|\det A|$는 가역 A에서 확률 질량을 보존해요.

#### 종이에 적을 첫 줄

$x=A^{-1}y$, $J=\partial x/\partial y=A^{-1}$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

역변환을 구해요. 선형 변환이라 역행렬을 곱하면 돼요.

$$
\mathbf{x} = \mathbf{A}^{-1}\mathbf{y} = \frac{1}{ad - bc}\begin{bmatrix}d & -b \\ -c & a\end{bmatrix}\begin{bmatrix}y_1 \\ y_2\end{bmatrix}
$$

$f(\mathbf{x})$에 대입해요. ${(\mathbf{A}^{-1}\mathbf{y})^\top = \mathbf{y}^\top\mathbf{A}^{-\top}}$이에요.

$$
f(\mathbf{A}^{-1}\mathbf{y}) = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{y}^\top\mathbf{A}^{-\top}\mathbf{A}^{-1}\mathbf{y}\right)
$$

넓이 배율을 봐요. $\mathbf{A}$는 $\mathbf{x}$ 쪽의 단위정사각형을 넓이 $|\det\mathbf{A}| = |ad - bc|$인 평행사변형으로 보내요. 확률은 그대로여야 하니 밀도는 $1/|ad - bc|$배가 돼요.

Jacobian으로도 같아요. ${\frac{\partial}{\partial \mathbf{y}}\mathbf{A}^{-1}\mathbf{y} = \mathbf{A}^{-1}}$이고, 행렬식은

$$
\det\left(\frac{\partial \mathbf{x}}{\partial \mathbf{y}}\right) = \det(\mathbf{A}^{-1}) = \frac{1}{ad - bc}
$$

2단계 식에 이 배율의 절댓값을 곱해요.

$$
f(\mathbf{y}) = f(\mathbf{A}^{-1}\mathbf{y})\left|\det\left(\frac{\partial \mathbf{x}}{\partial \mathbf{y}}\right)\right| = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{y}^\top\mathbf{A}^{-\top}\mathbf{A}^{-1}\mathbf{y}\right)|ad - bc|^{-1}
$$

#### 완성 답과 검산

#### 검산

치환 y=Ax에서 dy=|det A|dx를 곱하면 최종밀도의 적분은 원 표준정규의 적분1이에요. (AAᵀ)⁻¹=A⁻ᵀA⁻¹로 지수와 공분산도 일치해요.

정답:

$$
f(\mathbf{y}) = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{y}^\top\mathbf{A}^{-\top}\mathbf{A}^{-1}\mathbf{y}\right)|ad - bc|^{-1}
$$

#### 여기서 주의해요

forward Jacobian |det A|를 곱하면 정규화가 틀려요. 밀도의 함수 인자와 확률변수를 구별해요.

#### 설명을 닫고 다시 해요

1. $x=A^{-1}y$, $J=\partial x/\partial y=A^{-1}$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. forward Jacobian |det A|를 곱하면 정규화가 틀려요. 밀도의 함수 인자와 확률변수를 구별해요.

**페이지 요약**

#### 떠올릴 개념·공식

변수변환(change of variables)은 역변환의 밀도에 역 Jacobian 행렬식의 절댓값을 곱해요. $p_Y(y)=p_X(A^{-1}y)/|\det A|$

#### 첫 줄

$x=A^{-1}y$, $J=\partial x/\partial y=A^{-1}$예요.

#### 검산

치환 y=Ax에서 dy=|det A|dx를 곱하면 최종밀도의 적분은 원 표준정규의 적분1이에요. (AAᵀ)⁻¹=A⁻ᵀA⁻¹로 지수와 공분산도 일치해요.

#### 조건·구분

$ad-bc\ne0$인 가역 $\mathbf A$가 조건이에요. 순방향 Jacobian $|\det\mathbf A|$를 밀도에 곱하면 정규화가 틀리고, 밀도의 함수 인자와 확률변수를 구별해요.

---

<a id="p4"></a>

### P4. 축을 늘리는 변환과 밀도

MML Example 6.17 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1012_Several_Mathematical_Proofs-%EB%AC%B8%EC%A0%9C.pdf#page=4)

#### 주어진 조건

상태가 ${\mathbf{x} = \begin{bmatrix}x_1 \\ x_2\end{bmatrix}}$인 2변수 확률변수 $X$의 밀도는 다음과 같아요.

$$
f(\mathbf{x}) = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{x}^\top\mathbf{x}\right)
$$

행렬 ${\mathbf{A} = \begin{bmatrix}3 & 0 \\ 0 & 2\end{bmatrix}}$로 변환한 확률변수 $Y$의 상태는 $\mathbf{y} = \mathbf{A}\mathbf{x}$예요.

#### 구할 것

변수변환으로 $Y$의 밀도 $f(\mathbf{y})$를 구해 보세요. 원점에서의 값 $f(\mathbf{0})$도 구해 보세요.

#### 무엇을 구하는 문제인가요?

축을 늘리는 변환과 밀도를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

대각행렬의 선형 변환은 축마다 독립으로 늘려요. A=diag(3,2)의 역은diag(1/3,1/2), 넓이는6배라 밀도 높이는1/6배예요.

#### 종이에 적을 첫 줄

$x_1=y_1/3$, $x_2=y_2/2$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

역변환을 구해요. 대각 행렬이라 각 축을 따로 나누면 돼요.

$$
\mathbf{x} = \mathbf{A}^{-1}\mathbf{y} = \begin{bmatrix}\frac{1}{3} & 0 \\ 0 & \frac{1}{2}\end{bmatrix}\mathbf{y} = \begin{bmatrix}\frac{y_1}{3} \\ \frac{y_2}{2}\end{bmatrix}
$$

$f(\mathbf{x})$에 대입해요. ${\mathbf{x}^\top\mathbf{x} = \mathbf{y}^\top\mathbf{A}^{-\top}\mathbf{A}^{-1}\mathbf{y}}$이고 ${\mathbf{A}^{-\top}\mathbf{A}^{-1} = \begin{bmatrix}\frac{1}{9} & 0 \\ 0 & \frac{1}{4}\end{bmatrix}}$이에요.

$$
\mathbf{x}^\top\mathbf{x} = \frac{y_1^2}{9} + \frac{y_2^2}{4}
$$

넓이 배율은 ${|\det\mathbf{A}| = |3 \cdot 2 - 0 \cdot 0| = 6}$이에요. 단위정사각형이 $3 \times 2$ 직사각형이 되니 넓이가 6배예요. 확률은 보존되니 밀도는 $\frac{1}{6}$배가 돼요. Jacobian 행렬식으로 쓰면 $\det(\mathbf{A}^{-1}) = \frac{1}{6}$이에요.

둘을 곱해요. ${\frac{1}{2\pi} \cdot \frac{1}{6} = \frac{1}{12\pi}}$예요.

$$
f(\mathbf{y}) = \frac{1}{12\pi}\exp\left(-\frac{1}{2}\left(\frac{y_1^2}{9} + \frac{y_2^2}{4}\right)\right)
$$

원점에서는 지수부가 0이라 $\exp(0) = 1$이에요.

$$
f(\mathbf{0}) = \frac{1}{12\pi}
$$

#### 완성 답과 검산

#### 검산

Y의 공분산은diag(9,4), 정규화상수는1/(2π√36)=1/(12π)예요. 원점에서는 지수0이라 같은 값이에요.

정답: $|\det\mathbf{A}| = 6$,

$$
f(\mathbf{y}) = \frac{1}{12\pi}\exp\left(-\frac{1}{2}\left(\frac{y_1^2}{9} + \frac{y_2^2}{4}\right)\right)
$$

$f(\mathbf{0}) = \frac{1}{12\pi}$

#### 여기서 주의해요

분산은9와4예요. 축 길이3과2를 그대로 분산으로 쓰지 않아요.

#### 설명을 닫고 다시 해요

1. $x_1=y_1/3$, $x_2=y_2/2$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 분산은9와4예요. 축 길이3과2를 그대로 분산으로 쓰지 않아요.

**페이지 요약**

#### 떠올릴 개념·공식

대각행렬의 선형 변환은 축마다 독립으로 늘려요. A=diag(3,2)의 역은diag(1/3,1/2), 넓이는6배라 밀도 높이는1/6배예요.

#### 첫 줄

$x_1=y_1/3$, $x_2=y_2/2$예요.

#### 검산

Y의 공분산은diag(9,4), 정규화상수는1/(2π√36)=1/(12π)예요. 원점에서는 지수0이라 같은 값이에요.

#### 조건·구분

축 길이 배율 $3,2$를 분산으로 쓰지 않아요. 분산은 제곱된 $9,4$예요.

---

<a id="p5"></a>

### P5. 기울이는 변환과 밀도

MML Example 6.17 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1012_Several_Mathematical_Proofs-%EB%AC%B8%EC%A0%9C.pdf#page=5)

#### 주어진 조건

상태가 ${\mathbf{x} = \begin{bmatrix}x_1 \\ x_2\end{bmatrix}}$인 2변수 확률변수 $X$의 밀도는 다음과 같아요.

$$
f(\mathbf{x}) = \frac{1}{2\pi}\exp\left(-\frac{1}{2}\mathbf{x}^\top\mathbf{x}\right)
$$

행렬 ${\mathbf{A} = \begin{bmatrix}1 & 1 \\ 0 & 2\end{bmatrix}}$로 변환한 확률변수 $Y$의 상태는 $\mathbf{y} = \mathbf{A}\mathbf{x}$예요.

#### 구할 것

- (a) 역변환 $\mathbf{x} = \mathbf{A}^{-1}\mathbf{y}$를 구해 보세요.
- (b) Jacobian $\frac{\partial \mathbf{x}}{\partial \mathbf{y}}$의 행렬식을 구해 보세요.
- (c) $Y$의 밀도 $f(\mathbf{y})$를 구해 보세요.

#### 무엇을 구하는 문제인가요?

기울이는 변환과 밀도를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

비대각 A는 축을 기울여 성분들을 섞어요. 먼저 역변환을 성분으로 풀고 제곱합에 넣으면 교차항 부호를 확인하기 쉬워요.

#### 종이에 적을 첫 줄

$y_2=2x_2$에서 $x_2=y_2/2$를 먼저 얻어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

${\det\mathbf{A} = 1 \cdot 2 - 1 \cdot 0 = 2}$예요. 2×2 역행렬 공식으로

$$
\mathbf{A}^{-1} = \frac{1}{2}\begin{bmatrix}2 & -1 \\ 0 & 1\end{bmatrix} = \begin{bmatrix}1 & -\frac{1}{2} \\ 0 & \frac{1}{2}\end{bmatrix}
$$

성분으로 쓰면 $x_1 = y_1 - \frac{1}{2}y_2$, $x_2 = \frac{1}{2}y_2$예요.

#### (b)

${\frac{\partial}{\partial \mathbf{y}}\mathbf{A}^{-1}\mathbf{y} = \mathbf{A}^{-1}}$이에요. 행렬식은

$$
\det\left(\frac{\partial \mathbf{x}}{\partial \mathbf{y}}\right) = 1 \cdot \frac{1}{2} - \left(-\frac{1}{2}\right) \cdot 0 = \frac{1}{2}
$$

$\mathbf{A}$가 넓이를 2배로 늘리니 밀도는 $\frac{1}{2}$배가 된다는 뜻이에요.

#### (c)

지수부를 정리해요. ${\mathbf{x}^\top\mathbf{x} = \mathbf{y}^\top\mathbf{A}^{-\top}\mathbf{A}^{-1}\mathbf{y}}$이고

$$
\mathbf{A}^{-\top}\mathbf{A}^{-1} = \begin{bmatrix}1 & 0 \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix}\begin{bmatrix}1 & -\frac{1}{2} \\ 0 & \frac{1}{2}\end{bmatrix} = \begin{bmatrix}1 & -\frac{1}{2} \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix}
$$

성분으로 전개해도 같아요.

$$
x_1^2 + x_2^2 = \left(y_1 - \frac{1}{2}y_2\right)^2 + \frac{1}{4}y_2^2 = y_1^2 - y_1 y_2 + \frac{1}{2}y_2^2
$$

$f(\mathbf{A}^{-1}\mathbf{y})$에 Jacobian 행렬식의 절댓값 $\frac{1}{2}$를 곱해요. ${\frac{1}{2\pi} \cdot \frac{1}{2} = \frac{1}{4\pi}}$예요.

$$
f(\mathbf{y}) = \frac{1}{4\pi}\exp\left(-\frac{1}{2}\left(y_1^2 - y_1 y_2 + \frac{1}{2}y_2^2\right)\right)
$$

#### 완성 답과 검산

#### (a) 검산

역방향 대입으로 x1=y1−y2/2,x2=y2/2예요. A와 역행렬의 곱I2를 확인해요.

#### (b) 검산

역 Jacobian은삼각행렬이고 대각곱1×1/2=1/2예요.

#### (c) 검산

제곱합은y1²−y1y2+y2²/2예요. 공분산 AAᵀ=[[2,2],[2,4]]의 역은[[1,−1/2],[−1/2,1/2]]라 동일한 이차형식이에요.

정답: (a) ${\mathbf{A}^{-1} = \begin{bmatrix}1 & -\frac{1}{2} \\ 0 & \frac{1}{2}\end{bmatrix}}$ (b) $\frac{1}{2}$ (c)

$$
f(\mathbf{y}) = \frac{1}{4\pi}\exp\left(-\frac{1}{2}\left(y_1^2 - y_1 y_2 + \frac{1}{2}y_2^2\right)\right)
$$

#### 여기서 주의해요

역변환 x1=y1−y2/2의 마이너스가 지수의 교차항 −y1y2를 만들어요.

#### 설명을 닫고 다시 해요

1. $y_2=2x_2$에서 $x_2=y_2/2$를 먼저 얻어요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 역변환 x1=y1−y2/2의 마이너스가 지수의 교차항 −y1y2를 만들어요.

**페이지 요약**

#### 떠올릴 개념·공식

비대각 A는 축을 기울여 성분들을 섞어요.

#### 첫 줄

$y_2=2x_2$에서 $x_2=y_2/2$를 먼저 얻어요.

#### 검산

역방향 대입으로 x1=y1−y2/2,x2=y2/2예요. A와 역행렬의 곱I2를 확인해요. 역 Jacobian은삼각행렬이고 대각곱1×1/2=1/2예요. 제곱합은y1²−y1y2+y2²/2예요. 공분산 AAᵀ=[[2,2],[2,4]]의 역은[[1,−1/2],[−1/2,1/2]]라 동일한 이차형식이에요.

#### 조건·구분

밀도는 $f(\mathbf y)=\frac1{4\pi}\exp[-\frac12(y_1^2-y_1y_2+\frac12y_2^2)]$예요. 역변환의 마이너스가 교차항 $-y_1y_2$를 만들어요.

---

<a id="p6"></a>

### P6. 잡음이 섞인 아핀 변환의 교차공분산

MML Exercise 6.12 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1012_Several_Mathematical_Proofs-%EB%AC%B8%EC%A0%9C.pdf#page=6)

#### 주어진 조건

가우시안 확률변수 $\mathbf{x} \sim \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$가 있고 $\mathbf{x} \in \mathbb{R}^D$예요. 여기에

$$
\mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{b} + \mathbf{w}
$$

를 만들어요. $\mathbf{y} \in \mathbb{R}^E$, $\mathbf{A} \in \mathbb{R}^{E \times D}$, $\mathbf{b} \in \mathbb{R}^E$이고, $\mathbf{w} \sim \mathcal{N}(\mathbf{w} \mid \mathbf{0}, \mathbf{Q})$는 독립인 가우시안 잡음이에요. 독립이란 $\mathbf{x}$와 $\mathbf{w}$가 서로 독립이고 $\mathbf{Q}$가 대각 행렬이라는 뜻이에요.

#### 구할 것

교차공분산 $\mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}]$와 $\mathrm{Cov}_{y,x}[\mathbf{y}, \mathbf{x}]$를 구해 보세요.

#### 무엇을 구하는 문제인가요?

잡음이 섞인 아핀 변환의 교차공분산를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

교차공분산(cross covariance)은 $E[(x-\mu_x)(y-\mu_y)^\top]$예요. 첫 입력의 성분이 행, 두 번째 입력의 성분이 열이에요. y=Ax+b+w에서 두 번째 계수A는 전치해 오른쪽에 나와요.

#### 종이에 적을 첫 줄

$y-\mu_y=A(x-\mu_x)+w$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

$\mathbf{y}$의 평균부터 구해요. 기댓값은 linear operator이고 $\mathbb{E}[\mathbf{w}] = \mathbf{0}$이에요.

$$
\boldsymbol{\mu}_y = \mathbb{E}[\mathbf{y}] = \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}
$$

편차를 구해요. $\mathbf{b}$는 빠져요.

$$
\mathbf{y} - \boldsymbol{\mu}_y = \mathbf{A}(\mathbf{x} - \boldsymbol{\mu}_x) + \mathbf{w}
$$

교차공분산의 정의에 넣고 ${(\mathbf{A}\mathbf{B})^\top = \mathbf{B}^\top\mathbf{A}^\top}$를 써요.

$$
\mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}] = \mathbb{E}[(\mathbf{x} - \boldsymbol{\mu}_x)(\mathbf{x} - \boldsymbol{\mu}_x)^\top]\mathbf{A}^\top + \mathbb{E}[(\mathbf{x} - \boldsymbol{\mu}_x)\mathbf{w}^\top]
$$

$\mathbf{A}^\top$는 deterministic이라 기댓값 밖으로 나와요.

$\mathbf{x}$와 $\mathbf{w}$는 독립이라 교차공분산이 0이에요. ${\mathbb{E}[(\mathbf{x} - \boldsymbol{\mu}_x)\mathbf{w}^\top] = \mathbb{E}[\mathbf{x} - \boldsymbol{\mu}_x]\,\mathbb{E}[\mathbf{w}]^\top = \mathbf{0}}$이에요. 그래서

$$
\mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}] = \boldsymbol{\Sigma}_x\mathbf{A}^\top
$$

반대 순서는 전치예요. $\boldsymbol{\Sigma}_x$는 대칭이라 ${\boldsymbol{\Sigma}_x^\top = \boldsymbol{\Sigma}_x}$예요.

$$
\mathrm{Cov}_{y,x}[\mathbf{y}, \mathbf{x}] = \left(\boldsymbol{\Sigma}_x\mathbf{A}^\top\right)^\top = \mathbf{A}\boldsymbol{\Sigma}_x
$$

#### 완성 답과 검산

#### 검산

성분(i,j)은∑k Cov(x_i,x_k)A_jk로 ΣxAᵀ의(i,j)예요. 결과D×E, 반대순서는전치E×D=AΣx예요. 독립 잡음의 교차항은0이고 b도 사라져요.

정답: ${\mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}] = \boldsymbol{\Sigma}_x\mathbf{A}^\top}$, ${\mathrm{Cov}_{y,x}[\mathbf{y}, \mathbf{x}] = \mathbf{A}\boldsymbol{\Sigma}_x}$

#### 여기서 주의해요

Q가 대각이라는 사실만으로 x와 w의 독립은 나오지 않아요. 문제에 별도로 주어진 x,w의 독립을 써요.

#### 설명을 닫고 다시 해요

1. $y-\mu_y=A(x-\mu_x)+w$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. Q가 대각이라는 사실만으로 x와 w의 독립은 나오지 않아요. 문제에 별도로 주어진 x,w의 독립을 써요.

**페이지 요약**

#### 떠올릴 개념·공식

교차공분산(cross covariance)은 $E[(x-\mu_x)(y-\mu_y)^\top]$예요.

#### 첫 줄

$y-\mu_y=A(x-\mu_x)+w$예요.

#### 검산

성분(i,j)은∑k Cov(x_i,x_k)A_jk로 ΣxAᵀ의(i,j)예요. 결과D×E, 반대순서는전치E×D=AΣx예요. 독립 잡음의 교차항은0이고 b도 사라져요.

#### 조건·구분

$\mathbf x$와 $\mathbf w$의 독립은 문제에서 별도로 주어진 조건이에요. $\mathbf Q$가 대각이라는 사실만으로 두 벡터의 독립이 나오지 않아요.

---

<a id="p7"></a>

### P7. 결합 가우시안 p(x, y) 세우기

MML Exercise 6.12 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1012_Several_Mathematical_Proofs-%EB%AC%B8%EC%A0%9C.pdf#page=7)

#### 주어진 조건

가우시안 확률변수 $\mathbf{x} \sim \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$가 있고 $\mathbf{x} \in \mathbb{R}^D$예요. 여기에

$$
\mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{b} + \mathbf{w}
$$

를 만들어요. $\mathbf{y} \in \mathbb{R}^E$, $\mathbf{A} \in \mathbb{R}^{E \times D}$, $\mathbf{b} \in \mathbb{R}^E$이고, $\mathbf{w} \sim \mathcal{N}(\mathbf{w} \mid \mathbf{0}, \mathbf{Q})$는 독립인 가우시안 잡음이에요. 독립이란 $\mathbf{x}$와 $\mathbf{w}$가 서로 독립이고 $\mathbf{Q}$가 대각 행렬이라는 뜻이에요. 결합분포 $p(\mathbf{x}, \mathbf{y})$는 가우시안이에요. 교차공분산은 다음과 같이 주어져요.

$$
\mathrm{Cov}_{x,y}[\mathbf{x}, \mathbf{y}] = \boldsymbol{\Sigma}_x\mathbf{A}^\top, \qquad \mathrm{Cov}_{y,x}[\mathbf{y}, \mathbf{x}] = \mathbf{A}\boldsymbol{\Sigma}_x
$$

#### 구할 것

$\mathbf{y}$의 평균과 공분산 $\mathrm{Var}[\mathbf{y}]$를 구해서, 결합분포 $p(\mathbf{x}, \mathbf{y})$의 평균 벡터와 공분산 행렬(블록 행렬)을 완성해 보세요.

#### 무엇을 구하는 문제인가요?

결합 가우시안 p(x, y) 세우기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

결합가우시안(joint Gaussian)은 평균을 쌓고 자기·교차 공분산을 블록에 배치해요. y=Ax+b+w이면 우하단은AΣxAᵀ+Q이며 좌하단은우상단의 전치예요.

#### 종이에 적을 첫 줄

결합벡터 $u=[x^\top,y^\top]^\top$의 편차를 적어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

평균을 구해요. 기댓값은 linear operator이고 $\mathbb{E}[\mathbf{w}] = \mathbf{0}$이에요.

$$
\boldsymbol{\mu}_y = \mathbb{E}[\mathbf{y}] = \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}
$$

편차는 ${\mathbf{y} - \boldsymbol{\mu}_y = \mathbf{A}(\mathbf{x} - \boldsymbol{\mu}_x) + \mathbf{w}}$예요. $\mathbf{x}$와 $\mathbf{w}$는 독립이라 교차공분산이 0이에요. ${\mathbb{E}[(\mathbf{x} - \boldsymbol{\mu}_x)\mathbf{w}^\top] = \mathbf{0}}$이에요.

$\mathbf{y}$의 공분산을 정의대로 전개해요. $\mathbf{w}$와 $\mathbf{x}$가 만나는 두 항은 0이에요.

$$
\mathrm{Var}[\mathbf{y}] = \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbb{E}[\mathbf{w}\mathbf{w}^\top] = \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q}
$$

교차공분산은 주어진 대로 $\boldsymbol{\Sigma}_x\mathbf{A}^\top$와 $\mathbf{A}\boldsymbol{\Sigma}_x$예요. 왼쪽 위 블록은 ${\mathrm{Var}[\mathbf{x}] = \boldsymbol{\Sigma}_x}$예요.

블록으로 모아요. 결합분포가 가우시안이니 이 평균과 공분산으로 정해져요.

$$
p(\mathbf{x}, \mathbf{y}) = \mathcal{N}\left(\begin{bmatrix}\boldsymbol{\mu}_x \\ \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}\end{bmatrix}, \begin{bmatrix}\boldsymbol{\Sigma}_x & \boldsymbol{\Sigma}_x\mathbf{A}^\top \\ \mathbf{A}\boldsymbol{\Sigma}_x & \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q}\end{bmatrix}\right)
$$

#### 완성 답과 검산

#### 검산

u의 편차는B[x−μx,w]ᵀ 꼴이고 B=[[I,0],[A,I]]예요. B diag(Σx,Q)Bᵀ를 블록곱하면 정확한 네 블록이 나와요. 평균은[μx,Aμx+b]ᵀ예요.

정답: 평균 $\begin{bmatrix}\boldsymbol{\mu}_x \\ \mathbf{A}\boldsymbol{\mu}_x + \mathbf{b}\end{bmatrix}$, 공분산 $\begin{bmatrix}\boldsymbol{\Sigma}_x & \boldsymbol{\Sigma}_x\mathbf{A}^\top \\ \mathbf{A}\boldsymbol{\Sigma}_x & \mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top + \mathbf{Q}\end{bmatrix}$

#### 여기서 주의해요

교차블록에 Q를 더하지 않아요. Q는 y에만 들어간 잡음이에요. x와w의 독립이 핵심이고 Q가 대각일 필요는 없어요.

#### 설명을 닫고 다시 해요

1. 결합벡터 $u=[x^\top,y^\top]^\top$의 편차를 적어요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 교차블록에 Q를 더하지 않아요. Q는 y에만 들어간 잡음이에요. x와w의 독립이 핵심이고 Q가 대각일 필요는 없어요.

**페이지 요약**

#### 떠올릴 개념·공식

결합가우시안(joint Gaussian)은 평균을 쌓고 자기·교차 공분산을 블록에 배치해요. y=Ax+b+w이면 우하단은AΣxAᵀ+Q이며 좌하단은우상단의 전치예요.

#### 첫 줄

결합벡터 $u=[x^\top,y^\top]^\top$의 편차를 적어요.

#### 검산

u의 편차는B[x−μx,w]ᵀ 꼴이고 B=[[I,0],[A,I]]예요. B diag(Σx,Q)Bᵀ를 블록곱하면 정확한 네 블록이 나와요. 평균은[μx,Aμx+b]ᵀ예요.

#### 조건·구분

$\mathbf x$와 $\mathbf w$의 독립으로 교차항이 $0$이에요. $\mathbf Q$는 $\mathbf y$에만 들어가므로 교차블록에 더하지 않고, 이 결과에 $\mathbf Q$가 대각일 필요는 없어요.

---

<a id="p8"></a>

### P8. 시계열 모델의 다음 상태와 관측

MML Exercise 6.5 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1012_Several_Mathematical_Proofs-%EB%AC%B8%EC%A0%9C.pdf#page=8)

#### 주어진 조건

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

#### 구할 것

$p(\mathbf{x}_{t+1}, \mathbf{y}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t)$를 구해 보세요. 평균 벡터와 공분산 행렬(블록 행렬)을 구하면 돼요.

#### 무엇을 구하는 문제인가요?

시계열 모델의 다음 상태와 관측를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

시계열 예측에서 다음상태와 다음관측은 같은 미래 상태를 공유해 상관돼요. 먼저 $P=A\Sigma_tA^\top+Q$를 계산한 뒤 joint block을 조립해요. 새 잡음은 과거와 상태에 독립이라고 가정해요.

#### 종이에 적을 첫 줄

$\mu_{t+1}=A\mu_t$, $P=A\Sigma_tA^\top+Q$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

모든 기댓값은 $\mathbf{y}_1, \dots, \mathbf{y}_t$가 주어진 조건 아래에서 계산해요. 이 조건 아래 $\mathbf{x}_t$의 평균은 $\boldsymbol{\mu}_t$, 공분산은 $\boldsymbol{\Sigma}_t$예요. 새 잡음 $\mathbf{w}$, $\mathbf{v}$는 $\mathbf{x}_t$와 지난 관측에 독립이고 평균이 $\mathbf{0}$이에요.

$\mathbf{x}_{t+1}$의 평균은 같은 꼴로 따라가요.

$$
\mathbb{E}[\mathbf{x}_{t+1}] = \mathbf{A}\boldsymbol{\mu}_t
$$

편차는 ${\mathbf{x}_{t+1} - \mathbf{A}\boldsymbol{\mu}_t = \mathbf{A}(\mathbf{x}_t - \boldsymbol{\mu}_t) + \mathbf{w}}$예요. $\mathbf{x}_t$와 $\mathbf{w}$는 독립이라 둘이 만나는 항은 0이에요.

$$
\mathbf{P} := \mathrm{Var}[\mathbf{x}_{t+1}] = \mathbf{A}\boldsymbol{\Sigma}_t\mathbf{A}^\top + \mathbf{Q}
$$

즉 ${p(\mathbf{x}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t) = \mathcal{N}(\mathbf{A}\boldsymbol{\mu}_t, \mathbf{P})}$예요.

${\mathbf{y}_{t+1} = \mathbf{C}\mathbf{x}_{t+1} + \mathbf{v}}$의 평균은

$$
\mathbb{E}[\mathbf{y}_{t+1}] = \mathbf{C}\mathbf{A}\boldsymbol{\mu}_t
$$

편차는 ${\mathbf{y}_{t+1} - \mathbf{C}\mathbf{A}\boldsymbol{\mu}_t = \mathbf{C}(\mathbf{x}_{t+1} - \mathbf{A}\boldsymbol{\mu}_t) + \mathbf{v}}$예요. $\mathbf{v}$는 $\mathbf{x}_{t+1}$과 독립이라 교차항이 0이에요.

$$
\mathrm{Var}[\mathbf{y}_{t+1}] = \mathbf{C}\mathbf{P}\mathbf{C}^\top + \mathbf{R}
$$

교차공분산은 정의 $\mathbb{E}[(\mathbf{x}_{t+1} - \mathbf{A}\boldsymbol{\mu}_t)(\mathbf{y}_{t+1} - \mathbf{C}\mathbf{A}\boldsymbol{\mu}_t)^\top]$에 편차를 넣어요. $\mathbf{C}^\top$는 밖으로 나오고 $\mathbf{v}$ 항은 0이에요.

$$
\mathrm{Cov}[\mathbf{x}_{t+1}, \mathbf{y}_{t+1}] = \mathbf{P}\mathbf{C}^\top, \qquad \mathrm{Cov}[\mathbf{y}_{t+1}, \mathbf{x}_{t+1}] = \mathbf{C}\mathbf{P}
$$

$\mathbf{P}$는 대칭이라 ${(\mathbf{P}\mathbf{C}^\top)^\top = \mathbf{C}\mathbf{P}}$예요.

블록으로 모아요. 결합분포가 가우시안이니 이 평균과 공분산으로 정해져요.

$$
p(\mathbf{x}_{t+1}, \mathbf{y}_{t+1} \mid \mathbf{y}_1, \dots, \mathbf{y}_t) = \mathcal{N}\left(\begin{bmatrix}\mathbf{A}\boldsymbol{\mu}_t \\ \mathbf{C}\mathbf{A}\boldsymbol{\mu}_t\end{bmatrix}, \begin{bmatrix}\mathbf{P} & \mathbf{P}\mathbf{C}^\top \\ \mathbf{C}\mathbf{P} & \mathbf{C}\mathbf{P}\mathbf{C}^\top + \mathbf{R}\end{bmatrix}\right)
$$

#### 완성 답과 검산

#### 검산

조건부 평균은[Aμt,CAμt]ᵀ이고 블록공분산은[[P,PCᵀ],[CP,CPCᵀ+R]]예요. 다음상태 잡음과 측정잡음의 독립으로 빠진 교차항이0이에요. 이전 joint 변환의 A를C,Σx를P로 놓아도 같은결과예요.

정답: ${\mathbf{P} := \mathbf{A}\boldsymbol{\Sigma}_t\mathbf{A}^\top + \mathbf{Q}}$일 때 평균 $\begin{bmatrix}\mathbf{A}\boldsymbol{\mu}_t \\ \mathbf{C}\mathbf{A}\boldsymbol{\mu}_t\end{bmatrix}$, 공분산 $\begin{bmatrix}\mathbf{P} & \mathbf{P}\mathbf{C}^\top \\ \mathbf{C}\mathbf{P} & \mathbf{C}\mathbf{P}\mathbf{C}^\top + \mathbf{R}\end{bmatrix}$

#### 여기서 주의해요

현재 관측 y_t와 다음 관측 y_{t+1}를 구별해요. 아직 다음 관측으로 조건화하지 않아요.

#### 설명을 닫고 다시 해요

1. $\mu_{t+1}=A\mu_t$, $P=A\Sigma_tA^\top+Q$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 현재 관측 y_t와 다음 관측 y_{t+1}를 구별해요. 아직 다음 관측으로 조건화하지 않아요.

**페이지 요약**

#### 떠올릴 개념·공식

시계열 예측에서 다음상태와 다음관측은 같은 미래 상태를 공유해 상관돼요. $P=A\Sigma_tA^\top+Q$

#### 첫 줄

$\mu_{t+1}=A\mu_t$, $P=A\Sigma_tA^\top+Q$예요.

#### 검산

조건부 평균은[Aμt,CAμt]ᵀ이고 블록공분산은[[P,PCᵀ],[CP,CPCᵀ+R]]예요. 다음상태 잡음과 측정잡음의 독립으로 빠진 교차항이0이에요. 이전 joint 변환의 A를C,Σx를P로 놓아도 같은결과예요.

#### 조건·구분

모든 평균·공분산은 $\mathbf y_1,\ldots,\mathbf y_t$가 주어진 조건 아래예요. 새 잡음은 과거·상태에 독립이며, 아직 $\mathbf y_{t+1}$로 조건화한 갱신분포가 아니에요.

---

원 문제·정리노트·PDF는 보존해요.
