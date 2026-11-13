// Saves one topic into a 복습노트 folder under the next free number, then builds its page.
// Usage: node save.cjs <RUN/n/Main.dc.html> <DEST> <name>   → {"nn", "html", "dir"} JSON (exit 0), usage (exit 2) or the error (exit 1) on stderr
// Files are 인터렉티브_NN_<name>.html and .pack/자료_인터렉티브_NN_<name>/; spaces in name become '_'.
// Never overwrites: the number skips every 인터렉티브_NN* and .pack/자료_인터렉티브_NN*. Nothing is written next to the source.
const fs = require('node:fs');
const path = require('node:path');
const { nextNumber } = require('./resolve.cjs');
const { build, canvasJson, titleOf, verifyVendor, findVendorDir } = require('./build.cjs');

// A file name part: no path or reserved characters, no leading dot.
function cleanName(name) {
  const n = String(name == null ? '' : name).trim().replace(/\s+/g, '_');
  if (!n || /[\\/:*?"<>|]/.test(n) || n.startsWith('.')) throw new Error('bad name: ' + JSON.stringify(name));
  return n;
}

function save({ src, dest, name }) {
  name = cleanName(name);
  src = path.resolve(src);
  dest = path.resolve(dest);
  fs.mkdirSync(dest, { recursive: true });
  const nn = nextNumber(dest);
  const assets = path.join(dest, '.pack');
  const hadAssets = fs.existsSync(assets);
  const dir = path.join(assets, '자료_인터렉티브_' + nn + '_' + name);
  const html = path.join(dest, '인터렉티브_' + nn + '_' + name + '.html');
  fs.mkdirSync(assets, { recursive: true });
  const dropEmptyAssets = () => { if (!hadAssets) try { fs.rmdirSync(assets); } catch (e) { /* not empty: keep */ } };
  try {
    fs.mkdirSync(dir); // not recursive: fails instead of writing into a folder that appeared meanwhile
  } catch (e) {
    dropEmptyAssets();
    throw e;
  }
  let ownsHtml=false;
  try {
    const copy = path.join(dir, 'Main.dc.html');
    fs.copyFileSync(src, copy);
    fs.writeFileSync(path.join(dir, 'canvas.json'), canvasJson(titleOf(fs.readFileSync(copy, 'utf8'))));
    const vendorDir = verifyVendor(findVendorDir(dest));
    const output = build(copy, html, { vendorDir });
    const fd=fs.openSync(html,'wx'); ownsHtml=true;
    try{fs.writeFileSync(fd,output);}finally{fs.closeSync(fd);}
  } catch (e) {
    if(ownsHtml) fs.unlinkSync(html);
    // A half-made number would push every later save past a gap.
    fs.rmSync(dir, { recursive: true, force: true });
    dropEmptyAssets();
    throw e;
  }
  return { nn, html, dir };
}

if (require.main === module) {
  const [src, dest, name] = process.argv.slice(2);
  if (!src || !dest || !name || !fs.existsSync(src) || !fs.statSync(src).isFile()) {
    console.error('usage: node save.cjs <RUN/n/Main.dc.html> <DEST> <name>');
    process.exit(2);
  }
  try {
    console.log(JSON.stringify(save({ src, dest, name })));
  } catch (e) {
    console.error('save failed: ' + String(e.message || e).split('\n')[0]);
    process.exit(1);
  }
}

module.exports = { save };
