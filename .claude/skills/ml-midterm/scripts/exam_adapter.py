"""Local EXAM input adapter; the shared course generators stay unchanged."""
from pathlib import Path
import sys,json,hashlib,unicodedata,html
from collections import Counter
from exam_config import ExamConfig, config_for_output
from review_pdf_cards import read_cards,normalize_cards,parse,inner,outer
from mpe_source import subparts,existing_path
from mpe_types import Problem,SourcePack
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def resolve(repo,path):
 p=Path(path);p=p if p.is_absolute() else Path(repo)/p
 # reject lexical escapes and symlink escapes, then normalize existing components
 p=p.absolute()
 try:p.resolve().relative_to(Path(repo).resolve())
 except ValueError:raise ValueError('outside repository: '+str(p))
 current=Path(p.anchor)
 for part in p.parts[1:]:
  matches=[x for x in current.iterdir() if unicodedata.normalize('NFC',x.name)==unicodedata.normalize('NFC',part)]
  if len(matches)!=1:raise ValueError('missing or ambiguous path: '+str(p))
  current=matches[0]
 p=current
 if not p.resolve().is_relative_to(Path(repo).resolve()):raise ValueError('outside repository')
 return p

def validate_blueprint(value,repo,config):
 errors=[]
 if value.get('schema_version')!=1 or value.get('range')!='0909-1019' or value.get('slug')!=config.slug or value.get('style')!='exam':errors.append('invalid scope or schema')
 q=value.get('questions',[])
 if [x.get('id') for x in q]!=[f'p{i}' for i in range(1,11)]:errors.append('exactly p1-p10 required')
 if Counter(x.get('kind') for x in q)!=Counter(homework_variant=5,model_analysis=5):errors.append('5:5 split required')
 ids=set()
 for s in value.get('sources',[]):
  if s['id'] in ids:errors.append('duplicate source')
  ids.add(s['id'])
  try:
   p=resolve(repo,s['path'])
   if sha(p)!=s['sha256']:errors.append('reference hash mismatch: '+s['id'])
   if p.suffix=='.md' and p.parent.name=='STT' and not '0909'<=p.name[:4]<='1019':errors.append('out of scope STT')
  except (OSError,ValueError) as exc:errors.append(str(exc))
 for x in q:
  if x.get('origin_kind') not in ('homework_variant','textbook_variant','theory_application'):errors.append('invalid origin')
  if not x.get('subparts') or len(set(x['subparts']))!=len(x['subparts']):errors.append('invalid subparts')
  for ref in x.get('theory_refs',[])+x.get('course_evidence',[]):
   if ref.get('source') not in ids:errors.append('unknown reference')
  if not x.get('origin_ref') or not x.get('assumptions'):errors.append('missing provenance or assumptions')
 return errors

def load_exam_source(cards_path,blueprint_path,repo,config):
 if Path(repo).resolve()!=config.repo:raise ValueError('repository/config mismatch')
 cards_path=resolve(repo,cards_path);blueprint_path=resolve(repo,blueprint_path)
 if unicodedata.normalize('NFC',cards_path.name)!=config.stem+'.html':raise ValueError('source identity mismatch')
 b=json.loads(Path(blueprint_path).read_text());errors=validate_blueprint(b,repo,config)
 if errors:raise ValueError('; '.join(errors))
 pack=read_cards(cards_path,config.profile);norm=normalize_cards(pack,None,cards_path)
 nodes=list(parse(Path(cards_path).read_text()).find_all(lambda n:n.tag=='article' and 'card' in n.classes))
 if [n.attrs.get('id') for n in nodes]!=[x['id'] for x in b['questions']]:raise ValueError('card ID mismatch')
 problems=[]
 for n,x,q in zip(nodes,b['questions'],norm):
  if n.attrs.get('data-origin-kind')!=x['origin_kind'] or n.attrs.get('data-origin-ref')!=x['origin_ref']:raise ValueError(q.card.id+': origin mismatch')
  parts=subparts(q.ask_html,q.card.original_html)
  if list(parts)!=x['subparts']:raise ValueError(q.card.id+': subparts mismatch')
  c=q.card;problems.append(Problem(c.id,int(c.id[1:]),c.title,c.source,c.original_html,q.conditions_html,q.ask_html,tuple(f.html for f in c.figures),c.steps,c.answer_html,parts))
 return SourcePack('exam',pack.range,pack.slug,Path(cards_path).resolve(),sha(cards_path),tuple(problems))

def assemble_cards(card_dir,target,config):
 cards='\n'.join((Path(card_dir)/f'p{i}.html').read_text() for i in range(1,11))
 Path(target).parent.mkdir(parents=True,exist_ok=True)
 Path(target).write_text(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{html.escape(config.title_ko)}</title></head><body><section id="exam">'+cards+'</section></body></html>')
 return Path(target)

def verify_baseline(repo,baseline_path):
 errors=[]
 for rel,digest in json.loads(Path(baseline_path).read_text(encoding='utf-8'))['files'].items():
  try:
   if sha(resolve(repo,rel))!=digest:errors.append('baseline changed: '+rel)
  except (OSError,ValueError) as e:errors.append('baseline '+rel+': '+str(e))
 return errors

def markup_resources(markups,base,repo):
 """Hash image dependencies, including local dependencies of referenced SVGs."""
 from urllib.parse import urlsplit,unquote
 from mpe_rerender import reference_dependencies
 resources={}
 def add(path):
  path=resolve(repo,Path(path).resolve())
  if str(path) in resources:return
  resources[str(path)]=sha(path)
  for child in reference_dependencies(path,Path(repo)):
   add(child)
 for markup in markups:
  for node in parse(markup).find_all(lambda n:n.tag in ('img','image')):
   value=node.attrs.get('src',node.attrs.get('href',node.attrs.get('xlink:href','')))
   url=urlsplit(value)
   if not url.path and url.fragment:continue
   if url.scheme or url.netloc or not url.path:raise ValueError('local image resource required')
   add(Path(base)/unquote(url.path))
 return resources

def explanation_resources(pack,fragments,repo):
 markups=list(fragments.values())
 for p in pack.problems:
  markups += [p.conditions_html,p.ask_html,p.original_html,*p.figures_html,*p.reference_steps,p.reference_answer]
 return markup_resources(markups,pack.path.parent,repo)
