"""ML SSE graph and KaTeX parity with synthetic PCM, no paid voice or publishing."""
from pathlib import Path
import argparse,copy,json,shutil,subprocess,sys,time
from _util import SKILL,ROOT,pcm
from integration_smoke import author,fixture_reload
from test_selection import fixture
from lib.cache import atomic_json,file_hash
from lib.composition import assemble,stage_assets
from lib.theme import snapshot_theme
from lib.timing import build_timeline,write_subtitles
from lib.render import cpu_backend,render_parts,mux_with_receipt
from lib.render_options import default_render_options
from lib.subtitles import burn_subtitles
from lib.verify import verify_media,check_sources
from lib.math_evidence import validate_math_evidence

def inventory(root):return {p.relative_to(root).as_posix():file_hash(p) for p in root.rglob('*') if p.is_file()}
def checked(args):subprocess.run(list(map(str,args)),check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def compare_outputs(rows,frames,source_unchanged):
 result=dict(frames_equal=rows[0]['frame_hash']==rows[1]['frame_hash'] and all(r['frames']==frames for r in rows),pcm_equal=rows[0]['pcm_hash']==rows[1]['pcm_hash'],aac_equal=rows[0]['aac_hash']==rows[1]['aac_hash'],source_unchanged=source_unchanged)
 result['technical_complete']=all(result.values());return result

def run_acceptance(destination:Path,hyperframes_entry:Path,*,motion_duration:float=.6)->dict:
 dest,entry=map(lambda p:Path(p).resolve(),(destination,hyperframes_entry))
 if motion_duration not in (.6,24):raise ValueError('motion duration must be 0.6 or 24')
 if not entry.is_file():raise ValueError('HyperFrames entry missing')
 if dest.exists() and any(dest.iterdir()):raise ValueError('destination nonempty')
 dest.mkdir(parents=True,exist_ok=True);repo=dest/'author-repo';inputs,plan=fixture(repo,1);inputs,plan=fixture_reload(repo,plan)
 run=dest/'fixture';run.mkdir();m=author(run,plan,plan['clips'][0]);sid=m['scenes'][0]['id']
 # Two 30s scenes; first 24.4s slot supports the 24s continuous capture case.
 frag=run/'source/scene-fragments';motions=json.loads((frag/(sid+'.motion.json')).read_text())
 for row in motions:
  row['duration_s']=motion_duration if row['segment_id']=='seg-start' else .6
 atomic_json(frag/(sid+'.motion.json'),motions)
 second=copy.deepcopy(m['scenes'][0]);second['id']=sid+'-b';m['scenes'].append(second)
 for suffix in ('.html','.motion.json'):(frag/(second['id']+suffix)).write_text((frag/(sid+suffix)).read_text().replace(sid,second['id']).replace('seg-start','seg-start-b').replace('seg-middle','seg-middle-b').replace('seg-end','seg-end-b'))
 segments=copy.deepcopy(m['segments'])
 for seg in segments:seg['id']+='-b';seg['scene_id']=second['id']
 m['segments'].extend(segments);m['coverage_reviews'][0]['segment_ids'].extend(s['id'] for s in segments)
 ev=json.loads((run/'source/math-evidence.json').read_text());other=copy.deepcopy(ev['scenes'][0]);other['scene_id']=second['id'];ev['scenes'].append(other);atomic_json(run/'source/math-evidence.json',ev)
 assert not validate_math_evidence(run,m)
 audio=[]
 for index,seg in enumerate(m['segments']):
  samples=(585600,40800,40800)[index%3];p=run/'assets/voice'/(seg['id']+'.wav');pcm(p,samples);audio.append(dict(id=seg['id'],path=p.relative_to(run).as_posix(),samples=samples,rate=24000,sha256=file_hash(p)))
 atomic_json(run/'manifest.json',m);atomic_json(run/'source/audio.json',dict(voices=audio));stage_assets(SKILL/'assets/runtime',run);theme=snapshot_theme(ROOT/'.agents/skills/ml-review-pack',run)
 timeline=build_timeline(m,audio);assert timeline['total_frames']==1800;atomic_json(run/'source/timeline.json',timeline);write_subtitles(timeline,run);parts=assemble(m,timeline,theme,run);before=inventory(run);rows=[]
 for workers in (2,6):
  output=dest/f'workers-{workers}';shutil.copytree(run,output);options=dict(default_render_options({}),workers=workers);atomic_json(output/'source/render-options.json',options);backend=cpu_backend(entry,options)
  start=time.monotonic();rendered=render_parts(parts,output,backend);receipt=mux_with_receipt(rendered,audio,timeline,output/'review.mp4',backend);seconds=time.monotonic()-start
  frames=dest/f'{workers}.framemd5';aac=dest/f'{workers}.aac';checked(['ffmpeg','-y','-v','error','-i',output/'review.mp4','-map','0:v:0','-f','framemd5',frames]);checked(['ffmpeg','-y','-v','error','-i',output/'review.mp4','-map','0:a:0','-c:a','copy',aac])
  row=dict(workers=workers,seconds=seconds,frames=len([l for l in frames.read_text().splitlines() if l and not l.startswith('#')]),frame_hash=file_hash(frames),pcm_hash=file_hash(output/'work/mux/narration.wav'),aac_hash=file_hash(aac),master_hash=file_hash(output/'review.mp4'));rows.append(row);atomic_json(dest/'progress.json',rows);print(json.dumps(row),flush=True)
 result=dict(technical_complete=False,motion_duration=motion_duration,metrics=rows,frames_equal=rows[0]['frame_hash']==rows[1]['frame_hash'] and all(r['frames']==1800 for r in rows),pcm_equal=rows[0]['pcm_hash']==rows[1]['pcm_hash'],aac_equal=rows[0]['aac_hash']==rows[1]['aac_hash'],source_unchanged=inventory(run)==before,paid_requests=0,published=False,live_audio='unverified')
 atomic_json(dest/'result.json',result)
 source=check_sources(output,entry);result['source_check']=source;captioned=dest/'captioned.mp4';burn_subtitles(output/'review.mp4',output/'narration.srt',captioned);result['captioned_media']=verify_media(captioned,timeline)
 for at in (0,1,15,26,30,31,45,59):checked(['ffmpeg','-y','-v','error','-ss',at,'-i',captioned,'-frames:v','1',dest/f'frame-{at}.png'])
 result.update(compare_outputs(rows,1800,result['source_unchanged']));result['technical_complete']=result['technical_complete'] and source['status']=='passed' and result['captioned_media']['status']=='passed';atomic_json(dest/'result.json',result);return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--destination',required=True,type=Path);p.add_argument('--hyperframes-entry',required=True,type=Path);p.add_argument('--motion-duration',type=float,default=.6);a=p.parse_args();r=run_acceptance(a.destination,a.hyperframes_entry,motion_duration=a.motion_duration);print(json.dumps(r,indent=2));sys.exit(0 if r['technical_complete'] else 1)
