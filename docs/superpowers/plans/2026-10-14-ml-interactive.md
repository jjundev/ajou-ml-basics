# ml-interactive 및 1014 자료 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** ml-interactive 스킬을 만들고 1014 베이지안 선형회귀 실험 두 개를 검증·저장하여 기존 정리노트에 연결한다.

**Architecture:** 생명과학 bio-interactive의 공통 셸과 CLI를 독립 복사하여 ML용 경로·계산·그래프·연결 계약을 추가한다. 교육용 K=2 베이지안 선형회귀 계산은 브라우저와 Node에서 같은 순수 모듈을 쓰고, 정답은 Python Fraction으로 독립 검산한다. 기존 노트 수정은 문맥별 링크만 허용하며 재생성한 노트에는 저장된 상대 경로 명세로 연결을 복원한다.

**Tech Stack:** Node.js 20+, CommonJS/node:test, 기존 x-dc 런타임, Canvas 2D, Python 표준 라이브러리, 기존 로컬 KaTeX 0.16.11/Pretendard 1.3.9.

**Spec:** `C:/Users/Hyunjun/Desktop/현준대학/26-2/ajou-ml-basics/docs/superpowers/specs/2026-10-14-ml-interactive-design.md`

## Global Constraints

- Node.js 20 이상; CommonJS 도구와 Node 내장 test runner를 사용한다.
- 새 웹 프레임워크·차트 라이브러리·npm 설치 없이 기존 Canvas 2D 및 x-dc 런타임을 활용한다.
- KaTeX 0.16.11·Pretendard 1.3.9는 기존 `ml-problem-explain/assets/vendor`의 라이선스·provenance와 함께 복사하여 사용한다.
- HTML은 날짜 폴더, 나머지는 `.pack/`에 저장한다. 기존 날짜의 구형 MD 위치도 읽는다.
- NFC/NFD를 비교하되 반환·쓰기 경로는 실제 파일명을 사용한다.
- 기존 자료 번호를 덮어쓰지 않는다. 실패한 저장·노트 쓰기는 기존 파일을 보존한다.
- 정리노트의 본문·위젯·스타일·스크립트 및 기존 MD·문제·PDF를 변경하지 않는다. 관련 설명 뒤 안내·링크 추가와 기존 링크 새 탭 속성 보정만 허용한다.
- 안내는 실제 조작 기능과 일치하는 자연스러운 해요체 문장이다. 링크는 상대 경로와 `target="_blank" rel="noopener noreferrer"`를 사용한다.
- 같은 절의 같은 목적지는 재실행해도 중복하지 않는다. 다른 절·페이지 끝 링크는 해당 절의 안내를 대신하지 않는다.
- 정확한 수식·강의 범위는 1014 정리노트·STT·Lecture04 rev HO·MML로 확인한다. 학습용 데이터와 시각화 단순화는 표시한다.
- 1440×900 및 375×812, 라이트·다크, 키보드·패널·조작·수식·콘솔·새 탭 동작을 검사한다.
- 자동 커밋·외부 게시·전체 날짜 일괄 생성·1014 구형 팩 전체 이전은 이번 범위에서 제외한다.

## Review Focus

1. 1014 구형 MD와 다른 날짜의 .pack MD, NFC/NFD가 섞인 이름을 모두 실제 경로로 찾아야 한다 — Task 1 resolver fixture.
2. 데이터 0개, 상관 공분산, 잘못된 분산·입력에서는 계산을 정확히 수행하거나 명시적 RangeError로 거절해야 한다 — Task 2 독립 정답 및 입력 검사.
3. 모바일·다크·모드 전환·preset 단계에서 그래프와 패널이 같은 입력을 표시해야 한다 — Task 3 component 검사 및 Task 5 브라우저 matrix.
4. 번호 충돌·저장 실패·노트 쓰기 실패는 기존 자료와 노트를 보존해야 한다 — Task 1 저장 충돌 및 Task 4 쓰기 실패 fixture.
5. 노트 재생성·저장소 위치 이동·절 ID 변경은 중복 없이 복원하거나 구체적 skipped를 보고해야 한다 — Task 4 relink fixture 및 Task 6 최종 보존 검증.

---

## 작업 위치와 파일 지도

이 문서의 파일 표는 아래 절대 경로 별칭을 확장한 경로다. 실제 셸 호출은 절대 경로를 넘긴다. 실행 시작 때 using-git-worktrees로 작업 위치를 결정하고 REPO만 새 위치로 바꾼다. 사용자 미추적 파일 두 개는 편집·추가·커밋하지 않는다.

```powershell
$repoRoot = 'C:\Users\Hyunjun\Desktop\현준대학\26-2\ajou-ml-basics'
$bioRoot = 'C:\Users\Hyunjun\Desktop\현준대학\26-2\생명과학\.agents\skills\bio-interactive'
$skillRoot = Join-Path $repoRoot '.agents\skills\ml-interactive'
$packRoot = Join-Path $repoRoot '복습노트\1014'
$notePath = Join-Path $packRoot '정리노트_1014_Bayesian_Posterior_Prediction.html'
$runRoot = Join-Path ([IO.Path]::GetTempPath()) ('ml-interactive-' + [guid]::NewGuid().ToString('N'))
```

| 위치 | 책임 |
|---|---|
| SKILL/SKILL.md | 자동·명시 호출, 생성 및 연결 전용 흐름, 완료·보류 보고 |
| SKILL/agents/openai.yaml | Codex 표시명·설명·기본 프롬프트, 자동 발견 유지 |
| SKILL/assets/template.dc.html, dc-runtime.js | 공통 패널·테마·모바일·모드·preset 단계·그리기 |
| SKILL/assets/ml-math.js | K=2 사후·예측·밀도·seed 고정 표본 순수 계산 |
| SKILL/assets/vendor/ | 기존 로컬 수식·폰트·라이선스·provenance 자산 |
| SKILL/scripts/resolve.cjs | 날짜·주제·원본 위치·다음 번호 판단 |
| SKILL/scripts/build.cjs, save.cjs | HTML 빌드, 공통 자산 준비, 번호 충돌·실패 보존 |
| SKILL/scripts/harness.cjs, check.cjs, steps.cjs | component·입력 preset·장면·단계 검사 |
| SKILL/scripts/link-notes.cjs, relink.cjs | 문맥별 링크 삽입·속성 보정·상대 명세 재연결 |
| SKILL/references/ | scene-api.md, design.md, topic-selection.md, math-validation.md, note-links.md |
| SKILL/tests/ | 이식된 behavioral tests와 새 경로·수학·장면·연결 테스트 |
| REPO/.claude/skills/ml-interactive | .agents 원본으로의 상대 심볼릭 링크 |
| REPO/.claude/skills/ml-review-pack/SKILL.md, references/interactive-links.md | 발행 후 기존 인터랙티브 재연결 지침 |
| REPO/README.md | 스킬 호출·저장·연결 사용법 |
| PACK/인터렉티브_01_사전분포와_사후분포.html | 사후·회귀 실험 공개 HTML |
| PACK/인터렉티브_02_함수와_관측값의_예측분포.html | 예측 띠·밀도 실험 공개 HTML |
| PACK/.pack/자료_인터렉티브_NN_이름/ | Main.dc.html, canvas.json, brief.md, note-links.json, evidence/ |
| PACK/.pack/vendor/ml-interactive/ | 두 자료가 공유하는 수식·폰트 자산 |

01·02는 현재 신규 번호의 예상값이다. 실제 번호와 최종 경로는 save.cjs 결과를 사용한다.

## Task 1: 독립 스킬 골격과 ML 대상·저장 호환성

**Files:**
- Create: SKILL/SKILL.md, scripts/resolve.cjs, scripts/save.cjs, scripts/build.cjs, scripts/harness.cjs, scripts/check.cjs, scripts/steps.cjs, scripts/link-notes.cjs.
- Create: SKILL/assets/template.dc.html, assets/dc-runtime.js 및 BIO의 behavioral tests 복사본.
- Create: SKILL/tests/ml-resolve.test.cjs, tests/ml-save.test.cjs.
- Create: REPO/.claude/skills/ml-interactive 심볼릭 링크.

**Interfaces:**
- Consumes: BIO의 실제 파일, 생명과학 baseline commit `35d47326830928444004fff3cb197a5991c075ae`, ML 폴더 구조.
- Produces: `resolve({repo,arg}) -> {kind,folder,exists,date,notes,noteHtml,stt,existing,next}`; `nextNumber(folder)->string`; `save({src,dest,name})->{nn,html,dir}`. `NO_ARG/NO_TARGET/AMBIGUOUS_TARGET`는 `{error:code}` 및 exit 1.

- [ ] **Step 1: 복사본과 테스트 파일을 준비한다.** 원본 commit을 확인한 뒤 기존 동작을 독립 복사한다. `references/example-dna.dc.html`은 장면 품질 조사에만 사용하고 ML 스킬에 DNA 예시를 배포하지 않는다.

```powershell
git -C (Split-Path (Split-Path (Split-Path $bioRoot))) rev-parse HEAD
New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null
foreach ($name in @('scripts','assets','tests')) {
    Copy-Item -LiteralPath (Join-Path $bioRoot $name) -Destination (Join-Path $skillRoot $name) -Recurse
}
New-Item -ItemType Directory -Path (Join-Path $skillRoot 'references') -Force | Out-Null
foreach ($name in @('design.md','scene-api.md','topic-selection.md','note-links.md')) {
    Copy-Item -LiteralPath (Join-Path $bioRoot ('references\' + $name)) -Destination (Join-Path $skillRoot ('references\' + $name))
}
Copy-Item -LiteralPath (Join-Path $bioRoot 'SKILL.md') -Destination (Join-Path $skillRoot 'SKILL.md')
```

호환성 테스트는 다음 실제 임시 파일을 만든다. 새 테스트 파일 상단에는 `test=require('node:test')`, `assert=require('node:assert/strict')`, `fs=require('node:fs')`, `os=require('node:os')`, `path=require('node:path')`, `{resolve,nextNumber}=require('../scripts/resolve.cjs')`를 선언한다. t.after에서 해당 임시 폴더만 정리한다.

```js
test('reads legacy 1014 MD and returns actual NFD paths', t => {
  const repo = fs.mkdtempSync(path.join(os.tmpdir(), 'ml-resolve-'));
  t.after(() => fs.rmSync(repo, {recursive:true, force:true}));
  const folder = path.join(repo, '복습노트', '1014');
  fs.mkdirSync(folder, {recursive:true});
  const md = path.join(folder, '정리노트_1014_A.md'.normalize('NFD'));
  const html = path.join(folder, '정리노트_1014_A.html'.normalize('NFD'));
  fs.writeFileSync(md, '## 사후분포\n데이터를 본 뒤의 분포');
  fs.writeFileSync(html, '<article id="posterior">사후분포</article>');
  const got = resolve({repo,arg:'1014'});
  assert.deepEqual(got.notes,[md]);
  assert.deepEqual(got.noteHtml,[html]);
  assert.equal(resolve({repo,arg:'사후분포'}).folder,folder);
});
test('canonical MD wins over the same legacy name', t => {
  const repo = fs.mkdtempSync(path.join(os.tmpdir(), 'ml-resolve-'));
  t.after(() => fs.rmSync(repo, {recursive:true, force:true}));
  const folder = path.join(repo,'복습노트','1012');
  fs.mkdirSync(path.join(folder,'.pack'),{recursive:true});
  fs.writeFileSync(path.join(folder,'정리노트_1012_A.md'),'old');
  const canonical = path.join(folder,'.pack','정리노트_1012_A.md');
  fs.writeFileSync(canonical,'## 가우시안 곱');
  assert.deepEqual(resolve({repo,arg:'1012'}).notes,[canonical]);
});
```

- [ ] **Step 2: 실패를 확인한다.**

```powershell
node --test (Join-Path $skillRoot 'tests\ml-resolve.test.cjs')
```

Expected: legacy MD test fails because BIO only reads `.assets/`.

- [ ] **Step 3: ML 경로를 구현한다.** `resolve.cjs`의 `notesIn`을 아래로 교체하고 STT 이름을 `머러기.md`로 바꾼다. 반환 경로는 normalize된 가짜 경로가 아니다.

```js
function notesIn(folder) {
  const byName = new Map();
  for (const dir of [folder, path.join(folder,'.pack')]) {
    for (const d of list(dir)) {
      if (d.isFile() && /^정리노트_.*\.md$/.test(nfc(d.name))) {
        byName.set(nfc(d.name),path.join(dir,d.name));
      }
    }
  }
  return [...byName.values()];
}
function sttFor(repo,date) {
  if (!date) return null;
  const dir = child(repo,'STT');
  const hit = dir && list(dir).find(d => d.isFile() &&
    new RegExp('^'+date+'[ _]머러기\\.md$').test(nfc(d.name)));
  return hit ? path.join(dir,hit.name) : null;
}
```

번호 검색의 `.assets`는 `.pack`으로 바꾸고 루트의 legacy 자료 폴더 검색은 유지한다. 정확한 날짜 폴더 없이 범위 폴더 두 개가 해당 날짜를 포함하면 `AMBIGUOUS_TARGET`으로 거절한다. BIO 테스트의 fixture 과목명·경로·빌드 주석을 ML에 맞춰 변경하고 생명과학 생성 후보·교과서 경로는 ML 규칙으로 다시 쓴다. 문자열·문서 형태만 검사하는 BIO의 skill.test.cjs는 이식 대상에서 제외하고 실제 resolve/save/build/link 동작 테스트를 유지한다. SKILL.md의 DNA 예시 참조도 제거하며 ML 그래프 계약은 Task3에서 추가한다.

이식한 기존 테스트의 `bio-interactive`와 `.assets/` fixture 경로는 ML 원본과 `.pack/`으로 바꾼다. 제거·수정은 새 SKILL 안에서만 한다. 원본 BIO는 읽기 전용이다.

```powershell
Remove-Item -LiteralPath (Join-Path $skillRoot 'tests\skill.test.cjs')
```

- [ ] **Step 4: 저장 충돌과 쓰기 실패 테스트를 먼저 추가한다.** 기존 save fixture의 Main.dc.html을 사용한다.

```js
test('reserves numbers from .pack sources without replacing an existing page', t => {
  const dest = fs.mkdtempSync(path.join(os.tmpdir(),'ml-save-'));
  t.after(()=>fs.rmSync(dest,{recursive:true,force:true}));
  fs.mkdirSync(path.join(dest,'.pack','자료_인터렉티브_01_기존'),{recursive:true});
  fs.writeFileSync(path.join(dest,'인터렉티브_02_기존.html'),'preserve');
  assert.equal(nextNumber(dest),'03');
  assert.equal(fs.readFileSync(path.join(dest,'인터렉티브_02_기존.html'),'utf8'),'preserve');
});
```

기존 `save.test.cjs` 실패 주입 패턴을 확장하여 생성 HTML 쓰기 실패 후 새 자료 폴더가 남지 않는지 검사한다. open 성공 뒤 write 실패와 open EEXIST를 구분하고 EEXIST의 기존 파일을 지우지 않는 테스트를 각각 둔다.

- [ ] **Step 5: 저장을 독점 생성·복구하도록 바꾼다.** 자료 폴더 mkdir는 nonrecursive 예약으로 유지한다. HTML에는 아래 소유권 패턴을 적용한다.

```js
let ownsHtml = false;
try {
  const fd = fs.openSync(html,'wx');
  ownsHtml = true;
  try { fs.writeFileSync(fd,build(copy,html)); }
  finally { fs.closeSync(fd); }
} catch (error) {
  if (ownsHtml) fs.unlinkSync(html);
  fs.rmSync(dir,{recursive:true,force:true});
  throw error;
}
```

기존 outer catch와 중복 삭제하지 않도록 새 예약 폴더·새 파일 cleanup을 한 곳에 둔다. source와 기존 vendor는 cleanup 대상이 아니다.

- [ ] **Step 6: 전체 이식 테스트와 스킬 발견을 확인한다.**

```powershell
$testPaths = @(Get-ChildItem -LiteralPath (Join-Path $skillRoot 'tests') -Filter '*.test.cjs' -File | Select-Object -ExpandProperty FullName)
node --test @testPaths
New-Item -ItemType SymbolicLink -Path (Join-Path $repoRoot '.claude\skills\ml-interactive') -Target '..\..\.agents\skills\ml-interactive'
Get-Item -LiteralPath (Join-Path $repoRoot '.claude\skills\ml-interactive') | Select-Object LinkType,Target
```

Expected: all tests pass; 두 경로의 SKILL.md가 같은 원본을 읽는다. 심볼릭 링크 생성이 불가능하면 복제본 두 개를 만들지 말고 원인과 원본 위치를 보고한다.

- [ ] **Step 7: 변경 묶음을 검토한다.** commit 제안: `feat(ml-interactive): add portable ML target and storage tools`. 사용자가 별도로 커밋을 요청한 경우에만 해당 작업의 파일을 명시적으로 stage한다.

## Task 2: K=2 순수 계산과 독립 수치 검증

**Files:** Create SKILL/assets/ml-math.js, SKILL/tests/math.test.cjs, SKILL/tests/fixtures/math-golden.json, SKILL/tests/independent_math.py.

**Interfaces:**
- Consumes: finite `xs/ys`, integer `n`, 2-vector `m0`, symmetric SPD 2×2 `S0`, positive `sigma2`.
- Produces: `MLMath.posterior(options)->{mean:number[2],cov:number[2][2],n:number}`; `predict(p,x,sigma2)->{mean,functionVariance,observationVariance}`; `normalPdf(x,mu,variance)->number`; `sampleWeights(p,seed,count)->number[2][]`. CommonJS export와 browser global `MLMath`는 같은 API다.

- [ ] **Step 1: 해석적으로 구한 정답의 테스트를 쓴다.**

```js
const test=require('node:test'), assert=require('node:assert/strict');
const M=require('../assets/ml-math.js');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-12,`${a} != ${b}`);
test('symmetric observations and prediction match rational answers',()=>{
  const p=M.posterior({xs:[-1,0,1],ys:[0,1,2],sigma2:1});
  near(p.mean[0],3/4); near(p.mean[1],2/3);
  near(p.cov[0][0],1/4); near(p.cov[1][1],1/3); near(p.cov[0][1],0);
  const q=M.predict(p,2,1);
  near(q.mean,25/12); near(q.functionVariance,19/12); near(q.observationVariance,31/12);
});
test('off-diagonal posterior is retained',()=>{
  const p=M.posterior({xs:[0,1],ys:[1,2],sigma2:1});
  near(p.mean[0],4/5); near(p.mean[1],3/5);
  near(p.cov[0][1],-1/5); near(p.cov[1][0],-1/5);
});
test('zero data preserves nonzero mean and correlated prior',()=>{
  const S0=[[2,.5],[.5,1]],m0=[1,-2];
  const p=M.posterior({xs:[-1,0,1],ys:[0,1,2],n:0,m0,S0,sigma2:1});
  assert.deepEqual(p.mean,m0); assert.deepEqual(p.cov,S0);
});
test('rejects invalid inputs rather than plotting NaN',()=>{
  for(const input of [
    {sigma2:0},{sigma2:-1},{sigma2:NaN},{n:-1},{n:.5},{n:4},
    {S0:[[1,2],[2,1]]},{S0:[[1,0],[1,1]]},{xs:[Infinity,0,1]},
    {ys:[0,1]}, {m0:[0,NaN]}
  ]) assert.throws(()=>M.posterior({xs:[-1,0,1],ys:[0,1,2],sigma2:1,...input}),RangeError);
  assert.throws(()=>M.normalPdf(0,0,0),RangeError);
});
test('fixed seed repeats samples and input matrices are unchanged',()=>{
  const p=M.posterior({xs:[-1,0,1],ys:[0,1,2],sigma2:1});
  const before=JSON.stringify(p);
  assert.deepEqual(M.sampleWeights(p,1014,12),M.sampleWeights(p,1014,12));
  assert.equal(JSON.stringify(p),before);
});
```

- [ ] **Step 2: 실패를 확인한다.** `node --test SKILL/tests/math.test.cjs` Expected: MODULE_NOT_FOUND.

- [ ] **Step 3: 작은 행렬 계약을 구현한다.** 아래 핵심 계산과 검증 함수들을 UMD wrapper 안에 넣는다. 2×2 finite symmetric SPD만 허용하며 `inverse`는 determinant가 finite·positive가 아니면 RangeError를 던진다. `xs/ys` 전체의 길이·finite 값을 검사하고 n은 범위 안의 정수로만 허용한다.

```js
function inverse(S) {
  const [[a,b],[c,d]]=S,det=a*d-b*c;
  if(!(det>0) || !Number.isFinite(det)) throw new RangeError('covariance must be SPD');
  return [[d/det,-b/det],[-c/det,a/det]];
}
function posterior({xs,ys,n,m0=[0,0],S0=[[1,0],[0,1]],sigma2}={}) {
  if(n===undefined && Array.isArray(xs)) n=xs.length;
  validate({xs,ys,n,m0,S0,sigma2});
  if(n===0) return {mean:[...m0],cov:S0.map(r=>[...r]),n};
  const A=inverse(S0);
  const b=[A[0][0]*m0[0]+A[0][1]*m0[1],A[1][0]*m0[0]+A[1][1]*m0[1]];
  for(let i=0;i<n;i++){
    const x=xs[i],y=ys[i],beta=1/sigma2;
    A[0][0]+=beta; A[0][1]+=beta*x; A[1][0]+=beta*x; A[1][1]+=beta*x*x;
    b[0]+=beta*y; b[1]+=beta*x*y;
  }
  const cov=inverse(A);
  const mean=[cov[0][0]*b[0]+cov[0][1]*b[1],cov[1][0]*b[0]+cov[1][1]*b[1]];
  validatePosterior({mean,cov});
  return {mean,cov,n};
}
function predict(p,x,sigma2) {
  validatePosterior(p);
  if(!Number.isFinite(x)||!(sigma2>0)||!Number.isFinite(sigma2)) throw new RangeError('invalid prediction input');
  const mean=p.mean[0]+x*p.mean[1];
  const raw=p.cov[0][0]+2*x*p.cov[0][1]+x*x*p.cov[1][1];
  if(!Number.isFinite(raw)||raw < -1e-12) throw new RangeError('invalid function variance');
  const functionVariance=Math.max(0,raw);
  const observationVariance=functionVariance+sigma2;
  if(![mean,functionVariance,observationVariance].every(Number.isFinite)) throw new RangeError('prediction overflow');
  return {mean,functionVariance,observationVariance};
}
function normalPdf(x,mu,v) {
  if(![x,mu,v].every(Number.isFinite)||!(v>0)) throw new RangeError('normal density needs positive variance');
  return Math.exp(-.5*(x-mu)**2/v)/Math.sqrt(2*Math.PI*v);
}
```

입력 검증은 같은 모듈에 다음 함수로 정의한다. 사후·예측의 반환 직전에도 mean·cov·분산이 finite인지 확인하고 overflow이면 RangeError를 던진다.

```js
const vector=(a,n)=>Array.isArray(a)&&a.length===n&&a.every(Number.isFinite);
function requireSPD(S){
  if(!Array.isArray(S)||S.length!==2||!S.every(r=>vector(r,2))||
    Math.abs(S[0][1]-S[1][0])>1e-12||!(S[0][0]>0)||!(S[1][1]>0)||
    !(S[0][0]*S[1][1]-S[0][1]*S[1][0]>0))
    throw new RangeError('covariance must be finite symmetric SPD');
  if(!Number.isFinite(S[0][0]*S[1][1]-S[0][1]*S[1][0])) throw new RangeError('covariance overflow');
}
function validate({xs,ys,n,m0,S0,sigma2}){
  if(!Array.isArray(xs)||!xs.every(Number.isFinite)||!vector(ys,xs.length)||
    !Number.isInteger(n)||n<0||n>xs.length||!vector(m0,2)||
    !Number.isFinite(sigma2)||!(sigma2>0)) throw new RangeError('invalid regression input');
  requireSPD(S0);
}
function validatePosterior(p){
  if(!p||!vector(p.mean,2)) throw new RangeError('invalid posterior mean');
  requireSPD(p.cov);
}
```

브라우저 및 CommonJS export wrapper:

```js
(function(root,factory){
  if(typeof module==='object'&&module.exports) module.exports=factory();
  else root.MLMath=factory();
})(globalThis,function(){
  // 이 task에 정의한 vector, requireSPD, validate, validatePosterior,
  // inverse, posterior, predict, normalPdf, sampleWeights 함수가 이 위치에 들어간다.
  return {posterior,predict,normalPdf,sampleWeights};
});
```

seed 고정 표본은 아래 알고리즘을 사용한다. seed는 finite integer, count는 0..1000 integer만 허용한다.

```js
function sampleWeights(p,seed,count) {
  validatePosterior(p);
  if(!Number.isInteger(seed)||!Number.isInteger(count)||count<0||count>1000)
    throw new RangeError('invalid sampling input');
  const L00=Math.sqrt(p.cov[0][0]),L10=p.cov[1][0]/L00;
  const L11=Math.sqrt(p.cov[1][1]-L10*L10);
  let s=seed>>>0;
  const u=()=>{s=(Math.imul(1664525,s)+1013904223)>>>0;return (s+.5)/4294967296;};
  return Array.from({length:count},()=>{
    const r=Math.sqrt(-2*Math.log(u())),a=2*Math.PI*u();
    const z0=r*Math.cos(a),z1=r*Math.sin(a);
    return [p.mean[0]+L00*z0,p.mean[1]+L10*z0+L11*z1];
  });
}
```

- [ ] **Step 4: 독립 Python 계산과 결과 파일을 만든다.** JS 식을 복사하지 않고 Fraction으로 정밀도 연립방정식을 풀어 정답을 기록한다.

```python
from fractions import Fraction as F
import json
xs=list(map(F,[-1,0,1])); ys=list(map(F,[0,1,2]))
a=F(1)+len(xs); b=sum(xs); d=F(1)+sum(x*x for x in xs)
r=sum(ys); s=sum(x*y for x,y in zip(xs,ys)); det=a*d-b*b
mean=[(d*r-b*s)/det,(a*s-b*r)/det]
cov=[[d/det,-b/det],[-b/det,a/det]]
x=F(2); nu=cov[0][0]+2*x*cov[0][1]+x*x*cov[1][1]
print(json.dumps({'mean':[str(v) for v in mean], 'cov':[[str(v) for v in row] for row in cov],
 'x2':{'mean':str(mean[0]+x*mean[1]),'nu':str(nu),'total':str(nu+1)}},ensure_ascii=False,indent=2))
```

- [ ] **Step 5: 밀도 적분·상관 사전·입력 최소/최대 테스트를 추가한다.** trapezoid로 mean±8sd에서 4096개 구간 적분 후 1과의 오차<1e-6을 확인한다. tau2∈{.25,1,4}, sigma2∈{.1,1,2}, n∈{0,1,3}, x∈{-3,0,3} 전체 조합에서 covariance SPD, `observationVariance-functionVariance=sigma2`를 확인한다.

```js
test('normal density has unit area and predictive variances remain distinct',()=>{
  const h=16/4096;
  let area=0;
  for(let i=0;i<=4096;i++) area+=M.normalPdf(-8+i*h,0,1)*((i===0||i===4096)?0.5:1)*h;
  assert.ok(Math.abs(area-1)<1e-6);
  for(const tau2 of [.25,1,4]) for(const sigma2 of [.1,1,2]) for(const n of [0,1,3]){
    const p=M.posterior({xs:[-1,0,1],ys:[0,1,2],n,sigma2,S0:[[tau2,0],[0,tau2]]});
    assert.ok(p.cov[0][0]*p.cov[1][1]-p.cov[0][1]**2>0);
    for(const x of [-3,0,3]){
      const q=M.predict(p,x,sigma2);
      near(q.observationVariance-q.functionVariance,sigma2);
    }
  }
});
```

- [ ] **Step 6: 실행하고 검사한다.** Node tests와 Python 결과가 위 정답과 일치해야 한다. commit 제안: `feat(ml-interactive): add verified Bayesian regression math`.

## Task 3: 그래프·실험 단계·로컬 수식 셸

**Files:** Modify SKILL/assets/template.dc.html, scripts/build.cjs, scripts/save.cjs, scripts/harness.cjs, scripts/check.cjs, scripts/steps.cjs; Create SKILL/assets/vendor 복사본, tests/ml-template.test.cjs, tests/ml-build.test.cjs, references/scene-api.md, references/design.md, references/math-validation.md.

**Interfaces:**
- Consumes: MLMath API, 기존 `topic/buildScene/extraState/extraVals`, Canvas item 배열 I 및 overlay 배열 O.
- Produces: `compute(state)->plain numeric result`; `topic().PRESETS:Array<object>`; `Step.preset?:object`; 다각형 `{k:6,p:number[3],pts:number[3][],c:string,a?:number}`; `build(srcFile,outFile,{vendorDir?}={}) -> string` 및 `prepareVendor(dest)->absolute vendorDir`.

- [ ] **Step 1: 입력 단계와 band 렌더링 테스트를 추가한다.** template fixture를 복사한 임시 파일에서 topic().STEPS에 아래 preset을 넣고 `extraState`에 tau2 초기값을 추가한다. 테스트 helper는 기존 `withSteps`처럼 실제 Main.dc.html을 변형한다.

```js
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {loadComponent,makeCtx,makeCanvas}=require('../scripts/harness.cjs');
const templateFile=path.join(__dirname,'..','assets','template.dc.html');
function withPreset(t){
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'ml-preset-'));
  t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const file=path.join(dir,'Main.dc.html');
  const src=fs.readFileSync(templateFile,'utf8');
  const out=src.replace(/STEPS: \[[\s\S]*?\n      \],/,
    `STEPS: [{mode:'a',c:'#4A86E8',title:'강한 사전',who:'사전',text:'사전분산을 줄여요.',preset:{tau2:.25}}],`);
  assert.notEqual(out,src,'preset fixture must change the source');
  fs.writeFileSync(file,out);
  return file;
}
test('preset step applies inputs and stops playback',t=>{
  const fileWithPreset=withPreset(t);
  const {c}=loadComponent(fileWithPreset);
  c.setState({playing:true,tau2:1});
  c.pickStep(0);
  assert.equal(c.state.tau2,.25);
  assert.equal(c.state.playing,false);
});
test('flat polygon paints finite coordinates in both themes',()=>{
  const {c}=loadComponent(templateFile);
  c.setMode('a');
  c.buildScene=(mode,I)=>I.push({k:6,p:[-1,-1,0],pts:[[-1,-1,0],[1,-1,0],[0,1,0]],c:c.pal().a,a:.15});
  for(const theme of ['light','dark']){
    const {ctx,calls}=makeCtx(); c.setTheme(theme); c.attachCanvas(makeCanvas(ctx,375,812)); c.draw(.016,16);
    assert.ok(calls.some(x=>x.op==='fill'));
    assert.ok(calls.filter(x=>['moveTo','lineTo'].includes(x.op)).length>=3);
    assert.ok(calls.every(x=>x.args.every(a=>typeof a!=='number'||Number.isFinite(a))));
  }
});
```

- [ ] **Step 2: 실패 결과를 확인한다.** Expected: preset는 적용되지 않으며 polygon branch는 fill하지 않는다.

- [ ] **Step 3: primitive와 단계 동작을 구현한다.** 기존 drawing 루프의 다른 primitive를 건드리지 않고 아래 분기를 추가한다. 모든 pts는 길이3 finite 배열, 최소3점만 허용한다.

```js
if(it.k===6){
  if(!Array.isArray(it.pts)||it.pts.length<3||it.pts.some(p=>p.length!==3||!p.every(Number.isFinite)))
    throw new RangeError('invalid polygon points');
  const points=it.pts.map(p=>this.proj(p,V));
  ctx.fillStyle=it.c; ctx.beginPath();
  points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));
  ctx.closePath(); ctx.fill(); continue;
}
```

`pickStep`는 mode 설정 뒤 preset을 합치고 f 이동·중지를 유지한다. `steps.cjs` 출력에는 preset과 적용 후 핵심 숫자가 보이게 한다.

```js
if(s.preset) this.setState({...s.preset});
this.setState({f:this.sim.f,playing:false,step:i});
```

- [ ] **Step 4: preset 전체와 패널 계산을 검사한다.** harness VM에 `MLMath:require('../assets/ml-math.js')`를 넣는다. check는 PRESETS 각 상태에서 compute→renderVals→draw를 수행하고 예외를 `INPUT_THROWS:<index>`, 비유한값을 `RESULT_NAN:<index>`로 보고한다. 스칼라·배열·객체의 수치만 재귀 검사한다. 검사를 위해 broken fixture의 compute에서 NaN을 반환하는 테스트와 polygon 한 좌표를 NaN으로 바꾸는 테스트를 추가한다.

```js
const finiteTree=value=>typeof value==='number'?Number.isFinite(value):
  Array.isArray(value)?value.every(finiteTree):
  value && typeof value==='object'?Object.values(value).every(finiteTree):true;
```

- [ ] **Step 5: 로컬 자산과 빌드를 연결한다.** 기존 vendor 폴더를 라이선스·provenance와 함께 SKILL/assets/vendor로 복사한다. `prepareVendor`는 dest/.pack/vendor/ml-interactive에 파일이 없으면 exclusive copy하고 이미 있으면 provenance와 해시를 검증한다. 다른 스킬의 vendor 폴더는 덮어쓰지 않는다. preview에도 같은 상대 구조를 사용한다.

```powershell
Copy-Item -LiteralPath (Join-Path $repoRoot '.claude\skills\ml-problem-explain\assets\vendor') -Destination (Join-Path $skillRoot 'assets\vendor') -Recurse
```

build에서 원본 FONT_CSS CDN link를 제거하고 outFile 기준 vendor 상대 경로를 넣는다. HTML에는 MLMath 소스를 runtime 및 Component보다 먼저 inline으로 넣고 `<script` 종료 태그가 들어가지 않는 정적 자산만 임베드한다. KaTeX JS는 mount 전에 로드한다.

```js
const vendorHref=path.relative(path.dirname(outFile),vendorDir).split(path.sep).map(encodeURIComponent).join('/');
const fontLink=`<link rel="stylesheet" href="${vendorHref}/pretendard/pretendard.css">`;
const katexLink=`<link rel="stylesheet" href="${vendorHref}/katex/katex.min.css">`;
const katexScript=`<script src="${vendorHref}/katex/katex.min.js"></script>`;
const mathSource=fs.readFileSync(path.join(__dirname,'..','assets','ml-math.js'),'utf8');
```

정적 공식 ref의 구현:

```js
formulaRef:el=>{
  if(el) window.katex.render(String.raw`S_N=(S_0^{-1}+\sigma^{-2}\Phi^T\Phi)^{-1}`,el,
    {displayMode:true,throwOnError:true});
}
```

unit build test에서 결과의 모든 상대 src/href가 임시 preview 폴더에 존재하고 http(s) 외부 의존성이 없음을 검사한다. 실제 브라우저에서 KaTeX 오류가 없는지는 Task 5에서 확인한다.

`prepareVendor`에서 copied provenance.files에 나열된 SHA256을 검증한다. 복사 전후 해시가 다르면 `VENDOR_HASH_MISMATCH`로 해당 빌드만 중단한다. source vendor는 절대 수정하지 않는다. 라이선스만 확인하고 폰트 실제 파일 존재 검사를 생략하지 않는다.

- [ ] **Step 6: 공통 셸 회귀 테스트를 실행한다.** 초기 template의 demo 검사는 `--allow-template`로 수행한다. 모든 기존 모드·재생·좁은 서랍·blocked storage·reduced motion 테스트를 유지한다.

```powershell
$testPaths = @(Get-ChildItem -LiteralPath (Join-Path $skillRoot 'tests') -Filter '*.test.cjs' -File | Select-Object -ExpandProperty FullName)
node --test @testPaths
node (Join-Path $skillRoot 'scripts\check.cjs') (Join-Path $skillRoot 'assets\template.dc.html') --allow-template
```

Expected: all PASS, template `ok`. commit 제안: `feat(ml-interactive): add plotting and experiment presets`.

## Task 4: 문맥 연결과 팩 갱신 시 복원

**Files:** Modify SKILL/scripts/link-notes.cjs; Create SKILL/scripts/relink.cjs, tests/ml-relink.test.cjs, references/note-links.md; Modify REPO/.claude/skills/ml-review-pack/SKILL.md:142 부근·보고 절; Create REPO/.claude/skills/ml-review-pack/references/interactive-links.md.

**Interfaces:**
- Consumes: runtime manifest `{notes:[{note:absolute,links:[{sectionId,html:absolute,label,before,after,anchorId?}]}]}`.
- Produces: `linkNotes({note,links,dryRun=false})->{note,changed,results}`; stored metadata `{v:1,links:[{note:repoRelative,html:repoRelative,sectionId,label,before,after,anchorId?}]}`; `relink({repo,arg,dryRun=false})->{notes,skipped}`. CLI `node relink.cjs REPO ARG [--dry-run]`.

- [ ] **Step 1: BIO의 연결 동작 테스트를 ML 표식에 맞춰 유지한다.** section 문맥·기존 목적지 링크·앞뒤 byte·escaped text·comments/scripts·같은 절 아닌 link·dry-run·중복 ID 테스트를 모두 유지한다. 새 노트 쓰기 실패 테스트는 `fs.writeFileSync` 주입이 아니라 새 atomic writer의 rename을 실패시켜 원본 bytes 보존을 확인한다.

- [ ] **Step 2: worktree 이동과 ID 누락 복원 테스트를 추가한다.** metadata.note/html은 절대 경로로 저장하지 않는다.

```js
test('relinks a regenerated note after relocating the repo',t=>{
  const repo=fs.mkdtempSync(path.join(os.tmpdir(),'ml-relink-'));
  t.after(()=>fs.rmSync(repo,{recursive:true,force:true}));
  const folder=path.join(repo,'복습노트','1014');
  const data=path.join(folder,'.pack','자료_인터렉티브_01_사후');
  fs.mkdirSync(data,{recursive:true});
  const note=path.join(folder,'정리노트_1014_A.html'),html=path.join(folder,'인터렉티브_01_사후.html');
  const clean='<article id="s1-match"><h3>사후</h3><div class="layer formal">설명</div></article>';
  fs.writeFileSync(note,clean); fs.writeFileSync(html,'<title>사후분포</title>');
  fs.writeFileSync(path.join(data,'note-links.json'),JSON.stringify({v:1,links:[{
    note:'복습노트/1014/정리노트_1014_A.html',html:'복습노트/1014/인터렉티브_01_사후.html',
    sectionId:'s1-match',label:'사후분포 실험',before:'데이터 개수를 ',after:'에서 바꿔 보세요.'
  }]}));
  assert.equal(relink({repo,arg:'1014'}).notes[0].changed,true);
  assert.equal(relink({repo,arg:'1014'}).notes[0].changed,false);
  fs.writeFileSync(note,clean.replace('s1-match','new-id'));
  const result=relink({repo,arg:'1014'});
  assert.equal(result.notes[0].results[0].reason,'SECTION_MISSING');
  assert.equal(fs.readFileSync(note,'utf8'),clean.replace('s1-match','new-id'));
});
```

- [ ] **Step 3: 실패를 확인하고 relink를 구현한다.** `.pack/자료_인터렉티브_*`만 읽는다. notes 폴더는 resolve 결과 또는 `전체`에서 실제 폴더를 열거한다. note 경로로 선택한 대상 폴더를 필터링하며 다른 날짜 노트를 수정하지 않는다. metadata 없는 기존 자료는 `NO_LINK_METADATA`로 보고하여 agent가 내용을 읽고 직접 명세를 만들 수 있게 한다.

상대 경로를 안전하게 푸는 함수:

```js
function repoPath(repo,relative){
  if(typeof relative!=='string'||path.isAbsolute(relative)) throw new Error('relative path required');
  const result=path.resolve(repo,relative),rel=path.relative(path.resolve(repo),result);
  if(rel==='..'||rel.startsWith('..'+path.sep)||path.isAbsolute(rel)) throw new Error('path outside repo');
  return result;
}
```

실제 쓰기는 원본 옆 UUID 임시 파일에 exclusive write→rename을 사용한다. 실패하면 임시 파일만 지우고 원본은 유지한다. 표식은 `data-ml-interactive`; 원본을 byte-equivalent 방식으로 유지하는 offset scan은 그대로 둔다.

- [ ] **Step 4: 기존 폴더가 없는 경우·깨진 JSON·범위 밖 경로 테스트를 추가한다.** empty는 `{notes:[],skipped:[]}`, JSON 오류는 경로와 이유를 기록하고 다른 자료를 계속한다. `../../outside.html`은 거절해야 하며 해당 파일에 쓰지 않는다. rename 실패 테스트 후 임시 파일 잔류도 확인한다.

- [ ] **Step 5: review-pack 지침을 최소 연결한다.** 기본 팩·문제설명 처리 뒤 아래 명령을 수행하는 조건과 별도 결과 보고를 추가한다. 생성 스킬을 자동 호출하지 않는다. ID가 바뀌면 사용자 질문 없이 실제 문맥을 읽어 갱신하거나 skipped를 보고한다.

```powershell
node (Join-Path $repoRoot '.agents\skills\ml-interactive\scripts\relink.cjs') $repoRoot '1014' --dry-run
node (Join-Path $repoRoot '.agents\skills\ml-interactive\scripts\relink.cjs') $repoRoot '1014'
```

범용 지침은 실제 팩 range로 인자를 바꾼다. 스킬이 설치되지 않았거나 기존 자료가 없으면 기본 복습팩 성공을 막지 않는다. 링크 오류를 문제설명 승인 결과와 섞지 않는다. MD 재변환은 호출하지 않는다.

- [ ] **Step 6: 테스트와 연동 결과를 확인한다.** Node 전체 및 기존 review-pack test_skill_files.py를 실행한다. commit 제안: `feat(ml-interactive): link notes and restore existing connections`.

## Task 5: 1014 실험 두 개 저작·독립 검산·브라우저 검증

**Files:** Create RUN/1/Main.dc.html, RUN/2/Main.dc.html, 각 brief.md, evidence/independent_math.py, evidence/math-result.json, evidence/browser-validation.json·PNG; task 통과 후 Task 6이 공개 저장한다.

**Interfaces:**
- Consumes: 공통 셸, MLMath, check/build/steps, 정확한 1014 근거 자료.
- Produces: 검사된 두 Main.dc.html, 결과·관찰 안내·모드·preset·근거와 단순화 기록. 두 자료 모두 `compute(st)`를 사용한다.

- [ ] **Step 1: 실제 근거를 확인하고 브리프를 쓴다.** 입력은 REPO/STT/1014 머러기.md, REPO/강의노트/Lecture04_Linear_Regression_Part2_rev_HO.pdf, REPO/교과서/Mathematics_for_Machine_Learning.pdf, NOTE의 s1-match와 s2-uncertainty. PDF는 관련 페이지만 추출·시각 확인하고 실제 PDF 페이지·슬라이드 번호를 evidence/references-used.json에 기록한다. note에 적힌 페이지를 검증 없이 복사하지 않는다.

```powershell
New-Item -ItemType Directory -Path (Join-Path $runRoot '1'),(Join-Path $runRoot '2') -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $skillRoot 'assets\template.dc.html') -Destination (Join-Path $runRoot '1\Main.dc.html')
Copy-Item -LiteralPath (Join-Path $skillRoot 'assets\template.dc.html') -Destination (Join-Path $runRoot '2\Main.dc.html')
```

- [ ] **Step 2: 공통 계산과 입력을 두 자료에 적용한다.**

```js
extraState(){return {n:3,tau2:1,sigma2:1,xstar:0,labels:true,samples:true};}
compute(st){
  const p=MLMath.posterior({xs:[-1,0,1],ys:[0,1,2],n:st.n,
    S0:[[st.tau2,0],[0,st.tau2]],sigma2:st.sigma2});
  return {posterior:p,prediction:MLMath.predict(p,st.xstar,st.sigma2),
    samples:MLMath.sampleWeights(p,1014,12)};
}
```

수치 조작은 numeric input 및 labeled range로 제공하며 finite·범위·정수 규칙을 적용한다. 빈 number field는 계산 state에 넣지 않고 입력을 마지막 유효값으로 되돌린다. `extraVals`의 handler는 `onChange`를 사용하며 렌더된 n·tau2·sigma2·xstar 값을 일치시킨다. 마크업은 모든 동작에 label·aria 상태를 준다.

- [ ] **Step 3: 첫 자료의 모드·단계·장면을 완성한다.**

| 항목 | 값 |
|---|---|
| 제목 | 사전분포와 사후분포 |
| 모드 | 분포, 회귀 |
| 기본 시점 | yaw=0,pitch=0,zoom=1; rotatable=false,autoSpin=false,playback=null |
| presets | {n:0,tau2:1,sigma2:1}, {n:1,tau2:1,sigma2:1}, {n:3,tau2:1,sigma2:1}, {n:3,tau2:.25,sigma2:1} |
| 패널 | n, mN의 두 성분, SN의 세 독립 성분, σ², τ² |
| 꼭 기억해요 | θ 분포와 y 밀도 구분; 2D 등고선과 1D 확률 구분; 사전 강도와 데이터 영향 |

공분산의 Cholesky L로 단위원을 변환하여 r=1,2의 등고선을 그린다. 아래 실제 좌표 공식을 사용하고 axis 범위는 사전·사후 모두의 좌표를 포함한다.

```js
const L00=Math.sqrt(S[0][0]),L10=S[1][0]/L00,L11=Math.sqrt(S[1][1]-L10*L10);
const contour=Array.from({length:129},(_,i)=>{
  const t=2*Math.PI*i/128,u=r*Math.cos(t),v=r*Math.sin(t);
  return [m[0]+L00*u,m[1]+L10*u+L11*v,0];
});
```

회귀 모드에서는 같은 p의 평균선·12개 고정 표본선·n개 훈련점만 그린다. 관측점을 seed로 새로 생성하지 않는다. axis scaling은 data→scene affine map 한 번으로 처리하며 ticks와 curves가 같은 map을 쓴다.

- [ ] **Step 4: 둘째 자료의 두 모드·단계를 완성한다.**

| 항목 | 값 |
|---|---|
| 제목 | 함수와 관측값의 예측분포 |
| 모드 | 예측 띠, 밀도 |
| presets | {n:0,xstar:0,tau2:1,sigma2:1}, {n:3,xstar:0,tau2:1,sigma2:1}, {n:3,xstar:3,tau2:1,sigma2:1}, {n:3,xstar:3,tau2:1,sigma2:2} |
| readout | μ, ν, σ², ν+σ², √ν, √(ν+σ²) |
| 꼭 기억해요 | 함수값과 새 관측값; 분산과 표준편차; 밀도 높이와 구간 확률 |

예측 띠 모드는 x=-3..3의 121개 점에서 predict를 호출하고 ±2sd upper/lower를 k=6 polygon으로 채운다. 평균선은 동일 μ, 함수 띠와 관측 띠는 서로 다른 색과 범례로 표시한다. 선택한 x*의 수직선을 그린다.

밀도 모드는 두 분포의 넓이가 각각1이며 같은 μ를 가진다. y범위는 μ±5√(ν+σ²), 밀도축은 두 peak를 포함한다. ν=0이면 함수 밀도를 normalPdf로 호출하지 않고 μ 위치의 점질량 표식과 문구를 사용한다. σ² 변경은 posterior부터 다시 계산한다. 단계에 따라 축·panel·문구가 같은 preset을 표시한다.

- [ ] **Step 5: 두 source를 검사하고 대표 수치를 독립 검산한다.**

```powershell
node (Join-Path $skillRoot 'scripts\check.cjs') (Join-Path $runRoot '1\Main.dc.html')
node (Join-Path $skillRoot 'scripts\check.cjs') (Join-Path $runRoot '2\Main.dc.html')
node (Join-Path $skillRoot 'scripts\steps.cjs') (Join-Path $runRoot '1\Main.dc.html')
node (Join-Path $skillRoot 'scripts\steps.cjs') (Join-Path $runRoot '2\Main.dc.html')
```

Expected: 두 check는 ok; 단계 출력의 preset과 숫자가 일치한다. Task 2 Python을 RUN evidence로 복사하여 기본값뿐 아니라 n=0,1,3·tau2=.25·sigma2=2·x*=3도 Fraction 계산한다. 분포 문구·범위·등고선 해석을 원자료에 대조하고 오해를 유발하는 문장을 고친다.

- [ ] **Step 6: 실제 browser에서 8개 화면 조합과 상호작용을 확인한다.** 각 source를 RUN/n/preview.html에 빌드하고 repo 상대 구조를 유지한 stage 서버를 사용한다. 서버 port는 OS가 고른 빈 port를 출력받아 사용하고 종료 시 해당 process만 종료한다. 기존 Browser/CUA 문서에서 지원되는 도구만 사용한다.

검사 JSON의 항목:

```json
{"viewport":[1440,900],"theme":"light","mode":"분포","consoleErrors":[],"katexErrors":0,
 "horizontalOverflow":false,"canvasDrawn":true,"inputUpdatesReadout":true,"presetMatchesPanel":true,
 "resetRepeatsSamples":true,"keyboardWorks":true,"localResourcesLoaded":true}
```

375×812에서는 패널 drawer·Escape·최소44px button·라벨·canvas clipping을 직접 확인한다. 각 자료의 두 모드, 두 theme, 두 viewport를 검사하므로 총16개 mode 화면 조건이다. viewports×themes 기준으로는 자료당4회, 전체8회이며 각 회에 두 모드를 검사한다. `horizontalOverflow`는 root뿐 아니라 panel content의 실제 scrollWidth도 확인한다. 자동화 스크린샷을 저장하고 전체 플롯·축·수식·숫자를 눈으로 확인한다.

- [ ] **Step 7: source·검토 evidence를 최종 동결한다.** 고친 source는 check와 영향 받은 브라우저 조건을 다시 검사한다. 미검증 source는 Task 6으로 넘기지 않는다. commit 제안은 공개 저장 뒤 `docs(notes): add 1014 Bayesian interactives`로 모은다.

## Task 6: 발행·노트 연결·스킬 문서·최종 보존 검증

**Files:** Create PACK 공개 HTML 두 개, .pack 소유 자료·vendor; Modify NOTE의 두 연결 위치; Modify SKILL/SKILL.md·references/topic-selection.md·agents/openai.yaml 및 REPO/README.md.

**Interfaces:**
- Consumes: 통과한 RUN source·evidence, save 결과, `linkNotes` 명세.
- Produces: 최종 HTML 두 개·노트 새 탭 연결·재실행 unchanged·공개 경로 검증 보고.

- [ ] **Step 1: 기존 파일 hashes와 노트 백업을 RUN에 기록한다.** 모든 1014 기존 파일을 읽어 sha256을 기록한다. 새 `.pack` 디렉터리를 만들기 전에 수행한다.

```powershell
New-Item -ItemType Directory -Path (Join-Path $runRoot 'backups') -Force | Out-Null
Copy-Item -LiteralPath $notePath -Destination (Join-Path $runRoot 'backups\note.html')
Get-ChildItem -LiteralPath $packRoot -File -Recurse | Get-FileHash -Algorithm SHA256 |
    Select-Object Path,Hash | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runRoot 'before-hashes.json') -Encoding utf8
```

- [ ] **Step 2: 두 source를 개별 save하고 실제 출력을 저장한다.**

```powershell
node (Join-Path $skillRoot 'scripts\save.cjs') (Join-Path $runRoot '1\Main.dc.html') $packRoot '사전분포와_사후분포'
node (Join-Path $skillRoot 'scripts\save.cjs') (Join-Path $runRoot '2\Main.dc.html') $packRoot '함수와_관측값의_예측분포'
```

각 JSON을 RUN/save-1.json·save-2.json에 기록하고 `dir`에 brief·evidence를 복사한다. `html/dir`는 출력된 실제 값을 사용하며 예상01·02를 하드코딩하지 않는다. 공개 HTML을 실제 최종 경로에서 열어 수식·폰트·console을 다시 확인한다.

- [ ] **Step 3: 두 연결 명세를 저작하고 dry-run한다.** note 실제 경로와 save 결과를 사용한다. 예시 값의 절·문구는 다음 확정값이다.

```js
const links=[
 {sectionId:'s1-match',html:first.html,label:'사전분포와 사후분포 실험',
  before:'데이터 개수와 사전분산을 바꿀 때 사후분포가 어떻게 달라지는지 ',after:'에서 비교해 보세요.'},
 {sectionId:'s2-uncertainty',anchorId:'widget-uncertainty',html:second.html,label:'함수와 관측값의 예측분포 실험',
  before:'입력 위치와 잡음 분산을 바꾸며 함수값과 새 관측값의 예측 띠를 ',after:'에서 비교해 보세요.'}
];
const manifest={notes:[{note:notePath,links}]};
```

source storage용 각 `note-links.json`에는 자기 자료의 link 한 개와 `v:1`만 기록하고 `note/html`을 repo-relative forward slash로 바꾼다. raw absolute 경로는 evidence에서도 필요한 경우 별도 실행 로그로만 둔다.

- [ ] **Step 4: 연결을 적용하고 재실행한다.**

```powershell
node (Join-Path $skillRoot 'scripts\link-notes.cjs') (Join-Path $runRoot 'note-links.json') --dry-run
node (Join-Path $skillRoot 'scripts\link-notes.cjs') (Join-Path $runRoot 'note-links.json')
node (Join-Path $skillRoot 'scripts\link-notes.cjs') (Join-Path $runRoot 'note-links.json')
```

Expected: 처음 added 두 개, 두 번째 changed:false·unchanged 두 개. `.formal` 뒤/위젯 뒤를 브라우저에서 직접 읽고 두 링크를 각각 클릭한다. 새 탭 제목·최종 파일·원 노트 유지·375px 안내 overflow를 확인한다. 일반 재연결 CLI dry-run도 unchanged여야 한다.

- [ ] **Step 5: 스킬 본문과 discovery metadata를 완성한다.** 이름은 ml-interactive, description은 머신러닝 날짜·주제·기존 자료 연결을 trigger로 쓰고 정리노트·문제 생성은 ml-review-pack으로 라우팅한다. 준비에서는 REPO/복습노트·STT·강의노트·MML 존재와 Node floor를 검사한다. 주제 선정은 변화가 관찰되는 관계·분포·벡터 기하를 점수화하고 정의만 있는 후보를 제외한다. 내용 검토는 생물학 분자 방향 대신 행렬 차원·밀도·공분산·불확실성 해석을 대조한다. 복사된 생명과학 전용 경로·example-dna 의존성·opus 강제·Codex에 subagent가 없다는 문구를 제거한다. 위임은 사용자가 선택한 실행 방식과 실제 도구에 맞춘다.

SKILL frontmatter와 핵심 라우팅 문구:

```yaml
name: ml-interactive
description: 머신러닝기초 날짜나 주제로 수치·분포·그래프를 조작하는 인터랙티브 HTML을 만들고 기존 정리노트의 관련 설명에 연결한다. 인터랙티브 자료 생성, ML 시각 실험, 기존 자료 연결 또는 /ml-interactive [MMDD|주제]에 사용한다. 정리노트와 복습문제 생성은 ml-review-pack을 사용한다.
```

본문은 다음 조건을 실제 실행 절차에 넣는다: 연결만 요청되면 resolve·내용 확인·연결 명세·dry-run·적용·재실행·브라우저 확인만 수행한다. 생성 요청이면 범위 파악 후 후보선정과 brief를 완료하고 source 검사·독립 검산·내용 검토·브라우저 검증을 통과한 자료만 save한다. 주제별 실패는 다른 통과 주제를 막지 않으며 생성됨/연결보류를 구분한다. 최종 보고는 파일·모드·조작·단순화·보충·검증·노트 절·added/updated/unchanged/skipped·RUN·백업·커밋 제안을 포함한다.

```yaml
interface:
  display_name: "머신러닝 인터랙티브"
  short_description: "ML 개념을 조작하는 HTML 자료를 만들고 정리노트에 연결"
  default_prompt: "Use $ml-interactive to create interactive learning materials and link them to the relevant machine learning review notes."
```

README에는 `/ml-interactive 1014`, `/ml-interactive 가우시안 곱`, 기존 자료 전체 연결 요청, HTML/.pack 저장 규칙과 이번 두 공개 경로를 추가한다. 자동 발견을 유지한다.

- [ ] **Step 6: 전체 검사·보존 여부·diff를 확인한다.**

```powershell
$testPaths = @(Get-ChildItem -LiteralPath (Join-Path $skillRoot 'tests') -Filter '*.test.cjs' -File | Select-Object -ExpandProperty FullName)
node --test @testPaths
python (Join-Path $repoRoot '.claude\skills\ml-review-pack\tests\test_skill_files.py')
python 'C:\Users\Hyunjun\.codex\skills\.system\skill-creator\scripts\quick_validate.py' $skillRoot
git -C $repoRoot diff --check
git -C $repoRoot status --short
git -C $repoRoot diff --numstat
```

신규 untracked 파일은 `git diff --no-index -- /dev/null FILE`의 Windows 대응인 읽기 검토 또는 내용별 검사를 수행하고 diff에 안 보인다고 무시하지 않는다. before-hashes의 NOTE 제외 파일은 모두 동일해야 한다. 노트는 `data-ml-interactive` 문단 두 개를 offset scan으로 제거한 문자열이 backup 원본과 같아야 한다. `.pack` 생성이 있어도 기존 root MD·PDF·자료·그림을 이동·수정하지 않았는지 확인한다. 생명과학 원본도 git status에 새 변경이 없어야 한다.

BIO에는 실행 전부터 `.scratch/` 등의 사용자 미추적 파일이 있을 수 있으므로 clean 상태를 요구하지 않는다. 실행 전 status와 비교하여 이번 작업이 BIO에 변경을 추가하지 않았음을 확인한다.

- [ ] **Step 7: 결과를 사용자에게 전달한다.** 스킬·두 HTML·수정 노트의 절대 링크, 수학·브라우저 검사 결과, 보류·단순화·RUN/백업을 짧게 보고한다. 결과를 보기 쉽게 두 HTML 또는 정리노트를 open_in_codex로 연다. 자동 커밋하지 않는다. 변경 묶음별 commit 제안만 제공한다.

## 계획 자체 검토 기록

- Spec coverage: 경로·발견·저장 충돌 Task1, 수학 Task2, 그래프·수식·preset Task3, 연결·팩 갱신 Task4, 1014 두 자료 Task5, 발행·보존·보고 Task6.
- Interface consistency: posterior/compute/preset/build/save/linkNotes/relink의 키·서명은 각 생산 task와 소비 task에서 동일하게 사용한다.
- Review Focus: 다섯 항목을 담당 task의 실패 테스트·독립 계산·브라우저·hash 보존 검사에 배치했다.
- Source copies are starting points: 스킬 문서의 과목·근거·역할 계약은 Task6에서 ML 전용으로 완성하며 생명과학 런타임 파일은 원본 저장소에 의존하지 않는다.
- Execution handoff: writing-plans 지침에 따라 사용자에게 계획 검토와 실행 방법을 한 번 요청하고 답을 받은 뒤 구현을 시작한다. Native를 권장한다: 여섯 task가 동일 template·math·link 인터페이스를 연속 수정하고 실제 두 자료 검토도 이어지므로 한 실행자가 문맥을 유지하기 쉽다.
