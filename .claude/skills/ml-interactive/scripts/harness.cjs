// Loads the x-dc script of a .dc.html file into a vm sandbox with a DCLogic stub,
// so tests and check.cjs can drive a component without a browser.
const fs = require('node:fs');
const vm = require('node:vm');

function readDc(file) {
  return fs.readFileSync(file, 'utf8');
}

function markupPart(file) {
  const html = readDc(file);
  return html.slice(0, html.indexOf('data-dc-script'));
}

function makeStorage(store, mode) {
  if (mode === 'throw') {
    const boom = () => { throw new Error('storage blocked'); };
    return { getItem: boom, setItem: boom, removeItem: boom };
  }
  return {
    getItem: (k) => (Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; },
  };
}

function loadComponent(file, opts = {}) {
  const src = readDc(file).match(/<script type="text\/x-dc"[^>]*>([\s\S]*?)<\/script>/)[1];
  class DCLogic {
    constructor(props) { this.props = props || {}; this.state = {}; }
    setState(u) { this.state = Object.assign({}, this.state, typeof u === 'function' ? u(this.state) : u); }
  }
  const store = opts.storage && opts.storage !== 'throw' ? opts.storage : {};
  const win = {
    matchMedia: (q) => ({
      matches: q.includes('prefers-color-scheme: dark') ? !!opts.systemDark
        : q.includes('max-width: 1023.98px') ? !!opts.narrow
        : q.includes('prefers-reduced-motion') ? !!opts.reduceMotion : false,
    }),
    localStorage: makeStorage(store, opts.storage),
    devicePixelRatio: 1,
    innerWidth: opts.innerWidth || 1440,
    addEventListener() {}, removeEventListener() {},
  };
  const ctx = vm.createContext({ MLMath:require('../assets/ml-math.js'), DCLogic, window: win, requestAnimationFrame: opts.raf || (() => 0), cancelAnimationFrame() {}, console, ...(opts.document ? { document: opts.document } : {}) });
  vm.runInContext(src + '\n;globalThis.__C = Component;', ctx);
  const c = new ctx.__C({});
  return { c, store, win };
}

// Canvas 2D stub that records every method call with the styles current at call time.
function makeCtx() {
  const calls = [];
  const target = { fillStyle: '', strokeStyle: '', globalAlpha: 1, lineWidth: 1, font: '', textAlign: '', textBaseline: '', lineCap: '' };
  const ctx = new Proxy(target, {
    get(t, prop) {
      if (prop in t) return t[prop];
      if (typeof prop !== 'string') return undefined;
      return (...args) => {
        calls.push({ op: prop, args, fillStyle: t.fillStyle, strokeStyle: t.strokeStyle, alpha: t.globalAlpha });
        if (prop === 'createRadialGradient' || prop === 'createLinearGradient') return { addColorStop() {} };
        if (prop === 'measureText') return { width: 10 };
        return undefined;
      };
    },
    set(t, prop, v) { t[prop] = v; return true; },
  });
  return { ctx, calls };
}

function makeCanvas(ctx, w = 800, h = 600) {
  return {
    clientWidth: w, clientHeight: h, width: w, height: h, style: {},
    getContext: () => ctx,
    addEventListener() {}, removeEventListener() {}, setPointerCapture() {},
    getBoundingClientRect: () => ({ left: 0, top: 0 }),
  };
}

module.exports = { readDc, markupPart, loadComponent, makeCtx, makeCanvas };
