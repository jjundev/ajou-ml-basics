# ML Review PDF Widescreen Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 47문항/PDF 14개와 향후 ML 복습팩에 EC2와 같은 16:9·자막 여백·화면 글자 크기 계약을 적용한다.

**Architecture:** EC2의 고정 커밋 템플릿과 CSS를 ML에 복사하고 작은 layout 모듈을 추가한다. 기존 renderer에서 A4 fitting을 측정한 뒤 16:9로 렌더하며 기존 pagination·publisher를 유지한다. build 진입점에서 규격별 검증과 보고서를 묶는다.

**Tech Stack:** Python unittest, Playwright/Google Chrome, HTML/CSS/KaTeX/Pretendard, PyMuPDF, SHA256, 기존 POSIX publisher.

**Spec:** `docs/superpowers/specs/2026-10-07-ml-review-pdf-widescreen-design.md`

## Global Constraints

- 기본 복습팩 출력은 1920×1080 CSS px, PDF 1440×810pt의 16:9다.
- 하단 180px(900≤y≤1080)는 흰 자막 예약 영역이다. 텍스트·수식·그림·격자·Hint·제작자 표기를 넣지 않는다.
- 화면 글자 크기 보정식은 `(900 / (210 * 72 / 25.4)) / (1920 / 1440)`이다. 기본 본문 10pt는 약 11.34pt가 된다.
- 저수준 renderer는 기본 A4를 유지하고 build/CLI는 기본 `video-16x9`, `--layout a4`는 호환한다.
- 모드별·물리 페이지별 A4 배율을 보존한다. 분할 후 새 페이지 구성은 다시 측정한다. 임의 추가 축소·내용 삭제는 금지한다.
- 기존 47문항의 내용·순서·출처, HTML·MD·그림 bytes, PDF 파일명·링크를 보존한다.
- EC2 source commit은 `757fa081521008d46542e23d5a1a53112391aed2`. 런타임 EC2 의존성은 없다.
- stage 검증 및 전체 페이지 시각 검수 후 날짜별 백업·교체한다. 실패 시 기존 PDF를 보존한다.
- `.claude/skills/ml-review-pack`만 수정한다. `.agents` symlink를 별도 파일로 교체하지 않는다.
- 이번 계획 작성은 구현 승인이 아니다. 실행 시작 시 격리 및 동시 작업 상태를 확인한다. 아래 커밋 단계는 사용자 별도 요청 전까지 보류한다. push/merge는 포함하지 않는다.

## Review Focus

1. 장문 풀이에 A4의 0.8 배율이 적용된 경우: 새 PDF에서도 같은 화면 표시 크기를 유지한다. Task 2 `test_dense_text_preserves_a4_screen_size`.
2. 계속 페이지의 id가 바뀌는 경우: 새 후보별 typography를 재측정하고 누락 페이지를 기본 배율로 묵살하지 않는다. Task 2 `test_continuations_remeasure_and_missing_typography_fails`.
3. 글자가 없지만 그림·격자가 자막 영역에 들어간 경우: DOM 및 PDF 검사 모두 배포를 차단한다. Task 2 `test_caption_band_rejects_text_image_and_grid`.
4. 답안 PDF 실패 또는 공개 파일 교체 실패: 이전 문제지·답안지를 모두 복구한다. Task 2/3의 기존 실패 주입 테스트.
5. 기존 A4 호출과 긴 Hint 부록: A4 호환을 유지하고 양 규격 모두 Hint 넘침을 보고한다. Task 2 `test_a4_compatibility_and_wide_hint_overflow`.

---

## File Structure

모든 경로는 저장소 루트 기준이다. `S=.claude/skills/ml-review-pack`, `T=$S/tests`는 아래 실행 명령에서만 쓰는 zsh 변수다.

| 파일 | 책임 |
|---|---|
| `S/scripts/review_pdf_layout.py` (신규) | Layout/typography 타입, 규격 값, 템플릿 로딩·pt 보정 |
| `S/assets/pdf-problem.html`, `pdf-answer.html` | 해당 EC2 커밋의 원본 복사본 |
| `S/assets/pdf-video-16x9.css` (신규), `pdf-template-provenance.json` | CSS 복사본과 세 파일의 SHA/출처 |
| `S/scripts/review_pdf_render.py` | 공유 렌더 경로, A4 측정, geometry gate |
| `S/scripts/build_review_pdf.py` | layout 전달, 규격/PDF 자막 검사, validation 기록 |
| `S/tests/test_review_pdf_layout.py` (신규), 기존 payload/render/build/migration 테스트 | 규격·실제 PDF·배포 회귀 |
| `S/SKILL.md`, `S/references/pdf-workflow.md` | 향후 생성 계약과 검증 명령 |
| `복습노트/{0909,0914,0916,0921,0923,0928,0930}/*-{문제,답안}.pdf` | 최종 공개 PDF 14개 |
| `docs/superpowers/reports/2026-10-07-ml-review-pdf-widescreen.md` (실행 시 신규) | 페이지 대응·해시·회귀·시각 검수 근거 |

Task 1은 템플릿과 보정 단위를, Task 2는 끝까지 실행 가능한 생성기를, Task 3은 검증된 기존 자료와 향후 지침을 제공한다. `review_pdf_payload.py`, `review_pdf_pages.py`, `review_pdf_publish.py`는 변경을 계획하지 않는다.

### Task 1: 고정 템플릿과 layout 모듈

**Files:** Create `S/scripts/review_pdf_layout.py`, `S/assets/pdf-video-16x9.css`, `S/tests/test_review_pdf_layout.py`; Modify `S/assets/pdf-{problem,answer}.html`, `S/assets/pdf-template-provenance.json`, `S/tests/test_review_pdf_payload.py:31-37`.

**Interfaces:**
- Consumes: 기존 `ReviewPdfError`, `ASSETS`에 해당하는 스킬 assets 경로, 고정 EC2 Git object.
- Produces: `Layout = Literal['a4','video-16x9']`; `PageTypography(TypedDict)`의 `panel: float`, `solution: float`, `math: list[float]`, `hints: list[float]`; `Typography = dict[str, PageTypography]`.
- Produces: `load_template(mode: Mode, layout: Layout = 'a4') -> str`; `page_size_pt(layout: Layout) -> tuple[float,float]`; `VIDEO_TEXT_SCALE: float`. 무효 mode/layout은 `ReviewPdfError`.

- [x] **Step 1: 실패 테스트 작성.** 새 `TestLayout`에 아래 assertion을 작성한다. 고정 SHA 검사는 EC2 working tree가 아니라 지정 Git commit의 세 원본 파일 bytes와 최초 1회 대조한 provenance를 기준으로 한다. 기존 `test_templates_unchanged`는 새 provenance 계약으로 변경한다.

```python
def test_video_profile_and_a4_profile(self):
    self.assertEqual(page_size_pt('video-16x9'), (1440, 810))
    self.assertEqual(page_size_pt('a4'), (297*72/25.4, 210*72/25.4))
    self.assertAlmostEqual(VIDEO_TEXT_SCALE*10, 11.339286, places=5)
    self.assertIn('1920px 1080px', load_template('problems', 'video-16x9'))
    self.assertIn('297mm 210mm', load_template('answers', 'a4'))

def test_invalid_layout(self):
    with self.assertRaises(ReviewPdfError):
        load_template('problems', 'square')
```

- [x] **Step 2: RED 확인.** `S=.claude/skills/ml-review-pack; python3 -m unittest discover -s "$S/tests" -p 'test_review_pdf_layout.py' -v`. Expected: 새 모듈/심볼 부재로 FAIL.
- [x] **Step 3: 고정 복사·구현.** `git -C <EC2_ROOT> show 757fa081521008d46542e23d5a1a53112391aed2:workbook/templates/<file>`로 problem.html, answer.html, video-16x9.css를 읽어 ML 대응 파일에 복사한다. `load_template`는 EC2 render.py의 pt 보정과 CSS/flag 주입 방식으로 구현한다. `page_size_pt`는 위 정확한 두 규격을 반환한다. provenance에 source commit과 세 파일 SHA를 기록한다. 기존 원본 HTML 템플릿 bytes는 보정하지 않고 로딩 때만 변환한다.
- [x] **Step 4: GREEN 확인.** layout 및 payload 테스트를 각각 `python3 -m unittest discover -s "$S/tests" -p 'test_review_pdf_layout.py' -v`, `... -p 'test_review_pdf_payload.py' -v`로 실행한다. Expected: 모두 OK, ML 코드에 외부 EC2 import/path 의존성 없음.
- [ ] **Step 5: 승인된 경우에만 커밋.** 이 작업의 파일만 stage하고 `feat(ml-review): add widescreen PDF layout profile`. 커밋 미승인 상태에서는 단계 보류로 기록한다.

### Task 2: A4 배율 보존과 16:9 생성·검증

**Files:** Modify `S/scripts/review_pdf_render.py:62-130`, `S/scripts/build_review_pdf.py:22-87`, `S/tests/test_review_pdf_render.py`, `S/tests/test_review_pdf_build.py`; extend `S/tests/test_review_pdf_layout.py`.

**Interfaces:**
- Consumes: Task 1 타입 및 함수; 기존 `to_workbook(...) -> dict`, `paginate(problems, mode, measure) -> list[PageSlice]`, `RenderReport`, `BuildResult`.
- Produces: `measure_typography(payload: dict, mode: Mode, html_path: Path) -> Typography`.
- Produces: `render_workbook(payload: dict, mode: Mode, html_path: Path, pdf_path: Path | None = None, *, layout: Layout = 'a4', typography: Typography | None = None) -> RenderReport`.
- Produces: 공유 private `_render_document(payload, mode, html_path, pdf_path=None, *, layout='a4', typography=None) -> tuple[RenderReport, Typography]`. 측정은 PDF 출력 없이 A4 geometry issues를 반환/기록하며 기존 resource/KaTeX 실패는 예외 처리한다.
- Produces: `build_pack(review_path: Path, layouts_path: Path | None, build_dir: Path, *, layout: Layout = 'video-16x9') -> BuildResult`; `_verify_pdf(path: Path, expected_pages: int, layout: Layout) -> None`. `publish_build`와 CLI 반환 계약은 유지한다.

- [x] **Step 1: 실패 테스트 작성.** fixture는 기존 `TestRender`의 두 카드 및 `freeze_figures`를 재사용한다. 새 video 통합 테스트를 layout 모듈의 `TestVideoLayout`에 모은다. 각 검사는 아래 이름과 assertion을 사용한다.

```python
# test_wide_pair_dimensions_and_separation:
self.assertAlmostEqual(page.rect.width, 1440, delta=0.1)
self.assertAlmostEqual(page.rect.height, 810, delta=0.1)
self.assertEqual('ANSWER_ONLY_SENTINEL' in text, mode == 'answers')
# test_dense_text_preserves_a4_screen_size: 긴 한국어 문장을 넣어
# A4 panel 또는 solution fitting이 <1이 된 실제 fixture를 사용한다.
self.assertLess(a4_typography[page_id]['solution'], 1)
self.assertAlmostEqual(a4_font_pt*900/(210*72/25.4), wide_font_pt*1920/1440, delta=0.1)
self.assertEqual(a4_typography[page_id]['math'], wide_applied_math_scales)
# test_caption_band_rejects_text_image_and_grid: 각각 absolute y=950px에
# 텍스트, 1x1 검정 PNG, 검정 선을 넣은 payload를 별도로 렌더한다.
self.assertTrue(any(i.area == 'caption' for i in report.issues))
with self.assertRaises(ReviewPdfError):
    render_workbook(payload, mode, html, pdf, layout='video-16x9', typography=scales)
# test_continuations_remeasure_and_missing_typography_fails:
self.assertIn('p1-c2', measured_page_ids)
self.assertEqual(set(final_page_ids), set(final_typography))
with self.assertRaises(ReviewPdfError):
    render_workbook(payload, mode, html, layout='video-16x9', typography={})
```

계속 페이지 fixture는 기존 paginator 테스트의 단계 분할 입력을 사용하고 measure wrapper 호출을 spy하여 새 id를 확인한다. typography의 Hint 수식 배열도 동등성을 검사한다. `test_a4_compatibility_and_wide_hint_overflow`는 원래 A4 크기 assertions를 유지하고 600mm Hint fixture가 양 규격에서 `hint` issue를 내는지 확인한다. build 테스트에 기본 video, 명시 A4 및 실패 보고서 `status='failed'`를 추가한다.

- [x] **Step 2: RED 확인.** `python3 -m unittest discover -s "$S/tests" -p 'test_review_pdf_layout.py' -v`와 `... -p 'test_review_pdf_build.py' -v`. Expected: 새 인자/API 부재 또는 A4 출력으로 FAIL.
- [x] **Step 3: renderer 구현.** 기존 Chrome 경로를 `_render_document`로 공유한다. `measure_typography`는 EC2 render.py의 DOM selectors로 A4 fitting을 캡처한다. video 호출은 deep copy payload의 `meta.typography`에 측정값을 넣고 Task 1 템플릿을 사용한다. 입력 payload는 변경하지 않는다. 최종 template가 배율을 적용한 뒤 resource·geometry gate를 실행한다. 누락 page id는 실패시킨다. 페이지 내 가시 콘텐츠와 panel/work/Hint의 실제 경계가 y=900px 아래로 침범하면 `area='caption'` issue를 반환한다. 절대배치 요소도 포함하고 staging/흰 배경은 제외한다. DOM page의 mm→px 단위를 추정하지 말고 실제 rect와 video 규격값을 사용한다.
- [x] **Step 4: build 및 PDF 검사 구현.** 매 pagination 후보마다 같은 payload의 A4 배율을 먼저 측정하고 video 후보에 적용한다. A4 build에서는 새 측정을 하지 않는다. 최종 후보도 별도로 측정하여 보고서에 저장한다. CLI에 `--layout {a4,video-16x9}` 기본 video를 추가하고 모든 호출·test mocks에 전달한다. `_verify_pdf`는 선택 크기(허용 오차 0.1pt video/1mm A4), 비어 있지 않은 페이지, 페이지 수를 확인한다. video 마지막135pt의 text bbox·image bbox·비백색 도형 침범은 실패시킨다. 흰 배경 rectangle은 허용한다. 검사는 DOM gate의 대체가 아니다. validation JSON에 `layout`, `page_size_pt`, `caption_height_px`, 모드별 `typography`와 기존 mapping/hash를 저장한다.
- [x] **Step 5: GREEN 및 실패 격리 확인.** `python3 -m unittest discover -s "$S/tests" -p 'test_review_pdf*.py' -v`. Expected: 모두 OK, 기존 리소스 실패·answer/Hint overflow·유한 분할·second PDF failure·publisher rollback 테스트 유지. 기존 fake render mock은 새 kwargs를 받도록 수정하며 실패 주입은 최종 answers PDF에만 적용한다.
- [ ] **Step 6: 승인된 경우에만 커밋.** Task 2 파일만 stage하고 `feat(ml-review): preserve text size in widescreen PDFs`.

### Task 3: 기존 14개 재생성·배포와 향후 계약

**Files:** Modify `S/SKILL.md:126-132`, `S/references/pdf-workflow.md`, `S/tests/test_review_pdf_migration.py`, 기존 PDF14개; Create 실행 검증 보고서. 원본 HTML/MD/layouts/figures는 읽기만 한다.

**Interfaces:**
- Consumes: Task 2 `build_pack`, 기존 `publish_build`, `workbook/layouts/<date>_<slug>.json`, validation JSON.
- Produces: 같은 파일명 PDF14개, 향후 스킬의 기본 video 계약, 공개 파일 SHA·논리/물리 페이지 대응·검증 보고서.

- [x] **Step 1: 공개 산출물 실패 검사 작성.** `test_published_pairs_are_widescreen_and_caption_safe`에서 아래 검사를 추가한다. 기존 원본 해시/링크 검사를 유지한다.

```python
self.assertEqual(counts, {'0909':5,'0914':7,'0916':6,'0921':6,'0923':7,'0928':8,'0930':8})
self.assertEqual(len(published_pdf_paths), 14)
for path in published_pdf_paths:
    with fitz.open(path) as doc:
        for page in doc:
            self.assertAlmostEqual(page.rect.width, 1440, delta=0.1)
            self.assertAlmostEqual(page.rect.height, 810, delta=0.1)
            self.assertFalse(page.get_text(clip=fitz.Rect(0,675,1440,810)).strip())
```

- [x] **Step 2: RED 확인.** `python3 -m unittest discover -s "$S/tests" -p 'test_review_pdf_migration.py' -v`. Expected: 기존 A4 PDF의 크기 assertion FAIL, 원본 SHA 검사는 PASS.
- [x] **Step 3: 향후 지침 변경.** SKILL 및 pdf-workflow에 기본 16:9, 명시 A4, 하단180px, A4 배율 보존, 새 template/CSS provenance 및 전체 페이지 검수를 기록한다. “두 템플릿은 변경하지 않는다”는 실행 시 provenance 검증이라는 의미로 유지하되 새 커밋/세 파일 기준으로 명확히 한다. 노트 링크 변경 절차는 추가하지 않는다.
- [x] **Step 4: stage 생성.** 실행 RUN의 고유 build-dir에서 7개 날짜별 기존 review HTML와 대응 layouts로 `build_pack(..., layout='video-16x9')`를 호출한다. source/MD/figures149개 SHA와 기존 PDF14개 bytes를 실행 전 보존한다. A4 comparison은 원래 공개 PDF 및 동일 후보의 A4 측정을 사용한다. CLI 호출 예시는 `python3 "$S/scripts/build_review_pdf.py" --review "$review_path" --layouts "$layouts_path" --build-dir "$run_dir/build/$date" --stage-only --layout video-16x9 --report "$run_dir/$date-validation.json"`이다. date별 review/layout 경로는 기존 migration 테스트와 같은 NFC discovery 방식으로 찾아 전달한다.
- [x] **Step 5: 모든 stage PDF 검수.** validation의 47문항, 두 mode mapping, 14개 PDF, SHA, overflow0, 자막 침범0을 확인한다. 전체 페이지 PNG와 A4/16:9 화면 크기 비교 결과를 RUN에 저장한다. 4×4 행렬·표·방향 그래프·긴 증명·Hint 부록·필기 영역을 모두 직접 확인한다. 페이지수가101과 다르면 계속 페이지 id/이유를 기록한다. 실패한 날짜는 배포하지 않는다.
- [x] **Step 6: 날짜별 배포.** 전체 stage 검수가 끝난 뒤 `publish_build(result, date_folder, run_backup_folder)`로 PDF 쌍만 교체한다. 교체 직전 기존 PDF/source SHA를 재확인한다. existing rollback 테스트로 교체 실패 복구가 통과함을 확인한 다음 공개 파일을 변경한다. 설치 후 stage와 공개 PDF bytes, 원본149개/HTML/MD 해시, 노트 링크 목적지를 다시 대조한다.
- [x] **Step 7: 최종 회귀 및 보고서.** 아래를 각각 실행한다. Expected: `OK`, Node fail0. skip 수는 따로 기록한다. 실행 보고서에 출처 세 파일 SHA, 14개 최종 SHA, 날짜별 페이지수·계속 대응, 표시 글자 크기 차이, 전체 PNG 검수, backup 경로, 실패/미해결 항목과 배포 상태를 기록한다.

```bash
python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -v
python3 -m unittest discover -s .claude/skills/ml-preview-note/tests -v
python3 -m unittest discover -s tests -v
node --test tests/widget_math.test.js
git diff --check
```

- [ ] **Step 8: 승인된 경우에만 커밋.** PDF14개·Task3 지침/테스트·검증 보고서만 stage하고 `feat(ml-review): migrate review PDFs to widescreen`. push/merge하지 않는다.

## Self-Review

- Spec coverage: Task1 규격/보정/고정 복사, Task2 A4 측정/분할/geometry/PDF/CLI/오류, Task3 기존14개/향후생성/내용보존/배포/시각·회귀 검증. 미할당 요구 없음.
- Interfaces: Mode/RenderReport/BuildResult는 기존 타입, Layout/Typography는 Task1이 소유한다. 저수준 기본A4·build 기본video를 명시했고 기존 payload/paginator/publisher API는 보존한다.
- Review Focus: 5개 조건을 Task2/3의 이름 있는 테스트 또는 기존 실패 주입 테스트에 연결했다.
- Step/proportion: setup와 provenance는 Task1, 지침과 배포는 Task3에 포함했다. 구현 body 대신 인터페이스·assertion·검증 결과만 정했다.
- 실행 방법 선택 전에는 이 두 문서만 저장한다. 커밋 지시는 기존 사용자 선호에 따라 승인 시 실행하는 조건부 단계다.

## Execution record

2026-10-07 사용자 `native` 선택으로 구현했다. 커밋은 별도 요청 전까지 보류한다. 독립 리뷰의 Hint 부록 배율·질문 분할 우선순위·도형 stroke 경계3건은 재현 테스트 후 수정했다. `PageTypography`에는 문제 id별 `appendix_math: list[float]`를 추가하여 부록 페이지 분포가 바뀌어도 Hint entry의 href로 수식을 대응한다. 최종 검증 근거는 `docs/superpowers/reports/2026-10-07-ml-review-pdf-widescreen.md`에 기록한다.
