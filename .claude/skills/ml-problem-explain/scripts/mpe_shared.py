"""Narrow adapter to the course's existing card, Markdown, publication APIs."""
import sys
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / 'ml-review-pack/scripts'
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))
from review_pdf_cards import read_cards, normalize_cards, parse, inner, outer, compact
from review_pdf_types import REVIEW, HOMEWORK, ReviewPdfError
from html2md import Node, Ctx, convert, check_md
from check_html import math_delimiter_errors
from review_pdf_publish import publish_files
