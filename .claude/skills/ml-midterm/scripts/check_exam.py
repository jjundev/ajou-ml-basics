"""Validate authored inputs, provenance, review gates and final delivery."""
from pathlib import Path
import json,sys,argparse
from exam_adapter import explanation_tabs,load_exam_source,resolve_reference,sha,resolve,parse
from exam_config import config_for_output
from check_vector_derivatives import check_text

def validate_browser_report(report,path):
 from itertools import product
 errors=[]
 ids=[f'p{i}' for i in range(1,11)]
 views=['1280x900','1024x900','375x812'];themes=['light','dark']
 if report.get('status')!='pass' or report.get('errors')!=[] or report.get('html_sha256')!=sha(path):errors.append('stale browser review')
 doc=parse(Path(path).read_text(encoding='utf-8'))
 topic=next(doc.find_all(lambda node:node.tag=='article' and node.attrs.get('id')=='p8'),None)
 if report.get('topic_ids')!=ids or report.get('original_topic_ids')!=ids or topic is None or report.get('tab_order')!=explanation_tabs(topic):errors.append('browser topic/tab mismatch')
 expected=set(product(views,themes,ids))
 for key in ('screens','original_checks'):
  rows=report.get(key,[])
  if len(rows)!=60 or {(x.get('viewport'),x.get('theme'),x.get('topic')) for x in rows}!=expected:errors.append('incomplete browser '+key)
  if key=='screens' and any(any(x.get(k)!=0 for k in ('horizontal_overflow','katex_errors','unloaded_images','missing_fonts')) for x in rows):errors.append('browser rendering errors')
  if key=='original_checks' and any(not x.get('content_matches') or not x.get('active') or x.get('visible_count')!=1 for x in rows):errors.append('browser original mismatch')
 rows=report.get('print_checks',[])
 if len(rows)!=6 or {(x.get('viewport'),x.get('theme')) for x in rows}!=set(product(views,themes)) or any(x.get('korean_visible')!=10 or x.get('original_visible')!=10 for x in rows):errors.append('browser print incomplete')
 return errors

def check_english_delivery(output,repo):
 try:
  from english_source import load_english_problems,english_digests
  output=Path(output);config=config_for_output(repo,output);source=resolve(repo,output/(config.stem+'.html'));pdf=resolve(repo,output/(config.stem+'-문제-English.pdf'))
  r=json.loads((output/'.pack/evidence/english-pdf-validation.json').read_text(encoding='utf-8'))
  ps=load_english_problems(source,output/'.pack/blueprint.json',repo,config)
  if r.get('status')!='pass' or r.get('errors')!=[] or r.get('source_sha256')!=sha(source) or r.get('english_digests')!=english_digests(ps) or r.get('pdf_sha256')!=sha(pdf):return ['stale English PDF/source/review']
  if r.get('logical_count')!=10 or r.get('subpart_count')!=sum(len(__import__('mpe_source').subparts(p.ask_html,'')) for p in ps) or set(r['pages'])!={f'p{i}' for i in range(1,11)} or any(not x for x in r['pages'].values()):return ['English PDF page mapping missing']
  import fitz
  with fitz.open(pdf) as doc:
   pages=[n for nums in r['pages'].values() for n in nums]
   if sorted(pages)!=list(range(1,len(doc)+1)) or len(doc)!=r['page_count'] or len(r['page_ids'])!=len(doc):return ['English PDF physical page mismatch']
   for pid,nums in r['pages'].items():
    if [r['page_ids'][n-1] for n in nums]!=[pid if i==1 else f'{pid}-c{i}' for i in range(1,len(nums)+1)]:return ['English PDF page ID mismatch']
   visual=r.get('visual_review',{})
   if (not isinstance(visual,dict) or any(not isinstance(visual.get(k),str) or not visual[k].strip() for k in ('reviewer','evidence'))
       or visual.get('pages')!=list(range(1,len(doc)+1))):return ['English PDF whole-page visual review missing']
  delivery=json.loads((output/'.pack/delivery.json').read_text(encoding='utf-8'))
  if pdf.name not in delivery['files']:return ['English PDF not delivered']
  return []
 except (ValueError,OSError,KeyError,TypeError) as e:return ['English PDF: '+str(e)]

def validate_cards(cards_path,blueprint_path,repo,config):
 try:
  pack=load_exam_source(cards_path,blueprint_path,repo,config)
  if len(pack.problems)!=10:return ['expected 10 problems']
  return []
 except (ValueError,OSError) as e:return [str(e)]

def validate_answer_checks(pack,checks):
 expected={f'{p.id}:{s}' for p in pack.problems for s in p.subparts}
 if set(checks)!=expected:return ['missing or extra answer check']
 return [f'{key}: unresolved answer' for key,v in checks.items() if v.get('status')!='pass' or not v.get('conclusion') or not v.get('evidence') or v.get('method') not in ('exact','symbolic','proof','qualitative','numerical')]

def check_file_hashes(output,files,repo):
 errors=[]
 for rel,digest in files.items():
  try:
   p=resolve(repo,Path(output)/rel)
   if sha(p)!=digest:errors.append('delivery hash mismatch: '+rel)
  except (OSError,ValueError):errors.append('delivery file missing: '+rel)
 return errors

def check_delivery(output,repo):
 output=Path(output);errors=[]
 try:
  config=config_for_output(repo,output)
  pack=load_exam_source(output/(config.stem+'.html'),output/'.pack/blueprint.json',repo,config)
  authored=[pack.path]+list((output/'.pack/cards').glob('*.html'))+list((output/'.pack/explanations').glob('*.html'))
  errors += [str(p)+': '+e for p in authored for e in check_text(p.read_text(encoding='utf-8'))]
  errors+=validate_answer_checks(pack,json.loads((output/'.pack/evidence/answer-checks.json').read_text(encoding='utf-8'))['items'])
  delivery=json.loads((output/'.pack/delivery.json').read_text(encoding='utf-8'))
  errors+=check_file_hashes(output,delivery['files'],repo)
  for suffix in ['-문제.pdf','-답안.pdf']:
   p=output/(config.stem+suffix)
   if not p.is_file() or p.name not in delivery['files']:errors.append('missing PDF: '+suffix)
  from mpe_render import names,md_name,check_artifacts,artifact_hashes
  from mpe_types import Artifacts
  from mpe_contract import validate_reviews
  stem,fig,data=names(pack);manifest=output/data/'manifest.json'
  m=json.loads(manifest.read_text(encoding='utf-8'));files=tuple(output/n for n in m['files'])+(manifest,)
  artifacts=Artifacts(output/(stem+'.html'),output/md_name(pack),manifest,files)
  browser=json.loads((output/'.pack/evidence/browser-check.json').read_text(encoding='utf-8'))
  errors+=validate_browser_report(browser,artifacts.html)
  pdf_report=json.loads((output/'.pack/evidence/pdf-validation.json').read_text(encoding='utf-8'))
  if pdf_report.get('logical_count')!=10:errors.append('stale PDF count')
  if pdf_report.get('source_sha256')!=pack.sha256:
   from pdf_binding import check_pdf_binding
   errors+=check_pdf_binding(output,repo,config)
  errors+=check_english_delivery(output,repo)
  reviews=json.loads((output/data/'validation.json').read_text(encoding='utf-8'));fragments={p.id:(output/f'.pack/explanations/{p.id}.html').read_text(encoding='utf-8') for p in pack.problems}
  from exam_adapter import explanation_resources
  resources=explanation_resources(pack,fragments,repo)
  recorded={}
  for ref in reviews.get('references',[]):
   try:found=resolve_reference(repo,ref['path'],ref['sha256'])
   except (OSError,ValueError) as e:errors.append(str(e));continue
   recorded[str(found)]=ref['sha256']
   if sha(found)!=ref['sha256']:errors.append('stale reference: '+ref['path'])
  if any(recorded.get(path)!=digest for path,digest in resources.items()):errors.append('stale or missing image resource approval')
  required={config.stem+'.html',stem+'.html',md_name(pack),data+'/manifest.json',data+'/validation.json',
            '.pack/blueprint.json','.pack/evidence/answer-checks.json','.pack/evidence/browser-check.json',
            '.pack/evidence/pdf-validation.json','.pack/evidence/english-pdf-validation.json',
            *(config.stem+suffix for suffix in ('-문제.pdf','-답안.pdf','-문제-English.pdf')),*m['files']}
  if pdf_report.get('source_sha256')!=pack.sha256:
   required.add('.pack/evidence/korean-pdf-binding.json')
   binding=json.loads((output/'.pack/evidence/korean-pdf-binding.json').read_text(encoding='utf-8'))
   required.add(binding['snapshot_path'])
  errors+=['delivery missing: '+name for name in sorted(required-set(delivery['files']))]
  errors+=check_artifacts(pack,artifacts)+validate_reviews(pack,fragments,reviews)
  if reviews.get('artifact_hashes')!=artifact_hashes(artifacts):errors.append('stale artifact approval')
  if str(resolve(repo,output/'.pack/blueprint.json')) not in recorded:errors.append('blueprint not bound')
  if delivery.get('logical_count')!=10 or delivery.get('subpart_count')!=sum(len(p.subparts) for p in pack.problems):errors.append('invalid delivery counts')
 except (OSError,ValueError,KeyError,TypeError) as e:errors.append(str(e))
 return errors
if __name__=='__main__':
 for stream in (sys.stdout, sys.stderr):
  stream.reconfigure(encoding='utf-8')
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);a=ap.parse_args();errors=check_delivery(a.out.resolve(),a.repo.resolve());print(json.dumps({'status':'fail' if errors else 'pass','errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
