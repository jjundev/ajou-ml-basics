"""Chromium may rasterize a background as a full-page image including white space."""
from pathlib import Path
import io
import sys
import fitz
from PIL import Image, ImageDraw
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_review_pdf import _verify_pdf
from review_pdf_types import ReviewPdfError

def pdf_with_background(path, ink_in_caption):
    image = Image.new('RGB', (1440, 810), 'white')
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 20, 80, 80), fill='black')
    if ink_in_caption:
        draw.rectangle((20, 700, 30, 710), fill='black')
    data = io.BytesIO(); image.save(data, format='PNG')
    doc = fitz.open(); page = doc.new_page(width=1440, height=810)
    page.insert_image(page.rect, stream=data.getvalue())
    page.insert_text((100, 100), 'Problem 1')
    doc.save(path); doc.close()

def test_full_page_raster_with_white_caption_is_allowed(tmp_path):
    path = tmp_path / 'white.pdf'; pdf_with_background(path, False)
    _verify_pdf(path, 1, 'video-16x9')

def test_actual_image_ink_in_caption_is_rejected(tmp_path):
    path = tmp_path / 'ink.pdf'; pdf_with_background(path, True)
    with pytest.raises(ReviewPdfError, match='caption band'):
        _verify_pdf(path, 1, 'video-16x9')
