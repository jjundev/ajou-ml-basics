from pathlib import Path
import tempfile
import json
import unittest
from unittest.mock import patch
import fitz
from _util import FIXTURES
from build_review_pdf import build_pack, publish_build, main
from review_pdf_types import HOMEWORK, ReviewPdfError

class TestBuild(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.d=Path(self.tmp.name)
        self.source=self.d/'복습문제_0101_Pdf_Test.html';self.source.write_bytes((FIXTURES/'pdf/복습문제_0101_Pdf_Test.html').read_bytes())
    def test_stage_only_pair_and_report(self):
        result=build_pack(self.source,None,self.d/'build')
        report=json.loads(result.report_path.read_text(encoding='utf-8'))
        self.assertEqual(report['layout'],'video-16x9');self.assertEqual(report['page_size_pt'],[1440,810]);
        self.assertEqual(report['logical_count'],2);self.assertEqual(report['range'],'0101')
        self.assertEqual(report['pages']['problems']['p1'],[1])
        self.assertEqual(report['profile'],'review')
        self.assertTrue(result.problems_pdf.exists());self.assertTrue(result.answers_pdf.exists())
        self.assertEqual(sorted(p.name for p in self.d.glob('*pdf')),[])
        with fitz.open(result.answers_pdf) as doc:self.assertIn('ANSWER_ONLY_SENTINEL',''.join(p.get_text() for p in doc))
        self.source.write_text(self.source.read_text(encoding='utf-8')+' changed', encoding='utf-8')
        with self.assertRaisesRegex(ReviewPdfError,'stale'):publish_build(result,self.d/'public',self.d/'backups')
        self.assertFalse((self.d/'public').exists())
    def test_second_pdf_failure_publishes_neither(self):
        import build_review_pdf
        original=build_review_pdf.render_workbook
        def fail(payload,mode,html_path,pdf_path=None,**kwargs):
            if mode=='answers' and pdf_path is not None:raise ReviewPdfError('injected answers failure')
            return original(payload,mode,html_path,pdf_path,**kwargs)
        (self.d/'report.json').write_text('{"status":"validated"}', encoding='utf-8')
        with patch('build_review_pdf.render_workbook',fail):
            self.assertEqual(main(['--review',str(self.source),'--build-dir',str(self.d/'build'),'--pdf-dir',str(self.d/'public'),'--report',str(self.d/'report.json')]),1)
        self.assertFalse((self.d/'public').exists())
        evidence=json.loads((self.d/'report.json').read_text(encoding='utf-8'))
        self.assertEqual(evidence['status'],'failed')
        self.assertTrue(evidence['errors'])
    def test_usage_requires_destination_or_stage_only(self):
        with self.assertRaises(SystemExit) as e:main(['--review',str(self.source),'--build-dir',str(self.d/'build'),'--report',str(self.d/'report.json')])
        self.assertEqual(e.exception.code,2)
    def test_homework_profile_build(self):
        import build_review_pdf
        source=self.d/'과제9_Pdf_Test.html';source.write_bytes((FIXTURES/'pdf/과제9_Pdf_Test.html').read_bytes())
        seen=[];original=build_review_pdf.render_workbook
        def spy(payload,mode,html_path,pdf_path=None,**kwargs):
            seen.append(payload['meta']['title']);return original(payload,mode,html_path,pdf_path,**kwargs)
        with patch('build_review_pdf.render_workbook',spy):result=build_pack(source,None,self.d/'hw',profile=HOMEWORK)
        self.assertEqual(set(seen),{'머신러닝기초 과제9'})
        self.assertEqual((result.problems_pdf.name,result.answers_pdf.name),('과제9_Pdf_Test-문제.pdf','과제9_Pdf_Test-답안.pdf'))
        report=json.loads(result.report_path.read_text(encoding='utf-8'))
        self.assertEqual((report['profile'],report['range'],report['logical_count'],report['status']),('homework','9',2,'validated'))
        with fitz.open(result.problems_pdf) as doc:
            text=''.join(p.get_text() for p in doc)
        self.assertIn('과제',text);self.assertIn('HW9 Problem 1',text);self.assertNotIn('ANSWER_ONLY_SENTINEL',text)
        with fitz.open(result.answers_pdf) as doc:self.assertIn('ANSWER_ONLY_SENTINEL',''.join(p.get_text() for p in doc))
    def test_cli_profile_flag(self):
        args=['--review',str(self.source),'--build-dir',str(self.d/'b'),'--stage-only','--report',str(self.d/'r.json')]
        with patch('build_review_pdf.build_pack',side_effect=ReviewPdfError('stop')) as bp:
            self.assertEqual(main(['--profile','homework',*args]),1)
        self.assertIs(bp.call_args.kwargs['profile'],HOMEWORK)
        with self.assertRaises(SystemExit) as e:main(['--profile','nope',*args])
        self.assertEqual(e.exception.code,2)

    def test_explicit_a4_build(self):
        result=build_pack(self.source,None,self.d/'a4',layout='a4')
        with fitz.open(result.problems_pdf) as doc:self.assertAlmostEqual(doc[0].rect.width,297*72/25.4,delta=1)
        self.assertEqual(json.loads(result.report_path.read_text(encoding='utf-8'))['layout'],'a4')
