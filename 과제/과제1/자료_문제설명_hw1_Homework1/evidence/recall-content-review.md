# 개념·공식 추가 내용 및 독립 논증 검토 — 2026-10-12

검토자: Codex. 과제 개정 원 PDF의 9페이지를 추출·래스터화해 원문/조건을 대조하고, source.json 25문항 50소문항과 각 신규 recall 조각을 읽었다. 기존 풀이 여섯 구역은 별도 프로그램으로 보존을 대조한다. 아래의 개념/기호·가정 판단과 독립 계산을 함께 사용한다. 구조 검사만으로 수학 정확성을 승인하지 않는다.

읽은 자료의 경로/해시는 references.json, 추출 내용은 같은 evidence 디렉터리의 *-excerpts.txt에 있다. 원문 페이지는 PDF의 실제 1-based 페이지 번호이다. 자료의 행 gradient 표기와 달리 원 과제의 열 gradient 지시를 따른다. Lecture03 p26의 prior 자체 계수를 목적함수의 lambda와 그대로 동일시하지 않고, p23–24 및 MML p307의 전체 목적함수를 기준으로 양의 스케일을 맞췄다.

| 문항/원문 PDF 페이지 | 단서와 개념·기호 검토 | 적용 조건/소문항 커버리지 | 독립 판단·참고 자료 |
|---|---|---|---|
| P1 / 1 | 전치, i/j와 m/n, 위치 교환 | a/b/c, 직사각형·열벡터 허용 | 원소 정의 및 두 번 전치; 원 PDF |
| P2 / 1 | 내적, 노름, d·좌표, 직교 | a/d 내적, b/c 제곱근; 각도는 비영벡터 | 0 내적, 길이 3와 sqrt5; 원 PDF |
| P3 / 2 | 행×열의 내적, i/j/k 및 안쪽 차원 | main, 두 순서 모두 정의되나 교환 일반 불가 | 두 곱 독립 계산 |
| P4 / 2 | 행렬식, 2×2 a/b/c/d, minor | a/b ad−bc, c 대각곱, d 두 방법 | MML PDF p106–107, det 10/6/−6/0 |
| P5 / 2 | 역행렬, 항등행렬, 블록 B/s | a/b 2×2, c 블록; 블록별 가역 조건 | MML p106, 양쪽 곱 검산 |
| P6 / 3 | 선형 독립, 계수 c_i, 비자명해 | main, 계수 중 하나라도 0 아님 | MML p46–47, (−2,1,1) 관계 |
| P7 / 3 | 선형결합, X 열 배열, 계수 c | main, span은 존재, 가역은 유일성 | MML p46, Xc=y 대입/det5 |
| P8 / 3 | Gram, 열 a_i, 계수 v | main, A는 3×2, Gram는 2×2; full column rank | vᵀAᵀAv=||Av||²의 모든 v에 대한 항등식 |
| P9 / 3 | 특징 행렬, n/j/계수 theta | main, 관측 행·특징 열, 파라미터에 선형 | 원 PDF; Lecture03 p17–18, 예측(2,1,4) |
| P10 / 3 | gradient와 편미분, r와 연쇄법칙 | a/b 교차항, c chain rule; 열 gradient | MML p154, 심볼 미분과 일차 방향 항 비교 |
| P11 / 4 | Jacobian, 출력 f_i/입력 x_j | a 2×2, b 3×2; u,v 열 순서 | MML p156, 출력별 편미분 |
| P12 / 4 | 이차형식 Q, 고정 b, 정류점 | a 일반 Q+Qᵀ, b 대칭 Q/최소 조건 구분 | 일반 비대칭 2×2 gradient 항등식; Q 양의 정부호 |
| P13 / 4 | Gaussian d/mu/Sigma/precision | main, d=2; SPD, 상관 있으므로 독립 곱 금지 | Lecture04 p8, det3·정규화·전개 검산 |
| P14 / 5 | 완전제곱 a/b/d, 평균/분산 | main, a>0; 남는 상수 포함 | 일반 이차식 항등식, 직접 적분 mass1/mean1/var1/4 |
| P15 / 5 | likelihood, residual r_n, N/sigma² | main, 독립 고정 입력·알려진 공통 분산 | Gaussian 밀도 N개 곱: 계수 곱·지수 합 |
| P16 / 5 | 로그와 SSE/잔차 벡터, Phi/theta | main, 알려진 양의 분산; 전체 NLL 유지 | 로그 단조성+상수/양의 배율의 순서 보존 |
| P17 / 6 | gradient=0, K/N, normal equations | a full rank가 가역과 유일 최소 보장; b 절편/예측/S | Lecture03 p17–18; 모든 v에서 J(theta*+v)−J(theta*)=||Phi v||² |
| P18 / 6 | Bayes, prior b², ridge lambda/I_K | main, sigma²/b²>0, 절편 포함 모든 계수 | MML p307–308, Lecture03 p23–25; 양의 스케일 및 SPD 증명 |
| P19 / 6 | G/h, prior 분산과 lambda | a ML/MAP, b 분산 감소; 대각 사례로 단조 비교 제한 | ML/MAP exact; 비대각 일반화 안 함 |
| P20 / 7 | 중복 열·null space, s/d, ridge | a 특이, b 예측 동치, c lambda5/전역 최소 | J=15/2(s−2)²+5/2d²+15, 비음수 완전제곱 |
| P21 / 7 | 평균·편차 외적 d_n/N | a 평균, b 분모4; N−1 금지 | Lecture04 p6–7; 중심/원시 2차 모멘트식 일치 |
| P22 / 8 | A/c/mu/Sigma/C_xy/P/u | a finite moments, b precision inverse, c shared noise | Lecture04 p7–8; 독립 noise 혼합항0, 추가 covariance=Var(epsilon)uuᵀ |
| P23 / 9 | 잔차/스칼라 theta/ML/MAP | a 정규화N2, b sum x²>0, c prior0/예측, 절편 추가 금지 | Gaussian 곱+미분, ML8/5, MAP4/3 |
| P24 / 9 | 공통 평균/정밀도, m0/b²/sigma² | a 상수N3, b 표본평균, c prior 중심1/거리 | 일반 nonzero prior MAP의 미분=0, ML3/MAP5/2 |
| P25 / 9 | 밀도 곱/P_i/mu_q/Sigma_q/d | main, SPD; 같은 변수 함수 곱, 독립성 요구 안 함 | Lecture04 p10–11; 모든 x에서 지수차5/22, det6/11·정규화 |

## 일반식의 논증

- Gram: 임의 v에 대해 vᵀAᵀAv=(Av)ᵀ(Av). 열이 독립이면 Av=0의 해는 v=0뿐이므로 양의 정부호. 종속이면 비영 영공간 벡터가 있어 역행렬이 없음. 숫자 하나로 일반식의 증명을 대체하지 않았다.
- 정규방정식: 제곱을 전개한 gradient는 2Phiᵀ(Phi theta−y). 해 theta*에서 교차항이 소거되므로 J(theta*+v)−J(theta*)=||Phi v||²≥0. full column rank이면 v≠0에서 >0.
- 릿지: H=PhiᵀPhi+lambda I이면 vᵀHv=||Phi v||²+lambda||v||². lambda>0에서 모든 비영 v에 대해 양수. 전체 negative log posterior에 2sigma²를 곱해 lambda=sigma²/b²를 얻었다. 모든 계수를 규제한다는 과제 조건을 유지했다.
- 아핀 covariance: y−mu_y=A(x−mu_x)로부터 covariance와 C_xy를 유도했다. 공유 잡음은 epsilon u이며 독립성이 mixed expectation을 0으로 만들고 E[epsilon²]uuᵀ만 남긴다. u=(1,1)이므로 off-diagonal도 증가. 정밀도 이차식의 cross term은 P12+P21이다.
- Gaussian 곱: 두 지수 전개의 quadratic coefficient는 P0+P1, linear coefficient는 P0mu0+P1mu1. SPD 합은 SPD. 이를 중심 이차식으로 모으면 mu_q와 Sigma_q를 얻는다. 남은 상수로 비례식만 얻으며, 최종 q는 SPD covariance의 Gaussian 정규화 계수를 붙여 적분1을 보장한다.

## 첫 줄과의 역할 분리

recall은 연산 선택과 정의·기호·가정, start는 실제 값·배치·미분 첫 식을 담당한다. 첫 식에 필요한 짧은 공식은 두 구역에 재등장할 수 있지만 긴 설명은 복제하지 않았다. P22 start는 아핀 배치, recall은 precision/shared noise의 선택 기준까지 다룬다. 각 summary는 선택한 핵심만 남기고 본문을 전부 복제하지 않았다.
