const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {resolve,nextNumber}=require('../scripts/resolve.cjs');
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