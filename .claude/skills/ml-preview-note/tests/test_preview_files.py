import io
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import tempfile
import unicodedata
import unittest

import _util  # noqa: F401  (scripts 경로)
import preview_files as pf


class TestPick(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        self.lectures = self.repo / "강의노트"
        self.lectures.mkdir()
        for name in ("Lecture00_Course_Overview.pdf", "Lecture01_When_Models_Meet_Data_Part1.pdf",
                     "Lecture03_Linear_Regression_Part1.pdf", "Lecture03_Linear_Regression_Part1_rev.pdf", "notes.txt"):
            (self.lectures / name).write_bytes(b"%PDF")

    def tearDown(self):
        self._tmp.cleanup()

    def make_note(self, lecture, dir_name="예습노트"):
        d = self.repo / dir_name / lecture
        d.mkdir(parents=True)
        (d / f"예습노트_{lecture}_X.html").write_text("<html></html>", encoding="utf-8")

    def test_lists_lectures(self):
        self.assertEqual(list(pf.lecture_pdfs(self.repo)), ["L00", "L01", "L03"])

    def test_prefers_rev_and_strips_suffix(self):
        lec, pdf, slug = pf.pick(self.repo)
        self.assertEqual((lec, pdf.name, slug), ("L03", "Lecture03_Linear_Regression_Part1_rev.pdf", "Linear_Regression_Part1"))

    def test_explicit_lecture(self):
        lec, pdf, slug = pf.pick(self.repo, "L01")
        self.assertEqual((lec, slug), ("L01", "When_Models_Meet_Data_Part1"))

    def test_unknown_lecture_lists_available(self):
        with self.assertRaises(pf.PickError) as cm:
            pf.pick(self.repo, "L07")
        self.assertIn("L00, L01, L03", str(cm.exception))

    def test_latest_already_done_stops(self):
        self.make_note("L03")
        with self.assertRaises(pf.PickError) as cm:
            pf.pick(self.repo)
        self.assertIn("이미", str(cm.exception))
        self.assertIn("ajou-bb", str(cm.exception))
        self.assertEqual(pf.pick(self.repo, "L03")[0], "L03")  # 명시하면 다시 만들 수 있다

    def test_nfd_notes_dir_detected(self):
        self.make_note("L03", dir_name=unicodedata.normalize("NFD", "예습노트"))
        self.assertTrue(pf.has_note(self.repo, "L03"))

    def test_no_lectures_dir(self):
        with tempfile.TemporaryDirectory() as empty:
            with self.assertRaises(pf.PickError):
                pf.pick(empty)

    def test_cli_pick(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = pf.main(["pick", "--repo", str(self.repo)])
        self.assertEqual(code, 0)
        lec, pdf, slug = out.getvalue().strip().split("\t")
        self.assertEqual((lec, Path(pdf).name, slug), ("L03", "Lecture03_Linear_Regression_Part1_rev.pdf", "Linear_Regression_Part1"))

    def test_cli_error_exit_code(self):
        err = io.StringIO()
        with redirect_stderr(err):
            code = pf.main(["pick", "--repo", str(self.repo), "--lecture", "L07"])
        self.assertEqual(code, 1)
        self.assertIn("L07", err.getvalue())


class TestBackup(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "repo"
        self.run = Path(self._tmp.name) / "run"
        self.run.mkdir(parents=True)
        self.dir = self.repo / "예습노트" / "L03"
        self.dir.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def test_nothing_to_back_up(self):
        self.assertIsNone(pf.backup(self.repo, "L03", self.run))
        self.assertIsNone(pf.backup(self.repo, "L04", self.run))  # 폴더 자체가 없음

    def test_copies_only_this_lecture(self):
        (self.dir / "예습노트_L03_A.html").write_text("a", encoding="utf-8")
        (self.dir / "예습노트_L03_A.md").write_text("a", encoding="utf-8")
        (self.dir / "figures_L03").mkdir()
        (self.dir / "figures_L03" / "f.svg").write_text("<svg/>", encoding="utf-8")
        (self.dir / "memo.txt").write_text("x", encoding="utf-8")
        dst = pf.backup(self.repo, "L03", self.run)
        self.assertTrue(dst.name.startswith("previous-"))
        self.assertEqual(sorted(p.name for p in dst.iterdir()), ["figures_L03", "예습노트_L03_A.html", "예습노트_L03_A.md"])
        self.assertTrue((dst / "figures_L03" / "f.svg").exists())

    def test_each_backup_new_folder(self):
        (self.dir / "예습노트_L03_A.html").write_text("a", encoding="utf-8")
        a, b = pf.backup(self.repo, "L03", self.run), pf.backup(self.repo, "L03", self.run)
        self.assertNotEqual(a, b)

    def test_bad_args(self):
        with self.assertRaises(pf.PickError):
            pf.backup(self.repo, "3", self.run)
        with self.assertRaises(pf.PickError):
            pf.backup(self.repo, "L03", self.run / "missing")
