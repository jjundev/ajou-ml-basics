from pathlib import Path
import re
from .util import digest,file_hash
from .contracts import ReviewError,InputError
from .subtitles import caption_text,split_caption

def content_fingerprint(manifest,layers,coverage):
    def freeze(value):
        if isinstance(value,dict):
            return {k:({'path':v,'sha256':file_hash(v) if Path(v).is_file() else None} if k in ('original_svg','animated_svg','reference_png') else freeze(v)) for k,v in value.items()}
        if isinstance(value,list):return [freeze(v) for v in value]
        return value
    return digest({'manifest':manifest,'layers':freeze(layers),'coverage':{k:v for k,v in coverage.items() if k not in ('status','input_hash')}})

def _validate_page_manifest(manifest,layers,coverage,circuit_review,_hash=None):
    def require(ok,why):
        if not ok: raise ReviewError(why)
    require(manifest.get('schema_version') in (1,2),'manifest schema_version must be 1')
    require(bool(manifest.get('problem_id')) and bool(manifest.get('title','').strip()),'problem ID/title required')
    mapping=layers.get('map'); require(bool(mapping),'PageMap not authored')
    gs={g['id']:g for g in layers['glyphs']}; ss={s['id']:s for s in layers['shapes']}
    order=manifest.get('reveal_order',[])
    require(len(order)==len(gs) and set(order)==gs.keys(),'exact glyph coverage required')
    if any('writing_units' in step for step in mapping['steps']):
        from .writing_units import compile_writing_units
        compile_writing_units(layers)
    steps=mapping['steps']; ids=[s['id'] for s in steps]
    require(len(set(ids))==len(ids) and ids[-1]==mapping['answer_step_id'],'answer must be final step')
    expected=[g for s in steps for g in s['glyph_ids']]
    require(order==expected,'explicit PageMap reading order required; no coordinate sorting')
    glyph_step={g:s['id'] for s in steps for g in s['glyph_ids']}
    shape_step={g:s['id'] for s in steps for g in s['shape_ids']}
    anchors=manifest.get('shape_anchors',{})
    require(set(anchors)==ss.keys(),'exact shape anchors required')
    require(all(g in gs and glyph_step[g]==shape_step[s] for s,g in anchors.items()),'shape anchor must belong to same step')
    segs=manifest.get('segments',[]); require(bool(segs),'narration segments required')
    require(len({s['id'] for s in segs})==len(segs),'duplicate segment ID')
    from .speech_chunks import validate_speech_chunks,MODE
    require(manifest.get('caption_timing') in (None,MODE),'unsupported caption timing mode')
    require(manifest.get('caption_timing')==MODE or not any('chunks' in s for s in segs),'chunks require explicit caption timing mode')
    validate_speech_chunks(segs,required=manifest.get('caption_timing')==MODE)
    writing=[]
    for s in segs:
        require(bool(re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',s['id'])),'segment ID must be safe ASCII')
        require(s.get('kind') in ['problem','reason','write','check','summary'],'invalid segment kind')
        require(bool(s.get('text','').strip()) and bool(s.get('source_refs')),'segment text/source_refs required')
        if 'caption_text' in s:
            require(isinstance(s['caption_text'],str) and bool(s['caption_text'].strip()),'nonempty caption_text required')
        try:split_caption(caption_text(s))
        except InputError as ex:raise InputError('segment '+s['id']+': '+str(ex)) from ex
        if s['kind']=='write':
            require(s.get('step_id') in ids,'unknown writing step'); writing.append(s['step_id'])
        elif s.get('step_id'): require(s['step_id'] in ids,'unknown step')
    require(writing==ids,'one ordered write segment per mapped step; split the PageMap for smaller writing units')
    require(segs[0]['kind']=='problem','begin on original problem PDF')
    keys=manifest.get('cameras',[])
    require(all(type(k['at_frame']) is int and k['at_frame']>=0 and len(k['viewbox'])==4 and k['viewbox'][2]>0 and k['viewbox'][3]>0 for k in keys),'invalid camera key')
    require([k['at_frame'] for k in keys]==sorted(set(k['at_frame'] for k in keys)),'camera keys must be unique and ordered')
    h=_hash or content_fingerprint(manifest,layers,coverage)
    for r in [coverage,circuit_review]: require(r.get('status')=='passed' and r.get('input_hash')==h,'current authored review required')
    require(coverage.get('pdf_md_agree') is True,'PDF/MD disagreement blocks TTS')
    rows=coverage.get('rows',[])
    require([r.get('step_id') for r in rows]==ids,'coverage rows must follow every mapped step')
    require(all(r.get('source_refs') and r.get('pdf_text') and r.get('meaning_review') for r in rows),'source text and meaning evidence required')
    for row,step in zip(rows,steps):
        source_text=''.join(gs[g]['text'] for g in step['glyph_ids'])
        require(re.sub(r'\s+','',row['pdf_text'])==re.sub(r'\s+','',source_text),'coverage pdf_text differs from original glyph order')
    if manifest.get('schema_version')==2:
        from .math_review import validate_math_review
        validate_math_review(circuit_review,ids,h)
    else:
        checks=circuit_review.get('steps',[])
        require([r.get('step_id') for r in checks]==ids,'page review must cover every step')
        require(all(all(r.get(k) for k in ['assumptions','equations','units','evidence']) for r in checks),'assumptions/equations/units/evidence required')

def validate_manifest(manifest,layers,coverage,math_review):
    if layers.get('schema_version')!=2:return _validate_page_manifest(manifest,layers,coverage,math_review)
    from .bundle_layers import flatten_layers
    require=lambda ok,why: None if ok else (_ for _ in ()).throw(ReviewError(why))
    require(manifest.get('schema_version')==2,'bundle manifest schema must be 2')
    require(manifest.get('caption_timing')=='pcm-chunks-v1','new ML speech requires pcm-chunks-v1')
    pages=layers['pages'];problem_pages=[pid for pid in layers['page_order'] if pages[pid].get('role')=='problem']
    intros=[seg.get('page_id') for seg in manifest.get('segments',[]) if seg.get('kind')=='problem']
    require(intros==problem_pages,'problem page coverage must include every source problem page in order')
    step_page={step:step.split('::',1)[0] for step in layers['step_order']}
    for seg in manifest.get('segments',[]):
        require(seg.get('page_id') in pages,'unknown segment page_id')
        require(seg.get('kind')!='problem' or pages[seg['page_id']].get('role')=='problem','problem segment must use problem page role')
        if seg.get('step_id'):require(step_page.get(seg['step_id'])==seg['page_id'],'segment step/page mismatch')
    _validate_page_manifest(manifest,flatten_layers(layers),coverage,math_review,content_fingerprint(manifest,layers,coverage))
