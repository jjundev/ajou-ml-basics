"""Check current published links and inventory independently of historical approvals."""
import hashlib
import json
from pathlib import Path
import shutil
import unicodedata
from urllib.parse import unquote, urlsplit

import fitz
import pytest

from mpe_render import parse
from mpe_source import load_source
from review_sources import discover_reviews, html_name, review_dir, source_pdf

ROOT = Path(__file__).resolve().parents[4]
SOURCES = discover_reviews(ROOT / '복습노트')


def audit_delivery(source, root):
    pack = load_source(source, root)
    folder = pack.directory
    name = f'문제설명_{pack.range}_{pack.slug}'
    html = folder / (name + '.html')
    data = folder / '.pack' / ('자료_' + name)
    if not data.is_dir():
        data = folder / ('자료_' + name)
    manifest = json.loads((data / 'manifest.json').read_text(encoding='utf-8'))
    md = next((p for p in (folder / '.pack' / (name + '.md'), folder / (name + '.md')) if p.is_file()))
    historic_name = unicodedata.normalize('NFC', Path(manifest['source']).name)
    assert historic_name in (html_name(source), unicodedata.normalize('NFC', source.name))
    assert manifest['problems'] == [{'id': p.id, 'subparts': list(p.subparts)} for p in pack.problems]
    assert not (folder / html_name(source)).exists()
    for artifact in (html, md):
        relative = artifact.relative_to(folder).as_posix()
        content = artifact.read_bytes()
        expected = manifest['files'][relative]
        if artifact == html and hashlib.sha256(content).hexdigest() != expected:
            # Published CSS changed after the pack manifest was archived.
            viewport_height = b'html { height: 100%; } body { height: 100%; min-height: 0; display: grid; grid-template-rows: auto minmax(0, 1fr) auto; overflow: hidden; }'
            archived_height = b'body { height: 100vh; height: 100dvh; min-height: 0; display: grid; grid-template-rows: auto minmax(0, 1fr) auto; overflow: hidden; }'
            content = content.replace(viewport_height, archived_height, 1)
        assert hashlib.sha256(content).hexdigest() == expected
    pdf = source_pdf(source, '문제')
    links = [urlsplit(node.attrs['href']) for node in parse(html.read_text(encoding='utf-8')).find_all(
        lambda n: n.tag == 'a' and n.text().strip() == '원 문제 보기')]
    assert len(links) == len(pack.problems)
    with fitz.open(pdf) as doc:
        for problem, url in zip(pack.problems, links):
            assert (folder / unquote(url.path)).samefile(pdf)
            page_no = int(url.fragment.removeprefix('page='))
            header = doc[page_no - 1].get_text(clip=fitz.Rect(0, 0, doc[page_no - 1].rect.width, 55))
            assert problem.id.upper() in header and problem.source in header
    assert manifest['input_hash'] == json.loads((data / 'validation.json').read_text(encoding='utf-8'))['input_hash']


@pytest.mark.parametrize('source', SOURCES, ids=lambda p: review_dir(p).name)
def test_published_review_explanation(source):
    audit_delivery(source, ROOT)


@pytest.mark.parametrize('source', SOURCES, ids=lambda p: review_dir(p).name)
def test_published_layout_keeps_document_entries_on_top(source):
    top = {unicodedata.normalize('NFC', p.name) for p in review_dir(source).iterdir()
           if p.name != '.DS_Store'}
    assert '.pack' in top
    assert html_name(source) not in top
    assert source_pdf(source, '문제').is_file() and source_pdf(source, '답안').is_file()


def test_delivery_survives_checkout_relocation_and_detects_artifact_damage(tmp_path):
    archive = next(p for p in SOURCES if review_dir(p).name == '0909')
    relocated = tmp_path / 'checkout'
    shutil.copytree(review_dir(archive), relocated / '복습노트/0909')
    shutil.copytree(ROOT / 'workbook/layouts', relocated / 'workbook/layouts')
    moved = relocated / archive.relative_to(ROOT)
    audit_delivery(moved, relocated)
    md = next((review_dir(moved) / '.pack').glob('문제설명_*.md'))
    md.write_bytes(md.read_bytes() + b'changed')
    with pytest.raises(AssertionError):
        audit_delivery(moved, relocated)
