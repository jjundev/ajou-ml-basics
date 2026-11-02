// Builds a standalone page (opens directly in a browser) from a .dc.html source.
// Usage: node build.cjs <자료_인터렉티브_NN_<이름>/Main.dc.html> <인터렉티브_NN_<이름>.html>
const fs = require('node:fs');
const path = require('node:path');

const RUNTIME_PATH = path.join(__dirname, '..', 'assets', 'dc-runtime.js');
const FONT_CSS = '.pack/vendor/ml-interactive/pretendard/pretendard.css';
const VENDOR_SOURCE=path.join(__dirname,'../assets/vendor');
const crypto=require('node:crypto');

function titleOf(src) {
  const m = src.match(/<title>([\s\S]*?)<\/title>/);
  return m ? m[1].trim() : '';
}

function prepareVendor(dest){
 const out=path.join(dest,'.pack/vendor/ml-interactive');
 const provenance=fs.readFileSync(path.join(VENDOR_SOURCE,'provenance.json'));
 const files=JSON.parse(provenance).files;
 const hash=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
 // Validate the complete source and any existing destination before copying anything.
 for(const [rel,want] of Object.entries(files)){
  if(hash(path.join(VENDOR_SOURCE,rel))!==want)throw new Error('VENDOR_HASH_MISMATCH:source:'+rel);
  const f=path.join(out,rel);if(fs.existsSync(f)&&hash(f)!==want)throw new Error('VENDOR_HASH_MISMATCH:'+rel);
 }
 const manifest=path.join(out,'provenance.json');
 if(fs.existsSync(manifest)&&!fs.readFileSync(manifest).equals(provenance))throw new Error('VENDOR_HASH_MISMATCH:provenance');
 for(const rel of [...Object.keys(files),'provenance.json']){
  const f=path.join(out,rel);fs.mkdirSync(path.dirname(f),{recursive:true});
  if(!fs.existsSync(f))fs.copyFileSync(path.join(VENDOR_SOURCE,rel),f,fs.constants.COPYFILE_EXCL);
 }
 return out;
}
function build(srcFile, outFile, {vendorDir=path.join(path.dirname(outFile),'.pack/vendor/ml-interactive')}={}) {
  const src = fs.readFileSync(srcFile, 'utf8');
  // Uploaded /_blob fonts only resolve inside the canvas; the page loads Pretendard from the CDN like the notes.
  const helmet = src.match(/<helmet>([\s\S]*?)<\/helmet>/)[1].replace(/@font-face\s*{[^}]*}\n?/g, '').trim();
  const markup = src.slice(src.indexOf('</helmet>') + '</helmet>'.length, src.indexOf('</x-dc>')).trim();
  const script = src.match(/<script type="text\/x-dc"[^>]*>([\s\S]*?)<\/script>/)[1].trim();
  const runtime = fs.readFileSync(RUNTIME_PATH, 'utf8').trim();
  const vh=path.relative(path.dirname(outFile),vendorDir).split(path.sep).map(encodeURIComponent).join('/');
  const math=fs.readFileSync(path.join(__dirname,'../assets/ml-math.js'),'utf8');
  const rel = path.relative(path.dirname(outFile), srcFile).split(path.sep).join('/');
  return [
    '<!doctype html>',
    '<html lang="ko">',
    '<head>',
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
    `<title>${titleOf(src)}</title>`,
    `<!-- 생성 파일: ${rel}을 고친 뒤 ml-interactive/scripts/build.cjs로 다시 만드세요. -->`,
    `<link rel="stylesheet" href="${vh}/pretendard/pretendard.css">`,
    `<link rel="stylesheet" href="${vh}/katex/katex.min.css">`,
    `<script src="${vh}/katex/katex.min.js"></script>`,
    helmet,
    '</head>',
    '<body>',
    '<div id="dc-root"></div>',
    '<template id="dc-template">',
    markup,
    '</template>',
    '<script>',
    math,
    runtime,
    script,
    'mountDC(Component);',
    '</script>',
    '</body>',
    '</html>',
    '',
  ].join('\n');
}

// Manifest for publishing the source folder as a Design canvas later.
function canvasJson(title) {
  return JSON.stringify({
    v: 3,
    createdOnFiles: { v: 1, at: new Date().toISOString() },
    title,
    launch: { view: 'focused', file: 'Main.dc.html' },
    pages: [],
    boards: { 'Main.dc.html': { x: 0, y: 0, w: 1440, h: 900, title, expand: 'fill', is_interactive: true } },
    order: ['Main.dc.html'],
    notes: {},
    designSystems: [],
  });
}

if (require.main === module) {
  const [srcArg,outArg]=process.argv.slice(2);
  const srcFile=srcArg&&path.resolve(srcArg),outFile=outArg&&path.resolve(outArg);
  if (!srcFile || !outFile) {
    console.error('usage: node build.cjs <Main.dc.html> <out.html>');
    process.exit(2);
  }
  const html=build(srcFile,outFile);
  prepareVendor(path.dirname(outFile));
  fs.writeFileSync(outFile,html);
  const manifest = path.join(path.dirname(srcFile), 'canvas.json');
  if (!fs.existsSync(manifest)) fs.writeFileSync(manifest, canvasJson(titleOf(fs.readFileSync(srcFile, 'utf8'))));
  console.log('wrote ' + outFile);
}

module.exports = { build, canvasJson, titleOf, FONT_CSS, prepareVendor };
