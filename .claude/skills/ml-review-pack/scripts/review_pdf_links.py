"""Patch only the links topic; preserve the rest of the note byte-for-byte."""
import html
import re
import unicodedata
from urllib.parse import unquote
from manifest import pdf_hrefs
from review_pdf_types import ReviewPdfError


def add_pdf_links(note_html,range_,slug,logical_count):
    if not re.fullmatch(r'\d{4}(?:-\d{4})?',range_) or not re.fullmatch(r'[A-Za-z0-9_]+',slug) or logical_count<1:raise ReviewPdfError('invalid PDF link metadata')
    pattern=re.compile(r'<article\b[^>]*\bclass=["\'][^"\']*\btopic\b[^"\']*["\'][^>]*>.*?</article>',re.S)
    matches=[m for m in pattern.finditer(note_html) if re.search(r'\bid=["\'][^"\']*links["\']',m.group())]
    if len(matches)!=1:raise ReviewPdfError(f'{range_}: expected one links topic')
    match=matches[0];topic=match.group()
    topic=re.sub(r'<div\b(?=[^>]*\bclass="review-pdf-links")(?=[^>]*\bdata-range="'+re.escape(range_)+r'")[^>]*>.*?</div>\s*','',topic,flags=re.S)
    legacy=f'복습문제_{range_}_{slug}.html'
    def update_anchor(m):
        if unicodedata.normalize('NFC',unquote(html.unescape(m[2])))!=legacy:return m[0]
        return m[1]+m[2]+m[3]+re.sub(r'\d+(선|문항|문제)',lambda n:f'{logical_count}{n[1]}',m[4])+m[5]
    topic=re.sub(r'(<a\b[^>]*\bhref=["\'])([^"\']+)(["\'][^>]*>)(.*?)(</a>)',update_anchor,topic,flags=re.S)
    problem,answer=pdf_hrefs(range_,slug)
    block=f'<div class="review-pdf-links" data-range="{range_}"><p>복습문제 {logical_count}문항</p><ul><li><a href="{problem}">문제지 PDF</a></li><li><a href="{answer}">해설지 PDF</a></li></ul></div>'
    topic=topic[:-len('</article>')]+block+'</article>'
    return note_html[:match.start()]+topic+note_html[match.end():]
