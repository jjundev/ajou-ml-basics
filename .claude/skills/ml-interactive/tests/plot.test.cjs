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
