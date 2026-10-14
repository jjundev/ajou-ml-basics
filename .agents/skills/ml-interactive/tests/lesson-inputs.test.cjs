const test=require('node:test'),assert=require('node:assert/strict'),path=require('node:path');
const {loadComponent}=require('../scripts/harness.cjs');
const repo=path.resolve(__dirname,'../../../..');
for(const name of ['01_사전분포와_사후분포','02_함수와_관측값의_예측분포']){
 const file=path.join(repo,'복습노트/1014/.pack/자료_인터렉티브_'+name+'/Main.dc.html');
 test(name+' reset clears contradictory step and playback',()=>{
  const {c}=loadComponent(file);c.pickStep(0);c.setState({playing:true});c.renderVals().resetInputs();
  assert.equal(c.state.n,3);assert.equal(c.state.step,-1);assert.equal(c.state.playing,false);assert.equal(c.renderVals().hasStep,false);
 });
 test(name+' refuses off-step numeric values and keeps controls aligned',()=>{
  const {c}=loadComponent(file);
  for(const [key,bad,want] of [['tau2','.33',1],['sigma2','.33',1],...(name.startsWith('02')?[['xstar','.33',0]]:[])]){
   const input={target:{value:bad}};c.extraVals(c.state).controls.find(v=>v.key===key).change(input);
   assert.equal(c.state[key],want);assert.equal(input.target.value,String(want));
  }
 });
}
