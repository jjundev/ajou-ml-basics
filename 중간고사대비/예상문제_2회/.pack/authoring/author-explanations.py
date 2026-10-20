from author import *
import html
E=[]
def e(understand,recall,start,solve,verify,pitfall,retry,summary,terms):
 E.append(dict(understand=understand,recall=recall,start=start,solve=solve,verify=verify,pitfall=pitfall,retry=retry,summary=summary,terms=terms))
e(r'먼저 두 벡터만 보고, 마지막에 세 번째 벡터를 추가해요. (a)는 영벡터를 만드는 방법, (b)는 목표벡터를 만드는 방법, (c)는 중복 방향이 생기는지를 물어요.',
 r'“선형독립(linear independence)”은 영벡터를 만드는 계수가 모두 0이어야 한다는 뜻이에요. $av_1+bv_2=0$에서 $a,b$는 실수 계수예요. 각 성분을 비교하면 이 조건을 직접 검사할 수 있어요. 독립인 두 벡터로 같은 목표를 두 방법으로 나타냈다면 두 표현을 빼서 계수 차이가 모두 0임을 보일 수 있어요. 세 벡터의 종속은 계수가 모두 0은 아닌 관계 하나로 충분해요.',
 r'$$av_1+bv_2=(a,2b)^\top.$$ 영벡터와 비교할 때와 목표 $(3,4)^\top$와 비교할 때를 나누어요.',
 [r'$av_1+bv_2=0$은 $a=0$, $2b=0$이므로 $a=b=0$이에요. 따라서 $v_1,v_2$는 선형독립이에요.',r'$a=3$, $2b=4$에서 $b=2$예요. 따라서 $c=3v_1+2v_2$예요. 다른 계수 $a\prime,b\prime$도 같은 $c$를 만들면 $(a-a\prime)v_1+(b-b\prime)v_2=0$이에요. (a)의 독립성 때문에 두 계수 차이가 0이므로 유일해요.',r'$v_3=v_1+v_2$이므로 $v_1+v_2-v_3=0$이에요. 계수 $(1,1,-1)$는 모두 0이 아니므로 세 벡터는 선형종속이에요.'],
 [r'$(a,2b)=(0,0)$의 두 성분을 따로 풀면 영해만 나와요. 두 벡터의 방향이 겹치지 않는다는 판정과 같아요.',r'$3(1,0)^\top+2(0,2)^\top=(3,4)^\top$예요. 차이식에서 계수 차이가 0이라는 논증이 있으므로 단순히 한 표현을 찾은 데서 끝나지 않았어요.',r'$(1,0)^\top+(0,2)^\top-(1,2)^\top=(0,0)^\top$예요. 0이 아닌 관계를 실제로 확인했어요.'],
 r'두 벡터의 독립성을 확인한 결과를 세 벡터에 그대로 옮기지 않아요. 독립성은 어떤 벡터들의 집합을 검사하는지에 따라 달라져요.',
 ['두 성분의 방정식으로 독립성을 판정해요.','목표를 만든 뒤 계수의 유일성을 차이식으로 설명해요.'],
 r'두 벡터는 독립. $c=3v_1+2v_2$로 유일. 세 벡터는 $v_1+v_2-v_3=0$으로 종속.',
 [('선형결합 (linear combination)',r'벡터에 실수 계수를 곱해 더한 표현이에요. $av_1+bv_2$에서 계수는 스칼라이고 결과는 $2\times1$ 열벡터예요. 이 문제에서는 목표 $c$를 만드는 데 써요.'),('선형독립 (linear independence)',r'영벡터를 만드는 계수가 영계수뿐이라는 성질이에요. $av_1+bv_2=0$이 검사식이에요. 이 문제에서는 표현의 유일성을 보장해요.')])
e(r'입력 $x$는 열벡터지만 스칼라 출력 $f$의 미분은 행벡터예요. 벡터 출력 $g$의 미분은 출력마다 한 행을 갖는 행렬이에요. 최소점에서는 두 제곱항이 함께 0이 될 수 있는지 확인해요.',
 r'“행 미분(row derivative)”은 편미분을 가로로 모으라는 단서예요. $\nabla_xf=(\partial f/\partial u,\partial f/\partial v)$는 $1\times2$예요. Jacobian은 $J_{ij}=\partial g_i/\partial x_j$여서 출력 $g_1,g_2$가 행, 입력 $u,v$가 열이에요. 제곱항은 0 이상이므로 두 항을 동시에 0으로 만드는 점이 있으면 전역 최소를 바로 판단할 수 있어요.',
 r'$$\frac{\partial f}{\partial u}=2(u-1),\qquad \frac{\partial f}{\partial v}=4(v+1).$$ 한 변수로 미분할 때 나머지는 상수예요.',
 [r'$$\nabla_xf=\begin{pmatrix}2(u-1)&4(v+1)\end{pmatrix}\in\mathbb R^{1\times2}.$$ $(0,0)$에서는 $\begin{pmatrix}-2&4\end{pmatrix}$예요.',r'$g_1=u+v$의 두 미분을 첫 행에, $g_2=u-2v$의 두 미분을 둘째 행에 놓아요. $$J_g=\begin{pmatrix}1&1\\1&-2\end{pmatrix}\in\mathbb R^{2\times2}.$$ 선형함수라 입력값에 의존하지 않아요.',r'$f=(u-1)^2+2(v+1)^2\ge0$예요. $u=1$, $v=-1$일 때 두 항이 모두 0이므로 $x_*=(1,-1)^\top$, 최솟값은 0이에요. 0이 되려면 두 제곱이 각각 0이어야 하므로 이 전역 최소점은 유일해요.'],
 [r'성분별 편미분이 $-2,4$이고 결과를 가로로 모았으므로 차원은 $1\times2$예요. 입력의 열 방향과 구별해요.',r'$J_gx=(u+v,u-2v)^\top=g(x)$예요. $2\times2$ Jacobian과 $2\times1$ 입력의 곱이 원래 $2\times1$ 출력을 만들므로 출력 행·입력 열의 순서가 맞아요.',r'$f(1,-1)=0$이고 모든 $x$에서 $f(x)\ge0$예요. 정지점 확인에만 머물지 않고 전역성·유일성까지 확인했어요.'],
 r'gradient를 $(2(u-1),4(v+1))^\top$로 적으면 이 새 문제의 행 관례와 달라져요. Jacobian은 $2\times2$여도 성분의 행·열 위치를 바꾸면 다른 함수의 미분이 돼요.',
 ['스칼라 미분과 Jacobian의 차원을 먼저 적어요.','제곱항으로 최소점의 전역성과 유일성을 설명해요.'],
 r'$\nabla_xf=(2(u-1),4(v+1))$, $J_g=\begin{pmatrix}1&1\\1&-2\end{pmatrix}$. 최소점 $(1,-1)^\top$, 최솟값 0.',
 [('행 미분 (row derivative)',r'스칼라 함수를 열 입력으로 미분한 $1\times2$ 행벡터예요. 이 문제에서는 $f$의 편미분 두 개를 가로로 모아요.'),('Jacobian',r'벡터 출력의 모든 1차 편미분이에요. $J_{ij}=\partial g_i/\partial x_j$로 정의해요. 이 문제에서는 두 출력과 두 입력이 있어 $2\times2$예요.')])
e(r'두 밀도를 곱한 함수와 그것을 적분 1로 맞춘 밀도를 구별해요. (a)의 완전제곱으로 (b)의 평균·분산을 읽고, (c)에서는 처음 밀도의 앞 계수를 되살려 적분해요.',
 r'“Gaussian 곱”에서는 지수의 이차식을 완전제곱(completing the square)해요. $\mathcal N(z\mid m,v)=\exp[-(z-m)^2/(2v)]/\sqrt{2\pi v}$에서 $m$은 평균, $v>0$는 분산이에요. 지수의 제곱 중심이 평균이고 바깥 계수를 $1/(2v)$와 비교해 분산을 읽어요. 정규화(normalization)는 적분이 1이 되게 나누는 작업이므로 $Z$를 구할 때 상수항도 보존해야 해요.',
 r'$$p_0(z)p_1(z)=\frac1{4\pi}\exp\left[-\frac{z^2+(z-2)^2}{4}\right].$$ 각 분산이 2라서 지수의 분모는 4예요.',
 [r'$$z^2+(z-2)^2=2z^2-4z+4=2(z-1)^2+2.$$ 따라서 곱의 지수는 $-(z-1)^2/2-1/2$예요.',r'$z$에 따른 모양은 $\exp[-(z-1)^2/2]$예요. $1/(2v)=1/2$에서 $v=1$, 중심은 1이에요. $$q(z)=\frac1{\sqrt{2\pi}}\exp\left[-\frac{(z-1)^2}{2}\right]=\mathcal N(z\mid1,1).$$',r'$$p_0p_1=\frac{e^{-1/2}}{4\pi}\exp\left[-\frac{(z-1)^2}{2}\right].$$ 뒤 지수함수의 적분은 $\sqrt{2\pi}$이므로 $$Z=\frac{e^{-1/2}\sqrt{2\pi}}{4\pi}=\frac{e^{-1/2}}{\sqrt{8\pi}}.$$ $Z\ne1$이므로 원래 곱은 정규화된 확률밀도가 아니에요.'],
 [r'$z=0$에서 왼쪽은 4, 오른쪽도 $2+2=4$예요. 전개하면 두 다항식의 모든 계수가 같아요.',r'$q$의 앞 계수와 Gaussian 적분을 곱하면 1이에요. 정밀도도 $1/2+1/2=1$이므로 사후 곱의 분산 1과 일치해요.',r'$Zq(z)=e^{-1/2}\exp[-(z-1)^2/2]/(4\pi)$로 원래 곱과 같아요. $Z$는 약 $0.121$여서 1이 아니에요.'],
 r'정규화된 $q$에서는 없어지는 $e^{-1/2}$가 $Z$에서는 필요해요. 분산 2를 표준편차 2로 바꾸어 지수 분모를 8로 쓰지 않아요.',
 ['지수의 바깥 계수까지 포함해 평균·분산을 읽어요.','원래 곱의 상수와 적분값을 곱해 Z를 복원해요.'],
 r'$z^2+(z-2)^2=2(z-1)^2+2$. $q=\mathcal N(1,1)$, $Z=e^{-1/2}/\sqrt{8\pi}\ne1$.',
 [('정밀도 (precision)',r'분산의 역수 $1/v$예요. 같은 변수의 Gaussian을 곱할 때 정밀도가 더해져요. 이 문제에서는 $1/2+1/2=1$이에요.'),('정규화 상수 (normalizing constant)',r'함수의 전체 적분을 1로 만드는 데 필요한 상수예요. 이 문제의 $Z=\int p_0p_1$는 원래 곱을 나누는 값이에요.')])
e(r'스칼라 입력 세 개를 특징 열벡터로 바꾼 다음 각각 전치해 행으로 쌓아요. ML은 데이터만, MAP는 두 계수 모두에 주어진 prior까지 반영해요. 이 문항은 공식 적용형이므로 공식을 대입해 계산해요.',
 r'“$\phi(x)=(1,x)^\top$”는 첫 특징이 절편, 둘째 특징이 입력임을 뜻해요. $\phi$는 함수, $\phi(x_n)$는 $2\times1$ 특징벡터, $\Phi$는 $3\times2$ 설계행렬(design matrix)이에요. $\Phi_{n1}=1$, $\Phi_{n2}=x_n$이며 $n$은 관측 행 번호예요. 독립·동일분산 Gaussian 잡음에서 열독립이면 ML은 $(\Phi^\top\Phi)^{-1}\Phi^\top y$예요. 잡음분산과 prior 분산이 모두 1이므로 MAP는 $(\Phi^\top\Phi+I_2)^{-1}\Phi^\top y$예요. 절편에도 prior가 적용된다는 조건 때문에 두 대각성분 모두에 1을 더해요.',
 r'$$\phi(-1)=\begin{pmatrix}1\\-1\end{pmatrix},\quad \phi(0)=\begin{pmatrix}1\\0\end{pmatrix},\quad \phi(1)=\begin{pmatrix}1\\1\end{pmatrix}.$$ 이 전치들을 관측 순서대로 놓아요.',
 [r'$$\Phi=\begin{pmatrix}1&-1\\1&0\\1&1\end{pmatrix},\qquad y=\begin{pmatrix}1\\2\\3\end{pmatrix}.$$ 행은 관측, 열은 절편·입력 특징이에요.',r'열끼리 내적하면 $$\Phi^\top\Phi=\begin{pmatrix}3&0\\0&2\end{pmatrix},\quad \Phi^\top y=\begin{pmatrix}6\\2\end{pmatrix}.$$ 따라서 $$\hat\theta_{\rm ML}=\begin{pmatrix}1/3&0\\0&1/2\end{pmatrix}\begin{pmatrix}6\\2\end{pmatrix}=\begin{pmatrix}2\\1\end{pmatrix}.$$',r'$$\hat\theta_{\rm MAP}=(\Phi^\top\Phi+I_2)^{-1}\Phi^\top y=\begin{pmatrix}6/4\\2/3\end{pmatrix}=\begin{pmatrix}3/2\\2/3\end{pmatrix}.$$ $x_*=0$에서는 $\phi(0)=(1,0)^\top$이므로 평균 예측은 $\phi(0)^\top\hat\theta_{\rm MAP}=3/2$예요. prior가 절편과 기울기 모두를 0 쪽으로 당기므로 절편도 줄어요.'],
 [r'$\Phi\theta=(\theta_0-\theta_1,\theta_0,\theta_0+\theta_1)^\top$로 세 입력의 모델과 같아요.',r'$\Phi(2,1)^\top=(1,2,3)^\top=y$이므로 오차 0이에요. Gram 행렬식은 $3\cdot2=6>0$이라 ML이 유일해요.',r'$(\Phi^\top\Phi+I_2)(3/2,2/3)^\top=(6,2)^\top$예요. $x_*=0$의 특징은 기울기 항을 0으로 만들므로 예측값이 절편과 같아요.'],
 r'$\phi(x)$를 행으로 정의해 놓고 다시 전치하면 차원이 바뀌어요. 이 문제의 prior는 절편을 제외하지 않으므로 첫 대각항도 $3+1=4$예요.',
 ['특징벡터와 설계행렬의 차원을 말해요.','ML 공식과 MAP 공식에 각각 수치를 대입해요.'],
 r'$G=\operatorname{diag}(3,2)$, $\Phi^\top y=(6,2)^\top$. ML $(2,1)^\top$, MAP $(3/2,2/3)^\top$, $x_*=0$ 예측 $3/2$.',
 [('설계행렬 (design matrix)',r'$\Phi_{n,:}=\phi(x_n)^\top$인 관측×특징 행렬이에요. 이 문제에서는 $3\times2$이고 두 열은 절편·입력이에요.'),('MAP (maximum a posteriori)',r'posterior 밀도를 가장 크게 하는 모수예요. 이 문제에서는 prior가 두 계수에 제곱벌점을 주어 Gram에 $I_2$를 더해요.'),('ML (maximum likelihood)',r'주어진 모수에서 관측된 데이터의 밀도를 최대화해요. 이 문제의 동일 Gaussian 잡음에서는 최소제곱과 같아요.')])
e(r'네 점을 같은 확률로 고르는 이산분포예요. 평균에서 벗어난 네 벡터를 만든 뒤 외적을 평균내요. 변환에서는 배율과 이동의 역할을 구분해요.',
 r'“각각 확률 $1/4$”이므로 기대값(expectation)은 네 값의 평균이에요. 공분산(covariance)은 $\Sigma_X=E[(X-\mu_X)(X-\mu_X)^\top]$로 두 좌표의 함께 변하는 정도를 모은 $2\times2$ 행렬이에요. 아핀 변환 $Y=AX+b$에서는 $\mu_Y=A\mu_X+b$, $\Sigma_Y=A\Sigma_XA^\top$예요. 교차공분산은 첫 변수가 $X$일 때 $\operatorname{Cov}(X,Y)=\Sigma_XA^\top$예요. 중심화하면 상수 $b$가 사라져 이 공식들이 성립해요.',
 r'$$\mu_X=\frac14\left[\begin{pmatrix}0\\0\end{pmatrix}+\begin{pmatrix}2\\0\end{pmatrix}+\begin{pmatrix}0\\2\end{pmatrix}+\begin{pmatrix}2\\2\end{pmatrix}\right].$$',
 [r'각 좌표의 합이 4이므로 $\mu_X=(1,1)^\top$예요.',r'중심화 벡터는 $(-1,-1)^\top,(1,-1)^\top,(-1,1)^\top,(1,1)^\top$이에요. 각 좌표의 제곱은 모두 1이고 좌표곱의 합은 $1-1-1+1=0$이에요. 따라서 $$\Sigma_X=\begin{pmatrix}1&0\\0&1\end{pmatrix}.$$',r'공식에 대입하면 $$E[Y]=A\mu_X+b=\begin{pmatrix}3\\0\end{pmatrix},$$ $$\operatorname{Cov}(Y)=AI_2A^\top=\begin{pmatrix}4&0\\0&1\end{pmatrix},$$ $$\operatorname{Cov}(X,Y)=I_2A^\top=\begin{pmatrix}2&0\\0&1\end{pmatrix}.$$ $Y-E[Y]=A(X-\mu_X)$라 이동 $b$는 두 공분산에 들어가지 않아요.'],
 [r'각 좌표는 0과 2를 같은 확률로 가지므로 두 평균은 각각 1이에요.',r'외적 네 개를 합하면 $\operatorname{diag}(4,4)$이고 4로 나누면 $I_2$예요. 분모 3의 불편표본공분산을 계산한 것이 아니에요.',r'$Y$의 실제 네 값은 $(1,-1),(5,-1),(1,1),(5,1)$이에요. 평균 $(3,0)$에서의 차는 $(\pm2,\pm1)$이므로 분산 4,1과 교차항 0이 직접 확인돼요. $X$와 $Y$의 첫 좌표 중심곱은 항상 2, 둘째는 항상 1이에요.'],
 r'확률분포가 지정되어 있으므로 분모를 $N-1$로 바꾸지 않아요. $\operatorname{Cov}(X,Y)$와 $\operatorname{Cov}(Y,X)$는 일반적으로 전치 관계예요. 이 예에서 수치가 대각이라고 순서 규칙을 생략하지 않아요.',
 ['중심화한 네 벡터로 공분산을 다시 계산해요.','평균에는 b가 남고 공분산에는 사라지는 이유를 말해요.'],
 r'$\mu_X=(1,1)^\top$, $\Sigma_X=I_2$. $\mu_Y=(3,0)^\top$, $\Sigma_Y=\operatorname{diag}(4,1)$, $C_{XY}=\operatorname{diag}(2,1)$.',
 [('아핀 변환 (affine transformation)',r'선형변환 $AX$에 상수이동 $b$를 더한 변환이에요. 이 문제에서는 첫 좌표를 두 배 하고 $(1,-1)^\top$만큼 이동해요.'),('교차공분산 (cross-covariance)',r'$E[(X-\mu_X)(Y-\mu_Y)^\top]$예요. 행은 X좌표, 열은 Y좌표이고 이 문제에서는 $\Sigma_XA^\top$로 계산해요.')])
e(r'먼저 입력과 계수를 고정해서 출력의 무작위성이 어디서 오는지 봐요. 그런 다음 독립인 밀도의 곱, 음의 로그, 제곱오차 미분, 실제 수치 해 순서로 이어가요. 결과 미분은 $1\times2$ 행벡터예요.',
 r'“독립인 Gaussian 잡음”이 단서예요. $\theta$와 입력을 고정하면 $\phi(x_n)^\top\theta$는 상수라 출력의 평균만 이동해요. 조건부 독립(conditional independence)이 있으므로 likelihood를 두 밀도의 곱으로 써요. 로그는 곱을 합으로 바꾸고, 알려진 양의 분산에서는 음의 로그우도(NLL)의 최소점이 제곱오차와 같아요. $\Phi\in\mathbb R^{2\times2}$는 관측×특징, $y,\theta\in\mathbb R^{2\times1}$이에요. 정규방정식(normal equations)은 제곱오차의 행 미분을 0으로 둔 뒤 양변을 전치해서 얻어요.',
 r'$$y_n\mid x_n,\theta=\phi(x_n)^\top\theta+\epsilon_n.$$ 조건을 고정한 뒤 남는 무작위 변수는 $\epsilon_n$예요.',
 [r'잡음에 고정된 평균을 더하므로 $y_n\mid x_n,\theta\sim\mathcal N(\theta_0+\theta_1x_n,1)$이에요. 서로 다른 독립 잡음으로 만들어 조건부 출력들도 독립이에요. $$L(\theta)=\prod_{n=1}^2\frac1{\sqrt{2\pi}}e^{-(y_n-\phi(x_n)^\top\theta)^2/2}.$$ 따라서 $$L(\theta)=\frac1{2\pi}\exp\left[-\frac{(1-\theta_0+\theta_1)^2+(3-\theta_0-\theta_1)^2}{2}\right].$$',r'두 제곱의 합을 $Q$라 하면 $$-\log L=\log(2\pi)+\frac12Q.$$ 경험위험은 관측 두 개의 평균 제곱손실 $\widehat R=Q/2$예요. 따라서 NLL $=\log(2\pi)+\widehat R$이고, 더한 항은 $\theta$와 무관하므로 최소점이 같아요. 로그가 증가함수라 likelihood 최대화도 같은 점을 골라요.',r'$G=\Phi^\top\Phi$로 놓고 제곱을 펼쳐요. $$Q=y^\top y-2y^\top\Phi\theta+\theta^\top G\theta.$$ $G$는 대칭이므로 행 미분은 $$\nabla_\theta Q=-2y^\top\Phi+2\theta^\top G\in\mathbb R^{1\times2}.$$ 이를 $0_{1\times2}$로 놓으면 $\theta^\top G=y^\top\Phi$예요. <strong>양변을 전치</strong>하고 $G^\top=G$를 쓰면 $$G\theta=\Phi^\top y\in\mathbb R^{2\times1}.$$ 이것이 정규방정식이에요.',r'$$\Phi=\begin{pmatrix}1&-1\\1&1\end{pmatrix},\quad y=\begin{pmatrix}1\\3\end{pmatrix}.$$ 따라서 $G=2I_2$, $\Phi^\top y=(4,2)^\top$예요. $$\hat\theta_{\rm ML}=G^{-1}\Phi^\top y=\begin{pmatrix}2\\1\end{pmatrix},\quad \hat y=\Phi\hat\theta_{\rm ML}=\begin{pmatrix}1\\3\end{pmatrix}.$$ $G=2I_2$는 양의 정부호라 $Q$의 Hessian $2G=4I_2$도 양의 정부호이고 이 해가 유일한 전역 최소점이에요.'],
 [r'두 조건부 평균은 $\theta_0-\theta_1$, $\theta_0+\theta_1$예요. 이를 각 $\mathcal N(y_n\mid\mu_n,1)$에 넣으면 전개식과 같고 상수는 $(\sqrt{2\pi})^{-2}=1/(2\pi)$예요.',r'$Q$가 2만큼 증가하면 NLL은 1, $\widehat R$도 1만큼 증가해요. 고정된 상수를 더하는 연산만 남아 최소화 순서가 같아요.',r'성분으로 직접 미분하면 $\nabla_\theta Q=(4\theta_0-8,4\theta_1-4)$예요. $G=2I_2$, $y^\top\Phi=(4,2)$를 행 식에 넣은 것과 같아요. 곱 $\theta^\top G$와 $y^\top\Phi$는 모두 $1\times2$예요.',r'두 예측이 실제 y와 같아 $Q=0$이에요. $Q$는 항상 0 이상이고 $\det\Phi=2\ne0$이므로 같은 예측을 만드는 다른 계수도 없어요.'],
 r'독립성은 입력과 $\theta$를 조건으로 둔 상태의 말이에요. 행 미분을 열 정규방정식으로 곧바로 바꾸지 말고 양변 전치를 적어요. 밀도값을 구하는 (a)에서는 상수 $1/(2\pi)$도 필요해요.',
 ['잡음→조건부 밀도→곱 likelihood→NLL 순서로 써요.','행 미분을 0으로 놓고 양변을 전치해 수치 해를 얻어요.'],
 r'$L=(2\pi)^{-1}e^{-Q/2}$, NLL $=\log(2\pi)+Q/2$. $\nabla Q=-2y^\top\Phi+2\theta^\top G$. 전치→$G\theta=\Phi^\top y$. ML $(2,1)^\top$.',
 [('우도 (likelihood)',r'고정한 관측에서 모수를 바꿔 평가하는 밀도예요. 이 문제에서는 $L(\theta)=p(y\mid\Phi,\theta)$이고 두 관측의 곱으로 시작해요.'),('경험위험 (empirical risk)',r'관측별 손실의 평균이에요. 이 문제의 관측 수는 2이므로 제곱손실 위험은 $Q/2$예요.'),('정규방정식 (normal equations)',r'최소제곱 정지점이 만족하는 $\Phi^\top\Phi\theta=\Phi^\top y$예요. 이 문제에서는 행 미분식의 양변 전치를 통해 얻어요.')])
e(r'같은 평균을 갖는 두 관측으로 스칼라 계수 하나를 추정해요. prior를 곱해 만든 목적함수에서 데이터 항과 prior 항을 구분하고, 분산만 바꿔 벌점 세기를 비교해요.',
 r'“prior와 MAP”가 나오면 Bayes 법칙 $p(\theta\mid D)=p(D\mid\theta)p(\theta)/p(D)$를 떠올려요. $p(D)$는 모수를 적분한 evidence라 현재 비교하는 $\theta$와 무관해요. Gaussian의 음의 로그는 중심에서의 제곱거리/분산을 남겨요. 따라서 prior 분산이 작을수록 평균 0에서 멀어지는 벌점이 커져요. 여기서는 $\theta\in\mathbb R^{1\times1}$인 스칼라라 미분도 $1\times1$이에요. ridge는 데이터 제곱오차에 양의 계수로 $\theta^2$를 더한 형태예요.',
 r'$$p(D\mid\theta)=\mathcal N(1\mid\theta,1)\mathcal N(3\mid\theta,1).$$ 여기에 prior 밀도를 곱해요.',
 [r'Bayes 법칙에서 $p(D)=\int p(D\mid u)p(u)\,du$는 $\theta$와 무관해요. 그러므로 $$p(\theta\mid D)\propto \mathcal N(1\mid\theta,1)\mathcal N(3\mid\theta,1)\mathcal N(\theta\mid0,1).$$ 즉 $p(\theta\mid D)\propto\exp[-\{(1-\theta)^2+(3-\theta)^2+\theta^2\}/2]$예요.',r'상수항을 제외하면 $$J(\theta)=\frac12[(1-\theta)^2+(3-\theta)^2]+\frac12\theta^2.$$ 양수 2를 곱하면 데이터 제곱합 $Q$에 $\theta^2$가 더해져요. 따라서 $Q+\lambda\theta^2$로 쓴 ridge 계수는 $\lambda=1$이에요.',r'$$J\prime(\theta)=(\theta-1)+(\theta-3)+\theta=3\theta-4.$$ 0으로 놓으면 $\hat\theta_{\rm MAP}=4/3$이에요. prior를 제외하면 $Q/2$의 미분은 $2\theta-4$여서 $\hat\theta_{\rm ML}=2$예요. $J\prime\prime=3>0$이고 데이터 항도 곡률 2가 양수라 두 최소점은 각각 유일해요. MAP가 prior 평균 0에 더 가까워요.',r'prior 분산이 $1/4$이면 prior 벌점은 $\theta^2/(2\cdot1/4)=2\theta^2$예요. $$J_{1/4}\prime=(\theta-1)+(\theta-3)+4\theta=6\theta-4.$$ 따라서 MAP는 $2/3$이에요. $Q$ 기준 벌점계수는 $\lambda=4$로 커지고, $2>4/3>2/3>0$이므로 더 강하게 0 쪽으로 줄었어요.'],
 [r'세 Gaussian의 지수 분모가 모두 2이므로 세 제곱이 동일한 가중치로 더해져요. 분모 evidence를 생략했으므로 등식 대신 비례식이에요.',r'$2J=Q+\theta^2$라 제곱오차 항과 벌점항의 상대계수가 1이에요. 양의 배수는 최소점을 바꾸지 않아요.',r'$3(4/3)-4=0$, $2\cdot2-4=0$예요. 상수 곡률 3과 2는 양수라 정지점이 실제 최소점이에요.',r'$6(2/3)-4=0$이고 곡률 6은 양수예요. 분산의 역수 4가 미분의 prior 항에 들어간 것도 확인해요.'],
 r'prior 분산 $1/4$를 벌점계수 $1/4$로 쓰지 않아요. 여기서는 역수 4가 벌점 세기예요. likelihood를 모수의 정규화된 분포라고 부르지 않아요.',
 ['Bayes 식에서 evidence가 모수와 무관한 이유를 말해요.','prior 분산을 바꿔 목적함수부터 다시 미분해요.'],
 r'$J=Q/2+\theta^2/2$. ML $2$, MAP $4/3$. prior 분산 $1/4$→$J=Q/2+2\theta^2$→MAP $2/3$.',
 [('사전분포 (prior)',r'데이터를 보기 전 계수의 분포예요. 이 문제의 평균 0은 벌점의 중심, 분산은 그 벌점의 역세기를 정해요.'),('사후분포 (posterior)',r'likelihood와 prior를 곱해 데이터에 맞게 갱신한 계수 분포예요. 그 밀도의 최대점이 MAP예요.'),('ridge penalty',r'평균 0에서 벗어난 계수의 제곱에 벌점을 줘요. 이 문제에서 $Q+\lambda\theta^2$의 $\lambda$는 prior 분산 1이면 1, 1/4이면 4예요.')])
e(r'관측 하나로 스칼라 $\theta$의 분포를 갱신한 뒤, 그 분포 전체를 이용해 새 값을 예측해요. $f_*$에는 새 잡음이 없고 $y_*$에는 새 잡음이 있어요. 둘째 인수는 항상 분산이에요.',
 r'“잡음모델”에서 입력과 계수를 고정하면 출력 평균이 정해져 likelihood를 쓸 수 있어요. Gaussian prior와 likelihood의 곱은 완전제곱으로 Gaussian posterior가 돼요. “$f_*=2\theta$”에는 아핀 변환 공식 $E[aX]=aE[X]$, $\operatorname{Var}(aX)=a^2\operatorname{Var}(X)$를 적용해요. “독립인 새 잡음”이 더해지면 평균과 분산을 각각 더해요. 사용할 것은 prior 분산 1이 아니라 데이터를 반영한 posterior 분산이에요.',
 r'$$y\mid\theta\sim\mathcal N(\theta,1),\qquad p(y=2\mid\theta)=\frac1{\sqrt{2\pi}}e^{-(2-\theta)^2/2}.$$ 출력에 고정된 $\theta$를 더해 평균이 이동해요.',
 [r'$y=\theta+\epsilon$에서 $\theta$를 고정하면 $y$의 평균은 $\theta$, 분산은 1이에요. 관측값 2를 대입하면 $$p(y=2\mid\theta)=\mathcal N(2\mid\theta,1)=\frac1{\sqrt{2\pi}}e^{-(2-\theta)^2/2}.$$ 이는 점확률 $P(y=2\mid\theta)$가 아닌 밀도값이에요.',r'prior까지 곱하면 $$g(\theta)=\frac1{2\pi}e^{-\{(2-\theta)^2+\theta^2\}/2}.$$ 완전제곱은 $(2-\theta)^2+\theta^2=2(\theta-1)^2+2$예요. 따라서 모양은 $e^{-(\theta-1)^2}$이고 분산은 $1/2$예요. 적분 $\int e^{-(\theta-1)^2}d\theta=\sqrt\pi$로 정규화하면 $$p(\theta\mid y=2)=\frac1{\sqrt\pi}e^{-(\theta-1)^2},\qquad \theta\mid y=2\sim\mathcal N(1,1/2).$$',r'공식에 (b)의 값을 대입해요. $$E[f_*\mid y=2]=2\cdot1=2,$$ $$\operatorname{Var}(f_*\mid y=2)=2^2\cdot\frac12=2.$$ Gaussian의 선형변환도 Gaussian이므로 $f_*\mid y=2\sim\mathcal N(2,2)$예요.',r'새 잡음은 관측과 모수로부터 독립이라 조건을 둔 뒤에도 더할 수 있어요. $$E[y_*\mid y=2]=2+0=2,$$ $$\operatorname{Var}(y_*\mid y=2)=2+1=3.$$ 따라서 $y_*\mid y=2\sim\mathcal N(2,3)$예요. 분산 차이 1은 새로운 관측잡음의 불확실성이에요.'],
 [r'잔차 $2-\theta$를 평균 0·분산1 잡음 밀도에 넣으면 같은 식이에요. 계수 2가 아니라 관측값 2인 점도 확인해요.',r'정규화 계수 $1/\sqrt\pi$와 적분 $\sqrt\pi$의 곱은 1이에요. precision도 prior 1+관측 1=2여서 분산 $1/2$와 맞아요.',r'상수배는 분산에 제곱으로 들어가므로 $4\cdot1/2=2$예요. 분포의 평균 2와 분산 2는 서로 다른 역할이에요.',r'새 잡음 평균이 0이라 예측 평균은 그대로이고 분산만 1 증가해요. MAP $\theta=1$에 고정했다면 분산 1만 남지만 여기서는 모수 불확실성에서 전파된 분산 2도 포함해요.'],
 r'잠재값 $f_*$에 관측잡음 1을 미리 더하지 않아요. $\operatorname{Var}(2\theta)$를 $2\operatorname{Var}(\theta)$로 계산하지 말고 계수를 제곱해요. (c),(d)의 공식 적용을 위해 posterior를 다시 유도할 필요는 없어요.',
 ['likelihood의 관측값과 모수를 구분해 써요.','posterior로 잠재분산을 계산하고 마지막에 새 잡음을 더해요.'],
 r'$\theta\mid y=2\sim\mathcal N(1,1/2)$. $f_*\mid y=2\sim\mathcal N(2,2)$, $y_*\mid y=2\sim\mathcal N(2,3)$. 분산 차이는 새 잡음1.',
 [('사후예측 (posterior predictive)',r'사후 모수 불확실성을 반영한 새 출력 분포예요. 이 문제에서는 $2\theta$의 분산과 새 잡음분산을 함께 포함해요.'),('잠재값 (latent function value)',r'새 관측잡음을 더하기 전 함수값이에요. 이 문제의 $f_*=2\theta$는 posterior로부터 분산 2를 가져요.')])
e(r'이번에는 계수 하나의 최적값을 고르는 대신 두 모델을 비교해요. $M_0$에는 적분할 계수가 없고, $M_1$에는 prior 전체로 평균낼 계수가 있어요. 마지막에 모델 prior를 곱해 사후확률로 바꿔요.',
 r'“모델 비교”는 evidence(주변우도)를 떠올리는 단서예요. $p(y\mid M_1)=\int p(y\mid\theta,M_1)p(\theta\mid M_1)d\theta$는 prior로 likelihood를 평균낸 밀도예요. 독립 Gaussian의 합은 평균끼리·분산끼리 더하므로 어려운 적분 대신 주변분포를 찾을 수 있어요. Bayes factor $B_{01}$는 두 evidence의 비, posterior odds는 $B_{01}$에 prior odds $P(M_0)/P(M_1)$를 곱한 값이에요. 여기서는 두 모델의 prior가 같아요.',
 r'$$M_0:y=\epsilon,\qquad M_1:y=\theta+\epsilon.$$ 먼저 관측값 0을 대입하기 전 각각의 주변분포부터 적어요.',
 [r'$M_0$에서는 $y\sim\mathcal N(0,1)$이에요. $M_1$에서는 $$p(y\mid M_1)=\int\mathcal N(y\mid\theta,1)\mathcal N(\theta\mid0,3)d\theta.$$ 독립인 두 Gaussian의 합이라 평균은 $0+0=0$, 분산은 $3+1=4$예요. 따라서 $p(y\mid M_1)=\mathcal N(y\mid0,4)$예요. 이는 특정 $\theta$를 선택하는 대신 prior의 모든 값으로 평균낸 결과예요.',r'관측 $y=0$을 두 밀도에 대입해요. $$p(0\mid M_0)=\frac1{\sqrt{2\pi}},\qquad p(0\mid M_1)=\frac1{\sqrt{8\pi}}.$$ 평균에서 평가하므로 지수항은 둘 다 1이에요.',r'$$B_{01}=\frac{1/\sqrt{2\pi}}{1/\sqrt{8\pi}}=2.$$ 데이터가 $M_0$에 부여하는 밀도가 두 배라 $M_0$에 유리해요. evidence만의 비교와 모델 사후확률은 구분해요.',r'Bayes 식의 공통 분모 $p(y)$를 약분하면 $$\frac{P(M_0\mid y)}{P(M_1\mid y)}=\frac{P(M_0)}{P(M_1)}\frac{p(y\mid M_0)}{p(y\mid M_1)}.$$ prior odds가 1이므로 posterior odds는 $2:1$이에요. 두 사후확률의 합이 1이라 $P(M_0\mid0)=2/3$, $P(M_1\mid0)=1/3$이에요. 연속형 y는 점확률이 0이지만 밀도는 0이 아니에요. 여기서 관측 자료의 likelihood/evidence로 쓰는 것은 밀도값이므로 점확률로 바꾸어 $0/0$을 만들지 않아요.'],
 [r'$\operatorname{Var}(\theta+\epsilon)=3+1+2\operatorname{Cov}(\theta,\epsilon)=4$예요. 독립이라 공분산이 0인 조건을 사용했어요.',r'표준편차는 각각 1과 2라 평균 위치에서의 높이가 $1:1/2$예요. 두 밀도는 각각 전체 적분 1을 유지해요.',r'$p(0\mid M_0)=2p(0\mid M_1)$이므로 비의 방향 $01$과 값 2가 맞아요.',r'정규화 전 가중치는 $(1/2)/\sqrt{2\pi}$와 $(1/2)/\sqrt{8\pi}$예요. 합으로 나누면 $2/3,1/3$이고 두 값의 합이 1이에요.'],
 r'prior가 아닌 posterior로 evidence를 평균내면 관측을 반영하는 단계가 달라져요. $B_{01}=2$를 $P(M_0\mid y)=2$로 해석하지 않아요. odds를 확률로 바꾸는 정규화가 필요해요.',
 ['두 주변분포를 먼저 정하고 관측점에서 밀도를 계산해요.','Bayes factor의 방향과 모델 prior를 확인해 사후확률로 바꿔요.'],
 r'$M_0:y\sim\mathcal N(0,1)$, $M_1:y\sim\mathcal N(0,4)$. $B_{01}=2$, 같은 모델prior→posterior odds $2:1$, $P(M_0\mid0)=2/3$.',
 [('Evidence (marginal likelihood)',r'모델이 관측 데이터에 부여하는 밀도예요. $M_1$에서는 prior로 모수를 적분하고, $M_0$에서는 모수가 없어 잡음밀도를 그대로 써요.'),('Bayes factor',r'모델 evidence의 비예요. 이 문제는 방향을 $01$로 정했으므로 값 2는 $M_0$에 유리해요.'),('Posterior odds',r'두 모델 사후확률의 비예요. prior odds에 Bayes factor를 곱하며 이 문제에서는 $2:1$이에요.')])
e(r'3차원 벡터를 $b$ 방향의 직선 위로 내려놓아요. 계수 $\hat\theta$는 스칼라지만 투영 $\hat y$와 잔차 $r$은 원래와 같은 $3\times1$ 벡터예요. 직교조건을 세운 뒤 실제로 거리 최소까지 확인해요.',
 r'“잔차가 $b$에 수직”은 내적 $b^\top(y-b\theta)=0$을 쓰라는 단서예요. $b\ne0$이므로 $b^\top b>0$이고 계수는 $\hat\theta=(b^\top y)/(b^\top b)$예요. 이를 $b\hat\theta$에 대입하면 투영행렬(projection matrix) $P=bb^\top/(b^\top b)$가 나와요. 직교한 두 벡터의 제곱노름은 더해지므로 잔차와 직선방향의 차이를 나누면 전역 최소거리를 증명할 수 있어요. Gaussian 동일분산 잡음의 ML은 이 제곱거리를 최소화해요.',
 r'$$b^\top(y-b\theta)=b^\top y-(b^\top b)\theta=0.$$ 먼저 두 내적을 계산해요.',
 [r'$b^\top y=2$, $b^\top b=2$이므로 $2-2\theta=0$이에요. 따라서 $\hat\theta=1$이에요.',r'$$\hat y=b\hat\theta=\begin{pmatrix}1\\1\\0\end{pmatrix},\qquad r=y-\hat y=\begin{pmatrix}1\\-1\\1\end{pmatrix}.$$ $b^\top r=1-1+0=0$이라 직교해요.',r'$\hat y=b(b^\top y)/(b^\top b)$에서 $$P=\frac{bb^\top}{b^\top b}=\frac12\begin{pmatrix}1&1&0\\1&1&0\\0&0&0\end{pmatrix}\in\mathbb R^{3\times3}.$$ $bb^\top$가 대칭이므로 $P^\top=P$예요. 또한 $$P^2=\frac{b(b^\top b)b^\top}{(b^\top b)^2}=\frac{bb^\top}{b^\top b}=P.$$',r'임의의 $\theta$에 대해 $y-b\theta=r+b(\hat\theta-\theta)$예요. $r^\top b=0$이라 제곱노름을 펼친 교차항이 사라져요. 따라서 $$\|y-b\theta\|^2=\|r\|^2+(\theta-\hat\theta)^2\|b\|^2=3+2(\theta-1)^2.$$ 최소 제곱오차는 3이고 $\theta=1$에서만 달성돼요. 알려진 Gaussian 잡음분산 1에서 NLL은 $\frac32\log(2\pi)+\frac12\|y-b\theta\|^2$이므로 같은 해가 ML이에요.'],
 [r'$b^\top b=2>0$이므로 나눗셈이 가능하고 계수 해가 유일해요.',r'$\hat y+r=(2,0,1)^\top=y$예요. 잔차를 직선 방향과 내적하면 정확히 0이에요.',r'$Py=(1,1,0)^\top$로 (b)와 같아요. $Pb=b$이고 마지막 좌표를 0으로 보내 직선 위의 벡터를 보존해요. 대칭·멱등은 (c)의 행렬곱 계산으로 모든 입력에 대해 성립해요.',r'직접 성분 전개한 $(2-\theta)^2+\theta^2+1=2\theta^2-4\theta+5$도 $3+2(\theta-1)^2$와 같아요. 모든 실수 $\theta$에서 추가항이 0 이상이라 일부 수치 예만으로 최소라고 판단하지 않았어요.'],
 r'계수 $\hat\theta=1$을 투영벡터라고 부르지 않아요. $P$도 $3\times3$이에요. $P^\top=P^2=P$는 각 행렬이 같다는 뜻이고 모든 항등행렬이 된다는 뜻은 아니에요.',
 ['잔차 직교조건 하나로 계수와 투영을 구해요.','교차항 0에서 거리분해와 ML의 연결까지 설명해요.'],
 r'$\hat\theta=1$, $\hat y=(1,1,0)^\top$, $r=(1,-1,1)^\top$. $P=bb^\top/2$. 오차 $3+2(\theta-1)^2$→유일 ML, 최소3.',
 [('직교투영 (orthogonal projection)',r'부분공간 위에서 원래 벡터에 가장 가까운 벡터예요. 이 문제에서는 $y$를 $\operatorname{span}(b)$ 위의 $b\hat\theta$로 보내요.'),('멱등 (idempotent)',r'$P^2=P$라는 성질이에요. 한 번 투영한 결과를 다시 투영해도 같아요. 이 문제의 P는 대칭이기도 해서 직교투영행렬이에요.')])

def p(s):return '<p>'+s+'</p>'
def block(kind,body):
 titles={'understand':'문제를 내 말로 읽어요','recall':'이 문제를 봤을 때 떠올릴 개념과 공식','start':'종이에 쓰는 첫 줄','solve':'왜 이렇게 푸는지 함께 따라가요','verify':'완성 답과 검산','pitfall':'여기서 헷갈리기 쉬워요','retry':'설명을 닫고 다시 풀어요'}
 layer={'understand':'eli5','pitfall':'warn','retry':'eli5'}.get(kind,'formal')
 return f'<div class="layer {layer}" data-explanation="{kind}"><h4>{titles[kind]}</h4>{body}</div>'
for i,(x,z) in enumerate(zip(q,E),1):
 parts=list(string.ascii_lowercase[:len(x['ask'])]); assert len(z['solve'])==len(z['verify'])==len(parts)
 # Two long adjacent display formulas must remain separate readable paragraphs.
 def paragraphs(s):return p(s).replace('$$ $$','$$</p><p>$$')
 solve=''.join(f'<div data-subpart="{a}"><h4>({a})</h4>{paragraphs(s)}</div>' for a,s in zip(parts,z['solve']))
 verify=''.join(f'<div data-subpart="{a}"><h4>({a}) 검산</h4>{paragraphs(s)}</div>' for a,s in zip(parts,z['verify']))
 exp='\n'.join(block(k,solve if k=='solve' else verify if k=='verify' else '<ul>'+''.join('<li>'+t+'</li>' for t in z['retry'])+'</ul>' if k=='retry' else paragraphs(z[k])) for k in ('understand','recall','start','solve','verify','pitfall','retry'))
 exp+='<div class="sum" hidden><div class="summary-group"><h4>떠올릴 개념·공식</h4>'+paragraphs(z['summary'])+'</div><div class="summary-group"><h4>적용 조건</h4>'+p(x['assumptions'])+'</div></div>'
 provenance=f'{x["ref"]}의 개념을 실제 원자료와 대조한 새 변형이에요. MML PDF '+', '.join(map(str,x['pages']))+'쪽을 참고했어요. 원문제의 수치·차원·질문을 중하 난이도로 바꾸었고, 교수님의 실제 출제 확정 문항은 아니에요.'
 exp+='<section data-problem-panel="provenance"><h4>출제 근거</h4>'+p(provenance)+'</section>'
 exp+='<section data-problem-panel="terms"><h4>해설에 쓰인 용어</h4><dl class="terms">'+''.join('<dt>'+t+'</dt><dd>'+paragraphs(v)+'</dd>' for t,v in z['terms'])+'</dl></section>'
 path=OUT/f'.pack/explanations/p{i}.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(exp+'\n',encoding='utf-8')
 ask='<ol type="a">'+''.join('<li>'+a+'</li>' for a in x['ask'])+'</ol>'
 english='<div class="original" lang="en"><h4 data-english-title>'+x['en']+'</h4><div data-english-conditions>'+p(x['ec'])+'</div><div data-english-ask><ol type="a">'+''.join(f'<li data-english-part="{a}">{s}</li>' for a,s in zip(parts,x['ea']))+'</ol></div></div>'
 sol='<ol class="steps">'+''.join(f'<li><strong>({a})</strong>'+paragraphs(s)+'</li>' for a,s in zip(parts,z['solve']))+'</ol><div class="answer">'+paragraphs(z['summary'])+'</div>'
 card=f'<article class="card" id="p{i}" data-source="EXAM Problem {i}" data-origin-kind="{x["origin"]}" data-origin-ref="{html.escape(x["ref"],quote=True)}"><h3>{i}. {x["title"]}</h3><div class="problem"><div class="conditions">'+p(x['cond'])+'</div><div class="ask">'+ask+'</div></div>'+english+'<div class="hint"></div><div class="solution">'+sol+'</div></article>'
 path=OUT/f'.pack/cards/p{i}.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(card+'\n',encoding='utf-8')
dump(RUN/'authored-explanation-data.json',E)
print('authored 10 cards and 10 explanation fragments')
