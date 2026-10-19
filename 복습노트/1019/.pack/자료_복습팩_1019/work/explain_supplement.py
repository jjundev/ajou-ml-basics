from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse,unquote,urljoin,quote
from html.parser import HTMLParser
import json
r=Path('/tmp/ml-review-pack-20261019/1019');ep=r/'repo/tmp/ml-problem-explain/1019-20261019/review-1019-Prediction_and_Projection';cfg=json.loads((ep/'stage.json').read_text());stage=ep/cfg['stage'];html=stage/cfg['html'];dest=r/'repo/복습노트/1019';report={}
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a['href'])
s=Links();s.feed(html.read_text());checked=[]
for href in s.links:
 u=urlparse(href)
 if u.scheme or not u.path:continue
 p=(dest/unquote(u.path)).resolve()
 # Stage-generated self-owned assets resolve against stage, existing source/notes against final public folder.
 if not p.exists():p=(stage/unquote(u.path)).resolve()
 assert p.is_file(),(href,p)
 if u.fragment and p.suffix=='.html':
  t=Links();t.feed(p.read_text());assert unquote(u.fragment) in t.ids,(href,p)
 checked.append(href)
report['links_checked']=len(checked)
url='http://localhost:49191/explain/'+quote(cfg['html'])
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='chrome',headless=True);p=b.new_page(viewport={'width':1280,'height':900});p.goto(url,wait_until='networkidle');p.evaluate("location.hash='#p1'");p.wait_for_timeout(150)
 p.locator('#pager-next').click();assert p.evaluate('location.hash')=='#p2';p.locator('#pager-prev').click();assert p.evaluate('location.hash')=='#p1'
 p.locator('#panel-left nav a[href="#p8"]').click();assert p.evaluate('location.hash')=='#p8'
 p.locator('#toggle-left').click();p.locator('#toggle-right').click();p.wait_for_timeout(150);assert p.locator('#toggle-right').get_attribute('aria-expanded')=='true';assert p.locator('#panel-right').inner_text().find('완성 답')>=0
 p.screenshot(path=str(r/'work/explain-browser/summary-desktop.png'))
 p.emulate_media(media='print');p.evaluate("window.dispatchEvent(new Event('beforeprint'))");p.wait_for_timeout(150);printed=p.evaluate("[...document.querySelectorAll('main article.topic')].map(a=>({id:a.id,visible:getComputedStyle(a).display!=='none',problem:[...a.querySelectorAll('.conditions')].map(n=>n.textContent).join(''),original:a.textContent.includes('Find the projection matrix')||a.textContent.includes('find the coordinates')}))")
 assert len(printed)==8 and all(x['visible'] and x['original'] for x in printed),printed
 report['print_preserved']=printed
 b.close()
(r/'work/explain-supplement-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('links',len(checked),'pager/TOC/summary/print8 pass')
