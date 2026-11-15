"""Patch only the links topic; preserve the rest of the note byte-for-byte."""
import html
import re
import unicodedata
from urllib.parse import unquote, urlsplit
from manifest import pdf_hrefs
from review_pdf_types import ReviewPdfError


def add_pdf_links(note_html,range_,slug,logical_count, *, pdf_only=False):
    if not re.fullmatch(r'\d{4}(?:-\d{4})?',range_) or not re.fullmatch(r'[A-Za-z0-9_]+',slug) or logical_count<1:raise ReviewPdfError('invalid PDF link metadata')
    pattern=re.compile(r'<article\b[^>]*\bclass=["\'][^"\']*\btopic\b[^"\']*["\'][^>]*>.*?</article>',re.S)
    matches=[m for m in pattern.finditer(note_html) if re.search(r'\bid=["\'][^"\']*links["\']',m.group())]
    if len(matches)!=1:raise ReviewPdfError(f'{range_}: expected one links topic')
    match=matches[0];topic=match.group()
    topic=re.sub(r'<div\b(?=[^>]*\bclass="review-pdf-links")(?=[^>]*\bdata-range="'+re.escape(range_)+r'")[^>]*>.*?</div>\s*','',topic,flags=re.S)
    legacy=f'복습문제_{range_}_{slug}.html'
    problem,answer=pdf_hrefs(range_,slug)
    def update_anchor(m):
        if unicodedata.normalize('NFC',unquote(html.unescape(m[2])))!=legacy:return m[0]
        return m[1]+(problem if pdf_only else m[2])+m[3]+re.sub(r'\d+(선|문항|문제)',lambda n:f'{logical_count}{n[1]}',m[4])+m[5]
    topic=re.sub(r'(<a\b[^>]*\bhref=["\'])([^"\']+)(["\'][^>]*>)(.*?)(</a>)',update_anchor,topic,flags=re.S)
    block=f'<div class="review-pdf-links" data-range="{range_}"><p>복습문제 {logical_count}문항</p><ul><li><a href="{problem}">문제지 PDF</a></li><li><a href="{answer}">해설지 PDF</a></li></ul></div>'
    topic=topic[:-len('</article>')]+block+'</article>'
    return note_html[:match.start()]+topic+note_html[match.end():]


def problem_pages(pdf_path, problems):
    """Return only page jumps confirmed by the PDF's visible problem headers."""
    import fitz
    from collections import defaultdict

    declared = {p.id: p.source for p in problems}
    matches = defaultdict(list)
    with fitz.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf, 1):
            header = page.get_text(clip=fitz.Rect(0, 0, page.rect.width, 50))
            label = re.search(r'(?:예제|연습문제|자작)\s*(P[1-9]\d*)(?!\d)', header)
            if label and (problem := label[1].lower()) in declared and declared[problem] in header:
                matches[problem].append(page_no)
    return {p: pages[0] for p, pages in matches.items() if len(pages) == 1}


def relocate_problem_links(text, document, pdf, page_moves):
    """Refresh links to the rebuilt problem PDF and preserve unrelated links."""
    pattern = (r'(\]\()([^\s)]+)(\))' if document.suffix == '.md'
               else r'(\bhref\s*=\s*["\'])([^"\']+)(["\'])')

    def replace(match):
        raw = match[2]
        path, separator, fragment = raw.partition('#')
        page = re.fullmatch(r'page=([1-9]\d*)', fragment)
        if not separator or not page:
            return match[0]
        parsed = urlsplit(html.unescape(path))
        if parsed.scheme or parsed.netloc or (document.parent / unquote(parsed.path)).resolve() != pdf:
            return match[0]
        new_page = page_moves.get(int(page[1]))
        return match[1] + path + (f'#page={new_page}' if new_page else '') + match[3]

    return re.sub(pattern, replace, text)
