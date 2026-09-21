# 0914 머신러닝기초 강의 개요 (정방철 교수, 2026-09-14)

**총평.** 1,584줄(Part 01–08)을 처음부터 끝까지 읽었습니다. 녹음은 약 74분(00:00–73:57)이고 80분은 아닙니다. 이번 수업은 **Lecture01 "When Models Meet Data – Part 1"의 후반부**였습니다. Lecture02(Probabilistic Modeling, DGM, d-separation, Model Selection, Bayes factor)는 **시작하지 않았습니다.** 흐름은 이렇습니다. 모델은 "suppose"의 문제라는 복습 → Empirical Risk Minimization → Loss → Regularization → MLE → Gaussian 노이즈에서 MLE와 Least Squares가 같다는 것 → MAP 예고.
슬라이드 범위는 `강의노트/Lecture01_When_Models_Meet_Data_Part1.pdf`의 슬라이드 텍스트와 대조해 추정했습니다.

---

## 1. 복습: 모델은 "suppose"이고 선호의 문제다 (Part 01 00:00–04:04)

**핵심 내용**
- 데이터는 1차식, 2차식, 비선형 함수, 뉴럴넷(NN) 등 어떤 것으로든 모델링할 수 있다.
- **suppose와 assume의 차이** [슬라이드 외]
  - assume: 사실이 아닌 줄 알면서 그렇다고 가정하는 것.
  - suppose: 모르니까 그렇게 추측하는 것.
  - 모델을 고르는 일은 suppose다. "뉴럴넷으로 모델링하니까 비교적 잘 예측이 되던데? 그러면 되는 거야."
- 모델은 correct/incorrect(옳고 그름)의 문제가 아니다. **good/bad, 취사선택, preference(선호)**의 문제다.
- 수학은 definition에서 시작한다. definition은 참·거짓의 문제가 아니라 "유용하니까 그렇게 하기로 한 것"(by definition)이다. 그러니 좋은 모델과 나쁜 모델은 있어도, 옳은 모델과 그른 모델은 없다.

**비유와 일화**
- **영화 추천 (지난 시간 예시 복습)**
  - 사람 마음속의 심리적 기작은 알 수 없다.
  - 1년 전에 좋아하던 영화와 올해 좋아하는 영화가 다를 수 있다. 즉 "time-varying"이다.
  - 결론은 "Nobody knows." 그래도 데이터를 가능한 한 정확히 설명하려는 노력이 머신러닝이다.
- **GPU 일화**
  - 교수님이 1억 2천만 원짜리 GPU를 사준 랩은 "파라미터 30만 개짜리 NN"을 써도 된다.
  - 우리 랩은 작은 GPU밖에 없다.
  - 작은 모델로 비슷한 성능을 내는 쪽이 더 좋은 ML 엔진이다.

**학생과의 대화**
- 교수가 "수학은 뭘로부터 시작한다?"라고 묻자 한 학생이 호응했다. 교수가 "지난 학기에 확률을…" 들었는지 확인하며 짧게 대화했다.

⚠️ "거기에 있어서 이 모델을 결정하는 문제는 매우 중요하다." (01:24)

## 2. 학습(Training)의 의미와 범위 (Part 01 04:04–05:47)

- **예시**
  - $y = ax+b$로 "호기롭게" 설명해 보기로 한다.
  - $a=0.3,\ b=1.8$로 최적화하고, unseen $x$가 들어오면 $y$를 예측한다.
  - 이 과정이 training(학습, learning)이다.
- 모델 자체가 잘못되어 있으면 학습을 아무리 잘해도 unseen data에서 한계가 있다.
- [슬라이드 외] 예전에는 "학습 중입니다"라고 하면 그걸로 끝이었다.
  - 요즘 "학습한다"는 말에는 **모델을 바꿔보는 것, 즉 하이퍼파라미터를 건드려 모델 자체를 바꾸는 것까지** 포함된다.
  - 슬라이드 8의 "Model selection to choose hyperparameters"와 연결된다.
- "그 이그잼플 좀 이따 설명할게요. 크로스 밸리데이션이라고 하는데"라고 예고했지만, **이번 수업에서는 실제로 다루지 않았다.**

## 3. 오늘의 구성: Deterministic Function과 Probabilistic Model (Part 01 05:47–06:19)

모델을 정하는 방법은 크게 두 가지다.
1. deterministic function으로 정의한다 → ERM.
2. probabilistic model, 즉 PDF(확률밀도함수)로 정의한다 → MLE/MAP.

## 4. "Empirical Risk Minimization"이라는 용어 해석 (Part 01 06:19 – Part 02 11:58)

**핵심 내용**
- "강의 노트를 대충 만들지 않는다. 용어에 뉘앙스가 다 있다."
  - **Empirical** = 실험적이다. 플라톤 철학자처럼 "모름지기 데이터는 이래야만 해"라고 상상한 것이 아니라, 데이터를 실제로 넣어봤다는 뜻이다.
  - **Risk** = 위험 요소, 즉 부정적인 metric이다.
  - **Minimization** = 그것을 최소화한다.
- 정리하면, 함수 모델을 suppose하고(파라미터 $a, b$는 아직 미지수) 현재 데이터를 가장 잘 설명하도록 파라미터를 최적화한다. **risk를 최소화하는 관점에서.**
- 파라미터는 constant라고 부르기도 하지만 보통 파라미터라고 한다.
- [슬라이드 외] 공학에서 "최적"이라는 말 뒤에는 반드시 **"in terms of ★"**가 붙어야 한다.
  - "인생에서 무엇이 최적인가요?" 같은 질문은 허황되다.
  - "슬램덩크 기술은 없어요. 얼티메이트 옵티말 기술은 없다고 세상에."
  - 인생의 선택도 6개월만 지나면 "그때 그거 잘못했어" 한다. 인생은 후회의 연속이다.
- [슬라이드 외] 인공지능수학 과목에서 convex optimization, least squares, linear algebra, PCA를 배우는 이유는 **제약조건(constraint) 하의 최적화 이론**이 필요하기 때문이다.
- [슬라이드 외] 신호처리 연구자들이 ML을 잘하는 이유는 그들이 "최적화의 달인"이어서 빨리 갈아탈 수 있기 때문이다.

**일화: 이메일**
- 학기 초에 청강·수강 부탁 이메일이 많아서, 교수님이 지난주 학장님께 "이런 것 좀 하지 말자"고 건의했다.
- 한 학생이 "시간표상 교수님 수업이 편리하니 이미 신청한 과목을 바꾸고 싶다"고 메일을 보냈다.
  - 학교에 머무는 시간을 minimize하는 최적화를 한 것이고, 자기 삶을 관리하는 좋은 일이다.
  - 하지만 교수님은 답장하지 않았다. 핵심은 "어떤 관점에서 최적화하느냐"이다.

⚠️ "우리가 이 엔지니어로서 항상 이런 생각을 해야 돼요." (09:30, in terms of 관점)

⚠️ "어떤 관점에서 최적화를 하는지가 되게 중요하거든요." (10:07)

⚠️ "여러분들이 강의 노트를 이렇게 볼 때도 그냥 허투루 보지 말라는 거예요." (10:32)

⚠️ "여러분 머신러닝을 잘한다는 건 사실 최적화를 잘한다는 거예요." (11:16)

## 5. Predictor와 데이터 표기법 (Part 02 11:58–15:42)

- ML 엔진은 보통 **predictor**(예측기)이며, inference라고도 부른다. 새 데이터의 정답을 예측하는 함수이고, 여기서는 deterministic하다.
- 학습 데이터는 $\{(\mathbf{x}_1,y_1),\dots,(\mathbf{x}_N,y_N)\}$이고 supervised learning을 가정한다.
- **표기 관습 (by convention)**
  - 소문자 볼드 $\mathbf{x}$는 벡터, 일반체 $y$는 스칼라다.
- $\mathbf{x}_n\in\mathbb{R}^D$이다. $D=3$이면 $\mathbf{x}_1=[x_{11},x_{12},x_{13}]^\top$이다.
- **칠판에서 행렬 패킹**
  - $N$개의 열벡터를 나란히 묶으면 "길이 $D$, 너비 $N$"인 행렬이 된다.
  - 행의 수는 벡터 길이, 열의 수는 데이터 개수다.
  - **주의:** 슬라이드 11은 $X\in\mathbb{R}^{N\times D}$로 전치된 형태를 쓴다. 교수가 30:08에 이를 정정했다(9절 참고).
- 파라미터 세트(예: $a, b$)를 모은 벡터를 $\boldsymbol\theta$라 한다.

## 6. 좋은 파라미터 θ* 찾기와 "for all"의 의미 (Part 02 15:42 – Part 03 20:49, 슬라이드 10)

$$\text{Find }\boldsymbol\theta^*\ \text{ such that }\ f(\mathbf{x}_n,\boldsymbol\theta^*)=\hat y_n\approx y_n,\quad \forall n=1,\dots,N$$

- 모델(1차식이든 2차식이든)은 이미 정했고, 학습 파라미터 $\theta_1,\theta_2,\dots$를 찾는다.
  - 교수는 "라마(LLaMA) 같은 경우는 30만 개"라고 말했다. 이는 **발언 그대로 옮긴 것이며 실제 규모와는 다르다.**
  - 파라미터를 학습하는 것이 GPU의 역할이다.
- "such that"의 영어 의미를 설명했다. "수학은 언어니까."
- $y_n$은 데이터로 주어진 정답(라벨)이고, $\hat y_n$은 튜닝된 모델의 출력이다. 식의 뜻은 "A = B인데 B가 B′과 비슷했으면 좋겠다"이다.
- regression, classification, PCA, NN, 딥러닝은 수학적으로 표현하면 **모두 이것을 하는 것**이다.
- **"for all"의 의미 (예시)**
  - $\mathbf{x}_1$에 넣었을 때 정확히 $y_1$이 나오도록 미친 듯이 튜닝했다면, $\mathbf{x}_1$에 과적합된 것이다.
  - 같은 $\mathbf{x}_1$이 다시 들어오면 완벽한 엔진이다.
  - 하지만 $\mathbf{x}_2$를 넣었더니 $y_2$와 크게 다르다면 나쁜 예측기다.
  - 그래서 특정 데이터에 과적합하지 말고, 모든 학습 데이터에 두루두루 그럴듯한 파라미터를 찾아야 한다.

⚠️ "그런데 여기서 보면 이거는 for all이라는 말이 붙죠, 여기 또? 하나도 버릴 단어가 없어." (18:40)

## 7. 예시: Affine Function 모델 (Part 03 20:49–27:00, 슬라이드 10)

**칠판 유도**
1. 원래 하고 싶었던 모델:
   $f(\mathbf{x}_n,\boldsymbol\theta)=\theta_1x_{n1}+\theta_2x_{n2}+\dots+\theta_Dx_{nD}+b$
   입력의 weighted sum(내적)에 bias를 더한 것이다. 1차식이고 linear model이다.
2. 파라미터는 $\theta_1,\dots,\theta_D$($D$개)에 bias 하나를 더한 것이다. bias를 $\theta_0$로 "퉁친다."
3. bias가 밖에 나와 있어서 "까탈스럽다." $\theta_0 = 1\cdot\theta_0$이므로 **데이터를 augmentation**한다.
   - 맨 앞에 상수 1(unit feature $x^{(0)}=1$)을 "묻지도 따지지도 말고" 붙인다.
   $$\mathbf{x}_n=[1,x_n^{(1)},\dots,x_n^{(D)}]^\top\in\mathbb{R}^{D+1},\quad \boldsymbol\theta=[\theta_0,\theta_1,\dots,\theta_D]^\top$$
4. 그러면 $f(\mathbf{x}_n,\boldsymbol\theta)=\boldsymbol\theta^\top\mathbf{x}_n=\theta_0+\sum_{d=1}^D\theta_dx_n^{(d)}$이다. $\boldsymbol\theta^\top$는 가로, $\mathbf{x}_n$은 세로이므로 내적이다.
   - 교수 노트의 $n1, nd$와 슬라이드의 $n{,}1$ 표기는 같은 것이다.

**Linear와 Affine의 차이**
- 데이터와 무관한 상수가 더해져 있다.
- linear function은 원점을 지나야 하는데, 이 함수는 원점을 지나지 않을 수 있으므로 affine function이라 부른다.

**교수의 자문자답**
- "교수님, 왜 그렇게 하셨어요? 그냥 했어. 해본 거야."
- 이렇게 해서 괜찮으면 이걸로 끝내고, 안 되면 뉴럴넷을 쓴다.
- "I just tried. … 근거 없는 믿음으로 돌진해보는 거야."

⚠️ "여러분 여기가 되게 중요하다니까." (25:55)

⚠️ "내가 만약에 머신러닝을 공부하는 데 있어서 여러분들이 가장 중요한 컨셉이 뭐냐라고 묻는다면 저는 이 수식을 만드는 거라고 생각해요." (26:00)

⚠️ "제일 중요해요, 지금까지는. … 정말 중요하다니까, 이게. 이 모델을 이렇게 셋업하는 게 중요해요." (26:19)

## 8. 뉴럴넷의 뉴런도 결국 Affine Function (Part 03 27:00–29:14) [슬라이드 외]

슬라이드 10에는 "Neural network: Complex non-linear function" 한 줄만 있고, 칠판에서 확장해 설명했다.

- 칠판에 뉴런을 그렸다.
  - 입력 $x_1,\dots,x_D$에 가중치 $w_1,\dots,w_D$를 곱하고, $\sum_i w_ix_i+b$를 계산한다.
  - 여기에 비선형 activation function $\sigma(\cdot)$를 씌운다.
  - STT에는 "델타 또는 에타"로 인식되어 기호가 불명확하다. 예로 sigmoid와 ReLU를 들었다.
- 딥러닝은 이런 레이어가 여러 개 있는 것이다.
- "세상에서 가장 복잡한 모델이라고 알려진 DNN도 사실은 affine function의 weighted sum"이다. 레이어링으로 합친 composite function일 뿐이다.
- GPU는 원래 그래픽 처리용으로 곱셈과 덧셈을 하던 장치다. 곱셈·덧셈은 나눠서 할 수 있으므로 코어를 여러 개 두어 병렬 계산이 가능하고, 그래서 계산을 잘한다.

## 9. 데이터 행렬, Empirical Risk, Squared Loss (Part 03 29:14 – Part 05 39:54, 슬라이드 11)

**데이터 행렬**
- $X:=[\mathbf{x}_1,\dots,\mathbf{x}_N]^\top\in\mathbb{R}^{N\times D}$
  - "여기 트랜스포즈가 들어가 있네요"라고 정정했다.
  - 각 데이터 벡터를 가로로 눕혀 아래로 $N$개 쌓은 것이다.
  - 대문자 볼드는 행렬이다(convention). 라벨은 제외한 입력만 모은 것이다.
- $\mathbf{y}:=[y_1,\dots,y_N]^\top$는 세로 벡터다. 왜 이렇게 정의했는지는 "좀 있다 설명"한다고 했다.

**Average loss (Empirical risk)**
$$R_{\text{emp}}(f,X,\mathbf{y})=\frac1N\sum_{n=1}^N\ell(y_n,\hat y_n)$$
- 이것도 **정의(definition)**다. "꼭 저렇게 할 필요 없어요."
- 평균을 쓰는 이유는 특정 데이터가 아니라 두루두루 잘 동작하게 하려는 것이다. 학점 평점(4.0, 4.5, 3.5의 평균)에 비유했다.
- "잘 모르겠어도 팔짱 껴." 기호를 차분히 읽어보라는 뜻이다.
- $\ell$은 loss의 L에서 따온 것이고, 입력은 두 개다.
  - 첫째는 라벨(정답)이다.
  - 둘째는 $\hat y_n$이다. 이것은 **예측이 아니라 추정(estimate)**이다. 훈련 중에는 정답이 있지만 없다고 치고 계산한 값이기 때문이다.
  - hat(꺽쇠 모자)은 추정치를 뜻하는 관습이다. "추정 아니고 이 충치 같네"라는 농담이 있었다.
- loss는 $y_n$과 $\hat y_n$ 사이의 distance를 함수로 만든 것이다.
- "탑다운으로 보면 설계가 다 끝났는데", 아직 $\ell$의 정체는 말하지 않았다.

**Squared loss** (딥러닝에서도 많이 쓴다)
- $\ell(y_n,\hat y_n)=(y_n-\hat y_n)^2$
- $y_n$이 스칼라이므로 norm이 필요 없고 절댓값의 제곱이면 된다.

**칠판 유도: 스칼라 합에서 행렬 형태로**
1. $\frac1N\sum_n(y_n-\hat y_n)^2 = \frac1N\sum_n(y_n-\mathbf{x}_n^\top\boldsymbol\theta)^2$
2. 행별로 풀어 쓴다.
   - 1행: $(y_1-\mathbf{x}_1^\top\boldsymbol\theta)^2$
   - 2행: $(y_2-\mathbf{x}_2^\top\boldsymbol\theta)^2$
   - …
   - $N$행: $(y_N-\mathbf{x}_N^\top\boldsymbol\theta)^2$
3. 벡터 $\mathbf{y}-X\boldsymbol\theta$의 $n$번째 원소가 $y_n-\mathbf{x}_n^\top\boldsymbol\theta$이다.
4. 유클리디안 norm의 제곱은 각 원소를 제곱해서 더한 것이다.
   $$\min_{\boldsymbol\theta\in\mathbb{R}^D}\frac1N\|\mathbf{y}-X\boldsymbol\theta\|^2$$
5. $X\boldsymbol\theta = \hat{\mathbf{y}}=[\hat y_1,\dots,\hat y_N]^\top$이고 크기는 $N\times1$이다.

**김밥 비유** [슬라이드 외]
- $X$를 이렇게 정의한 것은 "나중에 아름답게 김밥으로 말기 위해 재료 손질을 한 것"이다. 교수님은 김밥을 좋아한다.

⚠️ "여러분 이거는 해보세요. 산수니까. 리니어 알지브라에서 이거 패킹하는 거 배웠잖아요." (37:24, 직접 해보라는 권유)

⚠️ "잊지 말아야 될 건 세타를 … 변화시키고 싶은 거." (38:22)

## 10. θ를 찾는 방법 예고 (Part 05 40:00–41:13)

- "바꿔 보면서 찾으세요. 무식하게."
  - $\theta$가 0~1 사이 값이면 실수 $D$개를 모두 탐색해야 한다.
  - 1을 추가한 augmentation을 쓰면 $D+1$개다.
- 이를 체계적으로 쉽게 푸는 방법이 선형대수에 있다. **least squares 알고리즘, pseudo-inverse** 등이다.
- 다음 주 linear regression에서 가르쳐 줄 예정이다.

## 11. 궁극 목표: Expected (True) Risk와 Train/Test 분할 (Part 05 41:13–46:27)

**가정**
- 앞으로 들어올 데이터가 지금 본 데이터와 크게 다르지 않다면, 현재 데이터에 잘 fitting하는 것으로 충분하다.
- [슬라이드 외] 성경 구절 "해 아래 새 것이 없다"(전도서)를 인용했다. 새 데이터도 이미 본 데이터의 일부일 것이라는 뜻이다. 이 가정이 성립하면 training만 잘되면 예측도 잘된다.

**바둑 AI 예시** [슬라이드 외]
- 전 세계 프로들의 **기보**를 학습했다.
- "이창호 9단이 바둑 두는 영상을 트레이닝했나요?" 그럴 필요가 없다.
- 바둑판을 벡터로 만들고, 흰 돌과 검은 돌의 위치와 순서를 데이터로 만든다. 교수는 이를 "그게 PCA이지", feature extraction이라고 표현했다.
- 그 결과 누가 들어와도 이긴다. "엠피리컬 로스를 미니마이즈하는 전략이 이미 서 있는 거지."

**Ultimate goal**
- 예측 리스크, 즉 unseen data에 대한 리스크를 최소화하는 것이다.
$$R_{\text{true}}(f)=\mathbb{E}_{\mathbf{x},y}\big[\ell(y,f(\mathbf{x},\boldsymbol\theta^*))\big]$$
- 교수는 "사실은 히든 레이턴트 베리어블이 있는 건데"라고 언급하며, 새로운 $\mathbf{x}$에 대해 평균적인 loss를 최소화하는 것이라고 설명했다.

**Train/Test 분할** [슬라이드 외]
- "70%로 트레이닝, 30%로 테스트. 7 대 3이다. 장인의 손맛 같은 거지." 청국장 끓일 때 소금을 몇 스푼 넣느냐와 같다.
- 또는 100 중 20은 test, 남은 80 중 20은 validation, 나머지 60은 training으로 쓴다.
- "정답은 없는 거야." 예측하고 싶은 것을 테스트 용도로 남겨두는 것이 좋다.

## 12. Overfitting과 Regularization (Part 05 46:27 – Part 06 54:12, 슬라이드 12)

**Overfitting**
- "fit too closely." 새 데이터에서 일반화가 안 되는 현상이다. "아, 내가 너무 오버했네" → overfitting.
- 해결책은 empirical risk에 **penalty term**을 추가하는 것이다.
  - "모름지기 세타란 말이야, 이래야만 해"라는 휴먼 메이드, 즉 **expert knowledge 항**이다.

**Regularized least squares**
$$\min_{\boldsymbol\theta}\ \frac1N\|\mathbf{y}-X\boldsymbol\theta\|^2+\lambda\|\boldsymbol\theta\|^2$$
- $\|\boldsymbol\theta\|^2$는 regularizer, $\lambda$는 regularization parameter이며 곧 **hyperparameter**다.
- 이것은 모델 자체를 바꾸지 않는다. 모델은 여전히 affine이다.

**λ에 따른 동작**
- $\lambda=0$: penalty가 사라져 empirical risk만 최소화하므로 "딱 과적합되기 좋지."
- $\lambda=1$: 훈련 데이터에 근접하려 하면서, 동시에 $\boldsymbol\theta$의 2-norm, 즉 **원점에서의 거리**도 체크한다. 둘 사이의 밸런스다.

**Norm 설명** [슬라이드 외]
- 2-norm의 제곱: $\|\boldsymbol\theta\|_2^2=\sum_d\theta_d^2$. 기하학적으로는 원점에서의 거리다.
- 1-norm: $\|\boldsymbol\theta\|_1=\sum_d|\theta_d|$
- p-norm: $\|\boldsymbol\theta\|_p=(\sum_d|\theta_d|^p)^{1/p}$
- 말장난: "노름이라고 하면 타짜 되는 건 아니니까 놈이라고 할게요", "이 놈 저 놈, 좋은 놈 나쁜 놈."
- **1-norm을 쓰면 sparse solution이 나온다.** 파라미터를 자꾸 0으로 만드는 습성이 있어서, nonzero인 원소의 개수를 최소화하려는 성질이 생긴다. 자세한 것은 최적화 시간에 배운다.

**1-norm이냐 2-norm이냐, λ는 0, 0.5, 1.5 중 무엇이냐** → "그게 바로 장인의 손맛이에요."
- **김밥 일화**
  - 교수님은 "고봉민김밥 홍보대사"이고 김가네김밥도 좋아한다.
  - 왜 좋아하는지 "휴먼 러닝"을 해보니 우엉을 좋아하는 것 같았다.
  - 낙지전골 뒤에는 우동사리보다 밥을 볶아 먹는 쪽을 좋아한다. 사람마다 취향이 다르다.
- 문제와 데이터에 따라 $\lambda=0.7$이 최적일 수도 있고 $0.9$가 최적일 수도 있다.

**Hyperparameter 최적화** [슬라이드 외]
- Gaussian Process를 이용한다. 참고서로 『Gaussian Processes for Machine Learning』("수학자들이 쓴 책")을 언급했다.
- 이런 방식을 **Bayesian Optimization**이라 한다.
- 일화: 교수님 랩에서도 시도 중인데, 학생(백주영)이 지난 주말 "교수님 잘 안 되는데요?"라고 메일을 보냈다. "될 때가 있고 안 될 때가 있고 그래."

## 13. 공지: Statistical Inference 동영상 (Part 06 54:12–54:52)

- 이제 ERM을 확률 모형으로 따지면 어떻게 되는지 넘어간다. "크게 다르지 않아요."
- 확률및랜덤변수 강의의 **Statistical Inference 챕터 동영상**을 방금(11시경) 올렸다(아래 공지 섹션 참고).

## 14. MLE 개념 (Part 06 54:52 – Part 07 61:29, 슬라이드 14)

**디지털통신 수강생 손 들기**
- 수강 중이거나 이미 들은 4학년 학생들에게 손을 들게 했다.
- 그 수업에서 MLD(Maximum Likelihood Detection)와 MAP를 배웠을 것이다. 이는 통신만의 용어가 아니라 **통계학 용어**다.

**어원 설명** [슬라이드 외]
- "I likely to love you"는 "너를 사랑하게 될 것만 같아"라는 뉘앙스다. likely to는 "~할 것 같은 느낌적인 느낌"이다.
- -hood는 childhood(어린 시절)처럼 명사를 만든다. **likelihood = 그럴듯함**, 즉 말이 되는, 합리적인(rational) 정도다.
- maximum이 붙으면 "최대로 그럴듯한"이 된다.
- likelihood는 엄밀히 말하면 PDF가 아니다(파라미터의 함수이기 때문).
- 일화: 로봇 같은 표정을 짓던 학생(주호)에게 "앞에 앉아"라고 자리를 옮기게 했다.

**결론**
- 주어진 데이터가 그 파라미터로부터 나왔을 likelihood가 최대가 되는 파라미터를 학습 파라미터로 정한다.

**확률 모델의 파라미터 예시**
- 지수분포: 교수는 "람다분의 1의 exponential 마이너스 람다 x"라고 말했다. 정확한 형태는 $\lambda e^{-\lambda x}$ 또는 $\frac1\lambda e^{-x/\lambda}$이며, 발언에 혼동이 있다.
- Gaussian: $\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$
  - $\mu$(평균)와 $\sigma^2$(분산, degree of spread)가 학습할 파라미터다.

**Negative log-likelihood**
$$\mathcal{L}_x(\boldsymbol\theta)=\mathcal{L}(\boldsymbol\theta):=-\log p(x\mid\boldsymbol\theta)$$
- log는 단조증가 함수다. 따라서 $-\log$를 최소화하는 것은 확률을 최대화하는 것과 같다.
- MLE는 $\boldsymbol\theta$를 바꿔 가며 $\mathcal{L}$을 최소화하는 $\boldsymbol\theta$를 찾는 것이다.

## 15. 지도학습에서의 MLE: Gaussian 노이즈면 Least Squares (Part 07 61:29 – Part 08 71:57, 슬라이드 15)

**칠판 유도**
1. i.i.d. 예제 $(\mathbf{x}_1,y_1),\dots,(\mathbf{x}_N,y_N)$가 있다.
   - i.i.d. = Independently and Identically Distributed.
   - $X=\{\mathbf{x}_n\}$(행렬 또는 집합), $Y=\{y_n\}$.
2. 식을 세운다.
   $$\mathcal{L}(\boldsymbol\theta)=-\log p(Y\mid X,\boldsymbol\theta)=-\log\prod_{n=1}^N p(y_n\mid\mathbf{x}_n,\boldsymbol\theta)=-\sum_{n=1}^N\log p(y_n\mid\mathbf{x}_n,\boldsymbol\theta)$$
   - **곱하는 이유:** $\mathbf{x}_1$은 $y_2, y_3$에 영향을 주지 않고 오직 $y_1$에만 영향을 준다. 통계적으로 독립이면 $p(A,B)=p(A)p(B)$이다.
   - $\log ab=\log a+\log b$이므로 곱이 합이 된다.
3. **가정(모델링)을 추가한다.** $y_n=\mathbf{x}_n^\top\boldsymbol\theta+w,\quad w\sim\mathcal N(0,\sigma^2)$
   - "교수님 왜 그렇게 서포즈하셨어요?" "그냥 그렇게 했어. 그럴 거 같아서. 이유가 없다니까."
4. 상수에 랜덤 변수를 더하면 랜덤 변수다. 평균은 상수만큼 이동하고 분산은 유지된다.
   $$y_n\mid\mathbf{x}_n,\boldsymbol\theta\sim\mathcal N(\mathbf{x}_n^\top\boldsymbol\theta,\sigma^2)$$
5. 대입한다. $\ln$과 $\exp$가 상쇄되고, $1/(2\sigma^2)$는 $n$과 무관하므로 합 밖으로 뺀다. 상수항은 무시한다.
   $$\mathcal{L}(\boldsymbol\theta)=-\sum_n\log\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\Big(-\frac{(y_n-\mathbf{x}_n^\top\boldsymbol\theta)^2}{2\sigma^2}\Big)=\frac N2\log(2\pi\sigma^2)+\frac{1}{2\sigma^2}\sum_n(y_n-\mathbf{x}_n^\top\boldsymbol\theta)^2$$
6. "이거 어디서 많이 본 거 아니에요?"
   - $y_n$은 실제 라벨이고, $\mathbf{x}_n^\top\boldsymbol\theta=\hat y_n$이다. 즉 **average empirical loss**다.
   - **확률 모델에서 NLL을 최소화하는 것은 deterministic 모델의 least-squares 문제와 같은 해를 준다.**

**데이터가 정말 그 식에서 만들어졌는가**
- "교수님, 저렇게 설명이 된다는 건 데이터가 애초에 저 수식으로부터 만들어졌다는 얘긴가요?" "꼭 그렇지 않아."
- ML은 데이터가 먼저 주어지는 **귀납적 학문**이다. "pretty well explained"되면 된다. "영원히 정답은 없다."

**넷플릭스 예시**
- 한 학생(리온)이 영화를 다 보면 좋아할 만한 영화를 추천한다.
- 그 모델이 linear, Transformer, DNN, RNN이어야 할 이유는 없다.
- "쥐만 잘 잡으면 돼, 냥이가." (흑묘백묘)

**"이렇게 할 필요가 있나요?"**
- 다음 시간에 랩을 한다.
- 이번 결과는 노이즈를 Gaussian으로 가정했기 때문에 "우연찮게" 이렇게 나온 것이다.
- Laplace나 exponential처럼 좌우 대칭이 아닌 노이즈를 가정하면 수식이 달라진다. [슬라이드 외]

⚠️ "교수님이 방금 막 발음을 촌스럽게 서포즈 자꾸 강조하잖아요? 이게 지금 강조하고 있는 거야. 여러분, 여기서 가정이 필요하다니까." (66:25–66:32)

## 16. 왜 확률 모델이 대세인가 (Part 08 71:57–73:11) [슬라이드 외]

- 한 학생(준호)에게 "왜 대세일까?"라고 물었고, 학생은 답하지 못했다.
- deterministic 해법은 PDF의 special case(Gaussian)로 정의할 수 있다. 즉 확률 모델이 deterministic metric을 **포함**한다.
- 확률및랜덤변수 수업의 멘트를 인용했다. "상수는 **delta PDF**를 갖는 랜덤 변수로 정의할 수 있다."
  - 확률밀도가 한 점에 모여 있으니 불확실성이 없다.
- 그래서 확률 모델이 기존 deterministic 함수를 포함하는 경우가 많다.

## 17. MAP 예고와 마무리 (Part 08 73:11–73:57)

- MAP는 앞서 말한 regularization, 즉 "모름지기 θ는 이럴 거야"라는 개념과 유사하다. "수요일 날 얘기"한다.
- 슬라이드 16의 식($p(\theta\mid x)\propto p(x\mid\theta)p(\theta)$)은 설명하지 않았다.

---

## 학생 질문과 답변

- **실제로 학생이 먼저 질문한 경우는 없다.** 교수는 "교수님, 왜 그렇게 하셨어요?" 같은 가상 질문을 던지고 스스로 답하는 방식을 여러 번 썼다(7, 10, 15절).
- 교수와 학생 사이의 짧은 대화:
  1. 03:21 확률 수업을 들은 학생과 짧은 문답.
  2. 55:00 디지털통신 수강생 손 들기.
  3. 56:05 주호에게 자리 이동 지시.
  4. 72:07 준호에게 질문했으나 답이 없었음.

## 강조 발언 정리

- ⚠️ 표시는 위 각 절에 있다. **"시험에 나온다"는 발언은 한 번도 없었다.**
- 가장 강하게 강조한 것은 두 가지다.
  - **affine 모델 $f=\boldsymbol\theta^\top\mathbf{x}$를 셋업하는 것** (26:00–26:32)
  - **모델은 suppose라는 점** (66:25)

---

## [별도] 이번 수업의 슬라이드 범위 (추정)

**Lecture01_When_Models_Meet_Data_Part1.pdf, 전체 18장**

| 시간 | 슬라이드 |
|---|---|
| 00:00–06:19 | 7–8 (Deterministic vs Probabilistic, Learning Algorithms) 복습 |
| 06:19–29:14 | 9 (로드맵 2번) → 10 (ERM) |
| 29:14–46:27 | 11 (Loss Function, $R_{\text{true}}$) |
| 46:27–54:12 | 12 (Overfitting & Regularization) |
| 54:12 이후 | 13 (로드맵 3번) |
| 54:52–61:29 | 14 (MLE Concept) |
| 61:29–71:57 | 15 (MLE: Supervised Learning) |
| 73:11 | 16 (MAP)은 제목만 예고 |

- **다루지 않은 것**
  - 슬라이드 16의 본문
  - 슬라이드 17 (Model Fitting)
  - 로드맵 (4) Probabilistic Modeling, (5) DGM, (6) Model Selection
  - **Lecture02 전체**
- 이전 수업(0909)은 슬라이드 8 무렵의 "unseen data 들어와 → test"에서 끝났다.
- 교과서 대응: **MML 8.1, 8.2.1–8.2.3, 8.3.1**이며, 8.3.2 MAP는 도입부만 다뤘다. 슬라이드 15는 MML Example 8.4와 대응한다.

## [별도] 공지사항 (원문 인용)

- "그런 수학을 여기다 쓰면 돼요. 그 수학을 다음 주에 가르쳐주겠다. 리니어 리그레션에서 아주 편한 예측하는 방법 하나를 가르쳐 줄 거예요." (41:03)
- "제가 지난주에 깜빡 잊고 교수님이 그 확률및랜덤변수 수업했던 것 중에 그 스태티스티컬 인퍼런스라는 그 챕터 동영상 … 방금 올렸대요. 아마 11시경 올라갔을 것 같은데, 강의가 한 세 개 정도 … 1시간짜리 강의 세 개니까 한 세 시간만 들으면 오늘 강의 여기까지 해도 되겠는데. 거기서 다 했던 거야." (54:22)
  - `강의노트/추가 강의/Lecture10–12 Statistical Inference Part 1–3`에 해당하는 것으로 보인다.
- "다음 시간에 랩을 할 건데" (71:23)
- "그건 이제 수요일 날 얘기하고요." (73:33, MAP)
- "이제 뭐 숙제도 좀 내주고 이그잼플도 좀 풀어보고 이제 리그레션 문제로 가고 조금 구체화될 거예요. … 다음 주부터 조금 디테일하게 들어갈 테니까." (73:41–73:54)
- "크로스 밸리데이션이라고 하는데 … 좀 이따 설명할게요" (05:47) → 이번 수업에서는 **다루지 않았다.**
- 퀴즈, 시험 범위, 교재 연습문제에 대한 구체적인 언급은 **없었다.**

## [별도] 전제지식으로 언급된 수학 개념과 MML 대응

| 개념 (수업 중 언급) | MML 챕터 |
|---|---|
| 벡터/행렬 표기 관습, 전치, 내적, 행렬 패킹, $X\boldsymbol\theta$, 데이터 augmentation | Ch.2 Linear Algebra |
| 유클리디안 norm, 1-/2-/p-norm, 원점까지의 거리, 거리 기반 loss | Ch.3 Analytic Geometry (3.1–3.2) |
| least squares, pseudo-inverse (다음 주 예고) | Ch.3.8 Projections, Ch.4 Matrix Decompositions (SVD) → Ch.9 |
| 최적화, 제약조건 하 최적화, convex optimization, L1의 sparsity | Ch.7 Continuous Optimization |
| $\theta$에 대한 최소화 (gradient는 다음 주) | Ch.5 Vector Calculus |
| PDF, Gaussian·지수분포, 평균·분산, i.i.d., 독립 $p(A,B)=p(A)p(B)$, 조건부 PDF, 상수+RV의 분포, delta PDF, Bayes 정리(MAP 예고) | Ch.6 Probability and Distributions |
| log의 단조성, $\log ab=\log a+\log b$ | 기초 해석 (Ch.5/7에서 활용) |
| PCA, feature extraction (바둑 예시) | Ch.10 (범위 밖) |
| Gaussian Process, Bayesian Optimization | 교재 범위 밖 |

## [별도] 교과서, 연습문제, 다른 강좌와 문헌 언급

- **MML 교과서, 특정 챕터, 연습문제를 직접 언급한 적은 없다.**
- 언급된 과목과 문헌:
  - 인공지능수학 (convex optimization, least squares, linear algebra, PCA)
  - 확률및랜덤변수 (Statistical Inference 동영상, delta PDF)
  - 디지털통신 (MLD, MAP)
  - 최적화 수업 (L1의 sparsity를 자세히 배우는 곳)
  - 『Gaussian Processes for Machine Learning』
  - 성경 "해 아래 새 것이 없다"(전도서)

## STT 보정 메모

- 표기 정규화: 서포즈 → suppose, 어쑴 → assume, 엠피리컬 → empirical, 어파인 → affine, 라이클리후드 → likelihood, 레귤러라이제이션 → regularization, 스파스 → sparse, 슈도 인버스 → pseudo-inverse, 리스트 스퀘어 → least squares.
- **확인이 필요한 발언**
  - "LLaMA 30만 개": 교수의 말실수로 보인다.
  - 지수분포 PDF: 발음된 식에 혼동이 있다.
  - activation 기호 "델타/에타": $\sigma$일 가능성이 높다.
  - 13:57의 D×N 행렬 설명과 슬라이드의 $N\times D$가 다르다. 교수가 30:08에 전치를 언급하며 정정했다.
  - 학생 이름 주호/준호, 리안/리온은 STT 표기가 일관되지 않는다.