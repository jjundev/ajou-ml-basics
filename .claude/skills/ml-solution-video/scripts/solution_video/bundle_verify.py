from pathlib import Path
import json,wave
from .util import read,write,digest,file_hash,local,S,browser,browser_config,checked,command
from .contracts import InputError
from .bundle_cli import check_content,gate_current
from .bundle_layers import flatten_layers
from .bundle_timeline import build_bundle_timeline
from .media import probe,ffmpeg,source_checks
from .subtitles import caption_srt_matches
from .speech_chunks import verify_chunk_sync,chunk_review_passed

def meaning_review_passed(run,kind,input_hash,manifest):
 try:
  r=read(Path(run)/'verification'/f'{kind}-review.json')
  if r.get('status')!='passed' or r.get('input_hash')!=input_hash or not str(r.get('notes','')).strip() or not r.get('evidence'):return False
  if kind=='audio' and (r.get('mode')!='live-listened' or not chunk_review_passed(r,manifest)):return False
  return all(local(run,p).is_file() and file_hash(local(run,p))==sha for p,sha in r['evidence'].items())
 except (OSError,KeyError,ValueError):return False

def verify_bundle_run(run,hyperframes_entry):
 from .verify import verification_fingerprint,teaching_browser
 run=Path(run).resolve();h=verification_fingerprint(run);checks={};evidence=[];final=run/'renders/final.mp4';m=read(run/'source/manifest.json');l=read(run/'layers/layers.json');t=read(run/'source/timeline.json')
 def check(name,fn):
  try:ok=fn();checks[name]=dict(status='passed' if ok else 'unverified')
  except Exception as ex:checks[name]=dict(status='unverified',reason=str(ex)[:500])
 check('content',lambda:bool(check_content(run)))
 check('original_svg',lambda:gate_current(run,l) is None)
 def timing():
  _,_,_,_,plan,writing=check_content(run)
  expected=build_bundle_timeline(m,l,read(run/'source/audio.json')['voices'],read(run/'source/config.json'),writing,plan)
  return t==expected
 check('measured_timeline',timing)
 def page_order():
  args=['node',S/'tests/bundle_check.mjs','--entry',run/'composition/index.html','--timeline',run/'source/timeline.json','--views',run/'composition/bundle-views.json',*browser_config()];rounds=[];start=0;total=None
  while total is None or start<total:
   r=json.loads(checked([*args,'--frame-start',str(start),'--frame-count','25',*(['--reference-only','true'] if start else [])],timeout=600 if t.get('teaching') else 120).stdout)
   if total is not None and r['oracle_total_probes']!=total:raise InputError('page oracle probe catalogue changed')
   total=r['oracle_total_probes'];rounds.append(r);write(run/'verification'/('page-order-round-'+str(start)+'.json'),r);start+=25
  result=dict(passed=bool(total) and rounds[0].get('forward_backward_checked') is True and sum(r['oracle_probes'] for r in rounds)==total and all(r['forward_backward_diff']==r['future_leaks']==r['parent_reference_diff']==0 and r['final_pencil']=='0' for r in rounds),total_probes=total,rounds=rounds)
  write(run/'verification/page-order.json',result);evidence.append('verification/page-order.json');return result['passed']
 check('page_order',page_order)
 def page_animations():
  results={};views=read(run/'composition/bundle-views.json')
  for pid,view in views.items():
   child=Path(view['run']);entry=run/'composition'/view['entry'];layers=Path(view['layers'])
   r=browser(['--mode','timeline','--entry',entry,'--layers',layers,'--dest',run/'verification/page-animation'/pid])
   passed=r['seek_equal'] and r['final_cursor']=='0'
   w=r.get('writing')
   if t.get('writing',{}).get('mode')=='pencil':
    passed=passed and bool(w) and all(w.get(k) for k in ('order_ok','seek_equal','gsap_seek_equal','bounds_ok','inactive_hidden')) and not w.get('final_visible') and w.get('tip_error_px',99)<=1 and all(w.get(k,-1)==0 for k in ('precomplete_diff','complete_diff','hidden_leaks'))
    flow=browser(['--mode','writing-flow','--entry',entry,'--layers',layers,'--dest',run/'verification/page-flow'/pid]);passed=passed and all(flow[k] for k in ('order_ok','fit_ok','transitions_ok','stable_camera','seek_equal'));r['flow']=flow
   if (child/'source/focus.json').is_file():
    from .annotations import load_teaching,compile_annotations
    from .lesson import lesson_expectations
    mm=read(child/'source/manifest.json');ll=read(layers);tt=read(child/'composition/timeline.json');plan=load_teaching(child,mm,ll);compiled=read(child/'composition/annotations/compiled.json') if plan and plan['items'] else None
    expected=run/'verification'/('teaching-'+pid+'.json');lesson=read(run/'source/lesson.json');lesson['steps']=[row for row in lesson['steps'] if row['step_id'].startswith(pid+'::')]
    write(expected,dict(timeline=tt,compiled=compiled,lesson=lesson_expectations(lesson,mm,tt,plan)))
    ink=teaching_browser(['--mode','teaching','--entry',entry,'--layers',layers,'--timeline',expected,'--dest',run/'verification/page-teaching'/pid]);passed=passed and all(ink[k] for k in ('timeline_equal','cameras_equal','geometry_equal','seek_equal','gsap_seek_equal','bounds_ok','inactive_hidden','lesson_flow')) and not ink['final_visible'] and ink['tip_error_px']<=1 and all(ink[k]==0 for k in ('original_pixel_diff','annotation_pixel_diff','future_leaks'));r['teaching']=ink
   results[pid]=dict(passed=passed,result=r)
  write(run/'verification/page-animation.json',results);evidence.append('verification/page-animation.json');return len(views)==len(read(run/'source/pair.json')['answer_pages']) and all(r['passed'] for r in results.values())
 check('writing_animation',page_animations);checks['writing_flow']=dict(checks['writing_animation']);checks['teaching_animation']=dict(checks['writing_animation']);checks['lesson_flow']=dict(checks['writing_animation'])
 def pacing():
  if t.get('writing',{}).get('mode')!='pencil':return True
  from .narration_pacing import analyze_narration_pacing
  r=analyze_narration_pacing(t,read(run/'source/audio.json')['voices'],run);write(run/'verification/narration-pacing.json',r);return r['status']=='passed'
 check('narration_pacing',pacing)
 check('hyperframes',lambda:bool(source_checks(read(run/'source/parts.json'),run,hyperframes_entry)))
 def media():
  streams=probe(final)['streams'];v=next(s for s in streams if s['codec_type']=='video');a=next(s for s in streams if s['codec_type']=='audio')
  if (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']),int(a['sample_rate']))!=(1920,1080,'30/1',t['total_frames'],24000):return False
  if abs(float(v['duration'])-float(a['duration']))>1/30 or command([ffmpeg(),'-v','error','-i',final,'-f','null','-'],timeout=1800).returncode:return False
  for rec in read(run/'source/audio.json')['voices']:
   p=local(run,rec['path'])
   if file_hash(p)!=rec['sha256']:return False
   with wave.open(str(p),'rb') as f:
    if (f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getnframes())!=(1,2,24000,rec['samples']):return False
  return True
 check('final_media',media)
 def captions():
  if not caption_srt_matches(t,run/'renders/captions.srt'):return False
  import subprocess,io
  from PIL import Image,ImageChops,ImageStat
  for cue in t['caption_cues']:
   at=(cue['start_sample']+cue['end_sample'])/48000;pics=[]
   for p in (run/'renders/master.mp4',final):
    r=subprocess.run([ffmpeg(),'-v','error','-ss',str(at),'-i',str(p),'-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True,timeout=60)
    if r.returncode:return False
    pics.append(Image.open(io.BytesIO(r.stdout)).convert('RGB'))
   diff=ImageChops.difference(*pics)
   if not diff.crop((0,900,1920,1080)).getbbox() or max(ImageStat.Stat(diff.crop((0,0,1920,900))).mean)>3:return False
  return bool(t['caption_cues'])
 check('captions',captions);check('chunk_sync',lambda:verify_chunk_sync(run)['status']=='passed')
 for kind in ('audio','visual'):check(kind+'_meaning',lambda k=kind:meaning_review_passed(run,k,h,m))
 technical=all(v['status']=='passed' for k,v in checks.items() if k not in ('audio_meaning','visual_meaning'));complete=all(v['status']=='passed' for v in checks.values())
 report=dict(schema_version=2,complete=complete,technical_complete=technical,input_hash=h,checks=checks,evidence=evidence,final_sha256=file_hash(final) if final.is_file() else None,review_hashes={p.relative_to(run).as_posix():file_hash(p) for p in (run/'verification').glob('*-review.json')},live_audio='verified' if checks['audio_meaning']['status']=='passed' else 'unverified')
 write(run/'verification/report.json',report);return report
