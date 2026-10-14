from dataclasses import replace
from pathlib import Path
import json
import pytest
from helpers import fragment, approved
from mpe_source import load_source
from mpe_render import build_explanation
from mpe_publish import publish_explanation
from mpe_types import ExplainError
import review_pdf_publish

ROOT = Path(__file__).resolve().parents[4]

def setup(tmp_path):
    src = tmp_path / 'repo/복습노트/1007/복습문제_1007_Product_of_Gaussians.html'
    src.parent.mkdir(parents=True)
    src.write_bytes((ROOT / '복습노트/1007' / src.name).read_bytes())
    pack = load_source(src, tmp_path / 'repo')
    pack = replace(pack, problems=pack.problems[:1])
    fragments = {p.id: fragment(p) for p in pack.problems}
    artifacts = build_explanation(pack, fragments, tmp_path / 'stage', tmp_path / 'repo')
    return pack, fragments, artifacts

def test_no_review_keeps_existing_files(tmp_path):
    pack, fragments, artifacts = setup(tmp_path)
    dst = pack.path.parent / artifacts.html.name
    dst.write_bytes(b'old')
    source = pack.path.read_bytes()
    with pytest.raises(ExplainError, match='보류'):
        publish_explanation(pack, artifacts, fragments, {}, pack.path.parent, tmp_path / 'backup')
    assert dst.read_bytes() == b'old'
    assert pack.path.read_bytes() == source

@pytest.mark.parametrize('change', ['source', 'fragment', 'artifact', 'report', 'browser', 'reference', 'manifest'])
def test_stale_inputs_or_failed_reviews_are_refused(tmp_path, change):
    pack, fragments, artifacts = setup(tmp_path)
    reviews = approved(pack, fragments, artifacts)
    reference = tmp_path / 'repo/reference.txt'
    reference.write_bytes(b'original')
    from mpe_source import sha256
    reviews['references'] = [{'path': str(reference), 'sha256': sha256(reference)}]
    if change == 'source':
        pack.path.write_bytes(pack.path.read_bytes() + b'changed')
    elif change == 'fragment':
        fragments['p1'] += 'changed'
    elif change == 'artifact':
        artifacts.html.write_bytes(artifacts.html.read_bytes() + b'changed')
    elif change == 'report':
        reviews['artifact_hashes'] = {}
    elif change == 'manifest':
        artifacts.manifest.write_bytes(artifacts.manifest.read_bytes() + b' ')
    elif change == 'reference':
        reference.write_bytes(b'changed')
    else:
        reviews['browser']['status'] = 'fail'
    with pytest.raises(ExplainError):
        publish_explanation(pack, artifacts, fragments, reviews, pack.path.parent, tmp_path / 'backup')
    assert not (pack.path.parent / artifacts.html.name).exists()

def test_outside_stage_and_wrong_destination_refused(tmp_path):
    pack, fragments, artifacts = setup(tmp_path)
    reviews = approved(pack, fragments, artifacts)
    outside = tmp_path / 'original.html'
    outside.touch()
    with pytest.raises(ExplainError):
        publish_explanation(pack, replace(artifacts, files=artifacts.files + (outside,)), fragments, reviews, pack.path.parent, tmp_path / 'backup')
    with pytest.raises(ExplainError):
        publish_explanation(pack, artifacts, fragments, reviews, tmp_path, tmp_path / 'backup')

def test_success_preserves_original_and_saves_review(tmp_path):
    pack, fragments, artifacts = setup(tmp_path)
    before = pack.path.read_bytes()
    published = publish_explanation(pack, artifacts, fragments, approved(pack, fragments, artifacts), pack.path.parent, tmp_path / 'backup')
    assert pack.path.read_bytes() == before
    assert (pack.path.parent / artifacts.html.name).read_bytes() == artifacts.html.read_bytes()
    # 날짜 폴더 최상위에는 HTML만, 나머지는 .pack/ 아래에 발행된다.
    top = {p.name for p in pack.path.parent.iterdir()}
    assert top == {pack.path.name, artifacts.html.name, '.pack'}
    assert (pack.path.parent / '.pack' / artifacts.md.name).read_bytes() == artifacts.md.read_bytes()
    report = next(p for p in published if p.name == 'validation.json')
    assert report.parent.parent.name == '.pack'
    assert json.loads(report.read_text(encoding='utf-8'))['browser']['status'] == 'pass'

def test_replace_failure_rolls_back_pair(tmp_path, monkeypatch):
    pack, fragments, artifacts = setup(tmp_path)
    for file in (artifacts.html, artifacts.md):
        old = pack.path.parent / file.relative_to(artifacts.html.parent)
        old.parent.mkdir(exist_ok=True)
        old.write_bytes(b'old-' + file.suffix.encode())
    replace_copy = review_pdf_publish._replace_copy
    calls = 0
    def fail_once(source, destination):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError('injected write failure')
        return replace_copy(source, destination)
    monkeypatch.setattr(review_pdf_publish, '_replace_copy', fail_once)
    with pytest.raises(ExplainError, match='injected'):
        publish_explanation(pack, artifacts, fragments, approved(pack, fragments, artifacts), pack.path.parent, tmp_path / 'backup')
    for file in (artifacts.html, artifacts.md):
        assert (pack.path.parent / file.relative_to(artifacts.html.parent)).read_bytes() == b'old-' + file.suffix.encode()
    assert not list(pack.path.parent.rglob('validation.json'))

def test_overlapping_publication_lock_is_refused(tmp_path):
    pack, fragments, artifacts = setup(tmp_path)
    with review_pdf_publish.publication_lock([pack.path.parent / artifacts.html.name]):
        with pytest.raises(ExplainError, match='locked'):
            publish_explanation(pack, artifacts, fragments, approved(pack, fragments, artifacts), pack.path.parent, tmp_path / 'backup')
