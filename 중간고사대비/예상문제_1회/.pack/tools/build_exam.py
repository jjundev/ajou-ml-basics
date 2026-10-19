"""Build this exam through the unchanged course PDF and explanation APIs."""
from pathlib import Path
import sys,json,shutil,re,argparse,uuid,html
from exam_adapter import EXAM,STEM,assemble_cards,read_cards,normalize_cards,parse,outer,sha,load_exam_source
from review_pdf_payload import to_workbook

def problem_payload(source):
 p=read_cards(source,EXAM);return to_workbook(normalize_cards(p,None,source),{},'problems',profile=EXAM)

def styled_source(repo,output,stage):
 from assemble import fill
 raw=assemble_cards(output/'.pack/cards',stage/(STEM+'.html'))
 root=parse(raw.read_text());cards=[]
 for node in root.find_all(lambda n:n.tag=='article' and 'card' in n.classes):
  sol=next(node.find_all(lambda n:'solution' in n.classes));sol.tag='details'
  # Add a native summary while preserving all authored solution steps.
  head=parse('<summary>참고 풀이와 답</summary>');sol.children.insert(0,head.children[0]);sol.children[0].parent=sol
  cards.append(outer(node))
 template=(repo/'.agents/skills/ml-review-pack/assets/review-template.html').read_text()
 vendor=stage/'.pack/source_vendor';shutil.copytree(repo/'.agents/skills/ml-problem-explain/assets/vendor',vendor)
 replacements={
 'https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.css':'.pack/source_vendor/pretendard/pretendard.css',
 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css':'.pack/source_vendor/katex/katex.min.css',
 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js':'.pack/source_vendor/katex/katex.min.js',
 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js':'.pack/source_vendor/katex/contrib/auto-render.min.js'}
 for a,b in replacements.items():template=template.replace(a,b)
 values={'PAGE_TITLE':'머신러닝기초 중간고사 예상문제 1회','DESCRIPTION':'0909–1019 직교투영까지, 10문항 실전 연습','TOC':''.join(f'<a href="#p{i}">{i}번</a>' for i in range(1,11)),'NOTE_HREF':'문제설명_0909-1019_Midterm_Practice_01.html','TITLE':'중간고사 예상문제 1회','INTRO':'처음부터 1019 직교투영까지 · 10문항. 과제 변형 5문항과 모델 분석 5문항으로 구성한 연습 자료예요. Gaussian의 둘째 인수는 분산이며 gradient는 열벡터예요.','PARTS':'<section id="exam"><h2>예상문제</h2>'+''.join(cards)+'</section>','FOOTER':'1019 STT의 약 50:50 안내를 반영한 추천 구성입니다. 실제 시험의 세부 문항·배점·시간은 확정하지 않습니다.','SCRIPTS':'','RANGE':'exam-0909-1019-Midterm_Practice_01'}
 text=fill(template,values).replace('>정리노트</a>','>문제설명</a>');raw.write_text(text)
 return raw

def build_base(repo,output,run):
 from build_review_pdf import build_pack
 from review_pdf_publish import publish_files
 repo=Path(repo).resolve();output=Path(output).resolve();run=Path(run).resolve();run.mkdir(parents=True,exist_ok=True)
 stage=run/('base-'+uuid.uuid4().hex);stage.mkdir()
 assets=repo/'.agents/skills/ml-review-pack/assets';provenance=json.loads((assets/'pdf-template-provenance.json').read_text())
 for v in provenance['templates'].values():
  if sha(assets/v['local_path'])!=v['sha256']:raise ValueError('pinned PDF template hash mismatch')
 source=styled_source(repo,output,stage);load_exam_source(source,output/'.pack/blueprint.json',repo)
 data=problem_payload(source)
 if any('solution' in p or p['hints'] for p in data['problems']):raise ValueError('problem payload leaks answer')
 result=build_pack(source,None,run/'pdf',layout='video-16x9',profile=EXAM)
 mapping={output/source.name:source,output/result.problems_pdf.name:result.problems_pdf,output/result.answers_pdf.name:result.answers_pdf,output/'.pack/evidence/pdf-validation.json':result.report_path}
 for p in (stage/'.pack/source_vendor').rglob('*'):
  if p.is_file():mapping[output/p.relative_to(stage)]=p
 publish_files(mapping,run/('base-backup-'+uuid.uuid4().hex))
 value={'source':output/source.name,'problems_pdf':output/result.problems_pdf.name,'answers_pdf':output/result.answers_pdf.name,'pdf_validation':output/'.pack/evidence/pdf-validation.json'}
 (run/'base-result.json').write_text(json.dumps({k:str(v) for k,v in value.items()},ensure_ascii=False,indent=2)+'\n')
 return value

def build_explain(repo,output,run):
 from mpe_render import build_explanation,artifact_hashes,dump
 from mpe_contract import initial_reviews
 from mpe_types import Artifacts
 repo=Path(repo).resolve();output=Path(output).resolve();run=Path(run).resolve()
 pack=load_exam_source(output/(STEM+'.html'),output/'.pack/blueprint.json',repo)
 fragments={p.id:(output/f'.pack/explanations/{p.id}.html').read_text() for p in pack.problems}
 stage=run/('explanation-'+uuid.uuid4().hex);art=build_explanation(pack,fragments,stage,repo)
 # Keep this exam's requested reader-facing title across rebuilds.
 for document in (art.html,art.md):
  document.write_text(document.read_text().replace('머신러닝기초 복습 0909-1019 문제설명','머신러닝기초 중간고사 모의평가 1회 문제설명'))
 for src in (output/'.pack/evidence').rglob('*'):
  if src.is_file():
   dest=art.manifest.parent/'evidence'/src.relative_to(output/'.pack/evidence');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
 manifest=json.loads(art.manifest.read_text());files=tuple(sorted(p for p in stage.rglob('*') if p.is_file() and p!=art.manifest));manifest['files']={p.relative_to(stage).as_posix():sha(p) for p in files};dump(art.manifest,manifest)
 art=Artifacts(art.html,art.md,art.manifest,files+(art.manifest,));review=initial_reviews(pack,fragments);review['artifact_hashes']=artifact_hashes(art)
 bp=json.loads((output/'.pack/blueprint.json').read_text());refs=[(repo/x['path']).resolve() for x in bp['sources']]+[(output/'.pack/blueprint.json').resolve()]
 review['references']=[{'path':str(p),'sha256':sha(p)} for p in refs];review_path=run/'review.json';dump(review_path,review)
 dump(run/'explanation-result.json',{'stage':str(stage),'html':str(art.html),'md':str(art.md),'manifest':str(art.manifest),'files':[str(p) for p in art.files],'review_path':str(review_path)})
 return {'pack':pack,'artifacts':art,'review_path':review_path}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('command',choices=['base','explain']);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--run',type=Path,required=True);a=ap.parse_args()
 result=(build_base if a.command=='base' else build_explain)(a.repo,a.out,a.run)
 print(json.dumps({k:str(v) for k,v in result.items() if k not in ('pack','artifacts')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
