from pathlib import Path
import json,hashlib,sys,string
R=Path.cwd(); RUN=R/'tmp/ml-midterm/round02-easier-20261020'; OUT=R/'중간고사대비/예상문제_2회'
def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def Q(title,en,cond,ec,ask,ea,origin,ref,assumptions,pages,hw=None):
 return dict(title=title,en=en,cond=cond,ec=ec,ask=ask,ea=ea,origin=origin,ref=ref,assumptions=assumptions,pages=pages,hw=hw)
q=[]
q.append(Q('두 벡터로 표현하기','Representing Vectors',
 r'열벡터 $v_1=(1,0)^\top$, $v_2=(0,2)^\top$, $v_3=(1,2)^\top$를 생각하자.',
 r'Consider the column vectors $v_1=(1,0)^\top$, $v_2=(0,2)^\top$, and $v_3=(1,2)^\top$.',
 [r'$av_1+bv_2=0$을 이용하여 $v_1,v_2$가 선형독립인지 판정하라.',r'$c=(3,4)^\top$를 $v_1,v_2$의 선형결합으로 나타내라. 계수가 유일한 이유도 설명하라.',r'$v_1,v_2,v_3$는 선형독립인가? 0이 아닌 계수의 선형관계를 하나 제시하라.'],
 [r'Use $av_1+bv_2=0$ to determine whether $v_1,v_2$ are linearly independent.',r'Express $c=(3,4)^\top$ as a linear combination of $v_1,v_2$. Explain why the coefficients are unique.',r'Are $v_1,v_2,v_3$ linearly independent? Give one relation whose coefficients are not all zero.'],
 'homework_variant','HW1 P6-P7','모든 벡터는 열벡터; 실수 계수',[46,47],(3,'P6-P7')))
q.append(Q('행 미분과 Jacobian','Row Derivatives and a Jacobian',
 r'$x=(u,v)^\top\in\mathbb R^{2\times1}$, $f(x)=(u-1)^2+2(v+1)^2$, $g(x)=(u+v,u-2v)^\top$이다. 스칼라 함수의 미분은 행벡터, Jacobian은 출력×입력으로 쓴다.',
 r'Let $x=(u,v)^\top\in\mathbb R^{2\times1}$, $f(x)=(u-1)^2+2(v+1)^2$, and $g(x)=(u+v,u-2v)^\top$. Use row derivatives for scalar functions and output-by-input Jacobians.',
 [r'$\nabla_x f$를 구하고 $(u,v)=(0,0)$에서 계산하라. 결과의 차원도 적어라.',r'$J_g$를 구하고 차원을 적어라.',r'$f$를 최소로 만드는 $x$와 최솟값을 구하라. 왜 전역 최소인지 제곱항으로 설명하라.'],
 [r'Find $\nabla_x f$ and evaluate it at $(u,v)=(0,0)$. State its dimensions.',r'Find $J_g$ and state its dimensions.',r'Find the minimizer of $f$ and its minimum value. Use the squared terms to justify global minimality.'],
 'homework_variant','HW1 P10-P12','과제 원문의 열 관례를 그대로 인용하는 문제가 아니라 새 행 관례 변형; 출력×입력 Jacobian',[153,155,156],(3,'P10'),))
q.append(Q('1차원 Gaussian의 곱','A Product of Univariate Gaussians',
 r'$p_0(z)=\mathcal N(z\mid0,2)$, $p_1(z)=\mathcal N(z\mid2,2)$, $z\in\mathbb R$이다. 둘째 인수는 분산이다. $Z=\int_{\mathbb R}p_0(z)p_1(z)\,dz$, $q(z)=p_0(z)p_1(z)/Z$라 하자.',
 r'Let $p_0(z)=\mathcal N(z\mid0,2)$ and $p_1(z)=\mathcal N(z\mid2,2)$ for $z\in\mathbb R$. The second argument is the variance. Define $Z=\int_{\mathbb R}p_0(z)p_1(z)\,dz$ and $q(z)=p_0(z)p_1(z)/Z$.',
 [r'곱의 지수에 나타나는 $z^2+(z-2)^2$를 완전제곱하라.',r'$q$의 평균·분산과 정규화된 밀도를 구하라.',r'$p_0p_1$의 상수 인자도 포함하여 $Z$를 구하라. $p_0p_1$ 자체가 밀도인지 판단하라.'],
 [r'Complete the square in $z^2+(z-2)^2$, which appears in the exponent of the product.',r'Find the mean, variance, and normalized density of $q$.',r'Compute $Z$, including the constant factors in $p_0p_1$. Is $p_0p_1$ itself a probability density?'],
 'homework_variant','HW1 P14,P25','두 Gaussian의 둘째 인수는 분산; 원래 곱과 정규화된 곱 구별',[207,208],(5,'P14; PDF 9쪽 P25')))
q.append(Q('작은 설계행렬의 ML과 MAP','ML and MAP with a Small Design Matrix',
 r'$\phi(x)=(1,x)^\top$, $f_\theta(x)=\phi(x)^\top\theta$, $\theta=(\theta_0,\theta_1)^\top$이다. 관측은 $(-1,1),(0,2),(1,3)$이고 잡음은 서로 독립인 $\mathcal N(0,1)$이다. MAP에서는 절편을 포함한 두 계수 모두에 $\theta\sim\mathcal N(0,I_2)$를 사용한다. ML/MAP의 표준 공식을 사용해도 된다.',
 r'Let $\phi(x)=(1,x)^\top$, $f_\theta(x)=\phi(x)^\top\theta$, and $\theta=(\theta_0,\theta_1)^\top$. The observations are $(-1,1),(0,2),(1,3)$, with independent $\mathcal N(0,1)$ noise. For MAP use $\theta\sim\mathcal N(0,I_2)$ for both coefficients, including the intercept. You may use the standard ML and MAP formulas.',
 [r'관측 순서대로 $\phi(x_n)^\top$를 쌓은 설계행렬 $\Phi$와 $y$를 구성하라.',r'$\Phi^\top\Phi$, $\Phi^\top y$, $\hat\theta_{\rm ML}$을 구하라.',r'$\hat\theta_{\rm MAP}$과 $x_*=0$에서의 평균 예측을 구하라. 절편도 줄어드는 이유를 설명하라.'],
 [r'Construct the design matrix $\Phi$ by stacking $\phi(x_n)^\top$ in observation order, and construct $y$.',r'Compute $\Phi^\top\Phi$, $\Phi^\top y$, and $\hat\theta_{\rm ML}$.',r'Compute $\hat\theta_{\rm MAP}$ and the predicted mean at $x_*=0$. Explain why the intercept also shrinks.'],
 'homework_variant','HW1 P9,P17,P19','입력 고정; 잡음분산 1; 모든 계수에 N(0,I2) prior',[300,302,307,308],(3,'P9; PDF 6쪽 P17,P19')))
q.append(Q('평균·공분산과 단순한 변환','Mean, Covariance, and a Simple Transformation',
 r'$X$는 $(0,0)^\top,(2,0)^\top,(0,2)^\top,(2,2)^\top$ 중 하나를 각각 확률 $1/4$로 갖는다. $Y=AX+b$, $A=\operatorname{diag}(2,1)$, $b=(1,-1)^\top$라 하자. 공분산은 이 확률분포에 대한 것으로 분모는 $4$이다. Gaussian은 가정하지 않는다.',
 r'$X$ takes each of $(0,0)^\top,(2,0)^\top,(0,2)^\top,(2,2)^\top$ with probability $1/4$. Let $Y=AX+b$, where $A=\operatorname{diag}(2,1)$ and $b=(1,-1)^\top$. Compute covariance under this distribution, using denominator $4$. Do not assume a Gaussian distribution.',
 [r'$\mu_X=E[X]$를 구하라.',r'$\Sigma_X=E[(X-\mu_X)(X-\mu_X)^\top]$를 구하라.',r'$E[Y]$, $\operatorname{Cov}(Y)$, $\operatorname{Cov}(X,Y)$를 구하라. 이동 $b$가 공분산에 영향을 주는지도 설명하라.'],
 [r'Compute $\mu_X=E[X]$.',r'Compute $\Sigma_X=E[(X-\mu_X)(X-\mu_X)^\top]$.',r'Compute $E[Y]$, $\operatorname{Cov}(Y)$, and $\operatorname{Cov}(X,Y)$. Explain whether the shift $b$ affects covariance.'],
 'homework_variant','HW1 P21-P22','명시한 이산분포; 분모4; Gaussian 가정 없음; Cov(X,Y)의 순서 고정',[194,196,198,200],(7,'P21; PDF 8쪽 P22')))
q.append(Q('잡음모델에서 최소제곱까지','From a Noise Model to Least Squares',
 r'$y_n=\phi(x_n)^\top\theta+\epsilon_n$, $\phi(x)=(1,x)^\top$, $\theta\in\mathbb R^{2\times1}$이다. 고정된 관측은 $(x_1,y_1)=(-1,1)$, $(x_2,y_2)=(1,3)$이고 $\epsilon_1,\epsilon_2$는 서로 독립인 $\mathcal N(0,1)$이다. $\Phi$의 $n$번째 행은 $\phi(x_n)^\top$이다. 미분은 행벡터로 쓴다.',
 r'Let $y_n=\phi(x_n)^\top\theta+\epsilon_n$, $\phi(x)=(1,x)^\top$, and $\theta\in\mathbb R^{2\times1}$. The fixed observations are $(x_1,y_1)=(-1,1)$ and $(x_2,y_2)=(1,3)$. The errors are independent $\mathcal N(0,1)$. Row $n$ of $\Phi$ is $\phi(x_n)^\top$. Use row derivatives.',
 [r'잡음분포에서 $p(y_n\mid x_n,\theta)$를 얻고, 독립성을 이용하여 두 관측의 likelihood $L(\theta)$를 상수까지 포함해 써라.',r'$-\log L(\theta)$를 구하라. 이를 최소화하는 것이 평균 제곱오차(ERM)를 최소화하는 것과 같은 이유를 설명하라.',r'$Q(\theta)=\|y-\Phi\theta\|^2$를 행 미분하고 0으로 놓아라. 양변을 전치하여 정규방정식을 도출하라.',r'이 데이터의 $\Phi^\top\Phi$와 $\Phi^\top y$를 계산하여 $\hat\theta_{\rm ML}$과 훈련 예측 $\hat y$를 구하라. 해의 유일성도 확인하라.'],
 [r'Obtain $p(y_n\mid x_n,\theta)$ from the noise distribution. Use independence to write the likelihood $L(\theta)$ of both observations, including its constant factor.',r'Find $-\log L(\theta)$. Explain why minimizing it is equivalent to empirical risk minimization (ERM) with mean squared error.',r'Compute the row derivative of $Q(\theta)=\|y-\Phi\theta\|^2$ and set it to zero. Transpose both sides to derive the normal equations.',r'Compute $\Phi^\top\Phi$ and $\Phi^\top y$ for these data, then find $\hat\theta_{\rm ML}$ and the training predictions $\hat y$. Check uniqueness.'],
 'theory_application','MML 9.2.1-9.2.2; HW1 P15-P17','입력 고정; θ 조건부 독립; 알려진 분산1; 행 미분',[298,299,300,302]))
q.append(Q('평균모델의 prior와 MAP','A Prior and MAP in a Mean Model',
 r'$y_n=\theta+\epsilon_n$이고 $\theta\in\mathbb R$, $\epsilon_n\stackrel{\rm iid}{\sim}\mathcal N(0,1)$이다. 관측은 $D=(y_1,y_2)=(1,3)$이다. prior는 $\theta\sim\mathcal N(0,1)$이며 잡음과 독립이다.',
 r'Let $y_n=\theta+\epsilon_n$, where $\theta\in\mathbb R$ and $\epsilon_n\stackrel{\rm iid}{\sim}\mathcal N(0,1)$. The data are $D=(y_1,y_2)=(1,3)$. Use the prior $\theta\sim\mathcal N(0,1)$, independent of the noise.',
 [r'Bayes 법칙을 이용하여 $p(\theta\mid D)$를 likelihood와 prior의 곱에 비례하는 식으로 써라. 정규화 상수는 계산하지 않아도 된다.',r'음의 log-posterior를 $\theta$와 무관한 상수를 제외하고 구하라. 데이터 오차 제곱합에 어떤 penalty가 더해지는가?',r'앞 목적함수를 미분하여 $\hat\theta_{\rm MAP}$을 구하고, prior를 제외한 $\hat\theta_{\rm ML}$과 비교하라.',r'prior만 $\mathcal N(0,1/4)$로 바꾸어 MAP을 다시 구하라. prior 분산 감소가 추정값에 미친 영향을 설명하라.'],
 [r'Use Bayes rule to express $p(\theta\mid D)$ as proportional to likelihood times prior. You need not compute the normalizing constant.',r'Find the negative log-posterior up to terms independent of $\theta$. What penalty is added to the sum of squared data errors?',r'Differentiate that objective to find $\hat\theta_{\rm MAP}$. Compare it with $\hat\theta_{\rm ML}$ obtained without the prior.',r'Change only the prior to $\mathcal N(0,1/4)$ and recompute MAP. Explain the effect of decreasing the prior variance.'],
 'theory_application','MML 9.2.3-9.2.4; HW1 P18,P24','모수1개; 독립 잡음분산1; prior 분산1 또는1/4',[307,308,309]))
q.append(Q('한 관측의 사후분포와 새 예측','One Observation, Posterior, and Prediction',
 r'$\theta\sim\mathcal N(0,1)$, $y=\theta+\epsilon$, $\epsilon\sim\mathcal N(0,1)$이고 $\theta,\epsilon$은 독립이다. $y=2$를 관측했다. 새 입력에서 잡음 없는 값은 $f_*=2\theta$, 관측값은 $y_*=2\theta+\epsilon_*$이다. $\epsilon_*\sim\mathcal N(0,1)$는 $\theta,\epsilon$과 독립이다. Gaussian의 아핀 변환·독립합 공식을 사용해도 된다.',
 r'Let $\theta\sim\mathcal N(0,1)$ and $y=\theta+\epsilon$, with $\epsilon\sim\mathcal N(0,1)$ independent of $\theta$. Observe $y=2$. At a new input the noise-free value is $f_*=2\theta$ and the observation is $y_*=2\theta+\epsilon_*$, where $\epsilon_*\sim\mathcal N(0,1)$ is independent of $\theta,\epsilon$. You may use the affine-transformation and independent-sum rules for Gaussians.',
 [r'잡음모델을 이용하여 관측 $y=2$의 likelihood $p(y=2\mid\theta)$를 써라. 여기서 likelihood는 관측점에서 평가한 밀도이다.',r'likelihood와 prior를 곱하고 완전제곱하여 정규화된 $p(\theta\mid y=2)$를 구하라.',r'앞 사후분포를 이용하여 $f_*\mid y=2$의 평균·분산과 분포를 구하라.',r'$y_*\mid y=2$의 평균·분산과 분포를 구하라. (c)에 비해 분산이 늘어나는 이유를 설명하라.'],
 [r'Use the noise model to write the likelihood $p(y=2\mid\theta)$. Here likelihood means the density evaluated at the observed value.',r'Multiply likelihood and prior, complete the square, and obtain the normalized posterior $p(\theta\mid y=2)$.',r'Use that posterior to find the mean, variance, and distribution of $f_*\mid y=2$.',r'Find the mean, variance, and distribution of $y_*\mid y=2$. Explain why its variance exceeds that in (c).'],
 'theory_application','MML 9.3.3-9.3.4; Lecture04 p14','분산표기; 새 잡음은 θ와 관측잡음에 독립; 모수와 잡음의 불확실성 구별',[312,314,315]))
q.append(Q('0을 관측했을 때의 모델 비교','Model Comparison after Observing Zero',
 r'두 모델은 $M_0:y=\epsilon$, $M_1:y=\theta+\epsilon$이다. 두 모델의 잡음은 $\epsilon\sim\mathcal N(0,1)$이고, $M_1$에서는 독립인 prior $\theta\sim\mathcal N(0,3)$를 사용한다. 모델 사전확률은 각각 $1/2$이고 관측은 스칼라 $y=0$ 하나이다. Gaussian 독립합 성질을 사용해도 된다. Bayes factor의 방향은 $B_{01}=p(y=0\mid M_0)/p(y=0\mid M_1)$이다.',
 r'Consider $M_0:y=\epsilon$ and $M_1:y=\theta+\epsilon$. In both models $\epsilon\sim\mathcal N(0,1)$. Under $M_1$, use the independent prior $\theta\sim\mathcal N(0,3)$. Both models have prior probability $1/2$. The data consist of one scalar observation $y=0$. You may use the independent-sum property of Gaussians. Define $B_{01}=p(y=0\mid M_0)/p(y=0\mid M_1)$.',
 [r'각 모델의 주변분포 $p(y\mid M_i)$를 구하라. $M_1$에서는 prior를 평균낸다는 뜻을 적분식과 독립합의 분산으로 설명하라.',r'각 주변밀도를 관측 $y=0$에서 평가하여 evidence를 구하라.',r'$B_{01}$을 계산하고 어느 모델에 유리한지 설명하라.',r'posterior odds와 $P(M_0\mid y=0)$를 구하라. 연속형 데이터의 evidence를 점확률 0으로 놓으면 안 되는 이유도 설명하라.'],
 [r'Find the marginal distribution $p(y\mid M_i)$ under each model. Under $M_1$, explain averaging over the prior using an integral and the variance of an independent sum.',r'Evaluate each marginal density at $y=0$ to obtain the evidences.',r'Compute $B_{01}$ and state which model it favors.',r'Find the posterior odds and $P(M_0\mid y=0)$. Explain why the evidence for continuous data must not be replaced by a zero point probability.'],
 'theory_application','Lecture04 p17; MML 9.3.3,9.3.4','모델prior각1/2; M0 모수없음; M1 prior분산3; evidence는 밀도값',[312,319]))
q.append(Q('한 직선으로의 직교투영','Orthogonal Projection onto a Line',
 r'$b=(1,1,0)^\top$, $y=(2,0,1)^\top$이고 $\hat y=b\theta$로 근사한다. 내적은 Euclidean 내적이다. 확률 해석에서는 $y=b\theta+\epsilon$, $\epsilon\sim\mathcal N(0,I_3)$을 사용한다.',
 r'Let $b=(1,1,0)^\top$ and $y=(2,0,1)^\top$, and approximate $y$ by $\hat y=b\theta$. Use the Euclidean inner product. For the probabilistic interpretation, use $y=b\theta+\epsilon$ with $\epsilon\sim\mathcal N(0,I_3)$.',
 [r'오차벡터 $y-b\theta$가 $b$에 수직이라는 조건에서 $\hat\theta$를 구하라.',r'$\hat y=b\hat\theta$와 적합 잔차 $r=y-\hat y$를 구하고 $b^\top r=0$을 직접 확인하라.',r'$\hat y=Py$를 만족하는 직교투영행렬 $P$를 구하라. $P^\top=P$, $P^2=P$를 확인하라.',r'임의의 $\theta$에 대해 $\|y-b\theta\|^2=\|r\|^2+(\theta-\hat\theta)^2\|b\|^2$임을 설명하라. 최소 제곱오차를 구하고 이 해가 ML인 이유를 설명하라.'],
 [r'Find $\hat\theta$ by requiring the error vector $y-b\theta$ to be orthogonal to $b$.',r'Find $\hat y=b\hat\theta$ and the fitted residual $r=y-\hat y$, and directly verify $b^\top r=0$.',r'Find the orthogonal projection matrix $P$ satisfying $\hat y=Py$. Check $P^\top=P$ and $P^2=P$.',r'Explain why $\|y-b\theta\|^2=\|r\|^2+(\theta-\hat\theta)^2\|b\|^2$ for every $\theta$. Find the minimum squared error and explain why this solution is ML.'],
 'theory_application','MML 3.8,9.4; Lecture04 p20,p24','유클리드내적; b≠0; 알려진 동일 Gaussian 잡음분산1',[319,320]))

if __name__=='__main__':
 dump(RUN/'questions-only.json',q)
 # No answer or explanation appears in this file; it is the blind review input.
 sources=[]
 for id,p in [('mml',next(R.rglob('Mathematics_for_Machine_Learning.pdf'))),('hw',next((R/'과제/과제1').glob('26_10*rev.pdf'))),('l04',R/'강의노트/Lecture04_Linear_Regression_Part2_rev_HO.pdf'),('stt1019',R/'STT/1019 머러기.md')]:
  sources.append(dict(id=id,path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 bp=dict(schema_version=1,range='0909-1019',slug='Midterm_Practice_02',style='exam',difficulty='중하 (1회차 대비 차원·계산·추론 부담 축소)',exam_hint=dict(source='stt1019',lines=[312,314],interpretation='약 절반 과제 유사, 약 절반 모델을 차근차근 분석; 10문항은 사용자 지정'),scope=dict(end='1019 orthogonal projection',excluded=['logistic regression','SVM'],count=10,official_time_points='미확인; 지정하지 않음'),sources=sources,questions=[])
 for i,x in enumerate(q,1):
  refs=[dict(source='mml',pdf_pages=x['pages'])]
  hw_pages={1:[3],2:[3,4],3:[5,9],4:[3,6],5:[7,8],6:[5,6],7:[6,9]}
  if i in hw_pages:refs.append(dict(source='hw',pdf_pages=hw_pages[i],problems=x['ref']))
  if i in (8,9,10):refs.append(dict(source='l04',pdf_pages={8:[14],9:[17],10:[20,24]}[i]))
  bp['questions'].append(dict(id=f'p{i}',kind='homework_variant' if i<=5 else 'model_analysis',subparts=list(string.ascii_lowercase[:len(x['ask'])]),origin_kind=x['origin'],origin_ref=x['ref'],theory_refs=refs,course_evidence=[dict(source='stt1019',lines=[312,314],scope='시험범위 종료점·과제/모델 분석 비율 안내')],assumptions=x['assumptions']))
 dump(OUT/'.pack/blueprint.json',bp)
 print('questions-only and blueprint authored:',sum(len(x['ask']) for x in q),'subparts')
