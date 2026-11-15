# `ml-problem-explain` 서술 규칙 개정 및 11월 문제설명 HTML 업데이트 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `ml-problem-explain`의 해설 서술 규칙과 HTML 템플릿·계약 검사를 '시각·구조 중심 스캔형 서술'(`<table>` + `ol.deriv` 식·주석 + 답 구조 선제시 + 기호 직결)로 개편하고, 11월 복습팩 3개(`1102`, `1104`, `1111`, 총 28문항)의 문제설명 HTML·MD를 개정 규칙에 맞춰 병렬로 재저작·검증·발행한다.

**Architecture:** 기존 7구역 계약(`understand`~`retry`)과 `mpe_cli.py` 파이프라인(`extract → build → check → publish`)은 유지하되, 형제 스킬 `ml-review-pack`이 이미 구현한 `ol.deriv` CSS/`deriv-fit` JS·`deriv_row_errors`·`html2md` 변환기를 `ml-problem-explain` 템플릿·계약 검사로 이식·연동한다. 규칙과 템플릿이 고정된 뒤, 독립된 3개 날짜(`1102`, `1104`, `1111`)를 별도 `RUN` 디렉터리로 분리해 3개 서브에이전트가 병렬로 재저작·감사·브라우저 검증·발행한다.

**Tech Stack:** Python 3.10+ (표준 라이브러리), pytest, Playwright (Chromium 브라우저 회귀 검증), KaTeX + Pretendard (로컬 `assets/vendor`), PowerShell.

**Spec:** 직전 턴 `/grill-yourself` 설계 확정안 (기본값 확정: `#6`=11월 복습팩 `1102`·`1104`·`1111` 28문항, `#7`=`solve` 첫 줄 답 구조/결론 선제시, `#8`=유형별 선별 집중 개편) + 참조 규격 [`.claude/skills/ml-review-pack/references/staged-body.md`](../../../.claude/skills/ml-review-pack/references/staged-body.md)

## Global Constraints

- 모든 HTML 조각은 `mpe_contract.py`의 7구역(`understand`, `recall`, `start`, `solve`, `verify`, `pitfall`, `retry`) 순서와 직계 `layer`, 소문항별 `solve`/`verify` 표지(`data-subpart`), `div.sum[hidden]`, `data-problem-panel="terms"`, `retry` `li` 1~3개 계약을 위반하지 않는다.
- 문제설명 본문에는 `<details>` 태그, `hidden` 속성(`div.sum` 제외), 인라인 `style`(SVG `stroke-width` 제외), 외부 리소스를 절대 넣지 않는다(`ol.deriv` 내부에서도 `<details>`("자세히") 금지).
- 정본 스킬 디렉터리는 `.claude/skills/ml-problem-explain`이며(`.agents/skills/ml-problem-explain`은 이를 가리키는 `SymbolicLink`), 원 문제 HTML·정리노트·PDF·기존 `evidence/` 검산 근거는 훼손하지 않는다.
- 모든 수정 팩은 `rerender`가 아닌 `extract → 조각 재저작 → build → check → ml-note-audit → review.json 4종(source_visual/content/independent/browser) pass → publish` 정식 경로로 발행한다.
- 미분 포함 문항은 `.claude/skills/ml-review-pack/scripts/check_vector_derivatives.py`를 통과해야 하며, 브라우저 검사는 1280×900·1024×900·375×812 (light/dark)에서 가로 넘침 0 및 KaTeX/콘솔 오류 0을 만족해야 한다.

## Review Focus

- **숨은 토픽 전환 시 `deriv-fit` 재계산:** 문제설명 HTML은 한 번에 하나의 `article.topic`만 표시하고 나머지는 `[hidden]`이므로, 두 번째 문항으로 이동할 때 폭 0에서 깨지지 않고 `ol.deriv` 주석 위치(`is-wide`)가 정확히 재측정되어야 한다. (Task 1 브라우저 테스트로 검증)
- **`mlLayoutMath()`와 `ol.deriv` 내 `.katex-display` 충돌 방지:** `note-template.html` 하단의 `mlLayoutMath()`가 `.deriv-eq .katex-display`를 `.math-row`로 감쌀 때도 `deriv-fit`의 `k.scrollWidth > k.clientWidth + 1` 판정과 375px 가로 넘침 0이 깨지지 않아야 한다. (Task 1 브라우저 테스트로 검증)
- **`ol.deriv` 내 `<details>` 혼입 차단:** `ml-review-pack` 예시를 그대로 복사해 `<details>`("자세히")를 넣으면 `mpe_contract.validate_fragment`가 즉시 거부해야 한다. (Task 1 단위 테스트로 검증)
- **`ol.deriv`와 `<table>`이 섞인 문항의 `html2md` 및 `check_md` 동기화:** `build_explanation`이 생성한 `.pack/문제설명_*.md`에 `$$` + `↳ 주석`과 마크다운 표가 깨지지 않고 `check_md` 오류가 0이어야 한다. (Task 1 단위 테스트 + Task 3~5 `check`로 검증)
- **수치·수식 재저작 중 기존 정답/조건 변질 방지:** 줄글을 `<table>`과 `ol.deriv`로 풀면서 반올림 자릿수, 부호, 조건 가정이 원문 및 `evidence/` 검산 스크립트와 어긋나지 않아야 한다. (Task 3~5 `ml-note-audit` 및 `independent` 재검증으로 확인)

---

## File Structure & Parallel Waves

- **Wave 1 (선행 기반 — Task 1 이후 Task 2 또는 인터페이스 고정 후 병렬):**
  - **Task 1**: `.claude/skills/ml-problem-explain/assets/note-template.html`, `scripts/mpe_shared.py`, `scripts/mpe_contract.py`, `tests/test_deriv_explain.py` — `ol.deriv` 스타일/스크립트/계약 검사/MD·브라우저 회귀 테스트 구축.
  - **Task 2**: `.claude/skills/ml-problem-explain/references/authoring.md`, `SKILL.md`, `references/verification.md` — 개정 서술 규칙 및 검토 체크리스트 반영.
- **Wave 2 (완전 병렬 — Task 1·2 완료 후 3개 서브에이전트 동시 실행):**
  - **Task 3**: `복습노트/1102/` (`문제설명_1102_PCA.html` 외 `.pack/` 산출물, 10문항) — RUN `tmp/ml-problem-explain/revamp-1102`
  - **Task 4**: `복습노트/1104/` (`문제설명_1104_PCA_Part2.html` 외 `.pack/` 산출물, 10문항) — RUN `tmp/ml-problem-explain/revamp-1104`
  - **Task 5**: `복습노트/1111/` (`문제설명_1111_Gaussian_Mixture_Models.html` 외 `.pack/` 산출물, 8문항) — RUN `tmp/ml-problem-explain/revamp-1111`
- **Wave 3 (통합 검증):**
  - **Task 6**: 전체 `ml-problem-explain` pytest + 1102/1104/1111 최종 발행본 Playwright 크로스 뷰포트 확인 + 정리.

---

### Task 1: 템플릿 `ol.deriv` 이식, 계약 검사 연동 및 회귀 테스트 추가

**Files:**
- Modify: `.claude/skills/ml-problem-explain/scripts/mpe_shared.py:10-12`
- Modify: `.claude/skills/ml-problem-explain/scripts/mpe_contract.py:1-10,42-81`
- Modify: `.claude/skills/ml-problem-explain/assets/note-template.html` (CSS ~120줄 이후 + `</body>` 직전 `<script id="deriv-fit">`)
- Reference (read-only): `.claude/skills/ml-review-pack/assets/note-template.html:90-120,861-894`
- Create: `.claude/skills/ml-problem-explain/tests/test_deriv_explain.py`

**Interfaces:**
- Consumes: `ml-review-pack/scripts/check_html.py:deriv_row_errors(source: str) -> list[str]` (via `mpe_shared.py`), `ml-review-pack/assets/note-template.html`의 `.deriv-body`, `ol.deriv`, `.deriv-eq`, `.deriv-why`, `.deriv-gen`, `.deriv-check`, `.deriv-legend` CSS 및 `#deriv-fit` 스크립트.
- Produces:
  - `mpe_shared.deriv_row_errors(source: str) -> list[str]`
  - `mpe_contract.validate_fragment(problem, fragment)` — 기존 검사 + `deriv_row_errors(fragment)` 포함
  - `note-template.html` — `ol.deriv` CSS + `#deriv-fit` JS 지원

- [ ] **Step 1: 실패하는 단위·MD·브라우저 회귀 테스트 작성 (`tests/test_deriv_explain.py`)**

```python
from dataclasses import replace
from pathlib import Path
import pytest
from helpers import fragment, problem
from mpe_contract import validate_fragment
from mpe_render import build_explanation
from mpe_source import load_source

ROOT = Path(__file__).resolve().parents[4]

VALID_DERIV_SOLVE = (
    '<div class="layer formal" data-explanation="solve">'
    '<h4>왜 이렇게 푸는지 함께 따라가요</h4>'
    '<div data-subpart="a"><h4>(a)</h4>'
    '<p>결론: $A=1$이에요.</p>'
    '<div class="deriv-body"><ol class="deriv">'
    '<li><div class="deriv-eq">$$A = 1$$</div>'
    '<div class="deriv-why"><p>주어진 조건을 그대로 써요.</p></div></li>'
    '</ol></div></div>'
    '<div data-subpart="b"><h4>(b)</h4><p>답은 $2$예요.</p></div>'
    '</div>'
)


def _swap_solve(base: str, new_solve: str) -> str:
    from mpe_shared import outer, parse
    node = next(parse(base).find_all(lambda n: n.attrs.get('data-explanation') == 'solve'))
    return base.replace(outer(node), new_solve)


def test_valid_deriv_and_table_fragment_accepted():
    base = fragment()
    with_deriv = _swap_solve(base, VALID_DERIV_SOLVE)
    assert validate_fragment(problem(), with_deriv) == []
    with_table = _swap_solve(
        base,
        '<div class="layer formal" data-explanation="solve"><h4>풀이</h4>'
        '<div data-subpart="a"><h4>(a)</h4>'
        '<div class="table-wrap"><table><thead><tr><th>x</th><th>값</th></tr></thead>'
        '<tbody><tr><td>1</td><td>1</td></tr></tbody></table></div></div>'
        '<div data-subpart="b"><h4>(b)</h4><p>2</p></div></div>',
    )
    assert validate_fragment(problem(), with_table) == []


def test_deriv_row_requires_one_formula_visible_note_and_forbids_details():
    base = fragment()
    bad_eq = VALID_DERIV_SOLVE.replace('$$A = 1$$', '$$A = 1$$ $$B = 2$$')
    assert any('수식' in e for e in validate_fragment(problem(), _swap_solve(base, bad_eq)))
    bad_why = VALID_DERIV_SOLVE.replace('<p>주어진 조건을 그대로 써요.</p>', '<p>   </p>')
    assert any('주석' in e for e in validate_fragment(problem(), _swap_solve(base, bad_why)))
    bad_details = VALID_DERIV_SOLVE.replace(
        '</div></li>',
        '<details><summary>자세히</summary><p>숨김</p></details></div></li>',
    )
    assert any('details' in e for e in validate_fragment(problem(), _swap_solve(base, bad_details)))


def test_build_explanation_converts_deriv_to_markdown(tmp_path):
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    p = pack.problems[0]
    pack = replace(pack, problems=(p,))
    frag = _swap_solve(
        fragment(p),
        VALID_DERIV_SOLVE.replace('<div data-subpart="b"><h4>(b)</h4><p>답은 $2$예요.</p></div>',
                                  '<div data-subpart="b"><h4>(b)</h4><p>2</p></div>'
                                  '<div data-subpart="c"><h4>(c)</h4><p>3</p></div>'),
    )
    artifacts = build_explanation(pack, {p.id: frag}, tmp_path / 'stage', ROOT)
    md = artifacts.md.read_text(encoding='utf-8')
    assert 'A = 1' in md
    assert '↳ 주어진 조건을 그대로 써요.' in md


def test_deriv_fit_reflows_hidden_topic_without_horizontal_overflow(tmp_path):
    pw = pytest.importorskip('playwright.sync_api')
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    p1, p2 = pack.problems[0], pack.problems[1]
    pack = replace(pack, problems=(p1, p2))
    wide_eq = r'$$' + ' + '.join(f'x_{{{i}}}' for i in range(1, 20)) + r' = 0$$'
    frag2 = _swap_solve(
        fragment(p2),
        '<div class="layer formal" data-explanation="solve"><h4>풀이</h4>'
        '<div data-subpart="a"><h4>(a)</h4>'
        '<div class="deriv-body"><ol class="deriv">'
        f'<li><div class="deriv-eq">{wide_eq}</div>'
        '<div class="deriv-why"><p>넓은 식은 주석이 아래로 내려가요.</p></div></li>'
        '</ol></div></div>'
        + ''.join(f'<div data-subpart="{s}"><h4>({s})</h4><p>1</p></div>' for s in p2.subparts if s != 'a')
        + '</div>',
    )
    artifacts = build_explanation(pack, {p1.id: fragment(p1), p2.id: frag2}, tmp_path / 'stage', ROOT)
    with pw.sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto(artifacts.html.as_uri(), wait_until='networkidle')
        page.evaluate('location.hash="p2"')
        page.wait_for_function('document.querySelector("#p2").hidden===false')
        page.wait_for_timeout(150)
        assert page.locator('#p2 ol.deriv > li').first.evaluate('el => getComputedStyle(el).gridTemplateColumns.split(" ").length') == 1
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert page.locator('.katex-error').count() == 0
        browser.close()
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `pytest .claude/skills/ml-problem-explain/tests/test_deriv_explain.py -v`
Expected: FAIL (`test_deriv_row_requires_one_formula_visible_note_and_forbids_details` 또는 `test_deriv_fit_reflows...` 실패)

- [ ] **Step 3: `mpe_shared.py`에 `deriv_row_errors` export 추가 및 `mpe_contract.py`에 연결**

In `.claude/skills/ml-problem-explain/scripts/mpe_shared.py:11`:
`from check_html import math_delimiter_errors, deriv_row_errors`

In `.claude/skills/ml-problem-explain/scripts/mpe_contract.py:8,79`:
`from mpe_shared import Node, parse, math_delimiter_errors, deriv_row_errors`
`validate_fragment()` 내부에 `errors.extend(deriv_row_errors(fragment))` 추가.

- [ ] **Step 4: `.claude/skills/ml-problem-explain/assets/note-template.html`에 `ol.deriv` CSS와 `#deriv-fit` JS 이식**

`.claude/skills/ml-review-pack/assets/note-template.html:90-120`의 `/* 식 줄 + 주석 */` CSS 블록을 `.claude/skills/ml-problem-explain/assets/note-template.html`의 `.table-wrap` / `table` 스타일 부근(`~120줄`)에 추가한다(단, 문제설명에서는 `details`를 금지하므로 `.deriv-why details`/`.deriv-why summary` 규칙은 빼거나 그대로 두어도 무해하며, 불필요 규칙 제거 원칙상 제외 권장).
그리고 `.claude/skills/ml-review-pack/assets/note-template.html:861-894`의 `<script id="deriv-fit">` 블록을 `.claude/skills/ml-problem-explain/assets/note-template.html`의 `</body>` 직전에 추가하고, 숨은 토픽 전환(`od:screen` 이벤트) 시에도 `refitVisible()`이 실행되도록 `document.addEventListener('od:screen', refitVisible);` 한 줄을 `start()` 안에 추가한다(문제설명 템플릿은 토픽별 `hidden` 전환을 쓰기 때문).

- [ ] **Step 5: 신규 테스트 및 기존 전체 테스트 통과 확인**

Run: `pytest .claude/skills/ml-problem-explain/tests -v`
Expected: ALL PASS (기존 테스트 + `test_deriv_explain.py` 4개 모두 통과)

- [ ] **Step 6: Commit**

```powershell
git add .claude/skills/ml-problem-explain/scripts/mpe_shared.py .claude/skills/ml-problem-explain/scripts/mpe_contract.py .claude/skills/ml-problem-explain/assets/note-template.html .claude/skills/ml-problem-explain/tests/test_deriv_explain.py
git commit -m "feat(ml-problem-explain): support ol.deriv layout and row checks"
```

---

### Task 2: `ml-problem-explain` 서술 규칙 개정 (`authoring.md`, `SKILL.md`, `verification.md`)

**Files:**
- Modify: `.claude/skills/ml-problem-explain/references/authoring.md:1-86`
- Modify: `.claude/skills/ml-problem-explain/SKILL.md:8-10,38`
- Modify: `.claude/skills/ml-problem-explain/references/verification.md:10-12`
- Reference (read-only): `.claude/skills/ml-review-pack/references/staged-body.md:49-60`

**Interfaces:**
- Consumes: Task 1에서 확정된 CSS 클래스(`.deriv-body`, `ol.deriv`, `.deriv-eq`, `.deriv-why`, `.deriv-gen`, `.deriv-check`, `.deriv-legend`, `.table-wrap`) 및 `deriv_row_errors` 검증 규칙.
- Produces: Task 3, 4, 5 서브에이전트 저작자/검토자가 따를 개정된 `authoring.md` 서술 계약.

- [ ] **Step 1: `authoring.md`에 '시각·구조 중심 스캔형 서술' 규칙 추가**

`.claude/skills/ml-problem-explain/references/authoring.md`에 다음 5개 구체 규칙을 반영한다(기존 `vector-derivative-convention.md`, `problem-solving-depth.md`, 7구역/소문항 표지/우측 요약 계약, `<details>` 금지 계약은 유지):
1. **`understand` 기호 직결·압축**: '표·줄·점' 같은 과도한 일상어 역번역을 금지하고, 문제의 기호($\mathbf P, \mathbf x, U$)를 직접 주어로 쓰며 괄호·동격으로 의미를 붙인다. `주어진 것`과 `구할 것` 핵심만 2~3줄(또는 불릿)로 적어 `recall`·`start`와 문장 복제를 피한다.
2. **`recall` 역할 주석**: 공식이 등장하면 기호 뜻과 분자·분모/항별 역할을 수식 위 `\overbrace`·`\underbrace` 또는 짧은 불릿으로 바로 대응시킨다.
3. **`start` 로드맵·뼈대**: 첫 식(또는 채울 빈 표의 행·열 뼈대)과 함께 2~3단계 풀이 순서를 한 줄 로드맵으로 적는다.
4. **`solve` 답 구조 선제시 + 유형별 2가지 포맷 분기**:
   - 각 소문항(또는 `solve` 상단) 첫 줄에 **최종 답 구조/결론 요약**을 먼저 밝힌 뒤 전개한다.
   - **수치 반복 계산형**(숫자·항이 3개 이상 이어지는 경우): 줄글 문단에 수치를 나열하지 말고 `<div class="table-wrap"><table>...</table></div>` 표로 계산 단계를 분리한다(대표 1항 대입 예시 1줄 + 전체 표 + 결과 해석 1줄).
   - **유도·증명형**(등호 연쇄·논리 근거가 핵심인 경우): `<div class="deriv-body"><ol class="deriv"><li><div class="deriv-eq">$$...$$</div><div class="deriv-why"><p>...</p></div></li>...</ol></div>` 형식으로 한 줄에 디스플레이 수식 1개와 사용한 성질·근거 한 줄(~25자)을 나란히 둔다. `ol.deriv` 안에 `<details>`를 쓰지 않는다.
   - **짧은 단답·개념 판별형**: 불필요한 표/`ol.deriv`를 억지로 쓰지 않고 2~3줄 핵심 근거만 간결히 적는다.
5. **표·식 줄 가독성**: `수식과 여백` 절에 `ol.deriv` 간격/강조(`\textcolor{#3182f6}{...}` 규칙은 `staged-body.md:53` 준수) 및 `.table-wrap` 사용 원칙을 추가한다.

- [ ] **Step 2: `SKILL.md` 및 `verification.md` 동기화**

- `.claude/skills/ml-problem-explain/SKILL.md:8,38`의 서술 순서 안내에 `solve` 시작 시 답 구조 선제시 및 표/`ol.deriv` 포맷 선택 기준을 반영한다.
- `.claude/skills/ml-problem-explain/references/verification.md:10-12`의 `content`·`browser` 체크 항목에 `ol.deriv` 행별 수식 1개 + 보이는 한 줄 주석, `<table>` 모바일 가로 넘침 0, `solve` 선제시 결론과 본문·요약 일치 확인을 추가한다.

- [ ] **Step 3: `.agents/skills/ml-problem-explain` 심볼릭 링크 반영 확인**

Run: `Compare-Object (Get-Content ".claude/skills/ml-problem-explain/references/authoring.md") (Get-Content ".agents/skills/ml-problem-explain/references/authoring.md")`
Expected: 출력 없음 (diff count 0)

- [ ] **Step 4: Commit**

```powershell
git add .claude/skills/ml-problem-explain/references/authoring.md .claude/skills/ml-problem-explain/SKILL.md .claude/skills/ml-problem-explain/references/verification.md
git commit -m "docs(ml-problem-explain): revise authoring rules for scannable visual explanations"
```

---

### Task 3 (Wave 2 병렬 A): `1102` 문제설명 HTML 업데이트 (10문항)

**Files:**
- Read-only inputs: `복습노트/1102/복습문제_1102_PCA.html`, `복습노트/1102/.pack/정리노트_1102_PCA.md`, `복습노트/1102/.pack/자료_문제설명_1102_PCA/fragments/p1.html`..`p10.html`, `복습노트/1102/.pack/자료_문제설명_1102_PCA/evidence/*`
- Working RUN: `tmp/ml-problem-explain/revamp-1102`
- Output (published by `mpe_cli.py publish`): `복습노트/1102/문제설명_1102_PCA.html`, `복습노트/1102/.pack/문제설명_1102_PCA.md`, `복습노트/1102/.pack/자료_문제설명_1102_PCA/*`

**Interfaces:**
- Consumes: Task 1의 `note-template.html`·`mpe_contract.py` 및 Task 2의 개정된 `authoring.md`·`verification.md`.
- Produces: 개정 서술 규칙이 적용되고 `mpe_cli.py publish`를 통과한 `1102` 산출물.

- [ ] **Step 1: 새 RUN으로 `extract` 실행 및 기존 `fragments`/`evidence` 확인**

Run:
```powershell
if (Test-Path "tmp/ml-problem-explain/revamp-1102") { Remove-Item -Recurse -Force "tmp/ml-problem-explain/revamp-1102" }
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py extract --repo . --target 1102 --run tmp/ml-problem-explain/revamp-1102
```
Expected: `extract: ...\revamp-1102\review-1102-PCA\source.json` 출력, 종료 코드 0.
기존 `복습노트/1102/.pack/자료_문제설명_1102_PCA/evidence/*`를 `tmp/ml-problem-explain/revamp-1102/review-1102-PCA/evidence/`로 복사해 독립 검산 자료를 확보한다.

- [ ] **Step 2: 10문항(`p1`~`p10`)을 개정된 `authoring.md`에 따라 `explanations/pN.html`로 재저작**

기존 `복습노트/1102/.pack/자료_문제설명_1102_PCA/fragments/p1.html`~`p10.html`의 수학 사실·수치·앵커 링크를 보존하면서 유형별로 개편한다:
- **유도·증명·행렬식 계산(`ol.deriv` + 근거 주석 중심)**: P1(고윳값·고유공간), P2(중복 고윳값·기하중복도), P3(그람-슈미트 직교화), P4(대칭행렬 고윳값 분해), P5(3×3 행렬식), P6(직교 고유공간 증명), P9(대각화 가능 판정 및 $P, D$), P10(두 대칭행렬의 공통 고윳값 증명) — `solve`에서 답 구조 선제시 + `ol.deriv` 한 줄 한 연산 적용, `understand`·`recall`·`start` 중복·일상어 치환 정리.
- **반례/개념 판별 중심(경량 정리 + 필요 시 비교표)**: P7(대각화 가능성 vs 가역성), P8(대수적·기하적 중복도 판별) — 2×2 판정 비교표 또는 간결한 근거 구조로 정리.

- [ ] **Step 3: 미분 검사(해당 시), `build`, `check`, `ml-note-audit` 실행**

Run:
```powershell
python .claude/skills/ml-review-pack/scripts/check_vector_derivatives.py tmp/ml-problem-explain/revamp-1102/review-1102-PCA/explanations/*.html
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py build --run tmp/ml-problem-explain/revamp-1102
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py check --run tmp/ml-problem-explain/revamp-1102
```
Expected: 오류 없이 통과 (`check` exit 0). 이어서 `ml-note-audit` 절차로 `stage`와 `복습노트/1102/` 형제 자료(`정리노트_1102_PCA.html`, `복습문제_1102_PCA.html`) 간 설명 감사를 실행해 `<RUN>/audit.md`에 남기고, Critical·Important가 있으면 조각 수정 후 재 `build`·`check`한다.

- [ ] **Step 4: `review.json` 4단계 실제 검증 기록 및 `publish`**

1. `source_visual`, `content`, `independent`, `browser`(로컬 HTTP로 stage를 열어 Playwright 1280×900·1024×900·375×812, light/dark, 10문항 전체 `ol.deriv`/`table`/가로 넘침 0/KaTeX 오류 0/링크 확인)를 수행하고 `tmp/ml-problem-explain/revamp-1102/review-1102-PCA/review.json`을 `pass`로 갱신한다(참고한 저장소 파일 경로+SHA-256을 `references`에 기록).
2. Run: `python .claude/skills/ml-problem-explain/scripts/mpe_cli.py publish --run tmp/ml-problem-explain/revamp-1102`
Expected: `복습노트/1102/문제설명_1102_PCA.html` 및 `.pack/` 발행 완료, exit 0.

---

### Task 4 (Wave 2 병렬 B): `1104` 문제설명 HTML 업데이트 (10문항)

**Files:**
- Read-only inputs: `복습노트/1104/복습문제_1104_PCA_Part2.html`, `복습노트/1104/.pack/정리노트_1104_PCA_Part2.md`, `복습노트/1104/.pack/자료_문제설명_1104_PCA_Part2/fragments/p1.html`..`p10.html`, `복습노트/1104/.pack/자료_문제설명_1104_PCA_Part2/evidence/*`
- Working RUN: `tmp/ml-problem-explain/revamp-1104`
- Output (published by `mpe_cli.py publish`): `복습노트/1104/문제설명_1104_PCA_Part2.html`, `복습노트/1104/.pack/문제설명_1104_PCA_Part2.md`, `복습노트/1104/.pack/자료_문제설명_1104_PCA_Part2/*`

**Interfaces:**
- Consumes: Task 1의 `note-template.html`·`mpe_contract.py` 및 Task 2의 개정된 `authoring.md`·`verification.md`.
- Produces: 개정 서술 규칙이 적용되고 `mpe_cli.py publish`를 통과한 `1104` 산출물.

- [ ] **Step 1: 새 RUN으로 `extract` 실행 및 기존 `evidence` 복사**

Run:
```powershell
if (Test-Path "tmp/ml-problem-explain/revamp-1104") { Remove-Item -Recurse -Force "tmp/ml-problem-explain/revamp-1104" }
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py extract --repo . --target 1104 --run tmp/ml-problem-explain/revamp-1104
```
Expected: `extract: ...\revamp-1104\review-1104-PCA_Part2\source.json` 출력, exit 0. 기존 `evidence/*`를 RUN의 `evidence/`로 복사.

- [ ] **Step 2: 10문항(`p1`~`p10`)을 개정된 `authoring.md`에 따라 `explanations/pN.html`로 재저작**

- **그래프·해석형(경량 정리 + 비교표)**: P1(누적 설명 분산 그래프 읽기), P2(주성분 평면), P3(복원 오차와 주성분 개수) — `understand`·`recall` 압축, 수치 비교가 있는 경우 표로 정리.
- **수치·열 계산형(`<table>` + 답 구조 선제시)**: P5(영화 평점 행렬 랭크 2 근사 — 층별 Chandra 열과 실제 평점 비교표).
- **SVD·증명형(`ol.deriv` + 근거 주석)**: P4(가로로 긴 행렬의 SVD), P6(사영을 뺀 나머지도 사영일까 — `ol.deriv` + `(b)` 치환 대응표), P7(왼쪽 특이벡터부터 구하는 SVD), P8(2×2 SVD), P9(랭크 1 근사), P10(스펙트럼 노름/최대 신장 비율 증명).

- [ ] **Step 3: 미분 검사(해당 시), `build`, `check`, `ml-note-audit` 실행**

Run:
```powershell
python .claude/skills/ml-review-pack/scripts/check_vector_derivatives.py tmp/ml-problem-explain/revamp-1104/review-1104-PCA_Part2/explanations/*.html
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py build --run tmp/ml-problem-explain/revamp-1104
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py check --run tmp/ml-problem-explain/revamp-1104
```
Expected: `check` exit 0. `ml-note-audit`로 `복습노트/1104/` 형제 자료와 대조 후 Critical·Important 수정 및 재 `build`·`check`.

- [ ] **Step 4: `review.json` 4단계 실제 검증 기록 및 `publish`**

1. 10문항 전체 `source_visual`, `content`, `independent`, `browser`(1280×900·1024×900·375×812, light/dark, 그림·표·`ol.deriv` 넘침 0 확인) 검증 후 `review.json` 갱신.
2. Run: `python .claude/skills/ml-problem-explain/scripts/mpe_cli.py publish --run tmp/ml-problem-explain/revamp-1104`
Expected: `복습노트/1104/문제설명_1104_PCA_Part2.html` 및 `.pack/` 발행 완료, exit 0.

---

### Task 5 (Wave 2 병렬 C): `1111` 문제설명 HTML 업데이트 (8문항)

**Files:**
- Read-only inputs: `복습노트/1111/복습문제_1111_Gaussian_Mixture_Models.html`, `복습노트/1111/.pack/정리노트_1111_Gaussian_Mixture_Models.md`, `복습노트/1111/.pack/자료_문제설명_1111_Gaussian_Mixture_Models/fragments/p1.html`..`p8.html`, `복습노트/1111/.pack/자료_문제설명_1111_Gaussian_Mixture_Models/evidence/*`
- Working RUN: `tmp/ml-problem-explain/revamp-1111`
- Output (published by `mpe_cli.py publish`): `복습노트/1111/문제설명_1111_Gaussian_Mixture_Models.html`, `복습노트/1111/.pack/문제설명_1111_Gaussian_Mixture_Models.md`, `복습노트/1111/.pack/자료_문제설명_1111_Gaussian_Mixture_Models/*`

**Interfaces:**
- Consumes: Task 1의 `note-template.html`·`mpe_contract.py` 및 Task 2의 개정된 `authoring.md`·`verification.md`.
- Produces: 개정 서술 규칙이 적용되고 `mpe_cli.py publish`를 통과한 `1111` 산출물.

- [ ] **Step 1: 새 RUN으로 `extract` 실행 및 기존 `evidence` 복사**

Run:
```powershell
if (Test-Path "tmp/ml-problem-explain/revamp-1111") { Remove-Item -Recurse -Force "tmp/ml-problem-explain/revamp-1111" }
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py extract --repo . --target 1111 --run tmp/ml-problem-explain/revamp-1111
```
Expected: `extract: ...\revamp-1111\review-1111-Gaussian_Mixture_Models\source.json` 출력, exit 0. 기존 `evidence/*` 복사.

- [ ] **Step 2: 8문항(`p1`~`p8`)을 개정된 `authoring.md`에 따라 `explanations/pN.html`로 재저작**

- **확률·빈도·가중 밀도 계산형(`<table>` + 답 구조 선제시)**: P1(두 번 뽑은 동전 경우의 수·PMF 표), P2(빈도표 조건부확률), P4(두 상태 기댓값), P6(세 가우시안 혼합 밀도 성분별 비교표), P7(두 관측값의 책임도 — 가중 밀도 표 + 행 정규화 표 2단계 분리 및 `\overbrace` 공식 주석), P8(책임도 행렬 열 합 표).
- **유도·적분·그래프 판독형(`ol.deriv` 또는 경량 정리)**: P3(혼합 밀도 봉우리 읽기 — 경량 정리), P5(밀도에서 누적확률 적분 — `ol.deriv` 식·주석).

- [ ] **Step 3: 미분 검사(해당 시), `build`, `check`, `ml-note-audit` 실행**

Run:
```powershell
python .claude/skills/ml-review-pack/scripts/check_vector_derivatives.py tmp/ml-problem-explain/revamp-1111/review-1111-Gaussian_Mixture_Models/explanations/*.html
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py build --run tmp/ml-problem-explain/revamp-1111
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py check --run tmp/ml-problem-explain/revamp-1111
```
Expected: `check` exit 0. `ml-note-audit`로 `복습노트/1111/` 형제 자료와 대조 후 Critical·Important 수정 및 재 `build`·`check`.

- [ ] **Step 4: `review.json` 4단계 실제 검증 기록 및 `publish`**

1. 8문항 전체 `source_visual`, `content`, `independent`, `browser`(1280×900·1024×900·375×812, light/dark, 표·`ol.deriv`·그림 넘침 0 확인) 검증 후 `review.json` 갱신.
2. Run: `python .claude/skills/ml-problem-explain/scripts/mpe_cli.py publish --run tmp/ml-problem-explain/revamp-1111`
Expected: `복습노트/1111/문제설명_1111_Gaussian_Mixture_Models.html` 및 `.pack/` 발행 완료, exit 0.

---

### Task 6 (Wave 3): 전체 회귀 검증, 임시 RUN 정리 및 최종 커밋

**Files:**
- Verify: `복습노트/1102/문제설명_1102_PCA.html`, `복습노트/1104/문제설명_1104_PCA_Part2.html`, `복습노트/1111/문제설명_1111_Gaussian_Mixture_Models.html` 및 각각의 `.pack/*.md`
- Clean up: `tmp/ml-problem-explain/revamp-1102`, `revamp-1104`, `revamp-1111` (임시 작업 디렉터리)

**Interfaces:**
- Consumes: Task 1~5의 모든 변경 및 발행 산출물.
- Produces: 전체 pytest 통과 + 발행본 3종 최종 브라우저 검증 확인 + 깔끔한 git 커밋.

- [ ] **Step 1: 스킬 전체 테스트 스위트 재실행**

Run: `pytest .claude/skills/ml-problem-explain/tests -v`
Expected: ALL PASS

- [ ] **Step 2: 최종 발행본 3개(`1102`, `1104`, `1111`) 로컬 HTTP 브라우저 일괄 스모크 검증**

로컬 HTTP 서버로 저장소 루트를 띄운 뒤 Playwright로 3개 HTML을 열어(375×812 및 1280×900, light/dark) 첫 문항~마지막 문항 순회 시 콘솔 오류 0, `.katex-error` 0, `document.documentElement.scrollWidth <= innerWidth`, 모든 내부 `정리노트_*`/`복습문제_*` 앵커 링크 대상 파일·ID 존재 여부를 한 번에 재확인한다.

- [ ] **Step 3: 임시 `tmp/ml-problem-explain/revamp-*` 작업 폴더 정리 및 최종 상태 확인**

Run:
```powershell
Remove-Item -Recurse -Force tmp/ml-problem-explain/revamp-1102, tmp/ml-problem-explain/revamp-1104, tmp/ml-problem-explain/revamp-1111 -ErrorAction SilentlyContinue
git status --short
```

- [ ] **Step 4: Commit**

```powershell
git add 복습노트/1102 복습노트/1104 복습노트/1111
git commit -m "docs(notes): update 1102, 1104, 1111 problem explanations with visual-first authoring rules"
```
