"""Validate authored mathematical evidence; this does not prove its truth."""
from .contracts import ReviewError
FIELDS=('variables','dimensions','assumptions','derivation','numeric_checks','visual_checks')
def validate_math_review(review,step_order,input_hash):
 if review.get('status')!='passed' or review.get('input_hash')!=input_hash:raise ReviewError('current authored math review required')
 rows=review.get('steps',[])
 if [r.get('step_id') for r in rows]!=step_order:raise ReviewError('math review must cover every ordered step')
 for row in rows:
  if not row.get('source_refs') or not str(row.get('meaning_review','')).strip():raise ReviewError('math source_refs/meaning_review required')
  for field in FIELDS:
   item=row.get(field)
   if not isinstance(item,dict) or type(item.get('applicable')) is not bool or not isinstance(item.get('evidence'),str) or not item['evidence'].strip():raise ReviewError('math '+field+' requires applicability and evidence, including NA reason')

def validate_source_refs(refs,run):
 from pathlib import Path
 import re,fitz
 from .util import read,local,file_hash
 allowed=read(Path(run)/'source/inputs.json')['files']
 for ref in refs:
  m=re.fullmatch(r'(html|cards|md|pdf|figure):([^#]+)(?:#(p\d+|page=\d+))?',ref)
  if not m:raise ReviewError('invalid source_ref '+str(ref))
  kind,path,anchor=m.groups()
  if path not in allowed or not local(run,path).is_file() or file_hash(local(run,path))!=allowed[path]['sha256']:raise ReviewError('unfrozen/changed source_ref')
  if kind in ('html','cards','md') and not anchor:raise ReviewError('card anchor required')
  if kind in ('html','cards'):
   from .ml_cards import read_cards
   if anchor.upper() not in {c['id'] for c in read_cards(local(run,path),[anchor.upper()])}:raise ReviewError('unknown source card anchor')
  if kind=='md':
   text=local(run,path).read_text();pid=anchor[1:]
   if not re.search(r'(?:P'+pid+r'\b|id=["\']'+anchor+r'["\']|\{#'+anchor+r'\})',text,re.I):raise ReviewError('unknown MD card anchor')
  if kind=='pdf':
   if not anchor or not anchor.startswith('page='):raise ReviewError('PDF page required')
   with fitz.open(local(run,path)) as d:
    if not 1<=int(anchor[5:])<=len(d):raise ReviewError('source PDF page outside range')
