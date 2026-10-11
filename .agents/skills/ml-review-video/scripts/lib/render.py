from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,os,re,shutil,signal,subprocess,time,uuid,wave
from .cache import digest,file_hash,cache_valid,atomic_json
from .render_options import load_render_options,validate_render_options,resolve_scene_workers,detect_hardware

def _stop_process_tree(proc):
    if os.name=='nt':
        subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],capture_output=True,timeout=10)
    else:
        # Chrome may detach into its own session; collect owned descendants before killing Node.
        rows=subprocess.run(['ps','-axo','pid=,ppid='],capture_output=True,text=True,timeout=3,check=True).stdout.splitlines()
        parents={int(r.split()[0]):int(r.split()[1]) for r in rows if len(r.split())==2}
        depths={proc.pid:0}
        while True:
            new={pid:depths[parent]+1 for pid,parent in parents.items() if parent in depths and pid not in depths}
            if not new: break
            depths.update(new)
        for pid in sorted(depths,key=depths.get,reverse=True):
            try: os.kill(pid,signal.SIGKILL)
            except ProcessLookupError: pass
        try: os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError: pass
    proc.kill() if proc.poll() is None else None
    return proc.communicate()

def command(args,cwd=None,timeout=300):
    args=[str(a) for a in args]
    proc=subprocess.Popen(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                          encoding='utf-8',errors='replace',start_new_session=os.name!='nt',
                          creationflags=(subprocess.CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP) if os.name=='nt' else 0)
    try: stdout,stderr=proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as ex:
        stdout,stderr=_stop_process_tree(proc)
        raise subprocess.TimeoutExpired(args,timeout,output=stdout,stderr=stderr) from ex
    except BaseException:
        _stop_process_tree(proc); raise
    return subprocess.CompletedProcess(args,proc.returncode,stdout,stderr)


def commit_media_receipt(pending,data,media,receipt):
    pending,media,receipt=map(Path,(pending,media,receipt))
    receipt_pending=receipt.with_name(receipt.name+'.'+uuid.uuid4().hex+'.pending')
    targets=[media,receipt];backups={};replaced=[];cleanup=False
    try:
        retained=[t.with_name(t.name+'.rollback') for t in targets
                  if t.with_name(t.name+'.rollback').exists() or t.with_name(t.name+'.rollback').is_symlink()]
        if retained: raise RuntimeError('unresolved recovery copies; inspect before retry: '+', '.join(map(str,retained)))
        atomic_json(receipt_pending,data)
        for target in targets:
            if target.exists() or target.is_symlink():
                backup=target.with_name(target.name+'.rollback')
                shutil.copy2(target,backup,follow_symlinks=False);backups[target]=backup
        for source,target in [(pending,media),(receipt_pending,receipt)]:
            os.replace(source,target);replaced.append(target)
        cleanup=True
    except BaseException as original:
        failures=[]
        for target in reversed(replaced):
            try:
                if target in backups:os.replace(backups[target],target)
                else:target.unlink(missing_ok=True)
            except BaseException as ex:failures.append(ex)
        if failures:
            retained=[str(p) for p in backups.values() if p.exists() or p.is_symlink()]
            raise RuntimeError('rollback failed; recovery copies retained: '+', '.join(retained)) from original
        cleanup=True;raise
    finally:
        pending.unlink(missing_ok=True);receipt_pending.unlink(missing_ok=True)
        if cleanup:
            for backup in backups.values():backup.unlink(missing_ok=True)

def probe_media(path):
    r=command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path])
    if r.returncode: raise ValueError('ffprobe failed: '+str(path))
    return json.loads(r.stdout)

def frames_ok(path,frames):
    try:
        s=next(s for s in probe_media(path)['streams'] if s['codec_type']=='video')
        return int(s['nb_frames'])==frames and int(s['width'])==1920 and int(s['height'])==1080 and s['r_frame_rate'] in ('30/1','60/2')
    except (ValueError,KeyError,StopIteration,OSError,TypeError): return False

DARK_MAX=80  # 다크 배경은 약 22/255. 라이트 배경은 200 이상이다.

def dark_failures(path,points=(0.1,0.35,0.6,0.85)):
    """영상 좌상단 8x8 배경 밝기를 여러 시점에서 재서 다크가 아닌 시각 목록을 돌려준다."""
    duration=float(probe_media(path)['format']['duration']); bad=[]
    for fraction in points:
        at=max(0,duration*fraction-0.05)
        r=subprocess.run(['ffmpeg','-v','error','-ss',str(at),'-i',str(path),'-frames:v','1','-vf','crop=8:8:0:0,scale=1:1,format=gray',
            '-f','rawvideo','-'],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        if r.returncode or len(r.stdout)<1 or r.stdout[0]>DARK_MAX: bad.append(round(at,2))
    return bad

def require_dark_entries(parts,run):
    """장면 진입점이 data-theme="dark"여야 한다. 통합 index.html 렌더(라이트로 나올 수 있음)는 거부한다."""
    for part in parts:
        entry=part['entry']
        if Path(entry).name=='index.html': raise ValueError('render scenes via scene-NN.html, never index.html: '+entry)
        head=(Path(run)/entry).read_text(encoding='utf-8')[:400]
        if not re.search(r'<html[^>]*data-theme="dark"',head): raise ValueError('scene entry is not dark mode: '+entry)

def choose_backend(probes):
    valid=[p for p in probes if p['ok']]
    if not valid: raise RuntimeError('No working video encoder')
    return min(valid,key=lambda p:p['seconds']/p['workers'])

def stable_backend(backend):
    return {k:v for k,v in backend.items() if k not in ('seconds','workers','ok')}

def probe_backends(run):
    dest=Path(run)/'work/probes'; dest.mkdir(parents=True,exist_ok=True)
    versions={k:command([k,'-version']).stdout.splitlines()[0] for k in ('ffmpeg','ffprobe')}
    candidates=[]
    for encoder in ('libx264','h264_nvenc'):
        path=dest/(encoder+'.mp4'); start=time.monotonic()
        args=['ffmpeg','-y','-v','error','-f','lavfi','-i','color=c=black:s=1920x1080:r=30','-frames:v','60','-an','-c:v',encoder]
        args+=['-preset','veryfast'] if encoder=='libx264' else ['-preset','p5']
        r=command(args+['-pix_fmt','yuv420p',path],timeout=60)
        ok=r.returncode==0 and frames_ok(path,60) and command(['ffmpeg','-v','error','-i',path,'-f','null','-']).returncode==0
        candidates.append({'encoder':encoder,'ok':ok,'seconds':time.monotonic()-start,'workers':1,
          'capture_gpu':False,'decode_gpu':False,'tool_versions':versions})
    # Measure a two-worker NVENC encode only when VRAM headroom is observed.
    gpu=command(['nvidia-smi','--query-gpu=memory.free','--format=csv,noheader,nounits']) if shutil.which('nvidia-smi') else None
    nv=next(p for p in candidates if p['encoder']=='h264_nvenc')
    if nv['ok'] and gpu and gpu.returncode==0 and int(gpu.stdout.splitlines()[0])>=2048 and (os.cpu_count() or 1)>=4:
        def trial(i):
            p=dest/f'parallel-{i}.mp4'
            r=command(['ffmpeg','-y','-v','error','-f','lavfi','-i','color=c=black:s=1920x1080:r=30',
              '-frames:v','60','-an','-c:v','h264_nvenc','-preset','p5',p])
            return r.returncode==0 and frames_ok(p,60)
        start=time.monotonic()
        with ThreadPoolExecutor(max_workers=2) as pool: ok=all(pool.map(trial,range(2)))
        candidates.append(dict(nv,ok=ok,seconds=time.monotonic()-start,workers=2))
    result=dict(choose_backend(candidates))
    atomic_json(Path(run)/'verification/backend-probes.json',{'probes':candidates,'chosen':result})
    return result

def cpu_backend(entry,options):
    return dict(encoder='libx264',workers=1,capture_gpu=False,decode_gpu=False,
                hyperframes_entry=str(Path(entry).resolve()),render_options=validate_render_options(options))

def render_parts(parts,run,backend):
    run=Path(run)
    options=validate_render_options(backend['render_options']) if 'render_options' in backend else load_render_options(run)
    host=detect_hardware() if options['workers']=='auto' else None
    selections=[resolve_scene_workers(run,p,options,hardware=host) for p in parts]
    require_dark_entries(parts,run); dest=run/'renders/parts'; dest.mkdir(parents=True,exist_ok=True)
    entry=Path(backend['hyperframes_entry']).resolve()
    if not entry.is_file(): raise ValueError('HyperFrames Node entry is missing')
    versions=dict(backend.get('tool_versions',{}))
    version=command(['node',entry,'--version'])
    if version.returncode: raise RuntimeError('HyperFrames unavailable')
    versions['hyperframes']=version.stdout.strip()
    dependencies={p.relative_to(run).as_posix():file_hash(p) for p in run.rglob('*')
                  if p.is_file() and p.suffix in ('.html','.css','.js','.svg','.png','.jpg','.jpeg','.webp','.woff2')
                  and p.relative_to(run).parts[0] not in ('renders','verification','work')}
    renderer={name:file_hash(Path(__file__).with_name(name)) for name in ('render.py','render_options.py','workload.py')}
    outputs=[]
    for part,selection in zip(parts,selections):
        out=dest/(part['id']+'.mp4'); receipt=out.with_suffix('.json')
        motion_files=[run/'source/timeline.json',run/'source/scene-fragments'/(part['id']+'.motion.json')]
        metadata={p.relative_to(run).as_posix():file_hash(p) for p in motion_files if p.is_file()}
        key=digest({'motion_metadata':metadata,'part':part,'dependencies':dependencies,'render_options':options,'versions':versions,'renderer':renderer,'worker_selection':selection})
        old=None
        if receipt.exists():
            try: old=json.loads(receipt.read_text(encoding='utf-8'))
            except (OSError,ValueError): pass
        if isinstance(old,dict) and cache_valid(out,old,key) and frames_ok(out,part['frames']):
            outputs.append(out); continue
        out.with_name(out.stem+'.pending.mp4').unlink(missing_ok=True) # clean legacy abandoned output
        pending=out.with_name(out.stem+'.'+uuid.uuid4().hex+'.pending.mp4')
        args=[str(a) for a in ['node',entry,'render','--composition',part['entry'],'--quality','delivery',
                              '--workers',selection['workers'],'--experimental-fast-capture=false','--output',pending]]
        started=time.monotonic()
        try:
            try: r=command(args,run,timeout=3600)
            except subprocess.TimeoutExpired as ex:
                def text(value): return value.decode('utf-8',errors='replace') if isinstance(value,bytes) else (value or '')
                out.with_suffix('.log').write_text(text(ex.stdout)+'\n'+text(ex.stderr)+'\nrender timeout',encoding='utf-8')
                raise
            out.with_suffix('.log').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
            if r.returncode or not pending.is_file() or not frames_ok(pending,part['frames']):
                raise RuntimeError('scene render failed: '+part['id'])
            record={'key':key,'output_sha256':file_hash(pending),'frames':part['frames'],
                    'render_options':options,'worker_selection':selection,'args':args,'elapsed_seconds':time.monotonic()-started,'versions':versions}
            commit_media_receipt(pending,record,out,receipt)
            outputs.append(out)
        finally: pending.unlink(missing_ok=True)
    return outputs

def render_receipt_data(run,backend,parts,master):
    records=[json.loads(Path(p).with_suffix('.json').read_text(encoding='utf-8')) for p in parts]
    return dict(schema_version=1,render_options=backend['render_options'],parts=records,
                master_sha256=file_hash(master))

def write_render_receipt(run,backend,parts,master):
    path=Path(run)/'verification/render-receipt.json'
    atomic_json(path,render_receipt_data(run,backend,parts,master))
    return path

def mux_with_receipt(parts,audio,timeline,destination,backend,*,captured=None):
    destination=Path(destination)
    pending=destination.with_name(destination.stem+'.'+uuid.uuid4().hex+'.pending.mp4')
    receipt=destination.parent/'verification/render-receipt.json'
    try:
        mux(parts,audio,timeline,pending)
        data=render_receipt_data(destination.parent,backend,parts if captured is None else captured,pending)
        commit_media_receipt(pending,data,destination,receipt)
        return receipt
    finally:pending.unlink(missing_ok=True)

def mux(parts,audio,timeline,destination):
    destination=Path(destination); run=destination.parent; work=run/'work/mux'; work.mkdir(parents=True,exist_ok=True)
    sources=[Path(p).resolve() for p in parts]
    if destination.resolve() in sources: raise ValueError('refusing to overwrite source')
    lines=[]
    for i,p in enumerate(sources):
        target=work/f'part-{i:04d}.mp4'
        r=command(['ffmpeg','-y','-v','error','-i',p,'-map','0:v:0','-an','-c:v','copy',target])
        if r.returncode: raise RuntimeError('video-only extraction failed')
        lines.append("file '"+target.name+"'")
    (work/'concat.txt').write_text('\n'.join(lines),encoding='utf-8')
    pcm=bytearray(timeline['total_samples']*2); voices={a['id']:a for a in audio}
    for seg in timeline['segments']:
        rec=voices[seg['id']]; path=run/rec['path']
        with wave.open(str(path),'rb') as f:
            if (f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getnframes())!=(1,2,24000,rec['samples']):
                raise ValueError('audio format/length changed')
            raw=f.readframes(f.getnframes())
        start=seg['start_sample']*2
        if start+len(raw)>len(pcm): raise ValueError('audio exceeds timeline')
        pcm[start:start+len(raw)]=raw
    mixed=work/'narration.wav'
    with wave.open(str(mixed),'wb') as f:
        f.setparams((1,2,24000,0,'NONE','not compressed')); f.writeframes(pcm)
    pending=destination.with_name(destination.stem+'.pending.mp4')
    try:
        r=command(['ffmpeg','-y','-v','error','-f','concat','-safe','1','-i',work/'concat.txt','-i',mixed,
          '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart',pending])
        if r.returncode or not frames_ok(pending,timeline['total_frames']): raise RuntimeError('mux failed')
        decode=command(['ffmpeg','-v','error','-i',pending,'-f','null','-'],timeout=1800)
        if decode.returncode: raise RuntimeError('final decode failed')
        light=dark_failures(pending)
        if light: raise RuntimeError(f'final video is not dark mode at {light}s')
        os.replace(pending,destination)
    finally:pending.unlink(missing_ok=True)
