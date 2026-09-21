# 머신러닝기초 정리노트 + 복습문제 HTML (0909~0916) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 0909·0914·0916 수업(STT)과 Lecture00~02, MML 교과서를 바탕으로 ELI5식 정리노트 HTML 1개와 교과서 기반 복습문제 HTML 1개를 만든다.

**Architecture:** 두 HTML은 각각 단일 파일로 동작하며, CSS와 JS는 파일 안에 인라인으로 넣는다. 외부 리소스는 KaTeX와 Pretendard 폰트만 CDN으로 불러온다. 위젯 수식 코드는 `scripts/widget_math.js` 하나를 원본으로 두고 정리노트에 그대로 복사해 넣는다. 복사본이 원본과 같은지는 테스트로 강제한다. 콘텐츠 규칙은 `tests/test_notes_html.py`의 계약 목록(ID, 필수 용어, 레이어, 링크)으로 표현한다. 각 콘텐츠 태스크는 먼저 자기 섹션을 계약에 추가해 테스트를 실패시키고, 내용을 써서 통과시키는 TDD 순서를 따른다.

**Tech Stack:** HTML5 + 직접 작성한 CSS(변수, 다크모드), KaTeX 0.16.11 auto-render, Pretendard 1.3.9, 바닐라 JS. 테스트는 Python 3 `unittest`(표준 `html.parser`만 사용)와 Node 24의 `node:test`로 한다.

**Spec:** `docs/plans/2026-09-21-lecture-notes-review-html-design.md`
**수업 내용 원천 (콘텐츠 태스크 필독):** `docs/plans/2026-09-21-lecture-notes-refs/stt-0909-summary.md`, `stt-0914-summary.md`, `stt-0916-summary.md`. 모두 STT 전사본을 정밀 요약한 것이며 타임스탬프, 칠판 유도, 원문 인용이 들어 있다. 아래 콘텐츠 명세에서 `0914§7`처럼 쓴 표기는 `stt-0914-summary.md`의 7절을 뜻한다.

## Global Constraints

- 산출물 경로(정확히 이대로):
  - `강의노트/정리노트_0909-0916_When_Models_Meet_Data.html`
  - `강의노트/복습문제_0909-0916_When_Models_Meet_Data.html`
- 외부 리소스는 아래 두 접두사로 시작하는 URL만 허용한다. Tailwind CDN은 금지다.
  - `https://cdn.jsdelivr.net/npm/katex@0.16.11/`
  - `https://cdn.jsdelivr.net/npm/pretendard@1.3.9/`
- `<html lang="ko">`를 쓴다. UI 문구는 한국어로 쓰고 전문용어는 영어를 병기한다.
- 수식은 `$…$`(인라인)와 `$$…$$`(디스플레이)로만 쓴다.
  - 본문 텍스트에 리터럴 `$`를 쓰지 않는다.
  - TeX 안에서 `<`, `>`, `&`를 쓰지 않는다. `\lt`, `\gt`를 쓰고, 정렬 환경 대신 `$$` 줄을 나눈다.
- 이 계획의 코드블록과 표에 있는 **TeX 수식 문자열은 공백까지 그대로** 복사한다. 테스트가 부분 문자열로 검사한다.
- 수업에서 아직 다루지 않은 주제는 `#s5-next`에만 적는다. `d-separation`, `Bayes factor`, `Bayesian Model Selection`, `Directed Graphical`, `MCMC`가 대상이다.
- 수업에서 미룬 유도에는 반드시 `<div class="layer supp">`와 배지 `📎 보충 · 수업 미유도`를 붙인다.
- 교수님이나 STT의 말실수(예: "LLaMA 30만 개", 지수분포 식 혼동)는 옮기지 않는다. 식은 올바른 형태로 쓴다.
- 순수 잡담은 넣지 않는다. 예: 화장실, 이메일 부탁, 자리 이동, GPU 가격, 학생 실명 농담. 학생 이름은 "한 학생"으로 쓴다.
- 모바일 375px 폭에서 페이지 가로 스크롤이 없어야 한다. `prefers-color-scheme: dark`를 지원한다.
- 링크에 쓰는 한글 파일명은 그대로 두고, 공백만 `%20`으로 인코딩한다(예: `추가%20강의/…`).
- 테스트 실행은 두 명령이다.
  - Python: `python3 -m unittest discover -s tests -p "test_*.py" -v`
  - Node: `node --test tests/widget_math.test.js`
- 기존 파일(STT, PDF, 추가 강의 HTML, 기존 스크립트와 테스트)은 수정하지 않는다. 커밋할 때는 각 태스크가 만든 파일만 스테이징한다.

---

## File Structure

| 파일 | 책임 |
|---|---|
| `scripts/review_answers.py` | 복습문제 정답을 Fraction으로 정확히 계산하는 정답 키. CLI로 출력 |
| `tests/test_review_answers.py` | 정답 키 단위 테스트 |
| `scripts/check_notes_html.py` | 표준 라이브러리만 쓰는 HTML 파서와 검사기(ID, 섹션·컨테이너 텍스트, 링크, 수식 구분자, 인라인 스크립트). CLI 제공 |
| `tests/test_check_notes_html.py` | 검사기 단위 테스트(인라인 픽스처) |
| `scripts/widget_math.js` | 위젯 수학 함수의 원본(브라우저와 Node 양용) |
| `tests/widget_math.test.js` | 위젯 수학 단위 테스트(node:test) |
| `tests/test_notes_html.py` | 두 HTML의 계약 테스트. `COMPLETED_SECTIONS`와 `COMPLETED_PROBLEMS`로 점진 활성화 |
| `강의노트/정리노트_0909-0916_When_Models_Meet_Data.html` | 정리노트 |
| `강의노트/복습문제_0909-0916_When_Models_Meet_Data.html` | 복습문제 |

---

### Task 1: 브랜치 생성 + 정답 키(`review_answers.py`)

**Files:**
- Create: `scripts/review_answers.py`
- Test: `tests/test_review_answers.py`

**Interfaces:**
- Produces:
  - `ex61_marginals() -> tuple[list[Fraction], list[Fraction]]` (p(x) 5개, p(y) 3개)
  - `ex61_conditionals() -> tuple[list[Fraction], list[Fraction]]` (p(x|y1), p(y|x3))
  - `ex64_bag2_given_mango() -> Fraction`
  - `beta_bernoulli_posterior(alpha:int, beta:int, n:int, k:int) -> tuple[int,int]`
  - `coin_estimates(n:int, k:int, alpha:int, beta:int) -> tuple[Fraction,Fraction,Fraction]` (ml, map, predictive)
  - `ex71_stationary_points() -> list[tuple[float,str]]` (x 오름차순, 종류는 `"min"`/`"max"`/`"saddle"`)
  - `map_l2_lambda(sigma2, b2, n) -> Fraction`

- [ ] **Step 1: 브랜치 생성**

```bash
git checkout -b feat/lecture-notes-0909-0916
```

- [ ] **Step 2: 실패하는 테스트 작성** — `tests/test_review_answers.py`

```python
#!/usr/bin/env python3
"""Unit tests for scripts/review_answers.py (복습문제 정답 키)."""

from fractions import Fraction as F
from pathlib import Path
import math
import sys
import unittest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from review_answers import (  # noqa: E402
    beta_bernoulli_posterior,
    coin_estimates,
    ex61_conditionals,
    ex61_marginals,
    ex64_bag2_given_mango,
    ex71_stationary_points,
    map_l2_lambda,
)


class TestExercise61(unittest.TestCase):
    def test_marginals(self):
        px, py = ex61_marginals()
        self.assertEqual(px, [F(16, 100), F(17, 100), F(11, 100), F(22, 100), F(34, 100)])
        self.assertEqual(py, [F(26, 100), F(47, 100), F(27, 100)])
        self.assertEqual(sum(px), 1)
        self.assertEqual(sum(py), 1)

    def test_conditionals(self):
        x_given_y1, y_given_x3 = ex61_conditionals()
        self.assertEqual(x_given_y1, [F(1, 26), F(1, 13), F(3, 26), F(5, 13), F(5, 13)])
        self.assertEqual(y_given_x3, [F(3, 11), F(5, 11), F(3, 11)])


class TestExercise64(unittest.TestCase):
    def test_bayes_bag2(self):
        self.assertEqual(ex64_bag2_given_mango(), F(1, 3))


class TestBetaBernoulli(unittest.TestCase):
    def test_posterior_parameters(self):
        self.assertEqual(beta_bernoulli_posterior(4, 4, 10, 2), (6, 12))

    def test_class_coin_example(self):
        ml, map_, pred = coin_estimates(10, 2, 4, 4)
        self.assertEqual(ml, F(1, 5))
        self.assertEqual(map_, F(5, 16))
        self.assertEqual(pred, F(1, 3))

    def test_uniform_prior_map_equals_ml(self):
        ml, map_, _ = coin_estimates(10, 2, 1, 1)
        self.assertEqual(map_, ml)


class TestExercise71(unittest.TestCase):
    def test_stationary_points(self):
        pts = ex71_stationary_points()
        self.assertEqual(len(pts), 2)
        (x1, k1), (x2, k2) = pts
        self.assertAlmostEqual(x1, -2 - math.sqrt(5))
        self.assertEqual(k1, "max")
        self.assertAlmostEqual(x2, -2 + math.sqrt(5))
        self.assertEqual(k2, "min")


class TestMapL2(unittest.TestCase):
    def test_lambda(self):
        self.assertEqual(map_l2_lambda(1, F(1, 2), 10), F(1, 5))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: 실패 확인**

Run: `python3 -m unittest discover -s tests -p "test_review_answers.py" -v`
Expected: FAIL. `ModuleNotFoundError: No module named 'review_answers'`

- [ ] **Step 4: 구현** — `scripts/review_answers.py`

```python
#!/usr/bin/env python3
"""
복습문제_0909-0916 정답 키.

교과서(MML)에는 공식 풀이가 없으므로, 복습문제 HTML의 모든 수치 정답을
여기서 Fraction으로 정확히 계산해 대조한다. 실행하면 정답표를 출력한다.
"""

from __future__ import annotations

from fractions import Fraction
import math

# MML Exercise 6.1: 행 = y1..y3, 열 = x1..x5
EX61_TABLE: tuple[tuple[Fraction, ...], ...] = (
    tuple(Fraction(v, 100) for v in (1, 2, 3, 10, 10)),
    tuple(Fraction(v, 100) for v in (5, 10, 5, 7, 20)),
    tuple(Fraction(v, 100) for v in (10, 5, 3, 5, 4)),
)


def ex61_marginals() -> tuple[list[Fraction], list[Fraction]]:
    """p(x)는 열 합, p(y)는 행 합."""
    px = [sum(row[j] for row in EX61_TABLE) for j in range(5)]
    py = [sum(row) for row in EX61_TABLE]
    return px, py


def ex61_conditionals() -> tuple[list[Fraction], list[Fraction]]:
    """p(x | Y=y1), p(y | X=x3)."""
    px, py = ex61_marginals()
    x_given_y1 = [v / py[0] for v in EX61_TABLE[0]]
    y_given_x3 = [row[2] / px[2] for row in EX61_TABLE]
    return x_given_y1, y_given_x3


def ex64_bag2_given_mango() -> Fraction:
    """MML Exercise 6.4: P(bag2 | mango)."""
    p_bag1, p_bag2 = Fraction(6, 10), Fraction(4, 10)
    p_mango_bag1, p_mango_bag2 = Fraction(4, 6), Fraction(4, 8)
    numerator = p_bag2 * p_mango_bag2
    return numerator / (p_bag1 * p_mango_bag1 + numerator)


def beta_bernoulli_posterior(alpha: int, beta: int, n: int, k: int) -> tuple[int, int]:
    """Beta(alpha, beta) prior + Bernoulli 관측 n번 중 k번 1 -> Beta(alpha+k, beta+n-k)."""
    return alpha + k, beta + n - k


def coin_estimates(n: int, k: int, alpha: int, beta: int) -> tuple[Fraction, Fraction, Fraction]:
    """(ML, MAP=사후 최빈값, 다음 관측이 1일 예측확률=사후 평균)."""
    ml = Fraction(k, n)
    map_ = Fraction(k + alpha - 1, n + alpha + beta - 2)
    pred = Fraction(k + alpha, n + alpha + beta)
    return ml, map_, pred


def ex71_stationary_points() -> list[tuple[float, str]]:
    """MML Exercise 7.1: f(x) = x^3 + 6x^2 - 3x - 5."""
    points = []
    for x in (-2 - math.sqrt(5), -2 + math.sqrt(5)):
        second = 6 * x + 12
        kind = "min" if second > 0 else "max" if second < 0 else "saddle"
        points.append((x, kind))
    return points


def map_l2_lambda(sigma2, b2, n) -> Fraction:
    """가우시안 likelihood(분산 sigma2) + N(0, b2 I) prior의 MAP = 정규화 LS의 lambda."""
    return Fraction(sigma2) / (n * Fraction(b2))


def main() -> None:
    px, py = ex61_marginals()
    x_y1, y_x3 = ex61_conditionals()
    print("Ex 6.1 p(x):", [str(v) for v in px], "p(y):", [str(v) for v in py])
    print("Ex 6.1 p(x|y1):", [str(v) for v in x_y1], "p(y|x3):", [str(v) for v in y_x3])
    print("Ex 6.4 P(bag2|mango):", ex64_bag2_given_mango())
    print("Ex 6.3 posterior Beta(4,4), N=10, k=2:", beta_bernoulli_posterior(4, 4, 10, 2))
    print("coin (ML, MAP, pred) a=4:", [str(v) for v in coin_estimates(10, 2, 4, 4)])
    print("Ex 7.1:", ex71_stationary_points())


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: 통과 확인**

Run: `python3 -m unittest discover -s tests -p "test_review_answers.py" -v`
Expected: 8개 테스트 모두 PASS

- [ ] **Step 6: 커밋**

```bash
git add scripts/review_answers.py tests/test_review_answers.py
git commit -m "feat: add answer key for 0909-0916 review problems"
```

---

### Task 2: HTML 검사기(`check_notes_html.py`)

**Files:**
- Create: `scripts/check_notes_html.py`
- Test: `tests/test_check_notes_html.py`

**Interfaces:**
- Produces:
  - `parse_html(source: str) -> Doc`, `parse_file(path) -> Doc`
  - `Doc` 필드:
    - `lang`, `ids: set[str]`, `duplicate_ids: set[str]`, `id_section: dict[str, str|None]`
    - `hrefs: list[str]`, `external_resources: list[str]`
    - `section_text: dict[str,str]`, `containers: dict[str, Container]`, `scripts_by_id: dict[str,str]`, `body_text: str`
  - `Container` 필드: `id`, `classes: set[str]`, `attrs: dict[str,str]`, `section`, `text`, `hrefs: list[str]`, `child_classes: set[str]`
    - 컨테이너는 class에 `topic` 또는 `card`가 있고 id가 있는 요소다.
  - `math_delimiter_errors(text: str) -> list[str]`
  - `broken_links(doc: Doc, base_dir: Path) -> list[str]` (href를 퍼센트 디코딩한 뒤 검사)
  - `main(argv) -> int` (CLI. 문제가 있으면 1)

- [ ] **Step 1: 실패하는 테스트 작성** — `tests/test_check_notes_html.py`

```python
#!/usr/bin/env python3
"""Unit tests for scripts/check_notes_html.py."""

from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from check_notes_html import broken_links, math_delimiter_errors, parse_file, parse_html  # noqa: E402

FIXTURE = """<!DOCTYPE html>
<html lang="ko"><head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<style>.x{color:red}</style>
</head><body>
<section id="s1"><h2>제목</h2>
  <article class="topic" id="s1-a"><h3>토픽</h3>
    <div class="layer eli5"><p>비유 $a$ <br> 문장</p><svg id="fig-a"><path d="M0 0"/></svg></div>
    <div class="layer formal">$$x^2$$ <a href="#s1">위로</a></div>
  </article>
</section>
<section id="s2"><p>둘째 섹션</p></section>
<script id="widget-math">function f(){ return `${1}`; }</script>
</body></html>"""


class TestParse(unittest.TestCase):
    def setUp(self):
        self.doc = parse_html(FIXTURE)

    def test_lang_and_ids(self):
        self.assertEqual(self.doc.lang, "ko")
        self.assertTrue({"s1", "s1-a", "fig-a", "s2", "widget-math"} <= self.doc.ids)
        self.assertEqual(self.doc.duplicate_ids, set())

    def test_id_section_mapping(self):
        self.assertEqual(self.doc.id_section["fig-a"], "s1")
        self.assertEqual(self.doc.id_section["s1-a"], "s1")

    def test_section_text_and_container(self):
        self.assertIn("비유", self.doc.section_text["s1"])
        self.assertIn("둘째 섹션", self.doc.section_text["s2"])
        con = self.doc.containers["s1-a"]
        self.assertEqual(con.section, "s1")
        self.assertIn("문장", con.text)
        self.assertTrue({"layer", "eli5", "formal"} <= con.child_classes)
        self.assertEqual(con.hrefs, ["#s1"])

    def test_scripts_and_styles_excluded_from_text(self):
        self.assertNotIn("return", self.doc.body_text)
        self.assertNotIn("color:red", self.doc.body_text)
        self.assertIn("function f()", self.doc.scripts_by_id["widget-math"])

    def test_external_resources(self):
        self.assertEqual(len(self.doc.external_resources), 2)

    def test_duplicate_ids_detected(self):
        doc = parse_html('<div id="a"></div><p id="a"></p>')
        self.assertEqual(doc.duplicate_ids, {"a"})


class TestMathDelimiters(unittest.TestCase):
    def test_balanced(self):
        self.assertEqual(math_delimiter_errors("a $x$ b $$y$$ c \\$5"), [])

    def test_unbalanced_inline(self):
        self.assertEqual(math_delimiter_errors("a $x b"), ["unbalanced $ (inline math)"])

    def test_unbalanced_display(self):
        self.assertIn("unbalanced $$ (display math)", math_delimiter_errors("$$x"))


class TestBrokenLinks(unittest.TestCase):
    def test_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "sub dir").mkdir()
            (base / "sub dir" / "b.html").write_text('<p id="there"></p>', encoding="utf-8")
            a = base / "a.html"
            a.write_text(
                '<p id="here"></p>'
                '<a href="#here"></a><a href="#nope"></a>'
                '<a href="sub%20dir/b.html#there"></a><a href="sub%20dir/b.html#gone"></a>'
                '<a href="missing.html"></a><a href="https://example.com"></a>',
                encoding="utf-8",
            )
            broken = broken_links(parse_file(a), base)
            self.assertEqual(broken, ["#nope", "sub%20dir/b.html#gone", "missing.html"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s tests -p "test_check_notes_html.py" -v`
Expected: FAIL. `ModuleNotFoundError: No module named 'check_notes_html'`

- [ ] **Step 3: 구현** — `scripts/check_notes_html.py`

```python
#!/usr/bin/env python3
"""
정리노트/복습문제 HTML 구조 검사기 (표준 라이브러리만 사용).

- parse_html / parse_file: id, 링크, 섹션·컨테이너별 텍스트, 인라인 스크립트 수집
- math_delimiter_errors: KaTeX 구분자($, $$) 짝 검사
- broken_links: 앵커/상대경로 링크 검사
CLI: python3 scripts/check_notes_html.py <file.html> [...]
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
CONTAINER_CLASSES = {"topic", "card"}


@dataclass
class Container:
    id: str
    classes: set[str]
    attrs: dict[str, str]
    section: str | None
    text: str = ""
    hrefs: list[str] = field(default_factory=list)
    child_classes: set[str] = field(default_factory=set)


@dataclass
class Doc:
    lang: str | None = None
    ids: set[str] = field(default_factory=set)
    duplicate_ids: set[str] = field(default_factory=set)
    id_section: dict[str, str | None] = field(default_factory=dict)
    hrefs: list[str] = field(default_factory=list)
    external_resources: list[str] = field(default_factory=list)
    section_text: dict[str, str] = field(default_factory=lambda: defaultdict(str))
    containers: dict[str, Container] = field(default_factory=dict)
    scripts_by_id: dict[str, str] = field(default_factory=dict)
    body_text: str = ""


class _Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doc = Doc()
        self.stack: list[tuple[str, str | None, str | None]] = []  # (tag, section_id, container_id)
        self.raw_tag: str | None = None
        self.script_id: str | None = None

    def _context(self) -> tuple[str | None, str | None]:
        if not self.stack:
            return None, None
        _, sec, con = self.stack[-1]
        return sec, con

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        sec, con = self._context()
        classes = set(a.get("class", "").split())
        if tag == "html":
            self.doc.lang = a.get("lang")
        el_id = a.get("id")
        if el_id:
            if el_id in self.doc.ids:
                self.doc.duplicate_ids.add(el_id)
            self.doc.ids.add(el_id)
        if tag == "section" and el_id:
            sec = el_id
        if el_id:
            self.doc.id_section[el_id] = sec
        if con is not None:
            self.doc.containers[con].child_classes |= classes
        if el_id and classes & CONTAINER_CLASSES:
            self.doc.containers[el_id] = Container(el_id, classes, a, sec)
            con = el_id
        if tag == "a" and "href" in a:
            self.doc.hrefs.append(a["href"])
            if con is not None:
                self.doc.containers[con].hrefs.append(a["href"])
        if tag == "script" and a.get("src"):
            self.doc.external_resources.append(a["src"])
        if tag == "link" and "stylesheet" in a.get("rel", "") and a.get("href"):
            self.doc.external_resources.append(a["href"])
        if tag in ("script", "style"):
            self.raw_tag = tag
            self.script_id = el_id if tag == "script" else None
            if self.script_id:
                self.doc.scripts_by_id[self.script_id] = ""
        if tag not in VOID_TAGS:
            self.stack.append((tag, sec, con))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.raw_tag = None
            self.script_id = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.raw_tag == "script":
            if self.script_id:
                self.doc.scripts_by_id[self.script_id] += data
            return
        if self.raw_tag == "style":
            return
        sec, con = self._context()
        self.doc.body_text += data
        if sec:
            self.doc.section_text[sec] += data
        if con:
            self.doc.containers[con].text += data


def parse_html(source: str) -> Doc:
    parser = _Parser()
    parser.feed(source)
    parser.close()
    return parser.doc


def parse_file(path: Path | str) -> Doc:
    return parse_html(Path(path).read_text(encoding="utf-8"))


def math_delimiter_errors(text: str) -> list[str]:
    errors: list[str] = []
    t = text.replace("\\$", "")
    if t.count("$$") % 2:
        errors.append("unbalanced $$ (display math)")
    t = re.sub(r"\$\$.*?\$\$", "", t, flags=re.S)
    if t.count("$") % 2:
        errors.append("unbalanced $ (inline math)")
    return errors


def broken_links(doc: Doc, base_dir: Path) -> list[str]:
    broken: list[str] = []
    cache: dict[Path, Doc] = {}
    for href in doc.hrefs:
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        path_part, _, frag = href.partition("#")
        if not path_part:
            if frag not in doc.ids:
                broken.append(href)
            continue
        target = (Path(base_dir) / unquote(path_part)).resolve()
        if not target.exists():
            broken.append(href)
            continue
        if frag and target.suffix == ".html":
            if target not in cache:
                cache[target] = parse_file(target)
            if frag not in cache[target].ids:
                broken.append(href)
    return broken


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    status = 0
    for name in argv:
        path = Path(name)
        doc = parse_file(path)
        problems = [f"duplicate id: {i}" for i in sorted(doc.duplicate_ids)]
        problems += math_delimiter_errors(doc.body_text)
        problems += [f"broken link: {h}" for h in broken_links(doc, path.parent)]
        print(f"{path}: {'OK' if not problems else 'FAIL'}")
        for problem in problems:
            print(f"  - {problem}")
        status |= int(bool(problems))
    return status


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 통과 확인**

Run: `python3 -m unittest discover -s tests -p "test_check_notes_html.py" -v`
Expected: 10개 테스트 모두 PASS

- [ ] **Step 5: 커밋**

```bash
git add scripts/check_notes_html.py tests/test_check_notes_html.py
git commit -m "feat: add stdlib HTML checker for study notes"
```

---

### Task 3: 위젯 수학 모듈(`widget_math.js`)

**Files:**
- Create: `scripts/widget_math.js`
- Test: `tests/widget_math.test.js`

**Interfaces:**
- Produces(브라우저에서는 전역 함수, Node에서는 `module.exports`):
  - `polyFeatures(x:number, degree:number) -> number[]` (`[1, x, …, x^degree]`)
  - `solveLinear(A:number[][], b:number[]) -> number[]` (부분 피벗 가우스-조던. 특이행렬이면 `Error('singular')`)
  - `ridgeFit(xs, ys, degree, lambda) -> number[]`: `(ΦᵀΦ + NλI)θ = Φᵀy`의 해. 절편을 포함한 모든 θ에 벌점을 준다(슬라이드 식 `λ‖θ‖²`와 같음).
  - `predictPoly(theta, x) -> number`, `mse(theta, xs, ys) -> number`
  - `mulberry32(seed) -> () => number` (0 이상 1 미만)
  - `makeDataset(seed) -> {trainX, trainY, testX, testY, truth}`
    - train은 [-1,1]에서 등간격 10개, test(unseen)는 [-0.95,0.95]에서 등간격 10개다.
    - 진짜 함수는 `sin(πx)`이고, 노이즈는 σ=0.25 가우시안이다.
  - `lgamma(z)`, `betaPdf(t, a, b) -> number` (t≤0 또는 t≥1이면 0)
  - `coinEstimates(N, k, a) -> {ml, map, pred}`: 대칭 prior Beta(a, a) 기준이다.

- [ ] **Step 1: 실패하는 테스트 작성** — `tests/widget_math.test.js`

```js
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const m = require('../scripts/widget_math.js');

const close = (a, b, eps = 1e-9) => assert.ok(Math.abs(a - b) < eps, `${a} !~ ${b}`);

test('polyFeatures builds [1, x, x^2, ...]', () => {
  assert.deepEqual(m.polyFeatures(2, 3), [1, 2, 4, 8]);
});

test('solveLinear solves a 2x2 system', () => {
  const x = m.solveLinear([[2, 1], [1, 3]], [3, 5]);
  close(x[0], 0.8);
  close(x[1], 1.4);
});

test('solveLinear throws on singular matrix', () => {
  assert.throws(() => m.solveLinear([[1, 2], [2, 4]], [1, 2]), /singular/);
});

test('ridgeFit recovers an exact line when lambda = 0', () => {
  const t = m.ridgeFit([0, 1, 2], [1, 3, 5], 1, 0);
  close(t[0], 1);
  close(t[1], 2);
});

test('ridgeFit shrinks parameters toward the origin for huge lambda', () => {
  const t = m.ridgeFit([0, 1, 2], [1, 3, 5], 1, 1e6);
  assert.ok(t.every((v) => Math.abs(v) < 1e-4));
});

test('makeDataset is deterministic per seed', () => {
  assert.deepEqual(m.makeDataset(7).trainY, m.makeDataset(7).trainY);
  assert.notDeepEqual(m.makeDataset(7).trainY, m.makeDataset(8).trainY);
});

test('seed 7 shows overfitting, good fit, underfitting', () => {
  const d = m.makeDataset(7);
  const fit = (deg, lam) => m.ridgeFit(d.trainX, d.trainY, deg, lam);
  const over = fit(9, 0);
  assert.ok(m.mse(over, d.trainX, d.trainY) < 1e-10);
  assert.equal(m.mse(over, d.testX, d.testY).toFixed(3), '0.712');
  assert.equal(m.mse(fit(3, 1e-3), d.testX, d.testY).toFixed(3), '0.109');
  assert.equal(m.mse(fit(1, 0), d.testX, d.testY).toFixed(3), '0.417');
});

test('betaPdf matches closed forms', () => {
  close(m.betaPdf(0.5, 1, 1), 1, 1e-9);
  close(m.betaPdf(0.3, 2, 2), 6 * 0.3 * 0.7, 1e-9);
  assert.equal(m.betaPdf(0, 2, 2), 0);
});

test('coinEstimates reproduces the class coin example', () => {
  const e = m.coinEstimates(10, 2, 4);
  close(e.ml, 0.2);
  close(e.map, 0.3125);
  close(e.pred, 1 / 3);
  const u = m.coinEstimates(10, 2, 1);
  close(u.map, u.ml);
});
```

- [ ] **Step 2: 실패 확인**

Run: `node --test tests/widget_math.test.js`
Expected: FAIL. `Cannot find module '../scripts/widget_math.js'`

- [ ] **Step 3: 구현** — `scripts/widget_math.js`

아래 내용을 **정확히 이대로** 쓴다. Task 4에서 이 파일 내용을 정리노트에 그대로 인라인한다.

```js
/* 위젯 수학 (정리노트 인라인 원본). 브라우저: 전역 함수 / Node: module.exports */
function polyFeatures(x, degree) {
  const row = [];
  for (let p = 0; p <= degree; p++) row.push(x ** p);
  return row;
}

function solveLinear(A, b) {
  const n = b.length;
  const M = A.map((row, i) => [...row, b[i]]);
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    [M[c], M[p]] = [M[p], M[c]];
    const piv = M[c][c];
    if (Math.abs(piv) < 1e-14) throw new Error('singular');
    for (let r = 0; r < n; r++) {
      if (r === c) continue;
      const f = M[r][c] / piv;
      for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k];
    }
  }
  return M.map((row, i) => row[n] / row[i]);
}

function ridgeFit(xs, ys, degree, lambda) {
  const N = xs.length;
  const D = degree + 1;
  const Phi = xs.map((x) => polyFeatures(x, degree));
  const A = Array.from({ length: D }, (_, i) =>
    Array.from({ length: D }, (_, j) => {
      let s = 0;
      for (let n = 0; n < N; n++) s += Phi[n][i] * Phi[n][j];
      return s + (i === j ? N * lambda : 0);
    })
  );
  const b = Array.from({ length: D }, (_, i) => {
    let s = 0;
    for (let n = 0; n < N; n++) s += Phi[n][i] * ys[n];
    return s;
  });
  return solveLinear(A, b);
}

function predictPoly(theta, x) {
  return theta.reduce((s, t, p) => s + t * x ** p, 0);
}

function mse(theta, xs, ys) {
  return xs.reduce((s, x, i) => s + (ys[i] - predictPoly(theta, x)) ** 2, 0) / xs.length;
}

function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function makeDataset(seed) {
  const rand = mulberry32(seed);
  const gauss = () => {
    const u = 1 - rand();
    const v = rand();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  const truth = (x) => Math.sin(Math.PI * x);
  const trainX = Array.from({ length: 10 }, (_, i) => -1 + (2 * i) / 9);
  const testX = Array.from({ length: 10 }, (_, i) => -0.95 + (1.9 * i) / 9);
  return {
    trainX,
    trainY: trainX.map((x) => truth(x) + 0.25 * gauss()),
    testX,
    testY: testX.map((x) => truth(x) + 0.25 * gauss()),
    truth,
  };
}

function lgamma(z) {
  const g = 7;
  const c = [
    0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
    -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6,
    1.5056327351493116e-7,
  ];
  if (z < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * z)) - lgamma(1 - z);
  z -= 1;
  let x = c[0];
  for (let i = 1; i < g + 2; i++) x += c[i] / (z + i);
  const t = z + g + 0.5;
  return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
}

function betaPdf(t, a, b) {
  if (t <= 0 || t >= 1) return 0;
  return Math.exp((a - 1) * Math.log(t) + (b - 1) * Math.log(1 - t) + lgamma(a + b) - lgamma(a) - lgamma(b));
}

function coinEstimates(N, k, a) {
  return { ml: k / N, map: (k + a - 1) / (N + 2 * a - 2), pred: (k + a) / (N + 2 * a) };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { polyFeatures, solveLinear, ridgeFit, predictPoly, mse, mulberry32, makeDataset, lgamma, betaPdf, coinEstimates };
}
```

- [ ] **Step 4: 통과 확인**

Run: `node --test tests/widget_math.test.js`
Expected: `# pass 9`, `# fail 0`

- [ ] **Step 5: 커밋**

```bash
git add scripts/widget_math.js tests/widget_math.test.js
git commit -m "feat: add widget math (ridge fit, beta pdf, coin estimates)"
```

---

### Task 4: 두 HTML 골격 + 계약 테스트

**Files:**
- Create: `강의노트/정리노트_0909-0916_When_Models_Meet_Data.html`
- Create: `강의노트/복습문제_0909-0916_When_Models_Meet_Data.html`
- Test: `tests/test_notes_html.py`

**Interfaces:**
- Consumes:
  - `check_notes_html.parse_file`, `broken_links`, `math_delimiter_errors` (Task 2)
  - `scripts/widget_math.js` 전문 (Task 3)
- Produces(이후 태스크가 쓰는 것):
  - 모든 섹션·토픽 id(아래 `TOPIC_IDS`)와 문제 카드 id `p1`~`p10`
  - CSS 클래스:
    - 레이어: `layer eli5|formal|prof|warn|supp`
    - 배지: `badge`, `badge supp`, `tag date`, `tag slide`
    - 레이아웃과 위젯: `figure`, `widget`, `controls`, `readout`, `legend`, `table-wrap`
    - 문제 카드: `card`, `problem`, `original`, `hint`, `solution`, `answer`, `link-back`, `done`
    - 플롯: `plot-*`, `pt-*`, `mark-*`, `axis`, `tick`
  - `tests/test_notes_html.py` 안의 `COMPLETED_SECTIONS`, `COMPLETED_PROBLEMS` 리스트(이후 태스크가 값을 추가)

- [ ] **Step 1: 계약 테스트 작성** — `tests/test_notes_html.py`

```python
#!/usr/bin/env python3
"""
정리노트/복습문제 HTML 계약 테스트.

콘텐츠 태스크는 먼저 COMPLETED_SECTIONS / COMPLETED_PROBLEMS 에 자기 항목을 추가해
테스트를 실패시킨 뒤(RED), 내용을 채워 통과시킨다(GREEN).
"""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from check_notes_html import broken_links, math_delimiter_errors, parse_file  # noqa: E402

NOTE_PATH = ROOT / "강의노트" / "정리노트_0909-0916_When_Models_Meet_Data.html"
REVIEW_PATH = ROOT / "강의노트" / "복습문제_0909-0916_When_Models_Meet_Data.html"
WIDGET_JS_PATH = ROOT / "scripts" / "widget_math.js"
NOTE_HREF = "정리노트_0909-0916_When_Models_Meet_Data.html"

ALLOWED_EXTERNAL_PREFIXES = (
    "https://cdn.jsdelivr.net/npm/katex@0.16.11/",
    "https://cdn.jsdelivr.net/npm/pretendard@1.3.9/",
)

SECTION_IDS = ["s0", "s1", "s2", "s3", "s4", "s5"]
TOPIC_IDS = {
    "s0": ["s0-course"],
    "s1": ["s1-components", "s1-induction", "s1-data", "s1-model", "s1-prob-model", "s1-learning"],
    "s2": ["s2-erm", "s2-affine", "s2-matrix", "s2-risk", "s2-reg"],
    "s3": ["s3-likelihood", "s3-iid", "s3-mle-ls", "s3-map", "s3-map-l2", "s3-fitting"],
    "s4": ["s4-generative", "s4-joint", "s4-posterior", "s4-three-ways", "s4-coin", "s4-predictive"],
    "s5": ["s5-cheatsheet", "s5-prereq", "s5-next", "s5-links"],
}
LAYERED_SECTIONS = {"s1", "s2", "s3", "s4"}  # 이 섹션의 토픽은 eli5/formal/prof 레이어 필수
FIGURE_IDS = {
    "s1": ["fig-pipeline", "fig-induction", "fig-data-vector", "fig-det-vs-prob", "fig-three-phases"],
    "s2": ["fig-neuron", "fig-matrix-packing"],
    "s3": ["fig-log", "fig-factory", "fig-prior-likelihood-posterior", "fig-model-class", "fig-fitting-3"],
    "s4": ["fig-general"],
}
WIDGET_IDS = {
    "s2": ["widget-reg", "reg-degree", "reg-lambda", "reg-plot", "reg-train-mse", "reg-test-mse", "widget-reg-ui"],
    "s4": ["widget-coin", "coin-n", "coin-k", "coin-a", "coin-plot", "coin-ml", "coin-map", "coin-pred", "widget-coin-ui"],
}
SUPP_TOPICS = {"s3-map-l2", "s4-coin"}
FORBIDDEN_OUTSIDE_NEXT = ["d-separation", "Bayes factor", "Bayesian Model Selection", "Directed Graphical", "MCMC"]

REQUIRED_TERMS = {
    "s0-course": ["35%", "20%", "10%", "지도학습", "비지도학습", "강화학습", "전제 과목", "Universal Approximation"],
    "s1-components": ["데이터", "모델", "러닝", "데이터가 부족", "GPU"],
    "s1-induction": ["귀납", "연역", "파란 점", "메인 레슨", "y(t) = x(t) * h(t)"],
    "s1-data": ["볼드", "N \\to \\infty", "\\mathbf{x}_n \\in \\mathbb{R}^D", "clustering", "MBTI", "feature", "PCA", "SVD", "kernel"],
    "s1-model": ["정답은 없", "suppose", "assume", "취사선택", "y = 3x_1 + 5x_2 + 6x_3 + 0.6"],
    "s1-prob-model": ["노이즈", "x=60", "p(y \\mid \\mathbf{x}) = \\mathcal{N}\\big(y \\mid f(\\mathbf{x}), \\sigma^2\\big)", "대령", "MLE"],
    "s1-learning": ["unseen", "such that", "prediction", "training", "model selection", "hyperparameter", "learning rate", "grid search", "gradient descent"],
    "s2-erm": ["Empirical", "Risk", "Minimization", "in terms of", "for all", "\\hat{y}_n \\approx y_n"],
    "s2-affine": ["augmentation", "affine", "원점", "\\boldsymbol{\\theta}^\\top \\mathbf{x}_n", "activation", "sigmoid", "ReLU"],
    "s2-matrix": ["\\in \\mathbb{R}^{N \\times D}", "R_{\\text{emp}}", "(y_n - \\hat{y}_n)^2", "\\|\\mathbf{y} - \\mathbf{X}\\boldsymbol{\\theta}\\|^2", "김밥", "전치"],
    "s2-risk": ["R_{\\text{true}}", "7:3", "validation", "기보", "해 아래"],
    "s2-reg": ["overfitting", "penalty", "regularizer", "\\lambda \\|\\boldsymbol{\\theta}\\|^2", "hyperparameter", "sparse", "\\|\\boldsymbol{\\theta}\\|_1", "Bayesian Optimization"],
    "s3-likelihood": ["likelihood", "그럴듯함", "\\mathcal{L}(\\boldsymbol{\\theta}) = -\\log p(\\mathbf{x} \\mid \\boldsymbol{\\theta})", "단조", "클로즈업", "1보다 클 수", "latent", "\\lambda e^{-\\lambda x}"],
    "s3-iid": ["i.i.d.", "\\prod_{n=1}^{N} p(y_n \\mid \\mathbf{x}_n, \\boldsymbol{\\theta})", "동일한 공장", "추석 선물 세트"],
    "s3-mle-ls": ["\\varepsilon \\sim \\mathcal{N}(0, \\sigma^2)", "\\frac{N}{2}\\log(2\\pi\\sigma^2)", "least squares", "suppose", "delta"],
    "s3-map": ["posterior", "CT", "\\propto", "argmax", "\\boldsymbol{\\theta}_{\\text{MAP}}", "uniform"],
    "s3-map-l2": ["\\mathcal{N}(\\mathbf{0}, b^2 \\mathbf{I})", "\\frac{\\sigma^2}{N b^2}", "나중에"],
    "s3-fitting": ["M^*", "M_{\\boldsymbol{\\theta}^*}", "빨간 거리", "overfitting", "underfitting", "good fitting", "되새김질", "파라미터 개수"],
    "s4-generative": ["generative process", "했을 거야", "노이즈", "c_n = \\mathbf{x}_n^\\top \\boldsymbol{\\theta}"],
    "s4-joint": ["joint", "marginal", "hidden", "latent", "인셉션", "확률 및 랜덤변수"],
    "s4-posterior": ["p(\\mathbf{x}, \\boldsymbol{\\theta}) = p(\\mathbf{x} \\mid \\boldsymbol{\\theta})\\, p(\\boldsymbol{\\theta})", "prior", "모름지기", "marginal likelihood", "\\int p(\\mathbf{x}, \\boldsymbol{\\theta})\\, d\\boldsymbol{\\theta}", "정규화"],
    "s4-three-ways": ["\\boldsymbol{\\theta}_{\\text{ML}}", "\\boldsymbol{\\theta}_{\\text{MAP}}", "Fully Bayesian", "장군"],
    "s4-coin": ["0.2", "0.3125", "\\frac{2}{\\theta} - \\frac{8}{1-\\theta} = 0", "머니볼", "그 사이", "Beta"],
    "s4-predictive": ["posterior predictive", "P(A \\mid \\boldsymbol{\\theta})\\, P(\\boldsymbol{\\theta} \\mid \\mathbf{X})", "조건부 독립", "mixture", "EM"],
    "s5-cheatsheet": ["치트시트", "R_{\\text{emp}}", "\\boldsymbol{\\theta}_{\\text{MAP}}"],
    "s5-prereq": ["Ch.2", "Ch.3", "Ch.5", "Ch.6", "Ch.7"],
    "s5-next": ["d-separation", "Bayes factor", "Linear Regression", "EM"],
    "s5-links": ["Lecture 10", "Lecture 11", "Lecture 12", "복습문제"],
}
S5_LINK_HREFS = [
    "추가%20강의/eli5_lecture10_statistical_inference_part1.html",
    "추가%20강의/eli5_lecture11_statistical_inference_part2.html",
    "추가%20강의/eli5_lecture12_statistical_inference_part3.html",
    "복습문제_0909-0916_When_Models_Meet_Data.html",
]

PROBLEMS = {
    "p1": {"source": "MML Example 8.1", "anchor": "s2-affine", "terms": ["\\mathbb{R}^{D+1}", "원점", "x_n^{(D)}"]},
    "p2": {"source": "MML Example 8.2", "anchor": "s2-matrix", "terms": ["\\|\\mathbf{y} - \\mathbf{X}\\boldsymbol{\\theta}\\|^2", "N \\times (D+1)"]},
    "p3": {"source": "MML Example 8.3", "anchor": "s2-reg", "terms": ["\\lambda \\to \\infty", "(\\mathbf{X}^\\top \\mathbf{X} + N\\lambda \\mathbf{I})", "hyperparameter"]},
    "p4": {"source": "MML Example 8.5", "anchor": "s3-mle-ls", "terms": ["\\frac{N}{2}\\log(2\\pi\\sigma^2)", "least squares"]},
    "p5": {"source": "MML Example 8.6", "anchor": "s3-map-l2", "terms": ["\\frac{\\sigma^2}{N b^2}", "\\frac{1}{2b^2}"]},
    "p6": {"source": "MML Exercise 6.1", "anchor": "s4-joint", "terms": ["0.16", "0.34", "0.26", "0.47", "\\frac{5}{13}", "\\frac{5}{11}"]},
    "p7": {"source": "MML Exercise 6.4", "anchor": "s3-map", "terms": ["\\frac{1}{3}", "0.6", "0.4"]},
    "p8": {"source": "MML Exercise 6.3", "anchor": "s4-coin", "terms": ["\\mathrm{Beta}(\\alpha + k, \\beta + N - k)", "0.3125", "\\frac{1}{3}"]},
    "p9": {"source": "MML Exercise 6.12", "anchor": "s4-generative", "terms": ["\\mathcal{N}\\big(\\mathbf{y} \\mid \\mathbf{A}\\mathbf{x} + \\mathbf{b}, \\mathbf{Q}\\big)"]},
    "p10": {"source": "MML Exercise 7.1", "anchor": "s4-coin", "terms": ["-2 + \\sqrt{5}", "-2 - \\sqrt{5}", "6x + 12"]},
}

# 콘텐츠 태스크가 여기에 항목을 추가한다.
COMPLETED_SECTIONS: list[str] = []
COMPLETED_PROBLEMS: list[str] = []


class _Common:
    path: Path

    @classmethod
    def setUpClass(cls):
        cls.doc = parse_file(cls.path)

    def test_lang_is_korean(self):
        self.assertEqual(self.doc.lang, "ko")

    def test_no_duplicate_ids(self):
        self.assertEqual(self.doc.duplicate_ids, set())

    def test_external_resources_allowlisted(self):
        for url in self.doc.external_resources:
            with self.subTest(url=url):
                self.assertTrue(url.startswith(ALLOWED_EXTERNAL_PREFIXES), url)

    def test_math_delimiters_balanced(self):
        self.assertEqual(math_delimiter_errors(self.doc.body_text), [])

    def test_links_resolve(self):
        self.assertEqual(broken_links(self.doc, self.path.parent), [])


class TestNote(_Common, unittest.TestCase):
    path = NOTE_PATH

    def test_all_section_and_topic_ids_exist(self):
        for sec in SECTION_IDS:
            self.assertIn(sec, self.doc.ids)
            for topic in TOPIC_IDS[sec]:
                with self.subTest(topic=topic):
                    self.assertIn(topic, self.doc.containers)
                    self.assertEqual(self.doc.containers[topic].section, sec)

    def test_widget_math_inline_copy_matches_source(self):
        inline = self.doc.scripts_by_id.get("widget-math", "")
        self.assertEqual(inline.strip(), WIDGET_JS_PATH.read_text(encoding="utf-8").strip())

    def test_scope_forbidden_terms(self):
        texts = {sec: self.doc.section_text.get(sec, "") for sec in SECTION_IDS if sec != "s5"}
        for topic in TOPIC_IDS["s5"]:
            if topic != "s5-next":
                texts[topic] = self.doc.containers[topic].text
        for where, text in texts.items():
            for term in FORBIDDEN_OUTSIDE_NEXT:
                with self.subTest(where=where, term=term):
                    self.assertNotIn(term, text)

    def test_completed_required_terms(self):
        for sec in COMPLETED_SECTIONS:
            for topic in TOPIC_IDS[sec]:
                text = self.doc.containers[topic].text
                for term in REQUIRED_TERMS[topic]:
                    with self.subTest(topic=topic, term=term):
                        self.assertIn(term, text)

    def test_completed_layers(self):
        for sec in COMPLETED_SECTIONS:
            if sec not in LAYERED_SECTIONS:
                continue
            for topic in TOPIC_IDS[sec]:
                with self.subTest(topic=topic):
                    self.assertTrue({"eli5", "formal", "prof"} <= self.doc.containers[topic].child_classes)

    def test_completed_supplement_badges(self):
        for topic in SUPP_TOPICS:
            sec = topic.split("-")[0]
            if sec in COMPLETED_SECTIONS:
                with self.subTest(topic=topic):
                    con = self.doc.containers[topic]
                    self.assertIn("supp", con.child_classes)
                    self.assertIn("📎 보충 · 수업 미유도", con.text)

    def test_completed_figures(self):
        for sec in COMPLETED_SECTIONS:
            for fig in FIGURE_IDS.get(sec, []):
                with self.subTest(fig=fig):
                    self.assertIn(fig, self.doc.ids)
                    self.assertEqual(self.doc.id_section[fig], sec)

    def test_completed_widgets(self):
        for sec in COMPLETED_SECTIONS:
            for wid in WIDGET_IDS.get(sec, []):
                with self.subTest(wid=wid):
                    self.assertIn(wid, self.doc.ids)

    def test_s5_links(self):
        if "s5" not in COMPLETED_SECTIONS:
            self.skipTest("s5 not completed yet")
        hrefs = self.doc.containers["s5-links"].hrefs
        for href in S5_LINK_HREFS:
            with self.subTest(href=href):
                self.assertIn(href, hrefs)


class TestReview(_Common, unittest.TestCase):
    path = REVIEW_PATH

    def test_all_problem_cards_exist(self):
        for pid in PROBLEMS:
            with self.subTest(pid=pid):
                self.assertIn(pid, self.doc.containers)
        self.assertIn("progress-count", self.doc.ids)

    def test_completed_problems(self):
        for pid in COMPLETED_PROBLEMS:
            spec = PROBLEMS[pid]
            card = self.doc.containers[pid]
            with self.subTest(pid=pid, check="source"):
                self.assertEqual(card.attrs.get("data-source"), spec["source"])
            with self.subTest(pid=pid, check="anchor"):
                self.assertIn(f"{NOTE_HREF}#{spec['anchor']}", card.hrefs)
            with self.subTest(pid=pid, check="parts"):
                self.assertTrue({"problem", "original", "hint", "solution", "answer", "link-back", "done"} <= card.child_classes)
            for term in spec["terms"]:
                with self.subTest(pid=pid, term=term):
                    self.assertIn(term, card.text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: ERROR. `setUpClass`에서 HTML 파일이 없어 `FileNotFoundError`

- [ ] **Step 3: 정리노트 골격 작성** — `강의노트/정리노트_0909-0916_When_Models_Meet_Data.html`

아래 전문을 쓴다. 단, `<script id="widget-math">` 안에는 `scripts/widget_math.js`의 **전체 내용을 한 글자도 바꾸지 않고** 붙여 넣는다. 테스트가 복사본을 원본과 비교한다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>머신러닝기초 정리노트</title>
  <meta name="description" content="정방철 교수님 머신러닝기초 0909·0914·0916 수업 정리 (When Models Meet Data)">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false,ignoredTags:['script','noscript','style','textarea','pre','code']})"></script>
  <style>
    :root {
      --bg: #f7f8fa; --surface: #ffffff; --surface-2: #f1f3f7; --ink: #1b2130; --ink-2: #4a5468; --line: #dde2ea;
      --accent: #2f6fdb; --accent-soft: #e6efff; --warn: #b54708; --warn-soft: #fff4e5;
      --prof: #6941c6; --prof-soft: #f3efff; --supp: #067647; --supp-soft: #e8f7ef;
      --eli5: #c4320a; --eli5-soft: #fff1eb; --danger: #d92d20;
      --radius: 14px; --shadow: 0 1px 2px rgba(16, 24, 40, .06);
    }
    @media (prefers-color-scheme: dark) {
      :root:not([data-theme="light"]) {
        --bg: #0f1218; --surface: #171b23; --surface-2: #1e2430; --ink: #e7eaf0; --ink-2: #a8b0c0; --line: #2a3140;
        --accent: #7aa7ff; --accent-soft: #1c2a45; --warn: #f5a15c; --warn-soft: #2d2215;
        --prof: #b69cff; --prof-soft: #251d3b; --supp: #5fd39a; --supp-soft: #14291f;
        --eli5: #ff9b73; --eli5-soft: #2e1c15; --danger: #ff6b61; --shadow: none;
      }
    }
    :root[data-theme="dark"] {
      --bg: #0f1218; --surface: #171b23; --surface-2: #1e2430; --ink: #e7eaf0; --ink-2: #a8b0c0; --line: #2a3140;
      --accent: #7aa7ff; --accent-soft: #1c2a45; --warn: #f5a15c; --warn-soft: #2d2215;
      --prof: #b69cff; --prof-soft: #251d3b; --supp: #5fd39a; --supp-soft: #14291f;
      --eli5: #ff9b73; --eli5-soft: #2e1c15; --danger: #ff6b61; --shadow: none;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; scroll-padding-top: 72px; }
    body { margin: 0; background: var(--bg); color: var(--ink); font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif; line-height: 1.7; font-size: 16px; }
    a { color: var(--accent); }
    .topbar { position: sticky; top: 0; z-index: 10; background: var(--surface); border-bottom: 1px solid var(--line); }
    .topbar-inner { max-width: 920px; margin: 0 auto; padding: 10px 16px; display: flex; gap: 12px; align-items: center; }
    .topbar strong { white-space: nowrap; font-size: 15px; }
    .toc { display: flex; gap: 4px; overflow-x: auto; white-space: nowrap; scrollbar-width: none; }
    .toc a { text-decoration: none; color: var(--ink-2); font-size: 13px; padding: 4px 10px; border-radius: 999px; }
    .toc a:hover { background: var(--accent-soft); color: var(--accent); }
    main { max-width: 920px; margin: 0 auto; padding: 24px 16px 80px; }
    .hero { padding: 24px 0 8px; }
    .hero h1 { font-size: clamp(26px, 5vw, 36px); line-height: 1.3; margin: 0 0 8px; }
    .hero p { color: var(--ink-2); margin: 0; }
    .legend-bar { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 0; font-size: 13px; }
    section { margin-top: 48px; }
    section > h2 { font-size: 24px; margin: 0 0 16px; padding-bottom: 8px; border-bottom: 2px solid var(--line); }
    .topic { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); padding: 20px; margin: 16px 0; }
    .topic h3 { margin: 0 0 6px; font-size: 19px; }
    .tags { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
    .tag { font-size: 12px; padding: 2px 8px; border-radius: 999px; background: var(--surface-2); color: var(--ink-2); }
    .layer { border-radius: 10px; padding: 12px 14px; margin: 10px 0; }
    .layer > :first-child { margin-top: 0; }
    .layer > :last-child { margin-bottom: 0; }
    .layer.eli5 { background: var(--eli5-soft); border-left: 4px solid var(--eli5); }
    .layer.eli5 .lead { font-size: 17px; font-weight: 600; }
    .layer.formal { background: var(--surface-2); border-left: 4px solid var(--accent); }
    .layer.prof { background: var(--prof-soft); border-left: 4px solid var(--prof); }
    .layer.warn { background: var(--warn-soft); border-left: 4px solid var(--warn); }
    .layer.supp { background: var(--supp-soft); border-left: 4px solid var(--supp); }
    .layer-title { font-weight: 700; font-size: 13px; letter-spacing: .02em; margin-bottom: 6px; display: block; }
    .badge { display: inline-block; font-size: 12px; font-weight: 700; padding: 2px 8px; border-radius: 999px; background: var(--surface); border: 1px solid var(--line); }
    .badge.supp { color: var(--supp); border-color: var(--supp); }
    blockquote { margin: 8px 0; padding: 0 0 0 12px; border-left: 3px solid var(--line); color: var(--ink-2); }
    .figure { margin: 12px 0; text-align: center; }
    .figure svg { width: 100%; height: auto; max-width: 640px; color: var(--ink); }
    .figure figcaption { font-size: 13px; color: var(--ink-2); margin-top: 4px; }
    .katex-display { overflow-x: auto; overflow-y: hidden; padding: 4px 0; }
    .table-wrap { overflow-x: auto; }
    table { border-collapse: collapse; width: 100%; font-size: 14px; }
    th, td { border: 1px solid var(--line); padding: 6px 8px; text-align: left; vertical-align: top; }
    th { background: var(--surface-2); }
    ol.steps li { margin: 6px 0; }
    .widget { background: var(--surface); border: 2px dashed var(--accent); border-radius: var(--radius); padding: 16px; margin: 20px 0; }
    .widget h4 { margin: 0 0 6px; }
    .widget-help { font-size: 14px; color: var(--ink-2); margin: 0 0 8px; }
    .controls { display: grid; gap: 8px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); margin-bottom: 8px; font-size: 14px; }
    .controls label { display: flex; align-items: center; gap: 8px; }
    .controls input[type=range] { flex: 1; min-width: 0; }
    .widget svg { width: 100%; height: auto; background: var(--surface-2); border-radius: 10px; }
    .readout { font-size: 15px; margin-top: 8px; }
    .legend { font-size: 13px; color: var(--ink-2); display: flex; flex-wrap: wrap; gap: 10px; }
    .sw { display: inline-block; width: 14px; height: 4px; vertical-align: middle; margin-right: 4px; border-radius: 2px; }
    .sw.truth { background: var(--ink-2); } .sw.fit { background: var(--accent); } .sw.train { background: var(--accent); height: 10px; width: 10px; border-radius: 50%; }
    .sw.test { background: var(--warn); height: 10px; width: 10px; border-radius: 50%; } .sw.like { background: var(--accent); } .sw.prior { background: var(--prof); } .sw.post { background: var(--supp); }
    .axis { stroke: var(--line); stroke-width: 1.5; }
    .tick { fill: var(--ink-2); font-size: 11px; }
    .plot-truth { fill: none; stroke: var(--ink-2); stroke-width: 1.5; stroke-dasharray: 5 4; }
    .plot-fit { fill: none; stroke: var(--accent); stroke-width: 2.5; }
    .pt-train { fill: var(--accent); }
    .pt-test { fill: var(--warn); }
    .plot-like { fill: none; stroke: var(--accent); stroke-width: 2; }
    .plot-prior { fill: none; stroke: var(--prof); stroke-width: 2; stroke-dasharray: 6 4; }
    .plot-post { fill: none; stroke: var(--supp); stroke-width: 3; }
    .mark-ml { stroke: var(--accent); stroke-width: 1.5; stroke-dasharray: 3 3; }
    .mark-map { stroke: var(--supp); stroke-width: 1.5; stroke-dasharray: 3 3; }
    .fig-ink { stroke: currentColor; fill: none; stroke-width: 2; }
    .fig-accent { stroke: var(--accent); fill: none; stroke-width: 2.5; }
    .fig-danger { stroke: var(--danger); fill: none; stroke-width: 2.5; }
    .fig-dot { fill: var(--accent); }
    .fig-text { fill: currentColor; font-size: 13px; font-family: inherit; }
    .fig-muted { fill: var(--ink-2); font-size: 12px; font-family: inherit; }
    footer { max-width: 920px; margin: 0 auto; padding: 24px 16px 48px; color: var(--ink-2); font-size: 13px; }
    @media (max-width: 480px) { .topic { padding: 14px; } .topbar strong { display: none; } }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <strong>🧸 머러기 정리노트</strong>
      <nav class="toc" aria-label="목차">
        <a href="#s0">0 오리엔테이션</a><a href="#s1">1 데이터·모델·러닝</a><a href="#s2">2 ERM</a>
        <a href="#s3">3 MLE·MAP</a><a href="#s4">4 확률적 추론</a><a href="#s5">5 요약·예고</a>
      </nav>
    </div>
  </header>
  <main>
    <div class="hero">
      <h1>When Models Meet Data — 5살도 이해하는 정리노트</h1>
      <p>정방철 교수님 머신러닝기초 · 0909 · 0914 · 0916 수업 (Lecture00~02, MML 8장)</p>
      <div class="legend-bar">
        <span class="badge">🧸 쉬운 비유</span><span class="badge">📐 정식 버전</span><span class="badge">🎙️ 교수님 한마디</span>
        <span class="badge">⚠️ 강조 포인트</span><span class="badge supp">📎 보충 · 수업 미유도</span>
      </div>
    </div>

    <section id="s0"><h2>0. 오리엔테이션</h2>
      <article class="topic" id="s0-course"><h3>과목 한눈에 보기</h3><div class="tags"><span class="tag date">📅 0902</span><span class="tag slide">L00</span></div></article>
    </section>

    <section id="s1"><h2>1. 데이터 · 모델 · 러닝</h2>
      <article class="topic" id="s1-components"><h3>머신러닝의 3요소: 데이터 · 모델 · 러닝</h3><div class="tags"><span class="tag date">📅 0909</span><span class="tag slide">L01 s5</span></div></article>
      <article class="topic" id="s1-induction"><h3>오늘의 메인 레슨: 머신러닝은 귀납이다</h3><div class="tags"><span class="tag date">📅 0909</span><span class="tag slide">L01 s5</span></div></article>
      <article class="topic" id="s1-data"><h3>데이터 = 벡터</h3><div class="tags"><span class="tag date">📅 0909</span><span class="tag slide">L01 s6</span></div></article>
      <article class="topic" id="s1-model"><h3>모델 = 수식 (정답은 없다)</h3><div class="tags"><span class="tag date">📅 0909 · 0914</span><span class="tag slide">L01 s5–7</span></div></article>
      <article class="topic" id="s1-prob-model"><h3>함수 모델 vs 확률 모델</h3><div class="tags"><span class="tag date">📅 0909</span><span class="tag slide">L01 s7</span></div></article>
      <article class="topic" id="s1-learning"><h3>러닝의 3단계와 하이퍼파라미터</h3><div class="tags"><span class="tag date">📅 0909 · 0914</span><span class="tag slide">L01 s8</span></div></article>
    </section>

    <section id="s2"><h2>2. Empirical Risk Minimization (모델 = 함수)</h2>
      <article class="topic" id="s2-erm"><h3>Empirical Risk Minimization이라는 이름</h3><div class="tags"><span class="tag date">📅 0914</span><span class="tag slide">L01 s10</span></div></article>
      <article class="topic" id="s2-affine"><h3>가장 중요한 수식: affine 모델과 augmentation</h3><div class="tags"><span class="tag date">📅 0914</span><span class="tag slide">L01 s10</span></div></article>
      <article class="topic" id="s2-matrix"><h3>데이터 행렬과 squared loss (김밥 말기)</h3><div class="tags"><span class="tag date">📅 0914</span><span class="tag slide">L01 s11</span></div></article>
      <article class="topic" id="s2-risk"><h3>진짜 목표: unseen data의 위험 (true risk)</h3><div class="tags"><span class="tag date">📅 0914</span><span class="tag slide">L01 s11</span></div></article>
      <article class="topic" id="s2-reg"><h3>Overfitting과 Regularization</h3><div class="tags"><span class="tag date">📅 0914</span><span class="tag slide">L01 s12</span></div></article>
    </section>

    <section id="s3"><h2>3. 확률 모델로 파라미터 추정: MLE · MAP</h2>
      <article class="topic" id="s3-likelihood"><h3>Likelihood = 그럴듯함, 그리고 −log</h3><div class="tags"><span class="tag date">📅 0914 · 0916</span><span class="tag slide">L01 s14</span></div></article>
      <article class="topic" id="s3-iid"><h3>i.i.d.: 같은 공장에서 찍어낸 데이터</h3><div class="tags"><span class="tag date">📅 0914 · 0916</span><span class="tag slide">L01 s15</span></div></article>
      <article class="topic" id="s3-mle-ls"><h3>가우시안 노이즈면 MLE = Least Squares</h3><div class="tags"><span class="tag date">📅 0914 · 0916</span><span class="tag slide">L01 s15</span></div></article>
      <article class="topic" id="s3-map"><h3>MAP: 데이터 + 선입견(prior)</h3><div class="tags"><span class="tag date">📅 0916</span><span class="tag slide">L01 s16</span></div></article>
      <article class="topic" id="s3-map-l2"><h3>📎 가우시안 prior = L2 정규화</h3><div class="tags"><span class="tag date">📅 0916</span><span class="tag slide">L01 s12 · s16</span></div></article>
      <article class="topic" id="s3-fitting"><h3>Model fitting: 과적합 · 과소적합 · 적정적합</h3><div class="tags"><span class="tag date">📅 0916</span><span class="tag slide">L01 s17</span></div></article>
    </section>

    <section id="s4"><h2>4. 확률적 모델링과 추론</h2>
      <article class="topic" id="s4-generative"><h3>Generative process: 데이터는 이렇게 만들어졌을 거야</h3><div class="tags"><span class="tag date">📅 0916</span><span class="tag slide">L02 s5</span></div></article>
      <article class="topic" id="s4-joint"><h3>Joint · Marginal · Latent</h3><div class="tags"><span class="tag date">📅 0916</span><span class="tag slide">L02 s5</span></div></article>
      <article class="topic" id="s4-posterior"><h3>Prior × Likelihood → Posterior</h3><div class="tags"><span class="tag date">📅 0916</span><span class="tag slide">L02 s5</span></div></article>
      <article class="topic" id="s4-three-ways"><h3>ML vs MAP vs Fully Bayesian</h3><div class="tags"><span class="tag date">📅 0916</span><span class="tag slide">L02 s6</span></div></article>
      <article class="topic" id="s4-coin"><h3>동전으로 보는 세 가지 답</h3><div class="tags"><span class="tag date">📅 0916</span><span class="tag slide">L02 s6</span></div></article>
      <article class="topic" id="s4-predictive"><h3>Posterior predictive와 조건부 독립</h3><div class="tags"><span class="tag date">📅 0916</span><span class="tag slide">L02 s6</span></div></article>
    </section>

    <section id="s5"><h2>5. 한 장 요약 · 다음 시간 예고</h2>
      <article class="topic" id="s5-cheatsheet"><h3>한 장 치트시트</h3></article>
      <article class="topic" id="s5-prereq"><h3>전제지식 지도 (MML Part I)</h3></article>
      <article class="topic" id="s5-next"><h3>다음 시간 예고 (아직 안 배움)</h3></article>
      <article class="topic" id="s5-links"><h3>함께 보면 좋은 자료</h3></article>
    </section>
  </main>
  <footer>출처: 정방철 교수님 강의자료(Lecture00–02) · 수업 녹음 전사(0909·0914·0916) · Deisenroth, Faisal, Ong, <i>Mathematics for Machine Learning</i> (2020) 8장.</footer>
  <script id="widget-math">
/* 여기에 scripts/widget_math.js 전체 내용을 그대로 붙여 넣는다 */
  </script>
</body>
</html>
```

- [ ] **Step 4: 복습문제 골격 작성** — `강의노트/복습문제_0909-0916_When_Models_Meet_Data.html`

`<head>`는 정리노트와 같다. `<title>`만 `머신러닝기초 복습문제`로, description만 `0909~0916 수업 범위 교과서(MML) 복습문제 10선`으로 바꾸고, `<style>` 블록은 **정리노트의 것을 그대로 복사**한 뒤 아래 CSS를 이어 붙인다.

```css
    .card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); padding: 20px; margin: 16px 0; }
    .card h3 { margin: 6px 0 10px; font-size: 18px; }
    .card-head { display: flex; flex-wrap: wrap; gap: 6px; }
    .badge.src { color: var(--accent); border-color: var(--accent); }
    .badge.level { color: var(--warn); border-color: var(--warn); }
    .problem { margin: 8px 0 12px; }
    details { border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; margin: 8px 0; background: var(--surface-2); }
    details > summary { cursor: pointer; font-weight: 700; }
    details[open] > summary { margin-bottom: 8px; }
    details.original { font-size: 14px; color: var(--ink-2); }
    .answer { font-weight: 700; background: var(--supp-soft); border-radius: 8px; padding: 8px 10px; }
    .link-back { font-size: 14px; color: var(--ink-2); }
    .done { display: inline-flex; gap: 6px; align-items: center; font-size: 14px; cursor: pointer; }
    .progress { position: sticky; top: 52px; z-index: 5; background: var(--surface); border: 1px solid var(--line); border-radius: 999px; padding: 6px 14px; display: inline-block; font-size: 14px; }
```

`<body>`:

```html
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <strong>📝 머러기 복습문제</strong>
      <nav class="toc" aria-label="목차">
        <a href="#partA">A 교과서 예제</a><a href="#partB">B 교과서 연습문제</a>
        <a href="정리노트_0909-0916_When_Models_Meet_Data.html">정리노트로 ↗</a>
      </nav>
    </div>
  </header>
  <main>
    <div class="hero">
      <h1>복습문제 10선 — 0909~0916 수업 범위</h1>
      <p>수업 범위인 MML 8장에는 연습문제가 없어서, <b>8장 본문 예제(Example 8.1~8.6)를 문제로 바꾼 5문항</b>과 <b>수업 내용으로 풀 수 있는 6·7장 연습문제 5문항</b>을 골랐습니다. 먼저 스스로 풀고, 막히면 💡 힌트, 그다음 ✅ 풀이를 여세요.</p>
      <p class="progress">풀었음 <b id="progress-count">0</b> / 10</p>
    </div>
    <section id="partA"><h2>A. 교과서 본문 예제 (MML 8장)</h2>
      <article class="card" id="p1"></article>
      <article class="card" id="p2"></article>
      <article class="card" id="p3"></article>
      <article class="card" id="p4"></article>
      <article class="card" id="p5"></article>
    </section>
    <section id="partB"><h2>B. 교과서 연습문제 (MML 6·7장)</h2>
      <article class="card" id="p6"></article>
      <article class="card" id="p7"></article>
      <article class="card" id="p8"></article>
      <article class="card" id="p9"></article>
      <article class="card" id="p10"></article>
    </section>
  </main>
  <footer>출처: Deisenroth, Faisal, Ong, <i>Mathematics for Machine Learning</i> (Cambridge University Press, 2020). 풀이는 자체 작성이며 <code>scripts/review_answers.py</code>로 수치를 검증했습니다.</footer>
  <script id="progress-ui">
    (function () {
      const KEY = 'mlb-review-0909-0916-done';
      let saved = {};
      try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { saved = {}; }
      const boxes = Array.from(document.querySelectorAll('input[data-done]'));
      const update = () => { document.getElementById('progress-count').textContent = String(boxes.filter((b) => b.checked).length); };
      boxes.forEach((b) => {
        b.checked = Boolean(saved[b.dataset.done]);
        b.addEventListener('change', () => {
          saved[b.dataset.done] = b.checked;
          try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) { /* 저장 불가 환경: 무시 */ }
          update();
        });
      });
      update();
    })();
  </script>
</body>
```

- [ ] **Step 5: 통과 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: 모두 PASS. `test_s5_links`는 SKIP이다. `COMPLETED_*`가 비어 있으므로 콘텐츠 테스트는 아무것도 검사하지 않고 통과한다.

- [ ] **Step 6: 커밋**

```bash
git add tests/test_notes_html.py "강의노트/정리노트_0909-0916_When_Models_Meet_Data.html" "강의노트/복습문제_0909-0916_When_Models_Meet_Data.html"
git commit -m "feat: scaffold study note and review HTML with contract tests"
```

---

## 콘텐츠 작성 공통 규칙 (Task 5~9)

**토픽 마크업 패턴:** 모든 s1~s4 토픽은 이 순서를 따른다. 태그 줄은 골격에 이미 있다.

```html
<article class="topic" id="…"><h3>…</h3><div class="tags">…</div>
  <div class="layer eli5"><span class="layer-title">🧸 쉽게 말하면</span><p class="lead">한 문장 비유</p> …그림(figure)… </div>
  <div class="layer formal"><span class="layer-title">📐 정식 버전</span> …정의·수식·단계별 유도(ol.steps)… </div>
  <div class="layer prof"><span class="layer-title">🎙️ 교수님 한마디</span> …일화·비유, 원문은 blockquote… </div>
  <div class="layer warn"><span class="layer-title">⚠️ 강조 포인트</span> …원문 인용 + (날짜 타임스탬프)… </div>   ← 원문 강조 발언이 있는 토픽만
  <div class="layer supp"><span class="badge supp">📎 보충 · 수업 미유도</span> … </div>             ← 명세에 표시된 토픽만
</article>
```

**문체:**
- 🧸 레이어는 초등학생이 이해할 수준의 1~3문장과 그림으로 쓴다.
- 📐 레이어는 빠짐없이, 정확하게 쓴다.
- 🎙️과 ⚠️의 인용은 요약 파일의 원문 인용을 쓰되 15단어 안팎으로 줄이고 `(0914 26:00)`처럼 출처를 붙인다.

**완성 예시(`s2-affine`, Task 6에서 이대로 쓴다):**

```html
<article class="topic" id="s2-affine"><h3>가장 중요한 수식: affine 모델과 augmentation</h3><div class="tags"><span class="tag date">📅 0914</span><span class="tag slide">L01 s10</span></div>
  <div class="layer eli5"><span class="layer-title">🧸 쉽게 말하면</span>
    <p class="lead">입력마다 "중요도(가중치)"를 곱해서 다 더하고, 마지막에 기본 점수(bias)를 더하는 계산기예요.</p>
    <p>기본 점수만 따로 떨어져 있는 게 귀찮으니, 입력 맨 앞에 숫자 <b>1</b>을 몰래 끼워 넣어요. 그러면 "1 × 기본 점수"가 되어 전부 한 번의 곱셈-덧셈(내적)으로 끝나요. 이걸 <b>augmentation</b>이라고 해요.</p>
    <figure class="figure"><svg id="fig-neuron" viewBox="0 0 520 200" role="img" aria-label="뉴런: 입력에 가중치를 곱해 더하고 activation을 통과">
      <circle cx="60" cy="40" r="16" class="fig-ink"/><text x="60" y="45" text-anchor="middle" class="fig-text">x₁</text>
      <circle cx="60" cy="100" r="16" class="fig-ink"/><text x="60" y="105" text-anchor="middle" class="fig-text">x₂</text>
      <circle cx="60" cy="160" r="16" class="fig-ink"/><text x="60" y="165" text-anchor="middle" class="fig-text">x_D</text>
      <line x1="76" y1="40" x2="224" y2="96" class="fig-ink"/><line x1="76" y1="100" x2="224" y2="100" class="fig-ink"/><line x1="76" y1="160" x2="224" y2="104" class="fig-ink"/>
      <text x="140" y="58" class="fig-muted">w₁</text><text x="140" y="94" class="fig-muted">w₂</text><text x="140" y="150" class="fig-muted">w_D</text>
      <circle cx="250" cy="100" r="26" class="fig-accent"/><text x="250" y="106" text-anchor="middle" class="fig-text">Σ + b</text>
      <line x1="276" y1="100" x2="340" y2="100" class="fig-ink"/>
      <rect x="340" y="76" width="70" height="48" rx="8" class="fig-accent"/><text x="375" y="105" text-anchor="middle" class="fig-text">σ(·)</text>
      <line x1="410" y1="100" x2="480" y2="100" class="fig-ink"/><text x="492" y="105" class="fig-text">ŷ</text>
      <text x="250" y="160" text-anchor="middle" class="fig-muted">affine (선형 + bias)</text><text x="375" y="160" text-anchor="middle" class="fig-muted">activation (비선형)</text>
    </svg><figcaption>뉴런 하나 = affine 함수 + activation. 딥러닝은 이걸 여러 층 쌓은 합성함수예요.</figcaption></figure>
  </div>
  <div class="layer formal"><span class="layer-title">📐 정식 버전</span>
    <p>원래 모델은 가중합에 bias를 더한 것이다: $f(\mathbf{x}_n, \boldsymbol{\theta}) = \theta_1 x_n^{(1)} + \dots + \theta_D x_n^{(D)} + \theta_0$.</p>
    <ol class="steps">
      <li>$\theta_0 = 1 \cdot \theta_0$ 이므로 데이터 맨 앞에 unit feature $x^{(0)} = 1$ 을 붙인다 (augmentation).</li>
      <li>$$\mathbf{x}_n = [1, x_n^{(1)}, \dots, x_n^{(D)}]^\top, \qquad \boldsymbol{\theta} = [\theta_0, \theta_1, \dots, \theta_D]^\top$$</li>
      <li>$$f(\mathbf{x}_n, \boldsymbol{\theta}) = \boldsymbol{\theta}^\top \mathbf{x}_n = \theta_0 + \sum_{d=1}^{D} \theta_d x_n^{(d)}$$ 누운 벡터 × 선 벡터 = 스칼라(내적).</li>
      <li>데이터와 무관한 상수 $\theta_0$ 때문에 $f(\mathbf{0}) = \theta_0$, 즉 원점을 지나지 않을 수 있다. 그래서 linear가 아니라 <b>affine</b> 함수라고 부른다.</li>
    </ol>
    <p>뉴런: $\hat{y} = \sigma\big(\sum_{i} w_i x_i + b\big)$. 여기서 $\sigma$ 는 sigmoid, ReLU 같은 activation function이다. DNN은 affine과 activation을 층층이 합성한 함수다.</p>
  </div>
  <div class="layer prof"><span class="layer-title">🎙️ 교수님 한마디</span>
    <p>"교수님, 왜 그렇게 하셨어요?" → "그냥 했어. 해본 거야." 괜찮으면 여기서 끝내고, 안 되면 뉴럴넷으로 간다. (0914 22:00 무렵)</p>
    <p>GPU가 딥러닝에 강한 이유: 결국 곱셈과 덧셈이라 코어 여러 개로 나눠 병렬 계산할 수 있어서다.</p>
  </div>
  <div class="layer warn"><span class="layer-title">⚠️ 강조 포인트</span>
    <blockquote>머신러닝에서 가장 중요한 컨셉이 뭐냐라고 묻는다면 저는 이 수식을 만드는 거라고 생각해요. (0914 26:00)</blockquote>
  </div>
</article>
```

**SVG 그림 규칙:**
- `viewBox`를 쓰고 `role="img"`와 한국어 `aria-label`을 단다.
- 색은 클래스(`fig-ink`, `fig-accent`, `fig-danger`, `fig-dot`, `fig-text`, `fig-muted`)로만 준다. 하드코딩한 색은 금지다.
- 글자 크기는 12~14px로 한다.
- SVG 안의 `<text>`에는 `$`를 쓰지 않는다. 유니코드(θ, σ, ₁)를 쓴다.
- 그림 목록은 각 태스크 명세에 있다.

---

### Task 5: 섹션 s0(오리엔테이션) + s1(데이터·모델·러닝)

**Files:**
- Modify: `강의노트/정리노트_0909-0916_When_Models_Meet_Data.html` (`#s0`, `#s1` 안의 article 채우기)
- Modify: `tests/test_notes_html.py` (`COMPLETED_SECTIONS`)

**Interfaces:**
- Consumes: 골격의 `#s0-course`, `#s1-*` article과 CSS 클래스 (Task 4)
- Produces: 그림 id `fig-pipeline`, `fig-induction`, `fig-data-vector`, `fig-det-vs-prob`, `fig-three-phases`

- [ ] **Step 1: 계약 활성화(RED)** — `tests/test_notes_html.py` 수정

```python
COMPLETED_SECTIONS: list[str] = ["s0", "s1"]
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: FAIL. `test_completed_required_terms`, `test_completed_layers`, `test_completed_figures`가 s0/s1 항목에서 실패한다.

- [ ] **Step 3: 콘텐츠 작성.** 원천은 `stt-0909-summary.md`, `stt-0914-summary.md` §1~3과 Lecture00 PDF다. 필수 용어는 `REQUIRED_TERMS`의 각 토픽 항목을 **그대로** 포함한다.

**`s0-course` (Lecture00, 레이어 불필요)**
- 강의 정보 표: 정방철 교수(원천관 406), TA 이영석, 월·수 12:00–13:15 원천관 539호, 교재(Géron *Hands-on ML* 3판, Deisenroth *MML*)
- 평가: 중간 35%, 기말 35%, 과제·퀴즈 20%, 출석 10%
- ML 정의: 손으로 규칙을 짜기 어려운 문제(사람·사물 인식, 음성 이해)를 선형대수·확률·수치최적화·통계로 **데이터에서 자동으로 배우는** 프로그램
- 세 종류: 지도학습(라벨이 있음), 비지도학습(라벨 없이 "흥미로운 패턴"을 찾음), 강화학습(agent가 환경과 상호작용하며 scalar reward를 최대화)
- AI ≈ DNN ≈ Deep Learning, Universal Approximation Theorem(신경망은 일반 함수 근사기라는 정리) 한 줄
- 학기 로드맵: When Models Meet Data → Linear·Logistic Regression → SVM·Ensemble·Clustering → PCA → GMM(EM)
- 전제 과목: 미적분·다변수미적분, 확률 및 랜덤변수, 머신러닝 수학, 선형대수. "기초가 탄탄하면 새 기술에 빨리 적응한다"는 메시지

**`s1-components` (0909 §1–2)**
- 🧸 요리 비유: 재료(데이터), 레시피(모델), 연습(러닝)
- 그림 `fig-pipeline`: 데이터 → 모델 → 러닝 → 예측(unseen)의 4상자 흐름
- 📐 3요소 정의(L01 s5):
  - 데이터 $\{(\mathbf{x}_1, y_1), \dots, (\mathbf{x}_N, y_N)\}$
  - 모델: deterministic function 또는 probabilistic model
  - 러닝: training과 prediction/inference
  - "좋은 모델 = unseen data에서 잘 동작하는 모델"
- 임계점 세 요인: 방대한 데이터, GPU·NPU, 최적화
- 🎙️ 교수님 수업을 여러 번 들은 학생 비유(데이터가 많으면 예측이 쉬움)
- ⚠️ "대부분의 문제는 데이터가 부족한 거예요" (0909 06:48)

**`s1-induction` (0909 §4 연역 vs 귀납, §8)**
- 🧸 탐정 비유: 발자국(데이터)을 보고 범인(규칙)을 추리하는 것이 귀납이다.
- 그림 `fig-induction`
  - 왼쪽은 "수식 → 데이터"(연역: 통신과 신호처리, `y(t) = x(t) * h(t)` + noise)
  - 오른쪽은 "파란 점 → 직선"(귀납: ML)
- 📐 연역과 귀납의 정의를 나란히 쓴다. 통신 예시는 수식 `$y(t) = x(t) * h(t) + n(t)$`를 쓴다.
- 🎙️ 로맨스 영화 마지막 장면 비유(표정 = 데이터, 마음 = 기작)
- 🎙️ "주어진 것은 파란 점이냐 검정 선이냐" 문답
- ⚠️ "오늘은 이게 진짜 메인 레슨이거든요… 귀납식" (0909 45:54)
- ⚠️ "머신러닝의 핵심은… 파란 점이 우리에게 주어졌다는 거예요" (0909 46:00)

**`s1-data` (0909 §3, §6)**
- 🧸 사진 한 장 → 아주 긴 숫자 줄 → 중요한 숫자만 남긴 짧은 줄
- 그림 `fig-data-vector`
- 📐 데이터셋 표기와 각 요소
  - 데이터셋: `$$\mathcal{D} = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \dots, (\mathbf{x}_N, y_N)\}$$`
  - 표기 관습: 볼드 소문자는 벡터, $y$는 스칼라. 괄호로 묶은 쌍은 짝꿍(세트)
  - 빅데이터: `$N \to \infty$`
  - 차원: `$\mathbf{x}_n \in \mathbb{R}^D$`, 각 성분을 feature(attribute, covariate)라고 부름
  - 개/고양이 예시: 사진은 픽셀×RGB 길이의 긴 실수 벡터, $y \in \{0,1\}$
- 📐 학습 방식과 feature 처리
  - supervised(라벨 있음) vs unsupervised(라벨 없음, clustering)
  - raw data와 feature vector의 차이. 이번 학기에는 feature vector를 "데이터"라고 부름
  - PCA: principal(주요한) + component + analysis. SVD, 고유값분해로 low-dimensional approximation을 만든다
  - feature map / kernel: 더 높은 차원의 비선형 조합
  - autoencoder(딥러닝의 feature extraction)
- 🎙️ 의학드라마 약어(convention) 비유
- 🎙️ MBTI = 사람을 16개로 clustering한 것

**`s1-model` (0909 §4, §9; 0914 §1)**
- 🧸 모델은 "데이터를 설명하는 이야기(수식)"이다. 더 잘 맞는 이야기는 있어도 "정답" 이야기는 없다.
- 📐 모델과 모델링
  - 모델 = 수식. deterministic($F = ma$, $y = ax + b$, 2차식…) vs probabilistic
  - 모델 셋업 예: `$y = 3x_1 + 5x_2 + 6x_3 + 0.6$` ("자신감 있게 질러야 된다")
  - 큰 모델은 작은 모델을 포함한다. 예: $ax^2 + bx + c$에서 $a = 0$
  - 모델 크기(파라미터 수)가 커지면 표현력도 커진다(유치원생 어휘 비유)
- 📐 suppose와 assume의 차이(0914 §1)
  - assume: 사실이 아닌 줄 알면서 가정
  - suppose: 모르니까 추측. 모델 선택은 suppose다
- 🎙️ 영화 추천(time-varying, "Nobody knows")
- 🎙️ 작은 GPU로 비슷한 성능을 내는 작은 모델이 더 좋은 엔진이라는 이야기(수치는 쓰지 않음)
- ⚠️ "모델이라는 말이 나오면… 수식이라고 생각해라" (0909 17:00)
- ⚠️ "가장 중요하게 생각해야 되는 게 모델링" (0909 19:18)
- ⚠️ "모델은 정답이 없어요" (0909 24:00)
- ⚠️ good/bad, 취사선택의 문제 (0909 28:10, 0914 01:24)

**`s1-prob-model` (0909 §4 동전, §11, §12)**
- 🧸 과녁에 활을 쏘면 딱 한 점이 아니라 가운데 근처에 흩어진다. 그 흩어짐까지 설명하는 게 확률 모델이다.
- 그림 `fig-det-vs-prob`
  - 위: 직선 위 x=60에서 점 하나(100)
  - 아래: x=60 위에 세운 종 모양 가우시안
- 📐 노이즈가 섞인 관측
  - noisy observation(논리회로 5.3V 예시)
  - 동전 5번 → 앞면 비율 0.6
  - 가우시안 $\mathcal{N}(\mu, \sigma^2)$는 실수 2개로 결정된다
- 📐 x=60 비교
  - 함수 모델: `x=60`이면 $\hat{y} = 100$
  - 확률 모델: `$$p(y \mid \mathbf{x}) = \mathcal{N}\big(y \mid f(\mathbf{x}), \sigma^2\big)$$`
- 📐 분포에서 답 하나를 고르는 기준: MLE, MAP, MMSE, Neyman–Pearson
  - MLE는 3절에서 정식으로 다룬다고 안내한다.
- 🎙️ 대령 일화: "숫자로 얘기해 주세요" → "그냥 100" = MLE의 직관 (0909 56:07)

**`s1-learning` (0909 §5, §13, §14; 0914 §2)**
- 🧸 요리대회 비유: 레시피 종류 고르기(model selection) → 간 맞추기(training) → 심사위원 앞에서 요리(prediction)
- 그림 `fig-three-phases`: 3단계 박스
- 📐 목표: unseen data에서 잘 동작하는 예측기를 찾는 것("such that"의 뜻)
- 📐 3단계(L01 s8)
  1. prediction / inference
  2. training / parameter estimation: ERM(비확률), ML·MAP(확률), cross-validation, regularization
  3. model selection: hyperparameter 선택
- 📐 parameter와 hyperparameter
  - parameter는 학습으로 얻는다(가중치, bias).
  - hyperparameter는 학습 전에 정한다(learning rate, 정규화 강도).
- 📐 learning과 training의 구분
  - learning은 모델 결정까지 포함한다.
  - training은 정해진 모델의 파라미터 튜닝이다.
  - 요즘은 모델을 바꾸는 것도 학습에 포함한다(0914 §2).
- 📐 파라미터 찾는 방법: grid search(돈과 시간이 많다면) vs gradient descent, least squares
- 🎙️ MBTI 4비트 → 6비트 = hyperparameter를 바꾸면 모델이 바뀐다
- 🎙️ "소 잡는 칼을 닭 잡는 데"
- ⚠️ "모델 선택이 매우 중요하다" (0909 66:00)

- [ ] **Step 4: 통과 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: 모두 PASS(`test_s5_links`는 SKIP)

- [ ] **Step 5: 커밋**

```bash
git add tests/test_notes_html.py "강의노트/정리노트_0909-0916_When_Models_Meet_Data.html"
git commit -m "feat(note): write orientation and data-model-learning sections"
```

---

### Task 6: 섹션 s2(ERM) + 위젯 1(과적합·정규화)

**Files:**
- Modify: `강의노트/정리노트_0909-0916_When_Models_Meet_Data.html` (`#s2`, 위젯 추가)
- Modify: `tests/test_notes_html.py` (`COMPLETED_SECTIONS`)

**Interfaces:**
- Consumes: 전역 함수 `makeDataset`, `ridgeFit`, `predictPoly`, `mse` (인라인 `widget-math`, Task 3·4)
- Produces:
  - 그림 id `fig-neuron`, `fig-matrix-packing`
  - 위젯 id `widget-reg`, `reg-degree`, `reg-degree-out`, `reg-lambda`, `reg-lambda-out`, `reg-plot`, `reg-train-mse`, `reg-test-mse`, 스크립트 `widget-reg-ui`

- [ ] **Step 1: 계약 활성화(RED)**

```python
COMPLETED_SECTIONS: list[str] = ["s0", "s1", "s2"]
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: FAIL. s2 토픽 용어, 레이어, 그림, 위젯 id

- [ ] **Step 3: 콘텐츠 작성.** 원천은 `stt-0914-summary.md` §3~12다.

**`s2-erm` (0914 §4–6)**
- 🧸 "실제로 해 봤더니(empirical) 틀린 정도(risk)가 가장 작게(minimization)"
- 📐 용어 해석(empirical = 실험적, risk = 부정적 metric, minimization)
- 📐 predictor는 deterministic 함수다. hat은 추정치(estimate)를 뜻한다.
- 📐 식: `$$\text{Find } \boldsymbol{\theta}^* \text{ such that } f(\mathbf{x}_n, \boldsymbol{\theta}^*) = \hat{y}_n \approx y_n, \ \forall n = 1, \dots, N$$`
- 📐 "for all"의 의미: $\mathbf{x}_1$ 하나에만 미친 듯이 맞추면 과적합이다. 모든 데이터에 두루 그럴듯해야 한다.
- 🎙️ "최적" 뒤에는 항상 "in terms of ★"가 붙는다. 인생 최적화, 수강신청 이메일 비유는 개념만 한 줄로.
- ⚠️ "어떤 관점에서 최적화를 하는지가 되게 중요" (0914 10:07)
- ⚠️ "머신러닝을 잘한다는 건 사실 최적화를 잘한다는 거" (0914 11:16)
- ⚠️ "for all… 하나도 버릴 단어가 없어" (0914 18:40)

**`s2-affine`:** 위 "완성 예시"를 그대로 쓴다.

**`s2-matrix` (0914 §9)**
- 🧸 김밥 비유: 재료(데이터 벡터)를 눕혀 차곡차곡 쌓으면(행렬) 한 번에 말 수 있다.
- 그림 `fig-matrix-packing`: 누운 벡터 $\mathbf{x}_1^\top, \dots, \mathbf{x}_N^\top$가 쌓여 $\mathbf{X}$가 되고, 옆에 $\mathbf{y}$
- 📐 데이터 행렬
  - `$$\mathbf{X} := [\mathbf{x}_1, \dots, \mathbf{x}_N]^\top \in \mathbb{R}^{N \times D}, \qquad \mathbf{y} := [y_1, \dots, y_N]^\top$$`
  - 각주: 교수님이 칠판에서 D×N으로 그렸다가 "트랜스포즈가 들어가 있네요"라며 전치를 정정함(0914 30:08). augmentation을 하면 열이 $D+1$개다.
- 📐 empirical risk(정의이며 평균은 선택이다. 학점 평점 비유)
  - `$$R_{\text{emp}}(f, \mathbf{X}, \mathbf{y}) = \frac{1}{N} \sum_{n=1}^{N} \ell(y_n, \hat{y}_n)$$`
- 📐 squared loss: `$$\ell(y_n, \hat{y}_n) = (y_n - \hat{y}_n)^2$$`
- 📐 합에서 노름까지 유도(ol.steps 5단계, 0914 §9 칠판 유도 그대로)
  - 최종식: `$$\min_{\boldsymbol{\theta}} \frac{1}{N} \|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$$`
  - $\mathbf{X}\boldsymbol{\theta} = \hat{\mathbf{y}} \in \mathbb{R}^{N \times 1}$
- ⚠️ "이거는 해보세요. 산수니까" (0914 37:24)
- ⚠️ "잊지 말아야 될 건 θ를… 변화시키고 싶은 거" (0914 38:22)

**`s2-risk` (0914 §10–11)**
- 🧸 시험공부는 기출(train)로 하지만, 점수는 처음 보는 문제(test)로 매긴다.
- 📐 θ 찾기: 무식하게 다 바꿔 보기 vs 선형대수(least squares, pseudo-inverse는 다음 주)
- 📐 true(expected) risk: `$$R_{\text{true}}(f) = \mathbb{E}_{\mathbf{x}, y}\big[\ell(y, f(\mathbf{x}))\big]$$`
  - 가정: 새 데이터는 본 데이터와 크게 다르지 않다("해 아래 새 것이 없다")
- 📐 분할
  - train/test = `7:3`
  - train/validation/test = 60/20/20
  - "정답은 없는 거야", 장인의 손맛
- 🎙️ 바둑 AI는 기보(판을 벡터로 만든 것)를 학습했다. 이창호 9단의 영상이 아니다.

**`s2-reg` (0914 §12)**
- 🧸 시험 문제의 답만 통째로 외운 학생(overfitting)에게 "너무 튀는 답은 벌점"(penalty)을 주는 것
- 📐 overfitting: fit too closely, 일반화 실패
- 📐 regularized least squares
  - `$$\min_{\boldsymbol{\theta}} \frac{1}{N} \|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 + \lambda \|\boldsymbol{\theta}\|^2$$`
  - regularizer $\|\boldsymbol{\theta}\|^2$, regularization parameter $\lambda$ = hyperparameter
  - 모델 자체(affine)는 바뀌지 않는다.
  - λ의 효과: $\lambda = 0$이면 과적합되기 좋고, λ가 커지면 원점 쪽으로 끌린다.
- 📐 노름
  - `$\|\boldsymbol{\theta}\|_2^2 = \sum_d \theta_d^2$`
  - `$\|\boldsymbol{\theta}\|_1 = \sum_d |\theta_d|$` (sparse solution, 0을 만드는 습성)
  - `$\|\boldsymbol{\theta}\|_p = \big(\sum_d |\theta_d|^p\big)^{1/p}$`
- 📐 하이퍼파라미터 최적화: Gaussian Process 기반 Bayesian Optimization(이름만)
- 🎙️ penalty = "모름지기 θ란 이래야 해"라는 expert knowledge
- 🎙️ λ = 0.7이냐 0.9냐는 장인의 손맛(김밥 우엉 취향 비유)

**위젯 1:** `s2-reg` article **다음**(`#s2` 섹션 안)에 삽입한다.

```html
<div class="widget" id="widget-reg">
  <h4>🎛️ 직접 해보기: 차수와 λ로 과적합 조절하기</h4>
  <p class="widget-help">파란 점(학습 데이터)만 보고 다항식 곡선을 맞춥니다. 주황 점은 한 번도 못 본 <b>unseen data</b>예요. 차수 9, λ=0(과적합)에서 시작합니다. λ를 올리거나 차수를 낮춰 테스트 MSE가 어떻게 변하는지 보세요.</p>
  <div class="controls">
    <label>다항 차수 <input type="range" id="reg-degree" min="1" max="9" step="1" value="9"> <output id="reg-degree-out">9</output></label>
    <label>λ <input type="range" id="reg-lambda" min="0" max="7" step="1" value="0"> <output id="reg-lambda-out">0</output></label>
  </div>
  <svg id="reg-plot" viewBox="0 0 560 300" role="img" aria-label="다항 회귀 적합 곡선과 학습·테스트 점"></svg>
  <div class="readout">학습 MSE <b id="reg-train-mse">–</b> · 테스트(unseen) MSE <b id="reg-test-mse">–</b></div>
  <p class="legend"><span><span class="sw truth"></span>진짜 함수 sin(πx)</span><span><span class="sw fit"></span>학습된 곡선</span><span><span class="sw train"></span>학습 점</span><span><span class="sw test"></span>unseen 점</span></p>
  <p class="widget-help">해볼 것: ① 차수 9, λ=0 → 학습 MSE≈0인데 테스트 MSE 0.712 (과적합) ② 차수 3, λ=0.001 → 테스트 0.109 (적정) ③ 차수 1, λ=0 → 테스트 0.417 (과소적합) ④ 차수 9, λ=10 → 너무 강한 벌점도 과소적합</p>
</div>
```

`</body>` 바로 앞, `widget-math` **다음**에 추가한다.

```html
<script id="widget-reg-ui">
(function () {
  const el = (id) => document.getElementById(id);
  const LAMBDAS = [0, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10];
  const W = 560, H = 300, P = 24;
  const sx = (x) => P + ((x + 1) / 2) * (W - 2 * P);
  const sy = (y) => H / 2 - (y * (H / 2 - P)) / 2;
  const clamp = (y) => Math.max(-2.2, Math.min(2.2, y));
  const path = (pts) => pts.map((p, i) => (i ? 'L' : 'M') + sx(p[0]).toFixed(1) + ' ' + sy(p[1]).toFixed(1)).join(' ');
  const data = makeDataset(7);
  const grid = Array.from({ length: 201 }, (_, i) => -1 + i / 100);
  function draw() {
    const deg = Number(el('reg-degree').value);
    const lam = LAMBDAS[Number(el('reg-lambda').value)];
    el('reg-degree-out').textContent = String(deg);
    el('reg-lambda-out').textContent = String(lam);
    const theta = ridgeFit(data.trainX, data.trainY, deg, lam);
    const axes = '<line class="axis" x1="' + P + '" y1="' + sy(0) + '" x2="' + (W - P) + '" y2="' + sy(0) + '"/>'
      + '<line class="axis" x1="' + sx(0) + '" y1="' + P / 2 + '" x2="' + sx(0) + '" y2="' + (H - P / 2) + '"/>';
    const truth = '<path class="plot-truth" d="' + path(grid.map((x) => [x, data.truth(x)])) + '"/>';
    const fit = '<path class="plot-fit" d="' + path(grid.map((x) => [x, clamp(predictPoly(theta, x))])) + '"/>';
    const dots = (xs, ys, cls) => xs.map((x, i) => '<circle class="' + cls + '" r="5" cx="' + sx(x).toFixed(1) + '" cy="' + sy(ys[i]).toFixed(1) + '"/>').join('');
    el('reg-plot').innerHTML = axes + truth + fit + dots(data.trainX, data.trainY, 'pt-train') + dots(data.testX, data.testY, 'pt-test');
    el('reg-train-mse').textContent = mse(theta, data.trainX, data.trainY).toFixed(3);
    el('reg-test-mse').textContent = mse(theta, data.testX, data.testY).toFixed(3);
  }
  el('reg-degree').addEventListener('input', draw);
  el('reg-lambda').addEventListener('input', draw);
  draw();
})();
</script>
```

- [ ] **Step 4: 통과 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add tests/test_notes_html.py "강의노트/정리노트_0909-0916_When_Models_Meet_Data.html"
git commit -m "feat(note): write ERM section with regularization widget"
```

---

### Task 7: 섹션 s3(MLE · MAP · Model fitting)

**Files:**
- Modify: `강의노트/정리노트_0909-0916_When_Models_Meet_Data.html` (`#s3`)
- Modify: `tests/test_notes_html.py` (`COMPLETED_SECTIONS`)

**Interfaces:**
- Consumes: 골격의 `#s3-*` article (Task 4)
- Produces: 그림 id `fig-log`, `fig-factory`, `fig-prior-likelihood-posterior`, `fig-model-class`, `fig-fitting-3`

- [ ] **Step 1: 계약 활성화(RED)**

```python
COMPLETED_SECTIONS: list[str] = ["s0", "s1", "s2", "s3"]
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: FAIL. s3 항목

- [ ] **Step 3: 콘텐츠 작성.** 원천은 `stt-0914-summary.md` §14~17, `stt-0916-summary.md` §1~9, §14다.

**`s3-likelihood` (0914 §14; 0916 §1, §3, §4)**
- 🧸 "이 동전이면 이런 결과가 나올 법하네?"의 정도가 likelihood다.
- 그림 `fig-log`: $\log t$ 곡선. 0~1 구간을 크게 벌려 보여 주는 "클로즈업"
- 📐 likelihood의 뜻과 정의
  - 어원: likely(~할 것 같은) + -hood(명사) = 그럴듯함
  - likelihood는 θ의 함수이며 θ의 PDF가 아니다.
  - 정의: `$$\mathcal{L}(\boldsymbol{\theta}) = -\log p(\mathbf{x} \mid \boldsymbol{\theta})$$` (negative log-likelihood)
  - MLE: $\mathcal{L}$을 최소화하는 θ
- 📐 log를 쓰는 이유 세 가지
  1. 단조증가라서 argmax가 보존된다.
  2. 가우시안의 exp를 없앤다.
  3. 아주 작은 확률 차이를 확대한다(클로즈업).
  - 덧붙임: PDF 값 자체는 1보다 클 수 있다(적분만 1).
- 📐 latent parameter θ와 확률 모형을 "정의(define)"한다는 것
  - 예: 지수분포 `$f(x) = \lambda e^{-\lambda x}$` ($x \ge 0$)
  - 예: 가우시안에서 $\theta_1 = \mu$, $\theta_2 = \sigma^2$
- 🎙️ "그럴듯하다"라는 우리말이 likelihood와 딱 맞는다.
- 🎙️ 디지털통신의 MLD도 같은 통계 용어다.
- ⚠️ "묻지도 말고 따지지도 말고 -log를 쳐" (0916 07:02)
- ⚠️ "외워도 돼요" (0916 08:59)
- ⚠️ "그 어떤 머신러닝 문제가 있어도… 항상 여기까지는 그냥 쓰는 거예요" (0916 12:18)

**`s3-iid` (0914 §15 1–2단계; 0916 §2, §5)**
- 🧸 같은 공장, 같은 기계에서 하나씩 따로 찍어낸 과자들
- 그림 `fig-factory`: 공장 하나(θ) → 과자 $y_1, \dots, y_N$
- 📐 i.i.d.(independent and identically distributed)의 정의
- 📐 칠판 유도 3단계(ol.steps)
  1. independent → 곱
  2. identical → θ 하나
  3. log → 합
  - 최종: `$$\mathcal{L}(\boldsymbol{\theta}) = -\log p(\mathcal{Y} \mid \mathcal{X}, \boldsymbol{\theta}) = -\log \prod_{n=1}^{N} p(y_n \mid \mathbf{x}_n, \boldsymbol{\theta}) = -\sum_{n=1}^{N} \log p(y_n \mid \mathbf{x}_n, \boldsymbol{\theta})$$`
- 📐 데이터마다 PDF가 다르면 PDF 하나당 데이터가 1개뿐이라 추정이 말이 안 된다.
- 🎙️ 추석 선물 세트: 벡터들을 모아 세트 $\mathcal{X}$로 만든다.
- 🎙️ "동일한 공장에서 동일한 불확실성을 갖고 찍어낸" (0916 14:45)

**`s3-mle-ls` (0914 §15–16; 0916 §6)**
- 🧸 "오차가 종 모양(가우시안)으로 생겼다"고 믿으면, 가장 그럴듯한 선은 오차 제곱합이 가장 작은 선과 같아진다.
- 📐 모델: `$$y_n = \mathbf{x}_n^\top \boldsymbol{\theta} + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, \sigma^2)$$`
  - 따라서 $y_n \mid \mathbf{x}_n, \boldsymbol{\theta} \sim \mathcal{N}(\mathbf{x}_n^\top \boldsymbol{\theta}, \sigma^2)$ (상수 + 가우시안이면 평균만 이동)
- 📐 A항/B항 분리 유도(0916 §6)
  - 결과: `$$\mathcal{L}(\boldsymbol{\theta}) = \frac{N}{2}\log(2\pi\sigma^2) + \frac{1}{2\sigma^2} \sum_{n=1}^{N} (y_n - \mathbf{x}_n^\top \boldsymbol{\theta})^2$$`
  - 첫째 항은 θ와 무관하다.
  - 둘째 항은 $\frac{1}{2\sigma^2}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$이다.
  - 따라서 MLE = least squares(s2-matrix로 링크)
- 📐 노이즈가 비대칭(Laplace, exponential)이면 다른 loss가 나온다(이름만).
- 📐 확률 모델이 "대세"인 이유: 상수는 delta PDF를 가진 확률변수다. 그래서 확률 모델이 deterministic 모델을 포함한다.
- 🎙️ "데이터가 애초에 저 식에서 만들어졌나요?" → "꼭 그렇지 않아", pretty well explained면 된다.
- 🎙️ 넷플릭스 추천, "쥐만 잘 잡으면 돼"(흑묘백묘)
- ⚠️ "발음을 촌스럽게 suppose 자꾸 강조하잖아요… 여기서 가정이 필요하다니까" (0914 66:25)

**`s3-map` (0914 §17; 0916 §7)**
- 🧸 데이터만 믿지 않고 "원래 이럴 거야"라는 선입견(prior)을 섞어서 판단한다.
- 그림 `fig-prior-likelihood-posterior`: prior(점선), likelihood(파랑), posterior(초록, 둘 사이) 곡선
- 📐 posterior = 사건(관측) 이후의 분포. 조건부 확률이다.
- 📐 Bayes 유도(ol.steps)
  1. `$p(A \mid B) = \frac{p(A, B)}{p(B)}$`
  2. `$$p(\boldsymbol{\theta} \mid \mathbf{x}) = \frac{p(\mathbf{x}, \boldsymbol{\theta})}{p(\mathbf{x})} = \frac{p(\mathbf{x} \mid \boldsymbol{\theta})\, p(\boldsymbol{\theta})}{p(\mathbf{x})}$$`
  3. 분모는 θ와 무관 → `$p(\boldsymbol{\theta} \mid \mathbf{x}) \propto p(\mathbf{x} \mid \boldsymbol{\theta})\, p(\boldsymbol{\theta})$`
  4. max vs argmax: max는 최대 확률값, argmax는 그 값을 주는 θ
  5. `$$\boldsymbol{\theta}_{\text{MAP}} = \arg\max_{\boldsymbol{\theta}} p(\boldsymbol{\theta} \mid \mathbf{x}) = \arg\min_{\boldsymbol{\theta}} \big[-\log p(\mathbf{x} \mid \boldsymbol{\theta}) - \log p(\boldsymbol{\theta})\big]$$`
     - 앞 항은 MLE 항, 뒤 항은 prior 항
  6. prior가 uniform(상수)이면 MAP = ML
- 🎙️ "손에 쥔 게 데이터예요, θ예요?"
- 🎙️ 의사의 CT 판독 비유(데이터 → 원인 추론)
- ⚠️ "보통의 inference problem을 수학으로 옮기면 항상 이 수식을 기억해야 돼" (0916 23:41)

**`s3-map-l2` (0916 §14 [보충]; supp 레이어 필수)**
- 🧸 "θ는 작을 거야"라는 믿음(가우시안 prior)을 넣으면, 벌점 $\lambda\|\boldsymbol{\theta}\|^2$을 준 것과 똑같아진다.
- 📐 prior와 정규화의 연결
  - prior는 편견·선호("모름지기 θ는…")이고, regularization 항과 연결된다. s2-reg로 링크한다.
  - 교수님은 "나중에 다시 썰 푸는 걸로"라며 수식 유도를 미뤘다(0916 55:32).
- 📎 supp 레이어 내용
  - prior: `$$p(\boldsymbol{\theta}) = \mathcal{N}(\mathbf{0}, b^2 \mathbf{I}) \ \Rightarrow\ -\log p(\boldsymbol{\theta}) = \frac{1}{2b^2}\|\boldsymbol{\theta}\|^2 + \text{const}$$`
  - MAP 목적함수: `$$\frac{1}{2\sigma^2}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 + \frac{1}{2b^2}\|\boldsymbol{\theta}\|^2$$`
  - $\frac{2\sigma^2}{N}$를 곱하면 `$$\lambda = \frac{\sigma^2}{N b^2}$$`
  - 해석: 믿음이 강할수록($b$가 작을수록) λ가 커진다.
  - MML 8.3.2, 9.2.3 참고. 복습문제 P5와 연결
- 🎙️ λ = 0이면 "선험적인 편견 따위는 고려하지 않겠다"

**`s3-fitting` (0916 §8–9)**
- 🧸 옷 맞추기: 너무 딱 붙으면 움직일 때 찢어지고(과적합), 너무 헐렁하면 안 맞는다(과소적합).
- 그림 `fig-model-class`
  - 큰 원 = 모델 클래스(예: linear)
  - 안쪽 점: $M_{\boldsymbol{\theta}_0}$ → $M_{\boldsymbol{\theta}^*}$ 화살표
  - 원 밖 별: $M^*$
  - 빨간 점선: $M_{\boldsymbol{\theta}^*}$와 $M^*$ 사이
- 그림 `fig-fitting-3`: 아래 SVG를 그대로 쓴다.
- 📐 model fitting vs parameter fitting: 모델 자체를 바꾸는 것 vs 파라미터 튜닝
- 📐 $M^*$(요정만 아는 진짜 모델), $M_{\boldsymbol{\theta}}$(가정한 클래스), $M_{\boldsymbol{\theta}^*}$(클래스 안의 최선)
  - 빨간 거리가 클수록 나쁜 모델이다.
- 📐 overfitting
  - 데이터 수에 비해 복잡한 모델. 예: 입력 −2에서 −100을 예측
  - 요즘 더 흔하다.
  - 모델 크기 = 최적화할 파라미터 개수
- 📐 underfitting: 너무 단순. 내 데이터조차 설명 못 하지만 안정적이다.
- 📐 good fitting: 컴퓨팅 자원, 문제 크기, 데이터 수를 모두 고려한다.
- 🎙️ 요정·지니 비유
- 🎙️ 학습 데이터로 테스트하는 논문 실수 = "되새김질… 당연히 소화가 잘 되겠지"
- ⚠️ "이렇게 하면 안 돼" (0916 33:45)

`fig-fitting-3` SVG(그대로 사용):

```html
<figure class="figure"><svg id="fig-fitting-3" viewBox="0 0 600 190" role="img" aria-label="과소적합, 적정적합, 과적합 세 그림">
  <g transform="translate(10,10)">
    <rect x="0" y="0" width="180" height="140" rx="10" class="fig-ink" stroke-opacity=".25"/>
    <circle cx="25" cy="110" r="4" class="fig-dot"/><circle cx="55" cy="70" r="4" class="fig-dot"/><circle cx="85" cy="45" r="4" class="fig-dot"/><circle cx="115" cy="50" r="4" class="fig-dot"/><circle cx="145" cy="85" r="4" class="fig-dot"/><circle cx="165" cy="115" r="4" class="fig-dot"/>
    <line x1="15" y1="85" x2="170" y2="80" class="fig-danger"/>
    <text x="90" y="165" text-anchor="middle" class="fig-text">과소적합 (너무 단순)</text>
  </g>
  <g transform="translate(210,10)">
    <rect x="0" y="0" width="180" height="140" rx="10" class="fig-ink" stroke-opacity=".25"/>
    <circle cx="25" cy="110" r="4" class="fig-dot"/><circle cx="55" cy="70" r="4" class="fig-dot"/><circle cx="85" cy="45" r="4" class="fig-dot"/><circle cx="115" cy="50" r="4" class="fig-dot"/><circle cx="145" cy="85" r="4" class="fig-dot"/><circle cx="165" cy="115" r="4" class="fig-dot"/>
    <path d="M15 120 Q 95 -10 172 122" class="fig-accent"/>
    <text x="90" y="165" text-anchor="middle" class="fig-text">적정적합 (good fitting)</text>
  </g>
  <g transform="translate(410,10)">
    <rect x="0" y="0" width="180" height="140" rx="10" class="fig-ink" stroke-opacity=".25"/>
    <circle cx="25" cy="110" r="4" class="fig-dot"/><circle cx="55" cy="70" r="4" class="fig-dot"/><circle cx="85" cy="45" r="4" class="fig-dot"/><circle cx="115" cy="50" r="4" class="fig-dot"/><circle cx="145" cy="85" r="4" class="fig-dot"/><circle cx="165" cy="115" r="4" class="fig-dot"/>
    <path d="M10 135 L25 110 C35 60 45 125 55 70 C65 15 75 70 85 45 C95 20 105 90 115 50 C125 10 135 130 145 85 C152 55 158 140 165 115 L172 20" class="fig-danger"/>
    <text x="90" y="165" text-anchor="middle" class="fig-text">과적합 (점만 외움)</text>
  </g>
</svg><figcaption>같은 데이터, 세 가지 모델. 과적합은 학습 점을 전부 지나지만 그 사이에서 크게 요동친다.</figcaption></figure>
```

- [ ] **Step 4: 통과 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add tests/test_notes_html.py "강의노트/정리노트_0909-0916_When_Models_Meet_Data.html"
git commit -m "feat(note): write MLE, MAP and model fitting section"
```

---

### Task 8: 섹션 s4(확률적 모델링과 추론) + 위젯 2(동전)

**Files:**
- Modify: `강의노트/정리노트_0909-0916_When_Models_Meet_Data.html` (`#s4`, 위젯 추가)
- Modify: `tests/test_notes_html.py` (`COMPLETED_SECTIONS`)

**Interfaces:**
- Consumes: 전역 함수 `betaPdf`, `coinEstimates` (인라인 `widget-math`)
- Produces:
  - 그림 id `fig-general`
  - 위젯 id `widget-coin`, `coin-n`, `coin-n-out`, `coin-k`, `coin-k-out`, `coin-a`, `coin-a-out`, `coin-plot`, `coin-ml`, `coin-map`, `coin-pred`, 스크립트 `widget-coin-ui`

- [ ] **Step 1: 계약 활성화(RED)**

```python
COMPLETED_SECTIONS: list[str] = ["s0", "s1", "s2", "s3", "s4"]
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: FAIL. s4 항목

- [ ] **Step 3: 콘텐츠 작성.** 원천은 `stt-0916-summary.md` §10~18이다.

**`s4-generative` (0916 §11–12)**
- 🧸 케이크(데이터)를 보고 "이 레시피(생성 과정)로 만들었을 거야"라고 추측하는 것
- 📐 ML의 목적은 unseen event의 prediction과 decision making이다.
- 📐 generative process를 suppose한다: $y_n = \mathbf{x}_n^\top \boldsymbol{\theta} + \varepsilon$
- 📐 칠판 설명
  - `$c_n = \mathbf{x}_n^\top \boldsymbol{\theta}$`는 상수다.
  - 따라서 $y_n = c_n + \varepsilon \Rightarrow y_n \sim \mathcal{N}(c_n, \sigma^2)$
  - θ는 평균을 바꾸는 방식으로 데이터에 영향을 준다. 복습문제 P9와 연결
- 🎙️ 신승훈 가사 "~했을 거야" 톤으로 설명한 generative process
- 🎙️ 에어컨 소리 = 노이즈, "마가 낀 게 아니고 노이즈가 꼈을 거다"

**`s4-joint` (0916 §12–13)**
- 🧸 두 사람 각각의 키 기록(marginal)보다, 둘이 함께 찍힌 사진(joint)에 정보가 더 많다.
- 📐 joint·marginal과 θ
  - PDF/PMF를 알면 평균, 분산, 기댓값 등 모든 것을 안다.
  - 변수가 둘이면 joint를 알아야 전부 안다. 각자의 것은 marginal이다.
  - 주변화: $p(\mathbf{x}) = \int p(\mathbf{x}, \boldsymbol{\theta})\, d\boldsymbol{\theta}$ (이산이면 합)
  - θ는 확률론에서는 hidden parameter, ML에서는 latent variable이라고 부른다.
- 🎙️ 인셉션 비유(겉의 현상 x, 꿈속 코어 θ)
- ⚠️ "확률 랜덤 변수 수업이 이만큼 중요한 거야" (0916 45:11)
  - 확률 및 랜덤변수 추가강의 링크: `추가%20강의/eli5_lecture10_statistical_inference_part1.html`
- ⚠️ θ가 원래 key information을 담는 게 아니다. 담도록 **만들어 가는** 것이다. "그런 생각은 없애야 된다니까" (0916 51:00) — 귀납의 관점

**`s4-posterior` (0916 §14–15)**
- 🧸 "원래 믿음(prior)" × "데이터가 말해 주는 것(likelihood)" = "업데이트된 믿음(posterior)"
- 📐 joint의 분해
  - `$$p(\mathbf{x}, \boldsymbol{\theta}) = p(\mathbf{x} \mid \boldsymbol{\theta})\, p(\boldsymbol{\theta})$$`
  - prior는 관찰 전의 편견·선호·의도("모름지기 파라미터는…")
  - likelihood는 forward(transition) probability
- 📐 prior와 정규화의 연결: λ = 0이면 편견 없음, λ가 크면 "θ는 작을수록 좋다". s3-map-l2로 링크
- 📐 posterior와 marginal likelihood
  - `$$p(\boldsymbol{\theta} \mid \mathbf{x}) = \frac{p(\mathbf{x}, \boldsymbol{\theta})}{p(\mathbf{x})} = \frac{p(\mathbf{x}, \boldsymbol{\theta})}{\int p(\mathbf{x}, \boldsymbol{\theta})\, d\boldsymbol{\theta}}$$`
  - 분모 $p(\mathbf{x})$ = marginal likelihood
- 🎙️ 분자와 분모가 모두 joint라서, 함수 하나만 계산하면 된다 = "엔지니어링적으로 효과적"
- ⚠️ "항상 이 확률 수식을 기억해야 되거든요" (0916 56:22)

**`s4-three-ways` (0916 §16–17)**
- 🧸 장군님은 "그래서 앞이야 뒤야?"라며 단답을 원하고(ML/MAP), 엔지니어는 분포 전체를 보고한다(Fully Bayesian).
- 그림 `fig-general`
  - 왼쪽: 말풍선 "앞? 뒤?" → 점 하나
  - 오른쪽: 분포 곡선 전체
- 📐 예측 문제 $P(A \mid \mathbf{X})$ (unseen data 분류: 개/고양이, 재밍 유무)
- 📐 세 가지 답
  - `$$\text{ML: } P(A \mid \mathbf{X}) \approx P(A \mid \boldsymbol{\theta}_{\text{ML}}), \quad \boldsymbol{\theta}_{\text{ML}} = \arg\max_{\boldsymbol{\theta}} P(\mathbf{X} \mid \boldsymbol{\theta})$$`
  - `$$\text{MAP: } P(A \mid \mathbf{X}) \approx P(A \mid \boldsymbol{\theta}_{\text{MAP}}), \quad \boldsymbol{\theta}_{\text{MAP}} = \arg\max_{\boldsymbol{\theta}} P(\boldsymbol{\theta} \mid \mathbf{X})$$`
  - Fully Bayesian: 분포 전체를 사용한다(s4-predictive). 성능은 Fully Bayesian이 가장 좋다.
- 🎙️ 장군님 비유(0909 대령 일화와 연결)

**`s4-coin` (0916 §17 + [보충]; supp 레이어 필수)**
- 🧸 10번 던져 앞면 2번. "데이터만 믿는 사람" 0.2, "반반이라 믿는 사람" 0.5, "섞는 사람" 약 0.3
- 📐 Fully Bayesian: 앞 0.5, 뒤 0.5라는 PMF 자체를 보고한다(한 학생의 답).
- 📐 ML
  - 앞면 확률 θ = 0.2. binomial 분포의 peak가 관측과 맞는 θ다.
  - 교수님: "미분해 보면 나오거든요" → 보충으로 유도
- 📐 MAP: "동전이면 반반" prior를 섞어 0.3 정도
- 📎 supp 레이어 내용
  - ML: `$\ell(\theta) = \log\binom{10}{2} + 2\log\theta + 8\log(1-\theta)$`
    - `$$\frac{2}{\theta} - \frac{8}{1-\theta} = 0 \ \Rightarrow\ \theta_{\text{ML}} = 0.2$$`
  - MAP: prior Beta(4, 4)이면 사후분포는 Beta(6, 12)
    - `$$\theta_{\text{MAP}} = \frac{k + \alpha - 1}{N + \alpha + \beta - 2} = \frac{5}{16} = 0.3125$$`
  - 복습문제 P8, P10과 연결
- 🎙️ 머니볼(데이터 사이언티스트)
- 🎙️ 야구 코치("어제 술 먹은 거다") vs 데이터 사이언티스트("이미 꺾였다") → "온전한 솔루션은 항상 그 사이에 있다" = MAP의 직관

**위젯 2:** `s4-coin` article 다음에 삽입한다.

```html
<div class="widget" id="widget-coin">
  <h4>🪙 직접 해보기: 동전 ML vs MAP vs 사후분포</h4>
  <p class="widget-help">N번 던져 앞면이 k번 나왔어요. prior 강도 a는 "모름지기 동전은 반반"이라는 믿음의 세기예요(Beta(a, a)). a=1이면 아무 믿음 없는 uniform prior라서 MAP가 ML과 같아져요.</p>
  <div class="controls">
    <label>던진 횟수 N <input type="range" id="coin-n" min="1" max="50" step="1" value="10"> <output id="coin-n-out">10</output></label>
    <label>앞면 수 k <input type="range" id="coin-k" min="0" max="10" step="1" value="2"> <output id="coin-k-out">2</output></label>
    <label>prior 강도 a <input type="range" id="coin-a" min="1" max="20" step="1" value="4"> <output id="coin-a-out">4</output></label>
  </div>
  <svg id="coin-plot" viewBox="0 0 560 260" role="img" aria-label="likelihood, prior, posterior 곡선과 ML·MAP 위치"></svg>
  <div class="readout">θ<sub>ML</sub> = <b id="coin-ml">–</b> · θ<sub>MAP</sub> = <b id="coin-map">–</b> · 다음에 앞면 나올 확률(Fully Bayesian) = <b id="coin-pred">–</b></div>
  <p class="legend"><span><span class="sw like"></span>likelihood(정규화)</span><span><span class="sw prior"></span>prior Beta(a, a)</span><span><span class="sw post"></span>posterior</span></p>
</div>
```

`widget-reg-ui` 다음에 추가한다.

```html
<script id="widget-coin-ui">
(function () {
  const el = (id) => document.getElementById(id);
  const W = 560, H = 260, P = 24;
  const sx = (t) => P + t * (W - 2 * P);
  const grid = Array.from({ length: 199 }, (_, i) => (i + 1) / 200);
  const fmt = (v) => String(Number(v.toFixed(4)));
  function draw() {
    const N = Number(el('coin-n').value);
    const kEl = el('coin-k');
    kEl.max = String(N);
    if (Number(kEl.value) > N) kEl.value = String(N);
    const k = Number(kEl.value);
    const a = Number(el('coin-a').value);
    el('coin-n-out').textContent = String(N);
    el('coin-k-out').textContent = String(k);
    el('coin-a-out').textContent = String(a);
    const like = grid.map((t) => betaPdf(t, k + 1, N - k + 1));
    const prior = grid.map((t) => betaPdf(t, a, a));
    const post = grid.map((t) => betaPdf(t, k + a, N - k + a));
    const ymax = Math.max(...like, ...prior, ...post) * 1.08;
    const sy = (y) => H - P - (y / ymax) * (H - 2 * P);
    const path = (ys) => ys.map((y, i) => (i ? 'L' : 'M') + sx(grid[i]).toFixed(1) + ' ' + sy(y).toFixed(1)).join(' ');
    const est = coinEstimates(N, k, a);
    const vline = (t, cls) => '<line class="' + cls + '" x1="' + sx(t).toFixed(1) + '" y1="' + P + '" x2="' + sx(t).toFixed(1) + '" y2="' + (H - P) + '"/>';
    const ticks = [0, 0.25, 0.5, 0.75, 1].map((t) => '<text class="tick" x="' + sx(t) + '" y="' + (H - 6) + '" text-anchor="middle">' + t + '</text>').join('');
    el('coin-plot').innerHTML = '<line class="axis" x1="' + P + '" y1="' + (H - P) + '" x2="' + (W - P) + '" y2="' + (H - P) + '"/>' + ticks
      + '<path class="plot-like" d="' + path(like) + '"/><path class="plot-prior" d="' + path(prior) + '"/><path class="plot-post" d="' + path(post) + '"/>'
      + vline(est.ml, 'mark-ml') + vline(est.map, 'mark-map');
    el('coin-ml').textContent = fmt(est.ml);
    el('coin-map').textContent = fmt(est.map);
    el('coin-pred').textContent = fmt(est.pred);
  }
  ['coin-n', 'coin-k', 'coin-a'].forEach((id) => el(id).addEventListener('input', draw));
  draw();
})();
</script>
```

**`s4-predictive` (0916 §18)**
- 🧸 "하나만 골라 말하지 말고, 가능한 모든 θ의 의견을 믿는 만큼 가중평균해서 예측하자"
- 📐 분포를 요약하는 방법
  - 연속 분포를 말로 설명하기 어렵다면, 가우시안(평균과 분산 2개)으로 요약한다. [0,1] 범위라면 Beta로 요약한다.
  - 봉우리가 여럿이면 mixture로 요약한다: `$\sum_k \pi_k \mathcal{N}(\mu_k, \sigma_k^2)$` → 학기 말 EM 알고리즘에서 다룬다.
- 📐 posterior predictive 유도(ol.steps)
  - `$$P(A \mid \mathbf{X}) = \int P(A, \boldsymbol{\theta} \mid \mathbf{X})\, d\boldsymbol{\theta} = \int P(A \mid \boldsymbol{\theta}, \mathbf{X})\, P(\boldsymbol{\theta} \mid \mathbf{X})\, d\boldsymbol{\theta} = \int P(A \mid \boldsymbol{\theta})\, P(\boldsymbol{\theta} \mid \mathbf{X})\, d\boldsymbol{\theta}$$`
- 📐 마지막 등호의 근거는 조건부 독립이다: `$P(x_1, \dots, x_N, A \mid \boldsymbol{\theta}) = \prod_{i=1}^{N} P(x_i \mid \boldsymbol{\theta}) \cdot P(A \mid \boldsymbol{\theta})$`
  - θ가 주어지면 X는 A에 대해 더 알려 주는 것이 없다.
- 📐 위젯 2의 "다음에 앞면 나올 확률"이 바로 이 값이다(동전의 경우 $\frac{k + a}{N + 2a}$).
- 🎙️ "이거는 다음 시간에 조금 더 자세히" (0916 72:04)

- [ ] **Step 4: 통과 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add tests/test_notes_html.py "강의노트/정리노트_0909-0916_When_Models_Meet_Data.html"
git commit -m "feat(note): write probabilistic inference section with coin widget"
```

---

### Task 9: 섹션 s5(치트시트 · 전제지식 · 예고 · 링크)

**Files:**
- Modify: `강의노트/정리노트_0909-0916_When_Models_Meet_Data.html` (`#s5`)
- Modify: `tests/test_notes_html.py` (`COMPLETED_SECTIONS`)

**Interfaces:**
- Consumes: 앞 섹션들의 토픽 id(치트시트의 앵커 링크 대상)

- [ ] **Step 1: 계약 활성화(RED)**

```python
COMPLETED_SECTIONS: list[str] = ["s0", "s1", "s2", "s3", "s4", "s5"]
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: FAIL. s5 용어, `test_s5_links`

- [ ] **Step 3: 콘텐츠 작성**

**`s5-cheatsheet`:** 제목 밑에 "시험 직전 한 장 치트시트" 문구를 넣고, `.table-wrap` 안에 표를 둔다(열: 개념 | 핵심 수식 | 한 줄 의미 | 노트 링크). 행은 다음과 같다.
1. 선형 예측기: `$f(\mathbf{x}_n, \boldsymbol{\theta}) = \boldsymbol{\theta}^\top \mathbf{x}_n$` → `#s2-affine`
2. Empirical risk: `$R_{\text{emp}} = \frac{1}{N}\sum_{n} \ell(y_n, \hat{y}_n)$` → `#s2-matrix`
3. Least squares: `$\min_{\boldsymbol{\theta}} \frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$` → `#s2-matrix`
4. Regularized LS: `$+\,\lambda\|\boldsymbol{\theta}\|^2$` → `#s2-reg`
5. NLL: `$\mathcal{L}(\boldsymbol{\theta}) = -\sum_{n} \log p(y_n \mid \mathbf{x}_n, \boldsymbol{\theta})$` → `#s3-iid`
6. MLE = LS (가우시안 노이즈) → `#s3-mle-ls`
7. MAP: `$\boldsymbol{\theta}_{\text{MAP}} = \arg\min_{\boldsymbol{\theta}} [-\log p(\mathbf{x} \mid \boldsymbol{\theta}) - \log p(\boldsymbol{\theta})]$` → `#s3-map`
8. 가우시안 prior ↔ L2: `$\lambda = \frac{\sigma^2}{N b^2}$` → `#s3-map-l2`
9. Posterior: `$p(\boldsymbol{\theta} \mid \mathbf{x}) \propto p(\mathbf{x} \mid \boldsymbol{\theta})\, p(\boldsymbol{\theta})$` → `#s4-posterior`
10. Posterior predictive: `$P(A \mid \mathbf{X}) = \int P(A \mid \boldsymbol{\theta})\, P(\boldsymbol{\theta} \mid \mathbf{X})\, d\boldsymbol{\theta}$` → `#s4-predictive`

**`s5-prereq`:** 표(열: MML 챕터 | 수업에서 쓰인 곳). 행은 다음과 같다.
- `Ch.2` 선형대수: 벡터·행렬 표기, 전치, 데이터 행렬 $\mathbf{X}$
- `Ch.3` 해석기하: 내적, 유클리드 노름, 1·2·p-노름
- `Ch.4` 행렬분해: SVD, 고유값분해(PCA의 도구)
- `Ch.5` 벡터미적분: 미분으로 argmin 찾기(동전 ML)
- `Ch.6` 확률과 분포: 조건부확률, Bayes, 주변화, i.i.d., 가우시안, Beta
- `Ch.7` 연속최적화: gradient descent, 최적화 관점("in terms of")

**`s5-next`:** "아직 수업에서 다루지 않은 슬라이드(제목만)" 목록을 넣는다.
- L02 s7 Bayesian Inference: Hardness (MCMC, Laplace approximation, variational inference)
- L02 s9–s15 Graphical Models · Directed Graphical Models · Conditional Independence & d-separation
- L02 s17 Nested Cross-Validation
- L02 s18 Bayesian Model Selection
- L02 s19 Bayes factor

예고된 일정도 적는다.
- 다음 주 Linear Regression(least squares와 pseudo-inverse로 θ를 한 번에 구하기)
- 실습(랩)
- 학기 말 EM 알고리즘

**`s5-links`:** 링크 목록이다. 링크 텍스트에 "Lecture 10", "Lecture 11", "Lecture 12"를 포함한다.
- `<a href="추가%20강의/eli5_lecture10_statistical_inference_part1.html">확률 및 랜덤변수 Lecture 10 · 통계적 추론 Part 1 (Bayesian, Beta prior)</a>`
- `<a href="추가%20강의/eli5_lecture11_statistical_inference_part2.html">Lecture 11 · Part 2 (MAP, LMS)</a>`
- `<a href="추가%20강의/eli5_lecture12_statistical_inference_part3.html">Lecture 12 · Part 3 (LLMS, ML)</a>`
- `<a href="복습문제_0909-0916_When_Models_Meet_Data.html">📝 복습문제 10선 풀러 가기</a>`
- 교수님 안내 한 줄: "지난 학기 확률 수업의 Statistical Inference 강의로 갈음" (0909 02:07)

- [ ] **Step 4: 통과 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: 전부 PASS(SKIP 0개)

- [ ] **Step 5: 커밋**

```bash
git add tests/test_notes_html.py "강의노트/정리노트_0909-0916_When_Models_Meet_Data.html"
git commit -m "feat(note): add cheatsheet, prerequisites, preview and links"
```

---

## 문제 카드 공통 마크업 (Task 10~11)

```html
<article class="card" id="pN" data-source="MML Example 8.1">
  <header class="card-head"><span class="badge src">MML Example 8.1 변형</span><span class="badge level">★</span><span class="tag date">📅 0914</span></header>
  <h3>PN. 제목</h3>
  <div class="problem">…한국어 문제…</div>
  <details class="original"><summary>📖 교과서 원문</summary>…원문(짧게)…</details>
  <details class="hint"><summary>💡 힌트</summary>…</details>
  <details class="solution"><summary>✅ 풀이</summary><ol class="steps">…</ol><p class="answer">정답: …</p></details>
  <p class="link-back">🔗 수업과 연결: <a href="정리노트_0909-0916_When_Models_Meet_Data.html#ANCHOR">…</a> — 한 줄 설명</p>
  <label class="done"><input type="checkbox" data-done="pN"> 풀었음</label>
</article>
```

각 카드의 `data-source`, 링크 앵커, 필수 용어는 `tests/test_notes_html.py`의 `PROBLEMS`와 일치해야 한다.

---

### Task 10: 복습문제 P1~P5 (교과서 8장 본문 예제)

**Files:**
- Modify: `강의노트/복습문제_0909-0916_When_Models_Meet_Data.html` (`#p1`~`#p5`)
- Modify: `tests/test_notes_html.py` (`COMPLETED_PROBLEMS`)

**Interfaces:**
- Consumes: 정리노트 앵커 `s2-affine`, `s2-matrix`, `s2-reg`, `s3-mle-ls`, `s3-map-l2`

- [ ] **Step 1: 계약 활성화(RED)**

```python
COMPLETED_PROBLEMS: list[str] = ["p1", "p2", "p3", "p4", "p5"]
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: FAIL. `test_completed_problems`

- [ ] **Step 3: 카드 작성.** 아래 내용을 공통 마크업에 채운다. 수식 문자열은 그대로 쓴다.

**P1:** `data-source="MML Example 8.1"`, ★, 📅0914, 앵커 `s2-affine`, 제목 "bias를 내적 안으로 넣기"
- 문제: D개의 특징을 가진 데이터에 대한 affine 예측기 $f(\mathbf{x}_n) = \theta_0 + \sum_{d=1}^{D} \theta_d x_n^{(d)}$를 생각하자.
  - (a) 이 식을 내적 하나 $\boldsymbol{\theta}^\top \mathbf{x}_n$으로 쓰려면 $\mathbf{x}_n$과 $\boldsymbol{\theta}$를 어떻게 다시 정의해야 하는가?
  - (b) 그때 두 벡터의 차원과 $f$의 정의역·공역은?
  - (c) 이 함수를 linear가 아니라 affine이라고 부르는 이유는?
- 원문: "We choose a more compact notation for an affine function by concatenating an additional unit feature $x^{(0)} = 1$ to $\mathbf{x}_n$ … (8.4) … (8.5)" — Example 8.1
- 힌트: $\theta_0 = 1 \cdot \theta_0$이다. 숫자 1을 데이터 쪽에 붙여 보자.
- 풀이
  1. `$\mathbf{x}_n = [1, x_n^{(1)}, \dots, x_n^{(D)}]^\top$`, `$\boldsymbol{\theta} = [\theta_0, \theta_1, \dots, \theta_D]^\top$`
  2. `$\boldsymbol{\theta}^\top \mathbf{x}_n = \theta_0 \cdot 1 + \sum_{d=1}^{D} \theta_d x_n^{(d)}$`로 원래 식과 같다.
  3. 두 벡터는 모두 `$\mathbb{R}^{D+1}$`에 속하고, $f: \mathbb{R}^{D+1} \to \mathbb{R}$이다(누운 벡터와 선 벡터의 내적은 스칼라).
  4. $f(\mathbf{0}) = \theta_0$이라 일반적으로 원점을 지나지 않는다. 그래서 affine이다.
- 정답: 앞에 1과 $\theta_0$를 붙인다. 둘 다 $\mathbb{R}^{D+1}$이다. 원점을 지나지 않을 수 있어서 affine이다.

**P2:** `data-source="MML Example 8.2"`, ★, 📅0914, 앵커 `s2-matrix`, 제목 "ERM을 행렬 한 줄로"
- 문제: 학습 데이터 $\{(\mathbf{x}_n, y_n)\}_{n=1}^{N}$($\mathbf{x}_n$은 P1처럼 1이 붙은 $\mathbb{R}^{D+1}$ 벡터), 선형 예측기 $\hat{y}_n = \boldsymbol{\theta}^\top \mathbf{x}_n$, squared loss가 주어졌다.
  - (a) empirical risk를 합(Σ) 꼴로 쓰시오.
  - (b) $\mathbf{X} := [\mathbf{x}_1, \dots, \mathbf{x}_N]^\top$, $\mathbf{y} := [y_1, \dots, y_N]^\top$로 두면 (a)가 `$\frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$`과 같음을 보이시오.
  - (c) $\mathbf{X}$와 $\mathbf{X}\boldsymbol{\theta}$의 크기는?
- 원문: Example 8.2, 식 (8.7)–(8.9) "…This equation can be equivalently expressed in matrix form…"
- 힌트: 벡터 $\mathbf{y} - \mathbf{X}\boldsymbol{\theta}$의 n번째 원소를 먼저 적어 보자. 유클리드 노름의 제곱은 원소 제곱의 합이다.
- 풀이
  1. $R_{\text{emp}} = \frac{1}{N}\sum_{n=1}^{N}(y_n - \boldsymbol{\theta}^\top \mathbf{x}_n)^2$
  2. $\mathbf{X}$의 n번째 행은 $\mathbf{x}_n^\top$이므로 $(\mathbf{X}\boldsymbol{\theta})_n = \mathbf{x}_n^\top \boldsymbol{\theta}$이다.
  3. $(\mathbf{y} - \mathbf{X}\boldsymbol{\theta})_n = y_n - \mathbf{x}_n^\top \boldsymbol{\theta}$
  4. $\|\mathbf{v}\|^2 = \sum_n v_n^2$이므로 (a)와 같다.
  5. $\mathbf{X} \in \mathbb{R}^{N \times (D+1)}$, $\mathbf{X}\boldsymbol{\theta} = \hat{\mathbf{y}} \in \mathbb{R}^{N}$
- 정답: `$\frac{1}{N}\sum_{n}(y_n - \boldsymbol{\theta}^\top \mathbf{x}_n)^2 = \frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$`, `$\mathbf{X} \in \mathbb{R}^{N \times (D+1)}$`

**P3:** `data-source="MML Example 8.3"`, ★★, 📅0914, 앵커 `s2-reg`, 제목 "λ를 0부터 무한대까지"
- 문제: `$\min_{\boldsymbol{\theta}} \frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 + \lambda\|\boldsymbol{\theta}\|^2$`에 대해 답하시오.
  - (a) $\lambda = 0$이면 어떤 문제가 되는가?
  - (b) `$\lambda \to \infty$`이면 해는 어디로 가는가?
  - (c) λ는 학습 파라미터인가, hyperparameter인가?
  - (d) [도전] gradient를 0으로 두어 해를 구하시오.
- 원문: Example 8.3, 식 (8.12) "The additional term $\|\boldsymbol{\theta}\|^2$ is called the regularizer…"
- 힌트
  - (b) 두 번째 항이 첫 번째 항을 압도하면 어떻게 될까?
  - (d) $\nabla_{\boldsymbol{\theta}}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 = -2\mathbf{X}^\top(\mathbf{y} - \mathbf{X}\boldsymbol{\theta})$, $\nabla_{\boldsymbol{\theta}}\|\boldsymbol{\theta}\|^2 = 2\boldsymbol{\theta}$
- 풀이
  1. (a) $\lambda = 0$이면 보통의 least squares(ERM만)가 된다. 과적합 위험이 있다("딱 과적합되기 좋지").
  2. (b) `$\lambda \to \infty$`이면 벌점이 지배해서 $\boldsymbol{\theta} \to \mathbf{0}$(원점)이 된다. 너무 단순해져 과소적합이다(위젯: 차수 9, λ=10).
  3. (c) hyperparameter다. 학습 전에 사람이 정한다.
  4. (d) $-\frac{2}{N}\mathbf{X}^\top(\mathbf{y} - \mathbf{X}\boldsymbol{\theta}) + 2\lambda\boldsymbol{\theta} = \mathbf{0}$ ⇒ `$(\mathbf{X}^\top \mathbf{X} + N\lambda \mathbf{I})\boldsymbol{\theta} = \mathbf{X}^\top \mathbf{y}$`. 다음 주 Linear Regression에서 정식으로 다룬다.
- 정답: (a) 과적합 위험, (b) $\boldsymbol{\theta} \to \mathbf{0}$, (c) hyperparameter, (d) $\boldsymbol{\theta} = (\mathbf{X}^\top \mathbf{X} + N\lambda \mathbf{I})^{-1}\mathbf{X}^\top \mathbf{y}$

**P4:** `data-source="MML Example 8.5"`, ★★, 📅0914·0916, 앵커 `s3-mle-ls`, 제목 "가우시안 NLL을 펼치면 least squares"
- 문제: 각 라벨이 $p(y_n \mid \mathbf{x}_n, \boldsymbol{\theta}) = \mathcal{N}(y_n \mid \mathbf{x}_n^\top \boldsymbol{\theta}, \sigma^2)$를 따르고 데이터는 i.i.d.라고 하자(σ는 알려진 상수).
  - (a) 전체 likelihood를 곱으로 쓰고, 왜 곱이 되는지 설명하시오.
  - (b) negative log-likelihood를 전개하시오.
  - (c) 그 최소화가 least squares와 같은 이유를 쓰시오.
- 원문: Example 8.4 (8.15)와 Example 8.5 (8.18a–d) "…minimizing $\mathcal{L}(\boldsymbol{\theta})$ corresponds to solving the least-squares problem…"
- 힌트: log는 곱을 합으로 바꾸고 exp를 없앤다. θ와 무관한 항은 argmin에 영향이 없다.
- 풀이
  1. independent이면 곱, identical이면 θ가 하나다: $p(\mathcal{Y} \mid \mathcal{X}, \boldsymbol{\theta}) = \prod_{n=1}^{N} \mathcal{N}(y_n \mid \mathbf{x}_n^\top \boldsymbol{\theta}, \sigma^2)$
  2. $\mathcal{L} = -\sum_{n} \log\Big[\frac{1}{\sqrt{2\pi\sigma^2}} \exp\big(-\frac{(y_n - \mathbf{x}_n^\top \boldsymbol{\theta})^2}{2\sigma^2}\big)\Big]$
  3. `$\mathcal{L}(\boldsymbol{\theta}) = \frac{N}{2}\log(2\pi\sigma^2) + \frac{1}{2\sigma^2}\sum_{n=1}^{N}(y_n - \mathbf{x}_n^\top \boldsymbol{\theta})^2$`
  4. 첫째 항은 상수이고, 둘째 항은 양수 × $\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$이다. 따라서 argmin이 least squares와 같다.
- 정답: 상수 + $\frac{1}{2\sigma^2}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2$ → least squares와 같은 해

**P5:** `data-source="MML Example 8.6"`, ★★★ 도전, 📅0916, 앵커 `s3-map-l2`, 제목 "prior가 곧 정규화"
- 배지 옆에 `<span class="badge supp">📎 보충 · 수업 미유도</span>`를 추가한다.
- 문제: P4에 prior $p(\boldsymbol{\theta}) = \mathcal{N}(\mathbf{0}, b^2\mathbf{I})$를 더한다. 교과서는 일반 공분산 $\boldsymbol{\Sigma}$를 쓰지만, 여기서는 $\boldsymbol{\Sigma} = b^2\mathbf{I}$로 단순화한 변형이다.
  - (a) $-\log p(\boldsymbol{\theta})$를 구하시오.
  - (b) MAP 목적함수를 쓰시오.
  - (c) P3의 정규화 LS와 같은 해를 주는 λ를 구하시오.
- 원문: Example 8.6 "…we assume that the parameter vector is distributed as a multivariate Gaussian with zero mean, i.e., $p(\boldsymbol{\theta}) = \mathcal{N}(\mathbf{0}, \boldsymbol{\Sigma})$…"
- 힌트: $\mathcal{N}(\mathbf{0}, b^2\mathbf{I})$의 밀도는 $\exp\big(-\frac{1}{2b^2}\|\boldsymbol{\theta}\|^2\big)$에 비례한다. 목적함수에 양수를 곱해도 argmin은 그대로다.
- 풀이
  1. `$-\log p(\boldsymbol{\theta}) = \frac{1}{2b^2}\|\boldsymbol{\theta}\|^2 + \text{const}$`
  2. $\boldsymbol{\theta}_{\text{MAP}} = \arg\min_{\boldsymbol{\theta}} \Big[\frac{1}{2\sigma^2}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 + \frac{1}{2b^2}\|\boldsymbol{\theta}\|^2\Big]$
  3. $\frac{2\sigma^2}{N}$를 곱하면 $\frac{1}{N}\|\mathbf{y} - \mathbf{X}\boldsymbol{\theta}\|^2 + \frac{\sigma^2}{N b^2}\|\boldsymbol{\theta}\|^2$
  4. 해석: b가 작을수록("θ는 작다"는 믿음이 강할수록) λ가 커진다.
- 정답: `$\lambda = \frac{\sigma^2}{N b^2}$`

- [ ] **Step 4: 통과 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add tests/test_notes_html.py "강의노트/복습문제_0909-0916_When_Models_Meet_Data.html"
git commit -m "feat(review): add problems P1-P5 from MML chapter 8 examples"
```

---

### Task 11: 복습문제 P6~P10 (교과서 연습문제)

**Files:**
- Modify: `강의노트/복습문제_0909-0916_When_Models_Meet_Data.html` (`#p6`~`#p10`)
- Modify: `tests/test_notes_html.py` (`COMPLETED_PROBLEMS`)

**Interfaces:**
- Consumes:
  - 정답 수치: `scripts/review_answers.py` (Task 1)
  - 정리노트 앵커: `s4-joint`, `s3-map`, `s4-coin`, `s4-generative`

- [ ] **Step 1: 계약 활성화(RED)**

```python
COMPLETED_PROBLEMS: list[str] = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10"]
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: FAIL. p6~p10

- [ ] **Step 3: 정답 키 출력 확인**

Run: `python3 scripts/review_answers.py`
Expected: 아래 각 줄이 출력된다.
- `p(x): ['4/25', '17/100', '11/100', '11/50', '17/50']`
- `P(bag2|mango): 1/3`
- `(6, 12)`
- `['1/5', '5/16', '1/3']`
- Ex 7.1 두 점(≈−4.236 max, ≈0.236 min)

- [ ] **Step 4: 카드 작성**

**P6:** `data-source="MML Exercise 6.1"`, ★, 📅0916, 앵커 `s4-joint`, 제목 "결합분포 표에서 주변·조건부 구하기"
- 문제: 두 이산 확률변수 X, Y의 결합분포가 아래 표와 같다.
  - (a) 주변분포 p(x), p(y)를 구하시오.
  - (b) 조건부분포 $p(x \mid Y = y_1)$, $p(y \mid X = x_3)$를 구하시오.
- 표(`.table-wrap` 안 `<table>`)

  |  | x1 | x2 | x3 | x4 | x5 |
  |---|---|---|---|---|---|
  | y1 | 0.01 | 0.02 | 0.03 | 0.1 | 0.1 |
  | y2 | 0.05 | 0.1 | 0.05 | 0.07 | 0.2 |
  | y3 | 0.1 | 0.05 | 0.03 | 0.05 | 0.04 |

- 원문: "Consider the following bivariate distribution p(x, y) of two discrete random variables X and Y. … Compute: a. The marginal distributions p(x) and p(y). b. The conditional distributions p(x|Y = y1) and p(y|X = x3)."
- 힌트: 주변화는 관심 없는 변수로 더하는 것이다. 연속이면 적분이며, 수업 식 $p(\mathbf{x}) = \int p(\mathbf{x}, \boldsymbol{\theta})\, d\boldsymbol{\theta}$와 같다. 조건부 = 결합 ÷ 주변.
- 풀이
  1. p(x)는 열 합: (0.16, 0.17, 0.11, 0.22, 0.34). 합이 1인지 확인한다.
  2. p(y)는 행 합: (0.26, 0.47, 0.27)
  3. `$p(x \mid y_1) = \frac{p(x, y_1)}{0.26} = \big(\frac{1}{26}, \frac{1}{13}, \frac{3}{26}, \frac{5}{13}, \frac{5}{13}\big)$`
  4. `$p(y \mid x_3) = \frac{p(x_3, y)}{0.11} = \big(\frac{3}{11}, \frac{5}{11}, \frac{3}{11}\big)$`
- 정답: 위 1–4

**P7:** `data-source="MML Exercise 6.4"`, ★, 📅0916, 앵커 `s3-map`, 제목 "망고는 어느 가방에서 왔을까 (Bayes)"
- 문제: 가방 1에는 망고 4개와 사과 2개, 가방 2에는 망고 4개와 사과 4개가 있다. 앞면 확률이 0.6인 동전을 던져 앞면이면 가방 1, 뒷면이면 가방 2에서 과일을 하나 꺼낸다. 친구가 (결과를 숨긴 채) 망고를 보여 줬다. 이 망고가 가방 2에서 나왔을 확률은?
- 원문: Exercise 6.4 원문 전체(짧음). "There are two bags. The first bag contains four mangos and two apples; … What is the probability that the mango was picked from bag 2? Hint: Use Bayes' theorem."
- 힌트: prior는 가방 선택 확률(0.6, 0.4), likelihood는 각 가방에서 망고가 나올 확률이다.
- 풀이
  1. prior: P(bag1) = 0.6, P(bag2) = 0.4
  2. likelihood: P(M | bag1) = 4/6 = 2/3, P(M | bag2) = 4/8 = 1/2
  3. evidence(marginal likelihood): P(M) = 0.6·2/3 + 0.4·1/2 = 0.4 + 0.2 = 0.6
  4. `$$P(\text{bag2} \mid M) = \frac{0.4 \cdot \frac{1}{2}}{0.6} = \frac{1}{3}$$`
  5. 해석: prior 0.4가 posterior 1/3으로 줄었다. 망고는 가방 1에서 더 잘 나오기 때문이다. 참고로 ML(likelihood만)로도, MAP로도 가방 1을 고른다.
- 정답: `$\frac{1}{3}$`

**P8:** `data-source="MML Exercise 6.3"`, ★★, 📅0916, 앵커 `s4-coin`, 제목 "베타-베르누이: 수업의 동전 완성하기"
- 배지 옆에 `<span class="badge supp">📎 보충 · 수업 미유도</span>`를 추가한다.
- 문제
  - (a) 원문 문제: Bernoulli likelihood $p(x \mid \mu) = \mu^x(1-\mu)^{1-x}$에 대한 켤레 사전분포를 고르고, 사후분포 $p(\mu \mid x_1, \dots, x_N)$를 구하시오.
  - [변형: 0916 수업의 동전] $x = 1$을 앞면이라 하고, 10번 던져 앞면이 2번 나왔다($\mu$는 수업의 θ와 같다).
    - (b) $\mu_{\text{ML}}$을 미분으로 구하시오.
    - (c) prior가 Beta(4, 4)일 때 $\mu_{\text{MAP}}$은?
    - (d) prior가 Beta(1, 1)(uniform)이면?
    - (e) Fully Bayesian으로 다음 던짐이 앞면일 확률은?
- 원문: "You have written a computer program that sometimes compiles and sometimes not … Choose a conjugate prior for the Bernoulli likelihood and compute the posterior distribution $p(\mu \mid x_1, \dots, x_N)$."
- 힌트
  - Beta 밀도는 $\mu^{\alpha-1}(1-\mu)^{\beta-1}$에 비례한다. 곱해 보면 같은 모양이 나온다.
  - Beta(α, β)의 최빈값은 $\frac{\alpha - 1}{\alpha + \beta - 2}$, 평균은 $\frac{\alpha}{\alpha + \beta}$다(확률 추가강의 Lecture 10).
- 풀이
  1. likelihood: $\prod_n \mu^{x_n}(1-\mu)^{1-x_n} = \mu^{k}(1-\mu)^{N-k}$, 단 $k = \sum_n x_n$
  2. prior Beta(α, β)와 곱하면 $\mu^{k+\alpha-1}(1-\mu)^{N-k+\beta-1}$ ⇒ 사후분포 `$\mathrm{Beta}(\alpha + k, \beta + N - k)$`. prior와 같은 가족이 되므로 켤레(conjugate)다.
  3. (b) $\ell(\mu) = 2\log\mu + 8\log(1-\mu)$, $\frac{2}{\mu} - \frac{8}{1-\mu} = 0$ ⇒ $\mu_{\text{ML}} = 0.2$
  4. (c) 사후분포 Beta(6, 12)의 최빈값: $\frac{5}{16} = 0.3125$. 교수님이 말한 "0.3 정도"다.
  5. (d) 사후분포 Beta(3, 9)의 최빈값: $\frac{2}{10} = 0.2$ = ML. uniform prior이면 MAP = ML이다.
  6. (e) `$P(x_{\text{new}} = 1 \mid \text{data}) = \int \mu\, p(\mu \mid \text{data})\, d\mu = \frac{6}{18} = \frac{1}{3}$`. 이것이 posterior predictive이며 정리노트의 동전 위젯 기본값과 같다.
- 정답: (a) Beta(α+k, β+N−k), (b) 0.2, (c) 0.3125, (d) 0.2, (e) 1/3

**P9:** `data-source="MML Exercise 6.12"`, ★, 📅0916, 앵커 `s4-generative`, 제목 "상수 + 가우시안 노이즈의 likelihood"
- 문제: $\mathbf{x} \sim \mathcal{N}(\boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$이고 $\mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{b} + \mathbf{w}$, $\mathbf{w} \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})$이며 x와 w는 독립이다.
  - (a) likelihood $p(\mathbf{y} \mid \mathbf{x})$를 쓰시오.
  - 원문의 (b)~(d)는 가우시안 주변화·조건화 규칙이 필요해서 이번 수업 범위 밖이다. 카드에 이 사실을 한 줄로 적는다.
- 원문: Exercise 6.12 앞부분 "Consider a Gaussian random variable $\mathbf{x} \sim \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_x, \boldsymbol{\Sigma}_x)$ … a. Write down the likelihood $p(\mathbf{y} \mid \mathbf{x})$."
- 힌트: x가 주어지면 $\mathbf{A}\mathbf{x} + \mathbf{b}$는 상수다. 수업의 $c_n = \mathbf{x}_n^\top \boldsymbol{\theta}$와 같은 역할이다.
- 풀이
  1. 조건부에서 $\mathbf{A}\mathbf{x} + \mathbf{b}$는 상수다.
  2. 상수 + 가우시안이면 평균만 이동하고 공분산은 그대로다.
  3. `$$p(\mathbf{y} \mid \mathbf{x}) = \mathcal{N}\big(\mathbf{y} \mid \mathbf{A}\mathbf{x} + \mathbf{b}, \mathbf{Q}\big)$$`
  4. 1차원 버전이 바로 수업의 $y_n \mid \mathbf{x}_n, \boldsymbol{\theta} \sim \mathcal{N}(\mathbf{x}_n^\top \boldsymbol{\theta}, \sigma^2)$이다.
- 정답: 위 3

**P10:** `data-source="MML Exercise 7.1"`, ★, 📅0916, 앵커 `s4-coin`, 제목 "미분해서 0: argmin 찾는 도구 연습"
- 문제: $f(x) = x^3 + 6x^2 - 3x - 5$의 정상점(stationary point)을 구하고, 각각 최대·최소·안장점 중 무엇인지 판정하시오.
- 원문: "Consider the univariate function $f(x) = x^3 + 6x^2 - 3x - 5$. Find its stationary points and indicate whether they are maximum, minimum, or saddle points."
- 힌트: $f'(x) = 0$으로 후보를 찾고, $f''$의 부호로 판정한다.
- 풀이
  1. $f'(x) = 3x^2 + 12x - 3 = 0 \iff x^2 + 4x - 1 = 0$
  2. 근의 공식으로 `$x = -2 + \sqrt{5}$`(≈ 0.236) 또는 `$x = -2 - \sqrt{5}$`(≈ −4.236)
  3. `$f''(x) = 6x + 12$`
  4. $x = -2 + \sqrt{5}$에서 $f'' = 6\sqrt{5} \gt 0$이므로 극소, $x = -2 - \sqrt{5}$에서 $f'' = -6\sqrt{5} \lt 0$이므로 극대. 안장점은 없다.
  5. 수업과의 연결: MLE·ERM의 argmin도 "미분해서 0"으로 찾는다(0916 동전: "미분해 보면 나오거든요"). 2계 도함수는 그 점이 정말 최소인지 확인하는 도구다.
- 정답: 극소 $x = -2 + \sqrt{5}$, 극대 $x = -2 - \sqrt{5}$

- [ ] **Step 5: 통과 확인**

Run: `python3 -m unittest discover -s tests -p "test_notes_html.py" -v`
Expected: PASS

- [ ] **Step 6: 커밋**

```bash
git add tests/test_notes_html.py "강의노트/복습문제_0909-0916_When_Models_Meet_Data.html"
git commit -m "feat(review): add problems P6-P10 from MML exercises"
```

---

### Task 12: 브라우저 검증 + 전체 테스트

**Files:**
- 수정 없음(발견된 결함은 해당 HTML에서 고치고, 고친 뒤 이 태스크를 처음부터 다시 실행)

- [ ] **Step 1: 전체 자동 테스트**

Run: `python3 -m unittest discover -s tests -p "test_*.py" -v && node --test tests/widget_math.test.js && python3 scripts/check_notes_html.py "강의노트/정리노트_0909-0916_When_Models_Meet_Data.html" "강의노트/복습문제_0909-0916_When_Models_Meet_Data.html"`
Expected: unittest 전부 OK(기존 `test_extract_exercises` 포함), node `# fail 0`, 검사기 두 줄 모두 `OK`

- [ ] **Step 2: 정리노트를 브라우저로 열기**

in-app 브라우저(`mcp__Claude_Browser__navigate`)로 다음 URL을 연다.
`file:///Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/강의노트/정리노트_0909-0916_When_Models_Meet_Data.html`

- [ ] **Step 3: 렌더링 검사**

KaTeX 로드를 기다린 뒤 `mcp__Claude_Browser__javascript_tool`로 실행한다.

```js
await new Promise((r) => setTimeout(r, 1500));
({
  katex: document.querySelectorAll('.katex').length,
  katexErrors: document.querySelectorAll('.katex-error').length,
  rawDollar: Array.from(document.querySelectorAll('main *')).filter((e) => !['SCRIPT', 'STYLE'].includes(e.tagName))
    .some((e) => Array.from(e.childNodes).some((n) => n.nodeType === 3 && n.textContent.includes('$'))),
  hScroll: document.documentElement.scrollWidth > window.innerWidth,
  regTrain: document.getElementById('reg-train-mse').textContent,
  regTest: document.getElementById('reg-test-mse').textContent,
  coin: ['coin-ml', 'coin-map', 'coin-pred'].map((id) => document.getElementById(id).textContent),
})
```

Expected: `katex`가 100 초과, `katexErrors: 0`, `rawDollar: false`, `hScroll: false`, `regTrain: "0.000"`, `regTest: "0.712"`, `coin: ["0.2","0.3125","0.3333"]`

- [ ] **Step 4: 위젯 상호작용 검사**

```js
const set = (id, v) => { const e = document.getElementById(id); e.value = String(v); e.dispatchEvent(new Event('input')); };
set('reg-degree', 3); set('reg-lambda', 3);
const good = document.getElementById('reg-test-mse').textContent;
set('reg-degree', 1); set('reg-lambda', 0);
const under = document.getElementById('reg-test-mse').textContent;
set('coin-a', 1);
const uniform = [document.getElementById('coin-ml').textContent, document.getElementById('coin-map').textContent];
set('coin-n', 1);
({ good, under, uniform, kMax: document.getElementById('coin-k').max, k: document.getElementById('coin-k').value })
```

Expected: `good: "0.109"`, `under: "0.417"`, `uniform: ["0.2","0.2"]`, `kMax: "1"`, `k: "1"`

- [ ] **Step 5: 모바일과 다크모드 확인**

1. `mcp__Claude_Browser__resize_window`를 `preset: "mobile"`, `colorScheme: "dark"`로 호출하고 페이지를 새로고침한다.
2. Step 3의 스크립트를 다시 실행한다. `hScroll: false`여야 한다.
3. `computer` 스크린샷으로 섹션 s2의 위젯과 s3의 그림을 보고, 다크 배경에서 글자와 선이 보이는지 확인한다.
4. 끝나면 `preset: "desktop"`, `colorScheme: "light"`로 되돌린다.

- [ ] **Step 6: 복습문제 확인**

`file:///Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/강의노트/복습문제_0909-0916_When_Models_Meet_Data.html`을 열고 실행한다.

```js
await new Promise((r) => setTimeout(r, 1500));
document.querySelectorAll('details').forEach((d) => { d.open = true; });
await new Promise((r) => setTimeout(r, 300));
const box = document.querySelector('input[data-done="p1"]'); box.click();
({
  cards: document.querySelectorAll('article.card').length,
  katexErrors: document.querySelectorAll('.katex-error').length,
  progress: document.getElementById('progress-count').textContent,
  hScroll: document.documentElement.scrollWidth > window.innerWidth,
})
```

Expected: `cards: 10`, `katexErrors: 0`, `progress: "1"`, `hScroll: false`

새로고침한 뒤 `progress-count`가 `"1"`로 유지되는지(localStorage) 확인하고, p1 체크를 해제해 원래대로 둔다.

- [ ] **Step 7: 링크 왕복 확인**

복습문제 P1의 "수업과 연결" 링크를 클릭하면 정리노트 `#s2-affine`으로 이동해야 한다. 정리노트 `#s5-links`의 Lecture 10 링크는 `추가 강의/eli5_lecture10…html`을 열어야 한다.

- [ ] **Step 8: 최종 커밋(검증 중 수정이 있었을 때만)**

```bash
git add "강의노트/정리노트_0909-0916_When_Models_Meet_Data.html" "강의노트/복습문제_0909-0916_When_Models_Meet_Data.html"
git commit -m "fix: address browser verification findings"
```

---

## Self-Review 결과

- **Spec 커버리지**

  | Spec 항목 | 태스크 |
  |---|---|
  | 통합 노트 | Task 4~9 |
  | 4층 블록 | 공통 규칙, `test_completed_layers` |
  | 📎 보충 3개 | `s3-map-l2`, `s4-coin` 두 곳, 테스트 `SUPP_TOPICS` |
  | 잡담 제외와 말실수 정정 | Global Constraints |
  | 추가강의 링크 | `s4-joint`, `s5-links`, `test_s5_links` |
  | Lecture00 | `s0-course` |
  | 위젯 2개 | Task 6, 8, 12 |
  | 문제 UX | 공통 마크업, 진행률 스크립트 |
  | 정답 검증 | Task 1, 11 Step 3 |
  | 스택과 외부 리소스 | `test_external_resources_allowlisted` |
  | 경로 | Global Constraints |
  | 브라우저 검증 | Task 12 |
  | #1 범위 | `FORBIDDEN_OUTSIDE_NEXT`, `s5-next` |
  | #2 문제 출처 | `PROBLEMS` 10개와 출처 |

- **Placeholder 검사:** 골격의 `widget-math` 자리 표시 주석은 Step 3에서 교체하도록 지시했고, 교체 여부는 `test_widget_math_inline_copy_matches_source`가 검사한다.
- **이름 일관성:** 다음 이름들이 테스트 상수와 마크업에서 같은 철자를 쓰는지 확인했다.
  - 테스트 상수: `TOPIC_IDS`, `FIGURE_IDS`, `WIDGET_IDS`, `PROBLEMS[*].anchor`
  - JS 전역 함수: `makeDataset`, `ridgeFit`, `predictPoly`, `mse`, `betaPdf`, `coinEstimates`
  - UI 스크립트 id: `widget-reg-ui`, `widget-coin-ui`
