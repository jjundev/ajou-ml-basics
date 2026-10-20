"""Exercise the existing reading UI in real Chrome, with offline local resources."""
from pathlib import Path
import json,sys,argparse,hashlib,re,html,uuid
from playwright.sync_api import sync_playwright
from exam_adapter import parse,inner

def normalized(text):
 # The fixed reader moves/drops sentence punctuation beside reflowed display math.
 # Source-to-card tests retain exact text/TeX; this compares the rendered content.
 return re.sub(r'[\s.,]+','',html.unescape(text).replace('$',''))

def original_expectations(path):
 root=parse(Path(path).read_text(encoding='utf-8'));expected={}
 for n in root.find_all(lambda n:'data-original-problem' in n.attrs):
  fields={}
  for attr in ['data-english-title','data-english-conditions','data-english-ask']:
   nodes=list(n.find_all(lambda x:attr in x.attrs))
   if len(nodes)!=1:raise ValueError('original field missing: '+attr)
   fields[attr]=normalized(nodes[0].text())
  expected[n.attrs['data-original-problem']]=fields
 return expected

DOM_FIELDS=r'''n => Object.fromEntries(['data-english-title','data-english-conditions','data-english-ask'].map(a=>{
 const c=n.querySelector('['+a+']').cloneNode(true);
 c.querySelectorAll('.katex').forEach(k=>k.replaceWith(document.createTextNode(k.querySelector('annotation').textContent)));
 return [a,c.textContent.replace(/\$/g,'').replace(/[\s.,]+/g,'')];
}))'''

def run_check(path,evidence,shots):
 evidence=Path(evidence);shots=Path(shots);shots.mkdir(parents=True,exist_ok=True)
 errors=[];screens=[];behaviors=[];original_checks=[];print_checks=[];expected=original_expectations(path)
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='chrome',headless=True)
  for width,height in [(1280,900),(1024,900),(375,812)]:
   for theme in ['light','dark']:
    ctx=browser.new_context(viewport={'width':width,'height':height},color_scheme=theme,reduced_motion='reduce')
    page=ctx.new_page();failures=[];external=[]
    page.on('pageerror',lambda e:failures.append(str(e)))
    page.on('console',lambda m:failures.append(m.text) if m.type=='error' else None)
    page.on('requestfailed',lambda r:failures.append(r.url))
    page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto(Path(path).resolve().as_uri(),wait_until='networkidle');page.wait_for_function("typeof katex!=='undefined' && document.querySelectorAll('.sums > .sum').length===10")
    page.evaluate('document.fonts.ready');ids=page.locator('article.topic').evaluate_all('(xs)=>xs.map(x=>x.id)')
    if ids!=[f'p{i}' for i in range(1,11)]:errors.append('topic IDs')
    for n in range(1,11):
     # Native hash navigation runs the template pager and moves problem/summary panes.
     page.evaluate('(id)=>{location.hash=id}',f'p{n}');page.wait_for_timeout(80)
     if not page.locator(f'#p{n}').is_visible():errors.append(f'{width} {theme} p{n}: topic hidden')
     if width<1024:
      toggle=page.locator(f'#p{n} .problem-toggle')
      if toggle.get_attribute('aria-expanded')!='true':toggle.click()
     page.locator('#tab-problem').click()
     if not page.locator(f'#problem-p{n}').is_visible():errors.append(f'Korean problem p{n}')
     if page.locator('#tabpanel-problem [data-english-title]').count():errors.append('English leaked into Korean problem tab')
     page.locator('#tab-original').click()
     orig=page.locator(f'[data-original-problem="p{n}"]')
     actual=orig.evaluate(DOM_FIELDS)
     matches=actual==expected.get(f'p{n}');active=page.locator('#tab-original').get_attribute('aria-selected')=='true'
     visible=page.locator('[data-original-problem]:visible').count()
     original_checks.append({'viewport':f'{width}x{height}','theme':theme,'topic':f'p{n}','content_matches':matches,'active':active,'visible_count':visible})
     if not matches or not active or visible!=1:errors.append(f'{width} {theme} p{n}: original content/state mismatch')
     if page.locator('#toggle-right').get_attribute('aria-expanded')!='true':page.locator('#toggle-right').click()
     page.wait_for_timeout(40)
     summary=page.locator('.sums > .sum:not([hidden])')
     if summary.count()!=1 or not summary.inner_text().strip():errors.append(f'empty summary p{n}')
     if width<1024:page.locator('#panel-right [data-panel-close]').click()
     else:
      # Keep main readable at 1024, then reopen as part of each iteration above.
      page.locator('#toggle-right').click()
     metrics=page.evaluate('''() => ({horizontal_overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth),katex_errors:document.querySelectorAll('.katex-error').length,unloaded_images:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,missing_fonts:[...document.fonts].filter(f=>f.status==='error').length})''')
     screens.append({'viewport':f'{width}x{height}','theme':theme,'topic':f'p{n}',**metrics})
     if any(metrics.values()):errors.append(f'{width} {theme} p{n}: {metrics}')
     if n in [1,3,5,7,8,9,10]:
      page.screenshot(path=str(shots/f'{width}-{theme}-p{n}.png'))
     if width<1024:toggle.click()
    # Prev/next must preserve actual article sequence.
    page.evaluate("location.hash='p8'");page.wait_for_timeout(60);page.locator('#pager-next').click();page.wait_for_timeout(60)
    if not page.locator('#p9').is_visible():errors.append('next navigation')
    page.locator('#pager-prev').click();page.wait_for_timeout(60)
    if not page.locator('#p8').is_visible():errors.append('previous navigation')
    if page.locator('#tab-original').get_attribute('aria-selected')!='true':errors.append('tab lost on navigation')
    if width<1024:page.locator('#p8 .problem-toggle').click()
    # Keyboard order is the same as the visible tab sequence.
    for key,target in [('Home','problem'),('ArrowRight','original'),('ArrowRight','provenance'),('ArrowRight','terms'),('ArrowLeft','provenance'),('End','terms'),('Home','problem')]:
     page.locator('[role=tab][aria-selected=true]').focus();page.keyboard.press(key)
     if page.locator('#tab-'+target).get_attribute('aria-selected')!='true':errors.append('keyboard tab order '+key)
    page.locator('#tab-original').click();page.reload(wait_until='networkidle')
    if page.locator('#tab-original').get_attribute('aria-selected')!='true':errors.append('original preference reload')
    if width>=1024:
     # Dock left/right/float and keyboard move/resize are provided by the fixed template.
     for dock in ['right','float','left']:
      page.locator(f'.prob-dock [data-dock="{dock}"]').click()
      if page.locator('.layout').get_attribute('data-prob-dock')!=dock:errors.append('dock '+dock)
      if not page.locator('[data-original-problem="p8"]').is_visible():errors.append('original dock '+dock)
      if dock=='float':
       for selector,key in [('.float-move','ArrowRight'),('.float-resize','ArrowDown')]:page.locator(selector).focus();page.keyboard.press(key)
       box=page.locator('#panel-prob').bounding_box()
       if box['x']<0 or box['y']<0 or box['x']+box['width']>width+1 or box['y']+box['height']>height+1:errors.append('floating bounds')
     for topic in ['p6','p8']:
      page.locator(f'#panel-left a[href="#{topic}"]').click();page.wait_for_timeout(80)
      if not page.locator(f'#{topic}').is_visible() or not page.locator(f'[data-original-problem="{topic}"]').is_visible():errors.append('toc original '+topic)
     page.locator('#toggle-left').click();page.locator('#toggle-prob').click();page.reload(wait_until='networkidle')
     if page.locator('.layout').get_attribute('data-left')!='closed' or page.locator('.layout').get_attribute('data-prob')!='closed':errors.append('closed persistence')
    else:
     page.locator('#toggle-left').click()
     if not page.locator('#panel-left').is_visible():errors.append('mobile toc')
     page.locator('#panel-left a[href="#p6"]').click();page.wait_for_timeout(80)
     toggle=page.locator('#p6 .problem-toggle')
     if toggle.get_attribute('aria-expanded')!='true':toggle.click()
     if not page.locator('[data-original-problem="p6"]').is_visible():errors.append('mobile toc original')
     if page.locator('#panel-left [data-panel-close]').is_visible():page.locator('#panel-left [data-panel-close]').click()
    page.emulate_media(media='print')
    # The math layout is scheduled asynchronously after panes move for print.
    page.wait_for_function("() => [...document.querySelectorAll('[data-source-problem],[data-original-problem]')].every(n=>n.getBoundingClientRect().height>0 && getComputedStyle(n).visibility==='visible')")
    printcheck=[page.locator('[data-source-problem]:visible').count(),page.locator('[data-original-problem]:visible').count()]
    print_checks.append({'viewport':f'{width}x{height}','theme':theme,'korean_visible':printcheck[0],'original_visible':printcheck[1]})
    if printcheck!=[10,10]:errors.append('print source/original preservation')
    errors+=failures+external;ctx.close()
  # Breakpoint transition in a fresh unsaved context.
  ctx=browser.new_context(viewport={'width':1023,'height':900},reduced_motion='reduce');p=ctx.new_page();p.goto(Path(path).resolve().as_uri(),wait_until='networkidle');p.evaluate("location.hash='p1'");p.wait_for_timeout(80)
  if p.locator('#toggle-prob').is_visible():errors.append('1023 breakpoint problem toggle')
  p.set_viewport_size({'width':1024,'height':900});p.wait_for_timeout(150)
  if not p.locator('#toggle-prob').is_visible() or p.locator('.layout').get_attribute('data-prob')!='open':errors.append('1024 breakpoint default open')
  if not p.locator('#tab-original').is_visible():errors.append('original lost across breakpoint')
  ctx.close()
  # Same directory keeps resources valid; remove only original data to test fallback.
  fixture=Path(path).with_name('.no-original-'+uuid.uuid4().hex+'.html')
  fixture.write_text(re.sub(r'<details class="original"[\s\S]*?</details>','',Path(path).read_text(encoding='utf-8')),encoding='utf-8')
  try:
   ctx=browser.new_context();ctx.add_init_script("localStorage.setItem('ml-problem-explain-tab',JSON.stringify('original'))")
   p=ctx.new_page();p.goto(fixture.resolve().as_uri(),wait_until='networkidle')
   if p.locator('#tab-original').is_visible():errors.append('empty original tab visible')
   if p.locator('#tab-problem').get_attribute('aria-selected')!='true':errors.append('missing original fallback')
   ctx.close()
  finally:fixture.unlink()
  behaviors=['all 10 topics; six viewport-theme combinations; full English title/conditions/tasks match','summary; mobile expand/collapse; no-original hidden/fallback fixture','previous/next; keyboard Home/End/Arrows; saved original preference','left/right/float dock; keyboard move/resize; floating viewport bounds','1023→1024; print Korean and English preservation']
  browser.close()
 report={'html_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'status':'fail' if errors else 'pass','topic_ids':[f'p{i}' for i in range(1,11)],'original_topic_ids':list(expected),'tab_order':['problem','original','provenance','terms'],'original_checks':original_checks,'print_checks':print_checks,'viewports':['1280x900','1024x900','375x812'],'themes':['light','dark'],'screens':screens,'behaviors':behaviors,'errors':errors}
 evidence.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':report['status'],'screens':len(screens),'errors':errors},ensure_ascii=False,indent=2));return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('html',type=Path);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--shots',type=Path,required=True);a=ap.parse_args();sys.exit(run_check(a.html,a.evidence,a.shots)['status']!='pass')
