const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { build, canvasJson } = require('../scripts/build.cjs');
const { loadComponent } = require('../scripts/harness.cjs');

const SKILL = path.join(__dirname, '..');
const EX = path.join(SKILL, 'assets', 'template.dc.html');
const PRETENDARD_CDN = '.pack/vendor/ml-interactive/pretendard/pretendard.css';

test('build makes a standalone page from a dc source', () => {
  const h = build(EX, path.join(os.tmpdir(), 'x', '인터렉티브_01.html'));
  for (const s of ['<!doctype html>', '<title>__TITLE__</title>', PRETENDARD_CDN, '<template id="dc-template">', 'class Component extends DCLogic', 'mountDC(Component)', '<meta name="viewport"'])
    assert.ok(h.includes(s), s);
  for (const s of ['/_blob/', 'support.js', '<x-dc>']) assert.equal(h.includes(s), false, s);
});

test('canvasJson names the board and title', () => {
  const j = JSON.parse(canvasJson('세포 호흡'));
  assert.equal(j.title, '세포 호흡');
  assert.equal(j.boards['Main.dc.html'].title, '세포 호흡');
  assert.deepEqual(j.order, ['Main.dc.html']);
});

test('harness loads a dc component', () => {
  const { c } = loadComponent(EX, { narrow: false });
  assert.equal(c.renderVals().leftCls, 'is-open');
});

test('cli writes the page and canvas.json', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'bi-build-'));
  const srcDir = path.join(dir, '자료_인터렉티브_01');
  fs.mkdirSync(srcDir);
  const src = path.join(srcDir, 'Main.dc.html');
  fs.copyFileSync(EX, src);
  const out = path.join(dir, '인터렉티브_01.html');
  const stdout = execFileSync('node', [path.join(SKILL, 'scripts', 'build.cjs'), src, out], { encoding: 'utf8' });
  assert.match(stdout, /^wrote /);
  assert.ok(fs.existsSync(out));
  assert.ok(fs.readFileSync(out, 'utf8').includes('자료_인터렉티브_01/Main.dc.html'));
  assert.equal(JSON.parse(fs.readFileSync(path.join(srcDir, 'canvas.json'), 'utf8')).title, '__TITLE__');
});

test('build uses verified local assets and refuses corrupted vendor',()=>{
 const d=fs.mkdtempSync(path.join(os.tmpdir(),'ml-vendor-'));
 try{
  const {prepareVendor}=require('../scripts/build.cjs');const vendor=prepareVendor(d),out=path.join(d,'preview.html');
  const h=build(EX,out,{vendorDir:vendor});
  for(const m of h.matchAll(/(?:href|src)="([^"{}]+)"/g)){if(m[1].startsWith('#'))continue;assert.ok(!/^https?:/.test(m[1]));assert.ok(fs.existsSync(path.resolve(d,decodeURIComponent(m[1]))),m[1]);}
  fs.writeFileSync(path.join(vendor,'katex/katex.min.js'),'corrupt');assert.throws(()=>prepareVendor(d),/VENDOR_HASH_MISMATCH/);
 }finally{fs.rmSync(d,{recursive:true,force:true});}
});
