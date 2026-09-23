from pathlib import Path
import shutil
import tempfile
import unittest

from _util import MINI_RUN

import assemble
import html2md


class TestHtml2Md(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.note, self.review = assemble.assemble(MINI_RUN, self.tmp)
        (self.note_md, self.review_md), self.figs = html2md.convert_pack(self.note, self.review)
        self.md = Path(self.note_md).read_text(encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_outputs_and_check_pass(self):
        self.assertEqual(Path(self.note_md).name, "정리노트_0101-0102_Mini_Test.md")
        self.assertEqual(html2md.check_md(self.note, self.note_md), [])
        self.assertEqual(html2md.check_md(self.review, self.review_md), [])

    def test_widget_static_becomes_figure_and_table(self):
        self.assertEqual(self.figs, 1)
        self.assertTrue((self.tmp / "figures_0101-0102" / "widget-mean-static.svg").exists())
        self.assertIn('<a id="widget-mean"></a>', self.md)
        self.assertIn("![평균 1.5 막대](figures_0101-0102/widget-mean-static.svg)", self.md)
        self.assertIn("| 1, 2 | $\\frac{3}{2}$ |", self.md)

    def test_links_rewritten_to_md(self):
        self.assertIn("(복습문제_0101-0102_Mini_Test.md)", self.md)
        review = Path(self.review_md).read_text(encoding="utf-8")
        self.assertIn("(정리노트_0101-0102_Mini_Test.md#s1-mean)", review)
        self.assertIn("**✅ 정답:**", review)

    def test_table_math_pipes(self):
        ctx = html2md.Ctx([], str(self.tmp), "figures_x")
        b = html2md.Builder()
        b.feed(r"<table><tr><th>a</th></tr><tr><td>$\|x\|$ | $|y|$</td></tr></table>")
        table = next(b.root.find_all(lambda n: n.tag == "table"))
        self.assertEqual(html2md.render_table(table, ctx)[2], r"| $\Vert x\Vert $ \| $\vert y\vert $ |")

    def test_check_md_detects_missing_math(self):
        Path(self.note_md).write_text(self.md.replace(r"\bar{x} = ", ""), encoding="utf-8")
        problems = html2md.check_md(self.note, self.note_md)
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith("수식 누락"))

    def test_bad_filename_rejected(self):
        bad = self.tmp / "note.html"
        shutil.copyfile(self.note, bad)
        with self.assertRaises(ValueError):
            html2md.convert_pack(bad, self.review)


if __name__ == "__main__":
    unittest.main()
