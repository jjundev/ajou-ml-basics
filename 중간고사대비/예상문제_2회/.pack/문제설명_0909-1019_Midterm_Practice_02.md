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
  - [6. 평균과 잡음분산을 함께 ML 추정하기](#p6)
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

### 6. 평균과 잡음분산을 함께 ML 추정하기

EXAM Problem 6 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p6)

#### 주어진 조건

$y_n=\theta+\epsilon_n$이며 $\epsilon_n$은 독립 $\mathcal N(0,s)$를 따른다. $\theta\in\mathbb R$와 분산 $s>0$가 모두 미지수이고, 관측 수 $N\ge2$이다.

#### 구할 것

1. 상수항을 포함한 음의 로그우도 $\mathcal L(\theta,s)$를 유도하라. 표본값들이 모두 같지 않을 때 공동 ML 추정 $\widehat\theta,\widehat s$를 구하라.
2. 관측 $y=(1,2,6)^\top$에서 두 추정값을 구하라. 분산을 구할 때 분모를 $N-1$로 바꾼 값과 비교하라.
3. 관측값이 전부 $c$로 같다면 $s>0$인 모수공간에서 공동 ML 추정값이 존재하는가? 우도의 경계 거동을 이용해 설명하라.

#### 문제를 내 말로 읽어요

이번에는 평균뿐 아니라 잡음의 퍼짐도 데이터로 정해요. 분산 $s$가 미지수이므로 Gaussian의 정규화 상수도 최적화에 영향을 줘요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“독립 Gaussian 관측”은 likelihood의 곱과 negative log-likelihood의 합을 떠올리는 단서예요. $\theta$는 평균, $s$는 양의 분산이에요. $N\log s/2$는 $\theta$에 대해서는 상수여도 $s$에 대해서는 상수가 아니에요. ML은 관측된 데이터의 우도를 가장 크게 만드는 선택이며, 불편분산(unbiased variance)의 분모 $N-1$와 목적이 달라요. 경계 $s\to0^+$가 모수공간 안에 포함되는지도 살펴요.

출제 근거: MML 9.2 maximum likelihood; unknown noise variance. MML PDF 298, 299, 300쪽의 개념을 사용한 새 변형·응용 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$$
\mathcal L(\theta,s)=\frac N2\log(2\pi s)+\frac1{2s}\sum_n(y_n-\theta)^2
$$

를 적어요. 미지수에 따라 달라지는 항을 지우지 않아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

우도는 $(2\pi s)^{-N/2}\exp[-\sum_n(y_n-\theta)^2/(2s)]$이므로

$$
\mathcal L=\frac N2\log(2\pi s)+\frac{S(\theta)}{2s}.
$$

고정 $s$에서 $\partial_\theta\mathcal L=N(\theta-\bar y)/s=0$이므로 $\widehat\theta=\bar y$예요. $S=\sum_n(y_n-\bar y)^2>0$이면

$$
\partial_s\mathcal L=\frac{Ns-S}{2s^2},\quad\widehat s=\frac SN.
$$

$s\lt S/N$에서는 감소하고 그보다 크면 증가하므로 유일한 최소예요. 각 $s$에서 최적 평균이 같아 공동 ML도 이 쌍이에요.

#### (b)

평균은 $(1+2+6)/3=3$이에요. 잔차 $(-2,-1,3)^\top$의 제곱합은14이므로

$$
\widehat\theta=3,\quad\widehat s_{\mathrm{ML}}=14/3.
$$

분모 $N-1=2$를 쓰면7이에요. 7은 이 모형의 분산 ML 값이 아니에요.

#### (c)

모든 관측이 $c$이면 $\theta=c$에서 잔차가0이에요. 이때

$$
p(y\mid c,s)=(2\pi s)^{-N/2}\to\infty\quad(s\to0^+).
$$

양의 $s$마다 더 작은 분산이 더 큰 우도를 주므로 $s>0$인 공간에는 최대점이 없어요. $\widehat s=0$을 허용된 Gaussian 분산이라고 쓰면 안 돼요.

#### 완성 답과 검산

#### (a) 검산

$S(\theta)=S(\bar y)+N(\theta-\bar y)^2$이므로 평균 선택의 전역성이 확인돼요. $S>0$일 때 $s\to0^+$와 $s\to\infty$ 모두 NLL이 커지고 중간의 $S/N$에서 최소예요.

#### (b) 검산

$(1-3)^2+(2-3)^2+(6-3)^2=4+1+9=14$예요. 미분식의 분자 $N\widehat s-S=3(14/3)-14=0$도 확인해요.

#### (c) 검산

$s$를 절반으로 줄이면 잔차0의 우도는 $2^{N/2}$배 커져요. 어떤 양의 분산도 최대값을 줄 수 없다는 직접 비교예요.

#### 여기서 헷갈리기 쉬워요

$\log s$를 상수로 지우면 분산 추정이 틀려요. 또한 경계의0은 문제에서 허용한 $s>0$에 속하지 않아요. ML 분산과 불편분산을 구별해요.

#### 설명을 닫고 다시 풀어요

- 조건에서 필요한 개념과 가정을 직접 적어요.
- 첫 식부터 각 소문항의 답까지 이어 써요.
- 검산으로 결과와 차원을 다시 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\widehat\theta=\bar y$, $\widehat s=N^{-1}\sum(y_n-\bar y)^2$는 SSE&gt;0일 때. SSE0이면 양의 분산 ML 부재예요.

#### 적용 조건

미지 s&gt;0; N&gt;=2; 잔차0 경계 별도

---

<a id="p7"></a>

### 7. 서로 다른 prior 분산과 MAP

EXAM Problem 7 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_02.html#p7)

#### 주어진 조건

$\Phi=\begin{pmatrix}1&-1\\1&1\end{pmatrix}$, $y=(0,4)^\top$에 대해 $y\mid\theta\sim\mathcal N(\Phi\theta,\sigma^2I_2)$이다. Prior는 $\theta\sim\mathcal N(m_0,S_0)$이며 $m_0=(2,0)^\top$, $S_0=\operatorname{diag}(4,1)$이다. $\sigma^2>0$는 알려져 있고 prior는 두 계수에 모두 적용된다.

#### 구할 것

1. $\theta$와 무관한 상수를 뺀 음의 로그 posterior와 MAP 정규방정식을 $\sigma^2$를 남겨 유도하라.
2. $\sigma^2=1$에서 $\theta_{\mathrm{MAP}}$과 $x_*=2$, $\phi(x_*)=(1,2)^\top$에서의 평균 예측을 구하라. ML과 비교하라.
3. 왜 해가 유일한지 증명하라. $\sigma^2\to0^+$와 $\sigma^2\to\infty$에서 MAP가 각각 무엇으로 수렴하는지 구하라.

#### 문제를 내 말로 읽어요

절편 prior의 중심은2이고 기울기 prior의 중심은0이에요. 두 prior 분산도 달라서 각 계수에 작용하는 벌점이 달라요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“서로 다른 prior 분산”이 보이면 scalar ridge 계수 하나보다 precision matrix $S_0^{-1}$를 떠올려요. 큰 prior 분산은 더 약한 벌점을 뜻해요. 일반 Gaussian prior에서 NLL에 $\frac12(\theta-m_0)^\top S_0^{-1}(\theta-m_0)$를 더해요. MAP는 이 quadratic objective의 최소점이에요. 양의 정부호 precision은 역행렬과 해의 유일성을 보장해요.

출제 근거: MML 9.2.3 Gaussian MAP with diagonal prior. MML PDF 307, 308, 309쪽의 개념을 사용한 새 변형·응용 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$S_0^{-1}=\operatorname{diag}(1/4,1)$, $G=2I_2$, $\Phi^\top y=(4,4)^\top$를 먼저 써요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

상수 $C$를 제외하면

$$
-\log p(\theta\mid y)=\frac{\|y-\Phi\theta\|^2}{2\sigma^2}+\frac12(\theta-m_0)^\top S_0^{-1}(\theta-m_0)+C.
$$

열 gradient를0으로 놓으면

$$
\left(\frac G{\sigma^2}+S_0^{-1}\right)\theta=\frac{\Phi^\top y}{\sigma^2}+S_0^{-1}m_0.
$$

양변에 $\sigma^2$를 곱하면 $(G+\sigma^2S_0^{-1})\theta=\Phi^\top y+\sigma^2S_0^{-1}m_0$예요.

#### (b)

$\sigma^2=1$에서

$$
\begin{pmatrix}9/4&0\\0&3\end{pmatrix}\theta=\begin{pmatrix}9/2\\4\end{pmatrix}
$$

이므로 $\theta_{\mathrm{MAP}}=(2,4/3)^\top$예요. $x_*=2$에서 평균은 $2+2(4/3)=14/3$예요. ML은 $2I\theta=(4,4)^\top$에서 $(2,2)^\top$, 평균 예측6이에요. 절편은 데이터의 ML 값과 prior 중심이 같아 그대로이고, 기울기는0 쪽으로 줄어요.

#### (c)

비영 $a$에 대해 Hessian $B=G/\sigma^2+S_0^{-1}$는

$$
a^\top Ba=\frac{\|\Phi a\|^2}{\sigma^2}+a^\top S_0^{-1}a>0
$$

이므로 유일한 최소점이 있어요. 구체적으로 정규방정식에서

$$
\theta_0=2,\quad\theta_1=\frac4{2+\sigma^2}.
$$

따라서 $\sigma^2\to0^+$이면 $(2,2)^\top=\theta_{\mathrm{ML}}$, $\sigma^2\to\infty$이면 $(2,0)^\top=m_0$로 가요.

#### 완성 답과 검산

#### (a) 검산

Prior 항을 성분으로 풀면 $(\theta_0-2)^2/8+\theta_1^2/2$예요. 분산4인 절편에 분산1인 기울기보다 작은 precision이 적용돼요.

#### (b) 검산

학습 MAP 예측은 $(2/3,10/3)^\top$, 잔차는 $(-2/3,2/3)^\top$예요. $\Phi^\top r=(0,4/3)^\top=S_0^{-1}(\theta-m_0)$여서 stationarity를 만족해요.

#### (c) 검산

일반 $\sigma^2$ 식에1을 대입하면 기울기는 $4/3$이에요. 극한에서 기울기는2와0으로, 절편은 계속2로 유지돼요.

#### 여기서 헷갈리기 쉬워요

Prior 분산4를 벌점4로 쓰면 반대로 계산한 거예요. 벌점은 역분산1/4이고, 중심이0이 아닌 prior에서는 우변의 $S_0^{-1}m_0$도 남겨야 해요.

#### 설명을 닫고 다시 풀어요

- 조건에서 필요한 개념과 가정을 직접 적어요.
- 첫 식부터 각 소문항의 답까지 이어 써요.
- 검산으로 결과와 차원을 다시 확인해요.

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

1. 완전제곱 또는 Gaussian posterior 공식으로 $p(\theta\mid y)$의 평균과 공분산을 구하라.
2. $x_*=1$에서 $f_*$와 $y_*$의 사후예측분포를 각각 구하라. MAP를 대입한 관측 예측분포와 비교하라.
3. 같은 posterior로 예측하는 두 미래 관측 $y_*^{(0)}$와 $y_*^{(1)}$은 각각 $x=0,1$에 대응한다. 이 둘의 $y$를 조건으로 한 공분산을 구하라. $\theta$까지 주면 독립인데도 $y$만 주었을 때 독립인지 설명하라.

#### 문제를 내 말로 읽어요

훈련 뒤에도 모수는 한 점으로 확정되지 않고 분포를 가져요. 두 미래 관측은 같은 불확실한 모수를 함께 사용하므로 관계가 생길 수 있어요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“Gaussian prior와 선형 Gaussian likelihood”는 Gaussian posterior의 precision 합을 떠올리는 단서예요. $S_N=(S_0^{-1}+\Phi^\top\Phi/\sigma^2)^{-1}$, $m_N=S_N(S_0^{-1}m_0+\Phi^\top y/\sigma^2)$예요. $f_*=\phi_*^\top\theta$의 분산은 $\phi_*^\top S_N\phi_*$이며 관측 $y_*$에는 독립 잡음분산을 더해요. 서로 다른 미래 관측의 공분산에서는 독립 잡음의 교차항은0이고 공유 모수의 항 $\phi_a^\top S_N\phi_b$만 남아요.

출제 근거: MML 9.3.3-9.3.4 posterior predictive; affine covariance. MML PDF 198, 312, 314, 315쪽의 개념을 사용한 새 변형·응용 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$\Phi^\top\Phi=2I_2$, $\Phi^\top y=(2,2)^\top$, $S_0=I_2$, $\sigma^2=2$를 공식에 넣어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

Posterior precision은 $I_2+\frac12(2I_2)=2I_2$예요. 따라서

$$
S_N=\tfrac12I_2,\quad m_N=\tfrac12I_2\cdot\tfrac12(2,2)^\top=(1/2,1/2)^\top.
$$

즉 $p(\theta\mid y)=\mathcal N((1/2,1/2)^\top,\frac12I_2)$예요.

#### (b)

$x_*=1$이면 $\phi_*=(1,1)^\top$예요. 평균은1, 잠재 분산은 $(1,1)(\frac12I)(1,1)^\top=1$이에요. 따라서

$$
f_*\mid y\sim\mathcal N(1,1),\quad y_*\mid y\sim\mathcal N(1,3).
$$

Posterior 최빈값 $\theta_{\mathrm{MAP}}=m_N$만 대입하면 관측 예측은 $\mathcal N(1,2)$예요. 평균은 같고 모수 불확실성1을 빠뜨려 분산이 작아요.

#### (c)

$\phi_0=(1,0)^\top$, $\phi_1=(1,1)^\top$이므로

$$
\operatorname{Cov}(y_*^{(0)},y_*^{(1)}\mid y)=\phi_0^\top S_N\phi_1=1/2.
$$

미래 잡음끼리의 공분산과 모수·잡음 교차 공분산은0이에요. $\theta$를 주면 서로 독립이지만 $y$만 주면 공통 $\theta$가 여전히 불확실하여 주변적으로 독립이 아니에요. 공분산이0이 아니라는 점만으로도 비독립을 알 수 있어요.

#### 완성 답과 검산

#### (a) 검산

Posterior 평균은 $(G/2+I)m_N=(1,1)^\top=\Phi^\top y/2$를 만족해요. $2I\cdot\frac12I=I$여서 공분산과 precision도 역행렬 관계예요.

#### (b) 검산

$f_*=\theta_0+\theta_1$에서 두 posterior 계수의 분산은 각각1/2이고 공분산0이에요. 합의 분산1에 잡음2를 더하면3이에요.

#### (c) 검산

두 미래 관측의 공동 공분산은 $\begin{pmatrix}5/2&1/2\\1/2&3\end{pmatrix}$예요. 직접 성분으로 쓰면 공통 $\theta_0$의 posterior 분산1/2이 교차 공분산에 남아요.

#### 여기서 헷갈리기 쉬워요

“잡음 독립”을 “모수를 적분한 관측도 독립”으로 바꾸면 안 돼요. 또한 $f_*$와 $y_*$ 중 어떤 것을 예측하는지 구별해야 잡음분산을 빠뜨리거나 두 번 더하지 않아요.

#### 설명을 닫고 다시 풀어요

- 조건에서 필요한 개념과 가정을 직접 적어요.
- 첫 식부터 각 소문항의 답까지 이어 써요.
- 검산으로 결과와 차원을 다시 확인해요.

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

1. 모수를 prior로 적분한 $p(y\mid M_i)$의 평균벡터와 공분산행렬을 각각 구하라.
2. 주어진 관측에서 두 evidence를 정규화 상수까지 계산하고 Bayes factor $B_{12}$를 구하라. 데이터만으로 어느 모델을 지지하는가?
3. posterior odds와 $P(M_1\mid y)$를 구해 사후확률이 큰 모델을 선택하라. (b)의 결론과 달라지는 이유를 설명하라.

#### 문제를 내 말로 읽어요

같은 잠재 평균을 두 번 쓰는 모형과 각 관측에 다른 잠재 평균을 쓰는 모형을 비교해요. 관측은1과 -1로 서로 반대 방향이에요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“모수를 적분한 evidence”에서는 한 번 최적화한 likelihood 대신 prior 아래의 관측분포를 구해요. 선형 Gaussian $y=B\theta+\epsilon$의 주변 공분산은 $BS_0B^\top+I$예요. 공통 모수는 관측 사이에 공분산을 만들어요. 다변량 Gaussian 밀도에는 $\det C$와 $y^\top C^{-1}y$가 모두 필요해요. Bayes factor는 evidence의 비이고 posterior odds는 여기에 모델 prior odds를 곱한 값이에요.

출제 근거: MML 9.3.5 evidence; shared versus separate parameters. MML PDF 205, 206, 312, 317, 318, 319쪽의 개념을 사용한 새 변형·응용 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$M_1$에서 $B=(1,1)^\top$, $M_2$에서 $B=I_2$라고 적어요. 각각 독립 잡음의 공분산 $I_2$를 더해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

두 모델 모두 주변 평균은0이에요. $M_1$은 공통 $\theta$를 더하므로

$$
C_1=\begin{pmatrix}1\\1\end{pmatrix}(1,1)+I_2=\begin{pmatrix}2&1\\1&2\end{pmatrix}.
$$

$M_2$는 모수도 독립이므로 $C_2=2I_2$예요. 따라서 $p(y\mid M_i)=\mathcal N(y\mid0,C_i)$예요.

#### (b)

$\det C_1=3$, $C_1^{-1}=\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$이며 관측 $y=(1,-1)^\top$에서 $y^\top C_1^{-1}y=2$예요. $C_2$에서는 행렬식4, 이차형식1이에요. 따라서

$$
p(y\mid M_1)=\frac{e^{-1}}{2\pi\sqrt3},\quad p(y\mid M_2)=\frac{e^{-1/2}}{4\pi}.
$$

$$
B_{12}=\frac2{\sqrt3}e^{-1/2}\simeq0.70036<1.
$$

데이터만으로는 $M_2$를 지지해요.

#### (c)

Prior odds를 곱하면

$$
O_{12}^{\mathrm{post}}=3B_{12}=2\sqrt3e^{-1/2}\simeq2.10108>1.
$$

두 모델의 사후확률 합이1이므로

$$
P(M_1\mid y)=\frac{3B_{12}}{1+3B_{12}}\simeq0.67753.
$$

따라서 사후확률이 큰 모델은 $M_1$이에요. 데이터가 $M_2$ 쪽으로 odds를 낮추었지만 처음의3:1 선호를 뒤집을 만큼 강하지는 않았어요.

#### 완성 답과 검산

#### (a) 검산

$M_1$에서 $\operatorname{Cov}(y_1,y_2)=\operatorname{Var}(\theta)=1$이고 $M_2$에서는0이에요. 대각성분은 둘 다 모수분산1+잡음분산1=2예요.

#### (b) 검산

$C_1(1,-1)^\top=(1,-1)^\top$이므로 역행렬도 이 방향에는 계수1을 적용해요. 따라서 이차형식은 $\|y\|^2=2$예요. $C_2^{-1}=I/2$에서는1이에요.

#### (c) 검산

Prior odds3는 prior 확률 $3/4,1/4$와 같아요. $\frac{(3/4)p_1}{(3/4)p_1+(1/4)p_2}=\frac{3B}{1+3B}$로 직접 정규화해도 같은 값이에요.

#### 여기서 헷갈리기 쉬워요

공통 모수를 적분하기 전에 관측 두 개를 무조건 독립으로 처리하면 $M_1$의 비대각 공분산1을 빠뜨려요. Evidence와 최적 likelihood도 구별하고 prior odds를 잊지 않아요.

#### 설명을 닫고 다시 풀어요

- 조건에서 필요한 개념과 가정을 직접 적어요.
- 첫 식부터 각 소문항의 답까지 이어 써요.
- 검산으로 결과와 차원을 다시 확인해요.

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

최소제곱 추정을 $\widehat\theta$라 하고 $P=\Phi G^{-1}\Phi^\top$로 둔다. Ridge에서는 절편 구별 없이 두 계수에 같은 벌점을 주어 $\frac12\|y-\Phi\theta\|^2+\frac12\|\theta\|^2$를 최소화한다. 그 해를 $\theta_R$, 예측행렬을 $H=\Phi(G+I_2)^{-1}\Phi^\top$라 한다.

#### 구할 것

1. 직교 잔차 조건으로 정규방정식을 유도하고 $\widehat\theta$, $\widehat y$, $r=y-\widehat y$를 구하라.
2. $P$를 수치로 구하고 $P^\top=P$, $P^2=P$를 확인하라.
3. $\theta_R$와 $\Phi^\top(y-\Phi\theta_R)$를 구하라. Ridge 잔차도 열공간에 직교하는가?
4. $v=\Phi(1,1)^\top$에 $H$와 $H^2$를 적용해 비교하라. $H$가 대칭이라는 사실만으로 직교투영행렬인지 판단할 수 있는가?

#### 문제를 내 말로 읽어요

최소제곱의 예측은 열공간의 가장 가까운 점이에요. Ridge도 같은 열공간 안에 예측을 만들지만, 계수를 줄이는 벌점 때문에 같은 점에 도착하는지는 다시 확인해야 해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“직교투영(orthogonal projection)”은 잔차가 모든 열에 직교한다는 $\Phi^\top r=0$을 떠올리는 단서예요. Full-column-rank일 때 $P=\Phi G^{-1}\Phi^\top$이고 $G=\Phi^\top\Phi$예요. 유클리드 직교투영행렬은 symmetry $P^\top=P$와 idempotence $P^2=P$를 모두 만족해요. Ridge는 정규방정식에 $I$가 추가되어 $\Phi^\top r_R=\theta_R$예요. 대칭만으로는 투영이라고 결론 낼 수 없어요.

출제 근거: MML 3.8 / 9.4 projections; ridge comparison. MML PDF 87, 88, 89, 319, 320쪽의 개념을 사용한 새 변형·응용 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$G=\begin{pmatrix}2&1\\1&2\end{pmatrix}$, $\Phi^\top y=(1,2)^\top$부터 써요. 정규방정식의 오른쪽은2차원이고 예측은3차원이에요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

열벡터 각각에 대해 잔차 내적0을 모으면 $\Phi^\top(y-\Phi\widehat\theta)=0$이에요. 즉 $G\widehat\theta=\Phi^\top y$예요. $G^{-1}=\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$를 곱하면

$$
\widehat\theta=(0,1)^\top,\quad\widehat y=(0,1,1)^\top,\quad r=(1,1,-1)^\top.
$$

#### (b)

행렬을 곱하면

$$
P=\frac13\begin{pmatrix}2&-1&1\\-1&2&1\\1&1&2\end{pmatrix}.
$$

대칭은 원소에서 확인돼요. $G$가 대칭이고 가역이므로

$$
P^2=\Phi G^{-1}(\Phi^\top\Phi)G^{-1}\Phi^\top=P.
$$

즉 같은 점을 두 번 투영해도 달라지지 않아요.

#### (c)

Ridge의 gradient0에서 $(G+I)\theta_R=\Phi^\top y$예요. 따라서

$$
\theta_R=\tfrac18\begin{pmatrix}3&-1\\-1&3\end{pmatrix}\begin{pmatrix}1\\2\end{pmatrix}=(1/8,5/8)^\top.
$$

예측은 $(1/8,5/8,3/4)^\top$, 잔차는 $(7/8,11/8,-3/4)^\top$이에요.

$$
\Phi^\top r_R=(1/8,5/8)^\top=\theta_R\ne0.
$$

따라서 이 ridge 잔차는 열공간에 직교하지 않아요.

#### (d)

$a=(1,1)^\top$이면 $Ga=3a$, $(G+I)a=4a$이고 $v=\Phi a=(1,1,2)^\top\ne0$이에요.

$$
Hv=\Phi(G+I)^{-1}Ga=\tfrac34v,
$$

$$
H^2v=\tfrac9{16}v\ne Hv.
$$

$H$는 대칭이지만 멱등성이 없으므로 직교투영행렬이 아니에요. 열공간의 벡터도 한 번 더 줄여버려요.

#### 완성 답과 검산

#### (a) 검산

$\Phi^\top r=(1-1,1-1)^\top=0$이고 $\widehat y+r=y$예요. 최소 잔차제곱은3이에요.

#### (b) 검산

$P\Phi=\Phi$, $Py=(0,1,1)^\top$예요. 정수행렬 $M=3P$를 직접 곱하면 $M^2=3M$도 확인돼요.

#### (c) 검산

$(G+I)(1/8,5/8)^\top=(1,2)^\top$예요. 잔차의 열별 내적은 $7/8-6/8=1/8$, $11/8-6/8=5/8$로 구한 계수와 같아요.

#### (d) 검산

$Hv=(3/4,3/4,3/2)^\top$, $H^2v=(9/16,9/16,9/8)^\top$로 명시하면 두 결과가 다름을 바로 볼 수 있어요.

#### 여기서 헷갈리기 쉬워요

예측이 열공간에 있다는 사실과 가장 가까운 직교투영이라는 사실은 달라요. 대칭행렬이라고 모두 투영행렬은 아니며 멱등성을 함께 확인해요.

#### 설명을 닫고 다시 풀어요

- 조건에서 필요한 개념과 가정을 직접 적어요.
- 첫 식부터 각 소문항의 답까지 이어 써요.
- 검산으로 결과와 차원을 다시 확인해요.

**페이지 요약**

#### 떠올릴 개념·공식

ML 잔차는 직교: $\Phi^\top r=0$. Ridge는 $\Phi^\top r_R=\theta_R\ne0$. $Hv=3v/4$, $H^2v=9v/16$이므로 비투영이에요.

#### 적용 조건

G 가역; ridge lambda1; 모든 계수 벌점

---

원 문제·정리노트·PDF는 보존해요.
