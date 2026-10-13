# 머신러닝기초 복습 영상 스킬 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** bio-review-video와 같은 제작 기능을 머신러닝기초에 맞게 제공하고, 생명과학 .env를 로컬로 복사해 TTS API 키를 사용한다.

**Architecture:** 기존 영상 스킬을 프로젝트 로컬에 복제하여 제작·재개·검증 계약을 유지한다. 자료 탐색·수학 설명·템플릿 연결을 조정하고 .env 설치와 계산 증거 검사를 작은 모듈로 추가한다. 생명과학 저장소에 런타임 의존성을 만들지 않는다.

**Tech Stack:** Python 3.10+, unittest, HTML/SVG, GSAP, KaTeX, HyperFrames, FFmpeg/ffprobe, Vertex AI TTS.

**Spec:** `docs/superpowers/specs/2026-10-06-ml-review-video-design.md` (실행자는 계획과 설계를 모두 읽는다).

## Global Constraints

- 설치 위치는 `.agents/skills/ml-review-video/`; 이 문서에서 `SKILL`은 그 경로, `REPO`는 머신러닝기초 저장소 루트다.
- `BIO_SKILL`은 `/Users/hyunjun_macbook_pro/Documents/Univ/생명과학/.agents/skills/bio-review-video/`다. 복사 원본만 읽고 변경하지 않는다.
- 원자료에서 노트 생성은 ml-review-pack이 담당한다. 원자료·기존 노트·기존 템플릿을 수정하지 않는다.
- 주제별 1–3분 목표·필요시 연장, Aoede·가로형·자동 완주·비용 상한 없음·사용량 기록.
- 다크모드·Pretendard·로컬 KaTeX·1920×1080·30fps, 모델 `gemini-2.5-flash-tts`, 공급자 `vertex-ai-express`를 유지한다.
- `.env`는 루트에만 복사하고 권한 0600. 키·파일 내용·키 해시는 출력·저장·커밋하지 않는다.
- 유료 API 호출 없이 구현 검사를 완료한다. 실제 키의 인증 성공을 로컬 로딩 성공으로 주장하지 않는다.
- 스킬 실행 시 HyperFrames entry skill을 읽는다. 이번 구현은 전체 새 영상 제작을 포함하지 않는다.
- 커밋·푸시는 직접 요청이 있을 때만 한다. 아래 커밋 단계는 요청이 없으면 생략하고 후보 메시지만 보고한다.

## Review Focus

1. 목적지 .env가 이미 다른 내용일 때 덮어쓰지 않음 — Task 2의 conflict test.
2. 셸에 다른 API 키가 있을 때 명시한 .env 키 사용 — Task 2의 precedence test.
3. NFD 경로·기간 노트·예고 내용이 섞였을 때 올바른 입력과 범위 유지 — Task 3의 Unicode/range/preview tests.
4. 수식 또는 그래프 계산 증거가 검토 후 변경되었을 때 완료 무효화 — Task 4의 fingerprint test.
5. 형제 영상 실패·출판 중단 후 재실행할 때 성공 결과와 기존 링크 보존 — Task 6의 inherited batch tests와 integration smoke.

## 파일 구성

- `SKILL/SKILL.md`, `agents/openai.yaml`: 호출 조건·전체 흐름·과목명·입출력.
- `SKILL/references/{selection-and-batches,sources-and-coverage,narration-and-motion,voice-and-budget,rendering-and-verification}.md`: 복제 후 과목 계약 수정.
- `SKILL/assets/{defaults.json,vertex-direction.txt,video-layout.css}`: 기본 설정·한국어 수학 발화·영상 배치.
- `SKILL/scripts/video.py`, `scripts/lib/*.py`: 기존 로컬 파이프라인. 필요 없는 구조 변경 없이 보존.
- `SKILL/scripts/lib/credentials.py`, `scripts/setup_env.py`: 충돌 없는 로컬 .env 설치.
- `SKILL/scripts/lib/math_evidence.py`: 수식·그래프 증거 구조와 파일 무결성 검사.
- `SKILL/tests/`: 기존 회귀 검사 복제, 과목 입력·인증·계산 증거·통합 검사 추가.
- `REPO/.env`: 실행 시 복사, Git 제외. 기존 `.gitignore`의 `.env` 규칙을 유지한다.

모든 파일 경로는 REPO 기준이다. 셸 명령의 `SKILL`은 실행 시 절대 경로로 정의하며 원본 또는 키 값을 변수로 출력하지 않는다.

---

### Task 1: 독립적인 머신러닝 영상 파이프라인과 호출 계약

**Files:** Create `SKILL/` 아래 기존 스킬의 scripts, assets, references, tests, SKILL.md, agents/openai.yaml. Create `SKILL/tests/test_ml_skill.py`.

**Interfaces:** 기존 `scripts/video.py`의 parser/main과 prepare-set, resume-set, publish-set, prepare, resume, revoice 명령 계약을 그대로 제공한다. 이후 task가 `scripts.lib` 모듈을 수정한다.

- [x] **Step 1:** `test_ml_skill.py`를 작성한다. `SKILL.md`의 name이 `ml-review-video`, metadata의 표시명이 머신러닝기초, defaults의 voice/width/height/fps/budget_usd가 `Aoede/1920/1080/30/None`이며 로컬 `scripts/video.py`가 존재하는지 검사한다.
- [x] **Step 2:** `python3 -m unittest discover -s "$SKILL/tests" -p test_ml_skill.py -v` 실행. 구현 파일 부재로 FAIL이어야 한다.
- [x] **Step 3:** BIO_SKILL의 위 파일만 복사한다. __pycache__, 실제 실행 산출물, 인증 파일은 복사하지 않는다. 이름·description·metadata·내레이터 지시를 머신러닝기초로 바꾸고 템플릿 경로를 `REPO/.agents/skills/ml-review-pack`으로 바꾼다. 명령별 동작은 유지한다.
- [x] **Step 4:** 위 단위 검사와 `python3 "$SKILL/scripts/video.py" --help`를 실행한다. PASS이고 기존 명령이 모두 표시되어야 한다. 기존 전체 unittest도 실행하여 복제 기준 결과를 남긴다.
- [x] **Step 5:** 요청이 있을 때만 해당 스킬 파일을 커밋한다. 후보: `feat(skills): add local ml review video pipeline`.

### Task 2: .env 로컬 복사와 명시적 키 선택

**Files:** Create `SKILL/scripts/lib/credentials.py`, `SKILL/scripts/setup_env.py`, `SKILL/tests/test_credentials.py`. Modify `SKILL/scripts/lib/vertex_tts.py:load_key`, `SKILL/references/voice-and-budget.md`, `SKILL/SKILL.md`.

**Interfaces:** `copy_env_file(source: Path, destination: Path) -> str`는 `copied` 또는 `reused`를 반환한다. 원본 부재·symlink·상이한 목적지에는 `CredentialError`를 발생시킨다. CLI `setup_env.py --source PATH --destination PATH`는 상태만 출력하고 실패 시 exit 1. 기존 `load_key(env_file=None) -> str`의 반환 계약은 유지한다.

- [x] **Step 1:** 임시 폴더와 가짜 키로 테스트 작성: `test_copy_mode_0600`은 바이트 동일성과 mode 0600, `test_reuse_identical`은 reused, `test_conflict_preserves_destination`은 오류와 목적지 불변, `test_missing_and_symlink_rejected`는 오류, `test_explicit_file_precedes_environment`는 env_file 키 선택, `test_environment_fallback_without_file`은 환경변수 키 선택, `test_cli_never_prints_secret`는 stdout/stderr에 가짜 키가 없음을 단언한다. 테스트는 실제 .env를 읽지 않는다.
- [x] **Step 2:** `python3 -m unittest discover -s "$SKILL/tests" -p test_credentials.py -v` 실행. 새 설치 모듈 부재와 기존 키 우선순위로 FAIL이어야 한다.
- [x] **Step 3:** 복사 모듈과 CLI를 구현한다. 목적지는 exclusive create로 만들고 중간 실패에 새 목적지만 제거한다. 기존 동일 파일은 권한만 0600으로 조정한다. 명시 env_file은 파일 내부 GOOGLE_API_KEY → GEMINI_API_KEY 순서, 없으면 오류; env_file 미지정 시만 환경변수 fallback. 오류 메시지는 키와 파일 내용을 포함하지 않는다.
- [x] **Step 4:** Task 2 검사와 기존 `test_tts.py`를 실행하여 PASS를 확인한다. 기존 precedence 기대가 있다면 새 명시 파일 계약으로 갱신하고 무파일 fallback 검사를 보존한다.
- [x] **Step 5:** 실제 설치를 수행한다: 원본/목적지의 symlink 여부와 `git check-ignore .env`를 확인한 뒤 `python3 "$SKILL/scripts/setup_env.py" --source /Users/hyunjun_macbook_pro/Documents/Univ/생명과학/.env --destination "$REPO/.env"`. 복사 뒤 파일 권한과 Git 제외를 확인하고, `load_key`를 호출해 성공 여부만 출력한다. 키나 파일 내용은 출력하지 않고 네트워크 호출하지 않는다.
- [x] **Step 6:** `SKILL.md`와 음성 문서에 설치·충돌·`--env-file <REPO>/.env` 전달을 명시한다. prepare-set/tts가 이미 이 인자를 지원하므로 API를 새로 만들지 않는다. config에는 env_file 경로만 저장한다.
- [x] **Step 7:** 요청이 있을 때만 코드·검사·문서를 커밋한다. `.env`는 staging 목록에 포함하지 않는다. 후보: `feat(skills): configure local ml video credentials`.

### Task 3: 머신러닝 자료 발견과 선정 기준

**Files:** Modify `SKILL/scripts/lib/sources.py:discover`, `SKILL/references/{selection-and-batches,sources-and-coverage}.md`, `SKILL/SKILL.md`. Create `SKILL/tests/test_ml_sources.py`, `SKILL/tests/fixtures/ml-notes/`의 합성 자료.

**Interfaces:** `discover(repo, selector) -> dict`의 `range/files/missing_optional`과 파일 `id/kind/path/sha256` 형식을 유지한다. 장마감은 발견되면 읽되 누락 경고의 기본 요구에서는 제거한다. selection.json 기존 schema v1을 유지한다; 예고 제외는 에이전트의 결정과 이유로 기록한다.

- [x] **Step 1:** `test_no_chapter_audit_warning`은 장마감 없는 정리노트/복습문제에서 missing_optional에 chapter-audit가 없음을 단언한다. `test_unicode_range_and_figures`는 NFD 이름과 두 날짜 폴더에서 정확한 range·노트·문제·그림 해시가 반환되는지 검사한다. 기존 범위 중복·unsafe symlink 검사도 보존한다.
- [x] **Step 2:** `python3 -m unittest discover -s "$SKILL/tests" -p test_ml_sources.py -v` 실행. chapter-audit 기대에서 FAIL이어야 한다.
- [x] **Step 3:** discover의 장마감 누락 취급만 변경하고 기존 파일 발견·해시·경로 검사를 유지한다. 선정 문서에 학습 범위/교과서 보충/예고 구분, 조건·단위·차원, 실제 상태 변화 기준과 예고 제외 예시를 추가한다. MML 페이지와 강의 슬라이드/STT locator를 coverage에 남기도록 한다.
- [x] **Step 4:** `test_ml_sources.py`, `test_sources.py`, `test_selection.py` 실행. 모두 PASS. 읽기 전용으로 실제 0930 자료를 discover하여 기대한 노트·문제·그림이 잡히는지 확인한다.
- [x] **Step 5:** 합성 노트에 배운 prior/posterior와 preview 최적화를 넣고 에이전트가 selection fixture를 작성한다. `test_preview_selection_fixture`에서 예고는 text+범위 밖 이유, 배운 내용만 clip requirement_ids, context는 prerequisite_ids에 포함됨을 검사하고 기존 require_selection을 통과시킨다. 이는 예시의 계약 검사이며 임의 노트 의미를 자동 판별한다는 주장으로 사용하지 않는다.
- [x] **Step 6:** 요청 시 커밋 후보: `feat(skills): adapt video sources and selection to ml`.

### Task 4: 계산·그래프 검증 증거와 완료 지문

**Files:** Create `SKILL/scripts/lib/math_evidence.py`, `SKILL/tests/test_math_evidence.py`. Modify `SKILL/scripts/lib/verify.py:review_fingerprint,verify_run`, `SKILL/scripts/lib/state.py:stage_fingerprint`, `SKILL/references/{narration-and-motion,rendering-and-verification}.md`.

**Interfaces:** `validate_math_evidence(run: Path, manifest: dict) -> list[str]`는 `source/math-evidence.json`의 오류 목록을 반환한다. `math_evidence_files(run: Path) -> list[Path]`는 지문에 포함할 파일들을 반환한다. 모든 경로는 RUN 내부 일반 파일이며 traversal·외부 symlink를 거부한다.

계약: JSON은 `schema_version:1`, `scenes` 배열. 각 장면은 `scene_id`, `mode`(`numeric` 또는 `qualitative`), `formula_refs`, `conditions`, `axes`, `units`, `dimensions`를 가진다. numeric에는 `calculation_script`, `calculation_result`, `states`(start/middle/end 각 label·figure_path·values)가 추가된다. 파일마다 기록된 sha256을 검사한다. qualitative는 숫자/계산을 쓰지 않는 이유를 필수로 기록한다. scene ID 누락/중복/미지의 참조를 거부한다. 의미 정확성은 coverage와 내용 검토에 기록한다.

- [x] **Step 1:** `test_numeric_evidence_complete`, `test_qualitative_reason_required`, `test_missing_scene_or_axes`, `test_unsafe_evidence_path`, `test_modified_result_invalidates_review`를 작성한다. 마지막 검사는 계산 결과를 바꾸면 review fingerprint가 달라지고 이전 검토로 verify_run을 완료할 수 없음을 단언한다.
- [x] **Step 2:** `python3 -m unittest discover -s "$SKILL/tests" -p test_math_evidence.py -v` 실행. 새 모듈 부재로 FAIL이어야 한다.
- [x] **Step 3:** 증거 구조·참조·파일 해시 검사를 구현한다. 지문 함수에 math-evidence.json과 관련 계산·결과·그림 파일을 포함한다. verify_run은 증거 오류가 있으면 기존 실패 보고 형식으로 완료를 막는다. 계산 스크립트를 자동 실행하지 않고 에이전트가 실행한 결과와 의미를 검토한다.
- [x] **Step 4:** 테스트와 기존 state/verify/batch 검사를 실행한다. 기존 가짜 RUN fixture에 최소 qualitative 증거를 추가하여 새 스킬의 완료 계약과 맞춘다. PASS 확인.
- [x] **Step 5:** 설명 문서에 수식 원문/발화 분리, 변수-화면 매핑, 축·단위·조건, 계산 실행과 근거 기록, 범위 밖 유도 제외를 명시한다. 기존 motion은 유지하고 계산된 SVG 상태를 순차 reveal/highlight하도록 예시를 제공한다.
- [x] **Step 6:** 요청 시 커밋 후보: `feat(skills): require math evidence for ml review videos`.

### Task 5: 머신러닝 템플릿과 로컬 수식 화면

**Files:** Modify `SKILL/tests/test_theme.py`, `SKILL/tests/test_composition.py`, `SKILL/tests/browser_check.mjs`, `SKILL/references/narration-and-motion.md`. Modify `SKILL/scripts/lib/{theme,composition}.py`는 검사로 확인된 호환 결함이 있을 때만 한다.

**Interfaces:** 기존 `snapshot_theme(pack, run)`, `stage_assets(source, run)`, `assemble(m, timeline, theme, run)` 유지. PACK은 REPO/.agents/skills/ml-review-pack. 외부 CDN 없이 assets/fonts 및 assets/vendor/katex를 사용한다.

- [x] **Step 1:** `test_ml_pack_snapshot`은 실제 ml-review-pack 템플릿과 snapshot의 해시 동일성·다크 토큰을 확인한다. `test_math_requires_complete_local_assets`는 KaTeX JS/CSS/auto-render/fonts 중 누락을 거부함을 검사한다. `test_math_scene_renders` 브라우저 fixture에는 분수·적분·첨자와 세 그래프 상태를 넣고 KaTeX 오류 0, 남은 수식 delimiter 0, 수식/축 텍스트 넘침 0을 검사한다.
- [x] **Step 2:** 위 검사를 실행하여 현재 지원/결함을 구분한다. 이미 PASS인 템플릿 기능은 변경하지 않는다. 자산 누락 등 실제 FAIL만 재현 기록으로 남긴다.
- [x] **Step 3:** 재현된 결함만 고친다. renderer 준비 시 font와 KaTeX 완전성을 확인하고 렌더 전 font 준비를 기다린다. 그래프는 계산된 SVG 상태를 기존 timeline에서 순차 표시하며 임의 SVG path morph 기능을 추가하지 않는다.
- [x] **Step 4:** 브라우저로 시작·중간·끝 상태를 seek하여 확인한다. `test_theme.py`, `test_composition.py`와 browser_check의 기존 호출 인터페이스로 검사를 실행해 PASS 확인. 대표 이미지를 직접 읽어 기호·축·색·대비를 확인한다.
- [x] **Step 5:** 요청 시 커밋 후보: `fix(skills): verify local math rendering for ml videos`.

### Task 6: 제작·재개·전달 통합 검증과 스킬 완성

**Files:** Modify `SKILL/tests/integration_smoke.py`, `SKILL/tests/test_selection.py`, `SKILL/SKILL.md`, `SKILL/references/{selection-and-batches,voice-and-budget,rendering-and-verification}.md`, `SKILL/agents/openai.yaml`.

**Interfaces:** Task 1의 기존 CLI, Task 2의 로컬 env_file, Task 3의 sources/selection, Task 4의 math evidence, Task 5의 실제 template/assets를 통합한다. publish-set/resume-set/revoice 기존 CLI 변경 없음.

- [x] **Step 1:** 기존 integration_smoke 호출 인자를 읽고 합성 선형회귀 fixture를 추가한다. 점 (0,0),(1,1),(2,2), 절편 0, 기울기 0/1/2에 대해 SSE가 5/0/5임을 unittest로 고정한다. start/middle/end SVG와 계산 결과를 해당 fixture에 연결한다.
- [x] **Step 2:** 가짜 TTS/로컬 PCM만으로 prepare-set → check → assemble → render → verify → publish-set을 수행한다. 핵심 검사: math evidence 포함, 최종 MP4와 제작자료 위치, 최종 결과 링크·해시, 1920×1080/30fps·오디오 존재, 현재 지문으로 verify 성공. 외부 TTS transport가 호출되면 실패하게 한다.
- [x] **Step 3:** 기존 0·1·N개, 형제 실패/재개, publish 중단/재시도, 이전버전·링크 보존, revoice 검사를 새 자료로 실행한다. 새 계산 증거를 갱신하지 않은 stale review는 완료를 막아야 한다. 실패 때 성공 음성 캐시를 재사용해야 한다.
- [x] **Step 4:** `python3 -m unittest discover -s "$SKILL/tests" -v`와 `python3 /Users/hyunjun_macbook_pro/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$SKILL"` 실행. 모두 PASS. integration_smoke는 기존 CLI의 실제 인자로 실행하며 브라우저·ffprobe 증거를 기록한다. 런타임 자산이 없으면 설치 가능한 로컬 의존성을 준비하고 재검사하며 생략을 PASS로 보고하지 않는다.
- [x] **Step 5:** SKILL.md·metadata·references에서 잔여 생명과학 지시/예시를 검색한다. 목소리·수식 발화·선정·template·env-file·resume·revoice·전체 복습·출력·실패 처리 계약을 self-review한다. 테스트의 bio fixture 이름은 역사적 회귀 입력이면 유지 가능하나 사용자-facing 지시는 모두 ML로 바꾼다.
- [x] **Step 6:** git status와 diff, 실제 .env ignored 여부를 확인한다. 구현 파일·검사 결과·로컬 .env 설치 여부·실제 인증 미검증을 보고한다. API 키 또는 .env는 diff·보고서·제작자료에 포함하지 않는다.
- [x] **Step 7:** 요청 시 커밋 후보: `test(skills): validate ml review video workflow`. 이 단계는 유료 영상 제작이나 push를 포함하지 않는다.

## 계획 자체 검토 결과

- 선정·전체 복습·review·resume·revoice·출력·기존 결과 보존은 Task 1/3/6, 음성 설정·.env는 Task 2, 수학 검증은 Task 4, 화면은 Task 5에 대응한다.
- 기존 공개 함수/명령 계약을 유지한다. 새 인터페이스는 credentials와 math_evidence에만 둔다.
- Review Focus 5항목은 소유 task의 검사에 연결했다.
- 원본 스킬을 수정하거나 공용 엔진을 새로 만드는 작업은 없다. 최초 검증에 실제 API 비용은 없다.
- 계획 작성 시 .env 존재와 ignore 규칙만 확인했다. .env 복사·스킬 코드 작성·키 인증은 실행 단계다.

## 실행 결과 (2026-10-06)

직접 구현 완료. 커밋 단계는 사용자 요청이 없어 생략했다. 전체 79 tests, skill validation, 실제 HyperFrames/Chrome/FFmpeg 제작·재개·독립 revoice 통합 검사가 통과했다. 실제 .env는 루트에 0600으로 복사했고 Git 제외 및 키 로딩만 확인했다. 인증 요청은 하지 않았다.

계획 보완: 중첩 편집 소스의 수식을 같은 시점에 렌더하기 위해 lib/math_render.py를 추가했다. 전체 복습·독립 revoice의 고정 출력 계약을 위해 lib/single.py를 추가했다. revoice는 원본 scope와 예산을 새 요청에 연결하지 않으며 해당 영상만 교체하고 형제 영상과 latest 목록을 보존한다. 테스트 fixture는 임시 폴더에서 생성한다. 검증 증거는 로컬 ignored .superpowers/sdd/2026-10-06-ml-review-video/에 보존했다.
