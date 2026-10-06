import hashlib
import tempfile
import unittest
from pathlib import Path
from _util import FIXTURES
from review_pdf_cards import read_cards, normalize_cards
from review_pdf_types import ReviewPdfError

SOURCE = FIXTURES / 'pdf/복습문제_0101_Pdf_Test.html'
class TestCards(unittest.TestCase):
    def test_preserves_entity_tex_and_step_order(self):
        pack = read_cards(SOURCE)
        self.assertEqual([c.id for c in pack.cards], ['p1','p2'])
        self.assertEqual(len(pack.cards[1].figures), 1)
        self.assertEqual(pack.cards[0].steps, ('첫 단계 $a/b$.','둘째 단계 $1/5$.'))
        self.assertIn(r'\frac{1}{5}',pack.cards[0].answer_html)
        self.assertIn('&amp;',pack.cards[0].statement_html)
        ps = normalize_cards(pack,None,SOURCE)
        self.assertIn('$a/b$',ps[0].ask_html)
        self.assertNotIn('<table',ps[1].conditions_html)
    def invalid(self, text, message):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/SOURCE.name;p.write_text(text)
            with self.assertRaisesRegex(ReviewPdfError,message):read_cards(p)
    def test_duplicate_id(self):
        self.invalid(SOURCE.read_text().replace('id="p2"','id="p1"'),'duplicate')
    def test_missing_solution(self):
        self.invalid(SOURCE.read_text().replace('class="solution"','class="missing"'),'p1.*solution')
    def test_layout_stale_source(self):
        with self.assertRaisesRegex(ReviewPdfError,'stale'):
            normalize_cards(read_cards(SOURCE),{'source_sha256':'bad','problems':{}},SOURCE)
    def test_missing_ask_and_content_loss(self):
        sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ReviewPdfError,'p1.*ask'):
            normalize_cards(read_cards(SOURCE),{'source_sha256':sha,'problems':{'p1':{'conditions_html':'x'},'p2':{}}},SOURCE)
        with self.assertRaisesRegex(ReviewPdfError,'p1.*preserv'):
            normalize_cards(read_cards(SOURCE),{'source_sha256':sha,'problems':{'p1':{'conditions_html':'changed','ask_html':'goal'},'p2':{}}},SOURCE)
