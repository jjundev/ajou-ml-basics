# ML Midterm Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 완성된 예상문제 1회의 양식·출제·해설 규칙을 보존하는 프로젝트 스킬 `ml-midterm`을 만들고 `ml-problem-explain`의 예상문제 해설 경로를 연결한다.

**Architecture:** 1회 `.pack/tools/`의 EXAM 어댑터와 생성·검증 코드를 새 스킬로 가져와 회차를 매개변수화한다. PDF는 `ml-review-pack`, 상세 해설은 `ml-problem-explain`의 기존 API와 템플릿을 재사용한다. 문제·PDF 검증 후 정확한 원본에 상세 해설을 연결하는 기존 순서를 유지하며, 전체 완료 판정은 모든 산출물과 현재 검토가 통과한 뒤에만 한다.

**Tech Stack:** Python 3.10+, dataclasses/pathlib/표준 라이브러리, 기존 과목 Python 모듈, pytest, Playwright와 로컬 Chrome, PyMuPDF, 검산용 SymPy, 로컬 KaTeX/Pretendard. Windows PowerShell과 Git worktree의 `.git` 파일도 지원한다.

**Spec:** 직전 `grill-yourself` 설계를 이 문서의 [확정 제작 명세](#확정-제작-명세)에 보존했다. 실행자는 이 절과 전체 작업을 함께 읽는다.

## Global Constraints

- 현재 완성된 1회차의 HTML 양식·PDF 판형·출제 방식·해설 작성 규칙을 유지한다. 초기 프롬프트보다 이후 수정으로 완성된 상태를 우선한다.
- 기본 범위는 처음부터 1019 직교투영까지, 대문항은 10개, 구성은 과제 변형 5개 + 모델 분석 5개다. 시험시간·배점은 임의로 추가하지 않는다.
- 42개 소문항은 1회차의 결과이지 다음 회차의 고정 규칙이 아니다. 페이지 수도 대문항 수와 분리한다.
- PDF는 기존 16:9, 1440×810pt, 하단 135pt(180 CSS px) 흰 여백을 유지한다. 템플릿·CSS를 바꾸거나 긴 문항을 축소해 밀어 넣지 않는다.
- HTML의 목차·문제 패널·우측 요약·이전/다음·테마·읽음 상태·도킹·크기 조절·모바일 동작을 유지한다. 탭은 문제 → 원문 → 출제 근거 → 용어다.
- 해설은 understand → recall → start → solve → verify → pitfall → retry와 기존 sum/provenance/terms 구조를 유지한다. 모든 소문항에 solve와 verify가 대응하고 본문 답은 펼친다.
- 공식 적용형은 공식 → 대입 → 결론·핵심 이유, 유도·증명형은 요구한 단계별 전개를 유지한다. 기호 해석이 필요한 곳은 역할·차원·실제 구성을 설명한다.
- 새 스칼라 미분은 행벡터, 변수는 열벡터, Jacobian은 출력×입력이다. 정규방정식은 행 미분 → 0 → 양변 전치로 연결한다. 기존 명시적 원문 관례 보존 분기는 공통 reference를 따른다.
- 영어 본문은 과제1 문체를 따르고 카드의 같은 영어 본문을 PDF와 원문 탭에 사용한다. 번역으로 수치·가정·요구·난이도를 바꾸거나 공식 시험 원문이라고 표시하지 않는다.
- 1회차·복습노트·과제·STT·교안·교재는 수정하지 않는다. 스킬 설치 검증에서는 새 실전 회차를 출제하지 않고 임시 복제/시험 입력만 사용한다.
- source_visual/content/independent/browser를 실제 수행한 경우만 기록한다. 과거 pass를 복사하거나 새 해시만 끼워 넣지 않는다. 수학적 충돌은 disputed로 두고 발행을 보류한다.
- 이 턴은 계획 파일만 저장한다. 구현 방식은 아직 선택되지 않았다. 아래 커밋은 구현 시의 경계이며 실행자의 사용자 지시를 따르고, 원격 push는 요청 없이 하지 않는다.

## Review Focus

1. 회차 2 이상 또는 42개가 아닌 소문항 입력: 제목·영문 표제·파일명·링크·읽음 키·리포트에 1회/42가 남지 않아야 한다. Task 1·2·3의 동적 회차/항목 집합 검사.
2. 한글 NFC/NFD 경로·저장소 이동·Git worktree: 올바른 자료를 하나로 찾고 저장소 밖 경로와 중복 후보는 거부해야 한다. Task 1의 경로·참조 해시 검사.
3. 오래된 JSON과 최신 설명 조각이 공존하거나 해설만 수정하는 입력: 최신 explanations를 사용하고 문제·영문·PDF를 보존해야 한다. Task 3의 조각 우선·비소유 파일 보존 검사.
4. 긴 영어/유도 문항과 원문 없는 비정상 카드: 계속 페이지에 소문항을 순서대로 보존하고 새 출제의 영어 누락은 거부해야 한다. Task 2의 실제 PDF 분할·언어 검사와 Task 4의 패널 회귀 검사.
5. 생성 후 입력·그림·템플릿·승인이 변하거나 파일 교체가 실패하는 경우: 오래된 승인을 거부하고 기존 유효 파일을 복구해야 한다. Task 3·4의 stale/발행 실패 주입 검사.

---

## 확정 제작 명세

### 사용자 동작과 보존 기준

- `/ml-midterm 2회`로 새 회차를 제작한다. 인자 없음은 현재 존재하는 회차 중 최댓값 + 1이다. 삭제된 2회를 복구하지 않고 새 문제를 작성한다.
- `/ml-problem-explain 중간고사 2회` 또는 예상문제 원본 HTML 경로는 기존 회차의 해설만 생성·보강한다. 문제설명 HTML을 전달한 경우 같은 폴더의 정확한 원본 HTML과 blueprint를 확인해 연결한다.
- 새 제작 요청에서 기존 회차가 있으면 덮어쓰지 않는다. 수정 요청은 지정한 범위만 처리하고 백업한다. 대상이 여러 개면 후보를 제시해 명시하게 한다.
- 새 스킬의 CLI는 저작을 자동으로 대신하지 않는다. 에이전트가 출제표·카드·설명·검산을 작성하고 도구는 조립·검사·발행을 담당한다.
- 기준은 현재 `중간고사대비/예상문제_1회/`와 `.pack/cards/`, `.pack/explanations/`다. `questions.json`, `solutions.json`, `panel-content.json`은 과거 저작/목록 자료이며 최신 HTML 조각을 덮어쓰는 생성 입력으로 사용하지 않는다.
- 참고 이력: `80d29c1` 유도 사슬, `a4ff066` 기호·차원 설명, `7c409d0` 행 미분, `da9dc53` 공식 적용형 간결화, `1d808ef` 영어 본문. 조사 시 HEAD는 `e80b9357c17a4b29f80ae735bbb162f21ba2a8f6`였으며 구현 시작 시 현재 상태를 다시 확인한다.

### 출제·해설 기준

`STT/1019 머러기.md:312,314`의 약 50:50 안내와 사용자의 10문항 지정을 구분해 기록한다. 1회차의 선형대수·미분·Gaussian·ML/MAP·공분산·사후예측·evidence·직교투영 출제표를 기본으로 사용한다. 모델 분석형은 앞 소문항의 결과를 다음 단계에 사용하며, 도출할 최종 공식을 조건/힌트에 미리 제공하지 않는다. 새 회차는 이전 회차와 데이터·조건·요구 과정의 차이를 기록한다. 실제 확인한 과제 번호·교재 PDF 페이지·강의 근거와 변형 종류를 blueprint에 남긴다.

저작 전 `.claude/skills/ml-problem-explain/references/{authoring,verification}.md`와 `.claude/skills/ml-review-pack/references/vector-derivative-convention.md`를 읽는다. 문제의 단서 → 개념/공식 선택 → 실제 첫 줄을 연결하고 긴 설명을 recall/start/solve에 복제하지 않는다. 검산은 별도 계산/논증이며 단순 구조 검사나 본문 반복을 독립 검산으로 부르지 않는다. 독립 검산자는 답·해설을 보지 않고 조건·질문·그림·필요 이론만 받는다.

### 산출 경로와 파일 구조

이하 경로는 저장소 루트 기준이다. `SKILL=.claude/skills/ml-midterm`, `BASE=중간고사대비/예상문제_1회`, `OUT=중간고사대비/예상문제_<N>회`, `RUN=tmp/ml-midterm-skill/<고유ID>`다. 테스트의 OUT은 저장소 안 RUN 하위에 둘 수 있지만 최종 사용자 경로를 자동 변경하지 않는다.

| 경로 | 책임 |
|---|---|
| `SKILL/SKILL.md` | 호출·출제/수정 분기·명령·검토·최종 전달 |
| `SKILL/references/exam-rules.md` | 범위·출제 배분·유도 사슬·출처·회차 차이 기록 |
| `SKILL/references/explanation-rules.md` | 최신 간결화/유도 규칙과 MPE 저작·검증 reference 연결 |
| `SKILL/references/baseline.json` | 기준 커밋과 실제 읽은 템플릿/CSS/실행 자원·렌더 관련 파일의 SHA-256 |
| `SKILL/scripts/exam_config.py` | 회차·경로·프로필·제목·읽음 키·대상 해석 |
| `SKILL/scripts/exam_adapter.py` | EXAM 카드/출제표 검증과 SourcePack 변환, 원 도구의 NFC/NFD 해석 재사용 |
| `SKILL/scripts/build_exam.py` | 기존 문제 HTML/PDF 및 MPE 조립 API 연결 |
| `SKILL/scripts/english_source.py`, `english_pdf.py` | 동일 영어 본문 추출·영어 전용 PDF 조립 |
| `SKILL/scripts/pdf_binding.py` | 영어 추가 이전의 한국어 PDF를 보존해야 할 때만 과거 입력 snapshot과 연결 |
| `SKILL/scripts/check_exam.py`, `browser_check.py` | 산출물·승인·해시 검증과 실제 브라우저 검사 |
| `SKILL/scripts/midterm_cli.py` | 회차 선택 및 아래 명령의 JSON 진입점 |
| `SKILL/tests/conftest.py`, `test_config_adapter.py`, `test_build.py`, `test_explain.py`, `test_delivery.py` | Task 1~4 검증; 기존 공용 모듈 이름과 테스트 import 충돌 방지 |
| `.agents/skills/ml-midterm` | `../../.claude/skills/ml-midterm`을 가리키는 기존 방식의 심볼릭 링크 |
| `.claude/skills/ml-problem-explain/SKILL.md` | 예상문제 분기 추가; 일반 날짜·과제·all 선택 유지 |

OUT에는 `중간고사예상_0909-1019_Midterm_Practice_<NN>.html`, 같은 stem의 `-문제.pdf`, `-답안.pdf`, `-문제-English.pdf`, `문제설명_0909-1019_Midterm_Practice_<NN>.html`을 둔다. NN은 최소 두 자리다. MD·발행 fragments·vendor·manifest·validation·근거는 현재와 같은 `.pack/` 구조다. 소유하지 않은 파일을 새 delivery hash 집합에 무조건 포함하지 않는다.

### 명령 계약과 실행 준비

`midterm_cli.py`의 명령은 `init`, `base`, `english`, `explain`, `publish`, `check`다. 공통 인자는 `--repo`, `--run`; init은 선택적 `--round`, 나머지는 `--out`을 받는다. `check`는 `--run`을 생략해 발행 폴더를 검사할 수 있다. `publish`는 승인된 상세 해설의 발행이며 새 문제/PDF를 자동 생성하지 않는다.

- `init`: 회차 충돌 확인 후 고유 RUN에 `run.json`을 만든다. repo/out/round/range/slug/stem과 mode=`create`를 반환한다. 빈 문제나 pass 검토를 만들지 않는다. 이후 OUT의 입력 작성은 이 run의 대상과 일치해야 한다.
- `base`: 저작된 OUT/.pack 입력을 읽고 기존처럼 임시 HTML/PDF를 검증한 뒤 원본 HTML·한국어 PDF 쌍을 백업 교체한다. HTML에는 한영 본문을 유지하고, 한국어 PDF는 영어 original만 비운 별도 입력 snapshot으로 생성한다. snapshot과 현재 HTML의 한국어 내용 digest를 기존 binding으로 연결한다. 기존 base 발행 흐름을 유지하되 run 상태는 `base_ready`이고 전체 pass가 아니다.
- `english`: 영어 PDF와 검증 보고서를 RUN stage에 생성한다. 최종 교체는 실제 영어 PDF 검수 후 수행한다.
- `explain`: EXAM 원본을 SourcePack으로 읽어 stage HTML/MD/manifest, `review.json`, `explanation-result.json`을 만든다. 네 검토 상태는 매번 not_run이다. base/english를 암묵 실행하지 않는다.
- `publish`: 현재 source/fragment/reference/artifact hash와 정책 버전을 확인하고 공유 `publish_explanation`으로 설명 소유 파일만 교체한다. 영어 PDF는 검수된 stage 파일을 공유 `publish_files`로 별도 교체한다. 전체 완료는 최종 check 이후다.
- `check`: 모든 필수 산출물·실제 소문항 집합·한영 대응·리포트·참조/그림/템플릿 hash·네 검토를 검사한다. JSON `status=pass, errors=[]`와 exit 0이 성공이고 실패는 exit 1이다.

공유 함수의 `publish_files`는 백업/복구가 있는 파일 교체이며 OS 원자적 전체 회차 transaction이 아니다. 중간 실패 시 검증되지 않은 해설을 발행하지 않고 RUN의 실패 단계와 백업 경로를 보고한다. 이미 검증해 만든 기본 문제/PDF가 있더라도 전체 회차 완료로 보고하지 않는다.

실행 시작 때 `python --version`, 로컬 Chrome 및 필요한 import를 확인한다. `uv`는 조사 환경에서 발견되지 않았으므로 필수 실행기로 가정하지 않는다. 필요한 경우 `python -m venv tmp/ml-midterm-skill-venv` 후 해당 venv에만 `pytest playwright pymupdf sympy`를 설치한다. 아래 명령의 `$mlMidtermPython`은 선택한 Python 절대경로다. 새 테스트에는 `pdf`/`browser`/`integration` marker를 등록한다. 테스트 임시 저장은 저장소 내부 `$mlMidtermTestTmp = '<repo>/tmp/ml-midterm-skill-tests/<고유ID>'`를 사용한다.

### Task 1: 회차별 입력 어댑터와 보존 기준

**Files:** Create `SKILL/scripts/{exam_config,exam_adapter}.py`, `SKILL/references/baseline.json`, `SKILL/tests/{conftest,test_config_adapter}.py`.

**Interfaces:**
- Produces frozen `ExamConfig(repo: Path, output: Path, round_number: int)`; 속성 `range_='0909-1019'`, `slug`, `stem`, `title_ko`, `title_en`, `reading_key`, `profile: CardProfile`는 회차에서 계산한다.
- Produces `next_round(repo: Path) -> int`, `config_for_round(repo: Path, number: int | None) -> ExamConfig`, `config_for_output(repo: Path, output: Path) -> ExamConfig`, `resolve_exam_target(repo: Path, target: str) -> ExamConfig`.
- Produces `validate_blueprint(value: dict, repo: Path, config: ExamConfig) -> list[str]`, `load_exam_source(cards_path: Path, blueprint_path: Path, repo: Path, config: ExamConfig) -> SourcePack`, `assemble_cards(card_dir: Path, target: Path, config: ExamConfig) -> Path`, `verify_baseline(repo: Path, baseline_path: Path) -> list[str]`.
- `resolve`와 sha helper는 원 도구에서 재사용한다. import는 명시 repo와 `Path(__file__)` 기준이며 `.git`이 디렉터리라는 가정으로 탐색하지 않는다.

- [x] **Step 1:** 기존 BASE와 공유 생성기·템플릿의 hash를 RUN에 기록하고 아래 실패 테스트를 작성한다. 시험 입력은 BASE의 cards/blueprint 복제이며 실제 BASE는 읽기만 한다.
  - `test_next_round_and_existing_output`: 1회만 있으면 2, 1·3회가 있으면 4; round 0/음수와 기존 out에 대한 init은 거부한다.
  - `test_round_two_profile`: slug=`Midterm_Practice_02`, stem=`중간고사예상_0909-1019_Midterm_Practice_02`, 영문 제목 끝=`02`; 1회/2회의 reading_key가 다르다.
  - `test_blueprint_and_card_contract`: p1~p10/5:5는 통과, 9개/배분 오류/slug 불일치/중복 소문항/출처 hash 변경은 거부한다. 원 도구의 실제 subparts 비교도 유지한다.
  - `test_unicode_worktree_and_paths`: NFC/NFD가 같은 파일로 해석되고 repo 밖/모호한 후보는 거부한다. 복제 repo의 `.git`이 파일인 경우와 저장소 경로 변경도 지원한다.
  - `test_baseline_change_is_reported`: 임시 자원 한 개를 변경하면 해당 경로를 오류에 포함한다. baseline hash를 자동 갱신하지 않는다.

  핵심 assertion 예시(`repo`는 실제 저장소 루트, config 선택 자체는 파일을 쓰지 않는다):

  ```python
  cfg = config_for_round(repo, 2)
  assert cfg.slug == 'Midterm_Practice_02'
  assert cfg.stem == '중간고사예상_0909-1019_Midterm_Practice_02'
  assert cfg.title_en.endswith('02')
  assert cfg.reading_key != config_for_round(repo, 1).reading_key
  ```
- [x] **Step 2:** `& $mlMidtermPython -m pytest .claude/skills/ml-midterm/tests/test_config_adapter.py --basetemp $mlMidtermTestTmp -q` 실행. 새 모듈 부재 또는 동작 assertion으로 FAIL인지 확인한다.
- [x] **Step 3:** 위 인터페이스를 구현한다. 범위/10개/5:5는 유지하고 회차·표제·slug·문항별 소문항 집합만 매개변수화한다. blueprint에 기존 schema_version=1을 유지하고 불필요한 새 스키마를 만들지 않는다.
- [x] **Step 4:** baseline.json에 현재 공유 `review-template.html`, MPE `note-template.html`, PDF 세 템플릿/CSS와 provenance, 로컬 vendor, 조립/페이지 분할/해설 렌더 관련 코드의 경로·SHA-256을 기록한다. 실제 기준 파일과 과거 source hash를 구분한다. template 변경을 자동 승인하지 않는다.
- [x] **Step 5:** Step 2 명령을 다시 실행해 전부 PASS를 확인하고 BASE hash 불변을 확인한다.
- [x] **Step 6:** Task 1 변경만 확인하고 구현 커밋 경계 `feat: add round-aware midterm input adapter`로 정리한다.

### Task 2: 기존 양식의 문제 HTML·한국어/영어 PDF 생성

**Files:** Create `SKILL/scripts/{build_exam,english_source,english_pdf,pdf_binding}.py`, `SKILL/tests/test_build.py`. 원본은 BASE/.pack/tools의 같은 이름 파일이다.

**Interfaces:**
- Consumes Task 1의 `ExamConfig`, `load_exam_source`, `assemble_cards`, `verify_baseline`.
- Produces `build_base(repo: Path, output: Path, run: Path) -> dict[str, Path]` with source/problems_pdf/answers_pdf/pdf_validation; `build_english_pdf(repo: Path, output: Path, run: Path) -> dict[str, Path]` with problems_pdf/report.
- 기존 `english_fields(original, pid, parts)`, `english_digests(problems)`를 유지한다. `load_english_problems(source, blueprint, repo, config)`와 `english_payload(problems, config, pages=None)`로 회차 정보를 전달한다.
- Produces `korean_pdf_source(source: Path, target: Path, config: ExamConfig) -> Path`: 카드의 original 내용만 비운 PDF 입력을 만든다. 카드의 조건·질문·풀이·답·출처를 바꾸지 않는다. 최종 HTML 자체를 수정하지 않는다.
- 공유 `build_review_pdf.build_pack(..., profile=config.profile, layout='video-16x9')`, `review_pdf_publish.publish_files`와 기존 분할·측정 코드를 재사용한다. 한국어 PDF binding도 config를 인자로 받으며 실제 PDF 입력 snapshot이 있을 때만 허용한다. 기존 파일 보존뿐 아니라 새 한영 HTML에서 한국어 PDF를 분리 생성할 때도 이 검증을 사용한다.

- [x] **Step 1:** 실제 입력/출력 테스트를 작성한다.
  - `test_base_payload_has_no_answers`: 문제 payload의 hint/solution/answer가 비고 조건·질문은 온전하다.
  - `test_round_two_english_and_dynamic_subparts`: 임시 2회 카드·blueprint의 p1 소문항 하나를 함께 제거해 총 41개로 만든다. 영어 추출/리포트가 41개이고 02 표제·파일명을 쓰며 질문 순서가 일치한다.
  - `test_english_missing_or_reordered_parts_rejected`: 영어 누락/중복/역순/한글 혼입/번호 override를 거부한다. baseline의 영어 42개는 통과한다.
  - `test_korean_pdf_projection_preserves_full_source`: 전체 HTML은 영어 10문항을 유지하고 PDF 입력은 original만 빈다. 한국어 조건·질문·풀이 digest는 동일하며 report의 source hash는 실제 PDF 입력 snapshot이다. snapshot/current/binding 중 하나를 바꾸면 검증이 실패한다.
  - `test_pdf_layout_and_long_continuation`(`pdf`): 기존 긴 영어 fixture를 현재 렌더러로 실제 생성해 여러 페이지에 소문항이 한 번씩 순서대로 나타나는지 확인한다. 매 페이지 1440×810pt와 하단135pt 흰 픽셀을 검사한다.

  41소문항 입력 생성 후의 assertion:

  ```python
  assert report['logical_count'] == 10
  assert report['subpart_count'] == 41
  assert pdf.name.endswith('Midterm_Practice_02-문제-English.pdf')
  assert korean_content_digest(full_source, config) == korean_content_digest(snapshot, config)
  ```
- [x] **Step 2:** `& $mlMidtermPython -m pytest .claude/skills/ml-midterm/tests/test_build.py --basetemp $mlMidtermTestTmp -q` 실행해 누락 모듈/기존 고정값에서 FAIL을 확인한다.
- [x] **Step 3:** 기존 도구를 포팅하고 Task 1 config를 연결한다. `STEM`, `EXAM`, `Practice 01`, 한국어 1회 표제, 리포트 42를 제거한다. shared 템플릿/공유 생성기는 수정하지 않는다. source_vendor 상대경로와 로컬 영어 PDF 자원 처리를 유지한다. `build_pack`에는 전체 한영 HTML 대신 `korean_pdf_source`의 출력을 전달한다.
- [x] **Step 3a:** `korean_content_digest(source: Path, config: ExamConfig) -> str`를 기존 binding 함수에서 포팅하고, `.pack/evidence/korean-pdf-source/<STEM>.html`에 실제 한국어 PDF 입력 snapshot을 보존한다. 문제·답안 PDF와 리포트가 그 snapshot에 연결되고, 발행 HTML의 한국어 digest가 같은 경우에만 binding을 기록한다.
- [x] **Step 4:** Step 2를 재실행해 PASS를 확인한다. 1회 입력을 RUN 안의 `예상문제_1회` 복제에 재생성하고 PDF 텍스트·페이지 매핑·렌더 이미지를 기준과 비교한다. PDF 생성 시각 등 metadata는 화면 동일성 비교에서 제외하되 의미·수식·여백은 제외하지 않는다.
- [x] **Step 5:** 세 PDF의 전체 페이지를 렌더해 실제 시각 검토한다. 한글·정답 유출·외부 요청·KaTeX/geometry 오류는 0이어야 한다. BASE hash 불변을 확인하고 커밋 경계 `feat: reuse midterm layouts for every round`로 정리한다.

### Task 3: 예상문제 해설 생성·승인·발행 연결

**Files:** Extend `SKILL/scripts/build_exam.py`; Create `SKILL/scripts/check_exam.py`, `SKILL/tests/test_explain.py`. 기존 MPE 구현은 수정하지 않는다.

**Interfaces:**
- Consumes Task 1 SourcePack과 Task 2의 원본 HTML, OUT/.pack/explanations/pN.html.
- Produces `build_explain(repo: Path, output: Path, run: Path) -> dict` with pack:`SourcePack`, artifacts:`Artifacts`, review_path:`Path`; `publish_explain(repo: Path, output: Path, run: Path) -> tuple[Path, ...]`; `check_delivery(output: Path, repo: Path) -> list[str]`.
- 공유 `mpe_render.build_explanation`, `check_artifacts`, `artifact_hashes`, `mpe_contract.initial_reviews/validate_reviews`, `mpe_publish.publish_explanation`을 사용한다. `explanation-result.json`은 기존 stage/html/md/manifest/files/review_path 키를 유지한다.
- run/index는 조립 당시 source와 조각의 hash를 담고 publish 때 현재 입력과 대조한다. `publish_explain`은 run의 artifact 파일 목록을 검증해 `Artifacts`를 복원하고 같은 source로 `SourcePack`을 다시 읽는다.

- [x] **Step 1:** 다음 실패 테스트를 작성한다.
  - `test_explanations_override_stale_inventory`: solutions.json/panel-content.json에 의도적으로 오래된 답을 넣어도 현재 explanations의 풀이·sum·용어가 HTML/MD에 나타난다. 질문·답을 자동 교정하지 않는다.
  - `test_every_subpart_has_solve_verify`: 실제 입력의 모든 소문항이 두 구역에 각각 대응하고 일곱 구역 순서 및 펼친 본문을 기존 validate_fragment로 검사한다.
  - `test_build_resets_reviews_and_preserves_problem_files`: build 직후 네 검토는 not_run이고 원본 HTML·cards·영어 본문·PDF 3개의 SHA-256은 동일하다. title은 `머신러닝기초 중간고사 모의평가 N회 문제설명`이며 원본 링크/읽음 키는 해당 회차다.
  - `test_publish_rejects_stale_or_unreviewed`: source/fragment/reference 그림/artifact/정책 버전 변경, 누락 검토를 각각 거부한다. 위조 통과 기록을 테스트 외 산출물로 남기지 않는다.
  - `test_publish_only_owns_explanation_files`: 허용된 해설 파일만 바꾸며 명시적 공유 발행 API 호출 전후 원본·PDF는 동일하다. 교체 실패 주입 시 이전 해설 파일을 복구한다.

  build 직후의 assertion(`review`는 새 review.json 내용):

  ```python
  assert all(review[key]['status'] == 'not_run'
             for key in ('source_visual', 'content', 'independent', 'browser'))
  assert after_non_owned_hashes == before_non_owned_hashes
  assert set(solve_parts) == set(verify_parts) == set(problem.subparts)
  ```
- [x] **Step 2:** `& $mlMidtermPython -m pytest .claude/skills/ml-midterm/tests/test_explain.py --basetemp $mlMidtermTestTmp -q`로 FAIL을 확인한다.
- [x] **Step 3:** 기존 build_explain을 회차화한다. 제목 치환은 기존처럼 문서의 정확한 공유 표제만 대상으로 하고 실패/중복 시 진단한다. 글꼴·CSS·UI script를 변형하지 않는다. 공유 조각 정규화/상대 링크 변환은 유지한다.
- [x] **Step 4:** publish_explain과 check_delivery를 구현한다. 구조·입력/참조·실제 항목 집합·승인/산출 hash를 기존 계약으로 검증하고 validation.json의 자기 해싱 순환을 만들지 않는다. 영어 PDF 존재·현재 본문 digest·hash도 전체 check에 포함한다. 해설만 작업의 check는 기존 PDF 승인도 검사하지만 재생성하지 않는다.
- [x] **Step 5:** Step 2를 재실행해 PASS를 확인하고 기존 MPE `test_contract.py`, `test_publish.py`, `test_row_review_policy.py`를 별도 pytest 프로세스로 실행한다. 기존 테스트의 임시 경로/fixture 문제와 신규 회귀를 구분해 기록한다.
- [x] **Step 6:** Task 3의 소유 파일만 확인하고 커밋 경계 `feat: connect midterm cards to problem explanations`로 정리한다.

### Task 4: CLI와 실제 전달·화면 회귀 검증

**Files:** Create `SKILL/scripts/{midterm_cli,browser_check}.py`, `SKILL/tests/test_delivery.py`; Extend `SKILL/scripts/check_exam.py`.

**Interfaces:**
- Consumes Task 1~3의 모든 공개 함수와 명령 계약. Produces `main(argv: list[str] | None = None) -> int` in midterm_cli.py; `run_check(path: Path, evidence: Path, shots: Path) -> dict` in browser_check.py.
- 실제 브라우저 리포트는 html_sha256/topic_ids/viewports/screens/original_checks/print_checks/errors/status를 기존 의미로 유지한다. 문항·소문항 수는 실제 입력에서 얻는다.

- [x] **Step 1:** CLI subprocess와 파일 보존을 검증하는 테스트를 작성한다.
  - `test_init_selects_next_and_rejects_existing`: 지정/생략 회차 JSON과 기존 폴더 충돌을 검사한다. init이 새 문제·PDF·승인을 만들지 않는지 확인한다.
  - `test_explain_target_resolution`: `중간고사 2회`, 원본 HTML, 대응 문제설명 HTML은 같은 원본을 선택한다. 여러 원본 후보와 repo 밖 경로는 거부한다. 일반 복습/과제 경로를 이 resolver가 가져가지 않는다.
  - `test_cli_explain_never_runs_base`: base/english를 실패 stub으로 바꾸어도 explain은 동작하고 비소유 파일 hash는 동일하다.
  - `test_check_rejects_wrong_round_and_incomplete_delivery`: 다른 회차 링크/리포트·빠진 PDF·오래된 browser hash·누락 영어·not_run은 exit1과 구체 errors를 반환한다.
  - `test_publication_failure_restores_existing_files`: 공유 파일 교체에 실패를 주입해 덮어쓴 파일이 복구되고 전체 pass가 기록되지 않는지 검사한다.

  불완전 전달 check subprocess의 assertion:

  ```python
  assert result.returncode == 1
  assert json.loads(result.stdout)['status'] == 'fail'
  assert json.loads(result.stdout)['errors']
  assert preserved_hashes_after == preserved_hashes_before
  ```
- [x] **Step 2:** `& $mlMidtermPython -m pytest .claude/skills/ml-midterm/tests/test_delivery.py --basetemp $mlMidtermTestTmp -q`로 FAIL을 확인한다.
- [x] **Step 3:** CLI를 구현하고 기존 browser_check를 포팅한다. 회차/주제 집합은 config와 DOM에서 확인한다. 1280×900·1024×900·375×812 × light/dark의 모든 문항, 1023→1024 경계, 저장된 닫힘, 도킹/이동/크기 조절, 목차·이전/다음·요약·원문·키보드·reload·모바일·인쇄를 유지한다. 원문 없는 fallback은 별도 시험 입력으로 확인하되 새 제작 카드의 영어 누락을 허용하지 않는다.
- [x] **Step 4:** Step 2를 재실행해 PASS를 확인한다. 이어 별도 integration 실행에서 BASE 복제 및 41소문항 2회 시험 입력을 실제 생성한다. 시험 입력은 실전 회차로 전달하지 않고 실제 근거 없는 수학 검토 pass를 만들지 않는다.
- [x] **Step 5:** 같은 Chrome·화면·테마·UI 상태에서 기준 1회 HTML과 새 생성 HTML을 비교한다. 단순 텍스트 keyword 검사 대신 CSS/실행 script 동일성과 DOM 조건/질문/영문/풀이/요약/용어 일치, 대표 화면 screenshot을 함께 확인한다. 추가/삭제된 문항·수식은 무시 항목으로 두지 않는다.
- [x] **Step 6:** 로컬 수식·자원·콘솔·문서 가로 넘침 오류 0, 모든 문항 원문 일치, 인쇄 한국어/영어 보존을 실제 확인한다. 1회 복제의 문항 수는 10이고 영어 검사는 60조합이어야 한다. 시험 입력의 항목 수는 41로 기록한다. 소유 범위·BASE hash 불변을 확인하고 커밋 경계 `test: verify midterm delivery and layout preservation`로 정리한다.

### Task 5: 스킬 지침·MPE 라우팅·최종 설치 검증

**Files:** Create `SKILL/SKILL.md`, `SKILL/references/{exam-rules,explanation-rules}.md`, `.agents/skills/ml-midterm` link; Modify `.claude/skills/ml-problem-explain/SKILL.md:1-27`(대상/설명 및 EXAM 실행 분기).

**Interfaces:**
- Consumes 위 명령 계약과 검증 결과. Produces `/ml-midterm [N회]`의 신규 제작/명시적 수정 경로, `/ml-problem-explain 중간고사 N회|HTML경로`의 설명 전용 경로.
- 일반 mpe_cli의 extract/load_source는 예상문제 입력을 지원하지 않으므로 새 분기는 Task 4 CLI의 explain/publish/check로 보낸다. 일반 날짜·기간·과제·인자 없음·all은 원 경로를 유지한다.

- [x] **Step 1:** `skill-creator`와 `writing-skills`를 읽고 이 작업의 적용 범위를 확인한다. 다음 행동 검증표를 RUN에 만든다: 새2회·회차생략·기존2회 새출제 충돌·2회 해설만·명시 HTML·일반1007·과제1·all·출처 미확인·수학 충돌·템플릿 변경. 각 행에 기대 선택 경로와 보존 파일을 명시한다.
- [x] **Step 2:** SKILL.md와 두 reference를 작성한다. 확정 제작 명세의 출제표·회차 차이·공식 적용/유도 구분·기호/차원·독립 검산·출처 기록을 연결한다. 자세한 공유 규칙은 중복 복사하지 않고 해당 authoring/verification/vector reference를 필수 읽기로 연결한다. 실행기가 문제를 자동 작성한다는 안내를 넣지 않는다.
- [x] **Step 3:** MPE frontmatter/대상/실행 분기에 기존 예상문제 지원을 추가한다. 기존 ‘원본 보존’은 유지하고 ‘새 출제’는 ml-midterm으로 연결한다. forecast 자동 선택이나 all 범위 확대를 하지 않는다. `.agents` 링크를 기존 프로젝트와 같은 방식으로 만들고 실제 해석된 원본 경로를 확인한다.
- [x] **Step 4:** `& $mlMidtermPython C:/Users/Hyunjun/.codex/skills/.system/skill-creator/scripts/quick_validate.py .claude/skills/ml-midterm`을 실행해 유효한 frontmatter/name/description을 확인한다. baseline·상대 reference·명령 경로·링크를 실제 resolve하고 Task 1~4 전체 테스트를 실행한다. 단순 문구 존재 검사를 행동 검증으로 대체하지 않는다.
- [x] **Step 5:** Step 1의 요청별로 도구 선택·필수 읽기·출력 범위를 실제 지침을 읽으며 검토한다. 공식 적용형 p4(b,c)/p8(d~f)와 유도형 p6/p7/p10을 대조해 최신 규칙을 오래된 장황한 설명으로 되돌리지 않는지 확인한다. independent 검산은 미래 실제 출제 호출 시 수행하며 스킬 설치 검증의 수동 점검을 그 결과로 보고하지 않는다.
- [x] **Step 6:** BASE 및 다른 수업 자료의 hash 불변, `git diff --check`, 변경 경로 제한을 확인한다. 실행 중 확인한 실패/누락은 RUN의 검증 기록에 남긴다. 새 스킬 링크·사용 예·실제 테스트 결과를 전달하고 커밋 경계 `feat: add ml-midterm skill and explanation routing`로 정리한다. 요청 없는 새 예상문제 출제/원격 push는 하지 않는다.

## 계획 자체 검토

- 명세 대응: 회차/출처/범위/고정값은 Task1, 문제 HTML·PDF·영문은 Task2, 최신 해설·공유 API·승인은 Task3, 실제 UI·최종 전달 조건은 Task4, 스킬 저작·호출·MPE 연결은 Task5에 배정했다.
- 인터페이스: 기존 build_base/build_english_pdf/build_explain의 repo/output/run 계약을 유지한다. 새 config와 SourcePack은 Task1에서 정의하며 공용 mpe_cli의 run.json/stage.json과 전용 explanation-result.json을 혼용하지 않는다.
- 양식 보존: 공유 템플릿을 새로 디자인하지 않고 baseline 변경 진단과 같은 입력의 재생성·실제 화면/PDF 비교로 검증한다. 스킬 설치 자체가 기존 1회 재발행이 되지 않도록 모든 시험 출력은 RUN 안에 둔다.
- 한국어 PDF 입력: 공용 PDF는 original이 있으면 함께 인쇄한다(`review_pdf_payload.py:85`, `pdf-problem.html:513`, `pdf-answer.html:572`). 영어 추가 전 PDF를 보존한 현재 기준을 재현하기 위해 Task2에서 별도 한국어 입력 snapshot과 digest binding을 만들며 최종 HTML의 영어는 보존한다.
- 위험 대응: Review Focus 1~5를 각 작업의 이름 있는 검증에 배정했다. 구조·수학·번역·원문 대조·브라우저 시각 검토를 구분했다. 과거 pass 복사나 입력 없는 독립 검산 승인은 허용하지 않는다.
- 환경: Python은 발견됐고 uv는 발견되지 않았다. venv 실행 경로를 명시했고 기본 Python에 선택 라이브러리가 설치됐다고 가정하지 않는다. 기존 도구와 같은 모듈명을 쓰는 새 테스트는 기존 테스트와 별도 프로세스로 실행해 import 충돌을 피한다.
- 실행 방식 추천: **Native**. 다섯 작업이 같은 config·원본·해설·검토 계약을 순서대로 공유하므로 한 구현자가 연결을 유지하고 마지막 전체 변경 검토를 별도 검토자에게 맡기는 편이 적절하다. 사용자의 선택 전 구현하지 않는다.
