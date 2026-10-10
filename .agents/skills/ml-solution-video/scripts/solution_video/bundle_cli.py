from pathlib import Path
import copy,shutil,uuid,wave
from datetime import datetime
from .util import read,write,digest,file_hash,local,S
from .contracts import InputError,ReviewError
from .sources import discover,freeze_sources
from .bundle_layers import export_bundle,extract_bundle,verify_bundle_layers,flatten_layers
from .manifest import validate_manifest,content_fingerprint
from .math_review import validate_source_refs
from .review_adapter import default_config,validate_config,generate_voice
from .writing import default_writing,load_writing,validate_writing
from .annotations import load_teaching
from .lesson import load_lesson
from .bundle_timeline import build_bundle_timeline
from .state import STAGES,recover_run,finish_stage
from .render_options import default_render_options,load_render_options

def prepare_batch(repo,selector,problem_ids=None,review=False,writing_mode='pencil',*,pack=None,page_map=None):
 repo=Path(repo).resolve();failures=[];bundles=discover(repo,selector,problem_ids,failures,pack=pack,page_map=read(page_map) if isinstance(page_map,(Path,str)) else page_map)
 if len({b['key'] for b in bundles})!=len(bundles):raise InputError('duplicate bundle identity')
 batch=repo/'문제풀이영상'/selector/(selector+'_제작자료')/'실행'/(datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8]);batch.mkdir(parents=True)
 frozen=freeze_sources(bundles,batch);data=dict(schema_version=2,selector=selector,review=review,items=[]);write(batch/'batch.json',data)
 for b in frozen:
  key='problem-'+digest(b['key'])[:16];run=batch/'videos'/key;run.mkdir(parents=True)
  for relative in set(b['source_files'].values()):
   target=local(run,relative);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(local(batch,relative),target)
  write(run/'source/inputs.json',read(batch/'source/inputs.json'));write(run/'source/pair.json',b);write(run/'source/config.json',default_config());write(run/'source/writing.json',default_writing(writing_mode));write(run/'run.json',dict(batch=str(batch),review=review,problem_id=b['problem_id'],key=b['key']))
  write(run/'source/render-options.json',default_render_options())
  item=dict(id=b['problem_id'],key=b['key'],pack_id=b['pack_id'],range=b['range'],slug=b['slug'],run='videos/'+key,filename=b['problem_id']+' — 풀이.mp4',status='author-required',prefix=(b['range']+' — ' if '-' in selector else '')+(b['slug']+' — ' if len({x['slug'] for x in frozen})>1 else ''));data['items'].append(item);write(batch/'batch.json',data)
  try:
   export_bundle(b,run);finish_stage(run,'inputs',[run/'source/inputs.json',run/'source/pair.json'])
  except Exception as ex:item.update(status='failed',reason=str(ex)[:500]);write(run/'source/prepare-error.json',dict(reason=item['reason']))
  write(batch/'batch.json',data)
 for failure in failures:
  key='failed-'+digest(failure)[:16];run=batch/'videos'/key;write(run/'source/prepare-error.json',failure);data['items'].append(dict(id=failure['problem_id'] or failure['pack_id'],key=failure['key'],run='videos/'+key,filename=key+'.mp4',status='failed',reason=failure['reason']))
 write(batch/'batch.json',data);return batch

def load_content(run):return tuple(read(run/p) for p in ('source/manifest.json','layers/layers.json','source/coverage.json','source/math-review.json'))
def gate_current(run,layers):
 g=read(run/'verification/gate.json')
 if g.get('input_hash')!=digest(layers) or not g.get('passed') or not g.get('evidence_hashes'):raise ReviewError('bundle gate missing/stale/failed')
 for path,sha in g['evidence_hashes'].items():
  p=Path(path)
  if not p.is_relative_to(run) or file_hash(p)!=sha:raise ReviewError('gate evidence changed')
 for pid,p in layers['pages'].items():
  for field,sha in g['source_hashes'][pid].items():
   if file_hash(p[field])!=sha:raise ReviewError('page source changed')

def check_content(run):
 m,l,c,r=load_content(run);bundle=read(run/'source/pair.json')
 if any(m.get(k)!=bundle.get(k) for k in ('key','pack_id','problem_id','title')):raise ReviewError('manifest/source bundle identity mismatch')
 from .source_integrity import validate_bundle_sources
 validate_bundle_sources(bundle,l,run)
 validate_manifest(m,l,c,r);gate_current(run,l)
 refs=[ref for row in [*m['segments'],*c['rows'],*r['steps']] for ref in row.get('source_refs',[])];validate_source_refs(refs,run)
 teaching=load_teaching(run,m,l)
 if not (run/'source/lesson.json').is_file():raise ReviewError('ML lesson.json required')
 lesson=load_lesson(run,m,l,teaching);validate_source_refs([ref for row in lesson['steps'] for ref in row['source_refs']],run)
 writing=load_writing(run,read(run/'source/config.json'));validate_writing(writing)
 if writing['mode']=='pencil':
  from .writing_units import compile_writing_units
  compile_writing_units(flatten_layers(l))
 return m,l,c,r,teaching,writing

def run_bundle_stage(action,run,args,transport=None):
 run=Path(run).resolve();stage=dict(extract='layers',check='script',tts='voice',retime='timing',assemble='composition',render='render',captions='captions',verify='verify')[action]
 if action=='extract' and not (run/'layers/candidates.json').is_file():
  export_bundle(read(run/'source/pair.json'),run);finish_stage(run,'inputs',[run/'source/inputs.json',run/'source/pair.json']);(run/'source/prepare-error.json').unlink(missing_ok=True)
 needed=['source/map.json'] if action=='extract' else ['source/manifest.json','layers/layers.json','source/coverage.json','source/math-review.json','source/lesson.json']
 missing=[p for p in needed if not (run/p).is_file()]
 if missing:return dict(status='author-required',missing=missing,paid_requests=0)
 if action=='render':
  render_options=load_render_options(run,getattr(args,'render_workers',None));write(run/'source/render-options.json',render_options)
 if (run/'state.json').is_file():
  nxt=recover_run(run)
  if nxt and STAGES.index(nxt)<STAGES.index(stage):raise InputError('refresh prerequisite stage: '+nxt)
 if action=='extract':
  l=extract_bundle(read(run/'layers/candidates.json'),read(run/'source/map.json'));write(run/'layers/layers.json',l);g=verify_bundle_layers(l,run/'verification/gate-frames');write(run/'verification/gate.json',g)
  if not g['passed']:raise ReviewError('original SVG gate failed')
  finish_stage(run,'layers',[run/'layers/layers.json',run/'verification/gate.json',*[Path(p['animated_svg']) for p in l['pages'].values()]]);return dict(status='passed',paid_requests=0,gate=g)
 m,l,c,r,plan,writing=check_content(run)
 if action=='check':
  finish_stage(run,'script',[run/'source'/n for n in ('manifest.json','coverage.json','math-review.json','lesson.json')]);return dict(status='passed',paid_requests=0,input_hash=content_fingerprint(m,l,c))
 if action=='tts':
  cfg=read(args.config) if getattr(args,'config',None) else read(run/'source/config.json');validate_config(cfg);write(run/'source/config.json',cfg)
  meta=read(run/'run.json');batch=Path(meta['batch']);bd=read(batch/'batch.json')
  if meta['review']:
   scope=[i for i in bd['items'] if (local(batch,i['run'])/'source/pair.json').is_file() and not ((local(batch,i['run'])/'source/prepare-error.json').is_file() and not (local(batch,i['run'])/'layers/candidates.json').is_file())]
   hashes={}
   for i in scope:
    rr=local(batch,i['run'])
    try:mm,ll,cc,*_=check_content(rr)
    except (OSError,InputError):return dict(status='author-required',reason='finish all current batch scripts/reviews',paid_requests=0)
    hashes[i['key']]=content_fingerprint(mm,ll,cc)
   h=digest(hashes);approval=batch/'script-approval.json'
   if getattr(args,'approve_review',False):write(approval,dict(input_hash=h,approved=True))
   if not approval.is_file() or read(approval).get('input_hash')!=h:return dict(status='awaiting-review',input_hash=h,paid_requests=0)
  ledger=batch/'usage.json';count=lambda:len(read(ledger)['requests']) if ledger.is_file() else 0;before=count()
  try:audio=generate_voice(m['segments'],run,cfg,ledger,transport,env_file=getattr(args,'env_file',None))
  except Exception as ex:ex.paid_requests=0 if transport else count()-before;raise
  from .speech_chunks import validate_chunk_audio
  validate_chunk_audio(m['segments'],audio,run);finish_stage(run,'voice',[run/'source/audio.json',run/'source/chunk-audio.json'])
  t=build_bundle_timeline(m,l,audio,cfg,writing,plan);write(run/'source/timeline.json',t);finish_stage(run,'timing',[run/'source/timeline.json']);return dict(status='passed',segments=len(audio),paid_requests=0 if transport else count()-before)
 if action=='retime':
  cfg=read(run/'source/config.json');validate_config(cfg)
  proposed=read(args.writing_config) if getattr(args,'writing_config',None) else None
  if proposed:validate_writing(proposed);writing=proposed
  from .speech_chunks import join_segment_audio,validate_chunk_audio
  raw=read(run/'source/chunk-audio.json')['voices'];trims=read(run/'source/chunk-trims.json') if (run/'source/chunk-trims.json').is_file() else None;audio=join_segment_audio(m['segments'],raw,run,trims);validate_chunk_audio(m['segments'],audio,run)
  t=build_bundle_timeline(m,l,audio,cfg,writing,plan)
  if proposed:write(run/'source/writing.json',proposed)
  write(run/'source/audio.json',dict(voices=audio));finish_stage(run,'voice',[run/'source/audio.json',run/'source/chunk-audio.json']);write(run/'source/timeline.json',t);finish_stage(run,'timing',[run/'source/timeline.json']);return dict(status='passed',paid_requests=0,total_frames=t['total_frames'])
 if action=='assemble':
  from .composition import assemble
  parts=assemble(read(run/'source/pair.json'),l,m,read(run/'source/timeline.json'),run,Path(args.runtime));finish_stage(run,'composition',[run/'source/parts.json',*[p for p in (run/'composition').rglob('*') if p.is_file()]]);return dict(status='passed',parts=parts,paid_requests=0)
 if action=='render':
  from .media import render_master
  p=render_master(read(run/'source/parts.json'),read(run/'source/timeline.json'),read(run/'source/audio.json')['voices'],run,Path(args.hyperframes_entry),render_options=render_options);receipt=run/'verification/render-receipt.json';finish_stage(run,'render',[p,receipt]);return dict(status='passed',paid_requests=0,master=str(p),render_options=render_options,render_receipt=str(receipt))
 if action=='captions':
  from .subtitles import write_srt,burn_subtitles
  srt=write_srt(read(run/'source/timeline.json'),run/'renders/captions.srt');final=burn_subtitles(run/'renders/master.mp4',srt,run/'renders/final.mp4',S/'assets/fonts/Pretendard-Bold.ttf');finish_stage(run,'captions',[srt,final]);return dict(status='passed',final=str(final),paid_requests=0)
 from .verify import verify_run
 report=verify_run(run,Path(args.hyperframes_entry))
 if report['complete']:finish_stage(run,'verify',[run/'verification/report.json'])
 return dict(report,status='passed' if report['complete'] else 'failed',paid_requests=0)
