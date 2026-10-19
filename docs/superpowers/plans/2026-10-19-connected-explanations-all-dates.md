# 다른 날짜 정리노트의 연결 중심 설명 개선 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 1014·1019에서 검증한 설명 방식을 나머지 9개 날짜의 정리노트 HTML·MD에 주제별로 적용한다.

**Architecture:** 기존 도입과 레이어 안에서 출발식·변경점·중간 연산·결과 재사용을 연결한다. 날짜별 HTML·MD 쌍을 독립적인 수정·검증·커밋 단위로 삼고, 공통 생성기나 UI는 변경하지 않는다. 임시 stage에서 검증한 쌍만 원본에 반영한다.

**Tech Stack:** 기존 HTML/KaTeX, Markdown, Python 표준 라이브러리와 기존 검사기, 실제 브라우저.

**Spec:** 이 파일의 [설계 기준](#설계-기준) 및 `.agents/skills/ml-review-pack/references/big-picture-first.md`. 선행 설계와 시범 실행은 `docs/superpowers/plans/2026-10-19-connected-note-explanations.md` 참조.

## Global Constraints

- 설명 순서: “전체 연결 → 기억할 출발점 → 변경점 비교 → 한 단계씩 유도 → 다음 결과 연결 → 복원용 요약”.
- “수식 유도·개념 연결이 있는 부분에 적용하며, 모든 토픽에 같은 형식을 강제하지 않습니다.”
- “일반 공식 → 이번 문제의 대입 → 결과”를 끊기지 않게 설명한다.
- “수업 공식 / 동치인 재표현 / 보충 설명”을 등장 지점에서 구분한다.
- “설명을 무조건 길게 하는 것이 아니라, 식과 식 사이의 연결을 빠뜨리지 않는 것”을 목표로 한다.
- 벡터 자체는 열벡터, 스칼라의 벡터 미분 결과는 행벡터다. 열벡터 방정식으로 바꾸는 전치를 보인다.
- 기존 토픽 ID·목차·앵커·링크·유효한 원래 수식·출처·교수님 인용·SVG·위젯·스크립트·스타일을 보존한다.
- 발견한 수학적 오류나 오해를 부르는 설명은 근거와 수정 이유를 기록하고 HTML·MD 함께 고친다. 무조건 원문을 보존하느라 오류를 남기지 않는다.
- 예고·보충을 해당 날짜에 배운 본문으로 승격하지 않는다. 학습자의 숙달을 추측하지 않는다.
- 복습문제·문제설명·PDF·영상·인터랙티브·공통 UI·스킬 지침·1014·1019는 수정 대상에서 제외한다.
- 모든 대응 MD는 현재 `.pack/` 위치를 유지한다. 전체 팩 재생성이나 전체 MD 변환으로 무관한 파일을 덮어쓰지 않는다.
- 실행 방식은 기존 선택인 Native를 유지한다. 계획 검토 후 직접 실행하고 마지막에 한 번 독립 리뷰한다. 푸시는 하지 않는다.

## Review Focus

1. 분포와 점 추정의 혼동: ML·MAP도 대입 예측으로 분포를 낼 수 있다. 0916의 “단답/분포” 표를 출력 대상 기준으로 바로잡고 의미 검토한다(Task 4).
2. 목적함수 배율·상수·미분 방향: 정규화 계수와 사후 공분산에서 배율을 잃지 않으며 행벡터 정상조건 뒤 전치를 보인다(Tasks 3, 6, 7).
3. 시점에 맞지 않는 설명: 예고된 일반 사전분포나 미유도 예측 결과를 강의에서 유도한 것으로 쓰지 않는다. STT·슬라이드 대조 기록을 남긴다(Tasks 7–9).
4. 행렬을 스칼라처럼 약분: 비가환 공분산과 rank-deficient 특징행렬에서도 가정·곱 순서·해의 유일성을 정확히 설명한다(Tasks 6, 10).
5. HTML만 개선되고 MD·해시 진입이 깨짐: 전체 MD 목차·기존 링크를 보존하고 토픽 직접 진입에서도 출발식이 보이며 375px 두 테마에서 읽힌다(모든 날짜 작업의 쌍 검증).

---

## 설계 기준

사용자는 기억한 결과를 새 식의 어느 자리에 넣는지 보았을 때 쉽게 이해했다. 따라서 이미 있는 큰 그림을 다시 생성하지 않고, 상세 본문에서 공백이 있는 연결을 메운다. 날짜 순서가 곧 읽기 순서는 아니므로 수정한 토픽에 필요한 출발식과 앞선 결과 링크를 함께 둔다.

- **개론(0909):** 한 예측 모델로 모델 선택 → 파라미터 학습 → 새 데이터 평가를 연결한다. 아직 안 배운 MAP 수식이나 미분을 억지로 넣지 않는다.
- **학습 기준(0914·0916):** 같은 데이터 항을 재사용하며 손실·우도·사전분포가 무엇을 바꾸는지 비교한다. 파라미터 추정 결과와 예측 결과를 구별한다.
- **베이지안 추론(0921):** 주변화 → 곱 규칙 → 조건부 독립을 줄마다 연결한다. 예측 적분의 사후 가중치와 모델 증거의 사전 가중치를 구별한다.
- **회귀 계산(0923·0928):** 단일 관측 → 행렬 잔차 → 행벡터 미분 → 정상조건 → 해를 연결한다. 사전분포를 추가했을 때 달라지는 항만 비교한다.
- **불확실성 전달(0930):** 스칼라 분산·공분산에서 행렬 공식으로 연결하고 실제 변환행렬의 자리를 보인다. 미래 강의의 최종 예측분포는 필요한 경우 후속 노트 링크로 연결한다.
- **가우시안 계산(1007·1012):** 스칼라 완전제곱 → 행렬 계수 비교 → 평균·공분산을 연결한다. 이미 충분한 증명은 반복하지 않고 어떤 결과를 어디에 쓰는지만 보강한다.

각 날짜의 완료 기준은 독자가 (1) 출발점을 말하고, (2) 바뀐 항을 구분하며, (3) 중간 연산을 따라가고, (4) 결과를 다음 식에 대입할 수 있는 설명이 본문에 있는 것이다. 키워드 수나 글자 수는 품질 기준이 아니다. 우측 요약에는 본문에서 설명한 결과만 둔다.

## 파일 구조

아래 각 행은 수정할 두 파일의 **정확한 경로**다. 새로운 영구 생성기·검사기·레퍼런스는 만들지 않는다.

| 날짜 | HTML | 대응 MD |
|---|---|---|
| 0909 | `복습노트/0909/정리노트_0909_Data_Models_Learning.html` | `복습노트/0909/.pack/정리노트_0909_Data_Models_Learning.md` |
| 0914 | `복습노트/0914/정리노트_0914_ERM_and_MLE.html` | `복습노트/0914/.pack/정리노트_0914_ERM_and_MLE.md` |
| 0916 | `복습노트/0916/정리노트_0916_MAP_and_Generative_Models.html` | `복습노트/0916/.pack/정리노트_0916_MAP_and_Generative_Models.md` |
| 0921 | `복습노트/0921/정리노트_0921_Bayesian_Inference_Model_Selection.html` | `복습노트/0921/.pack/정리노트_0921_Bayesian_Inference_Model_Selection.md` |
| 0923 | `복습노트/0923/정리노트_0923_Linear_Regression.html` | `복습노트/0923/.pack/정리노트_0923_Linear_Regression.md` |
| 0928 | `복습노트/0928/정리노트_0928_Linear_Regression.html` | `복습노트/0928/.pack/정리노트_0928_Linear_Regression.md` |
| 0930 | `복습노트/0930/정리노트_0930_Bayesian_Linear_Regression.html` | `복습노트/0930/.pack/정리노트_0930_Bayesian_Linear_Regression.md` |
| 1007 | `복습노트/1007/정리노트_1007_Product_of_Gaussians.html` | `복습노트/1007/.pack/정리노트_1007_Product_of_Gaussians.md` |
| 1012 | `복습노트/1012/정리노트_1012_Several_Mathematical_Proofs.html` | `복습노트/1012/.pack/정리노트_1012_Several_Mathematical_Proofs.md` |

계획 밖 파일은 변경하지 않는다.

## 공통 실행 계약

실행 기록은 한국어로 쓴다. 아래 공통 절차를 날짜별 검증 단계에서 참조한다.

### 기준선과 작업 인터페이스

- `RUN`은 실행 시 새로 생성하는 `%TEMP%/ml-connected-all-<uuid>/` 절대 경로다. `baseline/`, `stage/`, `work/`, `evidence/`를 둔다.
- `RUN/evidence/scope.json`은 `[{date: str, html: str, md: str, topics: list[str], sources: list[str]}]`다. 경로는 위 표와 아래 Task의 토픽 ID를 그대로 쓴다.
- `RUN/baseline/`에 대상 18개 파일과 날짜 폴더 전체의 SHA256 목록을 보존한다. stage에는 대상 날짜 폴더를 복사하고, 원자료·공유 vendor·다른 날짜를 상대 링크 검증에 사용할 수 있게 읽기 연결한다.
- 기존 검사기 인터페이스는 `check_learning_map.py <HTML...>`, `check_html.py <HTML...>`, `html2md.check_md(html_path: Path, md_path: Path) -> list[str]`다. 반환값 `[]`가 MD 검사 통과다. 모듈은 `.agents/skills/ml-review-pack/scripts`에서 임포트한다.
- 새 보존 검산은 `RUN/work/check_preservation.py`에만 작성한다. 입력은 baseline·stage 경로와 scope.json, 결과는 `evidence/preservation.json`이다. 토픽 ID/순서, 원래 href의 출현 횟수, script/style/SVG, 모든 MD 링크·목차, 대상 밖 해시가 보존되어야 한다. 수학 오류로 바꾸는 식은 `evidence/corrections.md`에 원문·근거·새 식을 기록해 예외를 제한한다.
- 계산 검산은 `RUN/work/math_checks.py`에서 `fractions.Fraction`과 표준 라이브러리 `unittest`를 쓴다. 설명 품질을 문구 일치 단위 테스트로 대체하지 않는다.

### 날짜별 쌍 검증

1. 해당 날짜의 변경 토픽을 읽어 여섯 설명 기능의 적용/불필요/누락과 STT·슬라이드 위치를 `evidence/<date>-review.md`에 기록한다. 모든 원자료를 무차별 재전사하지 않는다.
2. stage HTML에 위 두 정적 검사기를 실행해 모두 `OK`, 대응 MD에 `check_md(...) == []`, 보존 검사에 실패 0을 확인한다. 새 설명·수식·조건은 HTML과 MD를 직접 대조한다.
3. 실제 HTTP 브라우저에서 1440×900·375×812와 light/dark 조합 4개를 확인한다. 전체 토픽을 순회해 `.content` 가로 넘침 0, KaTeX 오류 0, 미렌더 수식 0을 확인한다. 수정 토픽은 해시 직접 진입, 도입·긴 식의 캡처, 페이지 요약·테마·목차 조작을 검사한다. 위젯이 있는 날짜는 기존 입력을 바꾸고 값 반영을 확인한다. 기존 PDF·인터랙티브 링크와 추가한 교차 노트 링크가 정확한 대상으로 열리는지 확인한다. PDF 자체를 재생성·재검수했다고 보고하지 않는다.
4. 통과한 HTML·MD 두 파일만 함께 반영한다. 반영 직전 원본이 baseline과 같음을 확인하고, 다르면 최신 변경을 통합해 필요한 검사만 다시 한다. 실패하면 그 날짜의 원본을 유지한다.
5. `git diff --check` 통과 후 해당 두 경로만 명시해 stage·커밋한다. `git add .`는 쓰지 않는다. 공개 경로에서도 변경 토픽과 링크를 확인한다.

## Task 1: 범위·출처·보존 기준선 확정

**Files:** Read 위 표의 18개 파일, 날짜별 `STT/<MMDD> 머러기.md`, 관련 `강의노트/*.pdf`. Create RUN 내부 scope·백업·검증 도구·증거만.

**Interfaces:** Consumes 설계 기준과 기존 검사기. Produces 위 실행 계약의 scope.json·baseline·stage·보존 검사기. 후속 Task는 날짜 필터로 같은 기준선을 사용한다.

- [x] **Step 1:** 최신 Git 상태를 확인하고 범위 18개 파일을 백업해 scope.json과 해시를 작성한다. 선행 커밋은 `fd0664c`지만 실행 시 HEAD를 새로 기록한다.
- [x] **Step 2:** 날짜별 수정 토픽의 기존 formal·요약·MD를 읽고 원자료 위치 및 연결의 공백을 scope.json과 `<date>-review.md`에 확정한다. 0930·1007·1012에는 `scalar-to-vector-covariance.md` 전체를 읽어 적용한다.
- [x] **Step 3:** 보존 검사기를 만들고 정상 baseline 복사본에는 실패 0을 확인한다. 별도 임시 복사본의 링크 하나·MD 목차·토픽 ID를 각각 삭제했을 때 해당 오류가 잡히는지 확인한 뒤 원래 stage를 유지한다.
- [x] **Step 4:** 9개 원본에 두 정적 검사와 MD 검사를 실행하고 선행 오류를 기록한다. 계획 작성 시 두 HTML 검사기는 9개 모두 `OK`였으나 실행 시 다시 확인한다.

## Task 2: 0909 — 모델을 정하고, 학습하고, 평가하는 연결

**Files:** 위 표 0909 쌍. Modify `s0-targets`, `s2-function`, `s2-fitting`, `s3-three-phases`, `s3-hyperparam`, `s4-cheatsheet`.

**Interfaces:** Consumes Task 1 기준선. Produces 모델 꼴·파라미터·손실·평가 데이터 역할을 분리한 설명. 이후 날짜는 이 용어를 재사용한다.

- [x] **Step 1:** `y=θ₁x+θ₀` 하나를 기준으로 각 단계가 무엇을 입력받아 무엇을 결정하는지 현재 공백을 기록한다.
- [x] **Step 2:** 기존 도입과 상세 문장을 연결한다. 차수를 정하는 일과 계수를 맞추는 일을 비교하고 선택한 계수를 새 입력에 대입하는 자리까지 보인다. learning rate처럼 함수 꼴을 직접 바꾸지 않는 하이퍼파라미터도 있으므로 기존 “하이퍼파라미터는 모두 모델 자체를 바꾼다”식 단정을 바로잡는다. ML을 베이지안 방법과 동일시하는 문장도 확률모델 기반 추정과 베이지안 추정을 구분해 수정한다.
- [x] **Step 3:** MD를 동기화하고 개념 검토한다. 훈련 오차 최소가 일반화 보장은 아니며, 상세 미분·새 공식 없이 흐름이 복원되는지 확인한다.
- [x] **Step 4:** 날짜별 쌍 검증을 실행하고 통과한 쌍만 반영한다.
- [x] **Step 5:** 두 파일만 커밋한다: `docs(notes): connect model selection training and evaluation in 0909`.

## Task 3: 0914 — 같은 제곱오차를 ERM과 ML에서 재사용

**Files:** 위 표 0914 쌍. Modify `s0-learning-map`, `s1-affine`, `s2-squared`, `s3-reg`, `s4-mle-ls`, `s5-cheatsheet`.

**Interfaces:** Consumes 0909 모델/학습 역할. Produces 잔차 벡터·제곱오차·음의 로그우도·정규화 목적함수의 대응.

- [x] **Step 1:** `R_emp=(1/N)∥y−Xθ∥²`와 `NLL=C+(1/(2σ²))∥y−Xθ∥²`의 연결에서 빠진 조건·배율을 기록한다.
- [x] **Step 2:** 바이어스 흡수 → 관측별 예측을 행렬로 쌓기 → 잔차 → 제곱합을 연결한다. 고정된 `σ²>0`에서 양의 배율과 θ 무관 상수는 argmin을 바꾸지 않음을 보여준다. 정규화 목적함수의 데이터 항은 그대로이고 패널티만 추가됨을 비교한다. `≈`로 상수 생략을 표현하지 않는다.
- [x] **Step 3:** `math_checks.py`에 `test_erm_nll_scale`를 추가해 N=2, σ²=2, 잔차=(1,−2)에서 제곱합=5, ERM=5/2, NLL−C=5/4를 assert한다. 설명과 MD를 동기화한다.
- [x] **Step 4:** `python RUN/work/math_checks.py`의 해당 테스트와 날짜별 쌍 검증을 통과시킨다.
- [x] **Step 5:** 두 파일만 커밋한다: `docs(notes): connect ERM and Gaussian likelihood in 0914`.

## Task 4: 0916 — ML 목적함수에 prior를 추가하는 MAP

**Files:** 위 표 0916 쌍. Modify `s0-learning-map`, `s1-map`, `s1-map-reg`, `s2-posterior`, `s3-three-ways`, `s4-cheatsheet`.

**Interfaces:** Consumes 0914의 NLL. Produces posterior 정규화·MAP 목적함수·FB 결과 보존의 구별. 가우시안 정규화 유도는 기존 보충 범위를 유지한다.

- [x] **Step 1:** 현재 비교표의 ML/MAP “단답(Yes/No)”와 FB “분포” 구분을 검토한다. 파라미터 추정 결과와 관측 예측 결과가 섞였음을 출처와 함께 기록한다.
- [x] **Step 2:** 같은 베이즈 식에서 MAP은 θ 무관 분모를 생략하고 최고점을, FB는 정규화한 분포를 유지함을 연결한다. 음의 로그에서 ML 데이터 항에 `−log p(θ)`가 더해짐을 줄마다 보인다. uniform prior의 지지집합 안에서만 ML과 같은 목적함수라는 조건을 둔다. 비교표는 “θ 한 점 / θ 사후분포 유지”로 고치고 모든 방식이 예측분포를 낼 수 있음을 구별한다.
- [x] **Step 3:** `test_map_weights`를 추가한다. 이산 후보 우도=(1/5,4/5), prior=(9/10,1/10)이면 ML 선택은 둘째, 정규화 posterior=(9/13,4/13), MAP 선택은 첫째를 assert한다. RUN 검산이며 새 복습문제는 만들지 않는다. MD를 동기화한다.
- [x] **Step 4:** 해당 계산 테스트와 날짜별 쌍 검증을 통과시킨다.
- [x] **Step 5:** 두 파일만 커밋한다: `docs(notes): distinguish parameter estimates and predictions in 0916`.

## Task 5: 0921 — 같은 주변화를 예측과 모델 증거에 대입

**Files:** 위 표 0921 쌍. Modify `s0-learning-map`, `s0-approx`, `s1-derivation`, `s1-expectation`, `s3-bayes-ms`, `s3-bayes-factor`, `s4-cheatsheet`.

**Interfaces:** Consumes posterior와 점 추정 구별. Produces posterior 가중 예측과 prior 가중 증거의 비교, posterior odds 복원 규칙.

- [x] **Step 1:** 일반 주변화와 곱 규칙을 출발식으로 잡고 적분 변수·남는 변수·가중분포를 기존 식과 대조한다.
- [x] **Step 2:** `P(A|X)=∫P(A,θ|X)dθ` → 곱 규칙 → 명시한 조건부 독립 → 기존 예측식을 연결한다. delta 대입은 근사임을 밝힌다. 모델 증거에서는 prior로 가중한다는 차이를 표 하나로 비교하고 posterior odds=prior odds×Bayes factor에 원래 베이즈 식을 대입한다.
- [x] **Step 3:** `test_bayesian_averaging`을 추가해 weights=(1/4,3/4), 조건부 확률=(1/5,4/5)의 가중값=13/20, prior odds=2와 BF=3이면 posterior odds=6을 assert한다. `g(θ)=θ²`, θ=0/2 각1/2이면 E[g]=2와 g(E[θ])=1도 확인해 평균 대입과의 혼동을 검사한다. MD를 동기화한다.
- [x] **Step 4:** 해당 계산 테스트와 날짜별 쌍 검증을 통과시킨다. 그래프·독립성 상세를 새로 확장하지 않는다.
- [x] **Step 5:** 두 파일만 커밋한다: `docs(notes): connect marginalization prediction and evidence in 0921`.

## Task 6: 0923 — 잔차에서 정상조건, 다시 예측값까지

**Files:** 위 표 0923 쌍. Modify `s0-learning-map`, `s2-nll`, `s2-ml-erm`, `s3-normal-eq`, `s3-pinv`, `s3-vector-diff`, `s4-cheatsheet`.

**Interfaces:** Consumes ERM/NLL의 공통 잔차. Produces 행벡터 미분 → 전치 → 정상조건 → full-column-rank 해 → Xθ의 연결.

- [x] **Step 1:** 기존 목적함수 이름과 행/열 차원을 확인하고 정상조건의 전치 및 가역성 조건 누락을 기록한다.
- [x] **Step 2:** 기존 유도를 재사용해 미분 결과의 각 항이 1×D임을 보이고, `θᵀXᵀX=yᵀX`를 전치해 `XᵀXθ=Xᵀy`로 바꾼다. full-column-rank에서만 역행렬 공식을 쓰며 일반 유사역행렬의 존재와 이 특수 표현을 구별한다. 결과를 `ŷ=Xθ̂`의 자리에 넣는다.
- [x] **Step 3:** `test_normal_equation`을 추가해 X=[[1,0],[1,1],[1,2]], y=(1,2,2)에서 θ̂=(7/6,1/2), Xᵀ(y−Xθ̂)=0을 assert한다. rank-deficient X=[[1,1],[2,2]]는 XᵀX의 det=0을 확인하고 역행렬·유일해 주장을 배제하는 의미 검토를 기록한다. MD를 동기화한다.
- [x] **Step 4:** 해당 계산 테스트와 날짜별 쌍 검증을 통과시킨다. 보충 미분 증명을 본문에 중복 복사하지 않는다.
- [x] **Step 5:** 두 파일만 커밋한다: `docs(notes): connect residual gradients and regression estimates in 0923`.

## Task 7: 0928 — ML에서 MAP으로 바뀌는 항 비교

**Files:** 위 표 0928 쌍. Modify `s0-learning-map`, `s1-chain`, `s1-theta-ml`, `s2-feature-matrix`, `s4-gaussian-prior`, `s4-ml-vs-map`, `s5-general-prior`, `s5-rls`, `s6-cheatsheet`.

**Interfaces:** Consumes 행벡터 정상조건과 Φ 특징행렬. Produces 등방 prior MAP의 변경 항, 일반 prior로의 대입 관계. 후속 상세는 검증된 1014로 링크한다.

- [x] **Step 1:** ML의 `ΦᵀΦ`, `Φᵀy`를 출발점으로 prior 항이 추가되는 자리를 기록하고 일반 prior 토픽의 실제 수업/예고 경계를 확인한다.
- [x] **Step 2:** 데이터 항 미분은 유지하고 prior의 행벡터 미분을 더해 정상조건을 묶는다. 등방 prior에서는 왼쪽에 `(σ²/b²)I`가 추가되고 오른쪽은 그대로임을 비교한다. 일반형의 `m₀=0,S₀=b²I` 대입으로 특수형을 복원한다. 일반형의 전체 해 유도를 0928 수업 내용으로 새로 추가하지 말고 기존 설명 범위를 유지하며 1014로 연결한다. 평균제곱손실의 λ와 비정규화 제곱합의 계수를 혼용하지 않는다.
- [x] **Step 3:** `test_map_special_prior`를 추가해 ΦᵀΦ=diag(3,2), Φᵀy=(3,2), σ²=2, b²=2이면 ML=(1,1), MAP=(3/4,2/3)을 assert한다. 평균손실+λ∥θ∥² 관례에서 `Nλ=σ²/b²`를 확인한다. MD를 동기화한다.
- [x] **Step 4:** 해당 계산 테스트와 날짜별 쌍 검증을 통과시킨다. 행벡터 관례·후속 링크·예고 경계를 직접 검토한다.
- [x] **Step 5:** 두 파일만 커밋한다: `docs(notes): compare unchanged and prior terms in 0928 MAP`.

## Task 8: 0930 — 스칼라 규칙을 벡터 불확실성에 적용

**Files:** 위 표 0930 쌍. Modify `s0-learning-map`, `s2-predictive`, `s2-cond-expectation`, `s3-covariance`, `s3-variance-matrix`, `s4-sum`, `s4-affine`, `s5-cheatsheet`.

**Interfaces:** Consumes 주변화와 스칼라 기댓값/분산. Produces Cov 정의·선형변환·가중 예측의 연결. 최종 가우시안 예측식 상세는 1019 링크를 사용한다.

- [x] **Step 1:** 스칼라 분산, 공분산의 원소, 행렬 차원 중 이미 충분한 설명을 찾아 반복하지 않을 부분을 기록한다.
- [x] **Step 2:** 스칼라 `Var(aX+b)=a²Var(X)`에서 행렬 `Cov(AX+b)=AΣAᵀ`로 연결하고 전치가 필요한 차원을 보인다. 합의 분산에는 교차공분산이 있고 비상관/독립일 때 사라짐을 구별한다. 예측 평균의 선형성만으로 예측분포 전체가 평균 파라미터 대입과 같다고 결론 내리지 않도록 정리한다.
- [x] **Step 3:** `test_affine_moments`를 추가해 μ=(1,−1), Σ=[[4,1],[1,9]], A=[2,3], b=5일 때 E[Y]=4, Var[Y]=109, Cov(X,Y)=(11,29)ᵀ를 assert한다. 교차항 12를 빠뜨린 결과97과 구별한다. MD를 동기화한다.
- [x] **Step 4:** 해당 계산 테스트와 날짜별 쌍 검증을 통과시킨다. 일반 모멘트 공식에 가우시안 가정이 필요하다는 잘못된 제한을 넣지 않는다.
- [x] **Step 5:** 두 파일만 커밋한다: `docs(notes): connect scalar covariance and affine uncertainty in 0930`.

## Task 9: 1007 — 완전제곱 결과로 분포의 평균·공분산 읽기

**Files:** 위 표 1007 쌍. Modify `s0-factory`, `s1-affine`, `s3-lemma`, `s3-product-scalar`, `s3-product-matrix`, `s4-posterior`, `s5-cheatsheet`.

**Interfaces:** Consumes 아핀 모멘트와 prior/likelihood. Produces 스칼라 이차식과 행렬 이차식의 계수 대응, 기존 사후분포 결과의 적용 자리.

- [x] **Step 1:** 기존 스칼라·행렬 곱 공식에서 어떤 계수를 읽는지와 posterior 결과의 수업/예고/보충 상태를 확인한다.
- [x] **Step 2:** 스칼라 `ax²−2bx+c`의 중심 b/a·분산1/a에서 행렬 `xᵀAx−2bᵀx+c`의 중심 A⁻¹b·공분산 A⁻¹로 대응시킨다. A는 대칭 양의 정부호라는 조건과 임시 묶음임을 밝힌다. 정규화 전 곱과 PDF를 구별한다. 기존 posterior 식의 precision 합·precision×mean 합을 어디서 대입했는지 연결하되 비정칙 Φ의 likelihood를 무조건 θ에 관한 정규화 Gaussian PDF라고 부르지 않는다. 시점 밖의 상세는 1014·1019로 연결한다.
- [x] **Step 3:** `test_scalar_gaussian_product`를 추가해 μ₀=0, ν₀=4, μ₁=3, ν₁=1일 때 분산4/5·평균12/5를 assert한다. ν는 표준편차가 아닌 분산임을 HTML·MD에서 확인하고 동기화한다.
- [x] **Step 4:** 해당 계산 테스트와 날짜별 쌍 검증을 통과시킨다. 지수의 −1/2와 precision 배율을 직접 대조한다.
- [x] **Step 5:** 두 파일만 커밋한다: `docs(notes): connect completing squares and Gaussian parameters in 1007`.

## Task 10: 1012 — 증명의 출력이 다음 계산의 입력이 되게 연결

**Files:** 위 표 1012 쌍. Modify `s0-learning-map`, `s0-variance`, `s0-cross`, `s1-lz`, `s1-inverse`, `s1-det`, `s2-matrix-lemma`, `s2-product`, `s2-rewrite`, `s3-cheatsheet`.

**Interfaces:** Consumes 아핀 변환·Gaussian coefficient matching. Produces 밀도 변수변환, 공분산 변환, 곱 공식이 각각 어디에 필요한지 복원 가능한 설명.

- [x] **Step 1:** 이미 상세한 공분산·변수변환·행렬 곱 증명은 보존 대상으로 표시한다. 각 증명에서 만든 결과의 다음 대입 자리만 빠져 있는지 점검한다.
- [x] **Step 2:** 도입을 세 도구의 입력·출력·사용처로 보강한다. `Σ=LLᵀ`를 지수부의 역행렬과 앞 계수의 행렬식에 각각 재사용함을 연결한다. 스칼라 역수 합과 행렬 precision 합을 비교하고, 강의식으로 바꾸는 단계의 곱 순서와 전치 이유를 유지한다. Σ₀Σ₁=Σ₁Σ₀를 가정하지 않는다.
- [x] **Step 3:** `test_noncommuting_gaussian_product`를 추가한다. Σ₀=[[2,1],[1,2]], Σ₁=diag(1,3)이면 Σ₀Σ₁≠Σ₁Σ₀이고 `(Σ₀⁻¹+Σ₁⁻¹)⁻¹=Σ₁(Σ₀+Σ₁)⁻¹Σ₀=[[9/14,3/14],[3/14,15/14]]`임을 assert한다. `test_density_transform`에서는 L=[[2,0],[1,3]], Σ=LLᵀ=[[4,2],[2,10]], detΣ=36, abs(detL)=6을 확인한다. MD를 동기화한다.
- [x] **Step 4:** 두 계산 테스트와 날짜별 쌍 검증을 통과시킨다. 긴 유도는 식 자체의 내부 스크롤을 허용하되 본문 페이지 가로 넘침은 없어야 한다.
- [x] **Step 5:** 두 파일만 커밋한다: `docs(notes): connect Gaussian proof outputs and substitutions in 1012`.

## Task 11: 날짜 사이의 연결과 최종 Native 리뷰

**Files:** Read 9개 변경 쌍과 1014·1019. Modify 검토에서 발견한 이번 범위 오류만. Update 이 계획의 체크박스와 실행 결과.

**Interfaces:** Consumes Tasks 1–10의 HTML·MD·계산·보존·브라우저 증거. Produces 변경 날짜·검증 결과·수정/보류 항목·커밋 목록이 있는 `RUN/evidence/final-review.md`.

- [x] **Step 1:** 전체 계산 테스트, 9개 쌍의 보존 검사, 9개 HTML 두 검사, MD 검사, `git diff --check`를 실행해 모두 통과한 결과를 기록한다. 기존 `test_learning_map.py`, `test_html2md.py`, `test_regression_0909_0916.py`도 unittest discover의 해당 패턴으로 실행한다.
- [x] **Step 2:** 실제 브라우저에서 새 교차 날짜 링크와 1014·1019 도착 토픽을 확인한다. 전역 표기 통일 때문에 날짜 고유의 X/Φ·ν/σ²를 무조건 치환하지 않았는지 검토한다. 출발식은 해당 토픽만 읽어도 파악되어야 한다.
- [x] **Step 3:** Native의 최종 독립 리뷰어 한 명에게 설계 기준·18개 파일 diff·원자료 대응표·검증 증거를 전달한다. 모델은 해당 실행 스킬의 지정을 따르고 없으면 상속한다. Critical/Important를 고치고 수정 부분의 검사만 다시 수행한다. 읽기 전용 리뷰를 요청하고 미반영 항목은 이유를 남긴다.
- [x] **Step 4:** 리뷰 수정이 있으면 해당 경로만 추가 커밋하고, 계획 완료 체크·실행 결과를 갱신한다. 최종 Git 상태·커밋 목록·남은 문제를 확인하고 사용자에게 날짜별 변화와 노트 링크를 보고한다. 푸시는 하지 않는다.

## 계획 자체 검토 및 인계

- 현재 존재하는 다른 날짜 9개를 모두 포함했고 실제 MD 9개의 `.pack/` 경로를 확인했다. 1014·1019를 다시 수정하지 않는다.
- 여섯 설명 기능은 기존 도입·본문·요약에 적용하며 주제와 무관한 MAP 표를 전체 날짜에 반복하지 않는다.
- Review Focus 다섯 항목은 각각 개념 교정, 수치 검산, 원자료 경계 확인, 비가환/특이행렬 확인, 전 날짜 브라우저·MD 보존 검사에 대응한다.
- 문서 편집에는 의미 비교를 쓰고, 수학과 보존 검사에는 실행 가능한 수치·손상 검증을 쓴다. 검산용 입력을 새 문제로 배포하지 않는다.
- 공통 검증은 한 곳에 정의하고 날짜 작업은 해당 내용·토픽·독립적으로 검토할 수 있는 결과와 커밋을 지정했다.
- 계획 작성 시점에 기존 작업은 `fd0664c`로 커밋했고, 새 9개 노트의 본문은 아직 수정하지 않은 상태였다.
- 실행 방식 Native는 이미 선택되어 있다. writing-plans의 인계 규칙에 따라 이 계획을 한 번 검토받은 후 executing-plans로 진행한다.


## 실행 결과 (2026-10-19)

Native 실행 완료. 0909·0914·0916·0921·0923·0928·0930·1007·1012의 HTML·대응 MD 18개를 날짜별 검증 후 커밋했다. 원래의 수식·ID·링크·그림·위젯·스크립트·스타일과 수정 대상 밖 자료는 보존했다. 최종 독립 리뷰는 수학·출처·시점·MD 보존에서 Critical/Important를 발견하지 않았고, 0928 반복 대입 1건은 핵심 요구인 반복 축소에 따라 교정했다.

최종 검사 39개 통과, 구형 합본 경로를 요구하는 기존 검사 2개는 skip으로 구분했다. 현재 날짜별 경로의 정적·MD·수식 검사, 36개 날짜/화면/테마 조합과 656개 토픽 순회, 67개 로컬 링크 응답, 실제 공개 경로 9개 검증을 통과했다. 리뷰 수정 토픽은 다시 검증했다.

백업·검증·독립 리뷰 및 실행 판단 기록: `C:\Users\Hyunjun\AppData\Local\Temp\ml-connected-all-d6449ef3ae\evidence\final-review.md`. 외부 푸시나 자료 재생성은 하지 않았다.
