const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const nfc = (p) => p.normalize('NFC').replace(/\\/g, '/');
const { save } = require('../scripts/save.cjs');

const SKILL = path.join(__dirname, '..');
const T = path.join(SKILL, 'assets', 'template.dc.html');
const SCRIPT = path.join(SKILL, 'scripts', 'save.cjs');

// A fresh run folder with one topic (run/1/Main.dc.html) and an empty dest folder.
function setup() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bi-save-'));
  const src = path.join(tmp, 'run', '1', 'Main.dc.html');
  fs.mkdirSync(path.dirname(src), { recursive: true });
  fs.writeFileSync(src, fs.readFileSync(T, 'utf8').replaceAll('__TITLE__', '테스트 주제'));
  const dest = path.join(tmp, '1010');
  fs.mkdirSync(dest);
  return { tmp, src, dest };
}

test('first save gets 01', () => {
  const { src, dest } = setup();
  const r = save({ src, dest, name: 'Test_Topic' });
  assert.equal(r.nn, '01');
  assert.equal(r.html, path.join(dest, '인터렉티브_01_Test_Topic.html'));
  assert.equal(r.dir, path.join(dest, '.pack', '자료_인터렉티브_01_Test_Topic'));
  assert.match(fs.readFileSync(r.html, 'utf8'), /<title>테스트 주제<\/title>/);
  for (const f of ['Main.dc.html', 'canvas.json']) assert.ok(fs.existsSync(path.join(r.dir, f)), f);
  assert.match(JSON.parse(fs.readFileSync(path.join(r.dir, 'canvas.json'), 'utf8')).title, /테스트 주제/);
});

test('existing html moves to the next number', () => {
  const { src, dest } = setup();
  fs.writeFileSync(path.join(dest, '인터렉티브_01.html'), 'x');
  assert.equal(save({ src, dest, name: 'Test_Topic' }).nn, '02');
  assert.equal(fs.readFileSync(path.join(dest, '인터렉티브_01.html'), 'utf8'), 'x');
});

test('skips a number whose data folder exists', () => {
  const { src, dest } = setup();
  fs.writeFileSync(path.join(dest, '인터렉티브_01.html'), 'x');
  fs.mkdirSync(path.join(dest, '.pack', '자료_인터렉티브_02'), { recursive: true });
  assert.equal(save({ src, dest, name: 'Test_Topic' }).nn, '03');
});

test('creates a missing dest', () => {
  const { tmp, src } = setup();
  const d = path.join(tmp, 'new', '1010');
  assert.equal(save({ src, dest: d, name: 'Test_Topic' }).nn, '01');
  assert.ok(fs.existsSync(path.join(d, '인터렉티브_01_Test_Topic.html')));
});

test('writes nothing next to the source', () => {
  const { src, dest } = setup();
  const before = fs.readdirSync(path.dirname(src)).sort();
  save({ src, dest, name: 'Test_Topic' });
  assert.deepEqual(fs.readdirSync(path.dirname(src)).sort(), before);
});

test('two saves in a row get 01 and 02', () => {
  const { src, dest } = setup();
  assert.equal(save({ src, dest, name: 'Test_Topic' }).nn, '01');
  assert.equal(save({ src, dest, name: 'Test_Topic' }).nn, '02');
});

test('cli prints the result and exits 2 on bad input', () => {
  const { src, dest } = setup();
  const ok = spawnSync(process.execPath, [SCRIPT, src, dest, 'Test_Topic'], { encoding: 'utf8' });
  assert.equal(ok.status, 0, ok.stderr);
  assert.equal(JSON.parse(ok.stdout).nn, '01');
  assert.equal(spawnSync(process.execPath, [SCRIPT, src], { encoding: 'utf8' }).status, 2);
  assert.equal(spawnSync(process.execPath, [SCRIPT, src, dest], { encoding: 'utf8' }).status, 2);
  assert.equal(spawnSync(process.execPath, [SCRIPT, '/no/such/Main.dc.html', dest, 'Test_Topic'], { encoding: 'utf8' }).status, 2);
});

test('a failed save leaves no numbered folder', () => {
  const { tmp, dest } = setup();
  assert.throws(() => save({ src: path.join(tmp, 'run', '1'), dest, name: 'Test_Topic' }));
  assert.deepEqual(fs.readdirSync(dest), []);
  const bad = path.join(tmp, 'bad.dc.html');
  fs.writeFileSync(bad, '<title>x</title>');
  assert.throws(() => save({ src: bad, dest, name: 'Test_Topic' }));
  assert.deepEqual(fs.readdirSync(dest), []);
});

test('cli rejects a folder as the source', () => {
  const { tmp, dest } = setup();
  const r = spawnSync(process.execPath, [SCRIPT, path.join(tmp, 'run', '1'), dest, 'Test_Topic'], { encoding: 'utf8' });
  assert.equal(r.status, 2);
  assert.deepEqual(fs.readdirSync(dest), []);
});

test('numbers count files that already have a name', () => {
  const { src, dest } = setup();
  fs.writeFileSync(path.join(dest, '인터렉티브_01_Lac_Operon.html'), 'x');
  fs.mkdirSync(path.join(dest, '.pack', '자료_인터렉티브_02_Translation'), { recursive: true });
  const r = save({ src, dest, name: 'Test_Topic' });
  assert.equal(r.nn, '03');
  assert.equal(path.basename(r.html), '인터렉티브_03_Test_Topic.html');
});

test('spaces in the name become underscores', () => {
  const { src, dest } = setup();
  const r = save({ src, dest, name: '  Transcription and  RNA Processing ' });
  assert.equal(path.basename(r.html), '인터렉티브_01_Transcription_and_RNA_Processing.html');
  assert.equal(path.basename(r.dir), '자료_인터렉티브_01_Transcription_and_RNA_Processing');
});

test('rejects a missing or unsafe name and writes nothing', () => {
  const { src, dest } = setup();
  for (const name of [undefined, '', '   ', 'a/b', '../x', 'a:b'])
    assert.throws(() => save({ src, dest, name }), /name/, String(name));
  assert.deepEqual(fs.readdirSync(dest), []);
});

test('a Korean name with English proper nouns is kept as written', () => {
  const { src, dest } = setup();
  const r = save({ src, dest, name: '전사와 RNA 가공' });
  assert.equal(path.basename(r.html), '인터렉티브_01_전사와_RNA_가공.html');
});

test('save puts the data folder under .pack', () => {
  const { src, dest } = setup();
  const r = save({ src, dest, name: '전사' });
  assert.equal(nfc(path.relative(dest, r.dir)), '.pack/자료_인터렉티브_01_전사');
  assert.match(fs.readFileSync(r.html, 'utf8'), /생성 파일: \.pack\/자료_인터렉티브_01_전사\/Main\.dc\.html/);
  assert.deepEqual(fs.readdirSync(dest).map(nfc).sort(), ['.pack', '인터렉티브_01_전사.html']);
});
