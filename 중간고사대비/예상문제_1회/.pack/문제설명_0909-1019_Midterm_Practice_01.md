# 머신러닝기초 중간고사 모의평가 1회 문제설명

주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.

문제의 첫 줄부터 검산까지 설명해요.

**목차**

- [문항별 설명](#problems)
  - [1. 선형결합과 해의 유일성](#p1)
  - [2. Gradient·Jacobian·이차함수](#p2)
  - [3. 가우시안 곱과 정규화](#p3)
  - [4. 특징행렬로 계산하는 ML과 MAP](#p4)
  - [5. 표본 공분산과 아핀 변환](#p5)
  - [6. 확률모델에서 경험위험 최소화까지](#p6)
  - [7. Gaussian prior가 만드는 ridge](#p7)
  - [8. 사후분포와 새 관측의 예측](#p8)
  - [9. Evidence·Bayes factor·모델 선택](#p9)
  - [10. 최소제곱 해를 직교투영으로 읽기](#p10)

<a id="problems"></a>

## 문항별 설명

<a id="p1"></a>

### 1. 선형결합과 해의 유일성

EXAM Problem 1 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p1)

#### 주어진 조건

열벡터 $v_1=(1,0,1)^\top$, $v_2=(0,1,1)^\top$, $v_3=(1,1,2)^\top$를 두고 $V=[v_1\ v_2\ v_3]$, $U=[v_1\ v_2]$라 하자.

#### 구할 것

1. $v_1,v_2,v_3$의 선형독립 여부를 0이 아닌 계수의 선형관계로 판정하라.
2. $b=(2,1,3)^\top$에 대해 $V\alpha=b$의 모든 해를 구하라. $c=(2,1,4)^\top$로 우변을 바꾸면 해가 있는가?
3. $U^\top U$와 그 역행렬을 구하라. $V^\top V$의 역행렬 존재 여부와 비교하라.

#### 문제를 내 말로 읽어요

세 벡터로 만들 수 있는 방향을 읽는 문제예요. 벡터가 세 개라는 사실만으로 3차원 전체를 만들 수 있는 것은 아니에요. 같은 방향을 중복해서 넣었는지 먼저 확인해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“선형독립”을 보면 $V\alpha=0$의 해를 떠올려요. 영벡터를 만드는 계수가 $\alpha=0$뿐이어야 독립이에요. “모든 해”를 구할 때는 자유변수를 남겨야 해요. Gram 행렬 $U^\top U$는 열벡터 사이의 내적을 모은 행렬이에요. $z^\top U^\top Uz=\|Uz\|^2$이므로 열독립일 때에만 가역이에요.

#### 종이에 쓸 첫 줄

$v_3=v_1+v_2$인지 성분별로 써 봐요. 이어서 $V\alpha=(\alpha_1+\alpha_3,\alpha_2+\alpha_3,\alpha_1+\alpha_2+2\alpha_3)^\top$로 적어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

먼저 $V=[v_1\ v_2\ v_3]$는 세 열벡터를 옆으로 놓은 $3\times3$ 행렬이에요. 계수 $\alpha=(\alpha_1,\alpha_2,\alpha_3)^\top$를 곱한다는 것은 $V\alpha=\alpha_1v_1+\alpha_2v_2+\alpha_3v_3$라는 선형결합을 만든다는 뜻이에요. 아래첨자 1, 2, 3은 여기서는 벡터의 번호예요.

선형독립인지 묻기 때문에, 모두 0은 아닌 계수로 영벡터를 만들 수 있는지 찾아요. 실제로 더하면

$$
v_1+v_2=\begin{pmatrix}1+0\\0+1\\1+1\end{pmatrix}=\begin{pmatrix}1\\1\\2\end{pmatrix}=v_3.
$$

따라서 $v_1+v_2-v_3=(1-1,1-1,2-2)^\top=0$이에요. 결과 벡터는 0이지만 사용한 계수 $(1,1,-1)^\top$는 0이 아니므로 세 벡터는 선형종속이에요. 한편 $av_1+bv_2=(a,b,a+b)^\top=0$이면 첫 두 성분에서 $a=b=0$이에요. 앞의 두 열은 독립이므로 열공간의 차원은 2예요.

#### (b)

이번에는 영벡터가 아니라 주어진 $b=(2,1,3)^\top$를 만드는 계수를 모두 찾아요. 행렬 곱의 각 행을 읽으면

$$
\alpha_1+\alpha_3=2,\qquad\alpha_2+\alpha_3=1,
$$

$$
\alpha_1+\alpha_2+2\alpha_3=3.
$$

셋째 식은 첫째 식과 둘째 식을 더한 것이라 독립된 제약이 아니에요. $\alpha_3=t$를 아무 실수로 정하면 $\alpha_1=2-t$, $\alpha_2=1-t$이므로 모든 해는 $\alpha=(2-t,1-t,t)^\top$예요. 자유변수는 해를 빼먹지 않고 표현하는 장치예요. 실제로 셋째 성분은 $(2-t)+(1-t)+2t=3$으로 항상 맞아요.

이와 달리 $c=(2,1,4)^\top$를 넣으면 첫 두 식의 합은 3인데 셋째 식은 4를 요구해요. 모든 열과 그 선형결합은 $z_3=z_1+z_2$라는 평면 안에 있고, $b$는 그 평면 위, $c$는 밖에 있어요. 따라서 $b$에는 무수히 많은 해가 있고 $c$에는 해가 없어요.

#### (c)

Gram 행렬은 열벡터 사이의 내적을 모은 행렬이에요.

$$
U^\top U=\begin{pmatrix}v_1^\top v_1&v_1^\top v_2\\v_2^\top v_1&v_2^\top v_2\end{pmatrix}=\begin{pmatrix}2&1\\1&2\end{pmatrix}.
$$

행렬식이 $2\cdot2-1\cdot1=3$이므로 $2\times2$ 역행렬 공식을 적용하면

$$
(U^\top U)^{-1}=\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}.
$$

반면 (a)에서 $V$의 열이 선형종속이므로 $V^\top V$는 특이행렬이고 역행렬이 없어요.

#### 완성 답과 검산

#### (a) 검산

계수 $1,1,-1$을 원래 세 벡터에 직접 곱하면 세 성분 모두 0이에요. 독립이라고 결론 내릴 수 없어요.

#### (b) 검산

일반해를 대입하면 첫째 성분 $2-t+t=2$, 둘째 $1-t+t=1$, 셋째 $3$이에요. $t=0$과 $t=1$도 서로 다른 해예요. $c$는 공간을 정의하는 관계 $z_3=z_1+z_2$를 위반해요.

#### (c) 검산

$\frac13\begin{pmatrix}2&1\\1&2\end{pmatrix}\begin{pmatrix}2&-1\\-1&2\end{pmatrix}=I_2$예요. $V$의 영공간에 0이 아닌 벡터가 있으므로 Gram 행렬도 역행렬을 가질 수 없어요.

#### 여기서 헷갈리기 쉬워요

열이 많다고 해가 유일한 것은 아니에요. 또 $V\alpha=b$가 해를 여러 개 갖는 것과, 다른 우변 $c$에는 해가 없는 것은 모순이 아니에요. 우변이 열공간에 들어오는지부터 나누어 판단해요.

#### 설명을 닫고 다시 풀어요

- 비영 계수로 영벡터를 만드는 식을 성분별로 써요.
- 일반해의 자유변수를 바꾸어 두 해를 만들고 c가 열공간 밖인 이유를 말해요.
- 두 Gram 행렬의 역행렬 존재 여부를 열독립과 연결해 설명해요.

**페이지 요약**

#### 떠올릴 개념·공식

독립: $V\alpha=0\Rightarrow\alpha=0$. Gram: $U^\top U$ 가역 $\Leftrightarrow$ 열독립. 일반해 $(2-t,1-t,t)^\top$.

#### 적용 조건

선형독립을 가정하지 않고 직접 판정; 모든 벡터는 열벡터

#### 출제 근거

출제 근거: 과제1 P6-P8 변형. MML PDF 46, 47쪽의 이론을 대조했어요. 과제의 수치·조건을 바꾼 변형 문제예요. 교수님의 세부 출제 확정 내용은 아니에요.

#### 해설에 쓰인 용어

- **선형결합 (linear combination)** — 벡터 각각에 실수 계수를 곱한 뒤 더해서 만든 벡터예요.$v=\sum_i\alpha_i v_i$에서 $\alpha_i$가 계수예요.이 문제에서는 열벡터가 만드는 벡터를 계수로 표현할 때 써요.
- **선형독립 (linear independence)** — 영벡터를 만드는 선형결합의 계수가 모두 0일 때 그 벡터들은 선형독립이에요.$V\alpha=0\Rightarrow\alpha=0$인지 확인해요.이 문제에서는 벡터 개수가 아니라 계수 방정식으로 독립 여부를 판정해요.
- **선형종속 (linear dependence)** — 모두 0은 아닌 계수로도 영벡터를 만들 수 있는 상태예요.$V\alpha=0$을 만족하는 $\alpha\ne0$가 존재해요.이 문제에서는 0이 아닌 계수 관계를 찾는 이유를 설명해요.
- **자유변수 (free variable)** — 연립방정식의 다른 조건을 만족시키면서 임의의 값으로 정할 수 있는 미지수예요.예를 들어 자유변수를 $t\in\mathbb R$로 두면 나머지 미지수를 $t$의 식으로 표현해요.이 문제에서는 모든 해를 한 가족으로 나타낼 때 써요.
- **Gram 행렬 (Gram matrix)** — 열벡터 사이의 모든 내적을 모은 행렬이에요.$G=U^\top U$이며 $G_{ij}=u_i^\top u_j$예요. 실수 행렬 $U$의 열이 독립이면 $G$는 가역이에요.이 문제에서는 열벡터의 독립성과 역행렬 존재를 연결해요.
- **가역·특이행렬 (invertible·singular matrix)** — 정사각행렬에 역행렬이 있으면 가역, 없으면 특이행렬이라고 해요.$A^{-1}A=AA^{-1}=I$가 역행렬의 조건이에요. $Az=0$에 $z\ne0$인 해가 있으면 $A$는 특이해요.이 문제에서는 두 Gram 행렬의 역행렬 존재 여부를 구분해요.

---

<a id="p2"></a>

### 2. Gradient·Jacobian·이차함수

EXAM Problem 2 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p2)

#### 주어진 조건

$x=(x_1,x_2)^\top$에 대해 다음을 정의한다. Gradient는 행벡터이고 Jacobian은 $(J_f)_{ij}=\partial f_i/\partial x_j$이다.

$$
f(x)=\begin{pmatrix}x_1^2+x_2\\x_1x_2\end{pmatrix},\quad A=\begin{pmatrix}4&1\\1&2\end{pmatrix},\quad b=\begin{pmatrix}1\\0\end{pmatrix}
$$

$$
q(x)=\tfrac12 x^\top Ax-b^\top x.
$$

#### 구할 것

1. $J_f(x)$와 $J_f(1,2)$를 구하고 차원을 써라.
2. $q(x)$를 성분으로 전개하고 $\nabla q(x)$와 Hessian을 구하라.
3. 정지점 $\nabla q(x)=0$을 구하고, 유일한 전역 최소점인지 이유를 밝혀라.

#### 문제를 내 말로 읽어요

벡터 출력 $f$에는 Jacobian, 스칼라 출력 $q$에는 gradient를 써요. 이 자료에서 $\nabla_x q=\partial q/\partial x$는 강의의 행벡터 표기예요. 예를 들어 $\partial\|x\|^2/\partial x=2x^\top$예요. 행렬 모양을 먼저 정하면 미분한 값을 어디에 놓을지 헷갈리지 않아요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

Jacobian은 출력 하나마다 한 행, 입력 하나마다 한 열이에요. 여기서는 $2\times2$예요. Gradient는 강의와 같이 $1\times2$ 행벡터로 모아요. 입력 $x$ 자체는 $2\times1$ 열벡터예요. Hessian은 모든 2차 편미분을 모은 행렬이에요. 대칭 $A$에 대해 $\nabla(\frac12x^\top Ax)=x^\top A$이고 Hessian은 $A$예요. 대칭 $2\times2$ 행렬은 첫 선도 주행렬식과 전체 행렬식이 양수이면 양의 정부호예요.

#### 종이에 쓸 첫 줄

$q=2x_1^2+x_1x_2+x_2^2-x_1$로 먼저 전개해요. 이 한 줄에서 교차항과 $1/2$가 제대로 반영됐는지 확인할 수 있어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

이 문제의 $x=(x_1,x_2)^\top$는 하나의 입력 벡터이고, $x_1,x_2$는 그 벡터의 두 성분이에요. $f(x)=(f_1(x),f_2(x))^\top$도 벡터지만 각각 $f_1=x_1^2+x_2$, $f_2=x_1x_2$라는 스칼라 함수로 나누어 미분해요.

편미분에서는 미분하지 않는 성분을 상수로 취급해요. 네 자리를 하나씩 계산하면

$$
\frac{\partial f_1}{\partial x_1}=2x_1,\qquad\frac{\partial f_1}{\partial x_2}=1,
$$

$$
\frac{\partial f_2}{\partial x_1}=x_2,\qquad\frac{\partial f_2}{\partial x_2}=x_1.
$$

Jacobian은 출력 번호가 행, 입력 성분 번호가 열인 약속이에요. 따라서 두 출력의 미분을 각각 한 행에 놓아요.

$$
J_f(x)=\begin{pmatrix}2x_1&1\\x_2&x_1\end{pmatrix}.
$$

점 $(1,2)$에서 평가한다는 말은 이 식에 $x_1=1,x_2=2$를 넣으라는 뜻이에요. 그래서 $J_f(1,2)=\begin{pmatrix}2&1\\2&1\end{pmatrix}$예요. 입력의 작은 변화 $\Delta x$에 대해 $\Delta f\approx J_f\Delta x$가 $2\times1$로 나오는지도 확인해요.

#### (b)

$q$는 벡터를 받아 스칼라 하나를 내는 함수예요. $x^\top Ax$의 크기는 $(1\times2)(2\times2)(2\times1)=1\times1$이에요. 공식만 외우기 전에 곱을 전개해요.

$$
Ax=\begin{pmatrix}4x_1+x_2\\x_1+2x_2\end{pmatrix},
$$

$$
x^\top Ax=x_1(4x_1+x_2)+x_2(x_1+2x_2).
$$

교차항 $x_1x_2$가 두 번 나와요. $b^\top x=x_1$이고 앞의 $1/2$를 곱하면 $q=2x_1^2+x_1x_2+x_2^2-x_1$이에요. 이를 각 성분에 대해 미분한 값을 가로로 모으면

$$
\nabla q=\begin{pmatrix}4x_1+x_2-1&x_1+2x_2\end{pmatrix}=x^\top A-b^\top.
$$

Hessian은 $(H_q)_{ij}=\partial^2q/(\partial x_i\partial x_j)$로 정의해요. 행 gradient의 $i$번째 성분을 $x_j$로 미분해 $i$행 $j$열에 놓아요. 첫째 미분식을 $x_1,x_2$로 다시 미분하면 $(4,1)$, 둘째 식을 미분하면 $(1,2)$예요. 따라서 Hessian은 $H_q=\begin{pmatrix}4&1\\1&2\end{pmatrix}=A$예요. 이 문제의 $A$가 대칭이라 $\nabla(\frac12x^\top Ax)=x^\top A$가 성립해요.

#### (c)

(b)의 행 gradient를 0으로 놓고 양변 전치하면 $Ax=b$예요.

$$
4x_1+x_2=1,\qquad x_1+2x_2=0\quad\Rightarrow\quad x_*=(2/7,-1/7)^\top.
$$

Hessian $A$는 대칭이고 선도 주행렬식이 $4>0$, $\det A=7>0$이므로 양의 정부호예요. 따라서 이 정지점은 유일한 전역 최소점이에요.

#### 완성 답과 검산

#### (a) 검산

$f_1$은 $x_1$ 방향으로 $2x_1$, $x_2$ 방향으로 1만큼 변해요. 이 값들이 첫째 행에 있는지 확인해요.

#### (b) 검산

$\frac12x^\top Ax$의 교차항은 $\frac12(x_1x_2+x_2x_1)=x_1x_2$예요. 미분하면 두 교차 편미분이 모두 1이 되어 Hessian이 대칭이에요.

#### (c) 검산

$A(2/7,-1/7)^\top=(1,0)^\top=b$예요. 또 $q(x)-q(x_*)=\frac12(x-x_*)^\top A(x-x_*)>0$은 $x\ne x_*$에서 성립하므로 전역성과 유일성이 함께 확인돼요.

#### 여기서 헷갈리기 쉬워요

$x^\top Ax$와 $\frac12x^\top Ax$의 gradient는 2배 차이가 나요. Jacobian의 행과 열을 바꾸거나 gradient를 열벡터로 쓰지 않도록 문제의 표기 약속을 따라요.

#### 설명을 닫고 다시 풀어요

- x의 성분과 f의 출력 번호를 구분하며 네 편미분 자리를 채워요.
- 이차형식을 전개해 1/2와 교차항을 확인해요.
- 정지점만으로 최소성을 결론 낼 수 없는 이유와 이 문제의 충분조건을 말해요.

**페이지 요약**

#### 떠올릴 개념·공식

$J_f$: 출력×입력. 대칭 $A$이면 $\nabla q=x^\top A-b^\top$, $H=A$. 최소점 $(2/7,-1/7)^\top$.

#### 적용 조건

gradient는 행벡터, Jacobian은 출력×입력, A는 대칭

#### 출제 근거

출제 근거: 과제1 P10-P12 변형. MML PDF 153, 155, 156쪽의 이론을 대조했어요. 과제의 수치·조건을 바꾼 변형 문제예요. 교수님의 세부 출제 확정 내용은 아니에요.

#### 해설에 쓰인 용어

- **Jacobian 행렬 (Jacobian)** — 벡터 출력의 각 성분이 각 입력에 얼마나 민감한지 모은 일차 미분 행렬이에요.$f:\mathbb R^d\to\mathbb R^m$이면 $(J_f)_{ij}=\partial f_i/\partial x_j$, 크기는 $m\times d$예요.이 문제에서는 벡터 함수의 각 출력 미분을 올바른 행에 배치해요.
- **기울기 (gradient)** — 스칼라 함수의 각 입력 성분에 대한 일차 편미분을 모은 벡터예요. 여기서는 강의와 같이 행벡터로 써요.$\nabla_x L=(\partial L/\partial x_1,\ldots,\partial L/\partial x_d)$예요.이 문제에서는 스칼라 목적함수의 정지점을 구할 때 써요.
- **Hessian 행렬 (Hessian)** — 스칼라 함수의 이차 편미분을 모아 곡률을 나타낸 행렬이에요.$(H_L)_{ij}=\partial^2L/(\partial x_i\partial x_j)$예요. 매끄러운 함수에서는 대칭이에요.이 문제에서는 정지점 주변과 전체 이차함수의 곡률을 판단해요.
- **정지점 (stationary point)** — 미분 가능한 함수에서 기울기가 0인 점이에요. 이것만으로 최소점이라고 결론 내릴 수는 없어요.$\nabla L=0$을 푼 뒤 곡률이나 목적함수의 성질을 확인해요.이 문제에서는 기울기를 0으로 놓아 후보점을 찾는 단계예요.
- **양의 정부호 (positive definite)** — 실수 대칭행렬이 0이 아닌 모든 방향에 양의 이차형식 값을 주는 성질이에요.$z\ne0\Rightarrow z^\top Az>0$예요. 대칭인 양의 정부호 행렬은 가역이에요.이 문제에서는 이차함수의 유일한 전역 최소점을 보장하는 조건이에요.
- **이차형식 (quadratic form)** — 벡터의 성분을 두 개씩 곱한 항들을 행렬 하나로 표현한 스칼라예요.$x^\top Ax$예요. 공분산의 역행렬을 쓰는 Gaussian 지수와 곡률 분석에 나타나요.이 문제에서는 성분 전개와 행렬 미분을 연결해요.

---

<a id="p3"></a>

### 3. 가우시안 곱과 정규화

EXAM Problem 3 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p3)

#### 주어진 조건

실수 $z$에 대해 $p_0(z)=\mathcal N(z\mid0,1)$, $p_1(z)=\mathcal N(z\mid2,3)$이다. $\mathcal N(z\mid m,v)$의 둘째 인수 $v$는 분산이다.

$g(z)=p_0(z)p_1(z)$, $Z=\int_{-\infty}^{\infty}g(z)\,dz$, $q(z)=g(z)/Z$로 둔다.

#### 구할 것

1. $g(z)$의 지수에 들어가는 $z^2+(z-2)^2/3$을 완전제곱하라.
2. 정규화된 $q(z)$의 평균·분산과 정규화 상수를 포함한 밀도를 구하라.
3. $Z$를 계산하고 $g(z)$를 그대로 확률밀도라고 부를 수 있는지 설명하라.

#### 문제를 내 말로 읽어요

두 밀도를 곱하면 “같은 $z$를 두 밀도가 함께 얼마나 지지하는지”를 나타내요. 곱의 적분은 자동으로 1이 되지 않으므로 $Z$로 나누는 과정이 필요해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“가우시안 곱”과 “완전제곱”이 단서예요. 지수가 $-\frac12a(z-m)^2$ 형태일 때 precision(분산의 역수)은 $a=1/\sigma^2$, 분산은 $\sigma^2=1/a$예요. 지수에 곱해진 $-1/2$까지 함께 비교해야 해요. 평균은 제곱 안의 중심 $m$이에요. $\mathcal N(z\mid m,v)$의 앞 계수는 $1/\sqrt{2\pi v}$예요. 분산과 표준편차를 구분하고, 지수의 상수항도 $Z$ 계산에서는 남겨요.

#### 종이에 쓸 첫 줄

$z^2+(z-2)^2/3=\frac43z^2-\frac43z+\frac43$로 지수를 한 이차식으로 모아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$z$는 적분할 스칼라이고 $\mathcal N(z\mid m,v)$의 둘째 인수 $v$는 분산이에요. 같은 $z$에서 두 밀도의 높이를 곱하므로 각각의 일반식부터 대입해요.

$$
p_0(z)=\frac1{\sqrt{2\pi}}e^{-z^2/2},\qquad p_1(z)=\frac1{\sqrt{6\pi}}e^{-(z-2)^2/6}.
$$

앞 계수의 곱은 $1/(\sqrt{2\pi}\sqrt{6\pi})=1/(2\pi\sqrt3)$이고, 지수함수의 곱은 지수의 합이에요. 따라서

$$
g(z)=\frac1{2\pi\sqrt3}\exp\!\left[-\frac12\left(z^2+\frac{(z-2)^2}{3}\right)\right].
$$

가우시안의 평균과 분산을 읽으려면 제곱 하나로 묶어야 해요. $(z-2)^2=z^2-4z+4$를 넣으면 괄호 안은 $\frac43z^2-\frac43z+\frac43$이에요. 한편 $\frac43(z-\frac12)^2=\frac43z^2-\frac43z+\frac13$이므로 원래 상수 $4/3$를 맞추려면 1을 더해야 해요.

$$
z^2+\frac{(z-2)^2}{3}=\frac43(z-\tfrac12)^2+1.
$$

바깥의 $-1/2$를 두 항 모두에 곱하면 상수 $-1/2$가 남아요. $e^{a+b}=e^ae^b$로 분리하면

$$
g(z)=\frac{e^{-1/2}}{2\pi\sqrt3}\exp[-\tfrac23(z-\tfrac12)^2].
$$

이 앞 계수는 아직 전체 적분이 1이 되도록 정한 계수가 아니에요. (b)에서는 정규화된 밀도의 모양을, (c)에서는 버리지 않은 상수를 포함해 전체 넓이를 구해요.

#### (b)

(a)의 지수를 $-\frac12a(z-m)^2$와 비교하면 평균은 $m=1/2$, 정밀도는 $a=4/3$이에요. 따라서 분산은 $v=a^{-1}=3/4$예요.

Gaussian 밀도 공식에 대입하면 정규화된 밀도는

$$
q(z)=\frac1{\sqrt{2\pi(3/4)}}\exp\!\left[-\frac{(z-1/2)^2}{2(3/4)}\right]=\sqrt{\frac2{3\pi}}\exp\!\left[-\frac23(z-\tfrac12)^2\right].
$$

즉 $q(z)=\mathcal N(z\mid1/2,3/4)$예요.

#### (c)

(a)의 $g$와 (b)의 $q$는 지수 부분이 같아요. $g=Zq$이므로 앞 계수의 비가 $Z$예요.

$$
Z=\frac{e^{-1/2}/(2\pi\sqrt3)}{\sqrt{2/(3\pi)}}=\frac{e^{-1/2}}{\sqrt{8\pi}}.
$$

$\int g(z)\,dz=Z\ne1$이므로 $g$ 자체는 확률밀도가 아니에요. $q=g/Z$로 나누면 전체 적분이 1인 확률밀도가 돼요.

#### 완성 답과 검산

#### (a) 검산

$\frac43(z-1/2)^2+1$을 전개하면 $\frac43z^2-\frac43z+\frac43$이어서 원래 식과 일치해요.

#### (b) 검산

precision을 따로 더해도 $v^{-1}=1+1/3=4/3$, $m=v(0/1+2/3)=1/2$예요. 앞 계수 $\sqrt{2/(3\pi)}=1/\sqrt{2\pi(3/4)}$도 일치해요.

#### (c) 검산

곱의 적분 항등식으로도 $Z=\mathcal N(0\mid2,1+3)=e^{-1/2}/\sqrt{8\pi}$예요. $g$를 이 값으로 나누면 (b)의 앞 계수가 나와요.

#### 여기서 헷갈리기 쉬워요

중심 $1/2$를 구한 뒤 상수항 $+1$을 버리면 정규화된 모양은 찾을 수 있지만 $Z$는 틀려요. “비례한다”와 “같다”를 구분해요.

#### 설명을 닫고 다시 풀어요

- 지수가 $-3(z-m)^2$이면 분산과 정규화 앞 계수를 직접 구해요.
- $g$, $Z$, $q$ 각각의 의미와 적분값을 말해요.
- 완전제곱의 상수항을 남겨 Z를 다시 구해요.

**페이지 요약**

#### 떠올릴 개념·공식

precision 합산: $v^{-1}=v_0^{-1}+v_1^{-1}$. $m=1/2$, $v=3/4$, $Z=e^{-1/2}/\sqrt{8\pi}$.

#### 적용 조건

N의 둘째 인수는 분산; 정규화된 곱과 원래 곱을 구분

#### 출제 근거

출제 근거: 과제1 P14·P25 변형. MML PDF 207, 208쪽의 이론을 대조했어요. 과제의 수치·조건을 바꾼 변형 문제예요. 교수님의 세부 출제 확정 내용은 아니에요.

#### 해설에 쓰인 용어

- **Gaussian·정규분포 (Gaussian distribution)** — 평균을 중심으로 퍼짐이 정해지는 확률분포예요. 스칼라에서는 평균과 분산으로 정해져요.$\mathcal N(z\mid m,v)$의 $m$은 평균, $v>0$는 분산이에요. 표준편차는 $\sqrt v$예요.이 문제에서는 곱하기 전과 정규화한 뒤의 분포 모양을 읽어요.
- **정밀도 (precision)** — 분산의 역수 또는 공분산 행렬의 역행렬이에요. 퍼짐이 작을수록 정밀도가 커져요.스칼라에서는 $v^{-1}$, 다변량에서는 $S^{-1}$예요. 행렬인 경우 공분산이 가역이어야 해요.이 문제에서는 제곱항의 계수에서 분산을 읽는 데 써요.
- **완전제곱 (completing the square)** — 이차식에서 중심을 묶어 제곱항과 상수항으로 나누는 변형이에요.$az^2-2bz=a(z-b/a)^2-b^2/a$예요. Gaussian의 중심과 분산을 읽을 때는 $a>0$이어야 해요.이 문제에서는 지수를 중심과 상수 부분으로 나누어요.
- **정규화 상수 (normalizing constant)** — 양의 함수를 전체 적분값으로 나누어 총질량이 1인 밀도로 만드는 데 쓰는 값이에요.$q(z)=g(z)/Z$, $Z=\int g(z)\,dz$이며 $0<Z<\infty$여야 해요.이 문제에서는 곱한 함수의 적분값을 남겨 두어야 하는 이유예요.
- **확률밀도 (probability density)** — 연속 확률변수가 어떤 값 주변에 얼마나 집중되는지 나타내는 함수예요. 한 점의 확률과는 달라요.$P(a\le X\le b)=\int_a^b p(x)\,dx$예요. 밀도값 자체는 1보다 클 수도 있어요.이 문제에서는 두 밀도의 곱이 그 자체로 정규화되었다고 가정하지 않아요.

---

<a id="p4"></a>

### 4. 특징행렬로 계산하는 ML과 MAP

EXAM Problem 4 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p4)

#### 주어진 조건

스칼라 목적함수의 미분 결과는 강의와 같이 행벡터로 쓴다. 파라미터 벡터 자체는 열벡터이다.

관측은 $(x_n,y_n)=(-1,0),(0,1),(1,4)$이고 $\phi(x)=(1,x)^\top$이다. 모델은 $y_n=\phi(x_n)^\top\theta+\epsilon_n$이며 $\epsilon_n$은 독립 $\mathcal N(0,1)$이다.

MAP에서는 절편을 포함한 두 계수 모두에 $\theta\sim\mathcal N(0,I_2)$ prior를 적용한다. $\Phi$의 $n$번째 행은 $\phi(x_n)^\top$이다.

#### 구할 것

1. $\Phi$, $\Phi^\top\Phi$, $\Phi^\top y$를 구하라.
2. $\theta_{\mathrm{ML}}$을 구하고 $x_*=2$에서 평균 예측값을 구하라.
3. $\theta_{\mathrm{MAP}}$과 $x_*=2$에서 평균 예측값을 구하라. ML과 달라진 이유를 설명하라.

#### 문제를 내 말로 읽어요

먼저 세 관측을 행으로 모아 $3\times2$ 특징행렬을 만들어요. 같은 데이터에 대해 ML은 잔차만, MAP은 잔차와 prior를 함께 고려해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“고정 특징·Gaussian 잡음”은 최소제곱을 떠올리는 단서예요. $N$은 관측 수, $K$는 계수 수예요. $\Phi\in\mathbb R^{N\times K}$이고 열독립이면 $\theta_{\mathrm{ML}}=(\Phi^\top\Phi)^{-1}\Phi^\top y$예요. 평균 0, 공분산 $I$인 prior와 잡음분산 1이면 MAP의 Gram 행렬에 $I$를 더해요. 이 문제는 절편에도 prior를 적용하므로 두 대각성분을 모두 바꿔요.

#### 종이에 쓸 첫 줄

$\Phi=\begin{pmatrix}1&-1\\1&0\\1&1\end{pmatrix}$와 $y=(0,1,4)^\top$부터 적어요. 각 행이 관측 하나라는 뜻이에요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

여기서 $x_1=-1,x_2=0,x_3=1$은 서로 다른 세 관측의 스칼라 입력이에요. 아래첨자는 관측 번호예요. 여러 값을 $X$라는 벡터로 모아 적을 수 있어도 $\phi(x_n)$에 넣는 것은 그중 하나인 스칼라예요.

$\phi$ 자체는 입력을 특징으로 바꾸는 함수이고, $\phi(x)$는 그 함수를 계산한 결과인 $2\times1$ 열벡터예요. 하나씩 대입하면

$$
\phi(x_1)=\begin{pmatrix}1\\-1\end{pmatrix},\quad\phi(x_2)=\begin{pmatrix}1\\0\end{pmatrix},\quad\phi(x_3)=\begin{pmatrix}1\\1\end{pmatrix}.
$$

$\theta=(\theta_0,\theta_1)^\top$도 $2\times1$ 열벡터예요. $\phi(x_n)^\top\theta=1\theta_0+x_n\theta_1$에서 $\theta_0$는 절편, $\theta_1$은 기울기예요. 열벡터 두 개를 그대로 곱하지 않고, 첫 벡터를 전치해 $(1\times2)(2\times1)$ 내적을 만들어요.

모든 관측의 예측을 세로로 모으기 위해 **관측 하나를 한 행에 두는 약속**을 사용해요. 그러므로 열벡터 $\phi(x_n)$를 전치한 행을 아래로 쌓아요.

$$
\Phi=\begin{pmatrix}\phi(x_1)^\top\\\phi(x_2)^\top\\\phi(x_3)^\top\end{pmatrix}=\begin{pmatrix}1&-1\\1&0\\1&1\end{pmatrix}.
$$

$\Phi$는 하나의 벡터가 아니라 $3\times2$ 행렬이에요. $[\phi(x_1)\ \phi(x_2)\ \phi(x_3)]$처럼 열로 나란히 놓으면 $2\times3$인 $\Phi^\top$가 돼요. 다른 배치 약속도 가능하지만 그 경우 곱셈식도 함께 바꿔야 해요. 현재 약속에서는

$$
\Phi\theta=\begin{pmatrix}\theta_0-\theta_1\\\theta_0\\\theta_0+\theta_1\end{pmatrix}
$$

가 $y=(0,1,4)^\top$와 같은 $3\times1$이 되어 바로 비교할 수 있어요.

$\Phi$의 두 열은 $(1,1,1)^\top$, $(-1,0,1)^\top$예요. 열끼리 내적해 Gram 행렬을 채우면

$$
\Phi^\top\Phi=\begin{pmatrix}1+1+1&-1+0+1\\-1+0+1&(-1)^2+0^2+1^2\end{pmatrix}=\begin{pmatrix}3&0\\0&2\end{pmatrix}.
$$

각 열과 $y$의 내적도 계산해요.

$$
\Phi^\top y=\begin{pmatrix}1\cdot0+1\cdot1+1\cdot4\\(-1)\cdot0+0\cdot1+1\cdot4\end{pmatrix}=\begin{pmatrix}5\\4\end{pmatrix}.
$$

각 결과의 크기는 $2\times2$, $2\times1$이에요. 비대각 원소가 0인 것은 여기서 입력의 합이 0이기 때문이지, 모든 특징행렬에서 성립하는 규칙은 아니에요.

#### (b)

동일한 분산의 독립 Gaussian 잡음에서는 ML이 최소제곱과 같아요. (a)의 Gram 행렬은 가역이므로 ML 공식에 바로 대입해요.

$$
\theta_{\mathrm{ML}}=(\Phi^\top\Phi)^{-1}\Phi^\top y=\begin{pmatrix}1/3&0\\0&1/2\end{pmatrix}\begin{pmatrix}5\\4\end{pmatrix}=\begin{pmatrix}5/3\\2\end{pmatrix}.
$$

새 입력에서 $\phi(2)=(1,2)^\top$이므로 평균 예측값은

$$
\widehat\mu_*^{\mathrm{ML}}=\phi(2)^\top\theta_{\mathrm{ML}}=\frac53+2\cdot2=\frac{17}3.
$$

#### (c)

평균 0, 공분산 $\tau^2I$인 Gaussian prior에서는 $\lambda=\sigma^2/\tau^2$인 MAP 공식을 써요. 여기서는 $\sigma^2=\tau^2=1$이므로 $\lambda=1$이에요.

$$
\theta_{\mathrm{MAP}}=(\Phi^\top\Phi+\lambda I_2)^{-1}\Phi^\top y=\begin{pmatrix}1/4&0\\0&1/3\end{pmatrix}\begin{pmatrix}5\\4\end{pmatrix}=\begin{pmatrix}5/4\\4/3\end{pmatrix}.
$$

따라서 새 입력에서 평균 예측값은

$$
\widehat\mu_*^{\mathrm{MAP}}=\phi(2)^\top\theta_{\mathrm{MAP}}=\frac54+2\cdot\frac43=\frac{47}{12}.
$$

ML과 다른 이유는 prior가 계수를 0 쪽으로 당기는 제곱벌점을 더하기 때문이에요. 이 문제에서는 절편에도 prior가 적용되어 두 대각성분 모두에 1을 더해요.

#### 완성 답과 검산

#### (a) 검산

$\Phi^\top y=(0+1+4,-1\cdot0+0\cdot1+1\cdot4)^\top=(5,4)^\top$로 직접 확인해요.

#### (b) 검산

ML의 학습 예측은 $(-1/3,5/3,11/3)^\top$이고 잔차는 $(1/3,-2/3,1/3)^\top$예요. 잔차 합과 $x$가중 잔차 합이 모두 0이므로 정규방정식을 만족해요.

#### (c) 검산

$(\Phi^\top\Phi+I)\theta_{\mathrm{MAP}}=(5,4)^\top$예요. 또한 $17/3=68/12$이므로 MAP 예측 $47/12$가 수치적으로도 더 작아요.

#### 여기서 헷갈리기 쉬워요

데이터 순서를 바꾸었다면 $\Phi$와 $y$를 같은 순서로 바꿔야 해요. 절편의 prior를 빼는 다른 ridge 관습을 이 문제에 적용하면 답이 달라져요.

#### 설명을 닫고 다시 풀어요

- 세 스칼라에 $\phi$를 적용한 열벡터를 적고 전치해 $\Phi$를 만들어요.
- $\Phi\theta$의 세 성분과 새 입력에서 평균 예측의 뜻을 말해요.
- 잡음분산 1, 사전 공분산 $2I_2$에서 더하는 행렬을 유도해요.

**페이지 요약**

#### 떠올릴 개념·공식

Gram $\operatorname{diag}(3,2)$, ML $(5/3,2)$, MAP $(5/4,4/3)$. 모든 계수에 prior 적용.

#### 적용 조건

잡음분산 1, 절편 포함 모든 계수에 N(0,I) prior

#### 출제 근거

출제 근거: 과제1 P17-P20 변형. MML PDF 300, 302, 307, 308쪽의 이론을 대조했어요. 과제의 수치·조건을 바꾼 변형 문제예요. 교수님의 세부 출제 확정 내용은 아니에요.

#### 해설에 쓰인 용어

- **특징 (feature)** — 입력을 모형이 사용할 수 있도록 바꾼 표현이에요.$\phi(x)$의 성분에 $1$, $x$, $x^2$ 같은 함수를 넣을 수 있어요. $\phi(x)^\top\theta$는 모수 $\theta$에 대해 선형이에요.이 문제에서는 입력을 두 성분의 표현으로 바꾸어요.
- **특징행렬 (design matrix)** — 관측 하나의 특징벡터를 한 행에 놓아 쌓은 행렬이에요.$\Phi_{n,:}=\phi(x_n)^\top$이며 관측이 $N$개, 특징이 $K$개면 $N\times K$예요.이 문제에서는 관측 순서에 맞춰 특징을 행으로 쌓아요.
- **최대우도 추정 (maximum likelihood·ML)** — 관측한 데이터를 가장 그럴듯하게 만드는 모수를 고르는 방법이에요.$\hat\theta_{\mathrm{ML}}=\arg\max_\theta p(y\mid\theta,X)$예요. 입력 $X$와 관측 $y$는 고정해요.이 문제에서는 Gaussian 잡음의 데이터 적합도를 최대화해요.
- **최대사후 추정 (maximum a posteriori·MAP)** — 데이터를 본 뒤 모수의 사후밀도가 가장 높은 점을 고르는 방법이에요.$\hat\theta_{\mathrm{MAP}}=\arg\max_\theta p(\theta\mid D)$예요. prior와 likelihood가 함께 들어가요.이 문제에서는 모수 prior까지 반영한 추정점을 구해요.
- **사전분포 (prior)** — 현재 데이터를 보기 전에 모수의 가능성을 표현한 분포예요.$p(\theta)$ 또는 $p(\theta\mid M)$로 써요. Gaussian prior의 평균 $m_0$는 중심, 공분산 $S_0$는 퍼짐이에요.이 문제에서는 절편에도 prior가 적용된다는 조건을 읽어요.
- **Gram 행렬 (Gram matrix)** — 열벡터 사이의 모든 내적을 모은 행렬이에요.$G=U^\top U$이며 $G_{ij}=u_i^\top u_j$예요. 실수 행렬 $U$의 열이 독립이면 $G$는 가역이에요.이 문제에서는 두 추정법의 선형 방정식을 행렬로 정리해요.

---

<a id="p5"></a>

### 5. 표본 공분산과 아핀 변환

EXAM Problem 5 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p5)

#### 주어진 조건

세 관측 $x_1=(0,0)^\top$, $x_2=(2,0)^\top$, $x_3=(0,2)^\top$가 있다. 확률벡터 $X$는 이 셋 중 하나를 각각 확률 $1/3$로 취한다. 공분산은 분모 $N=3$을 사용한다.

$$
Y=AX+b,\quad A=\begin{pmatrix}1&1\\1&-1\end{pmatrix},\quad b=\begin{pmatrix}1\\-1\end{pmatrix}.
$$

#### 구할 것

1. $\mu_X=E[X]$와 $\Sigma_X=\frac13\sum_{n=1}^3(x_n-\mu_X)(x_n-\mu_X)^\top$를 구하라.
2. $\mu_Y$, $\Sigma_Y$, $C_{XY}=E[(X-\mu_X)(Y-\mu_Y)^\top]$를 구하라.
3. $Y_1,Y_2$는 무상관인가? 독립인가? 이 문제의 실제 세 가능한 $Y$값과 확률을 이용해 판단하라.

#### 문제를 내 말로 읽어요

$X$는 세 점을 똑같은 확률로 고르는 확률벡터예요. 그래서 분모 3인 공분산이 곧 이 분포의 공분산이에요. 변환 뒤 독립 여부는 공분산만 보고 끝내지 않아요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“아핀 변환”은 $E[AX+b]=A\mu_X+b$, $\operatorname{Cov}(AX+b)=A\Sigma_XA^\top$를 떠올리게 해요. 교차공분산은 첫 변수가 $X$이므로 $C_{XY}=\Sigma_XA^\top$예요. 상수 $b$는 평균에는 들어가지만 중심화할 때 사라져요. 비대각 공분산 0은 무상관이며, Gaussian 공동분포가 없으면 독립을 뜻하지 않아요.

#### 종이에 쓸 첫 줄

$\mu_X=(2/3,2/3)^\top$와 $E[XX^\top]=\operatorname{diag}(4/3,4/3)$를 써요. $\Sigma_X=E[XX^\top]-\mu_X\mu_X^\top$로 계산하면 짧아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$x_1=(0,0)^\top,x_2=(2,0)^\top,x_3=(0,2)^\top$는 벡터 관측 세 개예요. $X$는 이 셋 중 하나를 확률 $1/3$씩 고르는 확률벡터이고, $X_1,X_2$는 선택된 벡터의 첫째·둘째 성분이에요. 관측 번호 $x_n$과 성분 번호 $X_i$를 구분해요.

균등 선택의 기대값은 세 벡터의 평균이에요.

$$
\mu_X=\frac13\left[\begin{pmatrix}0\\0\end{pmatrix}+\begin{pmatrix}2\\0\end{pmatrix}+\begin{pmatrix}0\\2\end{pmatrix}\right]=\begin{pmatrix}2/3\\2/3\end{pmatrix}.
$$

평균을 뺀 벡터 $d_n=x_n-\mu_X$는 $d_1=(-2/3,-2/3)^\top$, $d_2=(4/3,-2/3)^\top$, $d_3=(-2/3,4/3)^\top$예요. 공분산은 이 편차의 외적을 평균내요. 외적은 $(2\times1)(1\times2)$라서 $2\times2$이고, 예를 들어 $d_1d_1^\top$의 네 원소는 편차 성분의 쌍별 곱이에요.

$$
d_1d_1^\top=\frac19\begin{pmatrix}4&4\\4&4\end{pmatrix},\qquad d_2d_2^\top=\frac19\begin{pmatrix}16&-8\\-8&4\end{pmatrix},
$$

$$
d_3d_3^\top=\frac19\begin{pmatrix}4&-8\\-8&16\end{pmatrix}.
$$

따라서 $\Sigma_X=\frac13\sum_nd_nd_n^\top=\frac1{27}\begin{pmatrix}24&-12\\-12&24\end{pmatrix}=\frac19\begin{pmatrix}8&-4\\-4&8\end{pmatrix}$예요. 대각은 각 성분의 분산, 비대각은 두 성분의 공분산이에요. 이 문제의 분모 3은 실제 확률 $1/3$에서 나와요. 불편 표본공분산의 분모 $N-1$로 바꾸면 다른 양을 계산하게 돼요.

#### (b)

아핀 변환 $Y=AX+b$의 평균·공분산·교차공분산 공식을 바로 적용해요.

$$
\mu_Y=A\mu_X+b,\qquad\Sigma_Y=A\Sigma_XA^\top,\qquad C_{XY}=\Sigma_XA^\top.
$$

(a)의 결과를 대입하면

$$
\mu_Y=\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}2/3\\2/3\end{pmatrix}+\begin{pmatrix}1\\-1\end{pmatrix}=\begin{pmatrix}7/3\\-1\end{pmatrix},
$$

$$
\Sigma_Y=A\left[\frac19\begin{pmatrix}8&-4\\-4&8\end{pmatrix}\right]A^\top=\begin{pmatrix}8/9&0\\0&8/3\end{pmatrix},
$$

$$
C_{XY}=\frac19\begin{pmatrix}8&-4\\-4&8\end{pmatrix}A^\top=\begin{pmatrix}4/9&4/3\\4/9&-4/3\end{pmatrix}.
$$

상수 $b$는 평균에만 영향을 줘요. 교차공분산은 $X,Y$ 순서이므로 $\Sigma_XA^\top$이며, $C_{YX}=C_{XY}^\top$예요.

#### (c)

(b)의 $\Sigma_Y$에서 비대각 성분이 0이므로 $Y_1,Y_2$는 무상관이에요. 독립은 더 강한 조건으로, 모든 가능한 값 $a,b$에 대해 $P(Y_1=a,Y_2=b)=P(Y_1=a)P(Y_2=b)$여야 해요. 이 분포는 세 점에만 확률을 두므로 공동 Gaussian이라는 조건도 없어요.

각 입력을 실제로 변환하면 $(0,0)^\top\mapsto(1,-1)^\top$, $(2,0)^\top\mapsto(3,1)^\top$, $(0,2)^\top\mapsto(3,-3)^\top$이고 각각 확률은 $1/3$이에요.

$Y_1=1$은 첫 점에서, $Y_2=1$은 둘째 점에서 가능하지만 두 사건이 동시에 일어나는 점은 없어요. 따라서

$$
P(Y_1=1,Y_2=1)=0,
$$

$$
P(Y_1=1)P(Y_2=1)=\frac13\cdot\frac13=\frac19.
$$

한 쌍에서라도 독립 조건이 깨졌으므로 독립이 아니에요. 첫 성분이 1이라는 정보를 알면 둘째 성분은 반드시 $-1$이라는 사실도 같은 결론을 보여 줘요. 공분산 0은 이런 의존관계 전체를 검사하는 조건이 아니에요.

#### 완성 답과 검산

#### (a) 검산

세 중심화 벡터 $(-2/3,-2/3)$, $(4/3,-2/3)$, $(-2/3,4/3)$의 외적을 합해 3으로 나누어도 같은 행렬이에요.

#### (b) 검산

변환된 세 점의 평균은 $(7/3,-1)$이에요. 첫째 성분 편차는 $(-4/3,2/3,2/3)$, 둘째는 $(0,2,-2)$여서 공분산은 0, 분산은 각각 $8/9,8/3$이에요.

#### (c) 검산

$Y_1=1$인 경우에는 $Y_2=-1$만 가능해요. 조건부확률 $P(Y_2=1\mid Y_1=1)=0$은 주변확률 $1/3$과 다르므로 독립이 아니에요.

#### 여기서 헷갈리기 쉬워요

분모를 $N-1=2$로 바꾸지 않아요. “무상관이면 독립”은 일반 법칙이 아니에요. 여기서는 실제 결합확률 하나를 비교하면 독립이 아님을 보일 수 있어요.

#### 설명을 닫고 다시 풀어요

- $x_n$의 관측 번호와 $X_i$의 성분 번호를 구분해요.
- 편차 외적 하나를 네 원소로 펼치고 분모가 3인 이유를 말해요.
- 무상관을 계산한 뒤 독립 조건이 깨지는 사건 한 쌍을 찾아요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mu_Y=A\mu_X+b$, $\Sigma_Y=A\Sigma_XA^\top$, $C_{XY}=\Sigma_XA^\top$. 무상관이지만 독립 아님.

#### 적용 조건

공분산 분모 N=3; X는 세 관측을 균등 선택; Gaussian 가정 없음

#### 출제 근거

출제 근거: 과제1 P21-P22 변형. MML PDF 194, 196, 198, 200쪽의 이론을 대조했어요. 과제의 수치·조건을 바꾼 변형 문제예요. 교수님의 세부 출제 확정 내용은 아니에요.

#### 해설에 쓰인 용어

- **표본 공분산 (sample covariance)** — 주어진 표본으로 평균 주변의 함께 움직임을 계산한 행렬이에요.이 문항의 정의는 $S=\frac1N\sum_n(x_n-\bar x)(x_n-\bar x)^\top$예요. 분모가 $N-1$인 불편추정량과 구별해요.이 문제에서는 문제에서 지정한 분모로 표본의 퍼짐을 계산해요.
- **아핀 변환 (affine transformation)** — 선형 변환을 한 뒤 일정한 벡터만큼 평행이동하는 변환이에요.$Y=AX+b$예요. $E[Y]=A\mu_X+b$, $\operatorname{Cov}(Y)=A\Sigma_XA^\top$예요.이 문제에서는 원래 표본의 통계를 변환한 표본의 통계로 옮겨요.
- **공분산 (covariance)** — 평균에서 벗어난 두 성분이 함께 움직이는 정도예요. 대각성분은 각 성분의 분산이에요.$\Sigma_X=E[(X-\mu_X)(X-\mu_X)^\top]$예요. 스칼라 분산과 공분산 행렬의 크기를 구별해요.이 문제에서는 변환 전후 성분들의 함께 움직임을 읽어요.
- **교차공분산 (cross-covariance)** — 서로 다른 두 확률벡터 사이의 성분별 공분산을 모은 행렬이에요.$C_{XY}=E[(X-\mu_X)(Y-\mu_Y)^\top]$예요. $X$의 차원이 행 수, $Y$의 차원이 열 수예요.이 문제에서는 첫 변수와 둘째 변수의 순서를 지켜 행렬을 만들어요.
- **무상관 (uncorrelated)** — 두 변수의 공분산이 0인 상태예요. 일반적으로 독립까지 뜻하지는 않아요.$\operatorname{Cov}(X,Y)=0$은 선형적인 함께 움직임이 없다는 조건이에요.이 문제에서는 비대각 원소가 0이라는 결론의 범위를 읽어요.
- **공동 Gaussian (jointly Gaussian)** — 각 변수를 따로 보는 것에 더해, 이들을 합쳐 만든 벡터 전체가 다변량 Gaussian인 경우예요.공동 Gaussian인 두 변수는 교차공분산이 0이면 독립이에요. 주변분포가 각각 Gaussian이라는 사실만으로는 부족해요.이 문제에서는 무상관에서 독립까지 결론 내릴 수 있는 추가 조건을 구별해요.

---

<a id="p6"></a>

### 6. 확률모델에서 경험위험 최소화까지

EXAM Problem 6 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p6)

#### 주어진 조건

스칼라 목적함수의 미분 결과는 강의와 같이 행벡터로 쓴다. 파라미터 벡터 자체는 열벡터이다.

고정 입력 $x_1,\ldots,x_N$과 $y_n=\theta_0+\theta_1x_n+\epsilon_n$을 생각하자. $\theta=(\theta_0,\theta_1)^\top$이고, $\epsilon_n$은 서로 독립이며 $\mathcal N(0,\sigma^2)$를 따른다. $\sigma^2>0$는 알려져 있다. $\Phi$의 $n$번째 행은 $(1,x_n)$이며 열들은 선형독립이다.

#### 구할 것

1. 고정 입력과 $\theta$가 주어졌을 때 $y_n$의 조건부 분포를 쓰고, 관측들의 조건부 독립성이 성립하는 이유를 설명하라.
2. 소문항 (a)를 이용해 전체 우도 $p(y\mid\Phi,\theta)$와 음의 로그우도 $\mathcal L(\theta)$를 정규화 상수까지 써라.
3. 소문항 (b)의 목적함수를 제곱손실 경험위험 $\widehat R(\theta)=N^{-1}\sum_n(y_n-\phi(x_n)^\top\theta)^2$와 연결하라. 왜 최소점이 같은가?
4. 소문항 (c)의 제곱오차를 $\theta$의 이차식으로 전개하고 행 gradient를 구해 정규방정식을 도출하라.
5. 소문항 (d)를 풀어 $\theta_{\mathrm{ML}}$을 도출하고 유일한 최소점임을 보여라. 특징을 $(1,x,x^2)^\top$로 바꾸어도 선형 회귀인 이유를 설명하라.

#### 문제를 내 말로 읽어요

확률모델에서 경험위험 최소화까지: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 Gaussian 선형 회귀의 ML 추정식에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“서로 독립인 Gaussian 잡음”은 조건부 우도를 곱으로 쓰는 단서예요. 입력과 $\theta$가 주어졌을 때 각 출력의 평균은 $\phi_n^\top\theta$, 분산은 $\sigma^2$예요. 경험위험(empirical risk)은 관측 손실의 평균이에요. $\theta$와 무관한 상수나 양의 배수는 최소화 위치를 바꾸지 않아요. 알려진 고정 $\sigma^2$라는 조건이 이 연결에 필요해요.

#### 종이에 쓸 첫 줄

$y_n\mid\Phi,\theta\sim\mathcal N(\phi_n^\top\theta,\sigma^2)$부터 적고, 다음 줄에서 독립성을 곱으로 바꾸어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

입력 $x_n$은 고정된 스칼라, $y_n$은 그 입력의 출력이고 $n$은 관측 번호예요. $\phi_n=(1,x_n)^\top$와 $\theta=(\theta_0,\theta_1)^\top$는 $2\times1$이므로 $\phi_n^\top\theta=\theta_0+\theta_1x_n$은 스칼라예요. $\Phi$는 이 전치 특징을 행으로 모은 $N\times2$ 행렬이에요.

잡음 모형 $y_n=\phi_n^\top\theta+\epsilon_n$에서 입력과 계수를 주어진 값으로 고정해요. 그러면 무작위인 것은 $\epsilon_n\sim\mathcal N(0,\sigma^2)$뿐이에요. 상수를 더하면 평균만 이동하므로

$$
y_n\mid\Phi,\theta\sim\mathcal N(\phi_n^\top\theta,\sigma^2).
$$

독립인 잡음마다 서로 다른 출력을 하나씩 만들기 때문에 이 조건 아래 출력들도 독립이에요. 모수의 분포까지 적분해 없앤 뒤의 주변 독립을 주장하는 것은 아니에요. 이 조건부 독립이 (b)에서 밀도를 곱할 근거예요.

#### (b)

관측한 $y=(y_1,\ldots,y_N)^\top$와 $\Phi$를 고정하고 미지수 $\theta$를 바꾸어 평가하는 함수를 우도(likelihood)라고 해요. (a)의 독립성 때문에 결합밀도를 개별 밀도의 곱으로 쓸 수 있어요.

$$
p(y\mid\Phi,\theta)=\prod_{n=1}^N\frac1{\sqrt{2\pi\sigma^2}}\exp\!\left[-\frac{(y_n-\phi_n^\top\theta)^2}{2\sigma^2}\right].
$$

같은 앞 계수를 $N$번 곱하면 $(2\pi\sigma^2)^{-N/2}$이고 지수는 합쳐져요. 잔차벡터 $r=y-\Phi\theta$의 $n$번째 성분이 괄호 안의 오차이므로 $\sum_nr_n^2=\|r\|^2$예요.

$$
p(y\mid\Phi,\theta)=(2\pi\sigma^2)^{-N/2}\exp\!\left[-\frac{\|y-\Phi\theta\|^2}{2\sigma^2}\right].
$$

로그는 곱을 합으로, 지수함수를 지수로 바꿔요. 앞에 음수를 붙이면 최대화가 최소화로 바뀌어요.

$$
\mathcal L(\theta)=-\log p(y\mid\Phi,\theta)=\frac N2\log(2\pi\sigma^2)+\frac{\|y-\Phi\theta\|^2}{2\sigma^2}.
$$

여기까지는 정규화 계수도 보존한 정확한 등식이에요. 우도는 $y$에 대한 밀도식에서 출발했지만, 최적화할 때에는 $y$를 고정하고 $\theta$의 함수로 보는 점에 주의해요.

#### (c)

경험위험 $\widehat R(\theta)=\frac1N\sum_n(y_n-\phi_n^\top\theta)^2$은 이 문제에서 제곱손실의 평균이에요. (b)의 잔차제곱합은 평균이 아니라 합이므로 $N\widehat R$이에요. 이를 대입하면

$$
\mathcal L(\theta)=C+\frac{N}{2\sigma^2}\widehat R(\theta),\qquad C=\frac N2\log(2\pi\sigma^2).
$$

최적화 변수는 $\theta$이며 $N,\Phi,y,\sigma^2$는 고정이에요. 따라서 $C$는 어떤 후보를 골라도 같고 $N/(2\sigma^2)>0$이에요. 두 후보의 위험 차이가 양수이면 음의 로그우도 차이도 양수이므로 순위와 최소점이 같아요.

로그가 증가함수라는 사실까지 연결하면 우도 최대화 = 음의 로그우도 최소화 = 경험위험 최소화예요. 이때 버릴 수 있다는 것은 최소점 위치를 구하는 목적에 한정해요. 밀도값이나 evidence 자체를 계산할 때 정규화 계수를 지워도 된다는 뜻은 아니에요.

#### (d)

최소점이 같으므로 미분하기 쉬운 $Q(\theta)=\|y-\Phi\theta\|^2$를 사용해요. 노름 제곱을 내적으로 바꾸고 분배법칙으로 네 항을 펼쳐요.

$$
Q=(y-\Phi\theta)^\top(y-\Phi\theta),
$$

$$
Q=y^\top y-y^\top\Phi\theta-\theta^\top\Phi^\top y+\theta^\top\Phi^\top\Phi\theta.
$$

$y^\top\Phi\theta$는 스칼라여서 전치해도 같고, 전치한 식이 $\theta^\top\Phi^\top y$예요. 두 교차항을 합하면 $Q=y^\top y-2\theta^\top\Phi^\top y+\theta^\top G\theta$, $G=\Phi^\top\Phi$예요.

$y^\top y$는 상수, 선형항의 행 gradient는 $-2y^\top\Phi$, 대칭행렬 $G$의 이차항 gradient는 $2\theta^\top G$예요. 그러므로

$$
\nabla_\theta Q=-2y^\top\Phi+2\theta^\top\Phi^\top\Phi.
$$

이 $1\times2$ 행 gradient를 0으로 놓고 2로 나누면 $\theta^\top\Phi^\top\Phi=y^\top\Phi$예요. 양변 전치하면 정규방정식 $\Phi^\top\Phi\theta=\Phi^\top y$를 얻어요. 양변은 계수 두 개에 대응하는 $2\times1$이에요. 아직 역행렬을 곱하지 않았으므로 이 단계 자체는 열독립 없이도 성립해요.

#### (e)

주어진 열독립 조건은 $\Phi v=0$이면 $v=0$이라는 뜻이에요. 따라서 $v\ne0$일 때

$$
v^\top(\Phi^\top\Phi)v=(\Phi v)^\top(\Phi v)=\|\Phi v\|^2>0.
$$

즉 $G=\Phi^\top\Phi$는 양의 정부호이고 역행렬이 있어요. (d)의 양변 왼쪽에 $G^{-1}$를 곱하면

$$
\theta_{\mathrm{ML}}=(\Phi^\top\Phi)^{-1}\Phi^\top y.
$$

곱 순서는 $(2\times2)(2\times N)(N\times1)$이라 결과는 $2\times1$이에요. 목적함수의 Hessian $2G$가 양의 정부호이므로 구한 해는 유일한 전역 최소점이에요. 열종속이면 이 역행렬 공식과 유일성을 그대로 사용할 수 없어요.

선형 회귀의 ‘선형’은 입력 $x$가 아니라 모수 $\theta$에 대한 말이에요. 예를 들어 특징을 $(1,x,x^2)^\top$로 바꾸면 예측은 $\theta_0+\theta_1x+\theta_2x^2$로 곡선이지만, 미지수인 각 계수가 일차로 더해지므로 여전히 모수에 선형이에요. 그때에는 $\Phi$가 $N\times3$이 되고 같은 유도를 적용해요.

#### 완성 답과 검산

#### (a) 검산

각 평균은 스칼라이고 분산은 알려진 양수예요. 독립성은 모수를 고정한 조건부 주장임을 확인해요.

#### (b) 검산

$N=1$을 넣으면 한 관측 Gaussian 밀도와 그 음의 로그로 돌아가요.

#### (c) 검산

$\mathcal L(\theta_a)-\mathcal L(\theta_b)=N(\widehat R(\theta_a)-\widehat R(\theta_b))/(2\sigma^2)$여서 부호가 같아요.

#### (d) 검산

원래 제곱합을 성분별 미분해도 $-2\sum_n(y_n-\phi_n^\top\theta)\phi_n^\top$로 같아요.

#### (e) 검산

최종 식을 정규방정식에 넣으면 양변이 같아요. 잔차는 $\Phi^\top r=0$, 추정량은 $2\times1$이에요.

#### 여기서 헷갈리기 쉬워요

조건부 독립과 주변 독립을 혼동하지 않아요. $\sigma^2$도 함께 추정하는 문제라면 그 항을 상수라고 버릴 수 없어요. 여기서는 알려진 분산으로 고정했어요.

#### 설명을 닫고 다시 풀어요

- 조건부 Gaussian 한 개에서 시작해 곱 우도와 음의 로그를 유도해요.
- 최적화에서 무엇이 고정이고 어떤 항을 생략하는지 설명해요.
- 제곱노름을 전개해 정규방정식을 얻고 역행렬 조건을 말해요.

**페이지 요약**

#### 떠올릴 개념·공식

독립 Gaussian → 곱 우도 → NLL $=\mathrm{const}+\mathrm{SSE}/(2\sigma^2)$ → ERM. 선형성은 계수 $\theta$ 기준.

#### 적용 조건

고정 입력; θ를 조건으로 독립인 동일분산 Gaussian 잡음; σ² 알려짐

#### 출제 근거

출제 근거: MML 9.2 theory application. MML PDF 298, 299, 300, 302쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **우도 (likelihood)** — 관측한 데이터는 고정하고 모수를 바꾸어 보며 평가하는 데이터 밀도예요.$L(\theta)=p(y\mid\theta,X)$예요. 같은 식이라도 $\theta$에 대한 정규화된 확률분포라고 가정하면 안 돼요.이 문제에서는 조건부 관측 밀도들을 모아 모수의 함수를 만들어요.
- **조건부 독립 (conditional independence)** — 공유하는 조건을 고정했을 때 변수들의 결합분포가 곱으로 나뉘는 성질이에요.$p(y_1,y_2\mid\theta,X)=p(y_1\mid\theta,X)p(y_2\mid\theta,X)$예요. $\theta$를 적분한 뒤에도 독립이라고 자동으로 결론 내릴 수는 없어요.이 문제에서는 모수를 고정했을 때 우도를 곱으로 쓰는 근거예요.
- **음의 로그우도 (negative log-likelihood·NLL)** — 우도에 로그를 취하고 부호를 바꾼 목적함수예요. 우도의 곱을 항들의 합으로 다룰 수 있어요.$\operatorname{NLL}(\theta)=-\log p(y\mid\theta,X)$예요. 우도 최대화와 NLL 최소화의 위치는 같아요.이 문제에서는 곱으로 된 우도를 합으로 바꾸어 미분해요.
- **경험위험 (empirical risk)** — 관측한 각 데이터의 손실을 평균낸 값이에요.$R_N(\theta)=\frac1N\sum_n\ell(y_n,f_\theta(x_n))$예요. 어떤 손실을 택했는지 함께 밝혀야 해요.이 문제에서는 관측 손실 평균과 확률모형의 목적함수를 연결해요.
- **잔차제곱합 (sum of squared errors·SSE)** — 관측값과 모형 예측의 차이를 제곱해서 모두 더한 값이에요.$\operatorname{SSE}=\sum_n(y_n-\hat y_n)^2=\|y-\hat y\|^2$예요. 합과 평균은 $N$배 차이가 있어요.이 문제에서는 Gaussian NLL에서 남는 데이터 오차 부분이에요.
- **정규방정식 (normal equations)** — 최소제곱 목적함수를 미분해 얻는 선형 방정식이에요.$\Phi^\top\Phi\theta=\Phi^\top y$예요. 유일한 해를 역행렬로 쓰려면 $\Phi$의 열독립 조건이 필요해요.이 문제에서는 미분 결과를 하나의 선형 방정식으로 정리해요.
- **최대우도 추정 (maximum likelihood·ML)** — 관측한 데이터를 가장 그럴듯하게 만드는 모수를 고르는 방법이에요.$\hat\theta_{\mathrm{ML}}=\arg\max_\theta p(y\mid\theta,X)$예요. 입력 $X$와 관측 $y$는 고정해요.이 문제에서는 확률모형에서 출발한 최적화의 의미를 설명해요.

---

<a id="p7"></a>

### 7. Gaussian prior가 만드는 ridge

EXAM Problem 7 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p7)

#### 주어진 조건

스칼라 목적함수의 미분 결과는 강의와 같이 행벡터로 쓴다. 파라미터 벡터 자체는 열벡터이다.

고정 $\Phi\in\mathbb R^{N\times K}$에 대해 $y\mid\theta\sim\mathcal N(\Phi\theta,\sigma^2 I_N)$, $\theta\sim\mathcal N(m_0,\tau^2 I_K)$이다. $\sigma^2,\tau^2>0$는 알려져 있고 prior는 절편이 있으면 그 계수에도 적용한다. $\Phi$의 열독립은 가정하지 않는다.

#### 구할 것

1. Bayes 정리를 이용해 $p(\theta\mid y,\Phi)$에 비례하는 likelihood와 prior의 곱을 써라. Evidence는 $\theta$에 의존하는가?
2. 소문항 (a)에 Gaussian 밀도를 대입하고 $\theta$와 무관한 상수를 분리해 음의 로그 posterior를 유도하라.
3. 소문항 (b)의 두 이차항을 각각 미분하여 MAP 정규방정식을 도출하라.
4. 소문항 (c)를 풀어 MAP 추정식을 도출하라. 제곱오차와 $\|\theta-m_0\|^2$의 합으로 쓸 때 상대 벌점계수 $\lambda$는 무엇인가?
5. 소문항 (d)의 역행렬이 열독립 가정 없이도 존재하는 이유를 비영 벡터의 이차형식으로 증명하라.
6. $\Phi=\begin{pmatrix}1&1\\2&2\end{pmatrix}$, $y=(1,2)^\top$, $m_0=0$, $\lambda=1$일 때 (d)의 해를 계산하라. $\lambda=0$의 해의 유일성 및 $\lambda\to\infty$의 극한과 비교하라.

#### 문제를 내 말로 읽어요

Gaussian prior가 만드는 ridge: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 Gaussian prior와 ridge의 MAP 추정식에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

Bayes 정리에서 posterior는 likelihood×prior에 비례해요. 음의 로그를 취하면 잔차 벌점과 prior 중심에서의 거리 벌점이 더해져요. $\lambda=\sigma^2/\tau^2$는 두 벌점의 상대 세기예요. $\Phi^\top\Phi$는 양의 준정부호이고 $\lambda I$를 더하면 모든 방향의 곡률이 양수가 돼요.

#### 종이에 쓸 첫 줄

$-\log p(\theta\mid y,\Phi)=\frac1{2\sigma^2}\|y-\Phi\theta\|^2+\frac1{2\tau^2}\|\theta-m_0\|^2+C$부터 적어요. $C$만 $\theta$와 무관해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

고정된 것은 관측 $y$, 특징행렬 $\Phi$, 잡음분산 $\sigma^2$, prior의 평균 $m_0$와 분산 $\tau^2$예요. 찾는 것은 $K\times1$ 계수벡터 $\theta$예요. Prior는 데이터를 보기 전의 모수 분포, likelihood는 주어진 모수에서 관측을 설명하는 밀도, posterior는 데이터를 반영한 모수 분포예요.

$$
p(\theta\mid y,\Phi)=\frac{p(y\mid\Phi,\theta)p(\theta)}{p(y\mid\Phi)}.
$$

분모를 $\int p(y\mid\Phi,u)p(u)\,du$로 쓰면 $u$는 적분 뒤 사라지는 임시 변수예요. 따라서 분모는 지금 비교하는 $\theta$에 따라 달라지지 않아요. 고정된 양수로 나누어도 최대가 되는 위치는 같으므로 분자의 곱을 최대화해도 MAP가 같아요.

그러나 분모를 없앤 곱이 곧 정규화된 사후밀도라는 뜻은 아니에요. 여기서 분모를 생략하는 이유는 사후밀도값 전체가 아니라 최대점 하나를 구하기 때문이에요.

#### (b)

Gaussian의 지수는 공분산의 역행렬을 사용해요. $\Sigma_0=\tau^2I_K$라면 $\Sigma_0^{-1}=(1/\tau^2)I_K$이므로 prior 밀도는

$$
p(\theta)=(2\pi\tau^2)^{-K/2}\exp\!\left[-\frac{\|\theta-m_0\|^2}{2\tau^2}\right].
$$

따라서 사전분산이 분모에 들어가요. 큰 분산은 같은 거리에도 약한 벌점을, 작은 분산은 강한 벌점을 줘요. Likelihood의 지수에는 잡음분산 $\sigma^2$가 분모에 있어요. (a)의 곱에 음의 로그를 취하면 두 지수의 부호가 바뀌어 더해져요.

$$
J(\theta)=\frac{\|y-\Phi\theta\|^2}{2\sigma^2}+\frac{\|\theta-m_0\|^2}{2\tau^2}+C.
$$

$C$는 정규화 계수의 로그와 evidence의 로그를 모은 $\theta$ 무관 상수예요. 첫 항은 데이터에서의 오차, 둘째 항은 prior 중심으로부터의 제곱거리예요. $m_0$를 임의로 0으로 바꾸면 다른 prior를 푸는 것이므로 그대로 남겨요.

#### (c)

(b)를 $\theta$에 대해 미분해요. 제곱노름에서 나온 2가 분모의 2와 소거돼요.

$$
\nabla_\theta J=\frac{\theta^\top\Phi^\top\Phi-y^\top\Phi}{\sigma^2}+\frac{(\theta-m_0)^\top}{\tau^2}.
$$

이 $1\times K$ 행 gradient를 0으로 놓으면 $\theta^\top\Phi^\top\Phi-y^\top\Phi+(\sigma^2/\tau^2)(\theta-m_0)^\top=0$이에요. 여기서는 $\sigma^2$를 곱했어요. 양변 전치하면

$$
\Phi^\top\Phi\theta-\Phi^\top y+\frac{\sigma^2}{\tau^2}\theta-\frac{\sigma^2}{\tau^2}m_0=0.
$$

즉 사전분산은 여전히 분모에 있고 잡음분산이 분자로 올라와요. $\lambda=\sigma^2/\tau^2$로 이름을 붙이고 $\theta=I_K\theta$를 사용하면

$$
(\Phi^\top\Phi+\lambda I_K)\theta=\Phi^\top y+\lambda m_0.
$$

왼쪽의 $\lambda I_K$는 행렬과 벡터를 곱하기 위해 나타난 것이에요. 오른쪽의 $\lambda m_0$는 $-\lambda m_0$를 이항한 결과예요. 앞 문제에서 사전분산을 $b^2$라고 썼다면 여기의 $\tau^2$와 같은 역할이에요.

#### (d)

(c)는 $K\times K$ 행렬과 $K\times1$ 벡터의 선형방정식이에요. 그 행렬이 가역이면 양변 왼쪽에 역행렬을 곱해요.

$$
\theta_{\mathrm{MAP}}=(\Phi^\top\Phi+\lambda I_K)^{-1}(\Phi^\top y+\lambda m_0).
$$

가역성은 다음 소문항에서 $\lambda>0$으로 확인해요. 목적함수 관점에서도 (b)에 양수 $2\sigma^2$를 곱하면

$$
\|y-\Phi\theta\|^2+\lambda\|\theta-m_0\|^2+2\sigma^2C
$$

가 되어 같은 최소점을 가져요. $m_0=0$이면 익숙한 ridge 제곱벌점이에요. 잡음이 클수록 데이터의 상대 신뢰가 낮아져 $\lambda$가 커지고, prior 분산이 클수록 prior의 제약이 약해져 $\lambda$가 작아져요. 일반 공분산 $\Sigma_0$에서는 $\lambda I_K$ 대신 $\sigma^2\Sigma_0^{-1}$를 써야 해요.

#### (e)

$\Phi$의 열이 종속이어도 Gram 행렬의 이차형식은 제곱노름이라 음수가 될 수 없어요. 문제는 어떤 비영 방향에서 0이 될 수 있다는 점이에요. $A=\Phi^\top\Phi+\lambda I_K$로 두고 모든 $v\ne0$를 생각하면

$$
v^\top Av=\|\Phi v\|^2+\lambda\|v\|^2.
$$

첫 항은 0 이상이고, 둘째 항은 $\lambda>0$와 $\|v\|^2>0$ 때문에 반드시 양수예요. 따라서 합은 양수이고 $A$는 양의 정부호예요. 만약 $Av=0$인 비영 벡터가 있으면 $v^\top Av=0$이 되어 모순이므로 역행렬도 존재해요.

또한 (b)의 Hessian은 $A/\sigma^2$이고 $\sigma^2>0$이므로 양의 정부호예요. 따라서 정지점은 유일한 전역 최소점, 즉 유일한 MAP예요. 여기서 열독립을 별도로 가정할 필요가 없는 이유는 $\lambda\|v\|^2$가 모든 비영 방향에 양의 곡률을 더하기 때문이에요.

#### (f)

수치 예의 $\Phi=\begin{pmatrix}1&1\\2&2\end{pmatrix}$는 두 열이 같아 열종속이에요. $y=(1,2)^\top$와 내적하면 $G=\begin{pmatrix}5&5\\5&5\end{pmatrix}$, $\Phi^\top y=(5,5)^\top$예요. $m_0=0$, $\lambda=1$을 넣으면

$$
6\theta_1+5\theta_2=5,\qquad5\theta_1+6\theta_2=5.
$$

두 식을 빼면 $\theta_1-\theta_2=0$이에요. 같은 값을 첫 식에 넣어 $11\theta_1=5$이므로 $\theta=(5/11,5/11)^\top$예요. 이 소문항의 두 계수는 $\theta_1,\theta_2$라는 표기를 따라요.

$\lambda=0$이면 두 방정식 모두 $5(\theta_1+\theta_2)=5$가 돼요. 예측은 $(\theta_1+\theta_2)(1,2)^\top$이므로 합이 1인 모든 계수가 잔차 0을 만들어요. 따라서 최소제곱 해는 유일하지 않아요.

일반 $\lambda>0$에서는 식의 차가 $\lambda(\theta_1-\theta_2)=0$이 되어 두 계수가 같고, $(10+\lambda)\theta_1=5$예요. 따라서 각 계수는 $5/(10+\lambda)$이며 $\lambda\to\infty$이면 둘 다 prior 평균 0으로 가요. 이 대칭 예의 성분별 감소를 모든 ridge 문제의 성분별 법칙으로 일반화하지 않아요.

#### 완성 답과 검산

#### (a) 검산

분모를 적분식으로 쓰면 적분 변수는 사라지고 데이터와 모델만 남아요.

#### (b) 검산

각 항은 무차원 지수이며 prior 중심을0으로 임의 변경하지 않았어요.

#### (c) 검산

$\theta=m_0$에서 prior의 gradient는0이에요. 부호를 확인하는 간단한 점검이에요.

#### (d) 검산

$\sigma^2$를 크게 하면 데이터보다 prior의 상대 비중이 커져 $\lambda$가 커져요.

#### (e) 검산

$Av=0$인 비영 벡터가 있다면 $v^\top Av=0$이어야 하므로 위 양수 결과와 모순이에요.

#### (f) 검산

$(6+5)5/11=5$로 양 행을 만족해요. 일반 $\lambda>0$에서는 두 성분이 $5/(10+\lambda)$여서 큰 벌점 극한은0이에요.

#### 여기서 헷갈리기 쉬워요

$m_0\ne0$일 때 우변의 $\lambda m_0$를 빠뜨리지 않아요. 규제(regularization)는 계수를 prior 쪽으로 제약하지만 시험·새 데이터 오차가 항상 좋아진다는 보장은 없어요. 지나치게 큰 $\lambda$는 데이터 정보를 거의 무시해요.

#### 설명을 닫고 다시 풀어요

- 두 분산의 분모를 남긴 미분식에서 $\lambda$와 $\lambda m_0$를 유도해요.
- 열종속이어도 양의 벌점이 유일성을 보장하는 이유를 임의 방향으로 증명해요.
- 수치 예의 두 식을 빼서 같은 계수를 얻고 벌점의 두 극한을 설명해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\lambda=\sigma^2/\tau^2>0$. $G+\lambda I\succ0$. MAP $=(G+\lambda I)^{-1}(\Phi^\top y+\lambda m_0)$.

#### 적용 조건

고정 입력; 모든 계수에 N(m0,τ²I) prior; σ²,τ²&gt;0

#### 출제 근거

출제 근거: MML 9.2.3-9.2.4 theory application. MML PDF 307, 308, 309쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **사전분포 (prior)** — 현재 데이터를 보기 전에 모수의 가능성을 표현한 분포예요.$p(\theta)$ 또는 $p(\theta\mid M)$로 써요. Gaussian prior의 평균 $m_0$는 중심, 공분산 $S_0$는 퍼짐이에요.이 문제에서는 벌점이 어느 모수 중심에서 시작하는지 결정해요.
- **사후분포 (posterior)** — 데이터를 반영해 갱신한 모수의 분포예요.$p(\theta\mid D)\propto p(D\mid\theta)p(\theta)$예요. MAP라는 한 점과 달리 모수 전체의 불확실성을 담아요.이 문제에서는 우도와 prior를 결합해 최적화 대상을 만들어요.
- **최대사후 추정 (maximum a posteriori·MAP)** — 데이터를 본 뒤 모수의 사후밀도가 가장 높은 점을 고르는 방법이에요.$\hat\theta_{\mathrm{MAP}}=\arg\max_\theta p(\theta\mid D)$예요. prior와 likelihood가 함께 들어가요.이 문제에서는 사후밀도가 가장 큰 모수를 구해요.
- **Ridge·L2 벌점 (ridge regularization)** — 제곱오차에 모수의 제곱 크기 벌점을 더해 해를 고르는 방법이에요.$\|y-\Phi\theta\|^2+\lambda\|\theta\|^2$에서 $\lambda>0$가 벌점의 세기예요. 이 자료의 해당 문항은 절편에도 벌점을 적용해요.이 문제에서는 분산 비율이 제곱거리 벌점의 세기로 나타나요.
- **양의 준정부호 (positive semidefinite)** — 실수 대칭행렬의 이차형식이 어느 방향에서도 음수가 되지 않는 성질이에요.모든 $z$에 대해 $z^\top Az\ge0$예요. 값이 0인 방향이 있을 수 있어 가역을 보장하지 않아요.이 문제에서는 특징행렬이 열종속이어도 Gram 행렬이 갖는 성질이에요.
- **양의 정부호 (positive definite)** — 실수 대칭행렬이 0이 아닌 모든 방향에 양의 이차형식 값을 주는 성질이에요.$z\ne0\Rightarrow z^\top Az>0$예요. 대칭인 양의 정부호 행렬은 가역이에요.이 문제에서는 양의 벌점을 더했을 때 해가 유일해지는 이유예요.

---

<a id="p8"></a>

### 8. 사후분포와 새 관측의 예측

EXAM Problem 8 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p8)

#### 주어진 조건

스칼라 회귀모델 $y_n=x_n\theta+\epsilon_n$에서 $\theta\sim\mathcal N(1,2)$, 독립 잡음 $\epsilon_n\sim\mathcal N(0,2)$이다. 잡음들은 $\theta$와도 독립이다. 데이터 $D=\{(1,2),(1,0)\}$가 관측되었다. 모든 Gaussian의 둘째 인수는 분산이다.

새 입력은 $x_*=2$이고, $f_*=x_*\theta$, $y_*=f_*+\epsilon_*$이다. $\epsilon_*\sim\mathcal N(0,2)$는 $\theta,D$ 및 기존 잡음과 독립이다.

#### 구할 것

1. 독립성을 이용해 likelihood와 prior의 곱을 쓰고, $\theta$와 무관한 양의 인자를 제외한 지수식을 구하라.
2. 소문항 (a)의 지수를 $-\tfrac12(A\theta^2-2b\theta+c)$로 모아 $A,b,c$를 구하라.
3. 소문항 (b)를 완전제곱하고 적분값이1이 되도록 정규화하여 posterior 평균·분산과 밀도를 도출하라.
4. 소문항 (c)의 분포에서 $f_*=x_*\theta$의 평균·분산과 분포를 도출하라.
5. 소문항 (d)에 독립 미래 잡음을 더해 $y_*$의 사후예측 평균·분산과 분포를 도출하라.
6. 소문항 (c)의 MAP 값을 구하고 그 값에 모수를 고정한 관측 예측분포를 (e)와 비교하라. 분산 차이는 어디서 오는가?

#### 문제를 내 말로 읽어요

사후분포와 새 관측의 예측: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 Gaussian posterior와 사후예측분포에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

Gaussian prior와 Gaussian likelihood를 곱하면 사후분포도 Gaussian이에요. 분산의 역수인 precision을 모으면 $S_N^{-1}=S_0^{-1}+\sigma^{-2}\sum x_n^2$, $m_N=S_N(S_0^{-1}m_0+\sigma^{-2}\sum x_ny_n)$예요. 새 잡음이 독립일 때 $\operatorname{Var}(y_*\mid D)=x_*^2S_N+\sigma^2$예요. 잠재 함수 $f_*$에는 마지막 잡음항이 없어요.

#### 종이에 쓸 첫 줄

$g(\theta)=p(\theta)p(2\mid\theta)p(0\mid\theta)$부터 적어요. 이 곱의 지수를 전개한 뒤 완전제곱해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

여기서 $\theta$는 벡터가 아니라 스칼라 계수예요. 관측은 $(x_1,y_1)=(1,2)$, $(x_2,y_2)=(1,0)$이고 모형은 $y_n=x_n\theta+\epsilon_n$이에요. 입력이 둘 다 1이므로 각 조건부 평균은 $\theta$예요. 두 출력값을 평균이나 prior 평균과 혼동하지 않아요.

Prior와 두 관측의 조건부 밀도를 곱해 정규화 전의 함수를 만들어요.

$$
g(\theta)=\mathcal N(\theta\mid1,2)\mathcal N(2\mid\theta,2)\mathcal N(0\mid\theta,2).
$$

세 분산은 모두 2라서 일반 Gaussian 지수의 분모 $2v$가 $2\cdot2=4$예요. 각각의 앞 계수는 $1/\sqrt{4\pi}$이므로 정확한 곱은

$$
g(\theta)=(4\pi)^{-3/2}\exp\!\left[-\frac{(\theta-1)^2+(2-\theta)^2+\theta^2}{4}\right].
$$

모양만 비교할 때는 $\theta$와 무관한 앞 계수를 생략해 비례 기호를 쓸 수 있어요. 두 likelihood를 곱한 근거는 $\theta$와 입력이 주어졌을 때 관측 잡음이 독립이라는 조건이에요. $g$의 적분은 아직 1이라고 가정하지 않아요.

#### (b)

(a)의 제곱항을 각각 펼쳐요. $(\theta-1)^2=\theta^2-2\theta+1$, $(2-\theta)^2=\theta^2-4\theta+4$, 마지막은 $\theta^2$이에요. 따라서 합은 $3\theta^2-6\theta+5$예요.

문제가 요구한 $-\frac12(A\theta^2-2b\theta+c)$와 비교하려면 바깥의 $-1/2$를 먼저 맞춰야 해요.

$$
-\frac{3\theta^2-6\theta+5}{4}=-\frac12\left(\frac32\theta^2-3\theta+\frac52\right).
$$

이차항에서 $A=3/2$, 일차항에서 $-2b=-3$이므로 $b=3/2$, 상수항에서 $c=5/2$예요. 여기의 $b$는 이차식을 정리하기 위한 계수로, 앞 문항에서 사전분산을 표시한 $b^2$와는 다른 역할이에요. $A$가 정밀도 역할을 하는 것도 바깥의 $-1/2$까지 맞췄기 때문이에요.

#### (c)

(b)의 이차식을 평균 중심의 제곱으로 바꿔요.

$$
A\theta^2-2b\theta+c=\frac32(\theta^2-2\theta)+\frac52,
$$

$$
=\frac32\big[(\theta-1)^2-1\big]+\frac52=\frac32(\theta-1)^2+1.
$$

따라서 전체 지수는 $-\frac34(\theta-1)^2-\frac12$예요. 상수 $e^{-1/2}$는 정규화할 때 앞 계수와 함께 나누어지므로 모양은 $e^{-3(\theta-1)^2/4}$예요. 일반식 $e^{-(\theta-\mu)^2/(2v)}$와 비교해 $\mu=1$, $1/(2v)=3/4$를 얻어요. 역수를 취하면 $2v=4/3$이므로 $v=2/3$이에요.

정규화된 밀도의 앞 계수도 계산해요.

$$
\frac1{\sqrt{2\pi v}}=\frac1{\sqrt{2\pi\cdot2/3}}=\frac1{\sqrt{4\pi/3}}=\sqrt{\frac3{4\pi}}.
$$

그러므로 $p(\theta\mid D)=\sqrt{3/(4\pi)}\exp[-3(\theta-1)^2/4]$이고 $\theta\mid D\sim\mathcal N(1,2/3)$예요. 적분 $\int e^{-3(\theta-1)^2/4}d\theta=\sqrt{4\pi/3}$과 앞 계수를 곱하면 1이 되어 정규화도 확인돼요. 사후 정밀도 $3/2$는 prior의 $1/2$와 두 관측의 $1/2+1/2$를 더한 값이에요.

#### (d)

$f_*=2\theta$이므로 **상수배의 평균·분산 공식**을 바로 적용하면 돼요.
$$
E[aX]=aE[X],\qquad \operatorname{Var}(aX)=a^2\operatorname{Var}(X).
$$
(c)에서 구한 사후분포는 $\theta\mid D\sim\mathcal N(1,2/3)$이므로
$$
E[f_*\mid D]=2E[\theta\mid D]=2\cdot1=2.
$$
$$
\operatorname{Var}(f_*\mid D)=2^2\operatorname{Var}(\theta\mid D)=4\cdot\frac23=\frac83.
$$
Gaussian의 상수배도 Gaussian이므로
$$
\boxed{f_*\mid D\sim\mathcal N(2,8/3)}.
$$
여기서는 **사후분산 $2/3$**을 사용하며, 새 관측 잡음은 (e)에서 더해요.

#### (e)

$y_*=f_*+\epsilon_*$이고 새 잡음은 $f_*$와 독립인 $\mathcal N(0,2)$예요. 독립인 두 확률변수의 합은 평균과 분산을 각각 더하면 돼요.

$$
E[y_*\mid D]=2+0=2,\qquad\operatorname{Var}(y_*\mid D)=\frac83+2=\frac{14}3.
$$

독립 Gaussian의 합도 Gaussian이므로 $y_*\mid D\sim\mathcal N(2,14/3)$예요.

#### (f)

(c)의 사후분포는 Gaussian이므로 MAP는 사후평균과 같아 $\theta_{\mathrm{MAP}}=1$이에요. 이를 고정 대입하면

$$
y_*=2\theta_{\mathrm{MAP}}+\epsilon_*=2+\epsilon_*\sim\mathcal N(2,2).
$$

(e)와 예측평균은 같지만, 모수 불확실성을 제외했으므로 분산은 $8/3$ 작아요.

#### 완성 답과 검산

#### (a) 검산

$\theta$가 주어진 조건에서 두 관측의 잡음이 독립인지 확인해요.

#### (b) 검산

$\theta=0$을 넣으면 전개 전후 지수 모두 $-5/4$예요. 이차·일차 계수도 각각 일치해요.

#### (c) 검산

완전제곱을 다시 전개하면 원래 이차식이에요. $\sqrt{3/(4\pi)}\int e^{-3(\theta-1)^2/4}d\theta=1$이에요.

#### (d) 검산

$f_*=2\theta$를 직접 중심화하면 $f_*-2=2(\theta-1)$여서 분산은 $4(2/3)$이에요.

#### (e) 검산

전체분산법칙으로도 $E[2\mid D]+\operatorname{Var}(2\theta\mid D)=2+8/3$이에요.

#### (f) 검산

$14/3-2=8/3$으로 (d)의 잠재 분산과 정확히 같아요.

#### 여기서 헷갈리기 쉬워요

prior 분산 2를 precision 2로 쓰지 않아요. $x_*=2$를 분산에 곱할 때는 제곱해서 4를 곱해요. 새 관측 $y_*$와 잡음 없는 함수 $f_*$를 구분해요.

#### 설명을 닫고 다시 풀어요

- 세 Gaussian 인자의 평균·분산과 지수 분모 4의 이유를 말해요.
- 제곱 전개·완전제곱·계수 비교로 사후분산을 다시 구해요.
- 잠재값·새 관측·MAP 고정 대입의 세 분산을 구별해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\theta\mid D\sim\mathcal N(1,2/3)$. 잠재분산 $8/3$, 관측분산 $14/3$. MAP 고정 예측은 $\mathcal N(2,2)$.

#### 적용 조건

서로 독립 잡음, prior와 독립; 새 잡음도 독립; 분산 표기

#### 출제 근거

출제 근거: MML 9.3.3-9.3.4 theory application. MML PDF 312, 314, 315쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **사전분포 (prior)** — 현재 데이터를 보기 전에 모수의 가능성을 표현한 분포예요.$p(\theta)$ 또는 $p(\theta\mid M)$로 써요. Gaussian prior의 평균 $m_0$는 중심, 공분산 $S_0$는 퍼짐이에요.이 문제에서는 관측 전 모수의 중심과 퍼짐을 넣어요.
- **우도 (likelihood)** — 관측한 데이터는 고정하고 모수를 바꾸어 보며 평가하는 데이터 밀도예요.$L(\theta)=p(y\mid\theta,X)$예요. 같은 식이라도 $\theta$에 대한 정규화된 확률분포라고 가정하면 안 돼요.이 문제에서는 모수에 따라 두 관측을 설명하는 밀도를 만들어요.
- **정밀도 (precision)** — 분산의 역수 또는 공분산 행렬의 역행렬이에요. 퍼짐이 작을수록 정밀도가 커져요.스칼라에서는 $v^{-1}$, 다변량에서는 $S^{-1}$예요. 행렬인 경우 공분산이 가역이어야 해요.이 문제에서는 관측과 prior의 제곱항 계수를 모아요.
- **완전제곱 (completing the square)** — 이차식에서 중심을 묶어 제곱항과 상수항으로 나누는 변형이에요.$az^2-2bz=a(z-b/a)^2-b^2/a$예요. Gaussian의 중심과 분산을 읽을 때는 $a>0$이어야 해요.이 문제에서는 곱을 정규화된 사후밀도로 바꾸어요.
- **사후분포 (posterior)** — 데이터를 반영해 갱신한 모수의 분포예요.$p(\theta\mid D)\propto p(D\mid\theta)p(\theta)$예요. MAP라는 한 점과 달리 모수 전체의 불확실성을 담아요.이 문제에서는 예측에 전달할 모수의 평균과 분산을 담아요.
- **잠재 함수값 (latent function value)** — 관측 잡음을 더하기 전 모형이 나타내는 함수값이에요.$f_*=\phi(x_*)^\top\theta$이고 관측은 $y_*=f_*+\epsilon_*$예요. 두 값의 예측 분산을 구별해요.이 문제에서는 새 관측 잡음을 더하기 전 분산을 구해요.
- **사후예측분포 (posterior predictive)** — 모수의 사후 불확실성을 평균내어 새 관측의 분포를 구한 것이에요.$p(y_*\mid D)=\int p(y_*\mid\theta)p(\theta\mid D)\,d\theta$예요. 새 입력 등 고정 조건은 표기에서 생략했어요.이 문제에서는 모수 불확실성과 새 잡음을 함께 반영해요.
- **점 추정 대입 (plug-in prediction)** — 모수의 전체 분포 대신 추정한 한 점을 모형에 넣어 예측하는 방법이에요.$p(y_*\mid\hat\theta)$처럼 써요. 이 방식은 모수 자체의 사후 불확실성을 적분하지 않아요.이 문제에서는 모수를 한 점으로 고정한 예측과 비교해요.

---

<a id="p9"></a>

### 9. Evidence·Bayes factor·모델 선택

EXAM Problem 9 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p9)

#### 주어진 조건

두 모델은 $y=\theta+\epsilon$, $\epsilon\sim\mathcal N(0,1)$을 공유하며 $\epsilon$은 $\theta$와 독립이다. $M_1$은 $\theta\sim\mathcal N(0,1)$, $M_2$는 $\theta\sim\mathcal N(0,4)$를 쓴다. 모델 사전확률은 $P(M_1)=1/3$, $P(M_2)=2/3$이다. 관측은 하나이며 $y=0$이다. Gaussian의 둘째 인수는 분산이다.

#### 구할 것

1. 모델 $M_j$의 prior 분산을 $v_j$로 두고, $p(y\mid M_j)$를 $\theta$에 대한 적분으로 써라. 적분하는 분포가 posterior가 아닌 prior인 이유를 설명하라.
2. 소문항 (a)의 Gaussian 곱에서 지수의 $\theta$ 항을 완전제곱하라. 적분을 계산하여 임의의 $y$에 대한 evidence 밀도를 $v_j$로 표현하라.
3. 소문항 (b)에 $v_1=1,v_2=4$와 관측 $y=0$을 대입해 두 evidence를 정규화 상수까지 계산하라.
4. 소문항 (c)의 비로 Bayes factor $B_{12}$를 구하고 데이터가 어느 모델을 지지하는지 판단하라.
5. Bayes 정리의 두 모델 posterior를 나누어 posterior odds 공식을 유도하라. (d)와 모델 prior를 사용해 $P(M_1\mid y=0)$ 및 선택할 모델을 구하라.

#### 문제를 내 말로 읽어요

Evidence·Bayes factor·모델 선택: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 Gaussian evidence와 posterior odds에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

Evidence(주변우도)는 아직 특정 계수를 고르기 전 모델이 데이터에 부여하는 밀도예요. 그래서 $p(\theta\mid M)$라는 prior로 우도를 평균내요. 독립 Gaussian의 합은 평균과 분산을 각각 더해요. Bayes factor는 evidence 비이고 posterior odds는 prior odds×Bayes factor예요. 연속 관측의 evidence 값은 점의 확률이 아닌 밀도값이에요.

#### 종이에 쓸 첫 줄

$p(y\mid M_j)=\int p(y\mid\theta,M_j)p(\theta\mid M_j)d\theta$를 적고 두 Gaussian 밀도를 대입해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$M_1,M_2$는 모형의 이름이고 $j$는 그 번호예요. 이 문항에서 $\theta,y$는 모두 스칼라예요. $v_j$는 모형 $M_j$ 아래 모수의 사전분산이고, 관측 잡음의 분산은 별도로 1이에요.

Evidence는 ‘계수를 어느 값으로 정했을 때’의 적합도가 아니라 ‘이 모형의 prior에서 가능한 모든 계수를 고려했을 때’의 관측 밀도예요. 우도에 prior를 가중치로 곱해 적분해요.

$$
p(y\mid M_j)=\int_{-\infty}^{\infty}\mathcal N(y\mid\theta,1)\mathcal N(\theta\mid0,v_j)\,d\theta.
$$

적분 중에는 $y$를 고정하고 $\theta$를 움직여요. 적분이 끝나면 $\theta$는 사라지고 $y$의 함수가 남아요. 이를 모수의 주변화라고 해요. Prior 대신 posterior를 넣으면 이미 데이터를 반영한 다른 양을 계산하게 돼요. 최적의 한 계수만 골라 우도를 계산하는 ML과도 다른 연산이에요.

#### (b)

두 Gaussian의 일반식을 대입하면 앞 계수는 $1/(\sqrt{2\pi}\sqrt{2\pi v_j})=1/(2\pi\sqrt{v_j})$예요. 지수 안의 제곱합을 먼저 전개해요.

$$
(y-\theta)^2+\frac{\theta^2}{v_j}=\left(1+\frac1{v_j}\right)\theta^2-2y\theta+y^2.
$$

$A=1+1/v_j>0$로 두면 완전제곱은 $A(\theta-y/A)^2+y^2-y^2/A$예요. $1/A=v_j/(1+v_j)$이므로 남은 상수는 $y^2(1-v_j/(1+v_j))=y^2/(1+v_j)$예요.

$$
p(y\mid M_j)=\frac{e^{-y^2/[2(1+v_j)]}}{2\pi\sqrt{v_j}}\int e^{-A(\theta-y/A)^2/2}\,d\theta.
$$

적분 안은 분산 $1/A$인 Gaussian에서 앞 계수를 뺀 모양이에요. 정규화된 밀도의 적분이 1이므로 이 적분은 $\sqrt{2\pi/A}$예요. 따라서 앞 계수까지 정리하면

$$
\frac1{2\pi\sqrt{v_j}}\sqrt{\frac{2\pi}{A}}=\frac1{\sqrt{2\pi v_jA}}=\frac1{\sqrt{2\pi(1+v_j)}}.
$$

결국 $p(y\mid M_j)=\frac1{\sqrt{2\pi(1+v_j)}}e^{-y^2/[2(1+v_j)]}$이며 $y\mid M_j\sim\mathcal N(0,1+v_j)$예요. Evidence에서는 모형에 따라 앞 계수가 달라지므로 지수 모양만 남기면 안 돼요.

#### (c)

이제 $v_1=1$, $v_2=4$를 (b)에 넣어요. 관측의 분산은 prior 분산과 잡음분산을 더한 $1+v_1=2$, $1+v_2=5$예요. $y=0$이면 $e^{-0^2/[2(1+v_j)]}=1$이라 앞 계수만 남아요.

$$
p(0\mid M_1)=\frac1{\sqrt{2\pi\cdot2}}=\frac1{\sqrt{4\pi}},
$$

$$
p(0\mid M_2)=\frac1{\sqrt{2\pi\cdot5}}=\frac1{\sqrt{10\pi}}.
$$

이 수치는 $P(y=0\mid M_j)$라는 한 점의 확률이 아니라 0에서 평가한 확률밀도예요. 연속분포에서 정확히 한 점의 확률은 0이며, 구간의 확률은 밀도를 적분해 구해요. 여기서는 같은 관측값에서 두 모형의 밀도를 비교해요.

#### (d)

Bayes factor는 두 evidence의 비예요.

$$
B_{12}=\frac{p(0\mid M_1)}{p(0\mid M_2)}=\frac{1/\sqrt{4\pi}}{1/\sqrt{10\pi}}=\sqrt{\frac52}>1.
$$

따라서 데이터는 $M_1$을 더 지지해요. 모델 사전확률은 아직 반영하지 않았으며, 최종 사후확률 비교는 (e)에서 해요.

#### (e)

모형 prior $P(M_1)=1/3$, $P(M_2)=2/3$는 ‘어느 모형인가’의 확률이에요. 모수 prior $p(\theta\mid M_j)$와 대상이 달라요. Bayes 정리에서 두 모형의 공통 분모 $p(y)$를 나누어 소거하면

$$
\frac{P(M_1\mid y)}{P(M_2\mid y)}=B_{12}\frac{P(M_1)}{P(M_2)}.
$$

Prior odds는 $(1/3)/(2/3)=1/2$예요. 따라서 posterior odds $O=\sqrt{5/2}/2\approx0.79057<1$이에요. 데이터는 $M_1$ 쪽으로 비율을 올렸지만 시작 비율이 $1/2$였으므로 사후에도 $M_2$의 확률이 더 커요.

오즈 $O$는 확률 자체가 아니에요. $p=P(M_1\mid0)$라 두면 두 모형뿐이므로 $P(M_2\mid0)=1-p$이고 $O=p/(1-p)$예요. 이를 풀면 $p=O/(1+O)$예요.

$$
P(M_1\mid0)=\frac{\sqrt{5/2}}{2+\sqrt{5/2}}\approx0.44152.
$$

나머지 $P(M_2\mid0)\approx0.55848$이므로 사후확률이 큰 모형을 고르면 $M_2$예요. Bayes factor와 최종 사후 선택이 서로 다른 단계를 답한다는 점을 확인해요.

#### 완성 답과 검산

#### (a) 검산

적분 변수 $\theta$를 없애면 evidence는 $y$의 밀도예요.

#### (b) 검산

평균0인 독립 $\theta+\epsilon$의 분산도 $v_j+1$이에요. 유도한 밀도의 적분이1이고 평균·분산도 일치해요.

#### (c) 검산

$y=0$에서 더 작은 분산의 Gaussian 높이가 더 커요.

#### (d) 검산

정규화 상수를 빼면 이 관측에서 지수가 모두0이어서 두 모델이 같다는 오답을 얻어요.

#### (e) 검산

$O/(1+O)+(1/(1+O))=1$이고 $O<1$이에요. 데이터의 지지와 최종 모델 선택을 구별해요.

#### 여기서 헷갈리기 쉬워요

Bayes factor가 1보다 크다고 곧바로 $M_1$의 사후확률이 더 크다고 결론 내리지 않아요. prior odds를 반드시 곱해요. Evidence와 사후예측은 둘 다 적분이지만 평균내는 계수 분포가 달라요.

#### 설명을 닫고 다시 풀어요

- prior로 적분하는 이유와 사라지는 변수를 말해요.
- 완전제곱 뒤 남은 상수와 앞 계수까지 정리해 evidence를 구해요.
- Bayes factor에 prior odds를 곱한 뒤 오즈를 확률로 바꿔요.

**페이지 요약**

#### 떠올릴 개념·공식

evidence: prior 평균. $B_{12}=\sqrt{5/2}$, posterior odds $=\sqrt{10}/4$. 사후 선택 $M_2$.

#### 적용 조건

두 모델 prior probability 명시; evidence는 prior로 적분

#### 출제 근거

출제 근거: Lecture04 s17 and MML 9.3.3 theory application. MML PDF 312, 319쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **주변우도·Evidence (marginal likelihood)** — 모형의 prior 아래에서 모수를 적분해 얻는 관측 데이터의 밀도예요.$p(y\mid M)=\int p(y\mid\theta,M)p(\theta\mid M)\,d\theta$예요. 연속 데이터에서는 확률이 아닌 밀도값이에요.이 문제에서는 모형별 prior를 사용해 관측 밀도를 구해요.
- **주변화 (marginalization)** — 관심 밖 변수를 적분하거나 합해서 분포에서 없애는 연산이에요.$p(y)=\int p(y,\theta)\,d\theta$예요. Evidence는 prior를, 사후예측은 posterior를 사용해 평균내요.이 문제에서는 모수를 특정 값으로 최적화하지 않고 적분해요.
- **Bayes factor** — 데이터가 두 모형 중 어느 쪽을 상대적으로 더 지지하는지 나타내는 evidence의 비예요.$B_{12}=p(y\mid M_1)/p(y\mid M_2)$예요. $B_{12}>1$이면 이 비의 분자 모형을 더 지지해요.이 문제에서는 같은 관측에 대한 두 evidence의 방향을 비교해요.
- **사전·사후 오즈 (prior·posterior odds)** — 두 모형의 확률을 같은 순서로 나눈 비예요.$O_{12}^{\rm prior}=p(M_1)/p(M_2)$, $O_{12}^{\rm post}=p(M_1\mid y)/p(M_2\mid y)$예요. $O_{12}^{\rm post}=B_{12}O_{12}^{\rm prior}$예요.이 문제에서는 데이터의 지지와 모델 prior를 결합해요.
- **확률밀도 (probability density)** — 연속 확률변수가 어떤 값 주변에 얼마나 집중되는지 나타내는 함수예요. 한 점의 확률과는 달라요.$P(a\le X\le b)=\int_a^b p(x)\,dx$예요. 밀도값 자체는 1보다 클 수도 있어요.이 문제에서는 관측 한 점에서 계산한 evidence 수치의 의미를 구별해요.

---

<a id="p10"></a>

### 10. 최소제곱 해를 직교투영으로 읽기

EXAM Problem 10 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p10)

#### 주어진 조건

동일한 알려진 분산의 독립 Gaussian 잡음을 갖는 $y=\Phi\theta+\epsilon$에서

$$
\Phi=\begin{pmatrix}1&0\\1&1\\1&-1\end{pmatrix},\quad y=\begin{pmatrix}2\\2\\0\end{pmatrix}.
$$

$\Phi$의 열들은 선형독립이며 내적은 유클리드 내적이다. $\widehat y=\Phi\widehat\theta$, $r=y-\widehat y$로 둔다.

#### 구할 것

1. $\widehat y=\Phi\widehat\theta$가 최근접점이라고 하자. 임의의 계수 변화 $h$에 대해 $t=0$에서 $\|y-\Phi(\widehat\theta+th)\|^2$의 도함수가0임을 이용해 잔차 직교 조건을 도출하라.
2. 소문항 (a)에 $r=y-\Phi\widehat\theta$를 넣어 정규방정식과 일반적인 최소제곱 추정식을 도출하라.
3. 소문항 (b)를 $\widehat y=\Phi\widehat\theta$에 대입하여 $\widehat y=Py$가 되는 행렬 $P$를 도출하라. 차원·대칭성·멱등성을 보여라.
4. 주어진 수치에서 (b), (c)를 사용해 $\widehat\theta$, $P$, $\widehat y$, $r$를 계산하고 $\Phi^\top r=0$을 확인하라.
5. 임의의 $u\in\operatorname{col}(\Phi)$에 대해 (a)의 직교성을 이용해 $\|y-u\|^2$를 두 제곱거리의 합으로 분해하라. 이로부터 최근접점이라는 결론을 완성하라.

#### 문제를 내 말로 읽어요

최소제곱 해를 직교투영으로 읽기: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 최소제곱 추정식과 직교투영행렬에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

직교 조건은 열마다 $\phi_k^\top r=0$이므로 모아서 $\Phi^\top r=0$이에요. 열독립이면 $G=\Phi^\top\Phi$가 가역이고 $P=\Phi G^{-1}\Phi^\top$가 투영행렬이에요. 직교투영은 대칭·멱등을 만족해요. 마지막 최소거리 주장은 직교벡터의 제곱노름이 더해지는 피타고라스 성질로 보여요.

#### 종이에 쓸 첫 줄

$r=y-\Phi\widehat\theta$와 $\|r-t\Phi h\|^2$를 적고, $t$에 대한 미분부터 시작해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$\theta$는 계수공간 $\mathbb R^K$의 벡터이고, $\Phi\theta$는 예측공간 $\mathbb R^N$의 벡터예요. 수치 예에서는 $K=2,N=3$이므로 두 공간의 차원이 달라요. $\widehat\theta$는 최소점 후보, $h\in\mathbb R^K$는 계수를 움직일 방향, $t\in\mathbb R$는 그 방향으로 움직일 양이에요.

계수를 $\widehat\theta+th$로 바꾸면 예측은 $\Phi\widehat\theta+t\Phi h$가 돼요. $r=y-\Phi\widehat\theta$라 두면 새로운 잔차는 $r-t\Phi h$예요. 거리제곱을 전개하면

$$
F(t)=\|r\|^2-2t h^\top\Phi^\top r+t^2\|\Phi h\|^2.
$$

최소점에서 어떤 방향으로도 일차적으로 줄어들 수 없으므로 모든 $h$에 대해 $F'(0)=-2h^\top\Phi^\top r=0$이어야 해요. $a=\Phi^\top r$라 두고 $h=a$도 선택할 수 있으므로 $a^\top a=0$, 따라서 $a=0$이에요.

$$
\Phi^\top r=0.
$$

이 식의 각 성분은 ‘특징행렬의 한 열과 잔차의 내적이 0’이라는 뜻이에요. 그러므로 잔차는 열공간 전체에 직교해요. 지금은 최소점의 필요조건을 얻었고 (e)에서 충분성도 확인해요.

#### (b)

(a)의 직교조건에 잔차 정의를 대입해요.

$$
\Phi^\top(y-\Phi\widehat\theta)=0\quad\Rightarrow\quad\Phi^\top\Phi\widehat\theta=\Phi^\top y.
$$

이것이 정규방정식이에요. 왼쪽에서 $N$차원의 잔차를 $K$개의 열과 내적하여 계수공간의 조건 $K$개로 바꾼 셈이에요. $G=\Phi^\top\Phi$는 $K\times K$이고, 주어진 열독립 조건에서 비영 $v$에 대해 $v^\top Gv=\|\Phi v\|^2>0$이므로 가역이에요.

양변 왼쪽에 $G^{-1}$를 곱하면 $G^{-1}G=I_K$이므로

$$
\widehat\theta=(\Phi^\top\Phi)^{-1}\Phi^\top y.
$$

여기서 직사각형 $\Phi$ 자체를 역행렬로 ‘나눈’ 것이 아니에요. 역행렬을 취한 대상은 열독립으로 가역성이 확인된 정사각 Gram 행렬이에요. 곱 순서는 $(K\times K)(K\times N)(N\times1)$이에요.

#### (c)

(b)의 결과는 계수이고, 열공간 위의 점을 얻으려면 앞에 $\Phi$를 한 번 더 곱해야 해요.

$$
\widehat y=\Phi\widehat\theta=\Phi G^{-1}\Phi^\top y=Py,\qquad P=\Phi G^{-1}\Phi^\top.
$$

계수 추정 행렬 $G^{-1}\Phi^\top$는 $K\times N$으로 관측을 계수로 옮겨요. 투영행렬 $P$는 $N\times N$으로 관측을 같은 관측공간 안의 예측벡터로 옮겨요. 수치 예에서는 각각 $2\times3$, $3\times3$이에요.

전치는 곱 순서를 뒤집어요. $G^\top=G$이면 $(G^{-1})^\top=(G^\top)^{-1}=G^{-1}$이므로

$$
P^\top=(\Phi G^{-1}\Phi^\top)^\top=\Phi G^{-1}\Phi^\top=P.
$$

또한 두 $P$ 사이의 $\Phi^\top\Phi$를 $G$로 묶으면

$$
P^2=\Phi G^{-1}(\Phi^\top\Phi)G^{-1}\Phi^\top=\Phi G^{-1}GG^{-1}\Phi^\top=P.
$$

대칭성은 유클리드 직교투영의 성질이고, 멱등성은 이미 투영한 점을 다시 투영해도 그대로라는 뜻이에요. 실제로 $P\Phi=\Phi$라 열공간의 모든 점이 고정돼요.

#### (d)

주어진 $\Phi$의 열은 $(1,1,1)^\top$, $(0,1,-1)^\top$이고 $y=(2,2,0)^\top$예요. 각 열의 제곱합과 내적을 계산하면

$$
G=\begin{pmatrix}1+1+1&0+1-1\\0+1-1&0+1+1\end{pmatrix}=\begin{pmatrix}3&0\\0&2\end{pmatrix},
$$

$$
\Phi^\top y=\begin{pmatrix}2+2+0\\0\cdot2+1\cdot2-1\cdot0\end{pmatrix}=\begin{pmatrix}4\\2\end{pmatrix}.
$$

$G^{-1}=\operatorname{diag}(1/3,1/2)$를 곱하면 $\widehat\theta=(4/3,1)^\top$예요. 투영행렬은 열의 외적으로도 계산할 수 있어요. $a=(1,1,1)^\top$, $b=(0,1,-1)^\top$라 두면 $P=\frac13aa^\top+\frac12bb^\top$예요. 예를 들어 $P_{22}=1/3+1/2=5/6$, $P_{23}=1/3-1/2=-1/6$이에요. 전체는

$$
P=\frac16\begin{pmatrix}2&2&2\\2&5&-1\\2&-1&5\end{pmatrix}.
$$

계수를 각 행에 넣으면 예측은 $\widehat y=(4/3,4/3+1,4/3-1)^\top=(4/3,7/3,1/3)^\top$이에요. 잔차는 각 관측에서 이를 빼서 $r=(2/3,-1/3,-1/3)^\top$예요. 따라서 $\mathrm{SSE}=(2/3)^2+(-1/3)^2+(-1/3)^2=6/9=2/3$이에요.

직교도 직접 확인해요. 첫 열과의 내적은 $2/3-1/3-1/3=0$, 둘째 열과의 내적은 $0-1/3+1/3=0$이므로 $\Phi^\top r=0$이에요.

#### (e)

열공간의 임의의 다른 점을 $u=\Phi\beta$로 두어요. 예측 $\widehat y=\Phi\widehat\theta$와의 차이는 $\widehat y-u=\Phi(\widehat\theta-\beta)$라 역시 열공간 안에 있어요. (a)의 잔차는 그 공간에 직교하므로

$$
r^\top(\widehat y-u)=(\Phi^\top r)^\top(\widehat\theta-\beta)=0.
$$

$y-u=(y-\widehat y)+(\widehat y-u)=r+(\widehat y-u)$로 나누고 노름을 제곱해요. 일반적으로는 교차항 $2r^\top(\widehat y-u)$가 있지만 방금 확인한 직교성 때문에 사라져요.

$$
\|y-u\|^2=\|r\|^2+\|\widehat y-u\|^2\ge\|r\|^2.
$$

제곱노름은 음수가 될 수 없으므로 어떤 $u$도 $\widehat y$보다 가까울 수 없어요. 등호는 $\|\widehat y-u\|^2=0$, 즉 $u=\widehat y$일 때만 성립하므로 최근접 예측점은 유일해요. 수치 예에서 최소 거리제곱은 (d)의 $2/3$이에요. 이 기하학적 논증은 임의의 $u$ 전체에 적용되므로 몇 점을 대입한 확인보다 강한 최소성 증명이에요. 계수의 유일성까지 얻는 데에는 열독립 조건을 함께 사용해요.

#### 완성 답과 검산

#### (a) 검산

$h$를 각 좌표 기저로 택하면 각 열과 잔차의 내적이0임을 개별 확인할 수 있어요.

#### (b) 검산

$G$의 비영 이차형식은 $\|\Phi v\|^2>0$이어서 역행렬 조건을 만족해요.

#### (c) 검산

$P\Phi=\Phi$이므로 열공간의 점은 다시 투영해도 움직이지 않아요.

#### (d) 검산

$Py=(4/3,7/3,1/3)^\top$이며 예측과 잔차 합이 원래 $y$예요. SSE는 $2/3$이에요.

#### (e) 검산

$u=\widehat y$를 대입하면 둘째 항은0이에요. 그 외에는 양수라 더 멀어요.

#### 여기서 헷갈리기 쉬워요

$P$를 계수 추정 행렬 $(\Phi^\top\Phi)^{-1}\Phi^\top$와 혼동하지 않아요. 전자는 $3\times3$, 후자는 $2\times3$이에요. 이 공식은 열독립 가정 아래에서 사용해요.

#### 설명을 닫고 다시 풀어요

- 계수와 예측의 공간을 구분하고 h와 t의 역할을 말해요.
- 모든 h에서 방향 미분이 0이면 직교조건을 얻는 이유를 증명해요.
- 투영행렬의 대칭·멱등성과 임의 u에 대한 최소거리 논증을 다시 써요.

**페이지 요약**

#### 떠올릴 개념·공식

$\Phi^\top r=0$, $P=\Phi(\Phi^\top\Phi)^{-1}\Phi^\top$, $P^\top=P^2=P$. 최소 잔차제곱 $2/3$.

#### 적용 조건

Φ full column rank; 유클리드 내적, 알려진 동일 Gaussian 잡음분산

#### 출제 근거

출제 근거: MML 3.8,9.4 theory application. MML PDF 87, 88, 89, 319, 320쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 해설에 쓰인 용어

- **잔차제곱합 (sum of squared errors·SSE)** — 관측값과 모형 예측의 차이를 제곱해서 모두 더한 값이에요.$\operatorname{SSE}=\sum_n(y_n-\hat y_n)^2=\|y-\hat y\|^2$예요. 합과 평균은 $N$배 차이가 있어요.이 문제에서는 열공간 안에서 관측과의 거리를 최소화해요.
- **잔차 (residual)** — 관측벡터에서 예측벡터를 뺀 차이예요.$r=y-\hat y$예요. 일반적인 최소제곱 해에서는 $\Phi^\top r=0$이지만 벌점이 들어간 해에서는 이 조건이 달라질 수 있어요.이 문제에서는 방향에 대한 거리 미분에서 직교 조건을 얻어요.
- **정규방정식 (normal equations)** — 최소제곱 목적함수를 미분해 얻는 선형 방정식이에요.$\Phi^\top\Phi\theta=\Phi^\top y$예요. 유일한 해를 역행렬로 쓰려면 $\Phi$의 열독립 조건이 필요해요.이 문제에서는 열마다의 직교 조건을 하나의 식으로 모아요.
- **직교투영 (orthogonal projection)** — 벡터를 부분공간 위의 가장 가까운 벡터로 옮기는 연산이에요.$\hat y\in\operatorname{col}(\Phi)$이고 $r=y-\hat y$가 그 공간의 모든 벡터에 직교해요.이 문제에서는 최소제곱 예측벡터의 기하학적 의미예요.
- **대칭행렬 (symmetric matrix)** — 전치해도 변하지 않는 실수 정사각행렬이에요.$P^\top=P$예요. 대칭이라는 조건 하나만으로 직교투영행렬이 되지는 않아요.이 문제에서는 도출한 행렬의 전치 성질을 확인해요.
- **멱등성 (idempotence)** — 같은 연산을 두 번 해도 한 번 한 것과 같은 성질이에요.$P^2=P$예요. 이미 투영한 벡터를 다시 투영해도 변하지 않는지 확인해요.이 문제에서는 투영을 반복해도 예측이 변하지 않는지 확인해요.
- **피타고라스 성질 (Pythagorean identity)** — 두 벡터가 직교하면 합의 제곱노름이 각각의 제곱노름의 합이 되는 성질이에요.$a^\top b=0$이면 $\|a+b\|^2=\|a\|^2+\|b\|^2$예요.이 문제에서는 직교 조건이 실제 최소거리를 보장함을 증명해요.

---

원 문제·정리노트·PDF는 보존해요.
