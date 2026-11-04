# 복습문제 8선 — 1104 수업 범위

교과서 본문 예제 4개와 연습문제 4개예요. 먼저 풀어 보고 막히면 힌트를 열어 보세요.

> `복습문제_1104_PCA_Part2.html`를 마크다운으로 옮겼어요. 원문, 힌트, 풀이는 접혀 있어요. 먼저 풀어 보고 펼쳐 보세요.

**목차**

- [A. 교과서 본문 예제](#partA)
  - [P1. 숫자 8의 누적 설명 분산](#p1)
  - [P2. 주성분 평면에 놓인 숫자 0과 1](#p2)
  - [P3. 주성분 개수와 숫자 8의 복원](#p3)
  - [P4. 가로로 긴 행렬의 특잇값 분해](#p4)
- [B. 교과서 연습문제](#partB)
  - [P5. 사영에서 남는 부분과 사라지는 부분](#p5)
  - [P6. 두 행이 직교하는 행렬의 특잇값 분해](#p6)
  - [P7. 가장 큰 특잇값으로 랭크 1 근사](#p7)
  - [P8. 행렬이 벡터의 길이를 가장 크게 늘리는 비율](#p8)

<a id="partA"></a>

## A. 교과서 본문 예제

<a id="p1"></a>

### P1. 숫자 8의 누적 설명 분산

MNIST 학습 데이터에서 숫자 8만 골라 공분산 행렬을 구했어요. 왼쪽은 큰 고윳값부터 200개를 나열한 그래프예요. 오른쪽은 앞에서부터 주성분을 하나씩 추가할 때 누적 설명 분산을 나타내요.

*그림 10.5*

주성분을 처음 몇 개 추가할 때와 뒤에서 추가할 때 중 어느 쪽에서 누적 설명 분산이 크게 늘어나나요? 왼쪽 그래프를 근거로 설명해 보세요.

<details><summary>교과서 원문 보기</summary>

“Figure 10.5(a) shows the 200 largest eigenvalues of the data covariance matrix.” — Example 10.2

</details>

<details><summary>힌트 보기</summary>

왼쪽 그래프에서 앞부분과 뒷부분의 고윳값을 비교해 보세요.

</details>

<details><summary>풀이 보기</summary>

1. $M$번째 주성분을 추가하면 누적 설명 분산이 $\lambda_M$만큼 늘어나요. $\lambda_M$은 그 주성분 방향을 고유벡터로 갖는 공분산 행렬의 고윳값이에요.
2. 왼쪽에서 초반 고윳값은 크고 뒤로 갈수록 작아져요. 그래서 오른쪽 누적 그래프의 초반은 가파르고 이후에는 완만해져요.

정답은 초반 몇 개의 주성분에서 누적 설명 분산이 크게 늘어난다는 거예요.

</details>

---

<a id="p2"></a>

### P2. 주성분 평면에 놓인 숫자 0과 1

MNIST 학습 데이터의 숫자 0(파란 점)과 숫자 1(주황 점)을 첫 두 주성분이 만드는 평면에 나타냈어요. 빨간 표시와 선은 일부 점을 원래 이미지와 연결해요.

*그림 10.10*

숫자 0과 1의 점 무리는 얼마나 잘 나뉘나요? 어느 쪽 점들이 더 넓게 퍼져 있나요?

<details><summary>교과서 원문 보기</summary>

“We observe a relatively clear separation between “0”s (blue dots) and “1”s (orange dots)” — Example 10.3

</details>

<details><summary>힌트 보기</summary>

색마다 점이 모인 위치를 먼저 보고, 같은 색 점끼리 차지하는 범위를 비교해 보세요.

</details>

<details><summary>풀이 보기</summary>

1. 주황 점은 주로 왼쪽에, 파란 점은 주로 오른쪽에 모여 있어요. 경계 일부가 겹쳐도 두 무리는 비교적 잘 나뉘어요.
2. 파란 점이 주황 점보다 평면에서 넓게 퍼져 있어요. 따라서 이 두 주성분으로 본 집단 내부의 변동은 숫자 0 쪽이 더 커요.

정답은 0과 1은 비교적 분리되고 0 집단이 더 퍼져 있다는 거예요.

</details>

---

<a id="p3"></a>

### P3. 주성분 개수와 숫자 8의 복원

MNIST 숫자 이미지는 가로세로 28픽셀, 총 784픽셀이에요. 숫자 8의 학습 이미지 5,389장으로 주성분을 구했어요. 그림은 테스트 이미지 네 장의 원본과, 같은 네 장을 주성분 1개, 10개, 100개, 500개로 복원한 결과예요.

*그림 10.12*

- (a) 주성분을 더 많이 쓸수록 복원한 이미지는 어떻게 달라지나요?
- (b) 주성분 784개를 모두 쓰면 원본을 어떻게 복원할 수 있나요?

<details><summary>교과서 원문 보기</summary>

“With an increasing number of principal components (PCs), the reconstructions become sharper and more details are accounted for.” — Example 10.4

</details>

<details><summary>힌트 보기</summary>

한 열만 따라 내려가며 획의 모양을 비교해 보세요. 784개를 모두 쓰면 빠지는 방향이 있는지도 생각해 보세요.

</details>

<details><summary>풀이 보기</summary>

1. 한 열은 같은 원본을 복원한 결과예요. 주성분이 1개면 획이 흐리고 비슷한 모양으로 보이지만, 개수를 늘리면 각 숫자의 고유한 획이 선명해져요. 500개를 쓰면 원본에 매우 가까워요.
2. 픽셀 벡터는 $\mathbb R^{784}$에 있어요. 784개 주성분을 모두 유지하면 그 공간 전체의 좌표가 남아요. 따라서 중심화한 값을 그대로 복원하고 평균을 더하면 원본과 같아요.

정답은 주성분을 늘릴수록 세부가 복원되며 784개로 정확히 복원한다는 거예요.

</details>

---

<a id="p4"></a>

### P4. 가로로 긴 행렬의 특잇값 분해

$$
A=\begin{bmatrix}1&0&1\\-2&1&0\end{bmatrix}
$$

행렬 $A$의 전체 특잇값 분해 $A=U\Sigma V^\top$를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

“Let us find the singular value decomposition of” — Example 4.13

</details>

<details><summary>힌트 보기</summary>

$A^\top A$의 정규직교 고유벡터를 먼저 구하세요. 양의 특잇값에 대응하는 왼쪽 특이벡터는 $Av_i$를 정규화하면 나와요.

</details>

<details><summary>풀이 보기</summary>

1. $B=A^\top A$를 계산해요. 특성다항식을 인수분해하면 고윳값이 $6,1,0$이에요.

   $$
   B=\begin{bmatrix}5&-2&1\\-2&1&0\\1&0&1\end{bmatrix}
   $$

   $$
   \det(\lambda I_3-B)=\lambda(\lambda-6)(\lambda-1)
   $$
2. $Bv=\lambda v$의 둘째와 셋째 행을 보면 $\lambda=6$일 때 벡터 성분비는 $5:-2:1$이에요. $\lambda=1$일 때는 첫 성분이 0이고, 첫째 행에서 셋째 성분이 둘째의 두 배예요. 각각 단위벡터로 만들어요.

   $$
   v_1=\frac{1}{\sqrt{30}}\begin{bmatrix}5\\-2\\1\end{bmatrix}
   $$

   $$
   v_2=\frac{1}{\sqrt5}\begin{bmatrix}0\\1\\2\end{bmatrix}
   $$
3. $\lambda=0$ 방향은 $Av=0$을 풀어요. 첫 성분을 $-1$로 두면 둘째는 $-2$, 셋째는 $1$이에요. 단위벡터로 만든 뒤 $V=[v_1\ v_2\ v_3]$의 마지막 열에 둬요.

   $$
   v_3=\frac{1}{\sqrt6}\begin{bmatrix}-1\\-2\\1\end{bmatrix}
   $$
4. 양의 고윳값의 제곱근은 $\sigma_1=\sqrt{6}$과 $\sigma_2=1$이에요. $\Sigma$는 $A$와 같은 $2\times3$ 크기로 두어요.

   $$
   \Sigma=\begin{bmatrix}\sqrt{6}&0&0\\0&1&0\end{bmatrix}
   $$
5. $Av_1=(6,-12)^\top/\sqrt{30}$과 $Av_2=(2,1)^\top/\sqrt5$를 각각 $\sigma_1,\sigma_2$로 나눠요.

   $$
   U=\frac1{\sqrt5}\begin{bmatrix}1&2\\-2&1\end{bmatrix}
   $$

   $Av_3=0$이므로 $AV=U\Sigma$가 돼요. $V$의 열이 정규직교하므로 오른쪽에 $V^\top$를 곱하면 $A=U\Sigma V^\top$예요.

정답은 위의 $U,\Sigma,V$이고 양의 특잇값은 $\sqrt{6},1$이에요.

</details>

---

<a id="partB"></a>

## B. 교과서 연습문제

<a id="p5"></a>

### P5. 사영에서 남는 부분과 사라지는 부분

$V$는 벡터공간이고 $\pi$는 $V$에서 $V$로 가는 선형사상이에요. $\mathrm{id}_V$는 $V$의 항등사상이에요.

- (a) $\pi$가 사영일 필요충분조건이 $\mathrm{id}_V-\pi$도 사영이라는 것을 증명해 보세요.
- (b) $\pi$가 사영이라고 가정해요. $\operatorname{Im}(\pi)$와 $\ker(\pi)$를 써서 $\operatorname{Im}(\mathrm{id}_V-\pi)$와 $\ker(\mathrm{id}_V-\pi)$를 나타내 보세요.

<details><summary>교과서 원문 보기</summary>

“Let V be a vector space and π an endomorphism of V.” — Exercise 3.7

</details>

<details><summary>힌트 보기</summary>

$Q=\mathrm{id}_V-\pi$를 두고 $Q^2-Q$를 전개해 보세요. 이어서 $\pi Q$와 $Q\pi$가 각각 무엇인지 확인해 보세요.

</details>

<details><summary>풀이 보기</summary>

1. $I=\mathrm{id}_V$와 $Q=I-\pi$를 놓아요. $I$는 항등사상이므로 곱을 전개하면 $Q^2=(I-\pi)(I-\pi)=I-2\pi+\pi^2$예요. 여기에서 $Q=I-\pi$를 빼면 $Q^2-Q=\pi^2-\pi$예요. 선형사상 $P$가 사영일 조건은 $P^2=P$이므로 두 사영 조건은 동치예요.
2. $\pi^2=\pi$이면 $\pi Q=0$이므로 $Qx$는 항상 $\ker\pi$에 들어가요. 반대로 $\pi y=0$이면 $Qy=y$이므로 $y$는 $\operatorname{Im}Q$에 들어가요. 따라서 $\operatorname{Im}Q=\ker\pi$예요.
3. $Q\pi=0$이므로 $\pi x$는 항상 $\ker Q$에 들어가요. 반대로 $Qy=0$이면 $y=\pi y$이므로 $y$는 $\operatorname{Im}\pi$에 들어가요. 따라서 $\ker Q=\operatorname{Im}\pi$예요.

정답은 (a) 두 사영 조건은 동치예요. (b) 상과 핵이 서로 바뀌어요. $\operatorname{Im}Q=\ker\pi$이고 $\ker Q=\operatorname{Im}\pi$예요.

</details>

---

<a id="p6"></a>

### P6. 두 행이 직교하는 행렬의 특잇값 분해

$$
A=\begin{bmatrix}2&2\\-1&1\end{bmatrix}
$$

행렬 $A$의 특잇값 분해를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

“Find the singular value decomposition of” — Exercise 4.9

</details>

<details><summary>힌트 보기</summary>

$AA^\top$을 계산해 왼쪽 특이벡터를 구하세요. $v_i=A^\top u_i/\sigma_i$로 오른쪽 특이벡터를 구할 수 있어요.

</details>

<details><summary>풀이 보기</summary>

1. $AA^\top=\operatorname{diag}(8,2)$예요. 고윳값이 큰 순으로 왼쪽 특이벡터는 $e_1,e_2$이고, 특잇값은 $2\sqrt{2},\sqrt{2}$예요.
2. $A^\top e_1=(2,2)^\top$과 $A^\top e_2=(-1,1)^\top$을 각각 해당 특잇값으로 나눠 $v_1,v_2$를 구해요.

   $$
   V=\frac1{\sqrt2}\begin{bmatrix}1&-1\\1&1\end{bmatrix}
   $$
3. $U=I_2$로 두고 $\Sigma=\operatorname{diag}(2\sqrt{2},\sqrt{2})$를 넣으면 $U\Sigma V^\top$의 두 행은 $(2,2)$와 $(-1,1)$이 돼요.

정답은 $U=I_2$, $\Sigma=\operatorname{diag}(2\sqrt{2},\sqrt{2})$, $V=\frac{1}{\sqrt2}\begin{bmatrix}1&-1\\1&1\end{bmatrix}$예요.

</details>

---

<a id="p7"></a>

### P7. 가장 큰 특잇값으로 랭크 1 근사

$$
A=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}
$$

행렬 $A$의 랭크 1 근사를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

“Find the rank-1 approximation of” — Exercise 4.10

</details>

<details><summary>힌트 보기</summary>

$AA^\top$에서 가장 큰 고윳값에 대응하는 단위벡터 $u_1$을 구하세요. $u_1u_1^\top A$는 첫 SVD 항만 남겨요.

</details>

<details><summary>풀이 보기</summary>

1. $AA^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix}$의 고윳값은 $25,9$예요. 가장 큰 고윳값 $25$의 단위 고유벡터는 $u_1=(1,1)^\top/\sqrt2$예요.
2. $\sigma_1=\sqrt{25}=5$이고 $v_1$은 같은 특잇값의 오른쪽 단위 특이벡터예요. 에카르트–영 정리에 따라 Frobenius 오차를 최소화하는 랭크 1 근사는 SVD의 첫 항 $\sigma_1u_1v_1^\top$이에요. $u_1^\top A=\sigma_1v_1^\top$이므로 첫 항을 $u_1u_1^\top A$로 계산할 수 있어요.
3. $u_1u_1^\top$의 모든 성분은 $\frac{1}{2}$예요. 이를 $A$ 왼쪽에 곱하면 $A$의 두 행을 평균 낸 행이 두 번 나와요.

정답은 $\begin{bmatrix}\frac{5}{2}&\frac{5}{2}&0\\\frac{5}{2}&\frac{5}{2}&0\end{bmatrix}$예요.

</details>

---

<a id="p8"></a>

### P8. 행렬이 벡터의 길이를 가장 크게 늘리는 비율

$A\in\mathbb R^{m\times n}$이고 $\sigma_1$은 $A$의 가장 큰 특잇값이에요.

$x\ne0$에서 정리 4.24가 성립함을 증명해 보세요.

$$
\max_{x\ne0}\frac{\lVert Ax\rVert_2}{\lVert x\rVert_2}=\sigma_1
$$

<details><summary>교과서 원문 보기</summary>

“Show that for x ≠ 0 Theorem 4.24 holds” — Exercise 4.12

</details>

<details><summary>힌트 보기</summary>

$A=U\Sigma V^\top$로 두고 $V^\top x$의 좌표로 길이 비율의 제곱을 써 보세요. 등호를 만드는 벡터도 찾아야 해요.

</details>

<details><summary>풀이 보기</summary>

1. $z=V^\top x$라 놓아요. $V$와 $U$가 직교행렬이므로 $\lVert x\rVert_2=\lVert z\rVert_2$이고 $\lVert Ax\rVert_2=\lVert\Sigma z\rVert_2$예요.
2. $k=\min(m,n)$으로 놓으면 다음 부등식이 성립해요.

   $$
   \lVert\Sigma z\rVert_2^2=\sum_{i=1}^{k}\sigma_i^2 z_i^2\le \sigma_1^2\sum_{i=1}^{n} z_i^2=\sigma_1^2\lVert z\rVert_2^2
   $$

   $x\ne0$이므로 길이 비율은 $\sigma_1$ 이하예요.
3. $x$를 $V$의 첫 열 $v_1$로 골라요. $z=V^\top v_1$의 첫 성분은 1이고 나머지는 0이므로 $z$는 첫 표준기저 벡터 $e_1$이에요. 이때 $\lVert Ax\rVert_2=\sigma_1$이고 $\lVert x\rVert_2=1$이므로 상한에 도달해요.

정답은 최댓값 $\sigma_1$이에요.

</details>

---

출처는 Deisenroth, Faisal, Ong의 *Mathematics for Machine Learning*이에요. 풀이는 자체 작성했고 수치는 Python으로 검산했어요.
