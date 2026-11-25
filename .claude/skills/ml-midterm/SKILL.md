---
name: ml-midterm
description: 머신러닝기초 중간고사 예상문제·모의고사의 새 회차 제작이나 지정 회차 수정을 요청할 때 사용한다. /ml-midterm [N회], 중간고사 대비 10문항 출제에 사용한다. 기존 예상문제의 해설만 요청하면 ml-problem-explain의 중간고사 분기를 사용한다.
---

# 중간고사 예상문제 제작

완성된 `중간고사대비/예상문제_1회/`의 **현재** 문제 HTML·한국어 문제/답안 PDF·영어 문제 PDF·문제설명 HTML/MD를 기준으로 다음 회차를 만든다. CLI는 저작 도구이며 문제나 해설을 자동 작성하지 않는다.

| 요청 | 처리 |
|---|---|
| `/ml-midterm 2회` | 새 2회. 기존 폴더가 있으면 덮어쓰지 않는다. |
| 회차 생략 | 존재하는 회차 폴더의 최댓값+1. 삭제된 과거 회차 복원으로 대체하지 않는다. |
| 지정 회차 수정 | 사용자가 지정한 범위만 백업 후 교체한다. |
| 해설만·`/ml-problem-explain 중간고사 N회`·예상문제 HTML | [해설 전용 경로](references/explanation-rules.md#해설만-처리)를 따른다. base/english를 실행하지 않는다. |

## 제작

1. [출제 규칙](references/exam-rules.md)과 [해설 규칙·검토/발행](references/explanation-rules.md)을 읽는다. 이들이 연결하는 MPE 저작·검증·벡터 미분 reference도 필수다. 기준 1회의 `.pack/cards/`, `.pack/explanations/`와 실제 출처를 확인한다. 오래된 `questions.json`, `solutions.json`, `panel-content.json`으로 최신 조각을 재생성하지 않는다.
2. `uv run python --version`과 로컬 Chrome을 확인한다. Python 의존성은 `uv sync`로 설치한다. 저장소 루트에서 고유 RUN으로 시작한다.

   ```powershell
   uv run python .claude/skills/ml-midterm/scripts/midterm_cli.py init --repo . --round 2 --run tmp/ml-midterm/round02-first
   ```

   회차 생략은 `--round`를 뺀다. 반환된 `out`이 OUT이다. init은 RUN 메타데이터만 만든다. 명시한 회차가 이미 있으면 충돌을 알리고 기존 파일을 보존한다. 번호를 임의로 바꾸지 않으며, 다른 회차 선택이나 기존 회차 수정은 사용자가 명시한 범위를 따른다.
3. OUT의 `.pack/blueprint.json`, `cards/p1.html`~`p10.html`, `explanations/p1.html`~`p10.html`을 저작한다. 시작~1019 직교투영, 10대문항, 과제 변형 5+모델 분석 5를 지킨다. 소문항 수와 PDF 페이지 수는 고정하지 않는다. 영어 본문과 한국어 조건/질문의 요구가 같아야 한다. 원자료·1회차를 수정하지 않는다.
4. 답과 가정을 별도 계산으로 확인하고, 답·해설을 보지 않은 별도 검산자가 먼저 검산한다. 실제 근거를 `.pack/evidence/`에 남긴다. 출처 미확인·수학 충돌은 보류한다. 구조 검사 결과로 수학 pass를 만들지 않는다.
5. 같은 `--repo . --out <OUT> --run <RUN>`으로 `base`, `english`, `explain`을 순서대로 실행한다. base는 한영 HTML과 영어 original만 비운 한국어 PDF 입력 snapshot을 보존한다. 영어 PDF와 상세 해설은 stage에 생성된다. 공통 HTML/CSS/script/PDF 템플릿을 바꾸지 않는다. [baseline.json](references/baseline.json) 변경 진단은 기준을 자동 갱신해 우회하지 말고 변경 이유와 영향을 확인한다.
6. [검토·발행 절차](references/explanation-rules.md#검토와-발행)를 수행한다. 새 review의 네 상태는 not_run이다. 실제 원문·내용·독립 검산·브라우저 검토 후 해설을 `publish`하고, 검수한 영어 PDF를 별도로 발행한다. 전체 산출물에 `check`가 pass일 때만 완료로 보고한다.

산출물은 OUT의 원본 HTML, 한국어 문제/답안 PDF, 영어 문제 PDF, 문제설명 HTML과 `.pack/`의 MD·자원·조각·근거다. 최종 HTML/PDF 링크, 실제 검증 결과, 백업 위치나 보류 이유를 전달한다. 실패 후 `base_ready`나 `explanation_published`를 전체 완료로 해석하지 않는다. 중간 단계 실패는 RUN의 failure.json·백업으로 진단하며 파일 교체는 복구 가능하지만 전체 회차를 한 번에 원자적으로 교체하지는 않는다.
