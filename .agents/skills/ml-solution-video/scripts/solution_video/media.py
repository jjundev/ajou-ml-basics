from pathlib import Path
from fractions import Fraction
import functools,json,os,shutil,subprocess,time,wave
from .util import checked,command,write,file_hash,local
from .contracts import InputError
from .render_options import load_render_options,validate_render_options
@functools.lru_cache
def ffmpeg():
    candidates=[os.environ.get('ML_FFMPEG'),shutil.which('ffmpeg'),'/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg']
    for p in candidates:
        if p and Path(p).is_file() and ' subtitles ' in command([p,'-filters']).stdout: return p
    raise InputError('FFmpeg with libass subtitles missing; supply ML_FFMPEG')
def probe(path): return json.loads(checked(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]).stdout)
def source_checks(parts,run,entry):
    result=[]
    for p in parts:
        html=local(run,p['entry']); args=['node',entry,'check',html.parent,'--json','--samples','3']
        r=command(args,timeout=180)
        dest=Path(run)/'verification'/('check-'+p['key']+'.json'); write(dest,{'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'entry_sha256':file_hash(entry),'html_sha256':file_hash(html)})
        if r.returncode: raise InputError('HyperFrames check failed; inspect '+str(dest))
        result.append(dest)
    return result


def _validate_media(path,frames,*,audio=False):
    try:
        streams=probe(path)['streams']
        video=next(s for s in streams if s['codec_type']=='video')
        if (int(video['width']),int(video['height']),Fraction(video['r_frame_rate']),int(video['nb_frames']))!=(1920,1080,Fraction(30),frames):
            raise InputError('render video contract mismatch: '+str(path))
        if audio:
            voice=next(s for s in streams if s['codec_type']=='audio')
            if (int(voice['sample_rate']),int(voice['channels']))!=(24000,1):
                raise InputError('master audio must be mono 24kHz')
    except (KeyError,TypeError,ValueError,StopIteration,ZeroDivisionError) as ex:
        raise InputError('invalid render metadata: '+str(path)) from ex


def _commit_master_and_receipt(master_pending: Path,receipt_data: dict,master: Path,receipt: Path) -> None:
    receipt_pending=receipt.with_name(receipt.name+'.pending')
    targets=[master,receipt];backups={};replaced=[];cleanup_backups=False
    try:
        retained=[t.with_name(t.name+'.rollback') for t in targets if t.with_name(t.name+'.rollback').exists()]
        if retained:raise InputError('unresolved render recovery copies; inspect before retry: '+', '.join(map(str,retained)))
        write(receipt_pending,receipt_data)
        for target in targets:
            if target.exists():
                backup=target.with_name(target.name+'.rollback')
                shutil.copyfile(target,backup);backups[target]=backup
        for pending,target in [(master_pending,master),(receipt_pending,receipt)]:
            os.replace(pending,target);replaced.append(target)
        cleanup_backups=True
    except BaseException as original:
        failures=[]
        for target in reversed(replaced):
            try:
                if target in backups:os.replace(backups[target],target)
                else:target.unlink(missing_ok=True)
            except BaseException as error:failures.append(error)
        if failures:
            retained=[str(p) for p in backups.values() if p.exists()]
            raise InputError('render rollback failed; recovery copies retained: '+', '.join(retained)) from original
        cleanup_backups=True
        raise
    finally:
        master_pending.unlink(missing_ok=True)
        receipt_pending.unlink(missing_ok=True)
        receipt_pending.with_suffix(receipt_pending.suffix+'.pending').unlink(missing_ok=True)
        if cleanup_backups:
            for backup in backups.values():backup.unlink(missing_ok=True)


def _log_text(value):
    return value.decode('utf-8',errors='replace') if isinstance(value,bytes) else value or ''


def render_master(parts: list[dict],timeline: dict,audio: list[dict],run: Path,hyperframes_entry: Path,*,render_options: dict[str,object] | None=None) -> Path:
    run=Path(run).resolve();entry=Path(hyperframes_entry).resolve()
    options=load_render_options(run) if render_options is None else validate_render_options(render_options)
    source_checks(parts,run,entry)
    outputs=[];records=[];work=run/'renders';work.mkdir(parents=True,exist_ok=True)
    for part in parts:
        html=local(run,part['entry']);out=work/(part['key']+'.mp4');pending=work/(part['key']+'.pending.mp4')
        args=[str(a) for a in ['node',entry,'render','--composition',html.name,'--quality','delivery','--workers',options['workers'],'--experimental-fast-capture=false','--output',pending]]
        log=work/(part['key']+'.log');start=time.perf_counter()
        try:
            pending.unlink(missing_ok=True)
            r=command(args,cwd=html.parent,timeout=7200)
            log.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
            if r.returncode or not pending.is_file():raise InputError('HyperFrames render failed; inspect '+str(log))
            frames=part['last_frame']-part['first_frame'];_validate_media(pending,frames)
            record=dict(key=part['key'],command=args,elapsed_seconds=time.perf_counter()-start,output_sha256=file_hash(pending),frames=frames)
            os.replace(pending,out);outputs.append(out);records.append(record)
        except Exception as ex:
            if isinstance(ex,subprocess.TimeoutExpired):
                log.write_text(_log_text(ex.stdout)+'\n'+_log_text(ex.stderr)+'\n'+str(ex),encoding='utf-8')
            else:
                with log.open('a',encoding='utf-8') as f:f.write('\n'+str(ex))
            raise
        finally:pending.unlink(missing_ok=True)
    mixed=bytearray(timeline['total_samples']*2);voices={a['id']:a for a in audio}
    for s in timeline['segments']:
        a=voices[s['id']];p=local(run,a['path'])
        if file_hash(p)!=a['sha256']:raise InputError('PCM hash changed')
        with wave.open(str(p),'rb') as f:
            if (f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getnframes())!=(1,2,24000,a['samples']):raise InputError('PCM provenance mismatch')
            raw=f.readframes(f.getnframes())
        start=s['start_sample']*2
        if start+len(raw)>s['end_sample']*2:raise InputError('voice exceeds measured slot')
        mixed[start:start+len(raw)]=raw
    with wave.open(str(work/'narration.wav'),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes(mixed)
    for i,p in enumerate(outputs):shutil.copyfile(p,work/f'part-{i}.mp4')
    (work/'concat.txt').write_text('\n'.join("file 'part-"+str(i)+".mp4'" for i in range(len(outputs))),encoding='utf-8')
    master=work/'master.mp4';pending=work/'master.pending.mp4'
    try:
        pending.unlink(missing_ok=True)
        checked([ffmpeg(),'-y','-v','error','-f','concat','-safe','1','-i','concat.txt','-i','narration.wav','-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart',pending],cwd=work,timeout=300)
        _validate_media(pending,timeline['total_frames'],audio=True)
        receipt=dict(schema_version=1,options=options,parts=records,master_sha256=file_hash(pending))
        _commit_master_and_receipt(pending,receipt,master,run/'verification/render-receipt.json')
    except Exception as ex:
        with (work/'master.log').open('a',encoding='utf-8') as f:
            if isinstance(ex,subprocess.TimeoutExpired):f.write(_log_text(ex.stdout)+'\n'+_log_text(ex.stderr)+'\n')
            f.write(str(ex)+'\n')
        raise
    finally:pending.unlink(missing_ok=True)
    return master
