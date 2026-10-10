from pathlib import Path
import json,os
from .cache import digest,file_hash,cache_valid,atomic_json
from .render import command,frames_ok,stable_backend
from .timing import frame_at

def picture_fingerprint(run,sid):
    run=Path(run); files={}
    paths=list((run/'assets').rglob('*'))
    paths += list((run/'source').glob('*.css'))
    paths += [run/'source/theme.json']
    paths += [run/'source/scene-fragments'/(sid+ext) for ext in ('.html','.motion.json')]
    for p in paths:
        if p.is_file() and 'voice' not in p.relative_to(run).parts:
            files[p.relative_to(run).as_posix()]=file_hash(p)
    return digest(files)

def retime_input(timeline):
    windows=[]
    for scene in timeline['scenes']:
        segs=[s for s in timeline['segments'] if s['scene_id']==scene['id']]
        boundaries=[scene['first_frame']]+[frame_at(s['start_sample']) for s in segs]+[frame_at(scene['end_sample']-18000),scene['last_frame']]
        names=['intro']+[s['id'] for s in segs]+['tail']
        for i,name in enumerate(names):
            windows.append({'id':scene['id']+'-'+name,'scene_id':scene['id'],'first_frame':boundaries[i],'last_frame':boundaries[i+1]})
    return {'fps':timeline['fps'],'windows':windows}

def plan_revoice(old,new,source_hash,unchanged_scenes):
    if old['fps']!=30 or new['fps']!=30: raise ValueError('revoice requires 30fps')
    if [w['id'] for w in old['windows']] != [w['id'] for w in new['windows']] or not old['windows']:
        raise ValueError('window IDs do not match; rebuild changed scenes')
    out=[]; previous_old=previous_new=0
    for a,b in zip(old['windows'],new['windows']):
        if a['first_frame']!=previous_old or b['first_frame']!=previous_new or a['last_frame']<a['first_frame'] or b['last_frame']<b['first_frame']:
            raise ValueError('overlap/gap/reversed window')
        oldlen=a['last_frame']-a['first_frame']; newlen=b['last_frame']-b['first_frame']
        speed=oldlen/max(newlen,1)
        mode='retime' if a['scene_id'] in unchanged_scenes and oldlen>0 and newlen>0 and .8<=speed<=1.25 else 'rerender'
        w=dict(b,source_first_frame=a['first_frame'],source_last_frame=a['last_frame'],mode=mode)
        w['key']=digest({'source_sha256':source_hash,'window':w})
        out.append(w); previous_old=a['last_frame']; previous_new=b['last_frame']
    bad={w['scene_id'] for w in out if w['mode']=='rerender'}
    for w in out:
        if w['scene_id'] in bad: w['mode']='rerender'
    return out

def render_revoice(source,windows,run,backend,replacements):
    source=Path(source); run=Path(run); before=file_hash(source)
    dest=run/'renders/retimed'; dest.mkdir(parents=True,exist_ok=True)
    out=[]; used=set()
    for i,w in enumerate(windows):
        if w['mode']=='rerender':
            if w['scene_id'] not in replacements: raise ValueError('scene must be rerendered: '+w['scene_id'])
            if w['scene_id'] not in used: out.append(Path(replacements[w['scene_id']])); used.add(w['scene_id'])
            continue
        path=dest/f'window-{i:04d}.mp4'; receipt=path.with_suffix('.json')
        key=digest({'window':w,'source':before,'backend':stable_backend(backend)})
        frames=w['last_frame']-w['first_frame']
        if receipt.exists() and cache_valid(path,json.loads(receipt.read_text()),key) and frames_ok(path,frames):
            out.append(path); continue
        ratio=frames/(w['source_last_frame']-w['source_first_frame'])
        args=['ffmpeg','-y','-v','error']
        if backend.get('decode_gpu'): args+=['-hwaccel','cuda']
        args+=['-ss',str(w['source_first_frame']/30),'-t',str((w['source_last_frame']-w['source_first_frame'])/30),
          '-i',str(source),'-an','-vf',f'setpts={ratio:.12f}*(PTS-STARTPTS),fps=30,tpad=stop_mode=clone:stop_duration=1,format=yuv420p',
          '-frames:v',str(frames),'-c:v',backend['encoder']]
        args+=['-preset','p5'] if backend['encoder']=='h264_nvenc' else ['-preset','veryfast']
        pending=path.with_suffix('.pending.mp4')
        r=command(args+[str(pending)])
        if r.returncode or not frames_ok(pending,frames): raise RuntimeError('revoice window render failed')
        os.replace(pending,path); atomic_json(receipt,{'key':key,'output_sha256':file_hash(path)})
        out.append(path)
    if before!=file_hash(source): raise RuntimeError('source changed during revoice')
    atomic_json(run/'source/retime-manifest.json',{'source_sha256':before,'windows':windows})
    return out
