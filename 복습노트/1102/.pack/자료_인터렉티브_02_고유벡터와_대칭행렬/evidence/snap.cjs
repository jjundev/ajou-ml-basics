// node snap.cjs <html> <out.png> <width> <theme> [stepIndex...]: clicks steps in order, then captures.
const { chromium } = require(process.env.ML_PLAYWRIGHT_MODULE || 'playwright'), { pathToFileURL } = require('url');
(async () => {
  const [file, out, w, theme, ...steps] = process.argv.slice(2), width = Number(w), narrow = width < 1024;
  const b = await chromium.launch({ headless: true, channel: 'chrome' }), p = await b.newPage({ viewport: { width, height: narrow ? 812 : 900 }, colorScheme: theme });
  await p.goto(pathToFileURL(file).href); await p.locator('.canvas').waitFor();
  if (narrow && steps.length) await p.getByRole('button', { name: '조작 패널', exact: true }).click();
  for (const s of steps) await p.locator('.steps .btn').nth(Number(s)).click();
  if (narrow && steps.length) await p.keyboard.press('Escape');
  await p.waitForTimeout(400); await p.screenshot({ path: out }); await b.close();
})();
