# 예습노트 섹션 작성 규칙

## 작성자 브리프 (메인 에이전트가 섹션마다 1명, 병렬, model: opus / lite: sonnet, GPT이면 sol / lite: luna)

---
머신러닝기초 예습노트의 섹션 `<sid>`(`<섹션 title>`)를 쓴다. 학생이 **수업을 들으면서 옆에 띄워 보는** 노트다. 짧게 쓴다.

- 읽기: `<SKILL>/references/content-rules.md`(이 파일 전체)
- 계약: `<RUN>/manifest.json`의 섹션 `<sid>` — 토픽 id·제목·`slides`·`required_terms`·`layers`·`supp`를 정확히 따른다.
- 링크: 이 섹션 토픽의 `links` `<이 섹션의 links 목록>`을 그 토픽 안에 `<a href="…">`로 넣는다. `href`는 글자 그대로(`%20` 포함).
- 근거: `<RUN>/slides.txt`(`=== <Lxx> sN ===` 구획), 필요하면 MML `<RUN>/repo/교과서/Mathematics_for_Machine_Learning.pdf` <쪽>
- 출력: `<RUN>/sections/<sid>.html` **한 파일만**. `<section>`/`<h2>`는 쓰지 않는다(조립기가 감싼다). 임시 파일은 `<RUN>/work/`에만.
- 자기 검사(끝내기 전): 그림이 있으면 곡선 증가·감소 방향이 슬라이드와 맞는지(SVG y축은 아래로 커진다), `required_terms`가 문자 그대로 있는지, 슬라이드 태그 `<Lxx> <slides>`가 글자 그대로 있는지(범위는 en dash `–`), `$` 짝, 토픽 본문 600자 이하(공백·수식·그림 제외), 쉽게 말하면 2문장 이하이고 기호·영어 약어·전문용어가 없는지, 들을 때 포인트 2항목 이하이고 "~하실 거예요" 같은 예측이 없는지, 이모지 없음, `layers`가 빈 목록이 아닌 토픽마다 맨 끝에 `<div class="sum" hidden>`.
- 보고: 파일 경로, 토픽별 한 줄, 슬라이드에 있었지만 뺀 것과 이유.
---

## 범위
- 슬라이드에 있는 내용만 설명한다. 슬라이드에 없는 설명(교과서에서 가져온 유도·배경)은 `supp`가 `true`인 토픽의 보충 레이어에만 쓴다.
- 교수님 말씀이나 수업 중 강조는 아직 모르므로 **추측해서 쓰지 않는다**.

## 토픽 마크업 (이 순서)
```html
<article class="topic" id="…"><h3>…</h3><div class="tags"><span class="tag slide">L04 s12–14</span></div>
  <div class="layer eli5"><span class="layer-title">쉽게 말하면</span><p class="lead">한 문장 비유</p> …그림(필요할 때만)… </div>
  <div class="layer formal"><span class="layer-title">정확히 말하면</span> …핵심 식 + 기호 뜻… </div>
  <div class="layer listen"><span class="layer-title">들을 때 포인트</span><ul><li>…</li></ul></div>   ← manifest layers에 listen이 있을 때만
  <div class="layer supp"><span class="badge supp">교과서 보충</span> … </div>                              ← manifest supp=true만
  <div class="sum" hidden>…페이지 요약…</div>                                                          ← layers가 빈 목록이 아닌 토픽만, 맨 끝
</article>
```
- 레이어 제목과 배지 글자는 위와 글자 그대로 쓴다. `layer prof`, `layer warn`은 쓰지 않는다(검사 실패).
- 슬라이드 태그는 manifest `lecture`와 `slides`를 공백 하나로 이은 글자 그대로이고, 태그 span 안에는 그 글자만 쓴다(검사기가 정확히 비교한다). `slides`가 빈 문자열인 `s0` 토픽은 `<div class="tags">`를 생략한다.
- 토픽은 그것만 읽어도 이해되게 쓰고, 앞 토픽은 `<a href="#토픽id">토픽 제목</a>`으로 잇는다.
- "미리 알아둘 것"(`s0`) 토픽: 이 강의를 따라가려면 필요한 선수 개념 하나. 이전 복습노트나 MML 쪽 링크를 건다.
- "한눈에 보기"(마지막 섹션): `-cheatsheet`는 표(`<div class="table-wrap"><table>`), `-links`는 `<ul><li><a>`.

## 분량 (검사기가 센다)
- 토픽 본문 **600자 이하**: 레이어 안 글자만 센다. 공백, `$…$`/`$$…$$` 수식, 그림, 레이어 제목, 배지, 태그, 요약 패널은 빼고 센다.
- **한 화면**: 토픽 하나가 720×900 창에서 스크롤 없이 보여야 한다(브라우저 검사). 글자 수가 600자 안이어도 디스플레이 수식·목록·그림이 많으면 넘친다. 그림이 있는 토픽은 글을 300자 안팎으로 줄인다.
- **쉽게 말하면**: 2문장 이하("."·"?"·"!" 뒤 공백으로 나눈다), 전문용어·기호 없이. 그림은 슬라이드가 그림으로 설명하는 개념일 때만 1개.
- **정확히 말하면**: 슬라이드의 핵심 식을 쓰고, 기호마다 뜻 한 줄(`<ul>`). 유도는 쓰지 않거나 한 줄에 한 단계씩 3단계 이하.
- **들을 때 포인트**: 2항목 이하. 학생이 수업 중에 **할 일**을 쓴다: "~가 나오면 ~를 확인해 보세요", "~와 연결해 보세요". 교수님이 무엇을 말할지 예측하지 않는다("설명하실 거예요", "강조하실 거예요"는 검사 실패). 예: "$\frac{\partial \mathbf{e}}{\partial \boldsymbol{\theta}} = -\boldsymbol{\Phi}$가 나오면 야코비안의 $\mathbf{A}\mathbf{x}$ 규칙과 연결해 보세요", "앞 슬라이드의 $\boldsymbol{\theta}$가 여기서 다시 나와요".
- 문체: "~해요" 체, 한 문장에 한 가지, 군더더기 수식어 없이. 전문용어는 영어 병기(예: 최소제곱(least squares)).

## 페이지 요약 (`.sum`)
```html
<div class="sum" hidden>
  <p class="sum-lead">토픽 핵심 한 문장("~해요" 체)</p>
  <p class="panel-label">핵심 식</p>
  <ul class="eq-list"><li><span class="eq-name">식 이름</span>$$…$$</li></ul>
  <p class="panel-label">용어</p>
  <dl class="terms"><dt>용어(영어)</dt><dd>한 줄 뜻</dd></dl>
</div>
```
- 본문에 이미 나온 식·용어를 **같은 TeX 표기로** 1~2개. 식이 없으면 "핵심 식" 줄과 `eq-list`를, 용어가 없으면 "용어" 줄과 `dl`을 뺀다.

## 수식
- `$…$`, `$$…$$`만. 본문에 리터럴 `$` 금지. TeX 안 `<`, `>`, `&` 금지(`\lt`, `\gt`).
- 벡터 `\mathbf{x}`, 파라미터 벡터 `\boldsymbol{\theta}`, 행렬 `\mathbf{X}` — manifest `required_terms`와 같은 표기.

## SVG 그림
- `<figure class="figure"><svg id="fig-<kebab>" viewBox="…" role="img" aria-label="한국어 설명">…</svg><figcaption>…</figcaption></figure>`
- 색은 클래스로만: `fig-ink`, `fig-accent`, `fig-danger`(선만), `fig-dot`(채움), `fig-text`, `fig-muted`(글자). 하드코딩 색 금지.
- 글자 12~14px, SVG `<text>`에 `$` 금지(θ, σ, ₁ 같은 유니코드). id는 페이지 전체에서 유일.
- `<text>`에는 `fig-text`·`fig-muted`만 쓴다(`fig-accent` 같은 선 클래스를 붙이면 글자에 윤곽선이 생겨 뭉개진다). 선과 글을 짝지으려면 figcaption에 "파란 선(…)"처럼 적는다.
- **SVG y축은 아래로 커진다.** 값이 줄어드는 곡선은 y 좌표가 커져야 한다. 곡선을 그린 뒤 시작·끝 y 좌표로 증가·감소 방향이 슬라이드와 맞는지 확인한다.
- 그림은 가로로 넓게(viewBox 가로:세로 4:1 안팎) 그려 한 화면 높이를 아낀다.
- 위젯(`class="widget"`)은 만들지 않는다.
