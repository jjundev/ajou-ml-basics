import json, pathlib, hashlib, re, html, sys
from html.parser import HTMLParser
BASE=pathlib.Path('/Users/hyunjun_macbook_pro/Documents/Univ/.course-summary-worktrees/2026-10-20')
ACA=BASE/'자구알/.superpowers/sdd/2026-10-20-course-html-summary-panels/academic'
OUT=ACA/'dated-controller-comparison'
class Node:
 def __init__(self,tag='',attrs=None,start=0): self.tag=tag;self.attrs=dict(attrs or []);self.children=[];self.start=start;self.end=start
 def text(self): return ' '.join(x if isinstance(x,str) else x.text() for x in self.children)
 def all(self,pred):
  out=[]
  for n in self.children:
   if isinstance(n,Node):
    if pred(n):out.append(n)
    out.extend(n.all(pred))
  return out
class Parser(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.s=s;self.offsets=[0];self.root=Node();self.stack=[self.root]
  for m in re.finditer('\n',s):self.offsets.append(m.end())
  self.feed(s)
 def pos(self):l,c=self.getpos();return self.offsets[l-1]+c
 def handle_starttag(self,t,a):
  n=Node(t,a,self.pos());self.stack[-1].children.append(n)
  if t not in ['br','hr','img','meta','link','input','source','wbr','path','line','circle','rect','ellipse','polyline','polygon','use']:self.stack.append(n)
  else:n.end=self.pos()+len(self.get_starttag_text())
 def handle_startendtag(self,t,a):
  n=Node(t,a,self.pos());n.end=self.s.find('>',self.pos())+1;self.stack[-1].children.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:
    self.stack[i].end=self.s.find('>',self.pos())+1;self.stack=self.stack[:i];break
 def handle_data(self,d):self.stack[-1].children.append(d)
def text(s):return re.sub(r'\s+',' ',Parser(s).root.text()).strip()
def canon(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(d):return hashlib.sha256(d if isinstance(d,bytes) else d.encode()).hexdigest()
MAP=json.loads((BASE/'머신러닝기초/.task6c-run-ml-01/current-pack-reference-map.json').read_text())
def data():
 for group in [1,2]:
  fp=ACA/f'dated-group{group}/results.json';frozen=json.loads(fp.read_text())
  for pack in frozen['packs']:
   key=pack['pack_id']; m=next(x for x in MAP if x['pack_id']==('homework-1-Homework1' if key=='hw1' else x['pack_id']) and (key=='hw1' or x['pack_id'].startswith('review-'+key+'-')))
   packetpath=BASE/f'머신러닝기초/.task6c-run-ml-01/blind-review-packets/group-{group}/{key}/PACK/questions.json'
   if not packetpath.exists():packetpath=packetpath.parent.parent/'questions.json'
   pq=json.loads(packetpath.read_text())
   yield group,fp,pack,m,packetpath,pq
def show(keys):
 for g,fp,pack,m,pp,pq in data():
  key=pack['pack_id']
  if key not in [x.split(':')[0] for x in keys]:continue
  print('\n## PACK',key)
  for q in pq['questions']:
   if key not in keys and (key+':'+q['id']) not in keys:continue
   r=next(r for r in pack['results'] if r['id']==q['id']); raw=(pathlib.Path(m['active_fragment_directory'])/(q['id']+'.html')).read_text(); root=Parser(raw).root
   print('\n###',q['id'],'SOURCE',text(q['conditions_html']+q['ask_html']));print('ORIGINAL',text(q.get('original_question_html','')))
   print('FROZEN',[(s['subpart_id'],s['conclusion'],s['unresolved']) for s in r['subparts']])
   for sec in ['solve','verify','pitfall']:
    ns=root.all(lambda n:n.attrs.get('data-explanation')==sec);print(sec, re.sub(r'\s+',' ',ns[0].text()).strip() if ns else 'MISSING')
   ns=root.all(lambda n:'sum' in n.attrs.get('class','').split()); print('SUM',text(raw[ns[0].start:ns[0].end]) if ns else 'MISSING')
if __name__=='__main__':show(sys.argv[1:])
