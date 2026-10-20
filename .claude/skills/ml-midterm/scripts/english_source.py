"""Single English source for the PDF and the existing original-problem tab."""
from pathlib import Path
from dataclasses import replace
import re,json,hashlib,html
from exam_adapter import read_cards,normalize_cards,parse,inner,load_exam_source
from review_pdf_payload import to_workbook

INSTRUCTIONS='Show your calculation and derivation steps. All parameter vectors are column vectors; write gradients as row vectors. Unless stated otherwise, the second parameter of a univariate Gaussian is its variance.'
KOREAN=re.compile('[가-힣ㄱ-ㅎㅏ-ㅣ]')

def english_fields(original,pid,parts):
 root=parse(original);fields=[]
 for attr in ['data-english-title','data-english-conditions','data-english-ask']:
  nodes=list(root.find_all(lambda n:attr in n.attrs))
  if len(nodes)!=1 or not nodes[0].text().strip():raise ValueError(f'{pid}: missing, duplicate or empty {attr}')
  fields.append(inner(nodes[0]))
 if KOREAN.search(''.join(fields)):raise ValueError(f'{pid}: Korean in English fields')
 ask=parse(fields[2]);top=[n for n in ask.children if not isinstance(n,str) or n.strip()]
 if len(top)!=1 or isinstance(top[0],str) or top[0].tag!='ol':raise ValueError(f'{pid}: one top-level English ordered list required')
 ol=top[0]
 if ol.attrs.get('type')!='a' or ol.attrs.get('start','1')!='1' or 'reversed' in ol.attrs:raise ValueError(f'{pid}: English list must start at (a)')
 lis=[n for n in ol.children if not isinstance(n,str) or n.strip()]
 if any(isinstance(n,str) or n.tag!='li' or 'value' in n.attrs for n in lis):raise ValueError(f'{pid}: direct English li children without numbering overrides required')
 labels=[n.attrs.get('data-english-part') for n in lis]
 marked=list(ask.find_all(lambda n:'data-english-part' in n.attrs))
 if labels!=list(parts) or len(marked)!=len(lis) or len(list(ask.find_all(lambda n:n.tag=='li')))!=len(lis):raise ValueError(f'{pid}: English subpart count/order mismatch')
 if any(not n.text().strip() for n in lis):raise ValueError(f'{pid}: empty English subpart')
 return tuple(fields)

def load_english_problems(source:Path,blueprint:Path,repo:Path,config):
 pack=load_exam_source(source,blueprint,repo,config)
 normalized=normalize_cards(read_cards(source,config.profile),None,source)
 result=[]
 for p,q in zip(pack.problems,normalized):
  title,conditions,ask=english_fields(p.original_html,p.id,p.subparts)
  c=replace(q.card,title=title,original_html='',hint_html='',steps=(),answer_html='',figures=(),hint_label='')
  result.append(replace(q,card=c,conditions_html=conditions,ask_html=ask))
 return tuple(result)

def english_payload(problems,config,pages=None):
 data=to_workbook(problems,{},'problems',pages,profile=config.profile)
 data['meta']['title']=config.title_en
 for p in data['problems']:
  base=p['id'].split('-')[0]
  p.update(kind='Practice',number='Problem '+base[1:]+(' (continued)' if '-c' in p['id'] else ''),section=f'Midterm Practice {config.round_number:02d}')
  p['html']['original']='';p['hints']=[]
 return data

def english_digests(problems):
 return {p.card.id:hashlib.sha256(json.dumps([p.card.title,p.conditions_html,p.ask_html],ensure_ascii=False,separators=(',',':')).encode()).hexdigest() for p in problems}
