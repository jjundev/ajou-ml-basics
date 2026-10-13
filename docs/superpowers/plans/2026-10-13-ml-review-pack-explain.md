# ML Review Pack Explain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 복습팩 신규·갱신에 전체 문제설명을 연결하고 과거 9팩 63문항의 설명을 발행한다.

**Architecture:** 기본 팩의 기존 HTML/MD/PDF 배포 경계를 유지하고, 성공 직후 형제 ml-problem-explain 스킬 전체 절차를 명시 HTML 경로로 실행한다. 과거 팩은 기존 HTML을 입력으로 읽고 설명 소유 파일만 발행한다. 새 자동 저작기나 렌더러를 만들지 않는다.

**Tech Stack:** Python 3.10+ 표준 라이브러리 실행기, 기존 unittest/pytest, 기존 HTML/MD 렌더러, 로컬 KaTeX/Pretendard, 브라우저 검토 도구. 수학 검산에 필요한 라이브러리는 실행 환경에만 설치한다.

**Spec:** `docs/superpowers/specs/2026-10-13-ml-review-pack-explain-design.md` — 실행 전 전체를 읽는다.

## Global Constraints

- Python 3.10 이상, 설명 실행기는 표준 라이브러리만 사용한다.
- 설명 순서는 `understand → recall → start → solve → verify → pitfall → retry`이다.
- 문체는 `~해요` 체와 영어 전문용어 병기이다.
- `source_visual/content/independent/browser` 네 실제 검토는 lite에서도 생략하지 않는다.
- 브라우저 검토는 1280×900/375×812, light/dark에서 전체 문항을 확인한다.
- 콘솔·KaTeX 오류·누락 자원·외부 요청·문서 가로 넘침은 0이어야 한다.
- backfill은 원 복습문제·정리노트 HTML/MD·PDF·기존 그림·과제·은행·교재를 수정하지 않는다.
- 설명 소유 파일만 고유 백업 후 교체하며 교체 실패 시 복구한다.
- 실패 시 검증된 기본 팩과 이전 설명을 보존하고 “복습팩 생성됨 / 문제설명 보류”로 보고한다.
- 커밋·푸시는 별도 사용자 지시가 있을 때만 수행한다. 아래 커밋 단계는 사용자 승인된 경우에만 실행하고, 그 외에는 검토 가능한 diff를 남긴다.
- Spec의 나머지 전역 제약도 모든 Task에 적용한다. `.agents` 링크 실체인 `.claude`만 수정한다.

## Review Focus

1. 여러 slug·통합/개별 팩·NFC/NFD 경로: 전달받은 실제 HTML 하나만 처리하고 최신 날짜로 바꾸지 않는다. Task 1의 명시 경로 CLI 테스트.
2. 갱신 도중 입력/참조/조각 변경: 오래된 승인을 거부하고 원본과 이전 설명을 보존한다. Task 1의 stale-input 회귀 검사.
3. 일부 소문항 누락·증명/정성 문항: 전체 검토 집합을 확인하고 수치 예제를 증명 승인으로 쓰지 않는다. Task 2·3의 delivery 검사와 실제 수학 검토.
4. HTML 교체 후 MD/자산 저장 실패·미검토 lite: rollback하고 완료로 보고하지 않는다. Task 1의 미검토·교체 실패 회귀 검사.
5. 구형 카드·원 문제 anchor·모바일 긴 수식·summary 중복 표지: 현재 발행 경로에서 원문과 링크·문자·수식 표시를 검증한다. Task 2의 0909 구형 팩 및 Task 3의 전체 화면/labels 검사.

---

## 파일 구조

| 경로 | 역할 |
|---|---|
| `.claude/skills/ml-review-pack/SKILL.md` | 준비 확인, 8단계 연결, 산출물/lite/보고/실패 계약 |
| `.claude/skills/ml-review-pack/references/problem-explain.md` | 명시 경로로 설명 스킬 전체 실행하는 공통 지침 |
| `.claude/skills/ml-review-pack/tests/test_skill_files.py` | 공통 지침 연결과 참조 존재 검사 |
| `.claude/skills/ml-problem-explain/tests/test_cli.py` | 명시 경로·전체 문항·미검토 발행 거부 회귀 |
| `.claude/skills/ml-problem-explain/tests/test_source.py` | 실제 최신 날짜에 의존하는 테스트를 임시 fixture로 고립 |
| `.claude/skills/ml-problem-explain/tests/test_delivery.py` | 실제 설명 납품의 입력/문항/파일/검토 일치 검사 |
| `복습노트/<range>/문제설명_<range>_<slug>.html/.md` | 새 학습 설명 |
| `복습노트/<range>/figures_문제설명_<range>_<slug>/` | 설명 소유 그림 |
| `복습노트/<range>/자료_문제설명_<range>_<slug>/` | 조각·근거·검토·manifest·로컬 자원 |
| `docs/verify/2026-10-13-ml-review-pack-explain.md/.json` | inventory·보존·팩별 결과·RUN/백업·테스트 보고 |

실행용 임시 파일은 `tmp/ml-problem-explain/<고유ID>/`에 둔다. Git 범위에 tmp, venv, 캐시, .env를 넣지 않는다. SKILL.md 수정만으로 동작하는 연결이며 production Python 코드는 회귀 결함을 재현한 경우에만 범위를 보고하고 수정한다.

### Task 1: 미래 생성·갱신의 설명 연결 계약

**Files:** 위 표의 SKILL.md, 새 reference, test_skill_files.py, test_cli.py, test_source.py.

**Interfaces:**
- Consumes: `mpe_cli.main(argv=None) -> int`, `resolve_sources(repo: Path, target: str | None) -> tuple[Path, ...]`, 현행 PDF `publish_files` 배포 성공.
- Produces: 공통 절차 입력 `ABS_REPO`, `ABS_REVIEW`, `EXPLAIN_SKILL`, 팩별 빈 `EXPLAIN_RUN`(모두 절대 경로). 결과 published/withheld, 이유, HTML/MD/RUN/백업. CLI 인터페이스는 변경하지 않는다.

- [x] **Step 1: 테스트 기준선 실행**
  Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -v` 및 `python3 -m pytest .claude/skills/ml-problem-explain/tests -q`. 필요한 테스트 의존성은 별도 venv로 준비하고 실제 Python 경로를 보고한다. 실패를 기록한다. `test_latest_and_explicit_homework`의 1007 고정 기대값은 현재 최신 1012와 다르므로 환경 의존 기존 실패로 분리한다.
- [x] **Step 2: 실패 테스트 작성**
  `test_skill_files.py`에 `test_problem_explain_handoff`를 추가한다. 참조가 SKILL 본문에서 연결되고 존재해야 하며, 0단계의 의존성 확인과 8단계의 배포 뒤 설명 호출, 9단계의 발행/보류 보고가 있어야 한다. 새 지침은 명시 경로·전체 저작·네 검토·lite 포함·실패 정책을 담아야 한다. 현재 reference 부재로 FAIL을 확인한다.
- [x] **Step 3: 기존 경계의 실행 테스트 추가 및 고립**
  `test_cli_explicit_review_path_ignores_newer_and_other_slug`를 추가한다. 임시 repo에 실제 0909 원 HTML과 대응 workbook layout을 복사하고, 다른 slug와 최신 날짜 후보를 함께 둔다. 명시 경로 extract 결과의 source.json은 해당 원 경로/hash/전체 문항이어야 한다. 모든 조각 build/check 후 미검토 publish는 returncode 1, 원본 및 기존 설명 bytes 불변이어야 한다. 테스트용 조각/approved는 실제 발행 승인에 사용하지 않는다.
  `test_latest_and_explicit_homework`는 최신 선택 부분을 날짜 1007/1012의 임시 fixture로 옮기고 1012를 기대한다. 기존 과제·명시 경로 검사도 유지한다.
- [x] **Step 4: 연결 지침 구현**
  공통 reference에 extract → 저작 → 독립 검산 → build/check → 실제 review.json 기록 → publish를 명시한다. SKILL 0단계/8단계/9단계·산출물·lite·오류 처리에서 연결한다. 문제설명 실패는 기본 팩 rollback 사유가 아니며 이전 설명을 현재 입력 승인으로 보고하지 않는다. 사용자 요청으로 기존 팩을 갱신하는 경우도 같은 최종 설명 절차를 수행하고 별도 update-existing 기능은 추가하지 않는다.
- [x] **Step 5: 경계 회귀 확인**
  Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -v` 및 `python3 -m pytest .claude/skills/ml-problem-explain/tests -q`. PASS. 특히 `test_stale_inputs_or_failed_reviews_are_refused`, `test_no_review_keeps_existing_files`, `test_replace_failure_rolls_back_pair`, `test_one_stale_pack_does_not_block_other_pack`, 소문항·labels 검사 통과를 확인한다.
- [x] **Step 6: 검토 또는 승인된 커밋**
  diff와 whitespace 검사 후 Task 1 파일만 검토한다. 커밋이 승인되면 메시지 `feat(ml-review): generate verified problem explanations`을 사용한다.

### Task 2: inventory·보호 기준선과 대표 0909 실제 발행

**Files:** 새 test_delivery.py, docs/verify 보고서, 0909 설명 소유 파일.

**Interfaces:**
- Consumes: Task 1 공통 절차, `load_source(path: Path, repo: Path) -> SourcePack`, `check_artifacts(pack, artifacts) -> list[str]`, `Artifacts(html, md, manifest, files)`.
- Produces: 보고 JSON에 baseline(상대 path→SHA-256), inventory(path/hash/range/slug/problem_ids/subparts), packs(동일 identity + status/reason/run/backup/html/md). 실제 published 경로 기준으로 후속 Task가 검증한다.

- [x] **Step 1: 실행 목록·보호 기준선 저장**
  임시 RUN에 복습노트의 현재 원문 HTML/MD/PDF·기존 그림/제작자료, workbook layouts, STT/강의노트/교과서, 과제(과제1 설명 포함), from_the_past가 있으면 그 파일까지 baseline을 기록한다. Git 제외 캐시·.DS_Store·tmp·.env는 제외한다. spec 표와 현황을 대조해 차이가 있으면 기록한다. 실제로 읽은 자료·쪽·해시는 팩별 evidence에 별도 기록한다.
- [x] **Step 2: 실제 납품 회귀 검사 작성**
  `test_published_review_explanation`을 실제 복습문제 경로별 parameterize한다. `load_source`의 range/slug에서 설명 HTML/MD/자료 경로를 정한다. 파일 부재는 skip 대신 FAIL이다. 공개 manifest의 source/path/hash와 problems/subparts가 입력과 같아야 하며, `Artifacts`를 manifest files로 구성해 `check_artifacts` 결과는 `[]`이어야 한다. validation의 네 상태는 pass, content/independent items 키는 `{p.id + ':' + s}` 전체와 일치, references의 파일/hash가 현재와 일치해야 한다. 검토 내용의 수학적 타당성은 이 테스트가 승인하지 않는다.
- [x] **Step 3: 0909 납품 검사 FAIL 확인**
  Run: `python3 -m pytest .claude/skills/ml-problem-explain/tests/test_delivery.py -k 0909 -q`. 현재 설명 파일이 없어 FAIL이어야 한다.
- [x] **Step 4: 대표 팩 전체 저작·독립 검산**
  0909의 정확한 HTML 경로로 공통 절차를 수행한다. 기존 workbook layout 해시 검사를 유지한다. 현재 기준 5문항·7검토 단위이며 실제 source.json으로 전체 범위를 확인한다. 원자료·개념·조건과 기존 참고 답을 대조하고 검산 evidence를 준비한다. 저작 조각·검산 스크립트·출력을 설명 자료와 함께 보존한다.
- [x] **Step 5: 네 실제 검토 후 발행**
  build/check 후 현재 산출물에 대해 원자료/내용/독립/브라우저 검토를 수행하고 승인한다. 공개 위치에서 자원/anchor를 재확인한다. source/fragment 변경 시 이전 승인 재사용을 금지한다. validation.json을 manifest의 owned files에 임의 추가하지 않는다(발행기가 저장하는 검토 보고서다).
- [x] **Step 6: 대표 납품 PASS·보호 파일 확인**
  Step 3 명령이 PASS이고 baseline과 보호 파일 bytes가 일치해야 한다. RUN/백업/읽은 쪽/검산/화면 결과를 보고서에 기록한다. 충돌이 있으면 withheld로 기록하고 다른 팩은 독립 처리한다.
- [x] **Step 7: 검토 또는 승인된 커밋**
  Task 2 테스트·보고서·0909 소유 파일만 검토한다. 승인되면 `docs(ml-review): add verified 0909 problem explanations`으로 커밋한다.

### Task 3: 나머지 8팩 backfill 및 전체 검증

**Files:** 0914/0916/0921/0923/0928/0930/1007/1012 설명 소유 파일, Task 2 보고서 갱신.

**Interfaces:**
- Consumes: Task 1 공통 절차와 Task 2 inventory/baseline/packs·실제 납품 검사.
- Produces: inventory의 모든 팩 결과, 모든 현재 설명 산출물, 전체 보존·테스트·실화면 검증 보고.

- [x] **Step 1: 남은 실제 납품 검사 FAIL 확인**
  Run: `python3 -m pytest .claude/skills/ml-problem-explain/tests/test_delivery.py -q`. 미생성 팩은 FAIL, 발행된 0909는 PASS이어야 한다.
- [x] **Step 2: 팩별 원자료 대조·전체 저작**
  inventory의 남은 8개 명시 HTML 경로를 날짜 오름차순으로 처리한다. 각각 별도 EXPLAIN_RUN을 쓴다. 모든 pN/subpart를 일곱 구역·요약으로 작성하고, MML Example/변형의 원 자료 조건과 카드 조건을 구분한다. 증명·정성 답은 논증과 가정을 확인하고 numeric 예제만으로 proof 승인을 하지 않는다. 공분산 관련 문항은 현행 scalar-to-vector-covariance 참고를 적용하되 수업 근거를 대신하지 않는다.
- [x] **Step 3: 팩별 검산·조립·네 실제 검토·발행**
  Task 1 절차 그대로 수행한다. 네 화면 조건에서 모든 본문·요약·목차·pager·원문/개념 링크·행렬·긴 유도식을 확인한다. 조각에 중복 소문항 표지가 생기면 공통 labels 정상화와 저작 원인을 확인하고 재build/review한다. 한 팩 실패는 withheld로 기록하고 다른 팩을 계속한다.
- [x] **Step 4: 공개 위치 전체 납품·보존 확인**
  Task 2 baseline을 다시 대조해 보호 파일 변경 0을 확인한다. 검토 스크린샷·결과는 현재 발행 HTML 해시와 연결되어야 한다. report JSON의 각 published 행은 실제 path/문항/소문항/source hash와 일치하고 withheld는 이유와 RUN을 가진다. 현재 예상 9팩·63문항·96검토 단위를 확인하되 실행 inventory와 다른 경우 이유를 보고한다.
- [x] **Step 5: 전체 회귀 검사 실행**
  Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -v`, `python3 -m pytest .claude/skills/ml-problem-explain/tests -q`, `git diff --check`. 모두 PASS이어야 한다. 원문 복사 evidence의 공백 문제는 원문을 조용히 고치지 말고 해당 파일에만 적용되는 처리와 비용을 보고한다.
- [x] **Step 6: 최종 보고서·자기 검토**
  docs/verify에 팩별 결과, 전체 수량, 네 실제 검토, 보호 hash, 현재 공개 경로, RUN/백업, 테스트 결과와 미해결을 기록한다. 완료 조건·다섯 Review Focus를 다시 대조한다. 테스트용 approved()가 실자료 승인에 사용되지 않았는지 확인한다. 모든 실제 팩 통과 전에는 전체 완료라고 보고하지 않는다.
- [x] **Step 7: 검토 또는 승인된 커밋**
  변경 범위가 스킬/테스트/설명 소유 파일/계획/검증 문서뿐인지 확인한다. 승인되면 `docs(ml-review): add verified explanations for existing packs`로 커밋한다. push는 별도 요청 때만 수행한다.

## 계획 자기 검토

- [x] Spec의 자동 연결·전체 backfill·lite·보류·보존·전체 검토를 Task 1–3에 배치했다.
- [x] 기존 CLI/SourcePack/Artifacts 인터페이스만 사용하고 새 production API를 만들지 않았다.
- [x] Review Focus 다섯 항목을 기존 회귀·추가 경계 검사·실제 납품/화면 검토에 연결했다.
- [x] 설명 없음 실패→발행 후 통과와 실제 수학 검토를 구분했다.
- [x] 커밋/푸시 권한을 추정하지 않으며 계획 단계에서 구현·발행하지 않는다.

실행 완료: Native 방식. 2026-10-13 검증 보고서와 실행 ledger에 실제 결과·판단·최종 리뷰 수정 및 경미한 보류 사항을 기록했다. 커밋·푸시는 승인되지 않아 단계의 검토 경로를 수행했다.
