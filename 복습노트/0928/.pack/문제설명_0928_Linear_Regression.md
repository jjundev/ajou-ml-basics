# 머신러닝기초 복습 0928 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [P1. 2차 다항식의 특징행렬 쓰기](#p1)
  - [P2. 3차 다항식 최대우도 적합 준비하기](#p2)
  - [P3. 사전분포를 바꾼 다항회귀 MAP](#p3)
  - [P4. 곱의 미분과 치환 미분](#p4)
  - [P5. 가우시안 모양 함수 미분하기](#p5)
  - [P6. 연쇄법칙과 편미분의 차원](#p6)
  - [P7. tanh 층의 자코비안 차원](#p7)
  - [P8. 로지스틱 시그모이드 미분하기](#p8)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### P1. 2차 다항식의 특징행렬 쓰기

MML Example 9.4 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0928_Linear_Regression.html#p1)

#### 주어진 조건

입력이 스칼라인 훈련 데이터 $N = 3$개가 있어요: $x_1 = -1$, $x_2 = 1$, $x_3 = 2$.

#### 구할 것

2차 다항식 특징 $\boldsymbol{\phi}(x) = [1, x, x^2]^\top$을 쓸 때, 특징행렬 $\boldsymbol{\Phi}$를 숫자로 적어 보세요.

#### 무엇을 구하는 문제인가요?

2차 다항식의 특징행렬 쓰기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

특징행렬(design matrix)의 한 행은 한 데이터의 특징 벡터 전치예요. $\Phi_{ij}=\phi_j(x_i)$로 데이터 i와 특징 j를 구별해요. 2차는 상수항까지3특징이에요.

#### 종이에 적을 첫 줄

첫 행 $[1,-1,(-1)^2]=[1,-1,1]$을 적어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

특징이 $1, x, x^2$ 세 개라서 $K = 3$이고, 행은 데이터 수만큼 $N = 3$개예요. 그래서 $\boldsymbol{\Phi} \in \mathbb{R}^{3 \times 3}$이에요.

$\Phi_{ij} = \phi_j(x_i)$이므로 $i$번째 행에 $[1, x_i, x_i^2]$를 적어요.

$x_1 = -1$이면 $[1, -1, 1]$, $x_2 = 1$이면 $[1, 1, 1]$, $x_3 = 2$이면 $[1, 2, 4]$예요.

세 행을 위에서부터 쌓아요.

$$
\boldsymbol{\Phi} = \begin{bmatrix} 1 & -1 & 1 \\ 1 & 1 & 1 \\ 1 & 2 & 4 \end{bmatrix}
$$

수업과의 연결: 0928 수업에서 "첫 행은 $\mathbf{x}_1$로, 마지막 행은 $\mathbf{x}_N$으로 만든다"고 한 특징행렬 $\Phi_{ij} = \phi_j(\mathbf{x}_i)$를 숫자로 채워 본 거예요.

#### 완성 답과 검산

#### 검산

각 행에−1,1,2를 다시 대입하면 [1,−1,1],[1,1,1],[1,2,4]예요. Φθ는3×1 예측 벡터여야 해요.

정답: $\boldsymbol{\Phi} = \begin{bmatrix} 1 & -1 & 1 \\ 1 & 1 & 1 \\ 1 & 2 & 4 \end{bmatrix}$

#### 여기서 주의해요

−1의 제곱은1이에요. 데이터 벡터를 열로 쌓으면 전치된 다른 행렬이 돼요.

#### 설명을 닫고 다시 해요

1. 첫 행 $[1,-1,(-1)^2]=[1,-1,1]$을 적어요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. −1의 제곱은1이에요. 데이터 벡터를 열로 쌓으면 전치된 다른 행렬이 돼요.

**페이지 요약**

#### 떠올릴 개념·공식

특징행렬(design matrix)의 한 행은 한 데이터의 특징 벡터 전치예요. $\Phi_{ij}=\phi_j(x_i)$

#### 첫 줄

첫 행 $[1,-1,(-1)^2]=[1,-1,1]$을 적어요.

#### 검산

각 행에−1,1,2를 다시 대입하면 [1,−1,1],[1,1,1],[1,2,4]예요. Φθ는3×1 예측 벡터여야 해요.

---

<a id="p2"></a>

### P2. 3차 다항식 최대우도 적합 준비하기

MML Example 9.5 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0928_Linear_Regression.html#p2)

#### 주어진 조건

데이터셋이 $N = 8$개의 쌍 $(x_n, y_n)$으로 이뤄져 있어요. $x_n \sim \mathcal{U}[-5, 5]$이고 $y_n = -\sin(x_n/5) + \cos(x_n) + \epsilon$, $\epsilon \sim \mathcal{N}(0, 0.2^2)$이에요.

#### 구할 것

이 데이터에 3차 다항식을 최대우도 추정으로 맞추려고 해요.

- (a) 특징 벡터 $\boldsymbol{\phi}(x)$의 길이 $K$는 얼마인가요?
- (b) 특징행렬 $\boldsymbol{\Phi}$의 크기는 얼마인가요?
- (c) 최대우도 해 $\boldsymbol{\theta}_{\text{ML}}$을 $\boldsymbol{\Phi}$와 $\mathbf{y}$로 적어 보세요.

#### 무엇을 구하는 문제인가요?

3차 다항식 최대우도 적합 준비하기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

3차 다항식은 θ0부터θ3까지4계수예요. Φ는 N×K이고, full column rank일 때 최대우도 해는 $(\Phi^\top\Phi)^{-1}\Phi^\top y$예요. 잡음 분산은 고정 양수라 최소제곱과 같아요.

#### 종이에 적을 첫 줄

$\phi(x)=[1,x,x^2,x^3]^\top$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

3차 다항식의 특징은 $\boldsymbol{\phi}(x) = [1, x, x^2, x^3]^\top$이에요. 항이 네 개라서 $K = 4$예요.

#### (b)

행은 데이터 수 $N = 8$개, 열은 특징 수 $K = 4$개예요. 그래서 $\boldsymbol{\Phi} \in \mathbb{R}^{8 \times 4}$이고, $n$번째 행은 $[1, x_n, x_n^2, x_n^3]$이에요.

#### (c)

음의 로그우도는 $\frac{1}{2\sigma^2}\|\mathbf{y} - \boldsymbol{\Phi}\boldsymbol{\theta}\|^2 + \text{const}$예요. 이걸 $\boldsymbol{\theta}$로 미분해 0으로 두면

$$
\boldsymbol{\theta}_{\text{ML}} = (\boldsymbol{\Phi}^\top \boldsymbol{\Phi})^{-1} \boldsymbol{\Phi}^\top \mathbf{y}
$$

이때 $\boldsymbol{\Phi}^\top \boldsymbol{\Phi}$는 $4 \times 4$라서 역행렬 계산이 작아요.

수업과의 연결: 0928 수업에서 "3차면 $K = 4$"라고 한 말과, $\mathbf{X}$ 자리에 $\boldsymbol{\Phi}$를 넣은 유사역행렬 해를 그대로 쓴 거예요.

#### 완성 답과 검산

#### (a) 검산

최고차수가3이어도 상수항 포함 K=4예요.

#### (b) 검산

8개 입력에 각각4특징을 만들므로8×4예요.

#### (c) 검산

미분식 $\Phi^\top\Phi\theta=\Phi^\top y$에 해를 대입하면 만족해요. 적어도4개의 서로 다른 입력이면 Vandermonde 열이 독립이에요.

정답: (a) $K = 4$ (b) $\boldsymbol{\Phi} \in \mathbb{R}^{8 \times 4}$ (c) $\boldsymbol{\theta}_{\text{ML}} = (\boldsymbol{\Phi}^\top \boldsymbol{\Phi})^{-1} \boldsymbol{\Phi}^\top \mathbf{y}$

#### 여기서 주의해요

역행렬 공식은 열들이 독립일 때 써요. 중복 입력 등으로 rank가 부족하면 일반화 역행렬을 쓰고 해가 유일하지 않을 수 있어요.

#### 설명을 닫고 다시 해요

1. $\phi(x)=[1,x,x^2,x^3]^\top$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 역행렬 공식은 열들이 독립일 때 써요. 중복 입력 등으로 rank가 부족하면 일반화 역행렬을 쓰고 해가 유일하지 않을 수 있어요.

**페이지 요약**

#### 떠올릴 개념·공식

3차 다항식은 θ0부터θ3까지4계수예요. $(\Phi^\top\Phi)^{-1}\Phi^\top y$

#### 첫 줄

$\phi(x)=[1,x,x^2,x^3]^\top$예요.

#### 검산

최고차수가3이어도 상수항 포함 K=4예요. 8개 입력에 각각4특징을 만들므로8×4예요. 미분식 $\Phi^\top\Phi\theta=\Phi^\top y$에 해를 대입하면 만족해요. 적어도4개의 서로 다른 입력이면 Vandermonde 열이 독립이에요.

---

<a id="p3"></a>

### P3. 사전분포를 바꾼 다항회귀 MAP

MML Example 9.6 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0928_Linear_Regression.html#p3)

#### 주어진 조건

잡음이 $\epsilon \sim \mathcal{N}(0, 0.2^2)$인 다항회귀 데이터에서 파라미터에 가우시안 사전분포 $p(\boldsymbol{\theta}) = \mathcal{N}(\mathbf{0}, \frac{1}{4}\mathbf{I})$를 두고 MAP 추정을 해요. MAP 해는 아래와 같아요.

$$
\boldsymbol{\theta}_{\text{MAP}} = \left(\boldsymbol{\Phi}^\top \boldsymbol{\Phi} + \frac{\sigma^2}{b^2} \mathbf{I}\right)^{-1} \boldsymbol{\Phi}^\top \mathbf{y}
$$

#### 구할 것

- (a) 이 식에 들어가는 $\frac{\sigma^2}{b^2}$ 값을 구해 보세요.
- (b) 6차 다항식과 8차 다항식 중 어느 쪽에서 사전분포(정규화)의 효과가 크게 드러날까요? 이유도 말해 보세요.

#### 무엇을 구하는 문제인가요?

사전분포를 바꾼 다항회귀 MAP를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

MAP의 정규화 계수는 잡음 분산과 prior 분산의 비율이에요. $\lambda=\sigma^2/b^2$에서0.2는 표준편차,1/4은 prior 공분산의 계수예요. 고차에서의 효과는 데이터와 특징 스케일에도 달려요.

#### 종이에 적을 첫 줄

$\sigma^2=(0.2)^2=1/25$, $b^2=1/4$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

잡음 표준편차가 $0.2$라서 $\sigma^2 = 0.04 = \frac{1}{25}$이에요.

사전분포 $\mathcal{N}(\mathbf{0}, \frac{1}{4}\mathbf{I})$를 $\mathcal{N}(\mathbf{0}, b^2 \mathbf{I})$와 맞춰 보면 $b^2 = \frac{1}{4}$이에요.

나누면 $\frac{\sigma^2}{b^2} = \frac{1/25}{1/4} = \frac{4}{25} = 0.16$이에요.

수업과의 연결: 0928 수업에서 ML과 MAP는 $\frac{\sigma^2}{b^2}\mathbf{I}$ 한 항만 다르고 이 항이 정규화(regularizer) 역할을 한다고 했어요. $b^2$를 $\frac{1}{4}$로 작게 잡을수록 이 항이 커져 선호를 더 강하게 반영해요.

#### (b)

교과서 비교 그림에서는8차의 큰 ML 계수가 prior에 의해 줄어드는 효과를 기대해요. 하지만 입력·출력 실현값이 없으므로 이 문제의 모든 데이터에 대한 엄밀한 순위는 정할 수 없어요. 예를 들어 y=0이면 두 차수 모두 MAP=0으로 같아요.

#### 완성 답과 검산

#### (a) 검산

(1/25)/(1/4)=4/25=0.16이에요. 표준편차0.2를 그대로 나누면 잘못돼요.

#### (b) 검산

교과서 비교 그림에서는8차의 큰 ML 계수가 prior에 의해 줄어드는 효과를 기대해요. 하지만 입력·출력 실현값이 없으므로 이 문제의 모든 데이터에 대한 엄밀한 순위는 정할 수 없어요. 예를 들어 y=0이면 두 차수 모두 MAP=0으로 같아요.

정답: (a) $\frac{\sigma^2}{b^2} = \frac{4}{25} = 0.16$ (b) 8차 다항식. 차수가 높을수록 최대우도 계수가 커지므로 사전분포(정규화) 효과가 더 크게 드러나요.

원 참고 답의8차 선택은 해당 예제의 경향으로 읽어요. 모든 데이터에서 계수가 반드시 더 크다는 주장은 성립하지 않아요.

#### 여기서 주의해요

8차의 효과가 항상 더 크다는 정리는 없어요. 해당 교과서 예제의 경향과 보편적 명제를 구별해요.

#### 설명을 닫고 다시 해요

1. $\sigma^2=(0.2)^2=1/25$, $b^2=1/4$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 8차의 효과가 항상 더 크다는 정리는 없어요. 해당 교과서 예제의 경향과 보편적 명제를 구별해요.

**페이지 요약**

#### 떠올릴 개념·공식

MAP의 정규화 계수는 잡음 분산과 prior 분산의 비율이에요. $\lambda=\sigma^2/b^2$에서0.2는 표준편차,1/4은 prior 공분산의 계수예요.

#### 첫 줄

$\sigma^2=(0.2)^2=1/25$, $b^2=1/4$예요.

#### 검산

(1/25)/(1/4)=4/25=0.16이에요. 표준편차0.2를 그대로 나누면 잘못돼요. 교과서 비교 그림에서는8차의 큰 ML 계수가 prior에 의해 줄어드는 효과를 기대해요. 하지만 입력·출력 실현값이 없으므로 이 문제의 모든 데이터에 대한 엄밀한 순위는 정할 수 없어요. 예를 들어 y=0이면 두 차수 모두 MAP=0으로 같아요.

---

<a id="p4"></a>

### P4. 곱의 미분과 치환 미분

MML Exercise 5.1 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0928_Linear_Regression.html#p4)

#### 주어진 조건

#### 구할 것

아래 함수의 도함수 $f'(x)$를 구해 보세요. $\log$는 자연로그예요.

$$
f(x) = \log(x^4) \sin(x^3)
$$

#### 무엇을 구하는 문제인가요?

곱의 미분과 치환 미분를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

곱의 미분(product rule)은 $(uv)\prime=u\prime v+uv\prime$예요. 합성함수에는 연쇄법칙(chain rule)으로 안쪽 미분까지 곱해요. log(x⁴)는 실수 x≠0에서 정의돼요.

#### 종이에 적을 첫 줄

$u=\log(x^4)$, $v=\sin(x^3)$로 나눠요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

곱의 미분: $f'(x) = [\log(x^4)]' \sin(x^3) + \log(x^4) [\sin(x^3)]'$이에요.

$u = x^4$로 두면 $[\log u]' = \frac{1}{u} \cdot 4x^3 = \frac{4x^3}{x^4} = \frac{4}{x}$예요.

$v = x^3$으로 두면 $[\sin v]' = \cos v \cdot 3x^2 = 3x^2 \cos(x^3)$이에요.

합치면

$$
f'(x) = \frac{4}{x} \sin(x^3) + 3x^2 \log(x^4) \cos(x^3)
$$

수업과의 연결: 0928 수업에서 $(x + 2y^3)^2$을 $y$로 미분할 때 쓴 치환 미분이 여기서도 두 번 쓰였어요. 교수님 말대로 $\log$는 자연로그(ln)예요.

#### 완성 답과 검산

#### 검산

독립 symbolic 미분 결과를 빼면0이에요. x≠0에서 u′=4/x, v′=3x²cos(x³)를 각각 곱해 더한 식이에요.

정답: $f'(x) = \frac{4}{x} \sin(x^3) + 3x^2 \log(x^4) \cos(x^3)$

#### 여기서 주의해요

log(x⁴)=4log(x)는 x&gt;0일 때만 맞아요. 전체 정의역에는4log|x|가 맞아요.

#### 설명을 닫고 다시 해요

1. $u=\log(x^4)$, $v=\sin(x^3)$로 나눠요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. log(x⁴)=4log(x)는 x&gt;0일 때만 맞아요. 전체 정의역에는4log|x|가 맞아요.

**페이지 요약**

#### 떠올릴 개념·공식

곱의 미분(product rule)은 $(uv)\prime=u\prime v+uv\prime$예요.

#### 첫 줄

$u=\log(x^4)$, $v=\sin(x^3)$로 나눠요.

#### 검산

독립 symbolic 미분 결과를 빼면0이에요. x≠0에서 u′=4/x, v′=3x²cos(x³)를 각각 곱해 더한 식이에요.

---

<a id="p5"></a>

### P5. 가우시안 모양 함수 미분하기

MML Exercise 5.3 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0928_Linear_Regression.html#p5)

#### 주어진 조건

$\mu, \sigma \in \mathbb{R}$은 상수예요.

#### 구할 것

아래 함수의 도함수 $f'(x)$를 구해 보세요.

$$
f(x) = \exp\left(-\frac{1}{2\sigma^2}(x - \mu)^2\right)
$$

#### 무엇을 구하는 문제인가요?

가우시안 모양 함수 미분하기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

지수 합성함수의 도함수는 바깥 exp를 남기고 지수의 도함수를 곱해요. μ,σ는 미분 대상이 아닌 상수이며 분모가 있으므로 σ≠0이 필요해요.

#### 종이에 적을 첫 줄

$u=-(x-\mu)^2/(2\sigma^2)$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

$u = -\frac{1}{2\sigma^2}(x - \mu)^2$로 두면 $f = \exp(u)$예요.

$\frac{du}{dx} = -\frac{1}{2\sigma^2} \cdot 2(x - \mu) = -\frac{x - \mu}{\sigma^2}$예요.

연쇄법칙으로 곱하면

$$
f'(x) = -\frac{x - \mu}{\sigma^2} \exp\left(-\frac{1}{2\sigma^2}(x - \mu)^2\right)
$$

$x = \mu$에서 도함수가 0이라 여기가 봉우리예요.

수업과의 연결: 0928 수업에서 가우시안 PDF의 지수 부분 $-\frac{(y - \mathbf{x}^\top\boldsymbol{\theta})^2}{2\sigma^2}$을 다뤘어요. 같은 꼴을 치환 미분으로 직접 미분해 본 거예요.

#### 완성 답과 검산

#### 검산

독립 미분과 일치하며 x=μ에서는0이에요. σ²&gt;0이면 μ 왼쪽에서 증가, 오른쪽에서 감소하므로 봉우리가 맞아요.

정답: $f'(x) = -\frac{x - \mu}{\sigma^2} \exp\left(-\frac{1}{2\sigma^2}(x - \mu)^2\right)$

#### 여기서 주의해요

원 조건에 σ∈R만 적혀 있지만 σ=0에서는 함수가 정의되지 않아요. 분산 해석에서는 σ&gt;0으로 두어요.

#### 설명을 닫고 다시 해요

1. $u=-(x-\mu)^2/(2\sigma^2)$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 원 조건에 σ∈R만 적혀 있지만 σ=0에서는 함수가 정의되지 않아요. 분산 해석에서는 σ&gt;0으로 두어요.

**페이지 요약**

#### 떠올릴 개념·공식

지수 합성함수의 도함수는 바깥 exp를 남기고 지수의 도함수를 곱해요.

#### 첫 줄

$u=-(x-\mu)^2/(2\sigma^2)$예요.

#### 검산

독립 미분과 일치하며 x=μ에서는0이에요. σ²&gt;0이면 μ 왼쪽에서 증가, 오른쪽에서 감소하므로 봉우리가 맞아요.

---

<a id="p6"></a>

### P6. 연쇄법칙과 편미분의 차원

MML Exercise 5.7 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0928_Linear_Regression.html#p6)

#### 주어진 조건

#### 구할 것

연쇄법칙으로 $\frac{df}{d\mathbf{x}}$를 구해 보세요. 각 편미분의 차원도 함께 적어요.

- (a) $f(z) = \log(1 + z)$, $z = \mathbf{x}^\top \mathbf{x}$, $\mathbf{x} \in \mathbb{R}^D$
- (b) $\mathbf{f}(\mathbf{z}) = \sin(\mathbf{z})$, $\mathbf{z} = \mathbf{A}\mathbf{x} + \mathbf{b}$, $\mathbf{A} \in \mathbb{R}^{E \times D}$, $\mathbf{x} \in \mathbb{R}^D$, $\mathbf{b} \in \mathbb{R}^E$. 여기서 $\sin$은 $\mathbf{z}$의 성분마다 따로 적용해요.

#### 무엇을 구하는 문제인가요?

연쇄법칙과 편미분의 차원를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

Jacobian은 출력차원×입력차원이에요. 행 미분 convention에서 $df/dx=(df/dz)(dz/dx)$를 써요. 성분별 sin의 Jacobian은 대각 cos이고 xᵀx는 성분제곱 합이에요.

#### 종이에 적을 첫 줄

(a) $df/dz=1/(1+z)$, (b) $J_{fz}=\operatorname{diag}(\cos z)$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$\frac{df}{dz} = \frac{1}{1 + z}$이고, 스칼라라서 차원은 $1 \times 1$이에요.

$z = \mathbf{x}^\top \mathbf{x} = x_1^2 + \dots + x_D^2$이므로 $\frac{dz}{d\mathbf{x}} = 2\mathbf{x}^\top \in \mathbb{R}^{1 \times D}$예요.

곱하면 $\frac{df}{d\mathbf{x}} = \frac{2\mathbf{x}^\top}{1 + \mathbf{x}^\top \mathbf{x}} \in \mathbb{R}^{1 \times D}$예요.

#### (b)

$\frac{\partial f_i}{\partial z_j}$는 $i = j$일 때 $\cos z_i$, 아니면 0이에요. 그래서 $\frac{d\mathbf{f}}{d\mathbf{z}} = \operatorname{diag}(\cos \mathbf{z}) \in \mathbb{R}^{E \times E}$예요.

$\frac{d\mathbf{z}}{d\mathbf{x}} = \mathbf{A} \in \mathbb{R}^{E \times D}$예요. $\mathbf{b}$는 $\mathbf{x}$와 상관없어서 미분하면 0이에요.

곱하면 $\frac{d\mathbf{f}}{d\mathbf{x}} = \operatorname{diag}(\cos \mathbf{z})\,\mathbf{A} \in \mathbb{R}^{E \times D}$예요. $(E \times E)(E \times D)$라 차원이 맞아요.

수업과의 연결: 0928 수업의 $\frac{\partial L}{\partial \mathbf{e}} = 2\mathbf{e}^\top$, $\frac{d(\mathbf{A}\mathbf{x})}{d\mathbf{x}} = \mathbf{A}$를 연쇄법칙으로 이어 붙이고, "디멘션만 맞추면 된다"는 말대로 차원을 확인한 거예요.

#### 완성 답과 검산

#### (a) 검산

성분 j로 직접 미분해도 $2x_j/(1+\sum x_i^2)$라 1×D예요.

#### (b) 검산

f_i=sin(∑A_ij x_j+b_i)를 x_j로 미분하면 cos(z_i)A_ij예요. diag(cos z)A의 (i,j)칸과 같고 E×D예요.

정답: (a) $\frac{df}{d\mathbf{x}} = \frac{2\mathbf{x}^\top}{1 + \mathbf{x}^\top \mathbf{x}} \in \mathbb{R}^{1 \times D}$ (b) $\frac{d\mathbf{f}}{d\mathbf{x}} = \operatorname{diag}(\cos \mathbf{z})\,\mathbf{A} \in \mathbb{R}^{E \times D}$

#### 여기서 주의해요

벡터 미분의 열 gradient와 행 Jacobian을 혼합하지 않아요. z=xᵀx≥0이라 log의 정의역도 맞아요.

#### 설명을 닫고 다시 해요

1. (a) $df/dz=1/(1+z)$, (b) $J_{fz}=\operatorname{diag}(\cos z)$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 벡터 미분의 열 gradient와 행 Jacobian을 혼합하지 않아요. z=xᵀx≥0이라 log의 정의역도 맞아요.

**페이지 요약**

#### 떠올릴 개념·공식

Jacobian은 출력차원×입력차원이에요. $df/dx=(df/dz)(dz/dx)$

#### 첫 줄

(a) $df/dz=1/(1+z)$, (b) $J_{fz}=\operatorname{diag}(\cos z)$예요.

#### 검산

성분 j로 직접 미분해도 $2x_j/(1+\sum x_i^2)$라 1×D예요. f_i=sin(∑A_ij x_j+b_i)를 x_j로 미분하면 cos(z_i)A_ij예요. diag(cos z)A의 (i,j)칸과 같고 E×D예요.

---

<a id="p7"></a>

### P7. tanh 층의 자코비안 차원

MML Exercise 5.8 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0928_Linear_Regression.html#p7)

#### 주어진 조건

#### 구할 것

아래 함수에서 연쇄법칙으로 $\frac{d\mathbf{f}}{d\mathbf{x}}$를 구해 보세요. 각 편미분의 차원도 적어요. 두 편미분의 곱을 끝까지 계산하지 않아도 돼요.

$$
\mathbf{f} = \tanh(\mathbf{z}) \in \mathbb{R}^M, \quad \mathbf{z} = \mathbf{A}\mathbf{x} + \mathbf{b}, \quad \mathbf{x} \in \mathbb{R}^N,\ \mathbf{A} \in \mathbb{R}^{M \times N},\ \mathbf{b} \in \mathbb{R}^M
$$

여기서 $\tanh$는 $\mathbf{z}$의 성분마다 따로 적용해요.

#### 무엇을 구하는 문제인가요?

tanh 층의 자코비안 차원를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

성분별 tanh 층의 Jacobian은 $\operatorname{diag}(1-\tanh^2z)$예요. 각 출력은 같은 번호의 z만 보므로 비대각은0이에요. 뒤의 affine layer Jacobian은 A예요.

#### 종이에 적을 첫 줄

$J_{fx}=J_{fz}A$로 연쇄를 적어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

$\frac{d\mathbf{f}}{d\mathbf{x}} = \frac{d\mathbf{f}}{d\mathbf{z}}\frac{d\mathbf{z}}{d\mathbf{x}}$로 나눠요.

$\frac{\partial f_i}{\partial z_j}$는 $i = j$일 때 $1 - \tanh^2 z_i$, 아니면 0이에요. 그래서 $\frac{d\mathbf{f}}{d\mathbf{z}} = \operatorname{diag}(1 - \tanh^2 \mathbf{z}) \in \mathbb{R}^{M \times M}$예요.

$\frac{d\mathbf{z}}{d\mathbf{x}} = \mathbf{A} \in \mathbb{R}^{M \times N}$예요. $\mathbf{b}$는 상수라 사라져요.

곱은 $(M \times M)(M \times N)$이므로 $\frac{d\mathbf{f}}{d\mathbf{x}} = \operatorname{diag}(1 - \tanh^2 \mathbf{z})\,\mathbf{A} \in \mathbb{R}^{M \times N}$예요.

수업과의 연결: 0928 수업에서 $\mathbb{R}^n \to \mathbb{R}^m$ 함수의 자코비안은 $m \times n$이라고 했어요. 여기서도 $\mathbb{R}^N \to \mathbb{R}^M$이라 결과가 $M \times N$이에요. 수업에서 말한 DNN 가중치 학습도 이런 층의 연쇄법칙이에요.

#### 완성 답과 검산

#### 검산

성분 미분은 $(1-\tanh^2z_i)A_{ij}$예요. (M×M)(M×N)=M×N이고 b의 미분은0이에요.

정답: $\frac{d\mathbf{f}}{d\mathbf{z}} = \operatorname{diag}(1 - \tanh^2 \mathbf{z}) \in \mathbb{R}^{M \times M}$, $\frac{d\mathbf{z}}{d\mathbf{x}} = \mathbf{A} \in \mathbb{R}^{M \times N}$, $\frac{d\mathbf{f}}{d\mathbf{x}} \in \mathbb{R}^{M \times N}$

#### 여기서 주의해요

1−tanh²z를 벡터로 둔 채 A와 행렬곱하면 차원이 안 맞아요. 대각행렬로 만들어요.

#### 설명을 닫고 다시 해요

1. $J_{fx}=J_{fz}A$로 연쇄를 적어요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 1−tanh²z를 벡터로 둔 채 A와 행렬곱하면 차원이 안 맞아요. 대각행렬로 만들어요.

**페이지 요약**

#### 떠올릴 개념·공식

성분별 tanh 층의 Jacobian은 $\operatorname{diag}(1-\tanh^2z)$예요.

#### 첫 줄

$J_{fx}=J_{fz}A$로 연쇄를 적어요.

#### 검산

성분 미분은 $(1-\tanh^2z_i)A_{ij}$예요. (M×M)(M×N)=M×N이고 b의 미분은0이에요.

---

<a id="p8"></a>

### P8. 로지스틱 시그모이드 미분하기

MML Exercise 5.2 · [원 문제 보기](../%EB%B3%B5%EC%8A%B5%EB%AC%B8%EC%A0%9C_0928_Linear_Regression.html#p8)

#### 주어진 조건

#### 구할 것

로지스틱 시그모이드 함수의 도함수 $f'(x)$를 구해 보세요. 구한 결과를 $f(x)$로도 나타내 보세요.

$$
f(x) = \frac{1}{1 + \exp(-x)}
$$

#### 무엇을 구하는 문제인가요?

로지스틱 시그모이드 미분하기를 주어진 조건에서 차례로 구해요. 원문 아래의 각 소문항이 모두 풀이 대상이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

시그모이드(sigmoid)는 $(1+e^{-x})^{-1}$ 합성함수예요. 역수 미분과 exp(−x)의 미분은 각각 음의 부호가 생겨 결과가 양수예요.

#### 종이에 적을 첫 줄

$u=1+e^{-x}$, $f=u^{-1}$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### 풀이

$u = 1 + \exp(-x)$로 두면 $f = u^{-1}$이고, $\frac{df}{du} = -u^{-2}$예요.

$\frac{du}{dx} = -\exp(-x)$예요.

곱하면 부호 두 개가 상쇄돼요.

$$
f'(x) = -\frac{1}{(1 + \exp(-x))^2} \cdot (-\exp(-x)) = \frac{\exp(-x)}{(1 + \exp(-x))^2}
$$

분자를 $\exp(-x) = (1 + \exp(-x)) - 1$로 쪼개요. 그러면 $\frac{\exp(-x)}{1 + \exp(-x)} = 1 - f(x)$예요.

그래서 $f'(x) = \frac{1}{1 + \exp(-x)} \cdot \frac{\exp(-x)}{1 + \exp(-x)} = f(x)(1 - f(x))$예요. 함숫값만 알면 도함수가 바로 나와요.

수업과의 연결: 0928 수업에서 $(x + 2y^3)^2$에 쓴 치환 미분 그대로예요. 교수님이 DNN 가중치를 학습할 때 연쇄법칙을 많이 쓴다고 했는데, 시그모이드의 이 도함수가 그 연쇄에 자주 들어가요.

#### 완성 답과 검산

#### 검산

별도 symbolic 미분에서 $e^{-x}/(1+e^{-x})^2=f(1-f)$를 확인해요. x=0이면f=1/2이고 도함수1/4예요.

정답: $f'(x) = \frac{\exp(-x)}{(1 + \exp(-x))^2} = f(x)(1 - f(x))$

#### 여기서 주의해요

안쪽의 −1을 빠뜨리면 감소함수라는 잘못된 결과가 나와요.

#### 설명을 닫고 다시 해요

1. $u=1+e^{-x}$, $f=u^{-1}$예요.
2. 각 소문항의 계산과 이유를 직접 적어요.
3. 안쪽의 −1을 빠뜨리면 감소함수라는 잘못된 결과가 나와요.

**페이지 요약**

#### 떠올릴 개념·공식

시그모이드(sigmoid)는 $(1+e^{-x})^{-1}$ 합성함수예요.

#### 첫 줄

$u=1+e^{-x}$, $f=u^{-1}$예요.

#### 검산

별도 symbolic 미분에서 $e^{-x}/(1+e^{-x})^2=f(1-f)$를 확인해요. x=0이면f=1/2이고 도함수1/4예요.

---

원 문제·정리노트·PDF는 보존해요.
