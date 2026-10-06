from dataclasses import replace
import unittest
from _util import FIXTURES
from review_pdf_cards import read_cards,normalize_cards
from review_pdf_types import RenderReport, LayoutIssue, ReviewPdfError
from review_pdf_pages import paginate
from review_pdf_payload import page_id

class TestPages(unittest.TestCase):
    def setUp(self):
        path=FIXTURES/'pdf/복습문제_0101_Pdf_Test.html'
        p=normalize_cards(read_cards(path),None,path)[0]
        self.ps=[replace(p,card=replace(p.card,steps=tuple(f'step {i}' for i in range(7))))]
    def measure(self,pages):
        return RenderReport(tuple(page_id(p) for p in pages),tuple(LayoutIssue(page_id(p),'work','too many steps') for p in pages if p.step_end-p.step_start>3),(),())
    def test_split_preserves_all_steps(self):
        pages=paginate(self.ps,'answers',self.measure)
        self.assertEqual([i for p in pages for i in range(p.step_start,p.step_end)],list(range(7)))
        self.assertEqual([p.continuation for p in pages],[1,2,3])
        self.assertEqual([p.show_answer for p in pages],[False,False,True])
        self.assertTrue(all(p.conditions_html==self.ps[0].conditions_html for p in pages))
        self.assertTrue(all(p.ask_html==self.ps[0].ask_html for p in pages))
    def test_unsplittable_matrix_fails(self):
        with self.assertRaisesRegex(ReviewPdfError,'p1.*unsplittable'):
            paginate(self.ps,'problems',lambda pages:RenderReport(tuple(page_id(p) for p in pages),(LayoutIssue('p1','math','wide matrix'),),(),()))
    def test_question_blocks_continue(self):
        ps=[replace(self.ps[0],ask_html='<ol><li>first</li><li>second</li><li>third</li></ol>')]
        def measure(pages):
            return RenderReport(tuple(page_id(p) for p in pages),tuple(LayoutIssue(page_id(p),'panel','ask length') for p in pages if p.ask_html.count('<li>')>1),(),())
        pages=paginate(ps,'problems',measure)
        self.assertEqual(''.join(p.ask_html for p in pages).count('<li>'),3)
        self.assertEqual([p.continuation for p in pages],[1,2,3])
        self.assertTrue(all(p.conditions_html==ps[0].conditions_html for p in pages))
    def test_missing_work_space_fails(self):
        with self.assertRaisesRegex(ReviewPdfError,'writing space'):
            paginate(self.ps,'problems',lambda pages:RenderReport(('p1',),(LayoutIssue('p1','work','missing writing space'),),(),()))

    def test_inline_emphasis_never_becomes_sentence_boundary(self):
        ps=[replace(self.ps[0],ask_html='주어진 행렬에서 <strong>고윳값을 구한 뒤</strong> 대응하는 고유벡터를 구하세요.')]
        from review_pdf_cards import parse
        def measure(pages):
            return RenderReport(tuple(page_id(p) for p in pages),tuple(LayoutIssue(page_id(p),'panel','long ask') for p in pages if len(parse(p.ask_html).text())>20),(),())
        with self.assertRaisesRegex(ReviewPdfError,'unsplittable'):
            paginate(ps,'problems',measure)

    def test_split_preserves_subquestion_numbering(self):
        ps=[replace(self.ps[0],ask_html='<ol type="a" start="3"><li>first</li><li>second</li></ol>')]
        def measure(pages):
            return RenderReport(tuple(page_id(p) for p in pages),tuple(LayoutIssue(page_id(p),'panel','ask length') for p in pages if p.ask_html.count('<li>')>1),(),())
        from review_pdf_cards import parse
        pages=paginate(ps,'problems',measure)
        attrs=[parse(p.ask_html).children[0].attrs for p in pages]
        self.assertEqual([a['type'] for a in attrs],['a','a'])
        self.assertEqual([a['start'] for a in attrs],['3','4'])
