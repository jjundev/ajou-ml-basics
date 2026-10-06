import base64
from dataclasses import replace
import tempfile
import unittest
from pathlib import Path
import fitz
from PIL import Image
import io
from unittest.mock import patch
from _util import FIXTURES
from review_pdf_cards import read_cards, normalize_cards
from review_pdf_payload import to_workbook
from review_pdf_render import freeze_figures, render_workbook
from review_pdf_types import ReviewPdfError,FigureInput

class TestRender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.d=Path(cls.tmp.name)
        cls.source=FIXTURES/'pdf/복습문제_0101_Pdf_Test.html'
        cls.pack=read_cards(cls.source);cls.ps=normalize_cards(cls.pack,None,cls.source)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_table_and_graph_visible(self):
        graph='<svg viewBox="0 0 200 80" width="200" height="80"><defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="#1b2130"/></marker></defs><line class="fig-ink" x1="30" y1="35" x2="170" y2="35" marker-end="url(#arr)"/><text class="fig-text" x="10" y="35">x1</text><text class="fig-text" x="175" y="35">x2</text></svg>'
        pack=replace(self.pack,cards=(replace(self.pack.cards[0],figures=(FigureInput('graph',graph,'svg'),)),self.pack.cards[1]))
        assets=freeze_figures(pack,self.d/'media')
        for asset in assets.values():
            im=Image.open(io.BytesIO(base64.b64decode(asset.src.split(',',1)[1])))
            self.assertGreater(im.width,100);self.assertGreater(asset.h_mm,0)
            self.assertEqual(im.convert('RGB').getpixel((0,0)),(255,255,255))
            self.assertLess(im.convert('RGB').getextrema()[0][0],100)
    def test_pdf_pair_dimensions_searchable_and_answer_separation(self):
        assets=freeze_figures(self.pack,self.d/'table')
        for mode in ['problems','answers']:
            pdf=self.d/f'{mode}.pdf'
            report=render_workbook(to_workbook(self.ps,assets,mode),mode,self.d/f'{mode}.html',pdf)
            self.assertFalse(report.issues)
            with fitz.open(pdf) as doc:
                self.assertGreaterEqual(len(doc),2)
                text=''.join(p.get_text() for p in doc)
                self.assertIn('한글 수식',text)
                self.assertEqual('ANSWER_ONLY_SENTINEL' in text,mode=='answers')
                for page in doc:
                    self.assertAlmostEqual(page.rect.width*25.4/72,297,delta=1)
                    self.assertAlmostEqual(page.rect.height*25.4/72,210,delta=1)
                    self.assertTrue(page.get_text().strip())
    def test_answer_only_overflow(self):
        payload=to_workbook(self.ps[:1],{},'answers')
        payload['problems'][0]['solution']['answer']='<div style="height:300mm">oversized answer</div>'
        report=render_workbook(payload,'answers',self.d/'overflow.html')
        self.assertTrue(any(i.area=='answer' for i in report.issues))
    def test_hint_only_overflow(self):
        payload=to_workbook(self.ps[:1],{},'answers')
        payload['problems'][0]['hints'][0]['html']='<div style="height:600mm">oversized hint</div>'
        report=render_workbook(payload,'answers',self.d/'hint-overflow.html')
        self.assertTrue(any(i.area=='hint' for i in report.issues))
    def test_resource_failure(self):
        payload=to_workbook(self.ps[:1],{},'problems')
        payload['problems'][0]['figures']=[{'src':(self.d/'absent.png').as_uri(),'w_mm':20,'h_mm':20}]
        with self.assertRaisesRegex(ReviewPdfError,'resource'):render_workbook(payload,'problems',self.d/'broken.html')
    def test_network_failure(self):
        from playwright.sync_api import BrowserContext
        original=BrowserContext.new_page
        def blocked(context):
            page=original(context);page.route('https://cdn.jsdelivr.net/**',lambda route:route.abort());return page
        with patch.object(BrowserContext,'new_page',blocked):
            with self.assertRaisesRegex(ReviewPdfError,'resource'):
                render_workbook(to_workbook(self.ps[:1],{},'problems'),'problems',self.d/'network.html')
