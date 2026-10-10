"""Explicit speech/caption pairs and measured PCM boundaries."""
from pathlib import Path
import re,os,wave,tempfile
from .contracts import InputError
from .util import read,write,local,file_hash,digest

MODE='pcm-chunks-v1'

def _normalized(value):
    if not isinstance(value,str) or not value.strip():raise InputError('nonempty chunk text required')
    return ' '.join(value.split())

def validate_speech_chunks(segments:list[dict],*,required:bool)->None:
    from .subtitles import caption_text,chunk_caption
    identities=set()
    for segment in segments:
        sid=segment.get('id','unknown');chunks=segment.get('chunks')
        def fail(why):raise InputError('segment '+str(sid)+': '+why)
        if not isinstance(sid,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',sid):fail('invalid segment ID')
        if chunks is None:
            if required:fail('speech chunks required')
            if sid in identities:fail('duplicate speech identity')
            identities.add(sid);continue
        if not isinstance(chunks,list) or not chunks:fail('nonempty speech chunks required')
        ids=set()
        for chunk in chunks:
            if not isinstance(chunk,dict):fail('chunk must be an object')
            cid=chunk.get('id')
            if not isinstance(cid,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',cid):fail('invalid chunk ID')
            ident=sid+'__'+cid
            if cid in ids or ident in identities:fail('duplicate speech identity '+ident)
            ids.add(cid);identities.add(ident)
            try:
                _normalized(chunk.get('text'))
                if 'caption_text' not in chunk:fail('chunk '+cid+' caption_text required')
                chunk_caption(caption_text(dict(chunk,id=ident)))
            except InputError as ex:fail('chunk '+cid+': '+str(ex))
        for key in ['text','caption_text']:
            if _normalized(segment.get(key))!=_normalized(' '.join(chunk[key] for chunk in chunks)):
                fail(key+' differs from joined speech chunks')

def speech_items(segments:list[dict])->list[dict]:
    validate_speech_chunks(segments,required=False)
    items=[]
    for segment in segments:
        if 'chunks' not in segment:items.append(dict(id=segment['id'],text=segment['text']));continue
        for chunk in segment['chunks']:
            items.append(dict(id=segment['id']+'__'+chunk['id'],segment_id=segment['id'],chunk_id=chunk['id'],text=chunk['text']))
    return items

def _pcm(record,run):
    try:
        path=local(run,record['path'])
        if type(record['samples']) is not int or record['samples']<=0 or record['rate']!=24000 or file_hash(path)!=record['sha256']:
            raise InputError('PCM provenance mismatch')
        with wave.open(str(path),'rb') as w:
            if (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes(),w.getcomptype())!=(1,2,24000,record['samples'],'NONE'):
                raise InputError('PCM format mismatch')
            raw=w.readframes(w.getnframes())
            if len(raw)!=record['samples']*2:raise InputError('PCM truncated')
            return raw
    except (OSError,KeyError,TypeError,wave.Error) as ex:raise InputError('invalid chunk PCM') from ex

def _segment_plans(segments,chunk_audio,run,trims):
    validate_speech_chunks(segments,required=True)
    items=speech_items(segments);records={a['id']:a for a in chunk_audio}
    if len(records)!=len(chunk_audio) or set(records)!={i['id'] for i in items}:raise InputError('chunk audio/manifest mismatch')
    trim_rows={}
    if trims is not None:
        if not isinstance(trims,dict) or trims.get('schema_version')!=1 or not isinstance(trims.get('rows'),list):raise InputError('invalid chunk trims')
        allowed={(i['segment_id'],i['chunk_id']) for i in items}
        for row in trims['rows']:
            if not isinstance(row,dict):raise InputError('invalid chunk trim row')
            pair=(row.get('segment_id'),row.get('chunk_id'))
            if pair not in allowed or pair in trim_rows or not isinstance(row.get('reason'),str) or not row['reason'].strip():raise InputError('invalid or duplicate chunk trim')
            trim_rows[pair]=row
    plans=[]
    for segment in segments:
        chunks=[];parts=[];offset=0
        for chunk in segment['chunks']:
            ident=segment['id']+'__'+chunk['id'];a=records[ident];raw=_pcm(a,run)
            lo,hi=0,a['samples'];trim=trim_rows.get((segment['id'],chunk['id']))
            if trim:
                lo,hi=trim.get('start_sample'),trim.get('end_sample')
                if (type(lo) is not int or type(hi) is not int or not 0<=lo<hi<=a['samples']
                    or trim.get('raw_sha256')!=a['sha256']):raise InputError('invalid/stale chunk trim '+ident)
            chunks.append(dict(id=chunk['id'],source_id=ident,raw_sha256=a['sha256'],trim_start_sample=lo,trim_end_sample=hi,start_sample=offset,end_sample=offset+hi-lo))
            parts.append(raw[lo*2:hi*2]);offset+=hi-lo
        key=digest(dict(policy=MODE,segment_id=segment['id'],chunks=chunks))
        plans.append(dict(id=segment['id'],raw=b''.join(parts),samples=offset,rate=24000,key=key,chunks=chunks))
    return plans

def join_segment_audio(segments:list[dict],chunk_audio:list[dict],run:Path,trims:dict|None=None)->list[dict]:
    run=Path(run);dest=run/'assets/voice';dest.mkdir(parents=True,exist_ok=True);out=[]
    for plan in _segment_plans(segments,chunk_audio,run,trims):
        path=dest/(plan['id']+'-joined-'+plan['key'][:16]+'.wav');pending=path.with_suffix('.pending.wav')
        with wave.open(str(pending),'wb') as w:w.setparams((1,2,24000,0,'NONE',''));w.writeframes(plan['raw'])
        os.replace(pending,path)
        rec={k:v for k,v in plan.items() if k!='raw'}
        rec.update(path=path.relative_to(run).as_posix(),sha256=file_hash(path),output_sha256=file_hash(path),policy=MODE)
        write(path.with_suffix('.json'),rec);out.append(rec)
    return out

def validate_chunk_audio(segments:list[dict],voices:list[dict],run:Path)->None:
    if not any('chunks' in s for s in segments):return
    run=Path(run);a=read(run/'source/chunk-audio.json')['voices']
    trim_path=run/'source/chunk-trims.json';trims=read(trim_path) if trim_path.is_file() else None
    cfg_path=run/'source/config.json'
    if cfg_path.is_file():
        from .speech_tts import make_speech_payload,POLICY
        cfg=read(cfg_path);items={i['id']:i for i in speech_items(segments)}
        for rec in a:
            if rec.get('id') not in items:raise InputError('unknown chunk receipt')
            item=items[rec['id']];payload=make_speech_payload(item['text'],cfg)
            key=digest(dict(policy=POLICY,text=item['text'],pronunciation=cfg.get('pronunciation',{}),model=cfg['model'],payload=payload))
            if rec.get('policy')!=POLICY or rec.get('payload_hash')!=digest(payload) or rec.get('key')!=key:raise InputError('stale speech chunk receipt')
    plans=_segment_plans(segments,a,run,trims);actual={v['id']:v for v in voices}
    if len(actual)!=len(voices) or set(actual)!={s['id'] for s in segments}:raise InputError('joined segment mismatch')
    for expected in plans:
        record=actual[expected['id']]
        if any(record.get(k)!=expected[k] for k in ['samples','rate','key','chunks']) or _pcm(record,run)!=expected['raw']:
            raise InputError('joined PCM/chunk boundaries changed: '+expected['id'])

def validate_caption_cues(timeline:dict)->list[dict]:
    from .subtitles import caption_text,chunk_caption
    cues=timeline.get('caption_cues')
    if timeline.get('caption_timing')!=MODE or not isinstance(cues,list) or not cues:raise InputError('measured caption cues required')
    index=0;previous_end=0
    for seg in timeline['segments']:
        chunks=seg.get('chunks');cursor=seg['start_sample']
        if not isinstance(chunks,list) or not chunks:raise InputError('missing timeline speech chunks')
        for chunk in chunks:
            if index>=len(cues):raise InputError('missing caption cue')
            cue=cues[index];index+=1
            lo,hi=cue.get('start_sample'),cue.get('end_sample')
            chunk_caption(caption_text(cue))
            if (cue.get('segment_id')!=seg['id'] or cue.get('chunk_id')!=chunk['id']
                or caption_text(cue)!=caption_text(chunk)
                or type(lo) is not int or type(hi) is not int or lo!=cursor or lo<previous_end or hi-lo<24
                or hi>seg['start_sample']+seg['voice_samples']):raise InputError('invalid measured caption cue')
            cursor=hi;previous_end=hi
        if cursor!=seg['start_sample']+seg['voice_samples'] or cursor>seg['end_sample']:raise InputError('caption/voice coverage mismatch')
    if index!=len(cues):raise InputError('extra caption cue')
    return cues

def chunk_review_passed(review:dict,manifest:dict)->bool:
    if manifest.get('caption_timing')!=MODE:return True
    if review.get('mode')!='live-listened':return False
    expected=[(s['id'],c['id']) for s in manifest['segments'] for c in s['chunks']]
    rows=review.get('chunk_checks')
    if not isinstance(rows,list) or any(not isinstance(r,dict) for r in rows):return False
    if [(r.get('segment_id'),r.get('chunk_id')) for r in rows]!=expected:return False
    return all(all(r.get(k) is True for k in ['transcript_match','no_instruction_speech','natural_join','sync_passed'])
               and isinstance(r.get('notes'),str) and r['notes'].strip() for r in rows)

def verify_chunk_sync(run:Path)->dict:
    from .subtitles import write_srt
    from .teaching import build_teaching_timeline
    from .annotations import load_teaching
    from .writing import load_writing
    run=Path(run).resolve();issues=[];hashes={}
    try:
        m=read(run/'source/manifest.json');t=read(run/'source/timeline.json')
        if m.get('caption_timing')!=MODE or t.get('caption_timing')!=MODE:raise InputError('chunk timing mode required')
        voices=read(run/'source/audio.json')['voices'];validate_chunk_audio(m['segments'],voices,run)
        validate_caption_cues(t)
        l=read(run/'layers/layers.json');cfg=read(run/'source/config.json')
        writing=load_writing(run,cfg) if (run/'source/writing.json').is_file() else None
        if l.get('schema_version')==2:
            from .bundle_timeline import build_bundle_timeline
            expected=build_bundle_timeline(m,l,voices,cfg,writing,load_teaching(run,m,l))
        else:expected=build_teaching_timeline(m,l,voices,cfg,writing,load_teaching(run,m,l))
        if t['caption_cues']!=expected['caption_cues']:raise InputError('timeline differs from measured PCM')
        with tempfile.TemporaryDirectory(prefix='ml-chunk-sync-') as td:
            path=write_srt(expected,Path(td)/'expected.srt')
            if path.read_bytes()!=(run/'renders/captions.srt').read_bytes():raise InputError('SRT differs from measured chunk boundaries')
        paths=[run/'source/manifest.json',run/'source/audio.json',run/'source/chunk-audio.json',run/'source/timeline.json',run/'renders/captions.srt']
        paths.extend(local(run,a['path']) for a in voices)
        paths.extend(local(run,a['path']) for a in read(run/'source/chunk-audio.json')['voices'])
        paths.extend([run/'source/chunk-trims.json'] if (run/'source/chunk-trims.json').is_file() else [])
        hashes={p.relative_to(run).as_posix():file_hash(p) for p in paths}
    except (InputError,OSError,KeyError,TypeError,ValueError) as ex:issues.append(str(ex)[:500])
    result=dict(status='passed' if not issues else 'unverified',input_hash=digest(hashes),evidence_hashes=hashes,issues=issues)
    write(run/'verification/chunk-sync.json',result);return result
