// Browser QA: node qa.cjs <n> [page.html] → runs desktop/mobile, light/dark, every mode, input, step and panel.
const fs = require('fs'), path = require('path'), assert = require('assert/strict'), { pathToFileURL } = require('url');
const { chromium } = require('C:/Users/Hyunjun/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const CONFIG = {
  1: { modes: { '단계': ['in-sigma1', 'in-rho'], '스케일': ['in-sigma1', 'in-rho'] }, playback: ['단계'], toggles: { '단계': ['이름표', '원래 점'], '스케일': ['표준화', '이름표'] } },
  2: { modes: { '쌓기': [], '읽기': ['in-sigma1', 'in-sigma2', 'in-rho'], '평균': ['in-mu1', 'in-mu2'] }, playback: ['쌓기'], toggles: { '읽기': ['곱 부호 색', '이름표'], '평균': ['centering', '이름표'] } },
  3: { modes: { '길이': ['in-len', 'in-theta', 'in-x1', 'in-x2'], '사잇각': ['in-phi', 'in-l1', 'in-l2'] }, playback: [], toggles: { '길이': ['이름표'], '사잇각': ['이름표'] }, formula: '수식' },
};
const n = process.argv[2], cfg = CONFIG[n], run = path.join(__dirname, n), file = process.argv[3] || path.join(run, 'preview.html');
const tag = process.argv[3] ? 'final' : 'preview', evidence = path.join(run, 'evidence');
fs.mkdirSync(evidence, { recursive: true });
const btn = (page, name) => page.getByRole('button', { name, exact: true });

async function openLeft(page, narrow) { if (narrow) await btn(page, '조작 패널').click(); }
async function closeDrawer(page, narrow) {
  if (!narrow) return;
  await page.keyboard.press('Escape');
  assert.equal(await btn(page, '조작 패널').getAttribute('aria-expanded'), 'false');
}
async function checkField(page, id) {
  const input = page.locator('#' + id), range = input.locator('xpath=following-sibling::input[1]');
  const [min, max, step] = await Promise.all(['min', 'max', 'step'].map((a) => input.getAttribute(a)));
  const start = await input.inputValue();
  for (const v of [min, max, start]) { await input.fill(v); assert.equal(Number(await input.inputValue()), Number(v), id); }
  await input.fill(''); assert.equal(await input.inputValue(), start, id + ' empty');
  await input.fill(String(Number(max) + Number(step))); assert.equal(await input.inputValue(), start, id + ' above');
  await input.fill(String(Number(min) + Number(step) / 3)); assert.equal(await input.inputValue(), start, id + ' off grid');
  // 슬라이더를 움직이는 동안 같은 DOM 노드가 유지되어야 끌기가 끊기지 않아요.
  const before = await range.elementHandle();
  await range.fill(max); assert.equal(await before.evaluate((el) => el.isConnected), true, id + ' range replaced');
  assert.equal(Number(await input.inputValue()), Number(max));
  await range.fill(start);
}

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'chrome' }), results = [];
  for (const width of [1440, 375]) for (const theme of ['light', 'dark']) {
    const narrow = width < 1024;
    const page = await browser.newPage({ viewport: { width, height: narrow ? 812 : 900 }, colorScheme: theme, hasTouch: false });
    const errors = [], external = [];
    page.on('pageerror', (e) => errors.push(e.message));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('request', (r) => { if (/^https?:/.test(r.url())) external.push(r.url()); });
    await page.goto(pathToFileURL(file).href);
    await page.locator('.canvas').waitFor();
    await page.evaluate(() => document.fonts.ready);
    const shot = (name) => page.screenshot({ path: path.join(evidence, `${tag}-${width}-${theme}-${name}.png`) });

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
      }
      await closeDrawer(page, narrow);
      await page.waitForTimeout(320);
      await shot(mode + '-last-step');
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
      await btn(page, '확대').click(); await btn(page, '축소').click(); await btn(page, '시점 처음으로').click();
      if (narrow) {
        await btn(page, '설명 패널').click();
        await page.locator('.panel-right.is-open').waitFor();
        await page.waitForTimeout(280);
        await shot(mode + '-right');
        await page.keyboard.press('Escape');
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
      await page.locator('.formula-scroll').focus();
      await page.keyboard.press('ArrowLeft');
      assert.equal(await page.locator('.formula-row').count(), lines - 1);
      await page.keyboard.press('ArrowRight');
      await btn(page, '확대').click();
      assert.equal(await page.locator('.stage-body').evaluate((el) => el.style.getPropertyValue('--formula-scale').trim()), '1.1');
      await btn(page, '수식 크기 초기화').click();
      await page.waitForTimeout(120);
      await shot('formula');
    }
    const layout = await page.evaluate(() => ({
      overflow: document.documentElement.scrollWidth > innerWidth,
      katexErrors: document.querySelectorAll('.katex-error').length,
      firstLeft: getComputedStyle(document.querySelector('.panel-left .panel-content > *')).borderTopWidth,
      fontLoaded: document.fonts.check('16px Pretendard'),
    }));
    assert.equal(layout.overflow, false); assert.equal(layout.katexErrors, 0);
    await openLeft(page, narrow);
    await btn(page, '입력과 모드 처음으로').click();
    const firstMode = Object.keys(cfg.modes)[0];
    assert.equal(await btn(page, firstMode).getAttribute('aria-pressed'), 'true');
    await closeDrawer(page, narrow);
    const katexCount = await page.locator('.katex').count();
    await page.waitForTimeout(120);
    await shot('reset');
    assert.deepEqual(errors, []); assert.deepEqual(external, []);
    results.push({ width, theme, ...layout, katexCount, modes: Object.keys(cfg.modes).length + (cfg.formula ? 1 : 0), inputs: true, steps: true, reset: true, drawer: narrow });
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(evidence, tag + '-browser.json'), JSON.stringify(results, null, 2));
  console.log('PASS', n, tag, JSON.stringify(results));
})().catch((e) => { console.error(e); process.exit(1); });
