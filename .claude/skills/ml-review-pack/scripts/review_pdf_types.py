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
@dataclass(frozen=True)
class ReviewPack:
    range: str
    slug: str
    cards: tuple[ReviewCard,...]
    source_path: Path | None = None
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
