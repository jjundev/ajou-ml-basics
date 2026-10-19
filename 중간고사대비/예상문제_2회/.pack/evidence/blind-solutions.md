# 모의평가 2 독립 블라인드 수학 풀이

읽은 문제 원문은 `blind-input.html` 하나뿐이다. 참고 풀이, 해설, 작성 대화는 읽지 않았다. 아래의 `pass`는 독립적으로 해당 답을 도출했다는 뜻이며 참고답과의 일치 판정이 아니다. Gaussian 둘째 인수는 분산, gradient는 열벡터로 해석한다.

## p1:a

\[
V(t)=\begin{pmatrix}1&0&1\\0&1&1\\1&1&t\end{pmatrix},\qquad \det V(t)=t-2.
\]
열벡터 세 개가 독립이고 R³의 기저인 필요충분조건은 \(t\ne2\)이다.

## p1:b

미지수를 \((a,b,c)^T\)라 쓰면 \(a+c=1,b+c=2,a+b+2c=3\)이다. 마지막 식은 앞 두 식의 합이므로 모든 해는
\[
\alpha=(1-u,2-u,u)^T,\qquad u\in\mathbb R.
\]
우변이 \((1,2,4)^T\)이면 앞 두 식의 합은 3인데 마지막 식은 4여야 하므로 해가 없다. 열공간은 \(\{(z_1,z_2,z_3)^T:z_3=z_1+z_2\}\)이다.

## p1:c

\(a+c=1,b+c=2,a+b+3c=4\)에 앞 두 식을 대입하면 \(3+c=4\)이다. 따라서 \(\alpha=(0,1,1)^T\). t=3에서는 행렬이 가역이고 열공간이 R³ 전체이므로 같은 우변도 유일하게 표현된다.

## p2:a

\[
J_f(x)=\begin{pmatrix}1&1\\x_2&x_1\end{pmatrix},\qquad J_f(1,2)=\begin{pmatrix}1&1\\2&1\end{pmatrix}\in\mathbb R^{2\times2}.
\]

## p2:b

\(f(1,2)=(3,2)^T\), 따라서 \(\nabla_z\ell(f(1,2))=(2,0)^T\). 연쇄법칙은
\[
\nabla_xL=J_f^T(f(x)-(1,2)^T),\qquad \nabla_xL(1,2)=(2,2)^T.
\]
직접 전개하면
\[
L(x)=\tfrac12(x_1+x_2-1)^2+\tfrac12(x_1x_2-2)^2,
\]
\[
\nabla L=\begin{pmatrix}x_1+x_2-1+x_2(x_1x_2-2)\\x_1+x_2-1+x_1(x_1x_2-2)\end{pmatrix}.
\]
점 (1,2)에서 역시 (2,2)ᵀ이다.

## p2:c

\(D_dL=\nabla L^Td=(2,2)(1,-1)^T=0\). 경로를 직접 대입해도 \(L(1+h,2-h)=2+\tfrac12(h-h^2)^2\)여서 h=0 미분값이 0이다. 그러나 gradient가 0이 아니므로 이 점은 정지점이 아니다. 한 방향의 미분값 0은 그 방향이 gradient에 직교한다는 뜻이다.

## p3:a

\[
E[Y]=A\mu+b=(0,4)^T,\qquad \operatorname{Cov}(Y)=A\Sigma A^T=\begin{pmatrix}6&0\\0&2\end{pmatrix}.
\]

## p3:b

\(Y_1\sim N(0,6)\), \(Y_2\sim N(4,2)\). 결합밀도는
\[
p_Y(y_1,y_2)=\frac1{4\pi\sqrt3}\exp\left[-\frac{y_1^2}{12}-\frac{(y_2-4)^2}{4}\right],\quad (y_1,y_2)\in\mathbb R^2.
\]
정규화 상수는 \((2\pi)^{-1}|\operatorname{Cov}(Y)|^{-1/2}=(4\pi\sqrt3)^{-1}\)이다.

## p3:c

Y는 아핀 변환된 공동 Gaussian이며 공분산의 비대각 원소가 0이므로 Y₁,Y₂는 독립이다. X₁,X₂의 공분산은 1이므로 독립이 아니다. 공동 Gaussian이라는 전제가 무상관에서 독립을 얻는 데 필요하다.

## p4:a

분산이 둘 다 2이므로
\[
g(\theta)=\frac1{4\pi}\exp\left[-\frac{(\theta+1)^2+(3-\theta)^2}{4}\right]
=\frac{e^{-2}}{4\pi}\exp[-(\theta-1)^2/2].
\]
문제가 지정한 식 자체의 완전제곱은
\[
\frac{(\theta+1)^2}{2}+\frac{(3-\theta)^2}{2}
=\theta^2-2\theta+5=(\theta-1)^2+4.
\]
이 식에는 전체 지수에서 추가 계수 -1/2가 곱해진다. 지정한 식을 그대로 음의 지수로 쓰면 분산이 달라지므로 주의한다.

## p4:b

posterior precision은 \(1/2+1/2=1\), 평균은 \((-1)/2+3/2=1\)이다. 따라서
\[
\theta\mid y=3\sim N(1,1),\qquad p(\theta\mid y=3)=\frac1{\sqrt{2\pi}}e^{-(\theta-1)^2/2}.
\]
우도만 최대화하는 ML은 3, posterior를 최대화하는 MAP는 1이다.

## p4:c

\(y=\theta+\epsilon\)에서 독립 분산을 더하면 \(y\sim N(-1,4)\). 따라서
\[
Z=p(y=3)=\frac{e^{-2}}{\sqrt{8\pi}}.
\]
직접 적분해도 \(e^{-2}(4\pi)^{-1}\sqrt{2\pi}\)로 같다. Z는 관측 y=3에서 평가한 주변밀도 값인 스칼라이고, posterior는 θ의 정규화된 밀도 함수이다. \(p(\theta\mid y=3)=g(\theta)/Z\). 연속변수이므로 p(y=3)는 여기서 점 사건의 확률이 아니라 밀도 표기이다.

## p5:a

\[
\Phi=\begin{pmatrix}1&1\\1&0\\1&1\end{pmatrix},\quad
\Phi^T\Phi=\begin{pmatrix}3&2\\2&2\end{pmatrix},\quad
\Phi^Ty=(6,6)^T.
\]
Gram 행렬식은 2이므로 가역이다. 두 행이 같아도 두 열 \((1,1,1)^T\), \((1,0,1)^T\)은 독립이다.

## p5:b

정규방정식 \(3\theta_1+2\theta_2=6,2\theta_1+2\theta_2=6\)에서
\[
\theta_{ML}=(0,3)^T,\quad \widehat y=(3,0,3)^T,\quad r:=y-\widehat y=(-1,0,1)^T,\quad \|r\|^2=2.
\]
\(\phi(2)=(1,4)^T\)이므로 평균 예측은 12이다. 잔차를 반대 부호로 정의하면 벡터 부호만 바뀌고 제곱합은 같다.

## p5:c

잡음분산과 prior 공분산이 각각 1과 I이므로
\[
\theta_{MAP}=(\Phi^T\Phi+I)^{-1}\Phi^Ty
=\begin{pmatrix}4&2\\2&3\end{pmatrix}^{-1}(6,6)^T=(3/4,3/2)^T.
\]
평균 예측은 \(3/4+4(3/2)=27/4\). 입력 x에는 제곱이 들어가지만 모수 θ에는 \(\theta_1+\theta_2x^2\)로 선형이므로 선형 회귀이다.

## p6:a

\[
p(y\mid\theta,s)=(2\pi s)^{-N/2}\exp\left[-\frac1{2s}\sum_n(y_n-\theta)^2\right],
\]
\[
\mathcal L(\theta,s)=\frac N2\log(2\pi)+\frac N2\log s+\frac1{2s}\sum_n(y_n-\theta)^2.
\]
제곱합은 \(S(\theta)=S(\bar y)+N(\theta-\bar y)^2\)이므로 모든 s>0에서 θ 최소점은 \(\widehat\theta=\bar y\). 표본이 모두 같지 않으면 \(S(\bar y)>0\)이다. s 미분은 \(N/(2s)-S(\bar y)/(2s^2)\)이며 유일한 최소점은
\[
\widehat s=\frac1N\sum_n(y_n-\bar y)^2>0.
\]
s→0 또는 ∞에서 음의 로그우도가 ∞로 가므로 이 점이 공동 전역 ML이다.

## p6:b

\(\widehat\theta=(1+2+6)/3=3\), 제곱합은 \(4+1+9=14\)이다. 따라서 ML 분산은 \(14/3\). N−1을 분모로 쓰는 불편 표본분산은 \(14/2=7\)로 더 크며 ML 분산과 다르다.

## p6:c

모두 c이면 θ=c에서 \(p(y\mid c,s)=(2\pi s)^{-N/2}\to\infty\) as s→0⁺이다. 허용 공간 s>0 안에서는 최대가 달성되지 않으므로 공동 ML 추정값이 없다. (c,0)은 허용 모수가 아니다.

## p7:a

\(q:=\sigma^2>0\)라 하면 θ에 무관한 상수를 제외한 음의 로그 posterior는
\[
Q(\theta)=\frac1{2q}\|y-\Phi\theta\|^2+\frac12(\theta-m_0)^TS_0^{-1}(\theta-m_0)
=\frac1{2q}\|y-\Phi\theta\|^2+\frac{(\theta_1-2)^2}{8}+\frac{\theta_2^2}{2}.
\]
미분하여
\[
\left(\frac{\Phi^T\Phi}{q}+S_0^{-1}\right)\theta
=\frac{\Phi^Ty}{q}+S_0^{-1}m_0.
\]
구체적으로 \(\Phi^T\Phi=2I\), \(\Phi^Ty=(4,4)^T\)이므로
\[
\begin{pmatrix}2/q+1/4&0\\0&2/q+1\end{pmatrix}\theta
=\begin{pmatrix}4/q+1/2\\4/q\end{pmatrix}.
\]
따라서 모든 q에서 \(\theta_{MAP}(q)=(2,4/(2+q))^T\).

## p7:b

q=1이면 \(\theta_{MAP}=(2,4/3)^T\), 평균 예측은 \(2+2(4/3)=14/3\). ML은 \((\Phi^T\Phi)^{-1}\Phi^Ty=(2,2)^T\), 평균 예측은 6이다. 첫 계수는 ML과 prior 평균이 모두 2여서 변하지 않고, 둘째 계수는 prior 평균 0 쪽으로 줄어든다.

## p7:c

임의의 u≠0에 대해 Hessian의 이차형식은
\[
u^T\left(\Phi^T\Phi/q+S_0^{-1}\right)u=\|\Phi u\|^2/q+u^TS_0^{-1}u>0.
\]
따라서 목적함수는 엄격 볼록이고 유일한 최소점을 갖는다. 위 명시해에서 q→0⁺이면 (2,2)ᵀ=ML, q→∞이면 (2,0)ᵀ=m₀로 수렴한다.

## p8:a

\[
S_N^{-1}=I+\tfrac12\Phi^T\Phi=2I,\quad S_N=\tfrac12I,
\qquad m_N=S_N\tfrac12\Phi^Ty=(1/2,1/2)^T.
\]
따라서 \(\theta\mid y\sim N((1/2,1/2)^T,I/2)\).

## p8:b

x*=1에서 φ*=(1,1)ᵀ이므로 잠재값의 평균은 1, 분산은 \(\phi_*^TS_N\phi_*=1\). 따라서
\[
f_*\mid y\sim N(1,1),\qquad y_*\mid y\sim N(1,3).
\]
Gaussian posterior의 MAP는 m_N이다. MAP 고정 대입은 \(y_*\mid\theta=m_N\sim N(1,2)\)이므로 평균은 같으나 모수 불확실성 1을 빠뜨린다.

## p8:c

φ₀=(1,0)ᵀ, φ₁=(1,1)ᵀ이다. 미래 잡음은 서로 독립이므로
\[
\operatorname{Cov}(y_*^{(0)},y_*^{(1)}\mid y)=\phi_0^TS_N\phi_1=1/2.
\]
전체 결합분포는
\[
\begin{pmatrix}y_*^{(0)}\\y_*^{(1)}\end{pmatrix}\mid y
\sim N\left(\begin{pmatrix}1/2\\1\end{pmatrix},\begin{pmatrix}5/2&1/2\\1/2&3\end{pmatrix}\right).
\]
θ까지 주면 두 관측의 확률적 변동은 독립 잡음뿐이지만, y만 주면 불확실한 θ₁을 공유하므로 독립이 아니다. 비영 공분산이 이를 직접 증명한다.

## p9:a

모두 평균은 (0,0)ᵀ이다. M₁에서는 공통 θ가 두 관측에 공분산 1을 만들므로
\[
y\mid M_1\sim N\left(0,\begin{pmatrix}2&1\\1&2\end{pmatrix}\right).
\]
M₂에서는 각 모수와 잡음이 모두 독립이므로 \(y\mid M_2\sim N(0,2I)\).

## p9:b

M₁의 공분산 행렬식은 3, 역행렬은 \(\tfrac13\left(\begin{smallmatrix}2&-1\\-1&2\end{smallmatrix}\right)\). y=(1,−1)ᵀ에 대한 이차형식은 2이다. M₂의 행렬식은 4, 이차형식은 1이다. 따라서
\[
p(y\mid M_1)=\frac{e^{-1}}{2\pi\sqrt3},\qquad
p(y\mid M_2)=\frac{e^{-1/2}}{4\pi},
\]
\[
B_{12}=\frac2{\sqrt3}e^{-1/2}\approx0.7003612793<1.
\]
데이터의 evidence만으로는 M₂를 지지한다. 두 관측 부호가 반대여서 공유 모수의 양의 상관과 잘 맞지 않는다.

## p9:c

\[
\frac{P(M_1\mid y)}{P(M_2\mid y)}=3B_{12}=2\sqrt3e^{-1/2}\approx2.101083838.
\]
두 비교 모델이 모델 공간을 구성한다고 해석하면
\[
P(M_1\mid y)=\frac{2\sqrt3e^{-1/2}}{1+2\sqrt3e^{-1/2}}\approx0.6775320977,
\]
\(P(M_2\mid y)\approx0.3224679023\)이고 M₁을 선택한다. prior odds 3이 evidence의 M₂ 선호보다 강하므로 결과가 바뀐다.

조건 점검: 절대확률 계산에는 M₁,M₂가 상호배타적이고 비교 대상 전체라는 통상적 이모델 비교 해석을 썼다. 다른 모델도 가능하면 odds는 그대로 구할 수 있으나 주어진 odds만으로 M₁의 절대 사후확률은 결정되지 않는다. 문제의 '두 모델을 비교' 문맥에서는 자연스러운 가정이다.

## p10:a

직교 잔차 조건은 \(\Phi^Tr=0\), r=y−Φθ이다. 따라서 \(G\widehat\theta=\Phi^Ty\). 여기서
\[
G=\begin{pmatrix}2&1\\1&2\end{pmatrix},\quad G^{-1}=\tfrac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix},\quad\Phi^Ty=(1,2)^T.
\]
그러므로 \(\widehat\theta=(0,1)^T\), \(\widehat y=(0,1,1)^T\), \(r=(1,1,-1)^T\). 실제로 \(\Phi^Tr=(0,0)^T\).

## p10:b

\[
P=\frac13\begin{pmatrix}2&-1&1\\-1&2&1\\1&1&2\end{pmatrix}=M/3.
\]
M은 대칭이고 직접 곱하면
\[
M^2=\begin{pmatrix}6&-3&3\\-3&6&3\\3&3&6\end{pmatrix}=3M.
\]
따라서 Pᵀ=P, P²=M²/9=M/3=P이다.

## p10:c

\[
\theta_R=(G+I)^{-1}\Phi^Ty=\frac18\begin{pmatrix}3&-1\\-1&3\end{pmatrix}(1,2)^T=(1/8,5/8)^T.
\]
예측은 (1/8,5/8,3/4)ᵀ, 잔차는 (7/8,11/8,−3/4)ᵀ이다. 따라서
\[
\Phi^T(y-\Phi\theta_R)=(1/8,5/8)^T=\theta_R\ne0.
\]
Ridge 잔차는 이 경우 열공간에 직교하지 않는다. 정규방정식 자체가 \(\Phi^Tr=\theta_R\)이기 때문이다.

## p10:d

\[
H=\frac18\begin{pmatrix}3&-1&2\\-1&3&2\\2&2&4\end{pmatrix},\qquad v=\Phi(1,1)^T=(1,1,2)^T.
\]
직접 곱하거나 G(1,1)ᵀ=3(1,1)ᵀ을 이용하면
\[
Hv=\tfrac34v=(3/4,3/4,3/2)^T,\qquad H^2v=\tfrac9{16}v=(9/16,9/16,9/8)^T.
\]
두 값이 다르므로 H²≠H이다. H는 대칭이지만 직교투영행렬은 아니다. 직교투영에는 대칭성과 멱등성이 모두 필요하다.

## 조건·모호함 종합

- 풀이를 막는 수치 모순이나 미지정 모수는 발견하지 못했다.
- p4:a는 지정한 완전제곱 식과 실제 지수 전체의 -1/2 계수를 구별해야 한다. 올바른 likelihood/prior로 해석하면 일관적이다.
- p5:b의 잔차 방향은 문제에 명시되지 않았으므로 본 풀이에서는 y−예측으로 정의했다.
- p9:c 절대 사후확률은 두 모델만으로 비교 모델 공간이 완결된다는 통상 가정을 명시했다.
- 미래 잡음 독립 조건, 모든 계수 prior/벌점 적용 조건, p6의 열린 분산 모수공간은 모두 풀이에 반영했다.

## 문제 조건 재확인 기록

갱신된 `blind-input.html`만 다시 읽어 p9 조건의 “모델 공간은 M₁,M₂ 두 모델로만 구성된다” 명시를 확인했다. 이 문구는 기존 p9:c 독립 풀이가 사용한 두 모델 완결 가정을 명시한 것으로, 계산이나 답을 변경하지 않는다. 이에 따라 위 초기 조건 점검에서 지적한 p9:c의 가정 미명시는 현재 입력에서 해소되었다. 참고 풀이와 다른 자료는 다시 읽지 않았다.

현재 `blind-input.html` SHA-256: `8142a84738993a2aa6524d85f12a234bb5577ab10ee7a5891b054b748f017945`
