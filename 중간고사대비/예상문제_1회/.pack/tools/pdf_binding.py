"""Bind unchanged Korean PDFs to their exact historical input and Korean fields."""
from pathlib import Path
from dataclasses import asdict
import json,hashlib
from exam_adapter import EXAM,STEM,read_cards,sha,resolve

def korean_content_digest(source:Path):
 cards=[]
 for c in read_cards(source,EXAM).cards:
  record=asdict(c);record.pop('original_html');cards.append(record)
 return hashlib.sha256(json.dumps(cards,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def binding_record(output):
 output=Path(output);e=output/'.pack/evidence';source=output/(STEM+'.html');snapshot=e/'korean-pdf-source'/source.name
 old=json.loads((e/'pdf-validation.json').read_text())
 if sha(snapshot)!=old['source_sha256']:raise ValueError('historical PDF source mismatch')
 digest=korean_content_digest(source)
 if digest!=korean_content_digest(snapshot):raise ValueError('Korean content changed')
 return {'schema_version':1,'snapshot_path':snapshot.relative_to(output).as_posix(),'snapshot_sha256':sha(snapshot),'pdf_report_sha256':sha(e/'pdf-validation.json'),'current_source_sha256':sha(source),'korean_content_digest':digest,'pdfs':{STEM+suffix:sha(output/(STEM+suffix)) for suffix in ['-문제.pdf','-답안.pdf']}}

def check_pdf_binding(output:Path,repo:Path):
 try:
  output=Path(output);b=json.loads((output/'.pack/evidence/korean-pdf-binding.json').read_text())
  if b!=binding_record(output):return ['stale Korean PDF binding']
  snapshot=resolve(repo,output/b['snapshot_path'])
  if sha(snapshot)!=b['snapshot_sha256']:return ['snapshot mismatch']
  report=json.loads((output/'.pack/evidence/pdf-validation.json').read_text())
  if report.get('logical_count')!=10:return ['Korean PDF count mismatch']
  for mode,suffix in [('problems','-문제.pdf'),('answers','-답안.pdf')]:
   if report['pdfs'][mode]['sha256']!=sha(output/(STEM+suffix)):return ['Korean PDF changed']
  return []
 except (ValueError,OSError,KeyError,TypeError) as e:return ['Korean PDF binding: '+str(e)]
