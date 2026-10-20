# 출제 기준과 입력

`STT/1019 머러기.md`의 마지막 시험 안내를 직접 읽는다(현재 312,314행 근처). 범위는 시작부터 1019 직교투영까지다. 교수의 안내는 약 절반 과제와 비슷한 문제, 약 절반 모델을 따라가는 이론 분석이다. **10문항은 사용자 지정**이다. 시험시간·배점·주제별 공식 출제 확률을 만들지 않는다. logistic regression/SVM 등 범위 밖 주제를 넣지 않는다.

## 출제표

| 문항 | 기본 역할 |
|---|---|
| p1 | 선형독립·선형결합·해의 유일성 |
| p2 | 행 gradient·Jacobian·이차함수 미분 |
| p3 | Gaussian 곱·완전제곱·정규화 |
| p4 | 특징함수/설계행렬·ML/MAP 수치 계산 |
| p5 | 공분산·아핀 변환 |
| p6 | 확률모델→iid likelihood→NLL→ERM→정규방정식 |
| p7 | prior→posterior 목적함수→MAP/ridge |
| p8 | 사후분포→사후예측·불확실성 |
| p9 | evidence→Bayes factor→posterior odds·모델 비교 |
| p10 | 직교성→최소제곱·직교투영 |

p1~p5는 과제 변형, p6~p10은 모델 분석을 기본으로 한다. 주제 조정은 범위·5:5 역할을 유지한다. 모델 분석은 4~6개 정도의 연결된 소문항으로 앞 결과를 다음 단계에 사용하게 한다. 도출할 최종 공식을 조건이나 힌트에 먼저 제공하지 않는다. 숫자만 계산하는 독립 질문 묶음으로 대체하지 않는다. 1회차의 42소문항을 다음 회차에 강제하지 않는다.

새 회차는 실제 확인한 과제·교재 문항에서 데이터·가정·요구 과정의 변형을 설계한다. 이전 회차와의 차이를 `.pack/회차차이.md`에 문항별로 남긴다. 과거 삭제된 2회 내용을 새 회차로 복원하지 않는다.

## 저장 계약

기준 1회 `.pack/blueprint.json`의 schema_version=1을 따른다. range=`0909-1019`, slug=`Midterm_Practice_<최소두자리>`, style=`exam`이다. sources에는 실제 읽은 저장소 파일의 id/path/SHA-256을 기록한다. 상대 경로는 저장소 루트 기준이며 NFC/NFD 경로를 어댑터로 해석한다. 출처가 바뀌면 새로 읽고 검증한다.

questions는 p1~p10 순서다. kind는 homework_variant 5개, model_analysis 5개다. origin_kind는 homework_variant/textbook_variant/theory_application, origin_ref는 실제 과제 번호·교재 문항, assumptions는 해당 가정이다. subparts는 실제 요구의 a,b,... 순서이며 중복 없이 카드·영어·해설과 일치한다. theory_refs/course_evidence는 sources의 id를 참조하고 실제 PDF 페이지·절·STT 위치를 적는다. 검증기가 출처 주장의 진위를 대신 확인하지는 않는다.

카드는 1회의 pN.html 구조를 사용한다: `article.card#pN`, `data-origin-kind`, `data-origin-ref`, `EXAM Problem N`, 조건·ask·참고 solution/answer·출처. 원문 탭용 original 안에 data-english-title, data-english-conditions, data-english-ask가 각각 하나 있다. 영어 ask는 하나의 `<ol type="a">` 안에 data-english-part="a" 등의 직계 li를 순서대로 둔다. start/reversed/value로 표시 번호를 바꾸지 않는다. 과제1 영어 문체를 따르되 공식 시험 원문으로 표시하지 않는다. 한영 수치·가정·질문·난이도를 대조한다.

한국어 PDF는 영어 original을 비운 동일 내용 snapshot으로 생성하며, 한국어 카드 digest와 실제 snapshot/report/PDF hash를 binding한다. 최종 HTML의 영어를 지우지 않는다. PDF는 기존 1440×810pt, 하단135pt 흰 여백이며 긴 문항은 계속 페이지로 나눈다. 글씨를 축소하거나 템플릿을 다시 디자인하지 않는다.

## 보존 근거

현재 1회와 이후 수정 이력이 초기 프롬프트보다 우선한다. `80d29c1` 유도 사슬, `a4ff066` 기호/차원, `7c409d0` 행 미분, `da9dc53` 공식 적용 간결화, `1d808ef` 영어 본문을 반영한다. 과거 GPT 대화에서 확정된 p8(d~f)의 공식 적용 간결화와 p8(a)의 잡음→조건부 likelihood 설명은 현재 조각으로 확인한다. 오래된 장황한 전개나 열 gradient로 되돌리지 않는다.
