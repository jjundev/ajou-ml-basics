"""Verify the complete generated note against a pre-change snapshot."""
from pathlib import Path
import sys,json,re,hashlib,runpy,shutil
repo=Path.cwd();sys.path.insert(0,str(repo/'.agents/skills/ml-problem-explain/scripts'))
from mpe_shared import parse,inner,compact
from mpe_labels import normalize_subpart_labels
folder=Path(__file__).parent.parent
meta=json.loads((folder/'stage.json').read_text());stage=folder/meta['stage']
baseline=Path(sys.argv[1]);data='자료_문제설명_hw1_Homework1'
result={'problems':0,'removed':0,'duplicate_prefixes':0,'math_preserved':True,'references_preserved':True,'idempotent':True}
for oldfile in (baseline/'fragments').glob('p*.html'):
 before=parse(oldfile.read_text());aftertext=(stage/data/'fragments'/oldfile.name).read_text();after=parse(aftertext)
 result['problems']+=1
 assert normalize_subpart_labels(aftertext)==aftertext
 oldparts=list(before.find_all(lambda n:'data-subpart' in n.attrs));newparts=list(after.find_all(lambda n:'data-subpart' in n.attrs))
 assert [(n.attrs,n.tag) for n in oldparts]==[(n.attrs,n.tag) for n in newparts]
 op=list(before.find_all(lambda n:n.tag=='p'));np=list(after.find_all(lambda n:n.tag=='p'));assert len(op)==len(np)
 for a,b in zip(op,np):
  parent=a.parent
  while parent and 'data-subpart' not in parent.attrs:parent=parent.parent
  expected=a.text()
  if parent and re.fullmatch('[a-z]',parent.attrs['data-subpart']):
   expected=re.sub(r'^\s*\('+parent.attrs['data-subpart']+r'\)\s+','',expected,count=1)
  assert expected==b.text(),(oldfile.name,a.text(),b.text())
  result['removed']+=a.text()!=b.text()
 assert re.findall(r'\$\$.*?\$\$|\$[^$]*\$',before.text(),re.S)==re.findall(r'\$\$.*?\$\$|\$[^$]*\$',after.text(),re.S)
 for block in newparts:
  for p in block.find_all(lambda n:n.tag=='p'):
   if re.match(r'^\s*\('+re.escape(block.attrs['data-subpart'])+r'\)\s+',p.text()):result['duplicate_prefixes']+=1
old=parse((baseline/meta['html']).read_text());new=parse((stage/meta['html']).read_text())
for attr in ['data-source-problem','data-original-problem']:
 a=list(old.find_all(lambda n:attr in n.attrs));b=list(new.find_all(lambda n:attr in n.attrs))
 assert len(a)==len(b)==25
 assert [compact(inner(n)) for n in a]==[compact(inner(n)) for n in b]
# Every mathematical expression in the entire document is unchanged.
assert re.findall(r'\$\$.*?\$\$|\$[^$]*\$',old.text(),re.S)==re.findall(r'\$\$.*?\$\$|\$[^$]*\$',new.text(),re.S)
for path,digest in json.loads((folder/'evidence/protected-hashes.json').read_text()).items():
 assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
# Rerun the actual assignment author on an isolated extracted source.
authorrun=folder/'author-regeneration';authorrun.mkdir(exist_ok=True);(authorrun/'explanations').mkdir(exist_ok=True)
shutil.copy2(folder/'source.json',authorrun/'source.json')
saved=sys.argv;sys.argv=['author.py',str(authorrun)]
try:runpy.run_path(str(folder/'evidence/author.py'),run_name='__main__')
finally:sys.argv=saved
for file in (authorrun/'explanations').glob('p*.html'):
 assert normalize_subpart_labels(file.read_text())==file.read_text()
result['author_regeneration_problems']=len(list((authorrun/'explanations').glob('p*.html')))
assert result['problems']==25 and result['removed']==70 and result['duplicate_prefixes']==0 and result['author_regeneration_problems']==25
# Check Markdown paragraphs inside solve/verify subpart headings independently.
md=(stage/meta['md']).read_text();inside_section=False;label=None;bad=[]
for line in md.splitlines():
 if line.startswith('#### '):
  title=line[5:]
  if title in ['한 단계씩 계산해요','다른 길로 검산해요']:inside_section=True;label=None
  elif (m:=re.match(r'^\(([a-z])\)(?: 검산)?$',title)):label=m[1] if inside_section else None
  else:inside_section=False;label=None
 elif inside_section and label and re.match(r'^\('+label+r'\)\s+',line):bad.append(line)
assert not bad,bad
result['markdown_duplicate_prefixes']=len(bad)
(folder/'evidence/label-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
