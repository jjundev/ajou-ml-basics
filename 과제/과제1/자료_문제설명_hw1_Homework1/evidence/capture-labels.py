from pathlib import Path
import json
from playwright.sync_api import sync_playwright
folder=Path(__file__).parent.parent;meta=json.loads((folder/'stage.json').read_text());stage=folder/meta['stage']
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True)
 for width,height in [(1280,900),(375,812)]:
  page=browser.new_page(viewport={'width':width,'height':height},color_scheme='dark')
  page.goto((stage/meta['html']).as_uri()+'#p17',wait_until='networkidle')
  page.evaluate('document.fonts.ready');page.wait_for_timeout(300)
  page.locator('#p17 [data-explanation="solve"] > h4').scroll_into_view_if_needed()
  page.wait_for_timeout(300)
  page.screenshot(path=str(folder/'evidence'/f'labels-p17-solve-{width}-dark.png'))
  page.close()
 browser.close()
