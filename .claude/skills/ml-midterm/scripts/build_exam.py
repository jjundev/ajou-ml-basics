"""Build this exam through the unchanged course PDF and explanation APIs."""
from pathlib import Path
import sys,os,json,shutil,re,argparse,uuid,html
from exam_config import config_for_output
from exam_adapter import verify_baseline,assemble_cards,read_cards,normalize_cards,parse,outer,sha,load_exam_source,resolve,explanation_resources
from check_vector_derivatives import check_text
from review_pdf_payload import to_workbook

def problem_payload(source,config):
 p=read_cards(source,config.profile);return to_workbook(normalize_cards(p,None,source),{},'problems',profile=config.profile)

def styled_source(repo,output,stage,config):
 from assemble import fill
 raw=assemble_cards(output/'.pack/cards',stage/(config.stem+'.html'),config)
 root=parse(raw.read_text());cards=[]
 for node in root.find_all(lambda n:n.tag=='article' and 'card' in n.classes):
  sol=next(node.find_all(lambda n:'solution' in n.classes));sol.tag='details'
  # Add a native summary while preserving all authored solution steps.
  head=parse('<summary>참고 풀이와 답</summary>');sol.children.insert(0,head.children[0]);sol.children[0].parent=sol
  cards.append(outer(node))
 template=(repo/'.agents/skills/ml-review-pack/assets/review-template.html').read_text()
 from mpe_render import resolve_vendor_dir,verify_shared_vendor
 verify_shared_vendor(resolve_vendor_dir(repo))
 vendor_rel=Path(os.path.relpath((repo/'assets'/'vendor').resolve(),config.output.resolve())).as_posix()
 replacements={
 'https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.css':f'{vendor_rel}/pretendard/pretendard.css',
 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css':f'{vendor_rel}/katex/katex.min.css',
 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js':f'{vendor_rel}/katex/katex.min.js',
 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js':f'{vendor_rel}/katex/contrib/auto-render.min.js'}
 for a,b in replacements.items():template=template.replace(a,b)
 values={'PAGE_TITLE':config.title_ko,'DESCRIPTION':'0909–1019 직교투영까지, 10문항 실전 연습','TOC':''.join(f'<a href="#p{i}">{i}번</a>' for i in range(1,11)),'NOTE_HREF':f'문제설명_{config.range_}_{config.slug}.html','TITLE':f'중간고사 예상문제 {config.round_number}회','INTRO':'처음부터 1019 직교투영까지 · 10문항. 과제 변형 5문항과 모델 분석 5문항으로 구성한 연습 자료예요. Gaussian의 둘째 인수는 분산이며 gradient는 강의와 같이 행벡터예요.','PARTS':'<section id="exam"><h2>예상문제</h2>'+''.join(cards)+'</section>','FOOTER':'1019 STT의 약 50:50 안내를 반영한 추천 구성입니다. 실제 시험의 세부 문항·배점·시간은 확정하지 않습니다.','SCRIPTS':'','RANGE':f'exam-{config.range_}-{config.slug}'}
 text=fill(template,values).replace('>정리노트</a>','>문제설명</a>')
 errors=check_text(text)
 if errors:raise ValueError('; '.join(errors))
 raw.write_text(text,encoding='utf-8',newline='\n')
 return raw

def build_base(repo,output,run):
 from build_review_pdf import build_pack
 from review_pdf_publish import publish_files
 repo=Path(repo).resolve();output=Path(output).resolve();run=Path(run).resolve();run.mkdir(parents=True,exist_ok=True)
 config=config_for_output(repo,output)
 errors=verify_baseline(repo,Path(__file__).resolve().parents[1]/'references/baseline.json')
 if errors:raise ValueError('; '.join(errors))
 stage=run/('base-'+uuid.uuid4().hex);stage.mkdir()
 assets=repo/'.agents/skills/ml-review-pack/assets';provenance=json.loads((assets/'pdf-template-provenance.json').read_text())
 for v in provenance['templates'].values():
  if sha(assets/v['local_path'])!=v['sha256']:raise ValueError('pinned PDF template hash mismatch')
 source=styled_source(repo,output,stage,config);load_exam_source(source,output/'.pack/blueprint.json',repo,config)
 data=problem_payload(source,config)
 if any('solution' in p or p['hints'] for p in data['problems']):raise ValueError('problem payload leaks answer')
 snapshot=korean_pdf_source(source,stage/'.pack/evidence/korean-pdf-source'/source.name,config)
 result=build_pack(snapshot,None,run/('pdf-'+uuid.uuid4().hex),layout='video-16x9',profile=config.profile)
 from pdf_binding import korean_resource_hashes
 report=json.loads(result.report_path.read_text())
 report['korean_resources']=korean_resource_hashes(source,config)
 result.report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 mapping={output/source.name:source,output/result.problems_pdf.name:result.problems_pdf,output/result.answers_pdf.name:result.answers_pdf,output/'.pack/evidence/pdf-validation.json':result.report_path}
 mapping[output/snapshot.relative_to(stage)]=snapshot
 for p in snapshot.parent.rglob('*'):
  if p.is_file():mapping[output/p.relative_to(stage)]=p
 publish_files(mapping,run/('base-backup-'+uuid.uuid4().hex))
 from pdf_binding import binding_record
 binding=output/'.pack/evidence/korean-pdf-binding.json'
 binding_stage=stage/'korean-pdf-binding.json'
 binding_stage.write_text(json.dumps(binding_record(output,config),ensure_ascii=False,indent=2)+'\n')
 publish_files({binding:binding_stage},run/('binding-backup-'+uuid.uuid4().hex))
 value={'source':output/source.name,'problems_pdf':output/result.problems_pdf.name,'answers_pdf':output/result.answers_pdf.name,'pdf_validation':output/'.pack/evidence/pdf-validation.json'}
 (run/'base-result.json').write_text(json.dumps({k:str(v) for k,v in value.items()},ensure_ascii=False,indent=2)+'\n')
 return value


def korean_pdf_source(source,target,config):
 from pdf_binding import korean_content_digest
 root=parse(Path(source).read_text(encoding='utf-8'))
 for n in root.find_all(lambda n:n.tag=='article' and 'card' in n.classes):
  for original in n.find_all(lambda n:'original' in n.classes):original.children=[]
 target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
 src_vendor=Path(os.path.relpath((config.repo/'assets'/'vendor').resolve(),config.output.resolve())).as_posix()
 dest_dir=(config.output/'.pack/evidence/korean-pdf-source') if target.parent.name=='korean-pdf-source' else config.output
 snap_vendor=Path(os.path.relpath((config.repo/'assets'/'vendor').resolve(),dest_dir.resolve())).as_posix()
 text=outer(root).replace(f'{src_vendor}/',f'{snap_vendor}/')
 target.write_text(text,encoding='utf-8')
 if korean_content_digest(source,config)!=korean_content_digest(target,config):raise ValueError('Korean PDF projection changed content')
 # Preserve authored image URLs and card digests while mirroring their files.
 from urllib.parse import urlsplit,unquote
 from mpe_rerender import reference_dependencies
 sandbox=target.parent.parents[2] if target.parent.name=='korean-pdf-source' else target.parent
 copied=set()
 def copy_image(src,dst):
  src=resolve(config.repo,Path(src).resolve());dst=Path(dst).resolve()
  if not dst.is_relative_to(sandbox.resolve()) or dst==target.resolve():raise ValueError('image resource escapes PDF stage')
  if (src,dst) in copied:return
  copied.add((src,dst));dst.parent.mkdir(parents=True,exist_ok=True)
  if src!=dst:shutil.copy2(src,dst)
  for dep in reference_dependencies(src,config.repo):
   relative=__import__('os').path.relpath(dep,src.parent)
   copy_image(dep,dst.parent/relative)
 for node in root.find_all(lambda n:n.tag in ('img','image')):
  url=urlsplit(node.attrs.get('src',node.attrs.get('href',node.attrs.get('xlink:href',''))))
  if not url.path and url.fragment:continue
  if url.scheme or url.netloc or not url.path:raise ValueError('local PDF image resource required')
  rel=unquote(url.path);copy_image(config.output/rel,target.parent/rel)
 return target

def build_explain(repo,output,run):
 from mpe_render import build_explanation,artifact_hashes,dump
 from mpe_contract import initial_reviews
 from mpe_types import Artifacts
 repo=Path(repo).resolve();output=Path(output).resolve();run=Path(run).resolve()
 config=config_for_output(repo,output)
 errors=verify_baseline(repo,Path(__file__).resolve().parents[1]/'references/baseline.json')
 if errors:raise ValueError('; '.join(errors))
 pack=load_exam_source(output/(config.stem+'.html'),output/'.pack/blueprint.json',repo,config)
 fragments={p.id:(output/f'.pack/explanations/{p.id}.html').read_text() for p in pack.problems}
 errors=[f'{pid}: {e}' for pid,text in fragments.items() for e in check_text(text)]
 if errors:raise ValueError('; '.join(errors))
 stage=run/('explanation-'+uuid.uuid4().hex);art=build_explanation(pack,fragments,stage,repo)
 # Keep this exam's requested reader-facing title across rebuilds.
 for document in (art.html,art.md):
  old=f'머신러닝기초 복습 {config.range_} 문제설명'
  text=document.read_text()
  if text.count(old)!=(2 if document==art.html else 1):raise ValueError('explanation title replacement mismatch')
  document.write_text(text.replace(old,f'머신러닝기초 중간고사 모의평가 {config.round_number}회 문제설명'))
 manifest=json.loads(art.manifest.read_text());files=tuple(sorted(p for p in stage.rglob('*') if p.is_file() and p!=art.manifest));manifest['files']={p.relative_to(stage).as_posix():sha(p) for p in files};dump(art.manifest,manifest)
 art=Artifacts(art.html,art.md,art.manifest,files+(art.manifest,));review=initial_reviews(pack,fragments);review['artifact_hashes']=artifact_hashes(art)
 bp=json.loads((output/'.pack/blueprint.json').read_text());refs=[resolve(repo,x['path']) for x in bp['sources']]+[(output/'.pack/blueprint.json').resolve()]
 pins=json.loads((Path(__file__).resolve().parents[1]/'references/baseline.json').read_text())
 refs+= [resolve(repo,rel) for rel in pins['files']]
 resources=explanation_resources(pack,fragments,repo)
 refs+=[Path(path) for path in resources]
 refs=list(dict.fromkeys(refs))
 review['references']=[{'path':str(p),'sha256':sha(p)} for p in refs];review_path=run/'review.json';dump(review_path,review)
 dump(run/'explanation-result.json',{'stage':str(stage),'html':str(art.html),'md':str(art.md),'manifest':str(art.manifest),'files':[str(p) for p in art.files],'review_path':str(review_path),'source_sha256':pack.sha256,'fragments':{k:__import__('hashlib').sha256(v.encode()).hexdigest() for k,v in fragments.items()},'resources':resources,'output':str(output)})
 return {'pack':pack,'artifacts':art,'review_path':review_path}

def publish_explain(repo,output,run):
 from mpe_publish import publish_explanation
 from mpe_types import Artifacts
 from mpe_render import dump
 import hashlib
 repo=Path(repo).resolve();output=Path(output).resolve();run=Path(run).resolve()
 config=config_for_output(repo,output)
 errors=verify_baseline(repo,Path(__file__).resolve().parents[1]/'references/baseline.json')
 if errors:raise ValueError('; '.join(errors))
 index=json.loads((run/'explanation-result.json').read_text(encoding='utf-8'))
 if Path(index['output']).resolve()!=output:raise ValueError('run output mismatch')
 stage=resolve(repo,index['stage'])
 if not stage.is_relative_to(run):raise ValueError('stage outside run')
 fields=[resolve(repo,index[k]) for k in ('html','md','manifest')]
 files=tuple(resolve(repo,p) for p in index['files'])
 if any(not p.is_relative_to(stage) for p in fields+list(files)):raise ValueError('artifact outside stage')
 art=Artifacts(*fields,files)
 pack=load_exam_source(output/(config.stem+'.html'),output/'.pack/blueprint.json',repo,config)
 fragments={p.id:(output/f'.pack/explanations/{p.id}.html').read_text(encoding='utf-8') for p in pack.problems}
 if pack.sha256!=index['source_sha256'] or index['fragments']!={k:hashlib.sha256(v.encode()).hexdigest() for k,v in fragments.items()}:
  raise ValueError('stale source or fragments: rebuild and review')
 resources=explanation_resources(pack,fragments,repo)
 if resources!=index.get('resources',{}):raise ValueError('stale image resource: rebuild and review')
 review_path=resolve(repo,index['review_path'])
 if not review_path.is_relative_to(run):raise ValueError('review outside run')
 reviews=json.loads(review_path.read_text(encoding='utf-8'))
 recorded={str(resolve(repo,x['path'])):x['sha256'] for x in reviews.get('references',[])}
 if any(recorded.get(path)!=digest for path,digest in resources.items()):raise ValueError('image reference approval missing')
 published=publish_explanation(pack,art,fragments,reviews,output,run/('explanation-backup-'+uuid.uuid4().hex))
 dump(run/'publish-result.json',{'status':'explanation_published','files':[str(p) for p in published]})
 return published
