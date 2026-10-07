"""Parse saved HTML rather than its JavaScript-mutated DOM."""
from pathlib import Path
import hashlib
import html
import re
import unicodedata
from html2md import Builder, Node, VOID, serialize
from check_html import math_delimiter_errors
from review_pdf_types import CardProfile, REVIEW, FigureInput, ReviewCard, ReviewPack, NormalizedProblem, ReviewPdfError


def parse(text):
    parser=Builder();parser.feed(text);return parser.root


def outer(node):
    if isinstance(node,str):return html.escape(node,quote=False)
    if node.tag=='svg':return serialize(node)
    attrs=''.join(f' {k}="{html.escape(v,quote=True)}"' for k,v in node.attrs.items())
    start=f'<{node.tag}{attrs}>'
    return start if node.tag in VOID else start+inner(node)+f'</{node.tag}>'


def inner(node, skip_summary=False):
    return ''.join(outer(c) for c in node.children if not (skip_summary and isinstance(c,Node) and c.tag=='summary'))


def one(node, cls, context):
    found=list(node.find_all(lambda n:cls in n.classes))
    if len(found)!=1:raise ReviewPdfError(f'{context}: missing or ambiguous {cls}')
    return found[0]


def media_nodes(node):
    result=[]
    def walk(n):
        for c in n.children:
            if not isinstance(c,Node):continue
            if c.tag in ('svg','table','img','figure') or 'figure' in c.classes:
                result.append(c)
            else:walk(c)
    walk(node);return result


def without_media(text):
    root=parse(text)
    for n in media_nodes(root):n.parent.children.remove(n)
    return inner(root)


def compact(text):
    return re.sub(r'\s+','',parse(text).text())


def read_cards(path: Path, profile: CardProfile = REVIEW) -> ReviewPack:
    path=Path(path)
    m=re.fullmatch(profile.filename_re,unicodedata.normalize('NFC',path.name))
    if not m:raise ReviewPdfError(f'invalid {profile.name} filename: {path.name}')
    root=parse(path.read_text(encoding='utf-8'));cards=[];seen=set()
    for node in root.find_all(lambda n:n.tag=='article' and 'card' in n.classes):
        id_=node.attrs.get('id','')
        if not re.fullmatch(r'p[1-9]\d*',id_) or id_ in seen:raise ReviewPdfError(f'{m[1]} {id_}: invalid/duplicate id')
        seen.add(id_);source=node.attrs.get('data-source','')
        if not re.fullmatch(profile.source_re,source):raise ReviewPdfError(f'{id_}: invalid source')
        expected=profile.expected_source(m[1],id_)
        if expected and source!=expected:raise ReviewPdfError(f'{id_}: source {source} != {expected}')
        titles=list(node.find_all(lambda n:n.tag=='h3'))
        if len(titles)!=1:raise ReviewPdfError(f'{id_}: missing title')
        problem=one(node,'problem',id_);sol=one(node,'solution',id_)
        steps_node=one(sol,'steps',id_);steps=tuple(inner(n).strip() for n in steps_node.children if isinstance(n,Node) and n.tag=='li')
        if not steps or any(not compact(s) for s in steps):raise ReviewPdfError(f'{id_}: missing solution steps')
        figures=[]
        for i,n in enumerate(media_nodes(problem),1):
            kind='svg' if n.tag=='svg' or list(n.find_all(lambda c:c.tag=='svg')) else 'table' if n.tag=='table' or list(n.find_all(lambda c:c.tag=='table')) else 'image'
            figures.append(FigureInput(f'f{i}',outer(n),kind))
        ancestor=node.parent
        while ancestor is not root and ancestor.tag!='section':ancestor=ancestor.parent
        card=ReviewCard(id_,titles[0].text().strip(),source,ancestor.attrs.get('id',''),inner(problem).strip(),inner(one(node,'original',id_),True).strip(),inner(one(node,'hint',id_),True).strip(),steps,inner(one(sol,'answer',id_)).strip(),tuple(figures))
        for field in [card.statement_html,card.original_html,card.hint_html,*card.steps,card.answer_html]:
            errors=math_delimiter_errors(parse(field).text())
            if errors:raise ReviewPdfError(f'{id_}: math {errors}')
        if not compact(card.answer_html):raise ReviewPdfError(f'{id_}: missing answer')
        cards.append(card)
    if not cards:raise ReviewPdfError(f'{path}: no review cards')
    return ReviewPack(m[1],m[2],tuple(cards),path.resolve(),profile)


def normalize_cards(pack: ReviewPack, layouts: dict | None, source_path: Path) -> tuple[NormalizedProblem,...]:
    if layouts is not None:
        if layouts.get('source_sha256')!=hashlib.sha256(Path(source_path).read_bytes()).hexdigest():raise ReviewPdfError(f'{pack.range}: stale layout source')
        if set(layouts.get('problems',{}))!={c.id for c in pack.cards}:raise ReviewPdfError(f'{pack.range}: layout ids do not match')
    out=[]
    for card in pack.cards:
        if layouts is not None:
            fields=layouts['problems'][card.id]
            for key in ('conditions_html','ask_html'):
                if not isinstance(fields.get(key),str):raise ReviewPdfError(f'{card.id}: missing {key}')
            conditions,ask=fields['conditions_html'],fields['ask_html']
        else:
            root=parse(card.statement_html)
            def direct(cls):return [c for c in root.children if isinstance(c,Node) and cls in c.classes]
            if len(direct('conditions'))!=1 or len(direct('ask'))!=1:raise ReviewPdfError(f'{card.id}: conditions/ask markup or manual layout required')
            conditions,ask=inner(direct('conditions')[0]),inner(direct('ask')[0])
        conditions,ask=without_media(conditions),without_media(ask)
        if not compact(ask):raise ReviewPdfError(f'{card.id}: empty ask')
        if compact(conditions+ask)!=compact(without_media(card.statement_html)):raise ReviewPdfError(f'{card.id}: statement preservation failed')
        out.append(NormalizedProblem(card,conditions,ask))
    return tuple(out)
