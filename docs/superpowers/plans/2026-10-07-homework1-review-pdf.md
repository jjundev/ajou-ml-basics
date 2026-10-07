# 과제1 복습문제 양식 PDF Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 과제1의 Problem 1–25를 복습문제 카드 HTML로 옮기고, 기존 PDF 빌더로 `과제/과제1/과제1_Homework1-문제.pdf`·`-답안.pdf` 쌍을 만든다.

**Architecture:** `ml-review-pack` PDF 빌더에 `CardProfile`(review/homework)을 도입해 파일명·출처 규칙, kind 배지, 제목, 출력 파일명을 프로필에서 받는다. 템플릿은 그대로다. 정답은 repo 관례(`scripts/review_answers.py`)대로 Fraction 정답 키 `scripts/homework1_answers.py`가 계산하고, 카드의 `.answer` TeX 토큰과 대조한다. 그 전에 Windows 체크아웃에서 빌더가 import조차 안 되는 문제(fcntl, CRLF)를 고친다.

**Tech Stack:** Python 3 표준 라이브러리(`fractions`, `unittest`), PyMuPDF(`fitz`), Playwright + 설치된 Google Chrome(`channel='chrome'`), KaTeX(템플릿 내장 CDN).

**Spec:** `docs/superpowers/specs/2026-10-07-homework1-review-pdf-design.md`

## Global Constraints
- 실행 환경: Windows 11, Git Bash. 명령은 `python`(not `python3`). 테스트는 `python -m unittest`(pytest 아님 — skill 테스트는 `_util` 경로 주입 방식).
- 경로 약속: `S=.claude/skills/ml-review-pack` (repo 루트 기준 상대 경로). 모든 명령은 repo 루트에서 실행.
- 템플릿 세 개(`$S/assets/pdf-problem.html`, `pdf-answer.html`, `pdf-video-16x9.css`)는 수정 금지. SHA는 `$S/assets/pdf-template-provenance.json` 값 그대로: problem `1ddb009d…bdc7`, answer `557b30b2…1b06`, video `d5665853…d870`.
- `review` 프로필의 기본 동작·에러 메시지·출력 파일명은 바이트 단위로 불변. 기존 테스트 전부 통과.
- 레이아웃: `video-16x9` (1440×810pt, 하단 135pt 자막 여백).
- 과제 파일명 규칙: 카드 HTML `과제<N>_<Slug>.html`, 출처 `HW<N> Problem <k>`(카드 id `p<k>`와 번호 일치), 배지 `과제`, 제목 `머신러닝기초 과제<N>`, PDF `과제<N>_<Slug>-문제.pdf`/`-답안.pdf`.
- 이번 산출물: `과제/과제1/과제1_Homework1.html` → `과제/과제1/과제1_Homework1-문제.pdf`, `과제1_Homework1-답안.pdf`.
- 카드 문장: 토스처럼 짧고 다정한 "~해요" 체, 이모지·장식 기호 금지. 조건·질문은 한국어, `details.original`은 영어 원문 전문.
- 수식: `$…$`, `$$…$$`만. TeX 안의 `&`는 HTML에서 `&amp;`로 쓰고 `<`,`>` 금지(`\lt`,`\gt`). 벡터 `\mathbf{x}`, 행렬 `\mathbf{A}`, 파라미터 `\boldsymbol{\theta}`, 특징행렬 `\boldsymbol{\Phi}`, 전치 `^\top`.
- 정답 TeX 규약(대조기와 맞물림): 정수는 그대로, 분수는 `\frac{p}{q}`(음수는 `-\frac{p}{q}`), 행렬·벡터는 `\begin{bmatrix}…\end{bmatrix}`(열벡터는 원소마다 `\\`). 대조 시 HTML 엔티티를 풀고 모든 공백을 지운다.
- 새 스크립트는 표준 라이브러리만(sympy 등 추가 의존성 금지).
- 커밋: Conventional Commits, 메시지 끝에 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. 푸시는 하지 않는다.

## Review Focus
- 긴 카드(P17, P22의 세 소문항, P25)는 `(계속)` 페이지로 나뉘어도 자막대(하단 135pt)를 침범하면 안 된다 → Task 7의 빌드 검증(`_verify_pdf`)과 전체 페이지 PNG 검수로 고정.
- 카드 id와 출처 번호가 어긋난 경우(`p7`에 `HW1 Problem 8`, 또는 과제 번호 불일치 `HW2`) → 조용히 잘못된 머리글을 찍지 말고 빌드가 거부해야 한다 → Task 2 `test_homework_source_must_match_card_and_number`.
- 프로필을 빠뜨린 실행(`--profile` 없이 과제 HTML 빌드) → `invalid review filename`으로 즉시 실패해야 한다 → Task 2 `test_default_profile_is_review`.
- 문제지 PDF에 정답이 새면 안 된다 → Task 3 `test_homework_profile_build`의 `ANSWER_ONLY_SENTINEL` 부재 검사.
- macOS에서 클론해 NFD 파일명이 된 `과제1_…html`도 읽혀야 한다 → Task 2 `test_nfd_filename`.

---

### Task 1: Windows에서 PDF 빌더 실행 가능하게 하기

현재 Windows 체크아웃에서 skill 테스트 111개 중 failures 2·errors 6. 원인은 (1) `review_pdf_publish.py`의 `import fcntl`(POSIX 전용) → `build_review_pdf.py`·`assemble.py` import 실패, (2) `core.autocrlf=true`로 HTML/CSS/JSON이 CRLF로 체크아웃되어 템플릿 SHA와 레이아웃 `source_sha256`가 어긋남.

**Files:**
- Create: `.gitattributes`
- Modify: `.claude/skills/ml-review-pack/scripts/review_pdf_publish.py:7` (import), `:17-27` (`publication_lock`)
- Modify: `.claude/skills/ml-review-pack/scripts/review_pdf_render.py:40` (`read_text()` 인코딩 명시)
- Test: 기존 `$S/tests/test_review_pdf_publish.py`(잠금 테스트 포함), 전체 skill 스위트

**Interfaces:**
- Consumes: 없음
- Produces: Windows에서 import 가능한 `review_pdf_publish.publish_files(staged, backup_dir)`, `publication_lock(destinations)` — 시그니처 불변

- [ ] **Step 1: 실패 확인 (RED)**

Run: `python -m unittest discover -s .claude/skills/ml-review-pack/tests 2>&1 | tail -3`
Expected: `FAILED (failures=2, errors=6, skipped=2)` — `No module named 'fcntl'`, `test_templates_unchanged` SHA 불일치, `stale layout source`.

- [ ] **Step 2: LF 고정 `.gitattributes` 추가 후 작업 트리 재체크아웃**

작업 트리가 깨끗한지 먼저 확인한다(비어 있지 않으면 중단하고 보고).
```bash
git status --porcelain
printf '* text=auto eol=lf\n' > .gitattributes
git add .gitattributes
git add --renormalize .
git status --porcelain
```
Expected: 마지막 출력은 `A  .gitattributes` 한 줄뿐(블롭은 이미 LF). 그다음 추적 텍스트 파일을 LF로 다시 꺼낸다.
```bash
git ls-files -z -- '*.html' '*.css' '*.json' '*.js' '*.md' '*.py' '*.svg' | xargs -0 rm -f
git checkout -- .
git ls-files --eol -- .claude/skills/ml-review-pack/assets/pdf-problem.html
```
Expected: `i/lf    w/lf    attr/text=auto eol=lf …`, 그리고 `git status --porcelain`은 여전히 `A  .gitattributes`만.

- [ ] **Step 3: 잠금에 Windows 분기 추가**

`review_pdf_publish.py`의 `import fcntl` 줄을 다음으로 바꾼다.
```python
try:
    import fcntl
except ImportError:  # Windows: msvcrt byte-range lock, released when the handle closes
    fcntl=None
    import msvcrt
```
`publication_lock` 위에 헬퍼를 추가한다.
```python
def _try_lock(stream):
    if fcntl:fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB);return
    stream.seek(0)
    try:msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
    except OSError as e:raise BlockingIOError(str(e)) from e
```
`publication_lock` 안의 `try:fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)`를 `try:_try_lock(stream)`으로 바꾼다(except 절 `BlockingIOError` 그대로).

`review_pdf_render.py:40`의 `(ASSETS/'pdf-problem.html').read_text()`를 `(ASSETS/'pdf-problem.html').read_text(encoding='utf-8')`로 바꾼다.

- [ ] **Step 4: 전체 스위트 통과 확인 (GREEN)**

Run: `python -m unittest discover -s .claude/skills/ml-review-pack/tests 2>&1 | tail -3` 그리고 `python -m unittest discover -s tests 2>&1 | tail -3`
Expected: 둘 다 `OK` (skill: `Ran 111 tests … OK (skipped=2)`, root: `Ran 47 tests … OK (skipped=22)`). `test_review_pdf_publish`의 `locked` 테스트가 Windows 분기로 통과해야 한다.

- [ ] **Step 5: Commit**
```bash
git add .gitattributes .claude/skills/ml-review-pack/scripts/review_pdf_publish.py .claude/skills/ml-review-pack/scripts/review_pdf_render.py
git commit -m "fix(ml-review): run review PDF builder on Windows checkouts" -m "Pin LF line endings so template provenance hashes match, and fall back to msvcrt locking where fcntl is unavailable." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: `CardProfile`과 프로필별 카드 읽기

**Files:**
- Modify: `.claude/skills/ml-review-pack/scripts/review_pdf_types.py` (`ReviewPack` 앞에 `CardProfile`, `REVIEW`, `HOMEWORK`, `PROFILES` 추가; `ReviewPack`에 `profile` 필드)
- Modify: `.claude/skills/ml-review-pack/scripts/review_pdf_cards.py:55-84` (`read_cards`)
- Create: `.claude/skills/ml-review-pack/tests/fixtures/pdf/과제9_Pdf_Test.html`
- Test: `.claude/skills/ml-review-pack/tests/test_review_pdf_cards.py`

**Interfaces:**
- Consumes: 없음
- Produces:
  - `CardProfile(name: str, filename_re: str, source_re: str, kind_label: str | None, title_fmt: str, stem_fmt: str, source_fmt: str | None)`; 메서드 `kind(source: str) -> str`, `expected_source(range_: str, card_id: str) -> str | None`
  - 상수 `REVIEW`, `HOMEWORK`, `PROFILES: dict[str, CardProfile]` (`{'review': REVIEW, 'homework': HOMEWORK}`)
  - `ReviewPack.profile: CardProfile = REVIEW`
  - `read_cards(path: Path, profile: CardProfile = REVIEW) -> ReviewPack`

- [ ] **Step 1: 과제 fixture 작성**

`.claude/skills/ml-review-pack/tests/fixtures/pdf/과제9_Pdf_Test.html` (기존 `복습문제_0101_Pdf_Test.html`과 같고 출처만 다름):
```html
<section id="hw9">
<article class="card" id="p1" data-source="HW9 Problem 1"><h3>P1. 한글 수식</h3><div class="problem"><div class="conditions">조건 $a=1$ &amp; $b=5$.</div><div class="ask">$a/b$를 구하세요.</div></div><details class="original"><summary>원문</summary>Find the ratio.</details><details class="hint"><summary>힌트</summary>나눗셈.</details><details class="solution"><summary>풀이</summary><ol class="steps"><li>첫 단계 $a/b$.</li><li>둘째 단계 $1/5$.</li></ol><p class="answer">정답 $\frac{1}{5}$ ANSWER_ONLY_SENTINEL</p></details></article>
<article class="card" id="p2" data-source="HW9 Problem 2"><h3>P2. 표</h3><div class="problem"><div class="conditions">표를 이용하세요.<table><tr><th>x</th><th>y</th></tr><tr><td>1</td><td>2</td></tr></table></div><div class="ask">합은?</div></div><details class="original"><summary>원문</summary>Find the sum.</details><details class="hint"><summary>힌트</summary>더해요.</details><details class="solution"><summary>풀이</summary><ol class="steps"><li>1과 2.</li><li>합은 3.</li></ol><p class="answer">3</p></details></article>
</section>
```

- [ ] **Step 2: 실패하는 테스트 작성**

`test_review_pdf_cards.py` 상단 import에 `import unicodedata`와 `from review_pdf_types import HOMEWORK, REVIEW`를 추가하고, `SOURCE` 아래에 `HW_SOURCE = FIXTURES / 'pdf/과제9_Pdf_Test.html'`를 두고 파일 끝에 클래스를 추가한다.
```python
class TestHomeworkProfile(unittest.TestCase):
    def write(self, d, text, name=HW_SOURCE.name):
        p=Path(d)/name;p.write_text(text,encoding='utf-8');return p
    def test_reads_homework_pack(self):
        pack=read_cards(HW_SOURCE,HOMEWORK)
        self.assertEqual((pack.range,pack.slug),('9','Pdf_Test'))
        self.assertIs(pack.profile,HOMEWORK)
        self.assertEqual([c.source for c in pack.cards],['HW9 Problem 1','HW9 Problem 2'])
    def test_default_profile_is_review(self):
        self.assertIs(read_cards(SOURCE).profile,REVIEW)
        with self.assertRaisesRegex(ReviewPdfError,'invalid review filename'):read_cards(HW_SOURCE)
    def test_homework_rejects_mml_source(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.write(d,HW_SOURCE.read_text(encoding='utf-8').replace('HW9 Problem 1','MML Example 9.1'))
            with self.assertRaisesRegex(ReviewPdfError,'p1: invalid source'):read_cards(p,HOMEWORK)
    def test_homework_source_must_match_card_and_number(self):
        for wrong in ('HW9 Problem 2','HW8 Problem 1'):
            with self.subTest(wrong=wrong),tempfile.TemporaryDirectory() as d:
                p=self.write(d,HW_SOURCE.read_text(encoding='utf-8').replace('data-source="HW9 Problem 1"',f'data-source="{wrong}"'))
                with self.assertRaisesRegex(ReviewPdfError,'p1: source'):read_cards(p,HOMEWORK)
    def test_nfd_filename(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.write(d,HW_SOURCE.read_text(encoding='utf-8'),unicodedata.normalize('NFD',HW_SOURCE.name))
            self.assertEqual(read_cards(p,HOMEWORK).range,'9')
    def test_profile_helpers(self):
        self.assertEqual(REVIEW.kind('MML Example 9.1'),'예제')
        self.assertEqual(REVIEW.kind('MML Exercise 6.1'),'연습문제')
        self.assertEqual(HOMEWORK.kind('HW1 Problem 7'),'과제')
        self.assertIsNone(REVIEW.expected_source('0909','p3'))
        self.assertEqual(HOMEWORK.expected_source('1','p7'),'HW1 Problem 7')
        self.assertEqual(HOMEWORK.stem_fmt.format(range='1',slug='Homework1'),'과제1_Homework1')
        self.assertEqual(HOMEWORK.title_fmt.format(range='1'),'머신러닝기초 과제1')
```

- [ ] **Step 3: RED 확인**

Run: `python -m unittest discover -s .claude/skills/ml-review-pack/tests -p 'test_review_pdf_cards.py' -v`
Expected: `ImportError: cannot import name 'HOMEWORK' from 'review_pdf_types'`.

- [ ] **Step 4: `review_pdf_types.py`에 프로필 추가**

`class ReviewPack` 바로 위에 추가한다(파일의 압축된 스타일 유지).
```python
@dataclass(frozen=True)
class CardProfile:
    """Naming and labeling rules for one kind of card source (review pack, homework)."""
    name: str
    filename_re: str  # groups: (range, slug)
    source_re: str
    kind_label: str | None  # None: derive 예제/연습문제 from source
    title_fmt: str  # .format(range=…)
    stem_fmt: str  # .format(range=…, slug=…)
    source_fmt: str | None = None  # exact source per card: .format(range=…, n=…)
    def kind(self, source: str) -> str:
        return self.kind_label or ('예제' if ' Example ' in source else '연습문제')
    def expected_source(self, range_: str, card_id: str) -> str | None:
        return self.source_fmt.format(range=range_, n=card_id[1:]) if self.source_fmt else None
REVIEW = CardProfile('review', r'복습문제_(\d{4}(?:-\d{4})?)_([A-Za-z0-9_]+)\.html', r'MML (Example|Exercise) \d+(?:\.\d+)+', None, '머신러닝기초 복습문제 {range}', '복습문제_{range}_{slug}')
HOMEWORK = CardProfile('homework', r'과제(\d+)_([A-Za-z0-9_]+)\.html', r'HW\d+ Problem \d+', '과제', '머신러닝기초 과제{range}', '과제{range}_{slug}', 'HW{range} Problem {n}')
PROFILES = {p.name: p for p in (REVIEW, HOMEWORK)}
```
`ReviewPack`의 마지막 필드 `source_path: Path | None = None` 아래에 `profile: CardProfile = REVIEW`를 추가한다.

- [ ] **Step 5: `read_cards`를 프로필로 일반화**

`review_pdf_cards.py`의 import에 `CardProfile, REVIEW`를 추가한다(`from review_pdf_types import …` 줄). `read_cards`를 다음처럼 바꾼다(나머지 본문 불변).
```python
def read_cards(path: Path, profile: CardProfile = REVIEW) -> ReviewPack:
    path=Path(path)
    m=re.fullmatch(profile.filename_re,unicodedata.normalize('NFC',path.name))
    if not m:raise ReviewPdfError(f'invalid {profile.name} filename: {path.name}')
```
출처 검사 두 줄:
```python
        if not re.fullmatch(profile.source_re,source):raise ReviewPdfError(f'{id_}: invalid source')
        expected=profile.expected_source(m[1],id_)
        if expected and source!=expected:raise ReviewPdfError(f'{id_}: source {source} != {expected}')
```
반환: `return ReviewPack(m[1],m[2],tuple(cards),path.resolve(),profile)`.

- [ ] **Step 6: GREEN 확인**

Run: `python -m unittest discover -s .claude/skills/ml-review-pack/tests -p 'test_review_pdf*.py' -v 2>&1 | tail -3`
Expected: `OK` — 새 6개 테스트 포함, 기존 review 테스트 무변경 통과.

- [ ] **Step 7: Commit**
```bash
git add .claude/skills/ml-review-pack/scripts/review_pdf_types.py .claude/skills/ml-review-pack/scripts/review_pdf_cards.py .claude/skills/ml-review-pack/tests/test_review_pdf_cards.py ".claude/skills/ml-review-pack/tests/fixtures/pdf/과제9_Pdf_Test.html"
git commit -m "feat(ml-review): read homework cards through a card profile" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: 프로필을 payload·빌드·CLI까지 전달

**Files:**
- Modify: `.claude/skills/ml-review-pack/scripts/review_pdf_payload.py:15-29` (`to_workbook`)
- Modify: `.claude/skills/ml-review-pack/scripts/build_review_pdf.py:49-82` (`build_pack`), `:93-111` (`main`)
- Test: `.claude/skills/ml-review-pack/tests/test_review_pdf_payload.py`, `.claude/skills/ml-review-pack/tests/test_review_pdf_build.py`

**Interfaces:**
- Consumes: `CardProfile`, `REVIEW`, `HOMEWORK`, `PROFILES`, `read_cards(path, profile)` (Task 2)
- Produces:
  - `to_workbook(problems, assets, mode, pages=None, profile: CardProfile = REVIEW) -> dict` — `kind`가 `profile.kind(c.source)`
  - `build_pack(review_path, layouts_path, build_dir, *, layout='video-16x9', profile: CardProfile = REVIEW) -> BuildResult` — PDF 이름 `f'{profile.stem_fmt.format(range=…, slug=…)}-문제.pdf'`, `meta.title = profile.title_fmt.format(range=…)`, `validation.json`에 `"profile": profile.name`
  - CLI `--profile {homework,review}` (기본 `review`)

- [ ] **Step 1: 실패하는 테스트 작성**

`test_review_pdf_payload.py`: import에 `from review_pdf_types import HOMEWORK`를 추가하고 `TestPayload`에 메서드를 추가한다.
```python
    def test_homework_kind_badge(self):
        path=FIXTURES/'pdf/과제9_Pdf_Test.html'
        ps=normalize_cards(read_cards(path,HOMEWORK),None,path)[:1]
        p=to_workbook(ps,{},'problems',profile=HOMEWORK)['problems'][0]
        self.assertEqual((p['kind'],p['section'],p['number']),('과제','HW9 Problem 1','P1'))
        self.assertEqual(to_workbook(self.ps[:1],{},'problems')['problems'][0]['kind'],'예제')
```
`test_review_pdf_build.py`: import에 `from review_pdf_types import HOMEWORK`를 추가하고 `TestBuild`에 메서드 두 개를 추가한다.
```python
    def test_homework_profile_build(self):
        import build_review_pdf
        source=self.d/'과제9_Pdf_Test.html';source.write_bytes((FIXTURES/'pdf/과제9_Pdf_Test.html').read_bytes())
        seen=[];original=build_review_pdf.render_workbook
        def spy(payload,mode,html_path,pdf_path=None,**kwargs):
            seen.append(payload['meta']['title']);return original(payload,mode,html_path,pdf_path,**kwargs)
        with patch('build_review_pdf.render_workbook',spy):result=build_pack(source,None,self.d/'hw',profile=HOMEWORK)
        self.assertEqual(set(seen),{'머신러닝기초 과제9'})
        self.assertEqual((result.problems_pdf.name,result.answers_pdf.name),('과제9_Pdf_Test-문제.pdf','과제9_Pdf_Test-답안.pdf'))
        report=json.loads(result.report_path.read_text(encoding='utf-8'))
        self.assertEqual((report['profile'],report['range'],report['logical_count'],report['status']),('homework','9',2,'validated'))
        with fitz.open(result.problems_pdf) as doc:
            text=''.join(p.get_text() for p in doc)
        self.assertIn('과제',text);self.assertIn('HW9 Problem 1',text);self.assertNotIn('ANSWER_ONLY_SENTINEL',text)
        with fitz.open(result.answers_pdf) as doc:self.assertIn('ANSWER_ONLY_SENTINEL',''.join(p.get_text() for p in doc))
    def test_cli_profile_flag(self):
        args=['--review',str(self.source),'--build-dir',str(self.d/'b'),'--stage-only','--report',str(self.d/'r.json')]
        with patch('build_review_pdf.build_pack',side_effect=ReviewPdfError('stop')) as bp:
            self.assertEqual(main(['--profile','homework',*args]),1)
        self.assertIs(bp.call_args.kwargs['profile'],HOMEWORK)
        with self.assertRaises(SystemExit) as e:main(['--profile','nope',*args])
        self.assertEqual(e.exception.code,2)
```
기존 `test_stage_only_pair_and_report`에 `self.assertEqual(report['profile'],'review')` 한 줄을 추가한다.

- [ ] **Step 2: RED 확인**

Run: `python -m unittest discover -s .claude/skills/ml-review-pack/tests -p 'test_review_pdf_payload.py' -v` 그리고 `... -p 'test_review_pdf_build.py' -v`
Expected: `to_workbook() got an unexpected keyword argument 'profile'`, `build_pack() got an unexpected keyword argument 'profile'`, `KeyError: 'profile'`, `unrecognized arguments: --profile`.

- [ ] **Step 3: payload 구현**

`review_pdf_payload.py`: import를 `from review_pdf_types import PageSlice, ReviewPdfError, REVIEW`로 바꾸고, 시그니처를 `def to_workbook(problems, assets, mode, pages=None, profile=REVIEW):`로 바꾼다. `item` 안의 `'kind':'예제' if ' Example ' in c.source else '연습문제'`를 `'kind':profile.kind(c.source)`로 바꾼다.

- [ ] **Step 4: build_pack·CLI 구현**

`build_review_pdf.py`:
- import에 `from review_pdf_types import BuildResult,ReviewPdfError,REVIEW,PROFILES`(기존 import 줄 확장).
- 시그니처 `def build_pack(review_path,layouts_path,build_dir,*,layout: Layout="video-16x9",profile=REVIEW):`
- `pack=read_cards(review_path)` → `pack=read_cards(review_path,profile)`
- `evidence` dict에 `'profile':profile.name` 추가.
- 루프 앞에 `title=profile.title_fmt.format(range=pack.range);stem=profile.stem_fmt.format(range=pack.range,slug=pack.slug)`.
- `measure` 안과 루프 뒤의 두 곳: `payload=to_workbook(problems,assets,mode,pages,profile);payload['meta']['title']=title`
- `pdf=stage/f'{stem}-{suffix}.pdf'`
- `main`: `ap.add_argument('--profile',choices=sorted(PROFILES),default='review')`를 추가하고 호출을 `build_pack(args.review,args.layouts,args.build_dir,layout=args.layout,profile=PROFILES[args.profile])`로 바꾼다.

- [ ] **Step 5: GREEN 확인**

Run: `python -m unittest discover -s .claude/skills/ml-review-pack/tests 2>&1 | tail -3`
Expected: `OK` (Chrome 렌더 포함, 1분 내외).

- [ ] **Step 6: 워크플로 문서 갱신**

`.claude/skills/ml-review-pack/references/pdf-workflow.md`의 "기본 규격은 `video-16x9`…" 문단 바로 아래에 추가한다.
```markdown
과제 PDF는 `--profile homework`로 만든다. 입력 파일명은 `과제<N>_<Slug>.html`, 카드 `data-source`는 `HW<N> Problem <k>`(카드 id `p<k>`와 번호 일치)이며, 출력은 `과제<N>_<Slug>-문제.pdf`/`-답안.pdf`, 배지는 `과제`, 제목은 `머신러닝기초 과제<N>`이다. 프로필을 생략하면 `review` 규칙이 적용되어 과제 파일명은 `invalid review filename`으로 실패한다.
```
Run: `python -m unittest discover -s .claude/skills/ml-review-pack/tests -p 'test_skill_files.py'` → Expected: `OK`.

- [ ] **Step 7: Commit**
```bash
git add .claude/skills/ml-review-pack/scripts/review_pdf_payload.py .claude/skills/ml-review-pack/scripts/build_review_pdf.py .claude/skills/ml-review-pack/tests/test_review_pdf_payload.py .claude/skills/ml-review-pack/tests/test_review_pdf_build.py .claude/skills/ml-review-pack/references/pdf-workflow.md
git commit -m "feat(ml-review): build homework PDF pairs with --profile homework" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: 과제1 Fraction 정답 키와 카드 대조기

정답 값은 이 plan 작성 시 sympy 독립 계산과 교차 검증했다(P14 `c=\sqrt{2/\pi}\,e^{3/2}` 포함).

**Files:**
- Create: `scripts/homework1_answers.py`
- Test: `tests/test_homework1_answers.py`

**Interfaces:**
- Consumes: `read_cards(path, HOMEWORK)` (Task 2) — `main`에서만
- Produces: `key() -> dict[str, list[str]]` (p1–p25, 공백 제거된 TeX 토큰), `missing(answers: dict[str, str]) -> list[str]` (`'pN: no card'`, `'pN: missing <token>'`), CLI `python scripts/homework1_answers.py <카드.html> [p1,p2,…]` → `OK`/누락 목록, 종료코드 0/1. 인자 없이 실행하면 정답 토큰표 출력.

- [ ] **Step 1: 실패하는 테스트 작성**

`tests/test_homework1_answers.py`:
```python
#!/usr/bin/env python3
"""Unit tests for scripts/homework1_answers.py (과제1 정답 키)."""

from fractions import Fraction as F
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from homework1_answers import (  # noqa: E402
    P22, bm, col, det, fr, inv, key, main, mat, missing, p17_ml, p19_map, p23, p24, p25,
)

CARD = (
    '<article class="card" id="p4" data-source="HW1 Problem 4"><h3>P4. t</h3>'
    '<div class="problem"><div class="conditions">c</div><div class="ask">a</div></div>'
    '<details class="original"><summary>o</summary>x</details><details class="hint"><summary>h</summary>y</details>'
    '<details class="solution"><summary>s</summary><ol class="steps"><li>z</li></ol>'
    '<p class="answer">$\\det(\\mathbf{A})=10$, $\\det(\\mathbf{B})=6$, $\\det(\\mathbf{C})=-6$, $\\det(\\mathbf{D})=0$</p>'
    '</details></article>'
)


class TestFormat(unittest.TestCase):
    def test_fr(self):
        self.assertEqual(fr(3), '3')
        self.assertEqual(fr(F(-4, 5)), '-\\frac{4}{5}')

    def test_bm_column(self):
        self.assertEqual(bm(col(1, F(1, 3))), '\\begin{bmatrix}1\\\\\\frac{1}{3}\\end{bmatrix}')


class TestValues(unittest.TestCase):
    def test_linear_algebra(self):
        self.assertEqual(det(mat([[1, 3, 5], [2, 4, 6], [0, 2, 4]])), 0)
        self.assertEqual(inv(mat([[1, -2], [3, 1]])), mat([[F(1, 7), F(2, 7)], [F(-3, 7), F(1, 7)]]))

    def test_regression(self):
        self.assertEqual(p17_ml(), col(F(7, 3), 1))
        self.assertEqual(p19_map(1), col(F(7, 4), F(2, 3)))
        self.assertEqual(p19_map(F(1, 4)), col(1, F(1, 3)))
        self.assertEqual(p23(), (F(8, 5), F(4, 3)))
        self.assertEqual(p24(), (3, F(5, 2)))

    def test_gaussian(self):
        mu, s = p25()
        self.assertEqual(mu, col(F(3, 11), F(4, 11)))
        self.assertEqual(s, mat([[F(7, 11), F(2, 11)], [F(2, 11), F(10, 11)]]))
        self.assertEqual(P22['c'][1], mat([[8, 0], [0, 4]]))


class TestMissing(unittest.TestCase):
    def test_all_25_keys(self):
        self.assertEqual(sorted(key(), key=lambda p: int(p[1:])), [f'p{i}' for i in range(1, 26)])

    def test_entity_and_whitespace_normalized(self):
        answers = {
            'p4': '정답: $\\det(\\mathbf{A}) = 10$, $\\det(\\mathbf{B})=6$, $\\det(\\mathbf{C})=-6$, $\\det(\\mathbf{D})=0$',
            'p21': '$\\bar{\\mathbf{x}}=\\begin{bmatrix} 2 \\\\ 3 \\end{bmatrix}$, '
                   '$\\mathbf{S}=\\begin{bmatrix}1 &amp; 1\\\\ 1 &amp; 2\\end{bmatrix}$',
        }
        out = missing(answers)
        self.assertEqual([m for m in out if m.startswith(('p4:', 'p21:'))], [])
        self.assertIn('p1: no card', out)

    def test_wrong_value_reported(self):
        self.assertIn('p4: missing \\det(\\mathbf{A})=10', missing({'p4': '$\\det(\\mathbf{A})=11$'}))

    def test_main_reads_homework_cards(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / '과제1_Test.html'
            p.write_text(f'<section id="hw1">{CARD}</section>', encoding='utf-8')
            self.assertEqual(main([str(p), 'p4']), 0)
            self.assertEqual(main([str(p)]), 1)


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: RED 확인**

Run: `python -m unittest discover -s tests -p 'test_homework1_answers.py' -v`
Expected: `ModuleNotFoundError: No module named 'homework1_answers'`.

- [ ] **Step 3: 정답 키 구현**

`scripts/homework1_answers.py`:
```python
#!/usr/bin/env python3
"""
과제1(Homework #1) 정답 키와 카드 대조기.

모든 수치 정답을 Fraction으로 정확히 계산하고, 과제1 카드 HTML의
`.answer`에 정답 TeX 토큰이 그대로 들어 있는지 검사한다.
토큰 규약: 정수는 그대로, 분수는 \\frac{p}{q}(음수는 앞에 -), 행렬·벡터는
\\begin{bmatrix}...\\end{bmatrix}(열벡터는 한 칸짜리 행). 비교 전 HTML 엔티티를
풀고 모든 공백을 지운다.
"""

from __future__ import annotations

from fractions import Fraction as F
import html
from pathlib import Path
import re
import sys

Matrix = list[list[F]]


def mat(rows) -> Matrix:
    return [[F(v) for v in row] for row in rows]


def col(*values) -> Matrix:
    return [[F(v)] for v in values]


def T(a: Matrix) -> Matrix:
    return [list(r) for r in zip(*a)]


def mul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(c, a: Matrix) -> Matrix:
    return [[F(c) * x for x in r] for r in a]


def eye(n: int) -> Matrix:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def det(a: Matrix) -> F:
    if len(a) == 1:
        return a[0][0]
    return sum((-1) ** j * a[0][j] * det([r[:j] + r[j + 1:] for r in a[1:]]) for j in range(len(a)))


def inv(a: Matrix) -> Matrix:
    n = len(a)
    m = [list(r) + e for r, e in zip(a, eye(n))]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        m[c] = [x / m[c][c] for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                m[r] = [x - m[r][c] * y for x, y in zip(m[r], m[c])]
    return [r[n:] for r in m]


def fr(x) -> str:
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    sign = '-' if x < 0 else ''
    return f'{sign}\\frac{{{abs(x.numerator)}}}{{{x.denominator}}}'


def bm(a: Matrix) -> str:
    return '\\begin{bmatrix}' + '\\\\'.join('&'.join(fr(v) for v in r) for r in a) + '\\end{bmatrix}'


# ---- 수치 정답 ----
P3_A, P3_B = mat([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), mat([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
P8_A = mat([[1, -1], [1, 0], [1, 1]])
P9_PHI = mat([[1, -1, 1], [1, 0, 0], [1, 1, 1]])
P17_PHI, P17_Y = mat([[1, -1], [1, 0], [1, 1]]), col(2, 1, 4)


def p17_ml() -> Matrix:
    return mul(inv(mul(T(P17_PHI), P17_PHI)), mul(T(P17_PHI), P17_Y))


def p19_map(b2) -> Matrix:
    g = add(mul(T(P17_PHI), P17_PHI), scale(1 / F(b2), eye(2)))  # sigma^2 = 1
    return mul(inv(g), mul(T(P17_PHI), P17_Y))


def p20() -> tuple[Matrix, F]:
    phi, y = mat([[1, 1], [2, 2]]), col(3, 6)
    th = mul(inv(add(mul(T(phi), phi), scale(5, eye(2)))), mul(T(phi), y))
    r = add(y, scale(-1, mul(phi, th)))
    return th, mul(T(r), r)[0][0] + 5 * mul(T(th), th)[0][0]


def p21() -> tuple[Matrix, Matrix]:
    xs = [col(1, 1), col(1, 3), col(3, 3), col(3, 5)]
    m = scale(F(1, 4), [[sum(x[i][0] for x in xs)] for i in range(2)])
    s = [[F(0)] * 2 for _ in range(2)]
    for x in xs:
        d = add(x, scale(-1, m))
        s = add(s, mul(d, T(d)))
    return m, scale(F(1, 4), s)


def linear_map(a: Matrix, c: Matrix, mu: Matrix, sx: Matrix, extra: Matrix | None = None):
    """y = A x + c (+ 독립 잡음 공분산 extra) -> (mu_y, Sigma_y, C_xy)."""
    sy = mul(mul(a, sx), T(a))
    return add(mul(a, mu), c), add(sy, extra) if extra else sy, mul(sx, T(a))


P22B_SX = inv(mat([[1, -1], [-1, 2]]))  # 지수 이차형식의 정밀도 행렬을 뒤집은 것
P22 = {
    'a': linear_map(mat([[1, 2], [-1, 1]]), col(1, -2), col(1, 2), mat([[4, 1], [1, 2]])),
    'b': linear_map(mat([[2, -1], [1, 1]]), col(-1, 2), col(1, -1), P22B_SX),
    # Cov(x1,x2) = E[x1x2] - E[x1]E[x2] = 0 - (1)(-1) = 1, 같은 eps가 두 좌표에 들어가 1로 채운 행렬이 더해짐
    'c': linear_map(mat([[1, 1], [1, -1]]), col(0, 0), col(1, -1), mat([[2, 1], [1, 3]]), mat([[1, 1], [1, 1]])),
}


def p23() -> tuple[F, F]:
    xs, ys = (1, 2), (2, 3)
    sxx, sxy = sum(F(x * x) for x in xs), sum(F(x * y) for x, y in zip(xs, ys))
    return sxy / sxx, sxy / (sxx + 1)  # prior N(0,1), noise var 1


def p24() -> tuple[F, F]:
    ys = (2, 3, 4)
    return F(sum(ys), len(ys)), F(sum(ys) + 1, len(ys) + 1)  # prior N(1,1), noise var 1


def p25() -> tuple[Matrix, Matrix]:
    s0, s1 = mat([[1, 0], [0, 2]]), mat([[2, 1], [1, 2]])
    sq = inv(add(inv(s0), inv(s1)))
    return mul(sq, add(mul(inv(s0), col(0, 0)), mul(inv(s1), col(1, 1)))), sq


def key() -> dict[str, list[str]]:
    th17, (th20, j20) = p17_ml(), p20()
    m21, s21 = p21()
    ml23, map23 = p23()
    ml24, map24 = p24()
    mu25, s25 = p25()
    g8 = mul(T(P8_A), P8_A)
    k = {
        'p1': [bm(T(mat([[1, -2, 3], [0, 4, 5]]))), bm(T(col(2, -1, 4))), bm(T(mat([[1, 2, 0], [-1, 3, 4], [5, 0, -2]])))],
        'p2': ['\\mathbf{x}^\\top\\mathbf{y}=0', '\\|\\mathbf{x}\\|_2=3', '\\|\\mathbf{y}\\|_2=\\sqrt{5}', '직교'],
        'p3': [bm(mul(P3_A, P3_B)), bm(mul(P3_B, P3_A)), '\\neq'],
        'p4': [f'\\det(\\mathbf{{{n}}})={fr(det(mat(m)))}' for n, m in
               [('A', [[3, 1], [2, 4]]), ('B', [[1, -2], [3, 0]]), ('C', [[2, 0, 0], [0, -1, 0], [0, 0, 3]]), ('D', [[1, 3, 5], [2, 4, 6], [0, 2, 4]])]],
        'p5': [f'\\mathbf{{{n}}}^{{-1}}=' + bm(inv(mat(m))) for n, m in
               [('A', [[2, 1], [1, 1]]), ('B', [[1, -2], [3, 1]]), ('C', [[2, 1, 0], [1, 2, 0], [0, 0, 2]])]],
        'p6': ['\\mathbf{x}_3=2\\mathbf{x}_1-\\mathbf{x}_2', '선형 종속'],
        'p7': ['\\mathbf{y}=-6\\mathbf{x}_1+3\\mathbf{x}_2+2\\mathbf{x}_3'],
        'p8': [bm(g8), '=' + fr(det(g8)), bm(inv(g8))],
        'p9': [bm(P9_PHI), bm(mul(P9_PHI, col(1, 1, 2)))],
        'p10': [bm(col(0, -2)), bm(col(-4, -2)), bm(col(-2, -4, 2))],
        'p11': [bm(mat([[1, 2], [3, -1]])), bm(mat([[2, 1], [2, 1], [0, 4]]))],
        'p12': ['3x_1^2+2x_1x_2+2x_2^2-2x_1+2x_2', 'x_1=' + fr(F(3, 5)), 'x_2=' + fr(F(-4, 5))],
        'p13': ['\\frac{1}{2\\pi\\sqrt{3}}', '-\\frac{1}{3}(x_1^2-x_1x_2+x_2^2-3x_1+3x_2+3)'],
        'p14': ['c=\\sqrt{\\frac{2}{\\pi}}e^{3/2}', '\\mu=1', 'v=\\frac{1}{4}'],
        'p15': ['(2\\pi\\sigma^2)^{-N/2}', '\\sum_{n=1}^{N}(y_n-\\theta_0-\\theta_1x_n)^2'],
        'p16': ['\\frac{N}{2}\\log(2\\pi\\sigma^2)', '\\frac{1}{2\\sigma^2}\\|\\mathbf{y}-\\boldsymbol{\\Phi}\\boldsymbol{\\theta}\\|_2^2'],
        'p17': ['(\\boldsymbol{\\Phi}^\\top\\boldsymbol{\\Phi})^{-1}\\boldsymbol{\\Phi}^\\top\\mathbf{y}', bm(th17), bm(mul(P17_PHI, th17)), 'S=\\frac{8}{3}'],
        'p18': ['\\frac{\\sigma^2}{b^2}\\mathbf{I}_K', '\\lambda=\\frac{\\sigma^2}{b^2}'],
        'p19': [bm(th17), bm(p19_map(1)), bm(p19_map(F(1, 4)))],
        'p20': [bm(mat([[5, 5], [5, 5]])), '\\det(\\boldsymbol{\\Phi}^\\top\\boldsymbol{\\Phi})=0', bm(col(3, 6)), bm(th20), '=' + fr(j20)],
        'p21': [bm(m21), bm(s21)],
        'p22': [bm(v) for part in 'abc' for v in P22[part]] + [bm(col(1, -1)), bm(P22B_SX)],
        'p23': ['\\frac{1}{2\\pi}', '\\theta_{\\mathrm{ML}}=' + fr(ml23), '\\theta_{\\mathrm{MAP}}=' + fr(map23),
                '\\hat{y}_{\\mathrm{ML}}=' + fr(3 * ml23), '\\hat{y}_{\\mathrm{MAP}}=' + fr(3 * map23)],
        'p24': ['(2\\pi)^{-3/2}', '\\theta_{\\mathrm{ML}}=' + fr(ml24), '\\theta_{\\mathrm{MAP}}=' + fr(map24), 'MAP'],
        'p25': [bm(mu25), bm(s25), bm(inv(s25)), '\\frac{1}{2\\pi}\\sqrt{\\frac{11}{6}}'],
    }
    return {p: [re.sub(r'\s+', '', t) for t in ts] for p, ts in k.items()}


def missing(answers: dict[str, str]) -> list[str]:
    """answers: 카드 id -> answer HTML. 카드가 없거나 토큰이 빠진 항목을 돌려준다."""
    out = []
    for pid, tokens in key().items():
        if pid not in answers:
            out.append(f'{pid}: no card')
            continue
        text = re.sub(r'\s+', '', html.unescape(answers[pid]))
        out += [f'{pid}: missing {t}' for t in tokens if t not in text]
    return out


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.claude/skills/ml-review-pack/scripts'))
    from review_pdf_cards import read_cards
    from review_pdf_types import HOMEWORK
    pack = read_cards(Path(argv[0]), HOMEWORK)
    only = set(argv[1].split(',')) if len(argv) > 1 else None
    problems = [m for m in missing({c.id: c.answer_html for c in pack.cards}) if only is None or m.split(':')[0] in only]
    print('\n'.join(problems) or 'OK')
    return 1 if problems else 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        for pid, tokens in key().items():
            print(pid, *tokens, sep='\n  ')
        sys.exit(0)
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 4: GREEN 확인**

Run: `python -m unittest discover -s tests -p 'test_homework1_answers.py' -v`
Expected: `Ran 9 tests … OK`. 이어서 `PYTHONIOENCODING=utf-8 python scripts/homework1_answers.py | head -20`으로 정답 토큰표가 출력되는지 본다(예: `p4` 아래 `\det(\mathbf{A})=10`).

- [ ] **Step 5: Commit**
```bash
git add scripts/homework1_answers.py tests/test_homework1_answers.py
git commit -m "feat(homework): add exact answer key for homework 1" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: 과제1 카드 HTML — P1–P12 (선형대수·미분)

**Files:**
- Create: `과제/과제1/과제1_Homework1.html`
- Reference(읽기 전용): `과제/과제1/26_10_Introduction_to_Machine_Learning_homework1_rev.pdf` (원문은 `python -c "import pymupdf;d=pymupdf.open('과제/과제1/26_10_Introduction_to_Machine_Learning_homework1_rev.pdf');print(''.join(p.get_text() for p in d))"`로 추출)

**Interfaces:**
- Consumes: `HOMEWORK` 규칙(Task 2), `homework1_answers.py` CLI(Task 4)
- Produces: `과제/과제1/과제1_Homework1.html` — `<section id="hw1">` 안의 `article.card#p1…p12`; Task 6이 같은 섹션에 p13–p25를 이어 붙인다.

카드 규칙(모든 카드 공통):
- 마크업은 아래 P4 예시와 같은 구조. `.problem`의 직계 자식은 `.conditions` 1개 + `.ask` 1개. 조건이 질문보다 먼저 오고, 원문의 순서·수치·식·소문항을 보존한다.
- 공통 규약 세 가지(열벡터, gradient는 열벡터, 단변량 가우시안의 둘째 모수는 분산)는 해당되는 카드의 conditions에 한 줄로 넣는다: 열벡터 → P1, P2, P6, P7, P9, P12 / gradient 열벡터 → P10, P12.
- `details.original`의 summary는 `과제 원문 보기`, 본문은 영어 원문 전문을 큰따옴표로 감싸고 ` — Problem N`을 붙인다. 원문 수식도 `$…$`로 옮긴다.
- `details.hint`: 원 Hint가 있는 P10, P11은 그 내용을 한국어로 옮기고, 나머지는 풀이 방향 한 문장.
- 풀이 `<ol class="steps">`: 한 `<li>`에 한 단계, `$$` 디스플레이는 `<li>`당 최대 하나(페이지 분할 단위가 `<li>`라서). 증명·서술 요구(P2(d) 직교 설명, P3 비교, P6 근거, P8 곱셈 검증, P9 선형인 이유)는 별도 단계로 쓴다.
- `.answer`는 "정답: "으로 시작하고 아래 표의 토큰을 모두 포함한다.
- 표·SVG·이미지는 쓰지 않는다(모든 행렬은 KaTeX `bmatrix`).

예시 카드(P4, 그대로 사용):
```html
<article class="card" id="p4" data-source="HW1 Problem 4">
  <h3>P4. 행렬식 계산</h3>
  <div class="problem"><div class="conditions">다음 네 행렬이 주어져요.
  $$\mathbf{A}=\begin{bmatrix}3 &amp; 1\\2 &amp; 4\end{bmatrix},\quad \mathbf{B}=\begin{bmatrix}1 &amp; -2\\3 &amp; 0\end{bmatrix}$$
  $$\mathbf{C}=\begin{bmatrix}2 &amp; 0 &amp; 0\\0 &amp; -1 &amp; 0\\0 &amp; 0 &amp; 3\end{bmatrix},\quad \mathbf{D}=\begin{bmatrix}1 &amp; 3 &amp; 5\\2 &amp; 4 &amp; 6\\0 &amp; 2 &amp; 4\end{bmatrix}$$</div>
  <div class="ask">각 행렬의 행렬식을 구해 보세요. (d)는 첫 행 전개와 Sarrus 규칙 두 방법으로 모두 구해요.<ol><li>(a) $\det(\mathbf{A})$</li><li>(b) $\det(\mathbf{B})$</li><li>(c) $\det(\mathbf{C})$</li><li>(d) $\det(\mathbf{D})$</li></ol></div></div>
  <details class="original"><summary>과제 원문 보기</summary>"Compute the determinant of each matrix. For part (d), use both expansion along the first row and the Sarrus rule." — Problem 4</details>
  <details class="hint"><summary>힌트 보기</summary>$2\times 2$ 행렬은 $ad-bc$, 대각행렬은 대각 원소를 모두 곱하면 돼요.</details>
  <details class="solution"><summary>풀이 보기</summary><ol class="steps">
    <li>(a) $\det(\mathbf{A})=3\cdot 4-1\cdot 2=10$이에요.</li>
    <li>(b) $\det(\mathbf{B})=1\cdot 0-(-2)\cdot 3=6$이에요.</li>
    <li>(c) 대각행렬이라 $\det(\mathbf{C})=2\cdot(-1)\cdot 3=-6$이에요.</li>
    <li>(d) 첫 행으로 전개해요. $$\det(\mathbf{D})=1(4\cdot 4-6\cdot 2)-3(2\cdot 4-6\cdot 0)+5(2\cdot 2-4\cdot 0)=4-24+20=0$$</li>
    <li>(d) Sarrus 규칙으로도 확인해요. $$(1\cdot 4\cdot 4+3\cdot 6\cdot 0+5\cdot 2\cdot 2)-(5\cdot 4\cdot 0+1\cdot 6\cdot 2+3\cdot 2\cdot 4)=36-36=0$$</li>
  </ol><p class="answer">정답: $\det(\mathbf{A})=10$, $\det(\mathbf{B})=6$, $\det(\mathbf{C})=-6$, $\det(\mathbf{D})=0$</p></details>
</article>
```

카드별 내용(제목, 풀이 핵심, `.answer` 필수 토큰 — 공백은 자유):

| id | 제목 | 풀이 핵심 | `.answer` 필수 토큰 |
|---|---|---|---|
| p1 | 전치 구하기 | 행↔열 교환을 (a)(b)(c) 단계로 | `\begin{bmatrix}1&0\\-2&4\\3&5\end{bmatrix}`, `\begin{bmatrix}2&-1&4\end{bmatrix}`, `\begin{bmatrix}1&-1&5\\2&3&0\\0&4&-2\end{bmatrix}` |
| p2 | 내적과 노름 | $\mathbf{x}^\top\mathbf{y}=2-2+0$, $\|\mathbf{x}\|_2=\sqrt{9}$, $\|\mathbf{y}\|_2=\sqrt{5}$, (d) 내적 0이라 직교 | `\mathbf{x}^\top\mathbf{y}=0`, `\|\mathbf{x}\|_2=3`, `\|\mathbf{y}\|_2=\sqrt{5}`, `직교` |
| p3 | 행렬 곱의 순서 | $AB$, $BA$ 각 원소 계산 후 비교 | `\begin{bmatrix}4&3&5\\10&9&11\\16&15&17\end{bmatrix}`, `\begin{bmatrix}5&7&9\\11&13&15\\8&10&12\end{bmatrix}`, `\neq` |
| p4 | 행렬식 계산 | 위 예시 그대로 | `\det(\mathbf{A})=10`, `\det(\mathbf{B})=6`, `\det(\mathbf{C})=-6`, `\det(\mathbf{D})=0` |
| p5 | 역행렬 구하기 | 2×2는 $\frac{1}{ad-bc}$ 공식(det 1, 7), (c)는 블록: 왼쪽 위 2×2(det 3)의 역 + $\frac12$; 각 단계에 곱해서 $\mathbf{I}$ 확인 한 줄 | `\mathbf{A}^{-1}=\begin{bmatrix}1&-1\\-1&2\end{bmatrix}`, `\mathbf{B}^{-1}=\begin{bmatrix}\frac{1}{7}&\frac{2}{7}\\-\frac{3}{7}&\frac{1}{7}\end{bmatrix}`, `\mathbf{C}^{-1}=\begin{bmatrix}\frac{2}{3}&-\frac{1}{3}&0\\-\frac{1}{3}&\frac{2}{3}&0\\0&0&\frac{1}{2}\end{bmatrix}` |
| p6 | 선형 독립 판정 | $c_1\mathbf{x}_1+c_2\mathbf{x}_2+c_3\mathbf{x}_3=\mathbf{0}$ 소거 → $(c_1,c_2,c_3)=(-2,1,1)$ 비자명해 → $\mathbf{x}_3=2\mathbf{x}_1-\mathbf{x}_2$ 검산 | `\mathbf{x}_3=2\mathbf{x}_1-\mathbf{x}_2`, `선형 종속` |
| p7 | 선형결합으로 나타내기 | 연립방정식 소거 → $(-6,3,2)$, 검산 | `\mathbf{y}=-6\mathbf{x}_1+3\mathbf{x}_2+2\mathbf{x}_3` |
| p8 | $\mathbf{A}^\top\mathbf{A}$와 역행렬 | 곱 → $\det=6\ne0$이라 역 존재 → 대각 역 → 곱해서 $\mathbf{I}_2$ 검증 | `\begin{bmatrix}3&0\\0&2\end{bmatrix}`, `=6`, `\begin{bmatrix}\frac{1}{3}&0\\0&\frac{1}{2}\end{bmatrix}` |
| p9 | 특징 행렬과 예측 | 행마다 $\phi(x_n)^\top$ → $\boldsymbol{\Phi}\boldsymbol{\theta}$ → 모델이 $\boldsymbol{\theta}$에 대해 선형이라 선형회귀 | `\begin{bmatrix}1&-1&1\\1&0&0\\1&1&1\end{bmatrix}`, `\begin{bmatrix}2\\1\\4\end{bmatrix}` |
| p10 | gradient 구하기 | 편미분식 → 점 대입, (c)는 연쇄법칙 $2(u+2v-w-3)\cdot(1,2,-1)$ | `\begin{bmatrix}0\\-2\end{bmatrix}`, `\begin{bmatrix}-4\\-2\end{bmatrix}`, `\begin{bmatrix}-2\\-4\\2\end{bmatrix}` |
| p11 | 야코비 행렬 | 일반형 → 점 대입 (출력 행, 입력 열) | `\begin{bmatrix}1&2\\3&-1\end{bmatrix}`, `\begin{bmatrix}2&1\\2&1\\0&4\end{bmatrix}` |
| p12 | 이차형식의 정류점 | $h=3x_1^2+2x_1x_2+2x_2^2-2x_1+2x_2$ 전개 → 편미분 $6x_1+2x_2-2$, $2x_1+4x_2+2$ → 연립 | `3x_1^2+2x_1x_2+2x_2^2-2x_1+2x_2`, `x_1=\frac{3}{5}`, `x_2=-\frac{4}{5}` |

- [ ] **Step 1: 대조기 RED 확인**

`과제/과제1/과제1_Homework1.html`을 아래 뼈대로 만들고 P4 예시 카드만 넣는다.
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>머신러닝기초 과제1</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false})"></script>
</head>
<body>
<main>
<h1>머신러닝기초 과제1 — Linear Algebra, Gaussian Densities, and Linear Regression</h1>
<section id="hw1">
<!-- P4 예시 카드 -->
</section>
</main>
</body>
</html>
```
Run: `python scripts/homework1_answers.py "과제/과제1/과제1_Homework1.html" p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12`
Expected: 종료코드 1, `p1: no card` … `p12: no card`(p4 제외) 출력.

- [ ] **Step 2: P1–P3, P5–P12 카드 작성**

위 표와 공통 규칙대로 11장을 id 순서대로 `<section id="hw1">`에 넣는다(P4 자리 유지).

- [ ] **Step 3: GREEN 확인**

Run: `python scripts/homework1_answers.py "과제/과제1/과제1_Homework1.html" p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12`
Expected: `OK`, 종료코드 0. 이어서 카드 계약 검사:
```bash
python -c "import sys;sys.path.insert(0,'.claude/skills/ml-review-pack/scripts');from pathlib import Path;from review_pdf_cards import read_cards,normalize_cards;from review_pdf_types import HOMEWORK;p=Path('과제/과제1/과제1_Homework1.html');k=read_cards(p,HOMEWORK);normalize_cards(k,None,p);print(len(k.cards),[c.id for c in k.cards])"
```
Expected: `12 ['p1', …, 'p12']` (예외 없음 = `$` 짝·필수 블록·출처 번호 통과).

- [ ] **Step 4: Commit**
```bash
git add "과제/과제1/과제1_Homework1.html"
git commit -m "docs(homework): add homework 1 cards P1-P12" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: 과제1 카드 HTML — P13–P25 (가우시안·회귀)

**Files:**
- Modify: `과제/과제1/과제1_Homework1.html` (`<section id="hw1">` 끝에 p13–p25 추가)

**Interfaces:**
- Consumes: Task 5의 파일·카드 공통 규칙(아래에 다시 적음), `homework1_answers.py` CLI
- Produces: 카드 25장이 모두 있는 `과제/과제1/과제1_Homework1.html`

카드 규칙(Task 5와 동일, 다시 적음): `.problem` 직계 `.conditions` 1개 + `.ask` 1개, 조건 먼저, 원문 순서·수치·소문항 보존. `details.original` summary `과제 원문 보기`, 영어 전문 + ` — Problem N`. 풀이 `<li>`당 한 단계·`$$` 최대 하나. `.answer`는 "정답: "으로 시작. 표·SVG 금지. 공통 규약을 conditions에 한 줄로: 단변량 가우시안 둘째 모수 = 분산 → P14, P15, P23, P24 / 열벡터 → P13, P16–P22, P25. 원 Hint가 있는 P13, P14, P18은 그 내용(식 포함)을 한국어로 옮겨 `details.hint`에 넣는다.

| id | 제목 | 풀이 핵심 | `.answer` 필수 토큰 |
|---|---|---|---|
| p13 | 2차원 가우시안 밀도 | $\det\boldsymbol{\Sigma}=3$, $\boldsymbol{\Sigma}^{-1}=\frac13\begin{bmatrix}2&-1\\-1&2\end{bmatrix}$ → 이차형식 $\frac23(x_1^2-x_1x_2+x_2^2-3x_1+3x_2+3)$ 전개 → $-\frac12$ 곱 | `\frac{1}{2\pi\sqrt{3}}`, `-\frac{1}{3}(x_1^2-x_1x_2+x_2^2-3x_1+3x_2+3)` |
| p14 | 완전제곱으로 정규화 | $4z^2-8z+7=4(z-1)^2+3$ → $c\,e^{-3/2}e^{-(z-1)^2/(2\cdot\frac14)}$ → $\mathcal{N}(z\mid1,\frac14)$와 비교, $c\,e^{-3/2}=\sqrt{2/\pi}$ | `c=\sqrt{\frac{2}{\pi}}e^{3/2}`, `\mu=1`, `v=\frac{1}{4}` |
| p15 | 단순회귀의 우도 | 독립 → 곱 → 지수 합 | `(2\pi\sigma^2)^{-N/2}`, `\sum_{n=1}^{N}(y_n-\theta_0-\theta_1x_n)^2` |
| p16 | 음의 로그우도와 최소제곱 | $\det(\sigma^2\mathbf{I}_N)=\sigma^{2N}$, 이차형식 $\frac{1}{\sigma^2}\|\cdot\|_2^2$ → NLL 전개 → 상수·양의 배수는 argmin을 안 바꿈 | `\frac{N}{2}\log(2\pi\sigma^2)`, `\frac{1}{2\sigma^2}\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2` |
| p17 | 정규방정식과 수치 예 | (a) $J=\mathbf{y}^\top\mathbf{y}-2\boldsymbol{\theta}^\top\boldsymbol{\Phi}^\top\mathbf{y}+\boldsymbol{\theta}^\top\boldsymbol{\Phi}^\top\boldsymbol{\Phi}\boldsymbol{\theta}$ → $\nabla J=-2\boldsymbol{\Phi}^\top\mathbf{y}+2\boldsymbol{\Phi}^\top\boldsymbol{\Phi}\boldsymbol{\theta}$ → 열 독립이라 가역; (b) $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}=\mathrm{diag}(3,2)$, $\boldsymbol{\Phi}^\top\mathbf{y}=(7,2)^\top$ | `(\boldsymbol{\Phi}^\top\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^\top\mathbf{y}`, `\begin{bmatrix}\frac{7}{3}\\1\end{bmatrix}`, `\begin{bmatrix}\frac{4}{3}\\\frac{7}{3}\\\frac{10}{3}\end{bmatrix}`, `S=\frac{8}{3}` |
| p18 | MAP과 릿지 | $-\log p(\boldsymbol{\theta}\mid\cdot)=\frac{1}{2\sigma^2}\|\mathbf{y}-\boldsymbol{\Phi}\boldsymbol{\theta}\|_2^2+\frac{1}{2b^2}\|\boldsymbol{\theta}\|_2^2+\text{const}$ → gradient 0 → $2\sigma^2$ 곱해 비교 | `\frac{\sigma^2}{b^2}\mathbf{I}_K`, `\lambda=\frac{\sigma^2}{b^2}` |
| p19 | ML vs MAP 수치 비교 | ML $=\mathrm{diag}(3,2)^{-1}(7,2)^\top$; MAP $=(\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+\frac{1}{b^2}\mathbf{I})^{-1}\boldsymbol{\Phi}^\top\mathbf{y}$, $b^2=1$: diag(4,3), $b^2=\frac14$: diag(7,6) → $b^2$이 작을수록 0쪽으로 수축 | `\begin{bmatrix}\frac{7}{3}\\1\end{bmatrix}`, `\begin{bmatrix}\frac{7}{4}\\\frac{2}{3}\end{bmatrix}`, `\begin{bmatrix}1\\\frac{1}{3}\end{bmatrix}` |
| p20 | 특이한 $\boldsymbol{\Phi}^\top\boldsymbol{\Phi}$와 규제 | (a) det 0 → (b) 두 θ 모두 $\boldsymbol{\Phi}\boldsymbol{\theta}=(3,6)^\top$, 잔차 0 → ML 해가 유일하지 않음 → (c) $(\boldsymbol{\Phi}^\top\boldsymbol{\Phi}+5\mathbf{I})\boldsymbol{\theta}=\boldsymbol{\Phi}^\top\mathbf{y}=(15,15)^\top$, 최솟값 $5+10$ | `\begin{bmatrix}5&5\\5&5\end{bmatrix}`, `\det(\boldsymbol{\Phi}^\top\boldsymbol{\Phi})=0`, `\begin{bmatrix}3\\6\end{bmatrix}`, `\begin{bmatrix}1\\1\end{bmatrix}`, `=15` |
| p21 | 표본 평균과 공분산 | 평균 → 편차 4개 → 외적 합 ÷4 | `\begin{bmatrix}2\\3\end{bmatrix}`, `\begin{bmatrix}1&1\\1&2\end{bmatrix}` |
| p22 | 아핀 변환의 평균·공분산 | $\mathbf{y}=\mathbf{A}\mathbf{x}+\mathbf{c}$ → $\boldsymbol{\mu}_y=\mathbf{A}\boldsymbol{\mu}_x+\mathbf{c}$, $\boldsymbol{\Sigma}_y=\mathbf{A}\boldsymbol{\Sigma}_x\mathbf{A}^\top$, $\mathbf{C}_{xy}=\boldsymbol{\Sigma}_x\mathbf{A}^\top$. (b) 지수의 정밀도 $\begin{bmatrix}1&-1\\-1&2\end{bmatrix}$(det 1이 상수 $\frac{1}{2\pi}$와 일치) → 역. (c) $\mathrm{Cov}(x_1,x_2)=E[x_1x_2]-E[x_1]E[x_2]=1$, 같은 $\varepsilon$이라 $\boldsymbol{\Sigma}_y$에 1로 채운 행렬 더함, $\varepsilon\perp\mathbf{x}$라 $\mathbf{C}_{xy}$엔 영향 없음 | (a) `\begin{bmatrix}6\\-1\end{bmatrix}`, `\begin{bmatrix}16&-1\\-1&4\end{bmatrix}`, `\begin{bmatrix}6&-3\\5&1\end{bmatrix}`; (b) `\begin{bmatrix}1\\-1\end{bmatrix}`, `\begin{bmatrix}2&1\\1&1\end{bmatrix}`, `\begin{bmatrix}2\\2\end{bmatrix}`, `\begin{bmatrix}5&4\\4&5\end{bmatrix}`, `\begin{bmatrix}3&3\\1&2\end{bmatrix}`; (c) `\begin{bmatrix}0\\2\end{bmatrix}`, `\begin{bmatrix}8&0\\0&4\end{bmatrix}`, `\begin{bmatrix}3&1\\4&-2\end{bmatrix}` |
| p23 | 절편 없는 회귀의 ML·MAP | $L=\frac{1}{2\pi}\exp[-\frac12((2-\theta)^2+(3-2\theta)^2)]$ → NLL 미분 $5\theta-8=0$ → 사후 $6\theta-8=0$ → 예측 | `\frac{1}{2\pi}`, `\theta_{\mathrm{ML}}=\frac{8}{5}`, `\theta_{\mathrm{MAP}}=\frac{4}{3}`, `\hat{y}_{\mathrm{ML}}=\frac{24}{5}`, `\hat{y}_{\mathrm{MAP}}=4` |
| p24 | 평균 추정의 ML·MAP | $L=(2\pi)^{-3/2}\exp[-\frac12\sum(y_n-\theta)^2]$ → $3\theta-9=0$ → $4\theta-10=0$ → MAP이 1에 더 가까움 | `(2\pi)^{-3/2}`, `\theta_{\mathrm{ML}}=3`, `\theta_{\mathrm{MAP}}=\frac{5}{2}`, `MAP` |
| p25 | 두 가우시안의 곱 | $\boldsymbol{\Sigma}_q=(\boldsymbol{\Sigma}_0^{-1}+\boldsymbol{\Sigma}_1^{-1})^{-1}$, $\boldsymbol{\mu}_q=\boldsymbol{\Sigma}_q(\boldsymbol{\Sigma}_0^{-1}\boldsymbol{\mu}_0+\boldsymbol{\Sigma}_1^{-1}\boldsymbol{\mu}_1)$ 유도(지수의 이차·일차항 비교) → $\boldsymbol{\Sigma}_q^{-1}=\begin{bmatrix}\frac53&-\frac13\\-\frac13&\frac76\end{bmatrix}$, $\det\boldsymbol{\Sigma}_q=\frac{6}{11}$ → 정규화 밀도 | `\begin{bmatrix}\frac{3}{11}\\\frac{4}{11}\end{bmatrix}`, `\begin{bmatrix}\frac{7}{11}&\frac{2}{11}\\\frac{2}{11}&\frac{10}{11}\end{bmatrix}`, `\begin{bmatrix}\frac{5}{3}&-\frac{1}{3}\\-\frac{1}{3}&\frac{7}{6}\end{bmatrix}`, `\frac{1}{2\pi}\sqrt{\frac{11}{6}}` |

- [ ] **Step 1: RED 확인**

Run: `python scripts/homework1_answers.py "과제/과제1/과제1_Homework1.html"`
Expected: 종료코드 1, `p13: no card` … `p25: no card` 13줄.

- [ ] **Step 2: P13–P25 카드 작성**

위 표와 규칙대로 13장을 `<section id="hw1">` 끝에 id 순서대로 추가한다. P22의 `.ask`는 `(a)(b)(c)` `<ol>`로 각각의 정의(기댓값·분산·밀도·$\mathbf{y}$ 정의)를 조건에 두고 묻는 것만 ask에 둔다. 각 소문항의 풀이는 최소 3단계(μ_y, Σ_y, C_xy)로 나눈다.

- [ ] **Step 3: GREEN 확인**

Run: `python scripts/homework1_answers.py "과제/과제1/과제1_Homework1.html"` → Expected: `OK`.
Run(카드 계약): Task 5 Step 3의 `python -c …` 명령 → Expected: `25 ['p1', …, 'p25']`.

- [ ] **Step 4: Commit**
```bash
git add "과제/과제1/과제1_Homework1.html"
git commit -m "docs(homework): add homework 1 cards P13-P25" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: PDF 쌍 빌드·전체 페이지 검수·배포

**Files:**
- Create: `과제/과제1/과제1_Homework1-문제.pdf`, `과제/과제1/과제1_Homework1-답안.pdf`
- 빌드 산출물(커밋 안 함): `$TMP/hw1-pdf/…` — `TMP`는 세션 scratchpad 또는 `python -c "import tempfile;print(tempfile.gettempdir())"`의 하위 폴더

**Interfaces:**
- Consumes: `build_review_pdf.py --profile homework`(Task 3), `review_pdf_publish.publish_files`(Task 1), 카드 25장(Task 6)
- Produces: 공개 PDF 두 개

- [ ] **Step 1: stage 빌드**
```bash
TMP=$(python -c "import tempfile;print(tempfile.gettempdir())")/hw1-pdf
python .claude/skills/ml-review-pack/scripts/build_review_pdf.py --profile homework --review "과제/과제1/과제1_Homework1.html" --build-dir "$TMP/build" --stage-only --report "$TMP/validation.json"
```
Expected: 종료코드 0, JSON 한 줄(`problems_pdf`, `answers_pdf`, `report`). `validation.json`에서 `status: validated`, `profile: homework`, `logical_count: 25`, `layout: video-16x9`, `page_size_pt: [1440, 810]`, 모든 `issues` 빈 배열을 확인한다. 실패하면 `errors`의 카드 id를 보고 Task 5/6의 해당 카드를 고친다(예: KaTeX 오류 → TeX 수정, 분할 실패 → 그 카드의 긴 `<li>`를 둘로 나눔). 같은 오류로 2회 실패하면 멈추고 보고한다.

- [ ] **Step 2: 템플릿 SHA 확인**

Run: `python -m unittest discover -s .claude/skills/ml-review-pack/tests -p 'test_review_pdf_payload.py' -k templates -v` → Expected: `OK`.

- [ ] **Step 3: 전체 페이지 PNG 렌더링**
```bash
python - "$TMP" <<'EOF'
import json, sys
from pathlib import Path
import pymupdf
tmp = Path(sys.argv[1]); e = json.loads((tmp / 'validation.json').read_text(encoding='utf-8'))
for mode in ('problems', 'answers'):
    pdf = Path(e['pdfs'][mode]['path']); out = tmp / 'png' / mode; out.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(pdf) as doc:
        for i, page in enumerate(doc, 1):
            page.get_pixmap(dpi=60).save(out / f'{i:02d}.png')
    print(mode, e['pdfs'][mode]['page_count'], 'pages ->', out)
EOF
```
Expected: 모드별 페이지 수 출력(문제지 ≥ 25, 해설지 ≥ 25).

- [ ] **Step 4: 육안 검수**

PNG를 **모든 페이지** 연다(Read 도구로 이미지 열람). 페이지마다 확인한다: 머리글 `과제 · P<k>`와 `HW1 Problem <k> · n / N`, 행렬·분수 KaTeX 렌더링(빨간 오류 텍스트 없음), 하단 자막 여백이 비어 있음, `(계속)` 페이지의 이어짐, 문제지에 풀이·정답이 없음, 해설지의 단계 번호 순서, Hint 블록. 결함이 있으면 해당 카드를 고치고 Step 1부터 다시 한다.

- [ ] **Step 5: 공개 폴더에 배포**
```bash
python - "$TMP" <<'EOF'
import json, sys
from pathlib import Path
sys.path.insert(0, '.claude/skills/ml-review-pack/scripts')
from build_review_pdf import digest
from review_pdf_publish import publish_files
tmp = Path(sys.argv[1]); e = json.loads((tmp / 'validation.json').read_text(encoding='utf-8'))
assert e['status'] == 'validated' and e['profile'] == 'homework'
assert digest(e['source_path']) == e['source_sha256'], 'stale source'
staged = {}
for mode in ('problems', 'answers'):
    src = Path(e['pdfs'][mode]['path'])
    assert digest(src) == e['pdfs'][mode]['sha256'], 'PDF changed'
    staged[Path('과제/과제1') / src.name] = src
publish_files(staged, tmp / 'backups')
print(*staged, sep='\n')
EOF
```
Expected: `과제/과제1/과제1_Homework1-문제.pdf`, `과제/과제1/과제1_Homework1-답안.pdf` 두 줄.

- [ ] **Step 6: 최종 회귀 확인**

Run: `python -m unittest discover -s .claude/skills/ml-review-pack/tests 2>&1 | tail -3` 그리고 `python -m unittest discover -s tests 2>&1 | tail -3` → Expected: 둘 다 `OK`.

- [ ] **Step 7: Commit**
```bash
git add "과제/과제1/과제1_Homework1-문제.pdf" "과제/과제1/과제1_Homework1-답안.pdf"
git commit -m "docs(homework): add homework 1 problem and answer PDFs" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
