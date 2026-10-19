# 머신러닝기초 중간고사 모의평가 2회 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [1. 매개변수에 따라 바뀌는 기저와 해](#p1)
  - [2. 합성함수의 미분과 방향 변화](#p2)
  - [3. 다변량 Gaussian의 아핀 변환](#p3)
  - [4. Gaussian 곱에서 posterior와 evidence 읽기](#p4)
  - [5. 입력에는 비선형인 특징과 최소제곱](#p5)
  - [6. 스칼라 선형 모델에서 ML과 투영식 유도](#p6)
  - [7. 서로 다른 prior 분산과 MAP](#p7)
  - [8. 사후 불확실성과 두 미래 관측의 관계](#p8)
  - [9. 공유 모수 모델과 독립 모수 모델의 evidence](#p9)
  - [10. 직교투영과 ridge 예측의 차이](#p10)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### 1. 매개변수에 따라 바뀌는 기저와 해

EXAM Problem 1 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p1)

#### 주어진 조건

열벡터 $v_1=(1,0,1)^\top$, $v_2=(0,1,1)^\top$, $v_3=(1,1,t)^\top$와 $V(t)=[v_1\ v_2\ v_3]$를 생각하자. $t\in\mathbb R$이다.

#### 구할 것

1. $\det V(t)$를 구하고 세 벡터가 $\mathbb R^3$의 기저가 되는 $t$의 조건을 밝혀라.
2. $t=2$일 때 $V(2)\alpha=(1,2,3)^\top$의 모든 해를 구하라. 우변이 $(1,2,4)^\top$이면 해가 있는지 설명하라.
3. $t=3$일 때 $V(3)\alpha=(1,2,4)^\top$를 풀고, (b)의 같은 우변과 결과가 달라지는 이유를 열공간과 연결하라.

#### 문제를 내 말로 읽어요

같은 두 방향에 세 번째 벡터를 더했을 때 새로운 방향이 생기는지 보는 문제예요. $t$가 달라지면 세 번째 벡터의 마지막 성분만 바뀌어요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“기저”라는 표현에서 span과 선형독립(linear independence)을 함께 떠올려요. $3\times3$ 정사각행렬에서는 determinant가 0이 아니면 세 열이 $\mathbb R^3$의 기저예요. 행렬식이 0이면 우변이 column space에 들어가는지 따로 판단하고, 해가 있으면 자유변수를 남겨요.

출제 근거: HW1 P6-P8. MML PDF 46, 47쪽의 개념을 사용한 새 변형·응용 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$v_3-v_1-v_2=(0,0,t-2)^\top$부터 적어요. 열을 빼는 연산은 행렬식을 바꾸지 않으므로 세 번째 방향의 독립성을 바로 읽을 수 있어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

셋째 열에서 앞의 두 열을 빼면

$$
\det V(t)=\det\begin{pmatrix}1&0&0\\0&1&0\\1&1&t-2\end{pmatrix}=t-2.
$$

따라서 $t\ne2$이면 세 열은 독립이고 $\mathbb R^3$의 기저예요. $t=2$에서는 $v_3=v_1+v_2$라서 독립이 아니에요.

#### (b)

$t=2$에서 $\alpha_1+\alpha_3=1$, $\alpha_2+\alpha_3=2$예요. 세 번째 식은 이 둘의 합이에요. $s=\alpha_3\in\mathbb R$로 두면

$$
\alpha=(1-s,2-s,s)^\top.
$$

모든 열은 $z_3=z_1+z_2$라는 평면 위에 있어요. $(1,2,4)^\top$는 $4\ne1+2$라서 그 평면 밖이고 해가 없어요.

#### (c)

$t=3$에서는 앞의 두 식을 이용하면 셋째 식이 $3+\alpha_3=4$가 돼요. 그래서

$$
\alpha=(0,1,1)^\top.
$$

이때 행렬식은1이므로 열공간은 $\mathbb R^3$ 전체예요. (b)에서 만들 수 없던 우변도 이번에는 유일하게 만들 수 있어요.

#### 완성 답과 검산

#### (a) 검산

$t=2$를 대입하면 행렬식이0, $t=3$에서는1이에요. $v_3-v_1-v_2$도 각각 영벡터와 $(0,0,1)^\top$가 돼요.

#### (b) 검산

일반해를 원래 식에 넣으면 $(1,2,3)^\top$가 나와요. 세 번째 성분 관계가 맞는 모든 $s$가 허용돼요. 다른 우변은 그 관계를 위반해요.

#### (c) 검산

$v_2+v_3=(0,1,1)^\top+(1,1,3)^\top=(1,2,4)^\top$예요. 비영 행렬식이 해의 존재와 유일성을 함께 보장해요.

#### 여기서 헷갈리기 쉬워요

행렬식0은 “모든 우변에 해가 없다”는 뜻이 아니에요. 열공간 안의 우변에는 해가 있고, 밖의 우변에는 해가 없어요.

#### 설명을 닫고 다시 풀어요

- 조건에서 필요한 개념과 가정을 직접 적어요.
- 첫 식부터 각 소문항의 답까지 이어 써요.
- 검산으로 결과와 차원을 다시 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\det V=t-2$. $t=2$에서는 평면 $z_3=z_1+z_2$; $t\ne2$에서는 전체 $\mathbb R^3$.

#### 적용 조건

열벡터; 실수 매개변수; 독립 여부를 계산으로 판정

---

<a id="p2"></a>

### 2. 합성함수의 미분과 방향 변화

EXAM Problem 2 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p2)

#### 주어진 조건

$x=(x_1,x_2)^\top$에 대해 $f(x)=(x_1+x_2,x_1x_2)^\top$, $\ell(z)=\tfrac12\|z-(1,2)^\top\|^2$, $L(x)=\ell(f(x))$라 하자. Gradient는 열벡터, Jacobian은 $(J_f)_{ij}=\partial f_i/\partial x_j$이다.

#### 구할 것

1. $J_f(x)$와 $J_f(1,2)$를 구하고 차원을 써라.
2. 연쇄법칙으로 $\nabla_x L(1,2)$를 구하라. $L(x)$를 성분으로 전개해 직접 미분한 결과와도 비교하라.
3. $d=(1,-1)^\top$에 대해 $D_dL(1,2)=\left.\frac{d}{dh}L((1,2)^\top+hd)\right|_{h=0}$를 구하라. 이 값이 0이면 $(1,2)^\top$가 정지점인지 설명하라.

#### 문제를 내 말로 읽어요

$x$를 $f$로 먼저 바꾼 뒤 그 결과의 손실을 계산해요. 손실이 $z$에 대해 변하는 양과 $z$가 $x$에 대해 변하는 양을 연결해야 해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“합성함수”가 chain rule의 단서예요. $z=f(x)$일 때 열 gradient는 $\nabla_xL=J_f^\top\nabla_z\ell$이에요. $J_f$의 행은 출력 성분, 열은 입력 성분이므로 여기서는 $2\times2$예요. $\ell=\frac12\|z-a\|^2$의 gradient는 $z-a$예요. 문제에서 정의한 방향 변화는 $D_dL=\nabla L^\top d$이며 $d$를 단위벡터로 바꾸지 않아요.

출제 근거: HW1 P10-P12. MML PDF 153, 156, 159쪽의 개념을 사용한 새 변형·응용 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$z=f(1,2)=(3,2)^\top$와 $\nabla_z\ell=(3,2)^\top-(1,2)^\top=(2,0)^\top$를 먼저 써요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

출력별로 미분하면

$$
J_f(x)=\begin{pmatrix}1&1\\x_2&x_1\end{pmatrix},\quad J_f(1,2)=\begin{pmatrix}1&1\\2&1\end{pmatrix}.
$$

입력과 출력이 각각2개이므로 $2\times2$예요.

#### (b)

열 gradient를 연결하려면 전치가 필요해요.

$$
\nabla_xL(1,2)=\begin{pmatrix}1&2\\1&1\end{pmatrix}\begin{pmatrix}2\\0\end{pmatrix}=\begin{pmatrix}2\\2\end{pmatrix}.
$$

직접 전개하면 $L=\frac12(x_1+x_2-1)^2+\frac12(x_1x_2-2)^2$예요. 따라서

$$
\partial_{x_1}L=x_1+x_2-1+x_2(x_1x_2-2),
$$

$$
\partial_{x_2}L=x_1+x_2-1+x_1(x_1x_2-2).
$$

$(1,2)$에서 모두2로 일치해요.

#### (c)

$$
D_dL(1,2)=(2,2)\begin{pmatrix}1\\-1\end{pmatrix}=0.
$$

특정 방향 하나에서 1차 변화가 없다는 뜻이에요. 정지점은 모든 방향에서 1차 변화가 없어야 하며 $\nabla L=0$이어야 해요. 여기서는 gradient가 $(2,2)^\top\ne0$이므로 정지점이 아니에요.

#### 완성 답과 검산

#### (a) 검산

$f_2=x_1x_2$를 $x_1$로 미분하면 $x_2$예요. 이 항이 둘째 행 첫째 열에 있는지 확인해요.

#### (b) 검산

합성 경로와 직접 미분의 두 결과가 $(2,2)^\top$로 같아요. $J_f\nabla_z\ell$로 잘못 곱하면 $(2,4)^\top$가 되므로 직접 미분이 전치 오류를 잡아줘요.

#### (c) 검산

$x(h)=(1+h,2-h)$이면 $L(x(h))=2+\frac12(h-h^2)^2$예요. $h=0$의 미분이0으로 확인돼요. 반면 $e_1$ 방향 미분은2이므로 정지점일 수 없어요.

#### 여기서 헷갈리기 쉬워요

한 방향의 미분0과 gradient0을 혼동하지 않아요. 또 출력에서 입력으로 열 gradient를 되돌릴 때는 Jacobian의 전치를 곱해요.

#### 설명을 닫고 다시 풀어요

- 조건에서 필요한 개념과 가정을 직접 적어요.
- 첫 식부터 각 소문항의 답까지 이어 써요.
- 검산으로 결과와 차원을 다시 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\nabla_xL=J_f^\top\nabla_z\ell=(2,2)^\top$. $D_dL=0$이지만 정지점은 아니에요.

#### 적용 조건

gradient 열벡터; 방향 d의 h-미분 정의 사용

---

<a id="p3"></a>

### 3. 다변량 Gaussian의 아핀 변환

EXAM Problem 3 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p3)

#### 주어진 조건

$X\sim\mathcal N(\mu,\Sigma)$인 2차원 Gaussian 확률벡터이다.

$$
\mu=\begin{pmatrix}1\\-1\end{pmatrix},\quad\Sigma=\begin{pmatrix}2&1\\1&2\end{pmatrix},\quad Y=AX+b,
$$

$$
A=\begin{pmatrix}1&1\\1&-1\end{pmatrix},\quad b=\begin{pmatrix}0\\2\end{pmatrix}.
$$

#### 구할 것

1. $E[Y]$와 $\operatorname{Cov}(Y)$를 구하라.
2. $Y_1,Y_2$의 주변분포와 정규화 상수를 포함한 결합밀도 $p_Y(y_1,y_2)$를 써라.
3. $Y_1,Y_2$는 독립인가? 원래의 $X_1,X_2$에 대해서도 독립인지 판단하고, 두 결론의 근거를 설명하라.

#### 문제를 내 말로 읽어요

확률벡터를 더하기와 빼기로 바꾸었을 때 중심과 퍼짐이 어떻게 변하는지 계산해요. 이번에는 원래부터 공동 Gaussian이라는 조건이 있어요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“아핀 변환(affine transformation)” $Y=AX+b$에서는 평균 $A\mu+b$, 공분산 $A\Sigma A^\top$를 써요. 상수 $b$는 중심화하면 없어지므로 공분산에 들어가지 않아요. 두 변수의 공분산이0이어도 일반적으로 독립은 아니지만, 공동 Gaussian에서는 대각 공분산이 밀도 곱분해를 보장해요. 양의 정부호 공분산 $C$인 2차원 Gaussian의 앞 계수는 $1/(2\pi\sqrt{\det C})$예요.

출제 근거: HW1 P13/P22. MML PDF 198, 200, 206쪽의 개념을 사용한 새 변형·응용 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$A\mu=(0,2)^\top$와 $A\Sigma=\begin{pmatrix}3&3\\1&-1\end{pmatrix}$를 먼저 계산해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$$
\mu_Y=A\mu+b=(0,4)^\top,
$$

$$
\Sigma_Y=A\Sigma A^\top=\begin{pmatrix}6&0\\0&2\end{pmatrix}.
$$

변환행렬은 $2\times2$이고 결과 공분산도 $2\times2$예요.

#### (b)

아핀 변환 후에도 Gaussian이므로 $Y_1\sim\mathcal N(0,6)$, $Y_2\sim\mathcal N(4,2)$예요. $\det\Sigma_Y=12$이며 역행렬은 $\operatorname{diag}(1/6,1/2)$예요. 따라서

$$
p_Y(y_1,y_2)=\frac{1}{4\pi\sqrt3}\exp\!\left[-\frac{y_1^2}{12}-\frac{(y_2-4)^2}{4}\right].
$$

#### (c)

위 밀도는 $\mathcal N(y_1\mid0,6)\mathcal N(y_2\mid4,2)$로 곱분해돼요. 따라서 $Y_1,Y_2$는 독립이에요. 원래 $X_1,X_2$는 공분산이1로 0이 아니므로 독립이 아니에요. 독립이고 유한한 분산을 가지면 공분산이0이어야 하기 때문이에요.

#### 완성 답과 검산

#### (a) 검산

$\operatorname{Var}(X_1+X_2)=2+2+2=6$, $\operatorname{Var}(X_1-X_2)=2+2-2=2$예요. 교차 공분산은 $2-2=0$으로 행렬 계산과 일치해요.

#### (b) 검산

주변 밀도의 앞 계수 곱은 $1/\sqrt{12\pi}\cdot1/\sqrt{4\pi}=1/(4\pi\sqrt3)$이에요. 두 밀도의 적분이 각각1이므로 결합밀도 적분도1이에요.

#### (c) 검산

$E[X_1X_2]=\operatorname{Cov}(X_1,X_2)+E[X_1]E[X_2]=1-1=0$인 반면 평균의 곱은 $-1$이에요. 두 값이 달라 독립일 수 없어요.

#### 여기서 헷갈리기 쉬워요

공분산 변환에서 오른쪽의 $A^\top$를 빠뜨리지 않아요. “무상관이면 독립”이라는 결론은 여기의 공동 Gaussian 조건을 함께 써야 해요.

#### 설명을 닫고 다시 풀어요

- 조건에서 필요한 개념과 가정을 직접 적어요.
- 첫 식부터 각 소문항의 답까지 이어 써요.
- 검산으로 결과와 차원을 다시 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

$Y\sim\mathcal N((0,4)^\top,\operatorname{diag}(6,2))$. 공동 Gaussian이고 교차 공분산0이므로 독립이에요.

#### 적용 조건

공동 Gaussian; covariance 양의 정부호

---

<a id="p4"></a>

### 4. Gaussian 곱에서 posterior와 evidence 읽기

EXAM Problem 4 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p4)

#### 주어진 조건

스칼라 $\theta$의 prior는 $\mathcal N(\theta\mid-1,2)$이고 $y\mid\theta\sim\mathcal N(\theta,2)$이다. $y=3$을 관측했다. Gaussian의 둘째 인수는 분산이다. $g(\theta)=p(y=3\mid\theta)p(\theta)$, $Z=\int g(\theta)d\theta$로 둔다.

#### 구할 것

1. $g(\theta)$를 앞 계수까지 쓰고, 지수 안의 $\frac{(\theta+1)^2}{2}+\frac{(3-\theta)^2}{2}$를 완전제곱하라.
2. $p(\theta\mid y=3)$의 평균·분산과 밀도를 구하라. ML과 MAP 추정값을 각각 구하라.
3. $Z=p(y=3)$를 구하라. $Z$가 posterior 밀도 $p(\theta\mid y=3)$와 어떻게 다른지 설명하라.

#### 문제를 내 말로 읽어요

관측3은 모수가3 부근이라는 정보를 주고 prior는 -1 부근이라는 정보를 줘요. 두 정보의 곱을 정규화하면 posterior가 돼요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“Gaussian prior×likelihood”는 precision(분산의 역수)을 더하는 단서예요. Posterior precision은 $1/2+1/2=1$이에요. Posterior는 $\theta$에 대한 밀도이고 evidence는 관측 $y$의 주변밀도 값이에요. Evidence는 $\theta$를 적분해서 없애며 posterior를 정규화해요. ML은 likelihood만, MAP는 prior까지 사용해요.

출제 근거: HW1 P14/P25. MML PDF 207, 208쪽의 개념을 사용한 새 변형·응용 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$g(\theta)=\frac1{4\pi}\exp[-\frac12\{(\theta+1)^2/2+(3-\theta)^2/2\}]$부터 써요. 각 Gaussian의 앞 계수는 $1/\sqrt{4\pi}$예요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$$
g(\theta)=\frac1{4\pi}\exp\!\left[-\frac12\left\{\frac{(\theta+1)^2}{2}+\frac{(3-\theta)^2}{2}\right\}\right].
$$

중괄호 안은 $\theta^2-2\theta+5=(\theta-1)^2+4$예요. 따라서

$$
g(\theta)=\frac{e^{-2}}{4\pi}e^{-(\theta-1)^2/2}.
$$

상수 $e^{-2}$는 evidence 계산을 위해 남겨요.

#### (b)

정규화된 밀도는

$$
p(\theta\mid y=3)=\frac1{\sqrt{2\pi}}e^{-(\theta-1)^2/2}=\mathcal N(\theta\mid1,1).
$$

평균1, 분산1이에요. Likelihood는 $(3-\theta)^2$가 작을수록 크므로 $\theta_{\mathrm{ML}}=3$이에요. Posterior의 최빈값은 $\theta_{\mathrm{MAP}}=1$이에요.

#### (c)

$$
Z=\frac{e^{-2}}{4\pi}\int e^{-(\theta-1)^2/2}d\theta=\frac{e^{-2}}{\sqrt{8\pi}}.
$$

Prior와 독립 잡음을 더하면 $y\sim\mathcal N(-1,4)$이므로 $p(y=3)$로도 같은 값을 얻어요. $Z$는 이 관측에서 하나의 수이고, posterior는 $\theta$에 따라 변하는 밀도예요.

#### 완성 답과 검산

#### (a) 검산

$\theta=1$일 때 원래 중괄호 값은 $4/2+4/2=4$예요. 완전제곱 표현에서도 $0+4=4$예요.

#### (b) 검산

Precision 계산으로 $v=(1/2+1/2)^{-1}=1$, $m=v(-1/2+3/2)=1$이에요. 두 정보가 같은 분산이어서 중심은 -1과3의 중간이에요.

#### (c) 검산

$Z\,p(\theta\mid3)$의 앞 계수는 $e^{-2}/(4\pi)$로 원래 $g$와 같아요. $y$의 평균 -1에서 관측3은4만큼 떨어지고 총분산4이므로 지수는 -2예요.

#### 여기서 헷갈리기 쉬워요

완전제곱 뒤 상수항을 버리면 posterior의 모양만 찾을 수 있어요. Evidence에는 지수의 상수항과 원래 앞 계수가 모두 필요해요.

#### 설명을 닫고 다시 풀어요

- 조건에서 필요한 개념과 가정을 직접 적어요.
- 첫 식부터 각 소문항의 답까지 이어 써요.
- 검산으로 결과와 차원을 다시 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

Posterior $\mathcal N(1,1)$, ML3, MAP1. Evidence $Z=e^{-2}/\sqrt{8\pi}$.

#### 적용 조건

분산 표기; prior와 알려진 관측잡음

---

<a id="p5"></a>

### 5. 입력에는 비선형인 특징과 최소제곱

EXAM Problem 5 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p5)

#### 주어진 조건

관측 $(x_n,y_n)=(-1,2),(0,0),(1,4)$와 특징 $\phi(x)=(1,x^2)^\top$를 사용한다. $y_n=\phi(x_n)^\top\theta+\epsilon_n$, 독립 $\epsilon_n\sim\mathcal N(0,1)$이다. MAP에서는 두 계수 모두 $\theta\sim\mathcal N(0,I_2)$ prior를 사용한다. $\Phi$의 각 행은 $\phi(x_n)^\top$이다.

#### 구할 것

1. $\Phi$, $\Phi^\top\Phi$, $\Phi^\top y$를 구하라. $x=-1$과 $x=1$의 행이 같아도 Gram 행렬이 가역인지 판단하라.
2. $\theta_{\mathrm{ML}}$, 잔차벡터, 잔차제곱합을 구하고 $x_*=2$에서 평균을 예측하라.
3. $\theta_{\mathrm{MAP}}$와 $x_*=2$에서의 평균 예측을 구하라. 이 모델을 선형 회귀라고 부르는 이유를 설명하라.

#### 문제를 내 말로 읽어요

$x=-1$과1은 $x^2$가 같아서 같은 특징으로 표현돼요. 그래도 상수 열과 제곱 열이 서로 다른 방향인지 따로 확인해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“특징(feature)”은 입력을 모형이 읽는 표현이에요. 각 관측의 특징을 행으로 쌓으면 $\Phi\in\mathbb R^{3\times2}$예요. 행 중복은 열종속과 같지 않아요. Gaussian 잡음에서 ML은 정규방정식 $\Phi^\top\Phi\theta=\Phi^\top y$를 풀어요. 잡음분산1과 prior $I$이면 MAP는 Gram 행렬에 $I$를 더해요. 모델의 선형성은 입력 $x$보다 모수 $\theta$에 대해 판단해요.

출제 근거: HW1 P9/P17-P19. MML PDF 298, 300, 302쪽의 개념을 사용한 새 변형·응용 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$\Phi=\begin{pmatrix}1&1\\1&0\\1&1\end{pmatrix}$와 $y=(2,0,4)^\top$를 적고 열별 내적을 계산해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$$
\Phi=\begin{pmatrix}1&1\\1&0\\1&1\end{pmatrix},\quad G=\Phi^\top\Phi=\begin{pmatrix}3&2\\2&2\end{pmatrix},
$$

$$
\Phi^\top y=\begin{pmatrix}6\\6\end{pmatrix}.
$$

$\det G=6-4=2>0$이므로 가역이에요. 첫째와 셋째 행이 같아도 두 열은 독립이에요.

#### (b)

$3\theta_0+2\theta_1=6$, $2\theta_0+2\theta_1=6$에서

$$
\theta_{\mathrm{ML}}=(0,3)^\top.
$$

학습 예측은 $(3,0,3)^\top$, 잔차는 $r=y-\Phi\theta=(-1,0,1)^\top$이며 $\|r\|^2=2$예요. $x_*=2$에서는 $\phi=(1,4)^\top$이므로 평균 예측은12예요.

#### (c)

$$
\begin{pmatrix}4&2\\2&3\end{pmatrix}\theta_{\mathrm{MAP}}=\begin{pmatrix}6\\6\end{pmatrix}
$$

을 풀면 $\theta_{\mathrm{MAP}}=(3/4,3/2)^\top$예요. $x_*=2$에서 평균은 $3/4+4(3/2)=27/4$예요. $\theta_0+\theta_1x^2$는 $\theta_0,\theta_1$의 선형결합이므로 선형 회귀예요.

#### 완성 답과 검산

#### (a) 검산

$a(1,1,1)^\top+b(1,0,1)^\top=0$의 가운데 성분에서 $a=0$, 첫째 성분에서 $b=0$이에요. 열독립이 직접 확인돼요.

#### (b) 검산

$\Phi^\top r=(0,0)^\top$예요. 같은 특징을 가진 두 관측의 출력2와4는 하나의 공통 예측3으로 맞추어져요.

#### (c) 검산

$(G+I)(3/4,3/2)^\top=(6,6)^\top$예요. MAP 잔차 $(-1/4,-3/4,7/4)^\top$에 대해 $\Phi^\top r=(3/4,3/2)^\top=\theta_{\mathrm{MAP}}$이므로 벌점 정규방정식도 맞아요.

#### 여기서 헷갈리기 쉬워요

$x=2$에서 특징의 둘째 성분은2가 아니라4예요. 행 중복만 보고 역행렬이 없다고 판단하지 말고 열의 독립성이나 Gram 행렬식을 확인해요.

#### 설명을 닫고 다시 풀어요

- 조건에서 필요한 개념과 가정을 직접 적어요.
- 첫 식부터 각 소문항의 답까지 이어 써요.
- 검산으로 결과와 차원을 다시 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

ML $(0,3)^\top$, SSE2, 예측12. MAP $(3/4,3/2)^\top$, 예측 $27/4$.

#### 적용 조건

독립 잡음 분산1; 두 계수 모두 prior

---

<a id="p6"></a>

### 6. 스칼라 선형 모델에서 ML과 투영식 유도

EXAM Problem 6 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p6)

#### 주어진 조건

고정 입력 $x_n\in\mathbb R$와 관측 $y_n=\theta x_n+\epsilon_n$을 생각하자. $\theta\in\mathbb R$는 미지수이며 잡음들은 서로 독립 $\mathcal N(0,\sigma^2)$를 따른다. $\sigma^2>0$는 알려져 있고 $\sum_n x_n^2>0$이다. $x=(x_1,\ldots,x_N)^\top$, $y=(y_1,\ldots,y_N)^\top$이다.

#### 구할 것

1. 입력과 $\theta$가 주어졌을 때 각 $y_n$의 분포를 쓰고, 독립성을 이용해 결합우도 $p(y\mid x,\theta)$를 정규화 상수까지 구성하라.
2. 소문항 (a)에 음의 로그를 취하라. $\theta$와 무관한 항을 분리해 제곱오차 최소화와 연결하라.
3. 소문항 (b)의 제곱오차를 $\theta$에 대해 전개하고 미분하여 ML 추정식과 분모 조건을 도출하라.
4. 소문항 (c)의 정지점이 유일한 최소점임을 이계미분으로 보여라. $x,y\in\mathbb R^N$의 내적으로 추정식을 다시 써라.
5. 소문항 (d)의 식을 $\widehat y=x\widehat\theta$에 대입해 $\widehat y=Py$의 행렬 $P$를 도출하고 $x^\top(y-\widehat y)=0$을 보여라.
6. $x=(1,2,-1)^\top$, $y=(1,3,0)^\top$에서 (c), (e)의 추정값·예측·잔차제곱합을 계산하라.

#### 문제를 내 말로 읽어요

스칼라 선형 모델에서 ML과 투영식 유도: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 스칼라 선형 회귀의 ML 공식과 직선으로의 투영에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“스칼라 계수에 독립 Gaussian 잡음”이라는 조건에서 likelihood 최대화를 떠올려요. 입력은 고정이고 관측의 평균만 $\theta x_n$으로 달라져요. 알려진 양의 분산이면 음의 로그우도의 최소점은 제곱오차의 최소점과 같아요. 합을 전개한 뒤 스칼라 미분으로 추정식을 만들어요. $\sum x_n^2>0$은 분모와 곡률이 양수라는 조건이에요. 최종 예측을 입력벡터의 상수배로 쓰면 직교투영과 연결돼요.

출제 근거: MML 9.2 ML; 1019 scalar linear model and projection. MML PDF 298, 299, 300쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$p(y\mid x,\theta)=\prod_n p(y_n\mid x_n,\theta)$를 적고 각 항에 평균 $\theta x_n$인 Gaussian 밀도를 넣어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$y_n=\theta x_n+\epsilon_n$이므로

$$
y_n\mid x,\theta\sim\mathcal N(\theta x_n,\sigma^2).
$$

독립 잡음의 밀도를 곱하면

$$
p(y\mid x,\theta)=(2\pi\sigma^2)^{-N/2}\exp\!\left[-\frac{\sum_n(y_n-\theta x_n)^2}{2\sigma^2}\right].
$$

모수는 스칼라 하나이고 입력 벡터는 고정이에요.

#### (b)

(a)의 음의 로그는

$$
\mathcal L=\frac N2\log(2\pi\sigma^2)+\frac{Q(\theta)}{2\sigma^2},\quad Q=\sum_n(y_n-\theta x_n)^2.
$$

첫 항은 $\theta$와 무관하고 둘째 항의 배율은 양수여서 $Q$를 최소화해도 같아요.

#### (c)

(b)의 합을 전개해요.

$$
Q=\sum y_n^2-2\theta\sum x_ny_n+\theta^2\sum x_n^2.
$$

따라서 $Q^{\prime}=-2\sum x_ny_n+2\theta\sum x_n^2$예요. 0으로 놓으면

$$
\widehat\theta=\frac{\sum x_ny_n}{\sum x_n^2}.
$$

가정한 $\sum x_n^2>0$ 덕분에 나눌 수 있어요.

#### (d)

(c)에서 $Q^{\prime\prime}=2\sum x_n^2>0$이므로 유일한 최소점이에요. 열벡터 내적으로 바꾸면

$$
\widehat\theta=\frac{x^\top y}{x^\top x}.
$$

이때 분자와 분모 모두 스칼라예요.

#### (e)

(d)를 예측식에 넣고 $y$를 오른쪽으로 모아요.

$$
\widehat y=\frac{xx^\top}{x^\top x}y,\quad P=\frac{xx^\top}{x^\top x}.
$$

따라서

$$
x^\top(y-\widehat y)=x^\top y-\frac{x^\top x}{x^\top x}x^\top y=0.
$$

예측은 $x$가 만드는 직선 위에 있고 잔차는 그 직선에 수직이에요.

#### (f)

$x^\top x=6$, $x^\top y=7$이므로 $\widehat\theta=7/6$이에요.

$$
\widehat y=(7/6,7/3,-7/6)^\top,
$$

$$
r=(-1/6,2/3,7/6)^\top.
$$

잔차제곱합은 $1/36+4/9+49/36=11/6$이에요.

#### 완성 답과 검산

#### (a) 검산

$N=1$로 놓으면 단일 Gaussian likelihood예요. 분산은 추정 대상이 아닌 알려진 상수예요.

#### (b) 검산

로그를 취한 뒤 지수의 음수와 바깥 음수가 상쇄되어 제곱항이 양수가 돼요.

#### (c) 검산

$\sum x_n^2\widehat\theta=\sum x_ny_n$이므로 미분식에 대입하면0이에요.

#### (d) 검산

$Q(\theta)=Q(\widehat\theta)+(x^\top x)(\theta-\widehat\theta)^2$로도 전역 최소가 확인돼요.

#### (e) 검산

$P^\top=P$, $P^2=P$예요. $xx^\top$는 $N\times N$이고 분모는 양수 스칼라예요.

#### (f) 검산

$x^\top r=-1/6+4/3-7/6=0$이에요. 또 $y^\top y-(x^\top y)^2/(x^\top x)=10-49/6=11/6$으로 SSE가 같아요.

#### 여기서 헷갈리기 쉬워요

모수가 스칼라인 것과 데이터가 한 개인 것은 달라요. $x$는 길이 $N$인 열벡터예요. $x^\top x$는 스칼라이고 $xx^\top$는 행렬이므로 순서를 바꾸면 차원이 달라져요.

#### 설명을 닫고 다시 풀어요

- 각 소문항에서 얻은 식을 다음 소문항의 첫 줄로 옮겨요.
- 모델에서 시작해 최종 공식을 보지 않고 유도해요.
- 독립성·차원·역행렬 조건을 설명하며 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

우도 → 로그 → 제곱오차 미분 → $\widehat\theta=(x^\top y)/(x^\top x)$ → $P=xx^\top/(x^\top x)$. 수치 예에서 추정값 $7/6$, SSE $11/6$이에요.

#### 적용 조건

알려진 sigma^2&gt;0; 고정 입력; sum x_n^2&gt;0; 스칼라 모수

---

<a id="p7"></a>

### 7. 서로 다른 prior 분산과 MAP

EXAM Problem 7 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p7)

#### 주어진 조건

$\Phi=\begin{pmatrix}1&-1\\1&1\end{pmatrix}$, $y=(0,4)^\top$에 대해 $y\mid\theta\sim\mathcal N(\Phi\theta,\sigma^2I_2)$이다. Prior는 $\theta\sim\mathcal N(m_0,S_0)$이며 $m_0=(2,0)^\top$, $S_0=\operatorname{diag}(4,1)$이다. $\sigma^2>0$는 알려져 있고 prior는 두 계수에 모두 적용된다.

#### 구할 것

1. likelihood와 prior를 곱하고 Bayes 정리를 이용해 음의 로그 posterior를 $\theta$와 무관한 상수와 두 이차항으로 나타내라.
2. 소문항 (a)의 두 이차항을 각각 열 gradient로 미분하라. $S_0^{-1}$가 등장하는 이유도 설명하라.
3. 소문항 (b)를0으로 놓아 MAP 정규방정식과 추정식을 도출하라. 이 단계에서는 $\sigma^2,m_0,S_0$를 기호로 남겨라.
4. 소문항 (c)의 계수행렬이 양의 정부호임을 이차형식으로 보여 해의 유일성을 설명하라.
5. $\sigma^2=1$을 (c)에 대입해 MAP과 $x_*=2$, $\phi(x_*)=(1,2)^\top$에서 평균 예측을 구하라. ML과 비교하라.
6. 소문항 (c)를 이용해 이 데이터에서 MAP의 두 성분을 $\sigma^2$의 함수로 구하고, $\sigma^2\to0^+$와 $\sigma^2\to\infty$의 극한을 해석하라.

#### 문제를 내 말로 읽어요

서로 다른 prior 분산과 MAP: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 일반 Gaussian prior의 MAP 추정식에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“서로 다른 prior 분산”이 보이면 scalar ridge 계수 하나보다 precision matrix $S_0^{-1}$를 떠올려요. 큰 prior 분산은 더 약한 벌점을 뜻해요. 일반 Gaussian prior에서 NLL에 $\frac12(\theta-m_0)^\top S_0^{-1}(\theta-m_0)$를 더해요. MAP는 이 quadratic objective의 최소점이에요. 양의 정부호 precision은 역행렬과 해의 유일성을 보장해요.

출제 근거: MML 9.2.3 Gaussian MAP with diagonal prior. MML PDF 307, 308, 309쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$S_0^{-1}=\operatorname{diag}(1/4,1)$, $G=2I_2$, $\Phi^\top y=(4,4)^\top$를 먼저 써요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

Posterior는 $p(y\mid\theta)p(\theta)$에 비례해요. Gaussian 지수 두 개를 더하고 음의 로그를 취하면

$$
J=\frac{\|y-\Phi\theta\|^2}{2\sigma^2}+\frac12(\theta-m_0)^\top S_0^{-1}(\theta-m_0)+C.
$$

$C$에는 고정 분산의 정규화 상수와 evidence를 모아요.

#### (b)

(a)의 첫 항의 gradient는 $\Phi^\top(\Phi\theta-y)/\sigma^2$예요. 둘째 항은 대칭행렬 $S_0^{-1}$를 이용해 $S_0^{-1}(\theta-m_0)$예요. Gaussian 지수는 공분산의 역행렬인 precision으로 거리를 재므로 분산 자체가 아닌 역분산이 들어가요.

#### (c)

(b)의 합을0으로 놓으면

$$
B\theta=\frac{\Phi^\top y}{\sigma^2}+S_0^{-1}m_0,\quad B=\frac{\Phi^\top\Phi}{\sigma^2}+S_0^{-1}.
$$

따라서

$$
\theta_{\mathrm{MAP}}=B^{-1}\left(\frac{\Phi^\top y}{\sigma^2}+S_0^{-1}m_0\right).
$$

양변에 $\sigma^2$를 곱한 형태도 같아요.

#### (d)

비영 $a$에 대해

$$
a^\top Ba=\frac{\|\Phi a\|^2}{\sigma^2}+a^\top S_0^{-1}a>0.
$$

Proper Gaussian prior의 공분산 $S_0$가 양의 정부호이므로 역행렬도 양의 정부호예요. $B$는 목적함수의 Hessian이어서 정지점은 유일한 전역 최소점이에요.

#### (e)

$G=2I$, $\Phi^\top y=(4,4)^\top$, $S_0^{-1}=\operatorname{diag}(1/4,1)$이에요. (c)에서 $\sigma^2=1$이면

$$
\operatorname{diag}(9/4,3)\theta=(9/2,4)^\top.
$$

따라서 MAP는 $(2,4/3)^\top$, 평균 예측은 $14/3$이에요. ML는 $(2,2)^\top$, 평균 예측은6이에요.

#### (f)

(c)의 양변에 $\sigma^2$를 곱하면 두 성분은

$$
(2+\sigma^2/4)\theta_0=4+\sigma^2/2,
$$

$$
(2+\sigma^2)\theta_1=4.
$$

따라서 $\theta_0=2$, $\theta_1=4/(2+\sigma^2)$예요. 잡음분산이0으로 가면 ML $(2,2)^\top$, 무한히 커지면 prior 중심 $(2,0)^\top$로 수렴해요.

#### 완성 답과 검산

#### (a) 검산

Prior 항은 성분으로 $(\theta_0-2)^2/8+\theta_1^2/2$예요.

#### (b) 검산

Prior 중심에서 prior gradient가0이고 작은 prior 분산에 더 큰 precision이 적용돼요.

#### (c) 검산

양변에 $\sigma^2$를 곱하면 $(G+\sigma^2S_0^{-1})\theta=\Phi^\top y+\sigma^2S_0^{-1}m_0$예요.

#### (d) 검산

$Ba=0$인 비영 $a$를 가정하면 양수 이차형식과 모순이므로 가역이에요.

#### (e) 검산

MAP 잔차는 $(-2/3,2/3)^\top$이고 $\Phi^\top r=(0,4/3)^\top=S_0^{-1}(\theta-m_0)$예요.

#### (f) 검산

$\sigma^2=1$을 일반 성분식에 넣으면 (e)의 $4/3$이 다시 나와요.

#### 여기서 헷갈리기 쉬워요

Prior 분산4를 벌점4로 쓰면 반대로 계산한 거예요. 벌점은 역분산1/4이고, 중심이0이 아닌 prior에서는 우변의 $S_0^{-1}m_0$도 남겨야 해요.

#### 설명을 닫고 다시 풀어요

- 각 소문항에서 얻은 식을 다음 소문항의 첫 줄로 옮겨요.
- 모델에서 시작해 최종 공식을 보지 않고 유도해요.
- 독립성·차원·역행렬 조건을 설명하며 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\theta_{\mathrm{MAP}}=(2,4/3)^\top$ at $\sigma^2=1$. 잡음이 커질수록 prior 중심으로 수렴해요.

#### 적용 조건

proper diagonal prior; sigma^2&gt;0; full rank Phi

---

<a id="p8"></a>

### 8. 사후 불확실성과 두 미래 관측의 관계

EXAM Problem 8 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p8)

#### 주어진 조건

$\theta\sim\mathcal N(0,I_2)$, $y\mid\theta\sim\mathcal N(\Phi\theta,2I_2)$이고 $\Phi=\begin{pmatrix}1&-1\\1&1\end{pmatrix}$, 관측 $y=(0,2)^\top$이다. $\phi(x)=(1,x)^\top$로 둔다. 미래 값은 $f_* =\phi(x_*)^\top\theta$, $y_*=f_*+\epsilon_*$이다. 모든 미래 잡음은 서로 독립 $\mathcal N(0,2)$이며 $\theta$·학습 잡음과도 독립이다.

#### 구할 것

1. likelihood와 prior의 곱을 쓰고 $\theta$에 대한 지수를 전개하라. $-\tfrac12(\theta^\top B\theta-2b^\top\theta+c)$ 형태의 $B,b,c$를 구하라.
2. 소문항 (a)를 $\theta-m$에 대한 완전제곱으로 바꾸어 $m$과 posterior 공분산 $S$를 $B,b$로 표현하라. 정규화된 posterior 밀도도 써라.
3. 주어진 $\Phi,y$에 대해 (a), (b)의 행렬과 벡터를 계산하여 posterior 평균·공분산을 구하라.
4. 소문항 (c)를 이용해 임의의 $\phi_*$에 대한 $f_*=\phi_*^\top\theta$의 평균·분산을 도출하라. $x_*=1$에서 분포를 구하라.
5. 소문항 (d)에 미래 잡음을 더해 관측의 사후예측분포를 도출하라. $x_*=1$에서 MAP 고정 대입과 비교하라.
6. 소문항 (d), (e)의 논리를 두 미래 관측 $x=0,1$에 적용해 $y$를 조건으로 한 교차 공분산을 도출·계산하라. 모수를 주었을 때의 독립성이 모수 적분 후에도 유지되는가?

#### 문제를 내 말로 읽어요

사후 불확실성과 두 미래 관측의 관계: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 완전제곱으로 얻는 posterior와 사후예측 공식에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“Gaussian prior와 선형 Gaussian likelihood”는 Gaussian posterior의 precision 합을 떠올리는 단서예요. $S_N=(S_0^{-1}+\Phi^\top\Phi/\sigma^2)^{-1}$, $m_N=S_N(S_0^{-1}m_0+\Phi^\top y/\sigma^2)$예요. $f_*=\phi_*^\top\theta$의 분산은 $\phi_*^\top S_N\phi_*$이며 관측 $y_*$에는 독립 잡음분산을 더해요. 서로 다른 미래 관측의 공분산에서는 독립 잡음의 교차항은0이고 공유 모수의 항 $\phi_a^\top S_N\phi_b$만 남아요.

출제 근거: MML 9.3.3-9.3.4 posterior predictive; affine covariance. MML PDF 198, 312, 314, 315쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$p(\theta\mid y)\propto\exp[-\tfrac14\|y-\Phi\theta\|^2-\tfrac12\theta^\top\theta]$를 적고 $\theta$의 차수별로 항을 모아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

곱은 $\mathcal N(y\mid\Phi\theta,2I)\mathcal N(\theta\mid0,I)$예요. 지수는

$$
-\tfrac12\left(\tfrac12\|y-\Phi\theta\|^2+\theta^\top\theta\right).
$$

제곱을 전개해 모으면

$$
B=I+\tfrac12\Phi^\top\Phi,\quad b=\tfrac12\Phi^\top y,\quad c=\tfrac12 y^\top y.
$$

$B$는 이차항, $b$는 일차항의 계수예요.

#### (b)

(a)의 $m=B^{-1}b$로 두면

$$
\theta^\top B\theta-2b^\top\theta+c=(\theta-m)^\top B(\theta-m)+c-b^\top B^{-1}b.
$$

$B\succ0$이므로 $S=B^{-1}$예요. 모수 차원은2이므로 정규화된 밀도는

$$
p(\theta\mid y)=\frac{|B|^{1/2}}{2\pi}\exp[-\tfrac12(\theta-m)^\top B(\theta-m)].
$$

즉 $m,S$를 갖는 Gaussian이에요.

#### (c)

$\Phi^\top\Phi=2I$, $\Phi^\top y=(2,2)^\top$, $y^\top y=4$예요. 따라서 (a)는 $B=2I$, $b=(1,1)^\top$, $c=2$이고 (b)는

$$
S=\tfrac12 I,\quad m=(1/2,1/2)^\top.
$$

완전제곱에서 남는 상수는 $c-b^\top B^{-1}b=1$이에요.

#### (d)

(c)의 posterior로 평균내면

$$
E[f_*\mid y]=\phi_*^\top m.
$$

중심화한 제곱을 평균내면

$$
\operatorname{Var}(f_*\mid y)=E[\phi_*^\top(\theta-m)(\theta-m)^\top\phi_*\mid y]=\phi_*^\top S\phi_*.
$$

Gaussian의 선형변환이므로 $x_*=1$, $\phi_*=(1,1)^\top$에서 $f_*\mid y\sim\mathcal N(1,1)$이에요.

#### (e)

미래 잡음이 독립이고 평균0이므로 (d)의 평균은 유지되고 분산에는2를 더해요.

$$
y_*\mid y\sim\mathcal N(\phi_*^\top m,\phi_*^\top S\phi_*+2).
$$

$x_*=1$에서는 $\mathcal N(1,3)$이에요. MAP는 $m$이고 고정 대입 관측분포는 $\mathcal N(1,2)$여서 모수 불확실성1이 빠져요.

#### (f)

$\phi_0=(1,0)^\top$, $\phi_1=(1,1)^\top$예요. (d)의 중심화 계산을 두 출력의 곱으로 바꾸면

$$
\operatorname{Cov}(y_*^{(0)},y_*^{(1)}\mid y)=\phi_0^\top S\phi_1=1/2.
$$

미래 잡음끼리와 모수·잡음 사이 교차 공분산은0이에요. $\theta$를 주면 독립이지만 $y$만 주면 공유 모수가 불확실해 관측들이 독립이 아니에요.

#### 완성 답과 검산

#### (a) 검산

전개 전 지수에 $\theta=0$을 넣으면 $-1$이고 전개 후 $-c/2=-1$과 같아요.

#### (b) 검산

$B m=b$이므로 완전제곱의 교차항은 정확히 $-2b^\top\theta$예요. 밀도의 적분은1이에요.

#### (c) 검산

$B S=I$, $B m=b$이고 정규화 계수는 $1/\pi$예요.

#### (d) 검산

$f_*=\theta_0+\theta_1$의 분산은 $1/2+1/2=1$이에요.

#### (e) 검산

전체분산법칙도 관측분산 $2+1=3$을 줘요. 잡음을 두 번 더하지 않아요.

#### (f) 검산

두 관측의 공동 공분산은 $\begin{pmatrix}5/2&1/2\\1/2&3\end{pmatrix}$예요. 공유한 $\theta_0$의 분산 $1/2$이 비대각에 남아요.

#### 여기서 헷갈리기 쉬워요

“잡음 독립”을 “모수를 적분한 관측도 독립”으로 바꾸면 안 돼요. 또한 $f_*$와 $y_*$ 중 어떤 것을 예측하는지 구별해야 잡음분산을 빠뜨리거나 두 번 더하지 않아요.

#### 설명을 닫고 다시 풀어요

- 각 소문항에서 얻은 식을 다음 소문항의 첫 줄로 옮겨요.
- 모델에서 시작해 최종 공식을 보지 않고 유도해요.
- 독립성·차원·역행렬 조건을 설명하며 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

Posterior $m_N=(1/2,1/2)^\top$, $S_N=I/2$. 예측 $f_*:N(1,1)$, $y_*:N(1,3)$. 미래 교차 공분산1/2.

#### 적용 조건

독립 미래 잡음; 공통 posterior의 theta 적분

---

<a id="p9"></a>

### 9. 공유 모수 모델과 독립 모수 모델의 evidence

EXAM Problem 9 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p9)

#### 주어진 조건

두 관측 $y=(1,-1)^\top$를 비교한다. $M_1$은 공통 $\theta\sim\mathcal N(0,1)$와 $y_n=\theta+\epsilon_n$을, $M_2$는 서로 독립 $\theta_n\sim\mathcal N(0,1)$와 $y_n=\theta_n+\epsilon_n$을 사용한다. 두 모델에서 $\epsilon_1,\epsilon_2\overset{\mathrm{ind}}\sim\mathcal N(0,1)$이고 잡음과 모든 모수는 독립이다. 모델 공간은 $M_1,M_2$ 두 모델로만 구성된다. 모델 prior odds는 $P(M_1)/P(M_2)=3$이다.

#### 구할 것

1. 각 모델을 $y=B_i\vartheta_i+\epsilon$로 표현하라. $B_i$, 모수벡터 $\vartheta_i$의 prior와 $p(y\mid M_i)$의 적분식을 써라.
2. 소문항 (a)의 모수와 잡음의 독립성을 이용해 관측 주변분포의 평균·공분산을 정의에서 구하라. 주변분포가 Gaussian인 이유도 설명하라.
3. 소문항 (b)의 Gaussian 밀도를 정규화 상수까지 써라. 주어진 $y$에 대해 각 행렬식과 이차형식을 계산하여 두 evidence를 구하라.
4. 소문항 (c)의 evidence 비에서 Bayes factor $B_{12}$를 구하고 데이터가 지지하는 모델을 판단하라.
5. Bayes 정리로 posterior odds를 evidence 비와 prior odds로 표현하는 공식을 유도하라. (d)를 사용해 $P(M_1\mid y)$와 최종 선택을 구하라.

#### 문제를 내 말로 읽어요

공유 모수 모델과 독립 모수 모델의 evidence: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 주변화한 evidence와 Bayes 모델 비교 공식에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“모수를 적분한 evidence”에서는 한 번 최적화한 likelihood 대신 prior 아래의 관측분포를 구해요. 선형 Gaussian $y=B\theta+\epsilon$의 주변 공분산은 $BS_0B^\top+I$예요. 공통 모수는 관측 사이에 공분산을 만들어요. 다변량 Gaussian 밀도에는 $\det C$와 $y^\top C^{-1}y$가 모두 필요해요. Bayes factor는 evidence의 비이고 posterior odds는 여기에 모델 prior odds를 곱한 값이에요.

출제 근거: MML 9.3.5 evidence; shared versus separate parameters. MML PDF 205, 206, 312, 317, 318, 319쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$M_1$에서 $B=(1,1)^\top$, $M_2$에서 $B=I_2$라고 적어요. 각각 독립 잡음의 공분산 $I_2$를 더해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$M_1$은 $B_1=(1,1)^\top$, 스칼라 $\vartheta_1=\theta\sim\mathcal N(0,1)$이에요. $M_2$는 $B_2=I_2$, $\vartheta_2=(\theta_1,\theta_2)^\top\sim\mathcal N(0,I_2)$예요. 두 경우 모두

$$
p(y\mid M_i)=\int p(y\mid\vartheta_i,M_i)p(\vartheta_i\mid M_i)d\vartheta_i.
$$

한 점의 모수 대신 prior 전체로 평균내요.

#### (b)

(a)에서 평균은 $B_iE[\vartheta_i]+E[\epsilon]=0$이에요. 중심화한 곱의 평균에서 독립 교차항이0이라

$$
C_i=B_i\operatorname{Cov}(\vartheta_i)B_i^\top+I_2.
$$

따라서

$$
C_1=\begin{pmatrix}2&1\\1&2\end{pmatrix},\quad C_2=2I_2.
$$

독립 Gaussian의 선형변환과 합이므로 적분한 관측분포는 $\mathcal N(0,C_i)$예요.

#### (c)

(b)의 주변 밀도가 evidence예요.

$$
p(y\mid M_i)=\frac{\exp[-y^\top C_i^{-1}y/2]}{2\pi\sqrt{|C_i|}}.
$$

$C_1$의 행렬식은3, 역행렬은 $\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$이고 이차형식은2예요. $C_2$는 행렬식4, 이차형식1이에요. 따라서

$$
p_1=\frac{e^{-1}}{2\pi\sqrt3},\quad p_2=\frac{e^{-1/2}}{4\pi}.
$$

#### (d)

(c)의 비를 취하면

$$
B_{12}=\frac2{\sqrt3}e^{-1/2}\simeq0.70036<1.
$$

두 번째 모델의 evidence가 크므로 데이터만으로는 $M_2$를 지지해요.

#### (e)

Bayes 정리의 두 posterior를 나누면 공통 분모가 소거돼요.

$$
\frac{P(M_1\mid y)}{P(M_2\mid y)}=\frac{p(y\mid M_1)}{p(y\mid M_2)}\frac{P(M_1)}{P(M_2)}.
$$

따라서 $O=3B_{12}=2\sqrt3 e^{-1/2}\simeq2.10108$이고

$$
P(M_1\mid y)=\frac O{1+O}\simeq0.67753.
$$

최종 선택은 $M_1$이에요. 데이터는 처음3:1인 prior odds를 낮췄지만1아래로 뒤집지는 않았어요.

#### 완성 답과 검산

#### (a) 검산

$B_1$는 $2\times1$, $B_2$는 $2\times2$라 두 경우 모두 관측 차원은2예요.

#### (b) 검산

$M_1$의 비대각은 공유 모수의 분산1, $M_2$의 비대각은 독립성으로0이에요.

#### (c) 검산

$C_1y=y$라 $y^\top C_1^{-1}y=\|y\|^2=2$예요. $C_2^{-1}=I/2$에서는1이에요.

#### (d) 검산

$2/\sqrt3\simeq1.1547$에 $e^{-1/2}\simeq0.60653$을 곱하면0.70036이에요.

#### (e) 검산

Prior 확률 $3/4,1/4$로 직접 정규화해도 $(3p_1)/(3p_1+p_2)$로 같은 답이에요.

#### 여기서 헷갈리기 쉬워요

공통 모수를 적분하기 전에 관측 두 개를 무조건 독립으로 처리하면 $M_1$의 비대각 공분산1을 빠뜨려요. Evidence와 최적 likelihood도 구별하고 prior odds를 잊지 않아요.

#### 설명을 닫고 다시 풀어요

- 각 소문항에서 얻은 식을 다음 소문항의 첫 줄로 옮겨요.
- 모델에서 시작해 최종 공식을 보지 않고 유도해요.
- 독립성·차원·역행렬 조건을 설명하며 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

$C_1=\begin{pmatrix}2&1\\1&2\end{pmatrix}$, $C_2=2I$. $B_{12}\simeq.70036$, posterior odds $\simeq2.10108$, $P(M_1\mid y)\simeq.67753$.

#### 적용 조건

모델별 독립 관계와 prior odds=3

---

<a id="p10"></a>

### 10. 직교투영과 ridge 예측의 차이

EXAM Problem 10 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p10)

#### 주어진 조건

$$
\Phi=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix},\quad y=\begin{pmatrix}1\\2\\0\end{pmatrix},\quad G=\Phi^\top\Phi.
$$

최소제곱 추정량을 $\widehat\theta$라 한다. Ridge에서는 절편 구별 없이 두 계수 모두에 같은 벌점을 준다. 두 예측값은 각각 $\widehat y=\Phi\widehat\theta$, $\widehat y_R=\Phi\theta_R$이다. 내적은 유클리드 내적이다.

#### 구할 것

1. 최소제곱 목적함수 $Q(\theta)=\tfrac12\|y-\Phi\theta\|^2$를 전개·미분해 정규방정식을 도출하라.
2. 소문항 (a)를 풀어 일반적인 추정식을 도출한 뒤 주어진 수치의 $\widehat\theta$, $\widehat y$, $r$를 구하라. 해의 유일성 조건을 확인하라.
3. 소문항 (b)를 예측식에 대입해 $\widehat y=Py$의 $P$를 도출하라. 수치행렬과 대칭성·멱등성을 확인하라.
4. Ridge 목적함수 $\tfrac12\|y-\Phi\theta\|^2+\tfrac12\|\theta\|^2$를 미분하고, (a)와 비교해 정규방정식 및 해 $\theta_R$를 도출·계산하라.
5. 소문항 (d)를 예측식에 대입해 $\widehat y_R=Hy$의 $H$를 도출하라. Ridge의 잔차 조건을 얻고 수치로 확인해, (a)의 잔차 직교성과 비교하라.
6. $v=\Phi(1,1)^\top$에 (e)의 $H,H^2$를 적용하라. (c)와 비교해 대칭만으로 직교투영행렬이라고 할 수 있는지 설명하라.

#### 문제를 내 말로 읽어요

직교투영과 ridge 예측의 차이: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 최소제곱·ridge 해와 두 예측행렬에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“직교투영(orthogonal projection)”은 잔차가 모든 열에 직교한다는 $\Phi^\top r=0$을 떠올리는 단서예요. Full-column-rank일 때 $P=\Phi G^{-1}\Phi^\top$이고 $G=\Phi^\top\Phi$예요. 유클리드 직교투영행렬은 symmetry $P^\top=P$와 idempotence $P^2=P$를 모두 만족해요. Ridge는 정규방정식에 $I$가 추가되어 $\Phi^\top r_R=\theta_R$예요. 대칭만으로는 투영이라고 결론 낼 수 없어요.

출제 근거: MML 3.8 / 9.4 projections; ridge comparison. MML PDF 87, 88, 89, 319, 320쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$Q(\theta)=\tfrac12(y-\Phi\theta)^\top(y-\Phi\theta)$를 전개하고 $\theta$에 대한 열 gradient를 구해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

제곱을 전개하면

$$
Q=\tfrac12 y^\top y-\theta^\top\Phi^\top y+\tfrac12\theta^\top G\theta.
$$

대칭인 $G$를 이용해 미분하면

$$
\nabla Q=G\theta-\Phi^\top y.
$$

0으로 놓아 $G\widehat\theta=\Phi^\top y$를 얻어요. 이는 $\Phi^\top(y-\Phi\widehat\theta)=0$과 같아요.

#### (b)

(a)에서 열독립이면

$$
\widehat\theta=G^{-1}\Phi^\top y.
$$

이 데이터는 $G=\begin{pmatrix}2&1\\1&2\end{pmatrix}$이고 행렬식3으로 가역이에요. $\Phi^\top y=(1,2)^\top$를 곱하면

$$
\widehat\theta=(0,1)^\top,\quad\widehat y=(0,1,1)^\top,\quad r=(1,1,-1)^\top.
$$

$G\succ0$여서 유일한 최소점이에요.

#### (c)

(b)를 $\Phi\widehat\theta$에 넣으면

$$
P=\Phi G^{-1}\Phi^\top=\frac13\begin{pmatrix}2&-1&1\\-1&2&1\\1&1&2\end{pmatrix}.
$$

$G^{-1}$가 대칭이므로 $P^\top=P$예요.

$$
P^2=\Phi G^{-1}G G^{-1}\Phi^\top=P.
$$

따라서 이 행렬은 직교투영이에요.

#### (d)

벌점의 gradient는 $\theta$예요. (a)의 gradient에 더해0으로 놓으면

$$
(G+I)\theta_R=\Phi^\top y.
$$

따라서

$$
\theta_R=(G+I)^{-1}\Phi^\top y=(1/8,5/8)^\top.
$$

$G+I=\begin{pmatrix}3&1\\1&3\end{pmatrix}$의 역행렬을 사용했어요.

#### (e)

(d)를 예측식에 넣으면

$$
H=\Phi(G+I)^{-1}\Phi^\top.
$$

정규방정식을 다시 정리하면

$$
\Phi^\top(y-\Phi\theta_R)=\theta_R.
$$

예측은 $(1/8,5/8,3/4)^\top$, 잔차는 $(7/8,11/8,-3/4)^\top$예요. 열별 내적은 $(1/8,5/8)^\top\ne0$이므로 (a)와 달리 잔차가 열공간에 직교하지 않아요.

#### (f)

$a=(1,1)^\top$이면 $Ga=3a$이고 $v=\Phi a=(1,1,2)^\top$예요. (e)에서

$$
Hv=\Phi(G+I)^{-1}Ga=\tfrac34v,
$$

$$
H^2v=\tfrac9{16}v\ne Hv.
$$

$H$는 대칭이지만 멱등성이 없어 (c)의 직교투영행렬과 달라요. 대칭이라는 사실만으로는 충분하지 않아요.

#### 완성 답과 검산

#### (a) 검산

$\theta=0$에서 gradient는 $-\Phi^\top y$이고 원래 제곱오차의 성분 미분과 같아요.

#### (b) 검산

$\Phi^\top r=0$, $\widehat y+r=y$, SSE는3이에요.

#### (c) 검산

$Py=\widehat y$, $P\Phi=\Phi$로 수치와 기하 의미가 함께 맞아요.

#### (d) 검산

$(G+I)(1/8,5/8)^\top=(1,2)^\top$예요. 양의 벌점으로 Hessian도 양의 정부호예요.

#### (e) 검산

잔차 내적은 $7/8-6/8=1/8$, $11/8-6/8=5/8$이에요. 단순히 열공간에 있는 예측이라는 이유로 최근접점이라고 할 수는 없어요.

#### (f) 검산

$Hv=(3/4,3/4,3/2)^\top$, $H^2v=(9/16,9/16,9/8)^\top$로 실제로 달라요.

#### 여기서 헷갈리기 쉬워요

예측이 열공간에 있다는 사실과 가장 가까운 직교투영이라는 사실은 달라요. 대칭행렬이라고 모두 투영행렬은 아니며 멱등성을 함께 확인해요.

#### 설명을 닫고 다시 풀어요

- 각 소문항에서 얻은 식을 다음 소문항의 첫 줄로 옮겨요.
- 모델에서 시작해 최종 공식을 보지 않고 유도해요.
- 독립성·차원·역행렬 조건을 설명하며 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

ML 잔차는 직교: $\Phi^\top r=0$. Ridge는 $\Phi^\top r_R=\theta_R\ne0$. $Hv=3v/4$, $H^2v=9v/16$이므로 비투영이에요.

#### 적용 조건

G 가역; ridge lambda1; 모든 계수 벌점

---

원 문제·정리노트·PDF는 보존해요.
