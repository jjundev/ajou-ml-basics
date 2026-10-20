import json, copy, unicodedata
from pathlib import Path
import pytest

def test_next_round_and_existing_output(tmp_path):
    from exam_config import next_round, config_for_round
    root = tmp_path / '중간고사대비'
    (root / '예상문제_1회').mkdir(parents=True)
    assert next_round(tmp_path) == 2
    (root / '예상문제_3회').mkdir()
    assert next_round(tmp_path) == 4
    for n in (0, -1):
        with pytest.raises(ValueError): config_for_round(tmp_path, n)

def test_round_two_profile(repo):
    from exam_config import config_for_round
    cfg = config_for_round(repo, 2)
    assert cfg.slug == 'Midterm_Practice_02'
    assert cfg.stem == '중간고사예상_0909-1019_Midterm_Practice_02'
    assert cfg.title_en.endswith('02')
    assert cfg.reading_key != config_for_round(repo, 1).reading_key

def test_blueprint_and_card_contract(repo, exam):
    from exam_adapter import validate_blueprint, load_exam_source, assemble_cards
    bp = exam.output / '.pack/blueprint.json'
    value = json.loads(bp.read_text())
    assert validate_blueprint(value, repo, exam) == []
    source = assemble_cards(exam.output / '.pack/cards', exam.output / (exam.stem + '.html'), exam)
    pack = load_exam_source(source, bp, repo, exam)
    assert len(pack.problems) == 10
    assert sum(len(p.subparts) for p in pack.problems) == 42
    mutations = [lambda b: b['questions'].pop(), lambda b: b['questions'][0].update(kind='model_analysis'),
                 lambda b: b.update(slug='Midterm_Practice_01'),
                 lambda b: b['questions'][0].update(subparts=['a', 'a']),
                 lambda b: b['sources'][0].update(sha256='0'*64)]
    for mutate in mutations:
        bad = copy.deepcopy(value); mutate(bad)
        assert validate_blueprint(bad, repo, exam)
    source.write_text(source.read_text().replace('data-origin-ref="HW1 P6-P8"', 'data-origin-ref="invented"'))
    with pytest.raises(ValueError, match='origin mismatch'): load_exam_source(source, bp, repo, exam)

def test_unicode_worktree_and_paths(tmp_path, repo, baseline):
    from exam_adapter import resolve
    from exam_config import config_for_output
    path = (baseline / '.pack/blueprint.json').relative_to(repo).as_posix()
    assert resolve(repo, unicodedata.normalize('NFD', path)) == resolve(repo, unicodedata.normalize('NFC', path))
    with pytest.raises(ValueError): resolve(repo, '../outside')
    (tmp_path / '.git').write_text('gitdir: elsewhere')
    out = tmp_path / '예상문제_12회'; out.mkdir()
    (out / '.pack').mkdir()
    (out / '.pack/blueprint.json').write_text(json.dumps({'range':'0909-1019','slug':'Midterm_Practice_12'}))
    assert config_for_output(tmp_path, out).round_number == 12
    a = tmp_path / '가'; a.write_text('a')
    b = tmp_path / unicodedata.normalize('NFD', '가'); b.write_text('b')
    with pytest.raises(ValueError, match='ambiguous'): resolve(tmp_path, a)

def test_baseline_change_is_reported(tmp_path):
    from exam_adapter import verify_baseline, sha
    p = tmp_path / 'template'; p.write_text('fixed')
    pin = tmp_path / 'baseline.json'; pin.write_text(json.dumps({'files': {'template': sha(p)}}))
    assert verify_baseline(tmp_path, pin) == []
    p.write_text('changed')
    assert 'template' in ' '.join(verify_baseline(tmp_path, pin))
