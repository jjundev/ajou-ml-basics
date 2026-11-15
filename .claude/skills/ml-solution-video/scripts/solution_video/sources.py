from pathlib import Path
import calendar,copy,re,shutil,unicodedata
from urllib.parse import unquote,urlparse
from .contracts import InputError
from .util import file_hash,write,digest
from .ml_cards import read_cards
from review_sources import discover_reviews, html_name, review_dir, source_markdown, source_pdf
from .page_pairs import map_pages,normalize_id,compare_conditions

def _norm(s):return unicodedata.normalize('NFC',s)
def _dates(selector):
 dates=selector.split('-')
 def valid(s):return len(s)==4 and s.isdigit() and 1<=int(s[:2])<=12 and 1<=int(s[2:])<=calendar.monthrange(2024,int(s[:2]))[1]
 if len(dates)>2 or not all(valid(d) for d in dates) or dates[0]>dates[-1]:raise InputError('invalid date selector: '+selector)
 return dates[0],dates[-1]
def _find(parent,name):
 matches=[p for p in Path(parent).iterdir() if _norm(p.name)==_norm(name)]
 if len(matches)!=1:raise InputError('missing or ambiguous source: '+name)
 return matches[0]
def discover(repo,selector,problem_ids=None,failures=None,*,pack=None,page_map=None):
 repo=Path(repo).resolve();lo,hi=_dates(selector);root=_find(repo,'복습노트');packs=[];cross=[]
 for p in discover_reviews(root):
  m=re.fullmatch(r'복습문제_(\d{4}(?:-\d{4})?)_([A-Za-z0-9_]+)\.html',html_name(p))
  if not m:continue
  a,b=_dates(m[1])
  if b<lo or a>hi:continue
  if pack and _norm(m[2])!=_norm(pack):continue
  if not (lo<=a and b<=hi) and not pack:cross.append(m[1]);continue
  packs.append((p,m[1],m[2]))
 if cross:raise InputError('boundary-crossing pack requires --pack: '+str(cross))
 if not packs:raise InputError('selected date/pack missing')
 identities=[(_norm(date),_norm(slug)) for _,date,slug in packs]
 if len(set(identities))!=len(identities):raise InputError('duplicate normalized pack identity')
 by_range={}
 for _,date,slug in packs:by_range.setdefault(date,[]).append(slug)
 if not pack and any(len(v)>1 for v in by_range.values()):raise InputError('ambiguous packs; specify --pack')
 requested=[]
 for ident in problem_ids or []:
  bits=ident.split(':');requested.append((bits[0] if len(bits)==2 else None,normalize_id(bits[-1])))
 if any(d is None for d,_ in requested) and len(packs)>1:raise InputError('ambiguous Pn; use date:Pn')
 bundles=[];matched=set()
 def fail(pid,date,slug,reason):
  if failures is None:raise InputError(reason)
  failures.append(dict(key=f'{date}:{slug}:{pid}' if pid else None,pack_id=f'{date}:{slug}',problem_id=pid,reason=reason))
 for html,date,slug in packs:
  try:
   card_errors=[];cards=read_cards(html,[n for d,n in requested if d is None or d==date] if requested else None,errors=card_errors if failures is not None else None)
   for error in card_errors:fail(error['problem_id'],date,slug,error['reason']);matched.update((d,n) for d,n in requested if n==error['problem_id'] and (d is None or d==date))
  except (OSError,ValueError,InputError) as ex:fail(None,date,slug,str(ex));continue
  for card in cards:
   pid=card['id'];selections=[(d,n) for d,n in requested if n==pid and (d is None or d==date)]
   if requested and not selections:continue
   matched.update(selections)
   try:
    md=source_markdown(html);pp=source_pdf(html,'문제');ap=source_pdf(html,'답안')
    source_kind = 'cards' if html.name.endswith('.cards.json') else 'html'
    sources={source_kind:str(html.resolve()), 'md':str(md.resolve()), 'problem_pdf':str(pp.resolve()), 'answer_pdf':str(ap.resolve())}
    for relative in card['figure_paths']:
     u=urlparse(relative)
     if u.scheme or u.netloc:raise InputError('remote figure requires frozen local source')
     target=(review_dir(html)/unquote(u.path)).resolve()
     if not target.is_relative_to(repo) or target.name.startswith('.') or target.suffix.lower() not in ('.svg','.png','.jpg','.jpeg','.webp'):raise InputError('unsafe source figure')
     if not target.is_file():raise InputError('figure missing: '+relative)
     sources['figure:'+relative]=str(target)
    explicit=(page_map or {}).get('problems',{}).get(f'{date}:{slug}:{pid}')
    problem_pages,answer_pages=map_pages(card,pp,ap,explicit=explicit)
    compare_conditions(problem_pages,answer_pages)
    bundles.append(dict(schema_version=2,key=f'{date}:{slug}:{pid}',pack_id=f'{date}:{slug}',range=date,slug=slug,problem_id=pid,title=card['title'],mml_source=card['source'],problem_pages=problem_pages,answer_pages=answer_pages,source_files=sources,card=card))
   except (InputError,OSError,ValueError,RuntimeError) as ex:fail(pid,date,slug,str(ex))
 if set(requested)-matched:raise InputError('problem IDs outside range: '+str(set(requested)-matched))
 return bundles

def freeze_sources(bundles,batch):
 batch=Path(batch);dest=batch/'source/snapshots';dest.mkdir(parents=True,exist_ok=True);result=copy.deepcopy(bundles);provenance={}
 def freeze(path):
  src=Path(path);sha=file_hash(src);target=dest/(sha+src.suffix)
  if target.exists() and file_hash(target)!=sha:raise InputError('corrupt frozen source')
  if not target.exists():shutil.copyfile(src,target)
  rel=target.relative_to(batch).as_posix();provenance.setdefault(rel,dict(original=str(src.resolve()),sha256=sha));return rel
 for b in result:
  b['source_files']={k:freeze(v) for k,v in b['source_files'].items()}
  for ref in b['problem_pages']+b['answer_pages']:ref['snapshot']=freeze(ref['snapshot'])
 import fitz,sys
 write(batch/'source/inputs.json',dict(files=provenance,bundles=result,tools=dict(python=sys.version,pymupdf=fitz.VersionBind)))
 return result

def validate_pairs(pairs):
 """Compatibility validator for private single-page tests; ML discovery uses bundles."""
 import fitz
 seen={}
 for pair in pairs:
  texts=[]
  for role in ('problem','answer'):
   ref=pair[role]
   with fitz.open(ref['snapshot']) as d:
    p=d[ref['page_index']];panels=[x['rect'] for x in p.get_drawings() if x.get('fill') and max(abs(a-b) for a,b in zip(x['fill'],(246/255,246/255,243/255)))<.002]
    text=p.get_text(clip=max(panels,key=lambda r:r.get_area()) if panels else fitz.Rect(0,60,p.rect.width, p.rect.height-30))
   texts.append(re.sub(r'\s+','',_norm(text)))
  if texts[0]!=texts[1]:raise InputError('problem/answer conditions differ')
  if pair['problem_id'] in seen and seen[pair['problem_id']]!=texts[1]:raise InputError('different answers')
  seen[pair['problem_id']]=texts[1]
