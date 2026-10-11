"""Assemble explanation notes with local resources and auditable preservation."""
import hashlib
import html
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit, quote
from mpe_contract import validate_fragment, payload_hash, markup_errors
from mpe_shared import Node, parse, inner, outer, compact, Ctx, convert, check_md
from mpe_source import sha256, inside, existing_path
from mpe_types import ExplainError, Artifacts

ASSETS = Path(__file__).resolve().parents[1] / 'assets'

def names(pack):
    stem = f'과제{pack.range}_문제설명_{pack.slug}' if pack.profile == 'homework' else f'문제설명_{pack.range}_{pack.slug}'
    range_ = f'hw{pack.range}' if pack.profile == 'homework' else pack.range
    return stem, f'figures_문제설명_{range_}_{pack.slug}', f'자료_문제설명_{range_}_{pack.slug}'

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def artifact_hashes(artifacts):
    root = artifacts.html.parent
    return {p.relative_to(root).as_posix(): sha256(p) for p in artifacts.files}

def resources(markup, problem, pack, repo, stage, fig_name, destination):
    root = parse(markup)
    nodes = list(root.find_all(lambda n: True))
    errors = markup_errors(root, allow_summary=True)
    if errors:
        raise ExplainError(f'{problem.id}: 원문/설명 마크업 오류: ' + ' / '.join(errors))
    # Scope SVG identifiers per occurrence (original English and reading may repeat media).
    for index, svg in enumerate(root.find_all(lambda n: n.tag == 'svg')):
        all_svg = [svg, *svg.find_all(lambda n: True)]
        ids = [n.attrs['id'] for n in all_svg if 'id' in n.attrs]
        if len(ids) != len(set(ids)):
            raise ExplainError(f'{problem.id}: 중복 SVG ID')
        suffix = '' if index == 0 else f'-svg{index+1}'
        mapping = {id_: f'{problem.id}{suffix}-{id_}' for id_ in ids}
        for node in all_svg:
            for key, value in list(node.attrs.items()):
                if key == 'id':
                    node.attrs[key] = mapping[value]
                elif key in ('href', 'xlink:href') and value.startswith('#') and value[1:] in mapping:
                    node.attrs[key] = '#' + mapping[value[1:]]
                else:
                    node.attrs[key] = re.sub(r'url\(#([^)]*)\)', lambda m: f'url(#{mapping.get(m[1],m[1])})', value)
    for node in nodes:
        if node.tag == 'img':
            url = urlsplit(node.attrs.get('src', ''))
            if url.scheme or url.netloc or not url.path:
                raise ExplainError(f'{problem.id}: 저장소 내부 그림만 허용')
            source = inside(existing_path(pack.path.parent / unquote(url.path)), repo)
            if not source.is_file():
                raise ExplainError(f'{problem.id}: 그림 없음: {source}')
            target = stage / fig_name / (sha256(source)[:16] + '-' + source.name)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            node.attrs['src'] = target.relative_to(stage).as_posix()
            node.attrs.pop('srcset', None)
        if node.tag == 'a':
            href = node.attrs.get('href', '')
            url = urlsplit(href)
            if url.scheme or url.netloc:
                raise ExplainError(f'{problem.id}: 개념 링크는 실제 저장소 자료만 허용')
            if not url.path:
                continue
            target = inside(existing_path(pack.path.parent / unquote(url.path)), repo)
            if not target.is_file():
                raise ExplainError(f'{problem.id}: 링크 파일 없음')
            if url.fragment:
                anchors = {n.attrs.get('id') for n in parse(target.read_text(encoding='utf-8')).find_all(lambda n: True)}
                if unquote(url.fragment) not in anchors:
                    raise ExplainError(f'{problem.id}: 링크 앵커 없음: {href}')
            # These links must remain usable after publication; stage checks resolve against destination.
            node.attrs['href'] = quote(Path(os.path.relpath(target, destination)).as_posix(), safe='/') + (f'#{url.fragment}' if url.fragment else '')
    return inner(root)

def build_explanation(pack, fragments, stage: Path, repo: Path) -> Artifacts:
    stage = Path(stage).resolve()
    if stage.exists() and any(stage.iterdir()):
        raise ExplainError('stage는 비어 있어야 해요: ' + str(stage))
    if set(fragments) != {p.id for p in pack.problems}:
        raise ExplainError('문항별 설명 조각 집합 불일치')
    errors = [e for p in pack.problems for e in validate_fragment(p, fragments[p.id])]
    if errors:
        raise ExplainError(' / '.join(errors))
    stage.mkdir(parents=True, exist_ok=True)
    stem, fig_name, data_name = names(pack)
    html_path, md_path = stage / f'{stem}.html', stage / f'{stem}.md'
    data_dir = stage / data_name
    data_dir.mkdir()
    (stage / fig_name).mkdir()
    shutil.copytree(ASSETS / 'vendor', data_dir / 'vendor')
    shutil.copy2(ASSETS / 'template-provenance.json', data_dir / 'template-provenance.json')
    articles = []
    toc = []
    for p in pack.problems:
        reading = (f'<div class="layer formal" data-source-problem="{p.id}"><h4>주어진 조건</h4>'
                   + '<div data-source-field="conditions">' + p.conditions_html + '</div><h4>구할 것</h4>'
                   + '<div data-source-field="ask">' + p.ask_html + '</div>' + ''.join(p.figures_html) + '</div>')
        if pack.profile == 'homework':
            reading += '<div class="layer formal" data-original-problem="' + p.id + '"><h4>과제 원문</h4>' + p.original_html + '</div>'
        # Validate each block separately: a summary remains a direct fragment child.
        reading = resources(reading, p, pack, repo, stage, fig_name, pack.path.parent)
        explanation = resources(fragments[p.id], p, pack, repo, stage, fig_name, pack.path.parent)
        articles.append(f'<article class="topic" id="{p.id}"><h3>{html.escape(p.title)}</h3>'
                        + f'<p class="panel-meta">{html.escape(p.source)}</p>' + reading + explanation + '</article>')
        toc.append(f'<li><a href="#{p.id}">{html.escape(p.title)}</a></li>')
        (data_dir / 'fragments').mkdir(exist_ok=True)
        (data_dir / 'fragments' / f'{p.id}.html').write_text(fragments[p.id], encoding='utf-8')
    title = f'머신러닝기초 {"과제" if pack.profile == "homework" else "복습"} {pack.range} 문제설명'
    values = {'PAGE_TITLE': html.escape(title), 'BRAND': '문제풀이 입문 설명', 'DESCRIPTION': '첫 줄부터 완성 답과 검산까지 설명해요.',
              'TOC': '<ul class="toc-list">' + ''.join(toc) + '</ul>', 'TITLE': html.escape(title),
              'SUBTITLE': '주어진 조건을 읽고, 첫 줄을 쓰고, 이유를 따라가며 답을 확인해요.',
              'SECTIONS': '<section id="problems"><h2>문항별 설명</h2>' + ''.join(articles) + '</section>',
              'FOOTER': '원 문제·정리노트·PDF는 보존해요.', 'SCRIPTS': '',
              'RANGE': f'ml-problem-explain-{pack.profile}-{pack.range}-{pack.slug}', 'VENDOR': data_name + '/vendor'}
    text = (ASSETS / 'note-template.html').read_text(encoding='utf-8')
    for key, value in values.items():
        text = text.replace('{{' + key + '}}', value)
    if re.search(r'\{\{[A-Z_]+\}\}', text):
        raise ExplainError('미치환 템플릿 슬롯')
    html_path.write_text(text, encoding='utf-8')
    ctx = Ctx([(html_path.name, md_path.name)], str(stage / fig_name), fig_name, prefix='explain')
    convert(str(html_path), str(md_path), ctx, ['문제의 첫 줄부터 검산까지 설명해요.'])
    manifest_path = data_dir / 'manifest.json'
    files = tuple(sorted(p for p in stage.rglob('*') if p.is_file()))
    dump(manifest_path, {'version': 1, 'profile': pack.profile, 'range': pack.range, 'slug': pack.slug,
                         'source': str(pack.path), 'source_sha256': pack.sha256,
                         'input_hash': payload_hash(pack, fragments), 'reading_key': values['RANGE'],
                         'destination': str(pack.path.parent), 'repo': str(repo.resolve()),
                         'problems': [{'id': p.id, 'subparts': list(p.subparts)} for p in pack.problems],
                         'files': {p.relative_to(stage).as_posix(): sha256(p) for p in files}})
    return Artifacts(html_path, md_path, manifest_path, tuple(sorted((*files, manifest_path))))

def check_artifacts(pack, artifacts):
    errors = []
    try:
        root = artifacts.html.parent.resolve()
        manifest = json.loads(artifacts.manifest.read_text(encoding='utf-8'))
        if manifest['source_sha256'] != pack.sha256 or manifest['source'] != str(pack.path):
            errors.append('manifest 입력 불일치')
        if manifest['problems'] != [{'id': p.id, 'subparts': list(p.subparts)} for p in pack.problems]:
            errors.append('manifest 문항 집합 불일치')
        owned = set(manifest['files']) | {artifacts.manifest.relative_to(root).as_posix()}
        if owned != {p.relative_to(root).as_posix() for p in artifacts.files}:
            errors.append('산출 파일 집합 불일치')
        for name, digest in manifest['files'].items():
            file = root / name
            if not file.resolve().is_relative_to(root) or not file.is_file() or sha256(file) != digest:
                errors.append('생성 파일 변경/누락: ' + name)
        document = parse(artifacts.html.read_text(encoding='utf-8'))
        ids = [n.attrs['id'] for n in document.find_all(lambda n: 'id' in n.attrs)]
        if len(ids) != len(set(ids)):
            errors.append('중복 문서 ID')
        topics = list(document.find_all(lambda n: n.tag == 'article' and 'topic' in n.classes))
        if [n.attrs.get('id') for n in topics] != [p.id for p in pack.problems]:
            errors.append('문항 순서/ID 불일치')
        for p in pack.problems:
            reading = list(document.find_all(lambda n: n.attrs.get('data-source-problem') == p.id))
            if len(reading) != 1:
                errors.append(f'{p.id}: 원문 보존 실패')
            else:
                for field, expected in [('conditions', p.conditions_html), ('ask', p.ask_html)]:
                    nodes = list(reading[0].find_all(lambda n: n.attrs.get('data-source-field') == field))
                    if len(nodes) != 1 or compact(inner(nodes[0])) != compact(expected):
                        errors.append(f'{p.id}: {field} 원문 보존 실패')
            if pack.profile == 'homework':
                original = list(document.find_all(lambda n: n.attrs.get('data-original-problem') == p.id))
                if len(original) != 1 or compact(p.original_html) not in compact(original[0].text()):
                    errors.append(f'{p.id}: 영어 원문 보존 실패')
        for node in document.find_all(lambda n: n.tag in ('img', 'link', 'script', 'a')):
            href = node.attrs.get('src') or node.attrs.get('href')
            if not href:
                continue
            url = urlsplit(href)
            if url.scheme or url.netloc:
                errors.append('외부 자원/링크: ' + href)
                continue
            if not url.path:
                if url.fragment and unquote(url.fragment) not in ids:
                    errors.append('링크 앵커 없음: ' + href)
                continue
            path = root / unquote(url.path)
            if node.tag == 'a':
                path = Path(manifest['destination']) / unquote(url.path)
            if not path.is_file():
                errors.append('자원 없음: ' + href)
        # Existing Markdown checker resolves links relative to stage; external course links
        # use their intended destination instead (checked above and by browser on publication).
        errors += [e for e in check_md(str(artifacts.html), str(artifacts.md)) if not e.startswith('링크 파일 없음:')]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append('산출 검사 실패: ' + str(exc))
    return errors
