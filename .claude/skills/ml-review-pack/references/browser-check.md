# 브라우저 검증 (메인 에이전트)

## 서버
file:// 미리보기에서는 스크립트가 돌지 않는다. 빈 포트로 서버를 띄운다. 셸 상태는 Bash 호출 사이에 이어지지 않으므로 포트 번호를 먼저 출력해 두고, 이후 명령과 URL에는 그 숫자를 직접 쓴다.
1. 빈 포트 찾기(출력된 숫자가 `<port>`):
   ```bash
   python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1])"
   ```
2. 서버 띄우기: Bash 도구의 `run_in_background: true`로 실행한다(명령 끝에 `&`를 붙이지 않는다).
   ```bash
   python3 -m http.server <port> --directory "<RUN>/repo"
   ```
3. URL: `http://localhost:<port>/복습노트/<파일명>` (한글 그대로).
4. 끝나면 서버를 종료한다: 그 백그라운드 작업을 멈추거나(TaskStop 등), `pkill -f "http.server <port>"`.

## 측정 전 준비
브라우저 창이 숨겨져 있으면 `document.documentElement.clientWidth`가 0이 되어 `hScroll`이 거짓 양성으로 나온다. 측정 전에 `resize_window`로 크기를 명시하고(`width: 1280`, `height: 900`) `document.documentElement.clientWidth > 0`을 확인한다. `.katex-mathml` 안 요소는 화면에 보이지 않으므로 넘침 원인으로 치지 않는다. 스크롤 직후 스크린샷은 늦게 반영될 수 있으니 1초쯤 기다린 뒤 찍는다.

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
`resize_window`(`preset: "mobile"`, `colorScheme: "dark"`) → 새로고침 → `clientWidth > 0` 확인 → 위 스크립트 재실행(`hScroll: false`) → 스크린샷으로 그림·위젯 글자가 보이는지 확인 → `preset: "desktop"`, `colorScheme: "light"`로 되돌린다.

## 복습문제
측정 전에 다시 `resize_window`(`width: 1280`, `height: 900`) → `clientWidth > 0` 확인(앞 단계의 `preset: "desktop"`은 창 크기를 창 자체 크기로 되돌려 숨은 창에서는 0이 될 수 있다).
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

## 마무리
모든 검사가 끝나면 `resize_window`(`preset: "desktop"`, `colorScheme: "light"`)로 되돌리고 서버를 종료한다(위 "서버" 4).
