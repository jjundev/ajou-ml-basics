from pathlib import Path
from html.parser import HTMLParser
import html,json,re,shutil
from .cache import digest,file_hash,atomic_json
from .theme import scene_shell
from .math_render import require_katex,render_math_fragment,katex_css

class FragmentParser(HTMLParser):
    def __init__(self,sid):
        super().__init__(); self.ids=set(); self.sid=sid; self.assets=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','iframe','object','embed','link','base','style'):
            raise ValueError('executable/remote fragment tag: '+tag)
        for k,v in attrs:
            if k.startswith('on') or k=='style': raise ValueError('use template CSS; no inline executable/style attributes')
            if k=='id':
                if v in self.ids or not v.startswith(self.sid+'-') or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',v):
                    raise ValueError('IDs must be unique and scene-prefixed')
                self.ids.add(v)
            if k in ('src','href','xlink:href') and v and not v.startswith('#'):
                if ':' in v or v.startswith(('/','\\')) or '..' in Path(v).parts: raise ValueError('nonlocal asset')
                self.assets.append(v)
    handle_startendtag=handle_starttag

def validate_fragment(fragment,sid):
    p=FragmentParser(sid); p.feed(fragment); return p

def stage_assets(source,run):
    source=Path(source); run=Path(run)
    for folder in ('fonts','vendor'):
        target=run/'assets'/folder; target.mkdir(parents=True,exist_ok=True)
    css=[]
    for name,weight in (('Regular','400'),('SemiBold','600'),('Bold','700 900')):
        src=source/'fonts'/('Pretendard-'+name+'.woff2')
        if not src.is_file(): raise ValueError('missing font: '+str(src))
        shutil.copyfile(src,run/'assets/fonts'/src.name)
        css.append("@font-face{font-family:Pretendard;src:url('"+src.name+"') format('woff2');font-weight:"+weight+";font-display:block}")
    shutil.copyfile(source/'vendor/gsap.min.js',run/'assets/vendor/gsap.min.js')
    (run/'assets/fonts/fonts.css').write_text('\n'.join(css),encoding='utf-8')
    for name in ('SOURCE.md','LICENSE','OFL.txt'):
        if (source/'fonts'/name).exists(): shutil.copyfile(source/'fonts'/name,run/'assets/fonts'/name)
    if (source/'vendor/katex').is_dir():
        require_katex(source/'vendor/katex')
        shutil.copytree(source/'vendor/katex',run/'assets/vendor/katex',dirs_exist_ok=True)

def assemble(m,timeline,theme,run):
    run=Path(run); dest=run/'source/compositions'; dest.mkdir(parents=True,exist_ok=True)
    parts=[]; hosts=[]
    timings={s['id']:s for s in timeline['scenes']}
    for scene in m['scenes']:
        sid=scene['id']; t=timings[sid]; start=t['start_sample']/24000
        frames=t['last_frame']-t['first_frame']; duration=frames/30
        fragment_path=run/'source/scene-fragments'/(sid+'.html')
        fragment=fragment_path.read_text(encoding='utf-8')
        parsed=validate_fragment(fragment,sid)
        for asset in parsed.assets:
            if not (run/asset).is_file(): raise ValueError('missing asset: '+asset)
        motions=json.loads(fragment_path.with_suffix('.motion.json').read_text(encoding='utf-8'))
        segments={s['id']:s for s in timeline['segments'] if s['scene_id']==sid}
        js=['const tl=gsap.timeline({paused:true});']
        initial={}
        for motion in sorted(motions,key=lambda row: segments.get(row.get('segment_id'),{}).get('start_sample',0)):
            target=motion['target']
            if not target.startswith('#') or target[1:] not in parsed.ids: raise ValueError('missing motion target')
            if motion.get('kind') not in ('reveal','move','count','highlight','path'): raise ValueError('unknown motion')
            if motion.get('segment_id') not in segments: raise ValueError('motion segment mismatch')
            seg=segments[motion['segment_id']]
            seconds=motion['duration_s']
            if type(seconds) not in (int,float) or not 0<seconds<=(seg['end_sample']-seg['start_sample'])/24000:
                raise ValueError('motion duration outside speech')
            allowed={'x','y','opacity','scale','rotation','textContent','strokeDashoffset','strokeDasharray','fill','color'}
            if not isinstance(motion['from'],dict) or not isinstance(motion['to'],dict) or not (set(motion['from'])|set(motion['to']))<=allowed:
                raise ValueError('unsupported motion property')
            first=initial.setdefault(target,{})
            for name,value in motion['from'].items():first.setdefault(name,value)
            values=dict(motion['to'],duration=seconds,ease='none',immediateRender=False)
            if motion['kind']=='count': values['snap']={'textContent':1}
            js.append('tl.fromTo('+json.dumps(target)+','+json.dumps(motion['from'])+','+json.dumps(values)+','+str(seg['start_sample']/24000-start)+');')
        if not motions: raise ValueError('scene requires meaningful motion')
        js[1:1]=['gsap.set('+json.dumps(target)+','+json.dumps(values)+');' for target,values in initial.items()]
        js.append('window.__timelines=window.__timelines||{};window.__timelines['+json.dumps(sid)+']=tl;')
        has_math='class="katex' in fragment or '$' in fragment
        if has_math: fragment=render_math_fragment(fragment,run/'assets/vendor/katex')
        script='<script>Promise.resolve().then(()=>document.fonts.ready).then(()=>{'+''.join(js).replace('</','<\\/')+'});</script>'
        body=f'<div id="{sid}-root" class="video-scene" data-composition-id="{sid}" data-width="1920" data-height="1080" data-duration="{duration:.9f}">'+fragment+'</div>'
        page=scene_shell(body+script,scene['template_kind'],theme)
        if has_math:
            page=page.replace('</head>','<link rel="stylesheet" href="assets/vendor/katex/katex.min.css"></head>')
        entry=sid+'.html'; (run/entry).write_text(page,encoding='utf-8')
        css=(run/theme['templates'][scene['template_kind']]['css_path']).read_text(encoding='utf-8')
        css+='\n'+(run/'source/video-layout.css').read_text(encoding='utf-8')
        if has_math: css+='\n'+katex_css(run/'assets/vendor/katex')
        sub='<template><style>'+css+'</style>'+body+script+'</template>'
        (dest/(sid+'.html')).write_text(sub,encoding='utf-8')
        assets={p.relative_to(run).as_posix():file_hash(p) for p in (run/'assets').rglob('*') if p.is_file() and 'voice' not in p.parts} if (run/'assets').exists() else {}
        key=digest({'page':page,'motions':motions,'theme':theme,'assets':assets,'frames':frames})
        parts.append({'id':sid,'entry':entry,'frames':frames,'key':key})
        hosts.append(f'<div class="clip" data-composition-id="{sid}" data-composition-src="source/compositions/{sid}.html" data-start="{t["first_frame"]/30:.9f}" data-duration="{duration:.9f}" data-track-index="1" style="position:absolute;inset:0"></div>')
    audio=[]
    for s in timeline['segments']:
        if s.get('path'):
            audio.append(f'<audio id="audio-{s["id"]}" src="{html.escape(s["path"],quote=True)}" data-start="{s["start_sample"]/24000:.9f}" data-duration="{(s["end_sample"]-s["start_sample"])/24000:.9f}" data-track-index="2"></audio>')
    root=f'<div id="main" data-composition-id="main" data-width="1920" data-height="1080" data-duration="{timeline["total_frames"]/30:.9f}">'+''.join(hosts+audio)+'</div><script>window.__timelines=window.__timelines||{};window.__timelines.main=gsap.timeline({paused:true});</script>'
    (run/'index.html').write_text(scene_shell(root,'note',theme),encoding='utf-8')
    atomic_json(run/'source/parts.json',{'parts':parts})
    return parts
