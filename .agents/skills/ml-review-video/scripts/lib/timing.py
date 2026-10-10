from pathlib import Path

def frame_at(sample,rate=24000,fps=30): return (sample*fps*2+rate)//(2*rate)
def end_frame(sample,rate=24000,fps=30): return (sample*fps+rate-1)//rate

def build_timeline(m,audio,fps=30):
    if fps!=30: raise ValueError('v1 requires 30fps')
    voices={a['id']:a for a in audio}
    if len(voices)!=len(audio) or set(voices)!={s['id'] for s in m['segments']}:
        raise ValueError('audio IDs do not match script')
    for a in audio:
        if a.get('rate')!=24000 or type(a.get('samples')) is not int or a['samples']<=0:
            raise ValueError('invalid PCM sample count/rate')
    t={'rate':24000,'fps':fps,'scenes':[],'segments':[]}; cursor=0
    for scene in m['scenes']:
        start=cursor; cursor+=13200
        segs=[s for s in m['segments'] if s['scene_id']==scene['id']]
        if not segs: raise ValueError('empty scene')
        for s in segs:
            a=voices[s['id']]; finish=cursor+a['samples']
            t['segments'].append(dict(s,start_sample=cursor,end_sample=finish,path=a.get('path','')))
            cursor=finish+7200
        cursor+=18000
        t['scenes'].append({'id':scene['id'],'title':scene.get('title',scene['visual']),
          'start_sample':start,'end_sample':cursor,'first_frame':frame_at(start),'last_frame':frame_at(cursor)})
    if not t['scenes']: raise ValueError('empty timeline')
    t['total_samples']=cursor; t['total_frames']=end_frame(cursor)
    t['scenes'][-1]['last_frame']=t['total_frames']
    return t

def _stamp(sample,separator=','):
    ms=(sample*1000+12000)//24000
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d}{separator}{ms%1000:03d}'

def write_subtitles(timeline,run):
    run=Path(run)
    text='\n'.join(f"{i}\n{_stamp(s['start_sample'])} --> {_stamp(s['end_sample'])}\n{s['text']}\n"
                   for i,s in enumerate(timeline['segments'],1))
    (run/'narration.srt').write_text(text,encoding='utf-8')
    (run/'chapters.txt').write_text('\n'.join(_stamp(s['start_sample'],'.')+' '+s['title'] for s in timeline['scenes']),encoding='utf-8')
