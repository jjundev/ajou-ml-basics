"""Parse source cards without executing their browser scripts."""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
import re
from .contracts import InputError
VOID={'img','br','hr','input','meta','link','source','wbr'}
class Node:
 def __init__(self,tag='',attrs=()):self.tag=tag;self.attrs=dict(attrs);self.children=[]
 def all(self,pred):
  out=[]
  for c in self.children:
   if isinstance(c,Node):
    if pred(c):out.append(c)
    out.extend(c.all(pred))
  return out
 def cls(self,name):return name in self.attrs.get('class','').split()
 def text(self):return ''.join(c.text() if isinstance(c,Node) else c for c in self.children)
 def inner(self):return ''.join(c.outer() if isinstance(c,Node) else escape(c,quote=False) for c in self.children)
 def outer(self):
  start='<'+self.tag+''.join(' '+k+'="'+escape(v or '',quote=True)+'"' for k,v in self.attrs.items())+'>'
  return start if self.tag in VOID else start+self.inner()+'</'+self.tag+'>'
class Parser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root]
 def handle_starttag(self,tag,attrs):
  n=Node(tag,attrs);self.stack[-1].children.append(n)
  if tag not in VOID:self.stack.append(n)
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs);self.handle_endtag(tag)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==tag:self.stack=self.stack[:i];return
 def handle_data(self,data):self.stack[-1].children.append(data)
def one(n,pred,name):
 found=n.all(pred)
 if len(found)!=1:raise InputError('missing or ambiguous '+name)
 return found[0]
def read_cards(path:Path,problem_ids=None,*,errors=None)->list[dict]:
 parser=Parser();parser.feed(Path(path).read_text(encoding='utf-8'));out=[];seen=set()
 selected=set(problem_ids) if problem_ids is not None else None
 for node in parser.root.all(lambda n:n.tag=='article' and n.cls('card')):
  pid=node.attrs.get('id','');source=node.attrs.get('data-source','')
  if not re.fullmatch('p[1-9][0-9]*',pid) or pid in seen:raise InputError('invalid/duplicate card ID')
  seen.add(pid)
  if selected is not None and pid.upper() not in selected:continue
  try:
   if not re.fullmatch(r'MML (Example|Exercise) \d+(?:\.\d+)+',source):raise InputError('invalid MML source')
   problem=one(node,lambda n:n.cls('problem'),'problem');sol=one(node,lambda n:n.cls('solution'),'solution')
   cs=problem.all(lambda n:n.cls('conditions'));qs=problem.all(lambda n:n.cls('ask'))
   if not cs and not qs:
    conditions_html=ask_html='';partition_status='author-required'
   elif len(cs)==len(qs)==1:
    conditions_html,ask_html=cs[0].inner(),qs[0].inner();partition_status='partitioned'
    if not qs[0].text().strip():raise InputError('empty ask')
   else:raise InputError('missing or ambiguous conditions/ask')
   stepsnode=one(sol,lambda n:n.cls('steps'),'steps');steps=[c.inner().strip() for c in stepsnode.children if isinstance(c,Node) and c.tag=='li']
   answer=one(sol,lambda n:n.cls('answer'),'answer');title=one(node,lambda n:n.tag=='h3','title').text().strip()
   if not steps or any(not s for s in steps) or not answer.text().strip() or not problem.text().strip():raise InputError('empty solution/ask')
   paths=[n.attrs['src'] for n in node.all(lambda n:n.tag=='img' and 'src' in n.attrs)]
   out.append(dict(id=pid.upper(),title=title,source=source,conditions_html=conditions_html,ask_html=ask_html,statement_html=problem.inner(),partition_status=partition_status,steps=steps,answer_html=answer.inner(),figure_paths=list(dict.fromkeys(paths))))
  except InputError as ex:
   if errors is None:raise
   errors.append(dict(problem_id=pid.upper(),reason=str(ex)))
 if not out and not errors:raise InputError('no ML cards')
 return out
