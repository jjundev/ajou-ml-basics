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
from review_pdf_render import freeze_figures,render_workbook,measure_typography
from review_pdf_publish import publish_files
from review_pdf_layout import Layout,page_size_pt
from review_sources import find_review, review_dir, source_pdf
from review_pdf_types import BuildResult,ReviewPdfError,REVIEW,PROFILES


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _verify_pdf(path,expected_pages,layout: Layout):
    width,height=page_size_pt(layout)
    tolerance=.1 if layout=='video-16x9' else 72/25.4
    with fitz.open(path) as doc:
        if len(doc)!=expected_pages:raise ReviewPdfError(f'{path.name}: extra or missing PDF pages')
        for i,page in enumerate(doc,1):
            if abs(page.rect.width-width)>tolerance or abs(page.rect.height-height)>tolerance:raise ReviewPdfError(f'{path.name} page {i}: expected {layout}')
            if not page.get_text().strip():raise ReviewPdfError(f'{path.name} page {i}: blank page')
            if layout=='video-16x9':
                band=fitz.Rect(0,675,1440,810)
                def intrudes(rect):
                    r=fitz.Rect(rect)
                    return r.y1>675+.1 and r.y0<810 and r.x1>0 and r.x0<1440
                for block in page.get_text('dict')['blocks']:
                    # Chromium can rasterize page backgrounds into one full-page
                    # image, whose bbox also includes the untouched white band.
                    # The exact raster check below rejects any visible image ink.
                    for line in block.get('lines',[]):
                        for span in line['spans']:
                            if span['text'].strip() and intrudes(span['bbox']):raise ReviewPdfError(f'{path.name} page {i}: text in caption band')
                for drawing in page.get_drawings():
                    colors=[drawing[k] for k,opacity in [('color','stroke_opacity'),('fill','fill_opacity')] if drawing.get(k) is not None and drawing.get(opacity,1)>0]
                    if colors and any(any(c<1 for c in color) for color in colors) and intrudes(fitz.Rect(drawing['rect'])+(-(drawing.get('width') or 0)/2,-(drawing.get('width') or 0)/2,(drawing.get('width') or 0)/2,(drawing.get('width') or 0)/2)):raise ReviewPdfError(f'{path.name} page {i}: drawing in caption band')
                # Raster gate covers stroke joins, masks and paint beyond geometric bboxes.
                pixels=page.get_pixmap(clip=band,alpha=False)
                if min(pixels.samples)<255:raise ReviewPdfError(f'{path.name} page {i}: visible ink in caption band')


def build_pack(review_path,layouts_path,build_dir,*,layout: Layout="video-16x9",profile=REVIEW):
    size=page_size_pt(layout)
    review_path=Path(review_path).resolve()
    if profile == REVIEW and not review_path.exists() and review_path.suffix == ".html":
        review_path = find_review(review_path)
    source_hash=digest(review_path)
    pack=read_cards(review_path,profile)
    if layouts_path is None and review_path.name.endswith('.cards.json'):
        filename = f'{pack.range}_{pack.slug}.json'
        layouts_path = next((root / 'workbook/layouts' / filename for root in review_dir(review_path).parents
                             if (root / 'workbook/layouts' / filename).is_file()), None)
    layouts=json.loads(Path(layouts_path).read_text(encoding='utf-8')) if layouts_path else None
    problems=normalize_cards(pack,layouts,review_path)
    stage=Path(build_dir)/('run-'+uuid.uuid4().hex);stage.mkdir(parents=True,exist_ok=False)
    assets=freeze_figures(pack,stage/'figures')
    evidence={'status':'validated','profile':profile.name,'range':pack.range,'slug':pack.slug,'logical_count':len(pack.cards),'source_path':str(review_path),'source_sha256':source_hash,'pages':{},'pdfs':{},'errors':[],'layout':layout,'page_size_pt':size,'caption_height_px':180 if layout=='video-16x9' else 0,'typography':{}}
    results={}
    title=profile.title_fmt.format(range=pack.range);stem=profile.stem_fmt.format(range=pack.range,slug=pack.slug)
    for mode,suffix in [('problems','문제'),('answers','답안')]:
        counter=0
        def measure(pages):
            nonlocal counter
            counter+=1
            payload=to_workbook(problems,assets,mode,pages,profile);payload['meta']['title']=title
            scales=measure_typography(payload,mode,stage/f'{mode}-a4-{counter}.html') if layout=='video-16x9' else None
            return render_workbook(payload,mode,stage/f'{mode}-measure-{counter}.html',layout=layout,typography=scales)
        pages=paginate(problems,mode,measure)
        payload=to_workbook(problems,assets,mode,pages,profile);payload['meta']['title']=title
        pdf=stage/f'{stem}-{suffix}.pdf'
        scales=measure_typography(payload,mode,stage/f'{mode}-a4-final.html') if layout=='video-16x9' else None
        report=render_workbook(payload,mode,stage/f'{mode}.html',pdf,layout=layout,typography=scales)
        _verify_pdf(pdf,len(report.page_ids),layout)
        evidence['typography'][mode]=scales
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
    source = Path(evidence['source_path'])
    if digest(source)!=evidence['source_sha256']:raise ReviewPdfError('stale source before publication')
    for mode,path in [('problems',result.problems_pdf),('answers',result.answers_pdf)]:
        if digest(path)!=evidence['pdfs'][mode]['sha256']:raise ReviewPdfError(f'{mode}: staged PDF changed')
    files = {Path(pdf_dir)/p.name: p for p in (result.problems_pdf, result.answers_pdf)}
    expected = {source: evidence['source_sha256']}
    if source.name.endswith('.cards.json'):
        pdf = source_pdf(source, '문제').resolve()
        if pdf.is_file() and (Path(pdf_dir) / result.problems_pdf.name).resolve() == pdf:
            from review_pdf_links import problem_pages, relocate_problem_links

            expected[pdf] = digest(pdf)
            old_pages = problem_pages(pdf, read_cards(source).cards)
            new_pages = evidence['pages']['problems']
            moves = {page: new_pages[pid][0] for pid, page in old_pages.items() if new_pages.get(pid)}
            root = review_dir(source)
            stem = f"{evidence['range']}_{evidence['slug']}"
            revisions = result.report_path.parent / ('page-links-' + uuid.uuid4().hex)
            for prefix in ('정리노트', '문제설명'):
                for path in (root / f'{prefix}_{stem}.html', source.parent / f'{prefix}_{stem}.md'):
                    if not path.is_file():
                        continue
                    raw = path.read_bytes()
                    text = raw.decode('utf-8')
                    updated = relocate_problem_links(text, path, pdf, moves)
                    if updated != text:
                        revisions.mkdir(exist_ok=True)
                        staged = revisions / path.name
                        staged.write_text(updated, encoding='utf-8')
                        files[path] = staged
                        expected[path] = hashlib.sha256(raw).hexdigest()
    publish_files(files, backup_dir, expected_hashes=expected)


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--review',required=True,type=Path,help='work-stage card HTML or published .cards.json');ap.add_argument('--layouts',type=Path)
    ap.add_argument('--build-dir',required=True,type=Path);ap.add_argument('--pdf-dir',type=Path)
    ap.add_argument('--report',required=True,type=Path);ap.add_argument('--stage-only',action='store_true')
    ap.add_argument('--layout',choices=['a4','video-16x9'],default='video-16x9')
    ap.add_argument('--profile',choices=sorted(PROFILES),default='review')
    args=ap.parse_args(argv)
    if not args.pdf_dir and not args.stage_only:ap.error('--pdf-dir or --stage-only required')
    try:
        result=build_pack(args.review,args.layouts,args.build_dir,layout=args.layout,profile=PROFILES[args.profile])
        if not args.stage_only:publish_build(result,args.pdf_dir,args.build_dir/'backups')
        args.report.parent.mkdir(parents=True,exist_ok=True)
        if args.report.resolve()!=result.report_path.resolve():shutil.copy2(result.report_path,args.report)
        print(json.dumps({'problems_pdf':str(result.problems_pdf),'answers_pdf':str(result.answers_pdf),'report':str(args.report)},ensure_ascii=False))
        return 0
    except (ReviewPdfError,OSError,json.JSONDecodeError) as e:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps({'status':'failed','source_path':str(args.review.resolve()),'errors':[str(e)]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f'review PDF failed: {e}',file=sys.stderr);return 1
if __name__=='__main__':
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    sys.exit(main())
