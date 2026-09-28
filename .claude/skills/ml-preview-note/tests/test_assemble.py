from contextlib import redirect_stdout
import io
from pathlib import Path
import shutil
import tempfile
import unittest

from _util import MINI_RUN

import preview_assemble as pa
from assemble import AssembleError  # preview_assemble이 복습 scripts 경로를 넣은 뒤라 import된다


class TestPreviewAssemble(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.note = pa.assemble(MINI_RUN, self.tmp / "out")
        self.html = self.note.read_text(encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_output_name(self):
        self.assertEqual(self.note.name, "예습노트_L99_Mini_Preview.html")

    def test_titles_brand_range(self):
        self.assertIn("<title>머신러닝기초 예습노트 L99</title>", self.html)
        self.assertIn('<strong class="brand">예습노트</strong>', self.html)
        self.assertIn('data-range="L99"', self.html)
        self.assertIn("<h1>Mini — 수업 전에 보는 예습노트</h1>", self.html)

    def test_sections_and_toc(self):
        self.assertIn('<a href="#s0">0 미리</a><a href="#s1">1 평균</a><a href="#s2">2 한눈에</a>', self.html)
        self.assertIn('<section id="s1"><h2>1. 평균과 분산</h2>', self.html)

    def test_no_slots_left(self):
        self.assertNotIn("{{", self.html)

    def test_missing_fragment_writes_nothing(self):
        run = self.tmp / "run"
        shutil.copytree(MINI_RUN, run)
        (run / "sections" / "s2.html").unlink()
        out = self.tmp / "out2"
        with self.assertRaises(AssembleError):
            pa.assemble(run, out)
        self.assertFalse(out.exists())

    def test_cli(self):
        with redirect_stdout(io.StringIO()):
            code = pa.main(["--run", str(MINI_RUN), "--out", str(self.tmp / "cli")])
        self.assertEqual(code, 0)
        self.assertTrue((self.tmp / "cli" / "예습노트_L99_Mini_Preview.html").exists())
