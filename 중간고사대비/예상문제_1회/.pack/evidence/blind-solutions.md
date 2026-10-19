# 독립 풀이: 중간고사 예상문제 1회

입력: `blind-input.html`만 읽고 독립적으로 풀었다. 총 10문항, 31개 소문항이다. 답안 대조 또는 정답 비교 통과 판정은 하지 않았다.

## p1

### (a)

선형종속이다. $v_1+v_2-v_3=0$.

각 좌표를 더하면 $(1,0,1)^\top+(0,1,1)^\top-(1,1,2)^\top=(0,0,0)^\top$이다. 계수 $(1,1,-1)^\top$는 영벡터가 아니므로 선형종속이다. 한편 $s v_1+t v_2=(s,t,s+t)^\top=0$이면 $s=t=0$이므로 처음 두 열은 독립이고 $\operatorname{rank}V=2$이다.

### (b)

$\alpha=(2-t,1-t,t)^\top$, $t\in\mathbb R$. $c=(2,1,4)^\top$에는 해가 없다.

$V\alpha=(\alpha_1+\alpha_3,\alpha_2+\alpha_3,\alpha_1+\alpha_2+2\alpha_3)^\top$이다. 첫 두 방정식에서 $\alpha_3=t$라 두면 $\alpha_1=2-t$, $\alpha_2=1-t$이고 셋째 식은 항상 $3$이다. 따라서 이 식이 모든 해다. 열공간은 $\{(s,t,s+t)^\top:s,t\in\mathbb R\}$이므로 $c$의 셋째 좌표 $4$는 첫 두 좌표 합 $3$과 달라 해가 없다.

### (c)

$U^\top U=\begin{pmatrix}2&1\\1&2\end{pmatrix}$, $(U^\top U)^{-1}=\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$. $V^\top V$는 비가역이다.

$v_1^\top v_1=v_2^\top v_2=2$, $v_1^\top v_2=1$이므로 위 Gram 행렬을 얻고 행렬식은 $4-1=3\ne0$이다. 반면 $V^\top V=\begin{pmatrix}2&1&3\\1&2&3\\3&3&6\end{pmatrix}$이고 $(1,1,-1)^\top$에 곱하면 $0$이다. 따라서 $V^\top V$는 영이 아닌 영공간 벡터를 가지며 역행렬이 없다.

## p2

### (a)

$J_f(x)=\begin{pmatrix}2x_1&1\\x_2&x_1\end{pmatrix}$, $J_f(1,2)=\begin{pmatrix}2&1\\2&1\end{pmatrix}$, 둘 다 $2\times2$.

첫 행은 첫 출력 $x_1^2+x_2$를 $x_1,x_2$로 각각 미분한 $(2x_1,1)$이고, 둘째 행은 둘째 출력 $x_1x_2$의 편미분 $(x_2,x_1)$이다. 출력 차원 2와 입력 차원 2에 따라 Jacobian은 $2\times2$다.

### (b)

$q=2x_1^2+x_1x_2+x_2^2-x_1$, $\nabla q=(4x_1+x_2-1,x_1+2x_2)^\top$, $\nabla^2q=A$.

$x^\top Ax=4x_1^2+2x_1x_2+2x_2^2$이고 $b^\top x=x_1$이다. 성분별 미분하면 열 gradient $\begin{pmatrix}4x_1+x_2-1\\x_1+2x_2\end{pmatrix}$를 얻는다. 다시 미분하면 $\begin{pmatrix}4&1\\1&2\end{pmatrix}=A$이며, 대칭 $A$에 대한 일반식 $\nabla q=Ax-b$와 일치한다.

### (c)

$x_*=(2/7,-1/7)^\top$는 유일한 전역 최소점이다.

$4x_1+x_2=1$, $x_1+2x_2=0$에서 $x_1=-2x_2$를 대입하면 $-7x_2=1$이므로 위 해다. 임의의 $h\ne0$에 대해 $h^\top Ah=4(h_1+h_2/4)^2+(7/4)h_2^2>0$이다. $x=x_*+h$를 전개하면 $q(x)-q(x_*)=\frac12h^\top Ah$이고 $h\ne0$일 때 양수이므로 유일한 전역 최소점이다. 최소값은 $q(x_*)=-\frac12b^\top x_*=-1/7$이다.

## p3

### (a)

$z^2+(z-2)^2/3=\frac43(z-\frac12)^2+1$.

왼쪽을 전개하면 $\frac43z^2-\frac43z+\frac43=\frac43(z^2-z+\frac14)+1$이다. 그러므로 완전제곱은 $\frac43(z-\frac12)^2+1$이다.

### (b)

$q=\mathcal N(z\mid1/2,3/4)$이며 $q(z)=\sqrt{2/(3\pi)}\exp[-\frac23(z-\frac12)^2]$.

곱 밀도는 $g(z)=\frac{1}{2\pi\sqrt3}\exp[-\frac12\{\frac43(z-\frac12)^2+1\}]=\frac{e^{-1/2}}{2\pi\sqrt3}\exp[-\frac23(z-\frac12)^2]$다. 지수의 $1/(2v)=2/3$에서 분산은 $v=3/4$, 중심에서 평균은 $m=1/2$이다. 정규화한 Gaussian 계수는 $1/\sqrt{2\pi(3/4)}=\sqrt{2/(3\pi)}$이다.

### (c)

$Z=e^{-1/2}/\sqrt{8\pi}$이며 $g$ 자체는 정규화된 확률밀도가 아니다.

Gaussian 적분으로 $Z=\frac{e^{-1/2}}{2\pi\sqrt3}\sqrt{\frac{3\pi}{2}}=\frac{e^{-1/2}}{2\sqrt{2\pi}}$이다. 이는 $\mathcal N(0\mid2,4)$와도 같다. $g\ge0$이지만 적분이 $1$이 아니므로 그대로 확률밀도라고 부를 수 없고 $q=g/Z$가 밀도다.

## p4

### (a)

$\Phi=\begin{pmatrix}1&-1\\1&0\\1&1\end{pmatrix}$, $\Phi^\top\Phi=\operatorname{diag}(3,2)$, $\Phi^\top y=(5,4)^\top$.

각 행은 $(1,x_n)$이므로 위 $3\times2$ 행렬이다. $\sum1=3$, $\sum x_n=0$, $\sum x_n^2=2$이고, $\sum y_n=5$, $\sum x_ny_n=(-1)0+0\cdot1+1\cdot4=4$다.

### (b)

$\theta_{\rm ML}=(5/3,2)^\top$, $\widehat y(2)=17/3$.

잡음 분산이 1인 독립 Gaussian 우도의 최대화는 $\|y-\Phi\theta\|^2$의 최소화다. 정규방정식으로 $\theta_{\rm ML}=(\Phi^\top\Phi)^{-1}\Phi^\top y=\operatorname{diag}(1/3,1/2)(5,4)^\top=(5/3,2)^\top$. 평균 예측은 $(1,2)\theta_{\rm ML}=5/3+4=17/3$이다.

### (c)

$\theta_{\rm MAP}=(5/4,4/3)^\top$, $\widehat y_{\rm MAP}(2)=47/12$.

prior가 절편까지 포함한 $\mathcal N(0,I_2)$이고 잡음 분산도 1이므로 음의 로그 사후밀도는 상수 외에 $\frac12\|y-\Phi\theta\|^2+\frac12\|\theta\|^2$다. 따라서 $(\Phi^\top\Phi+I_2)\theta=\Phi^\top y$이고 $\theta=(5/4,4/3)^\top$. 예측은 $5/4+2(4/3)=47/12$다. prior가 두 계수를 0 쪽으로 축소하는 벌점을 더하여 ML과 달라진다.

## p5

### (a)

$\mu_X=(2/3,2/3)^\top$, $\Sigma_X=\begin{pmatrix}8/9&-4/9\\-4/9&8/9\end{pmatrix}$.

$E[X]=(x_1+x_2+x_3)/3=(2/3,2/3)^\top$이고 $E[XX^\top]=\operatorname{diag}(4/3,4/3)$이다. 따라서 $\Sigma_X=E[XX^\top]-\mu_X\mu_X^\top=\operatorname{diag}(4/3,4/3)-\frac49\begin{pmatrix}1&1\\1&1\end{pmatrix}$로 주어진다. 이는 분모 3의 공분산이며 분모 2의 불편 표본 공분산을 쓰지 않았다.

### (b)

$\mu_Y=(7/3,-1)^\top$, $\Sigma_Y=\operatorname{diag}(8/9,8/3)$, $C_{XY}=\begin{pmatrix}4/9&4/3\\4/9&-4/3\end{pmatrix}$.

$E[Y]=A\mu_X+b=(4/3,0)^\top+(1,-1)^\top=(7/3,-1)^\top$. 중심화하면 $Y-\mu_Y=A(X-\mu_X)$이므로 $\Sigma_Y=A\Sigma_XA^\top$이고 $C_{XY}=\Sigma_XA^\top$다. 실제 곱셈은 $\Sigma_XA^\top=\frac19\begin{pmatrix}4&12\\4&-12\end{pmatrix}$, $A\Sigma_XA^\top=\frac19\begin{pmatrix}8&0\\0&24\end{pmatrix}$다. 이동 $b$는 공분산에 영향을 주지 않는다.

### (c)

$Y_1,Y_2$는 무상관이지만 독립은 아니다.

가능한 $Y$는 각각 확률 $1/3$로 $(1,-1)^\top$, $(3,1)^\top$, $(3,-3)^\top$다. $\Sigma_Y$의 비대각항이 0이므로 무상관이다. 그러나 $P(Y_1=1)=1/3$, $P(Y_2=1)=1/3$인 반면 $P(Y_1=1,Y_2=1)=0\ne1/9$다. 따라서 독립 조건이 깨진다. 이 분포는 세 점에 질량을 가진 이산분포이므로 Gaussian의 무상관-독립 성질을 적용할 수 없다.

## p6

### (a)

$p(y\mid\Phi,\theta)=(2\pi\sigma^2)^{-N/2}\exp[-\|y-\Phi\theta\|^2/(2\sigma^2)]$.

고정 입력에서 $y_n\mid x_n,\theta\sim\mathcal N(\theta_0+\theta_1x_n,\sigma^2)$다. 잡음의 독립으로 관측은 $\theta,\Phi$를 조건으로 독립이므로 결합우도가 $\prod_{n=1}^N p(y_n\mid x_n,\theta)$로 분해된다. 각 인자는 $(2\pi\sigma^2)^{-1/2}\exp[-(y_n-\theta_0-\theta_1x_n)^2/(2\sigma^2)]$이고, 곱의 상수와 지수를 모으면 위 식이다.

### (b)

$-\log p=\frac N2\log(2\pi\sigma^2)+\frac{1}{2\sigma^2}\sum_n(y_n-\phi(x_n)^\top\theta)^2$이며 ERM과 같은 최소점을 준다.

우도의 로그를 취하고 부호를 바꾸면 정규화 상수에서 $\frac N2\log(2\pi\sigma^2)$, 지수에서 $\frac1{2\sigma^2}\|y-\Phi\theta\|^2$를 얻는다. 경험위험 $\widehat R=\|y-\Phi\theta\|^2/N$이므로 $-\log p=\frac N2\log(2\pi\sigma^2)+\frac N{2\sigma^2}\widehat R$. 알려진 $\sigma^2>0$에서 앞 항은 $\theta$와 무관하고 위험 앞 계수는 양수이므로 argmin이 같다.

### (c)

$\Phi^\top\Phi\theta=\Phi^\top y$, $\theta_{\rm ML}=(\Phi^\top\Phi)^{-1}\Phi^\top y$. 다항 특징도 계수에 대해 선형이므로 선형 회귀다.

열 gradient는 $\nabla_\theta[-\log p]=\sigma^{-2}\Phi^\top(\Phi\theta-y)\in\mathbb R^{2}$이다. 이를 0으로 놓으면 정규방정식이다. 열독립 가정으로 임의의 $v\ne0$에 대해 $v^\top\Phi^\top\Phi v=\|\Phi v\|^2>0$이므로 역행렬이 있고 위 유일해를 얻는다. $\phi(x)=(1,x,x^2)^\top$라면 평균은 $\theta_0+\theta_1x+\theta_2x^2$로 입력에는 비선형일 수 있으나 미지 계수 $\theta$에는 선형이다. 새 특징행렬의 열독립까지 자동 보장되는 것은 아니며, 유일한 역행렬식 해를 쓰려면 그 열독립을 별도로 확인해야 한다.

## p7

### (a)

$L(\theta)=\frac{\|y-\Phi\theta\|^2}{2\sigma^2}+\frac{\|\theta-m_0\|^2}{2\tau^2}+C$, $\lambda=\sigma^2/\tau^2$, $\theta_{\rm MAP}=(\Phi^\top\Phi+\lambda I_K)^{-1}(\Phi^\top y+\lambda m_0)$.

Bayes 법칙에서 사후밀도는 우도와 prior의 곱에 비례한다. 둘의 지수를 더하고 음의 로그를 취하면 주어진 $L$이 나온다. 정확히는 $C=\frac N2\log(2\pi\sigma^2)+\frac K2\log(2\pi\tau^2)+\log p(y\mid\Phi)$이며 $\theta$와 무관하다. 목적함수에 양수 $2\sigma^2$를 곱하면 $\|y-\Phi\theta\|^2+\lambda\|\theta-m_0\|^2$. 미분하여 $\Phi^\top(\Phi\theta-y)+\lambda(\theta-m_0)=0$을 풀면 위 해다. 절편도 prior가 적용되므로 해당 좌표 역시 벌점에 포함한다.

### (b)

$\lambda>0$이면 $\Phi^\top\Phi+\lambda I_K$는 양의 정부호이므로 가역이다.

임의의 $v\in\mathbb R^K\setminus\{0\}$에 대해 $v^\top(\Phi^\top\Phi+\lambda I_K)v=\|\Phi v\|^2+\lambda\|v\|^2>0$이다. 첫 항은 0 이상이고 둘째 항은 엄격히 양수다. 만일 행렬이 비가역이면 영이 아닌 $v$에 대해 행렬 곱이 0이므로 이차형식도 0이 되어 모순이다. 따라서 $\Phi$의 열독립 없이도 가역이고 MAP은 유일하다.

### (c)

$\lambda=1$의 MAP은 $(5/11,5/11)^\top$. $\lambda=0$에서는 $\theta_1+\theta_2=1$인 모든 벡터가 해다. $\lambda\to\infty$이면 $(0,0)^\top$.

$\Phi^\top\Phi=\begin{pmatrix}5&5\\5&5\end{pmatrix}$, $\Phi^\top y=(5,5)^\top$. $\lambda=1$이면 $\begin{pmatrix}6&5\\5&6\end{pmatrix}\theta=(5,5)^\top$이며 두 식을 빼면 $\theta_1=\theta_2$, 따라서 $11\theta_1=5$다. $\lambda=0$에서는 $\Phi\theta=(\theta_1+\theta_2,2(\theta_1+\theta_2))^\top$이므로 잔차제곱은 $5(1-\theta_1-\theta_2)^2$이고 해가 무한히 많다. 일반 $\lambda>0$에서는 $\theta_\lambda=\frac5{10+\lambda}(1,1)^\top$이므로 $\lambda\to\infty$에서 0, 즉 prior 평균으로 간다. 참고로 $\lambda\downarrow0$의 극한은 비유일한 최소제곱해 중 최소 노름인 $(1/2,1/2)^\top$다.

## p8

### (a)

$p(\theta\mid D)=\mathcal N(\theta\mid1,2/3)$.

사후 precision은 prior $1/2$와 두 관측의 $x_n^2/2=1/2$를 더한 $3/2$이므로 분산은 $2/3$이다. 평균의 precision 가중 분자는 $m_0/v_0+\sum x_ny_n/2=1/2+(2+0)/2=3/2$여서 평균은 $1$이다. 직접 지수를 모으면 $p(\theta\mid D)\propto\exp[-\{(\theta-1)^2+(2-\theta)^2+(0-\theta)^2\}/4]$. 중괄호는 $3(\theta-1)^2+2$이므로 정규화 후 $\sqrt{3/(4\pi)}\exp[-3(\theta-1)^2/4]$가 된다.

### (b)

$f_*\mid D\sim\mathcal N(2,8/3)$, $y_*\mid D\sim\mathcal N(2,14/3)$.

$f_*=2\theta$이므로 사후 평균은 $2E[\theta\mid D]=2$이고 분산은 $2^2\operatorname{Var}(\theta\mid D)=4(2/3)=8/3$이다. 새 잡음은 평균 0, 분산 2이고 사후의 $\theta$와 독립이므로 $E[y_*\mid D]=2$, $\operatorname{Var}(y_*\mid D)=8/3+2=14/3$이다. 두 Gaussian의 합 역시 Gaussian이다. 두 분산 차이 2는 새 관측 잡음이며 $8/3$은 계수 불확실성이 함수값으로 전달된 부분이다.

### (c)

$\theta_{\rm MAP}=1$. 대입 예측은 $\mathcal N(2,2)$이며 사후예측 $\mathcal N(2,14/3)$와 다르다.

정규 사후분포는 평균에서 유일하게 최대이므로 MAP은 1이다. 이 값을 고정하면 $y_*=2+\epsilon_*$만 남아 분산은 2다. 사후예측은 $\int p(y_*\mid\theta)p(\theta\mid D)\,d\theta$로 모든 가능한 $\theta$의 불확실성을 적분하므로 분산이 $2+8/3$이다. 두 분포의 평균은 2로 같지만 분산 및 구간확률과 예측구간 폭이 다르므로 같은 예측분포라고 할 수 없다.

## p9

### (a)

$y\mid M_1\sim\mathcal N(0,2)$, $y\mid M_2\sim\mathcal N(0,5)$; $p(0\mid M_1)=1/\sqrt{4\pi}$, $p(0\mid M_2)=1/\sqrt{10\pi}$.

Evidence는 해당 데이터를 관측하기 전 모델이 부여하는 주변 예측밀도다. 미지 $\theta$를 데이터 관측 전 분포인 $p(\theta\mid M_j)$로 적분 제거하므로 prior를 쓴다. 같은 $y$를 반영한 posterior로 대신 평균내면 원래의 결합밀도 $p(y,\theta\mid M_j)=p(y\mid\theta,M_j)p(\theta\mid M_j)$를 주변화하는 계산이 아니다. 독립 Gaussian 합 $y=\theta+\epsilon$의 평균은 0, 분산은 prior 분산에 잡음 분산 1을 더한 값이므로 각각 2와 5다. Gaussian 정규화 계수를 $y=0$에서 평가하면 주어진 값이 나온다.

### (b)

$B_{12}=\sqrt{5/2}>1$이므로 데이터의 상대 evidence는 $M_1$을 지지한다.

$B_{12}=(1/\sqrt{4\pi})/(1/\sqrt{10\pi})=\sqrt{10/4}=\sqrt{5/2}\approx1.58114$. 따라서 0 부근의 이 관측은 $M_2$보다 $M_1$에서 더 높은 밀도를 받는다. Bayes factor는 모델 사전확률 비를 포함하지 않는 데이터의 상대 지지다.

### (c)

$\frac{P(M_1\mid0)}{P(M_2\mid0)}=\frac12\sqrt{5/2}=\sqrt{10}/4$; $P(M_1\mid0)=\frac{\sqrt5}{\sqrt5+2\sqrt2}\approx0.44152$. 선택은 $M_2$.

사후 odds는 Bayes factor와 사전 odds의 곱이다. 사전 odds는 $(1/3)/(2/3)=1/2$여서 사후 odds $r=\sqrt{5/2}/2\approx0.790569<1$. 따라서 $P(M_1\mid0)=r/(1+r)=\sqrt5/(\sqrt5+2\sqrt2)\approx0.441518$, $P(M_2\mid0)\approx0.558482$다. 사후확률로 고르면 $M_2$다. 데이터가 $M_1$에 주는 약 1.58배 지지가 사전의 $M_2$에 대한 2배 선호를 뒤집지 못해 (b)와 선택 기준 및 결과가 다르다.

## p10

### (a)

$\Phi^\top(y-\Phi\widehat\theta)=0$, 따라서 $\Phi^\top\Phi\widehat\theta=\Phi^\top y$.

열공간의 모든 벡터는 $\Phi a$ 꼴이다. 잔차 $r$가 이 공간에 직교하려면 모든 $a\in\mathbb R^2$에 대해 $(\Phi a)^\top r=a^\top\Phi^\top r=0$이어야 한다. 이는 $\Phi^\top r=0$과 동치다. $r=y-\Phi\widehat\theta$를 대입하고 정리하면 정규방정식이 나온다.

### (b)

$\widehat\theta=(4/3,1)^\top$, $\widehat y=(4/3,7/3,1/3)^\top$, $r=(2/3,-1/3,-1/3)^\top$이며 $\Phi^\top r=0$.

$\Phi^\top\Phi=\operatorname{diag}(3,2)$이고 $\Phi^\top y=(4,2)^\top$이므로 역행렬을 곱하면 위 $\widehat\theta$다. 이를 $\Phi$에 곱하면 $(4/3,4/3+1,4/3-1)^\top$가 되고 $y$에서 빼면 위 잔차다. 직접 확인하면 $\Phi^\top r=(2/3-1/3-1/3,(-1/3)-(-1/3))^\top=(0,0)^\top$이다.

### (c)

$P=\frac16\begin{pmatrix}2&2&2\\2&5&-1\\2&-1&5\end{pmatrix}\in\mathbb R^{3\times3}$, $P^\top=P$, $P^2=P$. $\widehat\theta\in\mathbb R^{2\times1}$.

열벡터 $c_1=(1,1,1)^\top$, $c_2=(0,1,-1)^\top$를 이용하면 $P=\frac13c_1c_1^\top+\frac12c_2c_2^\top$이므로 위 수치 행렬이다. $M=6P$라고 쓰면 $M^\top=M$이며 직접 곱해 $M^2=\begin{pmatrix}12&12&12\\12&30&-6\\12&-6&30\end{pmatrix}=6M$이다. 따라서 $P^\top=P$이고 $P^2=M^2/36=M/6=P$이다. $P$는 관측공간 $\mathbb R^3$에서 $y$를 $\widehat y$로 보내는 $3\times3$ 투영행렬이다. $\widehat\theta$는 두 계수를 가진 $2\times1$ 열벡터이며, $y$에서 계수로 보내는 행렬 $(\Phi^\top\Phi)^{-1}\Phi^\top$의 차원은 $2\times3$이다.

### (d)

$\|y-u\|^2=\|r\|^2+\|\widehat y-u\|^2$이며 $\widehat y$는 열공간에서 유일하게 가장 가까운 벡터다.

$u,\widehat y\in\operatorname{col}(\Phi)$이므로 $\widehat y-u$도 그 공간 안에 있다. 앞서 구한 $r$는 이 공간 전체에 직교하므로 $r^\top(\widehat y-u)=0$. $y-u=r+(\widehat y-u)$를 제곱하면 $\|y-u\|^2=\|r\|^2+2r^\top(\widehat y-u)+\|\widehat y-u\|^2$에서 중간 항이 사라진다. 따라서 거리는 최소한 $\|r\|^2=4/9+1/9+1/9=2/3$이고, 등호는 $u=\widehat y$일 때에만 성립한다. 이것이 직교투영의 유일한 최근접점 성질이다.

## 가정 및 표기 주의

- 문제의 모든 Gaussian 둘째 인수를 분산으로 사용했다. Gradient는 열벡터, Jacobian은 출력별 행을 사용하는 명시된 관례를 따랐다.
- p9의 p(y=0|M)는 연속형 관측의 밀도 평가값을 뜻한다. 정확히 한 점을 관측할 확률 P(y=0|M)는 두 모델 모두 0이다. 통상적인 evidence 표기로는 문제가 없으나 밀도와 확률은 구별해야 한다.
- p6에서 다항 특징으로 바꾸어도 계수에 대해 선형이라는 설명은 성립한다. 다항 특징행렬의 열독립과 역행렬 존재까지 기존 두 열의 독립에서 따라오지는 않는다.
- p5는 X가 세 점에 확률 1/3인 실제 분포이므로 분모 3 공분산이다. 제목의 표본 공분산만 보고 분모 N-1을 사용하지 않았다.
- 주어진 수치 및 가정에 내적 모순은 발견하지 않았다. 참조 답안과 비교하지 않았고 비교 통과 여부를 판정하지 않았다.
