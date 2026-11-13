# PCA 2부 — 5살도 이해하는 정리노트

정방철 교수님 머신러닝기초 · 1104 수업 (Lecture05–06, MML 10장)

> `정리노트_1104_PCA_Part2.html`를 마크다운으로 옮겼어요. 그림은 `figures_1104/` 폴더의 SVG, 위젯은 대표 설정의 정적 그림으로 바꿨어요. 수식은 `$…$` / `$$…$$`라서 GitHub, Obsidian, Typora에서 보여요.

**목차**

- [PCA의 두 목표](#s0)
  - [어떤 축을 남겨야 복원오차가 작아질까?](#s0-learning-map)
  - [고유기저에서 방향 분산 계산하기](#s0-spectral-weights)
  - [첫 번째부터 M번째까지 방향 고르기](#s0-top-directions)
- [사영과 복원](#s1)
  - [기저를 고정하고 좌표 구하기](#s1-projection)
  - [버린 방향에서 복원오차 계산하기](#s1-discarded)
  - [MNIST에서 사영과 복원 읽기](#s1-mnist)
- [SVD와 실제 계산](#s2)
  - [데이터의 SVD에서 주성분 찾기](#s2-svd)
  - [작은 행렬 두 개로 데이터 복원하기](#s2-low-rank)
  - [PCA를 적용하고 원래 단위로 돌아가기](#s2-workflow)
- [요약 · 예고](#s3)
  - [한 장 요약](#s3-cheatsheet)
  - [다음 시간 예고](#s3-next)
  - [함께 보면 좋은 자료](#s3-links)

<a id="s0"></a>

## PCA의 두 목표

<a id="s0-learning-map"></a>

### 어떤 축을 남겨야 복원오차가 작아질까?

*1104 수업 · L05 s26–28 · L06 s5–17*

**먼저 큰 그림**

표본 하나가 숫자 $D$개로 되어 있을 때, 그보다 적은 $M$개만 저장했다가 다시 $D$개로 펼치고 싶어요. 어떤 축에서 읽은 숫자를 남겨야 다시 펼친 결과가 원래와 가장 가까울까요?

1102에서는 축 하나가 정해졌을 때 그 축에서 읽은 좌표와 좌표의 분산을 구했어요. 1104에서는 축을 고르는 문제를 풀어요. 분산이 가장 큰 축이 무엇인지 증명하고, 그 축을 남기면 복원오차도 가장 작다는 것을 계산으로 확인해요.

| 보는 방향 | 계산하는 것 | 다음에 쓰는 곳 |
|---|---|---|
| 남기는 쪽 | 선택한 축에 담긴 분산 | 분산이 큰 순서로 축을 골라 압축해요. |
| 버리는 쪽 | 빠진 축에 담긴 분산 | 복원 벡터의 평균 제곱오차를 구해요. |

오늘 구하는 것은 네 가지예요. 남길 축을 모은 행렬, 표본마다 줄여 적은 좌표, 그 좌표를 원래 차원으로 펼친 복원 벡터, 그리고 원래 벡터와 복원 벡터의 차이를 제곱해 평균낸 복원오차예요. 평균을 뺀 데이터가 정해지면 남긴 분산과 버린 분산의 합은 변하지 않아요. 그래서 분산을 가장 많이 남기는 축과 오차를 가장 적게 만드는 축이 같아요.

계산은 네 걸음이에요. 먼저 [어느 방향의 분산이든 공분산 행렬의 고윳값들을 섞은 평균](#s0-spectral-weights)임을 보여요. 그러면 [가장 큰 고윳값의 방향부터 고르면](#s0-top-directions) 돼요. 다음으로 [복원오차가 버린 축의 고윳값 합](#s1-discarded)임을 계산해요. 마지막으로 공분산을 만들지 않고 [데이터 행렬을 바로 분해하는 특잇값 분해(SVD)](#s2-svd)로 같은 축을 구해요. 그 축의 분산은 특잇값의 제곱을 표본 수로 나눈 값이에요.

줄여 적은 좌표는 남긴 축의 수인 $M$차원이고, 복원 벡터는 원래 특성 수인 $D$차원이에요. 남기는 마지막 축과 버리는 첫 축의 고윳값이 같다면 최적 축을 여러 방식으로 고를 수 있어요.

**페이지 요약**

평균을 뺀 데이터에서 남긴 분산을 최대로 하면 버린 축의 분산 합인 평균 제곱 복원오차가 최소가 돼요.

줄여 적은 좌표는 남긴 축 수인 $M$차원이고, 복원 벡터는 원래 특성 수인 $D$차원이에요. 남기는 마지막 축과 버리는 첫 축의 고윳값이 같으면 최적 축을 여러 방식으로 고를 수 있어요.

---

<a id="s0-spectral-weights"></a>

### 고유기저에서 방향 분산 계산하기

*1104 수업 · L05 s10 · s19 · s26–27*

**쉽게 말하면**

종이에 찍힌 점들을 자 하나로 읽을 때 자를 기울이면 눈금에 표시되는 점 사이 간격이 달라져요.

![사선으로 늘어선 점과 그 사선에 나란한 자를 나타낸 그림](figures_1104/fig-direction-spread.svg)

*점들이 늘어선 방향에 자를 대면 넓은 범위의 눈금을 써요.*

**정확히 말하면**

이 페이지가 답하는 질문은 하나예요. **자를 어느 방향에 놓아야 눈금이 가장 넓게 퍼질까요?** 답을 먼저 말하면, 어느 방향의 퍼짐이든 공분산 행렬의 고윳값들을 섞은 평균이에요. 그래서 가장 큰 고윳값보다 더 넓게 퍼질 수는 없어요.

그림의 자 방향이 길이 1인 벡터 $\mathbf b\in\mathbb R^D$이고, 자에서 읽은 눈금이 내적 $\mathbf b^\top\mathbf x_n$이에요. $\mathbf x_n\in\mathbb R^D$는 특성별 평균을 이미 뺀 $n$번째 표본이고, 표본은 $N$개, 특성은 $D$개예요.

<a id="s0-weights-variance"></a>

#### 1 / 3 퍼짐을 숫자 하나로 쓰기

방향을 바꿀 때마다 표본 $N$개를 다시 읽지 않아도 되는 식을 만들어요.

자를 $\mathbf b$ 방향에 놓고 $n$번째 점을 읽은 눈금을 $z_n$이라고 해요.

$$
z_n=\mathbf b^\top\mathbf x_n.
$$

표본의 평균이 $\mathbf 0$이라 눈금의 평균도 0이에요. 평균이 0이면 분산은 제곱의 평균이에요. 이 값을 방향 분산 $V(\mathbf b)$라고 해요.

$$
V(\mathbf b)=\frac1N\sum_{n=1}^N(\mathbf b^\top\mathbf x_n)^2.
$$

이 식 그대로는 불편해요. 자를 조금 돌릴 때마다 점 $N$개를 전부 다시 읽어야 하거든요. 그래서 데이터에 관한 계산과 방향에 관한 계산을 떼어 놓아요. 실수 하나는 전치해도 같으므로 제곱의 한쪽을 뒤집어 써요.

$$
(\mathbf b^\top\mathbf x_n)^2=(\mathbf b^\top\mathbf x_n)(\mathbf x_n^\top\mathbf b)=\mathbf b^\top(\mathbf x_n\mathbf x_n^\top)\mathbf b.
$$

양 끝의 $\mathbf b$는 모든 표본에서 같으니 합 밖으로 꺼내요. 가운데에 남는 묶음이 공분산 행렬 $\mathbf S$예요.

$$
V(\mathbf b)=\mathbf b^\top\left[\frac1N\sum_{n=1}^N\mathbf x_n\mathbf x_n^\top\right]\mathbf b=\mathbf b^\top\mathbf S\mathbf b.
$$

데이터는 $\mathbf S$에 한 번만 모아 두고, 방향을 바꿀 때는 $\mathbf b$만 갈아 끼우면 된다는 거예요. $\mathbf S$의 $(i,j)$ 칸은 $x_{in}x_{jn}$의 평균이라 $i$와 $j$를 바꿔도 같아요. 그래서 $\mathbf S$는 대칭이고, 이 사실을 2단계에서 써요.

##### 작은 예로 넣어 보기

특성이 두 개이고 공분산이 아래와 같다고 해요.

$$
\mathbf S=\begin{bmatrix}2&1\\1&2\end{bmatrix}.
$$

가로 방향 $\mathbf b=(1,0)^\top$을 넣으면 $V=2$이고, 대각선 방향 $\mathbf b=(1,1)^\top/\sqrt2$를 넣으면 $V=\frac12(2+1+1+2)=3$이에요. 대각선 쪽이 더 넓게 퍼져요.

자를 길게 늘이면 눈금도 따라 커지므로($V(\alpha\mathbf b)=\alpha^2V(\mathbf b)$), 방향끼리 공정하게 비교하려고 $\|\mathbf b\|=1$인 벡터만 넣어요.

그런데 3이 최댓값일까요? 방향을 하나씩 넣어 보는 방법으로는 알 수 없어요. 모든 방향을 한꺼번에 비교할 수 있는 식이 필요해요.

<a id="s0-weights-coordinates"></a>

#### 2 / 3 방향을 고유벡터로 다시 쓰기

행렬 곱이 숫자 곱으로 바뀌는 축을 골라, 그 축으로 $\mathbf b$를 표현해요.

$\mathbf b^\top\mathbf S\mathbf b$에서 비교를 어렵게 하는 것은 가운데의 행렬 곱이에요. 1102에서 본 고유벡터는 바로 이 곱을 단순하게 만드는 방향이었어요. $\mathbf S\mathbf p_i=\lambda_i\mathbf p_i$이면 $\mathbf p_i$ 방향에서는 $\mathbf S$를 곱하는 일이 숫자 $\lambda_i$를 곱하는 일과 같아요.

위의 예에서 확인해 볼게요.

$$
\mathbf S\begin{bmatrix}1\\1\end{bmatrix}=\begin{bmatrix}3\\3\end{bmatrix}=3\begin{bmatrix}1\\1\end{bmatrix},\qquad \mathbf S\begin{bmatrix}1\\-1\end{bmatrix}=\begin{bmatrix}1\\-1\end{bmatrix}=1\begin{bmatrix}1\\-1\end{bmatrix}.
$$

길이를 1로 맞추면 $\mathbf p_1=(1,1)^\top/\sqrt2$, $\mathbf p_2=(1,-1)^\top/\sqrt2$이고 고윳값은 $\lambda_1=3$, $\lambda_2=1$이에요.

원래 쓰던 가로·세로 축으로 $\mathbf b$를 쓰면 안 될까요? 표현은 되지만 도움이 안 돼요. $\mathbf S(1,0)^\top=(2,1)^\top$은 $(1,0)^\top$의 숫자배가 아니라서 행렬 곱이 그대로 남아요. 아무 축이나 고를 수 있는 것과, 이번 목적에 쓸모 있는 축을 고르는 것은 달라요.

고유벡터들은 서로 수직일까요? 일반 행렬에서는 보장이 없어요. 여기서는 $\mathbf S$가 실수 대칭행렬이라 서로 수직이고 길이가 1인 고유벡터 $\mathbf p_1,\ldots,\mathbf p_D$를 고를 수 있어요. 예의 두 벡터도 내적이 $\frac12(1-1)=0$이에요. 고윳값은 큰 순서로 $\lambda_1\ge\cdots\ge\lambda_D\ge0$이라고 번호를 붙여요. $\mathbf p_i$ 방향의 분산이 $\mathbf p_i^\top\mathbf S\mathbf p_i=\lambda_i$이고 분산은 음수가 될 수 없어서 고윳값은 모두 0 이상이에요.

$$
\mathbf p_i^\top\mathbf p_i=1,\qquad \mathbf p_i^\top\mathbf p_j=0\quad(i\ne j).
$$

이제 $\mathbf b$를 이 축들의 가중합으로 써요. $c_i$는 $\mathbf b$가 $\mathbf p_i$ 쪽으로 얼마나 향하는지를 나타내는 숫자예요.

$$
\mathbf b=\sum_{i=1}^D c_i\mathbf p_i.
$$

$c_i$는 내적으로 읽어요. 양변에 $\mathbf p_i^\top$를 곱하면 수직인 축의 항은 0이 되고 $c_i$만 남기 때문이에요.

$$
c_i=\mathbf p_i^\top\mathbf b.
$$

같은 이유로 $\mathbf b$를 자기 자신과 내적하면 서로 다른 축의 항이 사라져 $\|\mathbf b\|^2=\sum_i c_i^2$이에요. $\mathbf b$의 길이가 1이므로 제곱한 가중치의 합은 1이에요.

$$
\sum_{i=1}^D c_i^2=1.
$$

예에서 가로 방향 $\mathbf b=(1,0)^\top$은 $c_1=c_2=1/\sqrt2$이고, 제곱의 합은 $\frac12+\frac12=1$이에요.

##### 행렬로 모아 쓰면

고유벡터를 열로 모은 행렬이 $\mathbf P=[\mathbf p_1,\ldots,\mathbf p_D]$이고, 같은 순서로 고윳값을 대각에 놓은 행렬이 $\boldsymbol\Lambda$예요. $\mathbf S\mathbf p_i=\lambda_i\mathbf p_i$를 열마다 모으면 $\mathbf S\mathbf P=\mathbf P\boldsymbol\Lambda$예요. $\mathbf P^\top\mathbf P$의 $(i,j)$ 칸이 $\mathbf p_i^\top\mathbf p_j$라서 대각선은 1, 나머지는 0이에요. 곧 $\mathbf P^\top\mathbf P=\mathbf I_D$이고, $\mathbf P$가 정방행렬이라 $\mathbf P^{-1}=\mathbf P^\top$예요. 오른쪽에 $\mathbf P^\top$를 곱하면 문제에서 자주 쓰는 모양이 나와요.

$$
\mathbf S=\mathbf P\boldsymbol\Lambda\mathbf P^\top.
$$

<a id="s0-weights-average"></a>

#### 3 / 3 분산이 가중평균이 되는 이유

$\mathbf b$의 전개를 분산식에 넣고, 사라지는 항과 남는 항을 확인해요.

축이 두 개인 경우부터 직접 써 볼게요. $\mathbf b=c_1\mathbf p_1+c_2\mathbf p_2$를 $V(\mathbf b)=\mathbf b^\top\mathbf S\mathbf b$의 양쪽에 넣어요.

$$
V(\mathbf b)=(c_1\mathbf p_1^\top+c_2\mathbf p_2^\top)\,\mathbf S\,(c_1\mathbf p_1+c_2\mathbf p_2).
$$

먼저 오른쪽 괄호에 $\mathbf S$를 곱해요. 고유벡터라서 행렬 곱이 숫자 곱으로 바뀌어요. 2단계에서 축을 고른 이유가 여기서 쓰여요.

$$
\mathbf S(c_1\mathbf p_1+c_2\mathbf p_2)=\lambda_1c_1\mathbf p_1+\lambda_2c_2\mathbf p_2.
$$

이제 왼쪽 괄호와 곱하면 네 항이 생겨요.

$$
V(\mathbf b)=\lambda_1c_1^2\,\mathbf p_1^\top\mathbf p_1+\lambda_2c_1c_2\,\mathbf p_1^\top\mathbf p_2+\lambda_1c_2c_1\,\mathbf p_2^\top\mathbf p_1+\lambda_2c_2^2\,\mathbf p_2^\top\mathbf p_2.
$$

가운데 두 항은 서로 다른 축의 내적이라 0이고, 양 끝의 내적은 1이에요.

$$
V(\mathbf b)=\lambda_1c_1^2+\lambda_2c_2^2.
$$

축이 $D$개여도 같은 일이 일어나요. $D\times D$개 항 중 번호가 같은 $D$개만 남아요.

$$
V(\mathbf b)=\sum_{i=1}^D\lambda_i c_i^2,\qquad \sum_{i=1}^D c_i^2=1.
$$

$c_i^2$은 음수가 아니고 합이 1이니, 방향 분산은 고윳값들을 $c_i^2$의 비율로 섞은 가중평균이에요. 예의 가로 방향에서는 $3\cdot\frac12+1\cdot\frac12=2$로, 1단계에서 직접 넣어 구한 값과 같아요.

평균은 섞은 값들 중 가장 큰 것을 넘지 못해요. 그래서 1단계에서 남긴 질문의 답이 나와요. 예에서 3보다 넓게 퍼지는 방향은 없어요. 이 내용을 일반적으로 쓰는 일은 [첫 번째부터 M번째까지 방향 고르기](#s0-top-directions)에서 해요.

##### 다시 만들 때 필요한 것

기억할 출발점은 세 가지예요. 방향 분산은 $\mathbf b^\top\mathbf S\mathbf b$이고, 고유벡터에서는 $\mathbf S\mathbf p_i=\lambda_i\mathbf p_i$이고, 대칭행렬의 고유벡터는 서로 수직이고 길이 1로 고를 수 있어요. $\mathbf b$를 고유벡터의 가중합으로 써서 넣으면 나머지 식은 위 순서대로 다시 나와요.

**교수님 말씀**

> “이게 또 대표적인 하나마나 한 짓이지.”

같은 벡터를 고유기저로 다시 쓰면, 고유벡터에 행렬을 곱하는 계산이 스칼라를 곱하는 계산으로 바뀌어요. 공분산의 두 비대각 원소가 같은 모습은 대각선을 접어 마주 찍은 데칼코마니에 비유했어요.

> “헷갈리면 손으로 디립다 써봐라.”

내적의 항을 직접 써 보면 어떤 교차항이 0인지 확인할 수 있어요.

**페이지 요약**

방향 분산은, 축을 고유벡터로 다시 쓰면 고윳값의 가중평균이에요.

*핵심 식*

- 방향 분산

  $$
  V(\mathbf b)=\mathbf b^\top\mathbf S\mathbf b,\quad \mathbf S=\frac1N\sum_n\mathbf x_n\mathbf x_n^\top
  $$
- 고유기저로 분해

  $$
  \mathbf S=\mathbf P\boldsymbol\Lambda\mathbf P^\top
  $$
- 고윳값의 가중평균

  $$
  V(\mathbf b)=\sum_{i=1}^D\lambda_i c_i^2,\quad c_i=\mathbf p_i^\top\mathbf b
  $$

  제곱 가중치의 합은 $\sum_i c_i^2=1$이에요.

$\mathbf S$가 실수 대칭행렬이라 고유벡터를 서로 수직, 길이 1로 고를 수 있어요. 방향끼리 비교하려고 $\|\mathbf b\|=1$로 맞춰요.

*예*

$\mathbf S=\begin{bmatrix}2&1\\1&2\end{bmatrix}$에서 $\lambda_1=3$, $\lambda_2=1$이에요. 가로 방향의 분산은 $3\cdot\frac12+1\cdot\frac12=2$예요.

---

<a id="s0-top-directions"></a>

### 첫 번째부터 M번째까지 방향 고르기

*1104 수업 · L05 s27–28*

**쉽게 말하면**

첫 번째 자는 점들이 가장 길게 늘어선 방향에 놓아요. 두 번째 자는 첫 번째 자와 모서리가 맞는 방향에 놓아요.

![서로 직각으로 만나는 두 자와 긴 자를 따라 퍼진 점들](figures_1104/fig-orthogonal-rulers.svg)

*두 자는 직각으로 만나요.*

**정확히 말하면**

이 페이지의 질문은 **어느 축들을 남겨야 분산을 가장 많이 담을까요?**예요. 답을 먼저 말하면, 공분산 $\mathbf S$의 고윳값이 큰 순서대로 고유벡터 $M$개를 남기면 돼요.

출발점은 [고유기저에서 방향 분산 계산하기](#s0-spectral-weights)의 결과예요. 길이 1인 방향 $\mathbf b$를 고유벡터 $\mathbf p_i$의 가중합 $\mathbf b=\sum_i c_i\mathbf p_i$로 쓰면 분산은 고윳값의 가중평균이었어요. 고윳값은 큰 순서로 $\lambda_1\ge\cdots\ge\lambda_D\ge0$이에요.

$$
V(\mathbf b)=\sum_{i=1}^D\lambda_i c_i^2,\qquad \sum_{i=1}^D c_i^2=1.
$$

<a id="s0-directions-first"></a>

#### 1 / 2 첫 방향의 최댓값 찾기

분산이 넘을 수 없는 값을 구하고, 그 값을 실제로 만드는 방향을 찾아요.

방향을 고른다는 것은 무게 $c_i^2$를 어느 고윳값에 얼마나 실을지 정하는 일이에요. 무게의 합이 1로 묶여 있으니, 가장 큰 고윳값에 전부 실을 때 평균이 가장 커요. 고윳값이 3과 1인 예에서는 $3c_1^2+1c_2^2$이고, $c_1^2=1$일 때 가장 큰 값 3이 나와요.

1. **넘을 수 없는 값을 정해요.** 모든 $\lambda_i$가 $\lambda_1$ 이하이고 $c_i^2$은 음수가 아니에요. 각 항의 $\lambda_i$를 $\lambda_1$로 바꾸면 합은 줄지 않아요.

   $$
   V(\mathbf b)=\sum_{i=1}^D\lambda_i c_i^2\le\lambda_1\sum_{i=1}^D c_i^2=\lambda_1.
   $$
2. **그 값을 만드는 방향을 찾아요.** $\mathbf b_1=\mathbf p_1$로 고르면 $c_1=1$이고 나머지 $c_i$는 0이라 $V(\mathbf b_1)=\lambda_1$이에요. 어떤 방향도 넘지 못하는 값을 실제로 만들었으니 이 값이 최댓값이에요.

$\mathbf p_1$과 $-\mathbf p_1$은 같은 축을 가리키므로 어느 쪽을 써도 돼요. 가장 큰 고윳값이 여러 개로 같다면, 그 고윳값을 갖는 고유벡터들이 만드는 공간의 단위벡터 중 무엇을 골라도 같은 최댓값이에요.

<a id="s0-directions-remaining"></a>

#### 2 / 2 직교하는 다음 방향 고르기

이미 고른 축과 수직이라는 조건을 넣고, 남은 방향의 최댓값을 구해요.

둘째 축도 분산이 가장 큰 방향으로 고르면 될까요? 그러면 다시 $\mathbf p_1$이 나와요. 같은 정보를 두 번 적게 되는 거예요. 새 축에는 아직 담지 않은 정보를 담아야 하므로, PCA는 이미 고른 축과 수직인 단위벡터 중에서 다음 축을 찾아요.

수직 조건을 가중치로 옮겨 볼게요. $\mathbf b$가 $\mathbf p_1$과 수직이면 $\mathbf p_1^\top\mathbf b=0$인데, 이 내적이 바로 $c_1$이에요. 곧 수직 조건은 $c_1=0$이에요. 첫 고윳값에는 무게를 실을 수 없으니, 남은 고윳값 중 가장 큰 $\lambda_2$에 전부 싣는 $\mathbf b_2=\mathbf p_2$가 답이에요.

같은 계산을 $k$번째 축에 적용해요. $\mathbf p_1,\ldots,\mathbf p_{k-1}$을 이미 골랐다면 $c_1=\cdots=c_{k-1}=0$이고, 합은 $k$번째 항부터 시작해요.

$$
V(\mathbf b)=\sum_{i=k}^D\lambda_i c_i^2\le\lambda_k\sum_{i=k}^D c_i^2=\lambda_k.
$$

$\mathbf b_k=\mathbf p_k$가 이 값을 만들어요.

이렇게 고른 첫 $M$개 축을 열로 모은 행렬이 $\mathbf B=[\mathbf p_1,\ldots,\mathbf p_M]\in\mathbb R^{D\times M}$이에요. 축마다 담긴 분산을 더한 보존 분산은 $\sum_{i=1}^M\lambda_i$예요. 고윳값이 3과 1인 예에서 축 하나를 남기면 전체 분산 4 중 3을 담아요.

$M\lt D$이고 $\lambda_M=\lambda_{M+1}$이면 같은 고윳값의 공간에서 다른 축을 골라도 보존 분산은 같아요. 다음 [기저를 고정하고 좌표 구하기](#s1-projection)에서는 이 $\mathbf B$로 좌표를 구하고 복원해요.

<a id="s0-directions-joint"></a>

#### 여러 축을 함께 고를 때의 결론

위에서는 축을 하나씩 차례로 골랐어요. $M$개를 한꺼번에 고르는 경우에도 상위 $M$개 고유방향을 남길 때 보존 분산 $\sum_{i=1}^M\lambda_i$가 최대예요. 문제를 풀 때는 이 결론만 쓰면 되고, 증명은 선택 보충이에요.

<details><summary>선택 보충: 여러 축을 함께 비교하는 증명</summary>

강의에서 보인 순차 선택을 바탕으로, 여기서는 여러 축을 한꺼번에 비교할 때도 같은 선택이 최적인 이유를 덧붙여요. 임의의 정규직교 단위축 $\mathbf q_1,\ldots,\mathbf q_M\in\mathbb R^D$를 열로 모은 행렬을 $\mathbf C=[\mathbf q_1,\ldots,\mathbf q_M]\in\mathbb R^{D\times M}$이라 해요. 앞의 숫자 계수 $c_i$와 구별하려고 축 벡터에는 $\mathbf q_m$을 써요.

$\mathbf C^\top\mathbf p_i$의 $m$번째 값은 $\mathbf q_m^\top\mathbf p_i$예요. 따라서 $i$번째 고유방향을 선택한 부분공간에 얼마나 담는지 나타내는 가중치는 다음과 같아요.

$$
w_i=\|\mathbf C^\top\mathbf p_i\|^2=\sum_{m=1}^M(\mathbf q_m^\top\mathbf p_i)^2.
$$

1. **가중치의 범위와 합을 구해요.** 선택한 축을 전체 정규직교 기저로 보태면, 단위벡터 $\mathbf p_i$의 전체 좌표 제곱합은 1이에요. $w_i$는 그중 $M$개만 더하므로 $0\le w_i\le1$이에요. 반대로 $m$을 고정하면, $\mathbf p_i^\top\mathbf q_m$은 단위축 $\mathbf q_m$의 전체 고유기저 좌표예요.

   $$
   \sum_{i=1}^D(\mathbf p_i^\top\mathbf q_m)^2=\|\mathbf q_m\|^2=1.
   $$

   내적은 실수라 $\mathbf q_m^\top\mathbf p_i=\mathbf p_i^\top\mathbf q_m$예요. 유한한 두 합의 순서를 바꾸면 다음과 같아요.

   $$
   \sum_{i=1}^D w_i=\sum_{m=1}^M\sum_{i=1}^D(\mathbf p_i^\top\mathbf q_m)^2=\sum_{m=1}^M1=M.
   $$
2. **축별 분산을 더해요.** 앞의 방향 분산식에서 $\mathbf b=\mathbf q_m$, $c_i=\mathbf p_i^\top\mathbf q_m$을 대입해요.

   $$
   V(\mathbf q_m)=\sum_{i=1}^D\lambda_i(\mathbf p_i^\top\mathbf q_m)^2.
   $$

   모든 선택 축에 대해 더하고 합의 순서를 바꾸면 괄호 안이 $w_i$예요.

   $$
   \sum_{m=1}^M V(\mathbf q_m)=\sum_{i=1}^D\lambda_i\left[\sum_{m=1}^M(\mathbf p_i^\top\mathbf q_m)^2\right]=\sum_{i=1}^D\lambda_i w_i.
   $$
3. **상위 고유축 선택과 비교해요.** $\sum_iw_i=M$을 앞뒤로 나누어 옮기면, 앞쪽에서 비운 가중치와 뒤쪽에 둔 가중치가 같아요.

   $$
   \sum_{i=1}^M(1-w_i)=M-\sum_{i=1}^M w_i=\sum_{i=M+1}^D w_i.
   $$

   상위 $M$축을 모두 담을 때의 분산에서 임의 선택의 분산을 빼요. 앞쪽에서는 $\lambda_i\ge\lambda_M$, 뒤쪽에서는 $\lambda_i\le\lambda_M$이고 각 가중치는 음수가 아니에요.

   $$
   \begin{aligned}\sum_{i=1}^M\lambda_i-\sum_{i=1}^D\lambda_iw_i&=\sum_{i=1}^M\lambda_i(1-w_i)-\sum_{i=M+1}^D\lambda_iw_i\\&\ge\lambda_M\left[\sum_{i=1}^M(1-w_i)-\sum_{i=M+1}^D w_i\right]\\&=0.\end{aligned}
   $$

따라서 앞 $M$개의 고유방향에 가중치를 1씩 두는 선택이 전체 보존 분산도 최대로 만들어요. $M=D$라면 뒤쪽 합은 빈 합인 0이고 모든 방향을 보존해요.

</details>

**교수님 말씀**

> “그러면 b를 어떻게 선택하면 λ1이 만들어질까? 그게 optimal이잖아.”

모든 후보가 넘을 수 없는 값부터 찾고, 실제로 그 값을 만드는 후보를 대입해요.

**페이지 요약**

고른 축과 직교하는 후보만 남기면, 아직 고르지 않은 고윳값 중 가장 큰 값이 다음 방향의 분산 상한이에요.

*핵심 식*

- 남은 후보의 상한

  $$
  V(\mathbf b)=\sum_{i=k}^D\lambda_i c_i^2\le\lambda_k
  $$
- 상한에 도달하는 방향

  $$
  \mathbf b_k=\mathbf p_k
  $$
- 최대 전체 보존 분산

  $$
  \sum_{i=1}^M\lambda_i
  $$

다음 축은 이미 고른 축과 직교하는 단위축 중에서 골라, 같은 방향을 중복 선택하지 않아요.

*용어*

- **직교 제약** — 이미 고른 축의 좌표를 0으로 두는 조건이에요.
- **고윳값 중복** — 선택 경계의 고윳값이 같으면 같은 최댓값을 내는 축 조합이 여러 개예요.

---

<a id="s1"></a>

## 사영과 복원

<a id="s1-projection"></a>

### 기저를 고정하고 좌표 구하기

*1104 수업 · L06 s5–7*

**쉽게 말하면**

길 위에서 길 밖의 점과 가장 가까운 곳을 찾고 싶어요.

![길 밖의 점에서 길에 수직선을 내려 가장 가까운 곳을 찾은 그림](figures_1104/fig-projection-foot.svg)

*길에 직각으로 내려가면 가장 가까운 곳에 닿아요.*

**정확히 말하면**

이 페이지의 질문은 **남길 축이 정해졌을 때, 표본마다 어떤 숫자 $M$개를 적어야 가장 가깝게 복원될까요?**예요. 답을 먼저 말하면, 축들이 서로 수직이고 길이가 1일 때는 표본과 각 축의 내적을 적으면 돼요.

$$
\mathbf z_n=\mathbf B^\top\mathbf x_n,\qquad \tilde{\mathbf x}_n=\mathbf B\mathbf z_n=\mathbf B\mathbf B^\top\mathbf x_n.
$$

그림의 길이 남긴 축들이 만드는 공간이고, 길 밖의 점이 표본 $\mathbf x_n$, 가장 가까운 곳이 복원값 $\tilde{\mathbf x}_n$이에요. 내적이 왜 가장 가까운 점을 주는지는 오차를 최소화해서 확인해요.

<a id="s1-projection-objective"></a>

#### 1 / 4 복원오차와 변수 정하기

정해진 것과 구할 것을 구별하고, 줄이려는 오차를 식으로 써요.

세 가지를 구별해요. 평균을 뺀 표본 $\mathbf x_n\in\mathbb R^D$는 주어진 데이터예요. 축 벡터 $\mathbf b_1,\ldots,\mathbf b_M\in\mathbb R^D$를 열로 모은 $\mathbf B\in\mathbb R^{D\times M}$은 모든 표본이 함께 쓰는 고정된 행렬이에요. 좌표 $\mathbf z_n\in\mathbb R^M$이 표본마다 새로 구할 미지수예요.

복원값은 좌표의 성분을 가중치로 삼아 축 벡터를 더한 $D$차원 벡터예요.

$$
\tilde{\mathbf x}_n=\mathbf B\mathbf z_n=z_{1n}\mathbf b_1+\cdots+z_{Mn}\mathbf b_M.
$$

원래 표본과 복원값의 거리 제곱을 모든 표본에서 평균낸 값이 복원오차 $J_M$이에요.

$$
J_M=\frac1N\sum_{n=1}^N\|\mathbf x_n-\tilde{\mathbf x}_n\|^2.
$$

$\mathbf z_n$은 합의 $n$번째 항에만 들어 있어요. 그래서 $\mathbf B$를 고정하면 표본 하나의 오차를 줄이는 문제를 $N$번 따로 푸는 것과 같아요.

<a id="s1-projection-derivative"></a>

#### 2 / 4 좌표로 미분하기

오차가 가장 작은 좌표에서는 미분이 0이라는 조건을 쓰려고, 좌표에 대한 미분을 구해요.

$J_M$은 복원값 $\tilde{\mathbf x}_n$을 거쳐 $\mathbf z_n$에 의존하므로 연쇄법칙으로 두 미분을 곱해요. 강의 슬라이드는 성분별로 썼고, 여기서는 같은 계산을 행벡터로 묶어요.

먼저 오차를 복원값으로 미분해요. 숫자에서 $(x-a)^2$을 $a$로 미분하면 $-2(x-a)$인 것과 같은 모양이고, 벡터에서는 $1\times D$ 행벡터가 돼요.

$$
\frac{\partial J_M}{\partial\tilde{\mathbf x}_n}=-\frac2N(\mathbf x_n-\tilde{\mathbf x}_n)^\top.
$$

다음으로 복원값 $\tilde{\mathbf x}_n=\mathbf B\mathbf z_n$을 좌표로 미분하면 $D\times M$ 행렬 $\mathbf B$예요. 두 미분을 곱하면 좌표에 대한 $1\times M$ 행벡터를 얻어요.

$$
\frac{\partial J_M}{\partial\mathbf z_n}=-\frac2N(\mathbf x_n-\tilde{\mathbf x}_n)^\top\mathbf B.
$$

이 식에서 마지막 행렬 대신 그 $i$번째 열 $\mathbf b_i$만 곱하면 슬라이드의 $i$번째 성분을 얻어요.

<a id="s1-projection-coordinates"></a>

#### 3 / 4 정규방정식에서 좌표 구하기

미분을 0으로 놓은 식을 좌표에 대해 풀어요.

1. 미분을 $1\times M$ 영행벡터로 놓아요. 양변을 $-2/N$으로 나누고 복원값 $\tilde{\mathbf x}_n=\mathbf B\mathbf z_n$을 대입해요.

   $$
   (\mathbf x_n-\mathbf B\mathbf z_n)^\top\mathbf B=\mathbf 0_{1\times M}.
   $$

   전치를 분배해요. 곱의 전치에서는 $\mathbf B$와 $\mathbf z_n$의 순서를 바꿔요.

   $$
   \mathbf x_n^\top\mathbf B-\mathbf z_n^\top\mathbf B^\top\mathbf B=\mathbf 0_{1\times M}.
   $$

   두 번째 항을 옮겨 정리해요.

   $$
   \mathbf z_n^\top\mathbf B^\top\mathbf B=\mathbf x_n^\top\mathbf B.
   $$

   구하려는 $\mathbf z_n$이 행벡터로 누워 있으니 양변을 전치해 열벡터로 세워요. 이 식이 정규방정식(normal equations)이에요.

   $$
   \mathbf B^\top\mathbf B\mathbf z_n=\mathbf B^\top\mathbf x_n.
   $$
2. $\mathbf z_n$ 앞의 $\mathbf B^\top\mathbf B$를 없애야 해요. $\mathbf B$의 열이 선형독립이면 $\mathbf B^\top\mathbf B$가 가역이라 양변 왼쪽에 역행렬을 곱할 수 있어요. $\mathbf B^\dagger=(\mathbf B^\top\mathbf B)^{-1}\mathbf B^\top$를 $\mathbf B$의 유사역행렬(pseudoinverse)이라 불러요.

   $$
   \mathbf z_n=(\mathbf B^\top\mathbf B)^{-1}\mathbf B^\top\mathbf x_n.
   $$
3. PCA의 축은 서로 수직이고 길이가 1이에요. $(\mathbf B^\top\mathbf B)_{ij}=\mathbf b_i^\top\mathbf b_j$이므로 대각선은 길이의 제곱 1, 나머지는 수직인 축의 내적 0이에요. 곧 $\mathbf B^\top\mathbf B=\mathbf I_M$이고 역행렬 항이 사라져요.

   $$
   \mathbf z_n=\mathbf B^\top\mathbf x_n,\qquad z_{in}=\mathbf b_i^\top\mathbf x_n.
   $$

좌표를 구할 때 내적만 하면 되는 것은 축이 직교 정규일 때예요. 축이 서로 수직이 아니면 한 축과의 내적에 다른 축의 성분이 섞여 들어가므로 $(\mathbf B^\top\mathbf B)^{-1}$로 바로잡아야 해요.

<a id="s1-projection-residual"></a>

#### 4 / 4 복원과 잔차 확인하기

구한 좌표로 복원하고, 남은 차이가 모든 축에 수직인지 확인해요.

구한 좌표를 복원식에 대입하면 $\tilde{\mathbf x}_n=\mathbf B\mathbf B^\top\mathbf x_n$이에요. 원래 표본에서 복원값을 뺀 벡터를 잔차라고 해요. 정규방정식의 항을 한쪽으로 모으면 잔차와 모든 축의 내적이 0이라는 식이 돼요.

$$
\mathbf B^\top(\mathbf x_n-\tilde{\mathbf x}_n)=\mathbf 0.
$$

그림에서 길에 직각으로 내려간 선이 이 잔차예요. 잔차가 남긴 공간과 수직이므로 이 복원을 직교사영(orthogonal projection)이라 불러요.

평면의 점 $(6,8)$에서 가로축 하나만 남겨 볼게요. $\mathbf B=(1,0)^\top$이면 좌표는 내적 $6$이고, 복원값은 $(6,0)$, 잔차는 $(0,8)$이에요. 잔차와 가로축의 내적은 0이에요.

$\mathbf B^\top\mathbf B$와 $\mathbf B\mathbf B^\top$는 다른 행렬이에요. $\mathbf B^\top\mathbf B=\mathbf I_M$은 좌표로 조립했다가 다시 읽으면 같은 좌표가 나온다는 뜻이에요. 반대 순서인 $\mathbf B\mathbf B^\top$는 $D\times D$ 행렬이고, 벡터를 남긴 공간으로 보내는 사영행렬이에요. $M\lt D$이면 $\mathbf I_D$와 달라요. 위 예에서도 $(6,8)$이 $(6,0)$으로 바뀌었어요. 표본이 처음부터 남긴 공간 안에 있을 때만 복원값이 원래 벡터와 같아요.

단위벡터 내적에서 기저 행렬 B의 층별 내적 z = Bᵀx와 평면 사영 복원 x̃ = Bz로 확장되는 과정을 [내적에서 행렬 사영으로 실험](../%EC%9D%B8%ED%84%B0%EB%A0%89%ED%8B%B0%EB%B8%8C_01_%EB%82%B4%EC%A0%81%EC%97%90%EC%84%9C_%ED%96%89%EB%A0%AC_%EC%82%AC%EC%98%81%EC%9C%BC%EB%A1%9C.html)에서 직접 비교해 보세요.

**교수님 말씀**

이전 최소제곱 풀이를 떠올리고, 평면의 점 $(6,8)$을 예로 들어 좌표의 뜻을 짚었어요. 가로 단위벡터와 내적하면 $6$, 세로 단위벡터와 내적하면 $8$이 나와요. 새 축에서도 같은 방식으로 좌표를 읽어요.

**페이지 요약**

직교 정규 축을 고정하면 각 축과의 내적으로 좌표를 구하고, 그 좌표로 축을 가중합해 가장 가까운 점을 복원해요.

*핵심 식*

- 선형독립인 일반 기저에서 좌표

  $$
  \mathbf z_n=(\mathbf B^\top\mathbf B)^{-1}\mathbf B^\top\mathbf x_n.
  $$
- 직교 정규 기저에서 좌표

  $$
  \mathbf z_n=\mathbf B^\top\mathbf x_n,\qquad z_{in}=\mathbf b_i^\top\mathbf x_n.
  $$
- 직교 정규 기저에서 복원

  $$
  \tilde{\mathbf x}_n=\mathbf B\mathbf B^\top\mathbf x_n
  $$

직교 정규 열들의 내적은 $\mathbf B^\top\mathbf B=\mathbf I_M$을 만들어요. $M\lt D$일 때 반대 순서인 $\mathbf B\mathbf B^\top$는 사영행렬이며, 일반적인 역변환이 아니에요.

*용어*

- **직교사영(orthogonal projection)** — 잔차가 부분공간의 모든 축과 수직이 되는 가장 가까운 점을 찾는 연산.

---

<a id="s1-discarded"></a>

### 버린 방향에서 복원오차 계산하기

*1104 수업 · L06 s8–10*

**쉽게 말하면**

가로로 얼마나 갔는지만 적어 두면, 원래 자리의 높이는 잃어버려요.

![남긴 거리를 가로선으로, 기록에서 빠진 높이를 세로선으로 나타낸 그림](figures_1104/fig-discarded-height.svg)

*가로로 간 거리는 그대로라서, 원래 자리와의 차이는 높이만큼이에요.*

**정확히 말하면**

이 페이지의 질문은 두 가지예요. **복원하면 얼마나 틀릴까요? 그리고 어떤 축을 남겨야 가장 덜 틀릴까요?** 답을 먼저 말하면, 복원오차는 버린 축들에 담긴 분산의 합이에요. 그래서 분산이 큰 축을 남기고 작은 축을 버리면 오차가 가장 작아요.

출발점은 [기저를 고정하고 좌표 구하기](#s1-projection)의 복원식 $\tilde{\mathbf x}_n=\mathbf B\mathbf B^\top\mathbf x_n$이에요. 1단계부터 3단계까지는 서로 수직이고 길이 1인 축이면 무엇이든 성립하고, 4단계에서 고유벡터를 골라 넣어요.

<a id="s1-discarded-residual"></a>

#### 1 / 4 버린 축으로 잔차 쓰기

원래 표본에서 복원값을 빼면 무엇이 남는지 확인해요.

남긴 축 $\mathbf b_1,\ldots,\mathbf b_M$만으로는 $D$차원 벡터를 다 표현할 수 없어요. 그래서 이 축들과 수직인 축 $\mathbf b_{M+1},\ldots,\mathbf b_D$를 $D-M$개 보태 전체 직교 정규 기저를 만들어요. 보탠 축이 버리는 축이고, 이 축들이 만드는 공간을 직교여공간(orthogonal complement)이라 해요.

전체 기저가 있으면 표본을 축마다의 내적 좌표로 남김없이 쓸 수 있어요. 남긴 축의 합과 버린 축의 합으로 나누어 써요.

$$
\mathbf x_n=\sum_{m=1}^M(\mathbf b_m^\top\mathbf x_n)\mathbf b_m+\sum_{j=M+1}^D(\mathbf b_j^\top\mathbf x_n)\mathbf b_j.
$$

첫 합은 복원값 $\tilde{\mathbf x}_n=\mathbf B\mathbf B^\top\mathbf x_n$을 축별로 풀어 쓴 것과 같아요. 그래서 원래 표본에서 복원값을 빼면 두 번째 합만 남아요.

$$
\mathbf x_n-\tilde{\mathbf x}_n=\sum_{j=M+1}^D(\mathbf b_j^\top\mathbf x_n)\mathbf b_j.
$$

틀린 부분은 버린 축 방향의 성분이라는 거예요. 점 $(6,8)$에서 가로축만 남기면 남긴 성분이 6, 버린 성분이 8이에요.

<a id="s1-discarded-squares"></a>

#### 2 / 4 제곱오차 전개하기

잔차의 길이 제곱을 버린 좌표의 제곱합으로 바꿔요.

식을 짧게 쓰려고 잔차를 $\mathbf r_n=\mathbf x_n-\tilde{\mathbf x}_n$, 버린 축의 좌표를 $a_{jn}=\mathbf b_j^\top\mathbf x_n$이라 잠시 이름 붙여요. 그러면 $\mathbf r_n=\sum_{j=M+1}^D a_{jn}\mathbf b_j$예요. 벡터의 길이 제곱은 자기 자신과의 내적이에요.

$$
\|\mathbf r_n\|^2=\mathbf r_n^\top\mathbf r_n=\left(\sum_{i=M+1}^D a_{in}\mathbf b_i^\top\right)\left(\sum_{j=M+1}^D a_{jn}\mathbf b_j\right).
$$

두 합을 곱해 펼치면 축 번호의 모든 조합이 나와요.

$$
\|\mathbf r_n\|^2=\sum_{i=M+1}^D\sum_{j=M+1}^D a_{in}a_{jn}(\mathbf b_i^\top\mathbf b_j).
$$

[고유기저에서 방향 분산 계산하기](#s0-spectral-weights)의 3단계와 같은 일이 일어나요. 서로 다른 축의 내적은 0이라 번호가 다른 항이 사라지고, 같은 축의 내적은 1이에요.

$$
\|\mathbf r_n\|^2=\sum_{j=M+1}^D a_{jn}^2=\sum_{j=M+1}^D(\mathbf b_j^\top\mathbf x_n)^2.
$$

점 $(6,8)$의 예에서는 버린 좌표가 8 하나라 오차의 제곱이 64예요. 이 값을 표본 $N$개에서 평균내면 복원오차 $J_M$이에요.

$$
J_M=\frac1N\sum_{n=1}^N\sum_{j=M+1}^D(\mathbf b_j^\top\mathbf x_n)^2.
$$

<a id="s1-discarded-variance"></a>

#### 3 / 4 방향별 분산으로 바꾸기

복원오차를 버린 축의 분산으로 읽고, 남긴 분산과의 관계를 구해요.

합의 순서를 바꿔 축 하나씩 보면, 안쪽은 그 축에서 읽은 좌표 제곱의 평균이에요. 이것은 [방향 분산](#s0-spectral-weights) $V(\mathbf b_j)=\mathbf b_j^\top\mathbf S\mathbf b_j$와 같은 식이에요.

$$
\frac1N\sum_{n=1}^N(\mathbf b_j^\top\mathbf x_n)^2=\mathbf b_j^\top\mathbf S\mathbf b_j.
$$

따라서 복원오차는 버린 축마다의 분산을 더한 값이에요.

$$
J_M=\sum_{j=M+1}^D\mathbf b_j^\top\mathbf S\mathbf b_j.
$$

버린 분산을 줄이는 일과 남긴 분산을 키우는 일은 같은 일일까요? 둘의 합이 축을 어떻게 고르든 변하지 않는다면 그래요. 이를 확인하려고 전체 축의 분산을 모두 더해요. 2단계의 계산을 버린 축뿐 아니라 전체 축에 적용하면 좌표 제곱합이 표본의 길이 제곱이에요.

$$
\sum_{j=1}^D(\mathbf b_j^\top\mathbf x_n)^2=\|\mathbf x_n\|^2.
$$

표본에서 평균내면 왼쪽은 전체 축의 분산 합이 되고, 오른쪽에는 축 $\mathbf b_j$가 들어 있지 않아요.

$$
\sum_{j=1}^D\mathbf b_j^\top\mathbf S\mathbf b_j=\frac1N\sum_{n=1}^N\|\mathbf x_n\|^2.
$$

오른쪽을 성분으로 풀면 $\frac1N\sum_n\sum_d x_{dn}^2$이고, $d$번째 특성의 분산 $S_{dd}$를 모두 더한 값이에요. 행렬의 대각 원소 합을 트레이스(trace) $\operatorname{tr}\mathbf S$라고 불러요.

$$
\operatorname{tr}\mathbf S=\sum_{d=1}^D S_{dd}=\sum_{j=1}^D\mathbf b_j^\top\mathbf S\mathbf b_j.
$$

전체 분산 $\operatorname{tr}\mathbf S$는 어떤 직교 정규 기저를 써도 같다는 거예요. 이 합을 남긴 축과 버린 축으로 나누고 남긴 쪽을 옮겨요.

$$
J_M=\operatorname{tr}\mathbf S-\sum_{m=1}^M\mathbf b_m^\top\mathbf S\mathbf b_m.
$$

$\operatorname{tr}\mathbf S$가 고정된 값이라, 남긴 분산을 키우는 만큼 복원오차가 줄어요.

<a id="s1-discarded-minimum"></a>

#### 4 / 4 최소오차를 고윳값으로 읽기

가장 좋은 축을 골라 넣고, 그때의 오차를 고윳값으로 계산해요.

남긴 분산이 최대인 선택은 [첫 번째부터 M번째까지 방향 고르기](#s0-top-directions)에서 구했어요. 고윳값이 큰 순서로 $\mathbf S$의 고유벡터 $M$개를 남기는 선택이에요. 여기서부터 $\mathbf b_j$는 아무 축이 아니라 $\mathbf S$의 $j$번째 고유벡터 $\mathbf p_j$이고, 버리는 축은 나머지 고유벡터예요. 버린 축마다 $\mathbf S\mathbf b_j=\lambda_j\mathbf b_j$를 대입해요.

$$
\mathbf b_j^\top\mathbf S\mathbf b_j=\lambda_j\mathbf b_j^\top\mathbf b_j=\lambda_j.
$$

버린 축의 고윳값을 더하면 최소 복원오차예요.

$$
J_M^\star=\sum_{j=M+1}^D\lambda_j.
$$

$\mathbf S=\begin{bmatrix}2&1\\1&2\end{bmatrix}$의 예에서 고윳값은 3과 1이에요. 축 하나를 남기면 남긴 분산이 3, 복원오차가 1이고, 둘의 합 4가 $\operatorname{tr}\mathbf S=2+2$와 같아요.

남긴 축들의 사영 성분 x̃ = Bz와 버린 수직 축의 잔차 x − x̃가 피타고라스 등식을 이루는 모습을 [내적에서 행렬 사영으로 실험](../%EC%9D%B8%ED%84%B0%EB%A0%89%ED%8B%B0%EB%B8%8C_01_%EB%82%B4%EC%A0%81%EC%97%90%EC%84%9C_%ED%96%89%EB%A0%AC_%EC%82%AC%EC%98%81%EC%9C%BC%EB%A1%9C.html)의 평면 모드에서 확인해 보세요.

**교수님 말씀**

내적의 제곱을 스칼라와 그 전치의 곱으로 써도 값은 같지만, 가운데 두 벡터를 묶으면 공분산을 알아볼 수 있다고 설명했어요. 전체 에너지가 일정하니 남기는 쪽이 커지면 잃는 쪽이 작아진다고 연결했어요.

**페이지 요약**

원래 벡터와 복원값에서 남긴 축의 항이 상쇄되므로 복원오차는 버린 방향의 분산 합이에요.

*핵심 식*

- 전체 분산과 보존 분산의 차이

  $$
  J_M=\operatorname{tr}\mathbf S-\sum_{m=1}^M\mathbf b_m^\top\mathbf S\mathbf b_m.
  $$
- 상위 축을 남겼을 때 최소 복원오차

  $$
  J_M^\star=\sum_{j=M+1}^D\lambda_j.
  $$

*용어*

- **직교여공간(orthogonal complement)** — 남긴 부분공간의 모든 벡터에 수직인 벡터들의 공간.

---

<a id="s1-mnist"></a>

### MNIST에서 사영과 복원 읽기

*1104 수업 · L06 s11 · MML 예제 10.3–10.4*

**쉽게 말하면**

손글씨 한 장을 숫자 두 개로 요약하면 종이 위의 점 하나로 찍을 수 있어요.

![왼쪽의 두 손글씨를 각각 숫자 두 개로 요약해 오른쪽에 점 두 개로 나타낸 모식도](figures_1104/fig-digit-dots.svg)

*점이 모인 자리를 비교해 손글씨의 무리를 살펴봐요.*

**정확히 말하면**

MNIST 손글씨 한 장은 $28\times28$ 픽셀이라 밝기를 펼치면 $784$차원 벡터예요. 강의의 산점도에서는 숫자 0과 1의 중심화된 벡터를 상위 두 주성분 방향 $\mathbf b_1,\mathbf b_2$에 사영해요. $\mathbf x_n$을 한 이미지의 중심화 벡터라고 하면, 두 내적이 산점도의 가로·세로 좌표예요.

$$
\mathbf z_n=(\mathbf b_1^\top\mathbf x_n,\ \mathbf b_2^\top\mathbf x_n)^\top\in\mathbb R^2.
$$

산점도에서 0과 1은 비교적 분리되며 일부 점은 겹쳐요. 0의 무리는 1의 무리보다 더 넓게 퍼져 보여요. PCA는 전체 표본의 보존 분산을 기준으로 두 축을 고르고, 숫자 라벨은 산점도에서 두 무리를 구분해 표시할 때 써요. (L06 s11, MML Fig. 10.10)

이미지로 복원하려면 남긴 $M$개 좌표로 $\mathbf B\mathbf z_n\in\mathbb R^{784}$를 만든 다음, 중심화할 때 뺀 평균 이미지를 더하고 $28\times28$ 모양으로 배치해요. $M$이 작아도 복원한 이미지는 $784$픽셀이고, 중심화된 변동 중 보존한 방향의 정보가 담겨요.

**교과서의 복원 예시** MML 예제 10.4에서는 숫자 8로 PCA를 학습하고, 같은 테스트 이미지를 $M=1,10,100,500$으로 복원해 비교해요. 주성분 하나에서는 윤곽이 흐릿하고, 더 많은 축을 포함하면 필체의 세부가 드러나요. $784$개 축을 모두 쓰면 완전한 직교 정규 기저가 되어 원래 픽셀 값을 복원해요. (MML Fig. 10.12)

**교수님 말씀**

두 축으로 줄인 뒤에도 0과 1의 무리가 어느 정도 보이는 점을 짚었어요. 이어 축을 하나 더 확보하거나 50개 좌표를 남기는 상황을 들어, 압축할 때 남기는 좌표 수를 바꿀 수 있다고 설명했어요.

**페이지 요약**

784픽셀짜리 이미지를 상위 두 축의 좌표로 찍어 분포를 비교하고, 이미지 복원에는 남긴 축의 가중합과 평균을 사용해요.

PCA의 축 선택에는 숫자 라벨을 쓰지 않아요. 라벨은 산점도에서 두 무리를 구분해 표시할 때 사용해요.

*용어*

- **두 주성분의 사영 좌표** — 산점도의 가로·세로를 정하는 두 내적.
- **복원 이미지** — 남긴 축의 가중합에 평균을 되돌려 얻은 784픽셀 이미지. 784개 축을 모두 쓰면 원래 픽셀 값을 얻어요.

---

<a id="s2"></a>

## SVD와 실제 계산

<a id="s2-svd"></a>

### 데이터의 SVD에서 주성분 찾기

*1104 수업 · L06 s13*

**쉽게 말하면**

한 점씩 모아 만든 지도에서도 점들이 길게 늘어선 방향을 찾을 수 있어요.

![길게 늘어선 점 구름의 긴 방향을 잇는 선](figures_1104/fig-svd-cloud.svg)

*긴 방향을 먼저 고르면 점들의 퍼짐을 많이 담을 수 있어요.*

**정확히 말하면**

지금까지는 공분산 $\mathbf S$를 만든 다음 그 고유벡터를 구했어요. 이 페이지의 질문은 **$\mathbf S$를 만들지 않고 데이터 행렬에서 바로 같은 축을 구할 수 있을까요?**예요. 답을 먼저 말하면, 데이터 행렬을 특잇값 분해했을 때 나오는 왼쪽 특이벡터가 그 축이고, 축의 분산은 특잇값의 제곱을 표본 수로 나눈 값이에요.

<a id="s2-svd-factorization"></a>

#### 1 / 3 데이터 행렬 분해하기

특잇값 분해가 데이터 행렬을 어떤 세 행렬로 나누는지 확인해요.

출발식은 평균을 뺀 표본 $N$개를 열로 쌓은 $\mathbf X\in\mathbb R^{D\times N}$과 공분산 $\mathbf S=\mathbf X\mathbf X^\top/N$이에요.

고유분해 $\mathbf S=\mathbf P\boldsymbol\Lambda\mathbf P^\top$는 정방행렬에만 쓸 수 있어요. $\mathbf X$는 $D\times N$ 직사각행렬이라 그대로는 못 써요. 직사각행렬에 쓰는 비슷한 분해가 특잇값 분해(SVD)예요.

$$
\mathbf X=\mathbf U\mathbf\Sigma\mathbf V^\top.
$$

세 행렬의 역할은 다음과 같아요.

| 행렬 | 크기 | 담긴 것 |
|---|---|---|
| $\mathbf U$ | $D\times D$ | 특성 공간의 방향들이에요. 열 $\mathbf u_i$를 왼쪽 특이벡터라 하고, 서로 수직이고 길이가 1이에요. |
| $\mathbf\Sigma$ | $D\times N$ | 대각선에만 값이 있어요. 이 값 $\sigma_i\ge0$이 특잇값이고 큰 순서로 놓아요. |
| $\mathbf V$ | $N\times N$ | 표본 쪽의 방향들이에요. 열 $\mathbf v_i$도 서로 수직이고 길이가 1이에요. |

$\mathbf U$와 $\mathbf V$는 열들이 직교 정규인 정방행렬이라, 고유기저 행렬 $\mathbf P$와 마찬가지로 $\mathbf U^\top\mathbf U=\mathbf I_D$, $\mathbf V^\top\mathbf V=\mathbf I_N$이에요.

<a id="s2-svd-covariance"></a>

#### 2 / 3 공분산 식에 대입하기

분해한 $\mathbf X$를 공분산 식에 넣어, $\mathbf S$가 어떤 모양이 되는지 봐요.

1. **전치를 먼저 구해요.** 곱을 전치하면 순서가 뒤집혀요.

   $$
   \mathbf X^\top=(\mathbf U\mathbf\Sigma\mathbf V^\top)^\top=\mathbf V\mathbf\Sigma^\top\mathbf U^\top.
   $$
2. **출발식에 대입해요.**

   $$
   \mathbf S=\frac1N\mathbf X\mathbf X^\top=\frac1N\mathbf U\mathbf\Sigma\mathbf V^\top\mathbf V\mathbf\Sigma^\top\mathbf U^\top.
   $$
3. **가운데를 정리해요.** $\mathbf V^\top\mathbf V=\mathbf I_N$이므로 $\mathbf V$가 사라져요.

   $$
   \mathbf S=\mathbf U\left(\frac{\mathbf\Sigma\mathbf\Sigma^\top}{N}\right)\mathbf U^\top.
   $$

<a id="s2-svd-components"></a>

#### 3 / 3 주성분과 분산 읽기

정리한 식을 고유분해와 나란히 놓고, 축과 분산을 읽어요.

가운데의 $\mathbf\Sigma\mathbf\Sigma^\top$가 어떤 행렬인지 작은 경우로 확인해요. $D=2$, $N=3$이면 다음과 같아요.

$$
\mathbf\Sigma=\begin{bmatrix}\sigma_1&0&0\\0&\sigma_2&0\end{bmatrix},\qquad \mathbf\Sigma\mathbf\Sigma^\top=\begin{bmatrix}\sigma_1^2&0\\0&\sigma_2^2\end{bmatrix}.
$$

$\mathbf\Sigma\mathbf\Sigma^\top$는 특잇값의 제곱이 대각에 놓인 $D\times D$ 대각행렬이에요. 이제 두 식을 나란히 놓아요.

$$
\mathbf S=\mathbf P\boldsymbol\Lambda\mathbf P^\top,\qquad \mathbf S=\mathbf U\left(\frac{\mathbf\Sigma\mathbf\Sigma^\top}{N}\right)\mathbf U^\top.
$$

양쪽 모두 직교 정규 열을 가진 행렬, 대각행렬, 그 전치의 곱이에요. 그래서 $\mathbf U$의 열 $\mathbf u_i$가 $\mathbf S$의 고유벡터, 곧 주성분 방향이고, 가운데 대각 원소가 고윳값이에요.

$$
\lambda_i=\frac{\sigma_i^2}{N}.
$$

예를 들어 표본이 12개이고 가장 큰 특잇값이 6이면 첫 주성분의 분산은 $36/12=3$이에요. 특잇값 자체가 분산이 아니라는 점을 조심해요. 제곱한 뒤 표본 수로 나눠요.

표본 수가 특성 수보다 적으면($N\lt D$) 특잇값은 $N$개뿐이에요. 대각의 남는 자리는 0이고, 그 방향의 분산도 0이에요.

같은 데이터로 계산하면 두 방법에서 같은 고윳값과 같은 축을 얻어요. 다만 벡터의 부호는 반대로 나올 수 있고, 고윳값이 같은 축들은 그 공간 안에서 다르게 골라질 수 있어요.

**교수님 말씀**

> “$\mathbf{X}$를 그냥 놓고 singular value decomposition을 해도 똑같은 결과가 나온다.”

**페이지 요약**

공분산을 직접 분해하거나 중심화 데이터의 SVD에서 주성분 방향을 얻을 수 있어요.

*핵심 식*

- 데이터의 특잇값 분해

  $$
  \mathbf X=\mathbf U\mathbf\Sigma\mathbf V^\top.
  $$
- 공분산의 직교 분해

  $$
  \mathbf S=\mathbf U\left(\frac{\mathbf\Sigma\mathbf\Sigma^\top}{N}\right)\mathbf U^\top.
  $$
- 축에 남는 분산

  $$
  \lambda_i=\frac{\sigma_i^2}{N}.
  $$

왼쪽 특이벡터가 원래 특성 공간의 축이에요. 특잇값은 제곱한 뒤 표본 수로 나눠야 분산이에요. 부호는 달라질 수 있고, 고윳값이 같은 축들은 다르게 골라질 수 있어요.

---

<a id="s2-low-rank"></a>

### 작은 행렬 두 개로 데이터 복원하기

*1104 수업 · L06 s14*

**쉽게 말하면**

여러 겹의 그림을 포개서 한 장을 만들어요. 가장 진한 겹부터 몇 장 남기면 적은 양으로도 원래 모양을 많이 살릴 수 있어요.

![진한 두 겹을 남기고 흐린 한 겹을 빼는 그림](figures_1104/fig-rank-layers.svg)

**정확히 말하면**

이 페이지의 질문은 **표본 전체를 한꺼번에 압축하면 무엇을 저장하게 되고, 얼마나 틀릴까요?**예요. 답을 먼저 말하면, 축을 담은 행렬과 좌표를 담은 행렬 두 개를 저장하고, 틀리는 양은 버린 특잇값의 제곱합이에요.

출발점은 표본 하나의 복원식 $\tilde{\mathbf x}_n=\mathbf B\mathbf B^\top\mathbf x_n$이에요. $\mathbf X$의 열마다 같은 계산을 하므로 전체로는 $\tilde{\mathbf X}_M=\mathbf B\mathbf B^\top\mathbf X$예요. 축 $\mathbf B$에는 [데이터의 SVD에서 주성분 찾기](#s2-svd)에서 구한 상위 $M$개의 왼쪽 특이벡터를 넣어요. 이 행렬을 $\mathbf U_M\in\mathbb R^{D\times M}$이라 쓰고, $M\le\min(D,N)$으로 둬요.

<a id="s2-low-rank-coordinates"></a>

#### 1 / 3 남길 좌표 구하기

모든 표본의 좌표를 SVD의 조각으로 써요.

좌표는 $\mathbf z_n=\mathbf B^\top\mathbf x_n$이었으니, 전체 표본의 좌표 행렬은 $\mathbf U_M^\top\mathbf X$예요. 여기에 $\mathbf X=\mathbf U\mathbf\Sigma\mathbf V^\top$를 넣어요.

$$
\mathbf U_M^\top\mathbf X=(\mathbf U_M^\top\mathbf U)\mathbf\Sigma\mathbf V^\top.
$$

괄호 안을 먼저 봐요. $\mathbf U_M$은 $\mathbf U$의 첫 $M$열이에요. $\mathbf U_M^\top\mathbf U$의 $(i,j)$ 칸은 $\mathbf u_i^\top\mathbf u_j$라서 번호가 같을 때만 1이에요. $M=2$, $D=3$이면 다음과 같아요.

$$
\mathbf U_M^\top\mathbf U=\begin{bmatrix}1&0&0\\0&1&0\end{bmatrix}.
$$

이 행렬을 곱하면 뒤에 오는 행렬의 첫 $M$개 행만 남아요. $\mathbf\Sigma\mathbf V^\top$의 $i$번째 행은 $\sigma_i\mathbf v_i^\top$이므로, 남는 것은 상위 $M$개의 특잇값과 그에 대응하는 $\mathbf V$의 열이에요. 이들을 모은 행렬을 $\mathbf\Sigma_M\in\mathbb R^{M\times M}$(대각행렬), $\mathbf V_M\in\mathbb R^{N\times M}$($\mathbf V$의 첫 $M$열)이라 써요.

$$
\mathbf U_M^\top\mathbf X=\mathbf\Sigma_M\mathbf V_M^\top\in\mathbb R^{M\times N}.
$$

이 행렬의 $n$번째 열이 $n$번째 표본의 좌표 $M$개예요.

<a id="s2-low-rank-reconstruction"></a>

#### 2 / 3 원래 크기로 복원하기

축 행렬과 좌표 행렬을 곱해 모든 표본을 원래 차원으로 되돌려요.

복원은 좌표에 축을 곱하는 일이었어요. $D\times M$ 축 행렬에 $M\times N$ 좌표 행렬을 곱하면 $D\times N$ 행렬이 돌아와요.

$$
\tilde{\mathbf X}_M=\mathbf U_M\mathbf\Sigma_M\mathbf V_M^\top.
$$

압축한 데이터는 축 행렬 $\mathbf U_M$과 좌표 행렬 $\mathbf\Sigma_M\mathbf V_M^\top$ 두 개로 보관한다는 거예요.

같은 식을 겹으로도 읽을 수 있어요. $v_{ni}$를 $\mathbf v_i$의 $n$번째 성분이라 하면, $n$번째 표본의 $i$번째 좌표는 $\sigma_i v_{ni}$예요. $\sigma_i\mathbf u_i\mathbf v_i^\top$는 모든 표본에서 이 좌표를 같은 방향 $\mathbf u_i$에 곱해 나란히 놓은 한 겹이에요. 겹을 $M$장 더하면 복원 행렬이에요.

$$
\tilde{\mathbf X}_M=\sum_{i=1}^M\sigma_i\mathbf u_i\mathbf v_i^\top.
$$

특잇값이 큰 겹일수록 행렬에 크게 기여하므로 큰 것부터 남겨요.

<a id="s2-low-rank-error"></a>

#### 3 / 3 버린 정보의 양 계산하기

복원오차를 버린 특잇값으로 계산해요.

행렬 전체의 오차는 원소 차이를 모두 제곱해 더한 값으로 재요. 이 값을 Frobenius 노름의 제곱 $\|\cdot\|_F^2$이라 해요. 열마다 나누어 더하면 표본별 제곱 복원오차의 합이고, 평균이 아니라 합이라서 $J_M^\star$의 $N$배예요.

$$
\|\mathbf X-\tilde{\mathbf X}_M\|_F^2=NJ_M^\star.
$$

[버린 방향에서 복원오차 계산하기](#s1-discarded)의 $J_M^\star=\sum_{i\gt M}\lambda_i$에 $\lambda_i=\sigma_i^2/N$을 대입하면 $N$이 약분돼요.

$$
\|\mathbf X-\tilde{\mathbf X}_M\|_F^2=\sum_{i\gt M}\sigma_i^2.
$$

특잇값이 $5,3,1$일 때 두 겹을 남기면 버린 제곱합은 $1^2=1$이고, 한 겹만 남기면 $3^2+1^2=10$이에요. 특잇값이 없는 자리는 0으로 봐요.

이렇게 큰 특잇값부터 $M$겹을 남긴 행렬은, 랭크가 $M$ 이하인 모든 행렬 중 이 오차가 가장 작아요. 이 사실을 에카르트–영 정리(Eckart–Young theorem)라 하고, 이런 근사를 저랭크 근사라고 불러요. $\mathbf X$의 랭크가 처음부터 $M$ 이하이면 버릴 특잇값이 없어 그대로 복원돼요.

**꼭 기억해요**

> “low-rank matrix approximation이라는 것도 있는데 여러분 이게 요, 진짜 중요해요.”

**페이지 요약**

큰 특잇값에 대응하는 층부터 남기면 같은 랭크 한도에서 행렬의 제곱 복원오차가 가장 작아요.

*핵심 식*

- 전체 표본의 좌표

  $$
  \mathbf U_M^\top\mathbf X=\mathbf\Sigma_M\mathbf V_M^\top\in\mathbb R^{M\times N}.
  $$
- 랭크 제한 복원 ($M\le\min(D,N)$)

  $$
  \tilde{\mathbf X}_M=\mathbf U_M\mathbf\Sigma_M\mathbf V_M^\top.
  $$

  $$
  \tilde{\mathbf X}_M=\sum_{i=1}^M\sigma_i\mathbf u_i\mathbf v_i^\top.
  $$
- 전체 샘플의 제곱오차

  $$
  \|\mathbf X-\tilde{\mathbf X}_M\|_F^2=NJ_M^\star.
  $$

  $$
  \|\mathbf X-\tilde{\mathbf X}_M\|_F^2=\sum_{i\gt M}\sigma_i^2.
  $$

실제 랭크가 한도 이하이면 정확히 복원돼요.

---

<a id="s2-workflow"></a>

### PCA를 적용하고 원래 단위로 돌아가기

*1104 수업 · L06 s16–17*

**쉽게 말하면**

서로 다른 자로 잰 숫자를 비슷한 눈금에 놓아요. 짧게 적고 다시 펼친 다음 처음 쓰던 눈금으로 돌려요.

![눈금을 맞춘 뒤 짧게 적고 처음 눈금으로 복원하는 흐름](figures_1104/fig-workflow-scales.svg)

**정확히 말하면**

지금까지의 식은 모두 평균을 이미 뺀 데이터에서 출발했어요. 이 페이지의 질문은 **평균을 빼지 않은 실제 데이터에는 앞뒤로 무엇을 더 해야 할까요?**예요. 답을 먼저 말하면, 앞에서 평균을 빼고 필요하면 눈금을 맞춘 뒤 PCA를 하고, 복원한 다음에는 그 처리를 거꾸로 되돌려요.

<a id="s2-workflow-preprocess"></a>

#### 1 / 3 평균과 눈금 맞추기

훈련 데이터의 평균을 빼고, 필요하면 표준편차로 눈금을 맞춰요.

1. **중심화.** 원래 샘플 $\mathbf x^{\rm raw}\in\mathbb R^D$에서 훈련 데이터의 성분별 평균 $\boldsymbol\mu$를 빼요. 앞의 모든 식이 평균 0을 전제로 분산을 제곱의 평균으로 썼기 때문이에요.
2. **필요하면 표준화.** 특성마다 단위나 크기가 크게 다르면, 숫자가 큰 특성이 분산의 대부분을 차지해 축 선택을 좌우해요. 이를 막으려면 특성마다 표준편차 $s_d$로 나눠요. $\mathbf T=\operatorname{diag}(s_1,\ldots,s_D)$라 두면 처리한 샘플은 다음과 같아요.

   $$
   \mathbf y=\mathbf T^{-1}(\mathbf x^{\rm raw}-\boldsymbol\mu).
   $$

   나누려면 $s_d\gt0$이어야 해요. 값이 변하지 않는 상수 특성은 표준화하기 전에 제외할 수 있어요.

<a id="s2-workflow-projection"></a>

#### 2 / 3 축을 고르고 압축·복원하기

처리한 데이터에 앞에서 배운 식을 그대로 적용해요.

1. **축 선택.** 처리한 데이터 $\mathbf y$로 공분산을 만들고, 고윳값이 큰 순서로 정규직교 고유벡터 $M$개를 $\mathbf B$에 담아요.
2. **사영하고 복원.** $\mathbf z=\mathbf B^\top\mathbf y$로 $M$개 숫자로 줄이고, $\tilde{\mathbf y}=\mathbf B\mathbf z$로 다시 $D$개 숫자로 펼쳐요. 앞의 식에서 $\mathbf x_n$ 자리에 $\mathbf y$가 들어간 것뿐이에요.

<a id="s2-workflow-units"></a>

#### 3 / 3 원래 단위로 되돌리기

앞에서 한 처리를 마지막에 한 것부터 거꾸로 되돌려요.

$\tilde{\mathbf y}$는 아직 평균을 빼고 눈금을 맞춘 단위예요. 앞에서 평균을 먼저 빼고 표준편차로 나눴으니, 되돌릴 때는 표준편차를 먼저 곱하고 평균을 나중에 더해요.

$$
\tilde{\mathbf x}^{\rm raw}=\mathbf T\tilde{\mathbf y}+\boldsymbol\mu.
$$

표준화 없이 중심화만 했다면 위 두 식에서 $\mathbf T=\mathbf I_D$예요.

새 샘플을 압축하고 복원할 때도 훈련 데이터에서 구한 같은 평균과 표준편차를 써요. 표준화를 하느냐에 따라 분산과 복원오차를 재는 단위가 달라지므로 고르는 축도 달라질 수 있어요.

이 과정을 선형 오토인코더로 읽으면 $\mathbf B^\top$는 줄이는 인코더, $\mathbf B$는 펼치는 디코더예요.

**교수님 말씀**

> “채널을 가장 적게 쓰면서 누가 누가 잘 $\mathbf X$라는 벡터를 복원할 수 있는가?”

**페이지 요약**

처리한 공간에서 사영과 복원을 하고, 표준편차를 곱한 다음 평균을 더해 원래 단위로 돌아와요.

*핵심 식*

- 전처리

  $$
  \mathbf y=\mathbf T^{-1}(\mathbf x^{\rm raw}-\boldsymbol\mu).
  $$
- 인코더와 디코더$\mathbf z=\mathbf B^\top\mathbf y$, $\tilde{\mathbf y}=\mathbf B\mathbf z$
- 역변환

  $$
  \tilde{\mathbf x}^{\rm raw}=\mathbf T\tilde{\mathbf y}+\boldsymbol\mu.
  $$

표준화를 쓸 때는 양의 표준편차가 필요해요. 표준화 여부에 따라 분산을 재는 단위가 달라져요. $\mathbf B^\top$와 $\mathbf B$는 각각 선형 인코더와 디코더 역할을 해요.

---

<a id="s3"></a>

## 요약 · 예고

<a id="s3-cheatsheet"></a>

### 한 장 요약

| 하고 싶은 일 | 출발점과 결과 |
|---|---|
| 퍼짐을 보존하기 | 중심화한 데이터의 공분산 $\mathbf S=\mathbf X\mathbf X^\top/N$에서 상위 $M$개 정규직교 고유벡터로 $\mathbf B$를 구성해요. |
| 한 샘플을 압축하고 복원하기 | $\mathbf z_n=\mathbf B^\top\mathbf x_n$은 $M$차원 좌표예요. $\tilde{\mathbf x}_n=\mathbf B\mathbf z_n$은 $D$차원 복원이에요. |
| 훈련 평균 제곱오차 재기 | 상위 $M$개 방향을 남겼다면 버린 방향의 고윳값을 합해요. $J_M^\star=\sum_{i=M+1}^D\lambda_i$. |
| 공분산을 직접 분해하지 않고 계산하기 | $\mathbf X=\mathbf U\mathbf\Sigma\mathbf V^\top$에서 상위 왼쪽 특이벡터를 가져와요. $\lambda_i=\sigma_i^2/N$. |
| 원래 단위 복원하기 | 표준화한 데이터로 학습했다면 복원 벡터에 표준편차를 곱하고 평균을 더해요. |

---

<a id="s3-next"></a>

### 다음 시간 예고

- 다음 주 월요일 중간고사 문제 풀이
- 다음 주 수요일 밀도 추정
- 11월 중 PCA 실습 예정

---

<a id="s3-links"></a>

### 함께 보면 좋은 자료

- [1104 복습문제](복습문제_1104_PCA_Part2.md)
- [1102 정리노트에서 사영 분산 다시 보기](../../1102/정리노트_1102_PCA.html#s4-v1)
- [Lecture06 PCA Part 2 강의자료](../../../강의노트/Lecture06_PCA_Part2.pdf)

복습문제 10문항

- [문제지 PDF](복습문제_1104_PCA_Part2-문제.pdf)
- [해설지 PDF](복습문제_1104_PCA_Part2-답안.pdf)

---

출처는 정방철 교수님 강의자료 Lecture05–06, 1104 수업 전사, Deisenroth, Faisal, Ong의 *Mathematics for Machine Learning* 10장이에요.
