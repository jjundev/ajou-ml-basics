# 머신러닝기초 복습 1019 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [P1. 직선으로 내린 그림자](#p1)
  - [P2. 직선으로 내린 그림자](#p2)
  - [P3. 직선으로 내린 그림자](#p3)
  - [P4. 직선으로 내린 그림자](#p4)
  - [P5. 평면에 가장 가까운 점](#p5)
  - [P6. 평면에 가장 가까운 점](#p6)
  - [P7. 평면에 가장 가까운 점](#p7)
  - [P8. 평면에 가장 가까운 점](#p8)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### P1. 직선으로 내린 그림자

MML Example 3.10 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1019_Prediction_and_Projection.html#p1)

#### 주어진 조건

보통의 내적을 사용해요. 원점을 지나는 직선 $U=\operatorname{span}(\mathbf{b})$와 벡터 $\mathbf{x}$가 주어져요.

$$
\mathbf{b}=\begin{bmatrix}1\\2\\2\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}1\\1\\1\end{bmatrix}
$$

#### 구할 것

- (a) 직선 $U$로 보내는 투영행렬 $\mathbf{P}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})=\mathbf{P}\mathbf{x}$를 구해 보세요.
- (c) $\mathbf{P}\pi_U(\mathbf{x})=\pi_U(\mathbf{x})$인지 확인해 보세요.

<details><summary>원문 보기</summary>

“Find the projection matrix” — MML Example 3.10

</details>

#### 문제를 내 말로 읽어요

공간의 점을 정해진 줄로 곧게 내려요. 먼저 이 일을 하는 표를 만들고, 주어진 점을 보낸 뒤, 한 번 더 보내도 제자리인지 확인해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘원점을 지나는 직선’과 ‘보통의 내적’이라는 조건에서 직교투영(orthogonal projection)을 떠올려요. 직선 위 점 중 원래 벡터와 거리가 가장 작은 점을 구하는 연산이에요. 세 방향 성분이 함께 남는 기울어진 직선이에요. 결과의 성분비가 1:2:2가 되어야 해요.

$U=\operatorname{span}(\mathbf b)$는 $\mathbf b$의 모든 실수배를 모은 집합이에요. $\mathbf b$는 방향을 정하는 3차원 열벡터, $\mathbf x$는 옮길 벡터, $\lambda$는 직선 위 위치를 정하는 스칼라예요. 후보를 $\lambda\mathbf b$로 쓰면 잔차 $\mathbf r=\mathbf x-\lambda\mathbf b$가 직선에 수직일 때 가장 가까워요.

$$
\mathbf b^{\mathsf T}(\mathbf x-\lambda\mathbf b)=0
$$

$$
\lambda=\frac{\mathbf b^{\mathsf T}\mathbf x}{\mathbf b^{\mathsf T}\mathbf b}
$$

$$
\pi_U(\mathbf x)=\mathbf P\mathbf x,\qquad\mathbf P=\frac{\mathbf b\mathbf b^{\mathsf T}}{\mathbf b^{\mathsf T}\mathbf b}
$$

전치(transpose)는 열을 행으로 바꿔요. 분모 $\mathbf b^{\mathsf T}\mathbf b$는 $1\times1$인 제곱 길이이고, 분자 $\mathbf b\mathbf b^{\mathsf T}$는 $3\times3$ 바깥곱(outer product)이에요. 그래서 $\mathbf P$도 $3\times3$이에요. $\mathbf b\ne\mathbf0$일 때만 분모가 양수여서 이 공식을 쓸 수 있고, 이 문제의 방향벡터는 그 조건을 만족해요.

한 번 보낸 결과는 이미 직선 위에 있으므로 두 번째 투영은 결과를 바꾸지 않아요. 이 성질이 멱등성(idempotence) $\mathbf P^2=\mathbf P$예요. (c)에서는 주어진 벡터의 결과에 한 번 더 곱해 직접 확인해요.

[직선 위에서 가장 가까운 점](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1019_Prediction_and_Projection.html#s2-line)의 직교 잔차 유도와 같은 원리예요.

#### 종이에 쓸 첫 줄

$$
\mathbf b^{\mathsf T}\mathbf b=1^2+2^2+2^2=9
$$

투영행렬의 분모부터 확정해요. 다음 줄에는 방향벡터를 세로와 가로로 곱해 바깥곱을 써요. 이 첫 줄은 원래 벡터 $\mathbf x$를 아직 사용하지 않아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 투영행렬

방향벡터의 각 성분을 모든 성분에 곱해 행을 만들어요. 내적처럼 모두 더해 숫자 하나로 줄이지 않아요.

$$
\mathbf b\mathbf b^{\mathsf T}=\begin{bmatrix}1\\2\\2\end{bmatrix}\begin{bmatrix}1 & 2 & 2\end{bmatrix}=\begin{bmatrix}1 & 2 & 2\\2 & 4 & 4\\2 & 4 & 4\end{bmatrix}
$$

제곱 길이 9로 각 원소를 나누면 요청한 투영행렬이에요.

$$
\boxed{\mathbf P=\frac{1}{9}\begin{bmatrix}1 & 2 & 2\\2 & 4 & 4\\2 & 4 & 4\end{bmatrix}}
$$

#### (b) 투영벡터

행렬을 원래 벡터에 적용해요. 같은 계산을 먼저 내적으로 묶으면 $\mathbf b(\mathbf b^{\mathsf T}\mathbf x)/(\mathbf b^{\mathsf T}\mathbf b)$가 되어 계산량이 줄어요.

$$
\mathbf b^{\mathsf T}\mathbf x=(1)(1)+(2)(1)+(2)(1)=5
$$

$$
\lambda=\frac{5}{9}
$$

$$
\boxed{\pi_U(\mathbf x)=\frac{5}{9}\begin{bmatrix}1\\2\\2\end{bmatrix}=\begin{bmatrix}\frac{5}{9}\\\frac{10}{9}\\\frac{10}{9}\end{bmatrix}}
$$

배율은 숫자 하나이고 투영벡터는 그 숫자를 방향벡터에 곱한 결과예요.

#### (c) 다시 투영하기

첫 투영값 전체를 다시 입력에 넣어요. 새 방향이나 새 행렬을 구하는 일이 아니에요.

$$
\mathbf b^{\mathsf T}\pi_U(\mathbf x)=5
$$

$$
\mathbf P\pi_U(\mathbf x)=\mathbf b\frac{5}{9}
$$

$$
=\frac{5}{9}\begin{bmatrix}1\\2\\2\end{bmatrix}=\begin{bmatrix}\frac{5}{9}\\\frac{10}{9}\\\frac{10}{9}\end{bmatrix}
$$

이 결과가 (b)의 벡터와 성분별로 같으므로 물음의 등식이 성립해요.

#### 완성 답과 검산

#### (a) 행렬 확인

답의 행렬은 대칭이에요. 원소도 확인하고, 두 번의 작용이 한 번과 같은지 행렬곱으로 확인해요.

$$
\mathbf P^{\mathsf T}=\mathbf P
$$

$$
\mathbf P^2=\frac{1}{81}\begin{bmatrix}9 & 18 & 18\\18 & 36 & 36\\18 & 36 & 36\end{bmatrix}
$$

$$
=\frac{1}{9}\begin{bmatrix}1 & 2 & 2\\2 & 4 & 4\\2 & 4 & 4\end{bmatrix}=\mathbf P
$$

또한 $\mathbf P\mathbf b=\mathbf b$라서 방향벡터 자체를 보존해요. 분자와 분모의 곱 순서가 맞는지 점검할 수 있어요.

#### (b) 직선과 직교 조건 확인

$$
\mathbf r=\mathbf x-\pi_U(\mathbf x)=\begin{bmatrix}\frac{4}{9}\\-\frac{1}{9}\\-\frac{1}{9}\end{bmatrix}
$$

$$
\mathbf b^{\mathsf T}\mathbf r=1\cdot\frac49+2\cdot(-\frac19)+2\cdot(-\frac19)=0
$$

투영값이 $\frac{5}{9}\mathbf b$로 직선 위에 있고, 잔차의 내적은 0이에요. 두 조건을 함께 만족하므로 가장 가까운 점이라는 독립적인 기하 조건도 맞아요.

#### (c) 재투영 확인

행렬로 직접 곱한 값도 확인해요.

$$
\mathbf P\pi_U(\mathbf x)=\frac{1}{9}\begin{bmatrix}1 & 2 & 2\\2 & 4 & 4\\2 & 4 & 4\end{bmatrix}\begin{bmatrix}\frac{5}{9}\\\frac{10}{9}\\\frac{10}{9}\end{bmatrix}=\begin{bmatrix}\frac{5}{9}\\\frac{10}{9}\\\frac{10}{9}\end{bmatrix}
$$

이 값이 완성 답이에요. 모든 $\mathbf x$에 대한 멱등성은 (a)의 행렬 제곱으로, 이 문제의 입력에 대한 재투영은 위 대입으로 각각 확인했어요.

#### 이 문항에서 조심할 점

분모 9는 길이 3의 제곱이에요. 3으로 나누면 직선 위의 점은 나오지만 가장 가까운 점이 아니에요. 배율 $5/9$만 답으로 내지 말고 세 성분을 갖는 투영벡터도 써요.

직교투영행렬이라는 이름이 직교행렬을 뜻하지는 않아요. 여기서는 $\mathbf P^2=\mathbf P$이고, 길이를 보존하는 조건 $\mathbf P^{\mathsf T}\mathbf P=\mathbf I$를 요구하지 않아요.

#### 설명을 닫고 다시 해 봐요

1. 왜 분모가 길이가 아니라 제곱 길이인지 말하고, 숫자를 다시 계산해요.
2. 행렬·배율·투영벡터의 크기를 구별하며 세 답을 다시 써요.
3. 잔차와 방향벡터의 내적, 투영값의 재투영을 해설 없이 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

직선의 가장 가까운 점은 잔차가 방향벡터와 직교하는 점이에요.

$$
\mathbf P=\frac{\mathbf b\mathbf b^{\mathsf T}}{\mathbf b^{\mathsf T}\mathbf b}
$$

#### 첫 줄

$$
\mathbf b^{\mathsf T}\mathbf b=9
$$

#### 핵심 답

$$
\pi_U(\mathbf x)=\begin{bmatrix}\frac{5}{9}\\\frac{10}{9}\\\frac{10}{9}\end{bmatrix}
$$

#### 검산

직선 위의 점인지와 잔차의 직교를 함께 확인해요. 다시 투영한 값도 같아요.

#### 조건·구분

보통의 내적과 $\mathbf b\ne\mathbf0$에서 쓰는 식이에요. 분모는 길이의 제곱인 스칼라, 분자는 $3\times3$ 바깥곱이에요. 배율은 스칼라이고 투영벡터는 세 성분이에요. $\mathbf P^T=\mathbf P$, $\mathbf P^2=\mathbf P$인 직교투영행렬을 길이 보존 직교행렬 $\mathbf P^T\mathbf P=\mathbf I$와 구별해요.

---

<a id="p2"></a>

### P2. 직선으로 내린 그림자

MML Example 3.10 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1019_Prediction_and_Projection.html#p2)

#### 주어진 조건

보통의 내적을 사용해요. 원점을 지나는 직선 $U=\operatorname{span}(\mathbf{b})$와 벡터 $\mathbf{x}$가 주어져요.

$$
\mathbf{b}=\begin{bmatrix}1\\0\\0\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}2\\3\\1\end{bmatrix}
$$

#### 구할 것

- (a) 직선 $U$로 보내는 투영행렬 $\mathbf{P}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})=\mathbf{P}\mathbf{x}$를 구해 보세요.
- (c) $\mathbf{P}\pi_U(\mathbf{x})=\pi_U(\mathbf{x})$인지 확인해 보세요.

<details><summary>원문 보기</summary>

“Find the projection matrix” — MML Example 3.10

</details>

#### 문제를 내 말로 읽어요

공간의 점을 정해진 줄로 곧게 내려요. 먼저 이 일을 하는 표를 만들고, 주어진 점을 보낸 뒤, 한 번 더 보내도 제자리인지 확인해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘원점을 지나는 직선’과 ‘보통의 내적’이라는 조건에서 직교투영(orthogonal projection)을 떠올려요. 직선 위 점 중 원래 벡터와 거리가 가장 작은 점을 구하는 연산이에요. 첫째 좌표축으로 내리는 문제예요. 첫 성분은 남고 다른 두 성분은 0이 되어야 해요.

$U=\operatorname{span}(\mathbf b)$는 $\mathbf b$의 모든 실수배를 모은 집합이에요. $\mathbf b$는 방향을 정하는 3차원 열벡터, $\mathbf x$는 옮길 벡터, $\lambda$는 직선 위 위치를 정하는 스칼라예요. 후보를 $\lambda\mathbf b$로 쓰면 잔차 $\mathbf r=\mathbf x-\lambda\mathbf b$가 직선에 수직일 때 가장 가까워요.

$$
\mathbf b^{\mathsf T}(\mathbf x-\lambda\mathbf b)=0
$$

$$
\lambda=\frac{\mathbf b^{\mathsf T}\mathbf x}{\mathbf b^{\mathsf T}\mathbf b}
$$

$$
\pi_U(\mathbf x)=\mathbf P\mathbf x,\qquad\mathbf P=\frac{\mathbf b\mathbf b^{\mathsf T}}{\mathbf b^{\mathsf T}\mathbf b}
$$

전치(transpose)는 열을 행으로 바꿔요. 분모 $\mathbf b^{\mathsf T}\mathbf b$는 $1\times1$인 제곱 길이이고, 분자 $\mathbf b\mathbf b^{\mathsf T}$는 $3\times3$ 바깥곱(outer product)이에요. 그래서 $\mathbf P$도 $3\times3$이에요. $\mathbf b\ne\mathbf0$일 때만 분모가 양수여서 이 공식을 쓸 수 있고, 이 문제의 방향벡터는 그 조건을 만족해요.

한 번 보낸 결과는 이미 직선 위에 있으므로 두 번째 투영은 결과를 바꾸지 않아요. 이 성질이 멱등성(idempotence) $\mathbf P^2=\mathbf P$예요. (c)에서는 주어진 벡터의 결과에 한 번 더 곱해 직접 확인해요.

[직선 위에서 가장 가까운 점](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1019_Prediction_and_Projection.html#s2-line)의 직교 잔차 유도와 같은 원리예요.

#### 종이에 쓸 첫 줄

$$
\mathbf b^{\mathsf T}\mathbf b=1^2+0^2+0^2=1
$$

투영행렬의 분모부터 확정해요. 다음 줄에는 방향벡터를 세로와 가로로 곱해 바깥곱을 써요. 이 첫 줄은 원래 벡터 $\mathbf x$를 아직 사용하지 않아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 투영행렬

방향벡터의 각 성분을 모든 성분에 곱해 행을 만들어요. 내적처럼 모두 더해 숫자 하나로 줄이지 않아요.

$$
\mathbf b\mathbf b^{\mathsf T}=\begin{bmatrix}1\\0\\0\end{bmatrix}\begin{bmatrix}1 & 0 & 0\end{bmatrix}=\begin{bmatrix}1 & 0 & 0\\0 & 0 & 0\\0 & 0 & 0\end{bmatrix}
$$

제곱 길이 1로 각 원소를 나누면 요청한 투영행렬이에요.

$$
\boxed{\mathbf P=\begin{bmatrix}1 & 0 & 0\\0 & 0 & 0\\0 & 0 & 0\end{bmatrix}}
$$

#### (b) 투영벡터

행렬을 원래 벡터에 적용해요. 같은 계산을 먼저 내적으로 묶으면 $\mathbf b(\mathbf b^{\mathsf T}\mathbf x)/(\mathbf b^{\mathsf T}\mathbf b)$가 되어 계산량이 줄어요.

$$
\mathbf b^{\mathsf T}\mathbf x=(1)(2)+(0)(3)+(0)(1)=2
$$

$$
\lambda=\frac{2}{1}=2
$$

$$
\boxed{\pi_U(\mathbf x)=2\begin{bmatrix}1\\0\\0\end{bmatrix}=\begin{bmatrix}2\\0\\0\end{bmatrix}}
$$

배율은 숫자 하나이고 투영벡터는 그 숫자를 방향벡터에 곱한 결과예요.

#### (c) 다시 투영하기

첫 투영값 전체를 다시 입력에 넣어요. 새 방향이나 새 행렬을 구하는 일이 아니에요.

$$
\mathbf b^{\mathsf T}\pi_U(\mathbf x)=2
$$

$$
\mathbf P\pi_U(\mathbf x)=\mathbf b\frac{2}{1}
$$

$$
=2\begin{bmatrix}1\\0\\0\end{bmatrix}=\begin{bmatrix}2\\0\\0\end{bmatrix}
$$

이 결과가 (b)의 벡터와 성분별로 같으므로 물음의 등식이 성립해요.

#### 완성 답과 검산

#### (a) 행렬 확인

답의 행렬은 대칭이에요. 원소도 확인하고, 두 번의 작용이 한 번과 같은지 행렬곱으로 확인해요.

$$
\mathbf P^{\mathsf T}=\mathbf P
$$

$$
\mathbf P^2=\frac{1}{1}\begin{bmatrix}1 & 0 & 0\\0 & 0 & 0\\0 & 0 & 0\end{bmatrix}
$$

$$
=\begin{bmatrix}1 & 0 & 0\\0 & 0 & 0\\0 & 0 & 0\end{bmatrix}=\mathbf P
$$

또한 $\mathbf P\mathbf b=\mathbf b$라서 방향벡터 자체를 보존해요. 분자와 분모의 곱 순서가 맞는지 점검할 수 있어요.

#### (b) 직선과 직교 조건 확인

$$
\mathbf r=\mathbf x-\pi_U(\mathbf x)=\begin{bmatrix}0\\3\\1\end{bmatrix}
$$

$$
\mathbf b^{\mathsf T}\mathbf r=1\cdot0+0\cdot3+0\cdot1=0
$$

투영값이 $2\mathbf b$로 직선 위에 있고, 잔차의 내적은 0이에요. 두 조건을 함께 만족하므로 가장 가까운 점이라는 독립적인 기하 조건도 맞아요.

#### (c) 재투영 확인

행렬로 직접 곱한 값도 확인해요.

$$
\mathbf P\pi_U(\mathbf x)=\begin{bmatrix}1 & 0 & 0\\0 & 0 & 0\\0 & 0 & 0\end{bmatrix}\begin{bmatrix}2\\0\\0\end{bmatrix}=\begin{bmatrix}2\\0\\0\end{bmatrix}
$$

이 값이 완성 답이에요. 모든 $\mathbf x$에 대한 멱등성은 (a)의 행렬 제곱으로, 이 문제의 입력에 대한 재투영은 위 대입으로 각각 확인했어요.

#### 이 문항에서 조심할 점

둘째·셋째 성분 3과 1을 남기면 첫째 좌표축 위에 있지 않아요. 방향벡터의 길이가 1이어서 분모가 보이지 않을 뿐, 일반식의 분모를 생략하는 규칙은 아니에요.

직교투영행렬이라는 이름이 직교행렬을 뜻하지는 않아요. 여기서는 $\mathbf P^2=\mathbf P$이고, 길이를 보존하는 조건 $\mathbf P^{\mathsf T}\mathbf P=\mathbf I$를 요구하지 않아요.

#### 설명을 닫고 다시 해 봐요

1. 왜 분모가 길이가 아니라 제곱 길이인지 말하고, 숫자를 다시 계산해요.
2. 행렬·배율·투영벡터의 크기를 구별하며 세 답을 다시 써요.
3. 잔차와 방향벡터의 내적, 투영값의 재투영을 해설 없이 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

직선의 가장 가까운 점은 잔차가 방향벡터와 직교하는 점이에요.

$$
\mathbf P=\frac{\mathbf b\mathbf b^{\mathsf T}}{\mathbf b^{\mathsf T}\mathbf b}
$$

#### 첫 줄

$$
\mathbf b^{\mathsf T}\mathbf b=1
$$

#### 핵심 답

$$
\pi_U(\mathbf x)=\begin{bmatrix}2\\0\\0\end{bmatrix}
$$

#### 검산

직선 위의 점인지와 잔차의 직교를 함께 확인해요. 다시 투영한 값도 같아요.

#### 조건·구분

보통의 내적과 $\mathbf b\ne\mathbf0$에서 쓰는 식이에요. 분모는 길이의 제곱인 스칼라, 분자는 $3\times3$ 바깥곱이에요. 배율은 스칼라이고 투영벡터는 세 성분이에요. $\mathbf P^T=\mathbf P$, $\mathbf P^2=\mathbf P$인 직교투영행렬을 길이 보존 직교행렬 $\mathbf P^T\mathbf P=\mathbf I$와 구별해요.

이 문제에서는 방향벡터의 길이가 $1$이어서 분모가 $1$이에요. 일반식에서 분모를 생략하는 규칙이 아니며 첫째 성분만 남겨 $[2,0,0]^T$로 보내요.

---

<a id="p3"></a>

### P3. 직선으로 내린 그림자

MML Example 3.10 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1019_Prediction_and_Projection.html#p3)

#### 주어진 조건

보통의 내적을 사용해요. 원점을 지나는 직선 $U=\operatorname{span}(\mathbf{b})$와 벡터 $\mathbf{x}$가 주어져요.

$$
\mathbf{b}=\begin{bmatrix}0\\1\\0\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}3\\2\\1\end{bmatrix}
$$

#### 구할 것

- (a) 직선 $U$로 보내는 투영행렬 $\mathbf{P}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})=\mathbf{P}\mathbf{x}$를 구해 보세요.
- (c) $\mathbf{P}\pi_U(\mathbf{x})=\pi_U(\mathbf{x})$인지 확인해 보세요.

<details><summary>원문 보기</summary>

“Find the projection matrix” — MML Example 3.10

</details>

#### 문제를 내 말로 읽어요

공간의 점을 정해진 줄로 곧게 내려요. 먼저 이 일을 하는 표를 만들고, 주어진 점을 보낸 뒤, 한 번 더 보내도 제자리인지 확인해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘원점을 지나는 직선’과 ‘보통의 내적’이라는 조건에서 직교투영(orthogonal projection)을 떠올려요. 직선 위 점 중 원래 벡터와 거리가 가장 작은 점을 구하는 연산이에요. 둘째 좌표축으로 내리는 문제예요. 좌표의 위치를 살펴 둘째 성분 2를 보존해요.

$U=\operatorname{span}(\mathbf b)$는 $\mathbf b$의 모든 실수배를 모은 집합이에요. $\mathbf b$는 방향을 정하는 3차원 열벡터, $\mathbf x$는 옮길 벡터, $\lambda$는 직선 위 위치를 정하는 스칼라예요. 후보를 $\lambda\mathbf b$로 쓰면 잔차 $\mathbf r=\mathbf x-\lambda\mathbf b$가 직선에 수직일 때 가장 가까워요.

$$
\mathbf b^{\mathsf T}(\mathbf x-\lambda\mathbf b)=0
$$

$$
\lambda=\frac{\mathbf b^{\mathsf T}\mathbf x}{\mathbf b^{\mathsf T}\mathbf b}
$$

$$
\pi_U(\mathbf x)=\mathbf P\mathbf x,\qquad\mathbf P=\frac{\mathbf b\mathbf b^{\mathsf T}}{\mathbf b^{\mathsf T}\mathbf b}
$$

전치(transpose)는 열을 행으로 바꿔요. 분모 $\mathbf b^{\mathsf T}\mathbf b$는 $1\times1$인 제곱 길이이고, 분자 $\mathbf b\mathbf b^{\mathsf T}$는 $3\times3$ 바깥곱(outer product)이에요. 그래서 $\mathbf P$도 $3\times3$이에요. $\mathbf b\ne\mathbf0$일 때만 분모가 양수여서 이 공식을 쓸 수 있고, 이 문제의 방향벡터는 그 조건을 만족해요.

한 번 보낸 결과는 이미 직선 위에 있으므로 두 번째 투영은 결과를 바꾸지 않아요. 이 성질이 멱등성(idempotence) $\mathbf P^2=\mathbf P$예요. (c)에서는 주어진 벡터의 결과에 한 번 더 곱해 직접 확인해요.

[직선 위에서 가장 가까운 점](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1019_Prediction_and_Projection.html#s2-line)의 직교 잔차 유도와 같은 원리예요.

#### 종이에 쓸 첫 줄

$$
\mathbf b^{\mathsf T}\mathbf b=0^2+1^2+0^2=1
$$

투영행렬의 분모부터 확정해요. 다음 줄에는 방향벡터를 세로와 가로로 곱해 바깥곱을 써요. 이 첫 줄은 원래 벡터 $\mathbf x$를 아직 사용하지 않아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 투영행렬

방향벡터의 각 성분을 모든 성분에 곱해 행을 만들어요. 내적처럼 모두 더해 숫자 하나로 줄이지 않아요.

$$
\mathbf b\mathbf b^{\mathsf T}=\begin{bmatrix}0\\1\\0\end{bmatrix}\begin{bmatrix}0 & 1 & 0\end{bmatrix}=\begin{bmatrix}0 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
$$

제곱 길이 1로 각 원소를 나누면 요청한 투영행렬이에요.

$$
\boxed{\mathbf P=\begin{bmatrix}0 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}}
$$

#### (b) 투영벡터

행렬을 원래 벡터에 적용해요. 같은 계산을 먼저 내적으로 묶으면 $\mathbf b(\mathbf b^{\mathsf T}\mathbf x)/(\mathbf b^{\mathsf T}\mathbf b)$가 되어 계산량이 줄어요.

$$
\mathbf b^{\mathsf T}\mathbf x=(0)(3)+(1)(2)+(0)(1)=2
$$

$$
\lambda=\frac{2}{1}=2
$$

$$
\boxed{\pi_U(\mathbf x)=2\begin{bmatrix}0\\1\\0\end{bmatrix}=\begin{bmatrix}0\\2\\0\end{bmatrix}}
$$

배율은 숫자 하나이고 투영벡터는 그 숫자를 방향벡터에 곱한 결과예요.

#### (c) 다시 투영하기

첫 투영값 전체를 다시 입력에 넣어요. 새 방향이나 새 행렬을 구하는 일이 아니에요.

$$
\mathbf b^{\mathsf T}\pi_U(\mathbf x)=2
$$

$$
\mathbf P\pi_U(\mathbf x)=\mathbf b\frac{2}{1}
$$

$$
=2\begin{bmatrix}0\\1\\0\end{bmatrix}=\begin{bmatrix}0\\2\\0\end{bmatrix}
$$

이 결과가 (b)의 벡터와 성분별로 같으므로 물음의 등식이 성립해요.

#### 완성 답과 검산

#### (a) 행렬 확인

답의 행렬은 대칭이에요. 원소도 확인하고, 두 번의 작용이 한 번과 같은지 행렬곱으로 확인해요.

$$
\mathbf P^{\mathsf T}=\mathbf P
$$

$$
\mathbf P^2=\frac{1}{1}\begin{bmatrix}0 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
$$

$$
=\begin{bmatrix}0 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}=\mathbf P
$$

또한 $\mathbf P\mathbf b=\mathbf b$라서 방향벡터 자체를 보존해요. 분자와 분모의 곱 순서가 맞는지 점검할 수 있어요.

#### (b) 직선과 직교 조건 확인

$$
\mathbf r=\mathbf x-\pi_U(\mathbf x)=\begin{bmatrix}3\\0\\1\end{bmatrix}
$$

$$
\mathbf b^{\mathsf T}\mathbf r=0\cdot3+1\cdot0+0\cdot1=0
$$

투영값이 $2\mathbf b$로 직선 위에 있고, 잔차의 내적은 0이에요. 두 조건을 함께 만족하므로 가장 가까운 점이라는 독립적인 기하 조건도 맞아요.

#### (c) 재투영 확인

행렬로 직접 곱한 값도 확인해요.

$$
\mathbf P\pi_U(\mathbf x)=\begin{bmatrix}0 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}\begin{bmatrix}0\\2\\0\end{bmatrix}=\begin{bmatrix}0\\2\\0\end{bmatrix}
$$

이 값이 완성 답이에요. 모든 $\mathbf x$에 대한 멱등성은 (a)의 행렬 제곱으로, 이 문제의 입력에 대한 재투영은 위 대입으로 각각 확인했어요.

#### 이 문항에서 조심할 점

방향벡터의 1은 둘째 자리에 있어요. $\operatorname{diag}(1,0,0)$으로 쓰면 첫째 축에 보내는 다른 행렬이 돼요. 결과가 $(2,0,0)^{\mathsf T}$가 아니라 $(0,2,0)^{\mathsf T}$인지 위치까지 확인해요.

직교투영행렬이라는 이름이 직교행렬을 뜻하지는 않아요. 여기서는 $\mathbf P^2=\mathbf P$이고, 길이를 보존하는 조건 $\mathbf P^{\mathsf T}\mathbf P=\mathbf I$를 요구하지 않아요.

#### 설명을 닫고 다시 해 봐요

1. 왜 분모가 길이가 아니라 제곱 길이인지 말하고, 숫자를 다시 계산해요.
2. 행렬·배율·투영벡터의 크기를 구별하며 세 답을 다시 써요.
3. 잔차와 방향벡터의 내적, 투영값의 재투영을 해설 없이 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

직선의 가장 가까운 점은 잔차가 방향벡터와 직교하는 점이에요.

$$
\mathbf P=\frac{\mathbf b\mathbf b^{\mathsf T}}{\mathbf b^{\mathsf T}\mathbf b}
$$

#### 첫 줄

$$
\mathbf b^{\mathsf T}\mathbf b=1
$$

#### 핵심 답

$$
\pi_U(\mathbf x)=\begin{bmatrix}0\\2\\0\end{bmatrix}
$$

#### 검산

직선 위의 점인지와 잔차의 직교를 함께 확인해요. 다시 투영한 값도 같아요.

#### 조건·구분

보통의 내적과 $\mathbf b\ne\mathbf0$에서 쓰는 식이에요. 분모는 길이의 제곱인 스칼라, 분자는 $3\times3$ 바깥곱이에요. 배율은 스칼라이고 투영벡터는 세 성분이에요. $\mathbf P^T=\mathbf P$, $\mathbf P^2=\mathbf P$인 직교투영행렬을 길이 보존 직교행렬 $\mathbf P^T\mathbf P=\mathbf I$와 구별해요.

방향벡터의 $1$이 둘째 자리에 있으므로 $\mathbf P=\operatorname{diag}(0,1,0)$이고 결과는 $[0,2,0]^T$예요. 첫째 축의 $\operatorname{diag}(1,0,0)$와 구별해요.

---

<a id="p4"></a>

### P4. 직선으로 내린 그림자

MML Example 3.10 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1019_Prediction_and_Projection.html#p4)

#### 주어진 조건

보통의 내적을 사용해요. 원점을 지나는 직선 $U=\operatorname{span}(\mathbf{b})$와 벡터 $\mathbf{x}$가 주어져요.

$$
\mathbf{b}=\begin{bmatrix}1\\1\\1\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}3\\3\\3\end{bmatrix}
$$

#### 구할 것

- (a) 직선 $U$로 보내는 투영행렬 $\mathbf{P}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})=\mathbf{P}\mathbf{x}$를 구해 보세요.
- (c) $\mathbf{P}\pi_U(\mathbf{x})=\pi_U(\mathbf{x})$인지 확인해 보세요.

<details><summary>원문 보기</summary>

“Find the projection matrix” — MML Example 3.10

</details>

#### 문제를 내 말로 읽어요

공간의 점을 정해진 줄로 곧게 내려요. 먼저 이 일을 하는 표를 만들고, 주어진 점을 보낸 뒤, 한 번 더 보내도 제자리인지 확인해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘원점을 지나는 직선’과 ‘보통의 내적’이라는 조건에서 직교투영(orthogonal projection)을 떠올려요. 직선 위 점 중 원래 벡터와 거리가 가장 작은 점을 구하는 연산이에요. 주어진 점은 이미 방향벡터의 3배예요. 직선 위의 점은 옮기지 않는다는 사실을 예상하고 계산해요.

$U=\operatorname{span}(\mathbf b)$는 $\mathbf b$의 모든 실수배를 모은 집합이에요. $\mathbf b$는 방향을 정하는 3차원 열벡터, $\mathbf x$는 옮길 벡터, $\lambda$는 직선 위 위치를 정하는 스칼라예요. 후보를 $\lambda\mathbf b$로 쓰면 잔차 $\mathbf r=\mathbf x-\lambda\mathbf b$가 직선에 수직일 때 가장 가까워요.

$$
\mathbf b^{\mathsf T}(\mathbf x-\lambda\mathbf b)=0
$$

$$
\lambda=\frac{\mathbf b^{\mathsf T}\mathbf x}{\mathbf b^{\mathsf T}\mathbf b}
$$

$$
\pi_U(\mathbf x)=\mathbf P\mathbf x,\qquad\mathbf P=\frac{\mathbf b\mathbf b^{\mathsf T}}{\mathbf b^{\mathsf T}\mathbf b}
$$

전치(transpose)는 열을 행으로 바꿔요. 분모 $\mathbf b^{\mathsf T}\mathbf b$는 $1\times1$인 제곱 길이이고, 분자 $\mathbf b\mathbf b^{\mathsf T}$는 $3\times3$ 바깥곱(outer product)이에요. 그래서 $\mathbf P$도 $3\times3$이에요. $\mathbf b\ne\mathbf0$일 때만 분모가 양수여서 이 공식을 쓸 수 있고, 이 문제의 방향벡터는 그 조건을 만족해요.

한 번 보낸 결과는 이미 직선 위에 있으므로 두 번째 투영은 결과를 바꾸지 않아요. 이 성질이 멱등성(idempotence) $\mathbf P^2=\mathbf P$예요. (c)에서는 주어진 벡터의 결과에 한 번 더 곱해 직접 확인해요.

[직선 위에서 가장 가까운 점](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1019_Prediction_and_Projection.html#s2-line)의 직교 잔차 유도와 같은 원리예요.

#### 종이에 쓸 첫 줄

$$
\mathbf b^{\mathsf T}\mathbf b=1^2+1^2+1^2=3
$$

투영행렬의 분모부터 확정해요. 다음 줄에는 방향벡터를 세로와 가로로 곱해 바깥곱을 써요. 이 첫 줄은 원래 벡터 $\mathbf x$를 아직 사용하지 않아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 투영행렬

방향벡터의 각 성분을 모든 성분에 곱해 행을 만들어요. 내적처럼 모두 더해 숫자 하나로 줄이지 않아요.

$$
\mathbf b\mathbf b^{\mathsf T}=\begin{bmatrix}1\\1\\1\end{bmatrix}\begin{bmatrix}1 & 1 & 1\end{bmatrix}=\begin{bmatrix}1 & 1 & 1\\1 & 1 & 1\\1 & 1 & 1\end{bmatrix}
$$

제곱 길이 3으로 각 원소를 나누면 요청한 투영행렬이에요.

$$
\boxed{\mathbf P=\frac{1}{3}\begin{bmatrix}1 & 1 & 1\\1 & 1 & 1\\1 & 1 & 1\end{bmatrix}}
$$

#### (b) 투영벡터

행렬을 원래 벡터에 적용해요. 같은 계산을 먼저 내적으로 묶으면 $\mathbf b(\mathbf b^{\mathsf T}\mathbf x)/(\mathbf b^{\mathsf T}\mathbf b)$가 되어 계산량이 줄어요.

$$
\mathbf b^{\mathsf T}\mathbf x=(1)(3)+(1)(3)+(1)(3)=9
$$

$$
\lambda=\frac{9}{3}=3
$$

$$
\boxed{\pi_U(\mathbf x)=3\begin{bmatrix}1\\1\\1\end{bmatrix}=\begin{bmatrix}3\\3\\3\end{bmatrix}}
$$

배율은 숫자 하나이고 투영벡터는 그 숫자를 방향벡터에 곱한 결과예요.

#### (c) 다시 투영하기

첫 투영값 전체를 다시 입력에 넣어요. 새 방향이나 새 행렬을 구하는 일이 아니에요.

$$
\mathbf b^{\mathsf T}\pi_U(\mathbf x)=9
$$

$$
\mathbf P\pi_U(\mathbf x)=\mathbf b\frac{9}{3}
$$

$$
=3\begin{bmatrix}1\\1\\1\end{bmatrix}=\begin{bmatrix}3\\3\\3\end{bmatrix}
$$

이 결과가 (b)의 벡터와 성분별로 같으므로 물음의 등식이 성립해요.

#### 완성 답과 검산

#### (a) 행렬 확인

답의 행렬은 대칭이에요. 원소도 확인하고, 두 번의 작용이 한 번과 같은지 행렬곱으로 확인해요.

$$
\mathbf P^{\mathsf T}=\mathbf P
$$

$$
\mathbf P^2=\frac{1}{9}\begin{bmatrix}3 & 3 & 3\\3 & 3 & 3\\3 & 3 & 3\end{bmatrix}
$$

$$
=\frac{1}{3}\begin{bmatrix}1 & 1 & 1\\1 & 1 & 1\\1 & 1 & 1\end{bmatrix}=\mathbf P
$$

또한 $\mathbf P\mathbf b=\mathbf b$라서 방향벡터 자체를 보존해요. 분자와 분모의 곱 순서가 맞는지 점검할 수 있어요.

#### (b) 직선과 직교 조건 확인

$$
\mathbf r=\mathbf x-\pi_U(\mathbf x)=\begin{bmatrix}0\\0\\0\end{bmatrix}
$$

$$
\mathbf b^{\mathsf T}\mathbf r=1\cdot0+1\cdot0+1\cdot0=0
$$

투영값이 $3\mathbf b$로 직선 위에 있고, 잔차의 내적은 0이에요. 두 조건을 함께 만족하므로 가장 가까운 점이라는 독립적인 기하 조건도 맞아요.

잔차가 영벡터이므로 거리는 0이에요. 이미 직선 위에 있던 입력이라는 예상과 일치해요.

#### (c) 재투영 확인

행렬로 직접 곱한 값도 확인해요.

$$
\mathbf P\pi_U(\mathbf x)=\frac{1}{3}\begin{bmatrix}1 & 1 & 1\\1 & 1 & 1\\1 & 1 & 1\end{bmatrix}\begin{bmatrix}3\\3\\3\end{bmatrix}=\begin{bmatrix}3\\3\\3\end{bmatrix}
$$

이 값이 완성 답이에요. 모든 $\mathbf x$에 대한 멱등성은 (a)의 행렬 제곱으로, 이 문제의 입력에 대한 재투영은 위 대입으로 각각 확인했어요.

#### 이 문항에서 조심할 점

이 벡터 하나가 그대로 남았다고 해서 $\mathbf P=\mathbf I$라고 하면 안 돼요. 예를 들어 $(1,0,0)^{\mathsf T}$는 $(1/3,1/3,1/3)^{\mathsf T}$로 바뀌므로 모든 벡터를 보존하는 항등행렬은 아니에요.

직교투영행렬이라는 이름이 직교행렬을 뜻하지는 않아요. 여기서는 $\mathbf P^2=\mathbf P$이고, 길이를 보존하는 조건 $\mathbf P^{\mathsf T}\mathbf P=\mathbf I$를 요구하지 않아요.

#### 설명을 닫고 다시 해 봐요

1. 왜 분모가 길이가 아니라 제곱 길이인지 말하고, 숫자를 다시 계산해요.
2. 행렬·배율·투영벡터의 크기를 구별하며 세 답을 다시 써요.
3. 잔차와 방향벡터의 내적, 투영값의 재투영을 해설 없이 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

직선의 가장 가까운 점은 잔차가 방향벡터와 직교하는 점이에요.

$$
\mathbf P=\frac{\mathbf b\mathbf b^{\mathsf T}}{\mathbf b^{\mathsf T}\mathbf b}
$$

#### 첫 줄

$$
\mathbf b^{\mathsf T}\mathbf b=3
$$

#### 핵심 답

$$
\pi_U(\mathbf x)=\begin{bmatrix}3\\3\\3\end{bmatrix}
$$

#### 검산

직선 위의 점인지와 잔차의 직교를 함께 확인해요. 다시 투영한 값도 같아요.

#### 조건·구분

보통의 내적과 $\mathbf b\ne\mathbf0$에서 쓰는 식이에요. 분모는 길이의 제곱인 스칼라, 분자는 $3\times3$ 바깥곱이에요. 배율은 스칼라이고 투영벡터는 세 성분이에요. $\mathbf P^T=\mathbf P$, $\mathbf P^2=\mathbf P$인 직교투영행렬을 길이 보존 직교행렬 $\mathbf P^T\mathbf P=\mathbf I$와 구별해요.

$\mathbf x=3\mathbf b$여서 잔차가 $0$인 특별한 입력이에요. 이 벡터가 그대로 남아도 $\mathbf P=\mathbf I$는 아니며, $[1,0,0]^T$는 $[1/3,1/3,1/3]^T$로 바뀌어요.

---

<a id="p5"></a>

### P5. 평면에 가장 가까운 점

MML Example 3.11 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1019_Prediction_and_Projection.html#p5)

#### 주어진 조건

보통의 내적을 사용해요. $\mathbf{B}$의 두 열벡터가 평면 $U$의 기저예요. $U=\operatorname{span}(\mathbf{b}_1,\mathbf{b}_2)$로 두어요.

$$
\mathbf{B}=[\mathbf{b}_1\ \mathbf{b}_2]=\begin{bmatrix}1 & 0\\1 & 1\\1 & 2\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}6\\0\\0\end{bmatrix}
$$

#### 구할 것

- (a) 이 기저에 대한 투영벡터의 좌표 $\boldsymbol{\lambda}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})$와 투영오차 $\|\mathbf{x}-\pi_U(\mathbf{x})\|$를 구해 보세요.
- (c) 투영행렬 $\mathbf{P}$를 구해 보세요.
- (d) 차이벡터가 두 기저벡터에 직교하는지, $\mathbf{P}^2=\mathbf{P}$인지 확인해 보세요.

<details><summary>원문 보기</summary>

“find the coordinates” — MML Example 3.11

</details>

#### 무엇을 구하는 문제인가요

두 방향으로 펼친 평면 안에서 목표점과 가장 가까운 자리를 찾아요. 먼저 두 방향을 얼마씩 섞을지 정하고, 그 결과가 목표와 얼마나 떨어졌는지 확인해요.

(a)는 두 개의 좌표, (b)는 세 성분의 투영벡터와 거리, (c)는 모든 입력에 적용하는 행렬, (d)는 직교성과 반복 투영의 성질을 물어요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

문제의 ‘기저’, ‘평면’, ‘투영’이라는 단서에서 **직교투영(orthogonal projection)**을 떠올려요. 기저(basis)는 이 평면의 모든 점을 유일하게 표현하는 두 독립 방향이에요. 투영은 평면 위에서 목표와 거리가 가장 가까운 점을 고르는 일이에요.

$\mathbf B$는 두 기저를 열로 모은 $3\times2$ 행렬이고, $\mathbf x$는 목표인 $3\times1$ 벡터예요. $\boldsymbol\lambda=(\lambda_1,\lambda_2)^{\mathsf T}$는 섞는 양 두 개, $\mathbf q=\mathbf B\boldsymbol\lambda$는 평면 위의 $3\times1$ 점이에요. 가장 가까울 때 잔차 $\mathbf r=\mathbf x-\mathbf q$가 두 기저 모두와 직교해야 해요.

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\mathbf0
$$

$$
\mathbf B^{\mathsf T}\mathbf B\boldsymbol\lambda=\mathbf B^{\mathsf T}\mathbf x
$$

이 식을 **정규방정식(normal equation)**이라고 해요. 기저 열이 독립이므로 $\mathbf G=\mathbf B^{\mathsf T}\mathbf B$는 가역이고, 이 식으로 좌표를 구할 수 있어요. $\mathbf B$ 자체는 정사각행렬이 아니므로 $\mathbf B^{-1}$를 쓰는 방법은 맞지 않아요.

$$
\boldsymbol\lambda=(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}\mathbf x
$$

(b)의 ‘오차’는 차이벡터 자체나 제곱거리와 구별해요. Euclidean norm(유클리드 노름)은 성분 제곱의 합에 제곱근을 취한 길이예요.

$$
\|\mathbf r\|=\sqrt{r_1^2+r_2^2+r_3^2}
$$

(c)는 이 과정을 임의의 목표에 적용할 **투영행렬(projection matrix)**을 물어요. 좌표를 구하는 $2\times3$ 유사역행렬(pseudo-inverse) 앞에 기저를 곱해 원래의 세 성분으로 되돌려요.

$$
\mathbf B^+=(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}
$$

$$
\mathbf P=\mathbf B\mathbf B^+\in\mathbb R^{3\times3}
$$

(d)의 직교는 내적이 0이라는 뜻이에요. 멱등성(idempotence) $\mathbf P^2=\mathbf P$는 이미 평면 위로 보낸 벡터를 다시 투영해도 바뀌지 않는다는 뜻이에요. 한 벡터에서만 같은지 보는 대신 행렬 전체의 성질을 확인해야 해요.

#### 종이에 적을 첫 줄

종이에 가장 먼저 ‘평면 위 후보는 $\mathbf q=\mathbf B\boldsymbol\lambda$’라고 써요. 이제 수직 조건을 두 행의 연립방정식으로 만들기 위해 전치를 적어요.

$$
\mathbf B^{\mathsf T}=\begin{bmatrix}1 & 1 & 1\\0 & 1 & 2\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\begin{bmatrix}0\\0\end{bmatrix}
$$

전치(transpose)는 행과 열을 바꾸는 연산이에요. $2\times3$ 전치에 $3\times1$ 잔차를 곱하므로 기저마다 하나씩, 조건 두 개가 나와요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 기저 좌표

두 행의 내적을 계산해 $2\times2$ 계수행렬과 $2\times1$ 우변을 만들어요.

$$
\mathbf G=\mathbf B^{\mathsf T}\mathbf B=\begin{bmatrix}3 & 3\\3 & 5\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}\mathbf x=\begin{bmatrix}6\\0\end{bmatrix}
$$

$$
\begin{bmatrix}3 & 3\\3 & 5\end{bmatrix}\begin{bmatrix}\lambda_1\\\lambda_2\end{bmatrix}=\begin{bmatrix}6\\0\end{bmatrix}
$$

둘째 행에서 첫째 행을 빼면 첫 좌표가 사라져요. 둘째 좌표를 구한 뒤 첫째 행에 넣어요.

$$
3\lambda_1+3\lambda_2=6
$$

$$
3\lambda_1+5\lambda_2=0
$$

$$
2\lambda_2=-6
$$

$$
\lambda_2=-3
$$

$$
3\lambda_1-9=6
$$

$$
\lambda_1=5
$$

$$
\boldsymbol\lambda=\begin{bmatrix}5\\-3\end{bmatrix}
$$

#### (b) 투영과 오차

좌표 두 개는 배율이에요. 각 기저벡터에 그 배율을 곱해 더하면 원래의 세 성분을 가진 점이 나와요.

$$
\mathbf q=\mathbf B\boldsymbol\lambda=\begin{bmatrix}1 & 0\\1 & 1\\1 & 2\end{bmatrix}\begin{bmatrix}5\\-3\end{bmatrix}
$$

$$
\mathbf q=\begin{bmatrix}5\\2\\-1\end{bmatrix}
$$

$$
\mathbf r=\mathbf x-\mathbf q=\begin{bmatrix}6\\0\\0\end{bmatrix}-\begin{bmatrix}5\\2\\-1\end{bmatrix}
$$

$$
\mathbf r=\begin{bmatrix}1\\-2\\1\end{bmatrix}
$$

오차는 세 성분을 더한 값이 아니라 길이예요. 음수 성분도 제곱하면 양수가 돼요.

$$
\|\mathbf r\|^2=(1)^2+(-2)^2+(1)^2=6
$$

$$
\|\mathbf r\|=\sqrt{6}
$$

#### (c) 투영행렬

이제 목표 $\mathbf x$가 바뀌어도 쓸 수 있는 행렬을 만들어요. $2\times2$ 역행렬 공식을 적용할 때 대각 성분을 맞바꾸고 나머지 두 성분의 부호를 바꿔 행렬식으로 나눠요.

$$
\det\mathbf G=(3)(5)-(3)(3)=6
$$

$$
\mathbf G^{-1}=\frac{1}{6}\begin{bmatrix}5 & -3\\-3 & 3\end{bmatrix}
$$

오른쪽의 전치부터 곱해 $2\times3$ 유사역행렬을 구하고, 왼쪽에 기저를 곱해 $3\times3$ 투영행렬을 만들어요. 곱 순서를 유지해야 차원도 맞아요.

$$
\mathbf B^+=\mathbf G^{-1}\mathbf B^{\mathsf T}=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\-3 & 0 & 3\end{bmatrix}
$$

$$
\mathbf P=\mathbf B\mathbf B^+=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}
$$

#### (d) 직교성과 반복 투영

먼저 차이벡터가 각 기저와 직교하는지 실제 내적으로 확인해요.

$$
\mathbf b_1^{\mathsf T}\mathbf r=(1)(1)+(1)(-2)+(1)(1)=0
$$

$$
\mathbf b_2^{\mathsf T}\mathbf r=(0)(1)+(1)(-2)+(2)(1)=0
$$

$\mathbf q-\mathbf x=-\mathbf r$를 써도 내적은 여전히 0이에요. 다음은 평면 위의 모든 점이 그대로 남는다는 것을 확인해요.

$$
\mathbf P\mathbf B=\mathbf B\mathbf G^{-1}(\mathbf B^{\mathsf T}\mathbf B)
$$

$$
\mathbf P\mathbf B=\mathbf B\mathbf G^{-1}\mathbf G=\mathbf B
$$

어떤 입력을 한 번 투영한 결과도 $\mathbf B$의 열들의 조합이에요. 따라서 다시 투영하면 바뀌지 않아요.

$$
\mathbf P^2=(\mathbf P\mathbf B)\mathbf G^{-1}\mathbf B^{\mathsf T}
$$

$$
\mathbf P^2=\mathbf B\mathbf G^{-1}\mathbf B^{\mathsf T}=\mathbf P
$$

이 계산은 특정 목표점 하나가 아니라 행렬 전체에 대한 증명이에요. 또 $\mathbf G^{-1}$가 대칭이므로 $\mathbf P^{\mathsf T}=\mathbf P$예요. 이 대칭성과 수직 잔차가 직교투영의 성질과 일치해요.

#### 완성 답과 검산

#### (a) 좌표 검산

답인 좌표를 원래 두 행의 식에 다시 넣어요. 좌변이 계산했던 우변과 정확히 같아요.

$$
\begin{bmatrix}3 & 3\\3 & 5\end{bmatrix}\begin{bmatrix}5\\-3\end{bmatrix}=\begin{bmatrix}6\\0\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}\mathbf x=\begin{bmatrix}6\\0\end{bmatrix}
$$

$$
\boldsymbol\lambda=\begin{bmatrix}5\\-3\end{bmatrix}
$$

#### (b) 투영과 거리 검산

좌표로 만든 점과 행렬로 만든 점을 서로 다른 곱으로 비교해요.

$$
\mathbf P\mathbf x=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}\begin{bmatrix}6\\0\\0\end{bmatrix}
$$

$$
\mathbf P\mathbf x=\begin{bmatrix}5\\2\\-1\end{bmatrix}=\mathbf q
$$

$$
\|\mathbf x-\mathbf q\|^2=6
$$

$$
\|\mathbf x-\mathbf q\|=\sqrt{6}
$$

평면 위 임의의 다른 점 $\mathbf z$를 잡으면 잔차와 평면 내 차이가 수직이에요. 그래서 아래 식의 둘째 항은 음수가 될 수 없고, 지금 점이 최단거리라는 뜻도 확인돼요.

$$
\|\mathbf x-\mathbf z\|^2=\|\mathbf x-\mathbf q\|^2+\|\mathbf q-\mathbf z\|^2
$$

#### (c) 행렬 검산

투영행렬이 각 기저를 그대로 두는지 실제 숫자로 확인해요. 이는 두 열 전체에 대한 검사예요.

$$
\mathbf P\mathbf B=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}\begin{bmatrix}1 & 0\\1 & 1\\1 & 2\end{bmatrix}
$$

$$
\mathbf P\mathbf B=\begin{bmatrix}1 & 0\\1 & 1\\1 & 2\end{bmatrix}=\mathbf B
$$

또한 수치 행렬의 행과 열을 바꾸어도 같아서 $\mathbf P^{\mathsf T}=\mathbf P$예요. 최종 투영행렬은 다음과 같아요.

$$
\mathbf P=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}
$$

#### (d) 전체 행렬의 멱등성 검산

직교성은 성분별 내적으로, 멱등성은 $3\times3$ 전체 곱으로 별도 확인해요.

$$
\mathbf B^{\mathsf T}\mathbf r=\begin{bmatrix}0\\0\end{bmatrix}
$$

$$
\mathbf M=\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}
$$

$$
\mathbf M^2=\begin{bmatrix}30 & 12 & -6\\12 & 12 & 12\\-6 & 12 & 30\end{bmatrix}
$$

$$
\mathbf M^2=6\mathbf M
$$

$$
\mathbf P^2=\frac{\mathbf M^2}{36}=\frac{\mathbf M}{6}=\mathbf P
$$

따라서 직교성과 $\mathbf P^2=\mathbf P$가 모두 성립해요. 단지 이 문제의 목표점에서만 두 번의 결과가 같은지를 확인한 것이 아니에요.

#### 여기서 헷갈리기 쉬워요

좌표는 두 성분, 투영은 세 성분이에요. $\boldsymbol\lambda$를 최종 투영벡터라고 쓰면 서로 다른 공간을 섞게 돼요. 기저가 정규직교라고 주어지지 않았다면 $\boldsymbol\lambda=\mathbf B^{\mathsf T}\mathbf x$를 바로 쓸 수 없어요.

오차와 제곱오차를 구별해 마지막 제곱근을 확인해요. 대칭행렬이라는 사실 하나만으로 멱등성이 따라오지는 않아요. $\mathbf P^2=\mathbf P$는 전체 행렬곱이나 위의 대수 증명으로 확인해야 해요.

#### 설명을 닫고 다시 해 봐요

1. 설명을 닫고 왜 $\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=0$부터 쓰는지 말해 보세요.
2. 좌표 두 개, 투영의 세 성분, 오차를 직접 다시 구해 보세요.
3. 한 목표벡터만 쓰지 않고 $\mathbf P^2=\mathbf P$를 보이는 식을 써 보세요.

**페이지 요약**

#### 첫 줄

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\mathbf0
$$

#### 떠올릴 개념·공식

기저의 배율은 정규방정식으로, 가장 가까운 점은 직교투영으로 구해요.

$$
\mathbf P=\mathbf B(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}
$$

#### 완성 답

$$
\boldsymbol\lambda=\begin{bmatrix}5\\-3\end{bmatrix}
$$

$$
\pi_U(\mathbf x)=\begin{bmatrix}5\\2\\-1\end{bmatrix}
$$

$$
\|\mathbf r\|=\sqrt{6}
$$

#### 검산

기저와 잔차의 내적은 0, 전체 행렬은 $\mathbf P^2=\mathbf P$예요.

#### 조건·구분

$\mathbf B\in\mathbb R^{3\times2}$의 독립 기저 열과 보통의 내적을 전제해요. $\mathbf B$ 자체의 역행렬은 쓰지 않아요. 좌표는 두 성분, 투영은 세 성분이고, $\mathbf B^+$는 $2\times3$, $\mathbf P$는 $3\times3$이에요. 기저가 정규직교임을 확인하지 않고 $\boldsymbol\lambda=\mathbf B^T\mathbf x$를 쓰면 안 돼요.

오차는 잔차의 노름이고 제곱오차와 구별해요. 직교 잔차의 피타고라스 분해가 최소거리를 보장해요. 대칭성이나 벡터 하나의 재투영만으로 전체 멱등성을 증명하지 않고 행렬곱으로 $\mathbf P^2=\mathbf P$를 확인해요.

---

<a id="p6"></a>

### P6. 평면에 가장 가까운 점

MML Example 3.11 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1019_Prediction_and_Projection.html#p6)

#### 주어진 조건

보통의 내적을 사용해요. $\mathbf{B}$의 두 열벡터가 평면 $U$의 기저예요. $U=\operatorname{span}(\mathbf{b}_1,\mathbf{b}_2)$로 두어요.

$$
\mathbf{B}=[\mathbf{b}_1\ \mathbf{b}_2]=\begin{bmatrix}1 & 0\\0 & 1\\0 & 0\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}2\\3\\4\end{bmatrix}
$$

#### 구할 것

- (a) 이 기저에 대한 투영벡터의 좌표 $\boldsymbol{\lambda}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})$와 투영오차 $\|\mathbf{x}-\pi_U(\mathbf{x})\|$를 구해 보세요.
- (c) 투영행렬 $\mathbf{P}$를 구해 보세요.
- (d) 차이벡터가 두 기저벡터에 직교하는지, $\mathbf{P}^2=\mathbf{P}$인지 확인해 보세요.

<details><summary>원문 보기</summary>

“find the coordinates” — MML Example 3.11

</details>

#### 무엇을 구하는 문제인가요

두 방향으로 펼친 평면 안에서 목표점과 가장 가까운 자리를 찾아요. 먼저 두 방향을 얼마씩 섞을지 정하고, 그 결과가 목표와 얼마나 떨어졌는지 확인해요.

(a)는 두 개의 좌표, (b)는 세 성분의 투영벡터와 거리, (c)는 모든 입력에 적용하는 행렬, (d)는 직교성과 반복 투영의 성질을 물어요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

문제의 ‘기저’, ‘평면’, ‘투영’이라는 단서에서 **직교투영(orthogonal projection)**을 떠올려요. 기저(basis)는 이 평면의 모든 점을 유일하게 표현하는 두 독립 방향이에요. 투영은 평면 위에서 목표와 거리가 가장 가까운 점을 고르는 일이에요.

$\mathbf B$는 두 기저를 열로 모은 $3\times2$ 행렬이고, $\mathbf x$는 목표인 $3\times1$ 벡터예요. $\boldsymbol\lambda=(\lambda_1,\lambda_2)^{\mathsf T}$는 섞는 양 두 개, $\mathbf q=\mathbf B\boldsymbol\lambda$는 평면 위의 $3\times1$ 점이에요. 가장 가까울 때 잔차 $\mathbf r=\mathbf x-\mathbf q$가 두 기저 모두와 직교해야 해요.

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\mathbf0
$$

$$
\mathbf B^{\mathsf T}\mathbf B\boldsymbol\lambda=\mathbf B^{\mathsf T}\mathbf x
$$

이 식을 **정규방정식(normal equation)**이라고 해요. 기저 열이 독립이므로 $\mathbf G=\mathbf B^{\mathsf T}\mathbf B$는 가역이고, 이 식으로 좌표를 구할 수 있어요. $\mathbf B$ 자체는 정사각행렬이 아니므로 $\mathbf B^{-1}$를 쓰는 방법은 맞지 않아요.

$$
\boldsymbol\lambda=(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}\mathbf x
$$

(b)의 ‘오차’는 차이벡터 자체나 제곱거리와 구별해요. Euclidean norm(유클리드 노름)은 성분 제곱의 합에 제곱근을 취한 길이예요.

$$
\|\mathbf r\|=\sqrt{r_1^2+r_2^2+r_3^2}
$$

(c)는 이 과정을 임의의 목표에 적용할 **투영행렬(projection matrix)**을 물어요. 좌표를 구하는 $2\times3$ 유사역행렬(pseudo-inverse) 앞에 기저를 곱해 원래의 세 성분으로 되돌려요.

$$
\mathbf B^+=(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}
$$

$$
\mathbf P=\mathbf B\mathbf B^+\in\mathbb R^{3\times3}
$$

(d)의 직교는 내적이 0이라는 뜻이에요. 멱등성(idempotence) $\mathbf P^2=\mathbf P$는 이미 평면 위로 보낸 벡터를 다시 투영해도 바뀌지 않는다는 뜻이에요. 한 벡터에서만 같은지 보는 대신 행렬 전체의 성질을 확인해야 해요.

#### 종이에 적을 첫 줄

종이에 가장 먼저 ‘평면 위 후보는 $\mathbf q=\mathbf B\boldsymbol\lambda$’라고 써요. 이제 수직 조건을 두 행의 연립방정식으로 만들기 위해 전치를 적어요.

$$
\mathbf B^{\mathsf T}=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\begin{bmatrix}0\\0\end{bmatrix}
$$

전치(transpose)는 행과 열을 바꾸는 연산이에요. $2\times3$ 전치에 $3\times1$ 잔차를 곱하므로 기저마다 하나씩, 조건 두 개가 나와요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 기저 좌표

두 행의 내적을 계산해 $2\times2$ 계수행렬과 $2\times1$ 우변을 만들어요.

$$
\mathbf G=\mathbf B^{\mathsf T}\mathbf B=\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}\mathbf x=\begin{bmatrix}2\\3\end{bmatrix}
$$

$$
\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}\begin{bmatrix}\lambda_1\\\lambda_2\end{bmatrix}=\begin{bmatrix}2\\3\end{bmatrix}
$$

계수행렬이 단위행렬이라 각 좌표를 바로 읽을 수 있어요.

$$
\lambda_1=2
$$

$$
\lambda_2=3
$$

$$
\boldsymbol\lambda=\begin{bmatrix}2\\3\end{bmatrix}
$$

#### (b) 투영과 오차

좌표 두 개는 배율이에요. 각 기저벡터에 그 배율을 곱해 더하면 원래의 세 성분을 가진 점이 나와요.

$$
\mathbf q=\mathbf B\boldsymbol\lambda=\begin{bmatrix}1 & 0\\0 & 1\\0 & 0\end{bmatrix}\begin{bmatrix}2\\3\end{bmatrix}
$$

$$
\mathbf q=\begin{bmatrix}2\\3\\0\end{bmatrix}
$$

$$
\mathbf r=\mathbf x-\mathbf q=\begin{bmatrix}2\\3\\4\end{bmatrix}-\begin{bmatrix}2\\3\\0\end{bmatrix}
$$

$$
\mathbf r=\begin{bmatrix}0\\0\\4\end{bmatrix}
$$

오차는 세 성분을 더한 값이 아니라 길이예요. 음수 성분도 제곱하면 양수가 돼요.

$$
\|\mathbf r\|^2=(0)^2+(0)^2+(4)^2=16
$$

$$
\|\mathbf r\|=4
$$

#### (c) 투영행렬

이제 목표 $\mathbf x$가 바뀌어도 쓸 수 있는 행렬을 만들어요. $2\times2$ 역행렬 공식을 적용할 때 대각 성분을 맞바꾸고 나머지 두 성분의 부호를 바꿔 행렬식으로 나눠요.

$$
\det\mathbf G=(1)(1)-(0)(0)=1
$$

$$
\mathbf G^{-1}=\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}
$$

오른쪽의 전치부터 곱해 $2\times3$ 유사역행렬을 구하고, 왼쪽에 기저를 곱해 $3\times3$ 투영행렬을 만들어요. 곱 순서를 유지해야 차원도 맞아요.

$$
\mathbf B^+=\mathbf G^{-1}\mathbf B^{\mathsf T}=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\end{bmatrix}
$$

$$
\mathbf P=\mathbf B\mathbf B^+=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
$$

#### (d) 직교성과 반복 투영

먼저 차이벡터가 각 기저와 직교하는지 실제 내적으로 확인해요.

$$
\mathbf b_1^{\mathsf T}\mathbf r=(1)(0)+(0)(0)+(0)(4)=0
$$

$$
\mathbf b_2^{\mathsf T}\mathbf r=(0)(0)+(1)(0)+(0)(4)=0
$$

$\mathbf q-\mathbf x=-\mathbf r$를 써도 내적은 여전히 0이에요. 다음은 평면 위의 모든 점이 그대로 남는다는 것을 확인해요.

$$
\mathbf P\mathbf B=\mathbf B\mathbf G^{-1}(\mathbf B^{\mathsf T}\mathbf B)
$$

$$
\mathbf P\mathbf B=\mathbf B\mathbf G^{-1}\mathbf G=\mathbf B
$$

어떤 입력을 한 번 투영한 결과도 $\mathbf B$의 열들의 조합이에요. 따라서 다시 투영하면 바뀌지 않아요.

$$
\mathbf P^2=(\mathbf P\mathbf B)\mathbf G^{-1}\mathbf B^{\mathsf T}
$$

$$
\mathbf P^2=\mathbf B\mathbf G^{-1}\mathbf B^{\mathsf T}=\mathbf P
$$

이 계산은 특정 목표점 하나가 아니라 행렬 전체에 대한 증명이에요. 또 $\mathbf G^{-1}$가 대칭이므로 $\mathbf P^{\mathsf T}=\mathbf P$예요. 이 대칭성과 수직 잔차가 직교투영의 성질과 일치해요.

#### 완성 답과 검산

#### (a) 좌표 검산

답인 좌표를 원래 두 행의 식에 다시 넣어요. 좌변이 계산했던 우변과 정확히 같아요.

$$
\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}\begin{bmatrix}2\\3\end{bmatrix}=\begin{bmatrix}2\\3\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}\mathbf x=\begin{bmatrix}2\\3\end{bmatrix}
$$

$$
\boldsymbol\lambda=\begin{bmatrix}2\\3\end{bmatrix}
$$

#### (b) 투영과 거리 검산

좌표로 만든 점과 행렬로 만든 점을 서로 다른 곱으로 비교해요.

$$
\mathbf P\mathbf x=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}\begin{bmatrix}2\\3\\4\end{bmatrix}
$$

$$
\mathbf P\mathbf x=\begin{bmatrix}2\\3\\0\end{bmatrix}=\mathbf q
$$

$$
\|\mathbf x-\mathbf q\|^2=16
$$

$$
\|\mathbf x-\mathbf q\|=4
$$

평면 위 임의의 다른 점 $\mathbf z$를 잡으면 잔차와 평면 내 차이가 수직이에요. 그래서 아래 식의 둘째 항은 음수가 될 수 없고, 지금 점이 최단거리라는 뜻도 확인돼요.

$$
\|\mathbf x-\mathbf z\|^2=\|\mathbf x-\mathbf q\|^2+\|\mathbf q-\mathbf z\|^2
$$

#### (c) 행렬 검산

투영행렬이 각 기저를 그대로 두는지 실제 숫자로 확인해요. 이는 두 열 전체에 대한 검사예요.

$$
\mathbf P\mathbf B=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}\begin{bmatrix}1 & 0\\0 & 1\\0 & 0\end{bmatrix}
$$

$$
\mathbf P\mathbf B=\begin{bmatrix}1 & 0\\0 & 1\\0 & 0\end{bmatrix}=\mathbf B
$$

또한 수치 행렬의 행과 열을 바꾸어도 같아서 $\mathbf P^{\mathsf T}=\mathbf P$예요. 최종 투영행렬은 다음과 같아요.

$$
\mathbf P=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
$$

#### (d) 전체 행렬의 멱등성 검산

직교성은 성분별 내적으로, 멱등성은 $3\times3$ 전체 곱으로 별도 확인해요.

$$
\mathbf B^{\mathsf T}\mathbf r=\begin{bmatrix}0\\0\end{bmatrix}
$$

$$
\mathbf M=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
$$

$$
\mathbf M^2=\begin{bmatrix}1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}
$$

$$
\mathbf M^2=1\mathbf M
$$

$$
\mathbf P^2=\frac{\mathbf M^2}{1}=\frac{\mathbf M}{1}=\mathbf P
$$

따라서 직교성과 $\mathbf P^2=\mathbf P$가 모두 성립해요. 단지 이 문제의 목표점에서만 두 번의 결과가 같은지를 확인한 것이 아니에요.

#### 여기서 헷갈리기 쉬워요

좌표는 두 성분, 투영은 세 성분이에요. $\boldsymbol\lambda$를 최종 투영벡터라고 쓰면 서로 다른 공간을 섞게 돼요. 기저가 정규직교임을 확인하지 않았다면 $\boldsymbol\lambda=\mathbf B^{\mathsf T}\mathbf x$를 바로 쓸 수 없어요.

오차와 제곱오차를 구별해 마지막 제곱근을 확인해요. 대칭행렬이라는 사실 하나만으로 멱등성이 따라오지는 않아요. $\mathbf P^2=\mathbf P$는 전체 행렬곱이나 위의 대수 증명으로 확인해야 해요.

#### 설명을 닫고 다시 해 봐요

1. 설명을 닫고 왜 $\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=0$부터 쓰는지 말해 보세요.
2. 좌표 두 개, 투영의 세 성분, 오차를 직접 다시 구해 보세요.
3. 한 목표벡터만 쓰지 않고 $\mathbf P^2=\mathbf P$를 보이는 식을 써 보세요.

**페이지 요약**

#### 첫 줄

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\mathbf0
$$

#### 떠올릴 개념·공식

기저의 배율은 정규방정식으로, 가장 가까운 점은 직교투영으로 구해요.

$$
\mathbf P=\mathbf B(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}
$$

#### 완성 답

$$
\boldsymbol\lambda=\begin{bmatrix}2\\3\end{bmatrix}
$$

$$
\pi_U(\mathbf x)=\begin{bmatrix}2\\3\\0\end{bmatrix}
$$

$$
\|\mathbf r\|=4
$$

#### 검산

기저와 잔차의 내적은 0, 전체 행렬은 $\mathbf P^2=\mathbf P$예요.

#### 조건·구분

$\mathbf B\in\mathbb R^{3\times2}$의 독립 기저 열과 보통의 내적을 전제해요. $\mathbf B$ 자체의 역행렬은 쓰지 않아요. 좌표는 두 성분, 투영은 세 성분이고, $\mathbf B^+$는 $2\times3$, $\mathbf P$는 $3\times3$이에요. 기저가 정규직교임을 확인하지 않고 $\boldsymbol\lambda=\mathbf B^T\mathbf x$를 쓰면 안 돼요.

오차는 잔차의 노름이고 제곱오차와 구별해요. 직교 잔차의 피타고라스 분해가 최소거리를 보장해요. 대칭성이나 벡터 하나의 재투영만으로 전체 멱등성을 증명하지 않고 행렬곱으로 $\mathbf P^2=\mathbf P$를 확인해요.

여기서는 $\mathbf B^T\mathbf B=\mathbf I_2$인 정규직교 기저예요. $\mathbf P=\operatorname{diag}(1,1,0)$, 잔차는 $[0,0,4]^T$이고 제곱오차 $16$의 제곱근이 오차 $4$예요.

---

<a id="p7"></a>

### P7. 평면에 가장 가까운 점

MML Example 3.11 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1019_Prediction_and_Projection.html#p7)

#### 주어진 조건

보통의 내적을 사용해요. $\mathbf{B}$의 두 열벡터가 평면 $U$의 기저예요. $U=\operatorname{span}(\mathbf{b}_1,\mathbf{b}_2)$로 두어요.

$$
\mathbf{B}=[\mathbf{b}_1\ \mathbf{b}_2]=\begin{bmatrix}1 & 0\\1 & 1\\1 & 2\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}0\\6\\0\end{bmatrix}
$$

#### 구할 것

- (a) 이 기저에 대한 투영벡터의 좌표 $\boldsymbol{\lambda}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})$와 투영오차 $\|\mathbf{x}-\pi_U(\mathbf{x})\|$를 구해 보세요.
- (c) 투영행렬 $\mathbf{P}$를 구해 보세요.
- (d) 차이벡터가 두 기저벡터에 직교하는지, $\mathbf{P}^2=\mathbf{P}$인지 확인해 보세요.

<details><summary>원문 보기</summary>

“find the coordinates” — MML Example 3.11

</details>

#### 무엇을 구하는 문제인가요

두 방향으로 펼친 평면 안에서 목표점과 가장 가까운 자리를 찾아요. 먼저 두 방향을 얼마씩 섞을지 정하고, 그 결과가 목표와 얼마나 떨어졌는지 확인해요.

(a)는 두 개의 좌표, (b)는 세 성분의 투영벡터와 거리, (c)는 모든 입력에 적용하는 행렬, (d)는 직교성과 반복 투영의 성질을 물어요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

문제의 ‘기저’, ‘평면’, ‘투영’이라는 단서에서 **직교투영(orthogonal projection)**을 떠올려요. 기저(basis)는 이 평면의 모든 점을 유일하게 표현하는 두 독립 방향이에요. 투영은 평면 위에서 목표와 거리가 가장 가까운 점을 고르는 일이에요.

$\mathbf B$는 두 기저를 열로 모은 $3\times2$ 행렬이고, $\mathbf x$는 목표인 $3\times1$ 벡터예요. $\boldsymbol\lambda=(\lambda_1,\lambda_2)^{\mathsf T}$는 섞는 양 두 개, $\mathbf q=\mathbf B\boldsymbol\lambda$는 평면 위의 $3\times1$ 점이에요. 가장 가까울 때 잔차 $\mathbf r=\mathbf x-\mathbf q$가 두 기저 모두와 직교해야 해요.

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\mathbf0
$$

$$
\mathbf B^{\mathsf T}\mathbf B\boldsymbol\lambda=\mathbf B^{\mathsf T}\mathbf x
$$

이 식을 **정규방정식(normal equation)**이라고 해요. 기저 열이 독립이므로 $\mathbf G=\mathbf B^{\mathsf T}\mathbf B$는 가역이고, 이 식으로 좌표를 구할 수 있어요. $\mathbf B$ 자체는 정사각행렬이 아니므로 $\mathbf B^{-1}$를 쓰는 방법은 맞지 않아요.

$$
\boldsymbol\lambda=(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}\mathbf x
$$

(b)의 ‘오차’는 차이벡터 자체나 제곱거리와 구별해요. Euclidean norm(유클리드 노름)은 성분 제곱의 합에 제곱근을 취한 길이예요.

$$
\|\mathbf r\|=\sqrt{r_1^2+r_2^2+r_3^2}
$$

(c)는 이 과정을 임의의 목표에 적용할 **투영행렬(projection matrix)**을 물어요. 좌표를 구하는 $2\times3$ 유사역행렬(pseudo-inverse) 앞에 기저를 곱해 원래의 세 성분으로 되돌려요.

$$
\mathbf B^+=(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}
$$

$$
\mathbf P=\mathbf B\mathbf B^+\in\mathbb R^{3\times3}
$$

(d)의 직교는 내적이 0이라는 뜻이에요. 멱등성(idempotence) $\mathbf P^2=\mathbf P$는 이미 평면 위로 보낸 벡터를 다시 투영해도 바뀌지 않는다는 뜻이에요. 한 벡터에서만 같은지 보는 대신 행렬 전체의 성질을 확인해야 해요.

#### 종이에 적을 첫 줄

종이에 가장 먼저 ‘평면 위 후보는 $\mathbf q=\mathbf B\boldsymbol\lambda$’라고 써요. 이제 수직 조건을 두 행의 연립방정식으로 만들기 위해 전치를 적어요.

$$
\mathbf B^{\mathsf T}=\begin{bmatrix}1 & 1 & 1\\0 & 1 & 2\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\begin{bmatrix}0\\0\end{bmatrix}
$$

전치(transpose)는 행과 열을 바꾸는 연산이에요. $2\times3$ 전치에 $3\times1$ 잔차를 곱하므로 기저마다 하나씩, 조건 두 개가 나와요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 기저 좌표

두 행의 내적을 계산해 $2\times2$ 계수행렬과 $2\times1$ 우변을 만들어요.

$$
\mathbf G=\mathbf B^{\mathsf T}\mathbf B=\begin{bmatrix}3 & 3\\3 & 5\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}\mathbf x=\begin{bmatrix}6\\6\end{bmatrix}
$$

$$
\begin{bmatrix}3 & 3\\3 & 5\end{bmatrix}\begin{bmatrix}\lambda_1\\\lambda_2\end{bmatrix}=\begin{bmatrix}6\\6\end{bmatrix}
$$

둘째 행에서 첫째 행을 빼면 둘째 좌표가 먼저 정해져요. 좌표가 0이어도 두 기저가 독립이라는 조건은 변하지 않아요.

$$
3\lambda_1+3\lambda_2=6
$$

$$
3\lambda_1+5\lambda_2=6
$$

$$
2\lambda_2=0
$$

$$
\lambda_2=0
$$

$$
3\lambda_1=6
$$

$$
\lambda_1=2
$$

$$
\boldsymbol\lambda=\begin{bmatrix}2\\0\end{bmatrix}
$$

#### (b) 투영과 오차

좌표 두 개는 배율이에요. 각 기저벡터에 그 배율을 곱해 더하면 원래의 세 성분을 가진 점이 나와요.

$$
\mathbf q=\mathbf B\boldsymbol\lambda=\begin{bmatrix}1 & 0\\1 & 1\\1 & 2\end{bmatrix}\begin{bmatrix}2\\0\end{bmatrix}
$$

$$
\mathbf q=\begin{bmatrix}2\\2\\2\end{bmatrix}
$$

$$
\mathbf r=\mathbf x-\mathbf q=\begin{bmatrix}0\\6\\0\end{bmatrix}-\begin{bmatrix}2\\2\\2\end{bmatrix}
$$

$$
\mathbf r=\begin{bmatrix}-2\\4\\-2\end{bmatrix}
$$

오차는 세 성분을 더한 값이 아니라 길이예요. 음수 성분도 제곱하면 양수가 돼요.

$$
\|\mathbf r\|^2=(-2)^2+(4)^2+(-2)^2=24
$$

$$
\|\mathbf r\|=\sqrt{24}
$$

#### (c) 투영행렬

이제 목표 $\mathbf x$가 바뀌어도 쓸 수 있는 행렬을 만들어요. $2\times2$ 역행렬 공식을 적용할 때 대각 성분을 맞바꾸고 나머지 두 성분의 부호를 바꿔 행렬식으로 나눠요.

$$
\det\mathbf G=(3)(5)-(3)(3)=6
$$

$$
\mathbf G^{-1}=\frac{1}{6}\begin{bmatrix}5 & -3\\-3 & 3\end{bmatrix}
$$

오른쪽의 전치부터 곱해 $2\times3$ 유사역행렬을 구하고, 왼쪽에 기저를 곱해 $3\times3$ 투영행렬을 만들어요. 곱 순서를 유지해야 차원도 맞아요.

$$
\mathbf B^+=\mathbf G^{-1}\mathbf B^{\mathsf T}=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\-3 & 0 & 3\end{bmatrix}
$$

$$
\mathbf P=\mathbf B\mathbf B^+=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}
$$

#### (d) 직교성과 반복 투영

먼저 차이벡터가 각 기저와 직교하는지 실제 내적으로 확인해요.

$$
\mathbf b_1^{\mathsf T}\mathbf r=(1)(-2)+(1)(4)+(1)(-2)=0
$$

$$
\mathbf b_2^{\mathsf T}\mathbf r=(0)(-2)+(1)(4)+(2)(-2)=0
$$

$\mathbf q-\mathbf x=-\mathbf r$를 써도 내적은 여전히 0이에요. 다음은 평면 위의 모든 점이 그대로 남는다는 것을 확인해요.

$$
\mathbf P\mathbf B=\mathbf B\mathbf G^{-1}(\mathbf B^{\mathsf T}\mathbf B)
$$

$$
\mathbf P\mathbf B=\mathbf B\mathbf G^{-1}\mathbf G=\mathbf B
$$

어떤 입력을 한 번 투영한 결과도 $\mathbf B$의 열들의 조합이에요. 따라서 다시 투영하면 바뀌지 않아요.

$$
\mathbf P^2=(\mathbf P\mathbf B)\mathbf G^{-1}\mathbf B^{\mathsf T}
$$

$$
\mathbf P^2=\mathbf B\mathbf G^{-1}\mathbf B^{\mathsf T}=\mathbf P
$$

이 계산은 특정 목표점 하나가 아니라 행렬 전체에 대한 증명이에요. 또 $\mathbf G^{-1}$가 대칭이므로 $\mathbf P^{\mathsf T}=\mathbf P$예요. 이 대칭성과 수직 잔차가 직교투영의 성질과 일치해요.

#### 완성 답과 검산

#### (a) 좌표 검산

답인 좌표를 원래 두 행의 식에 다시 넣어요. 좌변이 계산했던 우변과 정확히 같아요.

$$
\begin{bmatrix}3 & 3\\3 & 5\end{bmatrix}\begin{bmatrix}2\\0\end{bmatrix}=\begin{bmatrix}6\\6\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}\mathbf x=\begin{bmatrix}6\\6\end{bmatrix}
$$

$$
\boldsymbol\lambda=\begin{bmatrix}2\\0\end{bmatrix}
$$

#### (b) 투영과 거리 검산

좌표로 만든 점과 행렬로 만든 점을 서로 다른 곱으로 비교해요.

$$
\mathbf P\mathbf x=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}\begin{bmatrix}0\\6\\0\end{bmatrix}
$$

$$
\mathbf P\mathbf x=\begin{bmatrix}2\\2\\2\end{bmatrix}=\mathbf q
$$

$$
\|\mathbf x-\mathbf q\|^2=24
$$

$$
\|\mathbf x-\mathbf q\|=\sqrt{24}
$$

평면 위 임의의 다른 점 $\mathbf z$를 잡으면 잔차와 평면 내 차이가 수직이에요. 그래서 아래 식의 둘째 항은 음수가 될 수 없고, 지금 점이 최단거리라는 뜻도 확인돼요.

$$
\|\mathbf x-\mathbf z\|^2=\|\mathbf x-\mathbf q\|^2+\|\mathbf q-\mathbf z\|^2
$$

#### (c) 행렬 검산

투영행렬이 각 기저를 그대로 두는지 실제 숫자로 확인해요. 이는 두 열 전체에 대한 검사예요.

$$
\mathbf P\mathbf B=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}\begin{bmatrix}1 & 0\\1 & 1\\1 & 2\end{bmatrix}
$$

$$
\mathbf P\mathbf B=\begin{bmatrix}1 & 0\\1 & 1\\1 & 2\end{bmatrix}=\mathbf B
$$

또한 수치 행렬의 행과 열을 바꾸어도 같아서 $\mathbf P^{\mathsf T}=\mathbf P$예요. 최종 투영행렬은 다음과 같아요.

$$
\mathbf P=\frac{1}{6}\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}
$$

#### (d) 전체 행렬의 멱등성 검산

직교성은 성분별 내적으로, 멱등성은 $3\times3$ 전체 곱으로 별도 확인해요.

$$
\mathbf B^{\mathsf T}\mathbf r=\begin{bmatrix}0\\0\end{bmatrix}
$$

$$
\mathbf M=\begin{bmatrix}5 & 2 & -1\\2 & 2 & 2\\-1 & 2 & 5\end{bmatrix}
$$

$$
\mathbf M^2=\begin{bmatrix}30 & 12 & -6\\12 & 12 & 12\\-6 & 12 & 30\end{bmatrix}
$$

$$
\mathbf M^2=6\mathbf M
$$

$$
\mathbf P^2=\frac{\mathbf M^2}{36}=\frac{\mathbf M}{6}=\mathbf P
$$

따라서 직교성과 $\mathbf P^2=\mathbf P$가 모두 성립해요. 단지 이 문제의 목표점에서만 두 번의 결과가 같은지를 확인한 것이 아니에요.

#### 여기서 헷갈리기 쉬워요

좌표는 두 성분, 투영은 세 성분이에요. $\boldsymbol\lambda$를 최종 투영벡터라고 쓰면 서로 다른 공간을 섞게 돼요. 기저가 정규직교라고 주어지지 않았다면 $\boldsymbol\lambda=\mathbf B^{\mathsf T}\mathbf x$를 바로 쓸 수 없어요.

오차와 제곱오차를 구별해 마지막 제곱근을 확인해요. 대칭행렬이라는 사실 하나만으로 멱등성이 따라오지는 않아요. $\mathbf P^2=\mathbf P$는 전체 행렬곱이나 위의 대수 증명으로 확인해야 해요.

#### 설명을 닫고 다시 해 봐요

1. 설명을 닫고 왜 $\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=0$부터 쓰는지 말해 보세요.
2. 좌표 두 개, 투영의 세 성분, 오차를 직접 다시 구해 보세요.
3. 한 목표벡터만 쓰지 않고 $\mathbf P^2=\mathbf P$를 보이는 식을 써 보세요.

**페이지 요약**

#### 첫 줄

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\mathbf0
$$

#### 떠올릴 개념·공식

기저의 배율은 정규방정식으로, 가장 가까운 점은 직교투영으로 구해요.

$$
\mathbf P=\mathbf B(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}
$$

#### 완성 답

$$
\boldsymbol\lambda=\begin{bmatrix}2\\0\end{bmatrix}
$$

$$
\pi_U(\mathbf x)=\begin{bmatrix}2\\2\\2\end{bmatrix}
$$

$$
\|\mathbf r\|=\sqrt{24}
$$

#### 검산

기저와 잔차의 내적은 0, 전체 행렬은 $\mathbf P^2=\mathbf P$예요.

#### 조건·구분

$\mathbf B\in\mathbb R^{3\times2}$의 독립 기저 열과 보통의 내적을 전제해요. $\mathbf B$ 자체의 역행렬은 쓰지 않아요. 좌표는 두 성분, 투영은 세 성분이고, $\mathbf B^+$는 $2\times3$, $\mathbf P$는 $3\times3$이에요. 기저가 정규직교임을 확인하지 않고 $\boldsymbol\lambda=\mathbf B^T\mathbf x$를 쓰면 안 돼요.

오차는 잔차의 노름이고 제곱오차와 구별해요. 직교 잔차의 피타고라스 분해가 최소거리를 보장해요. 대칭성이나 벡터 하나의 재투영만으로 전체 멱등성을 증명하지 않고 행렬곱으로 $\mathbf P^2=\mathbf P$를 확인해요.

좌표 $\lambda_2=0$이어도 두 기저의 독립성은 바뀌지 않아요. 투영은 $[2,2,2]^T$, 잔차는 $[-2,4,-2]^T$이고 오차는 $\sqrt{24}$예요.

---

<a id="p8"></a>

### P8. 평면에 가장 가까운 점

MML Example 3.11 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1019_Prediction_and_Projection.html#p8)

#### 주어진 조건

보통의 내적을 사용해요. $\mathbf{B}$의 두 열벡터가 평면 $U$의 기저예요. $U=\operatorname{span}(\mathbf{b}_1,\mathbf{b}_2)$로 두어요.

$$
\mathbf{B}=[\mathbf{b}_1\ \mathbf{b}_2]=\begin{bmatrix}1 & 1\\2 & 0\\0 & 1\end{bmatrix},\qquad\mathbf{x}=\begin{bmatrix}1\\2\\3\end{bmatrix}
$$

#### 구할 것

- (a) 이 기저에 대한 투영벡터의 좌표 $\boldsymbol{\lambda}$를 구해 보세요.
- (b) 투영벡터 $\pi_U(\mathbf{x})$와 투영오차 $\|\mathbf{x}-\pi_U(\mathbf{x})\|$를 구해 보세요.
- (c) 투영행렬 $\mathbf{P}$를 구해 보세요.
- (d) 차이벡터가 두 기저벡터에 직교하는지, $\mathbf{P}^2=\mathbf{P}$인지 확인해 보세요.

<details><summary>원문 보기</summary>

“find the coordinates” — MML Example 3.11

</details>

#### 무엇을 구하는 문제인가요

두 방향으로 펼친 평면 안에서 목표점과 가장 가까운 자리를 찾아요. 먼저 두 방향을 얼마씩 섞을지 정하고, 그 결과가 목표와 얼마나 떨어졌는지 확인해요.

(a)는 두 개의 좌표, (b)는 세 성분의 투영벡터와 거리, (c)는 모든 입력에 적용하는 행렬, (d)는 직교성과 반복 투영의 성질을 물어요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

문제의 ‘기저’, ‘평면’, ‘투영’이라는 단서에서 **직교투영(orthogonal projection)**을 떠올려요. 기저(basis)는 이 평면의 모든 점을 유일하게 표현하는 두 독립 방향이에요. 투영은 평면 위에서 목표와 거리가 가장 가까운 점을 고르는 일이에요.

$\mathbf B$는 두 기저를 열로 모은 $3\times2$ 행렬이고, $\mathbf x$는 목표인 $3\times1$ 벡터예요. $\boldsymbol\lambda=(\lambda_1,\lambda_2)^{\mathsf T}$는 섞는 양 두 개, $\mathbf q=\mathbf B\boldsymbol\lambda$는 평면 위의 $3\times1$ 점이에요. 가장 가까울 때 잔차 $\mathbf r=\mathbf x-\mathbf q$가 두 기저 모두와 직교해야 해요.

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\mathbf0
$$

$$
\mathbf B^{\mathsf T}\mathbf B\boldsymbol\lambda=\mathbf B^{\mathsf T}\mathbf x
$$

이 식을 **정규방정식(normal equation)**이라고 해요. 기저 열이 독립이므로 $\mathbf G=\mathbf B^{\mathsf T}\mathbf B$는 가역이고, 이 식으로 좌표를 구할 수 있어요. $\mathbf B$ 자체는 정사각행렬이 아니므로 $\mathbf B^{-1}$를 쓰는 방법은 맞지 않아요.

$$
\boldsymbol\lambda=(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}\mathbf x
$$

(b)의 ‘오차’는 차이벡터 자체나 제곱거리와 구별해요. Euclidean norm(유클리드 노름)은 성분 제곱의 합에 제곱근을 취한 길이예요.

$$
\|\mathbf r\|=\sqrt{r_1^2+r_2^2+r_3^2}
$$

(c)는 이 과정을 임의의 목표에 적용할 **투영행렬(projection matrix)**을 물어요. 좌표를 구하는 $2\times3$ 유사역행렬(pseudo-inverse) 앞에 기저를 곱해 원래의 세 성분으로 되돌려요.

$$
\mathbf B^+=(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}
$$

$$
\mathbf P=\mathbf B\mathbf B^+\in\mathbb R^{3\times3}
$$

(d)의 직교는 내적이 0이라는 뜻이에요. 멱등성(idempotence) $\mathbf P^2=\mathbf P$는 이미 평면 위로 보낸 벡터를 다시 투영해도 바뀌지 않는다는 뜻이에요. 한 벡터에서만 같은지 보는 대신 행렬 전체의 성질을 확인해야 해요.

#### 종이에 적을 첫 줄

종이에 가장 먼저 ‘평면 위 후보는 $\mathbf q=\mathbf B\boldsymbol\lambda$’라고 써요. 이제 수직 조건을 두 행의 연립방정식으로 만들기 위해 전치를 적어요.

$$
\mathbf B^{\mathsf T}=\begin{bmatrix}1 & 2 & 0\\1 & 0 & 1\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\begin{bmatrix}0\\0\end{bmatrix}
$$

전치(transpose)는 행과 열을 바꾸는 연산이에요. $2\times3$ 전치에 $3\times1$ 잔차를 곱하므로 기저마다 하나씩, 조건 두 개가 나와요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 기저 좌표

두 행의 내적을 계산해 $2\times2$ 계수행렬과 $2\times1$ 우변을 만들어요.

$$
\mathbf G=\mathbf B^{\mathsf T}\mathbf B=\begin{bmatrix}5 & 1\\1 & 2\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}\mathbf x=\begin{bmatrix}5\\4\end{bmatrix}
$$

$$
\begin{bmatrix}5 & 1\\1 & 2\end{bmatrix}\begin{bmatrix}\lambda_1\\\lambda_2\end{bmatrix}=\begin{bmatrix}5\\4\end{bmatrix}
$$

첫째 행의 두 배에서 둘째 행을 빼면 둘째 좌표가 사라져요. 분수를 소수로 바꾸지 않고 대입해요.

$$
5\lambda_1+\lambda_2=5
$$

$$
\lambda_1+2\lambda_2=4
$$

$$
9\lambda_1=6
$$

$$
\lambda_1=\frac23
$$

$$
\lambda_2=5-5\cdot\frac23=\frac53
$$

$$
\boldsymbol\lambda=\begin{bmatrix}\frac{2}{3}\\\frac{5}{3}\end{bmatrix}
$$

#### (b) 투영과 오차

좌표 두 개는 배율이에요. 각 기저벡터에 그 배율을 곱해 더하면 원래의 세 성분을 가진 점이 나와요.

$$
\mathbf q=\mathbf B\boldsymbol\lambda=\begin{bmatrix}1 & 1\\2 & 0\\0 & 1\end{bmatrix}\begin{bmatrix}\frac{2}{3}\\\frac{5}{3}\end{bmatrix}
$$

$$
\mathbf q=\begin{bmatrix}\frac{7}{3}\\\frac{4}{3}\\\frac{5}{3}\end{bmatrix}
$$

$$
\mathbf r=\mathbf x-\mathbf q=\begin{bmatrix}1\\2\\3\end{bmatrix}-\begin{bmatrix}\frac{7}{3}\\\frac{4}{3}\\\frac{5}{3}\end{bmatrix}
$$

$$
\mathbf r=\begin{bmatrix}-\frac{4}{3}\\\frac{2}{3}\\\frac{4}{3}\end{bmatrix}
$$

오차는 세 성분을 더한 값이 아니라 길이예요. 음수 성분도 제곱하면 양수가 돼요.

$$
\|\mathbf r\|^2=(-\frac{4}{3})^2+(\frac{2}{3})^2+(\frac{4}{3})^2=4
$$

$$
\|\mathbf r\|=2
$$

#### (c) 투영행렬

이제 목표 $\mathbf x$가 바뀌어도 쓸 수 있는 행렬을 만들어요. $2\times2$ 역행렬 공식을 적용할 때 대각 성분을 맞바꾸고 나머지 두 성분의 부호를 바꿔 행렬식으로 나눠요.

$$
\det\mathbf G=(5)(2)-(1)(1)=9
$$

$$
\mathbf G^{-1}=\frac{1}{9}\begin{bmatrix}2 & -1\\-1 & 5\end{bmatrix}
$$

오른쪽의 전치부터 곱해 $2\times3$ 유사역행렬을 구하고, 왼쪽에 기저를 곱해 $3\times3$ 투영행렬을 만들어요. 곱 순서를 유지해야 차원도 맞아요.

$$
\mathbf B^+=\mathbf G^{-1}\mathbf B^{\mathsf T}=\frac{1}{9}\begin{bmatrix}1 & 4 & -1\\4 & -2 & 5\end{bmatrix}
$$

$$
\mathbf P=\mathbf B\mathbf B^+=\frac{1}{9}\begin{bmatrix}5 & 2 & 4\\2 & 8 & -2\\4 & -2 & 5\end{bmatrix}
$$

#### (d) 직교성과 반복 투영

먼저 차이벡터가 각 기저와 직교하는지 실제 내적으로 확인해요.

$$
\mathbf b_1^{\mathsf T}\mathbf r=(1)(-\frac{4}{3})+(2)(\frac{2}{3})+(0)(\frac{4}{3})=0
$$

$$
\mathbf b_2^{\mathsf T}\mathbf r=(1)(-\frac{4}{3})+(0)(\frac{2}{3})+(1)(\frac{4}{3})=0
$$

$\mathbf q-\mathbf x=-\mathbf r$를 써도 내적은 여전히 0이에요. 다음은 평면 위의 모든 점이 그대로 남는다는 것을 확인해요.

$$
\mathbf P\mathbf B=\mathbf B\mathbf G^{-1}(\mathbf B^{\mathsf T}\mathbf B)
$$

$$
\mathbf P\mathbf B=\mathbf B\mathbf G^{-1}\mathbf G=\mathbf B
$$

어떤 입력을 한 번 투영한 결과도 $\mathbf B$의 열들의 조합이에요. 따라서 다시 투영하면 바뀌지 않아요.

$$
\mathbf P^2=(\mathbf P\mathbf B)\mathbf G^{-1}\mathbf B^{\mathsf T}
$$

$$
\mathbf P^2=\mathbf B\mathbf G^{-1}\mathbf B^{\mathsf T}=\mathbf P
$$

이 계산은 특정 목표점 하나가 아니라 행렬 전체에 대한 증명이에요. 또 $\mathbf G^{-1}$가 대칭이므로 $\mathbf P^{\mathsf T}=\mathbf P$예요. 이 대칭성과 수직 잔차가 직교투영의 성질과 일치해요.

#### 완성 답과 검산

#### (a) 좌표 검산

답인 좌표를 원래 두 행의 식에 다시 넣어요. 좌변이 계산했던 우변과 정확히 같아요.

$$
\begin{bmatrix}5 & 1\\1 & 2\end{bmatrix}\begin{bmatrix}\frac{2}{3}\\\frac{5}{3}\end{bmatrix}=\begin{bmatrix}5\\4\end{bmatrix}
$$

$$
\mathbf B^{\mathsf T}\mathbf x=\begin{bmatrix}5\\4\end{bmatrix}
$$

$$
\boldsymbol\lambda=\begin{bmatrix}\frac{2}{3}\\\frac{5}{3}\end{bmatrix}
$$

#### (b) 투영과 거리 검산

좌표로 만든 점과 행렬로 만든 점을 서로 다른 곱으로 비교해요.

$$
\mathbf P\mathbf x=\frac{1}{9}\begin{bmatrix}5 & 2 & 4\\2 & 8 & -2\\4 & -2 & 5\end{bmatrix}\begin{bmatrix}1\\2\\3\end{bmatrix}
$$

$$
\mathbf P\mathbf x=\begin{bmatrix}\frac{7}{3}\\\frac{4}{3}\\\frac{5}{3}\end{bmatrix}=\mathbf q
$$

$$
\|\mathbf x-\mathbf q\|^2=4
$$

$$
\|\mathbf x-\mathbf q\|=2
$$

평면 위 임의의 다른 점 $\mathbf z$를 잡으면 잔차와 평면 내 차이가 수직이에요. 그래서 아래 식의 둘째 항은 음수가 될 수 없고, 지금 점이 최단거리라는 뜻도 확인돼요.

$$
\|\mathbf x-\mathbf z\|^2=\|\mathbf x-\mathbf q\|^2+\|\mathbf q-\mathbf z\|^2
$$

#### (c) 행렬 검산

투영행렬이 각 기저를 그대로 두는지 실제 숫자로 확인해요. 이는 두 열 전체에 대한 검사예요.

$$
\mathbf P\mathbf B=\frac{1}{9}\begin{bmatrix}5 & 2 & 4\\2 & 8 & -2\\4 & -2 & 5\end{bmatrix}\begin{bmatrix}1 & 1\\2 & 0\\0 & 1\end{bmatrix}
$$

$$
\mathbf P\mathbf B=\begin{bmatrix}1 & 1\\2 & 0\\0 & 1\end{bmatrix}=\mathbf B
$$

또한 수치 행렬의 행과 열을 바꾸어도 같아서 $\mathbf P^{\mathsf T}=\mathbf P$예요. 최종 투영행렬은 다음과 같아요.

$$
\mathbf P=\frac{1}{9}\begin{bmatrix}5 & 2 & 4\\2 & 8 & -2\\4 & -2 & 5\end{bmatrix}
$$

#### (d) 전체 행렬의 멱등성 검산

직교성은 성분별 내적으로, 멱등성은 $3\times3$ 전체 곱으로 별도 확인해요.

$$
\mathbf B^{\mathsf T}\mathbf r=\begin{bmatrix}0\\0\end{bmatrix}
$$

$$
\mathbf M=\begin{bmatrix}5 & 2 & 4\\2 & 8 & -2\\4 & -2 & 5\end{bmatrix}
$$

$$
\mathbf M^2=\begin{bmatrix}45 & 18 & 36\\18 & 72 & -18\\36 & -18 & 45\end{bmatrix}
$$

$$
\mathbf M^2=9\mathbf M
$$

$$
\mathbf P^2=\frac{\mathbf M^2}{81}=\frac{\mathbf M}{9}=\mathbf P
$$

따라서 직교성과 $\mathbf P^2=\mathbf P$가 모두 성립해요. 단지 이 문제의 목표점에서만 두 번의 결과가 같은지를 확인한 것이 아니에요.

#### 여기서 헷갈리기 쉬워요

좌표는 두 성분, 투영은 세 성분이에요. $\boldsymbol\lambda$를 최종 투영벡터라고 쓰면 서로 다른 공간을 섞게 돼요. 기저가 정규직교라고 주어지지 않았다면 $\boldsymbol\lambda=\mathbf B^{\mathsf T}\mathbf x$를 바로 쓸 수 없어요.

오차와 제곱오차를 구별해 마지막 제곱근을 확인해요. 대칭행렬이라는 사실 하나만으로 멱등성이 따라오지는 않아요. $\mathbf P^2=\mathbf P$는 전체 행렬곱이나 위의 대수 증명으로 확인해야 해요.

#### 설명을 닫고 다시 해 봐요

1. 설명을 닫고 왜 $\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=0$부터 쓰는지 말해 보세요.
2. 좌표 두 개, 투영의 세 성분, 오차를 직접 다시 구해 보세요.
3. 한 목표벡터만 쓰지 않고 $\mathbf P^2=\mathbf P$를 보이는 식을 써 보세요.

**페이지 요약**

#### 첫 줄

$$
\mathbf B^{\mathsf T}(\mathbf x-\mathbf B\boldsymbol\lambda)=\mathbf0
$$

#### 떠올릴 개념·공식

기저의 배율은 정규방정식으로, 가장 가까운 점은 직교투영으로 구해요.

$$
\mathbf P=\mathbf B(\mathbf B^{\mathsf T}\mathbf B)^{-1}\mathbf B^{\mathsf T}
$$

#### 완성 답

$$
\boldsymbol\lambda=\begin{bmatrix}\frac{2}{3}\\\frac{5}{3}\end{bmatrix}
$$

$$
\pi_U(\mathbf x)=\begin{bmatrix}\frac{7}{3}\\\frac{4}{3}\\\frac{5}{3}\end{bmatrix}
$$

$$
\|\mathbf r\|=2
$$

#### 검산

기저와 잔차의 내적은 0, 전체 행렬은 $\mathbf P^2=\mathbf P$예요.

#### 조건·구분

$\mathbf B\in\mathbb R^{3\times2}$의 독립 기저 열과 보통의 내적을 전제해요. $\mathbf B$ 자체의 역행렬은 쓰지 않아요. 좌표는 두 성분, 투영은 세 성분이고, $\mathbf B^+$는 $2\times3$, $\mathbf P$는 $3\times3$이에요. 기저가 정규직교임을 확인하지 않고 $\boldsymbol\lambda=\mathbf B^T\mathbf x$를 쓰면 안 돼요.

오차는 잔차의 노름이고 제곱오차와 구별해요. 직교 잔차의 피타고라스 분해가 최소거리를 보장해요. 대칭성이나 벡터 하나의 재투영만으로 전체 멱등성을 증명하지 않고 행렬곱으로 $\mathbf P^2=\mathbf P$를 확인해요.

---

원 문제·정리노트·PDF는 보존해요.
