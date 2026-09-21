# 0916 머신러닝기초 강의 아웃라인 (정방철 교수, 약 72분 25초)

**참고:** 전사본 2,004줄 전체를 Part 01부터 Part 08까지 순서대로 모두 읽었습니다. 슬라이드 범위를 맞추려고 `강의노트/Lecture01…pdf`, `Lecture02…pdf`의 텍스트를 추출해 대조했고, 직전 수업(`STT/0914 머러기.md`)의 마지막 부분도 확인했습니다. 타임스탬프는 강의 시작 기준 절대시간이며 Part 번호를 함께 적었습니다. STT가 한글로 받아 적은 영어 용어는 정식 용어로 고쳤습니다.

**전체 흐름:** MLE를 다시 짚고 i.i.d. 가정으로 NLL을 유도함 → 가우시안 노이즈 가정에서 MLE가 Least Squares와 같아짐 → MAP (Bayes 정리, uniform prior이면 MLE와 같음) → Model fitting, overfitting/underfitting → (Lecture02) generative process와 확률 모형 → joint, prior, likelihood, posterior, marginal likelihood → ML, MAP, Fully Bayesian 비교 (장군님 비유, 동전 예시) → posterior predictive 식을 보여 주고 "다음 시간에 자세히"로 마무리.

---

## 0. 도입 잡담 (P01 00:00–00:24)
- 작은아버지 식구들이 추석 때 할머니 드시라고, 애들 먹으라고 **추석 선물 세트**를 들고 온다는 이야기를 합니다. 이 비유는 06:29에 데이터를 모아 행렬 X로 만드는 설명에서 다시 나옵니다.

## 1. 지난 시간 복습과 likelihood의 뜻 (P01 00:26–04:59) — Lec01 슬라이드 14
**핵심 내용**
- 모델을 **deterministic function**으로 두면 ERM이나 least squares를 풀어 파라미터를 튜닝합니다. **확률 모형**으로 두면 PDF의 파라미터(가우시안이면 평균과 분산)를 최적화합니다. 후자의 대표 방법이 **Maximum Likelihood Estimation**입니다.
- [슬라이드 외] **likelihood의 어원:** likely는 "~할 것 같다"이고, 여기에 -hood가 붙어 명사형 "그럴 것 같음, 그럴듯함"이 됩니다. maximum likelihood는 "가장 그럴듯함"입니다. 교수는 "우리말 '그럴듯하다'가 likelihood와 정확히 같은 뜻"이라고 했습니다. 방금 연구실 학생들과 커피를 마시며 나눈 얘기라면서 "그 분야에서 쓰는 용어들을 조금 섬세하게 볼 필요가 있다"고 했습니다.
- [슬라이드 외] 머신러닝은 **귀납적 학문**입니다. 데이터 뒤에 숨은 latent variable, latent model, 패턴을 수학적으로 해석하는 방법론이라고 설명했습니다("이번 학기 2주째 계속 이런 설명밖에 안 하고 있는데"). "그럴 것 같다, 확신한다" 같은 말을 수학으로 옮기면 **확률**이 됩니다. 그 확률이 가장 큰 것을 고르는 게 공학자에게 가장 효과적인 방법이고, MLE, detection, classification이 모두 확률을 도입합니다.
- **Negative log-likelihood의 논리**
  - log는 **단조증가 함수**라서 log를 취해도 값의 대소(우열)가 바뀌지 않습니다.
  - loss와 risk는 보통 "부정적 metric"으로 정의하므로 minimize하고 싶습니다. 그래서 $-\log$를 붙입니다.
  - 따라서 $\arg\max_\theta p(\cdot\mid\theta) = \arg\min_\theta\,[-\log p(\cdot\mid\theta)]$이고, 이것을 최소화하는 θ를 **maximum likelihood estimator**라고 부릅니다.

## 2. i.i.d.와 데이터 표기 (P01 04:59–07:01) — 슬라이드 15
- 지도학습 데이터: $(x_1,y_1),\dots,(x_N,y_N)$, $x_n\in\mathbb{R}^D$.
- ⚠️ i.i.d.에 대해 교수는 "지난 시간에도 i.i.d.에 대해 그렇지, 좀 강조를 했었죠?"라고 했습니다. $x_1$은 짝인 $y_1$에만 영향을 주고 $y_2$ 등에는 영향을 주지 않습니다. 다음 데이터가 생성될 때는 통계적으로 독립입니다. 교수는 이것을 "identically and independently distributed"라고 불렀습니다.
- **추석 선물 세트 비유:** D차원 벡터 $x_1,\dots,x_N$을 "모아 모아 모아서 세트로 만든" 입력 집합을 **"멋드러지게 꺾어 놓은 X"**, 즉 $\mathcal{X}$로 씁니다. 정답 $y_1,\dots,y_N$(N×1)은 $\mathcal{Y}$입니다.

## 3. NLL 공식과 "왜 하필 log인가" (P01 07:02–09:22)
- ⚠️ "negative log-likelihood를 계산하는 방법은 **항상 예외 없이** 이 수식을 쓰는 거예요… 묻지도 말고 따지지도 말고 -log를 쳐."
- ⚠️ "항상 예외 없이… 마이너스를 붙이고 로그를 취하고 likelihood가 되면 항상 이렇게 conditional probability 또는 conditional PDF를… 이렇게 **외워도 돼요**." (곧바로 "물어도 되고 따져도 되긴 해"라고 농담)
$$\mathcal{L}(\theta) = -\log p(\mathcal{Y}\mid\mathcal{X},\theta)$$
- [슬라이드 외] **exp나 linear 같은 다른 단조증가 함수가 아니라 log를 쓰는 이유**
  1. **가우시안 때문:** 노이즈나 observation을 가우시안으로 모델링하는 경우가 많은데, log를 취하면 exponential이 사라집니다.
  2. **작은 확률값을 확대:** 확률이 0.0000…처럼 매우 작아지면 0.001과 0.002(두 배 차이)의 격차가 잘 드러나지 않습니다. log 함수는 1보다 작은 영역을 늘려 줍니다. 교수는 이것을 **예능이나 영화에서 감독이 보고 싶은 영역을 클로즈업하는 것**에 비유했습니다.
  3. 보충 설명: **확률밀도함수의 값 자체는 1보다 클 수 있고**, 적분한 값만 1을 넘을 수 없습니다.

## 4. latent variable θ와 "확률 모형을 정의한다"는 것 (P01 09:22 – P02 12:18)
- x가 주어졌을 때 y가 나오게 만드는 파라미터 θ를 **latent parameter 또는 latent variable**(숨겨진 변수)이라고 부릅니다. 지도학습에는 정답지가 있습니다.
- (가상 질문) "왜 '정의(define)'한다고 하나요?" 답: x와 y의 관계를 deterministic function으로 둘지 PDF로 둘지는 **내가 정하는 것**이기 때문입니다.
- [슬라이드 외] 예시:
  - 지수분포 $f(x)=\lambda e^{-\lambda x}$ ($x\ge0$). λ에 따라 가파르게 또는 느리게 감소합니다.
  - 가우시안에서 $\mu=\theta_1,\ \sigma^2=\theta_2$로 두면 $f(x;\theta_1,\theta_2)=\frac{1}{\sqrt{2\pi\theta_2}}\exp\!\big(-\frac{(x-\theta_1)^2}{2\theta_2}\big)$가 되어 PDF가 θ의 식이 됩니다.
- $p(\mathcal{Y}\mid\mathcal{X},\theta)$를 최대화하는 θ가 최적화, 학습, 트레이닝, 훈련해야 할 파라미터(latent variable)입니다.
- ⚠️ "여기까지의 수식은 **그 어떤 머신러닝 문제가 있어도** probabilistic modeling을 하겠다고 마음을 먹으면 **항상** 여기서 여기까지는 그냥 쓰는 거예요."

## 5. i.i.d. 가정을 적용한 칠판 유도 (P02 12:27–15:56) — 슬라이드 15
**칠판 유도 단계**
1. 시작 식: $\mathcal{L}(\theta)=-\log p(\mathcal{Y}\mid\mathcal{X},\theta)$
2. **Independence만 쓰면** 곱으로 분해됩니다. $x_n$은 $y_n$하고만 관련이 있고, 관계 파라미터를 $\theta_n$으로 둡니다.
$$-\log\prod_{n=1}^N p(y_n\mid x_n,\theta_n)$$
3. **Identically distributed까지 쓰면** 모두 같은 PDF이므로 첨자 n을 지우고 $\theta$ 하나로 씁니다.
$$-\log\prod_{n=1}^N p(y_n\mid x_n,\theta)$$
4. $\log(ab)=\log a+\log b$를 적용합니다. (STT에는 "로그 a 곱하기 로그 b는…"이라고 잘못 말했다가 곧바로 고치는 부분이 있습니다.)
$$\mathcal{L}(\theta)=-\sum_{n=1}^N\log p(y_n\mid x_n,\theta)$$
   이것을 negative log-likelihood function 또는 log-likelihood loss라고 부르며, 이것을 최소화하는 게 목표입니다.

**교수가 든 이유**
- [슬라이드 외] 데이터 하나를 만들 때마다 PDF가 바뀐다면 PDF 하나를 추정하는 데 데이터가 1개밖에 없게 됩니다. "말이 안 되잖아, 이거 빅데이터 아니잖아요?" 그래서 데이터 전체를 설명하는 PDF 하나를 만들고, i.i.d.를 가정합니다.
- (질문, 실제 학생 질문인지 교수의 수사적 질문인지는 불분명) "$y_1$이 $x_1$에 의해 만들어지는 이 데이터 세트가 확률밀도함수 하나에 의해서만 만들어진다는 겁니까?" 답: "맞아요. **동일한 공장에서 동일한 불확실성을 갖고 찍어낸** 데이터 N개 세트를 가지고 있다는 가정이에요."

## 6. 가우시안 노이즈 가정: MLE와 Least Squares가 같아짐 (P02 16:12 – P03 20:26) — 슬라이드 15
- 모델: $y_n = x_n^\top\theta+\varepsilon$, $\varepsilon\sim\mathcal N(0,\sigma^2)$. 그러면 $y_n\mid x_n,\theta\sim\mathcal N(x_n^\top\theta,\ \sigma^2)$입니다. 평균은 $x_n$과 θ의 내적입니다. (17:15 "저기 리모컨 좀")
$$p(y_n\mid x_n,\theta)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\Big(-\frac{(y_n-x_n^\top\theta)^2}{2\sigma^2}\Big)$$

**칠판 유도 (A항, B항 분리)**
$$\mathcal L(\theta)=-\sum_{n=1}^N\Big[\underbrace{\log\tfrac{1}{\sqrt{2\pi\sigma^2}}}_{A}+\underbrace{\log\exp\!\Big(-\tfrac{(y_n-x_n^\top\theta)^2}{2\sigma^2}\Big)}_{B}\Big]
= -N\log\tfrac{1}{\sqrt{2\pi\sigma^2}}+\frac{1}{2\sigma^2}\sum_{n=1}^N(y_n-x_n^\top\theta)^2$$
- A항은 n과 무관하므로 N번 더하면 $N\log\frac{1}{\sqrt{2\pi\sigma^2}}$입니다. **θ와 무관하므로** "이퀄이 아니라 **비례한다(∝)**로 바꾸면서" 무시합니다. (엄밀히는 상수를 더한 것이지만 argmin은 같습니다.)
$$\mathcal L(\theta)\ \propto\ \frac{1}{2\sigma^2}\sum_{n=1}^N(y_n-x_n^\top\theta)^2=\frac{1}{2\sigma^2}\|y-X\theta\|_2^2$$
- [슬라이드 외] 각 성분 제곱의 합은 벡터 $y-X\theta$의 **유클리드 노름의 제곱**과 같습니다. 따라서 확률 모형의 MLE가 deterministic 모델의 **Least Squares 문제와 동일**해집니다.

## 7. MAP (Maximum A Posteriori) (P03 20:34–28:16) — 슬라이드 16
- [슬라이드 외] **posterior의 뜻:** "사후"이지만 "죽은 후(after death)가 아니고 사건이 발생한 이후"라는 뜻입니다. 그래서 사후 분포라고 부르며, 역시 conditional probability입니다. 확률 및 랜덤변수 수업의 forward/reverse probability, Bayesian learning/inference와 연결됩니다.
- **추론 문제의 틀 (학생 문답):** "여러분 손에 쥐어진 게 데이터예요, 세타예요?" → "데이터지." "찾으려는 건?" → "세타지."
  - [슬라이드 외] **의사의 CT 판독 비유:** 의사 손에 쥐어진 것은("많은 연봉이 쥐어…" 농담) 영상, 숫자, 테이블 같은 데이터입니다. 의사는 그것을 보고 암인지 건강한지라는 원인 파라미터를 추론합니다.
- ⚠️ "보통의 inference problem의 체계를 수학으로 옮겨 놓으라고 하면 **항상 이 수식을 기억해야 돼.** 나한테 주어진 건 뭐지? 내가 알고 싶은 건 뭐지?" 주어진 것을 조건에 두고 추론하려는 파라미터를 앞에 두면 그것이 posterior distribution입니다.

**칠판 유도**
1. 조건부확률의 정의: $P(A\mid B)=\frac{P(A,B)}{P(B)}$ (STT에는 "나누기 P A"로 나오는데 말실수 또는 인식 오류이며 $P(B)$가 맞습니다.)
2. Multiplication rule로 분자를 풉니다. "확률 및 랜덤변수 2주차에 하는 게 이거잖아."
$$p(\theta\mid x)=\frac{p(x,\theta)}{p(x)}=\frac{p(x\mid\theta)\,p(\theta)}{p(x)}$$
3. 분모가 θ와 관련이 있느냐는 질문에 학생들이 "없지"라고 답합니다. 그래서 무시하고 ∝를 씁니다: $p(\theta\mid x)\propto p(x\mid\theta)p(\theta)$
4. [슬라이드 외] **max와 argmax의 차이:** max는 "최대가 된 확률값이 얼마냐"이고, **argmax는 "그 수식을 최대화하게 만드는 θ를 찾아라"**입니다.
5. -log로 바꿉니다.
$$\theta_{\text{MAP}}=\arg\max_\theta p(\theta\mid x)=\arg\min_\theta\big[-\log p(x\mid\theta)-\log p(\theta)\big]$$
6. [슬라이드 외] 뒤의 $-\log p(x\mid\theta)$는 "방금 한 거", 즉 **MLE 항**입니다. 여기에 θ의 marginal PDF(prior)가 log로 더해져 있고, 확률로 보면 곱해져 있는 셈입니다.
7. [슬라이드 외] **prior를 상수(uniform)로 두면** θ와 무관해집니다. 교수는 "uniform 분포가 purely random이잖아요"라고 했고, 이 경우 **MAP 규칙이 ML 규칙과 같아집니다.**

## 8. Model fitting (P03 28:19 – P04 31:53) — 슬라이드 17
- 공지: "다음 주부터 제대로 된 regression으로 바로 들어갈 거니까"
- (가상 질문) "모델 피팅과 파라미터 피팅은 같은 건가요?" 답: 파라미터에는 training, learning, optimization, fitting이라는 말을 쓰고, 이것은 **모델 파라미터**에 쓰는 표현입니다. **Model fitting은 모델 자체를 바꾸는 것**입니다. 최선을 다해 파라미터를 튜닝했는데도 성능이 나쁘면 모델을 바꿔 봐야 합니다.
- **"전지전능한 지니/천사/요정" 비유:**
  - x에서 y가 생성되는 진짜 과정은 요정만 알고 있는 **$M^*$**(ideal unknown model)입니다.
  - 나는 모르니까 linear, Gaussian, mixed Gaussian 등으로 **$M_\theta$**를 가정합니다.
  - 초기값 $M_{\theta_0}$에서 gradient descent, 최적화, 확률 도입 등으로 파라미터를 학습해 **$M_{\theta^*}$**에 도착합니다. 교수는 "보통 스타(*)는 optimal에 쓴다"고 했습니다.
  - $M_{\theta^*}$는 "linear라는 **모델 클래스 안에서의 최선**"입니다. $M_{\theta^*}$와 $M^*$ 사이의 **빨간 거리**가 클수록 좋지 않은 모델이고, 우연히 가까워지면 좋은 학습을 한 것입니다.

## 9. Overfitting, Underfitting, Good fitting (P04 31:53–38:12) — 슬라이드 17 그림
**Overfitting**
- 가진 데이터 점들만 기가 막히게 설명하는 ML 추정을 한 경우입니다. 새 입력 3에서는 실제와 크게 차이가 나고, **입력 -2에서는 -100으로 예측**할 수 있습니다.
- [슬라이드 외] **논문 실수 일화:** 학생들이 데이터셋으로 학습시킨 뒤 **그 데이터셋의 일부로 테스트한 결과를 논문에 싣는** 실수를 합니다. 학습에 쓴 1.3 같은 입력을 다시 넣으면 당연히 맞힙니다. 교수는 이를 "되새김질… 당연히 소화가 잘 되겠지"라고 비유했습니다. ⚠️ "말이 안 되는 거야. **이렇게 하면 안 돼.**"
- 결과: 과하게 적합한 탓에 **unseen data**에 대해 예상치 못한 큰 에러가 납니다.
- 원인: **데이터 개수에 비해 너무 복잡한 모델**입니다. 옛날에는 underfitting이 많았고 **요즘은 overfitting이 더 많습니다.** 8,000만 원짜리 GPU를 "이빠이" 돌려 파라미터가 많은 모델을 쓰기 때문입니다.
- [슬라이드 외] **모델 사이즈 = the number of parameters to be optimized.** 교수는 LLaMA, GPT 파라미터 수를 예로 들었는데 STT상 "70만 개", "530만 개"로 나옵니다. 실제로는 70B, 530B 규모를 말하려던 것으로 보입니다.

**Underfitting**
- 데이터는 많은데 **너무 간단한 모델**("난 모르겠고 리니어로 해")을 쓴 경우입니다. **내 데이터조차 설명이 안 됩니다.** 과거에 컴퓨팅 파워가 부족해 작은 모델을 쓸 때 흔했습니다.
- [슬라이드 외] 장점: **모델이 안정적**입니다. 어떤 데이터가 와도 적당히는 맞추지만 아주 잘 맞추지는 못합니다.

**Good fitting**
- "개념적인 얘기니까 그냥 머릿속으로 받아만 두세요." 데이터 사이즈와 모델 사이즈가 적절해서 현재 데이터와 앞으로 들어올 데이터를 모두 잘 설명하는 상태입니다.
- Model fitting은 **컴퓨팅 자원의 양, 풀려는 문제의 크기, 손에 쥔 데이터의 개수**를 모두 녹여서 판단해야 합니다.
- (가상 질문) "어떻게 하면 잘 할 수 있습니까?" 답: "GPT한테 물어보세요. 농담이고", 결국 사람의 노하우가 필요하다고 했습니다.

## 10. Part 2 진입과 복습 (P04 38:12–39:15) — Lec02 슬라이드 2~4
- "파트 2에서는 세 가지 토픽을 다룰 건데 아마 오늘은 이 4, 5를 간단하게 좀 다루고, 모델 셀렉션은 거의…" 실제로는 (4)만 부분적으로 다뤘습니다.
- 복습: 모델을 어떻게 가정하고 파라미터를 어떻게 학습할지, model fitting과 selection도 요즘은 learning의 일부라는 점, deterministic과 probabilistic이라는 두 원칙, 확률 모형이면 ML/MAP으로 PDF를 "guess"한다는 점.

## 11. Generative process와 확률 모형 (P04 39:15 – P05 44:58) — Lec02 슬라이드 5
- 많은 ML task는 **unseen event의 prediction**과 expected risk를 최소화하는 **decision making**입니다. 이를 위해 확률 모형을 많이 씁니다.
- 관측 데이터가 어떤 **generative process**(random process)로 만들어졌을 것이라고 가정(suppose)하고 모델을 세우는 것이 확률 모형입니다.
- 예: $y_n=x_n^\top\theta+n$, $n\sim\mathcal N(0,\sigma^2)$ … "만들어졌을 **거야**"
- [슬라이드 외] **신승훈 일화:** 국문학 전공이라 작사와 작곡을 직접 했다는 이야기입니다. 교수가 곡명을 잊자 학생 영석이 "보이지 않는 사랑"이라고 알려 줬습니다. 마지막 가사가 "~했을 거야"로 끝나는데, 교수는 "신승훈 톤으로" generative process를 다시 설명하며 이 표현을 썼습니다. 교수가 "만들어졌을…"에서 멈추자 **학생 예림이 "거야"를 받아쳐 줬고**, 교수는 "고맙다, 예림아"라고 했습니다. (이어서 메일을 보낸 예림이 이예림인지 전예림인지 헷갈린 잡담이 있습니다.)
- [슬라이드 외] **데이터는 온전하지 않다:** 온도 측정이나 사진이 물리 세계의 정보를 전부 담지는 못합니다. 소리에는 잡음이 끼는데, 지금 교수가 노래하는 동안에도 에어컨 소리가 녹음되고 있고 녹음실이라면 이런 것을 제외한다는 예를 들었습니다. "**마가 낀 게 아니고 노이즈가 꼈을 거다**"라고 했습니다. 그 노이즈를 random variable(불확실성)로 가정하는 것이 probabilistic model입니다.

## 12. Joint distribution, marginal, latent/hidden parameter (P05 45:03 – P06 50:28)
- ⚠️ "확률 랜덤 변수 수업이 **이만큼 중요한 거야.**" (예림이 확률 수업을 들었다고 답했습니다.)
- [슬라이드 외] **정보가 가장 많은 분포는 joint 분포**입니다. $f_X(x), f_\theta(\theta), f_Y(y)$는 **marginal PDF**로, 자기 자신의 불확실성만 설명합니다. PDF/PMF를 알면 그 확률변수의 평균, 분산, 함수의 기댓값, 공분산 등 **모든 것**을 알 수 있습니다("주민등록번호를 알아야 되나?" 농담). 확률변수가 둘이면 **joint PDF**를 알아야 다 압니다. 그래서 probabilistic modeling에서는 가능하다면 joint distribution을 알아야 합니다.
- θ는 확률론에서는 **hidden parameter**, 머신러닝에서는 **latent variable**이라고 부르며, x를 설명할 단서를 제공합니다.
  - [슬라이드 외] **인셉션 비유:** "왜 꿈속의 꿈으로 들어가요?" 표면에 보이는 현상은 x이고, 그 안의 코어(기작)가 θ입니다. θ를 바꿔 가며 현상이 어떻게 변하는지 보고 싶은 것이 ML의 습성입니다.
- [슬라이드 외] **칠판 설명:** $x_n$은 given이고 θ는 추정 대상이라 둘 다 확률변수가 아닙니다. 따라서 $c_n = x_n^\top\theta$는 상수입니다.
$$y_n=c_n+n,\ n\sim\mathcal N(0,\sigma^2)\ \Rightarrow\ y_n\sim\mathcal N(c_n,\sigma^2)$$
  가우시안에 상수를 더하면 평균만 $c_n$으로 이동합니다. $c_n$은 **θ의 함수**이므로, θ는 평균을 바꾸는 방식으로 데이터에 영향을 줍니다.

## 13. "θ가 key information을 encapsulate한다"의 올바른 관점 (P06 50:28–52:16)
- 슬라이드 문구: joint distribution과 hidden parameter가 "encapsulate the key information".
- ⚠️ ML은 연역이 아니라 **귀납**입니다. (가상 질문) "θ가 원래 key information을 담고 있는 겁니까?" 교수: "**그거 아니라니까. 머신러닝을 연구할 때 그런 생각은 없애야 된다니까.**" θ가 key information을 머금도록 모델을 잘 설정하고 **만들어 가고 최적화해야** 한다는 것이 올바른 관점입니다.
- 모델 가정이 잘못되면(8절의 원 그림, $M^*$와의 거리) 최적화에 한계가 있습니다. 목표는 실제 데이터를 잘 설명할 뿐 아니라 **unseen data도 잘 예측하는 θ**입니다.

## 14. Prior × Likelihood = Joint, 그리고 regularization과의 연결 (P06 52:16–55:35)
$$p(x,\theta)=p(x\mid\theta)\,p(\theta)$$
- Joint 확률은 multiplicative rule로 항상 decompose(인수분해)됩니다. $p(\theta)$는 **prior**이고, $p(x\mid\theta)$는 **likelihood**입니다.
- [슬라이드 외] likelihood는 확률 수업에서 배운 **forward probability** 또는 **transition probability**이기도 하며, "보통 주어지는 경우가 많다"고 했습니다.
- [슬라이드 외] **prior = 사전(before):** x를 관찰하기 **전에** 내가 가진 notion, 컨셉, **편견, 바이어스, preference, 의도(intention)**입니다. "인간적인 면이 들어가 있다", "**모름지기 파라미터는 이런 거 아니겠습니까?**"라고 표현했습니다.
- **Lec01 슬라이드 12(regularization)로 되돌아가 연결했습니다:**
$$\min_\theta\ \frac1N\|y-X\theta\|^2+\lambda\|\theta\|^2$$
  - $\lambda=0$이면 "선험적인 편견 따위는 고려하지 않겠다"는 뜻입니다.
  - λ가 크면 "모름지기 θ는 벡터 크기가 작을수록 좋다"는 선호를 수식에 녹인 것입니다. prior가 이 regularization 항을 만드는 데 기여합니다.
  - "요게 이제 연관이 됩니다, 좀 이따가… **나중에 다시 썰 푸는 걸로.**" 수식 유도는 하지 않았습니다.
- [보충: 수업에서 유도하지 않음, 예고만 함] 가우시안 prior $\theta\sim\mathcal N(0,b^2I)$를 두면 $-\log p(\theta)=\frac{1}{2b^2}\|\theta\|^2+\text{const}$입니다. 따라서 MAP 목적함수는 $\frac{1}{2\sigma^2}\|y-X\theta\|^2+\frac{1}{2b^2}\|\theta\|^2$이 되고, 이는 L2 regularization에서 $\lambda=\frac{\sigma^2}{Nb^2}$인 경우와 같습니다. (MML 8.3.2, 9.2.3 참고)

## 15. Posterior와 marginal likelihood (P06 55:38–58:59) — 슬라이드 5 하단
- ⚠️ "여러분들이 머신러닝을 한다, 데이터로부터 학습 모형을 만들어 낸다라고 할 때 **항상 이 확률 수식을 기억해야 되거든요.**" 내 손안의 데이터는 무엇이고 추론할 파라미터는 무엇인지 따져서 $p(\theta\mid x)$를 최대화하는 문제로 푼다는 뜻입니다.

**칠판 유도**
$$p(\theta\mid x)=\frac{p(x,\theta)}{p(x)}=\frac{p(x\mid\theta)p(\theta)}{p(x)},\qquad
p(x)=\int_{-\infty}^{\infty}p(x,\theta)\,d\theta=\int p(x\mid\theta)p(\theta)\,d\theta$$
$$\therefore\ p(\theta\mid x)=\frac{p(x,\theta)}{\int p(x,\theta)\,d\theta}$$
- Marginal PDF는 joint PDF를 **관심 없는 θ에 대해 적분**해서 구합니다.
- [슬라이드 외] "위, 아래, 위, 아래… 팔짱 끼고 쳐다보면" 분자도 joint이고 분모도 joint입니다. (가상 질문) "왜 꼭 저렇게 합니까?" 답: "**엔지니어링적으로 효과적**입니다. 함수 하나만 계산하면 분자에도 쓰고, 적분해서 분모에도 쓸 수 있으니까."

## 16. Prediction 문제 설정 (P06 58:59 – P07 60:39) — Lec02 슬라이드 6 도입
- 데이터셋 X가 주어졌을 때 사건 A를 예측합니다: $P(A\mid X)$. 러닝이 끝나 모형이 최적화된 뒤, **unseen data**에 대해 개인지 고양이인지, 남자인지 여자인지, **재밍(jamming)이 있었는지** 같은 classification을 하는 상황입니다.
- ⚠️ "이 강의 자료는 진짜 여러분들 강의 **이걸 들어야 돼요.** 지난 학기 확률 및 랜덤변수 수업 시간에 강의해 놨다… 거기서 누차 내가 얘기했어요. 오늘 요약본으로 설명할 테니까 오늘 가서 **꼭** 강의 수강…" 연구실 학생 수연이의 반말에 대한 농담이 이어졌습니다.

## 17. ML vs MAP vs Fully Bayesian: 장군님, 동전, 머니볼 (P07 60:40–69:25) — 슬라이드 6
**장군님 비유 [슬라이드 외]** (확률 수업에서 자주 쓴 비유)
- 장군님은 복잡하고 긴 말을 싫어하고 **Yes/No 단답형**을 요구합니다("청문회 같네요").
- 엔지니어와 데이터 사이언티스트는 "원재료"인 분포 전체를 가지고 있습니다.
- **Fully Bayesian은 엔지니어가 좋아하는 방식**(복잡하지만)이고, **ML과 MAP은 단답을 원하는 장군님이 좋아하는 대답**입니다.

**동전 예시 (학생 기훈과의 문답)**
- **Fully Bayesian:** 앞면이 나올지 뒷면이 나올지 묻자 기훈이 "앞면 0.5, 뒷면 0.5"라고 답했습니다. 이것이 정확한 대답이고 Fully Bayesian입니다. PMF(0 = 앞면, 1 = 뒷면, 각각 0.5)를 그대로 보고하는 것이며, 교수는 discrete-time signal처럼 이산 시퀀스 정보를 말로 설명한 것이라고 했습니다(신호 및 시스템 비유). "성능은 이게 **왔다**지"라고 해서 성능은 Fully Bayesian이 가장 좋다고 했습니다.
- **ML:** 머릿속에 P(앞)=0.2, P(뒤)=0.8이 있을 때 장군님이 "그래서 앞이냐 뒤냐?"라고 물으면 "**뒷면**"이라고 답합니다. 근거는 "열 번 던졌는데 앞면 두 번, 뒷면 여덟 번 나왔으니 **앞면 확률이 0.2이기 때문에 이런 데이터가 나오지 않았겠습니까?**"입니다. 데이터에만 기반한 추정입니다.
  - Binomial 분포로 설명했습니다. 반반이면 10번 중 5에서 peak가 서는데, 뒷면이 8번이면 peak가 8에 오는 분포가 나오려면 θ(앞면 확률)가 0.2여야 합니다. 0.5라는 관념을 가진 사람의 머릿속 binomial은 5에서 peak입니다. "계산해 보면 이거 **미분해 보면 나오거든요.** 디테일한 얘기는 나중에."
  - [보충] $\ell(\theta)=\log\binom{10}{2}+2\log\theta+8\log(1-\theta)$이고, $\frac{2}{\theta}-\frac{8}{1-\theta}=0$에서 $\hat\theta_{ML}=0.2$입니다.
- [슬라이드 외] **머니볼** 영화: 브래드 피트 주연, 오클랜드 야구팀이 데이터 사이언티스트를 활용한 이야기입니다. 교수는 데이터 사이언티스트를 뚱뚱하고 펩시와 햄버거만 먹으며 CRT 모니터를 보는 사람으로 묘사한 게 기분이 좋지 않았다고 했습니다. 데이터 사이언티스트에게는 본능적 감각이 없다는 점을 들어 "기훈이는 데이터 사이언티스트야, ML을 이해한 거야"라고 했습니다.
- **MAP:** $\arg\max p(\theta\mid x)\propto p(x\mid\theta)p(\theta)$입니다. 데이터 사이언티스트의 말만 듣지 않고 "**모름지기 동전이면 반반이어야 되는 거 아니야?**"라는 선입견, 편견, 의도(prior)까지 반영합니다. "네 생각과 내 생각을 섞자"고 해서 앞면 확률을 **0.3 정도**로 씁니다. "정확하게 어떻게 반영했는지는 **나중에 설명할게**."
  - [보충] Beta(α,β) prior를 쓰면 $\theta_{MAP}=\frac{k+\alpha-1}{N+\alpha+\beta-2}$입니다. 예를 들어 α=β=4이면 5/16 ≈ 0.31입니다.
- [슬라이드 외] **야구 일화:** 야구인 출신 코치는 "내가 해봐서 아는데 에이징 커브가 아니라 **어제 술 먹은** 거다, 혼내면 다음엔 잘 던진다"고 하고, 데이터 사이언티스트는 "이미 꺾였다, 구속이 안 나온다"고 합니다. 교수는 "**온전한 솔루션은 항상 그 사이에 있다**"고 했습니다. prior와 데이터를 섞는 것이 MAP의 직관입니다.
- **Fully Bayesian 정리:** θ를 하나로 결정하지 않고 **PDF 자체를 predictive distribution으로 사용**합니다.

**슬라이드 6의 식**
$$\text{ML: }P(A\mid X)\approx P(A\mid\theta_{ML}),\ \theta_{ML}=\arg\max_\theta P(X\mid\theta)\qquad
\text{MAP: }P(A\mid X)\approx P(A\mid\theta_{MAP}),\ \theta_{MAP}=\arg\max_\theta P(\theta\mid X)$$

## 18. Fully Bayesian의 실제와 posterior predictive (P07 69:27 – P08 72:19)
- (가상 질문) θ(앞면 확률)에 대한 분포가 연속 곡선으로 나오면 장군님께 그림을 그려 가며 설명해야 해서 말이 길어집니다. "everybody dislikes this."
- [슬라이드 외] 그래서 predictive distribution을 **가우시안으로 가정**하면 **파라미터 두 개로** 설명할 수 있습니다. 예: "장군님, 평균 7.8, 분산 3.2인 가우시안입니다." 교수는 확률값 θ처럼 [0,1] 범위인 경우는 **Beta distribution**이 어울린다고 언급했습니다.
- [슬라이드 외] 봉우리가 여럿이면 **mixed Gaussian**으로 표현합니다: $(\mu_1,\sigma_1),(\mu_2,\sigma_2),(\mu_3,\sigma_3)$의 합으로, 정규화하면 $\sum_k\pi_k\mathcal N(\mu_k,\sigma_k^2)$입니다. 교수는 이것이 **학기 말에 할 EM(Expectation-Maximization) 알고리즘**과 관련된 모델이라고 예고했습니다.
- **칠판 유도 (슬라이드 6):**
$$P(A\mid X)=\int P(A,\theta\mid X)\,d\theta=\int P(A\mid\theta,X)\,P(\theta\mid X)\,d\theta=\int P(A\mid\theta)\,P(\theta\mid X)\,d\theta$$
  - θ로 marginalize하면 θ가 사라지는 구조를 거꾸로 이용합니다. θ가 주어지는 순간 X의 영향이 사라지므로 $P(A\mid\theta,X)=P(A\mid\theta)$이며, 이는 슬라이드의 conditional independence 가정입니다. 이 식을 **posterior predictive distribution**이라고 합니다.
  - "이거는 **다음 시간에 조금 더 자세히 다시 설명할게요.**"
- 72:19 "오늘 강의는 여기까지… 질문 있으신 분 받겠습니다." 이후 질의응답은 녹음되지 않았습니다.

---

## 학생 질문과 답변
**실제 학생과의 문답**
- 22:20 "데이터예요, 세타예요?" → "데이터"
- 25:26 "분모가 θ와 관련 있어요?" → "없지"
- 42:00 영석이 곡명 "보이지 않는 사랑"을 알려 줌
- 43:46 예림이 "거야"로 호응
- 45:11 예림이 확률 수업 수강 여부에 "네"
- 62:18 기훈이 "앞면 0.5, 뒷면 0.5"라고 답함

**교수의 수사적 가상 질문** (교수는 "교수님, ~?" 형식으로 학생 질문을 흉내 낸 뒤 스스로 답하는 습관이 있습니다)
- 07:15 왜 log를 쓰는가
- 10:05 왜 "define"이라고 하는가
- 14:45 하나의 PDF에서만 생성되는가 (실제 질문일 가능성도 있음)
- 28:40 모델 피팅과 파라미터 피팅은 같은가
- 37:53 어떻게 하면 잘 하는가
- 47:37 왜 인셉션처럼 들어가는가
- 50:51 θ가 원래 key info를 담는가
- 58:40 왜 joint로 쓰는가
- 69:27, 70:59 연속 분포나 다봉 분포는 어떻게 설명하는가

## 이번 수업의 슬라이드 범위 (추정)
- **시작:** Lecture01 **슬라이드 14~15**(MLE 개념, MLE in supervised learning)를 다시 짚으며 시작했습니다. 직전 수업(0914)은 슬라이드 15의 예제 직후 "MAP은 수요일에"라고 하며 끝났습니다.
- Lecture01 슬라이드 16(MAP) → 17(Model Fitting). 중간에 슬라이드 12(Regularized LS)로 잠깐 되돌아갔습니다(54:35).
- Lecture02 슬라이드 2~4(Targets, Roadmap) → **슬라이드 5**(Generative Process와 Probabilistic Models, 약 20분) → **슬라이드 6**(Fully Bayesian vs ML/MAP).
- **끝:** 슬라이드 6 중간에서 끝났습니다. 조건부 독립 Q/A는 "다음 시간"으로 미뤘습니다.
- **다루지 않은 부분:** 슬라이드 7(Bayesian inference의 어려움: MCMC, Laplace, VI, EP), 9~15(Graphical models, d-separation), 17~19(Nested CV, Bayesian model selection, Bayes factor).

## 공지사항 (원문 인용)
- 28:19 "우리가 **다음 주부터 제대로 된 리그레션으로 바로 들어갈 거니까**"
- 38:17 "파트 2에서는… 세 가지의 토픽을 다룰 건데 아마 오늘은 이 4, 5를 간단하게 좀 다루고 모델 셀렉션은…" (실제로는 4만 일부 진행)
- 55:32 "요게 이제 연관이 됩니다, 좀 이따가… 그건 **나중에 다시 썰 푸는 걸로**" (prior와 regularization의 수식 연결)
- 60:01 "지난 학기에 **확률 및 랜덤 변수** 수업 시간에 강의해 놨다… 오늘 가서 꼭 강의 수강" (복습 권고)
- 66:53 "디테일한 얘기는 나중에" (ML 미분 계산), 68:15 "어떻게 정확하게 반영했는지는 나중에 설명할게" (MAP prior 반영)
- 71:32 "**학기 말에 할 EM 알고리즘**"
- 72:04 "이거는 **다음 시간에 조금 더 자세히** 다시 설명할게요" (posterior predictive)
- **퀴즈, 과제, 시험범위 언급은 없었고, "시험에 나온다"류 발언도 없었습니다.** 참고로 0914 수업 끝에서는 "이제 뭐 숙제도 좀 내주고 이그잼플도 좀 풀어보고"라고 예고했지만, 이번 수업에서 과제는 나오지 않았습니다.

## ⚠️ 강조 발언 모음
- 07:02 "항상 예외 없이 이 수식을 쓰는 거예요… 묻지도 말고 따지지도 말고 -log를 쳐"
- 08:59 "외워도 돼요"
- 12:18 "그 어떤 머신러닝 문제가 있어도… 항상 여기까지는 그냥 쓰는 거예요"
- 23:41 "항상 이 수식을 기억해야 돼"
- 56:22 "항상 이 확률 수식을 기억해야 되거든요"
- 33:45 학습 데이터로 테스트하는 것은 "이렇게 하면 안 돼"
- 45:11 "확률 랜덤 변수 수업이 이만큼 중요한 거야"
- 51:00 "그런 생각은 없애야 된다니까"

## 전제지식 (MML 교과서 챕터 대응)
- **Ch.6 확률과 분포:** 조건부확률의 정의, product(multiplication) rule, sum rule과 marginalization(∫dθ), Bayes 정리, joint/marginal PDF와 PMF, PDF 값이 1을 넘을 수 있다는 점, 독립, 조건부 독립, i.i.d., 평균, 분산, 공분산, 가우시안(상수를 더하면 평균이 이동), 지수분포, 이항분포, Beta 분포와 conjugacy, 가우시안 혼합
- **Ch.2 선형대수:** 데이터 행렬 $X\in\mathbb R^{N\times D}$, 벡터 표기
- **Ch.3 해석기하:** 내적 $x_n^\top\theta$, 유클리드 노름 $\|y-X\theta\|^2$
- **Ch.5 벡터 미적분:** 미분으로 MLE 구하기 ("미분해보면 나오거든요")
- **Ch.7 연속 최적화:** gradient descent, min과 argmin, 단조변환(log)으로 최적해가 보존됨
- **Ch.8 (본 강의):** 8.3.1 MLE, 8.3.2 MAP, 8.3.3 Model fitting, 8.4 Probabilistic modeling과 inference. 예고된 내용은 Ch.9 Linear regression(다음 주)과 Ch.11 GMM/EM(학기 말)입니다.
- **다른 과목:** 확률 및 랜덤변수(2주차 조건부확률, 장군님 비유, 머니볼), 신호 및 시스템(discrete-time signal 비유)

## 교과서, 연습문제, 특정 챕터 언급
- **MML 교과서 챕터 번호나 연습문제를 직접 언급한 부분은 없습니다.**
- 대신 "지난 학기 확률 및 랜덤변수 강의"를 반복해서 참조했고, "확률 및 랜덤변수 2주차 = conditional probability"를 명시했습니다. 앞으로 다룰 주제로는 regression(다음 주)과 EM 알고리즘(학기 말)이 언급됐습니다.
- 수업에서 "나중에"로 미룬 세 가지 계산은 위 본문에 [보충]으로 따로 표시해 두었습니다: 동전 MLE의 미분 계산, Beta prior를 쓴 MAP, 가우시안 prior와 L2 regularization의 등가성. 필기 노트를 만들 때 이 부분은 수업에서 실제로 유도하지 않았다는 점을 구분해 주세요.