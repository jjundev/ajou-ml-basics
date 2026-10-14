const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {save}=require('../scripts/save.cjs');
const {nextNumber,resolve}=require('../scripts/resolve.cjs');
function setup(t){const dest=fs.mkdtempSync(path.join(os.tmpdir(),'ml-save-'));t.after(()=>fs.rmSync(dest,{recursive:true,force:true}));return dest;}
test('reserves .pack source numbers',t=>{const d=setup(t);fs.mkdirSync(path.join(d,'.pack','자료_인터렉티브_01_기존'),{recursive:true});assert.equal(nextNumber(d),'02');});
test('ambiguous date ranges are rejected',t=>{const d=setup(t);for(const x of ['1010-1015','1012-1016'])fs.mkdirSync(path.join(d,'복습노트',x),{recursive:true});assert.throws(()=>resolve({repo:d,arg:'1014'}),{code:'AMBIGUOUS_TARGET'});});
test('exclusive page collision preserves the colliding file',t=>{
 const dest=setup(t),src=path.join(__dirname,'../assets/template.dc.html'),html=path.join(dest,'인터렉티브_01_Test.html');
 const orig=fs.mkdirSync;fs.mkdirSync=(p,...a)=>{const r=orig(p,...a);if(String(p).endsWith('자료_인터렉티브_01_Test'))fs.writeFileSync(html,'keep');return r;};
 try{assert.throws(()=>save({src,dest,name:'Test'}),{code:'EEXIST'});}finally{fs.mkdirSync=orig;}
 assert.equal(fs.readFileSync(html,'utf8'),'keep');assert.ok(!fs.existsSync(path.join(dest,'.pack','자료_인터렉티브_01_Test')));
});
test('write failure after exclusive open removes only the new page',t=>{
 const dest=setup(t),src=path.join(__dirname,'../assets/template.dc.html');const orig=fs.writeFileSync;
 fs.writeFileSync=(p,...a)=>{if(typeof p==='number')throw new Error('injected write failure');return orig(p,...a);};
 try{assert.throws(()=>save({src,dest,name:'Test'}),/injected/);}finally{fs.writeFileSync=orig;}
 assert.ok(!fs.existsSync(path.join(dest,'인터렉티브_01_Test.html')));assert.ok(!fs.existsSync(path.join(dest,'.pack','자료_인터렉티브_01_Test')));
});
