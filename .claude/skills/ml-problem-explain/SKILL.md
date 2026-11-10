---
name: ml-problem-explain
description: 머신러닝기초의 기존 복습문제·과제·중간고사 예상문제의 문제설명 HTML과 MD를 만든다. 문제해설, 입문 풀이 설명, 과제 풀이 설명 또는 /ml-problem-explain [날짜|기간|과제번호|중간고사 N회|HTML경로]에 사용한다. 새 출제는 ml-midterm 등 별도 스킬이다.
---

# 머신러닝기초 문제풀이 입문 설명

논회실의 문제설명 기능을 이 과목의 기존 카드에 적용한다. 이론은 읽었지만 문제풀이 경험이 부족한 학생에게 **문제의 단서 → 떠올릴 개념·공식 → 첫 줄 → 단계별 이유 → 완성 답 → 검산**을 모두 보여 준다. 복습문제·과제·중간고사 예상문제를 지원한다.

**설명 깊이 필수 읽기**: 저작자·리뷰어·감사자에게 [문제풀이에 필요한 설명 깊이](../ml-review-pack/references/problem-solving-depth.md)와 적용 문항 브리프를 전달한다. 신규·기존 해설 수정·lite/backfill 모두 필요한 판단·조건·계산 연결을 갖추고 설명을 마친다. 일곱 구역·소문항별 solve/verify는 유지하며, 정성 문항에 쓰지 않는 공식이나 새 숫자 검산 문제로 구역을 채우지 않는다. 독립 검증 전체는 evidence에 두고 독자용 verify는 해당 답의 필요한 점검에 집중한다.

**미분 문항 필수 읽기**: 저작·검토 전에 [공통 벡터 미분 관례](../ml-review-pack/references/vector-derivative-convention.md)를 전체 읽는다. 기본은 열벡터 변수에 대한 스칼라 미분을 행벡터로 쓰고, 열 정규방정식으로 전환할 때 양변 전치를 명시하는 것이다. 기존 원문이 열 gradient를 명시하면 원문·조건을 보존하고 그 관례를 따르며 강의와의 차이를 설명한다. 문제 조건까지 통일하는 별도 사용자 요청이 있을 때에만 요청 범위에서 원천과 문제·PDF를 함께 수정한다. 해설 본문·sum·용어·MD·재생성 조각도 같은 관례로 검토한다.

## 대상과 보존

- `1007`: 해당 날짜 복습문제. `0909-0916`: 기간의 날짜별 팩을 각각 처리한다.
- `과제1` 또는 `hw1`: 저장된 과제1 카드.
- `중간고사 N회` 또는 예상문제 원본/문제설명 HTML: [ml-midterm 해설 전용 경로](../ml-midterm/references/explanation-rules.md#해설만-처리)를 사용한다. 같은 폴더의 유일한 원본과 blueprint를 전용 resolver로 확인한다. 일반 extract/load_source는 EXAM을 지원하지 않는다. base/english를 실행하거나 문제·PDF를 바꾸지 않는다. 새 출제는 [ml-midterm](../ml-midterm/SKILL.md)으로 보낸다.
- HTML 경로: 해당 파일을 명시한다.
- 실제 시험(채점된 시험지): 스캔을 전사해 `시험결과/중간고사/중간고사_<MMDD>_<slug>.html` 카드(`data-source="Midterm <MMDD> Q<n>"`)를 먼저 만들고, 그 HTML 경로를 `--target`으로 명시한다. 프로필 이름은 `midterm`이다(ml-midterm 예상문제 어댑터의 `exam`과 구별). 산출물은 과제처럼 카드 HTML 옆에 `중간고사_<MMDD>_문제설명_<slug>.html/.md`, `figures_문제설명_exam<MMDD>_<slug>/`, `자료_문제설명_exam<MMDD>_<slug>/`로 둔다. `all`·날짜 대상으로는 선택되지 않는다. 예: `시험결과/중간고사/.pack/`(transcript·scan crop·검산 스크립트).
- 인자 없음: 파일명 날짜 기준 최신 복습문제. 과제는 자동 선택하지 않는다.

여러 slug나 통합/개별 팩이 겹치면 후보 경로를 보여 주고 대상을 명시하게 한다. PDF만 있는 과제는 카드 HTML 준비가 먼저 필요하다. 새 문제, 정리노트, PDF, 영상, 자동 채점은 만들지 않는다. 기존 원 HTML·MD·PDF·그림을 수정하지 않는다. 카드의 풀이·정답은 참고 답안이며 독립 검산을 대신하지 않는다.

## 실행

저장소 루트에서 `python --version`으로 Python 3.10 이상을 확인한다. 실행기는 표준 라이브러리만 사용한다. 설치 작업 자체에서는 실제 수업 자료를 생성하지 않는다.

중간고사 대상은 위 EXAM 분기의 `midterm_cli.py explain → 실제 검토 → publish → check`로 처리한다. 다음 일반 절차는 날짜·기간·과제·인자 없음·all에 그대로 적용하며, 중간고사를 자동 선택하거나 all에 추가하지 않는다.

1. 새 고유 RUN을 `tmp/ml-problem-explain/<실행ID>` 아래 정하고 extract한다.

   ```powershell
   python .claude/skills/ml-problem-explain/scripts/mpe_cli.py extract --repo . --target 과제1 --run tmp/ml-problem-explain/hw1-first
   ```

2. 출력 대상 디렉터리의 `source.json`을 읽는다. 문항 ID·조건·질문·모든 subparts·그림·참고 풀이를 확인한다. MML·교안·과제 원 PDF·기존 정리노트의 관련 페이지를 실제로 읽는다. 원문과 그림은 PDF 페이지로 대조한다. 필요할 때만 STT를 보조로 쓴다.
3. [저작 규칙](references/authoring.md)을 읽고 각 `explanations/pN.html`을 작성한다. `understand → recall → start → solve → verify → pitfall → retry` 순서의 일곱 구역, 모든 소문항별 solve/verify 표지, 펼친 답과 우측 요약이 필요하다. 각 문항의 recall은 **이 문제를 봤을 때 떠올릴 개념과 공식**을 입문형으로 설명한다. 문제의 단서·개념의 뜻·공식과 기호·적용 조건·선택 이유를 연결하고 우측 요약에도 핵심 개념·공식을 짧게 넣는다. 설명은 에이전트가 저작한다. CLI만 실행하면 풀이가 자동 작성되지는 않는다.
4. 별도 계산·상징 계산·증명 검토로 답을 검증한다. 스크립트와 결과·근거 자료를 `evidence/`에 남긴다. 단순 구조 검사를 수학 검증으로 기록하지 않는다. 충돌·모호함은 disputed로 보고하고 해당 팩을 보류한다.
4b. 형제 스킬 [ml-note-audit](../ml-note-audit/SKILL.md)의 "생성 절차에서 부를 때"로 설명 감사를 한다(lite·backfill 포함). `<대상>`은 `explanations/*.html`, `<형제 자료>`는 같은 날짜의 정리노트·복습문제·인터렉티브다. 결과는 `<RUN>/audit.md`에 두고 Critical·Important는 build 전에 조각에서 고친다. 남은 항목은 보고의 미해결에 적는다.
   미분은 변수/결과 차원·곱 순서·0으로 놓기·양변 전치와 원문 관례 처리 근거를 남긴다. 행 관례로 저작한 설명 조각·HTML·MD에 `python .claude/skills/ml-review-pack/scripts/check_vector_derivatives.py <경로...>`도 실행한다. 보존할 다른 관례 원문은 분리하여 수동 대조하고 이유를 기록한다. 기계 검사는 수학 검산을 대체하지 않는다.
5. build와 check를 실행한다. build는 새 stage와 `review.json`을 만들며 모든 검토 상태를 not_run으로 초기화한다. 재build 시 기존 승인도 다시 검토한다.

   ```powershell
   python .claude/skills/ml-problem-explain/scripts/mpe_cli.py build --run tmp/ml-problem-explain/hw1-first
   python .claude/skills/ml-problem-explain/scripts/mpe_cli.py check --run tmp/ml-problem-explain/hw1-first
   ```

6. [검토 기록](references/verification.md)을 읽고 실제 내용·답·원문 대조 결과를 `review.json`에 기록한다. 읽은 저장소 자료의 path/hash를 references에 기록한다. 로컬 브라우저에서 1280×900/375×812, 두 테마, 목차·이전/다음·요약·수식·그림·링크를 확인한다. 콘솔·KaTeX 오류, 누락 자원, 문서 가로 넘침은 0이어야 한다. 자원은 동봉된 로컬 KaTeX/Pretendard를 쓰며 외부 요청이 없어야 한다. stage의 원 문제/개념 링크는 최종 발행 디렉터리 기준이므로 대상 원 파일의 실제 anchor도 별도로 확인한다.
7. 승인된 review.json과 현재 해시가 일치하면 발행한다. 추가 확인 요청 없이 사용자 호출 범위에서 실행한다. 입력·참조·산출 파일 변경, 미검토, 실패는 발행을 막는다. 파일 교체 실패는 백업으로 복구한다.

   ```powershell
   python .claude/skills/ml-problem-explain/scripts/mpe_cli.py publish --run tmp/ml-problem-explain/hw1-first
   ```

팩별로 독립 성공/실패를 보고한다. 완성 HTML·MD 링크와 백업 경로, 보류 이유를 알려 준다. 결과가 유용하면 HTML을 Codex 패널로 연다.

## 산출 위치

복습: HTML은 `복습노트/<날짜>/문제설명_<날짜>_<slug>.html`, 나머지는 날짜 폴더의 `.pack/` 아래에 둔다: `.pack/문제설명_<날짜>_<slug>.md`, 그림 `.pack/figures_문제설명_<날짜>_<slug>/`, 생성 기록·검토·조각·검산·로컬 자원 `.pack/자료_문제설명_<날짜>_<slug>/`.

과제: `과제/과제<N>/과제<N>_문제설명_<slug>.html/.md`, 그림 `figures_문제설명_hwN_<slug>/`, 자료 `자료_문제설명_hwN_<slug>/`(모두 HTML과 같은 폴더). 기존 정리노트에 링크를 자동 삽입하지 않는다. 읽음 상태는 원 노트와 다른 `ml-problem-explain-<profile>-<range>-<slug>` 범위로 저장한다.


## 공통 업데이트: 대상·화면·검토 기준

- `all`: 기존 복습팩만 끝 날짜 내림차순으로 처리한다. 과제·forecast는 자동 선택하지 않는다. 전자회로2는 `.assets/problems.txt`가 있는 팩만 선택한다. 여러 후보는 명시 경로(전자회로2는 날짜 범위)로 해소하고 새 문제를 출제하지 않는다.
- 화면: 1024px 이상은 목차와 문제 패널이 기본으로 함께 열린다. 저장된 닫힘 선택은 유지한다. 문제 패널은 `문제 | 원문` 탭, 왼쪽·오른쪽 붙이기·띄우기, 이동·크기 조절을 지원한다. 상태 키는 `od-panels:explain:v2:prob`다. 원문 없는 문항은 원문 탭을 숨기고, 모바일은 해설 위 `문제 보기`로 펼친다. 그림 확대와 인쇄 원문 보존도 검토한다.
- 객관식: 입력에 명시된 정답 모델의 보기 ID·순서·정답·mode가 실제 보기와 맞을 때만 클릭 판정·알림·다시 풀기를 제공한다. 모델 없음/불일치는 정적 표시하고 진단한다. 해설 문장이나 보기 위치로 정답 모델을 추측하지 않는다. 전자회로2 workbook 입력은 정적 표시한다.
- 현재 검토 기준은 `review_policy_version="problem-explain-2026-10-20-row-derivatives"`다. build의 review.json과 manifest에 기록하며, 이전 기준이나 기준 없는 기록은 새 발행을 승인하지 못한다. 기존 발행 HTML의 열람에는 영향을 주지 않는다.

### 레이아웃만 바뀐 기존 발행분 재발행

발행 자료 `.pack/자료_문제설명_<range>_<slug>/ (과제는 기존 HTML 옆 자료 폴더)`의 fragments·evidence를 새 RUN으로 복사하고 stage만 조립한다. CLI의 rerender는 자동 발행하지 않는다.

```sh
python3 ".claude/skills/ml-problem-explain/scripts/mpe_cli.py" rerender --repo "<저장소 절대경로>" --target 1007 --run "<비어 있는 새 RUN 절대경로>"
```

입력·설명 조각·입력 그림·검산 자료·참조 파일이 검증되고 검토 기준도 현재와 같을 때만 content·independent를 재사용한다. 전자회로2는 problems.txt뿐 아니라 문제 MD·그림 전체의 합성 해시가 같아야 한다. 참조 누락·내용 변경·기준 누락/변경이면 content·independent도 not_run으로 되돌리고 실제 검토를 다시 한다. 경로 이전은 실제 대상과 바이트/링크 동등성을 입증할 때만 허용하며, 입증하지 못하면 재검토한다. 원본 HTML의 스타일·실행 스크립트만 바뀐 경우는 과거 입력을 확인할 수 있을 때만 동일 문항으로 인정하고 JSON 정답 데이터는 내용으로 취급한다.

`check` 뒤 source_visual·browser를 실제로 다시 확인한다. 검토 기준이 바뀐 이번 업데이트의 옛 발행분은 내용 검토·독립 검산도 새로 필요하다. 네 검토가 모두 pass인 뒤에만 별도 publish 절차를 사용한다. 사용자가 stage까지만 요청했다면 publish를 실행하지 않는다. 새로 해설을 저작해야 하면 기존 정상 저작 절차로 돌아간다.

## 본문과 우측 패널 표시 계약

중앙 주제·문항 제목과 패널의 고정 제목은 유지한다. 우측에는 중앙 제목을 복사하지 않는다. `sum-for`는 제목이 아닌 유일한 `.sums` 컨테이너 ID로 보존한다. `.sum` 전환, 문제·원문 탭, 힌트·풀이, 앵커, read/solved 저장 키와 payload를 유지한다. 예습·과제·시험도 같은 표시 계약을 따른다.

요약은 같은 토픽 본문의 핵심 개념·작동 원리·성립 조건·혼동 구분을 압축한다. 식·용어·항목 수에 고정 상한을 두지 않는다. 본문에 없는 사실을 요약에만 추가하지 않으며 보충의 범위·출처·불확실성을 보존한다. 문제설명은 풀이의 판단 조건·결론·단서를 압축하고 문제 데이터와 풀이 본문을 바꾸지 않는다.

검토 시 자료·토픽별로 일반·강조·주의·보충의 서로 다른 핵심을 별도 행으로 기록하고 본문 주장, 대응 요약 문장, pass/unresolved와 생략 이유를 대조한다. 보완 후 실제 요약을 다시 읽는다. 기존 동반 MD와 재생성 원고도 동기화하되 원래 없는 MD 형식은 만들지 않는다. 요약·예고·링크 화면의 기존 구조를 유지한다. 검증 JSON은 `{schema_version:1, html, html_sha256, audit_path, audit_sha256, semantic_status, browser_status, evidence, unresolved}`를 기록한다. 실제 검사 뒤에만 status를 바꾸며 HTML·감사표 해시 변경 후에는 기록을 갱신해야 한다.
