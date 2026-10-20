from pathlib import Path
import sys, shutil, json
import pytest

REPO = Path(__file__).resolve().parents[4]
BASE = REPO / '중간고사대비/예상문제_1회'
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

def pytest_configure(config):
    for marker in ('pdf', 'browser', 'integration'):
        config.addinivalue_line('markers', marker + ': actual artifact integration')

@pytest.fixture
def repo():
    return REPO

@pytest.fixture
def baseline():
    return BASE

@pytest.fixture
def exam(tmp_path):
    from exam_config import ExamConfig
    out = tmp_path / '예상문제_2회'
    for folder in ('cards', 'explanations'):
        shutil.copytree(BASE / '.pack' / folder, out / '.pack' / folder)
    b = json.loads((BASE / '.pack/blueprint.json').read_text())
    b['slug'] = 'Midterm_Practice_02'
    (out / '.pack/blueprint.json').write_text(json.dumps(b, ensure_ascii=False))
    return ExamConfig(REPO, out, 2)
