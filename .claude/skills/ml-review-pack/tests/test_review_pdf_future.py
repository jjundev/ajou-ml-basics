"""End-to-end staging semantics, including relative resources and inline math."""
from pathlib import Path
import tempfile
import unittest
import base64
from dataclasses import replace
from _util import FIXTURES
from review_pdf_cards import read_cards,normalize_cards
from review_pdf_payload import to_workbook
from review_pdf_render import render_workbook,freeze_figures
from review_pdf_types import ReviewPdfError
from check_html import parse_file,broken_links

class TestFuture(unittest.TestCase):
    def test_relative_course_links_resolve_in_isolated_stage(self):
        from review_pdf_stage import prepare_stage
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);repo=root/'repo';repo.mkdir();run=root/'run';run.mkdir()
            (repo/'강의노트').mkdir();(repo/'강의노트/lecture.pdf').write_bytes(b'lecture')
            prior=repo/'복습노트/0923';prior.mkdir(parents=True);(prior/'note.html').write_text('<html lang="ko">earlier</html>')
            stage=prepare_stage(run,repo,'0930')
            self.assertEqual(stage,(run/'work/stage/복습노트/0930').resolve())
            note=stage/'note.html';note.write_text('<a href="../0923/note.html">earlier</a><a href="../../강의노트/lecture.pdf">lecture</a>')
            self.assertEqual(broken_links(parse_file(note),stage),[])
            self.assertFalse((repo/'복습노트/0930').exists())
            self.assertEqual(prepare_stage(run,repo,'0930'),stage)
    def test_inline_matrix_overflow_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path=FIXTURES/'pdf/복습문제_0101_Pdf_Test.html'
            ps=normalize_cards(read_cards(path),None,path)[:1]
            payload=to_workbook(ps,{},'problems')
            payload['problems'][0]['html']['conditions']=r'$\begin{bmatrix}'+(' & '.join(str(i) for i in range(39)))+r'\end{bmatrix}$'
            report=render_workbook(payload,'problems',Path(d)/'inline.html')
            self.assertTrue(any(i.area=='math' for i in report.issues),report)
            with self.assertRaisesRegex(ReviewPdfError,'overflow'):
                render_workbook(payload,'problems',Path(d)/'inline.html',Path(d)/'inline.pdf')
            self.assertFalse((Path(d)/'inline.pdf').exists())
    def test_relative_image_is_source_relative(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/'복습문제_0101_Pdf_Test.html'
            text=(FIXTURES/'pdf/복습문제_0101_Pdf_Test.html').read_text().replace('조건 $a=1$ &amp; $b=5$.','조건 $a=1$ &amp; $b=5$.<img src="diagram.png">')
            source.write_text(text)
            (root/'diagram.png').write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII='))
            assets=freeze_figures(read_cards(source),root/'different/build/figures')
            self.assertIn(('p1','f1'),assets)
            self.assertTrue(assets[('p1','f1')].src.startswith('data:image/png;base64,'))
