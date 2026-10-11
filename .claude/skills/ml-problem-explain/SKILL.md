---
name: ml-problem-explain
description: 머신러닝기초의 기존 복습문제·과제 카드로 첫 줄부터 이유·완성 답·검산까지 펼친 문제설명 HTML과 MD를 만든다. 문제해설, 입문 풀이 설명, 복습문제 풀이 설명, 과제 풀이 설명 또는 /ml-problem-explain [날짜|기간|과제번호|HTML경로]에 사용한다. 새 출제·정리노트·PDF·영상 생성은 별도 스킬이다.
---

# 머신러닝기초 문제풀이 입문 설명

논회실의 문제설명 기능을 이 과목의 기존 카드에 적용한다. 이론은 읽었지만 문제풀이 경험이 부족한 학생에게 **문제의 단서 → 떠올릴 개념·공식 → 첫 줄 → 단계별 이유 → 완성 답 → 검산**을 모두 보여 준다. 복습문제와 과제를 지원한다.

## 대상과 보존

- `1007`: 해당 날짜 복습문제. `0909-0916`: 기간의 날짜별 팩을 각각 처리한다.
- `과제1` 또는 `hw1`: 저장된 과제1 카드.
- HTML 경로: 해당 파일을 명시한다.
- 인자 없음: 파일명 날짜 기준 최신 복습문제. 과제는 자동 선택하지 않는다.

여러 slug나 통합/개별 팩이 겹치면 후보 경로를 보여 주고 대상을 명시하게 한다. PDF만 있는 과제는 카드 HTML 준비가 먼저 필요하다. 새 문제, 정리노트, PDF, 영상, 자동 채점은 만들지 않는다. 기존 원 HTML·MD·PDF·그림을 수정하지 않는다. 카드의 풀이·정답은 참고 답안이며 독립 검산을 대신하지 않는다.

## 실행

저장소 루트에서 `python --version`으로 Python 3.10 이상을 확인한다. 실행기는 표준 라이브러리만 사용한다. 설치 작업 자체에서는 실제 수업 자료를 생성하지 않는다.

1. 새 고유 RUN을 `tmp/ml-problem-explain/<실행ID>` 아래 정하고 extract한다.

   ```powershell
   python .claude/skills/ml-problem-explain/scripts/mpe_cli.py extract --repo . --target 과제1 --run tmp/ml-problem-explain/hw1-first
   ```

2. 출력 대상 디렉터리의 `source.json`을 읽는다. 문항 ID·조건·질문·모든 subparts·그림·참고 풀이를 확인한다. MML·교안·과제 원 PDF·기존 정리노트의 관련 페이지를 실제로 읽는다. 원문과 그림은 PDF 페이지로 대조한다. 필요할 때만 STT를 보조로 쓴다.
3. [저작 규칙](references/authoring.md)을 읽고 각 `explanations/pN.html`을 작성한다. `understand → recall → start → solve → verify → pitfall → retry` 순서의 일곱 구역, 모든 소문항별 solve/verify 표지, 펼친 답과 우측 요약이 필요하다. 각 문항의 recall은 **이 문제를 봤을 때 떠올릴 개념과 공식**을 입문형으로 설명한다. 문제의 단서·개념의 뜻·공식과 기호·적용 조건·선택 이유를 연결하고 우측 요약에도 핵심 개념·공식을 짧게 넣는다. 설명은 에이전트가 저작한다. CLI만 실행하면 풀이가 자동 작성되지는 않는다.
4. 별도 계산·상징 계산·증명 검토로 답을 검증한다. 스크립트와 결과·근거 자료를 `evidence/`에 남긴다. 단순 구조 검사를 수학 검증으로 기록하지 않는다. 충돌·모호함은 disputed로 보고하고 해당 팩을 보류한다.
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

복습: `복습노트/<날짜>/문제설명_<날짜>_<slug>.html/.md`.

과제: `과제/과제<N>/과제<N>_문제설명_<slug>.html/.md`.

그림은 별도 `figures_문제설명_<날짜 또는 hwN>_<slug>/`, 생성 기록·검토·조각·검산·로컬 자원은 `자료_문제설명_<날짜 또는 hwN>_<slug>/`에 저장한다. 기존 정리노트에 링크를 자동 삽입하지 않는다. 읽음 상태는 원 노트와 다른 `ml-problem-explain-<profile>-<range>-<slug>` 범위로 저장한다.
