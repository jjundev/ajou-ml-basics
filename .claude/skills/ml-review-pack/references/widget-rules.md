# 위젯 규칙

## 언제
- 팩 전체에 0~2개. "슬라이더를 움직이면 개념이 보이는" 경우만(예: λ와 과적합, prior 강도와 MAP).
- manifest에는 적지 않는다. **메인 에이전트가** 작성자를 띄우기 전에 위젯을 둘 토픽(0~2개)을 정해 그 섹션 작성자 브리프의 `<위젯>` 자리에 적는다(SKILL.md 3단계).
- 섹션 작성자는 브리프에 적힌 토픽에만 위젯을 만든다. "위젯 없음"이면 만들지 않는다(그림은 정적 SVG로). 만든 위젯은 보고에 적는다.

## 마크업
```html
<div class="widget" id="widget-<name>"><h4>🎛️ 직접 해보기: …</h4>
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
- 대표 설정의 수치는 **위젯 스크립트와 같은 수학**으로 계산한다: 위젯 수학을 `<RUN>/work/widget_<name>.js`로 저장하고 `node`로 실행해 좌표·값을 뽑는다.
- 정적 SVG id는 `widget-<name>-static-<n>`(파일명이 된다).
