from pathlib import Path
import re,unicodedata
from .contracts import InputError
from .util import file_hash

def norm(s):return unicodedata.normalize('NFC',s)
def normalize_id(s):
 m=re.fullmatch(r'[pP]0*(\d+)',s)
 if not m or int(m[1])<1:raise InputError('invalid problem ID: '+s)
 return 'P'+str(int(m[1]))
def map_pages(card,problem_pdf,answer_pdf,*,explicit=None):
 import fitz
 result=[]
 for role,path in [('problem',Path(problem_pdf)),('answer',Path(answer_pdf))]:
  refs=[]
  with fitz.open(path) as d:
   if explicit:
    if explicit.get('sha256',{}).get(role)!=file_hash(path):raise InputError('stale explicit page-map hash')
    indices=explicit.get(role,[])
    if not indices or any(type(i)!=int or i<0 or i>=len(d) for i in indices) or indices!=sorted(set(indices)):raise InputError('invalid/duplicate explicit page indices')
   else:indices=range(len(d))
   for index in indices:
    pg=d[index];header=norm(pg.get_text(clip=fitz.Rect(0,0,pg.rect.width,min(65,pg.rect.height*.12))));compact=re.sub(r'\s+','',header)
    badge=re.search(r'(?:예제|연습|문제)?P0*(\d+)(?!\d)',header,re.I)
    if not badge or normalize_id('P'+badge[1])!=card['id']:
     if explicit:raise InputError('explicit map header/source mismatch')
     continue
    if re.sub(r'\s+','',card['source']) not in compact:raise InputError('PDF MML source mismatch: '+card['id'])
    title=re.sub(r'\s+','',norm(card['title']))
    # Generated PDF title may omit the "P2 ·" prefix shown by HTML h3.
    title=re.sub(r'^P\d+[·.:—-]*','',title)
    if title and title not in compact:raise InputError('PDF title mismatch: '+card['id'])
    refs.append(dict(id=role+'-'+str(len(refs)+1),role=role,snapshot=str(path.resolve()),page_index=index,width_pt=pg.rect.width,height_pt=pg.rect.height,continuation=len(refs)+1))
   if not refs:raise InputError('PDF header missing: '+card['id']+' '+role)
   # Duplicate first pages cannot be guessed into a continuation.
   for ref in refs[1:]:
    h=norm(d[ref['page_index']].get_text(clip=fitz.Rect(0,0,ref['width_pt'],65)))
    if not explicit and not re.search(r'계속|continued',h,re.I):raise InputError('ambiguous duplicate PDF page; author --page-map')
  result.append(refs)
 return tuple(result)

def compare_conditions(problem_pages,answer_pages):
 import fitz
 def text(refs):
  panels=[]
  for ref in refs:
   with fitz.open(ref['snapshot']) as doc:
    p=doc[ref['page_index']];boxes=[x['rect'] for x in p.get_drawings() if x.get('fill') and len(x['fill'])==3 and max(abs(a-b) for a,b in zip(x['fill'],(246/255,246/255,243/255)))<.002]
    if boxes:
     value=re.sub(r'\s+','',norm(p.get_text(clip=max(boxes,key=lambda r:r.get_area()))))
     if value and value not in panels:panels.append(value)
  return ''.join(panels)
 pp,aa=text(problem_pages),text(answer_pages)
 if (pp or aa) and pp!=aa:raise InputError('problem/answer conditions differ across page set')
