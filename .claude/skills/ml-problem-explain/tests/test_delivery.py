"""Published delivery checks; semantic approval remains a separate human/agent review."""
import hashlib
import json
from pathlib import Path
import unicodedata
import tempfile
import shutil
import pytest
from mpe_source import load_source
from mpe_types import Artifacts
from mpe_render import check_artifacts, artifact_hashes

ROOT = Path(__file__).resolve().parents[4]
SOURCES = sorted(p for p in (ROOT / '복습노트').rglob('*.html')
                 if unicodedata.normalize('NFC', p.name).startswith('복습문제_'))

def repo_relative(path, root):
    """Recorded macOS NFD names and Git NFC names identify the same file."""
    normalize = lambda value: Path(unicodedata.normalize('NFC', str(value)))
    return normalize(path).relative_to(normalize(root))


def structural_check_in_current_checkout(pack, artifacts, manifest, root):
    """Rebase only a disposable view; never rewrite approved files or hashes."""
    old_repo = Path(manifest['repo'])
    assert repo_relative(manifest['source'], old_repo) == repo_relative(pack.path, root)
    assert repo_relative(manifest['destination'], old_repo) == repo_relative(pack.path.parent, root)
    mapped = {**manifest, 'source': str(pack.path),
              'destination': str(pack.path.parent), 'repo': str(root)}
    original_root = artifacts.html.parent
    with tempfile.TemporaryDirectory(prefix='ml-delivery-view-') as directory:
        view = Path(directory).resolve()
        # Byte-identical copies; the manifest gets a disposable rebased view.
        for file in artifacts.files:
            rel = file.relative_to(original_root)
            dest = view / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if file == artifacts.manifest:
                dest.write_text(json.dumps(mapped, ensure_ascii=False), encoding='utf-8')
            else:
                shutil.copy2(file, dest)
        viewed = Artifacts(view / artifacts.html.name, view / artifacts.md.name,
                           view / artifacts.manifest.relative_to(original_root),
                           tuple(view / file.relative_to(original_root) for file in artifacts.files))
        return check_artifacts(pack, viewed)


def audit_delivery(source, root):
    pack = load_source(source, root)
    name = f'문제설명_{pack.range}_{pack.slug}'
    html, md = source.parent / (name + '.html'), source.parent / (name + '.md')
    data = source.parent / ('자료_' + name)
    manifest_path = data / 'manifest.json'
    assert html.is_file() and md.is_file() and manifest_path.is_file(), name
    manifest = json.loads(manifest_path.read_text())
    assert repo_relative(manifest['source'], manifest['repo']) == repo_relative(source, root)
    assert manifest['source_sha256'] == pack.sha256
    assert manifest['problems'] == [{'id':p.id, 'subparts':list(p.subparts)} for p in pack.problems]
    artifacts = Artifacts(html, md, manifest_path,
                          tuple(source.parent / p for p in manifest['files']) + (manifest_path,))
    assert structural_check_in_current_checkout(pack, artifacts, manifest, root) == []
    review = json.loads((data / 'validation.json').read_text())
    assert review['input_hash'] == manifest['input_hash']
    assert review['artifact_hashes'] == artifact_hashes(artifacts)
    keys = {p.id + ':' + s for p in pack.problems for s in p.subparts}
    for kind in ('source_visual', 'content', 'independent', 'browser'):
        assert review[kind]['status'] == 'pass'
        assert review[kind]['reviewer'] and review[kind]['evidence']
    for kind in ('content', 'independent'):
        assert set(review[kind]['items']) == keys
        assert all(item['status'] == 'pass' for item in review[kind]['items'].values())
    assert review['references']
    for ref in review['references']:
        current_reference = root / repo_relative(ref['path'], manifest['repo'])
        assert hashlib.sha256(current_reference.read_bytes()).hexdigest() == ref['sha256']


@pytest.mark.parametrize('source', SOURCES, ids=lambda p: p.parent.name)
def test_published_review_explanation(source):
    audit_delivery(source, ROOT)


@pytest.mark.parametrize('damage', [None, 'reference', 'artifact'])
def test_delivery_survives_checkout_relocation(tmp_path, damage):
    import shutil
    source = next(p for p in SOURCES if p.parent.name == '0909')
    pack = load_source(source, ROOT)
    name = f'문제설명_{pack.range}_{pack.slug}'
    data = source.parent / ('자료_' + name)
    manifest_path = data / 'manifest.json'
    validation_path = data / 'validation.json'
    manifest_bytes, validation_bytes = manifest_path.read_bytes(), validation_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    review = json.loads(validation_bytes)
    relocated = tmp_path / 'different-home' / 'checkout'
    def copy(path):
        dest = relocated / path.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        return dest
    # Only the input, related note, referenced sources and owned output are needed.
    for path in source.parent.glob('*.html'):
        copy(path)
    for relative in manifest['files']:
        copy(source.parent / relative)
    copy(manifest_path)
    copy(validation_path)
    layout = ROOT / 'workbook/layouts' / f'{pack.range}_{pack.slug}.json'
    copy(layout)
    for ref in review['references']:
        copy(Path(ref['path']))
    moved = relocated / source.relative_to(ROOT)
    assert moved.read_bytes() == source.read_bytes()
    assert not moved.samefile(source)
    if damage:
        target = (relocated / Path(review['references'][0]['path']).relative_to(ROOT)
                  if damage == 'reference' else moved.parent / (name + '.md'))
        target.write_bytes(target.read_bytes() + b'changed')
        with pytest.raises(AssertionError):
            audit_delivery(moved, relocated)
    else:
        audit_delivery(moved, relocated)
    assert manifest_path.read_bytes() == manifest_bytes
    assert validation_path.read_bytes() == validation_bytes
    moved_data = moved.parent / data.name
    assert (moved_data / 'manifest.json').read_bytes() == manifest_bytes
    assert (moved_data / 'validation.json').read_bytes() == validation_bytes
