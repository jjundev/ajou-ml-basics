# 실제 중간고사 문제설명·오답분석 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `시험결과/중간고사/26-2 머러기 중간고사 스캔.pdf`(실제 시험지 + 내 답안 + 채점, 79점)로 (1) `/ml-problem-explain` 형식의 문제설명 HTML/MD와 (2) 내 실수·약한 개념 분석 문서를 만든다.

**Architecture:** 스캔을 먼저 구조화 전사(문제 원문 / 내 답안 / 채점 표시)로 옮긴다. ml-problem-explain은 현재 `복습문제_*`(REVIEW)·`과제N_*`(HOMEWORK) 카드 HTML과 예상문제(EXAM, blueprint 필요)만 받으므로, 실제 시험용 카드 프로필 `exam`을 추가하고 전사로부터 카드 HTML을 만든 뒤 기존 extract → 저작 → build/check → 검토 → publish 절차를 그대로 탄다. 오답분석은 전사의 채점 데이터와 독립 검산 답을 대조해 별도 MD로 쓴다.

**Tech Stack:** Python 3.10+ 표준 라이브러리(MPE 스크립트), pytest, sympy(검산 evidence 전용), pdftoppm(스캔 렌더링), 로컬 KaTeX/Pretendard.

**Spec:** 사용자 요청(2026-11-09) + `.claude/skills/ml-problem-explain/SKILL.md`, `references/authoring.md`, `references/verification.md`.

## Global Constraints

- 원본 스캔 PDF는 수정·이동하지 않는다.
- 시험지 지시문 보존: "All vectors and gradients are column vectors. The Jacobian convention is (J_g)_ij = ∂g_i/∂x_j. In N(μ, v), v denotes the variance." → SKILL.md의 "원문이 열 gradient를 명시하면 원문·조건을 보존하고 그 관례를 따르며 강의(행벡터)와의 차이를 설명" 분기를 적용한다.
- 해설 문체 `~해요`, 영어 용어 병기, 7구역 `understand → recall → start → solve → verify → pitfall → retry`, 소문항마다 solve/verify 표지.
- `review_policy_version="problem-explain-2026-10-20-row-derivatives"`.
- 외부 네트워크 요청 0, 콘솔·KaTeX 오류 0, 1280×900·375×812 두 테마 가로 넘침 0.
- 이름·학번은 산출물에 전사하지 않는다(원문 이미지 crop에서도 머리말 영역 제외).
- 카드의 "참고 풀이"는 **독립 검산한 정답**이며 내 답안이 아니다. 내 답안은 오답분석에만 쓴다.

## Review Focus

1. 손글씨 오독 — 내 답안·채점자 표기(점수, ☆, "Mean? Var.?")를 잘못 읽으면 분석 전체가 틀린다. 기대: 전사 각 항목에 `confidence`와 원문 crop 경로가 있고, 불확실 항목은 분석에 "판독 불확실"로 표시.
2. 부분 점수 합계 — 소문항 점수 합이 표지 총점 79와 다르면 오독 신호. 기대: Task 1 검사로 차단.
3. 문항 9→10 연속 문항(method credit) — 10번 감점이 9번 오류의 전파인지 독립 오류인지 구분해야 한다. 기대: 분석의 오류 원인 필드에 `propagated_from`.
4. 열/행 gradient 관례 충돌 — 해설이 강의 관례(행)로 바꿔 쓰면 시험 원문과 어긋난다. 기대: 해설은 열 관례, recall에 차이 한 줄.
5. 원문 탭 이미지 크기 — 11MB 스캔을 그대로 넣으면 HTML이 무거워진다. 기대: 문항별 crop을 150dpi PNG(또는 WebP)로 각 ≤600KB.

## Decision Points (실행 전 확인 필요)

- **D1. 카드 프로필:** (권장) MPE에 `exam` 프로필을 추가(Task 2). 대안: 스킬 코드 무수정으로 note-template에 직접 손저작 — 빠르지만 build/check·review 게이트를 잃는다.
- **D2. 스캔 PDF 커밋 여부:** 기본은 생성물만 커밋하고 11MB 스캔은 커밋하지 않음.

---

### Task 1: 스캔 구조화 전사

**Files:**
- Create: `시험결과/중간고사/.pack/transcript.json`
- Create: `시험결과/중간고사/.pack/scan/qN.png` (문항별 crop, N=1..10)
- Create: `시험결과/중간고사/.pack/scripts/check_transcript.py`

**Interfaces:**
- Produces: `transcript.json` = `{exam_date:"2026-10-21", total:79, instructions:str, questions:[{n:int, title:str, points:10, pages:[int], crop:str, parts:[{label:"a"|"b", statement_tex:str, my_answer_tex:str, score:int, max:5, grader_marks:[str], confidence:"high"|"low"}]}]}`

- [ ] **Step 1:** 11쪽을 200dpi로 scratchpad에 렌더링하고 쪽마다 실제로 읽는다(문항이 쪽을 넘는 경우 포함).
- [ ] **Step 2:** `check_transcript.py <json>` 작성 — 단언: 질문 10개, 각 parts 2개, `sum(score)==total==79`, 모든 `crop` 파일 존재·≤600KB, `statement_tex` 비어 있지 않음. 빈 JSON으로 실행해 FAIL 확인.
- [ ] **Step 3:** 전사 작성. 문제 원문은 TeX로 그대로, 내 답안은 쓴 그대로(틀린 식 포함), 채점자 빨간 표기는 `grader_marks`에.
- [ ] **Step 4:** `python3 -I 시험결과/중간고사/.pack/scripts/check_transcript.py 시험결과/중간고사/.pack/transcript.json` → `OK 10 questions, 20 parts, 79 points`.
- [ ] **Step 5:** 사용자에게 low-confidence 항목만 짧게 확인 요청(있을 때만).

### Task 2: MPE `exam` 카드 프로필 (D1 승인 시)

**Files:**
- Modify: `.claude/skills/ml-review-pack/scripts/review_pdf_types.py:40-42`
- Modify: `.claude/skills/ml-problem-explain/scripts/mpe_source.py:80,118,161` (프로필 선택)
- Modify: `.claude/skills/ml-problem-explain/scripts/mpe_render.py:23-32,169,237` (stem·경로·제목)
- Test: `.claude/skills/ml-problem-explain/tests/test_source.py`, `tests/test_render.py`

**Interfaces:**
- Produces: `EXAM_ACTUAL = CardProfile('exam', r'중간고사_(\d{4})_([A-Za-z0-9_]+)\.html', r'Midterm \d{4} Q\d+', '시험', '머신러닝기초 중간고사 {range}', '중간고사_{range}_{slug}', 'Midterm {range} Q{n}')`, `PROFILES['exam']`.
- 산출 경로(HOMEWORK처럼 HTML 옆): `중간고사_{range}_문제설명_{slug}.html/.md`, `figures_문제설명_exam{range}_{slug}/`, `자료_문제설명_exam{range}_{slug}/`. 제목 `머신러닝기초 중간고사 {range} 문제설명`.

- [ ] **Step 1: 실패 테스트**
  - `test_resolve_exam_html_path`: `시험결과/중간고사/중간고사_1021_Midterm.html` 경로 지정 시 `resolve_sources` 반환 1개.
  - `test_load_source_exam_profile`: fixture 카드 2개(`data-source="Midterm 1021 Q1"`) → `pack.profile=='exam'`, `pack.range=='1021'`, `pack.slug=='Midterm'`.
  - `test_exam_output_names`: render 경로 함수가 `('중간고사_1021_문제설명_Midterm', 'figures_문제설명_exam1021_Midterm', '자료_문제설명_exam1021_Midterm')`.
  - `test_all_excludes_exam`: `--target all`이 exam 카드를 고르지 않음. `resolve_sources`의 rglob 화이트리스트(`복습노트`,`과제`)는 그대로 둔다 — exam은 HTML 경로 지정으로만 진입.
- [ ] **Step 2:** `python3 -m pytest .claude/skills/ml-problem-explain/tests/test_source.py .claude/skills/ml-problem-explain/tests/test_render.py -q` → 새 4개 FAIL.
- [ ] **Step 3:** 구현. 프로필 선택은 `profile_for(name: str) -> CardProfile` 한 함수(접두사 `과제`→HOMEWORK, `중간고사_`→EXAM_ACTUAL, 그 외 REVIEW)로 모아 세 곳에서 사용. render 분기는 `pack.profile in ('homework','exam')`일 때 HTML 옆 배치.
- [ ] **Step 4:** 전체 `python3 -m pytest .claude/skills/ml-problem-explain/tests .claude/skills/ml-review-pack/tests -q` → 모두 PASS(기존 테스트 회귀 없음).
- [ ] **Step 5:** 커밋 `feat(ml-problem-explain): support actual exam card profile`.

### Task 3: 시험 카드 HTML

**Files:**
- Create: `시험결과/중간고사/중간고사_1021_Midterm.html`
- Create: `시험결과/중간고사/.pack/scripts/build_cards.py`
- Create: `시험결과/중간고사/.pack/evidence/answer-checks.py`, `answer-checks.json`

**Interfaces:**
- Consumes: `transcript.json`(Task 1), `EXAM_ACTUAL`(Task 2).
- Produces: 카드 `id="p1".."p10"`, `data-source="Midterm 1021 Q{n}"`, 각 카드에 `.conditions`·`.ask` 각 1개, 원문 figure = `.pack/scan/qN.png`, `.solution`의 참고 풀이·`.answer` = 독립 검산 답. 마크업은 `과제/과제1/과제1_Homework1.html` 카드 구조를 따른다.

- [ ] **Step 1:** `answer-checks.py` — sympy로 20개 소문항 정답을 문제 원문만으로 계산(예: Q1a ∇f(−1,2)=(−2,16)ᵀ, Q2a det=3, Q2b p=(2,1,1)ᵀ, r=(1,−1,−1)ᵀ). 결과를 `{ "pN:a": {status, method, conclusion} }`로 저장. 증명형은 `method:"manual-proof"`와 근거 문장.
- [ ] **Step 2:** `build_cards.py transcript.json answer-checks.json out.html` 작성 후 실행.
- [ ] **Step 3:** 검증: `python3 -c "import sys;sys.path[:0]=['.claude/skills/ml-problem-explain/scripts','.claude/skills/ml-review-pack/scripts'];from pathlib import Path;from mpe_source import load_source;p=load_source(Path('시험결과/중간고사/중간고사_1021_Midterm.html'),Path('.'));print(len(p.problems),sum(len(x.subparts) for x in p.problems))"` → `10 20`.
- [ ] **Step 4:** 브라우저로 카드 HTML을 열어 수식·원문 이미지가 깨지지 않는지 확인.

### Task 4: 문제설명 저작·검토·발행 (ml-problem-explain 절차)

**Files:**
- Run dir: `tmp/ml-problem-explain/midterm1021-<id>/`
- Publish: `시험결과/중간고사/중간고사_1021_문제설명_Midterm.html/.md` + figures/자료 폴더

**Interfaces:**
- Consumes: 카드 HTML(Task 3), `answer-checks.json`.

- [ ] **Step 1:** `python3 .claude/skills/ml-problem-explain/scripts/mpe_cli.py extract --repo . --target 시험결과/중간고사/중간고사_1021_Midterm.html --run tmp/ml-problem-explain/midterm1021-<id>`
- [ ] **Step 2:** `authoring.md`, `verification.md`, `vector-derivative-convention.md` 전체 읽기. 각 문항 관련 강의노트·MML 페이지·기존 복습노트를 찾아 references에 기록.
- [ ] **Step 3:** `explanations/p1..p10.html` 저작(7구역). pitfall 구역에 **이 시험에서 실제로 잃기 쉬운 지점**(예: Q1b "State its dimensions" 누락, Q3b mean/variance 미기재)을 일반화해 넣는다 — 개인 점수는 넣지 않는다.
- [ ] **Step 4:** 형제 스킬 ml-note-audit로 감사 → `audit.md`; Critical·Important 수정. `check_vector_derivatives.py`는 열 관례 원문 보존 분기이므로 수동 대조 결과를 기록.
- [ ] **Step 5:** `mpe_cli.py build --run …` → `mpe_cli.py check --run …` exit 0.
- [ ] **Step 6:** review.json에 source_visual/content/independent/browser 실제 검토 기록(1280×900, 375×812, 두 테마).
- [ ] **Step 7:** `mpe_cli.py publish --run …` → 발행 경로 확인.

### Task 5: 오답·약점 분석

**Files:**
- Create: `시험결과/중간고사/중간고사_오답분석.md`
- Create: `시험결과/중간고사/.pack/scripts/check_analysis.py`

**Interfaces:**
- Consumes: `transcript.json`, `answer-checks.json`, 발행된 문제설명 HTML 앵커.

- [ ] **Step 1:** `check_analysis.py` — 단언: 표의 20행, 감점 합 = 21, 각 감점 행에 `오류 유형 ∈ {계산 실수, 요구사항 누락, 개념 오해, 표기·관례, 미완성/시간}`과 근거 crop 링크.
- [ ] **Step 2:** 문서 작성. 구성:
  1. 한눈 요약(총점, 감점 21점의 유형별 분포).
  2. 소문항별 표: 배점 / 득점 / 내 답 / 정답 / 차이 / 오류 유형 / 전파 여부(Q9→Q10).
  3. **실수 패턴**(반복되는 행동 습관: 예 — 문제 요구 항목 체크 누락, 부호·대입 실수).
  4. **어려워하는 개념** 순위: 개념 → 근거 문항 → 강의 날짜(`복습노트/<MMDD>`) → 다시 볼 문제설명 앵커.
  5. 기말 대비 행동 목록(3~5개, 구체적).
- [ ] **Step 3:** `python3 -I 시험결과/중간고사/.pack/scripts/check_analysis.py 시험결과/중간고사/중간고사_오답분석.md` → OK.
- [ ] **Step 4:** 커밋 `docs(exam): add midterm explanation and error analysis` (D2에 따라 스캔 PDF 제외).
