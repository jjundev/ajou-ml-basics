# 섹션 작성 규칙

## 작성자 브리프 (메인 에이전트가 섹션마다 1명, 병렬, model: opus / lite: sonnet, GPT이면 sol / lite: luna)

---
머신러닝기초 정리노트의 섹션 `<sid>`(`<섹션 title>`)를 쓴다.

- 읽기: `<SKILL>/references/content-rules.md`(이 파일 전체), 위젯이 있으면 `<SKILL>/references/widget-rules.md`
- 학습 레퍼런스: <학습 레퍼런스> — 필수 읽기로 지정되면 해당 파일 전체를 먼저 읽고, 지정된 토픽에만 적용한다. `적용 없음` 또는 `참고 누락`이면 일반 작성 규칙을 따른다.
- 위젯: <위젯> (메인 에이전트가 정한 것만 만든다. "위젯 없음"이면 이 섹션에는 위젯을 넣지 않는다)
- 계약: `<RUN>/manifest.json`의 섹션 `<sid>` — 토픽 id·제목·`required_terms`·`layers`·`supp`가 정확히 여기 적힌 대로여야 한다.
- 링크: manifest `links` 중 `topic`이 이 섹션에 있는 항목 `<이 섹션의 links 목록>`을 모두 그 토픽 안에 `<a href="…">`로 넣는다. `href`는 글자 그대로 복사(`%20` 포함). 복습문제 링크만은 `{{REVIEW_HREF}}`로 써도 된다(조립 뒤 실제 파일명이 되어 검사를 통과한다).
- 근거: `<RUN>/summaries/stt-*.md`(해당 날짜), `<RUN>/slides.txt`, 필요하면 MML `<RUN>/repo/교과서/Mathematics_for_Machine_Learning.pdf` <쪽>
- 출력: `<RUN>/sections/<sid>.html` **한 파일만**. `<section>`/`<h2>`는 쓰지 않는다(조립기가 감싼다). 임시 파일은 아래 규칙.
- 임시·보조 파일(스크립트, 초안, 그림 생성 폴더)은 `<RUN>/work/` 아래에만 둔다. 저장소(`STT/`, `강의노트/`, `교과서/`, `복습노트/`)와 scratchpad 루트, `/tmp`에는 아무것도 쓰지 않는다. 한글(NFD) 파일명은 복사하거나 이름을 바꾸지 말고 Python `os.listdir` + `unicodedata.normalize('NFC', …)`로 찾아 그 경로로 연다.
- 자기 검사(끝내기 전): 토픽별로 `required_terms`가 모두 문자 그대로 들어갔는지, `$` 짝, `links` 항목이 해당 토픽 안에 있는지, 금지어 `<forbidden 목록>`이 없는지. 금지어는 예고 토픽 `<preview_topic>` 안에서만 허용된다 — 이 토픽에는 예고 제목을 빠뜨리지 말고 쓴다. eli5 레이어마다 문장 수(figcaption 포함)가 3 이하이고 전문용어·기호(θ, σ, 식, 영어 용어)가 없는지 — 있으면 formal 레이어로 옮긴다. 조각 어디에도 이모지를 쓰지 않았는지. `layers`가 빈 목록이 아닌 토픽마다 마지막에 `<div class="sum" hidden>`이 있고, 그 식·용어가 본문과 같은 표기인지. 그림 설명(글, `aria-label`)이 SVG 클래스의 실제 모양(채움/윤곽)과 맞는지.
- 보고: 파일 경로, 토픽별 한 줄, 요약에 있었지만 넣지 않은 것과 이유.
- 공분산 레퍼런스를 적용한 토픽의 자기 검사(`lite` 포함): 가중합과 스칼라 지식의 연결이 있는지, 일반 규칙의 계수 위치·전치·차원이 정확한지, 교차/자기 공분산을 구별했는지 확인한다. 설명됨과 숙달·미확인을 혼동하지 않았는지, 원자료 없이 수업 범위를 넓히거나 교수님 발언을 만들지 않았는지도 확인한다. 확인 예제는 관련 설명에 필요할 때만 쓰며 문제 카드로 자동 추가하지 않는다. 보고에 적용 토픽 id와 사용한 설명 연결을 적는다.
---

## 큰 그림과 수식의 연결
- `big-picture-first.md`를 전체 읽고 메인의 `RUN/learning-map.json` 브리프를 따른다. 첫 학습 토픽은 오늘의 질문·관계·결과·유도 목적·혼동을 수식 전개보다 먼저 설명한다.
- 큰 그림 토픽은 formal 레이어 하나로 작성할 수 있다. eli5·교수님 말씀 의무의 예외이며 기호를 쓸 수 있다. 뒤의 일반 개념 토픽에는 기존 레이어 규칙을 유지한다.
- 각 유도는 구하려는 대상과 계산 목적을 먼저 한 문장으로 연결한다. 기호의 첫 등장에는 뜻·차원·역할을 설명한다. 임시 묶음은 임시 이름임을 밝힌다.
- 섹션 하나가 독립적으로 읽혀도 목표가 보이도록 하되, 큰 그림 표 전체를 모든 섹션에 반복하지 않는다.

## 범위
- 요약의 슬라이드 대조표에서 "다룸/일부"인 내용만 쓴다. "예고만/안 다룸"은 `s<N>-next`에 제목만.
- 수업에서 말한 모든 개념, 칠판 유도, 교수님 비유와 강조 발언을 빠짐없이 싣는다(잡담 제외).
- STT 오인식과 말실수는 올바른 형태로 쓴다. 식이 틀렸던 경우만 각주 한 줄로 "(수업 중 X로 적었다가 정정)".

## 토픽 마크업 (이 순서)
```html
<article class="topic" id="…"><h3>…</h3><div class="tags"><span class="tag date">MMDD 수업</span><span class="tag slide">L0X sN</span></div>
  <div class="layer eli5"><span class="layer-title">쉽게 말하면</span><p class="lead">한 문장 비유</p> …그림… </div>
  <div class="layer formal"><span class="layer-title">정확히 말하면</span> …정의·수식·단계별 유도(ol.steps)… </div>
  <div class="layer prof"><span class="layer-title">교수님 말씀</span> …비유·일화, 원문은 blockquote… </div>
  <div class="layer warn"><span class="layer-title">꼭 기억해요</span> …원문 인용 + (MMDD MM:SS)… </div>   ← 강조 발언이 있을 때만
  <div class="layer supp"><span class="badge supp">보충 · 수업에서 유도하진 않았어요</span> … </div>             ← manifest supp=true만
  <div class="sum" hidden>…페이지 요약(아래)…</div>                                                    ← layers가 빈 목록이 아닌 토픽만, 맨 끝
</article>
```
- 레이어 제목과 배지 글자는 위와 글자 그대로 쓴다. 이모지, 장식 기호(★, ↗, → 같은 화살표 아이콘), "아래를 보세요" 같은 안내 문장은 쓰지 않는다.
- 템플릿이 토픽 하나를 한 화면에 보여 준다. 토픽은 그것만 읽어도 이해되게 쓰고, "위에서 본 것처럼"처럼 앞 토픽의 위치에 기대는 말 대신 `<a href="#토픽id">토픽 제목</a>`으로 잇는다.
- 요약·예고 섹션: 치트시트는 표(`<div class="table-wrap"><table>`), 예고는 `<ul>`, 링크는 `<ul><li><a>`.
- 복습문제 링크는 `href="{{REVIEW_HREF}}"`로 쓴다(조립기가 실제 파일명으로 바꾼다. manifest의 파일명을 그대로 써도 된다). 다른 링크는 manifest `href`를 글자 그대로.

## 페이지 요약 (`.sum`)
화면 오른쪽 "페이지 요약" 패널에 그 토픽의 핵심만 보여 준다. 템플릿이 토픽의 **직계 자식** `.sum`을 패널로 옮기므로 토픽 안 맨 끝에, 레이어 밖에 둔다. `hidden`은 꼭 붙인다(본문에 두 번 보이지 않게).
```html
<div class="sum" hidden>
  <p class="sum-lead">토픽 핵심 한 문장("~해요" 체)</p>
  <p class="panel-label">핵심 식</p>
  <ul class="eq-list"><li><span class="eq-name">식 이름</span>$$…$$</li></ul>
  <p class="panel-label">용어</p>
  <dl class="terms"><dt>용어(영어)</dt><dd>한 줄 뜻</dd></dl>
</div>
```
- 새 내용을 쓰지 않는다. 본문(formal 레이어)에 이미 나온 식·용어를 **같은 TeX 표기로** 1~3개씩 고른다. 요약에만 있는 식이나 설명은 두지 않는다.
- 식이 없는 토픽은 "핵심 식" 줄과 `eq-list`를 빼고, 용어가 없으면 "용어" 줄과 `dl`을 뺀다. `sum-lead`는 항상 쓴다.
- 요약·예고 섹션처럼 `layers`가 `[]`인 토픽에는 두지 않는다.

## 문체
- 쉽게 말하면(eli5): 초등학생이 이해할 1~3문장(figcaption 포함) + 그림. 전문용어·기호 없이(필요하면 정확히 말하면에 쓴다). 토스처럼 짧고 다정한 "~해요" 체.
- 정확히 말하면(formal): 빠짐없이, 정확하게. 유도는 한 줄에 한 단계. 문장은 "~해요" 체, 유도 단계는 식 위주로 짧게.
- 교수님 말씀(prof)/꼭 기억해요(warn): 원문 인용은 15단어 안팎으로 줄이고 `(0914 26:00)`처럼 출처.
- UI 글은 한국어, 전문용어는 영어 병기(예: 과적합(overfitting)). 한 문장에 한 가지만 말하고, 군더더기 수식어("아주", "정말", "한번")는 뺀다.

## 수식
- `$…$`(인라인), `$$…$$`(디스플레이)만. 본문에 리터럴 `$` 금지.
- TeX 안에 `<`, `>`, `&` 금지 → `\lt`, `\gt`. 정렬 환경 대신 `$$` 줄을 나눈다.
- PDF 템플릿은 40자가 넘고 중괄호·`\left…\right` 바깥에 관계 기호(`=`, `\le(q)`, `\ge(q)`, `\approx`, `\Rightarrow`)가 있는 `$…$`를 display로 바꾸고 관계 기호마다 줄을 나눈다. 문장 속에 한 줄로 두려는 긴 식(행렬 정의 `A=\begin{bmatrix}…\end{bmatrix}` 등)은 식 전체를 `${…}$`처럼 중괄호로 감싼다. 여러 식을 쉼표로 나란히 쓸 때도 식마다 감싼다(`${\mathbf{A}=…},\quad{\mathbf{B}=…}$`).
- 벡터는 `\mathbf{x}`, 파라미터 벡터는 `\boldsymbol{\theta}`, 행렬 `\mathbf{X}` — manifest `required_terms`와 같은 표기.

## SVG 그림
- 개념 토픽마다 eli5 레이어에 그림 1개 이상(흐름도, 막대, 곡선 등).
- `<figure class="figure"><svg id="fig-<kebab>" viewBox="…" role="img" aria-label="한국어 설명">…</svg><figcaption>…</figcaption></figure>`
- 색은 클래스로만: `fig-ink`, `fig-accent`, `fig-danger`, `fig-dot`, `fig-text`, `fig-muted`. 하드코딩 색 금지(다크모드).
- 채움과 윤곽: `fig-ink`, `fig-accent`, `fig-danger`는 선만 그린다(`fill:none`). 속이 칠해진 점·도형은 `fig-dot`(강조색 채움)뿐이다(`fig-text`, `fig-muted`는 글자용). 글·figcaption·`aria-label`에서 "색칠된", "채워진"은 `fig-dot` 도형에만 쓰고, 선만 있는 도형은 "테두리", "선"으로 부른다.
- 글자 12~14px, SVG `<text>`에 `$` 금지(θ, σ, ₁ 같은 유니코드).
- id는 페이지 전체에서 유일해야 한다(`fig-` + 토픽 고유 단어).

## PDF 연결
노트의 마지막 links 토픽에 PDF 문제지/해설지 링크를 메인 에이전트가 검증 후 삽입한다. 기존 review HTML link는 유지하고 문항 수는 실제 카드 수로 계산한다.
