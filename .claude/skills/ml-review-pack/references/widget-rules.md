# 위젯 규칙

## 언제
- 팩 전체에 0~2개. 같은 데이터를 두고 한 값을 움직여 중간 상태·최댓값·경계를 확인하는 등 직접 조작이 비교에 도움이 되는 토픽에 배정한다. 대표 상태만 봐도 차이가 선명하면 그림이나 표로 비교한다.
- 기존 노트에서 같은 대상과 조작으로 그 질문에 답하는 위젯이 있으면 먼저 재사용을 검토한다. 관찰이 먼저 필요한 위치에 배치할 때는 기존 ID와 링크를 보존한다.
- manifest에는 적지 않는다. **메인 에이전트가** 작성자를 띄우기 전에 위젯을 둘 토픽(0~2개)을 정해 그 섹션 작성자 브리프의 `<위젯>` 자리에 적는다(SKILL.md 3단계).
- 섹션 작성자는 브리프에 배정된 위젯을 만들고 보고한다. "위젯 없음"으로 지정된 토픽의 비교는 정적 그림이나 표로 작성한다.

## 마크업
```html
<div class="widget" id="widget-<name>"><h4>직접 해 보기: …</h4>
  <p class="widget-help">무엇을 움직이면 무엇이 보이는지 한 문장.</p>
  <div class="controls">
    <label>차수 <input type="range" id="<name>-a" min="1" max="9" step="1" value="3"> <b id="<name>-a-val">3</b></label>
  </div>
  <svg id="<name>-plot" viewBox="0 0 560 300" role="img" aria-label="…"></svg>
  <p class="readout">… <b id="<name>-out">…</b></p>
  <p class="legend"><span><span class="sw fit"></span>설명</span>…</p>
  <div class="widget-static" hidden>
    <figure class="figure"><svg id="widget-<name>-static-1" viewBox="0 0 560 300" role="img" aria-label="대표 설정 1">…</svg></figure>
    <div class="table-wrap"><table><tr><th>설정</th><th>결과</th></tr><tr><td>…</td><td>…</td></tr></table></div>
  </div>
</div>
<script id="widget-<name>-ui">(function () { /* 수학 + 그리기, 전역 오염 금지 */ })();</script>
```
- 스크립트는 조각 파일 끝에 둔다. 조립기가 `</body>` 앞으로 옮긴다. 외부 라이브러리 금지.
- 그래프 선·점은 템플릿 CSS 클래스(`axis`, `tick`, `plot-truth`, `plot-fit`, `pt-train`, `pt-test`, `plot-like`, `plot-prior`, `plot-post`, `mark-ml`, `mark-map`, `fig-*`)를 쓴다.

## `.widget-static` (필수 — 없으면 check_html이 실패)
- MD 버전에서 위젯 대신 보이는 정적 대체물. `hidden` 속성으로 HTML에서는 숨긴다.
- 대표 설정 2~4개의 정적 SVG(위젯과 같은 모양, 스크립트 없이 path 좌표를 미리 계산해 박아 넣음)와 결과 표.
- 본문에서 다음 식에 사용하는 대표 설정을 반드시 포함한다. 설정마다 유지한 대상과 읽을 값의 뜻이 드러나야 한다.
- 대표 설정의 수치는 **위젯 스크립트와 같은 수학**으로 계산한다: 위젯 수학을 `<RUN>/work/widget_<name>.js`로 저장하고 `node`로 실행해 좌표·값을 뽑는다.
- 정적 SVG id는 `widget-<name>-static-<n>`(파일명이 된다).
