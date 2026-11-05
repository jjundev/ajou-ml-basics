// Browser QA: node qa.cjs [page.html] → desktop/mobile, light/dark, every mode, inputs, steps, toggles, zoom, drawer, formula.
// Playwright comes from ML_PLAYWRIGHT_MODULE (see ml-interactive design.md).
const fs = require('fs'), path = require('path'), assert = require('assert/strict'), { pathToFileURL } = require('url');
const { chromium } = require(process.env.ML_PLAYWRIGHT_MODULE || 'playwright');

const M = ['in-a11', 'in-a12', 'in-a21', 'in-a22', 'in-c1', 'in-c2'];
const cfg = {
  modes: { '모눈': M, '대각화': M },
  playback: ['대각화'],
  toggles: { '모눈': ['이름표', '고유기저 모눈', '성분 보조선'], '대각화': ['이름표', '변환 모눈', '목표 Dc'] },
  formula: '비교'
};
const run = path.resolve(__dirname, '..'), file = process.argv[2] ? path.resolve(process.argv[2]) : path.join(run, 'preview.html');
const tag = process.argv[2] ? 'final' : 'preview', evidence = __dirname;
fs.mkdirSync(evidence, { recursive: true });
const btn = (page, name) => page.getByRole('button', { name, exact: true });

async function openLeft(page, narrow) { if (narrow && (await btn(page, '조작 패널').getAttribute('aria-expanded')) !== 'true') await btn(page, '조작 패널').click(); }
async function closeDrawer(page, narrow) {
  if (!narrow) return;
  await page.keyboard.press('Escape');
  assert.equal(await btn(page, '조작 패널').getAttribute('aria-expanded'), 'false');
}
async function checkField(page, id) {
  const input = page.locator('#' + id), range = input.locator('xpath=following-sibling::input[@type="range"][1]');
  const [min, max, step] = await Promise.all(['min', 'max', 'step'].map((a) => input.getAttribute(a)));
  const start = await input.inputValue();
  for (const v of [min, max, start]) { await input.fill(v); assert.equal(Number(await input.inputValue()), Number(v), id); }
  await input.fill(''); assert.equal(await input.inputValue(), start, id + ' empty');
  await input.fill(String(Number(max) + Number(step))); assert.equal(await input.inputValue(), start, id + ' above');
  await input.fill(String(Number(min) - Number(step))); assert.equal(await input.inputValue(), start, id + ' below');
  await input.fill(String(Number(min) + Number(step) / 3)); assert.equal(await input.inputValue(), start, id + ' off grid');
  if (await range.count()) {
    const before = await range.elementHandle();
    await range.fill(max); assert.equal(await before.evaluate((el) => el.isConnected), true, id + ' range replaced');
    assert.equal(Number(await input.inputValue()), Number(max));
    await range.fill(start);
  }
}
const canvasShot = (page) => page.locator('.canvas').screenshot();

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'chrome' }), results = [];
  for (const width of [1440, 375]) for (const theme of ['light', 'dark']) {
    const narrow = width < 1024;
    const page = await browser.newPage({ viewport: { width, height: narrow ? 812 : 900 }, colorScheme: theme, hasTouch: false });
    const errors = [], external = [];
    page.on('pageerror', (e) => errors.push(e.message));
    page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') errors.push(m.type() + ': ' + m.text()); });
    page.on('request', (r) => { if (/^https?:/.test(r.url())) external.push(r.url()); });
    await page.goto(pathToFileURL(file).href);
    await page.locator('.canvas').waitFor();
    await page.evaluate(() => document.fonts.ready);
    const shot = (name) => page.screenshot({ path: path.join(evidence, `${tag}-${width}-${theme}-${name}.png`) });
    const layoutCheck = async (label) => {
      await page.waitForTimeout(80);
      const l = await page.evaluate(() => {
        const h1 = document.querySelector('.stage-head h1').getBoundingClientRect(), tools = document.querySelector('.view-btns').getBoundingClientRect();
        const stale = [...document.querySelectorAll('[data-tex]')].filter((el) => el.dataset.rendered !== el.getAttribute('data-tex')).length;
        return { overflow: document.documentElement.scrollWidth > innerWidth, katexErrors: document.querySelectorAll('.katex-error').length,
          headRow: tools.top < h1.bottom && h1.top < tools.bottom, toolH: tools.height, stale };
      });
      assert.equal(l.overflow, false, label + ' overflow'); assert.equal(l.katexErrors, 0, label + ' katex'); assert.equal(l.headRow, true, label + ' head row');
      assert.equal(l.stale, 0, label + ' stale TeX');
    };
    await shot('first');

    for (const [mode, fields] of Object.entries(cfg.modes)) {
      await btn(page, mode).click();
      await openLeft(page, narrow);
      for (const id of fields) await checkField(page, id);
      for (const t of cfg.toggles[mode] || []) {
        const b = btn(page, t), v = await b.getAttribute('aria-pressed');
        await b.click(); assert.notEqual(await b.getAttribute('aria-pressed'), v);
        await b.click(); assert.equal(await b.getAttribute('aria-pressed'), v);
      }
      const steps = page.locator('.steps .btn'), count = await steps.count();
      assert.ok(count >= 3, mode + ' steps');
      for (let i = 0; i < count; i++) {
        await steps.nth(i).click();
        assert.equal(await steps.nth(i).getAttribute('aria-pressed'), 'true');
        assert.ok((await page.locator('.detail').innerText()).length > 5);
        if (i === 0) { await closeDrawer(page, narrow); await page.waitForTimeout(250); await shot(mode + '-step1'); await openLeft(page, narrow); }
      }
      await closeDrawer(page, narrow);
      await page.waitForTimeout(320);
      await shot(mode + '-last-step');
      await layoutCheck(mode);
      if (cfg.playback.includes(mode)) {
        const scrub = page.locator('.scrub input');
        await scrub.fill(String(Math.round(Number(await scrub.getAttribute('max')) / 2)));
        await btn(page, '재생').click();
        await page.waitForTimeout(350);
        assert.equal(await btn(page, '일시정지').count(), 1);
        await btn(page, '일시정지').click();
        await page.waitForTimeout(100);
        await shot(mode + '-mid');
      }
      const before = await canvasShot(page);
      await btn(page, '확대').click(); await page.waitForTimeout(120);
      const zoomed = await canvasShot(page);
      assert.ok(!before.equals(zoomed), mode + ' zoom changes canvas');
      await btn(page, '축소').click(); await btn(page, '시점 처음으로').click();
      if (narrow) {
        await btn(page, '설명 패널').click();
        await page.locator('.panel-right.is-open').waitFor();
        await page.waitForTimeout(280);
        await shot(mode + '-right');
        await page.keyboard.press('Escape');
        assert.equal(await btn(page, '설명 패널').getAttribute('aria-expanded'), 'false');
      }
    }
    if (cfg.formula) {
      await btn(page, cfg.formula).click();
      const next = btn(page, '다음 줄 쓰기'), prev = btn(page, '이전 줄');
      assert.equal(await prev.isDisabled(), true);
      const total = await page.locator('.formula-progress').innerText(), lines = Number(total.split('/')[1].trim().split(' ')[0]);
      for (let i = 1; i < lines; i++) await next.click();
      assert.equal(await next.isDisabled(), true);
      assert.equal(await page.locator('.formula-row').count(), lines);
      assert.equal(await page.locator('.formula-row.is-active').count(), 1);
      assert.equal(await page.locator('.formula-row.is-active .sub').count(), 1);
      await page.locator('.formula-scroll').focus();
      await page.keyboard.press('ArrowLeft');
      assert.equal(await page.locator('.formula-row').count(), lines - 1);
      await page.keyboard.press('ArrowRight');
      for (let i = 0; i < 3; i++) await btn(page, '확대').click();
      assert.equal(await page.locator('.stage-body').evaluate((el) => el.style.getPropertyValue('--formula-scale').trim()), '1.3');
      await page.waitForTimeout(150);
      await shot('formula-zoom');
      await btn(page, '수식 크기 초기화').click();
      assert.equal(await page.locator('.stage-body').evaluate((el) => el.style.getPropertyValue('--formula-scale').trim()), '1');
      assert.equal(await page.locator('.formula-row').count(), lines, 'reset keeps steps');
      await page.waitForTimeout(120);
      await shot('formula');
      await layoutCheck('formula');
    }
    const layout = await page.evaluate(() => ({
      overflow: document.documentElement.scrollWidth > innerWidth,
      katexErrors: document.querySelectorAll('.katex-error').length,
      firstLeft: getComputedStyle(document.querySelector('.panel-left .panel-content > *')).borderTopWidth,
      firstRight: getComputedStyle(document.querySelector('.panel-right .panel-content .sec')).borderTopWidth,
      fontLoaded: document.fonts.check('16px Pretendard'),
    }));
    assert.equal(layout.overflow, false); assert.equal(layout.katexErrors, 0); assert.equal(layout.fontLoaded, true);
    assert.equal(layout.firstRight, '0px', 'right first section has no top rule');
    await openLeft(page, narrow);
    await btn(page, '입력과 모드 처음으로').click();
    const firstMode = Object.keys(cfg.modes)[0];
    assert.equal(await btn(page, firstMode).getAttribute('aria-pressed'), 'true');
    await closeDrawer(page, narrow);
    const katexCount = await page.locator('.katex').count();
    await page.waitForTimeout(150);
    await shot('reset');
    const resetShot = await canvasShot(page);
    assert.deepEqual(errors, []); assert.deepEqual(external, []);
    results.push({ width, theme, ...layout, katexCount, modes: Object.keys(cfg.modes).length + (cfg.formula ? 1 : 0), inputs: true, steps: true, zoom: true, reset: resetShot.length > 0, drawer: narrow });
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(evidence, tag + '-browser.json'), JSON.stringify(results, null, 2));
  console.log('PASS', tag, JSON.stringify(results.map((r) => [r.width, r.theme, r.katexCount, r.firstLeft, r.firstRight])));
})().catch((e) => { console.error(e); process.exit(1); });
