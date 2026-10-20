"""Validate authored inputs, provenance, review gates and final delivery."""
from pathlib import Path
import json,sys,argparse
from exam_adapter import load_exam_source,STEM,sha,resolve,parse
from check_vector_derivatives import check_text

def validate_cards(cards_path,blueprint_path,repo):
 try:
  pack=load_exam_source(cards_path,blueprint_path,repo)
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
  pack=load_exam_source(output/(STEM+'.html'),output/'.pack/blueprint.json',repo)
  authored=[output/(STEM+'.html')]+list((output/'.pack/cards').glob('*.html'))+list((output/'.pack/explanations').glob('*.html'))
  errors += [str(p)+': '+e for p in authored for e in check_text(p.read_text(encoding='utf-8'))]
  errors+=validate_answer_checks(pack,json.loads((output/'.pack/evidence/answer-checks.json').read_text())['items'])
  delivery=json.loads((output/'.pack/delivery.json').read_text())
  errors+=check_file_hashes(output,delivery['files'],repo)
  for suffix in ['-문제.pdf','-답안.pdf']:
   p=output/(STEM+suffix)
   if not p.is_file() or p.name not in delivery['files']:errors.append('missing PDF: '+suffix)
  from mpe_render import names,md_name,check_artifacts,artifact_hashes
  from mpe_types import Artifacts
  from mpe_contract import validate_reviews
  stem,fig,data=names(pack);manifest=output/data/'manifest.json'
  m=json.loads(manifest.read_text());files=tuple(output/n for n in m['files'])+(manifest,)
  artifacts=Artifacts(output/(stem+'.html'),output/md_name(pack),manifest,files)
  browser=json.loads((output/'.pack/evidence/browser-check.json').read_text())
  if browser.get('status')!='pass' or browser.get('html_sha256')!=sha(artifacts.html):errors.append('stale browser review')
  pdf_report=json.loads((output/'.pack/evidence/pdf-validation.json').read_text())
  if pdf_report.get('source_sha256')!=pack.sha256 or pdf_report.get('logical_count')!=10:errors.append('stale PDF source')
  reviews=json.loads((output/data/'validation.json').read_text());fragments={p.id:(output/f'.pack/explanations/{p.id}.html').read_text() for p in pack.problems}
  errors+=check_artifacts(pack,artifacts)+validate_reviews(pack,fragments,reviews)
  if reviews.get('artifact_hashes')!=artifact_hashes(artifacts):errors.append('stale artifact approval')
  for ref in reviews.get('references',[]):
   p=resolve(repo,ref['path'])
   if sha(p)!=ref['sha256']:errors.append('stale reference: '+ref['path'])
  if str((output/'.pack/blueprint.json').resolve()) not in {x['path'] for x in reviews['references']}:errors.append('blueprint not bound')
  if delivery.get('logical_count')!=10 or delivery.get('subpart_count')!=sum(len(p.subparts) for p in pack.problems):errors.append('invalid delivery counts')
 except (OSError,ValueError,KeyError,TypeError) as e:errors.append(str(e))
 return errors
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);a=ap.parse_args();errors=check_delivery(a.out.resolve(),a.repo.resolve());print(json.dumps({'status':'fail' if errors else 'pass','errors':errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
