"""Exercise the existing reading UI in real Chrome, with offline local resources."""
from pathlib import Path
import json,sys,argparse,hashlib
from playwright.sync_api import sync_playwright

def run_check(path,evidence,shots):
 evidence=Path(evidence);shots=Path(shots);shots.mkdir(parents=True,exist_ok=True)
 errors=[];screens=[];behaviors=[]
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
     if page.locator('#tab-original').is_visible():errors.append('empty original tab visible')
     if width<1024:
      toggle=page.locator(f'#p{n} .problem-toggle');toggle.click()
      if not page.locator(f'#problem-p{n}').is_visible():errors.append(f'mobile problem p{n}')
      toggle.click()
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
    # Prev/next must preserve actual article sequence.
    page.evaluate("location.hash='p8'");page.wait_for_timeout(60);page.locator('#pager-next').click();page.wait_for_timeout(60)
    if not page.locator('#p9').is_visible():errors.append('next navigation')
    page.locator('#pager-prev').click();page.wait_for_timeout(60)
    if not page.locator('#p8').is_visible():errors.append('previous navigation')
    if width>=1024:
     # Dock left/right/float and keyboard move/resize are provided by the fixed template.
     for dock in ['right','float','left']:
      page.locator(f'.prob-dock [data-dock="{dock}"]').click()
      if page.locator('.layout').get_attribute('data-prob-dock')!=dock:errors.append('dock '+dock)
      if dock=='float':
       for selector,key in [('.float-move','ArrowRight'),('.float-resize','ArrowDown')]:page.locator(selector).focus();page.keyboard.press(key)
       box=page.locator('#panel-prob').bounding_box()
       if box['x']<0 or box['y']<0 or box['x']+box['width']>width+1 or box['y']+box['height']>height+1:errors.append('floating bounds')
     page.locator('#toggle-left').click();page.locator('#toggle-prob').click();page.reload(wait_until='networkidle')
     if page.locator('.layout').get_attribute('data-left')!='closed' or page.locator('.layout').get_attribute('data-prob')!='closed':errors.append('closed persistence')
    else:
     page.locator('#toggle-left').click()
     if not page.locator('#panel-left').is_visible():errors.append('mobile toc')
     page.locator('#panel-left [data-panel-close]').click()
    page.emulate_media(media='print');printcheck=page.evaluate("() => [...document.querySelectorAll('[data-source-problem]')].length")
    if printcheck!=10:errors.append('print source preservation')
    errors+=failures+external;ctx.close()
  # Breakpoint transition in a fresh unsaved context.
  ctx=browser.new_context(viewport={'width':1023,'height':900},reduced_motion='reduce');p=ctx.new_page();p.goto(Path(path).resolve().as_uri(),wait_until='networkidle');p.evaluate("location.hash='p1'");p.wait_for_timeout(80)
  if p.locator('#toggle-prob').is_visible():errors.append('1023 breakpoint problem toggle')
  p.set_viewport_size({'width':1024,'height':900});p.wait_for_timeout(150)
  if not p.locator('#toggle-prob').is_visible() or p.locator('.layout').get_attribute('data-prob')!='open':errors.append('1024 breakpoint default open')
  behaviors=['all 10 topics; local KaTeX/Pretendard; six viewport-theme combinations','summary contents; mobile problem expand/collapse; original tab hidden without original','previous/next; toc; saved closed state','left/right/float dock; keyboard move/resize; floating viewport bounds','1023→1024; print source preservation']
  ctx.close();browser.close()
 report={'html_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'status':'fail' if errors else 'pass','topic_ids':[f'p{i}' for i in range(1,11)],'viewports':['1280x900','1024x900','375x812'],'themes':['light','dark'],'screens':screens,'behaviors':behaviors,'errors':errors}
 evidence.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':report['status'],'screens':len(screens),'errors':errors},ensure_ascii=False,indent=2));return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('html',type=Path);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--shots',type=Path,required=True);a=ap.parse_args();sys.exit(run_check(a.html,a.evidence,a.shots)['status']!='pass')
