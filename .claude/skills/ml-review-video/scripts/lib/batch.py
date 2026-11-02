from .render_options import default_render_options
"""Prepare independent clip runs and publish only a fully verified selection."""
from pathlib import Path
from datetime import datetime
import copy, json, os, shutil, uuid
from .cache import atomic_json, digest, file_hash, file_lock
from .sources import discover
from .selection import require_selection, validate_clip_manifest, filename, SelectionError
from .state import RunStore, stage_fingerprint
from .verify import review_fingerprint, DOMAINS

def read(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def _snapshot(inputs,root):
    result=copy.deepcopy(inputs)
    for rec in result['files']:
        source=Path(rec['path']);target=root/'source/inputs'/(rec['id']+source.suffix)
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        if file_hash(target)!=rec['sha256']: raise SelectionError('source changed while snapshotting: '+rec['id'])
        rec['snapshot']=target.relative_to(root).as_posix()
    atomic_json(root/'source/inputs.json',result)
    return result

def prepare_set(repo,selector,plan,config,review=False):
    inputs=discover(repo,selector);require_selection(plan,inputs)
    # Reject credentials supplied as configuration values. The CLI additionally
    # checks config keys; an explicitly supplied env_file path remains allowed.
    if any('key' in k.lower() or 'token' in k.lower() and k!='max_output_tokens' for k in config):
        raise SelectionError('never put credentials in batch config')
    date=Path(repo).resolve()/'복습영상'/inputs['range']
    materials=date/(inputs['range']+'_제작자료')
    batch=materials/'실행'/(datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8])
    batch.mkdir(parents=True)
    frozen=copy.deepcopy(plan);atomic_json(batch/'selection.json',frozen)
    _snapshot(inputs,batch)
    clips=[]
    for clip in frozen['clips']:
        run=batch/'videos'/clip['id'];run.mkdir(parents=True)
        _snapshot(inputs,run)
        atomic_json(run/'source/selection.json',frozen)
        atomic_json(run/'source/clip-scope.json',{'clip_id':clip['id'],'selection_hash':digest(frozen)})
        atomic_json(run/'config.json',config)
        atomic_json(run/'source/render-options.json',default_render_options())
        state={'schema_version':1,'range':inputs['range'],'review':review,'source_run':None,'stages':{}}
        state['stages']['inputs']={'status':'passed','input_hash':stage_fingerprint(run,'inputs'),
            'output_hashes':{'source/inputs.json':file_hash(run/'source/inputs.json')}}
        RunStore(run).save(state)
        clips.append({'id':clip['id'],'title':clip['title'],'filename':filename(clip['title']),
                      'run':run.relative_to(batch).as_posix()})
    atomic_json(batch/'batch.json',{'schema_version':1,'range':inputs['range'],
        'selection_hash':digest(frozen),'clips':clips,'review':review,'status':'prepared'})
    return batch

def _load(batch):
    batch=Path(batch).resolve();data=read(batch/'batch.json');plan=read(batch/'selection.json')
    require_selection(plan)
    if data.get('schema_version')!=1 or data.get('range')!=plan['range'] or data.get('selection_hash')!=digest(plan):
        raise SelectionError('batch plan changed; prepare a new set instead of silently changing scope')
    if batch.parent.name!='실행' or batch.parents[1].name!=data['range']+'_제작자료' or batch.parents[2].name!=data['range']:
        raise SelectionError('unexpected batch location')
    clips=data.get('clips')
    if not isinstance(clips,list) or len(clips)!=len(plan['clips']): raise SelectionError('batch clip inventory mismatch')
    for rec,clip in zip(clips,plan['clips']):
        if any(rec.get(k)!=v for k,v in {'id':clip['id'],'title':clip['title'],
                                      'filename':filename(clip['title']),'run':'videos/'+clip['id']}.items()):
            raise SelectionError('batch clip mapping changed')
        run=(batch/rec['run']).resolve()
        if not run.is_relative_to(batch) or not run.is_dir(): raise SelectionError('unsafe clip run')
    # Snapshot hashes, rather than stale absolute source paths, make a batch
    # portable and prove which exact version of the notes was selected.
    inputs=read(batch/'source/inputs.json')
    expected={s['id']:s for s in plan['sources']}
    records=inputs['files']
    if inputs.get('range')!=plan['range'] or len(records)!=len(expected) or {r['id'] for r in records}!=set(expected):
        raise SelectionError('batch snapshot inventory differs from selection')
    for rec in records:
        if any(rec[k]!=expected[rec['id']][k] for k in ('sha256','kind')):
            raise SelectionError('batch snapshot metadata changed')
        path=(batch/rec['snapshot']).resolve()
        if not path.is_relative_to(batch/'source/inputs') or file_hash(path)!=rec['sha256']:
            raise SelectionError('batch source snapshot changed')
    return batch,data,plan

def check_scope(run,manifest):
    path=Path(run)/'source/clip-scope.json'
    if not path.exists(): return  # Legacy/full single-video pipeline.
    scope=read(path);plan=read(Path(run)/'source/selection.json')
    if scope.get('selection_hash')!=digest(plan): raise SelectionError('clip selection changed')
    validate_clip_manifest(plan,scope.get('clip_id'),manifest)
    root=Path(run).resolve()
    for source in manifest['sources']:
        path=(root/source['path']).resolve()
        if not path.is_relative_to(root) or file_hash(path)!=source['sha256']:
            raise SelectionError('manifest source snapshot changed: '+source['id'])

def budget_path(run):
    run=Path(run).resolve()
    if (run/'source/clip-scope.json').exists():
        batch=run.parents[1];_load(batch)
        return batch/'cost-ledger.json'
    return run/'cost-ledger.json'

def _verified(run,plan,clip_id):
    from .math_evidence import validate_math_evidence
    try:
        m=read(run/'manifest.json');validate_clip_manifest(plan,clip_id,m);check_scope(run,m)
        if validate_math_evidence(run,m): return False
        scope=read(run/'source/clip-scope.json')
        if scope!={'clip_id':clip_id,'selection_hash':digest(plan)} or digest(read(run/'source/selection.json'))!=digest(plan): return False
        report=read(run/'verification/report.json');key=review_fingerprint(run,m)
        if not report.get('complete') or report.get('input_hash')!=key or not (run/'review.mp4').is_file():return False
        expected=set()
        for domain in DOMAINS:
            item=report.get(domain,{})
            if item.get('status')!='passed' or item.get('input_hash')!=key or not item.get('evidence'):return False
            expected.update(item['evidence'])
        hashes=report.get('evidence_hashes',{})
        if set(hashes)!=expected:return False
        for relative,h in hashes.items():
            p=(run/relative).resolve()
            if not p.is_relative_to(run.resolve()) or file_hash(p)!=h:return False
        return True
    except (OSError,ValueError,KeyError,TypeError):return False

def resume_set(batch):
    batch,data,plan=_load(batch);clips=[]
    for rec in data['clips']:
        run=batch/rec['run']
        if _verified(run,plan,rec['id']): status='verified';next_stage=None
        else:
            with RunStore(run).lock():next_stage=RunStore(run).recover()
            status='pending'
            if next_stage is None:next_stage='verify'
        clips.append(dict(rec,status=status,next=next_stage))
    return {'batch':str(batch),'status':'verified' if all(c['status']=='verified' for c in clips) else 'pending',
            'clips':clips,'selected_count':len(clips)}

def _archive_previous(date,materials,batch,only_filenames=None):
    journal=batch/'work/archive.json'
    if journal.exists():record=read(journal)
    else:
        old=[p for p in date.iterdir() if p!=materials and not p.name.startswith('.')
             and (only_filenames is None or p.name in only_filenames)]
        archive=materials/'이전버전'/batch.name
        moves=[]
        for p in old:
            target=archive/p.name
            if target.exists() or target.is_symlink():raise SelectionError('archive collision; previous files preserved')
            moves.append({'source':p.relative_to(date).as_posix(),'target':target.relative_to(date).as_posix()})
        links=[]
        for p in date.rglob('*'):
            if not p.is_symlink() or p.name!='review.mp4' or p.is_relative_to(batch):continue
            target=p.resolve()
            links.append({'link':p.relative_to(date).as_posix(),
                          'target':target.relative_to(date).as_posix() if target.is_relative_to(date) else str(target)})
        record={'moves':moves,'links':links,'done':False};atomic_json(journal,record)
    if record['done']:return
    moves=[]
    for rec in record['moves']:
        source=date/rec['source'];target=date/rec['target']
        if not source.resolve().is_relative_to(date) or not target.resolve().is_relative_to(date):
            raise SelectionError('unsafe archive journal')
        moves.append((source,target))
        if target.exists() or target.is_symlink():continue  # Already moved before an interruption.
        target.parent.mkdir(parents=True,exist_ok=True);source.rename(target)
    def relocated(path):
        for source,target in moves:
            if path==source:return target
            if path.is_relative_to(source):return target/path.relative_to(source)
        return path
    for rec in record['links']:
        original=date/rec['link'];target=date/rec['target']
        link=relocated(original);target=relocated(target)
        if link.is_symlink() and target.exists():
            link.unlink();link.symlink_to(os.path.relpath(target,link.parent))
    record['done']=True;atomic_json(journal,record)

def publish_set(batch):
    batch=Path(batch).resolve()
    with file_lock(batch/'work/publish.lock'):
        batch,data,plan=_load(batch);date=batch.parents[2];materials=batch.parents[1]
        if any(not _verified(batch/r['run'],plan,r['id']) for r in data['clips']):
            raise SelectionError('all selected clips must pass current verification before set publication')
        if data.get('status')=='published':
            published=read(materials/'latest.json')
            if published.get('batch')!=batch.relative_to(materials).as_posix():
                raise SelectionError('this set is archived; prepare a new set to replace the current output')
            for rec in published['videos']:
                if file_hash(date/rec['filename'])!=rec['sha256']:raise SelectionError('published video changed')
            return {'status':'complete','batch':str(batch),'videos':published['videos']}
        exports=batch/'work/export';exports.mkdir(parents=True,exist_ok=True);videos=[]
        for rec in data['clips']:
            source=batch/rec['run']/'review.mp4';staged=exports/rec['filename'];shutil.copyfile(source,staged)
            h=file_hash(source)
            if file_hash(staged)!=h:raise SelectionError('export hash mismatch')
            videos.append(dict(rec,sha256=h))
        _archive_previous(date,materials,batch)
        for rec in videos:
            dest=date/rec['filename'];os.replace(exports/rec['filename'],dest)
        # Keep the validated originals until *all* top-level exports exist.
        # A partial export can then be retried without dangling source aliases.
        for rec in videos:
            dest=date/rec['filename']
            alias=batch/rec['run']/'review.mp4'
            alias.unlink();alias.symlink_to(os.path.relpath(dest,alias.parent))
            if not _verified(alias.parent,plan,rec['id']):raise SelectionError('post-publication verification fingerprint changed')
        publication={'schema_version':1,'range':data['range'],'batch':batch.relative_to(materials).as_posix(),
                     'selection_hash':data['selection_hash'],'videos':videos,'status':'complete'}
        atomic_json(materials/'latest.json',publication)
        for rec in videos:
            run=batch/rec['run'];store=RunStore(run)
            with store.lock():
                state=store.load()
                state['stages']['publish']={'status':'passed','input_hash':stage_fingerprint(run,'publish'),
                    'output_hashes':{'review.mp4':file_hash(run/'review.mp4')}}
                store.save(state)
        data['status']='published';atomic_json(batch/'batch.json',data)
        return {'status':'complete','batch':str(batch),'videos':videos}
