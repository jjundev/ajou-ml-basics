import json
import subprocess
import sys
from pathlib import Path
import pytest
from helpers import fragment, approved
from mpe_source import load_source
from mpe_cli import load_run
from review_sources import source_markup, html_name, review_dir

ROOT = Path(__file__).resolve().parents[4]
CLI = Path(__file__).resolve().parents[1] / 'scripts/mpe_cli.py'

def call(*args):
    return subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True, text=True, encoding='utf-8')

def test_missing_target_returns_one(tmp_path):
    result = call('extract', '--repo', ROOT, '--target', '과제999', '--run', tmp_path / 'run')
    assert result.returncode == 1
    assert '대상 없음' in result.stderr

def test_cli_round_trip_and_unreviewed_publish(tmp_path):
    repo = tmp_path / 'repo'
    source = repo / '과제/과제1/과제1_Homework1.html'
    source.parent.mkdir(parents=True)
    source.write_bytes((ROOT / '과제/과제1' / source.name).read_bytes())
    run = tmp_path / 'run'
    result = call('extract', '--repo', repo, '--target', '과제1', '--run', run)
    assert result.returncode == 0, result.stderr
    item = load_run(run)[0]
    assert item['pack'] == load_source(source, repo)
    before = source.read_bytes()
    for p in item['pack'].problems:
        (item['folder'] / 'explanations' / f'{p.id}.html').write_text(fragment(p), encoding='utf-8')
    for command in ('build', 'check'):
        result = call(command, '--run', run)
        assert result.returncode == 0, result.stderr
    result = call('publish', '--run', run)
    assert result.returncode == 1 and '보류' in result.stderr
    assert source.read_bytes() == before
    assert not list(source.parent.glob('*문제설명*.html'))
    item = load_run(run)[0]
    from mpe_cli import load_artifacts, load_fragments
    artifacts = load_artifacts(item)
    reviews = approved(item['pack'], load_fragments(item), artifacts)
    (item['folder'] / 'review.json').write_text(json.dumps(reviews, ensure_ascii=False), encoding='utf-8')
    result = call('publish', '--run', run)
    assert result.returncode == 0, result.stderr
    assert list(source.parent.glob('*문제설명*.html'))
    assert source.read_bytes() == before

def test_extract_refuses_nonempty_run(tmp_path):
    run = tmp_path / 'run'
    run.mkdir()
    (run / 'keep.txt').write_text('keep')
    result = call('extract', '--repo', ROOT, '--target', '1007', '--run', run)
    assert result.returncode == 1
    assert (run / 'keep.txt').read_text() == 'keep'

def test_forged_serialized_problem_is_rejected(tmp_path):
    run = tmp_path / 'run'
    assert call('extract', '--repo', ROOT, '--target', '1007', '--run', run).returncode == 0
    source_json = next(run.rglob('source.json'))
    value = json.loads(source_json.read_text(encoding='utf-8'))
    value['problems'][0]['ask_html'] = '위조 조건'
    source_json.write_text(json.dumps(value), encoding='utf-8')
    result = call('check', '--run', run)
    assert result.returncode == 1
    assert '추출' in result.stderr

def test_one_stale_pack_does_not_block_other_pack(tmp_path):
    repo = tmp_path / 'repo'
    for date in ('1006', '1007'):
        source = repo / '복습노트' / date / f'복습문제_{date}_Product_of_Gaussians.html'
        source.parent.mkdir(parents=True)
        source.write_bytes(source_markup(ROOT / '복습노트/1007/.pack/복습문제_1007_Product_of_Gaussians.cards.json').encode())
    run = tmp_path / 'run'
    assert call('extract', '--repo', repo, '--target', '1006-1007', '--run', run).returncode == 0
    for item in load_run(run):
        for p in item['pack'].problems:
            (item['folder'] / 'explanations' / f'{p.id}.html').write_text(fragment(p), encoding='utf-8')
    later = repo / '복습노트/1007/복습문제_1007_Product_of_Gaussians.html'
    later.write_bytes(later.read_bytes() + b'changed')
    result = call('build', '--run', run)
    assert result.returncode == 1
    assert (run / 'review-1006-Product_of_Gaussians/stage.json').is_file()
    assert not (run / 'review-1007-Product_of_Gaussians/stage.json').is_file()

def test_check_refuses_fragments_changed_after_build(tmp_path):
    run = tmp_path / 'run'
    assert call('extract', '--repo', ROOT, '--target', '1007', '--run', run).returncode == 0
    item = load_run(run)[0]
    for p in item['pack'].problems:
        (item['folder'] / 'explanations' / f'{p.id}.html').write_text(fragment(p), encoding='utf-8')
    assert call('build', '--run', run).returncode == 0
    (item['folder'] / 'explanations/p1.html').write_text('<p>풀이 누락</p>', encoding='utf-8')
    result = call('check', '--run', run)
    assert result.returncode == 1
    machine = json.loads((item['folder'] / 'machine.json').read_text(encoding='utf-8'))
    assert machine['status'] == 'fail'


def test_cli_explicit_review_path_ignores_newer_and_other_slug(tmp_path):
    import shutil
    repo = tmp_path / 'repo'
    original = ROOT / '복습노트/0909/.pack/복습문제_0909_Data_Models_Learning.cards.json'
    source = repo / original.relative_to(ROOT)
    source.parent.mkdir(parents=True)
    shutil.copy2(original, source)
    for suffix in ('-문제.pdf','-답안.pdf'):
        pdf = review_dir(original) / (Path(html_name(original)).stem + suffix)
        shutil.copy2(pdf, review_dir(source) / pdf.name)
    layout = Path('workbook/layouts/0909_Data_Models_Learning.json')
    (repo / layout).parent.mkdir(parents=True)
    shutil.copy2(ROOT / layout, repo / layout)
    for date, slug in [('0909', 'Other'), ('1012', 'Latest')]:
        other = repo / '복습노트' / date / f'복습문제_{date}_{slug}.html'
        other.parent.mkdir(parents=True, exist_ok=True)
        other.write_text(source_markup(original), encoding='utf-8')
    before = source.read_bytes()
    old = review_dir(source) / '문제설명_0909_Data_Models_Learning.html'
    old.write_bytes(b'previous explanation')
    run = tmp_path / 'run'
    result = call('extract', '--repo', repo, '--target', source, '--run', run)
    assert result.returncode == 0, result.stderr
    item, = load_run(run)
    expected = load_source(source, repo)
    assert item['pack'] == expected
    value = json.loads((item['folder'] / 'source.json').read_text())
    assert value['path'] == str(source) and value['sha256'] == expected.sha256
    assert [p['id'] for p in value['problems']] == [p.id for p in expected.problems]
    for p in expected.problems:
        (item['folder'] / 'explanations' / f'{p.id}.html').write_text(fragment(p))
    for command in ('build', 'check'):
        result = call(command, '--run', run)
        assert result.returncode == 0, result.stderr
    result = call('publish', '--run', run)
    assert result.returncode == 1 and '보류' in result.stderr
    assert source.read_bytes() == before
    assert old.read_bytes() == b'previous explanation'
