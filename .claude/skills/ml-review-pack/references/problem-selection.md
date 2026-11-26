# 문제 선별 규칙 (MML 전용)

## 원칙
- 문제는 **MML 교과서에서만** 가져온다. 자작 문제는 아래 "자작 문제" 절의 경우에만 허용한다. 숫자만 바꾼 변형은 본문 예제(`variant: true`)에 한해 허용한다(카드에 출처·변형 배지는 달지 않는다).
- 출처가 `Example N.M`이면 그 Example의 **회색 상자 안** 내용만 쓴다. PDF 쪽을 열어 상자가 어디서 끝나는지 확인한다. 상자 밖 본문 설명·식(예: Example 8.8 뒤의 동전 실험)은 문제 출처가 아니다.
- "변형"은 숫자·데이터 값만 바꾼다. 구조(그래프 모양과 노드 수, 변수 수, 식의 꼴, 예제를 문제로 바꾸는 것 이상의 질문)를 바꾸면 자작 문제다. 예외는 아래 "덧붙이는 요구"뿐이다.
- 수업에서 배운 내용만으로 풀 수 있어야 한다. 풀이에 수업에서 안 다룬 개념이 한 단계라도 필요하면 제외.
- `problem-solving-depth.md`에 따라 강의 핵심과 교과서 확장을 구분한다. 관계를 소개한 수업을 완전한 손계산·별도 정리 증명까지 요구한 것으로 확대하지 않는다. 기존에 선정한 문제는 수업 필수 범위의 근거가 아니다. 확장 문제의 존재로 정리노트 필수 깊이를 늘리지 않는다.
- 8~12문항. 난이도는 아래 출제 명세표의 문항 수별 표를 따른다. 명세표가 없을 때만 개념 확인(level 1) : 계산(2) : 도전(3) ≈ 5 : 4 : 1.
  적합한 후보가 부족하면 억지로 수업 밖 개념·중복 심화를 더하지 않는다. 부족한 수·근거와 미충족 명세를 RUN과 보고에 남긴다. 이 기록은 검사 통과나 요구 면제가 아니며, 미충족 팩을 자동 승인하지 않는다.

## 출제 명세표 (`<REPO>/시험결과/출제명세표.json`)
실제 시험의 요구 구조를 복습문제에 옮긴다. 주제 비중은 옮기지 않는다(기말은 중간고사 뒤 강의라고 본다). 사람이 읽는 표는 같은 폴더의 `출제명세표.md`.
1. `targets`를 읽는다.
   - 난이도 1:2:3: 8문항 1:5:2, 9문항 1:6:2, 10문항 2:6:2, 11문항 2:6:3, 12문항 2:7:3.
   - 요구가 2개 이상인 문제가 절반 이상.
   - 마지막 요구가 계산이 아닌(읽기·판정·설명·지정 꼴) 문제가 절반 이상.
   - 앞 소문항 결과를 이어 쓰는 카드 1개 이상. MML 예제를 숫자 그대로 (a)/(b)로 나눠 (b)가 (a)의 결과를 쓰게 한다.
   - 팩의 수업 날짜(`sessions`)마다 난이도 2 이상 문제 1개 이상.
2. 문제마다 `RUN/blueprint.json`에 태그를 적는다. 형식은 `scripts/check_blueprint.py` 머리말에 있다.
   - `asks`: 카드 `.ask`가 구하라는 항목 수. `last_ask`: 끝 항목의 종류(계산 / 읽기 / 판정 / 설명 / 지정 꼴). `chained`: (b)가 (a)의 결과를 쓰면 `true`.
   - 맞는 MML 문제가 없어 목표를 못 채우면 억지로 끼우지 않는다. `gaps`에 같은 키(`levels`, `multi_ask`, `non_calc_last`, `chained`, `dates`)로 이유를 적는다.
3. 검증: `uv run python "$SKILL/scripts/check_blueprint.py" "$RUN/manifest.json" "$RUN/blueprint.json" "$REPO/시험결과/출제명세표.json"` 결과가 `OK`. 자작 문제가 있으면 `--self-checks "$RUN/self-checks.json"`을 붙인다.
4. 명세표 파일이 없으면 이 절차를 건너뛰고 보고서에 적는다.

### 덧붙이는 요구
원래 문제의 답에서 새 개념 없이 바로 나오는 항목만 끝에 덧붙일 수 있다.
- 읽기: 행렬·야코비안의 차원, 완전제곱식에서 평균·분산, 결과 분포를 평균·공분산과 함께 명시.
- 판정: 직교 확인, 독립 여부, 정규화 여부를 수치로 근거.
- "왜"를 묻는 설명은 MML 원문에 그 설명이 있을 때만 쓴다.
- 덧붙인 항목은 `.ask`의 마지막 `<li>`로 따로 둔다. 문장 속 "and" 뒤에 묻지 않는다. 실제 시험에서 놓친 항목이 모두 이 자리였다.
- 정답은 다른 정답과 같이 `answers.py`로 계산해 `terms`에 넣는다.

## 자작 문제 (명세표 빈칸 전용)
MML 후보를 모두 본 뒤에도 명세표 목표가 비면, 그 빈칸에만 직접 만든 문제를 넣을 수 있다. `gaps`에 이유를 적고 넘어가도 된다.
- 조건(모두 `check_blueprint.py`가 검사한다):
  - MML 문제만 세었을 때 실제로 비는 목표만 채운다. `fills`: `multi_ask` / `non_calc_last` / `chained` / `dates` 중 하나. 난이도 비율(`levels`)은 자작으로 맞추지 않는다.
  - `dates`를 채우면 그 날짜의 난이도 2 이상 문제여야 한다.
  - 팩당 최대 `targets.max_self_made`(2)문항.
  - `uses`: 풀이 단계가 기대는 이번 팩 토픽 id 전부. 예고 토픽과 `-links` 토픽은 쓸 수 없다. 이 토픽들로 풀 수 없으면 만들지 않는다.
  - `RUN/self-checks.py`(sympy)가 문제 조건에서 정답을 처음부터 계산해 소문항마다 assert하고, 문제가 성립하는지(가역, 적분 1, 양의 정부호 등)도 assert한다. 결과는 `RUN/self-checks.json`에 `{"pN": {"status": "pass", "method": "sympy exact"}}`. 형식은 `시험결과/중간고사/.pack/evidence/answer-checks.py`와 같다.
- manifest: `part`는 `partC`(`{"id": "partC", "title": "C. 명세표 보충", "short": "C 보충"}`), `source`는 `"자작 pN"`(N은 카드 id 번호), `variant`는 `false`. 정답은 `answers.py`에도 넣어 `answer`·`terms`를 채운다.
- 숫자는 정답부터 정한다. 중간 결과(역행렬, 행렬식, 사후 공분산 등)가 작은 정수나 간단한 분수가 되도록 거꾸로 고른다. 중간고사 9번의 $\Phi^\top\Phi=2I$처럼.
- 문장은 한국어, 기호는 수업·MML 표기. 덧붙이는 요구 규칙과 (a)/(b) 이어짐 규칙을 똑같이 따른다.

## 수업 범위가 Part II(8~12장)일 때 — Part II에는 연습문제가 없다
1. **Part A**: 그 장 본문의 `Example N.M` 중 수업에서 다룬 것을 문제로 바꾼다(`variant: true`). 원문은 카드의 "교과서 원문 보기" 토글에 짧게.
2. **Part B**: Part I(2~7장) 연습문제 중 **핵심 개념이 수업에서 다뤄진 것**만. 예: MLE/MAP를 배웠으면 6장 Beta-Bernoulli, 조건부확률; 최소제곱을 배웠으면 5장 기울기, 7장 정상점.
3. 이전 복습팩에서 이미 쓴 문제는 다시 쓰지 않는다(`복습노트/*/.pack/복습문제_*.cards.json` 각 카드의 `data-source` 확인).

## 수업 범위가 Part I(2~7장)일 때
- 그 장의 연습문제를 우선하고, 본문 Example은 보조로.

## 위치 찾기
- 연습문제 PDF: `교과서/연습문제/Chapter_0{2..7}_*_Exercises.pdf`(없으면 아래 목차 방법).
- MML 목차의 `Exercises` 항목(PDF 1-기준 쪽): 2장 70, 3장 102, 4장 143, 5장 176, 6장 228, 7장 253. **책 쪽 = PDF 쪽 − 6.**
- 스니펫:
  ```bash
  REPO=… uv run python - <<'EOF'
  import fitz, os, re
  d = fitz.open(os.path.join(os.environ["REPO"], "교과서/Mathematics_for_Machine_Learning.pdf"))
  print([(t, p) for lvl, t, p in d.get_toc() if t == "Exercises"])
  first = {}
  for i in range(d.page_count):
      for m in re.finditer(r"Example (\d+)\.(\d+)", d[i].get_text()):
          first.setdefault(m.group(0), i + 1)
  print({k: v for k, v in first.items() if k.startswith("Example 9.")})  # 필요한 장
  EOF
  ```
  `Example N.M`의 첫 등장 쪽이 본문 참조일 수 있으니 해당 쪽을 열어 예제 본문인지 확인한다.

## 정답
- 모든 수치 정답은 `fractions.Fraction`(필요하면 `math`)으로 계산해 manifest `answer`와 카드 `terms`에 넣는다.
- 기호 정답(식)은 풀이 단계를 역으로 대입해 한 번 더 확인한다.
