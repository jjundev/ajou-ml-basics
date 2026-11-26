"""Bind unchanged Korean PDFs to their exact historical input and Korean fields."""
from pathlib import Path
from dataclasses import asdict
import json,hashlib
from exam_adapter import read_cards,sha,resolve

def korean_resource_hashes(source,config):
 from exam_adapter import markup_resources
 cards=read_cards(source,config.profile).cards
 markup=[part for c in cards for part in [c.statement_html,c.hint_html,*c.steps,c.answer_html]]
 return markup_resources(markup,config.output,config.repo)

def korean_content_digest(source:Path,config):
 cards=[]
 for c in read_cards(source,config.profile).cards:
  record=asdict(c);record.pop('original_html');cards.append(record)
 return hashlib.sha256(json.dumps(cards,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def binding_record(output,config):
 output=Path(output);e=output/'.pack/evidence';source=resolve(config.repo,output/(config.stem+'.html'));snapshot=resolve(config.repo,e/'korean-pdf-source'/source.name)
 old=json.loads((e/'pdf-validation.json').read_text(encoding='utf-8'))
 if 'korean_resources' in old and old['korean_resources']!=korean_resource_hashes(source,config):raise ValueError('Korean PDF image resource changed')
 if sha(snapshot)!=old['source_sha256']:raise ValueError('historical PDF source mismatch')
 digest=korean_content_digest(source,config)
 if digest!=korean_content_digest(snapshot,config):raise ValueError('Korean content changed')
 return {'schema_version':1,'snapshot_path':snapshot.relative_to(output).as_posix(),'snapshot_sha256':sha(snapshot),'pdf_report_sha256':sha(e/'pdf-validation.json'),'current_source_sha256':sha(source),'korean_content_digest':digest,'pdfs':{config.stem+suffix:sha(output/(config.stem+suffix)) for suffix in ['-문제.pdf','-답안.pdf']}}

def check_pdf_binding(output:Path,repo:Path,config):
 try:
  output=Path(output);b=json.loads((output/'.pack/evidence/korean-pdf-binding.json').read_text(encoding='utf-8'))
  if b!=binding_record(output,config):return ['stale Korean PDF binding']
  snapshot=resolve(repo,output/b['snapshot_path'])
  if sha(snapshot)!=b['snapshot_sha256']:return ['snapshot mismatch']
  report=json.loads((output/'.pack/evidence/pdf-validation.json').read_text(encoding='utf-8'))
  if report.get('logical_count')!=10:return ['Korean PDF count mismatch']
  for mode,suffix in [('problems','-문제.pdf'),('answers','-답안.pdf')]:
   if report['pdfs'][mode]['sha256']!=sha(output/(config.stem+suffix)):return ['Korean PDF changed']
  return []
 except (ValueError,OSError,KeyError,TypeError) as e:return ['Korean PDF binding: '+str(e)]
