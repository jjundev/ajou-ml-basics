from pathlib import Path
import shutil

def make_ml_repo(dest:Path,*,dates=('1007',),continuations=False,a4=False,ambiguous=False)->Path:
 import fitz
 dest=Path(dest)
 for date in dates:
  folder=dest/'복습노트'/date;folder.mkdir(parents=True,exist_ok=True)
  for slug in ('Basics','Other') if ambiguous else ('Basics',):
   stem='복습문제_'+date+'_'+slug
   cards=[]
   for n in (1,2):
    cards.append(f'<article class="card" id="p{n}" data-source="MML Example 9.{n}"><h3>Problem {n}</h3><div class="problem"><div class="conditions">x = {n}</div><div class="ask">Compute y.</div></div><div class="solution"><ol class="steps"><li>y = x + 1</li></ol><div class="answer">y = {n+1}</div></div></article>')
   (folder/(stem+'.html')).write_text(''.join(cards));(folder/(stem+'.md')).write_text('# Problems\n'+ '\n'.join(f'## P{n}\ny = x + 1\ny = {n+1}' for n in (1,2)))
   for role in ('문제','답안'):
    doc=fitz.open()
    for n in (1,2):
     for c in range(2 if continuations and role=='답안' and n==1 else 1):
      p=doc.new_page(width=842 if a4 else 1440,height=595 if a4 else 810)
      p.insert_text((25,32),f'P{n}'+(' (continued)' if c else ''),fontsize=16);p.insert_text((150,32),f'Problem {n}');p.insert_text((25,52),f'MML Example 9.{n}')
      p.insert_text((25,130),f'x = {n}',fontsize=14)
      if role=='답안':p.insert_text((320,170),f'y = x + 1 = {n+1}',fontsize=18)
    p=doc.new_page(width=1440,height=810);p.insert_text((25,32),'Hint');doc.save(folder/(stem+'-'+role+'.pdf'))
 return dest

def make_bundle_run(dest:Path,*,answer_pages:int=1)->Path:
 from solution_video.util import read,write
 from solution_video.pdf_pages import inside
 from solution_video.bundle_layers import extract_bundle,flatten_layers
 from solution_video.manifest import content_fingerprint
 from solution_video.state import finish_stage
 import video
 repo=make_ml_repo(Path(dest)/'repo',continuations=answer_pages==2);batch=video.prepare_batch(repo,'1007',['P1']);run=batch/read(batch/'batch.json')['items'][0]['run'];bundle=read(run/'source/pair.json');candidates=read(run/'layers/candidates.json');maps={}
 for pid,page in candidates['pages'].items():
  if not pid.startswith('answer'):continue
  work=[300,150,800,230];gs=[g['id'] for g in page['glyphs'] if inside(g['bbox'],work)];ss=[s['id'] for s in page['shapes'] if inside(s['bbox'],work)]
  maps[pid]=dict(work_bbox=work,steps=[dict(id='s',glyph_ids=gs,shape_ids=ss,writing_units=[dict(id='u',line_id='l',chunk_id='c',column_id='col',band=[300,800],glyph_ids=gs,shape_ids=ss,camera_break_before=False)])],terminal_step_id='s')
 order=[pid+'::s' for pid in maps];mp=dict(schema_version=2,pages=maps,step_order=order,answer_step_id=order[-1]);write(run/'source/map.json',mp);layers=extract_bundle(candidates,mp);flat=flatten_layers(layers)
 refs=['html:'+bundle['source_files']['html']+'#p1','md:'+bundle['source_files']['md']+'#p1','pdf:'+bundle['source_files']['answer_pdf']+'#page=1']
 def seg(sid,pid,step,kind,text,caption):return dict(id=sid,page_id=pid,step_id=step,kind=kind,text=text,caption_text=caption,source_refs=refs,chunks=[dict(id='c1',text=text,caption_text=caption)])
 segments=[seg('intro','problem-1','','problem','조건을 확인합니다.','조건을 확인합니다.')];lesson=[];rows=[];math=[]
 for n,sid in enumerate(order):
  pid=sid.split('::')[0];segments.extend([seg('reason'+str(n),pid,sid,'reason','엑스에 일을 더합니다.','x에 1을 더합니다.'),seg('write'+str(n),pid,sid,'write','결과는 이입니다.','y = 2입니다.')]);lesson.append(dict(step_id=sid,mode='reasoned',meaning_notes='x=1, y=x+1=2 follows the fixed card.',source_refs=refs,reason_segment_ids=['reason'+str(n)],check_segment_ids=[],region_ids=[],annotation_ids=[]));objects={g['id']:g for g in flat['glyphs']};step=flat['map']['steps'][n];rows.append(dict(step_id=sid,pdf_text=''.join(objects[g]['text'] for g in step['glyph_ids']),md_text='y = x + 1; y = 2',source_refs=refs,meaning_review='Compared card, MD and PDF: x=1, y=x+1=2.'));details=dict(variables='x,y are scalar',dimensions='scalar addition',assumptions='x=1',derivation='y=x+1',numeric_checks='1+1=2',visual_checks='Original equal and plus signs inspected');math.append(dict(step_id=sid,source_refs=refs,meaning_review='Fixed synthetic teaching fixture',**{k:dict(applicable=True,evidence=v) for k,v in details.items()}))
 m=dict(schema_version=2,key=bundle['key'],pack_id=bundle['pack_id'],problem_id='P1',title=bundle['title'],segments=segments,reveal_order=[g for s in flat['map']['steps'] for g in s['glyph_ids']],shape_anchors={sh:s['glyph_ids'][-1] for s in flat['map']['steps'] for sh in s['shape_ids']},cameras=[],caption_timing='pcm-chunks-v1');coverage=dict(status='passed',pdf_md_agree=True,rows=rows);h=content_fingerprint(m,layers,coverage);coverage['input_hash']=h
 for name,obj in [('manifest',m),('coverage',coverage),('math-review',dict(status='passed',input_hash=h,steps=math)),('lesson',dict(schema_version=1,steps=lesson))]:write(run/'source'/(name+'.json'),obj)
 return run
