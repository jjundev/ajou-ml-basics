"""Solution-video TTS: spoken text only, independently versioned cache."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
import os,re,threading,time,uuid,wave
from .contracts import InputError
from .util import digest,file_hash,read,write

POLICY='spoken-text-only-v1'

def make_speech_payload(text:str,config:dict)->dict:
    if not isinstance(text,str) or not text.strip():raise InputError('nonempty spoken text required')
    for original,spoken in config.get('pronunciation',{}).items():text=text.replace(original,spoken)
    return {'contents':[{'role':'user','parts':[{'text':text}]}],
            'generationConfig':{'responseModalities':['AUDIO'],'maxOutputTokens':config['max_output_tokens'],
              'speechConfig':{'languageCode':'ko-KR','voiceConfig':{'prebuiltVoiceConfig':{'voiceName':config['voice']}}}}}

def synthesize_speech(items:list[dict],run:Path,config:dict,budget:object,transport,*,sleep=time.sleep)->list[dict]:
    from .review_adapter import _modules
    tts,_=_modules();run=Path(run);dest=run/'assets/voice';dest.mkdir(parents=True,exist_ok=True)
    if not items or len({i.get('id') for i in items})!=len(items):raise InputError('nonempty unique speech items required')
    for item in items:
        if not isinstance(item.get('id'),str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',item['id']):raise InputError('invalid speech ID')
        make_speech_payload(item.get('text'),config)
    throttled=threading.Event()
    def one(item):
        payload=make_speech_payload(item['text'],config)
        key=digest(dict(policy=POLICY,text=item['text'],pronunciation=config.get('pronunciation',{}),model=config['model'],payload=payload))
        wav=dest/(item['id']+'-'+key[:16]+'.wav');receipt=wav.with_suffix('.json')
        if receipt.is_file() and wav.is_file():
            try:
                rec=read(receipt)
                if (isinstance(rec,dict) and type(rec.get('samples')) is int and rec['samples']>0 and rec.get('rate')==24000
                    and rec.get('policy')==POLICY and rec.get('key')==key and rec.get('id')==item['id']
                    and rec.get('path')==wav.relative_to(run).as_posix() and rec.get('payload_hash')==digest(payload)
                    and rec.get('sha256')==rec.get('output_sha256')==file_hash(wav)):
                    with wave.open(str(wav),'rb') as f:
                        if (f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getnframes(),f.getcomptype())==(1,2,24000,rec['samples'],'NONE'):
                            return rec
            except (ValueError,OSError,KeyError,wave.Error):pass
        rates,upper=tts._pricing(config,payload)
        for attempt in range(max(1,min(4,int(config.get('max_attempts',4))))):
            request_id=str(uuid.uuid4())
            if not budget.reserve(request_id,upper):raise tts.VertexError(reason='budget exhausted')
            try:response=transport(payload)
            except Exception as ex:
                budget.settle(request_id,None)
                status=ex.status if isinstance(ex,tts.VertexError) else None
                retry=isinstance(ex,tts.VertexError) and (status in (429,500,502,503,504) or status is None)
                if status==429:throttled.set()
                if not retry or attempt+1>=min(4,int(config.get('max_attempts',4))):raise tts.VertexError(status,'transport failure') from None
                sleep(min(45,5*2**attempt));continue
            usage=response.get('usageMetadata',{})
            if rates is not None and all(type(usage.get(k)) is int and usage[k]>=0 for k in ('promptTokenCount','candidatesTokenCount')):
                cost=(usage['promptTokenCount']*rates[0]+usage['candidatesTokenCount']*rates[1])/Decimal(1000000)
                budget.settle(request_id,cost,usage)
            else:budget.settle(request_id,None,usage)
            try:raw=tts._decode(response)
            except Exception:raise tts.VertexError(reason='invalid or incomplete audio') from None
            pending=wav.with_suffix('.pending.wav')
            with wave.open(str(pending),'wb') as f:
                f.setparams((1,2,24000,0,'NONE','not compressed'));f.writeframes(raw)
            os.replace(pending,wav)
            rec=dict(id=item['id'],path=wav.relative_to(run).as_posix(),samples=len(raw)//2,rate=24000,
                     key=key,sha256=file_hash(wav),output_sha256=file_hash(wav),policy=POLICY,payload_hash=digest(payload),
                     usage={k:v for k,v in usage.items() if type(v) is int})
            write(receipt,rec);return rec
        raise tts.VertexError(reason='attempts exhausted')
    out=[];index=0
    while index<len(items):
        workers=1 if throttled.is_set() else max(1,min(4,int(config.get('tts_concurrency',2))))
        batch=items[index:index+workers]
        with ThreadPoolExecutor(max_workers=workers) as pool:out.extend(pool.map(one,batch))
        index+=len(batch)
    return out
