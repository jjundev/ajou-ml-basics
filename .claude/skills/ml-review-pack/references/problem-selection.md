# 문제 선별 규칙 (MML 전용)

## 원칙
- 문제는 **MML 교과서에서만** 가져온다. 자작 문제 금지. 숫자만 바꾼 변형은 본문 예제(`variant: true`)에 한해 허용하고 카드에 "변형" 배지를 단다.
- 출처가 `Example N.M`이면 그 Example의 **회색 상자 안** 내용만 쓴다. PDF 쪽을 열어 상자가 어디서 끝나는지 확인한다. 상자 밖 본문 설명·식(예: Example 8.8 뒤의 동전 실험)은 문제 출처가 아니다.
- "변형"은 숫자·데이터 값만 바꾼다. 구조(그래프 모양과 노드 수, 변수 수, 식의 꼴, 예제를 문제로 바꾸는 것 이상의 질문)를 바꾸면 자작 문제다.
- 수업에서 배운 내용만으로 풀 수 있어야 한다. 풀이에 수업에서 안 다룬 개념이 한 단계라도 필요하면 제외.
- 8~12문항. 난이도 ★(개념 확인) : ★★(계산) : ★★★(도전) ≈ 5 : 4 : 1.

## 수업 범위가 Part II(8~12장)일 때 — Part II에는 연습문제가 없다
1. **Part A**: 그 장 본문의 `Example N.M` 중 수업에서 다룬 것을 문제로 바꾼다(`variant: true`). 원문은 카드의 📖 원문 토글에 짧게.
2. **Part B**: Part I(2~7장) 연습문제 중 **핵심 개념이 수업에서 다뤄진 것**만. 예: MLE/MAP를 배웠으면 6장 Beta-Bernoulli, 조건부확률; 최소제곱을 배웠으면 5장 기울기, 7장 정상점.
3. 이전 복습팩에서 이미 쓴 문제는 다시 쓰지 않는다(`복습노트/복습문제_*.html`의 `data-source` 확인).

## 수업 범위가 Part I(2~7장)일 때
- 그 장의 연습문제를 우선하고, 본문 Example은 보조로.

## 위치 찾기
- 연습문제 PDF: `교과서/연습문제/Chapter_0{2..7}_*_Exercises.pdf`(없으면 아래 목차 방법).
- MML 목차의 `Exercises` 항목(PDF 1-기준 쪽): 2장 70, 3장 102, 4장 143, 5장 176, 6장 228, 7장 253. **책 쪽 = PDF 쪽 − 6.**
- 스니펫:
  ```bash
  REPO=… python3 - <<'EOF'
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
