# 문제 카드 규칙

## 작성자 브리프 (메인 에이전트가 1명, model: opus / lite: sonnet, GPT이면 sol / lite: luna)

---
머신러닝기초 복습문제 카드를 쓴다.

- 읽기: `<SKILL>/references/card-rules.md`(이 파일 전체), `<SKILL>/references/problem-selection.md`의 원칙
- 계약: `<RUN>/manifest.json`의 `problems` — id, `source`, `anchor`, `level`, `date`, `terms`, `answer`를 그대로 따른다.
- 금지어: `<forbidden 목록>` — 카드 어디에도(문제, 원문, 힌트, 풀이 포함) 쓰지 않는다. 검사기가 복습문제 페이지 전체를 훑는다. "다음 시간에 배울 …" 같은 예고도 쓰지 않는다.
- 근거: MML PDF `<RUN>/repo/교과서/Mathematics_for_Machine_Learning.pdf`(문제별 쪽은 manifest 옆 `<RUN>/problem-pages.txt`), 정답 계산 `<RUN>/answers.py`, 정리노트 토픽 제목은 manifest
- 출력: `<RUN>/cards/<pid>.html` 문제마다 한 파일. 다른 곳에 쓰지 않는다(임시 파일은 아래 규칙).
- 임시·보조 파일(스크립트, 초안, 그림 생성 폴더)은 `<RUN>/work/` 아래에만 둔다. 저장소(`STT/`, `강의노트/`, `교과서/`, `복습노트/`)와 scratchpad 루트, `/tmp`에는 아무것도 쓰지 않는다. 한글(NFD) 파일명은 복사하거나 이름을 바꾸지 말고 Python `os.listdir` + `unicodedata.normalize('NFC', …)`로 찾아 그 경로로 연다.
- 자기 검사: 카드별 `terms`가 문자 그대로 있는지, 정답이 `answer`와 같은지, `$` 짝, 금지어 `<forbidden 목록>`이 하나도 없는지. 문제가 `source`의 Example 상자(또는 연습문제) 안 내용 그대로인지 — 변형은 숫자·데이터 값만 바꾸고 구조(그래프 모양, 변수 수, 식의 꼴, 묻는 것)는 그대로. 어긋나면 고치지 말고 보고에 적는다.
- 보고: 카드별 한 줄(출처, 정답), 풀이 중 수업 밖 개념이 필요했던 곳.
---

## 마크업
```html
<article class="card" id="pN" data-source="MML Example 9.1">
  <h3>PN. 제목</h3>
  <div class="problem"><div class="conditions">…주어진 조건·식·표·그림…</div><div class="ask">…구할 것… 여러 문항이면 <ol><li>(a) …</li><li>(b) …</li></ol></div></div>
  <details class="original"><summary>교과서 원문 보기</summary>"…원문 짧게…" — Example 9.1</details>
  <details class="hint"><summary>힌트 보기</summary>…한두 문장…</details>
  <details class="solution"><summary>풀이 보기</summary><ol class="steps"><li>…</li></ol><p class="answer">정답: …</p></details>
</article>
```
- `data-source`는 manifest `source`와 글자까지 같다. 출처는 이 속성과 교과서 원문 보기 안에만 두고, 화면에 출처 배지는 달지 않는다.
- 난이도(`level`)와 수업 날짜(`date`)는 문제 구성에만 쓰고, 카드 위에 배지·태그 줄(`card-head`)을 두지 않는다.
- 카드에 "수업에서 다시 보기", "수업과 연결" 같은 연결 안내 줄을 두지 않는다. manifest `anchor`는 풀이가 기대는 토픽을 고르는 데만 쓴다.
- 이모지와 장식 기호(★, ↗ 등)는 쓰지 않는다. 문제·힌트·풀이 문장은 토스처럼 짧고 다정한 "~해요" 체로 쓴다(예: "평균을 구해 보세요.", "더한 뒤 개수로 나눠요.").
- 템플릿이 카드 하나를 한 화면에 보여 준다. 카드는 다른 카드 없이도 풀 수 있게 쓴다.
- 원문 인용은 한 카드에 25단어 이내.
- 풀이 마지막 단계는 계산·증명의 결론으로 마무리한다. 풀이 안에도 별도의 "수업과의 연결" 안내 줄을 넣지 않는다.
- 수식 규칙은 `content-rules.md`의 "수식"과 같다.

## PDF 계약
- `.conditions`와 `.ask`는 `.problem`의 직계 자식으로 각각 한 개다. 조건은 질문보다 먼저 쓰고 원본 순서·수치·식·소문항을 보존한다. 증명 목표 식은 ask 안에 유지한다. 풀이와 최종 답은 solution에만 둔다.
- 문제지 오른쪽 Hint 띠에는 `<details class="hint" data-label="…">`의 짧은 힌트가 보인다(태그 없는 60자 이내 명사형 한 구절, inline `$…$`만, `$$` 금지). 답안 Hint 부록에서는 이 구절이 제목, 힌트 본문이 설명이 된다. 없으면 "풀이 방향"이 보인다.
- SVG/표는 원문에 보관하고 PDF 변환기가 별도 그림으로 고정한다. SVG viewBox와 화살표 정의를 보존한다. 파일 그림은 현재 날짜 stage 폴더(예: figures_<range>/diagram.png)에 복사하고 원본 HTML 기준 상대 src를 쓴다. 메인 에이전트는 이 참조 자산도 HTML/MD/PDF와 함께 배포한다.
