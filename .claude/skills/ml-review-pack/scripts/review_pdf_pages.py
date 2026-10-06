"""Finite pagination using whole solution steps and question blocks."""
from dataclasses import replace
from html2md import Node
from review_pdf_cards import parse, outer
from review_pdf_payload import initial_pages, page_id
from review_pdf_types import ReviewPdfError


def _question_blocks(text):
    root=parse(text)
    nodes=[n for n in root.children if not isinstance(n,str) or n.strip()]
    if len(nodes)==1 and isinstance(nodes[0],Node) and nodes[0].tag in ('ol','ul'):
        n=nodes[0]
        items=[c for c in n.children if isinstance(c,Node) and c.tag=='li']
        try:start=int(n.attrs.get('start',len(items) if 'reversed' in n.attrs else '1'))
        except ValueError:raise ReviewPdfError('invalid ordered list start')
        result=[]
        for i,c in enumerate(items):
            value=c.attrs.get('value')
            if value is not None:
                try:start=int(value)
                except ValueError:raise ReviewPdfError('invalid ordered list item value')
            wrapper=Node(n.tag,n.attrs.copy())
            if n.tag=='ol':wrapper.attrs['start']=str(start)
            wrapper.children=[c];result.append(outer(wrapper))
            start+=-1 if 'reversed' in n.attrs else 1
        return result
    # Text and inline emphasis belong to the same semantic sentence/block.
    # Never infer a sentence boundary from an HTML inline tag.
    block_tags={'p','div','ol','ul','blockquote','h1','h2','h3','h4','section'}
    result=[];inline=[]
    for n in nodes:
        if isinstance(n,Node) and n.tag in block_tags:
            if inline:result.append(''.join(inline));inline=[]
            result.append(outer(n))
        else:inline.append(outer(n))
    if inline:result.append(''.join(inline))
    return result


def _renumber(pages):
    counts={};out=[]
    for p in pages:
        counts[p.logical_id]=counts.get(p.logical_id,0)+1
        out.append(replace(p,continuation=counts[p.logical_id]))
    return out


def paginate(problems,mode,measure):
    if mode not in ('problems','answers'):raise ReviewPdfError(f'invalid mode: {mode}')
    pages=initial_pages(problems)
    # Every iteration consumes a whole-step or whole-question boundary.
    max_splits=sum(len(p.card.steps)+len(_question_blocks(p.ask_html)) for p in problems)
    for _ in range(max_splits+1):
        report=measure(pages)
        if report.failed_resources or report.katex_errors:raise ReviewPdfError('pagination resource/math failure')
        if not report.issues:return pages
        issue=report.issues[0]
        idx=next((i for i,p in enumerate(pages) if page_id(p)==issue.page_id),None)
        if idx is None:raise ReviewPdfError(f'{issue.page_id}: unsplittable {issue.area}: {issue.detail}')
        p=pages[idx]
        if 'writing space' in issue.detail:raise ReviewPdfError(f'{p.logical_id}: missing writing space')
        if mode=='answers' and issue.area in ('work','answer') and p.step_end-p.step_start>1:
            boundary=(p.step_start+p.step_end)//2
            first=replace(p,step_end=boundary,show_answer=False)
            second=replace(p,step_start=boundary,show_original=False)
        elif issue.area=='panel':
            blocks=_question_blocks(p.ask_html)
            if len(blocks)<2:raise ReviewPdfError(f'{p.logical_id}: unsplittable panel/conditions: {issue.detail}')
            boundary=len(blocks)//2
            first=replace(p,ask_html=''.join(blocks[:boundary]),show_answer=False,step_end=p.step_start)
            second=replace(p,ask_html=''.join(blocks[boundary:]),show_original=False)
        else:raise ReviewPdfError(f'{p.logical_id}: unsplittable {issue.area}: {issue.detail}')
        pages[idx:idx+1]=[first,second];pages=_renumber(pages)
    raise ReviewPdfError('unsplittable pagination exhausted finite boundaries')
