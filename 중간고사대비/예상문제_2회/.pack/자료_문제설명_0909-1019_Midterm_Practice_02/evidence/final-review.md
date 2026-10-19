# 모의평가 2회 최종 독립 검토

검토자: final_review_02 (Native 실행의 새 최종 검토자)
검토일: 2026-10-19
판정: **pass_with_minor — Critical 0, Important 0, Minor 1**

## 검토 범위와 방법

- `.pack/questions.json` 10문항/31소문항 전체와 `solutions.json`의 모든 solve/verify를 읽어 문제 요구, 조건, 중간 계산, 답, 검산을 대조했다. 별도 블라인드 풀이 `evidence/blind-solutions.md`와 계산 검증 `math-check-result.json`의 실제 내용도 확인했다. 작성자의 content-review/source-visual 문서로 독립 검토를 대신하지 않았다.
- `explanations/p1.html`부터 `p10.html`까지 7구역과 소문항 수를 확인했다. 1–9번은 solve/verify 각각 3개, 10번은 각각 4개이며 누락이 없다. 설명 stage의 소유 fragment 10개가 원본과 바이트 단위로 같다. HTML에는 모든 understand/recall/start/solve/verify/pitfall 본문이 있고 MD에도 공백 정규화 후 모든 31개 solve 본문이 있다.
- `explanation-result.json`이 가리키는 stage HTML/MD의 제목은 모두 `머신러닝기초 중간고사 모의평가 2회 문제설명`이다. 1회 slug/문서 제목의 잔존은 검색되지 않았다.
- 생성된 문제/답안 PDF를 pdfinfo로 확인했다. 둘 다 10쪽, 1440 × 810 pt (16:9)이다. problems-sheet-0..2, answers-sheet-0..2에서 전체 20쪽을 시각 대조하고, answers-1..10 전체 개별 PNG도 확대 확인했다. 문제·수식·답의 잘림, 겹침, 빈 답안, 대체 글리프는 보이지 않는다. 답안과 함께 반복 표시된 조건·요구도 검토했다.
- HTML 화면의 p6 solve, p9 solve, p10 verify 캡처를 추가 확인했다. 수식 표시는 정상이다. 전체 10문항 × 화면 크기 × 테마의 실행 검사는 root 담당이므로 이 문서는 그 검사나 발행 승인을 대신하지 않는다.
- blueprint의 15개 원문 경로가 실제 존재하고 SHA-256과 일치함을 확인했다. HW1 P6–P14/P17–P19/P22/P25와 MML 주요 참조를 대조했다. 교과서 PDF 298,299,307,312,314,315,318쪽은 원 PDF에서 직접 텍스트를 읽었고, HW PDF4 및 MML PDF300/318 그림도 시각 확인했다. STT0909의 평균·분산 공동 최적화 발언과 STT1019의 직교투영/중간고사 범위/약 50:50 발언을 직접 읽었다.

## Critical

없음.

## Important

없음. 풀이를 바꾸거나 문항을 철회해야 하는 수학적 오류, 필수 조건 누락, 요구된 중간 계산 누락은 발견하지 못했다.

## Minor

### M1 — 6번의 새 응용을 뒷받침하는 강의 근거를 독자용 출처 문장에도 보여 주면 좋음

- 위치: `.pack/explanations/p6.html:1`의 recall/출제 근거 문장, `.pack/blueprint.json`의 p6 origin_ref 및 course_evidence (288–295행). 같은 문장은 현재 stage HTML/MD에도 들어 있다.
- 관찰: 독자에게는 `MML 9.2 maximum likelihood; unknown noise variance. MML PDF 298, 299, 300쪽의 개념을 사용한 새 변형·응용 문제`라고 표시된다. 그러나 MML PDF298은 이 절에서 잡음분산을 알려진 값으로 가정하며, PDF299–300은 그 조건에서 theta를 추정한다. 미지 평균·분산을 함께 최적화하는 수업 근거는 blueprint에 있는 STT0909 1669–1672행이지만 독자용 문장에는 나오지 않는다.
- 영향: 수학은 맞고 새 응용임도 명시되어 있어 차단 결함은 아니다. 다만 제시된 교과서 쪽에서 미지 분산 ML 결과를 직접 찾으려는 독자에게 출처 연결이 불분명하다.
- 제안: 6번의 독자용 출처를 `0909 수업의 Gaussian 평균·분산 최적화 설명과 MML 9.2의 우도·로그우도 방법을 결합한 새 스칼라 응용; 미지 분산 결과는 여기서 직접 유도`처럼 구체화한다. 2회 로컬 설명/metadata만 수정하면 충분하며 공유 스킬이나 1회 변경을 요구하지 않는다.

## 수학 검토 기록

| 문항 | 대조 결과 |
|---|---|
| p1 a–c | det=t−2, t=2의 일반해 (1−u,2−u,u), 불일치 우변, t=3의 해 (0,1,1) 및 열공간 해석이 맞다. |
| p2 a–c | Jacobian 규약과 전치, gradient (2,2), 직접 성분 미분, 비단위 d에 대한 정의된 방향미분 0, 비정지점 결론이 맞다. |
| p3 a–c | 평균 (0,4), 공분산 diag(6,2), 정규화 계수 1/(4π√3), 공동 Gaussian에서의 독립/원 X의 비독립이 맞다. |
| p4 a–c | 완전제곱 (theta−1)^2+4 바깥의 −1/2를 보존했다. posterior N(1,1), ML3/MAP1, evidence exp(−2)/√(8π)가 맞다. |
| p5 a–c | 중복 행과 열독립을 구별한다. ML(0,3), 잔차(−1,0,1), SSE2, 예측12; MAP(3/4,3/2), 예측27/4가 맞다. |
| p6 a–c | log s 항과 정규화 상수를 보존했다. SSE>0에서 평균과 SSE/N이 공동 전역 ML이며 표본 (1,2,6)에서 3,14/3이다. SSE=0이면 s→0+에서 우도가 발산하여 열린 모수공간에 최대점이 없다는 결론과 검산이 맞다. |
| p7 a–c | 비영 prior 중심의 우변항, 역분산 벌점, MAP(2,4/3), 예측14/3, 양의 정부호 Hessian과 두 잡음분산 극한이 맞다. |
| p8 a–c | posterior 평균(1/2,1/2), 공분산 I/2; f*=N(1,1), y*=N(1,3), MAP 대입 N(1,2)가 맞다. 미래 교차 공분산1/2는 공통 theta 때문에 생기며 조건부 독립과 y만 조건화한 의존을 올바르게 구별한다. |
| p9 a–c | M1의 비대각 공분산1, M2의 2I, evidence의 정규화와 이차형식, BF≈0.70036, posterior odds≈2.10108, P(M1|y)≈0.67753이 맞다. 현재 문제는 두 모델만으로 공간이 완결됨을 명시한다. |
| p10 a–d | 직교 잔차에서 정규방정식을 유도했다. P의 수치/대칭/멱등, ridge 계수(1/8,5/8)와 비직교 잔차가 맞다. Hv=3v/4와 H²v=9v/16으로 대칭만으로 직교투영이 되지 않음을 보였다. |

블라인드 풀이의 p9 초기 조건 주의는 문서 끝의 새 문제 해시 재확인에서 해소되었다. 계산 검증 JSON은 28개 검사키이며 일부 소문항을 묶는다. 이를 31개 독립 계산 테스트라고 과장하지 않는다. 31개 소문항은 블라인드 문서 및 본 검토에서 별도로 대응했다.

## declined-to-judge / 한계

- 공식 출제 가능성·실제 적중률·교수의 확정 문항 여부: 판단하지 않는다. 산출물은 새 변형·응용임을 명시한다.
- 전체 화면/테마 조합의 브라우저 동작과 최종 발행 상태: root가 진행하므로 이 검토의 판정 범위 밖이다. review.json의 not_run은 현 단계에서 정상이며 결함으로 세지 않았다.
- 본 검토 이후 변경본은 자동 승인하지 않는다. root가 수정 범위를 확인하고 필요한 재생성/회귀 검사를 수행해야 한다.

## 검토 시 입력 해시

- `중간고사대비/예상문제_2회/.pack/questions.json`: `8cf0b5365a0f52444933bfe582ed5cc0639b7363471fe10828e328a3848bed68`
- `중간고사대비/예상문제_2회/.pack/solutions.json`: `9c9c894294252d5cd34ec2b9518c8145069541303f19ef91fe711d446b4c3ef2`
- `중간고사대비/예상문제_2회/.pack/blueprint.json`: `ee8f9f2db373cdd1c99dea0ceabb779ed8bf1aea5f8d0831a3d100328937f6a6`
- `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/tmp/ml-midterm-practice-02/native/explanation-3188950a59ff4b668a8e7f68ee7f95b9/문제설명_0909-1019_Midterm_Practice_02.html`: `be45f8ca95af5a02fa6f84b3315947cb0acd9a3bab02429b0ff0adc4fdde614b`
- `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/tmp/ml-midterm-practice-02/native/explanation-3188950a59ff4b668a8e7f68ee7f95b9/.pack/문제설명_0909-1019_Midterm_Practice_02.md`: `f50a7e6b584f863657b2fed01a315197820f694af5a220407c26bdf8d7dfe777`
