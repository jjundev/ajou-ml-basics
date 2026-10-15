"""Select saved sources without guessing, then preserve their raw questions."""
import hashlib
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from mpe_choices import with_choices
from mpe_types import ExplainError, Problem, SourcePack
from mpe_shared import HOMEWORK, REVIEW, Node, ReviewPdfError, read_cards, normalize_cards, parse

def nfc(value):
    return unicodedata.normalize('NFC', str(value))

def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inside(path: Path, repo: Path) -> Path:
    path, repo = Path(path).absolute(), Path(repo).absolute()
    # Normalize unresolved spellings only; two existing NFC/NFD sibling directories are distinct.
    if not repo.exists():
        repo = existing_path(repo)
    try:
        path.resolve().relative_to(repo.resolve())
    except ValueError:
        try:
            if not path.exists():
                path = existing_path(path)
            path.resolve().relative_to(repo.resolve())
        except (ValueError, OSError) as exc:
            raise ExplainError(f'저장소 밖 경로: {path}') from exc
    current = path
    while current != repo and current != current.parent:
        if current.is_symlink():
            raise ExplainError(f'심볼릭 링크 입력 금지: {current}')
        current = current.parent
    return path

def existing_path(path: Path) -> Path:
    """Resolve encoded/Unicode-normalized paths component by component."""
    path = path.absolute()
    current = Path(path.anchor)
    for part in path.parts[1:]:
        candidate = current / part
        if candidate.exists():
            current = candidate
        elif current.is_dir():
            matches = [p for p in current.iterdir() if nfc(p.name) == nfc(part)]
            if len(matches) != 1:
                raise ExplainError(f'경로 없음 또는 모호함: {path}')
            current = matches[0]
        else:
            raise ExplainError(f'경로 없음: {path}')
    return current

def date_key(value):
    try:
        datetime.strptime('2000' + value, '%Y%m%d')
    except ValueError as exc:
        raise ExplainError(f'잘못된 날짜: {value}') from exc
    return value

def resolve_sources(repo: Path, target: str | None) -> tuple[Path, ...]:
    repo = repo.resolve()
    if target and target.lower().endswith('.html'):
        path = Path(target)
        path = path if path.is_absolute() else repo / path
        path = inside(path, repo)
        if not path.is_file():
            try:
                path = inside(existing_path(path), repo)
            except ExplainError as exc:
                raise ExplainError(f'대상 없음: {path}') from exc
        return (path,)
    candidates = []
    for path in repo.rglob('*.html'):
        rel = nfc(path.relative_to(repo))
        if rel.split('\\')[0].split('/')[0] not in ('복습노트', '과제'):
            continue
        for profile in (REVIEW, HOMEWORK):
            match = re.fullmatch(profile.filename_re, nfc(path.name))
            if match:
                candidates.append((profile.name, match[1], path))
    if target == 'all':
        found = [path for kind, _, path in candidates if kind == 'review']
    elif target and re.fullmatch(r'(?:과제|hw)\s*[1-9]\d*', target, re.I):
        number = str(int(re.search(r'\d+', target)[0]))
        found = [p for kind, value, p in candidates if kind == 'homework' and value == number]
        if not found:
            raise ExplainError('대상 없음: 과제 카드 HTML을 먼저 준비하세요 (PDF 전사는 별도 작업).')
    else:
        reviews = [(value, path) for kind, value, path in candidates if kind == 'review']
        if target is None:
            latest = max((value.split('-')[-1] for value, _ in reviews), default='')
            latest_candidates = [(value, path) for value, path in reviews if value.split('-')[-1] == latest]
            ranges = {value for value, _ in latest_candidates}
            if len(ranges) > 1:
                raise ExplainError('여러 후보 (최신 날짜의 통합/개별):\n' + '\n'.join(str(p) for _, p in latest_candidates))
            target = next(iter(ranges), '')
        if not re.fullmatch(r'\d{4}(?:-\d{4})?', target):
            raise ExplainError('대상 없음 또는 잘못된 대상: ' + target)
        bounds = target.split('-')
        for date in bounds:
            date_key(date)
        if len(bounds) == 2 and bounds[0] > bounds[1]:
            raise ExplainError('날짜 범위 순서 오류')
        found = [path for value, path in reviews if value == target]
        if len(bounds) == 2:
            individual = [path for value, path in reviews if '-' not in value and bounds[0] <= value <= bounds[1]]
            if found and individual:
                raise ExplainError('여러 후보 (통합/개별):\n' + '\n'.join(map(str, found + individual)))
            if not found:
                found = individual
    if not found:
        raise ExplainError('대상 없음: ' + str(target))
    by_range = {}
    for path in found:
        match = re.fullmatch((HOMEWORK if nfc(path.name).startswith('과제') else REVIEW).filename_re, nfc(path.name))
        by_range.setdefault(match[1], []).append(path)
    if any(len(group) > 1 for group in by_range.values()):
        raise ExplainError('여러 후보: HTML 경로를 명시하세요.\n' + '\n'.join(map(str, found)))
    if target == 'all':
        found.sort(key=lambda p: (re.fullmatch(REVIEW.filename_re,nfc(p.name))[1].split('-')[-1],nfc(p.name)),reverse=True)
        return tuple(inside(path,repo) for path in found)
    return tuple(inside(path, repo) for path in sorted(found, key=lambda p: nfc(p.name)))

def choice_container(node, root):
    return bool({'choices','options'} & set(node.classes)) or any({'choices','options'} & set(a.classes) for a in ancestors(node,root))

def subparts(ask: str, original: str) -> tuple[str, ...]:
    root = parse(ask)
    original_root = parse(original)
    parts = list(original_root.find_all(lambda n: 'part' in n.classes))
    marked = tuple(m[1] for n in parts if (m := re.match(r'\s*\(([a-z])\)', n.text())))
    lists = [n for n in root.find_all(lambda n: n.tag == 'ol')
             if not choice_container(n,root) and not any(a.tag in ('li', 'ol') for a in ancestors(n, root))]
    if len(lists) > 1:
        raise ExplainError('질문 목록 여러 개: 소문항 구분을 확인하세요')
    if not lists:
        if marked:
            raise ExplainError('질문 목록·원문 소문항 표지 불일치')
        return ('main',)
    items = [n for n in lists[0].children if isinstance(n, Node) and n.tag == 'li']
    labels = tuple((re.match(r'\s*\(([a-z])\)', n.text())[1]
                    if re.match(r'\s*\(([a-z])\)', n.text()) else chr(97 + i)) for i, n in enumerate(items))
    if not labels or len(labels) != len(set(labels)):
        raise ExplainError('중복 또는 빈 소문항 표지')
    if marked and set(marked) != set(labels):
        raise ExplainError('질문 목록·원문 소문항 표지 불일치')
    return labels

def ancestors(node, root):
    node = node.parent
    while node is not root and node is not None:
        yield node
        node = node.parent

def load_source(path: Path, repo: Path) -> SourcePack:
    path = inside(Path(path), Path(repo))
    try:
        profile = HOMEWORK if nfc(path.name).startswith('과제') else REVIEW
        pack = read_cards(path, profile)
        layouts = None
        for card in pack.cards:
            root = parse(card.statement_html)
            if not all(len([n for n in root.children if isinstance(n, Node) and cls in n.classes]) == 1
                       for cls in ('conditions', 'ask')):
                layout = existing_path(repo / 'workbook/layouts' / f'{pack.range}_{pack.slug}.json')
                layouts = json.loads(layout.read_text(encoding='utf-8'))
                break
        normalized = normalize_cards(pack, layouts, path)
        problems = tuple(Problem(n.card.id, int(n.card.id[1:]), n.card.title, n.card.source,
                                 n.card.original_html, n.conditions_html, n.ask_html,
                                 tuple(f.html for f in n.card.figures), n.card.steps, n.card.answer_html,
                                 subparts(n.ask_html, n.card.original_html)) for n in normalized)
        return SourcePack(profile.name, pack.range, pack.slug, path, sha256(path), with_choices(path,problems))
    except (ReviewPdfError, OSError, json.JSONDecodeError) as exc:
        raise ExplainError(str(exc)) from exc
