"""Pinned workbook templates and output profiles; no external checkout required."""
from pathlib import Path
import re
from typing import Literal, TypedDict
from review_pdf_types import Mode, ReviewPdfError

Layout = Literal['a4', 'video-16x9']
class PageTypography(TypedDict):
    panel: float
    solution: float
    math: list[float]
    hints: list[float]
    appendix_math: list[float]
Typography = dict[str, PageTypography]
ASSETS = Path(__file__).resolve().parent.parent / 'assets'
VIDEO_TEXT_SCALE = (900 / (210 * 72 / 25.4)) / (1920 / 1440)

def page_size_pt(layout: Layout) -> tuple[float, float]:
    if layout == 'a4': return (297 * 72 / 25.4, 210 * 72 / 25.4)
    if layout == 'video-16x9': return (1440, 810)
    raise ReviewPdfError(f'invalid layout: {layout}')

def load_template(mode: Mode, layout: Layout = 'a4') -> str:
    page_size_pt(layout)
    if mode not in ('problems', 'answers'): raise ReviewPdfError(f'invalid mode: {mode}')
    html = (ASSETS / ('pdf-problem.html' if mode == 'problems' else 'pdf-answer.html')).read_text(encoding='utf-8')
    if layout == 'video-16x9':
        html = re.sub(r'(font-size|--fs-body)(\s*:\s*)([0-9.]+)pt',
                      lambda m: f'{m[1]}{m[2]}{float(m[3]) * VIDEO_TEXT_SCALE:.6f}pt', html)
        css = (ASSETS / 'pdf-video-16x9.css').read_text(encoding='utf-8')
        html = html.replace('</head>', '<style>' + css + '</style><script>window.workbookVideoLayout=true;</script></head>')
    return html
