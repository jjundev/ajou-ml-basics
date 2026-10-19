# 장면 작성 계약 (`assets/template.dc.html`)

주제 하나는 템플릿을 복사한 `Main.dc.html` 한 파일이에요. 바꾸는 곳은 다음 위치뿐이에요.

1. 자리표시 `__TITLE__`(`<title>`과 `.brand`, 2곳)
2. 마크업 슬롯 `<!-- SLOT:left -->` … `<!-- /SLOT:left -->`, `<!-- SLOT:right -->` … `<!-- /SLOT:right -->` 사이(예시 내용은 지우고 새로 써요)
3. 스크립트 맨 위 주제 훅: `topic()`, `buildScene()`, `extraState()`, `extraVals()`, `compute(state)`
4. 그 밖의 셸(상단 바, 패널, 본문 헤더·수식 노트, 캔버스, 재생 바, 접힌 주의사항, 공통 메서드)은 고치지 않아요. 고쳐야 하면 템플릿을 고치고 테스트를 돌려요.

다 쓰면 `node scripts/check.cjs <Main.dc.html>`이 `ok`를 내야 해요. 오류 줄은 `코드:대상 — 예외 문장` 모양이에요.

| 코드 | 뜻 |
|---|---|
| `SHELL_MISSING` | 셸 마크업 조각이 없어졌어요 |
| `HOLE_SYNTAX` | 런타임이 못 읽는 구멍(`{{!x}}`, `{{a ? b : c}}`, `onClick="x{{f}}"`) |
| `HOLE_UNKNOWN` | 없는 값(`{{is.cycle}}`처럼 모드 이름을 바꾼 뒤 남은 것, `{{s.titel}}` 같은 오타) |
| `EVENT_UNSUPPORTED` / `HEX_IN_MARKUP` | 아래 마크업 규칙 위반 |
| `TOPIC_INVALID` | `topic()` 데이터 누락·불일치: 모드 필드(`cam`, `fit`, `D`, `canvasLabel`), `STEPS[n].mode`가 없는 모드, `STEPS[n].f`가 재생 범위 밖, `f`가 있는 `STEPS[n].phase` 빠짐, 모드별 `MISTAKES`, `PAL.light`/`PAL.dark` (단계 번호는 `STEPS` 전체 순서로 1부터) |
| `STEP_OFF_PHASE` | 단계의 `f`에서 재생 바 글자(`playback.label(f)`)의 과정 이름이 `phase`와 다름(다음 과정에 들어가 있음), 또는 `label`이 예외 |
| `RENDER_THROWS` | `renderVals()`가 예외 |
| `DRAW_THROWS` | 장면 그리기 예외(모드별 `:a`, 단계 누른 뒤 `:step2`) |
| `SCENE_EMPTY` / `SCENE_NAN` | 그린 것이 없음 / 좌표가 숫자가 아님(예: `cam.zoom` 빠짐) |
| `TEMPLATE_LEFT` | `__TITLE__`, `DEMO`가 남음 |

## `topic()`

```js
topic() {
  return {
    MODES: [Mode, ...],          // 1–3개. 첫 번째가 처음 화면. 2개 이상이면 상단 바에 모드 버튼이 생겨요
    STEPS: [Step, ...],          // 선택. 현재 모드의 단계만 왼쪽 「단계」 목록에 보여요(없으면 칸이 숨겨져요)
    MISTAKES: { a: [{ title, text }, ...], ... },   // 모드 key별 「꼭 기억해요」 3개
    TOGGLES: { a: [['labels', '이름표'], ...] },    // 선택. 모드 key별(또는 모든 모드 공통 배열) 보기 옵션
    PAL: { light: {...}, dark: {...} }               // 캔버스 색
  };
}
```

- `DEMO: true`는 템플릿 예시 표시예요. 실제 주제에서는 지워요(남으면 `TEMPLATE_LEFT:DEMO`).
- `TOGGLES`의 첫 값은 상태 키예요. 초기값을 `extraState()`에 넣어요. 자동 회전(`spin`)은 `autoSpin` 모드에 셸이 알아서 붙여요.

### Mode

| 키 | 뜻 |
|---|---|
| `key` | 짧은 영문 키(`'a'`, `'cycle'` 등). 마크업에서 `{{is.<key>}}`로 그 모드인지 알 수 있어요 |
| `label` | 상단 버튼 글자(2–4자, 예: 「구조」 「과정」) |
| `cam` | `{ yaw, pitch, zoom }` 처음 시점. 평면 장면은 `{ yaw: 0, pitch: 0, zoom: 1 }` |
| `fit` | `[w, h]` 장면 단위로 화면에 담을 너비·높이. 화면 크기 = `min(W / w, H / h)` |
| `D` | 원근 거리. 작을수록 원근이 세요(구조 30, 넓은 과정 60 정도) |
| `autoSpin` | 처음에 천천히 돌지(동작 줄이기 설정이면 꺼져요) |
| `rotatable` | 끌어서 돌릴 수 있는지. 평면 도식은 `false` |
| `playback` | `null` 또는 `{ fmax, rate, label(f) }`. 재생 바가 생기고 `f`가 0→`fmax`로 초당 `rate × 속도`만큼 늘어요. `label(f)`는 스크럽 위 글자로, `'<과정 이름> · ' + f.toFixed(1) + ' / ' + fmax` 모양으로 써요 |
| `canvasLabel(f)` | 캔버스의 `aria-label`. 지금 화면을 한 문장으로 |

### 본문 유형과 제목

Mode의 선택 필드: `view:'graph'|'formula'`(생략하면 graph), `title`(생략하면 label). 공통 헤더가 제목과 도구를 같은 행에 배치한다. 주제 슬롯에서 헤더를 다시 만들거나 기존 버튼을 복제·이동하지 않는다.

수식형은 `playback:null`, `autoSpin:false`, `rotatable:false`로 지정한다. `cam`, `fit`, `D`, `canvasLabel`은 기존 모드 계약대로 제공하되 buildScene은 이 모드에서 아무것도 그리지 않아도 된다. checker는 수식형에만 빈 캔버스를 허용하고 단계 데이터를 별도로 검사한다.

수식형의 STEPS는 같은 mode의 순서대로 최소 한 개가 필요하다. 각 단계는 기존 `mode,c,title,text`에 `tex` 하나 또는 `left,right` 한 쌍 중 하나를 추가한다. 비어 있는 식은 허용하지 않는다. `text`는 현재 줄의 이유다. `who`는 생략 가능하다. `preset`도 기존과 같이 지원한다.

```js
// Mode 예시
{key:'mean',label:'평균',title:'MAP과 사후평균',view:'formula',
 cam:{yaw:0,pitch:0,zoom:1},fit:[14,14],D:60,
 autoSpin:false,rotatable:false,playback:null,
 canvasLabel:()=> 'MAP과 사후평균의 등식 전개'}
// STEPS 예시 (String.raw로 TeX 역슬래시를 보존)
{mode:'mean',c:'#1677ff',title:'공통 인수 묶기',
 tex:String.raw`(cA)^{-1}=c^{-1}A^{-1}`,text:'스칼라의 역수를 밖으로 꺼내요.'}
// 비교식은 tex 대신 left/right와 선택적인 열 이름을 사용
{mode:'mean',c:'#1677ff',title:'두 식 비교',
 left:String.raw`S_0^{-1}`,right:String.raw`(b^2I)^{-1}`,
 leftLabel:'일반 사전분포',rightLabel:'단순 사전분포',text:'오른쪽은 왼쪽의 특수한 경우예요.'}
```

공통 셸이 로컬 KaTeX로 렌더링하므로 ref 훅이나 DOM 삽입을 추가하지 않는다. 첫 식은 자동으로 표시되고 이전/다음·좌우 키·단계 목록은 동일한 STEPS 인덱스를 사용한다. 수식형에서는 왼쪽 단계의 부연 설명을 중복 표시하지 않는다. 배율 초기화와 처음부터 다시 시작하는 동작은 다르다. 전체 초기화가 필요한 주제는 슬롯에서 입력과 모드를 함께 초기화하는 버튼을 제공한다.

### Step

`{ mode, f?, phase?, c, title, who, text }` — 누르면 그 `mode`로 바꾸고, `f`가 있으면 그 진행값으로 옮기고 재생을 멈춰요. `c`는 번호 테두리 색, `who`는 행위자(변수와 설정 등), `text`는 아래 상세 칸 문장.

`f`가 있으면 `phase`도 써요. 그 `f`에서 재생 바 글자(`playback.label(f)`)에서 ` · `로 나뉜 과정 이름 하나와 똑같이 써요(예: `두 번째 입력 · 갱신 · 3.0 / 16`이면 `갱신`). 이름 일부만 쓰면 다음 과정과 구별되지 않아요. 단계는 그 과정이 화면에 다 보이는 지점에 둬요(다음 과정의 시작점에 두지 않아요).

목록에는 현재 모드의 단계만 `STEPS` 순서대로 나오고, 번호는 모드 안에서 1부터 세요. 검사 오류의 단계 번호는 `STEPS` 전체 순서예요.

### PAL

`light`·`dark` 둘 다 필요해요. 셸이 쓰는 키: `bg`(캔버스 배경, 테마 `bg`와 같게), `labelBg`(라벨 칩 배경), `ink`(라벨 글자), `ring`(고리 표시), `blobAlpha`(반투명 구 진하기, 기본 0.3). 나머지 키는 장면 색으로 자유롭게 써요. 다크 색은 같은 색상의 밝은 쪽으로 맞춰요.

## `buildScene(mode, I, O)`

매 프레임 불려요. 배열에 push만 하고 그리지는 않아요. 진행값은 `this.sim.f`(매끄러운 값), 토글은 `this.state.<키>`, 색은 `this.pal()`.

좌표는 `[x, y, z]` 장면 단위, 원점이 화면 가운데, y가 위쪽이에요. 카메라 중심은 원점에 고정이라 장면을 원점 둘레에 놓아요. 깊이 안개는 앞뒤 차이가 있을 때만 생겨요(평면 장면은 그대로 진하게).

| `k` | 모양 | 필드 |
|---|---|---|
| `0` | 빛 받은 구 | `p, r, c`, `flat?`(납작한 원), `a?`(투명도 0–1) |
| `1` | 막대·선 | `p, q, w, c`, `rod?`(어두운 테두리로 입체 막대), `flat?`(끝 각지게), `a?` |
| `3` | 글자 | `p, text, size, c` (`size`는 장면 단위, 화면에서 8–14px로 잘려요) |
| `4` | 화살촉 | `p, q, c` — `p→q` 가운데에 `q` 쪽을 향한 삼각형 |
| `5` | 반투명 음영 구 | `p, r, c`, `focus?`(테두리 굵게) — 추상 기하 도형 |

`O`(라벨, 항상 맨 위에 그려져요):
- 칩: `{ p, text, c, size?, dx?, dy?, lead?, a? }` — `dx/dy` 픽셀만큼 옮기고 `lead`면 `p`까지 선을 그어요. 겹치지 않게 평면 기준으로 고정 오프셋을 줘요.
- 고리: `{ t: 'ring', p, text }` — 깜박이는 원과 아래 글자(닉, 결합 자리 표시 등).

도우미: `this.lerp(a, b, t)`, `this.sm(x)`(0–1 부드러운 계단), `this.mix(hex, to, amt)`, `this.rgba(hex, a)`, `this.textTone(hex)`(라이트에서 글자용으로 어둡게).

## `extraState()` / `extraVals(st)`

- `extraState()` → 초기 상태에 합쳐요(토글 키, 주제 전용 선택값).
- `extraVals(st)` → `renderVals()` 결과에 합쳐요. 슬롯 마크업의 `{{…}}`은 공통 키나 여기 키만 쓸 수 있어요(아니면 `HOLE_UNKNOWN`).

## 공통 상태와 마크업 값

상태: `formulaScale, mode, f, playing, speed, step, spin, theme, leftOpen, rightOpen, drawer, narrow, leftW, rightW, resizing` (+ `extraState()`). `step`은 `STEPS` 전체 인덱스(없으면 -1)예요.

메서드: `setMode(key)`는 모드를 바꾸고 `f`·고른 단계를 지우고 수식 배율을 1로 돌려요. `pickStep(i)`는 `STEPS[i]`(전체 인덱스)를 골라요. 필요하면 모드를 바꾸고 `f`로 옮겨요.

`renderVals()` 공통 키: `th, isDark, isLight, themeLabel, toggleTheme, canvasRef, canvasCls, hasModes, is, modes[{label, pressed, pick}], leftCls, rightCls, leftExpanded, rightExpanded, scrimCls, toggleLeft, toggleRight, closePanels, layoutStyle, layoutCls, leftWNow, rightWNow, leftHandleRef, rightHandleRef, onKey, hasToggles, toggles[{label, pressed, toggle}], hasSteps, steps[{num, title, who, c, pressed, pick}], hasStep, stepDetail, mistakes, canvasLabel, zoomIn, zoomOut, resetView, hasPlayback, isPlaying, notPlaying, playLabel, togglePlay, fInt, fLabel, fMax10, onScrub, speeds[{label, pressed, pick}]`

## 마크업 규칙

- 런타임이 아는 것만: `{{점.경로}}` 구멍, `onClick`·`onKeyDown`·`onMouseEnter`·`onMouseLeave`·`onChange`, `ref`, `<sc-if value>`, `<sc-for list as>`. 그 밖의 이벤트는 동작하지 않아요(`EVENT_UNSUPPORTED`).
- `<sc-if>` 안에는 요소 하나로 감싸서 넣어요.
- 마크업에 `#rrggbb`를 직접 쓰지 않아요. 색은 CSS 토큰(`var(--ink-2)` 등)이나 `{{legend.x}}` 같은 구멍으로만(`HEX_IN_MARKUP`).
- 쓸 수 있는 공통 클래스: `.fold`(접힌 보충 설명), `.sec`, `.sec-title`, `.sub`, `.opt`, `.btn`, `.tiles`(`.three`), `.tile`, `.events`, `.event`, `.dot`, `.legend`, `.sw`(`.ball`), `.detail`, `.num`, `.float`, `.hover-card`.


## ML 계산·preset·polygon

compute(state)는 그래프와 패널의 동일한 순수 계산 결과를 반환한다. K=2 예시는 MLMath API를 사용한다. 자세한 입력은 math-validation.md를 읽는다.
Step에는 preset 객체를 추가할 수 있다. mode를 바꾼 뒤 입력을 합치고 재생을 멈춘다. topic.PRESETS는 checker가 compute→renderVals→draw로 전체 검사하는 상태 목록이다. 비유한 결과는 RESULT_NAN, 예외는 INPUT_THROWS다.
k=6 채움 다각형: {k:6,p:pts[0],pts:[[x,y,z],...],c,a?}. 최소 3점, 길이3 finite 좌표만 허용한다. 띠는 upper+reversed(lower) 점으로 만들고 같은 변환의 k=1 선으로 테두리를 그린다.
숫자 입력은 onChange를 쓴다(런타임의 input 이벤트). 유효 범위와 finite를 검사하고 빈 값은 마지막 상태로 복원한다. 정적 공식은 ref callback으로 로컬 window.katex.render를 한 번 호출한다.

수식형 공통 값: `isFormula, stageTitle, stageBodyCls, formulaScale, formulaRows, formulaProgress, formulaPrevDisabled, formulaNextDisabled, formulaPrev, formulaNext, formulaRootRef, formulaNavRef, onFormulaKey, resetViewLabel`. 일반 주제 저작 시 직접 재정의하지 않는다. `formulaRows`는 현재 모드에서 선택한 단계까지의 목록이다. 그래프형의 기존 주제 훅은 그대로 사용할 수 있다.
