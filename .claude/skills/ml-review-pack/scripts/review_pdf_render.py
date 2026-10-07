"""Chrome renderer with resource, font and geometry gates."""
from pathlib import Path
import base64
from copy import deepcopy
from review_pdf_layout import Layout, Typography, load_template
from playwright.sync_api import sync_playwright, Error as BrowserError
from html2md import SVG_CSS
from urllib.parse import urljoin,urlparse
from review_pdf_cards import parse,inner
from review_pdf_payload import inject_data
from review_pdf_types import FigureAsset, LayoutIssue, RenderReport, ReviewPdfError
ASSETS=Path(__file__).resolve().parent.parent/'assets'


def _watch(page):
    failures=[]
    page.on('requestfailed',lambda r:failures.append(f'{r.url}: {r.failure}'))
    page.on('response',lambda r:failures.append(f'{r.url}: HTTP {r.status}') if r.status>=400 else None)
    page.on('pageerror',lambda e:failures.append(f'JavaScript: {e}'))
    return failures


def _resources(page, failures):
    page.evaluate('''async () => {await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(()=>{})));}''')
    missing=page.evaluate('''() => ({images:[...document.images].filter(i=>!i.complete || !i.naturalWidth).map(i=>i.src),fonts:[...document.fonts].filter(f=>f.status==='error').map(f=>f.family),katex:typeof katex==='undefined' || typeof renderMathInElement==='undefined',pretendard:![...document.fonts].some(f=>f.family.includes('Pretendard') && f.status==='loaded')})''')
    errors=page.locator('.katex-error').all_text_contents()
    if failures or missing['images'] or missing['fonts'] or missing['katex'] or missing['pretendard']:
        raise ReviewPdfError(f'resource failure: {failures}; {missing}')
    if errors:raise ReviewPdfError(f'KaTeX error: {errors}')


def freeze_figures(pack,build_dir):
    build_dir=Path(build_dir);build_dir.mkdir(parents=True,exist_ok=True);assets={}
    if not any(c.figures for c in pack.cards):return assets
    with sync_playwright() as pw:
        browser=pw.chromium.launch(channel='chrome',headless=True)
        try:
            ctx=browser.new_context(viewport={'width':1400,'height':1000},device_scale_factor=300/96)
            page=ctx.new_page();failures=_watch(page)
            head=(ASSETS/'pdf-problem.html').read_text(encoding='utf-8').split('<style>')[0]
            for c in pack.cards:
                for f in c.figures:
                    path=build_dir/f'{c.id}-{f.id}.html'
                    css=SVG_CSS+'''body {margin:0;background:white;color:#1b2130;font-family:Pretendard,sans-serif;font-size:16px;} #capture {display:inline-block;padding:8px;background:white;} table {border-collapse:collapse;background:white;color:#1b2130;} th,td {border:1px solid #4a5468;padding:8px 12px;text-align:center;} svg {display:block;max-width:900px;} .figure {margin:0;} figcaption {font-size:13px;text-align:center;}'''
                    figure=parse(f.html)
                    for node in figure.find_all(lambda n:n.tag=='img'):
                        src=node.attrs.get('src','')
                        if not urlparse(src).scheme:
                            if pack.source_path is None:
                                raise ReviewPdfError(f'{c.id}: source path required for relative image {src}')
                            node.attrs['src']=urljoin(pack.source_path.as_uri(),src)
                    path.write_text(head+f'<style>{css}</style></head><body><div id="capture">'+inner(figure)+'''</div><script>addEventListener('DOMContentLoaded',async()=>{await document.fonts.ready;renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});await document.fonts.ready;document.documentElement.dataset.ready='true';});</script></body></html>''',encoding='utf-8')
                    failures.clear();page.goto(path.resolve().as_uri(),wait_until='load',timeout=120000)
                    page.wait_for_function("document.documentElement.dataset.ready==='true'",timeout=120000)
                    _resources(page,failures)
                    box=page.locator('#capture').bounding_box()
                    png=page.locator('#capture').screenshot(path=str(build_dir/f'{c.id}-{f.id}.png'),animations='disabled')
                    assets[(c.id,f.id)]=FigureAsset('data:image/png;base64,'+base64.b64encode(png).decode(),box['width']*25.4/96,box['height']*25.4/96)
        except BrowserError as e:raise ReviewPdfError(f'{pack.range}: figure resource/render failure: {e}') from e
        finally:browser.close()
    return assets


GEOMETRY = r'''() => {
 const issues=[];const pages=[...document.querySelectorAll('#book > .page')];
 const add=(p,a,d)=>issues.push({page_id:p.id || 'hint',area:a,detail:d});
 const outside=(r,b)=>r.left<b.left-1||r.right>b.right+1||r.top<b.top-1||r.bottom>b.bottom+1;
 for(const p of pages){
  p.style.zoom='';
  if(window.workbookVideoLayout){
   const boundary=p.getBoundingClientRect().top+900;
   const visible=n=>{const c=getComputedStyle(n);return c.display!=='none'&&c.visibility!=='hidden'&&c.opacity!=='0'&&!n.closest('.sr');};
   for(const n of p.querySelectorAll('*')){
    if(!visible(n))continue;
    const c=getComputedStyle(n),r=n.getBoundingClientRect();
    const ink=c.backgroundColor!=='rgba(0, 0, 0, 0)'&&c.backgroundColor!=='rgb(255, 255, 255)';
    const border=['Top','Bottom','Left','Right'].some(side=>parseFloat(c['border'+side+'Width'])>0&&c['border'+side+'Style']!=='none');
    if(r.width>0&&r.height>0&&r.bottom>boundary+.5&&(n.matches('img,svg,canvas,.panel,.work,.hint-cols')||ink||border))add(p,'caption','element enters reserved caption band');
    for(const t of n.childNodes){
     if(t.nodeType!==Node.TEXT_NODE||!t.textContent.trim())continue;
     const range=document.createRange();range.selectNodeContents(t);
     for(const b of range.getClientRects())if(b.width>0&&b.height>0&&b.bottom>boundary+.5)add(p,'caption','text enters reserved caption band');
    }
   }
  }
  const panel=p.querySelector('.panel'),work=p.querySelector('.work'),cols=p.querySelector('.hint-cols');
  if(panel){
   const b=panel.getBoundingClientRect();
   if(panel.scrollHeight>panel.clientHeight+1)add(p,'panel','panel scroll height');
   for(const n of panel.querySelectorAll('.block')) if(outside(n.getBoundingClientRect(),b))add(p,'panel','block outside panel');
  }
  if(work){
   const b=work.getBoundingClientRect();
   if(b.width<=1||b.height<=1)add(p,'work','missing writing space');
   const flow=work.querySelector('.sol-flow');
   if(flow)for(const n of flow.querySelectorAll('.sol-step'))if(outside(n.getBoundingClientRect(),flow.getBoundingClientRect()))add(p,'work','solution step outside flow');
   const ans=work.querySelector('.sol-answer');
   if(ans){
    if(outside(ans.getBoundingClientRect(),b))add(p,'answer','answer outside work');
    for(const n of ans.querySelectorAll('.prose,.prose > *:not(.katex-display)'))if(outside(n.getBoundingClientRect(),b))add(p,'answer','answer content outside work');
   }
  }
  if(cols){
   if(cols.scrollWidth>cols.clientWidth+1)add(p,'hint','Hint columns overflow');
   for(const n of cols.querySelectorAll('.hint-item'))if(outside(n.getBoundingClientRect(),cols.getBoundingClientRect()))add(p,'hint','Hint item outside columns');
  }
  for(const n of p.querySelectorAll('.fig')){
   const band=n.closest('.fig-band');if(band&&outside(n.getBoundingClientRect(),band.getBoundingClientRect()))add(p,'figure','figure outside band');
  }
  for(const n of p.querySelectorAll('.katex')){
   const owner=n.closest('.prose,.hint-item,.sol-flow');
   if(owner&&outside(n.getBoundingClientRect(),owner.getBoundingClientRect()))add(p,'math','visible math outside prose');
  }
  for(const owner of p.querySelectorAll('.prose')){
   const area=owner.closest('.panel')?'panel':owner.closest('.sol-answer')?'answer':owner.closest('.hint-cols')?'hint':'work';
   for(const n of owner.children){
    if(n.closest('.katex') || n.classList.contains('katex-display'))continue;
    for(const r of n.getClientRects())if(r.width>0 && r.height>0 && outside(r,owner.getBoundingClientRect()))add(p,area,'visible content outside prose');
   }
  }
 }
 // Pagination consumes its first issue: repair semantic overflow before caption safety.
 issues.sort((a,b)=>Number(a.area==='caption')-Number(b.area==='caption'));
 return {page_ids:pages.map((p,i)=>p.id||'hint-page-'+(i+1)),issues};
}'''


TYPOGRAPHY = r"""() => {
 const appendix=id=>[...document.querySelectorAll('#book > .page--hint .hint-entry-num')].filter(n=>n.getAttribute('href')==='#'+id).flatMap(n=>[...n.closest('.hint-entry').querySelectorAll('.katex-display > .katex')]);
 const scale=n=>{const t=getComputedStyle(n).transform;return t==='none'?1:parseFloat(t.slice(7).split(',')[0]);};
 return Object.fromEntries([...document.querySelectorAll('#book > .page--problem')].map(p=>[p.id,{
  panel:parseFloat(getComputedStyle(p.querySelector('.panel')).getPropertyValue('--fs'))||1,
  solution:p.querySelector('.work')?(parseFloat(getComputedStyle(p.querySelector('.work')).getPropertyValue('--sfs'))||1):1,
  math:[...p.querySelectorAll('.katex-display > .katex')].map(scale),
  hints:[...p.querySelectorAll('.hint-strip-formula')].map(scale),
  appendix_math:appendix(p.id).map(scale)
 }]));
}"""


def measure_typography(payload: dict, mode: str, html_path: Path) -> Typography:
    return _render_document(payload, mode, html_path)[1]


def render_workbook(payload, mode, html_path, pdf_path=None, *, layout: Layout='a4', typography: Typography | None=None):
    return _render_document(payload,mode,html_path,pdf_path,layout=layout,typography=typography)[0]


def _render_document(payload,mode,html_path,pdf_path=None,*,layout: Layout='a4',typography: Typography | None=None):
    if mode not in ('problems','answers'):raise ReviewPdfError(f'invalid mode: {mode}')
    html_path=Path(html_path);html_path.parent.mkdir(parents=True,exist_ok=True)
    template=load_template(mode,layout)
    payload=deepcopy(payload)
    if layout=='video-16x9':
        expected={p['id'] for p in payload['problems']}
        if typography is None or expected != set(typography):raise ReviewPdfError('missing or unexpected typography page ids')
        if any('appendix_math' not in scales for scales in typography.values()):raise ReviewPdfError('missing Hint appendix typography')
        payload['meta']['typography']=typography
    html_path.write_text(inject_data(template,payload),encoding='utf-8')
    with sync_playwright() as pw:
        browser=pw.chromium.launch(channel='chrome',headless=True)
        try:
            page=browser.new_context(viewport={'width':1400,'height':1000}).new_page();failures=_watch(page)
            page.emulate_media(media='print')
            page.goto(html_path.resolve().as_uri(),wait_until='load',timeout=120000)
            page.wait_for_function('document.documentElement.dataset.ready',timeout=120000)
            _resources(page,failures)
            if page.get_attribute('html','data-ready')!='true':raise ReviewPdfError('workbook data-ready error')
            if layout=='video-16x9':
                # Hint entries may move between appendix pages. Match their stable target,
                # then restore display math in item order without editing pinned templates.
                mismatch=page.evaluate(r'''scales => {
                  for(const [id,values] of Object.entries(scales)){
                    const nodes=[...document.querySelectorAll('#book > .page--hint .hint-entry-num')]
                      .filter(n=>n.getAttribute('href')==='#'+id)
                      .flatMap(n=>[...n.closest('.hint-entry').querySelectorAll('.katex-display > .katex')]);
                    if(nodes.length!==values.appendix_math.length)return id;
                    nodes.forEach((node,i)=>{
                      node.style.transformOrigin='left center';
                      node.style.transform=values.appendix_math[i]<1?`scale(${values.appendix_math[i]})`:'';
                    });
                  }
                  return null;
                }''',typography)
                if mismatch:raise ReviewPdfError(f'{mismatch}: Hint appendix math correspondence changed')
            geometry=page.evaluate(GEOMETRY)
            report=RenderReport(tuple(geometry['page_ids']),tuple(LayoutIssue(**i) for i in geometry['issues']),(),())
            if pdf_path is not None:
                if report.issues:raise ReviewPdfError(f'{mode}: unresolved overflow: {report.issues}')
                pdf_path=Path(pdf_path);pdf_path.parent.mkdir(parents=True,exist_ok=True)
                page.pdf(path=str(pdf_path),prefer_css_page_size=True,print_background=True)
            return report,page.evaluate(TYPOGRAPHY)
        except BrowserError as e:raise ReviewPdfError(f'{mode}: resource/render failure: {e}') from e
        finally:browser.close()
