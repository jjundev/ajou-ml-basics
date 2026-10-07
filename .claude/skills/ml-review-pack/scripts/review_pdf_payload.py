"""Convert normalized review cards into the unchanged EC2 template schema."""
import json
import re
from review_pdf_types import PageSlice, ReviewPdfError, REVIEW


def initial_pages(problems):
    return [PageSlice(p.card.id,1,p.conditions_html,p.ask_html,0,len(p.card.steps),tuple(f.id for f in p.card.figures),True,True) for p in problems]


def page_id(page):
    return page.logical_id if page.continuation==1 else f'{page.logical_id}-c{page.continuation}'


def to_workbook(problems, assets, mode, pages=None, profile=REVIEW):
    if mode not in ('problems','answers'):raise ReviewPdfError(f'invalid mode: {mode}')
    ps=initial_pages(problems) if pages is None else pages
    lookup={p.card.id:p for p in problems};records=[]
    for page in ps:
        p=lookup[page.logical_id];c=p.card
        figs=[]
        for fid in page.figure_ids:
            asset=assets.get((c.id,fid))
            if asset is None:raise ReviewPdfError(f'{c.id}: missing asset {fid}')
            figs.append({'src':asset.src,'w_mm':asset.w_mm,'h_mm':asset.h_mm})
        item={'id':page_id(page),'kind':profile.kind(c.source),'number':c.id.upper()+(' (계속)' if page.continuation>1 else ''),'title':re.sub(r'^P\d+\.\s*','',c.title),'section':c.source,'book_page':None,'difficulty':0,'sol':False,'original_lang':'en','html':{'original':c.original_html if page.show_original else '', 'conditions':page.conditions_html,'ask':page.ask_html},'figures':figs,'hints':[{'label':'풀이 방향','html':c.hint_html}] if c.hint_html and page.continuation==1 else []}
        if mode=='answers':item['solution']={'steps':[{'label':'','html':s} for s in c.steps[page.step_start:page.step_end]],'answer':c.answer_html if page.show_answer else ''}
        records.append(item)
    return {'meta':{'title':'머신러닝기초 복습문제','total':len(records)},'problems':records}


def inject_data(template,payload):
    if template.count('__WORKBOOK_DATA__')!=1:raise ReviewPdfError('template must contain one workbook placeholder')
    return template.replace('__WORKBOOK_DATA__',json.dumps(payload,ensure_ascii=False).replace('<',r'\u003c'))
