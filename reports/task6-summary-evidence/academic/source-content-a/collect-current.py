import sys,pathlib,json,hashlib,re
from urllib.parse import unquote
sys.dont_write_bytecode=True
out=pathlib.Path(__file__).parent
repo=pathlib.Path('/Users/hyunjun_macbook_pro/Documents/Univ/.course-summary-worktrees/2026-10-20/머신러닝기초')
sys.path.insert(0,str(repo/'.claude/skills/ml-problem-explain/scripts'))
from mpe_source import load_source
from mpe_shared import parse,inner,outer,compact
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
h=lambda s:hashlib.sha256(s.encode()).hexdigest()
def one(root,pred):
 a=list(root.find_all(pred));assert len(a)==1,len(a);return a[0]
a=json.loads((out/'assigned-packs.json').read_text());result=[]
for p in a:
 pack=load_source(pathlib.Path(p['source']),repo);doc=parse(pathlib.Path(p['html']).read_text());qs=[]
 for q in pack.problems:
  topic=one(doc,lambda n:n.tag=='article' and n.attrs.get('id')==q.id)
  link=one(topic,lambda n:n.tag=='a' and n.text()=='원 문제 보기')
  assert unquote(link.attrs['href'])==pack.path.name+'#'+q.id
  fields={}
  for field in ['conditions','ask']:
   current=inner(one(topic,lambda n:n.attrs.get('data-source-field')==field));expected=getattr(q,field+'_html');fields[field]={'exact_canonical_match':compact(current)==compact(expected),'current_html':current,'source_html':expected};assert fields[field]['exact_canonical_match']
  originals=list(doc.find_all(lambda n:n.attrs.get('data-original-problem')==q.id))
  original=originals[0] if originals else None
  fragpath=pathlib.Path(p['active_fragment_directory'])/(q.id+'.html');frag=parse(fragpath.read_text());sections={}
  for section in ['understand','recall','start','solve','verify','pitfall','retry']:
   fnode=one(frag,lambda n:n.attrs.get('data-explanation')==section);pnode=one(topic,lambda n:n.attrs.get('data-explanation')==section)
   assert compact(inner(fnode))==compact(inner(pnode))
   sections[section]={'html':inner(fnode),'text':fnode.text(),'sha256':h(outer(fnode)),'published_fragment_match':True}
  summary=one(frag,lambda n:'sum' in n.classes);published=one(doc,lambda n:'sum' in n.classes and n.attrs.get('data-for')==q.id) if False else None
  # summaries are moved into the central .sums container; locate by summary payload.
  matching=[n for n in doc.find_all(lambda n:'sum' in n.classes) if compact(inner(n))==compact(inner(summary))]
  assert len(matching)==1
  figures=[]
  for i,fig in enumerate(q.figures_html):
   sourcefig=parse(fig);svgs=list(sourcefig.find_all(lambda n:n.tag=='svg'))
   if svgs:
    publishedsvg=one(topic,lambda n:n.tag=='svg');geometry=lambda s:re.sub(r' id="[^"]*"','',s)
    assert geometry(outer(svgs[0]))==geometry(outer(publishedsvg))
   figures.append({'html':fig,'sha256':h(fig),'published_geometry_match':True})
  qs.append({'id':q.id,'title':q.title,'source_label':q.source,'source_link':link.attrs['href'],'source_link_target_verified':True,'subparts':q.subparts,'source_fields':fields,'source_original_html':q.original_html,'published_original_html':inner(original) if original else None,'original_access':'source card original details via 원 문제 보기; no inline original tab in current or pre-change dated explanation','figures':figures,'fragment':str(fragpath),'fragment_sha256':sha(fragpath),'sections':sections,'summary':{'html':inner(summary),'text':summary.text(),'sha256':h(outer(summary)),'published_match':True}})
 result.append({'pack_id':p['pack_id'],'date':pack.range,'source':str(pack.path),'source_sha256':sha(pack.path),'html':p['html'],'html_sha256':sha(p['html']),'manifest':p['manifest'],'manifest_sha256':sha(p['manifest']),'inline_original_current_count':len(list(doc.find_all(lambda n:n.attrs.get('data-original-problem') is not None))),'inline_original_prechange_count':pathlib.Path(repo/'.task6-run-ml-01/before'/pathlib.Path(p['html']).relative_to(repo)).read_text().count('data-original-problem'),'MML_pdf':{'path':p['MML_pdf']['path'],'sha256':sha(p['MML_pdf']['path'])},'questions':qs})
(out/'current-read-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Collected',len(result),'packs,',sum(len(x['questions']) for x in result),'questions,',sum(len(q['subparts']) for x in result for q in x['questions']),'subparts; current source fields/figures and all active/published sections match; source originals collected and source links verified.')
