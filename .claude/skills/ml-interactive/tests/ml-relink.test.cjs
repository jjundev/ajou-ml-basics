const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {relink}=require('../scripts/relink.cjs');
test('finds cross-date artifacts but modifies only the requested note folder',t=>{
 const repo=fs.mkdtempSync(path.join(os.tmpdir(),'ml-cross-'));t.after(()=>fs.rmSync(repo,{recursive:true,force:true}));
 const old=path.join(repo,'복습노트/1012'),newer=path.join(repo,'복습노트/1014'),d=path.join(newer,'.pack/자료_인터렉티브_01_X');
 fs.mkdirSync(old,{recursive:true});fs.mkdirSync(d,{recursive:true});
 const note=path.join(old,'정리노트_1012_A.html'),other=path.join(newer,'정리노트_1014_B.html'),html=path.join(newer,'인터렉티브_01_X.html');
 const clean='<article id="a"><h3>X</h3></article>';fs.writeFileSync(note,clean);fs.writeFileSync(other,clean);fs.writeFileSync(html,'X');
 const link=n=>({note:path.relative(repo,n),html:path.relative(repo,html),sectionId:'a',label:'X',before:'Try ',after:'.'});
 fs.writeFileSync(path.join(d,'note-links.json'),JSON.stringify({v:1,links:[link(note),link(other)]}));
 const got=relink({repo,arg:'1012'});assert.equal(got.notes.length,1);assert.equal(got.notes[0].changed,true);assert.equal(fs.readFileSync(other,'utf8'),clean);
 fs.writeFileSync(note,clean);assert.equal(relink({repo,arg:'전체'}).notes.length,2);
});
test('empty target is a no-op and invalid metadata cannot escape the repo',t=>{
 const repo=fs.mkdtempSync(path.join(os.tmpdir(),'ml-meta-'));t.after(()=>fs.rmSync(repo,{recursive:true,force:true}));
 assert.deepEqual(relink({repo,arg:'1014'}),{notes:[],skipped:[]});
 const folder=path.join(repo,'복습노트','1014'),d=path.join(folder,'.pack','자료_인터렉티브_01_X');fs.mkdirSync(d,{recursive:true});
 const file=path.join(d,'note-links.json');fs.writeFileSync(file,'broken');assert.equal(relink({repo,arg:'1014'}).skipped[0].reason,'METADATA_INVALID');
 fs.writeFileSync(file,JSON.stringify({v:1,links:[{note:'../../outside.html',html:'../../target.html'}]}));
 assert.equal(relink({repo,arg:'1014'}).skipped[0].reason,'METADATA_INVALID');
 fs.unlinkSync(file);assert.equal(relink({repo,arg:'1014'}).skipped[0].reason,'NO_LINK_METADATA');
});
test('all targets honors actual NFD note-root names',t=>{
 const repo=fs.mkdtempSync(path.join(os.tmpdir(),'ml-nfd-'));t.after(()=>fs.rmSync(repo,{recursive:true,force:true}));
 const relative=path.join('복습노트'.normalize('NFD'),'1014'),folder=path.join(repo,relative),d=path.join(folder,'.pack','자료_인터렉티브_01_X');fs.mkdirSync(d,{recursive:true});
 const note=path.join(folder,'정리노트_A.html'),html=path.join(folder,'인터렉티브_01_X.html');fs.writeFileSync(note,'<article id="a"><h3>X</h3></article>');fs.writeFileSync(html,'X');
 fs.writeFileSync(path.join(d,'note-links.json'),JSON.stringify({v:1,links:[{note:path.relative(repo,note),html:path.relative(repo,html),sectionId:'a',label:'X',before:'Try ',after:'.'}]}));
 assert.equal(relink({repo,arg:'전체'}).notes.length,1);
});
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
test('date targets match NFC metadata against NFD folders on disk',t=>{
 const repo=fs.mkdtempSync(path.join(os.tmpdir(),'ml-nfd-date-'));t.after(()=>fs.rmSync(repo,{recursive:true,force:true}));
 const folder=path.join(repo,'복습노트'.normalize('NFD'),'1102'),d=path.join(folder,'.pack','자료_인터렉티브_01_사영'.normalize('NFD'));fs.mkdirSync(d,{recursive:true});
 const clean='<article id="a"><h3>X</h3></article>',note=path.join(folder,'정리노트_1102_PCA.html'.normalize('NFD'));
 fs.writeFileSync(note,clean);fs.writeFileSync(path.join(folder,'인터렉티브_01_사영.html'.normalize('NFD')),'X');
 fs.writeFileSync(path.join(d,'note-links.json'),JSON.stringify({v:1,links:[{note:'복습노트/1102/정리노트_1102_PCA.html',html:'복습노트/1102/인터렉티브_01_사영.html',sectionId:'a',label:'X',before:'Try ',after:'.'}]}));
 const first=relink({repo,arg:'1102'});assert.equal(first.notes.length,1);assert.equal(first.notes[0].changed,true);
 const again=relink({repo,arg:'1102'});assert.equal(again.notes[0].changed,false);assert.equal(again.notes[0].results[0].status,'unchanged');
});
