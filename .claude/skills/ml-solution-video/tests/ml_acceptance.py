"""Local scratch acceptance: synthetic PCM is never a live audio approval."""
from pathlib import Path
import argparse,shutil,json,base64
from types import SimpleNamespace
from fixtures import S,make_audio
from ml_authored import author_run
import video
from solution_video.util import read,write,file_hash,digest
from solution_video.sources import discover
from solution_video.bundle_timeline import build_bundle_timeline
from solution_video.annotations import load_teaching
from solution_video.review_adapter import default_config
from solution_video.writing import load_writing
from solution_video.subtitles import write_srt

def fake_voice(run):
 m=read(run/'source/manifest.json');l=read(run/'layers/layers.json');cfg=default_config();writing=load_writing(run,cfg);plan=load_teaching(run,m,l);dummy=[]
 for seg in m['segments']:
  a=make_audio(seg['id'],72000,run/'dummy');a['path']='dummy/'+a['path'];a['chunks']=[dict(id='c1',start_sample=0,end_sample=72000)];dummy.append(a)
 t=build_bundle_timeline(m,l,dummy,cfg,writing,plan);lengths={}
 for s in t['segments']:
  frames=[sp['end_frame'] for sp in t.get('writing_spans',[]) if sp['step_id']==s.get('step_id') and s['kind']=='write'];n=max(72000,(max(frames)-s['start_sample']//800)*800) if frames else 72000;lengths[s['text']]=max(n,lengths.get(s['text'],0))
 def transport(payload):
  text=payload['contents'][0]['parts'][0]['text'];raw=b'\x00\x10'*lengths[text]
  return dict(candidates=[dict(finishReason='STOP',content=dict(parts=[dict(inlineData=dict(mimeType='audio/L16;rate=24000',data=base64.b64encode(raw).decode()))]))],usageMetadata=dict(promptTokenCount=0,candidatesTokenCount=0))
 return transport

def run_acceptance(repo,dest,hyperframes_entry,*,env_file=None,live=False):
 repo=Path(repo).resolve();dest=Path(dest).resolve()
 if dest==repo or dest.is_relative_to(repo/'복습노트'):raise ValueError('acceptance requires a separate scratch destination')
 inputs=discover(repo,'1007',['P2','P3','P8']);source_hashes={path:file_hash(path) for b in inputs for path in b['source_files'].values()};folder=dest/'복습노트/1007';folder.parent.mkdir(parents=True,exist_ok=True)
 if not folder.exists():shutil.copytree(repo/'복습노트/1007',folder)
 batch=video.prepare_batch(dest,'1007',['P2','P3','P8']);rows=[];errors=[]
 for item in read(batch/'batch.json')['items']:
  run=batch/item['run'];row=dict(problem_id=item['id'],run=str(run),checks={});rows.append(row)
  try:
   author_run(run)
   args=SimpleNamespace(config=None,env_file=env_file,approve_review=False,writing_config=None,runtime=S/'assets/runtime/vendor/gsap.min.js',hyperframes_entry=hyperframes_entry)
   for action in ('extract','check','tts','assemble','render','captions'):
    result=video.run_stage(action,run,args,None if live else fake_voice(run) if action=='tts' else None);row['checks'][action]=result['status'];print(item['id'],action,result['status'],flush=True)
    if result['status']!='passed':raise ValueError(result.get('reason',str(result)))
   report=video.verify_run(run,Path(hyperframes_entry));row.update(technical_complete=report.get('technical_complete',False),complete=report['complete'],live_audio=report['live_audio'],checks=report['checks'],final=str(run/'renders/final.mp4'),final_sha256=file_hash(run/'renders/final.mp4'))
  except Exception as ex:errors.append(dict(problem_id=item['id'],reason=str(ex)[:900]));row['technical_complete']=False
 unchanged=all(file_hash(path)==sha for path,sha in source_hashes.items());result=dict(technical_complete=unchanged and not errors and all(r.get('technical_complete') for r in rows),complete=False,live_audio='unverified',paid_requests=0 if not live else None,source_hashes=source_hashes,source_preserved=unchanged,checks=rows,errors=errors,evidence=[str(batch)],production_publish_blocked=True,synthetic_pcm=not live)
 write(batch/'acceptance.json',result);write(dest/'acceptance.json',result);return result

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',required=True,type=Path);p.add_argument('--dest',required=True,type=Path);p.add_argument('--hyperframes-entry',required=True,type=Path);p.add_argument('--live',action='store_true');p.add_argument('--env-file',type=Path);a=p.parse_args();r=run_acceptance(a.repo,a.dest,a.hyperframes_entry,env_file=a.env_file,live=a.live);print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['technical_complete'] else 1
if __name__=='__main__':raise SystemExit(main())
