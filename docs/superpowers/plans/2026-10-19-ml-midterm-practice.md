# ML Midterm Practice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 처음부터 1019 직교투영까지의 실제 수업과 과제·MML을 근거로 실전형 중간고사 예상문제 10문항 1회분의 문제지 PDF·해설지 PDF·문제설명 HTML을 제작한다.

**Architecture:** 기존 PDF 템플릿·페이지 분할·문제설명 렌더러·검토 계약을 재사용한다. 이번 자료의 `.pack/tools/`에만 예상문제 입력 어댑터와 제작·검증 진입점을 추가하고 공유 스킬 코드는 변경하지 않는다. 검증된 기본 문제 HTML·PDF 쌍을 먼저 발행한 뒤 그 정확한 원본으로 설명을 생성하며, 설명까지 통과해야 전체 완료로 보고한다.

**Tech Stack:** Python 3.10+, 기존 Python 제작 모듈, fractions/SymPy/NumPy를 이용한 별도 수학 검산, PyMuPDF, Playwright와 로컬 Chrome, 기존 KaTeX/Pretendard 자원. 실행 의존성은 격리 환경에만 준비한다.

**Spec:** 이 문서의 [확정 제작 명세](#확정-제작-명세). 앞선 채팅의 grill-yourself 설계를 실행에 필요한 형태로 함께 보존한다. 실행자는 명세와 작업을 모두 읽는다.

## Global Constraints

- 범위는 처음부터 1019 수업 마지막 직교투영까지다. 대문항은 정확히 10개, 과제 변형 5개와 모델 적용·이론 분석 5개다.
- 교수님의 약 50:50 안내는 제작 배분의 근거이며 확정 배점표나 세부 출제 주제의 보장은 아니다.
- 기본 추천이던 실전형 1회분을 이번 계획의 확정값으로 채택한다. 문제는 원칙적으로 2–4개 소문항이며 공식 힌트는 주지 않고 소문항으로 유도한다.
- PDF는 기존 `video-16x9`: 1920×1080 CSS px, 1440×810pt, 하단 180 CSS px(135pt) 흰 여백이다. 템플릿과 CSS를 수정하지 않는다.
- HTML은 기존 문제 패널·목차·우측 요약과 일곱 설명 구역을 유지한다. 설명 문체는 기존 자료의 `~해요` 체다.
- Python 실행기는 3.10 이상이다. 배포 자원은 로컬 KaTeX/Pretendard를 사용한다.
- 출처는 원본 직접 사용·과제 변형·교과서 변형·교과서 이론 적용 구성 문제를 구분한다. 확인하지 않은 연습문제 번호나 원문을 만들지 않는다.
- 실제로 읽은 수업 자료로 범위를 확인한다. 기존 조사 문서의 로지스틱 회귀·SVM 예정 범위를 그대로 사용하지 않는다.
- 공식 시험시간·배점은 확인되지 않았으므로 정하지 않는다. 출제표의 주제 배분은 추천 구성으로 표시한다.
- `source_visual/content/independent/browser`는 실제 검토 후 기록한다. 수학적 모호함·답 충돌·검토 누락이면 해당 발행을 보류한다.
- 기존 복습노트·과제·STT·교안·교재·공유 스킬 파일은 보존한다. 정리노트·영상·새 스킬은 생성하지 않는다.
- 이 계획 작성은 구현·커밋·푸시 승인이 아니다. 커밋·푸시는 별도 사용자 요청이 있을 때만 수행한다.

## Review Focus

1. 과제 변형을 MML 원문으로 오기하거나 범위 밖 이론을 사용하는 입력: 출제표·카드의 문항 ID/출처/실제 수업 근거가 맞아야 한다. Task 1의 출처 불일치·NFC/NFD 검사.
2. 가역성·양의 정부호·prior 평균·공분산 분모·독립 잡음 조건: 필요한 조건을 문제에 명시하고 해당 가정으로 답을 검산한다. Task 2의 문제별 수학 검토.
3. 소문항 누락 및 풀이를 본 검산을 독립 풀이로 오인: 전 소문항 집합과 블라인드 입력 목록을 확인한다. Task 2·4의 검산/검토 집합 검사.
4. 긴 행렬·유도식의 계속 페이지와 문제지 정답 유출: 축소로 밀어 넣지 않고 기존 분할기를 사용하며 문제지 payload의 풀이·힌트가 비어 있어야 한다. Task 3의 PDF/유출 검사.
5. 승인 후 원본·참조·설명 변경, 모바일 요약·소문항 표지·최종 링크 오류: 오래된 승인을 거부하고 최종 경로에서 재검토한다. Task 4의 stale/화면/배포 검사.

---

## 확정 제작 명세

### 출제 근거와 주제 배분

`STT/1019 머러기.md:312–314`에서 직교투영까지가 범위이고, 약 절반은 과제 유사 문제, 나머지는 모델을 따라가며 이론 분석하는 문제라고 안내했다. 대문항 10개는 사용자가 지정했다. 미응답 선택 #9는 grill-yourself의 기본값 확정 규칙에 따라 **실전형**으로 확정한다.

| ID | 유형 | 문항 목표 | 우선 대조할 자료 |
|---|---|---|---|
| p1 | homework_variant | 선형독립·선형결합·해의 존재와 유일성 | 과제1 P6–P8, MML 2장 |
| p2 | homework_variant | gradient·Jacobian·이차형식 미분과 차원 | 과제1 P10–P12, MML 5장 |
| p3 | homework_variant | 완전제곱을 이용한 가우시안 곱의 평균·공분산 | 과제1 P14·P25, MML 6.5절 |
| p4 | homework_variant | 특징행렬 구성과 ML·MAP 수치 계산 | 과제1 P17–P20, MML 9.2절 |
| p5 | homework_variant | 평균·공분산과 아핀 변환 | 과제1 P21–P22, MML 6장 |
| p6 | model_analysis | 잡음 모델 → i.i.d. 우도 → NLL → 최소제곱 | Lecture03, MML 9.2절 |
| p7 | model_analysis | prior → MAP/ridge 유도 → 정규화 효과 해석 | Lecture03–04, MML 9.2절 |
| p8 | model_analysis | 작은 회귀 모델의 사후분포와 사후예측분포 | 0930–1019, MML 9.3절 |
| p9 | model_analysis | 주변화 → Bayes factor → posterior odds로 두 모델 비교 | 0921·1019, Lecture04 rev_HO s17 |
| p10 | model_analysis | 직교 조건 → 최소제곱 해·투영행렬 → 잔차 직교 검산 | 1019, MML 3.8·9.4절 |

이는 교과서 위치의 후보표다. 최종 문항의 절·쪽수·Example/Exercise 번호는 원 PDF 페이지로 검증한다. 0909–1019 STT 전체를 확인해 데이터·모델·손실/ERM·생성모델/조건부 독립 등 초기 개념을 p6/p7의 모델 가정·해석에 연결한다. 새로운 대문항은 추가하지 않는다. 개별 문항의 소문항 수가 과도해지면 같은 목표 안에서 계산량을 줄인다.

### 출력과 파일 책임

이하 `OUT = 중간고사대비/예상문제_1회`, `TOOLS = OUT/.pack/tools`, `STEM = 중간고사예상_0909-1019_Midterm_Practice_01`. 경로는 저장소 루트 기준이며 실제 파일 탐색은 Unicode 정규화로 발견한 경로를 쓴다.

| 생성 경로 | 책임 |
|---|---|
| `OUT/STEM.html` | 조건·질문·참고 풀이를 가진 제작 원본이자 설명의 원 문제 링크 대상 |
| `OUT/STEM-문제.pdf` | 실전형 문제지, 조건·질문·필기 공간 |
| `OUT/STEM-답안.pdf` | 사용자에게 해설지로 안내할 PDF, 전 소문항의 유도·답·검산 |
| `OUT/문제설명_0909-1019_Midterm_Practice_01.html` | 기존 템플릿을 사용한 전 문항 설명 |
| `OUT/.pack/blueprint.json` | 실제 수업 범위·출처·출제 배분·자료 해시·소문항 목록 |
| `OUT/.pack/cards/p1.html` … `p10.html` | 문항별 원본 조각, 참고 풀이·정답 포함 |
| `OUT/.pack/explanations/p1.html` … `p10.html` | 일곱 구역과 소문항별 풀이·검산을 저작한 조각 |
| `OUT/.pack/evidence/` | 조건/질문만 담은 blind-input.html, 독립 풀이, 검산 코드·결과, 실제 읽은 쪽/화면 기록 |
| `OUT/.pack/제작검증.md`, `OUT/.pack/delivery.json` | 출제 근거·검토·페이지 대응·파일 해시·미해결 기록 |
| `TOOLS/exam_adapter.py` | 이번 예상문제의 CardProfile과 SourcePack 변환·출처/범위 검증 |
| `TOOLS/build_exam.py` | 원본 조립·기존 PDF/설명 모듈 호출·검토 후 발행 진입점 |
| `TOOLS/check_exam.py`, `TOOLS/tests/test_exam.py` | 제작물 구조·출처·해시·발행 요건의 좁은 검증과 회귀 검사 |
| `OUT/.pack/문제설명_*.md`, 기존 설명 렌더러가 소유하는 그림·자료 디렉터리 | 기존 생성 규칙 그대로 유지 |

독립 검토·명령 출력·스크린샷 등 임시 실행 자료는 `tmp/ml-midterm-practice/<고유ID>/`에 둔다. 필요한 근거만 `.pack/evidence/`로 보존한다. 이 계획 턴에서는 위 파일을 생성하지 않는다.

### 재사용 지점과 어댑터 경계

- PDF: `.agents/skills/ml-review-pack/scripts/review_pdf_types.py:27`의 `CardProfile`, `review_pdf_cards.read_cards/normalize_cards`, `build_review_pdf.build_pack(..., profile=EXAM, layout='video-16x9')`를 사용한다.
- EXAM: name=`exam`, filename 정규식=`중간고사예상_(\d{4}-\d{4})_([A-Za-z0-9_]+)\.html`, source 정규식=`EXAM Problem [1-9]\d*`, source_fmt=`EXAM Problem {n}`, kind_label=`예상문제`, title_fmt=`머신러닝기초 중간고사 예상문제 1회`, stem_fmt=`중간고사예상_{range}_{slug}`.
- `data-source="EXAM Problem N"`은 문항 식별자다. 실제 과제·교과서 출처와 변형 방식은 카드의 별도 `data-origin-kind`/`data-origin-ref` 및 blueprint에 기록하고 해설에서 읽을 수 있게 한다.
- 설명: `mpe_types.Problem/SourcePack(profile='exam', ...)`를 만들고 `mpe_render.build_explanation/check_artifacts`, `mpe_contract.initial_reviews/validate_reviews`, `mpe_publish.publish_explanation`을 직접 호출한다. EXAM 지원이 없는 `mpe_cli extract/load_run`을 경유하거나 전역 함수를 monkey-patch하지 않는다.
- `build_explanation`은 exam도 일반 복습과 동일한 파일명·`.pack/` 자원 구조로 렌더링한다. 기존 상단 제목 `머신러닝기초 복습 0909-1019 문제설명`은 허용하고 문항 제목·출처 및 slug로 예상문제를 구분한다. 공유 제목 처리 확장은 이 작업의 범위 밖이다.
- 전체 검토는 기존 `problem-explain-2026-10-15` 계약을 사용한다. 새 build는 이전 pass를 이어받지 않는다.

### Task 1: 수업 범위·출처표와 예상문제 입력 계약 확정

**Files:** Create `OUT/.pack/blueprint.json`, `TOOLS/exam_adapter.py`, `TOOLS/tests/test_exam.py`.

**Interfaces:**
- Consumes: STT 0909–1019 전체, Lecture00–04 실제 해당 페이지, 과제1 원 문제 PDF/HTML, MML 원 PDF, 기존 출처 조사 문서(참고용).
- Produces: `EXAM: CardProfile`; `validate_blueprint(value: dict, repo: Path) -> list[str]`; `load_exam_source(cards_path: Path, blueprint_path: Path, repo: Path) -> SourcePack`.
- blueprint 최상위 필드: `schema_version=1`, `range='0909-1019'`, `slug='Midterm_Practice_01'`, `style='exam'`, `exam_hint`, `scope`, `sources`, `questions`.
- `sources`는 `id/path/sha256` 목록이다. `questions`는 순서대로 `id/kind/subparts/origin_kind/origin_ref/theory_refs/course_evidence/assumptions`를 가진다. references는 source ID와 실제 PDF 쪽(1 기준) 또는 STT 줄 범위를 참조한다. `kind`는 표의 두 값, `origin_kind`는 `homework_variant|textbook_variant|theory_application`이다.
- 테스트 fixture `repo`는 발견한 실제 저장소 절대 Path, `output`은 OUT 절대 Path, `blueprint`는 실제 blueprint.json을 읽은 dict다. 변형 검사는 deepcopy 또는 tmp_path에 복사한 자료에서만 수행한다. 이후 Task도 이 fixture를 사용한다.

```python
def test_blueprint_scope_and_split(blueprint, repo):
    from copy import deepcopy
    from collections import Counter
    assert validate_blueprint(blueprint, repo) == []
    assert [q['id'] for q in blueprint['questions']] == [f'p{i}' for i in range(1, 11)]
    assert Counter(q['kind'] for q in blueprint['questions']) == {'homework_variant': 5, 'model_analysis': 5}
    bad = deepcopy(blueprint)
    bad['questions'].pop()
    assert validate_blueprint(bad, repo)
```

- [x] **Step 1: 자료를 읽어 blueprint 초안을 저작한다.** PDF 행렬·그림·예제 경계는 렌더링해서 대조하고 source SHA-256을 저장한다. 과거 문서만으로 주제·쪽수를 확정하지 않는다.
- [x] **Step 2: 실패해야 할 입력 검사 테스트를 작성한다.** `test_blueprint_scope_and_split`: 정상 fixture의 IDs는 p1–p10, 두 kind 개수는 각각 5, 범위는 0909-1019; 9문항·6:4·범위 밖 자료를 허용한 fixture는 모두 오류. `test_origin_mismatch_and_unicode_paths`: NFC/NFD 동등 경로는 같은 실제 파일을 찾고, 카드 출처/blueprint 불일치·참조 해시 불일치는 거부.
- [x] **Step 3: 테스트의 실패를 확인한다.** `uv run --with pytest python -m pytest '중간고사대비/예상문제_1회/.pack/tools/tests/test_exam.py' -q` → 새 어댑터 부재로 실패해야 한다.
- [x] **Step 4: 위 인터페이스를 구현한다.** `load_exam_source`는 기존 `read_cards(..., EXAM)`와 `normalize_cards`, `mpe_source.subparts`로 `Problem`들을 만들고 `SourcePack('exam', range, slug, path, sha256, problems)`을 반환한다. 카드/blueprint ID·출처·소문항 일치를 확인하고 오류를 예외로 반환한다. 경로는 repo 내부로 제한한다.
- [x] **Step 5: 테스트를 통과시키고 범위표를 내용 검토한다.** 같은 명령 → PASS. 실제 수업 안에서 각 문항을 풀 수 있고 공식 시험의 세부 출제라고 표현하지 않았는지 확인한다.

### Task 2: 10문항·참고 해설 저작과 블라인드 검산

**Files:** Create `OUT/.pack/cards/p1.html` … `p10.html`, `OUT/.pack/evidence/`, `TOOLS/check_exam.py`; Update blueprint·tests.

**Interfaces:**
- Consumes: Task 1의 출제표와 EXAM 입력 계약.
- Produces: 문항별 `article.card#pN`; `exam_adapter.assemble_cards(card_dir: Path, target: Path) -> Path`; `check_exam.validate_cards(cards_path: Path, blueprint_path: Path, repo: Path) -> list[str]`; `evidence/answer-checks.json`의 소문항별 method/conclusion/evidence.
- 카드에는 `.problem` 직계 `.conditions`와 `.ask`, `(a)` 등 일치하는 소문항 표지를 둔다. 기존 파서가 요구하는 `.original`과 `.hint`는 내용 없는 구역으로 두고 `.solution > .steps` 및 `.answer`에 참고 답을 쓴다. 재사용한 짧은 원문이 필요한 경우에만 original을 채운다.
- 실제 문항 조각 저작 후 제작 원본을 조립해 검사한다. `answer_checks` fixture는 evidence/answer-checks.json의 `items` 사전이며 key는 `pN:a` 같은 소문항 ID다. `pack`은 Task 1의 `load_exam_source`로 읽는다.

```python
def test_subparts_and_blind_input(pack, answer_checks, output):
    expected = {f'{p.id}:{s}' for p in pack.problems for s in p.subparts}
    assert set(answer_checks) == expected
    assert all(item['status'] == 'pass' for item in answer_checks.values())
    text = (output / '.pack/evidence/blind-input.html').read_text()
    root = parse(text)
    assert not list(root.find_all(lambda n: bool(n.classes & {'solution', 'answer', 'hint'})))
    assert len(list(root.find_all(lambda n: 'problem' in n.classes))) == 10
```

- [x] **Step 1: 카드·검산 계약의 실패 테스트를 작성한다.** `test_subparts_and_blind_input`: (a)–(c) 중 (c) 검산이 빠지면 오류; blind-input에는 조건·질문·그림만 있고 `.solution/.answer/.hint` 및 풀이 데이터가 없어야 한다. `test_unresolved_answer_blocks_delivery`: 검산 fail/disputed는 완료 불가.
- [x] **Step 2: Task 1의 pytest 명령으로 새 검사 실패를 확인한다.** 기존 PASS와 새 검사 FAIL을 구분한다.
- [x] **Step 3: 10개 카드를 저작하고 `assemble_cards`·`validate_cards`를 구현한다.** assemble_cards는 p1–p10을 순서대로 section 안에 넣은 읽기용 HTML을 임시 target에 만들어 검사/블라인드 입력의 기준을 제공한다. Task 3은 이 조립 함수를 그대로 사용하고 화면 템플릿만 붙인다. 과제와 수치는 바꾸되 손계산 가능한 작은 정수·유리수 위주로 정한다. 공분산 분모 N/N-1, prior 평균·공분산, 잡음분산, 절편 prior, full-column-rank/가역성 조건을 필요한 문제에 명시한다. p8은 사후 평균·분산 후 관측값 예측의 잡음항, p9는 prior로 평균한 evidence와 prior odds를 구분한다.
- [x] **Step 4: 문제만으로 독립 풀이를 수행한다.** 새 검산자에게 `evidence/blind-input.html`과 허용 이론 자료만 전달한다. Native 방식에서도 이 독립 검산은 별도 검토자로 수행한다. 참고 풀이·정답·설명 조각·작성 대화는 전달하지 않는다. 문항별 원답과 독립 결과를 컨트롤러가 대조한다.
- [x] **Step 5: 수학 결과를 별도 검산한다.** Fraction/행렬 연산/상징 유도를 사용한다. `Φᵀ(y−Φθ)=0`, 정규방정식, 가우시안 정규화/공분산, 투영의 `Pᵀ=P`, `P²=P` 등 해당 문항의 불변식을 확인한다. 일반 증명은 수치 예시만으로 승인하지 않는다.
- [x] **Step 6: 전체 소문항 검산과 테스트를 통과시킨다.** pytest → PASS; 실제 `answer-checks.json`은 소문항 집합과 정확히 같고 충돌 0. 문제를 수정하면 해당 블라인드 검산·후속 산출물을 새로 검증한다.

### Task 3: 원본 조립과 기존 양식의 PDF 쌍 제작·발행

**Files:** Create `TOOLS/build_exam.py`, `OUT/STEM.html`, PDF 쌍, `.pack/evidence/pdf-validation.json`; Update tests.

**Interfaces:**
- Consumes: Task 2 카드·검산과 `assemble_cards(card_dir, target)`, 기존 `review-template.html`, `build_pack(review_path, layouts_path, build_dir, *, layout, profile) -> BuildResult`.
- Produces: `build_exam.build_base(repo: Path, output: Path, run: Path) -> dict`; dict keys=`source/problems_pdf/answers_pdf/pdf_validation`(Path). `build_exam.py base --repo PATH --out PATH --run PATH` 진입점.
- `base_result` fixture는 별도 임시 RUN에서 build_base를 실행한 반환 dict다. PDF 검사는 실제 실행에서만 수행하며 빠른 어댑터 검사와 분리한다.

```python
@pytest.mark.pdf
def test_pdf_pair_and_page_mapping(base_result):
    report = json.loads(base_result['pdf_validation'].read_text())
    for mode, key in [('problems', 'problems_pdf'), ('answers', 'answers_pdf')]:
        assert set(report['pages'][mode]) == {f'p{i}' for i in range(1, 11)}
        assert all(report['pages'][mode].values())
        with fitz.open(base_result[key]) as doc:
            assert all(tuple(page.rect)[2:] == (1440.0, 810.0) for page in doc)
```

- [x] **Step 1: 실패 테스트를 작성한다.** `test_problem_payload_has_no_solution_or_hint`: 문제지 모드의 풀이·정답·힌트가 0이고 문항 조건·질문 수는 10. `test_pdf_pair_and_page_mapping`: 모든 페이지 크기는 1440×810pt이고 모드별 논리 ID 집합은 p1–p10; 길어진 p8/p10 fixture의 계속 페이지도 같은 논리 ID에 속한다.
- [x] **Step 2: pytest로 새 검사 실패를 확인한다.** PDF 실검사는 `pdf` marker로 분리하고 처음에는 실행기 부재를 확인한다.
- [x] **Step 3: `build_base`를 구현한다.** 기존 review 템플릿의 스타일/동작을 재사용해 카드 원본을 조립한다. EXAM profile을 전달해 PDF를 만든다. 템플릿 세 SHA를 `pdf-template-provenance.json`과 대조하고 실행 중 고정한다. 첫 PDF 저작 직전에 PDF 스킬의 artifact marker를 한 번 수행한다. 기존 분할·측정·흰 하단 여백 검사를 유지한다.
- [x] **Step 4: 실제 PDF를 생성한다.** `uv run --with playwright --with pymupdf python '중간고사대비/예상문제_1회/.pack/tools/build_exam.py' base --repo . --out '중간고사대비/예상문제_1회' --run 'tmp/ml-midterm-practice/<고유ID>'` → source 및 PDF 둘의 검증 보고서가 생겨야 한다. 사용자에게 없는 페이지 수를 미리 약속하지 않는다.
- [x] **Step 5: PDF 전 페이지를 눈으로 검수한다.** PNG로 렌더링해 문제·해설의 행렬·긴 수식·계속 페이지·글자 크기·필기 공간·공백 페이지와 정답 노출을 확인한다. pytest의 pdf marker 검사도 PASS여야 한다. 문제가 있으면 카드/레이아웃 입력을 고치고 다시 생성한다.
- [x] **Step 6: 검증된 기본 원본과 PDF 쌍을 발행한다.** 기존 `publish_files`로 정확한 대상만 교체하고 백업/롤백을 유지한다. 링크 대상인 `OUT/STEM.html#pN`이 실제로 존재하는 상태를 만든다. 설명이 아직 없으므로 전체 완료로 보고하지 않는다.

### Task 4: 전 문항 문제설명과 최종 검증·전달

**Files:** Create 설명 HTML/MD·자료, `OUT/.pack/explanations/pN.html`, `.pack/제작검증.md`, `.pack/delivery.json`; Update `build_exam.py`, `check_exam.py`, tests.

**Interfaces:**
- Consumes: 최종 발행 원본에 대한 `load_exam_source`, 기존 `build_explanation(pack, fragments, stage, repo) -> Artifacts`, `initial_reviews`, `artifact_hashes`, `publish_explanation`.
- Produces: `build_exam.build_explain(repo: Path, output: Path, run: Path) -> dict`(keys=`pack/artifacts/review_path`); `check_exam.check_delivery(output: Path, repo: Path) -> list[str]`; `build_exam.py explain --repo PATH --out PATH --run PATH`; `check_exam.py --out PATH --repo PATH`(오류 0이면 exit 0).
- `reviewed_explanation` fixture는 실제 Task 4 검토 후의 `pack/fragments/reviews` tuple을 읽는다. 아래 거부 검사는 복사한 검토 기록을 사용하고 실제 승인 파일을 변경하지 않는다.

```python
def test_unreviewed_subpart_rejected(reviewed_explanation):
    from copy import deepcopy
    pack, fragments, reviews = reviewed_explanation
    assert validate_reviews(pack, fragments, reviews) == []
    bad = deepcopy(reviews)
    key = next(iter(bad['independent']['items']))
    bad['independent']['items'][key]['status'] = 'not_run'
    assert validate_reviews(pack, fragments, bad)
```

- [x] **Step 1: 실패 테스트를 추가한다.** `test_stale_source_and_reviews_rejected`: 실제 참조/입력/blueprint/조각 하나가 바뀌거나 소문항 하나가 not_run이면 발행 거부. `test_final_links_and_complete_pair`: PDF 하나·HTML 하나·원문 anchor 하나가 없어도 delivery 오류. 브라우저 테스트 이름은 `test_all_topics_and_responsive_panels`; 전체 10문항과 각 요약/소문항을 검사한다.
- [x] **Step 2: pytest로 새 검사 실패를 확인한다.** 원본 SHA 불일치는 검토 승인 전과 발행 직전 모두 재현한다. 브라우저/PDF 검사는 별도 marker로 필요한 환경에서 실행한다.
- [x] **Step 3: 설명 10개를 저작한다.** `ml-problem-explain/references/authoring.md`와 `verification.md`를 전체 읽는다. 일곱 구역과 모든 solve/verify 소문항 표지, 숨김 sum을 작성하고 recall에 단서·개념·공식·기호·적용 조건·선택 이유를 연결한다. 우측 요약에 핵심 개념·공식과 적용 조건을 남긴다.
- [x] **Step 4: `build_explain`과 `check_delivery`를 구현한다.** 입력 어댑터로 SourcePack을 만든 뒤 기존 build/check API를 직접 사용한다. 기존 `mpe_cli.build`와 같은 방식으로 evidence·현재 artifact hashes·initial_reviews를 연결하되 새 review의 네 단계는 not_run으로 시작한다. blueprint와 그 안의 모든 실제 참조 파일을 review.references에 path/SHA로 결합해 blueprint만 바뀌어도 과거 승인을 거부한다. 코드가 임의로 검토 pass를 생성하지 않는다. validation.json은 자기 해시/소유 파일 집합에 넣지 않는다.
- [x] **Step 5: 설명 stage를 조립하고 실제 네 검토를 수행한다.** Task 3과 같은 실행 환경의 `build_exam.py explain ...`로 stage 생성 → `check_artifacts`/`validate_fragment` 오류 0. 원문 PDF 시각 대조, 전 소문항 내용 검토, Task 2 독립 결과 대조, 실제 브라우저 검토 후 review.json을 기록한다. 읽은 참조의 그림까지 path/SHA를 남긴다.
- [x] **Step 6: 브라우저와 최종 링크를 검증한다.** 1280×900·1024×900·375×812 및 light/dark에서 모든 문항을 확인한다. 1023→1024 경계·목차·이전/다음·요약·문제 패널·모바일 접힘·원문 탭·인쇄를 검사한다. 콘솔/KaTeX 오류·외부 요청·누락 자원·문서 가로 넘침·소문항 표지 중복·요약 수식 중복은 0. 최종 목적지 기준 PDF/원문 링크도 별도 확인한다.
- [x] **Step 7: 승인된 설명만 발행한다.** `publish_explanation`에 현재 SourcePack/Artifacts/fragments/reviews/목적지/고유 백업 경로를 넘긴다. 변경된 hash나 미검토가 있으면 재검토한다. 설명 실패 시 기본 PDF 쌍은 보존하고 “기본 문제 자료 생성됨 / 문제설명 보류”로 보고한다.
- [x] **Step 8: 최종 전체 검증과 전달을 완료한다.** `uv run --with pytest --with playwright --with pymupdf python -m pytest '중간고사대비/예상문제_1회/.pack/tools/tests/test_exam.py' -q` → 전 검사 PASS. `uv run --with pymupdf python '중간고사대비/예상문제_1회/.pack/tools/check_exam.py' --out '중간고사대비/예상문제_1회' --repo .` → exit 0, 10문항/5:5/전 소문항/두 PDF/설명 HTML/현재 해시/검토·링크 일치. 제작검증.md에 실제 페이지 수·근거·검토·백업을 기록하고 사용자에게 세 결과물 링크를 제공한다.

## 커밋 경계

사용자가 별도로 커밋을 요청한 경우에만 Task 1(입력·근거), Task 2(문항·검산), Task 3–4(검증된 납품)를 검토 가능한 단위로 묶는다. 각 커밋 전 정확한 파일만 staging하고 `git diff --cached --check`와 staged diff를 확인한다. 예시 메시지는 `feat(study): add midterm practice source adapter`, `docs(study): author ten midterm practice questions`, `docs(study): publish verified midterm practice pack`이다. tmp·환경·캐시·비밀정보·무관한 변경은 staging하지 않는다. 이 계획만 작성한 턴에는 커밋하지 않는다.

## 계획 자체 점검

- 명세 대응: 출제 근거/5:5/범위는 Task 1, 문항·난이도·수학 조건은 Task 2, 기존 PDF 양식은 Task 3, 전 소문항 설명·화면·납품은 Task 4가 담당한다.
- 인터페이스: EXAM → SourcePack → 기존 build/check/review/publish API 순서다. 기존 CLI가 exam을 인식한다고 가정하지 않는다.
- Review Focus 다섯 항목은 각 소유 Task의 검사와 실제 검토로 연결했다. 합성 테스트 성공을 수학·시각 검증 완료로 간주하지 않는다.
- 코드 구현·자료 생성은 아직 수행하지 않았다. 이 문서의 체크박스는 실행 진행 상황에 따라 갱신한다.
- 권장 실행 방식은 Native다. 하나의 출제표와 동일 문항을 PDF·설명에 계속 연결하므로 작성 문맥을 유지하고, 블라인드 검산과 최종 검토만 별도 검토자로 분리하는 편이 적합하다.

## Native 실행 결과 (2026-10-19)

4개 Task 완료. 예상문제_1회에 문제·해설 PDF 각10쪽과 전10문항31소문항 문제설명 HTML을 발행했다. 독립 검산, 24개 정확/상징 검산, 실제60개 브라우저 조합, PDF 전쪽/변경쪽 렌더링을 확인했다. 별도 최종 검토의 Important2개(Φ 및 unscaled NLL 명시 누락)는 회귀 검사의 실패를 확인하고 한 번의 수정 작업으로 보완했다. 상세 근거는 생성 폴더 .pack/제작검증.md 및 evidence/final-review.md에 보존한다. 커밋·푸시는 수행하지 않았다.
