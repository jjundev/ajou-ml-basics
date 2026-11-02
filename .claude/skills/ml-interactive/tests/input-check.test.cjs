const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {check}=require('../scripts/check.cjs');
test('checker rejects non-finite experiment results',t=>{
 const d=fs.mkdtempSync(path.join(os.tmpdir(),'ml-bad-'));t.after(()=>fs.rmSync(d,{recursive:true,force:true}));
 const f=path.join(d,'Main.dc.html');let s=fs.readFileSync(path.join(__dirname,'../assets/template.dc.html'),'utf8');
 s=s.replace('  topic() {','  compute(){return {value:NaN};}\n  topic() {').replace('      DEMO: true,','      PRESETS:[{}], DEMO: true,');fs.writeFileSync(f,s);
 assert.ok(check(f,{allowTemplate:true}).errors.includes('RESULT_NAN:0'));
});
test('note rename failure preserves bytes and leaves no temporary file',t=>{
 const {linkNotes}=require('../scripts/link-notes.cjs');const d=fs.mkdtempSync(path.join(os.tmpdir(),'ml-atomic-'));t.after(()=>fs.rmSync(d,{recursive:true,force:true}));
 const note=path.join(d,'note.html'),html=path.join(d,'experiment.html'),s='<article id="a"><h3>Example</h3></article>';fs.writeFileSync(note,s);fs.writeFileSync(html,'<title>X</title>');
 const orig=fs.renameSync;fs.renameSync=()=>{throw new Error('rename blocked');};
 try{assert.throws(()=>linkNotes({note,links:[{sectionId:'a',html,label:'X',before:'Try ',after:'.'}]}),/rename blocked/);}finally{fs.renameSync=orig;}
 assert.equal(fs.readFileSync(note,'utf8'),s);assert.deepEqual(fs.readdirSync(d).sort(),['experiment.html','note.html']);
});
