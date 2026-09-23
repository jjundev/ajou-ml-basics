# 브라우저 검증 (메인 에이전트)

## 서버
file:// 미리보기에서는 스크립트가 돌지 않는다. 빈 포트로 서버를 띄운다.
```bash
PORT=$(python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1])")
python3 -m http.server $PORT --directory "<RUN>/repo" >/dev/null 2>&1 &   # run_in_background
```
URL: `http://localhost:$PORT/복습노트/<파일명>` (한글 그대로). 끝나면 서버를 종료한다.

## 정리노트 (`mcp__Claude_Browser__javascript_tool`)
```js
await new Promise((r) => setTimeout(r, 1500));
const textNodes = Array.from(document.querySelectorAll('main *')).filter((e) => !['SCRIPT', 'STYLE'].includes(e.tagName) && !e.closest('[hidden]'));
({
  katex: document.querySelectorAll('.katex').length,
  katexErrors: document.querySelectorAll('.katex-error').length,
  rawDollar: textNodes.some((e) => Array.from(e.childNodes).some((n) => n.nodeType === 3 && n.textContent.includes('$'))),
  hScroll: document.documentElement.scrollWidth > window.innerWidth,
  widgets: Array.from(document.querySelectorAll('.widget')).map((w) => ({ id: w.id, drawn: Array.from(w.querySelectorAll('svg')).some((s) => !s.closest('[hidden]') && s.childElementCount > 0) })),
})
```
통과: `katexErrors: 0`, `rawDollar: false`, `hScroll: false`, 모든 위젯 `drawn: true`. `read_console_messages`에 오류 없음.

위젯마다 슬라이더 하나를 바꾸고(`input` 이벤트) readout 값이 `.widget-static` 표의 같은 설정 값과 같은지 확인한다.

## 모바일·다크
`resize_window`(`preset: "mobile"`, `colorScheme: "dark"`) → 새로고침 → 위 스크립트 재실행(`hScroll: false`) → 스크린샷으로 그림·위젯 글자가 보이는지 확인 → `preset: "desktop"`, `colorScheme: "light"`로 되돌린다.

## 복습문제
```js
await new Promise((r) => setTimeout(r, 1500));
document.querySelectorAll('details').forEach((d) => { d.open = true; });
await new Promise((r) => setTimeout(r, 300));
({
  cards: document.querySelectorAll('article.card').length,
  katexErrors: document.querySelectorAll('.katex-error').length,
  hScroll: document.documentElement.scrollWidth > window.innerWidth,
})
```
통과: `cards`가 manifest 문제 수, `katexErrors: 0`, `hScroll: false`. 첫 카드의 "수업과 연결" 링크를 눌러 노트 토픽으로 이동하는지 확인.
