import json
from pathlib import Path
import shutil
import tempfile
import unittest

from _util import MINI_RUN

import assemble


class TestAssemble(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.note, self.review = assemble.assemble(MINI_RUN, self.tmp)
        self.note_html = self.note.read_text(encoding="utf-8")
        self.review_html = self.review.read_text(encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_output_names(self):
        self.assertEqual(self.note.name, "정리노트_0101-0102_Mini_Test.html")
        self.assertEqual(self.review.name, "복습문제_0101-0102_Mini_Test.html")

    def test_sections_toc_and_titles(self):
        self.assertIn('<nav class="toc" aria-label="목차"><a href="#s1">1 기초</a><a href="#s2">2 요약·예고</a></nav>', self.note_html)
        self.assertIn('<section id="s1"><h2>1. 기초 통계</h2>', self.note_html)
        self.assertIn("<h1>Mini — 테스트 정리노트</h1>", self.note_html)
        self.assertIn("<title>머신러닝기초 정리노트 0101-0102</title>", self.note_html)

    def test_scripts_moved_after_main(self):
        main_end = self.note_html.index("</main>")
        self.assertGreater(self.note_html.index('<script id="widget-mean-ui">'), main_end)

    def test_href_tokens_replaced_and_no_slots_left(self):
        self.assertIn('href="복습문제_0101-0102_Mini_Test.html"', self.note_html)
        self.assertIn('href="정리노트_0101-0102_Mini_Test.html#s1-mean"', self.review_html)
        self.assertNotIn("{{", self.note_html + self.review_html)

    def test_review_parts_progress_and_storage_key(self):
        self.assertIn('<section id="partA"><h2>A. 교과서 예제</h2>', self.review_html)
        self.assertIn('<b id="progress-count">0</b> / 1', self.review_html)
        self.assertIn("const KEY = 'mlb-review-0101-0102-done';", self.review_html)

    def test_missing_fragment_raises(self):
        run = self.tmp / "run"
        shutil.copytree(MINI_RUN, run)
        (run / "cards" / "p1.html").unlink()
        with self.assertRaises(assemble.AssembleError):
            assemble.assemble(run, self.tmp / "out")

    def test_fill_rejects_missing_slot(self):
        with self.assertRaises(assemble.AssembleError):
            assemble.fill("<p>{{NOPE}}</p>", {})

    def test_fill_does_not_expand_slots_inside_values(self):
        self.assertEqual(assemble.fill("{{A}}", {"A": "{{B}}"}), "{{B}}")


if __name__ == "__main__":
    unittest.main()
