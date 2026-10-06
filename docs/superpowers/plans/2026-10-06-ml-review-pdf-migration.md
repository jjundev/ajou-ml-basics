# 머신러닝기초 복습문제 PDF 마이그레이션 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 7개 날짜 47문항과 향후 머신러닝기초 복습문제를 전자회로2와 동일한 문제·답안 PDF로 제공한다.

**Architecture:** 전자회로2 HTML 템플릿 두 개를 바이트 그대로 과목 로컬 스킬에 보관한다. 저장된 카드 HTML과 조건/질문 분할 데이터에서 템플릿 JSON을 만들고 Chrome으로 렌더링한다. 내용 보존·페이지 넘침·PDF 쌍·노트 링크를 검증한 뒤 배포하며 기존 HTML/Markdown 생성 API는 유지한다.

**Tech Stack:** Python 3.10+ 표준 라이브러리, unittest, Playwright의 설치된 Google Chrome, 기존 KaTeX·Pretendard CDN, PDF QA용 PyMuPDF. 현재 시스템 Python 3.14에서 Playwright·PyMuPDF와 Poppler가 확인되었다. BeautifulSoup·ReportLab·새 브라우저 설치는 필요하지 않다.

**Spec:** /Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/docs/superpowers/specs/2026-10-06-ml-review-pdf-migration-design.md

## Global Constraints

- 난이도와 문항 내용을 유지하고, 행렬 계산·유도·증명을 손으로 풀 수 있는 필기 공간을 마련한다.
- 기존 자료와 앞으로 생성하는 ml-review-pack을 모두 대상으로 한다.
- 기존 대상은 0909/0914/0916/0921/0923/0928/0930, 카드 수 5/7/6/6/7/8/8, 합계 47문항과 PDF 14개다.
- 전자회로2 workbook/templates/problem.html, answer.html을 그대로 복사한다. 생성된 HTML의 __WORKBOOK_DATA__ 치환만 허용한다.
- 파일명은 복습문제_<날짜>_<기존 slug>-문제.pdf / -답안.pdf다. UI에서는 문제지/해설지로 안내한다.
- 기존 HTML·Markdown·figures는 보존하며 정리노트 본문·수식·그림을 재작성하지 않는다.
- 원본 오류는 형식 변환 성공과 구분하여 보고한다. 문제가 발견되면 임의 문제 교체나 조용한 수정 없이 해당 pack의 출판을 보류한다.
- 문제 모드의 payload에는 solution 키나 정답 본문을 넣지 않는다. 증명 대상 식은 질문이므로 유지한다.
- 수식·행렬·표·단일 풀이 단계 내부를 잘라 분리하지 않는다. 한 블록 자체가 들어가지 않으면 실패한다.
- 생성·검사 중에는 별도 build-dir를 사용하고, 두 PDF와 링크가 준비된 후에만 공개 파일을 변경한다.
- 커밋·푸시는 별도 사용자 요청이 있을 때만 실행한다. 아래 커밋 단계는 제안이다.
- 실행 전 using-git-worktrees 절차로 격리를 결정한다. 관찰 시 ML은 codex/ml-review-video였으므로 분기를 재확인하고 영상 작업에 변경을 섞지 않는다.
- .agents/skills/ml-review-pack 심볼릭 링크는 보존한다. 아래 SKILL의 실제 파일은 .claude/skills/ml-review-pack이다.

## Review Focus

1. 저장된 HTML과 실행된 DOM의 details 위치 차이: 원시 HTML만 파싱하고 원문·힌트·풀이를 모두 보존한다. Task 1.
2. 확률표·SVG의 테마/CSS 상속, HTML 엔티티와 viewBox 대소문자: 독립 그림의 값·화살표·라벨을 보존한다. Task 2–3.
3. 정답만 넘치거나 Hint/그림만 잘리는 페이지: 템플릿 넘침 플래그 외에 모든 영역의 실제 경계도 검사한다. Task 3–4.
4. 증명 목표와 풀이 정답의 동일한 수식: 문제의 목표 식은 유지하고 해설 데이터만 제거한다. Task 2.
5. 두 번째 PDF나 노트 갱신 실패, NFD 경로, 재실행: 기존 PDF/노트를 복구하고 PDF 링크를 중복 생성하지 않는다. Task 5–6.

---

## 경로와 파일 구조

**ML_REPO:** /Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초
**EC2_REPO:** /Users/hyunjun_macbook_pro/Documents/Univ/전자회로2
**SKILL:** /Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.claude/skills/ml-review-pack

이 문서의 코드 경로는 ML_REPO 상대 경로다. `SKILL/...`는 위 실제 경로의 축약이다. 명령은 ML_REPO에서 실행한다. Python import는 기존 tests/_util.py가 scripts를 sys.path에 넣는 패턴을 따른다. scratch/build는 실행 워크트리의 work/ml-review-pdf/ 아래에 둔다.

| 파일 | 역할 |
|---|---|
| SKILL/assets/pdf-problem.html, pdf-answer.html | EC2 원본과 바이트 동일한 템플릿 |
| SKILL/assets/pdf-template-provenance.json | 원본 경로·원본 Git HEAD·SHA-256·확인 날짜 |
| SKILL/scripts/review_pdf_types.py | 아래 공통 dataclass와 Mode 계약 |
| SKILL/scripts/review_pdf_cards.py | 원시 카드 파싱·조건/질문 분할·원본 보존 검사 |
| SKILL/scripts/review_pdf_payload.py | 정규화 데이터/페이지를 EC2 JSON으로 변환 |
| SKILL/scripts/review_pdf_render.py | 표/그림 고정, Chrome 렌더링, DOM 검사 |
| SKILL/scripts/review_pdf_pages.py | 블록 경계로 유한한 후속 페이지 분할 |
| SKILL/scripts/review_pdf_publish.py | 스테이징 파일 배포·백업·실패 복구 |
| SKILL/scripts/build_review_pdf.py | 위 단계 조합과 CLI |
| SKILL/scripts/review_pdf_links.py | 정리노트 PDF 링크의 좁은 범위 편집 |
| workbook/layouts/<date>_<slug>.json | 기존 카드의 source_sha256와 조건/질문 분할 |
| SKILL/tests/test_review_pdf_*.py | 카드·payload·렌더·분할·배포·연결 검증 |
| SKILL/tests/fixtures/pdf/ | 작은 대표 입력과 오류 입력; 전체 강의자료 복제 금지 |
| docs/superpowers/reports/2026-10-06-ml-review-pdf-migration.md | 전체 자료 검증 근거와 미해결 |
| 복습노트/<date>/*-문제.pdf, *-답안.pdf | 최종 14개 PDF |

수정 대상은 기존 SKILL.md, references/card-rules.md·manifest-guide.md·content-rules.md·browser-check.md·review-prompt.md, scripts/assemble.py·manifest.py와 관련 테스트다. check_html.py·html2md.py는 새 PDF 링크의 동작이 이미 맞으면 수정 없이 회귀 검사만 한다. HTML 템플릿 디자인과 예습노트 공개 헬퍼는 변경하지 않는다.

## 공통 데이터 계약 — Task 1에서 정의

모든 컨테이너는 frozen dataclass이고 문자열 HTML은 저장된 원본에서 가져온다.

- `Mode = Literal["problems", "answers"]`.
- `FigureInput(id: str, html: str, kind: Literal["svg", "table", "image"])`.
- `ReviewCard(id: str, title: str, source: str, part: str, statement_html: str, original_html: str, hint_html: str, steps: tuple[str, ...], answer_html: str, figures: tuple[FigureInput, ...])`.
- `ReviewPack(range: str, slug: str, cards: tuple[ReviewCard, ...])`.
- `NormalizedProblem(card: ReviewCard, conditions_html: str, ask_html: str)`.
- `FigureAsset(src: str, w_mm: float, h_mm: float)`. src는 PNG data URI.
- `PageSlice(logical_id: str, continuation: int, conditions_html: str, ask_html: str, step_start: int, step_end: int, figure_ids: tuple[str, ...], show_original: bool, show_answer: bool)`. continuation은 첫 쪽 1, 후속 2…; step_end는 exclusive.
- `LayoutIssue(page_id: str, area: str, detail: str)`. area는 panel/work/answer/hint/figure/math 중 하나.
- `RenderReport(page_ids: tuple[str, ...], issues: tuple[LayoutIssue, ...], katex_errors: tuple[str, ...], failed_resources: tuple[str, ...])`.
- `BuildResult(problems_pdf: Path, answers_pdf: Path, report_path: Path)`. 공개 경로가 아닌 검증된 stage 경로를 반환한다.
- review_pdf_types.py에 `class ReviewPdfError(ValueError)`를 정의한다. 각 모듈 오류는 이를 상속하고 날짜·문제 id·영역을 메시지에 포함한다.

layout JSON은 `{"source_sha256": "<원본 HTML bytes SHA-256>", "problems": {"p1": {"conditions_html": "...", "ask_html": "..."}}}`다. 모든 원본 카드 id와 정확히 대응한다. 미래의 구조화 카드에는 layout을 생략할 수 있다.

### Task 1: 카드 정본과 분할 데이터 계약

**Files:** Create SKILL/scripts/review_pdf_types.py, review_pdf_cards.py, SKILL/tests/test_review_pdf_cards.py, fixtures/pdf/복습문제_0101_Pdf_Test.html, layouts.json, invalid-card.html.
**Interfaces:**
- Consumes: 저장된 article.card, 기존 html2md.Builder·Node와 check_html.math_delimiter_errors.
- Produces: `read_cards(path: Path) -> ReviewPack`; `normalize_cards(pack: ReviewPack, layouts: dict | None, source_path: Path) -> tuple[NormalizedProblem, ...]`.
- read_cards는 NFC 파일명 `복습문제_<range>_<slug>.html`에서 range/slug를 읽고 .card 순서로 파싱한다. normalize_cards는 비구조화 카드에 layout이 없으면 실패한다. 구조화 카드는 .problem 직계 .conditions와 .ask를 읽는다.

- [ ] **Step 1: 대표 fixture와 실패 테스트 작성.** 복습문제_0101_Pdf_Test.html에 p1 Example 9.1의 질문·수식과 p2 Exercise 6.1의 중첩 표/풀이를 넣고 source_sha256를 실제 fixture bytes에서 구한다. `TestCards`에 다음 assertion을 구현한다.
```python
pack = read_cards(FIXTURES / "pdf/복습문제_0101_Pdf_Test.html")
self.assertEqual([c.id for c in pack.cards], ["p1", "p2"])
self.assertEqual(len(pack.cards[1].figures), 1)
self.assertEqual(len(pack.cards[1].steps), 2)
self.assertIn(r"\frac{1}{5}", pack.cards[0].answer_html)
with self.assertRaisesRegex(ReviewPdfError, "p1.*ask"):
    normalize_cards(pack, {"source_sha256": source_hash, "problems": {"p1": {"conditions_html": "주어진 조건"}}}, source_path)
```
test_duplicate_id / test_missing_solution / test_layout_stale_source / test_preserves_entity_tex_and_step_order도 작성한다. 각각 중복 p1, 누락된 .solution, 다른 SHA, `&amp;`와 TeX 및 li 순서를 검사한다. source_hash와 source_path는 fixture 경로와 실제 bytes에서 계산한다.

- [ ] **Step 2:** `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_cards.py -v`. 새 모듈이 아직 없어 실패하는 것을 확인한다.
- [ ] **Step 3:** 위 타입과 함수를 구현한다. HTML은 Builder로 파싱하고 부분 HTML 재직렬화 헬퍼는 이 모듈 내부에 둔다. SVG는 기존 serialize로 대문자 속성을 복원한다. 표와 figure를 추출한 나머지 문제 본문은 layout의 conditions+ask와 공백·태그를 제외하고 순서대로 비교한다. 원본 그림과 추출 그림의 문자·구조도 대응시킨다. summary의 UI 문구는 본문에서 제외한다.
- [ ] **Step 4:** 같은 명령에서 Task 1 테스트가 모두 PASS하는지 확인한다.
- [ ] **Step 5:** 커밋이 승인되어 있다면 Task 1의 위 파일만 stage한다. 제안: `feat: normalize review cards for PDF`.

### Task 2: 동일 템플릿과 모드별 JSON

**Files:** Create SKILL/assets/pdf-problem.html, pdf-answer.html, pdf-template-provenance.json; SKILL/scripts/review_pdf_payload.py; SKILL/tests/test_review_pdf_payload.py.
**Interfaces:**
- Consumes: Task 1의 타입과 정규화 함수.
- Produces: `to_workbook(problems: Sequence[NormalizedProblem], assets: Mapping[tuple[str, str], FigureAsset], mode: Mode, pages: Sequence[PageSlice] | None = None) -> dict`; `inject_data(template: str, payload: dict) -> str`.
- pages=None은 각 논리 문제를 한 페이지로 배치한다. 페이지 수가 바뀌어도 report에서 원래 문제 id를 추적한다. meta.total은 본체의 물리 페이지 레코드 수다. Hint 부록은 여기에 포함하지 않는다.

- [ ] **Step 1: 실패 테스트 작성.** `TestPayload`에서 그림이 없는 p1 하나를 두 모드로 변환한다. 테스트 전용 NormalizedProblem에는 ask_html=PROOF_TARGET_SENTINEL, answer_html=ANSWER_ONLY_SENTINEL로 둔다. original_step과 original_answer는 이 입력 객체의 실제 값이다. 다음을 확인한다.
```python
problem_data = to_workbook(problems, {}, "problems")
answer_data = to_workbook(problems, {}, "answers")
self.assertNotIn("solution", problem_data["problems"][0])
self.assertNotIn("ANSWER_ONLY_SENTINEL", json.dumps(problem_data))
self.assertIn("PROOF_TARGET_SENTINEL", problem_data["problems"][0]["html"]["ask"])
self.assertEqual(answer_data["problems"][0]["solution"]["steps"][0]["html"], original_step)
self.assertEqual(answer_data["problems"][0]["solution"]["answer"], original_answer)
self.assertNotIn("</script><script>", inject_data(template, {"text": "</script><script>bad</script>"}))
```
TestTemplates는 provenance의 SHA와 동봉 템플릿 bytes의 SHA 일치를 검사한다. 테스트 실행에는 EC2 폴더가 필요하지 않아야 한다. HTML 원문·source·P 번호·Example/Exercise→예제/연습문제 매핑과 누락 asset 실패도 assert한다.

- [ ] **Step 2:** `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_payload.py -v`. 아직 구현하지 않아 FAIL하는지 확인한다.
- [ ] **Step 3:** EC2의 두 템플릿을 변경 없이 복사하고 spec의 SHA와 현재 bytes를 대조한다. provenance에 실제 Git HEAD를 기록한다. 위 두 함수를 구현하고 JSON 문자열에 들어간 `<`를 리터럴 Unicode escape `\u003c`로 대체한다. source를 section, P 번호를 number에 넣고 검증하지 않은 book_page는 null, difficulty는 0, sol은 false로 둔다. label이 없는 step은 빈 문자열이다. 그림·표는 figures에만 넣는다. 후속 페이지는 id=p1-c2, number=P1 (계속)로 구분하고 답은 마지막 페이지에 한 번만 표시한다.
- [ ] **Step 4:** Task 1–2 테스트를 같은 discover 명령으로 PASS시킨다. provenance hash와 bytes를 재확인한다.
- [ ] **Step 5:** 승인 시에만 위 파일을 stage한다. 제안: `feat: reuse EC2 templates for ML workbooks`.

### Task 3: 그림 고정과 실제 Chrome 검증

**Files:** Create SKILL/scripts/review_pdf_render.py; SKILL/tests/test_review_pdf_render.py; fixtures/pdf/media.html.
**Interfaces:**
- Consumes: Task 1–2.
- Produces: `freeze_figures(pack: ReviewPack, build_dir: Path) -> dict[tuple[str, str], FigureAsset]`; `render_workbook(payload: dict, mode: Mode, html_path: Path, pdf_path: Path | None = None) -> RenderReport`.
- CDN/폰트/KaTeX/이미지 실패는 ReviewPdfError. DOM 넘침은 report.issues로 반환해 Task 4가 분할하게 한다. 문제가 있는 결과는 공개하지 않는다.

- [ ] **Step 1: 브라우저 실패 테스트 작성.** TestRender의 test_table_and_graph_visible은 3×5 확률표와 다섯 노드 그래프 fixture를 고정한 뒤 img naturalWidth>0, 배경이 흰색, 셀 값/부모 방향/라벨이 원본과 동일함을 확인한다. test_answer_only_overflow, test_hint_only_overflow, test_resource_failure를 작성한다.
```python
report = render_workbook(payload_with_oversized_answer, "answers", html_path)
self.assertTrue(any(i.area == "answer" for i in report.issues))
with self.assertRaisesRegex(ReviewPdfError, "resource"):
    render_workbook(payload_with_missing_image, "problems", html_path)
```
payload_with_oversized_answer는 원래 답 HTML을 `<div style="height:300mm">ANSWER_ONLY_SENTINEL</div>`로 대체한 입력이다. payload_with_missing_image는 figures의 src를 존재하지 않는 stage 폴더의 file URI로 대체한 입력이다. 정상 fixture PDF는 PyMuPDF로 297×210mm(각 축 허용 오차 1mm), 한국어 텍스트 존재, 빈 페이지 없음, 풀이 모드에서만 정답 존재를 assert한다. 네트워크 실패 테스트는 Playwright route 차단을 사용하고 정상 테스트의 CDN 성공을 가정으로 생략하지 않는다.

- [ ] **Step 2:** `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_render.py -v`.FAIL 확인.
- [ ] **Step 3:** 설치된 Chrome channel을 사용한다. freeze_figures는 source의 명시적 SVG 클래스 색·stroke와 표 테두리를 독립 wrapper에 넣고 폰트·이미지·수식 준비 후 device_scale_factor=300/96로 PNG 캡처한다. 크기는 CSS px에서 25.4/96으로 mm 변환하고 PNG를 data URI로 전달한다. render_workbook는 원본 템플릿에 inject하여 data-ready를 최대120초 기다리고 print_background=true/prefer_css_page_size=true로 PDF를 만든다. page-id별 panel/work/answer/Hint/figure/display-math 경계와 이미지 decode, KaTeX error 노드, 요청 실패, 실제 요청 폰트 로드를 검사한다. DOM 기하 오차는 CSS 1px만 허용한다.
- [ ] **Step 4:** 정상과 실패 fixture 테스트 모두 PASS 확인. 정상 결과 첫 문제·표·그래프·정답·Hint 페이지를 눈으로 검사하여 기하 검사만으로 놓치는 선/라벨 문제를 찾는다.
- [ ] **Step 5:** 승인 시 위 파일만 stage. 제안: `feat: render and validate ML workbook pages`.

### Task 4: 내용 손실 없는 후속 페이지

**Files:** Create SKILL/scripts/review_pdf_pages.py; SKILL/tests/test_review_pdf_pages.py.
**Interfaces:**
- Consumes: Task 1의 PageSlice와 Task 3의 RenderReport.
- Produces: `paginate(problems: Sequence[NormalizedProblem], mode: Mode, measure: Callable[[Sequence[PageSlice]], RenderReport]) -> list[PageSlice]`.
- measure는 Task 2 to_workbook와 Task 3 render_workbook을 연결한 callback이다. 각 호출은 새 stage HTML을 만들고 payload를 재측정한다.

- [ ] **Step 1: 실패 테스트 작성.** TestPages에 test_split_preserves_all_steps / test_unsplittable_matrix_fails / test_answer_on_final_page_only / test_condition_blocks_continue / test_missing_work_space_fails를 작성한다. 측정 callback은 fixture의 각 page 용량을 결정적으로 제한한다. 아래 예제는 풀이 단계 7개인 단일 p1 문제를 사용하고, measure_three_steps_per_page는 페이지당 최대 3단계만 허용하는 테스트 헬퍼다.
```python
pages = paginate(problems, "answers", measure_three_steps_per_page)
covered = [i for p in pages for i in range(p.step_start, p.step_end)]
self.assertEqual(covered, list(range(7)))
self.assertEqual([p.show_answer for p in pages], [False, False, True])
self.assertEqual([p.continuation for p in pages], [1, 2, 3])
with self.assertRaisesRegex(ReviewPdfError, "p1.*unsplittable"):
    paginate(single_matrix_problem, "problems", always_overflow)
```
problem의 증명목표·필수 조건은 모든 후속 페이지에서 찾을 수 있어야 한다. 긴 질문의 소문항 순서와 조건 문장 보존도 assert한다.

- [ ] **Step 2:** `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_pages.py -v`.FAIL 확인.
- [ ] **Step 3:** 먼저 원본 템플릿의 자동 맞춤 결과를 측정한다. 남은 넘침 영역에서 문장/소문항/풀이 li 경계만 사용해 뒤쪽 블록을 다음 페이지로 옮긴다. 원문·조건·질문·풀이·정답·그림은 논리 문제에 계속 대응시킨다. 필수 조건은 반복할 수 있으나 신규 조건을 만들지 않는다. 문제 모드 각 페이지의 .work 높이 또는 폭이 0이면 실패한다. 각 분할은 아직 쓰지 않은 유한 경계 하나를 소비해야 하며, 더 나눌 수 없으면 ReviewPdfError로 종료한다.
- [ ] **Step 4:** Task 4 테스트 PASS 확인 후 Task 3 Chrome 렌더로 긴 실제 0923 P7·0930 P3/P8을 스모크 검사한다. 그들의 layout은 Task 7 전체 migration 전 대표 3문항만 임시 fixture로 준비한다. 내용 누락 없이 issues가 비는 것을 확인한다.
- [ ] **Step 5:** 승인 시 위 파일만 stage. 제안: `feat: paginate long ML solutions without content loss`.

### Task 5: 빌드 CLI와 배포 실패 복구

**Files:** Create SKILL/scripts/build_review_pdf.py, review_pdf_publish.py; SKILL/tests/test_review_pdf_build.py, test_review_pdf_publish.py.
**Interfaces:**
- Consumes: Tasks 1–4.
- Produces: `build_pack(review_path: Path, layouts_path: Path | None, build_dir: Path) -> BuildResult`; `publish_files(staged: Mapping[Path, Path], backup_dir: Path) -> None`. staged는 최종 목적지→검증된 stage 파일 매핑이다.
- CLI: `build_review_pdf.py --review PATH [--layouts PATH] --build-dir PATH [--pdf-dir PATH] --report PATH [--stage-only]`. stage-only는 공개 쓰기 없음. report는 선택한 경로에 JSON 검증 보고서를 복사한다. --pdf-dir 없으면 stage-only를 필수로 요구한다.

- [ ] **Step 1: 실패 테스트 작성.** TestBuild는 실제 Chrome fixture의 두 PDF와 report를 검사한다. TestPublish는 교체 중 두 번째 파일에서 예외를 주입한다.
```python
before = {p: p.read_bytes() for p in destinations}
with self.assertRaises(OSError):
    publish_files(staged, backup_dir)
self.assertEqual({p: p.read_bytes() for p in destinations}, before)
self.assertFalse(new_destination.exists())
```
test_nfd_pack_path는 실제 NFD 폴더의 source를 읽고 기존 파일을 중복 생성하지 않는지 검사한다. test_same_pack_concurrent_publish는 두 번째 실행의 lock 획득 실패와 첫 실행의 stage/공개 파일 bytes 보존을 확인한다. test_second_pdf_failure_publishes_neither와 test_stale_source_blocked도 작성한다. stage 파일이 하나라도 누락되면 공개 파일을 쓰기 전에 실패한다.

- [ ] **Step 2:** 두 test_review_pdf_build.py/test_review_pdf_publish.py를 각각 unittest discover로 실행하여 FAIL 확인.
- [ ] **Step 3:** build_pack은 parse→normalize→freeze→두 모드 paginate/render→증거 JSON 저장을 순서대로 실행한다. report에 range/slug/logical_count/id→물리페이지 매핑/두 PDF hash/원본 hash/모든 오류를 기록한다. publish_files는 모든 stage 경로를 선검사하고 목적지 기존 파일을 고유 backup-dir에 복사 후 같은 filesystem의 임시 파일+replace를 사용한다. 일부 교체에 실패하면 이미 바꾼 기존 파일을 복구하고 새로 생긴 목적지는 제거한다. 다중 파일의 OS 수준 원자성을 주장하지 않는다. CLI 종료코드 0=검증 성공, 1=내용/렌더/배포 실패, 2=사용법 오류. 같은 range의 배포가 이미 진행 중이면 work 영역의 배타적 lock을 얻지 못한 실행은 공개 파일을 건드리지 않고 실패한다. stale lock은 이전 실행이 실제 종료되었음을 확인하기 전 자동 삭제하지 않는다.
- [ ] **Step 4:** 두 테스트를 PASS시키고 stage-only 전후 공개 폴더 bytes 동일을 확인한다. EC2 저장소를 읽지 않고 local copies만으로 빌드하는 검사도 통과한다.
- [ ] **Step 5:** 승인 시 위 파일만 stage. 제안: `feat: stage and publish validated review PDF pairs`.

### Task 6: 노트 링크와 향후 복습팩 연결

**Files:** Create SKILL/scripts/review_pdf_links.py, SKILL/tests/test_review_pdf_links.py; Modify SKILL/scripts/assemble.py:50-110, manifest.py:163-172, SKILL.md:10-11,66-141; references/card-rules.md:18-35, manifest-guide.md:15-18,48-53, content-rules.md:11,38, browser-check.md 및 review-prompt.md; 관련 기존 테스트.
**Interfaces:**
- Consumes: Task 5 BuildResult/publish_files.
- Produces: `pdf_names(range_: str, slug: str) -> tuple[str, str]` in manifest.py; `add_pdf_links(note_html: str, range_: str, slug: str, logical_count: int) -> str` in review_pdf_links.py.
- assemble의 기존 `assemble(run_dir, out_dir) -> tuple[Path, Path]` API와 REVIEW_HREF를 유지한다. 새 keyword-only `include_pdf_links: bool = False`와 CLI --pdf-links를 추가한다. 옵션 사용 시 out_dir의 검증된 두 PDF가 없으면 두 HTML 모두 쓰지 않고 실패한다. 순수 legacy 호출은 브라우저를 실행하지 않는다.

- [ ] **Step 1: 실패 테스트 작성.** TestLinks에 다음 assertion과 원본 노트의 수식/본문/기존 href 보존을 확인하는 test_preserve_unrelated_content를 추가한다.
```python
once = add_pdf_links(note_html, "0914", "ERM_and_MLE", 7)
self.assertEqual(add_pdf_links(once, "0914", "ERM_and_MLE", 7), once)
self.assertIn("복습문제_0914_ERM_and_MLE-문제.pdf", once)
self.assertIn("복습문제_0914_ERM_and_MLE-답안.pdf", once)
self.assertNotIn("8선", pdf_link_block(once))
self.assertIn("7", legacy_review_link_text(once))
self.assertNotIn("8선", legacy_review_link_text(once))
```
pdf_link_block과 legacy_review_link_text는 테스트 내 HTMLParser 헬퍼다. 각각 class=review-pdf-links 블록과 기존 review HTML을 가리키는 anchor 문구를 찾는다. note_html fixture의 기존 link 문구는 8선으로 둔다. TestAssemble에 test_pdf_links_missing_pair_writes_neither를 추가한다. 기존 HTML/MD convert_pack 실행 후 .pdf href 유지, check_html의 PDF 존재 검사, ml-preview-note 공개 함수 회귀를 검증한다.

- [ ] **Step 2:** `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_links.py -v`와 수정한 TestAssemble를 실행하여 FAIL 확인.
- [ ] **Step 3:** 새 PDF 링크 블록을 마지막 links 토픽 안에 추가한다. data-range와 class=review-pdf-links로 재실행 대상을 식별한다. 기존 HTML 링크는 보조 링크로 유지하되 그 링크의 잘못된 문항 수만 실제 count로 바로잡는다. 전체 노트를 DOM 직렬화로 다시 쓰지 말고 해당 노드 범위만 패치한다. card-rules에 .problem 안의 .conditions/.ask 마크업을 필수로 추가한다. 미래 skill의 순서는 HTML/MD stage 조립→기존 검증→PDF stage 빌드→PDF 링크 삽입/MD 갱신→링크/수학 검사→publish_files로 네 HTML/MD와 두 PDF 배포다. manifest.links에는 두 PDF link를 추가하고 기존 review HTML link는 유지한다. 백업·보고·실패 설명을 PDF까지 확장한다.
- [ ] **Step 4:** `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -v`, `python3 -m unittest discover -s .claude/skills/ml-preview-note/tests -v`, `python3 -m unittest discover -s tests -v`를 실행한다. PDF 링크와 기존 API 회귀가 PASS여야 한다. 기존 의도적 fixture skip은 실제 회귀 PASS로 보고하지 않는다.
- [ ] **Step 5:** 승인 시 Task 6 변경 파일만 stage. 제안: `feat: include workbook PDFs in future ML review packs`.

### Task 7: 기존 47문항 이관과 전체 PDF 검수

**Files:** Create workbook/layouts/0909_Data_Models_Learning.json, 0914_ERM_and_MLE.json, 0916_MAP_and_Generative_Models.json, 0921_Bayesian_Inference_Model_Selection.json, 0923_Linear_Regression.json, 0928_Linear_Regression.json, 0930_Bayesian_Linear_Regression.json; SKILL/tests/test_review_pdf_migration.py; docs/superpowers/reports/2026-10-06-ml-review-pdf-migration.md; 7개 날짜의 두 PDF. Modify 같은 날짜 정리노트 HTML/MD의 PDF 링크와 문항 수 안내만.
**Interfaces:**
- Consumes: Tasks 1–6.
- Produces: 기존 전체 자료와 미래 생성 fixture의 검증된 배포; 코드 API 추가 없음.

- [ ] **Step 1: 실패하는 실제 자료 대응 테스트 작성.** TestMigration은 NFC 경로 탐색으로 일곱 HTML을 읽고 대응 layout을 검사한다.
```python
self.assertEqual(counts, {"0909": 5, "0914": 7, "0916": 6, "0921": 6, "0923": 7, "0928": 8, "0930": 8})
self.assertEqual(sum(counts.values()), 47)
self.assertEqual(set(layouts_by_date), set(counts))
self.assertEqual(len(expected_pdf_names), 14)
```
source_sha256와 기존 각 카드 id/source/수식/표/그림/풀이/정답 대응을 Task 1 보존 검사로 확인한다. existing review HTML/MD bytes는 migration 전후 동일을 assert한다.

- [ ] **Step 2:** `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_migration.py -v`.layout 미작성으로 FAIL 확인.
- [ ] **Step 3:** 기존 47카드의 conditions/ask를 layout JSON으로 작성한다. 숫자와 식을 바꾸지 않고 모든 source hash를 기록한다. 수치·행렬 정답은 Fraction/행렬 곱 등 독립 계산으로 확인하고 기호 문제는 전제·각 변형을 대조하여 문제별 검증 방법과 결과를 보고서에 남긴다. 기존 scripts/review_answers.py는 일부 날짜용이므로 47문항 검증 완료의 근거로 단독 사용하지 않는다.
- [ ] **Step 4:** 일곱 날짜를 각각 Task 5 CLI --stage-only로 빌드한다. 실패 날짜는 publish하지 않고 문제 id/원인을 보고한다. 정상 날짜는 14개 stage PDF의 크기·텍스트·logical mapping을 검사한다.
- [ ] **Step 5:** PyMuPDF 또는 pdftoppm으로 stage PDF 전체 페이지를 work/ml-review-pdf/qa/<date>/<mode>/ 아래 PNG로 렌더링한다. 모든 페이지를 inspect하고 표의 값, 그래프 선·노드, 4×4 행렬, 장문 증명, 후속 페이지의 조건, 마지막 답, Hint 부록을 확인한다. 두 개의 PDF가 모두 QA 완료되어야 그 날짜를 다음 단계로 넘긴다. 실행 시 사용하는 PDF skill의 authoring marker가 요구되면 첫 PDF 작성 전에 한 번 수행한다.
- [ ] **Step 6:** 기존 정리노트를 stage에 복사하고 add_pdf_links로 수정한 뒤 Markdown을 갱신한다. 원래 HTML/MD의 math/그림/토픽/id와 PDF 링크를 비교한다. 두 PDF+노트 HTML/MD를 publish_files로 배포한다. 기존 review HTML/MD와 figures가 바뀌지 않았는지 hash로 확인한다.
- [ ] **Step 7:** Task 6의 세 Python 테스트 suite를 실행하고 `node --test tests/widget_math.test.js`도 실행한다. TestMigration으로 총47문항/14개 PDF/날짜별 한 쌍을 확인하고, 실제 정리노트에서 두 PDF 링크를 열어 페이지·파일 연결을 확인한다. 검증 report에 명령 결과·QA 페이지 수·템플릿 SHA·원본 보존·정답 검증·미해결·백업 경로를 기록한다.
- [ ] **Step 8:** 승인 시 생성 PDF·layout·변경 노트·검증 보고서·migration 테스트만 stage. 제안: `docs: migrate existing ML review problems to PDF`.push하지 않는다.

## 완료 및 자체 검토 기록

- 요구사항 대응: 원본 템플릿 Task2, 카드/내용 보존 Task1·7, 수치/기호 정확성 Task7, 그림 Task3, 문제/정답 분리 Task2, 넘침 Task3·4, 배포 실패 복구 Task5, 기존/미래 연결 Task6·7.
- 다섯 Review Focus 모두 해당 task의 명시적 테스트에 대응한다.
- 후속 task는 위 공통 타입과 정확한 함수 이름을 사용한다. Task7은 새 API를 만들지 않는다.
- 순서는 1→2→3→4→5→6→7이다. 통합 의존성이 커서 Native 실행을 권장한다.
- 이 계획 작성 중 실제 코드·템플릿·강의자료·PDF는 수정하거나 빌드하지 않았다. 구현용 테스트는 아직 실행하지 않았다.
- 커밋은 사용자 요청이 있을 때만 수행하고, 구현 전 계획 검토 및 실행 방식을 확인한다.
