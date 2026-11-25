"""Rebuild a fresh stage from verified published fragments; never publish here."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import replace, fields
from pathlib import Path
from urllib.parse import unquote, urlsplit
from mpe_source import inside, load_source, sha256, existing_path
from mpe_shared import parse
from mpe_types import ExplainError
from mpe_review_policy import carry_reviews

CODE_RE = re.compile(r'<style\b[^>]*>.*?</style>|<script\b(?![^>]*application/json)[^>]*>.*?</script>',re.S|re.I)

def git_blob(path, digest):
    try:
        commits = subprocess.run(['git','log','--format=%H','--',path.name],cwd=path.parent,capture_output=True,check=True).stdout.decode().split()
        for commit in commits:
            p = subprocess.run(['git','show',f'{commit}:./{path.name}'],cwd=path.parent,capture_output=True)
            if p.returncode:
                continue
            # Windows checkouts may have CRLF although the committed blob uses LF.
            for data in (p.stdout, p.stdout.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')):
                if hashlib.sha256(data).hexdigest() == digest:
                    return data
    except (OSError,subprocess.CalledProcessError):
        pass
    return None

def relocated(path, repo):
    path = inside(path,repo)
    if path.is_file():
        return path
    try:
        normalized=inside(existing_path(path),repo)
        if normalized.is_file():
            return normalized
    except (ExplainError,OSError):
        pass
    candidates = []
    for parent in path.parents:
        if re.fullmatch(r'\d{4}(?:-\d{4})?',parent.name):
            candidates = [parent/side/path.relative_to(parent) for side in ('.pack','.assets')]
            break
    found = [inside(p,repo) for p in candidates if p.is_file()]
    return found[0] if len(found) == 1 else path

def equivalent_text(old, current, old_path, new_path, repo, allow_moved_targets=False):
    """Accept CSS/code-only changes; resolve URL relocations to verified actual files."""
    decode = lambda data: CODE_RE.sub('',data.decode('utf-8'))
    a,b = decode(old),decode(current)
    if a == b:
        return True
    pattern = re.compile(r'''\b(src|href)=(['"])(.*?)\2''',re.I)
    old_urls,new_urls = list(pattern.finditer(a)),list(pattern.finditer(b))
    if len(old_urls) != len(new_urls):
        return False
    for left,right in zip(old_urls,new_urls):
        if left.group() == right.group():
            continue
        u,v = urlsplit(left[3]),urlsplit(right[3])
        if (left[1] != right[1] or u.scheme or u.netloc or v.scheme or v.netloc
            or not u.path or not v.path or u.query != v.query or u.fragment != v.fragment):
            return False
        p,q = inside(old_path.parent/unquote(u.path),repo),inside(new_path.parent/unquote(v.path),repo)
        if allow_moved_targets:  # only source inputs, guarded later by historical source_resources hashes
            p,q=relocated(p,repo),relocated(q,repo)
        if not p.is_file() or not q.is_file() or sha256(p) != sha256(q):
            return False
    return pattern.sub('URL',a) == pattern.sub('URL',b)

def same_problems(previous, current, path, repo):
    if len(previous) != len(current):
        return False
    for old,new in zip(previous,current):
        for field in fields(old):
            left,right=getattr(old,field.name),getattr(new,field.name)
            if left == right:
                continue
            if isinstance(left,str) and isinstance(right,str) and field.name.endswith('_html'):
                if equivalent_text(left.encode(),right.encode(),path,path,repo,allow_moved_targets=True):
                    continue
            if field.name == 'figures_html' and len(left)==len(right):
                if all(equivalent_text(a.encode(),b.encode(),path,path,repo,allow_moved_targets=True) for a,b in zip(left,right)):
                    continue
            return False
    return True

def verified_resources(stored, current, repo):
    if not isinstance(stored,dict):
        return False
    mapped={}
    for name,digest in stored.items():
        path=relocated(repo/name,repo)
        if not path.is_file() or sha256(path)!=digest:
            return False
        mapped[path.relative_to(repo).as_posix()]=digest
    return mapped==current

def reference_dependencies(path,repo):
    if path.suffix.lower() not in ('.html','.md','.svg'):
        return []
    text=path.read_text(encoding='utf-8')
    urls=[]
    if path.suffix.lower()=='.md':
        urls=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text)
    else:
        for node in parse(text).find_all(lambda n:n.tag in ('img','image')):
            urls.append(node.attrs.get('src',node.attrs.get('href',node.attrs.get('xlink:href',''))))
    result=[]
    for value in urls:
        url=urlsplit(value)
        if url.scheme or url.netloc or not url.path:
            raise ExplainError('참조 그림의 로컬 hash 확인 필요')
        result.append(inside(existing_path(path.parent/unquote(url.path)),repo))
    return result

def verified_references(references, old_repo, repo):
    if not isinstance(references,list):
        return [],False
    carried=[]
    for ref in references:
        if not isinstance(ref,dict) or not isinstance(ref.get('path'),str) or not isinstance(ref.get('sha256'),str):
            return [],False
        path=Path(old_repo)/ref['path']
        if path.is_relative_to(old_repo):
            path=repo/path.relative_to(old_repo)
        current=relocated(path,repo)
        if not current.is_file():
            print('rerender: 참조 자료 없음: 검토를 다시 하세요: '+path.name)
            return carried,False
        digest=sha256(current)
        if digest != ref['sha256']:
            old=git_blob(path,ref['sha256'])
            if old is None or current.suffix.lower() not in ('.html','.md') or not equivalent_text(old,current.read_bytes(),path,current,repo):
                print('rerender: 참조 자료 변경: 검토를 다시 하세요: '+path.name)
                return carried,False
            print('rerender: 참조 자료는 스타일·스크립트만 바뀌었어요: '+path.name)
        carried.append({**ref,'path':str(current),'sha256':digest})
    recorded={Path(ref['path']).resolve():ref['sha256'] for ref in carried}
    try:
        for ref in carried:
            for dependency in reference_dependencies(Path(ref['path']),repo):
                if recorded.get(dependency.resolve())!=sha256(dependency):
                    print('rerender: 참조 그림 hash 누락/변경: '+dependency.name)
                    return carried,False
    except (ExplainError,OSError,ValueError):
        return carried,False
    return carried,True

def source_resources(pack,repo):
    base=pack.directory
    result={}
    for problem in pack.problems:
        markup=problem.conditions_html+problem.ask_html+problem.original_html+''.join(problem.figures_html)
        for node in parse(markup).find_all(lambda n:n.tag=='img'):
            url=urlsplit(node.attrs.get('src',''))
            if url.scheme or url.netloc or not url.path:
                raise ExplainError('저장소 내부 그림만 허용')
            path=inside(existing_path(base/unquote(url.path)),repo)
            result[path.relative_to(repo).as_posix()]=sha256(path)
    return result

def rerender(repo,target,run):
    from mpe_cli import extract,load_run,load_fragments,build,read_json
    from mpe_render import names,dump
    from mpe_contract import payload_hash
    repo=Path(repo).resolve()
    failed=bool(extract(repo,target,run))
    errors=[]
    try:
        items=load_run(run,errors=errors)
    except (ExplainError,OSError,ValueError,KeyError,TypeError) as exc:
        print(str(exc),file=sys.stderr)
        return 1
    for error in errors:
        print(error,file=sys.stderr)
    failed=failed or bool(errors)
    for item in items:
        try:
            pack,folder=item['pack'],item['folder']
            data=pack.directory/names(pack)[2]
            ids={p.id for p in pack.problems}
            published=inside(data/'fragments',repo)
            if not published.is_dir() or {p.stem for p in published.glob('*.html')} != ids:
                raise ExplainError('발행된 조각 없음/불일치: 정상 저작 절차를 쓰세요')
            manifest=read_json(inside(data/'manifest.json',repo))
            stored=read_json(inside(data/'validation.json',repo))
            intact=True
            for name,digest in manifest.get('files',{}).items():
                source=inside(pack.directory/Path(name),repo)
                intact = intact and source.is_file() and sha256(source)==digest
            if not manifest.get('files') or not intact:
                raise ExplainError('발행된 조각/검산 자료 변경: 정상 저작 절차를 쓰세요')
            for p in pack.problems:
                shutil.copy2(inside(published/f'{p.id}.html',repo),folder/'explanations'/f'{p.id}.html')
            evidence=data/'evidence'
            if evidence.is_dir():
                for child in evidence.rglob('*'):
                    inside(child,repo)
                shutil.copytree(evidence,folder/'evidence',dirs_exist_ok=True)
            fragments=load_fragments(item)
            same=stored.get('input_hash')==payload_hash(pack,fragments)
            # Only HTML adapters can recover a style-only historical input. EC2's digest covers all MD/images.
            if not same and True and pack.profile=='review' and stored.get('input_hash'):
                from review_sources import html_name
                old_path = pack.directory / html_name(pack.path)
                prior_sha = manifest.get('source_sha256', '')
                old=git_blob(old_path,prior_sha)
                if old is not None:
                    with tempfile.TemporaryDirectory() as tmp:
                        path=Path(tmp)/pack.directory.name/html_name(pack.path)
                        path.parent.mkdir();path.write_bytes(old)
                        try:
                            previous=load_source(path,Path(tmp))
                            same=(same_problems(previous.problems,pack.problems,old_path,repo) and payload_hash(replace(pack,sha256=manifest['source_sha256']),fragments)==stored['input_hash'])
                        except (ExplainError,OSError):
                            same=False
            if same and stored.get('input_hash')!=payload_hash(pack,fragments):
                print('rerender: 원본 파일은 바뀌었지만 문항 내용은 같아요')
            refs,valid=verified_references(stored.get('references'),Path(manifest.get('repo',str(repo))),repo)
            same=same and valid and verified_resources(manifest.get('source_resources'),source_resources(pack,repo),repo)
            build(item,fragments)
            fresh=read_json(folder/'review.json')
            # Keep stale references visible when manual re-review is required; publish will reject them.
            if not valid:
                refs=stored.get('references',[])
            review=carry_reviews(stored,fresh,refs,same)
            dump(folder/'review.json',review)
            reused=review['content']['status']=='pass' and review['independent']['status']=='pass'
            print('rerender: '+('content·independent 재사용, source_visual·browser 재검토 필요' if reused else '입력 변경: 네 검토 모두 다시 필요 (입력·근거·검토 기준을 확인하세요)'))
        except (ExplainError,OSError,ValueError,KeyError,TypeError) as exc:
            failed=True
            print(f'{item["folder"].name}: {exc}',file=sys.stderr)
    return int(failed)
