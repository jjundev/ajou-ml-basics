# 복습문제 8선 — 1019 수업 범위

교과서 본문 예제 두 개의 원형·수치변형으로 구성한 직선 투영 4개와 평면 투영 4개예요. 먼저 풀어 보고, 막히면 힌트를 열어 보세요.

> `복습문제_1019_Prediction_and_Projection.html`를 마크다운으로 옮겼어요. 원문, 힌트, 풀이는 접혀 있어요. 먼저 풀어 보고 펼쳐 보세요.

**목차**

- [A. 교과서 예제로 익히는 투영](#partA)
  - [P1. 직선으로 내린 그림자](#p1)
  - [P2. 직선으로 내린 그림자](#p2)
  - [P3. 직선으로 내린 그림자](#p3)
  - [P4. 직선으로 내린 그림자](#p4)
  - [P5. 평면에 가장 가까운 점](#p5)
  - [P6. 평면에 가장 가까운 점](#p6)
  - [P7. 평면에 가장 가까운 점](#p7)
  - [P8. 평면에 가장 가까운 점](#p8)

<a id="partA"></a>

## A. 교과서 예제로 익히는 투영

<a id="p1"></a>

### P1. 직선으로 내린 그림자

보통의 내적을 사용해요. 원점을 지나는 직선 $U=\operatorname{span}(\mathbf{b})$와 벡터 $\mathbf{x}$가 주어져요.

$$
\mathbf{b}=\begin{bmatrix}1\\2\\2\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}1\\1\\1\end{bmatrix}
$$

- (a) 직선 $U$로 보내는 투영행렬 $\mathbf{P}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})=\mathbf{P}\mathbf{x}$를 구해 보세요.
- (c) $\mathbf{P}\pi_U(\mathbf{x})=\pi_U(\mathbf{x})$인지 확인해 보세요.

<details><summary>교과서 원문 보기</summary>

“Find the projection matrix” — MML Example 3.10

</details>

<details><summary>힌트 보기</summary>

$\mathbf{P}=\mathbf{b}\mathbf{b}^{\mathsf T}/(\mathbf{b}^{\mathsf T}\mathbf{b})$를 먼저 써요. 투영벡터에 같은 행렬을 한 번 더 곱해 확인해요.

</details>

<details><summary>풀이 보기</summary>

1. 분모와 바깥곱을 구해요.

   $$
   \mathbf{b}^{\mathsf T}\mathbf{b}=9
   $$

   $$
   \mathbf{b}\mathbf{b}^{\mathsf T}=\begin{bmatrix}1 & 2 & 2\\2 & 4 & 4\\2 & 4 & 4\end{bmatrix}
   $$
2. 바깥곱을 분모로 나누면 투영행렬이에요.

   $$
   \mathbf{P}=\frac{\mathbf{b}\mathbf{b}^{\mathsf T}}{\mathbf{b}^{\mathsf T}\mathbf{b}}=\frac{1}{9}\begin{bmatrix}1 & 2 & 2\\2 & 4 & 4\\2 & 4 & 4\end{bmatrix}
   $$
3. 원래 벡터를 곱해 투영을 구해요.

   $$
   \mathbf{b}^{\mathsf T}\mathbf{x}=5
   $$

   $$
   \pi_U(\mathbf{x})=\mathbf{b}\frac{5}{9}=\begin{bmatrix}\frac{5}{9}\\\frac{10}{9}\\\frac{10}{9}\end{bmatrix}
   $$
4. 투영벡터는 이미 직선 위에 있어 다시 투영해도 같아요.

   $$
   \mathbf{b}^{\mathsf T}\pi_U(\mathbf{x})=5
   $$

   $$
   \mathbf{P}\pi_U(\mathbf{x})=\frac{5}{9}\begin{bmatrix}1\\2\\2\end{bmatrix}=\begin{bmatrix}\frac{5}{9}\\\frac{10}{9}\\\frac{10}{9}\end{bmatrix}
   $$

정답:

$$
\mathbf{P}=\frac{1}{9}\begin{bmatrix}1 & 2 & 2\\2 & 4 & 4\\2 & 4 & 4\end{bmatrix}
$$

$$
\pi_U(\mathbf{x})=\begin{bmatrix}\frac{5}{9}\\\frac{10}{9}\\\frac{10}{9}\end{bmatrix}
$$

다시 투영한 벡터도 같아요.

</details>

---

<a id="p2"></a>

### P2. 직선으로 내린 그림자

보통의 내적을 사용해요. 원점을 지나는 직선 $U=\operatorname{span}(\mathbf{b})$와 벡터 $\mathbf{x}$가 주어져요.

$$
\mathbf{b}=\begin{bmatrix}1\\0\\0\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}2\\3\\1\end{bmatrix}
$$

- (a) 직선 $U$로 보내는 투영행렬 $\mathbf{P}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})=\mathbf{P}\mathbf{x}$를 구해 보세요.
- (c) $\mathbf{P}\pi_U(\mathbf{x})=\pi_U(\mathbf{x})$인지 확인해 보세요.

<details><summary>교과서 원문 보기</summary>

“Find the projection matrix” — MML Example 3.10

</details>

<details><summary>힌트 보기</summary>

$\mathbf{P}=\mathbf{b}\mathbf{b}^{\mathsf T}/(\mathbf{b}^{\mathsf T}\mathbf{b})$를 먼저 써요. 투영벡터에 같은 행렬을 한 번 더 곱해 확인해요.

</details>

<details><summary>풀이 보기</summary>

1. 분모와 바깥곱을 구해요.

   $$
   \mathbf{b}^{\mathsf T}\mathbf{b}=1
   $$

   $$
   \mathbf{b}\mathbf{b}^{\mathsf T}=\begin{bmatrix}1 & 0 & 0\\0 & 0 & 0\\0 & 0 & 0\end{bmatrix}
   $$
2. 바깥곱을 분모로 나누면 투영행렬이에요.

   $$
   \mathbf{P}=\frac{\mathbf{b}\mathbf{b}^{\mathsf T}}{\mathbf{b}^{\mathsf T}\mathbf{b}}=\begin{bmatrix}1 & 0 & 0\\0 & 0 & 0\\0 & 0 & 0\end{bmatrix}
   $$
3. 원래 벡터를 곱해 투영을 구해요.

   $$
   \mathbf{b}^{\mathsf T}\mathbf{x}=2
   $$

   $$
   \pi_U(\mathbf{x})=\mathbf{b}\frac{2}{1}=\begin{bmatrix}2\\0\\0\end{bmatrix}
   $$
4. 투영벡터는 이미 직선 위에 있어 다시 투영해도 같아요.

   $$
   \mathbf{b}^{\mathsf T}\pi_U(\mathbf{x})=2
   $$

   $$
   \mathbf{P}\pi_U(\mathbf{x})=2\begin{bmatrix}1\\0\\0\end{bmatrix}=\begin{bmatrix}2\\0\\0\end{bmatrix}
   $$

정답:

$$
\mathbf{P}=\begin{bmatrix}1 & 0 & 0\\0 & 0 & 0\\0 & 0 & 0\end{bmatrix}
$$

$$
\pi_U(\mathbf{x})=\begin{bmatrix}2\\0\\0\end{bmatrix}
$$

다시 투영한 벡터도 같아요.

</details>

---

<a id="p3"></a>

### P3. 직선으로 내린 그림자

보통의 내적을 사용해요. 원점을 지나는 직선 $U=\operatorname{span}(\mathbf{b})$와 벡터 $\mathbf{x}$가 주어져요.

$$
\mathbf{b}=\begin{bmatrix}0\\1\\0\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}3\\2\\1\end{bmatrix}
$$

- (a) 직선 $U$로 보내는 투영행렬 $\mathbf{P}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})=\mathbf{P}\mathbf{x}$를 구해 보세요.
- (c) $\mathbf{P}\pi_U(\mathbf{x})=\pi_U(\mathbf{x})$인지 확인해 보세요.

<details><summary>교과서 원문 보기</summary>

“Find the projection matrix” — MML Example 3.10

</details>

<details><summary>힌트 보기</summary>

$\mathbf{P}=\mathbf{b}\mathbf{b}^{\mathsf T}/(\mathbf{b}^{\mathsf T}\mathbf{b})$를 먼저 써요. 투영벡터에 같은 행렬을 한 번 더 곱해 확인해요.

</details>

<details><summary>풀이 보기</summary>

1. 분모와 바깥곱을 구해요.

   $$
   \mathbf{b}^{\mathsf T}\mathbf{b}=1
   $$

   $$
   \mathbf{b}\mathbf{b}^{\mathsf T}=\begin{bmatrix}0 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
   $$
2. 바깥곱을 분모로 나누면 투영행렬이에요.

   $$
   \mathbf{P}=\frac{\mathbf{b}\mathbf{b}^{\mathsf T}}{\mathbf{b}^{\mathsf T}\mathbf{b}}=\begin{bmatrix}0 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
   $$
3. 원래 벡터를 곱해 투영을 구해요.

   $$
   \mathbf{b}^{\mathsf T}\mathbf{x}=2
   $$

   $$
   \pi_U(\mathbf{x})=\mathbf{b}\frac{2}{1}=\begin{bmatrix}0\\2\\0\end{bmatrix}
   $$
4. 투영벡터는 이미 직선 위에 있어 다시 투영해도 같아요.

   $$
   \mathbf{b}^{\mathsf T}\pi_U(\mathbf{x})=2
   $$

   $$
   \mathbf{P}\pi_U(\mathbf{x})=2\begin{bmatrix}0\\1\\0\end{bmatrix}=\begin{bmatrix}0\\2\\0\end{bmatrix}
   $$

정답:

$$
\mathbf{P}=\begin{bmatrix}0 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
$$

$$
\pi_U(\mathbf{x})=\begin{bmatrix}0\\2\\0\end{bmatrix}
$$

다시 투영한 벡터도 같아요.

</details>

---

<a id="p4"></a>

### P4. 직선으로 내린 그림자

보통의 내적을 사용해요. 원점을 지나는 직선 $U=\operatorname{span}(\mathbf{b})$와 벡터 $\mathbf{x}$가 주어져요.

$$
\mathbf{b}=\begin{bmatrix}1\\1\\1\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}3\\3\\3\end{bmatrix}
$$

- (a) 직선 $U$로 보내는 투영행렬 $\mathbf{P}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})=\mathbf{P}\mathbf{x}$를 구해 보세요.
- (c) $\mathbf{P}\pi_U(\mathbf{x})=\pi_U(\mathbf{x})$인지 확인해 보세요.

<details><summary>교과서 원문 보기</summary>

“Find the projection matrix” — MML Example 3.10

</details>

<details><summary>힌트 보기</summary>

$\mathbf{P}=\mathbf{b}\mathbf{b}^{\mathsf T}/(\mathbf{b}^{\mathsf T}\mathbf{b})$를 먼저 써요. 투영벡터에 같은 행렬을 한 번 더 곱해 확인해요.

</details>

<details><summary>풀이 보기</summary>

1. 분모와 바깥곱을 구해요.

   $$
   \mathbf{b}^{\mathsf T}\mathbf{b}=3
   $$

   $$
   \mathbf{b}\mathbf{b}^{\mathsf T}=\begin{bmatrix}1 & 1 & 1\\1 & 1 & 1\\1 & 1 & 1\end{bmatrix}
   $$
2. 바깥곱을 분모로 나누면 투영행렬이에요.

   $$
   \mathbf{P}=\frac{\mathbf{b}\mathbf{b}^{\mathsf T}}{\mathbf{b}^{\mathsf T}\mathbf{b}}=\frac{1}{3}\begin{bmatrix}1 & 1 & 1\\1 & 1 & 1\\1 & 1 & 1\end{bmatrix}
   $$
3. 원래 벡터를 곱해 투영을 구해요.

   $$
   \mathbf{b}^{\mathsf T}\mathbf{x}=9
   $$

   $$
   \pi_U(\mathbf{x})=\mathbf{b}\frac{9}{3}=\begin{bmatrix}3\\3\\3\end{bmatrix}
   $$
4. 투영벡터는 이미 직선 위에 있어 다시 투영해도 같아요.

   $$
   \mathbf{b}^{\mathsf T}\pi_U(\mathbf{x})=9
   $$

   $$
   \mathbf{P}\pi_U(\mathbf{x})=3\begin{bmatrix}1\\1\\1\end{bmatrix}=\begin{bmatrix}3\\3\\3\end{bmatrix}
   $$

정답:

$$
\mathbf{P}=\frac{1}{3}\begin{bmatrix}1 & 1 & 1\\1 & 1 & 1\\1 & 1 & 1\end{bmatrix}
$$

$$
\pi_U(\mathbf{x})=\begin{bmatrix}3\\3\\3\end{bmatrix}
$$

다시 투영한 벡터도 같아요.

</details>

---

<a id="p5"></a>

### P5. 평면에 가장 가까운 점

보통의 내적을 사용해요. $\mathbf{B}$의 두 열벡터가 평면 $U$의 기저예요. $U=\operatorname{span}(\mathbf{b}_1,\mathbf{b}_2)$로 두어요.

$$
\mathbf{B}=[\mathbf{b}_1\ \mathbf{b}_2]=\begin{bmatrix}1 & 0\\1 & 1\\1 & 2\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}6\\0\\0\end{bmatrix}
$$

- (a) 이 기저에 대한 투영벡터의 좌표 $\boldsymbol{\lambda}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})$와 투영오차 $\|\mathbf{x}-\pi_U(\mathbf{x})\|$를 구해 보세요.
- (c) 투영행렬 $\mathbf{P}$를 구해 보세요.
- (d) 차이벡터가 두 기저벡터에 직교하는지, $\mathbf{P}^2=\mathbf{P}$인지 확인해 보세요.

<details><summary>교과서 원문 보기</summary>

“find the coordinates” — MML Example 3.11

</details>

<details><summary>힌트 보기</summary>

$\mathbf{B}^{\mathsf T}\mathbf{B}\boldsymbol{\lambda}=\mathbf{B}^{\mathsf T}\mathbf{x}$를 풀어요. 그 좌표로 투영을 만든 뒤 차이벡터의 길이를 구해요.

</details>

<details><summary>풀이 보기</summary>

1. 정규방정식에 필요한 두 곱을 구해요.

   $$
   \mathbf{B}^{\mathsf T}\mathbf{B}=\begin{bmatrix}3 & 3\\3 & 5\end{bmatrix}
   $$

   $$
   \mathbf{B}^{\mathsf T}\mathbf{x}=\begin{bmatrix}6\\0\end{bmatrix}
   $$
2. 기저의 좌표를 구해요.

   $$
   \mathbf{B}^{\mathsf T}\mathbf{B}\boldsymbol{\lambda}=\mathbf{B}^{\mathsf T}\mathbf{x}
   $$

   $$
   \boldsymbol{\lambda}=\begin{bmatrix}5\\-3\end{bmatrix}
   $$
3. 좌표를 기저에 곱해 투영벡터를 구해요.

   $$
   \pi_U(\mathbf{x})=\mathbf{B}\boldsymbol{\lambda}=\begin{bmatrix}5\\2\\-1\end{bmatrix}
   $$
4. 차이벡터의 길이가 투영오차예요.

   $$
   \mathbf{r}=\mathbf{x}-\pi_U(\mathbf{x})=\begin{bmatrix}1\\-2\\1\end{bmatrix}
   $$

   $$
   \|\mathbf{r}\|^2=(1)^2+(-2)^2+(1)^2=6
   $$

   $$
   \|\mathbf{r}\|=\sqrt{6}
   $$
5. 역행렬을 끼워 투영행렬을 만들어요.

   $$
   (\mathbf{B}^{\mathsf T}\mathbf{B})^{-1}=\frac{1}{6}\begin{bmatrix}5 & -3\\-3 & 3\end{bmatrix}
   $$

   $$
   \mathbf{P}=\mathbf{B}(\mathbf{B}^{\mathsf T}\mathbf{B})^{-1}\mathbf{B}^{\mathsf T}=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}
   $$
6. 차이벡터와 기저벡터의 내적이 모두 0인지 확인해요.

   $$
   \mathbf{b}_1^{\mathsf T}\mathbf{r}=(1)(1)+(1)(-2)+(1)(1)=0
   $$

   $$
   \mathbf{b}_2^{\mathsf T}\mathbf{r}=(0)(1)+(1)(-2)+(2)(1)=0
   $$

   따라서 부호가 반대인 $\pi_U(\mathbf{x})-\mathbf{x}$도 두 기저벡터에 직교해요.
7. 행렬을 다시 곱해도 같은 투영행렬이 나와요.

   $$
   \mathbf{P}^{2}=\left(\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}\right)^2=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}=\mathbf{P}
   $$

정답:

$$
\boldsymbol{\lambda}=\begin{bmatrix}5\\-3\end{bmatrix},\quad\pi_U(\mathbf{x})=\begin{bmatrix}5\\2\\-1\end{bmatrix}
$$

$$
\|\mathbf{x}-\pi_U(\mathbf{x})\|=\sqrt{6}
$$

$$
\mathbf{P}=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}
$$

차이벡터는 두 기저벡터에 직교하고, $\mathbf{P}^2=\mathbf{P}$예요.

</details>

---

<a id="p6"></a>

### P6. 평면에 가장 가까운 점

보통의 내적을 사용해요. $\mathbf{B}$의 두 열벡터가 평면 $U$의 기저예요. $U=\operatorname{span}(\mathbf{b}_1,\mathbf{b}_2)$로 두어요.

$$
\mathbf{B}=[\mathbf{b}_1\ \mathbf{b}_2]=\begin{bmatrix}1 & 0\\0 & 1\\0 & 0\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}2\\3\\4\end{bmatrix}
$$

- (a) 이 기저에 대한 투영벡터의 좌표 $\boldsymbol{\lambda}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})$와 투영오차 $\|\mathbf{x}-\pi_U(\mathbf{x})\|$를 구해 보세요.
- (c) 투영행렬 $\mathbf{P}$를 구해 보세요.
- (d) 차이벡터가 두 기저벡터에 직교하는지, $\mathbf{P}^2=\mathbf{P}$인지 확인해 보세요.

<details><summary>교과서 원문 보기</summary>

“find the coordinates” — MML Example 3.11

</details>

<details><summary>힌트 보기</summary>

$\mathbf{B}^{\mathsf T}\mathbf{B}\boldsymbol{\lambda}=\mathbf{B}^{\mathsf T}\mathbf{x}$를 풀어요. 그 좌표로 투영을 만든 뒤 차이벡터의 길이를 구해요.

</details>

<details><summary>풀이 보기</summary>

1. 정규방정식에 필요한 두 곱을 구해요.

   $$
   \mathbf{B}^{\mathsf T}\mathbf{B}=\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}
   $$

   $$
   \mathbf{B}^{\mathsf T}\mathbf{x}=\begin{bmatrix}2\\3\end{bmatrix}
   $$
2. 기저의 좌표를 구해요.

   $$
   \mathbf{B}^{\mathsf T}\mathbf{B}\boldsymbol{\lambda}=\mathbf{B}^{\mathsf T}\mathbf{x}
   $$

   $$
   \boldsymbol{\lambda}=\begin{bmatrix}2\\3\end{bmatrix}
   $$
3. 좌표를 기저에 곱해 투영벡터를 구해요.

   $$
   \pi_U(\mathbf{x})=\mathbf{B}\boldsymbol{\lambda}=\begin{bmatrix}2\\3\\0\end{bmatrix}
   $$
4. 차이벡터의 길이가 투영오차예요.

   $$
   \mathbf{r}=\mathbf{x}-\pi_U(\mathbf{x})=\begin{bmatrix}0\\0\\4\end{bmatrix}
   $$

   $$
   \|\mathbf{r}\|^2=(0)^2+(0)^2+(4)^2=16
   $$

   $$
   \|\mathbf{r}\|=4
   $$
5. 역행렬을 끼워 투영행렬을 만들어요.

   $$
   (\mathbf{B}^{\mathsf T}\mathbf{B})^{-1}=\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}
   $$

   $$
   \mathbf{P}=\mathbf{B}(\mathbf{B}^{\mathsf T}\mathbf{B})^{-1}\mathbf{B}^{\mathsf T}=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
   $$
6. 차이벡터와 기저벡터의 내적이 모두 0인지 확인해요.

   $$
   \mathbf{b}_1^{\mathsf T}\mathbf{r}=(1)(0)+(0)(0)+(0)(4)=0
   $$

   $$
   \mathbf{b}_2^{\mathsf T}\mathbf{r}=(0)(0)+(1)(0)+(0)(4)=0
   $$

   따라서 부호가 반대인 $\pi_U(\mathbf{x})-\mathbf{x}$도 두 기저벡터에 직교해요.
7. 행렬을 다시 곱해도 같은 투영행렬이 나와요.

   $$
   \mathbf{P}^{2}=\left(\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}\right)^2=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}=\mathbf{P}
   $$

정답:

$$
\boldsymbol{\lambda}=\begin{bmatrix}2\\3\end{bmatrix},\quad\pi_U(\mathbf{x})=\begin{bmatrix}2\\3\\0\end{bmatrix}
$$

$$
\|\mathbf{x}-\pi_U(\mathbf{x})\|=4
$$

$$
\mathbf{P}=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
$$

차이벡터는 두 기저벡터에 직교하고, $\mathbf{P}^2=\mathbf{P}$예요.

</details>

---

<a id="p7"></a>

### P7. 평면에 가장 가까운 점

보통의 내적을 사용해요. $\mathbf{B}$의 두 열벡터가 평면 $U$의 기저예요. $U=\operatorname{span}(\mathbf{b}_1,\mathbf{b}_2)$로 두어요.

$$
\mathbf{B}=[\mathbf{b}_1\ \mathbf{b}_2]=\begin{bmatrix}1 & 0\\1 & 1\\1 & 2\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}0\\6\\0\end{bmatrix}
$$

- (a) 이 기저에 대한 투영벡터의 좌표 $\boldsymbol{\lambda}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})$와 투영오차 $\|\mathbf{x}-\pi_U(\mathbf{x})\|$를 구해 보세요.
- (c) 투영행렬 $\mathbf{P}$를 구해 보세요.
- (d) 차이벡터가 두 기저벡터에 직교하는지, $\mathbf{P}^2=\mathbf{P}$인지 확인해 보세요.

<details><summary>교과서 원문 보기</summary>

“find the coordinates” — MML Example 3.11

</details>

<details><summary>힌트 보기</summary>

$\mathbf{B}^{\mathsf T}\mathbf{B}\boldsymbol{\lambda}=\mathbf{B}^{\mathsf T}\mathbf{x}$를 풀어요. 그 좌표로 투영을 만든 뒤 차이벡터의 길이를 구해요.

</details>

<details><summary>풀이 보기</summary>

1. 정규방정식에 필요한 두 곱을 구해요.

   $$
   \mathbf{B}^{\mathsf T}\mathbf{B}=\begin{bmatrix}3 & 3\\3 & 5\end{bmatrix}
   $$

   $$
   \mathbf{B}^{\mathsf T}\mathbf{x}=\begin{bmatrix}6\\6\end{bmatrix}
   $$
2. 기저의 좌표를 구해요.

   $$
   \mathbf{B}^{\mathsf T}\mathbf{B}\boldsymbol{\lambda}=\mathbf{B}^{\mathsf T}\mathbf{x}
   $$

   $$
   \boldsymbol{\lambda}=\begin{bmatrix}2\\0\end{bmatrix}
   $$
3. 좌표를 기저에 곱해 투영벡터를 구해요.

   $$
   \pi_U(\mathbf{x})=\mathbf{B}\boldsymbol{\lambda}=\begin{bmatrix}2\\2\\2\end{bmatrix}
   $$
4. 차이벡터의 길이가 투영오차예요.

   $$
   \mathbf{r}=\mathbf{x}-\pi_U(\mathbf{x})=\begin{bmatrix}-2\\4\\-2\end{bmatrix}
   $$

   $$
   \|\mathbf{r}\|^2=(-2)^2+(4)^2+(-2)^2=24
   $$

   $$
   \|\mathbf{r}\|=\sqrt{24}
   $$
5. 역행렬을 끼워 투영행렬을 만들어요.

   $$
   (\mathbf{B}^{\mathsf T}\mathbf{B})^{-1}=\frac{1}{6}\begin{bmatrix}5 & -3\\-3 & 3\end{bmatrix}
   $$

   $$
   \mathbf{P}=\mathbf{B}(\mathbf{B}^{\mathsf T}\mathbf{B})^{-1}\mathbf{B}^{\mathsf T}=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}
   $$
6. 차이벡터와 기저벡터의 내적이 모두 0인지 확인해요.

   $$
   \mathbf{b}_1^{\mathsf T}\mathbf{r}=(1)(-2)+(1)(4)+(1)(-2)=0
   $$

   $$
   \mathbf{b}_2^{\mathsf T}\mathbf{r}=(0)(-2)+(1)(4)+(2)(-2)=0
   $$

   따라서 부호가 반대인 $\pi_U(\mathbf{x})-\mathbf{x}$도 두 기저벡터에 직교해요.
7. 행렬을 다시 곱해도 같은 투영행렬이 나와요.

   $$
   \mathbf{P}^{2}=\left(\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}\right)^2=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}=\mathbf{P}
   $$

정답:

$$
\boldsymbol{\lambda}=\begin{bmatrix}2\\0\end{bmatrix},\quad\pi_U(\mathbf{x})=\begin{bmatrix}2\\2\\2\end{bmatrix}
$$

$$
\|\mathbf{x}-\pi_U(\mathbf{x})\|=\sqrt{24}
$$

$$
\mathbf{P}=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}
$$

차이벡터는 두 기저벡터에 직교하고, $\mathbf{P}^2=\mathbf{P}$예요.

</details>

---

<a id="p8"></a>

### P8. 평면에 가장 가까운 점

보통의 내적을 사용해요. $\mathbf{B}$의 두 열벡터가 평면 $U$의 기저예요. $U=\operatorname{span}(\mathbf{b}_1,\mathbf{b}_2)$로 두어요.

$$
\mathbf{B}=[\mathbf{b}_1\ \mathbf{b}_2]=\begin{bmatrix}1 & 1\\2 & 0\\0 & 1\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}1\\2\\3\end{bmatrix}
$$

- (a) 이 기저에 대한 투영벡터의 좌표 $\boldsymbol{\lambda}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})$와 투영오차 $\|\mathbf{x}-\pi_U(\mathbf{x})\|$를 구해 보세요.
- (c) 투영행렬 $\mathbf{P}$를 구해 보세요.
- (d) 차이벡터가 두 기저벡터에 직교하는지, $\mathbf{P}^2=\mathbf{P}$인지 확인해 보세요.

<details><summary>교과서 원문 보기</summary>

“find the coordinates” — MML Example 3.11

</details>

<details><summary>힌트 보기</summary>

$\mathbf{B}^{\mathsf T}\mathbf{B}\boldsymbol{\lambda}=\mathbf{B}^{\mathsf T}\mathbf{x}$를 풀어요. 그 좌표로 투영을 만든 뒤 차이벡터의 길이를 구해요.

</details>

<details><summary>풀이 보기</summary>

1. 정규방정식에 필요한 두 곱을 구해요.

   $$
   \mathbf{B}^{\mathsf T}\mathbf{B}=\begin{bmatrix}5 & 1\\1 & 2\end{bmatrix}
   $$

   $$
   \mathbf{B}^{\mathsf T}\mathbf{x}=\begin{bmatrix}5\\4\end{bmatrix}
   $$
2. 기저의 좌표를 구해요.

   $$
   \mathbf{B}^{\mathsf T}\mathbf{B}\boldsymbol{\lambda}=\mathbf{B}^{\mathsf T}\mathbf{x}
   $$

   $$
   \boldsymbol{\lambda}=\begin{bmatrix}\frac{2}{3}\\\frac{5}{3}\end{bmatrix}
   $$
3. 좌표를 기저에 곱해 투영벡터를 구해요.

   $$
   \pi_U(\mathbf{x})=\mathbf{B}\boldsymbol{\lambda}=\begin{bmatrix}\frac{7}{3}\\\frac{4}{3}\\\frac{5}{3}\end{bmatrix}
   $$
4. 차이벡터의 길이가 투영오차예요.

   $$
   \mathbf{r}=\mathbf{x}-\pi_U(\mathbf{x})=\begin{bmatrix}-\frac{4}{3}\\\frac{2}{3}\\\frac{4}{3}\end{bmatrix}
   $$

   $$
   \|\mathbf{r}\|^2=(-\frac{4}{3})^2+(\frac{2}{3})^2+(\frac{4}{3})^2=4
   $$

   $$
   \|\mathbf{r}\|=2
   $$
5. 역행렬을 끼워 투영행렬을 만들어요.

   $$
   (\mathbf{B}^{\mathsf T}\mathbf{B})^{-1}=\frac{1}{9}\begin{bmatrix}2 & -1\\-1 & 5\end{bmatrix}
   $$

   $$
   \mathbf{P}=\mathbf{B}(\mathbf{B}^{\mathsf T}\mathbf{B})^{-1}\mathbf{B}^{\mathsf T}=\frac{1}{9}\begin{bmatrix}5 & 2 & 4\\2 & 8 & -2\\4 & -2 & 5\end{bmatrix}
   $$
6. 차이벡터와 기저벡터의 내적이 모두 0인지 확인해요.

   $$
   \mathbf{b}_1^{\mathsf T}\mathbf{r}=(1)(-\frac{4}{3})+(2)(\frac{2}{3})+(0)(\frac{4}{3})=0
   $$

   $$
   \mathbf{b}_2^{\mathsf T}\mathbf{r}=(1)(-\frac{4}{3})+(0)(\frac{2}{3})+(1)(\frac{4}{3})=0
   $$

   따라서 부호가 반대인 $\pi_U(\mathbf{x})-\mathbf{x}$도 두 기저벡터에 직교해요.
7. 행렬을 다시 곱해도 같은 투영행렬이 나와요.

   $$
   \mathbf{P}^{2}=\left(\frac{1}{9}\begin{bmatrix}5 & 2 & 4\\2 & 8 & -2\\4 & -2 & 5\end{bmatrix}\right)^2=\frac{1}{9}\begin{bmatrix}5 & 2 & 4\\2 & 8 & -2\\4 & -2 & 5\end{bmatrix}=\mathbf{P}
   $$

정답:

$$
\boldsymbol{\lambda}=\begin{bmatrix}\frac{2}{3}\\\frac{5}{3}\end{bmatrix},\quad\pi_U(\mathbf{x})=\begin{bmatrix}\frac{7}{3}\\\frac{4}{3}\\\frac{5}{3}\end{bmatrix}
$$

$$
\|\mathbf{x}-\pi_U(\mathbf{x})\|=2
$$

$$
\mathbf{P}=\frac{1}{9}\begin{bmatrix}5 & 2 & 4\\2 & 8 & -2\\4 & -2 & 5\end{bmatrix}
$$

차이벡터는 두 기저벡터에 직교하고, $\mathbf{P}^2=\mathbf{P}$예요.

</details>

---

출처: Deisenroth, Faisal, Ong, Mathematics for Machine Learning (Cambridge University Press, 2020). 풀이는 자체 작성이며 수치는 Python으로 검증했습니다.
