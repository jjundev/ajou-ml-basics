#!/usr/bin/env python3
"""Build and validate a review workbook pair in a private staging directory."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys
import uuid
import fitz
from review_pdf_cards import read_cards,normalize_cards
from review_pdf_payload import to_workbook,page_id
from review_pdf_pages import paginate
from review_pdf_render import freeze_figures,render_workbook
from review_pdf_publish import publish_files
from review_pdf_types import BuildResult,ReviewPdfError


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _verify_pdf(path,expected_pages):
    with fitz.open(path) as doc:
        if len(doc)!=expected_pages:raise ReviewPdfError(f'{path.name}: extra or missing PDF pages')
        for i,page in enumerate(doc,1):
            if abs(page.rect.width*25.4/72-297)>1 or abs(page.rect.height*25.4/72-210)>1:raise ReviewPdfError(f'{path.name} page {i}: expected A4 landscape')
            if not page.get_text().strip():raise ReviewPdfError(f'{path.name} page {i}: blank page')


def build_pack(review_path,layouts_path,build_dir):
    review_path=Path(review_path).resolve()
    source_hash=digest(review_path)
    pack=read_cards(review_path)
    layouts=json.loads(Path(layouts_path).read_text(encoding='utf-8')) if layouts_path else None
    problems=normalize_cards(pack,layouts,review_path)
    stage=Path(build_dir)/('run-'+uuid.uuid4().hex);stage.mkdir(parents=True,exist_ok=False)
    assets=freeze_figures(pack,stage/'figures')
    evidence={'status':'validated','range':pack.range,'slug':pack.slug,'logical_count':len(pack.cards),'source_path':str(review_path),'source_sha256':source_hash,'pages':{},'pdfs':{},'errors':[]}
    results={}
    for mode,suffix in [('problems','문제'),('answers','답안')]:
        counter=0
        def measure(pages):
            nonlocal counter
            counter+=1
            payload=to_workbook(problems,assets,mode,pages);payload['meta']['title']=f'머신러닝기초 복습문제 {pack.range}'
            return render_workbook(payload,mode,stage/f'{mode}-measure-{counter}.html')
        pages=paginate(problems,mode,measure)
        payload=to_workbook(problems,assets,mode,pages);payload['meta']['title']=f'머신러닝기초 복습문제 {pack.range}'
        pdf=stage/f'복습문제_{pack.range}_{pack.slug}-{suffix}.pdf'
        report=render_workbook(payload,mode,stage/f'{mode}.html',pdf)
        _verify_pdf(pdf,len(report.page_ids))
        mapping={c.id:[] for c in pack.cards}
        for i,p in enumerate(pages,1):mapping[p.logical_id].append(i)
        evidence['pages'][mode]=mapping
        evidence['pdfs'][mode]={'path':str(pdf),'sha256':digest(pdf),'page_count':len(report.page_ids),'page_ids':list(report.page_ids),'issues':[]}
        results[mode]=pdf
    if digest(review_path)!=source_hash:raise ReviewPdfError(f'{pack.range}: stale source changed during build')
    report_path=stage/'validation.json';report_path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return BuildResult(results['problems'],results['answers'],report_path)


def publish_build(result,pdf_dir,backup_dir):
    evidence=json.loads(result.report_path.read_text(encoding='utf-8'))
    if digest(evidence['source_path'])!=evidence['source_sha256']:raise ReviewPdfError('stale source before publication')
    for mode,path in [('problems',result.problems_pdf),('answers',result.answers_pdf)]:
        if digest(path)!=evidence['pdfs'][mode]['sha256']:raise ReviewPdfError(f'{mode}: staged PDF changed')
    publish_files({Path(pdf_dir)/p.name:p for p in [result.problems_pdf,result.answers_pdf]},backup_dir)


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--review',required=True,type=Path);ap.add_argument('--layouts',type=Path)
    ap.add_argument('--build-dir',required=True,type=Path);ap.add_argument('--pdf-dir',type=Path)
    ap.add_argument('--report',required=True,type=Path);ap.add_argument('--stage-only',action='store_true')
    args=ap.parse_args(argv)
    if not args.pdf_dir and not args.stage_only:ap.error('--pdf-dir or --stage-only required')
    try:
        result=build_pack(args.review,args.layouts,args.build_dir)
        if not args.stage_only:publish_build(result,args.pdf_dir,args.build_dir/'backups')
        args.report.parent.mkdir(parents=True,exist_ok=True)
        if args.report.resolve()!=result.report_path.resolve():shutil.copy2(result.report_path,args.report)
        print(json.dumps({'problems_pdf':str(result.problems_pdf),'answers_pdf':str(result.answers_pdf),'report':str(args.report)},ensure_ascii=False))
        return 0
    except (ReviewPdfError,OSError,json.JSONDecodeError) as e:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps({'status':'failed','source_path':str(args.review.resolve()),'errors':[str(e)]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f'review PDF failed: {e}',file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
