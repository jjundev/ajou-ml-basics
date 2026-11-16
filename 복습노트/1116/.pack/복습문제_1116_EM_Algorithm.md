# 복습문제 8선 — 1116 수업 범위

MML 11장 예제로 만든 문제 **6개**, 5장 예제 **1개**, 5장 연습문제 **1개**로 EM의 갱신 계산과 벡터·행렬 미분을 연습해요. 먼저 풀어 보고, 막히면 힌트를 열어 보세요.

> `복습문제_1116_EM_Algorithm.html`를 마크다운으로 옮겼어요. 원문, 힌트, 풀이는 접혀 있어요. 먼저 풀어 보고 펼쳐 보세요.

**목차**

- [A. 교과서 예제 변형](#partA)
  - [P1. 총 책임도로 혼합 가중치 갱신하기](#p1)
  - [P2. 책임도 표로 평균 갱신하기](#p2)
  - [P3. 교과서 책임도 표로 평균 갱신하기](#p3)
  - [P4. 갱신된 평균으로 분산 갱신하기](#p4)
  - [P5. 수렴한 GMM을 초기값과 비교하기](#p5)
  - [P6. 최소제곱 손실의 기울기와 차원](#p6)
  - [P7. 분수로 분산 갱신하기](#p7)
- [B. 교과서 연습문제](#partB)
  - [P8. 벡터와 행렬로 스칼라 함수 미분하기](#p8)

<a id="partA"></a>

## A. 교과서 예제 변형

<a id="p1"></a>

### P1. 총 책임도로 혼합 가중치 갱신하기

관측 $7$개에 성분 $3$개짜리 GMM을 맞추고 있어요. 갱신 전 혼합 가중치는 $\pi_1=\pi_2=\pi_3=\frac{1}{3}$이에요.

E-step에서 구한 성분별 총 책임도 $N_k=\sum_{n=1}^{7} r_{nk}$는 다음과 같아요.

${N_1=2.058}$, ${N_2=2.008}$, ${N_3=2.934}$

EM의 M-step 가중치 갱신식은 다음과 같이 주어져요. 여기서 $N$은 관측의 개수예요.

$$
\pi_k^{\text{new}}=\frac{N_k}{N}
$$

- (a) 세 성분의 새 가중치 $\pi_k^{\text{new}}$를 소수점 아래 셋째 자리까지 구해 보세요.
- (b) (a)의 세 값을 더하면 $1$이 되는지 확인하고, 갱신 전 $\frac{1}{3}$보다 커진 성분을 골라 보세요.

<details><summary>교과서 원문 보기</summary>

“Here we see that the third component gets more weight/importance, while the other components become slightly less important.” — Example 11.5

</details>

<details><summary>힌트 보기</summary>

관측이 $7$개이므로 $N=7$이에요. 각 $N_k$를 $7$로 나눠요. 합을 확인할 때는 반올림한 값 대신 $N_1+N_2+N_3$을 먼저 더해 봐요.

</details>

<details><summary>풀이 보기</summary>

- (a) 관측이 $7$개라서 $N=7$이에요. 갱신식에 성분별 총 책임도를 넣어요.

  $$
  \pi_1^{\text{new}}=\frac{2.058}{7}=0.294
  $$

  $$
  \pi_2^{\text{new}}=\frac{2.008}{7}\approx0.287
  $$

  $$
  \pi_3^{\text{new}}=\frac{2.934}{7}\approx0.419
  $$
- (b) 반올림한 값을 더하면 $0.294+0.287+0.419=1.000$이에요. 반올림 전에도 정확히 $1$이에요. 분자를 먼저 더하면 관측 수와 같기 때문이에요.

  $$
  \sum_{k=1}^{3}\pi_k^{\text{new}}=\frac{2.058+2.008+2.934}{7}=\frac{7}{7}=1
  $$
- (b) 갱신 전 가중치는 $\frac{1}{3}\approx0.333$이에요. $0.294$와 $0.287$은 이보다 작고, $0.419$만 커요. 그래서 커진 성분은 성분 $3$뿐이에요.

정답 (a) ${(\pi_1^{\text{new}},\pi_2^{\text{new}},\pi_3^{\text{new}})=(0.294,0.287,0.419)}$ (b) 합은 정확히 $1$이고, $\frac{1}{3}$보다 커진 성분은 성분 $3$이에요.

</details>

---

<a id="p2"></a>

### P2. 책임도 표로 평균 갱신하기

1차원 관측 $x_1,\dots,x_7$에 성분 $3$개짜리 GMM을 맞추고 있어요. E-step에서 구한 책임도 $r_{nk}$가 아래 표에 있어요. 행은 관측 $x_n$, 열은 성분 $k=1,2,3$이에요.

| $x_n$ | $r_{n1}$ | $r_{n2}$ | $r_{n3}$ |
|---|---|---|---|
| $-4$ | $1$ | $0$ | $0$ |
| $-2$ | $1$ | $0$ | $0$ |
| $-1$ | $\frac{1}{2}$ | $\frac{1}{2}$ | $0$ |
| $0$ | $0$ | $1$ | $0$ |
| $2$ | $0$ | $\frac{1}{2}$ | $\frac{1}{2}$ |
| $4$ | $0$ | $0$ | $1$ |
| $6$ | $0$ | $0$ | $1$ |

M-step의 평균 갱신식은 다음과 같아요.

$$
\mu_k^{\text{new}}=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}x_n
$$

- (a) 세 성분의 총 책임도 $N_k=\sum_{n=1}^{7} r_{nk}$를 구해 보세요.
- (b) (a)의 $N_k$를 써서 세 성분의 새 평균 $\mu_k^{\text{new}}$를 구해 보세요.

<details><summary>교과서 원문 보기</summary>

“In our example from Figure 11.3, the mean values are updated as follows” — Example 11.3

</details>

<details><summary>힌트 보기</summary>

$N_k$는 열 $k$를 위에서 아래로 더한 값이에요. 평균은 같은 열의 책임도로 관측을 가중해 더한 뒤 $N_k$로 나눠요.

</details>

<details><summary>풀이 보기</summary>

- (a) 성분 하나를 고정하고 그 열의 책임도를 모두 더해요. $0$인 칸은 빼고 더해도 같아요.

  $$
  N_1=1+1+\tfrac{1}{2}=\frac{5}{2}
  $$

  $$
  N_2=\tfrac{1}{2}+1+\tfrac{1}{2}=2
  $$

  $$
  N_3=\tfrac{1}{2}+1+1=\frac{5}{2}
  $$

  세 값의 합은 $7$로 관측 수와 같아요. 행마다 책임도의 합이 $1$이기 때문이에요.
- (b) 같은 열의 책임도를 관측값에 곱해 더한 뒤, (a)의 $N_k$로 나눠요.

  $$
  \mu_1^{\text{new}}=\frac{1\cdot(-4)+1\cdot(-2)+\frac{1}{2}\cdot(-1)}{5/2}=\frac{-13/2}{5/2}=-2.6
  $$

  $$
  \mu_2^{\text{new}}=\frac{\frac{1}{2}\cdot(-1)+1\cdot0+\frac{1}{2}\cdot2}{2}=\frac{1/2}{2}=0.25
  $$

  $$
  \mu_3^{\text{new}}=\frac{\frac{1}{2}\cdot2+1\cdot4+1\cdot6}{5/2}=\frac{11}{5/2}=4.4
  $$

정답 (a) ${(N_1,N_2,N_3)=\left(\frac{5}{2},2,\frac{5}{2}\right)}$ (b) ${(\mu_1^{\text{new}},\mu_2^{\text{new}},\mu_3^{\text{new}})=(-2.6,0.25,4.4)}$

</details>

---

<a id="p3"></a>

### P3. 교과서 책임도 표로 평균 갱신하기

관측값은 $-3,-2.5,-1,0,2,4,5$예요. 성분 $3$개짜리 GMM의 갱신 전 평균은 $\mu_1=-4$, $\mu_2=0$, $\mu_3=8$이에요. E-step에서 구한 책임도 $r_{nk}$가 반올림되어 아래 표에 있어요. 행은 관측 $x_n$, 열은 성분 $k=1,2,3$이에요. 표에 적힌 수로 계산해요.

| $x_n$ | $r_{n1}$ | $r_{n2}$ | $r_{n3}$ |
|---|---|---|---|
| $-3$ | $1.0$ | $0.0$ | $0.0$ |
| $-2.5$ | $1.0$ | $0.0$ | $0.0$ |
| $-1$ | $0.057$ | $0.943$ | $0.0$ |
| $0$ | $0.001$ | $0.999$ | $0.0$ |
| $2$ | $0.0$ | $0.066$ | $0.934$ |
| $4$ | $0.0$ | $0.0$ | $1.0$ |
| $5$ | $0.0$ | $0.0$ | $1.0$ |

M-step의 평균 갱신식은 다음과 같아요. 여기서 $N_k=\sum_{n=1}^{7} r_{nk}$예요.

$$
\mu_k^{\text{new}}=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}x_n
$$

- (a) 세 성분의 새 평균 $\mu_k^{\text{new}}$를 소수점 아래 둘째 자리까지 구해 보세요.
- (b) (a)의 결과로 갱신 전후 평균의 이동 거리 $|\mu_k^{\text{new}}-\mu_k|$를 구하고, 가장 많이 움직인 성분을 골라 보세요.

<details><summary>교과서 원문 보기</summary>

“Here we see that the means of the first and third mixture component move toward the regime of the data” — Example 11.3

</details>

<details><summary>힌트 보기</summary>

먼저 열의 합으로 $N_k$를 구해요. 그다음 같은 열의 책임도를 관측값에 곱해 더하고 $N_k$로 나눠요.

</details>

<details><summary>풀이 보기</summary>

- (a) 열마다 책임도를 더해 $N_k$를 구해요.

  $$
  N_1=1.0+1.0+0.057+0.001=2.058
  $$

  $$
  N_2=0.943+0.999+0.066=2.008
  $$

  $$
  N_3=0.934+1.0+1.0=2.934
  $$
- (a) 같은 열의 책임도로 관측값을 가중해 더해요. $0$인 칸은 빼도 돼요.

  $$
  \sum_n r_{n1}x_n=-3-2.5+0.057\cdot(-1)+0.001\cdot0=-5.557
  $$

  $$
  \sum_n r_{n2}x_n=0.943\cdot(-1)+0.999\cdot0+0.066\cdot2=-0.811
  $$

  $$
  \sum_n r_{n3}x_n=0.934\cdot2+4+5=10.868
  $$
- (a) 각 합을 $N_k$로 나눈 뒤 반올림해요.

  $$
  \mu_1^{\text{new}}=\frac{-5.557}{2.058}\approx-2.70
  $$

  $$
  \mu_2^{\text{new}}=\frac{-0.811}{2.008}\approx-0.40
  $$

  $$
  \mu_3^{\text{new}}=\frac{10.868}{2.934}\approx3.70
  $$
- (b) (a)의 값에서 갱신 전 평균을 빼 거리를 재요.

  $$
  |-2.70-(-4)|=1.30
  $$

  $$
  |-0.40-0|=0.40
  $$

  $$
  |3.70-8|=4.30
  $$

  $4.30$이 가장 크므로 가장 많이 움직인 성분은 성분 $3$이에요.

정답 (a) ${(\mu_1^{\text{new}},\mu_2^{\text{new}},\mu_3^{\text{new}})=(-2.70,-0.40,3.70)}$ (b) 이동 거리는 $(1.30,0.40,4.30)$이고, 성분 $3$이 $4.30$으로 가장 많이 움직여요.

</details>

---

<a id="p4"></a>

### P4. 갱신된 평균으로 분산 갱신하기

관측값 $-3,-2.5,-1,0,2,4,5$에 성분 $3$개짜리 1차원 GMM을 맞추고 있어요. E-step에서 구한 책임도 $r_{nk}$가 반올림되어 아래 표에 있어요. 행은 관측 $x_n$, 열은 성분 $k=1,2,3$이에요.

| $x_n$ | $r_{n1}$ | $r_{n2}$ | $r_{n3}$ |
|---|---|---|---|
| $-3$ | $1.0$ | $0.0$ | $0.0$ |
| $-2.5$ | $1.0$ | $0.0$ | $0.0$ |
| $-1$ | $0.057$ | $0.943$ | $0.0$ |
| $0$ | $0.001$ | $0.999$ | $0.0$ |
| $2$ | $0.0$ | $0.066$ | $0.934$ |
| $4$ | $0.0$ | $0.0$ | $1.0$ |
| $5$ | $0.0$ | $0.0$ | $1.0$ |

총 책임도는 ${(N_1,N_2,N_3)=(2.058,2.008,2.934)}$이에요. 이미 갱신된 평균은 ${(\mu_1^{\text{new}},\mu_2^{\text{new}},\mu_3^{\text{new}})=(-2.7,-0.4,3.7)}$이고, 이 값을 그대로 써요. 갱신 전 분산은 ${(\sigma_1^2,\sigma_2^2,\sigma_3^2)=(1,0.2,3)}$이에요. 분산 갱신식은 다음과 같아요.

$$
(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}(x_n-\mu_k^{\text{new}})^2
$$

- (a) 세 성분의 새 분산 $(\sigma_k^{\text{new}})^2$을 소수점 아래 둘째 자리까지 구해 보세요.
- (b) (a)의 결과를 갱신 전 분산과 비교해, 분산이 줄어든 성분과 커진 성분을 골라 보세요.

<details><summary>교과서 원문 보기</summary>

“Here we see that the variances of the first and third component shrink significantly” — Example 11.4

</details>

<details><summary>힌트 보기</summary>

성분 $k$의 열에서 $0$이 아닌 칸만 골라요. 그 관측과 $\mu_k^{\text{new}}$의 차를 제곱해 책임도를 곱하고, 더한 뒤 $N_k$로 나눠요.

</details>

<details><summary>풀이 보기</summary>

- (a) 성분 $1$은 $\mu_1^{\text{new}}=-2.7$에서 편차를 재요. 책임도가 $0$이 아닌 관측은 $-3,-2.5,-1,0$이에요.

  $$
  \sum_n r_{n1}(x_n+2.7)^2=0.09+0.04+0.057\cdot2.89+0.001\cdot7.29=0.30202
  $$

  $$
  (\sigma_1^{\text{new}})^2=\frac{0.30202}{2.058}\approx0.15
  $$
- (a) 성분 $2$는 $\mu_2^{\text{new}}=-0.4$에서 재요. 관측 $-1,0,2$만 남아요.

  $$
  \sum_n r_{n2}(x_n+0.4)^2=0.943\cdot0.36+0.999\cdot0.16+0.066\cdot5.76=0.87948
  $$

  $$
  (\sigma_2^{\text{new}})^2=\frac{0.87948}{2.008}\approx0.44
  $$
- (a) 성분 $3$은 $\mu_3^{\text{new}}=3.7$에서 재요. 관측 $2,4,5$만 남아요.

  $$
  \sum_n r_{n3}(x_n-3.7)^2=0.934\cdot2.89+0.09+1.69=4.47926
  $$

  $$
  (\sigma_3^{\text{new}})^2=\frac{4.47926}{2.934}\approx1.53
  $$
- (b) 갱신 전과 비교하면 $1\to0.15$, $0.2\to0.44$, $3\to1.53$이에요. 성분 $1$과 성분 $3$은 분산이 줄었고, 성분 $2$는 커졌어요.

  교과서는 반올림하기 전의 책임도로 계산해 성분 $1$의 새 분산을 $0.14$로 적었어요. 표의 반올림한 수로 계산하면 $0.15$가 나와요.

정답 (a) ${((\sigma_1^{\text{new}})^2,(\sigma_2^{\text{new}})^2,(\sigma_3^{\text{new}})^2)\approx(0.15,0.44,1.53)}$ (b) 성분 $1$·$3$은 줄고, 성분 $2$는 커져요.

</details>

---

<a id="p5"></a>

### P5. 수렴한 GMM을 초기값과 비교하기

관측값 $-3,-2.5,-1,0,2,4,5$에 성분 $3$개짜리 1차원 GMM을 EM으로 맞췄어요. 반복이 수렴해 얻은 GMM은 다음과 같아요.

$$
p(x)=0.29\,\mathcal{N}(x\mid-2.75,\,0.06)
$$

$$
\qquad+0.28\,\mathcal{N}(x\mid-0.50,\,0.25)
$$

$$
\qquad+0.43\,\mathcal{N}(x\mid3.64,\,1.63)
$$

$\mathcal{N}(x\mid\mu_k,\sigma_k^2)$에서 세로선 뒤 두 값은 평균과 분산이에요. 그래서 위 식의 $0.06$, $0.25$, $1.63$은 분산이에요.

EM을 시작한 초기값은 평균 $(\mu_1,\mu_2,\mu_3)=(-4,0,8)$, 분산 ${(\sigma_1^2,\sigma_2^2,\sigma_3^2)=(1,0.2,3)}$, 혼합 가중치 $\pi_1=\pi_2=\pi_3=\frac{1}{3}$이었어요.

- (a) 수렴한 GMM의 세 혼합 가중치를 더하면 $1$이 되는지 확인하고, 각 성분의 표준편차 $\sigma_k$를 소수점 아래 둘째 자리까지 구해 보세요.
- (b) 수렴한 GMM을 초기값과 비교해, 평균이 가장 많이 이동한 성분과 분산이 커진 성분을 골라 보세요.

<details><summary>교과서 원문 보기</summary>

“When we run EM on our example from Figure 11.3, we obtain the final result” — Example 11.6

</details>

<details><summary>힌트 보기</summary>

표준편차는 분산의 제곱근이에요. 이동 거리는 수렴한 평균과 초기 평균의 차의 절댓값이에요. 분산은 성분마다 초기값과 크기를 비교해요.

</details>

<details><summary>풀이 보기</summary>

- (a) 각 성분 앞의 계수가 혼합 가중치예요. 세 가중치를 더하면 $1$이에요.

  $$
  0.29+0.28+0.43=1
  $$
- (a) 표준편차는 분산 $0.06$, $0.25$, $1.63$의 제곱근이에요.

  $$
  \sigma_1=\sqrt{0.06}\approx0.24
  $$

  $$
  \sigma_2=\sqrt{0.25}=0.50
  $$

  $$
  \sigma_3=\sqrt{1.63}\approx1.28
  $$
- (b) 수렴한 평균에서 초기 평균을 빼 이동 거리를 재요.

  $$
  |-2.75-(-4)|=1.25
  $$

  $$
  |-0.50-0|=0.50
  $$

  $$
  |3.64-8|=4.36
  $$

  $4.36$이 가장 크므로 평균이 가장 많이 이동한 성분은 성분 $3$이에요.
- (b) 분산은 $1\to0.06$, $0.2\to0.25$, $3\to1.63$으로 바뀌었어요. 성분 $1$과 성분 $3$은 분산이 줄었고, 커진 성분은 성분 $2$뿐이에요.

정답 (a) 가중치 합은 $1$이고, 표준편차는 ${(\sigma_1,\sigma_2,\sigma_3)\approx(0.24,0.50,1.28)}$ (b) 평균이 가장 많이 이동한 성분은 성분 $3$(이동 거리 $4.36$), 분산이 커진 성분은 성분 $2$예요.

</details>

---

<a id="p6"></a>

### P6. 최소제곱 손실의 기울기와 차원

선형모형 ${\mathbf{y}=\boldsymbol{\Phi}\boldsymbol{\theta}}$를 생각해요. 파라미터 $\boldsymbol{\theta}\in\mathbb{R}^{D}$와 관측 $\mathbf{y}\in\mathbb{R}^{N}$은 열벡터이고, 입력 특징 행렬은 $\boldsymbol{\Phi}\in\mathbb{R}^{N\times D}$예요. 두 함수를 다음처럼 정의해요.

$$
L(\mathbf{e})=\|\mathbf{e}\|^2
$$

$$
\mathbf{e}(\boldsymbol{\theta})=\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}
$$

미분은 수업 관례를 따라요. 스칼라를 열벡터로 미분한 결과는 행벡터예요. 벡터 $\mathbf{e}$를 벡터 $\boldsymbol{\theta}$로 미분한 결과는 $(i,j)$ 성분이 $\partial e_i/\partial\theta_j$인 행렬이에요.

- (a) 연쇄법칙 ${\frac{\partial L}{\partial\boldsymbol{\theta}}=\frac{\partial L}{\partial\mathbf{e}}\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}}$를 써서 $\frac{\partial L}{\partial\boldsymbol{\theta}}$를 $\mathbf{e}$와 $\boldsymbol{\Phi}$로 나타내 보세요.
- (b) (a)에서 구한 $\frac{\partial L}{\partial\mathbf{e}}$, $\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$, $\frac{\partial L}{\partial\boldsymbol{\theta}}$의 차원을 각각 읽어 보세요.

<details><summary>교과서 원문 보기</summary>

“We seek ∂L/∂θ, and we will use the chain rule for this purpose.” — Example 5.11

</details>

<details><summary>힌트 보기</summary>

${\|\mathbf{e}\|^2=\mathbf{e}^\top\mathbf{e}}$를 성분의 제곱합으로 쓰면 $\partial L/\partial e_n$이 바로 나와요. $e_n$을 $\theta_d$로 미분하면 $\boldsymbol{\Phi}$의 성분이 남아요.

</details>

<details><summary>풀이 보기</summary>

- (a) $L$을 성분으로 쓰면 $e_n$에 대한 편미분이 바로 보여요. 스칼라를 열벡터로 미분했으니 결과를 행벡터로 모아요.

  $$
  L=\mathbf{e}^\top\mathbf{e}=\sum_{n=1}^{N}e_n^2
  $$

  $$
  \frac{\partial L}{\partial e_n}=2e_n
  $$

  $n$번째 칸에 $2e_n$을 둔 행벡터는 열벡터 $2\mathbf{e}$를 전치한 것과 같아요.

  $$
  \frac{\partial L}{\partial\mathbf{e}}=2\mathbf{e}^\top
  $$
- (a) $\mathbf{e}$의 성분 하나를 펼치면 $\theta_d$ 앞의 계수가 보여요. $\mathbf{y}$는 $\boldsymbol{\theta}$와 무관해서 미분하면 $0$이에요.

  $$
  e_n=y_n-\sum_{d=1}^{D}\Phi_{nd}\theta_d
  $$

  $$
  \frac{\partial e_n}{\partial\theta_d}=-\Phi_{nd}
  $$

  $$
  \frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}=-\boldsymbol{\Phi}
  $$
- (a) 두 결과를 연쇄법칙 순서대로 곱해요. 마지막에 $\mathbf{e}$의 정의를 넣어도 돼요.

  $$
  \frac{\partial L}{\partial\boldsymbol{\theta}}=2\mathbf{e}^\top(-\boldsymbol{\Phi})=-2\mathbf{e}^\top\boldsymbol{\Phi}=-2(\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta})^\top\boldsymbol{\Phi}
  $$
- (b) ${\mathbf{e}=\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}}$는 $N\times1$ 열벡터라서 $2\mathbf{e}^\top$은 $1\times N$ 행벡터예요. $-\boldsymbol{\Phi}$는 행이 $e_1,\dots,e_N$, 열이 $\theta_1,\dots,\theta_D$에 대응해서 $N\times D$예요.

  $$
  \underbrace{2\mathbf{e}^\top}_{1\times N}\;\underbrace{(-\boldsymbol{\Phi})}_{N\times D}\in\mathbb{R}^{1\times D}
  $$

  안쪽 $N$이 맞아야 곱이 정의되므로 순서는 $\mathbf{e}^\top\boldsymbol{\Phi}$예요. $\boldsymbol{\theta}$는 $D\times1$ 열벡터이지만, 스칼라 $L$을 $\boldsymbol{\theta}$로 미분한 결과는 $1\times D$ 행벡터예요.

정답 (a) ${\frac{\partial L}{\partial\boldsymbol{\theta}}=-2\mathbf{e}^\top\boldsymbol{\Phi}}$ (b) ${\frac{\partial L}{\partial\mathbf{e}}\in\mathbb{R}^{1\times N}}$, ${\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}\in\mathbb{R}^{N\times D}}$, ${\frac{\partial L}{\partial\boldsymbol{\theta}}\in\mathbb{R}^{1\times D}}$

</details>

---

<a id="p7"></a>

### P7. 분수로 분산 갱신하기

1차원 관측 $x_1,\dots,x_7$에 성분 $3$개짜리 GMM을 맞추고 있어요. E-step에서 구한 책임도 $r_{nk}$가 아래 표에 있어요. 행은 관측 $x_n$, 열은 성분 $k=1,2,3$이에요.

| $x_n$ | $r_{n1}$ | $r_{n2}$ | $r_{n3}$ |
|---|---|---|---|
| $-4$ | $1$ | $0$ | $0$ |
| $-2$ | $1$ | $0$ | $0$ |
| $-1$ | $\frac{1}{2}$ | $\frac{1}{2}$ | $0$ |
| $0$ | $0$ | $1$ | $0$ |
| $2$ | $0$ | $\frac{1}{2}$ | $\frac{1}{2}$ |
| $4$ | $0$ | $0$ | $1$ |
| $6$ | $0$ | $0$ | $1$ |

총 책임도는 ${(N_1,N_2,N_3)=\left(\frac{5}{2},2,\frac{5}{2}\right)}$예요. 이미 갱신된 평균은 ${(\mu_1^{\text{new}},\mu_2^{\text{new}},\mu_3^{\text{new}})=\left(-\frac{13}{5},\frac{1}{4},\frac{22}{5}\right)}$이에요. 갱신 전 분산은 ${(\sigma_1^2,\sigma_2^2,\sigma_3^2)=\left(2,\frac{1}{2},3\right)}$이에요. 분산 갱신식은 다음과 같아요.

$$
(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}(x_n-\mu_k^{\text{new}})^2
$$

- (a) 세 성분의 새 분산 $(\sigma_k^{\text{new}})^2$을 기약분수로 구해 보세요.
- (b) (a)의 결과를 갱신 전 분산과 비교해, 분산이 줄어든 성분과 커진 성분을 골라 보세요.

<details><summary>교과서 원문 보기</summary>

“In our example from Figure 11.3, the variances are updated as follows” — Example 11.4

</details>

<details><summary>힌트 보기</summary>

성분 $k$의 열에서 $0$이 아닌 칸만 골라요. 편차를 분수로 두고 제곱해 책임도를 곱한 뒤, 합을 $N_k$로 나눠요.

</details>

<details><summary>풀이 보기</summary>

- (a) 성분 $1$은 관측 $-4,-2,-1$만 남아요. $\mu_1^{\text{new}}=-\frac{13}{5}$에서 편차는 차례로 $-\frac{7}{5}$, $\frac{3}{5}$, $\frac{8}{5}$이에요.

  $$
  \sum_n r_{n1}(x_n-\mu_1^{\text{new}})^2=\frac{49}{25}+\frac{9}{25}+\frac{1}{2}\cdot\frac{64}{25}=\frac{90}{25}=\frac{18}{5}
  $$

  $$
  (\sigma_1^{\text{new}})^2=\frac{18/5}{5/2}=\frac{36}{25}
  $$
- (a) 성분 $2$는 관측 $-1,0,2$만 남아요. $\mu_2^{\text{new}}=\frac{1}{4}$에서 편차는 $-\frac{5}{4}$, $-\frac{1}{4}$, $\frac{7}{4}$이에요.

  $$
  \sum_n r_{n2}(x_n-\mu_2^{\text{new}})^2=\frac{1}{2}\cdot\frac{25}{16}+\frac{1}{16}+\frac{1}{2}\cdot\frac{49}{16}=\frac{76}{32}=\frac{19}{8}
  $$

  $$
  (\sigma_2^{\text{new}})^2=\frac{19/8}{2}=\frac{19}{16}
  $$
- (a) 성분 $3$은 관측 $2,4,6$만 남아요. $\mu_3^{\text{new}}=\frac{22}{5}$에서 편차는 $-\frac{12}{5}$, $-\frac{2}{5}$, $\frac{8}{5}$이에요.

  $$
  \sum_n r_{n3}(x_n-\mu_3^{\text{new}})^2=\frac{1}{2}\cdot\frac{144}{25}+\frac{4}{25}+\frac{64}{25}=\frac{140}{25}=\frac{28}{5}
  $$

  $$
  (\sigma_3^{\text{new}})^2=\frac{28/5}{5/2}=\frac{56}{25}
  $$
- (b) 소수로 바꿔 비교해요. $\frac{36}{25}=1.44\lt2$, $\frac{19}{16}=1.1875\gt\frac{1}{2}$, $\frac{56}{25}=2.24\lt3$이에요. 성분 $1$과 성분 $3$은 분산이 줄었고, 성분 $2$는 커졌어요.

정답 (a) $\frac{36}{25}$, $\frac{19}{16}$, $\frac{56}{25}$ (b) 성분 $1$·$3$은 줄고, 성분 $2$는 커져요.

</details>

---

<a id="partB"></a>

## B. 교과서 연습문제

<a id="p8"></a>

### P8. 벡터와 행렬로 스칼라 함수 미분하기

두 스칼라 함수를 생각해요.

$$
f(\mathbf{t})=\sin\bigl(\log(\mathbf{t}^\top\mathbf{t})\bigr)
$$

$$
g(\mathbf{X})=\operatorname{tr}(\mathbf{A}\mathbf{X}\mathbf{B})
$$

크기는 ${\mathbf{t}\in\mathbb{R}^{D}}$, ${\mathbf{A}\in\mathbb{R}^{D\times E}}$, ${\mathbf{X}\in\mathbb{R}^{E\times F}}$, ${\mathbf{B}\in\mathbb{R}^{F\times D}}$예요.

$\mathbf{t}$는 영벡터가 아닌 열벡터예요. $\mathbf{A}\mathbf{X}\mathbf{B}$는 $D\times D$ 정사각행렬이고, $\operatorname{tr}$은 정사각행렬의 대각 성분을 모두 더한 대각합(trace)이에요.

미분은 수업 관례를 따라요. 스칼라를 열벡터로 미분한 결과는 행벡터예요. 스칼라를 행렬 $\mathbf{X}$로 미분한 결과는 $\mathbf{X}$의 각 원소 $X_{pq}$에 대한 편미분 $\partial g/\partial X_{pq}$를 같은 $(p,q)$ 자리에 둔 행렬이에요.

- (a) $f$를 $\mathbf{t}$로 미분한 $\frac{df}{d\mathbf{t}}$를 구해 보세요.
- (b) $g$를 $\mathbf{X}$로 미분한 $\frac{dg}{d\mathbf{X}}$를 $\mathbf{A}$와 $\mathbf{B}$로 나타내 보세요.
- (c) (a)와 (b)에서 구한 두 미분의 차원을 각각 읽어 보세요.

<details><summary>교과서 원문 보기</summary>

“Differentiate f with respect to t and g with respect to X” — Exercise 5.6

</details>

<details><summary>힌트 보기</summary>

(a)는 $u=\mathbf{t}^\top\mathbf{t}$로 놓고 연쇄법칙을 써요. (b)는 대각합을 행렬 성분의 합으로 펼친 뒤 원소 하나 $X_{pq}$로 미분해요.

</details>

<details><summary>풀이 보기</summary>

- (a) 안쪽 스칼라에 ${u=\mathbf{t}^\top\mathbf{t}=\sum_{d=1}^{D}t_d^2}$라는 이름을 붙여요. $\partial u/\partial t_d=2t_d$를 행벡터로 모아요.

  $$
  \frac{du}{d\mathbf{t}}=2\mathbf{t}^\top
  $$
- (a) 바깥 함수 $f=\sin(\log u)$는 $u$ 하나의 함수예요. $\sin$과 $\log$를 차례로 미분해요.

  $$
  \frac{df}{du}=\cos(\log u)\cdot\frac{1}{u}
  $$
- (a) 연쇄법칙으로 두 결과를 곱하고 $u=\mathbf{t}^\top\mathbf{t}$를 다시 넣어요.

  $$
  \frac{df}{d\mathbf{t}}=\frac{df}{du}\frac{du}{d\mathbf{t}}=\frac{2\cos\bigl(\log(\mathbf{t}^\top\mathbf{t})\bigr)}{\mathbf{t}^\top\mathbf{t}}\,\mathbf{t}^\top
  $$
- (b) 행렬곱의 $(i,i)$ 성분을 펼쳐요. 여기서 $i$는 $1$부터 $D$, $j$는 $1$부터 $E$, $l$은 $1$부터 $F$까지 도는 합의 첨자예요. 먼저 $\mathbf{A}\mathbf{X}$의 성분을 행×열 곱으로 쓰고, 그 결과에 $\mathbf{B}$를 한 번 더 행×열로 곱해요.

  $$
  (\mathbf{A}\mathbf{X})_{il}=\sum_{j=1}^{E}A_{ij}X_{jl}
  $$

  $$
  (\mathbf{A}\mathbf{X}\mathbf{B})_{ii}=\sum_{l=1}^{F}(\mathbf{A}\mathbf{X})_{il}B_{li}=\sum_{j=1}^{E}\sum_{l=1}^{F}A_{ij}X_{jl}B_{li}
  $$

  대각합은 이 대각 성분을 $i$에 대해 모두 더한 값이에요.

  $$
  g=\operatorname{tr}(\mathbf{A}\mathbf{X}\mathbf{B})=\sum_{i=1}^{D}\sum_{j=1}^{E}\sum_{l=1}^{F}A_{ij}X_{jl}B_{li}
  $$
- (b) 원소 하나 $X_{pq}$를 고정해요. $X_{pq}$가 들어 있는 항은 $j=p$, $l=q$인 항으로, $i$마다 하나씩이에요. 나머지 항은 미분하면 $0$이에요.

  $$
  \frac{\partial g}{\partial X_{pq}}=\sum_{i=1}^{D}A_{ip}B_{qi}
  $$
- (b) 첨자 순서를 행렬곱 꼴로 맞춰요. $A_{ip}=(\mathbf{A}^\top)_{pi}$, $B_{qi}=(\mathbf{B}^\top)_{iq}$예요.

  $$
  \frac{\partial g}{\partial X_{pq}}=\sum_{i=1}^{D}(\mathbf{A}^\top)_{pi}(\mathbf{B}^\top)_{iq}=(\mathbf{A}^\top\mathbf{B}^\top)_{pq}
  $$

  $(p,q)$ 자리에 이 값을 두면 행렬 전체가 나와요.

  $$
  \frac{dg}{d\mathbf{X}}=\mathbf{A}^\top\mathbf{B}^\top
  $$
- (c) (a)의 결과는 스칼라 $\frac{2\cos(\log(\mathbf{t}^\top\mathbf{t}))}{\mathbf{t}^\top\mathbf{t}}$에 $1\times D$ 행벡터 $\mathbf{t}^\top$을 곱한 것이라 $\mathbb{R}^{1\times D}$예요. (b)의 결과는 $(E\times D)(D\times F)$ 곱이라 $\mathbb{R}^{E\times F}$이고, $\mathbf{X}$와 모양이 같아요.

정답 (a) ${\frac{df}{d\mathbf{t}}=\frac{2\cos(\log(\mathbf{t}^\top\mathbf{t}))}{\mathbf{t}^\top\mathbf{t}}\mathbf{t}^\top}$ (b) ${\frac{dg}{d\mathbf{X}}=\mathbf{A}^\top\mathbf{B}^\top}$ (c) ${\frac{df}{d\mathbf{t}}\in\mathbb{R}^{1\times D}}$, ${\frac{dg}{d\mathbf{X}}\in\mathbb{R}^{E\times F}}$

</details>

---

출처: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* (Cambridge University Press, 2020). 풀이는 자체 작성이며 수치는 Python으로 검증했습니다.
