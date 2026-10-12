import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents/skills/ml-stt"
CLAUDE_DIR = ROOT / ".claude/skills/ml-stt"


class MlSttTests(unittest.TestCase):
    def setUp(self):
        import sys
        scripts_dir = str(SKILL_DIR / "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)

    def test_01_skill_entrypoints_and_metadata(self):
        skill_md = SKILL_DIR / "SKILL.md"
        self.assertTrue(skill_md.is_file(), "SKILL.md must exist in .agents/skills/ml-stt/")
        # Ensure it is NOT linked into .claude/skills (disallow Claude)
        self.assertFalse(CLAUDE_DIR.exists(), ".claude/skills/ml-stt must NOT exist (disallow Claude)")

        content = skill_md.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "SKILL.md must have frontmatter")
        import yaml
        parts = content.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "Frontmatter must be enclosed by ---")
        frontmatter = yaml.safe_load(parts[1])
        self.assertIsInstance(frontmatter, dict, "Frontmatter must parse into a valid dict")
        self.assertEqual(frontmatter.get("name"), "ml-stt")
        self.assertIn("Gemini Only", frontmatter.get("description", ""))
        self.assertIn("Model Compatibility Gate", content, "SKILL.md must contain Model Compatibility Gate")
        self.assertIn("STT/<MMDD> 머러기.md", content, "SKILL.md must document standard output path")

    def test_02_all_agents_skills_frontmatter_valid(self):
        import glob
        import yaml

        skill_files = glob.glob(str(ROOT / ".agents/skills/**/SKILL.md"), recursive=True)
        self.assertGreater(len(skill_files), 0, "There should be skills in .agents/skills")

        for s_file in skill_files:
            text = Path(s_file).read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---"), f"{s_file} must have frontmatter")
            parts = text.split("---", 2)
            self.assertGreaterEqual(len(parts), 3, f"{s_file} frontmatter malformed")
            data = yaml.safe_load(parts[1])
            self.assertIsInstance(data, dict, f"{s_file} frontmatter did not parse as dict")
            self.assertIn("name", data, f"{s_file} missing name")
            self.assertIn("description", data, f"{s_file} missing description")

    def test_03_parse_date(self):
        from infer_context import parse_date

        self.assertEqual(parse_date("20261005_머러기.m4a"), "1005")
        self.assertEqual(parse_date("1005 머러기.mp3"), "1005")
        self.assertEqual(parse_date("1005.m4a"), "1005")
        self.assertEqual(parse_date("녹음_1001.wav"), "1001")
        self.assertEqual(parse_date("/path/to/2026-0928-class.m4a"), "0928")
        self.assertEqual(parse_date("audio.m4a", date_override="1005"), "1005")

        with self.assertRaises(ValueError):
            parse_date("audio_without_date.m4a")

    def test_04_infer_lecture(self):
        from infer_context import infer_lecture

        lec_0909 = infer_lecture(ROOT, "0909")
        self.assertEqual(lec_0909, 1)

        lec_1007 = infer_lecture(ROOT, "1007")
        self.assertEqual(lec_1007, 4)

    def test_05_build_stt_prompt(self):
        from infer_context import build_stt_prompt

        prompt = build_stt_prompt(lecture_num=4, lecture_title="Probability_Distributions", terms=["가우시안", "우도", "MLE"])
        self.assertIn("머신러닝기초", prompt)
        self.assertIn("정방철 교수님", prompt)
        self.assertIn("ECE3512", prompt)
        self.assertIn("Lecture04", prompt)
        self.assertIn("Probability_Distributions", prompt)
        self.assertIn("가우시안", prompt)
        self.assertIn("MLE", prompt)

    def test_06_merge_transcripts(self):
        import tempfile
        from merge_transcripts import merge_transcripts

        with tempfile.TemporaryDirectory() as tmpdir:
            part1 = Path(tmpdir) / "1005_머러기_part01.md"
            part2 = Path(tmpdir) / "1005_머러기_part02.md"
            part1.write_text("첫 번째 파트 발화 내용입니다.\n\n가우시안 분포에 대해 설명합니다.\n", encoding="utf-8")
            part2.write_text("두 번째 파트 발화 내용입니다.\n\n최대우도추정(MLE)을 다룹니다.\n", encoding="utf-8")

            out_file = Path(tmpdir) / "1005 머러기.md"
            res = merge_transcripts(
                target_dir=tmpdir,
                prefix="1005_머러기",
                out_file=str(out_file),
                keep_parts=True,
            )
            self.assertTrue(out_file.is_file())
            content = out_file.read_text(encoding="utf-8")
            self.assertIn("# 1005_머러기 전체 오디오 전사본", content)
            self.assertIn("## Part 01", content)
            self.assertIn("## Part 02", content)
            self.assertIn("가우시안 분포에 대해 설명합니다.", content)
            self.assertIn("최대우도추정(MLE)을 다룹니다.", content)

            # Test timestamp stripping when timestamps=False
            part3 = Path(tmpdir) / "1005_머러기_part03.md"
            part3.write_text("01:23\n이 문장은 타임스탬프가 붙어있습니다.\n", encoding="utf-8")
            res_stripped = merge_transcripts(
                target_dir=tmpdir,
                prefix="1005_머러기",
                out_file=str(out_file),
                keep_parts=True,
                timestamps=False,
            )
            content_stripped = out_file.read_text(encoding="utf-8")
            self.assertNotIn("01:23", content_stripped)
            self.assertIn("이 문장은 타임스탬프가 붙어있습니다.", content_stripped)


if __name__ == "__main__":
    unittest.main()
