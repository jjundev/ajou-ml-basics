from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from review_sources import archive_cards, source_pdf, find_review
from review_pdf_cards import read_cards
from review_pdf_publish import publish_pack

FIXTURE = SCRIPTS.parent / 'tests/fixtures/pdf/복습문제_0101_Pdf_Test.html'


def test_archive_preserves_cards_after_html_removal(tmp_path):
    html = tmp_path / FIXTURE.name
    html.write_bytes(FIXTURE.read_bytes())
    original = read_cards(html)
    data = archive_cards(html)
    html.unlink()
    assert find_review(html) == data
    assert read_cards(data).cards == original.cards
    pdf = html.with_name(html.stem + '-문제.pdf')
    pdf.write_bytes(b'legacy-root')
    assert source_pdf(data, '문제') == pdf


def test_source_pdf_prefers_date_folder_and_can_read_older_packs(tmp_path):
    html = tmp_path / FIXTURE.name
    html.write_bytes(FIXTURE.read_bytes())
    data = archive_cards(html)
    pdf = html.with_name(html.stem + '-문제.pdf')
    packed = data.parent / pdf.name
    packed.write_bytes(b'packed')
    assert source_pdf(data, '문제') == packed
    pdf.write_bytes(b'current')
    assert source_pdf(data, '문제') == pdf


def test_publish_omits_private_review_html(tmp_path):
    stage = tmp_path / 'stage'
    stage.mkdir()
    note = stage / '정리노트_0101_Pdf_Test.html'
    note.write_text('<p>test</p>')
    html = stage / FIXTURE.name
    html.write_bytes(FIXTURE.read_bytes())
    storage = stage / '.pack'
    storage.mkdir()
    for name in (note.with_suffix('.md').name, html.with_suffix('.md').name):
        (storage / name).write_text(name)
    pdfs = [html.stem + '-문제.pdf', html.stem + '-답안.pdf']
    for name in pdfs:
        (stage / name).write_text(name)
    (storage / pdfs[0]).write_text('stale staged copy')
    dest = tmp_path / 'published'
    publish_pack(stage, dest, tmp_path / 'backups', {'range': '0101', 'slug': 'Pdf_Test'})
    assert (dest / note.name).exists()
    assert not (dest / html.name).exists()
    for name in pdfs:
        assert (dest / name).read_text() == name
        assert not (dest / '.pack' / name).exists()
    assert read_cards(find_review(dest / html.name)).cards == read_cards(html).cards


def test_republished_pdf_relocates_existing_problem_page_links(tmp_path):
    import json
    import fitz
    from build_review_pdf import digest, publish_build
    from review_pdf_types import BuildResult

    review = tmp_path / FIXTURE.name
    review.write_bytes(FIXTURE.read_bytes())
    source = archive_cards(review)
    review.unlink()
    problem = source_pdf(source, '문제')
    answer = source_pdf(source, '답안')
    with fitz.open() as pdf:
        pdf.new_page().insert_text((30, 30), '예제P1 MML Example 9.1', fontname='korea')
        pdf.new_page().insert_text((30, 30), '연습문제P2 MML Exercise 6.1', fontname='korea')
        pdf.save(problem)
    answer.write_bytes(problem.read_bytes())
    explanation = tmp_path / '문제설명_0101_Pdf_Test.html'
    explanation.write_text(f'<a href="{problem.name}#page=2">원 문제 보기</a>', encoding='utf-8')
    markdown = source.parent / explanation.with_suffix('.md').name
    markdown.write_text(f'[원 문제 보기](../{problem.name}#page=2)', encoding='utf-8')

    stage = tmp_path / 'generated'
    stage.mkdir()
    new_problem, new_answer = stage / problem.name, stage / answer.name
    with fitz.open(problem) as pdf:
        pdf.insert_page(1, text='continuation')
        pdf.save(new_problem)
    new_answer.write_bytes(answer.read_bytes())
    report = stage / 'validation.json'
    report.write_text(json.dumps({
        'source_path': str(source), 'source_sha256': digest(source), 'profile': 'review',
        'range': '0101', 'slug': 'Pdf_Test', 'pages': {'problems': {'p1': [1, 2], 'p2': [3]}},
        'pdfs': {'problems': {'sha256': digest(new_problem)}, 'answers': {'sha256': digest(new_answer)}},
    }), encoding='utf-8')
    publish_build(BuildResult(new_problem, new_answer, report), problem.parent, tmp_path / 'backups')
    assert '#page=3' in explanation.read_text(encoding='utf-8')
    assert '#page=3' in markdown.read_text(encoding='utf-8')
    assert digest(problem) == digest(new_problem)
