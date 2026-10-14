// Checks a topic's Main.dc.html against the template contract (references/scene-api.md).
// Usage: node check.cjs <Main.dc.html> [--allow-template]   → prints "ok" (exit 0) or one error per line (exit 1)
// check() returns {ok, errors: codes, details: the same codes with the exception message when there was one}.
const fs = require('node:fs');
const { readDc, loadComponent, makeCtx, makeCanvas } = require('./harness.cjs');

const SHELL = ['class="app"', 'class="topbar"', 'class="layout', 'panel panel-left', 'panel panel-right', 'class="scrim',
  'class="stage"', 'ref="{{canvasRef}}"', 'class="view-btns"', '@media (max-width: 1023.98px)', 'aria-label="{{themeLabel}}"'];
const EVENTS = ['onClick', 'onKeyDown', 'onMouseEnter', 'onMouseLeave', 'onChange'];
const FRAMES = 120;

// Markup between </helmet> and </x-dc>: the part the runtime compiles.
function bodyMarkup(src) {
  return src.slice(src.indexOf('</helmet>') + '</helmet>'.length, src.indexOf('</x-dc>'));
}

// The runtime only parses {{dotted.path}}; sc-if value, sc-for list, ref and on* must be exactly one hole.
function holeSyntax(markup) {
  const bad = new Set();
  const plain = markup.replace(/\shint-[\w-]+="[^"]*"/g, '');
  for (const m of plain.matchAll(/\{\{([\s\S]*?)\}\}/g)) if (!/^\s*[\w.$]+\s*$/.test(m[1])) bad.add(m[1].trim());
  for (const m of plain.matchAll(/<(sc-if|sc-for)\b[^>]*>|\s(ref|on[A-Za-z]+)="([^"]*)"/g)) {
    const attrs = m[1] ? [...m[0].matchAll(/\s(value|list)="([^"]*)"/g)].map((x) => [x[1], x[2]]) : [[m[2], m[3]]];
    for (const [name, val] of attrs) if (val.includes('{{') && !/^\s*\{\{\s*[\w.$]+\s*\}\}\s*$/.test(val)) bad.add(name);
  }
  return [...bad];
}

const dig = (o, segs) => segs.reduce((x, k) => (x == null ? undefined : x[k]), o);

// Every {{hole}} must resolve: its first name is a renderVals key or an enclosing <sc-for as> name,
// and the full dotted path is defined in at least one checked state (for loop items: in at least one item).
// `vals` is every renderVals() result the render checks produced.
function unknownHoles(markup, vals) {
  const bad = new Set(), scope = [];
  const keys = new Set(vals.flatMap((v) => Object.keys(v)));
  const items = (list) => (list ? vals.flatMap((v) => { const a = dig(v, list); return Array.isArray(a) ? a : []; }) : []);
  // Returns the top-level list path for a loop variable path, or null when it cannot be judged.
  const judge = (path) => {
    const segs = path.split('.'), loop = [...scope].reverse().find((e) => e.as === segs[0]);
    if (loop) {
      const its = items(loop.list);
      if (segs.length > 1 && its.length && its.every((it) => dig(it, segs.slice(1)) === undefined)) bad.add(path);
      return null;
    }
    if (!keys.has(segs[0])) { bad.add(segs[0]); return null; }
    if (segs.length > 1 && vals.every((v) => dig(v, segs) === undefined)) bad.add(path);
    return segs;
  };
  const re = /<sc-for\b[^>]*>|<\/sc-for>|\shint-[\w-]+="[^"]*"|\{\{\s*([\w$.]+)\s*\}\}/g;
  let m;
  while ((m = re.exec(markup))) {
    const tok = m[0];
    if (tok.startsWith('<sc-for')) {
      const list = tok.match(/list="\{\{\s*([\w$.]+)\s*\}\}"/), as = tok.match(/\sas="([\w$]+)"/);
      scope.push({ as: as ? as[1] : '', list: list ? judge(list[1]) : null });
    } else if (tok === '</sc-for>') scope.pop();
    else if (m[1]) judge(m[1]);
  }
  return [...bad];
}

// Topic data the shell relies on. Steps are numbered from 1 in STEPS order.
// A step with f names its phase: the process name the playback label shows at that f
// (one whole ' · ' part of a '<과정 이름> · f / fmax' label, so '억제자' does not pass on '억제자 이동').
function topicChecks(topic, add) {
  const modes = topic.MODES || [];
  for (const m of modes) for (const k of ['cam', 'fit', 'D', 'canvasLabel']) if (m[k] == null) add('TOPIC_INVALID:MODES.' + m.key + '.' + k);
  (topic.STEPS || []).forEach((s, i) => {
    const n = i + 1, m = modes.find((d) => d.key === s.mode);
    if (!m) add('TOPIC_INVALID:STEPS[' + n + '].mode');
    else if (s.f != null && (!m.playback || !(s.f >= 0 && s.f <= m.playback.fmax))) add('TOPIC_INVALID:STEPS[' + n + '].f');
    else if (s.f != null) phaseCheck(s, n, m.playback, add);
  });
  for (const m of modes) {
    const list = topic.MISTAKES && topic.MISTAKES[m.key];
    if (!Array.isArray(list) || !list.length) add('TOPIC_INVALID:MISTAKES.' + m.key);
  }
  for (const t of ['light', 'dark']) if (!topic.PAL || !topic.PAL[t]) add('TOPIC_INVALID:PAL.' + t);
}

function phaseCheck(s, n, playback, add) {
  const phase = typeof s.phase === 'string' ? s.phase.trim() : '';
  if (!phase) return add('TOPIC_INVALID:STEPS[' + n + '].phase');
  let label;
  try {
    label = String(playback.label(s.f));
  } catch (e) {
    return add('STEP_OFF_PHASE:' + n, e);
  }
  const parts = label.split(' · ').map((x) => x.trim());
  if (parts.length > 1 ? !parts.includes(phase) : !label.includes(phase)) add('STEP_OFF_PHASE:' + n, "기대 '" + s.phase + "', 실제 '" + label + "'");
}

function renderChecks(file, modes, add) {
  const vals = [];
  for (const narrow of [true, false]) {
    for (const theme of ['light', 'dark']) {
      for (const mode of modes) {
        try {
          const { c } = loadComponent(file, { narrow });
          c.setTheme(theme);
          c.setMode(mode);
          vals.push(c.renderVals());
        } catch (e) {
          add('RENDER_THROWS:' + (narrow ? 'narrow' : 'wide') + '-' + theme + '-' + mode, e);
        }
      }
    }
  }
  return vals;
}

// Draws each mode directly (tick() swallows exceptions): sweeps playback 0→fmax and the
// camera around, light then dark, then each view option flipped once. Non-finite numbers
// reaching the canvas mean a blank scene (e.g. a missing cam.zoom).
const nonFinite = (calls) => calls.some((x) => x.args.some((a) => typeof a === 'number' && !Number.isFinite(a)));

function drawChecks(file, modes, add) {
  for (const mode of modes) {
    let c, calls, last = 0;
    try {
      ({ c } = loadComponent(file, { narrow: false }));
      c.setMode(mode);
      const made = makeCtx();
      calls = made.calls;
      c.attachCanvas(makeCanvas(made.ctx, 800, 600));
    } catch (e) {
      add('DRAW_THROWS:' + mode, e);
      continue;
    }
    const pb = c.modeDef(mode).playback;
    try {
      if (pb) c.setState({ playing: true });
      for (let k = 0; k < FRAMES; k++) {
        if (k === FRAMES / 2) c.setTheme('dark');
        if (pb) { c.sim.f = pb.fmax * k / (FRAMES - 1); c.setState({ f: c.sim.f }); }
        c.cam.yaw += 0.05;
        last = calls.length;
        c.draw(0.016, (k + 1) * 16);
      }
      const end = calls.slice(last);
      if (!end.some((x) => x.op === 'arc' || x.op === 'lineTo' || x.op === 'fillText')) add('SCENE_EMPTY:' + mode);
      if (nonFinite(calls)) add('SCENE_NAN:' + mode);
      for (const t of c.renderVals().toggles) {
        t.toggle();
        c.draw(0.016, 0);
        c.renderVals().toggles.find((x) => x.label === t.label).toggle();
      }
    } catch (e) {
      add('DRAW_THROWS:' + mode, e);
    }
  }
}

// Picks each step from a fresh component and draws the frame it jumps to.
function stepChecks(file, add) {
  let c;
  try {
    ({ c } = loadComponent(file, { narrow: false }));
    c.attachCanvas(makeCanvas(makeCtx().ctx, 800, 600));
  } catch (e) { return; }
  const n = (c.T.STEPS || []).length;
  for (let i = 0; i < n; i++) {
    try {
      c.pickStep(i);
      c.renderVals();
      c.draw(0.016, 0);
    } catch (e) {
      add('DRAW_THROWS:step' + (i + 1), e);
    }
  }
}

function check(file, opts = {}) {
  const errors = [], details = [];
  const add = (code, e) => {
    if (errors.includes(code)) return;
    errors.push(code);
    details.push(e ? code + ' — ' + String((e && e.message) || e).split('\n')[0] : code);
  };
  const src = readDc(file);
  const head = src.slice(0, src.indexOf('data-dc-script'));
  const markup = bodyMarkup(src);

  for (const s of SHELL) if (!head.includes(s)) add('SHELL_MISSING:' + s);
  for (const m of markup.matchAll(/\s(on[A-Z]\w*)=/g)) if (!EVENTS.includes(m[1])) add('EVENT_UNSUPPORTED:' + m[1]);
  for (const h of holeSyntax(markup)) add('HOLE_SYNTAX:' + h);
  for (const m of markup.matchAll(/(?<!&)#[0-9a-fA-F]{6}(?![0-9a-fA-F])/g)) add('HEX_IN_MARKUP:' + m[0]);

  let topic;
  try {
    topic = loadComponent(file).c.topic();
  } catch (e) {
    add('RENDER_THROWS:load', e);
    return { ok: false, errors, details };
  }
  topicChecks(topic, add);
  const modes = topic.MODES.map((m) => m.key);
  const vals = renderChecks(file, modes, add);
  for (const h of unknownHoles(markup, vals)) add('HOLE_UNKNOWN:' + h);
  drawChecks(file, modes, add);
  stepChecks(file, add);
  const finiteTree=v=>typeof v==='number'?Number.isFinite(v):Array.isArray(v)?v.every(finiteTree):v&&typeof v==='object'?Object.values(v).every(finiteTree):true;
  (topic.PRESETS||[{}]).forEach((preset,i)=>{
    try{const {c}=loadComponent(file);c.setState(preset);if(c.compute&&!finiteTree(c.compute(c.state)))add('RESULT_NAN:'+i);
      for(const mode of modes){c.setMode(mode);c.setState(preset);c.renderVals();const made=makeCtx();c.attachCanvas(makeCanvas(made.ctx));c.draw(.016,0);if(nonFinite(made.calls))add('RESULT_NAN:'+i);}
    }catch(e){add('INPUT_THROWS:'+i,e);}
  });

  if (!opts.allowTemplate) {
    for (const p of ['__TITLE__']) if (src.includes(p)) add('TEMPLATE_LEFT:' + p);
    if (topic.DEMO === true) add('TEMPLATE_LEFT:DEMO');
  }
  return { ok: errors.length === 0, errors, details };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const file = args.find((a) => !a.startsWith('--'));
  if (!file || !fs.existsSync(file)) {
    console.error('usage: node check.cjs <Main.dc.html> [--allow-template]');
    process.exit(2);
  }
  const r = check(file, { allowTemplate: args.includes('--allow-template') });
  console.log(r.ok ? 'ok' : r.details.join('\n'));
  process.exit(r.ok ? 0 : 1);
}

module.exports = { check };
