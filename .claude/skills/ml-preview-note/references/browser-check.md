# 브라우저 검증 (메인 에이전트)

## 서버
file:// 미리보기에서는 스크립트가 돌지 않는다. 빈 포트로 서버를 띄운다. 셸 상태가 이어지지 않으므로 포트 번호를 먼저 출력하고 이후에는 그 숫자를 직접 쓴다.
1. 빈 포트: `python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1])"`
2. 서버: Bash 도구의 `run_in_background: true`로 `python3 -m http.server <port> --directory "<RUN>/repo"` (끝에 `&` 없이)
3. URL: `http://localhost:<port>/예습노트/<Lxx>/<파일명>` (한글 그대로)
4. 끝나면 그 백그라운드 작업을 멈추거나 `pkill -f "http.server <port>"`.

## 측정 전 준비
숨은 창에서는 `document.documentElement.clientWidth`가 0이 된다. 측정 전에 `resize_window`로 크기를 명시하고 `clientWidth > 0`을 확인한다. `.katex-mathml` 안 요소는 넘침 원인으로 치지 않는다.

## 화면별 측정 함수
템플릿은 한 번에 토픽 하나를 `.content` 안에 보여 준다. 아래 함수를 매 실행에 붙여 넣는다. `over`는 가로로 넘친 화면, `tall`은 세로 스크롤이 필요한 화면이다.
```js
async function measureScreens() {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const scroller = document.querySelector('.content') || document.documentElement;
  const screens = Array.from(document.querySelectorAll('main .screen'));
  const over = [], tall = [];
  for (const s of screens.length ? screens : [document.querySelector('main')]) {
    if (screens.length) { location.hash = s.id ? '#' + s.id : ''; await wait(150); }
    document.getAnimations().forEach((a) => a.finish());
    if (scroller.scrollWidth > scroller.clientWidth + 1 || document.documentElement.scrollWidth > window.innerWidth + 1) over.push(s.id || 'hero');
    if (s.matches('article.topic') && scroller.scrollHeight > scroller.clientHeight + 1) tall.push(s.id);
  }
  location.hash = '';
  await wait(150);
  return { over, tall };
}
```

## 반 화면(720×900, 수업 중 쓰는 크기)
`resize_window`(`width: 720`, `height: 900`) → 새로고침 → `clientWidth > 0` 확인 → `mcp__Claude_Browser__javascript_tool`:
```js
await new Promise((r) => setTimeout(r, 1500));
const textNodes = Array.from(document.querySelectorAll('main *, #panel-right *')).filter((e) => !['SCRIPT', 'STYLE'].includes(e.tagName) && !e.closest('[hidden]'));
({
  brand: document.querySelector('.brand').textContent,
  katexErrors: document.querySelectorAll('.katex-error').length,
  rawDollar: textNodes.some((e) => Array.from(e.childNodes).some((n) => n.nodeType === 3 && n.textContent.includes('$'))),
  sumsInPanel: document.querySelectorAll('#panel-right .sum').length,
  sumsLeftInMain: document.querySelectorAll('main .sum').length,
  widgets: document.querySelectorAll('.widget').length,
  ...(await measureScreens()),
})
```
통과: `brand: "예습노트"`, `katexErrors: 0`, `rawDollar: false`, `sumsInPanel`이 manifest에서 `layers`가 빈 목록이 아닌 토픽 수, `sumsLeftInMain: 0`, `widgets: 0`, `over: []`, `tall: []`. `tall`에 나온 토픽은 작성자에게 "720×900 한 화면에 들어가게 줄여 주세요"로 되돌린다. `read_console_messages`에 오류가 없어야 한다.

개념 토픽 하나로 넘겨(`location.hash = '#<토픽 id>'`) 스크린샷을 찍고, 슬라이드 태그와 "들을 때 포인트" 박스가 보이는지 확인한다.

## 모바일·다크
`resize_window`(`preset: "mobile"`, `colorScheme: "dark"`) → 새로고침 → `clientWidth > 0` 확인 → 위 스크립트 재실행(`over: []`만 통과 조건, 모바일의 `tall`은 참고만) → 스크린샷으로 그림 글자가 보이는지 확인 → `#theme-toggle`을 눌러 배경색과 `aria-label`이 바뀌는지 확인한 뒤 `localStorage.removeItem('od-theme')`.

## 마무리
`resize_window`(`preset: "desktop"`, `colorScheme: "light"`)로 되돌리고 서버를 종료한다.
