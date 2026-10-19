# 예상문제 1회 전체 해설 보강 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 예상문제 1회 1~10번 전체 42개 소문항의 해설을 기호의 의미부터 중간 계산과 결과 해석까지 이어 읽을 수 있도록 보강한다.

**Architecture:** 기존 EXAM SourcePack과 문항별 HTML 조각을 유지한다. `.pack/tools/build_exam.py`의 `explain` 경로로 HTML·MD와 발행용 fragments를 함께 생성하고, 새 수학·내용·원문·브라우저 검토를 수행한 후 기존 발행 API로 교체한다. 문항·답안 PDF와 공용 생성기 코드는 수정하지 않는다.

**Tech Stack:** Python 3.10+, 기존 EXAM/MPE Python API, HTML, 로컬 KaTeX/Pretendard, pytest, 정확 유리수/상징 계산, 실제 브라우저.

**Spec:** 이 문서의 [승인된 설계](#승인된-설계). 2026-10-20 대화에서 사용자가 승인한 grill-yourself 설계를 실행에 필요한 형태로 보존했다.

## Global Constraints

- 범위는 예상문제 1회의 1~10번, 전체 42개 소문항이다. 문항별 수는 `[3,3,3,3,3,5,6,6,5,5]`다.
- 각 소문항은 ‘무엇을 구하나 → 기호가 무엇인가 → 왜 이 식을 쓰나 → 일반식·수치 대입·중간 계산 → 결과 해석·검산’을 이어 설명한다.
- 기호의 의미를 다른 문항에서 가져오지 않는다. 기호 정의와 적용 조건은 해당 문항 안에서 확인할 수 있어야 한다.
- 분모·역수·제곱근·1/2는 중간 계산을 남긴다. 행렬 공식에는 차원을 함께 확인한다.
- 중요한 설명은 해당 소문항 본문에 둔다. 기존 7구역 understand/recall/start/solve/verify/pitfall/retry, sum, 목차·문항 ID·문제 패널을 유지한다.
- 기존 3번의 분산·정밀도 및 정규화 교정 내용을 보존한다.
- 기존 문제 HTML·문제 PDF·답안 PDF·cards·questions.json·solutions.json·blueprint.json의 조건과 정답은 보존한다.
- 중요한 설명을 접힌 패널에만 두지 않는다. 본문 LaTeX는 기존 로컬 KaTeX로 렌더링한다.
- 학습 숙달은 확인되지 않았다. 설명 후 동의한 사실을 독립 회상 성공으로 기록하지 않는다.
- 새 문제팩·영상·PDF·UI 기능을 만들지 않는다. 커밋·푸시는 이번 작업의 완료 조건이 아니다.
- 발행 검토 기준은 `problem-explain-2026-10-15`다. 실제 수행하지 않은 검토에 pass를 쓰거나 이전 승인을 복사하지 않는다.

## Review Focus

1. 아래첨자의 뜻이 문항마다 다르다: p2의 x₁은 성분, p4의 x₁은 스칼라 관측, p5의 x₁은 벡터 관측이다. Task 1·2의 문항별 의미 검토로 확인한다.
2. 분산·역분산과 행렬의 역행렬이 뒤섞이기 쉽다: p3·p4·p7·p8에서 계수 비교 및 λ 연결을 정확 계산과 설명 검토로 확인한다(Task 2·3).
3. 상수 생략은 목적에 따라 달라진다: 최적화에서는 버릴 수 있어도 정규화·evidence에서는 필요한 인자를 보존한다(Task 2·3).
4. 점 추정의 평균 예측과 사후예측분포를 구분한다: p4·p8의 평균·분산·잡음·모수 불확실성을 비교한다(Task 2·3).
5. 긴 유도와 옛 절대경로는 재생성·화면·발행을 깨뜨릴 수 있다: 새 경로의 참조 해시, 조각 동기화, 3화면×2테마의 전 문항 표시를 확인한다(Task 4).

---

## 승인된 설계

이번 대화에서 사용자는 φ가 함수인지, φ(x)가 벡터인지, x_n이 벡터의 성분인지 관측 번호인지, Φ가 무엇인지, 전치와 행 배치가 왜 필요한지, θ의 모양, 새 입력의 평균 예측, 사전 공분산과 λ의 관계에서 설명이 필요했다. 3번 학습 기록에서는 분산 3/4와 정밀도 4/3, 정규분포 앞 계수의 제곱근·역수, g·Z·q와 정규화 적분 연결이 필요했다. 이를 실제로 확인된 혼동으로 사용하되 다른 문항의 이해 부족까지 확인됐다고 단정하지 않는다.

| 문항 | 해설 보강 수용 기준 |
|---|---|
| p1 | 열배치·선형결합을 실제 성분 연산으로 펼친다. 비영 계수와 영벡터를 구분하고, 자유변수·우변의 열공간 포함 여부·Gram 내적·역행렬 조건을 연결한다. |
| p2 | x의 성분과 벡터 출력 f를 구분한다. 네 편미분의 위치, 이차형식 곱셈과 1/2, gradient·Hessian, 정지점의 최소성·유일성 근거를 설명한다. |
| p3 | 기존 교정을 유지한다. 앞 계수의 곱→지수 전개→완전제곱→분산 읽기→정규화 계수→적분 Z→q=g/Z를 생략 없이 연결한다. |
| p4 | x_n→φ(x_n)→전치→Φ 구성→Φθ를 실제 값으로 보여 준다. φ/φ(x)/Φ/θ의 역할과 크기, 평균 예측, σ²/b²와 σ²Σ₀⁻¹, 절편까지 prior가 적용되는 이유를 설명한다. |
| p5 | 확률벡터 X와 관측 벡터 x_n 및 성분 X_i를 구분한다. 평균→편차→외적→공분산, 변환에서 b의 소거, 교차공분산 순서, 무상관과 독립의 반례를 계산한다. |
| p6 | 조건부 분포→독립성의 곱→음의 로그→경험위험→이차식→미분→정규방정식을 연결한다. 고정된 변수·상수와 모수에 대한 선형성을 명시한다. |
| p7 | Bayes 분모를 최적화에서 생략하는 이유, 사전분산의 분모, σ²를 곱해 λ를 얻는 과정, λm₀, λ>0의 유일성과 극한을 설명한다. |
| p8 | 세 Gaussian 인자와 분모 4, A·b·c 계수 비교, 완전제곱·정규화, 상수배 분산의 제곱, f_*·y_*·MAP 고정 대입을 구분한다. |
| p9 | θ 적분과 prior 가중 평균의 의미, 완전제곱·앞 계수·적분, 밀도와 점 확률, Bayes factor·prior odds·posterior odds·확률의 관계를 설명한다. |
| p10 | 계수공간과 예측공간, h·t의 역할, 모든 h에 대한 도함수 조건, 정규방정식, 계수 추정 행렬과 투영행렬, 대칭·멱등·피타고라스 논증을 연결한다. |

일반화에 주의한다. ridge 계수가 성분별로 언제나 줄어든다고 말하지 않는다. 공동 Gaussian 조건 없이 무상관을 독립이라고 하지 않는다. 최적화용 상수 생략을 evidence 계산에 적용하지 않는다. 정규화가 새 데이터 오차를 항상 개선한다고 말하지 않는다.

## 파일 구조와 실행 인터페이스

이하 모든 경로는 저장소 루트 기준이다. 셸의 위치를 반드시 저장소 루트로 둔다.

- `OUT = 중간고사대비/예상문제_1회`
- `RUN = tmp/ml-problem-explain/midterm-01-expansion-20261020` (이미 있으면 덮어쓰지 말고 고유 접미사를 붙인다).
- `DATA = .pack/자료_문제설명_0909-1019_Midterm_Practice_01`
- 저작 입력: `OUT/.pack/explanations/p1.html`~`p10.html`. `build_explain`이 실제로 읽는 설명 원본이다.
- 발행 HTML: `OUT/문제설명_0909-1019_Midterm_Practice_01.html`.
- 발행 MD: `OUT/.pack/문제설명_0909-1019_Midterm_Practice_01.md`.
- 재생성 자료: `OUT/DATA/fragments/p1.html`~`p10.html`, `manifest.json`, `validation.json`, 포함 evidence 및 기존 로컬 자원.
- 검토·전달 기록: `OUT/.pack/evidence/{answer-checks.json,approved-review.json,browser-check.json,content-review.md,final-review.md}`, `OUT/.pack/delivery.json`, `OUT/.pack/제작검증.md`. 실질 변경과 현재 해시에 맞춰 갱신한다.
- 새 검산·검토 원본은 RUN 아래에 보관하고, 검토가 참조하는 파일은 build 전에 `OUT/.pack/evidence/`에 보관한다. build 후 evidence를 추가하면 재build·재검토한다.
- 재생성 API: `build_exam.build_explain(repo: Path, output: Path, run: Path) -> dict`, 키는 `pack`, `artifacts`, `review_path`다. CLI는 `python "$OUT/.pack/tools/build_exam.py" explain --repo . --out "$OUT" --run "$RUN"`이다.
- CLI 산출 `RUN/explanation-result.json`: `stage`, `html`, `md`, `manifest`, `files`, `review_path`. 공용 `mpe_cli`의 run.json/stage.json과 다른 형식이므로 섞지 않는다.
- 발행 API: `mpe_publish.publish_explanation(pack, artifacts, fragments, reviews, destination, backup_dir)`. 같은 프로세스의 `build_explain` 결과와 저작 조각을 사용한다.
- 최종 검사 CLI: `python "$OUT/.pack/tools/check_exam.py" --out "$OUT" --repo .`.

### Task 1: p1·p2의 기호·행렬 연산과 미분 연결 보강

**Files:** Modify `OUT/.pack/explanations/p1.html`, `p2.html`; Create `RUN/coverage.md`, `RUN/baseline-hashes.json`.

**Interfaces:** Consumes 기존 문항과 저작 규칙 `.agents/skills/ml-problem-explain/references/{authoring,verification}.md`. Produces 기존 data-explanation/data-subpart 계약을 유지한 p1·p2 조각과 42개 소문항 수용 검토표.

- [x] **Step 1:** Python 버전을 확인하고 원 문제 HTML·PDF 2개·기존 설명 HTML/MD·10개 조각·발행 자료와 기록을 RUN의 backup에 복사한다. 보존 대상의 SHA-256을 baseline-hashes.json에 기록한다. 기존 사용자 변경을 별도로 확인한다.
- [x] **Step 2:** coverage.md에 42행을 만들고 각 소문항의 질문 의미·기호·선택 이유·전개·해석·검산 충족 여부를 기존 내용으로 점검한다. 실제 누락을 before로 기록하고, 텍스트 키워드만으로 이해 가능 여부를 판정하지 않는다.
- [x] **Step 3:** p1(a~c)를 저작한다. v₁+v₂-v₃=0의 세 성분, α₃=t에서 α=(2-t,1-t,t), b와 c의 차이, UᵀU의 네 내적과 determinant 3을 계산한다.
- [x] **Step 4:** p2(a~c)를 저작한다. 네 편미분을 각각 계산하고, xᵀAx의 교차항을 전개하며, 연립방정식으로 x_*=(2/7,-1/7)을 구한다. 양의 정부호와 최소성의 논리를 풀어쓴다.
- [x] **Step 5:** `mpe_contract.validate_fragment(problem, fragment) -> list[str]`를 두 문항에 실행해 빈 목록을 확인하고 coverage의 해당 6행을 재검토한다. 실제 곱·미분 결과를 별도 계산으로 확인한다.

### Task 2: p3~p5의 정규화·특징행렬·공분산 연결 보강

**Files:** Modify `OUT/.pack/explanations/p3.html`, `p4.html`, `p5.html`; Update `RUN/coverage.md`.

**Interfaces:** Consumes Task 1의 표기·구역 계약. Produces p3~p5의 완결된 조각과 해당 9행의 검토 결과.

- [x] **Step 1:** p3(a~c)의 기존 교정과 수용 기준을 대조한다. m=1/2, v=3/4, precision=4/3, q의 계수 √(2/(3π)), Z=e^(-1/2)/√(8π)를 보존하며 완전제곱·적분·상수 인자를 연결한다.
- [x] **Step 2:** p4(a)에 x₁=-1,x₂=0,x₃=1을 하나씩 넣는 과정과 φ/φ(x_n)/Φ/θ의 차원, Φ의 행 배치 약속과 행렬 곱의 연결을 추가한다. ΦᵀΦ=diag(3,2), Φᵀy=(5,4)의 모든 성분을 계산한다.
- [x] **Step 3:** p4(b~c)에 θ_ML=(5/3,2), 평균 예측 17/3, Σ₀=b²I₂, λ=σ²/b²=1, σ²Σ₀⁻¹=I₂, θ_MAP=(5/4,4/3), 예측 47/12를 연결한다. σ²=1·Σ₀=2I₂일 때 λ=1/2인 짧은 확인 예를 넣는다.
- [x] **Step 4:** p5(a~c)에 세 중심화 벡터, 외적 하나의 네 성분과 합산, Σ_X=1/9·[[8,-4],[-4,8]], Σ_Y=diag(8/9,8/3), C_XY=[[4/9,4/3],[4/9,-4/3]]를 전개한다. 세 Y값과 결합확률 0 대 주변확률 곱 1/9로 독립을 반박한다.
- [x] **Step 5:** 세 조각의 구조 검사를 실행하고 coverage 9행과 Task 1의 회귀 항목을 재검토한다. 특히 p2·p4·p5 아래첨자 뜻을 서로 비교해 올바른 문맥인지 확인한다.

### Task 3: p6~p10의 확률·유도·예측·투영 설명 보강

**Files:** Modify `OUT/.pack/explanations/p6.html`~`p10.html`; Create `RUN/verify_expansion.py`, `RUN/math-results.json`; Update `RUN/coverage.md`.

**Interfaces:** Consumes 기존 문항의 a~f 요구와 앞 소문항 결과. Produces 완결된 5개 조각, 총 42행 coverage, 독립 계산을 대조할 정확 계산 결과.

- [x] **Step 1:** p6(a~e)에 독립 Gaussian 밀도의 곱, 정규화 계수 (2πσ²)^(-N/2), 음의 로그, L=C+N·R/(2σ²), 제곱노름의 네 항에서 교차항을 합치는 과정, 열 gradient와 유일성 논증을 쓴다.
- [x] **Step 2:** p7(a~f)에 likelihood·prior·posterior의 역할과 고정값, λ=σ²/τ²의 유도, λm₀, 양의 정부호 논증을 쓴다. 마지막 예는 θ=(5/11,5/11), λ=0의 θ₁+θ₂=1, λ→∞의 0을 계산한다. b²와 τ²는 각각 해당 자료의 사전분산 표기임을 연결한다.
- [x] **Step 3:** p8(a~f)에 제곱항 3θ²-6θ+5, A=b=3/2·c=5/2, posterior N(1,2/3)의 계수 계산, f_*~N(2,8/3), y_*~N(2,14/3), MAP 고정 예측 N(2,2)를 전개한다. 상수배 분산은 중심화한 제곱으로 설명한다.
- [x] **Step 4:** p9(a~e)에 적분 변수를 제거한다는 뜻, A=1+1/v_j의 완전제곱과 남은 상수항, evidence N(0,1+v_j)의 앞 계수까지 정리한다. B₁₂=√(5/2), prior odds=1/2, posterior odds=B₁₂/2, P(M₁|0)≈0.44152와 최종 M₂ 선택을 구분한다.
- [x] **Step 5:** p10(a~e)에 θ̂,h∈R²와 y,r∈R³의 구분, t에 대한 미분, 모든 h이면 Φᵀr=0인 이유, 역행렬·전치의 순서를 쓴다. θ̂=(4/3,1), P=1/6·[[2,2,2],[2,5,-1],[2,-1,5]], r=(2/3,-1/3,-1/3), SSE=2/3을 계산하고 피타고라스 등호 조건을 설명한다.
- [x] **Step 6:** `RUN/verify_expansion.py`를 계산 검증 도구로 작성한다. `main() -> int`가 p1~p5·p7~p10의 위 수치, p3·p8·p9의 Gaussian 계수/적분, p2·p6·p7의 미분, p10의 Pᵀ=P·P²=P·Φᵀr=0을 정확 또는 상징 계산으로 검사하고 math-results.json에 결과를 기록하게 한다. 이 도구는 해설 문구의 키워드를 검사하지 않는다.
- [x] **Step 7:** `python "$RUN/verify_expansion.py"`를 실행한다. 실패한 등식이 0개여야 하며 증명·개념 항목은 coverage에서 별도로 검토한다. 10개 조각의 validate_fragment 결과가 모두 빈 목록이고 총 42개 solve/verify 소문항이 대응하는지 확인한다.

### Task 4: 새 검토·재생성·발행과 전달

**Files:** Modify 위 파일 구조에 명시한 발행 HTML·MD·자료·검토·delivery 기록. Create RUN의 stage와 backups. 기존 생성기·공용 코드 수정 없음.

**Interfaces:** Consumes Task 1~3의 저작 조각, coverage와 계산 결과. Produces 현재 원문·설명·참조 해시에 묶인 검토 기록과 최종 check_delivery PASS인 설명 팩.

- [x] **Step 1:** 원 문제와 필요한 교안·MML 페이지를 실제로 대조한다. 별도 검산자는 문제·필요 이론만 받고 설명·기존 정답을 보지 않은 상태에서 42항목을 검산한다. 제작 스킬의 독립 검산 요구에 따라 이 단계에서 검산 에이전트를 사용할 수 있다. root의 대조 결과를 함께 기록한다.
- [x] **Step 2:** 10문항의 retry를 기호 해석·첫 줄·오개념 확인 질문으로 구체화하고 sum을 본문과 일치시킨다. coverage의 모든 항목이 해설 자체로 충족되는지 읽고 content-review.md에 근거를 남긴다.
- [x] **Step 3:** 필요한 새 검산 근거를 evidence에 저장한다. blueprint의 참조를 현재 저장소에서 실제 경로로 확인하고 읽은 참조의 절대경로·SHA-256을 수집한다. 과거 Mac 경로의 validation을 수정해 재사용하지 않는다.
- [x] **Step 4:** 전용 `build_exam.py explain` CLI를 실행한다. 새 stage HTML·MD·manifest와 review.json을 확인하고 `mpe_render.check_artifacts(pack, artifacts)` 및 `validate_fragment`를 실행한다. 두 API의 오류 목록이 모두 비어야 한다. 생성된 MD의 누락 여부를 42항목과 대조한다.
- [x] **Step 5:** 실제 브라우저로 1280×900·1024×900·375×812의 light/dark에서 p1~p10 전체를 확인한다. 수식·표·본문이 잘리지 않고 문서 가로 넘침·KaTeX/콘솔 오류·누락 자원·외부 요청이 0인지 확인한다. 목차·이전/다음·요약·문제 패널과 1023→1024 경계를 점검하고 현재 HTML SHA-256을 포함한 browser-check.json과 시각 증거를 기록한다.
- [x] **Step 6:** 실제 source_visual/content/independent/browser 결과와 42개 content·independent item을 새 review에 기록한다. 새 검토 뒤 artifact_hashes를 최종 확인하고 validate_reviews 결과가 비어 있는지 확인한다. 충돌은 disputed로 남기고 해결 전 발행하지 않는다.
- [x] **Step 7:** 실제 API `publish_explanation(pack, artifacts, fragments, reviews, output, run / 'backups')`로 발행한다. 발행 HTML·MD·fragments의 동기화 및 review·delivery·제작검증 기록의 최종 경로/해시를 갱신한다. 승인 파일 자신을 manifest 승인 해시에 포함시키는 순환 참조를 새로 만들지 않는다. 기존 해시 산출 계약을 그대로 사용한다.
- [x] **Step 8:** `python "$OUT/.pack/tools/check_exam.py" --out "$OUT" --repo .`를 실행하여 `status: pass`, `errors: []`를 확인한다. 이어 `python -m pytest "$OUT/.pack/tools/tests/test_exam.py" -q`로 기존 계약 회귀 검사를 실행한다. 환경/참조 실패는 숨기거나 테스트를 약화하지 말고 해결한다.
- [x] **Step 9:** baseline-hashes.json과 비교하여 원 문제 HTML·PDF 2개와 저작 문제 입력이 동일한지 확인한다. `git diff --check`와 `git status --short`로 변경 범위를 확인한다. 최종 전체 변경 검토를 수행하고 학습상 혼동을 유발하는 지적을 해결한다.
- [x] **Step 10:** 사용자에게 완성 HTML·MD의 절대경로 링크, 전 문항 보강과 주요 변화, 실제 검증 결과를 간결하게 전달한다. 유용하면 HTML을 Codex 패널로 연다. 승인된 범위의 로컬 발행에 추가 승인을 요구하지 않는다.

## 계획 자체 검토

- 설계 범위: 10문항·42소문항과 모든 공통 설명 기준을 Tasks 1~4에 배정했다.
- 파일 구조: 전용 build가 저작 원본을 읽고 발행 fragments·MD를 생성하는 방향을 소스에서 확인했다. 공용 CLI의 다른 run 형식을 사용하지 않는다.
- 검증 구분: 구조 검사·정확 계산·독립 검산·설명 의미 검토·원문 대조·브라우저 검토를 구분했다. 문구 존재만 확인하는 새 pytest는 만들지 않는다.
- Review Focus의 5개 위험 모두 해당 작업의 계산 또는 실제 검토 단계로 연결했다.
- 실행 방식: 아직 사용자 선택 전이다. Native를 권장한다. 이번 학습 대화의 맥락과 표기 일관성을 한 작성자가 유지하고, 독립 검산과 마지막 검토만 분리하는 편이 적절하다.
