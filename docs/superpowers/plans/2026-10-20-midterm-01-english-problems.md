# 예상문제 1회 영어 본문·영어 문제지 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 예상문제 1회 전체 10문항·42개 소문항에 과제1 문체의 영어 본문을 추가하고, 같은 본문으로 영어 전용 PDF와 해설 HTML의 원문 탭을 제공한다.

**Architecture:** 문항별 `.original`을 영어 본문의 단일 원본으로 사용하고 기존 EXAM/MPE 어댑터와 원문 탭을 재사용한다. 영어 문제지의 입력 변환·표제 번역·렌더링은 이번 팩의 로컬 모듈에 두며 공용 생성기는 수정하지 않는다. 한국어 PDF는 바이트를 보존하고 제작 당시 입력 스냅샷과 현재 한국어 내용의 동일성을 별도로 검증한다.

**Tech Stack:** Python 3.10+, dataclasses, 기존 EXAM/MPE API, 기존 PDF paginator·KaTeX·Pretendard·16:9 CSS, Playwright/Chrome, PyMuPDF, pytest, Poppler.

**Execution:** 2026-10-20 사용자의 Native 실행 승인으로 구현했다. 세부 검증·독립 검산·최종 검토 및 보존 기록은 대상 팩의 `.pack/제작검증.md`와 `.pack/evidence/native-execution.md`에 보관한다.

**Spec:** 이 문서의 [확정 설계](#확정-설계). 2026-10-20 대화의 grill-yourself 설계를 함께 보존한다. 미응답 결정 #8은 해당 스킬의 기본값 확정 규칙에 따라 **기존 16:9 가로형 [confirmed by default]**으로 채택한다. 이번 요청은 계획 작성이며 구현 착수 승인은 아니다.

## Global Constraints

- 대상은 `중간고사대비/예상문제_1회`의 p1~p10이다. 소문항 수는 `[3,3,3,3,3,5,6,6,5,5]`, 합계 42개다.
- 영어화로 수치·수식·가정·소문항 순서·참조·난이도·요구 결과를 바꾸지 않는다. 새 힌트·풀이·배점·시험시간은 넣지 않는다.
- 영어 문체는 `과제/과제1/26_10_Introduction_to_Machine_Learning_homework1_rev.pdf`의 `Let`, `Consider`, `Compute`, `Find`, `Derive`, `Show that`, `Explain` 및 `Problem N`/`(a)` 구조를 따른다.
- 문체만 과제1을 따른다. 과제1의 열 gradient 약속을 복사하지 않는다. 현재 예상문제의 행 gradient, 열 parameter vector, Gaussian 둘째 인수=분산 약속을 유지한다.
- 영어 PDF 파일명은 `중간고사예상_0909-1019_Midterm_Practice_01-문제-English.pdf`다. 본문·제목·표제·계속 표시·머리말·실제 출력되는 안내는 영어로만 표시한다. 파일명은 위 값을 유지한다.
- 판형은 `video-16x9`, 1440×810pt다. 하단 135pt(180 CSS px)는 기존과 같이 흰 여백이다. 영문이 길면 소문항 경계에서 분할하고 작은 글자로 밀어 넣지 않는다.
- 한국어 문제·답안 PDF, 한국어 조건·질문·참고 풀이·해설 조각·출제 근거·용어와 패널 배치 기본값을 보존한다. 원 문제 HTML은 영어 본문 추가에 필요한 부분만 변경한다.
- 원문 탭은 문제 패널의 `문제 → 원문 → 출제 근거 → 용어` 순서다. 사용자의 우측 배치 설정을 유지하며 요약 패널에 탭을 중복 생성하지 않는다.
- 영어 PDF와 원문 탭은 같은 영어 본문을 사용한다. 공유 스킬·템플릿 파일과 예상문제 2회는 수정하지 않는다. 공용 함수를 monkey-patch하지 않는다.
- 검토 기록은 실제 확인한 결과만 쓴다. 변경된 입력에 과거 pass나 새 해시만 덮어씌워 승인하지 않는다. 오래된 원본·본문·PDF·검토 해시는 거부한다.
- 커밋·푸시는 현재 요청 범위에 없다. 아래 작업 단위마다 diff를 검토하되 자동 커밋하지 않는다. 사용자가 별도로 커밋을 요청한 경우에만 해당 작업 파일을 명시해 커밋한다.

## Review Focus

1. 번역에서 분산/정밀도·행/열 gradient·절편 prior·미래 잡음 독립 조건이 달라질 수 있다. Task 1의 42항목 의미 대조와 변조 fixture로 잡는다.
2. 영어 본문이 원문·조건·질문에 중복되거나 한국어 표제·정답이 PDF에 남을 수 있다. Task 2의 payload/렌더 결과 검사와 실제 PDF 문자 검사가 담당한다.
3. p7~p10의 긴 영어 소문항을 분할할 때 (d)가 (a)로 바뀌거나 빠질 수 있다. Task 2의 실제 Chrome 계속 페이지 검사로 순서·표지를 확인한다.
4. 모바일에서 탭을 검사하기 전에 문제 패널이 접혀 있거나, 원문 탭 선택 후 문항을 바꾸면 다른 문항 본문이 남을 수 있다. Task 4에서 펼침·탭 선택·문항 이동·저장 상태를 확인한다.
5. 원문 추가로 전체 HTML 해시가 바뀔 때 한국어 PDF 검증을 생략하거나 과거 승인에 새 해시만 붙일 수 있다. Task 3의 스냅샷/내용 동일성 검사 및 Task 5의 새 발행 검토로 막는다.

---

## 확정 설계

기존 문제를 영어로 읽고 푸는 연습 자료다. 영어 본문은 예상문제의 새 영문판이며 공식 중간고사 원문이라고 표시하지 않는다. 해설과 영어 PDF는 한 묶음의 동일 데이터 흐름이므로 하나의 계획으로 다룬다.

기존 구현에서 확인한 연결 지점:

- `OUT/문제설명_0909-1019_Midterm_Practice_01.html:548–559`에 원문 탭이 이미 있고, 1386–1387행에서 `details.original`을 등록한다. 1411–1426행에서 표시, 1683–1693행에서 키보드 순서를 처리한다.
- `.agents/skills/ml-problem-explain/scripts/mpe_render.py:156–158`은 `Problem.original_html`이 비어 있지 않으면 원문 영역을 생성한다. HTML 직접 패치 대신 원본 카드로 재생성한다.
- `TOOLS/exam_adapter.py:62–64`는 `original_html`을 이미 전달한다. `mpe_source.subparts(ask, original)`의 소문항 대응 계약을 유지한다.
- `TOOLS/build_exam.py`의 `base`는 한국어 PDF 두 개를 다시 발행하므로 이번 제작에 호출하지 않는다. `styled_source`로 HTML만 stage에서 조립하고, 영어 PDF는 별도 경로에서 만든다.
- 공용 `review_pdf_payload.to_workbook`은 `.original`과 한국어 조건/질문을 모두 출력하고 `(계속)`을 붙인다. 공용 PDF 템플릿에는 `문제 원문`, `조건`, `구할 것`이 고정돼 있다. 영어 입력·표제 변환이 모두 필요하다.
- `TOOLS/browser_check.py:26`은 원문 탭이 숨겨진다고 가정한다. `TOOLS/check_exam.py:48–49`는 현재 HTML의 전체 해시를 한국어 PDF 제작 원본 해시와 비교한다. 두 검사를 이번 계약에 맞게 확장한다.

### 파일 구조와 책임

이하 경로 약어는 저장소 루트 기준이다. 명령은 루트의 PowerShell에서 실행한다.

```powershell
$examOut = '중간고사대비/예상문제_1회'
$examTools = "$examOut/.pack/tools"
$examStem = '중간고사예상_0909-1019_Midterm_Practice_01'
$examRun = 'tmp/midterm-01-english-20261020'
```

| 파일 | 변경과 책임 |
|---|---|
| `OUT/.pack/cards/p1.html`~`p10.html` | 기존 `.original`에 영어 제목·조건·질문 저작 |
| `TOOLS/english_source.py` | 영어 본문 추출·검증, 영어 전용 NormalizedProblem과 payload 생성 |
| `TOOLS/english_pdf.py` | 영어 템플릿 어댑터·실측 분할·영어 PDF와 검증 보고서 stage 생성 |
| `TOOLS/pdf_binding.py` | 한국어 PDF의 과거 입력과 현재 한국어 내용 동일성 검증 |
| `TOOLS/build_exam.py` | `english` 명령과 stage 전용 영어 빌드 연결; 기존 base/explain 명령 보존 |
| `TOOLS/browser_check.py` | 원문 탭·전체 영어 본문·접근성·모바일 동작 검사 확장 |
| `TOOLS/check_exam.py` | 기존 발행 검사에 영어 PDF·한국어 PDF 보존 검증 통합 |
| `TOOLS/tests/conftest.py` | 기존 pytest marker 유지와 로컬 tools import 경로 설정 |
| `TOOLS/tests/test_english_source.py`, `test_english_pdf.py`, `test_pdf_binding.py` | 세 로컬 모듈의 동작·실패 조건 검증 |
| `TOOLS/tests/test_exam.py` | 영어 최종 배포물·원문 탭 검토 기록의 통합 검사 추가 |
| `OUT/STEM.html` | 영어 본문이 포함된 원 문제 HTML 재조립 |
| `OUT/STEM-문제-English.pdf` | 새 영어 전용 문제지 |
| `OUT/문제설명_0909-1019_Midterm_Practice_01.html` | 원문 탭이 활성화된 해설 |
| `OUT/.pack/문제설명_0909-1019_Midterm_Practice_01.md` 및 렌더러 소유 자료 | HTML과 함께 재생성; 경로는 `mpe_render.names/md_name`으로 결정 |
| `OUT/.pack/evidence/english-content-review.md` | 42행 한영 의미 대조표·문체 검토 |
| `OUT/.pack/evidence/english-pdf-validation.json` | 영어 입력·PDF 해시, 페이지 대응·언어·geometry·시각 검토 결과 |
| `OUT/.pack/evidence/korean-pdf-source/STEM.html` | 변경 전 HTML의 바이트 스냅샷; 한국어 PDF 제작 원본 증거 |
| `OUT/.pack/evidence/korean-pdf-binding.json` | 스냅샷·기존 보고서·현재 한국어 내용·PDF 해시 연결 |
| 기존 `.pack/evidence` 검토·`delivery.json`·`제작검증.md` | 새 stage의 실제 검토와 최종 해시 반영 |

`OUT/STEM-문제.pdf`, `OUT/STEM-답안.pdf`, 기존 `pdf-validation.json`은 바이트를 변경하지 않는다. 새 실행의 backup·스냅샷 후보·렌더 PNG는 RUN에 둔다. 위 `OUT`, `TOOLS`, `STEM`, `RUN`은 각각 `$examOut`, `$examTools`, `$examStem`, `$examRun`을 뜻한다.

### 데이터 계약

각 카드의 `.original`에 `lang="en"`을 지정하고 다음 세 요소를 정확히 하나씩 둔다. 영어 제목은 주제명만 담고, 번호는 PDF/원문 표시 문맥에서 붙인다.

```html
<div class="original" lang="en">
  <h4 data-english-title>Linear Combinations and Uniqueness of Solutions</h4>
  <div data-english-conditions><p>Let ...</p></div>
  <div data-english-ask><ol type="a"><li data-english-part="a">Determine ...</li></ol></div>
</div>
```

영어 질문은 한국어 소문항과 일대일 대응하는 하나의 최상위 `ol`이다. 각 `li`의 `data-english-part`는 `a`, `b`, … 순서로 중복 없이 지정하고 기존 한국어 `subparts`와 순서까지 비교한다. 중복 `.part` 표지를 만들지 않는다. LaTeX 기호와 수식은 원래 표기를 유지하며 문장 속 영문 교차 참조는 `part (a)`처럼 쓴다. 표지만 같은 잘못된 번역이나 수식 문자열의 단순 집합 비교는 실제 의미 검토를 대신하지 않는다.

## Task 1: 영어 본문 저작과 단일 원본 어댑터

**Files:** Create `TOOLS/english_source.py`, `TOOLS/tests/test_english_source.py`, `OUT/.pack/evidence/english-content-review.md`; Modify `TOOLS/tests/conftest.py`, `OUT/.pack/cards/p1.html`~`p10.html`.

**Interfaces:**
- Consumes: `exam_adapter.load_exam_source(cards_path, blueprint_path, repo) -> SourcePack`, `read_cards(path, EXAM)`, `mpe_source.subparts(ask, original) -> tuple[str, ...]`.
- Produces: `load_english_problems(source: Path, blueprint: Path, repo: Path) -> tuple[NormalizedProblem, ...]`; `english_payload(problems: tuple[NormalizedProblem, ...], pages: list[PageSlice] | None = None) -> dict`.
- 반환 객체의 필드·타입은 기존 `NormalizedProblem/ReviewCard` 계약이며 본문만 영어로 변환한다.

- [x] **Step 1:** 실행 환경·작업 상태를 기록하고 기존 한국어 PDF 2개, HTML, 카드, 해설 조각, 기존 PDF 검증 보고서를 RUN/backup에 복사한다. Python은 3.10 이상이며 필요한 의존성을 import할 수 있어야 한다. 루트 `.env`는 읽거나 출력하지 않는다. 변경 전 HTML 해시가 기존 보고서의 `source_sha256`과 같아야 다음 단계로 간다.
- [x] **Step 2:** `test_english_source.py`에 fixture 기반 실패 테스트를 작성한다. `test_missing_duplicate_or_empty_english_fields_rejected`, `test_subpart_count_and_order_rejected`, `test_english_payload_excludes_korean_original_hints_and_solutions`를 정의한다. 유효 fixture는 IDs p1~p10, 위 42개 구성을 반환해야 하며 누락·중복·빈 조건/질문·한글 본문·다른 소문항 표지를 `ValueError`로 거부한다. payload에는 `html.original == ''`, `hints == []`, `solution` 키 없음, 영어 조건/질문 1회만 있어야 한다. conftest에 `Path(__file__).resolve().parents[1]`을 sys.path에 추가하여 테스트 파일 수집 순서와 무관하게 tools 모듈을 import하도록 한다. 기존 marker는 유지한다.

  핵심 assertion은 다음과 같다. 각 테스트는 임시 디렉터리에 10문항의 유효 영어 fixture를 만들고 검사 대상을 한 필드씩 변조한다. 영어 field marker 구조는 위 데이터 계약을 사용하며 fixture도 실제 EXAM ID/출처/blueprint 계약을 만족해야 한다.

  ```python
  problems = load_english_problems(source, blueprint, repo)
  assert [p.card.id for p in problems] == [f'p{i}' for i in range(1, 11)]
  assert [len(subparts(p.ask_html, '')) for p in problems] == [3,3,3,3,3,5,6,6,5,5]
  payload = english_payload(problems)
  assert all(p['html']['original'] == '' and p['hints'] == [] and 'solution' not in p for p in payload['problems'])
  with pytest.raises(ValueError):
      load_english_problems(source_with_reversed_part_markers, blueprint, repo)
  ```
- [x] **Step 3:** `python -m pytest "$examTools/tests/test_english_source.py" -q` 실행. 새 API 부재로 FAIL인지 확인한다.
- [x] **Step 4:** 두 API를 구현한다. 기존 `NormalizedProblem/ReviewCard`를 `dataclasses.replace`로 변환하며 원문에서 뽑은 영어 조건·질문·제목만 채운다. `original_html`, hint, steps, answer를 비우고 ID·출처 식별은 유지한다. payload의 kind=`Practice`, number=`Problem N`/`Problem N (continued)`, section=`Midterm Practice 01`, meta.title=`Introduction to Machine Learning - Midterm Practice 01`로 고정한다. 빈 필드나 한글이 있으면 문항 ID와 오류를 반환하고 fallback 번역을 만들지 않는다.
- [x] **Step 5:** 기존 과제1 원본과 현재 10문항을 읽어 세 필드를 저작한다. 영어 표준 안내는 `Show your calculation and derivation steps. All parameter vectors are column vectors; write gradients as row vectors. Unless stated otherwise, the second parameter of a univariate Gaussian is its variance.`로 한다. 이 공통 안내는 PDF 첫 페이지에 한 번, 필요 문항의 행 gradient·분산 가정은 해당 영어 본문에도 유지한다.
- [x] **Step 6:** 42행 의미 대조표를 작성한다. 각 행에 한국어 요구·영어 대응·수치/조건·교차 참조·검토 결과를 기록한다. p3의 정규화, p4/p7의 절편 prior, p5의 분모 3/무상관과 독립, p8의 미래 잡음 독립·두 예측분산, p9의 prior 적분, p10의 모든 h/유클리드 내적을 명시적으로 대조한다. 자동 검사는 필드/라벨만 보증하며 이 표는 실제 독해 검토다.
- [x] **Step 7:** 같은 테스트와 `python -m pytest "$examTools/tests/test_row_convention.py" -q`를 실행해 PASS를 확인한다. 한국어 조건·질문·해설/정답 조각의 변경이 없음을 backup과 대조하고 diff를 검토한다.

## Task 2: 영어 전용 16:9 PDF 생성

**Files:** Create `TOOLS/english_pdf.py`, `TOOLS/tests/test_english_pdf.py`; Modify `TOOLS/build_exam.py`의 `main`과 명령 dispatch; Create RUN의 영어 PDF stage/검증 보고서.

**Interfaces:**
- Consumes: Task 1의 두 API; `review_pdf_pages.paginate(problems, 'problems', measure) -> list[PageSlice]`; `review_pdf_layout.load_template`, `review_pdf_payload.inject_data`; 기존 `RenderReport`, `Typography`.
- Produces: `english_template(repo: Path, layout: Layout) -> str`; `render_english(repo: Path, payload: dict, html_path: Path, pdf_path: Path | None = None, *, layout: Layout = 'video-16x9', typography: Typography | None = None) -> tuple[RenderReport, Typography]`; `build_english_pdf(repo: Path, output: Path, run: Path) -> dict[str, Path]`.
- 빌드 반환 키는 `problems_pdf`, `report`다. CLI `build_exam.py english --repo . --out OUT --run RUN`은 stage 경로만 출력한다. 실제 최종 발행은 Task 5에서 수행하며 기존 PDF에 쓰지 않는다.

- [x] **Step 1:** 실패 테스트 `test_english_template_translates_visible_labels`, `test_english_pdf_is_16x9_and_contains_no_korean`, `test_long_english_questions_keep_labels_across_pages`를 작성한다. 템플릿 label은 `Original problem`, `Given`, `Tasks`, 문서 lang은 `en`이어야 한다. 실제 PDF 각 페이지는 1440×810pt, 본문 비어 있지 않음, 한글 `[가-힣ㄱ-ㅎㅏ-ㅣ]` 0개, 하단 135pt 흰색이어야 한다. 긴 p8 fixture는 실제 2페이지 이상, (a)~(f) 질문이 각각 한 번이고 순서가 보존돼야 한다.

  ```python
  assert all((p.rect.width, p.rect.height) == (1440, 810) for p in doc)
  assert not re.search(r'[가-힣ㄱ-ㅎㅏ-ㅣ]', '\n'.join(p.get_text() for p in doc))
  assert all(min(p.get_pixmap(clip=fitz.Rect(0, 675, 1440, 810), alpha=False).samples) == 255 for p in doc)
  assert len(report['pages']['p8']) > 1  # 길이를 늘린 영어 fixture의 실제 PDF 결과
  assert rendered_part_labels == list('abcdef')
  ```
- [x] **Step 2:** `python -m pytest "$examTools/tests/test_english_pdf.py" -q`를 실행해 새 API 부재로 FAIL인지 확인한다.
- [x] **Step 3:** 영어 템플릿/렌더 API를 구현한다. pinned template 해시를 확인한 뒤 메모리의 `load_template('problems', layout)`에서 정확한 표제·문서언어·오류 안내만 영어로 치환하고 각 치환의 예상 개수를 검증한다. CSS와 공용 템플릿은 보존한다. CDN 자원은 저장소의 기존 vendor 파일에 대한 절대 file URI로 바꿔 외부 요청을 0으로 한다. 첫 페이지 공통 안내는 첫 문항 조건 앞에 PDF 표시용으로만 붙인다.
- [x] **Step 4:** `render_english`에서 기존 렌더러의 font/math/resource 대기, `GEOMETRY`, `TYPOGRAPHY` 검사 계약을 재사용한다. 새 로컬 실행 경로에서 동일 영어 template의 a4 실측 결과를 16:9 typography에 적용한다. `pdf_path`가 있을 때 미해결 geometry/resource/math 오류를 거부하고 Chrome PDF를 생성한다. 공유 `_render_document`의 고정 템플릿을 monkey-patch하지 않는다.
- [x] **Step 5:** `build_english_pdf`와 CLI를 연결한다. 영어 NormalizedProblem을 실측 분할하고 매 측정/최종 payload에 같은 영어 어댑터를 적용한다. 최종 출력 텍스트·페이지 geometry·하단 흰 여백을 확인하고, 입력 해시/문항별 영어 본문 해시/PDF 해시/p1~p10 페이지 대응/실제 페이지 ID/오류를 보고서에 기록한다. 출력은 RUN에만 생성한다.
- [x] **Step 6:** 적용되는 PDF 스킬을 읽고 첫 실제 PDF authoring 명령 직전에 artifact-operation 기록을 한 번 수행한다. 테스트용 fixture는 임시 파일이며 사용자 전달물은 영어 PDF 1개다. 기록 도구가 요구하는 값은 현재 스킬 계약에 맞춘다.
- [x] **Step 7:** Step 2 테스트를 다시 실행해 PASS를 확인한다. 영어 본문 문항별 digest는 제목·조건·질문의 canonical HTML 기준으로 기록하며 PDF 표시용 공통 안내와 `space_math` 레이아웃 래퍼를 원본 본문 digest에 섞지 않는다.
- [x] **Step 8:** 긴 fixture를 포함한 실제 PDF를 Poppler로 PNG 렌더링해 전 페이지를 읽고 겹침·잘림·라벨·가독성·필기 공간을 확인한다. 시각 검토 완료 전 report의 최종 상태는 pass로 바꾸지 않는다.

## Task 3: 한국어 PDF 보존과 영어 발행 검증 계약

**Files:** Create `TOOLS/pdf_binding.py`, `TOOLS/tests/test_pdf_binding.py`; Modify `TOOLS/check_exam.py`; Create OUT의 한국어 입력 snapshot과 `korean-pdf-binding.json`.

**Interfaces:**
- Consumes: Task 1 backup, 기존 `pdf-validation.json`, Task 2 보고서.
- Produces: `korean_content_digest(source: Path) -> str`; `check_pdf_binding(output: Path, repo: Path) -> list[str]`; `check_english_delivery(output: Path, repo: Path) -> list[str]` (`check_exam.py`). 성공은 `[]`다.
- 한국어 digest는 `read_cards(source, EXAM)`의 문항 순서와 각 ReviewCard의 모든 필드에서 **original_html만 제외한** canonical JSON의 SHA-256이다. title/source/part/statement/hint/steps/answer/figure ID·HTML·종류를 포함한다. HTML 전체 해시의 임의 대체물이 아니라 보존 판정 전용이다.

- [x] **Step 1:** `test_original_only_change_preserves_korean_pdf_binding`, `test_korean_statement_or_answer_change_rejected`, `test_missing_snapshot_or_changed_pdf_report_rejected`, `test_missing_or_stale_english_pdf_rejected`를 작성한다. original만 바뀌고 모든 한국어 필드가 같으면 `[]`; 조건·정답·문항 순서·기존 PDF·과거 report·snapshot 중 하나가 달라지면 오류가 있어야 한다. 영어 PDF 누락/해시 변경/영어 입력 변경/페이지 대응 누락도 거부한다.

  ```python
  assert korean_content_digest(baseline) == korean_content_digest(original_only_changed)
  assert korean_content_digest(baseline) != korean_content_digest(korean_answer_changed)
  assert check_pdf_binding(valid_output, repo) == []
  assert check_pdf_binding(output_with_changed_korean_pdf, repo)
  assert check_english_delivery(output_with_stale_english_source, repo)
  ```
- [x] **Step 2:** `python -m pytest "$examTools/tests/test_pdf_binding.py" -q`로 FAIL을 확인한다.
- [x] **Step 3:** 두 보존 API를 구현한다. 변경 전 HTML을 `OUT/.pack/evidence/korean-pdf-source/STEM.html`에 보관하며 bytes SHA는 기존 report의 `source_sha256`과 정확히 같아야 한다. binding에는 schema_version=1, snapshot 상대 경로/해시, 기존 report 해시, 현재 HTML 해시, 한국어 digest, 한국어 PDF 두 파일의 해시를 기록한다. 현재 HTML과 snapshot의 digest를 매 검사마다 다시 계산하며, 보고서의 기존 PDF 해시·실제 파일과 함께 모두 일치해야 한다.
- [x] **Step 4:** `check_exam.check_delivery`의 전체 HTML↔한국어 PDF 해시 단일 비교를 조건부로 확장한다. 기존 report와 현재 source hash가 같으면 기존 엄격 검사를 유지한다. 다를 때만 완전한 binding 증거를 요구한다. 영어 버전에서는 새 PDF가 delivery files에 포함되고, 영어 report가 현재 입력·영어 필드·현재 PDF·10문항 전체 페이지 대응을 검증해야 한다. 기존 구조/참조/독립 검토/브라우저 검사는 생략하지 않는다.
- [x] **Step 5:** Step 2를 다시 실행해 PASS를 확인한다. 기존 한국어 report bytes가 backup과 같은지 검사하고 diff를 검토한다. report의 과거 source_sha256을 현재 hash로 덮어쓰는 코드는 없어야 한다.

## Task 4: 해설 재생성과 원문 탭 전체 동작 검증

**Files:** Modify `TOOLS/browser_check.py`, `TOOLS/tests/test_exam.py`; Generate RUN의 source/해설 stage/새 검토 자료. 기존 원문 탭 템플릿 수정 없음.

**Interfaces:**
- Consumes: `build_exam.styled_source(repo, output, stage) -> Path`, `build_exam.build_explain(repo, output, run) -> dict`, Task 1 영어 본문.
- Produces: 기존 `run_check(path, evidence, shots)`의 report에 `original_topic_ids`(p1~p10), `tab_order`(['problem','original','provenance','terms']), `original_checks`(각 viewport/theme/topic의 영어 본문 일치·활성 탭·오류)를 추가한다. 기존 report 필드를 유지한다.

- [x] **Step 1:** `test_exam.py`에 `test_original_tabs_cover_every_english_problem`을 추가한다. 위 세 필드와 3화면×2테마×10문항=60개의 원문 확인, 오류 없음, report의 현재 HTML 해시 일치를 단언한다. 실제 브라우저 검사 전에는 FAIL이어야 한다.

  ```python
  assert report['original_topic_ids'] == [f'p{i}' for i in range(1, 11)]
  assert report['tab_order'] == ['problem', 'original', 'provenance', 'terms']
  assert len(report['original_checks']) == 60
  assert report['errors'] == []
  assert report['html_sha256'] == sha(final_html)
  ```
- [x] **Step 2:** `browser_check.run_check`의 빈 원문 탭 가정을 현재 데이터에 맞게 바꾼다. 모바일은 먼저 문제 보기를 펼친 후 `원문`을 선택한다. 모든 문항에서 영어 제목·조건·42개 질문의 원문 DOM 텍스트가 카드와 같고 다른 문항 원문이 보이지 않는지 확인한다. 한국어 문제 탭은 영어 본문을 포함하지 않아야 한다. 단순 `is_visible`만으로 내용을 검증하지 않는다.
- [x] **Step 3:** 같은 검사에 ArrowLeft/Right/Home/End의 탭 순서, 원문 선택 후 다음/이전/목차 이동, reload 시 탭 선호 유지, 1023→1024 전환, 오른쪽 도킹에서 순서/영문 표시, 왼쪽/float 기존 동작, 인쇄에서 한국어 문제와 영어 원문 모두 보존을 포함한다. 원문 없는 별도 임시 fixture에서는 기존 숨김/fallback 동작도 계속 확인한다. 원래 기본 도킹은 바꾸지 않는다.
- [x] **Step 4:** `styled_source`로 stage HTML을 조립하고 한국어 digest가 snapshot과 같은지 검증한다. 소스 HTML과 vendor 자원만 백업을 거쳐 OUT에 갱신한다. `base` 명령은 호출하지 않는다. `python "$examTools/build_exam.py" explain --repo . --out "$examOut" --run "$examRun/explain"`을 실행해 설명 stage를 생성한다. 기존 `data-problem-panel` 출제 근거/용어와 행 gradient 규칙도 보존됐는지 확인한다.
- [x] **Step 5:** `python "$examTools/browser_check.py" '<explanation-result.json의 html 절대경로>' --evidence "$examRun/browser-check.json" --shots "$examRun/browser-shots"`를 실행한다. 결과는 status=pass, errors=[], 60개 원문 확인이며 overflow/KaTeX/콘솔/누락 자원/외부 요청은 모두 0이어야 한다. 실제 원문 화면을 light/dark·데스크톱·모바일에서 시각 확인한다.
- [x] **Step 6:** 새 입력 해시로 source_visual/content/independent/browser 검토를 수행한다. 현재 `mpe_review_policy.POLICY_VERSION`과 검토 reference 문서를 확인하고 요구 items 전체를 실제 검토한다. independent는 문항·필요한 이론만 본 별도 검산자가 먼저 풀고 작성자가 대조한다. 실행 방식과 무관하게 이 독립 검산 요구는 유지한다. 과거 입력의 pass를 복사하지 않는다. `check_artifacts`, `validate_fragment`, `validate_reviews`가 모두 빈 오류 목록인지 확인한다.

## Task 5: 최종 발행·검증·전달

**Files:** Publish 위 OUT 산출물과 MPE 소유 HTML/MD/자료; Update `.pack/delivery.json`, `.pack/제작검증.md`, 검토·증거 파일; Modify `TOOLS/tests/test_exam.py`의 영어 최종 배포 검사.

**Interfaces:**
- Consumes: Tasks 1~4의 stage 결과와 검토; `mpe_publish.publish_explanation(pack, artifacts, fragments, reviews, destination, backup_dir) -> tuple[Path, ...]`; `review_pdf_publish.publish_files(mapping, backup_dir)`; `check_exam.check_delivery(output, repo)`.
- Produces: 영어 PDF·원문 탭이 있는 해설·완전한 delivery 기록. 기존 한국어 PDF의 SHA-256 2개는 baseline과 동일하다.

- [x] **Step 1:** `test_final_english_pdf_and_original_content_match`를 추가한다. 최종 카드·원 문제 HTML·해설의 `data-original-problem` 10개·영어 report의 문항별 본문 digest가 같고 질문 수가 42개여야 한다. PDF 실물 검사는 제목/전 문항 영어 텍스트와 페이지 매핑을 대조한다. renderer가 삽입한 줄바꿈·KaTeX MathML 때문에 raw innerHTML byte 비교를 요구하지 말고, 원문 필드별 텍스트/TeX를 정규화하여 비교한다.
- [x] **Step 2:** final 경로 발행 전 Task 2 영어 PDF의 전 페이지 시각 검토와 Task 4 현재 stage 검토가 완료됐는지 확인한다. PDF 생성/edit 첫 authoring 명령 전에는 적용되는 PDF 스킬의 artifact-operation 기록 요구를 확인한다. 이미 Task 2에서 기록했다면 중복 기록하지 않는다.
- [x] **Step 3:** 영어 PDF와 그 report, 한국어 snapshot/binding을 `publish_files`로 발행하고, 해설은 `publish_explanation`으로 발행한다. stage 오류 시 기존 파일은 교체하지 않는다. source HTML 변경 후 최종 발행까지 중간 실패한 경우 baseline 백업으로 영향 파일을 복구하여 오래된 해설과 새 source를 완료 상태로 남기지 않는다.
- [x] **Step 4:** 발행된 해설의 browser 검사를 final 경로에서 수행하고 최신 evidence를 기록한다. evidence를 MPE 소유 자료 안에 복사해야 한다면 stage에서 갱신하고 manifest/artifact_hashes를 다시 계산·검증한 뒤 재발행한다. 승인 후 hashed 산출물을 직접 수정하지 않는다. review 자신은 기존 계약대로 자기 해시 집합에서 제외한다.
- [x] **Step 5:** delivery의 source·카드·도구·영어 PDF·보고서·해설·새 증거 해시와 10/42 counts를 갱신한다. 기존 report는 과거 제작 근거로 보존하고 binding을 추가한다. delivery 자신의 해시는 files에 넣지 않는다. `제작검증.md`에 실제 영어 문체/42항목/시각·브라우저/한국어 PDF 보존 결과를 기록한다.
- [x] **Step 6:** 아래 명령을 실행한다. 첫 명령은 `status: pass`, `errors: []`; pytest는 전체 PASS; 마지막 명령은 오류 출력 없음이어야 한다. 의존성·경로 실패를 skip으로 숨기거나 assertion을 완화하지 않는다.

```powershell
python "$examTools/check_exam.py" --out "$examOut" --repo .
python -m pytest "$examTools/tests" -q
git diff --check
```

- [x] **Step 7:** baseline과 최종 한국어 PDF 2개의 SHA-256 및 한국어 조건·질문·풀이·해설 조각을 대조해 보존을 확인한다. `git status --short`와 diff로 이번 팩 외 변경이 없는지 확인하고 최종 전체 변경 검토의 지적을 해결한다. 영어 PDF와 갱신된 해설의 절대경로 링크, 실제 검사 결과를 사용자에게 전달한다.

## 계획 자체 검토

- 사양 대응: 영어 문체/내용 보존은 Task 1, 영어 전용 16:9 PDF는 Task 2, 기존 한국어 PDF 보존·무결성은 Task 3, 기존 원문 탭과 모바일은 Task 4, 최종 동일성/발행은 Task 5가 담당한다.
- Review Focus 5개에 각각 의미 대조·실패 fixture, 영문 payload/PDF 문자 검사, 실제 계속 페이지, 60개 원문 화면·저장/접힘 전환, 원본 바인딩 변조 거부 검사를 배정했다.
- 함수명·반환 키·기존 MPE/NormalizedProblem/PageSlice/RenderReport 타입을 작업 사이에서 통일했다. 공용 PDF renderer에 존재하지 않는 template 인자를 전달하지 않는다.
- 한국어 PDF 재생성 없이 source hash 변화에 대응하고, 새 source에 과거 승인을 재사용하지 않는다. 검토 증거의 자기 해시 순환도 만들지 않는다.
- 계획 작성 단계에서는 이 파일만 생성한다. 구현·영어 본문 저작·PDF 생성·커밋·푸시는 실행 지시 이후다.
