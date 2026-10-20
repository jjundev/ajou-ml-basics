# 본문–요약 수동 감사 0916

범위: 이 날짜의 정리노트·복습문제·문제설명 실제 본문과 실제 요약. 외부 원자료 전체의 독립 학술 검증은 아니다. 교수 일화·비유·반복은 원리/조건과 다른 새 핵심이 없으면 생략한다. 질문·풀이·정답 본문은 이번 작업에서 보존했다.

| 자료·토픽 | 구분 | 실제 본문 주장 | 대응하는 현재 요약 문장 / 생략 이유 | 보완 전 | 판정 |
|---|---|---|---|---|---|
| 문제설명_0916_MAP_and_Generative_Models.html#p1 | 일반 | 고정 SPD Σ하 θ의 Gaussian -log prior는 quadratic/2+상수; MAP는 NLL+quadratic 최소화. | posterior의 분모 evidence는 θ와 무관해요. 따라서 NLL에 prior 이차항을 더하는 minimizer가 MAP예요. | 기존 반영 | pass |
| 문제설명_0916_MAP_and_Generative_Models.html#p1 | 주의 | 고정 SPD Σ하 θ의 Gaussian -log prior는 quadratic/2+상수; MAP는 NLL+quadratic 최소화. | $\Sigma$는 고정된 양의 정부호 $D\times D$ 공분산이고 $\theta\in\mathbb R^D$만 최적화해요. $\Sigma$나 분산도 최적화하면 관련 로그 상수항을 버릴 수 없어요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0916_MAP_and_Generative_Models.html#p2 | 일반 | p(x)는 같은 열의 joint를 y에 대해 합함; [.16,.17,.11,.22,.34], 전체합1. | 독립 분수 계산으로 [16,17,11,22,34]/100을 얻고 합이1이에요. | 기존 반영 | pass |
| 문제설명_0916_MAP_and_Generative_Models.html#p2 | 주의 | p(x)는 같은 열의 joint를 y에 대해 합함; [.16,.17,.11,.22,.34], 전체합1. | $x$가 열, $y$가 행이므로 $p(x)$는 같은 열을 더해요. 열마다 별도로 1로 맞추는 것이 아니라 주변확률 다섯 개의 합이 1이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0916_MAP_and_Generative_Models.html#p3 | 일반 | p(y)는 행 합 [.26,.47,.27], 전체합1. | 독립 분수 계산으로 [26,47,27]/100이고 세 행 합이1이에요. | 기존 반영 | pass |
| 문제설명_0916_MAP_and_Generative_Models.html#p3 | 주의 | p(y)는 행 합 [.26,.47,.27], 전체합1. | $p(y)$는 $x$를 없애는 행 합이에요. 열 합은 $p(x)$라는 다른 질문에 답해요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0916_MAP_and_Generative_Models.html#p4 | 일반 | p(x\|y1)는 y1행을 양수.26으로 나눔, [1,2,3,10,10]/26. | 분자는 [1,2,3,10,10]/100, 공통 분모26/100이라 [1,2,3,10,10]/26이에요. | 기존 반영 | pass |
| 문제설명_0916_MAP_and_Generative_Models.html#p4 | 주의 | p(x\|y1)는 y1행을 양수.26으로 나눔, [1,2,3,10,10]/26. | 분모는 조건으로 주어진 $p(y_1)=0.26>0$이에요. $p(x)$로 나누면 조건 방향이 달라져요. | unresolved → 보완 후 다시 읽음 | pass |
| 문제설명_0916_MAP_and_Generative_Models.html#p5 | 일반 | p(y\|x3)는 세번째 열을 .11로 정규화, [3,5,3]/11. | 세 확률은 [3,5,3]/11로 합1이에요. | 기존 반영 | pass |
| 문제설명_0916_MAP_and_Generative_Models.html#p6 | 일반 | iid Bernoulli k성공의 likelihood와 proper Beta prior 지수 합→Beta(α+k,β+N−k); 평균과 mode 차이. | 지수는 α+k−1과 β+N−k−1이라 Beta(α+k,β+N−k)의 정규화 적분이 존재해요. | 기존 반영 | pass |
| 문제설명_0916_MAP_and_Generative_Models.html#p6 | 주의 | iid Bernoulli k성공의 likelihood와 proper Beta prior 지수 합→Beta(α+k,β+N−k); 평균과 mode 차이. | $\alpha,\beta>0$, $0<\mu<1$에서 posterior는 Beta$(\alpha+k,\beta+N-k)$예요. 성공확률 $\mu$와 횟수 $k$를 구별하고 posterior 평균과 MAP도 구별해요. | unresolved → 보완 후 다시 읽음 | pass |
| 복습문제_0916_MAP_and_Generative_Models.html#p1 | 일반 | 고정 SPD Σ하 θ의 Gaussian -log prior는 quadratic/2+상수; MAP는 NLL+quadratic 최소화. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0916_MAP_and_Generative_Models.html#p2 | 일반 | p(x)는 같은 열의 joint를 y에 대해 합함; [.16,.17,.11,.22,.34], 전체합1. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0916_MAP_and_Generative_Models.html#p3 | 일반 | p(y)는 행 합 [.26,.47,.27], 전체합1. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0916_MAP_and_Generative_Models.html#p4 | 일반 | p(x\|y1)는 y1행을 양수.26으로 나눔, [1,2,3,10,10]/26. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0916_MAP_and_Generative_Models.html#p5 | 일반 | p(y\|x3)는 세번째 열을 .11로 정규화, [3,5,3]/11. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 복습문제_0916_MAP_and_Generative_Models.html#p6 | 일반 | iid Bernoulli k성공의 likelihood와 proper Beta prior 지수 합→Beta(α+k,β+N−k); 평균과 mode 차이. | N/A: 원래 .sum 없는 문제 카드다. 힌트·풀이·정답 구조를 그대로 보존하고 새 요약을 만들지 않았다. | 해당 없음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s0-learning-map | 일반 | ML은 고정 미지 계수, MAP/FB는 prior로 랜덤 계수 모형; MAP은 점 선택, FB는 전체 유지. | MAP은 확률변수로 모델링한 파라미터에서 한 점을 고르고, FB는 가능한 값들의 불확실성을 계속 반영해요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s0-learning-map | 조건·구분 | ML은 고정 미지 계수, MAP/FB는 prior로 랜덤 계수 모형; MAP은 점 선택, FB는 전체 유지. | ML은 고정된 미지의 파라미터에서 우도를, MAP은 사전분포를 부여한 파라미터에서 사후밀도를 최대화해요. MAP은 최고점만 찾으면 되고 사후분포 전체 계산이 먼저 필요한 것은 아니에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s0-nll | 일반 | 최대 우도와 최소 NLL이 같은 계수; log로 exp 해제, 작은 값 구별, PDF 높이와 적분을 구분. | 가장 그럴듯한 $\theta$를 찾는 문제를 $-\log$로 최소화 문제로 바꿔요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s0-nll | 조건·구분 | 최대 우도와 최소 NLL이 같은 계수; log로 exp 해제, 작은 값 구별, PDF 높이와 적분을 구분. | 로그는 가우시안의 $\exp$를 풀고 작은 값의 차이를 드러내요. PDF 높이는 1보다 클 수 있으며 전체 적분이 1이라는 조건과 구별해요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s0-iid | 일반 | 독립/동일분포 가정을 분리해 곱 및 공유 계수로 만들고 log 곱법칙으로 합을 얻음. | i.i.d. 가정이 있어야 곱이 한 $\theta$의 로그 합으로 바뀌어요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s0-iid | 조건·구분 | 독립/동일분포 가정을 분리해 곱 및 공유 계수로 만들고 log 곱법칙으로 합을 얻음. | 독립이면 예제별 우도를 곱으로 나누고, 동일 분포이면 공통 $\theta$를 써요. 곱을 합으로 바꾸는 단계는 $\log(ab)=\log a+\log b$예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s0-mle-ls | 일반 | 공통 Gaussian 잡음과 iid, 분산을 계수와 무관하게 둔 NLL에서 제곱합만 남김. | 노이즈가 가우시안이면 MLE는 least squares와 같은 답을 줘요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s0-mle-ls | 조건·구분 | 공통 Gaussian 잡음과 iid, 분산을 계수와 무관하게 둔 NLL에서 제곱합만 남김. | 여기서는 i.i.d.와 공통 가우시안 잡음을 가정하고, $\sigma^2$를 $\theta$와 무관한 값으로 두어요. NLL에서 $\theta$와 무관한 상수항을 제외하고 남은 양의 배율의 오차 제곱합을 최소화하므로 해가 같아요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s1-posterior | 일반 | 데이터 x를 조건으로 θ를 추론; Bayes 분모는 θ와 무관, max/argmax 구분. | 데이터 $x$가 주어졌을 때 $\theta$의 확률, 곧 posterior를 베이즈 룰로 구해요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s1-posterior | 조건·구분 | 데이터 x를 조건으로 θ를 추론; Bayes 분모는 θ와 무관, max/argmax 구분. | 분모 $P(x)$는 $\theta$와 무관해 최고점 선택에서 제외해요. $\max$는 최고 밀도값이고 $\arg\max$는 그 값을 만드는 파라미터예요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s1-map | 일반 | posterior 곱에 -log를 취하면 NLL + negative log prior; uniform은 상수라 ML과 같음. | MAP는 음의 로그우도에 음의 로그 prior를 더해 최소화해요. prior가 uniform이면 MAP = MLE예요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s1-map | 조건·구분 | posterior 곱에 -log를 취하면 NLL + negative log prior; uniform은 상수라 ML과 같음. | 정확한 최소화 항은 NLL에 음의 로그 prior $-\log P(\theta)$를 더한 것이에요. 확률로 쓰면 likelihood와 prior의 곱이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s1-map-reg | 일반 | 작은 θ를 선호하는 정규화; b²I Gaussian prior의 공분산/독립 조건 및 λ 매핑은 수업 밖 유도. | $\lambda\\|\theta\\|^2$ 정규화 항은 "$\theta$는 작을수록 좋다"는 prior를 식에 넣은 것이에요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s1-map-reg | 조건·구분 | 작은 θ를 선호하는 정규화; b²I Gaussian prior의 공분산/독립 조건 및 λ 매핑은 수업 밖 유도. | 보충(MML Example 8.6): 가우시안 likelihood와 $\theta\sim\mathcal N(0,b^2I)$, $b^2>0$인 가우시안 prior에서 $\lambda=\sigma^2/(Nb^2)$예요. 벡터 성분은 분산 $b^2$, 교차 공분산 0이며 공동 가우시안이라 독립이에요. 이 유도는 수업에서 미룬 부분이고, prior 폭이 좁을수록 벌점이 강해져요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s1-map-reg | 보충 | b²I의 대각/교차 공분산과 공동 Gaussian에서 독립이라는 조건을 모두 보존. | 벡터 성분은 분산 $b^2$, 교차 공분산 0이며 공동 가우시안이라 독립이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s1-fitting | 일반 | 모델 클래스 안의 최선도 진짜 규칙과 멀 수 있음; 과적합/과소적합 증상과 새 데이터 평가 구분. | 모델 클래스 안의 최적 $M_{\theta^*}$가 진짜 모델 $M^*$에 가까워야 하고, 모델 크기는 데이터에 알맞아야 해요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s1-fitting | 조건·구분 | 모델 클래스 안의 최선도 진짜 규칙과 멀 수 있음; 과적합/과소적합 증상과 새 데이터 평가 구분. | 과적합은 훈련에는 잘 맞고 새 데이터에는 어긋나며, 과소적합은 훈련 데이터도 잘 설명하지 못해요. 적정적합은 양쪽을 잘 설명해야 하므로 학습 데이터로 테스트하지 않아요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s1-fitting | 강조 | 훈련 데이터로 테스트하면 성능 평가가 왜곡된다는 교수 주의. | 학습 데이터로 테스트하지 않아요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s2-generative | 일반 | 가정한 생성과정에서 입력·계수 고정시 평균만 상수 이동, 잡음 분산 보존. | 데이터가 "이렇게 만들어졌을 거야" 하고 가정한 과정이 generative process예요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s2-generative | 조건·구분 | 가정한 생성과정에서 입력·계수 고정시 평균만 상수 이동, 잡음 분산 보존. | 이 유도는 입력과 미지의 계수를 고정해 $c_n=x_n^\top\theta$를 상수로 보아요. 가우시안 잡음에 상수를 더하면 평균만 $c_n$으로 옮겨지고 분산 $\sigma^2$는 유지돼요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s2-joint | 일반 | joint는 변수간 관계 포함, 주변화로 marginal을 얻지만 marginal 둘로 joint 복원 불가. | joint 분포가 정보를 가장 많이 담고, marginal은 거기서 한 변수만 남긴 거예요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s2-joint | 조건·구분 | joint는 변수간 관계 포함, 주변화로 marginal을 얻지만 marginal 둘로 joint 복원 불가. | joint는 변수 사이 관계까지 담아요. 관심 없는 변수를 적분해 marginal을 얻을 수 있지만 marginal 둘만으로 원래 joint를 복원할 수는 없어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s2-posterior | 일반 | prior×likelihood가 joint, θ 적분이 evidence, 이를 나눠 posterior; 데이터가 주어졌는지 먼저 구분. | prior와 likelihood를 곱해 joint를 만들고, joint 하나로 marginal likelihood와 posterior를 모두 구해요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s3-three-ways | 일반 | ML likelihood, MAP posterior의 점 최적화와 FB의 전체 posterior 적분 예측을 구분. | ML과 MAP는 $\theta$ 하나로 단답을 내고, Fully Bayesian은 posterior 전체로 예측해요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s3-three-ways | 조건·구분 | ML likelihood, MAP posterior의 점 최적화와 FB의 전체 posterior 적분 예측을 구분. | ML은 likelihood 최적화, MAP은 prior를 반영한 posterior 최적화이고 둘 다 점 추정이에요. FB의 핵심 계산은 posterior로 가중한 적분이며, 표시한 예측식의 조건부 독립 가정은 뒤 보충에서 풀어요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s3-coin | 일반 | 2/10 앞면의 ML 0.2, Beta prior의 MAP; uniform 예외와 미지정 수업 예시/보충 a=4를 구분. | ML은 데이터만 믿어 0.2를 내고, MAP는 "반반"이라는 prior를 섞어 그 사이 값을 내요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s3-coin | 조건·구분 | 2/10 앞면의 ML 0.2, Beta prior의 MAP; uniform 예외와 미지정 수업 예시/보충 a=4를 구분. | 보충의 대칭 Beta$(a,a)$ prior 계산은 수업에서 유도하지 않았어요. $a=1$이면 MAP도 0.2이고 $a=4$이면 $5/16=0.3125$예요. 수업의 “0.3 정도”는 $a=4$를 지정한 결과가 아니에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s3-coin | 보충 | a=4는 보충 선택이며 수업이 0.3이라는 값으로 a를 정한 것은 아님. | 수업의 “0.3 정도”는 $a=4$를 지정한 결과가 아니에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s3-predictive | 일반 | 주변화+곱규칙 뒤 θ에서 X 영향 사라진다는 조건부 독립 가정; posterior 평균 예측은 MAP와 다름. | Fully Bayesian 예측은 posterior로 가중평균한 predictive distribution이고, 조건부 독립 덕분에 식이 간단해져요. | 기존 반영 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s3-predictive | 조건·구분 | 주변화+곱규칙 뒤 θ에서 X 영향 사라진다는 조건부 독립 가정; posterior 평균 예측은 MAP와 다름. | $P(A\mid\theta,X)=P(A\mid\theta)$는 조건부 독립 가정이에요. 보충의 Beta posterior 예에서 $a=4$이면 다음 앞면 확률은 $1/3$으로 MAP $5/16$과 다르고, $a=1$에서도 예측 $1/4$은 ML·MAP $1/5$과 달라요. 이 상세 전개는 수업 밖 보충이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s3-predictive | 보충 | 조건부 독립은 가정이고, uniform prior에서도 predictive .25와 ML/MAP .2는 다름. | $a=1$에서도 예측 $1/4$은 ML·MAP $1/5$과 달라요. 이 상세 전개는 수업 밖 보충이에요. | unresolved → 보완 후 다시 읽음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s4-cheatsheet | 일반 | 앞 학습 토픽들을 연결하는 기존 치트시트 표. | N/A: 이 화면 자체가 요약·링크 표다. 별도 .sum을 새로 만들지 않았다. | 해당 없음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s4-next | 일반 | 아직 배우지 않은 다음 시간 범위를 명시한 예고. | N/A: 예고 화면이며 현재 학습 범위 요약으로 전환하지 않았다. | 해당 없음 | pass |
| 정리노트_0916_MAP_and_Generative_Models.html#s4-links | 일반 | 기존 학습·문제·PDF 자료의 링크 모음. | N/A: 링크 화면으로 기존 구조를 유지했다. | 해당 없음 | pass |

## Current regeneration source classification correction (Task6b)

Active content inputs are the published `fragments/pN.html`, copied to RUN `explanations/pN.html` by `mpe_rerender.py` lines 188–206 and read by `mpe_cli.load_fragments`. The files under `evidence/`, including `author.py`, are historical authoring/review evidence; the current build copies them as artifacts and does not execute them. Their six Task6a summary edits were restored only after exact current bytes matched the controller Task6b baseline, retaining all current fragment summaries. No historical author/review script is a renewed approval. Current browser and approval binding remain pending.


## Task6c visible-summary equation line breaks

- `정리노트_0916_MAP_and_Generative_Models.html#s1-map`: actual summary display equations now `\begin{aligned}\theta_{\text{MAP}}&=\arg\min_\theta\bigl[\\&-\log P(x\mid\theta)\\&-\log P(\theta)\bigr]\end{aligned}`. Same-body operators/values/order and conditions were directly reread; no learning-body change.
