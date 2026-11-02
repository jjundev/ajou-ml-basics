"""Frozen ML multi-page render parity; no TTS or publication path."""
from pathlib import Path
import argparse,json,shutil,subprocess,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from solution_video.util import read,write,file_hash
from solution_video.media import render_master
from solution_video.render_options import default_render_options

def inventory(root):
 return {p.relative_to(root).as_posix():file_hash(p) for p in root.rglob('*') if p.is_file()}
def checked(args):
 subprocess.run(list(map(str,args)),check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def measure(master,run,dest,workers,pcm):
 frames=dest/f'{workers}.framemd5';aac=dest/f'{workers}.aac'
 checked(['ffmpeg','-y','-v','error','-i',master,'-map','0:v:0','-f','framemd5',frames]);checked(['ffmpeg','-y','-v','error','-i',master,'-map','0:a:0','-c:a','copy',aac])
 decoded=[l for l in frames.read_text().splitlines() if l and not l.startswith('#')]
 return dict(workers=workers,frames=len(decoded),frame_hash=file_hash(frames),pcm_hash=file_hash(pcm),aac_hash=file_hash(aac),master_hash=file_hash(master))
def compare_outputs(rows,frames,source_unchanged):
 result=dict(frames_equal=rows[0]['frame_hash']==rows[1]['frame_hash'] and all(r['frames']==frames for r in rows),pcm_equal=rows[0]['pcm_hash']==rows[1]['pcm_hash'],aac_equal=rows[0]['aac_hash']==rows[1]['aac_hash'],source_unchanged=source_unchanged)
 result['technical_complete']=all(result.values());return result

def run_acceptance(fixture:Path,destination:Path,hyperframes_entry:Path)->dict:
 fixture,dest,entry=map(lambda p:Path(p).resolve(),(fixture,destination,hyperframes_entry))
 if dest==fixture or dest.is_relative_to(fixture) or fixture.is_relative_to(dest):raise ValueError('destination overlaps fixture')
 if dest.exists() and any(dest.iterdir()):raise ValueError('destination nonempty')
 if not entry.is_file():raise ValueError('HyperFrames entry missing')
 for n in ('source/parts.json','source/timeline.json','source/audio.json','source/pair.json'):
  if not (fixture/n).is_file():raise ValueError('missing input: '+n)
 pair=read(fixture/'source/pair.json');pages=pair.get('problem_pages',[])+pair.get('answer_pages',[])
 if len({p['id'] for p in pages})<2:raise ValueError('multiple problem/answer pages required')
 parts=read(fixture/'source/parts.json');timeline=read(fixture/'source/timeline.json');audio=read(fixture/'source/audio.json')['voices']
 for p in [*(fixture/p['entry'] for p in parts),*(fixture/a['path'] for a in audio)]:
  if not p.is_file():raise ValueError('missing input: '+str(p))
 before=inventory(fixture);dest.mkdir(parents=True,exist_ok=True);rows=[]
 for workers in (2,6):
  run=dest/f'workers-{workers}';shutil.copytree(fixture,run,ignore=shutil.ignore_patterns('renders','verification','work','state.json'))
  options=dict(default_render_options({}),workers=workers);write(run/'source/render-options.json',options)
  start=time.monotonic();master=render_master(parts,timeline,audio,run,entry,render_options=options)
  row=measure(master,run,dest,workers,run/'renders/narration.wav');row['seconds']=time.monotonic()-start;rows.append(row);print(json.dumps(row),flush=True)
  write(dest/'progress.json',rows)
 result=dict(technical_complete=False,metrics=rows,frames_equal=rows[0]['frame_hash']==rows[1]['frame_hash'] and all(r['frames']==timeline['total_frames'] for r in rows),pcm_equal=rows[0]['pcm_hash']==rows[1]['pcm_hash'],aac_equal=rows[0]['aac_hash']==rows[1]['aac_hash'],source_unchanged=inventory(fixture)==before,paid_requests=0,published=False,live_audio='unverified')
 result.update(compare_outputs(rows,timeline['total_frames'],result['source_unchanged']));write(dest/'result.json',result)
 for at in (0,timeline['total_frames']/60,max(0,timeline['total_frames']/30-1)):
  checked(['ffmpeg','-y','-v','error','-ss',at,'-i',master,'-frames:v','1',dest/f'frame-{at:.2f}.png'])
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fixture',required=True,type=Path);p.add_argument('--destination',required=True,type=Path);p.add_argument('--hyperframes-entry',required=True,type=Path);a=p.parse_args();r=run_acceptance(a.fixture,a.destination,a.hyperframes_entry);print(json.dumps(r,indent=2));sys.exit(0 if r['technical_complete'] else 1)
