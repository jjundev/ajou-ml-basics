# 독립 수학 검산 결과

입력: `blind-1.html`, `blind-2.html`만을 문제 자료로 사용. 다른 풀이·참고답·보고서나 다른 에이전트의 수학 결과는 읽지 않았다. 각 문항은 직접 유도했고 일부 수치행렬을 SymPy 유리수 연산으로 교차검산했다.

풀이 소문항 수: 1회 42개, 2회 44개, 총 86개.

## 입력 SHA-256

- `blind-1.html`: `791f33d4fb97158abddcdca88f8b89b0989b7ca424f50d14aba81ea65f1e10fe`
- `blind-2.html`: `053c607c2f0e047d9e4e4a474c3d6787e10c5b91f6181b32024e0bf245c3a33e`

## 1회

### p1:a (exact)

$v_3=v_1+v_2$이므로 $v_1+v_2-v_3=0$. 계수 $(1,1,-1)$은 비영이어서 세 열은 선형종속이다. $v_1,v_2$는 첫째·둘째 성분으로 독립임을 바로 확인한다.

### p1:b (exact)

첫 두 행은 $\alpha_1+\alpha_3=2$, $\alpha_2+\alpha_3=1$을 준다. 셋째 행은 이 둘의 합이므로 $\alpha=(2-s,1-s,s)^\top$, $s\in\mathbb R$가 모든 해다. 모든 열의 셋째 성분이 첫 두 성분의 합이므로 열공간은 $\{(u,v,u+v)^\top\}$. $c=(2,1,4)^\top$는 이 평면 밖이어서 해가 없다.

### p1:c (exact)

$U^\top U=\begin{pmatrix}2&1\\1&2\end{pmatrix}$이고 행렬식이 $3$이므로 $(U^\top U)^{-1}=\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$. $V^\top V=\begin{pmatrix}2&1&3\\1&2&3\\3&3&6\end{pmatrix}$는 비영 벡터 $(1,1,-1)^\top$를 영벡터로 보내므로 역행렬이 없다. Gram 행렬의 가역성은 행이 아니라 열의 독립성에 달렸다.

### p2:a (symbolic)

$J_f(x)=\begin{pmatrix}2x_1&1\\x_2&x_1\end{pmatrix}$, $J_f(1,2)=\begin{pmatrix}2&1\\2&1\end{pmatrix}$. 두 입력·두 출력이므로 모두 $2\times2$이다.

### p2:b (symbolic)

$q=2x_1^2+x_1x_2+x_2^2-x_1$. 따라서 열 gradient는 $\nabla q=(4x_1+x_2-1,\ x_1+2x_2)^\top\in\mathbb R^2$, Hessian은 $\nabla^2q=A=\begin{pmatrix}4&1\\1&2\end{pmatrix}\in\mathbb R^{2\times2}$이다.

### p2:c (proof)

$4x_1+x_2=1$, $x_1+2x_2=0$에서 $x_*=(2/7,-1/7)^\top$. $A$의 선행 주행렬식은 $4>0$, $\det A=7>0$이어서 양의 정부호다. $q(x)-q(x_*)=\frac12(x-x_*)^\top A(x-x_*)>0$ ($x\ne x_*$)이므로 유일한 전역 최소점이다.

### p3:a (exact)

$z^2+(z-2)^2/3=\frac43z^2-\frac43z+\frac43=\frac43(z-\frac12)^2+1$. 따라서 $g(z)=\frac1{2\pi\sqrt3}e^{-1/2}\exp[-\frac23(z-\frac12)^2]$.

### p3:b (exact)

정밀도가 $4/3$이므로 평균 $1/2$, 분산 $3/4$다. $q(z)=\frac1{\sqrt{2\pi(3/4)}}\exp[-(z-1/2)^2/(2(3/4))]=\sqrt{\frac2{3\pi}}\exp[-\frac23(z-1/2)^2]$. 이 앞 계수는 Gaussian 적분에 의해 적분값을 1로 만든다.

### p3:c (exact)

$\int\exp[-\frac23(z-1/2)^2]dz=\sqrt{3\pi/2}$이므로 $Z=\frac{e^{-1/2}}{\sqrt{8\pi}}=\mathcal N(2\mid0,4)$. $Z\ne1$이므로 비음수인 $g$ 자체는 정규화된 확률밀도가 아니다. $g/Z$가 밀도다.

### p4:a (exact)

$\Phi=\begin{pmatrix}1&-1\\1&0\\1&1\end{pmatrix}\in\mathbb R^{3\times2}$, $y=(0,1,4)^\top$, $\Phi^\top\Phi=\operatorname{diag}(3,2)$, $\Phi^\top y=(5,4)^\top$.

### p4:b (exact)

분산 1의 독립 Gaussian 우도의 최대화는 잔차제곱합 최소화다. $\Phi^\top\Phi\theta=\Phi^\top y$에서 $\theta_{ML}=(5/3,2)^\top$. $\phi(2)=(1,2)^\top$이므로 평균 예측은 $5/3+2\cdot2=17/3$.

### p4:c (exact)

음의 로그 posterior의 가변항은 $\frac12\|y-\Phi\theta\|^2+\frac12\|\theta\|^2$. 따라서 $(\Phi^\top\Phi+I)\theta=\Phi^\top y$, $\theta_{MAP}=(5/4,4/3)^\top$. 평균 예측은 $5/4+2(4/3)=47/12$. 영평균 prior의 이차벌점이 절편과 기울기를 모두 0 방향으로 수축시킨다.

### p5:a (exact)

$\mu_X=(2/3,2/3)^\top$. $E[XX^\top]=\operatorname{diag}(4/3,4/3)$이므로 $\Sigma_X=E[XX^\top]-\mu_X\mu_X^\top=\begin{pmatrix}8/9&-4/9\\-4/9&8/9\end{pmatrix}$. 이는 분모 3을 쓴 결과이며 불편표본공분산의 분모 2와 다르다.

### p5:b (exact)

$Y-\mu_Y=A(X-\mu_X)$에서 $\mu_Y=A\mu_X+b=(7/3,-1)^\top$, $\Sigma_Y=A\Sigma_XA^\top=\operatorname{diag}(8/9,8/3)$. 정의된 교차공분산의 순서에 따라 $C_{XY}=\Sigma_XA^\top=\begin{pmatrix}4/9&4/3\\4/9&-4/3\end{pmatrix}$이며 세 행렬은 모두 $2\times2$다. 이동 $b$는 공분산에 영향을 주지 않는다.

### p5:c (proof)

가능한 $Y$는 $(1,-1)^\top,(3,1)^\top,(3,-3)^\top$이고 각각 확률 $1/3$이다. 공분산의 비대각 원소가 0이므로 무상관이다. 그러나 $P(Y_1=1)=1/3$, $P(Y_2=1)=1/3$인데 $P(Y_1=1,Y_2=1)=0\ne1/9$. 따라서 독립은 아니다. 이산분포에 Gaussian의 무상관-독립 정리를 적용할 수 없다.

### p6:a (proof)

$y_n\mid x_n,\theta\sim\mathcal N(\theta_0+\theta_1x_n,\sigma^2)$. 입력과 모수를 고정하면 각 $y_n$은 서로 독립인 $\epsilon_n$에 각각 상수만 더한 값이므로 조건부 독립이다. 따라서 결합밀도는 각 조건부 밀도의 곱이다.

### p6:b (symbolic)

$p(y\mid\Phi,\theta)=\prod_{n=1}^N\frac1{\sqrt{2\pi\sigma^2}}e^{-(y_n-\phi(x_n)^\top\theta)^2/(2\sigma^2)}=(2\pi\sigma^2)^{-N/2}e^{-\|y-\Phi\theta\|^2/(2\sigma^2)}$. $\mathcal L(\theta)=\frac N2\log(2\pi\sigma^2)+\frac1{2\sigma^2}\|y-\Phi\theta\|^2$. $\Phi$는 $N\times2$, $y$는 $N\times1$이다.

### p6:c (proof)

$\mathcal L(\theta)=C+\frac{N}{2\sigma^2}\widehat R(\theta)$, $C=\frac N2\log(2\pi\sigma^2)$. $\sigma^2>0$, $N>0$이고 $C$는 모수와 무관하므로 양의 상수배와 상수 이동은 최소점 집합을 보존한다. 따라서 ML은 제곱손실 경험위험 최소화와 같다.

### p6:d (symbolic)

$Q=\|y-\Phi\theta\|^2=y^\top y-2\theta^\top\Phi^\top y+\theta^\top\Phi^\top\Phi\theta$. $G=\Phi^\top\Phi$는 대칭이므로 $\nabla_\theta Q=-2\Phi^\top y+2G\theta\in\mathbb R^2$. 따라서 $G\theta=\Phi^\top y$가 정규방정식이다. 경험위험의 gradient는 이 식을 $N$으로 나눈 것이다.

### p6:e (proof)

열독립에 의해 비영 $h$에 대해 $h^\top Gh=\|\Phi h\|^2>0$이므로 $G$는 가역이며 $\theta_{ML}=G^{-1}\Phi^\top y$. Hessian $2G$가 양의 정부호이므로 유일한 전역 최소점이다. $(1,x,x^2)^\top$로 바꾸면 평균은 $\theta_0+\theta_1x+\theta_2x^2$로 입력에는 비선형이지만 미지 계수에는 선형이어서 선형 회귀다. 새 특징행렬에 대한 해의 유일성은 새 열들의 독립성을 별도로 요구한다.

### p7:a (symbolic)

Bayes 정리에서 $p(\theta\mid y,\Phi)=p(y\mid\Phi,\theta)p(\theta)/p(y\mid\Phi)\propto p(y\mid\Phi,\theta)p(\theta)$. Evidence $p(y\mid\Phi)=\int_{\mathbb R^K}p(y\mid\Phi,\vartheta)p(\vartheta)d\vartheta$는 모수를 적분한 값으로 현재의 $\theta$에는 의존하지 않는다.

### p7:b (symbolic)

곱은 $(2\pi\sigma^2)^{-N/2}(2\pi\tau^2)^{-K/2}\exp[-\|y-\Phi\theta\|^2/(2\sigma^2)-\|\theta-m_0\|^2/(2\tau^2)]$. 따라서 음의 로그 posterior는 $\frac1{2\sigma^2}\|y-\Phi\theta\|^2+\frac1{2\tau^2}\|\theta-m_0\|^2+C$, $C=\frac N2\log(2\pi\sigma^2)+\frac K2\log(2\pi\tau^2)+\log p(y\mid\Phi)$. $C$는 $\theta$와 무관하다.

### p7:c (symbolic)

첫 이차항의 열 gradient는 $\sigma^{-2}\Phi^\top(\Phi\theta-y)$이고, 둘째는 $\tau^{-2}(\theta-m_0)$. 합을 0으로 두면 $(\sigma^{-2}\Phi^\top\Phi+\tau^{-2}I_K)\theta=\sigma^{-2}\Phi^\top y+\tau^{-2}m_0$. 양변은 $K\times1$이다.

### p7:d (symbolic)

$\lambda=\sigma^2/\tau^2>0$로 두면 $\theta_{MAP}=(\Phi^\top\Phi+\lambda I_K)^{-1}(\Phi^\top y+\lambda m_0)$. 음의 로그 posterior를 $2\sigma^2$배 하면 가변항이 $\|y-\Phi\theta\|^2+\lambda\|\theta-m_0\|^2$가 된다. 따라서 이 합에서 상대 벌점계수는 $\lambda=\sigma^2/\tau^2$다.

### p7:e (proof)

임의의 비영 $h\in\mathbb R^K$에 대해 $h^\top(\Phi^\top\Phi+\lambda I_K)h=\|\Phi h\|^2+\lambda\|h\|^2>0$. 따라서 행렬은 양의 정부호여서 열독립 없이도 가역이고 MAP은 유일하다. 핵심 조건은 $\lambda>0$이며 $\lambda=0$에는 이 증명이 적용되지 않는다.

### p7:f (exact)

$G=\begin{pmatrix}5&5\\5&5\end{pmatrix}$, $\Phi^\top y=(5,5)^\top$. $\lambda=1$에서 $(G+I)^{-1}=\frac1{11}\begin{pmatrix}6&-5\\-5&6\end{pmatrix}$이므로 $\theta_{MAP}=(5/11,5/11)^\top$. $\lambda=0$이면 $\theta_1+\theta_2=1$인 모든 벡터가 최소제곱해이므로 유일하지 않다. $\lambda>0$의 해는 $(5/(10+\lambda),5/(10+\lambda))^\top$로 $\lambda\to\infty$에 $(0,0)^\top=m_0$로 간다. 참고로 $\lambda\to0^+$에서는 $(1/2,1/2)^\top$인 최소노름 해를 고른다.

### p8:a (symbolic)

모수에 조건부로 관측들이 독립이므로 곱은 $\mathcal N(2\mid\theta,2)\mathcal N(0\mid\theta,2)\mathcal N(\theta\mid1,2)=(4\pi)^{-3/2}\exp[-\{(2-\theta)^2+\theta^2+(\theta-1)^2\}/4]$. 모수와 무관한 양의 앞 계수를 제외하면 뒤 지수식이다.

### p8:b (exact)

제곱합은 $3\theta^2-6\theta+5$. 따라서 지수는 $-\frac12[\frac32\theta^2-2(\frac32)\theta+\frac52]$로 $A=3/2$, $b=3/2$, $c=5/2$. $A>0$이므로 정규화 가능한 Gaussian 핵이다.

### p8:c (exact)

$A\theta^2-2b\theta+c=\frac32(\theta-1)^2+1$. 모수와 무관한 $e^{-1/2}$는 정규화 시 사라진다. $\int e^{-3(\theta-1)^2/4}d\theta=\sqrt{4\pi/3}$이므로 $p(\theta\mid D)=\sqrt{\frac3{4\pi}}e^{-3(\theta-1)^2/4}=\mathcal N(\theta\mid1,2/3)$. 평균 1, 분산 $2/3$다.

### p8:d (exact)

선형변환 $f_*=2\theta$는 Gaussian을 보존한다. $E[f_*\mid D]=2E[\theta\mid D]=2$, $\operatorname{Var}(f_*\mid D)=4\operatorname{Var}(\theta\mid D)=8/3$. 따라서 $f_*\mid D\sim\mathcal N(2,8/3)$. 밀도 계수는 $1/\sqrt{2\pi(8/3)}$이다.

### p8:e (exact)

독립 미래 잡음의 평균은 0, 분산은 2이므로 $E[y_*\mid D]=2$, $\operatorname{Var}(y_*\mid D)=8/3+2=14/3$. 두 독립 Gaussian의 합이어서 $y_*\mid D\sim\mathcal N(2,14/3)$이며 정규화 계수는 $1/\sqrt{2\pi(14/3)}$이다.

### p8:f (proof)

Gaussian posterior의 유일한 최빈값은 평균과 같아 $\theta_{MAP}=1$. 이를 고정하면 $y_*\mid\theta_{MAP}\sim\mathcal N(2,2)$. 완전한 posterior 예측 $\mathcal N(2,14/3)$와 평균은 같지만 분산은 $8/3$ 작다. 이 차이는 $\operatorname{Var}(E[y_*\mid\theta,D]\mid D)=4\operatorname{Var}(\theta\mid D)=8/3$, 즉 모수의 사후 불확실성이다.

### p9:a (symbolic)

$p(y\mid M_j)=\int_{\mathbb R}\mathcal N(y\mid\theta,1)\mathcal N(\theta\mid0,v_j)d\theta$. 이는 결합밀도 $p(y,\theta\mid M_j)$를 주변화한 것이므로 prior로 가중한다. 같은 데이터를 이미 조건화한 posterior를 넣으면 이 주변화 정의와 달라져 데이터를 이중 사용하게 된다.

### p9:b (symbolic)

$v=v_j>0$로 두면 $(y-\theta)^2+\theta^2/v=\frac{v+1}{v}(\theta-\frac{v y}{v+1})^2+\frac{y^2}{v+1}$. 곱의 앞 계수는 $1/(2\pi\sqrt v)$, 완전제곱 핵의 적분은 $\sqrt{2\pi v/(v+1)}$. 따라서 $p(y\mid M_j)=\frac1{\sqrt{2\pi(v_j+1)}}e^{-y^2/[2(v_j+1)]}=\mathcal N(y\mid0,v_j+1)$.

### p9:c (exact)

$y=0$에서 $p(0\mid M_1)=1/\sqrt{4\pi}=1/(2\sqrt\pi)$, $p(0\mid M_2)=1/\sqrt{10\pi}$. 이 값들은 연속관측의 밀도값이며 $P(y=0)$라는 점확률은 아니다.

### p9:d (exact)

$B_{12}=p(0\mid M_1)/p(0\mid M_2)=\sqrt{5/2}>1$. 따라서 관측 데이터 자체의 evidence 비교는 $M_1$을 지지한다.

### p9:e (proof)

$P(M_j\mid y)=p(y\mid M_j)P(M_j)/p(y)$를 나누면 $\frac{P(M_1\mid y)}{P(M_2\mid y)}=B_{12}\frac{P(M_1)}{P(M_2)}=\frac12\sqrt{5/2}=\sqrt{5/8}<1$. 따라서 $P(M_1\mid0)=\frac{\sqrt5}{\sqrt5+2\sqrt2}$, $P(M_2\mid0)=\frac{2\sqrt2}{\sqrt5+2\sqrt2}$이다. posterior 최대확률 기준의 선택은 $M_2$다. 모델 공간이 두 모델임을 전제로 정규화했다.

### p10:a (proof)

$r=y-\Phi\widehat\theta$라 하면 $\|r-t\Phi h\|^2=\|r\|^2-2t h^\top\Phi^\top r+t^2\|\Phi h\|^2$. 최근접점에서 모든 $h\in\mathbb R^K$에 대해 도함수 $-2h^\top\Phi^\top r=0$. 특히 $h=\Phi^\top r$를 택하면 $\Phi^\top r=0$, 즉 잔차는 열공간의 모든 벡터에 직교한다.

### p10:b (symbolic)

$\Phi^\top(y-\Phi\widehat\theta)=0$에서 $\Phi^\top\Phi\widehat\theta=\Phi^\top y$. 열독립이면 $G=\Phi^\top\Phi$가 양의 정부호로 가역이므로 $\widehat\theta=G^{-1}\Phi^\top y\in\mathbb R^K$. 이 문제에서 $N=3,K=2$.

### p10:c (proof)

대입하면 $P=\Phi(\Phi^\top\Phi)^{-1}\Phi^\top\in\mathbb R^{N\times N}$이고 $\widehat y=Py$. $G$가 대칭이어서 $(G^{-1})^\top=G^{-1}$, 따라서 $P^\top=P$. 또한 $P^2=\Phi G^{-1}(\Phi^\top\Phi)G^{-1}\Phi^\top=P$. 주어진 문제에서 차원은 $3\times3$이며 rank는 2다.

### p10:d (exact)

$G=\operatorname{diag}(3,2)$, $\Phi^\top y=(4,2)^\top$이므로 $\widehat\theta=(4/3,1)^\top$. $P=\begin{pmatrix}1/3&1/3&1/3\\1/3&5/6&-1/6\\1/3&-1/6&5/6\end{pmatrix}$, $\widehat y=(4/3,7/3,1/3)^\top$, $r=(2/3,-1/3,-1/3)^\top$. 실제 $\Phi^\top r=(2/3-1/3-1/3,\ -1/3+1/3)^\top=0$.

### p10:e (proof)

$u,\widehat y\in\operatorname{col}(\Phi)$이므로 $\widehat y-u$도 열공간에 있고 $r^\top(\widehat y-u)=0$. 따라서 $\|y-u\|^2=\|r+(\widehat y-u)\|^2=\|r\|^2+\|\widehat y-u\|^2\ge\|r\|^2$. 등호는 $u=\widehat y$일 때만 성립한다. 이는 (a)의 필요조건을 충분조건으로 완성하고 열공간 내 최근접점의 유일성도 보인다.


## 2회

### p1:a (symbolic)

$V(t)=\begin{pmatrix}1&0&1\\0&1&1\\1&1&t\end{pmatrix}$. 셋째 행에서 첫째·둘째 행을 빼면 마지막 대각원소가 $t-2$인 상삼각행렬이 되므로 $\det V(t)=t-2$. 따라서 세 열이 $\mathbb R^3$의 기저가 되는 필요충분조건은 $t\ne2$다.

### p1:b (exact)

$t=2$에서 셋째 열은 앞 두 열의 합. 첫 두 행이 $\alpha_1+\alpha_3=1$, $\alpha_2+\alpha_3=2$이므로 $\alpha=(1-s,2-s,s)^\top$ ($s\in\mathbb R$). 셋째 성분은 항상 첫 두 성분의 합 3이어서 $(1,2,4)^\top$는 열공간 밖이며 해가 없다.

### p1:c (exact)

앞 두 행으로 $\alpha_1=1-\alpha_3$, $\alpha_2=2-\alpha_3$. 셋째 행에 넣으면 $3+\alpha_3=4$이므로 $\alpha=(0,1,1)^\top$. $t=3$이면 행렬식 1로 열공간이 $\mathbb R^3$ 전체지만 $t=2$이면 $z=x+y$ 평면이다. 따라서 같은 우변도 전자는 유일해, 후자는 해 없음이다.

### p2:a (symbolic)

$J_f(x)=\begin{pmatrix}1&1\\x_2&x_1\end{pmatrix}$, $J_f(1,2)=\begin{pmatrix}1&1\\2&1\end{pmatrix}$. 둘 다 $2\times2$다.

### p2:b (symbolic)

$\nabla_z\ell(z)=z-(1,2)^\top$, $f(1,2)=(3,2)^\top$이다. 열 gradient의 연쇄법칙은 $\nabla_xL=J_f^\top\nabla_z\ell(f(x))$이므로 점 $(1,2)$에서 $J_f^\top(2,0)^\top=(2,2)^\top$. 직접 전개하면 $L=\frac12[(x_1+x_2-1)^2+(x_1x_2-2)^2]$이고 gradient는 $(a+x_2b,\ a+x_1b)^\top$, $a=x_1+x_2-1,b=x_1x_2-2$로 같은 결과다.

### p2:c (proof)

$D_dL=\nabla L(1,2)^\top d=(2,2)(1,-1)^\top=0$. 직접 경로에서는 $L(1+h,2-h)=2+\frac12(h-h^2)^2$로 미분값 0이다. 그러나 gradient $(2,2)^\top\ne0$여서 정지점은 아니다. 한 방향의 미분이 0이라는 것은 gradient와 그 방향이 직교한다는 뜻이며 모든 방향의 미분이 0인 조건보다 약하다.

### p3:a (exact)

$E[Y]=A\mu+b=(0,4)^\top$. $\operatorname{Cov}(Y)=A\Sigma A^\top=\begin{pmatrix}6&0\\0&2\end{pmatrix}$. 이들은 각각 $2\times1$, $2\times2$이며 $\det A=-2\ne0$이어서 변환 후에도 비퇴화 Gaussian이다.

### p3:b (exact)

$Y_1\sim\mathcal N(0,6)$, $Y_2\sim\mathcal N(4,2)$로 주변밀도는 각각 $\frac1{\sqrt{12\pi}}e^{-y_1^2/12}$, $\frac1{\sqrt{4\pi}}e^{-(y_2-4)^2/4}$. 결합 공분산 행렬식은 12이므로 $p_Y(y_1,y_2)=\frac1{2\pi\sqrt{12}}e^{-\frac12[y_1^2/6+(y_2-4)^2/2]}=\frac1{4\pi\sqrt3}e^{-y_1^2/12-(y_2-4)^2/4}$.

### p3:c (proof)

$Y$는 Gaussian의 아핀변환이므로 결합 Gaussian이며 공분산이 대각이다. (b)의 결합밀도가 주변밀도의 곱으로 분해되어 $Y_1,Y_2$는 독립이다. 반면 $\operatorname{Cov}(X_1,X_2)=1\ne0$이므로 $X_1,X_2$는 독립일 수 없다. 유한 이차모멘트를 가진 독립 확률변수라면 공분산이 0이어야 하기 때문이다.

### p4:a (exact)

$g(\theta)=\frac1{4\pi}\exp[-\frac12\{(\theta+1)^2/2+(3-\theta)^2/2\}]$. 중괄호 안은 $\theta^2-2\theta+5=(\theta-1)^2+4$. 따라서 $g(\theta)=\frac{e^{-2}}{4\pi}e^{-(\theta-1)^2/2}$.

### p4:b (exact)

$\int e^{-(\theta-1)^2/2}d\theta=\sqrt{2\pi}$이므로 posterior는 $p(\theta\mid3)=\frac1{\sqrt{2\pi}}e^{-(\theta-1)^2/2}=\mathcal N(\theta\mid1,1)$. 평균 1, 분산 1이다. 우도만 최대화하면 $\theta_{ML}=3$이고 posterior 최빈값은 $\theta_{MAP}=1$.

### p4:c (exact)

$Z=e^{-2}\sqrt{2\pi}/(4\pi)=e^{-2}/\sqrt{8\pi}=\mathcal N(3\mid-1,4)$. Evidence는 모수에 대해 적분한 결과로, 고정 관측 $y=3$에 대한 하나의 밀도값이다. Posterior는 관측을 고정하고 모수 $\theta$에 대한 적분값이 1인 함수이다. $Z$는 관측 $y$를 변수로 보면 정규화된 주변밀도의 한 값이며 모수 posterior 자체와는 다르다.

### p5:a (exact)

$\Phi=\begin{pmatrix}1&1\\1&0\\1&1\end{pmatrix}$, $G=\Phi^\top\Phi=\begin{pmatrix}3&2\\2&2\end{pmatrix}$, $\Phi^\top y=(6,6)^\top$. $\det G=6-4=2>0$이므로 가역이고 $G^{-1}=\frac12\begin{pmatrix}2&-2\\-2&3\end{pmatrix}$. 두 행의 중복은 열독립을 방해하지 않는다. 실제 열 $(1,1,1)^\top,(1,0,1)^\top$는 독립이다.

### p5:b (exact)

$\theta_{ML}=G^{-1}(6,6)^\top=(0,3)^\top$, $\widehat y=(3,0,3)^\top$. 잔차를 $r=y-\widehat y$로 두면 $r=(-1,0,1)^\top$이고 RSS는 $1+0+1=2$. $\phi(2)=(1,4)^\top$에서 평균 예측은 $12$.

### p5:c (exact)

$(G+I)\theta_{MAP}=(6,6)^\top$이며 $G+I=\begin{pmatrix}4&2\\2&3\end{pmatrix}$, 역행렬은 $\frac18\begin{pmatrix}3&-2\\-2&4\end{pmatrix}$. 따라서 $\theta_{MAP}=(3/4,3/2)^\top$, 평균 예측은 $3/4+4(3/2)=27/4$. 모델 평균 $\theta_0+\theta_1x^2$가 미지 계수에 선형이므로 선형 회귀다.

### p6:a (symbolic)

$y_n\mid x_n,\theta\sim\mathcal N(\theta x_n,\sigma^2)$. 서로 독립 잡음에 각각 고정 평균을 더한 관측은 조건부 독립이므로 $p(y\mid x,\theta)=(2\pi\sigma^2)^{-N/2}\exp[-\sum_n(y_n-\theta x_n)^2/(2\sigma^2)]$. $x,y$는 $N\times1$이고 $\theta$는 스칼라다.

### p6:b (symbolic)

음의 로그우도는 $\frac N2\log(2\pi\sigma^2)+\frac1{2\sigma^2}\sum_n(y_n-\theta x_n)^2$. 첫 항은 모수와 무관하고 둘째 항의 상수배는 양수이므로 ML은 $Q(\theta)=\sum_n(y_n-\theta x_n)^2$ 최소화와 같다.

### p6:c (symbolic)

$Q=y^\top y-2\theta\sum_nx_ny_n+\theta^2\sum_nx_n^2$. $Q'=-2\sum_nx_ny_n+2\theta\sum_nx_n^2=0$에서 $\widehat\theta=\frac{\sum_nx_ny_n}{\sum_nx_n^2}$. 주어진 $\sum_nx_n^2>0$가 분모를 보장한다. 이 조건이 없으면 실수 입력 전부가 0이고 목적함수는 모수와 무관해진다.

### p6:d (proof)

$Q''=2\sum_nx_n^2>0$이므로 스칼라 이차함수는 엄격히 볼록하고 (c)의 점이 유일한 전역 최소점이다. 음의 로그우도의 이계미분도 $\sigma^{-2}\sum_nx_n^2>0$. 내적 표기로 $\widehat\theta=(x^\top y)/(x^\top x)$다.

### p6:e (proof)

$\widehat y=x(x^\top y)/(x^\top x)=Py$, $P=xx^\top/(x^\top x)\in\mathbb R^{N\times N}$. 따라서 $x^\top(y-\widehat y)=x^\top y-(x^\top x)(x^\top y)/(x^\top x)=0$. 잔차는 $x$가 생성하는 1차원 열공간에 직교한다. $P^\top=P$, $P^2=P$도 즉시 확인된다.

### p6:f (exact)

$x^\top x=6$, $x^\top y=7$이므로 $\widehat\theta=7/6$, $\widehat y=(7/6,7/3,-7/6)^\top$. 잔차는 $(-1/6,2/3,7/6)^\top$이며 RSS $=1/36+4/9+49/36=11/6$. $P=\frac16\begin{pmatrix}1&2&-1\\2&4&-2\\-1&-2&1\end{pmatrix}$를 $y$에 곱해도 같은 예측을 얻는다.

### p7:a (symbolic)

Likelihood는 $(2\pi\sigma^2)^{-1}e^{-\|y-\Phi\theta\|^2/(2\sigma^2)}$, prior는 $(2\pi)^{-1}|S_0|^{-1/2}e^{-(\theta-m_0)^\top S_0^{-1}(\theta-m_0)/2}$이다. Bayes 정리로 $-\log p(\theta\mid y,\Phi)=\frac1{2\sigma^2}\|y-\Phi\theta\|^2+\frac12(\theta-m_0)^\top S_0^{-1}(\theta-m_0)+C$. 여기서 $C=\log(2\pi\sigma^2)+\log(2\pi)+\frac12\log|S_0|+\log p(y\mid\Phi)$는 모수와 무관하다.

### p7:b (symbolic)

두 항의 열 gradient는 각각 $\sigma^{-2}\Phi^\top(\Phi\theta-y)$와 $S_0^{-1}(\theta-m_0)$다. Gaussian 지수의 거리척도가 공분산 역행렬인 정밀도이기 때문에 미분 후에도 $S_0^{-1}$가 등장한다. $S_0^{-1}=\operatorname{diag}(1/4,1)$이므로 둘째 계수의 prior 편차에 더 큰 벌점이 붙는다.

### p7:c (symbolic)

합을 0으로 두면 $(\sigma^{-2}\Phi^\top\Phi+S_0^{-1})\theta=\sigma^{-2}\Phi^\top y+S_0^{-1}m_0$. 따라서 $\theta_{MAP}=(\sigma^{-2}\Phi^\top\Phi+S_0^{-1})^{-1}(\sigma^{-2}\Phi^\top y+S_0^{-1}m_0)$. 동치형은 $(\Phi^\top\Phi+\sigma^2 S_0^{-1})^{-1}(\Phi^\top y+\sigma^2 S_0^{-1}m_0)$. 행렬은 $2\times2$, 벡터는 $2\times1$이다.

### p7:d (proof)

비영 $h\in\mathbb R^2$에 대해 $h^\top(\sigma^{-2}\Phi^\top\Phi+S_0^{-1})h=\sigma^{-2}\|\Phi h\|^2+h^\top S_0^{-1}h>0$. $S_0=\operatorname{diag}(4,1)$은 양의 정부호이고 $\sigma^2>0$이므로 Hessian이 양의 정부호다. 따라서 계수행렬이 가역이고 MAP은 유일한 전역 최소점이다.

### p7:e (exact)

$\Phi^\top\Phi=2I_2$, $\Phi^\top y=(4,4)^\top$, $S_0^{-1}m_0=(1/2,0)^\top$. $\sigma^2=1$에서 계수행렬은 $\operatorname{diag}(9/4,3)$, 우변 $(9/2,4)^\top$이므로 $\theta_{MAP}=(2,4/3)^\top$. $\phi(2)=(1,2)^\top$의 평균은 $14/3$. ML은 $(2,2)^\top$이며 같은 입력의 평균은 6이다. 첫 계수는 ML과 prior 평균이 모두 2여서 그대로이고 둘째 계수는 prior 평균 0 쪽으로 수축한다.

### p7:f (symbolic)

$s=\sigma^2>0$로 쓰면 첫 성분은 $(4+s/2)/(2+s/4)=2$, 둘째는 $4/(2+s)$. 따라서 $\theta_{MAP}(s)=(2,4/(2+s))^\top$. $s\to0^+$에서는 $(2,2)^\top=\theta_{ML}$, $s\to\infty$에서는 $(2,0)^\top=m_0$. 잡음분산이 작으면 우도에, 크면 prior에 상대적으로 큰 무게가 실린다.

### p8:a (symbolic)

곱은 $(4\pi)^{-1}(2\pi)^{-1}\exp[-\frac12\{\frac12(y-\Phi\theta)^\top(y-\Phi\theta)+\theta^\top\theta\}]$. 전개하면 $B=I_2+\frac12\Phi^\top\Phi$, $b=\frac12\Phi^\top y$, $c=\frac12y^\top y$이고 지수는 $-\frac12(\theta^\top B\theta-2b^\top\theta+c)$. $B$는 $2\times2$, $b$는 $2\times1$, $c$는 스칼라다.

### p8:b (proof)

$B$는 $I_2$와 양의 준정부호 Gram 항의 합이므로 양의 정부호다. $m=B^{-1}b$, $S=B^{-1}$로 놓으면 $\theta^\top B\theta-2b^\top\theta+c=(\theta-m)^\top B(\theta-m)+c-b^\top B^{-1}b$. 마지막 항은 정규화 시 상쇄되어 $p(\theta\mid y)=\frac1{(2\pi)^{2/2}|S|^{1/2}}\exp[-\frac12(\theta-m)^\top S^{-1}(\theta-m)]$. 정규화 계수는 $|B|^{1/2}/(2\pi)$와 같다.

### p8:c (exact)

$\Phi^\top\Phi=2I_2$, $\Phi^\top y=(2,2)^\top$, $y^\top y=4$. 따라서 $B=2I_2$, $b=(1,1)^\top$, $c=2$, $m=(1/2,1/2)^\top$, $S=\frac12I_2$. 완전제곱의 상수 잔여항은 $c-b^\top B^{-1}b=1$이다. 정규화된 posterior는 $p(\theta\mid y)=\pi^{-1}\exp[-\|\theta-(1/2,1/2)^\top\|^2]$.

### p8:d (symbolic)

Gaussian의 선형함수이므로 $f_*\mid y\sim\mathcal N(\phi_*^\top m,\phi_*^\top S\phi_*)$. 평균식은 기대값의 선형성에서, 분산식은 $E[\phi_*^\top(\theta-m)(\theta-m)^\top\phi_*\mid y]$에서 나온다. 이 데이터에서는 $\phi(x)=(1,x)^\top$일 때 평균 $(1+x)/2$, 분산 $(1+x^2)/2$. $x_*=1$에서는 $f_*\mid y\sim\mathcal N(1,1)$. 임의의 영벡터 $\phi_*=0$이면 분산 0의 퇴화 점질량으로 해석한다.

### p8:e (proof)

독립 미래 잡음의 분산 2를 더하면 $y_*\mid y\sim\mathcal N(\phi_*^\top m,2+\phi_*^\top S\phi_*)$. $x_*=1$에서는 $\mathcal N(1,3)$. MAP은 $m=(1/2,1/2)^\top$이므로 이를 고정 대입한 분포는 $\mathcal N(1,2)$다. 완전한 예측의 추가 분산 1은 $\phi_*^\top S\phi_*$인 모수의 사후 불확실성이다.

### p8:f (proof)

서로 다른 두 미래 잡음은 조건부 교차공분산 0이고 모수와 독립이다. 따라서 $\operatorname{Cov}(y_{0}^{new},y_{1}^{new}\mid y)=\operatorname{Cov}(\phi(0)^\top\theta,\phi(1)^\top\theta\mid y)=\phi(0)^\top S\phi(1)=1/2$. 전체공분산 법칙으로도 $E[0\mid y]+\operatorname{Cov}(\phi(0)^\top\theta,\phi(1)^\top\theta\mid y)$이다. 두 미래 관측의 결합분포는 평균 $(1/2,1)^\top$, 공분산 $\begin{pmatrix}5/2&1/2\\1/2&3\end{pmatrix}$의 Gaussian. 모수를 고정하면 독립이지만 같은 미지 모수를 적분한 후에는 이 문제에서 독립이 유지되지 않는다.

### p9:a (symbolic)

$M_1$: $B_1=(1,1)^\top\in\mathbb R^{2\times1}$, $\vartheta_1=\theta\sim\mathcal N(0,1)$. $M_2$: $B_2=I_2$, $\vartheta_2=(\theta_1,\theta_2)^\top\sim\mathcal N(0,I_2)$. 두 경우 모두 $p(y\mid M_i)=\int_{\mathbb R^{d_i}}\mathcal N_2(y\mid B_i\vartheta_i,I_2)\mathcal N_{d_i}(\vartheta_i\mid0,I_{d_i})d\vartheta_i$이며 $d_1=1,d_2=2$다.

### p9:b (proof)

$E[y]=B_iE[\vartheta_i]+E[\epsilon]=0$. 정의에서 중심화한 곱을 전개하면 독립성과 영평균으로 교차항이 사라져 $C_i=E[yy^\top]=B_iE[\vartheta_i\vartheta_i^\top]B_i^\top+E[\epsilon\epsilon^\top]=B_iB_i^\top+I_2$. 따라서 $C_1=\begin{pmatrix}2&1\\1&2\end{pmatrix}$, $C_2=2I_2$. 독립 Gaussian 모수·잡음을 함께 쌓은 벡터가 결합 Gaussian이고 $y$는 그 선형변환이므로 Gaussian이다.

### p9:c (exact)

일반 밀도는 $p(y\mid M_i)=(2\pi)^{-1}|C_i|^{-1/2}\exp[-\frac12y^\top C_i^{-1}y]$. $M_1$에서 $|C_1|=3$, $C_1^{-1}=\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$이고 $y=(1,-1)^\top$에 대한 이차형식은 2다. 따라서 $E_1=e^{-1}/(2\pi\sqrt3)$. $M_2$에서는 $|C_2|=4$, $C_2^{-1}=I_2/2$, 이차형식 1이므로 $E_2=e^{-1/2}/(4\pi)$.

### p9:d (exact)

$B_{12}=E_1/E_2=\frac2{\sqrt3}e^{-1/2}<1$. 실제 $B_{12}^2=4/(3e)<1$이다. 따라서 관측 데이터만의 evidence는 서로 반대 부호의 관측을 더 잘 허용하는 $M_2$를 지지한다.

### p9:e (proof)

각 모델의 Bayes 식을 나누면 $\frac{P(M_1\mid y)}{P(M_2\mid y)}=\frac{p(y\mid M_1)}{p(y\mid M_2)}\frac{P(M_1)}{P(M_2)}=2\sqrt3e^{-1/2}>1$. 두 모델만 있으므로 $P(M_1\mid y)=\frac{2\sqrt3e^{-1/2}}{1+2\sqrt3e^{-1/2}}=\frac{2\sqrt3}{\sqrt e+2\sqrt3}$이고 $P(M_2\mid y)=\frac{\sqrt e}{\sqrt e+2\sqrt3}$. posterior 최대확률로는 prior odds가 더해져 $M_1$을 선택한다.

### p10:a (symbolic)

$Q(\theta)=\frac12y^\top y-\theta^\top\Phi^\top y+\frac12\theta^\top G\theta$. $G=\Phi^\top\Phi$가 대칭이므로 $\nabla Q=G\theta-\Phi^\top y$. 따라서 정규방정식은 $G\widehat\theta=\Phi^\top y$이며 $\Phi^\top(y-\Phi\widehat\theta)=0$과 동치다.

### p10:b (exact)

일반적으로 열독립이면 $\widehat\theta=(\Phi^\top\Phi)^{-1}\Phi^\top y$. 주어진 $G=\begin{pmatrix}2&1\\1&2\end{pmatrix}$, $G^{-1}=\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$, $\Phi^\top y=(1,2)^\top$이므로 $\widehat\theta=(0,1)^\top$, $\widehat y=(0,1,1)^\top$, $r=(1,1,-1)^\top$. $\det G=3>0$이고 선행 주행렬식도 2이므로 양의 정부호여서 해는 유일하다.

### p10:c (proof)

$P=\Phi G^{-1}\Phi^\top=\frac13\begin{pmatrix}2&-1&1\\-1&2&1\\1&1&2\end{pmatrix}\in\mathbb R^{3\times3}$. 수치행렬은 대칭이다. $M=3P$라 하면 $M^2=3M$이므로 $P^2=P$. 일반식으로도 $P^2=\Phi G^{-1}GG^{-1}\Phi^\top=P$다. 따라서 열공간으로의 직교투영행렬이다.

### p10:d (exact)

Ridge 목적함수 gradient는 $G\theta-\Phi^\top y+\theta$. 따라서 $(G+I_2)\theta_R=\Phi^\top y$, $\theta_R=(G+I_2)^{-1}\Phi^\top y$. 여기서 $G+I_2=\begin{pmatrix}3&1\\1&3\end{pmatrix}$, 역행렬은 $\frac18\begin{pmatrix}3&-1\\-1&3\end{pmatrix}$이므로 $\theta_R=(1/8,5/8)^\top$. Hessian $G+I_2$는 양의 정부호다.

### p10:e (exact)

$H=\Phi(G+I_2)^{-1}\Phi^\top=\frac18\begin{pmatrix}3&-1&2\\-1&3&2\\2&2&4\end{pmatrix}$, $\widehat y_R=(1/8,5/8,3/4)^\top$, $r_R=(7/8,11/8,-3/4)^\top$. Ridge 정규방정식은 $\Phi^\top r_R=\theta_R$를 준다. 실제 첫 성분 $7/8-3/4=1/8$, 둘째 $11/8-3/4=5/8$. 따라서 여기서는 잔차가 열공간에 직교하지 않으며, 최소제곱의 $\Phi^\top r=0$과 다르다.

### p10:f (proof)

$v=\Phi(1,1)^\top=(1,1,2)^\top$. $Hv=(3/4)v=(3/4,3/4,3/2)^\top$, $H^2v=(9/16)v=(9/16,9/16,9/8)^\top$. $v\ne0$이고 $3/4\ne9/16$이어서 $H^2\ne H$. 반면 $Pv=v$와 $P^2=P$다. $H$는 대칭이지만 멱등이 아니므로 직교투영행렬이 아니다. 대칭성만으로는 부족하고 멱등성이 함께 필요하다.

## 별도 findings

- **rounds 1 and 2 / all subquestions** [info]: 각 유도 사슬은 주어진 가정 및 앞 소문항에서 순서대로 진행 가능했다. 계산을 막는 누락된 차원·정규화 조건·역행렬 조건은 발견하지 못했다.
- **1:p10:a and 1:p10:e** [info]: (a)는 최근접점이라는 임시 가정에서 잔차 직교성의 필요조건을 얻고 (e)는 그 직교성에서 충분성을 증명한다. 이는 순환논증이 아니라 필요조건과 충분조건의 분리다.
- **1:p9:e and 2:p9:e** [info]: 선택할 모델은 posterior 최대확률을 기준으로 해석했다. 별도의 오분류 비용이나 손실함수가 주어지지 않았으므로 이 해석은 합리적이나 문항에 선택 기준을 명시하면 더 정확하다.
- **2:p8:d** [info]: 임의의 phi_*에 영벡터도 포함하면 f_*는 분산 0의 점질량이 되어 일반적인 Lebesgue Gaussian 밀도는 없다. phi(x)=(1,x)^T로 한정하면 항상 비영이어서 이 퇴화 문제는 생기지 않는다.
- **1:p6:e** [info]: 특징을 (1,x,x^2)^T로 바꾸어도 계수에 선형이라는 결론은 항상 가능하다. 그러나 원래 두 특징의 열독립만으로 새 세 특징의 열독립까지 보장되지는 않으므로 새 ML해의 유일성은 별도 가정이 필요하다.
- **all numerical derivation prompts** [info]: 문제의 목표 결론을 조건으로 미리 제공하여 유도를 대신하게 만드는 치명적인 답 노출은 발견하지 못했다. Gram의 열독립, 잡음의 알려진 양의 분산, Gaussian prior의 양의 정부호 공분산은 유도에 필요한 정당한 가정이다.

## 최종 검증

SymPy 정확연산 검증과 입력/결과 개수 검증에서 55개 assertion을 통과했다. 모든 86개 레코드의 conclusion과 method를 확인했으며 작업 종료 시점의 입력 SHA-256을 다시 계산했다.
