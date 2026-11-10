# Problem-Solving Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 생성·검토 스킬에 풀이 목적에 따른 설명량 기준을 적용하고 1102·1104 정리노트 HTML/MD의 불필요한 설명을 줄인다.

**Architecture:** 공통 설명량 기준을 레퍼런스 하나에 정의하고 기존 작성·선별·리뷰·감사 흐름에서 참조한다. 기존 구조 검사기와 표시 계약을 유지하면서 두 노트의 내용과 MD·요약을 함께 수정한다. 스킬 개선과 두 날짜 이관은 순차로 진행하며 자동 의미 검사기나 새 공개 스키마는 만들지 않는다.

**Tech Stack:** Markdown 스킬, 정적 HTML/CSS/JavaScript, Python 3 기존 검증기, unittest/pytest, 실제 브라우저.

**Spec:** `docs/superpowers/specs/2026-11-10-problem-solving-depth-design.md` — 채팅의 결정 #1은 1102·1104 정리노트로 기본 확정. 실행자는 두 문서를 먼저 읽는다.

## Global Constraints

- 기존 자료 수정은 1102·1104 정리노트 HTML과 각각의 `.pack` 동명 MD로 한정한다.
- 기존 복습문제·문제설명·인터렉티브·PDF의 내용은 수정하지 않는다.
- 향후 작성 기준은 신규 생성·기존 설명 수정·lite에 동일하게 적용한다.
- 글자 수나 모든 토픽에 동일한 구성은 강제하지 않는다.
- 기호·목적·조건 연결은 유지한다. 이전 설명 요청을 철회한 것으로 해석하지 않는다.
- 기존 토픽 ID·연결되는 앵커·위젯·읽음 상태를 유지한다.
- 기존 강의 순서·좌우 패널·테마·폰트 크기·문제 및 인터렉티브 링크를 유지한다.
- HTML과 기존 대응 MD 및 요약을 함께 갱신한다.
- 필요한 풀이 판단·필수 유도는 본문에 남긴다. 반복은 삭제하고 독립적인 가치가 있는 내용만 선택 보충으로 둔다.
- 학습자 발언·이해 반응을 독립 수행이나 숙달의 증거로 확대하지 않는다.
- 스키마·공개 HTML 속성·생성기 인터페이스·문제설명 일곱 구역 계약을 새로 만들거나 변경하지 않는다.
- 이번 계획 작성은 구현을 포함하지 않는다. 실행 중의 커밋·푸시는 별도 사용자 지시가 없는 한 제안만 한다.

## Review Focus

1. 내용 축약에서도 필요한 연결은 유지되어야 한다 — Task 3의 PᵀP/Gram–Schmidt 재현 검사, Task 4의 사영·잔차·상한 재현 검사.
2. 감사가 간결한 풀이에 새 예제·증명을 다시 요구하면 안 된다 — Task 2의 짧지만 충분한 풀이와 과잉 검산 대조 사례.
3. 미래 팩의 확장 문제를 강의 필수 근거로 되먹임하면 안 된다 — Task 1의 core/extension 선별 사례.
4. 선택 보충으로 옮긴 단계의 앵커·번호·요약이 잘못된 위치나 숨은 필수 설명을 가리키면 안 된다 — Task 4의 공동 최적성 직링크/요약/키보드 검사.
5. MD 동기화가 문제 MD·PDF·그림을 의도치 않게 바꾸면 안 된다 — Task 3·4의 범위 밖 해시 동등성과 MD 누락·잔존 검사.

---

## 파일 구조와 책임

실행 시 `REPO`는 실제 `git rev-parse --show-toplevel` 결과, `RUN`은 `tmp/problem-solving-depth/<고유 실행ID>`의 절대 경로다. 모든 명령은 저장소 루트를 기준으로 한다. `.agents/skills` 경유 복사본은 만들지 않고 심볼릭 링크의 정본인 `.claude/skills`만 수정한다.

| 작업 | 파일 | 책임 |
|---|---|---|
| 1 | Create `.claude/skills/ml-review-pack/references/problem-solving-depth.md` | 설명량의 공통 정본 |
| 1 | Create `.claude/skills/ml-review-pack/tests/fixtures/problem-solving-depth-cases.md` | 재현 가능한 저작·감사 행동 사례와 판정 기준 |
| 1 | Modify `.claude/skills/ml-review-pack/SKILL.md` | 생성·수정·lite로 기준 전달 |
| 1 | Modify `.claude/skills/ml-review-pack/references/{content-rules,manifest-guide,big-picture-first,learner-reasoning-patterns,staged-body,problem-selection}.md` | 강제 전개·레이어·비유·보존 충돌 제거와 범위 선별 |
| 2 | Modify `.claude/skills/ml-review-pack/references/review-prompt.md` | 설명 부족·과잉의 동시 리뷰 |
| 2 | Modify `.claude/skills/ml-note-audit/{SKILL.md,references/audit-brief.md}` | 기존 여섯 범주 유지 + 별도 설명량 검토 |
| 2 | Modify `.claude/skills/ml-problem-explain/{SKILL.md,references/authoring.md}` | 향후 해설의 반복·검산 증거 분리 |
| 3 | Modify `복습노트/1102/정리노트_1102_PCA.html` | 1102 내용 선별 |
| 3 | Modify `복습노트/1102/.pack/정리노트_1102_PCA.md` | 1102 MD 동기화 |
| 4 | Modify `복습노트/1104/정리노트_1104_PCA_Part2.html` | 1104 내용 선별 |
| 4 | Modify `복습노트/1104/.pack/정리노트_1104_PCA_Part2.md` | 1104 MD 동기화 |

확장자 목록은 위 표의 정확한 파일명으로 풀어 사용한다. 템플릿·검사기 런타임·문제설명 발행 버전은 이번 수정 대상이 아니다. 행동 사례·브라우저 결과·백업·해시는 RUN에 두고 공개 노트에는 넣지 않는다.

### Task 1: 생성 기준과 범위 선별 수정

**Files:** 위 파일 구조 표의 작업 1 파일 전부.

**Interfaces:**
- Consumes: Spec의 공통 제약·편집 판단, 기존 `RUN/learning-map.json` 저작 브리프, manifest의 기존 `layers`, `required_terms`, `supp`.
- Produces: 공통 기준 경로 `references/problem-solving-depth.md`; 생산용 기록의 다섯 열 `위치·원문 / 관련 풀이 판단 / 처리 / 남길 최소 연결 / 근거`; 행동 사례 C1–C5. 새 JSON 키·필수 HTML 속성은 없다.

- [ ] **Step 1: 실제 작업 상태와 실행 경계를 기록한다.**

Run: `git status --short`, `git branch --show-current`, `git rev-parse --show-toplevel`, `git rev-parse --git-dir`, `git rev-parse --git-common-dir`.
기존 변경은 보존한다. 실행 전에 using-git-worktrees의 환경 확인 절차를 따르며 기존 격리가 있으면 재사용한다. 새 실행 방식을 임의로 선택하거나 이 계획 작성 중 작업 트리를 만들지 않는다. RUN을 정하고 두 날짜 전체와 수정할 스킬 파일을 백업한다. 범위 밖 학습 파일은 HTML/MD/PDF/그림의 상대 경로와 SHA-256을 기록한다.

- [ ] **Step 2: 행동 회귀 사례 C1–C5를 작성하고 현재 지침의 결과를 기록한다.**

fixture에 아래 각 사례의 고정 입력·실행 지시·기대 판단을 적고, 동일 입력을 현재 지침으로 저작/검토해 `RUN/baseline.md`에 실제 출력을 보관한다. 구조 테스트나 키워드 검사를 이 행동 평가의 대용으로 쓰지 않는다. 기준에 어긋난 관찰이 없으면 실패라고 쓰지 않는다.

| ID | 고정 입력 | 판정 기준 |
|---|---|---|
| C1 | 1104 P2의 조건·그림·질문과 현재 해설. 그림의 분리/퍼짐 해설을 작성하라 | 색·분리·퍼짐의 근거로 답한다. 답에 쓰지 않는 784차원·Bᵀx 유도를 새로 가르치지 않는다 |
| C2 | 1102 P10의 일반 증명과 현재 3×2 숫자 예 검산. 필요한 풀이만 편집하라 | 일반 증명과 λ≠0 근거는 보존하고 추가 숫자 문제의 양방향 계산은 삭제/선택 권고한다 |
| C3 | 1102 Gram–Schmidt 본문 중 목적·사영·고유공간 보존 연결과 실제 계산 | 계수를 왜 골라 빼는지, 같은 고유공간 안에서 성질이 유지되는 이유를 보존한다. 공식만 남기지 않는다 |
| C4 | 1104 공동 최적성 531–553줄, 앞의 순차 선택 결과 및 같은 날짜 문제 목록 | 새 C,q,w 증명은 선택 보충, 상위 M축·보존 분산 결론은 본문. 1축 상한 논리를 통째로 삭제하지 않는다 |
| C5 | STT 1104 558–560·598줄, 교안 해당 쪽, P4/P7/P8/P10의 요구 | 수계산 SVD·별도 정리 증명을 교과서 확장으로 판단한다. 문제에 실렸다는 사실만으로 강의 필수로 승격하거나 시험 제외를 단정하지 않는다 |

C1은 공개 해설·문제에 쓰지 않는 평가용 출력이다. 원본 학습 파일은 이 단계에서 고치지 않는다.

- [ ] **Step 3: 공통 기준과 생성 지침을 함께 수정한다.**

Spec의 ‘스킬 수정’을 작업 1 파일에 반영한다. 특히 content-rules의 모든 비유·강조 포함 의무, manifest-guide의 prof·비유 단어 의무, staged-body의 내용 삭제·선택 보충 금지를 그대로 남긴 채 새 규칙만 덧붙이지 않는다. 레이아웃 전용 변경의 보존 규칙과 사용자 요청에 따른 내용 편집의 규칙을 명시적으로 구분한다.

큰 그림은 다섯 data-map 역할을 짧게 유지한다. 일반 합 전개와 최소 예제의 충분성을 내용으로 판단하고 고정 문장 수·수식 수·비율 목표를 만들지 않는다. 문제 수·명세표 부족은 근거와 미충족 사항을 보고하도록 하며 새 문제를 만들어 승인 조건을 회피하지 않는다. 과거 학습자 요청 사실을 삭제·수정하거나 전역 메모리를 갱신하지 않는다.

- [ ] **Step 4: 생성 기준의 행동과 기존 파일 계약을 확인한다.**

C1·C3·C5를 같은 입력과 같은 실행 방식으로 재실행해 `RUN/behavior-after.md`에 baseline과 대조한다. 실패는 실제 출력의 위치와 최소 보완으로 수정한다.

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p 'test_skill_files.py' -v`

Expected: exit 0, `OK`. 새 레퍼런스가 SKILL.md에서 실제 사용되고 참조 파일이 존재해야 한다. 이 테스트의 성공만으로 저작 품질을 통과시키지 않는다.

- [ ] **Step 5: 작업 1을 독립 검토 가능한 변경 단위로 정리한다.**

`git diff --check` 및 `git diff --stat`을 확인한다. 사례별 관찰 결과와 정책 충돌 제거 위치를 RUN에 남긴다. 커밋은 사용자 지시가 있으면 `docs(skills): bound review explanations by problem-solving needs` 단위로 제안한다.

### Task 2: 리뷰·감사·향후 문제설명에 기준 연결

**Files:** 위 파일 구조 표의 작업 2 파일 전부.

**Interfaces:**
- Consumes: Task 1의 공통 기준·다섯 열 기록·C1–C5 fixture.
- Produces: `RUN/audit.md`의 기존 Critical/Important/Minor·연결 검토 근거 뒤에 `설명량 검토` 표. 기존 여섯 결함 범주·문제설명 일곱 구역·소문항별 solve/verify는 유지한다.

- [ ] **Step 1: 기존 감사의 C2·C3·C4 판정을 기록한다.**

Task 1의 고정 입력을 사용한다. C3처럼 짧지만 충분한 연결과 실제로 빠진 연결의 차이를 사례 원문에서 구분해 `RUN/audit-before.md`에 적는다. 과잉 항목을 수학 오류로 잘못 분류하지 않는다.

- [ ] **Step 2: 리뷰·감사 지침과 해설 저작 지침을 수정한다.**

별도 설명량 표는 원문·풀이 필요성·처리·남길 연결을 요구한다. 기존 ‘찾을 범주(이것만)’은 수학·설명 결함 여섯 범주에 대한 제한임을 명확히 하고, 새 편집 검토를 차단하지 않게 한다. 생성·수정·lite 경로에 전달한다. 일반 리뷰의 ‘누락’은 모든 인용의 존재가 아니라 핵심 결과·조건·필요한 연결을 대상으로 한다.

향후 문제설명은 일곱 구역을 유지하되 빈 구역·상투 문장으로 채우지 않는다. 단순 정성 문제는 판단 기준과 그림 근거를 사용한다. `verify`는 해당 답의 조건 대입·짧은 논리 점검으로 충분할 수 있으며, 별도의 숫자 문제·역행렬·오답 행렬을 강제로 추가하지 않는다. 독립 검산은 evidence에 남긴다. 본문 details 금지와 기존 소문항 계약은 변경하지 않는다.

- [ ] **Step 3: 행동 사례와 구조 계약을 검증한다.**

C2·C3·C4를 재감사하고 C1의 간결한 해설을 작성해 기록한다. 짧지만 충분한 연결에 추가 장문 설명을 요구하지 않고, 필요한 설명을 빠뜨린 경우에는 보완해야 한다.

Run: `python3 -m unittest discover -s .claude/skills/ml-note-audit/tests -p 'test_audit_brief.py' -v`

Run: `python3 -m pytest .claude/skills/ml-problem-explain/tests/test_contract.py -q`

Expected: 양쪽 exit 0. 여섯 범주·감사 호출·일곱 구역·소문항 계약이 유지된다. pytest가 없으면 기존 프로젝트 Python 환경을 확인하며 환경 변경/새 설치를 목적으로 범위를 넓히지 않는다. 실제 불가 원인은 보고한다.

- [ ] **Step 4: 작성→검토 전달을 점검한다.**

SKILL의 참조 경로와 실제 저작·감사 브리프를 대조한다. 향후 해설만 공통 기준을 참조하고 기존 공개 문제설명은 변경되지 않았는지 해시를 확인한다. `git diff --check` 후 `docs(skills): review excessive explanations alongside missing links` 변경 단위로 정리한다.

### Task 3: 1102 정리노트 선별 편집과 검증

**Files:**
- Modify `복습노트/1102/정리노트_1102_PCA.html` — 큰 그림 373–390, EVD 826–859, 푸리에 1045 인근, 방향 분산 1380–1410, 보충 증명 1526–1586을 실제 ID로 재확인한다.
- Modify `복습노트/1102/.pack/정리노트_1102_PCA.md`.

**Interfaces:**
- Consumes: Task 1–2 기준, Spec의 1102 편집 목록, 수정 전 백업·보존 계약·범위 밖 해시.
- Produces: 검증된 1102 HTML/MD 쌍, `RUN/1102-edit-map.md`, `RUN/1102-audit.md`, 실제 브라우저 증거.

- [ ] **Step 1: 백업에서 보존 계약과 편집 지도를 만든다.**

대상 HTML 전체와 대응 MD, 연결된 문제 요구를 읽는다. 모든 기존 ID, href, 위젯 ID, script/style 및 저장 키를 기록한다. 토픽별 삭제/축약/보충/유지와 남길 최소 연결을 명시한다. PᵀP 각 칸의 의미·열별 AP=PD·Gram–Schmidt의 사영 및 성질 보존을 보존 사례로 먼저 기록한다.

- [ ] **Step 2: stage의 1102 HTML을 편집한다.**

Spec 1102 목록대로 수정한다. 불필요한 수식을 남겨 두고 주변 문장만 줄이지 않는다. 없어진 소제목 ID는 필요한 경우 짧은 결론·해당 보충의 실제 의미 있는 요소에 유지한다. 한 원리에 여러 경로가 있으면 주 경로와 필요한 작은 예를 선별한다. 선택 보충 표시만 붙이고 모든 내용을 필독 단계에 그대로 두지 않는다. 필수 수학 조건을 보충으로 숨기지 않는다. CSS·JS·위젯 코드는 변경하지 않는다.

- [ ] **Step 3: 1102 MD와 요약을 동기화한다.**

기존 MD를 직접 편집하고 변경한 본문·식·조건·보충 구분·링크를 맞춘다. 원래 남아 있던 풀이에 필요한 그림은 보존한다. `html2md.py` CLI를 공개 폴더에 실행하지 않는다: 기본 함수가 두 MD와 SVG를 재생성·정리하기 때문이다. 기존 요약을 수정된 본문에 맞추고 삭제한 내용이 MD·요약에 남지 않았는지 읽는다.

- [ ] **Step 4: 기존 검사와 풀이 재현을 수행한다.**

Run: `python3 .claude/skills/ml-review-pack/scripts/check_learning_map.py 복습노트/1102/정리노트_1102_PCA.html`

Run: `python3 .claude/skills/ml-review-pack/scripts/check_html.py 복습노트/1102/정리노트_1102_PCA.html`

위 명령은 stage에서도 같은 최종 상대 구조를 갖춘 대상에 적용한다. Expected: exit 0, `OK`.

기존 API `html2md.check_md(html_path, md_path) -> list[str]`를 호출해 반환값 `[]`를 확인한다. import 경로는 `.claude/skills/ml-review-pack/scripts`다. 이 API는 읽기 전용이다. 삭제한 설명·수식이 MD에 남는 경우는 이 검사가 놓칠 수 있으므로 edit-map의 삭제 항목도 직접 대조한다.

대표 재현: (a) 정규직교 열로 PᵀP의 대각 1·비대각 0을 설명한다. (b) 같은 고유공간의 두 벡터에서 사영 계수를 구해 빼고 어떤 성질이 보존되는지 설명한다. (c) 중심화·사영좌표에서 V=bᵀSb를 복원한다. 실제 본문 외에 필요했던 연결이 있으면 다시 보완한다. 사용자의 숙달을 주장하지 않는다.

- [ ] **Step 5: 실제 화면을 검증한다.**

375px와 1280px 이상 데스크톱, 라이트·다크에서 큰 그림·EVD·분산 유도·보충을 확인한다. 목차/단계 직링크/이전·다음/요약/위젯/읽음 상태를 조작한다. 수식 오류·누락 자원·문서 전체 가로 넘침은 없어야 한다. 토픽 ID·href·script/style·위젯 보존을 백업과 대조한다. 증거와 실패/보완을 RUN에 남긴다.

- [ ] **Step 6: 검증된 쌍만 반영한다.**

실패가 남으면 기존 공개 쌍을 유지한다. 통과하면 HTML/MD만 반영하고 범위 밖 해시 동등성을 확인한다. `git diff --check`를 수행하고 `docs(notes): trim redundant explanations in 1102 PCA` 변경 단위로 정리한다.

### Task 4: 1104 정리노트 선별 편집과 최종 검증

**Files:**
- Modify `복습노트/1104/정리노트_1104_PCA_Part2.html` — 공동 최적성 531–553, 헤시안 618, 버린 방향 분산 691–694, SVD 819–845 인근을 실제 ID로 재확인한다.
- Modify `복습노트/1104/.pack/정리노트_1104_PCA_Part2.md`.

**Interfaces:**
- Consumes: Task 1–2 기준, 검증된 Task 3의 1102 링크/연결, Spec의 1104 편집 목록, 초기 백업·해시.
- Produces: 검증된 1104 HTML/MD 쌍, `RUN/1104-edit-map.md`, `RUN/1104-audit.md`, `RUN/result.md`.

- [ ] **Step 1: 1104 편집·보존 지도를 만든다.**

전체 HTML/MD·핵심 강의 범위·문제 요구를 읽고 Spec 목록을 대응시킨다. 고유기저 전개→교차항 소거→가중합→상한·도달, 정규방정식→정규직교 좌표, BᵀB와 BBᵀ의 구별·잔차를 보존 사례로 기록한다. 공동 최적성의 C/q/w 증명이 별도 선택 학습임을 구분한다.

- [ ] **Step 2: 1104 HTML을 편집한다.**

공동 최적성은 짧은 결론과 기본 닫힘의 native details 보충으로 옮긴다. 기존 `s0-directions-joint` ID는 결론/보충 안내의 보이는 요소에 유지해 직링크가 의미 있는 위치를 가리키게 한다. 필수 단계 수·이동 링크는 앞의 두 단계로 맞추고 보충으로 가는 안내를 별도로 둔다. 모든 보충을 강제로 접는 전역 UI 변경은 하지 않는다.

헤시안 유일성 증명은 삭제하고 정규방정식·좌표식의 조건은 유지한다. 버린 축의 분산식은 이미 얻은 식에 j를 대응시켜 연결한다. SVD 성분 선택은 필요한 의미·크기로 축약하고 외적 한 층·버린 특잇값 제곱합은 남긴다. 안테나·압축센싱·연구 조언과 풀이에 쓰이지 않는 확장 모델 이름은 덜어낸다. 위젯·CSS·JS는 보존한다.

- [ ] **Step 3: 1104 MD와 요약을 동기화한다.**

Task 3과 같은 읽기 전용 MD 검사 방식을 사용한다. 공동 최적성의 선택 보충 여부를 MD에도 반영하고 우측 요약은 본문의 핵심 결론과 성립 조건을 압축한다. 보충의 C/q/w를 새 필수 공식처럼 요약에 남기지 않는다.

- [ ] **Step 4: 기존 검사와 대표 풀이를 재현한다.**

Run: `python3 .claude/skills/ml-review-pack/scripts/check_learning_map.py 복습노트/1104/정리노트_1104_PCA_Part2.html`

Run: `python3 .claude/skills/ml-review-pack/scripts/check_html.py 복습노트/1104/정리노트_1104_PCA_Part2.html`

`html2md.check_md`는 Task 3과 같은 API·기대값을 사용한다. 대표 재현은 (a) 상위 M개 고유방향·보존/손실 분산, (b) Bᵀx와 BBᵀx 계산·잔차 수직성, (c) 특잇값 층의 합과 버린 제곱오차이다. 공동 최적성 보충을 열지 않고 이 풀이가 가능해야 한다.

- [ ] **Step 5: 실제 보충·단계·연결 화면을 확인하고 반영한다.**

375px/데스크톱×라이트/다크에서 `#s0-directions-joint` 직링크, 두 필수 단계 번호·현재 위치 표시, 보충 키보드 열기/닫기, 요약 전환, 이전/다음, 읽음 상태, 1102 연결을 확인한다. 필요한 결과가 닫힌 보충 안에만 있으면 실패다. Task 3과 같은 구조·자원 검사 뒤 통과한 HTML/MD 쌍만 반영한다.

- [ ] **Step 6: 변경 범위와 관련 회귀 검사를 마감한다.**

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p 'test_learning_map.py' -v`

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p 'test_html2md.py' -v`

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p 'test_check_html.py' -v`

Run: `python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p 'test_manifest.py' -v`

Expected: 각 명령 exit 0, `OK`. 자동 검사에 실패하면 원인을 파악하고 수정 범위와의 관련성을 기록한다. 무관한 문제를 고치려고 전체 PDF·영상·다른 날짜를 재생성하지 않는다. Task 1–2의 검사를 해당 작업 완료 후 이미 통과했다면 변경이 없는 한 반복하지 않는다.

최초 범위 밖 해시와 현재 값을 대조하고 `git diff --check`, `git status --short`, `git diff --stat`을 확인한다. `RUN/result.md`에 스킬 변경·두 날짜별 삭제/축약/보충·남긴 연결·실제 검사·브라우저 증거·백업·미해결을 기록한다. 수정 전후 본문 분량은 참고 수치로만 제시한다. `docs(notes): trim redundant explanations in 1104 PCA` 변경 단위로 정리한다.

## 자체 검토와 실행 인계

- Spec 적용: 공통 기준·충돌 규칙→Task 1, 리뷰·해설 전달→Task 2, 날짜별 수정→Task 3–4, 각 날짜 검증·범위 보존→Task 3–4에 대응한다.
- 인터페이스: 새 프로그램 API는 없다. 기존 `layers/required_terms/supp`, 다섯 `data-map` 역할, 여섯 감사 범주, 일곱 해설 구역을 유지한다.
- 테스트 비례: 저위험 문장 수정에 텍스트 일치 단위 테스트를 추가하지 않는다. 기존 구조 검사 + 실제 저작/감사 사례 + 대표 풀이 재현 + 실제 화면을 사용한다.
- 실행 방식 권장: **Native**. 네 작업이 같은 공통 기준을 공유하고 두 노트의 연결을 순차로 확인하므로 메인이 맥락을 유지해 실행하기 적합하다. 사용자가 방식을 선택한 뒤 해당 실행 스킬을 적용한다.
- 이 계획 작성 턴에는 구현·커밋·푸시를 하지 않는다. 승인된 실행 방식과 계획 확인을 받은 뒤 시작한다.
