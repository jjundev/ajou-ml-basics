from dataclasses import replace
from pathlib import Path
import json
import re
import pytest
from helpers import fragment
from mpe_source import load_source, sha256
from mpe_types import ExplainError
from mpe_shared import parse, compact
from mpe_render import build_explanation, check_artifacts, artifact_hashes

ROOT = Path(__file__).resolve().parents[4]

@pytest.mark.parametrize('source', ['복습노트/1007/복습문제_1007_Product_of_Gaussians.html', '과제/과제1/과제1_Homework1.html'])
def test_render_preserves_questions_and_math_offline(tmp_path, source):
    source = ROOT / source
    before = source.read_bytes()
    pack = load_source(source, ROOT)
    pack = replace(pack, problems=pack.problems[:2])
    fragments = {p.id: fragment(p) for p in pack.problems}
    result = build_explanation(pack, fragments, tmp_path / 'stage', ROOT)
    assert check_artifacts(pack, result) == []
    text = result.html.read_text(encoding='utf-8')
    md = result.md.read_text(encoding='utf-8')
    root = parse(text)
    for p in pack.problems:
        reading = next(root.find_all(lambda n: n.attrs.get('data-source-problem') == p.id))
        fields = {n.attrs['data-source-field']: compact(n.text()) for n in reading.find_all(lambda n: 'data-source-field' in n.attrs)}
        assert fields == {'conditions': compact(p.conditions_html), 'ask': compact(p.ask_html)}
        assert f'<a id="{p.id}"></a>' in md
        if pack.profile == 'homework':
            assert p.original_html in text
            assert 'Find the transpose' in md
    assert 'https://cdn.' not in text
    assert f'ml-problem-explain-{pack.profile}-{pack.range}-{pack.slug}' in text
    assert not list(root.find_all(lambda n: n.tag == 'details'))
    assert source.read_bytes() == before
    assert set(artifact_hashes(result)) == {str(p.relative_to(result.html.parent)).replace('\\', '/') for p in result.files}

def test_missing_images_and_duplicate_svg_ids_refused(tmp_path):
    path = ROOT / '복습노트/1007/복습문제_1007_Product_of_Gaussians.html'
    pack = load_source(path, ROOT)
    p = pack.problems[0]
    pack = replace(pack, problems=(p,))
    with pytest.raises(ExplainError, match='경로|그림'):
        build_explanation(pack, {p.id: fragment(p) + '<img src="missing.png">'}, tmp_path / 'missing', ROOT)
    with pytest.raises(ExplainError, match='중복.*ID'):
        build_explanation(pack, {p.id: fragment(p) + '<svg><g id="a"></g><g id="a"></g></svg>'}, tmp_path / 'dup', ROOT)

def test_inline_svg_ids_rewritten_per_problem(tmp_path):
    pack = load_source(ROOT / '복습노트/1007/복습문제_1007_Product_of_Gaussians.html', ROOT)
    pack = replace(pack, problems=pack.problems[:2])
    fragments = {p.id: fragment(p) + '<svg viewBox="0 0 10 10"><defs><clipPath id="clip"><rect width="5" height="5"/></clipPath></defs><rect clip-path="url(#clip)" width="10" height="10"/></svg>' for p in pack.problems}
    result = build_explanation(pack, fragments, tmp_path / 'stage', ROOT)
    assert check_artifacts(pack, result) == []
    text = result.html.read_text(encoding='utf-8')
    assert 'url(#p1-clip)' in text and 'url(#p2-clip)' in text

def test_tampered_output_detected(tmp_path):
    pack = load_source(ROOT / '복습노트/1007/복습문제_1007_Product_of_Gaussians.html', ROOT)
    pack = replace(pack, problems=pack.problems[:1])
    result = build_explanation(pack, {p.id: fragment(p) for p in pack.problems}, tmp_path / 'stage', ROOT)
    result.html.write_text(result.html.read_text(encoding='utf-8') + '변경', encoding='utf-8')
    assert check_artifacts(pack, result)

def test_vendor_files_and_hashes_present():
    vendor = Path(__file__).resolve().parents[1] / 'assets/vendor'
    manifest = json.loads((vendor / 'provenance.json').read_text(encoding='utf-8'))
    for name, digest in manifest['files'].items():
        assert sha256(vendor / name) == digest
    for css in vendor.rglob('*.css'):
        for href in re.findall(r'url\([\'"]?([^\)\'"\s]+)', css.read_text(encoding='utf-8')):
            assert (css.parent / href).is_file()
