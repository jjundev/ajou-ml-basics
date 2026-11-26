# 브라우저 검증 (메인 에이전트)

## 서버
file:// 미리보기에서는 스크립트가 돌지 않는다. 빈 포트로 서버를 띄운다. 셸 상태는 Bash 호출 사이에 이어지지 않으므로 포트 번호를 먼저 출력해 두고, 이후 명령과 URL에는 그 숫자를 직접 쓴다.
1. 빈 포트 찾기(출력된 숫자가 `<port>`):
   ```bash
   uv run python -c "import random,socket; p=random.randrange(20000,60000); socket.socket().bind(('127.0.0.1',p)); print(p)"
   ```
2. 서버 띄우기: Bash 도구의 `run_in_background: true`로 실행한다(명령 끝에 `&`를 붙이지 않는다).
   ```bash
   uv run python -m http.server <port> --directory "<RUN>/work/stage"
   ```
3. URL: `http://localhost:<port>/복습노트/<range>/<파일명>` (한글 그대로).
4. 끝나면 서버를 종료한다: 그 백그라운드 작업을 멈추거나(TaskStop 등), `pkill -f "http.server <port>"`.

## 측정 전 준비
브라우저 창이 숨겨져 있으면 `document.documentElement.clientWidth`가 0이 되어 `hScroll`이 거짓 양성으로 나온다. 측정 전에 `resize_window`로 크기를 명시하고(`width: 1280`, `height: 900`) `document.documentElement.clientWidth > 0`을 확인한다. `.katex-mathml` 안 요소는 화면에 보이지 않으므로 넘침 원인으로 치지 않는다. 스크롤 직후 스크린샷은 늦게 반영될 수 있으니 1초쯤 기다린 뒤 찍는다.

## 가로 넘침 측정 (두 페이지 공통)
템플릿은 `body`를 고정하고 본문을 `.content` 안에서 스크롤하며, 한 번에 한 화면(토픽·카드)만 보여 준다. 그래서 `document.documentElement.scrollWidth`로는 넘침이 잡히지 않는다. 아래 `overflowScreens`로 화면을 하나씩 넘기며 `.content`를 잰다. 결과는 넘친 화면 id 목록이고, 비어 있어야 통과다. 목록이 나오면 그 화면에서 `.content`의 오른쪽 끝을 넘는 요소를 찾아 원인을 확인한다(`.katex-display`·`.table-wrap` 안의 자체 가로 스크롤은 넘침이 아니다).
```js
async function overflowScreens() {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const scroller = document.querySelector('.content') || document.documentElement;
  const screens = Array.from(document.querySelectorAll('main .screen'));
  const over = [];
  for (const s of screens.length ? screens : [document.querySelector('main')]) {
    if (screens.length) { location.hash = s.id ? '#' + s.id : ''; await wait(150); }
    // 넘어올 때의 translateX(24px) 애니메이션이 넘침으로 잡히지 않게 끝낸다(숨은 창에서는 애니메이션이 멈춰 있다)
    document.getAnimations().forEach((a) => a.finish());
    if (scroller.scrollWidth > scroller.clientWidth + 1 || document.documentElement.scrollWidth > window.innerWidth + 1) over.push(s.id || 'hero');
  }
  location.hash = '';
  await wait(150);
  return over;
}
```

## 정리노트 (`mcp__Claude_Browser__javascript_tool`)
위 `overflowScreens` 정의를 같은 실행에 붙여 넣는다.
```js
await new Promise((r) => setTimeout(r, 1500));
const textNodes = Array.from(document.querySelectorAll('main *, #panel-right *')).filter((e) => !['SCRIPT', 'STYLE'].includes(e.tagName) && !e.closest('[hidden]'));
({
  katex: document.querySelectorAll('.katex').length,
  katexErrors: document.querySelectorAll('.katex-error').length,
  rawDollar: textNodes.some((e) => Array.from(e.childNodes).some((n) => n.nodeType === 3 && n.textContent.includes('$'))),
  sumsInPanel: document.querySelectorAll('#panel-right .sum').length,
  sumsLeftInMain: document.querySelectorAll('main .sum').length,
  hScroll: await overflowScreens(),
  widgets: Array.from(document.querySelectorAll('.widget')).map((w) => ({ id: w.id, drawn: Array.from(w.querySelectorAll('svg')).some((s) => !s.closest('[hidden]') && s.childElementCount > 0) })),
})
```
통과: `katexErrors: 0`, `rawDollar: false`, `sumsInPanel`이 manifest에서 `layers`가 빈 목록이 아닌 토픽 수, `sumsLeftInMain: 0`, `hScroll: []`, 모든 위젯 `drawn: true`. `read_console_messages`에 오류 없음.

개념 토픽 하나로 넘겨(`location.hash = '#<토픽 id>'`) 오른쪽 "페이지 요약" 패널에 그 토픽의 요약이 보이는지 스크린샷으로 확인한다(1280px 이상에서는 패널이 기본으로 열린다).

위젯마다 해당 토픽으로 이동해 실제 조작으로 대표 설정들을 비교한다. 입력 중 조작값만 바뀌고 고정할 데이터·대상이 유지되는지, 표시값이 `.widget-static` 표의 같은 설정과 일치하는지 확인한다. 최댓값이나 역전이 학습 포인트라면 경계와 인접 설정을 비교해 반올림이 의미 있는 차이를 가리지 않는지도 확인한다.

## 모바일·다크
`resize_window`(`preset: "mobile"`, `colorScheme: "dark"`) → 새로고침 → `clientWidth > 0` 확인 → 위 스크립트 재실행(`hScroll: []`) → 스크린샷으로 그림·위젯 글자가 보이는지 확인 → 상단 바의 테마 버튼(`#theme-toggle`)을 눌러 `document.body` 배경색이 바뀌고 `aria-label`이 반대 모드로 바뀌는지 확인한 뒤 `localStorage.removeItem('od-theme')`로 지운다 → `preset: "desktop"`, `colorScheme: "light"`로 되돌린다.

## 복습문제
측정 전에 다시 `resize_window`(`width: 1280`, `height: 900`) → `clientWidth > 0` 확인(앞 단계의 `preset: "desktop"`은 창 크기를 창 자체 크기로 되돌려 숨은 창에서는 0이 될 수 있다). 이번에도 `overflowScreens` 정의를 붙여 넣는다.
```js
await new Promise((r) => setTimeout(r, 1500));
document.querySelectorAll('details').forEach((d) => { d.open = true; });
await new Promise((r) => setTimeout(r, 300));
({
  cards: document.querySelectorAll('article.card').length,
  aidGroups: document.querySelectorAll('#panel-right .aid').length,
  katexErrors: document.querySelectorAll('.katex-error').length,
  hScroll: await overflowScreens(),
})
```
통과: `cards`와 `aidGroups`가 모두 manifest 문제 수, `katexErrors: 0`, `hScroll: []`. 첫 카드로 넘겨 오른쪽 "풀이 도움" 패널에 그 카드의 원문·힌트·풀이가 보이는지, 상단 "정리노트" 링크가 노트로 이동하는지 확인한다.

## 마무리
모든 검사가 끝나면 `resize_window`(`preset: "desktop"`, `colorScheme: "light"`)로 되돌리고 서버를 종료한다(위 "서버" 4).

## PDF 연결
서버는 최종 배포 전에 RUN/work/stage 루트를 서비스한다. 브라우저 URL은 /복습노트/<range>/<정리노트 또는 복습문제>.html이며 검사기와 동일한 상대 구조를 쓴다. PDF 둘을 열고 모든 페이지를 PNG로 검사한다. 검색 가능한 한국어, A4 가로, 표/그래프/수식/필기 공간/Hint와 계속 페이지의 조건 및 마지막 답을 확인한다. HTML의 PDF 링크가 둘 다 정확한 파일을 여는지 확인한다. 실패 시 공개 폴더를 유지한다.

## 패널 동작 회귀

임시 stage의 실제 생성 결과를 빈 로컬 HTTP 포트로 제공하여 1280×900 / 375×812, light / dark에서 확인한다. 서로 다른 두 토픽을 이동하면 중앙 h3는 보이고 우측에는 같은 제목이 없어야 한다. `#sum-for.sums`는 하나이며 현재 `.sum:not([hidden])`만 정확한 요약을 표시한다. 표지에는 기존 안내, 문제 카드에는 힌트·풀이와 푼 문제 토글을 확인한다. 문제설명은 문제·원문 탭, 이전/다음, 수식 제목과 긴 수식도 확인한다. 이동·새로고침 전후 read/solved의 실제 키와 ID 배열 payload를 비교하고 콘솔·KaTeX 오류가 0인지 확인한다. 기존 missing-sum 검사가 여전히 누락을 잡아야 한다. 서버·브라우저는 finally에서 종료한다. 고정 PDF 템플릿·인쇄 CSS는 변경하지 않는다.
