from pathlib import Path
import json
import shutil
import unicodedata
import pytest
from mpe_source import load_source, resolve_sources, subparts
from mpe_types import ExplainError
from review_sources import html_name

ROOT = Path(__file__).resolve().parents[4]
HW = ROOT / '과제/과제1/과제1_Homework1.html'
REVIEW = ROOT / '복습노트/1007/.pack/복습문제_1007_Product_of_Gaussians.cards.json'

def test_homework_preserves_all_cards_and_subparts():
    before = HW.read_bytes()
    pack = load_source(HW, ROOT)
    assert pack.profile == 'homework'
    assert [p.id for p in pack.problems] == [f'p{i}' for i in range(1, 26)]
    assert pack.problems[0].subparts == ('a', 'b', 'c')
    assert pack.problems[1].subparts == ('a', 'b', 'c', 'd')
    assert pack.problems[2].subparts == ('main',)
    assert all(p.original_html and p.reference_answer for p in pack.problems)
    assert HW.read_bytes() == before

def test_latest_and_explicit_homework(tmp_path):
    for date in ('1007', '1012'):
        path = tmp_path / '복습노트' / date / f'복습문제_{date}_Fixture.html'
        path.parent.mkdir(parents=True)
        path.touch()
    resolved = resolve_sources(tmp_path, None)
    assert len(resolved) == 1 and resolved[0].name == '복습문제_1012_Fixture.html'
    resolved = resolve_sources(ROOT, '과제1')
    assert len(resolved) == 1 and resolved[0].samefile(HW)
    resolved = resolve_sources(ROOT, str(REVIEW))
    assert len(resolved) == 1 and resolved[0].samefile(REVIEW)

def test_duplicate_requires_explicit_path(tmp_path):
    folder = tmp_path / '복습노트/1007'
    folder.mkdir(parents=True)
    for slug in ('First', 'Second'):
        (folder / f'복습문제_1007_{slug}.html').touch()
    with pytest.raises(ExplainError, match='여러 후보'):
        resolve_sources(tmp_path, '1007')

def test_range_overlap_is_ambiguous(tmp_path):
    folder = tmp_path / '복습노트'
    folder.mkdir()
    for date in ('0909', '0916', '0909-0916'):
        (folder / f'복습문제_{date}_A.html').touch()
    with pytest.raises(ExplainError, match='여러 후보'):
        resolve_sources(tmp_path, '0909-0916')

def test_nfd_paths(tmp_path):
    folder = tmp_path / unicodedata.normalize('NFD', '복습노트') / '1007'
    folder.mkdir(parents=True)
    path = folder / unicodedata.normalize('NFD', html_name(REVIEW))
    path.touch()
    assert resolve_sources(tmp_path, '1007') == (path,)

def test_legacy_layout_and_stale_rejection(tmp_path):
    path = ROOT / '복습노트/0909/.pack/복습문제_0909_Data_Models_Learning.cards.json'
    pack = load_source(path, ROOT)
    assert pack.problems[0].conditions_html
    assert 'f(10)' in pack.problems[0].ask_html
    copied = tmp_path / path.name
    shutil.copy2(path, copied)
    layout = tmp_path / 'workbook/layouts/0909_Data_Models_Learning.json'
    layout.parent.mkdir(parents=True)
    data = json.loads((ROOT / 'workbook/layouts' / layout.name).read_text(encoding='utf-8'))
    data['source_sha256'] = '0' * 64
    layout.write_text(json.dumps(data), encoding='utf-8')
    with pytest.raises(ExplainError, match='stale layout source'):
        load_source(copied, tmp_path)

@pytest.mark.parametrize('target', ['과제999', '1330', '0930-0909'])
def test_missing_or_invalid_target(tmp_path, target):
    with pytest.raises(ExplainError):
        resolve_sources(tmp_path, target)

def test_outside_source_is_rejected(tmp_path):
    with pytest.raises(ExplainError, match='저장소'):
        load_source(HW, tmp_path)

def test_latest_day_and_integrated_pack_are_ambiguous(tmp_path):
    for folder, value in [('a', '1007'), ('b', '0930-1007')]:
        path = tmp_path / '복습노트' / folder / f'복습문제_{value}_A.html'
        path.parent.mkdir(parents=True)
        path.touch()
    with pytest.raises(ExplainError, match='여러 후보'):
        resolve_sources(tmp_path, None)

def test_original_subparts_cannot_be_collapsed_to_main():
    with pytest.raises(ExplainError, match='소문항'):
        subparts('<p>Calculate both.</p>', '<div class="part">(a) first</div><div class="part">(b) second</div>')

def test_explicit_nfc_path_resolves_existing_nfd_file(tmp_path):
    folder = tmp_path / unicodedata.normalize('NFD', '복습노트') / '1007'
    folder.mkdir(parents=True)
    path = folder / unicodedata.normalize('NFD', html_name(REVIEW))
    path.touch()
    resolved = resolve_sources(tmp_path, unicodedata.normalize('NFC', str(path)))
    assert len(resolved) == 1 and resolved[0].samefile(path)
