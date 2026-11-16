# 머신러닝기초 복습 1116 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [P1. 총 책임도로 혼합 가중치 갱신하기](#p1)
  - [P2. 책임도 표로 평균 갱신하기](#p2)
  - [P3. 교과서 책임도 표로 평균 갱신하기](#p3)
  - [P4. 갱신된 평균으로 분산 갱신하기](#p4)
  - [P5. 수렴한 GMM을 초기값과 비교하기](#p5)
  - [P6. 최소제곱 손실의 기울기와 차원](#p6)
  - [P7. 분수로 분산 갱신하기](#p7)
  - [P8. 벡터와 행렬로 스칼라 함수 미분하기](#p8)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### P1. 총 책임도로 혼합 가중치 갱신하기

MML Example 11.5 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=1)

#### 주어진 조건

관측 $7$개에 성분 $3$개짜리 GMM을 맞추고 있어요. 갱신 전 혼합 가중치는 $\pi_1=\pi_2=\pi_3=\frac{1}{3}$이에요.

E-step에서 구한 성분별 총 책임도 $N_k=\sum_{n=1}^{7} r_{nk}$는 다음과 같아요.

${N_1=2.058}$, ${N_2=2.008}$, ${N_3=2.934}$

EM의 M-step 가중치 갱신식은 다음과 같이 주어져요. 여기서 $N$은 관측의 개수예요.

$$
\pi_k^{\text{new}}=\frac{N_k}{N}
$$

#### 구할 것

- (a) 세 성분의 새 가중치 $\pi_k^{\text{new}}$를 소수점 아래 셋째 자리까지 구해 보세요.
- (b) (a)의 세 값을 더하면 $1$이 되는지 확인하고, 갱신 전 $\frac{1}{3}$보다 커진 성분을 골라 보세요.

<details><summary>원문 보기</summary>

“Here we see that the third component gets more weight/importance, while the other components become slightly less important.” — Example 11.5

</details>

#### 문제에서 주어진 것과 구할 것

주어진 것: 관측 수 $N=7$, 성분 $3$개의 총 책임도 $N_1=2.058$, $N_2=2.008$, $N_3=2.934$, 갱신 전 가중치 $\pi_k=\frac{1}{3}$, 그리고 M-step 식 $\pi_k^{\text{new}}=\frac{N_k}{N}$이에요.

구할 것: (a) 세 $\pi_k^{\text{new}}$를 소수점 아래 셋째 자리까지, (b) 세 값의 합이 $1$인지와 $\frac{1}{3}$보다 커진 성분이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘총 책임도 $N_k$’와 ‘혼합 가중치 갱신’이라는 단서에서 M-step의 **혼합 가중치(mixing weight) 갱신식**을 떠올려요. 이 문제에서는 식이 주어져 있으니 대입만 하면 돼요.

$$
\pi_k^{\text{new}}=\frac{\overbrace{N_k}^{\text{성분 }k\text{가 맡은 몫}}}{\underbrace{N}_{\text{전체 관측 수}}}
$$

- $N_k=\sum_{n=1}^{N} r_{nk}$는 책임도 표의 열 $k$를 더한 값이에요. 확률을 여러 개 더한 값이라 정수가 아니어도 되고 $1$보다 클 수 있어요.
- 책임도 표의 각 행은 합이 $1$이라서, 표 전체를 더하면 $\sum_{k}N_k=N$이에요. 그래서 새 가중치의 합은 저절로 $1$이 돼요.

E-step의 책임도 표에서 열 합이 $N_k$, 전체 합이 $N$이라는 구조는 [E-step과 M-step의 순서](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-em-steps)에서, 비율의 뜻은 [비율: 전체 몫 중 성분 k의 몫](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-pi)에서 다뤘어요.

#### 종이에 적을 첫 줄

$N=7$을 먼저 적고, 첫 성분부터 $\pi_1^{\text{new}}=\frac{2.058}{7}$로 시작해요.

풀이 로드맵: 1. $N_k$를 $7$로 나눠 세 가중치 계산 → 2. 분자 합 $\sum_k N_k$로 합이 $1$인지 확인 → 3. 세 값을 $\frac{1}{3}\approx0.333$과 비교해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** $(\pi_1^{\text{new}},\pi_2^{\text{new}},\pi_3^{\text{new}})=(0.294,\,0.287,\,0.419)$예요.

대표로 성분 $1$은 $\pi_1^{\text{new}}=\frac{2.058}{7}=0.294$예요. 세 성분을 같은 방법으로 표에 정리해요.

| 성분 $k$ | $N_k$ | $N_k/7$ | 셋째 자리 반올림 |
|---|---|---|---|
| $1$ | $2.058$ | $0.294$ | $0.294$ |
| $2$ | $2.008$ | $0.28686\ldots$ | $0.287$ |
| $3$ | $2.934$ | $0.41914\ldots$ | $0.419$ |

모든 성분을 같은 $N=7$로 나누므로, 총 책임도가 큰 성분일수록 새 가중치도 커요.

#### (b)

**최종 답 요약:** 합은 정확히 $1$이고, $\frac{1}{3}$보다 커진 성분은 성분 $3$뿐이에요.

반올림 전 값으로 더하면 분자끼리 먼저 더할 수 있어요. $\frac{2.058+2.008+2.934}{7}=\frac{7}{7}=1$이에요. 반올림한 값도 $0.294+0.287+0.419=1.000$이에요.

$\frac{1}{3}\approx0.333$과 비교하면 $0.294$와 $0.287$은 작고 $0.419$만 커요. 같은 말로 $N_k\gt\frac{7}{3}\approx2.333$인 성분은 $N_3=2.934$뿐이에요.

#### 완성 답과 검산

#### (a) 검산

거꾸로 곱해 봐요. $0.294\times7=2.058$, $0.287\times7=2.009$, $0.419\times7=2.933$으로 주어진 $N_k$와 반올림 오차 안에서 맞아요.

#### (b) 검산

$\sum_k N_k=7=N$이 성립하므로 합 $1$은 반올림과 무관한 정확한 값이에요.

#### 여기서 헷갈리기 쉬워요

분모는 성분 개수 $K=3$이 아니라 관측 수 $N=7$이에요. $N_k$를 $3$으로 나누면 합이 $\frac{7}{3}$이 되어 확률이 될 수 없어요.

(b)의 합 확인을 반올림한 값으로만 하면 $1.000$이 우연처럼 보여요. 분자 합 $\sum_kN_k=N$에서 정확히 $1$임을 설명해요.

#### 다시 풀 때 확인할 것

1. 분모에 들어갈 $N$이 관측 수인지 확인하고 $\pi_k^{\text{new}}=N_k/N$을 적어요.
2. $\sum_k N_k=N$으로 새 가중치 합이 $1$임을 한 줄로 보여요.
3. $N_k$와 $N/K=\frac{7}{3}$을 비교해 커진 성분을 골라요.

**페이지 요약**

#### 떠올릴 개념·공식

주어진 M-step 식 $\pi_k^{\text{new}}=N_k/N$에서 $N$은 관측 수 $7$이에요. $N_k$는 책임도 표의 열 합이고, 열 합을 모두 더하면 $N$이에요.

#### 결론과 검산

새 가중치는 $(0.294,\,0.287,\,0.419)$이고, 분자 합이 $7$이라 합은 정확히 $1$이에요. $\frac{1}{3}$보다 커진 것은 성분 $3$뿐이에요.

#### 용어

- **혼합 가중치(mixing weight) $\pi_k$** — GMM에서 성분 $k$를 고를 확률이에요. $\pi_k\ge0$이고 $\sum_k\pi_k=1$이에요.
- **총 책임도(total responsibility) $N_k$** — $N_k=\sum_{n=1}^{N}r_{nk}$로, 책임도 표의 열 $k$의 합이에요. 성분 $k$가 데이터 전체에서 맡은 관측 수 분량이고 정수가 아니어도 돼요.
- **M-step** — E-step에서 구한 책임도를 고정하고 $\boldsymbol{\mu}_k$, $\Sigma_k$, $\pi_k$를 다시 계산하는 단계예요.

#### 출제 근거

MML Example 11.5(혼합 가중치 갱신), 교과서 360쪽(PDF 366쪽)과 Example 11.2의 $N_1=2.058$, $N_2=2.008$, $N_3=2.934$(교과서 353쪽, PDF 359쪽).

수업: 1116 L07 s12의 M-step 식. 관련 정리노트: [비율: 전체 몫 중 성분 k의 몫](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-pi)

---

<a id="p2"></a>

### P2. 책임도 표로 평균 갱신하기

MML Example 11.3 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=2)

#### 주어진 조건

1차원 관측 $x_1,\dots,x_7$에 성분 $3$개짜리 GMM을 맞추고 있어요. E-step에서 구한 책임도 $r_{nk}$가 아래 표에 있어요. 행은 관측 $x_n$, 열은 성분 $k=1,2,3$이에요.

M-step의 평균 갱신식은 다음과 같아요.

$$
\mu_k^{\text{new}}=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}x_n
$$

#### 구할 것

- (a) 세 성분의 총 책임도 $N_k=\sum_{n=1}^{7} r_{nk}$를 구해 보세요.
- (b) (a)의 $N_k$를 써서 세 성분의 새 평균 $\mu_k^{\text{new}}$를 구해 보세요.

| $x_n$ | $r_{n1}$ | $r_{n2}$ | $r_{n3}$ |
|---|---|---|---|
| $-4$ | $1$ | $0$ | $0$ |
| $-2$ | $1$ | $0$ | $0$ |
| $-1$ | $\frac{1}{2}$ | $\frac{1}{2}$ | $0$ |
| $0$ | $0$ | $1$ | $0$ |
| $2$ | $0$ | $\frac{1}{2}$ | $\frac{1}{2}$ |
| $4$ | $0$ | $0$ | $1$ |
| $6$ | $0$ | $0$ | $1$ |

<details><summary>원문 보기</summary>

“In our example from Figure 11.3, the mean values are updated as follows” — Example 11.3

</details>

#### 문제에서 주어진 것과 구할 것

주어진 것: 관측 $x_n\in\{-4,-2,-1,0,2,4,6\}$과 $7\times3$ 책임도 표 $r_{nk}$(행 $n$은 관측, 열 $k$는 성분), 평균 갱신식 $\mu_k^{\text{new}}=\frac{1}{N_k}\sum_n r_{nk}x_n$이에요.

구할 것: (a) 열 합 $N_k=\sum_n r_{nk}$, (b) 그 $N_k$로 나눈 새 평균 $\mu_k^{\text{new}}$예요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘책임도 표’와 ‘평균 갱신’이라는 단서에서 E-step이 만든 $N\times K$ 표를 M-step이 **열 단위로** 쓴다는 점을 떠올려요.

- **총 책임도** $N_k$: 표의 열 $k$를 위에서 아래로 더한 값이에요. 각 행의 합은 $1$이므로 세 $N_k$를 모두 더하면 관측 수 $7$이에요.
- **가중 평균(weighted average)**: 평균 갱신식은 가중치 $r_{nk}/N_k$로 관측을 평균한 값이에요.

$$
\mu_k^{\text{new}}=\frac{\overbrace{\sum_{n} r_{nk}x_n}^{\text{열 }k\text{로 가중한 관측의 합}}}{\underbrace{N_k}_{\text{열 }k\text{의 합}}}=\sum_n\frac{r_{nk}}{N_k}x_n,\qquad\sum_n\frac{r_{nk}}{N_k}=1
$$

$N$이 아니라 $N_k$로 나눠야 가중치 합이 $1$이 되고, 그래서 새 평균은 그 성분이 맡은 관측들 사이에 놓여요. 표의 구조는 [E-step과 M-step의 순서](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-em-steps), 가중 평균의 뜻은 [평균: 합이 1인 가중치로 낸 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-mean)에서 다뤘어요.

#### 종이에 적을 첫 줄

표 아래에 열 합 줄을 하나 더 그리고, 첫 칸에 $N_1=1+1+\frac{1}{2}+0+0+0+0$을 적어요.

풀이 로드맵: 1. 세 열의 합 $N_k$ → 2. 열마다 $\sum_n r_{nk}x_n$ 계산 → 3. 그 합을 $N_k$로 나눠 $\mu_k^{\text{new}}$를 구해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** $(N_1,N_2,N_3)=\left(\frac{5}{2},\,2,\,\frac{5}{2}\right)$예요.

대표로 열 $1$은 $0$이 아닌 칸만 더해 $N_1=1+1+\frac{1}{2}=\frac{5}{2}$예요. 세 열을 표로 정리해요.

| 성분 $k$ | $0$이 아닌 칸 ($x_n$: $r_{nk}$) | $N_k$ |
|---|---|---|
| $1$ | $-4$: $1$, $-2$: $1$, $-1$: $\frac{1}{2}$ | $\frac{5}{2}$ |
| $2$ | $-1$: $\frac{1}{2}$, $0$: $1$, $2$: $\frac{1}{2}$ | $2$ |
| $3$ | $2$: $\frac{1}{2}$, $4$: $1$, $6$: $1$ | $\frac{5}{2}$ |

세 값의 합은 $\frac{5}{2}+2+\frac{5}{2}=7$로 관측 수와 같아요. 관측 $-1$과 $2$는 두 성분이 반씩 나눠 맡아서 $N_k$가 정수가 아닐 수 있어요.

#### (b)

**최종 답 구조:** $(\mu_1^{\text{new}},\mu_2^{\text{new}},\mu_3^{\text{new}})=(-2.6,\,0.25,\,4.4)$, 분수로는 $\left(-\frac{13}{5},\,\frac{1}{4},\,\frac{22}{5}\right)$예요.

대표로 성분 $1$은 $\sum_n r_{n1}x_n=1\cdot(-4)+1\cdot(-2)+\frac{1}{2}\cdot(-1)=-\frac{13}{2}$이고, $\mu_1^{\text{new}}=\frac{-13/2}{5/2}=-\frac{13}{5}=-2.6$이에요.

| 성분 $k$ | $\sum_n r_{nk}x_n$ | $N_k$ | $\mu_k^{\text{new}}$ |
|---|---|---|---|
| $1$ | $-4-2-\frac{1}{2}=-\frac{13}{2}$ | $\frac{5}{2}$ | $-\frac{13}{5}=-2.6$ |
| $2$ | $-\frac{1}{2}+0+1=\frac{1}{2}$ | $2$ | $\frac{1}{4}=0.25$ |
| $3$ | $1+4+6=11$ | $\frac{5}{2}$ | $\frac{22}{5}=4.4$ |

각 평균은 그 성분이 맡은 관측들 사이에 놓여요. 성분 $1$은 $[-4,-1]$, 성분 $2$는 $[-1,2]$, 성분 $3$은 $[2,6]$ 안에 있어요.

#### 완성 답과 검산

#### (a) 검산

행마다 합이 $1$인지 보면 일곱 행 모두 $1$이에요. 그러면 표 전체 합은 $7$이어야 하고, 실제로 $\sum_kN_k=7$이에요.

#### (b) 검산

가중 편차의 합이 $0$인지 확인해요. 성분 $2$는 $\frac{1}{2}\left(-1-\frac{1}{4}\right)+1\left(0-\frac{1}{4}\right)+\frac{1}{2}\left(2-\frac{1}{4}\right)=-\frac{5}{8}-\frac{2}{8}+\frac{7}{8}=0$이에요. 가중 평균이면 $\sum_n r_{nk}(x_n-\mu_k^{\text{new}})=0$이 성립해야 해요.

#### 여기서 헷갈리기 쉬워요

$N_k$는 행 합이 아니라 **열 합**이에요. 행 합은 언제나 $1$이라 새 정보를 주지 않아요.

나눌 때 관측 수 $7$이나 그 성분의 $0$이 아닌 칸 수 $3$을 쓰면 안 돼요. 반씩 맡은 관측은 $\frac{1}{2}$개로 세야 하므로 분모는 $N_k$예요.

#### 다시 풀 때 확인할 것

1. 표 아래에 열 합 줄을 그리고 $\sum_kN_k=7$을 확인해요.
2. 같은 열의 $r_{nk}$를 $x_n$에 곱해 더한 뒤 $N_k$로 나눠요.
3. 결과가 그 성분이 맡은 관측들 사이에 있는지 봐요.

**페이지 요약**

#### 떠올릴 개념·공식

$N_k$는 책임도 표의 열 합이에요. $\mu_k^{\text{new}}=\frac{1}{N_k}\sum_nr_{nk}x_n$은 합이 $1$인 가중치 $r_{nk}/N_k$로 낸 가중 평균이에요.

#### 결론과 검산

$N_k=\left(\frac{5}{2},2,\frac{5}{2}\right)$로 합이 $7$이에요. 새 평균은 $(-2.6,\,0.25,\,4.4)$이고, 가중 편차의 합이 $0$인지로 확인해요.

#### 용어

- **책임도(responsibility) $r_{nk}$** — 관측 $x_n$을 성분 $k$가 맡는 몫이에요. 한 행의 합은 $\sum_kr_{nk}=1$이에요.
- **총 책임도 $N_k$** — $N_k=\sum_nr_{nk}$, 책임도 표의 열 합이에요. 모두 더하면 관측 수 $N$이에요.
- **가중 평균(weighted average)** — 합이 $1$인 가중치 $r_{nk}/N_k$로 관측을 평균한 값이에요. 많이 맡은 관측일수록 평균을 세게 끌어요.

#### 출제 근거

MML Example 11.3(평균 갱신), 교과서 355쪽(PDF 361쪽)의 계산 구조를 분수로 끝나는 책임도 표로 바꾼 문항이에요.

관련 정리노트: [평균: 합이 1인 가중치로 낸 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-mean)

---

<a id="p3"></a>

### P3. 교과서 책임도 표로 평균 갱신하기

MML Example 11.3 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=3)

#### 주어진 조건

관측값은 $-3,-2.5,-1,0,2,4,5$예요. 성분 $3$개짜리 GMM의 갱신 전 평균은 $\mu_1=-4$, $\mu_2=0$, $\mu_3=8$이에요. E-step에서 구한 책임도 $r_{nk}$가 반올림되어 아래 표에 있어요. 행은 관측 $x_n$, 열은 성분 $k=1,2,3$이에요. 표에 적힌 수로 계산해요.

M-step의 평균 갱신식은 다음과 같아요. 여기서 $N_k=\sum_{n=1}^{7} r_{nk}$예요.

$$
\mu_k^{\text{new}}=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}x_n
$$

#### 구할 것

- (a) 세 성분의 새 평균 $\mu_k^{\text{new}}$를 소수점 아래 둘째 자리까지 구해 보세요.
- (b) (a)의 결과로 갱신 전후 평균의 이동 거리 $|\mu_k^{\text{new}}-\mu_k|$를 구하고, 가장 많이 움직인 성분을 골라 보세요.

| $x_n$ | $r_{n1}$ | $r_{n2}$ | $r_{n3}$ |
|---|---|---|---|
| $-3$ | $1.0$ | $0.0$ | $0.0$ |
| $-2.5$ | $1.0$ | $0.0$ | $0.0$ |
| $-1$ | $0.057$ | $0.943$ | $0.0$ |
| $0$ | $0.001$ | $0.999$ | $0.0$ |
| $2$ | $0.0$ | $0.066$ | $0.934$ |
| $4$ | $0.0$ | $0.0$ | $1.0$ |
| $5$ | $0.0$ | $0.0$ | $1.0$ |

<details><summary>원문 보기</summary>

“Here we see that the means of the first and third mixture component move toward the regime of the data” — Example 11.3

</details>

#### 문제에서 주어진 것과 구할 것

주어진 것: 관측 $-3,-2.5,-1,0,2,4,5$, 갱신 전 평균 $(\mu_1,\mu_2,\mu_3)=(-4,0,8)$, 반올림된 $7\times3$ 책임도 표, 평균 갱신식 $\mu_k^{\text{new}}=\frac{1}{N_k}\sum_nr_{nk}x_n$이에요. 표에 적힌 수로 계산해요.

구할 것: (a) 세 $\mu_k^{\text{new}}$를 소수점 아래 둘째 자리까지, (b) 이동 거리 $|\mu_k^{\text{new}}-\mu_k|$와 가장 많이 움직인 성분이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘책임도 표로 평균 갱신’이라는 단서에서 M-step의 **책임도 가중 평균**을 떠올려요. 표의 열 $k$ 하나만 써요.

$$
\mu_k^{\text{new}}=\frac{\overbrace{\sum_{n=1}^{7} r_{nk}x_n}^{\text{열 }k\text{로 가중한 합}}}{\underbrace{N_k=\sum_{n=1}^{7} r_{nk}}_{\text{열 }k\text{의 합}}}
$$

- 분자와 분모 모두 같은 열 $k$의 책임도를 써요. 분모 $N_k$로 나누므로 가중치 $r_{nk}/N_k$의 합이 $1$이에요.
- 새 평균에는 갱신 전 평균 $\mu_k$가 직접 들어가지 않아요. $\mu_k$는 E-step에서 책임도를 만들 때 이미 쓰였고, (b)에서 비교 기준으로만 다시 써요.

가중 평균의 뜻은 [평균: 합이 1인 가중치로 낸 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-mean)에서 다뤘어요.

#### 종이에 적을 첫 줄

열마다 $0$이 아닌 칸만 골라 $N_1=1.0+1.0+0.057+0.001$을 먼저 적어요.

풀이 로드맵: 1. 열 합 $N_k$ → 2. 가중합 $\sum_nr_{nk}x_n$ → 3. 나눠서 반올림한 $\mu_k^{\text{new}}$와 갱신 전 평균의 차이를 비교해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** $(\mu_1^{\text{new}},\mu_2^{\text{new}},\mu_3^{\text{new}})\approx(-2.70,\,-0.40,\,3.70)$이에요.

대표로 성분 $1$은 $N_1=2.058$, $\sum_nr_{n1}x_n=-3-2.5+0.057\cdot(-1)+0.001\cdot0=-5.557$이라서 $\mu_1^{\text{new}}=\frac{-5.557}{2.058}\approx-2.70$이에요. 같은 방법으로 성분 $2$는 $N_2=0.943+0.999+0.066$, $\sum_nr_{n2}x_n=-0.943+0+0.132$, 성분 $3$은 $N_3=0.934+1.0+1.0$, $\sum_nr_{n3}x_n=1.868+4+5$예요.

| 성분 $k$ | $N_k$ | $\sum_nr_{nk}x_n$ | $\mu_k^{\text{new}}$ (반올림 전) |
|---|---|---|---|
| $1$ | $2.058$ | $-5.557$ | $-2.70$ ($-2.7002$) |
| $2$ | $2.008$ | $-0.811$ | $-0.40$ ($-0.4039$) |
| $3$ | $2.934$ | $10.868$ | $3.70$ ($3.7042$) |

교과서 Example 11.3의 $-4\to-2.7$, $0\to-0.4$, $8\to3.7$과 같은 값이에요.

#### (b)

**최종 답 요약:** 이동 거리는 $(1.30,\,0.40,\,4.30)$이고, 가장 많이 움직인 성분은 성분 $3$이에요.

$|-2.70-(-4)|=1.30$, $|-0.40-0|=0.40$, $|3.70-8|=4.30$이에요.

성분 $3$은 갱신 전 평균 $8$이 데이터 오른쪽 끝 $5$보다 바깥에 있었는데, 맡은 관측 $2,4,5$의 가중 평균으로 옮겨 가서 가장 많이 움직였어요.

#### 완성 답과 검산

#### (a) 검산

세 $N_k$의 합은 $2.058+2.008+2.934=7$이고, 표의 각 행 합도 $1$이에요. 또 각 평균은 그 성분이 맡은 관측 범위 안에 있어요. 성분 $1$은 $[-3,0]$, 성분 $2$는 $[-1,2]$, 성분 $3$은 $[2,5]$ 안이에요.

#### (b) 검산

반올림 전 값으로 재도 $1.2998$, $0.4039$, $4.2958$로 순서가 같아서 결론이 바뀌지 않아요.

#### 여기서 헷갈리기 쉬워요

$0.001$이나 $0.066$처럼 작은 칸도 표에 적힌 대로 $N_k$와 가중합에 넣어요. 분자에만 넣고 분모에서 빠뜨리면 가중치 합이 $1$이 아니게 돼요.

(b)의 이동 거리는 부호 없는 거리예요. 성분 $1$은 오른쪽으로, 성분 $2$와 $3$은 왼쪽으로 움직였지만 크기만 비교해요.

#### 다시 풀 때 확인할 것

1. 열마다 $N_k$와 $\sum_nr_{nk}x_n$을 같은 칸들로 계산해요.
2. 나눈 값을 둘째 자리까지 반올림하고 맡은 관측 범위 안에 있는지 봐요.
3. 갱신 전 평균과의 차이의 절댓값으로 가장 큰 이동을 골라요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mu_k^{\text{new}}=\frac{1}{N_k}\sum_nr_{nk}x_n$, 분자와 분모 모두 열 $k$의 책임도를 써요. 갱신 전 평균은 (b)의 비교 기준이에요.

#### 결론과 검산

$N_k=(2.058,2.008,2.934)$, 새 평균 $(-2.70,-0.40,3.70)$이에요. 이동 거리 $(1.30,0.40,4.30)$으로 성분 $3$이 가장 많이 움직였어요. 반올림 전 값으로도 순서가 같아요.

#### 용어

- **책임도(responsibility) $r_{nk}$** — 관측 $x_n$을 성분 $k$가 맡는 몫이에요. 이 표는 교과서 값을 반올림한 것이고 각 행의 합은 $1$이에요.
- **총 책임도 $N_k$** — $N_k=\sum_nr_{nk}$, 열 $k$의 합이에요.
- **평균 갱신(mean update)** — 책임도를 고정하고 $\mu_k^{\text{new}}=\frac{1}{N_k}\sum_nr_{nk}x_n$으로 평균을 다시 계산하는 M-step의 한 식이에요.

#### 출제 근거

MML Example 11.2의 책임도 표(교과서 353쪽, PDF 359쪽)와 Example 11.3(평균 갱신, 교과서 355쪽, PDF 361쪽)이에요.

관련 정리노트: [평균: 합이 1인 가중치로 낸 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-mean)

---

<a id="p4"></a>

### P4. 갱신된 평균으로 분산 갱신하기

MML Example 11.4 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=4)

#### 주어진 조건

관측값 $-3,-2.5,-1,0,2,4,5$에 성분 $3$개짜리 1차원 GMM을 맞추고 있어요. E-step에서 구한 책임도 $r_{nk}$가 반올림되어 아래 표에 있어요. 행은 관측 $x_n$, 열은 성분 $k=1,2,3$이에요.

총 책임도는 ${(N_1,N_2,N_3)=(2.058,2.008,2.934)}$이에요. 이미 갱신된 평균은 ${(\mu_1^{\text{new}},\mu_2^{\text{new}},\mu_3^{\text{new}})=(-2.7,-0.4,3.7)}$이고, 이 값을 그대로 써요. 갱신 전 분산은 ${(\sigma_1^2,\sigma_2^2,\sigma_3^2)=(1,0.2,3)}$이에요. 분산 갱신식은 다음과 같아요.

$$
(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}(x_n-\mu_k^{\text{new}})^2
$$

#### 구할 것

- (a) 세 성분의 새 분산 $(\sigma_k^{\text{new}})^2$을 소수점 아래 둘째 자리까지 구해 보세요.
- (b) (a)의 결과를 갱신 전 분산과 비교해, 분산이 줄어든 성분과 커진 성분을 골라 보세요.

| $x_n$ | $r_{n1}$ | $r_{n2}$ | $r_{n3}$ |
|---|---|---|---|
| $-3$ | $1.0$ | $0.0$ | $0.0$ |
| $-2.5$ | $1.0$ | $0.0$ | $0.0$ |
| $-1$ | $0.057$ | $0.943$ | $0.0$ |
| $0$ | $0.001$ | $0.999$ | $0.0$ |
| $2$ | $0.0$ | $0.066$ | $0.934$ |
| $4$ | $0.0$ | $0.0$ | $1.0$ |
| $5$ | $0.0$ | $0.0$ | $1.0$ |

<details><summary>원문 보기</summary>

“Here we see that the variances of the first and third component shrink significantly” — Example 11.4

</details>

#### 문제에서 주어진 것과 구할 것

주어진 것: 관측 $-3,-2.5,-1,0,2,4,5$, 반올림된 책임도 표 $r_{nk}$, $(N_1,N_2,N_3)=(2.058,2.008,2.934)$, 이미 갱신된 평균 $(\mu_1^{\text{new}},\mu_2^{\text{new}},\mu_3^{\text{new}})=(-2.7,-0.4,3.7)$, 갱신 전 분산 $(1,0.2,3)$이에요.

구할 것: (a) $(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_nr_{nk}(x_n-\mu_k^{\text{new}})^2$을 둘째 자리까지, (b) 갱신 전보다 줄어든 성분과 커진 성분이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘1차원 GMM의 분산 갱신’이라는 단서에서 공분산 갱신식의 1차원 형태인 **가중 분산(weighted variance)**을 떠올려요.

$$
(\sigma_k^{\text{new}})^2=\frac{1}{\underbrace{N_k}_{\text{열 }k\text{의 합}}}\sum_{n=1}^{7}\underbrace{r_{nk}}_{\text{가중치}}\,\underbrace{(x_n-\mu_k^{\text{new}})^2}_{\text{새 평균에서 잰 편차 제곱}}
$$

- 가중치는 평균을 낼 때와 같은 $r_{nk}/N_k$예요. 그래서 분산도 그 성분이 맡은 관측들의 퍼짐만 재요.
- 편차의 기준은 같은 M-step에서 방금 구한 $\mu_k^{\text{new}}$예요. 갱신 전 평균 $\mu_k$나 갱신 전 분산 $\sigma_k^2$는 식에 들어가지 않고, $\sigma_k^2$는 (b)의 비교 기준이에요.

[공분산: 같은 가중치로 낸 편차 외적의 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-cov)의 ‘1차원에서는 가중 분산이에요’에서 같은 식을 다뤘어요.

#### 종이에 적을 첫 줄

성분 $1$의 편차부터 적어요. $x_n+2.7$은 $-0.3,\ 0.2,\ 1.7,\ 2.7$이고, 제곱은 $0.09,\ 0.04,\ 2.89,\ 7.29$예요.

풀이 로드맵: 1. 성분별로 $0$이 아닌 칸의 편차 제곱 → 2. $r_{nk}$를 곱해 더하기 → 3. $N_k$로 나눠 반올림하고 갱신 전 분산과 비교해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** $\bigl((\sigma_1^{\text{new}})^2,(\sigma_2^{\text{new}})^2,(\sigma_3^{\text{new}})^2\bigr)\approx(0.15,\,0.44,\,1.53)$이에요.

대표로 성분 $1$은 $1.0\cdot0.09+1.0\cdot0.04+0.057\cdot2.89+0.001\cdot7.29=0.30202$이고, $(\sigma_1^{\text{new}})^2=\frac{0.30202}{2.058}\approx0.1468\approx0.15$예요.

성분 $2$($\mu_2^{\text{new}}=-0.4$)는 $0.943\cdot0.36+0.999\cdot0.16+0.066\cdot5.76$, 성분 $3$($\mu_3^{\text{new}}=3.7$)은 $0.934\cdot2.89+1.0\cdot0.09+1.0\cdot1.69$를 더해요. 결과를 표로 정리해요.

| 성분 $k$ | 가중합 | $\div N_k$ | $(\sigma_k^{\text{new}})^2$ |
|---|---|---|---|
| $1$ | $0.30202$ | $\div2.058=0.1468$ | $0.15$ |
| $2$ | $0.87948$ | $\div2.008=0.4380$ | $0.44$ |
| $3$ | $4.47926$ | $\div2.934=1.5267$ | $1.53$ |

성분 $2$의 가중합에서는 멀리 떨어진 관측 $2$가 책임도 $0.066$만 받는데도 편차 제곱 $5.76$이 커서 $0.380$이나 보태요.

교과서 Example 11.4는 성분 $1$을 $0.14$로 적었어요. 교과서는 반올림 전 책임도로 계산했어요. 이 문제에 주어진 책임도는 반올림된 표뿐이라 그 수로 계산하면 $0.15$예요.

#### (b)

**최종 답 요약:** 성분 $1$과 성분 $3$은 분산이 줄었고, 성분 $2$는 커졌어요.

$1\to0.15$, $3\to1.53$은 줄었고, $0.2\to0.44$는 커졌어요. 성분 $2$는 갱신 전 분산 $0.2$보다 맡은 관측들($-1$, $0$, 그리고 일부의 $2$)이 더 넓게 퍼져 있었어요.

#### 완성 답과 검산

#### (a) 검산

성분 $3$이 맡은 관측 $2,4,5$는 새 평균 $3.7$에서 최대 $1.7$ 떨어져 있어요. 가중 분산은 가장 큰 편차 제곱 $2.89$보다 작아야 하는데 $1.53$이라 범위가 맞아요. 성분 $1$, $2$도 같은 방법으로 $0.15\lt7.29$, $0.44\lt5.76$이에요.

교과서 값 $0.14$와의 차이는 대부분 $x=0$ 칸($r_{41}=0.001$)의 반올림에서 나와요.

#### (b) 검산

반올림 전 값 $0.1468$, $0.4380$, $1.5267$로 비교해도 $1$, $0.2$, $3$ 대비 증감 방향이 같아요.

#### 여기서 헷갈리기 쉬워요

편차를 갱신 전 평균 $(-4,0,8)$에서 재면 다른 값이 나와요. 분산 갱신식의 편차 기준은 같은 M-step에서 구한 $\mu_k^{\text{new}}$예요.

책임도 $r_{nk}$는 제곱하지 않아요. 제곱하는 것은 편차 $(x_n-\mu_k^{\text{new}})$뿐이고 $r_{nk}$는 한 번만 곱해요.

#### 다시 풀 때 확인할 것

1. 성분별로 $0$이 아닌 칸의 $x_n-\mu_k^{\text{new}}$를 먼저 적어요.
2. 편차 제곱에 $r_{nk}$를 곱해 더하고 $N_k$로 나눠요.
3. 결과를 갱신 전 분산과 비교해 증감을 판정해요.

**페이지 요약**

#### 떠올릴 개념·공식

1차원 가중 분산 $(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_nr_{nk}(x_n-\mu_k^{\text{new}})^2$이에요. 편차는 새 평균에서 재고, 가중치는 평균과 같은 $r_{nk}/N_k$예요.

#### 결론과 검산

가중합 $(0.30202,\,0.87948,\,4.47926)$을 $N_k$로 나누면 새 분산은 $(0.15,\,0.44,\,1.53)$이에요. 성분 $1$·$3$은 줄고 성분 $2$는 커졌어요.

#### 교과서와의 차이

교과서의 성분 $1$ 값 $0.14$는 반올림 전 책임도로 계산한 값이에요. 반올림한 표의 $r_{41}=0.001$로 계산하면 $0.15$예요.

#### 용어

- **가중 분산(weighted variance)** — $(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_nr_{nk}(x_n-\mu_k^{\text{new}})^2$이에요. $D$차원 공분산 갱신식에서 $D=1$인 경우예요.
- **새 평균 $\mu_k^{\text{new}}$** — 같은 M-step에서 먼저 구한 평균이에요. 분산 갱신의 편차 기준이에요.
- **총 책임도 $N_k$** — $N_k=\sum_nr_{nk}$, 책임도 표의 열 합이에요.

#### 출제 근거

MML Example 11.2의 책임도 표(교과서 353쪽, PDF 359쪽)와 Example 11.4(분산 갱신, 교과서 357–358쪽, PDF 363–364쪽)예요. 교과서는 $\sigma_1^2:1\to0.14$로 적었어요.

관련 정리노트: [공분산: 같은 가중치로 낸 편차 외적의 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-cov)

---

<a id="p5"></a>

### P5. 수렴한 GMM을 초기값과 비교하기

MML Example 11.6 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=5)

#### 주어진 조건

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

#### 구할 것

- (a) 수렴한 GMM의 세 혼합 가중치를 더하면 $1$이 되는지 확인하고, 각 성분의 표준편차 $\sigma_k$를 소수점 아래 둘째 자리까지 구해 보세요.
- (b) 수렴한 GMM을 초기값과 비교해, 평균이 가장 많이 이동한 성분과 분산이 커진 성분을 골라 보세요.

<details><summary>원문 보기</summary>

“When we run EM on our example from Figure 11.3, we obtain the final result” — Example 11.6

</details>

#### 문제에서 주어진 것과 구할 것

주어진 것: 수렴한 GMM $p(x)=\sum_k\pi_k\,\mathcal{N}(x\mid\mu_k,\sigma_k^2)$의 계수 $(0.29,0.28,0.43)$, 평균 $(-2.75,-0.50,3.64)$, 분산 $(0.06,0.25,1.63)$과 초기값 평균 $(-4,0,8)$, 분산 $(1,0.2,3)$, 가중치 $\frac{1}{3}$이에요.

구할 것: (a) 가중치 합이 $1$인지와 표준편차 $\sigma_k$, (b) 평균이 가장 많이 이동한 성분과 분산이 커진 성분이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘$\mathcal{N}(x\mid\mu_k,\sigma_k^2)$에서 세로선 뒤 두 값’이라는 단서에서 **가우시안 혼합 밀도의 표기**를 읽는 법을 떠올려요.

$$
p(x)=\sum_{k=1}^{3}\underbrace{\pi_k}_{\text{앞의 계수}}\,\mathcal{N}\bigl(x\mid\underbrace{\mu_k}_{\text{평균}},\underbrace{\sigma_k^2}_{\text{분산}}\bigr),\qquad\sigma_k=\sqrt{\sigma_k^2}
$$

- 각 성분 앞의 계수가 혼합 가중치 $\pi_k$예요. $p(x)$가 확률밀도이려면 $\sum_k\pi_k=1$이어야 해요.
- 세로선 뒤 둘째 값은 분산이라서 표준편차(standard deviation)는 그 제곱근이에요. 표준편차는 평균에서 데이터가 퍼진 폭을 $x$와 같은 단위로 나타내요.

이 GMM은 E-step과 M-step을 되풀이해 파라미터가 더 바뀌지 않을 때까지 간 결과예요. 반복 절차는 [E-step과 M-step의 순서](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-em-steps)에서 다뤘어요.

#### 종이에 적을 첫 줄

초기값과 수렴값을 나란히 적는 비교표의 뼈대부터 그려요. 행은 성분 $1,2,3$, 열은 $\mu_k$(초기→수렴), $|\Delta\mu_k|$, $\sigma_k^2$(초기→수렴), 증감이에요.

풀이 로드맵: 1. $0.29+0.28+0.43$ 확인 → 2. 분산의 제곱근으로 $\sigma_k$ → 3. 표의 열을 채워 이동 거리와 분산 증감을 판정해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** 가중치 합은 $1$이고, $(\sigma_1,\sigma_2,\sigma_3)\approx(0.24,\,0.50,\,1.28)$이에요.

세 계수의 합은 $0.29+0.28+0.43=1$이에요. 대표로 성분 $1$의 표준편차는 $\sigma_1=\sqrt{0.06}=0.2449\ldots\approx0.24$예요.

| 성분 $k$ | 분산 $\sigma_k^2$ | $\sqrt{\sigma_k^2}$ | $\sigma_k$ |
|---|---|---|---|
| $1$ | $0.06$ | $0.2449\ldots$ | $0.24$ |
| $2$ | $0.25$ | $0.5$ | $0.50$ |
| $3$ | $1.63$ | $1.2767\ldots$ | $1.28$ |

분산이 $1$보다 작으면 표준편차는 분산보다 크고($0.06\to0.24$), $1$보다 크면 표준편차가 더 작아요($1.63\to1.28$).

#### (b)

**최종 답 요약:** 평균이 가장 많이 이동한 성분은 성분 $3$(이동 거리 $4.36$), 분산이 커진 성분은 성분 $2$예요.

대표로 성분 $3$은 $|3.64-8|=4.36$이에요. 세 성분을 표로 비교해요.

| 성분 $k$ | $\mu_k$: 초기 $\to$ 수렴 | $\vert \Delta\mu_k\vert $ | $\sigma_k^2$: 초기 $\to$ 수렴 | 분산 증감 |
|---|---|---|---|---|
| $1$ | $-4\to-2.75$ | $1.25$ | $1\to0.06$ | 감소 |
| $2$ | $0\to-0.50$ | $0.50$ | $0.2\to0.25$ | 증가 |
| $3$ | $8\to3.64$ | $4.36$ | $3\to1.63$ | 감소 |

$4.36$이 가장 커서 성분 $3$이 가장 많이 이동했고, 분산이 커진 것은 $0.2\to0.25$인 성분 $2$뿐이에요.

#### 완성 답과 검산

#### (a) 검산

표준편차를 다시 제곱해 봐요. $0.24^2=0.0576\approx0.06$, $0.50^2=0.25$, $1.28^2=1.6384$로 반올림한 $\sigma_3$의 오차 범위 안에서 $1.63$과 맞아요.

#### (b) 검산

$|\Delta\mu_k|$는 $1.25\lt4.36$, $0.50\lt4.36$이라 성분 $3$이 최대예요. 분산 쌍은 $0.06\lt1$, $0.25\gt0.2$, $1.63\lt3$이라 커진 것은 성분 $2$뿐이에요.

한 번 갱신한 값(3·4번 문제)과 결론은 같지만, 수렴값이 첫 갱신 방향으로 계속 가지는 않아요(예: 성분 $2$ 분산 $0.2\to0.44\to0.25$).

#### 여기서 헷갈리기 쉬워요

$\mathcal{N}(x\mid-2.75,\,0.06)$의 $0.06$을 표준편차로 읽으면 안 돼요. 이 문제의 표기에서 둘째 값은 분산이라서 표준편차는 $\sqrt{0.06}\approx0.24$예요.

(b)의 분산 비교는 분산끼리 해요. 수렴한 표준편차 $0.50$을 초기 분산 $0.2$와 비교하는 식으로 단위를 섞지 않아요.

#### 다시 풀 때 확인할 것

1. $\mathcal{N}(x\mid\cdot,\cdot)$의 두 값이 평균과 분산인지 확인해요.
2. 계수 합 $1$과 분산의 제곱근을 계산해요.
3. 초기값과 수렴값을 같은 종류끼리 나란히 놓고 이동 거리와 증감을 판정해요.

**페이지 요약**

#### 떠올릴 개념·공식

$p(x)=\sum_k\pi_k\mathcal{N}(x\mid\mu_k,\sigma_k^2)$에서 앞 계수는 가중치, 세로선 뒤는 평균과 분산이에요. 표준편차는 $\sigma_k=\sqrt{\sigma_k^2}$예요.

#### 결론과 검산

가중치 합 $1$, 표준편차 $(0.24,0.50,1.28)$이에요. 평균 이동 $(1.25,0.50,4.36)$으로 성분 $3$이 가장 많이 이동했고, 분산이 커진 성분은 성분 $2$뿐이에요.

#### 용어

- **가우시안 혼합 모형(Gaussian mixture model, GMM)** — $p(x)=\sum_k\pi_k\mathcal{N}(x\mid\mu_k,\sigma_k^2)$처럼 가우시안 여러 개를 가중치 $\pi_k$로 섞은 밀도예요. $\sum_k\pi_k=1$이에요.
- **표준편차(standard deviation) $\sigma_k$** — 분산 $\sigma_k^2$의 제곱근이에요. $x$와 같은 단위의 퍼짐 폭이에요.
- **수렴(convergence)** — E-step과 M-step을 되풀이해도 파라미터나 로그우도가 거의 변하지 않는 상태예요.

#### 출제 근거

MML Example 11.6(GMM Fit), 교과서 361–362쪽(PDF 367–368쪽)의 최종 GMM 식 (11.57)과 Example 11.3–11.5의 초기값이에요.

관련 정리노트: [E-step과 M-step의 순서](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-em-steps)

---

<a id="p6"></a>

### P6. 최소제곱 손실의 기울기와 차원

MML Example 5.11 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=6)

#### 주어진 조건

선형모형 ${\mathbf{y}=\boldsymbol{\Phi}\boldsymbol{\theta}}$를 생각해요. 파라미터 $\boldsymbol{\theta}\in\mathbb{R}^{D}$와 관측 $\mathbf{y}\in\mathbb{R}^{N}$은 열벡터이고, 입력 특징 행렬은 $\boldsymbol{\Phi}\in\mathbb{R}^{N\times D}$예요. 두 함수를 다음처럼 정의해요.

$$
L(\mathbf{e})=\|\mathbf{e}\|^2
$$

$$
\mathbf{e}(\boldsymbol{\theta})=\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}
$$

미분은 수업 관례를 따라요. 스칼라를 열벡터로 미분한 결과는 행벡터예요. 벡터 $\mathbf{e}$를 벡터 $\boldsymbol{\theta}$로 미분한 결과는 $(i,j)$ 성분이 $\partial e_i/\partial\theta_j$인 행렬이에요.

#### 구할 것

- (a) 연쇄법칙 ${\frac{\partial L}{\partial\boldsymbol{\theta}}=\frac{\partial L}{\partial\mathbf{e}}\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}}$를 써서 $\frac{\partial L}{\partial\boldsymbol{\theta}}$를 $\mathbf{e}$와 $\boldsymbol{\Phi}$로 나타내 보세요.
- (b) (a)에서 구한 $\frac{\partial L}{\partial\mathbf{e}}$, $\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$, $\frac{\partial L}{\partial\boldsymbol{\theta}}$의 차원을 각각 읽어 보세요.

<details><summary>원문 보기</summary>

“We seek ∂L/∂θ, and we will use the chain rule for this purpose.” — Example 5.11

</details>

#### 문제에서 주어진 것과 구할 것

주어진 것: 열벡터 $\boldsymbol{\theta}\in\mathbb{R}^{D}$, $\mathbf{y}\in\mathbb{R}^{N}$, 행렬 $\boldsymbol{\Phi}\in\mathbb{R}^{N\times D}$, 스칼라 손실 $L(\mathbf{e})=\|\mathbf{e}\|^2$와 $\mathbf{e}(\boldsymbol{\theta})=\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}$예요. 미분은 수업의 행벡터 관례를 따르고, $\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$의 $(i,j)$ 성분은 $\partial e_i/\partial\theta_j$예요.

구할 것: (a) 연쇄법칙으로 $\frac{\partial L}{\partial\boldsymbol{\theta}}$를 $\mathbf{e}$, $\boldsymbol{\Phi}$로, (b) 세 미분 $\frac{\partial L}{\partial\mathbf{e}}$, $\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$, $\frac{\partial L}{\partial\boldsymbol{\theta}}$의 차원이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘$L$이 $\mathbf{e}$의 함수이고 $\mathbf{e}$가 $\boldsymbol{\theta}$의 함수’라는 구조에서 **다변수 연쇄법칙(chain rule)**을 떠올려요. 두 미분을 각각 구해 문제에 적힌 순서대로 곱해요.

$$
\underbrace{\frac{\partial L}{\partial\boldsymbol{\theta}}}_{1\times D}=\underbrace{\frac{\partial L}{\partial\mathbf{e}}}_{1\times N}\;\underbrace{\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}}_{N\times D}
$$

- **스칼라를 열벡터로 미분**하면 편미분을 가로로 놓은 **행벡터**예요. 변수 $\boldsymbol{\theta}$, $\mathbf{e}$ 자체는 열벡터 그대로예요.
- **벡터를 벡터로 미분**한 야코비안(Jacobian)은 **출력×입력** 모양이에요. 행은 출력 $e_1,\dots,e_N$, 열은 입력 $\theta_1,\dots,\theta_D$라서 $N\times D$예요.
- 안쪽 차원 $N$이 맞아야 곱이 정의돼요. 그래서 곱 순서를 바꾸지 않아요.

행벡터 관례와 그 이유는 [기울기를 0으로: 무엇을 무엇으로 미분하나](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s2-zero-gradient)에서, 같은 구조($\mathbf{a}=\mathbf{x}_n-\boldsymbol{\mu}_k$의 미분이 $-\mathbf{I}$)의 연쇄법칙은 [이차식 미분](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s2-log-gauss-quad)에서 다뤘어요.

#### 종이에 적을 첫 줄

스칼라 $L$을 성분으로 펼친 $L=\mathbf{e}^\top\mathbf{e}=\sum_{n=1}^{N}e_n^2$을 먼저 적어요.

풀이 로드맵: 1. $\frac{\partial L}{\partial\mathbf{e}}$를 성분 편미분으로 → 2. $e_n$을 펼쳐 $\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$ → 3. 순서대로 곱하고 차원을 읽어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** $\frac{\partial L}{\partial\boldsymbol{\theta}}=-2\mathbf{e}^\top\boldsymbol{\Phi}=-2(\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta})^\top\boldsymbol{\Phi}$, $1\times D$ 행벡터예요.

$$
L=\mathbf{e}^\top\mathbf{e}=\sum_{n=1}^{N}e_n^2
$$

↳ 제곱 노름을 성분 합으로 펼쳐요

$$
\frac{\partial L}{\partial e_n}=2e_n
$$

↳ $e_n$이 든 항 $e_n^2$만 남아요

$$
\frac{\partial L}{\partial\mathbf{e}}=\begin{bmatrix}2e_1&\cdots&2e_N\end{bmatrix}=2\mathbf{e}^\top
$$

↳ 편미분을 가로로 모아 행벡터로 써요

$$
e_n=y_n-\sum_{d=1}^{D}\Phi_{nd}\theta_d
$$

↳ $\boldsymbol{\Phi}\boldsymbol{\theta}$의 $n$번째 성분을 펼쳐요

$$
\frac{\partial e_n}{\partial\theta_d}=-\Phi_{nd}
$$

↳ $y_n$은 상수, $\theta_d$ 앞 계수만 남아요

$$
\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}=-\boldsymbol{\Phi}
$$

↳ $(n,d)$ 자리에 $-\Phi_{nd}$를 둔 출력×입력 행렬

$$
\frac{\partial L}{\partial\boldsymbol{\theta}}=2\mathbf{e}^\top(-\boldsymbol{\Phi})=-2\mathbf{e}^\top\boldsymbol{\Phi}
$$

↳ 연쇄법칙 순서대로 곱해요

$$
\frac{\partial L}{\partial\boldsymbol{\theta}}=-2(\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta})^\top\boldsymbol{\Phi}
$$

↳ $\mathbf{e}=\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}$를 대입해요

#### (b)

**최종 답 요약:** $\frac{\partial L}{\partial\mathbf{e}}\in\mathbb{R}^{1\times N}$, $\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}\in\mathbb{R}^{N\times D}$, $\frac{\partial L}{\partial\boldsymbol{\theta}}\in\mathbb{R}^{1\times D}$예요.

$\mathbf{e}$는 $N\times1$ 열벡터라 $2\mathbf{e}^\top$은 $1\times N$이에요. $-\boldsymbol{\Phi}$는 행이 $e_1,\dots,e_N$, 열이 $\theta_1,\dots,\theta_D$에 대응해 $N\times D$예요.

$$
\underbrace{2\mathbf{e}^\top}_{1\times N}\;\underbrace{(-\boldsymbol{\Phi})}_{N\times D}\in\mathbb{R}^{1\times D}
$$

$\boldsymbol{\theta}$는 $D\times1$ 열벡터이지만, 스칼라 $L$을 $\boldsymbol{\theta}$로 미분한 결과는 $\theta_1,\dots,\theta_D$에 대한 편미분 $D$개를 가로로 놓은 $1\times D$ 행벡터예요.

#### 완성 답과 검산

#### (a) 검산

$N=D=1$로 줄여 봐요. $L=(y-\phi\theta)^2$을 1변수로 미분하면 $-2(y-\phi\theta)\phi$이고, $-2\mathbf{e}^\top\boldsymbol{\Phi}$에 $\mathbf{e}=y-\phi\theta$, $\boldsymbol{\Phi}=\phi$를 넣은 값과 같아요.

성분으로도 맞아요. $d$번째 칸은 $\sum_n\frac{\partial L}{\partial e_n}\frac{\partial e_n}{\partial\theta_d}=\sum_n2e_n(-\Phi_{nd})$이고, 이것이 $-2\mathbf{e}^\top\boldsymbol{\Phi}$의 $d$번째 성분이에요.

#### (b) 검산

곱 $(1\times N)(N\times D)$의 안쪽 $N$이 맞고 결과는 $1\times D$예요. 미분 대상 $\boldsymbol{\theta}$의 성분 수 $D$와 결과의 칸 수 $D$도 같아요.

#### 여기서 헷갈리기 쉬워요

$\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$를 $-\boldsymbol{\Phi}^\top$($D\times N$)로 쓰면 $N\neq D$일 때 $2\mathbf{e}^\top$($1\times N$)과 곱이 정의되지 않고, $N=D$여도 $(n,d)$ 성분이 $-\Phi_{dn}$이 되어 정의와 달라요. 문제의 정의대로 행은 출력 $e_i$, 열은 입력 $\theta_j$예요.

$-2\boldsymbol{\Phi}^\top\mathbf{e}$는 답을 전치한 $D\times1$ 모양이에요. 이 문제는 행벡터 관례라 답은 $-2\mathbf{e}^\top\boldsymbol{\Phi}$예요.

#### 다시 풀 때 확인할 것

1. $L=\sum_ne_n^2$, $e_n=y_n-\sum_d\Phi_{nd}\theta_d$로 성분을 펼쳐요.
2. 스칼라 미분은 가로로, 벡터 미분은 출력×입력으로 모아요.
3. $(1\times N)(N\times D)$ 곱의 차원으로 순서를 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

연쇄법칙 $\frac{\partial L}{\partial\boldsymbol{\theta}}=\frac{\partial L}{\partial\mathbf{e}}\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$예요. 스칼라를 열벡터로 미분하면 행벡터, 벡터를 벡터로 미분하면 출력×입력 행렬이에요.

#### 결론

$\frac{\partial L}{\partial\mathbf{e}}=2\mathbf{e}^\top$($1\times N$), $\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}=-\boldsymbol{\Phi}$($N\times D$)라서 $\frac{\partial L}{\partial\boldsymbol{\theta}}=-2\mathbf{e}^\top\boldsymbol{\Phi}=-2(\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta})^\top\boldsymbol{\Phi}$($1\times D$)예요.

#### 검산

$N=D=1$이면 $-2(y-\phi\theta)\phi$로 1변수 미분과 같아요. 안쪽 차원 $N$이 맞아야 곱이 정의돼요.

#### 용어

- **최소제곱 손실(least-squares loss)** — $L=\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|^2$, 잔차 $\mathbf{e}$의 제곱 노름이에요. 값은 스칼라예요.
- **행벡터 미분** — 스칼라를 $D\times1$ 열벡터로 미분한 결과예요. 편미분 $D$개를 가로로 놓은 $1\times D$ 행벡터예요.
- **야코비안(Jacobian)** — 벡터 $\mathbf{e}\in\mathbb{R}^N$을 $\boldsymbol{\theta}\in\mathbb{R}^D$로 미분한 $N\times D$ 행렬이에요. $(i,j)$ 성분은 $\partial e_i/\partial\theta_j$예요.
- **연쇄법칙(chain rule)** — 합성함수의 미분을 각 단계 미분의 곱으로 구하는 규칙이에요. 행렬곱이라 순서를 지켜요.

#### 출제 근거

MML Example 5.11(Gradient of a Least-Squares Loss in a Linear Model), 교과서 154쪽(PDF 160쪽), 식 (5.75)–(5.83)이에요. 교과서도 $\frac{\partial L}{\partial\boldsymbol{\theta}}\in\mathbb{R}^{1\times D}$인 행벡터로 적었어요.

관련 정리노트: [이차식 미분](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s2-log-gauss-quad)

---

<a id="p7"></a>

### P7. 분수로 분산 갱신하기

MML Example 11.4 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=7)

#### 주어진 조건

1차원 관측 $x_1,\dots,x_7$에 성분 $3$개짜리 GMM을 맞추고 있어요. E-step에서 구한 책임도 $r_{nk}$가 아래 표에 있어요. 행은 관측 $x_n$, 열은 성분 $k=1,2,3$이에요.

총 책임도는 ${(N_1,N_2,N_3)=\left(\frac{5}{2},2,\frac{5}{2}\right)}$예요. 이미 갱신된 평균은 ${(\mu_1^{\text{new}},\mu_2^{\text{new}},\mu_3^{\text{new}})=\left(-\frac{13}{5},\frac{1}{4},\frac{22}{5}\right)}$이에요. 갱신 전 분산은 ${(\sigma_1^2,\sigma_2^2,\sigma_3^2)=\left(2,\frac{1}{2},3\right)}$이에요. 분산 갱신식은 다음과 같아요.

$$
(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}(x_n-\mu_k^{\text{new}})^2
$$

#### 구할 것

- (a) 세 성분의 새 분산 $(\sigma_k^{\text{new}})^2$을 기약분수로 구해 보세요.
- (b) (a)의 결과를 갱신 전 분산과 비교해, 분산이 줄어든 성분과 커진 성분을 골라 보세요.

| $x_n$ | $r_{n1}$ | $r_{n2}$ | $r_{n3}$ |
|---|---|---|---|
| $-4$ | $1$ | $0$ | $0$ |
| $-2$ | $1$ | $0$ | $0$ |
| $-1$ | $\frac{1}{2}$ | $\frac{1}{2}$ | $0$ |
| $0$ | $0$ | $1$ | $0$ |
| $2$ | $0$ | $\frac{1}{2}$ | $\frac{1}{2}$ |
| $4$ | $0$ | $0$ | $1$ |
| $6$ | $0$ | $0$ | $1$ |

<details><summary>원문 보기</summary>

“In our example from Figure 11.3, the variances are updated as follows” — Example 11.4

</details>

#### 문제에서 주어진 것과 구할 것

주어진 것: 관측 $-4,-2,-1,0,2,4,6$과 분수 책임도 표 $r_{nk}$, $(N_1,N_2,N_3)=\left(\frac{5}{2},2,\frac{5}{2}\right)$, 새 평균 $\left(-\frac{13}{5},\frac{1}{4},\frac{22}{5}\right)$, 갱신 전 분산 $\left(2,\frac{1}{2},3\right)$이에요.

구할 것: (a) $(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_nr_{nk}(x_n-\mu_k^{\text{new}})^2$을 기약분수로, (b) 갱신 전보다 줄어든 성분과 커진 성분이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘분산 갱신식’과 ‘이미 갱신된 평균’이라는 단서에서 1차원 **가중 분산(weighted variance)**을 떠올려요. 평균을 낼 때와 같은 가중치로 새 평균 주위의 퍼짐을 재요.

$$
(\sigma_k^{\text{new}})^2=\frac{1}{\underbrace{N_k}_{\text{열 }k\text{의 합}}}\sum_{n=1}^{7}\underbrace{r_{nk}}_{\text{가중치}}\,\underbrace{(x_n-\mu_k^{\text{new}})^2}_{\text{새 평균 기준 편차 제곱}}
$$

- $r_{nk}=0$인 관측은 항이 $0$이라 빼고 계산해요. 성분마다 관측 세 개만 남아요.
- 편차를 분수로 먼저 구하면 분모가 같아져서 제곱해 더하기 쉬워요. 갱신 전 분산은 식에 들어가지 않고 (b)의 비교 기준이에요.

[공분산: 같은 가중치로 낸 편차 외적의 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-cov)의 1차원 가중 분산과 같은 식이에요.

#### 종이에 적을 첫 줄

성분 $1$의 편차부터 적어요. $\mu_1^{\text{new}}=-\frac{13}{5}$에서 $x_n=-4,-2,-1$의 편차는 $-\frac{7}{5},\ \frac{3}{5},\ \frac{8}{5}$이에요.

풀이 로드맵: 1. 성분별 편차를 분수로 → 2. $r_{nk}\times$편차 제곱을 더해 가중합 → 3. $N_k$로 나눠 약분하고 갱신 전 분산과 비교해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** $\bigl((\sigma_1^{\text{new}})^2,(\sigma_2^{\text{new}})^2,(\sigma_3^{\text{new}})^2\bigr)=\left(\frac{36}{25},\,\frac{19}{16},\,\frac{56}{25}\right)$이에요.

대표로 성분 $1$은 $1\cdot\frac{49}{25}+1\cdot\frac{9}{25}+\frac{1}{2}\cdot\frac{64}{25}=\frac{90}{25}=\frac{18}{5}$이고, $\frac{18/5}{5/2}=\frac{36}{25}$이에요.

| 성분 $k$ | 편차 $x_n-\mu_k^{\text{new}}$ | $r_{nk}\times$편차 제곱 | 가중합 | $\div N_k$ |
|---|---|---|---|---|
| $1$ | $-\frac{7}{5},\ \frac{3}{5},\ \frac{8}{5}$ | $\frac{49}{25}+\frac{9}{25}+\frac{1}{2}\cdot\frac{64}{25}$ | $\frac{18}{5}$ | $\frac{18}{5}\cdot\frac{2}{5}=\frac{36}{25}$ |
| $2$ | $-\frac{5}{4},\ -\frac{1}{4},\ \frac{7}{4}$ | $\frac{1}{2}\cdot\frac{25}{16}+\frac{1}{16}+\frac{1}{2}\cdot\frac{49}{16}$ | $\frac{19}{8}$ | $\frac{19}{8}\cdot\frac{1}{2}=\frac{19}{16}$ |
| $3$ | $-\frac{12}{5},\ -\frac{2}{5},\ \frac{8}{5}$ | $\frac{1}{2}\cdot\frac{144}{25}+\frac{4}{25}+\frac{64}{25}$ | $\frac{28}{5}$ | $\frac{28}{5}\cdot\frac{2}{5}=\frac{56}{25}$ |

성분 $2$의 가중합은 $\frac{25}{32}+\frac{2}{32}+\frac{49}{32}=\frac{76}{32}=\frac{19}{8}$이에요. 세 결과 모두 분자와 분모의 공약수가 $1$이라 기약분수예요.

#### (b)

**최종 답 요약:** 성분 $1$과 성분 $3$은 분산이 줄었고, 성분 $2$는 커졌어요.

소수로 바꾸면 $\frac{36}{25}=1.44\lt2$, $\frac{19}{16}=1.1875\gt\frac{1}{2}$, $\frac{56}{25}=2.24\lt3$이에요.

#### 완성 답과 검산

#### (a) 검산

$\mu_k^{\text{new}}$가 같은 가중치 $r_{nk}/N_k$로 낸 평균이라서, 같은 가중치로 ‘제곱의 평균 − 평균의 제곱’을 계산해도 같아야 해요. 성분 $2$는 $\frac{1}{2}\left(\frac{1}{2}\cdot1+1\cdot0+\frac{1}{2}\cdot4\right)=\frac{5}{4}$이고, $\frac{5}{4}-\left(\frac{1}{4}\right)^2=\frac{20}{16}-\frac{1}{16}=\frac{19}{16}$이에요.

#### (b) 검산

분수끼리 비교해도 $\frac{36}{25}\lt\frac{50}{25}$, $\frac{19}{16}\gt\frac{8}{16}$, $\frac{56}{25}\lt\frac{75}{25}$로 같은 결론이에요.

#### 여기서 헷갈리기 쉬워요

반씩 맡은 관측($-1$, $2$)은 편차 제곱에 $\frac{1}{2}$을 곱해요. 이 가중치를 빼먹고 세 항을 그대로 더하면 성분 $1$의 가중합이 $\frac{122}{25}$가 되어 답이 달라져요.

나누는 수는 맡은 관측 개수 $3$이 아니라 $N_k$예요. 성분 $1$·$3$은 $\frac{5}{2}$, 성분 $2$는 $2$로 나눠요.

#### 다시 풀 때 확인할 것

1. $r_{nk}\neq0$인 관측만 골라 새 평균 기준 편차를 분수로 적어요.
2. 편차 제곱에 $r_{nk}$를 곱해 더하고 $N_k$로 나눠 약분해요.
3. 새 평균이 같은 가중치의 평균이니 ‘제곱의 평균 − 평균의 제곱’으로 한 성분을 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

1차원 가중 분산 $(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_nr_{nk}(x_n-\mu_k^{\text{new}})^2$이에요. 편차는 새 평균에서 재고, 반씩 맡은 관측은 $\frac{1}{2}$로 가중해요.

#### 결론과 검산

가중합 $\left(\frac{18}{5},\frac{19}{8},\frac{28}{5}\right)$을 $N_k$로 나누면 $\left(\frac{36}{25},\frac{19}{16},\frac{56}{25}\right)$이에요. 성분 $1$·$3$은 줄고 성분 $2$는 커졌어요. 새 평균이 같은 가중치의 평균이라 ‘제곱의 평균 − 평균의 제곱’으로도 같은 값이 나와요.

#### 용어

- **가중 분산(weighted variance)** — $\frac{1}{N_k}\sum_nr_{nk}(x_n-\mu_k^{\text{new}})^2$, 책임도로 가중한 편차 제곱의 평균이에요. $D=1$일 때의 공분산 갱신식이에요.
- **새 평균 $\mu_k^{\text{new}}$** — 같은 M-step에서 먼저 구한 가중 평균이에요. 분산 갱신의 편차 기준이에요.
- **기약분수** — 분자와 분모의 최대공약수가 $1$인 분수예요.

#### 출제 근거

MML Example 11.4(분산 갱신), 교과서 357–358쪽(PDF 363–364쪽)의 계산 구조를 분수로 끝나는 책임도 표로 바꾼 문항이에요. 표와 새 평균은 복습문제 2번과 같아요.

관련 정리노트: [공분산: 같은 가중치로 낸 편차 외적의 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-cov)

---

<a id="p8"></a>

### P8. 벡터와 행렬로 스칼라 함수 미분하기

MML Exercise 5.6 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=8)

#### 주어진 조건

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

#### 구할 것

- (a) $f$를 $\mathbf{t}$로 미분한 $\frac{df}{d\mathbf{t}}$를 구해 보세요.
- (b) $g$를 $\mathbf{X}$로 미분한 $\frac{dg}{d\mathbf{X}}$를 $\mathbf{A}$와 $\mathbf{B}$로 나타내 보세요.
- (c) (a)와 (b)에서 구한 두 미분의 차원을 각각 읽어 보세요.

<details><summary>원문 보기</summary>

“Differentiate f with respect to t and g with respect to X” — Exercise 5.6

</details>

#### 문제에서 주어진 것과 구할 것

주어진 것: 스칼라 함수 $f(\mathbf{t})=\sin\bigl(\log(\mathbf{t}^\top\mathbf{t})\bigr)$($\mathbf{t}\in\mathbb{R}^{D}$, 영벡터 아닌 열벡터)와 $g(\mathbf{X})=\operatorname{tr}(\mathbf{A}\mathbf{X}\mathbf{B})$($\mathbf{A}\in\mathbb{R}^{D\times E}$, $\mathbf{X}\in\mathbb{R}^{E\times F}$, $\mathbf{B}\in\mathbb{R}^{F\times D}$)예요. 열벡터로 미분하면 행벡터, 행렬 $\mathbf{X}$로 미분하면 $\partial g/\partial X_{pq}$를 같은 $(p,q)$ 자리에 둔 행렬이에요.

구할 것: (a) $\frac{df}{d\mathbf{t}}$, (b) $\frac{dg}{d\mathbf{X}}$를 $\mathbf{A}$, $\mathbf{B}$로, (c) 두 미분의 차원이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

(a) ‘$\sin$ 안에 $\log$, 그 안에 $\mathbf{t}^\top\mathbf{t}$’라는 겹친 구조에서 **연쇄법칙(chain rule)**을 떠올려요. 안쪽 스칼라에 $u=\mathbf{t}^\top\mathbf{t}$라는 이름을 붙이면 1변수 미분과 벡터 미분이 나뉘어요.

$$
\frac{df}{d\mathbf{t}}=\underbrace{\frac{df}{du}}_{\text{스칼라}}\;\underbrace{\frac{du}{d\mathbf{t}}}_{1\times D\text{ 행벡터}},\qquad\frac{d(\mathbf{t}^\top\mathbf{t})}{d\mathbf{t}}=2\mathbf{t}^\top
$$

- $\mathbf{t}^\top\mathbf{t}=\sum_dt_d^2$를 $t_d$로 편미분하면 $2t_d$이고, 이것을 가로로 모으면 $2\mathbf{t}^\top$이에요.
- $\mathbf{t}\neq\mathbf{0}$이라 $u\gt0$이고, 그래서 $\log u$와 $\frac{1}{u}$이 정의돼요.

(b) ‘스칼라를 행렬로 미분’이라는 단서에서 **칸마다 편미분해 같은 자리에 두는 정의**를 떠올려요. 대각합(trace)을 성분 합으로 펼친 뒤 $X_{pq}$ 하나로 편미분해요.

$$
\left[\frac{dg}{d\mathbf{X}}\right]_{pq}=\frac{\partial g}{\partial X_{pq}},\qquad\operatorname{tr}(\mathbf{M})=\sum_iM_{ii},\qquad(\mathbf{A}\mathbf{X})_{il}=\sum_jA_{ij}X_{jl}
$$

행렬 미분의 정의는 [칸마다 미분하는 정의](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s3-matrix-deriv-def), 열벡터로 미분하면 행벡터가 되는 관례는 [기울기를 0으로: 무엇을 무엇으로 미분하나](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s2-zero-gradient)에서 다뤘어요.

#### 종이에 적을 첫 줄

(a)는 $u=\mathbf{t}^\top\mathbf{t}=\sum_{d=1}^{D}t_d^2$, (b)는 $g=\sum_{i=1}^{D}(\mathbf{A}\mathbf{X}\mathbf{B})_{ii}$를 먼저 적어요.

풀이 로드맵: 1. (a) $\frac{du}{d\mathbf{t}}$와 $\frac{df}{du}$를 곱하기 → 2. (b) 삼중합으로 펼쳐 $X_{pq}$로 편미분하고 행렬곱 꼴로 묶기 → 3. (c) 결과의 행·열 수 읽기예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** $\frac{df}{d\mathbf{t}}=\frac{2\cos\bigl(\log(\mathbf{t}^\top\mathbf{t})\bigr)}{\mathbf{t}^\top\mathbf{t}}\,\mathbf{t}^\top$, 스칼라 × $1\times D$ 행벡터예요.

$$
u=\mathbf{t}^\top\mathbf{t}=\sum_{d=1}^{D}t_d^2
$$

↳ 안쪽 스칼라에 이름을 붙여요

$$
\frac{du}{d\mathbf{t}}=\begin{bmatrix}2t_1&\cdots&2t_D\end{bmatrix}=2\mathbf{t}^\top
$$

↳ $\partial u/\partial t_d=2t_d$를 가로로 모아요

$$
\frac{df}{du}=\cos(\log u)\cdot\frac{1}{u}
$$

↳ $\sin$의 미분 × $\log$의 미분이에요

$$
\frac{df}{d\mathbf{t}}=\frac{df}{du}\frac{du}{d\mathbf{t}}=\frac{2\cos\bigl(\log(\mathbf{t}^\top\mathbf{t})\bigr)}{\mathbf{t}^\top\mathbf{t}}\,\mathbf{t}^\top
$$

↳ 연쇄법칙으로 곱하고 $u$를 되돌려요

#### (b)

**최종 답 구조:** $\frac{dg}{d\mathbf{X}}=\mathbf{A}^\top\mathbf{B}^\top$이에요. 첨자 $i=1,\dots,D$, $j=1,\dots,E$, $l=1,\dots,F$로 펼쳐요.

$$
(\mathbf{A}\mathbf{X}\mathbf{B})_{ii}=\sum_{l=1}^{F}(\mathbf{A}\mathbf{X})_{il}B_{li}
$$

↳ $(\mathbf{A}\mathbf{X})\mathbf{B}$의 행×열 곱이에요

$$
(\mathbf{A}\mathbf{X}\mathbf{B})_{ii}=\sum_{j=1}^{E}\sum_{l=1}^{F}A_{ij}X_{jl}B_{li}
$$

↳ $(\mathbf{A}\mathbf{X})_{il}$도 행×열로 펼쳐요

$$
g=\sum_{i=1}^{D}\sum_{j=1}^{E}\sum_{l=1}^{F}A_{ij}X_{jl}B_{li}
$$

↳ 대각합은 대각 성분을 $i$로 더한 값

$$
\frac{\partial g}{\partial X_{pq}}=\sum_{i=1}^{D}A_{ip}B_{qi}
$$

↳ $j=p$, $l=q$인 항만 $X_{pq}$를 포함해요

$$
\frac{\partial g}{\partial X_{pq}}=\sum_{i=1}^{D}(\mathbf{A}^\top)_{pi}(\mathbf{B}^\top)_{iq}=(\mathbf{A}^\top\mathbf{B}^\top)_{pq}
$$

↳ 전치로 첨자를 행×열 순서로 맞춰요

$$
\frac{dg}{d\mathbf{X}}=\mathbf{A}^\top\mathbf{B}^\top
$$

↳ $(p,q)$ 자리에 같은 값을 두면 전체 행렬

#### (c)

**최종 답 요약:** $\frac{df}{d\mathbf{t}}\in\mathbb{R}^{1\times D}$, $\frac{dg}{d\mathbf{X}}\in\mathbb{R}^{E\times F}$예요.

(a)는 스칼라 $\frac{2\cos(\log(\mathbf{t}^\top\mathbf{t}))}{\mathbf{t}^\top\mathbf{t}}$에 $1\times D$ 행벡터 $\mathbf{t}^\top$을 곱했으니 $1\times D$예요. (b)는 $\mathbf{A}^\top$($E\times D$)과 $\mathbf{B}^\top$($D\times F$)의 곱이라 $E\times F$이고, $\mathbf{X}$와 모양이 같아요.

#### 완성 답과 검산

#### (a) 검산

$D=1$, $t\gt0$이면 $f=\sin(\log t^2)=\sin(2\log t)$이고 1변수 미분은 $\frac{2\cos(2\log t)}{t}$예요. 답에 넣으면 $\frac{2\cos(\log t^2)}{t^2}\cdot t=\frac{2\cos(2\log t)}{t}$로 같아요.

#### (b) 검산

$D=E=F=1$이면 $g=aXb$이고 $\frac{dg}{dX}=ab$예요. 답 $\mathbf{A}^\top\mathbf{B}^\top$도 $ab$예요. 또 $\mathbf{A}^\top\mathbf{B}^\top=(\mathbf{B}\mathbf{A})^\top$이고 $\mathbf{B}\mathbf{A}$는 $F\times E$라서 전치하면 $E\times F$로 정의와 맞아요.

#### (c) 검산

열벡터로 미분한 결과의 칸 수는 $\mathbf{t}$의 성분 수 $D$, 행렬로 미분한 결과의 칸 수는 $\mathbf{X}$의 원소 수 $EF$여야 해요. $1\times D$와 $E\times F$가 둘 다 맞아요.

#### 여기서 헷갈리기 쉬워요

(a)에서 $\frac{du}{d\mathbf{t}}$를 열벡터 $2\mathbf{t}$로 쓰면 수업 관례와 달라요. 스칼라를 열벡터로 미분했으니 $2\mathbf{t}^\top$이고, 최종 답도 $\mathbf{t}^\top$으로 끝나요.

(b)에서 $\mathbf{B}\mathbf{A}$($F\times E$)를 답으로 쓰면 $E\neq F$일 때는 $\mathbf{X}$($E\times F$)와 모양이 달라 바로 걸러지고, $E=F$여도 $(p,q)$ 성분이 $\sum_iA_{ip}B_{qi}$와 달라요. 답은 첨자 계산에서 나오고 모양은 점검용이에요.

#### 다시 풀 때 확인할 것

- (a) $u=\mathbf{t}^\top\mathbf{t}$로 두고 $\frac{df}{du}\cdot2\mathbf{t}^\top$을 적어요.
- (b) $g=\sum_{i,j,l}A_{ij}X_{jl}B_{li}$로 펼친 뒤 $j=p$, $l=q$ 항만 남겨요.
- (c) 결과의 모양을 미분 대상($\mathbf{t}$의 성분 수, $\mathbf{X}$의 모양)과 맞춰 봐요.

**페이지 요약**

#### 떠올릴 개념·공식

(a) $u=\mathbf{t}^\top\mathbf{t}$로 두는 연쇄법칙, $\frac{du}{d\mathbf{t}}=2\mathbf{t}^\top$(행벡터). (b) 칸마다 미분해 같은 자리에 두는 정의와 $\operatorname{tr}$의 삼중합 전개예요.

#### 결론

$\frac{df}{d\mathbf{t}}=\frac{2\cos(\log(\mathbf{t}^\top\mathbf{t}))}{\mathbf{t}^\top\mathbf{t}}\mathbf{t}^\top\in\mathbb{R}^{1\times D}$, $\frac{dg}{d\mathbf{X}}=\mathbf{A}^\top\mathbf{B}^\top\in\mathbb{R}^{E\times F}$예요.

#### 검산

모두 1차원으로 줄이면 1변수 미분과 같아요. 행렬 미분 결과는 $\mathbf{X}$와 같은 $E\times F$예요.

#### 용어

- **대각합(trace) $\operatorname{tr}$** — 정사각행렬의 대각 성분 합 $\operatorname{tr}(\mathbf{M})=\sum_iM_{ii}$예요. 여기서 $\mathbf{A}\mathbf{X}\mathbf{B}$는 $D\times D$라 정의돼요.
- **행벡터 미분** — 스칼라를 $D\times1$ 열벡터 $\mathbf{t}$로 미분한 결과예요. 편미분을 가로로 놓은 $1\times D$ 행벡터예요.
- **스칼라의 행렬 미분** — $\partial g/\partial X_{pq}$를 $(p,q)$ 자리에 둔 행렬이에요. 결과는 $\mathbf{X}$와 같은 $E\times F$ 모양이에요.
- **연쇄법칙(chain rule)** — 합성함수의 미분을 바깥 함수의 미분과 안쪽 함수의 미분의 곱으로 구하는 규칙이에요.

#### 출제 근거

MML Exercise 5.6, 교과서 171쪽(PDF 177쪽)이에요. 미분 방향은 수업 관례(열벡터 변수에 대한 스칼라 미분은 행벡터, 행렬 미분은 원소별 같은 자리)를 문제 조건에 명시했어요.

관련 정리노트: [칸마다 미분하는 정의](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s3-matrix-deriv-def)

---

원 문제·정리노트·PDF는 보존해요.
