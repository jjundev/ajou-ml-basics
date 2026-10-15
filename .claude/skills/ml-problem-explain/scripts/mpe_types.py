"""Immutable inputs and staged explanation outputs."""
from dataclasses import dataclass
from pathlib import Path

class ExplainError(ValueError):
    pass

@dataclass(frozen=True)
class ChoiceModel:
    answer: str
    mode: str
    option_ids: tuple[str, ...]

@dataclass(frozen=True)
class Problem:
    id: str
    number: int
    title: str
    source: str
    original_html: str
    conditions_html: str
    ask_html: str
    figures_html: tuple[str, ...]
    reference_steps: tuple[str, ...]
    reference_answer: str
    subparts: tuple[str, ...]
    choice: ChoiceModel | None = None

@dataclass(frozen=True)
class SourcePack:
    profile: str
    range: str
    slug: str
    path: Path
    sha256: str
    problems: tuple[Problem, ...]

@dataclass(frozen=True)
class Artifacts:
    html: Path
    md: Path
    manifest: Path
    files: tuple[Path, ...]
