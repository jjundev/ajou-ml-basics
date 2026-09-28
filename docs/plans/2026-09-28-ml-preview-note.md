# ml-preview-note 예습노트 스킬 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 강의노트 PDF와 MML 교과서로 수업 중 옆에 띄울 짧은 예습노트 HTML(+MD)을 만드는 별도 스킬 `ml-preview-note`를 만든다.

**Architecture:** 새 스킬은 `ml-review-pack`의 `note-template.html`을 상대 심링크로 공유하고, 복습 스킬 `scripts/`의 공용 함수(`fill`, `check_common`, `check_note`, `html2md.convert` 등)를 import하는 얇은 래퍼 스크립트 5개로 manifest 검증·Lecture 선택·조립·검사·MD 변환을 한다. 복습 스킬 쪽 변경은 템플릿의 `{{BRAND}}` 슬롯과 `.layer.listen` 스타일 추가뿐이다.

**Tech Stack:** Python 3.14 표준 라이브러리(unittest, html.parser), PyMuPDF 1.27(SKILL.md 스니펫에서만), KaTeX 0.16.11, 인앱 브라우저 도구.

**Spec:** `docs/plans/2026-09-28-ml-preview-note-design.md`

## Global Constraints

- 스크립트는 표준 라이브러리만 쓴다. PyMuPDF(`fitz`)는 SKILL.md의 셸 스니펫에서만 쓴다.
- 테스트 명령(저장소 루트에서): `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-preview-note/tests -v`, 복습 스킬은 `-s .claude/skills/ml-review-pack/tests`.
- 출력: `예습노트/<Lxx>/예습노트_<Lxx>_<slug>.html`, 같은 이름 `.md`, `figures_<Lxx>/`. Lecture id 형식은 `L\d{2}`.
- 페이지 제목 `머신러닝기초 예습노트 <Lxx>`, 브랜드 `예습노트`, `data-range="<Lxx>"`.
- 레이어는 `eli5`(제목 "쉽게 말하면"), `formal`("정확히 말하면"), `listen`("들을 때 포인트"), 보충은 `layer supp` + `<span class="badge supp">교과서 보충</span>`. `prof`/`warn` 레이어는 쓰지 않는다.
- 분량: 토픽 본문 600자 이하(공백·TeX·그림·레이어 제목·배지·태그·요약 패널 제외), eli5 2문장 이하, listen 항목 2개 이하.
- 위젯 0개, 이모지 금지, 문체는 "~해요" 체.
- 템플릿은 `../../ml-review-pack/assets/note-template.html` 상대 심링크. 복습 스킬 변경은 추가만 하고, 복습 스킬 테스트 72개가 계속 통과해야 한다.
- 에이전트 모델: 작성자 opus(`lite`면 sonnet), GPT이면 sol/luna. 리뷰어는 기본으로 켜고 `lite`면 생략.
- 커밋 메시지는 Conventional Commits, 끝에 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. 최신 Lecture의 예습노트가 이미 있을 때 인자 없이 실행 → 지난 Lecture로 내려가지 않고 멈추며 ajou-bb 확인을 안내해야 한다. (Task 3 `test_latest_already_done_stops`)
2. 같은 번호의 원본 PDF와 `_rev` PDF가 함께 있을 때 → `_rev`를 고르고 slug에서 `_rev`를 뺀다. (Task 3 `test_prefers_rev_and_strips_suffix`)
3. macOS에서 `예습노트` 폴더 이름이 NFD일 때 → 기존 노트 감지와 백업이 그 폴더를 찾아야 한다. (Task 3 `test_nfd_notes_dir_detected`)
4. 수식이 많은 formal 레이어 → TeX는 600자 분량에서 빠져서 식 위주 토픽이 억울하게 실패하지 않는다. (Task 5 `test_math_not_counted`)
5. 다시 MD 변환할 때 이전 실행의 SVG가 남는 경우 → 고아 SVG를 지운다. (Task 6 `test_orphan_svgs_removed`)

---

### Task 1: 공유 템플릿에 `{{BRAND}}` 슬롯과 `.layer.listen` 스타일 추가 (복습 스킬)

**Files:**
- Modify: `.claude/skills/ml-review-pack/assets/note-template.html:86,89-90,324`
- Modify: `.claude/skills/ml-review-pack/scripts/assemble.py:63-73`
- Test: `.claude/skills/ml-review-pack/tests/test_assemble.py`

**Interfaces:**
- Consumes: 없음
- Produces: 템플릿 슬롯 집합 `{BRAND, DESCRIPTION, FOOTER, PAGE_TITLE, RANGE, SCRIPTS, SECTIONS, SUBTITLE, TITLE, TOC}`, CSS 클래스 `.layer.listen`. Task 2의 가드 테스트와 Task 4의 조립기가 이 슬롯 집합에 의존한다.

- [ ] **Step 0: 브랜치 만들기**

```bash
git switch -c feat/ml-preview-note
```

- [ ] **Step 1: 실패하는 테스트 작성** — `test_assemble.py`의 `TestAssemble` 클래스 안, `test_sections_toc_and_titles` 아래에 추가:

```python
    def test_brand_slot_filled(self):
        self.assertIn('<strong class="brand">정리노트</strong>', self.note_html)

    def test_listen_layer_styled(self):
        # 예습노트(ml-preview-note)가 같은 템플릿을 쓴다
        self.assertIn(".layer.listen", self.note_html)
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p "test_assemble.py" -v`
Expected: `test_listen_layer_styled` FAIL (`.layer.listen` 없음). `test_brand_slot_filled`는 지금은 하드코딩이라 PASS.

- [ ] **Step 3: 템플릿 수정** — `note-template.html`

324행:
```html
      <strong class="brand">{{BRAND}}</strong>
```
86행을:
```css
    .layer.prof, .layer.warn, .layer.listen { font-size: var(--fs-sub); line-height: 1.7; }
```
89~90행을:
```css
    .layer.warn, .layer.listen { background: var(--surface); border-top: 0; border-radius: var(--radius); padding: var(--s4); }
    .layer.warn .layer-title { color: var(--warn); font-size: var(--fs-body); }
    .layer.listen .layer-title { color: var(--accent-ink); font-size: var(--fs-body); }
```
(89~90행 원문의 속성은 그대로이고, 89행 선택자에 `.layer.listen`을 더한 것과 `.layer.listen .layer-title` 한 줄이 추가분이다.)

- [ ] **Step 4: 조립기 수정** — `assemble.py` `build_note`의 `fill(...)` 값 사전에 한 줄 추가:

```python
        "BRAND": "정리노트",
```
(`"PAGE_TITLE"` 줄 바로 아래)

- [ ] **Step 5: 복습 스킬 전체 테스트 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
Expected: `Ran 74 tests ... OK (skipped=2)` (새 테스트 2개 포함, `leftover-slot` 없음)

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/ml-review-pack/assets/note-template.html .claude/skills/ml-review-pack/scripts/assemble.py .claude/skills/ml-review-pack/tests/test_assemble.py
git commit -m "$(cat <<'EOF'
feat(skill): brand slot and listen layer in shared note template

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: 예습 스킬 뼈대 + manifest 검증기

**Files:**
- Create: `.claude/skills/ml-preview-note/assets/note-template.html` (심링크)
- Create: `.claude/skills/ml-preview-note/scripts/_review.py`
- Create: `.claude/skills/ml-preview-note/scripts/preview_manifest.py`
- Create: `.claude/skills/ml-preview-note/tests/_util.py`
- Create: `.claude/skills/ml-preview-note/tests/fixtures/mini-run/manifest.json`
- Create: `.claude/skills/ml-preview-note/tests/fixtures/mini-run/sections/s0.html`, `s1.html`, `s2.html`
- Test: `.claude/skills/ml-preview-note/tests/test_template.py`, `tests/test_manifest.py`

**Interfaces:**
- Consumes: 복습 `scripts/manifest.py`의 `ManifestError`, `_need(obj, key, typ, where, errors) -> bool`, `_strings(items, where, errors)`, `_objects(items, where, errors)` (제너레이터 `(i, dict)`)
- Produces:
  - `_review.REVIEW_SCRIPTS: Path` (import하면 `sys.path`에 추가됨)
  - `preview_manifest.ManifestError`, `validate(m: dict) -> list[str]`, `load(path) -> dict`, `note_name(m) -> str` (`"예습노트_<lecture>_<slug>.html"`), `fig_dir_name(lecture: str) -> str` (`"figures_<lecture>"`), `main(argv) -> int`
  - 테스트 도우미 `tests/_util.py`: `TESTS, SKILL, SCRIPTS, FIXTURES, MINI_RUN, REPO, REVIEW_SKILL`
  - 픽스처 `MINI_RUN`: lecture `L99`, slug `Mini_Preview`, 섹션 `s0`/`s1`/`s2`, 토픽 `s0-vector`, `s1-mean`(slides `s2–3`, 레이어 eli5·formal·listen, 그림 1개), `s1-var`(slides `s4`, supp), `s2-cheatsheet`, `s2-links`

- [ ] **Step 1: 폴더와 템플릿 심링크**

```bash
mkdir -p .claude/skills/ml-preview-note/{assets,scripts,references,tests/fixtures/mini-run/sections}
ln -s ../../ml-review-pack/assets/note-template.html .claude/skills/ml-preview-note/assets/note-template.html
```

- [ ] **Step 2: 테스트 도우미** — `tests/_util.py`

```python
"""예습 스킬 테스트 공통 경로."""

from __future__ import annotations

from pathlib import Path
import sys

TESTS = Path(__file__).resolve().parent
SKILL = TESTS.parent
SCRIPTS = SKILL / "scripts"
FIXTURES = TESTS / "fixtures"
MINI_RUN = FIXTURES / "mini-run"
REPO = SKILL.parents[2]  # <repo>/.claude/skills/ml-preview-note
REVIEW_SKILL = SKILL.parent / "ml-review-pack"
sys.path.insert(0, str(SCRIPTS))
```

- [ ] **Step 3: 실패하는 템플릿 가드 테스트** — `tests/test_template.py`

```python
"""공유 템플릿(심링크)이 예습 조립기가 기대하는 모양인지 지킨다. 복습 쪽에서 템플릿을 바꾸면 여기서 먼저 깨진다."""

import os
import re
import unittest

from _util import REVIEW_SKILL, SKILL

TEMPLATE = SKILL / "assets" / "note-template.html"
SLOTS = {"BRAND", "DESCRIPTION", "FOOTER", "PAGE_TITLE", "RANGE", "SCRIPTS", "SECTIONS", "SUBTITLE", "TITLE", "TOC"}


class TestSharedTemplate(unittest.TestCase):
    def test_relative_symlink_to_review_template(self):
        self.assertTrue(TEMPLATE.is_symlink())
        self.assertEqual(os.readlink(TEMPLATE), "../../ml-review-pack/assets/note-template.html")
        self.assertEqual(TEMPLATE.resolve(), (REVIEW_SKILL / "assets" / "note-template.html").resolve())

    def test_slots(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertEqual(set(re.findall(r"\{\{([A-Z_]+)\}\}", text)), SLOTS)

    def test_layer_styles(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        for sel in (".layer.eli5", ".layer.formal", ".layer.listen", ".badge.supp"):
            with self.subTest(sel=sel):
                self.assertIn(sel, text)
```

Run: `python3 -m unittest discover -s .claude/skills/ml-preview-note/tests -p "test_template.py" -v`
Expected: PASS (Task 1 이후라면). FAIL이면 Task 1이 빠진 것이다.

- [ ] **Step 4: 픽스처 manifest** — `tests/fixtures/mini-run/manifest.json`

```json
{
 "course": "머신러닝기초",
 "lecture": "L99",
 "slug": "Mini_Preview",
 "pdf": "강의노트/Lecture99_Mini_Preview.pdf",
 "note_title": "Mini — 수업 전에 보는 예습노트",
 "note_subtitle": "테스트용 · Lecture99 예습",
 "footer_note": "출처: 테스트 픽스처",
 "sections": [
  {"id": "s0", "title": "0. 미리 알아둘 것", "short": "0 미리", "topics": [
   {"id": "s0-vector", "title": "벡터", "slides": "s1", "required_terms": ["\\mathbf{x} \\in \\mathbb{R}^D"], "layers": ["eli5", "formal"], "supp": false}
  ]},
  {"id": "s1", "title": "1. 평균과 분산", "short": "1 평균", "topics": [
   {"id": "s1-mean", "title": "평균", "slides": "s2–3", "required_terms": ["\\bar{x} = \\frac{1}{N}\\sum_{n=1}^{N} x_n", "무게중심"], "layers": ["eli5", "formal", "listen"], "supp": false},
   {"id": "s1-var", "title": "분산", "slides": "s4", "required_terms": ["\\sigma^2"], "layers": ["eli5", "formal"], "supp": true}
  ]},
  {"id": "s2", "title": "2. 한눈에 보기", "short": "2 한눈에", "topics": [
   {"id": "s2-cheatsheet", "title": "치트시트", "slides": "", "required_terms": ["\\sigma^2"], "layers": [], "supp": false},
   {"id": "s2-links", "title": "함께 보면 좋은 자료", "slides": "", "required_terms": [], "layers": [], "supp": false}
  ]}
 ],
 "links": [{"topic": "s2-links", "href": "#s1-mean"}]
}
```

- [ ] **Step 5: 픽스처 조각 3개**

`sections/s0.html`:
```html
      <article class="topic" id="s0-vector"><h3>벡터</h3><div class="tags"><span class="tag slide">L99 s1</span></div>
        <div class="layer eli5"><span class="layer-title">쉽게 말하면</span><p class="lead">벡터는 숫자를 한 줄로 세운 묶음이에요.</p></div>
        <div class="layer formal"><span class="layer-title">정확히 말하면</span><p>$\mathbf{x} \in \mathbb{R}^D$는 실수 $D$개를 모은 열벡터예요.</p></div>
        <div class="sum" hidden>
          <p class="sum-lead">벡터는 숫자 묶음이에요.</p>
        </div>
      </article>
```

`sections/s1.html`:
```html
      <article class="topic" id="s1-mean"><h3>평균</h3><div class="tags"><span class="tag slide">L99 s2–3</span></div>
        <div class="layer eli5"><span class="layer-title">쉽게 말하면</span><p class="lead">평균은 시소의 무게중심이에요.</p>
          <figure class="figure"><svg id="fig-seesaw" viewBox="0 0 120 40" role="img" aria-label="시소를 나타내는 선"><line x1="10" y1="30" x2="110" y2="30" class="fig-ink"/></svg><figcaption>시소가 평평해지는 곳이 평균이에요.</figcaption></figure>
        </div>
        <div class="layer formal"><span class="layer-title">정확히 말하면</span><p>$$\bar{x} = \frac{1}{N}\sum_{n=1}^{N} x_n$$</p></div>
        <div class="layer listen"><span class="layer-title">들을 때 포인트</span><ul><li>무게중심 비유가 나오면 위 식과 연결해 보세요.</li></ul></div>
        <div class="sum" hidden>
          <p class="sum-lead">평균은 값들의 가운데예요.</p>
          <p class="panel-label">핵심 식</p>
          <ul class="eq-list"><li><span class="eq-name">표본 평균</span>$$\bar{x} = \frac{1}{N}\sum_{n=1}^{N} x_n$$</li></ul>
        </div>
      </article>
      <article class="topic" id="s1-var"><h3>분산</h3><div class="tags"><span class="tag slide">L99 s4</span></div>
        <div class="layer eli5"><span class="layer-title">쉽게 말하면</span><p class="lead">분산은 흩어진 정도예요.</p></div>
        <div class="layer formal"><span class="layer-title">정확히 말하면</span><p>$\sigma^2 = \frac{1}{N}\sum_{n}(x_n - \bar{x})^2$</p></div>
        <div class="layer supp"><span class="badge supp">교과서 보충</span><p>$N-1$로 나누는 표본분산은 MML 6.4절에 있어요.</p></div>
        <div class="sum" hidden>
          <p class="sum-lead">분산은 평균에서 얼마나 퍼졌는지예요.</p>
          <p class="panel-label">용어</p>
          <dl class="terms"><dt>분산(variance)</dt><dd>평균과의 차이를 제곱해 평균낸 값</dd></dl>
        </div>
      </article>
```

`sections/s2.html`:
```html
      <article class="topic" id="s2-cheatsheet"><h3>치트시트</h3>
        <div class="table-wrap"><table><tr><th>개념</th><th>식</th></tr><tr><td>분산</td><td>$\sigma^2$</td></tr></table></div>
      </article>
      <article class="topic" id="s2-links"><h3>함께 보면 좋은 자료</h3>
        <ul><li><a href="#s1-mean">평균 다시 보기</a></li></ul>
      </article>
```

- [ ] **Step 6: 실패하는 manifest 테스트** — `tests/test_manifest.py`

```python
import copy
import io
import json
from contextlib import redirect_stdout
import unittest

from _util import MINI_RUN

import preview_manifest as pm

BASE = json.loads((MINI_RUN / "manifest.json").read_text(encoding="utf-8"))


def errors_with(mutate):
    m = copy.deepcopy(BASE)
    mutate(m)
    return pm.validate(m)


class TestPreviewManifest(unittest.TestCase):
    def test_fixture_valid(self):
        self.assertEqual(pm.validate(BASE), [])
        self.assertEqual(pm.load(MINI_RUN / "manifest.json")["lecture"], "L99")

    def test_names(self):
        self.assertEqual(pm.note_name(BASE), "예습노트_L99_Mini_Preview.html")
        self.assertEqual(pm.fig_dir_name("L99"), "figures_L99")

    def test_missing_top_level_key(self):
        errs = errors_with(lambda m: m.pop("pdf"))
        self.assertTrue(any("manifest.pdf" in e for e in errs), errs)

    def test_bad_lecture(self):
        errs = errors_with(lambda m: m.update(lecture="L4"))
        self.assertTrue(any("manifest.lecture" in e for e in errs), errs)

    def test_stt_layer_rejected(self):
        errs = errors_with(lambda m: m["sections"][1]["topics"][0]["layers"].append("prof"))
        self.assertTrue(any("알 수 없는 레이어" in e for e in errs), errs)

    def test_concept_topic_needs_eli5_and_formal(self):
        errs = errors_with(lambda m: m["sections"][1]["topics"][0].update(layers=["eli5", "listen"]))
        self.assertTrue(any("eli5와 formal" in e for e in errs), errs)

    def test_slides_format(self):
        for bad in ("12", "s2-3", "s", ""):
            with self.subTest(slides=bad):
                errs = errors_with(lambda m: m["sections"][1]["topics"][0].update(slides=bad))
                self.assertTrue(any(".slides" in e for e in errs), errs)

    def test_section_ids_in_order(self):
        errs = errors_with(lambda m: m["sections"][0].update(id="s9"))
        self.assertTrue(any("s0이어야 함" in e for e in errs), errs)

    def test_topic_id_prefix(self):
        errs = errors_with(lambda m: m["sections"][1]["topics"][0].update(id="s0-mean"))
        self.assertTrue(any("s1-로 시작" in e for e in errs), errs)

    def test_last_section_needs_cheatsheet_and_links(self):
        errs = errors_with(lambda m: m["sections"][2]["topics"].pop(0))
        self.assertTrue(any("s2-cheatsheet" in e for e in errs), errs)

    def test_single_section_rejected(self):
        errs = errors_with(lambda m: m.update(sections=m["sections"][:1]))
        self.assertTrue(any("2개 이상" in e for e in errs), errs)

    def test_supp_on_summary_topic_rejected(self):
        errs = errors_with(lambda m: m["sections"][2]["topics"][0].update(supp=True))
        self.assertTrue(any(".supp" in e for e in errs), errs)

    def test_link_to_unknown_topic(self):
        errs = errors_with(lambda m: m["links"].append({"topic": "s7-x", "href": "#a"}))
        self.assertTrue(any("없는 토픽" in e for e in errs), errs)

    def test_cli_ok(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = pm.main([str(MINI_RUN / "manifest.json")])
        self.assertEqual((code, out.getvalue().strip()), (0, "OK"))
```

- [ ] **Step 7: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-preview-note/tests -p "test_manifest.py" -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'preview_manifest'`

- [ ] **Step 8: `_review.py` 작성**

```python
"""ml-review-pack의 scripts/를 import 경로에 넣는다. 양식·검사 로직을 복습 스킬과 공유하기 위해서다."""

from pathlib import Path
import sys

REVIEW_SCRIPTS = Path(__file__).resolve().parents[2] / "ml-review-pack" / "scripts"
if not REVIEW_SCRIPTS.is_dir():
    raise ImportError(f"ml-review-pack 스킬 없음: {REVIEW_SCRIPTS}")
if str(REVIEW_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(REVIEW_SCRIPTS))
```

- [ ] **Step 9: `preview_manifest.py` 작성**

```python
#!/usr/bin/env python3
"""
예습노트 manifest.json 로더·검증기 (표준 라이브러리만 사용).

manifest는 한 번의 실행(Lecture 하나)에 대한 계약이다. preview_assemble.py와 preview_check.py가 읽는다.
CLI: preview_manifest.py RUN/manifest.json   (검증만, 오류가 있으면 목록 출력 후 종료 코드 1)
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _review  # noqa: E402,F401  (ml-review-pack/scripts를 import 경로에 넣는다)
from manifest import ManifestError, _need, _objects, _strings  # noqa: E402  (복습 스킬 공용 도우미)

LAYER_NAMES = {"eli5", "formal", "listen"}
CONCEPT_LAYERS = {"eli5", "formal"}
TOP_LEVEL_TYPES = {
    "course": str, "lecture": str, "slug": str, "pdf": str,
    "note_title": str, "note_subtitle": str, "footer_note": str,
    "sections": list, "links": list,
}
LECTURE_RE = re.compile(r"L\d{2}")
SLUG_RE = re.compile(r"[A-Za-z0-9_]+")
ID_RE = re.compile(r"[A-Za-z][A-Za-z0-9-]*")
SLIDES_RE = re.compile(r"s\d+(–\d+)?")  # 범위는 en dash(–)


def validate(m: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(m, dict):
        return ["manifest: JSON 객체 필요"]
    for key, typ in TOP_LEVEL_TYPES.items():
        _need(m, key, typ, "manifest", errors)
    if errors:
        return errors
    if not LECTURE_RE.fullmatch(m["lecture"]):
        errors.append(f"manifest.lecture: L와 두 자리 숫자여야 함: {m['lecture']}")
    if not SLUG_RE.fullmatch(m["slug"]):
        errors.append(f"manifest.slug: 영문·숫자·밑줄만: {m['slug']}")
    if len(m["sections"]) < 2:
        errors.append("sections: '미리 알아둘 것'과 '한눈에 보기'를 포함해 2개 이상 필요")

    seen: set[str] = set()
    topic_ids: set[str] = set()

    def new_id(value: str, where: str) -> None:
        if not ID_RE.fullmatch(value):
            errors.append(f"{where}: id 형식 오류: {value}")
        if value in seen:
            errors.append(f"{where}: 중복 id: {value}")
        seen.add(value)

    for i, sec in _objects(m["sections"], "sections", errors):
        where = f"sections[{i}]"
        if not all([_need(sec, "id", str, where, errors), _need(sec, "title", str, where, errors),
                    _need(sec, "short", str, where, errors), _need(sec, "topics", list, where, errors)]):
            continue
        new_id(sec["id"], where)
        if sec["id"] != f"s{i}":
            errors.append(f"{where}.id: s{i}이어야 함: {sec['id']}")
        for j, t in _objects(sec["topics"], f"{where}.topics", errors):
            tw = f"{where}.topics[{j}]"
            ok = all([_need(t, "id", str, tw, errors), _need(t, "title", str, tw, errors),
                      _need(t, "slides", str, tw, errors), _need(t, "required_terms", list, tw, errors),
                      _need(t, "layers", list, tw, errors), _need(t, "supp", bool, tw, errors)])
            if not ok:
                continue
            new_id(t["id"], tw)
            topic_ids.add(t["id"])
            if not t["id"].startswith(f"{sec['id']}-"):
                errors.append(f"{tw}.id: {sec['id']}-로 시작해야 함: {t['id']}")
            _strings(t["required_terms"], f"{tw}.required_terms", errors)
            if not all(isinstance(x, str) for x in t["layers"]):
                errors.append(f"{tw}.layers: 문자열 목록이어야 함")
                continue
            unknown = set(t["layers"]) - LAYER_NAMES
            if unknown:
                errors.append(f"{tw}.layers: 알 수 없는 레이어 {sorted(unknown)}")
            if t["layers"]:
                if not CONCEPT_LAYERS <= set(t["layers"]):
                    errors.append(f"{tw}.layers: 개념 토픽은 eli5와 formal 필요")
                if not SLIDES_RE.fullmatch(t["slides"]):
                    errors.append(f"{tw}.slides: s12 또는 s12–14(en dash) 형식이어야 함: {t['slides']!r}")
            elif t["supp"]:
                errors.append(f"{tw}.supp: 레이어가 없는 토픽은 false여야 함")

    last = m["sections"][-1] if m["sections"] else None
    if isinstance(last, dict) and isinstance(last.get("id"), str) and isinstance(last.get("topics"), list):
        ids = {t.get("id") for t in last["topics"] if isinstance(t, dict)}
        for suffix in ("cheatsheet", "links"):
            if f"{last['id']}-{suffix}" not in ids:
                errors.append(f"sections[-1]: 토픽 {last['id']}-{suffix} 필요")

    for i, link in _objects(m["links"], "links", errors):
        where = f"links[{i}]"
        if _need(link, "topic", str, where, errors) and link["topic"] not in topic_ids:
            errors.append(f"{where}.topic: 없는 토픽: {link['topic']}")
        _need(link, "href", str, where, errors)
    return errors


def load(path: Path | str) -> dict:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise ManifestError(f"{path}: 파일을 읽을 수 없음: {e}") from e
    try:
        m = json.loads(text)
    except json.JSONDecodeError as e:
        raise ManifestError(f"{path}: JSON 형식 오류: {e}") from e
    errors = validate(m)
    if errors:
        raise ManifestError("\n".join(errors))
    return m


def note_name(m: dict) -> str:
    return f"예습노트_{m['lecture']}_{m['slug']}.html"


def fig_dir_name(lecture: str) -> str:
    return f"figures_{lecture}"


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("사용법: preview_manifest.py RUN/manifest.json", file=sys.stderr)
        return 2
    try:
        load(argv[0])
    except ManifestError as e:
        print(e)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 10: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-preview-note/tests -v`
Expected: `test_template` 3개 + `test_manifest` 14개 모두 PASS

- [ ] **Step 11: Commit**

```bash
git add .claude/skills/ml-preview-note
git commit -m "$(cat <<'EOF'
feat(skill): ml-preview-note scaffold and manifest validator

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Lecture 선택과 기존 예습노트 백업

**Files:**
- Create: `.claude/skills/ml-preview-note/scripts/preview_files.py`
- Test: `.claude/skills/ml-preview-note/tests/test_files.py`

**Interfaces:**
- Consumes: 없음(표준 라이브러리만)
- Produces:
  - `PickError(RuntimeError)`
  - `lecture_pdfs(repo) -> dict[str, tuple[Path, str]]` (`{"L03": (pdf 경로, slug)}`, 번호순)
  - `has_note(repo, lecture: str) -> bool`
  - `pick(repo, lecture: str | None = None) -> tuple[str, Path, str]` (`(lecture, pdf, slug)`)
  - `backup(repo, lecture: str, run) -> Path | None`
  - CLI `pick --repo R [--lecture Lxx]` → 표준출력 `Lxx<TAB>pdf<TAB>slug`, `backup --repo R --lecture Lxx --run RUN`, 오류는 표준에러 + 종료 코드 1

- [ ] **Step 1: 실패하는 테스트** — `tests/test_files.py`

```python
import io
from contextlib import redirect_stderr, redirect_stdout
import os
from pathlib import Path
import tempfile
import unicodedata
import unittest

import _util  # noqa: F401  (scripts 경로)
import preview_files as pf


class TestPick(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        self.lectures = self.repo / "강의노트"
        self.lectures.mkdir()
        for name in ("Lecture00_Course_Overview.pdf", "Lecture01_When_Models_Meet_Data_Part1.pdf",
                     "Lecture03_Linear_Regression_Part1.pdf", "Lecture03_Linear_Regression_Part1_rev.pdf", "notes.txt"):
            (self.lectures / name).write_bytes(b"%PDF")

    def tearDown(self):
        self._tmp.cleanup()

    def make_note(self, lecture, dir_name="예습노트"):
        d = self.repo / dir_name / lecture
        d.mkdir(parents=True)
        (d / f"예습노트_{lecture}_X.html").write_text("<html></html>", encoding="utf-8")

    def test_lists_lectures(self):
        self.assertEqual(list(pf.lecture_pdfs(self.repo)), ["L00", "L01", "L03"])

    def test_prefers_rev_and_strips_suffix(self):
        lec, pdf, slug = pf.pick(self.repo)
        self.assertEqual((lec, pdf.name, slug), ("L03", "Lecture03_Linear_Regression_Part1_rev.pdf", "Linear_Regression_Part1"))

    def test_explicit_lecture(self):
        lec, pdf, slug = pf.pick(self.repo, "L01")
        self.assertEqual((lec, slug), ("L01", "When_Models_Meet_Data_Part1"))

    def test_unknown_lecture_lists_available(self):
        with self.assertRaises(pf.PickError) as cm:
            pf.pick(self.repo, "L07")
        self.assertIn("L00, L01, L03", str(cm.exception))

    def test_latest_already_done_stops(self):
        self.make_note("L03")
        with self.assertRaises(pf.PickError) as cm:
            pf.pick(self.repo)
        self.assertIn("이미", str(cm.exception))
        self.assertIn("ajou-bb", str(cm.exception))
        self.assertEqual(pf.pick(self.repo, "L03")[0], "L03")  # 명시하면 다시 만들 수 있다

    def test_nfd_notes_dir_detected(self):
        self.make_note("L03", dir_name=unicodedata.normalize("NFD", "예습노트"))
        self.assertTrue(pf.has_note(self.repo, "L03"))

    def test_no_lectures_dir(self):
        with tempfile.TemporaryDirectory() as empty:
            with self.assertRaises(pf.PickError):
                pf.pick(empty)

    def test_cli_pick(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = pf.main(["pick", "--repo", str(self.repo)])
        self.assertEqual(code, 0)
        lec, pdf, slug = out.getvalue().strip().split("\t")
        self.assertEqual((lec, Path(pdf).name, slug), ("L03", "Lecture03_Linear_Regression_Part1_rev.pdf", "Linear_Regression_Part1"))

    def test_cli_error_exit_code(self):
        err = io.StringIO()
        with redirect_stderr(err):
            code = pf.main(["pick", "--repo", str(self.repo), "--lecture", "L07"])
        self.assertEqual(code, 1)
        self.assertIn("L07", err.getvalue())


class TestBackup(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "repo"
        self.run = Path(self._tmp.name) / "run"
        self.run.mkdir(parents=True)
        self.dir = self.repo / "예습노트" / "L03"
        self.dir.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def test_nothing_to_back_up(self):
        self.assertIsNone(pf.backup(self.repo, "L03", self.run))
        self.assertIsNone(pf.backup(self.repo, "L04", self.run))  # 폴더 자체가 없음

    def test_copies_only_this_lecture(self):
        (self.dir / "예습노트_L03_A.html").write_text("a", encoding="utf-8")
        (self.dir / "예습노트_L03_A.md").write_text("a", encoding="utf-8")
        (self.dir / "figures_L03").mkdir()
        (self.dir / "figures_L03" / "f.svg").write_text("<svg/>", encoding="utf-8")
        (self.dir / "memo.txt").write_text("x", encoding="utf-8")
        dst = pf.backup(self.repo, "L03", self.run)
        self.assertTrue(dst.name.startswith("previous-"))
        self.assertEqual(sorted(p.name for p in dst.iterdir()), ["figures_L03", "예습노트_L03_A.html", "예습노트_L03_A.md"])
        self.assertTrue((dst / "figures_L03" / "f.svg").exists())

    def test_each_backup_new_folder(self):
        (self.dir / "예습노트_L03_A.html").write_text("a", encoding="utf-8")
        a, b = pf.backup(self.repo, "L03", self.run), pf.backup(self.repo, "L03", self.run)
        self.assertNotEqual(a, b)

    def test_bad_args(self):
        with self.assertRaises(pf.PickError):
            pf.backup(self.repo, "3", self.run)
        with self.assertRaises(pf.PickError):
            pf.backup(self.repo, "L03", self.run / "missing")
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-preview-note/tests -p "test_files.py" -v`
Expected: FAIL — `No module named 'preview_files'`

- [ ] **Step 3: `preview_files.py` 작성**

```python
#!/usr/bin/env python3
"""
예습노트 대상 Lecture 고르기와 기존 예습노트 백업 (표준 라이브러리만 사용).

- 같은 번호에 _rev PDF가 있으면 그것을 쓰고, slug에서 _rev를 뺀다.
- 인자가 없으면 번호가 가장 큰 Lecture. 그 예습노트가 이미 있으면 멈춘다(지난 강의로 내려가지 않는다).
- macOS NFD 폴더·파일명도 NFC로 비교해 찾는다.
CLI:
  preview_files.py pick --repo REPO [--lecture L03]       → "L03<TAB>PDF 경로<TAB>slug"
  preview_files.py backup --repo REPO --lecture L03 --run RUN
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time
import unicodedata

PDF_RE = re.compile(r"Lecture(\d{2})_([A-Za-z0-9_]+?)(_rev)?\.pdf")
LECTURE_RE = re.compile(r"L\d{2}")
LECTURES_DIR = "강의노트"
NOTES_DIR = "예습노트"


class PickError(RuntimeError):
    pass


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def child(parent: Path | None, name: str) -> Path | None:
    """parent 안에서 NFC 이름이 name인 항목(NFD 이름 포함)."""
    if parent is None or not parent.is_dir():
        return None
    for entry in os.listdir(parent):
        if nfc(entry) == name:
            return parent / entry
    return None


def lecture_pdfs(repo) -> dict[str, tuple[Path, str]]:
    d = child(Path(repo), LECTURES_DIR)
    if d is None:
        raise PickError(f"{LECTURES_DIR}/ 폴더 없음: {repo}")
    found: dict[str, tuple[Path, str, bool]] = {}
    for entry in sorted(os.listdir(d)):
        m = PDF_RE.fullmatch(nfc(entry))
        if not m:
            continue
        lec, slug, rev = f"L{m.group(1)}", m.group(2), bool(m.group(3))
        if lec not in found or (rev and not found[lec][2]):
            found[lec] = (d / entry, slug, rev)
    return {k: (p, s) for k, (p, s, _) in sorted(found.items())}


def has_note(repo, lecture: str) -> bool:
    d = child(child(Path(repo), NOTES_DIR), lecture)
    return d is not None and any(
        nfc(n).startswith(f"예습노트_{lecture}_") and n.endswith(".html") for n in os.listdir(d))


def pick(repo, lecture: str | None = None) -> tuple[str, Path, str]:
    pdfs = lecture_pdfs(repo)
    if not pdfs:
        raise PickError(f"{LECTURES_DIR}/에 LectureNN_*.pdf 없음. 새 강의노트가 올라왔는지 ajou-bb로 확인하세요.")
    available = ", ".join(pdfs)
    if lecture is not None:
        if lecture not in pdfs:
            raise PickError(f"{lecture} 강의노트 없음. 사용 가능: {available}")
    else:
        lecture = max(pdfs)
        if has_note(repo, lecture):
            raise PickError(f"최신 강의 {lecture}의 예습노트가 이미 있어요. 새 강의노트가 올라왔는지 ajou-bb로 확인하세요. "
                            f"다시 만들려면 {lecture}를 인자로 주세요. 사용 가능: {available}")
    pdf, slug = pdfs[lecture]
    return lecture, pdf, slug


def _count(p: Path) -> int:
    return sum(len(files) for _, _, files in os.walk(p)) if p.is_dir() else 1


def backup(repo, lecture: str, run) -> Path | None:
    run = Path(run)
    if not LECTURE_RE.fullmatch(lecture) or not run.is_dir():
        raise PickError(f"백업 중단: lecture={lecture!r} 또는 run={str(run)!r} 잘못됨")
    src = child(child(Path(repo), NOTES_DIR), lecture)
    if src is None:
        return None
    hits = sorted((nfc(n), src / n) for n in os.listdir(src)
                  if nfc(n).startswith(f"예습노트_{lecture}_") or nfc(n) == f"figures_{lecture}")
    if not hits:
        return None
    dst = Path(tempfile.mkdtemp(prefix=time.strftime("previous-%Y%m%d-%H%M%S-"), dir=run))  # 항상 새 폴더
    for name, path in hits:
        if path.is_dir():
            shutil.copytree(path, dst / name)
        else:
            shutil.copy2(path, dst / name)
    want, got = sum(_count(p) for _, p in hits), _count(dst)
    if got != want:
        raise PickError(f"백업 실패: 파일 {want}개 중 {got}개만 복사됨 → {dst}")
    return dst


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick")
    p.add_argument("--repo", required=True)
    p.add_argument("--lecture")
    b = sub.add_parser("backup")
    b.add_argument("--repo", required=True)
    b.add_argument("--lecture", required=True)
    b.add_argument("--run", required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "pick":
            lecture, pdf, slug = pick(args.repo, args.lecture)
            print(f"{lecture}\t{pdf}\t{slug}")
        else:
            dst = backup(args.repo, args.lecture, args.run)
            print(f"백업: {dst}" if dst else "백업할 기존 예습노트 없음")
    except PickError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-preview-note/tests -p "test_files.py" -v`
Expected: 13개 PASS

- [ ] **Step 5: 실제 저장소로 확인**

Run: `python3 .claude/skills/ml-preview-note/scripts/preview_files.py pick --repo "$PWD"`
Expected: `L03	…/강의노트/Lecture03_Linear_Regression_Part1_rev.pdf	Linear_Regression_Part1`

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/ml-preview-note/scripts/preview_files.py .claude/skills/ml-preview-note/tests/test_files.py
git commit -m "$(cat <<'EOF'
feat(skill): lecture picker and backup for ml-preview-note

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: 예습노트 조립기

**Files:**
- Create: `.claude/skills/ml-preview-note/scripts/preview_assemble.py`
- Test: `.claude/skills/ml-preview-note/tests/test_assemble.py`

**Interfaces:**
- Consumes: 복습 `assemble.py`의 `AssembleError`, `esc(str) -> str`, `fill(template: str, values: dict[str, str]) -> str`(빠진 슬롯이면 `AssembleError`), `split_scripts(fragment) -> tuple[str, list[str]]`; `preview_manifest.load`, `note_name`, `ManifestError`; 템플릿 슬롯(Task 1)
- Produces: `build_note(m: dict, run_dir: Path) -> str`, `assemble(run_dir, out_dir) -> Path`(쓴 HTML 경로), CLI `--run RUN --out DIR`

- [ ] **Step 1: 실패하는 테스트** — `tests/test_assemble.py`

```python
from pathlib import Path
import shutil
import tempfile
import unittest

from _util import MINI_RUN

import preview_assemble as pa
from assemble import AssembleError  # preview_assemble이 복습 scripts 경로를 넣은 뒤라 import된다


class TestPreviewAssemble(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.note = pa.assemble(MINI_RUN, self.tmp / "out")
        self.html = self.note.read_text(encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_output_name(self):
        self.assertEqual(self.note.name, "예습노트_L99_Mini_Preview.html")

    def test_titles_brand_range(self):
        self.assertIn("<title>머신러닝기초 예습노트 L99</title>", self.html)
        self.assertIn('<strong class="brand">예습노트</strong>', self.html)
        self.assertIn('data-range="L99"', self.html)
        self.assertIn("<h1>Mini — 수업 전에 보는 예습노트</h1>", self.html)

    def test_sections_and_toc(self):
        self.assertIn('<a href="#s0">0 미리</a><a href="#s1">1 평균</a><a href="#s2">2 한눈에</a>', self.html)
        self.assertIn('<section id="s1"><h2>1. 평균과 분산</h2>', self.html)

    def test_no_slots_left(self):
        self.assertNotIn("{{", self.html)

    def test_missing_fragment_writes_nothing(self):
        run = self.tmp / "run"
        shutil.copytree(MINI_RUN, run)
        (run / "sections" / "s2.html").unlink()
        out = self.tmp / "out2"
        with self.assertRaises(AssembleError):
            pa.assemble(run, out)
        self.assertFalse(out.exists())

    def test_cli(self):
        self.assertEqual(pa.main(["--run", str(MINI_RUN), "--out", str(self.tmp / "cli")]), 0)
        self.assertTrue((self.tmp / "cli" / "예습노트_L99_Mini_Preview.html").exists())
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-preview-note/tests -p "test_assemble.py" -v`
Expected: FAIL — `No module named 'preview_assemble'`

- [ ] **Step 3: `preview_assemble.py` 작성**

```python
#!/usr/bin/env python3
"""
manifest + 섹션 조각 → 예습노트 HTML 하나 (표준 라이브러리만 사용).

실행 폴더 구조:
  RUN/manifest.json
  RUN/sections/<section-id>.html   (섹션 안쪽: <article class="topic"> 들)
템플릿은 ml-review-pack과 공유한다(assets/note-template.html 심링크).
CLI: preview_assemble.py --run RUN --out 예습노트/<Lxx>
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _review  # noqa: E402,F401
from assemble import AssembleError, esc, fill, split_scripts  # noqa: E402  (복습 스킬 공용)
import preview_manifest as pm  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets"
BRAND = "예습노트"


def read_fragment(path: Path) -> str:
    if not path.exists():
        raise AssembleError(f"조각 파일 없음: {path}")
    return path.read_text(encoding="utf-8")


def build_note(m: dict, run_dir: Path) -> str:
    sections, scripts = [], []
    for sec in m["sections"]:
        body, found = split_scripts(read_fragment(run_dir / "sections" / f"{sec['id']}.html"))
        scripts += found
        sections.append(f'    <section id="{sec["id"]}"><h2>{esc(sec["title"])}</h2>\n{body.strip()}\n    </section>')
    return fill((ASSETS / "note-template.html").read_text(encoding="utf-8"), {
        "PAGE_TITLE": esc(f"머신러닝기초 예습노트 {m['lecture']}"),
        "BRAND": BRAND,
        "DESCRIPTION": esc(m["note_subtitle"]),
        "TOC": "".join(f'<a href="#{s["id"]}">{esc(s["short"])}</a>' for s in m["sections"]),
        "TITLE": esc(m["note_title"]),
        "SUBTITLE": esc(m["note_subtitle"]),
        "SECTIONS": "\n".join(sections),
        "FOOTER": m["footer_note"],
        "SCRIPTS": "\n".join(f"  {s}" for s in scripts),
        "RANGE": m["lecture"],
    })


def assemble(run_dir: Path | str, out_dir: Path | str) -> Path:
    run_dir, out_dir = Path(run_dir), Path(out_dir)
    m = pm.load(run_dir / "manifest.json")
    html = build_note(m, run_dir)  # 조각이 하나라도 없으면 여기서 멈춰 아무 파일도 만들지 않는다
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / pm.note_name(m)
    path.write_text(html, encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        print(assemble(args.run, args.out))
    except (AssembleError, pm.ManifestError) as e:
        print(f"assemble 실패: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-preview-note/tests -v`
Expected: 지금까지 테스트 전부 PASS (test_assemble 6개 포함)

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/ml-preview-note/scripts/preview_assemble.py .claude/skills/ml-preview-note/tests/test_assemble.py
git commit -m "$(cat <<'EOF'
feat(skill): preview note assembler on shared template

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: 예습노트 검사기 (계약 + 슬라이드 태그 + 분량)

**Files:**
- Create: `.claude/skills/ml-preview-note/scripts/preview_check.py`
- Test: `.claude/skills/ml-preview-note/tests/test_check.py`

**Interfaces:**
- Consumes: 복습 `check_html.py`의 `Problem(code, where, detail)`, `parse_html(source) -> Doc`(`doc.containers[id].text/.child_classes`), `check_common(doc, source, path) -> list[Problem]`, `check_note(doc, m) -> list[Problem]`(`m`에 `sections`, `preview_topic`, `forbidden_outside_preview`, `links` 필요); `preview_manifest.load`; `preview_assemble.assemble`(테스트)
- Produces: `contract_view(m) -> dict`, `topic_stats(source) -> dict[str, TopicStats]`, `visible_chars(text) -> int`, `sentences(text) -> int`, `check_preview(m, note_path) -> list[Problem]`, CLI `--manifest M --note NOTE [FILES...]` → `OK` 또는 `FAIL (n)`. Problem 코드: 복습 코드 + `slide-tag`, `missing-supp`, `stt-layer`, `topic-long`, `eli5-long`, `listen-long`

- [ ] **Step 1: 실패하는 테스트** — `tests/test_check.py`

```python
from pathlib import Path
import shutil
import tempfile
import unittest

from _util import MINI_RUN

import preview_assemble as pa
import preview_check as pc
import preview_manifest as pm


class TestPreviewCheck(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.run = self.tmp / "run"
        shutil.copytree(MINI_RUN, self.run)
        self.m = pm.load(self.run / "manifest.json")

    def tearDown(self):
        self._tmp.cleanup()

    def patch(self, sid, old, new):
        p = self.run / "sections" / f"{sid}.html"
        text = p.read_text(encoding="utf-8")
        self.assertIn(old, text)
        p.write_text(text.replace(old, new, 1), encoding="utf-8")

    def problems(self):
        note = pa.assemble(self.run, self.tmp / "out")
        return pc.check_preview(self.m, note)

    def codes(self):
        return {(p.code, p.where) for p in self.problems()}

    def test_fixture_passes(self):
        self.assertEqual(self.problems(), [])

    def test_missing_required_term(self):
        self.patch("s1", r"$\sigma^2 = ", "$s = ")
        self.assertIn(("missing-term", "s1-var"), self.codes())

    def test_slide_tag(self):
        self.patch("s1", "L99 s2–3", "L99 s2")
        self.assertIn(("slide-tag", "s1-mean"), self.codes())

    def test_supp_label(self):
        self.patch("s1", "교과서 보충", "보충")
        self.assertIn(("missing-supp", "s1-var"), self.codes())

    def test_stt_layer(self):
        self.patch("s1", '<div class="layer listen">',
                   '<div class="layer prof"><span class="layer-title">교수님 말씀</span><p>가</p></div><div class="layer listen">')
        self.assertIn(("stt-layer", "s1-mean"), self.codes())

    def test_eli5_sentences(self):
        self.patch("s1", "평균은 시소의 무게중심이에요.", "평균은 시소의 무게중심이에요. 두 번째 문장이에요. 세 번째 문장이에요.")
        self.assertIn(("eli5-long", "s1-mean"), self.codes())

    def test_figcaption_not_counted_as_sentence(self):
        self.patch("s1", "평균은 시소의 무게중심이에요.", "평균은 시소의 무게중심이에요. 두 번째 문장이에요.")
        self.assertNotIn(("eli5-long", "s1-mean"), self.codes())

    def test_listen_items(self):
        self.patch("s1", "<li>무게중심 비유가 나오면 위 식과 연결해 보세요.</li>", "<li>가</li><li>나</li><li>다</li>")
        self.assertIn(("listen-long", "s1-mean"), self.codes())

    def test_topic_too_long(self):
        self.patch("s0", "열벡터예요.</p>", "열벡터예요.</p><p>" + "가" * 700 + "</p>")
        self.assertIn(("topic-long", "s0-vector"), self.codes())

    def test_math_not_counted(self):
        self.patch("s0", "열벡터예요.</p>", "열벡터예요.</p><p>$$" + "x_n + " * 300 + "x$$</p>")
        self.assertNotIn(("topic-long", "s0-vector"), self.codes())

    def test_summary_panel_not_counted(self):
        self.patch("s0", '<p class="sum-lead">벡터는 숫자 묶음이에요.</p>', '<p class="sum-lead">' + "가" * 700 + "</p>")
        self.assertNotIn(("topic-long", "s0-vector"), self.codes())

    def test_helpers(self):
        self.assertEqual(pc.visible_chars("가 나 $x^2$ $$y$$ 다"), 3)
        self.assertEqual(pc.sentences(" 하나예요. 둘이에요? 셋 "), 3)
        self.assertEqual(pc.sentences("값은 0.5예요."), 1)

    def test_cli(self):
        note = pa.assemble(self.run, self.tmp / "out")
        self.assertEqual(pc.main(["--manifest", str(self.run / "manifest.json"), "--note", str(note)]), 0)
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-preview-note/tests -p "test_check.py" -v`
Expected: FAIL — `No module named 'preview_check'`

- [ ] **Step 3: `preview_check.py` 작성**

```python
#!/usr/bin/env python3
"""
예습노트 HTML 검사기 (표준 라이브러리만 사용).

- 공통·계약 검사는 ml-review-pack의 check_common/check_note를 그대로 쓴다
  (예고 금지어는 없고, 보충 배지는 이 파일에서 "교과서 보충"으로 따로 검사한다).
- 예습 전용: 슬라이드 태그, 교과서 보충 배지, STT 레이어 금지, 분량(600자·eli5 2문장·listen 2항목).
- 분량은 레이어 안 글자만 센다. 공백, TeX($…$, $$…$$), 그림(svg·figure), 레이어 제목, 배지, 태그, 요약 패널은 뺀다.
CLI: preview_check.py --manifest RUN/manifest.json --note NOTE.html
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _review  # noqa: E402,F401
from check_html import VOID_TAGS, Problem, check_common, check_file, check_note, parse_html  # noqa: E402
import preview_manifest as pm  # noqa: E402

SUPP_LABEL = "교과서 보충"
STT_LAYERS = {"prof", "warn"}
MAX_CHARS = 600
MAX_ELI5_SENTENCES = 2
MAX_LISTEN_ITEMS = 2
LAYER_KINDS = ("eli5", "formal", "listen", "supp")
SKIP_TAGS = {"svg", "figure", "script", "style"}
SKIP_CLASSES = {"layer-title", "badge", "sum", "tags"}
MATH_RE = re.compile(r"\$\$.*?\$\$|\$[^$]*\$", re.S)


@dataclass
class TopicStats:
    text: str = ""
    eli5: str = ""
    listen_items: int = 0


class _StatsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stats: dict[str, TopicStats] = {}
        # (tag, topic_id, layer_kind, skip)
        self.stack: list[tuple[str, str | None, str | None, bool]] = []

    def _top(self) -> tuple[str | None, str | None, bool]:
        return self.stack[-1][1:] if self.stack else (None, None, False)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        cls = set(a.get("class", "").split())
        topic, layer, skip = self._top()
        if tag == "article" and "topic" in cls and a.get("id"):
            topic, layer = a["id"], None
            self.stats[topic] = TopicStats()
        if topic and tag == "div" and "layer" in cls:
            layer = next((k for k in LAYER_KINDS if k in cls), "other")
        skip = skip or tag in SKIP_TAGS or bool(cls & SKIP_CLASSES)
        if topic and layer and not skip:
            st = self.stats[topic]
            st.text += " "
            if layer == "eli5":
                st.eli5 += " "  # 블록 경계에서 문장이 붙지 않게
            if layer == "listen" and tag == "li":
                st.listen_items += 1
        if tag not in VOID_TAGS:
            self.stack.append((tag, topic, layer, skip))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        topic, layer, skip = self._top()
        if topic and layer and not skip:
            st = self.stats[topic]
            st.text += data
            if layer == "eli5":
                st.eli5 += data


def topic_stats(source: str) -> dict[str, TopicStats]:
    parser = _StatsParser()
    parser.feed(source)
    parser.close()
    return parser.stats


def visible_chars(text: str) -> int:
    return len(re.sub(r"\s", "", MATH_RE.sub("", text)))


def sentences(text: str) -> int:
    t = MATH_RE.sub("X", text).strip()
    return len([p for p in re.split(r"(?<=[.?!])\s+", t) if p.strip()])


def contract_view(m: dict) -> dict:
    """복습 check_note에 넘길 사본: 예고 금지어 없음, 보충 배지는 여기서 따로 검사."""
    v = copy.deepcopy(m)
    for sec in v["sections"]:
        for t in sec["topics"]:
            t["supp"] = False
    v["preview_topic"] = v["sections"][-1]["topics"][-1]["id"]
    v["forbidden_outside_preview"] = []
    return v


def check_preview(m: dict, note_path: Path | str) -> list[Problem]:
    path = Path(note_path)
    source = path.read_text(encoding="utf-8")
    doc = parse_html(source)
    out = check_common(doc, source, path) + check_note(doc, contract_view(m))
    stats = topic_stats(source)
    for sec in m["sections"]:
        for t in sec["topics"]:
            con = doc.containers.get(t["id"])
            if con is None or not t["layers"]:
                continue
            tag = f"{m['lecture']} {t['slides']}"
            if tag not in con.text:
                out.append(Problem("slide-tag", t["id"], f"'{tag}' 태그 없음"))
            if t["supp"] and ("supp" not in con.child_classes or SUPP_LABEL not in con.text):
                out.append(Problem("missing-supp", t["id"], f"layer supp + '{SUPP_LABEL}' 필요"))
            stt = STT_LAYERS & con.child_classes
            if stt:
                out.append(Problem("stt-layer", t["id"], ", ".join(sorted(stt))))
            st = stats.get(t["id"], TopicStats())
            n = visible_chars(st.text)
            if n > MAX_CHARS:
                out.append(Problem("topic-long", t["id"], f"본문 {n}자 > {MAX_CHARS}자"))
            k = sentences(st.eli5)
            if k > MAX_ELI5_SENTENCES:
                out.append(Problem("eli5-long", t["id"], f"쉽게 말하면 {k}문장 > {MAX_ELI5_SENTENCES}문장"))
            if st.listen_items > MAX_LISTEN_ITEMS:
                out.append(Problem("listen-long", t["id"], f"들을 때 포인트 {st.listen_items}개 > {MAX_LISTEN_ITEMS}개"))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--manifest")
    ap.add_argument("--note")
    args = ap.parse_args(argv)
    problems: list[Problem] = []
    if args.manifest:
        if not args.note:
            ap.error("--manifest에는 --note가 필요")
        try:
            problems += check_preview(pm.load(args.manifest), args.note)
        except pm.ManifestError as e:
            print(f"manifest 오류: {e}")
            return 1
    for name in args.files:
        problems += check_file(name)
    for p in problems:
        print(p)
    print("OK" if not problems else f"FAIL ({len(problems)})")
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-preview-note/tests -v`
Expected: 전부 PASS. `test_fixture_passes`가 실패하면 출력된 Problem을 보고 **픽스처가 아니라 검사기**를 고친다(픽스처는 규칙을 지키게 쓰였다). 단, `check_common`의 `broken-link`가 `#s1-mean`에서 나면 조립 결과에 `id="s1-mean"`이 있는지 확인한다.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/ml-preview-note/scripts/preview_check.py .claude/skills/ml-preview-note/tests/test_check.py
git commit -m "$(cat <<'EOF'
feat(skill): preview note checker with slide tags and length limits

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: MD 변환

**Files:**
- Create: `.claude/skills/ml-preview-note/scripts/preview_md.py`
- Test: `.claude/skills/ml-preview-note/tests/test_md.py`

**Interfaces:**
- Consumes: 복습 `html2md.py`의 `nfc(str)`, `Ctx(link_map, fig_dir_abs, fig_dir_name, prefix="", registry=None)`(`registry`: 내보낸 SVG 파일명 집합), `convert(path, out_path, ctx, intro: list[str])`, `check_md(html_path, md_path) -> list[str]`; `preview_assemble.assemble`(테스트)
- Produces: `convert_note(note_path) -> tuple[Path, int]`(`(md 경로, 그림 수)`), CLI `NOTE.html [--check]` → md 경로, `figures: N`, `--check`면 `OK`/`FAIL (n)`

- [ ] **Step 1: 실패하는 테스트** — `tests/test_md.py`

```python
from pathlib import Path
import tempfile
import unittest

from _util import MINI_RUN

import preview_assemble as pa
import preview_md as pmd
import html2md  # preview_md가 복습 scripts 경로를 넣은 뒤


class TestPreviewMd(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.note = pa.assemble(MINI_RUN, self.tmp / "out")

    def tearDown(self):
        self._tmp.cleanup()

    def test_convert_and_check(self):
        md, figs = pmd.convert_note(self.note)
        self.assertEqual(md.name, "예습노트_L99_Mini_Preview.md")
        self.assertEqual(figs, 1)
        self.assertTrue((self.tmp / "out" / "figures_L99" / "fig-seesaw.svg").exists())
        self.assertEqual(html2md.check_md(str(self.note), str(md)), [])
        text = md.read_text(encoding="utf-8")
        self.assertIn("**들을 때 포인트**", text)
        self.assertIn("**교과서 보충**", text)

    def test_orphan_svgs_removed(self):
        figs = self.tmp / "out" / "figures_L99"
        figs.mkdir()
        (figs / "old.svg").write_text("<svg/>", encoding="utf-8")
        pmd.convert_note(self.note)
        self.assertFalse((figs / "old.svg").exists())

    def test_bad_name(self):
        other = self.note.with_name("정리노트_0101_X.html")
        other.write_text(self.note.read_text(encoding="utf-8"), encoding="utf-8")
        with self.assertRaises(ValueError):
            pmd.convert_note(other)

    def test_cli_check(self):
        self.assertEqual(pmd.main([str(self.note), "--check"]), 0)
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s .claude/skills/ml-preview-note/tests -p "test_md.py" -v`
Expected: FAIL — `No module named 'preview_md'`

- [ ] **Step 3: `preview_md.py` 작성**

```python
#!/usr/bin/env python3
"""
예습노트 HTML → GitHub 마크다운 (표준 라이브러리만 사용).

ml-review-pack의 html2md 변환·검사 함수를 그대로 쓴다. 그림은 같은 폴더의 figures_<Lxx>/에 SVG로 내보낸다.
CLI:
  preview_md.py 예습노트_<Lxx>_<slug>.html            # 같은 폴더에 .md + figures_<Lxx>/
  preview_md.py 예습노트_<Lxx>_<slug>.html --check    # 변환 후 누락 검사(수식·앵커·그림·링크)
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _review  # noqa: E402,F401
import html2md  # noqa: E402  (복습 스킬 공용)

NAME_RE = re.compile(r"예습노트_(L\d{2})_([A-Za-z0-9_]+)\.html")


def convert_note(note_path: Path | str) -> tuple[Path, int]:
    src = Path(note_path).resolve()
    name = html2md.nfc(src.name)
    m = NAME_RE.fullmatch(name)
    if not m:
        raise ValueError(f"파일명 규칙 위반: {name}")
    fig_name = f"figures_{m.group(1)}"
    fig_abs = src.parent / fig_name
    fig_abs.mkdir(exist_ok=True)
    for entry in os.listdir(fig_abs):  # 다시 변환할 때 이전 실행의 고아 SVG를 남기지 않는다(.svg만, 이 폴더만)
        old = fig_abs / entry
        if entry.lower().endswith(".svg") and old.is_file() and not old.is_symlink():
            old.unlink()
    md_name = name[:-5] + ".md"
    ctx = html2md.Ctx([(name, md_name)], str(fig_abs), fig_name, prefix="note", registry=set())
    intro = [f"> `{name}`를 마크다운으로 옮겼어요. 그림은 `{fig_name}/` 폴더의 SVG예요. "
             "수식은 `$…$` / `$$…$$`라서 GitHub, Obsidian, Typora에서 보여요."]
    out = src.parent / md_name
    html2md.convert(str(src), str(out), ctx, intro)
    return out, len(ctx.registry)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("note")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    try:
        out, figs = convert_note(args.note)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    print(out)
    print(f"figures: {figs}")
    if not args.check:
        return 0
    problems = html2md.check_md(str(Path(args.note).resolve()), str(out))
    for p in problems:
        print(f"{out.name}: {p}")
    print("OK" if not problems else f"FAIL ({len(problems)})")
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-preview-note/tests -v`
Expected: 전부 PASS. `figs`가 1이 아니면 `html2md.block`이 `figure` 안 SVG를 어떻게 내보내는지(`export_svg`, `html2md.py:329`) 확인하고 기대값이 아니라 원인을 고친다.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/ml-preview-note/scripts/preview_md.py .claude/skills/ml-preview-note/tests/test_md.py
git commit -m "$(cat <<'EOF'
feat(skill): markdown export for preview notes

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: SKILL.md, 참조 문서, `.agents` 심링크

**Files:**
- Create: `.claude/skills/ml-preview-note/SKILL.md`
- Create: `.claude/skills/ml-preview-note/references/content-rules.md`
- Create: `.claude/skills/ml-preview-note/references/manifest-guide.md`
- Create: `.claude/skills/ml-preview-note/references/review-prompt.md`
- Create: `.claude/skills/ml-preview-note/references/browser-check.md`
- Create: `.agents/skills/ml-preview-note` (심링크)
- Test: `.claude/skills/ml-preview-note/tests/test_skill_files.py`

**Interfaces:**
- Consumes: Task 2~6의 CLI(`preview_files.py pick|backup`, `preview_manifest.py`, `preview_assemble.py --run --out`, `preview_check.py --manifest --note`, `preview_md.py NOTE --check`)
- Produces: `/ml-preview-note [Lxx] [lite]` 스킬

- [ ] **Step 1: 실패하는 테스트** — `tests/test_skill_files.py`

```python
"""SKILL.md 형식과, 본문이 가리키는 파일이 모두 있는지 확인한다."""

import os
import re
import unittest

from _util import REPO, SKILL

SKILL_MD = SKILL / "SKILL.md"


class TestSkillFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL_MD.read_text(encoding="utf-8")

    def test_frontmatter(self):
        m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", self.text)
        self.assertIsNotNone(m, "frontmatter는 name, description 두 줄")
        self.assertEqual(m.group(1), "ml-preview-note")
        self.assertIn("예습노트", m.group(2))
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_referenced_files_exist(self):
        refs = set(re.findall(r"(?:references|scripts|assets)/[\w.-]+\.(?:md|py|html)", self.text))
        self.assertGreaterEqual(len(refs), 9)
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

    def test_agents_symlink(self):
        link = REPO / ".agents" / "skills" / "ml-preview-note"
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), "../../.claude/skills/ml-preview-note")
```

Run: `python3 -m unittest discover -s .claude/skills/ml-preview-note/tests -p "test_skill_files.py" -v`
Expected: FAIL — `FileNotFoundError: …/SKILL.md`

- [ ] **Step 2: `SKILL.md` 작성**

````markdown
---
name: ml-preview-note
description: 머신러닝기초 다음 강의의 강의노트 PDF와 MML 교과서로, 수업 중 옆에 띄워 둘 짧은 예습노트 HTML(+MD, 그림)을 만들어 예습노트/<Lxx>/ 폴더에 저장한다. 문제는 만들지 않는다. "예습노트", "예습", "다음 강의 미리 보기", "L04 예습해줘"처럼 수업 전 준비를 요청하거나 /ml-preview-note [Lxx] [lite]로 부를 때 사용한다.
---

# 머신러닝기초 예습노트

강의노트 PDF와 MML 교과서로 Lecture 하나의 예습노트를 만든다. 수업을 들으면서 옆에 띄워 두는 용도라 **짧게** 쓰고, 토픽 순서는 **슬라이드 순서 그대로**다. 문제는 만들지 않는다. 양식은 `ml-review-pack` 정리노트와 같다(`assets/note-template.html`은 그 템플릿의 심링크). 중간에 사용자에게 묻지 않고 끝에 한 번 보고한다. 커밋은 제안만 한다.

**산출물** (`예습노트/<Lxx>/`): `예습노트_<Lxx>_<slug>.html`, 같은 이름 `.md`, `figures_<Lxx>/`

**인자**: `[Lxx] [lite]`
- `Lxx`가 없으면 번호가 가장 큰 Lecture PDF. 그 예습노트가 이미 있으면 멈추고 알린다.
- `lite`: 작성자를 sonnet(GPT이면 luna)으로, 6단계 리뷰를 생략한다. 기계 검사와 브라우저 검사는 그대로 한다.

**진행 표시**: 단계마다 한 줄. 예: `3/9 작성 중: 섹션 4개 (병렬)`

**경로 약속**
- `SKILL` = 이 파일이 있는 폴더(`.claude/skills/ml-preview-note`)의 절대 경로
- `REPO` = 저장소 루트
- `RUN` = `<scratchpad>/preview-note/<Lxx>/`
- 셸 상태는 Bash 호출 사이에 이어지지 않는다. `$SKILL`, `$RUN`, `$REPO`, `$LEC`는 실행할 때마다 실제 값으로 바꿔 쓰거나 같은 명령 앞에 붙여 설정한다. `cd`는 쓰지 않는다.

## 절차

### 0. 준비
1. `REPO`에 `강의노트/`와 `교과서/Mathematics_for_Machine_Learning.pdf`가 있는지 확인한다. 없으면 "머신러닝기초 저장소에서만 동작합니다"라고 알리고 멈춘다.
2. Lecture를 고른다.
   ```bash
   python3 "$SKILL/scripts/preview_files.py" pick --repo "$REPO" [--lecture Lxx]
   ```
   출력은 `Lxx<TAB>PDF 경로<TAB>slug`. 종료 코드가 1이면 표준에러 메시지(사용 가능 목록, ajou-bb 안내)를 그대로 보여 주고 멈춘다.
3. 실행 폴더를 만든다. 서브에이전트에게는 `RUN`, `RUN/repo`, `SKILL` 경로만 넘긴다.
   ```bash
   mkdir -p "$RUN"/{sections,work} && ln -sfn "$REPO" "$RUN/repo"
   ```
   에이전트는 `RUN` 밖에 쓰지 않는다. 임시 파일은 `RUN/work/`에만 둔다. `예습노트/`에는 메인 에이전트만 쓴다.

### 1. 자료 파악
1. 슬라이드 텍스트를 슬라이드 번호와 함께 `RUN/slides.txt`로 뽑는다.
   ```bash
   LEC=<Lxx> PDF=<PDF 경로> RUN=… python3 - <<'EOF'
   import fitz, os
   d = fitz.open(os.environ["PDF"])
   with open(os.path.join(os.environ["RUN"], "slides.txt"), "w", encoding="utf-8") as f:
       for i, page in enumerate(d, 1):
           f.write(f"=== {os.environ['LEC']} s{i} ===\n{page.get_text()}\n")
   print(len(d), "slides")
   EOF
   ```
   추출에 실패하면 PDF를 Read 도구로 직접 읽고, 보고서에 적는다.
2. `slides.txt`를 끝까지 읽고 슬라이드를 개념 단위(1~3장)로 묶는다.
3. MML에서 관련 장과 쪽을 찾는다. `keys`는 슬라이드 핵심어(영어 소문자)로 바꾼다. 출력 숫자가 링크 `#page=N`의 N이다.
   ```bash
   REPO=… python3 - <<'EOF'
   import fitz, os
   d = fitz.open(os.path.join(os.environ["REPO"], "교과서/Mathematics_for_Machine_Learning.pdf"))
   keys = ["linear regression", "least-squares", "maximum likelihood"]
   for i, p in enumerate(d):
       hit = [k for k in keys if k in p.get_text().lower()]
       if len(hit) >= 2:
           print(i + 1, hit)
   EOF
   ```
4. 이전 복습노트(`복습노트/*/정리노트_*.md`)에서 이 강의가 기대는 개념을 찾아 둔다("미리 알아둘 것"과 링크에 쓴다).

### 2. manifest
- `RUN/manifest.json`을 쓴다. 규칙은 `references/manifest-guide.md`.
- 검증: `python3 "$SKILL/scripts/preview_manifest.py" "$RUN/manifest.json"` → `OK`

### 3. 작성
- 섹션마다 작성자 1명을 **한 메시지에서 병렬로** 띄운다. 브리프는 `references/content-rules.md`.
- 모델은 opus, `lite`이면 sonnet. GPT이면 opus 대신 sol, sonnet 대신 luna.
- 브리프의 `<…>` 자리에 실제 경로, 섹션 id·제목, 그 섹션 토픽의 `links` 목록, MML 쪽 번호를 채운다.

### 4. 조립
- **처음 조립할 때만** 기존 예습노트를 백업한다(다시 조립할 때는 하지 않는다. 스킬이 만든 초안이 백업에 섞이기 때문이다).
  ```bash
  python3 "$SKILL/scripts/preview_files.py" backup --repo "$REPO" --lecture <Lxx> --run "$RUN"
  ```
  종료 코드가 1이면 조립하지 말고 원인을 고친다.
- 조립:
  ```bash
  python3 "$SKILL/scripts/preview_assemble.py" --run "$RUN" --out "$REPO/예습노트/<Lxx>"
  ```

### 5. 기계 검사
```bash
python3 "$SKILL/scripts/preview_check.py" --manifest "$RUN/manifest.json" --note "$REPO/예습노트/<Lxx>/<예습노트>.html"
```
- `FAIL`이면 Problem의 `where`(토픽·섹션 id)로 담당 작성자를 찾아 문제 목록을 보낸다(SendMessage, 안 되면 같은 브리프로 새 에이전트).
- `topic-long`·`eli5-long`·`listen-long`은 "줄여 주세요"로 보낸다. 내용을 다른 토픽으로 옮기지 말고 덜 중요한 문장을 뺀다.
- 고친 뒤 4단계(조립)부터 다시 한다. 최대 2회, 그래도 남으면 "미해결"로 보고한다.

### 6. 리뷰 (`lite`면 생략)
- 리뷰어 1명. 브리프는 `references/review-prompt.md`.
- Critical·Important는 모두, Minor는 쉬운 것만 고친다. 작성자별로 한 번에 모아 한 번만 수정 요청한다. 수정 후 4~5단계를 다시 한다.

### 7. 브라우저 검증
- `references/browser-check.md`대로 한다(KaTeX 오류 0, 남은 `$` 없음, 720px·375px 가로 넘침 없음, 720px에서 토픽 한 화면, 다크모드, 콘솔 오류).
- 결함은 5단계와 같은 방식으로 되돌린다(최대 2회 규칙에 포함). 끝나면 서버를 종료한다.

### 8. MD 변환
```bash
python3 "$SKILL/scripts/preview_md.py" "$REPO/예습노트/<Lxx>/<예습노트>.html" --check
```
`OK`가 나와야 한다. 누락은 대부분 조각의 마크업 문제다. 조각을 고치고 4단계부터 다시 한다.

### 9. 보고
```
## 예습노트 <Lxx> 완료
- 파일: 예습노트/<Lxx>/… (html 1, md 1, figures_<Lxx>/ N개)
- 범위: <PDF 이름> s1–sN, 토픽 M개
- 스킬이 정한 사항: slug, 섹션 구성, 교과서 보충으로 넣은 것과 이유, 뺀 슬라이드와 이유
- 미해결: … (없으면 "없음")
- 커밋 제안: git add 예습노트/<Lxx> && git commit -m "docs(notes): add preview note <Lxx>"
```
실행 폴더 경로(`RUN`)와 백업 경로(있으면)도 적는다.

## 오류 처리
| 상황 | 동작 |
|---|---|
| 저장소가 아님 | 알리고 멈춤 |
| Lecture PDF 없음 / 최신 Lecture 예습노트가 이미 있음 | `pick` 메시지를 보여 주고 멈춤 |
| PDF 텍스트 추출 실패 | Read 도구로 PDF를 읽고 보고서에 표시 |
| 포트 사용 중 | 다른 빈 포트 사용 |
| 백업 실패 | 조립하지 않고 원인을 고침 |
| 검사 2회 실패 | 멈추지 않고 나머지 단계를 끝낸 뒤 "미해결"로 보고 |
````

- [ ] **Step 3: `references/content-rules.md` 작성**

````markdown
# 예습노트 섹션 작성 규칙

## 작성자 브리프 (메인 에이전트가 섹션마다 1명, 병렬, model: opus / lite: sonnet, GPT이면 sol / lite: luna)

---
머신러닝기초 예습노트의 섹션 `<sid>`(`<섹션 title>`)를 쓴다. 학생이 **수업을 들으면서 옆에 띄워 보는** 노트다. 짧게 쓴다.

- 읽기: `<SKILL>/references/content-rules.md`(이 파일 전체)
- 계약: `<RUN>/manifest.json`의 섹션 `<sid>` — 토픽 id·제목·`slides`·`required_terms`·`layers`·`supp`를 정확히 따른다.
- 링크: 이 섹션 토픽의 `links` `<이 섹션의 links 목록>`을 그 토픽 안에 `<a href="…">`로 넣는다. `href`는 글자 그대로(`%20` 포함).
- 근거: `<RUN>/slides.txt`(`=== <Lxx> sN ===` 구획), 필요하면 MML `<RUN>/repo/교과서/Mathematics_for_Machine_Learning.pdf` <쪽>
- 출력: `<RUN>/sections/<sid>.html` **한 파일만**. `<section>`/`<h2>`는 쓰지 않는다(조립기가 감싼다). 임시 파일은 `<RUN>/work/`에만.
- 자기 검사(끝내기 전): `required_terms`가 문자 그대로 있는지, 슬라이드 태그 `<Lxx> <slides>`가 글자 그대로 있는지(범위는 en dash `–`), `$` 짝, 토픽 본문 600자 이하(공백·수식·그림 제외), 쉽게 말하면 2문장 이하, 들을 때 포인트 2항목 이하, 이모지 없음, `layers`가 빈 목록이 아닌 토픽마다 맨 끝에 `<div class="sum" hidden>`.
- 보고: 파일 경로, 토픽별 한 줄, 슬라이드에 있었지만 뺀 것과 이유.
---

## 범위
- 슬라이드에 있는 내용만 설명한다. 슬라이드에 없는 설명(교과서에서 가져온 유도·배경)은 `supp`가 `true`인 토픽의 보충 레이어에만 쓴다.
- 교수님 말씀이나 수업 중 강조는 아직 모르므로 **추측해서 쓰지 않는다**.

## 토픽 마크업 (이 순서)
```html
<article class="topic" id="…"><h3>…</h3><div class="tags"><span class="tag slide">L04 s12–14</span></div>
  <div class="layer eli5"><span class="layer-title">쉽게 말하면</span><p class="lead">한 문장 비유</p> …그림(필요할 때만)… </div>
  <div class="layer formal"><span class="layer-title">정확히 말하면</span> …핵심 식 + 기호 뜻… </div>
  <div class="layer listen"><span class="layer-title">들을 때 포인트</span><ul><li>…</li></ul></div>   ← manifest layers에 listen이 있을 때만
  <div class="layer supp"><span class="badge supp">교과서 보충</span> … </div>                              ← manifest supp=true만
  <div class="sum" hidden>…페이지 요약…</div>                                                          ← layers가 빈 목록이 아닌 토픽만, 맨 끝
</article>
```
- 레이어 제목과 배지 글자는 위와 글자 그대로 쓴다. `layer prof`, `layer warn`은 쓰지 않는다(검사 실패).
- 슬라이드 태그는 manifest `lecture`와 `slides`를 공백 하나로 이은 글자 그대로.
- 토픽은 그것만 읽어도 이해되게 쓰고, 앞 토픽은 `<a href="#토픽id">토픽 제목</a>`으로 잇는다.
- "미리 알아둘 것"(`s0`) 토픽: 이 강의를 따라가려면 필요한 선수 개념 하나. 이전 복습노트나 MML 쪽 링크를 건다.
- "한눈에 보기"(마지막 섹션): `-cheatsheet`는 표(`<div class="table-wrap"><table>`), `-links`는 `<ul><li><a>`.

## 분량 (검사기가 센다)
- 토픽 본문 **600자 이하**: 레이어 안 글자만 센다. 공백, `$…$`/`$$…$$` 수식, 그림, 레이어 제목, 배지, 태그, 요약 패널은 빼고 센다.
- **쉽게 말하면**: 2문장 이하("."·"?"·"!" 뒤 공백으로 나눈다), 전문용어·기호 없이. 그림은 슬라이드가 그림으로 설명하는 개념일 때만 1개.
- **정확히 말하면**: 슬라이드의 핵심 식을 쓰고, 기호마다 뜻 한 줄(`<ul>`). 유도는 쓰지 않거나 한 줄에 한 단계씩 3단계 이하.
- **들을 때 포인트**: 2항목 이하. 수업에서 무엇에 귀를 기울이면 되는지. 예: "이 식에서 왜 제곱을 쓰는지 설명하실 거예요", "앞 슬라이드의 $\boldsymbol{\theta}$가 여기서 다시 나와요".
- 문체: "~해요" 체, 한 문장에 한 가지, 군더더기 수식어 없이. 전문용어는 영어 병기(예: 최소제곱(least squares)).

## 페이지 요약 (`.sum`)
```html
<div class="sum" hidden>
  <p class="sum-lead">토픽 핵심 한 문장("~해요" 체)</p>
  <p class="panel-label">핵심 식</p>
  <ul class="eq-list"><li><span class="eq-name">식 이름</span>$$…$$</li></ul>
  <p class="panel-label">용어</p>
  <dl class="terms"><dt>용어(영어)</dt><dd>한 줄 뜻</dd></dl>
</div>
```
- 본문에 이미 나온 식·용어를 **같은 TeX 표기로** 1~2개. 식이 없으면 "핵심 식" 줄과 `eq-list`를, 용어가 없으면 "용어" 줄과 `dl`을 뺀다.

## 수식
- `$…$`, `$$…$$`만. 본문에 리터럴 `$` 금지. TeX 안 `<`, `>`, `&` 금지(`\lt`, `\gt`).
- 벡터 `\mathbf{x}`, 파라미터 벡터 `\boldsymbol{\theta}`, 행렬 `\mathbf{X}` — manifest `required_terms`와 같은 표기.

## SVG 그림
- `<figure class="figure"><svg id="fig-<kebab>" viewBox="…" role="img" aria-label="한국어 설명">…</svg><figcaption>…</figcaption></figure>`
- 색은 클래스로만: `fig-ink`, `fig-accent`, `fig-danger`(선만), `fig-dot`(채움), `fig-text`, `fig-muted`(글자). 하드코딩 색 금지.
- 글자 12~14px, SVG `<text>`에 `$` 금지(θ, σ, ₁ 같은 유니코드). id는 페이지 전체에서 유일.
- 위젯(`class="widget"`)은 만들지 않는다.
````

- [ ] **Step 4: `references/manifest-guide.md` 작성**

````markdown
# 예습노트 manifest.json 작성 규칙 (메인 에이전트)

manifest는 이번 예습노트의 계약이다. 작성자, 검사기, 조립기가 모두 이 파일을 기준으로 삼는다.
정본 예시: `tests/fixtures/mini-run/manifest.json`.
작성 후 반드시 `python3 <SKILL>/scripts/preview_manifest.py <RUN>/manifest.json` → `OK`.

## 최상위
| 키 | 값 |
|---|---|
| `course` | `"머신러닝기초"` |
| `lecture` | `"L04"` (`pick` 출력 첫 칸) |
| `slug` | `pick` 출력 셋째 칸(예: `"Linear_Regression_Part1"`) |
| `pdf` | 저장소 기준 PDF 경로(예: `"강의노트/Lecture03_Linear_Regression_Part1_rev.pdf"`) |
| `note_title` | `"<주제> — 수업 전에 보는 예습노트"` |
| `note_subtitle` | `"정방철 교수님 머신러닝기초 · Lecture04 <영문 제목> 예습 (MML N장)"` 형식 |
| `footer_note` | HTML 허용. `출처: 정방철 교수님 강의자료(LectureXX) · Deisenroth, Faisal, Ong, <i>Mathematics for Machine Learning</i> (2020) N장. 수업 전에 만든 노트라 수업 내용과 다를 수 있어요.` |
| `sections`, `links` | 아래 |

## sections / topics
- 섹션 id는 `s0`, `s1`, … 순서(검사기가 강제). `s0`은 "0. 미리 알아둘 것", 마지막 섹션은 "N. 한눈에 보기"이며 토픽 `s<N>-cheatsheet`, `s<N>-links`를 둔다.
- 가운데 섹션은 **슬라이드 순서**대로 묶는다(슬라이드 목차·소제목 단위). 토픽 id는 `s<n>-<kebab>`(영문 소문자), 섹션 id로 시작.
- 토픽 하나 = 슬라이드 1~3장. `slides`는 `"s7"` 또는 `"s7–9"`(en dash). 표지·목차·빈 슬라이드는 빼고 보고서에 적는다. 요약 섹션 토픽은 `""`.
- `short`는 상단 목차 글자(예: `"2 최소제곱"`), `title`은 `"2. 최소제곱법"`.
- `layers`
  - 개념 토픽: `["eli5", "formal", "listen"]`. 들을 거리가 없는 토픽(정의만 있는 짧은 슬라이드)은 `["eli5", "formal"]`.
  - `s0` 토픽: `["eli5", "formal"]`.
  - 요약 섹션 토픽: `[]`.
- `supp`: 슬라이드만으로는 식이 이해되지 않아 교과서 설명을 덧붙이는 토픽만 `true`. 요약 토픽은 항상 `false`.
- `required_terms`: 토픽당 2~6개, **슬라이드에 나오는** 핵심 용어·식. 식은 작성자가 공백까지 그대로 쓸 TeX 문자열(예: `"\\boldsymbol{\\theta}^{*}"`). 빈 문자열 금지. 요약 토픽은 치트시트에 넣을 식 몇 개 또는 `[]`.

## links
- `href`는 작성자가 `<a href="…">`에 **글자 그대로** 넣을 값이다(검사기가 해당 토픽 안의 링크와 정확히 비교하고, 파일이 실제로 있는지도 본다). 출력 폴더가 `예습노트/<Lxx>/`라 저장소 파일은 `../../`로 시작한다.
- MML 쪽: `{"topic": "s<N>-links", "href": "../../교과서/Mathematics_for_Machine_Learning.pdf#page=<쪽>"}` (1단계 3의 숫자).
- 선수 개념이 이전 복습노트에 있으면 `s0` 토픽에 `../../복습노트/<range>/정리노트_<range>_<slug>.html#<토픽 id>`.
- 확률 개념(Bayes, prior, MLE/MAP, 조건부확률)이 나오면 `../../강의노트/추가%20강의/eli5_lecture10_statistical_inference_part1.html`(part2·3은 `lecture11_…part2`, `lecture12_…part3`).
````

- [ ] **Step 5: `references/review-prompt.md` 작성**

````markdown
# 리뷰어 지시문 (lite에서는 생략)

---
머신러닝기초 예습노트 초안을 검토한다. 파일은 수정하지 않는다.

- 대상: `<RUN>/repo/예습노트/<Lxx>/<예습노트 html>`
- 근거: `<RUN>/slides.txt`, `<RUN>/manifest.json`, MML PDF
- 규칙: `<SKILL>/references/content-rules.md`

확인할 것:
1. **사실 오류**: 식, 정의, 부호, 조건이 슬라이드·교과서와 맞는가.
2. **슬라이드 대응**: 토픽 태그의 슬라이드 번호가 실제 그 내용이 있는 슬라이드인가. 빠진 슬라이드가 있는가.
3. **범위**: 슬라이드에 없는 설명이 "교과서 보충" 밖에 있는가. 교수님 발언을 지어낸 곳이 있는가.
4. **예습 효용**: 처음 듣는 학생이 수업 중에 이 토픽만 보고 슬라이드를 따라갈 수 있는가. 쉽게 말하면이 전문용어 없이 2문장 이하인가. 들을 때 포인트가 구체적인가("잘 들으세요" 같은 빈말이 아닌가).
5. **표현**: 잘린 문장, 빈 표 칸, 한 글자씩 줄바꿈되는 표.

출력 형식(이것만):
```
## Critical
- [s2-least-squares] 문제 → 고칠 내용
## Important
- …
## Minor
- …
```
각 항목은 토픽 id로 시작한다. 없으면 "없음".
---
````

- [ ] **Step 6: `references/browser-check.md` 작성**

````markdown
# 브라우저 검증 (메인 에이전트)

## 서버
file:// 미리보기에서는 스크립트가 돌지 않는다. 빈 포트로 서버를 띄운다. 셸 상태가 이어지지 않으므로 포트 번호를 먼저 출력하고 이후에는 그 숫자를 직접 쓴다.
1. 빈 포트: `python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1])"`
2. 서버: Bash 도구의 `run_in_background: true`로 `python3 -m http.server <port> --directory "<RUN>/repo"` (끝에 `&` 없이)
3. URL: `http://localhost:<port>/예습노트/<Lxx>/<파일명>` (한글 그대로)
4. 끝나면 그 백그라운드 작업을 멈추거나 `pkill -f "http.server <port>"`.

## 측정 전 준비
숨은 창에서는 `document.documentElement.clientWidth`가 0이 된다. 측정 전에 `resize_window`로 크기를 명시하고 `clientWidth > 0`을 확인한다. `.katex-mathml` 안 요소는 넘침 원인으로 치지 않는다.

## 화면별 측정 함수
템플릿은 한 번에 토픽 하나를 `.content` 안에 보여 준다. 아래 함수를 매 실행에 붙여 넣는다. `over`는 가로로 넘친 화면, `tall`은 세로 스크롤이 필요한 화면이다.
```js
async function measureScreens() {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const scroller = document.querySelector('.content') || document.documentElement;
  const screens = Array.from(document.querySelectorAll('main .screen'));
  const over = [], tall = [];
  for (const s of screens.length ? screens : [document.querySelector('main')]) {
    if (screens.length) { location.hash = s.id ? '#' + s.id : ''; await wait(150); }
    document.getAnimations().forEach((a) => a.finish());
    if (scroller.scrollWidth > scroller.clientWidth + 1 || document.documentElement.scrollWidth > window.innerWidth + 1) over.push(s.id || 'hero');
    if (s.matches('article.topic') && scroller.scrollHeight > scroller.clientHeight + 1) tall.push(s.id);
  }
  location.hash = '';
  await wait(150);
  return { over, tall };
}
```

## 반 화면(720×900, 수업 중 쓰는 크기)
`resize_window`(`width: 720`, `height: 900`) → 새로고침 → `clientWidth > 0` 확인 → `mcp__Claude_Browser__javascript_tool`:
```js
await new Promise((r) => setTimeout(r, 1500));
const textNodes = Array.from(document.querySelectorAll('main *, #panel-right *')).filter((e) => !['SCRIPT', 'STYLE'].includes(e.tagName) && !e.closest('[hidden]'));
({
  brand: document.querySelector('.brand').textContent,
  katexErrors: document.querySelectorAll('.katex-error').length,
  rawDollar: textNodes.some((e) => Array.from(e.childNodes).some((n) => n.nodeType === 3 && n.textContent.includes('$'))),
  sumsInPanel: document.querySelectorAll('#panel-right .sum').length,
  sumsLeftInMain: document.querySelectorAll('main .sum').length,
  widgets: document.querySelectorAll('.widget').length,
  ...(await measureScreens()),
})
```
통과: `brand: "예습노트"`, `katexErrors: 0`, `rawDollar: false`, `sumsInPanel`이 manifest에서 `layers`가 빈 목록이 아닌 토픽 수, `sumsLeftInMain: 0`, `widgets: 0`, `over: []`, `tall: []`. `tall`에 나온 토픽은 작성자에게 "720×900 한 화면에 들어가게 줄여 주세요"로 되돌린다. `read_console_messages`에 오류가 없어야 한다.

개념 토픽 하나로 넘겨(`location.hash = '#<토픽 id>'`) 스크린샷을 찍고, 슬라이드 태그와 "들을 때 포인트" 박스가 보이는지 확인한다.

## 모바일·다크
`resize_window`(`preset: "mobile"`, `colorScheme: "dark"`) → 새로고침 → `clientWidth > 0` 확인 → 위 스크립트 재실행(`over: []`만 통과 조건, 모바일의 `tall`은 참고만) → 스크린샷으로 그림 글자가 보이는지 확인 → `#theme-toggle`을 눌러 배경색과 `aria-label`이 바뀌는지 확인한 뒤 `localStorage.removeItem('od-theme')`.

## 마무리
`resize_window`(`preset: "desktop"`, `colorScheme: "light"`)로 되돌리고 서버를 종료한다.
````

- [ ] **Step 7: `.agents` 심링크**

```bash
ln -s ../../.claude/skills/ml-preview-note .agents/skills/ml-preview-note
```

- [ ] **Step 8: 통과 확인**

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-preview-note/tests -v`
Expected: 전부 PASS (`test_referenced_files_exist`가 `references/` 4개 + `scripts/` 5개 = 9개 이상을 찾는다)

Run: `python3 -W error::ResourceWarning -m unittest discover -s .claude/skills/ml-review-pack/tests -v`
Expected: `OK (skipped=2)`

- [ ] **Step 9: Commit**

```bash
git add .claude/skills/ml-preview-note .agents/skills/ml-preview-note
git commit -m "$(cat <<'EOF'
feat(skill): ml-preview-note skill instructions and references

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 8: 실제 강의로 시범 실행 (사용자 승인 후)

에이전트를 여러 명 띄우는 실제 실행이라 **사용자에게 먼저 묻는다**: "`/ml-preview-note L03 lite`로 시범 실행할까요? 결과는 `예습노트/L03/`에 생기고, 커밋할지는 보고 뒤에 정하시면 돼요."

**Files:**
- Create(실행 결과): `예습노트/L03/예습노트_L03_Linear_Regression_Part1.html`, `.md`, `figures_L03/`

- [ ] **Step 1: 승인 받기** (위 질문)

- [ ] **Step 2: 스킬 실행** — `ml-preview-note` 스킬을 인자 `L03 lite`로 실행해 SKILL.md 0~9단계를 따른다.

- [ ] **Step 3: 결과 확인**

Run: `python3 .claude/skills/ml-preview-note/scripts/preview_check.py --manifest <RUN>/manifest.json --note 예습노트/L03/예습노트_L03_Linear_Regression_Part1.html`
Expected: `OK`

Run: `python3 .claude/skills/ml-preview-note/scripts/preview_md.py 예습노트/L03/예습노트_L03_Linear_Regression_Part1.html --check`
Expected: 마지막 줄 `OK`

- [ ] **Step 4: 발견한 규칙 문제 반영** — 실행 중 작성자가 헷갈린 규칙이나 검사기 오탐이 있으면 해당 `references/*.md` 또는 스크립트와 테스트를 고치고 전체 테스트를 다시 돌린다. 고친 게 있으면 커밋:

```bash
git add .claude/skills/ml-preview-note
git commit -m "$(cat <<'EOF'
fix(skill): tighten ml-preview-note rules after L03 trial

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: 결과물 커밋 여부는 사용자에게 맡긴다** (보고서의 커밋 제안만 보여 준다).
