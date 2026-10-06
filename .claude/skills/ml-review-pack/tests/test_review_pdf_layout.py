import unittest
from _util import SKILL
from review_pdf_types import ReviewPdfError
from review_pdf_layout import load_template, page_size_pt, VIDEO_TEXT_SCALE

class TestLayout(unittest.TestCase):
    def test_video_profile_and_a4_profile(self):
        self.assertEqual(page_size_pt('video-16x9'), (1440,810))
        self.assertEqual(page_size_pt('a4'), (297*72/25.4,210*72/25.4))
        self.assertAlmostEqual(VIDEO_TEXT_SCALE*10,11.339286,places=5)
        self.assertIn('1920px 1080px',load_template('problems','video-16x9'))
        self.assertIn('297mm 210mm',load_template('answers','a4'))
    def test_invalid_layout(self):
        for mode,layout in [('problems','square'),('bad','a4')]:
            with self.assertRaises(ReviewPdfError):load_template(mode,layout)

import copy
import tempfile
from pathlib import Path
import fitz
from playwright.sync_api import sync_playwright
from _util import FIXTURES
from review_pdf_cards import read_cards, normalize_cards
from review_pdf_payload import to_workbook
from review_pdf_render import render_workbook, measure_typography, _render_document
from build_review_pdf import _verify_pdf

class TestVideoLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.d=Path(cls.tmp.name)
        src=FIXTURES/'pdf/복습문제_0101_Pdf_Test.html'
        cls.ps=normalize_cards(read_cards(src),None,src)[:1]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def payload(self,mode='answers'):return to_workbook(self.ps,{},mode)
    def wide(self,payload,mode='answers',save=False):
        scales=measure_typography(payload,mode,self.d/'a4.html')
        return _render_document(payload,mode,self.d/'wide.html',self.d/'wide.pdf' if save else None,layout='video-16x9',typography=scales),scales
    def test_wide_pair_dimensions_and_separation(self):
        for mode in ['problems','answers']:
            payload=self.payload(mode);before=copy.deepcopy(payload)
            (report,actual),scales=self.wide(payload,mode,True)
            self.assertFalse(report.issues);self.assertEqual(payload,before)
            self.assertEqual(actual,scales)
            _verify_pdf(self.d/'wide.pdf',len(report.page_ids),'video-16x9')
            with fitz.open(self.d/'wide.pdf') as doc:
                self.assertEqual('ANSWER_ONLY_SENTINEL' in ''.join(p.get_text() for p in doc),mode=='answers')
                for p in doc:
                    self.assertAlmostEqual(p.rect.width,1440,delta=.1)
                    self.assertAlmostEqual(p.rect.height,810,delta=.1)
    def test_dense_text_preserves_a4_screen_size(self):
        payload=self.payload()
        payload['problems'][0]['solution']['steps']=[{'html':'긴 한국어 문장과 수식을 보존합니다. '*80+'$$x=y$$'}]
        (report,actual),scales=self.wide(payload)
        self.assertLess(scales['p1']['solution'],1)
        self.assertEqual(actual,scales)
        # Compare computed fonts, not only the profile constant.
        fonts=[]
        with sync_playwright() as pw:
            browser=pw.chromium.launch(channel='chrome',headless=True)
            try:
                page=browser.new_page();page.emulate_media(media='print')
                for name in ['a4','wide']:
                    page.goto((self.d/f'{name}.html').as_uri());page.wait_for_function("document.documentElement.dataset.ready==='true'")
                    fonts.append(page.locator('#p1 .sol-step .prose').first.evaluate('(n)=>parseFloat(getComputedStyle(n).fontSize)*72/96'))
            finally:browser.close()
        self.assertAlmostEqual(fonts[0]*900/(210*72/25.4),fonts[1]*1920/1440,delta=.1)
    def test_caption_band_rejects_text_image_and_grid(self):
        items=['<span>caption intruder</span>','<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGNgYGAAAAAEAAH2FzhVAAAAAElFTkSuQmCC" width="10" height="10">','<div style="width:40px;height:2px;background:black"></div>']
        for item in items:
            payload=self.payload();payload['problems'][0]['solution']['answer']='<div style="position:absolute;top:950px;left:50px">'+item+'</div>'
            (report,_),scales=self.wide(payload)
            self.assertTrue(any(i.area=='caption' for i in report.issues),report)
            with self.assertRaises(ReviewPdfError):render_workbook(payload,'answers',self.d/'rejected.html',self.d/'rejected.pdf',layout='video-16x9',typography=scales)
    def test_continuations_remeasure_and_missing_typography_fails(self):
        from dataclasses import replace
        from review_pdf_pages import paginate
        from review_pdf_types import LayoutIssue, RenderReport
        p=self.ps[0];p=replace(p,card=replace(p.card,steps=tuple('<p>step '+str(i)+'</p>' for i in range(8))))
        measured=[]
        def measure(pages):
            payload=to_workbook([p],{},'answers',pages)
            scales=measure_typography(payload,'answers',self.d/'candidate.html');measured.extend(scales)
            # Force one continuation using the established paginator fixture gate.
            if len(pages)==1:return RenderReport(tuple(scales),(LayoutIssue('p1','work','split'),),(),())
            return render_workbook(payload,'answers',self.d/'candidate-wide.html',layout='video-16x9',typography=scales)
        pages=paginate([p],'answers',measure)
        self.assertIn('p1-c2',measured)
        payload=to_workbook([p],{},'answers',pages)
        (report,actual),scales=self.wide(payload)
        self.assertEqual(set(actual),set(scales));self.assertEqual(set(actual),set(report.page_ids)-{i for i in report.page_ids if i.startswith('hint')})
        with self.assertRaises(ReviewPdfError):render_workbook(payload,'answers',self.d/'missing.html',layout='video-16x9',typography={})
    def test_a4_compatibility_and_wide_hint_overflow(self):
        payload=self.payload();payload['problems'][0]['hints'][0]['html']='<div style="height:600mm">hint</div>'
        self.assertTrue(any(i.area=='hint' for i in render_workbook(payload,'answers',self.d/'hint-a4.html').issues))
        (report,_),_=self.wide(payload)
        self.assertTrue(any(i.area=='hint' for i in report.issues))
    def test_pdf_caption_gate_rejects_all_ink(self):
        for kind in ['text','image','grid']:
            with fitz.open() as doc:
                p=doc.new_page(width=1440,height=810);p.insert_text((40,40),'Valid page')
                if kind=='text':p.insert_text((40,740),'intruder')
                elif kind=='image':p.insert_image(fitz.Rect(40,740,50,750),stream=fitz.Pixmap(fitz.csRGB,fitz.IRect(0,0,1,1),False).tobytes('png'))
                else:p.draw_line((40,740),(200,740),color=(0,0,0))
                path=self.d/(kind+'.pdf');doc.save(path)
            with self.assertRaisesRegex(ReviewPdfError,'caption'):_verify_pdf(path,1,'video-16x9')

    def test_real_solution_overflow_paginate(self):
        from dataclasses import replace
        from review_pdf_pages import paginate
        p=self.ps[0];p=replace(p,card=replace(p.card,steps=tuple(f'<div style="height:150px">step {i}</div>' for i in range(16))))
        def measure(pages):
            payload=to_workbook([p],{},'answers',pages)
            scales=measure_typography(payload,'answers',self.d/'long-a4.html')
            return render_workbook(payload,'answers',self.d/'long-wide.html',layout='video-16x9',typography=scales)
        pages=paginate([p],'answers',measure)
        self.assertGreater(len(pages),1)
        self.assertEqual([i for page in pages for i in range(page.step_start,page.step_end)],list(range(16)))
        self.assertFalse(measure(pages).issues)

    def test_hint_appendix_math_preserves_a4_scales(self):
        payload=self.payload()
        payload['problems'][0]['hints'][0]['html']='$$' + '+'.join(['x']*24) + '$$'
        (report,actual),scales=self.wide(payload)
        self.assertFalse(report.issues)
        self.assertLess(scales['p1']['appendix_math'][0],1)
        self.assertEqual(actual['p1']['appendix_math'],scales['p1']['appendix_math'])
        del scales['p1']['appendix_math']
        with self.assertRaises(ReviewPdfError):render_workbook(payload,'answers',self.d/'missing-hint.html',layout='video-16x9',typography=scales)

    def test_pdf_caption_gate_accounts_for_stroke_width(self):
        with fitz.open() as doc:
            p=doc.new_page(width=1440,height=810);p.insert_text((40,40),'Valid page')
            p.draw_line((40,674),(200,674),color=(0,0,0),width=8)
            path=self.d/'thick-stroke.pdf';doc.save(path)
        with self.assertRaisesRegex(ReviewPdfError,'caption'):_verify_pdf(path,1,'video-16x9')

    def test_real_question_overflow_paginate(self):
        from dataclasses import replace
        from review_pdf_pages import paginate
        p=replace(self.ps[0],ask_html=''.join(f'<p style="height:150px">Question block {i}</p>' for i in range(10)))
        def measure(pages):
            payload=to_workbook([p],{},'problems',pages)
            scales=measure_typography(payload,'problems',self.d/'long-question-a4.html')
            return render_workbook(payload,'problems',self.d/'long-question-wide.html',layout='video-16x9',typography=scales)
        pages=paginate([p],'problems',measure)
        self.assertGreater(len(pages),1)
        self.assertEqual(''.join(page.ask_html for page in pages),p.ask_html)
        self.assertFalse(measure(pages).issues)

    def test_hint_appendix_math_survives_different_page_flow(self):
        payload=self.payload()
        hint='<div style="height:120px">$$'+'+'.join(['x']*24)+'$$</div>'
        payload['problems'][0]['hints']=[{'label':f'Hint {i}','html':hint} for i in range(21)]
        (report,actual),scales=self.wide(payload)
        self.assertFalse(report.issues)
        self.assertEqual(len(scales['p1']['appendix_math']),21)
        self.assertEqual(actual['p1']['appendix_math'],scales['p1']['appendix_math'])
