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

MML Example 10.2 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=1)

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

숫자 8 이미지만 모아 PCA를 했어요. 주성분을 하나씩 더할 때마다 담기는 분산이 얼마나 늘어나는지, 그리고 그 증가가 앞쪽과 뒤쪽 중 어디서 큰지를 묻는 문제예요.

주어진 것은 누적 설명 분산의 식 ${V_M=\sum_{m=1}^{M}\lambda_m}$과 그래프 두 개예요. 왼쪽 그래프는 가로축이 고윳값의 순서(Index), 세로축이 그 고윳값(Eigenvalue)이에요. 오른쪽 그래프는 가로축이 주성분 개수 $M$, 세로축이 $V_M$(Captured variance)이에요.

(a)는 이웃한 두 누적값의 차이 ${V_M-V_{M-1}}$을 고윳값으로 쓰는 계산이고, (b)는 (a)의 식과 왼쪽 그래프를 이어서 앞쪽과 뒤쪽의 증가 폭을 비교하는 설명이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘주성분을 하나 추가할 때 늘어나는 양’이라는 말에서는 **누적합의 이웃 차이**를 떠올려요. 누적합에서 앞의 $M-1$개 항은 두 값에 똑같이 들어 있으니, 빼면 마지막 항 하나만 남아요.

‘공분산 행렬의 고윳값’이라는 단서에서는 정리노트의 방향 분산을 떠올려요. 단위 고유벡터 $\mathbf p_m$ 방향으로 사영한 좌표의 분산은 ${\mathbf p_m^\top\mathbf S\mathbf p_m=\lambda_m}$이에요. 그래서 고윳값(eigenvalue) $\lambda_m$은 **$m$번째 주성분 방향 하나에 담긴 분산**이에요.

상위 $M$개 고유벡터를 축으로 고르면, 서로 직교하는 축의 분산을 더한 누적 설명 분산(captured variance)은 다음과 같아요. 고윳값을 큰 순서로 늘어놓았으니 $\lambda_1\ge\lambda_2\ge\cdots$예요.

$$
V_M=\sum_{m=1}^{M}\lambda_m
$$

이 식을 쓰면 왼쪽 그래프의 점 하나의 높이가 오른쪽 곡선의 한 칸 상승 폭과 같다는 연결을 만들 수 있어요. [첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions)에서 같은 식을 다뤘어요.

#### 종이에 쓸 첫 줄

두 누적합을 같은 모양으로 나란히 적어요. 마지막 항만 따로 떼어 쓰면 비교가 쉬워져요.

$$
V_M=\lambda_1+\cdots+\lambda_{M-1}+\lambda_M,\qquad V_{M-1}=\lambda_1+\cdots+\lambda_{M-1}
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 한 칸 늘어날 때의 증가량

첫 줄의 두 식을 빼요. $\lambda_1$부터 $\lambda_{M-1}$까지는 두 식에 똑같이 있어서 모두 지워지고 $\lambda_M$만 남아요.

$$
V_M-V_{M-1}=\sum_{m=1}^{M}\lambda_m-\sum_{m=1}^{M-1}\lambda_m=\lambda_M
$$

$M$번째 주성분을 추가하면 누적 설명 분산은 **그 주성분 방향의 분산인 $\lambda_M$만큼** 늘어요.

#### (b) 왼쪽 그래프로 증가 폭 비교하기

(a)에 따라 오른쪽 곡선이 $M-1$에서 $M$으로 한 칸 갈 때 오르는 높이는 왼쪽 그래프의 $M$번째 점 높이 $\lambda_M$이에요. 그래서 왼쪽 점들의 높이만 읽으면 증가 폭을 비교할 수 있어요.

왼쪽 그래프를 읽어요. 첫째 고윳값은 약 46, 둘째는 약 32로 커요. 그 뒤로 셋째가 약 21, 다섯째쯤이 약 15로 빠르게 작아지고, 50번째 근처에서는 2~3 정도, 200번째 근처에서는 1보다 작아요.

앞쪽 $\lambda_M$이 크니 처음 몇 개를 추가할 때는 한 칸마다 수십씩 올라 $V_M$이 가파르게 늘어요. 뒤로 갈수록 $\lambda_M$이 작아져 한 칸의 상승이 작아지므로 곡선이 완만해져요. 다만 뒤쪽 고윳값도 양수라서 곡선은 200개까지 멈추지 않고 조금씩 계속 올라요.

따라서 **주성분을 처음 몇 개 추가할 때 누적 설명 분산이 크게 늘고, 뒤에서 추가할 때는 완만하게 늘어요.**

#### 완성 답과 검산

#### (a) 검산

$M=1$을 넣어 봐요. 아무 축도 고르지 않았을 때 담긴 분산은 0이므로 $V_0=0$이고, ${V_1-V_0=\lambda_1}$이에요. 오른쪽 곡선의 시작점 높이가 약 46으로 왼쪽 첫 점 ${\lambda_1\approx46}$과 같아 식과 그래프가 맞아요. $M=2$에서도 ${V_2\approx46+32=78}$이 오른쪽 곡선의 둘째 칸 높이와 비슷해요.

#### (b) 검산

오른쪽 곡선에서 같은 폭(50개)의 구간을 비교해요. 0개에서 50개까지는 0에서 약 370으로 약 370 늘었어요. 150개에서 200개까지는 약 505에서 약 525로 약 20 늘었어요. 앞쪽 구간의 증가가 훨씬 커서 (b)의 판단과 맞아요. 뒤쪽 구간도 20 정도는 올랐으니 뒤쪽 고윳값이 0은 아니라는 것도 함께 확인돼요.

#### 이 문항에서 조심할 점

오른쪽 곡선의 **높이**는 지금까지 담은 분산 $V_M$이고, 왼쪽 점의 높이는 한 칸의 **상승 폭** $\lambda_M$이에요. 오른쪽 곡선에서 $M=100$의 높이 약 460을 $\lambda_{100}$으로 읽으면 안 돼요. 왼쪽 그래프에서 $\lambda_{100}$은 1~2 정도예요.

‘뒤쪽 증가가 작다’를 ‘뒤쪽 고윳값은 버려도 0이다’로 바꿔 읽으면 안 돼요. 50개에서 200개까지 곡선이 약 370에서 약 525로 약 155 더 올랐어요. 하나하나는 작아도 개수가 많으면 합이 커요.

$V_M$은 분산의 합이지 비율이 아니에요. ‘몇 퍼센트를 담았는지’를 말하려면 전체 분산으로 나눠야 하는데, 그래프에는 200개까지만 있어서 이 문항에서는 비율을 구하지 않아요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. ${V_M}$과 ${V_{M-1}}$을 나란히 적고 빼서 ${V_M-V_{M-1}=\lambda_M}$을 다시 얻어요.
2. 두 그래프의 세로축이 각각 무엇인지(한 칸의 상승 폭과 누적 높이) 말해 봐요.
3. 왼쪽 앞쪽 점과 뒤쪽 점의 높이를 읽고, 오른쪽 곡선의 기울기와 이어서 설명해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\lambda_m$은 $m$번째 주성분 방향의 분산이에요. 누적 설명 분산은 ${V_M=\sum_{m=1}^{M}\lambda_m}$이에요.

#### 첫 줄

$V_M$과 $V_{M-1}$을 마지막 항만 떼어 나란히 적어요.

#### 핵심 답

(a) ${V_M-V_{M-1}=\lambda_M}$이에요.

(b) 앞쪽 고윳값(약 46, 32)이 크고 빠르게 작아지므로, 처음 몇 개를 추가할 때 크게 늘고 뒤로 갈수록 완만하게 늘어요. 곡선은 200개까지 조금씩 계속 올라요.

#### 검산

오른쪽 시작 높이 약 46이 $\lambda_1$과 같아요. 0→50개는 약 370, 150→200개는 약 20 올라요.

#### 조건·구분

오른쪽 높이는 누적값, 왼쪽 점은 한 칸의 상승 폭이에요. 뒤쪽 고윳값도 작지만 0은 아니에요.

#### 용어

- **고윳값(eigenvalue)** — 공분산 행렬 $\mathbf S$에서 ${\mathbf S\mathbf p_m=\lambda_m\mathbf p_m}$을 만족하는 수예요. 단위 고유벡터 $\mathbf p_m$ 방향의 분산과 같아요.
- **주성분(principal component)** — 큰 고윳값부터 고른 공분산 행렬의 단위 고유벡터 방향이에요. 서로 직교해요.
- **누적 설명 분산(captured variance)** — 앞에서부터 $M$개 주성분이 담는 분산의 합 ${V_M=\sum_{m=1}^{M}\lambda_m}$이에요. 비율이 아니라 분산의 합이에요.

#### 출제 근거

MML Example 10.2와 그림 10.5, 교과서 324–325쪽(PDF 330–331쪽), 식 (10.24).

수업: 1104 L05 s27–28(상위 $M$개 방향과 보존 분산).

관련 정리노트: [첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions)

---

<a id="p2"></a>

### P2. 주성분 평면에 놓인 숫자 0과 1

MML Example 10.3 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=2)

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

손글씨 0과 1의 이미지 한 장 한 장을 숫자 두 개로 요약해 종이 위의 점으로 찍었어요. 이 점들을 보고 두 숫자가 얼마나 잘 갈라지는지, 그리고 한 숫자 안에서 어느 쪽이 더 넓게 흩어져 있는지 읽는 문제예요.

주어진 것은 산점도 하나예요. 파란 점은 숫자 0, 주황 점은 숫자 1이고, 점 하나가 이미지 한 장이에요. 빨간 표시와 선은 일부 점을 원래 이미지와 이어 주는 안내선이에요.

(a)는 두 색의 무리가 섞이는지(집단 사이의 분리), (b)는 한 색 안에서 점이 얼마나 넓게 퍼졌는지(집단 안의 분산)를 따로 묻고 있어요. 계산 없이 그림을 근거로 답해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘첫 두 주성분이 만드는 평면’이라는 말에서는 **사영 좌표**(projection coordinates)를 떠올려요. MNIST 이미지 한 장은 $28\times28$ 픽셀이라 784차원 벡터이고, 평균을 뺀 이 벡터를 $\mathbf x_n$이라 해요. 첫 두 주성분 방향 $\mathbf b_1,\mathbf b_2$와 내적한 두 수가 산점도의 가로·세로 좌표예요.

$$
\mathbf z_n=\mathbf B^\top\mathbf x_n=\begin{bmatrix}\mathbf b_1^\top\mathbf x_n\\\mathbf b_2^\top\mathbf x_n\end{bmatrix}\in\mathbb R^2,\qquad\mathbf B=[\mathbf b_1,\mathbf b_2]
$$

‘얼마나 잘 나뉘나’는 두 집단의 점이 같은 자리에 섞이는지를 보는 질문이고, ‘집단 안의 분산’은 한 집단의 점이 자기 중심에서 얼마나 멀리 흩어지는지를 보는 질문이에요. 분산은 중심에서 떨어진 정도의 제곱 평균이라, 그림에서는 한 색이 차지하는 범위의 넓이로 비교할 수 있어요.

두 주성분은 숫자 라벨 없이 0과 1 이미지 전체의 분산이 큰 방향으로 골라요. 색은 그린 뒤에 라벨로 칠한 거예요. [MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)에서 같은 그림을 다뤘어요.

#### 종이에 쓸 첫 줄

색과 숫자를 먼저 짝지어 적고, 무엇을 볼지 구분해 둬요.

‘파란 점 = 숫자 0, 주황 점 = 숫자 1, 빨간 선 = 안내선(데이터 아님). (a)는 두 색의 경계, (b)는 한 색씩의 범위.’

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 두 무리의 분리 정도

주황 점은 그림의 왼쪽 위 좁은 자리에 모여 있고, 파란 점은 그 오른쪽의 넓은 자리에 모여 있어요. 두 무리의 중심이 서로 다른 곳에 있어요.

두 색이 맞닿는 경계를 보면, 주황 무리의 오른쪽 아래 가장자리에 주황 점 몇 개가 파란 무리 쪽으로 흩어져 있어 일부가 겹쳐요. 그래도 대부분의 점은 자기 색끼리 모여 있어요.

따라서 **0과 1의 점 무리는 경계에서 조금 겹치지만 비교적 뚜렷하게 나뉘어요.** 784차원을 2차원으로 줄였는데도 두 숫자가 대부분 갈라진다는 뜻이에요.

#### (b) 어느 집단이 더 퍼졌나

이번에는 한 색씩 따로 따라가요. 주황 점은 작은 덩어리로 촘촘히 뭉쳐 있고, 가로·세로 모두 좁은 범위에 있어요.

파란 점은 위쪽 끝에서 아래쪽 끝까지 훨씬 길게 퍼져 있고, 오른쪽으로도 멀리 흩어진 점이 많아요. 차지하는 범위가 주황 덩어리보다 가로·세로 모두 몇 배 넓어요.

따라서 **숫자 0 집단이 주성분 평면에서 더 넓게 퍼져 있어 집단 안의 분산이 더 커요.** 안내선에 이어진 0 이미지들은 크기와 기울기가 서로 다르고, 1 이미지들은 한 획짜리라 서로 비슷해 보여요. 이 차이가 퍼짐의 차이로 나타난다고 해석할 수 있어요.

#### 완성 답과 검산

#### (a) 검산

안내선이 가리키는 원본 이미지를 확인해요. 왼쪽 위 주황 무리에 이어진 이미지는 모두 1이고, 오른쪽 파란 무리에 이어진 이미지는 모두 0이에요. 자리마다 숫자가 한쪽으로 정해지니 두 무리가 대부분 나뉜다는 판단과 맞아요. 경계 근처에 다른 색 점이 섞인 것은 ‘완전한 분리’가 아니라 ‘비교적 뚜렷한 분리’로 답한 근거예요.

#### (b) 검산

가장 멀리 떨어진 점을 확인해요. 그림 아래쪽 끝과 오른쪽 끝에 홀로 떨어진 점은 대부분 파란색이에요. 주황 점은 덩어리에서 조금 벗어난 몇 개를 빼면 좁은 자리에 있어요. 바깥 범위로 보아도 0이 더 넓게 퍼졌다는 판단과 맞아요.

#### 이 문항에서 조심할 점

주황 덩어리는 점이 촘촘해서 색이 진하게 칠해져 크게 보일 수 있어요. 퍼짐은 **색의 진하기**가 아니라 **점들이 차지하는 범위**로 비교해요.

(a)의 분리와 (b)의 퍼짐은 다른 질문이에요. 두 집단이 잘 나뉘어도 한 집단은 넓게 퍼질 수 있어요. 한쪽 답으로 다른 쪽을 대신하지 않아요.

빨간 선과 빨간 점은 원본 이미지를 보여 주는 안내 표시예요. 선의 길이나 위치는 분산과 관계가 없어요.

여기서 본 퍼짐은 첫 두 주성분 좌표로 사영한 뒤의 퍼짐이에요. 784차원 원래 픽셀 공간 전체의 분산을 이 그림 하나로 단정하지 않아요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. 색과 숫자, 안내선의 뜻을 먼저 적어요.
2. 두 색이 만나는 경계를 찾아 섞이는 정도를 말해요.
3. 한 색씩 위·아래·좌·우 끝을 찾아 차지하는 범위를 비교해요.

**페이지 요약**

#### 떠올릴 개념·공식

점의 좌표는 첫 두 주성분과의 내적이에요.

$$
\mathbf z_n=\mathbf B^\top\mathbf x_n\in\mathbb R^2
$$

분리는 두 색이 섞이는지, 집단 안의 분산은 한 색이 차지하는 범위로 봐요.

#### 첫 줄

파란 점 = 0, 주황 점 = 1, 빨간 선 = 안내선으로 적어요.

#### 핵심 답

(a) 경계에서 조금 겹치지만 비교적 뚜렷하게 나뉘어요.

(b) 숫자 0 집단이 더 넓게 퍼져 집단 안의 분산이 더 커요.

#### 검산

안내선의 원본이 자리마다 한 숫자로 정해져요. 멀리 떨어진 점은 대부분 파란색이에요.

#### 조건·구분

색의 진하기가 아니라 범위로 퍼짐을 비교해요. 사영한 뒤 2차원 평면에서의 퍼짐이에요.

#### 용어

- **주성분 평면(principal subspace)** — 첫 두 주성분 방향 $\mathbf b_1,\mathbf b_2$가 만드는 평면이에요. 각 이미지는 이 평면 위의 점 하나로 찍혀요.
- **사영 좌표(projection coordinates)** — 평균을 뺀 이미지 벡터와 주성분 방향의 내적 ${\mathbf b_i^\top\mathbf x_n}$이에요. 산점도의 가로·세로 값이에요.
- **산점도(scatter plot)** — 이미지 한 장을 두 좌표를 갖는 점 하나로 그린 그림이에요.
- **집단 안의 분산(within-class variance)** — 한 숫자 집단의 점들이 자기 중심에서 얼마나 멀리 흩어졌는지를 나타내는 양이에요.

#### 출제 근거

MML Example 10.3과 그림 10.10, 교과서 332–333쪽(PDF 338–339쪽).

수업: 1104 L06 s11(MNIST 0과 1의 2차원 사영).

관련 정리노트: [MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)

---

<a id="p3"></a>

### P3. 주성분 개수와 숫자 8의 복원

MML Example 10.4 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=3)

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

숫자 8 이미지를 적은 수의 좌표로 줄였다가 다시 784픽셀 이미지로 되돌린 결과를 보는 문제예요. 남기는 주성분이 많을수록 원본에 얼마나 가까워지는지, 전부 남기면 정확히 같아지는지, 500개만으로도 충분한 이유가 무엇인지를 차례로 물어요.

주어진 것은 다음과 같아요. 이미지는 $D=784$차원 벡터이고, 주성분은 **학습 이미지** 5,389장으로 구했어요. 그림의 네 열은 **테스트 이미지** 네 장이고, 맨 윗줄이 원본, 아랫줄들이 주성분 1, 10, 100, 500개로 복원한 결과예요. 학습 데이터의 평균 제곱 복원오차(최솟값)는 ${J_M^\star=\sum_{i=M+1}^{D}\lambda_i}$예요. 오차 곡선(그림 10.13)은 약 400개를 넘으면 거의 0이고, 약 550개면 학습 데이터를 사실상 완전히 복원한다는 사실도 주어졌어요.

(a)는 그림 읽기, (b)는 $M=784$일 때 $J_{784}^\star$ 계산과 정확한 복원 판정, (c)는 (b)의 식과 오차 곡선을 이어 500개로 충분한 이유를 설명하는 문항이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘주성분 $M$개로 복원’이라는 말에서는 정리노트의 **사영과 복원**을 떠올려요. 평균을 뺀 이미지 $\mathbf x$를 상위 $M$개 정규직교 고유벡터를 열로 모은 ${\mathbf B\in\mathbb R^{784\times M}}$에 사영하면 좌표 ${\mathbf z=\mathbf B^\top\mathbf x}$($M$개 수)를 얻어요. 이 좌표로 축을 다시 더하면 784차원 복원 벡터가 돼요.

$$
\tilde{\mathbf x}=\mathbf B\mathbf z=\mathbf B\mathbf B^\top\mathbf x
$$

복원한 뒤에는 빼 두었던 평균 이미지를 다시 더해 그림으로 보여요.

‘복원오차’라는 말에서는 **버린 방향의 분산 합**을 떠올려요. 원래 벡터에서 복원값을 빼면 버린 축의 성분만 남고, 그 제곱의 학습 평균이 버린 고윳값의 합이에요. 고윳값은 $\lambda_1\ge\cdots\ge\lambda_{784}\ge0$으로 정렬되어 있어요.

$$
J_M^\star=\sum_{i=M+1}^{D}\lambda_i
$$

‘$M=D$’라는 조건에서는 **정사각 정규직교행렬**을 떠올려요. 열이 정규직교인 정사각행렬은 ${\mathbf B^\top\mathbf B=\mathbf I}$일 뿐 아니라 반대 순서로도 ${\mathbf B\mathbf B^\top=\mathbf I}$예요. [버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded)와 [MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)에서 같은 식을 다뤘어요.

#### 종이에 쓸 첫 줄

(a)는 한 열을 골라 위에서 아래로 원본, 1, 10, 100, 500 순서로 비교한다고 적어요. (b)·(c)는 오차식에 $M$을 넣은 두 식을 나란히 적어요.

$$
J_{784}^\star=\sum_{i=785}^{784}\lambda_i,\qquad J_{500}^\star=\sum_{i=501}^{784}\lambda_i
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 주성분 수에 따른 복원 이미지

한 열은 같은 원본을 복원한 결과라서 열 안에서 위아래로 비교해요.

주성분 1개에서는 네 장이 모두 흐릿하고 서로 비슷한 ‘평균적인 8’ 모양이에요. 원본마다 다른 기울기나 획 모양이 거의 드러나지 않아요.

10개에서는 각 열의 기울기와 대략적인 윤곽이 원본을 닮기 시작하지만 아직 번지고 배경이 회색으로 얼룩져요. 100개에서는 각 숫자만의 획이 알아볼 수 있을 만큼 또렷해지고, 배경의 얼룩이 남아 있어요. 500개에서는 원본과 거의 구별되지 않아요.

따라서 **주성분이 늘수록 흐릿하고 비슷한 모양에서 각 원본의 세부가 살아 있는 선명한 모양으로 바뀌어요.** 새 주성분을 하나 더할 때마다 그 방향의 성분을 복원에 보태기 때문이에요.

#### (b) 784개를 모두 쓸 때

$M=784=D$이면 $\mathbf B$는 $784\times784$ 정사각행렬이고, 784개의 정규직교 열은 $\mathbb R^{784}$ 전체의 정규직교기저예요.

$\mathbf B^\top\mathbf B$의 $(i,j)$ 칸은 $\mathbf b_i^\top\mathbf b_j$라서 대각은 1, 나머지는 0이에요. 그래서 ${\mathbf B^\top\mathbf B=\mathbf I}$이고, 정사각행렬이므로 $\mathbf B^\top$가 $\mathbf B$의 역행렬이에요. 역행렬은 반대 순서로 곱해도 단위행렬이라 다음이 성립해요.

$$
\mathbf B\mathbf B^\top=\mathbf I_{784}
$$

복원식에 넣어요.

$$
\tilde{\mathbf x}=\mathbf B\mathbf B^\top\mathbf x=\mathbf I_{784}\,\mathbf x=\mathbf x
$$

이 계산에는 $\mathbf x$가 학습 이미지라는 조건이 쓰이지 않아서, 학습 이미지든 테스트 이미지든 똑같이 성립해요. 빼 두었던 평균 이미지를 더하면 원본과 정확히 같아요.

오차식에서는 버린 축이 하나도 없어요. 합의 시작 번호 785가 끝 번호 784보다 커서 더할 항이 없는 빈 합이고, 빈 합은 0이에요.

$$
J_{784}^\star=\sum_{i=785}^{784}\lambda_i=0
$$

따라서 **주성분 784개를 모두 쓰면 ${J_{784}^\star=0}$이고, 원본이 정확히 복원돼요.**

#### (c) 500개로도 거의 완벽한 이유

먼저 $M$을 늘릴 때 오차가 어떻게 변하는지 봐요. $M$이 하나 커지면 합에서 $\lambda_{M+1}$ 한 항이 빠져요.

$$
J_{M}^\star-J_{M+1}^\star=\lambda_{M+1}\ge0
$$

고윳값이 음수가 아니라서 $J_M^\star$는 $M$이 커질 때 줄어들거나 그대로일 뿐 늘지 않아요. 그래서 ${J_{500}^\star\le J_{400}^\star}$예요.

조건에서 오차 곡선은 400개를 넘으면 거의 0이에요. 그러니 ${J_{500}^\star=\sum_{i=501}^{784}\lambda_i}$도 아주 작아요. 학습 이미지에서 버린 284개 방향의 분산을 모두 더해도 아주 작다는 뜻이에요. 조건의 ‘가장자리 픽셀은 늘 검정’도 같은 방향을 가리켜요. 늘 검정인 픽셀 $d$는 평균을 빼면 모든 이미지에서 0이라, 분산도 다른 픽셀과의 공분산도 0이에요. 그래서 $\mathbf S$의 $d$번째 열이 모두 0이고, 그 픽셀 하나만 1인 방향 $\mathbf e_d$는 ${\mathbf S\mathbf e_d=\mathbf 0}$, 곧 고윳값 0의 고유벡터예요. 이런 고윳값은 합에 아무것도 보태지 않아요.

그런데 $J_M^\star$는 **학습 이미지**에 대한 평균이고, 그림의 네 장은 **테스트 이미지**예요. 테스트 이미지도 학습 이미지와 같은 분포(같은 방식으로 모은 손글씨 숫자 8)에서 나왔다고 가정하면, 테스트 이미지도 버린 방향의 성분이 학습 때처럼 작을 것으로 기대해요.

따라서 **버린 고윳값의 합 $J_{500}^\star$가 아주 작고, 테스트 이미지가 학습 이미지와 같은 분포라는 가정 아래 500개만으로도 거의 완벽하게 복원돼요.**

#### 완성 답과 검산

#### (a) 검산

넷째 열(비스듬히 기운 8)로 다시 확인해요. 1개에서는 조금 기운 흐릿한 덩어리일 뿐 획의 세부가 없어요. 10개, 100개로 갈수록 비스듬한 획이 또렷해지고, 500개에서는 원본과 거의 같은 모양이에요. 같은 열 안에서 세부가 점점 살아난다는 판단과 맞아요.

#### (b) 검산

축 하나씩 확인해요. 복원값과 $\mathbf b_j$의 내적은 ${\mathbf b_j^\top\mathbf B\mathbf B^\top\mathbf x}$인데, ${\mathbf b_j^\top\mathbf B}$는 $j$번째 칸만 1인 행벡터라 결과가 ${\mathbf b_j^\top\mathbf x}$예요. 784개 축 모두에서 원본과 복원의 좌표가 같으니 두 벡터가 같아요. 오차식으로도 $M=783$일 때 ${J_{783}^\star=\lambda_{784}}$이고, 마지막 축까지 넣으면 그 한 항마저 빠져 0이 돼요.

#### (c) 검산

그림의 500개 줄이 실제로 원본 줄과 거의 같아 보여서 설명과 맞아요. 또 조건의 ‘약 550개면 학습 데이터를 사실상 완전히 복원’은 ${J_{550}^\star\approx0}$이라는 뜻이고, 줄어들기만 한다는 성질에 따라 ${J_{500}^\star}$는 ${J_{400}^\star}$와 ${J_{550}^\star}$ 사이에 있어요. 두 값이 모두 거의 0이니 ${J_{500}^\star}$도 거의 0이에요.

#### 이 문항에서 조심할 점

**‘거의 완벽’과 ‘정확’을 구분해요.** 500개는 그림에서 원본과 거의 같아 보이는 것이고, 수학적으로 오차가 정확히 0이 되는 것은 784개(또는 버린 고윳값이 모두 0일 때)예요.

**학습 오차를 테스트 결과로 바로 옮기지 않아요.** $J_M^\star$는 주성분을 구한 학습 이미지의 평균이에요. 테스트 이미지에 쓰려면 같은 분포라는 가정이 필요해요. 이 가정은 (c)의 답에 꼭 들어가야 해요.

(b)의 이유를 ‘$J_{784}^\star=0$이니까’로만 쓰면 학습 평균이 0이라는 말일 뿐이에요. 테스트 이미지까지 정확히 복원되는 근거는 ${\mathbf B\mathbf B^\top=\mathbf I}$예요. 이 성질은 $\mathbf B$가 정사각일 때만 성립하고, $M\lt784$에서는 $\mathbf B\mathbf B^\top$가 단위행렬이 아니에요.

(a)는 같은 열 안에서 비교해요. 다른 열의 원본은 서로 다른 8이라 열끼리 비교하면 복원 품질을 판단할 수 없어요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. 한 열을 골라 1, 10, 100, 500개 복원이 원본과 어떻게 달라지는지 말해 봐요.
2. $M=784$에서 ${\mathbf B\mathbf B^\top=\mathbf I}$인 이유와 ${J_{784}^\star}$가 빈 합이라 0인 이유를 적어요.
3. ${J_M^\star-J_{M+1}^\star=\lambda_{M+1}\ge0}$에서 출발해 400개 이후의 곡선 사실과 학습→테스트 가정을 이어 (c)를 설명해요.

**페이지 요약**

#### 떠올릴 개념·공식

복원은 ${\tilde{\mathbf x}=\mathbf B\mathbf B^\top\mathbf x}$이고, 학습 평균 제곱 복원오차는 버린 고윳값의 합이에요.

$$
J_M^\star=\sum_{i=M+1}^{D}\lambda_i
$$

#### 첫 줄

${J_{784}^\star}$와 ${J_{500}^\star}$에 $M$을 넣은 두 합을 나란히 적어요.

#### 핵심 답

(a) 주성분이 늘수록 흐릿하고 비슷한 모양에서 원본의 세부가 살아 있는 선명한 모양으로 바뀌어요.

(b) $M=784$면 $\mathbf B$가 전체 정규직교기저라 ${\mathbf B\mathbf B^\top=\mathbf I}$, ${\tilde{\mathbf x}=\mathbf x}$이고 ${J_{784}^\star=0}$이에요.

(c) $J_M^\star$는 줄어들기만 하고 400개 이후 거의 0이라 ${J_{500}^\star}$가 아주 작아요. 테스트 이미지가 같은 분포라는 가정 아래 500개로 거의 완벽하게 복원돼요.

#### 검산

축마다 ${\mathbf b_j^\top\tilde{\mathbf x}=\mathbf b_j^\top\mathbf x}$예요. ${J_{500}^\star}$는 ${J_{400}^\star}$와 ${J_{550}^\star}$ 사이에 있어요.

#### 조건·구분

거의 완벽(500)과 정확(784)을 구분해요. 학습 오차를 테스트로 옮길 때는 같은 분포 가정이 필요해요.

#### 용어

- **복원(reconstruction)** — 사영 좌표 ${\mathbf z=\mathbf B^\top\mathbf x}$로 축을 다시 더해 원래 차원의 벡터 ${\tilde{\mathbf x}=\mathbf B\mathbf z}$를 만드는 것이에요. 그림으로 볼 때는 평균 이미지를 다시 더해요.
- **평균 제곱 복원오차(average squared reconstruction error)** — 학습 이미지마다 ${\lVert\mathbf x_n-\tilde{\mathbf x}_n\rVert^2}$을 구해 평균낸 값이에요. 상위 $M$개 주성분을 쓰면 최솟값이 ${J_M^\star=\sum_{i=M+1}^{D}\lambda_i}$예요.
- **정규직교기저(orthonormal basis)** — 길이가 1이고 서로 수직인 벡터로 이루어진 기저예요. $D$개를 모두 열로 모은 정사각행렬은 ${\mathbf B\mathbf B^\top=\mathbf I}$를 만족해요.
- **빈 합(empty sum)** — 시작 번호가 끝 번호보다 커서 더할 항이 없는 합이에요. 값은 0이에요.
- **학습·테스트 이미지(training/test images)** — 학습 이미지는 주성분을 구하는 데 쓴 이미지, 테스트 이미지는 그 계산에 쓰지 않은 새 이미지예요.

#### 출제 근거

MML Example 10.4와 그림 10.12, 교과서 338–339쪽(PDF 344–345쪽). 그림 10.13과 식 (10.62)의 설명(약 550개면 학습 데이터 완전 복원, 가장자리 픽셀)은 조건에 문장으로 주어졌어요.

수업: 1104 L06 s8–11(버린 방향의 복원오차, MNIST 사영과 복원).

관련 정리노트: [버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded), [MNIST에서 사영과 복원 읽기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-mnist)

---

<a id="p4"></a>

### P4. 가로로 긴 행렬의 특잇값 분해

MML Example 4.13 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=4)

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

가로로 긴 $2\times3$ 행렬을 ‘입력 쪽 방향($\mathbf V$)’, ‘늘이는 배율($\mathbf\Sigma$)’, ‘출력 쪽 방향($\mathbf U$)’ 세 조각으로 나누는 문제예요. 순서는 정해져 있어요. 먼저 $\mathbf V$, 다음 $\mathbf\Sigma$, 마지막에 $\mathbf U$를 구해요.

주어진 것은 ${\mathbf A=\begin{bmatrix}1&1&0\\0&1&1\end{bmatrix}}$이에요. (a)는 ${\mathbf A^\top\mathbf A}$의 고윳값과 정규화된 고유벡터로 $\mathbf V$를, (b)는 그 고윳값으로 특잇값과 $\mathbf\Sigma$를, (c)는 ${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$로 $\mathbf U$를 구하고, (d)는 세 행렬의 크기를 읽어요.

MML Example 4.13의 수치를 바꾼 변형이에요. 교과서 행렬은 ${\begin{bmatrix}1&0&1\\-2&1&0\end{bmatrix}}$이고, 풀이 단계는 같아요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘특잇값 분해(singular value decomposition, SVD)’라는 말에서는 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$를 떠올려요. $\mathbf A$가 $m\times n$이면 $\mathbf U$는 $m\times m$, $\mathbf V$는 $n\times n$ 정사각 정규직교행렬이고, $\mathbf\Sigma$는 $\mathbf A$와 같은 $m\times n$ 크기에 대각에만 특잇값 ${\sigma_1\ge\sigma_2\ge\cdots\gt0}$을 놓고 나머지는 0인 행렬이에요.

‘$\mathbf A^\top\mathbf A$의 고유벡터로 $\mathbf V$’라는 단서에서는 정리노트에서 ${\mathbf X\mathbf X^\top}$에 SVD를 넣었던 계산을 반대쪽에 적용해요. 전치하면 곱의 순서가 뒤집혀 ${\mathbf A^\top=\mathbf V\mathbf\Sigma^\top\mathbf U^\top}$이고, $\mathbf U$의 열이 정규직교라 ${\mathbf U^\top\mathbf U=\mathbf I}$로 가운데가 사라져요.

$$
\mathbf A^\top\mathbf A=\mathbf V\mathbf\Sigma^\top\mathbf U^\top\mathbf U\mathbf\Sigma\mathbf V^\top=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top
$$

${\mathbf\Sigma^\top\mathbf\Sigma}$는 대각이 $\sigma_i^2$(특잇값이 없는 자리는 0)인 $n\times n$ 대각행렬이에요. 이 식은 1102의 고윳값 분해 ${\mathbf P\mathbf D\mathbf P^\top}$ 모양이라, **$\mathbf V$의 열 $\mathbf v_i$가 $\mathbf A^\top\mathbf A$의 고유벡터이고 고윳값이 $\sigma_i^2$**예요. 그래서 특잇값은 양의 고윳값의 제곱근이에요. ${\mathbf A^\top\mathbf A}$가 대칭이라 스펙트럼 정리로 정규직교 고유벡터를 고를 수 있어요.

‘${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$’는 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$의 오른쪽에 $\mathbf V$를 곱한 ${\mathbf A\mathbf V=\mathbf U\mathbf\Sigma}$(${\mathbf V^\top\mathbf V=\mathbf I}$)를 열마다 읽은 식 ${\mathbf A\mathbf v_i=\sigma_i\mathbf u_i}$에서 나와요.

고윳값은 1102에서 배운 특성다항식 ${\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)=0}$을 첫째 행으로 여인수 전개해 구해요. [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)에서 같은 대입을 다뤘어요.

#### 종이에 쓸 첫 줄

$\mathbf A^\top$의 행(= $\mathbf A$의 열)과 $\mathbf A$의 열을 내적해 ${\mathbf A^\top\mathbf A}$를 적어요. $(i,j)$ 칸은 $\mathbf A$의 $i$번째 열과 $j$번째 열의 내적이에요. 예를 들어 $(2,2)$ 칸은 둘째 열 $(1,1)^\top$의 자기 내적 ${1+1=2}$예요.

$$
\mathbf A^\top\mathbf A=\begin{bmatrix}1&1&0\\1&2&1\\0&1&1\end{bmatrix}
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) $\mathbf A^\top\mathbf A$의 고윳값과 $\mathbf V$

대각에서 $\lambda$를 빼고 첫째 행으로 전개해요. $(1,1)$ 소행렬식은 ${(2-\lambda)(1-\lambda)-1\cdot1}$이에요. $(1,2)$ 원소 1의 소행렬식은 첫째 행과 둘째 열을 지운 ${\begin{vmatrix}1&1\\0&1-\lambda\end{vmatrix}=1-\lambda}$이고, 자리 부호가 $-$예요. $(1,3)$ 원소는 0이라 그 항은 없어요.

$$
\det(\mathbf A^\top\mathbf A-\lambda\mathbf I)=(1-\lambda)\big[(2-\lambda)(1-\lambda)-1\big]-1\cdot(1-\lambda)
$$

두 항에 공통인 ${(1-\lambda)}$로 묶고, 괄호 안을 전개해요. ${(2-\lambda)(1-\lambda)=\lambda^2-3\lambda+2}$이에요.

$$
=(1-\lambda)\big[\lambda^2-3\lambda+2-1-1\big]=(1-\lambda)(\lambda^2-3\lambda)
$$

$$
=-\lambda(\lambda-1)(\lambda-3)
$$

고윳값은 큰 순서로 ${3,\ 1,\ 0}$이에요.

고윳값마다 ${(\mathbf A^\top\mathbf A-\lambda\mathbf I)\mathbf v=\mathbf 0}$의 행을 하나씩 식으로 써서 풀어요.

${\lambda=3}$: 행렬은 ${\begin{bmatrix}-2&1&0\\1&-1&1\\0&1&-2\end{bmatrix}}$예요. 첫째 행 ${-2v_1+v_2=0}$에서 ${v_2=2v_1}$, 셋째 행 ${v_2-2v_3=0}$에서 ${v_3=v_1}$이라 $(1,2,1)$ 방향이에요. 둘째 행 ${1-2+1=0}$도 맞아요.

${\lambda=1}$: 행렬은 ${\begin{bmatrix}0&1&0\\1&1&1\\0&1&0\end{bmatrix}}$예요. 첫째 행에서 ${v_2=0}$, 둘째 행 ${v_1+v_2+v_3=0}$에서 ${v_3=-v_1}$이라 $(1,0,-1)$ 방향이에요.

${\lambda=0}$: 행렬은 ${\mathbf A^\top\mathbf A}$ 그대로예요. 첫째 행 ${v_1+v_2=0}$에서 ${v_2=-v_1}$, 셋째 행 ${v_2+v_3=0}$에서 ${v_3=v_1}$이라 $(1,-1,1)$ 방향이에요. 둘째 행 ${1-2+1=0}$도 맞아요.

길이 $\sqrt6$, $\sqrt2$, $\sqrt3$으로 나눠 정규화하고, 큰 고윳값 순서로 열에 놓아요. 대칭행렬의 서로 다른 고윳값의 고유벡터라 서로 직교해요.

$$
\mathbf v_1=\frac{1}{\sqrt6}\begin{bmatrix}1\\2\\1\end{bmatrix},\quad\mathbf v_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\0\\-1\end{bmatrix},\quad\mathbf v_3=\frac{1}{\sqrt3}\begin{bmatrix}1\\-1\\1\end{bmatrix}
$$

$$
\mathbf V=\begin{bmatrix}\frac{1}{\sqrt6}&\frac{1}{\sqrt2}&\frac{1}{\sqrt3}\\\frac{2}{\sqrt6}&0&-\frac{1}{\sqrt3}\\\frac{1}{\sqrt6}&-\frac{1}{\sqrt2}&\frac{1}{\sqrt3}\end{bmatrix}
$$

#### (b) 특잇값과 $\mathbf\Sigma$

recall의 식에서 ${\mathbf A^\top\mathbf A}$의 고윳값은 $\sigma_i^2$이에요. 양의 고윳값은 3과 1 두 개라 특잇값은 그 제곱근 두 개예요. 고윳값 0은 특잇값이 없는 자리에 해당해요.

$$
\sigma_1=\sqrt3,\qquad\sigma_2=1
$$

$\mathbf\Sigma$는 $\mathbf A$와 같은 $2\times3$ 크기로 두고, 대각 $(1,1)$, $(2,2)$ 자리에 특잇값을 큰 순서로 놓고 나머지는 0으로 채워요.

$$
\mathbf\Sigma=\begin{bmatrix}\sqrt3&0&0\\0&1&0\end{bmatrix}
$$

#### (c) $\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i$로 $\mathbf U$

먼저 $\mathbf A\mathbf v_1$을 행×열로 계산해요. 첫째 행 $(1,1,0)$과 $(1,2,1)$의 내적은 3, 둘째 행 $(0,1,1)$과의 내적도 3이에요.

$$
\mathbf A\mathbf v_1=\frac{1}{\sqrt6}\begin{bmatrix}3\\3\end{bmatrix},\qquad\mathbf u_1=\frac{1}{\sqrt3}\cdot\frac{1}{\sqrt6}\begin{bmatrix}3\\3\end{bmatrix}=\frac{3}{\sqrt{18}}\begin{bmatrix}1\\1\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}
$$

${\sqrt{18}=3\sqrt2}$라 ${3/\sqrt{18}=1/\sqrt2}$예요. $\mathbf A\mathbf v_2$는 첫째 행과의 내적 ${1+0+0=1}$, 둘째 행과의 내적 ${0+0-1=-1}$이에요. $\sigma_2=1$로 나누면 그대로예요.

$$
\mathbf u_2=\mathbf A\mathbf v_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}
$$

$$
\mathbf U=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}
$$

${\mathbf u_1^\top\mathbf u_2=\frac12(1-1)=0}$이고 두 열의 길이가 1이라 $\mathbf U$는 정규직교행렬이에요. $\mathbf v_3$는 ${\sigma_3}$이 없어서 $\mathbf u$를 만들지 않아요. 대신 ${\mathbf A\mathbf v_3=\frac{1}{\sqrt3}(1-1+0,\ 0-1+1)^\top=\mathbf 0}$이라 ${\mathbf A\mathbf V=\mathbf U\mathbf\Sigma}$의 셋째 열(둘 다 $\mathbf 0$)도 맞아요.

세 열이 모두 맞으니 ${\mathbf A\mathbf V=\mathbf U\mathbf\Sigma}$예요. $\mathbf V$가 정사각 정규직교행렬이라 ${\mathbf V\mathbf V^\top=\mathbf I}$이고, 오른쪽에 $\mathbf V^\top$를 곱하면 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$예요.

#### (d) 세 행렬의 크기

$\mathbf A$가 $2\times3$이라 $m=2$, $n=3$이에요. $\mathbf U$는 출력 공간 $\mathbb R^2$의 기저라 $2\times2$, $\mathbf\Sigma$는 $\mathbf A$와 같은 $2\times3$, $\mathbf V$는 입력 공간 $\mathbb R^3$의 기저라 $3\times3$이에요.

곱 ${\mathbf U\mathbf\Sigma\mathbf V^\top}$의 크기도 ${(2\times2)(2\times3)(3\times3)=2\times3}$으로 $\mathbf A$와 같아요. 양의 특잇값이 $\sqrt3$과 $1$ 두 개라 $\mathbf A$의 랭크는 2예요.

#### 완성 답과 검산

#### (a) 검산

정규화 전 벡터에 ${\mathbf A^\top\mathbf A}$를 곱해요. ${(1,2,1)}$은 ${(1+2,\ 1+4+1,\ 2+1)}$, 곧 ${(3,6,3)=3(1,2,1)}$이에요. ${(1,0,-1)}$은 ${(1,\ 1-1,\ -1)}$, 곧 ${1\cdot(1,0,-1)}$이에요. ${(1,-1,1)}$은 ${(1-1,\ 1-2+1,\ -1+1)}$, 곧 ${(0,0,0)}$이에요. 세 내적 ${(1,2,1)\cdot(1,0,-1)=0}$, ${(1,2,1)\cdot(1,-1,1)=0}$, ${(1,0,-1)\cdot(1,-1,1)=0}$으로 서로 직교해요.

#### (b) 검산

반대쪽 ${\mathbf A\mathbf A^\top}$로 확인해요. $\mathbf A$의 두 행끼리 내적하면 ${\mathbf A\mathbf A^\top=\begin{bmatrix}2&1\\1&2\end{bmatrix}}$이고, 특성다항식 ${(2-\lambda)^2-1=0}$에서 고윳값이 $3,1$이에요. ${\mathbf A^\top\mathbf A}$의 양의 고윳값과 같아서 ${\sigma_1^2=3}$, ${\sigma_2^2=1}$이 맞아요. 또 ${\mathbf A\mathbf v_1=\frac{1}{\sqrt6}(3,3)^\top}$의 길이는 ${\frac{3\sqrt2}{\sqrt6}=\sqrt3}$으로 $\sigma_1$과 같아요. ${\mathbf A\mathbf v_i=\sigma_i\mathbf u_i}$에서 $\mathbf u_i$의 길이가 1이니 당연한 결과예요.

#### (c) 검산

층 두 개를 더해 $\mathbf A$가 나오는지 봐요. ${\sigma_1\mathbf u_1\mathbf v_1^\top}$의 계수는 ${\sqrt3\cdot\frac{1}{\sqrt2}\cdot\frac{1}{\sqrt6}=\frac{\sqrt3}{\sqrt{12}}=\frac12}$이고, ${\sigma_2\mathbf u_2\mathbf v_2^\top}$의 계수는 ${1\cdot\frac{1}{\sqrt2}\cdot\frac{1}{\sqrt2}=\frac12}$이에요.

$$
\frac12\begin{bmatrix}1&2&1\\1&2&1\end{bmatrix}+\frac12\begin{bmatrix}1&0&-1\\-1&0&1\end{bmatrix}=\begin{bmatrix}1&1&0\\0&1&1\end{bmatrix}
$$

원래 $\mathbf A$와 같아요. 또 ${\mathbf A\mathbf A^\top=\begin{bmatrix}2&1\\1&2\end{bmatrix}}$에 $\mathbf u_1$을 곱하면 ${\frac{1}{\sqrt2}(3,3)^\top=3\mathbf u_1}$, $\mathbf u_2$를 곱하면 ${\frac{1}{\sqrt2}(1,-1)^\top=\mathbf u_2}$라 $\mathbf u_1,\mathbf u_2$는 ${\mathbf A\mathbf A^\top}$의 고유벡터예요.

#### (d) 검산

곱셈이 정의되려면 이웃한 크기가 맞아야 해요. $\mathbf U$의 열 수 2 = $\mathbf\Sigma$의 행 수 2, $\mathbf\Sigma$의 열 수 3 = $\mathbf V^\top$의 행 수 3이라 곱할 수 있고, 결과는 바깥 크기 ${2\times3}$이에요.

#### 이 문항에서 조심할 점

**$\mathbf U$를 $\mathbf A\mathbf A^\top$에서 따로 구해 부호를 마음대로 정하면 안 돼요.** 예를 들어 ${\mathbf u_1=-\frac{1}{\sqrt2}(1,1)^\top}$도 $\mathbf A\mathbf A^\top$의 단위 고유벡터지만, $\mathbf v_1$은 그대로 두고 이것을 쓰면 첫 층의 부호만 뒤집혀 ${\mathbf U\mathbf\Sigma\mathbf V^\top=\begin{bmatrix}0&-1&-1\\-1&-1&0\end{bmatrix}}$이 되어 $\mathbf A$와 달라요. ${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$로 구하면 부호가 저절로 맞아요.

고윳값 0까지 제곱근을 씌워 $\mathbf\Sigma$에 ${\sigma_3=0}$을 넣으려고 $3\times3$으로 만들면 안 돼요. $\mathbf\Sigma$는 $\mathbf A$와 같은 $2\times3$이고, 대각 자리는 두 개뿐이에요.

특잇값은 고윳값의 **제곱근**이에요. ${\sigma_1=3}$으로 쓰면 ${\mathbf u_1=\mathbf A\mathbf v_1/3}$의 길이가 ${\sqrt3/3=1/\sqrt3}$이 되어 단위벡터가 아니에요.

$\mathbf V$의 열 순서와 $\mathbf\Sigma$의 대각 순서를 맞춰요. $\mathbf v_1$은 가장 큰 고윳값 3의 고유벡터예요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. ${\mathbf A^\top\mathbf A=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top}$을 써서 왜 $\mathbf A^\top\mathbf A$의 고유벡터가 $\mathbf V$인지 말해요.
2. ${\mathbf A^\top\mathbf A}$를 구하고 첫째 행 전개로 ${-\lambda(\lambda-1)(\lambda-3)}$을 얻은 뒤, 고유벡터 세 개를 행 식으로 풀어 정규화해요.
3. ${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$로 $\mathbf U$를 구하고 두 층을 더해 $\mathbf A$가 나오는지 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mathbf V$의 열은 $\mathbf A^\top\mathbf A$의 고유벡터, 고윳값은 $\sigma_i^2$예요.

$$
\mathbf A^\top\mathbf A=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top
$$

${\mathbf A\mathbf V=\mathbf U\mathbf\Sigma}$를 열마다 읽으면 ${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$예요.

#### 첫 줄

${\mathbf A^\top\mathbf A=\begin{bmatrix}1&1&0\\1&2&1\\0&1&1\end{bmatrix}}$를 열끼리의 내적으로 적어요.

#### 핵심 답

(a) 고윳값 ${3,1,0}$이에요.

$$
\mathbf v_1=\frac{1}{\sqrt6}\begin{bmatrix}1\\2\\1\end{bmatrix},\ \mathbf v_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\0\\-1\end{bmatrix},\ \mathbf v_3=\frac{1}{\sqrt3}\begin{bmatrix}1\\-1\\1\end{bmatrix}
$$

(b) ${\sigma_1=\sqrt3}$, ${\sigma_2=1}$, ${\mathbf\Sigma=\begin{bmatrix}\sqrt3&0&0\\0&1&0\end{bmatrix}}$이에요.

(c) ${\mathbf U=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}}$이에요.

(d) $\mathbf U$는 $2\times2$, $\mathbf\Sigma$는 $2\times3$, $\mathbf V$는 $3\times3$이에요.

#### 검산

두 층 ${\frac12\begin{bmatrix}1&2&1\\1&2&1\end{bmatrix}+\frac12\begin{bmatrix}1&0&-1\\-1&0&1\end{bmatrix}}$이 $\mathbf A$예요. ${\mathbf A\mathbf A^\top}$의 고윳값도 $3,1$이에요.

#### 조건·구분

$\mathbf u_i$는 $\mathbf v_i$에서 구해 부호를 맞춰요. $\mathbf\Sigma$는 $\mathbf A$와 같은 크기이고, 특잇값은 고윳값의 제곱근이에요.

#### 용어

- **특잇값 분해(singular value decomposition, SVD)** — $m\times n$ 행렬을 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$로 쓰는 것이에요. $\mathbf U$($m\times m$), $\mathbf V$($n\times n$)는 정규직교행렬, $\mathbf\Sigma$($m\times n$)는 대각에 특잇값을 둔 행렬이에요.
- **특잇값(singular value)** — $\mathbf\Sigma$의 대각에 놓인 양수 ${\sigma_1\ge\sigma_2\ge\cdots}$예요. ${\mathbf A^\top\mathbf A}$의 양의 고윳값의 제곱근이에요.
- **오른쪽 특이벡터(right-singular vector)** — $\mathbf V$의 열 $\mathbf v_i$예요. ${\mathbf A^\top\mathbf A}$의 단위 고유벡터이고 입력 공간 $\mathbb R^n$의 정규직교기저를 이뤄요.
- **왼쪽 특이벡터(left-singular vector)** — $\mathbf U$의 열 $\mathbf u_i$예요. ${\sigma_i\gt0}$이면 ${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$로 구해요.
- **특성다항식(characteristic polynomial)** — ${\det(\mathbf M-\lambda\mathbf I)}$를 $\lambda$의 다항식으로 쓴 것이에요. 근이 고윳값이에요.

#### 출제 근거

MML Example 4.13(수치를 바꾼 변형), 교과서 125–126쪽(PDF 131–132쪽).

수업: 1104 L06 s13(데이터 행렬의 SVD), 1102 특성다항식·스펙트럼 정리.

관련 정리노트: [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

---

<a id="p5"></a>

### P5. 영화 평점 행렬의 랭크 2 근사

MML Example 4.15 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=5)

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

평점표를 ‘층’ 몇 장을 겹친 것으로 보고, 앞의 두 층만 남겨도 원래 평점이 되살아나는지 확인하는 문제예요. 특히 SF 영화를 좋아하지 않는 Chandra의 평점이 어느 층에 담기는지 봐요.

주어진 것은 평점 행렬 ${\mathbf A\in\mathbb R^{4\times3}}$(행 = 영화 Star Wars, Blade Runner, Amelie, Delicatessen, 열 = 관객 Ali, Beatrix, Chandra), 특잇값 ${\sigma_1=9.6438}$, ${\sigma_2=6.3639}$, ${\sigma_3=0.7056}$, 그리고 $\mathbf u_1,\mathbf u_2$(영화별 값)와 $\mathbf v_1,\mathbf v_2$(관객별 값)의 표예요. 랭크 2 근사는 ${\hat{\mathbf A}(2)=\sigma_1\mathbf u_1\mathbf v_1^\top+\sigma_2\mathbf u_2\mathbf v_2^\top}$예요.

(a)는 첫째 층의 Chandra 열 네 값, (b)는 $\hat{\mathbf A}(2)$의 Chandra 열과 실제 평점 ${(1,0,5,4)^\top}$의 비교, (c)는 셋째 층을 버려도 되는지 수치로 판정하는 문항이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘층 $\sigma_i\mathbf u_i\mathbf v_i^\top$’라는 말에서는 정리노트의 **랭크 1 층의 합**을 떠올려요. SVD는 행렬을 층의 합으로 써요. $\mathbf A$는 특잇값이 세 개라 층도 세 장이에요.

$$
\mathbf A=\sigma_1\mathbf u_1\mathbf v_1^\top+\sigma_2\mathbf u_2\mathbf v_2^\top+\sigma_3\mathbf u_3\mathbf v_3^\top
$$

‘Chandra 열’이라는 단서에서는 **외적의 열**을 떠올려요. ${\mathbf u\mathbf v^\top}$의 $(i,j)$ 칸은 $u_iv_j$라서, $j$번째 열은 벡터 $\mathbf u$ 전체에 숫자 $v_j$를 곱한 ${v_j\mathbf u}$예요. Chandra는 셋째 열이니 층 ${\sigma_i\mathbf u_i\mathbf v_i^\top}$의 Chandra 열은 ${\sigma_i\times(\mathbf v_i\text{의 Chandra 성분})\times\mathbf u_i}$예요.

‘버려도 되는지’라는 단서에서는 정리노트의 **Frobenius 제곱오차**를 떠올려요. Frobenius 노름의 제곱 ${\lVert\mathbf M\rVert_F^2}$는 원소 제곱합이고, 앞의 $M$개 층을 남기면 버린 제곱합은 버린 특잇값의 제곱합이에요.

$$
\lVert\mathbf A-\hat{\mathbf A}(M)\rVert_F^2=\sum_{i\gt M}\sigma_i^2
$$

정리노트에서는 중심화한 데이터 행렬로 이 식을 봤지만, 이 식은 어떤 행렬의 SVD에서나 성립해요. 이 문제에서는 버리는 층이 하나뿐이라 아래 (c)에서 원소 제곱합을 직접 계산해 확인할 수 있어요. 에카르트–영 정리(Eckart–Young theorem)에 따라 이렇게 큰 층부터 남긴 근사가 같은 랭크 안에서 제곱오차가 가장 작아요. [작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)에서 같은 식을 다뤘어요.

#### 종이에 쓸 첫 줄

표에서 $\mathbf v_1$의 Chandra 성분 $-0.1811$을 찾아 $\sigma_1$과 먼저 곱해 숫자 하나를 만들어요. 이 숫자를 $\mathbf u_1$의 네 값에 곱할 거예요.

$$
\sigma_1\times(-0.1811)=9.6438\times(-0.1811)=-1.7465
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 첫째 층의 Chandra 열

표의 소수 넷째 자리 값을 그대로 넣어 계산하고, 결과도 넷째 자리로 반올림해요. 첫 줄의 수 ${-1.7465}$(반올림 전 ${-1.74649}$)를 $\mathbf u_1$의 네 값에 곱해요. 예를 들어 Star Wars 자리는 ${(-1.74649)\times(-0.6710)=1.1719}$예요.

$$
-1.7465\,\mathbf u_1=-1.7465\begin{bmatrix}-0.6710\\-0.7197\\-0.0939\\-0.1515\end{bmatrix}=\begin{bmatrix}1.1719\\1.2570\\0.1640\\0.2646\end{bmatrix}
$$

$\mathbf u_1$과 $\mathbf v_1$의 값이 모두 음수라 곱하면 양수가 돼요.

실제 Chandra 평점 ${(1,0,5,4)^\top}$과 비교하면, Star Wars와 Blade Runner 자리는 1 근처라 비슷하지만 Amelie와 Delicatessen의 5점, 4점은 0.16, 0.26으로 거의 못 잡아요. MML의 해석에서 $\mathbf u_1,\mathbf v_1$은 SF 영화와 SF를 좋아하는 관객(Ali, Beatrix)을 나타내요. 프랑스 예술 영화를 좋아하는 Chandra의 취향은 첫째 층에 담기지 않아요.

따라서 **첫째 층의 Chandra 열은 ${(1.1719,\ 1.2570,\ 0.1640,\ 0.2646)^\top}$**이에요.

#### (b) $\hat{\mathbf A}(2)$의 Chandra 열

둘째 층도 같은 방식으로 구해요. $\mathbf v_2$의 Chandra 성분은 $-0.9807$이에요.

$$
\sigma_2\times(-0.9807)=6.3639\times(-0.9807)=-6.2411
$$

$$
-6.2411\,\mathbf u_2=-6.2411\begin{bmatrix}0.0236\\0.2054\\-0.7705\\-0.6030\end{bmatrix}=\begin{bmatrix}-0.1473\\-1.2819\\4.8087\\3.7634\end{bmatrix}
$$

MML의 해석에서 $\mathbf u_2,\mathbf v_2$는 프랑스 예술 영화와 그 애호가(Chandra)를 나타내요. 그래서 Amelie, Delicatessen 자리가 커요.

$\hat{\mathbf A}(2)$의 열은 두 층의 같은 열을 더한 거예요. 반올림하기 전 값으로 더하고 마지막에 넷째 자리로 반올림해요. 예를 들어 Blade Runner 자리는 ${1.25695+(-1.28192)=-0.02497}$이라 $-0.0250$이에요.

$$
\hat{\mathbf A}(2)\text{의 Chandra 열}=\begin{bmatrix}1.0246\\-0.0250\\4.9727\\4.0280\end{bmatrix}\approx\begin{bmatrix}1\\0\\5\\4\end{bmatrix}
$$

실제 평점과의 차이는 ${0.0246,\ 0.0250,\ 0.0273,\ 0.0280}$으로 모두 $0.03$ 이하예요. 따라서 **랭크 2 근사가 Chandra의 평점 ${(1,0,5,4)^\top}$을 거의 그대로 되살려요.**

#### (c) 셋째 층을 버려도 될까

먼저 크기를 비교해요. ${\sigma_3=0.7056}$은 ${\sigma_1=9.6438}$의 약 $0.07$배이고 ${\sigma_2=6.3639}$보다도 훨씬 작아요.

버린 양을 Frobenius 제곱오차로 재요. 세 층의 합에서 앞의 두 층을 빼면 셋째 층만 남아요.

$$
\mathbf A-\hat{\mathbf A}(2)=\sigma_3\mathbf u_3\mathbf v_3^\top
$$

이 층의 $(i,j)$ 칸은 ${\sigma_3u_{3,i}v_{3,j}}$이고, 칸마다 제곱해 모두 더하면 ${\sigma_3^2\big(\sum_iu_{3,i}^2\big)\big(\sum_jv_{3,j}^2\big)}$예요. $\mathbf u_3,\mathbf v_3$는 단위벡터라 두 괄호가 모두 1이에요.

$$
\lVert\mathbf A-\hat{\mathbf A}(2)\rVert_F^2=\sigma_3^2=0.7056^2\approx0.4979
$$

전체 크기와 비교해요. $\mathbf A$의 원소 제곱합은 행마다 ${25+16+1=42}$, ${25+25+0=50}$, ${0+0+25=25}$, ${1+0+16=17}$이라 합이 ${\lVert\mathbf A\rVert_F^2=134}$예요.

$$
\frac{0.4979}{134}\approx0.0037=0.37\%
$$

따라서 **셋째 층을 버려 잃는 양은 전체 제곱합의 약 0.37%뿐이라 버려도 돼요.** MML도 셋째 영화 취향·관객 무리의 증거가 없다고 결론 내려요.

#### 완성 답과 검산

#### (a) 검산

교과서 (4.100b)의 ${\mathbf u_1\mathbf v_1^\top}$ 셋째 열은 ${(0.1215,\ 0.1303,\ 0.0170,\ 0.0274)^\top}$이에요. 여기에 ${\sigma_1=9.6438}$을 곱하면 ${(1.1717,\ 1.2566,\ 0.1639,\ 0.2642)^\top}$이라 (a)의 값과 넷째 자리 반올림 차이 안에서 맞아요.

#### (b) 검산

교과서 (4.102)의 $\hat{\mathbf A}(2)$ 셋째 열은 ${(1.0244,\ -0.0250,\ 4.9724,\ 4.0278)^\top}$이에요. 우리 값과 넷째 자리에서 최대 0.0003 차이인데, 표의 반올림된 값으로 계산했기 때문이에요. 두 값 모두 ${(1,0,5,4)^\top}$에 0.03 이내로 가까워요.

#### (c) 검산

세 특잇값의 제곱은 ${9.6438^2\approx93.003}$, ${6.3639^2\approx40.499}$, ${0.7056^2\approx0.498}$이고, 모두 더하면 ${134.000}$이에요. 원소 제곱합 134와 같아요. 이것은 Frobenius 식에서 아무 층도 남기지 않은 경우(${\lVert\mathbf A\rVert_F^2=\sum_i\sigma_i^2}$)라, 0.37%의 분모로 134를 쓴 것이 맞아요. 남긴 두 층이 ${(93.003+40.499)/134\approx99.63\%}$를 담아요.

#### 이 문항에서 조심할 점

**열과 행을 바꾸면 안 돼요.** Chandra 열은 ${(\mathbf v_1\text{의 Chandra 성분})\times\mathbf u_1}$이에요. 반대로 ${(\mathbf u_1\text{의 셋째 값})\times\mathbf v_1}$, 곧 ${9.6438\times(-0.0939)\times\mathbf v_1}$을 계산하면 ${(0.6671,\ 0.5900,\ 0.1640)}$이 나오는데, 이것은 Amelie 행(세 관객의 Amelie 평점)이에요.

**$\sigma_i$를 빼먹지 않아요.** 교과서는 ${\mathbf A_i=\mathbf u_i\mathbf v_i^\top}$로 쓰고 ${\hat{\mathbf A}(2)=\sigma_1\mathbf A_1+\sigma_2\mathbf A_2}$로 $\sigma$를 따로 곱해요. 이 문제의 ‘층’은 $\sigma_i$까지 곱한 ${\sigma_i\mathbf u_i\mathbf v_i^\top}$예요. 빼먹으면 (a)가 ${(0.1215,\ 0.1303,\ 0.0170,\ 0.0274)^\top}$처럼 평점과 단위가 맞지 않는 작은 값이 나와요.

**단위를 맞춰 비교해요.** 버린 제곱합 ${\sigma_3^2=0.4979}$는 전체 제곱합 134와 비교해요. 제곱하지 않은 ${\sigma_3=0.7056}$을 134로 나누면 서로 다른 단위를 비교하는 거예요.

교과서 값과 넷째 자리가 조금 다른 것은 오류가 아니라 반올림 차이예요. 계산 중간에는 반올림하지 않고 마지막에만 반올림해요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. 외적 ${\mathbf u\mathbf v^\top}$의 $j$번째 열이 ${v_j\mathbf u}$인 이유를 칸 ${u_iv_j}$로 말해요.
2. ${\sigma_1v_{1,\text{Chandra}}}$, ${\sigma_2v_{2,\text{Chandra}}}$를 구해 각각 $\mathbf u_1$, $\mathbf u_2$에 곱하고 더해 ${(1,0,5,4)^\top}$과 비교해요.
3. ${\lVert\mathbf A-\hat{\mathbf A}(2)\rVert_F^2=\sigma_3^2}$를 ${\lVert\mathbf A\rVert_F^2=134}$와 비교해 비율을 구해요.

**페이지 요약**

#### 떠올릴 개념·공식

SVD는 층의 합 ${\sum_i\sigma_i\mathbf u_i\mathbf v_i^\top}$이에요. ${\mathbf u\mathbf v^\top}$의 $j$번째 열은 ${v_j\mathbf u}$예요.

$$
\lVert\mathbf A-\hat{\mathbf A}(M)\rVert_F^2=\sum_{i\gt M}\sigma_i^2
$$

#### 첫 줄

${\sigma_1\times(-0.1811)=-1.7465}$를 먼저 구해 $\mathbf u_1$에 곱해요.

#### 핵심 답

(a) ${(1.1719,\ 1.2570,\ 0.1640,\ 0.2646)^\top}$이라 Amelie·Delicatessen 평점을 거의 못 잡아요.

(b) ${(1.0246,\ -0.0250,\ 4.9727,\ 4.0280)^\top}$으로 ${(1,0,5,4)^\top}$과 거의 같아요.

(c) 버린 제곱오차 ${\sigma_3^2\approx0.4979}$가 전체 134의 약 0.37%라 셋째 층을 버려도 돼요.

#### 검산

교과서 (4.100b), (4.102)와 넷째 자리 반올림 차이 안에서 맞아요. ${\sigma_1^2+\sigma_2^2+\sigma_3^2\approx134}$예요.

#### 조건·구분

열은 $\mathbf v$의 성분 × $\mathbf u$예요. 층에는 $\sigma_i$를 곱해요. 제곱합끼리 비교해요.

#### 용어

- **랭크 1 층(rank-1 matrix)** — ${\sigma_i\mathbf u_i\mathbf v_i^\top}$처럼 열벡터와 행벡터의 외적에 수를 곱한 행렬이에요. 모든 열이 $\mathbf u_i$의 배수예요.
- **랭크 2 근사(rank-2 approximation)** — 앞의 두 층만 더한 ${\hat{\mathbf A}(2)=\sigma_1\mathbf u_1\mathbf v_1^\top+\sigma_2\mathbf u_2\mathbf v_2^\top}$이에요.
- **Frobenius 노름(Frobenius norm)** — 행렬 원소 제곱합의 제곱근이에요. 제곱 ${\lVert\mathbf M\rVert_F^2}$는 원소 제곱합이에요.
- **에카르트–영 정리(Eckart–Young theorem)** — 큰 특잇값의 층부터 $M$개 남긴 근사가 랭크 $M$ 이하 행렬 중 제곱오차가 가장 작다는 정리예요.

#### 출제 근거

MML Example 4.15(그림 4.10, Example 4.14의 평점표와 SVD), 교과서 127쪽·132–133쪽(PDF 133쪽·138–139쪽), 식 (4.100)–(4.103).

수업: 1104 L06 s14(랭크 제한 복원과 Frobenius 오차, 에카르트–영 정리).

관련 정리노트: [작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)

---

<a id="p6"></a>

### P6. 사영을 뺀 나머지도 사영일까

MML Exercise 3.7 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=6)

#### 주어진 조건

$V$는 벡터공간이고 $\pi:V\to V$는 선형사상이에요. $\mathrm{id}_V$는 $V$의 항등사상이에요. 선형사상 $\rho:V\to V$가 $\rho\circ\rho=\rho$를 만족하면 $\rho$를 사영이라고 해요. $\rho^2$은 $\rho\circ\rho$를 뜻해요.

#### 구할 것

- (a) $\pi$가 사영이면 $\mathrm{id}_V-\pi$도 사영임을 증명해 보세요.
- (b) 반대로 $\mathrm{id}_V-\pi$가 사영이면 $\pi$도 사영임을, (a)를 $\rho=\mathrm{id}_V-\pi$에 적용해 증명해 보세요.

<details><summary>원문 보기</summary>

“Prove that π is a projection if and only if idV − π is a projection” — Exercise 3.7

</details>

#### 문제를 내 말로 읽어요

‘사영’은 한 번 하고 나서 다시 해도 결과가 그대로인 연산이에요. 사영 $\pi$가 남긴 부분을 원래 벡터에서 빼는 연산 ${\mathrm{id}_V-\pi}$도 같은 성질을 갖는지, 그리고 그 반대도 성립하는지 증명하는 문제예요.

주어진 것은 벡터공간 $V$, 선형사상 ${\pi:V\to V}$, 항등사상 $\mathrm{id}_V$, 그리고 사영의 정의(선형사상 $\rho$가 ${\rho\circ\rho=\rho}$를 만족)예요. $\rho^2$은 ${\rho\circ\rho}$를 뜻해요.

(a)는 ‘$\pi$가 사영 ⇒ ${\mathrm{id}_V-\pi}$가 사영’, (b)는 반대 방향 ‘${\mathrm{id}_V-\pi}$가 사영 ⇒ $\pi$가 사영’을 (a)를 다시 써서 증명하라고 해요. 두 방향을 합치면 둘이 동치라는 MML Exercise 3.7(a)의 주장이 돼요. 숫자 예 하나로 확인하는 것이 아니라 모든 $V$, 모든 $\pi$에 대해 보여야 해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘사영’이라는 말에서는 1019에서 본 사영행렬의 성질 ${\mathbf P^2=\mathbf P}$를 떠올려요. 이 문제는 행렬 대신 선형사상으로 같은 성질을 정의해요. 두 번 적용한 결과가 한 번 적용한 결과와 같다는 뜻이고, 이런 성질을 멱등성(idempotence)이라고 해요.

$$
\rho\ \text{가 사영}\iff\rho(\rho(\mathbf x))=\rho(\mathbf x)\quad\text{(모든 }\mathbf x\in V\text{)}
$$

‘선형사상’이라는 단서에서는 덧셈과 상수배를 보존하는 성질 ${\pi(\mathbf a-\mathbf b)=\pi(\mathbf a)-\pi(\mathbf b)}$를 떠올려요. 이 성질이 있어야 괄호를 풀 수 있어요. 항등사상은 ${\mathrm{id}_V(\mathbf x)=\mathbf x}$이고, 선형사상 두 개의 차 ${\mathrm{id}_V-\pi}$도 선형사상이라 사영인지 물을 수 있어요.

‘사상이 같다’는 것은 모든 입력에서 출력이 같다는 뜻이에요. 그래서 임의의 $\mathbf x\in V$를 하나 잡고 양쪽 출력을 비교하는 방식으로 증명해요.

PCA에서는 ${\mathbf B^\top\mathbf B=\mathbf I}$인 $\mathbf B$로 만든 복원 ${\tilde{\mathbf x}=\mathbf B\mathbf B^\top\mathbf x}$가 사영이고, 버린 부분 ${\mathbf x-\tilde{\mathbf x}}$를 만드는 연산이 바로 ${\mathbf I-\mathbf B\mathbf B^\top}$예요. [기저를 고정하고 좌표 구하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-projection)와 [버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded)에서 두 부분을 다뤘어요.

#### 종이에 쓸 첫 줄

${I=\mathrm{id}_V}$로 줄여 쓰고, 임의의 $\mathbf x\in V$에 ${I-\pi}$를 두 번 적용한 결과를 적어요. 첫 번째 적용 결과 ${\mathbf x-\pi(\mathbf x)}$를 그대로 두 번째 입력에 넣어요.

$$
(I-\pi)\big((I-\pi)(\mathbf x)\big)=(I-\pi)\big(\mathbf x-\pi(\mathbf x)\big)
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) $\pi$가 사영이면 $\mathrm{id}_V-\pi$도 사영

첫 줄의 오른쪽에서 ${\mathbf y=\mathbf x-\pi(\mathbf x)}$라 두면, ${(I-\pi)(\mathbf y)=\mathbf y-\pi(\mathbf y)}$예요.

$$
(I-\pi)\big(\mathbf x-\pi(\mathbf x)\big)=\big(\mathbf x-\pi(\mathbf x)\big)-\pi\big(\mathbf x-\pi(\mathbf x)\big)
$$

뒤쪽 항의 괄호는 $\pi$가 선형이라 풀 수 있어요. ${\pi(\mathbf x-\pi(\mathbf x))=\pi(\mathbf x)-\pi(\pi(\mathbf x))}$예요.

$$
=\mathbf x-\pi(\mathbf x)-\pi(\mathbf x)+\pi(\pi(\mathbf x))=\mathbf x-2\pi(\mathbf x)+\pi(\pi(\mathbf x))
$$

여기까지는 사영이라는 가정을 쓰지 않았어요. 사상으로 쓰면 ${(I-\pi)^2=I-2\pi+\pi^2}$예요.

이제 가정 ${\pi\circ\pi=\pi}$, 곧 ${\pi(\pi(\mathbf x))=\pi(\mathbf x)}$를 넣어요.

$$
=\mathbf x-2\pi(\mathbf x)+\pi(\mathbf x)=\mathbf x-\pi(\mathbf x)=(I-\pi)(\mathbf x)
$$

임의의 $\mathbf x$에서 두 번 적용한 결과와 한 번 적용한 결과가 같으니 ${(I-\pi)\circ(I-\pi)=I-\pi}$예요. ${I-\pi}$는 선형사상이므로 **${\mathrm{id}_V-\pi}$는 사영이에요.**

#### (b) $\mathrm{id}_V-\pi$가 사영이면 $\pi$도 사영

이번에는 ${\rho=\mathrm{id}_V-\pi}$가 사영이라고 가정해요. $\rho$는 $V$에서 $V$로 가는 선형사상이고 ${\rho\circ\rho=\rho}$예요.

(a)는 ‘어떤 선형사상이든 사영이면, $\mathrm{id}_V$에서 그것을 뺀 것도 사영’이라는 주장이에요. $\pi$ 자리에 무엇을 넣어도 증명이 그대로 성립하니, $\rho$를 넣어 적용할 수 있어요. 그러면 ${\mathrm{id}_V-\rho}$가 사영이에요.

${\mathrm{id}_V-\rho}$를 원래 기호로 되돌려요. 임의의 $\mathbf x$에서 ${(\mathrm{id}_V-\rho)(\mathbf x)=\mathbf x-(\mathbf x-\pi(\mathbf x))=\pi(\mathbf x)}$예요.

$$
\mathrm{id}_V-\rho=\mathrm{id}_V-(\mathrm{id}_V-\pi)=\pi
$$

따라서 **$\pi$가 사영이에요.** (a)와 합치면 ‘$\pi$가 사영 ⇔ ${\mathrm{id}_V-\pi}$가 사영’이에요.

#### 완성 답과 검산

#### (a) 검산

증명의 각 줄이 무엇을 썼는지 다시 점검해요. 괄호 풀기에는 $\pi$의 선형성만, 마지막 줄에는 ${\pi(\pi(\mathbf x))=\pi(\mathbf x)}$만 썼어요. 특정한 $V$나 행렬을 쓰지 않았으니 모든 경우에 성립해요.

보조로 PCA의 사영에 대입해 봐요. ${\mathbf B^\top\mathbf B=\mathbf I}$이면 ${\mathbf P=\mathbf B\mathbf B^\top}$는 ${\mathbf P^2=\mathbf B(\mathbf B^\top\mathbf B)\mathbf B^\top=\mathbf B\mathbf B^\top=\mathbf P}$라 사영이에요. 그리고 ${(\mathbf I-\mathbf P)^2=\mathbf I-2\mathbf P+\mathbf P^2=\mathbf I-\mathbf P}$라서 (a)의 결론과 같아요. 버린 부분 ${\mathbf x-\tilde{\mathbf x}}$에 ${\mathbf I-\mathbf P}$를 한 번 더 적용해도 그대로라는 뜻이에요. 이 대입은 증명이 아니라 결론을 확인하는 예예요.

#### (b) 검산

(a)를 적용할 때 필요한 조건이 모두 있는지 확인해요. (a)의 가정은 ‘$V\to V$ 선형사상이고 사영’이에요. $\rho$는 선형사상 두 개의 차라 선형이고, 사영이라는 것은 (b)의 가정이에요. 결론 ${\mathrm{id}_V-\rho=\pi}$는 모든 입력에서 출력이 같다는 계산으로 확인했어요. 순환 논리 없이 (a)만으로 (b)를 얻었어요.

#### 이 문항에서 조심할 점

**교차항 두 개를 모두 남겨요.** 두 번 적용하면 $-\pi(\mathbf x)$가 두 번 나와요. 한 번만 쓰면 ${\mathbf x-\pi(\mathbf x)+\pi(\pi(\mathbf x))}$가 되고, 가정을 넣으면 $\mathbf x$만 남아 ‘${(I-\pi)^2=I}$’라는 틀린 결론이 나와요.

**한 방향만 보이고 끝내지 않아요.** (a)는 ‘$\pi$가 사영이면’에서 출발한 증명이라 반대 방향을 주지 않아요. (b)에서는 가정이 ‘${\mathrm{id}_V-\pi}$가 사영’으로 바뀌므로, (a)를 $\rho$에 적용하는 단계를 따로 써야 해요.

**숫자 예는 증명이 아니에요.** 사영행렬 하나에서 ${(\mathbf I-\mathbf P)^2=\mathbf I-\mathbf P}$를 확인해도, 다른 모든 $V$와 $\pi$에서 성립한다는 보장은 되지 않아요. 임의의 $\mathbf x$로 일반 계산을 해야 해요.

${\pi\circ\pi=\pi}$라고 해서 $\pi$가 $\mathrm{id}_V$나 영사상이라는 뜻은 아니에요. 예를 들어 $M\lt D$일 때의 ${\mathbf B\mathbf B^\top}$는 사영이지만 둘 다 아니에요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. 임의의 $\mathbf x$에 ${I-\pi}$를 두 번 적용하고, 선형성으로 ${\mathbf x-2\pi(\mathbf x)+\pi(\pi(\mathbf x))}$까지 전개해요.
2. ${\pi(\pi(\mathbf x))=\pi(\mathbf x)}$를 넣어 ${(I-\pi)(\mathbf x)}$가 되는 것을 보여요.
3. ${\rho=\mathrm{id}_V-\pi}$에 (a)를 적용하고 ${\mathrm{id}_V-\rho=\pi}$를 확인해 반대 방향을 끝내요.

**페이지 요약**

#### 떠올릴 개념·공식

사영은 두 번 적용해도 그대로인 선형사상이에요.

$$
\rho\circ\rho=\rho
$$

사상이 같다는 것은 모든 입력에서 출력이 같다는 뜻이라, 임의의 $\mathbf x$로 증명해요.

#### 첫 줄

${(I-\pi)\big((I-\pi)(\mathbf x)\big)=(I-\pi)\big(\mathbf x-\pi(\mathbf x)\big)}$를 적어요.

#### 핵심 답

(a) 선형성으로 ${\mathbf x-2\pi(\mathbf x)+\pi(\pi(\mathbf x))}$, 가정으로 ${\mathbf x-\pi(\mathbf x)}$가 되어 ${\mathrm{id}_V-\pi}$가 사영이에요.

(b) (a)를 ${\rho=\mathrm{id}_V-\pi}$에 적용하면 ${\mathrm{id}_V-\rho=\pi}$가 사영이에요.

#### 검산

(a)는 선형성과 ${\pi\circ\pi=\pi}$만 썼어요. PCA의 ${\mathbf I-\mathbf B\mathbf B^\top}$에서도 결론이 맞아요(예시일 뿐 증명은 아님).

#### 조건·구분

교차항 ${-2\pi}$를 모두 남겨요. 두 방향을 따로 보여요. 숫자 예는 증명이 아니에요.

#### 용어

- **선형사상(linear map)** — ${\pi(\mathbf a+\mathbf b)=\pi(\mathbf a)+\pi(\mathbf b)}$, ${\pi(c\mathbf a)=c\,\pi(\mathbf a)}$를 만족하는 사상이에요. 두 선형사상의 차도 선형사상이에요.
- **항등사상(identity map)** — 모든 $\mathbf x\in V$를 자기 자신으로 보내는 ${\mathrm{id}_V}$예요. 행렬로는 단위행렬 $\mathbf I$예요.
- **사영(projection)** — ${\rho\circ\rho=\rho}$를 만족하는 선형사상 ${\rho:V\to V}$예요. 행렬로는 ${\mathbf P^2=\mathbf P}$예요.
- **합성(composition)** — ${(\rho\circ\pi)(\mathbf x)=\rho(\pi(\mathbf x))}$처럼 한 사상의 출력을 다른 사상에 넣는 것이에요.

#### 출제 근거

MML Exercise 3.7, 교과서 97쪽(PDF 103쪽). 원문 (a)의 ‘필요충분’ 주장을 두 방향 (a), (b)로 나눴어요. 원문 (b)는 이 문항에 들어 있지 않아요.

수업: 1019 사영행렬 ${\mathbf P^2=\mathbf P}$, 1104 L06 s5–10(사영과 버린 부분).

관련 정리노트: [기저를 고정하고 좌표 구하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-projection), [버린 방향에서 복원오차 계산하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s1-discarded)

---

<a id="p7"></a>

### P7. 왼쪽 특이벡터부터 구하는 특잇값 분해

MML Exercise 4.8 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=7)

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

P4와 같은 특잇값 분해인데, 이번에는 크기가 작은 쪽인 ${\mathbf A\mathbf A^\top}$($2\times2$)에서 출발해 $\mathbf U$를 먼저 구하고, 거기서 $\mathbf V$를 거꾸로 얻는 문제예요. 특잇값이 두 개뿐이라 $\mathbf V$의 셋째 열은 다른 방법으로 채워야 해요.

주어진 것은 ${\mathbf A=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}}$예요. (a)는 ${\mathbf A\mathbf A^\top}$의 고윳값과 단위 고유벡터로 $\sigma_1,\sigma_2$와 $\mathbf u_1,\mathbf u_2$, (b)는 ${\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i}$로 $\mathbf v_1,\mathbf v_2$, (c)는 둘에 모두 수직인 단위벡터 $\mathbf v_3$로 $\mathbf V$ 완성, (d)는 ${\mathbf A\mathbf v_3=\mathbf 0}$인지와 그것이 $\mathbf\Sigma$의 셋째 열 0과 맞는지 판정이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘${\mathbf A\mathbf A^\top}$의 고유벡터로 $\mathbf u_i$’라는 단서에서는 정리노트에서 ${\mathbf X\mathbf X^\top}$에 SVD를 넣은 계산을 그대로 떠올려요. ${\mathbf A^\top=\mathbf V\mathbf\Sigma^\top\mathbf U^\top}$이고 ${\mathbf V^\top\mathbf V=\mathbf I}$라 가운데가 사라져요.

$$
\mathbf A\mathbf A^\top=\mathbf U\mathbf\Sigma\mathbf V^\top\mathbf V\mathbf\Sigma^\top\mathbf U^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top
$$

${\mathbf\Sigma\mathbf\Sigma^\top}$는 대각이 ${\sigma_1^2,\sigma_2^2}$인 $2\times2$ 대각행렬이라, **$\mathbf U$의 열이 ${\mathbf A\mathbf A^\top}$의 고유벡터이고 고윳값이 $\sigma_i^2$**예요.

‘${\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i}$’는 ${\mathbf A^\top=\mathbf V\mathbf\Sigma^\top\mathbf U^\top}$의 오른쪽에 $\mathbf U$를 곱한 ${\mathbf A^\top\mathbf U=\mathbf V\mathbf\Sigma^\top}$(${\mathbf U^\top\mathbf U=\mathbf I}$)에서 나와요. ${\mathbf\Sigma^\top}$는 $3\times2$이고 $(i,i)$ 자리에 $\sigma_i$가 있어서, ${\mathbf V\mathbf\Sigma^\top}$의 $i$번째 열은 ${\sigma_i\mathbf v_i}$예요. 열마다 읽으면 ${\mathbf A^\top\mathbf u_i=\sigma_i\mathbf v_i}$예요.

‘모두 수직인 단위벡터’라는 단서에서는 **내적 0 조건**을 떠올려요. $\mathbf V$는 $3\times3$ 정규직교행렬이어야 하니, 셋째 열은 앞의 두 열과의 내적이 0이고 길이가 1이어야 해요. [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)에서 같은 대입을 다뤘어요.

#### 종이에 쓸 첫 줄

$\mathbf A$의 두 행끼리 내적해 ${\mathbf A\mathbf A^\top}$의 네 칸을 적어요. 첫째 행 $(3,2,2)$의 자기 내적은 ${9+4+4=17}$, 두 행의 내적은 ${6+6-4=8}$, 둘째 행 $(2,3,-2)$의 자기 내적은 ${4+9+4=17}$이에요.

$$
\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix}
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) $\sigma_1,\sigma_2$와 $\mathbf u_1,\mathbf u_2$

특성다항식을 ${ad-bc}$로 세워요.

$$
\det(\mathbf A\mathbf A^\top-\lambda\mathbf I)=(17-\lambda)^2-64=0
$$

${(17-\lambda)^2=64}$라 ${17-\lambda=\pm8}$이고, 고윳값은 ${25,\ 9}$예요. 특잇값은 그 제곱근이라 ${\sigma_1=5}$, ${\sigma_2=3}$이에요.

${\lambda=25}$를 넣으면 행렬이 ${\begin{bmatrix}-8&8\\8&-8\end{bmatrix}}$이라 첫째 행 ${-8u_1+8u_2=0}$에서 ${u_1=u_2}$예요. ${\lambda=9}$를 넣으면 ${\begin{bmatrix}8&8\\8&8\end{bmatrix}}$이라 ${8u_1+8u_2=0}$에서 ${u_2=-u_1}$이에요. 길이 $\sqrt2$로 나눠 정규화해요.

$$
\mathbf u_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},\qquad\mathbf u_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}
$$

#### (b) $\mathbf v_1,\mathbf v_2$

$\mathbf A^\top$는 $\mathbf A$의 행을 열로 세운 $3\times2$ 행렬이에요. ${\mathbf A^\top(1,1)^\top}$은 두 열을 더한 ${(3+2,\ 2+3,\ 2-2)^\top=(5,5,0)^\top}$, ${\mathbf A^\top(1,-1)^\top}$은 첫 열에서 둘째 열을 뺀 ${(1,-1,4)^\top}$이에요.

$$
\mathbf v_1=\frac{\mathbf A^\top\mathbf u_1}{\sigma_1}=\frac{1}{5\sqrt2}\begin{bmatrix}5\\5\\0\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\\0\end{bmatrix}
$$

$$
\mathbf v_2=\frac{\mathbf A^\top\mathbf u_2}{\sigma_2}=\frac{1}{3\sqrt2}\begin{bmatrix}1\\-1\\4\end{bmatrix}
$$

$\mathbf v_2$의 길이 제곱은 ${(1+1+16)/18=1}$이라 단위벡터예요. ${\mathbf v_1^\top\mathbf v_2\propto1-1+0=0}$이라 서로 수직이에요.

#### (c) $\mathbf v_3$와 $\mathbf V$

특잇값은 두 개뿐이라 ${\mathbf A^\top\mathbf u_3/\sigma_3}$ 같은 식이 없어요. 그래도 $\mathbf V$는 $3\times3$ 정규직교행렬이어야 하니, $\mathbf v_1,\mathbf v_2$에 모두 수직인 단위벡터로 셋째 열을 채워요.

${\mathbf v_3\propto(a,b,c)^\top}$로 두고 두 내적을 0으로 놓아요. 앞의 상수 ${\frac{1}{\sqrt2}}$, ${\frac{1}{3\sqrt2}}$는 0과의 비교에 영향을 주지 않아 빼고 써요.

$$
(1,1,0)\cdot(a,b,c)=a+b=0,\qquad(1,-1,4)\cdot(a,b,c)=a-b+4c=0
$$

첫 식에서 ${b=-a}$를 둘째 식에 넣으면 ${2a+4c=0}$, ${c=-a/2}$예요. 분수를 피하려고 ${a=2}$로 두면 ${(2,-2,-1)^\top}$이고, 길이는 ${\sqrt{4+4+1}=3}$이에요.

$$
\mathbf v_3=\frac13\begin{bmatrix}2\\-2\\-1\end{bmatrix}
$$

$$
\mathbf V=\begin{bmatrix}\frac{1}{\sqrt2}&\frac{1}{3\sqrt2}&\frac23\\\frac{1}{\sqrt2}&-\frac{1}{3\sqrt2}&-\frac23\\0&\frac{4}{3\sqrt2}&-\frac13\end{bmatrix}
$$

$\mathbf v_3$는 부호를 바꾼 ${-\mathbf v_3}$도 정답이에요. $\mathbf u_i$의 부호를 바꾸면 ${\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i}$의 부호도 함께 바뀌어요.

#### (d) $\mathbf A\mathbf v_3=\mathbf 0$ 판정

직접 계산해요. 첫째 행과의 내적은 ${3\cdot2+2\cdot(-2)+2\cdot(-1)=0}$, 둘째 행과의 내적은 ${2\cdot2+3\cdot(-2)+(-2)\cdot(-1)=0}$이에요.

$$
\mathbf A\mathbf v_3=\frac13\begin{bmatrix}6-4-2\\4-6+2\end{bmatrix}=\begin{bmatrix}0\\0\end{bmatrix}
$$

왜 0이 되는지도 봐요. $\mathbf A$의 두 행은 ${(5,5,0)}$과 ${(1,-1,4)}$로 쓸 수 있어요.

$$
(3,2,2)=\tfrac12(5,5,0)+\tfrac12(1,-1,4),\qquad(2,3,-2)=\tfrac12(5,5,0)-\tfrac12(1,-1,4)
$$

${(5,5,0)}$은 $\mathbf v_1$ 방향, ${(1,-1,4)}$는 $\mathbf v_2$ 방향이라, 둘에 모두 수직인 $\mathbf v_3$는 두 행과의 내적이 0일 수밖에 없어요.

이제 $\mathbf\Sigma$와 비교해요. ${\mathbf\Sigma=\begin{bmatrix}5&0&0\\0&3&0\end{bmatrix}}$의 셋째 열은 $\mathbf 0$이에요. ${\mathbf A\mathbf V=\mathbf U\mathbf\Sigma}$의 셋째 열을 읽으면 왼쪽은 ${\mathbf A\mathbf v_3}$, 오른쪽은 ${\mathbf U\cdot\mathbf 0=\mathbf 0}$이에요. 따라서 **${\mathbf A\mathbf v_3=\mathbf 0}$이고, 이것은 $\mathbf\Sigma$의 셋째 열이 0인 것과 정확히 맞아요.** 앞의 두 열 ${\mathbf A\mathbf v_i=\sigma_i\mathbf u_i}$와 합쳐 ${\mathbf A\mathbf V=\mathbf U\mathbf\Sigma}$가 세 열 모두 성립하고, ${\mathbf V\mathbf V^\top=\mathbf I}$라 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$예요.

#### 완성 답과 검산

#### (a) 검산

${\mathbf A\mathbf A^\top(1,1)^\top}$는 ${(17+8,\ 8+17)^\top=25(1,1)^\top}$이고, ${\mathbf A\mathbf A^\top(1,-1)^\top}$는 ${(17-8,\ 8-17)^\top=9(1,-1)^\top}$이에요. 원소 제곱합 ${9+4+4+4+9+4=34}$가 ${\sigma_1^2+\sigma_2^2=25+9}$와도 같아요.

#### (b) 검산

${\mathbf A\mathbf v_i=\sigma_i\mathbf u_i}$도 맞는지 봐요. ${\mathbf A(1,1,0)^\top=(5,5)^\top}$이라 ${\mathbf A\mathbf v_1=\frac{1}{\sqrt2}(5,5)^\top=5\mathbf u_1}$이고, ${\mathbf A(1,-1,4)^\top}$는 ${(3-2+8,\ 2-3-8)^\top}$, 곧 ${(9,-9)^\top}$이라 ${\mathbf A\mathbf v_2=\frac{1}{3\sqrt2}(9,-9)^\top=3\mathbf u_2}$예요.

#### (c) 검산

${\mathbf v_1^\top\mathbf v_3\propto2-2+0=0}$, ${\mathbf v_2^\top\mathbf v_3\propto2+2-4=0}$, ${\lVert\mathbf v_3\rVert^2=(4+4+1)/9=1}$이에요. 세 열이 정규직교라 ${\mathbf V^\top\mathbf V=\mathbf I}$예요.

#### (d) 검산

층 두 개를 더해 $\mathbf A$가 나오는지 봐요. ${5\mathbf u_1\mathbf v_1^\top}$의 계수는 ${5\cdot\frac12}$, ${3\mathbf u_2\mathbf v_2^\top}$의 계수는 ${3\cdot\frac{1}{\sqrt2}\cdot\frac{1}{3\sqrt2}=\frac12}$이에요.

$$
\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}+\frac12\begin{bmatrix}1&-1&4\\-1&1&-4\end{bmatrix}=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}
$$

$\mathbf v_3$가 들어간 층이 없어도 $\mathbf A$가 완성되니, $\mathbf v_3$ 방향은 $\mathbf A$가 0으로 보낸다는 판정과 맞아요.

#### 이 문항에서 조심할 점

**$\mathbf v_i$를 $\mathbf A^\top\mathbf A$에서 따로 구해 부호를 마음대로 정하면 안 돼요.** 예를 들어 $\mathbf v_2$ 대신 ${-\mathbf v_2}$를 쓰고 $\mathbf u_2$는 그대로 두면, 둘째 층의 부호가 뒤집혀 두 행이 바뀐 행렬이 나와요.

$$
\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}-\frac12\begin{bmatrix}1&-1&4\\-1&1&-4\end{bmatrix}
$$

$$
=\begin{bmatrix}2&3&-2\\3&2&2\end{bmatrix}\ne\mathbf A
$$

${\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i}$로 구하면 부호가 저절로 맞아요.

$\sigma_i$로 나누는 것을 빼먹지 않아요. ${\mathbf A^\top\mathbf u_1=\frac{1}{\sqrt2}(5,5,0)^\top}$의 길이는 5라서, 나누지 않으면 단위벡터가 아니에요.

$\mathbf v_3$를 ${\mathbf A^\top\mathbf u_3/\sigma_3}$로 구하려 하면 안 돼요. $\mathbf u$와 $\sigma$는 두 개뿐이에요. 셋째 열은 수직 조건으로만 정해져요.

$\mathbf\Sigma$는 $\mathbf A$와 같은 $2\times3$ 크기예요. ${\mathbf\Sigma=\operatorname{diag}(5,3)}$인 $2\times2$로 쓰면 ${\mathbf U\mathbf\Sigma\mathbf V^\top}$의 곱셈 크기가 맞지 않아요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. ${\mathbf A\mathbf A^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top}$에서 왜 $\mathbf u_i$와 $\sigma_i^2$를 얻는지 말하고, ${(17-\lambda)^2-64=0}$을 풀어요.
2. ${\mathbf A^\top\mathbf U=\mathbf V\mathbf\Sigma^\top}$에서 ${\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i}$를 이끌어 $\mathbf v_1,\mathbf v_2$를 구해요.
3. 두 내적 0 조건으로 $\mathbf v_3$를 구하고, ${\mathbf A\mathbf v_3=\mathbf 0}$을 ${\mathbf A\mathbf V=\mathbf U\mathbf\Sigma}$의 셋째 열과 연결해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mathbf U$의 열은 ${\mathbf A\mathbf A^\top}$의 고유벡터, 고윳값은 $\sigma_i^2$예요.

$$
\mathbf A\mathbf A^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top
$$

${\mathbf A^\top\mathbf U=\mathbf V\mathbf\Sigma^\top}$를 열마다 읽으면 ${\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i}$예요.

#### 첫 줄

두 행끼리의 내적으로 ${\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix}}$을 적어요.

#### 핵심 답

(a) ${\sigma_1=5}$, ${\sigma_2=3}$, ${\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top}$, ${\mathbf u_2=\frac{1}{\sqrt2}(1,-1)^\top}$이에요.

(b) ${\mathbf v_1=\frac{1}{\sqrt2}(1,1,0)^\top}$, ${\mathbf v_2=\frac{1}{3\sqrt2}(1,-1,4)^\top}$이에요.

(c) ${\mathbf v_3=\frac13(2,-2,-1)^\top}$이에요.

(d) ${\mathbf A\mathbf v_3=\mathbf 0}$이라 $\mathbf\Sigma$의 셋째 열이 0인 것과 맞아요.

#### 검산

${\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}+\frac12\begin{bmatrix}1&-1&4\\-1&1&-4\end{bmatrix}=\mathbf A}$예요. ${\mathbf A\mathbf v_i=\sigma_i\mathbf u_i}$도 맞아요.

#### 조건·구분

$\mathbf v_i$는 $\mathbf u_i$에서 구해 부호를 맞춰요. $\mathbf v_3$는 수직 조건으로 정하고 부호는 자유예요. $\mathbf\Sigma$는 $2\times3$이에요.

#### 용어

- **왼쪽 특이벡터(left-singular vector)** — $\mathbf U$의 열 $\mathbf u_i$예요. ${\mathbf A\mathbf A^\top}$의 단위 고유벡터이고 고윳값은 $\sigma_i^2$예요.
- **오른쪽 특이벡터(right-singular vector)** — $\mathbf V$의 열 $\mathbf v_i$예요. ${\sigma_i\gt0}$이면 ${\mathbf v_i=\mathbf A^\top\mathbf u_i/\sigma_i}$로 구해요. 특잇값이 없는 자리의 열은 앞의 열들에 수직인 단위벡터로 채워요.
- **특잇값(singular value)** — ${\mathbf A\mathbf A^\top}$(또는 ${\mathbf A^\top\mathbf A}$)의 양의 고윳값의 제곱근이에요.
- **정규직교행렬(orthogonal matrix)** — 열이 서로 수직이고 길이가 1인 정사각행렬이에요. ${\mathbf V^\top\mathbf V=\mathbf V\mathbf V^\top=\mathbf I}$예요.

#### 출제 근거

MML Exercise 4.8, 교과서 138쪽(PDF 144쪽). 원문은 ‘SVD를 구하라’는 한 문장이고, 이 문항은 ${\mathbf A\mathbf A^\top}$에서 시작하는 (a)–(d) 단계로 나눴어요.

수업: 1104 L06 s13(데이터 행렬의 SVD), 1102 특성다항식.

관련 정리노트: [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

---

<a id="p8"></a>

### P8. 2×2 행렬의 특잇값 분해

MML Exercise 4.9 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=8)

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

$2\times2$ 정사각행렬의 특잇값 분해를 구하고, 마지막에 반대쪽 ${\mathbf A\mathbf A^\top}$로 답이 맞는지 스스로 판정하는 문제예요.

주어진 것은 ${\mathbf A=\begin{bmatrix}2&2\\-1&1\end{bmatrix}}$예요. (a)는 ${\mathbf A^\top\mathbf A}$의 고윳값과 단위 고유벡터로 $\mathbf V$를, (b)는 특잇값과 ${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$로 $\mathbf U$를 구하고, (c)는 ${\mathbf A\mathbf A^\top}$를 직접 계산해 (b)의 $\mathbf u_1,\mathbf u_2$가 그 고유벡터이고 고윳값이 $\sigma_i^2$인지 판정해요.

$\mathbf A$는 정사각행렬이지만 대칭이 아니에요. 그래서 $\mathbf U$와 $\mathbf V$가 서로 다를 수 있어요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘${\mathbf A^\top\mathbf A}$의 고유벡터로 $\mathbf V$’라는 단서에서는 정리노트의 SVD 대입을 반대쪽에 적용해요. ${\mathbf U^\top\mathbf U=\mathbf I}$라 가운데가 사라져요.

$$
\mathbf A^\top\mathbf A=\mathbf V\mathbf\Sigma^\top\mathbf U^\top\mathbf U\mathbf\Sigma\mathbf V^\top=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top
$$

${\mathbf\Sigma^\top\mathbf\Sigma=\operatorname{diag}(\sigma_1^2,\sigma_2^2)}$라서 **$\mathbf V$의 열이 ${\mathbf A^\top\mathbf A}$의 고유벡터이고 고윳값이 $\sigma_i^2$**예요. 특잇값은 고윳값의 제곱근이에요.

‘${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$’는 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$의 오른쪽에 $\mathbf V$를 곱한 ${\mathbf A\mathbf V=\mathbf U\mathbf\Sigma}$를 열마다 읽은 ${\mathbf A\mathbf v_i=\sigma_i\mathbf u_i}$에서 나와요.

‘${\mathbf A\mathbf A^\top}$의 고유벡터인지 판정’에서는 같은 대입을 다른 쪽에 한 ${\mathbf A\mathbf A^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top}$를 떠올려요. 이 식이 맞다면 $\mathbf u_i$는 ${\mathbf A\mathbf A^\top}$의 고유벡터이고 고윳값은 같은 $\sigma_i^2$여야 해요. 판정은 고유벡터의 정의 ${\mathbf A\mathbf A^\top\mathbf u_i=\sigma_i^2\mathbf u_i}$에 직접 대입해서 해요. [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)에서 같은 대입을 다뤘어요.

#### 종이에 쓸 첫 줄

$\mathbf A$의 두 열끼리 내적해 ${\mathbf A^\top\mathbf A}$를 적어요. 첫째 열 $(2,-1)$의 자기 내적은 ${4+1=5}$, 두 열의 내적은 ${4-1=3}$, 둘째 열 $(2,1)$의 자기 내적은 ${4+1=5}$예요.

$$
\mathbf A^\top\mathbf A=\begin{bmatrix}5&3\\3&5\end{bmatrix}
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) 고윳값과 $\mathbf V$

특성다항식은 ${(5-\lambda)^2-9=0}$이라 ${5-\lambda=\pm3}$이고, 고윳값은 큰 순서로 ${8,\ 2}$예요.

${\lambda=8}$이면 행렬이 ${\begin{bmatrix}-3&3\\3&-3\end{bmatrix}}$이라 ${-3v_1+3v_2=0}$, ${v_1=v_2}$예요. ${\lambda=2}$이면 ${\begin{bmatrix}3&3\\3&3\end{bmatrix}}$이라 ${3v_1+3v_2=0}$, ${v_2=-v_1}$이에요. 길이 $\sqrt2$로 나눠 큰 고윳값 순서로 열에 놓아요.

$$
\mathbf v_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},\qquad\mathbf v_2=\frac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}
$$

$$
\mathbf V=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}
$$

#### (b) 특잇값과 $\mathbf U$

특잇값은 고윳값의 제곱근이에요. ${\sqrt8=2\sqrt2}$예요.

$$
\sigma_1=2\sqrt2,\qquad\sigma_2=\sqrt2,\qquad\mathbf\Sigma=\begin{bmatrix}2\sqrt2&0\\0&\sqrt2\end{bmatrix}
$$

$\mathbf A$에 정규화 전 벡터를 곱해요. ${\mathbf A(1,1)^\top=(2+2,\ -1+1)^\top=(4,0)^\top}$, ${\mathbf A(1,-1)^\top=(2-2,\ -1-1)^\top=(0,-2)^\top}$이에요.

$$
\mathbf u_1=\frac{1}{2\sqrt2}\cdot\frac{1}{\sqrt2}\begin{bmatrix}4\\0\end{bmatrix}=\frac14\begin{bmatrix}4\\0\end{bmatrix}=\begin{bmatrix}1\\0\end{bmatrix}
$$

$$
\mathbf u_2=\frac{1}{\sqrt2}\cdot\frac{1}{\sqrt2}\begin{bmatrix}0\\-2\end{bmatrix}=\begin{bmatrix}0\\-1\end{bmatrix}
$$

$$
\mathbf U=\begin{bmatrix}1&0\\0&-1\end{bmatrix}
$$

${\mathbf u_1^\top\mathbf u_2=0}$이고 길이가 모두 1이라 $\mathbf U$는 정규직교행렬이에요. ${\mathbf A\mathbf V=\mathbf U\mathbf\Sigma}$가 두 열 모두 맞고 ${\mathbf V\mathbf V^\top=\mathbf I}$라, 오른쪽에 $\mathbf V^\top$를 곱하면 ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$예요.

$\mathbf v_2$의 부호를 반대로 골라 ${-\frac{1}{\sqrt2}(1,-1)^\top}$을 쓰면 ${\mathbf u_2=(0,1)^\top}$이 나와요. $\mathbf v_i$와 $\mathbf u_i$의 부호가 함께 바뀌므로 이것도 정답이에요.

#### (c) $\mathbf A\mathbf A^\top$로 판정

${\mathbf A\mathbf A^\top}$의 칸은 $\mathbf A$의 두 행끼리의 내적이에요. 첫째 행 $(2,2)$의 자기 내적은 8, 두 행 $(2,2)$와 $(-1,1)$의 내적은 ${-2+2=0}$, 둘째 행의 자기 내적은 2예요.

$$
\mathbf A\mathbf A^\top=\begin{bmatrix}8&0\\0&2\end{bmatrix}
$$

(b)의 $\mathbf u_1,\mathbf u_2$를 고유벡터 정의에 대입해요.

$$
\mathbf A\mathbf A^\top\mathbf u_1=\begin{bmatrix}8\\0\end{bmatrix}=8\mathbf u_1,\qquad\mathbf A\mathbf A^\top\mathbf u_2=\begin{bmatrix}0\\-2\end{bmatrix}=2\mathbf u_2
$$

고윳값 8과 2는 ${\sigma_1^2=(2\sqrt2)^2=8}$, ${\sigma_2^2=(\sqrt2)^2=2}$와 같아요. 따라서 **(b)의 $\mathbf u_1,\mathbf u_2$는 ${\mathbf A\mathbf A^\top}$의 고유벡터이고, 고윳값도 $\sigma_i^2$가 맞아요.** ${\mathbf A^\top\mathbf A}$와 ${\mathbf A\mathbf A^\top}$가 서로 다른 행렬인데도 같은 고윳값 8, 2를 가져요.

#### 완성 답과 검산

#### (a) 검산

${\mathbf A^\top\mathbf A(1,1)^\top=(5+3,\ 3+5)^\top=8(1,1)^\top}$, ${\mathbf A^\top\mathbf A(1,-1)^\top=(5-3,\ 3-5)^\top=2(1,-1)^\top}$이에요. 두 열의 내적은 ${\frac12(1-1)=0}$이라 $\mathbf V$는 정규직교행렬이에요.

#### (b) 검산

세 행렬을 곱해 $\mathbf A$가 나오는지 봐요. 먼저 ${\mathbf U\mathbf\Sigma=\begin{bmatrix}2\sqrt2&0\\0&-\sqrt2\end{bmatrix}}$예요.

$$
\mathbf U\mathbf\Sigma\mathbf V^\top=\begin{bmatrix}2\sqrt2&0\\0&-\sqrt2\end{bmatrix}\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}=\begin{bmatrix}2&2\\-1&1\end{bmatrix}
$$

원래 $\mathbf A$와 같아요. ($\mathbf V$는 대칭이라 ${\mathbf V^\top=\mathbf V}$예요.)

#### (c) 검산

${\mathbf A\mathbf A^\top}$를 SVD로 계산해도 같아야 해요. 계산하면 직접 계산한 값과 같아요.

$$
\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top=\begin{bmatrix}1&0\\0&-1\end{bmatrix}\begin{bmatrix}8&0\\0&2\end{bmatrix}\begin{bmatrix}1&0\\0&-1\end{bmatrix}
$$

$$
=\begin{bmatrix}8&0\\0&2\end{bmatrix}
$$

#### 이 문항에서 조심할 점

**$\mathbf u_i$를 ${\mathbf A\mathbf A^\top}$에서 따로 골라 부호를 정하면 안 돼요.** ${\mathbf A\mathbf A^\top=\operatorname{diag}(8,2)}$의 단위 고유벡터로 ${(0,1)^\top}$도 고를 수 있지만, ${\mathbf v_2=\frac{1}{\sqrt2}(1,-1)^\top}$을 그대로 두고 ${\mathbf u_2=(0,1)^\top}$을 쓰면 둘째 층의 부호가 뒤집혀 ${\mathbf U\mathbf\Sigma\mathbf V^\top=\begin{bmatrix}2&2\\1&-1\end{bmatrix}}$이 되어 $\mathbf A$와 달라요. (c)는 부호를 정하는 단계가 아니라 (b)의 결과를 판정하는 단계예요.

**특잇값은 고윳값의 제곱근이에요.** ${\sigma_1=8}$로 쓰면 ${\mathbf u_1=\mathbf A\mathbf v_1/8}$의 길이가 ${\frac{4/\sqrt2}{8}=\frac{1}{2\sqrt2}}$이라 단위벡터가 아니에요.

**$\mathbf A$ 자신의 고윳값과 특잇값은 달라요.** $\mathbf A$는 대칭이 아니라 ${\det(\mathbf A-\lambda\mathbf I)=(2-\lambda)(1-\lambda)+2}$이고 전개하면 ${\lambda^2-3\lambda+4}$인데, 판별식이 ${9-16=-7\lt0}$이라 실수 고윳값이 없어요. 특잇값은 항상 ${\mathbf A^\top\mathbf A}$에서 구해요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. ${\mathbf A^\top\mathbf A}$를 열끼리의 내적으로 구하고 ${(5-\lambda)^2-9=0}$을 풀어 $\mathbf V$를 만들어요.
2. ${\sigma_i=\sqrt{\lambda_i}}$를 구하고 ${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$로 $\mathbf U$를 만들어요.
3. ${\mathbf A\mathbf A^\top}$를 행끼리의 내적으로 구하고 ${\mathbf A\mathbf A^\top\mathbf u_i=\sigma_i^2\mathbf u_i}$에 대입해 판정해요.

**페이지 요약**

#### 떠올릴 개념·공식

${\mathbf A^\top\mathbf A=\mathbf V(\mathbf\Sigma^\top\mathbf\Sigma)\mathbf V^\top}$, ${\mathbf A\mathbf A^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top}$예요. 두 행렬의 고윳값이 모두 $\sigma_i^2$예요.

${\mathbf u_i=\mathbf A\mathbf v_i/\sigma_i}$예요.

#### 첫 줄

열끼리의 내적으로 ${\mathbf A^\top\mathbf A=\begin{bmatrix}5&3\\3&5\end{bmatrix}}$를 적어요.

#### 핵심 답

(a) 고윳값 ${8,2}$, ${\mathbf V=\frac{1}{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}}$이에요.

(b) ${\sigma_1=2\sqrt2}$, ${\sigma_2=\sqrt2}$, ${\mathbf U=\begin{bmatrix}1&0\\0&-1\end{bmatrix}}$이에요.

(c) ${\mathbf A\mathbf A^\top=\operatorname{diag}(8,2)}$라 $\mathbf u_1,\mathbf u_2$는 고윳값 ${\sigma_1^2=8}$, ${\sigma_2^2=2}$의 고유벡터가 맞아요.

#### 검산

${\mathbf U\mathbf\Sigma\mathbf V^\top}$을 곱하면 $\mathbf A$예요. ${\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top=\operatorname{diag}(8,2)}$도 맞아요.

#### 조건·구분

$\mathbf u_i$는 $\mathbf v_i$에서 구해 부호를 맞춰요. 특잇값은 고윳값의 제곱근이고, $\mathbf A$ 자신의 고윳값과 달라요.

#### 용어

- **특잇값 분해(singular value decomposition, SVD)** — ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$로 쓰는 것이에요. 정사각행렬이어도 $\mathbf U$와 $\mathbf V$는 서로 다를 수 있어요.
- **특잇값(singular value)** — ${\mathbf A^\top\mathbf A}$의 양의 고윳값의 제곱근이에요. ${\mathbf A\mathbf A^\top}$의 양의 고윳값과도 같아요.
- **고유벡터(eigenvector)** — ${\mathbf M\mathbf x=\lambda\mathbf x}$를 만족하는 0이 아닌 벡터예요. 판정은 직접 곱해 상수배인지 확인해요.
- **대각행렬(diagonal matrix)** — 비대각 원소가 모두 0인 정사각행렬이에요. ${\operatorname{diag}(8,2)}$의 고유벡터는 표준기저 방향이에요.

#### 출제 근거

MML Exercise 4.9, 교과서 138쪽(PDF 144쪽). 원문은 ‘SVD를 구하라’는 한 문장이고, 이 문항은 (a), (b)와 ${\mathbf A\mathbf A^\top}$ 판정 (c)로 나눴어요.

수업: 1104 L06 s13(데이터 행렬의 SVD), 1102 특성다항식.

관련 정리노트: [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

---

<a id="p9"></a>

### P9. 가장 큰 특잇값으로 만든 랭크 1 근사

MML Exercise 4.10 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=9)

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

행렬을 층 여러 장의 합으로 보고, 가장 진한 첫 층 한 장만 남겨 원래 행렬을 흉내 내는 문제예요. 남긴 층과 원래 행렬의 차이가 얼마인지도 직접 재 봐요.

주어진 것은 ${\mathbf A=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}}$와 Frobenius 노름의 제곱 ${\lVert\mathbf M\rVert_F^2}$ = 원소 제곱합이라는 정의예요. (a)는 가장 큰 특잇값 $\sigma_1$과 단위 특이벡터 $\mathbf u_1,\mathbf v_1$, (b)는 랭크 1 근사 ${\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top}$, (c)는 ${\mathbf A-\mathbf A_1}$의 원소 제곱합이 ${\sigma_2^2}$와 같은지 판정이에요.

P7과 같은 행렬이라 P7의 결과를 써도 되지만, 이 문항에서 필요한 첫 층만 다시 구해 볼게요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘랭크 1 근사’라는 말에서는 정리노트의 **랭크 제한 복원**을 떠올려요. SVD는 층의 합 ${\mathbf A=\sum_i\sigma_i\mathbf u_i\mathbf v_i^\top}$이고, 앞의 $M$개 층만 남긴 것이 랭크 $M$ 근사예요. $M=1$이면 첫 층 하나예요.

$$
\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top
$$

에카르트–영 정리(Eckart–Young theorem)에 따라 이 첫 층이 랭크 1 이하의 모든 행렬 중 원소 제곱합 오차가 가장 작아요.

‘$\mathbf A-\mathbf A_1$의 원소 제곱합’이라는 단서에서는 **버린 특잇값의 제곱합**을 떠올려요.

$$
\lVert\mathbf A-\mathbf A_M\rVert_F^2=\sum_{i\gt M}\sigma_i^2
$$

$\sigma_1,\mathbf u_1$은 ${\mathbf A\mathbf A^\top=\mathbf U(\mathbf\Sigma\mathbf\Sigma^\top)\mathbf U^\top}$의 가장 큰 고윳값과 그 단위 고유벡터에서, $\mathbf v_1$은 ${\mathbf A^\top\mathbf u_1=\sigma_1\mathbf v_1}$에서 구해요(P7과 같은 이유). [작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)에서 같은 식을 다뤘어요.

#### 종이에 쓸 첫 줄

두 행끼리 내적해 ${\mathbf A\mathbf A^\top}$를 적고 특성다항식을 세워요. 자기 내적은 ${9+4+4=17}$, 두 행의 내적은 ${6+6-4=8}$이에요.

$$
\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix},\qquad(17-\lambda)^2-64=0
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) $\sigma_1$, $\mathbf u_1$, $\mathbf v_1$

${17-\lambda=\pm8}$이라 고윳값은 ${25,\ 9}$이고, 특잇값은 그 제곱근 ${\sigma_1=5}$, ${\sigma_2=3}$이에요. 가장 큰 것은 ${\sigma_1=5}$예요.

${\lambda=25}$에서 첫째 행 ${-8u_1+8u_2=0}$이라 ${u_1=u_2}$이고, 길이 $\sqrt2$로 나눠요.

$$
\mathbf u_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}
$$

${\mathbf A^\top\mathbf u_1=\sigma_1\mathbf v_1}$을 써요. ${\mathbf A^\top(1,1)^\top}$은 $\mathbf A$의 두 행을 더한 ${(5,5,0)^\top}$이에요.

$$
\mathbf v_1=\frac{\mathbf A^\top\mathbf u_1}{\sigma_1}=\frac{1}{5\sqrt2}\begin{bmatrix}5\\5\\0\end{bmatrix}=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\\0\end{bmatrix}
$$

#### (b) 랭크 1 근사 $\mathbf A_1$

외적 ${\mathbf u_1\mathbf v_1^\top}$의 $(i,j)$ 칸은 ${u_{1,i}v_{1,j}}$예요. 각 칸은 ${\frac{1}{\sqrt2}\cdot\frac{1}{\sqrt2}=\frac12}$ 또는 ($\mathbf v_1$의 셋째 성분이 0이라) 0이에요.

$$
\mathbf u_1\mathbf v_1^\top=\frac12\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}
$$

여기에 ${\sigma_1=5}$를 곱해요.

$$
\mathbf A_1=5\cdot\frac12\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}=\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}
$$

두 행이 같아 랭크가 1이에요. 원래 $\mathbf A$의 두 행 ${(3,2,2)}$, ${(2,3,-2)}$에서 공통으로 큰 앞의 두 성분을 평균 ${2.5}$로 담고, 부호가 반대인 셋째 성분은 0으로 둔 모양이에요.

#### (c) $\lVert\mathbf A-\mathbf A_1\rVert_F^2$와 $\sigma_2^2$

원래 행렬에서 칸마다 빼요. ${3-\frac52=\frac12}$, ${2-\frac52=-\frac12}$, ${2-0=2}$처럼 계산해요.

$$
\mathbf A-\mathbf A_1=\begin{bmatrix}\frac12&-\frac12&2\\-\frac12&\frac12&-2\end{bmatrix}
$$

원소를 하나씩 제곱해 더해요.

$$
\lVert\mathbf A-\mathbf A_1\rVert_F^2=\tfrac14+\tfrac14+4+\tfrac14+\tfrac14+4=9
$$

${\sigma_2^2=3^2=9}$와 같아요. $2\times3$ 행렬이라 특잇값은 두 개뿐이고, 첫 층을 남긴 뒤 버린 특잇값 제곱합은 ${\sum_{i\gt1}\sigma_i^2=\sigma_2^2}$뿐이에요. 따라서 **${\lVert\mathbf A-\mathbf A_1\rVert_F^2=9=\sigma_2^2}$로 같아요.**

#### 완성 답과 검산

#### (a) 검산

${\mathbf A\mathbf v_1=\frac{1}{\sqrt2}(3+2,\ 2+3)^\top=\frac{1}{\sqrt2}(5,5)^\top=5\mathbf u_1}$이라 ${\mathbf A\mathbf v_1=\sigma_1\mathbf u_1}$이 맞아요. $\mathbf u_1$, $\mathbf v_1$의 길이 제곱은 ${\frac12(1+1)=1}$, ${\frac12(1+1+0)=1}$이에요.

#### (b) 검산

$\mathbf A_1$의 원소 제곱합은 ${\frac{25}{4}\times4=25=\sigma_1^2}$이에요. 첫 층 하나가 담는 제곱합이 $\sigma_1^2$이라는 것과 맞아요.

#### (c) 검산

남은 차이는 둘째 층과 같아야 해요. P7의 ${\mathbf u_2=\frac{1}{\sqrt2}(1,-1)^\top}$, ${\mathbf v_2=\frac{1}{3\sqrt2}(1,-1,4)^\top}$로 ${3\mathbf u_2\mathbf v_2^\top=\frac12\begin{bmatrix}1&-1&4\\-1&1&-4\end{bmatrix}}$이고, 위의 ${\mathbf A-\mathbf A_1}$과 같아요. 또 ${\lVert\mathbf A\rVert_F^2=9+4+4+4+9+4=34}$이고, ${25+9=34}$라 남긴 양과 버린 양의 합이 전체와 같아요.

#### 이 문항에서 조심할 점

**$\sigma_1$을 빼먹지 않아요.** ${\mathbf u_1\mathbf v_1^\top=\frac12\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}}$만 쓰면 오차 제곱합이 ${(2.5^2+1.5^2+2^2)\times2=25}$가 되어 ${\sigma_2^2=9}$보다 훨씬 커요.

**제곱합과 노름을 구분해요.** 문제가 묻는 것은 원소 **제곱합** ${\lVert\mathbf A-\mathbf A_1\rVert_F^2=9}$이고, 이것은 $\sigma_2^2$와 비교해요. 제곱근을 취한 ${\lVert\mathbf A-\mathbf A_1\rVert_F=3}$은 $\sigma_2$와 같아요. 9를 $\sigma_2=3$과 비교하면 틀린 판정이 나와요.

랭크 1 근사는 원소를 반올림하거나 큰 원소만 남기는 것이 아니에요. 가장 큰 특잇값의 층 ${\sigma_1\mathbf u_1\mathbf v_1^\top}$ 하나예요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. ${\mathbf A\mathbf A^\top}$의 가장 큰 고윳값으로 $\sigma_1$, $\mathbf u_1$을 구하고 ${\mathbf v_1=\mathbf A^\top\mathbf u_1/\sigma_1}$을 계산해요.
2. 외적 ${\mathbf u_1\mathbf v_1^\top}$를 칸마다 적고 $\sigma_1$을 곱해 $\mathbf A_1$을 만들어요.
3. ${\mathbf A-\mathbf A_1}$의 원소 제곱합을 구해 ${\sigma_2^2}$와 비교해요.

**페이지 요약**

#### 떠올릴 개념·공식

랭크 1 근사는 첫 층 ${\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top}$이에요. 버린 양은 버린 특잇값의 제곱합이에요.

$$
\lVert\mathbf A-\mathbf A_M\rVert_F^2=\sum_{i\gt M}\sigma_i^2
$$

#### 첫 줄

${\mathbf A\mathbf A^\top=\begin{bmatrix}17&8\\8&17\end{bmatrix}}$, ${(17-\lambda)^2-64=0}$을 적어요.

#### 핵심 답

(a) ${\sigma_1=5}$, ${\mathbf u_1=\frac{1}{\sqrt2}(1,1)^\top}$, ${\mathbf v_1=\frac{1}{\sqrt2}(1,1,0)^\top}$이에요.

(b) ${\mathbf A_1=\frac52\begin{bmatrix}1&1&0\\1&1&0\end{bmatrix}}$이에요.

(c) ${\lVert\mathbf A-\mathbf A_1\rVert_F^2=9=\sigma_2^2}$로 같아요.

#### 검산

${\mathbf A-\mathbf A_1=3\mathbf u_2\mathbf v_2^\top}$이에요. ${\lVert\mathbf A\rVert_F^2=34=25+9}$예요.

#### 조건·구분

층에 $\sigma_1$을 곱해요. 제곱합은 $\sigma_2^2$, 노름은 $\sigma_2$와 비교해요.

#### 용어

- **랭크 1 근사(rank-1 approximation)** — 가장 큰 특잇값의 층 ${\mathbf A_1=\sigma_1\mathbf u_1\mathbf v_1^\top}$이에요. 모든 행(열)이 한 벡터의 배수라 랭크가 1이에요.
- **외적(outer product)** — 열벡터 $\mathbf u$와 행벡터 $\mathbf v^\top$의 곱 ${\mathbf u\mathbf v^\top}$이에요. $(i,j)$ 칸은 $u_iv_j$예요.
- **Frobenius 노름(Frobenius norm)** — 원소 제곱합의 제곱근이에요. 제곱 ${\lVert\mathbf M\rVert_F^2}$는 원소 제곱합이에요.
- **에카르트–영 정리(Eckart–Young theorem)** — 큰 특잇값부터 $M$개 층을 남긴 근사가 랭크 $M$ 이하 행렬 중 Frobenius 오차가 가장 작다는 정리예요.

#### 출제 근거

MML Exercise 4.10, 교과서 138쪽(PDF 144쪽). 원문은 ‘랭크 1 근사를 구하라’는 한 문장이고, 이 문항은 (a), (b)와 Frobenius 오차 판정 (c)로 나눴어요.

수업: 1104 L06 s14(랭크 제한 복원, Frobenius 오차, 에카르트–영 정리).

관련 정리노트: [작은 행렬 두 개로 데이터 복원하기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-low-rank)

---

<a id="p10"></a>

### P10. 행렬이 벡터의 길이를 가장 크게 늘리는 비율

MML Exercise 4.12 · [원 문제 보기](%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_1104_PCA_Part2-%EB%AC%B8%EC%A0%9C.pdf#page=10)

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

0이 아닌 벡터 $\mathbf x$에 행렬 $\mathbf A$를 곱하면 길이가 몇 배가 되는지 생각해요. 어떤 방향으로 넣어도 그 배율이 가장 큰 특잇값 $\sigma_1$을 넘지 못하고, 딱 $\sigma_1$배가 되는 방향이 실제로 있다는 것을 네 단계로 증명하는 문제예요.

주어진 것은 ${\mathbf A\in\mathbb R^{m\times n}}$의 SVD ${\mathbf A=\mathbf U\mathbf\Sigma\mathbf V^\top}$, 오른쪽 특이벡터 $\mathbf v_1,\ldots,\mathbf v_n$이 $\mathbb R^n$의 정규직교기저라는 사실, ${\sigma_1\ge\cdots\ge\sigma_r\gt0}$과 ${i\gt r}$이면 ${\sigma_i=0}$이라는 약속, 그리고 모든 $i$에서 ${\mathbf A^\top\mathbf A\mathbf v_i=\sigma_i^2\mathbf v_i}$예요.

(a)는 ${\mathbf x=\sum_ic_i\mathbf v_i}$로 쓴 뒤 ${\lVert\mathbf A\mathbf x\rVert_2^2=\sum_i\sigma_i^2c_i^2}$ 증명, (b)는 ${\lVert\mathbf A\mathbf x\rVert_2^2\le\sigma_1^2\lVert\mathbf x\rVert_2^2}$ 증명, (c)는 ${\mathbf x=\mathbf v_1}$에서 등호 확인, (d)는 그래서 최댓값이 $\sigma_1$인 이유 설명이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

‘길이의 비율’과 ‘최댓값’이라는 말에서는 정리노트에서 첫 주성분을 고를 때 쓴 **상한 찾기 → 상한에 도달하기** 논리를 떠올려요. 방향 분산 ${\sum_i\lambda_ic_i^2}$를 ${\lambda_1}$로 묶고, ${\mathbf b=\mathbf p_1}$에서 등호를 얻었던 것과 같은 구조예요.

‘${\mathbf x=\sum_ic_i\mathbf v_i}$’라는 단서에서는 **정규직교기저 전개**를 떠올려요. $\mathbf v_i$가 $\mathbb R^n$의 정규직교기저라 어떤 $\mathbf x$든 이렇게 쓸 수 있고, 좌표는 ${c_i=\mathbf v_i^\top\mathbf x}$예요. ${\mathbf v_i^\top\mathbf v_j}$는 $i=j$면 1, 아니면 0이에요.

‘${\lVert\mathbf A\mathbf x\rVert_2^2}$’에서는 길이 제곱을 내적으로 쓰는 식을 떠올려요. 전치하면 곱의 순서가 뒤집혀 ${(\mathbf A\mathbf x)^\top=\mathbf x^\top\mathbf A^\top}$이에요.

$$
\lVert\mathbf A\mathbf x\rVert_2^2=(\mathbf A\mathbf x)^\top(\mathbf A\mathbf x)=\mathbf x^\top\mathbf A^\top\mathbf A\mathbf x
$$

그 다음은 조건 ${\mathbf A^\top\mathbf A\mathbf v_i=\sigma_i^2\mathbf v_i}$로 행렬 곱을 숫자 곱으로 바꿔요. [첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions)와 [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)에서 같은 구조를 다뤘어요.

#### 종이에 쓸 첫 줄

길이 제곱을 내적으로 바꾸고, 가운데 ${\mathbf A^\top\mathbf A\mathbf x}$에 전개를 넣을 준비를 해요.

$$
\lVert\mathbf A\mathbf x\rVert_2^2=\mathbf x^\top(\mathbf A^\top\mathbf A\mathbf x),\qquad\mathbf x=\sum_{j=1}^nc_j\mathbf v_j
$$

#### 왜 이렇게 푸는지 함께 따라가요

#### (a) $\lVert\mathbf A\mathbf x\rVert_2^2=\sum_i\sigma_i^2c_i^2$

먼저 오른쪽 괄호를 계산해요. 행렬 곱은 합에 나눠 곱할 수 있고 숫자 $c_j$는 앞으로 꺼낼 수 있어요. 그 다음 조건 ${\mathbf A^\top\mathbf A\mathbf v_j=\sigma_j^2\mathbf v_j}$를 넣어요.

$$
\mathbf A^\top\mathbf A\mathbf x=\sum_{j=1}^nc_j\mathbf A^\top\mathbf A\mathbf v_j=\sum_{j=1}^nc_j\sigma_j^2\mathbf v_j
$$

이제 왼쪽의 ${\mathbf x^\top=\sum_ic_i\mathbf v_i^\top}$와 내적해요. 두 합을 곱하면 모든 $(i,j)$ 쌍의 항이 생겨요.

$$
\lVert\mathbf A\mathbf x\rVert_2^2=\Big(\sum_{i=1}^nc_i\mathbf v_i^\top\Big)\Big(\sum_{j=1}^nc_j\sigma_j^2\mathbf v_j\Big)=\sum_{i=1}^n\sum_{j=1}^nc_ic_j\sigma_j^2\,\mathbf v_i^\top\mathbf v_j
$$

정규직교성으로 ${\mathbf v_i^\top\mathbf v_j}$는 $i=j$일 때만 1이라, 같은 인덱스 항만 남아요. $n=2$라면 네 항 중 두 항이에요.

$$
\lVert\mathbf A\mathbf x\rVert_2^2=\sum_{i=1}^n\sigma_i^2c_i^2
$$

같은 방식으로 ${\lVert\mathbf x\rVert_2^2=\mathbf x^\top\mathbf x=\sum_ic_i^2}$예요. 이것으로 **(a)가 증명돼요.**

#### (b) $\lVert\mathbf A\mathbf x\rVert_2^2\le\sigma_1^2\lVert\mathbf x\rVert_2^2$

특잇값은 큰 순서로 정렬되어 있고 $i\gt r$인 자리는 0이라, 모든 $i$에서 ${0\le\sigma_i^2\le\sigma_1^2}$이에요. 또 ${c_i^2\ge0}$이에요.

그래서 항마다 ${\sigma_i^2c_i^2\le\sigma_1^2c_i^2}$이에요. 음수가 아닌 $c_i^2$에 더 큰 수를 곱하면 줄지 않기 때문이에요. 모든 항을 더해요.

$$
\sum_{i=1}^n\sigma_i^2c_i^2\le\sum_{i=1}^n\sigma_1^2c_i^2=\sigma_1^2\sum_{i=1}^nc_i^2
$$

(a)의 두 결과를 양쪽에 넣으면 **${\lVert\mathbf A\mathbf x\rVert_2^2\le\sigma_1^2\lVert\mathbf x\rVert_2^2}$**예요.

${\mathbf x\ne\mathbf 0}$이면 ${\lVert\mathbf x\rVert_2^2\gt0}$이라 양변을 나눌 수 있어요. 양변이 음수가 아니라 제곱근을 씌워도 부등호 방향이 그대로예요.

$$
\frac{\lVert\mathbf A\mathbf x\rVert_2}{\lVert\mathbf x\rVert_2}\le\sigma_1
$$

#### (c) $\mathbf x=\mathbf v_1$에서 등호

${\mathbf x=\mathbf v_1}$이면 기저 전개의 좌표가 ${c_1=\mathbf v_1^\top\mathbf v_1=1}$이고, 나머지는 ${c_i=\mathbf v_i^\top\mathbf v_1=0}$이에요. (a)에 넣어요.

$$
\lVert\mathbf A\mathbf v_1\rVert_2^2=\sigma_1^2\cdot1^2+0=\sigma_1^2,\qquad\lVert\mathbf v_1\rVert_2^2=1
$$

두 값이 ${\sigma_1^2\cdot1}$로 같으니 (b)의 부등식이 **등호로 성립해요.** 길이 비율은 정확히 ${\sigma_1/1=\sigma_1}$이에요.

#### (d) 최댓값이 $\sigma_1$인 이유

(b)에 따라 0이 아닌 모든 $\mathbf x$의 길이 비율은 $\sigma_1$ 이하예요. 즉 $\sigma_1$은 넘을 수 없는 상한이에요.

(c)에 따라 ${\mathbf x=\mathbf v_1}$에서 비율이 실제로 $\sigma_1$이에요. 상한에 실제로 도달하는 입력이 있으니, 그 값이 모든 비율 중 가장 큰 값이에요.

$$
\max_{\mathbf x\ne\mathbf 0}\frac{\lVert\mathbf A\mathbf x\rVert_2}{\lVert\mathbf x\rVert_2}=\sigma_1
$$

공분산에서 단위축의 방향 분산을 ${\sum_i\lambda_ic_i^2\le\lambda_1}$로 묶고 첫 고유벡터에서 등호를 얻은 것과 같은 논리예요. 따라서 **길이 비율의 최댓값은 $\sigma_1$이에요.**

#### 완성 답과 검산

#### (a) 검산

P9의 행렬로 확인해요. ${\mathbf A=\begin{bmatrix}3&2&2\\2&3&-2\end{bmatrix}}$, ${\sigma=(5,3,0)}$, ${\mathbf x=\mathbf v_1+\mathbf v_2}$(곧 ${c=(1,1,0)}$)이면 (a)의 식은 ${25+9=34}$예요. 직접 계산하면 ${\mathbf A\mathbf v_1+\mathbf A\mathbf v_2=5\mathbf u_1+3\mathbf u_2=\frac{1}{\sqrt2}(8,2)^\top}$이라 길이 제곱이 ${\frac{64+4}{2}=34}$로 같아요. 이것은 일반 증명을 대신하지 않는 확인용 예예요.

#### (b) 검산

위 예에서 ${\lVert\mathbf x\rVert_2^2=1+1=2}$라 ${\sigma_1^2\lVert\mathbf x\rVert_2^2=50}$이고, ${34\le50}$이에요. 등호가 아닌 이유는 $c_2\ne0$인 항에서 ${\sigma_2^2=9\lt25}$이기 때문이에요.

#### (c) 검산

SVD의 열 관계 ${\mathbf A\mathbf v_1=\sigma_1\mathbf u_1}$로도 확인돼요. $\mathbf u_1$이 단위벡터라 ${\lVert\mathbf A\mathbf v_1\rVert_2=\sigma_1}$이에요. P9에서 ${\mathbf A\mathbf v_1=(5,5)^\top/\sqrt2}$의 길이가 5인 것과 맞아요.

#### (d) 검산

논리의 두 조각이 모두 있는지 점검해요. ‘모든 $\mathbf x$에서 이하’(b)와 ‘어떤 $\mathbf x$에서 같음’(c)이 모두 있어야 최댓값이에요. 특수한 경우로 ${\mathbf A=\mathbf 0}$이면 모든 특잇값이 0이고 모든 비율이 0이라 식이 그대로 성립해요.

#### 이 문항에서 조심할 점

**상한만 보이고 끝내지 않아요.** (b)만으로는 ‘$\sigma_1$ 이하’까지만 알 수 있어요. 실제로 $\sigma_1$이 되는 입력 ${\mathbf v_1}$을 보여야 최댓값이에요.

**제곱을 빼먹지 않아요.** ${\lVert\mathbf A\mathbf x\rVert_2=\sum_i\sigma_i\lvert c_i\rvert}$로 쓰면 틀려요. 위 예(${c=(1,1,0)}$)에서 이 식은 ${5+3=8}$이지만 실제 길이는 ${\sqrt{34}\approx5.83}$이에요. 직교 성분의 길이는 제곱해서 더해요.

**교차항이 사라지는 이유를 밝혀요.** ${i\ne j}$ 항이 없어지는 것은 ${\mathbf v_i^\top\mathbf v_j=0}$(정규직교성) 때문이에요. 이 조건 없이 아무 기저로 전개하면 교차항이 남아요.

나누기 전에 ${\mathbf x\ne\mathbf 0}$을 확인해요. ${\mathbf x=\mathbf 0}$이면 분모가 0이라 비율이 정의되지 않아요.

#### 설명을 닫고 다시 해 봐요

설명을 보지 않고 아래 순서대로 종이에 다시 풀어 봐요.

1. ${\lVert\mathbf A\mathbf x\rVert_2^2=\mathbf x^\top\mathbf A^\top\mathbf A\mathbf x}$에 ${\mathbf x=\sum c_j\mathbf v_j}$와 ${\mathbf A^\top\mathbf A\mathbf v_j=\sigma_j^2\mathbf v_j}$를 넣고 정규직교성으로 ${\sum\sigma_i^2c_i^2}$를 얻어요.
2. ${\sigma_i^2\le\sigma_1^2}$, ${c_i^2\ge0}$으로 상한을 만들고 ${\mathbf x\ne\mathbf 0}$으로 나눠요.
3. ${\mathbf x=\mathbf v_1}$에서 등호를 확인하고 ‘상한 + 도달 = 최댓값’으로 마무리해요.

**페이지 요약**

#### 떠올릴 개념·공식

정규직교기저 전개 ${\mathbf x=\sum c_i\mathbf v_i}$와 ${\mathbf A^\top\mathbf A\mathbf v_i=\sigma_i^2\mathbf v_i}$로 길이 제곱을 성분별로 써요.

$$
\lVert\mathbf A\mathbf x\rVert_2^2=\sum_i\sigma_i^2c_i^2
$$

상한을 찾고, 상한에 도달하는 입력을 찾아요.

#### 첫 줄

${\lVert\mathbf A\mathbf x\rVert_2^2=\mathbf x^\top(\mathbf A^\top\mathbf A\mathbf x)}$로 바꿔요.

#### 핵심 답

(a) 교차항이 정규직교성으로 사라져 ${\sum_i\sigma_i^2c_i^2}$예요.

(b) ${\sigma_i^2\le\sigma_1^2}$라 ${\lVert\mathbf A\mathbf x\rVert_2^2\le\sigma_1^2\lVert\mathbf x\rVert_2^2}$예요.

(c) ${\mathbf x=\mathbf v_1}$이면 ${\lVert\mathbf A\mathbf v_1\rVert_2=\sigma_1}$, ${\lVert\mathbf v_1\rVert_2=1}$이라 등호예요.

(d) 상한 $\sigma_1$에 실제로 도달하므로 최댓값은 $\sigma_1$이에요.

#### 검산

P9 행렬에서 ${c=(1,1,0)}$이면 ${34=25+9\le50}$이에요. ${\mathbf A\mathbf v_1=\sigma_1\mathbf u_1}$이에요.

#### 조건·구분

상한과 최댓값을 구분해요. 길이는 제곱해서 더해요. ${\mathbf x\ne\mathbf 0}$이어야 나눌 수 있어요.

#### 용어

- **유클리드 노름(Euclidean norm)** — ${\lVert\mathbf x\rVert_2=\sqrt{\mathbf x^\top\mathbf x}}$, 성분 제곱합의 제곱근인 길이예요.
- **정규직교기저(orthonormal basis)** — 서로 수직이고 길이가 1인 벡터로 이루어진 기저예요. 좌표는 ${c_i=\mathbf v_i^\top\mathbf x}$이고 ${\lVert\mathbf x\rVert_2^2=\sum_ic_i^2}$예요.
- **최대 특잇값(largest singular value)** — $\sigma_1$이에요. 0이 아닌 입력에서 ${\lVert\mathbf A\mathbf x\rVert_2/\lVert\mathbf x\rVert_2}$의 최댓값이에요.
- **상한(upper bound)** — 모든 후보 값이 넘지 못하는 값이에요. 실제로 도달하는 후보가 있으면 최댓값이에요.

#### 출제 근거

MML Exercise 4.12(정리 4.24), 교과서 138쪽(PDF 144쪽). 원문은 ‘정리 4.24가 성립함을 보여라’이고, 이 문항은 기저 전개 방식의 (a)–(d) 네 단계로 나눴어요.

수업: 1104 L05 s27–28(상한 찾기와 도달), L06 s13(SVD).

관련 정리노트: [첫 번째부터 M번째까지 방향 고르기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s0-top-directions), [데이터의 SVD에서 주성분 찾기](../%EC%A0%95%EB%A6%AC%EB%85%B8%ED%8A%B8_1104_PCA_Part2.html#s2-svd)

---

원 문제·정리노트·PDF는 보존해요.
