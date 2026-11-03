// node linkqa.cjs <note.html> <outdir>: clicks every data-ml-interactive link at 1440 and 375 and checks new-tab target + note kept.
const { chromium } = require(process.env.ML_PLAYWRIGHT_MODULE || 'playwright'), { pathToFileURL } = require('url'), fs = require('fs'), path = require('path'), assert = require('assert/strict');
(async () => {
  const [note, out] = process.argv.slice(2), b = await chromium.launch({ headless: true, channel: 'chrome' }), res = [];
  for (const width of [1440, 375]) {
    const ctx = await b.newContext({ viewport: { width, height: width < 1024 ? 812 : 900 } }), page = await ctx.newPage(), url = pathToFileURL(note).href;
    await page.goto(url);
    const links = page.locator('[data-ml-interactive] a');
    const n = await links.count();
    for (let i = 0; i < n; i++) {
      const a = links.nth(i), sec = await a.evaluate((el) => el.closest('article.topic').id);
      await page.evaluate((id) => { location.hash = id; }, sec); await page.waitForTimeout(350);
      const here = page.url();
      assert.equal(await a.getAttribute('target'), '_blank'); assert.equal(await a.getAttribute('rel'), 'noopener noreferrer');
      await a.scrollIntoViewIfNeeded();
      if (i === 0 || i === 6) await page.screenshot({ path: path.join(out, `link-${width}-context-${i}.png`) });
      const [tab] = await Promise.all([ctx.waitForEvent('page'), a.click()]);
      await tab.waitForLoadState('load'); await tab.locator('.canvas').waitFor();
      const title = await tab.title();
      res.push({ width, sec, title, tab: decodeURIComponent(tab.url().split('/').pop()), noteKept: page.url() === here });
      assert.equal(page.url(), here); assert.ok(here.startsWith(url));
      await tab.close();
    }
    await ctx.close();
  }
  await b.close();
  fs.writeFileSync(path.join(out, 'link-browser.json'), JSON.stringify(res, null, 2));
  console.log(res.map((r) => `${r.width} ${r.sec} → ${r.tab} (${r.title}) kept=${r.noteKept}`).join('\n'));
})().catch((e) => { console.error(e); process.exit(1); });
