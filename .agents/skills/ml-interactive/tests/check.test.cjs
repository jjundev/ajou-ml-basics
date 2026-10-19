const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { check } = require('../scripts/check.cjs');

const SKILL = path.join(__dirname, '..');
const T = path.join(SKILL, 'assets', 'template.dc.html');
const A = { allowTemplate: true };
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'bi-check-'));
let n = 0;

function mutate(fn) {
  const src = fs.readFileSync(T, 'utf8');
  const out = fn(src);
  assert.notEqual(out, src, 'mutation changed nothing');
  const p = path.join(TMP, 'm' + (n++) + '.dc.html');
  fs.writeFileSync(p, out);
  return p;
}

test('template passes with allowTemplate', () => {
  const r = check(T, A);
  assert.deepEqual(r.errors, []);
  assert.equal(r.ok, true);
});

test('template left as-is is rejected', () => {
  const r = check(T);
  assert.equal(r.ok, false);
  for (const e of ['TEMPLATE_LEFT:__TITLE__', 'TEMPLATE_LEFT:DEMO']) assert.ok(r.errors.includes(e), e);
});

test('missing shell piece', () => assert.ok(check(mutate((s) => s.replace('class="scrim', 'class="dim')), A).errors.includes('SHELL_MISSING:class="scrim')));

test('unknown hole', () => assert.ok(check(mutate((s) => s.replace('{{themeLabel}}"', '{{themLabel}}"')), A).errors.includes('HOLE_UNKNOWN:themLabel')));

test('loop variable outside its sc-for is unknown', () => {
  const r = check(mutate((s) => s.replace('<summary>꼭 기억할 점</summary>', '<summary>꼭 기억할 점</summary>{{md.label}}')), A);
  assert.ok(r.errors.includes('HOLE_UNKNOWN:md'));
});

test('unsupported event', () => assert.ok(check(mutate((s) => s.replace('onClick="{{zoomIn}}"', 'onDoubleClick="{{zoomIn}}"')), A).errors.includes('EVENT_UNSUPPORTED:onDoubleClick')));

test('raw hex in markup', () => assert.ok(check(mutate((s) => s.replace('<div class="scrim', '<div style="color:#123456" class="scrim')), A).errors.includes('HEX_IN_MARKUP:#123456')));

test('scene that throws', () => assert.ok(check(mutate((s) => s.replace(/buildScene\(mode, I, O\) \{/, '$& if (mode === "b") throw new Error("x");')), A).errors.includes('DRAW_THROWS:b')));

test('scene that throws late in playback', () => assert.ok(check(mutate((s) => s.replace(/buildScene\(mode, I, O\) \{/, '$& if (this.sim.f > 9) throw new Error("x");')), A).errors.includes('DRAW_THROWS:b')));

test('scene that throws in dark only', () => {
  const r = check(mutate((s) => s.replace("link: '#AEB7C4'", 'link: null')), A);
  assert.ok(r.errors.includes('DRAW_THROWS:a'), r.errors.join());
});

test('empty scene', () => assert.ok(check(mutate((s) => s.replace(/buildScene\(mode, I, O\) \{/, '$& return;')), A).errors.includes('SCENE_EMPTY:a')));

test('renderVals that throws', () => {
  const r = check(mutate((s) => s.replace(/extraVals\(st\) \{/, '$& if (st.narrow && st.theme === "dark") throw new Error("x");')), A);
  assert.ok(r.errors.includes('RENDER_THROWS:narrow-dark-a'), r.errors.join());
  assert.equal(r.errors.includes('RENDER_THROWS:wide-light-a'), false);
});

test('cli exit codes', () => {
  const cli = path.join(SKILL, 'scripts', 'check.cjs');
  const ok = spawnSync('node', [cli, T, '--allow-template'], { encoding: 'utf8' });
  assert.equal(ok.status, 0);
  assert.equal(ok.stdout.trim(), 'ok');
  const bad = spawnSync('node', [cli, T], { encoding: 'utf8' });
  assert.equal(bad.status, 1);
  assert.match(bad.stdout, /TEMPLATE_LEFT:DEMO/);
});

test('hole syntax the runtime cannot parse', () => {
  const r1 = check(mutate((s) => s.replace('<sc-if value="{{hasSteps}}"', '<sc-if value="{{!hasSteps}}"')), A);
  assert.ok(r1.errors.includes('HOLE_SYNTAX:!hasSteps'), r1.errors.join());
  const r2 = check(mutate((s) => s.replace('<summary>꼭 기억할 점</summary>', '<summary>꼭 기억할 점</summary>{{isPlaying ? 1 : 2}}')), A);
  assert.ok(r2.errors.includes('HOLE_SYNTAX:isPlaying ? 1 : 2'), r2.errors.join());
  const r3 = check(mutate((s) => s.replace('onClick="{{zoomIn}}"', 'onClick="x{{zoomIn}}"')), A);
  assert.ok(r3.errors.includes('HOLE_SYNTAX:onClick'), r3.errors.join());
});

test('errors carry the exception message', () => {
  const f = mutate((s) => s.replace(/buildScene\(mode, I, O\) \{/, '$& if (mode === "b") throw new Error("boom here");'));
  const r = check(f, A);
  assert.ok(r.errors.includes('DRAW_THROWS:b'));
  assert.ok(r.details.some((d) => d.startsWith('DRAW_THROWS:b') && d.includes('boom here')), r.details.join());
  const out = spawnSync('node', [path.join(SKILL, 'scripts', 'check.cjs'), f, '--allow-template'], { encoding: 'utf8' });
  assert.match(out.stdout, /DRAW_THROWS:b .*boom here/);
});

test('a hole whose full path is undefined in every mode', () => {
  const r = check(mutate((s) => s.replace('<sc-if value="{{is.b}}"', '<sc-if value="{{is.cycle}}"')), A);
  assert.ok(r.errors.includes('HOLE_UNKNOWN:is.cycle'), r.errors.join());
  const r2 = check(mutate((s) => s.replace('{{s.title}}', '{{s.titel}}')), A);
  assert.ok(r2.errors.includes('HOLE_UNKNOWN:s.titel'), r2.errors.join());
});

test('step pointing at a missing mode or past fmax', () => {
  const r = check(mutate((s) => s.replace("{ mode: 'b', f: 6,", "{ mode: 'c', f: 6,")), A);
  assert.ok(r.errors.includes('TOPIC_INVALID:STEPS[2].mode'), r.errors.join());
  const r2 = check(mutate((s) => s.replace("{ mode: 'b', f: 6,", "{ mode: 'b', f: 60,")), A);
  assert.ok(r2.errors.includes('TOPIC_INVALID:STEPS[2].f'), r2.errors.join());
});

test('missing mistakes or light palette', () => {
  const r = check(mutate((s) => s.replace("b: [{ title: '예시 문구'", "x: [{ title: '예시 문구'")), A);
  assert.ok(r.errors.includes('TOPIC_INVALID:MISTAKES.b'), r.errors.join());
  const r2 = check(mutate((s) => s.replace("light: { bg: '#ffffff', labelBg", "lite: { bg: '#ffffff', labelBg")), A);
  assert.ok(r2.errors.includes('TOPIC_INVALID:PAL.light'), r2.errors.join());
});

test('a step that breaks the scene when picked', () => {
  const r = check(mutate((s) => s.replace(/buildScene\(mode, I, O\) \{/, '$& if (this.state.step === 0) throw new Error("x");')), A);
  assert.ok(r.errors.includes('DRAW_THROWS:step1'), r.errors.join());
});

test('NaN geometry is a blank scene', () => {
  const r = check(mutate((s) => s.replace("cam: { yaw: 0, pitch: 0, zoom: 1 }, fit: [12.5, 5]", "cam: { yaw: 0, pitch: 0 }, fit: [12.5, 5]")), A);
  assert.ok(r.errors.includes('SCENE_NAN:b'), r.errors.join());
});

test('step with f but no phase', () => {
  const r = check(mutate((s) => s.replace(", phase: '진행'", '')), A);
  assert.ok(r.errors.includes('TOPIC_INVALID:STEPS[2].phase'), r.details.join('\n'));
});

test('step whose phase is not in the playback label', () => {
  const r = check(mutate((s) => s.replace("phase: '진행'", "phase: '연장'")), A);
  assert.ok(r.errors.includes('STEP_OFF_PHASE:2'), r.details.join('\n'));
  assert.ok(r.details.some((d) => d.startsWith('STEP_OFF_PHASE:2 — ') && d.includes("'연장'") && d.includes('진행 · 6.0 / 10')), r.details.join('\n'));
});

test('label that throws is reported as STEP_OFF_PHASE', () => {
  const r = check(mutate((s) => s.replace("label: (f) => '진행 · '", "label: (f) => f > 5 ? null.x : '진행 · '")), A);
  assert.ok(r.details.some((d) => d.startsWith('STEP_OFF_PHASE:2 — ')), r.details.join('\n'));
});

test('phase check skips a step whose f is already invalid', () => {
  const r = check(mutate((s) => s.replace('f: 6,', 'f: 60,')), A);
  assert.ok(r.errors.includes('TOPIC_INVALID:STEPS[2].f'), r.details.join('\n'));
  assert.ok(!r.errors.some((e) => e.startsWith('STEP_OFF_PHASE')), r.details.join('\n'));
});

test('phase that is only part of the process name is off phase', () => {
  const r = check(mutate((s) => s.replace("phase: '진행'", "phase: '진'")), A);
  assert.ok(r.errors.includes('STEP_OFF_PHASE:2'), r.details.join('\n'));
});

test('blank phase is missing', () => {
  const r = check(mutate((s) => s.replace("phase: '진행'", "phase: ' '")), A);
  assert.ok(r.errors.includes('TOPIC_INVALID:STEPS[2].phase'), r.details.join('\n'));
});

test('phase may be any named part of a nested label', () => {
  const r = check(mutate((s) => s.replace("label: (f) => '진행 · '", "label: (f) => '첫 구간 · 진행 · '")), A);
  assert.ok(!r.errors.some((e) => e.startsWith('STEP_OFF_PHASE')), r.details.join('\n'));
});
