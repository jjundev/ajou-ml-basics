const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {loadComponent}=require('../scripts/harness.cjs');
const {check}=require('../scripts/check.cjs');
const T=path.join(__dirname,'../assets/template.dc.html');
function formulaFile(){let s=fs.readFileSync(T,'utf8').replace('autoSpin: true, rotatable: true','autoSpin: false, rotatable: false').replace("key: 'a', label: '구조',", "key: 'a', label: '구조', title: '두 식 비교', view: 'formula',").replace("title: '고리 살펴보기', who: '구조',", "title: '출발식', tex: 'x=1', who: '',");s=s.replace("STEPS: [", "STEPS: [\n        {mode:'a',c:'#4A86E8',title:'첫 줄',tex:'x=0',text:'첫 이유'},");const f=path.join(fs.mkdtempSync(path.join(os.tmpdir(),'ml-ui-')),'Main.dc.html');fs.writeFileSync(f,s);return f;}
test('formula steps accumulate and navigate without affecting graph camera',()=>{const {c}=loadComponent(formulaFile());let v=c.renderVals();assert.equal(v.isFormula,true);assert.equal(v.stageTitle,'두 식 비교');assert.equal(v.formulaRows.length,1);assert.equal(v.formulaPrevDisabled,true);v.formulaNext();v=c.renderVals();assert.equal(v.formulaRows.length,2);assert.equal(v.formulaRows[0].active,false);assert.equal(v.formulaRows[1].active,true);assert.equal(v.formulaNextDisabled,true);const zoom=c.cam.zoom;v.zoomIn();assert.equal(c.cam.zoom,zoom);assert.ok(c.renderVals().formulaScale>1);c.renderVals().resetView();assert.equal(c.renderVals().formulaScale,1);c.renderVals().formulaPrev();assert.equal(c.renderVals().formulaRows.length,1);});
test('graph remains default and keeps camera zoom and playback',()=>{const {c}=loadComponent(T);assert.equal(c.renderVals().isFormula,false);c.renderVals().zoomIn();assert.ok(c.cam.zoom>1);c.renderVals().resetView();assert.equal(c.cam.zoom,1);c.setMode('b');assert.equal(c.renderVals().hasPlayback,true);});
test('formula type validates usable rows',()=>{const f=formulaFile();assert.equal(check(f,{allowTemplate:true}).ok,true);const s=fs.readFileSync(f,'utf8').replace(/tex: 'x=1'/,"tex: ''");fs.writeFileSync(f,s);assert.ok(check(f,{allowTemplate:true}).errors.some(e=>e.includes('formula')));});

test('formula checker allows an empty canvas but rejects missing and mixed rows', () => {
  const file = formulaFile();
  const source = fs.readFileSync(file, 'utf8').replace('buildScene(mode, I, O) {', 'buildScene(mode, I, O) { if(mode === "a")return;');
  fs.writeFileSync(file, source);
  assert.equal(check(file, {allowTemplate:true}).ok, true);
  for(const change of [
    s=>s.replace("tex: 'x=1'", "tex: 'x=1',left:'x'"),
    s=>s.replaceAll("mode:'a'", "mode:'b'").replaceAll("mode: 'a'", "mode: 'b'")
  ]) {
    fs.writeFileSync(file, change(source));
    assert.ok(check(file, {allowTemplate:true}).errors.some(e=>e.includes('.formula')));
  }
});

test('formula navigation stays bounded and changing mode resets size and progress', () => {
  const {c} = loadComponent(formulaFile());
  c.renderVals().formulaPrev();
  assert.equal(c.renderVals().formulaRows.length, 1);
  c.renderVals().formulaNext();
  c.renderVals().formulaNext();
  assert.equal(c.renderVals().formulaRows.length, 2);
  for(let i=0;i<15;i++)c.renderVals().zoomIn();
  assert.equal(c.renderVals().formulaScale,1.6);
  for(let i=0;i<15;i++)c.renderVals().zoomOut();
  assert.equal(c.renderVals().formulaScale,.8);
  c.setMode('b');c.setMode('a');
  assert.equal(c.renderVals().formulaScale,1);
  assert.equal(c.renderVals().formulaRows.length,1);
});
