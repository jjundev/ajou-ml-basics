"""Validate recorded calculation evidence, never claim to prove mathematics."""
import json
import math
import re
from pathlib import Path
from .cache import file_hash


def _local_file(run, relative):
    if not isinstance(relative,str) or not relative or Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError('unsafe math evidence path')
    path=run/relative
    if any(p.is_symlink() for p in [path, *path.parents] if p != run and p.is_relative_to(run)):
        raise ValueError('math evidence symlink')
    if not path.resolve().is_relative_to(run.resolve()) or not path.is_file():
        raise ValueError('missing or external math evidence')
    if path.name.startswith('.env'):
        raise ValueError('credential files are not math evidence')
    return path


def _read(run):
    path=_local_file(run,'source/math-evidence.json')
    data=json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(data,dict) or data.get('schema_version')!=1:
        raise ValueError('math evidence schema_version=1 required')
    if not isinstance(data.get('scenes'),list) or not isinstance(data.get('file_hashes'),dict):
        raise ValueError('math evidence scenes and file_hashes required')
    return data


def math_evidence_files(run: Path) -> list[Path]:
    run=Path(run).resolve()
    data=_read(run)
    return [run/'source/math-evidence.json']+[_local_file(run,p) for p in sorted(data['file_hashes'])]


def validate_math_evidence(run: Path, manifest: dict) -> list[str]:
    run=Path(run).resolve()
    try:
        data=_read(run)
        expected={s['id'] for s in manifest['scenes']}
        seen=set(); referenced=set()
        for row in data['scenes']:
            if not isinstance(row,dict): raise ValueError('math scene must be an object')
            sid=row.get('scene_id')
            if not isinstance(sid,str) or sid not in expected or sid in seen:
                raise ValueError('missing, unknown or duplicate math scene')
            seen.add(sid)
            for key in ('formula_refs','conditions','axes','units','dimensions'):
                values=row.get(key)
                if not isinstance(values,list) or not values or any(not isinstance(v,str) or not v.strip() for v in values):
                    raise ValueError('math scene '+sid+': nonempty '+key+' required')
            if row.get('mode')=='qualitative':
                if not isinstance(row.get('reason'),str) or not row['reason'].strip():
                    raise ValueError('qualitative scene needs a reason')
            elif row.get('mode')=='numeric':
                for key in ('calculation_script','calculation_result'):
                    _local_file(run,row.get(key)); referenced.add(row[key])
                states=row.get('states')
                if not isinstance(states,list) or len(states)!=3 or any(not isinstance(s,dict) for s in states):
                    raise ValueError('numeric scene needs start/middle/end states')
                if [s.get('label') for s in states]!=['start','middle','end']:
                    raise ValueError('numeric state labels must be start/middle/end')
                for state in states:
                    _local_file(run,state.get('figure_path'));referenced.add(state['figure_path'])
                    values=state.get('values')
                    if not isinstance(values,dict) or not values or any(not isinstance(k,str) or type(v) not in (int,float) or not math.isfinite(v) for k,v in values.items()):
                        raise ValueError('state values must be finite numbers')
            else:
                raise ValueError('math scene mode must be numeric or qualitative')
        if seen!=expected: raise ValueError('math evidence must cover every scene')
        hashes=data['file_hashes']
        if not referenced<=set(hashes): raise ValueError('math file hashes missing')
        for relative,expected_hash in hashes.items():
            path=_local_file(run,relative)
            if not isinstance(expected_hash,str) or not re.fullmatch(r'[a-f0-9]{64}',expected_hash) or file_hash(path)!=expected_hash:
                raise ValueError('math evidence file changed: '+relative)
        return []
    except (OSError,ValueError,TypeError,KeyError,UnicodeError):
        # Return structural diagnostics only; never include evidence contents.
        return ['missing, invalid or changed math evidence; check source/math-evidence.json and recorded files']
