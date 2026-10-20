import json,pathlib,re
from playwright.sync_api import sync_playwright
out=pathlib.Path(__file__).parent
packs=json.loads((out/'assigned-packs.json').read_text())
s=pathlib.Path(packs[3]['source']).read_text()
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':720,'height':380},device_scale_factor=1)
 for pid in ['p3','p4']:
  card=re.search(r'<article[^>]+id="'+pid+r'".*?</article>',s,re.S).group()
  svg=re.search(r'<svg.*?</svg>',card,re.S).group()
  page.set_content('<html><style>body{margin:20px;background:white}.fig-ink{fill:none;stroke:#111;stroke-width:1.5}.fig-text{fill:#111;font-family:Arial}svg{width:680px;height:310px}</style>'+svg+'</html>')
  page.screenshot(path=str(out/f'current-0921-{pid}-graph.png'))
 b.close()
