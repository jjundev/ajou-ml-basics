"""Page-local extraction with globally unique source identities."""
from pathlib import Path
import copy
from .pdf_pages import export_page,extract_layers,compare_completed
from .contracts import ExtractionError
from .util import digest,file_hash,write,local

def export_bundle(bundle,run):
 run=Path(run);pages={}
 for ref in bundle['problem_pages']+bundle['answer_pages']:
  pid=ref['id']
  if pid in pages or '/' in pid or '..' in pid:raise ExtractionError('duplicate/unsafe page ID')
  path=Path(ref['snapshot']);path=path if path.is_absolute() else local(run,path)
  pages[pid]=export_page(path,ref['page_index'],run/'layers/pages'/pid)
  pages[pid]['role']=ref.get('role','problem' if pid.startswith('problem') else 'answer')
 write(run/'layers/candidates.json',dict(schema_version=2,pages=pages));return pages

def extract_bundle(candidates,mapping):
 if mapping.get('schema_version')!=2:raise ExtractionError('BundleMap schema must be 2')
 pages=candidates.get('pages',candidates);answer_ids=[p for p in pages if pages[p].get('role','answer')=='answer']
 if set(mapping.get('pages',{}))!=set(answer_ids):raise ExtractionError('map must cover every answer page')
 out={};order=[]
 for pid,page in pages.items():
  if pid not in answer_ids:
   import xml.etree.ElementTree as ET
   from .pdf_pages import _painted,image_proven_invisible
   out[pid]=copy.deepcopy(page);root=ET.parse(page['original_svg']).getroot();nodes={'sv-'+str(i):n for i,n in enumerate(_painted(root))}
   for image in out[pid].get('images',[]):image['proven_invisible']=image_proven_invisible(root,nodes[image['id']])
   continue
  m=copy.deepcopy(mapping['pages'][pid]);terminal=m.pop('terminal_step_id',None)
  if not terminal:raise ExtractionError('local terminal_step_id required')
  m['answer_step_id']=terminal;out[pid]=extract_layers(page,m)
  out[pid]['role']='answer';order.extend(pid+'::'+s['id'] for s in m['steps'])
 if mapping.get('step_order')!=order or len(set(order))!=len(order):raise ExtractionError('ordered global step coverage required')
 if not order or mapping.get('answer_step_id')!=order[-1]:raise ExtractionError('global answer must be final step')
 return dict(schema_version=2,page_order=list(pages),pages=out,step_order=order,answer_step_id=order[-1])

def verify_bundle_layers(layers,evidence):
 evidence=Path(evidence);results={};hashes={}
 for pid in layers['page_order']:
  page=layers['pages'][pid]
  if page.get('role')=='problem':continue
  results[pid]=compare_completed(page,evidence/pid)
  for p in results[pid]['evidence']:hashes[str(Path(p).resolve())]=file_hash(p)
 result=dict(passed=bool(results) and all(all(r[k]==0 for k in ('pixel_diff','non_target_diff','hidden_leaks')) for r in results.values()),pages=results,evidence_hashes=hashes,input_hash=digest(layers),source_hashes={pid:{k:file_hash(p[k]) for k in ('original_svg','animated_svg','reference_png')} for pid,p in layers['pages'].items()})
 write(evidence/'bundle-gate.json',result);return result

def flatten_layers(layers):
 """Private temporal view; coordinates still belong to page_id, never merged PDF."""
 if layers.get('schema_version')!=2:return layers
 pages=layers['pages'];answer=[pid for pid in layers['page_order'] if pages[pid].get('role')=='answer'];first=pages[answer[0]];out=copy.deepcopy(first);out.update(glyphs=[],shapes=[]);steps=[]
 for pid in answer:
  p=pages[pid]
  for kind in ('glyphs','shapes'):
   for item in p[kind]:
    row=copy.deepcopy(item);row.update(id=pid+'::'+item['id'],page_id=pid);out[kind].append(row)
  for step in p['map']['steps']:
   row=copy.deepcopy(step);row['id']=pid+'::'+step['id'];row['page_id']=pid
   for field in ('glyph_ids','shape_ids'):row[field]=[pid+'::'+i for i in step[field]]
   for u in row.get('writing_units',[]):
    for field in ('id','line_id','chunk_id'):
     if field in u:u[field]=pid+'::'+u[field]
    for field in ('glyph_ids','shape_ids'):
     if field in u:u[field]=[pid+'::'+i for i in u[field]]
    for piece in u.get('pieces',[]):piece['id']=pid+'::'+piece['id']
   steps.append(row)
 out['map']=dict(work_bbox=first['map']['work_bbox'],steps=steps,answer_step_id=layers['answer_step_id']);out['bundle']=layers
 return out
