"""SKILL.md 형식과, 본문이 가리키는 파일이 모두 있는지 확인한다."""

import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unicodedata
import unittest

from _util import SKILL

SKILL_MD = SKILL / "SKILL.md"


class TestSkillFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL_MD.read_text(encoding="utf-8")

    def test_frontmatter(self):
        m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", self.text)
        self.assertIsNotNone(m, "frontmatter는 name, description 두 줄")
        self.assertEqual(m.group(1), "ml-review-pack")
        self.assertIn("정리노트", m.group(2))
        self.assertIn("복습문제", m.group(2))
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_referenced_files_exist(self):
        refs = set(re.findall(r"(?:references|scripts|assets)/[\w.-]+\.(?:md|py|html)", self.text))
        self.assertGreaterEqual(len(refs), 12)
        for rel in sorted(refs):
            with self.subTest(rel=rel):
                self.assertTrue((SKILL / rel).exists(), rel)

    def test_every_reference_is_used(self):
        for path in sorted((SKILL / "references").glob("*.md")):
            with self.subTest(ref=path.name):
                self.assertIn(f"references/{path.name}", self.text)

    def test_stage_two_selection_precedes_planner(self):
        stage = self.text.split("\n### 2. ", 1)[1].split("\n### 3. ", 1)[0]
        selection, planning = stage.split("#### 2b. 기획과 작성 준비", 1)
        self.assertIn("#### 2a. 문항 선별 판정", selection)
        for term in ("8~12문항", "WITHHELD", "RUN/problem-pages.txt",
                     "gaps.levels", "기획 없이 종료"):
            self.assertIn(term, selection)
        self.assertNotIn("기획 담당 1명", selection)
        self.assertIn("`PASS` 후 기획 담당 1명", planning)
        self.assertIn("기획은 진행하고 발행은 별도로 판단", selection)
        self.assertIn("갱신 대상 팩은 중복 대조에서 제외", selection)
        self.assertIn("기존 문항도 출처와 수업 범위를 다시 확인", selection)

    def test_stage_two_verifies_planner_after_completion(self):
        planning = self.text.split("#### 2b. 기획과 작성 준비", 1)[1].split("\n### 3. ", 1)[0]
        self.assertLess(planning.index("완료 신호"), planning.index("완료 후 한 번에 검증"))
        for term in ("작업자 ID", "파일 폴링 금지", "타임아웃", "메인 직접 수행",
                     "2a 재판정", "토픽 ID", "예시 검산", "3단계 진입"):
            self.assertIn(term, planning)
        report = self.text.split("\n### 9. 보고", 1)[1]
        self.assertIn("최초 보류면 기획 미실행", report)
        self.assertIn("재판정 보류면 이미 실행한 기획", report)

    def test_problem_explain_handoff(self):
        ref = SKILL / 'references/problem-explain.md'
        self.assertTrue(ref.is_file(), 'full explanation handoff is missing')
        self.assertIn('references/problem-explain.md', self.text)
        text = ref.read_text(encoding='utf-8')
        for term in ('ABS_REVIEW', 'extract', '저작', '독립', 'source_visual', 'content', 'independent', 'browser', 'publish', '보류'):
            self.assertIn(term, text)
        sections = re.split(r'\n### \d+\. ', self.text)
        self.assertIn('mpe_cli.py', sections[1])
        self.assertIn('references/problem-explain.md', sections[9])
        self.assertIn('문제설명 보류', sections[10])

    def test_steps_present(self):
        for n in range(10):
            with self.subTest(step=n):
                self.assertRegex(self.text, rf"\n### {n}\. ")


class TestBackupSnippet(unittest.TestCase):
    """SKILL.md 4단계 백업 스니펫(python 부분)을 임시 폴더에서 실제로 실행한다."""

    @classmethod
    def setUpClass(cls):
        text = SKILL_MD.read_text(encoding="utf-8")
        m = re.search(r"```bash\nRANGE=<range> REPO=… RUN=… python3 - <<'EOF'\n(.*?)\nEOF\n```", text, re.S)
        assert m, "SKILL.md 4단계 백업 스니펫을 찾지 못함"
        cls.code = m.group(1)

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.notes = self.tmp / "repo" / "복습노트"
        self.notes.mkdir(parents=True)
        self.run_dir = self.tmp / "run"
        self.run_dir.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def backup(self, range_):
        env = dict(os.environ, RANGE=range_, REPO=str(self.tmp / "repo"), RUN=str(self.run_dir))
        return subprocess.run([sys.executable, "-"], input=self.code, env=env, capture_output=True, text=True)

    def backups(self):
        return sorted(p for p in self.run_dir.iterdir() if p.name.startswith("previous-"))

    def test_nothing_to_back_up(self):
        r = self.backup("0921")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("백업할 기존 팩 없음", r.stdout)
        self.assertEqual(self.backups(), [])

    def test_backs_up_nfc_and_nfd_names_into_fresh_dirs(self):
        (self.notes / "정리노트_0921_A.html").write_text("n", encoding="utf-8")
        (self.notes / unicodedata.normalize("NFD", "복습문제_0921_A.md")).write_text("r", encoding="utf-8")
        (self.notes / "정리노트_0921-0923_B.html").write_text("other range", encoding="utf-8")
        (self.notes / "figures_0921").mkdir()
        (self.notes / "figures_0921" / "a.svg").write_text("<svg/>", encoding="utf-8")
        for _ in range(2):  # 같은 세션에서 다시 실행해도 이전 백업을 덮지 않는다
            r = self.backup("0921")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("백업 3항목(파일 3개)", r.stdout)
        dirs = self.backups()
        self.assertEqual(len(dirs), 2)
        for d in dirs:
            names = sorted(unicodedata.normalize("NFC", n) for n in os.listdir(d))
            self.assertEqual(names, ["figures_0921", "복습문제_0921_A.md", "정리노트_0921_A.html"])
            self.assertTrue((d / "figures_0921" / "a.svg").exists())

    def test_backs_up_dated_folder_layout(self):
        # 새 형식: 복습노트/<range>/ 안의 산출물. 폴더명이 NFD여도, 다른 range 폴더는 건드리지 않는다.
        pack = self.notes / "0921"
        (pack / "figures_0921").mkdir(parents=True)
        (pack / "figures_0921" / "a.svg").write_text("<svg/>", encoding="utf-8")
        (pack / "정리노트_0921_A.html").write_text("n", encoding="utf-8")
        (pack / unicodedata.normalize("NFD", "복습문제_0921_A.md")).write_text("r", encoding="utf-8")
        (self.notes / "0923").mkdir()
        (self.notes / "0923" / "정리노트_0923_B.html").write_text("other", encoding="utf-8")
        r = self.backup("0921")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("백업 3항목(파일 3개)", r.stdout)
        (d,) = self.backups()
        names = sorted(unicodedata.normalize("NFC", n) for n in os.listdir(d))
        self.assertEqual(names, ["figures_0921", "복습문제_0921_A.md", "정리노트_0921_A.html"])

    def test_backs_up_pack_subfolder(self):
        # .pack 형식: HTML은 날짜 폴더, MD·PDF·그림은 그 아래 .pack/.
        day = self.notes / "0921"
        (day / ".pack" / "figures_0921").mkdir(parents=True)
        (day / ".pack" / "figures_0921" / "a.svg").write_text("<svg/>", encoding="utf-8")
        (day / "정리노트_0921_A.html").write_text("n", encoding="utf-8")
        (day / ".pack" / "복습문제_0921_A.md").write_text("r", encoding="utf-8")
        (day / ".pack" / "복습문제_0921_A-문제.pdf").write_bytes(b"%PDF")
        r = self.backup("0921")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("백업 4항목(파일 4개)", r.stdout)
        (d,) = self.backups()
        names = sorted(unicodedata.normalize("NFC", n) for n in os.listdir(d))
        self.assertEqual(names, ["figures_0921", "복습문제_0921_A-문제.pdf", "복습문제_0921_A.md", "정리노트_0921_A.html"])

    def test_bad_range_fails_loudly(self):
        (self.notes / "정리노트_0921_A.html").write_text("n", encoding="utf-8")
        for bad in ("", "<range>", "921"):
            with self.subTest(bad=bad):
                r = self.backup(bad)
                self.assertEqual(r.returncode, 1)
                self.assertIn("백업 중단", r.stderr)
        self.assertEqual(self.backups(), [])


if __name__ == "__main__":
    unittest.main()
