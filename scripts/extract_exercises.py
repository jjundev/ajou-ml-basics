#!/usr/bin/env python3
"""
Mathematics for Machine Learning (MML) - Part I Exercises Extractor

Extracts the exercise pages of Part I (Chapters 2 through 7) from
교과서/Mathematics_for_Machine_Learning.pdf using PyMuPDF (fitz)
into chapter-specific PDFs and a combined workbook PDF.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import logging
from pathlib import Path
import sys

import fitz  # PyMuPDF


@dataclass(frozen=True)
class ChapterMetadata:
    """Metadata describing a chapter's exercise page range and target file."""

    chapter: int
    title: str
    start_page: int  # 0-based index, inclusive
    end_page: int  # 0-based index, inclusive
    filename: str

    @property
    def page_count(self) -> int:
        """Total number of exercise pages for this chapter."""
        return self.end_page - self.start_page + 1

    @property
    def page_range_1based(self) -> str:
        """1-based PDF page range representation (for human readability)."""
        return f"pp. {self.start_page + 1}-{self.end_page + 1}"


# Exact metadata for Part I (Chapters 2 - 7)
EXERCISE_CHAPTERS: list[ChapterMetadata] = [
    ChapterMetadata(
        chapter=2,
        title="Linear Algebra",
        start_page=69,
        end_page=74,
        filename="Chapter_02_Linear_Algebra_Exercises.pdf",
    ),
    ChapterMetadata(
        chapter=3,
        title="Analytic Geometry",
        start_page=101,
        end_page=102,
        filename="Chapter_03_Analytic_Geometry_Exercises.pdf",
    ),
    ChapterMetadata(
        chapter=4,
        title="Matrix Decompositions",
        start_page=142,
        end_page=143,
        filename="Chapter_04_Matrix_Decompositions_Exercises.pdf",
    ),
    ChapterMetadata(
        chapter=5,
        title="Vector Calculus",
        start_page=175,
        end_page=176,
        filename="Chapter_05_Vector_Calculus_Exercises.pdf",
    ),
    ChapterMetadata(
        chapter=6,
        title="Probability and Distributions",
        start_page=227,
        end_page=229,
        filename="Chapter_06_Probability_and_Distributions_Exercises.pdf",
    ),
    ChapterMetadata(
        chapter=7,
        title="Continuous Optimization",
        start_page=252,
        end_page=253,
        filename="Chapter_07_Continuous_Optimization_Exercises.pdf",
    ),
]

COMBINED_FILENAME = "MML_Part1_All_Exercises.pdf"
DEFAULT_REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE_PATH = DEFAULT_REPO_ROOT / "교과서" / "Mathematics_for_Machine_Learning.pdf"
DEFAULT_OUTPUT_DIR = DEFAULT_REPO_ROOT / "연습문제"


def extract_chapter_exercise(
    src_doc: fitz.Document,
    meta: ChapterMetadata,
    output_dir: Path,
) -> Path:
    """Extract exercise pages for a single chapter into a standalone PDF.

    Args:
        src_doc: Open PyMuPDF source Document.
        meta: Chapter metadata configuration.
        output_dir: Target directory where PDF will be saved.

    Returns:
        Path to the saved PDF file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / meta.filename

    new_doc = fitz.open()
    new_doc.insert_pdf(src_doc, from_page=meta.start_page, to_page=meta.end_page)

    # Add outline bookmark and document metadata
    new_doc.set_toc([[1, f"Chapter {meta.chapter}: {meta.title} Exercises", 1]])
    new_doc.set_metadata(
        {
            "title": f"MML Chapter {meta.chapter}: {meta.title} - Exercises",
            "author": "Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong",
            "subject": f"Mathematics for Machine Learning - Chapter {meta.chapter} Exercises",
            "creator": "PyMuPDF MML Exercises Extractor",
        }
    )

    new_doc.save(str(out_path))
    new_doc.close()

    logging.info(
        "[%s] Chapter %02d: %s | %s (%d pages) -> %s",
        "DONE",
        meta.chapter,
        meta.title,
        meta.page_range_1based,
        meta.page_count,
        out_path.name,
    )
    return out_path


def extract_combined_workbook(
    src_doc: fitz.Document,
    chapters: list[ChapterMetadata],
    output_path: Path,
) -> Path:
    """Extract all chapters' exercise pages into a single combined workbook PDF with TOC bookmarks.

    Args:
        src_doc: Open PyMuPDF source Document.
        chapters: Ordered list of ChapterMetadata to include.
        output_path: Target path for the combined workbook PDF.

    Returns:
        Path to the saved combined PDF file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    combined_doc = fitz.open()
    toc: list[list] = []
    current_page = 1

    for meta in chapters:
        toc.append([1, f"Chapter {meta.chapter}: {meta.title}", current_page])
        combined_doc.insert_pdf(src_doc, from_page=meta.start_page, to_page=meta.end_page)
        current_page += meta.page_count

    combined_doc.set_toc(toc)
    combined_doc.set_metadata(
        {
            "title": "Mathematics for Machine Learning - Part I Exercises",
            "author": "Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong",
            "subject": "Part I: Mathematical Foundations - Chapters 2 to 7 Exercises",
            "creator": "PyMuPDF MML Exercises Extractor",
        }
    )

    combined_doc.save(str(output_path))
    total_pages = len(combined_doc)
    combined_doc.close()

    logging.info(
        "[%s] Combined Workbook: %d chapters (%d total pages) -> %s",
        "DONE",
        len(chapters),
        total_pages,
        output_path.name,
    )
    return output_path


def run_extraction(
    source_path: Path = DEFAULT_SOURCE_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    chapters: list[int] | None = None,
    include_combined: bool = True,
    combined_only: bool = False,
) -> list[Path]:
    """Execute the exercise extraction process.

    Args:
        source_path: Path to Mathematics_for_Machine_Learning.pdf.
        output_dir: Path to directory where output PDFs will be created.
        chapters: Optional list of chapter numbers (e.g. [2, 3]) to extract. None extracts all.
        include_combined: Whether to generate the combined workbook.
        combined_only: If True, only generates the combined workbook and skips individual chapters.

    Returns:
        List of paths to generated PDF files.
    """
    if not source_path.is_file():
        raise FileNotFoundError(f"Source PDF file not found: {source_path}")

    # Filter chapters if requested
    selected_chapters = [
        meta for meta in EXERCISE_CHAPTERS
        if chapters is None or meta.chapter in chapters
    ]

    if not selected_chapters:
        raise ValueError(
            f"No valid chapters found for filter: {chapters}. Available: {[m.chapter for m in EXERCISE_CHAPTERS]}"
        )

    logging.info("=" * 70)
    logging.info("MML Part I Exercise Extraction")
    logging.info("Source PDF : %s", source_path)
    logging.info("Output Dir : %s", output_dir)
    logging.info("Chapters   : %s", [m.chapter for m in selected_chapters])
    logging.info("=" * 70)

    generated_files: list[Path] = []
    src_doc = fitz.open(str(source_path))

    try:
        # Validate that document contains all required pages
        total_source_pages = len(src_doc)
        max_required_page = max(meta.end_page for meta in selected_chapters)
        if total_source_pages <= max_required_page:
            raise ValueError(
                f"Source document has {total_source_pages} pages, but chapter requires page index {max_required_page}"
            )

        # 1. Extract individual chapter files (unless combined_only is True)
        if not combined_only:
            for meta in selected_chapters:
                out_path = extract_chapter_exercise(src_doc, meta, output_dir)
                generated_files.append(out_path)

        # 2. Extract combined workbook
        if include_combined:
            combined_path = output_dir / COMBINED_FILENAME
            out_path = extract_combined_workbook(src_doc, selected_chapters, combined_path)
            generated_files.append(out_path)

    finally:
        src_doc.close()

    logging.info("=" * 70)
    logging.info("Extraction completed successfully. %d file(s) created.", len(generated_files))
    logging.info("=" * 70)
    return generated_files


def build_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Extract Part I Exercise sections from Mathematics for Machine Learning PDF."
    )
    parser.add_argument(
        "--source",
        "-s",
        type=Path,
        default=DEFAULT_SOURCE_PATH,
        help=f"Path to source PDF file (default: {DEFAULT_SOURCE_PATH})",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save extracted exercise PDFs (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--chapters",
        "-c",
        nargs="+",
        type=int,
        choices=[meta.chapter for meta in EXERCISE_CHAPTERS],
        metavar="CH",
        help="Specific chapter numbers to extract (e.g., -c 2 3). Default: all (2 to 7).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--skip-combined",
        action="store_true",
        help="Skip generating the combined workbook PDF.",
    )
    group.add_argument(
        "--combined-only",
        action="store_true",
        help="Only generate the combined workbook PDF (skip individual chapter files).",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable debug-level logging.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    try:
        run_extraction(
            source_path=args.source.resolve(),
            output_dir=args.output_dir.resolve(),
            chapters=args.chapters,
            include_combined=not args.skip_combined,
            combined_only=args.combined_only,
        )
        return 0
    except Exception as exc:
        logging.error("Extraction failed: %s", exc, exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    sys.exit(main())
