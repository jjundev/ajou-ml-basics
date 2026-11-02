// Resolves a date (MMDD) or a topic to the 복습노트 folder to save into and the next 인터렉티브 number.
// Usage: node resolve.cjs <repo> <MMDD | 주제>   → JSON, or {"error": "<CODE>"} with exit 1
// Names on macOS disks are often NFD: every comparison is done in NFC, every returned path is the real one.
const fs = require('node:fs');
const path = require('node:path');

const nfc = (s) => s.normalize('NFC');
const squash = (s) => nfc(s).toLowerCase().replace(/\s+/g, '');

function fail(code) {
  const e = new Error(code);
  e.code = code;
  return e;
}

function list(dir) {
  try { return fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return []; }
}

// Real path of the child of dir whose NFC name is `name`, or null.
function child(dir, name) {
  const hit = list(dir).find((d) => nfc(d.name) === nfc(name));
  return hit ? path.join(dir, hit.name) : null;
}

function sttFor(repo, date) {
  if (!date) return null;
  const dir = child(repo, 'STT');
  const hit = dir && list(dir).find((d) => d.isFile() && new RegExp('^' + date + '[ _]머러기\\.md$').test(nfc(d.name)));
  return hit ? path.join(dir, hit.name) : null;
}

function dateFolders(notesDir) {
  return list(notesDir).filter((d) => d.isDirectory() && /^\d{4}(-\d{4})?$/.test(d.name))
    .map((d) => ({ name: d.name, start: d.name.slice(0, 4), end: d.name.slice(-4), path: path.join(notesDir, d.name) }));
}

// 정리노트 .md lives in <folder>/.pack/.
function notesIn(folder) {
  const byName = new Map();
  for (const dir of [folder, path.join(folder,'.pack')]) {
    for (const d of list(dir)) {
      if (d.isFile() && /^정리노트_.*\.md$/.test(nfc(d.name))) {
        byName.set(nfc(d.name),path.join(dir,d.name));
      }
    }
  }
  return [...byName.values()];
}

function existingIn(folder) {
  return list(folder).filter((d) => d.isFile() && /^(인터렉티브|3D모형)_.*\.html$/.test(nfc(d.name))).map((d) => {
    const m = fs.readFileSync(path.join(folder, d.name), 'utf8').match(/<title>([\s\S]*?)<\/title>/);
    return { file: d.name, title: m ? m[1].trim() : '' };
  });
}

// Highest NN over <folder>/인터렉티브_NN*.html, <folder>/.pack/자료_인터렉티브_NN* and (legacy) <folder>/자료_인터렉티브_NN*.
function nextNumber(folder) {
  let max = 0;
  for (const d of [...list(folder), ...list(path.join(folder, '.pack'))]) {
    const m = nfc(d.name).match(/^(?:인터렉티브_(\d{2,})(?:_[^/]*)?\.html|자료_인터렉티브_(\d{2,})(?:_[^/]*)?)$/);
    if (m) max = Math.max(max, Number(m[1] || m[2]));
  }
  return String(max + 1).padStart(2, '0');
}

function resolve({ repo, arg }) {
  const a = nfc(String(arg || '')).trim();
  if (!a) throw fail('NO_ARG');
  const notesDir = child(repo, '복습노트') || path.join(repo, '복습노트');
  const folders = dateFolders(notesDir);
  let kind, folder, date;

  if (/^\d{4}-\d{4}$/.test(a)) {
    kind = 'date';
    date = a.slice(0, 4);
    const hit = folders.find((f) => f.name === a);
    if (!hit) throw fail('NO_TARGET');
    folder = hit.path;
  } else if (/^\d{4}$/.test(a)) {
    kind = 'date';
    date = a;
    const exact = folders.find(f=>f.name===a);
    const ranges=folders.filter(f=>f.start<=a&&a<=f.end);
    if(!exact&&ranges.length>1) throw fail('AMBIGUOUS_TARGET');
    const hit=exact||ranges[0];
    if (hit) folder = hit.path;
    else if (sttFor(repo, a)) folder = path.join(notesDir, a);
    else throw fail('NO_TARGET');
  } else {
    kind = 'topic';
    // Link text is dropped so a later note's back-link ("지난 1006 수업: …오페론") does not count;
    // notes with every word of the topic in one H2/H3 heading win, then the latest end date.
    const needle = squash(a), words = a.split(/\s+/).map(squash);
    const inHeading = (l) => /^#{2,3}\s/.test(l) && words.every((w) => squash(l).includes(w));
    const hits = [];
    for (const f of folders) {
      const texts = notesIn(f.path).map((n) => fs.readFileSync(n, 'utf8').replace(/\[[^\]]*\]\([^)]*\)/g, ''));
      const heading = texts.some((t) => t.split('\n').some(inHeading));
      if (!heading && !texts.some((t) => squash(t).includes(needle))) continue;
      hits.push(Object.assign({ heading }, f));
    }
    hits.sort((x, y) => (y.heading - x.heading) || (x.end < y.end ? 1 : x.end > y.end ? -1 : 0));
    if (hits.length) { folder = hits[0].path; date = hits[0].end; }
    else { folder = child(notesDir, '주제별') || path.join(notesDir, '주제별'); date = null; }
  }

  const exists = fs.existsSync(folder);
  return {
    kind, folder, exists, date,
    notes: exists ? notesIn(folder) : [],
    noteHtml: exists ? list(folder).filter((d) => d.isFile() && /^정리노트_.*\.html$/.test(nfc(d.name))).map((d) => path.join(folder, d.name)) : [],
    stt: sttFor(repo, date),
    existing: exists ? existingIn(folder) : [],
    next: exists ? nextNumber(folder) : '01',
  };
}

if (require.main === module) {
  const [repo, ...rest] = process.argv.slice(2);
  try {
    console.log(JSON.stringify(resolve({ repo: path.resolve(repo || '.'), arg: rest.join(' ') }), null, 2));
  } catch (e) {
    if (!e.code) throw e;
    console.log(JSON.stringify({ error: e.code }));
    process.exit(1);
  }
}

module.exports = { resolve, nextNumber };
