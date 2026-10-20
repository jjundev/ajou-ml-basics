"""Round identity and target selection; selection never writes course files."""
from dataclasses import dataclass
from pathlib import Path
import json
import re
import sys

CODE_REPO = Path(__file__).resolve().parents[4]
for skill in ('ml-review-pack', 'ml-problem-explain'):
    sys.path.insert(0, str(CODE_REPO / '.claude/skills' / skill / 'scripts'))
from review_pdf_types import CardProfile

@dataclass(frozen=True)
class ExamConfig:
    repo: Path
    output: Path
    round_number: int

    def __post_init__(self):
        if isinstance(self.round_number, bool) or not isinstance(self.round_number, int) or self.round_number < 1:
            raise ValueError('round must be a positive integer')
        root = Path(self.repo).resolve()
        output = Path(self.output)
        output = (root / output).resolve() if not output.is_absolute() else output.resolve()
        if not output.is_relative_to(root) or output == root:
            raise ValueError('outside repository or repository root output')
        object.__setattr__(self, 'repo', root)
        object.__setattr__(self, 'output', output)

    @property
    def range_(self): return '0909-1019'
    @property
    def slug(self): return f'Midterm_Practice_{self.round_number:02d}'
    @property
    def stem(self): return f'중간고사예상_{self.range_}_{self.slug}'
    @property
    def title_ko(self): return f'머신러닝기초 중간고사 예상문제 {self.round_number}회'
    @property
    def title_en(self): return f'Introduction to Machine Learning - Midterm Practice {self.round_number:02d}'
    @property
    def reading_key(self): return f'ml-problem-explain-exam-{self.range_}-{self.slug}'
    @property
    def profile(self):
        return CardProfile('exam', r'중간고사예상_(\d{4}-\d{4})_([A-Za-z0-9_]+)\.html',
                           r'EXAM Problem [1-9]\d*', '예상문제', self.title_ko,
                           '중간고사예상_{range}_{slug}', 'EXAM Problem {n}')

def next_round(repo):
    folder = Path(repo) / '중간고사대비'
    numbers = [int(m[1]) for p in folder.iterdir() if p.is_dir()
               and (m := re.fullmatch(r'예상문제_(\d+)회', p.name))] if folder.exists() else []
    return max(numbers, default=0) + 1

def config_for_round(repo, number=None):
    number = next_round(repo) if number is None else number
    return ExamConfig(Path(repo), Path(repo).resolve() / f'중간고사대비/예상문제_{number}회', number)

def config_for_output(repo, output):
    from exam_adapter import resolve
    output = resolve(repo, output)
    bp = json.loads(resolve(repo, output / '.pack/blueprint.json').read_text(encoding='utf-8'))
    match = re.fullmatch(r'Midterm_Practice_(\d{2,})', bp.get('slug', ''))
    if not match or bp.get('range') != '0909-1019':
        raise ValueError('not a midterm blueprint')
    cfg = ExamConfig(Path(repo), output, int(match[1]))
    if cfg.slug != bp['slug']: raise ValueError('noncanonical slug')
    named = re.fullmatch(r'예상문제_(\d+)회', output.name)
    if named and int(named[1]) != cfg.round_number: raise ValueError('round folder/blueprint mismatch')
    return cfg

def resolve_exam_target(repo, target):
    from exam_adapter import resolve
    match = re.fullmatch(r'중간고사\s*(\d+)회', target.strip())
    if match:
        cfg = config_for_round(repo, int(match[1]))
        return resolve_exam_target(repo, str(cfg.output / (cfg.stem + '.html')))
    path = resolve(repo, target)
    cfg = config_for_output(repo, path.parent)
    originals = list(path.parent.glob('중간고사예상_*.html'))
    if len(originals) != 1 or originals[0].name != cfg.stem + '.html':
        raise ValueError('missing or ambiguous original: ' + str(originals))
    allowed = (cfg.stem + '.html', f'문제설명_{cfg.range_}_{cfg.slug}.html')
    if path.name not in allowed: raise ValueError('not a midterm HTML target')
    return cfg
