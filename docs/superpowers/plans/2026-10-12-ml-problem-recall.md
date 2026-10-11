# 문제별 떠올릴 개념과 공식 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** ml-problem-explain의 모든 신규 해설과 기존 과제1 P1~P25에 입문형 ‘떠올릴 개념과 공식’ 구역을 추가한다.

**Architecture:** 기존 설명 조각 계약에 recall을 추가하고 조립/발행 흐름은 유지한다. 계약 검사와 HTML·MD 보존을 먼저 검증한 뒤 저장된 과제1 설명 조각에 교육 내용을 저작하고 새 RUN에서 재검토·발행한다. .agents는 .claude의 링크이므로 실제 파일은 .claude에서 수정한다.

**Tech Stack:** Python 3.10+, 표준 라이브러리 HTML parser/dataclasses/hashlib, pytest, 로컬 KaTeX·Pretendard, 실제 브라우저 화면 검증.

**Spec:** `docs/superpowers/specs/2026-10-12-ml-problem-recall-design.md` — 실행자는 이 문서와 설계를 함께 읽는다.

## Global Constraints

- Python 3.10 이상, 실행기는 표준 라이브러리만 사용한다.
- 문체는 `~해요` 체와 영어 전문용어 병기이다.
- 기존 원 HTML·MD·PDF·그림을 수정하지 않는다. 갱신 대상은 설명 소유 산출물이다.
- HTML과 짝인 MD를 함께 재생성하고 설명 조각을 보존한다.
- 기존 과제1 P1~P25 전체를 갱신한다. 다른 날짜의 기존 해설은 일괄 수정하지 않는다.
- 새 문제·PDF·영상은 생성하지 않는다.
- 실제 공식·기호·적용 조건은 자료 대조와 내용 검토로 확인한다. 구조 검사만으로 수학 검증을 주장하지 않는다.
- 1280×900/375×812, light/dark에서 확인한다. 콘솔·KaTeX 오류·누락 자원·문서 가로 넘침은 0이어야 한다.
- 자원은 동봉된 로컬 KaTeX/Pretendard를 쓰며 외부 요청이 없어야 한다.
- 수정한 조각은 새 build와 실제 재검토를 거쳐 publish한다. 기존 검토의 해시만 바꿔 승인하지 않는다.
- 기존 설명 산출물은 백업하고 교체 실패 시 복구한다.

## Review Focus

1. 기존 6구역 조각: 과거 조각을 그대로 재build할 때 recall 누락을 명확히 보고한다. 기존 발행 파일을 자동 변경하지 않는다. Task 1의 legacy 테스트.
2. 내용 없는 구역/잘못된 위치: 제목만 있는 recall이나 start 뒤로 옮긴 recall을 거부한다. Task 1의 body/order 테스트.
3. 혼합 소문항: 공통 개념과 소문항별 개념을 함께 다루고 solve/verify 표지 검사는 유지한다. Task 1의 소문항 회귀 테스트와 Task 3의 문항별 검토.
4. 긴 식과 한글·기호: HTML→MD 변환과 우측 요약 이동에서 내용이 사라지지 않고 모바일에서 잘리지 않는다. Task 2 보존 테스트와 Task 3 화면 검증.
5. 오래된 승인/수학 가정: recall 변경 후 예전 승인을 재사용하지 않으며 역행렬·공분산·사전 평균 조건을 잘못 일반화하지 않는다. Task 2 hash 테스트와 Task 3 자료 대조.

---

## 파일 구조와 실행 준비

| 파일 | 책임 |
|---|---|
| `.claude/skills/ml-problem-explain/SKILL.md` | 7구역 생성 절차와 입문형 요구 |
| `.claude/skills/ml-problem-explain/references/authoring.md` | recall 저작·예시·요약 지침 |
| `.claude/skills/ml-problem-explain/references/verification.md` | 단서/공식/기호/가정 내용 검토 |
| `.claude/skills/ml-problem-explain/scripts/mpe_contract.py` | 구역 집합·순서·recall 내용 검사 |
| `.claude/skills/ml-problem-explain/tests/helpers.py` | 신규 계약의 공용 테스트 조각 |
| `.claude/skills/ml-problem-explain/tests/test_contract.py` | 누락·중복·빈 내용·순서·검토 해시 회귀 |
| `.claude/skills/ml-problem-explain/tests/test_render.py` | 본문·요약·MD 보존 회귀 |
| `과제/과제1/자료_문제설명_hw1_Homework1/fragments/p1.html` ~ `p25.html` | 발행 후 문항별 저작 조각 |
| `과제/과제1/과제1_문제설명_Homework1.html/.md` | 재생성된 독자용 해설 |
| `tmp/ml-problem-explain/<고유ID>/homework-1-Homework1/` | 저작·근거·검토·stage·백업 |

실행 시 git status를 먼저 확인한다. 계획 작성 시 다른 작업의 speech-caption-audit 설계/계획과 tmp/가 untracked였으므로 일괄 git add나 정리를 하지 않는다. 코드는 격리 작업이 필요하면 using-git-worktrees로 준비하되, 과제 산출물의 최종 목적지는 사용자 원 저장소다. 격리 checkout에 원 자료가 없으면 복사/권한 범위를 확인하고 원 저장소 산출물을 누락하지 않도록 최종 반영한다. 커밋은 아래 명시한 파일만 선택한다.

### Task 1: 필수 recall 계약과 저작 규칙

**Files:** Modify 위 파일 표의 SKILL.md, authoring.md, verification.md, mpe_contract.py, helpers.py, test_contract.py.

**Interfaces:**
- Consumes: `helpers.problem() -> Problem`, `helpers.fragment(p=None) -> str`; `Problem.subparts: tuple[str, ...]`; `mpe_shared.parse(str) -> Node`, `Node.children`, `Node.tag`, `Node.text()`.
- Produces: 기존 `validate_fragment(problem: Problem, fragment: str) -> list[str]` 서명을 유지하며 `KEYS = ('understand', 'recall', 'start', 'solve', 'verify', 'pitfall', 'retry')`를 적용한다.

- [x] **Step 1: 다음 실패 테스트를 test_contract.py에 추가한다.**

```python
RECALL = ('<div class="layer formal" data-explanation="recall">'
          '<h4>이 문제를 봤을 때 떠올릴 개념과 공식</h4>'
          '<p>제곱을 구하라는 단서에서 같은 수의 곱을 떠올려요. '
          '$A^2=A\\cdot A$이며 A는 주어진 스칼라예요.</p></div>')

def with_recall():
    text = fragment()
    if 'data-explanation="recall"' not in text:
        text = text.replace('<div class="layer formal" data-explanation="start">',
                            RECALL + '<div class="layer formal" data-explanation="start">')
    return text

def test_recall_required_and_legacy_fragment_refused():
    text = with_recall()
    assert validate_fragment(problem(), text) == []
    root = __import__('mpe_shared').parse(text)
    node = next(root.find_all(lambda n: n.attrs.get('data-explanation') == 'recall'))
    from mpe_shared import outer
    assert validate_fragment(problem(), text.replace(outer(node), ''))

def test_recall_duplicate_empty_and_wrong_order_refused():
    from mpe_shared import parse, outer
    text = with_recall()
    node = next(parse(text).find_all(lambda n: n.attrs.get('data-explanation') == 'recall'))
    block = outer(node)
    assert validate_fragment(problem(), text + block)
    empty = '<div class="layer formal" data-explanation="recall"><h4>개념</h4></div>'
    assert any('recall' in e for e in validate_fragment(problem(), text.replace(block, empty)))
    wrong = text.replace(block, '').replace('<div class="layer formal" data-explanation="solve">',
                                           block + '<div class="layer formal" data-explanation="solve">')
    assert any('순서' in e for e in validate_fragment(problem(), wrong))
```

- [x] **Step 2: 실패를 확인한다.**

```powershell
python -m pytest .claude/skills/ml-problem-explain/tests/test_contract.py -q
```

기대: 신규 7구역 조각이 현재 여섯 구역 계약에 거부되어 FAIL. 실패 이유가 import/환경 오류이면 계약 실패와 구분해 먼저 해결한다.

- [x] **Step 3: helpers.fragment에 RECALL 내용을 understand 다음에 넣고 계약 코드를 변경한다.**

`mpe_contract.py`의 KEYS와 구역 집합 오류 메시지를 바꾼다. 기존 Counter 검사를 유지하고 다음 코드를 sections/counts 검사 이후 추가한다.

```python
    if tuple(n.attrs['data-explanation'] for n in sections) != KEYS:
        errors.append('설명 구역 순서는 understand/recall/start/solve/verify/pitfall/retry여야 해요')
    for node in sections:
        if node.attrs['data-explanation'] == 'recall':
            body = ''.join(child.text() if isinstance(child, Node) else child
                           for child in node.children
                           if not isinstance(child, Node) or child.tag not in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'))
            if not body.strip():
                errors.append('recall: 제목 외에 단서·개념·공식·적용 조건 설명이 필요해요')
```

내용 검사 메시지는 저작 요구를 안내한다. 자동 검사로 의미/공식의 정확성을 판단하거나 키워드 개수로 pass를 주지 않는다. 기존 직계 layer/소문항/금지 태그 검사를 그대로 유지한다.

- [x] **Step 4: SKILL.md의 ‘여섯 구역’을 ‘일곱 구역’으로 바꾸고 authoring.md에 다음 행과 예시를 추가한다.**

```markdown
| recall | 문제의 단서 → 개념의 뜻 → 공식과 기호 → 적용 조건과 선택 이유. `layer formal` |
```

```html
<div class="layer formal" data-explanation="recall">
  <h4>이 문제를 봤을 때 떠올릴 개념과 공식</h4>
  <p>‘전치’라는 말에서 전치(transpose), 즉 행과 열의 교환을 떠올려요.</p>
  <p>$(A^\top)_{ij}=A_{ji}$예요. $i$는 행, $j$는 열 번호이고, $m\times n$ 행렬의 전치는 $n\times m$이에요.</p>
  <p>직사각형 행렬과 열벡터에도 적용돼요. 원소의 값과 부호는 그대로 두고 위치만 바꿔요.</p>
</div>
```

authoring.md에 공통/소문항별 개념 구분, 정성 문제의 정의·판단 기준, start와의 역할 차이, `summary-group` 요약을 명시한다. verification.md content 검토에 단서 연결·기호·공식·적용 가정·소문항별 누락 여부를 추가한다.

- [x] **Step 5: 기존 소문항 검사와 전체 suite가 통과하는지 확인하고 명시 파일만 커밋한다.**

```powershell
python -m pytest .claude/skills/ml-problem-explain/tests -q
git add .claude/skills/ml-problem-explain/SKILL.md .claude/skills/ml-problem-explain/references/authoring.md .claude/skills/ml-problem-explain/references/verification.md .claude/skills/ml-problem-explain/scripts/mpe_contract.py .claude/skills/ml-problem-explain/tests/helpers.py .claude/skills/ml-problem-explain/tests/test_contract.py
git commit -m "feat: require concept recall in problem explanations"
```

기대: legacy 제외한 신규 조각 PASS, recall 뒤에서도 solve/verify의 누락·중복 소문항은 FAIL. 기존 test_all_subparts_must_be_solved_and_verified가 이 회귀를 검증한다.

### Task 2: 본문·MD·요약 보존과 승인 무효화

**Files:** Modify `.claude/skills/ml-problem-explain/tests/test_render.py`, `tests/test_contract.py`; 필요한 경우만 `scripts/mpe_render.py`의 convert_markdown. 템플릿 변경은 화면에서 실제 오류가 확인되는 경우에 한한다.

**Interfaces:**
- Consumes: `build_explanation(pack: SourcePack, fragments: dict[str,str], stage: Path, repo: Path) -> Artifacts`, `check_artifacts(pack, artifacts) -> list[str]`, `validate_reviews(pack, fragments, reviews) -> list[str]`.
- Produces: 동일한 HTML/MD 경로·manifest 형식과 API. 신규 recall/요약 텍스트와 LaTeX가 두 출력에 남고 변경 후 옛 review는 거부된다.

- [x] **Step 1: test_render.py에 보존 테스트를 추가한다.**

```python
def test_recall_and_summary_survive_html_and_markdown(tmp_path):
    pack = load_source(ROOT / '과제/과제1/과제1_Homework1.html', ROOT)
    pack = replace(pack, problems=pack.problems[:1])
    p = pack.problems[0]
    text = fragment(p).replace('<div class="sum" hidden>',
        '<div class="sum" hidden><div class="summary-group">'
        '<h4>떠올릴 개념·공식</h4><p>전치의 크기는 $n\\times m$이에요.</p></div>')
    result = build_explanation(pack, {p.id: text}, tmp_path / 'stage', ROOT)
    assert check_artifacts(pack, result) == []
    html = result.html.read_text(encoding='utf-8')
    md = result.md.read_text(encoding='utf-8')
    node = next(parse(html).find_all(lambda n: n.attrs.get('data-explanation') == 'recall'))
    assert 'hidden' not in node.attrs
    for output in (html, md):
        assert '이 문제를 봤을 때 떠올릴 개념과 공식' in output
        assert '떠올릴 개념·공식' in output
        assert '$n\\times m$' in output
    assert 'A\\cdot A' in md
```

- [x] **Step 2: test_contract.py에 실제 recall만 바꾼 오래된 검토 거부 테스트를 추가한다.**

```python
def test_recall_edit_invalidates_approval():
    before = fragment()
    changed = before.replace('제곱을 구하라는 단서', '곱셈을 요구하는 단서')
    assert changed != before
    assert validate_reviews(pack(), {'p1': changed}, reviews())
```

- [x] **Step 3: 두 테스트를 실행하고 실패할 때만 변환 코드를 고친다.**

```powershell
python -m pytest .claude/skills/ml-problem-explain/tests/test_render.py .claude/skills/ml-problem-explain/tests/test_contract.py -q
```

기존 renderer가 임의 layer와 summary를 보존하므로 첫 실행부터 PASS일 수 있다. 구현을 억지로 추가하지 않는다. FAIL이면 parse 결과의 main/recall/sum과 MD를 대조해 누락 지점을 찾아 수정하고, 회귀 전체가 통과한 후 진행한다.

- [x] **Step 4: 선택 파일만 커밋한다.**

```powershell
git add .claude/skills/ml-problem-explain/tests/test_render.py .claude/skills/ml-problem-explain/tests/test_contract.py
git commit -m "test: preserve recall content and invalidate stale reviews"
```

실제로 renderer를 수정했으면 해당 파일도 명시적으로 stage한다.

### Task 3: 과제1 25문항 내용 저작·검토·발행

**Files:** RUN의 `explanations/p1.html` ~ `p25.html`, `evidence/`, `review.json`; 최종 `과제/과제1/과제1_문제설명_Homework1.html`, `.md`, `자료_문제설명_hw1_Homework1/`, `figures_문제설명_hw1_Homework1/`의 설명 소유 산출물.

**Interfaces:**
- Consumes: 새 7구역 계약; 기존 발행 `자료_문제설명_hw1_Homework1/fragments/`; CLI `extract/build/check/publish --run`; `load_run(run) -> list[dict]`, `load_fragments(item) -> dict[str,str]`, `load_artifacts(item) -> Artifacts`.
- Produces: P1~P25의 recall 본문과 요약이 포함된 HTML·MD·조각, 실제 검토 기록, 백업 경로. 원 과제 카드/PDF는 보존한다.

- [x] **Step 1: 새 고유 RUN을 extract하고 기존 조각을 복사한다.**

```powershell
python --version
$recallRun = 'tmp/ml-problem-explain/hw1-recall-' + [guid]::NewGuid().ToString('N')
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py extract --repo . --target 과제1 --run $recallRun
Copy-Item -LiteralPath '과제/과제1/자료_문제설명_hw1_Homework1/fragments' -Destination ($recallRun + '/baseline-fragments') -Recurse
Get-ChildItem -LiteralPath ($recallRun + '/baseline-fragments') -Filter '*.html' | Copy-Item -Destination ($recallRun + '/homework-1-Homework1/explanations')
$recallOriginalHashes = @{}
Get-ChildItem -LiteralPath '과제/과제1' -File -Recurse | Where-Object { $_.FullName -notmatch '문제설명' } | ForEach-Object {
    $recallOriginalHashes[$_.FullName] = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
}
$recallOriginalHashes | ConvertTo-Json | Set-Content -LiteralPath ($recallRun + '/homework-1-Homework1/evidence/original-hashes.json') -Encoding utf8
```

extract 종료 코드가 0이 아니면 의존 명령을 실행하지 않는다. `source.json`의 25문항/모든 subparts를 읽고, 원 자료의 SHA-256과 읽은 경로를 evidence에 남긴다. baseline-fragments는 비교용이며 수정하지 않는다.

- [x] **Step 2: 기존 조각으로 build를 실행해 recall 누락으로 거부되는지 확인한다.**

```powershell
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py build --run $recallRun
```

기대: exit 1, recall/일곱 구역 오류. 실제 발행 파일은 바뀌지 않는다.

- [x] **Step 3: 자료를 읽고 아래 저작 범위대로 문항별 recall을 작성한다.**

원 자료: `과제/과제1/26_10_Introduction_to_Machine_Learning_homework1_rev.pdf`, `과제1_Homework1-문제.pdf`, `과제1_Homework1-답안.pdf`, `교과서/Mathematics_for_Machine_Learning.pdf`, 관련 Lecture03/04 및 기존 정리노트. 답안은 참고이며 독립 검산을 대체하지 않는다. PDF 열람은 pdf 스킬을 적용한다. 아래 식은 선정 지침이며 실제 원문의 기호/분산/규제 정의에 맞춰 대조한다.

| 문항 | 단서와 떠올릴 개념·식 | 반드시 확인할 조건 |
|---|---|---|
| P1 | 전치: $(A^\top)_{ij}=A_{ji}$ | 행·열 크기 교환, 원소 값 불변 |
| P2 | 내적 $x^\top y=\sum_i x_i y_i$, 노름 $\sqrt{x^\top x}$, 직교 | 같은 차원, 유클리드 내적 |
| P3 | $(AB)_{ij}=\sum_k A_{ik}B_{kj}$ | 안쪽 차원과 곱 순서 |
| P4 | 2×2 행렬식 $ad-bc$, 여인수 전개 | 원문의 행렬 크기에 맞는 방법 |
| P5 | $A^{-1}$, $AA^{-1}=I$ | 정방행렬, 행렬식 0 아님 |
| P6 | 선형 독립: $\sum_i c_i v_i=0$의 해 | 자명해만 있는지, 열 rank |
| P7 | 선형결합 $Vc=b$ | 해의 존재와 유일성 구분 |
| P8 | Gram 행렬 $A^\top A$ | 역행렬은 A의 열이 독립일 때 |
| P9 | 특징 행렬 $\Phi$, 예측 $\Phi\theta$ | 행은 관측, 열은 특징, 절편 여부 |
| P10 | gradient $\nabla f$ | 스칼라 출력, 각 편미분에서 상수 |
| P11 | Jacobian $J_{ij}=\partial f_i/\partial x_j$ | 출력/입력 차원과 행·열 방향 |
| P12 | $\nabla(x^\top Ax)=(A+A^\top)x$ | 대칭일 때만 $2Ax$, 정류점/극값 구분 |
| P13 | 다변량 가우시안의 정규화 계수와 이차형식 | 공분산의 양의 정부호, 차원 d=2 |
| P14 | 완전제곱과 가우시안 적분 | 적분 변수, 이차항 계수 부호 |
| P15 | 독립 관측의 우도 $\prod_n p(y_n\mid x_n,\theta)$ | 조건부 독립, 잡음 분산 |
| P16 | 로그 곱→합, NLL→제곱오차 | theta에 무관한 상수만 제거 |
| P17 | $\Phi^\top\Phi\theta=\Phi^\top y$ | 역행렬 표현의 full column rank |
| P18 | 베이즈 규칙, 가우시안 사전→이차 벌점 | 잡음/사전 분산에 따른 lambda, 절편 규제 |
| P19 | ML 목적과 MAP 목적의 수치 비교 | 같은 데이터와 원문 규제 정의 |
| P20 | 열 중복, null space, $\Phi^\top\Phi+\lambda I$ | lambda>0, 규제 범위 |
| P21 | 평균과 외적 공분산 | 원문이 지정한 분모 4, N−1로 바꾸지 않음 |
| P22 | $E[Ax+b]=A\mu+b$, $\operatorname{Cov}(Ax+b)=A\Sigma A^\top$ | b는 결정적 상수, 차원 |
| P23 | 절편 없는 회귀의 ML/MAP | 설계에 절편 열 추가 금지 |
| P24 | 공통 평균 ML/MAP, 정밀도 가중 평균 | 사전 평균 1, 0 중심 벌점으로 바꾸지 않음 |
| P25 | 가우시안 곱의 완전제곱, 정밀도 합 | 분산 양수, 비례식과 정규화된 밀도 구분 |

각 문항 저작은 독립적인 2~5분 체크 단위로 진행하고 자료 대조 시간이 더 필요하면 읽기/저작을 나눈다. `understand` 다음에 recall을 삽입한다. sum 내부에 다음 구조의 개념 요약을 문항별로 작성한다.

```html
<div class="summary-group">
  <h4>떠올릴 개념·공식</h4>
  <p>전치는 행과 열을 교환해요. $(A^\top)_{ij}=A_{ji}$이고 크기는 $m\times n\to n\times m$이에요.</p>
</div>
```

P1 예시는 Task 1의 recall 본문을 사용한다. 다른 문항도 표의 단서·식·조건을 모두 문장으로 연결하고 기호를 정의한다. solve/verify/원문은 임의로 다시 쓰지 않는다. 기존 답 오류를 발견하면 독립 검토 근거를 남기고 disputed로 보류한다.

- [x] **Step 4: 문항별 내용 대조 기록을 작성한다.**

RUN evidence에 `recall-content-review.md`를 만든다. 각 P번호 아래 `단서`, `개념·공식 및 기호`, `적용 조건`, `소문항 커버리지`, `원 자료 파일과 실제 페이지`, `start와 중복 여부`를 기록한다. P8/P17의 rank, P18의 lambda/절편, P21의 분모, P24의 사전 평균, P25의 정규화는 명시적으로 확인한다. 먼저 기록할 결론을 정해 놓거나 자료를 읽지 않고 페이지 번호를 채우지 않는다.

- [x] **Step 5: build/check 및 전체 회귀를 실행한다.**

```powershell
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py build --run $recallRun
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py check --run $recallRun
python -m pytest .claude/skills/ml-problem-explain/tests -q
```

각 exit 0을 확인한다. build가 출력한 stage.json에서 실제 산출 경로를 읽는다. 임의 stage ID를 추정하지 않는다.

- [x] **Step 6: 아래 스크립트를 RUN/evidence/check_recall.py로 저장하고 stage를 검사한다.**

```python
import sys
from pathlib import Path
repo = Path.cwd()
sys.path.insert(0, str(repo / '.claude/skills/ml-problem-explain/scripts'))
from mpe_cli import load_run, load_fragments, load_artifacts
from mpe_contract import validate_fragment
from mpe_shared import parse
item = load_run(Path(sys.argv[1]))[0]
fragments = load_fragments(item)
artifacts = load_artifacts(item)
assert set(fragments) == {f'p{i}' for i in range(1, 26)}
for problem in item['pack'].problems:
    assert validate_fragment(problem, fragments[problem.id]) == []
html = artifacts.html.read_text(encoding='utf-8')
md = artifacts.md.read_text(encoding='utf-8')
nodes = list(parse(html).find_all(lambda n: n.attrs.get('data-explanation') == 'recall'))
assert len(nodes) == 25
assert md.count('#### 이 문제를 봤을 때 떠올릴 개념과 공식') == 25
assert md.count('떠올릴 개념·공식') == 25
assert all('hidden' not in n.attrs for n in nodes)
print('PASS: 25 recall sections, markdown and summary coverage')
```

```powershell
python ($recallRun + '/homework-1-Homework1/evidence/check_recall.py') $recallRun
```

검사 스크립트/결과를 stage에 포함하려면 근거 작성 완료 후 다시 build/check한다. 새 build는 승인을 초기화하므로 화면/내용/독립 검토는 최종 build 이후에 수행한다.

- [x] **Step 7: 실제 브라우저와 수학 검토를 수행한다.**

각 1280×900/375×812 × light/dark에서 P1~P25를 목차와 이전/다음으로 열고 recall의 위치·읽기·수식, 우측 개념 요약, 요약 너비 변경, 그림·링크를 확인한다. P13/P18/P25의 긴 식과 P1의 행렬을 집중 확인한다. 브라우저 도구는 실행 시 사용 가능한 도구의 문서에 따라 선택한다. 실제 화면·콘솔·요청/자원·가로 넘침 검사 결과를 RUN evidence에 남긴다. 고정 레이아웃 변경 없이 해결하려면 긴 식을 의미 단위로 나눈다. 조각을 바꾸면 Step 5부터 반복한다.

최종 stage에 대해 source_visual/content/independent/browser를 실제 수행한 결과만 review.json에 기록한다. 기존 independent-results는 보조 자료로 읽을 수 있으나 기존 status를 복사하지 않고 모든 문항/소문항을 재검토한다. content와 independent의 items는 source.json의 정확한 subpart 집합을 사용한다. references에 실제 읽은 파일의 절대 path/hash를 기록한다. 이 절차의 구체적 JSON 형식은 `.claude/skills/ml-problem-explain/references/verification.md`를 따른다.

- [x] **Step 8: 최종 check/publish와 보존 확인을 수행한다.**

```powershell
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py check --run $recallRun
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py publish --run $recallRun
foreach ($recallOriginalPath in $recallOriginalHashes.Keys) {
    if ((Get-FileHash -LiteralPath $recallOriginalPath -Algorithm SHA256).Hash -ne $recallOriginalHashes[$recallOriginalPath]) {
        throw ('원 자료 변경: ' + $recallOriginalPath)
    }
}
```

검토 실패·hash 불일치·자료 충돌이면 발행하지 않고 이유를 보고한다. 성공 시 백업 경로가 존재하는지 확인하고 원 카드/PDF/MD/그림 해시를 Step 1의 기록과 대조한다. 발행된 HTML/MD에서 recall 25개와 개념 요약 25개를 다시 확인한다. 실제 HTML을 Codex 패널로 열고 HTML·MD·백업 경로를 사용자에게 링크한다.

- [x] **Step 9: 산출물 변경을 선택해 커밋한다.**

```powershell
git add '과제/과제1/과제1_문제설명_Homework1.html' '과제/과제1/과제1_문제설명_Homework1.md' '과제/과제1/자료_문제설명_hw1_Homework1'
if (Test-Path -LiteralPath '과제/과제1/figures_문제설명_hw1_Homework1') {
    git add '과제/과제1/figures_문제설명_hw1_Homework1'
}
git commit -m "docs: add concept recall to homework one explanations"
```

## 계획 자체 검토

- 설계의 필수 구역·순서·본문·요약·깊이·25문항·원문 보존·검토·백업을 Task 1~3에 대응했다.
- 기존 함수명/타입과 CLI를 실제 파일에서 확인했다. 새 데이터 모델/CLI 명령은 도입하지 않는다.
- Review Focus 1~3은 계약 테스트/문항 검토, 4는 변환 테스트/화면 검증, 5는 승인 무효화 테스트/자료 대조로 확인한다.
- 사용자가 Native 실행을 선택했다. 2026-10-12 구현·검토·발행 완료: 회귀57, 소문항 독립검산50, 공식/보존63, 화면100 및 요약 패널 조절 통과. Task 1/2는 같은 계약의 변경으로 한 커밋에 묶고, 최종 검토의 빈 본문 검사 보완은 별도 커밋으로 기록했다.
