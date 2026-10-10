"""Convert normalized review cards into the unchanged EC2 template schema."""
import json
import re
from review_pdf_types import PageSlice, ReviewPdfError, REVIEW


# 템플릿(고정)의 breakEquations와 같은 수식 토큰·분할 기준
MATH_RE=re.compile(r'\$\$([\s\S]+?)\$\$|\$([^$]+?)\$')
EQ_SPLIT_LEN=40
TALL_OPEN='<span style="display:inline-block;margin:.8mm 0">'
GAP_OPEN='<div style="margin-top:1.6mm">'
PART_OPEN='<div class="part" style="margin-top:1.6mm">'


REL_RE=re.compile(r'(?:=|\\(?:approx|Rightarrow|leq?|geq?)(?![a-zA-Z]))')
CMD_RE=re.compile(r'\\([a-zA-Z]+|.)')


def has_top_level_relation(tex):
    """Port of the template's splitRelations test: a relation outside braces and \\left…\\right."""
    depth=0;i=0
    while i<len(tex):
        c=tex[i]
        if depth==0 and c in '=\\' and REL_RE.match(tex,i):return True
        if c=='{':depth+=1
        elif c=='}':depth-=1
        elif c=='\\':
            m=CMD_RE.match(tex,i);cmd=m[1] if m else ''
            if cmd=='left':depth+=1
            elif cmd=='right':depth-=1
            i+=len(cmd)
        i+=1
    return False


def space_math(html):
    """Give tall math vertical room without touching the frozen template CSS.

    Inline matrices become margin-bearing inline-blocks (only when the template keeps them
    inline), a display that directly follows another display gets a top gap, and
    <div class="part"> gets a top margin. Idempotent; text and TeX are unchanged."""
    if not html:return html
    toks=[];last=0
    for m in MATH_RE.finditer(html):
        toks+=[html[last:m.start()],m];last=m.end()
    toks.append(html[last:])
    out=[toks[0]];prev_display=False;prev_gapped=False
    for k in range(1,len(toks),2):
        m=toks[k];before=out[-1];after=toks[k+1]
        if m[1] is not None:
            between=before[6:] if prev_gapped and before.startswith('</div>') else before
            gapped=before.endswith(GAP_OPEN)
            if not gapped and prev_display and k>1 and not between.strip():
                out[-1]=before+GAP_OPEN;after='</div>'+after;gapped=True
            prev_display,prev_gapped=True,gapped
        else:
            tex=m[2].strip()
            keeps_inline=len(tex)<=EQ_SPLIT_LEN or not has_top_level_relation(tex)
            if '\\begin{' in tex and keeps_inline and not before.endswith(TALL_OPEN):
                out[-1]=before+TALL_OPEN;after='</span>'+after
            prev_display=prev_gapped=False
        out+=[m[0],after]
    return ''.join(out).replace('<div class="part">',PART_OPEN)


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
        item={'id':page_id(page),'kind':profile.kind(c.source),'number':c.id.upper()+(' (계속)' if page.continuation>1 else ''),'title':re.sub(r'^P\d+\.\s*','',c.title),'section':c.source,'book_page':None,'difficulty':0,'sol':False,'original_lang':'en','html':{'original':space_math(c.original_html) if page.show_original else '', 'conditions':space_math(page.conditions_html),'ask':space_math(page.ask_html)},'figures':figs,'hints':[{'label':c.hint_label or '풀이 방향','html':space_math(c.hint_html)}] if c.hint_html and page.continuation==1 else []}
        if mode=='answers':item['solution']={'steps':[{'label':'','html':space_math(s)} for s in c.steps[page.step_start:page.step_end]],'answer':space_math(c.answer_html) if page.show_answer else ''}
        records.append(item)
    return {'meta':{'title':'머신러닝기초 복습문제','total':len(records)},'problems':records}


def inject_data(template,payload):
    if template.count('__WORKBOOK_DATA__')!=1:raise ReviewPdfError('template must contain one workbook placeholder')
    return template.replace('__WORKBOOK_DATA__',json.dumps(payload,ensure_ascii=False).replace('<',r'\u003c'))
