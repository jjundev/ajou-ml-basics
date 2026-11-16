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

#### 문제를 내 말로 읽어요

**주어진 것:** 누적 설명 분산 공식 $V_M=\sum_{m=1}^{M}\lambda_m$과 두 그래프(왼쪽: 고윳값 순서별 크기 $\lambda_m$, 오른쪽: 주성분 개수별 누적 분산 $V_M$)가 주어졌어요.

**구할 것:** (a) 이웃한 두 누적값의 차이 $V_M-V_{M-1}$을 고윳값으로 나타내고, (b) 두 그래프를 연결해 주성분을 앞쪽과 뒤쪽에서 추가할 때의 증가 폭을 비교해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘주성분을 하나 추가할 때 늘어나는 양’이라는 단서에서 **누적합의 이웃 차이**와 **고윳값의 분산 의미**를 떠올려요.

공분산 행렬 $\mathbf S$의 단위 고유벡터 $\mathbf p_m$ 방향으로 사영한 좌표의 분산은 $\mathbf p_m^\top\mathbf S\mathbf p_m=\lambda_m$이에요. 즉, 고윳값 $\lambda_m$은 **$m$번째 주성분 축 하나에 담긴 분산**이에요.

상위 $M$개 주성분을 축으로 고를 때 서로 직교하는 축들의 분산을 더한 누적 설명 분산(captured variance)은 다음과 같아요($\lambda_1\ge\lambda_2\ge\cdots$).

$$
V_M=\sum_{m=1}^{M}\lambda_m=\underbrace{\sum_{m=1}^{M-1}\lambda_m}_{V_{M-1}}+\lambda_M
$$

따라서 왼쪽 그래프의 개별 점 높이($\lambda_M$)는 오른쪽 곡선에서 한 칸 전진할 때 오르는 **상승 폭(증분)**과 같아요. [첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions)에서 같은 식을 다뤘어요.

#### 종이에 쓸 첫 줄

두 누적합을 마지막 항 $\lambda_M$만 분리해 나란히 적고 빼는 2단계 로드맵(1. 두 식 차분 $\to$ 2. 그래프 좌표 대조)으로 시작해요.

$$
V_M=\sum_{m=1}^{M}\lambda_m=V_{M-1}+\lambda_M,\qquad V_{M-1}=\sum_{m=1}^{M-1}\lambda_m
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** 이웃한 두 누적 설명 분산의 차이는 $M$번째 고윳값인 $V_M-V_{M-1}=\lambda_M$이에요.

첫 줄의 두 식을 직접 차분해요. 공통인 앞의 $M-1$개 고윳값 합이 모두 소거돼요.

$$
V_M-V_{M-1}=\sum_{m=1}^{M}\lambda_m-\sum_{m=1}^{M-1}\lambda_m=\lambda_M
$$

따라서 $M$번째 주성분을 추가하면 누적 설명 분산은 정확히 그 주성분 축의 고유 분산인 **$\lambda_M$만큼** 늘어나요.

#### (b)

**최종 답 요약:** 초반 주성분(1~5번째) 추가 시에는 $\lambda_M$이 커서 가파르게 증가하고, 뒤쪽으로 갈수록 $\lambda_M$이 급감하여 완만하게 증가해요.

(a)에 따라 오른쪽 곡선의 $M$번째 증분은 왼쪽 그래프의 $M$번째 점 높이 $\lambda_M$이에요. 주요 지점별 수치를 표로 비교해요.

| 구간 / 순서 ($m$) | 왼쪽 고윳값 ($\lambda_m$, 증분) | 오른쪽 누적 분산 ($V_M$, 곡선 형태) | 해석 |
|---|---|---|---|
| $m=1, 2$ | 약 46, 약 32 (매우 큼) | 0에서 약 78로 급상승 | 첫 몇 개 축이 나중의 축보다 하나당 더 많은 분산을 담음 |
| $m=3 \sim 5$ | 약 21 $\to$ 약 15 (급격히 감소) | 기울기가 빠르게 완만해짐 | 개별 축이 더하는 분산이 빠르게 줄어듦 |
| $m \approx 50$ | 약 2 ~ 3 (작음) | $V_{50}\approx 370$ 도달 후 완만 | 그림의 200개까지 누적한 분산 중 약 7할에 도달 |
| $m \approx 150 \sim 200$ | 1 미만 (매우 작으나 양수) | 약 505에서 약 525로 완만히 증가 | 미세 잔차 영역이지만 계속 소폭 증가 |

따라서 **주성분을 처음 몇 개 추가할 때 누적 설명 분산이 크게 늘고, 뒤에서 추가할 때는 완만하게 늘어요.**

#### 완성 답과 검산

#### (a) 검산

$M=1$을 넣으면 $V_1-V_0=\lambda_1$이에요($V_0=0$). 오른쪽 곡선의 시작점 높이(약 46)가 왼쪽 첫 점 $\lambda_1\approx 46$과 일치해요. $M=2$에서도 $V_2\approx 46+32=78$로 둘째 칸 높이와 일치해요.

#### (b) 검산

오른쪽 곡선에서 50단위 구간 증가량을 대조해요. 구간 $[0, 50]$의 증가는 $\Delta V\approx 370$인 반면, 구간 $[150, 200]$의 증가는 $\Delta V\approx 20$이에요. 초반 증가 폭이 후반의 약 18배로 읽혀 왼쪽 고윳값의 감소와 일치해요.

#### 이 문항에서 조심할 점

**곡선의 높이와 기울기(점 높이)를 혼동하지 않아요.** 오른쪽 곡선의 높이는 누적합 $V_M$이고, 왼쪽 그래프 점의 높이는 한 칸의 증가량 $\lambda_M$이에요. 오른쪽 곡선에서 $M=100$의 높이(약 460)를 $\lambda_{100}$으로 읽으면 안 돼요.

**뒤쪽 고윳값이 작다고 0으로 단정하지 않아요.** 50개에서 200개까지 곡선이 약 370에서 약 525로 약 155 더 올라요. 이 구간에 양의 고윳값이 남아 있어 작은 증가량이 쌓여요.

$V_M$은 분산의 합이지 비율(%)이 아니에요. 비율을 구하려면 전체 분산으로 나눠야 해요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. $V_M$과 $V_{M-1}$을 나란히 적고 빼서 $V_M-V_{M-1}=\lambda_M$을 다시 유도해요.
2. 두 그래프의 세로축 의미(개별 축 분산 vs 누적 보존 분산)를 구별해요.
3. 왼쪽 그래프의 초반 점과 후반 점 높이를 읽어 오른쪽 곡선의 기울기 변화와 연결해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\lambda_m$은 $m$번째 주성분 방향의 분산이에요. 누적 설명 분산은 $V_M=\sum_{m=1}^{M}\lambda_m$이에요.

#### 첫 줄

$V_M$과 $V_{M-1}$을 마지막 항만 떼어 나란히 적어요.

#### 핵심 답

(a) $V_M-V_{M-1}=\lambda_M$이에요.

(b) 앞쪽 고윳값(약 46, 32)이 크고 빠르게 감소하므로, 처음 몇 개를 추가할 때 급격히 늘고 뒤로 갈수록 완만하게 늘어요. 곡선은 200개까지 계속 소폭 상승해요.

#### 검산

오른쪽 시작점 높이 약 46이 $\lambda_1$과 같아요. 구간 증가량은 $[0, 50]$이 약 370, $[150, 200]$이 약 20이에요.

#### 조건·구분

오른쪽 높이는 누적값, 왼쪽 점은 한 칸의 상승 폭이에요. 그림의 후반에도 누적합은 소폭 증가해요.

#### 용어

- **고윳값(eigenvalue)** — 공분산 행렬 $\mathbf S$에서 $\mathbf S\mathbf p_m=\lambda_m\mathbf p_m$을 만족하는 수예요. 단위 고유벡터 $\mathbf p_m$ 방향의 분산과 같아요.
- **주성분(principal component)** — 큰 고윳값부터 고른 공분산 행렬의 단위 고유벡터 방향이에요. 서로 직교해요.
- **누적 설명 분산(captured variance)** — 상위 $M$개 주성분이 보존하는 분산의 총합 $V_M=\sum_{m=1}^{M}\lambda_m$이에요. 비율이 아니라 분산의 합이에요.

#### 출제 근거

MML Example 10.2와 그림 10.5, 교과서 324–325쪽(PDF 330–331쪽), 식 (10.24).

수업: 1104 L05 s27–28(상위 $M$개 방향과 보존 분산).

관련 정리노트: [첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions)

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

#### 문제를 내 말로 읽어요

**주어진 것:** $28\times28$ 손글씨 이미지(784차원)를 첫 두 주성분 평면($\mathbb R^2$)에 투영한 산점도(파란 점: 숫자 0, 주황 점: 숫자 1, 빨간 선: 대표 이미지 안내선)가 주어졌어요.

**구할 것:** (a) 두 숫자 무리가 2차원 평면에서 분리되는 정도, (b) 각 숫자 집단 내부의 분산(퍼짐) 크기를 산점도를 근거로 판별해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘첫 두 주성분이 만드는 평면’이라는 단서에서 **사영 좌표(projection coordinates)**와 **2차원 축소**를 떠올려요.

평균을 뺀 이미지 $\mathbf x_n \in \mathbb R^{784}$을 상위 두 주성분 기저 $\mathbf B = [\mathbf b_1, \mathbf b_2] \in \mathbb R^{784\times 2}$에 투영하면 2차원 좌표 벡터를 얻어요.

$$
\mathbf z_n = \mathbf B^\top \mathbf x_n = \begin{bmatrix} \mathbf b_1^\top \mathbf x_n \\ \mathbf b_2^\top \mathbf x_n \end{bmatrix} \in \mathbb R^2
$$

‘분리 정도’는 두 집단 중심 간 거리 대비 경계의 중첩 유무를 보며, ‘집단 내 분산(within-class variance)’은 각 색상의 점에서 자기 집단 중심까지의 **제곱 거리의 평균**이에요. 그림에서는 외곽점 하나보다 점들이 중심을 둘러싸고 얼마나 넓게 퍼져 있는지를 봐요. [MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)에서 같은 그림을 다뤘어요.

#### 종이에 쓸 첫 줄

산점도의 색상과 숫자를 매핑하고 2단계 판별 기준(1. 경계 중첩 여부로 분리도 $\to$ 2. 중심에서 떨어진 거리의 산포로 집단 내 분산)을 적어요.

‘파란 점 = 숫자 0, 주황 점 = 숫자 1. (a)는 두 군집 경계의 겹침 판정, (b)는 군집별 가로·세로 확산 범위 비교.’

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 요약:** 경계부에서 일부 점이 중첩되지만 두 숫자(0과 1) 군집은 2차원 평면에서 비교적 뚜렷하게 분리돼요.

주황색 점(숫자 1)은 왼쪽 좁은 영역에 밀집되어 있고, 파란색 점(숫자 0)은 그보다 오른쪽에 중심을 두고 아래까지 넓게 퍼져 두 군집의 중심이 확실히 떨어져 있어요.

두 무리가 맞닿는 경계에서 주황 점 일부가 파란 무리 쪽으로 흩어져 경미한 겹침이 관찰되지만, 전체 데이터의 대다수는 자기 영역 내에 위치해요. 따라서 784차원을 단 2차원으로 축소했음에도 두 클래스가 비교적 뚜렷이 분리돼요.

#### (b)

**최종 답 요약:** 숫자 0 집단이 산점도에서 차지하는 가로·세로 영역이 훨씬 넓어 집단 내 분산이 숫자 1보다 훨씬 커요.

산점도에서 관찰되는 두 집단의 기하학적 분포 특성을 표로 비교해요.

| 비교 항목 | 숫자 1 군집 (주황 점) | 숫자 0 군집 (파란 점) | 판별 근거 |
|---|---|---|---|
| 분포 위치 | 좌상단 국소 영역 | 중앙에서 우하단까지 광범위 | 군집 중심 간 확실한 거리 확보 |
| 확산 영역 (범위) | 가로·세로 모두 좁음 | 상하·좌우로 더 넓게 확산 | 중심으로부터의 거리 제곱 평균(분산)이 0이 훨씬 큼 |
| 밀집도 및 형태 다양성 | 조밀하게 뭉침 (획 변형 적음) | 넓게 퍼짐 (기울기·두께·형태 다양) | 파란 무리의 중심 주변부터 외곽까지 넓게 점이 분포함 |
| 집단 내 분산 결론 | 상대적으로 작음 | **상대적으로 훨씬 큼** | 각 중심으로부터 퍼져 있는 점들의 가로·세로 폭 차이 |

따라서 **숫자 0 집단이 주성분 평면에서 더 넓게 퍼져 있어 집단 안의 분산이 더 커요.** 안내선에 연결된 원본 이미지에서도 1은 단순한 획 형태인 반면 0은 크기·기울기·가로세로 비율 변동이 커 이와 일치해요.

#### 완성 답과 검산

#### (a) 검산

안내선이 가리키는 원본 이미지를 확인해요. 왼쪽 주황 무리에 연결된 이미지는 숫자 1이고, 오른쪽 파란 무리에 연결된 이미지는 숫자 0이에요. 영역별로 클래스가 정합하므로 두 집단이 대부분 나뉜다는 판정과 정확히 맞아요.

#### (b) 검산

외곽 극단점(outlier)을 확인해요. 그림의 오른쪽과 아래쪽까지 파란 점이 퍼져 있고 점이 조밀한 부분도 주황 무리보다 넓어요. 주황 점 대부분은 자체 중심 가까이에 있어서 숫자 0의 분산이 더 크다는 결론과 일치해요.

#### 이 문항에서 조심할 점

**각 집단의 중심부터 점들이 얼마나 떨어져 있는지 살펴요.** 주황 점은 좁은 곳에 모여 있어요. 파란 무리에서는 중심과 거리가 있는 곳에도 점이 많이 분포해요.

**(a)의 분리도와 (b)의 분산은 독립된 질문이에요.** 두 집단이 완벽히 분리되어도 각 집단 내부의 분산은 작을 수도, 매우 클 수도 있어요.

빨간 선과 빨간 점은 대표 이미지의 위치를 표시하는 보조선일 뿐 데이터 포인트가 아니에요.

이 비교는 첫 두 주성분 평면으로 사영된 2차원 공간에서의 관찰이에요. 784차원 픽셀 공간 전체의 분산을 단정하지 않아요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. 산점도의 색상과 숫자(0: 파랑, 1: 주황) 매핑을 확인해요.
2. 두 군집이 접하는 경계의 중첩 여부를 관찰해 분리 정도를 서술해요.
3. 각 색상이 차지하는 평면 상의 종횡 너비를 대조해 집단 내 분산을 비교해요.

**페이지 요약**

#### 떠올릴 개념·공식

점의 좌표는 첫 두 주성분 기저와의 사영 내적이에요.

$$
\mathbf z_n=\mathbf B^\top\mathbf x_n\in\mathbb R^2
$$

분리는 군집 간 경계 중첩 여부, 분산 비교에는 각 군집 중심에서 점들이 떨어져 있는 정도를 봐요.

#### 첫 줄

파란 점 = 0, 주황 점 = 1, 빨간 선 = 대표 이미지 안내선으로 정리해요.

#### 핵심 답

(a) 경계에서 경미한 중첩이 있으나 비교적 뚜렷하게 나뉘어요.

(b) 숫자 0 집단이 훨씬 넓게 퍼져 집단 내 분산이 더 커요.

#### 검산

안내선으로 영역의 숫자를 확인할 수 있고, 파란 점은 가로·세로 양쪽으로 넓게 퍼져 있어요.

#### 조건·구분

자기 집단 중심으로부터의 퍼짐으로 분산을 비교해요. 2차원 사영 공간에서의 관찰이에요.

#### 용어

- **주성분 평면(principal subspace)** — 상위 두 주성분 기저 벡터 $\mathbf b_1, \mathbf b_2$가 생성하는 2차원 부분공간이에요.
- **사영 좌표(projection coordinates)** — 평균 중심화 데이터와 주성분 기저의 내적 $\mathbf b_i^\top \mathbf x_n$으로 정의되는 저차원 좌표예요.
- **산점도(scatter plot)** — 고차원 이미지를 2차원 사영 좌표의 점으로 시각화한 분포도예요.
- **집단 안의 분산(within-class variance)** — 동일 클래스 내부의 데이터들이 자체 중심점으로부터 흩어진 제곱 거리의 평균이에요.

#### 출제 근거

MML Example 10.3과 그림 10.10, 교과서 332–333쪽(PDF 338–339쪽).

수업: 1104 L06 s11(MNIST 0과 1의 2차원 사영).

관련 정리노트: [MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)

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

#### 문제를 내 말로 읽어요

**주어진 것:** $D=784$차원 손글씨 숫자 8 이미지, 학습 데이터로 구한 주성분 기저, 테스트 이미지 4장의 복원 그림(맨 윗행: 원본, 아래: $M=1, 10, 100, 500$), 학습 평균제곱 복원오차 식 $J_M^\star = \sum_{i=M+1}^{D}\lambda_i$, 그리고 $M$이 약 400개를 넘으면 학습 오차가 거의 0이라는 관찰이 주어졌어요.

**구할 것:** (a) 주성분 수 $M$ 증가에 따른 복원 이미지 품질 변화, (b) $M=784$일 때 $J_{784}^\star$ 계산 및 수학적 완전 복원 증명, (c) 500개만으로도 충분한 이유를 설명해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘주성분 $M$개로 복원’이라는 단서에서 **사영과 기저 복원**을 떠올려요. 복원할 원본 이미지 벡터를 $\mathbf x$, 숫자 8 학습 이미지 5,389장의 평균 벡터를 $\bar{\mathbf x}$라 해요. 정규직교 고유벡터를 열로 모은 $\mathbf B \in \mathbb R^{784\times M}$로 중심화 벡터 $\mathbf x-\bar{\mathbf x}$의 좌표 $\mathbf z$를 구해요. $\mathbf B\mathbf z$는 중심화된 공간에서의 복원이므로 평균 벡터를 더해 원래 이미지 좌표로 돌아가요.

$$
\tilde{\mathbf x}=\bar{\mathbf x}+\mathbf B\mathbf z,\qquad \mathbf z=\mathbf B^\top(\mathbf x-\bar{\mathbf x})
$$

‘평균제곱 복원오차’라는 단서에서 **버려진 방향의 고윳값 총합**을 떠올려요. 직교 기저에서 버려진 축 성분의 분산 합이 바로 최적 오차예요($\lambda_1\ge\cdots\ge\lambda_D\ge0$).

$$
J_M^\star = \sum_{i=M+1}^{D}\lambda_i
$$

‘$M=D=784$’라는 조건에서는 **정사각 직교행렬의 양방향 항등성**을 떠올려요. 열이 정규직교인 정사각행렬은 $\mathbf B^\top\mathbf B=\mathbf I$뿐만 아니라 $\mathbf B\mathbf B^\top=\mathbf I$도 만족해요. [버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded)와 [MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)에서 같은 공식을 다뤘어요.

#### 종이에 쓸 첫 줄

(a)는 열별 위아래 비교 로드맵, (b)·(c)는 오차 합의 시작 번호와 끝 번호를 적는 2단계 로드맵으로 시작해요.

$$
J_{784}^\star=\sum_{i=785}^{784}\lambda_i=0, \qquad J_{500}^\star=\sum_{i=501}^{784}\lambda_i
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 요약:** 주성분 수 $M$이 증가할수록 흐릿한 전체 평균 형태에서 개별 원본의 고유한 획과 기울기가 선명히 살아나는 형상으로 복원돼요.

각 열(동일 원본 이미지)의 $M$ 단계별 복원 특성을 표로 비교해요.

| 주성분 개수 ($M$) | 복원 이미지 상태 | 보존된 정보 | 특징 |
|---|---|---|---|
| $M=1$ | 흐릿한 얼룩 | 공통적인 8 윤곽이 두드러짐 | 이미지별 기울기와 획 차이는 흐릿하게 드러남 |
| $M=10$ | 대략적인 윤곽 형성 | 숫자의 대략적 기울기와 크기 | 세부 획이 번지고 배경에 회색 얼룩 잔존 |
| $M=100$ | 뚜렷한 숫자 형상 | 개별 숫자의 고유 필체와 획 특징 | 원본을 충분히 식별 가능하나 미세 노이즈 존재 |
| $M=500$ | 원본과 육안으로 매우 비슷함 | 세부 곡률 및 픽셀 명암 디테일 | 그림에서 원본과 매우 비슷한 복원 |

따라서 주성분을 늘릴수록 흐릿하고 정형화된 형태에서 개별 원본의 세부가 살아 있는 선명한 이미지로 전환돼요.

#### (b)

**최종 답 구조:** $M=784$일 때 $\mathbf B\mathbf B^\top=\mathbf I_{784}$이므로 $\tilde{\mathbf x}=\mathbf x$이고, 버려진 항이 없는 빈 합이므로 $J_{784}^\star=0$이에요.

$M=784=D$이면 기저 행렬 $\mathbf B$는 $784\times 784$ 정사각 정규직교행렬이에요. 정규직교 정사각행렬의 전치행렬은 곧 역행렬($\mathbf B^{-1}=\mathbf B^\top$)이므로 좌우 곱셈 순서에 관계없이 항등행렬이 돼요.

$$
\tilde{\mathbf x}=\bar{\mathbf x}+\mathbf B\mathbf B^\top(\mathbf x-\bar{\mathbf x})=\bar{\mathbf x}+\mathbf I_{784}(\mathbf x-\bar{\mathbf x})=\mathbf x
$$

복원오차 공식에서도 버려진 축이 전혀 없으므로 합의 시작 지점(785)이 끝 지점(784)을 초과하는 **빈 합(empty sum)**이 되어 정확히 0이에요.

$$
J_{784}^\star = \sum_{i=785}^{784}\lambda_i = 0
$$

따라서 모든 주성분을 사용하면 학습 이미지뿐 아니라 임의의 테스트 이미지까지 원본이 수학적으로 정확히 복원돼요.

#### (c)

**최종 답 요약:** $J_M^\star$는 단조 감소하여 $M=500$에서 버려진 학습 분산의 합이 거의 0이에요. 테스트 이미지 네 장의 복원도 그림에서 원본과 매우 비슷해요.

고윳값은 항상 비음수($\lambda_i \ge 0$)이므로 $M$이 커질수록 오차 $J_M^\star$는 단조 감소(줄어들거나 유지)해요.

$$
J_M^\star - J_{M+1}^\star = \lambda_{M+1} \ge 0 \implies J_{500}^\star \le J_{450}^\star
$$

문제에 주어진 오차 곡선 설명에 따르면 약 400개를 지난 구간에서 학습 오차가 이미 0에 가깝고, 따라서 $J_{500}^\star = \sum_{i=501}^{784}\lambda_i \approx 0$이에요. 특히 학습 이미지에서 바깥쪽 픽셀처럼 항상 같은 값을 갖는 좌표는 분산이 0이어서 유효 차원이 낮아져요.

이 네 테스트 이미지에서도 버려진 방향의 성분이 작았다는 점을 그림의 원본 행과 500개 복원 행이 거의 같다는 사실로 확인해요. 학습 평균오차만으로는 개별 테스트 이미지의 오차를 알 수 없어요.

#### 완성 답과 검산

#### (a) 검산

넷째 열(우측으로 기운 8)을 확인해요. $M=1$에서는 기울기와 획이 흐릿하지만, $M=10, 100$을 거치며 기울어진 필체가 살아나고 $M=500$에서는 그림에서 원본과 매우 비슷해요.

#### (b) 검산

복원식에서 원본을 빼면 $\tilde{\mathbf x}-\mathbf x=(\mathbf B\mathbf B^\top-\mathbf I_{784})(\mathbf x-\bar{\mathbf x})$예요. $M=784$에서는 괄호 안의 행렬이 0이므로 임의의 이미지 벡터에서 복원 차이가 0이에요.

#### (c) 검산

학습 오차는 $0\le J_{550}^\star\le J_{500}^\star\le J_{450}^\star$이고, 450개는 문제에서 0에 가깝다고 설명한 구간에 있어요. 그림 10.12에서는 테스트 이미지 네 장의 $M=500$ 행과 원본 행을 열별로 비교해요.

#### 이 문항에서 조심할 점

**‘거의 완벽한 복원’과 ‘수학적 정확한 복원’을 구별해요.** 그림의 500개 복원은 시각적 오차가 작은 근사예요. 모든 벡터의 정확한 복원은 $M=784$에서 보장돼요. 더 적은 축으로도 버린 방향의 성분이 모두 0인 벡터는 정확히 복원되고, 버린 고윳값이 모두 0이면 학습 평균오차가 0이에요.

**학습 평균오차와 테스트 이미지의 오차를 구분해요.** $J_M^\star$는 학습 데이터의 평균오차예요. 그림에서 제시한 테스트 사례의 실제 복원 결과는 원본과 비교해 따로 확인해요.

(b)의 복원 근거로 $J_{784}^\star=0$만 제시하면 학습 평균에 국한돼요. 임의의 벡터에 대한 복원은 $\mathbf B\mathbf B^\top=\mathbf I_{784}$ 항등식으로 보여야 해요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. $M=1, 10, 100, 500$에서 이미지 품질이 단계별로 어떻게 진화하는지 설명해요.
2. $M=784$일 때 $\mathbf B\mathbf B^\top=\mathbf I$를 이용해 $\tilde{\mathbf x}=\mathbf x$와 $J_{784}^\star=0$을 유도해요.
3. $J_M^\star$의 단조 감소성과 외곽 픽셀의 특성, 그림 속 테스트 이미지 비교를 연결해 500개 복원의 수준을 설명해요.

**페이지 요약**

#### 떠올릴 개념·공식

복원식은 $\tilde{\mathbf x}=\bar{\mathbf x}+\mathbf B\mathbf B^\top(\mathbf x-\bar{\mathbf x})$, 학습 평균제곱 복원오차는 버려진 고윳값 합 $J_M^\star=\sum_{i=M+1}^{D}\lambda_i$예요.

#### 첫 줄

$J_{784}^\star=\sum_{i=785}^{784}\lambda_i$, $J_{500}^\star=\sum_{i=501}^{784}\lambda_i$를 적어요.

#### 핵심 답

(a) 주성분이 늘수록 흐릿한 평균 형상에서 원본의 세부 획이 선명한 형상으로 복원돼요.

(b) $M=784$이면 $\mathbf B$가 정사각 직교행렬이라 $\mathbf B\mathbf B^\top=\mathbf I$, $\tilde{\mathbf x}=\mathbf x$이고 $J_{784}^\star=0$이에요.

(c) $J_M^\star$는 단조 감소하며 400개 이후 거의 0이고, 그림에서는 500개만으로 네 이미지가 원본과 매우 비슷하게 복원돼요.

#### 검산

784개를 모두 쓰면 $\tilde{\mathbf x}-\mathbf x=\mathbf 0$이에요. 학습 오차는 500개에서 0에 가깝고, 테스트 복원은 그림에서 확인해요.

#### 조건·구분

완전 복원(784)과 시각적 충분(500)을 구분해요. 학습 오차 곡선과 테스트 이미지의 실제 복원 결과를 구분해요.

#### 용어

- **복원(reconstruction)** — 중심화한 이미지의 저차원 좌표 $\mathbf z=\mathbf B^\top(\mathbf x-\bar{\mathbf x})$에서 $\tilde{\mathbf x}=\bar{\mathbf x}+\mathbf B\mathbf z$를 계산해 원래 이미지 좌표의 벡터를 얻는 과정이에요.
- **평균제곱 복원오차(average squared reconstruction error)** — 학습 이미지 $N$장과 복원 벡터 간의 유클리드 제곱 거리 평균 $\frac1N\sum_{n=1}^N\|\mathbf x_n-\tilde{\mathbf x}_n\|^2$이에요. 최솟값은 버려진 고윳값 합 $J_M^\star$예요.
- **정규직교기저(orthonormal basis)** — 크기가 1이고 상호 직교하는 기저예요. 전체 공간 차원만큼 모은 정사각행렬은 $\mathbf B\mathbf B^\top=\mathbf I$를 만족해요.
- **빈 합(empty sum)** — 합산 범위의 시작 인덱스가 종료 인덱스보다 커서 더할 항이 없는 합으로, 수학적으로 0으로 정의돼요.

#### 출제 근거

MML Example 10.4와 그림 10.12, 교과서 338–339쪽(PDF 344–345쪽). 그림 10.13과 식 (10.62)의 설명(약 550개면 학습 데이터 완전 복원, 가장자리 픽셀)은 조건에 문장으로 주어졌어요.

수업: 1104 L06 s8–11(버린 방향의 복원오차, MNIST 사영과 복원).

관련 정리노트: [버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded), [MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)

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

#### 문제를 내 말로 읽어요

**주어진 것:** 가로로 긴 $2\times 3$ 행렬 $\mathbf A=\begin{bmatrix}1&1&0\\0&1&1\end{bmatrix}$이 주어졌어요.

**구할 것:** (a) $\mathbf A^\top\mathbf A$의 고윳값과 단위 고유벡터로 $\mathbf V$를 구하고, (b) 양의 고윳값 제곱근으로 특잇값과 $\mathbf\Sigma$를 조립하며, (c) $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$ 관계식으로 $\mathbf U$를 산출하고, (d) 완성된 세 행렬의 크기(차원)를 명시해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘특잇값 분해(SVD)’라는 단서에서 행렬의 직교 분해 $\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top$를 떠올려요($\mathbf U\in\mathbb R^{m\times m}$, $\mathbf V\in\mathbb R^{n\times n}$은 정사각 직교행렬, $\mathbf\Sigma\in\mathbb R^{m\times n}$).

‘$\mathbf A^\top\mathbf A$의 고유벡터로 $\mathbf V$’라는 관계는 $\mathbf U^\top\mathbf U=\mathbf I$ 성질에서 가운데가 소거되며 유도돼요.

$$
\mathbf A^\top\mathbf A=\mathbf V\mathbf\Sigma^\top\mathbf U^\top\mathbf U\mathbf\Sigma\mathbf V^\top=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top
$$

$\mathbf V$의 열 $\mathbf v_i$를 대입하면 $\mathbf V^\top\mathbf v_i$는 $i$번째 위치만 1인 벡터예요. 따라서 **$\mathbf v_i$는 $\mathbf A^\top\mathbf A$의 고유벡터**이고 고윳값은 $\mathbf\Sigma^\top\mathbf\Sigma$의 $i$번째 대각값이에요. 이 문항의 대각값은 순서대로 $\sigma_1^2,\sigma_2^2,0$이에요.

SVD의 $\mathbf A\mathbf V=\mathbf U\mathbf\Sigma$에서 양의 특잇값에 대응하는 열은 $\mathbf A\mathbf v_i=\sigma_i\mathbf u_i$예요. $\sigma_i>0$인 열에서 이 식을 $\sigma_i$로 나누어요. [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)에서 같은 공식을 다뤘어요.

#### 종이에 쓸 첫 줄

$\mathbf A$의 열끼리 내적하여 대칭행렬 $\mathbf A^\top\mathbf A$를 계산하고 특성다항식을 세우는 3단계 로드맵(1. $\mathbf V$ $\to$ 2. $\mathbf\Sigma$ $\to$ 3. $\mathbf U$)으로 시작해요.

$$
\mathbf A^\top\mathbf A=\begin{bmatrix}1&1&0\\1&2&1\\0&1&1\end{bmatrix},\qquad\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)=0
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** 고윳값은 $3, 1, 0$이며 직교 정규화된 $\mathbf V$는 $3\times 3$ 행렬이에요.

$$
\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)=(1-\lambda)\big[(2-\lambda)(1-\lambda)-1\big]-1\cdot(1-\lambda)
$$

↳ 첫째 행으로 여인수 전개해요

$$
\hphantom{\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)}=(1-\lambda)(\lambda^2-3\lambda)
$$

↳ 공통인수 $(1-\lambda)$로 묶은 뒤, 괄호 안의 $(2-\lambda)(1-\lambda)-2$를 전개해요

$$
\hphantom{\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)}=-\lambda(\lambda-1)(\lambda-3)=0
$$

↳ 인수분해로 세 고윳값을 구해요

고윳값은 큰 순서대로 $\lambda_1=3, \lambda_2=1, \lambda_3=0$이에요. 고유벡터의 성분을 $(x,y,z)^\top$로 놓고 $(\mathbf A^\top\mathbf A-\lambda\mathbf I)(x,y,z)^\top=\mathbf 0$에 각 고윳값을 대입해요.

$\lambda_1=3$을 넣으면 첫째 행과 벡터의 곱은 $(1-3)x+1\cdot y+0\cdot z=-2x+y=0$이에요. 셋째 행의 $y-2z=0$과 함께 풀면 $(1,2,1)^\top$ 방향이에요. 길이 $\sqrt6$으로 나눠요.

$$
\mathbf v_1=\frac{1}{\sqrt6}\begin{bmatrix}1\\2\\1\end{bmatrix}
$$

$\lambda_2=1$: $y=0$, $x+y+z=0$에서 $(1,0,-1)^\top$ 방향이에요. 길이 $\sqrt2$로 나눠요.

$$
\mathbf v_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\0\\-1\end{bmatrix}
$$

$\lambda_3=0$: $x+y=0$, $y+z=0$에서 $(1,-1,1)^\top$ 방향이에요. 길이 $\sqrt3$으로 나눠요.

$$
\mathbf v_3=\frac{1}{\sqrt3}\begin{bmatrix}1\\-1\\1\end{bmatrix},\qquad\mathbf V=\begin{bmatrix}\frac{1}{\sqrt6}&\frac{1}{\sqrt2}&\frac{1}{\sqrt3}\\\frac{2}{\sqrt6}&0&-\frac{1}{\sqrt3}\\\frac{1}{\sqrt6}&-\frac{1}{\sqrt2}&\frac{1}{\sqrt3}\end{bmatrix}
$$

#### (b)

**최종 답 구조:** 특잇값은 양의 고윳값의 제곱근인 $\sigma_1=\sqrt3, \sigma_2=1$이며 $\mathbf\Sigma$는 $2\times 3$ 크기예요.

$$
\sigma_1=\sqrt{\lambda_1}=\sqrt3,\qquad\sigma_2=\sqrt{\lambda_2}=1
$$

$\mathbf\Sigma$는 원 행렬 $\mathbf A$와 동일한 $2\times 3$ 크기로 대각 자리에 $\sigma_1, \sigma_2$를 배치하고 나머지를 0으로 채워요.

$$
\mathbf\Sigma=\begin{bmatrix}\sqrt3&0&0\\0&1&0\end{bmatrix}
$$

#### (c)

**최종 답 구조:** $\mathbf U$는 단위 정규직교 벡터들로 이루어진 $2\times 2$ 정사각행렬이에요.

$\mathbf u_1, \mathbf u_2$를 공식 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$에 대입해 유도해요.

$$
\mathbf A\mathbf v_1=\begin{bmatrix}1&1&0\\0&1&1\end{bmatrix}\frac{1}{\sqrt6}\begin{bmatrix}1\\2\\1\end{bmatrix}=\frac{1}{\sqrt6}\begin{bmatrix}3\\3\end{bmatrix}
$$

↳ 행렬과 첫 고유벡터를 곱해요

$$
\mathbf u_1=\frac{\mathbf A\mathbf v_1}{\sigma_1}=\frac{1}{\sqrt3}\cdot\frac{3}{\sqrt6}\begin{bmatrix}1\\1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}
$$

↳ 특잇값 $\sqrt3$으로 나누어 정규화해요

$$
\mathbf A\mathbf v_2=\begin{bmatrix}1&1&0\\0&1&1\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1\\0\\-1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}
$$

↳ 행렬과 둘째 고유벡터를 곱해요

$$
\mathbf u_2=\frac{\mathbf A\mathbf v_2}{\sigma_2}=\frac{1}{1}\cdot\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}
$$

↳ 특잇값 1로 나누어 확정해요

두 열을 모아 $\mathbf U$를 완성해요($\mathbf u_1^\top\mathbf u_2=0$으로 직교성 만족).

$$
\mathbf U=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}
$$

#### (d)

**최종 답 요약:** $\mathbf U\in\mathbb R^{2\times 2}$, $\mathbf\Sigma\in\mathbb R^{2\times 3}$, $\mathbf V\in\mathbb R^{3\times 3}$이에요.

$\mathbf A$가 $2\times 3$($m=2, n=3$)이므로 출력 공간 기저 $\mathbf U$는 $2\times 2$, 대각 스케일링 $\mathbf\Sigma$는 $2\times 3$, 입력 공간 기저 $\mathbf V$는 $3\times 3$이에요.

행렬곱 크기 정합성은 $(2\times 2)(2\times 3)(3\times 3)=2\times 3$으로 $\mathbf A$의 차원과 정확히 일치해요.

#### 완성 답과 검산

#### (a) 검산

고유벡터 방정식 $(\mathbf A^\top\mathbf A)\mathbf v_i=\lambda_i\mathbf v_i$를 확인해요. $\begin{bmatrix}1&1&0\\1&2&1\\0&1&1\end{bmatrix}\begin{bmatrix}1\\2\\1\end{bmatrix}=\begin{bmatrix}3\\6\\3\end{bmatrix}=3\begin{bmatrix}1\\2\\1\end{bmatrix}$, $\begin{bmatrix}1&1&0\\1&2&1\\0&1&1\end{bmatrix}\begin{bmatrix}1\\0\\-1\end{bmatrix}=\begin{bmatrix}1\\0\\-1\end{bmatrix}=1\begin{bmatrix}1\\0\\-1\end{bmatrix}$, $\begin{bmatrix}1&1&0\\1&2&1\\0&1&1\end{bmatrix}\begin{bmatrix}1\\-1\\1\end{bmatrix}=\begin{bmatrix}0\\0\\0\end{bmatrix}=0\begin{bmatrix}1\\-1\\1\end{bmatrix}$으로 고윳값 $3, 1, 0$이 정확해요.

#### (b) 검산

출력 공간 행렬 $\mathbf A\mathbf A^\top=\begin{bmatrix}2&1\\1&2\end{bmatrix}$의 특성방정식 $(2-\lambda)^2-1=0$의 근도 $\lambda=3, 1$로 $\mathbf A^\top\mathbf A$의 양의 고윳값과 일치해요.

#### (c) 검산

외적 층의 합으로 $\mathbf A$를 직접 복원해요.

$$
\sigma_1\mathbf u_1\mathbf v_1^\top+\sigma_2\mathbf u_2\mathbf v_2^\top=\frac12\begin{bmatrix}1&2&1\\1&2&1\end{bmatrix}+\frac12\begin{bmatrix}1&0&-1\\-1&0&1\end{bmatrix}=\begin{bmatrix}1&1&0\\0&1&1\end{bmatrix}=\mathbf A
$$

원래 행렬 $\mathbf A$와 정확히 일치해요.

#### (d) 검산

정규직교성 $\mathbf U^\top\mathbf U=\mathbf I_2$, $\mathbf V^\top\mathbf V=\mathbf I_3$ 및 유효 랭크 $\operatorname{rank}(\mathbf A)=2$가 특잇값 개수와 완전히 부합해요.

#### 이 문항에서 조심할 점

**같은 양의 특잇값에 대응하는 두 벡터의 부호를 맞춰요.** 왼쪽과 오른쪽 벡터를 따로 구하면 부호가 어긋날 수 있어요. 여기서는 $\sigma_i>0$인 두 열에 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$를 적용해 맞춰요. 셋째 오른쪽 벡터는 $\mathbf A\mathbf v_3=\mathbf 0$의 방향이에요.

**특잇값은 고윳값의 제곱근이에요.** $\sigma_1=3$으로 착각하면 안 돼요. 고윳값 $\lambda_1=3$의 제곱근인 $\sigma_1=\sqrt3$이에요.

$\mathbf\Sigma$는 정사각이 아닌 $\mathbf A$와 같은 $2\times 3$ 행렬이에요. 0열을 빠뜨리지 않도록 주의해요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. $\mathbf A^\top\mathbf A$를 계산하고 첫째 행 여인수 전개로 특성방정식을 풀어 고윳값 $3, 1, 0$과 단위 고유벡터들을 구해요.
2. 양의 고윳값 제곱근으로 $\sigma_1, \sigma_2$를 구하고 $2\times 3$ $\mathbf\Sigma$를 조립해요.
3. $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 $\mathbf u_1, \mathbf u_2$를 산출하고 외적 층 합으로 $\mathbf A$ 복원을 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mathbf V$의 각 열은 $\mathbf A^\top\mathbf A$의 고유벡터이고, 고윳값은 $\mathbf\Sigma^\top\mathbf\Sigma$의 대응 대각값이에요. $\sigma_i>0$이면 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$예요.

$$
\mathbf A^\top\mathbf A=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top
$$

#### 첫 줄

$\mathbf A^\top\mathbf A=\begin{bmatrix}1&1&0\\1&2&1\\0&1&1\end{bmatrix}$을 적고 특성방정식을 세워요.

#### 핵심 답

(a) 고윳값 $3, 1, 0$, $\mathbf v_1=\frac{1}{\sqrt6}(1,2,1)^\top, \mathbf v_2=\frac{1}{\sqrt2}(1,0,-1)^\top, \mathbf v_3=\frac{1}{\sqrt3}(1,-1,1)^\top$이에요.

(b) $\sigma_1=\sqrt3, \sigma_2=1$, $\mathbf\Sigma=\begin{bmatrix}\sqrt3&0&0\\0&1&0\end{bmatrix}$이에요.

(c) $\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top, \mathbf u_2=\frac{1}{\sqrt2}(1,-1)^\top$, $\mathbf U=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}$이에요.

(d) $\mathbf U$는 $2\times 2$, $\mathbf\Sigma$는 $2\times 3$, $\mathbf V$는 $3\times 3$이에요.

#### 검산

외적 층의 합 $\frac12\begin{bmatrix}1&2&1\\1&2&1\end{bmatrix}+\frac12\begin{bmatrix}1&0&-1\\-1&0&1\end{bmatrix}=\mathbf A$로 일치해요.

#### 조건·구분

$\mathbf u_i$ 부호는 $\mathbf v_i$에 의해 결정돼요. $\mathbf\Sigma$의 차원은 $\mathbf A$와 동일해요.

#### 용어

- **특잇값 분해(singular value decomposition, SVD)** — 임의의 행렬을 $\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top$ 형태로 직교 분해하는 기법이에요.
- **특잇값(singular value)** — 양의 특잇값은 $\mathbf A^\top\mathbf A$와 $\mathbf A\mathbf A^\top$의 공통 양의 고윳값의 제곱근이에요.
- **오른쪽 특이벡터(right-singular vector)** — $\mathbf A^\top\mathbf A$의 단위 고유벡터들로 $\mathbf V$의 열을 구성해요.
- **왼쪽 특이벡터(left-singular vector)** — $\mathbf A\mathbf A^\top$의 단위 고유벡터들로, 양의 특잇값에 해당하는 열은 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 구해요.

#### 출제 근거

MML Example 4.13(수치를 바꾼 변형), 교과서 125–126쪽(PDF 131–132쪽).

수업: 1104 L06 s13(데이터 행렬의 SVD), 1102 특성다항식·스펙트럼 정리.

관련 정리노트: [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

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

#### 문제를 내 말로 읽어요

**주어진 것:** $4\times 3$ 영화 평점 행렬 $\mathbf A$(행: Star Wars, Blade Runner, Amelie, Delicatessen / 열: Ali, Beatrix, Chandra), 특잇값 $\sigma_1=9.6438, \sigma_2=6.3639, \sigma_3=0.7056$, 그리고 $\mathbf u_1, \mathbf u_2$ 및 $\mathbf v_1, \mathbf v_2$의 표가 주어졌어요.

**구할 것:** (a) 첫째 층의 Chandra 열 4개 값, (b) 랭크 2 근사 $\hat{\mathbf A}(2)$의 Chandra 열과 실제 평점 $(1,0,5,4)^\top$ 비교, (c) 셋째 층을 버려도 되는지 Frobenius 제곱오차 비율로 판정해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘층 $\sigma_i\mathbf u_i\mathbf v_i^\top$의 합’이라는 단서에서 SVD의 **외적 층 전개**를 떠올려요.

$$
\mathbf A=\sigma_1\mathbf u_1\mathbf v_1^\top+\sigma_2\mathbf u_2\mathbf v_2^\top+\sigma_3\mathbf u_3\mathbf v_3^\top
$$

‘Chandra 열’이라는 단서에서 **외적 행렬의 열 벡터 추출**을 떠올려요. $\mathbf u\mathbf v^\top$의 $j$번째 열은 스칼라 $v_j$가 곱해진 $v_j\mathbf u$예요. Chandra는 셋째 관객($j=3$)이므로 $i$번째 층의 Chandra 열은 $\sigma_i v_{i,3}\mathbf u_i$예요.

‘버려도 되는지’라는 단서에서는 **Frobenius 제곱오차**를 떠올려요. 랭크 2 근사를 취할 때 버려진 오차의 총합은 버려진 특잇값 제곱합과 같아요.

$$
\|\mathbf A-\hat{\mathbf A}(2)\|_F^2=\sum_{i>2}\sigma_i^2=\sigma_3^2
$$

에카르트–영 정리(Eckart–Young theorem)에 의해 상위 2개 층의 합이 최적 랭크 2 근사예요. [작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)에서 같은 공식을 다뤘어요.

#### 종이에 쓸 첫 줄

$\mathbf v_1$의 Chandra 성분($v_{1,3}=-0.1811$)에 $\sigma_1$을 곱해 스케일링 계수를 먼저 구하는 3단계 로드맵(1. 첫째 층 계산 $\to$ 2. 둘째 층 합산 $\to$ 3. 잔여 오차율 비교)으로 시작해요.

$$
\sigma_1 v_{1,3} = 9.6438 \times (-0.1811) \approx -1.7465
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** 첫째 층의 Chandra 열은 $(1.1719, 1.2570, 0.1640, 0.2646)^\top$이에요.

대표 1항 예시: Star Wars의 첫째 층 평점은 $(-1.74649)\times(-0.6710)\approx 1.1719$예요. 전체 영화의 계산 과정을 표로 정리해요.

| 영화 | $\mathbf u_1$ 성분 | 계산식 ($-1.7465 \times u_{1,i}$) | 첫째 층 Chandra 평점 | 실제 평점 |
|---|---|---|---|---|
| Star Wars | $-0.6710$ | $(-1.74649)\times(-0.6710)$ | $1.1719$ | $1$ |
| Blade Runner | $-0.7197$ | $(-1.74649)\times(-0.7197)$ | $1.2570$ | $0$ |
| Amelie | $-0.0939$ | $(-1.74649)\times(-0.0939)$ | $0.1640$ | $5$ |
| Delicatessen | $-0.1515$ | $(-1.74649)\times(-0.1515)$ | $0.2646$ | $4$ |

결과 해석: Chandra 열에서 첫째 층만 남기면 앞의 두 영화에서 값이 상대적으로 크고, Amelie와 Delicatessen의 높은 실제 평점은 거의 복원되지 않아요.

#### (b)

**최종 답 요약:** $\hat{\mathbf A}(2)$의 Chandra 열은 $(1.0246, -0.0250, 4.9727, 4.0280)^\top$로 실제 평점 $(1, 0, 5, 4)^\top$과 0.03 이내로 거의 완벽히 일치해요.

둘째 층 계수는 $\sigma_2 v_{2,3}=6.3639\times(-0.9807)\approx -6.2411$이에요. 대표 1항 예시: Blade Runner의 랭크 2 근사는 $1.2569504 + (-1.2819172) \approx -0.0250$이에요. 두 층의 합산과 실제 평점 비교를 표로 정리해요.

| 영화 | 첫째 층 평점 | 둘째 층 평점 ($-6.2411\times u_{2,i}$) | 랭크 2 근사 합 $\hat{\mathbf A}(2)$ | 실제 평점 | 잔차 오차 |
|---|---|---|---|---|---|
| Star Wars | $1.1719$ | $(-6.24107)\times 0.0236 = -0.1473$ | $1.0246$ | $1$ | $+0.0246$ |
| Blade Runner | $1.2570$ | $(-6.24107)\times 0.2054 = -1.2819$ | $-0.0250$ | $0$ | $-0.0250$ |
| Amelie | $0.1640$ | $(-6.24107)\times(-0.7705) = 4.8087$ | $4.9727$ | $5$ | $-0.0273$ |
| Delicatessen | $0.2646$ | $(-6.24107)\times(-0.6030) = 3.7634$ | $4.0280$ | $4$ | $+0.0280$ |

결과 해석: 둘째 층에서 Amelie와 Delicatessen 값이 크게 늘고 Blade Runner 값이 줄어 Chandra의 실제 평점 $(1, 0, 5, 4)^\top$를 거의 그대로 되살려요.

#### (c)

**최종 답 구조:** 버려진 셋째 층의 Frobenius 제곱오차는 $\sigma_3^2\approx 0.4979$로 전체 제곱합 134의 약 $0.37\%$에 불과하므로 셋째 층을 버려도 돼요.

앞의 두 층을 남기고 셋째 층을 버릴 때의 Frobenius 제곱오차를 계산해요.

$$
\|\mathbf A-\hat{\mathbf A}(2)\|_F^2=\sigma_3^2=0.7056^2\approx 0.4979
$$

원 행렬 $\mathbf A$의 원소 제곱합(전체 에너지)은 다음과 같아요.

$$
\|\mathbf A\|_F^2=(25+16+1)+(25+25+0)+(0+0+25)+(1+0+16)=134
$$

전체 대비 손실 비율을 구해요.

$$
\frac{\sigma_3^2}{\|\mathbf A\|_F^2}=\frac{0.4979}{134}\approx 0.003716 \approx 0.37\%
$$

따라서 전체 Frobenius 제곱노름의 약 0.37%가 잔차에 남고 약 99.63%가 앞 두 층에 남아요. 이 오차 척도에서는 셋째 층을 생략해도 근사가 좋아요.

#### 완성 답과 검산

#### (a) 검산

교과서 식 (4.100b)의 외적 정규화 열 $(0.1215, 0.1303, 0.0170, 0.0274)^\top$에 $\sigma_1=9.6438$을 곱하면 $(1.1717, 1.2566, 0.1639, 0.2642)^\top$으로 반올림 오차 범위 내에서 일치해요.

#### (b) 검산

교과서 식 (4.102)의 랭크 2 근사 Chandra 열 $(1.0244, -0.0250, 4.9724, 4.0278)^\top$과 대조할 때 표시값 기준 최대 0.0003만큼 다르며 실제 평점과의 차이가 모두 0.03 미만이에요.

#### (c) 검산

세 특잇값의 제곱합 $\sigma_1^2+\sigma_2^2+\sigma_3^2 \approx 93.003 + 40.499 + 0.498 = 134.000$으로 소수 셋째 자리까지 반올림하면 134.000이에요. 반올림 전의 특잇값을 쓰면 원 행렬 원소 제곱합 134와 같아요.

#### 이 문항에서 조심할 점

**외적에서 행과 열의 역할을 뒤바꾸지 않아요.** $i$번째 층의 Chandra 열은 $\sigma_i v_{i,3}\mathbf u_i$예요. 같은 층의 셋째 행 $\sigma_i u_{i,3}\mathbf v_i^\top$은 Amelie의 관객별 성분이에요.

**스케일링 인자 $\sigma_i$를 빠뜨리지 않아요.** 외적 $\mathbf u_i\mathbf v_i^\top$은 방향을 나타내고 $\sigma_i$를 곱해야 그 층의 크기가 반영돼요.

**오차 비율 계산 시 노름과 제곱합 단위를 일치시켜요.** 오차 $\sigma_3^2$을 전체 제곱합 134로 나누어야 유효한 비율이 돼요. 제곱하지 않은 $\sigma_3=0.7056$을 134로 나누면 왜곡이 발생해요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. 외적 $\sigma_1\mathbf u_1\mathbf v_1^\top$의 셋째 열 공식 $\sigma_1 v_{1,3}\mathbf u_1$을 종이에 세우고 4개 영화 값을 계산해요.
2. 둘째 층을 같은 방식으로 구해 더하고 실제 평점 $(1,0,5,4)^\top$과의 오차를 표로 확인해요.
3. $\|\mathbf A-\hat{\mathbf A}(2)\|_F^2=\sigma_3^2$를 $\|\mathbf A\|_F^2=134$로 나누어 손실률 0.37%를 도출해요.

**페이지 요약**

#### 떠올릴 개념·공식

$i$번째 층 $\sigma_i\mathbf u_i\mathbf v_i^\top$의 $j$번째 열은 $\sigma_i v_{i,j}\mathbf u_i$예요. 오차는 버려진 특잇값 제곱합이에요.

$$
\|\mathbf A-\hat{\mathbf A}(2)\|_F^2=\sigma_3^2
$$

#### 첫 줄

$\sigma_1\times(-0.1811)\approx -1.7465$를 먼저 계산해요.

#### 핵심 답

(a) 첫째 층 평점 $(1.1719, 1.2570, 0.1640, 0.2646)^\top$이에요.

(b) 랭크 2 근사는 $(1.0246, -0.0250, 4.9727, 4.0280)^\top$로 실제 평점과 거의 같아요.

(c) 오차 $\sigma_3^2\approx 0.4979$가 전체 134의 0.37%에 불과해 셋째 층을 버려도 무방해요.

#### 검산

교과서 식 (4.100b), (4.102)와 부합하며, 특잇값 제곱합 $\sum\sigma_i^2=134$와 일치해요.

#### 조건·구분

$i$번째 층의 열에는 $\sigma_i$와 $\mathbf v_i$의 해당 성분을 $\mathbf u_i$에 곱해요. 제곱오차는 전체 제곱합과 비교해요.

#### 용어

- **랭크 1 층(rank-1 matrix)** — 열벡터와 행벡터의 외적 $\sigma_i\mathbf u_i\mathbf v_i^\top$로 만들어진 랭크 1 행렬이에요.
- **랭크 2 근사(rank-2 approximation)** — 상위 2개 외적 층을 합산한 근사 행렬 $\hat{\mathbf A}(2)=\sigma_1\mathbf u_1\mathbf v_1^\top+\sigma_2\mathbf u_2\mathbf v_2^\top$이에요.
- **Frobenius 노름(Frobenius norm)** — 행렬 원소들의 제곱합의 제곱근 $\|\mathbf M\|_F=\sqrt{\sum_{ij}M_{ij}^2}$이에요.
- **에카르트–영 정리(Eckart–Young theorem)** — SVD의 상위 $M$개 층을 합한 근사 행렬이 랭크 $M$ 이하 행렬 중 Frobenius 오차를 최소화한다는 정리예요.

#### 출제 근거

MML Example 4.15(그림 4.10, Example 4.14의 평점표와 SVD), 교과서 127쪽·132–133쪽(PDF 133쪽·138–139쪽), 식 (4.100)–(4.103).

수업: 1104 L06 s14(랭크 제한 복원과 Frobenius 오차, 에카르트–영 정리).

관련 정리노트: [작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)

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

#### 문제를 내 말로 읽어요

**주어진 것:** 벡터공간 $V$, 선형사상 $\pi:V\to V$, 항등사상 $\mathrm{id}_V$, 그리고 사영(projection)의 정의 $\rho\circ\rho=\rho$(멱등성, idempotence)가 주어졌어요.

**구할 것:** (a) $\pi$가 사영이면 $\mathrm{id}_V-\pi$ 역시 사영임을 증명하고, (b) 반대로 $\mathrm{id}_V-\pi$가 사영이면 $\pi$도 사영임을 (a)의 결과를 재사용하여 증명해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘사영(projection)’이라는 단서에서 **두 번 적용해도 결과가 불변인 멱등성**을 떠올려요.

$$
\rho\ \text{가 사영} \iff \rho\circ\rho = \rho \iff \rho(\rho(\mathbf x)) = \rho(\mathbf x)\quad (\forall \mathbf x\in V)
$$

‘선형사상’이라는 단서에서 덧셈과 스칼라배를 보존하는 성질 $\pi(\mathbf a - \mathbf b) = \pi(\mathbf a) - \pi(\mathbf b)$를 떠올려요. 이 성질이 있어야 사상의 합성 괄호를 자유롭게 풀 수 있어요.

‘사상의 상등’은 임의의 벡터 $\mathbf x\in V$에 대해 출력이 일치함을 보이는 방식으로 증명해요. PCA에서 투영 $\mathbf P=\mathbf B\mathbf B^\top$과 버려진 여공간 투영 $\mathbf I - \mathbf B\mathbf B^\top$이 이에 대응돼요. [기저를 고정하고 좌표 구하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-projection)와 [버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded)에서 같은 구조를 다뤘어요.

#### 종이에 쓸 첫 줄

$I=\mathrm{id}_V$로 표기하고 임의의 $\mathbf x\in V$에 $(I-\pi)$를 연속 2회 적용하는 합성식을 적는 2단계 로드맵(1. 선형성 전개 $\to$ 2. $\pi^2=\pi$ 대입)으로 시작해요.

$$
(I-\pi)\big((I-\pi)(\mathbf x)\big)=(I-\pi)\big(\mathbf x-\pi(\mathbf x)\big)
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** $(I-\pi)\circ(I-\pi)=I-\pi$가 모든 벡터에 대해 성립하므로 $\mathrm{id}_V-\pi$는 사영이에요.

임의의 $\mathbf x\in V$에 대해 등호 연쇄를 전개해요.

$$
(I-\pi)\big((I-\pi)(\mathbf x)\big)=(I-\pi)\big(\mathbf x-\pi(\mathbf x)\big)
$$

↳ 안쪽 사상 $(I-\pi)$를 적용해요

$$
\hphantom{(I-\pi)\big((I-\pi)(\mathbf x)\big)}=\big(\mathbf x-\pi(\mathbf x)\big)-\pi\big(\mathbf x-\pi(\mathbf x)\big)
$$

↳ 바깥쪽 사상 $(I-\pi)$를 전개해요

$$
\hphantom{(I-\pi)\big((I-\pi)(\mathbf x)\big)}=\mathbf x-\pi(\mathbf x)-\pi(\mathbf x)+\pi(\pi(\mathbf x))
$$

↳ 사상 $\pi$의 선형성으로 전개해요

$$
\hphantom{(I-\pi)\big((I-\pi)(\mathbf x)\big)}=\mathbf x-2\pi(\mathbf x)+\pi(\mathbf x)
$$

↳ 가정인 멱등성 $\pi^2=\pi$를 대입해요

$$
\hphantom{(I-\pi)\big((I-\pi)(\mathbf x)\big)}=\mathbf x-\pi(\mathbf x)=(I-\pi)(\mathbf x)
$$

↳ 동류항을 정리해 멱등성을 얻어요

모든 $\mathbf x\in V$에서 $(I-\pi)^2(\mathbf x)=(I-\pi)(\mathbf x)$이므로 **$\mathrm{id}_V-\pi$는 사영이에요.**

#### (b)

**최종 답 구조:** $\rho=\mathrm{id}_V-\pi$로 두고 (a)의 명제를 이 사상에 적용하면 $\mathrm{id}_V-\rho=\pi$ 역시 사영이에요.

새로운 선형사상 $\rho = \mathrm{id}_V-\pi$를 정의해요. 가정에 따라 $\rho$는 사영이에요. (a)에서 증명한 일반 원리 ‘임의의 선형사상 $T$가 사영이면 $\mathrm{id}_V-T$도 사영이다’에 $T=\rho$를 대입해요. 두 단계의 대응 관계를 표로 정리해요.

| 단계 / 구성 요소 | (a)의 증명 논리 | (b)에서 대입할 대상 ($\rho=\mathrm{id}_V-\pi$) | 대응 결과 |
|---|---|---|---|
| 출발 사상 | $\pi$ (선형사상) | $\rho = \mathrm{id}_V-\pi$ (두 선형사상의 차) | $\rho$ 역시 $V\to V$ 선형사상임 |
| 가정 조건 | $\pi$가 사영임 | $\rho$가 사영임 ((b)의 전제 조건) | (a)의 적용 전제 완벽 충족 |
| (a)의 정리 적용 | $\mathrm{id}_V-\pi$가 사영임 | $\mathrm{id}_V-\rho$가 사영임 | (a)의 논리에 의해 즉시 성립 |
| 원래 기호 환원 | — | $\mathrm{id}_V-(\mathrm{id}_V-\pi)=\pi$ | **$\pi$는 사영임** 도출 완료 |

따라서 (a)를 그대로 적용해 식을 정리하면 $\mathrm{id}_V-\rho = \mathrm{id}_V-(\mathrm{id}_V-\pi) = \pi$가 되므로 **$\pi$ 역시 사영이에요.** (a)와 (b)가 합쳐져 $\pi$가 사영인 것과 $\mathrm{id}_V-\pi$가 사영인 것은 동치(필요충분조건)예요.

#### 완성 답과 검산

#### (a) 검산

증명의 각 단계를 검토해요. 3번째 줄은 오직 $\pi$의 선형성만, 4번째 줄은 $\pi(\pi(\mathbf x))=\pi(\mathbf x)$만 사용했어요. 특정 차원이나 기저에 의존하지 않는 일반 연산자 대수 증명이므로 완벽해요.

#### (b) 검산

순환 논리 없이 (a)의 보편 명제($\forall T, T^2=T \implies (I-T)^2=I-T$)에 $T=\rho$를 대입했으므로 논리적 비약 없이 정확해요.

#### 이 문항에서 조심할 점

**교차항 $-2\pi(\mathbf x)$를 빠뜨리지 않아요.** $(I-\pi)^2$을 단순 전개할 때 $I^2-\pi^2$처럼 잘못 전개하면 안 돼요. 사상의 합성은 분배법칙을 통해 $-2\pi$ 교차항이 반드시 등장해요.

**한쪽 방향 증명만으로 동치를 주장할 수 없어요.** (a)는 ‘$\pi \implies I-\pi$’만을 보였으므로, 반대 방향인 (b) ‘$I-\pi \implies \pi$’를 반드시 치환을 통해 별도로 입증해야 해요.

특정 행렬이나 수치 예시는 보조적 직관일 뿐 일반 증명을 대체할 수 없어요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. $(I-\pi)((I-\pi)(\mathbf x))$에 선형성을 적용해 $\mathbf x-2\pi(\mathbf x)+\pi(\pi(\mathbf x))$로 전개해요.
2. $\pi(\pi(\mathbf x))=\pi(\mathbf x)$를 대입해 $(I-\pi)(\mathbf x)$가 됨을 보여요.
3. $\rho=\mathrm{id}_V-\pi$로 두고 (a)의 정리를 이 사상에 적용하여 $\pi$가 사영임을 마무리해요.

**페이지 요약**

#### 떠올릴 개념·공식

사영의 정의는 멱등성 $\rho\circ\rho=\rho$예요. 선형성 분배로 합성식을 전개해요.

#### 첫 줄

$(I-\pi)\big((I-\pi)(\mathbf x)\big)=(I-\pi)\big(\mathbf x-\pi(\mathbf x)\big)$로 시작해요.

#### 핵심 답

(a) 선형성 전개와 $\pi^2=\pi$ 대입으로 $(I-\pi)^2=I-\pi$를 얻어 사영이에요.

(b) $\rho=\mathrm{id}_V-\pi$에 (a)를 적용하면 $\mathrm{id}_V-\rho=\pi$가 사영이에요.

#### 검산

연산자 분배 및 멱등성 조건만 사용해 임의의 공간에서 엄밀히 성립해요.

#### 조건·구분

교차항 $-2\pi$를 정확히 보존해요. (a)와 (b) 양방향을 분리 증명해요.

#### 용어

- **선형사상(linear map)** — 벡터 덧셈과 스칼라 곱을 보존하는 사상 $\pi(c\mathbf a+\mathbf b)=c\pi(\mathbf a)+\pi(\mathbf b)$예요.
- **항등사상(identity map)** — 모든 벡터를 자기 자신으로 보내는 사상 $\mathrm{id}_V(\mathbf x)=\mathbf x$예요.
- **사영(projection)** — 두 번 합성해도 결과가 같은 멱등 사상 $\rho\circ\rho=\rho$예요.
- **멱등성(idempotence)** — 연산을 여러 번 거듭 적용해도 최초 1회 적용한 결과와 동일한 대수적 성질이에요.

#### 출제 근거

MML Exercise 3.7, 교과서 97쪽(PDF 103쪽). 원문 (a)의 ‘필요충분’ 주장을 두 방향 (a), (b)로 나눴어요. 원문 (b)는 이 문항에 들어 있지 않아요.

수업: 1019 사영행렬 $\mathbf P^2=\mathbf P$, 1104 L06 s5–10(사영과 버린 부분).

관련 정리노트: [기저를 고정하고 좌표 구하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-projection), [버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded)

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

#### 문제를 내 말로 읽어요

**주어진 것:** $2\times 3$ 행렬 $\mathbf A=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}$이 주어졌어요.

**구할 것:** 크기가 작은 쪽인 $\mathbf A\mathbf A^\top$($2\times 2$)에서 출발해 (a) $\sigma_1, \sigma_2$와 $\mathbf u_1, \mathbf u_2$를 구하고, (b) $\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i$로 $\mathbf v_1, \mathbf v_2$를 구하며, (c) 직교 조건으로 $\mathbf v_3$를 채워 $\mathbf V$를 완성하고, (d) $\mathbf A\mathbf v_3=\mathbf 0$과 $\mathbf\Sigma$의 셋째 열(0열)의 정합성을 판정해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘$\mathbf A\mathbf A^\top$의 고유벡터로 $\mathbf u_i$’라는 단서에서 SVD 분해식을 $\mathbf A\mathbf A^\top$에 대입해요($\mathbf V^\top\mathbf V=\mathbf I$).

$$
\mathbf A\mathbf A^\top=\mathbf U\mathbf\Sigma\mathbf V^\top\mathbf V\mathbf\Sigma^\top\mathbf U^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top
$$

$\mathbf\Sigma\mathbf\Sigma^\top$는 대각이 $\sigma_1^2, \sigma_2^2$인 대각행렬이므로 **$\mathbf U$의 열 $\mathbf u_i$는 $\mathbf A\mathbf A^\top$의 단위 고유벡터이고 고윳값은 $\sigma_i^2$**예요.

전치 관계식 $\mathbf A^\top\mathbf U=\mathbf V\mathbf\Sigma^\top$의 양의 특잇값에 대응하는 열을 읽으면 $\mathbf A^\top\mathbf u_i=\sigma_i\mathbf v_i$예요. $\sigma_i>0$인 열을 $\sigma_i$로 나누어요.

‘모두 수직인 단위벡터 $\mathbf v_3$’는 $\mathbf V\in\mathbb R^{3\times 3}$가 정규직교행렬이어야 하므로 내적 0 조건($\mathbf v_1^\top\mathbf v_3=0, \mathbf v_2^\top\mathbf v_3=0, \|\mathbf v_3\|=1$)으로 결정돼요. [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)에서 같은 공식을 다뤘어요.

#### 종이에 쓸 첫 줄

$\mathbf A$의 두 행끼리 내적하여 대칭행렬 $\mathbf A\mathbf A^\top$를 적고 특성방정식을 세우는 4단계 로드맵(1. $\mathbf U,\mathbf\Sigma$ $\to$ 2. $\mathbf v_1,\mathbf v_2$ $\to$ 3. $\mathbf v_3$ $\to$ 4. 영공간 점검)으로 시작해요.

$$
\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix},\qquad\det(\mathbf A\mathbf A^\top-\lambda\mathbf I)=0
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** 특잇값은 $\sigma_1=5, \sigma_2=3$이고 $\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top, \mathbf u_2=\frac{1}{\sqrt2}(1,-1)^\top$이에요.

특성다항식을 세우고 인수분해해요.

$$
\det(\mathbf A\mathbf A^\top-\lambda\mathbf I)=(17-\lambda)^2-8^2=0
$$

↳ 행렬식 $ad-bc$를 계산해요

$$
\hphantom{\det(\mathbf A\mathbf A^\top-\lambda\mathbf I)}=(17-\lambda-8)(17-\lambda+8)=(9-\lambda)(25-\lambda)=0
$$

↳ 합차 공식으로 인수분해해요

$$
\lambda_1=25 \implies \sigma_1=5, \qquad \lambda_2=9 \implies \sigma_2=3
$$

↳ 양의 제곱근으로 특잇값을 구해요

고유벡터의 후보를 $\mathbf w=(x,y)^\top$로 두고 $(\mathbf A\mathbf A^\top-\lambda\mathbf I)\mathbf w=\mathbf 0$을 풀어요. $\lambda_1=25$를 대입한 첫째 행은 $(17-25)x+8y=0$이어서 $y=x$예요. $\lambda_2=9$에서는 $(17-9)x+8y=0$이어서 $y=-x$예요. 두 방향 벡터를 길이 $\sqrt2$로 나누어요.

$$
\mathbf u_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},\qquad\mathbf u_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}
$$

#### (b)

**최종 답 구조:** $\mathbf v_1=\frac{1}{\sqrt2}(1,1,0)^\top, \mathbf v_2=\frac{1}{3\sqrt2}(1,-1,4)^\top$이에요.

공식 $\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i$로 유도해요.

$$
\mathbf A^\top\mathbf u_1=\begin{bmatrix}3&2\\2&3\\2&-2\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}5\\5\\0\end{bmatrix}
$$

↳ $\mathbf A^\top$와 $\mathbf u_1$을 곱해요

$$
\mathbf v_1=\frac{\mathbf A^\top\mathbf u_1}{\sigma_1}=\frac{1}{5\sqrt2}\begin{bmatrix}5\\5\\0\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\\0\end{bmatrix}
$$

↳ 특잇값 5로 나누어 확정해요

$$
\mathbf A^\top\mathbf u_2=\begin{bmatrix}3&2\\2&3\\2&-2\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\\4\end{bmatrix}
$$

↳ $\mathbf A^\top$와 $\mathbf u_2$를 곱해요

$$
\mathbf v_2=\frac{\mathbf A^\top\mathbf u_2}{\sigma_2}=\frac{1}{3\sqrt2}\begin{bmatrix}1\\-1\\4\end{bmatrix}
$$

↳ 특잇값 3으로 나누어 확정해요

$\mathbf v_1^\top\mathbf v_2 \propto 1-1+0=0$으로 직교성을 만족해요.

#### (c)

**최종 답 구조:** $\mathbf v_3=\frac13(2,-2,-1)^\top$이며 완성된 $\mathbf V$는 $3\times 3$ 정규직교행렬이에요.

$\mathbf v_3\propto (a,b,c)^\top$로 두고 직교 조건을 세워요.

$$
(1,1,0)\cdot(a,b,c)=a+b=0,\qquad(1,-1,4)\cdot(a,b,c)=a-b+4c=0
$$

$b=-a$를 둘째 식에 대입하면 $2a+4c=0 \implies c=-a/2$예요. 정수비로 $a=2$로 두면 $(2,-2,-1)^\top$이고 길이는 $\sqrt{4+4+1}=3$이에요.

$$
\mathbf v_3=\frac13\begin{bmatrix}2\\-2\\-1\end{bmatrix},\qquad\mathbf V=\begin{bmatrix}\frac{1}{\sqrt2}&\frac{1}{3\sqrt2}&\frac23\\\frac{1}{\sqrt2}&-\frac{1}{3\sqrt2}&-\frac23\\0&\frac{4}{3\sqrt2}&-\frac13\end{bmatrix}
$$

#### (d)

**최종 답 요약:** $\mathbf A\mathbf v_3=\mathbf 0$이며 이는 $\mathbf\Sigma$의 셋째 열 $\mathbf 0$과 정확히 부합해요.

$\mathbf A\mathbf v_3$의 행렬곱을 직접 계산해요.

$$
\mathbf A\mathbf v_3=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}\frac13\begin{bmatrix}2\\-2\\-1\end{bmatrix}=\frac13\begin{bmatrix}6-4-2\\4-6+2\end{bmatrix}
$$

↳ 행렬과 셋째 특이벡터를 곱해요

$$
\hphantom{\mathbf A\mathbf v_3}=\begin{bmatrix}0\\0\end{bmatrix}=\mathbf 0
$$

↳ 계산 결과 영벡터가 돼요

$\mathbf\Sigma=\begin{bmatrix}5&0&0\\0&3&0\end{bmatrix}$의 셋째 열은 $\mathbf 0$이에요. SVD 관계식 $\mathbf A\mathbf V=\mathbf U\mathbf\Sigma$의 셋째 열을 읽으면 $\mathbf A\mathbf v_3=\mathbf U\cdot\mathbf 0=\mathbf 0$이므로 **$\mathbf A\mathbf v_3=\mathbf 0$은 $\mathbf\Sigma$의 셋째 열이 0인 구조와 정확히 일치해요.**

#### 완성 답과 검산

#### (a) 검산

$\mathbf A\mathbf A^\top\mathbf u_1 = \begin{bmatrix}17&8\\8&17\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}25\\25\end{bmatrix}=25\mathbf u_1$, $\mathbf A\mathbf A^\top\mathbf u_2 = \begin{bmatrix}17&8\\8&17\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}9\\-9\end{bmatrix}=9\mathbf u_2$로 고윳값 $25, 9$가 정확해요.

#### (b) 검산

$\mathbf A\mathbf v_1=\frac{1}{\sqrt2}(3+2, 2+3)^\top=\frac{5}{\sqrt2}(1,1)^\top=5\mathbf u_1$, $\mathbf A\mathbf v_2=\frac{1}{3\sqrt2}(3-2+8, 2-3-8)^\top=\frac{1}{3\sqrt2}(9,-9)^\top=3\mathbf u_2$로 $\mathbf A\mathbf v_i=\sigma_i\mathbf u_i$가 성립해요.

#### (c) 검산

$\mathbf v_1^\top\mathbf v_3\propto 2-2+0=0$, $\mathbf v_2^\top\mathbf v_3\propto 2+2-4=0$, $\|\mathbf v_3\|^2=(4+4+1)/9=1$로 $\mathbf V$가 정규직교행렬이에요.

#### (d) 검산

외적 층의 합으로 $\mathbf A$를 복원해요. $5\mathbf u_1\mathbf v_1^\top+3\mathbf u_2\mathbf v_2^\top=\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}+\frac12\begin{bmatrix}1&-1&4\\-1&1&-4\end{bmatrix}=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}=\mathbf A$로 일치해요.

#### 이 문항에서 조심할 점

**같은 양의 특잇값에 대응하는 두 벡터의 부호를 맞춰요.** 왼쪽과 오른쪽 벡터를 따로 구하면 부호가 어긋날 수 있어요. 여기서는 $i=1,2$에 $\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i$를 적용해 맞춰요.

**$\mathbf v_3$는 $\mathbf A^\top\mathbf u_3/\sigma_3$로 구할 수 없어요.** 특잇값은 2개뿐이므로 $\mathbf v_3$는 영공간/직교 조건으로만 정해져요.

$\mathbf\Sigma$는 $\mathbf A$와 동일한 $2\times 3$ 크기예요. 셋째 열이 0인 것을 놓치지 않아요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. $\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix}$을 구하고 $(17-\lambda)^2-64=0$을 풀어 $\sigma_1, \sigma_2$와 $\mathbf u_1, \mathbf u_2$를 구해요.
2. $\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i$로 $\mathbf v_1, \mathbf v_2$를 산출해요.
3. 내적 0 조건으로 $\mathbf v_3$를 채워 $\mathbf V$를 완성하고 $\mathbf A\mathbf v_3=\mathbf 0$과 $\mathbf\Sigma$의 0열을 연결해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mathbf U$의 각 열은 $\mathbf A\mathbf A^\top$의 고유벡터예요. $\sigma_i>0$이면 $\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i$예요.

$$
\mathbf A\mathbf A^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top
$$

#### 첫 줄

$\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix}$을 적고 시작해요.

#### 핵심 답

(a) $\sigma_1=5, \sigma_2=3$, $\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top, \mathbf u_2=\frac{1}{\sqrt2}(1,-1)^\top$이에요.

(b) $\mathbf v_1=\frac{1}{\sqrt2}(1,1,0)^\top, \mathbf v_2=\frac{1}{3\sqrt2}(1,-1,4)^\top$이에요.

(c) $\mathbf v_3=\frac13(2,-2,-1)^\top$이에요.

(d) $\mathbf A\mathbf v_3=\mathbf 0$으로 $\mathbf\Sigma$의 셋째 열(0열)과 일치해요.

#### 검산

외적 층의 합 $\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}+\frac12\begin{bmatrix}1&-1&4\\-1&1&-4\end{bmatrix}=\mathbf A$로 일치해요.

#### 조건·구분

$\mathbf v_i$ 부호는 $\mathbf u_i$와 연동해요. $\mathbf v_3$는 직교성으로 구해요.

#### 용어

- **왼쪽 특이벡터(left-singular vector)** — $\mathbf A\mathbf A^\top$의 단위 고유벡터들로 $\mathbf U$의 열을 이뤄요.
- **오른쪽 특이벡터(right-singular vector)** — 양의 특잇값에 대응하는 열은 $\mathbf A^\top\mathbf u_i/\sigma_i$로 구해요. 나머지 열은 $\mathbf A$의 영공간에서 정규직교기저를 골라 채워요.
- **특잇값(singular value)** — 양의 특잇값은 $\mathbf A\mathbf A^\top$의 양의 고윳값 제곱근이에요.
- **정규직교행렬(orthogonal matrix)** — 열들이 단위 길이를 갖고 상호 직교하는 정사각행렬이에요.

#### 출제 근거

MML Exercise 4.8, 교과서 138쪽(PDF 144쪽). 원문은 ‘SVD를 구하라’는 한 문장이고, 이 문항은 ${\mathbf A\mathbf A^\top}$에서 시작하는 (a)–(d) 단계로 나눴어요.

수업: 1104 L06 s13(데이터 행렬의 SVD), 1102 특성다항식.

관련 정리노트: [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

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

#### 문제를 내 말로 읽어요

**주어진 것:** $2\times 2$ 비대칭 행렬 $\mathbf A=\begin{bmatrix}2&2\\-1&1\end{bmatrix}$이 주어졌어요.

**구할 것:** (a) $\mathbf A^\top\mathbf A$의 고윳값과 단위 고유벡터로 $\mathbf V$를 구하고, (b) 특잇값과 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 $\mathbf U$를 구하며, (c) $\mathbf A\mathbf A^\top$를 직접 계산해 $\mathbf u_1, \mathbf u_2$가 그 고유벡터이고 고윳값이 $\sigma_i^2$인지 판정해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘$\mathbf A^\top\mathbf A$의 고유벡터로 $\mathbf V$’라는 단서에서 SVD 분해식을 $\mathbf A^\top\mathbf A$에 대입해요($\mathbf U^\top\mathbf U=\mathbf I$).

$$
\mathbf A^\top\mathbf A=\mathbf V\mathbf\Sigma^\top\mathbf U^\top\mathbf U\mathbf\Sigma\mathbf V^\top=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top
$$

$\mathbf\Sigma^\top\mathbf\Sigma=\operatorname{diag}(\sigma_1^2,\sigma_2^2)$이므로 **$\mathbf V$의 열 $\mathbf v_i$는 $\mathbf A^\top\mathbf A$의 단위 고유벡터이고 고윳값은 $\sigma_i^2$**예요.

$\sigma_i>0$일 때 $\mathbf A\mathbf v_i=\sigma_i\mathbf u_i$를 $\sigma_i$로 나누어 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$를 얻어요.

‘$\mathbf A\mathbf A^\top$의 고유벡터 판정’에서는 $\mathbf A\mathbf A^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top$ 관계를 통해 $\mathbf A\mathbf A^\top\mathbf u_i=\sigma_i^2\mathbf u_i$가 성립하는지 고유벡터 정의로 확인해요. [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)에서 같은 공식을 다뤘어요.

#### 종이에 쓸 첫 줄

$\mathbf A$의 두 열끼리 내적하여 대칭행렬 $\mathbf A^\top\mathbf A$를 적고 특성방정식을 세우는 3단계 로드맵(1. $\mathbf V$ $\to$ 2. $\mathbf\Sigma, \mathbf U$ $\to$ 3. $\mathbf A\mathbf A^\top$ 점검)으로 시작해요.

$$
\mathbf A^\top\mathbf A=\begin{bmatrix}5&3\\3&5\end{bmatrix},\qquad\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)=0
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** 고윳값은 $8, 2$이고 $\mathbf V=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}$이에요.

특성방정식을 풀어요.

$$
\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)=(5-\lambda)^2-3^2=0
$$

↳ $ad-bc$로 특성다항식을 세워요

$$
\hphantom{\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)}=(5-\lambda-3)(5-\lambda+3)=(2-\lambda)(8-\lambda)=0
$$

↳ 합차 공식으로 인수분해해요

$$
\lambda_1=8,\qquad\lambda_2=2
$$

↳ 내림차순으로 고윳값을 구해요

고유벡터의 후보를 $\mathbf w=(x,y)^\top$로 두고 $(\mathbf A^\top\mathbf A-\lambda\mathbf I)\mathbf w=\mathbf 0$을 풀어요. $\lambda_1=8$을 대입한 첫째 행은 $(5-8)x+3y=0$이어서 $y=x$예요. $\lambda_2=2$일 때는 $(5-2)x+3y=0$이 되어 $y=-x$예요. 두 방향 벡터를 길이 $\sqrt2$로 나누어요.

$$
\mathbf v_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},\qquad\mathbf v_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix},\qquad\mathbf V=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}
$$

#### (b)

**최종 답 구조:** $\sigma_1=2\sqrt2, \sigma_2=\sqrt2$, $\mathbf U=\begin{bmatrix}1&0\\0&-1\end{bmatrix}$이에요.

특잇값은 고윳값의 양의 제곱근이에요.

$$
\sigma_1=\sqrt8=2\sqrt2,\qquad\sigma_2=\sqrt2,\qquad\mathbf\Sigma=\begin{bmatrix}2\sqrt2&0\\0&\sqrt2\end{bmatrix}
$$

$\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 $\mathbf u_1, \mathbf u_2$를 유도해요.

$$
\mathbf A\mathbf v_1=\begin{bmatrix}2&2\\-1&1\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}4\\0\end{bmatrix}
$$

↳ $\mathbf A$와 첫 고유벡터를 곱해요

$$
\mathbf u_1=\frac{\mathbf A\mathbf v_1}{\sigma_1}=\frac{1}{2\sqrt2}\cdot\frac{1}{\sqrt2}\begin{bmatrix}4\\0\end{bmatrix}=\begin{bmatrix}1\\0\end{bmatrix}
$$

↳ 특잇값 $2\sqrt2$로 나누어 확정해요

$$
\mathbf A\mathbf v_2=\begin{bmatrix}2&2\\-1&1\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}0\\-2\end{bmatrix}
$$

↳ $\mathbf A$와 둘째 고유벡터를 곱해요

$$
\mathbf u_2=\frac{\mathbf A\mathbf v_2}{\sigma_2}=\frac{1}{\sqrt2}\cdot\frac{1}{\sqrt2}\begin{bmatrix}0\\-2\end{bmatrix}=\begin{bmatrix}0\\-1\end{bmatrix}
$$

↳ 특잇값 $\sqrt2$로 나누어 확정해요

두 열을 모아 $\mathbf U=\begin{bmatrix}1&0\\0&-1\end{bmatrix}$을 완성해요($\mathbf u_1^\top\mathbf u_2=0$ 만족).

#### (c)

**최종 답 구조:** $\mathbf A\mathbf A^\top=\operatorname{diag}(8,2)$이므로 $\mathbf u_1, \mathbf u_2$는 고윳값 $\sigma_1^2=8, \sigma_2^2=2$의 고유벡터가 맞아요.

$\mathbf A$의 두 행끼리 내적하여 $\mathbf A\mathbf A^\top$를 직접 계산해요.

$$
\mathbf A\mathbf A^\top=\begin{bmatrix}4+4&-2+2\\-2+2&1+1\end{bmatrix}=\begin{bmatrix}8&0\\0&2\end{bmatrix}
$$

고유벡터 정의식 $(\mathbf A\mathbf A^\top)\mathbf u_i$에 대입해요.

$$
\mathbf A\mathbf A^\top\mathbf u_1=\begin{bmatrix}8&0\\0&2\end{bmatrix}\begin{bmatrix}1\\0\end{bmatrix}=\begin{bmatrix}8\\0\end{bmatrix}=8\mathbf u_1
$$

↳ $\mathbf u_1$이 고윳값 8의 고유벡터예요

$$
\mathbf A\mathbf A^\top\mathbf u_2=\begin{bmatrix}8&0\\0&2\end{bmatrix}\begin{bmatrix}0\\-1\end{bmatrix}=\begin{bmatrix}0\\-2\end{bmatrix}=2\mathbf u_2
$$

↳ $\mathbf u_2$가 고윳값 2의 고유벡터예요

고윳값 8과 2는 $\sigma_1^2=(2\sqrt2)^2=8$, $\sigma_2^2=(\sqrt2)^2=2$와 정확히 일치하므로 **(b)의 $\mathbf u_1, \mathbf u_2$는 $\mathbf A\mathbf A^\top$의 고유벡터이고 고윳값도 $\sigma_i^2$가 맞아요.**

#### 완성 답과 검산

#### (a) 검산

$\mathbf A^\top\mathbf A\mathbf v_1=\begin{bmatrix}5&3\\3&5\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}8\\8\end{bmatrix}=8\mathbf v_1$, $\mathbf A^\top\mathbf A\mathbf v_2=\begin{bmatrix}5&3\\3&5\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}2\\-2\end{bmatrix}=2\mathbf v_2$로 고윳값 $8, 2$가 정확해요.

#### (b) 검산

세 행렬 $\mathbf U\mathbf\Sigma\mathbf V^\top$을 직접 곱해요.

$$
\mathbf U\mathbf\Sigma\mathbf V^\top=\begin{bmatrix}1&0\\0&-1\end{bmatrix}\begin{bmatrix}2\sqrt2&0\\0&\sqrt2\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}=\begin{bmatrix}2\sqrt2&0\\0&-\sqrt2\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}=\begin{bmatrix}2&2\\-1&1\end{bmatrix}=\mathbf A
$$

원래 행렬 $\mathbf A$가 완벽히 복원돼요.

#### (c) 검산

대각화 식 $\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top=\begin{bmatrix}1&0\\0&-1\end{bmatrix}\begin{bmatrix}8&0\\0&2\end{bmatrix}\begin{bmatrix}1&0\\0&-1\end{bmatrix}=\begin{bmatrix}8&0\\0&2\end{bmatrix}=\mathbf A\mathbf A^\top$으로 정확해요.

#### 이 문항에서 조심할 점

**$\mathbf u_i$ 부호를 $\mathbf A\mathbf A^\top$에서 임의로 선택하지 않아요.** $\mathbf A\mathbf A^\top$의 고유벡터로 $(0,1)^\top$을 고를 수도 있지만, $\mathbf u_2=(0,1)^\top$을 쓰면 둘째 층 부호가 반전되어 원래 $\mathbf A$와 다른 행렬이 돼요. 선택한 $\mathbf v_i$를 두고 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 짝을 맞춰요.

**$\mathbf A$ 자체의 고윳값과 특잇값을 혼동하지 않아요.** 이 문항에서는 $\mathbf A^\top\mathbf A$의 고윳값에 제곱근을 취해 특잇값을 구해요. (c)에서 확인하듯 $\mathbf A\mathbf A^\top$에서도 같은 양의 고윳값을 얻어요.

특잇값은 고윳값의 제곱근이에요. $\sigma_1=8$로 쓰지 않도록 주의해요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. $\mathbf A^\top\mathbf A=\begin{bmatrix}5&3\\3&5\end{bmatrix}$을 구하고 $(5-\lambda)^2-9=0$을 풀어 $\mathbf v_1, \mathbf v_2$를 구해요.
2. 특잇값 $2\sqrt2, \sqrt2$를 구하고 $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 $\mathbf U$를 완성해요.
3. $\mathbf A\mathbf A^\top=\operatorname{diag}(8,2)$를 계산하고 $\mathbf A\mathbf A^\top\mathbf u_i=\sigma_i^2\mathbf u_i$를 검증해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mathbf A^\top\mathbf A=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top$, $\mathbf A\mathbf A^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top$이며 고윳값은 $\sigma_i^2$예요.

#### 첫 줄

$\mathbf A^\top\mathbf A=\begin{bmatrix}5&3\\3&5\end{bmatrix}$을 적고 시작해요.

#### 핵심 답

(a) 고윳값 $8, 2$, $\mathbf V=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}$이에요.

(b) $\sigma_1=2\sqrt2, \sigma_2=\sqrt2$, $\mathbf U=\begin{bmatrix}1&0\\0&-1\end{bmatrix}$이에요.

(c) $\mathbf A\mathbf A^\top=\operatorname{diag}(8,2)$라 $\mathbf u_i$는 고윳값 $\sigma_i^2$의 고유벡터가 맞아요.

#### 검산

$\mathbf U\mathbf\Sigma\mathbf V^\top=\mathbf A$로 일치하며, $\mathbf A\mathbf A^\top$ 고유벡터 식도 정확해요.

#### 조건·구분

$\mathbf u_i$ 부호는 $\mathbf v_i$와 연동해요. $\mathbf A$ 자신의 고윳값과 구별해요.

#### 용어

- **특잇값 분해(singular value decomposition, SVD)** — 정사각 행렬에서도 $\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top$ 분해 시 $\mathbf U$와 $\mathbf V$는 일반적으로 서로 달라요.
- **특잇값(singular value)** — 양의 특잇값은 $\mathbf A^\top\mathbf A$ 및 $\mathbf A\mathbf A^\top$의 공통 양의 고윳값 제곱근이에요.
- **고유벡터(eigenvector)** — $\mathbf M\mathbf x=\lambda\mathbf x$를 만족하는 0이 아닌 벡터예요.
- **대각행렬(diagonal matrix)** — 비대각 성분이 0인 정사각행렬로, 표준기저 벡터들이 바로 고유벡터가 돼요.

#### 출제 근거

MML Exercise 4.9, 교과서 138쪽(PDF 144쪽). 원문은 ‘SVD를 구하라’는 한 문장이고, 이 문항은 (a), (b)와 ${\mathbf A\mathbf A^\top}$ 판정 (c)로 나눴어요.

수업: 1104 L06 s13(데이터 행렬의 SVD), 1102 특성다항식.

관련 정리노트: [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

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

#### 문제를 내 말로 읽어요

**주어진 것:** $2\times 3$ 행렬 $\mathbf A=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}$과 Frobenius 제곱노름 정의 $\|\mathbf M\|_F^2=\sum_{ij}M_{ij}^2$이 주어졌어요.

**구할 것:** (a) 가장 큰 특잇값 $\sigma_1$과 대응하는 단위 특이벡터 $\mathbf u_1, \mathbf v_1$을 구하고, (b) 랭크 1 근사 행렬 $\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top$을 계산하며, (c) 잔차 행렬 $\mathbf A-\mathbf A_1$의 Frobenius 제곱오차가 버려진 특잇값 제곱 $\sigma_2^2$와 일치하는지 판정해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘랭크 1 근사’라는 단서에서 SVD 외적 층 전개의 **첫째 주성분 층**을 떠올려요.

$$
\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top
$$

에카르트–영 정리(Eckart–Young theorem)에 의해 이 행렬이 랭크 1 이하의 모든 행렬 중 원래 행렬과의 원소 제곱오차를 최소화해요.

‘$\mathbf A-\mathbf A_1$의 원소 제곱합’이라는 단서에서는 **버려진 특잇값들의 제곱합 공식**을 떠올려요.

$$
\|\mathbf A-\mathbf A_1\|_F^2=\sum_{i>1}\sigma_i^2=\sigma_2^2
$$

$\mathbf u_1$은 $\mathbf A\mathbf A^\top$의 가장 큰 고윳값에 대응하는 단위 고유벡터, $\mathbf v_1$은 $\mathbf A^\top\mathbf u_1/\sigma_1$로 결정돼요. [작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)에서 같은 공식을 다뤘어요.

#### 종이에 쓸 첫 줄

$\mathbf A\mathbf A^\top$의 특성방정식을 세워 $\sigma_1, \mathbf u_1, \mathbf v_1$을 구하고 외적을 취하는 3단계 로드맵(1. 첫째 층 특이벡터 $\to$ 2. 외적 $\mathbf A_1$ $\to$ 3. 잔차 제곱합 대조)으로 시작해요.

$$
\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix},\qquad(17-\lambda)^2-64=0
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** $\sigma_1=5$, $\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top$, $\mathbf v_1=\frac{1}{\sqrt2}(1,1,0)^\top$이에요.

$\mathbf A\mathbf A^\top$의 고윳값과 고유벡터를 유도해요.

$$
\det(\mathbf A\mathbf A^\top-\lambda\mathbf I)=(17-\lambda)^2-8^2=0
$$

↳ 특성방정식을 세워요

$$
17-\lambda=\pm8\implies\lambda_1=25,\quad\lambda_2=9
$$

↳ 특성방정식에서 두 근을 구해요

$$
\lambda_1=25\implies \sigma_1=\sqrt{25}=5
$$

↳ 큰 고윳값의 제곱근이 최대 특잇값이에요

$$
(17-25)x+8y=0\implies x=y
$$

↳ 후보 $\mathbf w=(x,y)^\top$를 놓고 $(\mathbf A\mathbf A^\top-25\mathbf I)\mathbf w=\mathbf 0$의 첫째 행을 써요

$$
\mathbf u_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}
$$

↳ 방향 벡터를 단위 길이로 정규화해요

$$
\mathbf A^\top\mathbf u_1=\begin{bmatrix}3&2\\2&3\\2&-2\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}5\\5\\0\end{bmatrix}
$$

↳ $\mathbf A^\top$와 $\mathbf u_1$을 곱해요

$$
\mathbf v_1=\frac{\mathbf A^\top\mathbf u_1}{\sigma_1}=\frac{1}{5\sqrt2}\begin{bmatrix}5\\5\\0\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\\0\end{bmatrix}
$$

↳ $\sigma_1=5$로 나누어 확정해요

#### (b)

**최종 답 구조:** 랭크 1 근사 행렬은 $\mathbf A_1=\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}$이에요.

외적 $\sigma_1\mathbf u_1\mathbf v_1^\top$을 계산해요.

$$
\mathbf u_1\mathbf v_1^\top=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1&1&0\end{bmatrix}=\frac12\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}
$$

↳ 두 특이벡터의 외적을 계산해요

$$
\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top=5\cdot\frac12\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}=\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}
$$

↳ 특잇값 5를 곱해 랭크 1 행렬을 완성해요

두 행이 서로 같고 0이 아니므로 $\operatorname{rank}(\mathbf A_1)=1$이에요.

#### (c)

**최종 답 구조:** $\|\mathbf A-\mathbf A_1\|_F^2=9=\sigma_2^2$로 버려진 특잇값 제곱과 정확히 일치해요.

원 행렬에서 $\mathbf A_1$을 빼고 둘째 행은 첫째 행의 부호를 바꾼 벡터이므로 두 행의 제곱합이 같아요.

$$
\mathbf A-\mathbf A_1=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}-\begin{bmatrix}2.5&2.5&0\\2.5&2.5&0\end{bmatrix}=\begin{bmatrix}0.5&-0.5&2\\-0.5&0.5&-2\end{bmatrix}
$$

↳ 원 행렬에서 근사 행렬을 빼요

$$
\|\mathbf A-\mathbf A_1\|_F^2=2\cdot\big(0.5^2+(-0.5)^2+2^2\big)=2\cdot(0.25+0.25+4)=9
$$

↳ 둘째 행은 첫째 행의 부호를 바꾼 벡터이므로 두 행의 제곱합이 같아요

둘째 특잇값은 $\sigma_2=\sqrt{\lambda_2}=\sqrt9=3$이므로 $\sigma_2^2=3^2=9$예요. 따라서 **$\|\mathbf A-\mathbf A_1\|_F^2=9=\sigma_2^2$로 정확히 같아요.**

#### 완성 답과 검산

#### (a) 검산

$\mathbf A\mathbf v_1=\frac{1}{\sqrt2}\begin{bmatrix}3+2\\2+3\end{bmatrix}=\frac{5}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}=5\mathbf u_1$로 $\mathbf A\mathbf v_1=\sigma_1\mathbf u_1$이 완벽히 성립해요.

#### (b) 검산

$\mathbf A_1$의 Frobenius 제곱노름은 $4\times(2.5)^2=4\times 6.25=25=5^2=\sigma_1^2$으로 첫 층의 보존 에너지와 일치해요.

#### (c) 검산

원 행렬의 전체 제곱합은 $\|\mathbf A\|_F^2=9+4+4+4+9+4=34$이고, $\sigma_1^2+\sigma_2^2=25+9=34$이므로 에너지 보존 정리 $\|\mathbf A\|_F^2=\|\mathbf A_1\|_F^2+\|\mathbf A-\mathbf A_1\|_F^2$가 정확히 성립해요.

#### 이 문항에서 조심할 점

**$\sigma_1$ 곱하기를 빠뜨리지 않아요.** $\mathbf u_1\mathbf v_1^\top$만 적으면 첫 층의 원소 크기가 달라져 Frobenius 제곱오차가 커져요.

**노름과 제곱오차의 단위를 구별해요.** 문제에서 묻는 것은 원소 **제곱합** $\|\mathbf A-\mathbf A_1\|_F^2=9$이며 이는 $\sigma_2^2=9$와 비교해요. 제곱근을 취한 Frobenius 노름 $\|\mathbf A-\mathbf A_1\|_F=3$은 $\sigma_2=3$과 대응돼요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. $\mathbf A\mathbf A^\top$에서 $\sigma_1=5, \mathbf u_1, \mathbf v_1$을 구해요.
2. 외적 $\sigma_1\mathbf u_1\mathbf v_1^\top$을 계산해 $\mathbf A_1$을 만들어요.
3. $\mathbf A-\mathbf A_1$을 구하고 원소 제곱합 9가 $\sigma_2^2$와 일치함을 보여요.

**페이지 요약**

#### 떠올릴 개념·공식

랭크 1 근사는 첫 층 $\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top$이며, 오차는 버려진 특잇값 제곱합이에요.

$$
\|\mathbf A-\mathbf A_1\|_F^2=\sigma_2^2
$$

#### 첫 줄

$\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix}$을 적고 시작해요.

#### 핵심 답

(a) $\sigma_1=5$, $\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top$, $\mathbf v_1=\frac{1}{\sqrt2}(1,1,0)^\top$이에요.

(b) $\mathbf A_1=\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}$이에요.

(c) $\|\mathbf A-\mathbf A_1\|_F^2=9=\sigma_2^2$로 일치해요.

#### 검산

전체 제곱합 $\|\mathbf A\|_F^2=34 = 25+9 = \sigma_1^2+\sigma_2^2$로 일치해요.

#### 조건·구분

층에 $\sigma_1$을 곱해요. 제곱합은 $\sigma_2^2$, 노름은 $\sigma_2$와 비교해요.

#### 용어

- **랭크 1 근사(rank-1 approximation)** — 가장 큰 특잇값에 대응하는 첫 외적 층 $\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top$이에요.
- **외적(outer product)** — 열벡터와 행벡터의 곱 $\mathbf u\mathbf v^\top$으로 각 칸은 $u_iv_j$예요.
- **Frobenius 노름(Frobenius norm)** — 행렬 원소들의 제곱합의 제곱근이에요.
- **에카르트–영 정리(Eckart–Young theorem)** — 상위 $M$개 층의 합이 랭크 $M$ 이하 행렬 중 Frobenius 오차를 최소화한다는 정리예요.

#### 출제 근거

MML Exercise 4.10, 교과서 138쪽(PDF 144쪽). 원문은 ‘랭크 1 근사를 구하라’는 한 문장이고, 이 문항은 (a), (b)와 Frobenius 오차 판정 (c)로 나눴어요.

수업: 1104 L06 s14(랭크 제한 복원, Frobenius 오차, 에카르트–영 정리).

관련 정리노트: [작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)

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

#### 문제를 내 말로 읽어요

**주어진 것:** $m\times n$ 행렬 $\mathbf A$, SVD $\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top$, $\mathbb R^n$의 정규직교기저인 오른쪽 특이벡터 $\{\mathbf v_1,\ldots,\mathbf v_n\}$, 특잇값 순서 $\sigma_1\ge\cdots\ge\sigma_r>0$와 $i>r$에서 $\sigma_i=0$, 그리고 $\mathbf A^\top\mathbf A\mathbf v_i=\sigma_i^2\mathbf v_i$가 주어졌어요.

**구할 것:** (a) $\mathbf x=\sum_i c_i\mathbf v_i$로 전개하여 $\|\mathbf A\mathbf x\|_2^2=\sum_i \sigma_i^2 c_i^2$임을 보이고, (b) 이를 통해 $\|\mathbf A\mathbf x\|_2^2\le\sigma_1^2\|\mathbf x\|_2^2$ 부등식을 유도하며, (c) $\mathbf x=\mathbf v_1$에서 등호가 성립함을 확인하고, (d) 0이 아닌 벡터에 대한 길이 신장 비율의 최댓값이 $\sigma_1$인 이유를 완결해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘길이 신장 비율의 최댓값’이라는 단서에서 **상한 제시 후 도달(upper bound and attainment)** 논리를 떠올려요.

‘$\mathbf x=\sum_i c_i\mathbf v_i$’라는 단서에서 **정규직교기저 전개**를 떠올려요. 각 좌표는 $c_i=\mathbf v_i^\top\mathbf x$예요. 기저 벡터 간 내적은 $\mathbf v_i^\top\mathbf v_j=\delta_{ij}$($i=j$면 1, 다르면 0)이므로 벡터의 유클리드 노름 제곱은 좌표 제곱합과 같아요.

$$
\|\mathbf x\|_2^2=\mathbf x^\top\mathbf x=\sum_{i=1}^n c_i^2
$$

‘$\|\mathbf A\mathbf x\|_2^2$’에서는 길이 제곱을 전치 내적으로 표현하는 식을 떠올려요.

$$
\|\mathbf A\mathbf x\|_2^2=(\mathbf A\mathbf x)^\top(\mathbf A\mathbf x)=\mathbf x^\top\mathbf A^\top\mathbf A\mathbf x
$$

$\mathbf A^\top\mathbf A\mathbf v_i=\sigma_i^2\mathbf v_i$를 대입해 행렬곱을 스칼라 곱으로 환원해요. [첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions)와 [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)에서 같은 논증 구조를 다뤘어요.

#### 종이에 쓸 첫 줄

길이 제곱을 내적과 기저 전개식으로 표현하는 4단계 로드맵(1. 전개식 내적 $\to$ 2. 부등식 상한 $\to$ 3. $\mathbf v_1$ 등호 $\to$ 4. 최댓값 완결)으로 시작해요.

$$
\|\mathbf A\mathbf x\|_2^2=\mathbf x^\top(\mathbf A^\top\mathbf A\mathbf x),\qquad\mathbf x=\sum_{j=1}^n c_j\mathbf v_j
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

**최종 답 구조:** 직교성에 의해 교차항이 소거되어 $\|\mathbf A\mathbf x\|_2^2=\sum_{i=1}^n \sigma_i^2 c_i^2$이 성립해요.

등호 연쇄를 전개해요.

$$
\mathbf A^\top\mathbf A\mathbf x=\sum_{j=1}^n c_j\mathbf A^\top\mathbf A\mathbf v_j=\sum_{j=1}^n c_j\sigma_j^2\mathbf v_j
$$

↳ 선형성과 고유방정식을 적용해요

$$
\|\mathbf A\mathbf x\|_2^2=\Big(\sum_{i=1}^n c_i\mathbf v_i^\top\Big)\Big(\sum_{j=1}^n c_j\sigma_j^2\mathbf v_j\Big)
$$

↳ 전치된 $\mathbf x^\top$와 내적해요

$$
\hphantom{\|\mathbf A\mathbf x\|_2^2}=\sum_{i=1}^n\sum_{j=1}^n c_i c_j\sigma_j^2\,(\mathbf v_i^\top\mathbf v_j)
$$

↳ 이중 합산으로 전개해요

$$
\hphantom{\|\mathbf A\mathbf x\|_2^2}=\sum_{i=1}^n \sigma_i^2 c_i^2
$$

↳ 정규직교성으로 $i=j$ 항만 남겨요

동일한 방식으로 $\|\mathbf x\|_2^2=\sum_{i=1}^n c_i^2$이므로 (a)가 증명돼요.

#### (b)

**최종 답 구조:** 모든 $i$에 대해 $\sigma_i^2 \le \sigma_1^2$이므로 $\|\mathbf A\mathbf x\|_2^2 \le \sigma_1^2 \|\mathbf x\|_2^2$가 성립해요.

특잇값의 내림차순 정렬 조건($0\le \sigma_i^2 \le \sigma_1^2$)과 $c_i^2 \ge 0$을 적용해 부등식을 유도해요.

$$
\sum_{i=1}^n \sigma_i^2 c_i^2 \le \sum_{i=1}^n \sigma_1^2 c_i^2
$$

↳ 각 항마다 최대 특잇값 제곱으로 대체해요

$$
\hphantom{\sum_{i=1}^n \sigma_i^2 c_i^2} = \sigma_1^2 \sum_{i=1}^n c_i^2 = \sigma_1^2 \|\mathbf x\|_2^2
$$

↳ 공통인수를 묶고 기저 노름을 적용해요

$$
\frac{\|\mathbf A\mathbf x\|_2}{\|\mathbf x\|_2} \le \sigma_1
$$

↳ $\mathbf x\ne\mathbf 0$이면 $\|\mathbf x\|_2^2>0$이므로 이 값으로 양변을 나누고 음이 아닌 제곱근을 취해요

따라서 모든 0이 아닌 벡터 $\mathbf x$에 대해 $\|\mathbf A\mathbf x\|_2 \le \sigma_1 \|\mathbf x\|_2$가 성립해요.

#### (c)

**최종 답 요약:** $\mathbf x=\mathbf v_1$일 때 좌표가 $c_1=1, c_{i>1}=0$이 되어 $\|\mathbf A\mathbf v_1\|_2^2=\sigma_1^2$, $\|\mathbf v_1\|_2^2=1$이므로 부등식의 등호가 성립해요.

$\mathbf x=\mathbf v_1$을 대입하면 $c_1=\mathbf v_1^\top\mathbf v_1=1$, 나머지 $c_i=\mathbf v_i^\top\mathbf v_1=0$이에요. (a)의 결과에 대입해요.

$$
\|\mathbf A\mathbf v_1\|_2^2 = \sigma_1^2(1)^2 + \sum_{i=2}^n \sigma_i^2(0)^2 = \sigma_1^2,\qquad \|\mathbf v_1\|_2^2 = 1^2 = 1
$$

양변이 $\sigma_1^2\cdot 1$로 일치하므로 (b)의 부등식에서 등호가 엄밀히 성립해요. 신장 비율은 정확히 $\frac{\|\mathbf A\mathbf v_1\|_2}{\|\mathbf v_1\|_2}=\sigma_1$이에요.

#### (d)

**최종 답 요약:** (b)에 의해 비율의 상한이 $\sigma_1$이고, (c)에 의해 $\mathbf v_1$ 방향에서 상한에 도달하므로 최댓값은 $\sigma_1$이에요.

(b)에 의해 0이 아닌 모든 $\mathbf x$에 대해 신장 비율 $\frac{\|\mathbf A\mathbf x\|_2}{\|\mathbf x\|_2} \le \sigma_1$이므로 $\sigma_1$은 넘을 수 없는 상한(upper bound)이에요.

(c)에 의해 첫째 오른쪽 특이벡터 $\mathbf x=\mathbf v_1$을 입력으로 선택하면 신장 비율이 정확히 상한값인 $\sigma_1$에 도달해요.

$$
\max_{\mathbf x\ne\mathbf 0}\frac{\|\mathbf A\mathbf x\|_2}{\|\mathbf x\|_2} = \sigma_1
$$

따라서 **행렬 $\mathbf A$가 벡터의 길이를 늘리는 최대 비율은 $\sigma_1$이에요.** (이 값을 행렬 $\mathbf A$의 스펙트럼 노름(spectral norm) $\|\mathbf A\|_2$이라고 불러요.)

#### 완성 답과 검산

#### (a) 검산

P9의 행렬 $\mathbf A$($\sigma_1=5, \sigma_2=3, \sigma_3=0$)에서 $\mathbf x=\mathbf v_1+\mathbf v_2$($c=(1,1,0)^\top$)를 대입해요. 공식 결과는 $\sigma_1^2(1)+\sigma_2^2(1)=25+9=34$예요. 실제 행렬곱 $\mathbf A\mathbf x=5\mathbf u_1+3\mathbf u_2$의 노름 제곱은 $5^2+3^2=34$로 일치해요.

#### (b) 검산

위 예시에서 $\|\mathbf x\|_2^2=1+1=2$이므로 $\sigma_1^2\|\mathbf x\|_2^2=25\times 2=50$이에요. $34 \le 50$으로 부등식이 올바르게 성립해요.

#### (c) 검산

SVD 관계식 $\mathbf A\mathbf v_1=\sigma_1\mathbf u_1$에서 $\mathbf u_1$이 단위벡터이므로 $\|\mathbf A\mathbf v_1\|_2=\sigma_1\|\mathbf u_1\|_2=\sigma_1$로 등호가 성립함이 재확인돼요.

#### (d) 검산

상한 존재성((b))과 도달성((c))의 두 요건이 완비되어 최댓값 정리가 논리적 결함 없이 완성돼요.

#### 이 문항에서 조심할 점

**상한만 제시하고 최댓값이라 결론 내리면 안 돼요.** (b)만으로는 ‘$\sigma_1$ 이하’까지만 알 수 있어요. 실제로 그 값에 도달하는 벡터 $\mathbf v_1$이 존재함을 (c)에서 보여야 ‘최댓값’이 성립해요.

**노름에 직관적으로 $\sum \sigma_i |c_i|$를 쓰면 안 돼요.** 정규직교기저에서 성분들의 **제곱합**은 길이의 제곱이에요.

교차항 소거의 근거로 $\mathbf v_i^\top\mathbf v_j=\delta_{ij}$(정규직교성)를 밝혀야 해요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. $\mathbf x=\sum c_i\mathbf v_i$와 $\mathbf A^\top\mathbf A\mathbf v_i=\sigma_i^2\mathbf v_i$를 이용해 $\|\mathbf A\mathbf x\|_2^2=\sum\sigma_i^2 c_i^2$을 유도해요.
2. $\sigma_i^2\le\sigma_1^2$로 묶어 부등식 상한 $\sigma_1$을 도출해요.
3. $\mathbf x=\mathbf v_1$을 넣어 등호를 확인하고 상한과 도달성으로 최댓값 결론을 완성해요.

**페이지 요약**

#### 떠올릴 개념·공식

기저 전개 $\mathbf x=\sum c_i\mathbf v_i$와 $\mathbf A^\top\mathbf A\mathbf v_i=\sigma_i^2\mathbf v_i$로 길이 제곱을 계산해요.

$$
\|\mathbf A\mathbf x\|_2^2=\sum_{i=1}^n\sigma_i^2 c_i^2
$$

#### 첫 줄

$\|\mathbf A\mathbf x\|_2^2=\mathbf x^\top(\mathbf A^\top\mathbf A\mathbf x)$로 시작해요.

#### 핵심 답

(a) 직교성에 의해 교차항이 소거되어 $\sum\sigma_i^2 c_i^2$이에요.

(b) $\sigma_i^2\le\sigma_1^2$이므로 $\|\mathbf A\mathbf x\|_2^2\le\sigma_1^2\|\mathbf x\|_2^2$예요.

(c) $\mathbf x=\mathbf v_1$이면 신장 비율이 정확히 $\sigma_1$이 되어 등호가 성립해요.

(d) 상한 $\sigma_1$에 도달하는 벡터가 있으므로 최댓값은 $\sigma_1$이에요.

#### 검산

P9 수치 예에서 $34\le 50$으로 부등식이 성립하며 $\mathbf A\mathbf v_1=\sigma_1\mathbf u_1$로 등호가 확인돼요.

#### 조건·구분

상한과 도달성을 모두 확인해야 최댓값이에요. 직교 성분 길이는 제곱해서 합산해요.

#### 용어

- **유클리드 노름(Euclidean norm)** — 벡터의 2-노름 $\|\mathbf x\|_2=\sqrt{\sum x_i^2}$으로 기하학적 길이를 뜻해요.
- **정규직교기저(orthonormal basis)** — 크기가 1이고 서로 수직인 기저 벡터 집합이에요.
- **최대 특잇값(largest singular value)** — $\sigma_1$으로 행렬의 스펙트럼 노름(spectral norm) $\|\mathbf A\|_2=\max_{\mathbf x\ne\mathbf 0}\frac{\|\mathbf A\mathbf x\|_2}{\|\mathbf x\|_2}$과 같아요.
- **상한과 최댓값(upper bound & maximum)** — 상한은 넘을 수 없는 경계이며, 집합 내의 원소가 그 상한에 도달할 때 비로소 최댓값이 돼요.

#### 출제 근거

MML Exercise 4.12(정리 4.24), 교과서 138쪽(PDF 144쪽). 원문은 ‘정리 4.24가 성립함을 보여라’이고, 이 문항은 기저 전개 방식의 (a)–(d) 네 단계로 나눴어요.

수업: 1104 L05 s27–28(상한 찾기와 도달), L06 s13(SVD).

관련 정리노트: [첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions), [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

---

원 문제·정리노트·PDF는 보존해요.
