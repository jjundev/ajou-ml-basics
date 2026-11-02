"""Use the same final-delivery layout for full-review and revoice runs."""
import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from .cache import atomic_json,file_hash,file_lock
from .sources import _range
from .selection import filename
from .verify import DOMAINS,review_fingerprint
from .math_evidence import validate_math_evidence
from .batch import _archive_previous


def new_single_run(repo: Path, selected: str) -> Path:
    _range(selected)
    materials=Path(repo)/'복습영상'/selected/(selected+'_제작자료')
    run=materials/'실행'/(datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8])
    run.mkdir(parents=True)
    return run


def publish_single(run: Path, report: dict) -> Path:
    run=Path(run).resolve()
    if not report.get('complete') or any(report.get(k,{}).get('status')!='passed' for k in DOMAINS):
        raise ValueError('single run is not fully verified')
    m=json.loads((run/'manifest.json').read_text())
    if validate_math_evidence(run,m) or review_fingerprint(run,m)!=report.get('input_hash'):
        raise ValueError('single run changed after verification')
    hashes=report.get('evidence_hashes',{})
    expected={p for k in DOMAINS for p in report[k].get('evidence',[])}
    if not expected or set(hashes)!=expected:
        raise ValueError('single run review evidence missing')
    for relative,h in hashes.items():
        path=(run/relative).resolve()
        if not path.is_relative_to(run) or not path.is_file() or file_hash(path)!=h:
            raise ValueError('single run review evidence changed')
    materials=run.parents[1];date=materials.parent
    if materials.name!=m['range']+'_제작자료' or run.parent.name!='실행':
        raise ValueError('single run must be inside the managed production directory')
    title=m.get('title') or (m['scenes'][0]['visual'] if len(m['scenes'])==1 else '머신러닝기초 — '+m['scenes'][0]['visual']+'부터 전체 복습')
    name=filename(title);final=date/name;source=run/'review.mp4';h=file_hash(source)
    receipt=run/'work/publication.json'
    with file_lock(run/'work/publish.lock'):
        if receipt.exists():
            current=json.loads((materials/'latest.json').read_text())
            if current.get('run')!=run.relative_to(materials).as_posix() or not final.is_file() or file_hash(final)!=h:
                raise ValueError('single run is archived or published output changed')
            return final
        provenance_path=run/'source/from-run.json'
        revoice=json.loads(provenance_path.read_text()) if provenance_path.exists() else None
        prior=json.loads((materials/'latest.json').read_text()) if (materials/'latest.json').exists() else {}
        siblings=[]
        if revoice:
            replacement=revoice.get('replace_filename')
            if replacement and replacement!='review.mp4' and replacement!=name:
                raise ValueError('revoice title must preserve the original filename')
            if final.exists() and not (run/'work/archive.json').exists():
                if file_hash(final)!=revoice.get('source_video_sha256'):
                    raise ValueError('revoice source is no longer the current video')
            for rec in prior.get('videos',[]):
                if rec['filename']==name:continue
                other=date/rec['filename']
                if not other.is_file() or file_hash(other)!=rec['sha256']:
                    raise ValueError('sibling video changed; preserve current output')
                siblings.append(rec)
        export=run/'work/export.mp4';shutil.copyfile(source,export)
        if file_hash(export)!=h:raise ValueError('single export hash mismatch')
        _archive_previous(date,materials,run,only_filenames={name} if revoice else None)
        os.replace(export,final)
        alias=run/'work/review-link';alias.unlink(missing_ok=True)
        alias.symlink_to(os.path.relpath(final,source.parent))
        os.replace(alias,source)
        if review_fingerprint(run,m)!=report['input_hash']:
            raise ValueError('single publication fingerprint changed')
        publication={'schema_version':1,'range':m['range'],'run':run.relative_to(materials).as_posix(),
            'videos':siblings+[{'filename':name,'sha256':h,'run':run.relative_to(materials).as_posix()}],'sha256':h,'status':'complete'}
        atomic_json(materials/'latest.json',publication);atomic_json(receipt,publication)
        return final
