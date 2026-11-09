"""Immutable contracts for the review workbook pipeline."""
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
Mode = Literal['problems','answers']
class ReviewPdfError(ValueError):
    pass
@dataclass(frozen=True)
class FigureInput:
    id: str
    html: str
    kind: Literal['svg','table','image']
@dataclass(frozen=True)
class ReviewCard:
    id: str
    title: str
    source: str
    part: str
    statement_html: str
    original_html: str
    hint_html: str
    steps: tuple[str,...]
    answer_html: str
    figures: tuple[FigureInput,...]
    hint_label: str = ''  # 문제지 Hint 띠에 보일 짧은 힌트(data-label). 없으면 '풀이 방향'
@dataclass(frozen=True)
class CardProfile:
    """Naming and labeling rules for one kind of card source (review pack, homework)."""
    name: str
    filename_re: str  # groups: (range, slug)
    source_re: str
    kind_label: str | None  # None: derive 예제/연습문제 from source
    title_fmt: str  # .format(range=…)
    stem_fmt: str  # .format(range=…, slug=…)
    source_fmt: str | None = None  # exact source per card: .format(range=…, n=…)
    def kind(self, source: str) -> str:
        return self.kind_label or ('예제' if ' Example ' in source else '연습문제')
    def expected_source(self, range_: str, card_id: str) -> str | None:
        return self.source_fmt.format(range=range_, n=card_id[1:]) if self.source_fmt else None
REVIEW = CardProfile('review', r'복습문제_(\d{4}(?:-\d{4})?)_([A-Za-z0-9_]+)\.html', r'MML (Example|Exercise) \d+(?:\.\d+)+', None, '머신러닝기초 복습문제 {range}', '복습문제_{range}_{slug}')
HOMEWORK = CardProfile('homework', r'과제(\d+)_([A-Za-z0-9_]+)\.html', r'HW\d+ Problem \d+', '과제', '머신러닝기초 과제{range}', '과제{range}_{slug}', 'HW{range} Problem {n}')
# 'midterm' (not 'exam'): ml-midterm's 예상문제 adapter already uses SourcePack('exam', ...) with review-style outputs.
EXAM_ACTUAL = CardProfile('midterm', r'중간고사_(\d{4})_([A-Za-z0-9_]+)\.html', r'Midterm \d{4} Q\d+', '시험', '머신러닝기초 중간고사 {range}', '중간고사_{range}_{slug}', 'Midterm {range} Q{n}')
PROFILES = {p.name: p for p in (REVIEW, HOMEWORK, EXAM_ACTUAL)}
@dataclass(frozen=True)
class ReviewPack:
    range: str
    slug: str
    cards: tuple[ReviewCard,...]
    source_path: Path | None = None
    profile: CardProfile = REVIEW
@dataclass(frozen=True)
class NormalizedProblem:
    card: ReviewCard
    conditions_html: str
    ask_html: str
@dataclass(frozen=True)
class FigureAsset:
    src: str
    w_mm: float
    h_mm: float
@dataclass(frozen=True)
class PageSlice:
    logical_id: str
    continuation: int
    conditions_html: str
    ask_html: str
    step_start: int
    step_end: int
    figure_ids: tuple[str,...]
    show_original: bool
    show_answer: bool
@dataclass(frozen=True)
class LayoutIssue:
    page_id: str
    area: str
    detail: str
@dataclass(frozen=True)
class RenderReport:
    page_ids: tuple[str,...]
    issues: tuple[LayoutIssue,...]
    katex_errors: tuple[str,...]
    failed_resources: tuple[str,...]
@dataclass(frozen=True)
class BuildResult:
    problems_pdf: Path
    answers_pdf: Path
    report_path: Path
