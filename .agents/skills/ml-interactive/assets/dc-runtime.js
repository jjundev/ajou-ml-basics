// Minimal x-dc runtime for opening the canvas component as a plain HTML page.
// Supports what Main.dc.html uses: {{dotted.path}} holes in text and attributes,
// event attributes (onClick, onKeyDown, onMouseEnter, onMouseLeave, onChange),
// callback ref, <sc-if value> and <sc-for list as>.
const DC_EVENTS = { onclick: 'click', onkeydown: 'keydown', onmouseenter: 'mouseenter', onmouseleave: 'mouseleave', onchange: 'input' };
const DC_HOLE = /\{\{\s*([\w.$]+)\s*\}\}/g;
let dcSchedule = () => {};

class DCLogic {
  constructor(props) { this.props = props || {}; this.state = {}; }
  setState(u) {
    this.state = Object.assign({}, this.state, typeof u === 'function' ? u(this.state) : u);
    dcSchedule();
  }
}

function dcGet(scope, path) {
  let o = scope;
  for (const k of path.split('.')) { if (o == null) return undefined; o = o[k]; }
  return o;
}
function dcInterp(str, scope) {
  return str.replace(DC_HOLE, (_, p) => { const v = dcGet(scope, p); return v == null ? '' : String(v); });
}
function dcSingle(str) {
  const m = str.match(/^\s*\{\{\s*([\w.$]+)\s*\}\}\s*$/);
  return m ? m[1] : null;
}

// Compiles one node in place; pushes updaters that take the current scope.
function dcCompile(node, ups) {
  if (node.nodeType === 3) {
    if (!node.data.includes('{{')) return;
    const src = node.data;
    let last;
    ups.push((s) => { const v = dcInterp(src, s); if (v !== last) { node.data = v; last = v; } });
    return;
  }
  if (node.nodeType !== 1) return;
  const tag = node.tagName.toLowerCase();
  if (tag === 'sc-if' || tag === 'sc-for') { dcBlock(node, tag, ups); return; }
  for (const a of [...node.attributes]) {
    const name = a.name, val = a.value;
    if (name.startsWith('hint-')) { node.removeAttribute(name); continue; }
    if (!val.includes('{{')) continue;
    node.removeAttribute(name);
    if (DC_EVENTS[name]) {
      const p = dcSingle(val);
      let cur;
      node.addEventListener(DC_EVENTS[name], (e) => { const f = dcGet(cur, p); if (typeof f === 'function') f(e); });
      ups.push((s) => { cur = s; });
    } else if (name === 'ref') {
      const p = dcSingle(val);
      let done = false;
      ups.push((s) => { if (!done) { done = true; const f = dcGet(s, p); if (typeof f === 'function') f(node); } });
    } else {
      let last;
      ups.push((s) => {
        const v = dcInterp(val, s);
        if (v === last) return;
        last = v;
        if (name === 'value' && 'value' in node) node.value = v; else node.setAttribute(name, v);
      });
    }
  }
  for (const c of [...node.childNodes]) dcCompile(c, ups);
}

function dcBlock(el, tag, ups) {
  const anchor = document.createComment(tag);
  el.parentNode.replaceChild(anchor, el);
  const tpl = document.createDocumentFragment();
  while (el.firstChild) tpl.appendChild(el.firstChild);
  const make = () => {
    const frag = tpl.cloneNode(true), u = [];
    for (const c of [...frag.childNodes]) dcCompile(c, u);
    return { frag: frag, nodes: [...frag.childNodes], u: u };
  };
  if (tag === 'sc-if') {
    const p = dcSingle(el.getAttribute('value') || '');
    let inst = null;
    ups.push((s) => {
      const on = !!dcGet(s, p);
      if (!on) { if (inst) { inst.nodes.forEach((n) => n.remove()); inst = null; } return; }
      if (!inst) { inst = make(); anchor.parentNode.insertBefore(inst.frag, anchor); }
      inst.u.forEach((f) => f(s));
    });
  } else {
    const p = dcSingle(el.getAttribute('list') || ''), as = el.getAttribute('as');
    const insts = [];
    ups.push((s) => {
      const list = dcGet(s, p) || [];
      while (insts.length > list.length) insts.pop().nodes.forEach((n) => n.remove());
      while (insts.length < list.length) { const i = make(); anchor.parentNode.insertBefore(i.frag, anchor); insts.push(i); }
      list.forEach((item, k) => { const sc = Object.create(s); sc[as] = item; insts[k].u.forEach((f) => f(sc)); });
    });
  }
}

function mountDC(Component) {
  const comp = new Component({});
  const frag = document.getElementById('dc-template').content.cloneNode(true), ups = [];
  for (const c of [...frag.childNodes]) dcCompile(c, ups);
  const root = document.getElementById('dc-root');
  let pending = false;
  const render = () => { pending = false; const v = comp.renderVals(); ups.forEach((f) => f(v)); };
  dcSchedule = () => { if (!pending) { pending = true; queueMicrotask(render); } };
  root.appendChild(frag);
  render();
  window.addEventListener('pagehide', () => { if (comp.componentWillUnmount) comp.componentWillUnmount(); });
}
