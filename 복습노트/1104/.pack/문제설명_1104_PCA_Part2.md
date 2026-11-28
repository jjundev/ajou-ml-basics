# 머신러닝기초 복습 1104 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [P1. 숫자 8의 누적 설명 분산](#p1)
  - [P2. 주성분 평면에 놓인 숫자 0과 1](#p2)
  - [P3. 주성분 개수와 숫자 8의 복원](#p3)
  - [P4. 가로로 긴 행렬의 특잇값 분해](#p4)
  - [P5. 영화 평점 행렬의 랭크 2 근사](#p5)
  - [P6. 사영을 뺀 나머지도 사영일까](#p6)
  - [P7. 왼쪽 특이벡터부터 구하는 특잇값 분해](#p7)
  - [P8. 2×2 행렬의 특잇값 분해](#p8)
  - [P9. 가장 큰 특잇값으로 만든 랭크 1 근사](#p9)
  - [P10. 행렬이 벡터의 길이를 가장 크게 늘리는 비율](#p10)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### P1. 숫자 8의 누적 설명 분산

MML Example 10.2 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=1)

#### 주어진 조건

MNIST 학습 데이터에서 숫자 8만 골라 공분산 행렬 $\mathbf S$를 구했어요. $\mathbf S$의 고윳값을 큰 순서로 $\lambda_1\ge\lambda_2\ge\cdots$라 하고, 앞에서부터 $M$개의 주성분이 담는 누적 설명 분산을 $V_M$이라 해요. 정리노트에서 배운 식으로는 다음과 같아요.

$$
V_M=\sum_{m=1}^{M}\lambda_m
$$

왼쪽은 큰 고윳값 200개를 순서대로 찍은 그래프이고, 오른쪽은 주성분 개수 $M$에 따른 $V_M$ 그래프예요.

#### 구할 것

- (a) $M$번째 주성분을 추가할 때 늘어나는 양 $V_M-V_{M-1}$을 고윳값으로 나타내 보세요.
- (b) (a)의 결과를 써서, 주성분을 처음 몇 개 추가할 때와 뒤에서 추가할 때 중 어느 쪽에서 누적 설명 분산이 크게 늘어나는지 왼쪽 그래프를 근거로 설명해 보세요.

![왼쪽은 고윳값과 순서, 오른쪽은 누적 설명 분산과 주성분 개수를 나타낸 그래프](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1104_PCA_Part2/e38c6cc8acd8a6f5-mml-figure-10-5.png)

그림 10.5

<details><summary>원문 보기</summary>

“We see that only a few of them have a value that differs significantly from 0.” — Example 10.2

</details>

#### 풀이 목표

(a) 누적 설명 분산 $V_M$의 차분 $V_M-V_{M-1}$을 고윳값으로 나타내고, (b) 주성분을 앞쪽과 뒤쪽에서 추가할 때 증가 폭을 왼쪽 그래프로 비교해요.

#### 풀이 단서

고윳값 $\lambda_m$은 공분산 행렬 $\mathbf S$의 $m$번째 단위 고유벡터 $\mathbf p_m$ 방향 분산($\mathbf p_m^\top\mathbf S\mathbf p_m=\lambda_m$)이에요. 내림차순($\lambda_1\ge\lambda_2\ge\cdots$) 고윳값의 합 $V_M=\sum_{m=1}^{M}\lambda_m$이 상위 $M$개 주성분의 누적 설명 분산이에요([첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions)).

따라서 $V_M$과 $V_{M-1}$의 차이는 마지막 항 $\lambda_M$뿐이고, 왼쪽 그래프의 점 높이가 오른쪽 곡선의 한 칸 상승 폭이에요.

#### 첫 단계

$$
V_M=\sum_{m=1}^{M}\lambda_m=V_{M-1}+\lambda_M,\qquad V_{M-1}=\sum_{m=1}^{M-1}\lambda_m
$$

두 합을 빼서 한 칸 증가량을 구한 뒤, 왼쪽 그래프의 초반·후반 점 높이를 비교해요.

#### 핵심 풀이

#### (a) 한 개 추가 시 증가량

$V_M$에서 $V_{M-1}$을 빼면 앞의 공통인 $M-1$개 항이 모두 상쇄돼요.

$$
V_M-V_{M-1}=\sum_{m=1}^{M}\lambda_m-\sum_{m=1}^{M-1}\lambda_m=\lambda_M
$$

$M$번째 주성분을 추가하면 누적 설명 분산은 그 축의 고윳값 $\lambda_M$만큼 늘어요.

#### (b) 초반과 후반의 증가 폭 비교

(a)에 따라 오른쪽 곡선의 한 칸 상승 폭은 왼쪽 그래프의 점 높이 $\lambda_M$이에요. 왼쪽 그래프에서 $m=1,2$일 때 고윳값이 약 $46$, 약 $32$로 크고 $m=3\sim 5$에서도 빠르게 작아진 뒤, $m\approx 50$에서는 약 $2\sim 3$, $m\approx 150\sim 200$에서는 $1$ 미만(양수)으로 낮아져요.

그래서 주성분을 처음 몇 개 추가할 때 누적 설명 분산이 크게 늘고, 뒤에서 추가할 때는 완만하게 늘어요.

#### 최종 답

(a) $V_M-V_{M-1}=\lambda_M$이에요.

(b) 앞쪽 몇 개 고윳값(약 46, 32)이 크고 뒤로 갈수록 빠르게 작아지므로, 처음 몇 개를 추가할 때 누적 설명 분산이 크게 늘고 뒤에서는 완만하게 늘어요.

#### 답 확인

#### (a) 검산

빈 합 $V_0=0$을 쓰면 $M=1$에서 $V_1-V_0=\lambda_1$이고, 오른쪽 곡선의 시작 높이(약 46)가 왼쪽 첫 점 $\lambda_1\approx 46$과 맞아요. $M=2$도 $V_2\approx 46+32=78$로 일치해요.

#### (b) 검산

오른쪽 그래프의 50칸 증가량은 $[0,50]$에서 약 $370$, $[150,200]$에서 약 $20$($\approx 525-505$)이에요. 초반 증가가 후반의 약 18배로 왼쪽 점 높이 감소와 맞아요.

#### 주의할 점

오른쪽 곡선의 높이($V_M$)와 한 칸 증가량($\lambda_M$)을 혼동하지 않아요. 또 $m=150\sim 200$에서 $\lambda_m$이 작아도 양수여서 곡선은 200개까지 계속 조금씩 올라요. $V_M$은 비율(%)이 아니라 분산의 합이에요.

**페이지 요약**

#### 떠올릴 개념·공식

$\lambda_m$은 $m$번째 주성분 방향의 분산이고 $V_M=\sum_{m=1}^{M}\lambda_m$이에요.

#### 첫 줄

$V_M=V_{M-1}+\lambda_M$으로 마지막 항만 분리해요.

#### 핵심 답

(a) $V_M-V_{M-1}=\lambda_M$이에요. (b) 앞쪽 고윳값이 크고 빠르게 감소해 처음 몇 개를 추가할 때 크게 늘고 뒤에서는 완만하게 늘어요.

#### 검산

시작 높이 약 46이 $\lambda_1$과 같고, 50칸 증가량도 $[0,50]$ 약 370 vs $[150,200]$ 약 20이에요.

#### 조건·구분

오른쪽 높이는 누적합, 왼쪽 점 높이는 한 칸 증분이에요. $V_M$은 비율이 아니라 분산의 합이에요.

#### 출제 근거

MML Example 10.2와 그림 10.5, 교과서 324–325쪽(PDF 330–331쪽), 식 (10.24).

수업: 1104 L05 s27–28(상위 $M$개 방향과 보존 분산).

관련 정리노트: [첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions)

#### 용어

- **고윳값(eigenvalue)** — 공분산 행렬 $\mathbf S$에서 $\mathbf S\mathbf p_m=\lambda_m\mathbf p_m$을 만족하는 수로, 단위 고유벡터 $\mathbf p_m$ 방향의 분산이에요.
- **주성분(principal component)** — 큰 고윳값 순서대로 고른 공분산 행렬의 서로 직교하는 단위 고유벡터 방향이에요.
- **누적 설명 분산(captured variance)** — 상위 $M$개 주성분이 담는 분산의 총합 $V_M=\sum_{m=1}^{M}\lambda_m$이에요.

---

<a id="p2"></a>

### P2. 주성분 평면에 놓인 숫자 0과 1

MML Example 10.3 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=2)

#### 주어진 조건

MNIST 학습 데이터의 숫자 0(파란 점)과 숫자 1(주황 점)을 첫 두 주성분이 만드는 평면에 찍었어요. 점 하나가 이미지 한 장이에요. 빨간 표시와 선은 일부 점을 원래 이미지와 이어 줘요.

#### 구할 것

- (a) 숫자 0과 1의 점 무리는 얼마나 잘 나뉘나요? 그림을 근거로 답해 보세요.
- (b) 어느 숫자 집단이 주성분 평면에서 더 넓게 퍼져 있는지(집단 안의 분산이 더 큰 쪽) 그림에서 읽어 보세요.

![첫 두 주성분 평면에서 파란 점은 숫자 0, 주황 점은 숫자 1을 나타낸 산점도](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1104_PCA_Part2/1c20de4b2473ac2d-mml-figure-10-10.png)

그림 10.10

<details><summary>원문 보기</summary>

“We observe a relatively clear separation between “0”s (blue dots) and “1”s (orange dots)” … “the variation within the set of “0” is significantly greater” — Example 10.3

</details>

#### 풀이 목표

첫 두 주성분 평면의 산점도(파란 점: 숫자 0, 주황 점: 숫자 1)에서 (a) 두 숫자 무리의 분리 정도와 (b) 집단 안의 분산이 더 큰 쪽을 읽어요.

#### 풀이 단서

각 점은 중심화한 784차원 이미지를 상위 두 주성분 기저 $\mathbf B=[\mathbf b_1,\mathbf b_2]\in\mathbb R^{784\times 2}$에 사영한 2차원 좌표 $\mathbf z_n=\mathbf B^\top\mathbf x_n\in\mathbb R^2$예요([MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)).

분리 정도는 두 무리의 중심 분리와 경계 겹침 여부로 읽고, 집단 안의 분산은 각 집단 중심에서 점들이 떨어진 제곱 거리의 평균이므로 외곽점 몇 개보다 중심부터 외곽까지 퍼진 폭을 비교해요.

#### 첫 단계

산점도에서 파란 점(0)과 주황 점(1)이 모인 위치와 경계의 겹침을 먼저 확인한 뒤, 각 무리의 가로·세로 퍼짐을 비교해요. 빨간 선은 대표 점과 원본 이미지를 잇는 안내선이에요.

#### 핵심 풀이

#### (a) 두 숫자 무리의 분리 정도

주황 점(숫자 1)은 왼쪽의 좁은 영역에 모여 있고, 파란 점(숫자 0)은 그 오른쪽에서 위아래로 넓게 자리 잡아 두 무리의 중심이 뚜렷하게 떨어져 있어요.

두 무리가 맞닿는 중앙 경계에서는 주황 점과 파란 점 일부가 섞여 완전히 분리되지는 않지만, 784차원을 2차원으로 줄였는데도 두 무리는 비교적 뚜렷하게 나뉘어요.

#### (b) 집단 안의 분산 비교

주황 점(숫자 1)은 왼쪽 작은 영역 안에 조밀하게 뭉쳐 있는 반면, 파란 점(숫자 0)은 중심부부터 오른쪽과 아래쪽까지 가로·세로로 훨씬 넓게 퍼져 있어요.

따라서 각 집단 중심으로부터의 제곱 거리 평균인 집단 안의 분산은 숫자 0 쪽이 더 커요. 안내선에 연결된 이미지에서도 1은 비슷한 세로 획인 반면 0은 기울기와 너비 변화가 크게 보여요.

#### 최종 답

(a) 숫자 0과 1의 점 무리는 경계에서 일부 점이 겹치지만 비교적 뚜렷하게 나뉘어요.

(b) 숫자 0(파란 점) 집단이 주성분 평면에서 훨씬 넓게 퍼져 있어 집단 안의 분산이 더 커요.

#### 답 확인

#### (a) 검산

왼쪽 안내선 4개는 모두 주황 영역에서 숫자 1 이미지로 이어지고, 오른쪽 안내선 4개는 모두 파란 영역에서 숫자 0 이미지로 이어져 두 영역의 분류와 맞아요.

#### (b) 검산

외곽 점 몇 개만이 아니라 점이 조밀한 중심 영역 자체의 가로·세로 폭도 파란 무리가 주황 무리보다 훨씬 넓어 숫자 0의 분산이 크다는 판정이 유지돼요.

#### 주의할 점

점유 면적(가장 먼 외곽점)만 보고 분산을 단정하지 않고 중심 주변 점들의 전체 퍼짐을 함께 봐요. (a)의 분리도와 (b)의 집단 내 분산은 서로 다른 질문이며, 이 비교는 784차원 전체가 아니라 첫 두 주성분 평면(2차원)에서의 결과예요.

**페이지 요약**

#### 떠올릴 개념·공식

점의 좌표는 $\mathbf z_n=\mathbf B^\top\mathbf x_n\in\mathbb R^2$이고, 분리는 경계 겹침, 분산은 각 집단 중심에서의 퍼짐으로 읽어요.

#### 첫 줄

파란 점(0)과 주황 점(1)의 위치·경계 겹침과 각 무리의 가로·세로 폭을 읽어요.

#### 핵심 답

(a) 경계에 일부 겹침이 있으나 비교적 뚜렷하게 나뉘어요. (b) 숫자 0 집단이 더 넓게 퍼져 집단 안의 분산이 더 커요.

#### 검산

빨간 안내선이 왼쪽 1·오른쪽 0 영역과 맞고, 파란 무리는 밀집 영역 자체도 훨씬 넓어요.

#### 조건·구분

집단 내 분산은 중심에서의 퍼짐으로 판단하며, 2차원 사영 평면에서의 관찰이에요.

#### 출제 근거

MML Example 10.3과 그림 10.10, 교과서 332–333쪽(PDF 338–339쪽).

수업: 1104 L06 s11(MNIST 0과 1의 2차원 사영).

관련 정리노트: [MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)

#### 용어

- **주성분 평면(principal subspace)** — 상위 두 주성분 기저 벡터 $\mathbf b_1,\mathbf b_2$가 만드는 2차원 부분공간이에요.
- **사영 좌표(projection coordinates)** — 중심화 데이터와 주성분 기저의 내적 $\mathbf z_n=\mathbf B^\top\mathbf x_n$으로 얻은 저차원 좌표예요.
- **집단 안의 분산(within-class variance)** — 같은 집단의 점들이 자기 집단 중심으로부터 떨어진 제곱 거리의 평균이에요.

---

<a id="p3"></a>

### P3. 주성분 개수와 숫자 8의 복원

MML Example 10.4 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=3)

#### 주어진 조건

MNIST 숫자 이미지는 가로세로 28픽셀이라 $D=784$차원 벡터예요. 숫자 8의 학습 이미지 5,389장으로 주성분을 구했어요. 그림 맨 윗줄은 테스트 이미지 네 장의 원본이고, 아랫줄들은 같은 네 장을 주성분 1개, 10개, 100개, 500개로 복원한 결과예요.

공분산 행렬의 고윳값을 $\lambda_1\ge\cdots\ge\lambda_{784}\ge0$이라 하면, 상위 $M$개 주성분으로 복원할 때 학습 데이터의 평균 제곱 복원오차(최솟값)는 다음과 같아요.

$$
J_M^\star=\sum_{i=M+1}^{D}\lambda_i
$$

MML에 따르면 이 오차를 $M$에 따라 그린 곡선(그림 10.13)은 주성분이 약 400개를 넘으면 거의 0이고, 약 550개면 학습 데이터를 사실상 완전히 복원해요. 가장자리 픽셀은 늘 검정이라 분산이 0이에요.

#### 구할 것

- (a) 주성분을 1개, 10개, 100개, 500개로 늘려 가면 복원 이미지가 어떻게 달라지는지 그림에서 읽어 보세요.
- (b) 주성분 784개를 모두 쓸 때의 평균 제곱 복원오차 $J_{784}^\star$를 구해, 원본이 얼마나 정확히 복원되는지 답해 보세요.
- (c) (b)의 식과 조건의 오차 곡선을 이어, 주성분 500개만으로도 테스트 이미지가 거의 완벽하게 복원되는 이유를 설명해 보세요.

![테스트 이미지의 원본과 주성분 1개, 10개, 100개, 500개로 복원한 결과](figures_%EB%AC%B8%EC%A0%9C%EC%84%A4%EB%AA%85_1104_PCA_Part2/0528b87138766c3b-mml-figure-10-12.png)

그림 10.12

<details><summary>원문 보기</summary>

“With 500 principal components, we effectively obtain a near-perfect reconstruction.” … “784 PCs, we would recover the exact digit” — Example 10.4

</details>

#### 풀이 목표

$D=784$차원 숫자 8 이미지에서 (a) 그림 10.12의 $M=1,10,100,500$ 복원 변화를 읽고, (b) $M=784$일 때 $J_{784}^\star$와 완전 복원을 보이며, (c) 500개만으로 테스트 이미지가 거의 완벽히 복원되는 이유를 설명해요.

#### 풀이 단서

원본 이미지 벡터를 $\mathbf x$, 학습 이미지 5,389장의 평균 벡터를 $\bar{\mathbf x}$라 두면 상위 $M$개 정규직교 고유벡터 열행렬 $\mathbf B\in\mathbb R^{784\times M}$로 중심화 벡터를 사영·복원해요([MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)).

$$
\tilde{\mathbf x}=\bar{\mathbf x}+\mathbf B\mathbf z,\qquad \mathbf z=\mathbf B^\top(\mathbf x-\bar{\mathbf x})
$$

$M=D=784$이면 $\mathbf B$가 정사각 직교행렬이라 $\mathbf B\mathbf B^\top=\mathbf I_{784}$가 되고, 학습 평균 제곱 복원오차는 버린 방향의 고윳값 합 $J_M^\star=\sum_{i=M+1}^{D}\lambda_i$예요([버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded)).

#### 첫 단계

$$
J_{784}^\star=\sum_{i=785}^{784}\lambda_i=0,\qquad J_{500}^\star=\sum_{i=501}^{784}\lambda_i
$$

(a)는 그림의 각 열을 위에서 아래로 읽고, (b)·(c)는 두 합식과 직교행렬 항등식으로 이어가요.

#### 핵심 풀이

#### (a) 주성분 개수에 따른 복원 변화

각 열이 같은 테스트 이미지 한 장의 복원이에요. 행을 내려갈수록 흐릿한 8에서 개별 필체의 윤곽과 획이 살아나요.

| $M$ | 복원 상태 | 보존된 특징 |
|---|---|---|
| $1$ | 흐릿하고 서로 비슷한 8 | 전체적인 8의 윤곽만 남음 |
| $10$ | 배경 얼룩은 남지만 윤곽 분리 | 개별 이미지의 기울기와 큰 형태 |
| $100$ | 숫자 형상이 또렷함 | 각 필체의 획과 고리 모양 |
| $500$ | 맨 위 원본과 거의 같음 | 세부 획과 명암까지 살아남 |

#### (b) $M=784$일 때의 $J_{784}^\star$와 완전 복원

$M=784=D$이면 $\mathbf B$는 $784\times 784$ 정사각 정규직교행렬이므로 $\mathbf B^{-1}=\mathbf B^\top$, 곧 $\mathbf B\mathbf B^\top=\mathbf I_{784}$예요. 따라서 임의의 이미지 $\mathbf x$가 정확히 복원돼요.

$$
\tilde{\mathbf x}=\bar{\mathbf x}+\mathbf B\mathbf B^\top(\mathbf x-\bar{\mathbf x})=\bar{\mathbf x}+\mathbf I_{784}(\mathbf x-\bar{\mathbf x})=\mathbf x
$$

버린 방향이 없어 $J_{784}^\star=\sum_{i=785}^{784}\lambda_i$는 더할 항이 없는 빈 합(empty sum)이므로 $J_{784}^\star=0$이에요.

#### (c) 500개로 거의 완벽히 복원되는 이유

$\lambda_i\ge 0$이므로 $M$이 늘면 $J_M^\star$는 단조 감소해요($J_{500}^\star\le J_{450}^\star$). 문제의 오차 곡선 조건에서 약 400개 이후 학습 오차가 거의 0이므로 $J_{500}^\star=\sum_{i=501}^{784}\lambda_i\approx 0$이에요.

특히 늘 검정인 가장자리 픽셀은 평균 $\bar{\mathbf x}$를 빼면 모든 학습 이미지에서 0이라 분산이 0이고, 유효 차원이 784보다 훨씬 작아요. 그림 10.12의 테스트 이미지 4장도 같은 분포를 공유하며 버린 방향 성분이 아주 작아 500개 행이 원본과 거의 같아요.

#### 최종 답

(a) 주성분이 $1\to 10\to 100\to 500$으로 늘수록 흐릿하고 비슷한 모양에서 기울기·획·세부가 살아나 500개에서는 원본과 거의 같아져요.

(b) $J_{784}^\star=0$이며, $\mathbf B\mathbf B^\top=\mathbf I_{784}$이므로 임의의 이미지가 $\tilde{\mathbf x}=\mathbf x$로 수학적으로 정확히 복원돼요.

(c) 400개 이후 버린 고윳값 합 $J_{500}^\star$가 거의 0이고(가장자리 픽셀 등 0 분산 좌표 포함) 그림의 테스트 이미지들도 버린 방향 성분이 작아 500개만으로 거의 완벽히 복원돼요.

#### 답 확인

#### (a) 검산

넷째 열(오른쪽으로 기운 8)을 위에서 아래로 보면 $M=1$은 흐릿하고, $M=10, 100$에서 기울어진 두 고리가 또렷해지며, $M=500$은 맨 위 원본과 거의 구분되지 않아요.

#### (b) 검산

$\tilde{\mathbf x}-\mathbf x=(\mathbf B\mathbf B^\top-\mathbf I_{784})(\mathbf x-\bar{\mathbf x})$에 $\mathbf B\mathbf B^\top=\mathbf I_{784}$를 넣으면 임의의 $\mathbf x$에서 차가 $\mathbf 0$이에요.

#### (c) 검산

$0\le J_{550}^\star\le J_{500}^\star\le J_{450}^\star$이고, 450개는 조건에서 학습 오차가 거의 0이라 한 구간에 있어요. 테스트 4장의 실제 복원은 그림 10.12의 $M=500$ 행과 원본 행 비교로 확인해요.

#### 주의할 점

(b)의 완전 복원은 $J_{784}^\star=0$(학습 평균)만으로는 부족하고 $\mathbf B\mathbf B^\top=\mathbf I_{784}$로 보여야 임의의 테스트 이미지까지 성립해요. 또 500개 복원(시각적 근사)과 784개 복원(수학적 일치), 학습 평균 오차 $J_M^\star$와 개별 테스트 오차를 구별해요.

**페이지 요약**

#### 떠올릴 개념·공식

복원은 $\tilde{\mathbf x}=\bar{\mathbf x}+\mathbf B\mathbf B^\top(\mathbf x-\bar{\mathbf x})$, 학습 평균 제곱 복원오차는 $J_M^\star=\sum_{i=M+1}^{D}\lambda_i$예요.

#### 첫 줄

$J_{784}^\star=\sum_{i=785}^{784}\lambda_i=0$과 $J_{500}^\star=\sum_{i=501}^{784}\lambda_i$를 적어요.

#### 핵심 답

(a) $M$이 늘수록 흐릿한 8에서 필체와 세부가 선명해져 500개에서 원본과 거의 같아요. (b) $J_{784}^\star=0$이고 $\mathbf B\mathbf B^\top=\mathbf I_{784}$로 $\tilde{\mathbf x}=\mathbf x$예요. (c) 400개 이후 $J_{500}^\star\approx 0$이고 그림의 테스트 4장도 버린 성분이 작아 거의 완벽히 복원돼요.

#### 검산

$\tilde{\mathbf x}-\mathbf x=(\mathbf B\mathbf B^\top-\mathbf I_{784})(\mathbf x-\bar{\mathbf x})=\mathbf 0$이고, $0\le J_{550}^\star\le J_{500}^\star\le J_{450}^\star$예요.

#### 조건·구분

완전 복원(784)과 근사(500), 학습 평균 오차와 테스트 사례 관찰을 구별해요.

#### 출제 근거

MML Example 10.4와 그림 10.12, 교과서 338–339쪽(PDF 344–345쪽). 그림 10.13과 식 (10.62)의 설명은 조건에 문장으로 주어졌어요.

수업: 1104 L06 s8–11(버린 방향의 복원오차, MNIST 사영과 복원).

관련 정리노트: [버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded), [MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)

#### 용어

- **복원(reconstruction)** — 중심화 벡터의 저차원 좌표 $\mathbf z=\mathbf B^\top(\mathbf x-\bar{\mathbf x})$에서 $\tilde{\mathbf x}=\bar{\mathbf x}+\mathbf B\mathbf z$로 원래 차원 벡터를 되살리는 과정이에요.
- **평균제곱 복원오차(average squared reconstruction error)** — 학습 데이터에서 원본과 복원의 제곱 거리 평균이며 최솟값은 $J_M^\star=\sum_{i=M+1}^{D}\lambda_i$예요.
- **정규직교기저(orthonormal basis)** — 길이가 1이고 서로 직교하는 기저예요. $D$개 모두 모은 정사각행렬은 $\mathbf B\mathbf B^\top=\mathbf I$를 만족해요.
- **빈 합(empty sum)** — 시작 인덱스가 끝 인덱스보다 커서 더할 항이 없는 합으로 값은 0이에요.

---

<a id="p4"></a>

### P4. 가로로 긴 행렬의 특잇값 분해

MML Example 4.13 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=4)

#### 주어진 조건

다음 행렬의 특잇값 분해 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$를 세 단계로 구해요.

$$
\mathbf A=\begin{bmatrix}1&1&0\\0&1&1\end{bmatrix}
$$

#### 구할 것

- (a) $\mathbf A^\top\mathbf A$를 구하고, 그 고윳값과 정규화된 고유벡터로 오른쪽 특이벡터 행렬 $\mathbf V$를 만들어 보세요.
- (b) (a)의 고윳값으로 특잇값과 특잇값 행렬 $\mathbf\Sigma$를 구해 보세요.
- (c) ${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$로 왼쪽 특이벡터 행렬 $\mathbf U$를 구해 보세요.
- (d) $\mathbf U,\mathbf\Sigma,\mathbf V$의 크기를 읽어 보세요.

<details><summary>원문 보기</summary>

“Right-singular vectors as the eigenbasis of A⊤A.” … “Left-singular vectors as the normalized image of the right-singular vectors.” — Example 4.13

</details>

#### 풀이 목표

$2\times 3$ 행렬 $\mathbf A$의 SVD $\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top$를 (a) $\mathbf A^\top\mathbf A$에서 $\mathbf V$, (b) $\mathbf\Sigma$, (c) $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 $\mathbf U$, (d) 세 행렬의 크기 순으로 구해요.

#### 풀이 단서

$\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top$($\mathbf U^\top\mathbf U=\mathbf I_2$)를 $\mathbf A^\top\mathbf A$에 넣으면 $\mathbf A^\top\mathbf A=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top$이므로 $\mathbf V$의 열은 $\mathbf A^\top\mathbf A$의 단위 고유벡터, 대각값 $\sigma_1^2,\sigma_2^2,0$이 고윳값이에요([데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)).

또 $\mathbf A\mathbf V=\mathbf U\mathbf\Sigma$의 양의 특잇값($\sigma_i>0$) 열에서 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 $\mathbf U$의 열을 구해요.

#### 첫 단계

$$
\mathbf A^\top\mathbf A=\begin{bmatrix}1&1&0\\1&2&1\\0&1&1\end{bmatrix},\qquad\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)=0
$$

특성방정식으로 고윳값과 단위 고유벡터를 먼저 구한 뒤 $\mathbf\Sigma$와 $\mathbf U$를 차례로 만들어요.

#### 핵심 풀이

#### (a) $\mathbf A^\top\mathbf A$의 고윳값과 $\mathbf V$

$$
\begin{aligned}\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)&=(1-\lambda)\big[(2-\lambda)(1-\lambda)-1\big]\\&\quad-(1-\lambda)\end{aligned}
$$

↳ 첫째 행으로 여인수 전개해요

$$
=(1-\lambda)(\lambda^2-3\lambda)
$$

↳ $(1-\lambda)$로 묶고 안쪽을 전개해요

$$
=-\lambda(\lambda-1)(\lambda-3)=0
$$

↳ 큰 순서로 고윳값 $3,1,0$을 얻어요

고유벡터 후보 $(x,y,z)^\top$에 $(\mathbf A^\top\mathbf A-\lambda\mathbf I)(x,y,z)^\top=\mathbf 0$을 풀고 길이로 나눠요.

$\lambda_1=3$: $-2x+y=0$, $y-2z=0$에서 $(1,2,1)^\top$, $\lambda_2=1$: $y=0$, $x+y+z=0$에서 $(1,0,-1)^\top$, $\lambda_3=0$: $x+y=0$, $y+z=0$에서 $(1,-1,1)^\top$이에요.

$$
\mathbf v_1=\frac{1}{\sqrt6}\begin{bmatrix}1\\2\\1\end{bmatrix},\quad\mathbf v_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\0\\-1\end{bmatrix},\quad\mathbf v_3=\frac{1}{\sqrt3}\begin{bmatrix}1\\-1\\1\end{bmatrix},\quad\mathbf V=\begin{bmatrix}\frac{1}{\sqrt6}&\frac{1}{\sqrt2}&\frac{1}{\sqrt3}\\\frac{2}{\sqrt6}&0&-\frac{1}{\sqrt3}\\\frac{1}{\sqrt6}&-\frac{1}{\sqrt2}&\frac{1}{\sqrt3}\end{bmatrix}
$$

#### (b) 특잇값과 행렬 $\mathbf\Sigma$

양의 고윳값의 제곱근이 특잇값 $\sigma_1=\sqrt3$, $\sigma_2=1$이고, $\mathbf\Sigma$는 $\mathbf A$와 같은 $2\times 3$ 크기예요.

$$
\mathbf\Sigma=\begin{bmatrix}\sqrt3&0&0\\0&1&0\end{bmatrix}
$$

#### (c) 왼쪽 특이벡터 행렬 $\mathbf U$

$$
\begin{aligned}\mathbf A\mathbf v_1&=\frac{1}{\sqrt6}\begin{bmatrix}3\\3\end{bmatrix},\\\mathbf u_1&=\frac{\mathbf A\mathbf v_1}{\sqrt3}=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}\end{aligned}
$$

↳ $\mathbf A\mathbf v_1$을 $\sigma_1=\sqrt3$으로 나눠요

$$
\begin{aligned}\mathbf A\mathbf v_2&=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix},\\\mathbf u_2&=\frac{\mathbf A\mathbf v_2}{1}=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}\end{aligned}
$$

↳ $\mathbf A\mathbf v_2$를 $\sigma_2=1$로 나눠요

두 열을 모으면 $\mathbf U=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}$이에요($\mathbf u_1^\top\mathbf u_2=0$).

#### (d) 세 행렬의 크기

$\mathbf A$가 $2\times 3$이므로 $\mathbf U$는 $2\times 2$, $\mathbf\Sigma$는 $2\times 3$, $\mathbf V$는 $3\times 3$이에요($(2\times 2)(2\times 3)(3\times 3)=2\times 3$).

#### 최종 답

(a) 고윳값은 $3,1,0$이고 $\mathbf V=\begin{bmatrix}\frac{1}{\sqrt6}&\frac{1}{\sqrt2}&\frac{1}{\sqrt3}\\\frac{2}{\sqrt6}&0&-\frac{1}{\sqrt3}\\\frac{1}{\sqrt6}&-\frac{1}{\sqrt2}&\frac{1}{\sqrt3}\end{bmatrix}$이에요.

(b) $\sigma_1=\sqrt3$, $\sigma_2=1$이고 $\mathbf\Sigma=\begin{bmatrix}\sqrt3&0&0\\0&1&0\end{bmatrix}$이에요.

(c) $\mathbf U=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}$이에요.

(d) $\mathbf U\in\mathbb R^{2\times 2}$, $\mathbf\Sigma\in\mathbb R^{2\times 3}$, $\mathbf V\in\mathbb R^{3\times 3}$이에요.

#### 답 확인

#### (a) 검산

$\mathbf A^\top\mathbf A(1,2,1)^\top=(3,6,3)^\top$, $\mathbf A^\top\mathbf A(1,0,-1)^\top=(1,0,-1)^\top$, $\mathbf A^\top\mathbf A(1,-1,1)^\top=(0,0,0)^\top$이고 세 벡터의 쌍별 내적은 모두 $0$이에요.

#### (b) 검산

$\mathbf A\mathbf A^\top=\begin{bmatrix}2&1\\1&2\end{bmatrix}$의 고윳값도 $3,1$이고 $\|\mathbf A\mathbf v_1\|_2=\sqrt3=\sigma_1$이에요.

#### (c) 검산

$\sigma_1\mathbf u_1\mathbf v_1^\top+\sigma_2\mathbf u_2\mathbf v_2^\top=\frac12\begin{bmatrix}1&2&1\\1&2&1\end{bmatrix}+\frac12\begin{bmatrix}1&0&-1\\-1&0&1\end{bmatrix}=\begin{bmatrix}1&1&0\\0&1&1\end{bmatrix}=\mathbf A$예요.

#### (d) 검산

$\mathbf U^\top\mathbf U=\mathbf I_2$, $\mathbf V^\top\mathbf V=\mathbf I_3$이고 $\mathbf A\mathbf v_3=\mathbf 0$이라 $\mathbf\Sigma$의 셋째 0열과 맞아요.

#### 주의할 점

$\mathbf u_i$와 $\mathbf v_i$를 따로 구하면 부호가 어긋날 수 있으니 $\sigma_i>0$ 열에는 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 짝을 맞춰요. 특잇값은 고윳값이 아니라 제곱근($\sqrt3$, $1$)이고, $\mathbf\Sigma$는 $\mathbf A$와 같은 $2\times 3$이라 0열을 빠뜨리지 않아요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mathbf A^\top\mathbf A=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top$이고 $\sigma_i>0$일 때 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$예요.

#### 첫 줄

$\mathbf A^\top\mathbf A=\begin{bmatrix}1&1&0\\1&2&1\\0&1&1\end{bmatrix}$과 $\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)=0$으로 시작해요.

#### 핵심 답

(a) 고윳값 $3,1,0$, $\mathbf v_1=\frac{1}{\sqrt6}(1,2,1)^\top$, $\mathbf v_2=\frac{1}{\sqrt2}(1,0,-1)^\top$, $\mathbf v_3=\frac{1}{\sqrt3}(1,-1,1)^\top$. (b) $\sigma_1=\sqrt3,\sigma_2=1$, $\mathbf\Sigma=\begin{bmatrix}\sqrt3&0&0\\0&1&0\end{bmatrix}$. (c) $\mathbf U=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}$. (d) $2\times2$, $2\times3$, $3\times3$이에요.

#### 검산

$\sigma_1\mathbf u_1\mathbf v_1^\top+\sigma_2\mathbf u_2\mathbf v_2^\top=\mathbf A$이고 두 군 모두 정규직교예요.

#### 조건·구분

$\sigma_i=\sqrt{\lambda_i}$($\lambda_i>0$), $\mathbf u_i$ 부호는 $\mathbf v_i$에 연동하고 $\mathbf\Sigma$의 0열을 보존해요.

#### 출제 근거

MML Example 4.13(수치를 바꾼 변형), 교과서 125–126쪽(PDF 131–132쪽).

수업: 1104 L06 s13(데이터 행렬의 SVD), 1102 특성다항식·스펙트럼 정리.

관련 정리노트: [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

#### 용어

- **특잇값 분해(singular value decomposition, SVD)** — 임의의 $m\times n$ 행렬을 $\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top$로 분해하는 식이에요.
- **특잇값(singular value)** — 양의 특잇값은 $\mathbf A^\top\mathbf A$와 $\mathbf A\mathbf A^\top$의 양의 고윳값의 제곱근이에요.
- **오른쪽 특이벡터(right-singular vector)** — $\mathbf A^\top\mathbf A$의 단위 고유벡터들로 $\mathbf V$의 열을 이뤄요.
- **왼쪽 특이벡터(left-singular vector)** — 양의 특잇값에 대응하는 $\mathbf U$의 열은 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 구해요.

---

<a id="p5"></a>

### P5. 영화 평점 행렬의 랭크 2 근사

MML Example 4.15 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=5)

#### 주어진 조건

관객 세 명이 영화 네 편에 0점(최악)부터 5점(최고)까지 준 평점을 행렬 $\mathbf A\in\mathbb R^{4\times3}$에 담았어요. 행은 영화, 열은 관객이에요.

$\mathbf A$의 특잇값은 $\sigma_1=9.6438$, $\sigma_2=6.3639$, $\sigma_3=0.7056$이고, 앞의 두 왼쪽·오른쪽 특이벡터는 다음과 같아요(소수 넷째 자리).

앞의 두 층을 더한 랭크 2 근사는 다음과 같아요.

$$
\hat{\mathbf A}(2)=\sigma_1\mathbf u_1\mathbf v_1^\top+\sigma_2\mathbf u_2\mathbf v_2^\top
$$

#### 구할 것

- (a) 첫째 층 $\sigma_1\mathbf u_1\mathbf v_1^\top$의 Chandra 열(네 값)을 구해 보세요.
- (b) $\hat{\mathbf A}(2)$의 Chandra 열을 구해 $\mathbf A$의 Chandra 열 $(1,0,5,4)^\top$와 비교해 보세요.
- (c) 셋째 층 $\sigma_3\mathbf u_3\mathbf v_3^\top$를 버려도 되는지 수치로 근거를 들어 판정해 보세요.

| 영화＼관객 | Ali | Beatrix | Chandra |
|---|---|---|---|
| Star Wars | 5 | 4 | 1 |
| Blade Runner | 5 | 5 | 0 |
| Amelie | 0 | 0 | 5 |
| Delicatessen | 1 | 0 | 4 |

| 영화 | $\mathbf u_1$ | $\mathbf u_2$ |
|---|---|---|
| Star Wars | −0.6710 | 0.0236 |
| Blade Runner | −0.7197 | 0.2054 |
| Amelie | −0.0939 | −0.7705 |
| Delicatessen | −0.1515 | −0.6030 |

| 관객 | $\mathbf v_1$ | $\mathbf v_2$ |
|---|---|---|
| Ali | −0.7367 | 0.0852 |
| Beatrix | −0.6515 | 0.1762 |
| Chandra | −0.1811 | −0.9807 |

<details><summary>원문 보기</summary>

“this suggests that we can ignore the contribution of A3” — Example 4.15

</details>

#### 풀이 목표

$4\times 3$ 영화 평점 행렬 $\mathbf A$의 SVD에서 (a) 첫째 층의 Chandra 열, (b) 랭크 2 근사 $\hat{\mathbf A}(2)$의 Chandra 열과 실제 평점 $(1,0,5,4)^\top$ 비교, (c) 셋째 층을 버려도 되는지 제곱오차 비율로 판정해요.

#### 풀이 단서

외적 $\mathbf u_i\mathbf v_i^\top$의 $j$번째 열은 $\mathbf v_i$의 $j$번째 성분을 곱한 $v_{i,j}\mathbf u_i$예요. Chandra는 셋째 열($j=3$)이므로 $i$번째 층 $\sigma_i\mathbf u_i\mathbf v_i^\top$의 Chandra 열은 $\sigma_i v_{i,3}\mathbf u_i$예요.

버린 셋째 층의 Frobenius 제곱오차는 $\|\mathbf A-\hat{\mathbf A}(2)\|_F^2=\sigma_3^2$이므로, 원 행렬의 전체 제곱합 $\|\mathbf A\|_F^2$과 비교해 버릴 만한지 판정해요([작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)).

#### 첫 단계

$$
\sigma_1 v_{1,3}=9.6438\times(-0.1811)\approx -1.7465
$$

계산한 계수를 $\mathbf u_1$의 네 성분에 곱해 첫째 층 Chandra 열을 구한 뒤, 둘째 층을 더해 비교해요.

#### 핵심 풀이

#### (a) 첫째 층의 Chandra 열

대표 1항 대입: Star Wars는 $(-1.74649)\times(-0.6710)\approx 1.1719$예요.

| 영화 | $u_{1,k}$ | 첫째 층 ($\sigma_1 v_{1,3}u_{1,k}$) | 실제 |
|---|---|---|---|
| Star Wars | $-0.6710$ | $1.1719$ | $1$ |
| Blade Runner | $-0.7197$ | $1.2570$ | $0$ |
| Amelie | $-0.0939$ | $0.1640$ | $5$ |
| Delicatessen | $-0.1515$ | $0.2646$ | $4$ |

첫째 층만으로는 앞의 SF 두 편 쪽만 $1$ 근처이고 Amelie·Delicatessen(5, 4)은 거의 못 잡아요.

#### (b) $\hat{\mathbf A}(2)$의 Chandra 열과 비교

둘째 층 계수는 $\sigma_2 v_{2,3}=6.3639\times(-0.9807)\approx -6.2411$이에요. 대표 1항으로 Blade Runner는 $1.25695+(-1.28192)\approx -0.0250$이에요.

| 영화 | 첫째 층 | 둘째 층 ($\sigma_2 v_{2,3}u_{2,k}$) | $\hat{\mathbf A}(2)$ | 실제 | 차이 |
|---|---|---|---|---|---|
| Star Wars | $1.1719$ | $-0.1473$ | $1.0246$ | $1$ | $+0.0246$ |
| Blade Runner | $1.2570$ | $-1.2819$ | $-0.0250$ | $0$ | $-0.0250$ |
| Amelie | $0.1640$ | $4.8087$ | $4.9727$ | $5$ | $-0.0273$ |
| Delicatessen | $0.2646$ | $3.7634$ | $4.0280$ | $4$ | $+0.0280$ |

모든 영화에서 실제 평점 $(1,0,5,4)^\top$과의 차이가 $0.03$ 이하로 거의 일치해요.

#### (c) 셋째 층 생략 판정

버린 제곱오차는 $\|\mathbf A-\hat{\mathbf A}(2)\|_F^2=\sigma_3^2=0.7056^2\approx 0.4979$이고, 원 행렬의 원소 제곱합은 행마다 $42+50+25+17=134$예요.

$$
\frac{\sigma_3^2}{\|\mathbf A\|_F^2}=\frac{0.4979}{134}\approx 0.003716\approx 0.37\%
$$

전체 제곱노름의 약 $0.37\%$만 남고 $99.63\%$가 앞 두 층에 담기므로 근사 목적에서는 셋째 층을 버려도 돼요.

#### 최종 답

(a) 첫째 층 Chandra 열은 $(1.1719,\ 1.2570,\ 0.1640,\ 0.2646)^\top$이에요.

(b) $\hat{\mathbf A}(2)$의 Chandra 열은 $(1.0246,\ -0.0250,\ 4.9727,\ 4.0280)^\top$으로 실제 평점 $(1,0,5,4)^\top$과 모든 성분이 $0.03$ 이내로 거의 같아요.

(c) $\sigma_3^2\approx 0.4979$는 전체 제곱합 $134$의 약 $0.37\%$뿐이므로 셋째 층을 버려도 돼요.

#### 답 확인

#### (a) 검산

교과서 식 (4.100b)의 $\mathbf u_1\mathbf v_1^\top$ 셋째 열 $(0.1215, 0.1303, 0.0170, 0.0274)^\top$에 $\sigma_1=9.6438$을 곱한 값과 표시 넷째 자리 반올림 범위에서 맞아요.

#### (b) 검산

교과서 식 (4.102)의 $(1.0244,-0.0250,4.9724,4.0278)^\top$과 표의 넷째 자리 반올림 차이 $0.0003$ 이내로 일치해요.

#### (c) 검산

$\sigma_1^2+\sigma_2^2+\sigma_3^2\approx 93.003+40.499+0.498=134.000$으로 전체 원소 제곱합 $134$와 맞아요.

#### 주의할 점

$i$번째 층의 $j$번째 열은 $\sigma_i v_{i,j}\mathbf u_i$예요. 행과 열($u_{i,k}\mathbf v_i^\top$)을 바꾸거나 교과서 표기 $\mathbf A_i=\mathbf u_i\mathbf v_i^\top$처럼 $\sigma_i$를 빼뜨리면 값이 달라져요. 비율을 낼 때는 $\sigma_3$가 아니라 $\sigma_3^2$을 $134$로 나눠요.

**페이지 요약**

#### 떠올릴 개념·공식

$i$번째 층 $\sigma_i\mathbf u_i\mathbf v_i^\top$의 $j$번째 열은 $\sigma_i v_{i,j}\mathbf u_i$이고, 오차는 $\|\mathbf A-\hat{\mathbf A}(2)\|_F^2=\sigma_3^2$예요.

#### 첫 줄

$\sigma_1 v_{1,3}=9.6438\times(-0.1811)\approx -1.7465$를 구해요.

#### 핵심 답

(a) $(1.1719,1.2570,0.1640,0.2646)^\top$. (b) $(1.0246,-0.0250,4.9727,4.0280)^\top$으로 $(1,0,5,4)^\top$과 거의 같음. (c) $\sigma_3^2/134\approx 0.37\%$라 버려도 돼요.

#### 검산

교과서 (4.100b)·(4.102)와 반올림 범위 내 일치하고 $\sum\sigma_i^2\approx 134.000$이에요.

#### 조건·구분

열 추출에 $\sigma_i$와 $\mathbf v_i$의 성분을 곱하고, 오차 비율은 제곱노름 $\sigma_3^2$과 $134$로 계산해요.

#### 출제 근거

MML Example 4.15(그림 4.10, Example 4.14의 평점표와 SVD), 교과서 127쪽·132–133쪽(PDF 133쪽·138–139쪽), 식 (4.100)–(4.103).

수업: 1104 L06 s14(랭크 제한 복원과 Frobenius 오차).

관련 정리노트: [작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)

#### 용어

- **외적(outer product)** — 열벡터와 행벡터의 곱 $\mathbf u\mathbf v^\top$으로 $(k,j)$ 원소가 $u_k v_j$인 행렬이에요.
- **랭크 2 근사(rank-2 approximation)** — 상위 두 외적 층을 더한 행렬 $\hat{\mathbf A}(2)=\sigma_1\mathbf u_1\mathbf v_1^\top+\sigma_2\mathbf u_2\mathbf v_2^\top$이에요.
- **Frobenius 노름(Frobenius norm)** — 행렬 원소 제곱합의 제곱근 $\|\mathbf M\|_F=\sqrt{\sum_{k,j}M_{kj}^2}$예요.

---

<a id="p6"></a>

### P6. 사영을 뺀 나머지도 사영일까

MML Exercise 3.7 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=6)

#### 주어진 조건

$V$는 벡터공간이고 $\pi:V\to V$는 선형사상이에요. $\mathrm{id}_V$는 $V$의 항등사상이에요. 선형사상 $\rho:V\to V$가 $\rho\circ\rho=\rho$를 만족하면 $\rho$를 사영이라고 해요. $\rho^2$은 $\rho\circ\rho$를 뜻해요.

#### 구할 것

- (a) $\pi$가 사영이면 $\mathrm{id}_V-\pi$도 사영임을 증명해 보세요.
- (b) 반대로 $\mathrm{id}_V-\pi$가 사영이면 $\pi$도 사영임을, (a)를 $\rho=\mathrm{id}_V-\pi$에 적용해 증명해 보세요.

<details><summary>원문 보기</summary>

“Prove that π is a projection if and only if idV − π is a projection” — Exercise 3.7

</details>

#### 풀이 목표

벡터공간 $V$의 선형사상 $\pi:V\to V$에 대해 (a) $\pi$가 사영($\pi\circ\pi=\pi$)이면 $\mathrm{id}_V-\pi$도 사영임을 증명하고, (b) 그 역도 (a)를 $\rho=\mathrm{id}_V-\pi$에 적용해 증명해요.

#### 풀이 단서

사영의 정의 $\rho^2=\rho$를 보이려면 임의의 $\mathbf x\in V$에 두 번 적용한 결과가 한 번 적용한 결과와 같아야 해요. 두 선형사상의 차 $\mathrm{id}_V-\pi$도 선형이며, 선형사상 $\pi$는 $\pi(\mathbf a-\mathbf b)=\pi(\mathbf a)-\pi(\mathbf b)$로 전개돼요([기저를 고정하고 좌표 구하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-projection)).

#### 첫 단계

$I=\mathrm{id}_V$라 두고 임의의 $\mathbf x\in V$에 $(I-\pi)$를 두 번 적용한 식을 전개해요.

$$
(I-\pi)\big((I-\pi)(\mathbf x)\big)=(I-\pi)\big(\mathbf x-\pi(\mathbf x)\big)
$$

#### 핵심 풀이

#### (a) $\pi$가 사영 $\implies \mathrm{id}_V-\pi$도 사영

$$
(I-\pi)^2(\mathbf x)=(I-\pi)\big(\mathbf x-\pi(\mathbf x)\big)
$$

↳ 안쪽 사상 $I-\pi$를 적용해요

$$
=\big(\mathbf x-\pi(\mathbf x)\big)-\pi\big(\mathbf x-\pi(\mathbf x)\big)
$$

↳ 바깥쪽 사상 $I-\pi$를 적용해요

$$
=\mathbf x-\pi(\mathbf x)-\pi(\mathbf x)+\pi(\pi(\mathbf x))
$$

↳ $\pi$의 선형성으로 전개해요

$$
=\mathbf x-2\pi(\mathbf x)+\pi(\mathbf x)
$$

↳ 가정 $\pi\circ\pi=\pi$를 대입해요

$$
=\mathbf x-\pi(\mathbf x)=(I-\pi)(\mathbf x)
$$

↳ 동류항을 정리해요

모든 $\mathbf x\in V$에서 $(I-\pi)^2(\mathbf x)=(I-\pi)(\mathbf x)$이므로 $\mathrm{id}_V-\pi$는 사영이에요.

#### (b) $\mathrm{id}_V-\pi$가 사영 $\implies \pi$도 사영

$\rho=\mathrm{id}_V-\pi$라 두면 두 선형사상의 차이므로 $\rho:V\to V$는 선형사상이고, (b)의 가정에 따라 사영이에요.

(a)는 임의의 사영에 성립하므로 (a)를 이 사상 $\rho$에 그대로 적용하면 $\mathrm{id}_V-\rho$도 사영이에요. 그런데 $\mathrm{id}_V-\rho=\mathrm{id}_V-(\mathrm{id}_V-\pi)=\pi$이므로 $\pi$는 사영이에요.

#### 최종 답

(a) 모든 $\mathbf x\in V$에서 $(\mathrm{id}_V-\pi)^2(\mathbf x)=\mathbf x-2\pi(\mathbf x)+\pi(\pi(\mathbf x))=(\mathrm{id}_V-\pi)(\mathbf x)$이므로 $\mathrm{id}_V-\pi$는 사영이에요.

(b) 선형사상 $\rho=\mathrm{id}_V-\pi$에 (a)를 적용하면 $\mathrm{id}_V-\rho=\pi$도 사영이에요.

#### 답 확인

#### (a) 검산

전개에는 $\pi$의 선형성만, 정리에는 $\pi^2=\pi$만 썼고 좌표·기저 가정 없이 임의의 $\mathbf x\in V$에서 성립해요.

#### (b) 검산

(a)의 일반 명제(사영 $T\implies \mathrm{id}_V-T$도 사영)에 $T=\rho$를 대입한 것이라 순환 논리가 아니에요.

#### 주의할 점

$(I-\pi)^2$을 $I^2-\pi^2$로 잘못 풀지 않아요. 교차항 $-2\pi$가 나와야 $\pi^2=\pi$와 합쳐져 $I-\pi$가 돼요. 또 (a)만으로는 한쪽 방향만 보이므로 (b)에서 치환을 꼭 거쳐야 해요.

**페이지 요약**

#### 떠올릴 개념·공식

사영은 $\rho\circ\rho=\rho$를 만족하는 선형사상이에요. 선형성으로 합성 괄호를 전개해요.

#### 첫 줄

$(I-\pi)\big((I-\pi)(\mathbf x)\big)=(I-\pi)\big(\mathbf x-\pi(\mathbf x)\big)$를 적어요.

#### 핵심 답

(a) 선형성과 $\pi^2=\pi$로 $(\mathrm{id}_V-\pi)^2=\mathrm{id}_V-\pi$. (b) $\rho=\mathrm{id}_V-\pi$에 (a)를 적용해 $\mathrm{id}_V-\rho=\pi$도 사영이에요.

#### 검산

기저 없이 선형성·멱등성만 썼고, (b)는 (a)에 새 사영 $\rho$를 대입한 것이에요.

#### 조건·구분

교차항 $-2\pi$를 빼먹지 않고, 양방향을 분리해 보여요.

#### 출제 근거

MML Exercise 3.7, 교과서 97쪽(PDF 103쪽). 원문 (a)의 필요충분을 (a), (b) 두 방향으로 나눴어요.

수업: 1019 사영행렬 $\mathbf P^2=\mathbf P$, 1104 L06 s5–10(사영과 버린 부분).

관련 정리노트: [기저를 고정하고 좌표 구하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-projection), [버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded)

#### 용어

- **선형사상(linear map)** — 덧셈과 스칼라배를 보존하는 사상 $\pi(c\mathbf a+\mathbf b)=c\pi(\mathbf a)+\pi(\mathbf b)$예요.
- **항등사상(identity map)** — 모든 벡터를 자기 자신으로 보내는 사상 $\mathrm{id}_V(\mathbf x)=\mathbf x$예요.
- **사영(projection)** — $\rho\circ\rho=\rho$를 만족하는 선형사상이에요.

---

<a id="p7"></a>

### P7. 왼쪽 특이벡터부터 구하는 특잇값 분해

MML Exercise 4.8 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=7)

#### 주어진 조건

다음 행렬의 특잇값 분해 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$를 크기가 작은 $\mathbf A\mathbf A^\top$에서 시작해 구해요.

$$
\mathbf A=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}
$$

#### 구할 것

- (a) $2\times2$ 행렬 $\mathbf A\mathbf A^\top$의 고윳값과 정규화된 고유벡터로 $\sigma_1,\sigma_2$와 $\mathbf u_1,\mathbf u_2$를 구해 보세요.
- (b) ${\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i}$로 $\mathbf v_1,\mathbf v_2$를 구해 보세요.
- (c) $\mathbf v_1,\mathbf v_2$에 모두 수직인 단위벡터 $\mathbf v_3$를 구해 $\mathbf V$를 완성해 보세요.
- (d) $\mathbf A\mathbf v_3=\mathbf 0$인지 확인하고, 이것이 $\mathbf\Sigma$의 셋째 열이 0인 것과 맞는지 판정해 보세요.

<details><summary>원문 보기</summary>

“Find the SVD of the matrix” — Exercise 4.8

</details>

#### 풀이 목표

$2\times 3$ 행렬 $\mathbf A$의 SVD $\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top$를 작은 $2\times 2$ 행렬 $\mathbf A\mathbf A^\top$에서 시작해 (a) $\sigma_i,\mathbf u_i$, (b) $\mathbf v_1,\mathbf v_2$, (c) $\mathbf v_3$와 $\mathbf V$, (d) $\mathbf A\mathbf v_3=\mathbf 0$ 판정 순으로 구해요.

#### 풀이 단서

$\mathbf A\mathbf A^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top$($\mathbf V^\top\mathbf V=\mathbf I_3$)이므로 $\mathbf U$의 열 $\mathbf u_i$는 $\mathbf A\mathbf A^\top$의 단위 고유벡터, 대각값 $\sigma_1^2,\sigma_2^2$이 고윳값이에요([데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)).

$\mathbf A^\top\mathbf U=\mathbf V\mathbf\Sigma^\top$에서 $\sigma_i>0$ 열은 $\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i$로 구하고, 나머지 열 $\mathbf v_3$은 $\mathbf v_1,\mathbf v_2$에 모두 직교인 단위벡터로 채워요.

#### 첫 단계

$$
\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix},\qquad\det(\mathbf A\mathbf A^\top-\lambda\mathbf I)=0
$$

고윳값·고유벡터로 $\mathbf u_1,\mathbf u_2$를 먼저 구한 뒤 $\mathbf v_1,\mathbf v_2,\mathbf v_3$를 차례로 구해요.

#### 핵심 풀이

#### (a) $\sigma_1,\sigma_2$와 $\mathbf u_1,\mathbf u_2$

$$
(17-\lambda)^2-8^2=(9-\lambda)(25-\lambda)=0
$$

↳ 합차 공식으로 특성다항식을 풀어요

$$
\begin{aligned}\lambda_1&=25\implies\sigma_1=5,\\\lambda_2&=9\implies\sigma_2=3\end{aligned}
$$

↳ 양의 제곱근이 특잇값이에요

$(\mathbf A\mathbf A^\top-\lambda\mathbf I)(x,y)^\top=\mathbf 0$의 첫째 행에 $\lambda_1=25$를 넣으면 $-8x+8y=0$($y=x$), $\lambda_2=9$를 넣으면 $8x+8y=0$($y=-x$)이에요. 길이 $\sqrt2$로 나눠요.

$$
\mathbf u_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},\qquad\mathbf u_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}
$$

#### (b) 오른쪽 특이벡터 $\mathbf v_1,\mathbf v_2$

$$
\begin{aligned}\mathbf A^\top\mathbf u_1&=\frac{1}{\sqrt2}\begin{bmatrix}5\\5\\0\end{bmatrix},\\\mathbf v_1&=\frac{\mathbf A^\top\mathbf u_1}{5}=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\\0\end{bmatrix}\end{aligned}
$$

↳ $\mathbf A^\top\mathbf u_1$을 $\sigma_1=5$로 나눠요

$$
\begin{aligned}\mathbf A^\top\mathbf u_2&=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\\4\end{bmatrix},\\\mathbf v_2&=\frac{\mathbf A^\top\mathbf u_2}{3}=\frac{1}{3\sqrt2}\begin{bmatrix}1\\-1\\4\end{bmatrix}\end{aligned}
$$

↳ $\mathbf A^\top\mathbf u_2$를 $\sigma_2=3$으로 나눠요

#### (c) 셋째 열 $\mathbf v_3$과 행렬 $\mathbf V$

$\mathbf v_3\propto (a,b,c)^\top$가 $\mathbf v_1,\mathbf v_2$에 직교하려면 $a+b=0$, $a-b+4c=0$이에요. $b=-a$를 넣으면 $c=-a/2$이므로 $a=2$를 택해 $(2,-2,-1)^\top$을 길이 $\sqrt{4+4+1}=3$으로 나눠요.

$$
\mathbf v_3=\frac13\begin{bmatrix}2\\-2\\-1\end{bmatrix},\qquad\mathbf V=\begin{bmatrix}\frac{1}{\sqrt2}&\frac{1}{3\sqrt2}&\frac23\\\frac{1}{\sqrt2}&-\frac{1}{3\sqrt2}&-\frac23\\0&\frac{4}{3\sqrt2}&-\frac13\end{bmatrix}
$$

#### (d) $\mathbf A\mathbf v_3=\mathbf 0$과 $\mathbf\Sigma$의 셋째 열 판정

$$
\begin{aligned}\mathbf A\mathbf v_3&=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}\frac13\begin{bmatrix}2\\-2\\-1\end{bmatrix}\\&=\frac13\begin{bmatrix}6-4-2\\4-6+2\end{bmatrix}=\mathbf 0\end{aligned}
$$

↳ 행렬곱을 직접 계산해요

$\mathbf\Sigma=\begin{bmatrix}5&0&0\\0&3&0\end{bmatrix}$의 셋째 열이 $\mathbf 0$이므로 $\mathbf A\mathbf V=\mathbf U\mathbf\Sigma$의 셋째 열 $\mathbf A\mathbf v_3=\mathbf U\cdot\mathbf 0=\mathbf 0$과 정확히 맞아요.

#### 최종 답

(a) $\sigma_1=5,\ \sigma_2=3$, $\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top$, $\mathbf u_2=\frac{1}{\sqrt2}(1,-1)^\top$이에요.

(b) $\mathbf v_1=\frac{1}{\sqrt2}(1,1,0)^\top$, $\mathbf v_2=\frac{1}{3\sqrt2}(1,-1,4)^\top$이에요.

(c) $\mathbf v_3=\frac13(2,-2,-1)^\top$, $\mathbf V=[\mathbf v_1\ \mathbf v_2\ \mathbf v_3]$예요(반대 부호 $-\mathbf v_3$도 가능).

(d) $\mathbf A\mathbf v_3=\mathbf 0$이며, $\mathbf\Sigma$의 셋째 열이 0인 것과 정확히 일치해요.

#### 답 확인

#### (a) 검산

$\mathbf A\mathbf A^\top\mathbf u_1=25\mathbf u_1$, $\mathbf A\mathbf A^\top\mathbf u_2=9\mathbf u_2$이고 $\mathbf u_1^\top\mathbf u_2=0$이에요.

#### (b) 검산

$\mathbf A\mathbf v_1=5\mathbf u_1$, $\mathbf A\mathbf v_2=3\mathbf u_2$이고 $\mathbf v_1^\top\mathbf v_2=0$, $\|\mathbf v_2\|_2^2=(1+1+16)/18=1$이에요.

#### (c) 검산

$(1,1,0)\cdot(2,-2,-1)=0$, $(1,-1,4)\cdot(2,-2,-1)=0$이고 $\|(2,-2,-1)\|_2=3$이라 $\mathbf V$가 정규직교행렬이에요.

#### (d) 검산

$5\mathbf u_1\mathbf v_1^\top+3\mathbf u_2\mathbf v_2^\top=\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}+\frac12\begin{bmatrix}1&-1&4\\-1&1&-4\end{bmatrix}=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}=\mathbf A$예요.

#### 주의할 점

$\mathbf v_1,\mathbf v_2$는 $\mathbf A^\top\mathbf u_i/\sigma_i$로 $\mathbf u_i$와 부호 짝을 맞춰 구해야 해요. 또 양의 특잇값이 2개뿐이라 $\mathbf v_3$는 나눗셈이 아니라 직교 조건으로 구해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mathbf A\mathbf A^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top$이고 $\sigma_i>0$이면 $\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i$예요.

#### 첫 줄

$\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix}$의 특성방정식을 세워요.

#### 핵심 답

(a) $\sigma_1=5,\sigma_2=3$, $\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top$, $\mathbf u_2=\frac{1}{\sqrt2}(1,-1)^\top$. (b) $\mathbf v_1=\frac{1}{\sqrt2}(1,1,0)^\top$, $\mathbf v_2=\frac{1}{3\sqrt2}(1,-1,4)^\top$. (c) $\mathbf v_3=\frac13(2,-2,-1)^\top$. (d) $\mathbf A\mathbf v_3=\mathbf 0$으로 $\mathbf\Sigma$의 0열과 일치해요.

#### 검산

$5\mathbf u_1\mathbf v_1^\top+3\mathbf u_2\mathbf v_2^\top=\mathbf A$이고 $\mathbf V$가 정규직교행렬이에요.

#### 조건·구분

$\mathbf v_1,\mathbf v_2$는 $\mathbf u_i$와 부호를 맞추고, $\mathbf v_3$는 직교 조건으로 구해요.

#### 출제 근거

MML Exercise 4.8, 교과서 138쪽(PDF 144쪽). 원문은 SVD를 구하라는 한 문장이고 $\mathbf A\mathbf A^\top$부터 구하는 (a)–(d)로 나눴어요.

수업: 1104 L06 s13(데이터 행렬의 SVD), 1102 특성다항식.

관련 정리노트: [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

#### 용어

- **왼쪽 특이벡터(left-singular vector)** — $\mathbf A\mathbf A^\top$의 단위 고유벡터들로 $\mathbf U$의 열을 이뤄요.
- **오른쪽 특이벡터(right-singular vector)** — 양의 특잇값에 대응하는 열은 $\mathbf A^\top\mathbf u_i/\sigma_i$로 구하고, 나머지 열은 직교·단위 조건으로 채워요.
- **특잇값(singular value)** — 양의 특잇값은 $\mathbf A\mathbf A^\top$의 양의 고윳값의 제곱근이에요.
- **정규직교행렬(orthogonal matrix)** — 열들이 단위 길이를 갖고 서로 직교하는 정사각행렬이에요.

---

<a id="p8"></a>

### P8. 2×2 행렬의 특잇값 분해

MML Exercise 4.9 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=8)

#### 주어진 조건

다음 정사각행렬의 특잇값 분해 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$를 구해요.

$$
\mathbf A=\begin{bmatrix}2&2\\-1&1\end{bmatrix}
$$

#### 구할 것

- (a) $\mathbf A^\top\mathbf A$의 고윳값과 정규화된 고유벡터로 $\mathbf V$를 구해 보세요.
- (b) 특잇값을 구하고, ${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$로 $\mathbf U$를 구해 보세요.
- (c) $\mathbf A\mathbf A^\top$를 직접 계산해, (b)의 $\mathbf u_1,\mathbf u_2$가 그 고유벡터이고 고윳값이 $\sigma_i^2$인지 판정해 보세요.

<details><summary>원문 보기</summary>

“Find the singular value decomposition of” — Exercise 4.9

</details>

#### 풀이 목표

$2\times 2$ 행렬 $\mathbf A$의 SVD에서 (a) $\mathbf A^\top\mathbf A$로 $\mathbf V$, (b) 특잇값과 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 $\mathbf U$, (c) $\mathbf A\mathbf A^\top$을 직접 구해 $\mathbf u_i$가 고윳값 $\sigma_i^2$의 고유벡터인지 판정해요.

#### 풀이 단서

$\mathbf A^\top\mathbf A=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top$이므로 $\mathbf V$의 열이 $\mathbf A^\top\mathbf A$의 단위 고유벡터, 대각값이 $\sigma_i^2$예요. $\sigma_i>0$이면 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 부호를 맞춰 $\mathbf U$를 구하고, $\mathbf A\mathbf A^\top\mathbf u_i=\sigma_i^2\mathbf u_i$를 직접 확인해요([데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)).

#### 첫 단계

$$
\mathbf A^\top\mathbf A=\begin{bmatrix}5&3\\3&5\end{bmatrix},\qquad\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)=0
$$

$\mathbf A^\top\mathbf A$에서 $\mathbf V$와 특잇값을 구한 뒤 $\mathbf U$와 $\mathbf A\mathbf A^\top$을 순서대로 확인해요.

#### 핵심 풀이

#### (a) $\mathbf A^\top\mathbf A$의 고윳값과 $\mathbf V$

$$
(5-\lambda)^2-3^2=(2-\lambda)(8-\lambda)=0
$$

↳ 합차 공식으로 특성다항식을 풀어요

$$
\lambda_1=8,\qquad\lambda_2=2
$$

↳ 큰 순서로 고윳값을 정해요

$(\mathbf A^\top\mathbf A-\lambda\mathbf I)(x,y)^\top=\mathbf 0$의 첫째 행에 $\lambda_1=8$을 넣으면 $-3x+3y=0$($y=x$), $\lambda_2=2$를 넣으면 $3x+3y=0$($y=-x$)이에요. 길이 $\sqrt2$로 나눠요.

$$
\mathbf v_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},\qquad\mathbf v_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix},\qquad\mathbf V=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}
$$

#### (b) 특잇값과 $\mathbf U$

특잇값은 $\sigma_1=\sqrt8=2\sqrt2$, $\sigma_2=\sqrt2$이고 $\mathbf\Sigma=\begin{bmatrix}2\sqrt2&0\\0&\sqrt2\end{bmatrix}$예요.

$$
\begin{aligned}\mathbf A\mathbf v_1&=\frac{1}{\sqrt2}\begin{bmatrix}4\\0\end{bmatrix},\\\mathbf u_1&=\frac{\mathbf A\mathbf v_1}{2\sqrt2}=\begin{bmatrix}1\\0\end{bmatrix}\end{aligned}
$$

↳ $\mathbf A\mathbf v_1$을 $\sigma_1=2\sqrt2$로 나눠요

$$
\begin{aligned}\mathbf A\mathbf v_2&=\frac{1}{\sqrt2}\begin{bmatrix}0\\-2\end{bmatrix},\\\mathbf u_2&=\frac{\mathbf A\mathbf v_2}{\sqrt2}=\begin{bmatrix}0\\-1\end{bmatrix}\end{aligned}
$$

↳ $\mathbf A\mathbf v_2$를 $\sigma_2=\sqrt2$로 나눠요

두 열을 모으면 $\mathbf U=\begin{bmatrix}1&0\\0&-1\end{bmatrix}$이에요.

#### (c) $\mathbf A\mathbf A^\top$의 고유벡터·고윳값 판정

$\mathbf A$의 두 행 내적으로 $\mathbf A\mathbf A^\top=\begin{bmatrix}4+4&-2+2\\-2+2&1+1\end{bmatrix}=\begin{bmatrix}8&0\\0&2\end{bmatrix}$를 얻어요.

$$
\mathbf A\mathbf A^\top\mathbf u_1=\begin{bmatrix}8\\0\end{bmatrix}=8\mathbf u_1,\qquad\mathbf A\mathbf A^\top\mathbf u_2=\begin{bmatrix}0\\-2\end{bmatrix}=2\mathbf u_2
$$

고윳값 $8=\sigma_1^2$, $2=\sigma_2^2$이므로 (b)의 $\mathbf u_1,\mathbf u_2$는 $\mathbf A\mathbf A^\top$의 고유벡터이고 고윳값도 $\sigma_i^2$가 맞아요.

#### 최종 답

(a) 고윳값은 $8,2$이고 $\mathbf V=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}$이에요.

(b) $\sigma_1=2\sqrt2,\ \sigma_2=\sqrt2$이고 $\mathbf U=\begin{bmatrix}1&0\\0&-1\end{bmatrix}$이에요.

(c) $\mathbf A\mathbf A^\top=\operatorname{diag}(8,2)$이므로 $\mathbf u_1,\mathbf u_2$는 고윳값 $\sigma_1^2=8,\ \sigma_2^2=2$의 고유벡터가 맞아요.

#### 답 확인

#### (a) 검산

$\mathbf A^\top\mathbf A\mathbf v_1=8\mathbf v_1$, $\mathbf A^\top\mathbf A\mathbf v_2=2\mathbf v_2$이고 $\mathbf v_1^\top\mathbf v_2=0$이에요.

#### (b) 검산

$\mathbf U\mathbf\Sigma\mathbf V^\top=\begin{bmatrix}2\sqrt2&0\\0&-\sqrt2\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}=\begin{bmatrix}2&2\\-1&1\end{bmatrix}=\mathbf A$로 정확히 복원돼요.

#### (c) 검산

$\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top=\begin{bmatrix}1&0\\0&-1\end{bmatrix}\begin{bmatrix}8&0\\0&2\end{bmatrix}\begin{bmatrix}1&0\\0&-1\end{bmatrix}=\begin{bmatrix}8&0\\0&2\end{bmatrix}=\mathbf A\mathbf A^\top$이에요.

#### 주의할 점

$\mathbf u_2$를 $\mathbf A\mathbf A^\top$에서 임의로 $(0,1)^\top$으로 잡으면 $\mathbf v_2$와 부호가 어긋나 $\mathbf U\mathbf\Sigma\mathbf V^\top$의 둘째 행 부호가 반전돼요. 반드시 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 짝을 맞추고, 특잇값은 $\mathbf A$의 고윳값이 아니라 $\mathbf A^\top\mathbf A$ 고윳값의 제곱근이에요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mathbf A^\top\mathbf A=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top$, $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$, $\mathbf A\mathbf A^\top\mathbf u_i=\sigma_i^2\mathbf u_i$예요.

#### 첫 줄

$\mathbf A^\top\mathbf A=\begin{bmatrix}5&3\\3&5\end{bmatrix}$의 특성방정식을 세워요.

#### 핵심 답

(a) 고윳값 $8,2$, $\mathbf V=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}$. (b) $\sigma_1=2\sqrt2,\sigma_2=\sqrt2$, $\mathbf U=\begin{bmatrix}1&0\\0&-1\end{bmatrix}$. (c) $\mathbf A\mathbf A^\top=\operatorname{diag}(8,2)$라 $\mathbf u_i$는 고윳값 $\sigma_i^2$의 고유벡터가 맞아요.

#### 검산

$\mathbf U\mathbf\Sigma\mathbf V^\top=\mathbf A$이고 $\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top=\mathbf A\mathbf A^\top$이에요.

#### 조건·구분

$\mathbf u_i$ 부호는 $\mathbf v_i$와 연동하고, $\sigma_i$는 $\mathbf A$ 자체가 아니라 $\mathbf A^\top\mathbf A$ 고윳값의 제곱근이에요.

#### 출제 근거

MML Exercise 4.9, 교과서 138쪽(PDF 144쪽). 원문은 SVD를 구하라는 한 문장이고 (a), (b)와 $\mathbf A\mathbf A^\top$ 판정 (c)로 나눴어요.

수업: 1104 L06 s13(데이터 행렬의 SVD), 1102 특성다항식.

관련 정리노트: [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

#### 용어

- **특잇값 분해(singular value decomposition, SVD)** — 정사각행렬에서도 $\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top$에서 $\mathbf U$와 $\mathbf V$가 일반적으로 서로 달라요.
- **특잇값(singular value)** — 양의 특잇값은 $\mathbf A^\top\mathbf A$ 및 $\mathbf A\mathbf A^\top$의 양의 고윳값의 제곱근이에요.
- **고유벡터(eigenvector)** — $\mathbf M\mathbf x=\lambda\mathbf x$를 만족하는 0이 아닌 벡터예요.

---

<a id="p9"></a>

### P9. 가장 큰 특잇값으로 만든 랭크 1 근사

MML Exercise 4.10 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=9)

#### 주어진 조건

다음 행렬의 랭크 1 근사를 SVD의 첫 층 하나로 만들어요. 행렬 $\mathbf M$의 Frobenius 노름의 제곱 $\lVert\mathbf M\rVert_F^2$는 원소 제곱합이에요.

$$
\mathbf{A}=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}
$$

#### 구할 것

- (a) 가장 큰 특잇값 $\sigma_1$과 그에 대응하는 단위 특이벡터 $\mathbf u_1,\mathbf v_1$을 구해 보세요.
- (b) 랭크 1 근사 ${\mathbf{A}_1=\sigma_1\mathbf u_1\mathbf v_1^\top}$를 구해 보세요.
- (c) $\mathbf{A}-\mathbf{A}_1$의 원소 제곱합을 직접 계산해, 둘째 특잇값의 제곱 $\sigma_2^2$와 같은지 판정해 보세요.

<details><summary>원문 보기</summary>

“Find the rank-1 approximation of” — Exercise 4.10

</details>

#### 풀이 목표

$2\times 3$ 행렬 $\mathbf A$에서 (a) 최대 특잇값 $\sigma_1$과 $\mathbf u_1,\mathbf v_1$, (b) 랭크 1 근사 $\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top$를 구하고, (c) $\|\mathbf A-\mathbf A_1\|_F^2$가 $\sigma_2^2$와 같은지 판정해요.

#### 풀이 단서

랭크 1 근사는 SVD의 첫 외적 층 $\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top$이에요. $\mathbf u_1$은 $\mathbf A\mathbf A^\top$의 가장 큰 고윳값에 대응하는 단위 고유벡터, $\mathbf v_1=\mathbf A^\top\mathbf u_1/\sigma_1$이에요.

$2\times 3$ 행렬의 특잇값은 2개뿐이므로 첫 층을 빼고 남는 오차는 버린 특잇값 제곱합 $\|\mathbf A-\mathbf A_1\|_F^2=\sigma_2^2$와 비교해요([작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)).

#### 첫 단계

$$
\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix},\qquad(17-\lambda)^2-64=0
$$

큰 고윳값에서 $\sigma_1,\mathbf u_1,\mathbf v_1$을 구한 뒤 외적 $\mathbf A_1$과 잔차 $\mathbf A-\mathbf A_1$을 계산해요.

#### 핵심 풀이

#### (a) $\sigma_1$과 단위 특이벡터 $\mathbf u_1,\mathbf v_1$

$$
\begin{aligned}17-\lambda&=\pm8\implies\lambda_1=25,\ \lambda_2=9,\\\sigma_1&=\sqrt{25}=5\end{aligned}
$$

↳ 특성방정식으로 최대 특잇값을 구해요

$$
\begin{aligned}(17-25)x+8y&=0\implies x=y,\\\mathbf u_1&=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}\end{aligned}
$$

↳ 첫째 행으로 고유벡터를 구해 정규화해요

$$
\begin{aligned}\mathbf v_1&=\frac{\mathbf A^\top\mathbf u_1}{\sigma_1}=\frac{1}{5\sqrt2}\begin{bmatrix}5\\5\\0\end{bmatrix}\\&=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\\0\end{bmatrix}\end{aligned}
$$

↳ $\mathbf A^\top\mathbf u_1$을 $\sigma_1=5$로 나눠요

#### (b) 랭크 1 근사 $\mathbf A_1$

$$
\begin{aligned}\mathbf u_1\mathbf v_1^\top&=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1&1&0\end{bmatrix}\\&=\frac12\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}\end{aligned}
$$

↳ 두 단위 특이벡터의 외적을 구해요

$$
\mathbf A_1=5\mathbf u_1\mathbf v_1^\top=\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}
$$

↳ $\sigma_1=5$를 곱해 $\mathbf A_1$을 얻어요

두 행이 같고 0이 아니므로 $\operatorname{rank}(\mathbf A_1)=1$이에요.

#### (c) $\|\mathbf A-\mathbf A_1\|_F^2$와 $\sigma_2^2$ 비교

$$
\begin{aligned}\mathbf A-\mathbf A_1&=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}-\begin{bmatrix}\frac52&\frac52&0\\\frac52&\frac52&0\end{bmatrix}\\&=\begin{bmatrix}\frac12&-\frac12&2\\-\frac12&\frac12&-2\end{bmatrix}\end{aligned}
$$

↳ 원 행렬에서 근사 행렬을 빼요

$$
\|\mathbf A-\mathbf A_1\|_F^2=2\cdot\left(\frac14+\frac14+4\right)=9
$$

↳ 둘째 행은 부호만 반대라 2배해요

둘째 특잇값은 $\sigma_2=\sqrt{\lambda_2}=\sqrt9=3$이므로 $\sigma_2^2=9=\|\mathbf A-\mathbf A_1\|_F^2$로 정확히 같아요.

#### 최종 답

(a) $\sigma_1=5$, $\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top$, $\mathbf v_1=\frac{1}{\sqrt2}(1,1,0)^\top$이에요.

(b) $\mathbf A_1=\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}$이에요.

(c) $\|\mathbf A-\mathbf A_1\|_F^2=9$로 $\sigma_2^2=3^2=9$와 같아요.

#### 답 확인

#### (a) 검산

$\mathbf A\mathbf v_1=\frac{1}{\sqrt2}(5,5)^\top=5\mathbf u_1$로 $\mathbf A\mathbf v_1=\sigma_1\mathbf u_1$이 성립해요.

#### (b) 검산

$\|\mathbf A_1\|_F^2=4\times(5/2)^2=25=\sigma_1^2$로 첫 층의 제곱노름과 맞아요.

#### (c) 검산

$\|\mathbf A\|_F^2=9+4+4+4+9+4=34$이고 $\|\mathbf A_1\|_F^2+\|\mathbf A-\mathbf A_1\|_F^2=25+9=34$로 일치해요.

#### 주의할 점

$\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top$에서 $\sigma_1=5$를 빠뜨리면 제곱오차가 9가 아니라 25로 커져요. 또 문제에서 묻는 것은 노름 $3$이 아니라 제곱합 $9=\sigma_2^2$예요.

**페이지 요약**

#### 떠올릴 개념·공식

랭크 1 근사는 $\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top$이고 오차는 $\|\mathbf A-\mathbf A_1\|_F^2=\sigma_2^2$예요.

#### 첫 줄

$\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix}$의 특성방정식 $(17-\lambda)^2-64=0$을 풀어요.

#### 핵심 답

(a) $\sigma_1=5$, $\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top$, $\mathbf v_1=\frac{1}{\sqrt2}(1,1,0)^\top$. (b) $\mathbf A_1=\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}$. (c) $\|\mathbf A-\mathbf A_1\|_F^2=9=\sigma_2^2$예요.

#### 검산

$\|\mathbf A\|_F^2=34=25+9=\|\mathbf A_1\|_F^2+\|\mathbf A-\mathbf A_1\|_F^2$예요.

#### 조건·구분

$\sigma_1$을 꼭 곱하고, 제곱합 $9$를 $\sigma_2^2$과 비교해요.

#### 출제 근거

MML Exercise 4.10, 교과서 138쪽(PDF 144쪽). 원문은 랭크 1 근사를 구하라는 한 문장이고 (a), (b)와 오차 판정 (c)로 나눴어요.

수업: 1104 L06 s14(랭크 제한 복원, Frobenius 오차).

관련 정리노트: [작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)

#### 용어

- **랭크 1 근사(rank-1 approximation)** — 가장 큰 특잇값에 대응하는 첫 외적 층 $\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top$이에요.
- **외적(outer product)** — 열벡터와 행벡터의 곱 $\mathbf u\mathbf v^\top$으로 각 성분이 $u_iv_j$인 행렬이에요.
- **Frobenius 노름(Frobenius norm)** — 행렬 원소 제곱합의 제곱근 $\|\mathbf M\|_F=\sqrt{\sum_{i,j}M_{ij}^2}$예요.

---

<a id="p10"></a>

### P10. 행렬이 벡터의 길이를 가장 크게 늘리는 비율

MML Exercise 4.12 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=10)

#### 주어진 조건

$\mathbf A\in\mathbb R^{m\times n}$의 특잇값 분해를 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$라 해요. 오른쪽 특이벡터 $\mathbf v_1,\ldots,\mathbf v_n$은 $\mathbb R^n$의 정규직교기저이고, 양의 특잇값은 ${\sigma_1\ge\sigma_2\ge\cdots\ge\sigma_r\gt0}$이에요. $i\gt r$이면 $\sigma_i=0$으로 두면, 모든 $i$에서 ${\mathbf A^\top\mathbf A\mathbf v_i=\sigma_i^2\mathbf v_i}$예요.

#### 구할 것

$\mathbf x\ne\mathbf 0$일 때 다음 식(정리 4.24)을 네 단계로 증명해요.

$$
\max_{\mathbf x\ne\mathbf 0}\frac{\lVert\mathbf A\mathbf x\rVert_2}{\lVert\mathbf x\rVert_2}=\sigma_1
$$

- (a) $\mathbf x=\sum_{i=1}^n c_i\mathbf v_i$로 쓰고, ${\lVert\mathbf A\mathbf x\rVert_2^2=\sum_{i=1}^n\sigma_i^2c_i^2}$임을 증명해 보세요.
- (b) (a)를 써서 ${\lVert\mathbf A\mathbf x\rVert_2^2\le\sigma_1^2\lVert\mathbf x\rVert_2^2}$임을 증명해 보세요.
- (c) $\mathbf x=\mathbf v_1$에서 등호가 성립함을 확인해 보세요.
- (d) 그래서 길이 비율의 최댓값이 $\sigma_1$인 이유를 설명해 보세요.

<details><summary>원문 보기</summary>

“Show that for x ≠ 0 Theorem 4.24 holds” — Exercise 4.12

</details>

#### 풀이 목표

정규직교기저 $\{\mathbf v_1,\dots,\mathbf v_n\}$($\mathbf A^\top\mathbf A\mathbf v_i=\sigma_i^2\mathbf v_i$, $\sigma_1\ge\cdots\ge\sigma_r>0$, $i>r$이면 $\sigma_i=0$)를 써서 $\mathbf x\ne\mathbf 0$일 때 $\max_{\mathbf x\ne\mathbf 0}\frac{\|\mathbf A\mathbf x\|_2}{\|\mathbf x\|_2}=\sigma_1$을 (a)–(d) 네 단계로 증명해요.

#### 풀이 단서

최댓값 증명은 상한 제시((b))와 실제 도달((c))의 두 단계로 이뤄져요. 정규직교성 $\mathbf v_i^\top\mathbf v_j=\delta_{ij}$($i=j$면 1, 다르면 0) 덕분에 $\mathbf x=\sum_{i=1}^n c_i\mathbf v_i$($c_i=\mathbf v_i^\top\mathbf x$)의 길이 제곱은 $\|\mathbf x\|_2^2=\mathbf x^\top\mathbf x=\sum_{i=1}^n c_i^2$예요([첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions)).

여기에 $\|\mathbf A\mathbf x\|_2^2=\mathbf x^\top\mathbf A^\top\mathbf A\mathbf x$와 고유방정식 $\mathbf A^\top\mathbf A\mathbf v_j=\sigma_j^2\mathbf v_j$를 연결해요.

#### 첫 단계

$$
\|\mathbf A\mathbf x\|_2^2=(\mathbf A\mathbf x)^\top(\mathbf A\mathbf x)=\mathbf x^\top(\mathbf A^\top\mathbf A\mathbf x),\qquad\mathbf x=\sum_{j=1}^n c_j\mathbf v_j
$$

전개식을 $\mathbf A^\top\mathbf A$에 먼저 적용한 뒤 $\mathbf x^\top$와 내적해요.

#### 핵심 풀이

#### (a) $\|\mathbf A\mathbf x\|_2^2=\sum_{i=1}^n\sigma_i^2 c_i^2$ 증명

$$
\mathbf A^\top\mathbf A\mathbf x=\sum_{j=1}^n c_j\mathbf A^\top\mathbf A\mathbf v_j=\sum_{j=1}^n c_j\sigma_j^2\mathbf v_j
$$

↳ 선형성과 고유방정식을 써요

$$
\|\mathbf A\mathbf x\|_2^2=\Big(\sum_{i=1}^n c_i\mathbf v_i^\top\Big)\Big(\sum_{j=1}^n c_j\sigma_j^2\mathbf v_j\Big)
$$

↳ $\mathbf x^\top$와 $\mathbf A^\top\mathbf A\mathbf x$를 내적해요

$$
\hphantom{\|\mathbf A\mathbf x\|_2^2}=\sum_{i=1}^n\sum_{j=1}^n c_i c_j\sigma_j^2(\mathbf v_i^\top\mathbf v_j)
$$

↳ 이중 합으로 전개해요

$$
\hphantom{\|\mathbf A\mathbf x\|_2^2}=\sum_{i=1}^n\sigma_i^2 c_i^2
$$

↳ $\mathbf v_i^\top\mathbf v_j=\delta_{ij}$로 대각항만 남겨요

#### (b) 상한 부등식 $\|\mathbf A\mathbf x\|_2^2\le\sigma_1^2\|\mathbf x\|_2^2$

모든 $i$에서 $\sigma_i^2\le\sigma_1^2$이고 $c_i^2\ge 0$이므로 각 항을 $\sigma_1^2 c_i^2$로 올려도 부등호가 유지돼요.

$$
\|\mathbf A\mathbf x\|_2^2=\sum_{i=1}^n\sigma_i^2 c_i^2\le\sum_{i=1}^n\sigma_1^2 c_i^2=\sigma_1^2\sum_{i=1}^n c_i^2=\sigma_1^2\|\mathbf x\|_2^2
$$

$\mathbf x\ne\mathbf 0$이면 $\|\mathbf x\|_2>0$이므로 나누고 음이 아닌 제곱근을 취하면 $\frac{\|\mathbf A\mathbf x\|_2}{\|\mathbf x\|_2}\le\sigma_1$이에요.

#### (c) $\mathbf x=\mathbf v_1$에서의 등호

$\mathbf x=\mathbf v_1$이면 정규직교성으로 $c_1=\mathbf v_1^\top\mathbf v_1=1$, $i>1$에서 $c_i=\mathbf v_i^\top\mathbf v_1=0$이에요. (a)와 $\|\mathbf v_1\|_2=1$을 쓰면 $\|\mathbf A\mathbf v_1\|_2^2=\sigma_1^2$이고 $\frac{\|\mathbf A\mathbf v_1\|_2}{\|\mathbf v_1\|_2}=\sigma_1$이에요.

#### (d) 최댓값이 $\sigma_1$인 이유

(b)에 따라 모든 $\mathbf x\ne\mathbf 0$의 길이 비율은 상한 $\sigma_1$ 이하이고, (c)에 따라 $\mathbf x=\mathbf v_1$($\ne\mathbf 0$)에서 실제로 $\sigma_1$에 도달하므로 최댓값은 $\sigma_1$이에요.

#### 최종 답

(a) $\mathbf v_i^\top\mathbf v_j=\delta_{ij}$로 교차항이 사라져 $\|\mathbf A\mathbf x\|_2^2=\sum_{i=1}^n\sigma_i^2 c_i^2$이에요.

(b) $\sigma_i^2\le\sigma_1^2$와 $c_i^2\ge 0$으로 $\|\mathbf A\mathbf x\|_2^2\le\sigma_1^2\|\mathbf x\|_2^2$이에요.

(c) $\mathbf x=\mathbf v_1$일 때 $c_1=1, c_{i>1}=0$이라 $\|\mathbf A\mathbf v_1\|_2^2=\sigma_1^2\|\mathbf v_1\|_2^2=\sigma_1^2$로 등호가 성립해요.

(d) 모든 $\mathbf x\ne\mathbf 0$에서 비율의 상한이 $\sigma_1$이고 $\mathbf v_1$에서 도달하므로 최댓값은 $\sigma_1$이에요.

#### 답 확인

#### (a) 검산

$\mathbf v_i^\top\mathbf v_j=\delta_{ij}$와 선형성만 써서 $m,n$ 크기에 상관없이 성립하며 $\|\mathbf x\|_2^2=\sum_{i=1}^n c_i^2$도 같은 전개로 확인돼요.

#### (b) 검산

$c_i^2\ge 0$이라 부등호 방향이 보존되고, 나눗셈에서 $\mathbf x\ne\mathbf 0$ ($\|\mathbf x\|_2^2>0$) 조건을 지켰어요.

#### (c) 검산

$\mathbf A\mathbf v_1=\sigma_1\mathbf u_1$에서 $\|\mathbf u_1\|_2=1$이므로 $\|\mathbf A\mathbf v_1\|_2=\sigma_1$이 다시 확인돼요.

#### (d) 검산

상한 존재((b))와 비영벡터 $\mathbf v_1$에서의 도달((c))이 모두 갖춰져 최댓값 정의를 만족해요.

#### 주의할 점

(b)의 상한 $\le\sigma_1$만으로는 최댓값이 $\sigma_1$이라고 단정할 수 없고 (c)의 도달 벡터 $\mathbf v_1$이 있어야 해요. 또 직교 성분의 길이는 $\sum\sigma_i|c_i|$가 아니라 제곱합의 제곱근 $\sqrt{\sum\sigma_i^2 c_i^2}$이에요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mathbf x=\sum c_i\mathbf v_i$($c_i=\mathbf v_i^\top\mathbf x$)와 $\mathbf A^\top\mathbf A\mathbf v_i=\sigma_i^2\mathbf v_i$, $\mathbf v_i^\top\mathbf v_j=\delta_{ij}$를 써요.

#### 첫 줄

$\|\mathbf A\mathbf x\|_2^2=\mathbf x^\top(\mathbf A^\top\mathbf A\mathbf x)$에 $\mathbf x=\sum c_j\mathbf v_j$를 넣어요.

#### 핵심 답

(a) $\|\mathbf A\mathbf x\|_2^2=\sum\sigma_i^2 c_i^2$. (b) $\sigma_i^2\le\sigma_1^2$로 $\le\sigma_1^2\|\mathbf x\|_2^2$. (c) $\mathbf x=\mathbf v_1$에서 등호. (d) 상한 $\sigma_1$에 $\mathbf v_1$이 도달해 최댓값은 $\sigma_1$이에요.

#### 검산

정규직교성·$c_i^2\ge0$·$\|\mathbf x\|_2>0$과 $\mathbf A\mathbf v_1=\sigma_1\mathbf u_1$로 상한과 도달을 확인해요.

#### 조건·구분

상한만으로는 부족하며 도달 벡터 $\mathbf v_1$이 필요해요. 직교 합은 제곱합으로 계산해요.

#### 출제 근거

MML Exercise 4.12(정리 4.24), 교과서 138쪽(PDF 144쪽). 원문은 정리 4.24 증명을 요구하며 기저 전개 방식의 (a)–(d)로 나눴어요.

수업: 1104 L05 s27–28(상한 찾기와 도달), L06 s13(SVD).

관련 정리노트: [첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions), [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

#### 용어

- **유클리드 노름(Euclidean norm)** — 벡터의 길이 $\|\mathbf x\|_2=\sqrt{\sum x_i^2}=\sqrt{\mathbf x^\top\mathbf x}$예요.
- **정규직교기저(orthonormal basis)** — 단위 길이를 갖고 서로 수직($\mathbf v_i^\top\mathbf v_j=\delta_{ij}$)인 기저 벡터 묶음이에요.
- **최대 특잇값(largest singular value)** — 가장 큰 특잇값 $\sigma_1$으로, 행렬의 최대 신장 비율 $\max_{\mathbf x\ne\mathbf 0}\frac{\|\mathbf A\mathbf x\|_2}{\|\mathbf x\|_2}$과 같아요.
- **상한과 최댓값(upper bound & maximum)** — 모든 원소가 넘지 않는 경계가 상한이고, 그 경계에 실제로 도달하는 원소가 있을 때 최댓값이 돼요.

---
