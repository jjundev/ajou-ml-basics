// Applies reviewed contextual links without reserializing the surrounding HTML.
// Usage: node link-notes.cjs <manifest.json> [--dry-run]
// Manifest: {notes:[{note:<absolute path>, links:[{sectionId,html,label,before,after,anchorId?}]}]}
const fs = require('node:fs');
const path = require('node:path');

const escapeHtml = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const decodeHtml = s => s.replace(/&(?:amp|quot|apos|lt|gt|#\d+|#x[\da-f]+);/gi, entity => {
  const named = { '&amp;': '&', '&quot;': '"', '&apos;': "'", '&lt;': '<', '&gt;': '>' };
  if (named[entity.toLowerCase()]) return named[entity.toLowerCase()];
  const n = entity.match(/^&#(x[\da-f]+|\d+);$/i)?.[1];
  const cp = n && (n[0].toLowerCase() === 'x' ? parseInt(n.slice(1), 16) : Number(n));
  return cp > 0 && cp <= 0x10ffff ? String.fromCodePoint(cp) : entity;
});
const attrPattern = /\s+([^\s=/>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g;
function attributes(tag) {
  // Browsers keep the first value when an attribute occurs more than once.
  const attrs = {};
  for (const m of tag.matchAll(attrPattern)) {
    const key = m[1].toLowerCase();
    if (!Object.hasOwn(attrs, key)) attrs[key] = decodeHtml(m[2] ?? m[3] ?? m[4] ?? '');
  }
  return attrs;
}

// Offset-based element scan: ignores comments and raw-text script/style contents.
function elements(source) {
  const token = /<!--[\s\S]*?-->|<![^>]*>|<\/?[a-z][a-z\d:-]*\b(?:"[^"]*"|'[^']*'|[^'">])*>/gi;
  const nodes = [], stack = [];
  const voids = new Set('area base br col embed hr img input link meta param source track wbr'.split(' '));
  let m;
  while ((m = token.exec(source))) {
    const tag = m[0];
    if (tag.startsWith('<!')) continue;
    const name = tag.match(/^<\/?([\w:-]+)/)[1].toLowerCase();
    if (tag.startsWith('</')) {
      const i = stack.map(n => n.name).lastIndexOf(name);
      if (i >= 0) { stack[i].end = token.lastIndex; stack.length = i; }
      continue;
    }
    const node = { name, start: m.index, openEnd: token.lastIndex, end: null, attrs: attributes(tag), parent: stack.at(-1) };
    nodes.push(node);
    if (voids.has(name) || /\/>$/.test(tag)) node.end = token.lastIndex;
    else if (['script', 'style', 'textarea', 'title'].includes(name)) {
      const closing = new RegExp('</' + name + '\\s*>', 'gi');
      closing.lastIndex = token.lastIndex;
      const close = closing.exec(source);
      if (close) { node.end = closing.lastIndex; token.lastIndex = closing.lastIndex; }
      else token.lastIndex = source.length;
    } else stack.push(node);
  }
  return nodes;
}

const within = (node, ancestor) => {
  for (let n = node.parent; n; n = n.parent) if (n === ancestor) return true;
  return false;
};
const classes = node => (node.attrs.class || '').split(/\s+/);
const samePath = (a, b) => {
  const normalize = p => { p = p.normalize('NFC'); return process.platform === 'win32' ? p.toLowerCase() : p; };
  return normalize(path.resolve(a)) === normalize(path.resolve(b));
};
const isFile = file => { try { return fs.statSync(file).isFile(); } catch { return false; } };

function hrefPath(note, href) {
  // Only local HTML references; '+' is literal, while fragment/query suffixes are removed.
  if (/^(?:[a-z][\w+.-]*:|\/\/)/i.test(href)) return null;
  try { return path.resolve(path.dirname(note), decodeURIComponent(href.split(/[?#]/)[0])); } catch { return null; }
}

function newTabTag(tag) {
  const attrs = attributes(tag);
  const rel = [...new Set((attrs.rel || '').split(/\s+/).filter(Boolean).concat('noopener', 'noreferrer'))].join(' ');
  // Remove actual attribute spans, including valueless duplicates. Searching the
  // raw tag for target=/rel= would also damage words inside title/data attributes.
  let stripped = tag;
  const remove = [...tag.matchAll(attrPattern)].filter(m => ['target', 'rel'].includes(m[1].toLowerCase()));
  for (const m of remove.reverse()) stripped = stripped.slice(0, m.index) + stripped.slice(m.index + m[0].length);
  return stripped.replace(/>$/, ' target="_blank" rel="' + escapeHtml(rel) + '">');
}

function linkNotes({ note, links, dryRun = false }) {
  if (!path.isAbsolute(note) || !Array.isArray(links)) throw new Error('note must be absolute and links must be an array');
  const results = [];
  if (!isFile(note)) return { note, changed: false, results: links.map(l => ({ sectionId: l.sectionId, html: l.html, status: 'skipped', reason: 'NOTE_MISSING' })) };
  const original = fs.readFileSync(note, 'utf8');
  let source = original;
  for (const link of links) {
    const result = { sectionId: link.sectionId, html: link.html, status: 'skipped' };
    results.push(result);
    if (typeof link.html !== 'string' || !path.isAbsolute(link.html) || path.extname(link.html).toLowerCase() !== '.html' || samePath(note, link.html)) { result.reason = 'TARGET_INVALID'; continue; }
    if (!isFile(link.html)) { result.reason = 'TARGET_MISSING'; continue; }
    if (!['sectionId', 'label', 'before', 'after'].every(k => typeof link[k] === 'string') || !link.label.trim()) { result.reason = 'LINK_INVALID'; continue; }
    const nodes = elements(source);
    const sections = nodes.filter(n => n.attrs.id === link.sectionId);
    if (sections.length !== 1) { result.reason = sections.length ? 'SECTION_AMBIGUOUS' : 'SECTION_MISSING'; continue; }
    const section = sections[0];
    if (!section.end || !['article', 'section'].includes(section.name)) { result.reason = 'SECTION_INVALID'; continue; }
    const children = nodes.filter(n => within(n, section));
    const anchors = children.filter(n => n.name === 'a' && n.attrs.href && samePath(hrefPath(note, n.attrs.href) || path.dirname(note), link.html));
    if (anchors.length) {
      // Repair existing links, preserving their visible wording and unrelated attributes.
      let edited = false;
      for (const anchor of anchors.sort((a, b) => b.start - a.start)) {
        const old = source.slice(anchor.start, anchor.openEnd);
        if (anchor.attrs.target === '_blank' && ['noopener', 'noreferrer'].every(r => (anchor.attrs.rel || '').split(/\s+/).includes(r))) continue;
        source = source.slice(0, anchor.start) + newTabTag(old) + source.slice(anchor.openEnd);
        edited = true;
      }
      result.status = edited ? 'updated' : 'unchanged';
      continue;
    }
    let anchor;
    if (link.anchorId !== undefined) {
      const hits = children.filter(n => n.attrs.id === link.anchorId);
      if (hits.length !== 1) { result.reason = hits.length ? 'ANCHOR_AMBIGUOUS' : 'ANCHOR_MISSING'; continue; }
      anchor = hits[0];
    } else {
      // Prefer the precise explanation, then the introductory explanation, then a heading.
      anchor = children.find(n => classes(n).includes('layer') && classes(n).includes('formal'))
        || children.find(n => classes(n).includes('layer') && classes(n).includes('eli5'))
        || children.find(n => ['h2', 'h3'].includes(n.name));
    }
    if (!anchor?.end || ['p', 'a', 'span', 'script', 'style'].includes(anchor.name)) { result.reason = 'ANCHOR_INVALID'; continue; }
    const relative = path.relative(path.dirname(note), link.html);
    if (path.isAbsolute(relative)) { result.reason = 'TARGET_INVALID'; continue; }
    const href = relative.split(path.sep).map(encodeURIComponent).join('/');
    const block = '\n<p class="interactive-note" data-ml-interactive="' + escapeHtml(href) + '">' + escapeHtml(link.before)
      + '<a href="' + escapeHtml(href) + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(link.label) + '</a>'
      + escapeHtml(link.after) + '</p>\n';
    source = source.slice(0, anchor.end) + block + source.slice(anchor.end);
    result.status = 'added';
  }
  const changed = source !== original;
  if(changed&&!dryRun){
    const temp=note+'.'+require('node:crypto').randomUUID()+'.tmp';
    try{fs.writeFileSync(temp,source,{flag:'wx'});fs.renameSync(temp,note);}finally{if(fs.existsSync(temp))fs.unlinkSync(temp);}
  }
  return { note, changed, results };
}

if (require.main === module) {
  try {
    const [file, option] = process.argv.slice(2);
    if (!file || (option && option !== '--dry-run')) throw new Error('usage: node link-notes.cjs <manifest.json> [--dry-run]');
    const manifest = JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
    if (!Array.isArray(manifest.notes)) throw new Error('manifest.notes must be an array');
    console.log(JSON.stringify({ notes: manifest.notes.map(entry => linkNotes({ ...entry, dryRun: option === '--dry-run' })) }, null, 2));
  } catch (e) { console.error('link-notes failed: ' + e.message); process.exitCode = 1; }
}
module.exports = { linkNotes };
