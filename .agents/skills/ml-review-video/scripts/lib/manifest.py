"""Structural coverage gates; semantic review is an explicit agent responsibility."""
import re

class ManifestError(ValueError): pass

def validate_manifest(m):
    errors=[]
    if not isinstance(m,dict): return ['manifest:object-required']
    if m.get('schema_version')!=1: errors.append('schema_version:1-required')
    if not isinstance(m.get('range'),str) or not re.fullmatch(r'\d{4}(?:-\d{4})?',m.get('range','')):
        errors.append('range:invalid')
    arrays=('sources','topics','scenes','segments','questions','notices','conflicts','coverage_reviews','exclusions')
    if any(not isinstance(m.get(k),list) or any(not isinstance(x,dict) for x in m[k]) for k in arrays):
        return errors+['manifest:invalid-arrays']
    def text(row,key,label):
        if not isinstance(row.get(key),str) or not row[key].strip(): errors.append(label+':'+key)
    def ids(rows,label):
        result={}
        for row in rows:
            ident=row.get('id')
            if not isinstance(ident,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',ident):
                errors.append(label+':invalid-id'); continue
            if ident in result: errors.append(label+':duplicate:'+ident)
            result[ident]=row
        return result
    def refs(row,key,valid,label,nonempty=False):
        values=row.get(key)
        if not isinstance(values,list) or any(not isinstance(x,str) for x in values):
            errors.append(label+':'+key); return []
        if nonempty and not values: errors.append(label+':empty-'+key)
        if len(values)!=len(set(values)) or any(x not in valid for x in values):
            errors.append(label+':invalid-'+key)
        return values
    sources=ids(m['sources'],'sources'); topics=ids(m['topics'],'topics')
    scenes=ids(m['scenes'],'scenes'); segments=ids(m['segments'],'segments')
    questions=ids(m['questions'],'questions')
    for k,v in sources.items():
        for field in ('kind','path','sha256'): text(v,field,k)
    for key,rows in (('sources',sources),('topics',topics),('scenes',scenes),('segments',segments)):
        if not rows: errors.append(key+':empty')
    requirements=[]
    for ident,t in topics.items():
        reqs=t.get('requirements')
        if not isinstance(reqs,list) or not reqs or any(not isinstance(x,dict) for x in reqs):
            errors.append(ident+':requirements'); continue
        requirements.extend(reqs)
    reqs=ids(requirements,'requirements')
    for ident,r in reqs.items():
        for field in ('claim','locator','kind'): text(r,field,ident)
        if r.get('source_id') not in sources: errors.append(ident+':source')
        if type(r.get('required')) is not bool: errors.append(ident+':required-bool')
    linked=set(); by_requirement={}
    for ident,s in scenes.items():
        refs(s,'topic_ids',topics,ident,True); refs(s,'question_ids',questions,ident)
        for field in ('visual','motion'): text(s,field,ident)
        if s.get('template_kind') not in ('note','review'): errors.append(ident+':template_kind')
    for ident,s in segments.items():
        if s.get('scene_id') not in scenes: errors.append(ident+':scene')
        for field in ('text','caption'): text(s,field,ident)
        if 'subtitle_text' in s:
            text(s,'subtitle_text',ident)
            if isinstance(s['subtitle_text'],str) and any(c in s['subtitle_text'] for c in ('\n','\r','\x00')):
                errors.append(ident+':subtitle_text must be a single line of full narration')
        refs(s,'source_ids',sources,ident,True)
        for rid in refs(s,'requirement_ids',reqs,ident):
            linked.add(rid); by_requirement.setdefault(rid,set()).add(ident)
    for sid in scenes:
        if not any(s.get('scene_id')==sid for s in segments.values()): errors.append(sid+':empty')
    reviewed=set()
    for r in m['coverage_reviews']:
        rid=r.get('requirement_id'); segs=r.get('segment_ids')
        if (rid in reqs and r.get('status')=='passed' and isinstance(r.get('reason'),str)
            and r['reason'].strip() and isinstance(segs,list) and segs
            and all(isinstance(s,str) and s in by_requirement.get(rid,set()) for s in segs)):
            reviewed.add(rid)
    for rid,r in reqs.items():
        if r.get('required'):
            if rid not in linked: errors.append('uncovered:'+rid)
            if rid not in reviewed: errors.append('unreviewed:'+rid)
    for ident,q in questions.items():
        refs(q,'requirement_ids',reqs,ident,True); text(q,'locator',ident)
        if q.get('source_id') not in sources: errors.append(ident+':source')
        if not any(ident in s.get('question_ids',[]) for s in scenes.values()): errors.append(ident+':scene')
    for n in m['notices']:
        for key in ('text','period_label'): text(n,key,'notice')
        if n.get('source_id') not in sources: errors.append('notice:source')
    for c in m['conflicts']:
        if c.get('status')!='resolved' or not c.get('resolution') or not c.get('evidence'):
            errors.append('conflict:'+str(c.get('id','unknown')))
    for e in m['exclusions']:
        for key in ('locator','reason'): text(e,key,'exclusion')
        if e.get('source_id') not in sources or e.get('requirement_id') in reqs:
            errors.append('exclusion:learning-content')
    return errors

def require_ready(m):
    errors=validate_manifest(m)
    if errors: raise ManifestError('; '.join(errors))

def coverage_rows(m):
    require_ready(m)
    return [{'requirement_id':r['id'],'claim':r['claim'],
             'segment_ids':[s['id'] for s in m['segments'] if r['id'] in s['requirement_ids']]}
            for t in m['topics'] for r in t['requirements']]
