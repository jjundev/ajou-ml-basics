# 원자료 출처 대조 기록

검토자: /root/round02_blind_math. 문제만 보고 작성한 blind-review.json을 먼저 보존한 후, 카드·해설의 출처 주장을 아래 원자료와 대조했다. 원본 PDF, 카드, 해설은 수정하지 않았다.

## 실제 확인 범위

- 교재 텍스트: PDF 46,47,153,155,156,194,196,198,200,207,208,298,299,300,302,307,308,309,312,314,315,319,320쪽(23쪽).
- 과제 텍스트: PDF 3~9쪽(7쪽).
- Lecture04 텍스트: PDF 14,17,20,24쪽(4쪽).
- 실제 렌더링·view_image 확인: 교재 PDF 46,153,156,198,200,207,208,300,302,307,308,312,314,315,319,320쪽(16쪽), 과제 PDF 3~9쪽(7쪽), Lecture04 PDF 14,17,20,24쪽(4쪽): 총 27쪽.
- 위 34쪽은 PyMuPDF로 텍스트 추출하고 1.5배 해상도 PNG로 렌더링했다. 시각 검토한 27쪽은 contact-1.png~contact-7.png의 2×2 전체 페이지 묶음을 view_image로 실제 열어 확인했다. PDF에 인쇄된 쪽수와 PDF 물리 쪽수를 혼동하지 않았다. 교재는 예를 들어 PDF300=인쇄294쪽이다.
- 증빙은 source-evidence/{mml,hw,l04}-text.txt, 개별 페이지 PNG, contact-1.png~contact-7.png에 있다. 텍스트만 읽은 추가 교재 47,155,194,196,298,299,309쪽을 시각 검토했다고 주장하지 않는다.

## 문항별 출처와 결과

| 문항 | 실제 대조한 근거 | 결과 |
|---|---|---|
| p1 | HW PDF3 P6은 독립성, P7은 선형결합; 교재 PDF46 정의2.11/2.12, PDF47 종속관계의 의미 | 3차원 원문을 2차원 작은 수로 변형한 설명이 정확하다. 제시 수치는 원문 복사가 아니며 새 변형이라고 공개한다. |
| p2 | HW PDF3 P10은 열 gradient를 명시; PDF4 P11은 출력×입력 Jacobian, P12는 이차식 성분미분·최적화. 교재 PDF153 행 gradient 설명, PDF155/156 Jacobian과 m×n 배치 | 새 행 관례 변형이라는 조건이 정확하다. 과제 원문의 열 관례와 구별하며 원자료를 바꾸지 않는다. |
| p3 | HW PDF5 P14 완전제곱·정규화, PDF9 P25 Gaussian 정규화 곱; 교재 PDF207 식6.74~6.77 곱의 평균·분산·scale | 1차원 변형과 상수 Z를 포함한 풀이가 일치한다. PDF208은 Gaussian 혼합의 평균·분산으로 직접적인 곱 공식 페이지가 아니다. 핵심 곱 근거는 PDF207이다. PDF208은 주변 문맥 참조로만 해석해야 한다. |
| p4 | HW PDF3 P9 특징·설계행렬, PDF6 P17 최소제곱/ML, P19 절편 포함 MAP; 교재 PDF300 식9.10~9.12, PDF302 식9.16~9.19, PDF307 식9.28~9.31, PDF308 정규화 | 모든 계수에 prior 적용과 noise/prior 분산1에서 Gram+I 공식이 정확하다. 원문 관측값과 차원을 바꾼 새 변형이다. |
| p5 | HW PDF7 P21 분모4 평균·공분산, PDF8 P22 아핀 변환·교차공분산; 교재 PDF194 기대값, PDF196 정의6.6/6.7, PDF198 분모N 공분산, PDF200 식6.50~6.52 | 확률1/4 분포를 이용한 계산은 Gaussian을 요구하지 않는다. Cov(X,Y)=Σ_X A^T의 방향과 이동항 소거가 원자료와 일치한다. |
| p6 | HW PDF5 P15~16 likelihood 상수/NLL, PDF6 P17 정규방정식; 교재 PDF298 조건부 독립 likelihood, PDF299 로그·ML, PDF300 행 미분과 정규방정식, PDF302 특징행렬 | 고정 입력·모수 조건에서 독립성이 쓰이고, 상수(2π)^(-1)와 NLL상수를 보존한다. 행 미분 1×2를 0으로 놓은 뒤 양변 전치가 명시되어 있다. |
| p7 | HW PDF6 P18 prior penalty 및 λ=σ²/b², PDF9 P24 평균모델 MAP; 교재 PDF307 식9.28, PDF308 식9.32, PDF309 식9.33/9.34 | 새 모형의 prior 평균0과 관측 두 개가 원문과 다른 점을 새 변형으로 공개한다. half-SSE와 SSE 배율을 일관되게 표시하여 MAP4/3, 강한 prior에서2/3을 얻는다. |
| p8 | 교재 PDF312 식9.41~9.45 사후분포, PDF314 식9.57 posterior prediction, PDF315 식9.58/9.59 noiseless moments; Lecture04 PDF14 posterior predictive | θ posterior N(1,1/2), f* 분산2, y* 분산3과 관측잡음1의 구분이 정확하다. posterior를 재유도하지 않고 아핀·독립합 공식을 쓰는 간결한 후반 풀이가 맞다. |
| p9 | 교재 PDF312 식9.42 evidence의 prior 평균, PDF319 식9.64b Gaussian 주변우도; Lecture04 PDF17 prior odds×Bayes factor 및 주변우도 | prior 분산3+noise분산1=4, B01=2, 같은 model prior에서 posterior odds2:1/확률2/3과 일치한다. prior로 적분하는 것과 posterior로 예측하는 것을 구분한다. |
| p10 | Lecture04 PDF20 선투영 계수/행렬, PDF24 ML as projection; 교재 PDF319 식9.66/9.67, PDF320 9.4 일반 feature projection | 3차원 b의 1차원 span으로의 투영이므로 bb^T/(b^Tb)와 scalar계수 계산이 정확하다. 거리분해와 전역 최소3을 항등식으로 증명한다. |

## 원자료 자체에서 구별한 사항

- HW P10은 열 gradient를 요구하지만 이번 새 문항 p2/p6은 명시적으로 행 미분을 요구한다. 이는 원문 해설을 몰래 바꾼 것이 아니라 새 변형이며, 교재 PDF153/156/300/307의 행 관례를 따른다.
- 교재 PDF208은 곱 공식의 직접 근거가 아니다. p3의 근거를 가장 정확히 적으려면 PDF207을 핵심 페이지로 제시하면 된다. 현재 p3의 답이나 유도가 이 차이 때문에 틀리지는 않는다.
- Lecture04 PDF24 하단 일반 K차원 식에는 (Φ^TΦ)^(-1)Φ^Ty 뒤에 scalar 분수 형태를 이어 적은 표기가 있다. K>1에서 행렬로 나누는 분수는 일반 공식으로 유효하지 않다. 이번 해설 p4/p6은 역행렬 공식을, p10은 K=1인 scalar분모를 사용하므로 이 원자료 표기 문제를 답에 전파하지 않는다. 원본 슬라이드는 보존했다.
- p2(b) verify의 잘못된 대비 문장은 컨트롤러에게 보고했고, 수정 후 실제 조각을 재확인했다. 독립 검산의 정답은 변경되지 않았다.

## 원자료 해시

- `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/교과서/Mathematics_for_Machine_Learning.pdf` SHA-256 `3f87b70c64a35d30ec4e565b4d5cfd18fe913002d3b3bed44691c7d0838911bc`
- `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/과제/과제1/26_10_Introduction_to_Machine_Learning_homework1_rev.pdf` SHA-256 `4aaa039018637dc052419554ee6b6f0c069a32289c791d73d40ea87ed6fc6bd8`
- `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/강의노트/Lecture04_Linear_Regression_Part2_rev_HO.pdf` SHA-256 `0fc58bff676fe751eadae57ba34864ad0b1b7da76b1a6007c243d25d00017a4e`
