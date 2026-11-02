"""Validate agent-authored selection; never decide what merits a video."""
import re, unicodedata
from pathlib import Path
from .cache import file_hash
from .manifest import require_ready

class SelectionError(ValueError): pass

def filename(title):
    name=unicodedata.normalize('NFC',title)
    name=re.sub(r'[<>:"/\\|?*\x00-\x1f]','',name).strip(' .')
    if not name or name.casefold().endswith('.mp4'):
        raise SelectionError('provide a nonempty title without .mp4')
    if len(name.encode('utf-8'))>240: raise SelectionError('video title is too long')
    if re.fullmatch(r'(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])',name):
        raise SelectionError('reserved video title')
    return name+'.mp4'

def _rows(plan,key,nonempty=False):
    rows=plan.get(key)
    if not isinstance(rows,list) or any(not isinstance(r,dict) for r in rows) or (nonempty and not rows):
        raise SelectionError(key+': expected '+('nonempty ' if nonempty else '')+'object list')
    return rows

def _text(row,key):
    if not isinstance(row.get(key),str) or not row[key].strip():
        raise SelectionError('missing text: '+key)

def _ids(rows,label):
    result={}
    for row in rows:
        ident=row.get('id')
        if not isinstance(ident,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',ident) or ident in result:
            raise SelectionError(label+': duplicate or unsafe ID')
        result[ident]=row
    return result

def _refs(row,key,valid,nonempty=False):
    values=row.get(key)
    if not isinstance(values,list) or any(not isinstance(v,str) for v in values):
        raise SelectionError('invalid references: '+key)
    if (nonempty and not values) or len(values)!=len(set(values)) or any(v not in valid for v in values):
        raise SelectionError('unknown, duplicate or empty references: '+key)
    return values

def require_selection(plan,inputs=None):
    if not isinstance(plan,dict) or plan.get('schema_version')!=1 or plan.get('mode')!='selective':
        raise SelectionError('selection schema_version=1, mode=selective required')
    from .sources import _range
    _text(plan,'range');_range(plan['range'])
    sources=_ids(_rows(plan,'sources',True),'sources')
    topics=_ids(_rows(plan,'topics'),'topics')
    clips=_ids(_rows(plan,'clips'),'clips')
    for source in sources.values():
        for key in ('path','sha256','kind'): _text(source,key)
        if not re.fullmatch(r'[a-f0-9]{64}',source['sha256']): raise SelectionError('invalid source hash')
    if inputs is not None:
        expected={r['id']:r for r in inputs['files']}
        if plan['range']!=inputs['range'] or set(expected)!=set(sources):
            raise SelectionError('selection does not inventory all discovered sources')
        for sid,rec in expected.items():
            if any(sources[sid][k]!=rec[k] for k in ('sha256','kind')) or Path(sources[sid]['path']).resolve()!=Path(rec['path']).resolve():
                raise SelectionError('source changed: '+sid)
            if file_hash(rec['path'])!=rec['sha256']: raise SelectionError('source changed: '+sid)
    reviewed=set()
    for review in _rows(plan,'source_reviews'):
        _text(review,'reason');sid=review.get('source_id')
        if sid not in sources or sid in reviewed or review.get('status')!='reviewed':
            raise SelectionError('invalid or duplicate source review')
        reviewed.add(sid)
    if any(sid not in reviewed for sid,s in sources.items() if s['kind']!='figure'):
        raise SelectionError('all textual sources need a semantic inventory review')
    for topic in topics.values():
        for key in ('claim','locator','kind','reason'): _text(topic,key)
        if topic.get('source_id') not in sources or topic.get('decision') not in ('animate','text','context'):
            raise SelectionError('invalid topic source or decision')
    owners={};context=set();names=set();questions=set()
    for clip in clips.values():
        _text(clip,'title');_text(clip,'learning_question')
        name=filename(clip['title']).casefold()
        question=' '.join(unicodedata.normalize('NFC',clip['learning_question']).casefold().split())
        if name in names or question in questions: raise SelectionError('duplicate title or learning question; merge related clips')
        names.add(name);questions.add(question)
        primary=_refs(clip,'requirement_ids',topics,True)
        prerequisites=_refs(clip,'prerequisite_ids',topics)
        if set(primary)&set(prerequisites): raise SelectionError('primary/prerequisite overlap')
        for rid in primary:
            if topics[rid]['decision']!='animate' or rid in owners:
                raise SelectionError('each animation topic must have exactly one primary owner')
            owners[rid]=clip['id']
        context.update(prerequisites)
        states=clip.get('visual_states')
        if not isinstance(states,list) or len(states)<2 or any(not isinstance(s,str) or not s.strip() for s in states):
            raise SelectionError('clip needs at least two meaningful visual states')
        length=clip.get('target_duration_seconds')
        if type(length) is not int or length<=0: raise SelectionError('positive integer duration required')
        if not 60<=length<=180: _text(clip,'duration_override_reason')
    if set(owners)!={rid for rid,r in topics.items() if r['decision']=='animate'}:
        raise SelectionError('an animation topic is unassigned')
    if not {rid for rid,r in topics.items() if r['decision']=='context'}<=context:
        raise SelectionError('context topic has no consuming clip')
    return plan

def validate_clip_manifest(plan,clip_id,manifest):
    require_selection(plan);require_ready(manifest)
    clips={c['id']:c for c in plan['clips']}
    if clip_id not in clips or manifest['range']!=plan['range']: raise SelectionError('unknown clip or wrong range')
    clip=clips[clip_id];allowed=set(clip['requirement_ids']+clip['prerequisite_ids'])
    inventory={r['id']:r for r in plan['topics']}
    actual={r['id']:r for t in manifest['topics'] for r in t['requirements']}
    if set(actual)!=allowed: raise SelectionError('clip requirements must exactly match selected scope and prerequisites')
    for rid,r in actual.items():
        if not r['required'] or any(r[k]!=inventory[rid][k] for k in ('claim','source_id','locator','kind')):
            raise SelectionError('changed or optionalized selected claim: '+rid)
    sources={s['id']:s for s in plan['sources']}
    for source in manifest['sources']:
        sid=source['id']
        if sid not in sources or source['sha256']!=sources[sid]['sha256']:
            raise SelectionError('manifest source differs from frozen inventory')
