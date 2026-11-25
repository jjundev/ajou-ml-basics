from pathlib import Path
import sys, shutil, json, uuid
import pytest

REPO = Path(__file__).resolve().parents[4]
ROUND_ONE = '중간고사대비/예상문제_1회'
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

def pytest_configure(config):
    for marker in ('pdf', 'browser', 'integration'):
        config.addinivalue_line('markers', marker + ': actual artifact integration')

@pytest.fixture(scope='session')
def repo(tmp_path_factory):
    """A disposable course checkout, so outputs stay inside "the repository" without touching it."""
    from exam_adapter import resolve
    root = tmp_path_factory.mktemp('course').resolve()
    skip = shutil.ignore_patterns('__pycache__', '.pytest_cache')
    for skill in ('ml-midterm', 'ml-problem-explain', 'ml-review-pack'):
        for folder in ('scripts', 'assets'):
            src = REPO / '.claude/skills' / skill / folder
            if src.is_dir(): shutil.copytree(src, root / '.claude/skills' / skill / folder, ignore=skip)
    shutil.copytree(REPO / '.claude/skills/ml-review-pack/assets', root / '.agents/skills/ml-review-pack/assets')
    shutil.copytree(REPO / 'assets/vendor', root / 'assets/vendor')
    shutil.copytree(REPO / ROUND_ONE, root / ROUND_ONE, ignore=skip)
    blueprint = json.loads((root / ROUND_ONE / '.pack/blueprint.json').read_text(encoding='utf-8'))
    for source in blueprint['sources']:
        src = resolve(REPO, source['path']); dst = root / src.relative_to(REPO)
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
    return root

@pytest.fixture
def baseline(repo):
    return repo / ROUND_ONE

@pytest.fixture
def tmp_path(repo):
    """Per-test folder inside the disposable checkout."""
    path = repo / 'tmp' / uuid.uuid4().hex[:8]
    path.mkdir(parents=True)
    return path

@pytest.fixture
def exam(repo, baseline, tmp_path):
    from exam_config import ExamConfig
    out = tmp_path / '예상문제_2회'
    for folder in ('cards', 'explanations'):
        shutil.copytree(baseline / '.pack' / folder, out / '.pack' / folder)
    b = json.loads((baseline / '.pack/blueprint.json').read_text(encoding='utf-8'))
    b['slug'] = 'Midterm_Practice_02'
    (out / '.pack/blueprint.json').write_text(json.dumps(b, ensure_ascii=False), encoding='utf-8')
    return ExamConfig(repo, out, 2)
