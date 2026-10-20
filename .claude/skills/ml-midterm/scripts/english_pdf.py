"""Local English adapter over the pinned workbook layout and measurement gates."""
from pathlib import Path
from copy import deepcopy
from dataclasses import asdict
import json,re,uuid
from exam_config import config_for_output
from exam_adapter import sha,verify_baseline
from english_source import load_english_problems,english_payload,english_digests,INSTRUCTIONS,KOREAN
from review_pdf_layout import load_template,Layout,Typography
from review_pdf_types import RenderReport,LayoutIssue,ReviewPdfError
from review_pdf_render import _watch,_resources,GEOMETRY,TYPOGRAPHY
from review_pdf_payload import inject_data
from review_pdf_pages import paginate
from playwright.sync_api import sync_playwright

def english_template(repo:Path,layout:Layout,config):
 assets=Path(repo)/'.agents/skills/ml-review-pack/assets'
 provenance=json.loads((assets/'pdf-template-provenance.json').read_text())
 for v in provenance['templates'].values():
  if sha(assets/v['local_path'])!=v['sha256']:raise ValueError('pinned PDF template hash mismatch')
 text=load_template('problems',layout)
 for old,new in [('lang="ko"','lang="en"'),('<title>문제집</title>',f'<title>Midterm Practice {config.round_number:02d}</title>'),("block('문제 원문'","block('Original problem'"),("block('조건'","block('Given'"),("block('구할 것'","block('Tasks'"),('문제 데이터를 읽지 못했습니다:','Unable to read problem data:'),('content: "넘침"','content: "Overflow"')]:
  if text.count(old)!=1:raise ValueError('English template replacement mismatch: '+old)
  text=text.replace(old,new)
 vendor=Path(repo)/'.agents/skills/ml-problem-explain/assets/vendor'
 for url,rel in [('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css','pretendard/pretendard.css'),('https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css','katex/katex.min.css'),('https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js','katex/katex.min.js'),('https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js','katex/contrib/auto-render.min.js')]:
  if text.count(url)!=1:raise ValueError('missing local resource replacement: '+url)
  text=text.replace(url,(vendor/rel).resolve().as_uri())
 return text

def render_english(repo,payload,html_path,pdf_path=None,*,config,layout='video-16x9',typography=None):
 data=deepcopy(payload);html_path=Path(html_path);html_path.parent.mkdir(parents=True,exist_ok=True)
 if layout=='video-16x9':
  if typography is None or set(typography)!={p['id'] for p in data['problems']}:raise ValueError('missing or unexpected typography page ids')
  data['meta']['typography']=typography
 html_path.write_text(inject_data(english_template(repo,layout,config),data),encoding='utf-8')
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='chrome',headless=True)
  try:
   page=browser.new_context(viewport={'width':1400,'height':1000}).new_page();failures=_watch(page);external=[]
   page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) else None)
   page.emulate_media(media='print');page.goto(html_path.resolve().as_uri(),wait_until='load')
   page.wait_for_function('document.documentElement.dataset.ready');_resources(page,failures)
   if external:raise ReviewPdfError('external resources: '+str(external))
   if page.get_attribute('html','data-ready')!='true':raise ReviewPdfError('workbook data-ready error')
   g=page.evaluate(GEOMETRY);report=RenderReport(tuple(g['page_ids']),tuple(LayoutIssue(**i) for i in g['issues']),(),())
   if pdf_path is not None:
    if report.issues:raise ReviewPdfError('unresolved overflow: '+str(report.issues))
    page.pdf(path=str(pdf_path),prefer_css_page_size=True,print_background=True)
   return report,page.evaluate(TYPOGRAPHY)
  finally:browser.close()

def build_problems(repo,problems,stage,config):
 stage=Path(stage);stage.mkdir(parents=True,exist_ok=True);counter=0
 def payload(pages):
  data=english_payload(problems,config,pages)
  data['problems'][0]['html']['conditions']='<p>'+INSTRUCTIONS+'</p>'+data['problems'][0]['html']['conditions']
  return data
 def measure(pages):
  nonlocal counter
  counter+=1;data=payload(pages)
  _,scales=render_english(repo,data,stage/f'a4-{counter}.html',layout='a4',config=config)
  return render_english(repo,data,stage/f'measure-{counter}.html',typography=scales,config=config)[0]
 pages=paginate(problems,'problems',measure);data=payload(pages)
 _,scales=render_english(repo,data,stage/'a4-final.html',layout='a4',config=config)
 pdf=stage/(config.stem+'-문제-English.pdf')
 report,_=render_english(repo,data,stage/'english.html',pdf,typography=scales,config=config)
 from build_review_pdf import _verify_pdf
 import fitz
 _verify_pdf(pdf,len(report.page_ids),'video-16x9')
 with fitz.open(pdf) as doc:
  if KOREAN.search(''.join(p.get_text() for p in doc)):raise ValueError('Korean text in English PDF')
 mapping={p.card.id:[] for p in problems}
 for i,p in enumerate(pages,1):mapping[p.logical_id].append(i)
 return pdf,{'pages':mapping,'page_ids':list(report.page_ids),'page_count':len(report.page_ids),'layout':'video-16x9','page_size_pt':[1440,810],'caption_height_px':180,'typography':scales,'errors':[]}

def build_english_pdf(repo:Path,output:Path,run:Path):
 repo=Path(repo).resolve();output=Path(output).resolve();run=Path(run).resolve()
 config=config_for_output(repo,output)
 errors=verify_baseline(repo,Path(__file__).resolve().parents[1]/'references/baseline.json')
 if errors:raise ValueError('; '.join(errors))
 source=output/(config.stem+'.html');source_hash=sha(source)
 ps=load_english_problems(source,output/'.pack/blueprint.json',repo,config)
 pdf,report=build_problems(repo,ps,run/('english-'+uuid.uuid4().hex),config)
 if sha(source)!=source_hash:raise ValueError('source changed during English build')
 report.update(status='awaiting_visual_review',source_sha256=source_hash,english_digests=english_digests(ps),pdf_sha256=sha(pdf),logical_count=len(ps),subpart_count=sum(len(p.card.id) and len(__import__('mpe_source').subparts(p.ask_html,'')) for p in ps))
 path=pdf.parent/'english-pdf-validation.json';path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return {'problems_pdf':pdf,'report':path}
