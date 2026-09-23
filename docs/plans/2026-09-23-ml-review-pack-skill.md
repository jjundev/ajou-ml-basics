# 머신러닝기초 복습팩 스킬 `ml-review-pack` Implementation Plan

> **현재 상태 메모 (2026-09-24):** 아래에서 말하는 참조 구현 폴더 `docs/plans/2026-09-23-ml-review-pack-refs/`(`REFS`)는 스킬이 정본이 된 뒤 커밋 bf6e43e에서 삭제했다. 지금은 `.claude/skills/ml-review-pack/`이 유일한 기준(source of truth)이며, 이 계획서의 `REFS` 경로는 기록으로만 남긴다.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 이 저장소에서 `/ml-review-pack [기간] [lite]`를 한 번 호출하면 0909~0916과 같은 품질의 정리노트·복습문제(HTML+MD+그림)가 `복습노트/`에 만들어지는 프로젝트 스킬을 만든다.

**Architecture:**
- SKILL.md는 0~9단계 절차를 정의한다. 요약·작성·리뷰는 서브에이전트가 맡는다.
- 에이전트는 manifest.json과 HTML 조각 파일만 쓴다.
- 조립(`assemble.py`), 계약 검사(`check_html.py`), MD 변환(`html2md.py`)은 검증된 표준 라이브러리 스크립트로 처리한다.
- 템플릿은 0909~0916 팩의 CSS와 뼈대를 그대로 쓴다.

**Tech Stack:** Python 3.14 표준 라이브러리(unittest, html.parser), PyMuPDF(PDF 텍스트, 기존 설치분), KaTeX 0.16.11, Pretendard 1.3.9(jsdelivr), 인앱 브라우저 도구.

**Spec:** `docs/plans/2026-09-23-ml-review-pack-skill-design.md`

## Global Constraints

- 스킬 루트는 정확히 `.claude/skills/ml-review-pack/`이다. 이하 `SKILL_DIR`이라 부른다.
- 이 계획의 **스크립트, 테스트, 픽스처, 템플릿은 이미 프로토타입으로 검증을 마쳤다.** 원본은 `docs/plans/2026-09-23-ml-review-pack-refs/`에 있다(이하 `REFS`).
  - 각 태스크는 이 파일을 `cp`로 **바이트 그대로** 복사한다. 내용을 다시 타이핑하거나 "개선"하지 않는다.
  - 복사 후 `cmp`로 원본과 같은지 확인한다.
- 스크립트는 표준 라이브러리만 쓴다. sympy는 설치되어 있지 않다. 정답 계산에는 `fractions`를 쓴다.
- 외부 리소스는 `https://cdn.jsdelivr.net/npm/katex@0.16.11/`와 `https://cdn.jsdelivr.net/npm/pretendard@1.3.9/` 접두사만 허용한다.
- 스킬 테스트 명령(저장소 루트에서): `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
- 기존 파일은 수정하지 않는다: `STT/`, `강의노트/`, `교과서/`, `복습노트/`, `scripts/`, `tests/`.
  - 기존 `tests/test_notes_html.py`는 복습노트 이동 때문에 이미 실패한다. 이번 범위가 아니다.
- 한글 경로는 macOS에서 NFD로 저장될 수 있다. 파일명 비교는 항상 `unicodedata.normalize("NFC", …)`로 한다.
- 커밋할 때는 각 태스크가 만든 파일만 스테이징한다(`git add -A` 금지). 커밋 메시지는 다음 줄로 끝낸다.
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

## File Structure

| 파일 | 책임 | 태스크 |
|---|---|---|
| `SKILL_DIR/scripts/manifest.py` | manifest 스키마 검증, 파일명 규칙(`note_name`, `review_name`, `fig_dir_name`), CLI | 1 |
| `SKILL_DIR/tests/_util.py` | 테스트 경로 상수, `find_nfc`, `copy_nfc` | 1 |
| `SKILL_DIR/tests/fixtures/mini-run/**` | 섹션 2개, 토픽 4개, 위젯 1개, 카드 1개짜리 최소 실행 폴더 | 1 |
| `SKILL_DIR/tests/fixtures/manifest-0909-0916.json` | 기존 팩 계약을 manifest로 옮긴 회귀 픽스처 | 1 |
| `SKILL_DIR/assets/{note,review}-template.html` | CSS, 상단바, hero, 슬롯 `{{…}}` | 2 |
| `SKILL_DIR/scripts/assemble.py` | manifest + 조각 → HTML 2개, 스크립트를 body 끝으로 이동 | 2 |
| `SKILL_DIR/scripts/check_html.py` | 공통 검사 + 노트·문제 계약 검사, `Problem(code, where, detail)` | 3 |
| `SKILL_DIR/scripts/html2md.py` | HTML → MD + figures, `check_md` 누락 검사 | 4 |
| `SKILL_DIR/tests/test_regression_0909_0916.py` | 기존 팩에 대한 회귀 테스트 | 5 |
| `SKILL_DIR/references/*.md` | 에이전트 지시문과 작성 규칙 8개 | 6 |
| `SKILL_DIR/SKILL.md`, `SKILL_DIR/tests/test_skill_files.py` | 절차, 스킬 파일 무결성 테스트 | 7 |

---

### Task 1: 브랜치, 스킬 골격, manifest 검증기

**Files:**
- Create: `SKILL_DIR/scripts/manifest.py`
- Create: `SKILL_DIR/tests/_util.py`, `SKILL_DIR/tests/test_manifest.py`
- Create: `SKILL_DIR/tests/fixtures/mini-run/{manifest.json,sections/s1.html,sections/s2.html,cards/p1.html}`
- Create: `SKILL_DIR/tests/fixtures/manifest-0909-0916.json`
- Commit: 설계·계획 문서와 `REFS`

**Interfaces:**
- Produces:
  - `manifest.validate(m: dict) -> list[str]`: 빈 목록이면 유효하다.
  - `manifest.load(path) -> dict`: 오류가 있으면 `manifest.ManifestError`를 던진다.
  - `manifest.note_name(m) -> "정리노트_<range>_<slug>.html"`
  - `manifest.review_name(m) -> "복습문제_<range>_<slug>.html"`
  - `manifest.fig_dir_name(range_) -> "figures_<range>"`
  - `manifest.main(argv) -> int`: 0이면 OK, 1이면 오류, 2이면 사용법 오류.
  - 테스트 헬퍼: `_util.SKILL`, `SCRIPTS`, `FIXTURES`, `MINI_RUN`, `REPO`, `find_nfc(dir, name)`, `copy_nfc(src, dst_dir)`
- manifest 스키마: `REFS/tests/fixtures/mini-run/manifest.json`이 정본 예시다. 필수 키는 `manifest.py`의 `TOP_LEVEL_TYPES`와 `validate`에 있다.

- [ ] **Step 1: 브랜치 생성과 문서 커밋**

```bash
git switch -c feat/ml-review-pack-skill
git add docs/plans/2026-09-23-ml-review-pack-skill-design.md docs/plans/2026-09-23-ml-review-pack-skill.md docs/plans/2026-09-23-ml-review-pack-refs
git commit -m "docs(plan): design, plan and verified reference implementation for ml-review-pack skill

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 2: 테스트와 픽스처 복사(RED)**

```bash
S=.claude/skills/ml-review-pack; R=docs/plans/2026-09-23-ml-review-pack-refs
mkdir -p $S/scripts $S/tests/fixtures
cp $R/tests/_util.py $R/tests/test_manifest.py $S/tests/
cp -R $R/tests/fixtures/mini-run $S/tests/fixtures/
cp $R/tests/fixtures/manifest-0909-0916.json $S/tests/fixtures/
```

- [ ] **Step 3: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
Expected: `ModuleNotFoundError: No module named 'manifest'`로 FAIL

- [ ] **Step 4: 구현 복사**

```bash
cp docs/plans/2026-09-23-ml-review-pack-refs/scripts/manifest.py .claude/skills/ml-review-pack/scripts/
```

- [ ] **Step 5: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
Expected: `test_manifest` 11개 모두 OK

Run: `python3 .claude/skills/ml-review-pack/scripts/manifest.py .claude/skills/ml-review-pack/tests/fixtures/mini-run/manifest.json`
Expected: `OK`

- [ ] **Step 6: (선택) 회귀 픽스처 재생성 검증**

회귀 픽스처는 기존 계약 테스트 상수에서 만든다. 다시 만들어도 결과가 같은지 확인한다. 결과 파일은 커밋하지 않는다.

```bash
python3 docs/plans/2026-09-23-ml-review-pack-refs/make_regression_manifest.py "$PWD" "$TMPDIR/m.json" && cmp "$TMPDIR/m.json" .claude/skills/ml-review-pack/tests/fixtures/manifest-0909-0916.json && echo SAME
```

Expected: `sections 6 problems 10` 다음에 `SAME`

- [ ] **Step 7: 커밋**

```bash
git add .claude/skills/ml-review-pack/scripts/manifest.py .claude/skills/ml-review-pack/tests/_util.py .claude/skills/ml-review-pack/tests/test_manifest.py .claude/skills/ml-review-pack/tests/fixtures
git commit -m "feat(skill): scaffold ml-review-pack with manifest validator

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: 페이지 템플릿과 조립기

**Files:**
- Create: `SKILL_DIR/assets/note-template.html`, `SKILL_DIR/assets/review-template.html`
- Create: `SKILL_DIR/scripts/assemble.py`
- Test: `SKILL_DIR/tests/test_assemble.py`

**Interfaces:**
- Consumes: `manifest.load`, `note_name`, `review_name`
- Produces:
  - `assemble.assemble(run_dir, out_dir) -> (note_path, review_path)`
  - `assemble.fill(template, values) -> str`: 슬롯을 한 번에 치환한다. 값이 없는 슬롯이 있으면 `AssembleError`를 던진다.
  - `assemble.split_scripts(fragment) -> (html, [script…])`
  - `AssembleError`
  - CLI: `assemble.py --run RUN --out 복습노트`
- 조각 파일 규약:
  - 섹션 조각 `RUN/sections/<sid>.html`은 `<article class="topic">`를 나열한 것이다. `<section>`과 `<h2>`는 assemble이 감싼다.
  - 카드 조각 `RUN/cards/<pid>.html`은 `<article class="card">` 하나다.
  - 조각 안의 `{{NOTE_HREF}}`와 `{{REVIEW_HREF}}`는 실제 파일명으로 바뀐다.
- 템플릿 슬롯:
  - 노트: `PAGE_TITLE`, `DESCRIPTION`, `TOC`, `TITLE`, `SUBTITLE`, `SECTIONS`, `FOOTER`, `SCRIPTS`
  - 문제: `PAGE_TITLE`, `DESCRIPTION`, `TOC`, `NOTE_HREF`, `TITLE`, `INTRO`, `TOTAL`, `PARTS`, `FOOTER`, `SCRIPTS`, `RANGE`

- [ ] **Step 1: 테스트 복사(RED)**

```bash
cp docs/plans/2026-09-23-ml-review-pack-refs/tests/test_assemble.py .claude/skills/ml-review-pack/tests/
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p "test_assemble.py" -v`
Expected: `No module named 'assemble'`로 FAIL

- [ ] **Step 3: 템플릿 생성**

기존 0909~0916 HTML의 `<head>`(CSS 포함)를 잘라 템플릿을 만든다. 생성 결과가 REFS와 바이트 단위로 같아야 한다.

```bash
python3 docs/plans/2026-09-23-ml-review-pack-refs/build_templates.py 복습노트 .claude/skills/ml-review-pack/assets
cmp .claude/skills/ml-review-pack/assets/note-template.html docs/plans/2026-09-23-ml-review-pack-refs/assets/note-template.html
cmp .claude/skills/ml-review-pack/assets/review-template.html docs/plans/2026-09-23-ml-review-pack-refs/assets/review-template.html
```

Expected: `note-template.html`과 `review-template.html`을 출력하고, `cmp`는 아무것도 출력하지 않는다.
`복습노트/`가 없거나 `cmp`가 다르면 REFS의 `assets/*.html`을 그대로 복사한다.

- [ ] **Step 4: 조립기 복사**

```bash
cp docs/plans/2026-09-23-ml-review-pack-refs/scripts/assemble.py .claude/skills/ml-review-pack/scripts/
```

- [ ] **Step 5: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
Expected: 19개 OK (manifest 11 + assemble 8)

- [ ] **Step 6: 커밋**

```bash
git add .claude/skills/ml-review-pack/assets .claude/skills/ml-review-pack/scripts/assemble.py .claude/skills/ml-review-pack/tests/test_assemble.py
git commit -m "feat(skill): add page templates and fragment assembler

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: HTML 계약 검사기

**Files:**
- Create: `SKILL_DIR/scripts/check_html.py`
- Test: `SKILL_DIR/tests/test_check_html.py`

**Interfaces:**
- Consumes: `manifest.load`, `note_name`, `assemble.assemble`(테스트에서 사용)
- Produces:
  - `check_html.parse_html(src) -> Doc`, `parse_file(path) -> Doc`
  - `Doc` 필드: `ids`, `containers`, `widgets`, `body_text` 등
  - `Problem(code, where, detail)`
  - `check_common(doc, source, path) -> list[Problem]`
  - `check_note(doc, m)`, `check_review(doc, m)`
  - `check_pack(m, note_path, review_path) -> list[Problem]`, `check_file(path)`
  - `main(argv) -> 0 | 1`
- Problem 코드:
  - 공통: `lang`, `duplicate-id`, `external`, `math`, `broken-link`, `leftover-slot`, `widget-static-missing`
  - 노트: `missing-section`, `missing-topic`, `wrong-section`, `missing-term`, `missing-layer`, `missing-supp`, `forbidden-term`, `missing-link`
  - 문제: `progress`, `missing-card`, `card-source`, `card-anchor`, `card-parts`, `card-term`
- 기존 `scripts/check_notes_html.py`와 다른 점: 블록 태그 경계마다 `\n`을 넣는다. 인접한 `<li>$a$</li><li>$b$</li>`가 `$$`로 오검출되던 결함을 고친 것이다.

- [ ] **Step 1: 테스트 복사(RED)**

```bash
cp docs/plans/2026-09-23-ml-review-pack-refs/tests/test_check_html.py .claude/skills/ml-review-pack/tests/
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p "test_check_html.py" -v`
Expected: `No module named 'check_html'`로 FAIL

- [ ] **Step 3: 구현 복사**

```bash
cp docs/plans/2026-09-23-ml-review-pack-refs/scripts/check_html.py .claude/skills/ml-review-pack/scripts/
```

- [ ] **Step 4: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
Expected: 32개 OK (+13: primitives 4, pack 9)

- [ ] **Step 5: 커밋**

```bash
git add .claude/skills/ml-review-pack/scripts/check_html.py .claude/skills/ml-review-pack/tests/test_check_html.py
git commit -m "feat(skill): add manifest-driven HTML contract checker

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: MD 변환기와 누락 검사

**Files:**
- Create: `SKILL_DIR/scripts/html2md.py`
- Test: `SKILL_DIR/tests/test_html2md.py`

**Interfaces:**
- Consumes: `assemble.assemble`(테스트에서 사용)
- Produces:
  - `html2md.convert_pack(note_html, review_html) -> ([note_md, review_md], fig_count)`
    - 두 HTML은 같은 폴더에 있어야 하고 파일명이 `NAME_RE` 규칙을 따라야 한다. 아니면 `ValueError`를 던진다.
  - `html2md.check_md(html_path, md_path) -> list[str]`: 수식 누락, 앵커 누락, 그림 없음, 링크 파일·앵커 없음을 찾는다.
  - `Ctx(link_map, fig_dir_abs, fig_dir_name)`, `Builder`, `render_table`
  - CLI: `html2md.py NOTE REVIEW [--check]`
- 위젯 규칙:
  - `.widget-static`이 있으면 그 안의 그림과 표를 MD로 옮긴다.
  - 없으면 `*(인터랙티브 — HTML 버전에서 조작)*` 안내만 남긴다.
- 이전 세션의 일회용 변환기(`widget_snapshots.js` 의존, 파일명 하드코딩)를 일반화한 것이다.

- [ ] **Step 1: 테스트 복사(RED)**

```bash
cp docs/plans/2026-09-23-ml-review-pack-refs/tests/test_html2md.py .claude/skills/ml-review-pack/tests/
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p "test_html2md.py" -v`
Expected: `No module named 'html2md'`로 FAIL

- [ ] **Step 3: 구현 복사**

```bash
cp docs/plans/2026-09-23-ml-review-pack-refs/scripts/html2md.py .claude/skills/ml-review-pack/scripts/
```

- [ ] **Step 4: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
Expected: 38개 OK (+6)

- [ ] **Step 5: 커밋**

```bash
git add .claude/skills/ml-review-pack/scripts/html2md.py .claude/skills/ml-review-pack/tests/test_html2md.py
git commit -m "feat(skill): add generic HTML-to-Markdown converter with loss check

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: 0909~0916 회귀 테스트

**Files:**
- Test: `SKILL_DIR/tests/test_regression_0909_0916.py`

**Interfaces:**
- Consumes: `check_html.check_pack`, `html2md.convert_pack`, `html2md.check_md`, `manifest.load`, `_util.find_nfc`, `_util.copy_nfc`
- 알려진 차이는 `KNOWN_CODES = {"widget-static-missing", "broken-link"}`다.
  - `widget-static-missing`: 기존 팩은 스킬 이전에 만들어 `.widget-static`이 없다.
  - `broken-link`: 추가강의 링크가 폴더 이동으로 깨져 있다.
  - 이 두 코드 말고 다른 코드가 나오면 실패다.
- `복습노트/`에 파일이 없으면 스킵한다.

- [ ] **Step 1: 테스트 복사**

```bash
cp docs/plans/2026-09-23-ml-review-pack-refs/tests/test_regression_0909_0916.py .claude/skills/ml-review-pack/tests/
```

- [ ] **Step 2: 실행**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
Expected: 40개 OK. 회귀 2개가 **skipped가 아니어야** 한다. skipped이면 `복습노트/` 경로와 NFC 처리를 확인한다.

- [ ] **Step 3: 커밋**

```bash
git add .claude/skills/ml-review-pack/tests/test_regression_0909_0916.py
git commit -m "test(skill): regression against the hand-built 0909-0916 pack

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: 에이전트 지시문과 작성 규칙(references)

**Files:**
- Create: `SKILL_DIR/references/stt-summary-prompt.md`
- Create: `SKILL_DIR/references/manifest-guide.md`
- Create: `SKILL_DIR/references/content-rules.md`
- Create: `SKILL_DIR/references/widget-rules.md`
- Create: `SKILL_DIR/references/problem-selection.md`
- Create: `SKILL_DIR/references/card-rules.md`
- Create: `SKILL_DIR/references/review-prompt.md`
- Create: `SKILL_DIR/references/browser-check.md`

아래 8개 파일을 **내용 그대로** 만든다. 각 파일 블록의 첫 줄 주석은 파일 경로 표시이므로 파일에 넣지 않는다. 꺾쇠 `<…>` 부분은 SKILL.md 실행 때 메인 에이전트가 채우는 자리이고, 파일에는 그대로 둔다.

- [ ] **Step 1: `references/stt-summary-prompt.md`**

````markdown
# STT 요약 에이전트 지시문

메인 에이전트는 날짜마다 아래 브리프로 에이전트 1명을 띄운다(병렬, model: opus / lite: sonnet).

---
머신러닝기초(정방철 교수님) <MMDD> 수업 녹음 전사를 정밀 요약한다.

- 입력(읽기 전용): `<RUN>/repo/STT/<MMDD 머러기.md>` — **처음부터 끝까지 전부** 읽는다. 건너뛰지 않는다.
- 대조 자료: `<RUN>/repo/강의노트/<LectureXX_*.pdf>` 슬라이드 텍스트(메인이 추출해 `<RUN>/slides.txt`에 둠)
- 출력: `<RUN>/summaries/stt-<MMDD>.md` 한 파일만 쓴다. 다른 곳에는 쓰지 않는다.

출력 형식:
1. `# <MMDD> 머신러닝기초 강의 개요 (정방철 교수, <YYYY-MM-DD>)`
2. **총평**: 녹음 길이, 이번 수업이 다룬 강의자료와 슬라이드 범위(예: "L02 s7–12"), **시작하지 않은** 슬라이드, 흐름 한 줄.
3. 흐름 순서대로 `## N. 제목 (Part PP MM:SS–MM:SS)` 절. 각 절에:
   - **핵심 내용**: 정의, 식(TeX `$…$`), 칠판 유도 단계. 슬라이드에 없는 설명은 `[슬라이드 외]` 표시.
   - **비유와 일화**: 개념을 싣는 비유만. 순수 잡담(화장실, 자리, 이메일, 가격 등)은 쓰지 않는다.
   - **학생과의 대화**: 학생 이름은 "한 학생".
   - ⚠️ 강조 발언: 원문 인용 + `(MM:SS)`. "중요", "시험", "꼭" 같은 표현이 붙은 발언은 모두.
   - "나중에 할게요/유도는 생략" 처럼 **미룬 유도**는 `🕳️ 미룬 유도:`로 표시.
4. `## 슬라이드 대조표`: | 슬라이드 | 다룸/일부/예고만/안 다룸 | 근거 타임스탬프 |
5. `## 용어·식 목록`: 수업에서 실제로 쓴 용어와 식을 TeX 그대로 나열(정리노트 required_terms 후보).
6. `## 말실수 정정`: STT 오인식 또는 교수님 말실수와 올바른 형태.

보고: 파일 경로와 총평 3줄만 돌려준다.
---
````

- [ ] **Step 2: `references/manifest-guide.md`**

````markdown
# manifest.json 작성 규칙 (메인 에이전트)

manifest는 이번 팩의 계약이다. 작성자, 검사기, 조립기가 모두 이 파일을 기준으로 삼는다.
정본 예시: `tests/fixtures/mini-run/manifest.json`, 실제 규모 예시: `tests/fixtures/manifest-0909-0916.json`.
작성 후 반드시 `python3 <SKILL>/scripts/manifest.py <RUN>/manifest.json` → `OK`.

## 최상위
| 키 | 값 |
|---|---|
| `course` | `"머신러닝기초"` |
| `range` | `"0921"` 또는 `"0921-0923"` (첫 STT–마지막 STT 날짜) |
| `slug` | 이번 범위 대표 강의자료 제목의 영문 밑줄 형태, 예: `"Linear_Regression"`. 두 강의자료에 걸치면 뒤쪽 것 |
| `note_title` | `"<주제> — 5살도 이해하는 정리노트"` |
| `note_subtitle` | `"정방철 교수님 머신러닝기초 · 0921 · 0923 수업 (Lecture02~03, MML 9장)"` 형식 |
| `review_title` | `"복습문제 N선 — <range 물결표기> 수업 범위"` |
| `review_intro` | HTML 허용. 문제 구성(본문 예제 변형 몇 개, 연습문제 몇 개)과 "먼저 풀고 💡 힌트, 그다음 ✅ 풀이" 안내 |
| `footer_note` | HTML 허용. `출처: 정방철 교수님 강의자료(LectureXX–YY) · 수업 녹음 전사(MMDD…) · Deisenroth, Faisal, Ong, <i>Mathematics for Machine Learning</i> (2020) N장.` |
| `footer_review` | HTML 허용. `출처: Deisenroth, Faisal, Ong, <i>Mathematics for Machine Learning</i> (Cambridge University Press, 2020). 풀이는 자체 작성이며 수치는 Python으로 검증했습니다.` |
| `sessions` | 날짜별 `{date, stt, summary, slides}` |

## sections / topics
- 섹션 id는 `s0`, `s1`, … 순서. 마지막 섹션은 항상 "요약 · 예고"이며 토픽 `s<N>-cheatsheet`, `s<N>-next`, `s<N>-links`를 둔다.
- 섹션은 **개념 순서(슬라이드 로드맵)** 로 묶는다. 날짜는 토픽 태그로만 드러낸다.
- 토픽 id는 `s<n>-<kebab>`(영문 소문자). 토픽 하나 = 슬라이드 1~3장 또는 칠판 유도 하나.
- `short`는 상단 목차 글자(예: `"2 최소제곱"`), `title`은 `"2. 최소제곱법"`.
- `layers`: 개념 토픽은 `["eli5", "formal", "prof"]`. 교수님 발언이 없으면 `prof` 대신 빼되 이유를 보고서 "스킬이 정한 사항"에 적는다. 요약·예고 섹션 토픽은 `[]`.
- `supp`: 요약의 `🕳️ 미룬 유도`를 보충으로 싣는 토픽만 `true`.
- `required_terms`: 토픽당 3~9개. 요약의 **용어·식 목록과 강조 발언**에서 고른다.
  - 식은 작성자가 **공백까지 그대로** 쓸 TeX 문자열이다(예: `"\\boldsymbol{\\theta}_{\\text{ML}}"`).
  - 교수님 비유의 핵심 단어(예: `"김밥"`)를 최소 하나 넣어 🎙️ 레이어 누락을 잡는다.
- `preview_topic`: `s<N>-next`.
- `forbidden_outside_preview`: 슬라이드 대조표에서 "예고만/안 다룸"인 슬라이드의 핵심 용어 3~8개. 본문에 나오면 검사 실패.

## parts / problems
- `parts`: `partA`(교과서 본문 예제 변형), `partB`(교과서 연습문제). 한쪽이 0개면 그 part는 뺀다.
- 문제 선별은 `references/problem-selection.md`. 개수 8~12.
- `source`: `"MML Example 9.1"` / `"MML Exercise 6.3"` 정확히 이 형식. `variant`: 본문 예제를 문제로 바꿨으면 `true`.
- `anchor`: 풀이가 기대는 정리노트 토픽 id. `level`: 1~3. `date`: 관련 수업 날짜.
- `terms`: 카드에 반드시 나올 TeX/숫자(정답 포함).
- `answer`: Python으로 계산한 정답 문자열. 계산 예:
  ```bash
  python3 -c "from fractions import Fraction as F; print(F(2,10), F(2+3,10+6))"
  ```
  계산 스크립트를 `<RUN>/answers.py`로 남기고 보고서에 경로를 적는다.

## links
- `{"topic": "s<N>-links", "href": "<복습문제 파일명>"}`는 항상.
- 확률 개념(Bayes, prior, MLE/MAP, 조건부확률)이 나오면 추가강의 eli5 링크를 건다:
  `../강의노트/추가%20강의/eli5_lecture10_statistical_inference_part1.html`, `…lecture11_statistical_inference_part2.html`, `…lecture12_statistical_inference_part3.html`
- 이전 복습팩과 이어지는 개념이면 `정리노트_<이전 range>_<slug>.html#<토픽>` 링크를 건다(같은 `복습노트/` 폴더).
````

- [ ] **Step 3: `references/content-rules.md`**

````markdown
# 섹션 작성 규칙

## 작성자 브리프 (메인 에이전트가 섹션마다 1명, 병렬, model: opus / lite: sonnet)

---
머신러닝기초 정리노트의 섹션 `<sid>`(`<섹션 title>`)를 쓴다.

- 읽기: `<SKILL>/references/content-rules.md`(이 파일 전체), 위젯이 있으면 `<SKILL>/references/widget-rules.md`
- 계약: `<RUN>/manifest.json`의 섹션 `<sid>` — 토픽 id·제목·`required_terms`·`layers`·`supp`가 정확히 여기 적힌 대로여야 한다.
- 근거: `<RUN>/summaries/stt-*.md`(해당 날짜), `<RUN>/slides.txt`, 필요하면 MML `<RUN>/repo/교과서/Mathematics_for_Machine_Learning.pdf` <쪽>
- 출력: `<RUN>/sections/<sid>.html` **한 파일만**. `<section>`/`<h2>`는 쓰지 않는다(조립기가 감싼다).
- 자기 검사(끝내기 전): 토픽별로 `required_terms`가 모두 문자 그대로 들어갔는지, `$` 짝, 금지어 `<forbidden 목록>`이 없는지.
- 보고: 파일 경로, 토픽별 한 줄, 요약에 있었지만 넣지 않은 것과 이유.
---

## 범위
- 요약의 슬라이드 대조표에서 "다룸/일부"인 내용만 쓴다. "예고만/안 다룸"은 `s<N>-next`에 제목만.
- 수업에서 말한 모든 개념, 칠판 유도, 교수님 비유와 강조 발언을 빠짐없이 싣는다(잡담 제외).
- STT 오인식과 말실수는 올바른 형태로 쓴다. 식이 틀렸던 경우만 각주 한 줄로 "(수업 중 X로 적었다가 정정)".

## 토픽 마크업 (이 순서)
```html
<article class="topic" id="…"><h3>…</h3><div class="tags"><span class="tag date">📅 MMDD</span><span class="tag slide">L0X sN</span></div>
  <div class="layer eli5"><span class="layer-title">🧸 쉽게 말하면</span><p class="lead">한 문장 비유</p> …그림… </div>
  <div class="layer formal"><span class="layer-title">📐 정식 버전</span> …정의·수식·단계별 유도(ol.steps)… </div>
  <div class="layer prof"><span class="layer-title">🎙️ 교수님 한마디</span> …비유·일화, 원문은 blockquote… </div>
  <div class="layer warn"><span class="layer-title">⚠️ 강조 포인트</span> …원문 인용 + (MMDD MM:SS)… </div>   ← 강조 발언이 있을 때만
  <div class="layer supp"><span class="badge supp">📎 보충 · 수업 미유도</span> … </div>             ← manifest supp=true만
</article>
```
- 요약·예고 섹션: 치트시트는 표(`<div class="table-wrap"><table>`), 예고는 `<ul>`, 링크는 `<ul><li><a>`.
- 복습문제 링크는 `href="{{REVIEW_HREF}}"`로 쓴다(조립기가 실제 파일명으로 바꾼다).

## 문체
- 🧸: 초등학생이 이해할 1~3문장 + 그림. 전문용어 없이. "~예요" 체.
- 📐: 빠짐없이, 정확하게. 유도는 한 줄에 한 단계. "~다" 체.
- 🎙️/⚠️: 원문 인용은 15단어 안팎으로 줄이고 `(0914 26:00)`처럼 출처.
- UI 글은 한국어, 전문용어는 영어 병기(예: 과적합(overfitting)).

## 수식
- `$…$`(인라인), `$$…$$`(디스플레이)만. 본문에 리터럴 `$` 금지.
- TeX 안에 `<`, `>`, `&` 금지 → `\lt`, `\gt`. 정렬 환경 대신 `$$` 줄을 나눈다.
- 벡터는 `\mathbf{x}`, 파라미터 벡터는 `\boldsymbol{\theta}`, 행렬 `\mathbf{X}` — manifest `required_terms`와 같은 표기.

## SVG 그림
- 개념 토픽마다 🧸 레이어에 그림 1개 이상(흐름도, 막대, 곡선 등).
- `<figure class="figure"><svg id="fig-<kebab>" viewBox="…" role="img" aria-label="한국어 설명">…</svg><figcaption>…</figcaption></figure>`
- 색은 클래스로만: `fig-ink`, `fig-accent`, `fig-danger`, `fig-dot`, `fig-text`, `fig-muted`. 하드코딩 색 금지(다크모드).
- 글자 12~14px, SVG `<text>`에 `$` 금지(θ, σ, ₁ 같은 유니코드).
- id는 페이지 전체에서 유일해야 한다(`fig-` + 토픽 고유 단어).
````

- [ ] **Step 4: `references/widget-rules.md`**

````markdown
# 위젯 규칙

## 언제
- 팩 전체에 0~2개. "슬라이더를 움직이면 개념이 보이는" 경우만(예: λ와 과적합, prior 강도와 MAP).
- manifest에는 적지 않는다. 섹션 작성자가 판단하고 보고에 적는다.

## 마크업
```html
<div class="widget" id="widget-<name>"><h4>🎛️ 직접 해보기: …</h4>
  <p class="widget-help">무엇을 움직이면 무엇이 보이는지 한 문장.</p>
  <div class="controls">
    <label>차수 <input type="range" id="<name>-a" min="1" max="9" step="1" value="3"> <b id="<name>-a-val">3</b></label>
  </div>
  <svg id="<name>-plot" viewBox="0 0 560 300" role="img" aria-label="…"></svg>
  <p class="readout">… <b id="<name>-out">…</b></p>
  <p class="legend"><span><span class="sw fit"></span>설명</span>…</p>
  <div class="widget-static" hidden>
    <figure class="figure"><svg id="widget-<name>-static-1" viewBox="0 0 560 300" role="img" aria-label="대표 설정 1">…</svg></figure>
    <div class="table-wrap"><table><tr><th>설정</th><th>결과</th></tr><tr><td>…</td><td>…</td></tr></table></div>
  </div>
</div>
<script id="widget-<name>-ui">(function () { /* 수학 + 그리기, 전역 오염 금지 */ })();</script>
```
- 스크립트는 조각 파일 끝에 둔다. 조립기가 `</body>` 앞으로 옮긴다. 외부 라이브러리 금지.
- 그래프 선·점은 템플릿 CSS 클래스(`axis`, `tick`, `plot-truth`, `plot-fit`, `pt-train`, `pt-test`, `plot-like`, `plot-prior`, `plot-post`, `mark-ml`, `mark-map`, `fig-*`)를 쓴다.

## `.widget-static` (필수 — 없으면 check_html이 실패)
- MD 버전과 인쇄에서 위젯 대신 보이는 정적 대체물. `hidden` 속성으로 HTML에서는 숨긴다.
- 대표 설정 2~4개의 정적 SVG(위젯과 같은 모양, 스크립트 없이 path 좌표를 미리 계산해 박아 넣음)와 결과 표.
- 대표 설정의 수치는 **위젯 스크립트와 같은 수학**으로 계산한다: 위젯 수학을 `<RUN>/widget_<name>.js`로 저장하고 `node`로 실행해 좌표·값을 뽑는다.
- 정적 SVG id는 `widget-<name>-static-<n>`(파일명이 된다).
````

- [ ] **Step 5: `references/problem-selection.md`**

````markdown
# 문제 선별 규칙 (MML 전용)

## 원칙
- 문제는 **MML 교과서에서만** 가져온다. 자작 문제 금지. 숫자만 바꾼 변형은 본문 예제(`variant: true`)에 한해 허용하고 카드에 "변형" 배지를 단다.
- 수업에서 배운 내용만으로 풀 수 있어야 한다. 풀이에 수업에서 안 다룬 개념이 한 단계라도 필요하면 제외.
- 8~12문항. 난이도 ★(개념 확인) : ★★(계산) : ★★★(도전) ≈ 5 : 4 : 1.

## 수업 범위가 Part II(8~12장)일 때 — Part II에는 연습문제가 없다
1. **Part A**: 그 장 본문의 `Example N.M` 중 수업에서 다룬 것을 문제로 바꾼다(`variant: true`). 원문은 카드의 📖 원문 토글에 짧게.
2. **Part B**: Part I(2~7장) 연습문제 중 **핵심 개념이 수업에서 다뤄진 것**만. 예: MLE/MAP를 배웠으면 6장 Beta-Bernoulli, 조건부확률; 최소제곱을 배웠으면 5장 기울기, 7장 정상점.
3. 이전 복습팩에서 이미 쓴 문제는 다시 쓰지 않는다(`복습노트/복습문제_*.html`의 `data-source` 확인).

## 수업 범위가 Part I(2~7장)일 때
- 그 장의 연습문제를 우선하고, 본문 Example은 보조로.

## 위치 찾기
- 연습문제 PDF: `교과서/연습문제/Chapter_0{2..7}_*_Exercises.pdf`(없으면 아래 목차 방법).
- MML 목차의 `Exercises` 항목(PDF 1-기준 쪽): 2장 70, 3장 102, 4장 143, 5장 176, 6장 228, 7장 253. **책 쪽 = PDF 쪽 − 6.**
- 스니펫:
  ```bash
  python3 - <<'EOF'
  import fitz, re
  d = fitz.open("교과서/Mathematics_for_Machine_Learning.pdf")
  print([(t, p) for lvl, t, p in d.get_toc() if t == "Exercises"])
  first = {}
  for i in range(d.page_count):
      for m in re.finditer(r"Example (\d+)\.(\d+)", d[i].get_text()):
          first.setdefault(m.group(0), i + 1)
  print({k: v for k, v in first.items() if k.startswith("Example 9.")})  # 필요한 장
  EOF
  ```
  `Example N.M`의 첫 등장 쪽이 본문 참조일 수 있으니 해당 쪽을 열어 예제 본문인지 확인한다.

## 정답
- 모든 수치 정답은 `fractions.Fraction`(필요하면 `math`)으로 계산해 manifest `answer`와 카드 `terms`에 넣는다.
- 기호 정답(식)은 풀이 단계를 역으로 대입해 한 번 더 확인한다.
````

- [ ] **Step 6: `references/card-rules.md`**

````markdown
# 문제 카드 규칙

## 작성자 브리프 (메인 에이전트가 1명, model: opus / lite: sonnet)

---
머신러닝기초 복습문제 카드를 쓴다.

- 읽기: `<SKILL>/references/card-rules.md`(이 파일 전체), `<SKILL>/references/problem-selection.md`의 원칙
- 계약: `<RUN>/manifest.json`의 `problems` — id, `source`, `anchor`, `level`, `date`, `terms`, `answer`를 그대로 따른다.
- 근거: MML PDF `<RUN>/repo/교과서/Mathematics_for_Machine_Learning.pdf`(문제별 쪽은 manifest 옆 `<RUN>/problem-pages.txt`), 정답 계산 `<RUN>/answers.py`, 정리노트 토픽 제목은 manifest
- 출력: `<RUN>/cards/<pid>.html` 문제마다 한 파일. 다른 곳에 쓰지 않는다.
- 자기 검사: 카드별 `terms`가 문자 그대로 있는지, 정답이 `answer`와 같은지, `$` 짝.
- 보고: 카드별 한 줄(출처, 정답), 풀이 중 수업 밖 개념이 필요했던 곳.
---

## 마크업
```html
<article class="card" id="pN" data-source="MML Example 9.1">
  <header class="card-head"><span class="badge src">MML Example 9.1 변형</span><span class="badge level">★</span><span class="tag date">📅 MMDD</span></header>
  <h3>PN. 제목</h3>
  <div class="problem">…한국어 문제… 여러 문항이면 <ol><li>(a) …</li><li>(b) …</li></ol></div>
  <details class="original"><summary>📖 교과서 원문</summary>"…원문 짧게…" — Example 9.1</details>
  <details class="hint"><summary>💡 힌트</summary>…한두 문장…</details>
  <details class="solution"><summary>✅ 풀이</summary><ol class="steps"><li>…</li></ol><p class="answer">정답: …</p></details>
  <p class="link-back">🔗 수업과 연결: <a href="{{NOTE_HREF}}#ANCHOR">토픽 제목</a> — 한 줄 설명</p>
  <label class="done"><input type="checkbox" data-done="pN"> 풀었음</label>
</article>
```
- `data-source`는 manifest `source`와 글자까지 같다. 배지 글자에는 `variant: true`면 " 변형"을 붙인다.
- 난이도 배지: level 1 `★`, 2 `★★`, 3 `★★★ 도전`.
- 원문 인용은 한 카드에 25단어 이내.
- 풀이 마지막 단계에 "수업과의 연결"을 한 줄로(어느 수업의 어떤 말/식과 이어지는지).
- 수식 규칙은 `content-rules.md`의 "수식"과 같다.
````

- [ ] **Step 7: `references/review-prompt.md`**

````markdown
# 리뷰어 지시문 (lite에서는 생략)

---
머신러닝기초 복습팩 초안을 검토한다. 파일은 수정하지 않는다.

- 대상: `<RUN>/repo/복습노트/<정리노트 html>`, `<…/복습문제 html>`
- 근거: `<RUN>/summaries/stt-*.md`, `<RUN>/slides.txt`, `<RUN>/manifest.json`, `<RUN>/answers.py`, MML PDF
- 규칙: `<SKILL>/references/content-rules.md`, `card-rules.md`, `problem-selection.md`

확인할 것:
1. **사실 오류**: 식, 정의, 부호, 조건(예: "대칭/비대칭", "항상/보통")이 요약·슬라이드·교과서와 맞는가.
2. **누락**: 요약의 핵심 내용·강조 발언·미룬 유도 중 노트에 없는 것.
3. **범위**: "예고만/안 다룸" 내용이 본문에 설명되어 있는가.
4. **ELI5 품질**: 🧸 레이어가 전문용어 없이 1~3문장인가, 그림이 개념을 실제로 보여 주는가.
5. **문제**: 출처(`Example`/`Exercise` 번호)가 실제 교과서와 맞는가, 수업 범위로 풀 수 있는가, 정답이 `answers.py`와 같은가(직접 다시 계산).
6. **표현**: 표 첫 열이 한 글자씩 줄바꿈되거나 빈 칸이 있는 표, 잘린 문장.

출력 형식(이것만):
```
## Critical
- [s2-affine] 문제 → 고칠 내용
## Important
- [p3] …
## Minor
- …
```
각 항목은 토픽/카드 id로 시작한다. 없으면 "없음".
---
````

- [ ] **Step 8: `references/browser-check.md`**

````markdown
# 브라우저 검증 (메인 에이전트)

## 서버
file:// 미리보기에서는 스크립트가 돌지 않는다. 빈 포트로 서버를 띄운다.
```bash
PORT=$(python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1])")
python3 -m http.server $PORT --directory "<RUN>/repo" >/dev/null 2>&1 &   # run_in_background
```
URL: `http://localhost:$PORT/복습노트/<파일명>` (한글 그대로). 끝나면 서버를 종료한다.

## 정리노트 (`mcp__Claude_Browser__javascript_tool`)
```js
await new Promise((r) => setTimeout(r, 1500));
const textNodes = Array.from(document.querySelectorAll('main *')).filter((e) => !['SCRIPT', 'STYLE'].includes(e.tagName) && !e.closest('[hidden]'));
({
  katex: document.querySelectorAll('.katex').length,
  katexErrors: document.querySelectorAll('.katex-error').length,
  rawDollar: textNodes.some((e) => Array.from(e.childNodes).some((n) => n.nodeType === 3 && n.textContent.includes('$'))),
  hScroll: document.documentElement.scrollWidth > window.innerWidth,
  widgets: Array.from(document.querySelectorAll('.widget')).map((w) => ({ id: w.id, drawn: Array.from(w.querySelectorAll('svg')).some((s) => !s.closest('[hidden]') && s.childElementCount > 0) })),
})
```
통과: `katexErrors: 0`, `rawDollar: false`, `hScroll: false`, 모든 위젯 `drawn: true`. `read_console_messages`에 오류 없음.

위젯마다 슬라이더 하나를 바꾸고(`input` 이벤트) readout 값이 `.widget-static` 표의 같은 설정 값과 같은지 확인한다.

## 모바일·다크
`resize_window`(`preset: "mobile"`, `colorScheme: "dark"`) → 새로고침 → 위 스크립트 재실행(`hScroll: false`) → 스크린샷으로 그림·위젯 글자가 보이는지 확인 → `preset: "desktop"`, `colorScheme: "light"`로 되돌린다.

## 복습문제
```js
await new Promise((r) => setTimeout(r, 1500));
document.querySelectorAll('details').forEach((d) => { d.open = true; });
await new Promise((r) => setTimeout(r, 300));
({
  cards: document.querySelectorAll('article.card').length,
  katexErrors: document.querySelectorAll('.katex-error').length,
  hScroll: document.documentElement.scrollWidth > window.innerWidth,
})
```
통과: `cards`가 manifest 문제 수, `katexErrors: 0`, `hScroll: false`. 첫 카드의 "수업과 연결" 링크를 눌러 노트 토픽으로 이동하는지 확인.
````

- [ ] **Step 9: 커밋**

```bash
git add .claude/skills/ml-review-pack/references
git commit -m "docs(skill): add agent briefs and authoring rules for ml-review-pack

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: SKILL.md와 스킬 파일 무결성 테스트

**Files:**
- Create: `SKILL_DIR/SKILL.md`
- Test: `SKILL_DIR/tests/test_skill_files.py`

**Interfaces:**
- Consumes: Task 1~6의 모든 파일 경로
- Produces: `SKILL.md`. frontmatter의 `name`은 `ml-review-pack`이다. 본문에서 언급하는 `references/*.md`와 `scripts/*.py`는 모두 실제로 있어야 한다.

- [ ] **Step 1: 실패하는 테스트 작성**

`.claude/skills/ml-review-pack/tests/test_skill_files.py`:

```python
"""SKILL.md 형식과, 본문이 가리키는 파일이 모두 있는지 확인한다."""

import re
import unittest

from _util import SKILL

SKILL_MD = SKILL / "SKILL.md"


class TestSkillFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL_MD.read_text(encoding="utf-8")

    def test_frontmatter(self):
        m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", self.text)
        self.assertIsNotNone(m, "frontmatter는 name, description 두 줄")
        self.assertEqual(m.group(1), "ml-review-pack")
        self.assertIn("정리노트", m.group(2))
        self.assertIn("복습문제", m.group(2))
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_referenced_files_exist(self):
        refs = set(re.findall(r"(?:references|scripts|assets)/[\w.-]+\.(?:md|py|html)", self.text))
        self.assertGreaterEqual(len(refs), 12)
        for rel in sorted(refs):
            with self.subTest(rel=rel):
                self.assertTrue((SKILL / rel).exists(), rel)

    def test_every_reference_is_used(self):
        for path in sorted((SKILL / "references").glob("*.md")):
            with self.subTest(ref=path.name):
                self.assertIn(f"references/{path.name}", self.text)

    def test_steps_present(self):
        for n in range(10):
            with self.subTest(step=n):
                self.assertRegex(self.text, rf"\n### {n}\. ")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p "test_skill_files.py" -v`
Expected: `FileNotFoundError`(SKILL.md 없음)로 ERROR

- [ ] **Step 3: SKILL.md 작성**

`.claude/skills/ml-review-pack/SKILL.md`(아래 내용 그대로):

````markdown
---
name: ml-review-pack
description: 머신러닝기초 수업의 STT·강의노트·MML 교과서로 ELI5 정리노트 HTML과 교과서 기반 복습문제 HTML(+MD, 그림)을 만들어 복습노트/에 저장한다. "정리노트", "복습문제", "복습팩", "0921~0923 정리해줘"처럼 머신러닝기초 수업 정리를 요청하거나 /ml-review-pack [MMDD|MMDD-MMDD] [lite]로 부를 때 사용한다.
---

# 머신러닝기초 복습팩

수업 녹음 전사(STT)와 강의자료, MML 교과서로 한 기간의 복습팩을 만든다. 중간에 사용자에게 묻지 않고 끝에 한 번 보고한다. 커밋은 제안만 한다.

**산출물** (`복습노트/`):
`정리노트_<range>_<slug>.html`, `복습문제_<range>_<slug>.html`, 같은 이름의 `.md` 두 개, `figures_<range>/`

**인자**: `[MMDD | MMDD-MMDD] [lite]`
- `lite`: 작성자·요약 에이전트를 sonnet으로, 6단계 리뷰를 생략한다. 기계 검사와 브라우저 검사는 그대로 한다.

**진행 표시**: 단계마다 한 줄만 쓴다. 예: `3/9 작성 중: 섹션 5개 + 카드 10개 (병렬)`

**경로 약속**
- `SKILL` = 이 파일이 있는 폴더(`.claude/skills/ml-review-pack`)의 절대 경로
- `REPO` = 저장소 루트
- `RUN` = `<scratchpad>/review-pack/<range>/`

## 절차

### 0. 준비
1. `REPO`에 `STT/`, `강의노트/`, `교과서/Mathematics_for_Machine_Learning.pdf`가 모두 있는지 확인한다. 하나라도 없으면 "머신러닝기초 저장소에서만 동작합니다"라고 알리고 멈춘다.
2. STT 목록은 NFC로 읽는다. macOS에는 NFD 파일명이 섞여 있다.
   ```bash
   python3 -c "import os,unicodedata,re;print(sorted(re.match(r'(\d{4})',unicodedata.normalize('NFC',f)).group(1) for f in os.listdir('STT') if unicodedata.normalize('NFC',f).endswith('머러기.md')))"
   ```
3. 기간을 정한다.
   - 인자가 있으면 그 기간을 쓴다.
   - 인자가 없으면 `복습노트/정리노트_<range>_*.html` 중 가장 늦은 끝 날짜를 찾고, 그 뒤의 STT를 모두 쓴다.
   - 해당 STT가 하나도 없으면 사용 가능한 날짜를 보여 주고 멈춘다.
   - `range`는 첫 STT 날짜 하나이거나 `첫-끝` 형식이다.
4. 실행 폴더를 만든다. 서브에이전트에게는 `RUN`, `RUN/repo`, `SKILL` 경로만 넘긴다.
   ```bash
   mkdir -p "$RUN"/{summaries,sections,cards} && ln -sfn "$REPO" "$RUN/repo"
   ```
   에이전트는 `RUN` 밖에 쓰지 않는다. `복습노트/`에는 메인 에이전트만 쓴다.

### 1. 범위 파악
- STT 날짜마다 요약 에이전트 1명을 **병렬로** 띄운다. 브리프는 `references/stt-summary-prompt.md`에 있다.
- 에이전트가 도는 동안 메인 에이전트는 다음을 한다.
  - 관련 `강의노트/Lecture*.pdf` 텍스트를 슬라이드 번호와 함께 `RUN/slides.txt`에 추출한다(PyMuPDF, 쪽마다 `=== LXX sN ===`).
  - 추출에 실패하면 STT만으로 진행하고 보고서에 적는다.
  - MML에서 관련 장과 Example·연습문제 위치를 찾는다(`references/problem-selection.md`의 스니펫).

### 2. manifest
- 요약들의 슬라이드 대조표와 용어·식 목록으로 `RUN/manifest.json`을 쓴다. 규칙은 `references/manifest-guide.md`에 있다.
- 문제 선별은 `references/problem-selection.md`를 따른다.
  - 정답은 `RUN/answers.py`(`fractions`)로 계산한다.
  - 문제별 교과서 쪽은 `RUN/problem-pages.txt`에 적는다.
- 검증: `python3 "$SKILL/scripts/manifest.py" "$RUN/manifest.json"` 결과가 `OK`여야 한다.

### 3. 작성
- 섹션마다 작성자 1명을 띄운다. 브리프는 `references/content-rules.md`, 위젯 규칙은 `references/widget-rules.md`에 있다.
- 문제 작성자 1명이 모든 카드를 쓴다. 브리프는 `references/card-rules.md`에 있다.
- 모두 **한 메시지에서 병렬로** 띄운다. 모델은 opus, `lite`이면 sonnet이다.
- 브리프의 `<…>` 자리는 실제 경로, id, 금지어 목록으로 채운다.

### 4. 조립
```bash
python3 "$SKILL/scripts/assemble.py" --run "$RUN" --out "$REPO/복습노트"
```

### 5. 기계 검사
```bash
cd "$REPO/복습노트" && python3 "$SKILL/scripts/check_html.py" --manifest "$RUN/manifest.json" --note "<정리노트>.html" --review "<복습문제>.html"
```
- `FAIL`이면 Problem의 `where`(토픽 id, 카드 id, 섹션 id)로 담당 작성자를 찾는다.
- 그 작성자에게 문제 목록을 보내 조각을 고치게 한다(SendMessage, 안 되면 같은 브리프로 새 에이전트).
- 고친 뒤 4단계부터 다시 한다. 최대 2회까지이며, 그래도 남으면 "미해결"로 보고한다.

### 6. 리뷰 (`lite`면 생략)
- 리뷰어 1명을 띄운다. 브리프는 `references/review-prompt.md`에 있다.
- Critical과 Important는 모두, Minor는 쉬운 것만 고친다.
- 담당 작성자별로 **한 번에 모아서** 수정을 요청한다. 수정은 한 번만 한다.
- 수정 후 4~5단계를 다시 한다. 반영하지 않은 항목은 보고서에 적는다.

### 7. 브라우저 검증
- `references/browser-check.md`대로 한다.
  - http.server를 빈 포트에 띄운다.
  - 확인: KaTeX 오류 0, 남은 `$` 없음, 375px에서 가로 스크롤 없음, 다크모드, 위젯, 링크, 콘솔 오류
- 결함은 5단계와 같은 방식으로 작성자에게 되돌린다. 이것도 최대 2회 규칙에 포함된다.
- 끝나면 서버를 종료한다.

### 8. MD 변환
```bash
cd "$REPO/복습노트" && python3 "$SKILL/scripts/html2md.py" "<정리노트>.html" "<복습문제>.html" --check
```
- `OK`가 나와야 한다.
- 누락이 나오면 대부분 HTML 조각의 마크업 문제다(수식이 `svg`나 `.controls` 안에 있는 경우 등). 조각을 고치고 4단계부터 다시 한다.

### 9. 보고
다음 형식으로 끝낸다.
```
## 복습팩 <range> 완료
- 파일: 복습노트/… (html 2, md 2, figures_<range>/ N개)
- 범위: 배운 슬라이드 … / 예고만: …
- 문제: P1 MML Example 9.1 변형(★) … (정답은 RUN/answers.py로 검증)
- 스킬이 정한 사항: slug, 섹션 구성, 위젯, 뺀 내용과 이유
- 미해결: … (없으면 "없음")
- 커밋 제안: git add 복습노트/<파일들> && git commit -m "docs(notes): add review pack <range>"
```
실행 폴더 경로(`RUN`)도 적는다. 수정이 필요하면 조각을 고쳐 4단계부터 다시 돌리면 된다.

## 오류 처리
| 상황 | 동작 |
|---|---|
| 저장소가 아님 | 알리고 멈춤 |
| 기간에 해당하는 STT 없음 | 사용 가능한 날짜를 보여 주고 멈춤 |
| PDF 텍스트 추출 실패 | STT만으로 진행하고 보고서에 표시 |
| 포트 사용 중 | 다른 빈 포트 사용 |
| 같은 이름의 팩이 이미 있음 | 덮어쓰기 전에 기존 파일을 `RUN/previous/`에 복사하고 보고서에 적음 |
| 검사 2회 실패 | 멈추지 않고 나머지 단계를 끝낸 뒤 "미해결"로 보고 |
````

- [ ] **Step 4: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
Expected: 44개 OK (+4). 회귀 테스트 2개는 skipped가 아니어야 한다.

- [ ] **Step 5: 스킬 로드 확인**

Claude Code가 이 스킬을 인식하는지 확인한다. 새 세션이나 `/skills` 목록에서 `ml-review-pack`이 보이면 된다. 확인할 수 없으면 보고서에 "새 세션에서 확인 필요"라고 적는다.

- [ ] **Step 6: 커밋**

```bash
git add .claude/skills/ml-review-pack/SKILL.md .claude/skills/ml-review-pack/tests/test_skill_files.py
git commit -m "feat(skill): add ml-review-pack SKILL.md procedure

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: 압력 테스트와 인수 실행(0921)

**Files:**
- 스킬 수정은 발견된 결함이 있을 때만 한다. 해당 references나 SKILL.md를 고치고, 테스트를 다시 통과시킨 뒤 커밋한다.
- 결과물 `복습노트/*_0921_*`은 **커밋하지 않는다.** 커밋 여부는 사용자가 정한다.

- [ ] **Step 1: 인수 실행**

`/ml-review-pack 0921`을 실행한다. 이 세션에서 SKILL.md 절차를 그대로 따른다.
0921 STT(`STT/0921 머러기.md`)는 이미 있다. 이 날짜의 범위는 L02 후반이나 L03 초반일 것으로 예상되지만, 실제 범위는 요약으로 정한다.

Expected:
- 5단계 `check_html` OK
- 7단계 브라우저 검사 통과
- 8단계 `html2md --check` OK
- 9단계 보고서 출력

- [ ] **Step 2: 압력 검사(보고서와 결과물 대조)**

아래를 직접 확인하고 결과를 목록으로 남긴다.
1. 요약의 슬라이드 대조표에서 "예고만"인 슬라이드의 핵심 용어가 정리노트 본문에 없고 `s<N>-next`에만 있다.
2. 모든 카드의 `data-source`가 실제 MML의 Example이나 Exercise 번호다. PDF에서 두 개를 무작위로 골라 확인한다.
3. 자작 문제가 없다.
4. `answers.py`를 다시 실행한 값이 카드의 정답과 같다.
5. `.widget`이 있다면 `.widget-static` 표의 값과 브라우저 readout이 같다.

어긋나는 항목이 있으면 원인이 된 references 규칙을 고친다. 예를 들어 금지어 선정 규칙이 약했다면 `manifest-guide.md`를 보강한다. 테스트를 다시 돌린 뒤 커밋한다.

```bash
git add .claude/skills/ml-review-pack/references .claude/skills/ml-review-pack/SKILL.md
git commit -m "fix(skill): tighten rules found in 0921 acceptance run

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 3: 참조 구현 정리**

이제 스킬이 정본이므로 계획용 참조 복사본을 지운다. 계획 문서의 `REFS` 경로 설명은 git 히스토리로 추적할 수 있다.

```bash
git rm -r docs/plans/2026-09-23-ml-review-pack-refs
git commit -m "chore(plan): drop reference copies now that the skill is canonical

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 4: 최종 테스트**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
Expected: 44개 OK

---

## Self-Review 결과

- **Spec coverage**:

  | 설계 항목 | 태스크 |
  |---|---|
  | 위치(#3) | Global, T1 |
  | 입력과 기본 기간(#4) | T7 SKILL 0단계 |
  | 출력 이름(#5) | T1 `note_name`, T2 |
  | 범위와 금지어(#6) | T3 `forbidden-term`, T6 manifest-guide, T8 압력 테스트 |
  | MML 문제(#7) | T6 problem-selection, card-rules |
  | 조각 병렬 작성과 조립(#8) | T2, T7 3~4단계 |
  | 실행 폴더(#9) | T7 0단계 |
  | 검증 계층(#10) | T3, T6 review/browser, T7 5~8단계 |
  | MD와 widget-static(#11) | T4, T6 widget-rules |
  | 템플릿(#12) | T2 |
  | 커밋 제안만(#13) | T7 9단계 |
  | NFC(#14) | T1 `_util`, T7 0단계 |
  | 테스트(#15) | T1~T5, T7 |
  | lite(#17) | T7 인자 |
  | 끝에 보고(#18) | T7 9단계 |
  | 오류 처리 | T7 표 |
  | 인수 실행 | T8 |

- **Placeholder scan**:
  - 코드는 REFS의 검증된 파일을 `cp`와 `cmp`로 옮긴다.
  - 문서와 SKILL.md는 전문을 적었다.
  - `<…>`는 런타임에 채우는 브리프 슬롯이며, 그렇다고 명시했다.
- **Type consistency**: 모든 태스크의 테스트가 프로토타입에서 함께 통과했다(40개). 함수명과 슬롯명은 Interfaces 블록과 REFS 코드가 일치한다.
