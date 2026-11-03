const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { linkNotes } = require('../scripts/link-notes.cjs');

function fixture(t, source) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'bi-links-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const note = path.join(dir, '정리노트.html');
  const html = path.join(dir, '인터렉티브 NAD+ #1.html'.normalize('NFD'));
  fs.writeFileSync(html, '<title>발효</title>');
  fs.writeFileSync(note, source || '<article id="pcr"><h3>PCR</h3><div class="layer formal"><p>설명</p><div><p>중첩 설명</p></div></div><div class="layer warn">기억</div></article>');
  const link = { sectionId: 'pcr', html, label: 'PCR & 모형', before: '순서를 ', after: '에서 살펴보세요.' };
  return { dir, note, html, link };
}

test('adds a contextual new-tab link after the full nested explanation, preserving surrounding bytes', t => {
  const f = fixture(t);
  const original = fs.readFileSync(f.note, 'utf8');
  const r = linkNotes({ note: f.note, links: [f.link] });
  assert.equal(r.changed, true);
  assert.equal(r.results[0].status, 'added');
  const changed = fs.readFileSync(f.note, 'utf8');
  assert.match(changed, /<\/p><\/div><\/div>\s*<p class="interactive-note"/);
  assert.match(changed, /target="_blank" rel="noopener noreferrer"/);
  assert.match(changed, /PCR &amp; 모형/);
  assert.doesNotMatch(changed, /\(새 탭\)/);
  assert.equal(changed.replace(/\n?<p class="interactive-note"[^>]*>[\s\S]*?<\/p>\n?/, ''), original);
  const href = changed.match(/<a href="([^"]+)"/)[1];
  assert.match(href, /NAD%2B%20%231/);
  assert.equal(path.resolve(path.dirname(f.note), decodeURIComponent(href)), f.html);
  assert.deepEqual(linkNotes({ note: f.note, links: [f.link] }).results.map(x => x.status), ['unchanged']);
});

test('dryRun never writes and multiple links in different sections are all applied once', t => {
  const f = fixture(t, '<article id="pcr"><h3>PCR</h3><p>説明</p></article><article id="gel"><h3>겔</h3><p>설명</p></article>');
  const links = [f.link, { ...f.link, sectionId: 'gel', label: '겔' }];
  const original = fs.readFileSync(f.note, 'utf8');
  assert.equal(linkNotes({ note: f.note, links, dryRun: true }).changed, true);
  assert.equal(fs.readFileSync(f.note, 'utf8'), original);
  assert.equal(linkNotes({ note: f.note, links }).results.filter(x => x.status === 'added').length, 2);
  assert.equal(linkNotes({ note: f.note, links }).changed, false);
});

test('missing note, missing target, missing section and duplicate IDs skip without changing existing content', t => {
  const f = fixture(t);
  const original = fs.readFileSync(f.note, 'utf8');
  for (const [link, reason] of [
    [{ ...f.link, html: path.join(f.dir, 'missing.html') }, 'TARGET_MISSING'],
    [{ ...f.link, sectionId: 'absent' }, 'SECTION_MISSING'],
    [{ ...f.link, html: f.note }, 'TARGET_INVALID'],
  ]) {
    const r = linkNotes({ note: f.note, links: [link] });
    assert.equal(r.changed, false);
    assert.equal(r.results[0].reason, reason);
    assert.equal(fs.readFileSync(f.note, 'utf8'), original);
  }
  assert.equal(linkNotes({ note: path.join(f.dir, 'missing.html'), links: [f.link] }).results[0].reason, 'NOTE_MISSING');
  fs.writeFileSync(f.note, original + original);
  assert.equal(linkNotes({ note: f.note, links: [f.link] }).results[0].reason, 'SECTION_AMBIGUOUS');
  assert.equal(fs.readFileSync(f.note, 'utf8'), original + original);
});

test('existing destination link in the same section is upgraded without duplicate text', t => {
  const f = fixture(t);
  const href = path.basename(f.html).split('/').map(encodeURIComponent).join('/');
  const original = `<article id='pcr'><h3>PCR</h3><p><a class='old' href='${href}' target='_self' rel='nofollow'>기존 자료</a></p></article>`;
  fs.writeFileSync(f.note, original);
  const r = linkNotes({ note: f.note, links: [f.link] });
  assert.equal(r.results[0].status, 'updated');
  const result = fs.readFileSync(f.note, 'utf8');
  assert.equal((result.match(/<a\b/g) || []).length, 1);
  assert.match(result, /class='old'/);
  assert.match(result, /rel="nofollow noopener noreferrer"/);
  assert.equal(linkNotes({ note: f.note, links: [f.link] }).changed, false);
});

test('a link outside the target section does not suppress a contextual link', t => {
  const f = fixture(t);
  fs.appendFileSync(f.note, `<footer><a href="${encodeURIComponent(path.basename(f.html))}">자료</a></footer>`);
  assert.equal(linkNotes({ note: f.note, links: [f.link] }).results[0].status, 'added');
});

test('new-tab repair preserves target/rel words inside unrelated quoted attributes', t => {
  const f = fixture(t);
  const title = 'read target=_self and rel=nofollow here';
  fs.writeFileSync(f.note, `<article id="pcr"><h3>PCR</h3><a href="${encodeURIComponent(path.basename(f.html))}" title="${title}" target="_self">자료</a></article>`);
  assert.equal(linkNotes({ note: f.note, links: [f.link] }).results[0].status, 'updated');
  assert.ok(fs.readFileSync(f.note, 'utf8').includes(`title="${title}"`));
});

test('valueless or duplicate target/rel attributes do not suppress new-tab repair', t => {
  const f = fixture(t);
  for (const attrs of ['target rel', 'target="_self" target="_blank" rel="noopener noreferrer"']) {
    fs.writeFileSync(f.note, `<article id="pcr"><h3>PCR</h3><a href="${encodeURIComponent(path.basename(f.html))}" ${attrs}>자료</a></article>`);
    assert.equal(linkNotes({ note: f.note, links: [f.link] }).results[0].status, 'updated');
    const tag = fs.readFileSync(f.note, 'utf8').match(/<a\b[^>]*>/)[0];
    assert.equal((tag.match(/\btarget\b/g) || []).length, 1);
    assert.equal((tag.match(/\brel\b/g) || []).length, 1);
    assert.match(tag, /target="_blank" rel="noopener noreferrer"/);
  }
});

test('comments, script strings and quoted greater-than signs do not create fake sections', t => {
  const f = fixture(t, '<!-- <article id="pcr">fake</article> --><script>const s = \'<article id="pcr">fake</article>\';</script><article id="pcr" data-test="a > b"><h3>PCR</h3><div class="layer formal"><p>설명</p></div></article>');
  const original = fs.readFileSync(f.note, 'utf8');
  assert.equal(linkNotes({ note: f.note, links: [f.link] }).results[0].status, 'added');
  assert.ok(fs.readFileSync(f.note, 'utf8').startsWith(original.slice(0, original.indexOf('<article id="pcr" data-test'))));
});

test('explicit anchor must uniquely belong to the selected section', t => {
  const f = fixture(t, '<article id="pcr"><h3>PCR</h3><figure id="fig"><p>그림</p></figure><p>다음</p></article><div id="outside">밖</div>');
  assert.equal(linkNotes({ note: f.note, links: [{ ...f.link, anchorId: 'outside' }] }).results[0].reason, 'ANCHOR_MISSING');
  assert.equal(linkNotes({ note: f.note, links: [{ ...f.link, anchorId: 'fig' }] }).results[0].status, 'added');
  assert.match(fs.readFileSync(f.note, 'utf8'), /<\/figure>\s*<p class="interactive-note"/);
});

test('CLI accepts a grouped manifest and exposes per-note results', t => {
  const f = fixture(t);
  const manifest = path.join(f.dir, 'manifest.json');
  fs.writeFileSync(manifest, JSON.stringify({ notes: [{ note: f.note, links: [f.link] }] }));
  const cli = path.join(__dirname, '../scripts/link-notes.cjs');
  const r = spawnSync(process.execPath, [cli, manifest], { encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  assert.equal(JSON.parse(r.stdout).notes[0].results[0].status, 'added');
});

test('recognizes an existing link when the target path is spelled in the other Unicode form', t => {
  const f = fixture(t);
  assert.equal(linkNotes({ note: f.note, links: [f.link] }).results[0].status, 'added');
  const r = linkNotes({ note: f.note, links: [{ ...f.link, html: f.html.normalize('NFC') }] });
  assert.equal(r.changed, false);
  assert.equal(r.results[0].status, 'unchanged');
  assert.equal((fs.readFileSync(f.note, 'utf8').match(/interactive-note/g) || []).length, 1);
});
