const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { resolve, nextNumber } = require('../scripts/resolve.cjs');

// Builds a repo in a tmp dir. Every path is written NFD like macOS stores Korean names.
// A value of null makes a directory.
function fixture(tree) {
  const repo = fs.mkdtempSync(path.join(os.tmpdir(), 'bi-resolve-'));
  for (const [rel, content] of Object.entries(tree)) {
    const p = path.join(repo, rel.normalize('NFD'));
    if (content === null) fs.mkdirSync(p, { recursive: true });
    else { fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, content); }
  }
  return repo;
}
const nfc = (p) => p.normalize('NFC').replace(/\\/g, '/');

test('date folder with notes and stt', () => {
  const repo = fixture({ '복습노트/1006/.pack/정리노트_1006_X.md': '# 전사', '복습노트/1006/정리노트_1006_X.html': '', 'STT/1006 머러기.md': '...' });
  const r = resolve({ repo, arg: '1006' });
  assert.equal(r.kind, 'date');
  assert.equal(r.date, '1006');
  assert.equal(r.exists, true);
  assert.ok(nfc(r.folder).endsWith('복습노트/1006'));
  assert.equal(r.notes.length, 1);
  assert.equal(r.noteHtml.length, 1);
  assert.ok(fs.existsSync(r.noteHtml[0]));
  assert.ok(nfc(r.noteHtml[0]).endsWith('정리노트_1006_X.html'));
  assert.ok(nfc(r.notes[0]).endsWith('1006/.pack/정리노트_1006_X.md'));
  assert.ok(r.stt && nfc(r.stt).endsWith('STT/1006 머러기.md'));
  assert.ok(fs.existsSync(r.stt));
  assert.equal(r.next, '01');
});

test('finds NFD-named folders', () => {
  const repo = fixture({ '복습노트/1006/.pack/정리노트_1006_전사와_번역.md': '# 전사', 'STT/1006 머러기.md': '...' });
  const r = resolve({ repo, arg: '1006' });
  assert.equal(r.notes.length, 1);
  assert.ok(fs.existsSync(r.folder));
  assert.ok(fs.existsSync(r.notes[0]));
});

test('date inside a range folder', () => {
  const repo = fixture({ '복습노트/0922-0924/.pack/정리노트_0922-0924_X.md': '', '복습노트/0929/.pack/정리노트_0929_Y.md': '' });
  const r = resolve({ repo, arg: '0923' });
  assert.ok(nfc(r.folder).endsWith('복습노트/0922-0924'));
  assert.equal(r.exists, true);
  assert.equal(r.date, '0923');
});

test('exact folder wins over a range that also covers the date', () => {
  const repo = fixture({ '복습노트/0922-0924/a.md': '', '복습노트/0922/b.md': '' });
  assert.ok(nfc(resolve({ repo, arg: '0922' }).folder).endsWith('복습노트/0922'));
});

test('stt only date points to a new folder', () => {
  const repo = fixture({ '복습노트/1006/.pack/정리노트_1006_X.md': '', 'STT/1013 머러기.md': '...' });
  const r = resolve({ repo, arg: '1013' });
  assert.equal(r.exists, false);
  assert.ok(nfc(r.folder).endsWith('복습노트/1013'));
  assert.deepEqual(r.notes, []);
  assert.deepEqual(r.noteHtml, []);
  assert.ok(r.stt);
  assert.equal(r.next, '01');
});

test('no folder and no stt is NO_TARGET', () => {
  const repo = fixture({ '복습노트/1006/a.md': '' });
  assert.throws(() => resolve({ repo, arg: '1231' }), { code: 'NO_TARGET' });
});

test('empty arg is NO_ARG', () => {
  const repo = fixture({ '복습노트/1006/a.md': '' });
  assert.throws(() => resolve({ repo, arg: '' }), { code: 'NO_ARG' });
  assert.throws(() => resolve({ repo, arg: '   ' }), { code: 'NO_ARG' });
});

test('topic picks the latest note that mentions it', () => {
  const repo = fixture({
    '복습노트/0929/.pack/정리노트_0929_A.md': '젖당 오페론은 다음 시간에',
    '복습노트/1006/.pack/정리노트_1006_B.md': 'lac 오페론의 조절',
    '복습노트/1008/.pack/정리노트_1008_C.md': '세포 호흡',
    'STT/1006 머러기.md': '...',
  });
  const r = resolve({ repo, arg: '오페론' });
  assert.equal(r.kind, 'topic');
  assert.ok(nfc(r.folder).endsWith('복습노트/1006'));
  assert.equal(r.date, '1006');
  assert.ok(r.stt);
});

test('topic match ignores spaces, case, and NFD note text', () => {
  const repo = fixture({ '복습노트/1006/.pack/정리노트_1006_B.md': 'Lac 오페론'.normalize('NFD') });
  assert.ok(nfc(resolve({ repo, arg: 'lac오페론' }).folder).endsWith('복습노트/1006'));
});

test('topic not in any note goes to 주제별', () => {
  const repo = fixture({ '복습노트/1006/.pack/정리노트_1006_B.md': '오페론' });
  const r = resolve({ repo, arg: '광합성' });
  assert.equal(r.kind, 'topic');
  assert.ok(nfc(r.folder).endsWith('복습노트/주제별'));
  assert.equal(r.date, null);
  assert.equal(r.stt, null);
  assert.equal(r.next, '01');
});

test('existing interactives are listed with titles', () => {
  const repo = fixture({
    '복습노트/1001/3D모형_1001_x.html': '<html><head><title>__TITLE__</title></head></html>',
    '복습노트/1001/인터렉티브_01.html': '<title>세포 분열</title>',
    '복습노트/1001/정리노트_1001_x.html': '<title>정리노트</title>',
  });
  const r = resolve({ repo, arg: '1001' });
  assert.deepEqual(r.existing.map((e) => e.title).sort(), ['__TITLE__', '세포 분열']);
  assert.ok(r.existing.every((e) => typeof e.file === 'string'));
});

test('next number skips past every existing NN', () => {
  const repo = fixture({ '복습노트/1001/인터렉티브_03.html': '<title>a</title>', '복습노트/1001/.pack/자료_인터렉티브_04': null, '복습노트/1001/인터렉티브_01.html': '' });
  assert.equal(resolve({ repo, arg: '1001' }).next, '05');
});

test('next number counts names with a content suffix', () => {
  const repo = fixture({ '복습노트/1001/인터렉티브_02_DNA_Replication.html': '<title>a</title>', '복습노트/1001/.pack/자료_인터렉티브_03_Mitosis': null });
  assert.equal(resolve({ repo, arg: '1001' }).next, '04');
});

test('cli prints json, or an error code with exit 1', () => {
  const repo = fixture({ '복습노트/1006/.pack/정리노트_1006_X.md': '' });
  const cli = path.join(__dirname, '..', 'scripts', 'resolve.cjs');
  const ok = spawnSync('node', [cli, repo, '1006'], { encoding: 'utf8' });
  assert.equal(ok.status, 0);
  assert.equal(JSON.parse(ok.stdout).next, '01');
  const bad = spawnSync('node', [cli, repo, '1231'], { encoding: 'utf8' });
  assert.equal(bad.status, 1);
  assert.deepEqual(JSON.parse(bad.stdout), { error: 'NO_TARGET' });
});

test('topic prefers the note that teaches it over a later back-link', () => {
  const repo = fixture({
    '복습노트/1006/.pack/정리노트_1006_B.md': '## 전사\n### lac 오페론의 억제자 스위치\n오페론은 ...',
    '복습노트/1008/.pack/정리노트_1008_C.md': '# 세포 호흡\n[지난 1006 수업: 전사·번역과 오페론](../1006/x.html)\n',
  });
  assert.ok(nfc(resolve({ repo, arg: '오페론' }).folder).endsWith('복습노트/1006'));
});

test('range argument resolves to that range folder', () => {
  const repo = fixture({ '복습노트/0922-0924/.pack/정리노트_0922-0924_X.md': '' });
  const r = resolve({ repo, arg: '0922-0924' });
  assert.equal(r.kind, 'date');
  assert.ok(nfc(r.folder).endsWith('복습노트/0922-0924'));
  assert.throws(() => resolve({ repo, arg: '0101-0102' }), { code: 'NO_TARGET' });
});

test('a heading with every word of a multi-word topic counts as a heading match', () => {
  const repo = fixture({
    '복습노트/1001/.pack/정리노트_1001_A.md': '## 3. DNA 구조가 복제를 예고한다\n본문',
    '복습노트/1008/.pack/정리노트_1008_C.md': '# 번역\n지난 시간 DNA 복제에 이어서',
  });
  assert.ok(nfc(resolve({ repo, arg: 'DNA 복제' }).folder).endsWith('복습노트/1001'));
});

test('nextNumber counts .pack data folders in a range folder', () => {
  const repo = fixture({ '복습노트/0922-0924/.pack/자료_인터렉티브_03_x/Main.dc.html': '' });
  assert.equal(nextNumber(resolve({ repo, arg: '0922-0924' }).folder), '04');
});

test('nextNumber still counts legacy root data folders and tolerates a missing .pack', () => {
  const repo = fixture({ '복습노트/1001/자료_인터렉티브_02_old': null, '복습노트/1001/인터렉티브_01.html': '' });
  assert.equal(nextNumber(resolve({ repo, arg: '1001' }).folder), '03');
});

test('legacy notes at the date-folder root are read', () => {
  const repo = fixture({ '복습노트/1006/정리노트_1006_X.md': '# 전사', 'STT/1006 머러기.md': '...' });
  assert.equal(resolve({repo,arg:'1006'}).notes.length,1);
});
