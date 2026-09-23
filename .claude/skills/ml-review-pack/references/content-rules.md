# 섹션 작성 규칙

## 작성자 브리프 (메인 에이전트가 섹션마다 1명, 병렬, model: opus / lite: sonnet)

---
머신러닝기초 정리노트의 섹션 `<sid>`(`<섹션 title>`)를 쓴다.

- 읽기: `<SKILL>/references/content-rules.md`(이 파일 전체), 위젯이 있으면 `<SKILL>/references/widget-rules.md`
- 계약: `<RUN>/manifest.json`의 섹션 `<sid>` — 토픽 id·제목·`required_terms`·`layers`·`supp`가 정확히 여기 적힌 대로여야 한다.
- 링크: manifest `links` 중 `topic`이 이 섹션에 있는 항목 `<이 섹션의 links 목록>`을 모두 그 토픽 안에 `<a href="…">`로 넣는다. `href`는 글자 그대로 복사(`%20` 포함). 복습문제 링크만은 `{{REVIEW_HREF}}`로 써도 된다(조립 뒤 실제 파일명이 되어 검사를 통과한다).
- 근거: `<RUN>/summaries/stt-*.md`(해당 날짜), `<RUN>/slides.txt`, 필요하면 MML `<RUN>/repo/교과서/Mathematics_for_Machine_Learning.pdf` <쪽>
- 출력: `<RUN>/sections/<sid>.html` **한 파일만**. `<section>`/`<h2>`는 쓰지 않는다(조립기가 감싼다).
- 자기 검사(끝내기 전): 토픽별로 `required_terms`가 모두 문자 그대로 들어갔는지, `$` 짝, `links` 항목이 해당 토픽 안에 있는지, 금지어 `<forbidden 목록>`이 없는지. 금지어는 예고 토픽 `<preview_topic>` 안에서만 허용된다 — 이 토픽에는 예고 제목을 빠뜨리지 말고 쓴다.
- 보고: 파일 경로, 토픽별 한 줄, 요약에 있었지만 넣지 않은 것과 이유.
---

## 범위
- 요약의 슬라이드 대조표에서 "다룸/일부"인 내용만 쓴다. "예고만/안 다룸"은 `s<N>-next`에 제목만.
- 수업에서 말한 모든 개념, 칠판 유도, 교수님 비유와 강조 발언을 빠짐없이 싣는다(잡담 제외).
- STT 오인식과 말실수는 올바른 형태로 쓴다. 식이 틀렸던 경우만 각주 한 줄로 "(수업 중 X로 적었다가 정정)".

## 토픽 마크업 (이 순서)
```html
<article class="topic" id="…"><h3>…</h3><div class="tags"><span class="tag date">📅 MMDD</span><span class="tag slide">L0X sN</span></div>
  <div class="layer eli5"><span class="layer-title">🧸 쉽게 말하면</span><p class="lead">한 문장 비유</p> …그림… </div>
  <div class="layer formal"><span class="layer-title">📐 정식 버전</span> …정의·수식·단계별 유도(ol.steps)… </div>
  <div class="layer prof"><span class="layer-title">🎙️ 교수님 한마디</span> …비유·일화, 원문은 blockquote… </div>
  <div class="layer warn"><span class="layer-title">⚠️ 강조 포인트</span> …원문 인용 + (MMDD MM:SS)… </div>   ← 강조 발언이 있을 때만
  <div class="layer supp"><span class="badge supp">📎 보충 · 수업 미유도</span> … </div>             ← manifest supp=true만
</article>
```
- 요약·예고 섹션: 치트시트는 표(`<div class="table-wrap"><table>`), 예고는 `<ul>`, 링크는 `<ul><li><a>`.
- 복습문제 링크는 `href="{{REVIEW_HREF}}"`로 쓴다(조립기가 실제 파일명으로 바꾼다. manifest의 파일명을 그대로 써도 된다). 다른 링크는 manifest `href`를 글자 그대로.

## 문체
- 🧸: 초등학생이 이해할 1~3문장 + 그림. 전문용어 없이. "~예요" 체.
- 📐: 빠짐없이, 정확하게. 유도는 한 줄에 한 단계. "~다" 체.
- 🎙️/⚠️: 원문 인용은 15단어 안팎으로 줄이고 `(0914 26:00)`처럼 출처.
- UI 글은 한국어, 전문용어는 영어 병기(예: 과적합(overfitting)).

## 수식
- `$…$`(인라인), `$$…$$`(디스플레이)만. 본문에 리터럴 `$` 금지.
- TeX 안에 `<`, `>`, `&` 금지 → `\lt`, `\gt`. 정렬 환경 대신 `$$` 줄을 나눈다.
- 벡터는 `\mathbf{x}`, 파라미터 벡터는 `\boldsymbol{\theta}`, 행렬 `\mathbf{X}` — manifest `required_terms`와 같은 표기.

## SVG 그림
- 개념 토픽마다 🧸 레이어에 그림 1개 이상(흐름도, 막대, 곡선 등).
- `<figure class="figure"><svg id="fig-<kebab>" viewBox="…" role="img" aria-label="한국어 설명">…</svg><figcaption>…</figcaption></figure>`
- 색은 클래스로만: `fig-ink`, `fig-accent`, `fig-danger`, `fig-dot`, `fig-text`, `fig-muted`. 하드코딩 색 금지(다크모드).
- 글자 12~14px, SVG `<text>`에 `$` 금지(θ, σ, ₁ 같은 유니코드).
- id는 페이지 전체에서 유일해야 한다(`fig-` + 토픽 고유 단어).
