"""Build the exam card HTML (ml-problem-explain 'exam' profile) from transcript.json + answer-checks.json.

Usage: python3 -I build_cards.py <transcript.json> <answer-checks.json> <out.html>
Korean conditions/ask and the reference solutions are authored here; the English statement and the scan crop
go into the 원문 (details.original). Reference solutions are the independently checked answers, never the student's.
"""
import json
import sys
from pathlib import Path

def amp(s):
    return s.replace('&', '&amp;')

# Per question: Korean title, conditions, ask (a)/(b), hint label/body, solution steps, answer.
KO = {
1: dict(title='기울기와 야코비안', cond=r'모든 벡터와 gradient는 열벡터이고, 야코비안은 $(\mathbf J_{\mathbf g})_{ij}=\partial g_i/\partial x_j$로 정의해요.',
        a=r'$f(u,v)=2u^2-2uv+4v^2+6u-2v$의 열 gradient $\nabla f(u,v)$를 구하고 $(u,v)=(-1,2)$에서 값을 구하세요.',
        b=r'$\mathbf g(u,v)=\begin{pmatrix}u^2+2v\\ uv-v^2\\ 3u-v\end{pmatrix}$의 야코비안 $\mathbf J_{\mathbf g}(u,v)$를 구하고 $(-1,2)$에서 값을 구하세요. 크기(차원)도 쓰세요.',
        label=r'편미분을 행=출력, 열=입력으로 배치', hint=r'gradient는 편미분을 세로로 쌓고, 야코비안은 $i$행에 $g_i$의 편미분을 가로로 놓아요.',
        steps=[r'(a) $\partial f/\partial u=4u-2v+6$, $\partial f/\partial v=-2u+8v-2$라서 $\nabla f=\begin{bmatrix}4u-2v+6\\-2u+8v-2\end{bmatrix}$예요. $(-1,2)$를 넣으면 $\begin{bmatrix}-4-4+6\\2+16-2\end{bmatrix}=\begin{bmatrix}-2\\16\end{bmatrix}$이에요.',
               r'(b) 출력 3개, 입력 2개라서 $\mathbf J_{\mathbf g}$는 $3\times2$예요. $\mathbf J_{\mathbf g}(u,v)=\begin{bmatrix}2u&2\\v&u-2v\\3&-1\end{bmatrix}$이고, $(-1,2)$를 넣으면 $\begin{bmatrix}-2&2\\2&-5\\3&-1\end{bmatrix}$예요.'],
        ans=r'(a) $\nabla f(-1,2)=(-2,16)^\top$, (b) $\mathbf J_{\mathbf g}(-1,2)=\begin{bmatrix}-2&2\\2&-5\\3&-1\end{bmatrix}$, 크기 $3\times2$'),
2: dict(title='행렬 연산과 직교 사영', cond=r'$A=\begin{pmatrix}1&1\\1&0\\0&1\end{pmatrix}$, $\mathbf y=\begin{pmatrix}3\\0\\0\end{pmatrix}$이에요.',
        a=r'$A^\top A$와 그 행렬식, 역행렬을 구하세요.',
        b=r'$\mathbf y$를 $A$의 열공간에 직교 사영한 $\mathbf p=A(A^\top A)^{-1}A^\top\mathbf y$와 $\mathbf r=\mathbf y-\mathbf p$를 구하고, $\mathbf r$이 $A$의 두 열과 직교함을 확인하세요.',
        label=r'사영 후 잔차는 열공간과 직교', hint=r'$A^\top\mathbf y$를 먼저 구하고 $(A^\top A)^{-1}$을 곱하면 계수가 나와요. 직교는 $A^\top\mathbf r=\mathbf 0$으로 확인해요.',
        steps=[r'(a) $A^\top A=\begin{bmatrix}2&1\\1&2\end{bmatrix}$, $\det=4-1=3$, $(A^\top A)^{-1}=\tfrac13\begin{bmatrix}2&-1\\-1&2\end{bmatrix}$이에요.',
               r'(b) $A^\top\mathbf y=(3,3)^\top$, 계수 $(A^\top A)^{-1}A^\top\mathbf y=(1,1)^\top$, $\mathbf p=A(1,1)^\top=(2,1,1)^\top$, $\mathbf r=(1,-1,-1)^\top$이에요. $A^\top\mathbf r=(1-1,\ 1-1)^\top=\mathbf 0$이라 두 열과 직교해요.'],
        ans=r'(a) $A^\top A=\begin{bmatrix}2&1\\1&2\end{bmatrix}$, $\det=3$, 역행렬 $\tfrac13\begin{bmatrix}2&-1\\-1&2\end{bmatrix}$, (b) $\mathbf p=(2,1,1)^\top$, $\mathbf r=(1,-1,-1)^\top$, $A^\top\mathbf r=\mathbf 0$'),
3: dict(title='가우시안 확률밀도', cond=r'$\mathcal N(\mu,v)$의 $v$는 분산이고, 다변량 정규분포의 둘째 인자는 공분산행렬이에요.',
        a=r'$\mathbf x=(x_1,x_2)^\top\sim\mathcal N\!\left(\begin{pmatrix}2\\-2\end{pmatrix},\begin{pmatrix}3&1\\1&1\end{pmatrix}\right)$의 결합밀도를 정규화 상수까지 명시해 쓰고, 이차식을 $(x_1-2)$와 $(x_2+2)$로 전개하세요.',
        b=r'$p(z)=c\exp\!\left[-\tfrac12(9z^2+18z+13)\right]$, $z\in\mathbb R$가 정규화된 밀도가 되도록 $c>0$을 정하고, 완전제곱을 보이며 평균과 분산을 밝히세요.',
        label=r'상수 $(2\pi)^{-D/2}|\Sigma|^{-1/2}$, 완전제곱', hint=r'2차원이면 정규화 상수는 $\frac{1}{2\pi\sqrt{|\Sigma|}}$예요. 1차원은 $a(z-m)^2$ 꼴로 바꾸면 분산이 $1/a$예요.',
        steps=[r'(a) $|\Sigma|=3-1=2$, $\Sigma^{-1}=\tfrac12\begin{bmatrix}1&-1\\-1&3\end{bmatrix}$이에요. $a=x_1-2$, $b=x_2+2$로 두면 이차식은 $\tfrac12(a^2-2ab+3b^2)$예요.',
               r'(a) 그래서 $p(\mathbf x)=\frac{1}{2\pi\sqrt2}\exp\!\left(-\tfrac14\left[(x_1-2)^2-2(x_1-2)(x_2+2)+3(x_2+2)^2\right]\right)$이에요.',
               r'(b) $9z^2+18z+13=9(z+1)^2+4$라서 $p(z)=ce^{-2}\exp\!\left(-\frac{(z+1)^2}{2\cdot\frac19}\right)$이에요. 적분은 $ce^{-2}\sqrt{2\pi/9}=1$이므로 $c=\frac{3e^2}{\sqrt{2\pi}}$이고, $p=\mathcal N(-1,\tfrac19)$라 평균 $-1$, 분산 $\tfrac19$예요.'],
        ans=r'(a) $p(\mathbf x)=\frac{1}{2\sqrt2\,\pi}\exp\!\left(-\tfrac14[(x_1-2)^2-2(x_1-2)(x_2+2)+3(x_2+2)^2]\right)$, (b) $c=3e^2/\sqrt{2\pi}$, 평균 $-1$, 분산 $1/9$'),
4: dict(title='결합확률과 조건부확률', cond=r'$U\in\{0,1\}$, $V\in\{0,1,2\}$의 결합 pmf는 $p(0,0)=\tfrac1{10},\ p(0,1)=\tfrac2{10},\ p(0,2)=\tfrac1{10},\ p(1,0)=\tfrac2{10},\ p(1,1)=\tfrac1{10},\ p(1,2)=\tfrac3{10}$이에요.',
        a=r'$U$와 $V$의 주변 pmf를 구하세요.',
        b=r'$P(U=1\mid V=2)$를 구하고, $U$와 $V$가 독립인지 수치로 판단하세요.',
        label=r'주변=행·열 합, 조건부=결합/주변', hint=r'독립이면 모든 칸에서 $P(U=u,V=v)=P(U=u)P(V=v)$여야 해요. 한 칸만 어긋나도 독립이 아니에요.',
        steps=[r'(a) 행 합: $P(U=0)=\tfrac4{10}$, $P(U=1)=\tfrac6{10}$. 열 합: $P(V=0)=\tfrac3{10}$, $P(V=1)=\tfrac3{10}$, $P(V=2)=\tfrac4{10}$이에요.',
               r'(b) $P(U=1\mid V=2)=\frac{3/10}{4/10}=\tfrac34$이에요. $P(U=1)=\tfrac35\ne\tfrac34$이고 $P(1,2)=\tfrac3{10}\ne\tfrac35\cdot\tfrac25=\tfrac6{25}$라 독립이 아니에요.'],
        ans=r'(a) $P_U=(\tfrac4{10},\tfrac6{10})$, $P_V=(\tfrac3{10},\tfrac3{10},\tfrac4{10})$, (b) $\tfrac34$, 독립 아님'),
5: dict(title='베이즈 추론과 예측', cond=r'패킷 성공확률 $\theta$의 사전분포는 $P(\theta=\tfrac13)=\tfrac23$, $P(\theta=\tfrac23)=\tfrac13$이에요. $\theta$가 주어지면 $X_1,X_2,\dots$는 독립 Bernoulli($\theta$)이고, 관측은 $\mathcal D=\{X_1=1,X_2=1\}$이에요.',
        a=r'주변우도 $P(\mathcal D)$와 두 $\theta$ 값의 사후확률을 구하세요.',
        b=r'$\hat\theta_{\mathrm{MAP}}$과 완전 베이즈 예측 $P(X_3=1\mid\mathcal D)$를 구하고, MAP plug-in 예측과 비교해 왜 다른지 설명하세요.',
        label=r'예측은 사후확률로 가중 평균', hint=r'$P(X_3=1\mid\mathcal D)=\sum_\theta\theta\,P(\theta\mid\mathcal D)$예요. 사전확률이 아니라 사후확률로 가중해요.',
        steps=[r'(a) $P(\mathcal D\mid\tfrac13)=\tfrac19$, $P(\mathcal D\mid\tfrac23)=\tfrac49$이라 $P(\mathcal D)=\tfrac19\cdot\tfrac23+\tfrac49\cdot\tfrac13=\tfrac29$예요. 사후확률은 $\frac{2/27}{2/9}=\tfrac13$, $\frac{4/27}{2/9}=\tfrac23$이에요.',
               r'(b) 사후확률이 큰 $\hat\theta_{\mathrm{MAP}}=\tfrac23$이에요. $P(X_3=1\mid\mathcal D)=\tfrac13\cdot\tfrac13+\tfrac23\cdot\tfrac23=\tfrac59$이고 MAP plug-in은 $\tfrac23$이에요. 베이즈 예측은 $\theta=\tfrac13$일 가능성(사후 $\tfrac13$)도 평균에 넣어서 더 작아요.'],
        ans=r'(a) $P(\mathcal D)=\tfrac29$, 사후 $(\tfrac13,\tfrac23)$, (b) $\hat\theta_{\mathrm{MAP}}=\tfrac23$, $P(X_3=1\mid\mathcal D)=\tfrac59<\tfrac23$'),
6: dict(title='최대우도와 MAP 선형회귀', cond=r'$y_n=\theta_0+\theta_1x_n+\varepsilon_n$, $\varepsilon_n\overset{\text{iid}}{\sim}\mathcal N(0,1)$, $\boldsymbol\theta=(\theta_0,\theta_1)^\top$이고 관측은 $(-1,0),(0,1),(1,3)$이에요.',
        a=r'우도를 정규화 상수까지 $\boldsymbol\theta$의 함수로 쓰고, 최대화 조건식을 유도해 $\hat{\boldsymbol\theta}_{\mathrm{ML}}$을 구하세요.',
        b=r'사전분포 $\boldsymbol\theta\sim\mathcal N(\mathbf 0,I_2)$(관측 잡음과 독립, 절편·기울기 모두 적용)를 쓸 때 음의 로그사후를 상수 차이까지 쓰고, 미분해 $\hat{\boldsymbol\theta}_{\mathrm{MAP}}$을 구하세요.',
        label=r'정규방정식, MAP은 $+I$', hint=r'$\Phi$의 행은 $(1,x_n)$이에요. 기울기를 0으로 놓으면 ML은 $\Phi^\top\Phi\boldsymbol\theta=\Phi^\top\mathbf y$, MAP은 $(\Phi^\top\Phi+I)\boldsymbol\theta=\Phi^\top\mathbf y$예요.',
        steps=[r'(a) $\Phi=\begin{bmatrix}1&-1\\1&0\\1&1\end{bmatrix}$, $p(\mathbf y\mid\boldsymbol\theta)=(2\pi)^{-3/2}\exp(-\tfrac12\|\mathbf y-\Phi\boldsymbol\theta\|^2)$예요. 음의 로그우도의 gradient $\Phi^\top(\Phi\boldsymbol\theta-\mathbf y)=\mathbf 0$에서 $\Phi^\top\Phi\boldsymbol\theta=\Phi^\top\mathbf y$예요.',
               r'(a) $\Phi^\top\Phi=\begin{bmatrix}3&0\\0&2\end{bmatrix}$, $\Phi^\top\mathbf y=(4,3)^\top$이라 $\hat{\boldsymbol\theta}_{\mathrm{ML}}=(\tfrac43,\tfrac32)^\top$이에요.',
               r'(b) $-\log p(\boldsymbol\theta\mid\mathcal D)=\tfrac12\|\mathbf y-\Phi\boldsymbol\theta\|^2+\tfrac12\|\boldsymbol\theta\|^2+\text{const}$예요. gradient를 0으로 놓으면 $(\Phi^\top\Phi+I)\boldsymbol\theta=\Phi^\top\mathbf y$, 즉 $\begin{bmatrix}4&0\\0&3\end{bmatrix}\boldsymbol\theta=(4,3)^\top$이라 $\hat{\boldsymbol\theta}_{\mathrm{MAP}}=(1,1)^\top$이에요.'],
        ans=r'(a) $\hat{\boldsymbol\theta}_{\mathrm{ML}}=(\tfrac43,\tfrac32)^\top$, (b) $\hat{\boldsymbol\theta}_{\mathrm{MAP}}=(1,1)^\top$'),
7: dict(title='공분산과 교차공분산 행렬', cond=r'$E[x_1]=2,\ E[x_2]=-1,\ \mathrm{Var}(x_1)=3,\ \mathrm{Var}(x_2)=2,\ E[x_1x_2]=-1$이에요. $\varepsilon$은 $\mathbf x$와 독립이고 평균 0, 분산 2예요. $\mathbf y=\begin{pmatrix}x_1+x_2+1+\varepsilon\\2x_1-x_2-2+2\varepsilon\end{pmatrix}$이고, 두 좌표에 같은 $\varepsilon$이 들어가요.',
        a=r'$\boldsymbol\mu_x=E[\mathbf x]$, $\Sigma_x=\mathrm{Cov}(\mathbf x)$, $\boldsymbol\mu_y=E[\mathbf y]$를 구하세요.',
        b=r'$\Sigma_y=\mathrm{Cov}(\mathbf y)$와 교차공분산 $C_{xy}=E[(\mathbf x-\boldsymbol\mu_x)(\mathbf y-\boldsymbol\mu_y)^\top]$를 구하고, 공유 잡음이 $\Sigma_y$에 어떻게 기여하는지 보이세요.',
        label=r'$\mathbf y=A\mathbf x+\mathbf b+\mathbf w\varepsilon$', hint=r'$\mathbf w=(1,2)^\top$로 두면 $\Sigma_y=A\Sigma_xA^\top+\mathrm{Var}(\varepsilon)\mathbf w\mathbf w^\top$, $C_{xy}=\Sigma_xA^\top$예요.',
        steps=[r'(a) $\boldsymbol\mu_x=(2,-1)^\top$, $\mathrm{Cov}(x_1,x_2)=E[x_1x_2]-E[x_1]E[x_2]=-1+2=1$이라 $\Sigma_x=\begin{bmatrix}3&1\\1&2\end{bmatrix}$이에요. $A=\begin{bmatrix}1&1\\2&-1\end{bmatrix}$, $\mathbf b=(1,-2)^\top$이면 $\boldsymbol\mu_y=A\boldsymbol\mu_x+\mathbf b=(1,5)^\top+(1,-2)^\top=(2,3)^\top$예요.',
               r'(b) $A\Sigma_xA^\top=\begin{bmatrix}7&5\\5&10\end{bmatrix}$, 공유 잡음 항은 $2\mathbf w\mathbf w^\top=\begin{bmatrix}2&4\\4&8\end{bmatrix}$이라 $\Sigma_y=\begin{bmatrix}9&9\\9&18\end{bmatrix}$이에요. 같은 $\varepsilon$ 때문에 비대각에 $+4$가 생겨요.',
               r'(b) $C_{xy}=E[(\mathbf x-\boldsymbol\mu_x)(A(\mathbf x-\boldsymbol\mu_x)+\mathbf w\varepsilon)^\top]=\Sigma_xA^\top=\begin{bmatrix}4&5\\3&0\end{bmatrix}$이에요($\varepsilon$은 $\mathbf x$와 독립이라 기여 0).'],
        ans=r'(a) $\boldsymbol\mu_x=(2,-1)^\top$, $\Sigma_x=\begin{bmatrix}3&1\\1&2\end{bmatrix}$, $\boldsymbol\mu_y=(2,3)^\top$, (b) $\Sigma_y=\begin{bmatrix}9&9\\9&18\end{bmatrix}$, $C_{xy}=\begin{bmatrix}4&5\\3&0\end{bmatrix}$'),
8: dict(title='가우시안 밀도의 곱', cond=r'$g(z)=\mathcal N(z\mid0,1)\,\mathcal N(z\mid2,1)$, $Z=\int_{-\infty}^{\infty}g(z)\,dz$, $q(z)=g(z)/Z$예요.',
        a=r'$g(z)$의 지수에서 완전제곱을 하고, 정규화한 $q(z)$의 평균과 분산을 구하세요.',
        b=r'$Z$를 계산하세요. $g(z)$ 자체가 정규화된 확률밀도인지 근거와 함께 답하세요.',
        label=r'지수 합치기 → 완전제곱 → 남는 상수', hint=r'$z^2+(z-2)^2=2(z-1)^2+2$예요. 남는 $e^{-1}$이 $Z$에 들어가요.',
        steps=[r'(a) $g(z)=\frac1{2\pi}\exp\!\left(-\tfrac12[z^2+(z-2)^2]\right)=\frac{e^{-1}}{2\pi}\exp\!\left(-\frac{(z-1)^2}{2\cdot\frac12}\right)$이라 $q(z)=\mathcal N(z\mid1,\tfrac12)$, 평균 1, 분산 $\tfrac12$예요.',
               r'(b) $Z=\frac{e^{-1}}{2\pi}\sqrt{2\pi\cdot\tfrac12}=\frac{e^{-1}}{2\sqrt\pi}=\frac{e^{-1}}{\sqrt{4\pi}}\approx0.104\ne1$이라 $g$는 정규화된 밀도가 아니에요.'],
        ans=r'(a) $q=\mathcal N(1,\tfrac12)$, (b) $Z=e^{-1}/\sqrt{4\pi}\ne1$, 정규화 안 됨'),
9: dict(title='베이즈 선형회귀: 파라미터 사후분포', cond=r'$\mathbf y=\Phi\boldsymbol\theta+\boldsymbol\varepsilon$, $\boldsymbol\theta\sim\mathcal N(\mathbf m_0,S_0)$, $\boldsymbol\varepsilon\sim\mathcal N(\mathbf 0,\sigma^2I_N)$이고 사후는 $\mathcal N(\mathbf m_N,S_N)$, $S_N=(S_0^{-1}+\sigma^{-2}\Phi^\top\Phi)^{-1}$, $\mathbf m_N=S_N(S_0^{-1}\mathbf m_0+\sigma^{-2}\Phi^\top\mathbf y)$예요(증명 없이 사용 가능). $\phi(x)=(1,x)^\top$, 관측 $(-1,1),(1,3)$, $\mathbf m_0=\mathbf 0$, $S_0=I_2$, $\sigma^2=1$이에요.',
        a=r'설계행렬 $\Phi$와 관측벡터 $\mathbf y$를 만들고 $\Phi^\top\Phi$와 사후 공분산 $S_N$을 구하세요.',
        b=r'$\Phi^\top\mathbf y$와 사후 평균 $\mathbf m_N$을 구하고, 수치 평균·공분산으로 사후분포 $p(\boldsymbol\theta\mid\mathcal D)$를 쓰세요.',
        label=r'$S_N$은 정밀도 합의 역행렬', hint=r'$S_0^{-1}+\sigma^{-2}\Phi^\top\Phi$는 정밀도(precision)예요. 공분산은 그 역행렬이라 데이터가 늘면 작아져요.',
        steps=[r'(a) $\Phi=\begin{bmatrix}1&-1\\1&1\end{bmatrix}$, $\mathbf y=(1,3)^\top$, $\Phi^\top\Phi=2I$예요. 정밀도 $I+2I=3I$의 역행렬이라 $S_N=\tfrac13I$예요.',
               r'(b) $\Phi^\top\mathbf y=(4,2)^\top$, $\mathbf m_N=\tfrac13I\,(4,2)^\top=(\tfrac43,\tfrac23)^\top$이라 $p(\boldsymbol\theta\mid\mathcal D)=\mathcal N\!\left(\boldsymbol\theta\,\middle|\,(\tfrac43,\tfrac23)^\top,\tfrac13I\right)$이에요.'],
        ans=r'(a) $\Phi^\top\Phi=2I$, $S_N=\tfrac13I$, (b) $\Phi^\top\mathbf y=(4,2)^\top$, $\mathbf m_N=(\tfrac43,\tfrac23)^\top$, $\mathcal N(\mathbf m_N,\tfrac13I)$'),
10: dict(title='베이즈 선형회귀: 예측분포', cond=r'9(b)의 모델과 사후분포를 이어서 써요. 새 입력 $x_*=2$에서 $f_*=\phi(x_*)^\top\boldsymbol\theta=\theta_0+2\theta_1$, $y_*=f_*+\varepsilon_*$, $\varepsilon_*\sim\mathcal N(0,1)$이고, $\varepsilon_*$는 $\boldsymbol\theta$와 학습 잡음 모두와 독립이에요.',
        a=r'$p(f_*\mid x_*,\mathcal D)$를 평균·분산까지 구하고, 왜 가우시안인지 설명하며 밀도를 명시하세요.',
        b=r'$p(y_*\mid x_*,\mathcal D)$를 $\boldsymbol\theta$에 대한 적분으로 쓰고 결과 가우시안을 구하세요. 분산이 (a)와 왜 다른지 설명하세요.',
        label=r'새 특징벡터 $\phi(x_*)$로 평균·분산 전파', hint=r'$f_*$는 가우시안 $\boldsymbol\theta$의 선형결합이라 가우시안이에요. 새 입력의 특징벡터 $\phi(x_*)=(1,2)^\top$를 써요.',
        steps=[r'(a) $\phi_*=(1,2)^\top$이라 평균 $\phi_*^\top\mathbf m_N=\tfrac43+\tfrac43=\tfrac83$, 분산 $\phi_*^\top S_N\phi_*=\tfrac13(1+4)=\tfrac53$이에요. $p(f_*\mid x_*,\mathcal D)=\frac{1}{\sqrt{2\pi\cdot5/3}}\exp\!\left(-\frac{(f_*-8/3)^2}{2\cdot5/3}\right)$예요.',
               r'(b) $p(y_*\mid x_*,\mathcal D)=\int\mathcal N(y_*\mid\phi_*^\top\boldsymbol\theta,1)\,\mathcal N(\boldsymbol\theta\mid\mathbf m_N,S_N)\,d\boldsymbol\theta=\mathcal N(y_*\mid\tfrac83,\tfrac53+1)=\mathcal N(\tfrac83,\tfrac83)$이에요. 관측 잡음 $\varepsilon_*$의 분산 1이 더해져서 (a)보다 커요.'],
        ans=r'(a) $f_*\mid\mathcal D\sim\mathcal N(\tfrac83,\tfrac53)$, (b) $y_*\mid\mathcal D\sim\mathcal N(\tfrac83,\tfrac83)$'),
}

HEAD = '''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>머신러닝기초 중간고사 1021</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false})"></script>
  <style>body{max-width:860px;margin:2rem auto;padding:0 16px;font-family:system-ui,sans-serif;line-height:1.6}article{border-top:1px solid #ccc;padding:1rem 0}img{max-width:100%}</style>
</head>
<body>
<main>
<h1>머신러닝기초 중간고사 1021 — Midterm Examination (Fall 2026)</h1>
<section id="exam">
'''

def card(q, k, checks):
    n = q['n']
    a, b = q['parts']
    for lab in ('a', 'b'):
        assert checks[f'p{n}:{lab}']['status'] == 'pass', (n, lab)
    original = (f'"{amp(q["context_tex"])} <div class="part">(a) {amp(a["statement_tex"])}</div>'
                f'<div class="part">(b) {amp(b["statement_tex"])}</div>"'
                f'<p><img src=".pack/scan/q{n}.webp" alt="Q{n} 시험지 스캔" loading="lazy"></p>')
    steps = ''.join(f'\n    <li>{amp(s)}</li>' for s in k['steps'])
    return f'''<article class="card" id="p{n}" data-source="Midterm 1021 Q{n}">
  <h3>Q{n}. {k["title"]}</h3>
  <div class="problem"><div class="conditions">{amp(k["cond"])}</div>
  <div class="ask">다음을 구해 보세요.<ol><li>(a) {amp(k["a"])}</li><li>(b) {amp(k["b"])}</li></ol></div></div>
  <details class="original"><summary>시험 원문 보기</summary>{original}</details>
  <details class="hint" data-label="{amp(k["label"])}"><summary>힌트 보기</summary>{amp(k["hint"])}</details>
  <details class="solution"><summary>풀이 보기</summary><ol class="steps">{steps}
  </ol><p class="answer">정답: {amp(k["ans"])}</p></details>
</article>
'''

def main(transcript, checks, out):
    t = json.loads(Path(transcript).read_text(encoding='utf-8'))
    c = json.loads(Path(checks).read_text(encoding='utf-8'))['items']
    body = ''.join(card(q, KO[q['n']], c) for q in t['questions'])
    Path(out).write_text(HEAD + body + '</section>\n</main>\n</body>\n</html>\n', encoding='utf-8')
    print(f'wrote {out}: {len(t["questions"])} cards')

if __name__ == '__main__':
    main(*sys.argv[1:4])
