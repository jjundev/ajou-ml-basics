from pathlib import Path
from fractions import Fraction
import array,json,math,wave,shutil,tempfile,subprocess
from .cache import atomic_json,digest,file_hash
from .manifest import validate_manifest
from .math_evidence import validate_math_evidence
from .render import command,probe_media,dark_failures

DOMAINS=('content','audio','visual','source','media','sync')

def review_fingerprint(run,m):
    run=Path(run)
    files={p.relative_to(run).as_posix():file_hash(p) for p in run.rglob('*')
      if p.is_file() and p.relative_to(run).parts[0] not in ('verification','work','renders')
      and p.name not in ('run.json','cost-ledger.json','config.json') and p.suffix!='.lock'}
    return digest({'manifest':m,'files':files})

def verify_media(path,expected):
    errors=[]
    try:
        data=probe_media(path)
        videos=[s for s in data['streams'] if s['codec_type']=='video']
        audio=[s for s in data['streams'] if s['codec_type']=='audio']
        if len(videos)!=1 or len(audio)!=1: raise ValueError('expected one video and one audio stream')
        v,a=videos[0],audio[0]
        if (v['width'],v['height'])!=(1920,1080): errors.append('resolution')
        if Fraction(v['avg_frame_rate'])!=30: errors.append('fps')
        if int(v.get('nb_frames',-1))!=expected['total_frames']: errors.append('frames')
        if int(a.get('sample_rate',0))!=24000 or a.get('channels')!=1: errors.append('audio-format')
        if abs(float(v['duration'])-float(a['duration']))>1/30+1024/24000: errors.append('av-end-drift')
        if dark_failures(path): errors.append('not-dark')
        decoded=command(['ffmpeg','-v','error','-i',path,'-f','null','-'],timeout=1800)
        if decoded.returncode or decoded.stderr.strip(): errors.append('decode')
        return {'status':'failed' if errors else 'passed','errors':errors,'probe':data,'decode_exit':decoded.returncode,'decode_stderr':decoded.stderr}
    except (OSError,ValueError,KeyError,StopIteration) as ex:
        return {'status':'failed','errors':[type(ex).__name__]}

def verify_audio(run,audio,timeline):
    errors=[]; metrics=[]
    positions={s['id']:s for s in timeline['segments']}
    for rec in audio:
        try:
            p=Path(run)/rec['path']
            if rec.get('sha256') and file_hash(p)!=rec['sha256']: raise ValueError('hash')
            with wave.open(str(p),'rb') as f:
                if (f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getnframes())!=(1,2,24000,rec['samples']): raise ValueError('format')
                values=array.array('h',f.readframes(f.getnframes()))
            peak=max(abs(x) for x in values); rms=math.sqrt(sum(x*x for x in values)/len(values))
            clipping=sum(abs(x)>=32760 for x in values)/len(values)
            if peak<32 or rms<8: errors.append(rec['id']+':silent')
            if clipping>.001: errors.append(rec['id']+':clipping')
            s=positions[rec['id']]
            if s['end_sample']-s['start_sample']!=len(values): errors.append(rec['id']+':duration')
            metrics.append({'id':rec['id'],'rms_db':20*math.log10(max(rms,1)/32768),'peak':peak,'clipped_fraction':clipping,'seconds':len(values)/24000})
        except (OSError,ValueError,KeyError,wave.Error): errors.append(rec['id']+':invalid')
    if set(positions)!={r['id'] for r in audio}: errors.append('audio-ID-mismatch')
    return {'status':'failed' if errors else 'passed','errors':errors,'metrics':metrics}

def verify_sync(run,audio,timeline):
    run=Path(run); decoded=run/'work/sync-decoded.wav'; decoded.parent.mkdir(parents=True,exist_ok=True)
    r=command(['ffmpeg','-y','-v','error','-i',run/'review.mp4','-map','0:a:0','-ac','1','-ar','24000','-c:a','pcm_s16le',decoded],timeout=1800)
    if r.returncode: return {'status':'failed','errors':['cannot decode final audio']}
    with wave.open(str(decoded),'rb') as f: actual=array.array('h',f.readframes(f.getnframes()))
    voices={a['id']:a for a in audio}; errors=[]; metrics=[]
    if abs(len(actual)-timeline['total_samples'])>1024: errors.append('final audio sample count')
    for s in timeline['segments']:
        with wave.open(str(run/voices[s['id']]['path']),'rb') as f: expected=array.array('h',f.readframes(f.getnframes()))
        trim=min(1200,len(expected)//10)
        left=list(expected[trim:len(expected)-trim:4])
        right=list(actual[s['start_sample']+trim:s['end_sample']-trim:4])
        if len(left)!=len(right) or not left:
            errors.append(s['id']+':missing-final-audio'); continue
        energy=sum(x*x for x in left); error=sum((x-y)**2 for x,y in zip(left,right))
        relative=math.sqrt(error/max(energy,1))
        metrics.append({'id':s['id'],'relative_pcm_error':relative,'start_sample':s['start_sample']})
        if relative>.20: errors.append(s['id']+':final-audio-position-or-content')
    return {'status':'failed' if errors else 'passed','errors':errors,'segments':metrics}

def check_sources(run,entry,timeout=300):
    run=Path(run)
    parts=json.loads((run/'source/parts.json').read_text(encoding='utf-8'))['parts']
    evidence=[]; errors=[]; timed_out=False
    (run/'work').mkdir(exist_ok=True)
    # Raw template snapshots are reference inputs, not compositions. Check a
    # clean staging project containing only the real editable render sources.
    with tempfile.TemporaryDirectory(dir=run/'work',prefix='source-check-',ignore_cleanup_errors=True) as d:
        stage=Path(d)
        shutil.copytree(run/'assets',stage/'assets')
        (stage/'source').mkdir()
        for p in (run/'source').glob('*.css'): shutil.copyfile(p,stage/'source'/p.name)
        shutil.copytree(run/'source/compositions',stage/'source/compositions')
        for part in parts+[{'id':'main','entry':'index.html'}]:
            shutil.copyfile(run/part['entry'],stage/'index.html')
            p=run/'verification'/('source-check-'+part['id']+'.txt'); p.parent.mkdir(parents=True,exist_ok=True)
            try: r=command(['node',entry,'check',str(stage),'--json','--at-transitions'],stage,timeout=timeout)
            except subprocess.TimeoutExpired:
                p.write_text('Source check timed out; not verified.',encoding='utf-8')
                evidence.append(p.relative_to(run).as_posix()); errors.append('timeout: '+part['id']); timed_out=True
                continue
            p.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8'); evidence.append(p.relative_to(run).as_posix())
            if r.returncode: errors.append('HyperFrames source check: '+part['id'])
    return {'status':'unverified' if timed_out else ('failed' if errors else 'passed'),'evidence':evidence,'errors':errors}

def verify_run(run,m,reports):
    run=Path(run); key=review_fingerprint(run,m); result={}
    for domain in DOMAINS:
        item=dict(reports.get(domain,{'status':'unverified','errors':['missing report'],'evidence':[]}))
        evidence=item.get('evidence',[])
        if item.get('status')=='passed':
            if item.get('input_hash')!=key or not evidence or any(not (run/p).is_file() or not (run/p).resolve().is_relative_to(run.resolve()) for p in evidence):
                item={'status':'unverified','errors':['missing, stale or external evidence'],'evidence':evidence}
        result[domain]=item
    errors=validate_manifest(m)+validate_math_evidence(run,m)
    if errors: result['content']={'status':'failed','errors':errors,'evidence':[]}
    result['complete']=all(result[k]['status']=='passed' for k in DOMAINS)
    result['input_hash']=key
    result['evidence_hashes']={p:file_hash(run/p) for k in DOMAINS for p in result[k].get('evidence',[]) if (run/p).is_file() and (run/p).resolve().is_relative_to(run.resolve())}
    atomic_json(run/'verification/report.json',result)
    return result

def publish_latest(run,report):
    run=Path(run)
    if not report.get('complete') or any(report.get(k,{}).get('status')!='passed' for k in DOMAINS):
        raise ValueError('run is not fully verified')
    try:
        m=json.loads((run/'manifest.json').read_text(encoding='utf-8'))
        if review_fingerprint(run,m)!=report['input_hash']: raise ValueError('artifacts changed after verification')
        for p,h in report['evidence_hashes'].items():
            if file_hash(run/p)!=h: raise ValueError('evidence changed after verification')
        video=run/'review.mp4'
        atomic_json(run.parent/'latest.json',{'run_id':run.name,'video':run.name+'/review.mp4','sha256':file_hash(video)})
    except (OSError,KeyError): raise ValueError('missing verified artifacts') from None
