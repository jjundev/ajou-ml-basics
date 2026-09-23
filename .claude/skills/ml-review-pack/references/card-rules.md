# 문제 카드 규칙

## 작성자 브리프 (메인 에이전트가 1명, model: opus / lite: sonnet)

---
머신러닝기초 복습문제 카드를 쓴다.

- 읽기: `<SKILL>/references/card-rules.md`(이 파일 전체), `<SKILL>/references/problem-selection.md`의 원칙
- 계약: `<RUN>/manifest.json`의 `problems` — id, `source`, `anchor`, `level`, `date`, `terms`, `answer`를 그대로 따른다.
- 금지어: `<forbidden 목록>` — 카드 어디에도(문제, 원문, 힌트, 풀이, "수업과 연결" 줄 포함) 쓰지 않는다. 검사기가 복습문제 페이지 전체를 훑는다. "다음 시간에 배울 …" 같은 예고도 쓰지 않는다.
- 근거: MML PDF `<RUN>/repo/교과서/Mathematics_for_Machine_Learning.pdf`(문제별 쪽은 manifest 옆 `<RUN>/problem-pages.txt`), 정답 계산 `<RUN>/answers.py`, 정리노트 토픽 제목은 manifest
- 출력: `<RUN>/cards/<pid>.html` 문제마다 한 파일. 다른 곳에 쓰지 않는다.
- 임시·보조 파일(스크립트, 초안, 그림 생성 폴더)은 `<RUN>/work/` 아래에만 둔다. 저장소(`STT/`, `강의노트/`, `교과서/`, `복습노트/`)와 scratchpad 루트, `/tmp`에는 아무것도 쓰지 않는다. 한글(NFD) 파일명은 복사하거나 이름을 바꾸지 말고 Python `os.listdir` + `unicodedata.normalize('NFC', …)`로 찾아 그 경로로 연다.
- 자기 검사: 카드별 `terms`가 문자 그대로 있는지, 정답이 `answer`와 같은지, `$` 짝, 금지어 `<forbidden 목록>`이 하나도 없는지. 문제가 `source`의 Example 상자(또는 연습문제) 안 내용 그대로인지 — 변형은 숫자·데이터 값만 바꾸고 구조(그래프 모양, 변수 수, 식의 꼴, 묻는 것)는 그대로. 어긋나면 고치지 말고 보고에 적는다.
- 보고: 카드별 한 줄(출처, 정답), 풀이 중 수업 밖 개념이 필요했던 곳.
---

## 마크업
```html
<article class="card" id="pN" data-source="MML Example 9.1">
  <header class="card-head"><span class="badge src">MML Example 9.1 변형</span><span class="badge level">★</span><span class="tag date">📅 MMDD</span></header>
  <h3>PN. 제목</h3>
  <div class="problem">…한국어 문제… 여러 문항이면 <ol><li>(a) …</li><li>(b) …</li></ol></div>
  <details class="original"><summary>📖 교과서 원문</summary>"…원문 짧게…" — Example 9.1</details>
  <details class="hint"><summary>💡 힌트</summary>…한두 문장…</details>
  <details class="solution"><summary>✅ 풀이</summary><ol class="steps"><li>…</li></ol><p class="answer">정답: …</p></details>
  <p class="link-back">🔗 수업과 연결: <a href="{{NOTE_HREF}}#ANCHOR">토픽 제목</a> — 한 줄 설명</p>
  <label class="done"><input type="checkbox" data-done="pN"> 풀었음</label>
</article>
```
- `data-source`는 manifest `source`와 글자까지 같다. 배지 글자에는 `variant: true`면 " 변형"을 붙인다.
- 난이도 배지: level 1 `★`, 2 `★★`, 3 `★★★ 도전`.
- 원문 인용은 한 카드에 25단어 이내.
- 풀이 마지막 단계에 "수업과의 연결"을 한 줄로(어느 수업의 어떤 말/식과 이어지는지).
- 수식 규칙은 `content-rules.md`의 "수식"과 같다.
