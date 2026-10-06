from pathlib import Path
import tempfile
import json
import unittest
from unittest.mock import patch
import fitz
from _util import FIXTURES
from build_review_pdf import build_pack, publish_build, main
from review_pdf_types import ReviewPdfError

class TestBuild(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.d=Path(self.tmp.name)
        self.source=self.d/'복습문제_0101_Pdf_Test.html';self.source.write_bytes((FIXTURES/'pdf/복습문제_0101_Pdf_Test.html').read_bytes())
    def test_stage_only_pair_and_report(self):
        result=build_pack(self.source,None,self.d/'build')
        report=json.loads(result.report_path.read_text())
        self.assertEqual(report['layout'],'video-16x9');self.assertEqual(report['page_size_pt'],[1440,810]);
        self.assertEqual(report['logical_count'],2);self.assertEqual(report['range'],'0101')
        self.assertEqual(report['pages']['problems']['p1'],[1])
        self.assertTrue(result.problems_pdf.exists());self.assertTrue(result.answers_pdf.exists())
        self.assertEqual(sorted(p.name for p in self.d.glob('*pdf')),[])
        with fitz.open(result.answers_pdf) as doc:self.assertIn('ANSWER_ONLY_SENTINEL',''.join(p.get_text() for p in doc))
        self.source.write_text(self.source.read_text()+' changed')
        with self.assertRaisesRegex(ReviewPdfError,'stale'):publish_build(result,self.d/'public',self.d/'backups')
        self.assertFalse((self.d/'public').exists())
    def test_second_pdf_failure_publishes_neither(self):
        import build_review_pdf
        original=build_review_pdf.render_workbook
        def fail(payload,mode,html_path,pdf_path=None,**kwargs):
            if mode=='answers' and pdf_path is not None:raise ReviewPdfError('injected answers failure')
            return original(payload,mode,html_path,pdf_path,**kwargs)
        (self.d/'report.json').write_text('{"status":"validated"}')
        with patch('build_review_pdf.render_workbook',fail):
            self.assertEqual(main(['--review',str(self.source),'--build-dir',str(self.d/'build'),'--pdf-dir',str(self.d/'public'),'--report',str(self.d/'report.json')]),1)
        self.assertFalse((self.d/'public').exists())
        evidence=json.loads((self.d/'report.json').read_text())
        self.assertEqual(evidence['status'],'failed')
        self.assertTrue(evidence['errors'])
    def test_usage_requires_destination_or_stage_only(self):
        with self.assertRaises(SystemExit) as e:main(['--review',str(self.source),'--build-dir',str(self.d/'build'),'--report',str(self.d/'report.json')])
        self.assertEqual(e.exception.code,2)

    def test_explicit_a4_build(self):
        result=build_pack(self.source,None,self.d/'a4',layout='a4')
        with fitz.open(result.problems_pdf) as doc:self.assertAlmostEqual(doc[0].rect.width,297*72/25.4,delta=1)
        self.assertEqual(json.loads(result.report_path.read_text())['layout'],'a4')
