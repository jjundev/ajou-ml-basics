from dataclasses import replace
from pathlib import Path
import json, re
import pytest

def source_for(exam):
    from exam_adapter import assemble_cards
    return assemble_cards(exam.output / '.pack/cards', exam.output / (exam.stem + '.html'), exam)

def test_base_payload_has_no_answers(exam):
    from build_exam import problem_payload
    data = problem_payload(source_for(exam), exam)
    assert len(data['problems']) == 10
    assert all('solution' not in p and not p['hints'] and not p.get('answer') for p in data['problems'])
    assert all(p['html']['ask'] and p['html']['conditions'] for p in data['problems'])

def test_round_two_english_and_dynamic_subparts(repo, exam):
    from english_source import load_english_problems, english_payload
    from exam_adapter import parse, outer
    source = source_for(exam)
    root = parse(source.read_text())
    card = next(root.find_all(lambda n:n.attrs.get('id') == 'p1'))
    for attr, cls in [('data-english-ask', None), (None, 'ask')]:
        block = next(card.find_all(lambda n: attr in n.attrs if attr else cls in n.classes))
        ol = next(block.find_all(lambda n:n.tag == 'ol'))
        lis = [n for n in ol.children if not isinstance(n,str) and n.tag == 'li']
        ol.children.remove(lis[-1])
    source.write_text(outer(root))
    bp = exam.output / '.pack/blueprint.json'; b = json.loads(bp.read_text())
    b['questions'][0]['subparts'].pop(); bp.write_text(json.dumps(b))
    ps = load_english_problems(source, bp, repo, exam)
    assert sum(len(re.findall('data-english-part=', p.ask_html)) for p in ps) == 41
    data = english_payload(ps, exam)
    assert data['meta']['title'].endswith('02')
    assert all(p['section'] == 'Midterm Practice 02' for p in data['problems'])

@pytest.mark.parametrize('mutation', ['missing','duplicate','korean','reorder','override'])
def test_english_missing_or_reordered_parts_rejected(repo, exam, mutation):
    from english_source import load_english_problems
    source = source_for(exam); text = source.read_text()
    if mutation == 'missing': text = text.replace('data-english-title','data-no-title',1)
    if mutation == 'duplicate': text = text.replace('</h4>','</h4><h4 data-english-title>Duplicate</h4>',1)
    if mutation == 'korean': text = text.replace('data-english-title>','data-english-title>한글',1)
    if mutation == 'reorder': text = text.replace('data-english-part="a"','data-english-part="z"',1)
    if mutation == 'override': text = text.replace('data-english-part="a"','value="2" data-english-part="a"',1)
    source.write_text(text)
    with pytest.raises(ValueError): load_english_problems(source, exam.output / '.pack/blueprint.json', repo, exam)

def test_korean_pdf_projection_preserves_full_source(exam):
    from build_exam import korean_pdf_source
    from pdf_binding import korean_content_digest, binding_record, check_pdf_binding
    from exam_adapter import sha, read_cards
    source = source_for(exam); before = sha(source)
    e = exam.output / '.pack/evidence'; snapshot = e / 'korean-pdf-source' / source.name
    korean_pdf_source(source, snapshot, exam)
    assert sha(source) == before
    assert all(c.original_html.strip() for c in read_cards(source, exam.profile).cards)
    assert all(not c.original_html.strip() for c in read_cards(snapshot, exam.profile).cards)
    assert korean_content_digest(source, exam) == korean_content_digest(snapshot, exam)
    report = {'source_sha256':sha(snapshot),'logical_count':10,'pdfs':{}}
    for mode,suffix in [('problems','-문제.pdf'),('answers','-답안.pdf')]:
        p = exam.output / (exam.stem + suffix); p.write_bytes(mode.encode())
        report['pdfs'][mode] = {'sha256':sha(p)}
    (e/'pdf-validation.json').write_text(json.dumps(report))
    (e/'korean-pdf-binding.json').write_text(json.dumps(binding_record(exam.output, exam)))
    assert check_pdf_binding(exam.output, exam.repo, exam) == []
    snapshot.write_text(snapshot.read_text() + 'changed')
    assert check_pdf_binding(exam.output, exam.repo, exam)

@pytest.mark.pdf
def test_pdf_layout_and_long_continuation(repo, exam, tmp_path):
    from english_source import load_english_problems
    from english_pdf import build_problems
    import fitz
    ps = list(load_english_problems(source_for(exam), exam.output/'.pack/blueprint.json', repo, exam))
    p = ps[7]
    ask = re.sub(r'(<li[^>]*>)([\s\S]*?)(</li>)',lambda m:m[1]+m[2]+('<p>'+m[2]+'</p>')*3+m[3],p.ask_html)
    ps[7] = replace(p, ask_html=ask)
    pdf, report = build_problems(repo, ps, tmp_path/'long', exam)
    assert pdf.name.endswith('Midterm_Practice_02-문제-English.pdf')
    assert len(report['pages']['p8']) > 1
    with fitz.open(pdf) as doc:
        labels = [x for n in report['pages']['p8'] for x in re.findall(r'(?m)^\s*([a-f])\.\s*$',doc[n-1].get_text())]
        assert labels == list('abcdef')
        for page in doc:
            assert (page.rect.width, page.rect.height) == (1440,810)
            assert min(page.get_pixmap(clip=fitz.Rect(0,675,1440,810),alpha=False).samples) == 255
