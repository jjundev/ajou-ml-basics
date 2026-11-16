"""Store the authored parts of a review as data and keep their pack-relative URLs."""
import hashlib
import html
from html.parser import HTMLParser
from itertools import groupby
import json
from pathlib import Path
import re
import unicodedata

from review_pdf_types import REVIEW, ReviewPdfError


class CardFragments(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.source = source
        self.starts = [0, *(m.end() for m in re.finditer('\n', source))]
        self.sections = []
        self.article_depth = 0
        self.card = None
        self.cards = []
        self.interaction = None
        self.script_start = None
        self.feed(source)
        self.close()
        if self.card is not None or self.script_start is not None:
            raise ReviewPdfError('unclosed review source fragment')

    def position(self):
        line, column = self.getpos()
        return self.starts[line - 1] + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'section':
            self.sections.append(attrs.get('id', ''))
        elif tag == 'article':
            self.article_depth += 1
            if 'card' in (attrs.get('class') or '').split() and self.card is None:
                self.card = (self.article_depth, self.position(), self.sections[-1] if self.sections else '')
        elif tag == 'script' and attrs.get('id') == 'review-interaction-model':
            self.script_start = self.position()

    def handle_endtag(self, tag):
        if tag == 'section' and self.sections:
            self.sections.pop()
        elif tag == 'article':
            if self.card is not None and self.card[0] == self.article_depth:
                _, start, section = self.card
                end = self.source.index('>', self.position()) + 1
                self.cards.append({'section': section, 'markup': self.source[start:end]})
                self.card = None
            self.article_depth -= 1
        elif tag == 'script' and self.script_start is not None:
            if self.interaction is not None:
                raise ReviewPdfError('duplicate review interaction model')
            end = self.source.index('>', self.position()) + 1
            self.interaction = self.source[self.script_start:end]
            self.script_start = None


def review_dir(path):
    path = Path(path)
    return path.parent.parent if path.name.endswith('.cards.json') else path.parent


def html_name(path):
    return re.sub(r'\.cards\.json$', '.html', unicodedata.normalize('NFC', Path(path).name))


def archive_path(html_path):
    path = Path(html_path)
    return path.parent / '.pack' / (unicodedata.normalize('NFC', path.stem) + '.cards.json')


def find_review(html_path):
    path = Path(html_path)
    data = archive_path(path)
    return data if data.is_file() else path


def read_archive(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if (not isinstance(data, dict) or data.get('version') != 1
            or not isinstance(data.get('source_sha256'), str)
            or not re.fullmatch(r'[0-9a-f]{64}', data['source_sha256'])
            or not isinstance(data.get('cards'), list) or not data['cards']
            or any(not isinstance(card, dict) or not isinstance(card.get('section'), str)
                   or not isinstance(card.get('markup'), str) for card in data['cards'])
            or not (data.get('interaction') is None or isinstance(data['interaction'], str))):
        raise ReviewPdfError(f'{path}: invalid review card archive')
    return data


def source_markup(path):
    path = Path(path)
    if path.suffix != '.json':
        return path.read_text(encoding='utf-8')
    data = read_archive(path)
    sections = []
    for section, cards in groupby(data['cards'], key=lambda card: card['section']):
        markup = '\n'.join(card['markup'] for card in cards)
        sections.append(f'<section id="{html.escape(section, quote=True)}">{markup}</section>')
    return '\n'.join([*sections, data.get('interaction') or ''])


def legacy_digest(path):
    path = Path(path)
    if path.name.endswith('.cards.json'):
        return read_archive(path)['source_sha256']
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archive_cards(html_path):
    path = Path(html_path)
    if not re.fullmatch(REVIEW.filename_re, html_name(path)):
        raise ReviewPdfError(f'invalid review filename: {path.name}')
    raw = path.read_bytes()
    parts = CardFragments(raw.decode('utf-8'))
    if not parts.cards:
        raise ReviewPdfError(f'{path}: no review cards')
    target = archive_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({
        'version': 1, 'source_sha256': hashlib.sha256(raw).hexdigest(),
        'cards': parts.cards, 'interaction': parts.interaction,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return target


def source_pdf(path, kind):
    path = Path(path)
    if kind not in ('문제', '답안'):
        raise ReviewPdfError(f'invalid PDF kind: {kind}')
    root = review_dir(path)
    name = f'{Path(html_name(path)).stem}-{kind}.pdf'
    current = root / name
    packed = root / '.pack' / name
    return packed if not current.is_file() and packed.is_file() else current


def source_markdown(path):
    path = Path(path)
    root = review_dir(path)
    name = Path(html_name(path)).with_suffix('.md').name
    packed = root / '.pack' / name
    return packed if packed.is_file() else root / name


def discover_reviews(root):
    """Prefer a pack's archived cards over the matching legacy HTML."""
    root = Path(root)
    return sorted({
        find_review(review_dir(path) / html_name(path)) if path.name.endswith('.cards.json') else find_review(path)
        for pattern in ('*.html', '.pack/*.cards.json')
        for path in root.rglob(pattern)
        if path.is_file() and re.fullmatch(REVIEW.filename_re, html_name(path))
    })
