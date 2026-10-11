"""Immutable inputs and staged explanation outputs."""
from dataclasses import dataclass
from pathlib import Path

class ExplainError(ValueError):
    pass

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
