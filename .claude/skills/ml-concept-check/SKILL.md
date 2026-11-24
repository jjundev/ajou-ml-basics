---
name: ml-concept-check
description: 머신러닝기초에서 특정 수업의 새 개념을 확인하는 즉시 채점 HTML 확인문제를 만들 때 사용한다. 단독 호출은 /ml-concept-check <MMDD|MMDD-MMDD>. ml-review-pack은 신규 팩을 발행한 뒤 호출한다.
---

# 머신러닝기초 확인문제

복습팩 하나를 바탕으로 5~10분짜리 확인문제를 만든다. 수업 흐름에 따라 처음 배운 개념을 골라 4지선다와 짧은 값 입력으로 확인한다. 자구알과 같은 HTML 템플릿과 상호작용 자산을 쓴다. 수업 근거와 정리노트 토픽이 확인된 문항을 발행한다.

- `S`는 이 스킬의 절대 경로다. `RUN`은 저장소 밖에 만드는 **이번 확인문제 전용 폴더**다. 명령의 `$S`, `$RUN`, `$SRC`, `<range>`는 실제 값으로 바꾼다.
- 공개 HTML은 `복습노트/<range>/확인문제_<range>_<slug>.html`에 둔다. `objectives.json`, `items.json`, `blind-ledger.json`, `browser.json`은 같은 날짜의 `.pack/자료_확인문제_<range>_<slug>/`에 둔다. RUN에 블라인드 사본, 답안표, 검산, 스크린샷과 발행 백업을 남긴다.
- 기본적으로 힌트가 펼쳐져 있다. 제출하면 즉시 채점되고 풀이의 토픽 링크가 같은 창에서 열린다. 같은 탭에서 풀이 링크를 따라갔다가 브라우저 뒤로 가기로 돌아오면 제출 답안·채점·푼 문제 표시를 복원한다. 마지막 문항을 제출하면 복기창이 나타난다. 새로고침 시 풀이 상태가 초기화된다.

## 1. 범위와 문항 작성

```bash
python3 "$S/scripts/quiz.py" prepare <range> --run "$RUN"
```

- 신규 팩에서 호출할 때는 `--manifest <복습팩 RUN>/manifest.json`을 덧붙이고 복습팩 요약도 함께 읽는다. 단독 호출에서는 날짜 폴더에 보존된 manifest를 자동으로 찾으며, 없는 날짜는 STT와 정리노트의 HTML·MD로 범위를 잡는다. `scope.json`의 `src` 경로를 `SRC`로 사용한다.
- [문항 규칙](references/item-rules.md)을 읽는다. 현재 팩의 STT·정리노트 MD·복습문제를 대조한다. 실제 수업 토픽별로 목표를 고르고 `SRC/objectives.json`과 `SRC/items.json`을 작성한다. 작성은 메인이 하거나 작성자 한 명에게 맡긴다. 목표 6개 미만이면 분량을 억지로 늘리지 않고 이유를 보고한다.
- 단답 정답과 풀이의 중간 계산은 정확한 유리수로 검산한다. ML 복습팩의 [벡터 미분 관례](../ml-review-pack/references/vector-derivative-convention.md)는 미분이 등장하는 문항·힌트·해설에 적용한다.

```bash
python3 "$S/scripts/quiz.py" check --run "$RUN"
```

## 2. 독립 블라인드 풀이

```bash
python3 "$S/scripts/blind.py" make "$SRC" "$RUN/blind-r1.md"
python3 "$S/scripts/blind.py" record "$SRC" "$RUN/blind-answers-r1.md" "$SRC/blind-ledger.json" --round 1
python3 "$S/scripts/blind.py" status "$SRC" "$SRC/blind-ledger.json"
```

- `make` 후 [풀이자 브리프](references/blind-brief.md)에 따라 정답을 모르는 **새 서브에이전트**에게 사본과 정리노트 MD를 넘긴다. 대화 상속을 끄고 정답·힌트·원본 경로는 전달하지 않는다. 답안표를 받은 뒤 `record`와 `status`를 실행한다.
- 답 불일치 또는 이의가 있으면 근거를 확인해 문항을 고치고 규칙 검사를 다시 한다. `status`에 남은 문항을 모두 `make ... --only q2,q5`처럼 지정해 새 풀이자에게 다시 맡긴다. 독립 풀이가 해결되지 않으면 발행을 보류하고 해당 문항과 이유를 보고한다.

## 3. 오프라인 검증과 발행

```bash
python3 "$S/scripts/quiz.py" verify --run "$RUN" --shots "$RUN/shots"
```

- `verify`는 규칙과 블라인드 결과를 확인하고 RUN에서 HTML을 빌드한다. Playwright Chromium에서 1280×900·375×812 × 라이트·다크 네 가지를 오프라인으로 조작한다. 힌트, 오답과 재시도, 단답 채점, 정리노트 링크를 따라갔다가 뒤로 가기 뒤 풀이 복원, 복기창, 새로고침 뒤 초기화, 글꼴·KaTeX·가로 넘침을 검사한다. 스크린샷을 열어 가독성과 겹침을 확인한 뒤 아래 명령으로 발행한다.

```bash
python3 "$S/scripts/quiz.py" publish --run "$RUN"
```
- 목표·문항·장부·HTML을 바꾸면 `verify`를 다시 실행한다. 근거 노트나 STT가 바뀌면 새 RUN에서 시작한다. 규칙, 블라인드 또는 브라우저 검증이 실패하면 RUN 경로와 실패 항목을 남기고 발행을 보류한다.
- 발행 경로, 문항 수와 형식, 블라인드 풀이 결과, 브라우저 통과 여부, RUN과 백업 위치를 보고한다. 기존 파일을 갱신할 때도 같은 절차를 거친다.
