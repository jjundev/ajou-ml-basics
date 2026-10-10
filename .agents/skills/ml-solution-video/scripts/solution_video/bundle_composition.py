"""Compose source pages through isolated, deterministic page renderers."""
from pathlib import Path
import copy,json,html,re,shutil,xml.etree.ElementTree as ET
from .util import write,read,S,digest
from .bundle_layers import flatten_layers
from .contracts import InputError

def page_view(layers,page_id):
 p=copy.deepcopy(layers['pages'][page_id]);flat=flatten_layers(layers)
 p['glyphs']=[g for g in flat['glyphs'] if g['page_id']==page_id];p['shapes']=[s for s in flat['shapes'] if s['page_id']==page_id]
 p['map']['steps']=[s for s in flat['map']['steps'] if s['page_id']==page_id];p['map']['answer_step_id']=p['map']['steps'][-1]['id']
 # Rewrite reveal attributes only; PDF geometry and paths stay untouched.
 svg=Path(p['animated_svg']).read_text()
 for item in layers['pages'][page_id]['glyphs']+layers['pages'][page_id]['shapes']:svg=svg.replace('data-reveal="'+item['id']+'"','data-reveal="'+page_id+'::'+item['id']+'"')
 return p,svg

def timeline_view(t,page_id):
 out=copy.deepcopy(t)
 for field in ('segments','events','writing_spans','writing_unit_spans'):
  out[field]=[r for r in t.get(field,[]) if r.get('page_id')==page_id]
 out['cameras']=[]
 if 'teaching' in out:
  allowed={s['id'] for s in out['segments']};out['teaching']['cues']=[c for c in out['teaching']['cues'] if c['segment_id'] in allowed];out['teaching']['spans']=[s for s in out['teaching']['spans'] if s.get('page_id')==page_id]
 return out

def assemble_bundle(bundle,layers,manifest,timeline,run,runtime):
 from .composition import _assemble_page
 import fitz
 run=Path(run).resolve();dest=run/'composition';dest.mkdir(parents=True,exist_ok=True);frames=[];views={};page_data={}
 for pid in layers['page_order']:
  page=layers['pages'][pid];folder=dest/'pages'/pid;folder.mkdir(parents=True,exist_ok=True)
  if page.get('role')=='problem':
   svg=Path(page['original_svg']).read_text();(folder/'index.html').write_text('<html><body style="margin:0;background:white;overflow:hidden">'+svg.replace('<svg ','<svg style="width:1920px;height:1080px" ',1)+'</body></html>')
  else:
   p,svg=page_view(layers,pid);(folder/'animated.svg').write_text(svg);p['animated_svg']=str(folder/'animated.svg');t=timeline_view(timeline,pid)
   m=copy.deepcopy(manifest);m['segments']=t['segments'];m['cameras']=[]
   # Core renderer works in page coordinates and global frames.
   childrun=folder/'render';childrun.mkdir(parents=True,exist_ok=True)
   if timeline.get('writing'):write(childrun/'source/writing.json',timeline['writing'])
   if (run/'source/focus.json').is_file():
    from .annotations import load_teaching
    plan=load_teaching(run,manifest,layers)
    if plan:
     regions=[r for r in plan['regions'] if r['page_id']==pid];ids={r['id'] for r in regions};cues=[c for c in plan['cues'] if c['target'] in ids];items=[i for i in plan['items'] if i['region_id'] in ids]
     # Page sidecars are validated against original page hash, with v2 visibility policy retained.
     write(childrun/'source/focus.json',dict(schema_version=1,source_sha256=p['metadata']['source_sha256'],regions=regions,cues=cues));write(childrun/'source/annotations.json',dict(schema_version=1,source_sha256=p['metadata']['source_sha256'],items=items));p['ml_focus_policy']=True
     from .annotations import load_teaching as lt
     from .teaching import teaching_timing_settings
     localplan=lt(childrun,m,p)
     if t.get('teaching'):t['teaching']['timing_hash']=digest(teaching_timing_settings(localplan))
   ref=next(x for x in bundle['answer_pages'] if x['id']==pid);path=Path(ref['snapshot']);path=path if path.is_absolute() else run/path
   parts=_assemble_page(dict(problem=dict(ref,snapshot=str(path))),p,m,t,childrun,runtime)
   write(childrun/'layers/layers.json',p);write(childrun/'source/manifest.json',m);write(childrun/'source/timeline.json',t)
   write(childrun/'source/audio.json',read(run/'source/audio.json') if (run/'source/audio.json').is_file() else dict(voices=[]))
   src='pages/'+pid+'/render/'+parts[0]['entry'];views[pid]=dict(entry=src,layers=str(childrun/'layers/layers.json'),timeline=str(childrun/'source/timeline.json'),run=str(childrun))
  if page.get('role')=='problem':
   from .composition import _prefix
   svg=_prefix(Path(page['original_svg']).read_text(),pid+'-')
   height=__import__('solution_video.page_layout',fromlist=['page_layout']).page_layout(page['metadata']['width_pt'],page['metadata']['height_pt'])['height']
   frames.append('<div class="bundle-page" data-page-id="'+pid+'"><div data-local-name="pdf-viewport"><div data-local-name="problem-page">'+svg.replace('<svg ','<svg style="display:block;width:100%;height:'+str(height)+'px" ',1)+'</div></div><div data-local-name="caption-strip"></div></div>')
  else:
   core=(childrun/'composition/index.html').read_text();body=re.search(r'<body>(.*?)<script',core,re.S)[1]
   prefix=pid+'-'
   from .composition import _prefix
   # Mark local DOM identities before prefixing every SVG definition/reference.
   body=re.sub(r'\bid="([^"]+)"',lambda match:'data-local-name="'+match[1]+'" id="'+match[1]+'"',body)
   body=_prefix(body,prefix);body=body.replace('data-composition-id="solution"','').replace('data-duration=', 'data-page-duration=')
   frames.append('<div class="bundle-page" data-page-id="'+pid+'">'+body+'</div>')
   config=dict(timeline=read(childrun/'composition/timeline.json'),layout=__import__('solution_video.page_layout',fromlist=['page_layout']).page_layout(p['metadata']['width_pt'],p['metadata']['height_pt']),glyphs={g['id']:copy.deepcopy(g) for g in p['glyphs']+(p['shapes'] if t.get('writing_unit_spans') else [])},pencilMeta=__import__('solution_video.writing',fromlist=['load_pencil_asset']).load_pencil_asset(S/'assets/pencil') if t.get('writing',{}).get('mode')=='pencil' or (childrun/'composition/annotations/compiled.json').is_file() else None,annotations=read(childrun/'composition/annotations/compiled.json') if (childrun/'composition/annotations/compiled.json').is_file() else None)
   for g in config['glyphs'].values():g['svg_ids']=[prefix+i for i in g['svg_ids']]
   if config['annotations']:
    for item in config['annotations']['items']:
     if item.get('path_id'):item['path_id']=prefix+item['path_id']
     for u in item.get('units',[]):u['svg_ids']=[prefix+i for i in u.get('svg_ids',[])]
   page_data[pid]=config
 duration=timeline['total_frames']/30;encode=lambda value:json.dumps(value,ensure_ascii=False).replace('</','<\\/')
 runtime=Path(runtime);runtime=runtime/'gsap.min.js' if runtime.is_dir() else runtime;shutil.copyfile(runtime,dest/'gsap.min.js')
 for asset in ('camera.js','writing.js','pencil.js','annotations.js','bundle-player.js'):shutil.copyfile(S/'assets'/asset,dest/asset)
 shutil.copyfile(S/'assets/pencil/pencil-yellow-v1.png',dest/'pencil-yellow-v1.png')
 css=(S/'assets/layout.css').read_text();
 for name in ('pdf-viewport','problem-page','answer-page','cursor','caption-strip','pencil'):css=css.replace('#'+name,'[data-local-name="'+name+'"]')
 css+='\n.bundle-page{position:absolute;inset:0;width:100%;height:100%;visibility:hidden}\n'
 (dest/'layout.css').write_text(css)
 (dest/'index.html').write_text('<!doctype html><html><head><meta charset="utf-8"><script src="gsap.min.js"></script><link rel="stylesheet" href="layout.css"></head><body><div id="solution" data-composition-id="solution" data-width="1920" data-height="1080" data-duration="'+str(duration)+'">'+''.join(frames)+'</div><script src="camera.js"></script><script src="writing.js"></script><script src="pencil.js"></script><script src="annotations.js"></script><script>window.solutionTimeline='+encode(timeline)+';window.solutionPages='+encode(page_data)+';</script><script>'+(dest/'bundle-player.js').read_text()+'</script></body></html>')

 write(dest/'bundle-views.json',views);write(dest/'timeline.json',timeline);write(dest/'hyperframes.json',dict(width=1920,height=1080,fps=30));parts=[dict(entry='composition/index.html',first_frame=0,last_frame=timeline['total_frames'],key='solution')];write(run/'source/parts.json',parts);return parts
