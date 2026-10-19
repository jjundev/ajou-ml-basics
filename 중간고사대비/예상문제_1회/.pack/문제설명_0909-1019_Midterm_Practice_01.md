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

출제 근거: 과제1 P6-P8 변형. MML PDF 46, 47쪽의 이론을 대조했어요. 과제의 수치·조건을 바꾼 변형 문제예요. 교수님의 세부 출제 확정 내용은 아니에요.

#### 종이에 쓸 첫 줄

$v_3=v_1+v_2$인지 성분별로 써 봐요. 이어서 $V\alpha=(\alpha_1+\alpha_3,\alpha_2+\alpha_3,\alpha_1+\alpha_2+2\alpha_3)^\top$로 적어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$v_1+v_2-v_3=0$이에요. 계수 $(1,1,-1)$는 영벡터가 아니므로 세 벡터는 선형종속이에요. 반면 $av_1+bv_2=0$의 첫째·둘째 성분에서 $a=b=0$이므로 앞의 두 벡터는 독립이에요.

#### (b)

$V\alpha=b$에서 $\alpha_1+\alpha_3=2$, $\alpha_2+\alpha_3=1$이에요. 셋째 식은 앞의 두 식의 합이므로 새 제약이 아니에요. $t=\alpha_3\in\mathbb R$로 두면

$$
\alpha=(2-t,1-t,t)^\top.
$$

모든 열벡터는 셋째 성분이 첫째와 둘째의 합이에요. $c$는 $4\ne2+1$이므로 해가 없어요.

#### (c)

내적을 채우면

$$
U^\top U=\begin{pmatrix}2&1\\1&2\end{pmatrix},\quad (U^\top U)^{-1}=\tfrac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}.
$$

행렬식은 $3$이에요. $a=(1,1,-1)^\top\ne0$에 대해 $Va=0$이므로 $V^\top Va=0$이고, $V^\top V$는 특이행렬이에요.

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

- 조건과 미지수의 차원을 직접 적어요.
- 첫 식에서 완성 답까지 도움 없이 이어 써요.
- 각 소문항의 검산을 다시 수행해요.

**페이지 요약**

#### 떠올릴 개념·공식

독립: $V\alpha=0\Rightarrow\alpha=0$. Gram: $U^\top U$ 가역 $\Leftrightarrow$ 열독립. 일반해 $(2-t,1-t,t)^\top$.

#### 적용 조건

선형독립을 가정하지 않고 직접 판정; 모든 벡터는 열벡터

---

<a id="p2"></a>

### 2. Gradient·Jacobian·이차함수

EXAM Problem 2 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p2)

#### 주어진 조건

$x=(x_1,x_2)^\top$에 대해 다음을 정의한다. Gradient는 열벡터이고 Jacobian은 $(J_f)_{ij}=\partial f_i/\partial x_j$이다.

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

벡터 출력 $f$에는 Jacobian, 스칼라 출력 $q$에는 gradient를 써요. 행렬 모양을 먼저 정하면 미분한 값을 어디에 놓을지 헷갈리지 않아요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

Jacobian은 출력 하나마다 한 행, 입력 하나마다 한 열이에요. 여기서는 $2\times2$예요. Gradient는 이 과제의 약속에 따라 $2\times1$ 열벡터예요. Hessian은 모든 2차 편미분을 모은 행렬이에요. 대칭 $A$에 대해 $\nabla(\frac12x^\top Ax)=Ax$이고 Hessian은 $A$예요. 대칭 $2\times2$ 행렬은 첫 선도 주행렬식과 전체 행렬식이 양수이면 양의 정부호예요.

출제 근거: 과제1 P10-P12 변형. MML PDF 153, 155, 156쪽의 이론을 대조했어요. 과제의 수치·조건을 바꾼 변형 문제예요. 교수님의 세부 출제 확정 내용은 아니에요.

#### 종이에 쓸 첫 줄

$q=2x_1^2+x_1x_2+x_2^2-x_1$로 먼저 전개해요. 이 한 줄에서 교차항과 $1/2$가 제대로 반영됐는지 확인할 수 있어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

성분마다 미분하면

$$
J_f(x)=\begin{pmatrix}2x_1&1\\x_2&x_1\end{pmatrix},\quad J_f(1,2)=\begin{pmatrix}2&1\\2&1\end{pmatrix}.
$$

출력 2개, 입력 2개이므로 $2\times2$예요.

#### (b)

$q=2x_1^2+x_1x_2+x_2^2-x_1$이므로

$$
\nabla q=\begin{pmatrix}4x_1+x_2-1\\x_1+2x_2\end{pmatrix}=Ax-b,\quad H_q=\begin{pmatrix}4&1\\1&2\end{pmatrix}.
$$

두 번째 미분은 $x$와 무관해요.

#### (c)

$4x_1+x_2=1$, $x_1+2x_2=0$을 풀면

$$
x_*=(2/7,-1/7)^\top.
$$

$4>0$, $\det A=7>0$이므로 $A\succ0$이에요. 따라서 $q$는 엄격볼록이고 이 정지점이 유일한 전역 최소점이에요.

#### 완성 답과 검산

#### (a) 검산

$f_1$은 $x_1$ 방향으로 $2x_1$, $x_2$ 방향으로 1만큼 변해요. 이 값들이 첫째 행에 있는지 확인해요.

#### (b) 검산

$\frac12x^\top Ax$의 교차항은 $\frac12(x_1x_2+x_2x_1)=x_1x_2$예요. 미분하면 두 교차 편미분이 모두 1이 되어 Hessian이 대칭이에요.

#### (c) 검산

$A(2/7,-1/7)^\top=(1,0)^\top=b$예요. 또 $q(x)-q(x_*)=\frac12(x-x_*)^\top A(x-x_*)>0$은 $x\ne x_*$에서 성립하므로 전역성과 유일성이 함께 확인돼요.

#### 여기서 헷갈리기 쉬워요

$x^\top Ax$와 $\frac12x^\top Ax$의 gradient는 2배 차이가 나요. Jacobian의 행과 열을 바꾸거나 gradient를 행벡터로 쓰지 않도록 문제의 표기 약속을 따라요.

#### 설명을 닫고 다시 풀어요

- 조건과 미지수의 차원을 직접 적어요.
- 첫 식에서 완성 답까지 도움 없이 이어 써요.
- 각 소문항의 검산을 다시 수행해요.

**페이지 요약**

#### 떠올릴 개념·공식

$J_f$: 출력×입력. 대칭 $A$이면 $\nabla q=Ax-b$, $H=A$. 최소점 $(2/7,-1/7)^\top$.

#### 적용 조건

gradient는 열벡터, Jacobian은 출력×입력, A는 대칭

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

“가우시안 곱”과 “완전제곱”이 단서예요. $a(z-m)^2$에서 precision은 $a$, 분산은 $1/a$예요. 평균은 제곱 안의 중심 $m$이에요. $\mathcal N(z\mid m,v)$의 앞 계수는 $1/\sqrt{2\pi v}$예요. 분산과 표준편차를 구분하고, 지수의 상수항도 $Z$ 계산에서는 남겨요.

출제 근거: 과제1 P14·P25 변형. MML PDF 207, 208쪽의 이론을 대조했어요. 과제의 수치·조건을 바꾼 변형 문제예요. 교수님의 세부 출제 확정 내용은 아니에요.

#### 종이에 쓸 첫 줄

$z^2+(z-2)^2/3=\frac43z^2-\frac43z+\frac43$로 지수를 한 이차식으로 모아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

중심을 $1/2$로 맞추면

$$
z^2+\frac{(z-2)^2}{3}=\frac43(z-\tfrac12)^2+1.
$$

따라서

$$
g(z)=\frac{e^{-1/2}}{2\pi\sqrt3}\exp\!\left[-\frac23(z-\tfrac12)^2\right].
$$

#### (b)

$-\frac23(z-1/2)^2=-\frac{(z-1/2)^2}{2(3/4)}$이므로 평균 $1/2$, 분산 $3/4$예요.

$$
q(z)=\sqrt{\frac{2}{3\pi}}\exp\!\left[-\frac23(z-\tfrac12)^2\right]=\mathcal N(z\mid\tfrac12,\tfrac34).
$$

#### (c)

$\int\exp[-\frac23(z-1/2)^2]dz=\sqrt{3\pi/2}$이므로

$$
Z=\frac{e^{-1/2}}{\sqrt{8\pi}}.
$$

$Z\ne1$이므로 $g$ 자체는 정규화된 밀도가 아니에요. $g=Zq$로 구분해요.

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

- 조건과 미지수의 차원을 직접 적어요.
- 첫 식에서 완성 답까지 도움 없이 이어 써요.
- 각 소문항의 검산을 다시 수행해요.

**페이지 요약**

#### 떠올릴 개념·공식

precision 합산: $v^{-1}=v_0^{-1}+v_1^{-1}$. $m=1/2$, $v=3/4$, $Z=e^{-1/2}/\sqrt{8\pi}$.

#### 적용 조건

N의 둘째 인수는 분산; 정규화된 곱과 원래 곱을 구분

---

<a id="p4"></a>

### 4. 특징행렬로 계산하는 ML과 MAP

EXAM Problem 4 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p4)

#### 주어진 조건

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

출제 근거: 과제1 P17-P20 변형. MML PDF 300, 302, 307, 308쪽의 이론을 대조했어요. 과제의 수치·조건을 바꾼 변형 문제예요. 교수님의 세부 출제 확정 내용은 아니에요.

#### 종이에 쓸 첫 줄

$\Phi=\begin{pmatrix}1&-1\\1&0\\1&1\end{pmatrix}$와 $y=(0,1,4)^\top$부터 적어요. 각 행이 관측 하나라는 뜻이에요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

각 관측의 특징벡터를 행으로 놓으면

$$
\Phi=\begin{pmatrix}1&-1\\1&0\\1&1\end{pmatrix}.
$$

열별 내적과 출력의 내적은

$$
\Phi^\top\Phi=\begin{pmatrix}3&0\\0&2\end{pmatrix},\quad\Phi^\top y=\begin{pmatrix}5\\4\end{pmatrix}.
$$

$x_n$의 합이 0이므로 비대각성분이 0이에요.

#### (b)

$\operatorname{diag}(3,2)\theta=(5,4)^\top$에서

$$
\theta_{\mathrm{ML}}=(5/3,2)^\top.
$$

$x_*=2$의 평균 예측은 $5/3+2\cdot2=17/3$이에요.

#### (c)

prior의 음의 로그가 $\frac12\theta^\top\theta+\mathrm{const}$이므로 $\lambda=1$이에요. $\operatorname{diag}(4,3)\theta=(5,4)^\top$에서

$$
\theta_{\mathrm{MAP}}=(5/4,4/3)^\top.
$$

평균 예측은 $5/4+2(4/3)=47/12$예요. 계수가 prior 평균 0 쪽으로 작아졌어요.

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

- 조건과 미지수의 차원을 직접 적어요.
- 첫 식에서 완성 답까지 도움 없이 이어 써요.
- 각 소문항의 검산을 다시 수행해요.

**페이지 요약**

#### 떠올릴 개념·공식

Gram $\operatorname{diag}(3,2)$, ML $(5/3,2)$, MAP $(5/4,4/3)$. 모든 계수에 prior 적용.

#### 적용 조건

잡음분산 1, 절편 포함 모든 계수에 N(0,I) prior

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

출제 근거: 과제1 P21-P22 변형. MML PDF 194, 196, 198, 200쪽의 이론을 대조했어요. 과제의 수치·조건을 바꾼 변형 문제예요. 교수님의 세부 출제 확정 내용은 아니에요.

#### 종이에 쓸 첫 줄

$\mu_X=(2/3,2/3)^\top$와 $E[XX^\top]=\operatorname{diag}(4/3,4/3)$를 써요. $\Sigma_X=E[XX^\top]-\mu_X\mu_X^\top$로 계산하면 짧아요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$$
\mu_X=\begin{pmatrix}2/3\\2/3\end{pmatrix},\quad \Sigma_X=\frac19\begin{pmatrix}8&-4\\-4&8\end{pmatrix}.
$$

예를 들어 $(1,2)$ 성분은 $E[X_1X_2]-E[X_1]E[X_2]=0-4/9=-4/9$예요.

#### (b)

$$
\mu_Y=\begin{pmatrix}7/3\\-1\end{pmatrix},\quad\Sigma_Y=\begin{pmatrix}8/9&0\\0&8/3\end{pmatrix}.
$$

교차공분산은

$$
C_{XY}=\Sigma_XA^\top=\begin{pmatrix}4/9&4/3\\4/9&-4/3\end{pmatrix}.
$$

좌우 순서는 $X$의 차원×$Y$의 차원을 따라요.

#### (c)

가능한 $Y$는 $(1,-1)^\top,(3,1)^\top,(3,-3)^\top$이고 각각 확률 $1/3$이에요. 공분산이 0이므로 두 성분은 무상관이에요. 하지만 $P(Y_1=1,Y_2=1)=0$인 반면 $P(Y_1=1)P(Y_2=1)=1/9$이므로 독립은 아니에요.

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

- 조건과 미지수의 차원을 직접 적어요.
- 첫 식에서 완성 답까지 도움 없이 이어 써요.
- 각 소문항의 검산을 다시 수행해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\mu_Y=A\mu_X+b$, $\Sigma_Y=A\Sigma_XA^\top$, $C_{XY}=\Sigma_XA^\top$. 무상관이지만 독립 아님.

#### 적용 조건

공분산 분모 N=3; X는 세 관측을 균등 선택; Gaussian 가정 없음

---

<a id="p6"></a>

### 6. 확률모델에서 경험위험 최소화까지

EXAM Problem 6 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p6)

#### 주어진 조건

고정 입력 $x_1,\ldots,x_N$과 $y_n=\theta_0+\theta_1x_n+\epsilon_n$을 생각하자. $\theta=(\theta_0,\theta_1)^\top$이고, $\epsilon_n$은 서로 독립이며 $\mathcal N(0,\sigma^2)$를 따른다. $\sigma^2>0$는 알려져 있다. $\Phi$의 $n$번째 행은 $(1,x_n)$이며 열들은 선형독립이다.

#### 구할 것

1. 고정 입력과 $\theta$가 주어졌을 때 $y_n$의 조건부 분포를 쓰고, 관측들의 조건부 독립성이 성립하는 이유를 설명하라.
2. 소문항 (a)를 이용해 전체 우도 $p(y\mid\Phi,\theta)$와 음의 로그우도 $\mathcal L(\theta)$를 정규화 상수까지 써라.
3. 소문항 (b)의 목적함수를 제곱손실 경험위험 $\widehat R(\theta)=N^{-1}\sum_n(y_n-\phi(x_n)^\top\theta)^2$와 연결하라. 왜 최소점이 같은가?
4. 소문항 (c)의 제곱오차를 $\theta$의 이차식으로 전개하고 열 gradient를 구해 정규방정식을 도출하라.
5. 소문항 (d)를 풀어 $\theta_{\mathrm{ML}}$을 도출하고 유일한 최소점임을 보여라. 특징을 $(1,x,x^2)^\top$로 바꾸어도 선형 회귀인 이유를 설명하라.

#### 문제를 내 말로 읽어요

확률모델에서 경험위험 최소화까지: 주어진 모델에서 출발해 앞 소문항의 결과를 다음 단계에 사용해요. 마지막에는 Gaussian 선형 회귀의 ML 추정식에 도달해요.

#### 이 문제를 봤을 때 떠올릴 개념과 공식

“서로 독립인 Gaussian 잡음”은 조건부 우도를 곱으로 쓰는 단서예요. 입력과 $\theta$가 주어졌을 때 각 출력의 평균은 $\phi_n^\top\theta$, 분산은 $\sigma^2$예요. 경험위험(empirical risk)은 관측 손실의 평균이에요. $\theta$와 무관한 상수나 양의 배수는 최소화 위치를 바꾸지 않아요. 알려진 고정 $\sigma^2$라는 조건이 이 연결에 필요해요.

출제 근거: MML 9.2 theory application. MML PDF 298, 299, 300, 302쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$y_n\mid\Phi,\theta\sim\mathcal N(\phi_n^\top\theta,\sigma^2)$부터 적고, 다음 줄에서 독립성을 곱으로 바꾸어요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

주어진 식에서 $y_n$은 고정값 $\phi_n^\top\theta$에 Gaussian 잡음을 더한 값이에요. 따라서

$$
y_n\mid\Phi,\theta\sim\mathcal N(\phi_n^\top\theta,\sigma^2).
$$

각 출력의 무작위성은 서로 독립인 $\epsilon_n$에서만 오므로 입력과 $\theta$를 고정하면 출력들도 독립이에요.

#### (b)

(a)의 독립성으로 곱을 만들어요.

$$
p(y\mid\Phi,\theta)=(2\pi\sigma^2)^{-N/2}\exp\!\left[-\frac{\sum_n(y_n-\phi_n^\top\theta)^2}{2\sigma^2}\right].
$$

음의 로그를 취하면 곱의 정규화 상수도 남아요.

$$
\mathcal L=\frac N2\log(2\pi\sigma^2)+\frac{\|y-\Phi\theta\|^2}{2\sigma^2}.
$$

#### (c)

(b)의 합은 $N\widehat R$예요. 따라서

$$
\mathcal L=C+\frac{N}{2\sigma^2}\widehat R.
$$

$C$는 $\theta$와 무관하고 배율은 양수예요. 두 후보의 위험 대소관계가 그대로 보존되어 우도 최대화와 경험위험 최소화가 같은 모수를 골라요.

#### (d)

(c)의 제곱오차를 전개하면

$$
Q=y^\top y-2\theta^\top\Phi^\top y+\theta^\top\Phi^\top\Phi\theta.
$$

대칭인 Gram 행렬을 이용하면

$$
\nabla Q=2\Phi^\top\Phi\theta-2\Phi^\top y.
$$

이를0으로 놓아

$$
\Phi^\top\Phi\theta=\Phi^\top y
$$

를 얻어요.

#### (e)

(d)에서 열독립이므로 Gram 행렬이 가역이에요.

$$
\theta_{\mathrm{ML}}=(\Phi^\top\Phi)^{-1}\Phi^\top y.
$$

비영 $v$에 대해 $v^\top\Phi^\top\Phi v=\|\Phi v\|^2>0$이므로 이차 목적함수는 엄격히 볼록하고 해는 유일해요. 다항 특징도 $\theta_0+\theta_1x+\theta_2x^2$처럼 모수에 선형이므로 선형 회귀예요.

#### 완성 답과 검산

#### (a) 검산

각 평균은 스칼라이고 분산은 알려진 양수예요. 독립성은 모수를 고정한 조건부 주장임을 확인해요.

#### (b) 검산

$N=1$을 넣으면 한 관측 Gaussian 밀도와 그 음의 로그로 돌아가요.

#### (c) 검산

$\mathcal L(\theta_a)-\mathcal L(\theta_b)=N(\widehat R(\theta_a)-\widehat R(\theta_b))/(2\sigma^2)$여서 부호가 같아요.

#### (d) 검산

원래 제곱합을 성분별 미분해도 $-2\sum_n\phi_n(y_n-\phi_n^\top\theta)$로 같아요.

#### (e) 검산

최종 식을 정규방정식에 넣으면 양변이 같아요. 잔차는 $\Phi^\top r=0$, 추정량은 $K\times1$이에요.

#### 여기서 헷갈리기 쉬워요

조건부 독립과 주변 독립을 혼동하지 않아요. $\sigma^2$도 함께 추정하는 문제라면 그 항을 상수라고 버릴 수 없어요. 여기서는 알려진 분산으로 고정했어요.

#### 설명을 닫고 다시 풀어요

- 각 소문항에서 얻은 식을 다음 소문항의 첫 줄로 옮겨요.
- 모델에서 시작해 최종 공식을 보지 않고 유도해요.
- 독립성·차원·역행렬 조건을 설명하며 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

독립 Gaussian → 곱 우도 → NLL $=\mathrm{const}+\mathrm{SSE}/(2\sigma^2)$ → ERM. 선형성은 계수 $\theta$ 기준.

#### 적용 조건

고정 입력; θ를 조건으로 독립인 동일분산 Gaussian 잡음; σ² 알려짐

---

<a id="p7"></a>

### 7. Gaussian prior가 만드는 ridge

EXAM Problem 7 · [원 문제 보기](../%EC%A4%91%EA%B0%84%EA%B3%A0%EC%82%AC%EC%98%88%EC%83%81_0909-1019_Midterm_Practice_01.html#p7)

#### 주어진 조건

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

출제 근거: MML 9.2.3-9.2.4 theory application. MML PDF 307, 308, 309쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$-\log p(\theta\mid y,\Phi)=\frac1{2\sigma^2}\|y-\Phi\theta\|^2+\frac1{2\tau^2}\|\theta-m_0\|^2+C$부터 적어요. $C$만 $\theta$와 무관해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

Bayes 정리에서

$$
p(\theta\mid y,\Phi)=\frac{p(y\mid\Phi,\theta)p(\theta)}{p(y\mid\Phi)}.
$$

분모는 모수를 적분한 값이므로 현재 최적화 변수 $\theta$에 의존하지 않아요. 따라서 분자의 곱을 최대화해도 같은 MAP를 얻어요.

#### (b)

(a)의 두 Gaussian 지수에 음의 로그를 적용해요.

$$
-\log p(\theta\mid y,\Phi)=J=\frac{\|y-\Phi\theta\|^2}{2\sigma^2}+\frac{\|\theta-m_0\|^2}{2\tau^2}+C.
$$

두 분산은 고정값이고 $C$에만 정규화 상수와 evidence를 모았어요.

#### (c)

(b)에서 열 gradient는

$$
\nabla J=\frac{\Phi^\top(\Phi\theta-y)}{\sigma^2}+\frac{\theta-m_0}{\tau^2}.
$$

0으로 놓고 양변에 $\sigma^2$를 곱하면

$$
(\Phi^\top\Phi+\lambda I)\theta=\Phi^\top y+\lambda m_0,
$$

여기서 $\lambda=\sigma^2/\tau^2$예요.

#### (d)

(c)의 역행렬을 곱하면

$$
\theta_{\mathrm{MAP}}=(\Phi^\top\Phi+\lambda I)^{-1}(\Phi^\top y+\lambda m_0).
$$

(b)에 양수 $2\sigma^2$를 곱해도 최소점은 같으므로 상대 벌점은 $\lambda=\sigma^2/\tau^2$예요.

#### (e)

(d)의 행렬을 $A$라 하면

$$
v^\top Av=\|\Phi v\|^2+\lambda\|v\|^2>0\quad(v\ne0).
$$

$\lambda>0$이면 첫 항이0이어도 둘째 항이 양수예요. 따라서 $A$는 양의 정부호이고 가역이며 MAP는 유일해요.

#### (f)

$G=\begin{pmatrix}5&5\\5&5\end{pmatrix}$, $\Phi^\top y=(5,5)^\top$예요. (d)는

$$
\begin{pmatrix}6&5\\5&6\end{pmatrix}\theta=(5,5)^\top
$$

이므로 $\theta_{\mathrm{MAP}}=(5/11,5/11)^\top$예요. $\lambda=0$에서는 $\theta_1+\theta_2=1$인 모든 해가 최소제곱 해여서 유일하지 않아요. $m_0=0$에서 $\lambda\to\infty$이면 추정량은0으로 가요.

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

$m_0\ne0$일 때 우변의 $\lambda m_0$를 빠뜨리지 않아요. 정규화는 계수를 prior 쪽으로 제약하지만 시험·새 데이터 오차가 항상 좋아진다는 보장은 없어요. 지나치게 큰 $\lambda$는 데이터 정보를 거의 무시해요.

#### 설명을 닫고 다시 풀어요

- 각 소문항에서 얻은 식을 다음 소문항의 첫 줄로 옮겨요.
- 모델에서 시작해 최종 공식을 보지 않고 유도해요.
- 독립성·차원·역행렬 조건을 설명하며 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\lambda=\sigma^2/\tau^2>0$. $G+\lambda I\succ0$. MAP $=(G+\lambda I)^{-1}(\Phi^\top y+\lambda m_0)$.

#### 적용 조건

고정 입력; 모든 계수에 N(m0,τ²I) prior; σ²,τ²&gt;0

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

출제 근거: MML 9.3.3-9.3.4 theory application. MML PDF 312, 314, 315쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$g(\theta)=p(\theta)p(2\mid\theta)p(0\mid\theta)$부터 적어요. 이 곱의 지수를 전개한 뒤 완전제곱해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

Prior와 두 likelihood의 곱이에요.

$$
g(\theta)=\mathcal N(\theta\mid1,2)\mathcal N(2\mid\theta,2)\mathcal N(0\mid\theta,2).
$$

따라서

$$
g(\theta)\propto\exp\!\left[-\frac{(\theta-1)^2+(2-\theta)^2+\theta^2}{4}\right].
$$

독립 관측이므로 두 likelihood를 곱했어요.

#### (b)

(a)의 세 제곱을 전개하면 $3\theta^2-6\theta+5$예요.

$$
-\frac{3\theta^2-6\theta+5}{4}=-\frac12\left(\frac32\theta^2-3\theta+\frac52\right).
$$

따라서 $A=3/2$, $b=3/2$, $c=5/2$예요.

#### (c)

(b)에서

$$
A\theta^2-2b\theta+c=\frac32(\theta-1)^2+1.
$$

$\theta$와 무관한 항을 정규화 인자로 흡수하면 평균은 $b/A=1$, 분산은 $A^{-1}=2/3$이에요.

$$
p(\theta\mid D)=\sqrt{\frac3{4\pi}}\exp[-3(\theta-1)^2/4].
$$

적분1인 Gaussian 밀도로 정규화했어요.

#### (d)

(c)에서 $x_*=2$예요. 상수배의 평균은2배, 분산은4배이므로

$$
E[f_*\mid D]=2,\quad\operatorname{Var}(f_*\mid D)=8/3.
$$

Gaussian의 선형변환이어서 $f_*\mid D\sim\mathcal N(2,8/3)$예요.

#### (e)

(d)의 $f_*$에 평균0, 분산2의 독립 잡음을 더해요. 교차 공분산은0이므로

$$
E[y_*\mid D]=2,\quad\operatorname{Var}(y_*\mid D)=8/3+2=14/3.
$$

독립 Gaussian의 합이어서 $y_*\mid D\sim\mathcal N(2,14/3)$예요.

#### (f)

(c)의 Gaussian은 평균에서 최대이므로 $\theta_{\mathrm{MAP}}=1$이에요. 이 값을 고정하면 $y_*=2+\epsilon_*$여서 $\mathcal N(2,2)$예요. (e)와 평균은 같지만 분산은 $8/3$ 작아요. 고정 대입은 $x_*^2\operatorname{Var}(\theta\mid D)$라는 모수 불확실성을 제거해요.

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

- 각 소문항에서 얻은 식을 다음 소문항의 첫 줄로 옮겨요.
- 모델에서 시작해 최종 공식을 보지 않고 유도해요.
- 독립성·차원·역행렬 조건을 설명하며 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\theta\mid D\sim\mathcal N(1,2/3)$. 잠재분산 $8/3$, 관측분산 $14/3$. MAP 고정 예측은 $\mathcal N(2,2)$.

#### 적용 조건

서로 독립 잡음, prior와 독립; 새 잡음도 독립; 분산 표기

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

출제 근거: Lecture04 s17 and MML 9.3.3 theory application. MML PDF 312, 319쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$p(y\mid M_j)=\int p(y\mid\theta,M_j)p(\theta\mid M_j)d\theta$를 적고 두 Gaussian 밀도를 대입해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

모델이 정해지면 아직 관측을 반영하지 않은 모수 분포로 평균내요.

$$
p(y\mid M_j)=\int\mathcal N(y\mid\theta,1)\mathcal N(\theta\mid0,v_j)d\theta.
$$

Posterior는 이미 $y$를 반영한 분포여서 이 적분의 prior를 대신할 수 없어요.

#### (b)

(a)의 지수에 등장하는 제곱합은

$$
(y-\theta)^2+\theta^2/v_j=A(\theta-y/A)^2+\frac{y^2}{1+v_j},
$$

여기서 $A=1+1/v_j$예요. 곱의 앞 계수는 $1/(2\pi\sqrt{v_j})$이고 제곱항 적분은 $\sqrt{2\pi/A}$예요. 따라서

$$
p(y\mid M_j)=\frac{\exp[-y^2/(2(1+v_j))]}{\sqrt{2\pi(1+v_j)}}.
$$

즉 관측의 주변분포는 $\mathcal N(0,1+v_j)$예요.

#### (c)

(b)에서 $v_1=1,v_2=4$를 넣으면 관측 분산은2와5예요. $y=0$에서는 지수항이1이므로

$$
p(0\mid M_1)=1/\sqrt{4\pi},\quad p(0\mid M_2)=1/\sqrt{10\pi}.
$$

#### (d)

(c)의 밀도 비는

$$
B_{12}=\sqrt{5/2}>1.
$$

동일한 관측에 더 큰 evidence를 주는 $M_1$을 데이터가 지지해요. 이는 모델 prior를 아직 반영하지 않은 비교예요.

#### (e)

Bayes 정리의 공통 분모 $p(y)$가 소거돼요.

$$
\frac{P(M_1\mid y)}{P(M_2\mid y)}=\frac{p(y\mid M_1)}{p(y\mid M_2)}\frac{P(M_1)}{P(M_2)}.
$$

Prior odds는 $1/2$이므로 posterior odds는 $O=\sqrt{5/2}/2<1$이에요.

$$
P(M_1\mid0)=\frac O{1+O}=\frac{\sqrt{5/2}}{2+\sqrt{5/2}}\simeq0.44152.
$$

사후확률은 $M_2$가 더 커요.

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

- 각 소문항에서 얻은 식을 다음 소문항의 첫 줄로 옮겨요.
- 모델에서 시작해 최종 공식을 보지 않고 유도해요.
- 독립성·차원·역행렬 조건을 설명하며 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

evidence: prior 평균. $B_{12}=\sqrt{5/2}$, posterior odds $=\sqrt{10}/4$. 사후 선택 $M_2$.

#### 적용 조건

두 모델 prior probability 명시; evidence는 prior로 적분

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

출제 근거: MML 3.8,9.4 theory application. MML PDF 87, 88, 89, 319, 320쪽 및 범위 내 강의 개념을 연결한 새 유도형 연습 문제예요. 교수님의 세부 출제 확정 문항은 아니에요.

#### 종이에 쓸 첫 줄

$r=y-\Phi\widehat\theta$와 $\|r-t\Phi h\|^2$를 적고, $t$에 대한 미분부터 시작해요.

#### 왜 이렇게 푸는지 함께 따라가요

#### (a)

$r=y-\Phi\widehat\theta$로 두면 거리제곱은

$$
\|r-t\Phi h\|^2=\|r\|^2-2t h^\top\Phi^\top r+t^2\|\Phi h\|^2.
$$

$t=0$의 도함수는 $-2h^\top\Phi^\top r$예요. 모든 $h$에서0이므로

$$
\Phi^\top r=0.
$$

즉 잔차가 모든 열에 직교해요.

#### (b)

(a)에 잔차를 대입하면

$$
\Phi^\top(y-\Phi\widehat\theta)=0.
$$

따라서 $G\widehat\theta=\Phi^\top y$, $G=\Phi^\top\Phi$예요. 열독립으로 $G$가 가역이므로

$$
\widehat\theta=G^{-1}\Phi^\top y.
$$

#### (c)

(b)의 추정식을 예측식에 넣어요.

$$
\widehat y=\Phi G^{-1}\Phi^\top y,\quad P=\Phi G^{-1}\Phi^\top.
$$

$\Phi$가 $N\times K$이면 $P$는 $N\times N$이에요. $G^{-1}$가 대칭이라 $P^\top=P$이고

$$
P^2=\Phi G^{-1}G G^{-1}\Phi^\top=P.
$$

추정량 $\widehat\theta$의 차원 $K\times1$과 구별해요.

#### (d)

$G=\operatorname{diag}(3,2)$, $\Phi^\top y=(4,2)^\top$예요. 따라서 $\widehat\theta=(4/3,1)^\top$이고

$$
P=\frac16\begin{pmatrix}2&2&2\\2&5&-1\\2&-1&5\end{pmatrix}.
$$

$$
\widehat y=(4/3,7/3,1/3)^\top,\quad r=(2/3,-1/3,-1/3)^\top.
$$

열별 내적은 $2/3-1/3-1/3=0$과 $-1/3+1/3=0$이에요.

#### (e)

$\widehat y-u$는 열공간 안에 있어 (a)의 $r$와 직교해요.

$$
y-u=r+(\widehat y-u).
$$

내적 교차항이0이므로

$$
\|y-u\|^2=\|r\|^2+\|\widehat y-u\|^2\ge\|r\|^2.
$$

등호는 $u=\widehat y$일 때뿐이므로 이 점이 유일한 최근접점이에요. 필요조건에서 시작한 (a)의 논증에 충분성도 더했어요.

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

- 각 소문항에서 얻은 식을 다음 소문항의 첫 줄로 옮겨요.
- 모델에서 시작해 최종 공식을 보지 않고 유도해요.
- 독립성·차원·역행렬 조건을 설명하며 검산해요.

**페이지 요약**

#### 떠올릴 개념·공식

$\Phi^\top r=0$, $P=\Phi(\Phi^\top\Phi)^{-1}\Phi^\top$, $P^\top=P^2=P$. 최소 잔차제곱 $2/3$.

#### 적용 조건

Φ full column rank; 유클리드 내적, 알려진 동일 Gaussian 잡음분산

---

원 문제·정리노트·PDF는 보존해요.
