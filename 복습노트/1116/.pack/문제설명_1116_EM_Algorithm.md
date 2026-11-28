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

MML Example 11.5 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=1)

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

#### 풀이 목표

(a) 총 책임도 $N_k$와 관측 수 $N=7$로 새 혼합 가중치 $\pi_k^{\text{new}}$를 셋째 자리까지 구해요. (b) 세 값의 합이 $1$인지 확인하고 갱신 전 $\frac{1}{3}$보다 커진 성분을 골라요.

#### 풀이 단서

주어진 M-step 식 $\pi_k^{\text{new}}=\frac{N_k}{N}$에 대입해요. 책임도 표의 각 행 합이 $1$이므로 열 합을 모두 더하면 $\sum_{k=1}^3 N_k=N$이고, 새 가중치 합은 항상 $1$이에요([비율: 전체 몫 중 성분 k의 몫](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-pi)).

#### 첫 단계

$N=7$을 분모에 두고 첫 성분부터 $\pi_1^{\text{new}}=\frac{2.058}{7}$을 계산해요.

#### 핵심 풀이

#### (a) 새 혼합 가중치 계산

성분 $1$은 $\pi_1^{\text{new}}=\frac{2.058}{7}=0.294$예요. 같은 방법으로 세 성분을 표로 정리해요.

| 성분 $k$ | $N_k$ | $N_k/7$ | 셋째 자리 반올림 |
|---|---|---|---|
| $1$ | $2.058$ | $0.294$ | $0.294$ |
| $2$ | $2.008$ | $0.28686\ldots$ | $0.287$ |
| $3$ | $2.934$ | $0.41914\ldots$ | $0.419$ |

모든 성분을 같은 $N=7$로 나누므로 $N_k$가 클수록 새 가중치도 커요.

#### (b) 합 확인과 증가 성분 판정

반올림 전 분자를 먼저 더하면 $\frac{2.058+2.008+2.934}{7}=\frac{7}{7}=1$이고, 반올림한 세 값도 $0.294+0.287+0.419=1.000$이에요.

갱신 전 $\frac{1}{3}\approx0.333$보다 큰 값은 $0.419$뿐이라 성분 $3$만 커졌어요.

#### 최종 답

(a) $(\pi_1^{\text{new}},\,\pi_2^{\text{new}},\,\pi_3^{\text{new}})=(0.294,\,0.287,\,0.419)$예요.

(b) 합은 정확히 $1$이고, $\frac{1}{3}$보다 커진 성분은 성분 $3$이에요.

#### 답 확인

#### (a) 검산

$0.294\times7=2.058$, $0.287\times7=2.009$, $0.419\times7=2.933$으로 주어진 $N_k$와 반올림 오차 안에서 맞아요.

#### (b) 확인

$\sum_k N_k=7=N$이고 $N_3=2.934\gt\frac{7}{3}\approx2.333$이라 반올림과 무관하게 결론이 같아요.

#### 주의할 점

분모는 성분 개수 $K=3$이 아니라 관측 수 $N=7$이에요. $3$으로 나누면 합이 $\frac{7}{3}$이 되어 확률이 되지 않아요.

**페이지 요약**

#### 떠올릴 개념·공식

$\pi_k^{\text{new}}=N_k/N$에서 $N$은 관측 수 $7$이에요. 표 전체의 열 합 $\sum_k N_k=N$이라 합은 항상 $1$이에요.

#### 첫 줄

$N=7$을 놓고 $\pi_1^{\text{new}}=2.058/7$부터 나눠요.

#### 핵심 답

(a) $(0.294,\,0.287,\,0.419)$, (b) 합은 $1$이고 $\frac{1}{3}$보다 커진 것은 성분 $3$이에요.

#### 검산

각 값에 $7$을 곱하면 주어진 $N_k$가 반올림 오차 안에서 복원돼요.

#### 조건·구분

분모에 $K=3$이 아닌 관측 수 $N=7$을 써야 해요.

#### 출제 근거

MML Example 11.5(혼합 가중치 갱신), 교과서 360쪽(PDF 366쪽)과 Example 11.2의 $N_1=2.058$, $N_2=2.008$, $N_3=2.934$(교과서 353쪽, PDF 359쪽).

수업: 1116 L07 s12. 관련 정리노트: [비율: 전체 몫 중 성분 k의 몫](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-pi)

#### 용어

- **혼합 가중치(mixing weight) $\pi_k$** — GMM에서 성분 $k$가 차지하는 비율이에요. $\pi_k\ge0$이고 $\sum_k\pi_k=1$이에요.
- **총 책임도(total responsibility) $N_k$** — $N_k=\sum_{n=1}^{N}r_{nk}$로, 성분 $k$가 전체 데이터에서 맡은 관측 수 분량이에요.

---

<a id="p2"></a>

### P2. 책임도 표로 평균 갱신하기

MML Example 11.3 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=2)

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

#### 풀이 목표

(a) $7\times3$ 책임도 표에서 세 성분의 총 책임도 $N_k=\sum_{n=1}^{7} r_{nk}$를 구해요. (b) 이 $N_k$로 세 성분의 새 평균 $\mu_k^{\text{new}}$를 구해요.

#### 풀이 단서

$N_k$는 책임도 표의 **열 합**이에요. 평균 갱신식 $\mu_k^{\text{new}}=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}x_n$은 합이 $1$인 가중치 $r_{nk}/N_k$로 낸 가중 평균이에요([평균: 합이 1인 가중치로 낸 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-mean)).

#### 첫 단계

열 $1$의 $0$이 아닌 칸만 골라 $N_1=1+1+\frac{1}{2}$을 적고, 같은 칸으로 $\sum_n r_{n1}x_n$을 구해요.

#### 핵심 풀이

#### (a) 총 책임도 계산

열 $1$은 $0$이 아닌 칸만 더해 $N_1=1+1+\frac{1}{2}=\frac{5}{2}$예요. 세 열을 표로 정리해요.

| 성분 $k$ | $0$이 아닌 칸 ($x_n$: $r_{nk}$) | $N_k$ |
|---|---|---|
| $1$ | $-4$: $1$, $-2$: $1$, $-1$: $\frac{1}{2}$ | $\frac{5}{2}$ |
| $2$ | $-1$: $\frac{1}{2}$, $0$: $1$, $2$: $\frac{1}{2}$ | $2$ |
| $3$ | $2$: $\frac{1}{2}$, $4$: $1$, $6$: $1$ | $\frac{5}{2}$ |

세 값의 합은 $\frac{5}{2}+2+\frac{5}{2}=7$로 관측 수와 같아요.

#### (b) 새 평균 계산

성분 $1$은 $\sum_n r_{n1}x_n=1\cdot(-4)+1\cdot(-2)+\frac{1}{2}\cdot(-1)=-\frac{13}{2}$이라 $\mu_1^{\text{new}}=\frac{-13/2}{5/2}=-\frac{13}{5}=-2.6$이에요.

| 성분 $k$ | $\sum_n r_{nk}x_n$ | $N_k$ | $\mu_k^{\text{new}}$ |
|---|---|---|---|
| $1$ | $-4-2-\frac{1}{2}=-\frac{13}{2}$ | $\frac{5}{2}$ | $-\frac{13}{5}=-2.6$ |
| $2$ | $-\frac{1}{2}+0+1=\frac{1}{2}$ | $2$ | $\frac{1}{4}=0.25$ |
| $3$ | $1+4+6=11$ | $\frac{5}{2}$ | $\frac{22}{5}=4.4$ |

각 평균이 맡은 관측 구간($[-4,-1]$, $[-1,2]$, $[2,6]$) 안에 놓여요.

#### 최종 답

(a) $(N_1,\,N_2,\,N_3)=\left(\frac{5}{2},\,2,\,\frac{5}{2}\right)$예요.

(b) $(\mu_1^{\text{new}},\,\mu_2^{\text{new}},\,\mu_3^{\text{new}})=(-2.6,\,0.25,\,4.4)$이고, 분수로는 $\left(-\frac{13}{5},\,\frac{1}{4},\,\frac{22}{5}\right)$예요.

#### 답 확인

#### (a) 검산

일곱 행의 합이 모두 $1$이므로 세 열 합의 합 $\sum_k N_k=7$과 맞아요.

#### (b) 검산

가중 평균은 $\sum_n r_{nk}(x_n-\mu_k^{\text{new}})=0$을 만족해요. 성분 $2$는 $\frac{1}{2}\left(-1-\frac{1}{4}\right)+1\left(0-\frac{1}{4}\right)+\frac{1}{2}\left(2-\frac{1}{4}\right)=0$이에요.

#### 주의할 점

$N_k$는 행 합이 아니라 **열 합**이에요. 또 평균을 낼 때 관측 수 $7$이나 $0$이 아닌 칸 수 $3$이 아니라 $N_k$로 나눠야 가중치 합이 $1$이에요.

**페이지 요약**

#### 떠올릴 개념·공식

$N_k$는 표의 열 합이고, $\mu_k^{\text{new}}=\frac{1}{N_k}\sum_n r_{nk}x_n$은 가중치 $r_{nk}/N_k$로 낸 가중 평균이에요.

#### 첫 줄

열 $1$의 $0$이 아닌 칸으로 $N_1=1+1+\frac{1}{2}$부터 더해요.

#### 핵심 답

(a) $N_k=\left(\frac{5}{2},2,\frac{5}{2}\right)$, (b) $\mu_k^{\text{new}}=(-2.6,\,0.25,\,4.4)=\left(-\frac{13}{5},\frac{1}{4},\frac{22}{5}\right)$예요.

#### 검산

열 합의 합이 $7$이고, 가중 편차 합 $\sum_n r_{nk}(x_n-\mu_k^{\text{new}})=0$이 성립해요.

#### 조건·구분

분모는 칸 수 $3$이나 전체 $7$이 아니라 열 합 $N_k$예요.

#### 출제 근거

MML Example 11.3(평균 갱신), 교과서 355쪽(PDF 361쪽)의 계산 구조를 분수로 끝나는 책임도 표로 바꾼 문항이에요.

관련 정리노트: [평균: 합이 1인 가중치로 낸 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-mean)

#### 용어

- **책임도(responsibility) $r_{nk}$** — 관측 $x_n$을 성분 $k$가 맡는 몫이에요. 각 행의 합은 $\sum_k r_{nk}=1$이에요.
- **총 책임도(total responsibility) $N_k$** — $N_k=\sum_n r_{nk}$로, 책임도 표의 열 합이에요.
- **가중 평균(weighted average)** — 합이 $1$인 가중치 $r_{nk}/N_k$로 관측을 평균한 값이에요.

---

<a id="p3"></a>

### P3. 교과서 책임도 표로 평균 갱신하기

MML Example 11.3 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=3)

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

#### 풀이 목표

(a) 반올림된 책임도 표의 수를 그대로 써서 세 성분의 새 평균 $\mu_k^{\text{new}}$를 둘째 자리까지 구해요. (b) 이동 거리 $|\mu_k^{\text{new}}-\mu_k|$와 가장 많이 움직인 성분을 골라요.

#### 풀이 단서

평균 갱신식 $\mu_k^{\text{new}}=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}x_n$에서 분자와 분모 모두 같은 열 $k$의 책임도를 써요([평균: 합이 1인 가중치로 낸 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-mean)). 갱신 전 평균 $\mu_k$는 (b)의 이동 거리 비교에만 써요.

#### 첫 단계

열 $1$에서 $0$이 아닌 칸($x_n=-3,-2.5,-1,0$)으로 $N_1=1.0+1.0+0.057+0.001$부터 계산해요.

#### 핵심 풀이

#### (a) 새 평균 계산

성분 $1$은 $N_1=2.058$, $\sum_n r_{n1}x_n=-3-2.5+0.057\cdot(-1)+0.001\cdot0=-5.557$이므로 $\mu_1^{\text{new}}=\frac{-5.557}{2.058}\approx-2.70$이에요. 세 성분을 표로 정리해요.

| 성분 $k$ | $N_k$ | $\sum_n r_{nk}x_n$ | $\mu_k^{\text{new}}$ (반올림 전) |
|---|---|---|---|
| $1$ | $2.058$ | $-5.557$ | $-2.70$ ($-2.7002$) |
| $2$ | $2.008$ | $-0.811$ | $-0.40$ ($-0.4039$) |
| $3$ | $2.934$ | $10.868$ | $3.70$ ($3.7042$) |

교과서 Example 11.3의 $(-2.7,-0.4,3.7)$과 같아요.

#### (b) 이동 거리와 최대 이동 성분

갱신 전후 평균의 거리는 $|-2.70-(-4)|=1.30$, $|-0.40-0|=0.40$, $|3.70-8|=4.30$이에요. 성분 $3$의 갱신 전 평균 $8$이 관측 범위 밖에 있어 가장 크게($4.30$) 움직여요.

#### 최종 답

(a) $(\mu_1^{\text{new}},\,\mu_2^{\text{new}},\,\mu_3^{\text{new}})\approx(-2.70,\,-0.40,\,3.70)$이에요.

(b) 이동 거리는 $(1.30,\,0.40,\,4.30)$이고, 가장 많이 움직인 성분은 성분 $3$이에요.

#### 답 확인

#### (a) 검산

$2.058+2.008+2.934=7$이고, 각 평균이 맡은 관측 구간($[-3,0]$, $[-1,2]$, $[2,5]$) 안에 있어요.

#### (b) 확인

반올림 전 값으로 계산해도 $(1.300,\,0.404,\,4.296)$이라 크기 순서가 같아요.

#### 주의할 점

$0.001$이나 $0.066$처럼 작은 책임도도 한쪽에만 빼면 가중치 합이 $1$이 깨지고, 양쪽에서 모두 빼면 관측이 누락되어 $\sum_k N_k=N$과 새 평균이 달라져요. (b)의 이동 거리는 방향 부호 없는 절댓값이에요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mu_k^{\text{new}}=\frac{1}{N_k}\sum_n r_{nk}x_n$에서 분자와 분모 모두 열 $k$의 책임도를 써요.

#### 첫 줄

열 $1$의 $0$이 아닌 칸으로 $N_1=1.0+1.0+0.057+0.001$을 먼저 구해요.

#### 핵심 답

(a) $(-2.70,\,-0.40,\,3.70)$, (b) 이동 거리는 $(1.30,\,0.40,\,4.30)$으로 성분 $3$이 최대예요.

#### 검산

$\sum_k N_k=7$이고, 반올림 전 값으로도 이동 거리 순서가 같아요.

#### 조건·구분

작은 책임도($0.001$, $0.066$)도 분자·분모에 모두 포함해야 해요.

#### 출제 근거

MML Example 11.2의 책임도 표(교과서 353쪽, PDF 359쪽)와 Example 11.3(평균 갱신, 교과서 355쪽, PDF 361쪽)이에요.

관련 정리노트: [평균: 합이 1인 가중치로 낸 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-mean)

#### 용어

- **책임도(responsibility) $r_{nk}$** — 관측 $x_n$을 성분 $k$가 맡는 몫이에요. 이 표는 교과서 값을 반올림한 것이고 각 행 합이 $1$이에요.
- **총 책임도(total responsibility) $N_k$** — $N_k=\sum_n r_{nk}$로, 책임도 표의 열 합이에요.

---

<a id="p4"></a>

### P4. 갱신된 평균으로 분산 갱신하기

MML Example 11.4 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=4)

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

#### 풀이 목표

(a) 주어진 $N_k$, 새 평균 $\mu_k^{\text{new}}=(-2.7,-0.4,3.7)$, 반올림된 책임도 표로 새 분산 $(\sigma_k^{\text{new}})^2$을 둘째 자리까지 구해요. (b) 갱신 전 분산 $(1,0.2,3)$ 대비 증감을 판정해요.

#### 풀이 단서

1차원 가중 분산 $(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_{n=1}^7 r_{nk}(x_n-\mu_k^{\text{new}})^2$에서 편차는 방금 구한 $\mu_k^{\text{new}}$에서 재요([공분산: 같은 가중치로 낸 편차 외적의 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-cov)). 갱신 전 분산 $\sigma_k^2$는 (b)의 비교 기준이에요.

#### 첫 단계

성분 $1$($\mu_1^{\text{new}}=-2.7$)에서 $r_{n1}\neq0$인 $x_n=-3,-2.5,-1,0$의 편차 $-0.3,\,0.2,\,1.7,\,2.7$과 제곱 $0.09,\,0.04,\,2.89,\,7.29$를 먼저 적어요.

#### 핵심 풀이

#### (a) 새 분산 계산

성분 $1$은 $1.0\cdot0.09+1.0\cdot0.04+0.057\cdot2.89+0.001\cdot7.29=0.30202$이고, $(\sigma_1^{\text{new}})^2=\frac{0.30202}{2.058}\approx0.15$예요. 세 성분을 표로 정리해요.

| 성분 $k$ | 가중합 | $\div N_k$ | $(\sigma_k^{\text{new}})^2$ |
|---|---|---|---|
| $1$ | $0.30202$ | $\div2.058=0.1468$ | $0.15$ |
| $2$ | $0.87948$ | $\div2.008=0.4380$ | $0.44$ |
| $3$ | $4.47926$ | $\div2.934=1.5267$ | $1.53$ |

표에 적힌 수로 계산하면 성분 $1$은 $0.15$예요. 교과서 Example 11.4의 $0.14$는 반올림 전 책임도(예: $r_{41}\approx0.00015$)를 쓴 결과예요.

#### (b) 갱신 전후 분산 비교

$1\to0.15$, $3\to1.53$은 줄었고, $0.2\to0.44$는 커졌어요. 성분 $2$는 $r_{52}=0.066$인 관측 $2$의 편차 제곱 $5.76$이 커서($0.066\cdot5.76\approx0.380$) 분산이 커졌어요.

#### 최종 답

(a) $\bigl((\sigma_1^{\text{new}})^2,\,(\sigma_2^{\text{new}})^2,\,(\sigma_3^{\text{new}})^2\bigr)\approx(0.15,\,0.44,\,1.53)$이에요.

(b) 성분 $1$·$3$은 줄었고, 성분 $2$는 커졌어요.

#### 답 확인

#### (a) 검산

각 가중 분산은 해당 성분이 맡은 관측의 최대 편차 제곱($7.29$, $5.76$, $2.89$)보다 작아 범위가 맞아요.

#### (b) 확인

반올림 전 값 $(0.1468,\,0.4380,\,1.5267)$으로 비교해도 증감 방향이 같아요.

#### 주의할 점

편차를 갱신 전 평균 $(-4,0,8)$이 아니라 새 평균 $\mu_k^{\text{new}}$에서 재야 해요. 또 $r_{nk}$는 제곱하지 않고 편차 제곱에만 한 번 곱해요.

**페이지 요약**

#### 떠올릴 개념·공식

1차원 가중 분산 $(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_n r_{nk}(x_n-\mu_k^{\text{new}})^2$이에요. 편차는 새 평균에서 재요.

#### 첫 줄

성분 $1$의 $0$이 아닌 칸 편차 $-0.3,\,0.2,\,1.7,\,2.7$을 제곱해 $r_{n1}$과 곱해요.

#### 핵심 답

(a) 새 분산 $(0.15,\,0.44,\,1.53)$, (b) 성분 $1$·$3$은 줄고 성분 $2$는 커졌어요.

#### 검산

각 분산이 해당 성분의 최대 편차 제곱보다 작고, 반올림 전 값으로도 증감이 같아요.

#### 교과서와의 차이

교과서의 성분 $1$ 값 $0.14$는 반올림 전 책임도 기준이고, 표의 $r_{41}=0.001$로 계산하면 $0.15$예요.

#### 출제 근거

MML Example 11.2의 책임도 표(교과서 353쪽, PDF 359쪽)와 Example 11.4(분산 갱신, 교과서 357–358쪽, PDF 363–364쪽)예요. 교과서는 $\sigma_1^2:1\to0.14$로 적었어요.

관련 정리노트: [공분산: 같은 가중치로 낸 편차 외적의 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-cov)

#### 용어

- **가중 분산(weighted variance)** — $(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_n r_{nk}(x_n-\mu_k^{\text{new}})^2$로, $D=1$일 때의 공분산 갱신식이에요.
- **총 책임도(total responsibility) $N_k$** — $N_k=\sum_n r_{nk}$로, 책임도 표의 열 합이에요.

---

<a id="p5"></a>

### P5. 수렴한 GMM을 초기값과 비교하기

MML Example 11.6 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=5)

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

#### 풀이 목표

(a) 수렴한 GMM 식의 세 혼합 가중치 합이 $1$인지 확인하고 표준편차 $\sigma_k$를 둘째 자리까지 구해요. (b) 초기값 대비 평균이 가장 많이 이동한 성분과 분산이 커진 성분을 골라요.

#### 풀이 단서

$p(x)=\sum_{k=1}^3 \pi_k\,\mathcal{N}(x\mid\mu_k,\sigma_k^2)$에서 앞 계수가 가중치 $\pi_k$, 세로선 뒤 둘째 값이 **분산** $\sigma_k^2$이므로 표준편차는 $\sigma_k=\sqrt{\sigma_k^2}$예요([E-step과 M-step의 순서](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-em-steps)).

#### 첫 단계

가중치 합 $0.29+0.28+0.43$부터 확인하고, 성분 $1,2,3$의 초기값과 수렴값을 나란히 적는 비교표를 만들어요.

#### 핵심 풀이

#### (a) 가중치 합과 표준편차

세 가중치의 합은 $0.29+0.28+0.43=1$이에요. 성분 $1$의 표준편차는 $\sigma_1=\sqrt{0.06}=0.2449\ldots\approx0.24$이고, 세 성분을 표로 정리해요.

| 성분 $k$ | 분산 $\sigma_k^2$ | $\sqrt{\sigma_k^2}$ | $\sigma_k$ |
|---|---|---|---|
| $1$ | $0.06$ | $0.2449\ldots$ | $0.24$ |
| $2$ | $0.25$ | $0.5$ | $0.50$ |
| $3$ | $1.63$ | $1.2767\ldots$ | $1.28$ |

분산이 $1$보다 작으면 $\sigma_k\gt\sigma_k^2$이고, $1$보다 크면 $\sigma_k\lt\sigma_k^2$예요.

#### (b) 초기값 대비 평균 이동과 분산 증감

성분 $3$의 이동 거리는 $|3.64-8|=4.36$이에요. 세 성분을 표로 비교해요.

| 성분 $k$ | $\mu_k$: 초기 $\to$ 수렴 | $\vert \Delta\mu_k\vert $ | $\sigma_k^2$: 초기 $\to$ 수렴 | 분산 증감 |
|---|---|---|---|---|
| $1$ | $-4\to-2.75$ | $1.25$ | $1\to0.06$ | 감소 |
| $2$ | $0\to-0.50$ | $0.50$ | $0.2\to0.25$ | 증가 |
| $3$ | $8\to3.64$ | $4.36$ | $3\to1.63$ | 감소 |

이동 거리는 성분 $3$($4.36$)이 가장 크고, 분산이 커진 성분은 성분 $2$($0.2\to0.25$)뿐이에요.

#### 최종 답

(a) 가중치 합은 $1$이고, 표준편차는 $(\sigma_1,\,\sigma_2,\,\sigma_3)\approx(0.24,\,0.50,\,1.28)$이에요.

(b) 평균이 가장 많이 이동한 성분은 성분 $3$(이동 거리 $4.36$), 분산이 커진 성분은 성분 $2$예요.

#### 답 확인

#### (a) 검산

$0.24^2=0.0576\approx0.06$, $0.50^2=0.25$, $1.28^2=1.6384\approx1.63$으로 반올림 오차 안에서 맞아요.

#### (b) 확인

$|\Delta\mu_1|=1.25$와 $|\Delta\mu_2|=0.50$ 모두 $4.36$보다 작고, 분산 비교는 $0.06\lt1$, $0.25\gt0.2$, $1.63\lt3$이에요.

#### 주의할 점

$\mathcal{N}(x\mid-2.75,\,0.06)$의 $0.06$은 표준편차가 아니라 분산이에요. (b)의 분산 비교도 표준편차가 아니라 분산끼리 비교해야 해요.

**페이지 요약**

#### 떠올릴 개념·공식

$p(x)=\sum_k\pi_k\mathcal{N}(x\mid\mu_k,\sigma_k^2)$에서 앞 계수가 가중치, 세로선 뒤 둘째 값이 분산이라 $\sigma_k=\sqrt{\sigma_k^2}$예요.

#### 첫 줄

$0.29+0.28+0.43$과 성분별 초기→수렴 비교표를 먼저 적어요.

#### 핵심 답

(a) 합 $1$, $\sigma_k\approx(0.24,\,0.50,\,1.28)$, (b) 평균 최대 이동은 성분 $3$($4.36$), 분산 증가는 성분 $2$예요.

#### 검산

구한 표준편차를 제곱하면 반올림 오차 범위에서 주어진 분산과 일치해요.

#### 조건·구분

둘째 값이 분산이므로 표준편차를 구할 때 제곱근을 취하고, 비교는 분산끼리 해요.

#### 출제 근거

MML Example 11.6(GMM Fit), 교과서 361–362쪽(PDF 367–368쪽)의 최종 GMM 식 (11.57)과 Example 11.3–11.5의 초기값이에요.

관련 정리노트: [E-step과 M-step의 순서](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-em-steps)

#### 용어

- **가우시안 혼합 모형(Gaussian mixture model, GMM)** — $p(x)=\sum_k\pi_k\mathcal{N}(x\mid\mu_k,\sigma_k^2)$처럼 가우시안 여러 개를 $\sum_k\pi_k=1$인 가중치로 섞은 밀도예요.
- **표준편차(standard deviation) $\sigma_k$** — 분산 $\sigma_k^2$의 제곱근이에요. $x$와 같은 단위의 퍼짐 폭이에요.

---

<a id="p6"></a>

### P6. 최소제곱 손실의 기울기와 차원

MML Example 5.11 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=6)

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

#### 풀이 목표

(a) 연쇄법칙 $\frac{\partial L}{\partial\boldsymbol{\theta}}=\frac{\partial L}{\partial\mathbf{e}}\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$로 $\frac{\partial L}{\partial\boldsymbol{\theta}}$를 $\mathbf{e}$, $\boldsymbol{\Phi}$로 나타내요. (b) 세 미분의 차원을 각각 읽어요.

#### 풀이 단서

수업의 행벡터 관례([기울기를 0으로](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s2-zero-gradient))로 스칼라 $L$을 열벡터 $\mathbf{e}$로 미분하면 **행벡터**이고, $\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$는 $(i,j)$ 성분이 $\partial e_i/\partial\theta_j$인 **출력×입력** 야코비안이에요([이차식 미분](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s2-log-gauss-quad)). 안쪽 차원 $N$을 맞추려면 $\frac{\partial L}{\partial\mathbf{e}}\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$ 순서를 지켜요.

#### 첫 단계

성분별로 미분하려고 $L=\mathbf{e}^\top\mathbf{e}=\sum_{n=1}^{N}e_n^2$와 $e_n=y_n-\sum_{d=1}^{D}\Phi_{nd}\theta_d$를 적어요.

#### 핵심 풀이

#### (a) 연쇄법칙으로 기울기 구하기

$$
L=\sum_{n=1}^{N}e_n^2
$$

↳ 제곱 노름을 성분 합으로 펼쳐요

$$
\frac{\partial L}{\partial\mathbf{e}}=\begin{bmatrix}2e_1&\cdots&2e_N\end{bmatrix}=2\mathbf{e}^\top
$$

↳ $\partial L/\partial e_n=2e_n$을 가로로 모아요

$$
e_n=y_n-\sum_{d=1}^{D}\Phi_{nd}\theta_d
$$

↳ $\boldsymbol{\Phi}\boldsymbol{\theta}$의 $n$번째 성분을 펼쳐요

$$
\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}=-\boldsymbol{\Phi}
$$

↳ $(n,d)$ 성분이 $\partial e_n/\partial\theta_d=-\Phi_{nd}$예요

$$
\frac{\partial L}{\partial\boldsymbol{\theta}}=2\mathbf{e}^\top(-\boldsymbol{\Phi})=-2\mathbf{e}^\top\boldsymbol{\Phi}
$$

↳ 연쇄법칙 순서대로 곱해요

$$
\hphantom{\frac{\partial L}{\partial\boldsymbol{\theta}}}=-2(\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta})^\top\boldsymbol{\Phi}
$$

↳ $\mathbf{e}=\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}$를 대입해요

#### (b) 세 미분의 차원 읽기

$\mathbf{e}\in\mathbb{R}^{N\times1}$이라 $2\mathbf{e}^\top\in\mathbb{R}^{1\times N}$이고, 야코비안 $-\boldsymbol{\Phi}$는 행이 출력($N$), 열이 입력($D$)이라 $\mathbb{R}^{N\times D}$예요.

$$
\underbrace{2\mathbf{e}^\top}_{1\times N}\;\underbrace{(-\boldsymbol{\Phi})}_{N\times D}\in\mathbb{R}^{1\times D}
$$

따라서 $\frac{\partial L}{\partial\boldsymbol{\theta}}$는 $\mathbb{R}^{1\times D}$ 행벡터예요.

#### 최종 답

(a) $\frac{\partial L}{\partial\boldsymbol{\theta}}=-2\mathbf{e}^\top\boldsymbol{\Phi}$ ($=-2(\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta})^\top\boldsymbol{\Phi}$)예요.

(b) $\frac{\partial L}{\partial\mathbf{e}}\in\mathbb{R}^{1\times N}$, $\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}\in\mathbb{R}^{N\times D}$, $\frac{\partial L}{\partial\boldsymbol{\theta}}\in\mathbb{R}^{1\times D}$예요.

#### 답 확인

#### (a) 검산

$N=D=1$이면 $L=(y-\phi\theta)^2$의 1변수 미분 $-2(y-\phi\theta)\phi$와 일치해요.

#### (b) 확인

곱 $(1\times N)(N\times D)$의 안쪽 $N$이 맞고, 결과 칸 수 $D$가 $\boldsymbol{\theta}$의 성분 수와 같아요.

#### 주의할 점

$\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$를 $-\boldsymbol{\Phi}^\top$($D\times N$)로 쓰면 $2\mathbf{e}^\top$($1\times N$)과 곱할 수 없고 성분 정의 $\partial e_i/\partial\theta_j$와도 어긋나요. $-2\boldsymbol{\Phi}^\top\mathbf{e}$는 답을 전치한 $D\times1$ 열벡터예요.

**페이지 요약**

#### 떠올릴 개념·공식

연쇄법칙 $\frac{\partial L}{\partial\boldsymbol{\theta}}=\frac{\partial L}{\partial\mathbf{e}}\frac{\partial\mathbf{e}}{\partial\boldsymbol{\theta}}$에서 스칼라 미분은 행벡터($1\times N$), 야코비안은 출력×입력($N\times D$)이에요.

#### 첫 줄

$L=\sum_n e_n^2$와 $e_n=y_n-\sum_d\Phi_{nd}\theta_d$를 성분으로 펼쳐요.

#### 핵심 답

(a) $-2\mathbf{e}^\top\boldsymbol{\Phi}$, (b) 차원은 차례로 $1\times N$, $N\times D$, $1\times D$예요.

#### 검산

$N=D=1$이면 $-2(y-\phi\theta)\phi$가 되고, 곱 $(1\times N)(N\times D)$의 안쪽 $N$이 맞아요.

#### 조건·구분

행벡터 관례이므로 전치된 열벡터 $-2\boldsymbol{\Phi}^\top\mathbf{e}$($D\times1$)와 구분해요.

#### 출제 근거

MML Example 5.11(Gradient of a Least-Squares Loss in a Linear Model), 교과서 154쪽(PDF 160쪽), 식 (5.75)–(5.83)이에요. 교과서도 $\frac{\partial L}{\partial\boldsymbol{\theta}}\in\mathbb{R}^{1\times D}$인 행벡터로 적었어요.

관련 정리노트: [이차식 미분](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s2-log-gauss-quad)

#### 용어

- **행벡터 미분** — 스칼라를 $D\times1$ 열벡터로 미분한 결과예요. 편미분 $D$개를 가로로 놓은 $1\times D$ 행벡터예요.
- **야코비안(Jacobian)** — 벡터 $\mathbf{e}\in\mathbb{R}^N$을 $\boldsymbol{\theta}\in\mathbb{R}^D$로 미분한 $N\times D$ 행렬이에요. $(i,j)$ 성분은 $\partial e_i/\partial\theta_j$예요.
- **연쇄법칙(chain rule)** — 합성함수의 미분을 각 단계 미분의 곱으로 구하는 규칙이에요. 행렬곱 순서를 지켜요.

---

<a id="p7"></a>

### P7. 분수로 분산 갱신하기

MML Example 11.4 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=7)

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

#### 풀이 목표

(a) 분수 책임도 표와 주어진 $N_k$, $\mu_k^{\text{new}}$로 새 분산 $(\sigma_k^{\text{new}})^2$을 기약분수로 구해요. (b) 갱신 전 분산 $\left(2,\frac{1}{2},3\right)$ 대비 증감을 판정해요.

#### 풀이 단서

1차원 가중 분산 $(\sigma_k^{\text{new}})^2=\frac{1}{N_k}\sum_{n=1}^{7} r_{nk}(x_n-\mu_k^{\text{new}})^2$를 계산해요([공분산: 같은 가중치로 낸 편차 외적의 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-cov)). $r_{nk}=0$인 칸을 빼면 성분마다 $3$개 관측만 남고, 편차를 분수로 통분해 더한 뒤 $N_k$로 나눠요.

#### 첫 단계

성분 $1$($\mu_1^{\text{new}}=-\frac{13}{5}$)에서 $r_{n1}\neq0$인 $x_n=-4,-2,-1$의 편차 $-\frac{7}{5},\,\frac{3}{5},\,\frac{8}{5}$부터 구해요.

#### 핵심 풀이

#### (a) 기약분수로 새 분산 구하기

성분 $1$은 $1\cdot\frac{49}{25}+1\cdot\frac{9}{25}+\frac{1}{2}\cdot\frac{64}{25}=\frac{90}{25}=\frac{18}{5}$이고, $\frac{18/5}{5/2}=\frac{36}{25}$예요. 세 성분을 표로 정리해요.

| 성분 $k$ | 편차 $x_n-\mu_k^{\text{new}}$ | $r_{nk}\times$편차 제곱 | 가중합 | $\div N_k$ |
|---|---|---|---|---|
| $1$ | $-\frac{7}{5},\ \frac{3}{5},\ \frac{8}{5}$ | $\frac{49}{25}+\frac{9}{25}+\frac{1}{2}\cdot\frac{64}{25}$ | $\frac{18}{5}$ | $\frac{18}{5}\cdot\frac{2}{5}=\frac{36}{25}$ |
| $2$ | $-\frac{5}{4},\ -\frac{1}{4},\ \frac{7}{4}$ | $\frac{1}{2}\cdot\frac{25}{16}+\frac{1}{16}+\frac{1}{2}\cdot\frac{49}{16}$ | $\frac{19}{8}$ | $\frac{19}{8}\cdot\frac{1}{2}=\frac{19}{16}$ |
| $3$ | $-\frac{12}{5},\ -\frac{2}{5},\ \frac{8}{5}$ | $\frac{1}{2}\cdot\frac{144}{25}+\frac{4}{25}+\frac{64}{25}$ | $\frac{28}{5}$ | $\frac{28}{5}\cdot\frac{2}{5}=\frac{56}{25}$ |

세 분수 모두 분자·분모가 서로소라 기약분수예요.

#### (b) 갱신 전후 분산 비교

$\frac{36}{25}=1.44\lt2$, $\frac{19}{16}=1.1875\gt\frac{1}{2}$, $\frac{56}{25}=2.24\lt3$이므로 성분 $1$·$3$은 줄었고, 성분 $2$는 커졌어요.

#### 최종 답

(a) $\bigl((\sigma_1^{\text{new}})^2,\,(\sigma_2^{\text{new}})^2,\,(\sigma_3^{\text{new}})^2\bigr)=\left(\frac{36}{25},\,\frac{19}{16},\,\frac{56}{25}\right)$예요.

(b) 성분 $1$·$3$은 줄었고, 성분 $2$는 커졌어요.

#### 답 확인

#### (a) 검산

$\mu_k^{\text{new}}$가 같은 가중치 평균이라 ‘제곱의 평균 − 평균의 제곱’과 같아야 해요. 성분 $2$는 $\frac{1}{2}\left(\frac{1}{2}\cdot1+1\cdot0+\frac{1}{2}\cdot4\right)-\left(\frac{1}{4}\right)^2=\frac{5}{4}-\frac{1}{16}=\frac{19}{16}$이에요.

#### (b) 확인

분수로 통분해도 $\frac{36}{25}\lt\frac{50}{25}$, $\frac{19}{16}\gt\frac{8}{16}$, $\frac{56}{25}\lt\frac{75}{25}$로 같아요.

#### 주의할 점

반씩 맡은 관측($-1,2$)의 편차 제곱에는 $\frac{1}{2}$을 곱해야 해요. 또 나누는 분모는 $0$이 아닌 칸 수 $3$이 아니라 $N_k$예요.

**페이지 요약**

#### 떠올릴 개념·공식

1차원 가중 분산 $\frac{1}{N_k}\sum_n r_{nk}(x_n-\mu_k^{\text{new}})^2$에서 $r_{nk}\neq0$인 $3$개 관측만 남겨 분수로 계산해요.

#### 첫 줄

성분 $1$($\mu_1^{\text{new}}=-\frac{13}{5}$)의 편차 $-\frac{7}{5},\,\frac{3}{5},\,\frac{8}{5}$부터 적어요.

#### 핵심 답

(a) $\left(\frac{36}{25},\,\frac{19}{16},\,\frac{56}{25}\right)$, (b) 성분 $1$·$3$은 줄고 성분 $2$는 커졌어요.

#### 검산

같은 가중치의 제곱의 평균 − 평균의 제곱으로도 성분 $2$가 $\frac{19}{16}$으로 일치해요.

#### 조건·구분

반만 맡은 관측에 $\frac{1}{2}$을 곱하고, 분모는 칸 수 $3$이 아니라 $N_k$로 나눠요.

#### 출제 근거

MML Example 11.4(분산 갱신), 교과서 357–358쪽(PDF 363–364쪽)의 계산 구조를 분수로 끝나는 책임도 표로 바꾼 문항이에요. 표와 새 평균은 복습문제 2번과 같아요.

관련 정리노트: [공분산: 같은 가중치로 낸 편차 외적의 평균](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s1-meaning-cov)

#### 용어

- **가중 분산(weighted variance)** — $\frac{1}{N_k}\sum_n r_{nk}(x_n-\mu_k^{\text{new}})^2$로, 책임도로 가중한 편차 제곱의 평균이에요.
- **총 책임도(total responsibility) $N_k$** — $N_k=\sum_n r_{nk}$로, 책임도 표의 열 합이에요.

---

<a id="p8"></a>

### P8. 벡터와 행렬로 스칼라 함수 미분하기

MML Exercise 5.6 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1116_EM_Algorithm-%EB%AC%B8%EC%A0%9C.pdf#page=8)

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

#### 풀이 목표

(a) $f(\mathbf{t})=\sin\bigl(\log(\mathbf{t}^\top\mathbf{t})\bigr)$의 행벡터 미분 $\frac{df}{d\mathbf{t}}$를 구해요. (b) $g(\mathbf{X})=\operatorname{tr}(\mathbf{A}\mathbf{X}\mathbf{B})$의 행렬 미분 $\frac{dg}{d\mathbf{X}}$를 구해요. (c) 두 미분의 차원을 각각 읽어요.

#### 풀이 단서

(a) 안쪽 스칼라 $u=\mathbf{t}^\top\mathbf{t}$($\gt0$, $\mathbf{t}\neq\mathbf{0}$)로 치환해 연쇄법칙 $\frac{df}{d\mathbf{t}}=\frac{df}{du}\frac{du}{d\mathbf{t}}$와 행벡터 미분 $\frac{d(\mathbf{t}^\top\mathbf{t})}{d\mathbf{t}}=2\mathbf{t}^\top$을 써요([기울기를 0으로](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s2-zero-gradient)). (b) 대각합 $g=\sum_{i=1}^{D}(\mathbf{A}\mathbf{X}\mathbf{B})_{ii}$를 성분 삼중합으로 펼쳐 $\left[\frac{dg}{d\mathbf{X}}\right]_{pq}=\frac{\partial g}{\partial X_{pq}}$로 모아요([칸마다 미분하는 정의](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s3-matrix-deriv-def)).

#### 첫 단계

(a)는 $u=\mathbf{t}^\top\mathbf{t}=\sum_{d=1}^{D}t_d^2$, (b)는 $g=\sum_{i=1}^{D}(\mathbf{A}\mathbf{X}\mathbf{B})_{ii}$를 적어요.

#### 핵심 풀이

#### (a) 벡터 함수 f의 미분

$$
u=\mathbf{t}^\top\mathbf{t}=\sum_{d=1}^{D}t_d^2
$$

↳ 안쪽 스칼라를 $u$로 둬요

$$
\frac{du}{d\mathbf{t}}=2\mathbf{t}^\top
$$

↳ $\partial u/\partial t_d=2t_d$를 행벡터로 모아요

$$
\frac{df}{du}=\cos(\log u)\cdot\frac{1}{u}
$$

↳ $\sin$과 $\log$를 차례로 미분해요

$$
\frac{df}{d\mathbf{t}}=\frac{2\cos\bigl(\log(\mathbf{t}^\top\mathbf{t})\bigr)}{\mathbf{t}^\top\mathbf{t}}\,\mathbf{t}^\top
$$

↳ $\frac{df}{du}\frac{du}{d\mathbf{t}}$에 $u$를 되돌려요

#### (b) 대각합 g의 행렬 미분

첨자 $i=1,\dots,D$, $j=1,\dots,E$, $l=1,\dots,F$로 펼쳐 $(p,q)$ 성분을 편미분해요.

$$
(\mathbf{A}\mathbf{X}\mathbf{B})_{ii}=\sum_{l=1}^{F}(\mathbf{A}\mathbf{X})_{il}B_{li}
$$

↳ $(\mathbf{A}\mathbf{X})\mathbf{B}$의 대각 성분을 펼쳐요

$$
\hphantom{(\mathbf{A}\mathbf{X}\mathbf{B})_{ii}}=\sum_{j=1}^{E}\sum_{l=1}^{F}A_{ij}X_{jl}B_{li}
$$

↳ $(\mathbf{A}\mathbf{X})_{il}=\sum_{j=1}^E A_{ij}X_{jl}$을 넣어요

$$
g=\sum_{i=1}^{D}\sum_{j=1}^{E}\sum_{l=1}^{F}A_{ij}X_{jl}B_{li}
$$

↳ 대각합은 $i=1,\dots,D$의 합이에요

$$
\frac{\partial g}{\partial X_{pq}}=\sum_{i=1}^{D}A_{ip}B_{qi}
$$

↳ $j=p$, $l=q$인 항만 $X_{pq}$를 포함해요

$$
\hphantom{\frac{\partial g}{\partial X_{pq}}}=\sum_{i=1}^{D}(\mathbf{A}^\top)_{pi}(\mathbf{B}^\top)_{iq}=(\mathbf{A}^\top\mathbf{B}^\top)_{pq}
$$

↳ 전치로 행×열 곱 첨자를 맞춰요

$$
\frac{dg}{d\mathbf{X}}=\mathbf{A}^\top\mathbf{B}^\top
$$

↳ $(p,q)$ 자리에 모아 행렬을 만들어요

#### (c) 두 미분의 차원 읽기

$\frac{df}{d\mathbf{t}}$는 스칼라 배와 $1\times D$ 행벡터 $\mathbf{t}^\top$의 곱이라 $\mathbb{R}^{1\times D}$예요. $\frac{dg}{d\mathbf{X}}$는 $\mathbf{A}^\top$($E\times D$)과 $\mathbf{B}^\top$($D\times F$)의 곱이라 $\mathbf{X}$와 같은 $\mathbb{R}^{E\times F}$예요.

#### 최종 답

(a) $\frac{df}{d\mathbf{t}}=\frac{2\cos\bigl(\log(\mathbf{t}^\top\mathbf{t})\bigr)}{\mathbf{t}^\top\mathbf{t}}\,\mathbf{t}^\top$예요.

(b) $\frac{dg}{d\mathbf{X}}=\mathbf{A}^\top\mathbf{B}^\top$예요.

(c) $\frac{df}{d\mathbf{t}}\in\mathbb{R}^{1\times D}$, $\frac{dg}{d\mathbf{X}}\in\mathbb{R}^{E\times F}$예요.

#### 답 확인

#### (a) 검산

$D=1$, $t\gt0$이면 $f=\sin(2\log t)$의 1변수 미분 $\frac{2\cos(2\log t)}{t}$와 같아요.

#### (b) 검산

$D=E=F=1$이면 $g=aXb$의 미분 $ab$와 같고, $\mathbf{A}^\top\mathbf{B}^\top=(\mathbf{B}\mathbf{A})^\top$의 크기도 $(F\times E)^\top=E\times F$예요.

#### (c) 확인

미분 결과의 칸 수가 각각 $\mathbf{t}$($D$개)와 $\mathbf{X}$($E\times F$)의 원소 수와 맞아요.

#### 주의할 점

(a)에서 $\frac{du}{d\mathbf{t}}$를 열벡터 $2\mathbf{t}$로 쓰면 수업 관례와 달라요. (b)에서 전치 없는 $\mathbf{B}\mathbf{A}$($F\times E$)는 $E\neq F$일 때 차원부터 다르고 $E=F$여도 성분이 $\sum_i A_{ip}B_{qi}$와 어긋나요.

**페이지 요약**

#### 떠올릴 개념·공식

(a) $u=\mathbf{t}^\top\mathbf{t}$ 연쇄법칙과 행벡터 미분 $2\mathbf{t}^\top$, (b) $\operatorname{tr}(\mathbf{A}\mathbf{X}\mathbf{B})$를 삼중합으로 펼쳐 $X_{pq}$로 편미분해요.

#### 첫 줄

(a)는 $u=\sum_d t_d^2$, (b)는 $g=\sum_i (\mathbf{A}\mathbf{X}\mathbf{B})_{ii}$를 먼저 적어요.

#### 핵심 답

(a) $\frac{2\cos(\log(\mathbf{t}^\top\mathbf{t}))}{\mathbf{t}^\top\mathbf{t}}\mathbf{t}^\top$($1\times D$), (b) $\mathbf{A}^\top\mathbf{B}^\top$($E\times F$)이에요.

#### 검산

1차원으로 줄이면 1변수 미분과 일치하고, 행렬 미분은 $\mathbf{X}$와 같은 $E\times F$ 모양이에요.

#### 조건·구분

행벡터 미분이므로 $\mathbf{t}^\top$로 끝나고, 행렬 미분은 $\mathbf{B}\mathbf{A}$가 아닌 $\mathbf{A}^\top\mathbf{B}^\top$이에요.

#### 출제 근거

MML Exercise 5.6, 교과서 171쪽(PDF 177쪽)이에요. 미분 방향은 수업 관례(열벡터 변수에 대한 스칼라 미분은 행벡터, 행렬 미분은 원소별 같은 자리)를 문제 조건에 명시했어요.

관련 정리노트: [칸마다 미분하는 정의](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1116_EM_Algorithm.html#s3-matrix-deriv-def)

#### 용어

- **행벡터 미분** — 스칼라를 $D\times1$ 열벡터로 미분한 결과예요. 편미분을 가로로 놓은 $1\times D$ 행벡터예요.
- **스칼라의 행렬 미분** — $\partial g/\partial X_{pq}$를 $(p,q)$ 자리에 둔 행렬이에요. 결과는 $\mathbf{X}$와 같은 $E\times F$ 모양이에요.
- **대각합(trace) $\operatorname{tr}$** — 정사각행렬의 대각 성분 합 $\operatorname{tr}(\mathbf{M})=\sum_i M_{ii}$예요.

---
