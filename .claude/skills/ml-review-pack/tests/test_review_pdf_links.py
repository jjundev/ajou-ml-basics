import tempfile
import unittest
from pathlib import Path
from _util import MINI_RUN
from review_pdf_links import add_pdf_links
from review_pdf_types import ReviewPdfError
from manifest import pdf_names
from assemble import assemble,AssembleError

class TestLinks(unittest.TestCase):
    def setUp(self):
        self.note='<article class="topic" id="s5-links"><p>본문 $x^2$ &amp; 수식.</p><ul><li><a href="복습문제_0914_ERM_and_MLE.html">0914 복습문제 8선 풀러 가기</a></li></ul></article><script>const a="unchanged";</script>'
    def test_idempotent_links_and_correct_count(self):
        once=add_pdf_links(self.note,'0914','ERM_and_MLE',7)
        self.assertEqual(add_pdf_links(once,'0914','ERM_and_MLE',7),once)
        self.assertIn('복습문제_0914_ERM_and_MLE-문제.pdf',once)
        self.assertIn('복습문제_0914_ERM_and_MLE-답안.pdf',once)
        self.assertIn('복습문제 7선',once);self.assertNotIn('8선',once)
        self.assertEqual(pdf_names('0914','ERM_and_MLE'),('복습문제_0914_ERM_and_MLE-문제.pdf','복습문제_0914_ERM_and_MLE-답안.pdf'))
    def test_preserve_unrelated_content(self):
        once=add_pdf_links(self.note,'0914','ERM_and_MLE',7)
        self.assertIn('<p>본문 $x^2$ &amp; 수식.</p>',once)
        self.assertTrue(once.endswith('<script>const a="unchanged";</script>'))
        self.assertIn('href="복습문제_0914_ERM_and_MLE.html"',once)
    def test_pdf_links_missing_pair_writes_neither(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)
            with self.assertRaisesRegex(AssembleError,'PDF'):assemble(MINI_RUN,out,include_pdf_links=True)
            self.assertEqual(list(out.iterdir()),[])

class TestLegacyCounts(unittest.TestCase):
    def test_count_in_parenthetical_korean_label(self):
        for unit in ['문제','문항']:
            note=f'<article class="topic" id="s5-links"><a href="복습문제_0909_Data_Models_Learning.html">복습문제 풀러 가기 (0909 수업 범위 7{unit})</a></article>'
            updated=add_pdf_links(note,'0909','Data_Models_Learning',5)
            self.assertIn(f'수업 범위 5{unit}',updated)
            self.assertNotIn(f'7{unit}',updated)
