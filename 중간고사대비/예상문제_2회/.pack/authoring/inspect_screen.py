from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path.cwd();RUN=R/'tmp/ml-midterm/round02-easier-20261020';p=Path(json.loads((RUN/'explanation-result.json').read_text())['html']);shots=RUN/'main-shots';shots.mkdir(exist_ok=True)
with sync_playwright() as w:
 b=w.chromium.launch(channel='chrome',headless=True)
 for width,height,theme in [(1280,900,'light'),(375,812,'dark')]:
  c=b.new_context(viewport={'width':width,'height':height},color_scheme=theme,reduced_motion='reduce');page=c.new_page();page.goto(p.as_uri(),wait_until='networkidle');page.evaluate('document.fonts.ready')
  if width>=1024:
   for sel in ['#toggle-left','#toggle-prob','#toggle-right']:
    if page.locator(sel).get_attribute('aria-expanded')=='true':page.locator(sel).click()
  for i in (6,8,10):
   page.evaluate('(x)=>location.hash=x',f'p{i}');page.wait_for_timeout(120)
   solve=page.locator(f'#p{i} [data-explanation="solve"]');solve.scroll_into_view_if_needed();page.evaluate('(y)=>scrollTo(0,y-90)',solve.bounding_box()['y']+page.evaluate('scrollY'));page.wait_for_timeout(100)
   page.screenshot(path=str(shots/f'{width}-{theme}-p{i}-solve.png'))
  c.close()
 b.close()
print('6 additional solve-view screenshots captured')
