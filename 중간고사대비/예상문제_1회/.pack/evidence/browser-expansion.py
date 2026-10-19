from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib
RUN=Path(__file__).resolve().parent
result=json.loads((RUN/'explanation-result.json').read_text(encoding='utf-8'))
HTML=Path(result['html']);SHOTS=RUN/'browser';SHOTS.mkdir(exist_ok=True)
def run():
    samples=[];errors=[];external=[];missing=[];console=[];interactions=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for w,h in [(1280,900),(1024,900),(375,812)]:
            for theme in ['light','dark']:
                ctx=browser.new_context(viewport={'width':w,'height':h},color_scheme=theme,reduced_motion='reduce')
                page=ctx.new_page()
                page.set_default_timeout(5000)
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('console',lambda m:console.append(m.text) if m.type=='error' else None)
                page.on('request',lambda r:external.append(r.url) if r.url.startswith(('https:','http:')) else None)
                page.on('requestfailed',lambda r:missing.append({'url':r.url,'failure':r.failure}))
                page.goto(HTML.as_uri()+'#p1',wait_until='load');page.evaluate('document.fonts.ready');page.wait_for_timeout(250)
                for n in range(1,11):
                    page.evaluate('(id)=>{location.hash=id}',f'p{n}');page.wait_for_timeout(60)
                    root=page.locator(f'#p{n}')
                    assert root.is_visible(),f'p{n} invisible'
                    solve=root.locator('[data-explanation="solve"]')
                    solve.scroll_into_view_if_needed()
                    page.evaluate('(id)=>document.querySelector(id).scrollIntoView({block:"start"})',f'#p{n} [data-explanation="solve"]')
                    data=root.evaluate('''el=>({
                        horizontal_overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth),
                        katex_errors:el.querySelectorAll('.katex-error').length,
                        rendered_math:el.querySelectorAll('.katex').length,
                        solve:el.querySelectorAll('[data-explanation="solve"] [data-subpart]').length,
                        verify:el.querySelectorAll('[data-explanation="verify"] [data-subpart]').length,
                        math_overflow:[...el.querySelectorAll('.katex-display')].filter(x=>x.scrollWidth>x.clientWidth+2).map(x=>({text:x.innerText,width:x.clientWidth,scroll:x.scrollWidth})),
                        clipped_inline:[...el.querySelectorAll('p > .katex')].filter(x=>x.getBoundingClientRect().width>x.closest('p').clientWidth+2).map(x=>x.innerText),
                        gaps:[...el.querySelectorAll('[data-explanation]')].map(x=>({section:x.dataset.explanation,margin:getComputedStyle(x).marginTop})),
                        static_problem:document.querySelectorAll('#tabpanel-problem [data-answer]').length===0
                    })''')
                    data.update(topic=f'p{n}',viewport=f'{w}x{h}',theme=theme)
                    samples.append(data)
                    page.screenshot(path=str(SHOTS/f'{w}-{theme}-p{n}.png'))
                    # Every newly authored subpart gets a rendering and dimensions check.
                    for sub in solve.locator('[data-subpart]').all():
                        sub.scroll_into_view_if_needed()
                        assert sub.bounding_box()['height']>20
                    assert data['solve']==data['verify']
                # Use real controls on p4, including mobile drawer behavior.
                page.evaluate('location.hash="p4"');page.wait_for_timeout(60)
                if w<1024:
                    page.locator('#toggle-left').click();assert page.locator('#toggle-left').get_attribute('aria-expanded')=='true'
                page.locator('.toc a[href="#p5"]').click();page.wait_for_timeout(60)
                assert page.locator('#p5').is_visible()
                page.locator('#pager-next').click();assert page.locator('#p6').is_visible()
                page.locator('#pager-prev').click();assert page.locator('#p5').is_visible()
                page.locator('#toggle-right').click();assert page.locator('#toggle-right').get_attribute('aria-expanded')=='true'
                assert page.locator('#panel-right').inner_text().strip()
                if w<1024: page.locator('#panel-right [data-panel-close]').click()
                else: page.locator('#toggle-right').click()
                if w>=1024:
                    for dock in ['right','float','left']:
                        page.locator(f'.prob-dock [data-dock="{dock}"]').click()
                        assert page.locator('.layout').get_attribute('data-prob-dock')==dock
                    page.locator('#tab-terms').click();assert page.locator('#tabpanel-terms').is_visible()
                    page.locator('#tab-provenance').click();assert page.locator('#tabpanel-provenance').is_visible()
                    page.locator('#tab-problem').click()
                    assert not page.locator('#tab-original').is_visible()
                page.locator('#theme-toggle').click()
                interactions.append({'viewport':f'{w}x{h}','theme':theme,'toc_prev_next_summary_theme':'pass','dock_and_tabs':'pass' if w>=1024 else 'mobile collapsed'})
                (RUN/'browser-checkpoint.json').write_text(json.dumps({'samples':samples,'interactions':interactions},ensure_ascii=False,indent=2),encoding='utf-8')
                ctx.close()
        # Breakpoint defaults in fresh storage, then preserve explicit closed state.
        ctx=browser.new_context(viewport={'width':1023,'height':900},reduced_motion='reduce');page=ctx.new_page()
        page.goto(HTML.as_uri()+'#p4');page.wait_for_timeout(100)
        boundary={'1023':page.locator('.layout').get_attribute('data-left')}
        page.set_viewport_size({'width':1024,'height':900});page.wait_for_timeout(100)
        boundary['1024']=page.locator('.layout').get_attribute('data-left')
        assert boundary=={'1023':'closed','1024':'open'},boundary
        page.locator('#toggle-prob').click();page.reload();page.wait_for_timeout(100)
        assert page.locator('#toggle-prob').get_attribute('aria-expanded')=='false'
        # Confirm equations survive print media; problem source is still present.
        page.emulate_media(media='print');assert page.locator('#p4 [data-explanation="solve"] .katex').count()>0
        ctx.close();browser.close()
    issues=[x for x in samples if x['horizontal_overflow'] or x['katex_errors'] or x['math_overflow'] or x['clipped_inline'] or not x['rendered_math']]
    report={'status':'fail' if issues or errors or external or missing or console else 'pass','html_sha256':hashlib.sha256(HTML.read_bytes()).hexdigest(),'reviewer':'Codex / Chromium Playwright','samples':samples,'issues':issues,'page_errors':errors,'console_errors':console,'external_requests':external,'missing_resources':missing,'interactions':interactions,'boundary':boundary,'evidence':'browser/*.png; browser_check.py: 60 topic/viewport/theme cases, all solve subparts traversed'}
    (RUN/'browser-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['samples','interactions']},ensure_ascii=False))
    return report
if __name__=='__main__':run()
