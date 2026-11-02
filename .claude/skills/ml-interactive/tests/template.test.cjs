const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { loadComponent, makeCtx, makeCanvas, markupPart } = require('../scripts/harness.cjs');

const T = path.join(__dirname, '..', 'assets', 'template.dc.html');

const MIXED = `STEPS: [
        { mode: 'a', c: '#4A86E8', title: 'A1', who: '구조', text: 'a 첫째' },
        { mode: 'b', f: 6, phase: '진행', c: '#E5604F', title: 'B1', who: '과정', text: 'b 첫째' },
        { mode: 'a', c: '#4A86E8', title: 'A2', who: '구조', text: 'a 둘째' },
        { mode: 'b', f: 8, phase: '진행', c: '#E5604F', title: 'B2', who: '과정', text: 'b 둘째' }
      ],`;
const ONLY_B = `STEPS: [
        { mode: 'b', f: 6, phase: '진행', c: '#E5604F', title: '여섯 번째 구', who: '과정', text: '재생하면 구가 왼쪽부터 하나씩 나타나요. 여기서는 6개까지 나왔어요.' }
      ],`;

function withSteps(steps) {
  const src = fs.readFileSync(T, 'utf8');
  const out = src.replace(/STEPS: \[[\s\S]*?\n      \],/, steps);
  assert.notEqual(out, src, 'mutation changed nothing');
  const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'bi-tpl-')), 'Main.dc.html');
  fs.writeFileSync(file, out);
  return file;
}

function drawFrames(c, n, w, h) {
  const { ctx, calls } = makeCtx();
  c.attachCanvas(makeCanvas(ctx, w, h));
  for (let k = 1; k <= n; k++) c.draw(0.016, k * 16);
  return calls;
}

test('modes render as buttons and switch', () => {
  const { c } = loadComponent(T);
  let v = c.renderVals();
  assert.deepEqual(v.modes.map((m) => m.label), ['구조', '과정']);
  assert.equal(v.hasPlayback, false);
  v.modes[1].pick();
  v = c.renderVals();
  assert.equal(c.state.mode, 'b');
  assert.equal(v.modes[1].pressed, 'true');
  assert.equal(v.modes[0].pressed, 'false');
  assert.equal(v.hasPlayback, true);
});

test('wide opens both panels; narrow starts closed and Escape closes the drawer', () => {
  const wide = loadComponent(T, { narrow: false }).c.renderVals();
  assert.equal(wide.leftCls, 'is-open');
  assert.equal(wide.rightCls, 'is-open');
  const { c } = loadComponent(T, { narrow: true });
  let v = c.renderVals();
  assert.equal(v.leftCls, '');
  assert.equal(v.rightCls, '');
  v.toggleRight();
  v = c.renderVals();
  assert.equal(v.rightCls, 'is-open');
  assert.equal(v.scrimCls, 'is-on');
  v.onKey({ key: 'Escape' });
  assert.equal(c.renderVals().scrimCls, '');
});

test('theme is saved to od-theme', () => {
  const { c, store } = loadComponent(T);
  c.setTheme('dark');
  assert.equal(store['od-theme'], 'dark');
  assert.equal(c.renderVals().isDark, true);
});

test('blocked storage still loads', () => {
  assert.doesNotThrow(() => {
    const { c } = loadComponent(T, { storage: 'throw' });
    c.renderVals();
    c.setTheme('dark');
  });
});

test('reduced motion turns auto spin off', () => {
  assert.equal(loadComponent(T, { reduceMotion: true }).c.state.spin, false);
  assert.equal(loadComponent(T).c.state.spin, true);
});

test('draw paints every mode', () => {
  const { c } = loadComponent(T);
  for (const m of c.topic().MODES) {
    c.setMode(m.key);
    const calls = drawFrames(c, 10);
    assert.ok(calls.some((x) => x.op === 'arc'), m.key);
  }
});

test('zero-size canvas draws nothing and does not throw', () => {
  const { c } = loadComponent(T);
  let calls;
  assert.doesNotThrow(() => { calls = drawFrames(c, 3, 0, 0); });
  assert.equal(calls.some((x) => x.op === 'arc'), false);
});

test('playback advances to fmax and stops', () => {
  const { c } = loadComponent(T);
  c.setMode('b');
  const { ctx } = makeCtx();
  c.attachCanvas(makeCanvas(ctx));
  c.setState({ playing: true });
  for (let k = 1; k <= 2000; k++) c.tick(16 * k);
  assert.equal(c.state.f, 10);
  assert.equal(c.state.playing, false);
});

test('non-rotatable mode ignores drag', () => {
  const { c } = loadComponent(T);
  c.setMode('b');
  const { ctx } = makeCtx();
  c.attachCanvas(makeCanvas(ctx));
  const before = { yaw: c.cam.yaw, pitch: c.cam.pitch };
  c._pd({ clientX: 0, clientY: 0, pointerId: 1 });
  c._pm({ clientX: 100, clientY: 50 });
  assert.deepEqual({ yaw: c.cam.yaw, pitch: c.cam.pitch }, before);
  c.setMode('a');
  c._pd({ clientX: 0, clientY: 0, pointerId: 1 });
  c._pm({ clientX: 100, clientY: 50 });
  assert.notEqual(c.cam.yaw, c.topic().MODES[0].cam.yaw);
});

test('scrub and step pick move f', () => {
  const { c } = loadComponent(T);
  c.setMode('b');
  c.renderVals().onScrub({ target: { value: '50' } });
  assert.equal(c.state.f, 5);
  c.setMode('a');
  c.setState({ playing: true });
  const S = c.topic().STEPS[1];
  c.pickStep(1);
  assert.equal(c.state.mode, S.mode);
  assert.equal(c.state.f, S.f);
  assert.equal(c.state.playing, false);
  const v = c.renderVals();
  assert.equal(v.steps[0].pressed, 'true');
  assert.equal(v.stepDetail, S.text);
});

test('pickStep switches mode and moves f', () => {
  const { c } = loadComponent(T);
  const S = c.topic().STEPS[1];
  c.setMode('a');
  c.setState({ playing: true });
  c.pickStep(1);
  assert.equal(c.state.mode, S.mode);
  assert.equal(c.state.f, S.f);
  assert.equal(c.state.playing, false);
  assert.equal(c.state.step, 1);
  assert.equal(c.renderVals().stepDetail, S.text);
});

test('steps are filtered and renumbered per mode', () => {
  const { c } = loadComponent(withSteps(MIXED));
  assert.deepEqual(c.renderVals().steps.map((s) => [s.num, s.title]), [[1, 'A1'], [2, 'A2']]);
  c.setMode('b');
  assert.deepEqual(c.renderVals().steps.map((s) => [s.num, s.title]), [[1, 'B1'], [2, 'B2']]);
  c.renderVals().steps[1].pick();
  assert.equal(c.state.step, 3);
  assert.equal(c.state.f, 8);
});

test('pressed follows the global step index', () => {
  const { c } = loadComponent(T);
  c.pickStep(1);
  assert.deepEqual(c.renderVals().steps.map((s) => s.pressed), ['true']);
  c.setMode('a');
  assert.deepEqual(c.renderVals().steps.map((s) => s.pressed), ['false']);
});

test('mode without steps hides the section', () => {
  const { c } = loadComponent(withSteps(ONLY_B));
  c.setMode('a');
  const v = c.renderVals();
  assert.equal(v.hasSteps, false);
  assert.equal(v.hasStep, false);
  assert.deepEqual(v.steps, []);
});

test('placeholders and slots are present', () => {
  const m = markupPart(T);
  assert.equal(m.split('__TITLE__').length - 1, 2);
  for (const s of ['<!-- SLOT:left -->', '<!-- SLOT:right -->']) assert.ok(m.includes(s), s);
  assert.equal(m.includes('@font-face'), false);
});

test('first section in each panel has no divider', () => {
  // A slot often wraps its sections in a bare <div>; that first section counts too.
  const rule = markupPart(T).match(/\.panel-head \+ \.sec,\.panel-head \+ div > \.sec:first-child\{([^}]*)\}/);
  assert.ok(rule, '.panel-head + .sec and wrapped first .sec rule');
  assert.ok(rule[1].includes('border-top:0'), rule[1]);
});

test('template has no source line', () => {
  const m = markupPart(T);
  assert.equal(m.includes('class="source"'), false);
  assert.equal(m.includes('__SOURCE__'), false);
});

test('flat scene is not fogged', () => {
  const { c } = loadComponent(T);
  c.setMode('b');
  c.renderVals().onScrub({ target: { value: '50' } });
  const calls = drawFrames(c, 1);
  const arcs = calls.filter((x) => x.op === 'arc');
  assert.ok(Math.max(...arcs.map((x) => x.alpha)) > 0.99);
});

test('a scene error is logged once, not swallowed', (t) => {
  const fs = require('node:fs'), os = require('node:os');
  const src = fs.readFileSync(T, 'utf8').replace(/buildScene\(mode, I, O\) \{/, '$& throw new Error("boom");');
  const f = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'bi-tpl-')), 'x.dc.html');
  fs.writeFileSync(f, src);
  const { c } = loadComponent(f);
  const { ctx } = makeCtx();
  c.attachCanvas(makeCanvas(ctx));
  const err = t.mock.method(console, 'error', () => {});
  for (let k = 1; k <= 3; k++) c.tick(16 * k);
  assert.equal(err.mock.callCount(), 1);
});

test('picking the active mode keeps progress', () => {
  const { c } = loadComponent(T);
  c.setMode('b');
  c.renderVals().onScrub({ target: { value: '50' } });
  c.renderVals().modes[1].pick();
  assert.equal(c.state.f, 5);
  c.renderVals().modes[0].pick();
  assert.equal(c.state.mode, 'a');
  assert.equal(c.state.f, 0);
});

test('theme tokens include scroll colors', () => {
  const { c } = loadComponent(T);
  const { light, dark } = c.K.THEMES;
  for (const th of [light, dark]) for (const k of ['scroll', 'scrollHover']) assert.match(th[k] || '', /^#[0-9a-f]{6}$/i, k);
  assert.notEqual(light.scroll, dark.scroll);
  assert.notEqual(light.scrollHover, dark.scrollHover);
});

test('number input uses theme tokens', () => {
  const rule = markupPart(T).match(/\.app input\[type="number"\]\{([^}]*)\}/);
  assert.ok(rule, 'number input rule');
  for (const s of ['background:var(--bg)', 'color:var(--ink)', 'border:1px solid var(--line)', 'min-height:44px', 'font:inherit']) assert.ok(rule[1].includes(s), s);
});

test('panel scrollbar uses theme tokens', () => {
  const m = markupPart(T);
  for (const s of ['--scroll: {{th.scroll}}', '--scroll-hover: {{th.scrollHover}}', 'scrollbar-color:var(--scroll) transparent',
    '.panel-inner::-webkit-scrollbar-thumb{background:var(--scroll)', '.panel-inner::-webkit-scrollbar-thumb:hover{background:var(--scroll-hover)}'])
    assert.ok(m.includes(s), s);
});
