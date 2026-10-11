# 머신러닝기초 문제풀이 입문 설명 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 복습문제·과제 카드를 보존하면서 첫 줄부터 이유·완성 답·검산까지 설명하는 로컬 스킬을 만든다.

**Architecture:** 독립 스킬이 기존 저장 HTML을 읽고 설명 조각을 저작한 뒤 노트형 HTML·MD를 조립한다. 기존 파서·MD 변환·복구 가능한 파일 발행은 좁은 어댑터로 재사용하며, 설명 규칙·UI 템플릿·검증 기록은 새 스킬이 소유한다. `ml-review-pack` 및 논회실 파일은 수정하지 않는다.

**Tech Stack:** 기존 Python 환경, 표준 라이브러리/dataclasses/html.parser/hashlib, pytest, 기존 review_pdf_cards/html2md/review_pdf_publish, 로컬 KaTeX·Pretendard, 브라우저 검증. Python 3.10 이상(기존 코드의 union annotation 요구).

**Spec:** `docs/superpowers/specs/2026-10-11-ml-problem-explain-design.md`. 구현자는 이 문서와 설계를 모두 읽는다. 과제 지원은 사용자 확정 사항이다.

## Global Constraints

- 기존 복습문제와 과제를 모두 지원한다.
- 문항 ID, 번호, 순서, 제목, 조건, 질문, 그림, 모든 소문항을 유지한다.
- 본문 풀이를 details/hidden으로 감추지 않는다.
- 원 HTML/PDF/MD/그림을 수정하거나 삭제하지 않는다.
- 읽음 상태 키는 `ml-problem-explain-<profile>-<range>-<slug>`이다.
- 수식 오류, 깨진 자원, 콘솔 오류, 문서 가로 넘침은 0이어야 한다.
- 단순 구조 검사를 답 검증 통과로 취급하지 않는다.
- 새 문제·PDF·영상·자동 채점은 생성하지 않는다. PDF만 있는 과제는 카드 HTML 준비가 필요하다고 보고한다.
- 이번 계획 작성 단계에서는 구현·실제 학습자료 생성·커밋을 실행하지 않는다. 아래 커밋은 구현 단계의 검증 후 체크포인트다.

## Review Focus

1. 구형 카드에 conditions/ask가 없음: 해시 일치 레이아웃으로 보존 추출, 오래된 레이아웃은 실패 — Task 1.
2. 과제의 여러 소문항·영문 행렬: 원문 전문 보존과 소문항별 설명 누락 탐지 — Tasks 1, 2.
3. 날짜 범위·같은 날짜 여러 slug·NFD 경로: 후보를 합치거나 임의 선택하지 않음 — Task 1.
4. 긴 행렬·SVG ID 충돌·외부 CDN 실패: 수식 영역과 로컬 자원으로 렌더링, 중복 ID는 거부 — Tasks 3, 5.
5. 검토 기록의 해시가 오래됨·교체 실패·동시 발행: 발행 거부 또는 복구하며 원자료 유지 — Task 4.

---

## 파일 지도

새 디렉터리 `.claude/skills/ml-problem-explain/`를 이하 `SKILL`로 표기한다. 저장소 루트에서 명령을 실행한다.

| 파일 | 책임 |
|---|---|
| `SKILL/SKILL.md` | 호출과 실행 절차 |
| `SKILL/references/authoring.md` | 여섯 설명 구역과 수학 저작 |
| `SKILL/references/verification.md` | 의미/독립 답/화면 검토 기록 |
| `SKILL/scripts/mpe_types.py` | 불변 입력 타입과 오류 |
| `SKILL/scripts/mpe_shared.py` | 기존 스킬 API 어댑터 |
| `SKILL/scripts/mpe_source.py` | 대상 선택·추출·입력 해시 |
| `SKILL/scripts/mpe_contract.py` | 저작 조각 및 검토 기록 검사 |
| `SKILL/scripts/mpe_render.py` | 노트 템플릿 조립·그림 복사·MD |
| `SKILL/scripts/mpe_publish.py` | 최종 게이트·소유 파일만 발행 |
| `SKILL/scripts/mpe_cli.py` | extract/build/check/publish 명령 |
| `SKILL/assets/note-template.html` | 복사한 노트 UI |
| `SKILL/assets/vendor/` | KaTeX·Pretendard와 라이선스·SHA 목록 |
| `SKILL/tests/conftest.py` | scripts 경로와 임시 fixture |
| `SKILL/tests/test_source.py` | 선택·구형/과제 보존 |
| `SKILL/tests/test_contract.py` | 설명 누락·검토 기록 |
| `SKILL/tests/test_render.py` | 원문·수식·MD·ID·자원 |
| `SKILL/tests/test_publish.py` | 게이트·복구·보존 |
| `SKILL/tests/test_cli.py` | 전 흐름과 종료 상태 |
| `.agents/skills/ml-problem-explain` | 새 스킬의 상대 심볼릭 링크 |
| `README.md` | 복습문제·과제 호출 예시 |

## 공통 계약

```python
# mpe_types.py
from dataclasses import dataclass
from pathlib import Path

class ExplainError(ValueError):
    pass

@dataclass(frozen=True)
class Problem:
    id: str
    number: int
    title: str
    source: str
    original_html: str
    conditions_html: str
    ask_html: str
    figures_html: tuple[str, ...]
    reference_steps: tuple[str, ...]
    reference_answer: str
    subparts: tuple[str, ...]

@dataclass(frozen=True)
class SourcePack:
    profile: str
    range: str
    slug: str
    path: Path
    sha256: str
    problems: tuple[Problem, ...]

@dataclass(frozen=True)
class Artifacts:
    html: Path
    md: Path
    manifest: Path
    files: tuple[Path, ...]  # stage 아래 소유 파일 전체; 발행 전 상대 경로 검사
```

`subparts`는 최상위 ask `<ol>`의 각 직계 `<li>`에 대응하는 `a,b,c,...`이며 없으면 `("main",)`이다. 문자 표지가 있으면 그 표지를 사용하고, 없으면 순서로 부여한다. 중복 표지와 질문 목록·원문 표지 불일치는 오류다. 저작 문서는 한국어로 작성한다.

### Task 1: 복습·과제 대상 선택과 보존 추출

**Files:** Create `SKILL/scripts/mpe_types.py`, `mpe_shared.py`, `mpe_source.py`, `SKILL/tests/conftest.py`, `test_source.py`.

**Interfaces:**
- Consumes: 기존 `read_cards(path, profile)`, `normalize_cards(pack, layouts, source_path)`, `parse/inner/outer/media_nodes`, `REVIEW/HOMEWORK`.
- Produces: `resolve_sources(repo: Path, target: str | None) -> tuple[Path, ...]`, `load_source(path: Path, repo: Path) -> SourcePack`, `sha256(path: Path) -> str`.

- [ ] **Step 1: 실패 테스트 작성.** `conftest.py`는 `Path(__file__).resolve().parents[1] / "scripts"`를 sys.path에 추가한다. 다음 핵심 fixture를 `test_source.py`에 둔다.

```python
from pathlib import Path
import pytest
from mpe_source import load_source, resolve_sources
from mpe_types import ExplainError

ROOT = Path(__file__).resolve().parents[4]

def test_real_homework_preserves_all_cards():
    source = ROOT / "과제/과제1/과제1_Homework1.html"
    before = source.read_bytes()
    pack = load_source(source, ROOT)
    assert pack.profile == "homework"
    assert [p.id for p in pack.problems] == [f"p{i}" for i in range(1, 26)]
    assert all(p.original_html and p.reference_answer for p in pack.problems)
    assert source.read_bytes() == before

def test_duplicate_date_requires_explicit_path(tmp_path):
    folder = tmp_path / "복습노트/1007"
    folder.mkdir(parents=True)
    for slug in ("First", "Second"):
        (folder / f"복습문제_1007_{slug}.html").write_text("", encoding="utf-8")
    with pytest.raises(ExplainError, match="여러 후보"):
        resolve_sources(tmp_path, "1007")

def test_legacy_real_review_uses_verified_layout():
    pack = load_source(ROOT / "복습노트/0909/복습문제_0909_Data_Models_Learning.html", ROOT)
    assert pack.problems[0].conditions_html
    assert "f(10)" in pack.problems[0].ask_html
```

- [ ] **Step 2:** Run `python -m pytest .claude/skills/ml-problem-explain/tests/test_source.py -q`; expected import failure before implementation.
- [ ] **Step 3: API 재사용와 해시 검사 구현.** Existing scripts 위치는 `Path(__file__).resolve().parents[2] / "ml-review-pack/scripts"`로 구한다. `mpe_shared.py`에서 한 번만 sys.path를 추가하고 정확히 위 API를 export한다. `load_source`의 core는 아래 순서로 작성한다.

```python
raw = path.read_bytes()
profile = HOMEWORK if path.name.startswith("과제") else REVIEW
pack = read_cards(path, profile)
layout_path = repo / "workbook/layouts" / f"{pack.range}_{pack.slug}.json"
layouts = None
if any('class="conditions"' not in c.statement_html or 'class="ask"' not in c.statement_html for c in pack.cards):
    if not layout_path.is_file():
        raise ExplainError("조건/질문 분리 자료 없음: " + str(layout_path))
    layouts = json.loads(layout_path.read_text(encoding="utf-8"))
normalized = normalize_cards(pack, layouts, path)
```

`normalized`에서 Problem을 만들고 `figures_html`은 원 카드의 `figures[].html`을 유지한다. subparts는 HTMLParser 노드의 최상위 질문 목록을 순회한다. 입력 중첩 목록의 li는 별도 소문항으로 세지 않는다. `sha256`은 `hashlib.sha256(path.read_bytes()).hexdigest()`이다. 기존 parser 예외를 ExplainError로 바꾸되 원 문항 ID를 유지한다.

`resolve_sources`는 Path.rglob로 카드 파일명만 모으고 NFC 이름으로 비교한다. target 절대경로는 프로필 파일명인지 검사한다. `과제N`은 해당 과제 폴더에서만 검색한다. 날짜 범위는 MMDD를 date(2000,month,day)로 검증하고 시작>끝은 거부한다. 인자 없으면 가장 큰 파일명 종료 날짜를 고른다. 후보가 0개면 `대상 없음`, 한 날짜/과제에 2개 이상이면 `여러 후보`와 경로 목록을 반환하는 예외를 낸다. 통합/개별 날짜 팩이 겹치는 경우도 같은 예외다.

- [ ] **Step 4: 예외 테스트 추가.** 위 duplicate fixture에 `unicodedata.normalize("NFD", "복습노트")`를 사용한 테스트를 추가해 1개 후보를 찾는지 확인한다. 임시 저장소에 실제 0909 HTML과 레이아웃을 복사하고 레이아웃 `source_sha256="0"*64`로 바꾼 뒤 `load_source`가 `stale layout source`로 실패하는지 검사한다. 1007 최신 카드의 모든 conditions/ask와 매핑의 원문 텍스트가 보존되는지 비교한다. 없는 과제와 날짜 `1330`도 오류여야 한다.
- [ ] **Step 5:** Run source 테스트; expected PASS. `git add .claude/skills/ml-problem-explain/scripts/mpe_types.py .claude/skills/ml-problem-explain/scripts/mpe_shared.py .claude/skills/ml-problem-explain/scripts/mpe_source.py .claude/skills/ml-problem-explain/tests`; `git commit -m "feat: extract review and homework explanation sources"`.

### Task 2: 설명 저작과 문항별 검토 계약

**Files:** Create `SKILL/scripts/mpe_contract.py`, `SKILL/references/authoring.md`, `verification.md`, `SKILL/tests/test_contract.py`.

**Interfaces:**
- Consumes: SourcePack/Problem, `mpe_shared.parse`.
- Produces: `validate_fragment(problem: Problem, fragment: str) -> list[str]`, `validate_reviews(pack: SourcePack, fragments: dict[str,str], reviews: dict) -> list[str]`, `payload_hash(pack: SourcePack, fragments: dict[str,str]) -> str`.

- [ ] **Step 1: 실패 테스트.** 검산이라는 제목만으로 의미 검토가 통과하지 않게 한다. 구조는 기계 검사, 내용과 답은 근거가 있는 검토 기록으로 구분한다.

```python
from dataclasses import replace
from mpe_contract import validate_fragment, validate_reviews
from pathlib import Path
from mpe_types import Problem, SourcePack

def problem():
    return Problem("p1", 1, "행렬", "HW1 Problem 1", "", "", "", (), (), "", ("a", "b"))

def fragment():
    return ''.join(f'<div class="layer formal" data-explanation="{key}"><p>설명</p></div>'
        for key in ("understand", "start", "solve", "verify", "pitfall")) + \
        '<div class="layer warn" data-explanation="retry"><ul><li>다시 계산해요.</li></ul></div>' + \
        '<div class="sum" hidden>시작·판단·검산</div>'

def test_every_subpart_needs_explicit_solution():
    errors = validate_fragment(problem(), fragment())
    assert any("소문항" in error for error in errors)

def test_cannot_publish_without_independent_review():
    pack = SourcePack("homework", "1", "Homework1", Path("과제1_Homework1.html"), "0"*64, (problem(),))
    assert validate_reviews(pack, {"p1": fragment()}, {})
```

- [ ] **Step 2:** Run `python -m pytest .claude/skills/ml-problem-explain/tests/test_contract.py -q`; expected import failure.
- [ ] **Step 3: 여섯 구역과 소문항 검사를 구현.** 구역당 data-explanation 1개와 비어 있지 않은 텍스트를 요구한다. solve와 verify 각각에 `data-subpart="a"` 등 모든 `problem.subparts`가 정확히 1번 있어야 한다. retry는 li 1~3개다. summary는 topic 직계 자식 1개만 `hidden` 허용; 나머지 hidden/details, script/style/iframe, on* 속성, javascript URL은 거부한다. SVG 정의의 로컬 fragment는 허용한다.

```python
KEYS = ("understand", "start", "solve", "verify", "pitfall", "retry")
def payload_hash(pack, fragments):
    payload = {"source_sha256": pack.sha256, "fragments": fragments}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode("utf-8")).hexdigest()
```

검토 JSON는 `input_hash`, `source_visual`, `content`, `independent`, `browser`를 가진다. 처음은 전부 `not_run`; pass를 생성기가 자동 채우지 않는다. 각 검토의 status=pass, reviewer, evidence를 필수로 하고, content와 independent는 모든 문항/소문항 key(`p1:a` 등)를 포함해야 한다. independent는 각 key마다 method=`exact|symbolic|numerical|proof|qualitative`, 결론, 근거 파일/자료 위치를 기록한다. numerical은 tolerance와 잔차도 기록한다. source_visual은 과제 PDF 또는 MML 확인 페이지를 남긴다. input_hash는 현재 입력·조각 hash와 같아야 한다. not_run/fail/disputed 상태는 발행 불가.

- [ ] **Step 4: 저작 문서 작성.** authoring.md는 설계의 여섯 구역을 위 data-explanation 마크업에 연결하고 solve/verify에 소문항 표지를 예제로 명시한다. MML/교안 근거, 첫 식, 식 변형 이유, 차원·정규화·미분 가정, 완성 답, 실질 검산, 흔한 오류, 1~3개 재풀이, summary 재사용을 요구한다. verification.md는 구조와 의미 승인 분리, 실제 리뷰 기록, 답 충돌 보고, 수업 밖 보충 표기를 규정한다.
- [ ] **Step 5: 통과 fixture를 추가.** solve/verify 각각에 a,b 표지를 넣어 errors=[] 확인; b 제거 시 실패; duplicate a와 펼친 풀이에 hidden/details를 넣어 실패; payload_hash를 바꾼 뒤 이전 검토 기록이 실패하는지 검사한다. method=proof에 숫자 검사만 있는 evidence는 승인하지 않는 수동 검토 예시도 verification.md에 기록한다.
- [ ] **Step 6:** Run contract 테스트; expected PASS. `git add .claude/skills/ml-problem-explain/scripts/mpe_contract.py .claude/skills/ml-problem-explain/references .claude/skills/ml-problem-explain/tests/test_contract.py`; `git commit -m "feat: define complete problem explanation and review contract"`.

### Task 3: 노트형 HTML·MD와 로컬 자원 조립

**Files:** Create `SKILL/scripts/mpe_render.py`, `SKILL/assets/note-template.html`, `SKILL/assets/vendor/`, `SKILL/tests/test_render.py`.

**Interfaces:**
- Consumes: SourcePack, `validate_fragment`, `payload_hash`, 기존 html2md `Ctx/convert/check_md`.
- Produces: `build_explanation(pack: SourcePack, fragments: dict[str,str], stage: Path, repo: Path) -> Artifacts`, `check_artifacts(pack: SourcePack, artifacts: Artifacts) -> list[str]`.

- [ ] **Step 1: 실패 테스트를 작성.** real 1007의 첫 문항만 `dataclasses.replace(pack, problems=pack.problems[:1])`로 고른 fixture에 Task 2의 완전한 main 또는 a/b/c 설명을 공급한다. build가 `문제설명_1007_Product_of_Gaussians.html/.md`를 만들고 원본 hash가 유지되는지 assert한다. HTML의 각 topic 원문 노드와 입력 conditions/ask 텍스트·TeX·표·그림을 비교하는 테스트를 추가한다.
- [ ] **Step 2:** Run `python -m pytest .claude/skills/ml-problem-explain/tests/test_render.py -q`; expected import failure.
- [ ] **Step 3: 기존 노트 템플릿을 복사하고 조립.** 원본 `.claude/skills/ml-review-pack/assets/note-template.html`을 복사한다. 날짜 range 대신 분리된 읽음 key를 넣고, TOC는 문항별 anchor, title/brand는 문제설명으로 설정한다. 모든 슬롯 치환 후 미치환 슬롯은 실패. templates source의 현재 SHA를 provenance JSON에 기록한다. CDN URL 4개는 vendor 상대경로로 치환한다. repo의 기존 `.claude/skills/ml-review-pack` 또는 `.agents` 스킬 자원에 vendor가 없으면 공식 패키지의 해당 버전 파일을 가져와 라이선스·SHA를 동봉한다. KaTeX CSS의 모든 fonts URL도 동봉하고 시험한다.

```python
prefix = f"과제{pack.range}_문제설명" if pack.profile == "homework" else f"문제설명_{pack.range}"
stem = f"{prefix}_{pack.slug}"
key = f"ml-problem-explain-{pack.profile}-{pack.range}-{pack.slug}"
articles = []
for p in pack.problems:
    reading = (f'<div class="layer formal" data-source-problem="{p.id}">'
        f'<h4>주어진 조건</h4>{p.conditions_html}<h4>구할 것</h4>{p.ask_html}'
        + ''.join(p.figures_html) + '</div>')
    if pack.profile == "homework":
        reading += '<div class="layer formal"><h4>과제 원문</h4>' + p.original_html + '</div>'
    articles.append(f'<article class="topic" id="{p.id}"><h3>{html.escape(p.title)}</h3>'
        + reading + fragments[p.id] + '</article>')
```

파서에서 정규화가 제거한 그림은 figures_html로 다시 붙인다. 이미지 URL은 입력 HTML 기준으로 resolve하고 repo 내부 실제 파일만 별도 자산 폴더로 복사한다. percent-encoded/NFD 경로를 지원하고 경로 누락·탈출은 실패. inline SVG ID와 해당 `url(#...)`/href는 문항 prefix로 재작성하며 중복 원 ID는 실패한다. 개념 링크는 존재하는 노트 anchor만 허용하고 원 문제는 같은 문항 anchor로 연결한다. 모든 파일은 stage에서만 쓴다.

```python
ctx = Ctx(link_map={html_path.name: md_path.name}, fig_dir_abs=fig_dir,
          fig_dir_name=fig_dir.name, prefix="explain-")
convert(html_path, md_path, ctx, "문제의 첫 줄부터 검산까지 설명해요.")
```

`check_md(html_path, md_path) -> list[str]`를 check_artifacts 오류에 합친다. convert_pack은 파일명·문서쌍 전용이므로 호출하지 않는다. manifest에는 profile/range/slug, source 경로/hash, 읽음 key, 문항·소문항 목록, fragments hash, 생성된 상대 파일 목록을 기록한다.

- [ ] **Step 4: 오류·보존 테스트 추가.** HOMEWORK 단일 문항의 영어 원문 행렬을 HTML/MD 모두 비교, duplicate SVG ID 거부, 누락 이미지 실패, vendor CSS 모든 참조 파일 존재, 본문 details 없음, 읽음 key 격리, 모든 문항 anchor MD 보존을 검사한다. local vendor 요청만 허용하는 브라우저 시험은 Task 5에 연결한다.
- [ ] **Step 5:** Run render 테스트; expected PASS. `git add .claude/skills/ml-problem-explain/scripts/mpe_render.py .claude/skills/ml-problem-explain/assets .claude/skills/ml-problem-explain/tests/test_render.py`; `git commit -m "feat: render standalone review and homework explanation notes"`.

### Task 4: 발행 게이트·백업·복구

**Files:** Create `SKILL/scripts/mpe_publish.py`, `SKILL/tests/test_publish.py`; extend `mpe_shared.py` to export `publish_files`.

**Interfaces:**
- Consumes: `validate_reviews`, `check_artifacts`, `sha256`, 기존 `publish_files(staged, backup_dir)`.
- Produces: `publish_explanation(pack: SourcePack, artifacts: Artifacts, fragments: dict[str,str], reviews: dict, destination: Path, backup_dir: Path) -> tuple[Path,...]`.

- [ ] **Step 1: 실패 테스트.** 입력 원본과 기존 설명의 bytes를 저장하고 reviews={}로 publish하면 ExplainError가 나고 양쪽 bytes가 유지되어야 한다. artifacts.files에 `../원본.html`을 넣으면 경로 오류가 나야 한다.
- [ ] **Step 2:** Run `python -m pytest .claude/skills/ml-problem-explain/tests/test_publish.py -q`; expected import failure.
- [ ] **Step 3: 게이트와 파일 매핑 구현.**

```python
if sha256(pack.path) != pack.sha256:
    raise ExplainError("입력 변경: 설명을 다시 검증하세요")
errors = check_artifacts(pack, artifacts) + validate_reviews(pack, fragments, reviews)
if errors:
    raise ExplainError("발행 보류: " + " / ".join(errors))
stage_root = artifacts.html.parent.resolve()
mapping = {}
for src in artifacts.files:
    relative = src.resolve().relative_to(stage_root)
    dst = destination / relative
    if dst.resolve() == pack.path.resolve():
        raise ExplainError("원본 덮어쓰기 금지")
    mapping[dst] = src
publish_files(mapping, backup_dir)
return tuple(mapping)
```

파일 목록은 manifest 소유 접두사(설명 stem/자산/자료 폴더)와 일치해야 한다. 기존 그림이나 기존 입력과 같은 경로는 거부한다. symlink ancestor를 검사하고 백업은 고유 RUN 아래 둔다. validation.json을 쓰기 전에 source/fragments/생성 파일 hash를 최종 검토한다. 검토 보고 hash와 생성 파일 hash도 바뀌었으면 발행을 거부한다. publish_files의 lock/backup/rollback 구현을 새로 복제하지 않는다.

- [ ] **Step 4: 복구 테스트.** 임시 폴더의 기존 HTML/MD 두 개를 발행할 때 `review_pdf_publish._replace_copy`를 monkeypatch해 두 번째 교체에서 한 번 OSError를 발생시킨다(복구 호출은 성공시키는 count 조건 사용). HTML/MD가 모두 이전 bytes로 돌아오고 새로운 파일이 남지 않는지 확인한다. 입력 변경, 조각 변경, stage 파일 변경, 실패한 browser 검토, 겹치는 lock을 각각 시험한다. 기존 원 문제/노트/PDF의 전체 hash 집합이 successful publication 전후 같아야 한다.
- [ ] **Step 5:** Run publish 테스트; expected PASS. `git add .claude/skills/ml-problem-explain/scripts/mpe_publish.py .claude/skills/ml-problem-explain/scripts/mpe_shared.py .claude/skills/ml-problem-explain/tests/test_publish.py`; `git commit -m "feat: gate explanation publishing with backup and rollback"`.

### Task 5: 실행 명령·스킬 등록·사용 검증

**Files:** Create `SKILL/scripts/mpe_cli.py`, `SKILL/SKILL.md`, `SKILL/tests/test_cli.py`; create `.agents/skills/ml-problem-explain` link; modify `README.md` by appending usage.

**Interfaces:**
- Consumes: Tasks 1–4 public functions.
- Produces: `main(argv: list[str] | None = None) -> int` with extract/build/check/publish subcommands. Exit 0=성공, 1=검사/입력 실패. stdout은 경로와 단계, stderr는 오류와 문항 ID.

- [ ] **Step 1: CLI 실패 테스트.** subprocess로 존재하지 않는 과제 source를 extract하면 code=1, `대상 없음`을 확인한다. manifest로 export/import한 SourcePack과 원본 load_source의 문항 필드가 일치하는지 시험한다. `publish`를 review 없이 실행하면 기존 파일이 그대로이고 code=1인지 확인한다.
- [ ] **Step 2:** Run `python -m pytest .claude/skills/ml-problem-explain/tests/test_cli.py -q`; expected missing CLI failure.
- [ ] **Step 3: argparse command dispatch를 구현.**

```python
ap = argparse.ArgumentParser()
commands = ap.add_subparsers(dest="command", required=True)
extract = commands.add_parser("extract")
extract.add_argument("--repo", type=Path, required=True)
extract.add_argument("--target")
extract.add_argument("--run", type=Path, required=True)
for name in ("build", "check", "publish"):
    command = commands.add_parser(name)
    command.add_argument("--run", type=Path, required=True)
args = ap.parse_args(argv)
```

extract는 비어 있지 않은 RUN을 거부하고 대상별 디렉터리에 source.json(Problem 모든 필드), source hash, 참고풀이, subparts를 기록한다. build는 각 대상의 `explanations/<pid>.html`을 읽고 stage에 Artifacts를 만든다. check는 기계검사 결과를 machine report로 기록하며 검토 status를 pass로 바꾸지 않는다. publish는 각 대상 review.json을 검사해 destination으로 발행한다. target별 독립 성공/실패를 보고하고 하나라도 실패하면 전체 종료 1이다. JSON에 문자열 Path를 복원할 때 절대 path와 repository root, symlink를 검증한다.

- [ ] **Step 4: 스킬 절차 작성.** SKILL.md frontmatter name=`ml-problem-explain`, description에 복습문제/과제 문제해설·입문 풀이 설명 및 날짜·과제번호 호출을 명시한다. 본문은 extract → reference 확인 → 여섯 구역 저작 → 독립 검증 → build/check → browser review → publish → 링크/백업/보류 보고를 요구한다. 자동으로 실제 복습노트나 과제를 생성하는 것은 구현 완료 조건이 아니다. 아래 명령 예시는 literal 경로로 기입하고 Python PATH 확인 절차를 둔다.

```powershell
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py extract --repo . --target 과제1 --run tmp/ml-problem-explain/hw1-first
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py build --run tmp/ml-problem-explain/hw1-first
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py check --run tmp/ml-problem-explain/hw1-first
python .claude/skills/ml-problem-explain/scripts/mpe_cli.py publish --run tmp/ml-problem-explain/hw1-first
```

build 전에 에이전트가 설명 조각을 저작하고, publish 전에 실제 자료 대조와 브라우저 확인으로 검토 기록을 확정한다. README에는 명령만 실행해도 설명이 자동 저작되는 것으로 오해하지 않도록 이 단계를 명시한다.

- [ ] **Step 5: 로컬 등록.** PowerShell `New-Item -ItemType SymbolicLink -Path .agents/skills/ml-problem-explain -Target ../../.claude/skills/ml-problem-explain`로 기존 관례를 따른다. existing path는 덮어쓰지 않고 검사한다. 권한으로 symlink 생성이 안 되면 원본을 보존해 제한을 보고하고, 중복 복사로 두 스킬을 독립 관리하지 않는다. 링크 경유 SKILL.md 읽기와 resolve 결과를 시험한다.
- [ ] **Step 6: 실제 브라우저 점검.** 1007 복습문제와 과제1에서 각각 단일 문항을 고른 임시 fixture 설명을 작성해 stage에 조립한다. `python -m http.server 8765 --directory tmp/ml-problem-explain/browser-proof`를 숨겨진 프로세스로 실행한다(포트 사용 시 빈 포트). 브라우저 도구로 1280×900/375×812 두 테마를 확인하고 외부 네트워크를 끊어도 로컬 KaTeX·폰트·그림이 표시되는지 본다. 임시 결과는 공개 폴더로 발행하지 않는다.

페이지마다 console errors, `.katex-error` count, `document.documentElement.scrollWidth <= innerWidth`, 이미지 naturalWidth, 목차/이전/다음, `.sum`에서 우측으로 이동한 내용, 처음/마지막 문항, 긴 수식 영역의 scroll 동작을 기록한다. 실패는 Task 3 템플릿/렌더로 고치고 browser report를 현재 hash에 맞춰 다시 생성한다. screenshots와 근거를 browser 리뷰에 남기고 서버를 종료한다.

- [ ] **Step 7:** Run `python -m pytest .claude/skills/ml-problem-explain/tests -q` and `python -m pytest .claude/skills/ml-review-pack/tests tests/test_homework1_cards.py tests/test_homework1_answers.py -q`; 새 스킬·기존 스킬 regressions 모두 PASS. `git diff --check`와 기존 복습노트/과제/논회실 변경 없음 확인. README에 호출·입력 카드 필요·산출 위치·발행 보류 조건을 append.
- [ ] **Step 8:** `git add .claude/skills/ml-problem-explain .agents/skills/ml-problem-explain README.md`; `git commit -m "feat: register ML problem explanation skill for reviews and homework"`.

## 완료 판단과 실행 인계

새 스킬 등록, 두 입력 프로필의 fixture 전체 흐름, 원문·소문항 보존, 독립 검토 게이트, 오프라인 브라우저 점검, rollback 검증과 기존 테스트 통과가 완료 기준이다. 실제 모든 날짜·과제의 설명 생성은 별도 사용자 호출로 수행한다.

추천 실행 방식은 Native: 다섯 작업이 같은 SourcePack과 기존 파서에 연결되고, 새 외부 서비스가 없어서 동일 구현자가 순차적으로 처리하기 좋다. 구현 종료 후 독립 리뷰 한 번으로 전체 흐름을 확인한다. 사용자에게 계획 검토와 Native/Subagent-driven 선택을 요청한 뒤 구현을 시작한다.

## 계획 자체 검토

- 설계 범위 → Task 1/5; 설명 구역·수학·모든 소문항 → Task 2; HTML/MD/UI/자원 → Task 3/5; 보존·실패·백업 → Task 4.
- 공개 함수의 타입은 공통 계약과 각 task Interfaces에 고정했다.
- Review Focus 다섯 항목은 각각 지정한 task의 테스트/화면 검사에 연결했다.
- 실제 답 검증은 구조 검사에 포함하지 않고, 문항별 근거 검토를 발행 게이트로 두었다.
