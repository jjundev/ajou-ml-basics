"""Use only existing cache/budget/Vertex modules with a private package name."""
from pathlib import Path
import importlib.util,importlib,sys,types
from .util import S,read,write,file_hash,digest
from .contracts import InputError
NAME='_ml_solution_video_lib'
def default_config(): return read(S/'assets/defaults.json')
def adapter_files():
    folder=S/'scripts/solution_video/vendor_tts'
    files=[folder/(n+'.py') for n in ['__init__','cache','budget','vertex_tts']]
    if not all(p.is_file() for p in files): raise InputError('local TTS adapter dependency missing')
    return files
def adapter_hash(): return digest({p.name:file_hash(p) for p in adapter_files()})
def _modules():
    from .vendor_tts import vertex_tts,budget
    return vertex_tts,budget
def validate_config(config):
    def scrub(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if any(s in k.lower() for s in ['api_key','apikey','credential','secret','authorization','access_token']): raise InputError('credentials must come from environment, never config')
                scrub(x)
        elif isinstance(v,list):
            for x in v: scrub(x)
    scrub(config)
    expected={'provider':'vertex-ai-express','language':'ko-KR','sample_rate':24000,'width':1920,'height':1080,'fps':30}
    if any(config.get(k)!=v for k,v in expected.items()): raise InputError('unsupported provider/media contract; no automatic substitute')
    if not config.get('model') or not config.get('voice'): raise InputError('model/voice must be explicit')
    if not 0<float(config.get('chars_per_second',7))<=8: raise InputError('invalid writing speed')
def generate_voice(segments,run,config,ledger,transport=None,env_file=None):
    validate_config(config);run=Path(run)
    from .speech_chunks import speech_items,join_segment_audio,validate_speech_chunks,_segment_plans
    chunk_mode=any('chunks' in s for s in segments)
    validate_speech_chunks(segments,required=chunk_mode);items=speech_items(segments)
    trims=None
    if (run/'source/chunk-trims.json').is_file():
        try:
            trims=read(run/'source/chunk-trims.json')
            if not chunk_mode:raise InputError('chunk trims require chunk speech')
            previous=read(run/'source/chunk-audio.json')['voices']
            _segment_plans(segments,previous,run,trims)
            from .speech_tts import make_speech_payload,POLICY
            by_id={a['id']:a for a in previous};by_item={i['id']:i for i in items}
            for row in trims['rows']:
                ident=row['segment_id']+'__'+row['chunk_id'];item=by_item[ident];rec=by_id[ident]
                payload=make_speech_payload(item['text'],config)
                key=digest(dict(policy=POLICY,text=item['text'],pronunciation=config.get('pronunciation',{}),model=config['model'],payload=payload))
                if rec.get('key')!=key or rec.get('policy')!=POLICY:raise InputError('trimmed speech input changed; remove or reauthor trims first')
        except (OSError,KeyError,ValueError,TypeError) as ex:raise InputError('invalid/stale chunk trims; refresh against saved raw PCM') from ex
    tts,budget=_modules()
    write(run/'source/adapter.json',{'sha256':adapter_hash(),'files':{str(p):file_hash(p) for p in adapter_files()}})
    write(run/'source/config.json',config)
    # Credentials stay in memory inside live_transport; its errors are sanitized.
    transport=transport or tts.live_transport(tts.load_key(env_file),config['model'])
    b=budget.Budget(Path(ledger),limit_usd=config.get('budget_usd'))
    from .speech_tts import synthesize_speech
    audio=synthesize_speech(items,run,config,b,transport)
    if chunk_mode:
        write(run/'source/chunk-audio.json',{'policy':'spoken-text-only-v1','voices':audio})
        audio=join_segment_audio(segments,audio,run,trims)
    write(run/'source/audio.json',{'voices':audio})
    return audio
