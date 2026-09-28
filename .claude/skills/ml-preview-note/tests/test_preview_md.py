from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest

from _util import MINI_RUN

import preview_assemble as pa
import preview_md as pmd
import html2md  # preview_md가 복습 scripts 경로를 넣은 뒤


class TestPreviewMd(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.note = pa.assemble(MINI_RUN, self.tmp / "out")

    def tearDown(self):
        self._tmp.cleanup()

    def test_convert_and_check(self):
        md, figs = pmd.convert_note(self.note)
        self.assertEqual(md.name, "예습노트_L99_Mini_Preview.md")
        self.assertEqual(figs, 1)
        self.assertTrue((self.tmp / "out" / "figures_L99" / "fig-seesaw.svg").exists())
        self.assertEqual(html2md.check_md(str(self.note), str(md)), [])
        text = md.read_text(encoding="utf-8")
        self.assertIn("**들을 때 포인트**", text)
        self.assertIn("**교과서 보충**", text)

    def test_orphan_svgs_removed(self):
        figs = self.tmp / "out" / "figures_L99"
        figs.mkdir()
        (figs / "old.svg").write_text("<svg/>", encoding="utf-8")
        pmd.convert_note(self.note)
        self.assertFalse((figs / "old.svg").exists())

    def test_bad_name(self):
        other = self.note.with_name("정리노트_0101_X.html")
        other.write_text(self.note.read_text(encoding="utf-8"), encoding="utf-8")
        with self.assertRaises(ValueError):
            pmd.convert_note(other)

    def test_cli_check(self):
        with redirect_stdout(io.StringIO()):
            code = pmd.main([str(self.note), "--check"])
        self.assertEqual(code, 0)
