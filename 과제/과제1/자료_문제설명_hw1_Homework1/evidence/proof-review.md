# 독립 계산·논증 검토（2026-10-11）

검토자: Codex. 숫자 사례만으로 일반식을 승인하지 않았다.

- P1–P12: 전치 원소 정의·두 번 전치, 내적/노름과 직교 정의, 행렬곱 순서, 행렬식 첫 행 전개의 +−+ 및 Sarrus의 여섯 항, 양쪽 역행렬 곱, 비자명 관계와 좌표 재구성, Gram 차원, 특징행렬 행 방향, 편미분 열 규약, 야코비안 출력×입력 규약 확인. P10/11은 원 함수의 방향별 일차항으로도 확인했다.
- P13: 공분산의 고윳값 3,1은 양수다. 평균을 뺀 이차형식과 전개식을 상징적으로 비교했다. d차원 정상 가우시안의 정규화 공식에 d=2, det=3을 넣었다.
- P14: 완전제곱을 원식으로 되돌려 확인하고 정규화·1차·2차 중심 모멘트를 직접 적분했다. SymPy 원식 적분은 erf+erfc 조합을 남겼으므로 원식과 동일함을 확인한 중심 형태로 적분했다.
- P15: 알려진 양의 분산, 고정 입력, 독립 잡음이므로 각 관측의 조건부 밀도를 곱할 수 있다. 상수 N개 곱과 지수의 합을 일반 N으로 전개했다. 우도는 theta에 대한 밀도라는 주장이 아니다.
- P16: 공분산 행렬식은 (sigma²)^N, 역은 I/sigma²다. 음의 로그는 N/2 log(2πsigma²)+SSE/(2sigma²). theta에 무관한 상수와 양의 배율만 다르므로 임의의 두 theta의 목적함수 순서가 보존된다. 알려진 분산이라는 가정이 필수다.
- P17(a): J=yᵀy−2thetaᵀPhiᵀy+thetaᵀPhiᵀPhi theta. PhiᵀPhi는 대칭이므로 열 gradient는 −2Phiᵀy+2PhiᵀPhi theta다. full column rank이면 v≠0에서 Phi v≠0이므로 vᵀPhiᵀPhi v>0. 정규방정식 해 theta* 주변 J(theta*+v)−J(theta*)=||Phi v||²는 모든 v에서 성립한다. 교차항은 정규방정식 때문에 소거된다. 따라서 유일 전역 최소이자 ML이다.
- P18: Bayes 규칙의 evidence 및 알려진 분산·사전분산의 정규화 상수는 theta에 무관하다. NLL+negative log prior의 gradient를 0으로 두고 sigma²를 곱하면 Htheta=Phiᵀy, H=PhiᵀPhi+(sigma²/b²)I다. vᵀHv=||Phi v||²+lambda||v||²>0이므로 rank와 무관하게 유일 해다. 잔차항 계수를 1로 만든 RLS의 lambda는 sigma²/b²다. Lecture03 p26의 prior 단독 계수 1/(2b²)와는 목적함수 스케일을 구별한다. 과제에서 요청한 정규화가 우선하며 MML 9.2.3–9.2.4와 일치한다.
- P19: 이 과제는 절편을 포함한 모든 계수에 prior 적용. b² 감소는 lambda 증가; 이 대각행렬 사례의 양의 각 계수는 분모 증가로 0에 가까워진다.
- P20: 무규제 목적은 합 s만 식별한다. 규제 목적은 J=15/2(s−2)²+5/2 d²+15. 모든 실수 계수에서 완전제곱 항은 비음수이고 s=2,d=0만 0으로 만든다. 수치 샘플 최적화가 아닌 전역 증명이다.
- P21: 문제의 분모는 N=4다. raw second moment−mean outer product와 centered outer products가 동일하다.
- P22: y−E[y]=A(x−E[x])로 공분산·cross-covariance 식을 도출. 상수 이동은 공분산에 영향 없음. (b) exponent 행렬은 precision이며 inverse 필요. (c) Cov12=E[x1x2]−E[x1]E[x2]=1. epsilon 독립성으로 mixed terms는 0, 공유 epsilon의 공분산은 Var(epsilon)11ᵀ이지 I가 아니다. 성분별 분산/공분산 계산과 행렬 계산이 일치한다. 비가우시안 (a),(c)도 2차 모멘트만 필요하다.
- P23/24: 음의 로그의 미분과 완전제곱으로 각각 유일 최소 확인. P24 prior 중심 1을 사용하고 거리 비교. 표준 가우시안 상수 2/3개 각각 유지.
- P25: 두 positive definite precision을 더한 Pq는 positive definite. 전개된 exponent의 quadratic·linear coefficients를 비교하면 Sq=Pq⁻¹, muq=Sq(P0mu0+P1mu1). 이는 모든 x에서 성립하는 완전제곱이며 남는 exponent 차이는 5/22. 원 곱 정규화 전 적분은 exp(−5/22)/(2πsqrt(11)); 나눈 결과의 계수는 sqrt(11/6)/(2π). 완성 밀도는 det Sq=6/11인 정상 가우시안이므로 적분 1이다.

## 원문 대조

과제 원 PDF 9페이지 전체를 래스터화하고 source-pages.png로 보았다. 문항별 페이지: P1–2 p1, P3–5 p2, P6–10 p3, P11–13 p4, P14–16 p5, P17–19 p6, P20–21 p7, P22 p8, P23–25 p9. 수치, 부호, 소문항 50개, 조건(열벡터, 열 gradient, variance, 절편 규제, 공유 epsilon, 분모4)을 카드 source.json과 대조해 일치 확인. 원 PDF는 도표 없이 수식·행렬로 구성된다.

MML PDF 페이지 46–47(선형결합·독립),106–107(행렬식),154/156(연쇄법칙·Jacobian),200–207(모멘트·Gaussian),297–301/306–308(ML/MAP)을 확인했다. Lecture03 전체, 특히 p17–18 특징/ML, p22–26 MAP; Lecture04 p6–13 Gaussian·moments·Gaussian product도 확인했다. 교재/교안의 행 gradient와 달리 과제의 명시적 열 gradient 규약을 따랐다. 기존 1007 정리노트의 s0-features, s1-affine, s3-product-matrix도 참고했다. 설명 HTML에는 별도의 개념링크를 넣지 않았다.
